# Current Design State

Phase: blind benchmark - architecture selected; preliminary model complete
Telescope: EO only
Architecture: on-axis two-conic-mirror Cassegrain-type baseline; evaluate a minimal near-focus spherical field corrector

## Design history

- 2026-09-04: `WORK_GUIDE.md` was updated after the initial Track A design invocation and completion of `run_001`. The updated operating rules apply prospectively. `run_001` remains unchanged as the pre-update baseline. `BENCHMARK_TRACKS.md` was requested for the governing reread but was not present in the project, so no subsequent optical-design run was started.

## Fixed source requirements

See `requirements/eo_requirements.yaml`.

## Established conclusions

- EFL is approximately 794.2 mm from pixel pitch / IFOV.
- Entrance pupil is approximately 128.1 mm if f/6.2 is exact.
- Active pixel array implies approximately 0.8096 deg x 0.5930 deg FoV.
- Missing image-quality and packaging requirements must not be invented as customer requirements.
- Run 001 screened scaled doublet, triplet, multi-element telephoto and two-mirror candidates over 0.43, 0.55, 0.65 and 0.80 um.
- The refractive seeds were rejected because band-edge RMS spot radii remained approximately 0.1-0.2 mm; their length, glass mass and thermal behavior also compare poorly.
- The two-mirror seed preserves approximately 794.2 mm EFL and f/6.2 and is achromatic. Its RMS spot radius is approximately 3.4 um on axis and 8.8 um at the sensor-corner field.
- Its 0.55 um geometric MTF at the 182.5 cy/mm detector Nyquist frequency is low (approximately 0.025 on axis and below 0.016/0.007 tangential/sagittal at the corner), so it is not a final design.
- The estimated secondary footprint is 42.6% of the entrance-pupil diameter before mechanical margin. Explicit obscuration and vignetting remain unmodelled.
- The secondary conic of approximately -6.58 is a manufacturing/metrology risk.
- Full-aperture catadioptric and unobscured off-axis/three-mirror families were rejected at screening level because their large corrector or alignment/metrology burden is not yet justified.

## Open decisions for Chat

- whether a minimal near-focus spherical corrector materially improves corner MTF without unacceptable color, cost or sensitivity;
- physical secondary size, primary hole, baffles and resulting obscuration/vignetting;
- optimization merit-function balance between MTF/spot, obscuration, conic strength and corrector simplicity;
- whether the 800 m focus requirement is handled by detector refocus, group motion, or passive depth of focus;
- practical packaging/manufacturing constraints to add, if they existed in the original project.

## Last reviewed run

run_001 - Track A first-order architecture screening
