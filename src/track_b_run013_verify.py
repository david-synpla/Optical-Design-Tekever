"""Bounded thermal verification: local compensators, dense field and diffraction."""
import sys,time
import numpy as np
import track_b_run013_thermal as T
M=T.M
def run(cid):
    start=time.monotonic();base=M.Candidate(cid);r0,_,_=base.sample();rows=[]
    fields=[(a*M.A.HX,b*M.A.HY) for a in np.linspace(-1,1,5) for b in np.linspace(-1,1,5)]
    for scenario,temp in [('silica_high_frame',-25),('silica_high_frame',50),('silica_low_frame',-25),('silica_low_frame',50),('homogeneous_high_CTE',-25),('homogeneous_high_CTE',50)]:
        c=T.Thermal(cid,temp,*T.SCENARIOS[scenario]);adj={};steps=[]
        # Two local linear corrections; larger travel is a separately labelled
        # engineering diagnostic, not a retroactive change to Run010 caps.
        ns=['detector_z','secondary_tx','secondary_ty'];limits=[5,.001,.001]
        for iteration in range(2):
            r,_,_=c.sample(adj);cols=[]
            for name in ns:
                h=base.byname[name]['step'];lo=adj.copy();hi=adj.copy()
                lo[name]=lo.get(name,0)-h;hi[name]=hi.get(name,0)+h
                cols.append((c.sample(hi)[0]-c.sample(lo)[0])/(2*h))
            C=np.column_stack(cols);delta=np.linalg.lstsq(C,-(r-r0),rcond=1e-9)[0]
            raw={n:adj.get(n,0)+float(v) for n,v in zip(ns,delta)}
            adj={n:float(np.clip(raw[n],-lim,lim)) for n,lim in zip(ns,limits)}
            steps.append(dict(unbounded=raw,applied=adj.copy(),cap_hit=any(abs(raw[n]-adj[n])>1e-12 for n in ns)))
        _,dense,_=c.sample(adj,n=12,fields=fields)
        diffraction=[]
        if scenario=='silica_low_frame':
            for wl in [.43,.55,.8]:
                for f in [(0,0),(M.A.HX,M.A.HY)]:diffraction.append(c.diffraction(adj,f,wl,112))
        rows.append(dict(scenario=scenario,temperature_C=temp,iterations=steps,dense=dense,image_scale=c.scale(adj),diffraction=diffraction))
        T.save(cid+'_verification.json',dict(rows=rows,seconds=time.monotonic()-start))
        print(cid,scenario,temp,adj,'dense',dense['worst_rms_um'],'survive',dense['minimum_survival'],flush=True)
if __name__=='__main__':run(sys.argv[1])
