#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPILEPSY -- OVER-SYNCHRONISATION (D10) : seizure as the over-synchronisation pole of
the engine's synchrony axis, made a PRIMARY module. Pathological hypersynchrony --
the defining electrophysiology of a seizure -- is ALREADY the engine's failure
mode: the autism chapters used "over-sync" as the ceiling the theta-cap must stay
below, and the schizophrenia disorganisation-extreme reproduced the limit where the
selective ignition gate collapses and EVERY candidate assembly fires at once. This
module turns that limit into the primary object and reads it as the seizure
mechanism: as the E/I balance shifts toward excitation, the global order parameter R
is driven UP toward total phase-lock, and past a critical point the selective
single-winner gate (M4) collapses -- loss of GATING, the ictal state.
=================================================================================
WHERE THIS SITS ON THE ATLAS AXIS. Autism-T is the UNDER pole (an inhibitory bias
RAISES the R19 fold -> under-ignition, R too LOW). Schizophrenia is an intermediate
fold-lowering (an excitatory bias lets SOME weak/irrelevant assemblies ignite ->
aberrant salience, partial over-recruitment). Epilepsy is the SAME synchrony axis
pushed to its ceiling: the excitatory bias drives R toward global lock and EVERY
candidate ignites -> total loss of selective gating. The four conditions order on
one axis:

   autism-T  (R under, under-ignition)
      <  HEALTH  (R selective: only genuinely-driven assemblies cross)
      <  schizophrenia  (R up, aberrant salience: some irrelevant cross)
      <  EPILEPSY  (R at the over-sync ceiling: ALL cross -- gate lost / ictal)

The over-sync ceiling is the SHARED structure of the atlas: it is the ceiling the
autism theta-cap must stay below (20-theta-cap-pacemaker, over-sync past inj~0.15),
the distance an anticonvulsant-class push enlarges, and the distance an excitatory
E/I shift closes. One ceiling, three clinical readings.

NOT a claim that idiopathic epilepsy is one mechanism. Real epilepsy is HETEROGENEOUS
-- focal vs generalised, with genetic channelopathies (SCN1A, KCNQ2, GABRG2),
structural, metabolic, autoimmune and idiopathic etiologies -- LOCKED. What is
asserted is the MECHANISM at the synchrony/gating level (an excitatory E/I shift
drives R to the over-sync ceiling and collapses the selective gate) and the SIGN of
seizure susceptibility (toward excitation lowers the threshold; an inhibitory /
threshold-raising push raises it). NOTHING is asserted about which individual, which
seizure type, or that any drug treats it.

THE ICTAL ONSET AS A TIME-COURSE IS OWED. This module characterises the STATIC
susceptibility -- the standing E/I state, the critical bias, and the sign of the two
operators. The ictal TRANSITION as a temporal event (a seizure starting and
spreading in time) requires a dynamic state-switching layer (E2: the R19 bistable
switch used OVER TIME, transitions between attractors) -- held OPEN [O] to a future
module. Here: the fault line, not the time-course of crossing it.

PRE-REGISTERED PREDICTIONS (DIRECTION/sign only; readout = HEALTH<->ictal contrast
and the reversal pattern; never magnitudes):
  EP1  over-sync axis: an excitatory/disinhibitory E/I bias drives the global order
       parameter R UP toward lock; R is monotone non-decreasing in excitation.
  EP2  ictal gate collapse: past a critical bias the selective gate collapses -- the
       number of co-igniting assemblies jumps to ALL (selectivity -> 0). The seizure
       threshold is that critical bias; the transition is a threshold, not gradual
       drift across the whole range.
  EP3  anticonvulsant sign: from an ictal bias, an inhibitory / threshold-RAISING
       operator (the GABAergic anticonvulsant-class direction) moves R DOWN away from
       lock and RESTORES selective gating -- it raises the seizure threshold. Sign
       only; efficacy=0.
  EP4  axis ordering: R_autism-T < R_health < R_sz < R_seizure, with autism-T under-
       ignited, health selective, SZ aberrant (some irrelevant), seizure all-ignited;
       and the over-sync ceiling = the theta-cap ceiling (cross-link to 20).

ANTI-TUNING. The signs are required to hold over a SWEEP of the E/I bias (R monotone
in excitation; selectivity monotone non-increasing in excitation) and a SWEEP of the
anticonvulsant strength (R monotone down, selectivity restored), not at a single
point. The bias grid and the operator strengths are stimulus/severity probes in the
exact D8/D9 mould, NOT constants fit to a target. No new constant: the effective-
coupling-vs-bias map is the same k = kappa/(1-|b|) [excit] / kappa/(1+|b|) [inhib]
used in the schizophrenia module, capped at 2*kappa as a guard.

NOT MEDICAL ADVICE. efficacy=0 everywhere; in-silico MECHANISM probe only. Loss of
the selective GATE is a mechanism boundary, NOT a claim about ictal subjective
experience (Axis-A firewall: consciousness_claim stays 0).

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-
ONLY (emerge_all is NOT touched, so the engine tree stays 0fbf4988... and the
M0..M16 subtree stays 3a1ebbbb..., byte-identical). Writes
epilepsy_oversync_results.json + its sha256, verified bit-for-bit.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

A      = E.load_brain_atlas()
REGS   = list(A["organs"].keys())
N      = len(REGS)
F0     = np.array([A["organs"][r]["f0_hz"] for r in REGS])
OMEGA  = 2 * math.pi * F0
OMEGA0 = float(np.mean(OMEGA))
KAP    = E.KAPPA_EPHAPTIC                                 # measured 0.5496
G      = 1.0
FOLD   = float(E.spinodal(G))                            # R19 fold = 0.3849

POS = E._measured_geometry(REGS)
_D = np.zeros((N, N))
for _i in range(N):
    for _j in range(N):
        _D[_i, _j] = np.linalg.norm(POS[_i] - POS[_j]) if _i != _j else 0.0


def _rawW():
    W = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                W[i, j] = 1.0 / (_D[i, j] ** 3)
    return W

def _rn(W):
    s = W.sum(axis=1, keepdims=True)
    return W / np.where(s > 0, s, 1.0)

# effective ephaptic coupling under an E/I bias (same map as the SZ module; no new
# constant): an EXCITATORY bias RAISES coupling (k = kappa/(1-|b|), toward lock),
# an INHIBITORY bias LOWERS it (k = kappa/(1+|b|)); capped at 2*kappa as a guard.
def _k_bias(bias):
    if bias >= 0:
        return min(KAP / (1.0 - min(bias, 0.95)), 2.0 * KAP)
    return KAP / (1.0 + abs(bias))

# candidate-assembly salience field (M3 eddies), straddling the fold in health
DRIVES = [0.12, 0.20, 0.28, 0.36, 0.50, 0.60]

def _on_set(bias):
    """Indices of candidate assemblies that ignite under the shared salience drives
    + tonic bias. Selectivity = which cross the R19 fold. Pure engine settle()."""
    on = []
    for i, d in enumerate(DRIVES):
        if E.settle(G, d + bias, s0=-math.sqrt(G)) > 0.0:
            on.append(i)
    return on


def run():
    Wrn = _rn(_rawW())
    R_health = E._integrate(OMEGA, Wrn, KAP * OMEGA0)[0]
    H = set(_on_set(0.0))
    n_health = len(H)

    # ===== EP1 : over-sync axis -- R rises toward lock with excitation =====
    bias_grid = [-0.20, -0.10, 0.0, 0.10, 0.20, 0.30, 0.50, 0.70, 0.90]
    R_curve = {round(b, 2): E._integrate(OMEGA, Wrn, _k_bias(b) * OMEGA0)[0] for b in bias_grid}
    bg = sorted(R_curve)
    R_monotone_up = all(R_curve[bg[i]] <= R_curve[bg[i + 1]] + 1e-9 for i in range(len(bg) - 1))
    R_ceiling = R_curve[bg[-1]]                      # R at the most-excitatory bias (toward lock)
    EP1 = bool(R_monotone_up and R_ceiling > R_health)

    # ===== EP2 : ictal gate collapse -- selectivity -> 0 past a critical bias =====
    sel_curve = {round(b, 2): len(_on_set(b)) for b in bias_grid}
    # selectivity (number igniting) is monotone NON-DECREASING in excitation
    sel_monotone = all(sel_curve[bg[i]] <= sel_curve[bg[i + 1]] for i in range(len(bg) - 1))
    # find the seizure threshold: the smallest bias at which ALL candidates ignite (gate lost)
    b_seiz = None
    for b in bg:
        if sel_curve[b] == len(DRIVES):
            b_seiz = b; break
    on_at_seiz = _on_set(b_seiz) if b_seiz is not None else _on_set(bg[-1])
    gate_collapsed = bool(len(on_at_seiz) == len(DRIVES))
    every_irrelevant_recruited = bool(len(set(on_at_seiz) - H) == len(DRIVES) - n_health)
    EP2 = bool(sel_monotone and gate_collapsed and every_irrelevant_recruited and b_seiz is not None)

    # ===== EP3 : anticonvulsant sign -- inhibitory push lowers R, restores gating =====
    B_ICTAL = b_seiz if b_seiz is not None else 0.50
    ACD_SWEEP = [0.10, 0.20, 0.35, 0.55]            # threshold-RAISING (inhibitory) strengths
    R_ictal = E._integrate(OMEGA, Wrn, _k_bias(B_ICTAL) * OMEGA0)[0]
    R_acd_curve = {round(a, 2): E._integrate(OMEGA, Wrn, _k_bias(B_ICTAL - a) * OMEGA0)[0] for a in ACD_SWEEP}
    sa = sorted(R_acd_curve)                          # weakest ACD first
    R_acd_monotone_down = all(R_acd_curve[sa[i]] >= R_acd_curve[sa[i + 1]] - 1e-9 for i in range(len(sa) - 1))
    sel_acd_curve = {round(a, 2): len(_on_set(B_ICTAL - a)) for a in ACD_SWEEP}
    selectivity_restored = bool(min(sel_acd_curve.values()) < len(DRIVES))   # gate no longer fully collapsed
    acd_lowers_R = bool(R_acd_curve[sa[-1]] < R_ictal - 1e-9)
    EP3 = bool(R_acd_monotone_down and selectivity_restored and acd_lowers_R)

    # ===== EP4 : axis ordering (autism-T < health < SZ < seizure) =====
    B_AUT = -0.10                                     # autism-T inhibitory pole (D8)
    B_SZ  = +0.15                                     # SZ excitatory pole (D9)
    R_aut = E._integrate(OMEGA, Wrn, _k_bias(B_AUT) * OMEGA0)[0]
    R_sz  = E._integrate(OMEGA, Wrn, _k_bias(B_SZ) * OMEGA0)[0]
    on_aut = _on_set(B_AUT); on_sz = _on_set(B_SZ)
    aut_under = bool(len(on_aut) <= n_health)                       # under/at-selective
    sz_aberrant = bool(len(set(on_sz) - H) > 0 and len(on_sz) < len(DRIVES))  # some irrelevant, not all
    seiz_all = bool(len(on_at_seiz) == len(DRIVES))                 # all
    R_ordered = bool(R_aut <= R_health + 1e-9 <= R_sz + 1e-9 and R_sz <= R_ceiling + 1e-9)
    EP4 = bool(R_ordered and aut_under and sz_aberrant and seiz_all)

    # cross-link: the seizure ceiling is the same over-sync ceiling that bounds the cap
    ceiling_headroom_from_health = round(R_ceiling - R_health, 6)

    res = {
        "_what": "Epilepsy as over-synchronisation (D10): the over-sync pole of the "
                 "engine's synchrony axis, made a primary module. An excitatory/"
                 "disinhibitory E/I bias drives the global order parameter R UP toward "
                 "total phase-lock; past a critical bias the selective single-winner "
                 "gate collapses and EVERY candidate assembly ignites -- the ictal state "
                 "(loss of GATING). On one axis: autism-T (under-ignited) < health "
                 "(selective) < schizophrenia (aberrant, some irrelevant) < epilepsy "
                 "(all ignited). An inhibitory / threshold-raising anticonvulsant-class "
                 "push moves R back down and restores the gate (raises the seizure "
                 "threshold). The static susceptibility is characterised; the ictal "
                 "time-course is OWED to a state-switching layer (E2). MECHANISM only -- "
                 "NOT felt, NOT efficacy, NOT medical advice.",
        "axis": {
            "shared_axis": "global synchrony R (Kuramoto order parameter on the measured ephaptic "
                           "kernel) + the M3 R19 ignition gate; seizure = R at the over-sync ceiling "
                           "with the selective gate collapsed",
            "autism_T_pole": "INHIBITORY bias -> coupling DOWN -> R under, under-ignition (D8)",
            "schizophrenia_pole": "excitatory bias -> fold down -> aberrant salience, some irrelevant ignite (D9)",
            "epilepsy_pole": "excitatory bias -> R to lock -> ALL ignite, gate collapsed (this module)",
            "shared_ceiling": "the over-sync ceiling is the ceiling the theta-cap must stay below "
                              "(20-theta-cap-pacemaker), the distance an anticonvulsant enlarges, and "
                              "the distance an excitatory shift closes",
        },
        "baseline_health": {
            "kappa_measured": round(KAP, 6),
            "R_health": round(R_health, 6),
            "R19_fold_spinodal": round(FOLD, 6),
            "candidate_salience_drives": DRIVES,
            "healthy_selective_on_set": sorted(H),
            "n_selected_health": n_health,
        },
        "EP1_oversync_axis": {
            "model": "excitatory/disinhibitory E/I bias raises effective coupling -> R rises toward lock",
            "R_vs_bias": {str(k): round(v, 6) for k, v in R_curve.items()},
            "R_monotone_nondecreasing_in_excitation": bool(R_monotone_up),
            "R_ceiling": round(R_ceiling, 6),
            "R_ceiling_above_health": bool(R_ceiling > R_health),
            "oversync_reproduced": EP1,
        },
        "EP2_ictal_gate_collapse": {
            "model": "past a critical bias the selective gate collapses -> ALL candidate assemblies ignite",
            "selectivity_vs_bias": {str(k): v for k, v in sel_curve.items()},
            "selectivity_monotone_nondecreasing": bool(sel_monotone),
            "seizure_threshold_bias": b_seiz,
            "on_set_at_threshold": sorted(on_at_seiz),
            "all_candidates_ignite": gate_collapsed,
            "every_irrelevant_recruited": every_irrelevant_recruited,
            "gate_collapse_reproduced": EP2,
            "axis_A_firewall": "loss of GATING is a mechanism boundary, NOT a claim about ictal "
                               "subjective experience; consciousness_claim stays 0",
        },
        "EP3_anticonvulsant_sign": {
            "model": "from an ictal bias, an inhibitory / threshold-raising push lowers R and restores "
                     "selective gating -- the GABAergic anticonvulsant-class direction; sign only",
            "ictal_bias": B_ICTAL,
            "R_ictal": round(R_ictal, 6),
            "R_vs_anticonvulsant_strength": {str(k): round(v, 6) for k, v in R_acd_curve.items()},
            "R_monotone_down_under_anticonvulsant": bool(R_acd_monotone_down),
            "selectivity_vs_anticonvulsant_strength": {str(k): v for k, v in sel_acd_curve.items()},
            "selective_gating_restored": selectivity_restored,
            "anticonvulsant_lowers_R": acd_lowers_R,
            "anticonvulsant_sign_reproduced": EP3,
            "raises_seizure_threshold": "the inhibitory push raises the bias needed to lose the gate "
                                        "(moves the operating point away from the over-sync ceiling)",
        },
        "EP4_axis_ordering": {
            "_what": "autism-T < health < schizophrenia < epilepsy on the one synchrony axis",
            "R_autism_T": round(R_aut, 6),
            "R_health": round(R_health, 6),
            "R_schizophrenia": round(R_sz, 6),
            "R_seizure_ceiling": round(R_ceiling, 6),
            "on_set_autism_T": sorted(on_aut),
            "on_set_schizophrenia": sorted(on_sz),
            "on_set_seizure": sorted(on_at_seiz),
            "autism_under_ignited": aut_under,
            "schizophrenia_aberrant_partial": sz_aberrant,
            "seizure_all_ignited": seiz_all,
            "R_ordered_autT_le_health_le_sz_le_seiz": R_ordered,
            "ceiling_headroom_from_health": ceiling_headroom_from_health,
            "axis_ordering_reproduced": EP4,
        },
        "cited_and_locked": {
            "hypersynchrony_defines_seizure": "hypersynchronous neuronal firing is the defining "
                "electrophysiology of an epileptic seizure (Fisher 2005 ILAE; the EEG ictal signature)",
            "EI_imbalance_lowers_threshold": "a shift in excitation/inhibition toward excitation lowers "
                "the seizure threshold; enhancing inhibition (GABAergic) raises it -- the basis of many "
                "anticonvulsants (benzodiazepines, barbiturates, vigabatrin, tiagabine)",
            "epilepsy_heterogeneous_LOCK": "real epilepsy is HETEROGENEOUS -- focal vs generalised, with "
                "genetic channelopathies (SCN1A Dravet, KCNQ2, GABRG2), structural, metabolic, autoimmune "
                "and idiopathic etiologies -- NOT one mechanism or one gene",
            "ictal_onset_needs_dynamics_LOCK": "the ictal ONSET as a temporal transition (a seizure "
                "starting and spreading in time) requires a dynamic state-switching layer (the R19 "
                "bistable switch used over time, E2); this module characterises only the STATIC "
                "susceptibility (the standing E/I state and the sign of the operators)",
            "shared_ceiling_LOCK": "the over-sync ceiling here is the same ceiling the autism theta-cap "
                "must stay below (20-theta-cap-pacemaker over-syncs past inj~0.15) -- one ceiling, three "
                "clinical readings (autism cap bound / SZ extreme / seizure threshold)",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; which "
                "seizure type or etiology any individual's epilepsy is, is held OPEN",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "ictal_time_course": "OWED [O] -- the temporal ictal transition needs a state-switching "
                "layer (E2); only static susceptibility is asserted here",
            "which_seizure_type_individual": "OWED [O] -- requires per-individual data (EEG, genetics, "
                "imaging); the model asserts the over-sync mechanism and the E/I sign, NOT which "
                "epilepsy any individual has",
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "pac_grounded": True,
        },
        "overall": {
            "oversync_reproduced": EP1,
            "gate_collapse_reproduced": EP2,
            "anticonvulsant_sign_reproduced": EP3,
            "axis_ordering_reproduced": EP4,
            "is_full_module": bool(EP1 and EP2 and EP3 and EP4),
            "verdict": "epilepsy is the over-synchronisation pole of the engine's synchrony axis: an "
                       "excitatory E/I bias drives R to the over-sync ceiling and the selective gate "
                       "collapses (all assemblies ignite -- the ictal state); an inhibitory / "
                       "threshold-raising anticonvulsant-class push reverses it and raises the seizure "
                       "threshold. autism-T < health < schizophrenia < epilepsy on one axis, and the "
                       "over-sync ceiling is the same ceiling the theta-cap must stay below. The ictal "
                       "time-course is OWED to a state-switching layer (E2). efficacy=0.",
        },
    }
    return res


def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def _blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def epilepsy_oversync_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "epilepsy_oversync_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_epilepsy_oversync_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"epilepsy_oversync_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = epilepsy_oversync_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    b = res["baseline_health"]
    e1 = res["EP1_oversync_axis"]; e2 = res["EP2_ictal_gate_collapse"]
    e3 = res["EP3_anticonvulsant_sign"]; e4 = res["EP4_axis_ordering"]
    print("=" * 78)
    print("EPILEPSY -- OVER-SYNCHRONISATION (D10)   add-only, engine READ-ONLY")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  health: R={b['R_health']}  fold={b['R19_fold_spinodal']}  selective ON={b['healthy_selective_on_set']} (n={b['n_selected_health']})")
    print("-" * 78)
    print(f"  EP1 over-sync : R(bias)={e1['R_vs_bias']}")
    print(f"        monotone-up={e1['R_monotone_nondecreasing_in_excitation']}  ceiling={e1['R_ceiling']}>health => {e1['oversync_reproduced']}")
    print(f"  EP2 gate-coll : sel(bias)={e2['selectivity_vs_bias']}")
    print(f"        seizure-threshold-bias={e2['seizure_threshold_bias']}  ON@thr={e2['on_set_at_threshold']}  all-ignite={e2['all_candidates_ignite']} => {e2['gate_collapse_reproduced']}")
    print(f"  EP3 anticonv  : R_ictal={e3['R_ictal']}  R(ACD)={e3['R_vs_anticonvulsant_strength']}  sel(ACD)={e3['selectivity_vs_anticonvulsant_strength']}")
    print(f"        monotone-down={e3['R_monotone_down_under_anticonvulsant']}  gating-restored={e3['selective_gating_restored']} => {e3['anticonvulsant_sign_reproduced']}")
    print(f"  EP4 ordering  : R autT={e4['R_autism_T']} < health={e4['R_health']} < SZ={e4['R_schizophrenia']} < seiz={e4['R_seizure_ceiling']}")
    print(f"        autT-under={e4['autism_under_ignited']} SZ-aberrant={e4['schizophrenia_aberrant_partial']} seiz-all={e4['seizure_all_ignited']} => {e4['axis_ordering_reproduced']}")
    print("-" * 78)
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  EPILEPSY MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
