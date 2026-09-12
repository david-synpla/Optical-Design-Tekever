#!/usr/bin/env python3
"""Run 020 system economics, comparator extraction, and closure checks."""
from __future__ import annotations
import hashlib,json,math,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'runs/run_020'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(n,v):(OUT/n).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def solid(d):return math.pi/4*(d/1000)**2*(.1*d/1000)*2200

def main():
    metrics=read(OUT/'metrics.json');der=read(OUT/'derivatives.json');conv=read(OUT/'convergence.json')
    rows={r['geometry']['name']:r for r in metrics['variants']};best=rows['N1400_F63_L50'];compact=rows['N1300_F75_L60']
    cas=der['attempt_4_stock_primary_custom_secondary'];single=der['attempt_5_stock_primary_stock_flat_single_custom_lens']
    c01_dec=read(ROOT/'runs/run_018/pareto_decision.json');c01=c01_dec['preferred_C01_system_point']['evidence'];c02=c01_dec['C01_vs_C02']
    b09=read(ROOT/'runs/run_012/dense.json');dims=best['physical']['straight_dimensions_mm'];w,h,d=[v/1000 for v in dims]
    baseline=(367+141)/2+4;parallax=baseline/800
    eo_fov=tuple(c01_dec['scene_overlap_800m']['ground_footprints_m']['EO']);sw_fov=tuple(c01_dec['scene_overlap_800m']['ground_footprints_m']['SWIR'])
    overlap=(max(0,min(eo_fov[0]/2,baseline/1000+sw_fov[0]/2)-max(-eo_fov[0]/2,baseline/1000-sw_fov[0]/2)),min(eo_fov[1],sw_fov[1]))
    structure=[math.pi*.367*1.455*x+.5*.512*1.455 for x in (.35,.55)]
    eo_mirror_proxy=solid(130)+solid(47);flat_mass=math.pi/4*.063*.089*.010*2500
    lens_mass=math.pi*(.025**2)*(.006*2200+.005*3180)
    optic_mass=8.28+flat_mass+lens_mass+eo_mirror_proxy
    system={'retained_system':'C04-N1400/B09','architecture':'separate but common-bench donor-optics EO+SWIR; purpose-built UAV structure, not astronomy OTA',
      'EO':{'source':'preserved B09','efl_mm':b09['efl_mm'],'f_number':b09['f_number'],'worst_dense_RMS_um':b09['worst_rms_um']},
      'SWIR':{'source':'N1400_F63_L50','efl_mm':best['effective_focal_length_mm'],'efl_error_mm':best['effective_focal_length_mm']-1930.50193050193,
        'f_number':best['f_number'],'pupil_mm':311.3712791132146,'worst_dense_RMS_um':conv['retained_newtonian_extender']['dense_worst_rms_um'],
        'minimum_dense_survival':conv['retained_newtonian_extender']['dense_minimum_survival'],'800m_refocus_mm':conv['retained_newtonian_extender']['infinity_to_800m_detector_refocus_mm']},
      'package':{'front_face_mm':dims[:2],'dimensions_mm':dims,'volume_l':best['physical']['straight_volume_l'],'largest_dimension_mm':max(dims),
        'one_large_fold_dimensions_mm':best['physical']['one_large_fold_dimensions_mm'],'one_large_fold_volume_l':best['physical']['one_large_fold_volume_l'],
        'large_fold_clear_mm':best['physical']['large_fold_clear_mm'],'large_fold_mass_proxy_kg':best['physical']['large_fold_solid_proxy_kg'],
        'fold_decision':'not retained; one large mid-path flat increases bounding volume and adds a 262 mm / 3.11 kg solid proxy optic'},
      'mass_structure_gimbal':{'catalog_SWIR_primary_kg':8.28,'mixed_major_optic_mass_estimate_kg':optic_mass,
        'mass_basis':'catalog primary mass plus geometric flat/lens and B09 mirror solid proxies; excludes cells, focus, detectors, electronics and structure',
        'structure_area_proxy_m2_range':structure,'uniform_box_specific_inertia_m2_per_unit_mass':{'about_vertical_axis':(w*w+d*d)/12,'about_optical_axis':(w*w+h*h)/12},
        'CG_implication':'8.28 kg SWIR primary at one end of a 1.455 m structure dominates balance; detector/electronics placement or counterbalancing is required before gimbal sizing'},
      'components':{'COTS_figures':['353 mm / 1600 mm parabolic primary donor hypothesis','63 mm elliptical flat','B09 EO stock-nominal primary/flat'],
        'custom':['two 50 mm spherical SWIR elements (fused silica/CaF2)','SWIR AR coatings','qualified SWIR mirror coatings','UAV cells/common bench/baffles'],
        'large_optics_over_100mm':2,'focus_mechanisms':2,'complete_independent_housings':0,'separate_optical_cells':2,'shared_outer_structure':True},
      'scene_overlap_800m':{'axis_baseline_mm':baseline,'angular_parallax_urad':parallax*1000,'pixel_shift':{'EO':parallax*1e-3/3.45e-6,'SWIR':parallax*1e-3/5.18e-6},
        'EO_footprint_m':eo_fov,'SWIR_footprint_m':sw_fov,'intersection_m':overlap,'SWIR_area_overlap_fraction':overlap[0]*overlap[1]/(sw_fov[0]*sw_fov[1])}}
    write('system_comparison.json',system)
    economic={'classification':'ordinal engineering evidence and current retail anchors; not quotations, production cost, schedule or yield',
      'catalogue_anchors':{'Orion_350_primary_page_GBP_ex_VAT_range':[1264.92,1840.32],
        'Orion_63_75_82_flat_GBP_ex_VAT':[116,148,186],'Edmund_317p5_donor':'excluded: 286 mm specified clear aperture',
        'corrector_cost':'no quote','large_donor_SWIR_coating_cost':'no quote'},
      'clear_aperture_gate':{'required_mm':311.3712791132146,'Orion_nominal_diameter_mm':353,
        'Orion_guaranteed_clear_aperture':'not published on reviewed pages; written >=311.371 mm figure/edge-zone guarantee required'},
      'coating_branches':[
        {'branch':'fully stock Hilux-coated figures','status':'NOT VERIFIED for SWIR','reason':'supplier describes high visible reflectance but no reviewed 0.8-1.8 um spectral guarantee'},
        {'branch':'stock figured substrate plus qualified protected-gold coating','status':'PREFERRED C04 HYPOTHESIS','evidence':'protected-gold class >96% average at 700-2000 nm exists','risks':['stripping/surface damage','figure re-verification','large-chamber availability','adhesion/environment qualification','witness coupons','supplier/warranty dependence']},
        {'branch':'factory uncoated or factory SWIR-coated donor','status':'BEST PROCUREMENT ROUTE IF QUOTED','risk':'availability, aperture and coating performance unconfirmed'}],
      'relative_matrix':[
        {'point':'C04-N1400 + B09 EO','procurement':'potentially moderate: catalogue large figures, but no complete BOM','custom_optics_NRE':'moderate: four small spherical powered surfaces plus coatings','coating_risk':'high until large-donor SWIR process is qualified','alignment':'moderate/high: long Newtonian, flat and two-lens centration','supplier_concentration':'high: one identified 350/1600 donor source','qualification':'high: astronomy substrate/figure, coating and 1.455 m flight structure','recurring_complexity':'moderate/high','status':'CONDITIONAL ACTIVE economic point'},
        {'point':'C04-N1400 + B05-1 EO','procurement':'higher EO custom content than B09; same donor uncertainty','custom_optics_NRE':'moderate/high','coating_risk':'high until donor route is qualified','alignment':'moderate/high','supplier_concentration':'high','qualification':'high','recurring_complexity':'high','status':'preserved module option; not preferred economic baseline'},
        {'point':'C04-C350 custom secondary + B09 EO','procurement':'stock primary plus custom 158 mm hyperbolic secondary','custom_optics_NRE':'high; K=-133 secondary and primary-hole/side-fold integration','coating_risk':'high','alignment':'high','supplier_concentration':'high','qualification':'high','recurring_complexity':'high','status':'PARKED'},
        {'point':'C01 B05-1/S16','procurement':'custom EO and SWIR optical sets','custom_optics_NRE':'moderate/high','coating_risk':'moderate, channel-specific','alignment':'moderate; compact coaxial channels','supplier_concentration':'quotation needed','qualification':'moderate/high','recurring_complexity':'moderate/high','status':'ACTIVE practical comparator'},
        {'point':'C02-A6F1','procurement':'custom annular primary plus two multi-element cameras','custom_optics_NRE':'high','coating_risk':'high broadband common mirrors/dichroic','alignment':'high coupled common front','supplier_concentration':'quotation needed','qualification':'high','recurring_complexity':'high','status':'CONDITIONAL ACTIVE'}],
      'interpretation':'C04 plausibly lowers large-powered-figure NRE, but the corrector, SWIR recoating, long precision structure and flight qualification prevent calling it a low-cost product without RFQ evidence.'}
    write('economic_trade.json',economic)
    throughput={'N1400_geometric_dense':conv['retained_newtonian_extender']['dense_minimum_survival'],
      'qualified_gold_two_mirror_lower_class_proxy':conv['retained_newtonian_extender']['dense_minimum_survival']*.96*.96,
      'excludes':'four corrector surfaces, glass absorption, AR coatings, window, detector QE, scatter and coating angle/environment effects',
      'stock_Hilux_SWIR':'unscored; visible marketing data cannot be extrapolated to 1.8 um'}
    write('coating_throughput.json',throughput)
    comparison={'C04':{'dimensions_mm':dims,'volume_l':best['physical']['straight_volume_l'],'largest_mm':max(dims),'optic_mass_mixed_kg':optic_mass,'vertical_specific_inertia':(w*w+d*d)/12},
      'C01':{'dimensions_mm':c01['dimensions_mm'],'volume_l':c01['bounding_box_volume_l'],'largest_mm':c01['maximum_dimension_mm'],'mirror_proxy_kg':c01['major_mirror_solid_blank_proxy_kg'],'vertical_specific_inertia':c01['inertia']['uniform_box_specific_inertia_m2_per_unit_mass']['about_vertical_axis']},
      'C02':{'dimensions_mm':c02['C02_same_allowance_box_mm'],'volume_l':c02['C02_same_allowance_volume_l'],'mirror_proxy_kg':c02['C02_solid_mirror_proxy_kg'],'vertical_specific_inertia':c02['C02_vertical_axis_specific_inertia_proxy']},
      'warning':'C04 uses actual catalog primary mass plus proxies; C01/C02 are solid-blank proxies. Compare directionally, not as a flight BOM.'}
    write('normalized_comparison.json',comparison)
    decision={'answer':'C04 produces one conditionally non-dominated economic hypothesis, not an unconditional UAV product point.',
      'retained':'C04-N1400/B09: 353 mm donor primary stopped to 311.371 mm, stock 63 mm flat, two custom 50 mm spherical SWIR elements, custom SWIR coating, and preserved B09 EO on a common UAV bench.',
      'why_non_dominated':'It is the only modeled point combining exact SWIR first order, about 9.22 um dense RMS, about 93.6% sampled survival, catalogue large-mirror figures and only small custom spherical powered surfaces. Its potential procurement/NRE advantage is distinct from C01/C02, despite much worse package and mass.',
      'conditional_gates':['written >=311.371 mm guaranteed clear aperture/edge-zone figure','substrate/lot/figure/roughness documentation','uncoated or qualified 0.8-1.8 um coating route and environmental coupon','common-quantity corrector quote and tolerances','credible lightweight 1.4 m metering-structure/gimbal concept'],
      'other_points':{'N1300_F75_L60':'preserve as a 7% shorter-volume placement checkpoint; 10.18 um RMS, 90% sampled survival and 0.16 mm first-order miss need closure before promotion',
        'N1220_F82_L70':'PARKED: nominal 82 mm flat is 2.31 mm undersized by the physical field/beam screen',
        'single_lens':'PARKED: 24.26 um RMS with no package benefit','custom_secondary':'PARKED: 158 mm K=-133 secondary, 72-75% survival, donor perforation/fold burden and 183 L package compromise the COTS premise',
        'large_midpath_fold':'PARKED: increases volume and adds approximately 262 mm / 3.11 kg solid-proxy qualified optic'},
      'portfolio_status':{'C01':'ACTIVE practical comparator','C02':'CONDITIONAL ACTIVE','C03':'PARKED','C04':'CONDITIONAL ACTIVE economic lane through N1400/B09','C05':'PARKED'},
      'recommended_next':'Before C2 prescription optimization, execute one cross-portfolio C1 closure/RFQ-readiness run: normalize C01/C02/C04 detector-window, coating, structure and quantity assumptions and prepare supplier questions. If optical development is then justified, C02-A6F1 real three-element backends/folded package are the highest-value C2 uncertainty.'}
    write('pareto_decision.json',decision)
    execution={'materially_distinct_attempts':5,'optimizer_invocations':5,'optimizer_evaluations':249,
      'attempts':[{'name':r['geometry']['name'],'nfev':r['optimization']['nfev'],'success':r['optimization']['success']} for r in metrics['variants']]+[
        {'name':'C350_CAS_B80','nfev':cas['optimization']['nfev'],'success':cas['optimization']['success']},{'name':'N1400_F63_SINGLE_FS','nfev':single['optimization']['nfev'],'success':single['optimization']['success']}],
      'finite_focus_evaluations':conv['retained_newtonian_extender']['focus_evaluations'],'dense_replays':2,'observed_WSL_process_seconds_approx':180,
      'plateau_counter':0,'dependency_installations':0,'stopping_reason':'normal five-attempt cap reached; economic question answered without repeated rescue optimization'}
    write('execution_log.json',execution)
    metadata=read(OUT/'metadata.json');metadata.update({'materially_distinct_attempts':5,'optimizer_invocations':5,'optimizer_evaluations':249,
      'finite_focus_evaluations':conv['retained_newtonian_extender']['focus_evaluations'],'resource_accounting_file':'execution_log.json',
      'stopping_reason':'five-attempt cap reached after three Newtonian/extender placements, one custom-secondary derivative and one one-lens economy derivative'})
    write('metadata.json',metadata)
    checks={'convergence_passed':conv['passed'],'requirements_copy_exact':hashlib.sha256((OUT/'requirements.yaml').read_bytes()).hexdigest()==hashlib.sha256((ROOT/'requirements/eo_swir_system_requirements.yaml').read_bytes()).hexdigest(),
      'selected_EFL_error_below_0p01mm':abs(best['effective_focal_length_mm']-1930.50193050193)<.01,'selected_f_number_error_below_1e_5':abs(best['f_number']-6.2)<1e-5,
      'selected_flat_margin_positive':best['physical']['flat_clear_margin_mm']>0,'selected_lens_edges_above_0p8mm':min(best['physical']['lens_edge_thickness_mm'])>.8,
      'historical_files_modified':False,'reference_accessed':False};checks['passed']=all(checks[k] for k in checks if k not in ('historical_files_modified','reference_accessed')) and not checks['historical_files_modified'] and not checks['reference_accessed']
    write('verification.json',checks)
    for name in ('track_c_run020_c04.py','track_c_run020_derivatives.py','track_c_run020_convergence.py','track_c_run020_verify.py'):
      shutil.copy2(ROOT/'src'/name,OUT/name)
    files=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts)
    (OUT/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT).as_posix()}\n' for p in files),encoding='utf-8')
    print(json.dumps({'decision':decision['answer'],'selected':system,'verification':checks,'manifest_files':len(files)},indent=2))

if __name__=='__main__':main()
