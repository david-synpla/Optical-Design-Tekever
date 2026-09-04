# Track A Run 001 Architecture Screening

## Result

The two-conic-mirror telescope is the only screened family worth advancing. It preserves the required approximately 794.2 mm EFL and f/6.2 without chromatic focus error over 0.43-0.80 µm. Its preliminary RMS spot radius is on the order of a few micrometres, versus approximately 0.1-0.2 mm at the band edges for the scaled refractive seeds.

## Candidates

- **Scaled achromatic doublet:** simple spherical optics and low alignment complexity, but unacceptable secondary spectrum over the unusually broad visible band; also about 805 mm long.
- **Scaled air-spaced triplet:** more correction freedom but still severe band-edge color, thick 128 mm-class glass, and about 741 mm track. Rejected.
- **Scaled multi-element telephoto:** shorter at about 663 mm but uses several large high-index elements and retains severe band-edge color. Rejected on performance, mass, cost and thermal risk.
- **Two conic mirrors:** approximately 318 mm secondary-to-image distance, two aspheric mirrors, achromatic, and compact. Continue.

Two additional families were rejected before numerical optimization. A full-aperture Schmidt/Maksutov-type corrector would add a large precision optic, broadband refractive behavior and thermal risk without a supplied packaging need. An unobscured off-axis or three-mirror system could avoid central obscuration, but its freeform/aspheric fabrication, alignment and metrology burden is disproportionate at this stage. A minimal near-focus corrector remains a viable extension of the selected mirror baseline.

## Engineering assessment

The selected seed uses a -600 mm primary radius, -385.7 mm secondary radius, and 180 mm mirror separation. The conics and detector focus were varied in a bounded search; EFL and entrance pupil remained fixed. The secondary ray footprint implies roughly 42% linear obscuration before margin, but explicit obscuration, baffles and vignetting are not yet modelled. The strong secondary conic (-6.58) raises fabrication and metrology risk. A small near-focus spherical field corrector may trade modest refractive complexity for lower field aberration and a more practical focal surface.

## Assumptions and next action

Spot minimization and detector-Nyquist MTF are benchmark objectives, not customer limits. No package or distortion limit was invented. The 800 m requirement is presently represented only by the supplied 0.789 mm paraxial focus-shift estimate.

**Next action:** model obscuration and clear apertures, then compare the bare two-mirror form with a minimal spherical field-corrector group while monitoring MTF, distortion and manufacturability.
