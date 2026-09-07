# Run 012 — B09 cost-conscious hybrid development

**Decision: retain B09 as a provisional economical hybrid option alongside B05 and B06.** It has a credible traced nominal and a useful cost/manufacturing hypothesis, with a substantial corner-image-quality penalty. It is not qualified or proven cheaper in production. B01/B03 remain empirical COTS alternatives with unverified optical performance, not low optical scores.

Run013 thermal work took priority: this run paused after the in-flight solve and resumed verification after the thermal milestone was committed and pushed. Original solver output and invalid preliminary verification remain preserved.

## Prescription and requirement evidence

The independently seeded nominal uses a stock-like 130 mm, 650 mm focal-length paraboloid (R=-1300 mm, K=-1), a 47 mm minor-axis flat, and two 35 mm-diameter custom spherical N-BK7/N-F2 lenses. Entrance pupil 128.097242 mm; effective focal length 794.202541 mm; f/6.199997. The four lens curvatures and three separations were solved; no Track A, B05 or B06 geometry was used as a seed.

Dense 25-field, six-wavelength 430–800 nm tracing with 2304 equal-area pupil rays gives worst RMS **7.972 um**. At 800 m it is **7.897 um**, after **0.8123 mm** added image-path focus. The focus search converged; the nominal shape solve reached its 120-evaluation cap, so its saved geometry is a bounded checkpoint, not a converged optimum.

Central polychromatic angular image scales are 794.182/794.182 mm. At the source angular corners, centroid overrun relative to the fixed active rectangle is 10.47/7.67 um in X/Y. Thus paraxial EFL agreement does not close exact active-field registration. No distortion or image-quality acceptance threshold was invented.

The sampled intentionally transmitted pupil fraction is 0.8594–0.8750; additional clipping of those clear rays is 0.0000. This includes a field-dependent ideal flat shadow and four 0.5 mm spider vanes. Real substrate edges, hub, cell, tube and detector housing are not yet modelled. Expected throughput is this geometric factor times two mirror reflectances, four lens-surface transmissions, glass and window transmission; actual spectral coating data is missing.

## Diffraction-aware performance comparison

Common nominal infinity focus; 550 nm positive detector corner below. MTF values are X/Y at the stated frequencies. Each EE is actual / its own transmitted-pupil diffraction limit. These are monochromatic metrics at common focus, not averaged-MTF broadband claims. B09 uses a 384-point pupil grid (768 convergence checks); comparison designs use archived Run010 nominal data.

| Candidate | Dense nominal RMS, um | MTF50 | MTF100 | MTF150 | MTF Nyquist | EE 2x2 actual / ideal |
|---|---:|---:|---:|---:|---:|---:|
| B09 | 7.972 | 0.368/0.297 | 0.053/0.072 | 0.019/0.032 | 0.025/0.025 | 0.225/0.590 |
| B05-1 | 0.800 | 0.512/0.510 | 0.234/0.233 | 0.183/0.183 | 0.203/0.202 | 0.407/0.411 |
| B05-2 | 0.576 | 0.515/0.515 | 0.237/0.237 | 0.188/0.188 | 0.208/0.208 | 0.411/0.411 |
| B06 | 1.360 | 0.779/0.758 | 0.563/0.540 | 0.367/0.351 | 0.253/0.243 | 0.756/0.791 |

B09 retains useful center performance but gives up considerable corner contrast and energy concentration. At 430/550/800 nm its corner metrics are saved separately in diffraction.json; it is not judged from Nyquist alone. The nominal RMS is about 10x B05-1 and 5.9x B06, while energy/contrast losses are less directly related to those ratios. Keep it because fewer custom optics and simpler mirror tests may justify that sacrifice; customer utility and supplier quotations remain necessary.

## Manufacturing, packaging and sensitivity

Two of four optical elements are stock-nominal mirrors; one of three powered elements is COTS. Four custom powered surfaces are spherical, compared with B05's two custom conic mirrors plus four lens surfaces, or B06's three custom off-axis conic mirrors. The 35 mm lens edge thicknesses are 6.011/2.022 mm; the inter-lens edge gap is 0.485 mm. That misses the solver's soft 0.5 mm assembly target slightly; it is not a customer requirement, and must be reconciled with a real spacer/drawing before release.

The primary-to-flat axial distance is 480 mm, first lens lies 100.690 mm outboard, and detector lies 188.186 mm outboard. This is a long side-exit layout rather than a compact B05 replacement. Those are optical locations, not housing dimensions or mass. A stock OTA is a procurement source; custom cells, spider, barrel and detector mechanics are still required.

Six one-at-a-time diagnostics are in sensitivity.json: +/-0.1% primary radius, +/-100 urad flat tilt and +/-10 um first-lens decenter. They are assumed perturbations, not supplier tolerances. Radius error needs roughly +/-0.97 mm focus and recovers near 8 um RMS. Flat tilt and lens decenter leave centered RMS near 8 um, but pointing and detector registration are not compensated or qualified. This is much narrower evidence than Run010 and must not be presented as equal robustness maturity.

Stock substrate, long support CTE, spider thermal gradients, lens dn/dT, window and cell stress remain unverified for B09. The completed B05/B06 Run013 study shows why a material/support choice and range-plus-thermal focus allocation are needed; its numbers are not transferred to B09.

## Provisional economic portfolio

Relative classes below are engineering judgement from custom optical count, test difficulty and integration effort; they are not prices, schedules or production-yield forecasts. The labels describe potential products, not a forced three-winner outcome.

| Dimension | B09 economical hybrid | B05 balanced custom, variants retained | B06 higher mid-frequency/EE performance | B01/B03 stock-SCT route |
|---|---|---|---|---|
| Procurement / recurring cost | Potentially low/moderate; stock mirrors plus two small custom lenses | Moderate/high custom optical set | High-risk off-axis mirror manufacture and metrology | Low/moderate stock set; production terms unknown |
| NRE | Moderate corrector and custom mechanical package | Moderate/high custom mirror tests and corrector/cells | High alignment, off-axis datums, test fixtures and cells | Low bench characterization initially; rehousing can raise it |
| Alignment / manufacture | Familiar paraboloid and flat tests; lens centration/collimation | Coaxial but custom secondary metrology; focus comparatively forgiving | Three off-axis conics; coupled pointing/alignment controls | Preserve factory matched optics and datums; moving-primary shift/backlash risk |
| Integration / packaging | Long axial path and lateral detector; spacer clearance open | More compact; high obscuration, real cell/window open | Unobscured beam with packaging clearance evidence; real body/cells open | Compact catalogue assembly; detector/reducer geometry and qualification open |
| Thermal / schedule risk | Not yet modelled; stock lot and substrate/coating data missing | Uniform-temperature scenarios available; real structure/window pending | Uniform-temperature scenarios available; support mismatch more demanding | Proprietary model absent; physical bench and chamber evidence needed |
| Optical evidence / sacrifice | Modelled ~8 um worst RMS and reduced corner MTF/EE | Modelled ~0.6–0.8 um with strong high-frequency trade | Modelled ~1.36 um with higher mid-frequency/EE, not all-frequency winner | IQ presently unverified; disclosed pupil/EFL mismatch is a separate fact |

Current procurement anchors were checked on 2026-09-07 in Run011: the Sky-Watcher donor OTA is GBP229, while a replacement primary-only offer is EUR70.65; neither is a qualified production BOM. The C5/reducer stock subtotal is USD879.90; Nikon complete-lens offer GBP4,999. These original-currency retail anchors exclude custom optics, mechanics, coatings, acceptance tests, landed cost and qualification. See [Run011 procurement sources](../run_011/summary.md).

RFQ package needed next: measured primary/flat set (substrate, radius, figure, roughness, coatings, lot continuity); two spherical lenses with drawings, centration and broadband coatings; mirror cells/spider/relay barrel and range-plus-thermal focus mechanism; matching B05 and B06 optic/test-fixture packages at common quantities. No RFQ was sent and no purchasing action was taken.

B01/B03 must be evaluated with supplier data or assembled-system measurements before rehousing. Missing proprietary prescriptions mean unverified performance, not poor performance. Retaining factory datums can preserve the economic argument; custom optical compensation without a model or measured system identification could erase it. The exact 127 mm aperture/EFL mismatch remains unresolved independently of image quality.

## Corrections, resource use and next step

Physical fold mapping agrees within 2.8e-13 mm and has matching sampled survival. The initial folded helper incorrectly relied on negative refractive index instead of Optiland's reflection flag; fixed in verified_model.py. More significantly, the initial entrance plane crossed the parabolic sag, creating backward OPL segments and invalid FFT values. Moving that numerical stop 4 mm ahead of the vertex restores forward propagation (minimum 2.424 mm) and plausible on-axis 550 nm OPD RMS 0.097 waves. Powered radii, conics and their separations remain unchanged. Original solver model and before_opl_correction/ outputs are audit-only and must not be used for diffraction ranking.

After correction the 384-to-768 pupil convergence change is at most 0.00222 in MTF/EE. Reproduction: use verified_model.py plus verification.py and the saved parameters. The original model.py preserves the solve history. Requirements are unchanged; implementation corrections are not customer requirement changes.

One nominal shape attempt (evaluation cap reached); one final finite-focus solve plus its preserved pre-correction repeat; bounded dense/fold/FFT and six sensitivity diagnostics. No new architecture or second nominal optimization was started. Active engineering time is conservatively estimated below 25 minutes excluding the Run013 priority pause; no plateau claim is warranted from one attempt.

Next most useful action: define a shared detector/window, range-plus-thermal focus and mechanical datum specification, then apply a bounded B09 thermal/support/interface check using measured or explicitly bracketed stock material properties. Obtain supplier/bench evidence before claiming production economics or freezing the portfolio. Track B remains OPEN; its low-cost gate is advanced, not declared fully qualified.
