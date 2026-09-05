# Current Design State

Track: B — independent research-informed optical design
Stage: broad architecture gate complete; first B04 seed screened; workflow v3
Track A: FROZEN at b06af2c3b6c3e7bec4e4bf5b57f9249207d8a875. Seven freeze hashes verified; Runs 001–004 and freeze artifacts unchanged. reference/ remains unread.
Initialization milestone: 1734bcc. Broad architecture screening milestone: 9f5dd0c.

## Candidate portfolio

| IDs | Family | Status | Evidence / next gate |
|---|---|---|---|
| B01 | C5 + stock reducer | ACTIVE comparator | Run 005: close nominal geometry, not exact; real band/field/thermal measurements needed |
| B02 | Nikon 800/6.3 | ACTIVE comparator | Run 005: EFL and maximum f/# mismatch; detector/electronic interface and optical measurements needed |
| B03 | Retained SCT optics/custom mechanics | ACTIVE comparator | Run 005: rehousing does not fix B01 optical mismatch; retain only if integration trade earns it |
| B04 | Independently co-designed CDK | ACTIVE screening | Run 006: 7.30 um worst unclipped RMS, 792.62 mm image-scale estimate; physical model and EFL restoration next |
| B05 | Co-designed Cassegrain + relay | ACTIVE for screening | Run 005: independent model in its own future run; no prescription yet |
| B06 | Off-axis conic/aspheric TMA | ACTIVE for screening | Run 005: independent first-order/clearance screen in its own future run; no prescription yet |
| B07–B14 | RC/corrector; custom SCT; Newtonian/relay; Maksutov; APO; flat-medial aplanat; freeform escalation; Canon COTS | PARKED | Run 005 comparison records individual costs/risks and reopening reasons; no blanket rejection |

These are provisional development branches. No demonstrated Pareto frontier or compliant final candidate exists. Preserve candidates only when meaningful trade advantages survive verification.

## Established findings

Original requirements imply 794.2029 mm EFL and 128.0972 mm pupil at f/6.2, active field 0.809645 x 0.593006 deg. No customer tolerance is supplied for the small difference from rounded 0.81 deg. The specified band, flat detector, 800 m focus and -25 to +50 C remain the baseline. Image quality, mass, package, distortion, obscuration, transmission, stray light and tolerances remain trade variables.

Run 005 calculates six-wavelength diffraction references at 50/100/150/182.48 lp/mm and 1/2/3-pixel ensquared energy. These are ideal clear-pupil references, not candidate performance. Nikon cannot simply open from maximum f/6.3 to f/6.2; tuning SCT EFL cannot also enlarge its 127 mm pupil.

B04's independently derived ellipsoid/spherical-secondary/two-lens seed improved to 7.298 um worst common-centroid RMS. A preliminary mask gives 7.890 um worst monochromatic centered RMS; the metrics differ and are not directly comparable. Candidate diffraction MTF/EE remains uncomputed pending explicit physical pupils. Provisional 68.84 mm secondary, 40.42 mm primary hole, 71.12% clear area before other losses, positive lens edge thicknesses and 408.45 mm vertex span are screening estimates. Several variables reached bounds. Nominal EFL is still about 0.20% low; full compliance is not established.

## Resource status and next action

Run 005: zero optimizers; broad comparison question answered and closed.
Run 006: one substantial optimizer, one materially distinct B04 screening attempt; no plateau. Approximately 14.26 seconds recorded solve/initial-audit wall time plus several minutes of engineering. Closed at the seed-feasibility decision; five-attempt B04 screening allowance has four remaining, not reset by a new run.
Per-run limits remain about 30 active minutes / 10 substantial searches; candidate-stage cap five, plateau after three consecutive materially distinct non-improving attempts. No account quota percentage inferred.

Next: bounded B04 physical-pupil and EFL-restoration investigation, then separate B05/B06 screens. Include matched-pupil diffraction metrics and finite-conjugate assessment before promotion. All candidates still lack temperature verification; no final Track B freeze or reference access is justified.

Human intervention: user authorized the Track B transition, supplied research and diffraction-aware evaluation guidance. These are recorded methodological inputs, not autonomous discoveries. No subsequent human optical corrections. Autonomous corrections: Optiland CSV geometry uses k for the conic; failed export recovered without rerunning optimization. See runs/run_006/summary.md.
