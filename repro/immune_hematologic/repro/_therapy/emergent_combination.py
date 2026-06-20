#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_combination.py  --  EMERGENT combination-therapy contrast: a cytotoxic cull combined with a
basin-acting lever (differentiation re-flip OR surveillance clearance) CONVERTS the relapse curve into a cure
curve, MEASURED as a population trajectory (not asserted, not fitted).

WHY THIS EXISTS (v0.8.0). T17 (emergent_regrowth.py) measures, as a population trajectory, that a cytotoxic cull
ALONE relapses (the basin is intact, so the malignant fraction regrows toward carrying capacity) while a
differentiating re-flip ALONE cures (the basin is emptied, so it decays to ~0). The clinically decisive
question is the COMBINATION: what happens when a cytotoxic cull is given together with a basin/niche-acting
lever? The VP prediction from the attractor picture is sharp — the cull lowers the seed and the basin/niche
lever removes the malignant niche, so the combination should convert the relapse curve into a cure curve, and
the cull should ACCELERATE the cure (less cumulative burden) without being able to cure on its own. The VP
discipline is emergence: this must come OUT of the same basin-gated stochastic population layer, MEASURED.

Two physical basin inputs are MEASURED from the R19 substrate first (exactly as in T17):
  • f_cyto — the ON-basin fraction of cytotoxic survivors (drive removed, basin UNTOUCHED): a malignant
    population held at zero drive under noise keeps occupancy ≈ 1 (survivors stay malignant by hysteresis).
  • f_diff — the ON-basin fraction after a supra-spinodal differentiating re-flip: a malignant population driven
    across the spinodal empties the basin, occupancy ≈ 0.

The population then evolves with a stochastic logistic layer GATED by the measured basin fraction f, now with a
THIRD channel — an immune-surveillance clearance rate mu_surv (Lever D restored): committed cells are cleared
at rate mu_surv while the basin is intact (f ≈ 1):

    births       ~ Binomial(N, r·(1 − N/K)·f·dt)        # malignant proliferation (needs the malignant basin)
    deaths_diff  ~ Binomial(N, conv·(1 − f)·dt)         # re-flipped cells leave the pool (differentiation)
    deaths_surv  ~ Binomial(N, mu_surv·dt)              # restored immune surveillance clears committed cells

The five arms MEASURED:
  1. CYTOTOXIC alone        N0=(1−κ)K, f=f_cyto, mu_surv=0          → relapse
  2. DIFFERENTIATION alone  N0=K,      f=f_diff, mu_surv=0          → cure
  3. CYTOTOXIC + DIFF       N0=(1−κ)K, f=f_diff, mu_surv=0          → cure (conversion), lower cumulative burden
  4. SURVEILLANCE alone     N0=K,      f=f_cyto, mu_surv=μ*(>r)     → cure
  5. CYTOTOXIC + SURV       N0=(1−κ)K, f=f_cyto, mu_surv=μ*(>r)     → cure (conversion), lower cumulative burden

Nothing about the conversion is assumed; each N(t)/K is a counted population trajectory whose growth-vs-decay is
gated by the MEASURED basin fraction and the surveillance channel. The surveillance channel has an EMERGENT
threshold at mu_surv = r (the malignant growth rate): below it the population settles at an interior relapse
fixed point N* = K(1 − mu_surv/r) > 0; at/above it the population is driven to ~0 (cure). "Restored surveillance"
means mu_surv above this measured threshold — not a tuned magic number.

WHAT EMERGES (measured, deterministic seed=19):
  1. RELAPSE → CURE CONVERSION. A cytotoxic cull that relapses ALONE (≥90% K) is converted to a cure (≤10% K)
     when combined with EITHER basin/niche lever (differentiation re-flip or restored surveillance), MEASURED as
     a trajectory: the basin/niche lever removes the malignant niche while the cull lowers the seed.
  2. THE CULL ACCELERATES (lower cumulative burden). For both levers, the combination clears with LESS cumulative
     malignant burden (smaller area under the N(t)/K curve) than the basin/niche lever alone — the cull lowers
     the seed, so the same cure is reached from a lower starting point, MEASURED.
  3. THE CULL CANNOT CURE ALONE (basin/niche lever is necessary). The cytotoxic arm with no basin/niche lever
     relapses to carrying capacity regardless — the curative element is the basin/niche lever, the cull is
     adjuvant. This mirrors T17's basin-determined relapse, now in the combination direction.
  4. SURVEILLANCE THRESHOLD (honest, measured). Sweeping mu_surv shows the emergent threshold at the growth rate:
     a sub-threshold surveillance leaves an interior relapse fixed point, a supra-threshold (restored)
     surveillance cures — the final burden falls monotonically with surveillance, MEASURED.

GRADES (C3): the relapse→cure conversion under combination, the cull-accelerates (lower cumulative burden)
result, the cull-cannot-cure-alone necessity, and the surveillance threshold are [V] emergent (measured from the
basin-gated stochastic population layer with the surveillance channel). The ABSOLUTE growth rate r, conversion /
clearance rates, and clinical schedule are [O] — no fabricated timelines or response numbers. Determinism:
fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_AML = "bone_marrow_hematopoiesis"     # cleanest occupational anchor (same site as T17)

# --- measured R19 basin fractions (small stochastic Langevin sims, matching T17) ---------------------
_BN        = 600      # cells for the basin-occupancy measurement
_BDT       = 0.01     # basin-sim Langevin timestep
_BD        = 0.02     # cellular-noise scale (absolute value is [O])
_T_APPLY   = 30.0     # differentiating-drive application time
_T_RELAX   = 20.0     # settle after the drive is withdrawn
_T_HOLD    = 50.0     # drive-removal hold (cytotoxic survivors)
_SUP_FRAC  = 1.10     # supra-spinodal differentiating drive (empties the basin)

# --- population (regrowth) layer ---------------------------------------------------------------------
_K_POP     = 2000     # carrying capacity (absolute scale is [O])
_M_POP     = 400      # independent tumours per condition
_PDT       = 0.05     # population timestep
_R_GROW    = 1.0      # malignant proliferation rate (arbitrary; [O])
_CONV      = 1.0      # re-flip conversion rate (arbitrary; [O])
_T_POP     = 300      # population steps (long enough to relapse or clear)
_KAPPA     = 0.90     # cytotoxic kill fraction (seed = 0.1 K — a meaningful, non-degenerate seed)
_MU_RESTORED = 2.0    # restored-surveillance clearance rate (clearly above the growth threshold r)
_MU_SWEEP  = (0.3, 1.0, 2.0)   # surveillance sweep: below / at / above the growth-rate threshold r=1.0


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


def _regrowth(N0, f, mu_surv=0.0, K=_K_POP, M=_M_POP, dt=_PDT, T=_T_POP, r=_R_GROW, conv=_CONV, seed=SEED):
    """MEASURE the malignant population trajectory N(t)/K under a basin-gated logistic layer with three channels:
    malignant proliferation (needs the basin, f), differentiation clearance (1−f), surveillance clearance (mu_surv)."""
    rng = np.random.default_rng(seed)
    N = np.full(M, int(N0), dtype=float)
    traj = np.empty(T)
    p_decay = min(max(conv * (1.0 - f) * dt, 0.0), 1.0)               # re-flipped cells leave the pool
    p_clear = min(max(mu_surv * dt, 0.0), 1.0)                        # restored surveillance clears committed cells
    for t in range(T):
        p_grow = np.clip(r * (1.0 - N / K) * f * dt, 0.0, 1.0)        # malignant proliferation (needs the basin)
        Ni = N.astype(int)
        births = rng.binomial(Ni, p_grow)
        deaths = np.zeros(M, dtype=int)
        if p_decay > 0: deaths = deaths + rng.binomial(Ni, p_decay)
        if p_clear > 0: deaths = deaths + rng.binomial(Ni, p_clear)
        N = N + births - deaths
        np.clip(N, 0, K, out=N)
        traj[t] = float(N.mean()) / K
    return traj


def _final(traj, frac=0.1):
    """Mean of the final `frac` of the trajectory (the plateau / floor), as a fraction of K."""
    return float(traj[-max(1, int(len(traj) * frac)):].mean())


def _auc(traj, dt=_PDT):
    """Cumulative malignant burden = area under the N(t)/K curve (time units)."""
    return float(traj.sum() * dt)


def _coarse_monotone(traj, rising=True, nb=10, tol=0.03):
    blk = max(1, len(traj) // nb)
    means = [float(traj[i:i + blk].mean()) for i in range(0, len(traj) - blk + 1, blk)]
    if rising:
        return all(means[i + 1] >= means[i] - tol for i in range(len(means) - 1))
    return all(means[i + 1] <= means[i] + tol for i in range(len(means) - 1))


def emergent_combination(gammas):
    g = gammas[_AML]
    f_cyto = _basin_fraction(g, "cytotoxic")              # ≈ 1 (survivors stay malignant)
    f_diff = _basin_fraction(g, "differentiation")        # ≈ 0 (basin emptied)
    seed0 = (1.0 - _KAPPA) * _K_POP                       # cytotoxic seed (0.1 K)

    # ---- five arms ----------------------------------------------------------------------------------
    cyto      = _regrowth(seed0,   f_cyto, mu_surv=0.0,          seed=SEED)        # 1 cytotoxic alone
    diff      = _regrowth(_K_POP,  f_diff, mu_surv=0.0,          seed=SEED + 1)    # 2 differentiation alone
    cyto_diff = _regrowth(seed0,   f_diff, mu_surv=0.0,          seed=SEED + 2)    # 3 cytotoxic + differentiation
    surv      = _regrowth(_K_POP,  f_cyto, mu_surv=_MU_RESTORED, seed=SEED + 3)    # 4 surveillance alone (restored)
    cyto_surv = _regrowth(seed0,   f_cyto, mu_surv=_MU_RESTORED, seed=SEED + 4)    # 5 cytotoxic + surveillance

    arms = dict(
        cytotoxic_alone        = dict(final=round(_final(cyto), 3),      auc=round(_auc(cyto), 3),
                                      traj=[round(float(cyto[i]), 3) for i in range(0, len(cyto), max(1, len(cyto)//10))]),
        differentiation_alone  = dict(final=round(_final(diff), 3),      auc=round(_auc(diff), 3),
                                      traj=[round(float(diff[i]), 3) for i in range(0, len(diff), max(1, len(diff)//10))]),
        cytotoxic_plus_diff    = dict(final=round(_final(cyto_diff), 3), auc=round(_auc(cyto_diff), 3),
                                      traj=[round(float(cyto_diff[i]), 3) for i in range(0, len(cyto_diff), max(1, len(cyto_diff)//10))]),
        surveillance_alone     = dict(final=round(_final(surv), 3),      auc=round(_auc(surv), 3),
                                      traj=[round(float(surv[i]), 3) for i in range(0, len(surv), max(1, len(surv)//10))]),
        cytotoxic_plus_surv    = dict(final=round(_final(cyto_surv), 3), auc=round(_auc(cyto_surv), 3),
                                      traj=[round(float(cyto_surv[i]), 3) for i in range(0, len(cyto_surv), max(1, len(cyto_surv)//10))]),
    )

    cytotoxic_alone_relapses = bool(arms["cytotoxic_alone"]["final"] >= 0.90 and _coarse_monotone(cyto, rising=True))
    diff_combo_cures = bool(arms["cytotoxic_plus_diff"]["final"] <= 0.10 and _coarse_monotone(cyto_diff, rising=False))
    surv_combo_cures = bool(arms["cytotoxic_plus_surv"]["final"] <= 0.10 and _coarse_monotone(cyto_surv, rising=False))
    relapse_to_cure_conversion = bool(cytotoxic_alone_relapses and diff_combo_cures and surv_combo_cures)

    # the cull ACCELERATES: combination clears with lower cumulative burden than the basin/niche lever alone
    cull_lowers_burden_diff = bool(arms["cytotoxic_plus_diff"]["auc"] < arms["differentiation_alone"]["auc"] - 1e-9)
    cull_lowers_burden_surv = bool(arms["cytotoxic_plus_surv"]["auc"] < arms["surveillance_alone"]["auc"] - 1e-9)
    cull_accelerates = bool(cull_lowers_burden_diff and cull_lowers_burden_surv)

    # the cull CANNOT cure alone -> the basin/niche lever is the necessary curative element (mirrors T17)
    cull_alone_insufficient = bool(cytotoxic_alone_relapses)

    # ---- surveillance threshold sweep (emergent threshold at mu_surv = r) ----------------------------
    sweep = []
    for k, mu in enumerate(_MU_SWEEP):
        tr = _regrowth(_K_POP, f_cyto, mu_surv=mu, seed=SEED + 20 + k)
        sweep.append(dict(mu_surv=round(mu, 3), growth_rate_r=round(_R_GROW, 3),
                          final_fraction=round(_final(tr), 3),
                          cures=bool(_final(tr) <= 0.10)))
    finals = [s["final_fraction"] for s in sweep]
    surv_threshold_monotone = all(finals[i + 1] <= finals[i] + 1e-9 for i in range(len(finals) - 1))
    surv_cures_when_restored = bool(sweep[-1]["cures"] and not sweep[0]["cures"])
    surveillance_threshold = bool(surv_threshold_monotone and surv_cures_when_restored)

    ok = bool(relapse_to_cure_conversion and cull_accelerates and cull_alone_insufficient and surveillance_threshold)
    return dict(
        site="acute myeloid leukemia (marrow R19 switch)", gamma=round(g, 6),
        measured_basin_fraction=dict(cytotoxic_survivors_ON=round(f_cyto, 3),
                                     differentiation_residual_ON=round(f_diff, 3)),
        carrying_capacity_K=_K_POP, kill_fraction=_KAPPA, restored_surveillance_mu=_MU_RESTORED,
        arms=arms,
        cytotoxic_alone_relapses=bool(cytotoxic_alone_relapses),
        differentiation_combo_cures=bool(diff_combo_cures),
        surveillance_combo_cures=bool(surv_combo_cures),
        relapse_to_cure_conversion=bool(relapse_to_cure_conversion),
        cull_lowers_burden_diff=bool(cull_lowers_burden_diff),
        cull_lowers_burden_surv=bool(cull_lowers_burden_surv),
        cull_accelerates=bool(cull_accelerates),
        cull_alone_insufficient=bool(cull_alone_insufficient),
        surveillance_threshold_sweep=sweep,
        surveillance_threshold=bool(surveillance_threshold),
        all_pass=ok,
        grade="[V] combination therapy EMERGES as a measured basin-gated regrowth conversion: a cytotoxic cull "
              "that relapses ALONE (≥90% K) is converted to a cure (≤10% K) when combined with either basin/niche "
              "lever (differentiation re-flip or restored surveillance), the cull lowering the cumulative burden "
              "(smaller area under N(t)/K) while being unable to cure on its own, and the surveillance channel "
              "shows an emergent threshold at the growth rate (sub-threshold relapses to an interior fixed point, "
              "restored surveillance cures) — measured, not assumed; [O] absolute growth/conversion/clearance "
              "rates and clinical schedule")


def run(gammas):
    """T19: emergent combination-therapy contrast — relapse→cure conversion MEASURED as a basin-gated trajectory."""
    r = emergent_combination(gammas)
    return dict(T19=dict(target="T19",
                         claim="combination therapy EMERGES as a measured basin-gated regrowth conversion: a "
                               "cytotoxic cull that relapses ALONE (≥90% K) is converted to a cure (≤10% K) when "
                               "combined with either basin/niche lever (differentiation re-flip or restored "
                               "surveillance) — the cull lowers the cumulative burden while being unable to cure "
                               "alone, and the surveillance channel shows an emergent threshold at the growth rate "
                               "(restored = above it) — measured, not assumed; absolute rates / schedule stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T19"]["result"]
    print("COMBINATION THERAPY — relapse→cure conversion (AML marrow switch, γ=%.4f):" % r["gamma"])
    print("measured basin fraction: cytotoxic survivors ON=%.3f | differentiation residual ON=%.3f"
          % (r["measured_basin_fraction"]["cytotoxic_survivors_ON"], r["measured_basin_fraction"]["differentiation_residual_ON"]))
    print("\narm                       final(N/K)   cumulative_burden(AUC)")
    order = ["cytotoxic_alone", "differentiation_alone", "cytotoxic_plus_diff", "surveillance_alone", "cytotoxic_plus_surv"]
    for a in order:
        print("  %-24s   %.3f          %.3f" % (a, r["arms"][a]["final"], r["arms"][a]["auc"]))
    print("\ncytotoxic alone relapses:        ", r["cytotoxic_alone_relapses"])
    print("cyto+differentiation cures:      ", r["differentiation_combo_cures"])
    print("cyto+surveillance cures:         ", r["surveillance_combo_cures"])
    print("=> relapse→cure conversion:      ", r["relapse_to_cure_conversion"])
    print("cull lowers burden (diff/surv):  ", r["cull_lowers_burden_diff"], "/", r["cull_lowers_burden_surv"], "-> accelerates:", r["cull_accelerates"])
    print("cull alone insufficient:         ", r["cull_alone_insufficient"])
    print("\nsurveillance threshold sweep (threshold at growth rate r=%.1f):" % _R_GROW)
    print("  mu_surv   final_fraction   cures")
    for s in r["surveillance_threshold_sweep"]:
        print("   %.2f       %.3f          %s" % (s["mu_surv"], s["final_fraction"], s["cures"]))
    print("surveillance threshold (monotone + restored cures):", r["surveillance_threshold"])
    print("\nT19 all_pass:", r["all_pass"])
