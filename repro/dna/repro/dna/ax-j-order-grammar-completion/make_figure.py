# -*- coding: utf-8 -*-
"""
make_figure.py -- the Appendix-J figure (deterministic; stdlib + numpy + matplotlib).

Three panels tell the COMPLETION story:
  (A) O1 FLOOR RE-TEST  -- the nested-scope ablation: inherited 38-kit (0.475, reproduces App I)
                           -> + limb FGF/Wnt inducers (~0.70) -> + full HOX collinear chains
                           (~0.755, FLOOR MET); HOX-only is below floor. The pre-registered 0.70
                           line + the +-1 rank jitter band show the lift needs BOTH fixes and is
                           honestly marginal at the lower edge ([L], not [V]).
  (B) FILLED DEPTH<->CARNEGIE -- cascade DEPTH vs Carnegie onset rank on the FILLED 63-gene atlas;
                           the new limb + HOX genes are marked; the trend now clears the floor.
  (C) THE QUORUM GATE   -- OR (k=1) and AND/threshold-k (k_i=indeg) wavefronts both respect the
                           cascade partial order (0 violations); sequence-derived drive sqrt(gamma)
                           preserves firing order. The OR-gate is the k=1 special case.

Usage:  python3 make_figure.py
Writes: figures/order_grammar_completion_overview.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from completion import lock, cascade, seqtools, nulltest, coupled

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIG = os.path.join(_HERE, "figures")

_INK = "#16263a"
_NULL = "#b23b3b"
_DISC = "#1f6f4f"
_LIMB = "#c8821a"
_HOX = "#6a4c93"
_FLOOR = "#b23b3b"
_OR = "#1f6f4f"
_AND = "#2b6cb0"


def panel_floor(ax):
    abl = nulltest.floor_retest_ablation()
    jit = nulltest.floor_retest_jitter()
    floor = abl["preregistered_absolute_floor"]
    keys = ["scope_a_inherited_kit", "scope_b_plus_limb_inducers",
            "scope_c_plus_full_hox", "scope_d_hox_only_limb_ablated"]
    labels = ["inherited\n38-kit", "+ limb\ninducers", "+ full HOX\n(FILLED)", "HOX only\n(limb ablated)"]
    vals = [abl[k]["spearman"] for k in keys]
    cols = ["#8a8f98", _LIMB, _DISC, _HOX]
    xs = np.arange(len(vals))
    ax.bar(xs, vals, color=cols, edgecolor=_INK, linewidth=0.7, width=0.66, zorder=3)
    # floor line
    ax.axhline(floor, color=_FLOOR, lw=1.6, ls="--", zorder=4)
    ax.text(len(vals) - 0.5, floor + 0.012, "pre-registered floor %.2f" % floor,
            ha="right", va="bottom", color=_FLOOR, fontsize=8.5)
    # jitter band on the FILLED bar (index 2)
    ax.errorbar(2, abl["scope_c_plus_full_hox"]["spearman"],
                yerr=[[abl["scope_c_plus_full_hox"]["spearman"] - jit["p5"]],
                      [jit["p95"] - abl["scope_c_plus_full_hox"]["spearman"]]],
                fmt="none", ecolor=_INK, elinewidth=1.3, capsize=5, zorder=5)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.018, "%.3f" % v, ha="center", va="bottom", fontsize=9, color=_INK)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 0.92)
    ax.set_ylabel("Spearman(depth, Carnegie rank)", fontsize=9)
    ax.set_title("(A) O1 floor RE-TEST: the lift needs BOTH fixes\n"
                 "filled kit %.3f vs %.3f inherited; jitter p5 %.3f (stays [L])"
                 % (abl["scope_c_plus_full_hox"]["spearman"],
                    abl["scope_a_inherited_kit"]["spearman"], jit["p5"]),
                 fontsize=10.5, color=_INK)


def panel_filled(ax):
    anc = lock.carnegie_anchor()
    dg = lock.driver_gamma()
    dgi = lock.driver_gamma_inherited()
    d = cascade.depth()
    genes = sorted(anc.keys())
    cr = np.array([anc[g]["rank"] for g in genes], float)
    dep = np.array([d[g] for g in genes], float)
    abl = nulltest.floor_retest_ablation()
    rho_all = abl["scope_c_plus_full_hox"]["spearman"]

    rng = np.random.RandomState(19)
    jit = (rng.rand(len(genes)) - 0.5) * 0.18
    for i, g in enumerate(genes):
        prog = dg[g].get("program", "")
        if prog == "hox_collinear":
            c, m, s = _HOX, "^", 60
        elif g not in dgi:  # a NEW non-HOX gene = limb inducer/outgrowth/aer
            c, m, s = _LIMB, "s", 56
        else:
            c, m, s = _DISC, "o", 46
        ax.scatter(dep[i] + jit[i], cr[i], s=s, c=c, marker=m,
                   edgecolors="white", linewidths=0.7, zorder=3)
    b, a = np.polyfit(dep, cr, 1)
    xs = np.linspace(dep.min(), dep.max(), 20)
    ax.plot(xs, b * xs + a, color=_DISC, lw=1.6, alpha=0.85, zorder=2)
    ax.set_title("(B) FILLED depth $\\to$ Carnegie (63 genes)\n"
                 "Spearman(depth, Carnegie) = %.3f $\\geq$ floor" % rho_all,
                 fontsize=10.5, color=_INK)
    ax.set_xlabel("cascade depth = #regulators in series upstream", fontsize=9)
    ax.set_ylabel("Carnegie onset rank (early $\\to$ late)", fontsize=9)
    ax.invert_yaxis()
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=_DISC, markersize=8,
                      label="inherited driver"),
               Line2D([0], [0], marker="s", color="w", markerfacecolor=_LIMB, markersize=8,
                      label="NEW limb FGF/Wnt"),
               Line2D([0], [0], marker="^", color="w", markerfacecolor=_HOX, markersize=8,
                      label="NEW HOX collinear")]
    ax.legend(handles=handles, fontsize=7.5, loc="lower right", framealpha=0.9)


def panel_gate(ax):
    """OR (k=1) vs AND/threshold-k (k_i=indeg) firing time vs cascade depth -- both respect the
    partial order. Sequence-drive preserves order (annotated)."""
    sim_or = coupled.simulate(gate_mode="or", drive_mode="uniform")
    sim_and = coupled.simulate(gate_mode="and", drive_mode="uniform", alpha=1.0)
    d = cascade.depth()
    genes = sorted(set(sim_or["fire_time"]) & set(sim_and["fire_time"]) & set(d))
    dep = np.array([d[g] for g in genes], float)
    t_or = np.array([sim_or["fire_time"][g] for g in genes], float)
    t_and = np.array([sim_and["fire_time"][g] for g in genes], float)

    rng = np.random.RandomState(19)
    jx = (rng.rand(len(genes)) - 0.5) * 0.16
    ax.scatter(dep + jx, t_or, s=42, c=_OR, marker="o", edgecolors="white",
               linewidths=0.6, zorder=3, label="OR gate (k=1)")
    ax.scatter(dep + jx, t_and, s=42, c=_AND, marker="D", edgecolors="white",
               linewidths=0.6, zorder=3, label="AND / threshold-k ($k_i$=indeg)")
    # trend lines
    for t, c in ((t_or, _OR), (t_and, _AND)):
        b, a = np.polyfit(dep, t, 1)
        xs = np.linspace(dep.min(), dep.max(), 20)
        ax.plot(xs, b * xs + a, color=c, lw=1.3, alpha=0.7, zorder=2)

    thr = coupled.threshold_k_wavefront(alpha=1.0)
    poc = coupled.or_partial_order_compliance()
    seq = coupled.sequence_drive_preserves_order()
    ax.set_title("(C) the QUORUM gate: order survives AND\n"
                 "OR %d viol., AND %d viol.; seq-drive order $\\rho$=%.3f"
                 % (poc["n_violations"], thr["n_violations"],
                    seq["spearman_order_uniform_vs_sequence"]),
                 fontsize=10.5, color=_INK)
    ax.set_xlabel("cascade depth (sources $\\to$ deepest)", fontsize=9)
    ax.set_ylabel("coupled-R19 firing time (a.u.)", fontsize=9)
    ax.legend(fontsize=7.8, loc="upper left", framealpha=0.9)


def main():
    os.makedirs(_FIG, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(15.8, 5.1))
    panel_floor(axes[0])
    panel_filled(axes[1])
    panel_gate(axes[2])
    for ax in axes:
        ax.grid(True, alpha=0.18, zorder=0)
    fig.suptitle("Appendix J -- the order-grammar COMPLETION: floor re-test (O1) + days (O2) + "
                 "sequence drive (O3) + quorum gate", fontsize=12.5, color=_INK, y=1.02)
    fig.tight_layout()
    out = os.path.join(_FIG, "order_grammar_completion_overview.png")
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
