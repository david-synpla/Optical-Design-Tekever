# Run 004 - A06 off-axis/decentered three-mirror screening

**Decision: PARK A06. Do not promote it to a final development run. Track A architecture exploration is complete. No additional architecture family may be opened without explicit user instruction.** A01 remains parked as the preserved baseline. Full Track A verification and blind-portfolio freeze are still outstanding.

The screen answered the combined question negatively within its budget: tilting the tertiary can remove A04's sampled detector/beam conflict, but none of five attempts provided a flat-field advantage over A01. This is a bounded search result, not proof that every off-axis three-mirror design is unsuitable.

| Case | Worst flat-detector RMS radius, um | Minimum detector-center ray clearance, mm | Disposition |
|---|---:|---:|---|
| A01, matched pupil and 3 x 3 field sampling | 8.63 | Not requalified in this run | Preserved comparison baseline |
| A06 attempt 1: tilted tertiary, conics and return geometry | 169.05 | 26.03 | Removes sampled conflict, loses useful image quality and image scale |
| A06 attempt 2: tertiary decenter and detector orientation | 30.62 | 0.10 | Rays intersect the actual active detector rectangle |
| A06 attempt 3: secondary tilt, corrected clearance merit | 53.67 | 6.07 | No sampled active-rectangle hits, but fails circular screening keepout |
| A06 attempt 4: denser pupil, stronger clearance merit | 59.36 | 7.61 | Still below screening keepout; no image-quality advantage |
| A06 attempt 5: release primary power and mirror spacing | 59.38 | 7.61 | Negligible progress; five-attempt cap reached |

Clearance is evaluated on actual finite non-imaging ray segments against a detector plane centered at the on-axis image centroid. The circular keepout radius is 7.96 mm: active-array half-diagonal plus a 1 mm benchmark margin, **not a customer requirement**. Failing this circle does not by itself prove intersection with the rectangular sensor. The explicit rectangular check finds active-detector hits in attempt 2; none in the sampled rays of attempts 1/3/4/5. Detector housing depth, mounts and continuous-pupil clearance are not certified.

## Optical evidence and limitations

- All attempts use three rotational conic mirrors, with tertiary tilt/decenter and, progressively, secondary tilt. The primary/secondary pair remains centrally obscured; A06 here is not claimed to be a fully unobscured telescope.
- Nine fields cover both signs, center, side midpoints and all four corners: horizontal +/-0.4048225 deg and vertical +/-0.296503 deg. The pupil diameter is 128.0972 mm. The final audit uses a 35-ray-diameter uniform grid and checks 19/35/51 sampling for attempts 1 and 4; the decision is unchanged.
- Geometrical spot checks at 0.43, 0.55, 0.65 and 0.80 um agree for this reflective model. This is not a diffraction/MTF or coating-bandpass qualification.
- Attempt 4's field-derived image scales are 793.15 and 795.92 mm, giving nominal scale/pupil ratios about 6.192 and 6.213. These finite-field centroid scales are not a full first-order pupil or IFOV verification for an asymmetric system. Attempt 1 gives 786.63/802.27 mm. No final requirement-compliant candidate is claimed.
- Sampled aperture throughput is approximately 78.9-79.5%, essentially the A01 obscured-pupil level, before coatings, spiders, baffles, physical primary-hole modelling and detector blockage. Do not treat these sequential unblocked-ray fractions as system transmission.
- No A06 prescription earns further MTF/wavefront, 800 m focus, thermal (-25 to +50 C), tolerancing or stray-light work in this screen. These requirements and engineering issues remain unverified for A06.

## Manufacture, alignment, metrology and packaging

Attempt 4 illuminates approximately 128.1/54.7/48.3 mm mirror diameters, within model clear diameters 130/58/90 mm. The tertiary's 90 mm aperture is an allowance, not a proposed finished blank diameter. Sampled conic slopes are about 0.107/0.057/0.158; vertex-sphere departures at the footprint edge are about 8.95/4.68/1.51 um. These do not indicate obviously impossible surface fabrication, but they are not best-fit-sphere departures or a manufacturing validation.

Relative to A01, A06 adds a powered conic mirror, a third reflection/coating, tertiary tilt/decenter alignment, a tilted image plane and non-coaxial metrology/assembly. Attempt 4 retains a strong secondary conic near -7.14 and needs about 382 mm sampled axial mirror extent versus A01's roughly 318 mm secondary-to-image distance. Neither number includes a housing. A roughly 12 mm primary-hole ray radius is required at its vertex plane, before edge, thickness and alignment margins; the hole is not included as an explicit solid mechanical aperture. No package or cost ceiling was invented.

Small decenter/tilt perturbation probes are saved, but the model moves/recenters the detector with its geometry. They are diagnostic probes, **not fixed-mechanics tolerances**. No robustness or thermal compliance is claimed. The engineering burden is not proven intrinsically unacceptable; it is unjustified because this screen establishes no compensating optical benefit.

## Resource and model record

Five substantial optimizer invocations and five materially distinct attempts were completed, using about 129 seconds total optimizer wall time. The candidate-stage cap, not the 30-minute or ten-search ceiling, stopped optimization. Attempts 1-3 reached their 110-evaluation caps; attempt 4 terminated on `ftol` after 117 evaluations and attempt 5 on `xtol` after 13. Numerical termination is not physical success. A formal three-attempt plateau is not claimed because clearance and optical quality traded against each other.

An autonomous audit corrected attempts 1/2's clearance calculation from the nominal detector origin to the actual on-axis image location and replaced rounded field normalization with exact normalization. The original optimization evidence is retained; `audit.json` and `metrics.json` supersede those early clearance values for the decision. No human optical correction or hidden-reference information was used. The user's scope/closure instruction is recorded as procedural governance.

The scripts, prescriptions for all attempts, environment versions, sampling, bounds, merit definitions and raw results are saved here. `optimization_model.py` preserves the initial attempt-1/2 numerical model; `track_a_run004_screen.py` is the corrected model for attempts 3-5 and auditing. Run `src/track_a_run004_audit.py` through the configured WSL Python in a working copy to regenerate analysis; it imports the unchanged A01 model in `src/track_a_run002_corrector_comparison.py`. Search outputs refuse to overwrite existing attempts. Source and run files are committed together.

**Next action:** prepare the remaining A01 verification/limitations and blind-portfolio freeze scope. Do not open A06 development or another architecture family automatically.
