# TEKEVER Design Workflow

## 1. Purpose

This file defines how optical-design candidates, numerical runs, branching decisions, and resource budgets evolve through the TEKEVER benchmark.

It complements:

- `OPTICAL_DESIGN_RULES.md` — engineering quality and optical-design rules;
- `BENCHMARK_TRACKS.md` — Track A versus Track B methodology;
- `benchmark_protocol.md` — benchmark stages and evaluation;
- `WORK_GUIDE.md` — local execution rules;
- `ZEMAX_HANDOFF.md` — final OpticStudio validation handoff.

The workflow must support autonomous optical design without allowing one candidate or optimization loop to consume unlimited compute.

---

## 2. Candidate versus run

A **candidate** is a continuing optical-design lineage or architecture.

A **run** is one bounded engineering investigation: screening, optimization, comparison, verification, or maturity study.

A candidate may span many runs.

A run may compare multiple closely related candidates when that comparison is its explicit purpose.

Do not treat a run number as a candidate identity.

### Candidate IDs

Use stable candidate IDs within each benchmark track:

- Track A: `A01`, `A02`, `A03`, ...
- Track B: `B01`, `B02`, `B03`, ...

When one candidate is derived from another, preserve the genealogy explicitly.

Example:

- `A01` — bare two-mirror Cassegrain-type baseline
- `A02` — derivative of `A01` with a near-focus field corrector

Do not renumber candidates merely because their ranking changes.

---

## 3. Candidate lifecycle

Each serious candidate should have one of these states:

- `PROPOSED` — identified but not yet screened.
- `SCREENING` — undergoing inexpensive first-order or preliminary evaluation.
- `ACTIVE` — sufficiently promising to justify continued development.
- `PARKED` — not currently receiving effort but potentially worth reopening.
- `REJECTED` — evidence indicates continued work is not justified under the current requirements.
- `FROZEN` — preserved as part of a completed blind-track portfolio.

Prefer `PARKED` over `REJECTED` when the design may become attractive again if another branch exposes a worse trade-off.

A parked or rejected candidate may be reopened only for a clear engineering reason, which must be recorded.

---

## 4. Development stages

Use computational effort progressively.

### 4.1 Screening

Use first-order analysis, simple models, bounded sweeps, or other inexpensive methods to eliminate clearly poor directions.

Do not require final-quality optimization from every architecture.

### 4.2 Development

Build and optimize realistic models for promising candidates.

Release degrees of freedom progressively and preserve reproducibility.

### 4.3 Verification

For candidates that remain promising, verify the physical effects relevant to the architecture, including as applicable:

- real clear apertures;
- obscurations;
- vignetting;
- complete field and wavelength coverage;
- MTF, spot and wavefront performance;
- distortion;
- finite-conjugate focusing;
- detector sampling;
- physical packaging consequences.

Do not convert benchmark objectives into customer requirements.

### 4.4 Engineering maturity

For final contenders, assess practical consequences such as:

- manufacturability;
- alignment and assembly sensitivity;
- tolerancing where meaningful;
- thermal sensitivity where meaningful;
- coatings and materials;
- component availability;
- metrology burden;
- likely cost drivers;
- mechanical and packaging implications.

---

## 5. Branching and parallel exploration

The workflow is intentionally multi-branch.

Codex may:

- develop several candidates during the same benchmark stage;
- create a derivative candidate from an existing one;
- park one candidate while another is investigated;
- reopen a parked candidate if later evidence changes the trade space;
- compare multiple candidates in one run when direct comparison is efficient.

Do not force all work into the currently leading architecture.

Do not preserve weak alternatives merely to create variety.

A materially different architecture should normally receive a new candidate ID.

A materially different architecture exploration should normally begin in a new run rather than being appended indefinitely to the previous run.

---

## 6. Run definition

Before a substantive run begins, define its engineering question.

Examples:

- Does a minimal near-focus corrector materially improve a flat-sensor Cassegrain?
- Can explicit obscuration be reduced without unacceptable image-quality loss?
- Does a coaxial three-mirror architecture deserve development beyond screening?

A run should normally answer one principal engineering question.

If the work uncovers a new architecture or a substantially different engineering question, close the current run cleanly and start a new run.

Every meaningful numerical run uses a new immutable directory:

`runs/run_XXX/`

Never overwrite a previous meaningful run.

---

## 7. Default resource and stopping budget

Resource limits are benchmark-governance rules, not customer requirements.

The system should not assume it can directly measure the user's ChatGPT/Codex quota percentage. Use the proxy budgets below unless a reliable quota signal is explicitly available.

### 7.1 Per-run soft budget

A substantive autonomous run should normally stop after the first of:

- approximately **30 minutes of active optical-design/optimization work**;
- approximately **10 substantial computational searches or optimizer invocations**;
- completion of the run's stated engineering question.

Do not terminate an optimizer merely because the clock crosses the budget while that optimizer is already executing. Allow the current invocation to finish, then make a stop/continue decision.

File writing, result summarization, Git operations, and very cheap diagnostic calculations do not count as substantial optimizer invocations.

### 7.2 Candidate/stage attempt budget

Within one candidate at one development stage:

- normally allow no more than **5 materially distinct optimization attempts**;
- after **3 consecutive materially distinct attempts without meaningful engineering improvement**, declare the current branch plateaued for that stage.

A materially distinct attempt changes something meaningful such as:

- optimization parameterization;
- physically relevant design freedom;
- corrector concept;
- merit strategy;
- architecture geometry;
- optimizer/search strategy.

Changing only a random seed or making a trivial bound adjustment does not reset the plateau counter.

### 7.3 Meaningful improvement

An attempt counts as meaningful improvement if it produces either:

- approximately **5% or greater improvement** in the principal optical-performance metric relevant to that run; or
- a clear Pareto/engineering improvement such as:
  - fewer or simpler optical surfaces;
  - lower obscuration;
  - weaker aspheres/conics;
  - improved manufacturability;
  - reduced alignment sensitivity;
  - reduced cost/risk;
  - improved packaging;
  - better requirement compliance.

Small numerical improvements that do not change the engineering decision do not reset the plateau counter.

The 5% value is a workflow heuristic, not a physical requirement and not a universal optical-quality threshold.

### 7.4 What happens at a stop condition

When a budget or plateau condition is reached:

1. preserve the best valid result;
2. record the attempts and the evidence for diminishing returns;
3. make an explicit candidate decision:
   - advance to the next stage;
   - remain active but continue in a new run;
   - park;
   - reject;
   - branch to a different candidate;
4. close the current run;
5. update `design_state.md`;
6. commit at an appropriate engineering milestone.

Do not continue merely because another optimization can be imagined.

### 7.5 Exceptional continuation

If the AI believes exceeding a default budget is unusually valuable, it should stop and explain:

- why the current evidence justifies more compute;
- what specific unresolved question the extra budget would answer;
- what additional work is proposed.

It should request continuation rather than silently extending the run indefinitely.

---

## 8. Run metadata

Each run should contain the normal benchmark outputs and, when practical, a `metadata.json` with at least:

- track;
- run ID;
- candidate ID or candidate IDs;
- parent/preceding run where relevant;
- purpose;
- development stage;
- start/end time if available;
- substantial optimizer/search count;
- materially distinct attempt count;
- plateau counter;
- commit identifier when useful.

The exact schema may evolve. Metadata must not become more expensive than the engineering work it supports.

---

## 9. `design_state.md`

`design_state.md` is the current engineering dashboard, not the detailed historical record.

It should summarize:

- current benchmark track and stage;
- active candidate portfolio;
- each serious candidate's ID, architecture, lifecycle status, best supporting run, main strength and main risk;
- important established conclusions;
- open engineering questions;
- current resource/plateau status where relevant;
- the most useful next work.

Detailed calculations remain in run directories.

A new Codex session should be able to understand the current design situation from `design_state.md` and then open only the runs needed for the task.

---

## 10. Candidate comparison

First determine whether a candidate satisfies the explicit source requirements that apply to it.

Among technically viable candidates, compare engineering trade-offs such as:

- optical performance;
- manufacturability;
- robustness;
- cost drivers;
- complexity;
- size/packaging;
- alignment difficulty;
- procurement or metrology risk.

Do not invent hard pass/fail thresholds for properties the customer did not specify.

---

## 11. Pareto portfolio

The end of a benchmark track does not require a single universal winner.

Preserve a small set of genuinely non-dominated candidates when they represent materially different useful trade-offs.

A candidate is worth preserving when it is meaningfully better in one or more important engineering dimensions and alternatives are better in others.

Do not impose a fixed number of final candidates.

If one candidate is clearly preferred under the available requirements and engineering evidence, identify it as the recommendation while still preserving meaningful non-dominated alternatives.

Do not manufacture artificial "cheap", "balanced", or "high-performance" designs unless those trade-offs genuinely emerge from the engineering.

---

## 12. Track freeze

### Track B cost-conscious evidence gate (user instruction, 2026-09-07)

Maintain both a performance lane (B05 variants/B06 engineering and thermal work)
and a cost-conscious lane. Before Track B final selection/freeze, either retain
at least one credibly evaluated lower-cost COTS/hybrid option or document why
the investigated low-cost routes fail to offer an acceptable performance/cost
trade. Performance-lane maturity alone does not satisfy this gate. Compare
procurement, NRE, manufacturing, alignment, supply and qualification risks;
do not treat retail prices as production quotations or require the cheaper
candidate to equal the leading optical metrics. Use separate bounded runs.
See Run 011 for the initial selection gate and source request.

The already-planned matched B05/B06 thermal/material study has priority as the
next performance-lane development step; cost-lane work must not replace or
consume its budget. For proprietary COTS designs, distinguish unverified
performance due to unavailable prescriptions from poor predicted performance.
Do not assign a poor optical score merely because a model is unavailable.

Before a track is declared complete:

1. complete the required verification for every candidate being preserved;
2. record manufacturability, cost and engineering-risk assessments;
3. identify unresolved limitations;
4. freeze the candidate prescriptions and supporting models;
5. freeze the track portfolio;
6. commit the frozen result to Git.

For Track A, no state-of-the-art architecture briefing or known TEKEVER reference design may be accessed before the Track A portfolio is frozen.

For Track B, the research briefing is permitted but the known TEKEVER reference design remains hidden until Track B is frozen.

---

## 13. Zemax handoff

Final frozen candidates should be prepared for independent OpticStudio validation in accordance with `ZEMAX_HANDOFF.md`.

The Optiland model remains the source of the AI design history. The Zemax representation is an independent validation handoff and must not silently change the optical prescription.
