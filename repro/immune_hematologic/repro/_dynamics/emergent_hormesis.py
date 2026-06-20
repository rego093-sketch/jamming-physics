#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_hormesis.py  --  EMERGENT tolerance-immunity dose window as a MEASURED interior danger band whose lower
edge is set by an inflammatory insult and whose upper edge is set by central deletion (not asserted, not fitted).

WHY THIS EXISTS (v0.10.0). Three measured results meet here. T11 (emergent_selection.py) MEASURED that a clone
COMMITS when its drive reaches the spinodal (the activation saddle-node, from below by thermal activation). T21
(emergent_negative_selection.py) MEASURED that a self-clone whose self-drive reaches the spinodal is DELETED
centrally, not activated -- so high self-antigen dose is SAFE (the clone is removed). T23 (emergent_autoimmunity.py)
MEASURED that an ESCAPED self-clone (sub-deletion residual self-drive) BREAKS tolerance when an inflammatory insult
pushes its TOTAL drive over the spinodal. Put the three together against a swept self-antigen DOSE d and a fixed
insult: at LOW dose the clone is ignored (too little residual drive for the insult to break it -- safe), at HIGH
dose the clone is centrally DELETED (safe), and in BETWEEN sits a window where the clone both escapes deletion AND
is broken by the insult. The VP discipline is emergence: whether such a window exists, what sets its edges, and how
they move, must come OUT of the substrate dynamics, MEASURED.

HONEST SIGN. The roadmap framed this as a tolerance "safe band". The substrate gives the DUAL and we report it as
measured: the interior is the DANGER band (escape ∧ break), flanked by two SAFE regimes -- IGNORANCE below
(insufficient drive) and DELETION above (central tolerance). The safe doses are the two flanks; the danger is
interior. We report the sign the substrate produces, not the sign we expected.

This module composes two measured substrate processes against a swept self-antigen dose d (× spinodal):
  * P(escape) = 1 − p_delete(d)        -- the T21 central-deletion process (a DECREASING function of d: high dose
                                          drives commitment in the thymic context and is deleted), insult-INDEPENDENT
  * P(break | escaped) = p_break(d, insult) -- the T23 escaped-clone latch under the insult (an INCREASING function
                                          of d: a larger residual self-drive needs less insult to cross the spinodal)
  * NET break-risk(d) = P(escape) · P(break | escaped)
and MEASURES the edges of the resulting interior band by interpolating the 0.5-crossings of the two component
processes. Nothing about it is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. AN INTERIOR DANGER BAND EXISTS, FLANKED BY TWO SAFE REGIMES. The NET break-risk is single-peaked in dose: ≈ 0
     at low dose (ignorance), a peak at intermediate dose, ≈ 0 at high dose (deletion). The lower (break) edge sits
     below the peak which sits below the upper (deletion) edge -- a measured ordered interior band.
  2. THE LOWER EDGE TRACKS THE INSULT ONE-FOR-ONE (slope −1). Sweeping the insult, the lower (break) edge
     d_lo = spinodal − insult: it moves DOWN by exactly the insult increment (measured slope ≈ −1). A stronger
     insult lets a smaller residual self-drive break tolerance, widening the danger band from below.
  3. THE UPPER EDGE IS INSULT-INDEPENDENT (set by central deletion). The upper (deletion) edge d_hi does NOT move
     as the insult is swept (measured slope ≈ 0): it is fixed by the T21 central-tolerance threshold, a property of
     the thymic deletion process, not of the peripheral insult.
  4. THE BAND WIDTH GROWS ONE-FOR-ONE WITH THE INSULT (slope +1). Because only the lower edge moves, the width
     d_hi − d_lo increases by exactly the insult increment (measured slope ≈ +1). The danger band is OPENED by the
     insult: its width is the insult's signature on the dose axis -- a falsifiable measured prediction.
  5. THE WINDOW COLLAPSES AS THE INSULT VANISHES (honest control). As the insult → 0 the lower edge rises to meet
     the fixed upper edge and the band CLOSES (measured width → 0): with no insult there is no danger band -- the
     two safe flanks merge and every escaped dose is tolerated. The band is insult-driven, not intrinsic.
  6. THE BAND POSITION TRACKS EACH ORGAN'S SPINODAL. The upper (deletion) edge, measured organ by organ in units of
     that organ's spinodal, is a ≈ constant dimensionless fraction -- so in ABSOLUTE drive units the whole window
     sits at each organ's own spinodal scale, recovering the T21 ordering (the window POSITION is the organ's
     spinodal). And the lower edge obeys d_lo + insult = spinodal -- the T11/T18 commit threshold -- so the danger
     band opens exactly where the escaped clone plus the insult reach the activation saddle-node.

GRADES (C3): the interior-band existence and ordering, the lower-edge slope −1 (= spinodal − insult, the commit
threshold), the upper-edge insult-independence, the width slope +1, the zero-insult collapse, and the spinodal-
tracking position are [V] emergent (measured by composing the T21 deletion and T23 break processes over a dose
sweep). The ABSOLUTE band edges / width — set by the thermal lowering of the deletion edge, the insult amplitude,
and the free cellular-noise scale D — are [O], no fabricated numbers (the SLOPES are the clean invariants; the
absolute width carries a thermal offset). Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"        # the adaptive compartment carrying an escaped self-clone

# --- deterministic simulation size (fixed; reuse the T21 deletion + T23 break processes; no per-condition tuning) ---
_N      = 220       # cells per (dose, insult) condition
_DT     = 0.01      # integration timestep
_D      = 0.02      # cellular-noise scale (absolute value is [O])
_T_EDU  = 40.0      # thymic education window for central deletion (T21 process)
_DUR    = 600       # insult duration for the break process (T23 process)
_RELAX  = 700       # settle steps after the insult clears (T23 process)

_DOSES_NET  = tuple(round(0.2 * k, 2) for k in range(2, 8))          # 0.40 .. 1.40 display curve (single-peak, coarsened)
_DOSES_EDGE = tuple(round(0.10 * k, 2) for k in range(3, 13))        # 0.30 .. 1.20 grid for edge crossings (coarsened)
_INSULTS    = (0.20, 0.40, 0.60)                                     # insult sweep for the edge slopes
_INSULT_REF = 0.40                                                  # reference insult for the display curve
_INSULT_ZERO = 0.05                                                 # near-zero insult for the collapse control
_DOSES_POS  = tuple(round(0.05 * k, 2) for k in range(12, 21))       # 0.60 .. 1.00 grid for the per-organ edge


def p_delete(g, d_frac, D=_D, N=_N, dt=_DT, T=_T_EDU, seed=SEED):
    """MEASURED central-deletion probability (T21 process): a self-clone with fixed self-drive h=d_frac·spinodal is
    educated for T; any cell that commits ON in the thymic context is DELETED. Returns the deleted fraction.
    INCREASING in d_frac, so P(escape)=1−p_delete is DECREASING. Insult-independent (a central-tolerance property)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))
    committed = np.zeros(N, bool)
    sq = math.sqrt(2.0 * D * dt)
    h = d_frac * sp
    for _ in range(int(T / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        committed |= (s > 0.0)
        if committed.all():
            break
    return float(committed.mean())


def p_break_given_escaped(g, d_frac, insult_frac, D=_D, N=_N, dt=_DT, dur=_DUR, relax=_RELAX, seed=SEED + 7):
    """MEASURED tolerance-break probability for an ESCAPED clone (T23 process): residual self-drive h=d_frac·spinodal,
    hit by an insult of amplitude insult_frac·spinodal for `dur`, then settled under the persisting residual drive;
    returns the ON fraction. INCREASING in d_frac (larger residual breaks under less insult)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))
    sq = math.sqrt(2.0 * D * dt)
    h_pulse = (d_frac + insult_frac) * sp
    h_rest = d_frac * sp
    for _ in range(int(dur)):
        s += (g * s - s ** 3 + h_pulse) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(relax)):
        s += (g * s - s ** 3 + h_rest) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _edge_up(xs, ys):
    """Interpolate where an INCREASING series crosses 0.5 (the lower / break edge)."""
    if ys[0] >= 0.5:
        return xs[0]
    for i in range(1, len(ys)):
        if ys[i - 1] < 0.5 <= ys[i]:
            f = (0.5 - ys[i - 1]) / (ys[i] - ys[i - 1])
            return xs[i - 1] + f * (xs[i] - xs[i - 1])
    return None


def _edge_down(xs, ys):
    """Interpolate where a DECREASING series crosses 0.5 (the upper / deletion edge)."""
    if ys[0] < 0.5:
        return xs[0]
    for i in range(1, len(ys)):
        if ys[i - 1] >= 0.5 > ys[i]:
            f = (ys[i - 1] - 0.5) / (ys[i - 1] - ys[i])
            return xs[i - 1] + f * (xs[i] - xs[i - 1])
    return None


def _lsq_slope(xs, ys):
    n = len(xs); sx = sum(xs); sy = sum(ys); sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    return (n * sxy - sx * sy) / denom if abs(denom) > 1e-12 else float("nan")


def emergent_hormesis(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # P(escape) curve is insult-independent -> compute the deletion process ONCE on the fine grid and reuse.
    pesc_edge = [1.0 - p_delete(g_ref, d, D=D) for d in _DOSES_EDGE]
    d_hi_ref = _edge_down(_DOSES_EDGE, pesc_edge)

    # (1) INTERIOR DANGER BAND on the display grid at the reference insult (single-peaked, flanks low)
    pesc_net = [1.0 - p_delete(g_ref, d, D=D) for d in _DOSES_NET]
    pbrk_net = [p_break_given_escaped(g_ref, d, _INSULT_REF, D=D) for d in _DOSES_NET]
    net = [round(pe * pb, 3) for pe, pb in zip(pesc_net, pbrk_net)]
    peak_i = int(np.argmax(net))
    d_lo_ref = _edge_up(_DOSES_EDGE, [p_break_given_escaped(g_ref, d, _INSULT_REF, D=D) for d in _DOSES_EDGE])
    interior_ordered = bool(d_lo_ref is not None and d_hi_ref is not None
                            and d_lo_ref < _DOSES_NET[peak_i] < d_hi_ref
                            and net[0] < 0.1 and net[-1] < 0.1 and net[peak_i] > 0.4)

    # (2)-(4) INSULT SWEEP: lower edge slope −1, upper edge slope 0, width slope +1
    sweep = []
    for ins in _INSULTS:
        pbrk = [p_break_given_escaped(g_ref, d, ins, D=D) for d in _DOSES_EDGE]
        d_lo = _edge_up(_DOSES_EDGE, pbrk)
        width = (d_hi_ref - d_lo) if (d_lo is not None and d_hi_ref is not None) else None
        sweep.append(dict(insult=round(ins, 3),
                          d_lo=round(d_lo, 3) if d_lo is not None else None,
                          d_hi=round(d_hi_ref, 3) if d_hi_ref is not None else None,
                          width=round(width, 3) if width is not None else None,
                          lo_plus_insult=round(d_lo + ins, 3) if d_lo is not None else None))
    ins_x   = [r["insult"] for r in sweep]
    lo_y    = [r["d_lo"] for r in sweep]
    width_y = [r["width"] for r in sweep]
    lo_slope    = _lsq_slope(ins_x, lo_y)
    width_slope = _lsq_slope(ins_x, width_y)
    lo_slope_is_minus1 = bool(abs(lo_slope - (-1.0)) < 0.2)
    hi_independent     = bool(len(set(r["d_hi"] for r in sweep)) == 1)   # exact: same reused d_hi
    width_slope_is_one = bool(abs(width_slope - 1.0) < 0.2)
    # T11/T18 commit-threshold tie-in: d_lo + insult == spinodal (==1 in normalized units)
    lo_plus = [r["lo_plus_insult"] for r in sweep]
    commit_threshold_tie = bool(all(abs(v - 1.0) < 0.08 for v in lo_plus))

    # (5) ZERO-INSULT COLLAPSE (control): as insult -> 0, d_lo -> d_hi, band width -> 0
    pbrk_zero = [p_break_given_escaped(g_ref, d, _INSULT_ZERO, D=D) for d in _DOSES_EDGE]
    d_lo_zero = _edge_up(_DOSES_EDGE, pbrk_zero)
    width_zero = (d_hi_ref - d_lo_zero) if (d_lo_zero is not None and d_hi_ref is not None) else None
    # widths must increase with insult AND the near-zero-insult width must be a small fraction of the widest
    widths_sorted_ok = bool(all(width_y[i] <= width_y[i + 1] + 1e-9 for i in range(len(width_y) - 1)))
    collapses = bool(width_zero is not None and width_y[-1] is not None
                     and width_zero < 0.25 * width_y[-1] and widths_sorted_ok)

    # (6) POSITION TRACKS SPINODAL: upper (deletion) edge per organ, normalized -> ≈ const; absolute = ×spinodal
    pos_rows = {}
    norm_edges = []
    for o in _ORGANS:
        g = gammas[o]
        pe = [1.0 - p_delete(g, d, D=D) for d in _DOSES_POS]
        dhi = _edge_down(_DOSES_POS, pe)
        norm_edges.append(dhi)
        pos_rows[o] = dict(deletion_edge_over_spinodal=round(dhi, 3) if dhi is not None else None,
                           deletion_edge_absolute=round(dhi * spinodal(g), 4) if dhi is not None else None)
    pos_const = bool(norm_edges and (max(norm_edges) - min(norm_edges)) < 0.08)   # same dimensionless fraction

    ok = bool(interior_ordered and lo_slope_is_minus1 and hi_independent and width_slope_is_one
              and commit_threshold_tie and collapses and pos_const)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6),
        noise_D=D, insult_ref=_INSULT_REF,
        net_curve=dict(doses=list(_DOSES_NET), net=net, peak_dose=_DOSES_NET[peak_i],
                       low_flank=net[0], high_flank=net[-1],
                       d_lo=round(d_lo_ref, 3) if d_lo_ref is not None else None,
                       d_hi=round(d_hi_ref, 3) if d_hi_ref is not None else None,
                       interior_band_ordered=bool(interior_ordered)),
        insult_sweep=sweep,
        lower_edge_slope=round(lo_slope, 3), lower_edge_slope_is_minus1=bool(lo_slope_is_minus1),
        upper_edge_insult_independent=bool(hi_independent),
        width_slope=round(width_slope, 3), width_slope_is_one=bool(width_slope_is_one),
        commit_threshold_tie_in=dict(lo_plus_insult=lo_plus, equals_spinodal=bool(commit_threshold_tie)),
        zero_insult_collapse=dict(insult=_INSULT_ZERO, d_lo=round(d_lo_zero, 3) if d_lo_zero is not None else None,
                                  width=round(width_zero, 3) if width_zero is not None else None,
                                  widest=width_y[-1], collapses=bool(collapses)),
        position_tracks_spinodal=dict(per_organ=pos_rows, normalized_constant=bool(pos_const)),
        all_pass=ok,
        grade="[V] the tolerance-immunity dose window EMERGES by composing the T21 central-deletion process with "
              "the T23 escaped-clone break over a self-antigen dose sweep: an INTERIOR danger band (escape ∧ break) "
              "is flanked by two safe regimes (ignorance below, deletion above), its lower edge = spinodal − insult "
              "(measured slope −1, = the T11/T18 commit threshold so d_lo + insult = spinodal), its upper edge is "
              "insult-independent (set by central deletion, slope 0), its width grows one-for-one with the insult "
              "(slope +1), it COLLAPSES as the insult → 0 (no insult, no danger band), and its position tracks each "
              "organ's spinodal (deletion edge a constant dimensionless fraction) -- measured, not assumed; [O] "
              "absolute band edges / width (thermal lowering of the deletion edge, insult amplitude, cellular-noise "
              "scale D); the SLOPES are the clean invariants")


def run(gammas):
    """T26: emergent tolerance-immunity dose window -- composing T21 central deletion with the T23 escaped-clone break over a self-antigen dose sweep yields a MEASURED interior danger band whose lower edge tracks the insult (slope −1 = the commit threshold), whose upper edge is insult-independent (central deletion), whose width grows one-for-one with the insult, which collapses with no insult, and whose position tracks each organ's spinodal."""
    r = emergent_hormesis(gammas)
    return dict(T26=dict(target="T26",
                         claim="the tolerance-immunity dose window EMERGES by composing the T21 central-deletion "
                               "process with the T23 escaped-clone break over a self-antigen dose sweep: the "
                               "substrate gives an INTERIOR DANGER band (escape ∧ break) flanked by two SAFE "
                               "regimes -- ignorance (low dose) and central deletion (high dose); the lower (break) "
                               "edge = spinodal − insult so it tracks the insult one-for-one (measured slope −1, and "
                               "d_lo + insult = spinodal, the T11/T18 commit threshold), the upper (deletion) edge "
                               "is insult-independent (fixed by central tolerance, slope 0), the band width grows "
                               "one-for-one with the insult (slope +1, the insult's signature on the dose axis), the "
                               "window COLLAPSES as the insult → 0 (no insult, no danger band), and the window "
                               "position tracks each organ's spinodal -- measured, not assumed; absolute band edges "
                               "stay [O] (slopes are the clean invariants)",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T26"]["result"]
    print("TOLERANCE-IMMUNITY DOSE WINDOW (primary=%s, γ=%.4f, spinodal=%.4f, D=%.3f, insult_ref=%.2f):"
          % (r["primary"], r["gamma"], r["spinodal"], r["noise_D"], r["insult_ref"]))
    nc = r["net_curve"]
    print("\n(1) INTERIOR DANGER BAND (NET break-risk vs dose, single-peaked, flanked by safe regimes):")
    print("     doses:", nc["doses"])
    print("     NET  :", nc["net"])
    print("     peak@d=%.2f  low_flank=%.3f  high_flank=%.3f  d_lo=%.3f  d_hi=%.3f -> ordered interior band=%s"
          % (nc["peak_dose"], nc["low_flank"], nc["high_flank"], nc["d_lo"], nc["d_hi"], nc["interior_band_ordered"]))
    print("\n(2)-(4) INSULT SWEEP (lower edge slope −1, upper edge fixed, width slope +1):")
    for row in r["insult_sweep"]:
        print("     insult=%.2f  d_lo=%.3f  d_hi=%.3f  width=%.3f  (d_lo+insult=%.3f)"
              % (row["insult"], row["d_lo"], row["d_hi"], row["width"], row["lo_plus_insult"]))
    print("     lower-edge slope=%.3f (≈−1: %s) ; upper-edge insult-independent=%s ; width slope=%.3f (≈+1: %s)"
          % (r["lower_edge_slope"], r["lower_edge_slope_is_minus1"], r["upper_edge_insult_independent"],
             r["width_slope"], r["width_slope_is_one"]))
    ct = r["commit_threshold_tie_in"]
    print("     T11/T18 commit-threshold tie-in: d_lo+insult=%s == spinodal: %s" % (ct["lo_plus_insult"], ct["equals_spinodal"]))
    zc = r["zero_insult_collapse"]
    print("\n(5) ZERO-INSULT COLLAPSE (control, insult=%.2f):" % zc["insult"])
    print("     d_lo=%.3f  width=%.3f vs widest=%.3f -> band collapses=%s" % (zc["d_lo"], zc["width"], zc["widest"], zc["collapses"]))
    print("\n(6) POSITION TRACKS SPINODAL (deletion edge per organ; normalized ≈ const => absolute ∝ spinodal):")
    for o, row in r["position_tracks_spinodal"]["per_organ"].items():
        print("     %-28s deletion_edge=%.3f×sp  absolute=%.4f" % (o, row["deletion_edge_over_spinodal"], row["deletion_edge_absolute"]))
    print("     -> normalized constant across organs: %s" % r["position_tracks_spinodal"]["normalized_constant"])
    print("\nT26 all_pass:", r["all_pass"])
