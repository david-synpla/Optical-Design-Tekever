# Current Design State

Track: A - autonomous / uninformed
Stage: architecture exploration complete; portfolio verification/freeze remains outstanding
Workflow: v3 active after Run 002
Track status: architecture exploration closed after Run 004; no blind candidate is frozen. Do not open another architecture family without explicit user instruction.

## Candidate portfolio

| ID | Architecture / genealogy | Status | Best evidence | Main strength | Main risk |
|---|---|---|---|---|---|
| A01 | On-axis two-conic-mirror Cassegrain-type baseline | PARKED | Runs 001-002 | Compact, achromatic, approximately 794.2 mm EFL and f/6.2; remains viable | Flat-field image quality and detector-Nyquist MTF are weak; substantial obscuration and strong secondary conic |
| A02 | A01 derivative with 4 mm fused-silica near-focus singlet | REJECTED | Run 002 | Modest corner improvement | Degrades the center, adds chromatic dependence and does not justify two added surfaces/cell complexity |
| A03 | A01 derivative with 5.5 mm cemented N-BK7/N-F2 corrector | REJECTED | Run 002 | Improves portions of the middle field | Worst-field performance remains weak; three refracting surfaces, two glasses and cemented-interface burden are unjustified |
| A04 | Coaxial three-mirror anastigmat branch | REJECTED | Run 003 | Nominal seed suggested improved flat-field performance | Three distinct physical-clearance attempts plateaued; centered detector obstructs the pre-tertiary beam |
| A05 | All-refractive long-focus family screened as scaled doublet, triplet and multi-element telephoto | REJECTED | Run 001 | Unobscured conventional optical path | Approximately 0.1-0.2 mm band-edge RMS spots plus unfavorable length, glass mass and thermal behavior |
| A06 | Off-axis/decentered three-mirror reflective branch derived from the A04 topology finding | PARKED | Run 004 | A tilted tertiary can remove the sampled detector/beam conflict | No screened prescription combines credible clearance with a flat-field benefit over A01; extra alignment/metrology and package burden is unjustified |

No candidate is currently `ACTIVE` or `FROZEN`. A06 is not promoted to development. A01 remains the preserved baseline. Track A architecture exploration is complete; this is not a claim that the full track verification or blind portfolio freeze is complete.

## Established conclusions

- Explicit customer requirements remain those in `requirements/eo_requirements.yaml`; no customer image-quality, distortion, obscuration, package, mass, transmission, stray-light or tolerance limits were supplied.
- Derived first-order targets are approximately 794.2 mm EFL, 128.1 mm entrance pupil at f/6.2, and 0.8096 deg x 0.5930 deg active-array field.
- A01 achieved approximately 3.4-3.7 um on-axis and 8.4-8.8 um sensor-corner RMS spot radius in Runs 001-002. Its field curvature is the dominant flat-detector limitation.
- The Run 002 physical A01 model used a 130 mm clear primary and 58 mm secondary/entrance obstruction. Calculated aperture throughput was approximately 79.5% before spider, coating and baffle losses.
- Run 002 verified an approximately +0.844 mm detector shift from infinity focus for the 800 m finite conjugate using full-ray on-axis optimization. A practical focus mechanism is not designed.
- A02 and A03 do not provide enough flat-field benefit to justify their additional optical and mechanical complexity.
- The A04 diagnostic recovered 794.203 mm EFL magnitude and approximately 4.7/2.9/3.3/5.8 um monochromatic RMS across the sampled field, but its approximately 7.3 mm tertiary-detector clearance and nearly overlapping ray footprints are physically suspect. It is not a developed Run 002 design.
- The inability of the tested minimal correctors to remove A01's flat-field limitation justifies reopening architecture exploration.
- Run 003 proves that A04's nominal spot advantage is physically unusable with a centered detector: the Run 002 seed provides only 0.59 mm minimum pre-tertiary beam radius at the detector plane versus the 6.96 mm active half-diagonal (7.96 mm with the screening margin).
- Three materially distinct A04 attempts failed the detector-clearance screen. The best EFL-restored long-return attempt reached approximately 793.95 mm EFL and 1.4-9.7 um RMS but only 0.29 mm minimum clearance. A hard-clearance attempt degraded to approximately 77-80 um RMS and still did not clear the detector.

## Open engineering questions

1. What limitations must be recorded when preserving A01 for the blind portfolio?
2. What final verification and independent handoff are justified for A01 without reopening architecture exploration?
3. What primary-hole, spider and baffle geometry is practical for any preserved coaxial reflective candidate?
4. What detector-refocus mechanism can provide the verified finite-conjugate travel over the operating temperature range?
5. How do tolerances, thermal behavior, stray light, coating losses and manufacturing/metrology burden alter the candidate ranking?

## Resource and plateau status

- Runs 001 and 002 predate workflow v3; their numerical histories and resource use are not retroactively reinterpreted.
- Run 003 used 3 substantial searches and 3 materially distinct A04 screening attempts; all failed to produce a physically valid improvement, so the stage plateaued.
- A02 and A03 are closed as rejected derivatives. A01 is parked after its minimal-corrector development branch failed to resolve the structural flat-field limitation.
- A04 is rejected in its coaxial form. Any off-axis/decentered three-mirror work belongs to A06 and a new run.
- Run 004 screened only A06 in five substantial searches/five distinct attempts, reaching the candidate-stage attempt cap. No sixth search is authorized. No formal three-attempt plateau is claimed: clearance and optical metrics traded against each other, and attempt 5 made negligible progress.
- Run 004's matched 3 x 3 field/pupil audit gives A01 a worst flat-field RMS of 8.63 um. A06 attempt 1 clears the detector by 26.03 mm but has 169.05 um worst RMS; attempt 2 reaches 30.62 um but intersects the active detector; attempts 4/5 give about 59.4 um and 7.61 mm clearance versus the 7.96 mm circular screening keepout. No useful flat-field advantage was established.
- The user reported 14% remaining in the five-hour quota while Run 003's final attempt was executing; the running attempt was allowed to finish and the run was then closed without further searches.

## Procedural and human-intervention history

- 2026-09-04: `WORK_GUIDE.md` was updated after the initial Track A invocation and Run 001. The updated rules applied prospectively; Run 001 remained unchanged.
- 2026-09-04: Run 002 compared the physical A01 baseline with minimal corrector derivatives, explicitly modelled apertures, and verified the 800 m focus shift.
- 2026-09-04: Human intervention stopped extension of Run 002 into detailed TMA optimization. An already-running bounded seed sweep was retained only as screening evidence for a later candidate/run.
- 2026-09-04: Workflow v3 replaced the six governing workflow files after Run 002. This is a procedural benchmark milestone, not an optical-design correction; Runs 001 and 002 remain immutable historical evidence.
- 2026-09-04: Run 003 rejected A04's coaxial topology after three distinct attempts failed the centered-detector clearance screen. The user requested a prompt conclusion after reporting 14% remaining five-hour quota; no additional search was started.
- 2026-09-05: User authorized only a bounded Run 004 A06 screen, with promotion to one final development run only if clearly promising; otherwise park/reject and close architecture exploration. No further architecture family may be opened without explicit user instruction. This is procedural governance, not an optical correction.
- Run 004 internal model audit corrected detector keepout placement to the actual on-axis image centroid and used exact field normalization. Earlier nominal-origin clearance metrics are superseded by `runs/run_004/audit.json`. This correction was autonomous, not supplied by the user.

## Most useful next work

Prepare A01's remaining verification/limitations and blind-portfolio freeze scope. Do not open another architecture family, start A06 development, expose Track B research or read the hidden reference as a consequence of this screening closure.

## Last reviewed run

run_004 - Track A A06 off-axis/decentered three-mirror screen; five-attempt cap reached, A06 parked, architecture exploration complete
