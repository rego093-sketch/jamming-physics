#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_barrier_restoration.py  --  EMERGENT therapy Lever B (barrier restoration) by DIRECT stochastic
simulation (a MEASURED crossing-rate-vs-restored-barrier trajectory, not a closed form).

WHY THIS EXISTS (v0.7.0). fundamental_therapy.py derives Lever B from the R19 kernel, but it evaluates the
crossing rate with the CLOSED-FORM Kramers law rate = exp(−barrier/kT): restore a fraction of the lost
barrier, plug it into the exponential, and read off the collapse. T7 already showed that the Kramers law
EMERGES from the stochastic substrate in the carcinogenic direction (barrier eroded). The VP discipline is
emergence: Lever B's rate collapse must come OUT of the substrate dynamics in the THERAPEUTIC direction —
MEASURED as crossings are counted while the barrier is stepped back up — not asserted from the same formula.
This module does that. It integrates the overdamped Langevin equation of the SAME R19 field

    ds = (γ s − s³ + h) dt + sqrt(2 D dt) · ξ,      ξ ~ N(0,1),    start OFF at s = −√γ

for a population of healthy cells, where a carcinogen of fixed dose erodes the barrier and a restoration
fraction rf counteracts a fraction of that erosion (tumour-suppressor / epigenetic control returning):

    h(rf)        = dose_frac · (1 − rf) · spinodal(γ)            # net drive falls as the barrier is restored
    barrier(rf)  = (γ²/4) · (1 − dose_frac · (1 − rf))           # independently-computed restored barrier

and MEASURES the malignant crossing rate at each rf as (# cells that cross the ridge s=0) / (total cell-time
observed) — exactly the counted barrier-crossing statistic of emergent_kramers.py, swept in the restoration
direction. NOTHING about the exponential collapse is assumed; the rate is a counted statistic and the
independently-computed barrier is only compared against afterwards.

WHAT EMERGES (measured, deterministic seed=19):
  1. RATE COLLAPSE. The measured crossing rate falls monotonically as the barrier is restored (rf: 0→1) —
     restoring tumour-suppressor control collapses the malignant crossing rate, MEASURED, with a large
     multiplicative drop at full restoration (rate(rf=1) ≪ rate(rf=0)).
  2. KRAMERS LAW EMERGES IN THE THERAPEUTIC DIRECTION. log(measured rate) is LINEAR in the independently
     computed restored barrier (high R²) with an Arrhenius slope ≈ −1/D, so the exponential rate∝exp(−barrier/D)
     dependence that fundamental_therapy.py used as a closed form is now an EMERGENT property of the simulated
     restoration trajectory — the time-domain / measured twin of the Lever-B exponential collapse.

GRADES (C3): the rate collapse and the emergent Kramers law (the SHAPE of Lever B) are [V] emergent
(measured by simulation); the ABSOLUTE multiplicative factor — set by the free cellular-noise scale D — stays
[O] (no fabricated rate-drop numbers). Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, SEED

_ORGANS = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_AML    = "bone_marrow_hematopoiesis"          # cleanest occupational anchor for the full trajectory sweep

# --- deterministic simulation size (fixed; no per-organ tuning) --------------------------------------
_N         = 480      # walkers (cells) per restoration level
_DT        = 0.005    # Langevin timestep
_T_MAX     = 30.0     # observation horizon per walker (same horizon at every rf — no per-level tuning)
_D         = 0.12     # cellular-noise scale (representative; keeps rates measurable across the sweep; [O])
_DOSE_FRAC = 0.6      # fixed carcinogen dose (fraction of spinodal) that erodes the barrier
_RESTORE   = (0.0, 0.25, 0.5, 0.75, 1.0)   # fraction of the lost barrier restored (therapeutic sweep)


def measure_rate(g, h, D=_D, N=_N, dt=_DT, T_max=_T_MAX, seed=SEED):
    """MEASURED malignant-crossing rate: count ridge crossings of the stochastic R19 field at net drive h. No formula."""
    rng = np.random.default_rng(seed)
    s = np.full(N, -math.sqrt(g))                 # all cells start healthy (OFF basin)
    crossed = np.zeros(N, dtype=bool)
    tcross = np.full(N, T_max)
    sq = math.sqrt(2.0 * D * dt)
    for i in range(int(T_max / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
        newly = (~crossed) & (s > 0.0)            # crossed the ridge into the malignant basin
        if newly.any():
            tcross[newly] = (i + 1) * dt
            crossed[newly] = True
        if crossed.all():
            break
    total_time = float(np.minimum(tcross, T_max).sum())
    return (int(crossed.sum()) / total_time) if total_time > 0 else 0.0


def restoration_trajectory(g, D=_D, dose_frac=_DOSE_FRAC, restore=_RESTORE):
    """Measure crossing rate vs restored barrier; test emergent monotone collapse + the emergent Kramers law."""
    sp = spinodal(g); b0 = barrier(g)
    rates, beff = [], []
    for rf in restore:
        h = dose_frac * (1.0 - rf) * sp                # net carcinogenic drive after restoring fraction rf
        beff.append(b0 * (1.0 - dose_frac * (1.0 - rf)))   # independently-computed restored barrier
        rates.append(measure_rate(g, h, D=D))
    traj = [dict(restore_fraction=round(restore[i], 3),
                 restored_barrier=round(beff[i], 6),
                 measured_crossing_rate=round(rates[i], 8))
            for i in range(len(restore))]

    # (1) monotone collapse: rate non-increasing as the barrier is restored
    monotone = all(rates[i + 1] <= rates[i] + 1e-12 for i in range(len(rates) - 1))
    r0 = rates[0]
    full_drop = (rates[-1] / r0) if r0 > 0 else 0.0    # < 1: restoring lowers the rate (multiplicative drop)
    big_drop = bool(r0 > 0 and full_drop < 0.5)

    # (2) Kramers/Arrhenius EMERGES in the therapeutic direction: log(rate) linear in restored barrier, slope ~ -1/D
    xs = np.array([beff[i] for i in range(len(rates)) if rates[i] > 0])
    ys = np.log(np.array([rates[i] for i in range(len(rates)) if rates[i] > 0]))
    if len(xs) >= 3:
        A = np.vstack([xs, np.ones_like(xs)]).T
        slope, intercept = np.linalg.lstsq(A, ys, rcond=None)[0]
        resid = ys - (slope * xs + intercept)
        denom = float(((ys - ys.mean()) ** 2).sum())
        r2 = 1.0 - float((resid ** 2).sum() / denom) if denom > 0 else 0.0
        slope_recovers_invD = abs((-slope) - (1.0 / D)) / (1.0 / D) < 0.30
    else:
        slope, r2, slope_recovers_invD = 0.0, 0.0, False

    ok = bool(monotone and big_drop and r2 > 0.95 and slope_recovers_invD)
    return dict(
        gamma=round(g, 6), noise_D=D, dose_frac=dose_frac, restore_fractions=list(restore),
        trajectory=traj,
        rate_monotone_decreasing=bool(monotone),
        full_restoration_rate_drop=round(full_drop, 8),
        large_multiplicative_drop=bool(big_drop),
        arrhenius_R2=round(r2, 4), arrhenius_slope=round(float(slope), 4),
        expected_slope_minus_1_over_D=round(-1.0 / D, 4),
        slope_recovers_minus_1_over_D=bool(slope_recovers_invD),
        kramers_emerges=bool(r2 > 0.95 and slope_recovers_invD),
        all_pass=ok)


def emergent_barrier_restoration(gammas, D=_D):
    # full trajectory on the AML site (collapse shape + emergent Kramers law)
    aml = restoration_trajectory(gammas[_AML], D=D)
    # per-organ bracket: every organ collapses with a large drop from the eroded to the fully restored barrier.
    # AML reuses its full-trajectory endpoints; the other organs use a fast 2-point bracket (no full sweep).
    rows, bracket_ok = {}, True
    for o in _ORGANS:
        if o == _AML:
            eroded = aml["trajectory"][0]["measured_crossing_rate"]
            restored = aml["trajectory"][-1]["measured_crossing_rate"]
            monotone = aml["rate_monotone_decreasing"]
        else:
            g = gammas[o]; sp = spinodal(g)
            eroded = round(measure_rate(g, _DOSE_FRAC * sp, D=D), 8)             # rf = 0 (eroded barrier)
            restored = round(measure_rate(g, 0.0, D=D), 8)                       # rf = 1 (full barrier, h=0)
            monotone = bool(restored <= eroded + 1e-12)
        drop = (restored / eroded) if eroded > 0 else 0.0
        large = bool(eroded > 0 and drop < 0.5)
        rows[o] = dict(eroded_rate=eroded, restored_rate=restored,
                       full_restoration_rate_drop=round(drop, 8),
                       rate_monotone_decreasing=monotone, large_multiplicative_drop=large)
        bracket_ok = bracket_ok and monotone and large
    ok = bool(aml["all_pass"] and bracket_ok)
    return dict(
        aml_restoration_trajectory=aml,
        per_organ=rows,
        all_organs_collapse=bool(bracket_ok),
        all_pass=ok,
        grade="[V] Lever-B barrier restoration EMERGES as a measured crossing-rate-vs-restored-barrier "
              "trajectory: the counted malignant crossing rate collapses monotonically as the barrier is "
              "stepped back up (large multiplicative drop at full restoration) and log(rate) is linear in the "
              "restored barrier with slope recovering −1/D, so the Kramers exponential collapse is measured in "
              "the therapeutic direction, not asserted from the closed form; [O] absolute multiplicative factor "
              "/ cellular-noise scale D (free, uncalibrated)")


def run(gammas):
    """T14: emergent Lever B — barrier restoration MEASURED as a stochastic crossing-rate-vs-restored-barrier trajectory."""
    r = emergent_barrier_restoration(gammas)
    return dict(T14=dict(target="T14",
                         claim="fundamental-therapy Lever B (barrier restoration) EMERGES as a measured "
                               "crossing-rate-vs-restored-barrier trajectory of the stochastic R19 field: as a "
                               "fraction of the carcinogen-eroded barrier is restored, the counted malignant "
                               "crossing rate collapses monotonically (a large multiplicative drop at full "
                               "restoration) and log-rate is linear in the restored barrier (Kramers law emerges "
                               "in the therapeutic direction, slope recovers −1/D) — measured, not asserted from "
                               "the closed-form exponential; absolute factor / noise scale D stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T14"]["result"]
    a = r["aml_restoration_trajectory"]
    print("LEVER B — barrier-restoration trajectory (AML marrow switch, γ=%.4f, D=%.2f):" % (a["gamma"], a["noise_D"]))
    print("  restore_frac   restored_barrier   MEASURED_crossing_rate")
    for row in a["trajectory"]:
        print("     %.2f             %.4f              %.6f"
              % (row["restore_fraction"], row["restored_barrier"], row["measured_crossing_rate"]))
    print("  monotone collapse:", a["rate_monotone_decreasing"],
          "| full-restoration rate drop:", a["full_restoration_rate_drop"],
          "(large:", a["large_multiplicative_drop"], ")")
    print("  Arrhenius R^2 = %.4f, slope = %.3f (expect %.3f = -1/D) -> Kramers emerges: %s"
          % (a["arrhenius_R2"], a["arrhenius_slope"], a["expected_slope_minus_1_over_D"], a["kramers_emerges"]))
    print("\nper-organ collapse bracket:")
    for o, v in r["per_organ"].items():
        print("  %-26s eroded=%.5f restored=%.5f drop=%.5f monotone=%s large=%s"
              % (o, v["eroded_rate"], v["restored_rate"], v["full_restoration_rate_drop"],
                 v["rate_monotone_decreasing"], v["large_multiplicative_drop"]))
    print("\nall organs collapse:", r["all_organs_collapse"])
    print("T14 all_pass:", r["all_pass"])
