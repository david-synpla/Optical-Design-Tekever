"""Re-evaluate all saved A06 attempts using image-centered clearance and exact fields."""
import json,csv,shutil
import numpy as np
import matplotlib.pyplot as plt
from track_a_run004_screen import OUT,ROOT,FIELDS,KEEP,EPD,build,evaluate
from track_a_run002_corrector_comparison import build_bare

def engineering(v,n=35):
    l,origin,norm,tan=build(v)
    rp,spacing=v[11:13] if len(v)>11 else (-600,180)
    m=evaluate(v,n);center=np.array(m['detector_center_mm'])
    active_hits=[];footprints=[[],[],[]];hole=[];cloud=[]
    for fx,fy in FIELDS:
        ray=l.trace(fx/float(l.fields.max_field),fy/float(l.fields.max_field),.55,num_rays=n,distribution='uniform')
        points={i:np.column_stack([np.asarray(l.surfaces[i].x),np.asarray(l.surfaces[i].y),np.asarray(l.surfaces[i].z)]) for i in range(1,6)}
        count=0
        for a,b in [(1,2),(2,3),(3,4)]:
            pa=points[a];delta=points[b]-pa
            frac=((center-pa)@norm)/(delta@norm)
            hit=pa+frac[:,None]*delta
            good=(frac>=0)&(frac<=1)&(np.asarray(l.surfaces[a].intensity)>0)
            localx=(hit-center)[:,0];localy=(hit-center)@tan
            count+=int(np.sum(good&(np.abs(localx)<=11.22304/2)&(np.abs(localy)<=8.22/2)))
        active_hits.append(count)
        for idx,sidx in enumerate([2,3,4]):
            p=points[sidx];live=np.asarray(l.surfaces[sidx].intensity)>0
            pos=np.array([0,0,spacing]) if sidx==2 else np.array([0,0,0]) if sidx==3 else np.array([0,v[8],v[5]])
            angle=0 if sidx==2 else v[10] if sidx==3 else v[7]
            tang=np.array([0,np.cos(angle),np.sin(angle)])
            rho=np.hypot((p-pos)[:,0],(p-pos)@tang)
            footprints[idx].extend(rho[live]);cloud.extend(p[live])
        pa=points[3];delta=points[4]-pa;frac=(spacing-pa[:,2])/delta[:,2]
        hit=pa+frac[:,None]*delta;live=np.asarray(l.surfaces[3].intensity)>0
        hole.extend(np.hypot(hit[live,0],hit[live,1]))
    radii=[max(f) for f in footprints];curv=[rp,v[0],v[3]];conic=[v[1],v[2],v[4]]
    slopes=[float(r/np.sqrt(R*R-(1+k)*r*r)) for r,R,k in zip(radii,curv,conic)]
    dep=[]
    for r,R,k in zip(radii,curv,conic):
        z=(r*r/R)/(1+np.sqrt(1-(1+k)*r*r/R**2))
        zs=(r*r/R)/(1+np.sqrt(1-r*r/R**2))
        dep.append(float((z-zs)*1000))
    base=max(m['rms_um']);sens=[]
    for name,index,amount in [('tertiary y +10 um',8,.01),('tertiary tilt +0.01 deg',7,np.deg2rad(.01)),('secondary tilt +0.01 deg',10,np.deg2rad(.01))]:
        test=np.array(v);test[index]+=amount;q=evaluate(test,19)
        sens.append(dict(perturbation=name,worst_rms_um=max(q['rms_um']),minimum_clearance_mm=min(q['min_detector_clearance_mm']),note='Detector plane follows build parameterization; centroid recentered, not a fixed-mechanics tolerance analysis.'))
    return dict(active_sensor_hit_counts_by_field=active_hits,mirror_footprint_max_radius_mm=radii,
                mirror_max_conic_slope=slopes,conic_departure_from_vertex_sphere_at_footprint_um=dep,
                required_primary_hole_ray_radius_at_vertex_plane_mm=max(hole),
                sampled_mirror_ray_extent_xyz_mm=np.ptp(np.array(cloud),axis=0).tolist(),
                perturbation_probes=sens)

def baseline(n):
    l=build_bare();rms=[];through=[]
    for x,y in FIELDS:
        r=l.trace(x/float(l.fields.max_field),y/float(l.fields.max_field),.55,num_rays=n,distribution='uniform')
        good=np.asarray(r.i)>0;s=l.surfaces[-1]
        q=np.column_stack([np.asarray(s.x),np.asarray(s.y)])[good]
        rms.append(float(np.sqrt(np.mean(np.sum((q-q.mean(axis=0))**2,axis=1)))*1000))
        through.append(float(np.mean(good)))
    return dict(rms_um=rms,throughput=through)

def audit():
    cases=[]
    for path in sorted(OUT.glob('attempt_*.json')):
        d=json.loads(path.read_text());v=d['values']
        m=evaluate(v,35,True)
        cases.append(dict(attempt=d['attempt'],values=v,metrics=m,engineering=engineering(v)))
    wavecheck={str(c['attempt']):{str(w):evaluate(c['values'],19,wavelength=w)['rms_um'] for w in [.43,.55,.65,.80]} for c in cases}
    convergence={str(c['attempt']):{str(n):{'worst_rms_um':max((q:=evaluate(c['values'],n))['rms_um']),
                                           'minimum_clearance_mm':min(q['min_detector_clearance_mm'])} for n in [19,35,51]} for c in cases if c['attempt'] in [1,4]}
    data={'fields_deg':FIELDS,'wavelengths_um':[.43,.55,.65,.80],
          'geometrical_band_check':wavecheck,'pupil_sampling_convergence':convergence,
          'baseline_A01_same_sampling':baseline(35),'cases':cases,
          'audit_note':'Exact normalized field coordinates and detector keepout centered on on-axis image centroid. Earlier attempt 1/2 optimization evaluated nominal detector origin; superseded for physical decisions by this audit.'}
    compact={**data,'cases':[{**c,'metrics':{k:v for k,v in c['metrics'].items() if k!='traces'}} for c in cases]}
    (OUT/'audit.json').write_text(json.dumps(compact,indent=2)+'\n')
    print(json.dumps(compact,indent=2))
    fig,ax=plt.subplots(figsize=(9,4.5))
    ax.plot(range(9),data['baseline_A01_same_sampling']['rms_um'],'ko-',label='A01 flat detector')
    for c in cases:ax.plot(range(9),c['metrics']['rms_um'],'o-',label=f"A06 attempt {c['attempt']}")
    ax.set(xlabel='Field index (3 x 3 grid; center = 4)',ylabel='RMS spot radius (um)',title='Common flat-detector screening comparison')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'spot_comparison.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.5))
    for c in cases:ax.plot(range(9),c['metrics']['min_detector_clearance_mm'],'o-',label=f"A06 attempt {c['attempt']}")
    ax.axhline(KEEP,color='k',ls='--',label='Active half-diagonal + 1 mm assumption')
    ax.set(xlabel='Field index',ylabel='Minimum ray distance from image center (mm)',title='Detector clearance audit (sampled finite ray segments)')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'clearance.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.5))
    for ax,idx in zip(axes,[0,3]):
        case=cases[idx];v=case['values'];m=case['metrics'];l,c,norm,tan=build(v);c=np.array(m['detector_center_mm'])
        for field_idx in [0,4,8]:
            paths=np.array(m['traces'][field_idx])
            for j in range(0,paths.shape[1],max(1,paths.shape[1]//25)):
                path=paths[:,j,:]
                ax.plot(path[:,2],path[:,1],lw=.35,alpha=.4)
        for sidx in [2,3,4]:
            s=l.surfaces[sidx];pos=np.array([float(s.geometry.cs.z),float(s.geometry.cs.y)])
            ax.plot(pos[0],pos[1],'ko');ax.text(pos[0],pos[1]+8,f'M{sidx-1}',fontsize=8)
        ends=np.array([c-tan*KEEP,c+tan*KEEP]);ax.plot(ends[:,2],ends[:,1],'r-',lw=3,label='Detector circular keepout diameter')
        ax.set(xlabel='z (mm)',ylabel='y (mm)',title=f"A06 attempt {case['attempt']} sampled ray layout")
        ax.set_aspect('equal',adjustable='datalim');ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(OUT/'layout.png',dpi=160);plt.close(fig)

if __name__=='__main__':audit()
