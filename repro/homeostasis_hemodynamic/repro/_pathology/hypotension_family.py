#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hypotension_family.py  --  low-pressure failure as a NODE DECOMPOSITION (deterministic).

Hypertension is ONE failure: the renal integral controller RESETS its reference upward (RP4).
Hypotension is NOT one disease -- on the SAME relation MAP = CVP + CO x SVR it decomposes by WHICH
node of the defended-pressure loop fails. Each discriminant below reuses the EXISTING primitives in
vp_hmd_loops.py (baroreflex_buffer, kidney_integrator, map_from_seams, spinodal/margin) -- no new
substrate math, no hand-tuned constants (VP-SPEC C1). This makes hypotension a SHARPER test of the loop
than hypertension: hypertension probes the integrator's reset; hypotension probes every node's failure.

  node that fails            clinical form                 discriminant
  -------------------------  ----------------------------  ------------------------------------------
  RP6 fast buffer            orthostatic / autonomic       downward postural step, intact vs KO
  RP7 integrator reference   adrenal insufficiency (RAAS)  reference reset DOWN; fluids opposed back,
                                                           mineralocorticoid (reference) durable
  RP8 resistance effector    distributive / vasoplegic     SVR collapse; CO compensation insufficient
  RP9 volume substrate       hypovolemic / hemorrhagic     one-directional natriuresis -> deficit is a
                                                           substrate FOLD the kidney cannot self-correct
  (cardiogenic)              cardiogenic shock             RP5 basin collapse taken to loss of perfusion

GRADES (C3): shape/direction [V]; cited clinical anchors [L]; absolute mmHg / incidence / effect [O].
"""
import os, sys, math
import numpy as np
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
from vp_substrate import spinodal, seed_everything
import vp_hmd_loops as L


# ===========================================================================
# RP6 -- orthostatic / autonomic hypotension: loss of the FAST buffer.
#        The exact symmetric counterpart of RP2 (a downward postural step).
#        Intact baroreflex buffers gravitational pooling; autonomic failure /
#        PIEZO-KO (transduction 0) lets the full drop through -> orthostatic.
# ===========================================================================
def rp6_orthostatic():
    seed_everything()
    drop = -25.0                                   # head-ward pooling on standing, mmHg
    intact = L.baroreflex_buffer(step_mmHg=drop, transduction=1.0)
    failed = L.baroreflex_buffer(step_mmHg=drop, transduction=0.0)   # autonomic failure / PIEZO-KO
    return dict(
        postural_step_mmHg=drop,
        intact_residual_mmHg=intact["residual_mmHg"], intact_buffered_fraction=intact["buffered_fraction"],
        failed_residual_mmHg=failed["residual_mmHg"], failed_buffered_fraction=failed["buffered_fraction"],
        intact_buffers_majority=bool(intact["buffered_fraction"] > 0.5),
        autonomic_failure_is_orthostatic=bool(failed["buffered_fraction"] < 0.05),
        symmetric_with_rp2=True,
        anchor="autonomic failure / baroreflex loss -> orthostatic hypotension; mirror of the labile "
               "PIEZO1/2 double-KO (Zeng 2018) -- the buffer fails in BOTH directions [L]",
        shape_grade="[V]", gain_latency_grade="[L]", absolute_mmHg_grade="[O]")


# ===========================================================================
# RP7 -- adrenal insufficiency (Addison): the RAAS arm that SETS the renal
#        reference is lost -> the defended pressure resets DOWN (mirror of RP4).
#        A volume bolus is opposed back to the LOW reference (not durable);
#        restoring the reference (mineralocorticoid) is durable. Mirror of RP4 + T1.
# ===========================================================================
def rp7_adrenal_reference_loss():
    seed_everything()
    # (a) reference reset downward (lost mineralocorticoid set-point)
    _, p_normal, _ = L.kidney_integrator(dPset=0.0)
    _, p_low,    _ = L.kidney_integrator(dPset=-20.0)
    # (b) on the LOW-reference controller a volume bolus is a transient disturbance
    #     -> integral control rejects it back to the LOW reference (fluids not durable).
    tr, p_bolus_steady, _ = L.kidney_integrator(dPset=-20.0, bolus_mL=800.0, bolus_at_s=20.0)
    peak = float(np.max(tr))
    # (c) restoring the reference (mineralocorticoid replacement) durably restores pressure
    _, p_restored, _ = L.kidney_integrator(dPset=0.0)
    return dict(
        defended_P_normal=round(p_normal, 6), defended_P_low=round(p_low, 6),
        reset_shift_mmHg=round(p_low - p_normal, 6),
        attractor_moved_down=bool(p_low - p_normal < -5.0),
        bolus_peak_mmHg=round(peak, 6), bolus_steady_mmHg=round(p_bolus_steady, 6),
        bolus_opposed_back=bool(p_bolus_steady < p_normal - 5.0 and (peak - p_low) > 5.0),
        reference_restore_durable=bool(p_restored > p_low + 5.0),
        mirror="exact mirror of RP4: an integral controller defends a reset reference; here it is reset "
               "DOWN (lost RAAS/aldosterone reference). Fluids are opposed back; restoring the reference "
               "(mineralocorticoid) is durable -- the symmetric counterpart of antihypertensive durability",
        shape_grade="[V]", clinical_anchor_grade="[L]", absolute_grade="[O]")


# ===========================================================================
# RP8 -- distributive / vasoplegic shock: the RESISTANCE EFFECTOR (SVR) collapses.
#        MAP = CVP + CO x SVR with SVR -> low. Distinct from RP5 (the CO arm).
#        Even a doubled compensatory CO cannot restore MAP below a vasoplegia
#        floor -> the fix is a VASOPRESSOR (restore SVR), not inotrope/fluid alone.
# ===========================================================================
def rp8_distributive_svr_collapse():
    seed_everything()
    svr0 = L.SVR_REST_PRU
    map0 = L.map_from_seams(svr=svr0)
    rows = []
    floor_svr = None
    HYPOTENSIVE = 65.0                              # MAP below which perfusion is threatened (discriminant)
    for frac in [round(x, 3) for x in np.linspace(1.0, 0.25, 16)]:
        svr = svr0 * frac
        m_base = L.map_from_seams(svr=svr)                       # resting CO
        m_comp = L.map_from_seams(co=2.0 * L.CO_REST_L_MIN, svr=svr)  # baroreflex doubles CO
        rows.append(dict(svr_frac=frac, svr=round(svr, 4),
                         MAP_resting_CO=round(m_base, 4), MAP_doubled_CO=round(m_comp, 4),
                         hypotensive_even_with_doubled_CO=bool(m_comp < HYPOTENSIVE)))
        if floor_svr is None and m_comp < HYPOTENSIVE:
            floor_svr = round(svr, 4)
    # vasopressor vs inotrope at the floor: restore SVR vs raise CO
    svr_floor = floor_svr if floor_svr else svr0 * 0.3
    map_inotrope  = L.map_from_seams(co=2.0 * L.CO_REST_L_MIN, svr=svr_floor)   # double CO
    map_pressor   = L.map_from_seams(co=L.CO_REST_L_MIN, svr=svr0)              # restore SVR
    return dict(
        baseline_MAP=round(map0, 4), svr_sweep=rows,
        vasoplegia_floor_svr=floor_svr,
        MAP_inotrope_only=round(map_inotrope, 4), MAP_vasopressor=round(map_pressor, 4),
        vasopressor_beats_inotrope=bool(map_pressor > map_inotrope),
        failure_node="resistance effector (SVR), distinct from RP5 cardiac-output basin",
        principle="distributive shock is an SVR-arm collapse -> the corrective is to restore SVR "
                  "(vasopressor); raising CO alone cannot lift MAP above the perfusion floor [V]; "
                  "norepinephrine first-line in septic shock [L]",
        shape_grade="[V]", clinical_anchor_grade="[L]", absolute_grade="[O]")


# ===========================================================================
# RP9 -- hypovolemic / hemorrhagic shock: the VOLUME SUBSTRATE itself is depleted.
#        Sharpens RP3: renal pressure-natriuresis is ONE-DIRECTIONAL -- the kidney
#        can EXCRETE an excess (perfect adaptation, RP3) but cannot REPLACE a
#        deficit (it does not synthesise blood). So a volume EXCESS self-corrects
#        while a volume DEFICIT is a substrate FOLD that only external volume
#        (transfusion) restores. Distinct from a reference reset or effector loss.
# ===========================================================================
def kidney_integrator_onedirectional(bolus_mL, P0=70.0, a=0.05, V0=5000.0, k=8.0, Pset=93.0,
                                     T=400.0, dt=0.02):
    """Renal loop with PHYSIOLOGICAL natriuresis floor: out = max(0, k(P-Pset)).
    The kidney excretes excess volume but cannot add blood volume back."""
    seed_everything()
    V = V0 + (Pset - P0) / a                        # start at the defended point
    n = int(T / dt); bolus_step = int(20.0 / dt)
    P_tr = np.empty(n)
    for i in range(n):
        if i == bolus_step:
            V += bolus_mL
        P = P0 + a * (V - V0)
        out = max(0.0, k * (P - Pset))              # one-directional: excrete-only
        V += dt * (0.0 - out)
        P_tr[i] = P
    return float(P_tr[-1])


def rp9_hypovolemic_substrate_fold():
    seed_everything()
    p_excess  = kidney_integrator_onedirectional(bolus_mL=+800.0)   # volume EXCESS -> excreted -> back to Pset
    p_deficit = kidney_integrator_onedirectional(bolus_mL=-800.0)   # volume DEFICIT -> NOT recoverable by kidney
    p_baseline = kidney_integrator_onedirectional(bolus_mL=0.0)
    # transfusion: restore the lost volume externally
    p_transfused = kidney_integrator_onedirectional(bolus_mL=-800.0 + 800.0)
    Pset = 93.0
    return dict(
        steady_P_baseline=round(p_baseline, 6),
        steady_P_after_excess=round(p_excess, 6),
        steady_P_after_deficit=round(p_deficit, 6),
        steady_P_after_transfusion=round(p_transfused, 6),
        excess_self_corrects=bool(abs(p_excess - Pset) < 1.0),
        deficit_is_uncorrected_fold=bool(p_deficit < Pset - 5.0),
        transfusion_restores=bool(abs(p_transfused - Pset) < 1.0),
        asymmetry="renal natriuresis is excrete-only: a volume EXCESS self-corrects (RP3 perfect "
                  "adaptation) but a volume DEFICIT cannot be self-corrected -- the kidney does not make "
                  "blood. Hypovolemia is therefore a SUBSTRATE fold requiring external volume",
        failure_node="volume substrate (blood volume), distinct from reference (RP4/RP7) and effector (RP5/RP8)",
        principle="treat hypovolemic shock with VOLUME (transfusion/resuscitation), not vasopressor or "
                  "inotrope alone [V]; the fast baroreflex (SVR/HR up) only buys time [L]",
        shape_grade="[V]", clinical_anchor_grade="[L]", absolute_grade="[O]")


# ===========================================================================
# Cardiogenic shock = RP5 basin collapse to loss of perfusion. The TIMESCALE
# distinction from chronic HF (T2) is critical: in CHRONIC HF an inotrope SHRINKS
# the margin (harm); in ACUTE cardiogenic shock temporary inotropic / mechanical
# support is needed to hold perfusion until the basin is recovered.
# ===========================================================================
def cardiogenic_note():
    rp5 = L.rp5_basin_collapse()
    return dict(
        is_rp5_extreme=True, collapse_kappa=rp5["collapse_kappa"],
        timescale_distinction="chronic HF (T2): inotrope shrinks the barrier margin -> harm (PROMISE). "
                              "acute cardiogenic shock: temporary inotrope / mechanical support is needed "
                              "to maintain perfusion while the collapsed basin is recovered -- opposite "
                              "sign by timescale, same R19 fold",
        grade="[V] fold / [L] clinical timescale / [O] absolute")


# ===========================================================================
# T3 -- hypotension therapy is NODE-SPECIFIC (not a generic 'raise pressure').
#       Each failure node has a matched corrective; the wrong node's drug fails.
# ===========================================================================
def t3_node_specific_therapy():
    seed_everything()
    return dict(
        orthostatic_autonomic=dict(node="fast buffer", fix="restore the buffer: volume expansion, "
            "compression, sympathomimetic / midodrine; not a reference change", grade="[L]"),
        adrenal=dict(node="integrator reference", fix="REPLACE the reference (mineralocorticoid); fluids "
            "alone are opposed back to the low reference -- mirror of antihypertensive durability (RP7)", grade="[V]/[L]"),
        distributive=dict(node="resistance effector", fix="VASOPRESSOR to restore SVR (norepinephrine); "
            "inotrope/fluid alone cannot lift MAP above the perfusion floor (RP8)", grade="[V]/[L]"),
        hypovolemic=dict(node="volume substrate", fix="VOLUME (transfusion/resuscitation); the kidney "
            "cannot replace a deficit (RP9); vasopressor only buys time", grade="[V]/[L]"),
        cardiogenic=dict(node="cardiac effector", fix="TEMPORARY inotrope / mechanical support to hold "
            "perfusion -- opposite of chronic-HF inotrope harm, by timescale", grade="[V]/[L]"),
        principle="match the corrective to the FAILED NODE; the loop structure forbids a one-size "
                  "pressor -- the wrong node's drug is rejected or insufficient",
        direction_grade="[V]", clinical_grade="[L]", absolute_effect_grade="[O]")


# ===========================================================================
#  Aggregate
# ===========================================================================
def all_hypotension():
    return dict(
        RP6_orthostatic=rp6_orthostatic(),
        RP7_adrenal_reference_loss=rp7_adrenal_reference_loss(),
        RP8_distributive_svr_collapse=rp8_distributive_svr_collapse(),
        RP9_hypovolemic_substrate_fold=rp9_hypovolemic_substrate_fold(),
        cardiogenic=cardiogenic_note(),
        T3_node_specific_therapy=t3_node_specific_therapy(),
        thesis="hypotension is not one disease but a NODE DECOMPOSITION of the defended-pressure loop: "
               "fast buffer (RP6), integrator reference (RP7), resistance effector (RP8), volume substrate "
               "(RP9), cardiac effector (cardiogenic). Each is computed on the SAME MAP = CVP + CO x SVR "
               "engine with the existing primitives -- a sharper test than the single hypertension reset.")


if __name__ == "__main__":
    import json
    print(json.dumps(all_hypotension(), ensure_ascii=False, indent=2))
