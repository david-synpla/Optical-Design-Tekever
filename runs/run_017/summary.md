# Run 017 — C01 bounded system-level comparator

## Decision

**C01 is non-dominated and deserves further development, but it does not globally dominate Run 016 C02-A6F1.** A separate, mechanically integrated EO+SWIR payload is physically credible with the unchanged B05-1 EO telescope and a fresh two-conic SWIR Cassegrain. It offers substantially higher geometric pupil transmission, independently optimizable coatings and focus, no dichroic, and no demonstrated need for the two triplet-like cameras implied by C02. Its penalties are equally real: two large entrance optics, duplicated telescope metering structures, an approximately 500 mm screened front-face span, and a 255 mm screened channel baseline that creates range-dependent parallax and relative-boresight drift.

Three SWIR seeds remain non-dominated. S24_B200 has the best image quality but the longest/heaviest package; S16_B80 is the shortest and least obscured but has the fastest, highest-departure surfaces and weakest image quality; S20_B120 is the balanced C01-versus-C02 system baseline. No customer image-quality, mass, volume, obscuration, throughput, cost or pointing threshold is invented.

## Preserved B05 EO evidence

The Run 008 B05-1 model and configuration were loaded directly and were not altered. A fresh replay gives 794.203 mm EFL, f/6.2 and 0.799 um worst sampled RMS radius, consistent with Run 010's 0.800 um dense result. Run 013 remains the applicable bounded EO focus/thermal evidence: approximately 0.04 mm thermal focus travel for its 1.2 ppm/K structural scenario, up to 1.37 mm for its 24 ppm/K scenario, plus approximately 0.8 mm range focus at 800 m. These scenarios are engineering evidence, not transferred customer requirements.

B05-1 contributes a 128.10 mm entrance pupil, 133.0 mm primary blank envelope, two mirrors, two spherical corrector lenses and one channel focus interface. Reuse materially reduces C01 optical NRE and preserves independent EO commissioning, but its spider/cell, detector window, barrel and production tolerances remain unresolved.

## Fresh SWIR optical evidence

Each independent SWIR seed preserves 1930.502 mm EFL and f/6.2. Only primary conic, secondary conic and detector focus were varied. Nine signed fields and three wavelengths across 0.80–1.80 um were evaluated with physical entrance, secondary and primary-hole apertures. Reflective performance is achromatic in this model; coatings, scatter, detector window and tolerances are not included.

| Seed | Primary / back focus | Mirror separation | Worst RMS radius | Circular-obscuration transmission | Dense traced transmission | Primary edge slope | Folded package proxy |
|---|---:|---:|---:|---:|---:|---:|---:|
| S24_B200 | f/2.4 / 200 mm | 482.9 mm | 4.43 um | 86.1% | 85% | 5.98 deg | 500 x 337 x 611 mm; 103.1 L |
| **S20_B120** | **f/2.0 / 120 mm** | **441.6 mm** | **6.10 um** | **90.5%** | **90%** | **7.17 deg** | **500 x 337 x 542 mm; 91.4 L** |
| S16_B80 | f/1.6 / 80 mm | 379.6 mm | 8.77 um | 93.5% | 95% | 8.93 deg | 500 x 337 x 466 mm; 78.6 L |

The 1% difference between exact obscuration and dense traced fractions is pupil quadrature resolution, not unexplained clipping. Spiders, cell rims and baffles will reduce these figures. At 800 m, the three seeds refocus by 4.66–4.67 mm, matching the first-order requirement-derived value; this makes a separate SWIR focus mechanism unavoidable unless another system-level focus strategy is demonstrated.

For S20 at 1.2 um, scalar FFT gives center MTF25/50 of 0.590/0.333 and corner MTF25/50 of 0.534/0.246, versus matched obscured-pupil values near 0.663/0.393. The corner relative peak is 0.742. Increasing the pupil grid from 96 to 128 changes any reported MTF or relative-peak number by less than 0.00042. The seed is credible enough for architecture comparison, not a final diffraction-limited prescription.

## Package, mass and gimbal comparison

The preferred physical arrangement is **recessed side-by-side apertures with the SWIR converging return beam folded 90 degrees**. The fold plane was traced at 35% of SWIR back focus; S20 needs an approximately 42.4 mm elliptical-clear fold. The tilt itself and housing are not modeled, so this is a kinematic packaging witness, not CAD. A straight S20 arrangement is approximately 500 x 337 x 620 mm and 104.6 L under the same screening allowances; folding reduces it to approximately 500 x 337 x 542 mm and 91.4 L. Stacking only rotates the same front-face span and volume, so gimbal-axis orientation, not optical volume, decides between horizontal and vertical placement.

The S20 optical-only folded lower bound is approximately 446 x 313 x 487 mm, or 68.0 L, before the explicit cell/gap/dewar allowances that produce the 91.4 L screened box. Run 016's C02 number is a different, straight optical lower bound: 313.5 x 313.5 x 645.0 mm, or 63.39 L, before cells, dichroic branch clearance, electronics and gimbal margin. Therefore C02 retains the smaller frontal aperture and present lower-bound volume, while folded C01 has the shorter depth/inertia arm. Neither architecture has a proved complete CAD envelope.

Under the unchanged solid t/D=0.10, 2.2 g/cm3 mirror-blank proxy, S20 C01 has 5.83 kg of EO+SWIR mirrors versus 5.09 kg for the C02 common mirrors, approximately 14.5% more. An independent 15–30 kg/m2 mirror-area sensitivity gives 1.53–3.07 kg for the C01 mirrors, but excludes ribs, cells and qualification and is not payload mass. C01 also has two optics over 100 mm rather than C02's one. Conversely, C01 has four powered mirrors plus the two preserved EO lenses, while C02 currently implies two common mirrors, a dichroic and at least three camera elements per channel. Both currently require two focus mechanisms.

The screened C01 optical-axis baseline is 255.2 mm including cells/gap (219.7 mm for tangent clear pupils). At 800 m this corresponds to about 319 urad, 92.5 EO pixels or 61.6 SWIR pixels of range-dependent parallax if the axes are co-aligned at infinity. Calibration can remove deterministic disparity only with adequate range knowledge; structure temperature, vibration and gimbal loading also create a relative-boresight stability problem that C02's common front avoids.

## Manufacturing, coatings and cost/NRE

S20's 313.37 mm primary has 9.85 mm edge sag, 7.17 degree edge slope and 42.5 um edge departure from its vertex sphere; its 96.12 mm convex secondary has 2.14 mm edge sag and 20.4 um vertex-sphere departure. S16 reduces length and secondary size but increases primary edge sag/departure to 12.32 mm/80.2 um and secondary departure to 30.6 um. S24 is the gentlest primary but uses a 116.0 mm secondary and the largest obstruction. All are custom aspheres requiring explicit null/CGH, substrate, central-hole, support and lightweighting plans; none has supplier capability or cost evidence.

C01 avoids C02's 0.43–1.80 um common-mirror coating compromise and dichroic polarization/ghost problem. EO and SWIR reflectors and AR coatings can be optimized independently. It also avoids C02's f/1, 313.5 mm annular primary and currently unsuccessful physical cameras. C01 instead duplicates cells, baffles, detector barrels and assembly datums and requires cross-channel boresight metrology. On current evidence C01 likely has lower optical-development NRE and higher recurring mechanical duplication; C02 likely has higher custom optical/backend NRE and potentially lower recurring structural duplication. No monetary ranking is justified.

## Direct C01 versus C02 Pareto conclusion

- **Optical/throughput:** C01 leads with successful independent imaging seeds and 90–95% SWIR geometric transmission for its balanced/compact points. C02's common front is excellent at a curved focus but its physical doublets failed and traced channel survival is 70.8–73.3%.
- **Frontal area/common LOS:** C02 leads with one approximately 313.5 mm aperture, one optic over 100 mm and no inter-aperture parallax. C01 needs an approximately 500 mm screened transverse span and cross-channel calibration.
- **Length/inertia:** folded S16/S20 C01 offers a shorter 466/542 mm screened depth than C02's 645 mm straight sequence. C02 has no validated folded bounding box, so this is not a final inertia ranking.
- **Mass/structure:** C02 leads the current solid mirror proxy and shares the front metering structure. C01 is only about 0.74 kg higher in that proxy but duplicates cells/baffles; complete lightweight structures could change the result.
- **Manufacturing/NRE:** C01 reuses B05, uses independently coated two-mirror SWIR optics and avoids a dichroic and two complex cameras. C02 uses fewer large structures but concentrates risk in an f/1 annular primary, broadband coating/splitter and unproved flat-field cameras.

Thus C01 is a credible practical comparator and possible UAV-level winner under some cost, throughput and development-risk preferences, while C02 remains preferable under frontal-area, common-LOS and shared-structure preferences. The evidence supports a portfolio, not a forced winner.

## Status and next experiment

- **C01 family:** ACTIVE and non-dominated.
- **C01-S20_B120:** balanced system comparator for future cross-architecture tables.
- **C01-S16_B80:** retained compact/high-throughput point; do not discard for weaker nominal RMS alone.
- **C01-S24_B200:** retained performance/lower-slope point; lower priority because of package length and obstruction.
- **C02-A6F1:** CONDITIONAL ACTIVE, unchanged; no further backend solve before broader comparison.

**Next recommended experiment:** a bounded C03 unobscured common-aperture Stage C1 test that co-optimizes package, optic mass, clearance and metrology from the first solve. It is the missing conventional high-throughput common-LOS comparator. Preserve C04 as the subsequent mandatory economic lane. Do not enter detailed C01 tolerance/CAD development or resume C02 backend optimization in this run.

## Resource use and integrity

Three materially distinct SWIR hypotheses were tested, below the five-attempt stage budget; none plateaued. The authoritative solves converged in 8, 9 and 5 evaluations (22 total). Including two superseded debug replays caused by JSON serialization and an incorrect preliminary transmission denominator, nine optimizer invocations and 352 evaluations were executed. Approximate accumulated probe/script process time was 73.45 s plus reporting and verification. Superseded preliminary values are not candidate evidence; `execution_log.json` preserves the accounting.

No dependency was installed. `reference/` was not accessed. Historical Track A/B prescriptions and runs were unchanged. Run 017 closes here.
