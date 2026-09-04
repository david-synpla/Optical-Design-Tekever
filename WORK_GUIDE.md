# Work Operating Instructions

1. Work only inside the `Optical Design - Tekever` project unless explicitly instructed otherwise.

2. Run scientific Python through Ubuntu on WSL, using the project’s configured Linux Python environment. Do not fall back to the bundled ChatGPT/Codex Windows Python unless explicitly authorized.

3. Before any optical-design run, read:
   - `requirements/eo_requirements.yaml`
   - `OPTICAL_DESIGN_RULES.md`
   - `BENCHMARK_TRACKS.md`
   - `benchmark_protocol.md`
   - `design_state.md`

4. Never read, inspect, search, infer from, or otherwise use `reference/` during the blind phase.

5. Use Optiland as the primary optical-design and ray-tracing engine unless a task genuinely requires another tool.

6. Use reproducible scripts rather than notebooks for design, optimization, analysis, and reporting.

7. Do not install extra packages unless the task cannot reasonably be completed with the existing environment. If additional software is required, justify it briefly and keep the environment reproducible.

8. During Track A, do not perform broad external searches for existing telescope architectures or known solutions to this TEKEVER requirement set. General optical-engineering knowledge is allowed. During Track B, use the supplied research briefing and only perform further external research if explicitly authorized.

9. Do not invent missing customer requirements. Clearly distinguish:
   - explicit customer requirements;
   - derived quantities;
   - engineering assumptions;
   - design choices;
   - optimization results.

10. Architecture exploration is governed by `OPTICAL_DESIGN_RULES.md` and `BENCHMARK_TRACKS.md`.
    - During exploratory stages, consider materially different architecture families where appropriate.
    - Do not lock onto the first plausible design without comparison.
    - Once an architecture has been deliberately selected or frozen for a particular candidate, do not silently change it. Record and justify any later architecture change.

11. Use staged optimization and engineering judgement.
    - Do not exhaustively optimize every possible architecture.
    - Spend detailed optimization effort on the most promising candidates.
    - Preserve meaningful failed or rejected alternatives with concise reasons.
    - Avoid arbitrary limits on the number of exploratory architectures, while keeping expensive optimization work efficient.

12. Optical performance is not the only objective. Treat manufacturability, robustness, complexity, engineering risk, and expected cost as design considerations throughout the process.

13. Prefer compact decision-oriented outputs over long prose. Keep detailed numerical data in files.

14. Save every meaningful design result under a new `runs/run_XXX/` directory or equivalent track-specific structure. Never overwrite a previous meaningful run.

15. Every serious candidate must be reproducible from saved code, prescription/configuration, assumptions, wavelength and field sampling, optimization criteria, and software environment information.

16. Record any human correction that materially changes the optical design, assumptions, optimization strategy, model implementation, or engineering judgement. Human intervention is part of the benchmark.

17. Before accessing any known TEKEVER reference design, freeze and commit the best blind candidate in accordance with `OPTICAL_DESIGN_RULES.md`.

18. At the end of each substantive design invocation, report concisely:
   - best current result;
   - failed or unmet constraints;
   - important assumptions;
   - architecture status;
   - manufacturability/cost concerns;
   - the single most useful next action.
