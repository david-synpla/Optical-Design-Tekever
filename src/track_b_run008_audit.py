"""Read-only numerical rechecks of Run 008; writes only new audit artifacts."""
import json, hashlib, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import track_b_run008_cassegrain as m

out=m.ROOT/'runs/run_008'; x=json.loads((out/'configuration.json').read_text())['best']
o=m.build(x); axis=np.linspace(-1,1,181); xx,yy=np.meshgrid(axis,axis)
inside=xx**2+yy**2<=1; px=xx[inside]; py=yy[inside]
illum=[]
for field in m.FIELDS:
    r=o.ray_tracer.trace_generic(*field,px,py,.55)
    survives=np.asarray(r.i)>0
    illum.append(dict(field=field,full_pupil_area_fraction=float(survives.mean())))
    assert np.all(np.isfinite(np.asarray(r.x)[survives]))
scale=m.scale_factor(x)
def sag(c,r):return c*r*r/(1+np.sqrt(1-c*c*r*r))
edges=[4*scale+sag(x[4]/scale,m.AP['lens1'])-sag(x[3]/scale,m.AP['lens1']),
       3*scale+sag(x[6]/scale,m.AP['lens2'])-sag(x[5]/scale,m.AP['lens2'])]
diff=json.loads((out/'diffraction.json').read_text())['rows']
checks=json.loads((out/'sampling_check.json').read_text()); convergence=[]
for fine in checks:
    coarse=next(row for row in diff if row['field']==fine['field'] and row['wavelength_um']==fine['wavelength_um'])
    convergence.append(dict(field=fine['field'],wavelength_um=fine['wavelength_um'],
      max_mtf_difference=max(float(np.max(np.abs(np.array(fine['actual'][k])-coarse['actual'][k]))) for k in ['mtf_x','mtf_y']),
      max_ee_difference=float(np.max(np.abs(np.array(fine['actual']['ee_1_2_3_pixels'])-coarse['actual']['ee_1_2_3_pixels'])))))
# Verify saved replay and exact prescription first-order scale.
replay=m.geometric(x); expected=json.loads((out/'optimization.json').read_text())['best']
assert abs(replay['worst_rms_um']-expected['worst_rms_um'])<1e-9
assert abs(replay['efl_mm']-m.F)<1e-7
assert min(edges)>0
meta=json.loads((out/'metadata.json').read_text())
assert hashlib.sha256((out/'model.py').read_bytes()).hexdigest()==meta['script_sha256']
result=dict(equal_area_grid_illumination=illum,lens_edge_thickness_mm=edges,convergence=convergence,
            geometric_clear_area_expected=1-(m.AP['obstruction']/(m.D/2))**2,
            replay=True,efl_verified=True,hash_verified=True,
            limitations='No spider/coating radiometry/detailed baffles/thermal/tolerances; geometric area is not transmitted energy.')
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
fig,axes=plt.subplots(2,3,figsize=(12,7),sharex=True,sharey=True)
for col,wl in enumerate([.43,.55,.80]):
    for row,field in enumerate([(0,0),(m.HX,m.HY)]):
        d=next(d for d in diff if np.allclose(d['field'],field) and d['wavelength_um']==wl)
        ax=axes[row,col]
        ax.plot(m.FREQ,d['matched_diffraction']['mtf_x'],'k--',label='Matched pupil limit')
        ax.plot(m.FREQ,d['actual']['mtf_x'],'o-',label='X')
        ax.plot(m.FREQ,d['actual']['mtf_y'],'s-',label='Y')
        ax.set_title(f'{"Center" if row==0 else "Corner"}, {wl*1000:g} nm')
        ax.set_ylim(0,.7); ax.grid(alpha=.2)
        if row==1:ax.set_xlabel('Spatial frequency (lp/mm)')
        if col==0:ax.set_ylabel('Optical MTF')
axes[0,0].legend(fontsize=8); fig.suptitle('B05 physical pupil — diffraction-aware screening at a common detector plane')
fig.tight_layout(); fig.savefig(out/'mtf.png',dpi=150)
print(json.dumps(result,indent=2))
