# TEKEVER Benchmark Tracks

## Objective

Compare two AI-assisted optical-design workflows while keeping the source requirements, software environment, common engineering rules, resource-governance policy, and final evaluation framework as similar as practical.

The principal experimental variable is the presence or absence of a dedicated state-of-the-art architecture briefing.

## Track A — Autonomous / Uninformed

Track A receives:

- the source TEKEVER requirements;
- normalized/derived requirement files;
- the common optical-design rules;
- the design workflow and resource/stopping rules;
- the benchmark protocol;
- the available optical-design software environment.

Track A does **not** receive a dedicated state-of-the-art architecture briefing.

During Track A:

- general optical-engineering knowledge may be used normally;
- the AI should explore and manage the architecture/design space autonomously;
- external searching specifically for existing solutions to this TEKEVER requirement set is prohibited;
- `reference/` is inaccessible;
- multiple design branches may be developed, parked, rejected, reopened, or preserved;
- the final result may be a small portfolio of non-dominated blind candidates rather than one forced winner;
- runs remain bounded by the shared resource/stopping rules.

Track A must be frozen before the Track B research briefing is prepared or exposed to the design agent.

## Track B — Research-Informed

Track B starts again from the original requirements and common engineering rules.

Before Track B begins, a separate state-of-the-art review will be prepared outside the autonomous Track A design process.

The briefing may include:

- relevant telescope architecture families;
- comparable systems;
- literature, patents, or commercial examples;
- typical advantages and disadvantages;
- aberration-correction strategies;
- manufacturability and cost considerations;
- packaging and alignment challenges.

The briefing should inform the design search without prescribing the final architecture.

Track B must not start from Track A's optimized prescription. It may learn from the external research briefing, not from hidden knowledge of the known TEKEVER design.

Track B may also finish with a small portfolio of non-dominated candidates.

Use the same default run budgets and plateau rules as Track A unless the benchmark is explicitly changed.

## Contamination control

1. Freeze Track A before preparing or exposing the Track B research briefing.
2. Keep Track A and Track B candidate identities and outputs distinct.
3. Do not expose the known TEKEVER reference design to either track before both blind-track results are frozen.
4. Record human interventions separately for each track.
5. Record procedural workflow/budget changes separately from optical corrections.
6. Use the same final evaluation framework for both tracks.
7. Do not retroactively modify Track A designs after Track B research begins.

## Final comparison

After both blind tracks are frozen, compare:

- Track A portfolio;
- Track B portfolio;
- known TEKEVER reference design.

Assess at least:

- explicit requirement compliance;
- optical performance;
- manufacturability;
- robustness;
- complexity;
- expected cost and cost drivers;
- packaging;
- alignment/metrology risk;
- computational efficiency;
- AI autonomy and human corrections;
- quality of reasoning, reproducibility and traceability.

The experiment should determine not only whether AI can produce a credible telescope design, but also how much value is added by preliminary architecture research and how efficiently the AI allocates computational effort.
