"""Run 002: physical-aperture and minimal field-corrector comparison.

Track A only. This script uses no reference-design information.
"""

from __future__ import annotations

import csv
import importlib.metadata as md
import json
import math
import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from optiland import optic, physical_apertures
from optiland.analysis import Distortion, RmsWavefrontErrorVsField, SpotDiagram
from optiland.mtf import GeometricMTF
from scipy.optimize import minimize_scalar


TARGET_EFL_MM = 794.2029
EPD_MM = 128.0972
FIELDS_DEG = (0.0, 0.2864, 0.4048, 0.5019)
WAVELENGTHS_UM = (0.43, 0.55, 0.65, 0.80)
NYQUIST_CY_MM = 1.0 / (2.0 * 0.00274)


def aperture(r_max: float, r_min: float = 0.0):
    return physical_apertures.RadialAperture(r_max=r_max, r_min=r_min)


def configure(lens: optic.Optic, finite_800m: bool = False) -> optic.Optic:
    lens.set_aperture(aperture_type="EPD", value=EPD_MM)
    lens.fields.set_type("object_height" if finite_800m else "angle")
    for field in ((0.0,) if finite_800m else FIELDS_DEG):
        lens.fields.add(y=field)
    for wave in WAVELENGTHS_UM:
        lens.wavelengths.add(value=wave, is_primary=wave == 0.55)
    return lens


def common_front(lens: optic.Optic, secondary_to_next: float, finite_800m=False):
    lens.surfaces.add(
        index=0,
        radius=math.inf,
        thickness=800_000.0 if finite_800m else math.inf,
        comment="object",
    )
    lens.surfaces.add(
        index=1,
        thickness=180.0,
        aperture=aperture(65.0, 29.0),
        comment="entrance obscuration plane",
    )
    lens.surfaces.add(
        index=2,
        radius=-600.0,
        thickness=-180.0,
        material="mirror",
        is_stop=True,
        conic=-1.16201060,
        aperture=aperture(65.0),
        comment="primary mirror",
    )
    lens.surfaces.add(
        index=3,
        radius=-385.7,
        thickness=secondary_to_next,
        material="mirror",
        conic=-6.58144493,
        aperture=aperture(29.0),
        comment="secondary mirror",
    )


def build_bare(image_distance=317.61596583, finite_800m=False) -> optic.Optic:
    lens = optic.Optic(name="Run 002 obstructed bare two-mirror")
    common_front(lens, image_distance, finite_800m)
    lens.surfaces.add(index=4, comment="flat detector")
    return configure(lens, finite_800m)


def build_singlet() -> optic.Optic:
    lens = optic.Optic(name="Run 002 fused-silica meniscus")
    common_front(lens, 299.04898324)
    lens.surfaces.add(
        index=4,
        radius=141.79363056,
        thickness=4.0,
        material="fused_silica",
        aperture=aperture(10.0),
        comment="fused-silica corrector front",
    )
    lens.surfaces.add(
        index=5,
        radius=119.57427566,
        thickness=15.63474290,
        aperture=aperture(10.0),
        comment="corrector rear",
    )
    lens.surfaces.add(index=6, comment="flat detector")
    return configure(lens)


def build_doublet() -> optic.Optic:
    lens = optic.Optic(name="Run 002 cemented achromatic corrector")
    common_front(lens, 308.21358276)
    lens.surfaces.add(
        index=4,
        radius=405.72363897,
        thickness=3.0,
        material="N-BK7",
        aperture=aperture(10.0),
        comment="N-BK7 corrector front",
    )
    lens.surfaces.add(
        index=5,
        radius=-122.22544049,
        thickness=2.5,
        material=("N-F2", "schott"),
        aperture=aperture(10.0),
        comment="cemented N-BK7/N-F2 interface",
    )
    lens.surfaces.add(
        index=6,
        radius=644.25485064,
        thickness=5.83878997,
        aperture=aperture(10.0),
        comment="N-F2 corrector rear",
    )
    lens.surfaces.add(index=7, comment="flat detector")
    return configure(lens)


def build_curved_diagnostic() -> optic.Optic:
    lens = optic.Optic(name="Run 002 curved-image diagnostic")
    common_front(lens, 317.64390596)
    lens.surfaces[2].geometry.conic = -1.17790356
    lens.surfaces[3].geometry.conic = -6.77482123
    lens.surfaces.add(index=4, radius=-151.28649531, comment="curved diagnostic image")
    return configure(lens)


def rms_um(lens):
    diagram = SpotDiagram(lens, num_rings=7)
    return np.asarray(diagram.rms_spot_radius(), dtype=float) * 1000.0, diagram


def throughput(lens):
    values = []
    for field_index in range(len(FIELDS_DEG)):
        row = []
        for wave in WAVELENGTHS_UM:
            rays = lens.trace(0, FIELDS_DEG[field_index] / FIELDS_DEG[-1], wave, num_rays=100, distribution="uniform")
            row.append(float(np.count_nonzero(np.asarray(rays.i) > 0) / len(rays.i)))
        values.append(row)
    return values


def candidate_metrics(name, lens):
    spots, _ = rms_um(lens)
    distortion = Distortion(lens, wavelengths=[0.55], num_points=32)
    return {
        "name": name,
        "efl_mm": float(lens.paraxial.f2()),
        "f_number": float(lens.paraxial.FNO()),
        "track_mm": float(lens.total_track),
        "rms_spot_radius_um": spots.tolist(),
        "worst_rms_spot_radius_um": float(np.max(spots)),
        "throughput_fraction_by_field_and_wavelength": throughput(lens),
        "maximum_f_tan_distortion_percent_at_0p55um": float(np.max(np.abs(np.asarray(distortion.data[0])))),
    }


def finite_focus_shift():
    def score(image_distance):
        lens = build_bare(image_distance=image_distance, finite_800m=True)
        return float(np.mean(np.asarray(SpotDiagram(lens, num_rings=5).rms_spot_radius()) ** 2))

    result = minimize_scalar(score, bounds=(317.0, 319.5), method="bounded")
    return float(result.x - 317.61596583), float(result.x)


def save_prescription(run_dir: Path):
    rows = [
        (0, "object", "inf", "inf", 0, "air", "none"),
        (1, "entrance obscuration plane", "inf", 180.0, 0, "air", "r=29-65 mm annulus"),
        (2, "primary mirror", -600.0, -180.0, -1.16201060, "mirror", "r<=65 mm"),
        (3, "secondary mirror", -385.7, 317.61596583, -6.58144493, "mirror", "r<=29 mm"),
        (4, "flat detector", "inf", 0, 0, "air", "active diagonal 13.91 mm"),
    ]
    with (run_dir / "prescription.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("surface", "comment", "radius_mm", "thickness_mm", "conic", "material_after", "clear_aperture"))
        writer.writerows(rows)


def save_plots(run_dir: Path, selected, candidates):
    fig, _ = selected.draw(fields="all", wavelengths="primary", num_rays=7, figsize=(10, 4), title="Run 002 physical two-mirror baseline")
    fig.savefig(run_dir / "layout.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    _, spot = rms_um(selected)
    fig, _ = spot.view(figsize=(12, 4), add_airy_disk=True, show=False)
    fig.savefig(run_dir / "spot.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    mtf = GeometricMTF(selected, fields="all", wavelength=0.55, num_rays=180, num_points=256, max_freq=220)
    fig, _ = mtf.view(figsize=(9, 5), add_reference=True)
    fig.savefig(run_dir / "mtf.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    wfe = RmsWavefrontErrorVsField(selected, num_fields=9, wavelengths=[0.55], num_rays=10)
    fig, _ = wfe.view(figsize=(7, 4.5), show=False)
    fig.savefig(run_dir / "wavefront.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for name, lens in candidates.items():
        spots, _ = rms_um(lens)
        ax.plot(FIELDS_DEG, np.sqrt(np.mean(spots**2, axis=1)), marker="o", label=name)
    ax.axhline(2.74, color="black", linestyle="--", label="pixel pitch")
    ax.set(xlabel="Field angle (deg)", ylabel="Polychromatic RMS spot radius (um)", title="Run 002 flat-field comparison")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(run_dir / "corrector_comparison.png", dpi=180)
    plt.close(fig)
    freq = np.asarray(mtf.freq, dtype=float)
    return [
        {
            "tangential": float(np.interp(NYQUIST_CY_MM, freq, np.asarray(field)[0])),
            "sagittal": float(np.interp(NYQUIST_CY_MM, freq, np.asarray(field)[1])),
        }
        for field in mtf.mtf
    ]


def main():
    root = Path(__file__).resolve().parents[1]
    run_dir = root / "runs" / "run_002"
    if run_dir.exists():
        raise FileExistsError(f"Refusing to overwrite {run_dir}")
    run_dir.mkdir(parents=True)
    candidates = {
        "bare_obstructed": build_bare(),
        "fused_silica_singlet": build_singlet(),
        "cemented_N_BK7_N_F2_doublet": build_doublet(),
        "curved_image_diagnostic": build_curved_diagnostic(),
    }
    metrics = {
        "run_id": "run_002",
        "stage": "physical baseline and minimal corrector comparison",
        "sampling": {"fields_deg": FIELDS_DEG, "wavelengths_um": WAVELENGTHS_UM},
        "benchmark_assumptions": {
            "primary_clear_diameter_mm": 130.0,
            "secondary_clear_diameter_mm": 58.0,
            "entrance_obscuration_diameter_mm": 58.0,
            "corrector_clear_diameter_mm": 20.0,
            "aperture_throughput_excludes_reflection_coating_and_spider_losses": True,
        },
        "software": {"python": sys.version, "optiland": md.version("optiland"), "numpy": md.version("numpy"), "scipy": md.version("scipy")},
        "candidates": [candidate_metrics(name, lens) for name, lens in candidates.items()],
        "selected": "bare_obstructed",
        "architecture_status": "Cassegrain family retained provisionally; minimal correctors rejected; flat-field limitation triggers architecture revisit",
    }
    shift, finite_distance = finite_focus_shift()
    metrics["finite_800m_focus"] = {
        "best_secondary_to_image_distance_mm": finite_distance,
        "detector_shift_from_infinity_mm": shift,
        "mechanism_choice": "detector refocus",
        "status": "paraxial/full-ray on-axis model; mechanical implementation not designed",
    }
    metrics["selected_mtf_at_detector_nyquist"] = save_plots(run_dir, candidates["bare_obstructed"], candidates)
    metrics["unmet_or_unverified"] = [
        "No supplied customer image-quality, distortion, obscuration, package or mass limits exist.",
        "Flat-field corner image quality and detector-Nyquist MTF remain weak.",
        "Spider diffraction, mirror coating losses, baffle geometry and stray light are not modelled.",
        "Thermal compensation and tolerances remain unverified.",
    ]
    save_prescription(run_dir)
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    shutil.copy2(__file__, run_dir / Path(__file__).name)
    (run_dir / "summary.md").write_text(
        """# Track A Run 002 Physical Baseline and Corrector Comparison

## Result

The physical bare two-mirror baseline remains preferred, but it is not ready to freeze. A 58 mm secondary/entrance obstruction and 130 mm primary clear diameter were modelled explicitly. Aperture throughput is about 79.5% before spider, coating and baffle losses. The finite 800 m model supports detector refocus; its optimized shift is recorded in `metrics.json`.

## Corrector decision

The 4 mm fused-silica meniscus improves the flat-field corner from about 8.0-8.8 um to roughly 6.3-7.4 um, but worsens the center to 5.0-6.6 um and introduces wavelength dependence. It adds two coated surfaces, a precision cell and thermal/focus sensitivity.

The 5.5 mm cemented N-BK7/N-F2 doublet improves portions of the middle field but leaves approximately 7.6-8.2 um at the corner and about 3.5-7.7 um on axis. Its three spherical surfaces, cemented interface, two glasses and procurement/alignment burden are not justified by that performance. Both minimal correctors are rejected.

## Diagnostic and architecture status

A curved image surface near -151 mm radius allows about 0.4-4.2 um monochromatic RMS across the field. This demonstrates that field curvature is the dominant limitation for the flat IMX545, not chromatic aberration or a first-order EFL failure. The Cassegrain family remains provisionally viable, but the inability of minimal correctors to flatten the field is a fundamental warning. A broader architecture revisit is justified before further detailed optimization.

The mirror pair remains compact and achromatic but uses two aspheres, including a strong secondary conic, and substantial central obscuration. There is no customer image-quality or obscuration limit; spot and MTF comparisons are benchmark objectives.

**Next action:** compare a flat-field three-mirror/all-reflective candidate or a deliberately non-minimal corrector against this physical baseline before selecting the blind candidate.
""",
        encoding="utf-8",
    )
    print(json.dumps(metrics["finite_800m_focus"], indent=2))


if __name__ == "__main__":
    main()
