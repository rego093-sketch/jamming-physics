# -*- coding: utf-8 -*-
"""
make_figure.py -- the Appendix-L figure (deterministic; stdlib + numpy + matplotlib).

Two panels tell the close-out story:
  (A) B4 -- THE JITTER FLOOR CLOSES. The +-1 Carnegie-rank jitter distribution of Spearman(cascade
      depth, jittered rank), seed 19, on the K cascade (62 edges; PAX7 an artificial source) vs the
      L cascade (63 edges; + the cited MEOX1->PAX7 source-fix). The K p5 sits BELOW the 0.70 floor
      (marginal); the L p5 sits ABOVE it (jitter-robust). The strength stays [L], never [V].
  (B) B2 -- THE DRIVE IS NOT IN THE PROMOTER (DATA-BLOCKED). Per-edge motif-occupancy z-score of the
      cited parent-TF motif in the child promoter vs a dinucleotide-shuffle null. Most edges sit at/
      below background; the canonical SOX9 -| RUNX2 edge is BELOW background -- the per-edge drive
      lives in distal enhancers the +-2 kb gamma window does not contain.

Usage:  python3 make_figure.py
Writes: figures/blueprint_closeout_overview.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from completion import lock, cascade, nulltest, cis

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIG = os.path.join(_HERE, "figures")

_INK = "#16263a"
_KCOL = "#c8821a"      # K (before, marginal)
_LCOL = "#1f6f4f"      # L (after, closed)
_FLOOR = "#b23b3b"
_ABOVE = "#2b6cb0"
_BELOW = "#9aa6b2"
_CANON = "#b23b3b"


def _spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = a.argsort().argsort().astype(float); rb = b.argsort().argsort().astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    d = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / d) if d > 0 else 0.0


def _depth_on(gene_set, edges):
    genes = set(gene_set)
    adj = {g: [] for g in genes}; rev = {g: [] for g in genes}; indeg = {g: 0 for g in genes}
    for p, c, _ in edges:
        if p in genes and c in genes:
            adj[p].append(c); rev[c].append(p); indeg[c] += 1
    q = sorted([g for g in genes if indeg[g] == 0]); topo = []; ind = dict(indeg)
    while q:
        n = q.pop(0); topo.append(n)
        for c in sorted(adj[n]):
            ind[c] -= 1
            if ind[c] == 0:
                q.append(c)
        q.sort()
    d = {g: 0 for g in genes}
    for n in topo:
        for p in rev[n]:
            if d[p] + 1 > d[n]:
                d[n] = d[p] + 1
    return d


def _jitter_dist(depth_map):
    cfg = lock.floor_robustness_cfg()
    jitter = int(cfg["rank_jitter"]); n = int(cfg["n_draws"]); seed = int(cfg["seed"])
    anc = lock.carnegie_anchor(); genes = sorted(anc.keys())
    base = np.array([anc[g]["rank"] for g in genes], float)
    dep = np.array([depth_map[g] for g in genes], float)
    rng = np.random.default_rng(seed)
    vals = np.empty(n)
    for i in range(n):
        jr = base + rng.integers(-jitter, jitter + 1, size=base.size)
        vals[i] = _spearman(dep, jr)
    return vals


def panel_b4(ax):
    floor = lock.cascade_floor()
    genes = set(lock.driver_gamma().keys())
    rc = lock.DB["regulatory_cascade"]
    ei = rc["edges_inherited"]; el = rc["edges_limb_induction"]
    eh = rc["edges_hox_collinear"]; em = rc.get("edges_myogenic_upstream", [])
    dK = _depth_on(genes, ei + el + eh)             # K: 62 edges (PAX7 a source)
    dL = _depth_on(genes, ei + el + eh + em)        # L: 63 edges (+ MEOX1->PAX7)
    vK = _jitter_dist(dK); vL = _jitter_dist(dL)
    p5K = np.percentile(vK, 5); p5L = np.percentile(vL, 5)

    bins = np.linspace(0.45, 1.0, 46)
    ax.hist(vK, bins=bins, color=_KCOL, alpha=0.55, label="K (62 edges; PAX7 a source)")
    ax.hist(vL, bins=bins, color=_LCOL, alpha=0.55, label="L (+ cited MEOX1->PAX7)")
    ax.axvline(floor, color=_FLOOR, lw=2.0, ls="--", zorder=5)
    ax.text(floor, ax.get_ylim()[1] * 0.96, " 0.70 floor", color=_FLOOR, fontsize=8.5,
            va="top", ha="left", rotation=90)
    ax.axvline(p5K, color=_KCOL, lw=1.8, ls=":")
    ax.axvline(p5L, color=_LCOL, lw=1.8, ls=":")
    ax.annotate("K p5 %.3f\n(below floor)" % p5K, xy=(p5K, ax.get_ylim()[1] * 0.5),
                xytext=(p5K - 0.13, ax.get_ylim()[1] * 0.62), color=_KCOL, fontsize=8,
                ha="center", arrowprops=dict(arrowstyle="->", color=_KCOL, lw=1.2))
    ax.annotate("L p5 %.3f\n(clears floor)" % p5L, xy=(p5L, ax.get_ylim()[1] * 0.5),
                xytext=(p5L + 0.10, ax.get_ylim()[1] * 0.72), color=_LCOL, fontsize=8,
                ha="center", arrowprops=dict(arrowstyle="->", color=_LCOL, lw=1.2))
    ax.set_xlabel("Spearman(cascade depth, +-1 jittered Carnegie rank)", fontsize=9)
    ax.set_ylabel("jitter draws (seed 19, n=%d)" % len(vK), fontsize=9)
    ax.set_title("(A)  B4 -- the jitter floor closes (PAX7 source-fix)",
                 fontsize=10.5, color=_INK, loc="left", weight="bold")
    ax.legend(fontsize=7.8, loc="upper left", framealpha=0.9)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def panel_b2(ax):
    b2 = cis.occupancy_probe()
    rows = b2["rows"]
    labels = ["%s->%s" % (r["parent"], r["child"]) for r in rows]
    zs = [r["z"] for r in rows]
    y = np.arange(len(rows))
    colors = []
    for r in rows:
        if (r["parent"], r["child"]) == ("SOX9", "RUNX2"):
            colors.append(_CANON)
        elif r["above_background"]:
            colors.append(_ABOVE)
        else:
            colors.append(_BELOW)
    ax.barh(y, zs, color=colors, height=0.7)
    ax.axvline(0.0, color=_INK, lw=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=6.6)
    ax.invert_yaxis()
    ax.set_xlabel("motif-occupancy z vs dinucleotide-shuffle null", fontsize=9)
    ax.set_title("(B)  B2 -- drive NOT in the +-2 kb promoter (data-blocked)",
                 fontsize=10.5, color=_INK, loc="left", weight="bold")
    handles = [Patch(color=_ABOVE, label="above background"),
               Patch(color=_BELOW, label="at/below background"),
               Patch(color=_CANON, label="SOX9 -| RUNX2 (canonical, below)")]
    ax.legend(handles=handles, fontsize=7.2, loc="lower right", framealpha=0.9)
    ax.text(0.02, 0.02, "%d/%d above background; mean z %.2f"
            % (b2["n_above_background"], b2["n_edges_scored"], b2["mean_z"]),
            transform=ax.transAxes, fontsize=7.6, color=_INK, va="bottom", ha="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def main():
    os.makedirs(_FIG, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 5.4))
    panel_b4(ax1)
    panel_b2(ax2)
    fig.suptitle("Appendix L -- the blueprint close-out: B4 closed (jitter-robust [L]); "
                 "B2 data-blocked ([F], distal data required)",
                 fontsize=11.5, color=_INK, weight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out = os.path.join(_FIG, "blueprint_closeout_overview.png")
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print("wrote:", out)


if __name__ == "__main__":
    main()
