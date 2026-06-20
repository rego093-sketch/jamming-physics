from __future__ import annotations

"""Build the metriplectic dissipation table used in the main figure.

This script does **not** run any heavy simulations.  Instead it
summarises the pre-computed ensemble in
``data/raw/epsilon_events_ensemble.csv`` (or its processed form
``data/processed/epsilon_events_summary.csv``) into the compact table

    data/processed/dissipation_vs_Re_metriplectic.csv

which is then consumed by :mod:`src.plot_dissipation_saturation`.
The raw ensemble itself was generated offline with the production
Average Discrete Gradient (ADG) solver described in the Letter.
"""

import pathlib
import pandas as pd
from . import robustness_scans

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROC = DATA / "processed"
DATA_PROC.mkdir(parents=True, exist_ok=True)


def load_or_build_summary() -> pd.DataFrame:
    """Return the ensemble summary table.

    Preference is given to ``epsilon_events_summary.csv``; if it is
    missing but the raw ensemble file is present, we recompute the
    summary using :func:`robustness_scans.summarize_ensemble`.
    """
    summary_csv = DATA_PROC / "epsilon_events_summary.csv"
    if summary_csv.exists():
        return pd.read_csv(summary_csv)

    raw_csv = DATA_RAW / "epsilon_events_ensemble.csv"
    if not raw_csv.exists():
        raise FileNotFoundError(
            f"Neither {summary_csv} nor {raw_csv} could be found.\n"
            "This package is expected to ship with a pre-computed "
            "ensemble under data/raw; if you replaced it with your "
            "own data, please regenerate the summary first."
        )

    df_raw = pd.read_csv(raw_csv)
    summary = robustness_scans.summarize_ensemble(df_raw)
    summary.to_csv(summary_csv, index=False)
    print(f"Rebuilt ensemble summary at: {summary_csv}")
    return summary


def build_metriplectic_table(summary: pd.DataFrame) -> pd.DataFrame:
    """Construct the (Re_eff, epsilon) dataset for the main figure.

    We focus on the ``N = 1000`` runs, which sit in the middle of the
    parameter scan and are representative of the large-\"N\" regime.
    The resulting table has columns

    - ``Re_eff``         : mean effective Reynolds number
    - ``rc``             : merger radius
    - ``eps_bind_mean``  : mean event/binding dissipation
    - ``eps_tot_mean``   : mean total dissipation
    """
    df = summary.copy()

    # Prefer the middle N as a representative slice.
    df_mid = df[df["N"] == 1000]
    if df_mid.empty:
        # Fall back to averaging over N if that slice is unavailable.
        df_mid = (
            df.groupby("rc", as_index=False)
            .agg(
                Re_eff_mean=("Re_eff_mean", "mean"),
                eps_bind_mean=("eps_bind_mean", "mean"),
                eps_tot_mean=("eps_tot_mean", "mean"),
            )
        )
    else:
        df_mid = df_mid[["Re_eff_mean", "rc", "eps_bind_mean", "eps_tot_mean"]]

    df_mid = df_mid.rename(columns={"Re_eff_mean": "Re_eff"})
    df_mid = df_mid.sort_values("Re_eff").reset_index(drop=True)
    return df_mid


def main() -> None:
    summary = load_or_build_summary()
    table = build_metriplectic_table(summary)
    out_csv = DATA_PROC / "dissipation_vs_Re_metriplectic.csv"
    table.to_csv(out_csv, index=False)
    print(f"Saved metriplectic dissipation table to: {out_csv}")


if __name__ == "__main__":
    main()
