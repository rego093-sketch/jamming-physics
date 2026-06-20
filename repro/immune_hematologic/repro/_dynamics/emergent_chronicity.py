#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_chronicity.py  --  EMERGENT acute/chronic boundary by DIRECT stochastic simulation (not asserted).

WHY THIS EXISTS (v0.5.0). clonal_inflammation.py (T2) states the hysteresis loop width is 2×spinodal and
that a sub-spinodal pulse resolves while a supra-spinodal sustained drive latches. That is the analytic
statement of the loop. The VP discipline is emergence: the chronicity boundary in the real control plane —
insult AMPLITUDE × insult DURATION — must come OUT of the substrate dynamics, MEASURED. This module does
that. It drives a single R19 switch (an inflammatory cell, starting in the resting OFF basin) with a
rectangular insult of amplitude a·spinodal held for a duration, under cellular noise,

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt) · ξ,   h = a·spinodal during the pulse, then h = 0,

then WITHDRAWS the drive, lets the field settle, and MEASURES the basin it lands in — resting (OFF, the
insult RESOLVED = acute) or latched (ON, chronic). Sweeping amplitude × duration over a population of cells
MEASURES P(latch) across the (amplitude, duration) plane. Nothing about the boundary is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. CRITICAL AMPLITUDE = SPINODAL, organ by organ. At long duration the amplitude at which P(latch) crosses
     0.5 lands on the organ's own spinodal (a_crit/spinodal ≈ 1 for all four organs) — the chronicity
     amplitude threshold IS the saddle-node of that organ's measured γ, MEASURED not posited.
  2. SUB-SPINODAL NEVER CHRONIC. An amplitude clearly below the spinodal does not latch even at the longest
     duration — acute inflammation resolves no matter how long a too-weak insult is held.
  3. DOSE × TIME TRADEOFF. Above the spinodal, the minimum latching duration d_crit DECREASES monotonically
     as amplitude rises: a stronger insult needs less time to become chronic. This is the measured
     "dose × time" face of chronicity that the analytic loop width alone does not express.

GRADES (C3): chronicity boundary shape — critical-amplitude=spinodal, sub-spinodal-safe, and the monotone
dose×time tradeoff — [V] emergent (measured by simulation). The ABSOLUTE noise scale D (which sets how
sharp the transition is and the exact d_crit values) is [O], the same free cellular-noise scale as T7/T8.
Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]

# --- deterministic simulation size (fixed; low noise -> sharp boundary; no per-organ tuning) ---------
_N      = 300       # cells per (amplitude, duration) condition
_DT     = 0.01      # integration timestep
_RELAX  = 1000      # settle steps after the insult is withdrawn (decide final basin)
_D      = 0.02      # cellular-noise scale (low: sharp boundary; absolute value is [O])
_DUR_LONG = 800     # "long" insult duration for the amplitude threshold
_AMPS   = (0.70, 0.85, 0.95, 1.00, 1.05, 1.15, 1.30)         # amplitude grid (× spinodal) bracketing threshold
_DUR_GRID = (50, 100, 150, 200, 300, 400, 550, 700, 900)     # duration grid for the dose×time tradeoff
_SUPRA  = (1.10, 1.25, 1.50, 2.00)                           # supra-spinodal amplitudes for d_crit


def p_latch(g, a_frac, dur, D=_D, N=_N, dt=_DT, relax=_RELAX, seed=SEED):
    """MEASURED probability the insult latches ON: pulse a·spinodal for `dur` steps from OFF, withdraw, settle."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))                 # start in the resting (OFF) basin
    sq = math.sqrt(2.0 * D * dt)
    h = a_frac * sp
    for _ in range(int(dur)):                     # apply the insult
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    for _ in range(relax):                        # withdraw, let it decide a basin
        s += (g * s - s ** 3) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _amp_threshold(g, dur=_DUR_LONG, amps=_AMPS, D=_D):
    """Interpolate the amplitude (× spinodal) at which P(latch) crosses 0.5 at long duration."""
    ps = [p_latch(g, a, dur, D=D) for a in amps]
    for i in range(len(amps) - 1):
        if ps[i] < 0.5 <= ps[i + 1]:
            a = amps[i] + (0.5 - ps[i]) * (amps[i + 1] - amps[i]) / (ps[i + 1] - ps[i])
            return float(a), ps
    return float("nan"), ps


def _dur_threshold(g, a_frac, durs=_DUR_GRID, D=_D):
    """Smallest insult duration (in steps) for which P(latch) >= 0.5 at fixed amplitude."""
    for d in durs:
        if p_latch(g, a_frac, d, D=D) >= 0.5:
            return int(d)
    return None


def emergent_chronicity(gammas, D=_D):
    # (1) critical amplitude == spinodal, organ by organ
    amp_rows = {}
    crit_ok = True
    for o in _ORGANS:
        a_crit, _ = _amp_threshold(gammas[o], D=D)
        ratio = a_crit  # a_crit is already in units of the organ's spinodal
        amp_rows[o] = dict(a_crit_over_spinodal=round(ratio, 3),
                           matches_spinodal=bool(abs(ratio - 1.0) < 0.10))
        crit_ok = crit_ok and amp_rows[o]["matches_spinodal"]

    # (2) sub-spinodal never chronic (longest duration, clearly sub-threshold amplitude)
    g_ref = gammas["bone_marrow_hematopoiesis"]
    p_sub_long = p_latch(g_ref, 0.70, _DUR_GRID[-1], D=D)
    sub_safe = bool(p_sub_long < 0.10)

    # (3) dose x time tradeoff: d_crit DECREASES monotonically as amplitude rises (on the marrow switch)
    dcrit = {}
    for a in _SUPRA:
        dcrit[a] = _dur_threshold(g_ref, a, D=D)
    have = [a for a in _SUPRA if dcrit[a] is not None]
    vals = [dcrit[a] for a in have]
    tradeoff_monotone = bool(len(vals) >= 3 and all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)))

    ok = bool(crit_ok and sub_safe and tradeoff_monotone)
    return dict(
        noise_D=D,
        critical_amplitude=amp_rows,
        critical_amplitude_equals_spinodal=bool(crit_ok),
        subspinodal_p_latch_long_duration=round(p_sub_long, 3),
        subspinodal_never_chronic=bool(sub_safe),
        dose_time_d_crit_steps={("a=%.2f*sp" % a): dcrit[a] for a in _SUPRA},
        dose_time_tradeoff_monotone=bool(tradeoff_monotone),
        all_pass=ok,
        grade="[V] chronicity boundary (critical amplitude = spinodal organ-by-organ; sub-spinodal never "
              "latches; monotone dose×time tradeoff) EMERGES from a direct stochastic pulse simulation "
              "(measured, not asserted); [O] absolute noise scale D (transition sharpness / exact d_crit)")


def run(gammas):
    """T9: emergent acute/chronic boundary — the (amplitude × duration) chronicity boundary MEASURED from stochastic pulses."""
    r = emergent_chronicity(gammas)
    return dict(T9=dict(target="T9",
                        claim="the acute/chronic boundary EMERGES in the (insult amplitude × duration) plane "
                              "from direct stochastic pulse simulation of the R19 switch: the critical "
                              "amplitude equals each organ's spinodal, a sub-spinodal insult never becomes "
                              "chronic however long it is held, and the minimum latching duration falls "
                              "monotonically as amplitude rises (dose×time) — not asserted from the loop "
                              "width; absolute noise scale D stays [O]",
                        result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T9"]["result"]
    print("critical amplitude / spinodal per organ:")
    for o, v in r["critical_amplitude"].items():
        print("    %-26s a_crit/sp = %.3f  (matches spinodal=%s)" % (o, v["a_crit_over_spinodal"], v["matches_spinodal"]))
    print("critical amplitude == spinodal (all organs):", r["critical_amplitude_equals_spinodal"])
    print("sub-spinodal P(latch) at longest duration: %.3f -> never chronic: %s"
          % (r["subspinodal_p_latch_long_duration"], r["subspinodal_never_chronic"]))
    print("dose x time d_crit (steps):", r["dose_time_d_crit_steps"], "-> monotone:", r["dose_time_tradeoff_monotone"])
    print("T9 all_pass:", r["all_pass"])
