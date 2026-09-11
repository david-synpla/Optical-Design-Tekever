# Current Design State

Track: C — complete simultaneous co-boresighted EO+SWIR payload engineering development
Stage: C0 COMPLETE; Stage C1 Run 016 closed the bounded C02 A6F1 feasibility gate, retained its common front conditionally, parked minimum doublet backends, and prioritizes C01 next
Authoritative requirements: `requirements/eo_swir_system_requirements.yaml`
Track A: FROZEN and immutable at `b06af2c3b6c3e7bec4e4bf5b57f9249207d8a875`; tag `track-a-frozen`; classified as autonomous EO-only work against the legacy baseline.
Track B: PRESERVED as research-informed EO-only engineering evidence against the legacy baseline; its former B09-only next action is superseded by Track C.
Contamination state: `reference/` remains unread. The known TEKEVER/team prescription is excluded until Track C's independent portfolio is mature and a later reveal is explicitly authorized.

## Active Track C architecture portfolio

| ID | System architecture | Lifecycle status | Main strength | Main C1 risk/gate |
|---|---|---|---|---|
| C01 | Separate integrated EO and SWIR telescopes | ACTIVE — practical reference/fallback; next C1 comparator, not overall leader | Natural channel pupils/EFLs, no splitter, strongest EO reuse | Fresh SWIR seed; widest front face; duplicated datums/focusers; boresight drift and 800 m parallax |
| C02 | Common coaxial reflective fore-telescope plus independent EO/SWIR relays | CONDITIONAL ACTIVE through C02-A6F1; direct form and two-element backends PARKED | Curved-field common front is near its matched obscured-pupil diffraction limit; common-LOS split needs no demonstrated dedicated relay | 313 mm f/1 annular primary, 26–29% geometric pupil loss and at least triplet-like flat-field cameras; compare C01 before more C02 work |
| C03 | Common off-axis afocal/TMA front end plus modular relays | ACTIVE — recommend C1 | Unobscured common LOS and modular high-performance potential | Highest conventional off-axis alignment/metrology/NRE; prove minimum-complexity seed and clearance |
| C04 | Cost/COTS-maximized dual-channel branch | ACTIVE — recommend C1 economic lane | Lowest procurement/NRE hypothesis; B09 process reuse | 300/305 mm donors miss exact SWIR f/6.2; verify >=311.371 mm clear donor, coatings, substrates and qualification economics |
| C05 | Compact folded/freeform shared architecture | PARKED after C0 | Distinct aggressive volume-compression hypothesis | Reopen only if C01-C04 packaging is unattractive or supplier evidence lowers freeform/metrology risk |

No Track C candidate has been frozen or selected. Run 016 used two bounded minimum-backend feasibility solves, not detailed candidate optimization; its physical doublets are parked. Run 014 package ranges and ordinal risk classes remain engineering hypotheses, not customer requirements, CAD results or quotations.

Persistent Track C governance: because this is a UAV payload, every substantive C-series run co-optimizes and reports optical performance together with largest aperture/optic, optical and folded length, bounding box/volume, major-optic mass proxy, large-optic count, shared/duplicated structure, mechanism count, structural/gimbal consequences and manufacturing/cost. SWaP is continuous Pareto evidence; no unsupplied hard mass or volume limit may be invented. C01 is the practical comparator/fallback, not the presumed overall leader.

## Latest Track C evidence — Run 014

EO/SWIR first-order EFL is 794.203/1930.502 mm; f/6.2 pupil diameter is 128.097/311.371 mm; thin-lens infinity-to-800 m focus shift is 0.789/4.670 mm. SWIR therefore drives front-aperture scale. Separate EO+SWIR collecting area is only 16.9% above a SWIR-sized common pupil; under the equal-technology collecting-primary solid-blank proxy it is only 7.0% above. Neither calculation is a payload-mass prediction, so common aperture is not presumed to win SWaP.

C01's minimum tangent-pupil baseline is 219.7 mm before margins, corresponding at 800 m to 274.7 urad of range-dependent parallax (79.6 EO or 53.0 SWIR pixels). Separate telescopes remain feasible but need an explicit calibration/stability model. C02/C03 reduce fore-optic LOS degrees of freedom but retain downstream relay registration sensitivity.

At the neutral 0.90 mirror-reflectance / 0.90 useful splitter-port sensitivity point, core two-mirror throughput is 0.810 without a splitter, 0.729 with one, and 0.656 for three mirrors plus splitter. These exclude relays, windows, glass, QE, obscuration, polarization and scatter. The touching 0.80 um bands still require an engineering transition/QE allocation; no perfect crossover is assumed.

C0 envelope hypotheses overlap and do not establish a volume winner. C05 has the lowest assumed range but not enough evidence to justify its specialist freeform/monolithic NRE now. C02 is the strongest assumed conventional common-aperture balance; C01 remains non-dominated for reuse, independent coatings/focus and no splitter; C03 preserves the unobscured high-performance lane; C04 remains the mandatory economic lane despite unresolved donor and qualification evidence.

Useful immutable B-series evidence: B05-1 is the balanced C01 EO subsystem reference, B05-2 the compact EO alternative, B06 the C03 clearance/alignment warning and unobscured evidence, and B09 the C04 donor/custom-corrector process and packaging/cost caution. No historical prescription or run was changed, and Track B thermal/performance numbers are not transferred to new Track C architectures.

Open Track C issues: fresh SWIR and shared-front prescriptions; real telephoto ratios/layouts; mass/CAD/gimbal models; detector windows; obscuration/vignetting/stray light; relative boresight and thermal drift; focus range/accuracy; mirror substrate/lightweighting/cells; coating/QE/polarization allocation; supplier evidence and cost at stated quantities. No customer hard threshold exists for mass, volume, optical performance, throughput, distortion, obscuration, stray light or pointing stability.

Run 014 resource use: zero optimizer/substantial-search calls, zero prescription attempts and no plateau; one deterministic analytic WSL Python execution (0.49 s), plus reporting/verification. `reference/` was not accessed.

## Latest C02 evidence — Run 015

The directly power-bearing common Cassegrain is strongly coupled by the 2.43x channel pupil ratio. A conventional f/2.4, 200 mm-backfocus seed needs a 117.54 mm secondary and retains only 16.7% of the EO pupil area (15.6% in the denser replay), versus 85.4% SWIR. Moving the EO stop downstream images it at paraxial coordinates 2.75–8.96 m and produces 57.5–90.7 mm real entrance-plane pupil walk without improving survival. The EO channel cannot be treated as a harmless concentric stop inside the SWIR-sized telescope.

Faster direct seeds expose the trade rather than solve it: f/1.5 with 75 mm backfocus retains 64.6% EO / 93.8% SWIR but has 34.29/20.29 um worst shared-front EO/SWIR RMS; f/1 with 50 mm backfocus retains 81.3%/95.8% but worsens to 69.84/38.68 um. These RMS values precede the EO reducer and both final backends and are not acceptance scores. C02-D is PARKED before shape optimization.

The coaxial afocal sweep also shows coupling: compression shrinks the secondary but magnifies the EO backend field and forces primary-hole/pupil-walk growth. At f/2, 8x and 10x compression vignette the EO corner completely. The only conditional non-dominated pocket is C02-A6F1: two-paraboloid 6x compression with a 313.50 mm f/1 primary, 259.48 mm mirror separation, 56.25 mm secondary and 69.58 mm primary hole. It retains 70.8% EO and 73.3% SWIR minimum pupil area (70.8%/73.5% dense replay) and provides a truly collimated split, but leaves backend targets of 132.37 mm EFL/21.35 mm pupil/3.01 degree EO half-field and 321.75 mm/51.90 mm/1.46 degree SWIR half-field. The paraxial stop image lies near 12.96 m; a compact stable real pupil relay is unproved.

Run 015 used four substantial bounded model batches, two materially distinct physical experiments, zero optimizer calls and no plateau. `reference/` remained unread and historical runs were unchanged.

Next recommended action, only after new instruction: one bounded C02-A6F1 backend/manufacturing feasibility run with minimum-powered EO/SWIR cameras, a real pupil relay and dichroic plane, full-field stop images/vignetting, and an f/1 primary/hole fabrication and structure assessment. Park C02 as a family and prioritize C01 if that gate loses the current pupil survival or requires unattractive backend optics. C03 and C04 remain active for later separate C1 runs; C05 remains parked.

## Latest C02 evidence — Run 016

Perfect paraxial cameras isolate the A6F1 common front. On flat detector planes its corner RMS radius is 21.319 um EO and 28.196 um SWIR, but individual corner refocus of -0.400/-0.533 mm collapses this to 0.277/0.420 um. Forward split-pupil OPD confirms the mechanism: 0.656/0.331 waves RMS at the flat EO-550 nm/SWIR-1.2 um references becomes 0.0278/0.00325 waves after radial quadratic removal. Best-curved-focus MTF is close to the same traced obscured-pupil limit. The inferred focal-surface radius is about 60.5/63.0 mm. A6F1 is therefore not rejected for structural off-axis coma/astigmatism; backend field flattening is the real gate.

The actual split pupils remain field dependent. Maximum centroid walk is 1.484 mm EO and 4.223 mm SWIR; maximum RMS-ellipse axis ratio is 1.212/1.177. Minimum full-field geometric survival is 70.83/73.31%. A physical camera can sit directly at the collimated split without additional pupil loss, so a dedicated pupil relay is not yet mandatory despite the approximately 12.96 m paraxial stop image.

One air-spaced spherical doublet per channel was the minimum physical backend test. It reached 793.778/1930.489 mm EFL, f/6.1967/f/6.2000 and 70.0%/73.13% minimum survival, but retained 33.93/37.47 um worst three-wave, nine-field RMS radius. Both doublets are PARKED after 27/43 evaluations; no rescue attempts were spent. Any return to C02 should add one justified field-flattening/achromatization degree of freedom rather than repeat doublet optimization.

The f/1 primary is feasible in principle but materially burdensome as implemented: 313.50 mm clear diameter, 19.73 mm edge sag, 14.13 degree edge slope, 69.58 mm central hole and 121.96 mm radial annular clear width. Blank/hole process, annular support/print-through, full-aperture null or sub-aperture metrology, broadband coating, dichroic, spider, thermal focus and tolerances remain unproved; no mass, cost or yield claim is made.

Run 016's explicit SWaP proxies prevent the optical result from being treated as a win by itself. The straight sequential lower-bound envelope is about 313.5 x 313.5 x 645.0 mm (63.39 L) before cells, baffles, dichroic branch clearance, electronics and gimbal margin. Under the unchanged Run 014 solid-blank proxy (thickness/diameter 0.10, density 2.2 g/cm3), the annular primary plus secondary are about 5.09 kg; this is not payload mass and may change materially with substrate/support/lightweighting. The current model has one optic over 100 mm, a 56.25 mm secondary, approximately 62.3 mm SWIR camera elements and approximately 27.6 mm EO camera elements, one splitter and two focus mechanisms. A folded dichroic layout is needed to reduce the roughly 645 mm inertia arm, and its bounding box has not been proved.

Run 016 used four substantial bounded batches, two optimization attempts totaling 70 evaluations, no plateau and about 109.44 s recorded model-kernel wall time plus imports/reporting. `reference/` remained unread and historical runs were unchanged. The authoritative diffraction result is `runs/run_016/diffraction_audit.json`; it supersedes preliminary downstream-stop FFT entries retained inside `metrics.json`/`convergence.json` for audit history.

Next recommended action, only after new instruction: execute the bounded C01 C1 investigation using preserved B05 EO evidence and a fresh independent SWIR seed, with co-boresight/parallax, package and focus/thermal interfaces. This supplies the low-coupling comparator before deciding whether C02's common LOS justifies triplet-like channel backends and the f/1 annular primary. C03 and C04 remain active later branches; C05 remains parked.

## Preserved historical Track B EO portfolio

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

## Historical Track B resource state

Run 010 closed in 19.8 minutes elapsed including coding/reporting/tooling. Zero iterative optimizer calls, zero shape/architecture attempts; nine substantial analysis batches plus diagnostic checks. Exact nominal replay, rigid-body invariants, selected diffraction convergence, data ranges and Track A freeze hashes pass. No quota interruption or human optical correction occurred in this run.

Run 013 completed the prioritized matched thermal comparison without changing nominal shapes. Silica-like mirrors and a 1.2 ppm/K effective frame retain dense endpoint RMS of 0.799–0.801 / 0.544–0.627 / 1.337–1.383 um for B05-1 / B05-2 / B06. Thermal focus travel is about 0.04 / 0.05 / 0.09 mm maximum. A 24 ppm/K frame needs up to 1.37 / 1.76 / 3.23 mm and retains more aberration even after compensation. These are material scenarios, not selected hardware or qualification. Cold/hot 800 m checks require roughly 0.8 mm additional range-focus travel. See runs/run_013/summary.md for diffraction, image scale, finite-range and limitation details.

Run012 verification is complete. B09 reaches 794.202541 mm paraxial EFL and f/6.199997, with 7.972 um dense full-band RMS and 7.897 um at 800 m after 0.8123 mm refocus. At the nominal 550 nm positive corner, MTF100 is 0.053/0.072 and EE2 is 0.225 versus a 0.590 matched-pupil limit. Its lower performance is preserved as an explicit trade for stock mirrors and simpler custom spherical optics, not rejected against an invented IQ threshold. Current optical cost/NRE/qualification comparisons are in runs/run_012/summary.md.

B09 remains provisional: corner centroids overrun the fixed active rectangle by 10.47/7.67 um; the 0.485 mm lens edge gap misses a soft assembly target; stock substrate/coatings, thermal behavior, real cells/window and production economics are unverified. Its initial backward-path wavefront model and incorrect fold helper were corrected without changing powered shapes or separations. Use runs/run_012/verified_model.py; original model.py and before_opl_correction/ preserve audit history and must not supply diffraction scores.

Former Track B next action, now superseded by Track C initialization: define a common detector/window, range-plus-thermal focus and mechanical datum interface, then perform a bounded B09 thermal/support check and prepare common-quantity supplier RFQ specifications. This is retained as EO evidence and possible Track C input, not as the active project action.

User supplied the detailed Run 010 investigation scope and standing authorization to push completed work in this repository. Earlier milestones and exact lineage remain in runs/run_008, runs/run_009 and their committed metadata.

## Permanent cost-conscious lane and freeze gate

User instruction 2026-09-07 adds a permanent economic/COTS lane. Run 011 selects B09 for immediate independent hybrid development in Run 012; B01/B03 remain the empirical stock-SCT fallback. Current retail anchors and limitations are in runs/run_011/summary.md. B05/B06 thermal/material work remains necessary and receives its own budget. No low-cost route is rejected merely for lower nominal optical performance.

Priority correction: Run012 paused after its in-flight solve so Run013 thermal work proceeded before further cost-lane development. Thermal work has now completed its bounded scope. B01/B02/B03 full-band image quality is presently unverified because proprietary prescriptions or measurements are unavailable; it is not scored as poor predicted performance. Their disclosed EFL/aperture mismatches are separate geometric evidence.

Track B cannot freeze solely on performance-lane maturity. Retain a credibly evaluated lower-cost option or demonstrate why the investigated lower-cost routes offer no acceptable performance/cost trade. Produce a measured/modelled performance-versus-NRE/recurring-cost/risk portfolio, with no fabricated monetary quotations. This gate is also in DESIGN_WORKFLOW.md.

Recovery note: Run 010 numerical work was complete; its commit was interrupted by the approval service credit limit. Hashes passed and commit 110ee1c was pushed on resumption without repeating analyses. Run 011 is a separate scope, not an extension of the Run 010 budget.
