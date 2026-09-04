# TEKEVER Optical Design Rules

## 1. Purpose

This project is a blind benchmark of AI-assisted optical design.

The objective is not merely to produce a numerically optimized optical prescription. The objective is to determine whether an AI can autonomously develop a credible, manufacturable, robust and economically sensible telescope design from the supplied requirements.

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
20. Develop promising architecture families sufficiently to make a defensible comparison before choosing the final candidate.

## 5. Optical design methodology

21. Progress approximately through:

   first-order design  
   → architecture candidates  
   → preliminary models  
   → candidate comparison  
   → nominal optimization  
   → performance verification  
   → engineering assessment  
   → final blind candidate

22. Verify first-order quantities before detailed optimization.
23. Preserve explicit system requirements throughout optimization.
24. Do not compensate for an invalid first-order architecture by allowing the optimizer to produce physically unreasonable surfaces or dimensions.
25. Release optimization degrees of freedom progressively rather than making every possible parameter variable immediately without justification.
26. Quantities such as radii, spacings, powers, stop location, element bending and suitable glass choices should generally emerge from design and optimization rather than being assigned arbitrary values.
27. More complex design freedoms such as aspheres should be introduced when justified by a meaningful benefit rather than by default.
28. Avoid optimizing solely for one metric.
29. Evaluate, where relevant and supported by the model:
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
30. Evaluate performance across suitable wavelengths and field positions, not only on-axis or at the central wavelength.
31. Detector sampling must be considered when interpreting image-quality metrics.
32. Do not claim that the system satisfies a customer MTF, distortion, package-size or other limit unless such a requirement was actually supplied.

## 6. Manufacturability

33. A numerically excellent but impractical design is not an acceptable final design.
34. Continually examine practical optical characteristics such as:
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
35. Prefer conventional manufacturing where it achieves adequate performance.
36. Spherical surfaces are preferred when their performance is sufficiently competitive.
37. Aspheres, unusual materials or difficult surfaces are permitted when they provide a sufficiently important benefit.
38. Do not reject a solution merely because it has more elements. Manufacturing cost and risk depend on the entire design, not element count alone.
39. Flag any feature likely to require specialist manufacturing, metrology, alignment or assembly.
40. Prefer robust designs over extremely sensitive designs when their nominal optical performance is comparable.

## 7. Materials and components

41. Use realistic optical materials.
42. Consider availability, transmission over the required spectral band, dispersion, thermal behaviour, manufacturability and likely cost.
43. Avoid exotic or difficult-to-source materials unless technically justified.
44. Do not assume that every catalogue glass or component is equally available or economical.
45. Clearly identify any component or material whose procurement may be a significant design risk.

## 8. Cost

46. Cost is an explicit design consideration, even though no customer cost ceiling has been supplied.
47. Do not invent a monetary budget.
48. Evaluate cost comparatively by identifying likely cost drivers, including:
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
49. When two designs provide sufficiently similar useful performance, prefer the design expected to be cheaper, simpler and lower risk.
50. A more expensive architecture may be selected if its performance advantage is technically important and clearly justified.
51. Do not treat element count as a proxy for total cost.

## 9. Engineering judgement

52. Optimization merit-function value is not sufficient evidence that a design is good.
53. Inspect the actual optical prescription and physical layout after optimization.
54. Reject optimizer-generated solutions that exploit pathological geometries, unrealistic dimensions or numerical loopholes.
55. Use engineering judgement when deciding whether an improvement in nominal optical performance is worth increased complexity or cost.
56. The AI is allowed to conclude that no satisfactory design has yet been found.
57. Do not hide failures. A failed architecture or optimization may be useful evidence.

## 10. Reproducibility and traceability

58. Every serious design candidate must be reproducible.
59. Preserve enough information to reconstruct each important candidate, including:
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
60. Do not overwrite previous meaningful design runs.
61. Give each important run a unique identifier.
62. Record rejected candidates and failed approaches concisely rather than deleting their history.
63. Keep Git commits at meaningful engineering milestones.

## 11. Reporting

64. For each major candidate, provide a concise engineering summary containing:
   - architecture;
   - why it was considered;
   - principal optical results;
   - major advantages;
   - major weaknesses;
   - manufacturability assessment;
   - cost assessment;
   - major risks;
   - reason to continue or reject it.
65. Avoid producing large volumes of plots or data that do not help make a design decision.
66. Preserve detailed numerical results in files while keeping the design summary concise.

## 12. Human intervention

67. This benchmark also measures AI autonomy.
68. Record any case where a human has to correct:
   - an optical error;
   - an unjustified assumption;
   - an unrealistic prescription;
   - an optimization strategy;
   - a software/model implementation error;
   - an engineering judgement.
69. Human corrections should not be hidden from the benchmark record.

## 13. Final blind-design freeze

70. When the AI believes it has reached the best defensible design obtainable under this autonomous track, declare it the proposed blind candidate.
71. Before accessing any known TEKEVER reference design, freeze:
   - optical prescription;
   - architecture;
   - assumptions;
   - performance results;
   - manufacturability assessment;
   - cost assessment;
   - identified weaknesses;
   - design history summary.
72. Commit the frozen blind candidate to Git.
73. Do not inspect `reference/` until explicitly authorized after this freeze.

## 14. Overall design philosophy

The objective is not to maximize optical performance at any cost.

Seek the best engineering solution considering simultaneously:

**requirements compliance + optical performance + manufacturability + robustness + complexity + cost.**

Explore broadly first, then spend computational effort on the most promising designs.

Do not confuse numerical optimization with engineering design.
