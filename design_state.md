# Current Design State

Track: B — independent research-informed optical design
Stage: Runs 012 (B09 hybrid) and 013 (matched thermal/material study) CLOSED; performance/cost portfolio retained
Workflow: v3; Track B remains OPEN, not frozen.
Track A: FROZEN at b06af2c3b6c3e7bec4e4bf5b57f9249207d8a875; tag track-a-frozen. Its results remain immutable. reference/ remains unread.

## Portfolio

| ID / variant | Architecture | Status | Current engineering decision |
|---|---|---|---|
| B01 | C5 + stock reducer | ACTIVE comparator | Run 005; exact geometry mismatch, band/thermal behavior unmeasured |
| B02 | Nikon 800/6.3 | ACTIVE comparator | Run 005; EFL/f-number mismatch, detector interface and qualification outstanding |
| B03 | Retained SCT optics/custom mechanics | ACTIVE comparator | Integration trade; does not itself fix B01 optical geometry |
| B04 | Spherical-secondary CDK + two-lens corrector | PARKED | Run 007; simpler-secondary comparator, 7.445 um sampled RMS |
| B05 attempt 1 | Corrected two-conic Cassegrain | ACTIVE — provisional lower-risk baseline | Run 010: focus alone restores all 24 diagnostic specimens to <=1.063 um sampled RMS; smaller secondary-shape and image-scale burden |
| B05 attempt 2 | Compact corrected Cassegrain variant | ACTIVE — compact alternative | ~45.7 mm shorter than attempt 1; retains useful trade despite greater secondary fabrication, focus recovery and image-scale sensitivity |
| B06 | Unobscured off-axis three-conic TMA | ACTIVE — higher alignment/metrology burden | Focus alone inadequate in Run 010; focus plus secondary X/Y tilt retains mid-frequency/EE advantage, with residual figure and registration risks |
| B09 | Stock Newtonian mirrors + custom small corrector/extender | ACTIVE — provisional economical hybrid | Run012: 7.972 um dense RMS; two stock-nominal mirrors and two custom spherical lenses; lower corner MTF/EE, production savings unverified |
| B07–B08, B10–B14 | Other screened architecture families | PARKED | Run 005 reopening reasons remain authoritative; no blanket family rejection |

## Latest matched evidence

Run 010 uses exact Run 008/009 prescriptions, no nominal shape changes. Nine signed fields, six equally weighted wavelengths across 430–800 nm and common equal-area physical-pupil coordinates; dense checks use 25 fields and 576 pupil samples. Detailed results and assumptions: runs/run_010/summary.md.

| Metric | B05 attempt 1 | B05 attempt 2 | B06 |
|---|---:|---:|---:|
| Dense common nominal RMS, um | 0.800 | 0.576 | 1.360 |
| Largest RMS in 24 exploratory coupled-error cases, um | 13.097 | 17.005 | 19.004 |
| Largest after detector focus alone, um | 1.063 | 1.335 | 7.477 |
| Largest after focus + secondary X/Y tilt, dense stress specimen, um | 1.000 | 1.084 | 2.552 |
| Compensated stress-specimen 550 nm corner MTF X/Y at 100 lp/mm | 0.230/0.231 | 0.236/0.236 | 0.481/0.435 |
| Corresponding 2x2-pixel EE / matched ideal | 0.406/0.411 | 0.408/0.411 | 0.650/0.791 |

B06's advantage is frequency-dependent: in the same specimen its 550 nm Nyquist MTF is lower than B05, and at 800 nm B05 also exceeds it at 150 lp/mm. Preserve the trade rather than picking a nominal RMS or Nyquist winner. The 24-case uniform diagnostic ensemble is not supplier capability or predicted production yield. No production tolerance allocation exists.

## Engineering limits that affect the decision

The selected three-control policy remains within the diagnostic +/-0.5 mm focus and +/-1 mrad tilt caps. B06 needs up to 0.872 mrad secondary tilt versus 0.341/0.385 mrad for B05. Other tested axial/control combinations are correlated or saturate; they are not additional free rescue knobs. Practical measurement/actuator accuracy and locking remain unmodeled.

Centred RMS does not enforce detector registration. Largest compensated centroid displacement is 71.6/80.7/185.4 um; image scales also change. Original angular-field coverage on the fixed active detector needs explicit allocation. No pointing/distortion/image-quality tolerance was supplied.

B06 retains ~6.00 mm boundary clearance in its compensated stress specimen. B05's frozen entrance-annulus approximation omits a small additional secondary shadow: direct intersection gives up to 0.0208%/0.0149% of annular area for the compensated B05 variants. Historical runs were not rewritten. Real secondary substrate/spider/cell geometry, primary cell, detector package and baffles remain unresolved; interior pupil survival alone is not a complete physical-clearance test.

No actual detector-window specification was supplied. Hypothetical 0.5/1 mm N-BK7 windows were tested separately; a 1 mm window needs ~0.34–0.35 mm additional detector refocus. These are parameterized interface scenarios, not Sony specifications or nominal design additions.

Run 013 now provides matched uniform-temperature/material scenarios over -25 to +50 C. Hardware qualification remains open: actual coating/substrate/structure choices, gradients and stress, field registration, stray light, surface figure, measurement noise and independent OpticStudio validation. Source/QE-weighted broadband PSF/MTF remains open. Mass, housing dimensions, throughput and monetary cost are not established.

## Resource state and next action

Run 010 closed in 19.8 minutes elapsed including coding/reporting/tooling. Zero iterative optimizer calls, zero shape/architecture attempts; nine substantial analysis batches plus diagnostic checks. Exact nominal replay, rigid-body invariants, selected diffraction convergence, data ranges and Track A freeze hashes pass. No quota interruption or human optical correction occurred in this run.

Run 013 completed the prioritized matched thermal comparison without changing nominal shapes. Silica-like mirrors and a 1.2 ppm/K effective frame retain dense endpoint RMS of 0.799–0.801 / 0.544–0.627 / 1.337–1.383 um for B05-1 / B05-2 / B06. Thermal focus travel is about 0.04 / 0.05 / 0.09 mm maximum. A 24 ppm/K frame needs up to 1.37 / 1.76 / 3.23 mm and retains more aberration even after compensation. These are material scenarios, not selected hardware or qualification. Cold/hot 800 m checks require roughly 0.8 mm additional range-focus travel. See runs/run_013/summary.md for diffraction, image scale, finite-range and limitation details.

Run012 verification is complete. B09 reaches 794.202541 mm paraxial EFL and f/6.199997, with 7.972 um dense full-band RMS and 7.897 um at 800 m after 0.8123 mm refocus. At the nominal 550 nm positive corner, MTF100 is 0.053/0.072 and EE2 is 0.225 versus a 0.590 matched-pupil limit. Its lower performance is preserved as an explicit trade for stock mirrors and simpler custom spherical optics, not rejected against an invented IQ threshold. Current optical cost/NRE/qualification comparisons are in runs/run_012/summary.md.

B09 remains provisional: corner centroids overrun the fixed active rectangle by 10.47/7.67 um; the 0.485 mm lens edge gap misses a soft assembly target; stock substrate/coatings, thermal behavior, real cells/window and production economics are unverified. Its initial backward-path wavefront model and incorrect fold helper were corrected without changing powered shapes or separations. Use runs/run_012/verified_model.py; original model.py and before_opl_correction/ preserve audit history and must not supply diffraction scores.

Next: define a common detector/window, range-plus-thermal focus and mechanical datum interface, then perform a bounded B09 thermal/support check. Prepare common-quantity supplier RFQ specifications to replace qualitative economic classes. Do not start another nominal shape search or freeze Track B from the current evidence alone.

User supplied the detailed Run 010 investigation scope and standing authorization to push completed work in this repository. Earlier milestones and exact lineage remain in runs/run_008, runs/run_009 and their committed metadata.

## Permanent cost-conscious lane and freeze gate

User instruction 2026-09-07 adds a permanent economic/COTS lane. Run 011 selects B09 for immediate independent hybrid development in Run 012; B01/B03 remain the empirical stock-SCT fallback. Current retail anchors and limitations are in runs/run_011/summary.md. B05/B06 thermal/material work remains necessary and receives its own budget. No low-cost route is rejected merely for lower nominal optical performance.

Priority correction: Run012 paused after its in-flight solve so Run013 thermal work proceeded before further cost-lane development. Thermal work has now completed its bounded scope. B01/B02/B03 full-band image quality is presently unverified because proprietary prescriptions or measurements are unavailable; it is not scored as poor predicted performance. Their disclosed EFL/aperture mismatches are separate geometric evidence.

Track B cannot freeze solely on performance-lane maturity. Retain a credibly evaluated lower-cost option or demonstrate why the investigated lower-cost routes offer no acceptable performance/cost trade. Produce a measured/modelled performance-versus-NRE/recurring-cost/risk portfolio, with no fabricated monetary quotations. This gate is also in DESIGN_WORKFLOW.md.

Recovery note: Run 010 numerical work was complete; its commit was interrupted by the approval service credit limit. Hashes passed and commit 110ee1c was pushed on resumption without repeating analyses. Run 011 is a separate scope, not an extension of the Run 010 budget.
