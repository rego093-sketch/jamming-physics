from __future__ import annotations

"""Produce robustness plots for the metriplectic ensemble.

Two figures are generated:

- ``figures/robustness_Nscan.png``:
    mean ± one standard deviation of the event dissipation as a
    function of effective Reynolds number for several particle numbers
    ``N``.
- ``figures/robustness_seedscatter.png``:
    scatter of individual ensemble members in the
    (Re_eff, eps_bind) plane, illustrating the spread over random
    seeds.

Both plots are based entirely on the pre-computed ensemble stored in
``data/raw/epsilon_events_ensemble.csv``.
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROC = DATA / "processed"
FIGURES = ROOT / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)


def _load_summary() -> pd.DataFrame:
    """Load (or rebuild) the ensemble summary table."""
    summary_csv = DATA_PROC / "epsilon_events_summary.csv"
    if summary_csv.exists():
        return pd.read_csv(summary_csv)

    raw_csv = DATA_RAW / "epsilon_events_ensemble.csv"
    if not raw_csv.exists():
        raise FileNotFoundError(
            f"Raw ensemble file not found: {raw_csv}\n"
            "This archive is expected to include it; if you have "
            "replaced it with your own data, please regenerate the "
            "summary table first."
        )
    from . import robustness_scans

    df_raw = pd.read_csv(raw_csv)
    summary = robustness_scans.summarize_ensemble(df_raw)
    summary.to_csv(summary_csv, index=False)
    print(f"Rebuilt ensemble summary at: {summary_csv}")
    return summary


def plot_N_scan() -> None:
    """Plot mean±std of eps_bind vs Re_eff for each N."""
    summary = _load_summary()

    fig, ax = plt.subplots(figsize=(6, 4))

    for N in sorted(summary["N"].unique()):
        sub = summary[summary["N"] == N].sort_values("Re_eff_mean")
        ax.errorbar(
            sub["Re_eff_mean"],
            sub["eps_bind_mean"],
            yerr=sub["eps_bind_std"],
            marker="o",
            linestyle="-",
            label=f"N={N}",
        )

    ax.set_xscale("log")
    ax.set_xlabel(r"Effective Reynolds Number ($Re_{\mathrm{eff}}$)")
    ax.set_ylabel(r"Event Dissipation $\varepsilon_{\mathrm{bind}}$")
    ax.set_title("Robustness: N-scan of event dissipation")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    out = FIGURES / "robustness_Nscan.png"
    fig.savefig(out, dpi=300)
    print(f"Saved N-scan robustness figure to: {out}")


def plot_seed_scatter() -> None:
    """Scatter of individual ensemble members in (Re_eff, eps_bind)."""
    raw_csv = DATA_RAW / "epsilon_events_ensemble.csv"
    if not raw_csv.exists():
        raise FileNotFoundError(
            f"Raw ensemble file not found: {raw_csv}\n"
            "This archive is expected to include it."
        )
    df = pd.read_csv(raw_csv)

    fig, ax = plt.subplots(figsize=(6, 4))

    for rc in sorted(df["rc"].unique()):
        sub = df[df["rc"] == rc]
        ax.scatter(
            sub["Re_eff"],
            sub["eps_bind"],
            label=fr"$r_c={rc:g}$",
            alpha=0.7,
        )

    ax.set_xscale("log")
    ax.set_xlabel(r"Effective Reynolds Number ($Re_{\mathrm{eff}}$)")
    ax.set_ylabel(r"Event Dissipation $\varepsilon_{\mathrm{bind}}$")
    ax.set_title("Robustness: ensemble spread over seeds")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    out = FIGURES / "robustness_seedscatter.png"
    fig.savefig(out, dpi=300)
    print(f"Saved seed-scatter robustness figure to: {out}")


def main() -> None:
    plot_N_scan()
    plot_seed_scatter()


if __name__ == "__main__":
    main()
