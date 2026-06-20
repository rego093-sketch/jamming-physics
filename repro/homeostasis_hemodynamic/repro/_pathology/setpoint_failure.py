#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setpoint_failure.py  --  Hemodynamic Homeostasis PATHOLOGY module (v0.2.0-research).

Disease here is NOT a local lesion; it is a FAILURE of a defended setpoint -- a setpoint DRIFT/RESET or
an attractor COLLAPSE of the coupled homeostatic loop, on the same R19 substrate as the rest of the
framework: a healthy setpoint is a regulated attractor; disease = the loop resettling at a reset
reference, or the high-output basin annihilating.

This version replaces the earlier placeholder with the LAWS actually derived in the closed-loop module
(repro/_engine/vp_hmd_loops.py):

  essential hypertension  -- INTEGRAL-CONTROLLER RESET.  With a renal pressure-natriuresis integral
    controller, the defended pressure equals the reference: P* = P0 + dPset. A reset of the renal
    reference by dPset shifts the defended attractor by EXACTLY dPset, and any operating-point push is
    rejected back to P* (static rejection is total -- Guyton "infinite gain"). Law + check below (RP4).

  chronic heart failure  -- SADDLE-NODE BASIN COLLAPSE.  The cardiac operating point sits in the R19
    field with g = contractility kappa (barrier kappa^2/4) and h = -load. The high-output fixed point
    exists iff spinodal(kappa) > |load|; it ANNIHILATES at the threshold kappa* solving
    spinodal(kappa*) = |load_eff| (a saddle-node fold), NOT a reset. Law + check below (RP5).

GRADES (C3): the reset/collapse SHAPE = [V]; cited risk/progression anchor = [L]; ABSOLUTE
incidence/rate = [O] with a STATED obstacle (external calibration). No silent claims.

Composition with disease_wp: a MONOGENIC lesion enters as a loop PARAMETER (cited by disease_wp) and
the systemic trajectory is computed here; polygenic/acquired disease (essential hypertension, chronic
HF) lives here as loop dysregulation.
"""
import os, sys, json, math
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
import importlib
from vp_substrate import barrier, spinodal, settle
LOOPS = importlib.import_module("vp_hmd_loops")

FAILURES = [{'site': 'essential hypertension',
  'mechanism': 'renal pressure-natriuresis reference resets RIGHTWARD -> integral controller defends a higher pressure',
  'class': 'setpoint reset (attractor shift)',
  'anchor': 'RR vs cited risk (Na, BMI cohorts) [L]; setpoint-reset shape [V]; absolute incidence [O]'},
 {'site': 'chronic heart failure',
  'mechanism': 'contractility/load cross a saddle-node -> the cardiac high-output basin annihilates',
  'class': 'basin collapse (fold)',
  'anchor': 'progression vs cited markers [L]; collapse dynamics [V]; absolute rate [O]'}]


def hypertension_reset_law(dPset=20.0, op_drug=15.0):
    """Defended pressure under an integral controller = reference; a reset shifts it by EXACTLY dPset,
    and an operating-point drug is opposed back. Computed from the loop module (RP4)."""
    _, p_normal, _ = LOOPS.kidney_integrator(dPset=0.0)
    _, p_reset, _ = LOOPS.kidney_integrator(dPset=dPset)
    tr, p_drug_steady, _ = LOOPS.kidney_integrator(dPset=dPset, drug_mmHg=op_drug, drug_at_s=20.0)
    shift = p_reset - p_normal
    return dict(
        law="P_defended = P0 + dPset  (integral controller defends the reference; static rejection total)",
        defended_normal_mmHg=round(float(p_normal), 4),
        defended_reset_mmHg=round(float(p_reset), 4),
        predicted_shift_mmHg=round(float(dPset), 4),
        observed_shift_mmHg=round(float(shift), 4),
        shift_matches_reference=bool(abs(shift - dPset) < 1e-6),
        operating_point_drug_steady_mmHg=round(float(p_drug_steady), 4),
        opposed_back=bool(p_drug_steady > p_normal + 5.0),
        grade="[V] reset shape / [L] risk anchor / [O] absolute incidence")


def hf_collapse_law(load=0.8, kappa_hi=2.2, kappa_lo=0.6, steps=17):
    """High-output fixed point exists iff spinodal(kappa) > |load|; the saddle-node is at kappa* solving
    spinodal(kappa*) = |load|. Locate kappa* by the sweep and by the closed form, and confirm they agree.
    spinodal(kappa) = 2*(kappa/3)^1.5, so kappa* = 3*(|load|/2)^(2/3)."""
    L = abs(load)
    kappa_star_closed = 3.0 * (L / 2.0) ** (2.0 / 3.0)
    # sweep to find where the high-output basin is lost
    ks = [kappa_hi + (kappa_lo - kappa_hi) * i / (steps - 1) for i in range(steps)]
    lost_at = None
    for k in ks:
        s = settle(k, -L, s0=math.sqrt(max(k, 1e-9)))
        margin = spinodal(k) - L
        if not (s > 0.0 and margin > 0.0):
            lost_at = k; break
    return dict(
        law="high-output basin exists iff spinodal(kappa) > |load|; saddle-node at spinodal(kappa*) = |load|",
        load=round(float(L), 4),
        kappa_star_closed_form=round(float(kappa_star_closed), 6),
        kappa_collapse_swept=(round(float(lost_at), 6) if lost_at is not None else None),
        closed_form_matches_sweep=bool(lost_at is not None and abs(lost_at - kappa_star_closed) <= (kappa_hi - kappa_lo) / (steps - 1) + 1e-9),
        is_fold_not_reset=True,
        grade="[V] fold shape / [L] progression marker / [O] absolute rate")


def status():
    return {"model": "R19 setpoint as regulated attractor; disease = setpoint reset (hypertension) or basin collapse (HF)",
            "failures": FAILURES,
            "hypertension_reset_law": hypertension_reset_law(),
            "hf_collapse_law": hf_collapse_law(),
            "grades": "reset/collapse shape [V] / cited anchor [L] / absolute incidence-rate [O] (state obstacle)",
            "disease_wp_composition": "monogenic lesion = parameter in (cited); systemic trajectory = computed here"}


if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
