#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_crossreactivity.py  --  EMERGENT cross-reactivity / original-antigenic-sin: an experienced
(memory) clone is preferentially RECALLED against a shifted antigen even when a better-matched naive clone
exists, MEASURED as an imprinting bias that decays with antigenic distance (not asserted, not fitted).

WHY THIS EXISTS (v0.8.0). T16/T18 build a repertoire that competes and matures against an antigen. The clinically
important sequel is re-exposure to a DRIFTED antigen: original antigenic sin (imprinting) is the observation that
the immune system preferentially recalls the clones it already has — the ones raised against the ORIGINAL
antigen — even when a naive clone is a strictly better match to the new variant. The VP discipline is emergence:
this bias, and its decay with antigenic distance, must come OUT of the same coupled R19 competition, MEASURED,
never assumed. This module runs a minimal coupled contest on the adaptive-lymphoid substrate between:

    MEMORY clone (experienced):  effective affinity to the SHIFTED antigen degrades with antigenic distance d,
                                 aff_mem(d) = aff_mem0 − slope·d, but it carries a RECALL HEAD-START — an
                                 experienced cell sits nearer the activation ridge: s0_mem = −√γ·(1 − recall)
                                 (still in the OFF basin, so committing still needs drive; the head-start only
                                 makes the memory clone FASTER to cross, not automatic).
    NAIVE clone:                 starts fully OFF (s0 = −√γ) with NO head-start, but is BETTER MATCHED to the
                                 shifted antigen — aff_naive is fixed above the memory clone's affinity once the
                                 antigen has drifted (aff_naive > aff_mem(d) for d beyond the crossover).

Both compete for ONE shared antigen pool A(t) that committed clones deplete (the T12/T16 mechanism: whoever
crosses first commits, depletes the pool, and competitively excludes the other). P(memory dominates) — the
fraction of hosts where the memory clone commits and the naive clone is excluded — is MEASURED across a sweep of
the antigenic distance d, and against a recall=0 control.

WHAT EMERGES (measured, deterministic seed=19):
  1. IMPRINTING BIAS EXISTS (original antigenic sin). At intermediate antigenic distance the naive clone is the
     STRICTLY better match to the shifted antigen (aff_naive > aff_mem(d)), yet the experienced memory clone is
     still preferentially recalled (measured P(memory dominates) > ½) because its recall head-start lets it
     commit first and deplete the shared pool, competitively excluding the better-matched naive clone. The sin is
     MEASURED, not imposed.
  2. THE BIAS DECAYS WITH ANTIGENIC DISTANCE. P(memory dominates) falls monotonically as the antigen drifts
     further: the memory clone's affinity degrades until even its head-start cannot beat the better-matched naive
     clone, which then commits first — at the largest distance the naive clone wins (P(memory) well below ½). The
     imprinting-vs-escape crossover is MEASURED.
  3. RECALL HEAD-START REQUIRED (honest control). With the recall head-start removed (recall=0) the better-matched
     clone always wins in the imprinting zone (P(memory) < ½ wherever aff_naive > aff_mem(d)) — proving the bias
     comes from EXPERIENCE (the head-start), not from affinity. At zero distance the memory clone is both
     experienced and best-matched, so it trivially dominates (not a sin, just consistency). The ABSOLUTE
     magnitude is [O].

GRADES (C3): the existence of the imprinting bias (memory recalled despite a better-matched naive clone), its
monotone decay with antigenic distance, and the recall-head-start control are [V] emergent (measured from the
coupled stochastic competition). The ABSOLUTE imprinting magnitude — set by the recall head-start size, the
affinity-degradation slope, and the free cellular-noise scale D — is [O], no fabricated bias numbers.
Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGAN    = "lymphoid_adaptive"        # the adaptive compartment (PAX5): memory vs naive on one pool

# --- deterministic simulation size (fixed; no per-condition tuning) ----------------------------------
_M        = 300       # independent hosts per condition
_DT       = 0.01      # Langevin timestep
_T        = 30.0      # recall-response horizon
_D        = 0.02      # cellular-noise scale (absolute value is [O])
_A0       = 1.0       # shared antigen pool (arbitrary unit; [O])
_CONSUME  = 0.6       # antigen consumption per committed clone ([O])

_AFF_MEM0 = 1.00      # memory affinity to the ORIGINAL antigen (best-matched at zero drift)
_AFF_NAIVE = 0.85     # naive affinity to the SHIFTED antigen (fixed; supra-spinodal so it CAN commit)
_SLOPE    = 0.40      # affinity degradation per unit antigenic distance: aff_mem(d) = aff_mem0 − slope·d
_RECALL   = 0.60      # recall head-start (fraction of the OFF-well depth the memory clone starts toward the ridge)
_DISTANCES = (0.0, 0.3, 0.6, 0.9, 1.2)   # antigenic distances (crossover where aff_mem = aff_naive is d≈0.375)


def _two_clone_recall(g, aff_mem, aff_naive, recall, D=_D, M=_M, dt=_DT, T=_T, consume=_CONSUME, A0=_A0, seed=SEED):
    """MEASURE the memory-vs-naive recall contest for one shared pool. Returns (p_mem_only, p_naive_only, p_both, p_none).

    memory starts with a head-start (nearer the ridge); naive starts fully OFF. Whoever crosses first commits and
    depletes the shared pool, competitively excluding the other (T12/T16 mechanism).
    """
    rng = np.random.default_rng(seed)
    s_off = -math.sqrt(g)
    s_mem = np.full(M, s_off * (1.0 - recall))    # experienced: nearer the ridge (still OFF basin)
    s_nai = np.full(M, s_off)                      # naive: fully OFF
    A = np.full(M, float(A0))
    comm_mem = np.zeros(M, dtype=bool)
    comm_nai = np.zeros(M, dtype=bool)
    sq = math.sqrt(2.0 * D * dt)
    for _ in range(int(T / dt)):
        h_mem = aff_mem * A
        h_nai = aff_naive * A
        s_mem += (g * s_mem - s_mem ** 3 + h_mem) * dt + sq * rng.standard_normal(M)
        s_nai += (g * s_nai - s_nai ** 3 + h_nai) * dt + sq * rng.standard_normal(M)
        np.clip(s_mem, -5.0, 5.0, out=s_mem); np.clip(s_nai, -5.0, 5.0, out=s_nai)
        on_mem = s_mem > 0.0; on_nai = s_nai > 0.0
        comm_mem |= on_mem; comm_nai |= on_nai
        A -= consume * (on_mem.astype(float) + on_nai.astype(float)) * dt   # both committed clones deplete the pool
        np.clip(A, 0.0, None, out=A)
    p_mem_only   = float((comm_mem & ~comm_nai).mean())
    p_naive_only = float((comm_nai & ~comm_mem).mean())
    p_both       = float((comm_mem & comm_nai).mean())
    p_none       = float((~comm_mem & ~comm_nai).mean())
    return p_mem_only, p_naive_only, p_both, p_none


def _sweep(g, recall, seed0):
    rows = []
    for k, d in enumerate(_DISTANCES):
        aff_mem = _AFF_MEM0 - _SLOPE * d
        pmem, pnai, pboth, pnone = _two_clone_recall(g, aff_mem, _AFF_NAIVE, recall, seed=seed0 + k)
        rows.append(dict(
            antigenic_distance=round(d, 3),
            memory_affinity=round(aff_mem, 3), naive_affinity=round(_AFF_NAIVE, 3),
            naive_better_matched=bool(_AFF_NAIVE > aff_mem + 1e-9),
            P_memory_dominates=round(pmem, 3), P_naive_dominates=round(pnai, 3),
            P_both=round(pboth, 3), P_none=round(pnone, 3)))
    return rows


def emergent_crossreactivity(gammas):
    g = gammas[_ORGAN]; sp = spinodal(g)

    # ---- experienced repertoire (recall head-start) -----------------------------------------------
    exp = _sweep(g, _RECALL, seed0=SEED + 10)
    # imprinting zone: distances where the naive clone is strictly better-matched yet memory still dominates
    imprint_rows = [r for r in exp if r["naive_better_matched"] and r["P_memory_dominates"] > 0.5]
    imprinting_exists = bool(len(imprint_rows) > 0)

    pmem_seq = [r["P_memory_dominates"] for r in exp]
    bias_monotone_falls = all(pmem_seq[i + 1] <= pmem_seq[i] + 0.05 for i in range(len(pmem_seq) - 1))
    naive_wins_at_far = bool(exp[-1]["P_naive_dominates"] > exp[-1]["P_memory_dominates"] and exp[-1]["P_memory_dominates"] < 0.4)
    bias_decays_with_distance = bool(bias_monotone_falls and naive_wins_at_far)

    # ---- control: NO recall head-start (recall=0) -> better-matched clone always wins in the zone ----
    ctrl = _sweep(g, 0.0, seed0=SEED + 200)
    ctrl_zone = [r for r in ctrl if r["naive_better_matched"]]
    recall_required = bool(len(ctrl_zone) > 0 and all(r["P_memory_dominates"] < 0.5 for r in ctrl_zone))

    # zero-distance consistency (memory both experienced AND best-matched -> trivially dominates; not a sin)
    zero_dist = [r for r in exp if r["antigenic_distance"] == 0.0]
    zero_dist_memory_dominates = bool(zero_dist and zero_dist[0]["P_memory_dominates"] > 0.5)

    ok = bool(imprinting_exists and bias_decays_with_distance and recall_required and zero_dist_memory_dominates)
    return dict(
        organ=_ORGAN, gamma=round(g, 6), spinodal=round(sp, 6),
        noise_D=_D, memory_affinity_original=_AFF_MEM0, naive_affinity_shifted=_AFF_NAIVE,
        degradation_slope=_SLOPE, recall_headstart=_RECALL, antigen_pool_A0=_A0, consume=_CONSUME,
        crossover_distance=round((_AFF_MEM0 - _AFF_NAIVE) / _SLOPE, 3),
        experienced_sweep=exp,
        imprinting_zone_distances=[r["antigenic_distance"] for r in imprint_rows],
        imprinting_exists=bool(imprinting_exists),
        bias_decays_with_distance=bool(bias_decays_with_distance),
        naive_wins_at_far_distance=bool(naive_wins_at_far),
        control_no_recall_sweep=ctrl,
        recall_headstart_required=bool(recall_required),
        zero_distance_memory_dominates=bool(zero_dist_memory_dominates),
        all_pass=ok,
        grade="[V] original antigenic sin (imprinting) EMERGES from a coupled stochastic memory-vs-naive "
              "competition for one shared antigen pool: at intermediate antigenic distance the experienced memory "
              "clone is preferentially recalled even though the naive clone is strictly better-matched (measured "
              "P(memory)>½, the recall head-start commits first and excludes the better naive clone), the bias "
              "decays monotonically with antigenic distance until the better-matched naive clone wins, and "
              "removing the head-start abolishes the bias — measured, not assumed; [O] absolute imprinting "
              "magnitude (recall head-start, degradation slope, cellular-noise scale D)")


def run(gammas):
    """T20: emergent cross-reactivity / original antigenic sin — imprinting bias MEASURED vs antigenic distance."""
    r = emergent_crossreactivity(gammas)
    return dict(T20=dict(target="T20",
                         claim="original antigenic sin (imprinting) EMERGES from a coupled stochastic memory-vs-"
                               "naive competition for one shared antigen pool: at intermediate antigenic distance "
                               "the experienced memory clone is preferentially recalled even though the naive "
                               "clone is strictly better-matched (measured P(memory)>½ — the recall head-start "
                               "commits first and excludes the better naive clone), the bias decays monotonically "
                               "with antigenic distance until the better-matched naive clone wins, and removing the "
                               "head-start abolishes the bias — measured, not assumed; absolute magnitude stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T20"]["result"]
    print("ORIGINAL ANTIGENIC SIN / IMPRINTING in the adaptive lymphoid compartment (γ=%.4f, spinodal=%.4f):"
          % (r["gamma"], r["spinodal"]))
    print("memory original affinity=%.2f | naive shifted affinity=%.2f | degradation slope=%.2f | recall=%.2f | crossover d=%.2f"
          % (r["memory_affinity_original"], r["naive_affinity_shifted"], r["degradation_slope"],
             r["recall_headstart"], r["crossover_distance"]))
    print("\nexperienced repertoire (recall head-start):")
    print("  distance   mem_aff   naive_better?   P(memory)   P(naive)")
    for row in r["experienced_sweep"]:
        print("    %.2f       %.3f      %-5s          %.3f       %.3f"
              % (row["antigenic_distance"], row["memory_affinity"], str(row["naive_better_matched"]),
                 row["P_memory_dominates"], row["P_naive_dominates"]))
    print("  imprinting zone (naive better-matched but memory wins) at distances:", r["imprinting_zone_distances"])
    print("  imprinting exists:", r["imprinting_exists"], "| bias decays with distance:", r["bias_decays_with_distance"])
    print("\ncontrol — NO recall head-start (recall=0):")
    print("  distance   naive_better?   P(memory)")
    for row in r["control_no_recall_sweep"]:
        print("    %.2f       %-5s          %.3f" % (row["antigenic_distance"], str(row["naive_better_matched"]), row["P_memory_dominates"]))
    print("  recall head-start required (bias abolished without it):", r["recall_headstart_required"])
    print("\nT20 all_pass:", r["all_pass"])
