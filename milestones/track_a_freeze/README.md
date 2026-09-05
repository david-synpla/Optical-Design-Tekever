# Track A blind portfolio freeze

Freeze date: 2026-09-05

Track: A - autonomous / uninformed

Workflow: v3 (applied prospectively after Run 002)

Supporting runs: 001-004

Portfolio recommendation: A01, frozen with unresolved limitations

Reference and Track B research access before freeze: none

## Freeze decision

Track A is frozen with **A01 as its sole preserved final candidate**. A01 is the most credible result found under the bounded blind workflow: a centrally obscured, on-axis, two-conic-mirror Cassegrain-type telescope. It meets the derived first-order scale closely, is reflective across the supplied 0.43-0.80 um band, and remains substantially simpler and better supported than the investigated alternatives.

This freeze records the best defensible Track A result and its evidence. It does not assert production readiness or full customer-requirement verification. A01 retains weak flat-detector corner performance and detector-Nyquist MTF, while its mechanical, thermal, tolerance and stray-light implementation remains unresolved. No further Track A architecture optimization is authorized by this milestone.

The frozen A01 prescription and executable model are copied into this directory. The authoritative development evidence remains in Runs 001-002; rejected and parked alternatives remain preserved in Runs 001-004.

## Final portfolio

| ID | Final state | Architecture | Track A disposition |
|---|---|---|---|
| A01 | FROZEN | On-axis two-conic-mirror Cassegrain-type baseline | Sole final candidate and recommendation, with explicit unresolved limitations |
| A02 | REJECTED | A01 plus 4 mm fused-silica near-focus singlet | Corner improvement did not justify center degradation, color and added cell/surfaces |
| A03 | REJECTED | A01 plus cemented N-BK7/N-F2 corrector | No adequate worst-field benefit for the glass, surfaces and assembly burden |
| A04 | REJECTED | Coaxial three-mirror anastigmat | Centered detector obstructs the pre-tertiary beam; three constrained attempts plateaued |
| A05 | REJECTED | Long-focus all-refractive seeds | Severe band-edge secondary spectrum, length, glass mass and thermal/cost burden |
| A06 | PARKED | Tilted/decentered three-mirror reflective branch | Detector conflict can be removed, but no screened layout combines clearance with an advantage over A01 |

A06 is parked rather than rejected because Run 004 is a bounded parameterized screen, not an exhaustive proof against all off-axis three-mirror forms. It is outside the frozen final portfolio and may not be reopened without explicit user instruction.

## A01 frozen configuration and evidence

The frozen infinity-focus prescription is:

| Surface | Radius, mm | Separation after surface, mm | Conic | Clear aperture |
|---|---:|---:|---:|---|
| Entrance obscuration plane | infinity | 180.0000 | 0 | annulus, radius 29-65 mm |
| Primary mirror | -600.0000 | -180.0000 | -1.16201060 | radius <=65 mm |
| Secondary mirror | -385.7000 | 317.61596583 | -6.58144493 | radius <=29 mm |
| Flat detector | infinity | 0 | 0 | IMX545 active array basis |

Run 002 reports approximately 794.2 mm effective focal length, f/6.2, a 128.0972 mm entrance pupil, and approximately 79.5% geometrical aperture throughput before spider, coating and baffle losses. Its sampled polychromatic RMS spot radius is approximately 3.4-3.7 um on axis and 8.4-8.8 um at the active-array corner. Maximum reported f-tan distortion at 0.55 um is approximately 0.0327%.

The detector-Nyquist MTF values at the four radial fields are low: tangential/sagittal approximately 0.0668/0.0668, 0.1081/0.1409, 0.0474/0.1285 and 0.0235/0.0193. These are benchmark comparison results because the source supplied no customer image-quality or MTF limit.

At 800 m, Run 002's full-ray on-axis refocus gives a secondary-to-image distance of 318.46014064 mm, a +0.84417481 mm detector shift from infinity focus. The focus motion concept is detector refocus; no mechanism has been designed.

## Requirement status

| Source requirement | Frozen Track A evidence | Status at freeze |
|---|---|---|
| Wavelength 0.43-0.80 um | Reflective prescription sampled at 0.43, 0.55, 0.65 and 0.80 um | Nominal optical model supports it; coating transmission not verified |
| Horizontal FoV 0.81 deg | Derived active-array FoV 0.809645 deg with approximately 794.2 mm EFL | Nominally supported |
| IFOV 3.45 urad/pixel | Derived target EFL 794.2029 mm; A01 approximately 794.2 mm | Nominally supported |
| f/6.2 | 128.0972 mm entrance pupil at approximately 794.2 mm EFL | Nominally supported |
| Sony IMX545, 4096 x 3000, 2.74 um pixels | Flat active array 11.22304 x 8.22000 mm used for field interpretation | Modelled basis; packaging not designed |
| Minimum focus distance 800 m | +0.8442 mm full-ray on-axis detector refocus result | Optical refocus demonstrated; mechanism and full-field finite-conjugate performance unresolved |
| Operating temperature -25 to +50 C | No completed thermal/athermal analysis | Unverified |

No source limit was supplied for image quality, distortion, obscuration, package size, mass, transmission, stray light, tolerance or cost. Values used for comparison or screening in those areas remain benchmark assumptions, not customer requirements.

## Candidate comparison

A01 is preferred because it offers the best supported balance of optical performance, simplicity and physical plausibility. The refractive candidates have roughly 0.1-0.2 mm band-edge RMS spots and unfavorable length/glass burden. The minimal correctors add chromatic, mechanical and procurement complexity without resolving A01's flat-field limitation. A04's attractive nominal spot result is physically blocked by the centered detector. A06 can create a clear folded beam path, but its clear attempt has approximately 169 um worst-field RMS; its best-image-quality attempt has approximately 30.6 um worst RMS and intersects the active detector. Later A06 compromises remain near 59 um and miss the 7.96 mm circular screening keepout.

A01 therefore dominates the investigated physically credible alternatives for this Track A evidence set, even though it does not achieve strong detector-Nyquist imaging at the flat sensor corner.

## Manufacturing, alignment, metrology, packaging and cost

A01 requires two custom conic mirrors, including a strong secondary conic near -6.58, a central aperture/obscuration, mirror supports, a spider or equivalent secondary structure, baffling and a detector-refocus assembly. These are significant cost and metrology drivers. Its coaxial geometry and two powered surfaces are nevertheless simpler to manufacture, align and test than the three-mirror branches investigated here.

The current optical model uses a 130 mm clear primary and a 58 mm secondary/entrance obstruction. A practical primary hole, spider, baffles, housing, detector envelope and focus mechanism have not been designed. The reported roughly 317.6 mm secondary-to-image distance is an optical separation, not a finished package dimension. No monetary cost ceiling exists; cost conclusions are comparative.

## Unresolved items at freeze

- Full-field finite-conjugate image quality at 800 m and focus travel across the operating range.
- A realizable detector-refocus mechanism and its repeatability, focus sensitivity and thermal behavior.
- Tolerance analysis for mirror figure, spacing, despace, tilt, decenter and detector position.
- Thermal/athermal performance from -25 to +50 C, including structure and coatings.
- Physical primary hole, secondary support/spider, baffles, detector envelope and housing clearance.
- Spider diffraction, ghosting, scatter, stray light, obscuration details and relative illumination.
- Broadband mirror coating choice, transmission, durability and environmental qualification.
- Independent OpticStudio/Zemax reconstruction and validation.
- Production manufacturing route, best-fit-sphere departures, test geometry, alignment tooling and cost estimate.

These omissions bound the claims of the frozen portfolio. They do not create new customer requirements.

## Human interventions and autonomous corrections

- After Run 001, the human supplied updated operating guidance. It applied prospectively; Run 001 remained unchanged.
- During Run 002, the human stopped extension into detailed TMA optimization. The already-running bounded seed sweep was retained only as diagnostic evidence for a later run.
- After Run 002, the human installed workflow v3 as a procedural benchmark change. Runs 001-002 were not retroactively reinterpreted.
- During Run 003, the human reported 14% remaining in the five-hour quota and requested a prompt conclusion. The running third attempt completed and no additional search began.
- The human authorized Run 004 only as a bounded A06 screen and required a promotion-or-closure decision, followed by no new architecture family without explicit instruction.
- Run 004 autonomously corrected detector keepout centering and exact field normalization. The audit supersedes the early clearance calculation; this was an internal model correction, not a human optical correction.
- The human then requested this separate Track A freeze milestone before any Track B or reference access.

No known-reference prescription, Track B research briefing or external architecture search was used in Track A.

## Resource-use summary

| Work item | Recorded use | Stop/decision |
|---|---|---|
| Environment and smoke verification | Setup and verification work; not an architecture run | Optiland/WSL environment established |
| Run 001 | Predates workflow v3; reliable optimizer/search counters not recorded | Advanced the two-mirror baseline; rejected weak refractive families |
| Run 002 | Predates workflow v3; reliable optimizer/search counters not recorded | Preserved A01; rejected minimal correctors; TMA seed retained only as diagnostic |
| Run 003 | 3 substantial searches; 3 materially distinct attempts | Three-attempt plateau; A04 rejected |
| Run 004 | 5 substantial searches; 5 materially distinct attempts; 129.414 s recorded optimizer wall time | Candidate/stage attempt cap; A06 parked |

The known quantified workflow-v3 total is eight substantial searches and eight materially distinct attempts. No quota percentage is inferred beyond the user's Run 003 report. Runs 001-002 remain historical evidence with unknown reliable counters rather than guessed values.

## Freeze boundary

This milestone freezes Track A at the commit containing this document, `metadata.json`, the A01 prescription/model/supporting metrics and plots, and `SHA256SUMS.txt`. The copied A01 artifacts are byte-identical to their Run 002 sources at freeze time. The run directories and their earlier commits preserve the detailed evidence and genealogy. Track B has not begun, and no Track B research or `reference/` content may be accessed until this freeze commit exists.

The next permitted benchmark step is to begin Track B only under explicit user direction. Track A must not be modified retroactively after Track B research is exposed.
