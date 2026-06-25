# -*- coding: utf-8 -*-
"""
make_figure.py -- the build figure for Appendix H (deterministic, stdlib + numpy + matplotlib).

Three panels:
  (A) THE 4D BUILD SCHEDULE -- every module as a dot at (tau_on, system), coloured by system;
      the body filling module-by-module in spinodal-gamma order across developmental time, with
      the cumulative fill curve overlaid. (조금씩 조금씩 발달)
  (B) THE COUNT GRAMMAR G7 -- the inverse lever: serial count N ~ T/P vs clock period P, with the
      human point marked; halving P doubles N (count is the clock's integral, not gamma).
  (C) THE ASSEMBLY TREE -- the part-to-part graph rooted at the axial origin, drawn by depth
      (a body, not a pile of bricks).

Usage:  python3 make_figure.py
Writes: figures/build_overview.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from build import inventory, count, schedule, assembly, lock

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIG = os.path.join(_HERE, "figures")


def _color_map(systems):
    cmap = plt.get_cmap("tab20")
    return {s: cmap(i % 20) for i, s in enumerate(sorted(systems))}


def panel_schedule(ax):
    sched = schedule.module_schedule()
    systems = sorted({s["system"] for s in sched})
    colors = _color_map(systems)
    ypos = {s: i for i, s in enumerate(systems)}
    rng = np.random.RandomState(7)  # deterministic jitter
    for s in sched:
        y = ypos[s["system"]] + (rng.rand() - 0.5) * 0.6
        ax.scatter(s["tau_on"], y, s=14, color=colors[s["system"]],
                   edgecolors="none", alpha=0.8, zorder=3)
    ax.set_yticks(range(len(systems)))
    ax.set_yticks(range(len(systems)))
    ax.set_yticklabels(systems, fontsize=7)
    ax.set_xlabel("developmental time  tau_on  (spinodal-gamma order)", fontsize=8)
    ax.set_title("(A) the 4D build schedule: modules fill in gamma-order across tau",
                 fontsize=9, loc="left")
    ax.set_xlim(-0.03, 1.03)
    ax.grid(True, axis="x", ls=":", alpha=0.4)

    # cumulative fill curve on a twin axis
    fc = schedule.fill_curve(n_steps=40)
    ax2 = ax.twinx()
    ax2.plot([r["tau"] for r in fc], [r["fraction_present"] for r in fc],
             color="0.15", lw=1.6, zorder=4)
    ax2.set_ylabel("cumulative fraction of body present", fontsize=8)
    ax2.set_ylim(0, 1.02)


def panel_count(ax):
    cg = lock.count_grammar()
    P_human = cg["human_clock_period_min"]["value"]
    total_pairs = cg["human_somite_pairs_total"]["value"]
    T = total_pairs * P_human  # fixed window
    periods = np.linspace(P_human * 0.4, P_human * 2.2, 80)
    N = T / periods
    ax.plot(periods, N, color="#3b6", lw=2, zorder=2)
    # human point + the half/double lever points
    for fac, lbl in [(1.0, "human"), (0.5, "half P\n(2x count)"), (2.0, "2x P\n(0.5x count)")]:
        ax.scatter([P_human * fac], [T / (P_human * fac)], s=42, zorder=3,
                   color="#194", edgecolors="white")
        ax.annotate(lbl, (P_human * fac, T / (P_human * fac)),
                    textcoords="offset points", xytext=(6, 6), fontsize=7)
    ax.set_xlabel("segmentation-clock period  P  (min)", fontsize=8)
    ax.set_ylabel("serial count  N  ~  T_window / P", fontsize=8)
    ax.set_title("(B) the count grammar G7: N is the clock's integral (inverse lever), not gamma",
                 fontsize=9, loc="left")
    ax.grid(True, ls=":", alpha=0.4)


def panel_assembly(ax):
    g = assembly.graph()
    root = g["root"]
    edges = g["edges_child_to_parent"]
    nodes = set(edges.keys()) | set(edges.values()) | {root}

    # depth of each node (distance to root by parent links)
    def depth(n):
        d, cur, seen = 0, n, set()
        while cur != root and cur in edges and cur not in seen:
            seen.add(cur)
            cur = edges[cur]
            d += 1
        return d

    dep = {n: depth(n) for n in nodes}
    maxd = max(dep.values())
    # lay nodes out by depth column, spread vertically
    by_depth = {}
    for n in sorted(nodes):
        by_depth.setdefault(dep[n], []).append(n)
    pos = {}
    for d, ns in by_depth.items():
        for i, n in enumerate(sorted(ns)):
            y = (i - (len(ns) - 1) / 2.0)
            pos[n] = (d, y)
    # draw edges
    for child, parent in edges.items():
        if child in pos and parent in pos:
            x0, y0 = pos[child]
            x1, y1 = pos[parent]
            ax.plot([x1, x0], [y1, y0], color="0.7", lw=0.7, zorder=1)
    # draw nodes
    for n, (x, y) in pos.items():
        is_root = (n == root)
        ax.scatter([x], [y], s=80 if is_root else 26,
                   color="#c33" if is_root else "#36c",
                   edgecolors="white", zorder=2)
    ax.scatter([], [], color="#c33", label="axial root (%s)" % root)
    ax.scatter([], [], color="#36c", label="assembled part")
    ax.legend(fontsize=7, loc="upper right", framealpha=0.9)
    ax.set_xlabel("assembly depth from axial root", fontsize=8)
    ax.set_title("(C) the assembly tree: one connected body rooted at the axial origin "
                 "(not a pile)", fontsize=9, loc="left")
    ax.set_xlim(-0.5, maxd + 0.5)
    ax.set_yticks([])
    ax.grid(True, axis="x", ls=":", alpha=0.3)


def main():
    os.makedirs(_FIG, exist_ok=True)
    fig = plt.figure(figsize=(13, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], hspace=0.32, wspace=0.22)
    ax_a = fig.add_subplot(gs[0, :])
    ax_b = fig.add_subplot(gs[1, 0])
    ax_c = fig.add_subplot(gs[1, 1])
    panel_schedule(ax_a)
    panel_count(ax_b)
    panel_assembly(ax_c)

    summ = inventory.summary()
    fig.suptitle("Appendix H -- THE BUILD: %d buildable modules (%d bones derived = 206), "
                 "addressed -> counted -> sized -> assembled -> scheduled -> compiled (rigidified)"
                 % (summ["n_modules_named"], summ["bone_count_named"]),
                 fontsize=11, y=0.99)
    out = os.path.join(_FIG, "build_overview.png")
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("[wrote] %s" % out)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
