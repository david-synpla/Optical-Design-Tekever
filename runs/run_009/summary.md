# Run 009 — B06 independent off-axis TMA screen

Decision: advance B06 to development alongside both retained B05 variants. Close this bounded screen without further shape optimization. Track B remains open; Track A remains frozen and reference/ unread.

## Independence and recovery

The seed comes from original requirement-derived EFL/pupil, an independent three-power ABCD sweep with zero Petzval sum, and an off-axis entrance subaperture. It does not import any Track A prescription. A 132-seed inexpensive paraxial screen selected one geometry; one conic/focus solve produced the saved attempt. Three parent conics suffice for this screen; freeform escalation is not justified yet.

Quota interrupted work after the completed solve. On resumption, no optimizer remained running. The archived source hash and saved JSON passed; replay reproduced the original 1.321067 um RMS and 6.036865 mm clearance exactly. Python 3.14.4, Optiland 0.6.1 and SciPy 1.18.1 remain functional in the WSL environment. The completed shape solve was not repeated.

The finite-object verifier initially rejected one exact rim sample due to floating-point stop clipping. Moving finite-object pupil samples inward by 1e-9 of radius (0.064 nm) resolved this; no physical aperture or optical prescription was changed. The failed verification is procedural, not an optical candidate failure. The corrected verification completed successfully.

## Evidence and limits

| Quantity | B06 result |
|---|---|
| Parent paraxial EFL / physical entrance pupil | 794.202899 / 128.097242 mm; nominal f/6.2 |
| Local central X/Y image scales | 794.152366 / 794.209061 mm per radian |
| Dense infinity geometric audit | 25 signed fields, 65-grid physical disk; worst RMS 1.355534 um; all sampled rays survive |
| Physical clearance | 6.036865 mm minimum, tertiary-to-detector segment versus secondary; includes incoming path before entrance plane |
| 800 m detector-only refocus | +0.770896 mm along final beam; worst RMS 1.710303 um over 25 fields, 33-grid pupil |
| Parent-vertex axial span | 323.348486 mm; not a finished package dimension |
| Mirror patch diameters | 135.253 / 22.468 / 65.795 mm including assumed margins |

The virtual parent pupil is 358.097 mm only to launch rays through the displaced physical subaperture. It is not the collecting aperture and must not be used to claim f/2.2. Fourier sampling explicitly uses virtual-parent coordinates with the transmitted 128.097 mm disk. The matched ideal agrees with analytic clear circular f/6.2 MTF within 0.000909 absolute at all sampled frequencies/wavelengths. Increasing parent-pupil sampling from 256 to 384 changes sampled MTF by at most 0.001223 and 2-pixel EE by at most 0.000266 in the two checked cases.

Fixed-plane monochromatic scalar diffraction covers 430, 500, 550, 650, 725 and 800 nm at center, X edge, Y edge and both signed Y corners. X reflection symmetry supplies the opposite X fields. Frequencies are 50, 100, 150 and 182.482 lp/mm, plus 1/2/3-pixel ensquared energy. The minimum sampled MTF/matched-diffraction ratio is 0.8241. This is sampled evidence, not certification of the continuous field/band. All-reflective ideal geometry has no glass dispersion; actual coatings, polarization, scatter and detector window are absent. Source/QE-weighted broadband PSF/MTF remains outstanding.

At the positive corner at 550 nm, X/Y MTF is 0.779/0.758 at 50 lp/mm, 0.564/0.540 at 100 and 0.254/0.242 at Nyquist. Two-pixel EE is 0.756 versus matched ideal 0.791. B05 attempt 1 gives approximately 0.513/0.511, 0.235/0.234, 0.203/0.202 and EE 0.408. These are monochromatic comparisons with each architecture's own pupil; B06's advantage arises chiefly from unobscured collection, despite larger geometric RMS. They do not establish broadband transmission or a customer image-quality pass/fail threshold.

## Engineering comparison

| Trade | B06 assessment versus retained B05 |
|---|---|
| Manufacturability | Three custom off-axis conic patches; no stock powered optics demonstrated. Parent-sphere departures in manufacturing.json are not best-fit-sphere errors or fabrication tolerances. Supplier process/metrology review is required. |
| Alignment/metrology | Off-axis datums, mirror clocking and three-mirror alignment create additional engineering risk. Quantitative sensitivity and compensator analysis remain to be done. |
| Packaging | Approximately 323 mm vertex span, comparable to B05 baseline 329 mm, longer than B05 compact 283 mm. B06 is laterally asymmetric; the span alone cannot rank housing volume or mass. |
| Thermal | No refractive thermo-optic contribution in the ideal B06 prescription, but mirror substrates, structure expansion, gradients and refocus dominate an unmodeled problem. No -25 to +50 C qualification claim. |
| Robustness | Sampled self-clearance and physical-aperture survival pass. Mirror radius/slab margins of 2 mm and active-detector margins of 1 mm are assumptions. Cells, supports, detector electronics, baffles and finite-object nonincident clearance remain unverified. |
| COTS fraction | Zero identified stock powered elements in B06. B05 also uses custom optimized surfaces; catalog glass is not a stock finished optic. B01/B02/B03 remain COTS comparators. |
| Cost drivers | Engineering judgement: custom off-axis fabrication, test fixtures, datums and alignment likely dominate B06 nonrecurring cost. B05 retains axisymmetric manufacturing advantages but has two corrector lenses and their assembly/coating costs. No quotations or defensible currency estimates exist. |

Image quality, distortion, obscuration, mass, package size, transmission, stray light and tolerances remain engineering trades. The requirements are not expanded to turn these results into invented pass/fail limits. Field registration, distortion and edge coverage should be quantified during development rather than assuming paraxial focal length certifies exact active-field compliance.

## Stop and next step

The screen answers its engineering question: a fresh unobscured three-mirror candidate clears itself in the sampled model and earns a place in the portfolio. Preserve B06 and both B05 variants. Next use separate development runs for matched alignment/despace/decenter/tilt sensitivity, available compensators and thermal-material scenarios before more nominal shape optimization. Explicitly include detector-window and support/baffle integration. Do not collapse the portfolio to one winner from nominal RMS or Nyquist MTF.

Final resource ledger is closure.json. Three successful substantial searches (paraxial sweep, conic solve, scalar finite refocus), one B06 architecture attempt; one additional aborted refocus invocation is recorded conservatively as a fourth call. No plateau. Quota waiting did not reset the per-run limits. No new optical correction was supplied by the user.
