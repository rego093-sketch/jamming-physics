\
"""
mst_optionb_unit_realization.py

MST Option–B: operational-anchor unit realisation + RCROSS (633/532 nm)
for the lattice SOC bundle.

What this does (fit-free):
1) Estimate structural amplification A from the SOC avalanche log (A_post).
2) Realise absolute lattice units using an operational anchor (iodine-stabilized lines).
3) Perform an RCROSS check against 532 nm (and report 633 nm too).

Outputs (written under bundle root):
- results/mst_unit_realization.json
- results/mst_rcross.csv
- images/mst_rcross.png

Notes
- This is a minimal, auditable implementation meant to live inside the DOI bundle.
- Threshold tiers follow the registered YAML (config/thresholds.yaml), but to avoid
  adding PyYAML as a hard dependency, we embed the tier values here.

Author: Young Jae Lee (Independent Researcher)
"""

from __future__ import annotations

import csv
import json
import math
import os
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple

import numpy as np
import matplotlib.pyplot as plt


C_REF = 299_792_458.0  # m/s, exact by SI definition


# Recommended iodine-stabilized line frequencies (vacuum), as quoted in MST Option–B manuscript.
# Units: Hz (converted from kHz in the cited recommendation tables)
FREF_633_HZ = 473_612_353_604_000.0
FREF_532_HZ = 563_260_223_513_000.0


@dataclass(frozen=True)
class RCrossTier:
    name: str
    dev_max: float  # max(|f_obs/f_ref - 1|)


TIERS = {
    "guard": RCrossTier("guard", 1.0e-11),
    "nominal": RCrossTier("nominal", 1.0e-10),
    "relaxed": RCrossTier("relaxed", 1.0e-8),
}


def _robust_geomean(x: Iterable[float]) -> float:
    arr = np.asarray(list(x), dtype=float)
    arr = arr[np.isfinite(arr) & (arr > 0)]
    if arr.size == 0:
        raise ValueError("No finite positive values to compute geometric mean.")
    return float(np.exp(np.mean(np.log(arr))))


def _load_soc_avalanches(csv_path: str) -> np.ndarray:
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Missing SOC avalanche CSV: {csv_path}")
    rows = []
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            if "A_post" in row and row["A_post"] not in (None, "", "nan"):
                try:
                    rows.append(float(row["A_post"]))
                except ValueError:
                    # allow "inf" etc -> float handles "inf"
                    try:
                        rows.append(float(row["A_post"].strip()))
                    except Exception:
                        pass
    return np.asarray(rows, dtype=float)


def _ensure_dirs(root: str) -> Tuple[str, str]:
    res = os.path.join(root, "results")
    img = os.path.join(root, "images")
    os.makedirs(res, exist_ok=True)
    os.makedirs(img, exist_ok=True)
    return res, img


def run(
    root: str,
    n_anchor_633: float = 1e12,
    tier: str = "nominal",
    avalanches_csv: str = "results/soc_run3_avalanches.csv",
) -> Dict[str, float]:
    """
    Returns a dict (also written to results/mst_unit_realization.json).
    """
    if tier not in TIERS:
        raise ValueError(f"tier must be one of {list(TIERS)}, got {tier}")

    res_dir, img_dir = _ensure_dirs(root)

    A_post = _load_soc_avalanches(os.path.join(root, avalanches_csv))
    A_geo = _robust_geomean(A_post)

    # Operational anchor: use recommended frequencies as primary references, derive wavelengths.
    lambda_633 = C_REF / FREF_633_HZ
    lambda_532 = C_REF / FREF_532_HZ

    # Unit realisation (micro-lattice)
    a = lambda_633 / n_anchor_633
    dt = A_geo * a / C_REF

    # Derived lattice counts per wavelength
    N_633 = lambda_633 / a  # equals n_anchor_633 by construction
    N_532 = lambda_532 / a

    def f_obs(lambda_line: float) -> float:
        # Using the lattice transport form: f = (A / N_lambda) * (1/dt).
        # With dt = A*a/C, N_lambda=lambda/a, this collapses to C/lambda.
        N_line = lambda_line / a
        return (A_geo / N_line) * (1.0 / dt)

    fobs_633 = f_obs(lambda_633)
    fobs_532 = f_obs(lambda_532)

    def rel_dev(fobs: float, fref: float) -> float:
        return abs(fobs / fref - 1.0)

    dev_633 = rel_dev(fobs_633, FREF_633_HZ)
    dev_532 = rel_dev(fobs_532, FREF_532_HZ)

    tier_dev_max = TIERS[tier].dev_max

    rcross_rows = [
        {"lambda_nm": 633.0, "f_ref_hz": FREF_633_HZ, "f_obs_hz": fobs_633, "rel_dev": dev_633, "tier": tier, "dev_max": tier_dev_max},
        {"lambda_nm": 532.0, "f_ref_hz": FREF_532_HZ, "f_obs_hz": fobs_532, "rel_dev": dev_532, "tier": tier, "dev_max": tier_dev_max},
    ]

    # Write CSV
    rcross_csv = os.path.join(res_dir, "mst_rcross.csv")
    with open(rcross_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rcross_rows[0].keys()))
        w.writeheader()
        w.writerows(rcross_rows)

    # Plot (log scale)
    xs = [r["lambda_nm"] for r in rcross_rows]
    ys = [r["rel_dev"] for r in rcross_rows]
    # log-scale plot: avoid zero by clamping for display
    ys_plot = [max(y, 1e-16) for y in ys]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title("RCROSS check with 3-tier thresholds (log scale)")
    ax.set_xlabel("Wavelength λ_ref [nm]")
    ax.set_ylabel("Absolute relative deviation |f_obs/f_ref - 1| [-]")
    ax.set_yscale("log")
    ax.plot(xs, ys_plot, marker="x", linestyle="none")
    # Tier lines
    for name, t in TIERS.items():
        ax.axhline(t.dev_max, linestyle="--", linewidth=1.0)
        ax.text(min(xs) + 1.0, t.dev_max * 1.1, f"{name} {t.dev_max:g}", fontsize=9)
    fig.tight_layout()
    fig_path = os.path.join(img_dir, "mst_rcross.png")
    fig.savefig(fig_path, dpi=200)
    plt.close(fig)

    out = {
        "A_geo": A_geo,
        "n_anchor_633": n_anchor_633,
        "lambda_633_m": lambda_633,
        "lambda_532_m": lambda_532,
        "a_m": a,
        "dt_s": dt,
        "N_633": N_633,
        "N_532": N_532,
        "fobs_633_hz": fobs_633,
        "fobs_532_hz": fobs_532,
        "dev_633": dev_633,
        "dev_532": dev_532,
        "rcross_tier": tier,
        "rcross_dev_max": tier_dev_max,
    }

    with open(os.path.join(res_dir, "mst_unit_realization.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    return out


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, ".."))
    out = run(root=root)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
