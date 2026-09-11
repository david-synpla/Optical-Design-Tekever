#!/usr/bin/env python3
"""Track C Run 015: bounded physical C02 shared-coaxial experiment.

The run first falsifies/qualifies a directly power-bearing shared Cassegrain,
then tests a minimum-complexity coaxial afocal pupil-relay derivative.  It
explicitly records real-ray footprints, physical secondary/primary-hole
obscuration, vignetting, and paraxial entrance-pupil images for EO and SWIR.
No detailed backend prescription optimization is performed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import optiland
import yaml
from optiland import optic
from optiland.physical_apertures import RadialAperture


ROOT = next(p for p in Path(__file__).resolve().parents if (p / "WORK_GUIDE.md").exists())
REQ_PATH = ROOT / "requirements" / "eo_swir_system_requirements.yaml"
OUT = ROOT / "runs" / "run_015"
MARGIN_MM = 1.0  # screening assembly/edge allowance, not a customer requirement


def scalar(value):
    return float(np.asarray(value).reshape(-1)[0])


def channel_data(requirements: dict, name: str) -> dict:
    item = requirements["source_explicit_requirements"][name]
    pitch_mm = item["pixel_pitch_um"][0] / 1000.0
    ifov_rad = item["instantaneous_fov_urad_per_pixel"] * 1e-6
    efl = pitch_mm / ifov_rad
    pupil = efl / item["f_number"]
    half_x = math.degrees(math.atan(item["array_px"][0] * pitch_mm / (2 * efl)))
    half_y = math.degrees(math.atan(item["array_px"][1] * pitch_mm / (2 * efl)))
    diagonal = math.hypot(half_x, half_y)
    return {
        "name": name.upper(),
        "efl_mm": efl,
        "pupil_mm": pupil,
        "half_field_x_deg": half_x,
        "half_field_y_deg": half_y,
        "diagonal_half_field_deg": diagonal,
        "hx": half_x / diagonal,
        "hy": half_y / diagonal,
        "wavelengths_um": [0.43, 0.55, 0.80] if name == "eo" else [0.80, 1.20, 1.80],
    }


def normalized_fields(channel: dict) -> list[tuple[str, float, float]]:
    hx, hy = channel["hx"], channel["hy"]
    return [
        ("center", 0.0, 0.0),
        ("+x", hx, 0.0),
        ("-x", -hx, 0.0),
        ("+y", 0.0, hy),
        ("-y", 0.0, -hy),
        ("corner++", hx, hy),
        ("corner+-", hx, -hy),
        ("corner-+", -hx, hy),
        ("corner--", -hx, -hy),
    ]


def pupil_disk(n_rings: int = 48, n_azimuth: int = 96) -> tuple[np.ndarray, np.ndarray]:
    radii = np.sqrt((np.arange(n_rings) + 0.5) / n_rings) * 0.999
    theta = 2 * np.pi * (np.arange(n_azimuth) + 0.5) / n_azimuth
    return (radii[:, None] * np.cos(theta)).ravel(), (radii[:, None] * np.sin(theta)).ravel()


PX, PY = pupil_disk()


def set_field_wavelengths(model: optic.Optic, channel: dict) -> None:
    model.set_aperture(aperture_type="EPD", value=channel["pupil_mm"])
    model.fields.set_type("angle")
    model.fields.add(y=0)
    model.fields.add(y=channel["diagonal_half_field_deg"])
    for wavelength in channel["wavelengths_um"]:
        model.wavelengths.add(value=wavelength, is_primary=wavelength == channel["wavelengths_um"][1])


def direct_geometry(name: str, swir: dict, primary_speed: float, backfocus_mm: float) -> dict:
    final_efl = swir["efl_mm"]
    pupil = swir["pupil_mm"]
    primary_focal = primary_speed * pupil
    magnification = final_efl / primary_focal
    separation = (final_efl - backfocus_mm) / (magnification + 1)
    q = primary_focal - separation
    secondary_radius = -2 * q * (separation + backfocus_mm) / (separation + backfocus_mm - q)
    secondary_conic = -((magnification + 1) / (magnification - 1)) ** 2
    return {
        "name": name,
        "primary_speed": primary_speed,
        "backfocus_mm": backfocus_mm,
        "primary_focal_length_mm": primary_focal,
        "secondary_magnification": magnification,
        "mirror_separation_mm": separation,
        "primary_radius_mm": -2 * primary_focal,
        "primary_conic": -1.0,
        "secondary_radius_mm": secondary_radius,
        "secondary_conic": secondary_conic,
        "front_efl_mm": final_efl,
    }


def build_direct(
    geometry: dict,
    channel: dict,
    apertures: dict | None = None,
    downstream_stop_fraction: float | None = None,
    stop_radius_mm: float = 1000.0,
) -> tuple[optic.Optic, dict[str, int]]:
    sep = geometry["mirror_separation_mm"]
    backfocus = geometry["backfocus_mm"]
    physical = apertures is not None
    primary = apertures["primary_radius_mm"] if physical else 1000.0
    secondary = apertures["secondary_radius_mm"] if physical else 1000.0
    hole = apertures["primary_hole_radius_mm"] if physical else 1000.0

    model = optic.Optic(name=f"C02 direct shared Cassegrain {geometry['name']} {channel['name']}")
    model.surfaces.add(index=0, thickness=np.inf)
    entrance_aperture = RadialAperture(primary, secondary if physical else 0.0)
    entrance_is_stop = downstream_stop_fraction is None
    model.surfaces.add(index=1, thickness=sep + 3.0, is_stop=entrance_is_stop, aperture=entrance_aperture)
    model.surfaces.add(
        index=2,
        radius=geometry["primary_radius_mm"],
        thickness=-sep,
        conic=geometry["primary_conic"],
        material="mirror",
        aperture=RadialAperture(primary, hole if physical else 0.0),
    )
    if downstream_stop_fraction is None:
        model.surfaces.add(
            index=3,
            radius=geometry["secondary_radius_mm"],
            thickness=sep,
            conic=geometry["secondary_conic"],
            material="mirror",
            aperture=RadialAperture(secondary),
        )
        model.surfaces.add(index=4, thickness=backfocus, aperture=RadialAperture(hole))
        model.surfaces.add(index=5)
        indices = {"entrance": 1, "primary": 2, "secondary": 3, "primary_hole": 4, "image": 5}
    else:
        alpha = downstream_stop_fraction
        model.surfaces.add(
            index=3,
            radius=geometry["secondary_radius_mm"],
            thickness=alpha * sep,
            conic=geometry["secondary_conic"],
            material="mirror",
            aperture=RadialAperture(secondary),
        )
        model.surfaces.add(
            index=4,
            thickness=(1 - alpha) * sep,
            is_stop=True,
            aperture=RadialAperture(stop_radius_mm),
        )
        model.surfaces.add(index=5, thickness=backfocus, aperture=RadialAperture(hole))
        model.surfaces.add(index=6)
        indices = {"entrance": 1, "primary": 2, "secondary": 3, "eo_stop": 4, "primary_hole": 5, "image": 6}
    set_field_wavelengths(model, channel)
    return model, indices


def afocal_geometry(compression: float, swir: dict, primary_speed: float = 2.0) -> dict:
    pupil = swir["pupil_mm"]
    primary_focal = primary_speed * pupil
    secondary_focal = primary_focal / compression
    return {
        "name": f"A{int(compression)}_f{str(primary_speed).replace('.', 'p')}",
        "compression": compression,
        "primary_speed": primary_speed,
        "primary_focal_length_mm": primary_focal,
        "secondary_focal_length_magnitude_mm": secondary_focal,
        "mirror_separation_mm": primary_focal - secondary_focal,
        "primary_radius_mm": -2 * primary_focal,
        "primary_conic": -1.0,
        "secondary_radius_mm": -2 * secondary_focal,
        "secondary_conic": -1.0,
        "split_distance_after_primary_mm": 50.0,
    }


def build_afocal(
    geometry: dict,
    channel: dict,
    apertures: dict | None = None,
    downstream_stop: bool = True,
    stop_radius_mm: float = 1000.0,
) -> tuple[optic.Optic, dict[str, int]]:
    sep = geometry["mirror_separation_mm"]
    physical = apertures is not None
    primary = apertures["primary_radius_mm"] if physical else 1000.0
    secondary = apertures["secondary_radius_mm"] if physical else 1000.0
    hole = apertures["primary_hole_radius_mm"] if physical else 1000.0
    model = optic.Optic(name=f"C02 coaxial afocal {geometry['name']} {channel['name']}")
    model.surfaces.add(index=0, thickness=np.inf)
    model.surfaces.add(
        index=1,
        thickness=sep + 3.0,
        is_stop=not downstream_stop,
        aperture=RadialAperture(primary, secondary if physical else 0.0),
    )
    model.surfaces.add(
        index=2,
        radius=geometry["primary_radius_mm"],
        thickness=-sep,
        conic=-1.0,
        material="mirror",
        aperture=RadialAperture(primary, hole if physical else 0.0),
    )
    model.surfaces.add(
        index=3,
        radius=geometry["secondary_radius_mm"],
        thickness=sep,
        conic=-1.0,
        material="mirror",
        aperture=RadialAperture(secondary),
    )
    model.surfaces.add(index=4, thickness=geometry["split_distance_after_primary_mm"], aperture=RadialAperture(hole))
    model.surfaces.add(index=5, is_stop=downstream_stop, aperture=RadialAperture(stop_radius_mm))
    set_field_wavelengths(model, channel)
    return model, {"entrance": 1, "primary": 2, "secondary": 3, "primary_hole": 4, "pupil_split_plane": 5}


def trace_model(model: optic.Optic, indices: dict[str, int], channel: dict, field: tuple[str, float, float], wavelength: float | None = None) -> dict:
    label, hx, hy = field
    wavelength = wavelength if wavelength is not None else channel["wavelengths_um"][1]
    rays = model.ray_tracer.trace_generic(
        np.full(PX.size, hx), np.full(PX.size, hy), PX, PY, wavelength
    )
    intensity = np.asarray(model.surfaces.intensity)
    x = np.asarray(model.surfaces.x)
    y = np.asarray(model.surfaces.y)
    final_valid = np.isfinite(np.asarray(rays.x)) & (np.asarray(rays.i) > 0)
    surfaces = {}
    for name, index in indices.items():
        valid = np.isfinite(x[index]) & np.isfinite(y[index]) & (intensity[index] > 0)
        if np.any(valid):
            radii = np.hypot(x[index, valid], y[index, valid])
            surfaces[name] = {
                "survival_fraction": float(np.mean(valid)),
                "centroid_mm": [float(np.mean(x[index, valid])), float(np.mean(y[index, valid]))],
                "max_radius_mm": float(np.max(radii)),
                "x_range_mm": [float(np.min(x[index, valid])), float(np.max(x[index, valid]))],
                "y_range_mm": [float(np.min(y[index, valid])), float(np.max(y[index, valid]))],
            }
        else:
            surfaces[name] = {"survival_fraction": 0.0, "centroid_mm": [math.nan, math.nan], "max_radius_mm": math.nan}
    result = {
        "field": label,
        "normalized_field": [hx, hy],
        "wavelength_um": wavelength,
        "final_survival_fraction": float(np.mean(final_valid)),
        "surfaces": surfaces,
    }
    if "image" in indices and np.any(final_valid):
        points = np.column_stack([np.asarray(rays.x)[final_valid], np.asarray(rays.y)[final_valid]])
        centroid = points.mean(axis=0)
        result["image_centroid_mm"] = centroid.tolist()
        result["image_rms_um"] = float(np.sqrt(np.mean(np.sum((points - centroid) ** 2, axis=1))) * 1000)
    if "pupil_split_plane" in indices and np.any(final_valid):
        index = indices["pupil_split_plane"]
        L = np.asarray(model.surfaces.L)[index, final_valid]
        M = np.asarray(model.surfaces.M)[index, final_valid]
        N = np.asarray(model.surfaces.N)[index, final_valid]
        result["output_mean_direction"] = [float(np.mean(L)), float(np.mean(M)), float(np.mean(N))]
        result["output_direction_rms_urad"] = float(
            np.sqrt(np.var(L) + np.var(M)) * 1e6
        )
    return result


def size_apertures(builder, geometry: dict, channels: list[dict], downstream=False) -> tuple[dict, dict]:
    maxima = {"primary": 0.0, "secondary": 0.0, "primary_hole": 0.0}
    traces = {}
    for channel in channels:
        if builder is build_direct:
            model, indices = builder(geometry, channel, apertures=None)
        else:
            model, indices = builder(geometry, channel, apertures=None, downstream_stop=False)
        channel_rows = []
        for field in normalized_fields(channel):
            row = trace_model(model, indices, channel, field)
            channel_rows.append(row)
            for name in maxima:
                maxima[name] = max(maxima[name], row["surfaces"][name]["max_radius_mm"])
        traces[channel["name"]] = channel_rows
    apertures = {
        "primary_radius_mm": maxima["primary"] + MARGIN_MM,
        "secondary_radius_mm": maxima["secondary"] + MARGIN_MM,
        "primary_hole_radius_mm": maxima["primary_hole"] + MARGIN_MM,
        "sizing_margin_mm": MARGIN_MM,
        "basis": "union of EO and SWIR nine-field real-ray footprints plus 1 mm radial screening margin",
    }
    return apertures, traces


def physical_evaluation(builder, geometry: dict, apertures: dict, channels: list[dict], **kwargs) -> dict:
    result = {"geometry": geometry, "physical_apertures": apertures, "channels": {}}
    for channel in channels:
        model, indices = builder(geometry, channel, apertures=apertures, **kwargs)
        rows = [trace_model(model, indices, channel, field) for field in normalized_fields(channel)]
        result["channels"][channel["name"]] = {
            "paraxial_entrance_pupil_z_mm": scalar(model.paraxial.entrance_pupil_z()),
            "rows": rows,
            "minimum_survival_fraction": min(row["final_survival_fraction"] for row in rows),
            "center_survival_fraction": rows[0]["final_survival_fraction"],
            "maximum_image_rms_um": max((row.get("image_rms_um", 0.0) for row in rows)),
        }
    return result


def downstream_direct_stop_sweep(geometry: dict, apertures: dict, eo: dict) -> list[dict]:
    results = []
    for fraction in (0.2, 0.5, 0.8):
        probe, indices = build_direct(geometry, eo, apertures=apertures, downstream_stop_fraction=fraction, stop_radius_mm=1000)
        center = trace_model(probe, indices, eo, normalized_fields(eo)[0])
        stop_radius = center["surfaces"]["eo_stop"]["max_radius_mm"] + 0.2
        model, indices = build_direct(geometry, eo, apertures=apertures, downstream_stop_fraction=fraction, stop_radius_mm=stop_radius)
        rows = [trace_model(model, indices, eo, field) for field in normalized_fields(eo)]
        entrance_centroids = [row["surfaces"]["entrance"]["centroid_mm"] for row in rows]
        pupil_walk = max(math.hypot(*centroid) for centroid in entrance_centroids)
        results.append(
            {
                "fraction_secondary_to_primary": fraction,
                "physical_stop_radius_mm": stop_radius,
                "paraxial_entrance_pupil_z_mm": scalar(model.paraxial.entrance_pupil_z()),
                "entrance_plane_max_pupil_walk_mm": pupil_walk,
                "center_survival_fraction": rows[0]["final_survival_fraction"],
                "minimum_survival_fraction": min(row["final_survival_fraction"] for row in rows),
                "rows": rows,
            }
        )
    return results


def afocal_downstream_evaluation(geometry: dict, apertures: dict, channels: list[dict]) -> dict:
    result = {"geometry": geometry, "physical_apertures": apertures, "channels": {}}
    compression = geometry["compression"]
    for channel in channels:
        probe, indices = build_afocal(geometry, channel, apertures=apertures, downstream_stop=True, stop_radius_mm=1000)
        center_probe = trace_model(probe, indices, channel, normalized_fields(channel)[0])
        stop_radius = center_probe["surfaces"]["pupil_split_plane"]["max_radius_mm"] + 0.2
        model, indices = build_afocal(geometry, channel, apertures=apertures, downstream_stop=True, stop_radius_mm=stop_radius)
        rows = [trace_model(model, indices, channel, field) for field in normalized_fields(channel)]
        diag = rows[5]
        direction = diag.get("output_mean_direction")
        if direction is None:
            out_angle_deg = math.nan
        else:
            L, M, N = direction
            out_angle_deg = math.degrees(math.atan2(math.hypot(L, M), abs(N)))
        result["channels"][channel["name"]] = {
            "physical_stop_radius_mm": stop_radius,
            "paraxial_entrance_pupil_z_mm": scalar(model.paraxial.entrance_pupil_z()),
            "backend_target_efl_mm": channel["efl_mm"] / compression,
            "backend_target_pupil_mm": channel["pupil_mm"] / compression,
            "backend_diagonal_half_field_deg_paraxial": channel["diagonal_half_field_deg"] * compression,
            "real_output_diagonal_chief_angle_deg": out_angle_deg,
            "center_output_direction_rms_urad": rows[0]["output_direction_rms_urad"],
            "center_survival_fraction": rows[0]["final_survival_fraction"],
            "minimum_survival_fraction": min(row["final_survival_fraction"] for row in rows),
            "rows": rows,
        }
    return result


def flatten_summary(direct_results: list[dict], afocal_results: list[dict]) -> list[dict]:
    rows = []
    for result in direct_results:
        ap = result["physical_apertures"]
        rows.append(
            {
                "variant": f"direct_{result['geometry']['name']}",
                "primary_speed": result["geometry"]["primary_speed"],
                "afocal_compression": "",
                "primary_clear_diameter_mm": 2 * ap["primary_radius_mm"],
                "secondary_clear_diameter_mm": 2 * ap["secondary_radius_mm"],
                "primary_hole_diameter_mm": 2 * ap["primary_hole_radius_mm"],
                "secondary_to_eo_pupil_diameter_ratio": 2 * ap["secondary_radius_mm"] / direct_results[0]["channel_reference"]["EO"]["pupil_mm"],
                "eo_center_survival": result["channels"]["EO"]["center_survival_fraction"],
                "eo_min_survival": result["channels"]["EO"]["minimum_survival_fraction"],
                "swir_center_survival": result["channels"]["SWIR"]["center_survival_fraction"],
                "swir_min_survival": result["channels"]["SWIR"]["minimum_survival_fraction"],
                "backend_eo_diagonal_half_field_deg": "not modeled",
            }
        )
    for result in afocal_results:
        ap = result["physical_apertures"]
        rows.append(
            {
                "variant": f"afocal_{result['geometry']['name']}",
                "primary_speed": result["geometry"]["primary_speed"],
                "afocal_compression": result["geometry"]["compression"],
                "primary_clear_diameter_mm": 2 * ap["primary_radius_mm"],
                "secondary_clear_diameter_mm": 2 * ap["secondary_radius_mm"],
                "primary_hole_diameter_mm": 2 * ap["primary_hole_radius_mm"],
                "secondary_to_eo_pupil_diameter_ratio": 2 * ap["secondary_radius_mm"] / direct_results[0]["channel_reference"]["EO"]["pupil_mm"],
                "eo_center_survival": result["channels"]["EO"]["center_survival_fraction"],
                "eo_min_survival": result["channels"]["EO"]["minimum_survival_fraction"],
                "swir_center_survival": result["channels"]["SWIR"]["center_survival_fraction"],
                "swir_min_survival": result["channels"]["SWIR"]["minimum_survival_fraction"],
                "backend_eo_diagonal_half_field_deg": result["channels"]["EO"]["backend_diagonal_half_field_deg_paraxial"],
            }
        )
    return rows


def plot_layout(path: Path, builder, geometry: dict, apertures: dict, channels: list[dict], title: str, afocal=False) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    sample = np.linspace(-0.98, 0.98, 17)
    for ax, channel, color in zip(axes, channels, ("#2166ac", "#b2182b")):
        if afocal:
            model, indices = builder(geometry, channel, apertures=apertures, downstream_stop=True, stop_radius_mm=1000)
        else:
            model, indices = builder(geometry, channel, apertures=apertures)
        field = normalized_fields(channel)[5]
        model.ray_tracer.trace_generic(np.full(sample.size, field[1]), np.full(sample.size, field[2]), sample, np.zeros_like(sample), channel["wavelengths_um"][1])
        x = np.asarray(model.surfaces.x)
        z = np.asarray(model.surfaces.z)
        intensity = np.asarray(model.surfaces.intensity)
        for ray in range(sample.size):
            valid = np.isfinite(x[:, ray]) & np.isfinite(z[:, ray]) & (intensity[:, ray] > 0)
            if np.count_nonzero(valid) >= 2:
                ax.plot(z[valid, ray], x[valid, ray], color=color, alpha=0.45, linewidth=0.8)
        ax.axhline(0, color="black", linewidth=0.6)
        ax.set_ylabel(f"{channel['name']} x (mm)")
        ax.grid(True, alpha=0.2)
    axes[0].set_title(title + " — signed corner fan; clipped rays omitted")
    axes[-1].set_xlabel("Optiland global z coordinate (mm)")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_trade(path: Path, table: list[dict]) -> None:
    labels = [row["variant"].replace("direct_", "D-").replace("afocal_", "A-") for row in table]
    eo = [100 * row["eo_min_survival"] for row in table]
    swir = [100 * row["swir_min_survival"] for row in table]
    shadow = [100 * row["secondary_to_eo_pupil_diameter_ratio"] for row in table]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.bar(x - 0.22, eo, width=0.22, label="EO minimum transmitted pupil area")
    ax.bar(x, swir, width=0.22, label="SWIR minimum transmitted pupil area")
    ax.bar(x + 0.22, shadow, width=0.22, label="Secondary diameter / EO entrance-pupil diameter")
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel("Percent")
    ax.set_ylim(0, max(110, max(shadow) * 1.08))
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend()
    ax.set_title("Run 015 physical pupil/obscuration screen — no acceptance threshold imposed")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_prescription(path: Path, model: optic.Optic) -> None:
    rows = []
    for index, surface in enumerate(model.surfaces):
        rows.append(
            {
                "index": index,
                "radius_mm": scalar(surface.geometry.radius),
                "thickness_mm": scalar(surface.thickness),
                "conic": scalar(getattr(surface.geometry, "k", 0.0)),
                "is_reflective": surface.to_dict().get("interaction_model", {}).get("is_reflective", False),
                "material_after": surface.material_post.to_dict()["type"],
                "is_stop": index == model.surfaces.stop_index,
                "aperture": str(surface.aperture.to_dict()) if surface.aperture else "none",
            }
        )
    write_csv(path, rows)


def sanitize(value):
    if isinstance(value, dict):
        return {key: sanitize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def run(probe: bool = False) -> dict:
    requirements = yaml.safe_load(REQ_PATH.read_text(encoding="utf-8"))
    eo = channel_data(requirements, "eo")
    swir = channel_data(requirements, "swir")
    channels = [eo, swir]

    direct_specs = [
        direct_geometry("D1_f2p4_b200", swir, 2.4, 200.0),
        direct_geometry("D2_f1p5_b75", swir, 1.5, 75.0),
        direct_geometry("D3_f1p0_b50", swir, 1.0, 50.0),
    ]
    direct_results = []
    for geometry in direct_specs:
        apertures, open_traces = size_apertures(build_direct, geometry, channels)
        result = physical_evaluation(build_direct, geometry, apertures, channels)
        result["open_sizing_traces"] = open_traces
        result["channel_reference"] = {channel["name"]: channel for channel in channels}
        result["concentric_geometric_area_survival_proxy"] = {
            channel["name"]: max(0.0, 1 - (2 * apertures["secondary_radius_mm"] / channel["pupil_mm"]) ** 2)
            for channel in channels
        }
        direct_results.append(result)
    direct_stop = downstream_direct_stop_sweep(direct_specs[0], direct_results[0]["physical_apertures"], eo)

    afocal_results = []
    afocal_specs = [(2.0, 4.0), (2.0, 6.0), (2.0, 8.0), (2.0, 10.0), (1.5, 6.0), (1.0, 6.0), (1.0, 8.0)]
    for primary_speed, compression in afocal_specs:
        geometry = afocal_geometry(compression, swir, primary_speed=primary_speed)
        apertures, open_traces = size_apertures(build_afocal, geometry, channels)
        result = afocal_downstream_evaluation(geometry, apertures, channels)
        result["open_sizing_traces"] = open_traces
        result["channel_reference"] = {channel["name"]: channel for channel in channels}
        result["concentric_geometric_area_survival_proxy"] = {
            channel["name"]: max(0.0, 1 - (2 * apertures["secondary_radius_mm"] / channel["pupil_mm"]) ** 2)
            for channel in channels
        }
        afocal_results.append(result)

    summary_table = flatten_summary(direct_results, afocal_results)
    result = {
        "classification": "Stage C1 physical architecture experiment; aperture margins and variant geometry are engineering assumptions, not customer requirements",
        "channel_reference": {channel["name"]: channel for channel in channels},
        "direct_power_bearing": direct_results,
        "direct_D1_downstream_eo_stop_sweep": direct_stop,
        "coaxial_afocal_pupil_relay": afocal_results,
        "summary_table": summary_table,
    }
    if probe:
        print(json.dumps({
            "direct": [{"name": r["geometry"]["name"], "ap": r["physical_apertures"], "eo": r["channels"]["EO"]["minimum_survival_fraction"], "swir": r["channels"]["SWIR"]["minimum_survival_fraction"]} for r in direct_results],
            "afocal": [{"name": r["geometry"]["name"], "ap": r["physical_apertures"], "eo_center": r["channels"]["EO"]["center_survival_fraction"], "eo_min": r["channels"]["EO"]["minimum_survival_fraction"], "swir_center": r["channels"]["SWIR"]["center_survival_fraction"], "swir_min": r["channels"]["SWIR"]["minimum_survival_fraction"], "eo_stop_radius": r["channels"]["EO"]["physical_stop_radius_mm"], "eo_ep_z": r["channels"]["EO"]["paraxial_entrance_pupil_z_mm"], "eo_field": r["channels"]["EO"]["backend_diagonal_half_field_deg_paraxial"]} for r in afocal_results],
            "stop": [{k: v for k, v in row.items() if k != "rows"} for row in direct_stop],
        }, indent=2))
    return sanitize(result)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()
    start_wall = time.monotonic()
    start_utc = datetime.now(timezone.utc)
    if not args.probe and OUT.exists():
        raise RuntimeError(f"Refusing to overwrite immutable run directory: {OUT}")
    results = run(probe=args.probe)
    if args.probe:
        return
    OUT.mkdir(parents=False)
    write_json(OUT / "metrics.json", results)
    write_csv(OUT / "physical_screen.csv", results["summary_table"])

    direct = results["direct_power_bearing"]
    afocal = results["coaxial_afocal_pupil_relay"]
    plot_trade(OUT / "pupil_obscuration_trade.png", results["summary_table"])
    plot_layout(OUT / "direct_D1_layout.png", build_direct, direct[0]["geometry"], direct[0]["physical_apertures"], [results["channel_reference"]["EO"], results["channel_reference"]["SWIR"]], "Direct shared Cassegrain D1", afocal=False)
    recommended_afocal = next(item for item in afocal if item["geometry"]["name"] == "A6_f1p0")
    plot_layout(OUT / "afocal_A6_f1p0_layout.png", build_afocal, recommended_afocal["geometry"], recommended_afocal["physical_apertures"], [results["channel_reference"]["EO"], results["channel_reference"]["SWIR"]], "Coaxial afocal pupil relay A6, f/1 primary", afocal=True)
    direct_model, _ = build_direct(direct[1]["geometry"], results["channel_reference"]["SWIR"], apertures=direct[1]["physical_apertures"])
    write_prescription(OUT / "direct_D2_front_prescription.csv", direct_model)
    afocal_model, _ = build_afocal(recommended_afocal["geometry"], results["channel_reference"]["SWIR"], apertures=recommended_afocal["physical_apertures"], downstream_stop=True, stop_radius_mm=recommended_afocal["channels"]["SWIR"]["physical_stop_radius_mm"])
    write_prescription(OUT / "prescription.csv", afocal_model)

    dependencies = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "optiland": optiland.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "pyyaml": yaml.__version__,
    }
    write_json(OUT / "dependencies.json", dependencies)
    metadata = {
        "track": "C",
        "run_id": "015",
        "candidate_ids": ["C02"],
        "parent_run": "run_014",
        "purpose": "determine what form, if any, of common coaxial C02 merits further development using physical entrance-pupil, footprint, obscuration and vignetting evidence",
        "development_stage": "C1 low-cost numerical architecture screening",
        "start_time_utc": start_utc.isoformat(),
        "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "script_wall_seconds": time.monotonic() - start_wall,
        "substantial_computational_search_count": 4,
        "searches": ["direct shared Cassegrain speed/backfocus sweep", "direct EO downstream-stop pupil-image sweep", "coaxial afocal compression/pupil-relay sweep", "fast-primary afocal speed/compression check"],
        "materially_distinct_physical_model_experiments": 2,
        "optimization_attempt_count": 0,
        "plateau_counter": 0,
        "plateau_status": "not applicable; direct form stopped on structural pupil evidence before optimization",
        "candidate_decision": {"C02-D_direct_power_bearing": "PARKED", "C02-A6F1_coaxial_afocal_pupil_relay": "ACTIVE for one bounded backend/manufacturing feasibility run", "C02_family": "ACTIVE only through conditional afocal derivative"},
        "human_interventions": ["User supplied the pupil-ratio comparison to the 2024 shared-RC example and explicitly requested entrance-pupil/footprint testing before optimization."],
        "contamination_control": "reference/ not accessed",
    }
    write_json(OUT / "metadata.json", metadata)
    shutil.copy2(REQ_PATH, OUT / "requirements.yaml")
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)
    print(json.dumps({"out": str(OUT), "wall_seconds": metadata["script_wall_seconds"], "decision": metadata["candidate_decision"]}, indent=2))


if __name__ == "__main__":
    main()
