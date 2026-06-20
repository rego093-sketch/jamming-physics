#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fundamental_targets.py  --  fundamental vs symptomatic treatment, derived from the loop/basin structure.

The CHARTER asks for "more fundamental treatment" of the major diseases. The loop structure makes a
SHARP, FALSIFIABLE distinction that the visible-mechanism view misses, and it MATCHES the clinical
evidence base in both directions:

  HYPERTENSION (an integral-controller setpoint RESET, RP4):
    * an OPERATING-POINT therapy lowers the pressure without moving the renal reference -> the integral
      controller treats it as a constant disturbance and REJECTS it back toward the (high) reference
      -> benefit is not durable (tolerance/escape; lifelong dosing; vasodilator monotherapy fails
      without a volume/renal arm). [symptomatic]
    * a REFERENCE-RESET therapy lowers the renal pressure-natriuresis reference itself
      (renal denervation; sustained Na+/weight reduction; RAAS blockade; baroreflex activation)
      -> the defended pressure falls DURABLY. [fundamental]
    Prediction (direction [V]): durability of BP reduction tracks how much the therapy resets the
    renal reference, not how much it pushes the operating point. Matches: the diuretic/renal backbone
    of effective regimens, and renal denervation's durable, time-INCREASING effect
    (GSR-DEFINE office SBP ~ -20.5 mmHg at 3 yr) [L]; absolute effect sizes [O].

  CHRONIC HEART FAILURE (an R19 basin COLLAPSE, RP5; operative variable = barrier margin
  M = spinodal(kappa) - |load|, with a maladaptive neurohormonal cycle that RAISES load as output falls):
    * an EFFECTOR-FLOGGING therapy (positive inotrope) raises contractility drive briefly but raises
      O2 demand / wall stress and does NOT break the cycle -> the margin M SHRINKS over time
      -> accelerated collapse, even though acute hemodynamics improve. [symptomatic/harmful]
      Matches PROMISE: oral milrinone +28% mortality despite better hemodynamics (Packer 1991) [L].
    * a LOAD-REDUCING + CYCLE-BREAKING therapy (afterload/preload reduction + neurohormonal blockade)
      lowers load and damps the maladaptive gain -> the margin M GROWS -> the high-output basin is
      restored. [fundamental] Matches the four pillars (ARNI -16% all-cause mortality vs enalapril,
      PARADIGM-HF; beta-blockers; MRAs; SGLT2i, NNT ~19-21, DAPA-HF/EMPEROR-Reduced) [L]; absolute [O].
    The SGLT2i arm connects to the macula-densa sensory cell (raised NaCl delivery -> TGF -> diuresis/
    unload), tying the slow-loop sensor to a basin-restoring therapy.

GRADES (C3): the DIRECTION of each prediction (opposed-back vs durable; margin-shrinks vs margin-grows)
= [V]; the cited clinical durability / mortality direction = [L]; ABSOLUTE effect sizes = [O].
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__).replace("_therapy", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, settle, seed_everything
import vp_hmd_loops as L


# ===========================================================================
#  HYPERTENSION -- operating-point (symptomatic) vs reference-reset (fundamental)
# ===========================================================================
def hypertension_therapies(reset_up=20.0, op_drug=15.0, ref_reset=17.0):
    """On a hypertensive controller (renal reference reset UP by reset_up):
        A) operating-point drug  -> lowers P transiently, opposed back to the high reference;
        B) reference reset (e.g. denervation/Na-weight/RAAS) -> durable lower defended P."""
    seed_everything()
    _, p_normal, _ = L.kidney_integrator(dPset=0.0)
    _, p_hyper, _ = L.kidney_integrator(dPset=reset_up)

    # A) operating-point push: nadir then opposed back; withdraw -> returns to high reference
    trA, pA_steady, _ = L.kidney_integrator(dPset=reset_up, drug_mmHg=op_drug, drug_at_s=20.0)
    pA_nadir = float(np.min(trA))
    # withdrawal: apply for the first half, then remove -> must climb back to the high reference
    trAw, pAw_steady, _ = L.kidney_integrator(dPset=reset_up, drug_mmHg=op_drug, drug_at_s=20.0, T=200.0)
    # B) reference reset: lower the renal reference itself -> durable
    _, pB_steady, _ = L.kidney_integrator(dPset=reset_up - ref_reset)

    return dict(
        defended_P_normal=round(p_normal, 4), defended_P_hypertensive=round(p_hyper, 4),
        operating_point_drug=dict(
            nadir_mmHg=round(pA_nadir, 4), steady_mmHg=round(pA_steady, 4),
            transient_drop_mmHg=round(p_hyper - pA_nadir, 4),
            durable_drop_mmHg=round(p_hyper - pA_steady, 4),
            opposed_back=bool(pA_steady > p_normal + 5.0),
            verdict="symptomatic: rejected back toward the high reference; not durable alone"),
        reference_reset=dict(
            steady_mmHg=round(pB_steady, 4),
            durable_drop_mmHg=round(p_hyper - pB_steady, 4),
            durable=bool(pB_steady < p_hyper - 5.0),
            verdict="fundamental: moves the defended pressure DOWN and holds"),
        prediction="durability of BP reduction tracks RENAL-REFERENCE reset, not operating-point push",
        direction_grade="[V]", clinical_durability_grade="[L]", absolute_effect_grade="[O]",
        anchors="renal denervation durable & time-increasing (GSR-DEFINE ~ -20.5 mmHg @3yr; FDA-approved 2023); diuretic/renal backbone required for durable control [L]")


# ===========================================================================
#  HEART FAILURE -- effector-flog (symptomatic/harmful) vs load-reduce + cycle-break (fundamental)
#  operative variable: barrier margin M = spinodal(kappa) - |L_eff|, with a maladaptive cycle
#  L_eff = L0 + beta * max(0, s_tgt - s)  (load rises as output s falls).
# ===========================================================================
def hf_state(kappa, L0, beta, s_tgt=1.0, dkappa=0.0, dL=0.0, dbeta=0.0, iters=60):
    """Self-consistent operating state with the neurohormonal cycle. Returns the converged output s
    (high basin ~ +sqrt(kappa); collapsed ~ negative), the effective load, the barrier margin, and
    whether the high-output basin still holds."""
    k = max(kappa + dkappa, 1e-6)
    b = max(beta + dbeta, 0.0)
    s = math.sqrt(k)                                  # start in the high-output basin
    for _ in range(iters):
        Leff = max(L0 + dL + b * max(0.0, s_tgt - s), 0.0)
        s = settle(k, -Leff, s0=s)
    Leff = max(L0 + dL + b * max(0.0, s_tgt - s), 0.0)
    M = float(spinodal(k) - abs(Leff))
    return dict(kappa=round(k, 4), output=round(float(s), 6), load=round(float(Leff), 6),
                margin=round(M, 6), high_output_basin=bool(s > 0.0 and M > 0.0))


def heart_failure_therapies():
    """Compare a fragile compensated HF state under: inotrope (flog) vs load-reduce + cycle-break."""
    seed_everything()
    kappa0, L0, beta0 = 1.85, 0.55, 0.45             # compensated but fragile (small positive margin)
    base = hf_state(kappa0, L0, beta0)
    # inotrope: contractility drive up, but O2 demand / wall stress raises load and cycle not broken
    inotrope = hf_state(kappa0, L0, beta0, dkappa=+0.20, dL=+0.30)
    # load-reduce + cycle-break: afterload/preload down + neurohormonal blockade damps the cycle
    blockade = hf_state(kappa0, L0, beta0, dL=-0.18, dbeta=-0.30)
    return dict(
        baseline=base,
        inotrope_flog=dict(**inotrope,
            d_margin=round(inotrope["margin"] - base["margin"], 6),
            margin_shrinks=bool(inotrope["margin"] < base["margin"]),
            verdict="symptomatic/harmful: acute output up but margin shrinks -> accelerated collapse"),
        load_reduce_cycle_break=dict(**blockade,
            d_margin=round(blockade["margin"] - base["margin"], 6),
            margin_grows=bool(blockade["margin"] > base["margin"]),
            verdict="fundamental: margin grows -> high-output basin restored"),
        prediction="mortality benefit tracks margin (load reduction + cycle interruption); effector flogging shrinks the margin",
        sensory_link="SGLT2i arm acts via macula-densa NaCl delivery -> TGF -> diuresis/unload (slow-loop sensor -> basin-restoring therapy)",
        direction_grade="[V]", clinical_mortality_grade="[L]", absolute_grade="[O]",
        anchors="PROMISE milrinone +28% mortality despite better hemodynamics (Packer 1991); four pillars mortality benefit ARNI/BB/MRA/SGLT2i (PARADIGM-HF, CIBIS-II/MERIT-HF, RALES/EMPHASIS, DAPA-HF/EMPEROR-Reduced) [L]")


def status():
    return dict(
        hypertension=hypertension_therapies(),
        heart_failure=heart_failure_therapies(),
        principle="treat the SETPOINT/BASIN (reference reset; load reduction + cycle interruption), not the operating point / effector")


if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
