# Track B State-of-the-Art Research Notes — TEKEVER EO Telescope

**Date:** 2026-09-05  
**Status:** Research performed while Track A Run 004 is still in progress.  
**Benchmark handling:** **Do not place this file in the TEKEVER Git repository and do not expose it to Codex/Track A until Track A is frozen.** The final Track B briefing should be derived from these notes only after the Track A freeze commit.

## 1. Scope and methodology

This review is intentionally independent of the prescriptions and numerical outcomes generated during Track A. It starts from the original TEKEVER EO requirements and asks:

> What established, commercially available, modified-COTS, and custom telescope architectures are plausible for a ~128 mm entrance pupil, ~794 mm effective focal length, f/6.2, 430–800 nm long-range imaging system using a flat Sony IMX545 detector?

The search covered:

- classical reflecting telescope families;
- corrected Cassegrain / Dall–Kirkham / Ritchey–Chrétien systems;
- Schmidt- and Maksutov-Cassegrains;
- off-axis and three-mirror systems;
- airborne and space EO precedents;
- refractive and photographic super-telephoto optics;
- COTS-only and maximum-COTS strategies;
- freeform/all-aluminium architectures;
- recent manufacturability and thermo-mechanical work.

The purpose is **not** to prescribe the Track B winner. It is to give Codex a well-supported architecture map and useful starting directions so that its limited compute is spent on credible branches rather than rediscovering the whole literature.

---

## 2. Requirement baseline

### 2.1 Explicit customer requirements

| Parameter | Requirement |
|---|---:|
| Spectral band | 0.43–0.80 µm |
| Horizontal FoV | 0.81° |
| IFOV | 3.45 µrad/pixel |
| f-number | f/6.2 |
| Detector | Sony IMX545 |
| Array | 4096 × 3000 |
| Pixel pitch | 2.74 µm |
| Minimum focusing distance | 800 m |
| Operating temperature | −25 to +50 °C |

First-order values derived from those requirements:

- effective focal length: **~794.20 mm**;
- active-array field: **~0.8096° × 0.5930°**;
- entrance pupil if f/6.2 is exact: **~128.10 mm**.

No supplied customer limit exists for MTF, spot size, WFE, distortion, obscuration, package length, mass, transmission, stray light, number of elements, surface types, or manufacturing tolerances. Those remain design/trade variables.

### 2.2 Important detector/diffraction implication

The IMX545 Nyquist frequency is:

**~182.48 lp/mm**

At f/6.2, the diffraction cut-off frequency of an ideal unobscured circular aperture is approximately:

| Wavelength | Diffraction cut-off | Ideal clear-aperture MTF at 182.48 lp/mm | Airy diameter (2.44 λN) |
|---|---:|---:|---:|
| 430 nm | 375 lp/mm | ~0.406 | ~6.51 µm |
| 550 nm | 293 lp/mm | ~0.262 | ~8.32 µm |
| 650 nm | 248 lp/mm | ~0.157 | ~9.83 µm |
| 800 nm | 202 lp/mm | ~0.035 | ~12.10 µm |

This is important for Track B. A design should **not** be penalised merely because its MTF is low at detector Nyquist near 800 nm; even an ideal f/6.2 aperture has very little contrast there. Evaluation should include:

- monochromatic and polychromatic diffraction-referenced MTF;
- several spatial frequencies (for example 50, 100, 150 and 182.5 lp/mm);
- ensquared energy / detector sampling;
- explicit source spectrum and detector QE weighting if a broadband MTF is used.

Without a specified spectral weighting, equal-weight broadband MTF should be labelled a benchmark assumption.

---

# 3. Main research finding

The most important Track B result is **not** an exotic telescope family. It is that the TEKEVER first-order geometry has unusually close matches to existing commercial optics.

Two COTS baselines deserve immediate consideration before expensive custom optimisation:

1. **Celestron C5 Schmidt–Cassegrain + Celestron 0.63× Reducer/Corrector**
2. **NIKKOR Z 800 mm f/6.3 VR S**

The custom design search should then concentrate on architecture families with strong precedents for flat-field, long-EFL EO imaging:

3. **Co-designed Corrected Dall–Kirkham (CDK)**
4. **Cassegrain + deliberately designed small image-side compensator/relay**
5. **Off-axis TMA / Korsch-type all-reflective system**

A modified-COTS version of the SCT is sufficiently well supported by recent literature to deserve its own architecture stream rather than being treated merely as a purchasing shortcut.

---

# 4. COTS-only architecture candidates

## 4.1 Celestron C5 + 0.63× Reducer/Corrector

### Why this is striking

Celestron specifies the C5 as:

- aperture: **127 mm**;
- native focal length: **1250 mm**;
- native focal ratio: **f/10** (nominal);
- Schmidt–Cassegrain;
- close focus: **~6.1 m**;
- mass: **~2.72 kg**;
- envelope: **~330 × 152 × 168 mm**.

Celestron's current reducer documentation explicitly gives:

- C5 native EFL: 1250 mm;
- C5 with 0.63× reducer: **~788 mm**;
- the reducer is intended for the classic C5–C14 SCT family.

Simple first-order comparison:

- 1250 × 0.63 = **787.5 mm**;
- 787.5 / 127 = **f/6.2008**;
- IFOV with 2.74 µm pixels ≈ **3.479 µrad/pixel**.

Thus:

- f-number is essentially an exact match;
- EFL is only ~0.84% shorter than the TEKEVER-derived 794.2 mm;
- IFOV is only ~0.85% larger than requested.

The exact reduction required for 794.20 mm is ~0.63536×. Reducer magnification changes with spacing, so a small change may be possible, but Celestron warns that departure from the intended back focus degrades edge performance. Therefore the correct question is not “can spacing force 794.2 mm?” but:

> Can a C5 + reducer operate near the required EFL while preserving adequate image quality across the IMX545 field?

### Field correction

Celestron describes the 0.63× unit as both a focal reducer and field corrector, but states that it only **reduces** the SCT field curvature; it does not fully eliminate it.

That makes this an empirical COTS candidate rather than something whose detector-level performance can safely be inferred from focal length alone.

### Advantages

- exceptionally close first-order match;
- fully commercial optical set;
- very compact folded geometry;
- low optical NRE;
- 127 mm aperture is almost exactly the derived entrance pupil;
- focus range is inherently far greater than needed for an 800 m target;
- reducer itself is inexpensive (current Celestron US list price ~US$200);
- generic SCT prescriptions are publicly available for simulation.

### Risks / questions

- exact C5 prescription is proprietary;
- high-frequency MTF across the IMX545 field is not specified publicly;
- remaining field curvature;
- vignetting and illumination with the chosen sensor/backfocus;
- central obstruction;
- moving-primary focus may create image shift / mechanical sensitivity;
- consumer OTA structure is not a UAV-qualified optomechanical structure;
- no public −25 to +50 °C guarantee was identified;
- spider is avoided because the secondary sits on the corrector plate, which is a practical benefit.

### Track B treatment

Treat this as **COTS baseline C1**.

Do not invent a C5 prescription. If the exact design data remain unavailable:

1. use a public generic SCT model only to understand architecture trends;
2. evaluate the real COTS system by measurement if procurement is possible;
3. distinguish generic-model results from actual C5 performance.

A useful public generic prescription is the COMSOL Schmidt–Cassegrain tutorial: 203.2 mm entrance pupil, f/10, an aspheric corrector and two spherical mirrors. It can be scaled or re-optimised as a research seed but is **not** a C5 prescription.

---

## 4.2 NIKKOR Z 800 mm f/6.3 VR S

Nikon specifies:

- 800 mm focal length;
- f/6.3 maximum aperture;
- full-frame image format;
- 22 elements in 14 groups;
- 3 ED elements plus specialised elements including Phase Fresnel;
- internal focusing;
- minimum focus distance 5 m;
- ~140 mm diameter × 385 mm length;
- ~2.385 kg mass;
- professional weather-resistant construction (not equivalent to the TEKEVER temperature requirement).

Comparison to target:

- EFL: +0.73% relative to 794.2 mm;
- f/#: f/6.3 rather than f/6.2;
- IFOV ≈ **3.425 µrad/pixel**, ~0.72% smaller than requested.

The IMX545 diagonal is far smaller than a full-frame image circle, so only the central portion of the commercial lens would be used.

### Advantages

- extremely close focal length and aperture ratio;
- complete imaging lens rather than astronomical visual optics;
- enormous corrected image circle relative to the required sensor;
- internal focus and 5 m minimum focusing distance make 800 m trivial;
- already lightweight for an 800 mm-class optic;
- professional mechanical implementation;
- very wide spectral imaging heritage in the visible.

### Risks / questions

- optical prescription is proprietary;
- detector-level MTF at 2.74 µm sampling is not available in sufficiently quantitative public form for this application;
- f/6.3 is not exactly f/6.2;
- electronic Nikon Z mount complicates independent industrial control of aperture/focus/VR;
- no public qualification for −25 to +50 °C UAV operation;
- many refractive surfaces imply throughput, ghost and thermal-focus considerations;
- Phase Fresnel optics deserve particular broadband/stray-light testing.

### Cost reference

As of this review, Nikon France lists the lens around **€6,499** and Nikon Ireland around **€6,199**, subject to change.

### Track B treatment

Treat this as **COTS baseline C2**.

It is probably the strongest pure “buy rather than design” imaging baseline.

---

## 4.3 Canon RF 800 mm f/5.6 L IS USM

Canon specifies:

- 800 mm focal length;
- f/5.6 maximum aperture;
- 26 elements in 18 groups;
- fluorite, UD and Super-UD elements;
- 2.6 m minimum focus;
- ~163 × 432 mm;
- ~3.14 kg;
- professional environmental sealing and magnesium structure;
- aperture control in 1/8-stop increments.

It can be stopped near f/6.2. It is therefore a legitimate high-end COTS performance benchmark, although its first-order match is less elegant than the Nikon because f/6.2 is not its native maximum aperture.

Canon Portugal currently lists it at approximately **€20,649**, which makes it useful mainly as a benchmark for the upper end of COTS optical performance/cost.

### Track B treatment

Treat as **COTS benchmark C3**, not the first procurement choice.

---

# 5. Modified-COTS (MCOTS) architecture

## 5.1 Re-house commercial SCT optics in a custom UAV structure

A very recent 2026 Applied Sciences study is directly relevant. It retained the commercial optical components of a Celestron C6 Schmidt–Cassegrain while replacing the consumer structural implementation with a custom additively manufactured structure and new deployment/focus mechanism.

The authors explicitly identify the problem:

- terrestrial COTS SCT optics can be attractive;
- the original structure lacks the stiffness and focus approach needed for a space payload.

Their modified system:

- kept the COTS corrector/primary/secondary optical set;
- redesigned the structure;
- underwent sine-sweep and shock-surrogate testing;
- retained measured collimation within uncertainty;
- used FEA alongside test;
- was presented as TRL-3 validation, not full flight qualification.

### Why this matters for TEKEVER

A similar strategy may be better than either extreme:

- do not fly/use the consumer C5 OTA unchanged;
- do not redesign every optical surface from zero.

Instead:

**C5 optical set + custom stiff/light barrel + custom detector interface + custom focus + custom baffling**

This has a realistic path to lower NRE while still addressing UAV structural/thermal requirements.

### Strong candidate: MCOTS-M1

Use the C5 optical set but replace:

- tube/front housing as necessary;
- moving-primary consumer focus if it proves unstable;
- detector interface;
- baffles;
- mechanical mounts.

Consider focusing by:

- detector translation; or
- controlled secondary motion,

rather than relying automatically on the consumer moving-primary implementation.

This branch should be evaluated independently from the stock C5+reducer COTS baseline.

---

# 6. Custom corrected two-mirror architectures

## 6.1 Corrected Dall–Kirkham (CDK)

This is one of the strongest custom candidates.

The mature CDK architecture uses:

- ellipsoidal primary;
- spherical secondary;
- lens corrector group near the focal plane.

PlaneWave's production CDKs demonstrate the architecture specifically as a way to obtain a flat imaging field with simpler mirror fabrication/alignment than a classical corrected RC.

The crucial design lesson is:

> The corrector is not merely bolted onto a finished Dall–Kirkham. Mirrors and corrector are optimised together.

PlaneWave's faster/wider DeltaRho derivative uses a three-element corrector group, while conventional CDKs commonly use two elements.

### Why it fits the TEKEVER problem

- folded compact package;
- broadband reflective front end;
- only small lenses near the image plane;
- spherical secondary is fabrication/metrology friendly;
- field curvature/astigmatism are attacked intentionally from the first optimisation;
- 430–800 nm is a modest enough band that a small 2–3 element corrector can be glass-selected intelligently;
- target field (~0.81° × 0.59°) is not unusually large.

### Manufacturing implications

Likely easier than:

- a two-hyperboloid RC of similar performance;
- a freeform TMA.

Likely harder than:

- a stock COTS SCT.

The primary ellipsoid still requires aspheric manufacture/metrology, but the secondary sphere is especially attractive.

### Track B priority

**Very high.**

Suggested research-informed seed:

- ~128 mm entrance pupil;
- ~794 mm total EFL;
- f/6.2;
- ellipsoidal primary;
- spherical convex secondary;
- 2-element corrector near image initially;
- permit a 3rd corrector element only if justified;
- optimise mirrors and lenses simultaneously;
- spherical lens surfaces first;
- allow realistic glass choices;
- explicitly include physical central hole, secondary size, apertures, sensor package and back focal clearance.

---

## 6.2 Co-designed Cassegrain + compact compensator / relay

Classic optical-design literature establishes that one-, two- and three-element correctors at the Cassegrain secondary focus can improve the usable field. Importantly, Wynne found that allowing the mirror aspheric constants to vary together with the corrector can outperform holding a pre-existing RC prescription fixed.

This is highly relevant to Track B methodology:

> Do not interpret poor performance of a small add-on corrector on a fixed mirror pair as evidence that a **co-designed** Cassegrain + corrector architecture is poor.

### Airborne EO precedent: LC11 LOROP camera

A particularly relevant Optics Express paper reports a compact long-range oblique photography camera with:

- common 280 mm-aperture f/6.6 reflective front end;
- EO channel at f/7.5;
- small EO compensator and relay groups;
- lens groups located near the primary mirror to reduce package volume/mass;
- telecentric image formation;
- lightweight primary and SiC main frame;
- field testing.

This is far closer in application character to a TEKEVER long-range airborne EO telescope than a typical observatory instrument.

### 2026 long-range surveillance precedent

A July 2026 Applied Optics design reports:

- Cassegrain front section;
- moving all-spherical refractive relay;
- 150 mm entrance pupil;
- 800 mm / f/5.33 and 1200 mm / f/8 modes;
- 264 mm total track;
- −40 to +60 °C optical modelling;
- ≤0.04% computed EFL drift across the temperature range.

The band is MWIR and its materials cannot be transferred directly to visible optics, but the **architecture and engineering method** are highly relevant: folded mirror telescope + small refractive relay + explicit passive thermal design.

### Track B priority

**Very high.**

Suggested seed:

- two-mirror Cassegrain-like front end;
- 2–4 spherical image-side elements;
- co-optimise mirror powers/conics and relay;
- put lenses where beam diameters are small;
- explore telecentric output if it improves detector integration/focus behaviour;
- treat exact element count as an optimisation outcome, not a requirement.

This may be the best custom compromise between optical performance, manufacturing cost and packaging.

---

## 6.3 Ritchey–Chrétien + field corrector

RC corrects third-order spherical aberration and coma with two aspheric mirrors, but it does not inherently provide a flat detector plane. A field corrector remains a standard route.

A classic Applied Optics design achieved a white-light, diffraction-limited 1.2° flat field using a four-lens corrector on an RC system.

### Advantages

- established high-image-quality architecture;
- excellent basis for corrected field;
- large literature base.

### Disadvantages relative to CDK

- both mirrors are non-spherical;
- convex hyperbolic secondary can be more difficult to make/test;
- alignment sensitivity is typically less forgiving.

### Track B priority

**Medium-high**, but CDK and co-designed Cassegrain+relay should normally be tested first.

---

# 7. Three-mirror / off-axis reflective architectures

## 7.1 Off-axis TMA

Off-axis/decentred three-mirror systems have long heritage in:

- remote sensing;
- commercial imaging;
- military imaging;
- space EO.

The 2023 review by Strojnik et al. maps multiple three-mirror families including:

- reflective triplet;
- TMA;
- Korsch triplet;
- inverse-telephoto-derived forms.

TMA architectures can correct the principal low-order aberrations while providing a flat imaging surface.

### Advantages

- inherently achromatic;
- potentially unobscured;
- high flat-field image quality;
- compact folded package possible;
- no large refractive glass;
- potentially favourable stray-light topology with suitable intermediate image/stop.

### Disadvantages

- tight alignment;
- off-axis/aspheric fabrication and metrology;
- more difficult mechanical datum definition;
- freeform implementations can become expensive quickly.

### ESA heritage

Proba-V uses compact TMA telescopes with aspheric aluminium mirrors produced by single-point diamond turning. ESA explicitly highlights the mass advantage of reflective aluminium optics across multiple spectral bands.

Sentinel-2 uses three mirrors, focal plane and telescope structure in silicon carbide to obtain very high optomechanical stability.

These are not direct prescriptions for the TEKEVER telescope, but they establish that three-mirror reflective EO systems are a mature remote-sensing architecture.

### Track B priority

**Very high as the high-performance custom branch.**

Start with rotationally describable conic/aspheric surfaces and decentered/off-axis geometry. Add freeform terms only if a clear performance/package advantage justifies them.

---

## 7.2 Korsch-type variants

Korsch triplets are especially relevant where the design needs:

- an accessible focal plane;
- convenient stop/pupil locations;
- folded packaging;
- stray-light control;
- separation between incoming and outgoing beams.

For Track B, Korsch should not necessarily be a separate exhaustive branch from TMA. Instead, Codex should be told that **off-axis TMA/Korsch topologies are a family**, and it may use Korsch-like folding/stop placement to solve physical focal-plane access or package conflicts.

---

## 7.3 All-aluminium / freeform TMA

A 2025 Applied Optics system demonstrates an unobscured all-aluminium freeform three-mirror telescope with:

- 400–900 nm band;
- 4° × 4° FoV;
- 40 mm entrance pupil;
- f/4.03;
- optical MTF >0.7 at 90 lp/mm;
- <1% distortion;
- ~2.9 kg total mass;
- ground and near-Earth-orbit images.

The authors emphasise:

- single-point diamond turning;
- computer-generated-hologram metrology;
- freeform compactness;
- all-aluminium optomechanical athermalisation.

A related thermo-optical study discusses all-aluminium freeform telescope behaviour and the benefit of matching mirror and structure CTE.

### Implication for TEKEVER

This is an important **technology direction**, especially for UAV thermal stability:

**aluminium mirrors + aluminium structure** can reduce differential CTE effects.

However, scaling a freeform design from 40 mm to ~128 mm aperture and maintaining visible-band surface quality is not trivial. The fabrication and metrology burden may dominate cost.

### Track B treatment

Do not start with full freeform.

Use hierarchy:

1. off-axis 3-mirror conics/aspheres;
2. evaluate performance/package;
3. introduce low-order freeform only if required;
4. compare the resulting benefit against manufacturing/metrology cost.

---

# 8. Low-surface-count research directions

## 8.1 Two-mirror aplanat with flat medial focal plane

Terebizh (Experimental Astronomy, 2022) provides families of Schwarzschild/Gregorian two-mirror aplanats in which the **medial** focal surface can be made flat.

Important nuance:

- this is not the same as a fully anastigmatic flat field;
- tangential and sagittal foci remain separated by astigmatism;
- the flat medial plane contains the circles of least confusion.

### Why it is interesting

The TEKEVER field is only ~0.81° × 0.59°, so a research-informed two-mirror family may conceivably deliver adequate detector performance with only two reflective surfaces.

### Why it is not a default winner

The remaining astigmatism may be too large for the small pixels. It should be screened cheaply before committing optimisation resources.

### Track B priority

**Medium as a low-complexity research seed.**

---

## 8.2 Two-mirror unobscured freeform telescope

A 2020 Applied Optics paper demonstrates a fabricated all-aluminium unobscured two-mirror freeform imaging telescope:

- 25 mm pupil;
- f/3.7;
- 400–700 nm;
- 20° × 15° FoV;
- diamond-turned mirrors;
- CGH-based interferometric null testing.

This proves that two freeform mirrors can replace more conventional surfaces in compact unobscured imaging.

### Relevance

Potentially attractive because it combines:

- only two powered reflective surfaces;
- no central obstruction;
- compactness;
- athermal all-aluminium concept.

### Limitation

The demonstrated system is much smaller and dramatically wider-field than the TEKEVER case. Scaling to 128 mm and 794 mm EFL is a new design problem, and Optiland/freeform support may constrain autonomous optimisation.

### Track B priority

**Speculative / second-line**, only after CDK, Cassegrain+relay and conic TMA.

---

# 9. Other catadioptric families

## 9.1 Schmidt–Cassegrain

The stock C5 already makes this architecture important.

A classical SCT uses:

- aspheric full-aperture Schmidt corrector;
- spherical primary;
- spherical secondary;
- compact folded geometry.

Generic public prescriptions are available, which makes a **custom SCT** or a re-optimised SCT-like system possible in Track B even without reverse-engineering Celestron.

### Custom SCT possibility

A tailored system could use:

- custom ~128 mm Schmidt corrector;
- custom mirror spacings/powers;
- custom ~0.635× image-side corrector/reducer;
- exact 794.2 mm EFL;
- sensor-specific field correction.

This is more NRE than buying C5 optics but could be a useful bridge between COTS and a fully custom CDK.

### Priority

**Medium**, because the COTS SCT should first establish whether customisation is needed.

---

## 9.2 Maksutov–Cassegrain

A typical 127 mm COTS Maksutov is around:

- 127 mm aperture;
- 1500 mm EFL;
- f/11.8;
- ~5 kg tube mass;
- compact tube.

To reach 794 mm would require roughly a 0.53× reducer. Celestron explicitly states its SCT 0.63 reducer is **not** compatible with Maksutov-Cassegrains.

Historical optical-design literature does show flat-fielded Maksutov-Cassegrain systems using nearly spherical surfaces and a small number of correcting lenses.

### Advantages

- compact;
- mostly spherical surfaces;
- mature architecture.

### Disadvantages for this requirement

- heavy full-aperture meniscus;
- thermal inertia and refractive thermal sensitivity;
- large focal-reduction requirement;
- COTS reducer compatibility is poor.

### Priority

**Low-medium**.

---

# 10. Refractive architecture

## 10.1 Premium 130 mm APO as feasibility proof

Astro-Physics' 130GTX demonstrates:

- 130 mm clear aperture;
- 819 mm focal length;
- f/6.3;
- very strong 400–706 nm colour correction;
- >97% peak visual transmission;
- 8.2 kg OTA mass;
- ~724 mm retracted length.

This proves that an all-refractive 130 mm f/6.3 broadband imaging telescope is optically plausible, but also demonstrates the likely mass/length penalty.

Its dedicated field flattener changes the effective focal length to ~873 mm, so the stock imaging configuration is not a direct TEKEVER match.

### Implication

A custom APO/telephoto design is physically possible, but the Nikon 800/6.3 COTS lens is a far more compelling refractive benchmark because it achieves nearly the exact first-order target at much lower mass.

### Priority

**Low for fully custom long refractor; high only as COTS supertelephoto benchmark.**

---

# 11. Newtonian maximum-COTS route

Sky-Watcher's BK130PDS provides:

- 130 mm aperture;
- 650 mm EFL;
- f/5;
- 3.66 kg tube;
- 615 mm tube length.

Sky-Watcher offers an f/5 coma corrector that leaves magnification unchanged.

To reach ~794 mm, the 650 mm system would still need ~1.22× focal extension in addition to coma correction.

### Advantages

- very cheap/simple parabolic primary;
- COTS mirrors/tube/corrector;
- no full-aperture refractive corrector.

### Disadvantages

- physically long;
- spider/secondary obstruction and diffraction;
- additional extender/relay required;
- more interfaces/backfocus complexity;
- package less naturally compact than Cassegrain.

### Priority

**Low-medium COTS/MCOTS experiment**, useful if cost dominates.

---

# 12. Curved detector option

Literature shows that curved focal surfaces can materially simplify two-mirror telescope correction.

However, the TEKEVER input explicitly specifies the Sony IMX545, which is a flat detector.

Therefore:

- curved detector concepts may be used as diagnostic evidence about field curvature;
- they should **not** be treated as compliant Track B candidates unless TEKEVER explicitly permits changing the detector requirement.

---

# 13. Industrial long-range surveillance benchmark

Commercial rugged long-range lenses are worth including even when they do not exactly match the optical requirement.

For example, Beck Optronic markets a ruggedised 400–1050 nm long-range zoom family with configurations including:

- 150–600 mm at f/5.6;
- 210–840 mm at f/7.8;
- 300–1200 mm at f/11.2;

with MIL-oriented construction and customisation.

This does not directly satisfy 794 mm/f6.2, but it establishes a relevant industrial vendor class and suggests a useful RFI route:

> ask whether a fixed/modified ~800 mm f/6.2 version can be supplied around the IMX545 field.

Commercial enquiries may uncover a lower-risk solution that is not visible from public catalogues.

---

# 14. Architecture comparison

Ratings are qualitative and deliberately provisional. “Image potential” means ability of the architecture family to support a flat, well-corrected detector field; it is **not** a measured performance claim for a specific candidate.

| Architecture | First-order fit | Flat-field image potential | Broadband 430–800 | Compactness | Manufacturing | Alignment | COTS share | Thermal/rugged potential | Relative cost |
|---|---|---|---|---|---|---|---|---|---|
| C5 + 0.63 reducer | Excellent | Unknown–moderate | Good | Excellent | COTS | Moderate | Excellent | Needs rework/test | Very low |
| Nikon 800/6.3 | Excellent | Likely high, must measure | Excellent | Good | COTS | Excellent integration optically | Excellent | Consumer/pro lens qualification needed | Medium |
| Canon 800/5.6 stopped | Very good | Likely high, must measure | Excellent | Moderate | COTS | Excellent integration optically | Excellent | Pro lens; qualification still needed | Very high COTS |
| MCOTS re-housed SCT | Excellent | Same optical question as SCT | Good | Excellent | Low custom optics | Moderate | Very high | High after custom structure | Low–medium |
| CDK | Excellent after design | High | High | Excellent | Moderate | Moderate | Low | High | Medium |
| Cassegrain + relay | Excellent after design | High | High | Excellent | Moderate | Moderate | Medium possible | High | Medium |
| RC + corrector | Excellent after design | High | High | Excellent | Medium–difficult | Difficult | Low | High | Medium–high |
| Off-axis TMA/Korsch | Excellent after design | Very high | Excellent | Excellent | Difficult | Difficult | Low | Very high | High |
| All-Al freeform TMA | Excellent after design | Very high | Excellent | Excellent | Very difficult/specialist | Difficult | Low | Excellent | High |
| Flat-medial two-mirror | Excellent after design | Unknown–moderate | Excellent | Excellent | Moderate | Moderate | Low | High | Medium |
| 2-mirror freeform | Excellent after design | Potentially very high | Excellent | Excellent | Specialist | Difficult | Low | Excellent | High |
| Maksutov + reducer | Possible | Moderate–high | Good | Excellent | Moderate | Moderate | Medium | Moderate | Medium |
| APO/custom refractor | Excellent after design | High | Challenging but feasible | Poor–moderate | High glass burden | Moderate | Medium | Moderate | High |
| Newtonian + corrector + extender | Possible | Moderate–high | High | Poor–moderate | Easy | Moderate | High | Moderate | Low |

---

# 15. Recommended Track B architecture set

The briefing should not force Codex to develop all of these. It should give Codex a priority map and let screening determine which branches earn compute.

## Tier 1 — must evaluate

### B-COTS1 — Celestron C5 + 0.63 reducer/corrector
Purpose: low-cost COTS floor.

### B-COTS2 — Nikon Z 800 mm f/6.3
Purpose: high-quality complete COTS imaging floor.

### B-MCOTS1 — retained SCT optics in custom rugged structure
Purpose: test whether most optical NRE can be avoided while solving the consumer-mechanics problem.

### B-CUST1 — co-designed CDK
Purpose: strong manufacturable flat-field custom candidate.

### B-CUST2 — co-designed Cassegrain + 2–4 element compensator/relay
Purpose: strongest airborne-EO-inspired compromise.

### B-CUST3 — off-axis TMA/Korsch family
Purpose: high-performance all-reflective option.

## Tier 2 — screen if Tier 1 leaves an unresolved trade

- RC + corrector;
- custom SCT / tailored reducer;
- flat-medial two-mirror aplanat;
- all-aluminium conic/freeform variant;
- Newtonian maximum-COTS;
- Maksutov + tailored reducer.

## Tier 3 — speculative / requirement-relaxation

- two-mirror freeform;
- large custom APO/refractor;
- curved detector.

---

# 16. Suggested Track B computational strategy

This section is intended for the eventual Codex briefing, but should not be exposed until Track A is frozen.

## Step 1 — Buy-versus-build gate

Before generating many custom prescriptions, evaluate whether the publicly specified COTS solutions already meet the geometry closely enough.

For COTS systems where the prescription is proprietary:

- do not fabricate a fake prescription;
- record what can be established from official data;
- identify what must be measured;
- if a generic model is used, label it clearly.

## Step 2 — Low-cost custom corrected-reflector competition

Develop in parallel:

1. CDK;
2. co-designed Cassegrain + compact relay/corrector.

These two should be compared before moving immediately to freeforms.

## Step 3 — High-performance all-reflective competition

Develop:

3. off-axis TMA/Korsch.

Start with conic/aspheric rotationally describable surfaces and realistic physical clearance. Introduce freeform only when it produces a meaningful Pareto improvement.

## Step 4 — MCOTS branch

Independently assess:

- C5 optics retained;
- custom mechanical structure;
- robust focus mechanism;
- detector mount;
- baffles;
- thermal expansion strategy.

The optical question and mechanical question should be separated.

## Step 5 — Final Track B portfolio

Preserve only genuinely non-dominated candidates, e.g.:

- lowest-NRE / COTS;
- best custom performance per manufacturing cost;
- highest-performance all-reflective;

but do **not** force those labels if the actual trade space does not produce them.

---

# 17. What Track B should evaluate consistently

For every developed candidate:

## Optical

- EFL / IFOV;
- f-number / entrance pupil;
- full 2-D active sensor field;
- 430–800 nm monochromatic performance;
- polychromatic performance with declared weighting;
- MTF at multiple spatial frequencies;
- comparison to diffraction MTF;
- ensquared energy;
- distortion;
- field curvature;
- chief-ray angle / telecentricity if relevant;
- illumination/vignetting;
- obscuration;
- throughput estimate;
- ghost/stray-light risk;
- 800 m refocus.

## Physical

- real surface apertures;
- central hole/spider/secondary package where applicable;
- detector package clearance;
- focus mechanism space;
- baffle space;
- total optical track;
- approximate outer envelope.

## Manufacturability

- spherical vs conic vs general aspheric/freeform;
- aspheric departure;
- slope;
- aperture;
- substrate;
- surface figure/roughness;
- metrology method;
- alignment datum concept;
- likely tolerance sensitivity.

## Thermal / mechanical

- −25 to +50 °C focus drift;
- differential CTE;
- refractive dn/dT where relevant;
- mirror-spacing sensitivity;
- detector-position sensitivity;
- candidate structure material;
- whether passive athermalisation is plausible.

## Cost

Use cost drivers rather than a fictional exact production price:

- number/size of custom optical surfaces;
- difficult aspheres/freeforms;
- custom glass;
- coatings;
- metrology;
- alignment;
- structural complexity;
- focus mechanism;
- qualification burden;
- COTS fraction.

---

# 18. Experimental validation strategy for the two strongest COTS baselines

Because proprietary prescriptions limit simulation fidelity, physical COTS testing may be more efficient than reverse engineering.

## C5 + reducer

If procured:

1. mount the actual IMX545 or a camera with the same pixel pitch/active area;
2. use a calibrated collimator/infinity target;
3. measure centre/mid/corner MTF or slanted-edge performance;
4. map focus curvature across field;
5. measure illumination/vignetting;
6. repeat with targets corresponding to 800 m;
7. test sensitivity to reducer spacing;
8. test image motion during focus;
9. thermal-soak only after basic optical feasibility is demonstrated.

## Nikon 800/6.3

1. establish an industrial Nikon-Z mount/electronics interface;
2. test at f/6.3 and, if useful, f/6.2-equivalent aperture settings;
3. measure centre/corner MTF over the small IMX545 field;
4. verify focus repeatability and image shift;
5. disable or characterise VR for platform use;
6. test spectral response across 430–800 nm;
7. investigate thermal behaviour.

---

# 19. Strong conclusions

1. **COTS deserves its own Track B design stream.** The C5 + 0.63 reducer is an unusually close first-order match: ~788 mm and f/6.20 from a 127 mm aperture.

2. **The Nikon 800/6.3 is an unusually strong complete COTS imaging baseline.** It is close to the required EFL/f-number and uses only a small central part of its full-frame field.

3. **Modified-COTS is a serious engineering architecture, not a compromise of convenience.** Recent 2026 work demonstrates retained SCT optics with a redesigned load-bearing/focus structure.

4. **Corrected Dall–Kirkham should be a top custom Track B candidate.** Its spherical secondary and co-optimised small lens group provide an attractive manufacture/performance balance.

5. **A Cassegrain front end with a deliberately designed compensator/relay has especially relevant airborne/long-range EO precedent.** This is different from adding a weak field flattener after the fact.

6. **Off-axis TMA/Korsch is the principal high-performance all-reflective direction.** It has strong EO/space heritage but carries higher alignment, fabrication and metrology burden.

7. **Freeform should be an escalation, not a starting assumption.** Modern all-aluminium freeform systems show impressive performance and athermalisation, but specialist fabrication/metrology are significant cost/risk drivers.

8. **Track B should use diffraction-aware image metrics.** At f/6.2, an ideal 800 nm aperture itself has only ~0.035 MTF at the IMX545 Nyquist frequency. Blindly maximising Nyquist MTF across the full band can push the optimisation toward an impossible or meaningless target.

9. **No architecture should be rejected solely for failing an invented image-quality or package requirement.** The source input contains no such customer limit.

10. **The best Track B workflow is a buy-versus-build competition**, not simply a search for the optically best custom prescription.

---

# 20. Principal sources

## COTS / commercial

- Celestron, **C5 Spotting Scope** — official specifications: 127 mm aperture, 1250 mm f/10, close focus and mechanical data.
- Celestron, **Understanding Focal Reducers** — current documentation explicitly lists C5 + 0.63× reducer at ~788 mm.
- Celestron, **Reducer/Corrector #94175** — official compatibility/specification page; current US list price ~US$199.95.
- Nikon, **NIKKOR Z 800mm f/6.3 VR S** — official technical specifications and current European pricing.
- Canon Portugal, **RF 800mm F5.6 L IS USM** — official technical data and current list price.
- Astro-Physics, **130 mm f/6.3 StarFire GTX** — official specifications.
- Sky-Watcher, **BK130PDS** and **f/5 Coma Corrector** — official specifications.
- Sky-Watcher, **127 mm Maksutov-Cassegrain** — official specifications.
- Beck Optronic Solutions, **150–1200 mm Visible/NIR Zoom Lens** — rugged long-range commercial benchmark.

## COTS adaptation

- H. H. Øvrebø et al., **Adaptation and Mechanical Validation of a COTS Telescope for LEO Hyperspectral Imaging Using an Additively Manufactured Structure**, Applied Sciences 16 (2026) 5038. DOI: 10.3390/app16105038.

## Corrected Cassegrain / CDK

- PlaneWave Instruments, **CDK Optical Design** — ellipsoidal primary + spherical secondary + lens group, co-optimised for flat field.
- C. G. Wynne, **Corrector Systems for Cassegrain Telescopes**, Applied Optics 7 (1968). DOI: 10.1364/AO.7.000253.
- **Design Procedure for Ritchey–Chrétien Corrector**, Applied Optics 8 (1969). DOI page: 10.1364/AO.8.000685.
- COMSOL Ray Optics Application Library, **Schmidt–Cassegrain Telescope** — public generic optical prescription and modelling example.

## Airborne / long-range EO

- K.-W. Park et al., **Novel compact dual-band LOROP camera with telecentricity**, Optics Express 20 (2012) 10921–10932. DOI: 10.1364/OE.20.010921.
- **Compact catadioptric dual-field-of-view mid-wave infrared system design for long-range surveillance**, Applied Optics 65 (2026) 7540. DOI available from Optica article AO.604906.

## Three-mirror / freeform

- M. Strojnik et al., **Off-Axis Three-Mirror Optical System Designs: From Cooke’s Triplet to Remote Sensing and Surveying Instruments**, Applied Sciences 13 (2023) 8866. DOI: 10.3390/app13158866.
- ESA, **Proba-V Technologies / Fitting the world in a box** — TMA, aspheric aluminium mirror and SPDT heritage.
- ESA, **Sentinel-2 Instrument** — silicon-carbide mirrors/focal plane/structure for optomechanical stability.
- J. Yu et al., **Unobscured off-axis three-mirror freeform all-aluminum imaging telescope**, Applied Optics 64 (2025) 1677–1692. DOI: 10.1364/AO.554593.
- **The Opto-Mechanical–Thermal Coupling Analysis and Verification of an All-Aluminum Freeform Imaging Telescope**, Symmetry 14 (2022) 2391.

## Two-mirror / alternative

- V. Yu. Terebizh, **Two-mirror aplanatic telescopes with a flat field**, Experimental Astronomy 53 (2022) 1075–1083. DOI: 10.1007/s10686-022-09833-0.
- Y. Xie et al., **Optical design and fabrication of an all-aluminum unobscured two-mirror freeform imaging telescope**, Applied Optics 59 (2020) 833–840. DOI: 10.1364/AO.379324.
- R. L. Waland, **Flat-Fielded Maksutov-Cassegrain Optical Systems**, JOSA 51 (1961) 359–366. DOI: 10.1364/JOSA.51.000359.

---

## 21. Freeze boundary

These notes may be refined while Run 004 proceeds, but **do not expose their contents to Track A**.

After Track A is frozen:

1. record the Track A freeze commit;
2. copy/finalise this research outside the Track A history;
3. produce `TRACK_B_RESEARCH_BRIEF.md`;
4. start Track B from original requirements + common workflow + that briefing;
5. do not initialise Track B from Track A prescriptions.
