# Run 006 — B04 independent CDK seed screen

Decision: B04 remains ACTIVE for a physical-pupil model, not promoted to verification or frozen. One bounded joint solve establishes enough potential to justify that next question. It does not establish superiority over B05/B06 or the COTS comparators. This closes the seed investigation; no further optimizer runs were appended.

## Result and limits

- Initial common-centroid six-wavelength/3 x 3 field worst RMS: approximately 126 um. Saved solution: 7.298 um. Wavelengths are 430, 500, 550, 650, 725 and 800 nm, at one shared image plane. This is geometric RMS, not diffraction-limited image quality.
- On-axis finite-difference image-scale estimate: 792.616 mm versus 794.203 mm target (about -0.20%); f/6.1876 with the original 128.097 mm pupil. No customer tolerance was supplied, so the nominal mismatch remains unresolved. This centroid derivative is not an independently verified paraxial EFL.
- A denser post-trace mask gives worst monochromatic centered RMS 7.890 um. It removes rays blocked by a provisional secondary and primary hole; it is not the same metric as the common-centroid broadband number above and does not prove a physical model.
- Sampled envelopes plus a labelled 1 mm radial margin suggest secondary diameter 68.84 mm, primary-hole diameter 40.42 mm and corrector lens diameters about 33.51/32.44 mm. The corresponding on-axis unobscured area fraction is 71.12%, before spider, coatings and baffles. Full-field radiometric throughput remains unverified.
- Lens edge thicknesses are approximately 3.57 and 3.28 mm; the common-edge air gap is positive (5.23 mm). These basic checks avoid an obvious lens-intersection loophole. True clear apertures, mirror sag, cells and the detector package remain unresolved.
- Vertex span is 408.45 mm, not a finished mechanical envelope. This value is a trade variable, not a package requirement.
- Primary f-number and paraxial backfocus approach their upper screening bounds (3.5 and 160 mm); secondary radius correction approaches -8%. These bounds are design assumptions, not requirements. Do not widen them merely to harvest small RMS improvements. Reparameterize around the measured EFL and real pupil before another attempt.

The solver used 430/550/800 nm, four radial field samples, a common image centroid, and a field-scale penalty. Validation expanded to six wavelengths and a 3 x 3 signed detector grid. It did not optimize Nyquist MTF. The diffraction references in Run 005 prevent interpreting red-edge Nyquist contrast as an attainable high-MTF target; actual B04 matched-pupil MTF and ensquared energy are still required. Calculating unclipped-pupil MTF now would conceal the substantial real obstruction, so no such candidate metric is reported.

## Provenance and reproducibility

All geometry starts from the original requirements and fresh first-order equations documented in `configuration.json`: f1 = primary speed x pupil; M = target EFL/f1; separation = (target EFL - backfocus)/(M+1); derive secondary radius from its conjugates. Initial speed 2.5 and backfocus 100 mm are engineering starting assumptions. Neither Track A prescription nor its code supplied any seed. Two separate BK7/F2 lenses, fixed initial center thicknesses and spherical surfaces were a low-cost first hypothesis, not a final material/element-count requirement.

`metrics.json` and `configuration.json` are the original saved optimizer outputs. `model_executed.py` preserves the exact executed source. `model.py`/the source script fix only root discovery and CSV export (Optiland stores the conic in `geometry.k`, not `geometry.conic`). `prescription.csv` is the deliberately retained incomplete failed export; use `prescription_complete.csv` plus the configuration instead. The complete export was checked against the Optiland primary conic -0.6383070282. This was an autonomous software correction, not a human optical intervention.

From the repository root, configured WSL Python can reconstruct the saved result without running the optimizer:

```python
import sys, json
sys.path.insert(0, 'runs/run_006')
import model
x = json.load(open('runs/run_006/configuration.json'))['best']
optic = model.build(x)
print(model.audit(x)['worst_rms_um'])
```

Run scripts refuse to reuse an existing numerical run directory. Copied Run 005 `screen.py` is an archival copy; use its committed `src/track_b_run005_screen.py` from a fresh replay checkout. Do not rerun artifact-writing audit scripts over closed original runs; replay into a separate checkout/output copy.

## Engineering and next gate

The spherical secondary avoids a convex aspheric null test. The ellipsoidal primary still needs controlled aspheric manufacture and metrology; four small spherical lens faces and conventional glass families look plausible but availability/coating selections are unverified. Obstruction, mirror despace/tilt, lens centering, glass dn/dT, differential structure expansion and a roughly 180 mm image-side path are cost/robustness drivers. No athermal or -25 to +50 C claim is supported. Full-field 800 m focus, tolerances, transmission and stray light are outstanding.

Most useful next action: one separately bounded B04 physical-pupil/first-order restoration run, including explicit central obscuration and primary hole, EFL constraint, matched-pupil diffraction MTF/ensquared energy, and finite-conjugate screening. Then compare B05 and B06 in their own independent runs; do not consume the whole portfolio budget polishing this seed.

Resource use: one substantial search, one materially distinct screening attempt, 14.26 seconds recorded optimizer/initial-audit wall time. Model construction and physical audit added several minutes of active engineering, below the 30-minute run budget. No plateau is claimed. Track B remains open; the invocation closes at this reviewable screening milestone, not at a final track freeze.

Validation note: the exact executed-source archive retains its original extra blank line at EOF. Staged whitespace validation excludes only that preserved evidence file; all authored final files pass. Track A freeze hashes still pass 7/7, and Git shows no changes to its runs, freeze artifacts or original requirements.
