# Current Design State

Track: B — independent research-informed optical design
Stage: independent B06 screen complete; B05 and B06 retained for development
Workflow: v3; Track B remains OPEN, not frozen.
Track A: FROZEN at b06af2c3b6c3e7bec4e4bf5b57f9249207d8a875; tag track-a-frozen. Its results remain immutable. reference/ remains unread.

## Portfolio

| ID | Architecture | Status | Best evidence / decision |
|---|---|---|---|
| B01 | C5 + stock reducer | ACTIVE comparator | Run 005; close nominal geometry but exact mismatch, spectral/thermal behavior unmeasured |
| B02 | Nikon 800/6.3 | ACTIVE comparator | Run 005; EFL/f-number mismatch, detector interface and band/temperature testing outstanding |
| B03 | Retained SCT optics/custom mechanics | ACTIVE comparator | Run 005; does not itself fix B01 optical geometry; integration trade remains unverified |
| B04 | Spherical-secondary CDK + two-lens corrector | PARKED | Run 007 restores nominal EFL/f/6.2 and physical pupil; 7.445 um worst sampled RMS; retains simpler secondary/metrology trade |
| B05 | Co-designed two-conic Cassegrain + two-lens corrector | ACTIVE — advance to development | Run 008: retain attempt 1 as lower-risk baseline and attempt 2 as compact alternative; both independently seeded from requirements |
| B06 | Off-axis three-conic TMA | ACTIVE — advance to development | Run 009: independent seed; 1.356 um dense RMS, unobscured pupil, 6.037 mm screened clearance; custom off-axis fabrication/alignment risks |
| B07–B14 | Corrected RC; custom SCT; Newtonian/relay; Maksutov; APO; flat-medial aplanat; freeform escalation; Canon COTS | PARKED | Individual trade/reopening reasons in Run 005; no blanket family rejection |

## Current numerical evidence

Both B05 variants meet 550 nm paraxial EFL 794.202899 mm with 128.097242 mm entrance pupil, nominal f/6.2. Six-wavelength/nine-field worst geometric RMS is 0.799 um (attempt 1) and 0.576 um (attempt 2). Denser 17-wavelength/25-field uniform-pupil audits give 0.844 and 0.682 um respectively; these use different spectral-centroid weighting and sampling.

At 550 nm corner, B05 attempt 1 has X/Y MTF 0.513/0.511 at 50 lp/mm, 0.235/0.234 at 100 and 0.203/0.202 at Nyquist. Attempt 2 gives 0.513/0.513, 0.237/0.237 and 0.208/0.208. Corner 2x2-pixel EE is 0.408 and 0.411 versus matched-pupil ideal about 0.412. These are monochromatic fixed-plane scalar results; source/QE-weighted broadband PSF/MTF is not yet computed.

Both retain about 69.3% geometric pupil area, with no additional clipping in the sampled field. No spider, actual baffles or coating throughput is included. B05 attempt 1 vertex span is 329.04 mm; attempt 2 is 283.37 mm. These are not finished housing sizes.

800 m detector-only refocus is +0.78958 mm / +0.79314 mm, with six-color/nine-field worst RMS 1.017 / 1.699 um. Mechanisms remain undesigned. Spectral EFL ranges about 794.202–794.334 mm / 794.196–794.362 mm; no tolerance permits claiming exact full-band compliance.

## Engineering trade and remaining limits

B05 attempt 2 has a smaller conic magnitude but a tighter secondary curvature: its vertex-sphere departure is 38.80 um versus 14.66 um for attempt 1, and its despace sensitivity is worse. Both variants are worth retaining; nominal RMS alone should not pick the winner. Attempt 1 is the provisional engineering baseline. B04 is parked as a simpler spherical-secondary comparator, not rejected as an architecture.

No customer limits exist for image quality, distortion, obscuration, package, mass, transmission, stray light or tolerances. Aperture dimensions, merit weights, perturbations and equal sampled wavelength weighting are explicit benchmark assumptions. All candidates still lack -25 to +50 C thermal qualification/modeling, tolerance allocation, actual coating/substrate/cell choices, sensor cover-glass integration and stray-light validation. Track B cannot yet be frozen.

## Resource accounting and next work

Run 007: two optimizer calls, one distinct B04 attempt; B04 screening lifetime total two of five. Run 008: four optimizer calls, two distinct B05 attempts; B05 total two of five. Neither branch plateaued. Final Run 008 ledger is closure.json; its root metadata.json preserves initial-attempt execution only. Both runs closed after their engineering questions were answered, within the 30-minute/10-search limits. No quota percentage inferred.

Run 009 closed after quota-recovery verification. Completed shape solve replayed exactly; full explicit-pupil, diffraction and 800 m refocus checks pass. B06 nominal EFL/pupil are 794.202899/128.097242 mm. Dense 25-field RMS is 1.356 um, screened clearance 6.037 mm, vertex span 323.35 mm. At 550 nm positive corner, MTF X/Y at 100 lp/mm is 0.564/0.540 and 2-pixel EE 0.756 versus matched ideal 0.791. Finite 800 m refocus is +0.770896 mm along final beam with 1.710 um dense RMS. No broadband or thermal compliance claimed. See runs/run_009/summary.md and closure.json.

Next: separate bounded development runs for matched B05/B06 tolerance, alignment compensators and thermal-material scenarios; include detector window and physical supports. Preserve both B05 variants and B06. No further nominal shape search is justified before these engineering comparisons.

Human intervention: user authorized continuation on 2026-09-06; no new optical corrections. Autonomous engineering finding: reducing conic magnitude did not reduce actual aspheric departure or sensitivity. Track A geometry was not reused. Initial milestones remain 1734bcc (Track B initialization), 9f5dd0c (broad screen), b4b854d (B04 seed); Run 007 committed at 90428e2.

Recovery intervention: user requested resumption after quota interruption on 2026-09-07. No completed shape solve repeated; corrected only floating-point rim sampling in finite-object verification. Track A remains untouched; reference/ remains unread.
