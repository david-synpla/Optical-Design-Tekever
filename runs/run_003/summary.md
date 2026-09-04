# Track A Run 003 - A04 Coaxial TMA Physical Screen

## Decision

Reject A04's coaxial topology at the screening stage. The Run 002 seed's attractive nominal 4.7/3.0/3.1/4.9 um monochromatic RMS spots are not physically usable: the pre-tertiary beam passes through the centered detector location, reaching only 0.59 mm minimum radius on axis versus a 7.96 mm keepout benchmark assumption.

Three materially distinct constrained attempts did not produce a meaningful physically valid improvement. Attempt 1 retained useful nominal spots and EFL but only 0.30 mm minimum clearance. Attempt 2 used a long return geometry and restored approximately 793.95 mm EFL with 1.4-9.7 um RMS, yet clearance remained 0.29 mm. Attempt 3 hard-constrained the long return and strengthened clearance weighting; it still achieved only 1.53 mm worst-field clearance, missed EFL at 815.58 mm, and degraded RMS spots to approximately 77-80 um. The stage is plateaued under workflow v3.

The 7.96 mm keepout is not a customer requirement; it is the active sensor half-diagonal plus a 1 mm radial screening margin. Even the active area alone would obstruct every attempted layout. MTF and wavefront outputs are omitted because no physically clear candidate survived.

## Engineering consequence

The failure is topological rather than evidence against all three-mirror systems. A centered detector on the coaxial tertiary return path conflicts with the incoming beam. A materially different off-axis/decentered three-mirror branch may avoid this, but it must receive a new candidate ID and run because its alignment, fabrication and packaging trade space differs.

**Next action:** open a separate bounded screening run for an off-axis/decentered reflective branch and compare its mechanical feasibility against parked A01.
