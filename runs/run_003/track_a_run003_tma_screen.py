"""Run 003: bounded physical-feasibility screening of Track A candidate A04.

Track A only. This script uses no reference-design information.
"""

from __future__ import annotations

import argparse
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
from optiland.analysis import SpotDiagram
from scipy.optimize import least_squares


TARGET_EFL_MM = 794.2029
EPD_MM = 128.0972
FIELDS_DEG = (0.0, 0.2864, 0.4048, 0.5019)
WAVELENGTHS_UM = (0.43, 0.55, 0.65, 0.80)
FIELD_NORMALIZED = tuple(field / FIELDS_DEG[-1] for field in FIELDS_DEG)
DETECTOR_KEEPOUT_RADIUS_MM = math.hypot(11.22304 / 2, 8.22 / 2) + 1.0
SEED = [-383.333730, -1.15218742, -6.41899951, -1457.30254, -2.93018854, 313.478698, 7.26094452]
ATTEMPT_RESULTS = [
    [-369.0021548234158, -1.1531362418228104, -5.668997438896978, -769.7178264602898, -11.31970430215845, 312.356179498669, 28.58719064685741],
    [-478.12397940022714, -0.8178769229148599, -6.224226865613981, -160.48941192689435, -0.26925286002268484, 382.07144145007703, 185.94169475592824],
    [-524.2074579036746, -1.0071925056388178, -5.18415686351497, -196.38888513238297, -0.6223345332117669, 386.14969173245555, 247.19927747014142],
]


def aperture(r_max: float, r_min: float = 0.0):
    return physical_apertures.RadialAperture(r_max=r_max, r_min=r_min)


def build_tma(values):
    r2, k1, k2, r3, k3, secondary_to_tertiary, back_distance = values
    lens = optic.Optic(name="A04 coaxial TMA screening model")
    lens.surfaces.add(index=0, radius=math.inf, thickness=math.inf, comment="object")
    lens.surfaces.add(index=1, thickness=180.0, aperture=aperture(65.0, 29.0), comment="entrance obscuration plane")
    lens.surfaces.add(
        index=2, radius=-600.0, thickness=-180.0, material="mirror", is_stop=True,
        conic=k1, aperture=aperture(65.0), comment="primary mirror",
    )
    lens.surfaces.add(
        index=3, radius=r2, thickness=secondary_to_tertiary, material="mirror",
        conic=k2, aperture=aperture(29.0), comment="secondary mirror",
    )
    lens.surfaces.add(
        index=4, radius=r3, thickness=-back_distance, material="mirror",
        conic=k3, aperture=aperture(30.0), comment="tertiary mirror",
    )
    lens.surfaces.add(index=5, comment="flat detector")
    lens.set_aperture(aperture_type="EPD", value=EPD_MM)
    lens.fields.set_type("angle")
    for field in FIELDS_DEG:
        lens.fields.add(y=field)
    for wavelength in WAVELENGTHS_UM:
        lens.wavelengths.add(value=wavelength, is_primary=wavelength == 0.55)
    return lens


def coarse_metrics(values, num_rays=10):
    lens = build_tma(values)
    spots = np.asarray(SpotDiagram(lens, num_rings=3).rms_spot_radius(), dtype=float)[:, 1] * 1000.0
    secondary_tertiary_clearance = []
    primary_secondary_clearance = []
    throughput = []
    tertiary_footprint = []
    detector_z = values[5] - values[6]
    for field in FIELD_NORMALIZED:
        rays = lens.trace(0, field, 0.55, num_rays=num_rays, distribution="uniform")
        surface = lens.surfaces[3]
        valid = np.asarray(surface.intensity) > 0
        t = (detector_z - np.asarray(surface.z)[valid]) / np.asarray(surface.N)[valid]
        x = np.asarray(surface.x)[valid] + np.asarray(surface.L)[valid] * t
        y = np.asarray(surface.y)[valid] + np.asarray(surface.M)[valid] * t
        secondary_tertiary_clearance.append(float(np.min(np.hypot(x, y))))
        surface = lens.surfaces[2]
        valid = np.asarray(surface.intensity) > 0
        t = (detector_z - np.asarray(surface.z)[valid]) / np.asarray(surface.N)[valid]
        x = np.asarray(surface.x)[valid] + np.asarray(surface.L)[valid] * t
        y = np.asarray(surface.y)[valid] + np.asarray(surface.M)[valid] * t
        primary_secondary_clearance.append(float(np.min(np.hypot(x, y))))
        throughput.append(float(np.count_nonzero(np.asarray(rays.i) > 0) / len(rays.i)))
        t_surface = lens.surfaces[4]
        live_t = np.asarray(t_surface.intensity) > 0
        tertiary_footprint.append(float(np.max(np.hypot(np.asarray(t_surface.x)[live_t], np.asarray(t_surface.y)[live_t]))))
    return {
        "efl_mm": float(lens.paraxial.f2()),
        "f_number": float(lens.paraxial.FNO()),
        "rms_spot_radius_um_by_field": spots.tolist(),
        "secondary_to_tertiary_beam_min_radius_at_detector_plane_mm_by_field": secondary_tertiary_clearance,
        "primary_to_secondary_beam_min_radius_at_detector_plane_mm_by_field": primary_secondary_clearance,
        "minimum_detector_plane_ray_clearance_mm_by_field": np.minimum(secondary_tertiary_clearance, primary_secondary_clearance).tolist(),
        "throughput_fraction_by_field": throughput,
        "tertiary_footprint_radius_mm_by_field": tertiary_footprint,
    }


def residual(values, clearance_scale=0.35):
    try:
        metrics = coarse_metrics(values, num_rays=7)
        spots = np.asarray(metrics["rms_spot_radius_um_by_field"])
        clear = np.asarray(metrics["minimum_detector_plane_ray_clearance_mm_by_field"])
        throughput = np.asarray(metrics["throughput_fraction_by_field"])
        return np.concatenate([
            spots / 4.0,
            [(abs(metrics["efl_mm"]) - TARGET_EFL_MM) / 0.8],
            np.maximum(0.0, DETECTOR_KEEPOUT_RADIUS_MM - clear) / clearance_scale,
            np.maximum(0.0, 0.75 - throughput) / 0.02,
        ])
    except Exception:
        return np.full(13, 1e4)


def search(attempt):
    if attempt == 1:
        seed = np.array([-383.333730, -1.15218742, -6.41899951, -1457.30254, -2.93018854, 313.478698, 30.0])
        lower = np.array([-800.0, -3.0, -15.0, -4000.0, -15.0, 220.0, 25.0])
        upper = np.array([-180.0, 1.0, 3.0, -120.0, 3.0, 420.0, 100.0])
    elif attempt == 2:
        seed = np.array([-383.333730, -1.15218742, -6.41899951, -100.0, -2.93018854, 313.478698, 250.0])
        lower = np.array([-900.0, -4.0, -18.0, -4000.0, -20.0, 220.0, 150.0])
        upper = np.array([-150.0, 2.0, 5.0, -20.0, 5.0, 450.0, 300.0])
    else:
        seed = np.array([-478.1239794, -0.81787692, -6.22422687, -160.48941193, -0.26925286, 382.07144145, 250.0])
        lower = np.array([-900.0, -4.0, -18.0, -1500.0, -20.0, 330.0, 240.0])
        upper = np.array([-150.0, 2.0, 5.0, -20.0, 5.0, 450.0, 300.0])
    objective = residual if attempt < 3 else lambda values: residual(values, clearance_scale=0.18)
    result = least_squares(objective, seed, bounds=(lower, upper), max_nfev=350, verbose=2, x_scale="jac")
    print(json.dumps({
        "attempt": attempt, "success": bool(result.success), "message": result.message, "cost": float(result.cost),
        "nfev": int(result.nfev), "values": result.x.tolist(), "metrics": coarse_metrics(result.x, num_rays=18),
        "detector_keepout_radius_mm": DETECTOR_KEEPOUT_RADIUS_MM,
    }, indent=2))


def finalize():
    root = Path(__file__).resolve().parents[1]
    run_dir = root / "runs" / "run_003"
    if run_dir.exists():
        raise FileExistsError(f"Refusing to overwrite {run_dir}")
    run_dir.mkdir(parents=True)
    cases = [("run_002_seed", SEED)] + [(f"attempt_{i}", values) for i, values in enumerate(ATTEMPT_RESULTS, 1)]
    evaluated = []
    for name, values in cases:
        evaluated.append({"name": name, "parameters": dict(zip(
            ("secondary_radius_mm", "primary_conic", "secondary_conic", "tertiary_radius_mm", "tertiary_conic", "secondary_to_tertiary_mm", "tertiary_to_detector_return_mm"), values
        )), "metrics": coarse_metrics(values, num_rays=18)})
    metrics = {
        "run_id": "run_003",
        "track": "A",
        "candidate_id": "A04",
        "engineering_question": "Can a coaxial TMA retain a meaningful flat-field advantage while clearing a centered detector and both crossing beam legs?",
        "benchmark_assumptions": {
            "detector_keepout_radius_mm": DETECTOR_KEEPOUT_RADIUS_MM,
            "keepout_basis": "active sensor half-diagonal plus 1.0 mm radial benchmark margin; not a customer requirement",
            "primary_clear_radius_mm": 65.0,
            "secondary_clear_radius_mm": 29.0,
            "tertiary_clear_radius_mm": 30.0,
        },
        "sampling": {"fields_deg": FIELDS_DEG, "wavelengths_um": WAVELENGTHS_UM, "optimization_wavelength_um": 0.55},
        "software": {"python": sys.version, "optiland": md.version("optiland"), "numpy": md.version("numpy"), "scipy": md.version("scipy")},
        "cases": evaluated,
        "decision": "REJECT A04 coaxial topology at screening stage",
        "plateau": "three materially distinct attempts without a physically valid meaningful improvement",
        "omitted_outputs": "MTF and wavefront plots omitted because no physically clear candidate survived screening",
    }
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    (run_dir / "metadata.json").write_text(json.dumps({
        "track": "A", "run_id": "run_003", "candidate_ids": ["A04"], "parent_run": "run_002",
        "purpose": metrics["engineering_question"], "development_stage": "screening",
        "substantial_optimizer_search_count": 3, "materially_distinct_attempt_count": 3,
        "plateau_counter": 3, "plateau_status": "plateaued", "candidate_decision": "REJECTED",
        "resource_note": "Closed immediately after the third running attempt; user reported 14% remaining five-hour quota.",
    }, indent=2) + "\n", encoding="utf-8")
    with (run_dir / "prescription.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("surface", "comment", "radius_mm", "thickness_mm", "conic", "material_after", "clear_aperture", "status"))
        writer.writerows([
            (0, "object", "inf", "inf", 0, "air", "none", "screening seed only"),
            (1, "entrance obscuration plane", "inf", 180.0, 0, "air", "r=29-65 mm annulus", "screening seed only"),
            (2, "primary mirror", -600.0, -180.0, SEED[1], "mirror", "r<=65 mm", "screening seed only"),
            (3, "secondary mirror", SEED[0], SEED[5], SEED[2], "mirror", "r<=29 mm", "screening seed only"),
            (4, "tertiary mirror", SEED[3], -SEED[6], SEED[4], "mirror", "r<=30 mm", "screening seed only"),
            (5, "flat detector", "inf", 0, 0, "air", "active diagonal 13.91 mm", "physically obstructs incoming beam"),
        ])
    lens = build_tma(SEED)
    fig, _ = lens.draw(fields="all", wavelengths="primary", num_rays=7, figsize=(10, 4), title="Run 003 A04 nominal seed (physically obstructed)")
    fig.savefig(run_dir / "layout.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    spot = SpotDiagram(lens, num_rings=7)
    fig, _ = spot.view(figsize=(12, 4), add_airy_disk=True, show=False)
    fig.savefig(run_dir / "spot.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    for case in evaluated:
        ax.plot(FIELDS_DEG, case["metrics"]["minimum_detector_plane_ray_clearance_mm_by_field"], marker="o", label=case["name"])
    ax.axhline(DETECTOR_KEEPOUT_RADIUS_MM, color="black", linestyle="--", label="detector keepout")
    ax.set(xlabel="Field angle (deg)", ylabel="Minimum ray radius at detector plane (mm)", title="A04 detector-plane clearance screen")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(run_dir / "clearance.png", dpi=180)
    plt.close(fig)
    (run_dir / "summary.md").write_text("""# Track A Run 003 - A04 Coaxial TMA Physical Screen

## Decision

Reject A04's coaxial topology at the screening stage. The Run 002 seed's attractive nominal 4.7/3.0/3.1/4.9 um monochromatic RMS spots are not physically usable: the pre-tertiary beam passes through the centered detector location, reaching only 0.59 mm minimum radius on axis versus a 7.96 mm keepout benchmark assumption.

Three materially distinct constrained attempts did not produce a meaningful physically valid improvement. Attempt 1 retained useful nominal spots and EFL but only 0.30 mm minimum clearance. Attempt 2 used a long return geometry and restored approximately 793.95 mm EFL with 1.4-9.7 um RMS, yet clearance remained 0.29 mm. Attempt 3 hard-constrained the long return and strengthened clearance weighting; it still achieved only 1.53 mm worst-field clearance, missed EFL at 815.58 mm, and degraded RMS spots to approximately 77-80 um. The stage is plateaued under workflow v3.

The 7.96 mm keepout is not a customer requirement; it is the active sensor half-diagonal plus a 1 mm radial screening margin. Even the active area alone would obstruct every attempted layout. MTF and wavefront outputs are omitted because no physically clear candidate survived.

## Engineering consequence

The failure is topological rather than evidence against all three-mirror systems. A centered detector on the coaxial tertiary return path conflicts with the incoming beam. A materially different off-axis/decentered three-mirror branch may avoid this, but it must receive a new candidate ID and run because its alignment, fabrication and packaging trade space differs.

**Next action:** open a separate bounded screening run for an off-axis/decentered reflective branch and compare its mechanical feasibility against parked A01.
""", encoding="utf-8")
    shutil.copy2(__file__, run_dir / Path(__file__).name)
    print(json.dumps({"run_dir": str(run_dir), "decision": metrics["decision"]}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search", type=int, choices=(1, 2, 3))
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    if args.finalize:
        finalize()
    elif args.search:
        search(args.search)
    else:
        print(json.dumps({"values": SEED, "metrics": coarse_metrics(SEED, num_rays=18), "detector_keepout_radius_mm": DETECTOR_KEEPOUT_RADIUS_MM}, indent=2))


if __name__ == "__main__":
    main()
