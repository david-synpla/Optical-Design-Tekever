"""Dense spectral/field and mechanical shape audit, no optimization."""
import json, shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import track_b_run008_cassegrain as m

out=m.ROOT/'runs/run_008/attempt_02'; x=json.loads((out/'configuration.json').read_text())['best']; o=m.build(x)
waves=sorted(set(m.WAVES+np.linspace(.43,.8,13).tolist()))
axis=np.linspace(-1,1,81); xx,yy=np.meshgrid(axis,axis); disk=xx*xx+yy*yy<=1
px,py=xx[disk],yy[disk]
records=[]
for hx in np.linspace(-m.HX,m.HX,5):
    for hy in np.linspace(-m.HY,m.HY,5):
        data=[]; survival=[]
        for wl in waves:
            rays=o.ray_tracer.trace_generic(hx,hy,px,py,wl); keep=np.asarray(rays.i)>0
            points=np.column_stack([rays.x,rays.y])[keep]
            assert np.all(np.isfinite(points))
            data.append(points); survival.append(float(keep.mean()))
        center=np.concatenate(data).mean(axis=0)
        records.append(dict(field=[hx,hy],rms_um=[float(np.sqrt(np.mean(np.sum((p-center)**2,axis=1)))*1000) for p in data],
                            full_pupil_survival=survival))
# Infinitesimal paraxial ray is mathematical even though the pupil center is
# physically obscured. EFL uses output angle versus entrance height.
efl=[]
for wl in waves:
    ray=o.ray_tracer.trace_generic(0,0,np.array([1e-5]),np.array([0.]),wl)
    f=abs(float((1e-5*m.D/2)/(ray.L[0]/ray.N[0])))
    efl.append(dict(wavelength_um=wl,efl_mm=f,ifov_urad=m.R['pixel_pitch_um'][0]*1000/f))
assert abs(next(e['efl_mm'] for e in efl if e['wavelength_um']==.55)-m.F)<1e-4

def conic_sag(r,rad,k):
    c=1/rad
    return c*r*r/(1+np.sqrt(1-(1+k)*c*c*r*r))
shapes=[]
for i,name,radius in [(2,'primary',m.AP['primary_outer']),(3,'secondary',m.AP['secondary'])]:
    geom=o.surfaces[i].geometry; r=np.linspace(0,radius,1001)
    sag=conic_sag(r,float(geom.radius),float(geom.k)); sphere=conic_sag(r,float(geom.radius),0)
    shapes.append(dict(surface=name,clear_radius_mm=radius,
        max_departure_from_vertex_radius_sphere_um=float(max(abs(sag-sphere))*1000),
        max_slope_difference_from_vertex_sphere_mrad=float(max(abs(np.gradient(sag-sphere,r)))*1000),
        note='Vertex-radius sphere, NOT best-fit sphere or a specified surface-figure tolerance'))

fig,ax=plt.subplots(figsize=(10,4))
pos=np.asarray(o.surfaces.positions); origin=pos[2]
for i in range(1,9):
    ap=o.surfaces[i].aperture; radius=ap.r_max; inner=ap.r_min
    geom=o.surfaces[i].geometry
    for sign in [-1,1]:
        y=sign*np.linspace(inner,radius,150)
        sag=np.zeros_like(y) if not np.isfinite(geom.radius) else conic_sag(abs(y),float(geom.radius),float(getattr(geom,'k',0)))
        ax.plot(pos[i]-origin+sag,y,'k-',lw=1.5)
for field,color in [((0,0),'tab:blue'),((0,m.HY),'tab:orange')]:
    py=np.array([-.99,-.8,-.6,.6,.8,.99]); rays=o.ray_tracer.trace_generic(*field,np.zeros_like(py),py,.55)
    for i in np.where(np.asarray(rays.i)>0)[0]:ax.plot(np.asarray(o.surfaces.z)[1:,i]-origin,np.asarray(o.surfaces.y)[1:,i],color=color,lw=.6,alpha=.7)
ax.plot([pos[-1]-origin]*2,[-m.H/2,m.H/2],'r-',lw=3)
ax.set(xlabel='Axial position from primary vertex (mm)',ylabel='Y (mm)',title='B05 attempt 2 — finite apertures, mirror sag and surviving meridional rays')
ax.set_aspect('equal',adjustable='datalim'); fig.tight_layout(); fig.savefig(out/'layout.png',dpi=150)
result=dict(wavelengths_um=waves,field_count=25,pupil_grid=81,
    worst_rms_um=max(max(row['rms_um']) for row in records),rows=records,spectral_first_order=efl,mirror_shape_metrics=shapes,
    note='Independent denser uniform pupil audit; discrete samples do not prove continuous field/band or mechanical qualification')
(out/'extended_validation.json').write_text(json.dumps(result,indent=2)+'\n')
shutil.copy2(__file__,out/'extended_validation.py')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
