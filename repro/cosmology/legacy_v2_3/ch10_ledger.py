#!/usr/bin/env python3
"""
ch10_ledger.py -- Renders the honest-ledger synthesis figure (Chapter 10, ch10_ledger.png).

SYNTHESIS, not a new simulation: it lays out every result of the volume by status
(foundational/solid; degenerate consistency checks; distinguishing & testable; the sharpest
tension) and boxes the three falsifiable predictions. The underlying NUMBERS are produced by the
per-chapter scripts (see README_REPRODUCIBILITY_MAP.md); this script only renders the classification.
DEPENDENCIES: matplotlib.
"""
def main():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    cats = [
        ("Foundational / solid", "#1C7C3B", [
            r"Inflow input $\nu_p=3\pi^4$ (anchor)",
            r"Speed emergence $c^2=K/\rho$ ($R^2=1$)",
            r"Gravity $1/r^2$, equivalence principle",
            r"Intrinsic spin & tidal locking",
            r"CMB mechanism (present thermal emission)",
            r"Black holes (critical inflow, no singularity)"]),
        ("Degenerate consistency checks", "#185FA5", [
            r"Planetary orbits, Kepler $T^2/a^3=1.00001$",
            r"Supernova Hubble diagram (no dark energy needed)",
            r"NGC 2403 rotation curve ($\Upsilon=0.567$, $\chi^2$/dof$=1.99$)"]),
        ("Distinguishing & testable", "#C9A227", [
            r"$a_0=cH_0/2\pi$ (derived, 90% of empirical)",
            r"Angular-size minimum $z=e-1\approx1.72$",
            r"Dark matter as vacuum deficit (tracks baryons)"]),
        ("Sharpest tension (open)", "#C0392B", [
            r"Vacuum dispersion vs Fermi GRB (8-15 orders)",
            r"reframed by the angle account as an open dynamical item"]),
    ]
    preds = [
        r"P1  $a_0$ tracks $cH(z)$: environment / epoch dependence (vs constant $a_0$)",
        r"P2  gas-coincident dark cores in post-merger clusters (vs collisionless CDM)",
        r"P3  jet axis = spin axis; degree-scale collimation needs $a_k\lesssim0.008$",
    ]
    fig, ax = plt.subplots(figsize=(12.9, 8.5)); ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(-0.35, 12.2)
    ax.text(0.2, 11.9, "The honest ledger of the volume", fontsize=15, weight="bold")
    y = 11.3
    for title, color, items in cats:
        ax.add_patch(FancyBboxPatch((0.2, y-0.16), 9.6, 0.5, boxstyle="round,pad=0.02",
                                    fc=color, ec="none", alpha=0.92))
        ax.text(0.38, y+0.09, title, fontsize=12, color="white", weight="bold", va="center")
        y -= 0.72
        for it in items:
            ax.text(0.62, y, u"\u2022  " + it, fontsize=10, va="center", color="#222222")
            y -= 0.43
        y -= 0.22
    ax.add_patch(FancyBboxPatch((0.2, y-1.82), 9.6, 1.74, boxstyle="round,pad=0.03",
                                fc="none", ec="#222222", lw=1.6))
    ax.text(0.38, y-0.32, "Three falsifiable predictions", fontsize=12, weight="bold", color="#222222")
    yy = y-0.74
    for p in preds:
        ax.text(0.55, yy, p, fontsize=9.5, color="#222222"); yy -= 0.42
    plt.tight_layout(); plt.savefig("ch10_ledger.png", dpi=125, bbox_inches="tight"); plt.close()
    print("[figure written: ch10_ledger.png] -- honest-ledger synthesis (Chapter 10).")
    print("Classification only; the underlying numbers come from the per-chapter scripts.")

if __name__ == "__main__":
    main()
