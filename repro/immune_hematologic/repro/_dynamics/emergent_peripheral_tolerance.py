#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_peripheral_tolerance.py  --  EMERGENT peripheral tolerance / regulatory suppression as a MEASURED
suppressor field that subtracts from an escaped self-clone's drive and re-contains it below the saddle-node
(not asserted, not fitted).

WHY THIS EXISTS (v0.10.0). Central tolerance (T21, emergent_negative_selection.py) MEASURED that the thymic
deletion channel removes self-reactive clones driven above the spinodal, but leaves an ESCAPED near-threshold
fraction whose residual self-drive sits just BELOW the deletion threshold. Autoimmunity (T23,
emergent_autoimmunity.py) MEASURED that such an escaped clone, being bistable, LATCHES ON past a saddle-node when
an inflammatory insult pushes its TOTAL drive over the spinodal. Biology does not leave that escaped fraction
unguarded: a second, PERIPHERAL layer of tolerance (regulatory suppression) acts on the mature repertoire to hold
escaped self-clones quiescent. The VP discipline is emergence: whether a suppressor field can re-contain an escaped
clone, and exactly how much suppression that takes, must come OUT of the same substrate dynamics, MEASURED.

This module takes one escaped R19 self-clone (T23's setup: starting in the resting OFF basin, carrying a constant
sub-spinodal residual self-drive h_self = base · spinodal, hit by an inflammatory insult of amplitude
insult · spinodal) and adds a PERIPHERAL SUPPRESSOR FIELD that subtracts σ · spinodal from the drive while it is
engaged -- a regulatory tone that lowers the effective antigenic drive on the clone:

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt) · ξ,   h = (base + insult − σ)·spinodal during the insult,

with the suppressor PERSISTING into the settle (h = (base − σ)·spinodal after the insult clears -- regulatory tone
does not vanish when the insult does). The module MEASURES the basin the clone lands in -- contained (OFF, tolerance
held) or broken (ON, autoreactive) -- and sweeps the suppression strength σ to find the containment threshold.
Nothing about it is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. THE SUPPRESSION THRESHOLD IS THE SADDLE-NODE COMPLEMENT: σ_crit = (base + insult) − 1 (× spinodal). For an
     escaped clone whose insult would otherwise break it, the suppression at which P(break) crosses 0.5 (downward)
     lands exactly on the EXCESS of the total drive over the spinodal -- the suppressor has to cancel precisely the
     amount by which (residual + insult) overshoots the switch's saddle-node, organ by organ. Suppression and drive
     are the same currency read with opposite sign: the regulatory field neutralises the autoimmune overshoot of
     T23, MEASURED not posited.
  2. CONTAINMENT TRACKS THE ESCAPED RESIDUAL. Sweeping the escapee's residual self-drive `base` (its negative-
     selection depth) at a fixed insult, the required suppression σ_crit RISES with slope ≈ 1: a deeper escapee
     (larger residual, closer to having broken through central tolerance) needs proportionally MORE peripheral
     suppression to stay contained. The two tolerance layers add -- shallower central deletion (larger surviving
     residual) demands more peripheral regulatory tone, a measured division of labour between T21 and this layer.
  3. SUPPRESSION IS REQUIRED (honest control). With the suppressor off (σ = 0) the escaped clone driven by a
     supra-threshold insult breaks (measured P(break) ≈ 1); engaging sufficient suppression (σ above σ_crit) holds
     it contained (P(break) ≈ 0). Removing the channel reinstates the break -- containment is the suppressor's
     doing, not an artefact of the settle.

GRADES (C3): the containment-threshold shape — σ_crit = (residual + insult) − spinodal saddle-node complement, the
slope-≈1 tracking of escaped residual, and the suppression-required control — are [V] emergent (measured from the
coupled stochastic latch with a subtractive suppressor). The ABSOLUTE suppression strength — the mapping from σ to
a regulatory-cell count / cytokine level, the escaped-sliver width, and the free cellular-noise scale D — is [O],
no fabricated numbers. Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"        # the adaptive compartment where an escaped self-clone resides peripherally

# --- deterministic simulation size (fixed; mirror the T23 autoimmune latch; no per-condition tuning) ---
_N      = 250       # cells per (base, insult, sigma) condition
_DT     = 0.01      # integration timestep
_RELAX  = 1000      # settle steps after the insult is withdrawn (decide final basin); suppressor persists
_D      = 0.02      # cellular-noise scale (low: sharp boundary; absolute value is [O])
_DUR    = 800       # insult duration

# suppression grid (× spinodal); spans 0 .. >0.6 so the deepest escaped residual in the sweep still crosses
_SIGMAS     = (0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70)
_BASE_REF   = 0.30          # reference residual self-drive of a surviving escapee (× spinodal; sub-spinodal)
_INSULT_REF = 0.95          # reference inflammatory insult (× spinodal); base+insult = 1.25 > 1 so it would break
_BASE_SWEEP = (0.00, 0.20, 0.40, 0.60)   # escaped-residual (negative-selection depth) sweep


def p_break(g, base, insult, sigma, D=_D, N=_N, dt=_DT, dur=_DUR, relax=_RELAX, seed=SEED):
    """MEASURED probability an escaped self-clone breaks under an insult WITH a peripheral suppressor field of
    strength sigma subtracting from the drive: from the resting OFF basin hold h=(base+insult−sigma)·spinodal for
    `dur` steps, then withdraw the insult and settle under the persisting h=(base−sigma)·spinodal (residual self-
    drive minus regulatory tone); report the fraction landing in the ON basin. The suppressor persists into the
    settle -- regulatory tone does not vanish with the insult."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))                 # start in the resting (OFF / tolerant) basin
    sq = math.sqrt(2.0 * D * dt)
    h_pulse = (base + insult - sigma) * sp
    h_rest  = (base - sigma) * sp                 # insult withdrawn; residual self-drive AND suppressor persist
    for _ in range(int(dur)):
        s += (g * s - s ** 3 + h_pulse) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(relax)):
        s += (g * s - s ** 3 + h_rest) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _sigma_threshold(g, base, insult, sigmas=_SIGMAS, D=_D, seed=SEED):
    """Interpolate the suppression strength (× spinodal) at which P(break) crosses 0.5 DOWNWARD (break decreases as
    suppression rises). If already contained at the lowest sigma, return that; if never contained, return the top."""
    ps = [p_break(g, base, insult, sg, D=D, seed=seed) for sg in sigmas]
    if ps[0] < 0.5:                               # already contained at the lowest suppression
        return sigmas[0], ps
    for i in range(1, len(ps)):
        if ps[i - 1] >= 0.5 > ps[i]:
            f = (ps[i - 1] - 0.5) / (ps[i - 1] - ps[i])
            return sigmas[i - 1] + f * (sigmas[i] - sigmas[i - 1]), ps
    return sigmas[-1], ps


def emergent_peripheral_tolerance(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1) SUPPRESSION THRESHOLD == SADDLE-NODE COMPLEMENT (base+insult)−1, organ by organ
    excess_ref = _BASE_REF + _INSULT_REF - 1.0
    thr_rows = {}
    thr_ok = True
    for o in _ORGANS:
        g = gammas[o]
        sc, _ps = _sigma_threshold(g, _BASE_REF, _INSULT_REF, D=D)
        ratio = sc / excess_ref if excess_ref > 1e-9 else float("inf")
        ok = bool(abs(sc - excess_ref) < 0.10)
        thr_rows[o] = dict(sigma_crit_over_spinodal=round(sc, 3),
                           saddle_node_excess=round(excess_ref, 3),
                           ratio=round(ratio, 3), matches_excess=ok)
        thr_ok = thr_ok and ok

    # (2) CONTAINMENT TRACKS ESCAPED RESIDUAL: sweep base at fixed insult -> sigma_crit rises with slope ~1
    track_rows = []
    for base in _BASE_SWEEP:
        sc, _ps = _sigma_threshold(g_ref, base, _INSULT_REF, D=D)
        expect = max(base + _INSULT_REF - 1.0, 0.0)
        track_rows.append(dict(residual_self_drive=round(base, 3),
                               sigma_crit=round(sc, 3),
                               expected_excess=round(expect, 3),
                               matches=bool(abs(sc - expect) < 0.12)))
    sc_seq = [r["sigma_crit"] for r in track_rows]
    track_monotone = bool(all(sc_seq[i] <= sc_seq[i + 1] + 1e-9 for i in range(len(sc_seq) - 1))
                          and sc_seq[-1] > sc_seq[0])
    track_matches = bool(all(r["matches"] for r in track_rows))
    # measured slope of sigma_crit vs residual over the sweep (expect ~1: one-for-one with escaped depth)
    xs = [r["residual_self_drive"] for r in track_rows]; ys = sc_seq
    n = len(xs); sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    slope = (n*sxy - sx*sy) / (n*sxx - sx*sx) if (n*sxx - sx*sx) > 1e-12 else float("nan")
    slope_ok = bool(abs(slope - 1.0) < 0.25)

    # (3) SUPPRESSION REQUIRED (control): sigma=0 breaks, sufficient sigma contains
    p_no  = p_break(g_ref, _BASE_REF, _INSULT_REF, 0.0, D=D)
    p_yes = p_break(g_ref, _BASE_REF, _INSULT_REF, 0.40, D=D)   # 0.40 > excess 0.25 -> contained
    required = bool(p_no > 0.5 and p_yes < 0.5)

    ok = bool(thr_ok and track_monotone and track_matches and slope_ok and required)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6),
        noise_D=D, residual_self_drive_ref=_BASE_REF, insult_ref=_INSULT_REF,
        saddle_node_excess_ref=round(excess_ref, 3),
        suppression_threshold=thr_rows,
        threshold_equals_excess=bool(thr_ok),
        containment_tracks_residual=track_rows,
        tracking_monotone=bool(track_monotone), tracking_matches_excess=bool(track_matches),
        sigma_vs_residual_slope=round(slope, 3), slope_is_one=bool(slope_ok),
        suppression_required=dict(p_break_sigma0=round(p_no, 3), p_break_sigma_040=round(p_yes, 3),
                                  required=bool(required)),
        all_pass=ok,
        grade="[V] peripheral tolerance EMERGES from a subtractive regulatory suppressor field on an escaped T23 "
              "self-clone: the containment threshold is the saddle-node complement (measured σ_crit = (residual + "
              "insult) − spinodal, organ by organ -- the suppressor cancels exactly the total-drive overshoot of "
              "the switch), the required suppression rises one-for-one (slope ≈ 1) with the escaped residual so the "
              "central (T21) and peripheral layers add, and suppression is required (σ=0 breaks, sufficient σ "
              "contains) -- measured, not assumed; [O] absolute suppression strength (σ→regulatory-cell mapping), "
              "escaped-sliver width, cellular-noise scale D")


def run(gammas):
    """T24: emergent peripheral tolerance / regulatory suppression -- a subtractive suppressor field re-contains an escaped self-clone below the saddle-node MEASURED, with the containment threshold = the total-drive overshoot and a slope-≈1 division of labour with central deletion."""
    r = emergent_peripheral_tolerance(gammas)
    return dict(T24=dict(target="T24",
                         claim="peripheral tolerance / regulatory suppression EMERGES as a subtractive suppressor "
                               "field on an escaped self-clone (T23's bistable setup): the suppression at which the "
                               "clone is re-contained is the saddle-node COMPLEMENT (measured σ_crit = (residual + "
                               "insult) − spinodal, organ by organ -- the regulatory field neutralises exactly the "
                               "amount by which the total drive overshoots the switch), the required suppression "
                               "rises one-for-one (slope ≈ 1) with the escaped residual so central deletion (T21) "
                               "and peripheral suppression ADD, and suppression is required (σ=0 breaks, sufficient "
                               "σ contains) -- measured, not assumed; absolute suppression strength stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T24"]["result"]
    print("PERIPHERAL TOLERANCE / regulatory suppression on an escaped self-clone (primary=%s, γ=%.4f, spinodal=%.4f, D=%.3f):"
          % (r["primary"], r["gamma"], r["spinodal"], r["noise_D"]))
    print("    reference escapee: residual=%.2f insult=%.2f -> saddle-node excess=%.3f×sp"
          % (r["residual_self_drive_ref"], r["insult_ref"], r["saddle_node_excess_ref"]))
    print("\n(1) SUPPRESSION THRESHOLD == SADDLE-NODE COMPLEMENT (σ_crit == (residual+insult)−1), organ by organ:")
    for o, row in r["suppression_threshold"].items():
        print("     %-28s σ_crit=%.3f×sp  excess=%.3f  ratio=%.3f  matches=%s"
              % (o, row["sigma_crit_over_spinodal"], row["saddle_node_excess"], row["ratio"], row["matches_excess"]))
    print("     -> all organs: %s" % r["threshold_equals_excess"])
    print("\n(2) CONTAINMENT TRACKS ESCAPED RESIDUAL (σ_crit rises with the escapee's residual self-drive):")
    for row in r["containment_tracks_residual"]:
        print("     residual=%.2f  σ_crit=%.3f  expected_excess=%.3f  matches=%s"
              % (row["residual_self_drive"], row["sigma_crit"], row["expected_excess"], row["matches"]))
    print("     -> monotone: %s ; matches excess: %s ; measured slope=%.3f (≈1: %s)"
          % (r["tracking_monotone"], r["tracking_matches_excess"], r["sigma_vs_residual_slope"], r["slope_is_one"]))
    s = r["suppression_required"]
    print("\n(3) SUPPRESSION REQUIRED (control):")
    print("     σ=0 -> P(break)=%.3f ; σ=0.40 -> P(break)=%.3f -> required=%s"
          % (s["p_break_sigma0"], s["p_break_sigma_040"], s["required"]))
    print("\nT24 all_pass:", r["all_pass"])
