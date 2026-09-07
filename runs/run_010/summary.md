# Run 010 — matched sensitivity and assembly-compensator comparison

**Decision: retain all three candidates for the matched thermal/material study. B05-1 remains the provisional lower-risk baseline. B05-2 retains a useful compactness trade. B06 retains a substantial low/mid-frequency and energy-concentration advantage, but requires more alignment control and has greater figure-error sensitivity. No final architecture selection or Track B freeze is justified.**

The question is answered to the level supported by the saved ideal-surface models and the bounded diagnostic study. No nominal shape, glass choice or aperture was optimized. All earlier runs and Track A remain unchanged; reference/ was not accessed.

## Common experiment

Models are imported directly from the immutable Run 008 and Run 009 archives. Run 008 root configuration supplies B05-1; its attempt_02 configuration supplies B05-2; Run 009 attempt_01 supplies B06. Each candidate's nominal_prescription.json records the actual global coordinates, radii, conics, materials and apertures used. Replay matches the saved model's ray coordinates exactly. Software checks also prove that secondary despace leaves downstream vertices fixed, rigid-body motion leaves radii unchanged, and detector decentre translates image coordinates without falsely changing centred RMS.

Nine signed fields span the active detector angular field; six wavelengths are 430, 500, 550, 650, 725 and 800 nm with equal weights. Sensitivity uses 64 equal-area physical-pupil samples: common area coordinates, annulus for B05 and disk for B06. Rays are centred on one common spectral centroid per field, not independently per wavelength. Reported RMS is the largest wavelength/field value, with median, P90 and all individual values also saved. Selected cases were retraced at 25 fields and 576 physical-pupil samples. No lost rays were discarded to improve the merit.

There are 38 diagnostic variables per B05 variant and 29 for B06. All powered bodies receive axial/X/Y displacement and X/Y tilt; B06 additionally receives clocking about each patch's local surface normal. Tilts pivot about the physical patch centre for B06, the front vertex for a B05 lens, or the parent vertex for a centred mirror. The two faces of each lens move as one body. The B05 primary return-hole plane follows its primary. Detector focus, decentre and tilt are separate diagnostics. Shape checks include every powered radius, mirror conics, each B05 glass index and lens centre thickness. A corrector-group axial diagnostic supplies the lens-spacing/group-placement comparison.

| Diagnostic | Applied step, both signs | Meaning |
|---|---:|---|
| Body displacement / detector focus / lens thickness | 0.010 mm | Diagnostic amplitude, not a manufacturing tolerance |
| Body or detector tilt / B06 clock | 100 microradians | Defined pivot and axes; not a supplier capability |
| Radius | 100 ppm of saved radius | Relative radius error; absolute radius change differs between surfaces |
| Conic | 0.001 absolute K | Parameter sensitivity; **not equal figure error across mirrors** |
| Glass index | 0.0001 added at every wavelength | Constant index-offset surrogate; not a melt/dispersion or dn/dT model |

Each sensitivity.csv distinguishes step, measured slope, uncompensated result and compensated result. The slope is RMS **ray-coordinate** derivative over X/Y, fields, colors and pupil, in um per stated parameter unit; it is not the derivative of the worst-field scalar RMS. It is approximately radial-RMS sensitivity divided by sqrt(2) for a pure added aberration. Relative nonlinearity ratios for effectively zero columns, notably detector X/Y decentre, are numerical noise and must not be interpreted as fragility. Surface sag changes after piston/tip/tilt removal are tabulated in audit.json to expose how unequal a common K or radius coefficient error can be. No production allocation is proposed without an image-quality budget, supplier capability and metrology error budget.

## Coupled errors and recovery

Twenty-four Latin-hypercube specimens use independent uniform errors within the diagnostic amplitudes, seed 20260907. Shared parameter names receive the same normalized draws. B05 has its real extra lens variables; B06 has its tertiary and clock variables. The redundant corrector-group translation is excluded from simultaneous draws. This explores coupling; it is not a yield estimate, confidence interval or proof that the distributions are realistic production errors.

Compensation is one linear least-squares correction of the **change from the unchanged nominal ray residual**, followed by an actual nonlinear retrace. It does not improve the nominal design. The main comparison uses one compensator (detector Z), then three (detector Z and secondary X/Y tilt). Alternative two/three-control sets are evaluated separately, never cumulatively: focus plus secondary Z, focus plus detector tip/tilt, focus plus B05 corrector Z, or focus plus B06 tertiary X/Y tilt. Diagnostic travel caps are +/-0.5 mm and +/-1 mrad, not mechanism requirements. None of the selected three-control specimens hits a cap. These calculations assume the residual can be measured; no practical estimator, actuator accuracy, hysteresis or measurement noise has yet been modeled.

| Worst-field/wavelength RMS, um | B05-1 | B05-2 | B06 |
|---|---:|---:|---:|
| Common nominal, 25-field dense check | 0.800 | 0.576 | 1.360 |
| Coupled errors: median / largest, no compensation | 6.761 / 13.097 | 8.469 / 17.005 | 8.918 / 19.004 |
| Detector focus only: median / largest | 0.944 / 1.063 | 0.903 / 1.335 | 3.989 / 7.477 |
| Focus + secondary X/Y tilt: median / largest | 0.862 / 0.999 | 0.770 / 1.084 | 1.627 / 2.522 |
| Three-control worst specimen, dense retrace | 1.000 | 1.084 | 2.552 |

These common six-color baselines differ from Run 008's 17-color audit because spectral weights and pupil quadrature differ; this is not a new nominal optimization.

At +10 um secondary despace, uncompensated RMS is 3.973 / 5.493 / 7.237 um. At +100 ppm primary radius, it is 11.265 / 13.918 / 12.232 um. B05's dominant errors are largely focus-like. B06's -0.001 primary-K case still reaches 2.299 um after three-control correction. B06 primary clock at +100 microradians gives 1.651 um before compensation; clocking is a real datum, not an irrelevant rotation of a centred conic.

The uncompensated coupled-case deviation from the linear ray prediction is at most 0.0029 / 0.0046 / 0.0140 um RMS per coordinate. That supports local linear diagnostics at these amplitudes, not extrapolation to larger errors. Actual compensated retraces, not the linear prediction, supply the table.

## Compensator coupling and practicality

For the selected focus/secondary-tilt set, normalized Jacobian condition numbers are approximately 1.00 / 1.00 / 1.84. B06 focus and secondary X tilt have correlation 0.543: coupled, but not numerically degenerate in this full-field measurement basis. Focus plus secondary Z is much more ambiguous: condition numbers 436 / 170 / 19.4. Focus plus B05 corrector Z is also correlated (58.1 / 17.8). These axial pairs should not be treated as independent easy knobs.

B06 focus/tertiary tilt gives a larger worst sampled RMS of 6.518 um and saturates 9/24 cases; focus/detector tilt leaves 7.482 um and saturates 14/24. Focus/secondary Z saturates 9/24 and can worsen performance badly under this one-step capped policy. These are failures of those tested correction policies, not proofs that no iterative alignment can work. There is no reason to add them all as free rescue variables when the three selected controls already provide a clear comparison.

| Selected assembly adjustments over the 24 cases | B05-1 | B05-2 | B06 |
|---|---:|---:|---:|
| Detector global Z, mm | -0.190 to +0.172 | -0.253 to +0.228 | -0.295 to +0.240 |
| Largest absolute secondary tilt adjustment, mrad | 0.341 | 0.385 | 0.872 |
| Compensated local image-scale range, mm/radian | 793.825–794.594 | 792.811–795.557 | 792.293–795.902 |
| Largest field-centroid displacement from nominal, um | 71.6 | 80.7 | 185.4 |

B06's negative final propagation direction means global detector Z has the opposite sign to motion along the final beam. These assembly travels are not the 800 m refocus travels, which remain in earlier runs; combining both into a mechanism stroke requires a later mechanism design. Image scale is measured from the central-field Jacobian, not an invalid rotationally symmetric paraxial EFL for a misaligned TMA.

**Centroid displacement has not been silently compensated.** Decentre of the detector changes registration, not centred RMS. Three optical compensators do not guarantee that the original angular field remains on the fixed active pixel rectangle. Nominal field-edge distortion already makes that mapping slightly imperfect. Boresight/registration and active-field coverage must be allocated explicitly; adding detector X/Y would be two further mechanical controls, not a free consequence of a centred spot metric. No pointing or distortion tolerance exists in the source requirements.

## Diffraction advantage after error

Scalar monochromatic FFT uses the physical entrance pupil, about 112 samples across its diameter for each candidate; B06's larger virtual-parent grid is only a coordinate device. A zero-phase reference preserves each transmitted pupil amplitude. Frequencies are 50, 100, 150 and 182.482 lp/mm. All calculations use one fixed detector state per specimen, not separate wavelength refocus or averaged MTF magnitudes.

The following is the positive corner at 550 nm for each candidate's **worst RMS specimen after the selected three compensators** (B05 specimen 11; B06 specimen 19). It is a stress-case comparison, not a search for worst spectral MTF among all specimens.

| Metric after three controls | B05-1 | B05-2 | B06 |
|---|---:|---:|---:|
| MTF X/Y, 50 lp/mm | 0.509 / 0.511 | 0.513 / 0.515 | 0.740 / 0.694 |
| MTF X/Y, 100 lp/mm | 0.230 / 0.231 | 0.236 / 0.236 | 0.481 / 0.435 |
| MTF X/Y, 150 lp/mm | 0.180 / 0.180 | 0.186 / 0.187 | 0.280 / 0.254 |
| MTF X/Y, Nyquist | 0.199 / 0.200 | 0.206 / 0.206 | 0.183 / 0.168 |
| 2x2-pixel EE / matched ideal | 0.406 / 0.411 | 0.408 / 0.411 | 0.650 / 0.791 |

B06 retains about 82% of its matched ideal EE here and still concentrates about 1.6 times the energy fraction of B05 in the box. Its 100 lp/mm contrast remains about twice B05's, but its Nyquist contrast is lower. At 800 nm, B05 also exceeds B06 at 150 lp/mm. The appropriate trade is frequency-dependent; neither nominal RMS nor a single Nyquist value can select the architecture.

Center and both signed Y corners are evaluated at 430/550/800 nm for nominal, uncompensated, focus-only and three-control states. The six-color geometric study spans the entire requested band; the diffraction study samples endpoints and center, not every spectral interval. Source/QE-weighted broadband performance remains open. FFT scaling uses the common requirement-derived focal length: the measured image-scale changes imply an additional roughly 0.25% spatial-frequency scaling uncertainty, below the large architecture differences but relevant to small numerical rankings. Detector tilts here are <=100 microradians; FFT axes are the paraxial global transverse axes, not an exact tilted-plane vector diffraction calculation.

Increasing physical-pupil sampling to 168 changes selected MTF values by at most 0.00235 and EE by 0.00273 for B05, and 0.00065 / 0.00023 for B06. Do not rank the small B05 differences at finer precision than this. Plots show the measured values without claiming continuous-band certification.

## Physical interfaces

No defensible detector-window material/thickness or detector-body drawing exists in the supplied requirements. Separate **hypothetical** N-BK7 windows of 0.5 and 1.0 mm, 1 mm ahead of the detector and 10 mm clear radius, quantify this missing interface. These are not Sony specifications or added nominal design elements. The original powered surfaces remain fixed. A 1 mm window requires approximately +0.342 / +0.342 / -0.351 mm global detector refocus; refocused RMS is 0.785 / 0.613 / 1.582 um. That result cannot substitute for the actual sensor stack, coatings, wedge and thermal properties.

B06 boundary clearance is 6.037 mm nominal and 6.004 mm in the compensated stress specimen, against the existing conservative mirror envelopes. This includes the incoming path. A separate 2 mm additional radial cell-envelope scenario still leaves about 4.13 mm on the interior quadrature; no actual cell/support volume is certified. The secondary return-beam corridor is the obvious interface to protect.

B05's interior pupil quadrature misleadingly suggested about 1.2 mm clearance to the secondary. The dedicated **boundary** audit instead finds conservative overlap of 0.026 mm nominal and 0.036 mm in the compensated specimen. Direct incoming-ray intersection with the actual secondary confirms small extra shadowing beyond the frozen annulus approximation: at most **0.0129% / 0.0070%** of annular area nominal, and **0.0208% / 0.0149%** after compensation for B05-1 / B05-2. Thin-shell area integration was repeated at two radial densities. Thus the earlier annular model is a very close approximation, not a complete nonsequential obscuration model. Its historical results have not been rewritten. This tiny correction was not applied to the sensitivity/FFT arrays; it does not resolve the much larger unknown spider/cell effects.

A 2 mm added B05 secondary radial envelope clips even interior sampled rays. Secondary support must therefore fit within an allocated obstruction or deliberately increase it. A spider must cross the entrance beam unless another support concept is supplied; its width, diffraction and thermal motion remain unknown. Primary-hole clearance is checked as an annular obstacle, but real primary cell, secondary substrate/backside, baffles and detector package remain unresolved. No invented housing dimensions or complete clearance claim is made.

## Manufacturing and alignment assessment

| Topic | B05-1 / B05-2 | B06 |
|---|---|---|
| Secondary manufacture | B05-2 has tighter curvature (-310.48 versus -541.90 mm) and larger vertex-sphere departure (38.80 versus 14.66 um); lower absolute K does not make it easier. It also needs greater focus recovery and shows greater image-scale spread. | All three surfaces are off-axis patches. The common K diagnostic produces unequal sag errors; audit.json quantifies that. Primary conic accuracy remains a notable residual risk after alignment. |
| Lens fabrication/assembly | Four spherical surfaces in two custom lenses; radii, thickness, index-offset, centring and whole-element tilt were tested. Define optical axis to lens edge/barrel seat and control wedge/face-to-face centring, which is not represented by a pure whole-body tilt. | No powered lenses, but actual detector window is still required. |
| Datums / precision DOFs | Four powered bodies x five meaningful rigid-body DOFs = 20 diagnostic mechanical coordinates, plus five detector coordinates; these are not 25 adjustable knobs. Primary/barrel define the assembly frame. | Three patches x six rigid-body DOFs = 18, plus five detector coordinates; local normal, patch center and clock mark must be transferred to mechanical datums. |
| Test concept | Independently verify radii/conic shape; use appropriate asphere null/CGH testing for mirrors and conventional spherical test/centring methods for lenses. Verify the assembled field response, not only on-axis focus. | Establish patch mechanical/optical datums, then prescription-specific null/CGH or suitable stitched surface metrology, with clock and placement observable independently from residual figure. A parent-axis drawing alone is not an assembly datum. |
| Proposed alignment sequence | Inspect parts and lens subassembly; fix primary/barrel; set measured secondary spacing; establish detector focus; measure symmetric signed field residuals; apply secondary X/Y tilt if needed; check image scale and detector registration; lock and remeasure. | Inspect and register all patch datums/clock marks; establish measured mirror placement; set detector focus; use signed field information to separate secondary tilt from focus; verify tertiary placement independently; verify clearances and registration before locking. |
| Accessibility | Detector focus needs external axial access; secondary adjusters/spider must avoid clipping or obstructing test access. Corrector translation is correlated with focus and is not a preferred extra knob. | Secondary tip/tilt needs access without using the ~6 mm beam corridor for hardware. Detector focus is spatially separated; actuator attachment and locking remain undesigned. |
| Cost drivers, engineering judgement | B05-1 is the lower assembly/metrology-risk baseline. B05-2 buys ~45.7 mm axial compactness at greater secondary fabrication and calibration burden. | Custom off-axis test fixtures, datum transfer, clocking, stronger alignment recovery and tighter figure control are likely major nonrecurring cost drivers. No quotation or monetary estimate exists. |

CGH/null testing is a credible **candidate method**, not a selected vendor process: [Zygo describes CGHs for off-axis aspheric surfaces](https://www.zygo.com/products/metrology-systems/laser-interferometers/computer-generated-hologram), and [AOM describes transfer of mechanical datums into CGH optical references](https://aom.us/resources/2026-datum-based-metrology-for-freeform-optics/). Neither source certifies these prescriptions, tolerance capability, or cost. Only generic metrology information was consulted; no reference-design research was performed.

## Answers and next action

1. **B05-1 remains the provisional lower-risk baseline.** Focus alone recovers this diagnostic population well, with smaller image-scale and secondary-shape burdens.
2. **B05-2 remains justified by compactness.** Its nominal diffraction advantage is small relative to numerical precision and the pupil limit; its shorter package is the meaningful differentiator. It is not automatically preferable, nor sufficiently dominated to park.
3. **B06 merits continued development.** Three realistic types of adjustment retain substantial mid-frequency/EE advantage in the tested errors; focus alone is inadequate. This is conditional on datum/metrology quality and registration, not demonstrated production robustness.
4. **Park none of these three on this evidence.** All merit the next bounded matched thermal/material study across -25 to +50 C, retaining the same nominal prescriptions and explicit compensator limits. Obtain/parameterize actual substrate, structure and detector-window data, and include spider/cell thermal motion. Do not begin a broad thermal optimization or another nominal shape search within Run 010.

## Reproducibility and stopping

Use the configured WSL Python and archived track_b_run010_*.py scripts. The sensitivity and LHS/diffraction stages retain completed checkpoints on resume; validation artifacts and summary are stored only in this run. provenance.json and SHA256SUMS.txt identify exact inputs and outputs. Per-candidate folders retain all +/- results, raw Jacobian, 24 individual specimens, all compensator policies, diffraction arrays, denser checks, interface scenarios and nominal prescription exports.

The run uses **zero iterative optimizer invocations and zero nominal shape attempts**. Central-difference matrices, direct linear least-squares assembly corrections and bounded diagnostic ensembles are analyses, not hidden shape searches. Nine substantial analysis batches (three candidate sensitivity studies, three coupled ensembles, three diffraction follow-ups) were followed by cheap convergence/interface checks. closure.json records final elapsed time and counters. The run stops because its engineering question is answered to the model's limits, not because a numerical winner was forced. User instructions set the investigation scope; no human optical correction or quota interruption occurred during Run 010.
