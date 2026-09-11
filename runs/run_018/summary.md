# Run 018 — C01 bounded UAV system-integration experiment

## Decision

**A compact, common-bench C01 is genuinely competitive with C02-A6F1, but neither architecture dominates all UAV objectives.** Treating C01 as two independent cylindrical housings was unnecessarily punitive. A shared twin-lobe shell, common rear detector/focus datum, axial EO staggering and one small SWIR converging-return fold reduce the preferred compact C01 screen to approximately 470 x 325 x 446 mm and 68.2 L. This is 13.2% below Run 017's separate-tube S16 screen and has a shorter axial inertia arm than C02's present straight model.

C01 still pays for a wider front face, two large optics, approximately 13% more solid mirror-blank proxy, separate focus mechanisms and relative-boresight calibration. C02 retains one 313 mm front aperture, a common fore-optic LOS, fewer large optics and shared primary-secondary metering. No customer threshold or single winner is imposed.

## EO choice: B05-1 versus B05-2

B05-2 was explicitly compared rather than rejected by default. It is 45.67 mm shorter and has better nominal dense RMS radius (0.576 versus 0.800 um). In the common-shell layouts, however, the SWIR train sets depth: B05-1 and B05-2 produce identical front faces and bounding volumes in every S20/S16/S14 combination. Rear-aligning detector/focus interfaces simply allows B05-2 to be staggered farther aft.

For the preferred S16 package, B05-2 reduces the open-saddle/common-bench structural-area proxy by only 1.67% and the four-mirror point-mass pitch-inertia proxy by 4.95%. Its established penalties remain a tighter secondary radius, 38.8 versus 14.66 um vertex-sphere departure, larger focus-only coupled-error residual (1.335 versus 1.063 um), and greater high-frame thermal focus travel (1.758 versus 1.375 mm). Therefore:

- **B05-1 remains the preferred integrated EO baseline on current complete-system evidence.**
- **B05-2 remains a conditional compact packaging option**, not parked; reopen the choice if a real detector/electronics stack uses its 45.67 mm shortening or its modest inertia benefit.

No B05 prescription was changed.

## SWIR compactness branch

Run 017's S20_B120 and S16_B80 prescriptions were preserved. One new low-DOF S14_B50 two-mirror seed extended the compact end; only its two conics and detector focus varied. No catadioptric corrector was added because a weak corrector would not shorten the dominant primary-secondary separation without introducing a new powered architecture and another search.

| SWIR seed | Primary / back focus | Separation | Worst RMS | Dense / exact circular transmission | Primary edge slope / departure | Integrated folded box |
|---|---:|---:|---:|---:|---:|---:|
| S20_B120 | f/2.0 / 120 mm | 441.6 mm | 6.10 um | 90% / 90.5% | 7.17 deg / 42.5 um | 470 x 325 x 522 mm; 79.8 L |
| **S16_B80** | **f/1.6 / 80 mm** | **379.6 mm** | **8.77 um** | **95% / 93.5%** | **8.93 deg / 80.2 um** | **470 x 325 x 446 mm; 68.2 L** |
| S14_B50 | f/1.4 / 50 mm | 346.4 mm | 11.48 um | 95% / 95.1% | 10.18 deg / 118.4 um | 470 x 325 x 402 mm; 61.5 L |

S14 converged in five evaluations while preserving 1930.502 mm EFL and f/6.2. It is a valid compact stretch point, not the preferred baseline: its extra 43.7 mm package reduction from S16 costs 31% worse RMS radius and substantially greater primary departure. S20 remains the optical-performance point. S16 is the preferred current UAV balance because it captures most of S14's package/throughput benefit without its full fabrication and image-quality penalty.

All geometric transmission excludes spiders, cell rims, baffles, coatings, scatter and tolerances. Reflective seeds have no modeled chromatic power, but broadband coating and detector-window performance remain open.

## Integrated geometry

The retained layout has:

- 325.37 mm SWIR cell outside diameter and 141.0 mm EO cell outside diameter in a shared twin-lobe shell with a 4 mm structural web;
- 470.37 x 325.37 mm actual screened front face and 237.19 mm optical-axis baseline;
- B05-1 staggered 91.55 mm aft in the preferred S16 package, aligning detector/focus hardware near a common rear datum;
- only 0.80 mm EO field walk through that staggered entrance tunnel at the diagonal half-field;
- a 36.85 mm traced SWIR fold clear size in the converging return path;
- no EO fold, because it does not reduce the SWIR-dominated box and adds coating, alignment and stray-light burden;
- no full-aperture front fold, which would require approximately pupil-scale flats and worsen optic mass and inertia.

The common bench/shell shares the gimbal attachment, major thermal datum, rear electronics plane and outer environmental enclosure while retaining separate optical cells and channel focus. This should reduce redundant housing and relative datum count, but it does not prove thermo-elastic boresight stability. Gradients, joints, cells and actual detector/dewar drawings remain absent.

## Parallax and simultaneous scene overlap

At the integrated 237.19 mm baseline and 800 m, angular parallax is 296.5 urad: 85.9 EO pixels or 57.2 SWIR pixels. That is a registration/calibration displacement, not a comparable loss of scene.

The planar 800 m footprints are approximately:

| Quantity | Width x height |
|---|---:|
| EO field | 11.305 x 8.280 m |
| SWIR field | 5.304 x 4.243 m |
| Simultaneous intersection | 5.304 x 4.243 m |

Thus **100% of the SWIR field remains inside the EO field**; the common intersection is 24.0% of the larger EO footprint. With the same baseline, full SWIR containment persists down to approximately 63 m for a horizontal baseline or 94 m for a vertical baseline, well inside the specified 800 m minimum focus distance. Terrain relief, uncertain range, distortion and thermo-mechanical boresight drift can still impair pixel registration, so a range-aware calibration model remains necessary.

## Mass, CG and inertia proxies

The preferred B05-1/S16 system has a 5.74 kg solid-mirror-blank proxy, versus 5.09 kg for C02-A6F1. These use the existing t/D=0.10 and 2.2 g/cm3 convention and are not payload mass. C01 still has two optics over 100 mm rather than C02's one.

An open-saddle/common-bench structure-area sensitivity is 0.455–0.602 m2 for S16. At the explicitly illustrative 5 kg/m2 coefficient it becomes 2.27–3.01 kg; it scales linearly and excludes local cells, joints, electronics and qualification. The same simple cylindrical-skin proxy for C02 is 0.742 m2 before its dichroic branches. This shows that shared C01 structure need not be twice C02's mass, not that a flight structure has been designed.

Using a uniform-box shape proxy, S16 C01 has 0.03498 m2 specific inertia about the vertical axis versus 0.05033 m2 for C02 with the same simple external allowances: C01's shorter depth helps pitch/yaw inertia. About the optical axis, C01 is worse at 0.02726 versus 0.01898 m2 because of its wider front face. The four-mirror projected-area proxy places optical CG approximately 30 mm toward the SWIR side and 122 mm aft of the geometric box center. Gimbal placement and electronics can rebalance this, but no complete mass model exists.

## Fair C01/C02 interpretation

C02's published Run 016 box is a 313.5 x 313.5 x 645.0 mm optical lower bound (63.39 L). Applying the same simple 12 mm radial and 55 mm axial allowances used here gives approximately 337.5 x 337.5 x 700.0 mm (79.7 L), still excluding dichroic branch clearance and camera packaging. The integrated C01 S20 screen is almost identical in volume at 79.8 L; S16 is 68.2 L and S14 is 61.5 L. These normalized screens support competitiveness but are not CAD proof, particularly because no folded C02 arrangement has been modeled.

C01 currently leads in demonstrated complete-channel feasibility, geometric throughput, independent coatings, reuse, simpler optical element count and axial package/inertia. C02 leads in frontal width, common LOS, large-optic count, solid mirror proxy and absence of range-dependent inter-aperture parallax. Cost follows the same split: C01 likely lowers optical NRE but adds recurring dual-cell/calibration work; C02 may reduce structural duplication but still needs its f/1 annular primary, dichroic and unproved flat-field cameras. No monetary ranking is justified.

## Portfolio status and next experiment

- **C01 integrated B05-1/S16:** ACTIVE preferred C01 UAV comparator.
- **C01 B05-1/S20:** ACTIVE optical-performance point.
- **C01 B05-1/S14:** ACTIVE compact stretch point, lower priority pending image-quality/manufacturing allocation.
- **B05-2 integration:** CONDITIONAL ACTIVE if real rear packaging exploits its shortening.
- **C02-A6F1:** CONDITIONAL ACTIVE and non-dominated.

**Next recommended experiment:** the bounded C03 unobscured common-aperture C1 screen already identified in project state, with package, clearance, mirror mass, gimbal inertia and off-axis metrology active from the first solve. C04 remains the following mandatory economic lane. Do not proceed to detailed C01 tolerancing/CAD or resume C02 backend optimization without new instruction.

## Resource use and integrity

One materially distinct new SWIR hypothesis and three integration layout classes were tested. The authoritative S14 solve used one optimizer invocation and five evaluations; two debug replays caused by script defects add ten evaluations, for three invocations and fifteen evaluations total. Observed WSL process time was approximately 59.6 s plus deterministic verification/reporting. No plateau occurred and no dependency was installed.

`reference/` was not accessed. Historical Track A/B and Run 016/017 prescriptions were unchanged and copied inputs verify exactly. Run 018 closes here.
