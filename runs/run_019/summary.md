# Run 019 — bounded C03 sensitivity-aware UAV architecture screen

## Decision

**No screened minimum-complexity C03 form is a better current UAV Pareto point than both C01 and C02. Park C03 after this bounded C1 experiment.** The unobscured common front delivers 100% modeled geometric pupil survival, common LOS and no C01 parallax, but the compact end is optically poor, the better-imaging end is much too wide/large, and the lower-sensitivity geometry pays a large spacing and volume penalty. A real three-powered-element or TMA derivative could add pupil/aberration control, but this run supplies no evidence that its extra optic, alignment and NRE would recover the package trade. Reopen C03 only with a strict package allocation or new manufacturing evidence.

This is an architecture decision, not a customer acceptance test. No unsupplied image-quality, mass, volume or cost threshold is imposed.

## Model and bounded search

The minimum physical model is an unobscured, off-axis two-confocal-conic common afocal telescope, one dichroic, ideal EO/SWIR cameras and one passive camera-path fold. It preserves the required 311.371 mm SWIR entrance pupil and exact channel first-order EFL/f-number through the ideal backends. Four geometries trade 4x/6x/8x compression, primary speed, mirror separation and off-axis magnitude. Nine signed fields, three wavelengths and equal-area pupil samples were traced in both channels. No freeform was used.

From the first architecture screen, each point included central finite-difference response to +/-10 um mirror X/Y decenter and +/-100 urad X/Y tilt, one mirror at a time and without compensation. These are relative diagnostics, not tolerances or predicted production distributions. A fifth and final sensitivity-aware solve varied both conic constants and both channel focus offsets against nominal residual and representative perturbation response together; no nominal-only precursor was run.

## Optical, sensitivity and package trade

| C03 point | Passive-fold screen | EO / SWIR worst RMS radius | EO / SWIR composite perturbation response | Minimum beam gap | Consequence |
|---|---:|---:|---:|---:|---|
| A8_F1p0_O237 | 494 x 429 x 362 mm; 76.8 L | 77.86 / 43.67 um | 9.75 / 23.40 um | 2.90 mm | Compact endpoint; image performance is not competitive even with ideal cameras |
| A6_F1p0_O250 | 611 x 433 x 349 mm; 91.6 L | 55.16 / 31.07 um | 9.91 / 23.94 um | 3.53 mm | Compact A6 sensitivity reference |
| A6_F1p4_O256 | 621 x 442 x 453 mm; 124.3 L | 39.12 / 22.12 um | 5.72 / 13.76 um | 2.46 mm | 57.8% / 57.5% of compact-A6 response, but 35.7% more volume |
| A4_F1p2_O289 | 852 x 448 x 370 mm; 141.4 L | 27.30 / 15.46 um | 7.92 / 19.20 um | 3.56 mm | Better nominal endpoint, excessive lateral arm |
| A4_F1p2_O289_R | 852 x 448 x 370 mm; 141.4 L | 18.70 / 13.75 um | 7.89 / 19.11 um | 3.65 mm | Joint conic/focus refinement; best nominal, not desensitized |

The A6 spacing/speed change is the meaningful robustness result: it reduces the measured response to about 58% of the compact A6 value in both channels, qualitatively supporting the literature guidance that geometry must participate early. It is not a transferred 60% target, and the 35.7% package-volume increase prevents treating it as a free improvement.

The sensitivity-aware A4 conic solve improves nominal EO/SWIR RMS by 31.5%/11.1% but sensitivity by only 0.41%/0.45%. Final conics remain close to paraboloids. This shows why excellent nominal optimization alone would not answer the C03 question and why freeforms are not presently justified.

The compact and best-nominal endpoints pass a 16x48 to 24x72 pupil replay: worst-RMS changes are below 0.001% and dense physical survival is 100%. All final modeled points have 100% full-field geometric survival, but only 2.46–3.65 mm circle clearance before real cells, baffles, fold tilt and assembly margins. The neutral two-mirror-plus-splitter path sensitivity is 0.729 before camera/window/QE losses, versus 0.810 for a two-mirror path without a splitter under the same illustrative coefficients. These are coating sensitivities, not measured throughput.

## SWaP, gimbal and manufacture

Every point uses a 315.37 mm physical primary segment around the 311.37 mm illuminated aperture. The required parent-axis figure envelope is approximately 789–893 mm, separate from the illuminated clear aperture. Direct-segment solid-primary proxies are about 5.42 kg; common primary-plus-secondary proxies are 5.44–5.53 kg. The 85–123 kg full-parent-disk proxies are only an upper fabrication branch and are not assumed procurement or payload mass.

The compact A8 point is already 76.8 L and 494 mm at its largest dimension, versus the current integrated C01 B05-1/S16 screen at 68.2 L and 470 mm. Its nominal blur is far worse and its optical gaps are small. The best nominal C03 point is 141.4 L with an 852 mm lateral extent, producing an unattractive gimbal arm despite common LOS. The lower-sensitivity A6 is 124.3 L and 621 mm. C02's same-allowance straight screen is 79.7 L with a 5.09 kg common-mirror proxy; C03 wins geometric pupil transmission and avoids the annular primary/spider but does not establish a better complete package.

The two-mirror-only CG proxy sits 46–52 mm off the screened transverse box centre and 86–137 mm aft of its depth centre across the family. Its point-mass pitch-inertia proxy spans 0.0023–0.0136 kg m2, while the uniform-box vertical-axis specific-inertia proxy spans 0.0313–0.0719 m2 per unit mass. These exclude the dichroic, fold, cameras, cells, electronics, shell and gimbal; they identify balance and lateral-arm consequences rather than actuator requirements.

The modeled large-optic count is three at compact A6/A8 (primary plus tilted dichroic/fold) and five where the 4x/slow-6x camera beams also exceed 100 mm. Two channel focus mechanisms remain. The front mirrors and datum are shared, but cameras, detector interfaces, focus compensation and channel coatings remain duplicated. Direct off-axis segment fabrication avoids a full parent blank yet still needs a roughly 0.8–0.9 m parent-axis metrology reference, off-axis datum control and a credible null/CGH or sub-aperture plan. Those burdens, plus the long/wide folded boxes and small cell gaps, outweigh the unobscured-throughput benefit on current evidence. No supplier quote, yield or flight structure exists.

## Portfolio consequence

- **C01 B05-1/S16:** remains ACTIVE as the preferred practical system comparator, with S20 performance and S14 compact-stretch points preserved.
- **C02-A6F1:** remains CONDITIONAL ACTIVE for common LOS and compact frontal structure; obscuration, annular f/1 manufacture and real flat-field cameras remain its gates.
- **C03 minimum two-mirror common-afocal form:** PARKED.
- **C03 family:** PARKED after bounded C1; a true three-powered-element/TMA derivative is a possible future reopen condition, not the next task.
- **C04:** remains ACTIVE and is now the recommended next bounded C1 experiment.

Next recommended experiment, only after new instruction: execute the bounded C04 cost/COTS-maximized economic lane. Do not begin C03 freeforms, detailed tolerancing or production design.

## Unresolved issues and resource use

Unresolved C03 items include real EO/SWIR cameras, dichroic and fold angles, cells/baffles, stray light, polarization/coatings, thermal LOS stability, surface figure/mid-spatial allocation, lightweight segment mounts, actual gimbal structure and supplier cost/yield. These do not change the bounded disposition; they are reopen gates.

Four geometry points and one sensitivity-aware conic/focus attempt exhausted the normal five-attempt screen. The authoritative optimizer used one invocation and five evaluations. Two pre-closure corrections replayed that solve, making three invocations and fifteen evaluations total; three no-optimizer probes and two dense replays were also run. Observed WSL process time was approximately 145 s plus deterministic reporting/integrity work. No dependency was installed and no plateau occurred.

`reference/` was not accessed. Historical Track A/B runs and Run 016/018 evidence were not modified. Run 019 closes here.
