"""Nominal equivalence, rigid-body invariants, window and clearance diagnostics."""
import sys,copy,json,hashlib,csv
from pathlib import Path
import numpy as np
from optiland.physical_apertures import RadialAperture
import track_b_run010_sensitivity as m

class WindowCandidate(m.Candidate):
    thickness=0.
    def build(self,errors={}):
        o=super().build(errors)
        if self.thickness==0:return o
        t=self.thickness;last=len(o.surfaces)-1;sign=-1 if self.b06 else 1
        old=[copy.deepcopy(s.geometry.cs) for s in o.surfaces];z=float(old[-1].z)
        o.surfaces[last-1].thickness-=sign*(1+t)
        o.surfaces.add(index=last,thickness=sign*t,material='N-BK7',aperture=RadialAperture(10))
        o.surfaces.add(index=last+1,thickness=sign,material='air',aperture=RadialAperture(10))
        # Insertion must not reposition any pre-existing surface or detector.
        for i,cs in enumerate(old):o.surfaces[i if i<last else i+2].geometry.cs=cs
        o.surfaces[last].geometry.cs.z=z-sign*(1+t)
        o.surfaces[last+1].geometry.cs.z=z-sign
        return o

def clearance(c,errors={},extra=0):
    o=c.build(errors);_,met,hist=c.sample(errors,n=16,waves=[.55]);obs=[]
    for i in ([2,3,4] if c.b06 else [2,3]):
        s=o.surfaces[i];ap=s.aperture;g=s.geometry;cy=float(getattr(ap,'offset_y',0));cx=float(getattr(ap,'offset_x',0));r=float(ap.r_max)
        th=np.linspace(0,2*np.pi,128,endpoint=False);rr=np.linspace(0,r,5)
        xx=(cx+rr[:,None]*np.cos(th)).ravel();yy=(cy+rr[:,None]*np.sin(th)).ravel()
        zz=m.sag(np.hypot(xx,yy),float(g.radius),float(g.k));p=np.column_stack([xx,yy,zz]);origin,R=g.cs.get_effective_transform();p=p@np.asarray(R).T+np.asarray(origin)
        center=(p[:,:2].min(axis=0)+p[:,:2].max(axis=0))/2
        radius=float(np.max(np.linalg.norm(p[:,:2]-center,axis=1)))+extra
        # Existing B06 mirror patches already include 2 mm radial allowance.
        obs.append(dict(index=i,center=center,radius=radius,zlo=float(p[:,2].min())-(2 if c.b06 else 0),
            zhi=float(p[:,2].max())+(2 if c.b06 else 0),inner=0 if c.b06 or i==3 else max(0,21.5-extra)))
    minimum=1e9;limiter=None
    for xx,yy,zz in hist:
        for i in range(len(o.surfaces)-1):
            for ob in obs:
                j=ob['index']
                if j in [i,i+1]:continue
                dz=zz[i+1]-zz[i];safe=abs(dz)>1e-15
                den=np.where(safe,dz,1);a=(ob['zlo']-zz[i])/den;b=(ob['zhi']-zz[i])/den
                lo=np.maximum(0,np.minimum(a,b));hi=np.minimum(1,np.maximum(a,b));ok=(lo<=hi)&safe
                if not ok.any():continue
                bx=xx[i]-ob['center'][0];by=yy[i]-ob['center'][1];vx=xx[i+1]-xx[i];vy=yy[i+1]-yy[i]
                tt=np.clip(-(bx*vx+by*vy)/np.maximum(vx*vx+vy*vy,1e-30),lo,hi)
                dist=np.hypot(bx+tt*vx,by+tt*vy)-ob['radius']
                if ob['inner']:
                    maxr=np.maximum(np.hypot(bx+lo*vx,by+lo*vy),np.hypot(bx+hi*vx,by+hi*vy))
                    dist=np.maximum(dist,ob['inner']-maxr)
                val=float(dist[ok].min())
                if val<minimum:minimum=val;limiter=[i,i+1,j]
    return dict(minimum_mirror_envelope_clearance_mm=minimum,limiting_segment_obstacle=limiter,
        additional_radial_cell_allowance_mm=extra,minimum_survival=met['minimum_survival'],
        note='Sampled conservative circular/axial slabs; excludes real supports, detector body, baffles. Negative added-volume result identifies an interface risk, not a real cell collision.')

def run(cid):
    c=m.Candidate(cid);nom=c.nom;replay=c.build({});fields=[(0,0),(m.A.HX,m.A.HY)]
    px,py=c.pupil(6);diff=0
    for field in fields:
        for wl in m.WAVES:
            a=nom.ray_tracer.trace_generic(*field,px,py,wl);b=replay.ray_tracer.trace_generic(*field,px,py,wl)
            diff=max(diff,float(np.max(abs(np.array([a.x,a.y])-np.array([b.x,b.y])))))
    assert diff<1e-12
    r0,met,_=c.sample();rd,md,_=c.sample({'detector_x':.01})
    assert np.max(abs(r0-rd))<1e-10
    assert np.max(abs(np.array(md['centroids_mm'])-np.array(met['centroids_mm'])-[-.01,0]))<1e-10
    moved=c.build({'secondary_z':.01})
    for i in range(1,len(nom.surfaces)):
        delta=float(moved.surfaces[i].geometry.cs.z-nom.surfaces[i].geometry.cs.z)
        assert abs(delta-(.01 if i==3 else 0))<1e-12
    # Surface radii/conics must be unchanged for rigid-body perturbations.
    moved=c.build({'secondary_tx':.0001})
    assert all(float(a.geometry.radius)==float(b.geometry.radius) for a,b in zip(nom.surfaces,moved.surfaces))
    # Original nominal prescription export, including all global coordinates.
    pres=[]
    for i,s in enumerate(nom.surfaces):
        pres.append(dict(index=i,radius_mm=float(s.geometry.radius) if np.isfinite(s.geometry.radius) else None,
            conic=float(getattr(s.geometry,'k',0)),thickness_mm=float(s.thickness) if np.isfinite(s.thickness) else None,
            cs=s.geometry.cs.to_dict() if i else None,aperture=s.aperture.to_dict() if s.aperture else None,
            material=str(getattr(s.material_post,'name',type(s.material_post).__name__))))
    m.save(Path(cid)/'nominal_prescription.json',pres)
    window=WindowCandidate(cid);z=np.load(m.OUT/cid/'jacobian.npz');names=[d['name'] for d in c.defs];j=z['J'][:,names.index('detector_z')]
    windows=[]
    for t in [.5,1.]:
        window.thickness=t;rr,raw,_=window.sample();q=-float(j@(rr-r0)/(j@j))*.01
        _,fixed,_=window.sample({'detector_z':q})
        windows.append(dict(thickness_mm=t,glass='N-BK7 diagnostic surrogate',exit_to_detector_mm=1.,clear_radius_mm=10.,
            unrefocused=raw,linear_detector_refocus_global_z_mm=q,refocused=fixed))
    lhs=m.read(Path(cid)/'lhs.json');idx=lhs['summary']['focus_secondary_tilt']['worst_case'];case=m.read(Path(cid)/'lhs'/f'{idx:03}.json')
    errors=case['compensated']['focus_secondary_tilt']['total_errors']
    report=dict(nominal_replay_max_coordinate_difference_mm=diff,detector_decenter_translation_invariant=True,
        isolated_secondary_despace_invariant=True,rigid_body_shape_unchanged=True,window_scenarios=windows,
        nominal_clearance=clearance(c),perturbed_compensated_clearance=clearance(c,errors),
        illustrative_extra_cell_volume=clearance(c,errors,2),
        detector_package='No actual detector-body drawing or window specification supplied. Active-area-only nominal margins are not package certification.')
    m.save(Path(cid)/'interfaces.json',report);print(cid,json.dumps({k:v for k,v in report.items() if k not in ['window_scenarios']}),flush=True)

if __name__=='__main__':run(sys.argv[1])
