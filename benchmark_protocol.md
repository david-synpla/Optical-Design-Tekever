# Blind Benchmark Protocol

## Objective

Test whether ChatGPT can produce a technically credible EO telescope design from the supplied requirements without access to the known TEKEVER prescription.

## What is being tested

1. Correct optical modelling.
2. Architecture suitability.
3. Numerical optimization quality.
4. Engineering judgement and manufacturability.
5. Autonomy: amount of human correction required.

## Benchmark policy, not customer requirements

Because the source does not specify image-quality targets, the blind design may use the following only as optimization objectives:

- minimize polychromatic RMS spot / wavefront error over the full sensor field;
- report MTF at detector-relevant spatial frequencies;
- avoid vignetting over the active field;
- preserve specified EFL/IFOV, f-number, spectral band, and 800 m focusing capability;
- prefer a simpler, manufacturable solution when two solutions perform similarly;
- initially prefer spherical/conic surfaces and common optical materials unless a more complex surface is clearly justified.

These are benchmark rules, not inferred TEKEVER customer requirements.

## Stages

A. Environment smoke test.
B. Architecture chosen in normal Chat.
C. First-order model.
D. Nominal optimization.
E. Performance verification.
F. Freeze blind candidate.
G. Reveal known TEKEVER design and compare.
H. Requirement-change redesign test.

## Required outputs per numerical run

Create `runs/run_XXX/` containing:

- `summary.md` - maximum 500 words;
- `prescription.csv` - surfaces, radii, thicknesses, materials, apertures;
- `metrics.json` - EFL, f-number, FoV, distortion, spot/WFE/MTF metrics and constraint violations;
- `layout.png`;
- `spot.png`;
- `mtf.png` when available;
- `wavefront.png` when available;
- the Python script/model used for that run.

At the end, update `design_state.md` with conclusions only, not a transcript.
