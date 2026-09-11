#!/usr/bin/env python3
"""Track C Run 014: first-order EO+SWIR optical and SWaP architecture screen.

This is deliberately an analytic Stage C0 model.  It does not construct or
optimize an optical prescription.  Numerical package ranges and ordinal risk
ratings are engineering screening assumptions, not customer requirements.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runs" / "run_014"
REQ_PATH = ROOT / "requirements" / "eo_swir_system_requirements.yaml"
RUN_ID = "014"


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def first_order(channel: dict) -> dict:
    pitch_mm = float(channel["pixel_pitch_um"][0]) / 1000.0
    ifov_rad = float(channel["instantaneous_fov_urad_per_pixel"]) * 1e-6
    efl_mm = pitch_mm / ifov_rad
    pupil_mm = efl_mm / float(channel["f_number"])
    object_distance_mm = float(channel["minimum_focus_distance_m"]) * 1000.0
    focus_shift_mm = efl_mm * efl_mm / (object_distance_mm - efl_mm)
    width_rad = int(channel["array_px"][0]) * ifov_rad
    height_rad = int(channel["array_px"][1]) * ifov_rad
    return {
        "effective_focal_length_mm": efl_mm,
        "entrance_pupil_diameter_mm": pupil_mm,
        "horizontal_fov_deg_from_array_ifov": math.degrees(width_rad),
        "vertical_fov_deg_from_array_ifov": math.degrees(height_rad),
        "thin_lens_focus_shift_infinity_to_800m_mm": focus_shift_mm,
    }


def envelope_volume_l(bounds: list[list[float]]) -> list[float]:
    return [
        bounds[0][0] * bounds[1][0] * bounds[2][0] / 1e6,
        bounds[0][1] * bounds[1][1] * bounds[2][1] / 1e6,
    ]


def main() -> None:
    start = datetime.now(timezone.utc)
    if OUT.exists():
        raise RuntimeError(f"Refusing to overwrite immutable output directory: {OUT}")
    OUT.mkdir(parents=False)

    requirements = yaml.safe_load(REQ_PATH.read_text(encoding="utf-8"))
    source = requirements["source_explicit_requirements"]
    eo = first_order(source["eo"])
    swir = first_order(source["swir"])

    area_ratio = (swir["entrance_pupil_diameter_mm"] ** 2 + eo["entrance_pupil_diameter_mm"] ** 2) / swir["entrance_pupil_diameter_mm"] ** 2
    diameter_ratio = swir["entrance_pupil_diameter_mm"] / eo["entrance_pupil_diameter_mm"]
    min_tangent_baseline_mm = (swir["entrance_pupil_diameter_mm"] + eo["entrance_pupil_diameter_mm"]) / 2.0
    parallax_800m_urad = min_tangent_baseline_mm / 800_000.0 * 1e6

    # Solid collecting-primary blank proxy only: t/D=0.10, density=2.2 g/cm3.
    # It excludes secondary/tertiary optics, cells, baffles, electronics and
    # lightweighting.  The same assumption is applied to common and separate
    # cases solely to expose scale.
    def blank_proxy(diameters_mm: list[float]) -> dict:
        volume_mm3 = sum(math.pi / 40.0 * diameter**3 for diameter in diameters_mm)
        mass_kg = volume_mm3 / 1000.0 * 2.2 / 1000.0
        return {"solid_blank_volume_l": volume_mm3 / 1e6, "solid_blank_mass_proxy_kg": mass_kg}

    common_blank = blank_proxy([swir["entrance_pupil_diameter_mm"]])
    separate_blank = blank_proxy([swir["entrance_pupil_diameter_mm"], eo["entrance_pupil_diameter_mm"]])

    first_order_data = {
        "classification": "derived first-order quantities, not customer requirements",
        "eo": eo,
        "swir": swir,
        "system_ratios": {
            "swir_to_eo_efl_and_pupil_ratio": diameter_ratio,
            "swir_to_eo_pupil_area_ratio": diameter_ratio**2,
            "separate_to_common_collecting_area_ratio": area_ratio,
            "common_collecting_area_saving_percent_vs_separate": 100.0 * (1.0 - 1.0 / area_ratio),
            "minimum_tangent_separate_aperture_center_baseline_mm": min_tangent_baseline_mm,
            "parallax_at_800m_for_minimum_tangent_baseline_urad": parallax_800m_urad,
            "parallax_at_800m_in_eo_pixels": parallax_800m_urad / source["eo"]["instantaneous_fov_urad_per_pixel"],
            "parallax_at_800m_in_swir_pixels": parallax_800m_urad / source["swir"]["instantaneous_fov_urad_per_pixel"],
        },
        "collecting_primary_blank_proxy": {
            "assumption": "solid circular blank, thickness/diameter=0.10, density=2.2 g/cm3; collecting primaries only",
            "common_swir_sized_primary": common_blank,
            "separate_eo_plus_swir_primaries": separate_blank,
            "separate_to_common_mass_proxy_ratio": separate_blank["solid_blank_mass_proxy_kg"] / common_blank["solid_blank_mass_proxy_kg"],
            "limitations": "not a payload mass estimate; excludes lightweighting, all other optics, mounts, cells, baffles, mechanisms, windows, electronics and gimbal effects",
        },
    }

    # Bounding boxes are deliberately wide C0 architecture hypotheses.  They
    # allow volume-pressure comparison but are not layouts or requirements.
    architectures = [
        {
            "id": "C01",
            "architecture": "Separate integrated EO and SWIR telescopes",
            "sharing": "separate",
            "largest_required_clear_aperture_mm": swir["entrance_pupil_diameter_mm"],
            "representative_bbox_mm_minmax": [[460, 580], [340, 430], [650, 1050]],
            "large_optics_over_100mm_count_range": [3, 5],
            "powered_surface_count_range": [8, 12],
            "custom_powered_surface_count_range": [6, 10],
            "freeform_surface_count_range": [0, 0],
            "splitter_count": 0,
            "external_apertures": 2,
            "focus_mechanisms": 2,
            "relative_boresight_burden_1low_5high": 4,
            "alignment_metrology_burden_1low_5high": 3,
            "nre_class_1low_5high": 3,
            "recurring_custom_optics_burden_1low_5high": 3,
            "qualification_burden_1low_5high": 4,
            "supplier_concentration_1low_5high": 2,
            "cots_content": "EO B-series reuse possible; SWIR remains new; mechanics custom",
            "coating_throughput": "independent channel coatings; no dichroic loss",
            "thermal_focus": "two independent focus/athermalisation loops; lowest optical coupling",
            "gimbal_integration": "widest front face; two LOS datums; possible parallax but modular service",
            "c0_status": "ACTIVE - recommend C1",
            "pareto_role": "independent-channel/reuse and no-splitter lane",
            "c1_gate": "fresh SWIR seed plus integrated boresight/parallax and structure model",
        },
        {
            "id": "C02",
            "architecture": "Common coaxial reflective fore-telescope plus independent relays",
            "sharing": "partially_shared",
            "largest_required_clear_aperture_mm": swir["entrance_pupil_diameter_mm"],
            "representative_bbox_mm_minmax": [[340, 430], [340, 430], [550, 850]],
            "large_optics_over_100mm_count_range": [2, 4],
            "powered_surface_count_range": [8, 12],
            "custom_powered_surface_count_range": [6, 10],
            "freeform_surface_count_range": [0, 0],
            "splitter_count": 1,
            "external_apertures": 1,
            "focus_mechanisms": 2,
            "relative_boresight_burden_1low_5high": 2,
            "alignment_metrology_burden_1low_5high": 3,
            "nre_class_1low_5high": 4,
            "recurring_custom_optics_burden_1low_5high": 4,
            "qualification_burden_1low_5high": 4,
            "supplier_concentration_1low_5high": 3,
            "cots_content": "limited powered COTS; conventional coaxial manufacture",
            "coating_throughput": "two common reflections plus dichroic and channel relays; 800 nm allocation required",
            "thermal_focus": "shared fore-optic drift plus two relay focus controls",
            "gimbal_integration": "single LOS/front aperture; obscuration and secondary support affect aperture and jitter",
            "c0_status": "ACTIVE - recommend C1",
            "pareto_role": "conventional common-LOS balance lane",
            "c1_gate": "coaxial common-front seed, obscuration budget and collimated/pupil splitter placement",
        },
        {
            "id": "C03",
            "architecture": "Common off-axis afocal/TMA front end plus modular relays",
            "sharing": "partially_shared",
            "largest_required_clear_aperture_mm": swir["entrance_pupil_diameter_mm"],
            "representative_bbox_mm_minmax": [[420, 600], [340, 500], [500, 850]],
            "large_optics_over_100mm_count_range": [3, 5],
            "powered_surface_count_range": [9, 13],
            "custom_powered_surface_count_range": [7, 11],
            "freeform_surface_count_range": [0, 2],
            "splitter_count": 1,
            "external_apertures": 1,
            "focus_mechanisms": 2,
            "relative_boresight_burden_1low_5high": 2,
            "alignment_metrology_burden_1low_5high": 5,
            "nre_class_1low_5high": 5,
            "recurring_custom_optics_burden_1low_5high": 5,
            "qualification_burden_1low_5high": 5,
            "supplier_concentration_1low_5high": 4,
            "cots_content": "low powered COTS; modular backends may reuse standard processes",
            "coating_throughput": "unobscured pupil but at least one extra common reflection likely; dichroic allocation required",
            "thermal_focus": "common afocal LOS stability plus two independently athermalised/focused cameras",
            "gimbal_integration": "single LOS; asymmetric inertia/envelope and off-axis datum control",
            "c0_status": "ACTIVE - recommend C1",
            "pareto_role": "unobscured/common-LOS optical-performance lane",
            "c1_gate": "minimum-complexity three-mirror afocal seed and physical clearance/layout proof",
        },
        {
            "id": "C04",
            "architecture": "Cost/COTS-maximized dual-channel branch",
            "sharing": "separate_or_partially_shared",
            "largest_required_clear_aperture_mm": swir["entrance_pupil_diameter_mm"],
            "representative_bbox_mm_minmax": [[450, 650], [350, 480], [650, 1300]],
            "large_optics_over_100mm_count_range": [3, 5],
            "powered_surface_count_range": [7, 12],
            "custom_powered_surface_count_range": [4, 8],
            "freeform_surface_count_range": [0, 0],
            "splitter_count": "0_or_1",
            "external_apertures": "1_or_2",
            "focus_mechanisms": 2,
            "relative_boresight_burden_1low_5high": 4,
            "alignment_metrology_burden_1low_5high": 3,
            "nre_class_1low_5high": 2,
            "recurring_custom_optics_burden_1low_5high": 2,
            "qualification_burden_1low_5high": 5,
            "supplier_concentration_1low_5high": 3,
            "cots_content": "highest potential; donor optics require new airborne cells/coatings/qualification",
            "coating_throughput": "no splitter if separate, but stock SWIR transmission/coating suitability is unproven",
            "thermal_focus": "stock substrate/structure data and actuator range are gating unknowns",
            "gimbal_integration": "donor OTAs unsuitable as-is; custom lightweight rehousing can erode savings",
            "c0_status": "ACTIVE - recommend C1 economic lane",
            "pareto_role": "procurement/NRE and recurring-cost hypothesis lane",
            "c1_gate": "identify >=311.37 mm clear-aperture donor path or admit custom SWIR primary; verify coatings/substrates",
        },
        {
            "id": "C05",
            "architecture": "Compact folded/freeform shared architecture",
            "sharing": "partially_shared",
            "largest_required_clear_aperture_mm": swir["entrance_pupil_diameter_mm"],
            "representative_bbox_mm_minmax": [[350, 500], [320, 450], [350, 600]],
            "large_optics_over_100mm_count_range": [3, 5],
            "powered_surface_count_range": [6, 10],
            "custom_powered_surface_count_range": [6, 10],
            "freeform_surface_count_range": [2, 4],
            "splitter_count": 1,
            "external_apertures": 1,
            "focus_mechanisms": 2,
            "relative_boresight_burden_1low_5high": 2,
            "alignment_metrology_burden_1low_5high": 5,
            "nre_class_1low_5high": 5,
            "recurring_custom_optics_burden_1low_5high": 5,
            "qualification_burden_1low_5high": 5,
            "supplier_concentration_1low_5high": 5,
            "cots_content": "very low for powered optics",
            "coating_throughput": "multiple non-normal reflections and dichroic; polarization/angle effects important",
            "thermal_focus": "monolithic concept may remove mounts but couples thermal figure and surface registration",
            "gimbal_integration": "best assumed volume compression; mass benefit unproved and centre-of-gravity work remains",
            "c0_status": "PARKED after C0",
            "pareto_role": "latent compactness stretch lane",
            "c1_gate": "reopen only if C01-C04 packaging cannot form an attractive portfolio or supplier evidence lowers risk",
        },
    ]

    for architecture in architectures:
        architecture["representative_bbox_volume_l_minmax"] = envelope_volume_l(architecture["representative_bbox_mm_minmax"])
        architecture["bbox_classification"] = "C0 hypothesis range, not a CAD envelope or customer limit"
        architecture["mass_proxy_classification"] = "common primary proxy for shared paths; separate primary proxy for separate paths; excludes full payload"

    throughput_rows = []
    for reflectance in (0.88, 0.90, 0.92, 0.95, 0.98):
        for splitter_efficiency in (0.85, 0.90, 0.95):
            throughput_rows.append(
                {
                    "mirror_reflectance_each": reflectance,
                    "splitter_useful_port_efficiency": splitter_efficiency,
                    "two_mirror_no_splitter": reflectance**2,
                    "two_mirror_plus_splitter": reflectance**2 * splitter_efficiency,
                    "three_mirror_plus_splitter": reflectance**3 * splitter_efficiency,
                    "classification": "coating-count sensitivity only; excludes relays, windows, glass, QE, polarization and obscuration",
                }
            )

    write_json(OUT / "metrics.json", first_order_data)
    write_json(OUT / "architecture_screen.json", {"architecture_assumption_note": "ordinal ratings and envelope ranges are Stage C0 engineering hypotheses, not requirements or predictions", "architectures": architectures})
    write_csv(
        OUT / "first_order.csv",
        [
            {"channel": "EO", **eo},
            {"channel": "SWIR", **swir},
        ],
        ["channel", *eo.keys()],
    )
    write_csv(
        OUT / "architecture_screen.csv",
        architectures,
        list(architectures[0].keys()),
    )
    write_csv(OUT / "throughput_sensitivity.csv", throughput_rows, list(throughput_rows[0].keys()))

    labels = [item["id"] for item in architectures]
    volume_mid = [sum(item["representative_bbox_volume_l_minmax"]) / 2 for item in architectures]
    volume_err = [
        [mid - item["representative_bbox_volume_l_minmax"][0] for mid, item in zip(volume_mid, architectures)],
        [item["representative_bbox_volume_l_minmax"][1] - mid for mid, item in zip(volume_mid, architectures)],
    ]
    nre = [item["nre_class_1low_5high"] for item in architectures]
    colors = ["#2c7fb8", "#41b6c4", "#7fcdbb", "#fdae61", "#d7191c"]
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.errorbar(volume_mid, nre, xerr=volume_err, fmt="none", ecolor="#777777", capsize=4, alpha=0.75)
    for x, y, label, color in zip(volume_mid, nre, labels, colors):
        ax.scatter(x, y, s=110, color=color, edgecolor="black", linewidth=0.6, zorder=3)
        ax.annotate(label, (x, y), xytext=(7, 6), textcoords="offset points", fontsize=10, weight="bold")
    ax.set_xlabel("Representative C0 envelope hypothesis (litres, midpoint and range)")
    ax.set_ylabel("Relative NRE class (1 low, 5 high)")
    ax.set_yticks(range(1, 6))
    ax.grid(True, alpha=0.25)
    ax.set_title("Run 014 architecture trade — uncertainty ranges, not requirements")
    fig.tight_layout()
    fig.savefig(OUT / "swap_nre_trade.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.6, 5.3))
    rs = [row["mirror_reflectance_each"] for row in throughput_rows if row["splitter_useful_port_efficiency"] == 0.90]
    two = [row["two_mirror_no_splitter"] for row in throughput_rows if row["splitter_useful_port_efficiency"] == 0.90]
    two_split = [row["two_mirror_plus_splitter"] for row in throughput_rows if row["splitter_useful_port_efficiency"] == 0.90]
    three_split = [row["three_mirror_plus_splitter"] for row in throughput_rows if row["splitter_useful_port_efficiency"] == 0.90]
    ax.plot(rs, two, marker="o", label="2 mirrors, no splitter")
    ax.plot(rs, two_split, marker="o", label="2 mirrors + 90% useful splitter port")
    ax.plot(rs, three_split, marker="o", label="3 mirrors + 90% useful splitter port")
    ax.set_xlabel("Per-mirror reflectance assumption")
    ax.set_ylabel("Core-path throughput product")
    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.set_title("Coating/count sensitivity only — relay, window, QE and obscuration excluded")
    fig.tight_layout()
    fig.savefig(OUT / "throughput_sensitivity.png", dpi=180)
    plt.close(fig)

    shutil.copy2(REQ_PATH, OUT / "requirements.yaml")
    shutil.copy2(Path(__file__), OUT / Path(__file__).name)

    end = datetime.now(timezone.utc)
    dependencies = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "matplotlib": matplotlib.__version__,
        "pyyaml": yaml.__version__,
        "optiland_used": False,
        "reason": "Stage C0 is first-order analytic/SWaP screening with no prescription optimization",
    }
    write_json(OUT / "dependencies.json", dependencies)
    metadata = {
        "track": "C",
        "run_id": RUN_ID,
        "candidate_ids": labels,
        "preceding_run": "run_013 (historical Track B thermal evidence; Track C initialized afterward)",
        "purpose": "first-order optical plus SWaP architecture screening of C01-C05",
        "development_stage": "C0 screening",
        "start_time_utc": start.isoformat(),
        "end_time_utc": end.isoformat(),
        "substantial_optimizer_or_search_count": 0,
        "materially_distinct_optimization_attempt_count": 0,
        "plateau_counter": 0,
        "plateau_status": "not applicable; no optimization",
        "result": {
            "advance_to_c1": ["C01", "C02", "C03", "C04"],
            "park": ["C05"],
            "reject": [],
        },
        "human_interventions": [
            "User corrected requirements provenance taxonomy and Track C workflow authority before Run 014; numerical requirements were unchanged."
        ],
        "contamination_control": "reference/ not accessed",
    }
    write_json(OUT / "metadata.json", metadata)

    hashes = []
    for path in sorted(OUT.iterdir(), key=lambda p: p.name.lower()):
        if path.name == "SHA256SUMS.txt" or not path.is_file():
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.append(f"{digest}  {path.name}")
    (OUT / "SHA256SUMS.txt").write_text("\n".join(hashes) + "\n", encoding="utf-8")

    print(json.dumps({"run": str(OUT), "advance": ["C01", "C02", "C03", "C04"], "park": ["C05"], "elapsed_s": (end - start).total_seconds()}, indent=2))


if __name__ == "__main__":
    main()
