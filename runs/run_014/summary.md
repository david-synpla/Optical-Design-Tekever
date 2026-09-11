# Run 014 — Track C Stage C0 first-order optical + SWaP architecture screen

## Decision

Advance **C01, C02, C03 and C04** to separately bounded Stage C1 development. Park **C05** without rejecting it. No architecture is a universal winner: the four promoted families occupy different credible Pareto lanes, while C05's possible volume advantage is not yet strong enough to justify immediate freeform fabrication, metrology and supplier risk.

This run is an analytic architecture screen, not a prescription-development run. It performed no Optiland model construction, numerical prescription optimization or customer pass/fail scoring. The broad numerical envelope ranges and ordinal risk classes are labelled C0 engineering hypotheses; they are not requirements, CAD results, quotations or payload predictions.

## Requirements provenance correction

Before screening, the authoritative Track C requirements file was corrected without changing any numerical value:

- original source-explicit EO and SWIR channel values remain under `source_explicit_requirements`;
- same-payload, simultaneous-operation and co-boresight statements are now recorded separately as later user/team clarifications;
- shared, partially shared and separate optical trains are explicitly permitted architecture space, not a source requirement or preference;
- `WORK_GUIDE.md` now points substantive Track C work to the complete EO+SWIR requirements file, and `DESIGN_WORKFLOW.md` defines C-series candidate IDs.

The user-supplied provenance/governance correction is recorded as a procedural human intervention. It did not change the optical numerical problem.

## First-order findings

| Quantity | EO | SWIR |
|---|---:|---:|
| EFL from pitch/IFOV, mm | 794.203 | 1930.502 |
| Entrance pupil at f/6.2, mm | 128.097 | 311.371 |
| Horizontal FoV from array x IFOV, deg | 0.80966 | 0.37989 |
| Vertical FoV from array x IFOV, deg | 0.59301 | 0.30392 |
| Thin-lens infinity-to-800 m focus shift, mm | 0.789 | 4.670 |

SWIR drives the system scale: its EFL and pupil diameter are 2.431 times EO and its pupil area is 5.909 times EO. Independent EO and SWIR focus compensation remains the lowest-risk C0 assumption because the finite-range shifts differ by 3.881 mm and new architecture thermal motion remains unmodelled.

Separate collecting apertures require only 16.9% more primary area than one SWIR-sized common aperture. Under the deliberately simple equal-technology solid-blank proxy (thickness/diameter 0.10, density 2.2 g/cm3, collecting primaries only), adding the EO primary changes 5.216 kg to 5.579 kg, only 7.0%. This is not a payload mass estimate: cells, secondaries, relay optics, mechanisms, windows, baffles, structure, lightweighting and gimbal inertia can reverse the trade. It nevertheless shows why common aperture cannot be presumed to win on mass.

For side-by-side tangent circular pupils, C01's geometric centre baseline cannot be less than 219.7 mm before margins. At 800 m that baseline corresponds to 274.7 urad of parallax, about 79.6 EO pixels or 53.0 SWIR pixels. This does not prevent simultaneous same-scene imaging, but range-dependent registration and stable relative boresight must be explicit system metrics.

## C01–C05 decisions

| ID | C0 status | Principal case for preservation | Principal C1 risk/gate |
|---|---|---|---|
| C01 | **ACTIVE — recommend C1** | Natural pupil/EFL per channel, no dichroic loss, independent coatings/focus, strongest reuse of mature EO evidence | Wider front face, duplicated cells/datums and focusers, calibrated boresight drift and parallax; requires a fresh SWIR seed and integrated structure model |
| C02 | **ACTIVE — recommend C1** | Most conventional common-LOS lane; narrow fields suit a coaxial shared front end; axisymmetric manufacture/metrology | Central obscuration, 311 mm-class front end under-used by EO, dichroic transition and relay coupling; place split near a pupil/collimated region where feasible |
| C03 | **ACTIVE — recommend C1** | Unobscured common LOS, modular back ends and strongest high-end performance/throughput potential before coating losses | Highest conventional alignment/metrology/NRE burden, asymmetric envelope and likely extra reflection; must prove a minimum-complexity afocal seed and physical clearance |
| C04 | **ACTIVE — recommend C1 economic lane** | Only lane explicitly optimized for procurement/NRE/recurring-cost potential; stock-like mirror tests and B09 lessons remain valuable | A 300 or 305 mm clear pupil gives only f/6.435 or f/6.330 at the required SWIR EFL; exact f/6.2 needs at least 311.371 mm clear aperture, so a nominal >=320 mm donor or a custom primary is required. Coatings, substrate lots, rehousing and qualification can erase savings |
| C05 | **PARKED, not rejected** | Only family with a distinct aggressive volume-compression hypothesis and possible mount/interface reduction | Two to four freeforms/monolithic surfaces, specialist fabrication/metrology, coupled thermal registration, polarization/coating angles and concentrated supply risk are not justified before simpler branches expose a packaging failure |

The C0 envelope hypotheses overlap substantially: C01 about 102–262 L, C02 64–157 L, C03 71–255 L, C04 102–406 L and C05 39–135 L. These ranges are intentionally broad architecture placeholders, not measured package volumes. They show that C05 has a plausible compactness role but do not establish dominance; C02 currently offers the best assumed conventional common-aperture volume/NRE balance.

## Throughput, coating and thermal implications

Shared optics exchange common LOS for losses and coating complexity. In the neutral sensitivity case of 0.90 reflectance per mirror and 0.90 useful-port splitter efficiency, the core product is 0.810 for two mirrors without a splitter, 0.729 for two mirrors plus splitter, and 0.656 for three mirrors plus splitter. These are count sensitivities only: relay optics, windows, glass absorption, detector QE, obscuration, polarization and scatter are excluded. They do not prove C01 has higher end-to-end signal because its separate channels still require their own correctors and windows.

The 0.80 um touching band edge is unresolved. C02, C03 and C05 need a deliberate transition/QE/polarization allocation rather than assuming perfect simultaneous transmission and reflection at exactly 800 nm. Common mirror coating selection must also trade the 430 nm EO edge against SWIR throughput and durability. C01 avoids the dichroic allocation and permits independent coatings; C04 inherits whatever spectral limits its donors actually have.

No Track C architecture may reuse Run 013 thermal numbers. C0 recommends two channel-specific range/thermal focus controls for every promoted branch until a coupled solution proves superior. C02/C03 add common-fore-optic LOS drift; C01/C04 add relative telescope-datum drift.

## Useful B-series evidence, without historical alteration

- **B05-1** is the most useful balanced EO subsystem evidence for C01: 329 mm optical vertex span, strong nominal image quality and lower alignment/focus burden than B06. Its prescription remains historical and unchanged.
- **B05-2** supplies a 283 mm compact EO packaging alternative, but its stronger secondary shape and sensitivity prevent assuming it is automatically lower cost.
- **B06** proves an unobscured off-axis EO path can clear physically at approximately 323 mm vertex span and provides alignment/metrology warnings relevant to C03. It cannot be scaled to a 311 mm shared aperture as a performance prediction.
- **B09** supplies C04's best verified stock-mirror/custom-corrector process evidence and its caution: optical donor savings coexist with a long side-exit package, unverified coating/substrate data, lower corner image quality and custom airborne mechanics.
- B01/B03 remain empirical COTS integration fallbacks with unavailable full-band performance, not candidates assigned a poor optical score.

No Track A/B prescription or run was modified. No B-series thermal number or optical performance was transferred to a new Track C architecture.

## Unresolved issues and C1 gates

1. No architecture has a SWIR prescription, real telephoto ratio, obscuration, clear-aperture layout, detector-window interface or actual mass/CAD model.
2. No hard payload mass/volume, image-quality, throughput, distortion, obscuration, stray-light or boresight-stability threshold exists.
3. The mission/radiometric allocation around 800 nm, detector QE/source weighting, polarization and environmental coating durability are unknown.
4. Relative boresight, thermal drift, pointing/jitter and parallax calibration need system error budgets; common aperture does not eliminate downstream relay registration.
5. Mirror substrate/lightweighting technology, cell/structure material, thermal gradients, focus range/accuracy, vibration modes and gimbal inertia are open.
6. C04 lacks verified >=311.371 mm clear-aperture donor optics, SWIR-ready coatings/substrates, production terms and qualification evidence.
7. All package and cost comparisons remain relative hypotheses; no supplier RFQ, quotation or production-volume assumption exists.

## Resource use and closure

Zero optimizer or substantial computational-search invocations; zero prescription attempts; no plateau. One deterministic WSL Python analytic execution completed in 0.49 s, plus reporting and verification. No extra package was installed. Optiland was intentionally not invoked because C0 forbids detailed prescription optimization and the engineering question was answered with first-order calculations and SWaP/risk screening.

No layout, spot, MTF, wavefront or prescription file is emitted because no optical prescription exists at C0; creating those artifacts would imply false maturity. `metrics.json`, `architecture_screen.json/csv`, `first_order.csv`, the throughput sensitivity, plots, exact script, dependencies, requirements snapshot and hashes preserve the reproducible evidence.

**Next recommended action, only after new authorization:** Stage C1 Run 015, a minimum-degree-of-freedom C02 coaxial common-front seed with explicit obscuration, pupil/collimated splitter placement and independent EO/SWIR relay first-order targets. Follow with separate bounded C01, C03 and C04 runs; do not reopen C05 unless simpler branches demonstrate a package shortfall or supplier evidence materially reduces its risk.

`reference/` was not accessed. Stage C0 stops here; Stage C1 has not begun.
