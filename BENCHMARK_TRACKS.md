# TEKEVER Benchmark Tracks

## Objective

Compare two AI-assisted optical-design workflows while keeping the requirements, software environment, design rules and final evaluation criteria as similar as possible.

## Track A — Autonomous / Uninformed

The AI receives:
- the TEKEVER requirements;
- the common optical-design rules;
- the benchmark protocol;
- the available optical-design software environment.

The AI does **not** receive a dedicated state-of-the-art architecture briefing.

During Track A:
- the AI may use normal general optical-engineering knowledge;
- it must not search specifically for existing TEKEVER designs or known solutions to this requirement set;
- it must not inspect `reference/`;
- it should explore several materially different architecture families itself;
- it should freeze its best blind candidate before Track B research begins.

## Track B — Research-Informed

Track B starts from the original TEKEVER requirements and the same common design rules.

Before Track B begins, a separate state-of-the-art review will be prepared outside the autonomous design run. That review may include:
- relevant telescope architecture families;
- comparable systems;
- literature, patents or commercial examples;
- likely advantages and disadvantages;
- manufacturability and cost considerations;
- common aberration and packaging challenges.

The briefing should inform the AI without prescribing the final architecture.

Track B should not start from Track A's optimized prescription. It should restart from the original requirements plus the research briefing.

## Contamination control

1. Freeze Track A before preparing or exposing the state-of-the-art briefing to the design agent.
2. Keep Track A and Track B outputs in clearly separate run directories or branches.
3. Do not expose the known TEKEVER reference design to either track until both blind candidates are frozen.
4. Record human interventions separately for each track.
5. Use the same final evaluation framework for Track A and Track B.

## Final comparison

Compare:
- Track A blind candidate;
- Track B blind candidate;
- known TEKEVER reference design.

Assess at least:
- requirement compliance;
- optical performance;
- manufacturability;
- robustness;
- complexity;
- expected cost;
- engineering risk;
- AI autonomy / number of human corrections;
- quality of reasoning and traceability.

The purpose is to measure not only final design quality, but also the value added by the preliminary architecture research.
