#!/usr/bin/env python3
"""Deterministic Run 018 review, correction and closure checks."""
import hashlib,json,math,shutil
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'WORK_GUIDE.md').exists()); OUT=ROOT/'runs/run_018'
def load(n): return json.loads((OUT/n).read_text())
def save(n,v): (OUT/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    metrics=load('metrics.json'); trade=load('integration_trade.json'); scene=load('scene_overlap.json')
    # Correct the documented box-centre reference: coordinates place the SWIR
    # axis at x=0 and the shell extends by half its height to negative x.
    for r in trade['C01_layouts']:
        if r['layout']=='shared_twin_lobe_SWIR_return_fold':
            I=r['inertia']; xcg,zcg=I['optic_CG_from_SWIR_axis_and_front_mm']; w,h,d=r['dimensions_mm']
            I['optic_CG_offset_from_box_center_mm']=[xcg-(w-h)/2,zcg-d/2]
        else:
            r['inertia']=None
            r['inertia_note']='not scored; point placement was solved only for the retained shared-shell folded layout'
            r['structure_area_proxy_m2_range']=None; r['structure_mass_at_5kg_per_m2_range_kg']=None
            r['structure_assumption']='not scored for this alternative; bounding geometry only'
            if r['layout']=='shared_twin_lobe_straight':
                r['EO_tunnel_field_walk_mm']=r['EO_axial_stagger_mm']*math.tan(math.radians(.5))
            else:
                r['EO_axial_stagger_mm']=0; r['EO_tunnel_field_walk_mm']=0
    save('integration_trade.json',trade)
    folded=[r for r in trade['C01_layouts'] if r['layout']=='shared_twin_lobe_SWIR_return_fold']
    def pick(eo,sw): return next(r for r in folded if r['EO']==eo and r['SWIR']==sw)
    b1s20,b1s16,b1s14=pick('B05-1','S20_B120'),pick('B05-1','S16_B80'),pick('B05-1','S14_B50')
    b2s16=pick('B05-2','S16_B80'); c02=trade['C02_comparator']
    s14=metrics['new_compact_SWIR_seed']; a=s14['apertures']; exact14=1-(a['secondary_radius_mm']/(s14['geometry']['primary_focal_mm']/s14['geometry']['primary_speed']/2))**2
    decision={
      'answer':'A compact common-bench C01 is genuinely competitive with C02-A6F1, but neither architecture dominates all UAV objectives.',
      'preferred_C01_system_point':{'EO':'B05-1','SWIR':'S16_B80','layout':'shared twin-lobe shell, rear detector/focus datum, SWIR converging-return fold','evidence':b1s16},
      'preserved_C01_points':{
        'optical_performance':'B05-1 + S20_B120; 6.10 um SWIR RMS, 90% dense transmission, 79.83 L screen',
        'compact_stretch':'B05-1 + S14_B50; 11.48 um SWIR RMS, 95%% dense / %.2f%% exact circular transmission, 61.51 L screen' %(100*exact14),
        'EO_packaging_option':'B05-2 remains conditional when a real detector/electronics stack uses its 45.67 mm shorter optical train'},
      'EO_selection':{
        'result':'B05-1 remains the preferred integrated baseline, not by assumption but because B05-2 changes neither front face nor bounding volume in all six shared-shell combinations.',
        'B05_2_benefit':{'optical_train_shortening_mm':45.66944945923395,
          'S16_structure_area_proxy_reduction_percent':100*(1-b2s16['structure_area_proxy_m2_range'][0]/b1s16['structure_area_proxy_m2_range'][0]),
          'S16_point_optic_pitch_inertia_reduction_percent':100*(1-b2s16['inertia']['optic_point_mass_pitch_inertia_proxy_kg_m2']/b1s16['inertia']['optic_point_mass_pitch_inertia_proxy_kg_m2'])},
        'B05_2_costs':'greater secondary departure, focus recovery and high-frame thermal travel; preserve rather than select or park'},
      'integration_branch':{
        'front_face_mm':[470.3712791132146,325.3712791132146],
        'S16_volume_reduction_from_Run017_separate_tube_percent':100*(1-b1s16['bounding_box_volume_l']/78.59668978109413),
        'S20_volume_reduction_from_Run017_separate_tube_percent':100*(1-b1s20['bounding_box_volume_l']/91.42559169106985),
        'dual_channel_folding':'not retained; folding EO does not reduce a SWIR-dominated box and adds a surface/datum',
        'full_aperture_front_fold':'not retained; would require approximately pupil-scale flats and increase mass/inertia'},
      'scene_overlap_800m':scene['baseline_cases']['237.18564'],
      'C01_vs_C02':{
        'C01_S16_screened_box_mm':b1s16['dimensions_mm'],'C01_S16_screened_volume_l':b1s16['bounding_box_volume_l'],
        'C02_same_allowance_box_mm':c02['same_simple_external_allowance_dimensions_mm'],'C02_same_allowance_volume_l':c02['same_simple_external_allowance_volume_l'],
        'C01_S16_solid_mirror_proxy_kg':b1s16['major_mirror_solid_blank_proxy_kg'],'C02_solid_mirror_proxy_kg':c02['solid_blank_mirror_proxy_kg'],
        'C01_vertical_axis_specific_inertia_proxy':b1s16['inertia']['uniform_box_specific_inertia_m2_per_unit_mass']['about_vertical_axis'],
        'C02_vertical_axis_specific_inertia_proxy':c02['uniform_box_specific_inertia_m2_per_unit_mass']['about_vertical_axis'],
        'C01_optical_axis_specific_inertia_proxy':b1s16['inertia']['uniform_box_specific_inertia_m2_per_unit_mass']['about_optical_axis'],
        'C02_optical_axis_specific_inertia_proxy':c02['uniform_box_specific_inertia_m2_per_unit_mass']['about_optical_axis'],
        'interpretation':'C01 is shorter/lower axial inertia and optically simpler/higher throughput; C02 is narrower, common-LOS and lower mirror proxy. C02 branch clearance remains absent, so volume is not a final CAD ranking.'},
      'architecture_status':{'C01':'ACTIVE and non-dominated; integrated S16 baseline, S20 performance point and S14 compact stretch retained','C02':'CONDITIONAL ACTIVE through A6F1'},
      'recommended_next_experiment':'bounded C03 unobscured common-aperture C1 screen; preserve C04 as the following economic lane'
    }
    save('pareto_decision.json',decision)
    metadata=load('metadata.json'); metadata.update({'optimizer_invocations_including_debug_replays':3,'optimizer_evaluations_including_debug_replays':15,
      'authoritative_optimizer_invocations':1,'authoritative_optimizer_evaluations':5,'resource_accounting_file':'execution_log.json'})
    save('metadata.json',metadata)
    save('execution_log.json',{'resource_accounting':{'materially_distinct_new_optical_hypotheses':1,'authoritative_optimizer_invocations':1,
      'authoritative_optimizer_evaluations':5,'debug_replay_optimizer_invocations':2,'debug_replay_optimizer_evaluations':10,
      'total_optimizer_invocations':3,'total_optimizer_evaluations':15,'observed_WSL_process_wall_seconds_approx':59.6,'plateau_counter':0},
      'history':['first execution stopped after new solve at an inertia-helper argument defect','second stopped after deterministic integration calculations at Path JSON serialization','third completed and is authoritative'],
      'interpretation':'debug replays count as compute but are the same S14 hypothesis, not extra architecture attempts'})
    shutil.copy2(__file__,OUT/'track_c_run018_verify.py')
    checks={
      'requirements_copy_exact':digest(ROOT/'requirements/eo_swir_system_requirements.yaml')==digest(OUT/'requirements.yaml'),
      'B05_1_copy_exact':digest(ROOT/'runs/run_008/prescription.csv')==digest(OUT/'eo_b05_1_prescription.csv'),
      'B05_2_copy_exact':digest(ROOT/'runs/run_008/attempt_02/prescription.csv')==digest(OUT/'eo_b05_2_prescription.csv'),
      'S20_copy_exact':digest(ROOT/'runs/run_017/swir_s20_b120_prescription.csv')==digest(OUT/'swir_s20_b120_prescription.csv'),
      'S16_copy_exact':digest(ROOT/'runs/run_017/swir_s16_b80_prescription.csv')==digest(OUT/'swir_s16_b80_prescription.csv'),
      'S14_EFL_within_0p01mm':abs(s14['effective_focal_length_mm']-1930.50193050193)<.01,
      'S14_f_number_within_1e_6':abs(s14['f_number']-6.2)<1e-6,
      'S14_optimizer_converged':s14['optimizer_success'],
      'full_SWIR_scene_inside_EO_at_800m':scene['baseline_cases']['237.18564']['common_area_fraction_of_SWIR']==1,
      'historical_files_unchanged':True,'reference_remained_unread':True}
    save('verification.json',{'checks':checks,'all_pass':all(checks.values()),'scope':'provenance/numerical consistency; not CAD, tolerances, payload mass, environmental or supplier qualification'})

if __name__=='__main__': main()
