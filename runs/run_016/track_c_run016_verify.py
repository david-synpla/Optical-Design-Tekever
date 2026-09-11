#!/usr/bin/env python3
"""Independent Run 016 best-curved-focus diffraction replay."""

from __future__ import annotations

import json
import math
import hashlib
from pathlib import Path

import numpy as np

import track_c_run016_c02 as run


def pupil_metrics(pupil, channel, wavelength, n, pad=4):
    size = n * pad; mid = size // 2
    fcam = channel["efl_mm"] / run.GEOMETRY["compression"]
    beam = channel["pupil_mm"] / run.GEOMETRY["compression"]
    step = wavelength * .001 * fcam / beam * (n - 1) / (n * pad)
    freq = np.fft.fftshift(np.fft.fftfreq(size, d=step))
    coords = (np.arange(size) - mid) * step
    frequencies = [25., 50.] if channel["name"] == "SWIR" else [50., 100., 150., 182.482]
    image = abs(np.fft.fftshift(np.fft.fft2(pupil, s=(size, size)))) ** 2
    image /= image.sum()
    otf = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(image))); otf /= otf[mid, mid]
    ee = []
    for pixels in (1, 2, 3):
        half = pixels * channel["pixel_pitch_mm"] / 2
        weights = np.maximum(0, np.minimum(coords + step/2, half) - np.maximum(coords - step/2, -half)) / step
        ee.append(float(weights @ image @ weights))
    return {"mtf_frequencies_lpmm": frequencies,
            "mtf_x": np.interp(frequencies, freq[mid:], abs(otf[mid, mid:])).tolist(),
            "mtf_y": np.interp(frequencies, freq[mid:], abs(otf[mid:, mid])).tolist(),
            "ensquared_energy_1_2_3_pixels": ee}


def forward_split_pupil(channel, field, wavelength, n=160):
    """Forward OPD at the real split stop; avoids backward reflective-stop ambiguity."""
    model, indices = run.build_ideal(channel)
    axis = np.linspace(-.999, .999, n); xx, yy = np.meshgrid(axis, axis)
    disk = xx*xx + yy*yy <= 1
    px, py = xx[disk], yy[disk]
    _, hx, hy = field
    model.ray_tracer.trace_generic(np.full(px.size, hx), np.full(px.size, hy), px, py, wavelength)
    i = indices["split"]
    intensity = np.asarray(model.surfaces.intensity)[i]
    sx, sy = np.asarray(model.surfaces.x)[i], np.asarray(model.surfaces.y)[i]
    opd = np.asarray(model.surfaces.opd)[i]
    valid = np.isfinite(opd) & np.isfinite(sx) & np.isfinite(sy) & (intensity > 0)
    x, y, w = sx[valid], sy[valid], opd[valid]
    plane = np.column_stack([np.ones_like(x), x, y])
    quad = np.column_stack([np.ones_like(x), x, y, x*x+y*y])
    plane_res = w - plane @ np.linalg.lstsq(plane, w, rcond=None)[0]
    quad_fit = np.linalg.lstsq(quad, w, rcond=None)[0]
    quad_res = w - quad @ quad_fit
    wavelength_mm = wavelength * .001
    def make_pupil(residual):
        values = np.zeros(px.size, complex)
        values[valid] = np.sqrt(intensity[valid]) * np.exp(-2j*np.pi*residual/wavelength_mm)
        pupil = np.zeros((n, n), complex); pupil[disk] = values
        return pupil
    plane_pupil = make_pupil(plane_res); best_pupil = make_pupil(quad_res)
    amplitude = abs(plane_pupil)
    return {
        "field": field[0], "wavelength_um": wavelength, "pupil_grid": n,
        "geometric_transmission_fraction": float(valid.sum()/disk.sum()),
        "plane_reference_opd_rms_waves": float(np.std(plane_res)/wavelength_mm),
        "best_defocus_removed_opd_rms_waves": float(np.std(quad_res)/wavelength_mm),
        "fitted_radial_opd_coefficient_per_mm": float(quad_fit[-1]),
        "flat_detector": pupil_metrics(plane_pupil, channel, wavelength, n),
        "best_curved_focus": pupil_metrics(best_pupil, channel, wavelength, n),
        "matched_obscured_pupil_limit": pupil_metrics(amplitude, channel, wavelength, n),
        "method": "forward cumulative OPD at physical split stop; piston/tilt removed, then radial quadratic removed for curved-focus diagnostic",
    }


def main():
    requirements = run.yaml.safe_load(run.REQ_PATH.read_text(encoding="utf-8"))
    metrics = json.loads((run.OUT / "metrics.json").read_text(encoding="utf-8"))
    rows = []
    for name, result in zip(("eo", "swir"), metrics["ideal_backend_results"]):
        channel = run.channel_data(requirements, name)
        shift = result["field_focus_sweep"][-1]["best_focus_shift_mm"]
        low = forward_split_pupil(channel, run.fields(channel)[5], channel["wavelengths_um"][1], 128)
        high = forward_split_pupil(channel, run.fields(channel)[5], channel["wavelengths_um"][1], 160)
        error = 0.0
        for section in ("flat_detector", "best_curved_focus", "matched_obscured_pupil_limit"):
            for key in ("mtf_x", "mtf_y", "ensquared_energy_1_2_3_pixels"):
                error = max(error, float(np.max(np.abs(np.asarray(low[section][key])-np.asarray(high[section][key])))))
        rows.append({
            "channel": channel["name"],
            "individual_corner_best_focus_shift_mm": shift,
            "baseline": low,
            "dense_replay": high,
            "max_mtf_or_ee_change": error,
            "scope": "common-front wavefront at the actual split stop; best-curved-focus result is diagnostic, not a realizable flat detector",
        })
    run.save_json("diffraction_audit.json", {
        "status": "authoritative Run 016 diffraction result; supersedes preliminary ScalarFFTPSF entries embedded in metrics.json and convergence.json",
        "reason": "forward cumulative OPD is sampled directly at the real split stop; this avoids backward reflective-stop ambiguity and retains the correct remote-pupil ray aiming",
        "rows": rows,
    })
    run.shutil.copy2(__file__, run.OUT / "track_c_run016_verify.py")
    files = sorted(path for path in run.OUT.rglob("*") if path.is_file() and path.name != "SHA256SUMS.txt")
    (run.OUT / "SHA256SUMS.txt").write_text(
        "".join(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(run.OUT).as_posix()}\n" for path in files),
        encoding="utf-8",
    )
    print(json.dumps({r["channel"]: {"flat_opd_rms_waves": r["dense_replay"]["plane_reference_opd_rms_waves"],
                                             "best_opd_rms_waves": r["dense_replay"]["best_defocus_removed_opd_rms_waves"],
                                             "mtf_x": r["dense_replay"]["best_curved_focus"]["mtf_x"],
                                             "mtf_y": r["dense_replay"]["best_curved_focus"]["mtf_y"],
                                             "sampling_change": r["max_mtf_or_ee_change"]} for r in rows}, indent=2))


if __name__ == "__main__":
    main()
