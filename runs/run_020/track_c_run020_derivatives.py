#!/usr/bin/env python3
"""Run 020 attempts 4-5: custom-secondary and single-lens derivatives."""
from __future__ import annotations
import csv,importlib.util,json,math,shutil,time
from pathlib import Path
import numpy as np,yaml
from optiland import optic
from optiland.physical_apertures import RadialAperture
from scipy.optimize import least_squares
import track_c_run020_c04 as m

def load_run017():
    p=m.ROOT/'runs/run_017/track_c_run017_c01.py'; spec=importlib.util.spec_from_file_location('run017_c01',p)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def cassegrain_merit(v,r17,g,ch,aps):
    return r17.merit(np.array([-1.,v[0],v[1]]),g,ch,aps)

def cassegrain(ch):
    r17=load_run017(); g=r17.swir_geometry('C350_CAS_B80',ch,m.PRIMARY_F/ch['pupil_mm'],80.)
    aps=r17.size_apertures(g,ch); seed=np.array([g['classical_secondary_conic'],0.])
    fit=least_squares(cassegrain_merit,seed,args=(r17,g,ch,aps),bounds=([-250,-8],[0,8]),x_scale='jac',max_nfev=60,ftol=2e-6,xtol=2e-7,gtol=2e-6)
    row=r17.evaluate(g,ch,aps,[-1.,fit.x[0],fit.x[1]],18,48)
    secondary_d=2*aps['secondary_radius_mm']; hole_d=2*aps['hole_radius_mm']; donor_cell=m.DONOR_DIAMETER+14
    dims=[donor_cell+141+4,donor_cell,g['mirror_separation_mm']+g['backfocus_mm']+55]
    def solid(d): return math.pi/4*(d/1000)**2*(.1*d/1000)*2200
    row.update({'optimization':{'nfev':int(fit.nfev),'success':bool(fit.success),'message':fit.message},
      'fixed_stock_primary':{'radius_mm':-3200.,'conic':-1.,'catalog_diameter_mm':m.DONOR_DIAMETER},
      'physical':{'custom_secondary_clear_diameter_mm':secondary_d,'required_primary_hole_diameter_mm':hole_d,
        'package_dimensions_mm':dims,'package_volume_l':float(np.prod(dims)/1e6),'donor_plus_secondary_mass_proxy_kg':m.DONOR_MASS_KG+solid(secondary_d),
        'large_optics_over_100mm':2 if secondary_d>100 else 1,'focus_mechanisms_complete_payload':2,
        'integration_gate':'stock donor is unperforated; drilling/refiguring or a return-beam fold adds risk/obscuration and weakens the COTS premise'}})
    return row

def one_lens_build(ch,g,x):
    c1,c2,s,q=x; o=optic.Optic(name='C04 stock primary/flat plus single fused-silica extender')
    o.surfaces.add(index=0,thickness=np.inf); o.surfaces.add(index=1,thickness=m.STOP_AHEAD,is_stop=True,aperture=m.DonorPupil(ch,g))
    o.surfaces.add(index=2,radius=-3200,conic=-1,thickness=-g['flat_distance_mm'],material='mirror',aperture=RadialAperture(ch['pupil_mm']/2+2))
    o.surfaces.add(index=3,thickness=-(s-g['flat_distance_mm']),aperture=RadialAperture(g['flat_minor_mm']/2))
    o.surfaces.add(index=4,radius=-1/c1 if abs(c1)>1e-12 else np.inf,thickness=-6,material='fused_silica',aperture=RadialAperture(g['lens_diameter_mm']/2))
    o.surfaces.add(index=5,radius=-1/c2 if abs(c2)>1e-12 else np.inf,thickness=-q); o.surfaces.add(index=6)
    o.set_aperture(aperture_type='EPD',value=ch['pupil_mm']);o.fields.set_type('angle');o.fields.add(y=0);o.fields.add(y=ch['diag_deg'])
    for w in ch['waves_um']:o.wavelengths.add(value=w,is_primary=w==1.2)
    return o

def one_trace(o,ch,f,w,nr=8,na=32):
    _,hx,hy=f;o.surfaces[1].aperture.set_field(hx,hy);px,py=m.pupil(nr,na);r=o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,w)
    p=np.column_stack((np.asarray(r.x),np.asarray(r.y)));ok=np.isfinite(p).all(1)&(np.asarray(r.i)>0)
    if not np.any(ok):return {'field':f[0],'wave_um':w,'survival':0.,'rms_radius_um':1e6}
    c=p[ok].mean(0);return {'field':f[0],'wave_um':w,'survival':float(ok.mean()),'rms_radius_um':float(np.sqrt(np.mean(np.sum((p[ok]-c)**2,axis=1)))*1000)}

def one_merit(x,ch,g):
    try:
      o=one_lens_build(ch,g,x);vals=[]
      for f in (m.fields(ch)[0],m.fields(ch)[1],m.fields(ch)[3],m.fields(ch)[5]):
        rows=[]
        for w in ch['waves_um']:
          _,hx,hy=f;o.surfaces[1].aperture.set_field(hx,hy);px,py=m.pupil(5,20);r=o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,w)
          p=np.column_stack((np.asarray(r.x),np.asarray(r.y)));ok=np.isfinite(p).all(1)&(np.asarray(r.i)>0);rows.append((p,ok))
        good=np.concatenate([p[k] for p,k in rows]);ctr=good.mean(0)
        for p,k in rows:
          residual=np.zeros_like(p);residual[k]=(p[k]-ctr)/.01;residual[~k]=20;vals.extend(residual.ravel())
      vals.append((abs(m.scalar(o.paraxial.f2()))-ch['efl_mm'])/.02);return np.nan_to_num(vals,nan=1e5,posinf=1e5,neginf=-1e5)
    except Exception:return np.full(2401,1e5)

def one_lens(ch):
    g=m.geometry('N1400_F63_SINGLE_FS',1400,63,50);seed=np.array([-.003,.003,1500.,180.])
    fit=least_squares(one_merit,seed,args=(ch,g),bounds=([-.03,-.03,1430,40],[.03,.03,1580,350]),x_scale='jac',max_nfev=60,ftol=2e-6,xtol=2e-7,gtol=2e-6)
    o=one_lens_build(ch,g,fit.x);tr=[one_trace(o,ch,f,w,10,40) for f in m.fields(ch) for w in ch['waves_um']]
    side=fit.x[2]+6+fit.x[3]-g['flat_distance_mm'];cell=m.DONOR_DIAMETER+14;dims=[cell+141+4,cell,g['flat_distance_mm']+55]
    lr=g['lens_diameter_mm']/2
    def sag(c,r):return c*r*r/(1+math.sqrt(max(0,1-c*c*r*r)))
    return {'geometry':g,'parameters':fit.x.tolist(),'effective_focal_length_mm':abs(m.scalar(o.paraxial.f2())),
      'f_number':abs(m.scalar(o.paraxial.f2()))/ch['pupil_mm'],'worst_rms_radius_um':max(t['rms_radius_um'] for t in tr),
      'minimum_survival':min(t['survival'] for t in tr),'traces':tr,'optimization':{'nfev':int(fit.nfev),'success':bool(fit.success),'message':fit.message},
      'physical':{'lens_edge_thickness_mm':6+sag(fit.x[1],lr)-sag(fit.x[0],lr),'side_exit_track_mm':side,
        'package_dimensions_mm':dims,'package_volume_l':float(np.prod(dims)/1e6),'custom_powered_surfaces':2,
        'focus_mechanisms_complete_payload':2,'large_optics_over_100mm':2}}

def write_one(path,ch,row):
    o=one_lens_build(ch,row['geometry'],row['parameters']);keys=['surface','radius_mm','conic','thickness_mm','material_post','is_stop']
    with path.open('w',newline='',encoding='utf-8') as f:
      w=csv.DictWriter(f,keys);w.writeheader()
      for i,s in enumerate(o.surfaces.surfaces):
        q=s.geometry;rad=m.scalar(q.radius) if hasattr(q,'radius') else math.inf
        w.writerow({'surface':i,'radius_mm':rad if np.isfinite(rad) else 'infinity','conic':m.scalar(q.k) if hasattr(q,'k') else '',
          'thickness_mm':m.scalar(s.thickness) if np.isfinite(m.scalar(s.thickness)) else 'infinity','material_post':str(s.material_post),'is_stop':s.is_stop})

def main():
    ch=m.channel(yaml.safe_load(m.REQ.read_text(encoding='utf-8')));tick=time.perf_counter();cas=cassegrain(ch);single=one_lens(ch)
    m.save('derivatives.json',{'attempt_4_stock_primary_custom_secondary':cas,'attempt_5_stock_primary_stock_flat_single_custom_lens':single,
      'script_wall_seconds':time.perf_counter()-tick})
    write_one(m.OUT/'n1400_f63_single_fs_swir_prescription.csv',ch,single);shutil.copy2(__file__,m.OUT/'track_c_run020_derivatives.py')
    print(json.dumps({'cassegrain':{'efl':cas['effective_focal_length_mm'],'rms':cas['worst_rms_radius_um'],'secondary':cas['physical']['custom_secondary_clear_diameter_mm'],'hole':cas['physical']['required_primary_hole_diameter_mm'],'volume':cas['physical']['package_volume_l'],'nfev':cas['optimization']['nfev']},
      'single_lens':{'efl':single['effective_focal_length_mm'],'rms':single['worst_rms_radius_um'],'survival':single['minimum_survival'],'volume':single['physical']['package_volume_l'],'nfev':single['optimization']['nfev']}},indent=2))

if __name__=='__main__':main()
