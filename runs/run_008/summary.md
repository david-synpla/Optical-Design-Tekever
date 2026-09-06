# Run 008 — independent B05 Cassegrain/corrector competition

Decision: advance **B05 to development**, retaining two genuinely different parameter variants. Attempt 1 is the preferred engineering baseline for now; attempt 2 is the shorter, more demanding alternative. Park B04 as the spherical-secondary comparator. Neither B05 variant is production-ready or frozen. B06 remains worth its own inexpensive screen because an unobscured pupil could recover contrast/energy currently lost to obstruction.

## Independent seed and controlled comparison

B05 started from primary f/2.4, 85 mm backfocus, a parabolic primary and classical Cassegrain secondary conic derived from secondary magnification, plus weak separated BK7/F2 lenses. These are documented seed assumptions derived afresh from the TEKEVER first-order requirements. No B04 optimized prescription, Track A prescription or reference/ content seeded it. The reusable physical-pupil/analysis implementation and common aperture sizes were shared with Run 007 for a controlled comparison. B05 releases both mirror conics and the axial position of the two-lens corrector group; this is co-design, not a corrector appended to a frozen mirror pair.

Both variants retain the 128.097 mm entrance pupil and enforce 550 nm paraxial EFL 794.202899 mm, nominal f/6.2. The same 35.5 mm obstruction radius, 66.5 mm primary radius, 21.5 mm primary hole and 17.5 mm lens radii are engineering screening assumptions, not customer limits. No aperture is shrunk by the optimizer to conceal aberrations.

## Comparison

| Metric | B04 Run 007 | B05 attempt 1 | B05 attempt 2 |
|---|---:|---:|---:|
| Six-wavelength/nine-field worst RMS, um | 7.445 | 0.799 | 0.576 |
| Denser 17-wavelength/25-field uniform-pupil worst RMS, um | Not repeated | 0.844 | 0.682 |
| Entrance-to-image vertex span, mm | 412.45 | 329.04 | 283.37 |
| Secondary radius, mm | -929.66 | -541.90 | -310.48 |
| Secondary conic | 0 | -11.9997 | -5.9998 |
| Secondary departure from vertex-radius sphere, um | 0 | 14.66 | 38.80 |
| Primary departure from vertex-radius sphere, um | Not evaluated here | 7.35 | 13.34 |
| Worst center/corner RMS after either sign of 10 um secondary despace, um | 9.53 | 3.98 | 5.49 |
| Detector refocus for 800 m, mm | +0.78875 | +0.78958 | +0.79314 |
| Nine-field/six-color worst RMS after 800 m refocus, um | 7.382 | 1.017 | 1.699 |

The denser audits change field/pupil/spectral sampling and spectral-centroid weighting, so their numbers should not be used as a direct optimizer-improvement ratio. Both B05 variants retain positive lens edge thicknesses; attempt 2 has 3.02/5.37 mm edges and at least 14.56 mm inter-lens gap. Both dense audits retain approximately 69% of the full pupil, with no additional sampled field clipping. No coating throughput or detailed mechanical-envelope claim follows from these figures.

Attempt 2 was motivated by capping the secondary conic at -6, a manufacturing hypothesis. **That hypothesis did not hold as a simple cost improvement:** the tighter curvature increased actual secondary departure and slope (38.80 um / 4.31 mrad versus 14.66 um / 1.63 mrad), and despace sensitivity worsened. Its optical improvement and 45.7 mm shorter span nevertheless make it a meaningful alternative. A lower-magnitude conic is not inherently a cheaper asphere. Departures are relative to the vertex-radius sphere, not best-fit sphere or allowable figure errors. No vendor metrology/cost quote is available.

## Diffraction and spectral evidence

Monochromatic scalar FFT uses the same real pupil amplitude as its zero-phase reference, at one fixed detector plane. At 550 nm corner:

- Attempt 1 X/Y MTF: **0.513/0.511 at 50 lp/mm**, **0.235/0.234 at 100**, **0.203/0.202 at 182.48**. Its 2 x 2-pixel EE is **0.408**, matched reference **0.412**.
- Attempt 2 X/Y MTF: **0.513/0.513 at 50**, **0.237/0.237 at 100**, **0.208/0.208 at 182.48**. Its 2 x 2-pixel EE is **0.411**, matched reference **0.412**.

Across the four diffraction fields, six wavelengths and four reported frequencies, the minimum actual/matched MTF ratio is about **0.940 for attempt 1**, and **0.998 for attempt 2**. These are sampled **monochromatic** results, not a broadband MTF guarantee or continuous-field qualification. Finer-pupil checks differ by at most about 0.0014 absolute across MTF/EE in the checked center/550 nm and corner/800 nm cases. Numerical differences below that scale should not decide the portfolio.

The reference pupil is centrally obscured: it has only about 69.28% geometric area and a materially lower low-frequency diffraction limit than a clear aperture. Near-ideal performance for that pupil does not mean perfect clear-aperture performance. At 800 nm Nyquist, attempt 1 corner MTF is approximately 0.0477 versus its matched limit 0.0478; optimizing this frequency alone would obscure the more useful multi-frequency trade.

Separate infinitesimal-ray EFL checks across 17 wavelengths give approximately **794.202–794.334 mm** for attempt 1 and **794.196–794.362 mm** for attempt 2. The 550 nm target is restored exactly to numerical precision, but chromatic image scale remains nonzero. No customer EFL/IFOV tolerance was supplied, so do not claim exact full-band first-order compliance. Full-band geometric metrics use one common image plane/centroid; no independently focused wavelengths or averaged MTF magnitudes are used. Source/QE weighting and a combined broadband PSF/MTF are still pending.

## Manufacturing, robustness and remaining work

B05's two custom conic mirrors plus four spherical lens surfaces buy a large flat-field improvement over the screened spherical-secondary B04. The larger secondary-asphere test burden and stronger despace sensitivity are material cost/robustness penalties. Attempt 1 currently offers the more forgiving B05 trade with already strong diffraction performance; attempt 2 earns preservation through shorter packaging and improved nominal image quality, at greater shape/alignment burden. These are engineering judgments, not monetary quotations or customer limits.

The +/-20 um detector and +/-10 um secondary changes are diagnostic perturbations, not proposed manufacturing tolerances. They keep all other vertices fixed and do not compensate by refocus. Neither candidate has thermal modeling across -25 to +50 C, glass dn/dT treatment, a tolerance allocation, actual mirror substrates/coatings, a focus mechanism, spider/baffles, sensor cover glass, detector package or stray-light validation. Independent OpticStudio validation is still pending. Cost depends on these unfinished items, not just element count.

## Reproducibility and run closure

Root-level Run 008 numerical files preserve attempt 1. `attempt_02/` preserves the second variant separately; no attempt-1 result was overwritten. Root `metadata.json` records the initial attempt execution; **`closure.json` is the final run ledger** including both variants and both finite-refocus solves. `model.py` is the exact primary script; secondary scripts and source dependencies are committed. Code plus configuration are authoritative; attempt 2 also has a material-explicit CSV. Earlier runs remain immutable.

Saved-model replays, file hashes, JSON parsing, lens thicknesses, uniform-pupil vignetting, selected diffraction convergence and dense spectral/field checks pass. Seed-probe FFT values were not used as evidence: that highly aberrated starting state can alias on a coarse grid. Final performance claims use the optimized, convergence-checked models.

Resources: **four optimizer calls** (two shape solves and two scalar finite-refocus solves), **two materially distinct B05 screening attempts**. No plateau; both attempts made meaningful optical or packaging progress. Shape solves plus their first analysis stages recorded about 80.0 s and 58.3 s; overall engineering stayed below the 30-minute run limit. No third shape attempt is justified before comparing the remaining architecture and engineering risks.

Next useful action: a separately bounded **B06 off-axis reflective geometry/clearance screen**, with independent first-order construction, to determine whether removing obstruction justifies its fabrication and alignment burden. Preserve B05 for subsequent thermal/tolerance development. No final Track B freeze or reference access is warranted.
