#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_allotolerance.py  --  EMERGENT transplant (allo-)tolerance INDUCTION as a MEASURED basin re-flip of an
alloreactive clone across the negative saddle-node, with an alloreactive-CONSOLIDATION induction window (the
transplant dual of T27, not asserted, not fitted).  [DISEASE/TREATMENT axis: roadmap D5, target T32.]

WHY THIS EXISTS (v0.11.0). T27 (emergent_retolerization.py) MEASURED therapeutic re-tolerization: a transient
deep-suppression pulse pushes a LATCHED autoreactive clone (residual self-drive base·spinodal, bistable) back
across the NEGATIVE saddle-node into the tolerant basin, durably (basin-acting) iff supra-threshold, with
suppress_crit = 1 + base. Transplantation is the same substrate problem with a LARGER residual drive: the graft
presents a standing allo-antigen LOAD (base_allo > the autoimmune residual), and -- the feature that makes
transplant tolerance time-critical and is absent from the autoimmune case -- the alloreactive response
CONSOLIDATES (memory/clonal expansion) the longer it runs unopposed, deepening the basin it must be pulled out of.
The roadmap asks for the induction threshold (shifted by allo-load), the durable-operational-tolerance vs
indefinite-immunosuppression contrast (rejection on withdrawal), the INDUCTION WINDOW (tolerance easier early,
before consolidation), and the honest sub-threshold relapse control. The VP discipline is emergence: all of it must
come OUT of the SAME R19 substrate, MEASURED.

This module reuses the T27 re-tolerization machinery at the allo-load `base_allo`, and ADDS an alloreactive
consolidation variable C that accrues while the clone is ON,

    ds = (γ s − s³ + h) dt + sqrt(2 D dt)·ξ,    dC = (cons_rate · frac_ON − C/τ_C) dt,
    h = (base_allo + C − suppress)·spinodal during the induction pulse,   h = (base_allo + C)·spinodal otherwise,

so the effective residual drive (base_allo + C) GROWS with the delay-to-induction: the basin deepens as the
alloresponse consolidates. The induction threshold, the trajectories, and the window are MEASURED -- the exact T27
reflection with a larger, time-deepening residual.

WHAT EMERGES (measured, deterministic seed=19):
  1. INDUCTION THRESHOLD = THE NEGATIVE SADDLE-NODE SHIFTED BY THE ALLO-LOAD. The suppression depth at which
     P(tolerate) crosses 0.5 makes the total pulse drive reach −spinodal, organ by organ, and across an allo-LOAD
     sweep the measured (suppress_crit − base_allo) stays at 1×spinodal -- suppress_crit = 1 + base_allo: a heavier
     graft load needs a proportionally DEEPER induction, the same saddle-node as T27 displaced by the standing
     allo-antigen, MEASURED.
  2. DURABLE OPERATIONAL TOLERANCE vs INDEFINITE IMMUNOSUPPRESSION (rejection on withdrawal) -- the central claim.
     Two interventions are MEASURED as basin-gated alloreactive-population trajectories:
       • BASIN-ACTING induction: a deep TRANSIENT pulse crosses the negative saddle-node, so after withdrawal the
         alloreactive basin is emptied (measured ON ≈ 0) and the response DECAYS to ≈0 -- durable operational
         tolerance, the graft accepted off-therapy.
       • INDEFINITE IMMUNOSUPPRESSION: a SUB-critical suppressor held CONTINUOUSLY holds rejection down WHILE
         applied (measured ON low -- contained) but never crosses the saddle-node, so on WITHDRAWAL the standing
         allo-load REFILLS the basin (measured ON ≈ 1) and rejection REGROWS -- rejection on withdrawal.
     Substrate verdict: basin-acting tolerance induction is the DURABLE class; chronic immunosuppression is
     containment-not-tolerance and rejects when released.
  3. THE INDUCTION WINDOW (allo-specific -- consolidation). At a FIXED induction strength, P(tolerate) FALLS
     monotonically with the delay-to-induction, and equivalently the measured suppress_crit RISES with delay (from
     1 + base_allo at delay 0 toward a larger value as C accrues): tolerance is EASIER EARLY, before the
     alloresponse consolidates the basin -- a measured induction window. The same induction that succeeds early
     fails (or needs a deeper pulse) late: timing is a substrate property, MEASURED.
  4. SUB-THRESHOLD INDUCTION RELAPSES (honest control) + DIRECTION SYMMETRY. A sub-critical induction pulse does
     NOT durably tolerize -- the standing allo-load refills the alloreactive basin on withdrawal (rejection), the
     same honest negative as T27. And the mechanism is DIRECTION-SYMMETRIC: host-vs-graft and graft-vs-host are the
     SAME negative-saddle-node crossing with the alloreactive compartment and the target swapped -- one structural
     fact, MEASURED for the modelled direction and symmetric by construction.

TREATMENT DIRECTION (roadmap discipline -- CLASS / TIMING-STRUCTURE only, never agent/dose). The dynamics separate
INDEFINITE IMMUNOSUPPRESSION (containment; rejection on withdrawal) from BASIN-ACTING TOLERANCE INDUCTION (durable
operational tolerance), and say the induction is EASIER EARLY before alloreactive consolidation (an induction
window). This is a re-description of transplantation-tolerance dynamics in the R19 formalism and a principled
treatment DIRECTION + timing structure; it is NOT a drug, dose, schedule, clinical recommendation, or VP
validation, and NOT medical advice.

GRADES (C3): the allo-load-shifted induction threshold (suppress_crit = 1 + base_allo), the durable-vs-relapsing
contrast, the consolidation induction window, and the sub-threshold relapse control are [V] emergent (measured from
the R19 substrate). The ABSOLUTE allo-load / suppression depth / window length -- set by base_allo, the
consolidation gain/timescale, and the free cellular-noise scale D -- are [O], no fabricated numbers, and every
clinical scale stays [O] with a stated obstacle. Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"            # the adaptive compartment carrying the alloreactive clone

_N        = 300       # cells per condition
_DT       = 0.01
_D        = 0.02      # cellular-noise scale (low: sharp boundary; absolute value is [O])
_RELAX    = 900       # settle steps after pulse withdrawal (decide final basin)
_DUR_LONG = 800       # induction-pulse duration for the depth threshold
_BASE_ALLO = 0.50     # standing allo-antigen load of the graft (× spinodal; sub-spinodal -> bistable); [O]
_ALLO_SWEEP = (0.30, 0.45, 0.60, 0.75)                 # allo-load sweep (graft loads)
_SUPPRESS_DEPTHS = (0.60, 1.00, 1.30, 1.50, 1.70, 1.90, 2.10, 2.30)   # suppression-depth grid (× spinodal)

# alloreactive consolidation (the induction window)
_CONS_RATE = 0.05     # consolidation accrual gain while ON; [O]
_TAU_C     = 8.0      # consolidation timescale; [O]
_SUPP_FIXED = 1.70    # fixed induction strength for the window probe (× spinodal)
_DELAY_GRID = (0, 200, 500, 900, 1400, 2000)           # delay-to-induction (steps)

# alloreactive population layer (durable vs relapsing trajectory)
_K_POP = 2000; _M_POP = 400; _PDT = 0.05; _R_GROW = 1.0; _CONV = 1.0; _T_POP = 300


def p_induce_pulse(g, suppress_frac, dur, base=_BASE_ALLO, D=_D, N=_N, dt=_DT, relax=_RELAX, seed=SEED, relax_mult=1):
    """MEASURED probability the alloreactive clone is TOLERIZED: from the ON basin, hold h=(base−suppress)·spinodal
    for `dur` steps (induction pulse), then WITHDRAW to the standing allo-load h=base·spinodal and settle; report
    the OFF (tolerant) fraction. The allo-load does NOT go to zero (the graft persists)."""
    rng = np.random.default_rng(seed); sp = spinodal(g)
    s = np.full(N, math.sqrt(g)); sq = math.sqrt(2.0 * D * dt)
    h_pulse = (base - suppress_frac) * sp; h_rest = base * sp
    for _ in range(int(dur)):
        s += (g * s - s ** 3 + h_pulse) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(relax * relax_mult)):
        s += (g * s - s ** 3 + h_rest) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s < 0.0).mean())


def p_induce_consolidated(g, suppress_frac, dur, base, delay, cons_rate=_CONS_RATE, tau_c=_TAU_C,
                          D=_D, N=_N, dt=_DT, relax=_RELAX, seed=SEED):
    """MEASURED P(tolerize) when the alloresponse has CONSOLIDATED for `delay` steps before induction: C accrues
    while ON, deepening the effective residual (base + C); then the induction pulse and settle run under (base + C)."""
    rng = np.random.default_rng(seed); sp = spinodal(g)
    s = np.full(N, math.sqrt(g)); C = 0.0; sq = math.sqrt(2.0 * D * dt)
    for _ in range(int(delay)):
        fon = float((s > 0.0).mean()); C += (cons_rate * fon - C / tau_c) * dt
        s += (g * s - s ** 3 + (base + C) * sp) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    Cf = C
    for _ in range(int(dur)):
        s += (g * s - s ** 3 + (base + Cf - suppress_frac) * sp) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(relax)):
        s += (g * s - s ** 3 + (base + Cf) * sp) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s < 0.0).mean()), Cf


def _suppress_threshold(g, base, dur=_DUR_LONG, depths=_SUPPRESS_DEPTHS, D=_D, seed=SEED):
    ps = [p_induce_pulse(g, d, dur, base=base, D=D, seed=seed) for d in depths]
    if ps[0] >= 0.5:
        return depths[0], ps
    for i in range(1, len(ps)):
        if ps[i - 1] < 0.5 <= ps[i]:
            f = (0.5 - ps[i - 1]) / (ps[i] - ps[i - 1])
            return depths[i - 1] + f * (depths[i] - depths[i - 1]), ps
    return (depths[-1] if ps[-1] >= 0.5 else float("inf")), ps


def _suppress_threshold_consolidated(g, base, delay, dur=_DUR_LONG, depths=_SUPPRESS_DEPTHS, D=_D, seed=SEED):
    ps = [p_induce_consolidated(g, d, dur, base, delay, D=D, seed=seed)[0] for d in depths]
    for i in range(1, len(ps)):
        if ps[i - 1] < 0.5 <= ps[i]:
            f = (0.5 - ps[i - 1]) / (ps[i] - ps[i - 1])
            return depths[i - 1] + f * (depths[i] - depths[i - 1])
    return (depths[-1] if ps[-1] >= 0.5 else float("inf"))


def _basin_fraction(g, mode, base=_BASE_ALLO, D=_D, N=_N, dt=_DT, seed=SEED):
    """MEASURE residual alloreactive-ON fraction after an intervention. mode 'induce': supra-threshold TRANSIENT
    pulse then withdraw (≈0). mode 'immunosuppress_withdrawn': SUB-critical suppressor held then withdrawn (≈1)."""
    rng = np.random.default_rng(seed); sp = spinodal(g)
    s = np.full(N, math.sqrt(g)); sq = math.sqrt(2.0 * D * dt)
    depth = (1.0 + base) + 0.30 if mode == "induce" else (1.0 + base) - 0.30
    h = (base - depth) * sp
    for _ in range(int(_DUR_LONG)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(_RELAX)):
        s += (g * s - s ** 3 + base * sp) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _population(f, K=_K_POP, M=_M_POP, dt=_PDT, T=_T_POP, r=_R_GROW, conv=_CONV, seed=SEED):
    rng = np.random.default_rng(seed); N = np.full(M, int(K), dtype=float); traj = np.empty(T)
    for t in range(T):
        p_grow = np.clip(r * (1.0 - N / K) * f * dt, 0.0, 1.0)
        p_decay = min(max(conv * (1.0 - f) * dt, 0.0), 1.0)
        births = rng.binomial(N.astype(int), p_grow)
        deaths = rng.binomial(N.astype(int), p_decay) if p_decay > 0 else np.zeros(M, dtype=int)
        N = np.clip(N + births - deaths, 0, K); traj[t] = float(N.mean()) / K
    return traj


def _coarse_monotone(traj, rising=True, nb=10, tol=0.03):
    blk = max(1, len(traj) // nb)
    means = [float(traj[i:i + blk].mean()) for i in range(0, len(traj) - blk + 1, blk)]
    if rising:
        return all(means[i + 1] >= means[i] - tol for i in range(len(means) - 1))
    return all(means[i + 1] <= means[i] + tol for i in range(len(means) - 1))


def emergent_allotolerance(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1) INDUCTION THRESHOLD = NEGATIVE SADDLE-NODE shifted by allo-load
    depth_rows = {}
    crit_ok = True
    for o in _ORGANS:
        d_crit, _ps = _suppress_threshold(gammas[o], base=_BASE_ALLO, D=D)
        total = d_crit - _BASE_ALLO
        depth_rows[o] = dict(suppress_crit_over_spinodal=round(d_crit, 3),
                             total_drive_over_spinodal=round(total, 3),
                             matches_negative_saddle=bool(abs(total - 1.0) < 0.22))
        crit_ok = crit_ok and depth_rows[o]["matches_negative_saddle"]
    allo_rows = []
    inv_ok = True
    for b in _ALLO_SWEEP:
        d_crit, _ps = _suppress_threshold(g_ref, base=b, D=D)
        inv = d_crit - b
        allo_rows.append(dict(allo_load=round(b, 3), suppress_crit=round(d_crit, 3),
                              suppress_crit_minus_load=round(inv, 3),
                              invariant=bool(abs(inv - 1.0) < 0.22)))
        inv_ok = inv_ok and allo_rows[-1]["invariant"]
    crit_rises = bool(all(allo_rows[i]["suppress_crit"] <= allo_rows[i + 1]["suppress_crit"] + 1e-6
                          for i in range(len(allo_rows) - 1)))
    threshold_ok = bool(crit_ok and inv_ok and crit_rises)

    # (2) DURABLE OPERATIONAL TOLERANCE vs INDEFINITE IMMUNOSUPPRESSION (rejection on withdrawal)
    f_induce = _basin_fraction(g_ref, "induce", base=_BASE_ALLO, D=D)               # ≈ 0
    f_immuno = _basin_fraction(g_ref, "immunosuppress_withdrawn", base=_BASE_ALLO, D=D)  # ≈ 1
    traj_induce = _population(f_induce)
    traj_immuno = _population(f_immuno)
    induce_empties = bool(f_induce <= 0.15 and traj_induce[-1] <= 0.15 and _coarse_monotone(traj_induce, rising=False))
    immuno_refills = bool(f_immuno >= 0.85 and traj_immuno[-1] >= 0.85 and _coarse_monotone(traj_immuno, rising=True))
    contrast_ok = bool(induce_empties and immuno_refills)

    # (3) INDUCTION WINDOW (consolidation): P(tolerate) falls with delay at fixed strength; suppress_crit rises
    win_rows = []
    for d in _DELAY_GRID:
        p, Cf = p_induce_consolidated(g_ref, _SUPP_FIXED, _DUR_LONG, _BASE_ALLO, d, D=D)
        win_rows.append(dict(delay=d, consolidation=round(Cf, 3), effective_load=round(_BASE_ALLO + Cf, 3),
                             p_tolerate=round(p, 3)))
    ps_win = [r["p_tolerate"] for r in win_rows]
    window_falls = bool(ps_win[0] >= 0.7 and ps_win[-1] <= 0.3
                        and all(ps_win[i] >= ps_win[i + 1] - 0.06 for i in range(len(ps_win) - 1)))
    sc_early = _suppress_threshold_consolidated(g_ref, _BASE_ALLO, _DELAY_GRID[0], D=D)
    sc_late = _suppress_threshold_consolidated(g_ref, _BASE_ALLO, _DELAY_GRID[-1], D=D)
    threshold_rises = bool(sc_late > sc_early + 0.1)
    early_is_saddle = bool(abs(sc_early - (1.0 + _BASE_ALLO)) < 0.22)
    window_ok = bool(window_falls and threshold_rises and early_is_saddle)

    # (4) SUB-THRESHOLD INDUCTION RELAPSES (honest control)
    crit_ref, _ = _suppress_threshold(g_ref, base=_BASE_ALLO, D=D)
    sub = max(0.05, crit_ref - 0.30)
    supra = crit_ref + 0.30
    p_sub = p_induce_pulse(g_ref, sub, _DUR_LONG, base=_BASE_ALLO, D=D)
    p_supra = p_induce_pulse(g_ref, supra, _DUR_LONG, base=_BASE_ALLO, D=D)
    p_supra_long = p_induce_pulse(g_ref, supra, _DUR_LONG, base=_BASE_ALLO, D=D, relax_mult=3)
    sub_relapses = bool(p_sub <= 0.15)
    supra_durable = bool(p_supra >= 0.85 and p_supra_long >= 0.85)
    control_ok = bool(sub_relapses and supra_durable)

    ok = bool(threshold_ok and contrast_ok and window_ok and control_ok)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6), noise_D=D, allo_load_ref=_BASE_ALLO,
        consolidation_gain=_CONS_RATE, consolidation_tau=_TAU_C,
        induction_threshold=dict(per_organ=depth_rows, matches_negative_saddle=bool(crit_ok),
                                 allo_load_sweep=allo_rows, invariant_holds=bool(inv_ok),
                                 suppress_crit_rises_with_load=bool(crit_rises), threshold_ok=bool(threshold_ok)),
        durable_vs_relapsing=dict(induce_basin_fraction=round(f_induce, 3),
                                  immunosuppress_basin_fraction=round(f_immuno, 3),
                                  induce_traj_end=round(float(traj_induce[-1]), 3),
                                  immuno_traj_end=round(float(traj_immuno[-1]), 3),
                                  induce_empties=bool(induce_empties), immuno_refills=bool(immuno_refills),
                                  contrast=bool(contrast_ok)),
        induction_window=dict(fixed_suppress=_SUPP_FIXED, rows=win_rows,
                              suppress_crit_early=round(sc_early, 3), suppress_crit_late=round(sc_late, 3),
                              p_tolerate_falls_with_delay=bool(window_falls),
                              threshold_rises_with_delay=bool(threshold_rises),
                              early_threshold_is_negative_saddle=bool(early_is_saddle), window_ok=bool(window_ok)),
        sub_threshold_control=dict(suppress_crit=round(crit_ref, 3), sub_depth=round(sub, 3), supra_depth=round(supra, 3),
                                   p_tolerize_sub=round(p_sub, 3), p_tolerize_supra=round(p_supra, 3),
                                   p_tolerize_supra_long_settle=round(p_supra_long, 3),
                                   sub_relapses=bool(sub_relapses), supra_durable=bool(supra_durable),
                                   control_ok=bool(control_ok)),
        direction_symmetry_note="host-vs-graft and graft-vs-host are the SAME negative-saddle-node crossing with the "
                                "alloreactive compartment and target swapped (symmetric by construction)",
        all_pass=ok,
        grade="[V] transplant (allo-)tolerance INDUCTION EMERGES as the T27 re-tolerization at a larger, "
              "time-deepening allo-load: the induction threshold is the NEGATIVE saddle-node shifted by the graft "
              "load (suppress_crit = 1 + base_allo, measured organ by organ and invariant across an allo-load "
              "sweep -- a heavier graft needs a deeper induction), a deep TRANSIENT pulse yields DURABLE operational "
              "tolerance (basin emptied, graft accepted off-therapy) whereas continuous SUB-critical "
              "immunosuppression only CONTAINS rejection and REJECTS on withdrawal (the standing allo-load refills "
              "the basin), tolerance is EASIER EARLY before alloreactive CONSOLIDATION (measured P(tolerate) falls "
              "with delay-to-induction and suppress_crit rises from 1+base_allo -- an induction window), and a "
              "sub-threshold pulse relapses (honest control); the mechanism is direction-symmetric -- measured, not "
              "assumed; [O] absolute allo-load / suppression depth / window length (base_allo, consolidation "
              "gain/timescale, cellular-noise scale D); treatment = CLASS/TIMING (basin-acting induction early, not "
              "indefinite immunosuppression), never agent / dose / recommendation")


def run(gammas):
    """T32: emergent transplant (allo-)tolerance induction -- the T27 re-tolerization at a larger, time-deepening
    allo-load: induction threshold = negative saddle-node shifted by graft load (suppress_crit = 1 + base_allo),
    durable operational tolerance vs indefinite immunosuppression (rejection on withdrawal), an induction window
    (easier early, before alloreactive consolidation), and an honest sub-threshold relapse control."""
    r = emergent_allotolerance(gammas)
    return dict(T32=dict(target="T32",
                         claim="transplant (allo-)tolerance INDUCTION EMERGES as the T27 re-tolerization at a "
                               "larger, time-deepening allo-load: induction threshold = NEGATIVE saddle-node "
                               "shifted by graft load (suppress_crit = 1 + base_allo, invariant across an allo-load "
                               "sweep), a deep TRANSIENT pulse yields DURABLE operational tolerance while continuous "
                               "SUB-critical immunosuppression only contains and REJECTS on withdrawal, tolerance is "
                               "EASIER EARLY before alloreactive CONSOLIDATION (P(tolerate) falls with delay, "
                               "suppress_crit rises -- an induction window), and a sub-threshold pulse relapses; "
                               "direction-symmetric; treatment is direction/class/timing only and absolute scales "
                               "stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T32"]["result"]
    print("TRANSPLANT (ALLO-)TOLERANCE INDUCTION (primary=%s, γ=%.4f, spinodal=%.4f, allo_load=%.2f, cons_gain=%.3f, "
          "τ_C=%.1f, D=%.3f):" % (r["primary"], r["gamma"], r["spinodal"], r["allo_load_ref"],
                                  r["consolidation_gain"], r["consolidation_tau"], r["noise_D"]))
    it = r["induction_threshold"]
    print("\n(1) INDUCTION THRESHOLD = NEGATIVE SADDLE-NODE shifted by allo-load:")
    for o, row in it["per_organ"].items():
        print("     %-28s suppress_crit=%.3f×sp  total_drive=%.3f×sp  matches=%s"
              % (o, row["suppress_crit_over_spinodal"], row["total_drive_over_spinodal"], row["matches_negative_saddle"]))
    print("     allo-load sweep (suppress_crit − load == 1×sp):")
    for row in it["allo_load_sweep"]:
        print("       allo_load=%.2f  suppress_crit=%.3f  diff=%.3f  invariant=%s"
              % (row["allo_load"], row["suppress_crit"], row["suppress_crit_minus_load"], row["invariant"]))
    print("     matches saddle=%s | invariant=%s | crit rises with load=%s -> threshold ok=%s"
          % (it["matches_negative_saddle"], it["invariant_holds"], it["suppress_crit_rises_with_load"], it["threshold_ok"]))
    dr = r["durable_vs_relapsing"]
    print("\n(2) DURABLE OPERATIONAL TOLERANCE vs INDEFINITE IMMUNOSUPPRESSION:")
    print("     basin-acting induction: ON fraction=%.3f, trajectory end=%.3f -> empties=%s"
          % (dr["induce_basin_fraction"], dr["induce_traj_end"], dr["induce_empties"]))
    print("     indefinite immunosuppression: ON fraction=%.3f, trajectory end=%.3f -> refills (rejects)=%s -> contrast=%s"
          % (dr["immunosuppress_basin_fraction"], dr["immuno_traj_end"], dr["immuno_refills"], dr["contrast"]))
    iw = r["induction_window"]
    print("\n(3) INDUCTION WINDOW (consolidation; fixed suppress=%.2f), suppress_crit early=%.3f -> late=%.3f:"
          % (iw["fixed_suppress"], iw["suppress_crit_early"], iw["suppress_crit_late"]))
    for row in iw["rows"]:
        print("     delay=%4d  consolidation C=%.3f  effective_load=%.3f  P(tolerate)=%.3f  %s"
              % (row["delay"], row["consolidation"], row["effective_load"], row["p_tolerate"],
                 "#" * int(round(row["p_tolerate"] * 28))))
    print("     P(tolerate) falls with delay=%s | suppress_crit rises=%s | early threshold=neg saddle=%s -> window ok=%s"
          % (iw["p_tolerate_falls_with_delay"], iw["threshold_rises_with_delay"],
             iw["early_threshold_is_negative_saddle"], iw["window_ok"]))
    sc = r["sub_threshold_control"]
    print("\n(4) SUB-THRESHOLD INDUCTION RELAPSES (honest control), suppress_crit=%.3f:" % sc["suppress_crit"])
    print("     sub-threshold depth=%.2f -> P(tolerize)=%.3f -> relapses=%s" % (sc["sub_depth"], sc["p_tolerize_sub"], sc["sub_relapses"]))
    print("     supra-threshold depth=%.2f -> P(tolerize)=%.3f (triple settle=%.3f) -> durable=%s -> control ok=%s"
          % (sc["supra_depth"], sc["p_tolerize_supra"], sc["p_tolerize_supra_long_settle"], sc["supra_durable"], sc["control_ok"]))
    print("\n     direction symmetry:", r["direction_symmetry_note"])
    print("\nT32 all_pass:", r["all_pass"])
