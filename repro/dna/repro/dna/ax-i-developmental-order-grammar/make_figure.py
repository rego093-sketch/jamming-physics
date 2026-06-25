# -*- coding: utf-8 -*-
"""
make_figure.py -- the Appendix-I figure (deterministic; stdlib + numpy + matplotlib).

Three panels tell the whole story:
  (A) THE NULL      -- spinodal(gamma) vs Carnegie onset rank: a flat cloud. The single-locus
                       barrier does NOT order developmental staging (Spearman in the title).
  (B) THE DISCOVERY -- cascade DEPTH vs Carnegie onset rank: a rising trend. The linear axial
                       dependency chain (organizer->...->ossification) is highlighted and recovers
                       the order exactly; the named dilutors (limb-bud sources, HOX13) are marked.
  (C) THE CASCADE   -- the regulatory DAG drawn by depth (left=sources, right=deepest), every
                       cited edge pointing forward in Carnegie time (zero inversions).

Usage:  python3 make_figure.py
Writes: figures/order_grammar_overview.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from order import lock, cascade, seqtools, nulltest

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIG = os.path.join(_HERE, "figures")

_INK = "#16263a"
_NULL = "#b23b3b"
_DISC = "#1f6f4f"
_CHAIN = "#c8821a"
_EDGE = "#9bb0c2"


def _anchored():
    anc = lock.carnegie_anchor()
    dg = lock.driver_gamma()
    d = cascade.depth()
    genes = sorted(anc.keys())
    cr = np.array([anc[g]["rank"] for g in genes], float)
    spin = np.array([float(seqtools.spinodal(dg[g]["gamma"])) for g in genes], float)
    dep = np.array([d[g] for g in genes], float)
    return genes, cr, spin, dep


def panel_null(ax):
    genes, cr, spin, dep = _anchored()
    rho = nulltest.the_null()["spearman_spinodal_vs_carnegie"]
    ax.scatter(spin, cr, s=46, c=_NULL, edgecolors="white", linewidths=0.7, zorder=3)
    # least-squares guide line (visually flat)
    b, a = np.polyfit(spin, cr, 1)
    xs = np.linspace(spin.min(), spin.max(), 20)
    ax.plot(xs, b * xs + a, color=_NULL, lw=1.4, ls="--", alpha=0.7, zorder=2)
    ax.set_title("(A) the NULL: stiffness does not stage\nSpearman(spinodal $\\gamma$, Carnegie) = %.2f"
                 % rho, fontsize=10.5, color=_INK)
    ax.set_xlabel("spinodal($\\gamma$) = 2$(\\gamma/3)^{1.5}$  (single-locus key)", fontsize=9)
    ax.set_ylabel("Carnegie onset rank (early $\\to$ late)", fontsize=9)
    ax.invert_yaxis()


def panel_discovery(ax):
    genes, cr, spin, dep = _anchored()
    res = nulltest.absolute_strength_residual()
    chain = set(res["axial_chain"])
    dilutors = {"TBX4", "TBX5", "HOXA13", "HOXD13"}
    rho_all = res["spearman_depth_vs_carnegie_all"]
    rho_chain = res["spearman_depth_vs_carnegie_axial_chain"]

    rng = np.random.RandomState(19)
    jit = (rng.rand(len(genes)) - 0.5) * 0.18  # deterministic small x-jitter for overlapping ints
    for i, g in enumerate(genes):
        if g in chain:
            c, m, s, lab = _CHAIN, "o", 70, "axial chain ($\\rho$=%.2f)" % rho_chain
        elif g in dilutors:
            c, m, s, lab = "#8a8f98", "s", 52, "named dilutor"
        else:
            c, m, s, lab = _DISC, "o", 46, "other anchored"
        ax.scatter(dep[i] + jit[i], cr[i], s=s, c=c, marker=m,
                   edgecolors="white", linewidths=0.7, zorder=3)
    b, a = np.polyfit(dep, cr, 1)
    xs = np.linspace(dep.min(), dep.max(), 20)
    ax.plot(xs, b * xs + a, color=_DISC, lw=1.6, alpha=0.8, zorder=2)
    ax.set_title("(B) the DISCOVERY: cascade DEPTH stages\nSpearman(depth, Carnegie) = %.2f (all)"
                 % rho_all, fontsize=10.5, color=_INK)
    ax.set_xlabel("cascade depth = #regulators in series upstream", fontsize=9)
    ax.set_ylabel("Carnegie onset rank (early $\\to$ late)", fontsize=9)
    ax.invert_yaxis()
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=_CHAIN, markersize=8,
                      label="axial chain ($\\rho$=%.2f)" % rho_chain),
               Line2D([0], [0], marker="o", color="w", markerfacecolor=_DISC, markersize=8,
                      label="other anchored"),
               Line2D([0], [0], marker="s", color="w", markerfacecolor="#8a8f98", markersize=8,
                      label="named dilutor (limb / HOX13)")]
    ax.legend(handles=handles, fontsize=7.5, loc="lower right", framealpha=0.9)


def panel_cascade(ax):
    anc = lock.carnegie_anchor()
    dg = lock.driver_gamma()
    d = cascade.depth()
    genes = sorted(dg.keys())
    # layout: x = depth, y = stable per-layer slot
    layers = {}
    for g in genes:
        layers.setdefault(d[g], []).append(g)
    pos = {}
    for depth_val, gs in layers.items():
        gs = sorted(gs)
        for j, g in enumerate(gs):
            y = j - (len(gs) - 1) / 2.0
            pos[g] = (depth_val, y)

    # edges (only those among atlas genes), forward in depth
    for p, c, _ in lock.cascade_edges():
        if p in pos and c in pos:
            x0, y0 = pos[p]; x1, y1 = pos[c]
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle="-|>", color=_EDGE, lw=0.7, alpha=0.8),
                        zorder=1)
    # nodes: colour anchored genes by Carnegie rank, others grey
    for g in genes:
        x, y = pos[g]
        if g in anc:
            cval = anc[g]["rank"]
            sc = ax.scatter(x, y, s=58, c=[cval], cmap="viridis", vmin=1, vmax=11,
                            edgecolors=_INK, linewidths=0.5, zorder=3)
        else:
            ax.scatter(x, y, s=34, c="#d7dee6", edgecolors=_INK, linewidths=0.4, zorder=2)
    ax.set_title("(C) the cascade DAG by depth\nevery cited edge points forward in Carnegie time "
                 "(0 inversions)", fontsize=10.5, color=_INK)
    ax.set_xlabel("cascade depth (sources $\\to$ deepest)", fontsize=9)
    ax.set_yticks([])
    cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.02)
    cbar.set_label("Carnegie rank", fontsize=8)


def main():
    os.makedirs(_FIG, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.1))
    panel_null(axes[0])
    panel_discovery(axes[1])
    panel_cascade(axes[2])
    for ax in axes[:2]:
        ax.grid(True, alpha=0.18, zorder=0)
    fig.suptitle("Appendix I -- the developmental ORDER grammar: emergence order = toposort(cascade) "
                 "modulated by barrier $\\gamma^2/4$",
                 fontsize=12.5, color=_INK, y=1.02)
    fig.tight_layout()
    out = os.path.join(_FIG, "order_grammar_overview.png")
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
