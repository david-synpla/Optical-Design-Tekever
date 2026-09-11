#!/usr/bin/env python3
"""Track C Run 016: bounded C02-A6F1 image/pupil/backend feasibility test.

The first experiment couples the immutable Run 015 A6_f1p0 common front end
to perfect paraxial cameras.  It measures what the common front itself does to
full-field images, wavefronts, pupils, transmission and diffraction.  A real
backend or one extra-power diagnostic is only attempted if that evidence
supports continuing C02.
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
from optiland.psf import ScalarFFTPSF
from scipy.optimize import least_squares


ROOT = next(p for p in Path(__file__).resolve().parents if (p / "WORK_GUIDE.md").exists())
REQ_PATH = ROOT / "requirements" / "eo_swir_system_requirements.yaml"
OUT = ROOT / "runs" / "run_016"

# Exact Run 015 survivor; no front-end variable is optimized here.
GEOMETRY = {
    "name": "A6_f1p0",
    "compression": 6.0,
    "primary_focal_length_mm": 311.3712791132146,
    "secondary_focal_length_magnitude_mm": 51.895213185535766,
    "mirror_separation_mm": 259.47606592767886,
    "primary_radius_mm": -622.7425582264292,
    "secondary_radius_mm": -103.79042637107153,
    "split_distance_after_primary_mm": 50.0,
}
APERTURES = {
    "primary_radius_mm": 156.74936241416827,
    "secondary_radius_mm": 28.12436290261479,
    "primary_hole_radius_mm": 34.789984775974425,
    "EO_stop_radius_mm": 10.808407808944981,
    "SWIR_stop_radius_mm": 26.147,  # rounded up from Run 015 25.9863 + the same 0.2 mm stop margin
}


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
        "pixel_pitch_mm": pitch_mm,
        "half_field_x_deg": half_x,
        "half_field_y_deg": half_y,
        "diagonal_half_field_deg": diagonal,
        "hx": half_x / diagonal,
        "hy": half_y / diagonal,
        "wavelengths_um": [0.43, 0.55, 0.80] if name == "eo" else [0.80, 1.20, 1.80],
    }


def fields(channel: dict) -> list[tuple[str, float, float]]:
    hx, hy = channel["hx"], channel["hy"]
    return [
        ("center", 0.0, 0.0),
        ("+x", hx, 0.0), ("-x", -hx, 0.0),
        ("+y", 0.0, hy), ("-y", 0.0, -hy),
        ("corner++", hx, hy), ("corner+-", hx, -hy),
        ("corner-+", -hx, hy), ("corner--", -hx, -hy),
    ]


def set_configuration(model: optic.Optic, channel: dict) -> None:
    model.set_aperture(aperture_type="EPD", value=channel["pupil_mm"])
    model.fields.set_type("angle")
    model.fields.add(y=0)
    model.fields.add(y=channel["diagonal_half_field_deg"])
    for wavelength in channel["wavelengths_um"]:
        model.wavelengths.add(value=wavelength, is_primary=wavelength == channel["wavelengths_um"][1])


def build_ideal(channel: dict, lens_distance_mm: float = 0.0, pupil_lens_f_mm: float | None = None,
                focus_delta_mm: float = 0.0, diffraction_stop_at_entrance: bool = False):
    """A6 front plus a perfect channel camera; optional extra thin pupil-control power."""
    sep = GEOMETRY["mirror_separation_mm"]
    fcam = channel["efl_mm"] / GEOMETRY["compression"]
    stop = APERTURES[f"{channel['name']}_stop_radius_mm"]
    m = optic.Optic(name=f"C02 A6F1 ideal {channel['name']} backend")
    m.surfaces.add(index=0, thickness=np.inf)
    m.surfaces.add(index=1, thickness=sep + 3.0, is_stop=diffraction_stop_at_entrance,
                   aperture=RadialAperture(APERTURES["primary_radius_mm"], APERTURES["secondary_radius_mm"]))
    m.surfaces.add(index=2, radius=GEOMETRY["primary_radius_mm"], thickness=-sep,
                   conic=-1.0, material="mirror",
                   aperture=RadialAperture(APERTURES["primary_radius_mm"], APERTURES["primary_hole_radius_mm"]))
    m.surfaces.add(index=3, radius=GEOMETRY["secondary_radius_mm"], thickness=sep,
                   conic=-1.0, material="mirror", aperture=RadialAperture(APERTURES["secondary_radius_mm"]))
    m.surfaces.add(index=4, thickness=GEOMETRY["split_distance_after_primary_mm"],
                   aperture=RadialAperture(APERTURES["primary_hole_radius_mm"]))
    if pupil_lens_f_mm is None:
        m.surfaces.add(index=5, thickness=lens_distance_mm, is_stop=not diffraction_stop_at_entrance,
                       aperture=RadialAperture(stop))
        m.surfaces.add(index=6, surface_type="paraxial", f=fcam, thickness=fcam + focus_delta_mm,
                       aperture=RadialAperture(stop + 4.0))
        m.surfaces.add(index=7)
        indices = {"split": 5, "camera": 6, "image": 7}
    else:
        # One deliberately ideal extra powered degree of freedom.  It is a
        # diagnostic for pupil controllability, not a manufacturable prescription.
        m.surfaces.add(index=5, thickness=lens_distance_mm, is_stop=not diffraction_stop_at_entrance,
                       aperture=RadialAperture(stop))
        m.surfaces.add(index=6, surface_type="paraxial", f=pupil_lens_f_mm, thickness=40.0,
                       aperture=RadialAperture(stop + 4.0))
        # Choose the final ideal camera power to keep the combined paraxial EFL near target.
        m.surfaces.add(index=7, surface_type="paraxial", f=fcam, thickness=fcam + focus_delta_mm,
                       aperture=RadialAperture(stop + 8.0))
        m.surfaces.add(index=8)
        indices = {"split": 5, "pupil_power": 6, "camera": 7, "image": 8}
    set_configuration(m, channel)
    return m, indices


def build_real_doublet(channel: dict, x):
    """Minimum physical camera: two separated spherical catalog-material elements."""
    sep = GEOMETRY["mirror_separation_mm"]
    c1, c2, c3, c4, gap, image_distance = x
    stop = APERTURES[f"{channel['name']}_stop_radius_mm"]
    radius = stop + (3.0 if channel["name"] == "EO" else 5.0)
    t1, t2 = ((4.0, 3.0) if channel["name"] == "EO" else (7.0, 6.0))
    materials = ("N-BK7", "N-F2") if channel["name"] == "EO" else ("fused_silica", "LITHOTEC-CAF2")
    m = optic.Optic(name=f"C02 A6F1 real spherical doublet {channel['name']}")
    m.surfaces.add(index=0, thickness=np.inf)
    m.surfaces.add(index=1, thickness=sep + 3.0,
                   aperture=RadialAperture(APERTURES["primary_radius_mm"], APERTURES["secondary_radius_mm"]))
    m.surfaces.add(index=2, radius=GEOMETRY["primary_radius_mm"], thickness=-sep,
                   conic=-1.0, material="mirror",
                   aperture=RadialAperture(APERTURES["primary_radius_mm"], APERTURES["primary_hole_radius_mm"]))
    m.surfaces.add(index=3, radius=GEOMETRY["secondary_radius_mm"], thickness=sep,
                   conic=-1.0, material="mirror", aperture=RadialAperture(APERTURES["secondary_radius_mm"]))
    m.surfaces.add(index=4, thickness=GEOMETRY["split_distance_after_primary_mm"],
                   aperture=RadialAperture(APERTURES["primary_hole_radius_mm"]))
    m.surfaces.add(index=5, thickness=5.0, is_stop=True, aperture=RadialAperture(stop))
    surfaces = [(c1, t1, materials[0]), (c2, gap, "air"), (c3, t2, materials[1]),
                (c4, image_distance, "air")]
    for index, (curvature, thickness, material) in enumerate(surfaces, start=6):
        radius_mm = 1.0 / curvature if abs(curvature) > 1e-8 else np.inf
        m.surfaces.add(index=index, radius=radius_mm, thickness=thickness, material=material,
                       aperture=RadialAperture(radius))
    m.surfaces.add(index=10)
    set_configuration(m, channel)
    return m, {"split": 5, "lens_1_front": 6, "lens_1_back": 7, "lens_2_front": 8,
               "lens_2_back": 9, "image": 10}


def disk_sample(nrings=48, naz=96):
    r = np.sqrt((np.arange(nrings) + 0.5) / nrings) * 0.999
    a = 2 * np.pi * (np.arange(naz) + 0.5) / naz
    return (r[:, None] * np.cos(a)).ravel(), (r[:, None] * np.sin(a)).ravel()


def ellipse_metrics(x, y):
    pts = np.column_stack([x, y])
    c = pts.mean(axis=0)
    centered = pts - c
    cov = centered.T @ centered / len(pts)
    eig = np.sort(np.linalg.eigvalsh(cov))[::-1]
    # A uniformly filled ellipse has covariance semi_axis^2 / 4.
    axes = 2 * np.sqrt(np.maximum(eig, 0))
    return {
        "centroid_mm": c.tolist(),
        "equivalent_rms_ellipse_semiaxes_mm": axes.tolist(),
        "axis_ratio": float(axes[0] / axes[1]) if axes[1] else math.inf,
        "equivalent_area_mm2": float(np.pi * axes[0] * axes[1]),
        "max_radius_from_axis_mm": float(np.max(np.hypot(x, y))),
    }


def trace_field(model, indices, channel, field, wavelength, nrings=48, naz=96):
    label, hx, hy = field
    px, py = disk_sample(nrings, naz)
    rays = model.ray_tracer.trace_generic(np.full(px.size, hx), np.full(px.size, hy), px, py, wavelength)
    intensity = np.asarray(model.surfaces.intensity)
    sx, sy = np.asarray(model.surfaces.x), np.asarray(model.surfaces.y)
    split_i = indices["split"]
    split_valid = np.isfinite(sx[split_i]) & np.isfinite(sy[split_i]) & (intensity[split_i] > 0)
    valid = np.isfinite(np.asarray(rays.x)) & np.isfinite(np.asarray(rays.y)) & (np.asarray(rays.i) > 0)
    out = {
        "field": label,
        "normalized_field": [hx, hy],
        "wavelength_um": wavelength,
        "split_survival": float(split_valid.mean()),
        "image_survival": float(valid.mean()),
        "split_pupil": ellipse_metrics(sx[split_i, split_valid], sy[split_i, split_valid]),
    }
    if valid.any():
        pts = np.column_stack([np.asarray(rays.x)[valid], np.asarray(rays.y)[valid]])
        centroid = pts.mean(axis=0)
        out["image_centroid_mm"] = centroid.tolist()
        out["image_rms_radius_um"] = float(np.sqrt(np.mean(np.sum((pts - centroid) ** 2, axis=1))) * 1000)
        out["image_r80_radius_um"] = float(np.quantile(np.hypot(*(pts - centroid).T), 0.8) * 1000)
    return out


def paraxial_pupil(model):
    values = {}
    for key, fn in (
        ("entrance_pupil_location_mm", model.paraxial.entrance_pupil_z),
        ("entrance_pupil_diameter_mm", model.paraxial.EPD),
        ("exit_pupil_location_mm", model.paraxial.XPL),
        ("exit_pupil_diameter_mm", model.paraxial.XPD),
        ("effective_focal_length_mm", model.paraxial.f2),
    ):
        try:
            values[key] = scalar(fn())
        except (AttributeError, ValueError, ZeroDivisionError, FloatingPointError):
            values[key] = None
    return values


def diffraction(model, channel, field, wavelength, n=128, pad=4):
    label, hx, hy = field
    psf = ScalarFFTPSF(model, (hx, hy), wavelength, num_rays=n, grid_size=pad * n,
                       strategy="centroid_sphere", remove_tilt=False, robust_trim_std=0)
    data = psf.get_data((hx, hy), wavelength)
    phase = np.asarray(data.opd)
    amp = np.sqrt(np.asarray(data.intensity))
    mask = (amp > 0) & np.isfinite(phase)
    axis = np.linspace(-1, 1, n)
    xx, yy = np.meshgrid(axis, axis)
    disk = xx * xx + yy * yy <= 1
    pupil = np.zeros((n, n), complex)
    values = np.zeros_like(phase, complex)
    values[mask] = amp[mask] * np.exp(-2j * np.pi * phase[mask])
    pupil[disk] = values
    efl = channel["efl_mm"]
    diameter = channel["pupil_mm"]
    step = wavelength * 0.001 * efl / diameter * (n - 1) / (n * pad)
    size = n * pad
    mid = size // 2
    freq = np.fft.fftshift(np.fft.fftfreq(size, d=step))
    coords = (np.arange(size) - mid) * step
    frequencies = [25.0, 50.0] if channel["name"] == "SWIR" else [50.0, 100.0, 150.0, 182.482]

    def metrics(p):
        image = abs(np.fft.fftshift(np.fft.fft2(p, s=(size, size)))) ** 2
        image /= image.sum()
        otf = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(image)))
        otf /= otf[mid, mid]
        ee = []
        for pixels in (1, 2, 3):
            half = pixels * channel["pixel_pitch_mm"] / 2
            weights = np.maximum(0, np.minimum(coords + step / 2, half) - np.maximum(coords - step / 2, -half)) / step
            ee.append(float(weights @ image @ weights))
        return {
            "mtf_frequencies_lpmm": frequencies,
            "mtf_x": np.interp(frequencies, freq[mid:], abs(otf[mid, mid:])).tolist(),
            "mtf_y": np.interp(frequencies, freq[mid:], abs(otf[mid:, mid])).tolist(),
            "ensquared_energy_1_2_3_pixels": ee,
        }

    return {
        "field": label, "wavelength_um": wavelength, "pupil_grid": n,
        "transmitted_grid_fraction": float(mask.sum() / disk.sum()),
        "opd_rms_waves": float(np.std(phase[mask])) if mask.any() else None,
        "actual": metrics(pupil),
        "matched_obscured_pupil_limit": metrics(abs(pupil)),
    }


def evaluate_ideal(channel, diffraction_n=128):
    model, indices = build_ideal(channel)
    rows = []
    for field in fields(channel):
        for wavelength in channel["wavelengths_um"]:
            rows.append(trace_field(model, indices, channel, field, wavelength))
    # Three field positions at centre wavelength show full-field consequences cheaply.
    diff_fields = [fields(channel)[0], fields(channel)[1], fields(channel)[5]]
    diffs = [diffraction(model, channel, field, channel["wavelengths_um"][1], diffraction_n) for field in diff_fields]
    center = next(r for r in rows if r["field"] == "center" and r["wavelength_um"] == channel["wavelengths_um"][1])
    corner = next(r for r in rows if r["field"] == "corner++" and r["wavelength_um"] == channel["wavelengths_um"][1])
    desired_corner_radius = channel["efl_mm"] * math.tan(math.radians(channel["diagonal_half_field_deg"]))
    actual_corner_radius = math.hypot(*corner["image_centroid_mm"])
    return {
        "channel": channel,
        "paraxial": paraxial_pupil(model),
        "rows": rows,
        "diffraction": diffs,
        "summary": {
            "minimum_geometric_survival": min(r["image_survival"] for r in rows),
            "maximum_image_rms_radius_um": max(r["image_rms_radius_um"] for r in rows),
            "center_image_rms_radius_um": center["image_rms_radius_um"],
            "corner_image_rms_radius_um": corner["image_rms_radius_um"],
            "corner_distortion_percent": 100 * (actual_corner_radius / desired_corner_radius - 1),
            "maximum_split_pupil_axis_ratio": max(r["split_pupil"]["axis_ratio"] for r in rows),
            "maximum_split_pupil_centroid_walk_mm": max(math.hypot(*r["split_pupil"]["centroid_mm"]) for r in rows),
            "corner_midwave_opd_rms_waves": diffs[-1]["opd_rms_waves"],
        },
    }


def field_focus_sweep(channel):
    """Best individual field focus: diagnoses Petzval/defocus versus irreducible blur."""
    span = 1.5 if channel["name"] == "EO" else 4.0
    deltas = np.linspace(-span, span, 31)
    selected = [fields(channel)[0], fields(channel)[1], fields(channel)[3], fields(channel)[5]]
    rows = []
    for field in selected:
        samples = []
        for delta in deltas:
            model, indices = build_ideal(channel, focus_delta_mm=float(delta))
            traced = trace_field(model, indices, channel, field, channel["wavelengths_um"][1], 24, 48)
            samples.append((float(delta), traced["image_rms_radius_um"]))
        best_i = int(np.argmin([item[1] for item in samples]))
        rows.append({
            "field": field[0],
            "best_focus_shift_mm": samples[best_i][0],
            "best_focus_rms_radius_um": samples[best_i][1],
            "nominal_focus_rms_radius_um": samples[len(samples)//2][1],
            "focus_scan_span_mm": [-span, span],
        })
    return rows


def compare_diffraction_sampling(low, high):
    errors = []
    for key in ("mtf_x", "mtf_y", "ensquared_energy_1_2_3_pixels"):
        a = np.asarray(low["actual"][key]); b = np.asarray(high["actual"][key])
        errors.append(float(np.max(np.abs(a - b))))
        a = np.asarray(low["matched_obscured_pupil_limit"][key]); b = np.asarray(high["matched_obscured_pupil_limit"][key])
        errors.append(float(np.max(np.abs(a - b))))
    return max(errors)


def pupil_control_probe(channel):
    """One ideal three-power diagnostic; no search and no physical claim."""
    rows = []
    for fextra in (-200.0, 200.0):
        model, indices = build_ideal(channel, pupil_lens_f_mm=fextra)
        corner = trace_field(model, indices, channel, fields(channel)[5], channel["wavelengths_um"][1], 32, 64)
        rows.append({
            "extra_power_focal_length_mm": fextra,
            "paraxial": paraxial_pupil(model),
            "corner_survival": corner["image_survival"],
            "corner_rms_um": corner.get("image_rms_radius_um"),
            "interpretation": "ideal degree-of-freedom probe only; not a candidate prescription",
        })
    return rows


def real_trace(model, channel, field, wavelength, nrings=8, naz=16):
    px, py = disk_sample(nrings, naz)
    _, hx, hy = field
    rays = model.ray_tracer.trace_generic(np.full(px.size, hx), np.full(px.size, hy), px, py, wavelength)
    points = np.column_stack([np.asarray(rays.x), np.asarray(rays.y)])
    valid = np.isfinite(points).all(axis=1) & (np.asarray(rays.i) > 0)
    return points, valid


def real_backend_metrics(channel, x, nrings=16, naz=32):
    model, indices = build_real_doublet(channel, x)
    rows = []
    for field in fields(channel):
        traced = [real_trace(model, channel, field, wavelength, nrings, naz)
                  for wavelength in channel["wavelengths_um"]]
        valid_points = [points[valid] for points, valid in traced if valid.any()]
        if not valid_points:
            rows.append({"field": field[0], "rms_radius_um_by_wavelength": [None] * 3,
                         "survival_by_wavelength": [0.0] * 3})
            continue
        centroid = np.concatenate(valid_points).mean(axis=0)
        rms = [float(np.sqrt(np.mean(np.sum((points[valid] - centroid) ** 2, axis=1))) * 1000)
               if valid.any() else None for points, valid in traced]
        rows.append({"field": field[0], "centroid_mm": centroid.tolist(),
                     "rms_radius_um_by_wavelength": rms,
                     "survival_by_wavelength": [float(valid.mean()) for _, valid in traced]})
    efl = abs(scalar(model.paraxial.f2()))
    return {
        "parameters": list(map(float, x)),
        "parameter_names": ["c1_per_mm", "c2_per_mm", "c3_per_mm", "c4_per_mm", "air_gap_mm", "image_distance_mm"],
        "materials": ["N-BK7", "N-F2"] if channel["name"] == "EO" else ["fused_silica", "LITHOTEC-CAF2"],
        "paraxial": paraxial_pupil(model),
        "effective_focal_length_mm": efl,
        "f_number_from_entrance_pupil": efl / channel["pupil_mm"],
        "rows": rows,
        "worst_rms_radius_um": max(value for row in rows for value in row["rms_radius_um_by_wavelength"] if value is not None),
        "minimum_survival": min(value for row in rows for value in row["survival_by_wavelength"]),
    }


def real_backend_merit(x, channel):
    try:
        model, _ = build_real_doublet(channel, x)
        values = []
        sample_fields = [fields(channel)[0], fields(channel)[1], fields(channel)[3], fields(channel)[5]]
        for field in sample_fields:
            traced = [real_trace(model, channel, field, wavelength, 5, 10)
                      for wavelength in channel["wavelengths_um"]]
            valid_all = [points[valid] for points, valid in traced if valid.any()]
            if not valid_all:
                values.extend([100.0] * (len(traced) * 5 * 10 * 2)); continue
            centroid = np.concatenate(valid_all).mean(axis=0)
            scale = channel["pixel_pitch_mm"]
            for points, valid in traced:
                residual = np.full_like(points, 30.0)
                residual[valid] = (points[valid] - centroid) / scale
                values.extend(residual.ravel())
        values.append((abs(scalar(model.paraxial.f2())) - channel["efl_mm"]) / 0.2)
        values.append(max(0.0, 0.65 - real_backend_metrics(channel, x, 4, 8)["minimum_survival"]) * 100)
        return np.nan_to_num(values, nan=1e4, posinf=1e4, neginf=-1e4)
    except (ValueError, FloatingPointError, RuntimeError, ZeroDivisionError):
        return np.full(4 * 3 * 5 * 10 * 2 + 2, 1e4)


def solve_real_backend(channel, max_nfev=120):
    f = channel["efl_mm"] / GEOMETRY["compression"]
    base_c = 1 / (2 * 0.52 * f)
    seed = np.array([1.5*base_c, -0.7*base_c, -0.5*base_c, 0.25*base_c,
                     2.0 if channel["name"] == "EO" else 3.0, f])
    cmax = 0.05 if channel["name"] == "EO" else 0.025
    lower = [-cmax] * 4 + [0.5, 0.55*f]
    upper = [cmax] * 4 + [20.0, 1.45*f]
    initial = real_backend_metrics(channel, seed, 8, 16)
    fit = least_squares(real_backend_merit, seed, args=(channel,), bounds=(lower, upper),
                        x_scale="jac", max_nfev=max_nfev, ftol=2e-6, xtol=2e-7, gtol=2e-6,
                        verbose=0)
    final = real_backend_metrics(channel, fit.x, 20, 40)
    model, _ = build_real_doublet(channel, fit.x)
    write_prescription(OUT / f"real_doublet_{channel['name'].lower()}_prescription.csv", model)
    return {"channel": channel["name"], "model": "two air-spaced spherical elements",
            "initial": initial, "final": final, "nfev": fit.nfev,
            "optimizer_success": bool(fit.success), "optimizer_message": fit.message,
            "attempt_interpretation": "bounded minimum-complexity feasibility attempt, not a converged production prescription"}


def write_prescription(path, model):
    rows = []
    for i, surface in enumerate(model.surfaces.surfaces):
        geom = surface.geometry
        interaction = surface.interaction_model
        rows.append({
            "surface": i, "comment": surface.comment or "",
            "geometry": type(geom).__name__,
            "radius_mm": scalar(geom.radius) if hasattr(geom, "radius") else "",
            "conic": scalar(geom.k) if hasattr(geom, "k") else "",
            "thickness_mm": scalar(surface.thickness) if np.isfinite(scalar(surface.thickness)) else "infinity",
            "interaction": type(interaction).__name__,
            "ideal_focal_length_mm": scalar(interaction.f) if hasattr(interaction, "f") else "",
            "material_post": str(surface.material_post),
            "is_stop": surface.is_stop,
        })
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)


def plot_results(results):
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for row, color in zip(results, ("#2166ac", "#b2182b")):
        channel = row["channel"]["name"]
        mids = [r for r in row["rows"] if r["wavelength_um"] == row["channel"]["wavelengths_um"][1]]
        x = np.arange(len(mids))
        axes[0, 0].plot(x, [100*r["image_survival"] for r in mids], "o-", color=color, label=channel)
        axes[0, 1].plot(x, [r["image_rms_radius_um"] for r in mids], "o-", color=color, label=channel)
        axes[1, 0].plot(x, [r["split_pupil"]["axis_ratio"] for r in mids], "o-", color=color, label=channel)
        axes[1, 1].plot(x, [math.hypot(*r["split_pupil"]["centroid_mm"]) for r in mids], "o-", color=color, label=channel)
    labels = [f[0] for f in fields(results[0]["channel"])]
    for ax in axes.ravel():
        ax.set_xticks(np.arange(len(labels)), labels, rotation=35, ha="right"); ax.grid(True, alpha=.25); ax.legend()
    axes[0, 0].set_ylabel("Geometric transmission (%)")
    axes[0, 1].set_ylabel("Ideal-backend RMS radius (um)")
    axes[1, 0].set_ylabel("Split-pupil RMS ellipse axis ratio")
    axes[1, 1].set_ylabel("Split-pupil centroid walk (mm)")
    fig.suptitle("Run 016 — A6_f1p0 common-front evidence with perfect channel cameras")
    fig.tight_layout(); fig.savefig(OUT / "ideal_backend_full_field.png", dpi=180); plt.close(fig)


def save_json(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--real-backend", action="store_true")
    parser.add_argument("--diffraction-grid", type=int, default=128)
    args = parser.parse_args()
    req = yaml.safe_load(REQ_PATH.read_text(encoding="utf-8"))
    channels = [channel_data(req, "eo"), channel_data(req, "swir")]
    if args.real_backend:
        if not OUT.exists():
            raise RuntimeError("Run 016 ideal-front evidence must exist before the conditional real-backend attempt")
        start = time.perf_counter()
        attempts = [solve_real_backend(ch) for ch in channels]
        save_json("real_backend_attempts.json", {"attempts": attempts, "wall_seconds": time.perf_counter() - start})
        shutil.copy2(__file__, OUT / "track_c_run016_c02.py")
        print(json.dumps({a["channel"]: {"initial_worst_um": a["initial"]["worst_rms_radius_um"],
                                             "final_worst_um": a["final"]["worst_rms_radius_um"],
                                             "final_efl_mm": a["final"]["effective_focal_length_mm"],
                                             "minimum_survival": a["final"]["minimum_survival"],
                                             "nfev": a["nfev"]} for a in attempts}, indent=2))
        return
    if args.probe:
        for ch in channels:
            model, indices = build_ideal(ch)
            print(ch["name"], paraxial_pupil(model), trace_field(model, indices, ch, fields(ch)[5], ch["wavelengths_um"][1], 12, 24))
        return
    OUT.mkdir(parents=True, exist_ok=False)
    start = datetime.now(timezone.utc); tick = time.perf_counter()
    results = [evaluate_ideal(ch, args.diffraction_grid) for ch in channels]
    for result, channel in zip(results, channels):
        result["field_focus_sweep"] = field_focus_sweep(channel)
        result["summary"]["corner_best_focus_shift_mm"] = result["field_focus_sweep"][-1]["best_focus_shift_mm"]
        result["summary"]["corner_best_focus_rms_radius_um"] = result["field_focus_sweep"][-1]["best_focus_rms_radius_um"]
    # The only extra-power comparison is intentionally paraxial/ideal and EO-only.
    extra = pupil_control_probe(channels[0])
    save_json("metrics.json", {"geometry": GEOMETRY, "apertures": APERTURES, "ideal_backend_results": results,
                               "three_power_pupil_control_probe": extra})
    convergence = []
    for result, channel in zip(results, channels):
        high = diffraction(build_ideal(channel)[0], channel, fields(channel)[5], channel["wavelengths_um"][1], 160)
        low = result["diffraction"][-1]
        convergence.append({"channel": channel["name"], "baseline_grid": args.diffraction_grid,
                            "replay_grid": 160, "max_mtf_or_ee_change": compare_diffraction_sampling(low, high),
                            "replay": high})
    save_json("convergence.json", {"purpose": "independent denser corner diffraction replay", "rows": convergence,
                                   "decision_stability": "evaluated in summary after numerical review"})
    plot_results(results)
    model, _ = build_ideal(channels[0]); write_prescription(OUT / "prescription.csv", model)
    shutil.copy2(REQ_PATH, OUT / "requirements.yaml")
    shutil.copy2(__file__, OUT / "track_c_run016_c02.py")
    save_json("dependencies.json", {"python": sys.version, "platform": platform.platform(), "optiland": optiland.__version__,
                                    "numpy": np.__version__})
    metadata = {
        "track": "C", "run_id": "016", "candidate_ids": ["C02"], "parent_run": "run_015",
        "purpose": "test whether A6_f1p0 common-front image, pupil and diffraction evidence justifies realistic backend development",
        "development_stage": "C1 low-cost numerical architecture screening",
        "start_time_utc": start.isoformat(), "end_time_utc": datetime.now(timezone.utc).isoformat(),
        "script_wall_seconds": time.perf_counter() - tick,
        "substantial_computational_search_count": 2,
        "searches": ["full-field two-channel perfect-backend common-front trace and diffraction evaluation",
                     "bounded per-field best-focus sweep separating field curvature from residual aberration"],
        "materially_distinct_physical_model_experiments": 1,
        "optimization_attempt_count": 0, "plateau_counter": 0,
        "human_interventions": ["User supplied targeted Mersenne field/pupil literature findings and requested the ideal-backend falsification gate."],
        "contamination_control": "reference/ not accessed",
    }
    save_json("metadata.json", metadata)
    print(json.dumps({r["channel"]["name"]: r["summary"] for r in results}, indent=2), flush=True)


if __name__ == "__main__":
    main()
