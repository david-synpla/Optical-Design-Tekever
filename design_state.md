# Current Design State

Track: A - autonomous / uninformed
Stage: candidate screening and development
Workflow: v3 active after Run 002
Track status: open; no blind candidate is frozen

## Candidate portfolio

| ID | Architecture / genealogy | Status | Best evidence | Main strength | Main risk |
|---|---|---|---|---|---|
| A01 | On-axis two-conic-mirror Cassegrain-type baseline | PARKED | Runs 001-002 | Compact, achromatic, approximately 794.2 mm EFL and f/6.2; remains viable | Flat-field image quality and detector-Nyquist MTF are weak; substantial obscuration and strong secondary conic |
| A02 | A01 derivative with 4 mm fused-silica near-focus singlet | REJECTED | Run 002 | Modest corner improvement | Degrades the center, adds chromatic dependence and does not justify two added surfaces/cell complexity |
| A03 | A01 derivative with 5.5 mm cemented N-BK7/N-F2 corrector | REJECTED | Run 002 | Improves portions of the middle field | Worst-field performance remains weak; three refracting surfaces, two glasses and cemented-interface burden are unjustified |
| A04 | Coaxial three-mirror anastigmat branch | PROPOSED | Run 002 screening diagnostic only | One bounded seed suggests improved nominal flat-field performance at the required EFL magnitude | Existing seed has impractical tertiary-detector clearance and unverified self-obscuration/mechanical feasibility |
| A05 | All-refractive long-focus family screened as scaled doublet, triplet and multi-element telephoto | REJECTED | Run 001 | Unobscured conventional optical path | Approximately 0.1-0.2 mm band-edge RMS spots plus unfavorable length, glass mass and thermal behavior |

No candidate is currently `ACTIVE` or `FROZEN`. A04 is the proposed next screening branch; A01 is preserved for later comparison rather than rejected.

## Established conclusions

- Explicit customer requirements remain those in `requirements/eo_requirements.yaml`; no customer image-quality, distortion, obscuration, package, mass, transmission, stray-light or tolerance limits were supplied.
- Derived first-order targets are approximately 794.2 mm EFL, 128.1 mm entrance pupil at f/6.2, and 0.8096 deg x 0.5930 deg active-array field.
- A01 achieved approximately 3.4-3.7 um on-axis and 8.4-8.8 um sensor-corner RMS spot radius in Runs 001-002. Its field curvature is the dominant flat-detector limitation.
- The Run 002 physical A01 model used a 130 mm clear primary and 58 mm secondary/entrance obstruction. Calculated aperture throughput was approximately 79.5% before spider, coating and baffle losses.
- Run 002 verified an approximately +0.844 mm detector shift from infinity focus for the 800 m finite conjugate using full-ray on-axis optimization. A practical focus mechanism is not designed.
- A02 and A03 do not provide enough flat-field benefit to justify their additional optical and mechanical complexity.
- The A04 diagnostic recovered 794.203 mm EFL magnitude and approximately 4.7/2.9/3.3/5.8 um monochromatic RMS across the sampled field, but its approximately 7.3 mm tertiary-detector clearance and nearly overlapping ray footprints are physically suspect. It is not a developed Run 002 design.
- The inability of the tested minimal correctors to remove A01's flat-field limitation justifies reopening architecture exploration.

## Open engineering questions

1. Can A04 be configured with credible ray clearance, obscuration and packaging while retaining a meaningful flat-field advantage over A01?
2. If A04 fails physical screening, which materially different flat-field architecture deserves the next bounded run?
3. What primary-hole, spider and baffle geometry is practical for any preserved coaxial reflective candidate?
4. What detector-refocus mechanism can provide the verified finite-conjugate travel over the operating temperature range?
5. How do tolerances, thermal behavior, stray light, coating losses and manufacturing/metrology burden alter the candidate ranking?

## Resource and plateau status

- Runs 001 and 002 predate workflow v3; their numerical histories and resource use are not retroactively reinterpreted.
- No v3 candidate/stage attempt counter is active yet.
- A02 and A03 are closed as rejected derivatives. A01 is parked after its minimal-corrector development branch failed to resolve the structural flat-field limitation.
- The next substantive work must begin as a new bounded run, normally Run 003, with A04 at `SCREENING` and an explicit physical-feasibility question.

## Procedural and human-intervention history

- 2026-09-04: `WORK_GUIDE.md` was updated after the initial Track A invocation and Run 001. The updated rules applied prospectively; Run 001 remained unchanged.
- 2026-09-04: Run 002 compared the physical A01 baseline with minimal corrector derivatives, explicitly modelled apertures, and verified the 800 m focus shift.
- 2026-09-04: Human intervention stopped extension of Run 002 into detailed TMA optimization. An already-running bounded seed sweep was retained only as screening evidence for a later candidate/run.
- 2026-09-04: Workflow v3 replaced the six governing workflow files after Run 002. This is a procedural benchmark milestone, not an optical-design correction; Runs 001 and 002 remain immutable historical evidence.

## Most useful next work

Open Run 003 to answer one bounded question: whether a physically constrained A04 coaxial TMA can retain a meaningful flat-field advantage over A01 without tertiary-detector interference or unacceptable self-obscuration.

## Last reviewed run

run_002 - Track A physical baseline and minimal-corrector comparison; closed under the earlier workflow
