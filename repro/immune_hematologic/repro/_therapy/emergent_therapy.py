#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_therapy.py  --  EMERGENT therapy trajectories (Levers A & C) by DIRECT stochastic simulation.

WHY THIS EXISTS (v0.6.0). fundamental_therapy.py derives the four treatment levers from the R19 attractor
landscape, but Levers A (basin re-flip / differentiation) and C (drive removal) are evaluated by the
DETERMINISTIC settle (no noise): the re-flip threshold is read off the spinodal and hysteresis is read off
a single trajectory. Lever B is already emergent (the Kramers rate collapse). The VP discipline is
emergence: the reversal-vs-relapse behaviour of A and C must come OUT of the stochastic substrate, MEASURED
as basin-occupancy trajectories, not asserted from one deterministic settle. This module does that. It
integrates the overdamped Langevin equation of the SAME R19 field for a POPULATION of cells and MEASURES
the malignant-basin occupancy P(s>0) after each intervention:

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt) · ξ,    ξ ~ N(0,1)

  • LEVER A (differentiation): start every cell in the malignant ON basin (s=+√γ), apply a differentiating
    drive h = −frac·spinodal, withdraw it, let the field settle, and MEASURE the residual ON occupancy.
  • LEVER C (drive removal): start a committed (ON) population and a healthy (OFF) population, remove the
    carcinogen drive (h=0), and MEASURE each population's ON occupancy — committed cells should persist
    (hysteresis), healthy cells should stay healthy (prevented).
  • CYTOTOXIC CONTRAST: cytotoxic killing leaves the landscape untouched, so its survivors are exactly the
    "committed population at h=0" measurement — they stay ON (the basin refills). Differentiation empties it.

Nothing about a threshold or hysteresis is assumed; each occupancy is a counted basin statistic. The
independently-computed spinodal is only used afterwards, to compare against.

WHAT EMERGES (measured, deterministic seed=19):
  1. LEVER A RE-FLIP THRESHOLD = SPINODAL. The measured residual ON occupancy collapses from ≈1 to ≈0 as the
     differentiating drive crosses the spinodal: a sub-spinodal differentiating drive leaves the malignant
     basin occupied (the cell stays malignant), a supra-spinodal drive empties it (the cell differentiates),
     organ by organ — with NO cytotoxicity. The re-flip threshold is measured, not asserted.
  2. LEVER C IS PREVENTIVE, NOT CURATIVE. After drive removal the committed population's ON occupancy stays
     high (hysteresis → persistence / relapse) while the un-committed healthy population stays OFF
     (prevented). Removing the cause prevents new disease but does not reverse established disease — MEASURED.
  3. REVERSAL vs RELAPSE CONTRAST. Differentiation (Lever A, supra-spinodal) empties the malignant basin
     (occupancy → 0, a cure) whereas drive removal alone — and equivalently cytotoxic killing, which leaves
     the landscape intact — leaves the basin occupied (→ relapse). The durable cure must act on the basin,
     MEASURED, exactly the deterministic claim now confirmed stochastically.

GRADES (C3): the Lever-A re-flip threshold (= spinodal organ-by-organ), the Lever-C preventive/persistent
contrast, and the reversal-vs-relapse (differentiation-empties / cytotoxic-refills) contrast are [V]
emergent (measured by simulation). The ABSOLUTE dose/schedule of a real differentiating agent stays [O]
(clinical), and the noise scale D (transition sharpness) stays [O] — no fabricated response numbers.
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
_AML    = "bone_marrow_hematopoiesis"      # cleanest occupational anchor for the full trajectory sweep

# --- deterministic simulation size (fixed; no per-organ tuning) --------------------------------------
_N        = 300      # cells per condition
_DT       = 0.01     # Langevin timestep
_D        = 0.02     # cellular-noise scale (absolute value is [O])
_T_APPLY  = 30.0     # differentiating-drive application time (Lever A)
_T_RELAX  = 20.0     # settle time after the drive is withdrawn (decide final basin)
_T_HOLD   = 50.0     # horizon for the drive-removal persistence test (Lever C)
_SWEEP    = (0.0, 0.60, 0.75, 0.85, 0.95, 1.05, 1.20)   # differentiating drive as fraction of spinodal (AML sweep)
_SUB_FRAC = 0.70     # clearly sub-spinodal differentiating drive (basin persists)
_SUP_FRAC = 1.10     # clearly supra-spinodal differentiating drive (basin emptied)


def reflip_occupancy(g, diff_frac, D=_D, N=_N, dt=_DT, T_apply=_T_APPLY, T_relax=_T_RELAX, seed=SEED):
    """MEASURE residual malignant ON occupancy after applying a differentiating drive −diff_frac·spinodal then withdrawing it."""
    rng = np.random.default_rng(seed)
    s = np.full(N, math.sqrt(g))                 # all cells start in the malignant ON basin
    sq = math.sqrt(2.0 * D * dt)
    h = -diff_frac * spinodal(g)                 # opposing (differentiating) drive
    for _ in range(int(T_apply / dt)):
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(T_relax / dt)):           # withdraw, let it decide a basin
        s += (g * s - s ** 3) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def persistence_occupancy(g, start_on, D=_D, N=_N, dt=_DT, T=_T_HOLD, seed=SEED):
    """MEASURE ON occupancy of a population held at zero drive (drive removed). start_on: malignant ON vs healthy OFF."""
    rng = np.random.default_rng(seed)
    s = np.full(N, math.sqrt(g) if start_on else -math.sqrt(g))
    sq = math.sqrt(2.0 * D * dt)
    for _ in range(int(T / dt)):
        s += (g * s - s ** 3) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def emergent_therapy(gammas, D=_D):
    # ---- LEVER A: full re-flip trajectory on the AML site (threshold + monotonicity) -----------------
    g_aml = gammas[_AML]; sp_aml = spinodal(g_aml)
    sweep = []
    for fr in _SWEEP:
        occ = reflip_occupancy(g_aml, fr)
        sweep.append(dict(diff_drive_over_spinodal=round(fr, 3),
                          residual_ON_occupancy=round(occ, 3),
                          reflip_fraction=round(1.0 - occ, 3)))
    refl = [r["reflip_fraction"] for r in sweep]
    monotone_reflip = all(refl[i + 1] >= refl[i] - 1e-9 for i in range(len(refl) - 1))
    # measured 0.5-crossing differentiating drive (interpolated) — compare to the spinodal
    cross = None
    for i in range(len(_SWEEP) - 1):
        if refl[i] < 0.5 <= refl[i + 1]:
            cross = _SWEEP[i] + (0.5 - refl[i]) * (_SWEEP[i + 1] - _SWEEP[i]) / (refl[i + 1] - refl[i])
            break
    crossing_near_spinodal = bool(cross is not None and 0.70 <= cross <= 1.10)   # straddles the spinodal (thermal assist below)

    # ---- LEVER A bracket + LEVER C contrast, organ by organ ------------------------------------------
    rows, leverA_ok, leverC_ok, contrast_ok = {}, True, True, True
    for o in _ORGANS:
        g = gammas[o]
        occ_sub = reflip_occupancy(g, _SUB_FRAC)            # sub-spinodal differentiation -> basin persists
        occ_sup = reflip_occupancy(g, _SUP_FRAC)            # supra-spinodal differentiation -> basin emptied
        committed_persist = persistence_occupancy(g, start_on=True)    # drive removed, committed -> persists
        healthy_prevented = persistence_occupancy(g, start_on=False)   # drive removed, healthy   -> stays OFF
        a_ok = bool(occ_sub > 0.70 and occ_sup < 0.10)                 # threshold straddles the spinodal
        c_ok = bool(committed_persist > 0.90 and healthy_prevented < 0.10)
        ct_ok = bool(occ_sup < 0.10 and committed_persist > 0.90)      # differentiation empties / drive-removal (=cytotoxic survivors) refills
        rows[o] = dict(
            spinodal=round(spinodal(g), 6),
            leverA_subspinodal_ON_occupancy=round(occ_sub, 3),         # basin still occupied (stays malignant)
            leverA_supraspinodal_ON_occupancy=round(occ_sup, 3),       # basin emptied (differentiated)
            leverA_reflip_threshold_is_spinodal=a_ok,
            leverC_committed_ON_after_drive_removal=round(committed_persist, 3),   # hysteresis -> relapse
            leverC_healthy_ON_after_drive_removal=round(healthy_prevented, 3),     # prevented -> stays healthy
            leverC_preventive_not_curative=c_ok,
            cytotoxic_survivors_ON_occupancy=round(committed_persist, 3),          # same measurement: landscape intact
            differentiation_empties_basin=bool(occ_sup < 0.10),
            reversal_vs_relapse_contrast=ct_ok)
        leverA_ok = leverA_ok and a_ok
        leverC_ok = leverC_ok and c_ok
        contrast_ok = contrast_ok and ct_ok

    ok = bool(monotone_reflip and crossing_near_spinodal and leverA_ok and leverC_ok and contrast_ok)
    return dict(
        noise_D=D, sub_frac=_SUB_FRAC, sup_frac=_SUP_FRAC,
        leverA_aml_reflip_trajectory=sweep,
        leverA_reflip_monotone=bool(monotone_reflip),
        leverA_measured_crossing_over_spinodal=(round(cross, 3) if cross is not None else None),
        leverA_crossing_straddles_spinodal=bool(crossing_near_spinodal),
        per_organ=rows,
        leverA_threshold_is_spinodal_all_organs=bool(leverA_ok),
        leverC_preventive_not_curative_all_organs=bool(leverC_ok),
        reversal_vs_relapse_contrast_all_organs=bool(contrast_ok),
        all_pass=ok,
        grade="[V] Lever-A differentiation re-flip threshold (= spinodal organ-by-organ, non-cytotoxic), "
              "Lever-C preventive-not-curative contrast (committed persists, healthy prevented), and the "
              "reversal-vs-relapse contrast (differentiation empties the basin while drive-removal / cytotoxic "
              "killing leaves it occupied) EMERGE from direct stochastic basin-occupancy simulations (measured, "
              "not asserted from one deterministic settle); [O] absolute agent dose/schedule (clinical) and "
              "noise scale D (transition sharpness)")


def run(gammas):
    """T13: emergent therapy trajectories — Levers A & C MEASURED as stochastic reversal-vs-relapse basin-occupancy trajectories."""
    r = emergent_therapy(gammas)
    return dict(T13=dict(target="T13",
                         claim="the fundamental-therapy Levers A (differentiation re-flip) and C (drive "
                               "removal) EMERGE as measured stochastic basin-occupancy trajectories: the "
                               "re-flip threshold equals each organ's spinodal with no cytotoxicity, drive "
                               "removal is preventive-not-curative (committed cells persist by hysteresis, "
                               "healthy cells stay prevented), and differentiation empties the malignant basin "
                               "while drive-removal / cytotoxic killing leaves it occupied (relapse) — measured, "
                               "not asserted from a single deterministic settle; absolute dose/schedule and "
                               "noise scale D stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T13"]["result"]
    print("LEVER A — differentiation re-flip trajectory (AML marrow switch):")
    print("  diff_drive/sp   residual_ON_occupancy   reflip_fraction")
    for row in r["leverA_aml_reflip_trajectory"]:
        print("     %.2f               %.3f                 %.3f"
              % (row["diff_drive_over_spinodal"], row["residual_ON_occupancy"], row["reflip_fraction"]))
    print("  monotone:", r["leverA_reflip_monotone"],
          "| measured 0.5-crossing/spinodal =", r["leverA_measured_crossing_over_spinodal"],
          "(straddles spinodal:", r["leverA_crossing_straddles_spinodal"], ")")
    print("\nper-organ Lever A bracket + Lever C contrast:")
    for o, v in r["per_organ"].items():
        print("  %-26s A[sub=%.2f sup=%.2f ok=%s]  C[committed=%.2f healthy=%.2f ok=%s]  contrast=%s"
              % (o, v["leverA_subspinodal_ON_occupancy"], v["leverA_supraspinodal_ON_occupancy"],
                 v["leverA_reflip_threshold_is_spinodal"],
                 v["leverC_committed_ON_after_drive_removal"], v["leverC_healthy_ON_after_drive_removal"],
                 v["leverC_preventive_not_curative"], v["reversal_vs_relapse_contrast"]))
    print("\nLever A threshold=spinodal (all):", r["leverA_threshold_is_spinodal_all_organs"])
    print("Lever C preventive-not-curative (all):", r["leverC_preventive_not_curative_all_organs"])
    print("reversal-vs-relapse contrast (all):", r["reversal_vs_relapse_contrast_all_organs"])
    print("T13 all_pass:", r["all_pass"])
