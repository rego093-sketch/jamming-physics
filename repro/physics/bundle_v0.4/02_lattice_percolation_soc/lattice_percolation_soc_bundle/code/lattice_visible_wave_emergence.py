\
"""
lattice_visible_wave_emergence.py

Demonstration: "visible-light carrier" on the jammed lattice after unit realisation.

We do NOT allocate 1e12 cells. Instead we:
- keep the micro-lattice parameters (N_633 = 1e12, a, dt) fixed by the MST anchor,
- and sample the analytic traveling-wave mode on a sparse set of lattice indices.

This produces:
- spatial waveform over one wavelength (633 nm / 532 nm),
- temporal waveform over a few optical cycles (converted to femtoseconds),
- a spatio-temporal "carrier sheet" (x vs t image),
- a summary JSON of the physical mapping, period-in-ticks, and a speed sanity check.

Outputs:
- results/visible_wave_summary.json
- images/visible_wave_633_space.png
- images/visible_wave_633_time.png
- images/visible_wave_633_xt.png
- images/visible_wave_532_space.png
- images/visible_wave_532_time.png
- images/visible_wave_532_xt.png

Author: Young Jae Lee (Independent Researcher)
"""

from __future__ import annotations

import json
import math
import os
from typing import Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt

from mst_optionb_unit_realization import (
    C_REF,
    FREF_633_HZ,
    FREF_532_HZ,
    _load_soc_avalanches,
    _robust_geomean,
    _ensure_dirs,
)


def _traveling_wave(n: np.ndarray, t_ticks: np.ndarray, N_lambda: float, A: float) -> np.ndarray:
    """
    u(n,t) = sin(2π (n - A t)/N_lambda), where n and t can be float arrays.
    """
    return np.sin(2.0 * np.pi * (n - A * t_ticks) / N_lambda)


def _plot_space(root_img: str, tag: str, n: np.ndarray, u: np.ndarray, a_m: float) -> str:
    x_nm = (n * a_m) * 1e9
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f"Spatial carrier (one wavelength): {tag}")
    ax.set_xlabel("x [nm]")
    ax.set_ylabel("u(x) [arb.]")
    ax.plot(x_nm, u)
    fig.tight_layout()
    out_path = os.path.join(root_img, f"visible_wave_{tag}_space.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def _plot_time(root_img: str, tag: str, t_ticks: np.ndarray, u: np.ndarray, dt_s: float) -> str:
    t_fs = (t_ticks * dt_s) * 1e15
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f"Temporal carrier (few cycles): {tag}")
    ax.set_xlabel("t [fs]")
    ax.set_ylabel("u(t) [arb.]")
    ax.plot(t_fs, u)
    fig.tight_layout()
    out_path = os.path.join(root_img, f"visible_wave_{tag}_time.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def _plot_xt(root_img: str, tag: str, n: np.ndarray, t_ticks: np.ndarray, U: np.ndarray, a_m: float, dt_s: float) -> str:
    x_nm = (n * a_m) * 1e9
    t_fs = (t_ticks * dt_s) * 1e15
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f"Spatio-temporal carrier sheet: {tag}")
    ax.set_xlabel("t [fs]")
    ax.set_ylabel("x [nm]")
    im = ax.imshow(
        U,
        aspect="auto",
        origin="lower",
        extent=[t_fs.min(), t_fs.max(), x_nm.min(), x_nm.max()],
    )
    fig.colorbar(im, ax=ax, label="u(x,t)")
    fig.tight_layout()
    out_path = os.path.join(root_img, f"visible_wave_{tag}_xt.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def run(root: str, n_anchor_633: float = 1e12, cycles_to_plot: float = 3.0) -> Dict:
    res_dir, img_dir = _ensure_dirs(root)

    # Load A from SOC logs (robust)
    A_post = _load_soc_avalanches(os.path.join(root, "results/soc_run3_avalanches.csv"))
    A = _robust_geomean(A_post)

    # Anchor (vacuum wavelengths derived from recommended frequencies)
    lambda_633 = C_REF / FREF_633_HZ
    lambda_532 = C_REF / FREF_532_HZ

    # Micro lattice spacing and tick (same as in mst_optionb_unit_realization.py)
    a = lambda_633 / n_anchor_633
    dt = A * a / C_REF

    # Lattice cell counts per wavelength (can be non-integer for 532)
    N_633 = lambda_633 / a
    N_532 = lambda_532 / a

    # Period in ticks for each carrier
    P633_ticks = N_633 / A
    P532_ticks = N_532 / A

    # --- 633 nm plots ---
    # sample ~one wavelength in space
    n_space = np.linspace(0.0, N_633, 2048, endpoint=False)
    u_space_633 = _traveling_wave(n_space, np.array([0.0]), N_633, A).reshape(-1)

    # time series at n=0 for a few cycles
    t_ticks_633 = np.linspace(0.0, cycles_to_plot * P633_ticks, 6000)
    u_time_633 = _traveling_wave(np.array([0.0]), t_ticks_633, N_633, A).reshape(-1)

    # spatio-temporal sheet (downsampled)
    n_xt_633 = np.linspace(0.0, N_633, 400, endpoint=False)
    t_xt_633 = np.linspace(0.0, 1.0 * P633_ticks, 400)
    U_xt_633 = _traveling_wave(n_xt_633[:, None], t_xt_633[None, :], N_633, A)

    p1 = _plot_space(img_dir, "633", n_space, u_space_633, a_m=a)
    p2 = _plot_time(img_dir, "633", t_ticks_633, u_time_633, dt_s=dt)
    p3 = _plot_xt(img_dir, "633", n_xt_633, t_xt_633, U_xt_633, a_m=a, dt_s=dt)

    # --- 532 nm plots ---
    n_space_g = np.linspace(0.0, N_532, 2048, endpoint=False)
    u_space_532 = _traveling_wave(n_space_g, np.array([0.0]), N_532, A).reshape(-1)

    t_ticks_532 = np.linspace(0.0, cycles_to_plot * P532_ticks, 6000)
    u_time_532 = _traveling_wave(np.array([0.0]), t_ticks_532, N_532, A).reshape(-1)

    n_xt_532 = np.linspace(0.0, N_532, 400, endpoint=False)
    t_xt_532 = np.linspace(0.0, 1.0 * P532_ticks, 400)
    U_xt_532 = _traveling_wave(n_xt_532[:, None], t_xt_532[None, :], N_532, A)

    q1 = _plot_space(img_dir, "532", n_space_g, u_space_532, a_m=a)
    q2 = _plot_time(img_dir, "532", t_ticks_532, u_time_532, dt_s=dt)
    q3 = _plot_xt(img_dir, "532", n_xt_532, t_xt_532, U_xt_532, a_m=a, dt_s=dt)

    # Speed sanity check: two sensors separated by quarter wavelength (633)
    dn = 0.25 * N_633
    dx = dn * a
    dt_delay_ticks = dn / A
    dt_delay_s = dt_delay_ticks * dt
    c_est = dx / dt_delay_s

    out = {
        "A_geo": A,
        "n_anchor_633": n_anchor_633,
        "a_m": a,
        "dt_s": dt,
        "lambda_633_m": lambda_633,
        "lambda_532_m": lambda_532,
        "N_633": N_633,
        "N_532": N_532,
        "period_633_ticks": P633_ticks,
        "period_532_ticks": P532_ticks,
        "period_633_s": P633_ticks * dt,
        "period_532_s": P532_ticks * dt,
        "f_pred_633_hz": 1.0 / (P633_ticks * dt),
        "f_pred_532_hz": 1.0 / (P532_ticks * dt),
        "speed_check": {
            "dn_cells": dn,
            "dx_m": dx,
            "delay_ticks": dt_delay_ticks,
            "delay_s": dt_delay_s,
            "c_est_m_per_s": c_est,
            "c_ref_m_per_s": C_REF,
            "rel_err": abs(c_est / C_REF - 1.0),
        },
        "artifacts": {
            "space_633": os.path.relpath(p1, root),
            "time_633": os.path.relpath(p2, root),
            "xt_633": os.path.relpath(p3, root),
            "space_532": os.path.relpath(q1, root),
            "time_532": os.path.relpath(q2, root),
            "xt_532": os.path.relpath(q3, root),
        },
    }

    with open(os.path.join(res_dir, "visible_wave_summary.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    return out


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.abspath(os.path.join(here, ".."))
    out = run(root=root)
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
