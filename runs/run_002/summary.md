# Track A Run 002 Physical Baseline and Corrector Comparison

## Result

The physical bare two-mirror baseline remains viable, but it is not ready to freeze because it is flat-field limited. A 58 mm secondary/entrance obstruction and 130 mm primary clear diameter were modelled explicitly. Aperture throughput is about 79.5% before spider, coating and baffle losses. Full-ray on-axis optimization at the 800 m finite conjugate verifies a +0.844 mm detector shift from the infinity focus; the mechanical refocus implementation remains undesigned.

## Corrector decision

The 4 mm fused-silica meniscus improves the flat-field corner from about 8.0-8.8 um to roughly 6.3-7.4 um, but worsens the center to 5.0-6.6 um and introduces wavelength dependence. It adds two coated surfaces, a precision cell and thermal/focus sensitivity.

The 5.5 mm cemented N-BK7/N-F2 doublet improves portions of the middle field but leaves approximately 7.6-8.4 um at the corner and about 3.3-7.5 um on axis. Its three spherical surfaces, cemented interface, two glasses and procurement/alignment burden are not justified by that performance. Both minimal correctors are rejected.

## Diagnostic and architecture status

A curved image surface near -151 mm radius allows about 1.9-5.0 um monochromatic RMS across the sampled field. This demonstrates that field curvature is the dominant limitation for the flat IMX545, not chromatic aberration or a first-order EFL failure. The Cassegrain family remains viable, but the inability of minimal correctors to flatten the field justifies reopening architecture exploration.

A bounded TMA seed sweep was allowed to finish only as a screening diagnostic. Its more promising seed recovered 794.203 mm EFL magnitude and produced 4.7/2.9/3.3/5.8 um monochromatic RMS across the field. However, only 7.3 mm separated the tertiary and detector, while their ray-footprint radii were approximately 7.5 and 7.0 mm. The likely mechanical interference and unmodelled self-obscuration prevent treating this as a developed design. It is evidence for a separate future run only.

The mirror pair remains compact and achromatic but uses two aspheres, including a strong secondary conic, and substantial central obscuration. There is no customer image-quality or obscuration limit; spot and MTF comparisons are benchmark objectives.

**Next action:** install and read the workflow-v2 files before any further architecture optimization. Then open a separate run to compare an appropriately constrained flat-field architecture against this baseline.
