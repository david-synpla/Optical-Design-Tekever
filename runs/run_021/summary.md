# Run 021 — Track C C1 closure and RFQ readiness

## Decision

There is **not enough evidence to select one architecture for C2**. Advance a two-architecture gate:

- **C01 B05-1/S16 is the preferred C2 reference and fallback.** It is the only compact comparator with complete physical, polychromatic EO and SWIR prescriptions, a credible integrated fold, and no dichroic.
- **C02-A6F1 remains a conditional C2 challenger**, retained for its common line of sight, smaller frontal aperture and one-large-optic topology. It must pass three coupled gates before it can displace C01: quoteable annular-primary fabrication/metrology, a realizable dichroic transition allocation, and one bounded real three-element-camera plus folded-package demonstration.
- **C04-N1400/B09 remains a procurement-risk hedge, not a C2 optical-development candidate.** Even ideal donor answers do not remove its 1.455 m track, 273 L screen, 8.28 kg primary or high inertia. A radically lightweight/folded rescue would cease to be the low-NRE donor architecture already tested.

No architecture is frozen. No prescription was optimized or changed in this run. C03 and C05 remain parked.

## Normalization basis

The comparison uses one accounting boundary. Optical prescriptions, traced geometric survival and existing package geometry remain measured/modelled evidence. All three architectures are treated as carrying the same EO sensor interface, SWIR detector/dewar interface, channel electronics and two focus functions. Because drawings and masses for those modules are absent, they are reported as **common missing payload allowances**, not assigned invented values. Architecture-specific branch clearance remains charged to the architecture that creates it.

The reported mass numbers are not payload masses. C01 and C02 use the preserved solid-mirror blank proxy; C04 uses the catalogue 8.28 kg donor plus geometric optical proxies. Cells, baffles, structure, mechanisms, windows, detectors, electronics, harness, thermal hardware and gimbal are excluded from all optical-mass values. Existing structure-area proxies are retained as scalable geometry, not converted to a preferred structural material.

Coatings are normalized as count sensitivities. At the established neutral 0.90 reflectance and 0.90 useful splitter-port point, a two-mirror no-split path is 0.810 and a two-mirror-plus-splitter path is 0.729. These are not coating specifications. C01 SWIR has 95% traced geometric survival; C02 has 70.83% EO / 73.31% SWIR; C04 SWIR has 93.55%. Corrector surfaces, windows, absorption, scatter, polarization and detector QE remain outside those factors.

RFQs request identical commercial pricing scenarios—one engineering unit and recurring breaks at 5, 10 and 25 identical units—with NRE/tooling, inspection, witness samples and recurring unit price separated. These are quote-comparison quantities, not a production forecast. The only existing environmental requirement carried into the package is -25 to +50 C operation. Shock, vibration, humidity, altitude/pressure, storage temperature and life-cycle profiles must be supplied before release-to-build or flight qualification.

## Normalized Pareto consequence

| Objective | C01 B05-1/S16 | C02-A6F1 | C04-N1400/B09 |
|---|---|---|---|
| Optical maturity/performance | Complete modeled EO/SWIR trains; 0.80 / 8.77 um worst dense RMS | Common front near obscured-pupil limit on curved focus; real doublets parked at 33.93 / 37.47 um; triplet-like cameras absent | Complete modeled train conditional on donor; 7.97 / 9.22 um worst dense RMS |
| Package | 470 x 325 x 446 mm; 68.2 L | 337 x 337 x 700 mm; 79.7 L same-allowance straight screen, but dichroic branch/fold and cameras unproved | 512 x 367 x 1455 mm; 273.4 L; tested large fold is worse at 286.2 L |
| Mass proxy | 5.74 kg solid-mirror proxy; structure area 0.455–0.602 m2 | 5.09 kg solid-mirror proxy; cylindrical area 0.742 m2 before branches | 8.84 kg mixed optical estimate, including 8.28 kg donor; structure area 0.960–1.295 m2 |
| Inertia/CG | Lowest current axial extent; asymmetric twin-lobe CG needs CAD | Narrow front/common axis, but 700 mm straight arm and branches need fold proof | Dominated by long metering structure and heavy end primary; materially worst current gimbal case |
| Throughput evidence | No splitter; 0.810 neutral mirror factor; SWIR geometric survival 0.95 | Splitter; 0.729 neutral factor before 0.708/0.733 geometric survival | No splitter; 0.810 neutral mirror factor; SWIR survival 0.9355, then four refractive surfaces |
| LOS/parallax | Separate axes; 296.5 urad at 800 m, but 100% of SWIR scene overlaps EO in the planar screen | Common fore-optic LOS; downstream channel registration remains | Separate axes; 322.5 urad at 800 m, with 100% SWIR scene overlap in the planar screen |
| Manufacturing difficulty | Four custom conic mirrors plus EO corrector; conventional compact coaxial cells | f/1 annular primary with large hole, common secondary, dichroic and two three-element cameras | Catalogue primary/flat hypothesis plus four small custom spherical corrector surfaces; long precision structure |
| Alignment/tolerance | Moderate; independent channels and relative boresight datum | High/coupled; primary-secondary, split wavefront and two cameras affect both channels | Moderate/high; long Newtonian metering, flat and two-lens centration |
| Thermal/focus | Two mechanisms; B05 thermal evidence exists; SWIR and common-bench gradients open | Two mechanisms; shared front drift plus camera focus/athermalization unproved | Two mechanisms; 4.648 mm SWIR range refocus plus long-structure thermal drift |
| NRE | Moderate/high custom optics, but B05 evidence lowers optical-development risk | High and still uncertain: annular null/support, dichroic and two new cameras | Potentially lower large-figure NRE; custom corrector, coating process and flight structure remain |
| Recurring cost | Four custom mirrors/cells; quote absent | One difficult primary plus secondary, splitter and six camera elements; yield absent | Potential donor price advantage, but coating, corrector, long structure and qualification recur |
| Supplier risk | No qualified source or second-source evidence | No qualified source for primary/dichroic/cameras; coupled single-point failures | One identified donor source; clear aperture, lot continuity, recoating and replacement unproved |
| Qualification burden | Moderate/high, compact custom payload | High, novel coupled payload | High, astronomy donor and long flight structure |
| Major unresolved assumptions | Mirror quote/lightweighting; actual common-bench mass; window; boresight stability | Primary feasibility/mass; dichroic transition; real cameras; folded CAD; coating/polarization | Guaranteed clear figure; coating route; lot continuity; donor qualification; long-structure mass |

The table is intentionally not reduced to a weighted score. C01 leads current completeness, compactness and optical risk. C02 preserves a distinct common-LOS/front-area point. C04 preserves a possible procurement/NRE point but is dominated in the current UAV package.

## Ranking-changing gates

The complete classification is in `unknowns.csv`. The immediate C2 gate is:

1. Obtain budgetary, non-binding responses for C01 mirrors and the C02 annular primary/secondary at the same quantity breaks and inspection basis.
2. Select a physically finite 0.8 um dichroic transition only after detector QE/source/SNR ownership is assigned; obtain feasibility for at least two transition-width/AOI options.
3. If the C02 primary and dichroic responses are credible, authorize exactly one bounded C02 run: real three-element EO and SWIR cameras, detector-window sensitivity, and a physical two-branch folded envelope. Compare its complete package and toleranced image quality directly with C01.
4. In parallel, create a common detector/dewar/electronics envelope and a concept CAD/thermal-mass model for C01 and C02. A sole-architecture down-select waits for those two package models.

C04 donor/corrector RFQs should proceed as market-risk work, but no plausible answer to clear-aperture, coating or unit-price questions can alone overcome the present approximately 4.0x C01 volume, 3.1x maximum dimension, heavier primary and roughly 5.7x vertical-axis specific-inertia proxy. C04 would re-enter C2 only if a supplier offers a materially lighter donor and a purpose-built fold/structure concept that retains the procurement advantage.

## What is known versus assumption-driven

Known well enough for C2 work: system first order; C01 nominal EO/SWIR image evidence and folded screen; C02 full-field common-front pupil/obscuration and curved-field evidence; C04 nominal optical result conditional on its donor; relative scene overlap at 800 m; optic counts; and current envelope/mass-proxy direction.

Assumption-driven: all complete payload masses, cells/baffles, detector-window prescriptions, exact focus hardware, coating efficiencies, gradient behavior, flight loads, gimbal sizing, production yield/cost, and supplier continuity. C02 additionally lacks physical cameras and a folded branch package. C04 additionally lacks a guaranteed donor clear aperture and qualified SWIR coating route.

## Resource use and integrity

This was a closure/RFQ analysis, not an optical search: zero optimizer invocations, zero prescription attempts, zero substantial computational searches and no dependency installation. Work comprised read-only extraction of Runs 014–020, normalization, an unknowns classification and RFQ drafting. `reference/` was not accessed; historical runs and all Track A/B/C prescriptions were not modified. Run 021 closes here.
