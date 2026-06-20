#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_regrowth.py  --  EMERGENT cytotoxic relapse vs differentiation cure as a MEASURED regrowth
time-course (the T13 relapse failure mode made explicit as a population trajectory).

WHY THIS EXISTS (v0.7.0). T13 (emergent_therapy.py) establishes the relapse failure mode at the BASIN-OCCUPANCY
level: cytotoxic killing leaves the landscape intact, so survivors stay in the malignant basin, whereas
differentiation empties the basin. fundamental_therapy.py states the relapse as a fact, not a trajectory. The
VP discipline is emergence: the relapse must come OUT of the dynamics as a MEASURED time course. This module
adds a population-growth layer on top of the substrate's basin structure and MEASURES the malignant-fraction
regrowth N(t)/K after each intervention. Two physical inputs are MEASURED from the R19 substrate first:

  • f_cyto — the ON-basin fraction of cytotoxic survivors (drive removed, basin UNTOUCHED): a population that
    started malignant is held at zero drive under noise and the residual ON occupancy is MEASURED (≈1: the
    survivors stay malignant by hysteresis — the same measurement as T13's drive-removal persistence).
  • f_diff — the ON-basin fraction after a supra-spinodal differentiating re-flip: a malignant population is
    driven across the spinodal and the residual ON occupancy is MEASURED (≈0: the basin is emptied, the cells
    re-flip to healthy — the same measurement as T13's differentiation re-flip).

The population then evolves with a stochastic logistic layer GATED by the measured basin fraction f: malignant
cells proliferate toward a carrying capacity K only while the malignant basin is their niche (f≈1), and
re-flipped cells leave the malignant pool when the basin is emptied (f≈0):

    births ~ Binomial(N, r·(1 − N/K)·f·dt)            # malignant proliferation (needs the malignant basin)
    deaths ~ Binomial(N, conv·(1 − f)·dt)             # re-flipped cells leave the malignant pool (differentiation)

  • CYTOTOXIC: kill fraction κ (N0 = (1−κ)·K survivors, all malignant, f = f_cyto ≈ 1) → MEASURE N(t)/K.
  • DIFFERENTIATION: no killing (N0 = K, f = f_diff ≈ 0) → MEASURE N(t)/K.

Nothing about relapse is assumed; N(t)/K is a counted population trajectory whose growth-vs-decay is gated by
the MEASURED R19 basin fraction.

WHAT EMERGES (measured, deterministic seed=19):
  1. RELAPSE vs CURE TRAJECTORY CONTRAST. The cytotoxic malignant fraction regrows monotonically from (1−κ)
     back toward the carrying capacity (recovers to ≥ 90% K — relapse), while the differentiation fraction
     decays monotonically to ≈ 0 (≤ 10% K — cure), MEASURED as time courses. The cleanest durable cure acts on
     the basin (differentiation), exactly as T13's occupancy contrast, now an explicit regrowth curve.
  2. RELAPSE IS BASIN-DETERMINED, NOT KILL-DEPTH-DETERMINED (falsifiable). Sweeping the kill fraction κ, a
     deeper cytotoxic kill only LENGTHENS the measured delay to regrow (time-to-half rises with κ) but every
     kill depth still recovers to ≥ 90% K — because the barrier and basin are untouched, the outcome is full
     relapse regardless of how many cells are killed. Maximal cytotoxic kill does not cure; the basin does.

GRADES (C3): the relapse-vs-cure trajectory contrast and the deeper-kill-longer-delay-but-full-recovery result
are [V] emergent (measured from the basin-gated stochastic population layer). The ABSOLUTE growth rate r,
conversion rate, and clinical schedule are [O] — no fabricated timelines or response numbers. Determinism:
fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_AML = "bone_marrow_hematopoiesis"     # cleanest occupational anchor

# --- measured R19 basin fractions (small stochastic Langevin sims, matching T13) ---------------------
_BN        = 800      # cells for the basin-occupancy measurement
_BDT       = 0.01     # basin-sim Langevin timestep
_BD        = 0.02     # cellular-noise scale (absolute value is [O])
_T_APPLY   = 30.0     # differentiating-drive application time
_T_RELAX   = 20.0     # settle after the drive is withdrawn
_T_HOLD    = 50.0     # drive-removal hold (cytotoxic survivors)
_SUP_FRAC  = 1.10     # supra-spinodal differentiating drive (empties the basin)

# --- population (regrowth) layer ---------------------------------------------------------------------
_K_POP     = 2000     # carrying capacity (malignant cells a tissue can hold; absolute scale is [O])
_M_POP     = 400      # independent tumours per condition
_PDT       = 0.05     # population timestep
_R_GROW    = 1.0      # malignant proliferation rate (arbitrary; [O])
_CONV      = 1.0      # re-flip conversion / clearance rate (arbitrary; [O])
_T_POP     = 300      # population steps (long enough to relapse or clear)
_KAPPA     = 0.99     # main cytotoxic kill fraction
_KAPPA_SWEEP = (0.5, 0.9, 0.99)   # kill-fraction sweep (deeper kill = longer delay, same full recovery)


def _basin_fraction(g, mode, D=_BD, N=_BN, dt=_BDT, seed=SEED):
    """MEASURE residual malignant-ON basin fraction after an intervention. mode: 'cytotoxic' or 'differentiation'."""
    rng = np.random.default_rng(seed)
    s = np.full(N, math.sqrt(g))                          # all cells start in the malignant ON basin
    sq = math.sqrt(2.0 * D * dt)
    if mode == "differentiation":
        h = -_SUP_FRAC * spinodal(g)                      # supra-spinodal differentiating drive
        for _ in range(int(_T_APPLY / dt)):
            s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
        for _ in range(int(_T_RELAX / dt)):               # withdraw, let it settle
            s += (g * s - s ** 3) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    else:                                                 # cytotoxic: drive removed, basin untouched (hysteresis)
        for _ in range(int(_T_HOLD / dt)):
            s += (g * s - s ** 3) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _regrowth(N0, f, K=_K_POP, M=_M_POP, dt=_PDT, T=_T_POP, r=_R_GROW, conv=_CONV, seed=SEED):
    """MEASURE the malignant population trajectory N(t)/K under a logistic layer GATED by the basin fraction f."""
    rng = np.random.default_rng(seed)
    N = np.full(M, int(N0), dtype=float)
    traj = np.empty(T)
    for t in range(T):
        p_grow = np.clip(r * (1.0 - N / K) * f * dt, 0.0, 1.0)          # malignant proliferation (needs the basin)
        p_decay = min(max(conv * (1.0 - f) * dt, 0.0), 1.0)            # re-flipped cells leave the malignant pool
        births = rng.binomial(N.astype(int), p_grow)
        deaths = rng.binomial(N.astype(int), p_decay) if p_decay > 0 else np.zeros(M, dtype=int)
        N = N + births - deaths
        np.clip(N, 0, K, out=N)
        traj[t] = float(N.mean()) / K
    return traj


def _time_to(traj, level, dt=_PDT, rising=True):
    """Measured time to first reach a fraction `level` of K (rising) — in time units."""
    for t in range(len(traj)):
        if (rising and traj[t] >= level) or ((not rising) and traj[t] <= level):
            return t * dt
    return len(traj) * dt


def _coarse_monotone(traj, rising=True, nb=10, tol=0.03):
    """Coarse block-mean monotone-trend check (tolerates stochastic jitter at the plateau/floor)."""
    blk = max(1, len(traj) // nb)
    means = [float(traj[i:i + blk].mean()) for i in range(0, len(traj) - blk + 1, blk)]
    if rising:
        return all(means[i + 1] >= means[i] - tol for i in range(len(means) - 1))
    return all(means[i + 1] <= means[i] + tol for i in range(len(means) - 1))


def emergent_regrowth(gammas):
    g = gammas[_AML]
    f_cyto = _basin_fraction(g, "cytotoxic")              # ≈ 1 (survivors stay malignant)
    f_diff = _basin_fraction(g, "differentiation")        # ≈ 0 (basin emptied)

    # ---- main contrast: cytotoxic (kill κ, basin intact) vs differentiation (no kill, basin emptied) ----
    cyto = _regrowth((1.0 - _KAPPA) * _K_POP, f_cyto, seed=SEED)
    diff = _regrowth(_K_POP, f_diff, seed=SEED + 1)
    cyto_final = float(cyto[-int(len(cyto) * 0.1):].mean())
    diff_final = float(diff[-int(len(diff) * 0.1):].mean())
    cyto_relapses = bool(cyto_final >= 0.90 and _coarse_monotone(cyto, rising=True))
    diff_cures    = bool(diff_final <= 0.10 and _coarse_monotone(diff, rising=False))
    relapse_vs_cure = bool(cyto_relapses and diff_cures)

    cyto_traj = [round(float(cyto[i]), 3) for i in range(0, len(cyto), max(1, len(cyto) // 10))]
    diff_traj = [round(float(diff[i]), 3) for i in range(0, len(diff), max(1, len(diff) // 10))]

    # ---- kill-depth sweep: deeper kill = longer delay, but every depth recovers to ≥0.9 K --------------
    sweep = []
    for k, kap in enumerate(_KAPPA_SWEEP):
        tr = _regrowth((1.0 - kap) * _K_POP, f_cyto, seed=SEED + 10 + k)
        final = float(tr[-int(len(tr) * 0.1):].mean())
        t_half = _time_to(tr, 0.5, rising=True)
        sweep.append(dict(kill_fraction=round(kap, 3),
                          initial_fraction=round((1.0 - kap), 3),
                          final_fraction=round(final, 3),
                          time_to_half_K=round(t_half, 3),
                          recovers_to_90pct=bool(final >= 0.90)))
    delays = [s["time_to_half_K"] for s in sweep]
    deeper_kill_longer_delay = all(delays[i + 1] >= delays[i] - 1e-9 for i in range(len(delays) - 1))
    all_recover = all(s["recovers_to_90pct"] for s in sweep)
    basin_determined = bool(deeper_kill_longer_delay and all_recover)

    ok = bool(relapse_vs_cure and basin_determined)
    return dict(
        site="acute myeloid leukemia (marrow R19 switch)", gamma=round(g, 6),
        measured_basin_fraction=dict(cytotoxic_survivors_ON=round(f_cyto, 3),
                                     differentiation_residual_ON=round(f_diff, 3)),
        carrying_capacity_K=_K_POP, kill_fraction=_KAPPA,
        cytotoxic_regrowth_fraction_of_K=cyto_traj,
        differentiation_fraction_of_K=diff_traj,
        cytotoxic_final_fraction=round(cyto_final, 3),
        differentiation_final_fraction=round(diff_final, 3),
        cytotoxic_relapses=bool(cyto_relapses),
        differentiation_cures=bool(diff_cures),
        relapse_vs_cure_contrast=bool(relapse_vs_cure),
        kill_depth_sweep=sweep,
        deeper_kill_longer_delay=bool(deeper_kill_longer_delay),
        every_kill_depth_recovers=bool(all_recover),
        relapse_is_basin_determined=bool(basin_determined),
        all_pass=ok,
        grade="[V] the cytotoxic relapse vs differentiation cure EMERGES as a measured regrowth time-course: the "
              "malignant fraction regrows toward the carrying capacity after cytotoxic killing (≥90% K, basin "
              "intact) while it decays to ≈0 after a differentiating re-flip (≤10% K, basin emptied), and a "
              "deeper kill only lengthens the regrowth delay while every kill depth still fully recovers — so "
              "relapse is basin-determined, not kill-depth-determined (measured, not asserted); [O] absolute "
              "growth rate / conversion rate / clinical schedule")


def run(gammas):
    """T17: emergent cytotoxic relapse — the relapse-vs-cure failure mode MEASURED as a regrowth time-course."""
    r = emergent_regrowth(gammas)
    return dict(T17=dict(target="T17",
                         claim="the cytotoxic relapse failure mode EMERGES as a measured regrowth time-course "
                               "of a basin-gated population layer: cytotoxic killing leaves the malignant basin "
                               "intact so the malignant fraction regrows toward carrying capacity (≥90% K, "
                               "relapse) while a differentiating re-flip empties the basin so it decays to ≈0 "
                               "(≤10% K, cure), and sweeping the kill fraction shows a deeper kill only lengthens "
                               "the delay while every depth fully recovers — relapse is basin-determined, not "
                               "kill-depth-determined; absolute growth rate / schedule stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T17"]["result"]
    print("CYTOTOXIC RELAPSE vs DIFFERENTIATION CURE — regrowth time-course (AML marrow switch, γ=%.4f):" % r["gamma"])
    print("measured basin fraction: cytotoxic survivors ON=%.3f | differentiation residual ON=%.3f"
          % (r["measured_basin_fraction"]["cytotoxic_survivors_ON"], r["measured_basin_fraction"]["differentiation_residual_ON"]))
    print("\ncytotoxic regrowth N(t)/K:", r["cytotoxic_regrowth_fraction_of_K"])
    print("differentiation  N(t)/K:", r["differentiation_fraction_of_K"])
    print("cytotoxic final=%.3f (relapses=%s) | differentiation final=%.3f (cures=%s) -> contrast=%s"
          % (r["cytotoxic_final_fraction"], r["cytotoxic_relapses"],
             r["differentiation_final_fraction"], r["differentiation_cures"], r["relapse_vs_cure_contrast"]))
    print("\nkill-depth sweep (deeper kill = longer delay, same full recovery):")
    print("  kill_frac   initial   final   time_to_half_K   recovers_90%")
    for s in r["kill_depth_sweep"]:
        print("    %.2f       %.3f    %.3f      %.2f           %s"
              % (s["kill_fraction"], s["initial_fraction"], s["final_fraction"], s["time_to_half_K"], s["recovers_to_90pct"]))
    print("deeper kill longer delay:", r["deeper_kill_longer_delay"], "| every depth recovers:", r["every_kill_depth_recovers"])
    print("relapse is basin-determined:", r["relapse_is_basin_determined"])
    print("T17 all_pass:", r["all_pass"])
