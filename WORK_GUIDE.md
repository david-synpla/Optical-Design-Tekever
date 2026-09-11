# Work Operating Instructions

1. Work only inside the `Optical Design - Tekever` project unless explicitly instructed otherwise.

2. Run scientific Python through Ubuntu on WSL, using the project's configured Linux Python environment. Do not fall back to the bundled ChatGPT/Codex Windows Python unless explicitly authorized.

3. Before a substantive optical-design run, read:
   - `requirements/eo_swir_system_requirements.yaml` for Track C substantive work;
   - `requirements/eo_requirements.yaml` only for historical Track A/B work;
   - `OPTICAL_DESIGN_RULES.md`
   - `DESIGN_WORKFLOW.md`
   - `BENCHMARK_TRACKS.md`
   - `benchmark_protocol.md`
   - `design_state.md`
   - `TRACK_C_STATE_OF_THE_ART_RESEARCH.md` for Track C work

4. Never read, inspect, search, infer from, or otherwise use `reference/` during the blind phase.

5. Use Optiland as the primary optical-design and ray-tracing engine unless a task genuinely requires another tool.

6. Use reproducible scripts rather than notebooks for design, optimization, analysis and reporting.

7. Do not install extra packages unless the requested task cannot reasonably be completed with the existing environment. If additional software is required, justify it briefly and keep the environment reproducible.

8. During Track A, do not perform broad external searches for existing telescope architectures or known solutions to this TEKEVER requirement set. General optical-engineering knowledge is allowed. During Track B, use the approved research briefing and only perform further external research when permitted by the benchmark instructions.

9. Do not invent missing customer requirements. Clearly distinguish:
   - explicit customer requirements;
   - derived quantities;
   - engineering assumptions;
   - design choices;
   - optimization results.

10. Manage architecture exploration, candidate branching and lifecycle state according to `DESIGN_WORKFLOW.md`.
    - maintain stable candidate identities;
    - preserve meaningful competing branches;
    - park rather than prematurely discard candidates that may become useful again;
    - do not preserve weak alternatives solely to create variety;
    - start a new candidate for a materially different architecture;
    - normally start a new run when the engineering question or architecture changes materially.

11. Use staged optimization and engineering judgement.
    - screen broadly and cheaply;
    - spend detailed optimization effort on the most promising candidates;
    - verify physical effects before freezing a candidate;
    - preserve concise evidence for rejected or parked alternatives.

12. Apply the resource/stopping rules in `DESIGN_WORKFLOW.md`.
    - normally stop a substantive run after about 30 minutes of active optical-design/optimization work or about 10 substantial computational searches, whichever comes first;
    - normally permit no more than 5 materially distinct optimization attempts for one candidate at one development stage;
    - declare a stage plateaued after 3 consecutive materially distinct attempts without meaningful improvement;
    - use about 5% optical-metric improvement or a clear engineering/Pareto improvement as the default definition of meaningful progress;
    - do not pretend to know the user's remaining ChatGPT/Codex quota percentage unless a reliable programmatic signal is actually available;
    - when a default budget is reached, finish the currently executing optimizer, preserve the best result, make an explicit candidate decision, close the run, and report;
    - request additional budget rather than silently extending a run indefinitely.

13. Optical performance is not the only objective. Treat manufacturability, robustness, complexity, engineering risk, packaging and expected cost as design considerations throughout the process.
    - for every substantive Track C run, treat mass and package volume as continuous optical-design objectives, not a post-prescription review;
    - co-track largest optic/external aperture, characteristic or folded length, bounding-box dimensions/volume, major-optic mass proxy, large-optic count/sizes, duplicated/shared structure, focus/mechanism count, structural/gimbal consequences, optical performance and manufacturing/cost;
    - label assumptions and exclusions; do not invent hard UAV mass or volume limits;
    - use Pareto reasoning during optimization and preserve earlier non-dominated variants when optical improvement costs material SWaP or economics;
    - treat C01 as the practical reference/fallback for Track C comparisons, not as the automatic overall leader.

14. Prefer compact decision-oriented outputs over long prose. Keep detailed numerical data in files.

15. Save every meaningful design result under a new immutable `runs/run_XXX/` directory. Never overwrite a previous meaningful run.

16. When practical, include `metadata.json` in each run identifying:
    - track;
    - candidate ID(s);
    - purpose;
    - stage;
    - parent run where relevant;
    - substantial search/optimizer count;
    - materially distinct attempt count;
    - plateau status.

17. Every serious candidate must be reproducible from saved code, prescription/configuration, assumptions, wavelength and field sampling, optimization criteria and software environment information.

18. Keep `design_state.md` as the concise current candidate/engineering dashboard. Do not use it as a transcript.

19. Record any human correction that materially changes the optical design, assumptions, optimization strategy, model implementation or engineering judgement. Human intervention is part of the benchmark. Procedural workflow changes should be recorded separately from optical-design corrections.

20. Before accessing the known TEKEVER reference design, freeze and commit the relevant blind-track portfolio in accordance with `DESIGN_WORKFLOW.md`.

21. For final frozen candidates, prepare the independent OpticStudio/Zemax handoff described in `ZEMAX_HANDOFF.md`. Do not silently alter the prescription merely to make export easier.

22. At the end of each substantive design invocation, report concisely:
    - best current result(s);
    - candidate status changes;
    - failed or unmet constraints;
    - important assumptions;
    - resource/stopping-budget status;
    - manufacturability/cost concerns;
    - the single most useful next action.
