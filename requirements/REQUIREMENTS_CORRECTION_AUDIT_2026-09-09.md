# Requirements Correction Audit — Track C Initialization

Date: 2026-09-09
Starting repository commit: `ef3350f920d00e5b39aebfd2a2635c6a4f1ebadf`

## Correction

The project previously normalized and developed only the EO subset of the payload problem. `requirements/eo_requirements.yaml` remains unchanged as the historical baseline against which Tracks A and B were performed. It is not the authoritative requirements source for complete-system future work.

The new authoritative baseline is `requirements/eo_swir_system_requirements.yaml`. It records the required simultaneous, co-boresighted EO+SWIR payload; channel-specific source requirements; the adopted EO active width; first-order derived quantities; UAV engineering objectives; and quantities for which no customer pass/fail threshold exists.

## Historical classification

- Track A remains frozen and immutable as autonomous EO-only work against the legacy normalized EO subset. Its frozen commit is `b06af2c3b6c3e7bec4e4bf5b57f9249207d8a875` and its tag is `track-a-frozen`.
- Track B is preserved as research-informed EO-only work against that same incomplete subset. B05, B06, B09, and all other Track B evidence remain valid as EO engineering evidence. Track B does not represent the complete EO+SWIR payload, and its previous B09-only next action is superseded by Track C initialization.
- No historical run output is changed by this correction.

## Track C authority and boundaries

Track C is the complete-system EO+SWIR engineering-development phase. It may use lessons and evidence from Tracks A and B and the independent Track C research report. It must not access or use the known TEKEVER/team prescription or an architecture inferred from it.

The initial system-level candidate families are provisional research directions only:

- C01 — separate integrated EO and SWIR telescopes;
- C02 — common coaxial reflective fore-telescope with independent relays;
- C03 — common off-axis afocal/TMA front end with modular relays;
- C04 — cost/COTS-maximized dual-channel branch;
- C05 — compact folded/freeform stretch branch.

No candidate is selected, rejected, or numerically optimized by this milestone. The next authorized engineering action is Track C first-order optical plus SWaP architecture screening.

## Requirement taxonomy

- Source requirements: values directly supplied for the EO channel, SWIR channel, and simultaneous co-boresighted payload behavior.
- Adopted requirement: the 11.22304 mm EO active width selected to resolve the earlier listed-size inconsistency.
- Derived quantities: first-order EFL, pupil, FoV checks, and finite-range focus estimates. These are calculations, not customer requirements.
- Engineering objectives: mass, volume, cost, manufacturability, alignment/metrology burden, thermal behavior, focus implementation, coatings/throughput, supply risk, and optical performance.
- Unspecified quantities: no hard mass/volume limit and no customer pass/fail thresholds for MTF, RMS spot, WFE, distortion, throughput, obscuration, stray light, or pointing stability.
