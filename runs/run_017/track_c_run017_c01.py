#!/usr/bin/env python3
"""Run 017: bounded C01 separate-telescope optical and package comparator.

B05-1 is replayed unchanged as historical EO evidence.  Three fresh SWIR
two-mirror seeds expose the primary-speed/length/obscuration trade; only their
two conic constants and a small detector-focus compensation are solved.
Package and mass quantities are continuous engineering proxies, not limits.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
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
import scipy
import yaml
from optiland import optic
from optiland.physical_apertures import RadialAperture
from optiland.psf import ScalarFFTPSF
from scipy.optimize import least_squares, minimize_scalar


ROOT = next(p for p in Path(__file__).resolve().parents if (p / "WORK_GUIDE.md").exists())
OUT = ROOT / "runs" / "run_017"
REQ = ROOT / "requirements" / "eo_swir_system_requirements.yaml"
B05_MODEL = ROOT / "runs" / "run_008" / "model.py"
B05_CONFIG = ROOT / "runs" / "run_008" / "configuration.json"
RUN016_SWAP = ROOT / "runs" / "run_016" / "swap_screen.json"
MARGIN = 1.0


def scalar(v):
    return float(np.asarray(v).reshape(-1)[0])


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def channel(req, name):
    r = req["source_explicit_requirements"][name]
    pitch = r["pixel_pitch_um"][0] / 1000
    efl = pitch / (r["instantaneous_fov_urad_per_pixel"] * 1e-6)
    pupil = efl / r["f_number"]
    hx = math.degrees(math.atan(r["array_px"][0] * pitch / (2 * efl)))
    hy = math.degrees(math.atan(r["array_px"][1] * pitch / (2 * efl)))
    diag = math.hypot(hx, hy)
    return {"name": name.upper(), "efl_mm": efl, "pupil_mm": pupil,
            "half_x_deg": hx, "half_y_deg": hy, "diag_deg": diag,
            "hx": hx / diag, "hy": hy / diag,
            "waves_um": [0.43, 0.55, 0.80] if name == "eo" else [0.80, 1.20, 1.80]}


def fields(ch):
    x, y = ch["hx"], ch["hy"]
    return [("center", 0, 0), ("+x", x, 0), ("-x", -x, 0),
            ("+y", 0, y), ("-y", 0, -y), ("corner++", x, y),
            ("corner+-", x, -y), ("corner-+", -x, y), ("corner--", -x, -y)]


def pupil(nr=18, na=48, inner=0.0):
    r = np.sqrt(np.linspace(inner * inner + 0.5 * (1-inner*inner)/nr,
                            1 - 0.5 * (1-inner*inner)/nr, nr)) * 0.998
    t = 2 * np.pi * (np.arange(na) + .5) / na
    return (r[:, None] * np.cos(t)).ravel(), (r[:, None] * np.sin(t)).ravel()


def swir_geometry(name, ch, speed, backfocus):
    f1 = speed * ch["pupil_mm"]
    mag = ch["efl_mm"] / f1
    sep = (ch["efl_mm"] - backfocus) / (mag + 1)
    q = f1 - sep
    r2 = -2 * q * (sep + backfocus) / (sep + backfocus - q)
    return {"name": name, "primary_speed": speed, "backfocus_mm": backfocus,
            "primary_focal_mm": f1, "secondary_magnification": mag,
            "mirror_separation_mm": sep, "primary_radius_mm": -2*f1,
            "classical_primary_conic": -1.0, "secondary_radius_mm": r2,
            "classical_secondary_conic": -((mag+1)/(mag-1))**2}


def set_channel(o, ch):
    o.set_aperture(aperture_type="EPD", value=ch["pupil_mm"])
    o.fields.set_type("angle")
    o.fields.add(y=0); o.fields.add(y=ch["diag_deg"])
    for w in ch["waves_um"]:
        o.wavelengths.add(value=w, is_primary=w == ch["waves_um"][1])


def build_swir(g, ch, x=None, aps=None, finite=False, fold_probe_fraction=None):
    k1, k2, focus = (g["classical_primary_conic"], g["classical_secondary_conic"], 0.0) if x is None else x
    pr = 1000 if aps is None else aps["primary_radius_mm"]
    sr = 1000 if aps is None else aps["secondary_radius_mm"]
    hr = 1000 if aps is None else aps["hole_radius_mm"]
    sep, b = g["mirror_separation_mm"], g["backfocus_mm"]
    o = optic.Optic(name=f"Run 017 C01 independent SWIR {g['name']}")
    o.surfaces.add(index=0, thickness=800000 if finite else np.inf)
    o.surfaces.add(index=1, thickness=sep+3, is_stop=True,
                   aperture=RadialAperture(pr, sr if aps else 0))
    o.surfaces.add(index=2, radius=g["primary_radius_mm"], thickness=-sep,
                   conic=k1, material="mirror", aperture=RadialAperture(pr, hr if aps else 0))
    o.surfaces.add(index=3, radius=g["secondary_radius_mm"], thickness=sep,
                   conic=k2, material="mirror", aperture=RadialAperture(sr))
    if fold_probe_fraction is None:
        o.surfaces.add(index=4, thickness=b+focus, aperture=RadialAperture(hr))
        o.surfaces.add(index=5)
        ind = {"entrance": 1, "primary": 2, "secondary": 3, "hole": 4, "image": 5}
    else:
        z = b * fold_probe_fraction
        o.surfaces.add(index=4, thickness=z, aperture=RadialAperture(hr))
        o.surfaces.add(index=5, thickness=b-z+focus)
        o.surfaces.add(index=6)
        ind = {"entrance": 1, "primary": 2, "secondary": 3, "hole": 4,
               "fold_probe": 5, "image": 6}
    set_channel(o, ch)
    return o, ind


def trace(o, ind, ch, fld, wave, nr=18, na=48, inner=0):
    px, py = pupil(nr, na, inner)
    _, hx, hy = fld
    rays = o.ray_tracer.trace_generic(np.full(px.size, hx), np.full(px.size, hy), px, py, wave)
    xx, yy, ii = map(np.asarray, (o.surfaces.x, o.surfaces.y, o.surfaces.intensity))
    final = np.isfinite(np.asarray(rays.x)) & np.isfinite(np.asarray(rays.y)) & (np.asarray(rays.i) > 0)
    result = {"field": fld[0], "wavelength_um": wave, "survival": float(np.mean(final)), "surfaces": {}}
    for name, idx in ind.items():
        ok = np.isfinite(xx[idx]) & np.isfinite(yy[idx]) & (ii[idx] > 0)
        rr = np.hypot(xx[idx, ok], yy[idx, ok]) if np.any(ok) else np.array([])
        result["surfaces"][name] = {"max_radius_mm": float(np.max(rr)) if rr.size else None,
                                     "valid_fraction": float(np.mean(ok))}
    if np.any(final):
        p = np.column_stack((np.asarray(rays.x)[final], np.asarray(rays.y)[final]))
        c = p.mean(axis=0)
        result["centroid_mm"] = c.tolist()
        result["rms_radius_um"] = float(np.sqrt(np.mean(np.sum((p-c)**2, axis=1))) * 1000)
    else:
        result["centroid_mm"] = [None, None]; result["rms_radius_um"] = None
    return result


def size_apertures(g, ch):
    o, ind = build_swir(g, ch)
    maxima = {"primary": ch["pupil_mm"] / 2, "secondary": 0, "hole": 0}
    for fld in fields(ch):
        row = trace(o, ind, ch, fld, ch["waves_um"][1], 14, 40)
        for key in maxima:
            maxima[key] = max(maxima[key], row["surfaces"][key]["max_radius_mm"])
    return {"primary_radius_mm": maxima["primary"] + MARGIN,
            "secondary_radius_mm": maxima["secondary"] + MARGIN,
            "hole_radius_mm": maxima["hole"] + MARGIN,
            "radial_margin_mm": MARGIN}


def merit(x, g, ch, aps):
    try:
        o, ind = build_swir(g, ch, x, aps)
        vals = []
        inner = aps["secondary_radius_mm"] / (ch["pupil_mm"] / 2)
        px, py = pupil(7, 24, inner)
        for fld in (fields(ch)[0], fields(ch)[1], fields(ch)[3], fields(ch)[5]):
            _, hx, hy = fld
            rays = o.ray_tracer.trace_generic(np.full(px.size,hx),np.full(px.size,hy),px,py,ch["waves_um"][1])
            ok = np.isfinite(np.asarray(rays.x)) & np.isfinite(np.asarray(rays.y)) & (np.asarray(rays.i)>0)
            points = np.column_stack((np.asarray(rays.x),np.asarray(rays.y)))
            residual = np.full_like(points, 30.0)
            if np.any(ok): residual[ok] = (points[ok]-points[ok].mean(axis=0))/.003
            vals.extend(np.nan_to_num(residual,nan=30,posinf=30,neginf=-30).ravel())
        vals.extend([(x[0]-g["classical_primary_conic"])/1.5,
                     (x[1]-g["classical_secondary_conic"])/5.0, x[2]/2.0])
        return np.nan_to_num(vals, nan=1e4, posinf=1e4, neginf=-1e4)
    except Exception:
        return np.full(4 * 7 * 24 * 2 + 3, 1e4)


def evaluate(g, ch, aps, x, nr=20, na=56):
    o, ind = build_swir(g, ch, x, aps)
    rows = [trace(o, ind, ch, fld, w, nr, na, 0.0) for fld in fields(ch) for w in ch["waves_um"]]
    good = [r for r in rows if r["rms_radius_um"] is not None]
    return {"geometry": g, "apertures": aps, "solution": {"primary_conic": float(x[0]),
            "secondary_conic": float(x[1]), "detector_focus_mm": float(x[2])},
            "effective_focal_length_mm": abs(scalar(o.paraxial.f2())),
            "f_number": abs(scalar(o.paraxial.f2())) / ch["pupil_mm"],
            "minimum_survival": min(r["survival"] for r in rows),
            "center_survival": min(r["survival"] for r in rows if r["field"] == "center"),
            "worst_rms_radius_um": max(r["rms_radius_um"] for r in good),
            "median_rms_radius_um": float(np.median([r["rms_radius_um"] for r in good])),
            "rows": rows}


def solve_seed(g, ch, max_nfev=55):
    aps = size_apertures(g, ch)
    seed = np.array([g["classical_primary_conic"], g["classical_secondary_conic"], 0.0])
    initial = evaluate(g, ch, aps, seed, 12, 32)
    fit = least_squares(merit, seed, args=(g, ch, aps),
                        bounds=([-5, -30, -5], [0, 0, 5]), x_scale="jac",
                        max_nfev=max_nfev, ftol=2e-7, xtol=2e-7, gtol=2e-7)
    final = evaluate(g, ch, aps, fit.x)
    final.update({"initial_worst_rms_radius_um": initial["worst_rms_radius_um"],
                  "optimizer_nfev": int(fit.nfev), "optimizer_success": bool(fit.success),
                  "optimizer_message": fit.message})
    return final


def finite_focus(row, ch):
    g, aps = row["geometry"], row["apertures"]
    x0 = np.array([row["solution"]["primary_conic"], row["solution"]["secondary_conic"],
                   row["solution"]["detector_focus_mm"]])
    inner = aps["secondary_radius_mm"] / (ch["pupil_mm"] / 2)
    def objective(extra):
        x = x0.copy(); x[2] += extra
        o, ind = build_swir(g, ch, x, aps, finite=True)
        vals = [trace(o, ind, ch, f, ch["waves_um"][1], 10, 32, inner)["rms_radius_um"] for f in fields(ch)]
        return max(v for v in vals if v is not None)
    fit = minimize_scalar(objective, bounds=(-8, 8), method="bounded", options={"xatol": 2e-4})
    return {"object_distance_m": 800, "additional_detector_shift_mm": float(fit.x),
            "worst_monochromatic_rms_radius_um": float(fit.fun), "paraxial_expectation_mm": 4.67}


def diffraction(row, ch, field_index, grid):
    g, aps = row["geometry"], row["apertures"]
    x = [row["solution"]["primary_conic"], row["solution"]["secondary_conic"], row["solution"]["detector_focus_mm"]]
    o, _ = build_swir(g, ch, x, aps)
    fld = (fields(ch)[field_index][1], fields(ch)[field_index][2])
    ps = ScalarFFTPSF(o, fld, ch["waves_um"][1], num_rays=grid, grid_size=grid*4,
                      strategy="centroid_sphere", remove_tilt=False)
    p = np.asarray(ps.pupils[0]); actual = np.asarray(ps.psf, dtype=float); actual /= actual.sum()
    ideal = abs(np.fft.fftshift(np.fft.fft2(abs(p), s=actual.shape)))**2; ideal /= ideal.sum()
    extent = ps._get_psf_units(actual); dx = float(extent[0]) / actual.shape[1] / 1000
    nu = np.fft.fftshift(np.fft.fftfreq(actual.shape[0], d=dx)); mid = len(nu)//2
    def m(im):
        otf = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(im))); otf /= otf[mid, mid]
        return {str(f): float(np.interp(f, nu[mid:], abs(otf[mid, mid:]))) for f in (25, 50)}
    return {"field": fields(ch)[field_index][0], "wavelength_um": ch["waves_um"][1],
            "grid": grid, "actual_mtf_x": m(actual), "matched_pupil_mtf_x": m(ideal),
            "relative_peak": float(actual.max()/ideal.max())}


def load_b05(req_eo):
    spec = importlib.util.spec_from_file_location("run008_b05", B05_MODEL)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    cfg = json.loads(B05_CONFIG.read_text())["best"]
    assert abs(module.F - req_eo["efl_mm"]) < .01 and abs(module.D - req_eo["pupil_mm"]) < .01
    geo = module.geometric(np.array(cfg))
    model = module.build(np.array(cfg))
    surfaces = []
    for i, s in enumerate(model.surfaces.surfaces):
        geom = s.geometry
        radius = scalar(geom.radius) if hasattr(geom, "radius") else math.inf
        surfaces.append({"surface": i, "radius_mm": radius if np.isfinite(radius) else None,
                         "conic": scalar(geom.k) if hasattr(geom, "k") else None,
                         "thickness_mm": scalar(s.thickness) if np.isfinite(scalar(s.thickness)) else None,
                         "material_post": str(s.material_post), "is_stop": bool(s.is_stop)})
    return {"source": "unchanged Run 008 B05-1 model/configuration; Run 010 dense evidence retained",
            "configuration": cfg, "fresh_replay": geo,
            "run010_dense_worst_rms_radius_um": 0.800,
            "run013_temperature_endpoint_rms_radius_um": [0.799, 0.801],
            "run013_focus_notes": "about 0.04 mm over -25 to +50 C for the 1.2 ppm/K scenario; up to 1.37 mm for 24 ppm/K; not a transferred requirement",
            "apertures_mm": {k: float(v) for k,v in module.AP.items()}, "surfaces": surfaces}


def mirror_mass(d_outer, d_inner=0, density=2200, t_over_d=.10):
    return math.pi/4 * ((d_outer/1000)**2 - (d_inner/1000)**2) * (t_over_d*d_outer/1000) * density


def build_swap(seed_rows, b05):
    eo_d = 2*b05["apertures_mm"]["primary_outer"]
    eo_ext = eo_d + 20; eo_len = 329.04 + 45
    rows = []
    for s in seed_rows:
        g, a = s["geometry"], s["apertures"]
        sw_d = 2*a["primary_radius_mm"]; sw_ext = sw_d + 24
        straight = g["mirror_separation_mm"] + 3 + g["backfocus_mm"] + 55
        width = eo_ext + sw_ext + 10; height = sw_ext
        # A 90-degree return-fold probe is at 35% of SWIR back focus.  Its
        # converging-beam footprint is traced separately; the remaining path
        # fits behind the much wider two-aperture front face.
        fold_axial = g["mirror_separation_mm"] + 3 + .35*g["backfocus_mm"] + 55
        fold_model, fold_ind = build_swir(g, SWIR, [s["solution"]["primary_conic"], s["solution"]["secondary_conic"], s["solution"]["detector_focus_mm"]], a, fold_probe_fraction=.35)
        fr = trace(fold_model, fold_ind, SWIR, fields(SWIR)[5], SWIR["waves_um"][1], 16, 48,
                   a["secondary_radius_mm"]/(SWIR["pupil_mm"]/2))
        fold_clear = 2*fr["surfaces"]["fold_probe"]["max_radius_mm"]*math.sqrt(2)+4
        solid = mirror_mass(2*a["primary_radius_mm"], 2*a["hole_radius_mm"]) + mirror_mass(2*a["secondary_radius_mm"])
        eo_solid = mirror_mass(2*b05["apertures_mm"]["primary_outer"], 2*b05["apertures_mm"]["hole"]) + mirror_mass(2*b05["apertures_mm"]["secondary"])
        optical_area = math.pi/4*((sw_d/1000)**2+(2*a["secondary_radius_mm"]/1000)**2+(eo_d/1000)**2+(2*b05["apertures_mm"]["secondary"]/1000)**2)
        common = {"seed": g["name"], "external_aperture_max_mm": sw_ext,
                  "front_face_span_mm": width, "centerline_baseline_mm": .5*(eo_ext+sw_ext)+10,
                  "solid_blank_mirror_proxy_kg": solid+eo_solid,
                  "lightweighted_mirror_proxy_kg_range": [15*optical_area, 30*optical_area],
                  "large_optics_over_100_mm": 2, "powered_mirrors": 4,
                  "powered_corrector_lenses": 2, "focus_mechanisms": 2,
                  "shared_structure": "outer payload/gimbal frame and boresight calibration only",
                  "duplicated_structure": "two telescope metering cells, baffles, detector barrels and focus interfaces"}
        for layout, dims, extra in [
            ("side_by_side_recessed_straight", [width, height, max(eo_len, straight)], {"fold_mirror_clear_mm": 0}),
            ("stacked_recessed_straight", [height, width, max(eo_len, straight)], {"fold_mirror_clear_mm": 0}),
            ("side_by_side_SWIR_return_fold", [width, height, max(eo_len, fold_axial)], {"fold_mirror_clear_mm": fold_clear})]:
            r = dict(common); r.update({"layout": layout, "dimensions_mm": dims,
                "volume_l": float(np.prod(dims)/1e6), "maximum_dimension_mm": max(dims), **extra})
            rows.append(r)
    return rows


def write_prescription(path, row, ch):
    g, a = row["geometry"], row["apertures"]
    x = [row["solution"]["primary_conic"], row["solution"]["secondary_conic"], row["solution"]["detector_focus_mm"]]
    o, _ = build_swir(g, ch, x, a)
    fields_out = ["surface", "radius_mm", "conic", "thickness_mm", "material_post", "is_stop"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields_out); w.writeheader()
        for i, s in enumerate(o.surfaces.surfaces):
            geom = s.geometry
            w.writerow({"surface": i, "radius_mm": scalar(geom.radius) if hasattr(geom,"radius") else "",
                        "conic": scalar(geom.k) if hasattr(geom,"k") else "",
                        "thickness_mm": scalar(s.thickness) if np.isfinite(scalar(s.thickness)) else "infinity",
                        "material_post": str(s.material_post), "is_stop": s.is_stop})


def plot(seed_rows, packages):
    fig, ax = plt.subplots(1, 2, figsize=(10,4.5))
    ax[0].scatter([r["geometry"]["mirror_separation_mm"]+r["geometry"]["backfocus_mm"] for r in seed_rows],
                  [r["worst_rms_radius_um"] for r in seed_rows], s=65)
    for r in seed_rows: ax[0].annotate(r["geometry"]["name"], (r["geometry"]["mirror_separation_mm"]+r["geometry"]["backfocus_mm"], r["worst_rms_radius_um"]), xytext=(5,5), textcoords="offset points")
    ax[0].set(xlabel="SWIR optical length proxy (mm)", ylabel="Worst RMS radius (um)")
    folded = [r for r in packages if "return_fold" in r["layout"]]
    ax[1].scatter([r["volume_l"] for r in folded], [r["maximum_dimension_mm"] for r in folded], s=65)
    for r in folded: ax[1].annotate(r["seed"], (r["volume_l"],r["maximum_dimension_mm"]), xytext=(5,5), textcoords="offset points")
    ax[1].axvline(63.39, color="gray", ls="--", label="Run 016 C02 straight lower bound")
    ax[1].set(xlabel="C01 bounding-box proxy (L)", ylabel="Maximum box dimension (mm)")
    for a in ax: a.grid(alpha=.25)
    ax[1].legend(fontsize=8); fig.tight_layout(); fig.savefig(OUT/"c01_optical_package_pareto.png", dpi=180); plt.close(fig)


def save(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2, allow_nan=False)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--probe", action="store_true"); parser.add_argument("--resume", action="store_true"); args = parser.parse_args()
    req = yaml.safe_load(REQ.read_text(encoding="utf-8"))
    global SWIR
    EO, SWIR = channel(req,"eo"), channel(req,"swir")
    geometries = [swir_geometry("S24_B200", SWIR, 2.4, 200),
                  swir_geometry("S20_B120", SWIR, 2.0, 120),
                  swir_geometry("S16_B80", SWIR, 1.6, 80)]
    if args.probe:
        for g in geometries:
            a=size_apertures(g,SWIR); print(g["name"],g,a,evaluate(g,SWIR,a,[g["classical_primary_conic"],g["classical_secondary_conic"],0],8,24)["worst_rms_radius_um"])
        return
    # A failed pre-closure execution may leave only the new empty/partial run
    # directory.  Resume that same run until metadata closes it; never overwrite
    # a completed immutable run.
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "metadata.json").exists() and not args.resume:
        raise RuntimeError("Run 017 is already closed and immutable")
    started=datetime.now(timezone.utc); tick=time.perf_counter()
    b05=load_b05(EO)
    rows=[solve_seed(g,SWIR) for g in geometries]
    for r in rows: r["finite_focus_800m"]=finite_focus(r,SWIR)
    # The middle solution is the balanced system comparator; the other two
    # remain visible Pareto points rather than hidden failed attempts.
    selected=rows[1]
    selected["diffraction"]=[diffraction(selected,SWIR,i,96) for i in (0,5)]
    selected["diffraction_convergence_corner"]=diffraction(selected,SWIR,5,128)
    packages=build_swap(rows,b05)
    c02=json.loads(RUN016_SWAP.read_text(encoding="utf-8"))
    save("metrics.json", {"eo_b05_unchanged_evidence":b05,"swir_seed_results":rows,
                           "selected_system_comparator_seed":"S20_B120"})
    save("package_options.json", {"classification":"geometry and engineering proxies, not CAD or payload mass", "options":packages})
    save("c01_c02_comparison.json", {"c01_package_options":packages,"run016_c02_exact":c02})
    provenance={"authoritative_requirements":{"path":"requirements/eo_swir_system_requirements.yaml","sha256":sha256(REQ)},
                "B05_model":{"path":"runs/run_008/model.py","sha256":sha256(B05_MODEL)},
                "B05_configuration":{"path":"runs/run_008/configuration.json","sha256":sha256(B05_CONFIG)},
                "C02_baseline":{"path":"runs/run_016/swap_screen.json","sha256":sha256(RUN016_SWAP)},
                "historical_files_modified":False,"contamination_control":"reference/ not accessed"}
    save("provenance.json",provenance)
    shutil.copy2(REQ,OUT/"requirements.yaml"); shutil.copy2(__file__,OUT/"track_c_run017_c01.py")
    for r in rows: write_prescription(OUT/f"swir_{r['geometry']['name'].lower()}_prescription.csv",r,SWIR)
    write_prescription(OUT/"prescription.csv",selected,SWIR)
    plot(rows,packages)
    save("dependencies.json", {"python":sys.version,"platform":platform.platform(),"optiland":optiland.__version__,"numpy":np.__version__,"scipy":scipy.__version__})
    save("convergence.json", {"selected_seed":"S20_B120","corner_diffraction_grid_replay":[96,128],
        "interpretation":"filled after numerical review; all three SWIR seeds are separate bounded conic solves"})
    save("metadata.json", {"track":"C","run_id":"017","candidate_ids":["C01"],"parent_run":"run_016",
        "development_stage":"C1 bounded system-level comparator","start_time_utc":started.isoformat(),
        "end_time_utc":datetime.now(timezone.utc).isoformat(),"script_wall_seconds":time.perf_counter()-tick,
        "substantial_computational_search_count":4,"optimization_attempt_count":3,
        "optimizer_evaluations_total":sum(r["optimizer_nfev"] for r in rows),"plateau_counter":0,
        "attempts":["f/2.4 primary, 200 mm back focus","f/2.0 primary, 120 mm back focus","f/1.6 primary, 80 mm back focus"],
        "stopping_reason":"three deliberately spaced SWIR seeds answer the optical-length/obscuration/fabrication trade; no detailed tolerance optimization authorized",
        "contamination_control":"reference/ not accessed"})
    print(json.dumps({"b05_replay_worst_um":b05["fresh_replay"]["worst_rms_um"],
                      "swir":[{"name":r["geometry"]["name"],"worst_um":r["worst_rms_radius_um"],"survival":r["minimum_survival"],"nfev":r["optimizer_nfev"]} for r in rows],
                      "wall_seconds":time.perf_counter()-tick},indent=2))


if __name__=="__main__": main()
