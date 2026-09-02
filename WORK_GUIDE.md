# Work Operating Instructions

1. Work only inside the `Optical Design - Tekever` folder unless explicitly instructed otherwise.
2. Run scientific Python through Ubuntu on WSL, using the Linux interpreter path recorded in `python_path.txt`.
3. Read `requirements/eo_requirements.yaml`, `benchmark_protocol.md`, and `design_state.md` before a design run.
4. Never read `reference/` during the blind phase.
5. Use Optiland as the primary optical engine.
6. Use scripts, not notebooks, for reproducibility.
7. Do not install extra packages unless the requested task cannot be completed with the installed environment.
8. Do not search the web broadly. If Optiland API documentation is needed, search only enough to resolve the specific API issue.
9. Do not invent missing customer requirements. Put numerical modelling assumptions in the run summary.
10. Do not change the top-level architecture unless the task explicitly asks for an architecture change.
11. For each invocation, run at most three materially distinct optimization attempts before stopping for review unless explicitly instructed otherwise.
12. Prefer compact outputs over long prose.
13. Save every useful result under a new `runs/run_XXX/` directory; never overwrite a previous run.
14. Always finish with: best result, failed constraints, important assumptions, and the single most useful next action.
