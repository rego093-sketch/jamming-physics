from __future__ import annotations

"""Plot the dissipation saturation figure used in the Letter.

This script expects the following CSV files:

- ``data/processed/dissipation_vs_Re_metriplectic.csv``:
    built by :mod:`src.parameter_sweep` from the metriplectic ensemble.
- ``NS_reference/viscous_dissipation_vs_Re.csv``:
    built by :mod:`NS_reference.generate_viscous_data` (a modest
    pseudo-spectral Navier--Stokes solver) or supplied as part of the
    archive.

Running this module regenerates ``figures/dissipation_saturation.png``.
"""

import pathlib
import pandas as pd
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA_PROCESSED = DATA / "processed"
FIGURES = ROOT / "figures"
NS_REF = ROOT / "NS_reference"
FIGURES.mkdir(parents=True, exist_ok=True)


def _load_metriplectic() -> pd.DataFrame:
    csv = DATA_PROCESSED / "dissipation_vs_Re_metriplectic.csv"
    if not csv.exists():
        # Build it from the ensemble summary.
        from . import parameter_sweep

        parameter_sweep.main()
    return pd.read_csv(csv)


def _load_ns_reference() -> pd.DataFrame:
    csv = NS_REF / "viscous_dissipation_vs_Re.csv"
    if not csv.exists():
        raise FileNotFoundError(
            f"Navier–Stokes reference file not found: {csv}\n"
            "You can regenerate it by running\n"
            "    python NS_reference/generate_viscous_data.py"
        )
    return pd.read_csv(csv)


def main() -> None:
    df_m = _load_metriplectic()
    df_ns = _load_ns_reference()

    fig, ax = plt.subplots(figsize=(6, 4))

    # 64^2 Navier–Stokes reference (laptop-friendly demo)
    ax.plot(
        df_ns["Re_eff"],
        df_ns["eps_nu"],
        "o--",
        label=r"$\varepsilon_\nu$ (Navier--Stokes, $64^2$)",
    )

    # Optional high-resolution Navier–Stokes overlays (256^2, 512^2)
    for N, marker in [(256, "d-"), (512, "x-")]:
        csv_hi = NS_REF / f"viscous_dissipation_vs_Re_highres_{N}.csv"
        if csv_hi.exists():
            df_hi = pd.read_csv(csv_hi)
            ax.plot(
                df_hi["Re_eff"],
                df_hi["eps_nu"],
                marker,
                label=rf"$\varepsilon_\nu$ (NS, {N}^2)",
            )

    # Event / binding dissipation from the metriplectic model
    ax.plot(
        df_m["Re_eff"],
        df_m["eps_bind_mean"],
        "s-",
        label=r"$\varepsilon_{\mathrm{bind}}$ (events)",
    )

    # Total dissipation (if available)
    if "eps_tot_mean" in df_m.columns:
        ax.plot(
            df_m["Re_eff"],
            df_m["eps_tot_mean"],
            "^-",
            label=r"$\varepsilon_{\mathrm{tot}}$ (total)",
        )

    ax.set_xscale("log")
    ax.set_xlabel(r"Effective Reynolds Number ($Re_{\mathrm{eff}}$)")
    ax.set_ylabel(r"Dissipation Rate ($\varepsilon$)")
    ax.set_title("Onsager Anomaly: Dissipation Saturation")
    ax.legend(loc="lower left")
    ax.grid(True, which="both", alpha=0.3)

    fig.tight_layout()
    out_path = FIGURES / "dissipation_saturation.png"
    fig.savefig(out_path, dpi=300)
    print(f"Saved figure to: {out_path}")


if __name__ == "__main__":
    main()
