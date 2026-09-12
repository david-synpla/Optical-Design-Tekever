#!/usr/bin/env python3
"""Run 019: bounded C03 off-axis common-afocal architecture screen.

Four two-paraboloid geometries trade compression, powered-mirror separation
and off-axis magnitude. Nominal ideal-backend imaging and representative
mirror decenter/tilt sensitivity are evaluated together. A dichroic plus one
passive camera-path fold supplies a physical package witness. No freeforms.
"""
from __future__ import annotations
import argparse,copy,csv,hashlib,json,math,platform,shutil,sys,time
from datetime import datetime,timezone
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import optiland,scipy,yaml
from optiland import optic
from optiland.physical_apertures import OffsetRadialAperture
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
OUT=ROOT/'runs/run_019'; REQ=ROOT/'requirements/eo_swir_system_requirements.yaml'
MARGIN=2.0; SPLIT_AFTER_PRIMARY=45.0

def scalar(v): return float(np.asarray(v).reshape(-1)[0])
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def save(n,v): (OUT/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def channel(req,name):
    r=req['source_explicit_requirements'][name]; pitch=r['pixel_pitch_um'][0]/1000
    f=pitch/(r['instantaneous_fov_urad_per_pixel']*1e-6); pupil=f/r['f_number']
    hx=math.degrees(math.atan(r['array_px'][0]*pitch/(2*f))); hy=math.degrees(math.atan(r['array_px'][1]*pitch/(2*f))); diag=math.hypot(hx,hy)
    return {'name':name.upper(),'efl_mm':f,'pupil_mm':pupil,'hx':hx/diag,'hy':hy/diag,'diag_deg':diag,
      'half_x_deg':hx,'half_y_deg':hy,'waves_um':[.43,.55,.80] if name=='eo' else [.80,1.20,1.80]}

def fields(c):
    x,y=c['hx'],c['hy']; return [('center',0,0),('+x',x,0),('-x',-x,0),('+y',0,y),('-y',0,-y),('corner++',x,y),('corner+-',x,-y),('corner-+',-x,y),('corner--',-x,-y)]

def pupil(g,nr=10,na=32):
    r=np.sqrt((np.arange(nr)+.5)/nr)*.997; t=2*np.pi*(np.arange(na)+.5)/na; R=g['pupil_mm']/2; P=g['parent_radius_mm']
    return (r[:,None]*np.cos(t)*R/P).ravel(),((r[:,None]*np.sin(t)*R+g['off_axis_mm'])/P).ravel()

def geometry(name,pupil_mm,compression,primary_speed,off_axis_mm):
    f1=primary_speed*pupil_mm; f2=f1/compression; sep=f1-f2; R=pupil_mm/2
    threshold=R*(compression+1)/(compression-1)
    return {'name':name,'pupil_mm':pupil_mm,'compression':compression,'primary_speed':primary_speed,
      'primary_focal_mm':f1,'secondary_focal_mm':f2,'mirror_separation_mm':sep,'off_axis_mm':off_axis_mm,
      'unobscured_geometric_threshold_mm':threshold,'off_axis_margin_above_threshold_mm':off_axis_mm-threshold,
      'primary_radius_mm':-2*f1,'secondary_radius_mm':-2*f2,'parent_radius_mm':off_axis_mm+R+MARGIN}

def configure(o,c,g):
    o.set_aperture(aperture_type='EPD',value=2*g['parent_radius_mm']); o.fields.set_type('angle'); o.fields.add(y=0); o.fields.add(y=c['diag_deg'])
    for w in c['waves_um']: o.wavelengths.add(value=w,is_primary=w==c['waves_um'][1])

def build(g,c,aps=None,focus=0,ks=(-1.0,-1.0)):
    huge=1000; pa=aps['primary'] if aps else {'r':huge,'x':0,'y':g['off_axis_mm']}; sa=aps['secondary'] if aps else {'r':huge,'x':0,'y':0}; ca=aps['camera'] if aps else {'r':huge,'x':0,'y':0}
    sep=g['mirror_separation_mm']; fcam=c['efl_mm']/g['compression']
    o=optic.Optic(name=f"C03 {g['name']} {c['name']} ideal backend")
    o.surfaces.add(index=0,thickness=np.inf)
    o.surfaces.add(index=1,thickness=sep+3,is_stop=True,aperture=OffsetRadialAperture(g['pupil_mm']/2,offset_y=g['off_axis_mm']))
    o.surfaces.add(index=2,radius=g['primary_radius_mm'],thickness=-sep,conic=ks[0],material='mirror',aperture=OffsetRadialAperture(pa['r'],offset_x=pa['x'],offset_y=pa['y']))
    o.surfaces.add(index=3,radius=g['secondary_radius_mm'],thickness=sep,conic=ks[1],material='mirror',aperture=OffsetRadialAperture(sa['r'],offset_x=sa['x'],offset_y=sa['y']))
    o.surfaces.add(index=4,thickness=SPLIT_AFTER_PRIMARY)
    o.surfaces.add(index=5,surface_type='paraxial',f=fcam,thickness=fcam+focus,aperture=OffsetRadialAperture(ca['r'],offset_x=ca['x'],offset_y=ca['y']))
    o.surfaces.add(index=6); configure(o,c,g)
    return o,{'primary':2,'secondary':3,'return_primary_plane':4,'camera':5,'image':6}

def trace(o,ind,g,c,fld,w,nr=10,na=32,raw=False):
    px,py=pupil(g,nr,na); _,hx,hy=fld; rays=o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,w)
    sx,sy,si=map(np.asarray,(o.surfaces.x,o.surfaces.y,o.surfaces.intensity)); valid=np.isfinite(np.asarray(rays.x))&np.isfinite(np.asarray(rays.y))&(np.asarray(rays.i)>0)
    out={'field':fld[0],'wave_um':w,'survival':float(valid.mean()),'surfaces':{}}
    for n,i in ind.items():
      ok=np.isfinite(sx[i])&np.isfinite(sy[i])&(si[i]>0); pts=np.column_stack((sx[i,ok],sy[i,ok]))
      if len(pts):
        ctr=(pts.max(0)+pts.min(0))/2; rad=np.max(np.linalg.norm(pts-ctr,axis=1)); out['surfaces'][n]={'center_mm':ctr.tolist(),'radius_mm':float(rad)}
    if np.any(valid):
      p=np.column_stack((np.asarray(rays.x)[valid],np.asarray(rays.y)[valid])); ctr=p.mean(0); residual=p-ctr
      out.update({'centroid_mm':ctr.tolist(),'rms_radius_um':float(np.sqrt(np.mean(np.sum(residual**2,axis=1)))*1000)})
      if raw: out['_points']=p; out['_valid']=valid
    return out

def size_apertures(g,channels,ks=(-1.0,-1.0),focuses=(0.0,0.0)):
    pts={k:[] for k in ('primary','secondary','return_primary_plane','camera')}
    for ci,c in enumerate(channels):
      o,ind=build(g,c,focus=focuses[ci],ks=ks)
      for f in fields(c):
        r=trace(o,ind,g,c,f,c['waves_um'][1],8,28)
        for k in pts:
          d=r['surfaces'][k]; center=np.array(d['center_mm']); rr=d['radius_mm']; pts[k].append((center,rr))
    aps={}
    for k,rows in pts.items():
      lo=np.min([c-r for c,r in rows],axis=0); hi=np.max([c+r for c,r in rows],axis=0); ctr=(lo+hi)/2
      # Enclose the union of circular footprint bounds, not merely the larger
      # half-width of their rectangular envelope (which can clip diagonals).
      radius=float(max(np.linalg.norm(c-ctr)+r for c,r in rows)+MARGIN)
      aps[k]={'x':float(ctr[0]),'y':float(ctr[1]),'r':radius}
    # The physical primary segment cannot be smaller than the full required
    # entrance pupil merely because the finite pupil quadrature omits its rim.
    aps['primary']={'x':0.0,'y':g['off_axis_mm'],'r':max(aps['primary']['r'],g['pupil_mm']/2+MARGIN)}
    # The split/camera aperture is the same physical collimated beam envelope.
    aps['camera']=aps['camera']; return aps

def sample_model(g,c,aps,model=None,nr=8,na=24,focus=0,ks=(-1.0,-1.0)):
    o,ind=build(g,c,aps,focus,ks) if model is None else (model,{'primary':2,'secondary':3,'return_primary_plane':4,'camera':5,'image':6})
    raws=[]; rows=[]
    for f in fields(c):
      r=trace(o,ind,g,c,f,c['waves_um'][1],nr,na,raw=True); p=r.pop('_points'); r.pop('_valid'); residual=p-p.mean(0)
      raws.append(residual.ravel()); rows.append(r)
    return np.concatenate(raws),{'worst_rms_radius_um':max(r['rms_radius_um'] for r in rows),'median_rms_radius_um':float(np.median([r['rms_radius_um'] for r in rows])),
      'minimum_survival':min(r['survival'] for r in rows),'rows':rows}

def sag(r,R,k=-1):
    c=1/R; return c*r*r/(1+np.sqrt(1-(1+k)*c*c*r*r))

def perturb(o,index,ap,mode,amount):
    q=copy.deepcopy(o); geom=q.surfaces[index].geometry; p=np.array([0.,0.,float(geom.cs.z)]); p[:2]=[ap['x'],ap['y']]
    p[2]+=float(sag(np.hypot(ap['x'],ap['y']),float(geom.radius),float(geom.k)))
    if mode in ('x','y'):
      setattr(geom.cs,mode,float(getattr(geom.cs,mode))+amount)
    else:
      rv=np.zeros(3); rv[0 if mode=='tx' else 1]=amount; rot=Rotation.from_rotvec(rv); Rm=rot.as_matrix(); v=np.array([float(geom.cs.x),float(geom.cs.y),float(geom.cs.z)])
      v=p+Rm@(v-p); geom.cs.x,geom.cs.y,geom.cs.z=v; angles=rot.as_euler('xyz'); geom.cs.rx,geom.cs.ry,geom.cs.rz=angles
    return q

def sensitivity(g,c,aps,ks=(-1.0,-1.0),focus=0):
    # Sensitivity is evaluated without hard mirror-edge clipping so the vector
    # length stays fixed and measures aberration/registration, while clearance
    # and aperture survival are reported separately by the physical model.
    nominal,_=build(g,c,None,focus,ks); base_vec,base=sample_model(g,c,aps,nominal,6,20); rows=[]
    for mirror,index in [('primary',2),('secondary',3)]:
      for mode,step in [('x',.01),('y',.01),('tx',1e-4),('ty',1e-4)]:
        minus=perturb(nominal,index,aps[mirror],mode,-step); plus=perturb(nominal,index,aps[mirror],mode,step)
        vm,mm=sample_model(g,c,aps,minus,6,20); vp,mp=sample_model(g,c,aps,plus,6,20)
        response=(vp-vm)/2; rows.append({'mirror':mirror,'mode':mode,'step':step,'unit':'mm' if len(mode)==1 else 'rad',
          'rms_residual_response_um_at_step':float(np.sqrt(np.mean(response**2))*1000),
          'minus_worst_rms_um':mm['worst_rms_radius_um'],'plus_worst_rms_um':mp['worst_rms_radius_um'],
          'worst_centroid_shift_um':max(max(np.linalg.norm((np.array(a['centroid_mm'])-np.array(b['centroid_mm'])))*1000 for a,b in zip(mm['rows'],base['rows'])),
                                           max(np.linalg.norm((np.array(a['centroid_mm'])-np.array(b['centroid_mm'])))*1000 for a,b in zip(mp['rows'],base['rows'])))})
    return {'diagnostic':'central finite difference at +/-10 um X/Y decenter and +/-100 urad X/Y tilt; one mirror at a time; no compensator',
      'nominal':base,'rows':rows,'composite_centered_residual_response_um':float(np.sqrt(sum(r['rms_residual_response_um_at_step']**2 for r in rows))),
      'maximum_centroid_shift_um':max(r['worst_centroid_shift_um'] for r in rows)}

def circle_gap(a,b): return math.hypot(a['x']-b['x'],a['y']-b['y'])-a['r']-b['r']

def evaluate(g,channels,ks=(-1.0,-1.0),focuses=(0.0,0.0)):
    aps=size_apertures(g,channels,ks,focuses); optical={}; sensitivities={}
    for ci,c in enumerate(channels):
      o,ind=build(g,c,aps,focuses[ci],ks); rows=[trace(o,ind,g,c,f,w,16,48) for f in fields(c) for w in c['waves_um']]
      optical[c['name']]={'efl_mm':abs(scalar(o.paraxial.f2())),'f_number':abs(scalar(o.paraxial.f2()))/g['pupil_mm'],
        'worst_rms_radius_um':max(r['rms_radius_um'] for r in rows),'minimum_survival':min(r['survival'] for r in rows),'rows':rows}
      sensitivities[c['name']]=sensitivity(g,c,aps,ks,focuses[ci])
    incoming={'x':0,'y':g['off_axis_mm'],'r':g['pupil_mm']/2}
    clearance={'incoming_to_secondary_mm':circle_gap(incoming,aps['secondary']),
      'return_beam_to_primary_mm':circle_gap(aps['return_primary_plane'],aps['primary']),
      'fold_beam_to_primary_cell_projected_mm':circle_gap(aps['camera'],aps['primary'])}
    fold_clear=2*aps['camera']['r']*math.sqrt(2)+4
    return {'geometry':g,'solution':{'primary_conic':ks[0],'secondary_conic':ks[1],'EO_focus_mm':focuses[0],'SWIR_focus_mm':focuses[1]},'apertures':aps,'optical':optical,'sensitivity':sensitivities,'clearance':clearance,
      'minimum_circle_clearance_mm':min(clearance.values()),'fold_clear_mm':fold_clear}

def fixed_residual_vector(o,g,c,nr=5,na=16):
    values=[]
    for f in (fields(c)[0],fields(c)[1],fields(c)[3],fields(c)[5]):
      px,py=pupil(g,nr,na); _,hx,hy=f; rays=o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,c['waves_um'][1])
      p=np.column_stack((np.asarray(rays.x),np.asarray(rays.y))); valid=np.isfinite(p).all(1)&(np.asarray(rays.i)>0)
      residual=np.full_like(p,.3)
      if np.any(valid): residual[valid]=p[valid]-p[valid].mean(0)
      values.extend(residual.ravel())
    return np.asarray(values)

def robust_merit(v,g,channels,pivots):
    ks=v[:2]; focuses=v[2:]
    values=[]
    try:
      for ci,c in enumerate(channels):
        nominal,_=build(g,c,None,focuses[ci],ks); base=fixed_residual_vector(nominal,g,c)
        # Nominal performance and three representative relative alignment modes
        # are in the same solve.  The 0.35 factor is a screening trade weight,
        # not a tolerance or customer threshold.
        values.extend(base/.008)
        for mirror,index,mode,step in [('primary',2,'tx',1e-4),('secondary',3,'tx',1e-4),('secondary',3,'y',.01)]:
          minus=perturb(nominal,index,pivots[mirror],mode,-step); plus=perturb(nominal,index,pivots[mirror],mode,step)
          response=(fixed_residual_vector(plus,g,c)-fixed_residual_vector(minus,g,c))/2
          values.extend(.35*response/.008)
      values.extend([(ks[0]+1)/2,(ks[1]+1)/4,focuses[0]/3,focuses[1]/3])
      return np.nan_to_num(values,nan=1e4,posinf=1e4,neginf=-1e4)
    except Exception:
      # 2 channels x (nominal + 3 perturbation responses) x 4 fields x
      # 5 rings x 16 azimuth x 2 coordinates, plus 4 regularizers.
      return np.full(2*4*4*5*16*2+4,1e4)

def solve_robust(g,channels,max_nfev=45):
    base_aps=size_apertures(g,channels)
    seed=np.array([-1.,-1.,0.,0.])
    fit=least_squares(robust_merit,seed,args=(g,channels,base_aps),bounds=([-5,-15,-5,-5],[0,0,5,5]),
      x_scale='jac',max_nfev=max_nfev,ftol=2e-6,xtol=2e-7,gtol=2e-6)
    refined=copy.deepcopy(g); refined['name']=g['name']+'_R'
    result=evaluate(refined,channels,fit.x[:2],fit.x[2:])
    result['optimization']={'objective':'nominal plus representative alignment response; no nominal-only precursor',
      'initial':seed.tolist(),'final':fit.x.tolist(),'nfev':int(fit.nfev),'success':bool(fit.success),'message':fit.message,
      'screening_sensitivity_weight':.35}
    return result

def parent_metrics(g,aps,solution):
    outer=g['off_axis_mm']+aps['primary']['r']; radius=g['primary_radius_mm']; k=solution['primary_conic']
    dr=max(1e-3,outer*1e-5); slope=math.degrees(math.atan(abs((sag(outer+dr,radius,k)-sag(outer-dr,radius,k))/(2*dr))))
    segment_d=2*aps['primary']['r']; parent_d=2*(g['off_axis_mm']+aps['primary']['r'])
    def mass(d): return math.pi/4*(d/1000)**2*(.1*d/1000)*2200
    return {'illuminated_entrance_diameter_mm':g['pupil_mm'],'primary_clear_segment_diameter_mm':segment_d,
      'primary_parent_axis_full_diameter_mm':parent_d,'primary_outer_parent_radius_mm':outer,'primary_outer_slope_deg':slope,
      'segment_solid_blank_proxy_kg':mass(segment_d),'full_parent_disk_solid_blank_proxy_kg':mass(parent_d),
      'interpretation':'segment proxy assumes direct segment blank; full-parent proxy is a fabrication/metrology upper branch, not required procurement'}

def package(result,channels):
    g=result['geometry']; aps=result['apertures']; eo,sw=channels
    # Common front z extent plus cells. Dichroic reflects one camera; one passive
    # flat folds the other oppositely, so lateral camera extent sums both focal
    # lengths and half-beam/cell allowances.
    front_y_lo=min(aps['primary']['y']-aps['primary']['r'],aps['secondary']['y']-aps['secondary']['r'],aps['return_primary_plane']['y']-aps['return_primary_plane']['r'])
    front_y_hi=max(aps['primary']['y']+aps['primary']['r'],aps['secondary']['y']+aps['secondary']['r'],aps['return_primary_plane']['y']+aps['return_primary_plane']['r'])
    front_y=front_y_hi-front_y_lo+20; front_x=max(2*aps[k]['r'] for k in ('primary','secondary','return_primary_plane'))+20
    camera_lateral=eo['efl_mm']/g['compression']+sw['efl_mm']/g['compression']+2*aps['camera']['r']+60
    folded=[max(front_x,camera_lateral),front_y,g['mirror_separation_mm']+SPLIT_AFTER_PRIMARY+45]
    straight=[front_x,front_y,g['mirror_separation_mm']+SPLIT_AFTER_PRIMARY+max(eo['efl_mm'],sw['efl_mm'])/g['compression']+55]
    parent=parent_metrics(g,aps,result['solution'])
    # Segment mirrors plus dichroic/fold use a 0.1D solid proxy for continuity.
    mirror_ds=[2*aps['primary']['r'],2*aps['secondary']['r']]
    camera_clear=2*aps['camera']['r']; fold_clear=result['fold_clear_mm']
    modeled_optic_sizes=mirror_ds+[fold_clear,fold_clear,camera_clear,camera_clear]
    solid=sum(math.pi/4*(d/1000)**2*(.1*d/1000)*2200 for d in mirror_ds)
    w,h,d=[v/1000 for v in folded]
    return {'passive_folded_dimensions_mm':folded,'passive_folded_volume_l':float(np.prod(folded)/1e6),
      'straight_dimensions_mm':straight,'straight_volume_l':float(np.prod(straight)/1e6),
      'largest_dimension_mm':max(folded),'powered_mirror_count':2,'flat_fold_count':1,'dichroic_count':1,'focus_mechanisms':2,
      'large_optics_over_100mm':sum(x>100 for x in modeled_optic_sizes),'modeled_optic_sizes_mm':modeled_optic_sizes,
      'common_mirror_segment_solid_proxy_kg':solid,
      'parent_and_segment':parent,'uniform_box_specific_inertia_m2_per_unit_mass':{'about_vertical_axis':(w*w+d*d)/12,'about_optical_axis':(w*w+h*h)/12},
      'limitations':'ideal camera focal lengths set branch envelopes; no physical camera prescription, cells, electronics or fold tilt model'}

def write_prescription(path,result,c):
    s=result['solution']; focus=s['EO_focus_mm'] if c['name']=='EO' else s['SWIR_focus_mm']; ks=(s['primary_conic'],s['secondary_conic'])
    o,_=build(result['geometry'],c,result['apertures'],focus,ks); keys=['surface','radius_mm','conic','thickness_mm','material_post','is_stop']
    with path.open('w',newline='',encoding='utf-8') as f:
      w=csv.DictWriter(f,keys); w.writeheader()
      for i,s in enumerate(o.surfaces.surfaces):
        q=s.geometry; rad=scalar(q.radius) if hasattr(q,'radius') else math.inf
        w.writerow({'surface':i,'radius_mm':rad if np.isfinite(rad) else 'infinity','conic':scalar(q.k) if hasattr(q,'k') else '',
          'thickness_mm':scalar(s.thickness) if np.isfinite(scalar(s.thickness)) else 'infinity','material_post':str(s.material_post),'is_stop':s.is_stop})

def main():
    p=argparse.ArgumentParser(); p.add_argument('--probe',action='store_true'); p.add_argument('--resume',action='store_true'); args=p.parse_args(); req=yaml.safe_load(REQ.read_text()); channels=[channel(req,'eo'),channel(req,'swir')]; D=channels[1]['pupil_mm']
    geometries=[geometry('A4_F1p2_O289',D,4,1.2,289),geometry('A6_F1p0_O250',D,6,1.0,250),
      geometry('A6_F1p4_O256',D,6,1.4,256),geometry('A8_F1p0_O237',D,8,1.0,237)]
    if args.probe:
      for g in geometries:
        r=evaluate(g,channels); print(g['name'],{'rms':{k:v['worst_rms_radius_um'] for k,v in r['optical'].items()},'clear':r['clearance'],'sens':{k:v['composite_centered_residual_response_um'] for k,v in r['sensitivity'].items()},'aps':r['apertures']})
      return
    OUT.mkdir(parents=True,exist_ok=args.resume)
    if (OUT/'SHA256SUMS.txt').exists(): raise RuntimeError('Run 019 is closed and immutable')
    tick=time.perf_counter(); started=datetime.now(timezone.utc)
    results=[evaluate(g,channels) for g in geometries]
    # One fifth and final materially distinct attempt: sensitivity-aware conic
    # refinement of the best nominal low-compression form. No nominal-only solve.
    results.append(solve_robust(geometries[0],channels))
    for r in results: r['package']=package(r,channels)
    save('metrics.json',{'variants':results}); shutil.copy2(REQ,OUT/'requirements.yaml'); shutil.copy2(__file__,OUT/'track_c_run019_c03.py')
    for r in results: write_prescription(OUT/f"{r['geometry']['name'].lower()}_eo_ideal_prescription.csv",r,channels[0])
    save('provenance.json',{'requirements':{'path':'requirements/eo_swir_system_requirements.yaml','sha256':digest(REQ)},
      'guidance':'Wang et al., Optics Communications 575 (2025) 131228, DOI 10.1016/j.optcom.2024.131228; sensitivity-aware architecture screening, no transferred target',
      'historical_files_modified':False,'contamination_control':'reference/ not accessed'})
    save('dependencies.json',{'python':sys.version,'platform':platform.platform(),'optiland':optiland.__version__,'numpy':np.__version__,'scipy':scipy.__version__})
    save('metadata.json',{'track':'C','run_id':'019','candidate_ids':['C03'],'parent_run':'run_018','development_stage':'C1 bounded architecture experiment',
      'start_time_utc':started.isoformat(),'end_time_utc':datetime.now(timezone.utc).isoformat(),'script_wall_seconds':time.perf_counter()-tick,
      'materially_distinct_architecture_attempts':5,'optimizer_invocations':1,
      'optimizer_evaluations':results[-1]['optimization']['nfev'],'plateau_counter':0,
      'substantial_batches':['four-geometry nominal full-field trace','four-geometry representative two-channel sensitivity diagnostic','physical aperture/clearance and passive-fold packaging'],
      'stopping_reason':'four spacing/compression/off-axis points plus one sensitivity-aware conic refinement exhaust the normal five-attempt screen without freeform escalation','contamination_control':'reference/ not accessed'})
    fig,ax=plt.subplots(1,2,figsize=(10,4.5))
    ax[0].scatter([r['package']['passive_folded_volume_l'] for r in results],[r['optical']['EO']['worst_rms_radius_um'] for r in results])
    ax[1].scatter([r['package']['parent_and_segment']['primary_parent_axis_full_diameter_mm'] for r in results],[r['sensitivity']['EO']['composite_centered_residual_response_um'] for r in results])
    for r in results:
      n=r['geometry']['name']; ax[0].annotate(n,(r['package']['passive_folded_volume_l'],r['optical']['EO']['worst_rms_radius_um']),fontsize=8); ax[1].annotate(n,(r['package']['parent_and_segment']['primary_parent_axis_full_diameter_mm'],r['sensitivity']['EO']['composite_centered_residual_response_um']),fontsize=8)
    ax[0].set(xlabel='Passive-fold package proxy (L)',ylabel='EO ideal-backend worst RMS (um)'); ax[1].set(xlabel='Primary full-parent diameter (mm)',ylabel='EO composite sensitivity response (um)')
    for a in ax:a.grid(alpha=.25)
    fig.tight_layout();fig.savefig(OUT/'c03_pareto.png',dpi=180);plt.close(fig)
    print(json.dumps([{'name':r['geometry']['name'],'rms':{k:v['worst_rms_radius_um'] for k,v in r['optical'].items()},'sens':{k:v['composite_centered_residual_response_um'] for k,v in r['sensitivity'].items()},'clear':r['minimum_circle_clearance_mm'],'package_L':r['package']['passive_folded_volume_l']} for r in results],indent=2))

if __name__=='__main__': main()
