"""Bounded A06 screen. WSL Optiland; no external/reference architecture input.

Run from project root. Results are incremental; refuse overwrite of attempt files.
Angles radians, positions mm. Detector local coordinates obtained by projection.
"""
import json, math, time, sys, argparse, importlib.metadata as md
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from optiland import optic, physical_apertures
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'requirements/eo_requirements.yaml').is_file())
OUT=ROOT/'runs/run_004'
EFL=794.2029; EPD=128.0972
FIELDS=[(x,y) for y in [-0.296503,0,0.296503] for x in [-0.4048225,0,0.4048225]]
KEEP=math.hypot(11.22304/2,8.22/2)+1
# r2,k1,k2,r3,k3,z3,return,tertiary tilt,tertiary y,detector tilt correction,secondary tilt
SEED=[-478.1239794,-0.81787692,-6.22422687,-160.48941193,-0.26925286,382.07144145,185.94169476,0.10,0,0,0]

def build(v):
    r2,k1,k2,r3,k3,z3,b,t,y,dt,ts=v[:11]
    rp,spacing=v[11:13] if len(v)>11 else (-600,180)
    # Plane normal under Optiland's active rotation convention.
    center=np.array([0., y+b*math.sin(2*t),z3-b*math.cos(2*t)])
    ang=2*t+dt
    normal=np.array([0.,-math.sin(ang),math.cos(ang)])
    tangent=np.array([0.,math.cos(ang),math.sin(ang)])
    l=optic.Optic(name='A06 tilted/decentered three-conic-mirror screening')
    ap=physical_apertures.RadialAperture
    l.surfaces.add(index=0,z=-math.inf,radius=math.inf)
    l.surfaces.add(index=1,z=0,aperture=ap(r_max=65,r_min=29))
    l.surfaces.add(index=2,z=spacing,radius=rp,conic=k1,material='mirror',is_stop=True,aperture=ap(r_max=65))
    l.surfaces.add(index=3,z=0,radius=r2,conic=k2,rx=ts,material='mirror',aperture=ap(r_max=29))
    l.surfaces.add(index=4,z=z3,y=y,rx=t,radius=r3,conic=k3,material='mirror',aperture=ap(r_max=45))
    l.surfaces.add(index=5,z=center[2],y=center[1],rx=ang)
    l.set_aperture(aperture_type='EPD',value=EPD)
    l.fields.set_type('angle')
    for x,f in FIELDS:l.fields.add(x=x,y=f)
    for w in [.43,.55,.65,.80]:l.wavelengths.add(value=w,is_primary=w==.55)
    return l,center,normal,tangent

def evaluate(v,n=7,details=False,wavelength=.55):
    l,c,norm,tan=build(v); spots=[]; cent=[]; clear=[]; thru=[]; traces=[]
    ray=l.trace(0,0,wavelength,num_rays=n,distribution='uniform')
    s=l.surfaces[5]
    p=np.column_stack([np.asarray(s.x),np.asarray(s.y),np.asarray(s.z)])
    mean=p[np.asarray(ray.i)>0].mean(axis=0)
    c=c+np.array([mean[0]-c[0],0,0])+tan*np.dot(mean-c,tan)
    for fx,fy in FIELDS:
        ray=l.trace(fx/float(l.fields.max_field),fy/float(l.fields.max_field),wavelength,num_rays=n,distribution='uniform')
        surfaces=[]
        for s in l.surfaces:
            surfaces.append(np.column_stack([np.asarray(s.x),np.asarray(s.y),np.asarray(s.z)]))
        p=surfaces[5]; valid=np.asarray(ray.i)>0
        if sum(valid)<4:raise ValueError('too few rays')
        q=np.column_stack([(p-c)[:,0],(p-c)@tan])[valid]
        mean=q.mean(axis=0);cent.append(mean);spots.append(np.sqrt(np.mean(np.sum((q-mean)**2,axis=1)))*1000)
        thru.append(float(np.mean(valid)))
        # Only intersections on actual finite non-imaging segments count.
        distances=[]
        for a,b in [(1,2),(2,3),(3,4)]:
            pa,pb=surfaces[a],surfaces[b]; d=pb-pa
            frac=((c-pa)@norm)/(d@norm)
            hit=pa+frac[:,None]*d
            live=np.asarray(l.surfaces[a].intensity)>0
            inside=(frac>=0)&(frac<=1)&live
            if inside.any():distances.extend(np.linalg.norm(hit[inside]-c,axis=1))
        clear.append(float(min(distances)) if len(distances) else 1000.)
        if details:traces.append([a.tolist() for a in surfaces[1:]])
    cent=np.asarray(cent)
    ex=(cent[5,0]-cent[3,0])/(2*math.tan(math.radians(.4048225)))
    ey=(cent[7,1]-cent[1,1])/(2*math.tan(math.radians(.296503)))
    result=dict(rms_um=spots,centroids_mm=cent.tolist(),efl_xy_mm=[float(abs(ex)),float(abs(ey))],
                min_detector_clearance_mm=clear,throughput=thru,detector_center_mm=c.tolist())
    if details:result['traces']=traces
    return result

def residual(v,stage):
    try:
        m=evaluate(v,n=11 if stage>=4 else 7)
        r=np.r_[np.array(m['rms_um'])/5,(np.array(m['efl_xy_mm'])-EFL)/1.,
            np.maximum(0,KEEP-np.array(m['min_detector_clearance_mm']))/(.08 if stage>=4 else .3),
            np.maximum(0,.75-np.array(m['throughput']))/(.05 if stage>=4 else .02)]
        if not np.all(np.isfinite(r)):raise ValueError('nonfinite')
        return r
    except (ValueError,RuntimeError,IndexError,FloatingPointError):return np.full(29,1e5)

def main():
    p=argparse.ArgumentParser();p.add_argument('--attempt',type=int);p.add_argument('--diagnostic',action='store_true');args=p.parse_args()
    if args.diagnostic:
        print(json.dumps(evaluate(SEED,11),indent=2));return
    stage=args.attempt; dest=OUT/f'attempt_{stage}.json'
    if dest.exists():raise FileExistsError(dest)
    seed=np.array(SEED)
    low=np.array([-850,-3,-15,-1500,-15,300,140,.035,-20,-.15,-.05])
    high=np.array([-250,1,2,-60,3,450,280,.22,20,.15,.05])
    # Progressive freedom: tilted tertiary; decentered tertiary; secondary tilt.
    active=list(range(8)) if stage==1 else list(range(10 if stage==2 else 11))
    if stage>1:
        prev=json.loads((OUT/f'attempt_{stage-1}.json').read_text());seed=np.array(prev['values'])
    if stage==5:
        seed=np.r_[seed,-600.,180.];low=np.r_[low,-850.,130.];high=np.r_[high,-450.,240.]
        active=list(range(13))
    def expand(x):
        v=seed.copy();v[active]=x;return v
    start=time.time()
    res=least_squares(lambda x:residual(expand(x),stage),seed[active],bounds=(low[active],high[active]),
                      max_nfev=300 if stage>=4 else 110,x_scale='jac',ftol=2e-5,diff_step=2e-5)
    v=expand(res.x);m=evaluate(v,19,True)
    data=dict(attempt=stage,values=v.tolist(),metrics=m,nfev=res.nfev,cost=res.cost,
              message=res.message,seconds=time.time()-start,active_indices=active,
              software={k:md.version(k) for k in ['optiland','numpy','scipy']},python=sys.version)
    dest.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:val for k,val in data.items() if k!='metrics'},indent=2))
    print(json.dumps({k:val for k,val in m.items() if k!='traces'},indent=2))

if __name__=='__main__':main()
