# TEKEVER ChatGPT Optical Design Benchmark

Purpose: benchmark ChatGPT optical-design capability against an existing TEKEVER telescope design while keeping the known solution hidden until the blind design is complete.

## Operating split

- Chat: requirements, derivations, architecture decisions, merit-function strategy, review, and next-step decisions.
- Work: local code/file operations, Optiland model construction, numerical optimization, analyses, plots, and run outputs.

## Blind-test rule

Do not expose anything in `reference/` to Work until the blind nominal design has been frozen.

## Order of work

1. Run `environment_setup.ps1` manually.
2. Open this folder in ChatGPT desktop Work.
3. Give Work `prompts/01_environment_smoke_test.txt`.
4. Review the smoke-test result in normal Chat.
5. Decide the first optical architecture in Chat.
6. Put that decision in `design_state.md`.
7. Give Work `prompts/02_nominal_design.txt`.
8. Bring the concise Work run summary back to Chat for review.
9. Iterate one narrowly-scoped optimization task at a time.
10. Freeze the blind result before revealing `reference/`.

## Quota discipline

- One architecture per Work invocation.
- No broad literature research in Work unless specifically requested.
- No package installation after setup unless a missing capability is demonstrated.
- No long narrative reports from Work; save compact machine-readable metrics and a short summary.
- Do not let Work reconsider requirements or top-level architecture unless Chat explicitly asks it to.
