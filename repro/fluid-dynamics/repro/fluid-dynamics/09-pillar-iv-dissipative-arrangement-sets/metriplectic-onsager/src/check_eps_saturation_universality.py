from __future__ import annotations

import pathlib

import matplotlib.pyplot as plt
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True, parents=True)


def main() -> None:
    summary_csv = DATA / "processed" / "epsilon_events_summary.csv"
    df = pd.read_csv(summary_csv)

    eps = df["eps_tot_mean"]
    eps_mean = eps.mean()
    eps_min = eps.min()
    eps_max = eps.max()

    print("=== Saturation universality check ===")
    print(f"Number of points         : {len(eps)}")
    print(f"eps_tot_mean (avg)       : {eps_mean:.6f}")
    print(f"min(eps_tot_mean)        : {eps_min:.6f}")
    print(f"max(eps_tot_mean)        : {eps_max:.6f}")
    print(f"relative spread (max-min): {(eps_max-eps_min)/eps_mean:.3%}")
    print()
    print(df[["N", "rc", "Re_eff_mean", "eps_tot_mean"]])

    fig, ax = plt.subplots(figsize=(6, 4))
    for N, grp in df.groupby("N"):
        ax.plot(
            grp["Re_eff_mean"],
            grp["eps_tot_mean"],
            "o-",
            label=rf"$N={N}$",
        )

    ax.set_xscale("log")
    ax.set_xlabel(r"Effective Reynolds Number ($Re_{\mathrm{eff}}$)")
    ax.set_ylabel(r"$\langle \varepsilon_{\mathrm{tot}} \rangle$")
    ax.set_title("Saturation robustness across $N$ and $r_c$")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)

    out_path = FIGURES / "eps_saturation_universality.png"
    fig.savefig(out_path, dpi=300)
    print(f"Saved universality figure to: {out_path}")


if __name__ == "__main__":
    main()
