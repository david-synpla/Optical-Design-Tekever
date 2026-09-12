# Current Design State

Track: C — complete simultaneous co-boresighted EO+SWIR payload engineering development
Stage: C0 COMPLETE; Stage C1 Run 019 parks the screened minimum-complexity C03 lane and prioritizes the bounded C04 economic/COTS investigation next
Authoritative requirements: `requirements/eo_swir_system_requirements.yaml`
Track A: FROZEN and immutable at `b06af2c3b6c3e7bec4e4bf5b57f9249207d8a875`; tag `track-a-frozen`; classified as autonomous EO-only work against the legacy baseline.
Track B: PRESERVED as research-informed EO-only engineering evidence against the legacy baseline; its former B09-only next action is superseded by Track C.
Contamination state: `reference/` remains unread. The known TEKEVER/team prescription is excluded until Track C's independent portfolio is mature and a later reveal is explicitly authorized.

## Active Track C architecture portfolio

| ID | System architecture | Lifecycle status | Main strength | Main C1 risk/gate |
|---|---|---|---|---|
| C01 | Separate optics on an integrated common bench/shell | ACTIVE — non-dominated; B05-1/S16 preferred C01 UAV comparator, S20 performance and S14 stretch retained | Proven B05 EO reuse, compact shared structure, 90–95% traced SWIR pupil survival, no splitter/complex SWIR camera | 470 mm screened front span, two large optics, two focusers and relative-boresight calibration; real CAD/thermal structure absent |
| C02 | Common coaxial reflective fore-telescope plus independent EO/SWIR relays | CONDITIONAL ACTIVE through C02-A6F1; direct form and two-element backends PARKED | Curved-field common front is near its matched obscured-pupil diffraction limit; one frontal aperture/common LOS | 313 mm f/1 annular primary, 26–29% geometric pupil loss and at least triplet-like flat-field cameras; defer more backend work until broader comparison |
| C03 | Common off-axis afocal/TMA front end plus modular relays | PARKED after bounded C1; reopen only with a justified three-power derivative plus strict package allocation or new fabrication evidence | Unobscured common LOS, 100% modeled geometric survival and modular relay potential | Screened conic forms trade 76.8–141.4 L package against 43.7–13.8 um SWIR ideal-camera RMS; 0.79–0.89 m parent-axis metrology envelope and small cell gaps |
| C04 | Cost/COTS-maximized dual-channel branch | ACTIVE — recommend C1 economic lane | Lowest procurement/NRE hypothesis; B09 process reuse | 300/305 mm donors miss exact SWIR f/6.2; verify >=311.371 mm clear donor, coatings, substrates and qualification economics |
| C05 | Compact folded/freeform shared architecture | PARKED after C0 | Distinct aggressive volume-compression hypothesis | Reopen only if C01-C04 packaging is unattractive or supplier evidence lowers freeform/metrology risk |

No Track C candidate has been frozen or selected. Run 019 is a bounded architecture experiment, not detailed prescription/tolerance optimization or CAD; its package, mass, sensitivity and parent-envelope numbers are continuous engineering proxies. Run 016's physical C02 doublets remain parked. Run 014 package ranges and ordinal risk classes remain engineering hypotheses, not customer requirements, CAD results or quotations.

Persistent Track C governance: because this is a UAV payload, every substantive C-series run co-optimizes and reports optical performance together with largest aperture/optic, optical and folded length, bounding box/volume, major-optic mass proxy, large-optic count, shared/duplicated structure, mechanism count, structural/gimbal consequences and manufacturing/cost. SWaP is continuous Pareto evidence; no unsupplied hard mass or volume limit may be invented. C01 is the practical comparator/fallback, not the presumed overall leader.

## Latest C03 sensitivity-aware architecture evidence — Run 019

Run 019 tested the minimum-complexity unobscured C03 form: a two-confocal-conic common afocal front, dichroic, ideal EO/SWIR cameras and one passive branch fold. Four 4x/6x/8x geometries varied primary speed, mirror spacing and off-axis magnitude. Representative +/-10 um X/Y decenter and +/-100 urad X/Y tilt response was evaluated from the initial screen without compensation; one final conic/focus solve combined nominal and perturbation residuals rather than optimizing nominal image quality first. No freeform was introduced.

All final points retain 100% modeled full-field geometric pupil survival and positive 2.46–3.65 mm circle clearance before cells/baffles. The compact A8 point is about 494 x 429 x 362 mm (76.8 L) but has 77.86/43.67 um EO/SWIR worst RMS radius even with ideal cameras. The best-nominal refined A4 point is 18.70/13.75 um but expands to about 852 x 448 x 370 mm (141.4 L). The slow/wider-spaced A6 reduces EO/SWIR composite perturbation response to 57.8%/57.5% of compact A6, qualitatively confirming that spacing/off-axis geometry must be traded early, but costs 35.7% package volume and reaches 124.3 L. The literature's approximately 60% example is guidance, not a transferred target.

The sensitivity-aware A4 solve improves nominal EO/SWIR RMS by 31.5%/11.1% but improves the perturbation response by only 0.41%/0.45%; final conics remain near paraboloids. Nominal surface refinement therefore does not rescue the architecture, and freeforms are not justified on present evidence. Dense 24x72 pupil replays of the compact and best-nominal endpoints reproduce RMS within 0.001% and retain 100% survival.

The illuminated aperture is 311.37 mm and the physical primary segment is 315.37 mm, but the parent-axis figure/metrology envelope is approximately 789–893 mm. Common primary-plus-secondary solid proxies are 5.44–5.53 kg; full-parent-disk values are explicitly an upper fabrication branch, not assumed procurement. Compact points still need three optics over 100 mm once the tilted dichroic/fold are counted; slower/lower-compression points need five. Two focus mechanisms and independent cameras remain. The neutral two-mirror-plus-splitter path coefficient is 0.729 before cameras/windows/QE: better than C02 after obscuration, but below a comparable no-splitter two-mirror path.

Pareto consequence: no screened C03 point combines C01 B05-1/S16's 68.2 L complete-channel practicality and optical maturity or C02's approximately 79.7 L same-allowance common-front economy with acceptable nominal image, sensitivity and off-axis fabrication burden. C03 is PARKED after bounded C1. A true three-powered-element/TMA derivative may be reconsidered only with a strict package allocation or new manufacturing evidence; it is not the next development task.

Run 019 used four geometry points and one authoritative joint sensitivity-aware solve (five evaluations). Two pre-closure aperture-sizing corrections replayed the solve, giving three optimizer invocations and fifteen evaluations total, plus three no-optimizer probes and two dense replays. Observed WSL process time was approximately 145 s plus deterministic reporting/integrity work. No dependency was installed and no plateau occurred. `reference/` remained unread and historical evidence was unchanged.

Next recommended action, only after new instruction: execute the bounded C04 cost/COTS-maximized C1 economic lane. Do not begin C03 freeform/TMA escalation, detailed tolerancing or production design without new instruction.

## Latest C01 system-integration evidence — Run 018

Run 018 replaces the unnecessarily punitive picture of two complete cylindrical housings with a shared twin-lobe shell, common gimbal/thermal bench and rear detector/focus datum. With the Run 017 S16 SWIR seed, axial B05 staggering and only a 36.85 mm SWIR converging-return fold, the screened box is about 470 x 325 x 446 mm (68.2 L), 13.2% below the Run 017 separate-tube screen. The corresponding S20 performance point is 470 x 325 x 522 mm (79.8 L).

B05-1 and B05-2 were compared at system level. B05-2 is 45.67 mm shorter and nominally sharper, but the SWIR path sets every shared-shell bounding box: B05-2 changes neither front face nor volume. For the S16 combination it reduces the structural-area proxy by only 1.67% and the four-mirror point-inertia proxy by 4.95%, while retaining its known tighter/higher-departure secondary, larger focus-recovery residual and greater high-frame thermal travel. B05-1 is therefore the preferred C01 EO baseline on numerical system evidence, not assumption. B05-2 remains conditionally active if real detector/electronics packaging exploits its shorter train.

One new bounded SWIR compact seed, S14_B50, varies only two conics and focus. It preserves 1930.502 mm EFL/f/6.2, gives 11.48 um worst RMS, 95% dense and 95.1% exact circular-obscuration transmission, and enables a 470 x 325 x 402 mm (61.5 L) screen. Its f/1.4 primary has 10.18 degree edge slope and 118.4 um vertex-sphere departure, versus S16's 8.93 degree/80.2 um; S14 is retained as a compact stretch, not preferred over S16. No catadioptric corrector was added because it would add optical/manufacturing degrees of freedom without shortening the dominant two-mirror separation unless a genuinely new architecture were solved.

The shared-shell front axes are 237.19 mm apart. At 800 m this gives 296.5 urad displacement (85.9 EO or 57.2 SWIR pixels), but the planar scene-overlap result is benign: the full 5.304 x 4.243 m SWIR field remains inside the 11.305 x 8.280 m EO field. The simultaneous intersection is 100% of SWIR and 24.0% of EO. Full SWIR containment persists down to about 63 m for a horizontal baseline or 94 m for a vertical one. Parallax is therefore principally a registration/range-calibration issue at the required distance, not loss of SWIR common-scene coverage; terrain, range error, distortion and boresight drift remain open.

The preferred B05-1/S16 solid mirror-blank proxy is 5.74 kg versus C02's 5.09 kg. A scalable open-saddle/common-bench structural-area proxy is 0.455–0.602 m2; at the illustrative 5 kg/m2 coefficient it is 2.27–3.01 kg, not flight-structure mass. The uniform-box vertical-axis specific-inertia proxy is 0.03498 m2 for S16 C01 versus 0.05033 m2 for C02 under the same simple external allowances, while optical-axis specific inertia is worse for wide C01 at 0.02726 versus 0.01898 m2. C01's mirror-area proxy CG is about 30 mm toward SWIR and 122 mm aft of box center; real detectors, electronics, cells and gimbal placement can change it.

Applying common simple external allowances to the Run 016 straight C02 lower bound gives about 337 x 337 x 700 mm (79.7 L) before its unproved dichroic branches. Integrated C01 S20 is essentially equal in screened volume, while S16 is smaller and shorter but wider. C01 leads current complete-channel feasibility, transmission, independent coating, reuse, optical simplicity and axial inertia; C02 leads frontal width, common LOS, large-optic count and solid mirror proxy. Neither dominates.

Run 018 status: B05-1/S16 is the preferred C01 system comparator; B05-1/S20 and B05-1/S14 preserve performance and compact-stretch objectives; B05-2 stays conditional. C02-A6F1 remains conditional active. One new optical hypothesis used five authoritative evaluations; including two debug replays, total use was three optimizer invocations, fifteen evaluations and approximately 59.6 s observed WSL process time plus reporting/verification. No plateau occurred. `reference/` remained unread and historical runs were unchanged.

Next recommended action, only after new instruction: execute one bounded C03 unobscured common-aperture C1 screen with package, clearance, mirror mass, gimbal inertia and off-axis metrology active from the first solve. Preserve C04 as the following mandatory economic lane. Do not begin detailed C01 tolerance/CAD development or resume C02 backends without new instruction.

## Latest C01 evidence — Run 017

The unchanged Run 008 B05-1 model/configuration was replayed as EO evidence: 794.203 mm EFL, f/6.2 and 0.799 um worst sampled RMS radius, consistent with Run 010's 0.800 um dense result. No B-series prescription or run changed. Its previous thermal/focus scenarios remain evidence rather than transferred requirements.

Three fresh independent SWIR Cassegrains preserve 1930.502 mm EFL and f/6.2. Only two conics and detector focus were solved. S24_B200 (f/2.4 primary, 200 mm back focus) gives 4.43 um worst RMS radius and 85% dense traced pupil survival but the longest folded package proxy at about 500 x 337 x 611 mm (103.1 L). S20_B120 gives 6.10 um, 90% and 500 x 337 x 542 mm (91.4 L). S16_B80 gives 8.77 um, 95% and 500 x 337 x 466 mm (78.6 L). Exact circular-obscuration-only transmission is 86.1/90.5/93.5%; the dense values differ by pupil quadrature resolution. All exclude spiders, cells, coatings, scatter, windows and tolerances.

S20_B120 is the balanced future comparison baseline, while S16_B80 remains a compact/high-throughput non-dominated point and S24_B200 remains a lower-aberration/lower-primary-slope point. S20 monochromatic 1.2 um corner MTF25/50 is 0.534/0.246 versus its matched obscured-pupil 0.663/0.393; 96-to-128-grid change is below 0.00042. Infinity-to-800 m SWIR refocus is 4.66–4.67 mm for all seeds, so the system still has two focus interfaces.

The preferred screening layout recesses B05 beside the SWIR aperture and folds only the SWIR converging return. S20's traced fold-plane clear size is about 42.4 mm. Its optical-only folded lower bound is about 446 x 313 x 487 mm (68.0 L); applying explicit cell/gap/dewar allowances gives the 91.4 L screen. Run 016 C02 remains 313.5 x 313.5 x 645.0 mm (63.39 L) before its own excluded cells and branch clearance. C02 therefore retains the smaller frontal area and present lower-bound volume, while folded C01 has a shorter axial inertia arm. Neither is complete CAD.

Under the common solid t/D=0.10, 2.2 g/cm3 mirror proxy, S20 C01 is 5.83 kg versus C02's 5.09 kg, but these are mirror blanks rather than payload mass. C01 has two optics over 100 mm and duplicated telescope cells/baffles, versus C02's one large common primary/shared front structure. C01 instead avoids C02's broadband common coating, dichroic and two unproved triplet-like cameras, and reuses B05. Both have two focus mechanisms. Current evidence implies lower C01 optical-development NRE but higher recurring structural duplication; no monetary winner is justified.

S20's screened channel centerline spacing is 255.2 mm (219.7 mm for tangent clear pupils). At 800 m this is about 319 urad, 92.5 EO pixels or 61.6 SWIR pixels of range-dependent parallax. C01 therefore needs explicit range-aware registration plus thermo-structural boresight calibration; C02 retains the common-front LOS advantage.

Run 017 decision: C01 is ACTIVE and non-dominated, but does not globally dominate C02-A6F1. C01 leads current optical completeness, geometric throughput, independent coatings and B05 reuse; C02 leads frontal area, common LOS, large-optic count and shared front structure. S16/S20 C01 and C02-A6F1 are preserved because different continuous objectives favor each.

Run 017 tested three materially distinct SWIR hypotheses with no plateau. Authoritative solves used 8/9/5 evaluations (22 total). Including two superseded debugging replays, total resource accounting is nine optimizer invocations, 352 evaluations and approximately 73.45 s accumulated probe/script process time plus reporting/verification. `reference/` remained unread and historical runs were unchanged.

Next recommended action, only after new instruction: one bounded C03 unobscured common-aperture C1 test, co-optimizing package, mirror mass, clearance, gimbal consequences and off-axis metrology from the first solve. Preserve C04 as the subsequent mandatory economic lane. Do not begin detailed C01 tolerance/CAD work or resume C02 backend optimization without a new instruction.

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
