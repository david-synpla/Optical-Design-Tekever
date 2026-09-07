"""Checkpointed coupled-error experiment and diffraction follow-up for Run 010."""
import sys,json,time,copy
from pathlib import Path
import numpy as np
from scipy.stats import qmc
import track_b_run010_sensitivity as m

def compensation(c,errors,residual,label):
    sens=m.read(Path(c.cid)/'sensitivity.json');names=[d['name'] for d in c.defs]
    z=np.load(m.OUT/c.cid/'jacobian.npz');J=z['J'];r0=z['nominal']
    ns=sens['compensator_coupling'][label]['names'];C=J[:,[names.index(n) for n in ns]]
    q=np.linalg.lstsq(C,-(residual-r0),rcond=1e-8)[0];adjust={};saturated=[]
    for n,v in zip(ns,q):
        cap=.001 if c.byname[n]['mode'] in ['tx','ty'] else .5
        raw=float(v*c.byname[n]['step']);adjust[n]=float(np.clip(raw,-cap,cap))
        if abs(raw)>cap:saturated.append(n)
    total=errors.copy()
    for n,v in adjust.items():total[n]=total.get(n,0)+v
    rr,met,_=c.sample(total)
    return dict(adjustments=adjust,total_errors=total,metrics=met,saturated=saturated,
        linear_prediction_error_um=float(np.sqrt(np.mean((rr-(residual+C@q))**2))*1000))

def experiment(cid):
    c=m.Candidate(cid);folder=Path(cid);sens=m.read(folder/'sensitivity.json')
    union=sorted(set(d['name'] for cc in ['B05-1','B05-2','B06'] for d in m.Candidate(cc).defs if d.get('group')!='corrector'))
    unit=2*qmc.LatinHypercube(len(union),seed=20260907).random(24)-1
    cases=[];start=time.monotonic()
    for i,row in enumerate(unit):
        path=folder/'lhs'/f'{i:03}.json'
        if (m.OUT/path).exists():cases.append(m.read(path));continue
        errors={name:float(row[j]*c.byname[name]['step']) for j,name in enumerate(union) if name in c.byname}
        rr,met,_=c.sample(errors)
        z=np.load(m.OUT/cid/'jacobian.npz');dv=np.array([errors.get(d['name'],0)/d['step'] for d in c.defs])
        result=dict(index=i,errors=errors,uncompensated=met,
            linear_prediction_error_um=float(np.sqrt(np.mean((rr-z['nominal']-z['J']@dv)**2))*1000),
            compensated={label:compensation(c,errors,rr,label) for label in sens['compensator_coupling']})
        m.save(path,result);cases.append(result)
    summary={}
    for label in ['uncompensated']+list(sens['compensator_coupling']):
        metrics=[r['uncompensated'] if label=='uncompensated' else r['compensated'][label]['metrics'] for r in cases]
        vals=np.array([r['worst_rms_um'] for r in metrics]);cent0=np.array(sens['nominal']['centroids_mm'])
        shifts=[float(np.max(np.linalg.norm(np.array(r['centroids_mm'])-cent0,axis=1)))*1000 for r in metrics]
        summary[label]=dict(median_worst_rms_um=float(np.median(vals)),p90_worst_rms_um=float(np.percentile(vals,90)),
            maximum_worst_rms_um=float(vals.max()),min_survival=min(r['minimum_survival'] for r in metrics),
            max_centroid_displacement_um=max(shifts),worst_case=int(vals.argmax()))
    m.save(folder/'lhs.json',dict(seed=20260907,count=24,union_parameters=union,normalized_samples=unit.tolist(),
        distribution='Independent uniform +/- diagnostic magnitudes, Latin hypercube; exploratory, not capability/yield',
        summary=summary,seconds=time.monotonic()-start))
    print(cid,json.dumps(summary),flush=True)

def diffraction(cid):
    c=m.Candidate(cid);folder=Path(cid);lhs=m.read(folder/'lhs.json')
    # Same worst-after-three-adjustments specimen is evaluated before/after.
    idx=lhs['summary']['focus_secondary_tilt']['worst_case'];case=m.read(folder/'lhs'/f'{idx:03}.json')
    scenarios={'nominal':{},'uncompensated':case['errors'],
        'focus':case['compensated']['focus']['total_errors'],
        'focus_secondary_tilt':case['compensated']['focus_secondary_tilt']['total_errors']}
    result=[]
    for label,errors in scenarios.items():
        path=folder/f'diffraction_{label}.json'
        if (m.OUT/path).exists():result.append(m.read(path));continue
        rows=[]
        for field in [(0,0),(m.A.HX,m.A.HY),(m.A.HX,-m.A.HY)]:
            for wl in [.43,.55,.8]:rows.append(c.diffraction(errors,field,wl))
        _,dense,_=c.sample(errors,n=10)
        record=dict(scenario=label,specimen=idx,errors=errors,rows=rows,dense_metrics=dense,image_scale=c.scale(errors))
        m.save(path,record);result.append(record);print(cid,label,'diffraction complete',flush=True)
    fine=[]
    for label in ['nominal','focus_secondary_tilt']:
        for wl in [.43,.55]:
            fine.append(dict(scenario=label,**c.diffraction(scenarios[label],(m.A.HX,m.A.HY),wl,168)))
    m.save(folder/'diffraction_convergence.json',fine)

if __name__=='__main__':
    if sys.argv[2]=='lhs':experiment(sys.argv[1])
    else:diffraction(sys.argv[1])
