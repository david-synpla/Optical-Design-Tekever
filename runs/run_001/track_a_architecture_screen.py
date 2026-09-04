"""Track A first-order architecture screening for the TEKEVER EO telescope.

This script intentionally uses no data from reference/.  It reproduces the
first blind architecture decision and writes the required run_001 artifacts.
"""

from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from optiland import optic
from optiland.analysis import RmsWavefrontErrorVsField, SpotDiagram
from optiland.mtf import GeometricMTF
from optiland.samples import (
    Telephoto,
    TelescopeDoublet,
    TripletTelescopeObjective,
)


TARGET_EFL_MM = 794.2029
TARGET_EPD_MM = 128.0972
PIXEL_PITCH_MM = 0.00274
NYQUIST_CY_PER_MM = 1.0 / (2.0 * PIXEL_PITCH_MM)
WAVELENGTHS_UM = (0.43, 0.55, 0.65, 0.80)
FIELDS_DEG = (0.0, 0.2864, 0.4048, 0.5019)


def configure_sampling(lens: optic.Optic) -> optic.Optic:
    while lens.fields.num_fields:
        lens.fields.remove(0)
    while lens.wavelengths.num_wavelengths:
        lens.wavelengths.remove(0)
    lens.fields.set_type("angle")
    for field in FIELDS_DEG:
        lens.fields.add(y=field)
    for wavelength in WAVELENGTHS_UM:
        lens.wavelengths.add(value=wavelength, is_primary=wavelength == 0.55)
    lens.set_aperture(aperture_type="EPD", value=TARGET_EPD_MM)
    return lens


def scaled_sample(sample_class, image_distance_mm: float) -> optic.Optic:
    lens = sample_class()
    lens.updater.scale_system(TARGET_EFL_MM / lens.paraxial.f2())
    configure_sampling(lens)
    lens.updater.set_thickness(len(lens.surfaces) - 2, image_distance_mm)
    return lens


def build_doublet() -> optic.Optic:
    return scaled_sample(TelescopeDoublet, 803.5196660272221)


def build_triplet() -> optic.Optic:
    return scaled_sample(TripletTelescopeObjective, 616.6929745128558)


def build_telephoto() -> optic.Optic:
    return scaled_sample(Telephoto, 413.8096122823016)


def build_two_mirror() -> optic.Optic:
    # Fixed result of the bounded Track A conic/focus search.  Geometry was
    # constrained to a 600 mm primary radius and 180 mm mirror separation.
    lens = optic.Optic(name="Track A two-conic-mirror seed")
    lens.surfaces.add(index=0, radius=math.inf, thickness=math.inf)
    lens.surfaces.add(index=1, thickness=180.0, comment="entrance reference")
    lens.surfaces.add(
        index=2,
        radius=-600.0,
        thickness=-180.0,
        material="mirror",
        is_stop=True,
        conic=-1.16201060,
        comment="primary mirror",
    )
    lens.surfaces.add(
        index=3,
        radius=-385.7,
        thickness=317.61596583,
        material="mirror",
        conic=-6.58144493,
        comment="secondary mirror",
    )
    lens.surfaces.add(index=4, comment="flat detector")
    return configure_sampling(lens)


def spot_metrics(lens: optic.Optic) -> tuple[np.ndarray, SpotDiagram]:
    diagram = SpotDiagram(lens, num_rings=6)
    return np.asarray(diagram.rms_spot_radius(), dtype=float) * 1000.0, diagram


def candidate_metrics(name: str, lens: optic.Optic) -> dict:
    rms_um, _ = spot_metrics(lens)
    return {
        "name": name,
        "effective_focal_length_mm": float(lens.paraxial.f2()),
        "f_number": float(lens.paraxial.FNO()),
        "entrance_pupil_diameter_mm": float(lens.paraxial.EPD()),
        "total_track_mm": float(lens.total_track),
        "fields_deg": list(FIELDS_DEG),
        "wavelengths_um": list(WAVELENGTHS_UM),
        "rms_spot_radius_um_by_field_and_wavelength": rms_um.tolist(),
        "worst_rms_spot_radius_um": float(np.nanmax(rms_um)),
        "distortion_percent": None,
        "relative_illumination": None,
    }


def mirror_footprints(lens: optic.Optic) -> dict:
    lens.trace(0, 1, 0.55, num_rays=100, distribution="uniform")
    radii = []
    for surface_number in (2, 3, 4):
        surface = lens.surfaces[surface_number]
        radius = np.nanmax(np.hypot(np.asarray(surface.x), np.asarray(surface.y)))
        radii.append(float(radius))
    return {
        "primary_ray_footprint_radius_mm": radii[0],
        "secondary_ray_footprint_radius_mm": radii[1],
        "image_ray_footprint_radius_mm": radii[2],
        "estimated_linear_obscuration_ratio": radii[1] / (TARGET_EPD_MM / 2.0),
        "note": "Footprint estimate only; explicit obscuration/vignetting was not modelled.",
    }


def save_prescription(run_dir: Path, lens: optic.Optic) -> None:
    rows = [
        (0, "object", math.inf, math.inf, 0.0, "air", "object at infinity"),
        (1, "entrance reference", math.inf, 180.0, 0.0, "air", "layout reference"),
        (2, "primary mirror", -600.0, -180.0, -1.16201060, "mirror", "aperture stop"),
        (3, "secondary mirror", -385.7, 317.61596583, -6.58144493, "mirror", "convex secondary"),
        (4, "flat detector", math.inf, 0.0, 0.0, "air", "image surface"),
    ]
    with (run_dir / "prescription.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("surface", "comment", "radius_mm", "thickness_mm", "conic", "material_after", "role"))
        writer.writerows(rows)


def save_plots(run_dir: Path, lens: optic.Optic, spot: SpotDiagram) -> dict:
    fig, _ = lens.draw(
        fields="all",
        wavelengths="primary",
        num_rays=5,
        figsize=(10, 4),
        title="Track A two-conic-mirror seed",
    )
    fig.savefig(run_dir / "layout.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, _ = spot.view(figsize=(12, 4), add_airy_disk=True, show=False)
    fig.savefig(run_dir / "spot.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    mtf = GeometricMTF(
        lens,
        fields="all",
        wavelength=0.55,
        num_rays=160,
        num_points=256,
        max_freq=220,
    )
    fig, _ = mtf.view(figsize=(9, 5), add_reference=True)
    fig.savefig(run_dir / "mtf.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    freq = np.asarray(mtf.freq, dtype=float)
    nyquist_mtf = []
    for field_data in mtf.mtf:
        arr = np.asarray(field_data, dtype=float)
        nyquist_mtf.append(
            {
                "tangential": float(np.interp(NYQUIST_CY_PER_MM, freq, arr[0])),
                "sagittal": float(np.interp(NYQUIST_CY_PER_MM, freq, arr[1])),
            }
        )

    wfe = RmsWavefrontErrorVsField(
        lens, num_fields=9, wavelengths=[0.55], num_rays=10
    )
    fig, _ = wfe.view(figsize=(7, 4.5), show=False)
    fig.savefig(run_dir / "wavefront.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    return {
        "nyquist_frequency_cy_per_mm": NYQUIST_CY_PER_MM,
        "geometric_mtf_at_nyquist_by_field": nyquist_mtf,
        "rms_wavefront_error_waves_0p55um_vs_normalized_field": np.asarray(
            wfe._wavefront_error, dtype=float
        )[:, 0].tolist(),
    }


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    run_dir = project_root / "runs" / "run_001"
    if run_dir.exists():
        raise FileExistsError(f"Refusing to overwrite existing run: {run_dir}")
    run_dir.mkdir(parents=True)

    candidates = {
        "scaled_achromatic_doublet": build_doublet(),
        "scaled_air_spaced_triplet": build_triplet(),
        "scaled_multi_element_telephoto": build_telephoto(),
        "two_conic_mirrors": build_two_mirror(),
    }
    metrics = {
        "run_id": "run_001",
        "stage": "first-order architecture screening",
        "source_requirements": {
            "spectral_band_um": [0.43, 0.80],
            "horizontal_fov_deg": 0.81,
            "ifov_urad_per_pixel": 3.45,
            "f_number": 6.2,
            "minimum_focus_distance_m": 800,
        },
        "derived": {
            "target_efl_mm": TARGET_EFL_MM,
            "target_epd_mm": TARGET_EPD_MM,
            "active_fov_deg": [0.809645, 0.593006],
            "corner_field_deg": FIELDS_DEG[-1],
            "paraxial_800m_to_infinity_focus_shift_mm": 0.7892,
            "detector_nyquist_cy_per_mm": NYQUIST_CY_PER_MM,
        },
        "benchmark_assumptions": {
            "field_samples_deg": list(FIELDS_DEG),
            "wavelength_samples_um": list(WAVELENGTHS_UM),
            "selection_basis": "polychromatic RMS spot, geometry, manufacturability, complexity and comparative cost",
        },
        "candidates": [candidate_metrics(name, lens) for name, lens in candidates.items()],
        "selected_for_next_stage": "two_conic_mirrors, with a possible small field-corrector group",
        "unverified_or_failed_constraints": [
            "Physical secondary obstruction and baffle vignetting are not yet modelled.",
            "Distortion and relative illumination were not evaluated in this screen.",
            "Thermal behavior, tolerances, coatings and stray light remain unevaluated.",
            "The 800 m object distance requires a later finite-conjugate/refocus model.",
            "No customer image-quality, package or distortion limit was supplied.",
        ],
    }

    selected = candidates["two_conic_mirrors"]
    selected_spot_um, selected_spot = spot_metrics(selected)
    metrics["selected_candidate_details"] = mirror_footprints(selected)
    metrics["selected_candidate_details"].update(save_plots(run_dir, selected, selected_spot))
    metrics["selected_candidate_details"]["airy_radius_um_at_0p55um"] = (
        1.22 * 0.55 * abs(float(selected.paraxial.FNO()))
    )
    metrics["selected_candidate_details"]["rms_spot_radius_um"] = selected_spot_um.tolist()

    save_prescription(run_dir, selected)
    (run_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    shutil.copy2(__file__, run_dir / Path(__file__).name)
    (run_dir / "summary.md").write_text(
        """# Track A Run 001 Architecture Screening

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
""",
        encoding="utf-8",
    )
    print(json.dumps(metrics["selected_candidate_details"], indent=2))


if __name__ == "__main__":
    main()
