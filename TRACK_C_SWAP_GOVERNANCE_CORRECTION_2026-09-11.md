# Track C SWaP governance correction — 2026-09-11

## User correction

Track C develops a UAV payload. Mass and package volume are first-class continuous design objectives and must influence optical architecture, variables, merit choices and branch decisions during optimization. They are not merely downstream checks applied after image quality is achieved.

Every substantive C-series run must therefore co-track the minimum evidence listed in `DESIGN_WORKFLOW.md` section 10.1, including aperture/optic scale, characteristic or folded length, bounding volume, major-optic mass proxy, optic counts, shared/duplicated structure, mechanisms, structural/gimbal effects, optical performance and manufacturing/cost. No hard mass or volume limit may be invented without new source input.

Pareto reasoning applies throughout. An optically improved candidate is not automatically preferred if it materially worsens mass, volume, cost or integration, and earlier non-dominated variants remain preserved. C01 is the practical low-coupling reference/fallback, not a presumed overall leader.

## Files changed

- `DESIGN_WORKFLOW.md`: adds the persistent Track C continuous optical/SWaP co-optimization rule and required run evidence.
- `WORK_GUIDE.md`: adds the corresponding mandatory execution checklist for future sessions.
- `design_state.md`: records the live portfolio interpretation and removes leader-like wording from C01.
- `runs/run_016/swap_screen.json`: applies the correction immediately to the current A6F1 milestone.

This is a procedural governance correction, not an optical prescription change and not a customer requirement change. Historical runs remain immutable.
