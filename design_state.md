# Current Design State

Phase: blind benchmark - Run 002 complete; architecture exploration reopened; paused for workflow-v2
Telescope: EO only
Architecture: on-axis two-conic-mirror Cassegrain-type remains a viable baseline but is not selected or frozen; tested minimal correctors rejected

## Design history

- 2026-09-04: `WORK_GUIDE.md` was updated after the initial Track A design invocation and completion of `run_001`. The updated operating rules apply prospectively. `run_001` remains unchanged as the pre-update baseline. `BENCHMARK_TRACKS.md` was requested for the governing reread but was not present in the project, so no subsequent optical-design run was started.
- 2026-09-04: `BENCHMARK_TRACKS.md` became available and Run 002 compared the physical two-mirror baseline with minimal singlet and cemented-achromat correctors, explicitly modelled apertures, and verified the 800 m finite-conjugate focus shift.
- 2026-09-04: Human intervention stopped extension of Run 002 into detailed TMA or renewed architecture optimization and required a pause until workflow-v2 is installed. The already-running bounded TMA sweep was allowed to finish and is retained only as screening evidence for a separate future run.

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
- Run 002 confirms that the explicitly obstructed bare two-mirror baseline remains viable, with approximately 79.5% aperture throughput before spider, coating and baffle losses, but remains flat-field limited.
- A 4 mm fused-silica singlet modestly improves the corner while degrading the center and adding wavelength dependence; its added complexity is not justified.
- A 5.5 mm cemented N-BK7/N-F2 achromat improves parts of the middle field but does not improve the worst field sufficiently to justify three refracting surfaces, two glasses and a cemented interface.
- Full-ray on-axis optimization verifies that the 800 m finite conjugate requires approximately +0.844 mm detector refocus relative to infinity.
- A curved-image diagnostic confirms field curvature as the dominant remaining limitation for the flat IMX545, justifying reopened architecture exploration.
- A bounded TMA seed sweep showed potentially improved nominal flat-field performance, but the promising seed had only approximately 7.3 mm tertiary-to-detector clearance and nearly overlapping ray footprints. It is screening evidence only, not a developed Run 002 design.

## Open decisions for Chat

- which architecture to investigate after the workflow-v2 files are installed and read;
- whether a separately developed TMA can provide practical mechanical clearance without self-obscuration;
- physical primary hole, spider, baffles and resulting obscuration/vignetting;
- practical detector-refocus mechanism for the verified 800 m focus shift;
- tolerance, thermal and stray-light performance;
- practical packaging/manufacturing constraints to add, if they existed in the original project.

## Last reviewed run

run_002 - Track A physical baseline and minimal-corrector comparison; architecture work paused pending workflow-v2
