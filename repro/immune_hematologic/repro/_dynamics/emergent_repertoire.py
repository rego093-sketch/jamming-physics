#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_repertoire.py  --  EMERGENT N-clone repertoire dominance by a COUPLED stochastic competition (not asserted).

WHY THIS EXISTS (v0.7.0). T12 (emergent_competition.py) shows immunodominance for TWO clones racing for one
shared antigen pool. A real adaptive response is a REPERTOIRE: many clones with a distribution of affinities
compete for the same finite pool, and the response ends up concentrated on a few high-affinity clones (the
immunodominance hierarchy). The VP discipline is emergence: that concentration — and how it scales with
repertoire size and affinity spread — must come OUT of the coupled substrate dynamics, MEASURED, not assumed.
This module generalises T12 to N clones (R19 switches of the SAME adaptive-lymphoid γ) on one shared pool A(t):

    aff_i = linearly-spaced affinity ladder of width `spread` about a mean (a uniform affinity distribution)
    h_i(t) = aff_i · A(t)                                             (drive ∝ affinity × available antigen)
    ds_i  = (γ s_i − s_i³ + h_i) dt + sqrt(2 D dt) · ξ_i,   start OFF s_i = −√γ     (all clones resting)
    dA/dt = −consume · (#committed clones),   A ≥ 0                   (committed clones deplete the pool)

Over a population of independent hosts the per-clone commit probabilities p_i are MEASURED, and the dominance
concentration is read off them with two standard measures: the dominant-set size (# clones with p_i>½) and the
participation ratio N_eff = (Σp_i)² / Σ(p_i²) (the effective number of responding clones — 1 if one clone takes
everything, N if all respond equally). Nothing about a hierarchy is assumed; the concentration is a counted
statistic of the coupled dynamics. The affinity ladder's width and the repertoire size are then swept.

WHAT EMERGES (measured, deterministic seed=19):
  1. A FEW CLONES DOMINATE. At a moderate repertoire and spread the measured N_eff is far below the repertoire
     size N (a small dominant set), and the per-clone commit probability is monotone in affinity rank — the top
     affinities capture the response and the rest are competitively excluded. Immunodominance over a repertoire
     EMERGES from the coupling; it is not imposed.
  2. WIDER SPREAD → MORE CONCENTRATED. As the affinity spread widens the measured N_eff falls monotonically
     (fewer clones capture the response): a steeper affinity distribution sharpens dominance, MEASURED.
  3. LARGER REPERTOIRE → MORE CONCENTRATED (relatively). As the repertoire size N grows at fixed spread the
     dominant set does not scale with N (the shared pool sustains only a few committers), so the relative
     concentration N_eff/N falls — bigger repertoires are MORE focused, MEASURED.
  4. SYMMETRIC AT ZERO SPREAD (honest limit). At zero affinity spread there is no affinity hierarchy: the
     commit probabilities are essentially equal across clones (N_eff ≈ the pool-supported set, with no spurious
     winner). The depth of the hierarchy is set by the affinity spread relative to the noise — direction and
     scaling are measured; the absolute depth is [O].

GRADES (C3): the few-clones-dominate concentration, the sharpening with affinity spread, the relative
sharpening with repertoire size, and the symmetric zero-spread limit are [V] emergent (measured from the
coupled stochastic model). The ABSOLUTE hierarchy depth — set by the consumption rate, pool size, and the free
cellular-noise scale D — is [O], no fabricated dominance numbers. Determinism: fixed seed, BLAS pinned upstream,
round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGAN    = "lymphoid_adaptive"        # the adaptive compartment (PAX5): a repertoire of clones on one pool

# --- deterministic simulation size (fixed; no per-condition tuning) ----------------------------------
_M        = 170       # independent hosts per condition
_DT       = 0.01      # Langevin timestep
_T        = 30.0      # response horizon
_D        = 0.02      # cellular-noise scale (absolute value is [O])
_CONSUME  = 0.5       # antigen consumption rate per committed clone (sets hierarchy depth; [O])
_A0       = 1.0       # initial shared antigen pool (arbitrary unit; [O])
_AFF_MEAN = 0.88      # mean clone affinity (× — aff_mean·A0 clears the spinodal; the ladder straddles it)
_N_BASE   = 12        # baseline repertoire size
_SPREAD_BASE = 0.45   # baseline affinity-ladder width
_SPREADS  = (0.0, 0.15, 0.30, 0.45)    # affinity-ladder widths (fixed N): 0 = equal affinity
_NCLONES  = (4, 8, 12, 16)             # repertoire sizes (fixed spread)


def _affinities(n, spread, mean=_AFF_MEAN):
    """Linearly-spaced affinity ladder of width `spread` about `mean` (a uniform affinity distribution)."""
    if n == 1:
        return np.array([mean])
    return mean + np.linspace(-spread / 2.0, spread / 2.0, n)


def compete_repertoire(g, aff, D=_D, M=_M, dt=_DT, T=_T, consume=_CONSUME, A0=_A0, seed=SEED):
    """MEASURE per-clone commit probabilities for a repertoire of len(aff) clones racing for one shared pool."""
    n = len(aff)
    rng = np.random.default_rng(seed)
    s = np.full((M, n), -math.sqrt(g))            # all clones resting (OFF)
    A = np.full(M, A0)                            # shared pool per host
    committed = np.zeros((M, n), dtype=bool)
    sq = math.sqrt(2.0 * D * dt)
    aff_row = aff[None, :]
    for _ in range(int(T / dt)):
        h = aff_row * A[:, None]                  # drive ∝ affinity × available antigen
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal((M, n))
        np.clip(s, -5.0, 5.0, out=s)
        on = s > 0.0
        committed |= on
        A -= consume * on.sum(axis=1) * dt        # committed clones deplete the shared pool
        np.clip(A, 0.0, None, out=A)
    return committed.mean(axis=0)                 # p_i = commit probability of clone i across hosts


def _concentration(p):
    """Dominance concentration from per-clone commit probabilities p_i."""
    p = np.asarray(p, float)
    s1 = float(p.sum()); s2 = float((p ** 2).sum())
    n_eff = (s1 * s1 / s2) if s2 > 0 else 0.0     # participation ratio: effective # responding clones
    dom_set = int((p > 0.5).sum())                # # clones that reliably commit
    return n_eff, dom_set, s1


def _rank_monotone(p, aff):
    """Commit probability is monotone non-increasing in DESCENDING affinity rank (top affinity wins)."""
    order = np.argsort(-np.asarray(aff))          # highest affinity first
    pr = np.asarray(p)[order]
    return all(pr[i + 1] <= pr[i] + 0.06 for i in range(len(pr) - 1))   # tolerance for stochastic ties


def emergent_repertoire(gammas):
    g = gammas[_ORGAN]; sp = spinodal(g)

    # ---- experiment A: fix N, vary affinity spread ------------------------------------------------
    expA = []
    for k, spread in enumerate(_SPREADS):
        aff = _affinities(_N_BASE, spread)
        p = compete_repertoire(g, aff, seed=SEED + k)
        n_eff, dom, _ = _concentration(p)
        expA.append(dict(spread=round(spread, 3), N=_N_BASE,
                         N_eff=round(n_eff, 3), dominant_set=dom,
                         commit_prob=[round(float(x), 3) for x in p],
                         rank_monotone=bool(_rank_monotone(p, aff))))
    neff_A = [r["N_eff"] for r in expA]
    spread_sharpens = all(neff_A[i + 1] <= neff_A[i] + 1e-6 for i in range(len(neff_A) - 1))
    spread_clear = bool(neff_A[-1] < neff_A[0] - 0.5)                  # max spread clearly tighter than zero spread
    # symmetric at zero spread: equal affinities -> no hierarchy -> N_eff ≈ N (all clones participate equally)
    symmetric_zero = bool(expA[0]["N_eff"] / _N_BASE > 0.85)

    # ---- experiment B: fix spread, vary repertoire size N -----------------------------------------
    expB = []
    for k, n in enumerate(_NCLONES):
        aff = _affinities(n, _SPREAD_BASE)
        p = compete_repertoire(g, aff, seed=SEED + 100 + k)
        n_eff, dom, _ = _concentration(p)
        expB.append(dict(N=n, spread=round(_SPREAD_BASE, 3),
                         N_eff=round(n_eff, 3), dominant_set=dom,
                         relative_concentration=round(n_eff / n, 4),
                         rank_monotone=bool(_rank_monotone(p, aff))))
    rel_B = [r["relative_concentration"] for r in expB]
    biggerN_concentrates = all(rel_B[i + 1] <= rel_B[i] + 1e-6 for i in range(len(rel_B) - 1))

    # ---- baseline (N=12, spread=0.30): few clones dominate ----------------------------------------
    base = [r for r in expB if r["N"] == _N_BASE][0] if any(r["N"] == _N_BASE for r in expB) else expA[-1]
    few_dominate = bool(base["N_eff"] < _N_BASE / 2.0 and base["rank_monotone"])

    ok = bool(few_dominate and spread_sharpens and spread_clear and biggerN_concentrates and symmetric_zero)
    return dict(
        organ=_ORGAN, gamma=round(g, 6), spinodal=round(sp, 6),
        noise_D=_D, consume=_CONSUME, antigen_pool_A0=_A0, affinity_mean=_AFF_MEAN,
        experiment_A_vary_spread=expA,
        experiment_B_vary_N=expB,
        baseline=dict(N=base["N"], spread=base["spread"], N_eff=base["N_eff"],
                      dominant_set=base["dominant_set"], rank_monotone=base["rank_monotone"]),
        few_clones_dominate=bool(few_dominate),
        wider_spread_more_concentrated=bool(spread_sharpens and spread_clear),
        larger_repertoire_more_concentrated=bool(biggerN_concentrates),
        symmetric_at_zero_spread=bool(symmetric_zero),
        all_pass=ok,
        grade="[V] N-clone repertoire dominance EMERGES from a coupled stochastic shared-antigen competition: "
              "a few high-affinity clones capture the response (measured N_eff ≪ N, commit probability monotone "
              "in affinity rank), the concentration sharpens monotonically with the affinity spread and (relative "
              "to N) with repertoire size, and the zero-spread limit is symmetric — measured, not assumed; [O] "
              "absolute hierarchy depth (consumption rate, pool size, cellular-noise scale D)")


def run(gammas):
    """T16: emergent N-clone repertoire dominance — concentration MEASURED from a coupled stochastic competition."""
    r = emergent_repertoire(gammas)
    return dict(T16=dict(target="T16",
                         claim="repertoire-level immunodominance EMERGES from a coupled stochastic competition "
                               "of N clones for one shared antigen pool: the response concentrates on a few "
                               "high-affinity clones (measured participation ratio N_eff ≪ N, commit probability "
                               "monotone in affinity rank), the concentration sharpens with the affinity spread "
                               "and, relative to N, with repertoire size, and is symmetric at zero spread — "
                               "measured, not assumed; absolute hierarchy depth stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T16"]["result"]
    print("N-clone repertoire dominance in the adaptive lymphoid compartment (γ=%.4f, spinodal=%.4f):"
          % (r["gamma"], r["spinodal"]))
    print("\nexperiment A — fix N=%d, vary affinity spread:" % _N_BASE)
    print("  spread   N_eff   dominant_set   rank_monotone")
    for row in r["experiment_A_vary_spread"]:
        print("   %.2f     %.2f        %d            %s" % (row["spread"], row["N_eff"], row["dominant_set"], row["rank_monotone"]))
    print("\nexperiment B — fix spread=%.2f, vary repertoire size N:" % _SPREAD_BASE)
    print("   N    N_eff   dominant_set   N_eff/N")
    for row in r["experiment_B_vary_N"]:
        print("  %2d    %.2f        %d          %.3f" % (row["N"], row["N_eff"], row["dominant_set"], row["relative_concentration"]))
    print("\nbaseline (N=%d, spread=%.2f): N_eff=%.2f dominant_set=%d"
          % (r["baseline"]["N"], r["baseline"]["spread"], r["baseline"]["N_eff"], r["baseline"]["dominant_set"]))
    print("few clones dominate:               ", r["few_clones_dominate"])
    print("wider spread more concentrated:    ", r["wider_spread_more_concentrated"])
    print("larger repertoire more concentrated:", r["larger_repertoire_more_concentrated"])
    print("symmetric at zero spread:          ", r["symmetric_at_zero_spread"])
    print("T16 all_pass:", r["all_pass"])
