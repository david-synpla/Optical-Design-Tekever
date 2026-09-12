#!/usr/bin/env python3
"""Run 020: bounded C04 350/1600 donor-primary hybrid screen."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,platform,shutil,sys,time
from datetime import datetime,timezone
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np,optiland,scipy,yaml
from optiland import optic
from optiland.physical_apertures import RadialAperture
from scipy.optimize import least_squares

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
OUT=ROOT/'runs/run_020'; REQ=ROOT/'requirements/eo_swir_system_requirements.yaml'
PRIMARY_F=1600.; DONOR_DIAMETER=353.; DONOR_MASS_KG=8.280; STOP_AHEAD=18.; VANE=.7

def save(n,v): (OUT/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def scalar(v): return float(np.asarray(v).reshape(-1)[0])

def channel(req):
    r=req['source_explicit_requirements']['swir']; pitch=r['pixel_pitch_um'][0]/1000
    efl=pitch/(r['instantaneous_fov_urad_per_pixel']*1e-6); pupil=efl/r['f_number']
    hx=math.degrees(math.atan(r['array_px'][0]*pitch/(2*efl))); hy=math.degrees(math.atan(r['array_px'][1]*pitch/(2*efl))); diag=math.hypot(hx,hy)
    return {'efl_mm':efl,'pupil_mm':pupil,'hx':hx/diag,'hy':hy/diag,'diag_deg':diag,'waves_um':[.8,1.2,1.8]}

def fields(c):
    x,y=c['hx'],c['hy']; return [('center',0,0),('+x',x,0),('-x',-x,0),('+y',0,y),('-y',0,-y),('corner++',x,y),('corner+-',x,-y),('corner-+',-x,y),('corner--',-x,-y)]

def pupil(nr=7,na=28):
    r=np.sqrt((np.arange(nr)+.5)/nr)*.997; t=2*np.pi*(np.arange(na)+.5)/na
    return (r[:,None]*np.cos(t)).ravel(),(r[:,None]*np.sin(t)).ravel()

class DonorPupil(RadialAperture):
    def __init__(self,c,g): super().__init__(c['pupil_mm']/2); self.c=c; self.g=g; self.field=(0.,0.)
    def set_field(self,hx,hy): self.field=(hx,hy)
    def contains(self,x,y):
      hx,hy=self.field; l=math.tan(math.radians(self.c['diag_deg']*hx)); m=math.tan(math.radians(self.c['diag_deg']*hy))
      t=(STOP_AHEAD-self.g['flat_distance_mm']-x)/(1+l); xf=x+t*l; yf=y+t*m
      xs=x+(STOP_AHEAD-self.g['flat_distance_mm'])*l; ys=y+(STOP_AHEAD-self.g['flat_distance_mm'])*m
      return super().contains(x,y)&(xf*xf+yf*yf>(self.g['flat_minor_mm']/2)**2)&(abs(xs)>=VANE/2)&(abs(ys)>=VANE/2)
    def to_dict(self): return {'type':'DonorPupil','r_max':self.r_max,'flat_minor_mm':self.g['flat_minor_mm'],'vane_mm':VANE}

def geometry(name,flat_distance,flat_minor,lens_diameter):
    return {'name':name,'flat_distance_mm':flat_distance,'flat_minor_mm':flat_minor,'lens_diameter_mm':lens_diameter,
      'donor_nominal_diameter_mm':DONOR_DIAMETER,'primary_focal_mm':PRIMARY_F}

def build(c,g,x,finite=False):
    c1,c2,c3,c4,s,gap,q=x; pup=DonorPupil(c,g); lr=g['lens_diameter_mm']/2
    o=optic.Optic(name='C04 stock 350/1600 paraboloid plus stock flat and custom SWIR extender')
    o.surfaces.add(index=0,thickness=800000 if finite else np.inf)
    o.surfaces.add(index=1,thickness=STOP_AHEAD,is_stop=True,aperture=pup)
    o.surfaces.add(index=2,radius=-2*PRIMARY_F,conic=-1,thickness=-g['flat_distance_mm'],material='mirror',aperture=RadialAperture(c['pupil_mm']/2+2))
    o.surfaces.add(index=3,thickness=-(s-g['flat_distance_mm']),aperture=RadialAperture(g['flat_minor_mm']/2))
    for i,curv,t,mat in [(4,c1,6,'fused_silica'),(5,c2,gap,'air'),(6,c3,5,'LITHOTEC-CAF2'),(7,c4,q,'air')]:
      o.surfaces.add(index=i,radius=-1/curv if abs(curv)>1e-12 else np.inf,thickness=-t,material=mat,aperture=RadialAperture(lr))
    o.surfaces.add(index=8)
    o.set_aperture(aperture_type='EPD',value=c['pupil_mm']); o.fields.set_type('angle'); o.fields.add(y=0); o.fields.add(y=c['diag_deg'])
    for w in c['waves_um']: o.wavelengths.add(value=w,is_primary=w==1.2)
    return o

def trace(o,c,g,f,w,nr=7,na=28):
    _,hx,hy=f; o.surfaces[1].aperture.set_field(hx,hy); px,py=pupil(nr,na)
    rays=o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,w)
    p=np.column_stack((np.asarray(rays.x),np.asarray(rays.y))); ok=np.isfinite(p).all(1)&(np.asarray(rays.i)>0)
    if not np.any(ok): return {'field':f[0],'wave_um':w,'survival':0.,'rms_radius_um':1e6,'centroid_mm':[math.nan,math.nan]}
    ctr=p[ok].mean(0); return {'field':f[0],'wave_um':w,'survival':float(ok.mean()),
      'rms_radius_um':float(np.sqrt(np.mean(np.sum((p[ok]-ctr)**2,axis=1)))*1000),'centroid_mm':ctr.tolist()}

def physical(c,g,x):
    c1,c2,c3,c4,s,gap,q=x; lr=g['lens_diameter_mm']/2
    def sag(curv,r): return curv*r*r/(1+math.sqrt(max(0,1-curv*curv*r*r)))
    beam_at_flat=c['pupil_mm']*(1-g['flat_distance_mm']/PRIMARY_F)+2*g['flat_distance_mm']*math.tan(math.radians(c['diag_deg']))
    side=s+11+gap+q-g['flat_distance_mm']; cell=DONOR_DIAMETER+14
    front_width=cell+141+4; front_height=cell
    straight=[front_width,front_height,g['flat_distance_mm']+55]
    # One mid-path 45-degree flat halves axial length but sends the remaining
    # converging path sideways. It is a physical comparison, not a chosen design.
    mid=g['flat_distance_mm']/2; mid_beam=c['pupil_mm']*(1-mid/PRIMARY_F)+2*mid*math.tan(math.radians(c['diag_deg']))
    big_fold_clear=mid_beam*math.sqrt(2)+6
    folded=[max(front_width,g['flat_distance_mm']-mid+side+80),front_height,mid+75]
    def solid(d): return math.pi/4*(d/1000)**2*(.1*d/1000)*2200
    return {'lens_edge_thickness_mm':[6+sag(c2,lr)-sag(c1,lr),5+sag(c4,lr)-sag(c3,lr)],
      'air_gap_edge_mm':gap+sag(c3,lr)-sag(c2,lr),'beam_at_flat_including_field_mm':beam_at_flat,
      'flat_clear_margin_mm':g['flat_minor_mm']-beam_at_flat,'side_exit_track_mm':side,
      'straight_dimensions_mm':straight,'straight_volume_l':float(np.prod(straight)/1e6),
      'one_large_fold_dimensions_mm':folded,'one_large_fold_volume_l':float(np.prod(folded)/1e6),
      'large_fold_clear_mm':big_fold_clear,'large_fold_solid_proxy_kg':solid(big_fold_clear),
      'donor_primary_catalog_mass_kg':DONOR_MASS_KG,'donor_primary_solid_proxy_kg':solid(DONOR_DIAMETER),
      'focus_mechanisms_complete_payload':2,'large_optics_over_100mm_straight':2,
      'large_optics_over_100mm_large_fold':3,'limitations':'box includes integrated 141 mm EO cell proxy; cells/electronics/gimbal excluded; large fold is a new qualified optic'}

def evaluate(c,g,x,nr=10,na=40):
    o=build(c,g,x); traces=[trace(o,c,g,f,w,nr,na) for f in fields(c) for w in c['waves_um']]
    return {'geometry':g,'parameters':list(map(float,x)),'effective_focal_length_mm':abs(scalar(o.paraxial.f2())),
      'f_number':abs(scalar(o.paraxial.f2()))/c['pupil_mm'],'worst_rms_radius_um':max(t['rms_radius_um'] for t in traces),
      'minimum_survival':min(t['survival'] for t in traces),'traces':traces,'physical':physical(c,g,x)}

def merit(x,c,g):
    try:
      o=build(c,g,x); values=[]
      for f in (fields(c)[0],fields(c)[1],fields(c)[3],fields(c)[5]):
        pts=[]
        for w in c['waves_um']:
          _,hx,hy=f; o.surfaces[1].aperture.set_field(hx,hy); px,py=pupil(5,20); rays=o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,w)
          p=np.column_stack((np.asarray(rays.x),np.asarray(rays.y))); ok=np.isfinite(p).all(1)&(np.asarray(rays.i)>0); pts.append((p,ok))
        good=np.concatenate([p[k] for p,k in pts]); ctr=good.mean(0)
        for p,k in pts:
          residual=np.zeros_like(p); residual[k]=(p[k]-ctr)/.010; residual[~k]=20; values.extend(residual.ravel())
      values.append((abs(scalar(o.paraxial.f2()))-c['efl_mm'])/.02)
      ph=physical(c,g,x); values.extend([max(0,.8-v)*40 for v in ph['lens_edge_thickness_mm']]); values.append(max(0,.5-ph['air_gap_edge_mm'])*40)
      return np.nan_to_num(values,nan=1e5,posinf=1e5,neginf=-1e5)
    except Exception: return np.full(4*3*100*2+4,1e5)

def solve(c,g,seed,max_nfev=60):
    low=[-.025]*4+[g['flat_distance_mm']+25,1,40]; high=[.025]*4+[1560,40,350]
    fit=least_squares(merit,seed,args=(c,g),bounds=(low,high),x_scale='jac',max_nfev=max_nfev,ftol=2e-6,xtol=2e-7,gtol=2e-6)
    r=evaluate(c,g,fit.x); r['optimization']={'nfev':int(fit.nfev),'success':bool(fit.success),'message':fit.message,'seed':list(map(float,seed)),'bounds':[low,high]}; return r

def prescription(path,c,row):
    o=build(c,row['geometry'],row['parameters']); keys=['surface','radius_mm','conic','thickness_mm','material_post','is_stop']
    with path.open('w',newline='',encoding='utf-8') as f:
      w=csv.DictWriter(f,keys); w.writeheader()
      for i,s in enumerate(o.surfaces.surfaces):
        q=s.geometry; rad=scalar(q.radius) if hasattr(q,'radius') else math.inf
        w.writerow({'surface':i,'radius_mm':rad if np.isfinite(rad) else 'infinity','conic':scalar(q.k) if hasattr(q,'k') else '',
          'thickness_mm':scalar(s.thickness) if np.isfinite(scalar(s.thickness)) else 'infinity','material_post':str(s.material_post),'is_stop':s.is_stop})

def main():
    p=argparse.ArgumentParser(); p.add_argument('--probe',action='store_true'); p.add_argument('--resume',action='store_true'); args=p.parse_args()
    req=yaml.safe_load(REQ.read_text(encoding='utf-8')); c=channel(req); scale=PRIMARY_F/650
    base=np.array([.003620433551564968,.016405501349663336,.00022755195650503375,-.0061404001051408134,580.6896269009242,3.016685215604142,77.47947106043094])
    seed=np.r_[base[:4]/scale,base[4:]*scale]
    gs=[geometry('N1220_F82_L70',1220,82,70),geometry('N1300_F75_L60',1300,75,60),geometry('N1400_F63_L50',1400,63,50)]
    if args.probe:
      for g in gs: print(g['name'],json.dumps(evaluate(c,g,seed,6,24),indent=2)[:1000])
      return
    OUT.mkdir(parents=True,exist_ok=args.resume)
    if (OUT/'SHA256SUMS.txt').exists(): raise RuntimeError('Run 020 is closed and immutable')
    started=datetime.now(timezone.utc); tick=time.perf_counter(); rows=[]
    for g in gs:
      local=seed.copy(); local[4]=max(g['flat_distance_mm']+45,seed[4]); rows.append(solve(c,g,local))
    save('metrics.json',{'donor_hypothesis':{'nominal_diameter_mm':DONOR_DIAMETER,'nominal_focal_length_mm':PRIMARY_F,
      'catalog_mass_kg':DONOR_MASS_KG,'guaranteed_clear_aperture_status':'not published on reviewed supplier pages; >=311.371 mm supplier confirmation required'},'variants':rows})
    shutil.copy2(REQ,OUT/'requirements.yaml'); shutil.copy2(__file__,OUT/'track_c_run020_c04.py')
    for r in rows: prescription(OUT/f"{r['geometry']['name'].lower()}_swir_prescription.csv",c,r)
    save('dependencies.json',{'python':sys.version,'platform':platform.platform(),'optiland':optiland.__version__,'numpy':np.__version__,'scipy':scipy.__version__})
    save('provenance.json',{'requirements':{'path':'requirements/eo_swir_system_requirements.yaml','sha256':digest(REQ)},
      'donor':'Orion Optics UK 350 f/4.6 product/catalogue pages checked 2026-09-12; market evidence, not guaranteed flight specification',
      'historical_files_modified':False,'contamination_control':'reference/ not accessed'})
    save('metadata.json',{'track':'C','run_id':'020','candidate_ids':['C04'],'parent_run':'run_019','development_stage':'C1 bounded cost/COTS experiment',
      'start_time_utc':started.isoformat(),'end_time_utc':datetime.now(timezone.utc).isoformat(),'script_wall_seconds':time.perf_counter()-tick,
      'materially_distinct_attempts':3,'optimizer_invocations':3,'optimizer_evaluations':sum(r['optimization']['nfev'] for r in rows),'plateau_counter':0,
      'stopping_reason':'three donor-flat/corrector placements establish optical versus unavoidable long-track/fold trade; reserve two-attempt budget for a justified derivative only'})
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.scatter([r['physical']['straight_volume_l'] for r in rows],[r['worst_rms_radius_um'] for r in rows])
    for r in rows: ax.annotate(r['geometry']['name'],(r['physical']['straight_volume_l'],r['worst_rms_radius_um']),fontsize=8)
    ax.set(xlabel='Integrated straight package proxy (L)',ylabel='SWIR worst RMS radius (um)'); ax.grid(alpha=.25); fig.tight_layout();fig.savefig(OUT/'c04_optical_swap.png',dpi=180);plt.close(fig)
    print(json.dumps([{'name':r['geometry']['name'],'nfev':r['optimization']['nfev'],'efl':r['effective_focal_length_mm'],'fno':r['f_number'],
      'rms':r['worst_rms_radius_um'],'survival':r['minimum_survival'],'flat_margin':r['physical']['flat_clear_margin_mm'],
      'straight_L':r['physical']['straight_volume_l'],'folded_L':r['physical']['one_large_fold_volume_l']} for r in rows],indent=2))

if __name__=='__main__': main()
