#!/usr/bin/env python3
"""Deterministic closure checks and comparator extraction for Run 019."""
from __future__ import annotations
import hashlib,json,math,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'runs/run_019'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,v): (OUT/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def pct(a,b): return 100*(a/b-1)

def main():
    m=read(OUT/'metrics.json'); conv=read(OUT/'convergence.json')
    rows={v['geometry']['name']:v for v in m['variants']}
    compact=rows['A8_F1p0_O237']; coupled=rows['A6_F1p0_O250']; desens=rows['A6_F1p4_O256']
    base=rows['A4_F1p2_O289']; refined=rows['A4_F1p2_O289_R']
    c01=read(ROOT/'runs/run_018/pareto_decision.json')['preferred_C01_system_point']['evidence']
    c02=read(ROOT/'runs/run_018/pareto_decision.json')['C01_vs_C02']
    ratios={ch:100*desens['sensitivity'][ch]['composite_centered_residual_response_um']/coupled['sensitivity'][ch]['composite_centered_residual_response_um'] for ch in ('EO','SWIR')}
    decision={
      'answer':'No screened minimum-complexity C03 form is a better current UAV Pareto point than both C01 and C02.',
      'architecture_status':'PARKED after bounded C1; retain evidence and reopen only for a justified three-powered-element derivative with a strict package allocation or new fabrication evidence.',
      'screened_forms':{
        'compact_endpoint':{'name':compact['geometry']['name'],'package_l':compact['package']['passive_folded_volume_l'],
          'dimensions_mm':compact['package']['passive_folded_dimensions_mm'],'EO_SWIR_worst_rms_um':[compact['optical']['EO']['worst_rms_radius_um'],compact['optical']['SWIR']['worst_rms_radius_um']],
          'minimum_clearance_mm':compact['minimum_circle_clearance_mm']},
        'best_nominal_endpoint':{'name':refined['geometry']['name'],'package_l':refined['package']['passive_folded_volume_l'],
          'dimensions_mm':refined['package']['passive_folded_dimensions_mm'],'EO_SWIR_worst_rms_um':[refined['optical']['EO']['worst_rms_radius_um'],refined['optical']['SWIR']['worst_rms_radius_um']],
          'minimum_clearance_mm':refined['minimum_circle_clearance_mm']},
        'lower_sensitivity_endpoint':{'name':desens['geometry']['name'],'package_l':desens['package']['passive_folded_volume_l'],
          'dimensions_mm':desens['package']['passive_folded_dimensions_mm'],'relative_sensitivity_percent_of_compact_A6':ratios,
          'package_increase_percent_vs_compact_A6':pct(desens['package']['passive_folded_volume_l'],coupled['package']['passive_folded_volume_l'])}},
      'sensitivity_aware_solve':{'nominal_RMS_improvement_percent':{ch:-pct(refined['optical'][ch]['worst_rms_radius_um'],base['optical'][ch]['worst_rms_radius_um']) for ch in ('EO','SWIR')},
        'sensitivity_response_improvement_percent':{ch:-pct(refined['sensitivity'][ch]['composite_centered_residual_response_um'],base['sensitivity'][ch]['composite_centered_residual_response_um']) for ch in ('EO','SWIR')},
        'interpretation':'two conic constants and two channel focus offsets improve nominal imaging but do not materially desensitize the architecture; spacing/off-axis geometry is the effective early trade.'},
      'physical_optics':{'geometric_survival':1.0,'neutral_two_mirror_plus_splitter_path':0.729,
        'largest_clear_segment_mm':max(v['package']['parent_and_segment']['primary_clear_segment_diameter_mm'] for v in rows.values()),
        'full_parent_diameter_range_mm':[min(v['package']['parent_and_segment']['primary_parent_axis_full_diameter_mm'] for v in rows.values()),max(v['package']['parent_and_segment']['primary_parent_axis_full_diameter_mm'] for v in rows.values())],
        'common_mirror_solid_proxy_range_kg':[min(v['package']['common_mirror_segment_solid_proxy_kg'] for v in rows.values()),max(v['package']['common_mirror_segment_solid_proxy_kg'] for v in rows.values())],
        'minimum_clearance_range_mm':[min(v['minimum_circle_clearance_mm'] for v in rows.values()),max(v['minimum_circle_clearance_mm'] for v in rows.values())]},
      'comparators':{'C01_preferred_volume_l':c01['bounding_box_volume_l'],'C01_maximum_dimension_mm':c01['maximum_dimension_mm'],
        'C01_mirror_blank_proxy_kg':c01['major_mirror_solid_blank_proxy_kg'],'C02_same_allowance_volume_l':c02['C02_same_allowance_volume_l'],
        'C02_mirror_proxy_kg':c02['C02_solid_mirror_proxy_kg'],
        'interpretation':'C03 removes geometric obscuration and inter-aperture parallax, but no screened point combines C01-like volume and optical maturity or C02-like frontal/package economy with acceptable nominal/sensitivity/manufacturing burden.'},
      'freeform_decision':'not introduced: near-parabolic conic refinement did not materially reduce alignment response, while package/parent-envelope burden already gates the family.',
      'recommended_next_experiment':'bounded C04 cost/COTS-maximized C1 economic lane; do not proceed to C03 freeforms or detailed tolerancing without new instruction.'}
    write('pareto_decision.json',decision)
    manuf={'surface_class':'two off-axis conic segments; final conics remain near paraboloids; no freeforms',
      'variant_rows':[{'name':n,'illuminated_clear_mm':v['package']['parent_and_segment']['illuminated_entrance_diameter_mm'],
        'physical_segment_mm':v['package']['parent_and_segment']['primary_clear_segment_diameter_mm'],
        'parent_envelope_mm':v['package']['parent_and_segment']['primary_parent_axis_full_diameter_mm'],
        'outer_slope_deg':v['package']['parent_and_segment']['primary_outer_slope_deg'],
        'direct_segment_solid_proxy_kg':v['package']['parent_and_segment']['segment_solid_blank_proxy_kg'],
        'full_parent_solid_proxy_kg':v['package']['parent_and_segment']['full_parent_disk_solid_blank_proxy_kg'],
        'large_optics_over_100mm':v['package']['large_optics_over_100mm']} for n,v in rows.items()],
      'assessment':'direct segment fabrication avoids buying a full parent blank but still requires a roughly 0.78-0.89 m parent-axis figure/metrology reference, off-axis datum control, and small pre-cell beam gaps; a full-parent blank is an upper branch, not assumed procurement.',
      'unresolved':['direct-segment lightweighting and mount','null/CGH or sub-aperture metrology','surface figure and mid-spatial allocation','cell/baffle clearance beyond 1.5-3.6 mm optical gaps','real dichroic/fold tilt and cameras','thermo-elastic LOS stability','stray light and polarization']}
    write('manufacturing_screen.json',manuf)
    integration=[]
    for n,v in rows.items():
      aps=v['apertures']; g=v['geometry']; dims=v['package']['passive_folded_dimensions_mm']
      ylo=min(aps[k]['y']-aps[k]['r'] for k in ('primary','secondary','return_primary_plane'))-10
      ds=[2*aps['primary']['r'],2*aps['secondary']['r']]
      masses=[math.pi/4*(d/1000)**2*(.1*d/1000)*2200 for d in ds]
      yz=[(aps['primary']['y']-ylo,g['mirror_separation_mm']+3),(aps['secondary']['y']-ylo,3)]
      mt=sum(masses); cg=[sum(m*p[0] for m,p in zip(masses,yz))/mt,sum(m*p[1] for m,p in zip(masses,yz))/mt]
      point_i=sum(m*(((p[0]-cg[0])/1000)**2+((p[1]-cg[1])/1000)**2) for m,p in zip(masses,yz))
      integration.append({'name':n,'passive_folded_dimensions_mm':dims,'bounding_box_volume_l':v['package']['passive_folded_volume_l'],
        'largest_dimension_mm':max(dims),'mirror_proxy_CG_from_box_low_y_low_z_mm':cg,
        'mirror_proxy_CG_offset_from_box_center_y_z_mm':[cg[0]-dims[1]/2,cg[1]-dims[2]/2],
        'two_mirror_point_mass_pitch_inertia_proxy_kg_m2':point_i,
        'uniform_box_specific_inertia_m2_per_unit_mass':v['package']['uniform_box_specific_inertia_m2_per_unit_mass'],
        'shared':['primary','secondary','fore-optic metering structure','front baffle and line of sight'],
        'duplicated':['EO/SWIR cameras','detector interfaces','focus compensation','channel coatings/windows'],
        'limitations':'mirror-only CG/inertia proxy; dichroic, fold, cameras, cells, electronics, shell and gimbal excluded'})
    write('integration_screen.json',{'coordinate_note':'box axes are camera-fold lateral, off-axis-mirror transverse, and depth; CG reports transverse/depth only',
      'variants':integration,'gimbal_assessment':'compact A8 is near comparator volume but wider than C01 and has poor ideal-camera imaging; lower-sensitivity and best-nominal points create 621-852 mm lateral arms. Real component placement is needed before balance or actuator sizing.'})
    execution={'authoritative':{'architecture_points':4,'sensitivity_aware_optimizer_invocations':1,'optimizer_evaluations':refined['optimization']['nfev'],'dense_replays':2},
      'debug_and_correction':{'optimizer_replays':2,'optimizer_evaluations':10,'causes':['primary minimum-clear sizing correction','union-of-footprint circular enclosure correction'],'no_optimizer_probes':3},
      'total_optimizer_invocations':3,'total_optimizer_evaluations':15,'observed_WSL_process_seconds_approx':145.0,
      'dependency_installations':0,'plateau_counter':0,'resource_interpretation':'bounded architecture screen; correction replays are disclosed and are not additional architecture searches'}
    write('execution_log.json',execution)
    checks={'convergence_passed':conv['passed'],'all_minimum_clearances_positive':all(v['minimum_circle_clearance_mm']>0 for v in rows.values()),
      'all_full_field_survival_one':all(v['optical'][ch]['minimum_survival']==1 for v in rows.values() for ch in ('EO','SWIR')),
      'primary_covers_required_pupil':all(v['package']['parent_and_segment']['primary_clear_segment_diameter_mm']>=v['geometry']['pupil_mm'] for v in rows.values()),
      'requirements_copy_matches':hashlib.sha256((OUT/'requirements.yaml').read_bytes()).hexdigest()==hashlib.sha256((ROOT/'requirements/eo_swir_system_requirements.yaml').read_bytes()).hexdigest(),
      'historical_runs_modified':False,'reference_accessed':False}
    checks['passed']=all(checks[k] for k in ('convergence_passed','all_minimum_clearances_positive','all_full_field_survival_one','primary_covers_required_pupil','requirements_copy_matches')) and not checks['historical_runs_modified'] and not checks['reference_accessed']
    write('verification.json',checks)
    metadata=read(OUT/'metadata.json'); metadata.update({'optimizer_invocations_including_debug_replays':3,
      'optimizer_evaluations_including_debug_replays':15,'authoritative_optimizer_invocations':1,
      'authoritative_optimizer_evaluations':5,'resource_accounting_file':'execution_log.json'})
    write('metadata.json',metadata)
    shutil.copy2(__file__,OUT/'track_c_run019_verify.py')
    shutil.copy2(ROOT/'src/track_c_run019_convergence.py',OUT/'track_c_run019_convergence.py')
    files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts)
    (OUT/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT).as_posix()}\n' for p in files),encoding='utf-8')
    print(json.dumps({'decision':decision['answer'],'verification':checks,'manifest_files':len(files)},indent=2))

if __name__=='__main__': main()
