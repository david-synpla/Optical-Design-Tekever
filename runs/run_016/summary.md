# Run 016 — C02-A6F1 ideal-front and minimum-backend feasibility

## Decision

**Retain A6_f1p0 as a conditional C02 common-front seed, but stop C02 development here and test C01 next.** The two-paraboloid front is much better than its flat-plane spot sizes imply: its full-field residual after removing field-dependent radial defocus is 0.0278 waves RMS for EO at 550 nm and 0.00325 waves RMS for SWIR at 1.2 um. It therefore remains a credible common-LOS optical architecture.

However, a flat detector sees 21.32 um EO and 28.20 um SWIR corner RMS radius, and the first physical backend attempt shows that two spherical elements per channel are insufficient. The bounded doublets reach exact first order and retain the traced pupil, but their worst polychromatic RMS radii remain 33.93 um EO and 37.47 um SWIR. A6F1 now implies a real field-flattening, broadband camera of at least triplet-like complexity in each channel; that cost and tolerance burden must be compared with C01 before another C02 solve is authorized.

No customer IQ, throughput, obscuration, mass or cost threshold is invented. C02 is not selected and is not parked as a family. Its directly power-bearing form remains parked; the minimum doublet backend is parked; only the A6F1 common-front hypothesis remains conditionally active.

## Perfect-backend isolation

The exact Run 015 front prescription and apertures were coupled to perfect paraxial EO and SWIR cameras. Nine signed fields, three wavelengths and 4,608 equal-area rays per field were traced. The camera focal lengths are 132.367 mm EO and 321.750 mm SWIR, preserving the exact complete-system EFLs and f/6.2.

| Evidence | EO | SWIR |
|---|---:|---:|
| Minimum geometric pupil survival | 70.83% | 73.31% |
| Corner survival | 87.23% | 73.19% |
| Maximum split-pupil centroid walk | 1.484 mm | 4.223 mm |
| Maximum split-pupil RMS-ellipse axis ratio | 1.212 | 1.177 |
| Flat-detector corner RMS radius | 21.319 um | 28.196 um |
| Best individual corner focus shift | -0.400 mm | -0.533 mm |
| Best-focus corner RMS radius | 0.277 um | 0.420 um |
| Corner distortion | 0.827% | 0.120% |
| Approximate focal-surface radius from corner sag | 60.5 mm | 63.0 mm |

The field curvature is smooth and approximately common in radius despite the different channel scales. Individual +x/+y refocus also reduces EO RMS to 2.35/2.04 um and SWIR to 3.38/3.06 um; the residual is partly the coarse focus grid. The corner collapse by roughly two orders of magnitude is decisive evidence that the flat-plane blur is not structural coma/astigmatism.

## Forward pupil diffraction

The authoritative diffraction audit samples cumulative forward OPD at the real split-plane stop, preserving the remote-pupil ray aiming. Piston/tilt are removed for the flat-wavefront result, then a fitted radial quadratic is removed for the best-curved-focus diagnostic. This supersedes the preliminary `ScalarFFTPSF` entries embedded in `metrics.json` and `convergence.json`, whose numerical stop was behind the mirrors and is unsuitable for ranking this reflective path.

At the EO corner, the flat reference has 0.656 waves RMS at 550 nm and MTF50/100 of about 0.040/0.009 in both axes. Removing radial defocus leaves 0.0278 waves RMS and MTF50/100 of 0.745/0.503 (X) and 0.757/0.526 (Y), close to the same obscured-pupil limits of 0.756/0.525. At the SWIR corner, the flat reference has 0.331 waves RMS at 1.2 um and MTF25/50 of 0.108/0.018 (X); after defocus removal, 0.00325 waves RMS gives 0.651/0.413, essentially the matched 0.651/0.413 limit. The 128-to-160 grid replay changes any reported MTF/EE value by at most 0.00079.

These are monochromatic common-front results. They do not include real camera chromatic aberration, detector window, dichroic phase, coatings, scatter, polarization, spiders or tolerances.

## Minimum physical backend attempt

One air-spaced two-spherical-element camera was solved per channel with no dedicated pupil relay. EO used N-BK7/N-F2; SWIR used installed-catalog fused silica/CaF2 surrogates. Four curvatures, air gap and image distance varied. The EO attempt stopped after 27 evaluations and the SWIR attempt after 43.

| Backend | Final EFL | Final f/# | Minimum survival | Worst 3-wave, 9-field RMS radius | Status |
|---|---:|---:|---:|---:|---|
| EO spherical doublet | 793.778 mm | 6.1967 | 70.0% | 33.93 um | PARKED — insufficient broadband flat-field correction |
| SWIR spherical doublet | 1930.489 mm | 6.2000 | 73.13% | 37.47 um | PARKED — insufficient broadband flat-field correction |

The attempt is useful failure evidence. A physical camera can sit directly at the accessible collimated split and preserve essentially the Run 015 pupil survival, so a separate relay is not yet mandatory. But a simple doublet cannot simultaneously supply camera power, achromatization and the strong field flattening. The next C02 backend, if later authorized, should add one controlled degree of freedom (triplet/field flattener or an analytically seeded three-power form), not repeat doublet optimization. A naive unretargeted extra thin power changed EFL drastically and produced millimetre-scale blur; it is preserved in `metrics.json` only as evidence that pupil power cannot be added independently without re-solving the camera.

## Manufacturing, SWaP and integration

The f/1 primary is feasible in principle and is not rejected by speed alone. Its actual burden is a 313.50 mm clear diameter, 19.73 mm edge sag, 14.13 degree edge slope, 69.58 mm central hole and 121.96 mm radial annular clear width. The hole begins where the parent paraboloid sag is about 0.97 mm. This combination needs an explicit blank/hole process, annular support and print-through analysis, and a full-aperture null/CGH or validated sub-aperture metrology plan. No supplier quote, mirror material, areal density, surface figure or production yield is available, so neither mass nor cost is claimed.

C02 pays 26–29% geometric pupil loss before spider and coating losses, two broadband common mirrors, a dichroic, and now likely at least three powered camera elements per channel. Its benefit remains a single common fore-optic LOS, a compact 259.48 mm mirror separation, an accessible collimated split and no demonstrated need for a separate pupil relay. Dichroic angle/thickness, broadband mirror coating, channel AR coatings, polarization, ghosting, baffling, spider diffraction, focus/thermal travel and mirror separation sensitivity remain open.

The straight sequential package lower bound is approximately 313.5 x 313.5 x 645.0 mm, or 63.39 L, before cells, baffles, dichroic branch clearance, electronics, thermal hardware and gimbal margin. This agrees only with the lower edge of Run 014's broad C02 envelope; it is not CAD. Under the unchanged Run 014 solid-blank proxy (thickness/diameter 0.10 and density 2.2 g/cm3), the annular primary plus secondary are about 5.09 kg. That is not payload mass and could change materially with material, sag allowance, lightweighting, ribs, hole reinforcement and mounts. The present layout has one optic over 100 mm, a 56.25 mm secondary, approximately 62.3 mm SWIR camera elements, approximately 27.6 mm EO elements, one dichroic and two focus mechanisms. Folding the channel paths is likely necessary to reduce the straight 645 mm inertia arm, but no folded bounding box is yet proved. The complete continuous-objective record is in `swap_screen.json`.

## Portfolio consequence and next experiment

- **C02-D direct shared imaging:** PARKED, unchanged from Run 015.
- **C02-A6F1 common front:** CONDITIONAL ACTIVE optical seed; excellent curved-field wavefront, real pupil walk/obscuration and difficult manufacture remain.
- **C02 two-element channel cameras:** PARKED.
- **C02 family:** provisionally non-dominated for common-LOS performance, but not the next development priority.

**Next recommended experiment:** execute the planned bounded C01 C1 investigation, using the best preserved B05 EO lane as evidence and creating an independent SWIR seed plus co-boresight/parallax, packaging and focus/thermal interface model. C01 is a practical low-coupling reference/fallback, not the presumed overall leader. Its optical, mass, volume, large-optic, duplicated-structure, mechanism and gimbal proxies must be co-optimized and compared with A6F1. Only return to C02 if that Pareto comparison justifies one three-element flat-field backend attempt per channel. C03/C04 remain active later branches; C05 remains parked.

## Resource use and integrity

Four substantial bounded batches: perfect-backend full-field/diffraction trace, per-field focus sweep, one EO doublet solve and one SWIR doublet solve. Two optimizer attempts used 27 and 43 evaluations; no plateau and no repeated rescue attempt. Recorded kernel wall time is 109.44 s, plus imports, reporting and verification. One ideal extra-power diagnostic was cheap. No package installation occurred.

`reference/` was not accessed. Historical Track A/B prescriptions and runs were not changed. Run 016 closes here.
