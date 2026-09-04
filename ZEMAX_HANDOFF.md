# Zemax / OpticStudio Validation Handoff

## Purpose

Final frozen candidates should be transferable to Ansys Zemax OpticStudio for independent validation.

The Optiland design history remains authoritative for the AI benchmark. The Zemax handoff is a cross-tool representation of the same optical prescription, not a redesign.

## Preferred deliverable

For each final frozen candidate, create a handoff directory such as:

`handoff/track_A/A02/`

containing, when technically representable:

- `A02.zmx` — Zemax text lens file intended for opening/importing in OpticStudio;
- `prescription.csv` — neutral human-readable prescription;
- `mapping.md` — explanation of how Optiland surfaces/settings map to Zemax;
- `validation_checklist.md` — quantities to verify after opening in OpticStudio;
- the source export/build script used to generate the handoff.

The `.zmx` file should be generated only when the design can be mapped confidently to supported Zemax sequential constructs.

## Export principles

1. Do not change the optical design merely to make export easier.
2. Preserve, as applicable:
   - surface order;
   - radii and sign conventions;
   - thicknesses/spacings;
   - materials;
   - conic constants and supported aspheric terms;
   - stop/aperture definition;
   - clear apertures;
   - obscurations;
   - field definition;
   - wavelength definition and weights;
   - object conjugate;
   - image surface;
   - relevant solves/configurations if they can be represented reliably.
3. Record any setting that cannot be mapped one-to-one.
4. Treat the generated Zemax file as **unvalidated until it has been opened and checked in OpticStudio**.
5. Preserve the neutral `prescription.csv` even when a `.zmx` file is generated.

## Validation checklist

After opening the candidate in OpticStudio, verify at minimum:

- effective focal length;
- f-number / entrance pupil;
- object conjugate;
- field angles or image height;
- wavelength set;
- focus position;
- clear apertures and obscuration;
- conic/asphere definitions;
- spot performance;
- MTF at the same comparison frequencies;
- distortion;
- vignetting / ray clearance.

Small numerical differences between optical engines may occur. Large differences should be treated as an export/modeling problem until explained.

## Preferred creation method

For standard sequential spherical/conic/aspheric systems, generate a `.zmx` text lens file when the mapping is understood and reproducible.

If a candidate uses features that cannot be represented safely in a generated `.zmx`, provide instead:

- the neutral prescription and mapping;
- a reproducible Zemax build script using ZOS-API when a licensed OpticStudio environment is available.

If Codex later has access to a licensed local OpticStudio installation, prefer creating/opening the model through supported OpticStudio/ZOS-API mechanisms and then saving the native OpticStudio file from the application.

## Independence

Do not use Zemax during Track A or Track B to obtain hidden architecture guidance unless the benchmark is explicitly changed.

The first Zemax use should normally be cross-validation of a frozen candidate, not architectural assistance.
