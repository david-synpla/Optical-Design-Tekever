"""Validate B05 attempt 2 and close variant comparison, without more shape searches."""
import json, time, shutil, csv, hashlib
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.optimize import minimize_scalar
import track_b_run008_cassegrain as m

out=m.ROOT/'runs/run_008'; variant=out/'attempt_02'; x=json.loads((variant/'configuration.json').read_text())['best']
def focus_merit(delta):
    o=m.build(x,delta,True); score=0
    for field in [(0,0),(m.HX,m.HY)]:
        data=[m.trace(o,field,wl,8) for wl in [.43,.55,.80]]
        pts=np.concatenate([p[k] for p,k in data]); score+=float(np.mean(np.sum((pts-pts.mean(axis=0))**2,axis=1)))
    return score
finite=minimize_scalar(focus_merit,bounds=(-1,3),method='bounded',options={'xatol':1e-5,'maxiter':40})
(variant/'finite_800m.json').write_text(json.dumps(dict(detector_shift_mm=float(finite.x),success=bool(finite.success),
    metrics=m.geometric(x,float(finite.x),True)),indent=2)+'\n')
o=m.build(x); s=m.scale_factor(x)
def sag(c,r):return c*r*r/(1+np.sqrt(1-c*c*r*r))
edges=[4*s+sag(x[4]/s,17.5)-sag(x[3]/s,17.5),3*s+sag(x[6]/s,17.5)-sag(x[5]/s,17.5)]
airgap_center=x[7]*s; gap_edge=airgap_center+sag(x[5]/s,17.5)-sag(x[4]/s,17.5)
assert min(edges)>0 and min(airgap_center,gap_edge)>0
sensitivity=[]
for kind,delta in [('nominal',0),('detector',-.020),('detector',.020),('secondary',-.010),('secondary',.010)]:
    lens=m.build(x,delta if kind=='detector' else 0)
    if kind=='secondary':
        lens.updater.set_thickness(lens.surfaces[2].thickness+delta,2)
        lens.updater.set_thickness(lens.surfaces[3].thickness-delta,3)
    rms=[]
    for field in [(0,0),(m.HX,m.HY)]:
        data=[m.trace(lens,field,wl,12) for wl in m.WAVES]
        pts=np.concatenate([p[k] for p,k in data]); center=pts.mean(axis=0)
        rms.append(max(float(np.sqrt(np.mean(np.sum((p[k]-center)**2,axis=1)))*1000) for p,k in data))
    sensitivity.append(dict(perturbation=kind,mm=delta,center_corner_worst_rms_um=rms))
rows=[m.diffraction(x,field,wl,128) for field in [(0,0),(m.HX,0),(0,m.HY),(m.HX,m.HY)] for wl in m.WAVES]
(variant/'verification_diffraction.json').write_text(json.dumps(rows,indent=2)+'\n')
checks=[m.diffraction(x,(0,0),.55,192),m.diffraction(x,(m.HX,m.HY),.8,192)]
deltas=[]
for fine in checks:
    coarse=next(r for r in rows if np.allclose(r['field'],fine['field']) and r['wavelength_um']==fine['wavelength_um'])
    deltas.append(max(float(np.max(abs(np.array(fine['actual'][key])-coarse['actual'][key]))) for key in ['mtf_x','mtf_y','ee_1_2_3_pixels']))
vpos=np.asarray(o.surfaces.positions)
report=dict(vertex_span_mm=float(np.max(vpos[1:])-np.min(vpos[1:])),lens_edges_mm=edges,lens_airgap_min_mm=min(airgap_center,gap_edge),
    secondary_radius_mm=float(o.surfaces[3].geometry.radius),secondary_conic=float(o.surfaces[3].geometry.k),
    sensitivity=sensitivity,convergence_max_abs_differences=deltas,
    note='Conic magnitude alone is not a manufacturing metric. Compare radius, actual departure, slope and sensitivity.')
(variant/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
with (variant/'prescription.csv').open('w',newline='') as file:
    writer=csv.writer(file);writer.writerow(['index','radius_mm','thickness_mm','conic','material_after','aperture'])
    mats=['air','air','mirror','mirror','air','N-BK7','air','N-F2','air','air']
    for i,surf in enumerate(o.surfaces):
        writer.writerow([i,surf.geometry.radius,surf.thickness,getattr(surf.geometry,'k',0),mats[i],str(surf.aperture.to_dict()) if surf.aperture else 'none'])
assert abs(m.geometric(x)['worst_rms_um']-json.loads((variant/'metrics.json').read_text())['worst_rms_um'])<1e-9
shutil.copy2(__file__,out/'finalize.py')
print(json.dumps(report,indent=2));print('finite focus',finite.x)
