"""Compare saved B04/B05 metrics and small fixed-geometry perturbations.
No optimizer. Writes only new Run 008 comparison artifacts.
"""
import json, importlib, shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
OUT=ROOT/'runs/run_008'
results={}; all_diff={}
for cid,run,modname in [('B04','007','track_b_run007_physical'),('B05','008','track_b_run008_cassegrain')]:
    m=importlib.import_module(modname)
    folder=ROOT/f'runs/run_{run}'
    x=json.loads((folder/'configuration.json').read_text())['best']
    diffs=json.loads((folder/'diffraction.json').read_text())['rows']; all_diff[cid]=diffs
    opt=json.loads((folder/'optimization.json').read_text())['best']
    sensitivity=[]
    for kind,delta in [('nominal',0),('detector',-.020),('detector',.020),('secondary',-.010),('secondary',.010)]:
        o=m.build(x,focus=delta if kind=='detector' else 0)
        if kind=='secondary':
            o.updater.set_thickness(o.surfaces[2].thickness+delta,2)
            o.updater.set_thickness(o.surfaces[3].thickness-delta,3)
        rms=[]
        for field in [(0,0),(m.HX,m.HY)]:
            data=[m.trace(o,field,wl,12) for wl in m.WAVES]
            pts=np.concatenate([p[k] for p,k in data]); center=pts.mean(axis=0)
            rms.append(max(float(np.sqrt(np.mean(np.sum((p[k]-center)**2,axis=1)))*1000) for p,k in data))
        sensitivity.append(dict(perturbation=kind,mm=delta,center_corner_worst_rms_um=rms))
    o=m.build(x); vertices=np.asarray(o.surfaces.positions,dtype=float)
    # Maximum distortion against f*tan(field angle), using common spectral centroid;
    # includes lateral chromatic shift rather than asserting chief-ray distortion.
    scale_errors=[]
    for row in opt['rows']:
        target=m.F*np.tan(np.radians(m.ANG)*np.array(row['field']))
        if np.linalg.norm(target)>0:
            actual=np.linalg.norm(row['centroid_mm']); ideal=np.linalg.norm(target)
            scale_errors.append((actual/ideal-1)*100)
    results[cid]=dict(worst_rms_um=opt['worst_rms_um'],efl_mm=opt['efl_mm'],
        primary_radius_mm=float(o.surfaces[2].geometry.radius),primary_conic=float(o.surfaces[2].geometry.k),
        secondary_radius_mm=float(o.surfaces[3].geometry.radius),secondary_conic=float(getattr(o.surfaces[3].geometry,'k',0)),
        vertex_span_mm=float(np.max(vertices[1:])-np.min(vertices[1:])),
        max_abs_common_centroid_scale_error_percent=max(abs(v) for v in scale_errors),
        sensitivity=sensitivity,finite_focus=json.loads((folder/'finite_800m.json').read_text())['detector_shift_mm'])

fig,axes=plt.subplots(1,3,figsize=(12,4),sharey=True)
for col,wl in enumerate([.43,.55,.80]):
    ax=axes[col]
    for cid,color in [('B04','tab:blue'),('B05','tab:orange')]:
        d=all_diff[cid][-6+m.WAVES.index(wl)]
        ax.plot(m.FREQ,d['actual']['mtf_x'],'o-',color=color,label=f'{cid} X')
        ax.plot(m.FREQ,d['actual']['mtf_y'],'s--',color=color,label=f'{cid} Y')
    ax.plot(m.FREQ,d['matched_diffraction']['mtf_x'],'k:',label='Matched pupil limit')
    ax.set_title(f'Corner {wl*1000:g} nm'); ax.set_xlabel('Spatial frequency (lp/mm)'); ax.grid(alpha=.2)
axes[0].set_ylabel('Optical MTF'); axes[0].legend(fontsize=8)
fig.suptitle('Independent Track B corrected-reflector screen'); fig.tight_layout(); fig.savefig(OUT/'comparison_mtf.png',dpi=150)
(OUT/'comparison.json').write_text(json.dumps(dict(candidates=results,
    assumptions='Perturbations are diagnostic magnitudes, not manufacturing tolerances; no refocus after perturbation. Spacing changes keep other physical vertices fixed.',
    limits='No thermal model or dn/dT; changes in construction cannot be inferred from these one-at-a-time spacing sensitivities.'),indent=2)+'\n')
shutil.copy2(__file__,OUT/'comparison.py')
print(json.dumps(results,indent=2))
