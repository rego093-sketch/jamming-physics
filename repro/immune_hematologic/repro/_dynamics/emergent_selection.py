#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_selection.py  --  EMERGENT clonal-selection threshold by DIRECT stochastic simulation (not asserted).

WHY THIS EXISTS (v0.6.0). clonal_inflammation.py (T1) ASSERTS that a lymphocyte clone activates as a
saddle-node at the spinodal: it computes the spinodal |h|=2(γ/3)^1.5 analytically and checks the
deterministic settle flips there. That threshold is read off the closed-form, not emerged. The VP
discipline is emergence: the activation threshold must come OUT of the substrate dynamics, MEASURED, not
plugged in. This module does that. A resting clone (the OFF basin, s=−√γ) is driven by a slowly RISING
antigen-affinity signal h(t) under independent cellular noise,

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt) · ξ,    ξ ~ N(0,1),    h(t): h_lo → h_hi (slow ramp)

and the affinity drive h* at which each clone FIRST commits across the ridge s>0 is MEASURED. Over a
population the mean commit-drive is a counted statistic; nothing about the spinodal is assumed in the
measurement. The independently-computed spinodal is only used afterwards, to compare against.

WHAT EMERGES (measured, deterministic seed=19):
  1. COMMIT-DRIVE = SPINODAL, organ by organ. The measured mean affinity drive at commitment lands on the
     organ's own spinodal (ratio ≈ 0.98–0.99 at low noise — the small deficit is honest: thermal activation
     lets a clone cross slightly before the barrier fully vanishes, and the ratio → 1 as D → 0). So the
     saddle-node activation threshold IS the spinodal of the measured γ, MEASURED not posited.
  2. THE THRESHOLD ORDERS BY γ. The measured commit-drives rank in ascending-γ order across the four
     organs — higher-γ (deeper-well) compartments demand a stronger affinity signal to activate.
  3. SUB-SPINODAL = SELF-TOLERANCE, SUPRA-SPINODAL = COMMITMENT. At a fixed drive clearly below the
     spinodal a clone essentially never commits however long it is held (P(commit) ≈ 0 — this is tolerance);
     at a fixed drive clearly above the spinodal it commits with probability ≈ 1. The transition straddles
     the spinodal, MEASURED, so self-tolerance is just the sub-spinodal region of the one switch.

GRADES (C3): the activation threshold (= spinodal, organ-by-organ), its γ-ordering, and the
tolerance/commitment bracket are [V] emergent (measured by simulation). The ABSOLUTE noise scale D (which
sets the exact size of the small sub-spinodal deficit and the transition sharpness) is [O], the same free
cellular-noise scale as T7/T8/T9. Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]   # ascending-γ expectation

# --- deterministic simulation size (fixed; slow ramp + low noise -> sharp threshold; no per-organ tuning) -
_N        = 450      # clones per organ
_DT       = 0.01     # Langevin timestep
_H_LO     = 0.30     # ramp start (well below every organ's spinodal)
_H_HI     = 0.80     # ramp end   (above every organ's spinodal)
_T_RAMP   = 100.0    # ramp duration (slow -> quasi-static commit at the vanishing barrier)
_D        = 0.01     # cellular-noise scale (low: sharp threshold; absolute value is [O])
_N_FIX    = 500      # clones per fixed-drive tolerance/commitment probe
_T_FIX    = 40.0     # horizon for the fixed-drive probe
_SUB_FRAC = 0.70     # clearly sub-spinodal drive (self-tolerance)
_SUP_FRAC = 1.15     # clearly supra-spinodal drive (commitment)


def ramp_commit_drive(g, D=_D, N=_N, dt=_DT, h_lo=_H_LO, h_hi=_H_HI, T=_T_RAMP, seed=SEED):
    """MEASURED mean affinity drive at commitment: ramp h slowly, count the drive at first ridge crossing. No formula."""
    rng = np.random.default_rng(seed)
    s = np.full(N, -math.sqrt(g))                 # all clones start resting (OFF basin)
    committed = np.zeros(N, dtype=bool)
    hcommit = np.full(N, h_hi)
    sq = math.sqrt(2.0 * D * dt)
    nsteps = int(T / dt)
    for i in range(nsteps):
        h = h_lo + (h_hi - h_lo) * (i * dt / T)
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        newly = (~committed) & (s > 0.0)          # crossed the ridge into the activated basin
        if newly.any():
            hcommit[newly] = h
            committed[newly] = True
        if committed.all():
            break
    return float(hcommit.mean()), float(committed.mean())


def p_commit_fixed(g, frac, D=_D, N=_N_FIX, dt=_DT, T=_T_FIX, seed=SEED):
    """MEASURED probability a clone commits at a FIXED drive = frac·spinodal held for the horizon."""
    rng = np.random.default_rng(seed)
    s = np.full(N, -math.sqrt(g))
    committed = np.zeros(N, dtype=bool)
    sq = math.sqrt(2.0 * D * dt)
    h = frac * spinodal(g)
    for i in range(int(T / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        committed |= (s > 0.0)
        if committed.all():
            break
    return float(committed.mean())


def emergent_selection(gammas, D=_D):
    """Measure the commit-drive per organ by simulation; test threshold=spinodal, γ-ordering, tolerance bracket."""
    # (1) measured commit-drive == spinodal, organ by organ
    rows, commit_h, thresh_ok = {}, {}, True
    for o in _ORGANS:
        g = gammas[o]; sp = spinodal(g)
        mean_h, frac_c = ramp_commit_drive(g, D=D)
        commit_h[o] = mean_h
        ratio = mean_h / sp if sp > 0 else float("nan")
        matches = bool(0.90 <= ratio <= 1.05 and frac_c > 0.99)      # near the spinodal, from below (thermal)
        rows[o] = dict(spinodal=round(sp, 6), measured_commit_drive=round(mean_h, 6),
                       commit_drive_over_spinodal=round(ratio, 3), fraction_committed=round(frac_c, 3),
                       matches_spinodal=matches)
        thresh_ok = thresh_ok and matches

    # (2) the measured threshold ORDERS by γ (ascending commit-drive == ascending γ)
    order_commit = sorted(_ORGANS, key=lambda o: commit_h[o])
    order_gamma  = sorted(_ORGANS, key=lambda o: gammas[o])
    ordering_emerges = (order_commit == order_gamma)

    # (3) sub-spinodal = tolerance, supra-spinodal = commitment, organ by organ (the bracket straddles spinodal)
    bracket, bracket_ok = {}, True
    for o in _ORGANS:
        p_sub = p_commit_fixed(gammas[o], _SUB_FRAC, D=D)
        p_sup = p_commit_fixed(gammas[o], _SUP_FRAC, D=D)
        ok = bool(p_sub < 0.10 and p_sup > 0.90)
        bracket[o] = dict(p_commit_subspinodal=round(p_sub, 3), p_commit_supraspinodal=round(p_sup, 3),
                          tolerant_below_committed_above=ok)
        bracket_ok = bracket_ok and ok

    ok = bool(thresh_ok and ordering_emerges and bracket_ok)
    return dict(
        noise_D=D, sub_frac=_SUB_FRAC, sup_frac=_SUP_FRAC,
        commit_drive=rows,
        commit_drive_equals_spinodal=bool(thresh_ok),
        commit_drive_order_ascending=order_commit,
        gamma_order_ascending=order_gamma,
        threshold_orders_by_gamma=bool(ordering_emerges),
        tolerance_commitment_bracket=bracket,
        subspinodal_tolerant_supraspinodal_committed=bool(bracket_ok),
        all_pass=ok,
        grade="[V] the clonal-selection activation threshold (= spinodal organ-by-organ), its γ-ordering, "
              "and the sub-spinodal-tolerance / supra-spinodal-commitment bracket EMERGE from a direct "
              "stochastic rising-affinity simulation of the R19 switch (measured, not asserted from the "
              "closed-form spinodal); [O] absolute noise scale D (sub-spinodal deficit / transition sharpness)")


def run(gammas):
    """T11: emergent clonal-selection threshold — the activation drive MEASURED from a stochastic rising-affinity sim, not asserted as the spinodal."""
    r = emergent_selection(gammas)
    return dict(T11=dict(target="T11",
                         claim="clonal-selection activation EMERGES from a direct stochastic rising-affinity "
                               "simulation of the R19 switch: the measured commit-drive equals each organ's "
                               "spinodal (from below, by thermal activation), the threshold orders by γ, and "
                               "a sub-spinodal drive stays tolerant while a supra-spinodal drive commits — "
                               "the saddle-node threshold is measured, not asserted from the closed-form; "
                               "absolute noise scale D stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T11"]["result"]
    print("commit-drive vs spinodal per organ:")
    for o, v in r["commit_drive"].items():
        print("    %-26s commit=%.4f  spinodal=%.4f  ratio=%.3f  (matches=%s)"
              % (o, v["measured_commit_drive"], v["spinodal"], v["commit_drive_over_spinodal"], v["matches_spinodal"]))
    print("commit-drive == spinodal (all organs):", r["commit_drive_equals_spinodal"])
    print("threshold orders by γ:", r["threshold_orders_by_gamma"],
          "| commit order:", r["commit_drive_order_ascending"])
    print("tolerance/commitment bracket:")
    for o, v in r["tolerance_commitment_bracket"].items():
        print("    %-26s P(commit|0.70sp)=%.3f  P(commit|1.15sp)=%.3f  (ok=%s)"
              % (o, v["p_commit_subspinodal"], v["p_commit_supraspinodal"], v["tolerant_below_committed_above"]))
    print("T11 all_pass:", r["all_pass"])
