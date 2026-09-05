"""Finalize/audit the saved B04 result; no optimizer and no source-result rewrite."""
import sys,json,csv,hashlib,shutil
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
try:
    import track_b_run006_cdk as m
except ModuleNotFoundError:
    import model as m

out=m.ROOT/'runs/run_006'
cfg=json.loads((out/'configuration.json').read_text())
x=cfg['best']; o=m.build(x)
records=[]; traces=[]
for hx in [-m.W/np.hypot(m.W,m.H),0,m.W/np.hypot(m.W,m.H)]:
    for hy in [-m.H/np.hypot(m.W,m.H),0,m.H/np.hypot(m.W,m.H)]:
        for wl in m.WAVES:
            m.xy(o,hx,hy,wl,20)
            traces.append((hx,hy,wl,np.array(o.surfaces.x),np.array(o.surfaces.y),np.array(o.surfaces.z)))
rad=lambda xx,yy:np.hypot(xx,yy)
# Design circular apertures to sampled envelopes with explicit +1 mm radial cell margin.
secondary=max(np.max(rad(xx[2],yy[2])) for _,_,_,xx,yy,zz in traces)+1
def plane(xx,yy,zz,i,j,z):
    t=(z-zz[i])/(zz[j]-zz[i])
    return xx[i]+t*(xx[j]-xx[i]),yy[i]+t*(yy[j]-yy[i])
hole=max(np.max(rad(*plane(xx,yy,zz,2,3,0))) for _,_,_,xx,yy,zz in traces)+1
lens1=max(np.max(rad(xx[3:5],yy[3:5])) for _,_,_,xx,yy,zz in traces)+1
lens2=max(np.max(rad(xx[5:7],yy[5:7])) for _,_,_,xx,yy,zz in traces)+1
for hx,hy,wl,xx,yy,zz in traces:
    entrance=rad(*plane(xx,yy,zz,0,1,float(zz[2,0])))
    keep=(entrance>secondary)&(rad(xx[1],yy[1])>hole)
    pts=np.column_stack([xx[-1,keep],yy[-1,keep]])
    rms=float(np.sqrt(np.mean(np.sum((pts-pts.mean(axis=0))**2,axis=1)))*1000)
    records.append(dict(field=[hx,hy],wavelength_um=wl,sampled_ray_survival=float(np.mean(keep)),
                        monochromatic_centered_rms_um=rms))

def sag(r,c,k=0):
    return c*r*r/(1+np.sqrt(1-(1+k)*c*c*r*r))
edge1=4+sag(lens1,x[4])-sag(lens1,x[3])
edge2=3+sag(lens2,x[6])-sag(lens2,x[5])
min_gap=x[7]+sag(min(lens1,lens2),x[5])-sag(min(lens1,lens2),x[4])
m.xy(o,0,0,.55,5)
z=np.array(o.surfaces.z[:,0])
result=dict(secondary_radius_with_1mm_margin=secondary,primary_hole_radius_with_1mm_margin=hole,
            lens1_radius_with_1mm_margin=lens1,lens2_radius_with_1mm_margin=lens2,
            lens_edge_thickness_mm=[edge1,edge2],lens_gap_at_common_edge_mm=min_gap,
            vertex_positions_mm=z[1:].tolist(),vertex_extent_mm=float(max(z[1:])-min(z[1:])),
            primary_clear_diameter_mm=m.D,geometric_on_axis_area_fraction=1-(max(secondary,hole)/(m.D/2))**2,
            worst_masked_monochromatic_rms_um=max(r['monochromatic_centered_rms_um'] for r in records),
            records=records,assumptions=['1 mm radial sizing margins are benchmark choices, not detector/mechanical specifications',
            'Mask uses straight segments at secondary vertex and primary vertex; mirror sag/cell details need nonsequential audit',
            'Ray survival on hexapolar rings is sampling-dependent, not a calibrated radiometric throughput',
            'RMS here is centered per wavelength; do not compare it directly to common-centroid broadband merit',
            'No spider, actual baffles, detector package, coatings, ghosts, thermal or tolerances'],
            status='Further physical model required; not a verified or frozen optical design')
(out/'physical_audit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
# Recover CSV from saved optimizer parameters; no second optimizer call.
with (out/'prescription_complete.csv').open('w',newline='') as f:
    writer=csv.writer(f); writer.writerow(['index','radius_mm','thickness_mm','conic','material_after','screen_radius_mm'])
    materials=['air','mirror','mirror','N-BK7','air','N-F2','air','air']
    radii=[None,m.D/2,secondary,lens1,lens1,lens2,lens2,None]
    for i,s in enumerate(o.surfaces):
        writer.writerow([i,s.geometry.radius,s.thickness,getattr(s.geometry,'k',0),materials[i],radii[i]])
fig,ax=plt.subplots(figsize=(9,4))
for hx,hy,wl,xx,yy,zz in traces:
    if hx==0 and hy>=0 and wl==.55:
        for k in range(0,xx.shape[1],max(1,xx.shape[1]//30)):
            ax.plot(zz[1:,k],yy[1:,k],lw=.4,alpha=.35)
for i,r in [(1,m.D/2),(2,secondary),(3,lens1),(4,lens1),(5,lens2),(6,lens2)]:
    ax.plot([z[i],z[i]],[-r,r],'k-',lw=2)
ax.plot([z[7],z[7]],[-m.H/2,m.H/2],'r-',lw=3)
ax.set(xlabel='Axial position (mm)',ylabel='Y (mm)',title='B04 meridional screening rays; aperture outlines, no housing')
ax.set_aspect('equal',adjustable='datalim'); fig.tight_layout(); fig.savefig(out/'layout_screen.png',dpi=150)
shutil.copy2(m.__file__,out/'model.py'); shutil.copy2(__file__,out/'audit.py')
shutil.copy2(m.ROOT/'requirements/eo_requirements.yaml',out/'requirements.yaml')
metrics=json.loads((out/'metrics.json').read_text())
metadata=dict(track='B',run_id='006',candidate_ids=['B04'],stage='screening',parent_run=None,preceding_screen='005',
              purpose='Determine whether a fresh two-lens CDK co-design warrants physical development',
              substantial_search_count=1,materially_distinct_attempt_count=1,plateau=False,
              optimizer_seconds=metrics['attempts'][0]['elapsed_seconds'],closed_utc=datetime.now(timezone.utc).isoformat(),
              decision='ACTIVE for physical-model screening; no final-performance claim',track_a_seed_used=False,reference_accessed=False,
              stop_reason='Seed feasibility question answered; physical pupil model is next engineering question',
              export_recovery='Initial CSV exporter failed on Plane.conic after metrics/configuration saved. Complete CSV recovered without optimizer rerun; partial CSV retained.',
              versions=dict(python=sys.version,optiland=m.optiland.__version__,numpy=np.__version__,scipy=m.scipy.__version__),
              model_sha256=hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest(),
              audit_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(out/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
