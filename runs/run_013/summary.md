# Run 013 — matched thermal/material comparison

Decision: retain B05-1, B05-2 and B06. Prefer an effective low-CTE support concept for the next performance-lane engineering stage. This is a uniform-temperature scenario study, not thermal qualification or a material procurement selection. Nominal shapes are unchanged.

The user explicitly prioritized this study over further B09 development. Run012 paused after its in-flight solve; its verification resumes only after this study closes. Lack of a proprietary COTS prescription remains unverified performance, never an assumed low score.

## Material and modelling assumptions

- Nominal 20 C, sampled -25, -10, 20, 35, 50 C; uniform equilibrium, fixed 1 atm air-relative glass indices. Six equal-weight wavelengths 430–800 nm; nine signed fields, 64 equal-area pupil rays. Endpoint validation uses 25 fields and 576 pupil samples.
- Mirror CTE 0.52 ppm/K is a constant fused-silica-like approximation; Corning reports that mean near room temperature, not a certified constant over this entire range. Frame effective CTE 1.2 and 24 ppm/K are engineering cases, not selected structures. A homogeneous 24 ppm/K mirror/frame case is an ideal homology bound, not proof that an aluminium visible-light mirror meets figure, coating or metrology needs.
- N-BK7/N-F2 use 7.1/7.8 ppm/K glass expansion and the installed SCHOTT catalog thermo-optic coefficients; catalog hashes and computed indices are in glass_provenance.json. Lenses expand about their mechanical centers; mirror patch centers follow the frame while parent curvature/off-axis coordinates expand with the substrate. Conics remain fixed.
- Source entrance stop expands with the frame. Its B05 annulus remains the previously disclosed shadow approximation. Real mounts, gradients, stress, thermal lag, detector pixel-pitch expansion, pressure/altitude changes, coating deformation and the unspecified detector window are excluded. Those exclusions prevent a claim of compliance across the operating envelope.

Primary sources: [SCHOTT N-BK7](https://media.schott.com/api/public/content/41e799d0bf874807a0bb8e702fbb75b5?v=54856406), [SCHOTT N-F2](https://media.schott.com/api/public/content/061f3156c83a44ed9220770b0f65a869?v=d69b35e0), [Corning HPFS](https://www.corning.com/media/worldwide/csm/documents/1e624b3034474193b5b00ea6f558dd3d2.pdf), [thyssenkrupp 6005 expansion example](https://www.thyssenkrupp-materials.co.uk/aluminium-6005.html/index.html). Values inform scenarios; no hardware is ordered.

## Matched endpoint results

The Run010 diagnostic caps remain +/-0.5 mm detector Z and +/-1 mrad secondary tilt. High-frame mismatch saturates focus. A separately labelled +/-5 mm travel diagnostic uses two local linear correction steps, no shape optimization. It distinguishes actuator travel from residual aberration. Travel is signed global detector Z, not a common optical-axis sign.

| Case / candidate | Cold / hot dense RMS, um | Cold / hot detector Z, mm | Central image-scale range, mm |
|---|---:|---:|---:|
| silica_high_frame / B05-1 | 1.245 / 0.840 | +1.3746 / -0.9135 | 792.980–795.980 |
| silica_low_frame / B05-1 | 0.799 / 0.801 | +0.0385 / -0.0256 | 794.155–794.210 |
| homogeneous_high_CTE / B05-1 | 0.797 / 0.802 | +0.0051 / -0.0034 | 793.371–794.714 |
| silica_high_frame / B05-2 | 3.108 / 1.522 | +1.7578 / -1.1509 | 788.259–803.208 |
| silica_low_frame / B05-2 | 0.627 / 0.544 | +0.0491 / -0.0327 | 794.013–794.406 |
| homogeneous_high_CTE / B05-2 | 0.567 / 0.584 | +0.0044 / -0.0029 | 793.377–794.699 |
| silica_high_frame / B06 | 5.151 / 3.832 | -3.2318 / +2.0937 | 783.403–810.960 |
| silica_low_frame / B06 | 1.337 / 1.383 | -0.0920 / +0.0613 | 793.854–794.669 |
| homogeneous_high_CTE / B06 | 1.359 / 1.361 | -0.0000 / +0.0000 | 793.295–794.783 |

Low-frame cases preserve near-nominal performance with modest thermal travel. B05-1 is less sensitive than the compact B05-2 to high-frame mismatch; B06 needs both more travel and off-axis compensation. The ideal homogeneous case suppresses first-order mismatch but carries unquantified visible-mirror manufacturing risk. No universal winner follows.

## Diffraction and range checks

Endpoint low-frame PSFs compare actual versus the same transmitted-pupil diffraction limit at 430, 550 and 800 nm, center and corner; 50/100/150/182.482 lp/mm and 2x2-pixel EE are saved. These are monochromatic values, not averaged-magnitude broadband MTF. The Fourier scale uses the common nominal 794.203 mm convention inherited from Run010; central thermal image scales are separately reported above. Exact field-dependent physical-frequency registration remains open.

| Candidate | Cold corner 550 nm MTF100 X/Y | EE2 actual / matched | 800 m cold / hot RMS, um | Extra cold / hot range-focus Z, mm |
|---|---:|---:|---:|---:|
| B05-1 | 0.233/0.233 | 0.407/0.411 | 1.023/1.023 | +0.7901/+0.7900 |
| B05-2 | 0.237/0.237 | 0.411/0.411 | 1.750/1.664 | +0.7957/+0.7949 |
| B06 | 0.563/0.538 | 0.757/0.791 | 1.837/1.766 | -0.7734/-0.7719 |

Finite-range checks use nine fields, six wavelengths and 576 pupil rays at 800 m, with two detector-only correction steps after thermal compensation. Range travel is additional to thermal travel and is not constrained by the earlier sensitivity caps. No actual actuator has been specified.

Cold-corner FFT sampling 112 to 160 changes any reported MTF/EE by at most 0.00206. B06 cold low-frame boundary envelope clearance is 6.033 mm. Real cell/spider/window/body clearances remain open.

## Verification, limitations and next action

Exact 20 C replay and analytic uniform geometric homology pass. Off-axis thermal correction pivots include displaced parent origins; the initial B06 checkpoint before that implementation correction is retained for audit. An infinitesimal pupil-boundary inset removes floating-point exact-edge classification; its preliminary checkpoint is also retained. These are model implementation corrections, not prescription changes or user optical interventions.

Thermal IQ is a trade variable without a customer threshold. EFL/IFOV and active-field mapping vary with temperature; exact registration compliance is not established by centered RMS. The hardware material and compensator choices, full tolerance allocation, thermal gradients, detector window and independent OpticStudio verification remain necessary. Low CTE may reduce focus/alignment burden but adds support/material/joint/metrology cost; homogeneous metal optics may simplify homology but add visible figure/roughness/coating risk. No monetary quotation, mass, complete envelope or throughput is inferred.

Next: finish the saved B09 verification and compare its measured-model evidence and cost drivers with the retained performance portfolio. Then define a concrete support/actuator/window interface before more performance-lane development. Track B remains open.

Resource accounting: zero shape attempts or iterative shape optimizers. Three matched scenario batches, three endpoint verification batches, one interface batch; two bounded implementation-check repeats. No broad search or stage plateau. Run012 budget was paused, not consumed by this separate study.
