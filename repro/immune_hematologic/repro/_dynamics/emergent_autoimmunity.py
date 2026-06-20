#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_autoimmunity.py  --  EMERGENT autoimmune tolerance break as a MEASURED bistable latch of an escaped
self-reactive clone under an inflammatory insult (not asserted, not fitted).

WHY THIS EXISTS (v0.9.0). Two measured results meet here. T9 (emergent_chronicity.py) MEASURED that an
inflammatory insult held on a resting switch latches ON past a critical amplitude = the organ's spinodal, with a
dose x duration tradeoff, and persists after the insult clears (hysteresis). T21 (emergent_negative_selection.py)
MEASURED that central tolerance DELETES self-reactive clones driven above the spinodal, but that the deletion
channel leaves an ESCAPED near-threshold fraction: clones whose residual self-drive sits just BELOW the deletion
threshold and so survive into the periphery. Autoimmunity is the collision of the two: take such an escaped clone --
its residual self-antigen drive is sub-spinodal, so the switch is BISTABLE (a resting OFF basin and a
self-sustaining ON basin both exist) -- and hit it with an inflammatory insult pulse. The VP discipline is
emergence: whether, and when, tolerance breaks must come OUT of the same substrate dynamics, MEASURED.

This module drives one R19 self-clone (starting in the resting OFF basin) carrying a constant residual self-drive
h_self = base * spinodal (sub-spinodal), adds a rectangular inflammatory insult of amplitude insult * spinodal for
a duration, under cellular noise,

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt) · ξ,   h = (base + insult)·spinodal during the pulse,

then WITHDRAWS the insult and lets the field settle UNDER THE PERSISTING residual self-drive h = base·spinodal
(NOT to zero -- the self-antigen does not go away), and MEASURES the basin it lands in: tolerant (OFF, the insult
resolved) or broken (ON, a self-sustaining autoreactive response). Sweeping insult amplitude x duration, and
sweeping the residual self-drive `base`, MEASURES the tolerance-break boundary. Nothing about it is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. BREAK BOUNDARY IS THE SADDLE-NODE: TOTAL DRIVE = SPINODAL. With no residual self-drive the critical insult
     amplitude at which P(break) crosses 0.5 lands on the organ's own spinodal, organ by organ (recovering T9 in
     the autoimmune frame). With a residual self-drive present, the critical INSULT amplitude drops by exactly that
     residual: across a sweep of `base` the measured (base + critical-insult) sum stays at 1x spinodal -- the break
     boundary is the switch's saddle-node, and self-antigen and inflammation are interchangeable ways of reaching
     it, MEASURED not posited.
  2. THE BREAK IS IRREVERSIBLE -- A PATHOLOGICAL MEMORY. For an escaped clone (sub-spinodal residual self-drive)
     a supra-threshold insult latches the clone ON, and after the insult is WITHDRAWN to the persisting residual
     self-drive the clone STAYS ON (measured P(ON) after a long settle ≈ 1, unchanged when the settle is tripled) --
     a self-sustaining autoreactive state that outlives its trigger, the exact pathological mirror of the persistent
     immune memory of T4/T8. A sub-threshold insult RESOLVES (returns to OFF), and a deeply-tolerant clone (small
     residual drive) hit by a sub-spinodal-total insult NEVER breaks -- honest negative controls.
  3. DOSE x TIME TRADEOFF. Above threshold, the minimum breaking duration DECREASES monotonically as the insult
     amplitude rises -- a stronger inflammatory insult breaks tolerance faster (the same measured Kramers-style
     trade as T9, here for the tolerance latch).
  4. SUSCEPTIBILITY IS SET BY NEGATIVE-SELECTION DEPTH (the T21 -> T23 link). Sweeping the residual self-drive of
     the surviving escapee from deep-tolerant toward the deletion threshold, the critical insult amplitude DECREASES
     monotonically: a near-threshold escapee breaks under a weaker insult. Because central tolerance (T21) deletes
     exactly the near-threshold clones, DEEPER negative selection leaves only smaller-residual survivors and so
     RAISES the insult needed to break tolerance -- a measured link between deletion depth and autoimmune
     susceptibility, the break-risk concentrated in the escaped near-threshold fraction.

GRADES (C3): the break-boundary shape — total-drive = spinodal invariant, the irreversible-persistence pathological
memory, the dose x time tradeoff, and the negative-selection-depth susceptibility link — are [V] emergent (measured
from the coupled stochastic latch). The ABSOLUTE break rate / boundary timing — set by the residual-drive depth,
the insult amplitude / duration, and the free cellular-noise scale D — is [O], no fabricated numbers. Determinism:
fixed seed, BLAS pinned upstream, round-before-report.
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

# --- deterministic simulation size (fixed; mirror the T9 chronicity latch; no per-condition tuning) ---
_N      = 250       # cells per (amplitude, duration, base) condition
_DT     = 0.01      # integration timestep
_RELAX  = 1000      # settle steps after the insult is withdrawn (decide final basin)
_D      = 0.02      # cellular-noise scale (low: sharp boundary; absolute value is [O])
_DUR_LONG = 800     # "long" insult duration for the amplitude threshold

_INSULT_AMPS = (0.05, 0.10, 0.20, 0.30, 0.45, 0.55, 0.70, 0.85, 1.00, 1.15, 1.30)   # insult amplitude grid (× spinodal)
_DUR_GRID    = (50, 150, 300, 550, 900)        # duration grid for the dose×time tradeoff
_SUPRA       = (1.10, 1.25, 1.50, 2.00)                            # supra-threshold insults for d_crit (over total)
_BASE_REF    = 0.30          # reference residual self-drive of a surviving escapee (× spinodal; sub-spinodal)
_BASE_SWEEP  = (0.00, 0.20, 0.40, 0.60, 0.80)                      # residual self-drive sweep (deletion depth)


def p_break(g, insult_frac, dur, base=_BASE_REF, D=_D, N=_N, dt=_DT, relax=_RELAX, seed=SEED, relax_mult=1):
    """MEASURED probability tolerance breaks: from the resting OFF basin, hold h=(base+insult)·spinodal for `dur`
    steps, then WITHDRAW the insult and settle under the persisting residual self-drive h=base·spinodal; report the
    fraction that lands in the ON basin. The residual self-drive does NOT go to zero (the self-antigen persists)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))                 # start in the resting (OFF / tolerant) basin
    sq = math.sqrt(2.0 * D * dt)
    h_pulse = (base + insult_frac) * sp
    h_rest  = base * sp                           # the insult is withdrawn TO the residual self-drive, not to 0
    for _ in range(int(dur)):
        s += (g * s - s ** 3 + h_pulse) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(relax * relax_mult)):      # withdraw insult, let it decide a basin under residual self-drive
        s += (g * s - s ** 3 + h_rest) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _insult_threshold(g, base, dur=_DUR_LONG, amps=_INSULT_AMPS, D=_D, seed=SEED):
    """Interpolate the insult amplitude (× spinodal) at which P(break) crosses 0.5 at long duration, given a fixed
    residual self-drive `base`."""
    ps = [p_break(g, a, dur, base=base, D=D, seed=seed) for a in amps]
    if ps[0] >= 0.5:                              # crossing is at/below the lowest grid point
        return amps[0]
    for i in range(1, len(ps)):
        if ps[i - 1] < 0.5 <= ps[i]:
            f = (0.5 - ps[i - 1]) / (ps[i] - ps[i - 1])
            return amps[i - 1] + f * (amps[i] - amps[i - 1])
    return amps[-1] if ps[-1] >= 0.5 else float("inf")


def _dur_threshold(g, total_frac, base, durs=_DUR_GRID, D=_D, seed=SEED):
    """Smallest insult duration (steps) for which P(break) >= 0.5, at a fixed TOTAL drive = total_frac·spinodal
    (insult amplitude = total_frac − base)."""
    insult = total_frac - base
    for d in durs:
        if p_break(g, insult, d, base=base, D=D, seed=seed) >= 0.5:
            return d
    return None


def emergent_autoimmunity(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1a) no-residual critical insult == spinodal, organ by organ (recovers T9 saddle-node in the autoimmune frame)
    amp_rows = {}
    crit_ok = True
    for o in _ORGANS:
        g = gammas[o]
        a_crit = _insult_threshold(g, base=0.0, dur=_DUR_LONG, D=D)
        amp_rows[o] = dict(insult_crit_over_spinodal=round(a_crit, 3),
                           matches_spinodal=bool(abs(a_crit - 1.0) < 0.10))
        crit_ok = crit_ok and amp_rows[o]["matches_spinodal"]

    # (1b) TOTAL-DRIVE INVARIANT: across a residual-self-drive sweep, base + critical-insult == 1×spinodal
    invariant_rows = []
    inv_ok = True
    for base in _BASE_SWEEP:
        a_crit = _insult_threshold(g_ref, base=base, dur=_DUR_LONG, D=D)
        total = base + a_crit
        ok = bool(abs(total - 1.0) < 0.12)
        invariant_rows.append(dict(residual_self_drive=round(base, 3),
                                   critical_insult=round(a_crit, 3),
                                   total_drive_over_spinodal=round(total, 3),
                                   equals_spinodal=ok))
        inv_ok = inv_ok and ok

    # (2) IRREVERSIBLE PERSISTENCE (pathological memory) for an escaped clone (base=_BASE_REF)
    #     supra-threshold insult -> ON and STAYS ON after withdrawal; sub-threshold -> resolves; tripled settle = same
    crit_ref = _insult_threshold(g_ref, base=_BASE_REF, dur=_DUR_LONG, D=D)
    supra = crit_ref + 0.25
    sub   = max(crit_ref - 0.25, 0.05)
    p_supra      = p_break(g_ref, supra, _DUR_LONG, base=_BASE_REF, D=D)
    p_supra_long = p_break(g_ref, supra, _DUR_LONG, base=_BASE_REF, D=D, relax_mult=3)   # triple the settle
    p_sub        = p_break(g_ref, sub,   _DUR_LONG, base=_BASE_REF, D=D)
    persists      = bool(p_supra > 0.5 and abs(p_supra_long - p_supra) < 0.05)
    sub_resolves  = bool(p_sub < 0.5)
    # deeply-tolerant clone, sub-spinodal TOTAL insult never breaks (far-below control)
    p_far_below   = p_break(g_ref, 0.40, _DUR_GRID[-1], base=0.20, D=D)                  # total 0.60×sp
    far_below_safe = bool(p_far_below < 0.5)

    # (3) DOSE × TIME TRADEOFF on the escaped clone: min breaking duration decreases as insult amplitude rises
    #     (sweep TOTAL drive supra-threshold; insult = total − base)
    dose_time = []
    for tf in _SUPRA:
        d_crit = _dur_threshold(g_ref, tf, base=_BASE_REF, D=D)
        dose_time.append(dict(total_drive_over_spinodal=round(tf, 3),
                              insult_over_spinodal=round(tf - _BASE_REF, 3), d_crit=d_crit))
    dcrit_vals = [r["d_crit"] for r in dose_time if r["d_crit"] is not None]
    tradeoff_monotone = bool(len(dcrit_vals) == len(dose_time)
                             and all(dcrit_vals[i] >= dcrit_vals[i + 1] for i in range(len(dcrit_vals) - 1))
                             and dcrit_vals[0] > dcrit_vals[-1])

    # (4) SUSCEPTIBILITY vs NEGATIVE-SELECTION DEPTH (T21 -> T23): critical insult falls as residual self-drive rises
    suscept = [dict(residual_self_drive=r["residual_self_drive"], critical_insult=r["critical_insult"])
               for r in invariant_rows]
    crit_seq = [r["critical_insult"] for r in suscept]
    susceptibility_monotone = bool(all(crit_seq[i] >= crit_seq[i + 1] for i in range(len(crit_seq) - 1))
                                   and crit_seq[0] > crit_seq[-1])

    ok = bool(crit_ok and inv_ok and persists and sub_resolves and far_below_safe
              and tradeoff_monotone and susceptibility_monotone)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6),
        noise_D=D, residual_self_drive_ref=_BASE_REF,
        no_residual_critical_insult=amp_rows,
        no_residual_critical_equals_spinodal=bool(crit_ok),
        total_drive_invariant=invariant_rows,
        total_drive_invariant_holds=bool(inv_ok),
        persistence=dict(critical_insult=round(crit_ref, 3),
                         p_break_supra=round(p_supra, 3), p_break_supra_tripled_settle=round(p_supra_long, 3),
                         p_break_sub=round(p_sub, 3),
                         irreversible_persists=bool(persists), sub_threshold_resolves=bool(sub_resolves),
                         far_below_safe=bool(far_below_safe), p_far_below=round(p_far_below, 3)),
        dose_time_tradeoff=dose_time, dose_time_monotone=bool(tradeoff_monotone),
        susceptibility_vs_deletion_depth=suscept, susceptibility_monotone=bool(susceptibility_monotone),
        all_pass=ok,
        grade="[V] the autoimmune tolerance break EMERGES from the R19 self-clone latch combining the T9 insult "
              "dynamics with a T21 escaped clone's residual self-drive: the break boundary is the switch saddle-node "
              "(measured total drive = spinodal across a residual-drive sweep, self-antigen and inflammation "
              "interchangeable), the break is irreversible (latches ON and persists after the insult clears, the "
              "pathological mirror of memory), the dose×time tradeoff holds, and the critical insult falls as the "
              "residual self-drive nears the deletion threshold so deeper negative selection lowers susceptibility "
              "-- measured, not assumed; [O] absolute break rate / boundary timing (residual depth, insult "
              "amplitude / duration, cellular-noise scale D)")


def run(gammas):
    """T23: emergent autoimmune tolerance break -- an escaped self-clone's bistable latch under an inflammatory insult MEASURED, with a saddle-node break boundary, irreversible persistence, and a negative-selection-depth susceptibility link."""
    r = emergent_autoimmunity(gammas)
    return dict(T23=dict(target="T23",
                         claim="autoimmune tolerance break EMERGES from combining the T9 inflammatory latch with a "
                               "T21 escaped self-clone (sub-spinodal residual self-drive, so bistable): an "
                               "inflammatory insult breaks tolerance past a saddle-node boundary (measured total "
                               "drive = spinodal, self-antigen and inflammation interchangeable), the break is "
                               "irreversible -- it latches ON and persists after the insult clears, the pathological "
                               "mirror of immune memory -- with a dose×time tradeoff, and the critical insult falls "
                               "as the residual self-drive nears the deletion threshold, so deeper central tolerance "
                               "(T21) lowers autoimmune susceptibility -- measured, not assumed; absolute break rate "
                               "stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T23"]["result"]
    print("AUTOIMMUNE TOLERANCE BREAK on an escaped self-clone (primary=%s, γ=%.4f, spinodal=%.4f, D=%.3f):"
          % (r["primary"], r["gamma"], r["spinodal"], r["noise_D"]))
    print("\n(1a) no-residual critical insult == spinodal, organ by organ:")
    for o, row in r["no_residual_critical_insult"].items():
        print("     %-28s insult_crit=%.3f×sp  matches=%s" % (o, row["insult_crit_over_spinodal"], row["matches_spinodal"]))
    print("     -> all organs: %s" % r["no_residual_critical_equals_spinodal"])
    print("\n(1b) TOTAL-DRIVE INVARIANT (residual self-drive + critical insult == 1×spinodal):")
    for row in r["total_drive_invariant"]:
        print("     residual=%.2f  critical_insult=%.3f  total=%.3f×sp  ==spinodal:%s"
              % (row["residual_self_drive"], row["critical_insult"], row["total_drive_over_spinodal"], row["equals_spinodal"]))
    print("     -> invariant holds: %s" % r["total_drive_invariant_holds"])
    p = r["persistence"]
    print("\n(2) IRREVERSIBLE PERSISTENCE (pathological memory), escaped clone residual=%.2f, critical insult=%.3f:"
          % (r["residual_self_drive_ref"], p["critical_insult"]))
    print("     supra-threshold insult: P(break)=%.3f ; tripled settle: %.3f -> persists=%s"
          % (p["p_break_supra"], p["p_break_supra_tripled_settle"], p["irreversible_persists"]))
    print("     sub-threshold insult: P(break)=%.3f -> resolves=%s ; far-below control P=%.3f -> safe=%s"
          % (p["p_break_sub"], p["sub_threshold_resolves"], p["p_far_below"], p["far_below_safe"]))
    print("\n(3) DOSE × TIME TRADEOFF (min breaking duration falls as insult rises):")
    for row in r["dose_time_tradeoff"]:
        print("     total=%.2f×sp (insult=%.2f)  d_crit=%s" % (row["total_drive_over_spinodal"], row["insult_over_spinodal"], row["d_crit"]))
    print("     -> monotone decreasing: %s" % r["dose_time_monotone"])
    print("\n(4) SUSCEPTIBILITY vs NEGATIVE-SELECTION DEPTH (critical insult falls as residual self-drive rises):")
    for row in r["susceptibility_vs_deletion_depth"]:
        print("     residual_self_drive=%.2f  critical_insult=%.3f×sp" % (row["residual_self_drive"], row["critical_insult"]))
    print("     -> deeper deletion (smaller residual) => higher critical insult => lower susceptibility: %s" % r["susceptibility_monotone"])
    print("\nT23 all_pass:", r["all_pass"])
