# TEKEVER Optical Design Rules

## 1. Purpose

This project is a blind benchmark of AI-assisted optical design.

The objective is not merely to produce a numerically optimized optical prescription. The objective is to determine whether an AI can autonomously develop credible, manufacturable, robust and economically sensible telescope designs from the supplied requirements.

Optical performance, manufacturability, engineering risk and cost are all design objectives.

## 2. Requirement discipline

1. Treat only the supplied TEKEVER requirements as customer requirements.
2. Clearly distinguish between:
   - explicit customer requirements;
   - quantities mathematically derived from those requirements;
   - engineering assumptions;
   - design choices;
   - optimization results.
3. Never silently invent a missing customer requirement.
4. If an additional numerical target is useful for optimization, it may be introduced as a benchmark assumption, but it must be labelled as such.
5. If the supplied requirements are insufficient, inconsistent or ambiguous in a way that materially affects the design, identify this explicitly rather than hiding the problem.
6. Derived quantities should be traceable to the original requirements and their derivation should be reproducible.

## 3. Blind benchmark integrity

7. Do not inspect, search, infer from, or use anything in `reference/` during the blind phase.
8. Do not attempt to discover the known TEKEVER optical prescription from filenames, Git history, external sources, metadata or other indirect means.
9. Track A is the autonomous/uninformed benchmark.
10. During Track A, do not perform an external state-of-the-art search specifically to find existing architectures for this TEKEVER design problem.
11. General optical-engineering knowledge may be used normally.
12. A separate research-informed Track B will be performed later.

## 4. Architecture exploration

13. Do not simply optimize the first plausible optical layout.
14. Consider several materially different optical architecture families where physically reasonable.
15. Architecture exploration should occur early, but the design may return to alternative architectures later if optimization reveals a fundamental limitation.
16. For each serious candidate architecture, assess at least:
   - ability to satisfy the required optical geometry;
   - expected aberration-correction difficulty;
   - chromatic correction;
   - obscuration, if applicable;
   - package implications;
   - number and type of optical elements;
   - likely alignment sensitivity;
   - manufacturability;
   - expected cost drivers;
   - major technical risks.
17. Reject weak architectures explicitly and record the principal reason for rejection.
18. Do not force every possible architecture through a full optimization. Use engineering judgement to identify which candidates deserve detailed work.
19. Do not arbitrarily constrain the design to refractive, reflective or catadioptric solutions unless a requirement justifies doing so.
20. Develop promising architecture families sufficiently to make defensible comparisons.
21. Preserve multiple serious branches when they represent genuinely different engineering trade-offs.
22. Do not keep patching a candidate indefinitely if repeated evidence shows a structural limitation. Follow the plateau and resource-governance rules in `DESIGN_WORKFLOW.md`.

## 5. Optical design methodology

23. Progress approximately through:

   first-order design  
   → architecture candidates  
   → preliminary models  
   → candidate comparison  
   → nominal optimization  
   → performance verification  
   → engineering assessment  
   → blind-track portfolio freeze

24. Verify first-order quantities before detailed optimization.
25. Preserve explicit system requirements throughout optimization.
26. Do not compensate for an invalid first-order architecture by allowing the optimizer to produce physically unreasonable surfaces or dimensions.
27. Release optimization degrees of freedom progressively rather than making every possible parameter variable immediately without justification.
28. Quantities such as radii, spacings, powers, stop location, element bending and suitable glass choices should generally emerge from design and optimization rather than being assigned arbitrary values.
29. More complex design freedoms such as aspheres should be introduced when justified by a meaningful benefit rather than by default.
30. Avoid optimizing solely for one metric.
31. Evaluate, where relevant and supported by the model:
   - focal length / IFOV / FoV compliance;
   - f-number;
   - polychromatic image quality;
   - RMS spot size;
   - wavefront error;
   - MTF;
   - field curvature;
   - distortion;
   - lateral and longitudinal chromatic aberration;
   - vignetting;
   - clear apertures;
   - relative illumination;
   - total optical track;
   - focus behaviour;
   - sensitivity to practical construction.
32. Evaluate performance across suitable wavelengths and field positions, not only on-axis or at the central wavelength.
33. Detector sampling must be considered when interpreting image-quality metrics.
34. Do not claim that the system satisfies a customer MTF, distortion, package-size or other limit unless such a requirement was actually supplied.

## 6. Manufacturability

35. A numerically excellent but impractical design is not an acceptable final design.
36. Continually examine practical optical characteristics such as:
   - minimum centre thickness;
   - minimum edge thickness;
   - extreme radii;
   - steep surface slopes;
   - element diameter;
   - unusual aspect ratios;
   - very small air gaps;
   - mechanical interference;
   - difficult clear apertures;
   - strongly aspheric surfaces;
   - unusual materials;
   - alignment sensitivity;
   - centring sensitivity;
   - focus sensitivity;
   - assembly accessibility.
37. Prefer conventional manufacturing where it achieves adequate performance.
38. Spherical surfaces are preferred when their performance is sufficiently competitive.
39. Aspheres, unusual materials or difficult surfaces are permitted when they provide a sufficiently important benefit.
40. Do not reject a solution merely because it has more elements. Manufacturing cost and risk depend on the entire design, not element count alone.
41. Flag any feature likely to require specialist manufacturing, metrology, alignment or assembly.
42. Prefer robust designs over extremely sensitive designs when their nominal optical performance is comparable.

## 7. Materials and components

43. Use realistic optical materials.
44. Consider availability, transmission over the required spectral band, dispersion, thermal behaviour, manufacturability and likely cost.
45. Avoid exotic or difficult-to-source materials unless technically justified.
46. Do not assume that every catalogue glass or component is equally available or economical.
47. Clearly identify any component or material whose procurement may be a significant design risk.

## 8. Cost

48. Cost is an explicit design consideration, even though no customer cost ceiling has been supplied.
49. Do not invent a monetary budget.
50. Evaluate cost comparatively by identifying likely cost drivers, including:
   - number and size of optics;
   - surface complexity;
   - aspheres;
   - unusual glass;
   - coatings;
   - tight tolerances;
   - alignment difficulty;
   - custom mechanical complexity;
   - number of precision adjustments;
   - testing and metrology difficulty.
51. When two designs provide sufficiently similar useful performance, prefer the design expected to be cheaper, simpler and lower risk.
52. A more expensive architecture may be preserved or selected if its performance advantage is technically important and clearly justified.
53. Do not treat element count as a proxy for total cost.

## 9. Engineering judgement

54. Optimization merit-function value is not sufficient evidence that a design is good.
55. Inspect the actual optical prescription and physical layout after optimization.
56. Reject optimizer-generated solutions that exploit pathological geometries, unrealistic dimensions or numerical loopholes.
57. Use engineering judgement when deciding whether an improvement in nominal optical performance is worth increased complexity or cost.
58. The AI is allowed to conclude that no satisfactory design has yet been found.
59. Do not hide failures. A failed architecture or optimization may be useful evidence.
60. Do not force a single winner when the available requirements leave a genuine multi-objective trade-off.
61. Prefer a clear engineering decision over unlimited attempts at small numerical improvement.

## 10. Reproducibility and traceability

62. Every serious design candidate must be reproducible.
63. Preserve enough information to reconstruct each important candidate, including:
   - architecture;
   - prescription;
   - field sampling;
   - wavelength sampling;
   - aperture definition;
   - optimization variables;
   - optimization objectives;
   - relevant assumptions;
   - performance metrics;
   - software versions;
   - code used to generate the model.
64. Do not overwrite previous meaningful design runs.
65. Give each important run a unique identifier.
66. Keep stable candidate IDs as defined in `DESIGN_WORKFLOW.md`.
67. Record rejected and parked candidates concisely rather than deleting their history.
68. Keep Git commits at meaningful engineering milestones.

## 11. Reporting

69. For each major candidate, provide a concise engineering summary containing:
   - candidate ID and architecture;
   - why it was considered;
   - principal optical results;
   - major advantages;
   - major weaknesses;
   - manufacturability assessment;
   - cost assessment;
   - major risks;
   - current lifecycle status and reason.
70. Avoid producing large volumes of plots or data that do not help make a design decision.
71. Preserve detailed numerical results in files while keeping the design summary concise.

## 12. Human intervention

72. This benchmark also measures AI autonomy.
73. Record any case where a human has to correct:
   - an optical error;
   - an unjustified assumption;
   - an unrealistic prescription;
   - an optimization strategy;
   - a software/model implementation error;
   - an engineering judgement.
74. Human corrections should not be hidden from the benchmark record.
75. Procedural changes to resource budgets, workflow structure, or benchmark governance should be logged separately from optical-design corrections.

## 13. Final blind-track freeze

76. When the AI believes it has reached the best defensible set of results obtainable under the track, declare the proposed blind-track portfolio ready to freeze.
77. The portfolio may contain one candidate or several genuinely non-dominated candidates. Do not impose variety for its own sake.
78. If the evidence supports a preferred candidate, identify it as the recommendation while preserving meaningful alternatives.
79. Before accessing any known TEKEVER reference design, freeze for every preserved candidate:
   - optical prescription;
   - architecture;
   - assumptions;
   - performance results;
   - manufacturability assessment;
   - cost assessment;
   - identified weaknesses;
   - design genealogy and supporting runs.
80. Commit the frozen blind-track portfolio to Git.
81. Do not inspect `reference/` until explicitly authorized after the relevant blind-track freeze.

## 14. Overall design philosophy

The objective is not to maximize optical performance at any cost.

Seek strong engineering solutions considering simultaneously:

**requirements compliance + optical performance + manufacturability + robustness + complexity + packaging + cost.**

Explore broadly first, then spend computational effort on the most promising designs.

Preserve genuine engineering trade-offs rather than collapsing them prematurely into one scalar merit value.

Use finite computational budgets and explicit plateau logic so that engineering judgement, not endless optimization, determines when to move on.

Do not confuse numerical optimization with engineering design.
