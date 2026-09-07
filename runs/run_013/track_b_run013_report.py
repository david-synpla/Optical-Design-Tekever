"""Close and hash Run013 after verifying all archived checkpoints."""
import json,hashlib,shutil
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import track_b_run013_thermal as T
O=T.OUT
def main():
    lines=['# Run 013 — matched thermal/material comparison','',
    'Decision: retain B05-1, B05-2 and B06. Prefer an effective low-CTE support concept for the next performance-lane engineering stage. This is a uniform-temperature scenario study, not thermal qualification or a material procurement selection. Nominal shapes are unchanged.','',
    'The user explicitly prioritized this study over further B09 development. Run012 paused after its in-flight solve; its verification resumes only after this study closes. Lack of a proprietary COTS prescription remains unverified performance, never an assumed low score.','',
    '## Material and modelling assumptions','',
    '- Nominal 20 C, sampled -25, -10, 20, 35, 50 C; uniform equilibrium, fixed 1 atm air-relative glass indices. Six equal-weight wavelengths 430–800 nm; nine signed fields, 64 equal-area pupil rays. Endpoint validation uses 25 fields and 576 pupil samples.',
    '- Mirror CTE 0.52 ppm/K is a constant fused-silica-like approximation; Corning reports that mean near room temperature, not a certified constant over this entire range. Frame effective CTE 1.2 and 24 ppm/K are engineering cases, not selected structures. A homogeneous 24 ppm/K mirror/frame case is an ideal homology bound, not proof that an aluminium visible-light mirror meets figure, coating or metrology needs.',
    '- N-BK7/N-F2 use 7.1/7.8 ppm/K glass expansion and the installed SCHOTT catalog thermo-optic coefficients; catalog hashes and computed indices are in glass_provenance.json. Lenses expand about their mechanical centers; mirror patch centers follow the frame while parent curvature/off-axis coordinates expand with the substrate. Conics remain fixed.',
    '- Source entrance stop expands with the frame. Its B05 annulus remains the previously disclosed shadow approximation. Real mounts, gradients, stress, thermal lag, detector pixel-pitch expansion, pressure/altitude changes, coating deformation and the unspecified detector window are excluded. Those exclusions prevent a claim of compliance across the operating envelope.','',
    'Primary sources: [SCHOTT N-BK7](https://media.schott.com/api/public/content/41e799d0bf874807a0bb8e702fbb75b5?v=54856406), [SCHOTT N-F2](https://media.schott.com/api/public/content/061f3156c83a44ed9220770b0f65a869?v=d69b35e0), [Corning HPFS](https://www.corning.com/media/worldwide/csm/documents/1e624b3034474193b5b00ea6f558dd3d2.pdf), [thyssenkrupp 6005 expansion example](https://www.thyssenkrupp-materials.co.uk/aluminium-6005.html/index.html). Values inform scenarios; no hardware is ordered.','',
    '## Matched endpoint results','',
    'The Run010 diagnostic caps remain +/-0.5 mm detector Z and +/-1 mrad secondary tilt. High-frame mismatch saturates focus. A separately labelled +/-5 mm travel diagnostic uses two local linear correction steps, no shape optimization. It distinguishes actuator travel from residual aberration. Travel is signed global detector Z, not a common optical-axis sign.','',
    '| Case / candidate | Cold / hot dense RMS, um | Cold / hot detector Z, mm | Central image-scale range, mm |',
    '|---|---:|---:|---:|']
    fig,axs=plt.subplots(1,3,figsize=(12,3.4),sharey=True)
    interfaces=json.loads((O/'interface_verification.json').read_text())['results']
    for ax,cid in zip(axs,['B05-1','B05-2','B06']):
        data=json.loads((O/(cid+'.json')).read_text());v=json.loads((O/(cid+'_verification.json')).read_text())
        assert data['zero_temperature_max_residual_error_mm']<1e-10 and data['homology_max_error_mm']<1e-8
        for scenario in T.SCENARIOS:
            rows=[r for r in v['rows'] if r['scenario']==scenario];values=[r['dense']['worst_rms_um'] for r in rows]
            travel=[r['iterations'][-1]['applied']['detector_z'] for r in rows]
            scales=[s for r in rows for s in r['image_scale']['axis_scales_mm']]
            assert all(r['dense']['minimum_survival']==1 for r in rows)
            lines.append(f"| {scenario} / {cid} | {values[0]:.3f} / {values[1]:.3f} | {travel[0]:+.4f} / {travel[1]:+.4f} | {min(scales):.3f}–{max(scales):.3f} |")
            ax.plot([-25,50],values,'o-',label=scenario.replace('_',' '))
        ax.set_title(cid);ax.set_xlabel('Uniform temperature (C)');ax.grid(alpha=.3)
    axs[0].set_ylabel('Dense worst RMS (um)');axs[-1].legend(fontsize=7);fig.tight_layout();fig.savefig(O/'thermal_comparison.png',dpi=160)
    lines+=['','Low-frame cases preserve near-nominal performance with modest thermal travel. B05-1 is less sensitive than the compact B05-2 to high-frame mismatch; B06 needs both more travel and off-axis compensation. The ideal homogeneous case suppresses first-order mismatch but carries unquantified visible-mirror manufacturing risk. No universal winner follows.','',
    '## Diffraction and range checks','',
    'Endpoint low-frame PSFs compare actual versus the same transmitted-pupil diffraction limit at 430, 550 and 800 nm, center and corner; 50/100/150/182.482 lp/mm and 2x2-pixel EE are saved. These are monochromatic values, not averaged-magnitude broadband MTF. The Fourier scale uses the common nominal 794.203 mm convention inherited from Run010; central thermal image scales are separately reported above. Exact field-dependent physical-frequency registration remains open.','',
    '| Candidate | Cold corner 550 nm MTF100 X/Y | EE2 actual / matched | 800 m cold / hot RMS, um | Extra cold / hot range-focus Z, mm |',
    '|---|---:|---:|---:|---:|']
    for cid,inter in zip(['B05-1','B05-2','B06'],interfaces):
        v=json.loads((O/(cid+'_verification.json')).read_text());r=next(r for r in v['rows'] if r['scenario']=='silica_low_frame' and r['temperature_C']==-25)
        d=next(d for d in r['diffraction'] if d['wavelength_um']==.55 and d['field'][0]!=0)
        a=d['actual'];cold=inter['finite_800m_at_cold_low_frame'];hot=inter['finite_800m_at_hot_low_frame']
        lines.append(f"| {cid} | {a['mtf_x'][1]:.3f}/{a['mtf_y'][1]:.3f} | {a['ee2']:.3f}/{d['matched']['ee2']:.3f} | {cold['metrics']['worst_rms_um']:.3f}/{hot['metrics']['worst_rms_um']:.3f} | {cold['extra_detector_z_mm']:+.4f}/{hot['extra_detector_z_mm']:+.4f} |")
    lines+=['','Finite-range checks use nine fields, six wavelengths and 576 pupil rays at 800 m, with two detector-only correction steps after thermal compensation. Range travel is additional to thermal travel and is not constrained by the earlier sensitivity caps. No actual actuator has been specified.','',
    'Cold-corner FFT sampling 112 to 160 changes any reported MTF/EE by at most '+f"{max(i['max_mtf_or_ee_sampling_change'] for i in interfaces):.5f}. B06 cold low-frame boundary envelope clearance is {interfaces[-1]['cold_boundary_clearance']['minimum_mirror_envelope_clearance_mm']:.3f} mm. Real cell/spider/window/body clearances remain open.",'',
    '## Verification, limitations and next action','',
    'Exact 20 C replay and analytic uniform geometric homology pass. Off-axis thermal correction pivots include displaced parent origins; the initial B06 checkpoint before that implementation correction is retained for audit. An infinitesimal pupil-boundary inset removes floating-point exact-edge classification; its preliminary checkpoint is also retained. These are model implementation corrections, not prescription changes or user optical interventions.','',
    'Thermal IQ is a trade variable without a customer threshold. EFL/IFOV and active-field mapping vary with temperature; exact registration compliance is not established by centered RMS. The hardware material and compensator choices, full tolerance allocation, thermal gradients, detector window and independent OpticStudio verification remain necessary. Low CTE may reduce focus/alignment burden but adds support/material/joint/metrology cost; homogeneous metal optics may simplify homology but add visible figure/roughness/coating risk. No monetary quotation, mass, complete envelope or throughput is inferred.','',
    'Next: finish the saved B09 verification and compare its measured-model evidence and cost drivers with the retained performance portfolio. Then define a concrete support/actuator/window interface before more performance-lane development. Track B remains open.','',
    'Resource accounting: zero shape attempts or iterative shape optimizers. Three matched scenario batches, three endpoint verification batches, one interface batch; two bounded implementation-check repeats. No broad search or stage plateau. Run012 budget was paused, not consumed by this separate study.']
    (O/'summary.md').write_text('\n'.join(lines)+'\n')
    for src in ['track_b_run013_thermal.py','track_b_run013_verify.py','track_b_run013_interfaces.py','track_b_run013_report.py']:shutil.copy2(M.ROOT/'src'/src,O/src)
    deps=['src/track_b_run010_sensitivity.py','src/track_b_run010_interfaces.py','runs/run_008/model.py','runs/run_008/configuration.json','runs/run_008/attempt_02/configuration.json','runs/run_009/model.py','runs/run_009/attempt_01.json']+[f'runs/run_010/{c}/jacobian.npz' for c in ['B05-1','B05-2','B06']]
    T.save('dependencies.json',{p:hashlib.sha256((M.ROOT/p).read_bytes()).hexdigest() for p in deps})
    meta=json.loads((O/'metadata.json').read_text(encoding='utf-8-sig'));meta.update(status='CLOSED',end_utc=datetime.now(timezone.utc).isoformat(),substantial_analysis_batches=7,implementation_check_repeats=2,shape_optimizer_count=0,shape_attempts=0,plateau=False,reference_accessed=False,decision='Retain all three; low-CTE support is preferred scenario, not hardware selection')
    T.save('metadata.json',meta)
    (O/'SHA256SUMS.txt').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(O).as_posix()}\n' for p in sorted(O.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts))
if __name__=='__main__':
    M=T.M
    main()
