# Blind Benchmark Protocol

## Objective

Test whether ChatGPT/Codex can produce technically credible EO telescope designs from the supplied TEKEVER requirements without access to the known TEKEVER prescription, and compare autonomous design against research-informed design.

## What is being tested

1. Correct optical modelling.
2. Architecture exploration and suitability.
3. Numerical optimization quality.
4. Engineering judgement.
5. Manufacturability and robustness.
6. Cost-aware trade-off reasoning.
7. Reproducibility and traceability.
8. Autonomy: amount and type of human correction required.
9. Computational/resource efficiency.
10. Value added by preliminary state-of-the-art research.

## Benchmark policy, not customer requirements

Because the source does not specify image-quality targets, the blind design may use the following as optimization/comparison objectives only:

- minimize polychromatic RMS spot / wavefront error over the full active sensor field;
- report MTF at detector-relevant spatial frequencies;
- avoid vignetting over the active field;
- preserve specified EFL/IFOV, f-number, spectral band, and 800 m focusing capability;
- prefer simpler, more robust and more manufacturable solutions when useful performance is comparable;
- prefer lower-cost/lower-risk solutions when useful performance is comparable;
- initially prefer conventional surfaces and common materials unless greater complexity is justified.

These are benchmark rules, not inferred TEKEVER customer requirements.

## Resource-governance policy

The benchmark measures whether the AI allocates computational effort sensibly.

Use the default stopping rules defined in `DESIGN_WORKFLOW.md`, including:

- approximately 30 minutes of active optical-design/optimization work per substantive run;
- approximately 10 substantial computational searches per run;
- no more than about 5 materially distinct optimization attempts for one candidate at one development stage;
- a plateau decision after 3 consecutive materially distinct attempts without meaningful improvement;
- about 5% improvement in the principal optical metric, or a clear engineering/Pareto gain, as the default indication of meaningful progress.

These are workflow heuristics, not optical requirements.

Do not assume direct visibility into the user's ChatGPT/Codex quota percentage. If a reliable quota signal later becomes programmatically available, it may be added as an additional guardrail without replacing the engineering stopping rules.

## Benchmark stages

A. Environment verification.

B. Track A autonomous architecture exploration and screening.

C. Track A candidate development.

D. Track A verification and engineering assessment.

E. Freeze Track A blind portfolio.

F. Perform the separate state-of-the-art architecture research and prepare the Track B briefing.

G. Track B research-informed architecture exploration and screening.

H. Track B candidate development.

I. Track B verification and engineering assessment.

J. Freeze Track B blind portfolio.

K. Reveal the known TEKEVER design.

L. Compare Track A, Track B and the known design.

M. Attempt reproduction/explanation/improvement of the known design if useful.

N. Change one meaningful requirement and test redesign capability.

## Required outputs per meaningful numerical run

Create `runs/run_XXX/` containing, as applicable:

- `summary.md` — concise decision-oriented engineering summary;
- `metadata.json` — track, candidate IDs, purpose, stage, and resource counters;
- `prescription.csv` — surfaces, radii, thicknesses, materials, apertures;
- `metrics.json` — EFL, f-number, FoV and relevant performance/constraint metrics;
- `layout.png`;
- `spot.png`;
- `mtf.png` when available;
- `wavefront.png` when available;
- the reproducible Python/Optiland model or script used for that run.

Not every screening run needs every plot if the omitted output would add no engineering value.

At the end of each run, update `design_state.md` with conclusions and candidate status only, not a transcript.

## Run-boundary rule

A run should normally answer one principal engineering question.

If a materially different architecture or engineering question emerges, preserve the result that motivated the change, close the current run, and begin the new direction in a new run/candidate as appropriate.

Do not allow a run to become an indefinitely expanding architecture search.

## Final track output

Each blind track should freeze:

- every preserved final candidate prescription/model;
- the candidate portfolio and recommendation, if one is justified;
- requirement compliance;
- performance results;
- manufacturability assessment;
- cost-driver assessment;
- robustness/engineering-risk assessment;
- unresolved limitations;
- design genealogy and key supporting runs;
- resource-use summary;
- human interventions.

Final candidates should also be prepared for independent Zemax/OpticStudio validation according to `ZEMAX_HANDOFF.md`.
