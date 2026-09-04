# Workflow v3 — Changes

This package supersedes the earlier workflow-v2 package. Do not install both.

Main changes:

1. Added explicit run versus candidate separation.
2. Added stable Track A / Track B candidate IDs.
3. Added candidate lifecycle: proposed, screening, active, parked, rejected, frozen.
4. Added multi-branch design exploration and final Pareto portfolio.
5. Added a run-boundary rule: materially new architecture/questions normally start a new run.
6. Added default resource governance:
   - ~30 minutes active optimization per substantive run;
   - ~10 substantial computational searches per run;
   - max ~5 materially distinct attempts per candidate/stage;
   - plateau after 3 consecutive non-improving attempts;
   - ~5% main optical-metric improvement or clear engineering/Pareto gain as meaningful progress.
7. Added explicit rule not to assume direct visibility of ChatGPT/Codex quota percentage.
8. Added escalation rule: request more budget instead of silently continuing indefinitely.
9. Added resource counters to run metadata and final benchmark assessment.
10. Preserved the Track A / Track B contamination-control methodology.
11. Preserved the final Zemax/OpticStudio validation handoff.
12. Runs 001 and 002 should remain historical and unchanged when this workflow is installed.
