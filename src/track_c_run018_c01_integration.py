#!/usr/bin/env python3
"""Run 018: bounded C01 UAV integration trade.

Preserved B05-1/B05-2 and Run 017 SWIR evidence are combined in common-shell,
staggered and folded layouts. One new three-variable S14_B50 SWIR solve extends
the compact end. Package, structure, CG/inertia and finite-range overlap are
screening proxies, not CAD, payload mass, tolerances or customer limits.
"""
from __future__ import annotations
import csv, hashlib, importlib.util, json, math, platform, shutil, sys, time
from datetime import datetime, timezone
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import optiland, scipy, yaml

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists())
OUT=ROOT/'runs/run_018'
REQ=ROOT/'requirements/eo_swir_system_requirements.yaml'
RUN017=ROOT/'runs/run_017'
RUN016=ROOT/'runs/run_016'

def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def save(name,v): (OUT/name).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def import_run017():
    spec=importlib.util.spec_from_file_location('run017model',ROOT/'src/track_c_run017_c01.py')
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def eo_variants():
    return [
      {'name':'B05-1','prescription':str(ROOT/'runs/run_008/prescription.csv'),'configuration':str(ROOT/'runs/run_008/configuration.json'),
       'optical_length_mm':329.0375678790805,'mirror_separation_mm':231.78919251777828,
       'dense_worst_rms_um':.800,'low_CTE_endpoint_rms_um':[.799,.801],
       'low_CTE_max_thermal_focus_mm':.0385,'high_frame_max_thermal_focus_mm':1.3746,
       'range_focus_800m_mm':.7901,'focus_only_coupled_largest_rms_um':1.063,
       'secondary_radius_mm':-541.9007433554357,'secondary_departure_um':14.66,
       'assessment':'balanced lower sensitivity/metrology reference'},
      {'name':'B05-2','prescription':str(ROOT/'runs/run_008/attempt_02/prescription.csv'),'configuration':str(ROOT/'runs/run_008/attempt_02/configuration.json'),
       'optical_length_mm':283.36811841984655,'mirror_separation_mm':197.3857978048293,
       'dense_worst_rms_um':.576,'low_CTE_endpoint_rms_um':[.627,.544],
       'low_CTE_max_thermal_focus_mm':.0491,'high_frame_max_thermal_focus_mm':1.7578,
       'range_focus_800m_mm':.7957,'focus_only_coupled_largest_rms_um':1.335,
       'secondary_radius_mm':-310.4817449172851,'secondary_departure_um':38.80,
       'assessment':'45.67 mm shorter but tighter/higher-departure secondary and greater recovery sensitivity'}]

def channel(req,name):
    r=req['source_explicit_requirements'][name]; pitch=r['pixel_pitch_um'][0]/1000
    f=pitch/(r['instantaneous_fov_urad_per_pixel']*1e-6)
    hx=math.atan(r['array_px'][0]*pitch/(2*f)); hy=math.atan(r['array_px'][1]*pitch/(2*f))
    return {'name':name.upper(),'efl_mm':f,'pupil_mm':f/r['f_number'],'half_x_rad':hx,'half_y_rad':hy,
            'horizontal_fov_deg':math.degrees(2*hx),'vertical_fov_deg':math.degrees(2*hy)}

def sag(radius,k,r):
    c=1/radius
    return c*r*r/(1+math.sqrt(1-(1+k)*c*c*r*r))

def mirror_burden(row):
    g,a,x=row['geometry'],row['apertures'],row['solution']; rr=a['primary_radius_mm']; dr=rr*1e-6+1e-6
    z=sag(g['primary_radius_mm'],x['primary_conic'],rr)
    slope=(z-sag(g['primary_radius_mm'],x['primary_conic'],rr-dr))/dr
    return {'primary_clear_diameter_mm':2*rr,'primary_edge_sag_mm':abs(z),
            'primary_edge_slope_deg':math.degrees(math.atan(abs(slope))),
            'primary_vertex_sphere_departure_um':abs(z-sag(g['primary_radius_mm'],0,rr))*1000,
            'secondary_clear_diameter_mm':2*a['secondary_radius_mm'],'primary_hole_diameter_mm':2*a['hole_radius_mm']}

def mirror_mass(d_outer,d_inner=0):
    return math.pi/4*((d_outer/1000)**2-(d_inner/1000)**2)*(.1*d_outer/1000)*2200

def swir_mass(row):
    a=row['apertures']; return mirror_mass(2*a['primary_radius_mm'],2*a['hole_radius_mm'])+mirror_mass(2*a['secondary_radius_mm'])

def fold_clear(run17,row,swir):
    g,a,x=row['geometry'],row['apertures'],row['solution']
    model,ind=run17.build_swir(g,swir,[x['primary_conic'],x['secondary_conic'],x['detector_focus_mm']],a,fold_probe_fraction=.35)
    tr=run17.trace(model,ind,swir,run17.fields(swir)[5],swir['waves_um'][1],16,48,a['secondary_radius_mm']/(swir['pupil_mm']/2))
    return 2*tr['surfaces']['fold_probe']['max_radius_mm']*math.sqrt(2)+4

def overlap(eo,swir,baseline_mm,range_m=800):
    R=range_m*1000; shift=baseline_mm
    def width(half): return 2*R*math.tan(half)
    eo_x=(-R*math.tan(eo['half_x_rad']),R*math.tan(eo['half_x_rad']))
    sw_x=(shift-R*math.tan(swir['half_x_rad']),shift+R*math.tan(swir['half_x_rad']))
    eo_y=(-R*math.tan(eo['half_y_rad']),R*math.tan(eo['half_y_rad']))
    sw_y=(-R*math.tan(swir['half_y_rad']),R*math.tan(swir['half_y_rad']))
    ix=max(0,min(eo_x[1],sw_x[1])-max(eo_x[0],sw_x[0])); iy=max(0,min(eo_y[1],sw_y[1])-max(eo_y[0],sw_y[0]))
    sw_area=width(swir['half_x_rad'])*width(swir['half_y_rad'])
    eo_area=width(eo['half_x_rad'])*width(eo['half_y_rad'])
    angle=math.atan(baseline_mm/R)
    full_h=baseline_mm/(math.tan(eo['half_x_rad'])-math.tan(swir['half_x_rad']))/1000
    full_v=baseline_mm/(math.tan(eo['half_y_rad'])-math.tan(swir['half_y_rad']))/1000
    return {'range_m':range_m,'axis_baseline_mm':baseline_mm,'angular_parallax_urad':angle*1e6,
      'pixel_displacement':{'EO':angle/3.45e-6,'SWIR':angle/5.18e-6},
      'ground_footprints_m':{'EO':[width(eo['half_x_rad'])/1000,width(eo['half_y_rad'])/1000],
                             'SWIR':[width(swir['half_x_rad'])/1000,width(swir['half_y_rad'])/1000],
                             'common_intersection':[ix/1000,iy/1000]},
      'common_area_fraction_of_SWIR':ix*iy/sw_area,'common_area_fraction_of_EO':ix*iy/eo_area,
      'full_SWIR_containment_minimum_range_m':{'horizontal_baseline':full_h,'vertical_baseline':full_v},
      'interpretation':'parallel infinity-boresighted axes and planar target; ignores terrain relief, range error, distortion and boresight drift'}

def point_optic_inertia(eo,row,baseline,eo_offset,bbox):
    # Projected clear-area x 22.5 kg/m2 is a common lightweight optic-mass
    # sensitivity coefficient, not a substrate or payload-mass selection.
    coeff=22.5; a=row['apertures']; g=row['geometry']
    items=[]
    def add(name,d,x,z): items.append({'name':name,'mass_proxy_kg':coeff*math.pi/4*(d/1000)**2,'x_m':x/1000,'z_m':z/1000})
    add('SWIR primary',2*a['primary_radius_mm'],0,g['mirror_separation_mm']+3)
    add('SWIR secondary',2*a['secondary_radius_mm'],0,3)
    add(f"{eo['name']} primary",133,baseline,eo_offset+eo['mirror_separation_mm']+3)
    add(f"{eo['name']} secondary",71,baseline,eo_offset+3)
    mt=sum(i['mass_proxy_kg'] for i in items); xc=sum(i['mass_proxy_kg']*i['x_m'] for i in items)/mt; zc=sum(i['mass_proxy_kg']*i['z_m'] for i in items)/mt
    Iy=sum(i['mass_proxy_kg']*((i['x_m']-xc)**2+(i['z_m']-zc)**2) for i in items)
    w,h,d=[v/1000 for v in bbox]
    return {'assumption':'four mirrors as point masses at vertices; projected clear area x 22.5 kg/m2; lenses, cells, detectors, electronics and shell excluded',
      'items':items,'optic_mass_proxy_kg':mt,'optic_CG_from_SWIR_axis_and_front_mm':[xc*1000,zc*1000],
      'optic_CG_offset_from_box_center_mm':[xc*1000-(-.5*(bbox[0]-baseline)+bbox[0]/2),zc*1000-bbox[2]/2],
      'optic_point_mass_pitch_inertia_proxy_kg_m2':Iy,
      'uniform_box_specific_inertia_m2_per_unit_mass':{'about_vertical_axis':(w*w+d*d)/12,'about_optical_axis':(w*w+h*h)/12}}

def package_rows(eos,swirs,run17,swir_ch):
    rows=[]
    for eo in eos:
      for sw in swirs:
        g,a=sw['geometry'],sw['apertures']; fold=fold_clear(run17,sw,swir_ch)
        sw_od=2*a['primary_radius_mm']+12; eo_od=133+8; web=4
        shared_width=sw_od+eo_od+web; shared_height=sw_od; baseline=.5*(sw_od+eo_od)+web
        fold_rear=g['mirror_separation_mm']+3+.35*g['backfocus_mm']+35
        straight_rear=g['mirror_separation_mm']+3+g['backfocus_mm']+35
        eo_offset=max(0,fold_rear-(eo['optical_length_mm']+25))
        tunnel_walk=eo_offset*math.tan(math.radians(.5))
        # Open saddle cells on one bench: 50-80% of mirror-cell circumference,
        # plus one bench planform. This is a scalable structural area proxy.
        cell_area=(math.pi*(sw_od/1000)*(g['mirror_separation_mm']/1000)+math.pi*(eo_od/1000)*(eo['mirror_separation_mm']/1000))
        bench_area=(shared_width/1000)*(fold_rear/1000)
        structure_area=[.5*cell_area+bench_area,.8*cell_area+bench_area]
        common={'EO':eo['name'],'SWIR':g['name'],'front_face_dimensions_mm':[shared_width,shared_height],
          'axis_baseline_mm':baseline,'EO_axial_stagger_mm':eo_offset,'EO_tunnel_field_walk_mm':tunnel_walk,
          'SWIR_fold_clear_mm':fold,'major_mirror_solid_blank_proxy_kg':swir_mass(sw)+.383091265,
          'large_optics_over_100_mm':2,'focus_mechanisms':2,'powered_optics':6,
          'structure_area_proxy_m2_range':structure_area,'structure_mass_at_5kg_per_m2_range_kg':[5*v for v in structure_area],
          'structure_assumption':'50-80% open-saddle circumference for two mirror cells plus one common bench planform; scale linearly with actual areal density'}
        for layout,depth,extra in [
          ('shared_twin_lobe_SWIR_return_fold',fold_rear,{}),
          ('shared_twin_lobe_straight',straight_rear,{'EO_axial_stagger_mm':max(0,straight_rear-(eo['optical_length_mm']+25))}),
          ('separate_tube_screen_reference',g['mirror_separation_mm']+3+.35*g['backfocus_mm']+55,
           {'front_face_dimensions_mm':[2*a['primary_radius_mm']+24+153+10,2*a['primary_radius_mm']+24],
            'axis_baseline_mm':.5*(2*a['primary_radius_mm']+24+153)+10})]:
            r=dict(common); r.update(extra); r['layout']=layout
            front=r['front_face_dimensions_mm']; r['dimensions_mm']=[front[0],front[1],depth]
            r['bounding_box_volume_l']=float(np.prod(r['dimensions_mm'])/1e6); r['maximum_dimension_mm']=max(r['dimensions_mm'])
            r['EO_optical_performance']={'worst_dense_RMS_um':eo['dense_worst_rms_um'],'focus_only_coupled_largest_RMS_um':eo['focus_only_coupled_largest_rms_um']}
            r['SWIR_optical_performance']={'worst_RMS_um':sw['worst_rms_radius_um'],'minimum_dense_transmission':sw['minimum_survival']}
            r['inertia']=point_optic_inertia(eo,sw,baseline,eo_offset,r['dimensions_mm'])
            rows.append(r)
    return rows

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'metadata.json').exists(): raise RuntimeError('Run 018 is already closed and immutable')
    tick=time.perf_counter(); started=datetime.now(timezone.utc)
    req=yaml.safe_load(REQ.read_text(encoding='utf-8')); eo_ch=channel(req,'eo'); sw_ch=channel(req,'swir')
    r17=import_run017(); r17.SWIR=r17.channel(req,'swir')
    old=load(RUN017/'metrics.json')['swir_seed_results']; keep=[r for r in old if r['geometry']['name'] in ('S20_B120','S16_B80')]
    g=r17.swir_geometry('S14_B50',r17.SWIR,1.4,50); fresh=r17.solve_seed(g,r17.SWIR,max_nfev=55); fresh['finite_focus_800m']=r17.finite_focus(fresh,r17.SWIR)
    swirs=keep+[fresh]; eos=eo_variants(); packages=package_rows(eos,swirs,r17,r17.SWIR)
    overlaps={str(round(r['axis_baseline_mm'],6)):overlap(eo_ch,sw_ch,r['axis_baseline_mm']) for r in packages}
    c02=load(RUN016/'swap_screen.json'); d=c02['bounding_box']['unfolded_coaxial_lower_bound_dimensions_mm']
    c02_screen=[d[0]+24,d[1]+24,d[2]+55]
    c02_comp={'optical_lower_bound_dimensions_mm':d,'optical_lower_bound_volume_l':c02['bounding_box']['unfolded_coaxial_lower_bound_volume_l'],
      'same_simple_external_allowance_dimensions_mm':c02_screen,'same_simple_external_allowance_volume_l':float(np.prod(c02_screen)/1e6),
      'single_tube_lateral_area_proxy_m2':math.pi*(c02_screen[0]/1000)*(c02_screen[2]/1000),
      'solid_blank_mirror_proxy_kg':c02['major_optic_mass_proxy']['combined_common_mirror_mass_proxy_kg'],
      'uniform_box_specific_inertia_m2_per_unit_mass':{'about_vertical_axis':((c02_screen[0]/1000)**2+(c02_screen[2]/1000)**2)/12,
        'about_optical_axis':2*(c02_screen[0]/1000)**2/12},
      'limitations':'branch fold, camera cells, electronics and dichroic clearances remain unproved'}
    save('metrics.json',{'EO_variants':eos,'preserved_SWIR_seeds':keep,'new_compact_SWIR_seed':fresh})
    save('integration_trade.json',{'classification':'bounded geometry and scalable proxies, not CAD, payload mass or tolerance proof','C01_layouts':packages,'C02_comparator':c02_comp})
    save('scene_overlap.json',{'channel_fields':{'EO':eo_ch,'SWIR':sw_ch},'baseline_cases':overlaps})
    save('manufacturing_screen.json',{'new_seed':mirror_burden(fresh),'comparison':{'S20_B120':mirror_burden(keep[0]),'S16_B80':mirror_burden(keep[1])},
      'decision':'S14_B50 extends compactness with higher surface slope/departure; no catadioptric corrector was added because it would not shorten the dominant two-mirror separation without a new powered architecture'})
    provenance={}
    for label,path in [('requirements',REQ),('run017_metrics',RUN017/'metrics.json'),('run016_swap',RUN016/'swap_screen.json'),
      ('B05_1_prescription',eos[0]['prescription']),('B05_2_prescription',eos[1]['prescription'])]: provenance[label]={'path':str(Path(path).relative_to(ROOT)).replace('\\','/'),'sha256':digest(path)}
    provenance.update({'historical_files_modified':False,'contamination_control':'reference/ not accessed'})
    save('provenance.json',provenance)
    r17.write_prescription(OUT/'prescription.csv',fresh,r17.SWIR)
    shutil.copy2(eos[0]['prescription'],OUT/'eo_b05_1_prescription.csv'); shutil.copy2(eos[1]['prescription'],OUT/'eo_b05_2_prescription.csv')
    shutil.copy2(RUN017/'swir_s20_b120_prescription.csv',OUT/'swir_s20_b120_prescription.csv'); shutil.copy2(RUN017/'swir_s16_b80_prescription.csv',OUT/'swir_s16_b80_prescription.csv')
    shutil.copy2(REQ,OUT/'requirements.yaml'); shutil.copy2(__file__,OUT/'track_c_run018_c01_integration.py')
    # Plot only common-shell folded points; labels expose EO choice and SWIR branch.
    pts=[r for r in packages if r['layout']=='shared_twin_lobe_SWIR_return_fold']
    fig,ax=plt.subplots(1,2,figsize=(10,4.5))
    for marker,eo in [('o','B05-1'),('s','B05-2')]:
      q=[r for r in pts if r['EO']==eo]; ax[0].scatter([r['bounding_box_volume_l'] for r in q],[r['SWIR_optical_performance']['worst_RMS_um'] for r in q],marker=marker,label=eo)
      ax[1].scatter([r['inertia']['uniform_box_specific_inertia_m2_per_unit_mass']['about_vertical_axis'] for r in q],[r['inertia']['uniform_box_specific_inertia_m2_per_unit_mass']['about_optical_axis'] for r in q],marker=marker,label=eo)
      for r in q: ax[0].annotate(r['SWIR'],(r['bounding_box_volume_l'],r['SWIR_optical_performance']['worst_RMS_um']),xytext=(4,4),textcoords='offset points',fontsize=8)
    ax[0].set(xlabel='Screened bounding-box volume (L)',ylabel='SWIR worst RMS radius (um)'); ax[1].set(xlabel='Vertical-axis specific inertia proxy (m2)',ylabel='Optical-axis specific inertia proxy (m2)')
    for a in ax: a.grid(alpha=.25); a.legend();
    fig.tight_layout(); fig.savefig(OUT/'integrated_c01_pareto.png',dpi=180); plt.close(fig)
    save('dependencies.json',{'python':sys.version,'platform':platform.platform(),'optiland':optiland.__version__,'numpy':np.__version__,'scipy':scipy.__version__})
    save('metadata.json',{'track':'C','run_id':'018','candidate_ids':['C01'],'parent_run':'run_017','development_stage':'C1 bounded UAV integration experiment',
      'start_time_utc':started.isoformat(),'end_time_utc':datetime.now(timezone.utc).isoformat(),'script_wall_seconds':time.perf_counter()-tick,
      'materially_distinct_new_optical_hypotheses':1,'optimizer_invocations':1,'optimizer_evaluations':fresh['optimizer_nfev'],'plateau_counter':0,
      'integration_layout_classes':3,'stopping_reason':'EO choice, common-shell geometry, compact SWIR extension, inertia and finite-range scene overlap answer the bounded integration question',
      'contamination_control':'reference/ not accessed'})
    print(json.dumps({'S14':{'worst_um':fresh['worst_rms_radius_um'],'survival':fresh['minimum_survival'],'nfev':fresh['optimizer_nfev']},
      'shared_folded':[{'EO':r['EO'],'SWIR':r['SWIR'],'dims':r['dimensions_mm'],'L':r['bounding_box_volume_l']} for r in pts]},indent=2))

if __name__=='__main__': main()
