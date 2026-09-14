# Run 021 supplier-question package

Status: budgetary RFQ / manufacturability inquiry. Nominal optical geometry is supplied to obtain comparable responses; quoted figure and cosmetic tiers are **commercial comparison tiers, not released requirements**. Final drawings, tolerances, coating allocations and flight-load specifications do not yet exist.

## Common commercial and quality questions

Apply these questions to every custom optic or donor route.

1. Quote one engineering unit and recurring breaks at 5, 10 and 25 identical units. Separate NRE, tooling/nulls/CGHs, programming, first-article inspection, coating qualification, witness samples, recurring inspection and unit price. State MOQ and economic lot size.
2. State substrate manufacturer/grade, anneal/homogeneity class where relevant, blank pedigree, CTE, density, actual blank/finished mass and lead time. Offer a low-CTE solid option and supplier-recommended lightweight option; identify proof-test and print-through implications.
3. Quote supplier-standard figure grades and cost/schedule deltas for residual surface figure tiers of 0.10, 0.05 and 0.025 wave RMS at 632.8 nm after removal of the nominal conic. State spatial-frequency filtering, aperture mask, support orientation, gravity compensation and uncertainty. These tiers are for market comparison pending a system tolerance allocation.
4. State measured microroughness and bandwidth; price <=2 nm RMS and <=1 nm RMS options if available. State standard cosmetic quality and price a 40-20 option. Do not treat scratch-dig as a scatter model.
5. Provide radius/conic measurement uncertainty, edge-zone exclusion, clear-aperture definition and full inspection map. State whether the central hole/edge is included in the guaranteed figure zone.
6. State coating process, witness-coupon correlation, spectral/angular/polarization data, adhesion, humidity and thermal-cycle heritage. Quote coating separately from figure/substrate.
7. State lot-to-lot controls, capacity, obsolescence notice, repair/recoat policy, replacement lead time, second-site/second-source options and data rights for inspection tooling.
8. The operating temperature requirement is -25 to +50 C. State what can be warranted over that range. Identify the shock, vibration, humidity, altitude/pressure, storage-temperature and life-cycle inputs needed for an airborne qualification quotation; no unstated military standard is implied.

## C01 custom mirror package

All signs follow the preserved sequential-model convention and must be converted to drawing sag equations before order. Quote each optic separately and as matched EO and SWIR sets.

| Optic | Nominal powered surface | Required optical clear region | Spectral coating inquiry | Mechanical inquiry |
|---|---|---|---|---|
| EO primary | R = -760.0300 mm, K = -1.316742 | Annulus OD 133.0 mm, ID 43.0 mm | Qualified high-reflectance 0.43–0.80 um; provide R(lambda), AOI/polarization dependence and durability | Quote solid and lightweight low-CTE blanks; define hole-before/after-figure process, edge/chamfer, cell datum and finished mass |
| EO secondary | R = -541.9007 mm, K = -11.999713 | Circular diameter 71.0 mm | Same EO band | State test method for strong conic, mount land, back datum and matched-set alignment data |
| SWIR primary | R = -996.3881 mm, K = -1.039830 | Annulus OD 313.371 mm, ID 28.941 mm | Qualified high-reflectance 0.80–1.80 um | Quote solid, pocket-lightweighted and supplier-recommended alternatives; state facesheet/rib, hole reinforcement, support print-through and finished mass |
| SWIR secondary | R = -319.7149 mm, K = -3.285870 | Circular diameter 79.179 mm | Same SWIR band | State full-aperture test method, mount land/datum and matched-set options |

Supplier response requested:

- Can every stated clear aperture, including its edge zone, be guaranteed with no unpriced exclusion? If not, give the required mechanical oversize.
- What null/CGH/interferometric or profilometric method will be used for each conic, and which tooling can be amortized across lots?
- What lightweighting pattern, minimum facesheet and support points are recommended for the 313 mm primary under an airborne disturbance environment? Provide mass and first flexible-mode estimate only if boundary conditions are stated.
- Can EO and SWIR coatings be supplied by the mirror fabricator, with before/after figure maps and witness data? Identify coating stress risk.
- Identify the minimum drawing/tolerance information still needed for a firm quotation.

Mechanical/thermal inputs still required before a meaningful C01 structure/gimbal mass exists: detector/dewar/electronics CAD and masses; connector/cable keep-outs; focus stroke/resolution/repeatability and actuator placement; primary/secondary cell interfaces; baffle/stray-light lengths; stiffness/jitter and line-of-sight stability allocations; gimbal axes and allowable imbalance; UAV shock/vibration spectra; thermal boundary conditions, gradients, dissipation and heater/radiator concept; sealing/purge/window strategy; calibration target and boresight adjustment/lock concept.

## C02-A6F1 common-front package

### Annular primary and secondary

| Optic | Nominal powered surface | Required optical clear region | Additional geometry |
|---|---|---|---|
| Common primary | Paraboloid, R = -622.7426 mm, K = -1 | Annulus OD 313.499 mm, ID 69.580 mm; radial clear width 121.959 mm | f/1 parent; edge sag 19.728 mm; edge slope 14.128 deg; sag at hole edge about 0.97 mm |
| Common secondary | Paraboloid, R = -103.7904 mm, K = -1 | Circular diameter 56.249 mm | Nominal primary-secondary separation 259.476 mm |

Both mirrors require a coating usable across 0.43–1.80 um. Ask the supplier to propose durable protected-metal or other broadband systems and provide guaranteed R(lambda, AOI, polarization), coating stress and environmental evidence. Do not substitute a visible-only or SWIR-only claim.

Primary-specific questions:

- Is the hole produced before fine figuring, after figuring, or integral to the lightweight blank? What edge/chamfer and hole-diameter allowances protect the clear annulus?
- Quote solid low-CTE, pocket-lightweighted and supplier-preferred substrate/architecture alternatives. Give finished mass, facesheet/rib geometry, support definition and predicted print-through sensitivity.
- Describe a credible full-annulus metrology plan: null lens/CGH, stitching/sub-aperture method or another traceable approach. State how the central hole, steep edge, gravity support and obscured zones affect uncertainty.
- What figure yield and rework risk is expected at the three common comparison tiers? Which tier drives a new CGH or test tower?
- Can the mirror include rear/edge datums and flexure interfaces without corrupting the annular clear zone? What data are needed for a dynamic/support analysis?

An inability to quote a traceable annular figure, a finished lightweight mass competitive with the C01 large-mirror set, or repeatable production yield is potentially architecture-ending for C02.

### Dichroic at the 0.8 um boundary

The source bands touch at 0.80 um; no zero-width transition is requested. The current collimated SWIR beam is about 51.9 mm. Quote a projected useful circular beam of at least 55 mm, with the physical elliptical clear aperture sized for the proposed angle. Provide both EO-reflect/SWIR-transmit and EO-transmit/SWIR-reflect orientations if materially different.

Quote feasibility—not yet acceptance—for:

- a 20 nm transition option with guaranteed passbands ending at 0.79 um and starting at 0.81 um;
- a 40 nm transition option with guaranteed passbands ending at 0.78 um and starting at 0.82 um;
- supplier-recommended wider transition if either option causes excessive ripple, angle shift, polarization split, stress, cost or yield loss.

For candidate AOIs of 30 and 45 degrees, provide s/p spectral curves over 0.43–1.80 um across the full cone/field incidence range, useful-port efficiency, blocking/leakage, transition shift, temperature shift over -25 to +50 C, transmitted/reflected wavefront, wedge/ghost strategy, substrate/material/thickness, clear aperture, coating stress, damage/cleaning constraints, witness-coupon method and qualification heritage. Final passband ownership requires detector QE, source spectrum and SNR allocation and is therefore a system gate.

### Three-element backend-camera study specification

This is a budgetary optical-design/manufacturability study, not a released lens drawing. Use the traced A6F1 collimated split and do not add a dedicated pupil relay unless analysis proves it necessary. Size clear apertures so the camera adds no material vignetting to the preserved common-front pupil.

| Parameter | EO camera | SWIR camera |
|---|---:|---:|
| Camera EFL target | 132.367 mm | 321.750 mm |
| Nominal entrance-pupil diameter | 21.35 mm | 51.90 mm |
| Nominal f-number | 6.2 | 6.2 |
| Object-space diagonal half-field at camera | about 3.01 deg | about 1.46 deg |
| Spectral band | 0.43–0.80 um | 0.80–1.80 um |
| Detector active area | 11.223 x 8.220 mm | 12.8 x 10.24 mm |
| Complete-system EFL | 794.203 mm | 1930.502 mm |
| Existing common-front burden | about 60.5 mm focal-surface radius | about 63.0 mm focal-surface radius |

Study a maximum of three powered elements per channel initially, including a field-flattener role where useful. Report glass availability/athermalization, maximum diameter and thickness, surface/asphere count, barrel length, distortion, chief-ray angle, flat-detector RMS/MTF, lateral color, pupil/clearance, ghost paths, focus sensitivity, decenter/tilt sensitivity, temperature behavior and producibility. Provide a sensitivity to detector windows at zero, 0.5 and 1.0 mm optical thickness until actual window data arrive; do not select a nominal window from these cases. Separate optical-design NRE, element/tooling NRE and recurring cost.

The physical fold study must place the dichroic, both cameras, windows, detector/dewar envelopes and two focus functions without using the current 79.7 L straight screen as final CAD evidence.

## C04 donor and corrector package

### 353/1600 primary donor and 63 mm flat

Ask the donor supplier in writing:

1. Is at least 311.371 mm diameter a guaranteed, fully figured optical clear aperture on the nominal 353 mm, 1600 mm focal-length paraboloid? State edge-zone exclusion and provide a full-aperture map, not nominal blank diameter.
2. Confirm actual radius/conic, focal-length tolerance, edge thickness, substrate/anneal, finished mass, back shape, support recommendations, roughness, cosmetic grade and figure specification/measurement aperture for each offered optical grade.
3. Is an uncoated figured substrate available? Can the factory supply a qualified 0.80–1.80 um coating? Provide guaranteed spectral/angular data, coating stress, before/after figure maps, environmental evidence and witness samples.
4. If only a stock coating is available, identify chemistry/layers and approved stripping process. Who retains warranty after stripping/recoating? What surface damage, re-polish, edge and figure re-verification risks apply?
5. Can lots of 5, 10 and 25 be supplied to one controlled substrate, figure, edge-zone and coating specification? State yield, lot continuity, replacement/obsolescence policy, lead time, inspection data and second-source options.
6. What mechanical cell/support data exist, and what must change for -25 to +50 C airborne use? State which environmental tests have actually been passed; do not infer flight qualification from astronomy use.
7. For the 63 mm minor-axis flat, state guaranteed clear ellipse at 45 degrees, substrate, flatness, local slope, roughness, coating options, mass and lot availability.

### Two custom SWIR corrector elements

Nominal local signs follow the preserved model and require drawing confirmation. Quote as a matched pair and individually.

| Element | Material | Provisional OD / useful CA | R1 | R2 | Centre thickness |
|---|---|---|---:|---:|---:|
| L1 | Fused silica | 50 mm / >=48 mm | -389.1168 mm | -4637.9518 mm | 6.0 mm |
| L2 | Optical CaF2 | 50 mm / >=48 mm | -344.8821 mm | -111.0931 mm | 5.0 mm |

Ask for melt/lot data, index-homogeneity data, radius and centre-thickness capability, wedge/centring, edge thickness, CaF2 handling/coating risk, matched-cell tolerances, 0.80–1.80 um AR performance versus AOI, transmitted wavefront, ghost control, thermal cycling and replacement continuity. Quote optical-design/tolerance support separately because final tolerances and detector window are not allocated.

### C04 disposition test

A positive donor answer can validate C04 as a procurement hedge and establish real cost. It cannot by itself make the current 273.4 L / 1.455 m / 8.28 kg-primary system a competitive compact UAV payload. Ask whether a substantially lighter blank with the same 311.371 mm guaranteed clear figure is available. If not, do not open another C04 optical rescue. If yes, require a fresh structure/fold concept and show that its extra custom work preserves the donor's NRE/recurring advantage before C04 can re-enter C2.
