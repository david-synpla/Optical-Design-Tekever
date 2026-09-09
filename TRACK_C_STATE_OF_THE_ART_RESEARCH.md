# TEKEVER Track C — State-of-the-Art Research Report
## Complete simultaneous co-boresighted EO + SWIR UAV imaging payload

**Research date:** 2026-09-09  
**Purpose:** independent architecture research to inform Track C before numerical screening and optimisation.  
**Contamination rule:** this report intentionally does **not** use the known TEKEVER/team Zemax prescription or any architecture inferred from it.

---

## 1. Requirements basis used for this research

The architecture research assumes the following corrected complete-system problem.

### EO channel
- wavelength: 0.43–0.80 µm
- horizontal FoV: 0.81°
- IFOV: 3.45 µrad/pixel
- f/#: 6.2
- detector: Sony IMX545
- active array: 4096 × 3000
- pixel pitch: 2.74 µm
- adopted active width: 11.22304 mm
- minimum focus distance: 800 m
- operating temperature: −25 to +50 °C

### SWIR channel
- wavelength: 0.80–1.80 µm
- horizontal FoV: 0.38°
- IFOV: 5.18 µrad/pixel
- f/#: 6.2
- detector: SenS 1280 L-STE Flex
- active array: 1280 × 1024
- pixel pitch: 10 µm
- active size: 12.8 × 10.24 mm
- minimum focus distance: 800 m
- operating temperature: −25 to +50 °C

### System-level clarifications
- EO and SWIR are both required in one payload.
- They operate simultaneously.
- They are co-boresighted / observe the same scene.
- Shared, partially shared, or separate optical trains are all permitted design options.
- Mass and package volume are first-class optimisation objectives because this is a UAV payload.
- Cost is also a first-class trade-study objective.
- No hard numerical mass or package-volume limit has yet been supplied.
- No customer pass/fail threshold has been supplied for MTF, RMS spot, WFE, distortion, throughput, obscuration, stray light, or pointing stability. These should be analysed but not invented as requirements.

---

## 2. First-order consequences that shape the architecture trade

Using pixel pitch divided by IFOV:

- EO EFL ≈ 794.20 mm.
- SWIR EFL ≈ 1930.50 mm.

At f/6.2:

- EO first-order entrance pupil ≈ 128.10 mm.
- SWIR first-order entrance pupil ≈ 311.37 mm.

The FoV values independently check:

- 4096 × 3.45 µrad ≈ 0.8097°.
- 1280 × 5.18 µrad ≈ 0.3799°.

The thin-lens first-order focus movement from infinity to 800 m is approximately:

- EO: 0.79 mm.
- SWIR: 4.67 mm.

These are derived quantities, not new requirements.

### 2.1 The key architectural asymmetry

The SWIR EFL and first-order pupil are about 2.43× the EO values. The corresponding pupil-area ratio is about 5.91×.

This makes the common-aperture decision unusual:

- if a shared front aperture must directly support the SWIR f/6.2 requirement, it is naturally a roughly 311 mm-class front end;
- the EO channel then requires only about a 128 mm effective pupil and can be stopped or remapped downstream;
- a common front telescope is therefore physically dominated by the SWIR requirement.

If two circular primary apertures were used separately, the combined primary area would be only about 16.9% larger than the SWIR primary area alone. Conversely, a single 311 mm common primary saves about 14.5% of the *combined primary area*. This is only an aperture-area comparison, not a payload-mass prediction; duplicated cells, secondaries, barrels, baffles, focusers and windows may dominate.

**Implication:** common aperture does not automatically win on mass for this requirement set. Its strongest system-level benefits may instead be common line-of-sight, shared structure/pointing functions, and reduction of duplicated large-scale optical functions.

---

## 3. State-of-the-art architecture trend: common reflective front end + modular back ends

The strongest recent trend in high-performance multi-band imaging is a reflective common front end, often afocal or pupil-relayed, followed by spectral separation and independently optimised channel modules.

### 3.1 2026 four-band shared off-axis afocal telescope

Jiang, Yu and Wang (Optics Express, 2026) present a four-channel VIS/SWIR/MWIR/LWIR telescope using a shared off-axis afocal front telescope and independent back-end imaging modules. Their motivation is specifically to avoid on-axis obstruction, aberrations introduced by beam splitting in a converging beam, and strong coupling among spectral channels. The individual modules can be aligned, assembled and tested independently. The infrared backends use real exit pupils and are athermalised.

This is important for TEKEVER because the EO and SWIR channels demand very different final EFLs and detector samplings. A common afocal front end can establish common line-of-sight while independent back ends set each channel's final EFL, pupil and focus behaviour.

### 3.2 2026 modular VIS/SWIR/MWIR common-aperture design

A 2026 Photonics paper, *Design of a Three-Channel Common-Aperture Optical System Based on Modular Layout*, uses an off-axis afocal beam-shrinking common path and independently designed relay paths. The common path is deliberately power-neutral/afocal, and the layout is intended to improve compactness and assembly compared with tightly coupled common-aperture systems.

### 3.3 Engineering inference for TEKEVER

A **common reflective afocal fore-telescope + channel-specific EO/SWIR cameras** should therefore be a serious Track C branch. It is the strongest high-end common-aperture architecture found in the recent literature.

It should not be selected automatically, because TEKEVER's UAV cost, mass and volume priorities may favour simpler alternatives.

---

## 4. Airborne evidence: folded off-axis TMA common apertures are current practice

A 2025 *Chinese Optics* paper specifically addresses an airborne multispectral common-aperture targeting pod. It uses a folded off-axis three-mirror telescope as the common optical path. The design has a 220 mm effective aperture, long focal lengths in NIR/SWIR/MWIR, shares aperture/fast-steering functions, and is packaged for a 500 mm-class airborne spherical EO pod.

This is directly relevant evidence that:
- folded off-axis TMA fore-optics are credible for airborne multispectral long-focus imaging;
- common-aperture designs can support different effective focal lengths in separate spectral channels;
- folding and shared steering can be key packaging tools.

However, it does **not** prove such a design is optimal for a smaller TEKEVER UAV. Off-axis TMA optics bring custom conics/freeforms, metrology and alignment burden.

---

## 5. Coaxial RC/Cassegrain common-aperture systems remain highly credible

Recent literature does not support the idea that a high-end off-axis TMA is always necessary.

Yan et al. (Applied Optics, 2024) demonstrate a visible/SWIR common-aperture design sharing Ritchey–Chrétien primary and secondary mirrors, then separating the bands with a dichroic splitter and using channel-specific optics. Their visible and SWIR channels have different focal lengths and entrance pupils.

Earlier UAV/aerial-imaging work by Mahmoud et al. (SPIE/IGARSS, 2016) also studied common-aperture VIS/SWIR systems for UAV/aerial imaging using shared RC or common refractive fore-optics with dichroic separation.

The 2023 CAMIS design/fabrication literature also describes the long-standing trade:
- coaxial reflective common-aperture systems are comparatively simple but suffer central obscuration;
- off-axis reflective systems avoid obstruction but are harder to correct, align and test.

### TEKEVER relevance

The required FoVs are narrow (0.81° EO and 0.38° SWIR). That weakens one of the main reasons to accept the complexity of a wide-field off-axis TMA.

A **coaxial two-mirror common fore-telescope + independent relays** deserves equal early screening with the off-axis afocal approach. It may provide a better cost/manufacturability/SWaP balance despite obscuration.

---

## 6. Two separate telescopes remain a serious contender

The requirement is simultaneous and co-boresighted, but co-boresight does not physically require one optical aperture.

Separate EO and SWIR telescopes can be mechanically integrated onto one optical bench and calibrated for relative boresight. UAV and airborne multi-sensor calibration literature shows that relative angular sensor alignment is a standard engineering problem; it requires calibration and stability control but is not a fundamental obstacle.

### Advantages for this requirement set
- each channel gets its own natural pupil and EFL;
- no dichroic insertion loss or edge-transition problem;
- independent coatings/materials;
- independent 800 m focus mechanisms;
- existing mature EO work from Track A/B may be reusable;
- SWIR design does not force a 311 mm front aperture on the EO path.

### Penalties
- duplicated primary/secondary/cell/baffle/window structure;
- relative boresight stability and calibration;
- possible parallax from spatially separated apertures;
- potentially larger external envelope.

Because the SWIR aperture dominates the area so strongly, the separate-telescope solution is more competitive in mass than a simple "two telescopes must be heavier" intuition suggests.

**Recommendation:** separate, mechanically integrated telescopes must remain one of the top three Track C branches.

---

## 7. Spectral splitting: technically feasible, but the 0.80 µm boundary needs deliberate allocation

Visible/SWIR dichroic separation is established technology. Published multilayer beam-splitter designs cover VIS and SWIR, and commercial coating technologies demonstrate steep-edge and broad-band filter capability.

However, the TEKEVER bands meet exactly at 0.80 µm:
- EO: through 0.80 µm
- SWIR: starts at 0.80 µm

A real dichroic has a finite transition region and angle/polarisation dependence. A shared-aperture architecture therefore needs an explicit spectral-allocation decision around the crossover. Possible strategies include:
- define a small transition interval around 800 nm;
- accept partial throughput in both channels near crossover;
- bias the crossover according to detector QE and mission weighting.

This is an **engineering allocation**, not grounds to change the source requirement automatically. It should be included in Track C coating/throughput optimisation.

For common front mirrors, broadband metallic coatings are feasible over essentially the required span. Protected aluminium has broad coverage from roughly 400–2000 nm with lower but fairly uniform reflectance; protected/enhanced silver offers higher visible/NIR reflectance above its blue edge but needs special attention near 430 nm and environmental durability. Coating selection should therefore be optimised jointly with the 430 nm EO edge, SWIR throughput, number of reflections and environmental durability.

---

## 8. Refractive optics are feasible downstream, but should not dominate the large shared aperture

A 400–1700 nm LFAST telescope design published in 2024 demonstrates that conventional crown/flint glasses and spherical refractive correctors can support a very broad VIS–SWIR band in a practical telescope. SCHOTT data also show that many optical glasses remain usable into the NIR/SWIR, though absorption and dispersion vary strongly by glass type and thickness.

This supports:
- small channel-specific correctors;
- relay lenses;
- field flatteners;
- pupil relays.

It does **not** imply that a large 311 mm full-aperture refractor is attractive for a UAV.

Large front optics should preferentially remain reflective unless optimisation shows a compelling alternative. Every Track C refractive glass must be checked against its actual 0.43–0.80 or 0.80–1.80 µm transmission and dn/dT, not inherited from the EO design by assumption.

---

## 9. Freeform and monolithic optics: strong SWaP potential, higher NRE/metrology risk

Bauer et al. (Optics Express, 2024) demonstrate that freeform surfaces can materially improve the compactness and achievable performance of multiconfiguration afocal telescopes. A four-mirror freeform system achieved a 5× configuration ratio with compensated exit pupil and diffraction-limited performance.

A 2025 Optics Communications paper on multi-facial freeform monoliths shows another direction: combining several precision surfaces in one monolithic element can reduce component count and alignment interfaces. The paper also highlights current manufacturing challenges, particularly surface positioning and edge-thickness control.

### Track C role

Freeform/folded common optics should be retained as a **SWaP stretch branch**, not the baseline:
- potentially excellent volume reduction;
- potentially fewer mounts/interfaces;
- but high fabrication/metrology/NRE/supplier risk.

Only promote it if simpler conventional branches cannot reach an attractive volume/mass trade.

---

## 10. Lightweight mirror technology can materially change the UAV trade

Using conventional astronomical COTS hardware as a mass proxy is misleading.

Commercial 300–305 mm-class astronomical RC/Newtonian OTAs are commonly around 20–28 kg, while a bare 300 mm commercial primary mirror can be about 6.3 kg. This shows that:
- the structure/cell/mechanics can dominate mass;
- a complete COTS astronomy OTA is unlikely to be an optimal airborne package;
- COTS optical donor elements may still be economically useful.

A 2024 *Composite Structures* paper specifically develops a lightweight 400 mm reflector for airborne/UAV use using TPMS internal structures, reporting about 70% mass reduction with controlled thermal deformation. SCHOTT documents deep lightweighting of ZERODUR substrates, and SiC research shows very high specific stiffness and thermal conductivity but higher fabrication complexity/cost.

### Track C implication

Mass optimisation must move into the architecture loop early. For every serious branch, evaluate:
- substrate material;
- mirror thickness/lightweighting;
- cell architecture;
- structure material;
- thermal gradients;
- first modes/vibration later in the maturity process.

A 311 mm aperture does **not** imply a conventional 20–30 kg telescope if custom lightweight aerospace optomechanics are allowed; nor does it imply low cost.

---

## 11. Thermal range and finite focus should influence architecture early

The −25 to +50 °C operating range is demanding but within the range addressed by recent airborne/multiband optical designs. Recent common-aperture systems explicitly use passive/active athermalisation over comparable ranges.

For TEKEVER, the 800 m finite-focus requirement is especially important because the two channels have very different first-order focus excursions:
- EO ≈ 0.79 mm
- SWIR ≈ 4.67 mm

A common optical front end therefore does not necessarily imply a common focusing degree of freedom. Independent channel relays/focus compensators are likely to be useful and should be included as mechanical/SWaP variables.

Do not transfer Track B thermal numbers directly to new Track C architectures.

---

## 12. Co-boresight and image registration should be treated as system metrics

For two separate telescopes, relative boresight is an explicit calibration/stability problem. Airborne/UAV literature shows this can be calibrated using common targets and navigation references.

For common-aperture architectures, shared fore-optics reduce some relative line-of-sight degrees of freedom, but downstream relay alignment can still produce channel registration errors.

Track C should therefore report, even without a customer threshold:
- nominal EO/SWIR LOS offset;
- sensitivity of relative boresight to alignment errors;
- thermal relative-LOS drift;
- calibration degrees of freedom;
- parallax for separate apertures as a function of target range.

This is particularly relevant because both channels must observe the same scene simultaneously.

---

## 13. Recommended Track C architecture portfolio

The research supports five serious architecture families.

### C01 — Separate integrated EO and SWIR telescopes
**Concept:** two optically separate telescopes on a common, stable co-boresighted payload structure.

**Strengths**
- natural independent EFL/pupil for each channel;
- simpler spectral optimisation;
- no splitter loss;
- potentially reuse mature B-series EO work;
- may be competitive in mass because SWIR already dominates aperture.

**Risks**
- duplicated optics/mechanics;
- boresight calibration and drift;
- envelope/parallax.

**Priority:** very high.

---

### C02 — Common coaxial reflective fore-telescope + independent EO/SWIR relays
**Concept:** shared Cassegrain/RC-like reflective front end, spectral split at a suitable pupil/collimated region where practical, separate EO and SWIR cameras/relays.

**Strengths**
- comparatively conventional mirror manufacture/alignment;
- common LOS;
- narrow FoVs suit coaxial systems;
- potentially lower NRE than off-axis TMA.

**Risks**
- central obscuration;
- 311 mm-class common front end;
- EO path under-uses the aperture;
- splitter/throughput complexity.

**Priority:** very high.

---

### C03 — Common off-axis afocal TMA + modular EO/SWIR relays
**Concept:** unobscured broadband common afocal fore-telescope with independent backend modules.

**Strengths**
- closest match to current high-end multispectral architecture trend;
- unobscured pupil;
- common LOS;
- modular channel optimisation;
- splitting in pupil/collimated space can reduce splitter-induced aberration.

**Risks**
- custom off-axis surfaces;
- metrology/alignment/NRE;
- potentially larger or more awkward envelope.

**Priority:** very high, but should not be presumed to win.

---

### C04 — Cost/COTS-maximised dual-channel system
**Concept:** explicitly minimise optical procurement/NRE using stock or near-stock mirror sets and small custom correctors/relays. May be separate or partially shared.

**Strengths**
- low recurring optics cost potential;
- shorter development/supply chain if suitable parts exist;
- existing B-series economic lessons can be reused.

**Risks**
- commercial astronomy OTAs are too heavy/large as-is;
- stock coatings/substrates may not be ideal;
- custom airborne rehousing and qualification can erode savings;
- exact EFL/f/# may require custom relays.

**Priority:** mandatory Pareto branch.

---

### C05 — Compact folded/freeform shared architecture
**Concept:** use freeform and/or monolithic multi-facial optics to aggressively reduce package volume and alignment interfaces.

**Strengths**
- highest potential volume compression;
- could reduce element/mount count.

**Risks**
- highest NRE;
- specialised metrology/fabrication;
- supplier concentration;
- more difficult qualification.

**Priority:** stretch branch; screen cheaply first.

---

## 14. Candidate family that should be screened but not automatically promoted

A conventional common imaging telescope with a dichroic inserted directly in a converging beam should receive a cheap screen.

Recent literature specifically identifies converging-beam splitting as a source of added aberration and tight channel coupling. If a simple implementation is sufficiently compact and performs well at these narrow fields, it may still be attractive. Do not reject it by literature argument alone.

---

## 15. Recommended Track C screening workflow

### Stage C0 — first-order feasibility and SWaP screen
No full optimisation initially.

For every branch record:

**Requirements**
- EO/SWIR EFL and f/# compliance
- pupil sizes
- FoVs / sensor fit
- 800 m focus concept
- simultaneous/co-boresighted feasibility

**Geometry/SWaP**
- largest optic
- optical path length
- approximate bounding box
- number of large mirrors/lenses
- approximate substrate volume/mass proxy
- number of separate housings/windows
- focus mechanism count
- expected gimbal/payload integration consequences

**Optical complexity**
- powered surface count
- custom surface count
- spherical/conic/aspheric/freeform count
- splitter/dichroic count
- expected obscuration
- reflection/transmission count
- channel-specific correction burden

**Manufacture/integration**
- alignment degrees of freedom
- metrology difficulty
- coating difficulty
- likely structural datum complexity
- relative boresight sensitivity

**Economics**
- COTS content
- likely NRE class
- recurring custom-optics burden
- qualification burden
- supplier concentration

Prune only when an architecture is dominated or clearly infeasible.

### Stage C1 — low-cost numerical architecture screening
Develop realistic but bounded optical seeds for surviving branches. Use the minimum degrees of freedom needed to prove feasibility.

### Stage C2 — optical development
Optimise the non-dominated architectures using the corrected complete requirements. Include mass/volume proxies in merit/trade decisions rather than image quality alone.

### Stage C3 — engineering maturity
For survivors:
- tolerance/alignment;
- relative boresight;
- thermal/athermalisation;
- finite-range focus;
- coatings/throughput;
- stray light;
- real packaging;
- lightweight mirror/structure analysis;
- cost/RFQ package.

### Stage C4 — Pareto portfolio
Do not force one universal winner if there is a meaningful trade among:
- performance;
- mass;
- volume;
- cost;
- manufacturability;
- robustness;
- schedule/supply risk.

---

## 16. Specific engineering questions Track C should answer

1. Does a 311 mm common fore-telescope save enough structure/pointing hardware to outweigh the duplicated 128 mm EO telescope in the separate architecture?
2. Can a coaxial common fore-telescope meet the narrow fields with sufficiently low obscuration and smaller package/NRE than an off-axis TMA?
3. Does the off-axis afocal architecture provide enough performance/throughput/boresight advantage to justify custom mirror/metrology cost?
4. Can B05/B06 or another existing EO design be reused in C01 without compromising the complete payload trade?
5. Can a stock/near-stock 300 mm-class mirror set support an economically attractive SWIR branch after custom lightweight rehousing?
6. What is the optimal dichroic crossover allocation around 800 nm?
7. Which broadband mirror coating gives the best 430–1800 nm system throughput/environmental trade?
8. Are independent EO/SWIR focus mechanisms the lowest-risk way to cover infinity to 800 m and thermal drift?
9. What mirror-substrate/lightweighting technology becomes justified when mass is assigned real value?
10. How much relative boresight stability/calibration burden does C01 add versus C02/C03?

---

## 17. Overall research conclusion

No state-of-the-art evidence justifies selecting common or separate optics before numerical/system screening.

The strongest **common-aperture** state-of-the-art direction is:

> **reflective afocal/common fore-optics + spectral split near a pupil/collimated region + independent channel relays**

The strongest **lower-complexity common-aperture** alternative is:

> **coaxial Cassegrain/RC-like shared front optics + independent channel relays**

The strongest **architecture-level competitor** is:

> **two separate but mechanically integrated/co-boresighted telescopes**

For this particular TEKEVER requirement set, C01 is unusually competitive because the SWIR pupil is about 2.43× the EO pupil and already dominates the collecting aperture and likely the payload structure.

The recommended initial competition is therefore:

> **C01 vs C02 vs C03**, with **C04 preserved as the mandatory economic/COTS Pareto lane** and **C05 as a compactness stretch lane**.

Track C should decide the winner only after first-order optical + SWaP + manufacturability screening.

---

# References and evidence base

**R1.** Jiang, L.; Yu, Q.; Wang, Z. “Design of a large-aperture telescope with four visible-infrared channels sharing a common front off-axis afocal optic system.” *Optics Express* 34(10), 19186–19201 (2026). DOI: 10.1364/OE.592751.  
https://doi.org/10.1364/OE.592751

**R2.** “Design of a Three-Channel Common-Aperture Optical System Based on Modular Layout.” *Photonics* 13(2), 161 (2026).  
https://www.mdpi.com/2304-6732/13/2/161

**R3.** Liu, Y.-Q. et al. “Design of an optical system for airborne multispectral common-aperture targeting pod.” *Chinese Optics* 18(4), 850–858 (2025). DOI: 10.37188/CO.2025-0011.  
https://doi.org/10.37188/CO.2025-0011

**R4.** Yan, A.; Chen, W.; Li, Q.; Guo, M.; Wang, H. “Optical design of a visible/short-wave infrared common-aperture optical system with a long focal length and a wide field-of-view.” *Applied Optics* 63(9), 2382–2391 (2024). DOI: 10.1364/AO.517643.  
https://doi.org/10.1364/AO.517643

**R5.** Cao, J. et al. “Optical design and fabrication of a common-aperture multispectral imaging system for integrated deep space navigation and detection.” *Optics and Lasers in Engineering* 167, 107619 (2023). DOI: 10.1016/j.optlaseng.2023.107619.  
https://doi.org/10.1016/j.optlaseng.2023.107619

**R6.** Mahmoud, A.; Xu, D.; Xu, L. “Optical design of common aperture and high resolution electro-optical/infrared system for aerial imaging applications.” SPIE 9880, 98801G (2016). DOI: 10.1117/12.2219869.  
https://doi.org/10.1117/12.2219869

**R7.** Mahmoud, A. et al. “Optical design of high resolution and shared aperture electro-optical/infrared sensor for UAV remote sensing applications.” IGARSS 2016, 2921–2924. DOI: 10.1109/IGARSS.2016.7729754.  
https://doi.org/10.1109/IGARSS.2016.7729754

**R8.** Bauer, A.; Zhang, C.; Liu, Y.; Rolland, J. P. “Multiconfiguration afocal freeform telescopes.” *Optics Express* 32(4), 6154–6167 (2024). DOI: 10.1364/OE.516961.  
https://doi.org/10.1364/OE.516961

**R9.** “Multi-facial freeform monolith optics for astronomical and space applications.” *Optics Communications* 576, 131345 (2025). DOI: 10.1016/j.optcom.2024.131345.  
https://doi.org/10.1016/j.optcom.2024.131345

**R10.** Zeng, C.; Wang, W.; Hai, K.; Ma, S. “Lightweight airborne TPMS-filled reflective mirror design for low thermal deformation.” *Composite Structures* 327, 117665 (2024). DOI: 10.1016/j.compstruct.2023.117665.  
https://doi.org/10.1016/j.compstruct.2023.117665

**R11.** Berkson et al. “Large Fiber Array Spectroscopic Telescope: Optical Design for a Scalable Unit Telescope.” *Nanomanufacturing and Metrology* (2024). DOI: 10.1007/s41871-024-00235-8.  
https://doi.org/10.1007/s41871-024-00235-8

**R12.** SCHOTT, TIE-35 “Transmittance of optical glass.” Technical information.  
https://www.schott.com/

**R13.** Edmund Optics, “Metallic Mirror Coatings.” Broadband protected aluminium/silver/gold coating guidance.  
https://www.edmundoptics.com/knowledge-center/application-notes/optics/metallic-mirror-coatings/

**R14.** SCHOTT, ZERODUR lightweight mirror substrate technical information.  
https://www.schott.com/en-gb/products/zerodur

**R15.** Wang, Z. et al. “The Optimization Design of a Lightweight 2 m SiC Mirror for Ground-Based Telescopes.” *Photonics* 11(6), 581 (2024). DOI: 10.3390/photonics11060581.  
https://doi.org/10.3390/photonics11060581

**R16.** “An Innovative Procedure for Calibration of Strapdown Electro-Optical Sensors Onboard Unmanned Air Vehicles.” *Sensors* / PMC. Airborne visible/IR boresight calibration evidence.  
https://pmc.ncbi.nlm.nih.gov/articles/PMC3270860/

**R17.** “Boresight calibration of a multi-sensor system for UAS photogrammetry.” IEEE ELEKTRO 2018. DOI: 10.1109/ELEKTRO.2018.8398362.  
https://doi.org/10.1109/ELEKTRO.2018.8398362

**R18.** Mahendra, R.; Chandra, R. “Multispectral Beam Splitter from Visible to MWIR.” preprint (2022), DOI: 10.21203/rs.3.rs-1342599/v1.  
https://doi.org/10.21203/rs.3.rs-1342599/v1

**R19.** SCHOTT optical-coating technical information; broadband AR/edge-filter manufacturing capability.  
https://www.schott.com/

**R20.** Teleskop-Service, 300 mm commercial primary mirror data: 300 mm, 35–39 mm thick, approximately 6.3 kg. Commercial evidence only, not airborne qualification.  
https://www.teleskop-express.de/

**R21.** Commercial 300 mm-class RC/astronomical OTA examples (Starworks / TS/GSO / Taurus) commonly in the roughly 20–28 kg class. Used only as a mass/packaging reality check; not an airborne design benchmark.

---

## Evidence-quality note

The architectural conclusions rely primarily on peer-reviewed 2023–2026 optical-design literature and direct airborne/UAV references. Vendor sources are used only for material/coating/COTS feasibility and mass/procurement anchors. Commercial astronomy masses and prices must not be interpreted as production-airborne payload estimates or supplier quotations.
