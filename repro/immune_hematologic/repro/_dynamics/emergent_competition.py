#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_competition.py  --  EMERGENT immunodominance by a COUPLED stochastic competition model (not asserted).

WHY THIS EXISTS (v0.6.0). T1/T11 treat a single clone in isolation. Real adaptive responses are a
COMPETITION: many clones of the adaptive lymphoid compartment race for one shared, finite antigen pool, and
the response ends up dominated by a few high-affinity clones (immunodominance / clonal competition). VP did
not yet have this as an emergent result. The discipline is emergence: immunodominance must come OUT of the
coupled substrate dynamics, MEASURED, not be assumed. This module does that. Two clones (two R19 switches of
the SAME adaptive-lymphoid γ, differing only in antigen affinity) share one antigen pool A(t):

    h_i(t) = aff_i · A(t)                                              (drive ∝ affinity × available antigen)
    ds_i  = (γ s_i − s_i³ + h_i) dt + sqrt(2 D dt) · ξ_i,   start OFF s_i = −√γ      (both resting)
    dA/dt = −consume · (#committed clones),   A ≥ 0                    (committed clones deplete the pool)

The higher-affinity clone reaches its spinodal first, commits, and STARTS CONSUMING the shared antigen,
which lowers the drive available to the lower-affinity clone. Over a population of independent hosts the
commit fractions, the order of commitment, and the subdominant clone's commit probability are all MEASURED.
Nothing about a hierarchy is assumed; immunodominance is a counted outcome of the coupled dynamics. The
NO-competition baseline (A held fixed) is measured the same way for contrast.

WHAT EMERGES (measured, deterministic seed=19):
  1. COMPETITIVE EXCLUSION (winner-take-all). The subdominant clone commits with probability ≈ 1 when it is
     ALONE (its affinity drive clears the spinodal), but its commit probability COLLAPSES under competition
     once the dominant clone depletes the shared pool — the response is captured by the dominant clone. This
     winner-take-all hierarchy EMERGES from the coupling; it is not imposed.
  2. THE HIGHER-AFFINITY CLONE COMMITS FIRST (direction). At a substantial affinity gap the dominant clone
     reliably commits before the subdominant one (P(dominant first) ≫ 0.5) and reaches commitment with
     probability ≈ 1 — the direction of dominance tracks affinity, MEASURED.
  3. MONOTONE IN THE AFFINITY GAP, SYMMETRIC AT ZERO. As the affinity gap widens, dominance sharpens
     monotonically: P(dominant first) rises and the subdominant commit probability falls. At zero gap (equal
     affinity) the contest is a symmetric coin-flip (P(first) ≈ 0.5, equal commit fractions) — there is no
     spurious hierarchy when affinities are equal. Honest: the depth of the hierarchy is set by the affinity
     gap relative to the noise.

GRADES (C3): competitive exclusion, the affinity-ordered direction of dominance, the monotone-in-gap
sharpening, and the symmetric zero-gap limit are [V] emergent (measured from the coupled stochastic model).
The ABSOLUTE hierarchy depth / exact suppression magnitude — set by the consumption rate, pool size, and the
free cellular-noise scale D — is [O], no fabricated dominance ratios. Determinism: fixed seed, BLAS pinned
upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

# Immunodominance lives in the ADAPTIVE LYMPHOID compartment (PAX5) — clones of one pool competing.
_ORGAN   = "lymphoid_adaptive"

# --- deterministic simulation size (fixed; no per-condition tuning) ----------------------------------
_N        = 380      # independent hosts per condition
_DT       = 0.01     # Langevin timestep
_T        = 50.0     # response horizon
_D        = 0.02     # cellular-noise scale (absolute value is [O])
_CONSUME  = 0.6      # antigen consumption rate per committed clone (sets hierarchy depth; [O])
_A0       = 1.0      # initial shared antigen pool (arbitrary unit; [O])
_AFF_DOM  = 0.95     # dominant clone affinity (× — so aff·A0 just clears the spinodal at full pool)
_GAPS     = (0.00, 0.05, 0.10, 0.15, 0.20)   # affinity gaps (subdominant = dominant − gap)


def compete(g, aff1, aff2, coupled, D=_D, N=_N, dt=_DT, T=_T, consume=_CONSUME, A0=_A0, seed=SEED):
    """MEASURE two clones racing for a shared antigen pool. Returns (commit1, commit2, P(clone1 first)).
    coupled=True: committed clones deplete A (competition). coupled=False: A fixed (no-competition baseline)."""
    rng = np.random.default_rng(seed)
    s1 = np.full(N, -math.sqrt(g)); s2 = np.full(N, -math.sqrt(g))
    A  = np.full(N, A0)
    c1 = np.zeros(N, dtype=bool);   c2 = np.zeros(N, dtype=bool)
    t1 = np.full(N, np.inf);        t2 = np.full(N, np.inf)
    sq = math.sqrt(2.0 * D * dt)
    for i in range(int(T / dt)):
        h1 = aff1 * A; h2 = aff2 * A
        s1 += (g * s1 - s1 ** 3 + h1) * dt + sq * rng.standard_normal(N); np.clip(s1, -5.0, 5.0, out=s1)
        s2 += (g * s2 - s2 ** 3 + h2) * dt + sq * rng.standard_normal(N); np.clip(s2, -5.0, 5.0, out=s2)
        n1 = (~c1) & (s1 > 0.0); n2 = (~c2) & (s2 > 0.0)
        if n1.any(): t1[n1] = i * dt; c1[n1] = True
        if n2.any(): t2[n2] = i * dt; c2[n2] = True
        if coupled:
            oncount = (s1 > 0.0).astype(float) + (s2 > 0.0).astype(float)
            A -= consume * oncount * dt
            np.clip(A, 0.0, None, out=A)
    return float(c1.mean()), float(c2.mean()), float((t1 < t2).mean())


def emergent_competition(gammas, gaps=_GAPS, aff_dom=_AFF_DOM):
    g = gammas[_ORGAN]; sp = spinodal(g)
    rows = []
    for gap in gaps:
        aff_sub = aff_dom - gap
        dom_c, sub_c, dom_first = compete(g, aff_dom, aff_sub, coupled=True)      # competition
        _, sub_alone, _         = compete(g, aff_dom, aff_sub, coupled=False)     # subdominant alone (baseline)
        suppression = (sub_alone - sub_c)                                          # how much competition removes
        rows.append(dict(affinity_gap=round(gap, 3), aff_dominant=round(aff_dom, 3), aff_subdominant=round(aff_sub, 3),
                         dominant_commit=round(dom_c, 3), subdominant_commit_competition=round(sub_c, 3),
                         subdominant_commit_alone=round(sub_alone, 3),
                         competitive_suppression=round(suppression, 3),
                         P_dominant_commits_first=round(dom_first, 3)))

    zero = rows[0]; top = rows[-1]
    # (1) competitive exclusion: at a substantial gap the subdominant clone (P≈1 alone) is strongly suppressed
    exclusion = bool(top["subdominant_commit_alone"] > 0.85 and
                     top["subdominant_commit_competition"] < 0.5 * top["subdominant_commit_alone"])
    # (2) dominant commits first + reaches commitment at the substantial gap
    direction = bool(top["P_dominant_commits_first"] > 0.80 and top["dominant_commit"] > 0.85)
    # (3a) monotone in gap: P(first) non-decreasing, subdominant commit non-increasing
    pf = [r["P_dominant_commits_first"] for r in rows]
    sc = [r["subdominant_commit_competition"] for r in rows]
    monotone = bool(all(pf[i + 1] >= pf[i] - 1e-9 for i in range(len(pf) - 1)) and
                    all(sc[i + 1] <= sc[i] + 1e-9 for i in range(len(sc) - 1)))
    # (3b) symmetric coin-flip at zero gap (no spurious hierarchy when affinities are equal)
    symmetric = bool(abs(zero["P_dominant_commits_first"] - 0.5) < 0.12 and
                     abs(zero["dominant_commit"] - zero["subdominant_commit_competition"]) < 0.12)

    ok = bool(exclusion and direction and monotone and symmetric)
    return dict(
        organ=_ORGAN, gamma=round(g, 6), spinodal=round(sp, 6),
        noise_D=_D, consume=_CONSUME, antigen_pool_A0=_A0,
        sweep=rows,
        competitive_exclusion_emerges=bool(exclusion),
        dominant_commits_first=bool(direction),
        monotone_in_affinity_gap=bool(monotone),
        symmetric_at_zero_gap=bool(symmetric),
        all_pass=ok,
        grade="[V] immunodominance EMERGES from a coupled stochastic shared-antigen competition: the "
              "subdominant clone (P≈1 alone) is competitively excluded, the higher-affinity clone commits "
              "first, dominance sharpens monotonically with the affinity gap, and the zero-gap contest is a "
              "symmetric coin-flip (measured, not asserted); [O] absolute hierarchy depth (consumption rate, "
              "pool size, cellular-noise scale D)")


def run(gammas):
    """T12: emergent immunodominance — clonal competition for a shared antigen pool MEASURED from a coupled stochastic model."""
    r = emergent_competition(gammas)
    return dict(T12=dict(target="T12",
                         claim="immunodominance EMERGES from a coupled stochastic competition for one shared "
                               "antigen pool: the higher-affinity clone commits first and depletes the pool, "
                               "competitively excluding a subdominant clone that would otherwise commit with "
                               "probability ≈ 1; dominance sharpens monotonically with the affinity gap and is "
                               "a symmetric coin-flip at zero gap — measured, not assumed; absolute hierarchy "
                               "depth stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T12"]["result"]
    print("immunodominance in the adaptive lymphoid compartment (γ=%.4f, spinodal=%.4f):"
          % (r["gamma"], r["spinodal"]))
    print("  gap   dom_commit  sub_commit(comp)  sub_commit(alone)  suppression  P(dom first)")
    for row in r["sweep"]:
        print("  %.2f      %.2f          %.2f              %.2f             %.2f          %.2f"
              % (row["affinity_gap"], row["dominant_commit"], row["subdominant_commit_competition"],
                 row["subdominant_commit_alone"], row["competitive_suppression"], row["P_dominant_commits_first"]))
    print("competitive exclusion emerges:", r["competitive_exclusion_emerges"])
    print("dominant commits first:       ", r["dominant_commits_first"])
    print("monotone in affinity gap:     ", r["monotone_in_affinity_gap"])
    print("symmetric at zero gap:        ", r["symmetric_at_zero_gap"])
    print("T12 all_pass:", r["all_pass"])
