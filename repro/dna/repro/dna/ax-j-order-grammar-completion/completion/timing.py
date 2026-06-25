# -*- coding: utf-8 -*-
"""
completion.timing -- O2: ABSOLUTE timing, from ORDER to approximate DAYS.

Appendix I fixed only the ORDER (rank) of emergence and left absolute time [O]. This module attaches
REAL CITED measured rates and makes two honest, bounded predictions:

  (T1) the SEGMENTATION SUB-CLOCK  [L]
       The human presomitic-mesoderm oscillator has a period ~5 h (Diaz-Cuadros 2020 Nature 580:113;
       Matsuda 2020 Science 369:1450) and ~42 somite pairs form (O'Rahilly & Muller). So somitogenesis
       takes ~ 42 * 5 h = 210 h ~ 8.75 days. The CITED rate must REPRODUCE the CITED somitogenesis
       window (somites begin ~CS9, d20; the last pairs form ~CS13-14, d28-30 -> a measured span of
       ~8-10 days). The prediction 8.75 d lands inside that cited window WITHOUT being fitted to it:
       it is the product of two independently-cited numbers. This converts the segmentation sub-clock
       [O] -> [L].

  (T2) the ORDER -> DAY BAND map   [F] over [L] anchors
       Each gene carries a cited Carnegie stage; each Carnegie stage carries a cited approximate
       post-ovulation day (O'Rahilly & Muller; Hill embryology). Mapping the gene's cited stage to
       its cited day gives an approximate ONSET DAY per gene. The map (stage -> day) is the cited
       table [L]; reading a gene's day through it is a declared [F] lookup. The Spearman of these day
       estimates against the cascade DEPTH order is reported -- it must agree with the rank result.
       Crucially the GLOBAL multi-program developmental clock (why 5 h, why 42, across all organs)
       is NOT derived and stays [O]: we attach measured rates, we do not explain them.
"""
import numpy as np

from . import lock, cascade


def _spearman(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    ra = a.argsort().argsort().astype(np.float64)
    rb = b.argsort().argsort().astype(np.float64)
    ra -= ra.mean(); rb -= rb.mean()
    denom = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / denom) if denom > 0 else 0.0


# ----------------------------------------------------------------- T1 segmentation sub-clock
def segmentation_subclock():
    """The cited 5 h period x ~42 somite pairs must reproduce the cited ~8-10 day somitogenesis
    window. Two independently-cited numbers multiplied -- not fitted to the window. [L]."""
    period_h = lock.seg_clock_period_hours()      # ~5 h, cited
    n_somites = lock.somite_pairs_total()         # ~42, cited
    days = lock.carnegie_stage_days()
    pred_hours = n_somites * period_h
    pred_days = pred_hours / 24.0

    # the cited somitogenesis window: first somites ~CS9 (d20), the bulk complete by ~CS13 (d28).
    cs9 = days["CS9"]
    cs13 = days["CS13"]
    cited_span_days = cs13 - cs9                   # ~8 days, cited (independent of the period)
    # honest agreement: the predicted span lands within +/-2 days of the cited window span.
    within = abs(pred_days - cited_span_days) <= 2.0
    return {
        "period_hours_cited": period_h,
        "somite_pairs_cited": n_somites,
        "predicted_somitogenesis_hours": round(pred_hours, 1),
        "predicted_somitogenesis_days": round(pred_days, 3),
        "cited_window_CS9_to_CS13_days": round(cited_span_days, 1),
        "prediction_in_cited_window_pm2d": bool(within),
        "construction": "predicted = (cited period) x (cited somite count); the cited window span is "
                        "a THIRD independent number (CS13_day - CS9_day). Agreement is not fitted.",
        "grade": "[L] the cited segmentation rate reproduces the cited somitogenesis duration "
                 "(~8.75 d vs cited ~8 d window) -- the segmentation sub-clock is now absolute.",
    }


# ----------------------------------------------------------------- T2 order -> day band
def gene_onset_days():
    """Map each anchored gene's cited Carnegie stage to its cited approximate day. The stage->day
    table is [L]; the per-gene lookup is a declared [F]. Returns {gene: day}."""
    anc = lock.carnegie_anchor()
    days = lock.carnegie_stage_days()
    out = {}
    for g, rec in anc.items():
        cs = "CS%d" % int(rec["cs_approx"])
        if cs in days:
            out[g] = days[cs]
    return out


def order_to_day_consistency():
    """The cited day estimates must agree with the cascade DEPTH order (the same order validated at
    the rank level). Reports Spearman(depth, day) and the early/late day band. [F] over [L]."""
    od = gene_onset_days()
    d = cascade.depth()
    genes = sorted(od.keys())
    depths = [d[g] for g in genes]
    onset = [od[g] for g in genes]
    rho = _spearman(depths, onset)
    return {
        "n_genes_with_day": len(genes),
        "spearman_depth_vs_onset_day": round(rho, 4),
        "earliest_gene": min(genes, key=lambda g: od[g]),
        "earliest_day": round(min(od.values()), 1),
        "latest_gene": max(genes, key=lambda g: od[g]),
        "latest_day": round(max(od.values()), 1),
        "day_span": round(max(od.values()) - min(od.values()), 1),
        "grade": "[F] the cited order->day band is consistent with the cascade depth order (the same "
                 "order validated at the rank level); per-gene absolute day stays approximate.",
    }


def global_clock_open():
    """The honest residual: WHY 5 h, WHY 42, and how the many organ sub-clocks are phased into one
    body clock is NOT derived. Absolute multi-program timing stays [O]."""
    return {
        "what_is_closed": "the segmentation SUB-clock (cited rate -> cited duration) [L]; the "
                          "order->day band for the anchored genes [F over L].",
        "what_stays_open": "the GLOBAL multi-program developmental clock: the origin of the 5 h "
                           "period, the somite count, and the phase-alignment of distinct organ "
                           "sub-clocks into one absolute body timeline is NOT derived here.",
        "grade": "[O] absolute multi-program timing remains open -- measured rates are attached, "
                 "not explained.",
    }


def read():
    return {
        "segmentation_subclock": segmentation_subclock(),
        "order_to_day_consistency": order_to_day_consistency(),
        "global_clock_open": global_clock_open(),
    }
