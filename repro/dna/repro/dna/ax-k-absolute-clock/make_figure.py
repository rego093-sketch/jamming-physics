# -*- coding: utf-8 -*-
"""
make_figure.py -- the Appendix-K figure (deterministic; stdlib + numpy + matplotlib).

Two panels tell the ABSOLUTE-CLOCK (B1) story:
  (A) THE TWO-ANCHOR CLOCK -- day(s) = a + b*s. The SLOPE b comes from the in-vitro segmentation
      oscillator (5 h x 42 somites / 24, spread over CS9->CS13); the INTERCEPT a from the in-vivo
      first-heartbeat landmark (CS10 @ 22 d). ZERO free parameters. The cited Carnegie stage-days
      are HELD-OUT points (none used to fit either anchor); the line reproduces them to <= 0.6 d
      within the somite-clock window. The post-somitogenesis region (CS14+) is shaded -- the single
      somite-rate drifts there, reported, not hidden.
  (B) HELD-OUT GENE DAYS -- predicted vs cited stage-day for every anchored gene. The somite-window
      genes (held out) land on the identity line inside the +-1.5 d acceptance band; the CS14+ genes
      drift off it, the same honest bound.

Usage:  python3 make_figure.py
Writes: figures/absolute_clock_overview.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from completion import lock, timing

_HERE = os.path.dirname(os.path.abspath(__file__))
_FIG = os.path.join(_HERE, "figures")

_INK = "#16263a"
_SEG = "#2b6cb0"      # segmentation modality (slope)
_CARD = "#b23b3b"     # cardiac modality (intercept)
_LINE = "#1f6f4f"     # the calibration line
_INWIN = "#1f6f4f"    # in somite-clock window
_LATE = "#c8821a"     # post-somitogenesis (CS14+)
_BAND = "#1f6f4f"


def panel_clock(ax):
    gc = timing.global_clock()
    cfg = lock.absolute_clock_cfg()
    a = gc["calibration"]["intercept_a_days"]
    b = gc["calibration"]["slope_b_days_per_stage"]
    vlo, vhi = cfg["validated_window_cs"]
    zp_s, zp_d = cfg["zero_point_stage_cs"], cfg["zero_point_day"]
    accept = cfg["heldout_accept_days"]

    rows = gc["heldout_stage_validation"]["rows"]
    stages = np.array([r["stage_num"] for r in rows], float)
    cited = np.array([r["cited_day"] for r in rows], float)
    smax = stages.max()

    # shade the post-somitogenesis region (CS14+), where the single rate drifts
    ax.axvspan(vhi + 0.5, smax + 0.6, color=_LATE, alpha=0.08, zorder=0)
    ax.text(vhi + 0.6, 19.5, "post-somitogenesis\n(CS14+): single rate drifts",
            fontsize=7.6, color=_LATE, va="bottom", ha="left")

    # the calibration line
    xs = np.linspace(stages.min() - 0.2, smax + 0.4, 50)
    ax.plot(xs, a + b * xs, color=_LINE, lw=1.8, zorder=2,
            label="clock: day = %.3f + %.4f*s" % (a, b))
    # +-accept band around the line
    ax.fill_between(xs, a + b * xs - accept, a + b * xs + accept,
                    color=_BAND, alpha=0.10, zorder=1)

    # cited Carnegie days: held-out (in window) vs late
    for r in rows:
        s, c = r["stage_num"], r["cited_day"]
        if r["stage_num"] == zp_s:
            continue
        col = _INWIN if r["in_somite_window"] else _LATE
        ax.scatter(s, c, s=58, c=col, marker="o", edgecolors="white",
                   linewidths=0.8, zorder=4)
    # the two anchors, emphasised
    ax.scatter(zp_s, zp_d, s=200, marker="*", c=_CARD, edgecolors="white",
               linewidths=1.0, zorder=6)
    ax.annotate("cardiac INTERCEPT\nfirst heartbeat CS10 @ 22 d (in-vivo)",
                xy=(zp_s, zp_d), xytext=(zp_s - 0.3, zp_d + 5.2), fontsize=8, color=_CARD,
                ha="left", va="bottom",
                arrowprops=dict(arrowstyle="->", color=_CARD, lw=1.1))
    # slope source annotation (segmentation), drawn over the CS9->CS13 bracket
    ax.annotate("", xy=(vhi, a + b * vhi), xytext=(vlo, a + b * vlo),
                arrowprops=dict(arrowstyle="<->", color=_SEG, lw=2.0))
    ax.text((vlo + vhi) / 2.0, a + b * ((vlo + vhi) / 2.0) - 2.6,
            "segmentation SLOPE\n8.75 d over CS9->CS13 (in-vitro)",
            fontsize=8, color=_SEG, ha="center", va="top")

    ax.set_title("(A) the two-anchor absolute clock: 0 free parameters\n"
                 "held-out Carnegie days reproduced to <= %.2f d in the somite window"
                 % gc["heldout_stage_validation"]["max_abs_err_days"],
                 fontsize=10.5, color=_INK)
    ax.set_xlabel("Carnegie stage number s", fontsize=9)
    ax.set_ylabel("post-fertilization day", fontsize=9)
    handles = [
        Line2D([0], [0], color=_LINE, lw=1.8, label="calibration line (2 measured anchors)"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor=_CARD, markersize=15,
               label="cardiac anchor (intercept)"),
        Line2D([0], [0], color=_SEG, lw=2.0, label="segmentation anchor (slope)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=_INWIN, markersize=8,
               label="held-out cited day (somite window)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=_LATE, markersize=8,
               label="cited day (CS14+, drift)"),
        Patch(facecolor=_BAND, alpha=0.10, label="+- %.1f d acceptance band" % accept),
    ]
    ax.legend(handles=handles, fontsize=7.0, loc="lower right", framealpha=0.92)
    ax.grid(True, alpha=0.18, zorder=0)


def panel_genes(ax):
    gc = timing.global_clock()
    cfg = lock.absolute_clock_cfg()
    a = gc["calibration"]["intercept_a_days"]
    b = gc["calibration"]["slope_b_days_per_stage"]
    vlo, vhi = cfg["validated_window_cs"]
    accept = cfg["heldout_accept_days"]

    anc = lock.carnegie_anchor()
    days = lock.carnegie_stage_days()
    rng = np.random.RandomState(19)

    pred_in, cited_in, pred_lt, cited_lt = [], [], [], []
    for g, rec in anc.items():
        s = int(rec["cs_approx"])
        cs = "CS%d" % s
        if cs not in days:
            continue
        p = a + b * s
        c = days[cs] + (rng.rand() - 0.5) * 0.5   # tiny jitter so co-staged genes separate
        if vlo <= s <= vhi:
            pred_in.append(p); cited_in.append(c)
        else:
            pred_lt.append(p); cited_lt.append(c)

    lo = min(min(pred_in + pred_lt), min(cited_in + cited_lt)) - 1.5
    hi = max(max(pred_in + pred_lt), max(cited_in + cited_lt)) + 1.5
    xs = np.linspace(lo, hi, 50)
    # identity line + acceptance band
    ax.plot(xs, xs, color=_INK, lw=1.3, ls="--", zorder=2, label="predicted = cited")
    ax.fill_between(xs, xs - accept, xs + accept, color=_BAND, alpha=0.10, zorder=1,
                    label="+- %.1f d band" % accept)

    ax.scatter(pred_in, cited_in, s=46, c=_INWIN, marker="o", edgecolors="white",
               linewidths=0.6, zorder=4, label="somite-window genes (n=%d, held out)" % len(pred_in))
    ax.scatter(pred_lt, cited_lt, s=46, c=_LATE, marker="s", edgecolors="white",
               linewidths=0.6, zorder=4, label="CS14+ genes (n=%d, drift)" % len(pred_lt))

    ax.set_title("(B) held-out GENE days: predicted vs cited\n"
                 "%d somite-window genes within the band (max %.2f d)"
                 % (gc["heldout_gene_validation"]["n_genes"],
                    gc["heldout_gene_validation"]["max_abs_err_days"]),
                 fontsize=10.5, color=_INK)
    ax.set_xlabel("predicted day  (clock: a + b*stage)", fontsize=9)
    ax.set_ylabel("cited day  (Carnegie stage-day table)", fontsize=9)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_aspect("equal", adjustable="box")
    ax.legend(fontsize=7.2, loc="upper left", framealpha=0.92)
    ax.grid(True, alpha=0.18, zorder=0)


def main():
    os.makedirs(_FIG, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.6))
    panel_clock(axes[0])
    panel_genes(axes[1])
    fig.suptitle("Appendix K -- the absolute clock (B1): two independent measured anchors pin the "
                 "global zero-point; held-out days reproduced [L], never [V]",
                 fontsize=11.5, color=_INK, y=1.02)
    fig.tight_layout()
    out = os.path.join(_FIG, "absolute_clock_overview.png")
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
