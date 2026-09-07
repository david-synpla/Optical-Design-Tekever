# Run 011 — cost-conscious lane selection gate

Decision: reopen **B09** for an independently bounded hybrid Newtonian/corrector development run. Keep **B01/B03** as the second, empirical stock-SCT route; do not invent their proprietary prescription. B02 remains a complete-COTS purchase/control comparator, not the first low-cost development target. No other parked architecture is reopened.

The user explicitly added a permanent performance-versus-cost/risk portfolio objective. This changes roadmap/governance, not the TEKEVER optical requirements. Run 010 numerical work was complete before quota stopped its commit; hashes passed on recovery and milestone 110ee1c was committed and pushed without repeating any solves. Its B05/B06 findings and the planned thermal/material comparison stand.

## Current procurement evidence — checked 2026-09-07

Prices are displayed retail offers in their original currencies, not quotations, landed costs, production prices or availability guarantees. No currency conversion or purchasing action was performed.

| Route / product | Evidence | Source |
|---|---|---|
| B09: Sky-Watcher 130PDS OTA, part 10219 | GBP 229; awaiting stock, seller indicates usually 2–4 working days. 130 mm paraboloidal primary, 650 mm focal length, 47 mm secondary minor axis, 0.5 mm spider vanes; OTA mass 4 kg. | [First Light Optics product offer](https://www.firstlightoptics.com/reflectors/skywatcher-explorer-130p-ds-ota.html) |
| B09: replacement 130/650 primary, A5506 | EUR 70.65 displayed, last item; variant selector differs by EUR 0.05. Part-only supply is therefore plausible but price/quantity and matched secondary availability require confirmation. | [Binorum offer](https://www.binorum.eu/primary_mirror_sky_watcher_130_650_sw-5506/) |
| B01/B03: Celestron C5 item 52291 | USD 679.95; low stock. Nominal 127 mm aperture, 1250 mm focal length; 2.722 kg and 330 x 152 x 168 mm catalogue scope dimensions. | [Celestron product](https://www.celestron.com/products/c5-spotting-scope) |
| B01: Celestron reducer/corrector 94175 | USD 199.95, in stock. C5-compatible 0.63x nominal reduction. C5 plus reducer hardware subtotal USD 879.90 before interface/qualification. | [Celestron reducer](https://www.celestron.com/products/reducer-corrector), [manufacturer compatibility explanation](https://www.celestron.com/blogs/knowledgebase/understanding-focal-reducers) |
| B02: Nikon Z 800/6.3 VR S JMA502DA | GBP 4,999 displayed promotional retail, in stock, indicated 3–5 day delivery. An optical/control integration comparator rather than the cheapest hardware route. | [Nikon UK offer](https://www.nikon.co.uk/en_GB/product/lenses/mirrorless/nikkor-z-800mm-f6.3-vr-s-JMA502DA) |

Product claims are not TEKEVER qualification evidence. In particular, catalog coatings do not establish transmission across 430–800 nm; “parabolic” supplies a credible ideal mathematical nominal, not a measured figure map or tolerance guarantee. We do not adopt the seller's generic claim that a paraboloid produces sharp stars across an entire field: off-axis coma must be traced.

## Engineering gate

All rankings below are engineering judgement. Low/medium/high compare these routes' expected work, not money or time quotas.

| Dimension | B09 hybrid stock paraboloid + flat + small corrector/extender | B01 stock C5/reducer, then B03 limited mechanical adaptation | B02 complete photographic lens |
|---|---|---|---|
| Hardware / custom optics | Low stock-mirror procurement anchor; initially two small custom spherical lenses (four powered surfaces). Escalate only if clear benefit. | Low/moderate complete stock optical set; zero custom powered surfaces initially. New optical correction would need supplier model or empirical system identification. | Higher stock purchase anchor; zero custom powered surfaces. |
| NRE / scalability | Moderate corrector/cell NRE; no custom powered mirror or convex-asphere null. Mirror lot qualification and small-lens RFQ can support repeatability. | Low for initial bench characterization; moderate/high if rehousing destroys factory datums. Matched sets, moving-primary support and supply continuity need agreement. | Low optical NRE, potentially significant proprietary control/focus/VR and detector-interface NRE. |
| Exact optical geometry | Modelable nominal 650 mm paraboloid; 1.2218506x effective extension and 128.097 mm entrance stop can be designed. Needs demonstrated full-band correction. | At 127 mm pupil, tuning EFL to 794.203 gives f/6.2536; stock 0.63x gives 787.5 mm. Rehousing cannot create the missing aperture. No invented tolerance waiver. | 800 mm/f6.3 remains a nominal mismatch; cannot command its maximum aperture to f6.2. |
| Manufacture / alignment | Familiar primary/flat tests; lens centration, collimation, spider, side-exit relay alignment. Less specialized than off-axis TMA but not alignment-free. | Preserve factory matched corrector/mirrors; quantify focus backlash/image shift first. Fix primary and translate detector only if real conjugate tests support it. | Preserve sealed optical assembly; electronic focus repeatability and mount datum transfer need test. |
| Mechanics / volume / mass | Longer beam path and lateral detector; stock OTA mass is not UAV assembly mass. Retain optics in purpose-designed structure only after costing adaptation. | Compact folded path; custom cell, focus interface and support can remove accessories, but mass savings and thermal stability are unproven. | Complete lens body carries unavoidable housing/actuator integration; no inferred rejection from mass. |
| Thermal / interface | Mirror/structure CTE, long lever arms, lens dn/dT, exposed spider and window. Detector axial clearance after extender must be checked. | Schmidt plate/structure gradients, mirror focus motion, reducer spacing, detector window, condensation and cold mechanism behavior. | Multiple glasses/PF element, focus/VR electronics and sensor-stack dependence; supplied operating range unverified. |
| Supply / schedule risk | Current retail routes exist; stock counts do not prove volume continuity. Model can proceed now, measured part acceptance still needed. | Can define a bench prototype now. Optical development is data-limited without supplier prescription or actual hardware. | Buy-and-test route possible; control protocol and detector integration could dominate schedule. |
| Evidence / missing data | Credible ideal nominal from disclosed paraboloid and flat. Missing measured radius, figure/roughness, coating curves, substrate, lot scatter and true mechanical drawing. | Full prescription unavailable; no credible high-frequency/full-band performance simulation. Need empirical tests below. | Published specs are insufficient for requested spectral/high-frequency metrics; need empirical tests. |

B09 is selected because it combines a substantially cheaper stock-optics procurement anchor with a modelable nominal and a limited number of small custom surfaces. This is a testable economic hypothesis, not a demonstrated cheapest product. If its custom corrector, precision supports or qualification erase the advantage, retain that finding rather than forcing a “cheap” winner.

B01/B03 remain the second route because retaining a factory optical assembly could reduce optical NRE substantially. First measure the assembled C5/reducer before rehousing it. Its exact geometric mismatch must be explicitly accepted by the customer or addressed with a different, adequately sized stock optical set; the latter would require its own lineage/geometry investigation. No silent relaxation or fictional C5 model is permitted.

## Empirical and RFQ gates

For B01/B03 and B02, the minimum useful bench evidence is EFL/pupil measurement; collimated point/slanted-edge tests at center, signed edges and corners at 430/500/550/650/725/800 nm and a common detector focus; 50/100/150/Nyquist MTF and 2-pixel EE; illumination; 800 m equivalent conjugate/refocus; focus repeatability/image shift; then temperature and vibration tests. Use the actual detector/window or measure its effect. No equipment was bought or tested and no vendor messages were sent.

Prepare later RFQs for (1) measured 130/650 primary and matching flat, including quantities/lot continuity, figure, substrate and coatings; (2) the developed small spherical corrector and coatings; (3) mirror cells/spider/relay barrel/focus mechanism; (4) stock-SCT optical-set supply, drawing/prescription access and permitted rehousing; and (5) B05 custom mirrors/lenses and B06 off-axis mirrors with test fixtures. Quote common quantities and acceptance tests before translating relative classes into monetary comparisons.

## Permanent roadmap / freeze gate

Performance lane: B05-1, B05-2 and B06 remain active; Run 010 tolerance/alignment study is closed and matched -25 to +50 C thermal/material work is next. No nominal shape search is authorized merely by this lane addition.

Cost-conscious lane: B09 becomes ACTIVE for Run 012 hybrid development; B01/B03 remain an empirical fallback. Compare the developed B09 against Run 010 metrics and engineering limits, accepting that lower optical performance can be a useful trade.

Track B may not be frozen solely on B05/B06 maturity. Before final selection it must either retain a credibly evaluated lower-cost option or document why the low-cost routes fail to provide an acceptable economic/performance trade. “Low-cost”, “balanced custom” and “higher-performance” are comparison categories, not forced winners. All three need qualification and real RFQs. Run 011 ends here: no optical optimizer calls or new prescriptions.
