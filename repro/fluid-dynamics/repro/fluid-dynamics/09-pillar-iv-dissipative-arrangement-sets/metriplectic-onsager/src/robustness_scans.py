"""Robustness helper utilities for the metriplectic vortex model.

This module has two roles:

1. Provide a small convenience function :func:`summarize_ensemble` that
   reduces an ensemble of metriplectic runs to a table of means and
   standard deviations suitable for plotting.
2. Expose a command-line entry point that rebuilds the processed
   summary file ``data/processed/epsilon_events_summary.csv`` from the
   raw ensemble data in ``data/raw/epsilon_events_ensemble.csv``.

The raw CSV shipped with the reproducibility package was generated
offline using the production ADG solver described in the Letter.  The
functions here are intentionally lightweight and contain *no* heavy
numerics; they merely reorganise that data.  Users who wish to plug in
their own metriplectic integrator can regenerate the raw file and then
reuse the summarisation logic below.
"""

from __future__ import annotations

import pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA_RAW = DATA / "raw"
DATA_PROC = DATA / "processed"
DATA_PROC.mkdir(parents=True, exist_ok=True)


def summarize_ensemble(df: pd.DataFrame) -> pd.DataFrame:
    """Compute ensemble statistics for (N, r_c) bins.

    The input ``df`` is expected to contain at least the columns

    - ``N``          : number of vortices in the run
    - ``rc``         : merger radius used in that run
    - ``Re_eff``     : effective Reynolds number
    - ``eps_bind``   : event/binding dissipation rate
    - ``eps_tot``    : total dissipation rate
    - ``n_mergers``  : total number of merger events

    The output aggregates over random seeds and returns a tidy table
    with mean and standard deviation of the key diagnostics.
    """
    grouped = (
        df.groupby(["N", "rc"], as_index=False)
        .agg(
            Re_eff_mean=("Re_eff", "mean"),
            eps_bind_mean=("eps_bind", "mean"),
            eps_bind_std=("eps_bind", "std"),
            eps_tot_mean=("eps_tot", "mean"),
            eps_tot_std=("eps_tot", "std"),
            n_mergers_mean=("n_mergers", "mean"),
        )
        .sort_values(["N", "rc"])
    )
    return grouped


def main_from_existing() -> None:
    """Rebuild the processed ensemble summary from the bundled raw CSV.

    This is the entry point used in the README.  It does *not* run any
    new simulations; it simply recomputes the statistics in case the
    user has modified or regenerated the raw data file.
    """
    csv = DATA_RAW / "epsilon_events_ensemble.csv"
    if not csv.exists():
        raise FileNotFoundError(
            f"Raw ensemble file not found: {csv}\n"
            "This package ships with a pre-computed ensemble.\n"
            "If you have replaced it with your own data, please make "
            "sure to save it under this path and rerun this command."
        )

    df = pd.read_csv(csv)
    summary = summarize_ensemble(df)
    out = DATA_PROC / "epsilon_events_summary.csv"
    summary.to_csv(out, index=False)
    print(f"Saved ensemble summary to: {out}")


if __name__ == "__main__":
    main_from_existing()
