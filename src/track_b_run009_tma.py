"""Independent B06 off-axis-pupil three-mirror screening.

Fresh ABCD/Petzval seeds, no Track A or B05 prescription imports.
Virtual parent pupil is larger than the physical 128 mm subaperture.
"""
import sys,json,time,shutil,hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.optimize import least_squares
from optiland import optic
from optiland.physical_apertures import OffsetRadialAperture
import yaml,optiland,scipy

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
REQ=yaml.safe_load((ROOT/'requirements/eo_requirements.yaml').read_text())['source_explicit_requirements']
F=REQ['pixel_pitch_um'][0]*1000/REQ['instantaneous_fov_urad_per_pixel']; D=F/REQ['f_number']
W,H=np.array(REQ['array_px'])*REQ['pixel_pitch_um'][0]/1000
ANG=np.degrees(np.arctan(np.hypot(W,H)/(2*F)))
HX=np.degrees(np.arctan(W/(2*F)))/ANG; HY=np.degrees(np.arctan(H/(2*F)))/ANG
FIELDS=[(a*HX,b*HY) for a in [-1,0,1] for b in [-1,0,1]]


def first_order_grid():
    candidates=[]
    # Unfolded powers (+,-,+). Petzval sum zero is a starting condition,
    # not evidence of anastigmatic full-field correction.
    for f1 in np.linspace(2*D,3.5*D,9):
        p1=1/f1
        for frac in np.linspace(.80,.95,9):
            d12=frac*f1; a=1-d12*p1
            for frac23 in np.linspace(.55,.95,9):
                d23=frac23*d12
                roots=np.roots([-d23*a,d12*d23*p1*p1,-d12*p1*p1-1/F])
                for root in roots:
                    if abs(root.imag)>1e-8 or root.real<=0:continue
                    p3=float(root.real);p2=-p1-p3
                    c2=-p1-p2*a; a3=a+d23*c2; c3=c2-p3*a3
                    q=-a3/c3
                    if not 50<q<500 or a3>=0:continue
                    z=np.array([0,-d12,-d12+d23,-d12+d23-q])
                    if not z[3]<z[1]-10:continue
                    for offset in [85.,100.,115.]:
                        centers=np.array([offset,a*offset,a3*offset,0.])
                        radii=np.array([D/2,abs(a)*D/2,abs(a3)*D/2,np.hypot(W,H)/2])+2
                        # Incoming beam must clear secondary/tertiary/detector.
                        incoming=min(abs(offset-centers[j])-D/2-radii[j] for j in [1,2,3])
                        # Tertiary-to-detector bundle at the secondary vertex.
                        t=(z[1]-z[2])/(z[3]-z[2])
                        yc=(1-t)*centers[2];rad=(1-t)*radii[2]+t*radii[3]
                        sec_clear=abs(yc-centers[1])-rad-radii[1]
                        if min(incoming,sec_clear)<2:continue
                        candidates.append(dict(f1=f1,d12=d12,d23=d23,powers=[p1,p2,p3],q=q,offset=offset,
                            vertex_z=z.tolist(),centers_y=centers.tolist(),radii=radii.tolist(),
                            paraxial_clearance_mm=min(incoming,sec_clear),
                            score=float(np.ptp(z)+.5*(offset+D/2)+100*max(p3-.015,0))))
    return sorted(candidates,key=lambda r:r['score'])


def build(seed,ks,focus=0,apertures=None):
    p1,p2,p3=seed['powers'];d12=seed['d12'];d23=seed['d23'];q=seed['q']+focus
    offset=seed['offset']; parent_radius=offset+D/2
    o=optic.Optic(name='B06 independent off-axis-pupil TMA screen')
    o.surfaces.add(index=0,thickness=np.inf)
    o.surfaces.add(index=1,thickness=d12+10,is_stop=True,
        aperture=OffsetRadialAperture(D/2,offset_y=offset) if apertures else None)
    for idx,r,t,k in [(2,-2/p1,-d12,ks[0]),(3,2/p2,d23,ks[1]),(4,-2/p3,-q,ks[2])]:
        aperture=None
        if apertures:
            v=apertures[idx-2]; aperture=OffsetRadialAperture(v['radius'],offset_x=v['x'],offset_y=v['y'])
        o.surfaces.add(index=idx,radius=r,thickness=t,conic=k,material='mirror',aperture=aperture)
    o.surfaces.add(index=5)
    o.set_aperture(aperture_type='EPD',value=2*parent_radius)
    o.fields.set_type('angle');o.fields.add(y=0);o.fields.add(y=ANG)
    for wl in [.43,.55,.8]:o.wavelengths.add(value=wl,is_primary=wl==.55)
    return o


def pupil(seed,n=9):
    axis=np.linspace(-1,1,n);xx,yy=np.meshgrid(axis,axis);keep=xx*xx+yy*yy<=1
    parent_radius=seed['offset']+D/2
    return xx[keep]*D/2/parent_radius,(yy[keep]*D/2+seed['offset'])/parent_radius


def trace(o,seed,field,n=9,wl=.55):
    px,py=pupil(seed,n)
    r=o.ray_tracer.trace_generic(*field,px,py,wl)
    points=np.column_stack([r.x,r.y]);valid=np.isfinite(points).all(axis=1)&(np.asarray(r.i)>0)
    return points,valid


def audit(seed,ks,focus=0,n=17):
    o=build(seed,ks,focus);data=[]; bundles=[]
    for field in FIELDS:
        p,valid=trace(o,seed,field,n)
        if not np.all(valid):return dict(valid=False,reason='invalid ray',valid_fraction=float(valid.mean()))
        data.append(dict(field=field,centroid=p.mean(axis=0).tolist(),rms_um=float(np.sqrt(np.mean(np.sum((p-p.mean(axis=0))**2,axis=1)))*1000)))
        bundles.append((np.array(o.surfaces.x),np.array(o.surfaces.y),np.array(o.surfaces.z)))
    # Local detector image-scale Jacobian about center, not the parent f/#.
    eps=1e-4;centers=[]
    for field in [(eps,0),(-eps,0),(0,eps),(0,-eps)]:
        p,v=trace(o,seed,field,n);centers.append(p.mean(axis=0))
    jac=np.column_stack([(centers[0]-centers[1])/(2*eps*np.radians(ANG)),(centers[2]-centers[3])/(2*eps*np.radians(ANG))])
    fxy=np.linalg.norm(jac,axis=0)
    apertures=[]
    for idx in [2,3,4]:
        points=np.concatenate([np.column_stack([xx[idx],yy[idx]]) for xx,yy,zz in bundles])
        center=(points.max(axis=0)+points.min(axis=0))/2
        rad=float(np.max(np.linalg.norm(points-center,axis=1)))+2
        apertures.append(dict(x=float(center[0]),y=float(center[1]),radius=rad))
    detcenter=np.array(data[4]['centroid'])
    # Conservative axial slabs around true conic sags over each circular patch.
    obstacles=[]
    for idx,ap in zip([2,3,4],apertures):
        geom=o.surfaces[idx].geometry; rmin=max(0,np.hypot(ap['x'],ap['y'])-ap['radius']);rmax=np.hypot(ap['x'],ap['y'])+ap['radius']
        radii=np.linspace(rmin,rmax,100);c=1/float(geom.radius);k=float(geom.k)
        radicand=1-(1+k)*c*c*radii*radii
        if min(radicand)<=0:return dict(valid=False,reason='patch beyond real conic domain')
        sag=c*radii*radii/(1+np.sqrt(radicand));vertex=float(np.asarray(o.surfaces.positions).ravel()[idx])
        obstacles.append(dict(index=idx,x=ap['x'],y=ap['y'],radius=ap['radius'],zlo=vertex+float(min(sag))-2,zhi=vertex+float(max(sag))+2))
    zdet=float(np.asarray(o.surfaces.positions).ravel()[5])
    obstacles.append(dict(index=5,x=float(detcenter[0]),y=float(detcenter[1]),radius=float(np.hypot(W,H)/2+1),zlo=zdet-1,zhi=zdet+1))
    minclear=1e9;worst=None
    for xx,yy,zz in bundles:
        for i in range(1,5):
            for obs in obstacles:
                if obs['index'] in [i,i+1]:continue
                dz=zz[i+1]-zz[i]
                ta=(obs['zlo']-zz[i])/dz;tb=(obs['zhi']-zz[i])/dz
                low=np.maximum(0,np.minimum(ta,tb));high=np.minimum(1,np.maximum(ta,tb));ok=low<=high
                if not np.any(ok):continue
                vx=xx[i+1]-xx[i];vy=yy[i+1]-yy[i];bx=xx[i]-obs['x'];by=yy[i]-obs['y']
                den=vx*vx+vy*vy
                t=np.clip(-(bx*vx+by*vy)/np.maximum(den,1e-30),low,high)
                dist=np.hypot(bx+t*vx,by+t*vy)-obs['radius']
                val=float(np.min(dist[ok]))
                if val<minclear:minclear=val;worst=[i,i+1,obs['index']]
    return dict(valid=True,worst_rms_um=max(row['rms_um'] for row in data),fields=data,
                local_image_scale_mm=fxy.tolist(),jacobian=jac.tolist(),parent_efl_mm=float(o.paraxial.f2()),
                physical_epd_mm=D,virtual_parent_epd_mm=2*(seed['offset']+D/2),
                apertures=apertures,minimum_unintended_clearance_mm=minclear,worst_segment_obstacle=worst,
                detector_center_mm=detcenter.tolist(),obstacles=obstacles)


def merit(v,seed):
    ks=v[:3];focus=v[3];o=build(seed,ks,focus);values=[]
    for field in [(0,0),(HX,0),(0,HY),(HX,HY),(-HX,-HY)]:
        p,valid=trace(o,seed,field,9)
        if not np.all(valid):return np.full(5*len(p)*2+2,1e5)
        values.extend(((p-p.mean(axis=0))/.02).ravel())
    centers=[];eps=.001
    for field in [(eps,0),(-eps,0),(0,eps),(0,-eps)]:
        p,valid=trace(o,seed,field,9);centers.append(p.mean(axis=0))
    scales=[np.linalg.norm(centers[0]-centers[1])/(2*eps*np.radians(ANG)),np.linalg.norm(centers[2]-centers[3])/(2*eps*np.radians(ANG))]
    values.extend((np.array(scales)-F)/.25)
    return np.asarray(values)


def main():
    seeds=first_order_grid()
    if '--probe' in sys.argv:
        print('paraxial seed count',len(seeds))
        for seed in seeds[:3]:print(json.dumps(dict(seed=seed,audit=audit(seed,[-1,-1,-1])),indent=2)[:1300])
        return
    out=ROOT/'runs/run_009';out.mkdir(exist_ok=False);start=time.monotonic();stamp=datetime.now(timezone.utc).isoformat()
    (out/'paraxial_seeds.json').write_text(json.dumps(seeds,indent=2)+'\n')
    seed=seeds[0];initial=audit(seed,[-1,-1,-1]);records=[]
    (out/'initial.json').write_text(json.dumps(initial,indent=2)+'\n')
    fit=least_squares(merit,[-1,-1,-1,0],args=(seed,),bounds=([-15,-30,-15,-100],[0,0,0,100]),
        x_scale='jac',max_nfev=90,ftol=1e-5,xtol=1e-6,gtol=1e-5)
    result=audit(seed,fit.x[:3],fit.x[3],25)
    (out/'attempt_01.json').write_text(json.dumps(dict(seed=seed,parameters=fit.x.tolist(),metrics=result,nfev=fit.nfev,
        message=fit.message,seconds=time.monotonic()-start),indent=2)+'\n')
    shutil.copy2(__file__,out/'model.py');shutil.copy2(ROOT/'requirements/eo_requirements.yaml',out/'requirements.yaml')
    (out/'metadata.json').write_text(json.dumps(dict(track='B',candidate_ids=['B06'],run='009',parent_run=None,
        stage='screening',purpose='Can a fresh off-axis-pupil three-mirror topology clear itself and justify development?',
        start_utc=stamp,end_utc=datetime.now(timezone.utc).isoformat(),substantial_search_count=2,
        materially_distinct_attempt_count=1,plateau=False,versions={'python':sys.version,'optiland':optiland.__version__,'scipy':scipy.__version__},
        assumptions=['Petzval sum zero seed condition','Off-axis pupil offsets 85/100/115 mm','2 mm mirror patch/slab margins and 1 mm active-detector margin',
        'Coatings/thermal/tolerances unmodeled','Circular bounds enclose active rectangular detector; no customer packaging limit'],
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
    print(json.dumps(result,indent=2)[:3000])


if __name__=='__main__':main()
