# Run 015 — C02 shared-coaxial physical architecture experiment

## Decision

**Do not develop the directly power-bearing shared RC/Cassegrain further now. Park that C02 form rather than forcing a prescription optimization.** Keep C02 conditionally active only through the **A6_f1p0 coaxial afocal/pupil-relayed derivative**, and give that derivative one bounded backend/manufacturing feasibility run. If a real relay cannot preserve its current pupil survival and exact channel geometry, or if the 313 mm f/1 primary is not competitive in fabrication/SWaP, park C02 as a family and prioritize C01.

No customer threshold is imposed. The decision follows a structural Pareto trade: conventional primary speed produces an unattractive EO obstruction; faster primaries recover pupil area but increase surface/fabrication burden, reduce usable backfocus, and worsen uncorrected field aberration. The afocal derivative moves the split into collimated space, but beam compression magnifies field angles and drives primary-hole/pupil-walk penalties.

## Model and scope

The deterministic Optiland model uses the authoritative EO/SWIR EFLs, fields and f/6.2 entrance pupils. Each configuration sizes the primary, secondary and primary hole to the union of nine EO and nine SWIR real-ray field footprints, with a labelled 1 mm radial screening margin. Physical obscuration and vignetting are then traced with 4,608 equal-area pupil rays per field; selected results were replayed with 18,432 rays per field.

The two direct mirrors use the classical paraboloid/hyperboloid Cassegrain construction at exact 1930.502 mm front EFL. The afocal models use two confocal coaxial paraboloids and downstream EO/SWIR stops at a common collimated split plane 50 mm behind the primary. These are minimum-complexity physical experiments, not optimized or production prescriptions. Spiders, baffles, dichroic thickness/tilt, relays, detector windows, coatings, polarization, scatter, structures and tolerances are absent.

## Direct shared power-bearing form

| Variant | Primary / backfocus | Secondary / primary-hole diameter, mm | EO / SWIR minimum pupil survival | Worst shared-front RMS EO / SWIR, um | Finding |
|---|---:|---:|---:|---:|---|
| D1 | f/2.4 / 200 mm | 117.54 / 47.39 | 16.7% / 85.4% | 14.58 / 12.33 | Conventional packaging makes the SWIR-sized secondary 91.8% of the EO entrance-pupil diameter. EO is an extremely thin annulus. |
| D2 | f/1.5 / 75 mm | 76.30 / 36.24 | 64.6% / 93.8% | 34.29 / 20.29 | Better pupil trade, but only 75 mm backfocus for split/relays and materially stronger primary/fabrication and aberration burden. |
| D3 | f/1.0 / 50 mm | 55.12 / 34.41 | 81.3% / 95.8% | 69.84 / 38.68 | Pupil survival is recovered only with a 311 mm-class f/1 primary, 50 mm backfocus and the worst uncorrected field aberration. |

The RMS values are at the shared 1930.5 mm intermediate image. They do not include the EO 0.4114x reducer or either channel's final backend, and they are not pass/fail scores. They demonstrate that pupil recovery is not free: the geometry that shrinks the shared secondary is increasingly demanding optically and mechanically.

Putting the EO stop downstream does not rescue D1. Stops placed 20%, 50% and 80% from secondary to primary image the 128.097 mm entrance pupil at Optiland paraxial coordinates 2.750, 4.836 and 8.960 m, while the real entrance-plane pupil centroid walks by up to 57.5, 68.9 and 90.7 mm over the EO field. Minimum survival remains about 16.7%. Therefore the EO channel cannot be treated as a harmless concentric stop inside the SWIR telescope.

The denser replay gives 15.6% / 85.4%, 64.6% / 93.8%, and 81.3% / 96.9% EO/SWIR survival for D1/D2/D3 and reproduces all three paraxial EFLs to better than 1e-8 mm. The lifecycle decision is sampling-stable.

## Coaxial afocal/pupil-relayed derivative

At an f/2 primary, increasing compression from 4x to 10x shrinks the secondary from 84.36 to 38.23 mm, but magnifies the EO diagonal half-field from 2.01 to 5.02 degrees. The required primary hole grows from 100.29 mm at 4x to 123.60 mm at 10x, and EO minimum survival falls from 39.6% to zero for the 8x/10x cases. A smaller secondary alone is therefore a misleading architecture metric.

The bounded fast-primary check finds one conditional pocket:

- **A6_f1p0:** 6x afocal compression, 313.50 mm primary clear diameter, 259.48 mm mirror separation, 56.25 mm secondary and 69.58 mm primary hole.
- Real-ray minimum pupil survival is **70.8% EO and 73.3% SWIR**; the 18,432-ray replay gives 70.8% and 73.5%.
- Two paraboloids give numerical on-axis collimation (about 3e-10 urad output-direction RMS in the replay).
- The backend first-order targets become EO 132.367 mm EFL / 21.350 mm pupil / 3.011 degree diagonal half-field and SWIR 321.750 mm / 51.895 mm / 1.460 degrees. Real corner chief-ray angles are 3.033 and 1.461 degrees.
- The channel stops image to an Optiland paraxial entrance-pupil coordinate about 12.96 m from the model origin. The current result therefore does not prove a compact, stable real pupil relay.

A6_f1p0 is not a selected design. Its advantage over the direct form is a genuinely collimated split region and independent powered backends; its price is a 313 mm f/1 paraboloid, a 69.6 mm primary hole, residual 26–29% geometric pupil loss before spider/coatings, and a 3 degree EO backend half-field. No cost, mass, surface-figure, baffle or alignment benefit has yet been proved.

## Candidate state and next test

- **C02-D directly power-bearing:** PARKED. It is strongly coupled across pupil size, secondary obscuration, backfocus and aberration. No shape optimization was spent on it.
- **C02-A6F1 afocal/pupil-relayed:** ACTIVE, conditional. It is the only tested C02 variant retaining a non-dominated combination of collimated split, both-channel field survival and moderate common-front length, but only by accepting an f/1 large primary.
- **C02 family:** ACTIVE only through this conditional derivative. No other C02 variant is promoted.

**Next recommended experiment:** one bounded C1 run that adds minimum-powered EO/SWIR backends and a real pupil relay/dichroic plane to A6_f1p0. It must preserve exact EFL/f-number, trace full fields and both stop images, quantify primary-hole/secondary/spider vignetting, and estimate f/1 primary fabrication/structure cost and alignment. Stop early and park C02 if the relays need large extra optics, lose the current pupil survival, or if the primary/hole manufacture dominates the common-LOS benefit. Do not begin detailed optimization before that gate.

## Resource use and integrity

Four substantial bounded model batches: direct speed/backfocus sweep, direct downstream-stop pupil-image sweep, afocal compression sweep, and fast-primary afocal check. Two materially distinct physical model experiments, zero prescription optimizer calls and no plateau. Final artifact generation took 2.96 s; interactive API/sign probes and the independent dense replay were cheap diagnostics. No package installation or human optical correction occurred. The user's published-example pupil-ratio observation is recorded as a useful research intervention.

`reference/` was not accessed. No historical Track A/B prescription or run was changed. Run 015 closes here without backend optimization.
