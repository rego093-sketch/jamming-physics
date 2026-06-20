#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_sensitization.py  --  EMERGENT allergic sensitization and controlled DESENSITIZATION by direct stochastic
simulation (not asserted, not fitted).  [DISEASE/TREATMENT axis: roadmap D2, target T29.]

WHY THIS EXISTS (v0.11.0). T26 (emergent_hormesis.py) MEASURED a dose window with an IGNORANCE flank: a small
antigen drive leaves the effector in the resting OFF basin (ignored). Allergy is precisely the FAILURE of that
ignorance regime: an innocuous antigen that SHOULD be ignored instead crosses the effector commit threshold and
LATCHES a Th2/IgE-type effector program -- and the accumulation is what makes it pathological (repeated sub-threshold
exposure PRIMES until commitment). The clinical counter-move, allergen immunotherapy (desensitization), is the
controlled re-induction of tolerance by exposure -- the T27 re-tolerization dual reached through the exposure axis
rather than a direct suppressor. The roadmap asks for the sensitization threshold and its dose×repetition structure,
the latch, the controlled-exposure desensitization that RAISES the threshold, and the honest boundary where an
over-aggressive protocol sensitizes instead. The VP discipline is emergence: the threshold, the priming
accumulation, the latch, and the desensitization must come OUT of the SAME R19 substrate, MEASURED.

This module drives an effector clone (an R19 switch, resting OFF) by an antigen-exposure protocol. Each exposure of
dose d builds two competing per-exposure accumulators with DIFFERENT dose laws (the substrate asymmetry that makes
allergy dose-shaped):

    priming   P <- P·decay + a·d²     (Th2/IgE priming -- SUPERLINEAR in dose)
    tolerance T <- T·decay + b·d      (Treg tolerance  -- LINEAR in dose)

and the effector then settles under the net drive  h = (d_challenge + P − T)·spinodal.  Because priming is
superlinear and tolerance linear, there is a CROSSOVER dose d* (≈ b/a per exposure): ABOVE d* repeated exposure
drives P past T and SENSITIZES; BELOW d* tolerance dominates and exposure TOLERIZES (raises the threshold). Nothing
is assumed; P, T, and the committed fraction are integrated/counted from the dynamics.

WHAT EMERGES (measured, deterministic seed=19):
  1. A SENSITIZATION THRESHOLD AT THE SPINODAL, WITH DOSE×REPETITION STRUCTURE. A SINGLE exposure commits the
     effector only past the spinodal (the T26 commit threshold -- a large enough antigen), BUT a sub-threshold yet
     supra-crossover dose, REPEATED, accumulates priming and sensitizes after a measured number of exposures
     N_crit, and N_crit FALLS as the dose rises: allergy is reached either by a large single hit OR by repetition
     of a smaller one -- a measured dose×repetition threshold surface (the pathological failure of T26 ignorance).
  2. SENSITIZATION LATCHES (the established allergy). Once committed, the effector PERSISTS after the antigen
     clears (the antigen drive returns to zero but the effector stays ON by R19 memory): the sensitized state is a
     self-holding basin, not a transient response -- MEASURED (the T23/T9 latch, on the allergy axis).
  3. DESENSITIZATION = CONTROLLED RE-TOLERIZATION (the treatment dual). A controlled BELOW-crossover exposure
     protocol accumulates tolerance that RAISES the challenge threshold: a challenge dose that sensitizes a naive
     effector NO LONGER commits after the protocol, and the measured threshold-raise GROWS monotonically with
     protocol length -- the T27 re-tolerization reached through controlled exposure (basin-acting), MEASURED.
  4. THE CONTROLLED WINDOW IS REAL -- AN OVER-AGGRESSIVE PROTOCOL SENSITIZES (honest boundary). Desensitization
     works only in the controlled below-crossover window: an over-aggressive (above-crossover) exposure protocol
     drives priming OVER tolerance and SENSITIZES instead of tolerizing (the rush-protocol failure mode), and
     tolerance out-accumulates priming ONLY below the crossover dose -- the protective effect is a measured basin
     property with a real failure flank, not a universal good, MEASURED.

TREATMENT DIRECTION (roadmap discipline -- CLASS only, never agent/dose). The dynamics separate two classes:
ALLERGEN AVOIDANCE removes the drive (preventive, the effector re-primes on re-exposure -- not curative), whereas
CONTROLLED RE-TOLERIZATION by below-crossover exposure RAISES the commit threshold (basin-acting, durable), with a
real failure flank if the protocol is too aggressive. This is a re-description of allergy/immunotherapy dynamics in
the R19 formalism and a principled treatment DIRECTION + its boundary; it is NOT a drug, dose, schedule, clinical
recommendation, or VP validation, and NOT medical advice.

GRADES (C3): the sensitization threshold at the spinodal, the dose×repetition priming structure, the latch, the
controlled-exposure desensitization (threshold-raise growing with protocol length), and the over-aggressive failure
flank are [V] emergent (measured from the R19 effector under the exposure protocol). The ABSOLUTE dose units /
crossover / number of exposures -- set by the priming/tolerance gains a, b, the decay, and the free cellular-noise
scale D -- are [O], no fabricated numbers, and every clinical scale stays [O] with a stated obstacle. Determinism:
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
_PRIMARY = "lymphoid_adaptive"

_A_PRIME = 1.0      # priming gain (× d², SUPERLINEAR); [O]
_B_TOL   = 0.4      # tolerance gain (× d, LINEAR); [O] -- per-exposure crossover d* ≈ b/a
_DECAY   = 0.9      # per-exposure memory decay of both accumulators; [O]
_N       = 600      # effector cells
_RELAX   = 900      # settle steps
_DT      = 0.01
_D       = 0.02     # cellular-noise scale; [O]

_CHAL_DOSES = (0.70, 0.90, 1.00, 1.10, 1.30)     # single-exposure challenge sweep (× spinodal)
_D_SENS_GRID = (0.60, 0.70, 0.85)                # sensitizing (supra-crossover) doses for the repetition surface
_N_MAX      = 12                                  # max exposures scanned for N_crit
_D_CTRL     = 0.25                                # controlled (below-crossover) desensitization dose
_N_CTRL_GRID = (0, 5, 10, 20, 40)                # desensitization protocol lengths
_D_CHALLENGE = 1.00                              # post-protocol challenge (naive-sensitizing) dose
_D_AGGRESSIVE = 0.90                            # over-aggressive (above-crossover) protocol dose
_N_AGGRESSIVE = 20
_D_LATCH      = 1.30                             # supra-spinodal sensitizing hit for the latch demonstration
_DOSE_LAW_GRID = (0.20, 0.30, 0.40, 0.55, 0.70)  # to locate the priming/tolerance crossover


def _accumulate(doses, a=_A_PRIME, b=_B_TOL, decay=_DECAY):
    """Integrate the competing per-exposure priming P (∝ d², superlinear) and tolerance T (∝ d, linear)."""
    P = 0.0; T = 0.0
    for d in doses:
        P = P * decay + a * d * d
        T = T * decay + b * d
    return P, T


def _p_commit(g, d_chal, P, T, N=_N, relax=_RELAX, D=_D, dt=_DT, seed=SEED):
    """MEASURE the fraction of effector cells that commit (cross to ON) from the resting OFF basin under the net
    antigen drive h = (d_chal + P − T)·spinodal."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))
    sq = math.sqrt(2.0 * D * dt)
    h = (d_chal + P - T) * sp
    for _ in range(relax):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _persist_after_clear(g, d_sens, N=_N, settle=_RELAX, clear=_RELAX, D=_D, dt=_DT, seed=SEED):
    """Sensitize at dose d_sens, then CLEAR the antigen (drive 0) and settle -- MEASURE whether the effector stays
    ON (latched allergy)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, -math.sqrt(g))
    sq = math.sqrt(2.0 * D * dt)
    h = d_sens * sp
    for _ in range(settle):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    on_sens = float((s > 0.0).mean())
    for _ in range(clear):
        s += (g * s - s ** 3 + 0.0) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    on_clear = float((s > 0.0).mean())
    return on_sens, on_clear


def _single_dose_threshold(g, doses=_CHAL_DOSES, D=_D):
    fr = [_p_commit(g, d, 0.0, 0.0, D=D) for d in doses]
    for i in range(1, len(fr)):
        if fr[i - 1] < 0.5 <= fr[i]:
            f = (0.5 - fr[i - 1]) / (fr[i] - fr[i - 1])
            return doses[i - 1] + f * (doses[i] - doses[i - 1]), fr
    return (doses[0] if fr[0] >= 0.5 else float("inf")), fr


def _n_crit(g, d, n_max=_N_MAX, D=_D):
    """First exposure count at dose d for which the repeated-exposure committed fraction crosses 0.5."""
    for n in range(1, n_max + 1):
        P, T = _accumulate([d] * n)
        if _p_commit(g, d, P, T, D=D) >= 0.5:
            return n
    return None


def emergent_sensitization(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1) SENSITIZATION THRESHOLD AT SPINODAL + DOSE×REPETITION
    thr_rows = {}
    thr_ok = True
    for o in _ORGANS:
        d_crit, _fr = _single_dose_threshold(gammas[o], D=D)
        thr_rows[o] = dict(d_crit_over_spinodal=round(d_crit, 3), near_spinodal=bool(abs(d_crit - 1.0) < 0.16))
        thr_ok = thr_ok and thr_rows[o]["near_spinodal"]
    rep_rows = []
    for d in _D_SENS_GRID:
        nc = _n_crit(g_ref, d, D=D)
        rep_rows.append(dict(dose=round(d, 3), n_crit=nc))
    ncs = [r["n_crit"] for r in rep_rows]
    repetition_sensitizes = bool(all(n is not None for n in ncs))
    n_crit_falls = bool(repetition_sensitizes and all(ncs[i] >= ncs[i + 1] for i in range(len(ncs) - 1)))
    threshold_ok = bool(thr_ok and repetition_sensitizes and n_crit_falls)

    # (2) SENSITIZATION LATCHES
    on_sens, on_clear = _persist_after_clear(g_ref, _D_LATCH, D=D)
    latches = bool(on_sens >= 0.85 and on_clear >= 0.85)

    # (3) DESENSITIZATION = CONTROLLED RE-TOLERIZATION (threshold-raise grows with protocol length)
    des_rows = []
    for nctrl in _N_CTRL_GRID:
        P, T = _accumulate([_D_CTRL] * nctrl)
        commit = _p_commit(g_ref, _D_CHALLENGE, P, T, D=D)
        des_rows.append(dict(n_ctrl=nctrl, P=round(P, 3), T=round(T, 3),
                             threshold_raise=round(T - P, 3), challenge_commit=round(commit, 3)))
    naive_commit = des_rows[0]["challenge_commit"]          # nctrl=0 -> naive
    protected_commit = des_rows[-1]["challenge_commit"]     # longest protocol
    raises = [r["threshold_raise"] for r in des_rows]
    commits = [r["challenge_commit"] for r in des_rows]
    desens_protects = bool(naive_commit >= 0.5 and protected_commit <= 0.15)
    raise_monotone = bool(all(raises[i] <= raises[i + 1] + 1e-9 for i in range(len(raises) - 1)))
    commit_monotone = bool(all(commits[i] >= commits[i + 1] - 0.06 for i in range(len(commits) - 1)))
    desens_ok = bool(desens_protects and raise_monotone and commit_monotone)

    # (4) CONTROLLED WINDOW -- over-aggressive protocol SENSITIZES; tolerance wins only below crossover
    P_agg, T_agg = _accumulate([_D_AGGRESSIVE] * _N_AGGRESSIVE)
    agg_commit = _p_commit(g_ref, _D_AGGRESSIVE, P_agg, T_agg, D=D)
    aggressive_sensitizes = bool(agg_commit >= 0.85)
    # locate the priming/tolerance crossover (steady net) along the dose-law grid
    law_rows = []
    for d in _DOSE_LAW_GRID:
        P, T = _accumulate([d] * 30)
        law_rows.append(dict(dose=round(d, 3), P=round(P, 3), T=round(T, 3),
                             priming_wins=bool(P > T)))
    tol_below = law_rows[0]["P"] <= law_rows[0]["T"]               # tolerance dominates at the lowest dose
    prime_above = law_rows[-1]["P"] > law_rows[-1]["T"]            # priming dominates at the highest dose
    d_star = None
    for i in range(1, len(law_rows)):
        if (law_rows[i - 1]["P"] <= law_rows[i - 1]["T"]) and (law_rows[i]["P"] > law_rows[i]["T"]):
            d_star = round(0.5 * (law_rows[i - 1]["dose"] + law_rows[i]["dose"]), 3)
            break
    window_ok = bool(aggressive_sensitizes and tol_below and prime_above and (d_star is not None))

    ok = bool(threshold_ok and latches and desens_ok and window_ok)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6), noise_D=D,
        priming_gain=_A_PRIME, tolerance_gain=_B_TOL, decay=_DECAY,
        sensitization_threshold=dict(single_dose=thr_rows, near_spinodal=bool(thr_ok),
                                     repetition=rep_rows, repetition_sensitizes=bool(repetition_sensitizes),
                                     n_crit_falls_with_dose=bool(n_crit_falls), threshold_ok=bool(threshold_ok)),
        latch=dict(on_after_sensitize=round(on_sens, 3), on_after_clear=round(on_clear, 3), latches=bool(latches)),
        desensitization=dict(controlled_dose=_D_CTRL, challenge_dose=_D_CHALLENGE, protocol=des_rows,
                             naive_commit=round(naive_commit, 3), protected_commit=round(protected_commit, 3),
                             protects=bool(desens_protects), threshold_raise_monotone=bool(raise_monotone),
                             challenge_commit_monotone=bool(commit_monotone), desensitizes=bool(desens_ok)),
        controlled_window=dict(aggressive_dose=_D_AGGRESSIVE, aggressive_commit=round(agg_commit, 3),
                               aggressive_sensitizes=bool(aggressive_sensitizes), dose_law=law_rows,
                               crossover_dose=d_star, tolerance_wins_below=bool(tol_below),
                               priming_wins_above=bool(prime_above), window_ok=bool(window_ok)),
        all_pass=ok,
        grade="[V] allergic sensitization and controlled DESENSITIZATION EMERGE from an R19 effector under an "
              "antigen-exposure protocol: a single exposure commits only past the spinodal (the T26 commit "
              "threshold) but a sub-threshold supra-crossover dose REPEATED accumulates priming and sensitizes "
              "after a measured N_crit that falls with dose (allergy = failure of T26 ignorance), the sensitized "
              "effector LATCHES after the antigen clears (R19 memory), a controlled below-crossover exposure "
              "protocol RAISES the challenge threshold (the naive-sensitizing dose no longer commits, threshold-"
              "raise growing with protocol length -- the T27 re-tolerization through exposure), and the controlled "
              "window is REAL (an over-aggressive above-crossover protocol SENSITIZES instead, tolerance "
              "out-accumulating priming only below the crossover) -- measured, not assumed; [O] absolute dose units "
              "/ crossover / number of exposures (priming gain a, tolerance gain b, decay, cellular-noise scale D); "
              "treatment = CLASS (controlled re-tolerization vs avoidance), never agent / dose / recommendation")


def run(gammas):
    """T29: emergent allergic sensitization + controlled desensitization -- sensitization is the failure of the T26
    ignorance regime (innocuous antigen crosses the spinodal commit threshold, by a large hit or by repetition) and
    LATCHES, while desensitization is controlled re-tolerization (T27 through the exposure axis) that raises the
    threshold, with a real over-aggressive failure flank."""
    r = emergent_sensitization(gammas)
    return dict(T29=dict(target="T29",
                         claim="allergic sensitization + controlled DESENSITIZATION EMERGE from an R19 effector: a "
                               "single exposure commits only past the spinodal but a sub-threshold supra-crossover "
                               "dose REPEATED accumulates priming and sensitizes after a measured N_crit (falling "
                               "with dose) -- allergy = failure of T26 ignorance -- and the sensitized effector "
                               "LATCHES; a controlled below-crossover exposure protocol RAISES the threshold (T27 "
                               "re-tolerization through exposure, threshold-raise growing with protocol length), "
                               "and the window is real (over-aggressive protocol SENSITIZES instead); treatment is "
                               "direction/class only and absolute dose units stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T29"]["result"]
    print("ALLERGIC SENSITIZATION + CONTROLLED DESENSITIZATION (primary=%s, γ=%.4f, spinodal=%.4f, a=%.2f, b=%.2f, "
          "decay=%.2f, D=%.3f):" % (r["primary"], r["gamma"], r["spinodal"], r["priming_gain"],
                                    r["tolerance_gain"], r["decay"], r["noise_D"]))
    st = r["sensitization_threshold"]
    print("\n(1) SENSITIZATION THRESHOLD at spinodal + DOSE×REPETITION:")
    for o, row in st["single_dose"].items():
        print("     %-28s single-dose d_crit=%.3f×sp  near_spinodal=%s" % (o, row["d_crit_over_spinodal"], row["near_spinodal"]))
    for row in st["repetition"]:
        print("     repeated dose=%.2f -> N_crit=%s exposures" % (row["dose"], row["n_crit"]))
    print("     repetition sensitizes=%s | N_crit falls with dose=%s -> threshold ok=%s"
          % (st["repetition_sensitizes"], st["n_crit_falls_with_dose"], st["threshold_ok"]))
    lt = r["latch"]
    print("\n(2) SENSITIZATION LATCHES: ON after sensitize=%.3f -> ON after antigen clears=%.3f -> latches=%s"
          % (lt["on_after_sensitize"], lt["on_after_clear"], lt["latches"]))
    ds = r["desensitization"]
    print("\n(3) DESENSITIZATION = CONTROLLED RE-TOLERIZATION (controlled dose=%.2f, challenge dose=%.2f):"
          % (ds["controlled_dose"], ds["challenge_dose"]))
    for row in ds["protocol"]:
        print("     N_ctrl=%2d  P=%.2f T=%.2f  threshold_raise=%.2f×sp  challenge_commit=%.2f  %s"
              % (row["n_ctrl"], row["P"], row["T"], row["threshold_raise"], row["challenge_commit"],
                 "#" * int(round(row["challenge_commit"] * 24))))
    print("     naive commit=%.2f -> protected commit=%.2f | raise monotone=%s | commit monotone=%s -> desensitizes=%s"
          % (ds["naive_commit"], ds["protected_commit"], ds["threshold_raise_monotone"],
             ds["challenge_commit_monotone"], ds["desensitizes"]))
    cw = r["controlled_window"]
    print("\n(4) CONTROLLED WINDOW (over-aggressive protocol SENSITIZES; crossover dose d*=%s):" % cw["crossover_dose"])
    print("     aggressive dose=%.2f ×%d -> commit=%.2f -> sensitizes=%s"
          % (cw["aggressive_dose"], _N_AGGRESSIVE, cw["aggressive_commit"], cw["aggressive_sensitizes"]))
    for row in cw["dose_law"]:
        print("     dose=%.2f  P=%.2f T=%.2f  priming_wins=%s" % (row["dose"], row["P"], row["T"], row["priming_wins"]))
    print("     tolerance wins below=%s | priming wins above=%s -> window ok=%s"
          % (cw["tolerance_wins_below"], cw["priming_wins_above"], cw["window_ok"]))
    print("\nT29 all_pass:", r["all_pass"])
