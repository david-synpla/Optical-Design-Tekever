# Run 020 — bounded C04 cost/COTS-maximized C1 experiment

## Decision

**C04 produces one conditionally non-dominated economic hypothesis, not an unconditional UAV product point.** Retain C04-N1400/B09: the preserved B09 EO channel plus a SWIR train using the hypothesized 353 mm / 1600 mm catalogue primary stopped to 311.371 mm, a catalogue 63 mm flat, two custom 50 mm spherical fused-silica/CaF2 elements and separately qualified SWIR coatings. It is the only tested point that combines exact first order, useful modeled image quality, catalogue large powered figures and small custom powered optics.

The condition matters. The reviewed Orion pages do not guarantee >=311.371 mm clear figured aperture; the stock Hilux coating has visible marketing data rather than a verified 0.8–1.8 um specification; and the 1.455 m optical structure is a poor UAV package. C04 is therefore **CONDITIONAL ACTIVE as an economic lane**, not selected over C01/C02 and not ready for C2 optical optimization.

No hard optical, mass, volume or cost threshold is invented. Catalogue prices are order-of-magnitude retail anchors, not quotations or predicted production cost.

## Market gates

The current Orion catalogue tabulates the donor hypothesis as 353 mm diameter, 1600 mm focal length, 39 mm edge thickness and 8.28 kg. The product page spans approximately GBP 1,265–1,840 excluding VAT across grade/secondary choices. Current 63/75/82 mm minor-axis flats are listed at roughly GBP 116/148/186 excluding VAT. These establish availability and price scale, not flight suitability, lot continuity or guaranteed clear aperture.

The Edmund 317.5 mm example is excluded because its specified clear aperture is only 286 mm. This confirms that nominal diameter cannot be used as a donor qualification rule.

Fully stock coating is not credited. Orion describes Hilux as an enhanced-aluminium visible coating but publishes no reviewed 0.8–1.8 um guarantee. Protected gold is a credible custom-coating class because the cited Edmund product specifies average reflectance above 96% over 700–2000 nm, but that does not establish availability or cost on the 353 mm paraboloid. The preferred branch is stock figured substrate plus qualified SWIR coating, ideally supplied uncoated or factory-coated if quoted. Stripping, surface damage, figure re-verification, large-chamber capacity, adhesion/environmental qualification, witness coupons and supplier warranty remain explicit risks.

The complete 350 mm CT14 OTA is not used. Its current approximately 26 kg, 1430 mm catalogue specification only confirms that the optical elements and mirror-cell technology exist. Run 020 replaces it with a purpose-built UAV bench/structure hypothesis.

## Bounded optical experiments

Five materially distinct attempts reached the normal run cap:

| Attempt | Large donor configuration | SWIR worst RMS radius | Sampled survival | EFL / f-number | Package consequence | Status |
|---|---|---:|---:|---:|---|---|
| N1220_F82_L70 | Stock primary + 82 mm flat + two 70 mm lenses | 13.83 um | 89.0% | 1930.488 mm / 6.19996 | 240 L straight | PARKED: flat is 2.31 mm undersized by beam/field screen |
| N1300_F75_L60 | Stock primary + 75 mm flat + two 60 mm lenses | 10.18 um | 90.0% | 1930.342 mm / 6.19949 | 255 L straight | Preserved compact placement checkpoint; first-order miss and capped solve remain |
| **N1400_F63_L50** | **Stock primary + 63 mm flat + two 50 mm lenses** | **9.22 um dense** | **93.55% dense** | **1930.50184 mm / 6.1999997** | **273 L straight** | **Retained C04 economic point** |
| C350_CAS_B80 | Stock primary + custom powered secondary | 10.08 um dense | 74.61% dense | 1930.502 mm / 6.2 | 183 L | PARKED: 158 mm, K=-133 secondary and primary perforation/return-fold burden |
| N1400 single lens | Stock primary + 63 mm flat + one 50 mm fused-silica lens | 24.26 um | 96.5% | 1930.483 mm / 6.19994 | 273 L | PARKED: custom reduction does not compensate performance/package loss |

The retained N1400 prescription has four custom spherical corrector surfaces with healthy modeled lens edges of 5.26/6.94 mm and 6.00 mm edge air gap. Its 63 mm flat has 12.19 mm beam/field margin. A 10x40 to 16x64 pupil replay changes worst RMS by 0.44%; the 93.55% dense survival includes the flat/spider shadow. Infinity-to-800 m detector refocus is 4.648 mm and gives 7.82 um worst sampled RMS at 800 m. Two channel focus mechanisms remain.

All three two-lens solves and the one-lens solve stopped at their 60-evaluation caps. They are bounded checkpoints, not converged optima. The custom-secondary solve converged in nine evaluations. No sixth rescue attempt was opened.

## Complete UAV package comparison

The retained common-bench B09/N1400 screen is approximately **512 x 367 x 1455 mm, 273.4 L**. The 512 x 367 mm front face includes a 367 mm donor cell and 141 mm EO cell with a structural web. A mid-path fold does not rescue it: the converging beam requires an approximately 262 mm tilted flat, whose solid proxy is 3.11 kg; the resulting 1006 x 367 x 775 mm box is 286.2 L. That fold is parked because it adds volume, coating, alignment and a large qualified optic.

The mixed optical-mass estimate is about 8.84 kg, dominated by the donor primary's catalogue 8.28 kg. It adds geometric flat/lens and B09 mirror proxies but excludes cells, focusers, detectors, electronics and structure. It is directionally worse than the C01 5.74 kg and C02 5.09 kg solid-mirror proxies, though the bases are not identical. A simple open-truss/common-bench area proxy is 0.96–1.30 m2, versus 0.455–0.602 m2 for the current C01 comparator.

The uniform-box vertical-axis specific-inertia proxy is 0.1983 m2 per unit mass, versus 0.0350 for C01 and 0.0503 for the normalized C02 screen. The 8.28 kg primary at one end of a 1.455 m structure also creates a strong CG/balance burden; real electronics placement or counterbalancing must be modeled before gimbal sizing.

At the 258 mm screened channel baseline and 800 m, parallax is 322.5 urad: 93.5 EO or 62.3 SWIR pixels. As with C01, this is primarily registration burden: the complete 5.304 x 4.243 m SWIR field remains inside the 11.305 x 8.280 m EO field, so simultaneous SWIR overlap is 100% in the planar calculation.

| Comparator | Screened volume | Largest dimension | Principal advantage over C04 | Principal disadvantage versus C04 |
|---|---:|---:|---|---|
| C01 B05-1/S16 | 68.2 L | 470 mm | Compact, optically mature, lighter proxy, channel coatings | More custom large powered optics/NRE hypothesis |
| C02-A6F1 normalized | 79.7 L | 700 mm | Common LOS, smaller front, lower mirror proxy | Obscuration, annular f/1 primary, unproved multi-element cameras |
| **C04-N1400/B09** | **273.4 L** | **1455 mm** | Catalogue large powered figures; small spherical custom corrector | Long/heavy structure, parallax, coating and supplier gates |

C04 does not dominate the UAV package. Its only current Pareto basis is potentially lower large-optic procurement and NRE. That advantage is plausible rather than proved.

## Economic continuum

- **Stock primary + stock flat + two small custom lenses:** retained conditional point. This is the best numerical use of the donor.
- **Stock primary + stock flat + one custom lens:** parked; lower custom count costs substantial image quality without saving package.
- **Stock primary + custom secondary:** parked; a 158 mm extreme-conic secondary and donor-hole/return-fold modification erase much of the stock advantage.
- **Stock figured primary + stock Hilux coating:** unscored for SWIR because no suitable spectral guarantee was found.
- **Stock figured primary + custom protected-gold-class coating:** preferred coating hypothesis, conditional on quote and qualification.
- **B09 EO + donor SWIR:** preferred economic system combination; approximately 7.97 um EO and 9.22 um SWIR dense RMS.
- **B05-1 EO + donor SWIR:** preserved module option where EO performance matters, but it raises custom content without improving the donor-dominated package.

C04 likely reduces custom large powered-figure NRE relative to C01/C02. It still requires a custom corrector/barrel, large-mirror SWIR coating, long precision metering structure, two channel focus interfaces, boresight calibration and full airborne qualification. Recurring complexity is therefore moderate/high rather than demonstrated low. Supplier concentration is high because only one qualifying 350/1600 donor source has been identified and its clear aperture, substrate/lot controls and replacement terms remain unknown.

## Portfolio consequence and next experiment

- **C01:** ACTIVE practical comparator.
- **C02-A6F1:** CONDITIONAL ACTIVE.
- **C03:** PARKED.
- **C04-N1400/B09:** CONDITIONAL ACTIVE economic lane; not a selected product.
- **C05:** PARKED.

Before further prescription optimization, the next useful work is a bounded cross-portfolio C1 closure/RFQ-readiness run: normalize C01/C02/C04 detector-window, coating, structure and production-quantity assumptions, and prepare exact supplier questions for donor clear aperture, figure/roughness, substrate/lot continuity, uncoated/custom-gold supply, corrector tolerances and flight qualification. If that gate supports C2 optical development, the largest remaining optical uncertainty is a real three-element C02-A6F1 backend plus folded package.

## Resource use and integrity

Five materially distinct optimizer attempts used 249 evaluations total; four hit their bounded 60-evaluation caps and the custom-secondary attempt converged in nine. The 800 m focus check used 16 scalar evaluations, with two dense replays. Observed WSL process time was approximately 180 s plus reporting and integrity checks. No dependency was installed and no repeated rescue solve was started.

`reference/` was not accessed. Track A/B prescriptions and Runs 016–019 were not modified. Run 020 closes here.
