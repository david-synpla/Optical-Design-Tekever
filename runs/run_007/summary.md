# Run 007 — B04 physical-pupil and first-order gate

Decision: preserve B04 ACTIVE as a screened physical optical model. End this run and compare B05 next, rather than spend all remaining B04 attempts polishing this seed. B04 is not verified for production and Track B is not frozen.

## Findings

- 550 nm paraxial EFL **794.202899 mm**, entrance pupil **128.097242 mm**, nominal **f/6.2**. A uniform scale of optical radii and separations enforces EFL while retaining the specified entrance diameter. This replaces the centroid-based image-scale proxy used in Run 006; it does not enforce identical EFL at all wavelengths.
- Six wavelengths (430/500/550/650/725/800 nm), nine signed active-array field positions, common detector plane: worst common-centroid RMS **7.4446 um**. The scaled initial physical model was 7.4828 um, so the solve's optical improvement is only 0.51%. The meaningful advance is first-order restoration and explicit physical pupil modeling, not a claimed large RMS gain.
- At **800 m**, a detector-only shift **+0.788753 mm** gives sampled worst RMS **7.3816 um**. Refocus optimized center/corner at three wavelengths and was checked at all nine fields/six wavelengths. The object distance is measured from the entrance reference plane. This demonstrates nominal optical refocus, not a designed mechanism or thermal focus range.
- Entrance annulus: outer radius 64.0486 mm, inner radius 35.5 mm, situated 3 mm ahead of the secondary vertex. Primary radius 66.5 mm with 21.5 mm hole; returning beam explicitly traverses that hole; secondary radius 35.5 mm; lenses radius 17.5 mm. These are mechanical screening assumptions, not customer limits.
- Uniform full-pupil sampling gives about **69.31%** surviving area across all nine fields at 550 nm, consistent with analytic annulus area **69.28%**. No extra sampled field clipping occurs. Finite wavelength/edge sampling does not prove continuous-field clearance, detailed baffle/spider clearance or actual transmission.
- Lens edge thicknesses are positive: **3.54/3.34 mm**. Real cells, primary substrate thickness, spider, baffling and detector envelope are still absent.

## Diffraction-aware image quality

`diffraction.json` contains monochromatic optical MTF on detector X/Y axes at 50/100/150/182.482 lp/mm and centered 1/2/3-pixel ensquared energy. Each actual scalar FFT is compared with a zero-phase pupil retaining the same aperture and amplitude. The centroid-sphere strategy anchors the reference at the physical detector plane; no best-fit focus or defocus removal is used. The library's centroid weighting may trim image outliers; EE is centered on that reference, not guaranteed to maximize the energy box. No incoherent broadband MTF is fabricated from averaging MTF magnitudes. Geometric merit weights are equal across sampled colors; a source spectrum/QE is still unspecified.

At 550 nm, center X/Y MTF is approximately **0.438/0.438 at 50 lp/mm** versus matched limit **0.517**, and **0.207/0.207 at 100 lp/mm** versus **0.239**. Corner X/Y is **0.136/0.194 at 50**, **0.072/0.096 at 100**, and **0.044/0.068 at Nyquist**. Corner 2 x 2-pixel EE is approximately **0.111** versus **0.412** matched limit. These show substantial residual field aberrations rather than merely the red-edge diffraction cutoff.

At 800 nm the corner Nyquist MTF is about **0.023/0.024**, compared with the annular-pupil limit **0.0485**. An annular pupil redistributes contrast/energy, so the clear-pupil Run 005 reference is not interchangeable with this limit. No customer image-quality pass/fail limit exists.

Pupil sampling checks from 96 to 160 points across the diameter at center/550 nm and corner/800 nm change reported MTF by less than **0.0010 absolute**, and EE by less than **0.0010 absolute**. This checks those cases, not every field/wavelength. Both reference and actual PSFs are normalized to transmitted optical energy; coating transmission, detector MTF, polarization and scatter are not included in the claims.

## Reproducibility, costs and limits

Run 007 descends only from B04 Run 006. No Track A model or prescription is imported and reference/ is unread. `model.py` and source script are byte-matched; saved-model replay reproduces the result. `configuration.json`, `prescription.csv`, code and requirements preserve the model. Prescription materials are explicitly defined in code (mirrors, BK7/F2 lenses, air). `verification.json` records the replay, hash, lens-edge, grid-area and diffraction-convergence checks; `src/track_b_run007_audit.py` is its generator. Old runs are unchanged.

Spherical secondary metrology remains a B04 advantage; primary aspheric test, four small lens surfaces, large obstruction, spacing/centering sensitivity and the focus mechanism remain cost drivers. No tolerance or -25 to +50 C model exists yet. Broadband coatings, stray light and housing robustness remain unknown. No final Pareto ranking is justified.

Resource accounting: **two optimizer invocations** (joint physical solve and scalar finite refocus), **one materially distinct architectural attempt**, **two B04 screening attempts total including Run 006**. No plateau; three B04 attempts remain at this stage. Execution recorded about 4.10 seconds, with roughly ten minutes of model/API/verification engineering before closure, within workflow v3. Stop reason: the physical-pupil/first-order/nominal refocus question is answered; a different candidate now receives its own run.
