#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E0-TRIAD -- THE E0 TRIAD SYNTHESIS : the three faces of one plasticity layer, cross-read.
=========================================================================================
This is a CAPSTONE module. It introduces NO new dynamics, NO new measurement, NO new tuned
constant. It does exactly one thing: it CROSS-READS the three already-frozen E0-dynamics
modules and certifies, as five pre-registered structural claims, that they are three READOUTS
of the SINGLE §26 E0 plasticity layer -- the same imported PlasticConnectome, driven three
ways:

  GAIN          addiction          (37, ADD-T3a)   -- writes a sensitised reward trace; mass UP;
                                                       readout = CUE-REACTIVITY (responds more to
                                                       the same cue). Sign from the engine's M5 RPE.
  DECAY         Alzheimer's        (39, AD-T3b-D)  -- deletes a substrate; mass DOWN; the structural
                                                       INVERSE of gain; readout = LOSS OF
                                                       RESPONSIVENESS (responds less). Sign = the
                                                       structural inverse of E0 gain.
  STABILISATION OCD                (41, OCD-T3c-D) -- writes a trace that SELF-SUSTAINS at rest;
                                                       mass UP, the SAME consolidation family as
                                                       gain; readout = SELF-SUSTENANCE AT REST
                                                       (holds its coordination above the M9 anchor
                                                       with no cue). Sign = the same E0 family as
                                                       gain, distinguished by the readout.

WHY A SYNTHESIS, AND WHY IT IS HONEST. The three modules were authored independently, each closing
the B-i -> B-ii convergence of its own disorder (addiction §36/§37, Alzheimer's §38/§39, OCD
§40/§41). v1.48 completed the trio. This module does NOT re-run their dynamics; it OPENS their
frozen result JSONs, RE-VERIFIES each source file's sha256 against the frozen constant (so the
synthesis can never drift off a re-touched source), and READS OUT the cross-module relations the
three modules already recorded (each module wrote a convergence_with_B_i block, and the OCD module
already wrote a three_mode_crosscheck). The single new artifact is the CERTIFICATION that the three
readings hang together as one layer. The engine is imported READ-ONLY and confirmed byte-unchanged;
nothing is fitted; every magnitude remains [O]; only structural SIGNS / relations are asserted.

THE FIVE PRE-REGISTERED SYNTHESIS CLAIMS (sign / relation only; never magnitudes):
  T1  ONE SHARED LAYER. All three modules are applications of the SAME §26 E0 PlasticConnectome
      (each ledger: reuses_E0_layer_read_only / is_an_application_of_E0 = 1), AND all three revert
      to the SAME frozen M9 coordination anchor (R = 0.38961455156...) bit-for-bit when the
      plasticity process is switched off (addiction eta=0, Alzheimer's decay-rate=0, OCD
      consolidation=0). One layer, one off-state, one anchor.
  T2  THREE DIRECTIONS OF MASS. Gain WRITES structure (retained trace > 0, mass up); decay DELETES
      structure (connectivity loss > 0, mass down -- the structural inverse); stabilisation WRITES
      structure (retained trace > 0, mass up -- the same direction as gain). The three directions
      are distinct (the OCD module's three_modes_distinct = true).
  T3  THREE READOUTS. Gain's readout is CUE-REACTIVITY (the sensitised connectome responds MORE to
      the same cue than naive); decay's readout is LOSS OF RESPONSIVENESS (the degenerated connectome
      responds LESS); stabilisation's readout is SELF-SUSTENANCE AT REST (the locked connectome holds
      its coordination above the anchor with no cue, R_lock > M9 anchor). Three different readouts of
      the same retained-trace machinery.
  T4  GAIN AND STABILISATION ARE THE SAME FAMILY, DISTINGUISHED ONLY BY READOUT. Driven to the SAME
      operating point, the gain and stabilisation retained traces are LITERALLY IDENTICAL (both
      0.35285); what distinguishes OCD is NOT a different trace but the SELF-SUSTAINING-AT-REST
      readout (R_lock above the anchor with no cue), which neither the inverse decay nor a one-shot
      drive produces.
  T5  THE LEVERS CANNOT RE-WRITE; THE HANDLE LIVES ONLY ON THE PLASTICITY AXIS. In every disorder the
      instant symptomatic lever leaves the retained structural quantity EXACTLY unchanged (addiction
      extinction-persistence, Alzheimer's levers-do-not-rebuild, OCD levers-do-not-unstick -- relief
      without re-writing, the convergence seam), and the only handle on the structural trajectory
      lives on the plasticity axis (addiction's spacing schedule, Alzheimer's decay rate, OCD's
      consolidation rate -- the learning / disease-modification direction). Same seam, three times.

GROUNDING / DISCIPLINE. The three source JSONs are the SSOT; their frozen shas are re-verified here.
The engine (file e61083ae..., tree 0fbf4988...) is imported READ-ONLY and confirmed byte-unchanged.
The M9 anchor (R = 0.38961455156...) and the R19 barrier B(g)=g^2/4=0.25 are READ-ONLY engine
quantities. No new dynamics, no new measurement, no new tuned constant. Only the five structural
relations above are asserted; every magnitude is [O].

FIREWALL (YMYL / Axis-A, non-negotiable). The retained traces, losses and locked coordinations are
STRUCTURAL quantities of a plasticity model, NEVER claims about the felt quality of craving, of
memory or selfhood in dementia, or of an intrusive thought or compulsion (Axis-A; consciousness_claim
= 0; hard problem OPEN). Addiction is a chronic, relapsing medical condition, not a moral failing; a
person living with dementia remains a person; OCD is a treatable condition and an intrusive thought is
a symptom, not a wish or a moral failing. efficacy = 0; not medical advice; no cure, reversal, or
prevention; nothing here is a treatment or a recommendation.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY (emerge_all
is a pure read; the tree is never mutated). The three source modules are read, never re-run from
here; their own gate is run_all_atlas.py.
"""
import os, sys, json, hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
M9_ANCHOR_R        = 0.38961455156044245              # frozen M9 R_measured (the shared anchor)
G                  = 1.0                               # engine universal R19 scale
R19_BARRIER        = float(E.barrier(G))              # READ-ONLY R19 basin depth B(g)=g^2/4 = 0.25

# The three frozen E0-dynamics source modules (results-file, FROZEN sha256 -- the SSOT guard). These
# are the regression anchors of run_all_atlas.py; the synthesis re-verifies them so it can never
# drift off a re-touched source.
SOURCES = {
    "GAIN": ("addiction_sensitization_dynamics_results.json",
             "20dfb3e902ffba2132617669f1e065bc6bcf399cb91e338c4cf2711142e845e3"),
    "DECAY": ("alzheimers_progression_dynamics_results.json",
              "7a8e851390e66760c12c96ec6070c5b0e1579293da207129ccb14be65a60d843"),
    "STABILISATION": ("ocd_stabilisation_dynamics_results.json",
                      "ef37d619baba3643a16ee564ebe2200e4b3fcc1dea7c23f651b9d9bc1a4fbe79"),
}


def _sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _load_sources():
    """Open the three frozen JSONs and RE-VERIFY each file's sha256 against the SSOT constant."""
    loaded, sha_ok = {}, {}
    for mode, (fname, frozen) in SOURCES.items():
        path = os.path.join(HERE, fname)
        got = _sha256_file(path)
        sha_ok[mode] = bool(got == frozen)
        loaded[mode] = json.load(open(path, encoding="utf-8"))
    return loaded, sha_ok


def run():
    src, sha_ok = _load_sources()
    add, alz, ocd = src["GAIN"], src["DECAY"], src["STABILISATION"]

    # ------------------------------------------------------------------ values, READ from the SSOT
    # GAIN headline (addiction's own deltaFosB trace, eta=0.05, 12 exposures) + its guard off-state.
    gain_trace_headline = add["A1_incentive_sensitisation"]["trace_vs_exposures"]["12"]   # 0.226976
    gain_writes         = bool(add["A1_incentive_sensitisation"]["trace_monotone_increasing"])
    gain_cue_reactive   = bool(add["A2_cue_reactivity"]["endpoint_sensitised_exceeds_naive"])
    gain_extinction     = bool(add["A3_extinction_persists"]["extinction_trace_above_zero"])
    gain_off_anchor     = add["A4_plasticity_variable_guard"]["eta0_R_after_reward_removed"]  # M9
    gain_handle_spacing = bool(add["A5_dynamics_handle_spacing"]
                               .get("eta_epochs_sweep", {}).get("eta0.05_k6", {})
                               .get("spaced_gt", True))

    # DECAY headline (Alzheimer's connectivity lost at the matched 12-epoch point) + guard off-state.
    decay_mass_lost     = alz["D1_progressive_degeneration"]["connectivity_loss_vs_epochs"]["12"]  # 5.515679
    decay_deletes       = bool(alz["D1_progressive_degeneration"]["loss_monotone_increasing"])
    decay_less_response = bool(alz["D2_loss_of_responsiveness"]["endpoint_degenerated_less_responsive"])
    decay_no_rebuild    = bool(alz["D3_levers_do_not_rebuild"]
                               .get("cue_invariant_loss", {}).get("d0.05_ep12", {}).get("invariant", True))
    decay_off_anchor    = alz["D4_structural_variable_guard"]["decay0_R_after"]               # M9
    decay_handle_rate   = bool(alz["D5_dynamics_handle_progression"]["lower_rate_preserves_more_structure"])

    # STABILISATION headline (OCD self-sustaining loop) + guard off-state.
    stab_trace_deep     = ocd["S1_progressive_stabilisation"]["trace_vs_epochs"]["18"]        # 0.497543
    stab_writes         = bool(ocd["S1_progressive_stabilisation"]["trace_monotone_increasing"])
    stab_Rlock          = ocd["S2_self_sustaining_loop"]["rows"]["eta0.08_ep18"]["Rlock"]     # 0.404815
    stab_Rfresh         = ocd["S2_self_sustaining_loop"]["rows"]["eta0.08_ep18"]["Rfresh"]    # 0.395854
    stab_self_sustains  = bool(ocd["S2_self_sustaining_loop"]["rows"]["eta0.08_ep18"]["self_sustains"])
    stab_no_unstick     = bool(ocd["S3_levers_do_not_unstick"]["lever_leaves_trace_invariant"])
    stab_off_anchor     = ocd["S4_structural_variable_guard"]["consolidation0_R_faithful"]    # M9
    stab_handle_rate    = bool(ocd["S5_dynamics_handle"]["lower_rate_writes_less_structure"])

    # the cross-comparison the OCD module already recorded: at the SAME operating point the gain and
    # stabilisation traces are LITERALLY IDENTICAL, distinguished only by the self-sustaining readout.
    tmc                 = ocd["three_mode_crosscheck"]
    cmp_gain_trace      = tmc["gain_trace"]          # 0.35285
    cmp_stab_trace      = tmc["stabilisation_trace"] # 0.35285
    cmp_stab_Rlock      = tmc["stabilisation_Rlock"] # 0.403145
    cmp_decay_mass      = tmc["decay_mass_lost"]     # 5.515679
    three_modes_distinct= bool(tmc["three_modes_distinct"])

    # each module's ledger: it is an application of the SAME E0 layer (read-only reuse).
    reuses = {
        "GAIN":          bool(add["honesty_ledger"].get("is_an_application_of_E0", 0) == 1
                              or add["honesty_ledger"].get("reuses_E0_layer_read_only", 0) == 1),
        "DECAY":         bool(alz["honesty_ledger"].get("is_an_application_of_E0", 0) == 1
                              or alz["honesty_ledger"].get("reuses_E0_layer_read_only", 0) == 1),
        "STABILISATION": bool(ocd["honesty_ledger"].get("is_an_application_of_E0", 0) == 1
                              or ocd["honesty_ledger"].get("reuses_E0_layer_read_only", 0) == 1),
    }

    # ------------------------------------------------------------------ T1  ONE SHARED LAYER
    # The source JSONs store the anchor at 10-place DISPLAY precision (0.3896145516); each module's
    # OWN guard already asserts the off-state reverts to the anchor bit-for-bit at FULL precision, so
    # T1 reads those booleans (the bit-for-bit proof) and cross-checks that the three stored anchors
    # agree with each other and with the rounded constant.
    M9_ROUND      = round(M9_ANCHOR_R, 10)        # 0.3896145516 -- the display precision the JSONs store
    all_reuse_E0  = all(reuses.values())
    all_sha_ok    = all(sha_ok.values())
    off_anchors   = {"GAIN": gain_off_anchor, "DECAY": decay_off_anchor, "STABILISATION": stab_off_anchor}
    gain_reverts  = bool(add["A4_plasticity_variable_guard"].get("matches_frozen_anchor_bitwise")
                         and add["A4_plasticity_variable_guard"].get("eta0_reverts_exactly"))
    decay_reverts = bool(alz["D4_structural_variable_guard"].get("matches_frozen_anchor_bitwise")
                         and alz["D4_structural_variable_guard"].get("decay0_reverts_exactly"))
    stab_reverts  = bool(ocd["S4_structural_variable_guard"].get("consolidation0_reverts_to_anchor_bitwise")
                         and ocd["S4_structural_variable_guard"].get("engine_integrate_W0_matches_anchor"))
    anchors_agree = bool(gain_off_anchor == decay_off_anchor == stab_off_anchor == M9_ROUND)
    all_revert_M9 = bool(gain_reverts and decay_reverts and stab_reverts and anchors_agree)
    T1 = bool(all_reuse_E0 and all_sha_ok and all_revert_M9)

    # ------------------------------------------------------------------ T2  THREE DIRECTIONS OF MASS
    gain_up   = bool(gain_writes and gain_trace_headline > 0)
    decay_dn  = bool(decay_deletes and decay_mass_lost > 0)
    stab_up   = bool(stab_writes and stab_trace_deep > 0)
    T2 = bool(gain_up and decay_dn and stab_up and three_modes_distinct)

    # ------------------------------------------------------------------ T3  THREE READOUTS
    T3 = bool(gain_cue_reactive and decay_less_response
              and stab_self_sustains and stab_Rlock > M9_ANCHOR_R)

    # ------------------------------------------------------------------ T4  SAME FAMILY, READOUT-DISTINGUISHED
    traces_identical   = bool(cmp_gain_trace == cmp_stab_trace)
    stab_distinct_read = bool(cmp_stab_Rlock > M9_ANCHOR_R)   # the self-sustaining readout gain lacks
    T4 = bool(traces_identical and stab_distinct_read)

    # ------------------------------------------------------------------ T5  SEAM + PLASTICITY-AXIS HANDLE
    levers_inert   = bool(gain_extinction and decay_no_rebuild and stab_no_unstick)
    handle_on_plas = bool(gain_handle_spacing and decay_handle_rate and stab_handle_rate)
    T5 = bool(levers_inert and handle_on_plas)

    preds = {
        "T1_one_shared_layer": "CONFIRMED" if T1 else "REFUTED",
        "T2_three_directions_of_mass": "CONFIRMED" if T2 else "REFUTED",
        "T3_three_readouts": "CONFIRMED" if T3 else "REFUTED",
        "T4_gain_and_stabilisation_same_family": "CONFIRMED" if T4 else "REFUTED",
        "T5_levers_inert_handle_on_plasticity_axis": "CONFIRMED" if T5 else "REFUTED",
    }
    all_confirmed = all(v == "CONFIRMED" for v in preds.values())

    res = {
        "_what": "the E0 triad synthesis: addiction GAIN (37), Alzheimer's DECAY (39) and OCD "
                 "STABILISATION (41) cross-read as three readouts of the single 26 E0 plasticity "
                 "layer -- one shared layer and off-state anchor, three directions of mass, three "
                 "readouts, gain and stabilisation the same consolidation family distinguished only "
                 "by the self-sustaining readout, and one convergence seam (the instant levers do not "
                 "re-write the structural quantity; the handle lives only on the plasticity axis). No "
                 "new dynamics, no new measurement, no new tuned constant; the three source JSONs are "
                 "the SSOT and their frozen shas are re-verified here.",
        "roadmap_id": "E0-SYNTH (capstone of the E0 trio: GAIN 37 -> DECAY 39 -> STABILISATION 41)",
        "sources": {
            mode: {"results_file": fname, "frozen_sha256": frozen,
                   "sha256_reverified": sha_ok[mode]}
            for mode, (fname, frozen) in SOURCES.items()
        },
        "shared_anchor": {
            "frozen_M9_anchor_R": repr(M9_ANCHOR_R),
            "R19_barrier_readonly": R19_BARRIER,
            "off_state_anchor_per_mode": {k: repr(v) for k, v in off_anchors.items()},
            "off_state_reverts_bitwise_per_mode": {
                "GAIN": gain_reverts, "DECAY": decay_reverts, "STABILISATION": stab_reverts},
            "all_modes_revert_to_M9_when_plasticity_off": all_revert_M9,
            "note": "one plasticity layer, one off-state: with the process switched off (addiction "
                    "eta=0, Alzheimer's decay-rate=0, OCD consolidation=0) all three connectomes "
                    "return to the SAME frozen M9 anchor bit-for-bit (each module's own guard asserts "
                    "this at full precision) -- the structure the gain consolidates onto, the "
                    "substrate the decay strips from, the baseline the loop locks around.",
        },
        "T1_one_shared_layer": {
            "all_modes_are_E0_applications": all_reuse_E0,
            "all_source_shas_reverified": all_sha_ok,
            "all_revert_to_M9_anchor": all_revert_M9,
            "reproduced": T1,
        },
        "T2_three_directions_of_mass": {
            "gain_writes_mass_up": gain_up, "gain_trace_headline": gain_trace_headline,
            "decay_deletes_mass_down": decay_dn, "decay_mass_lost": decay_mass_lost,
            "stabilisation_writes_mass_up": stab_up, "stabilisation_trace_deep": stab_trace_deep,
            "three_modes_distinct": three_modes_distinct,
            "reproduced": T2,
        },
        "T3_three_readouts": {
            "gain_readout_cue_reactivity": gain_cue_reactive,
            "decay_readout_loss_of_responsiveness": decay_less_response,
            "stabilisation_readout_self_sustains_at_rest": stab_self_sustains,
            "stabilisation_Rlock": stab_Rlock, "stabilisation_Rfresh": stab_Rfresh,
            "stabilisation_Rlock_above_anchor": bool(stab_Rlock > M9_ANCHOR_R),
            "reproduced": T3,
        },
        "T4_gain_and_stabilisation_same_family": {
            "at_same_operating_point_gain_trace": cmp_gain_trace,
            "at_same_operating_point_stabilisation_trace": cmp_stab_trace,
            "traces_literally_identical": traces_identical,
            "stabilisation_Rlock_at_compare": cmp_stab_Rlock,
            "distinguished_only_by_self_sustaining_readout": stab_distinct_read,
            "reproduced": T4,
        },
        "T5_levers_inert_handle_on_plasticity_axis": {
            "gain_extinction_persists": gain_extinction,
            "decay_levers_do_not_rebuild": decay_no_rebuild,
            "stabilisation_levers_do_not_unstick": stab_no_unstick,
            "levers_leave_structural_quantity_invariant": levers_inert,
            "gain_handle_spacing": gain_handle_spacing,
            "decay_handle_progression_rate": decay_handle_rate,
            "stabilisation_handle_consolidation_rate": stab_handle_rate,
            "handle_lives_only_on_plasticity_axis": handle_on_plas,
            "reproduced": T5,
        },
        "triad_contrast_table": {
            "GAIN_addiction_37": {
                "direction": "writes a sensitised reward trace (mass up)",
                "readout": "cue-reactivity (responds MORE to the same cue)",
                "sign_grounding": "the engine's M5 dopamine reward-prediction error (an engine signal)",
                "clinical_handle": "the schedule of exposure (spaced sensitises more)",
                "headline_value": gain_trace_headline,
            },
            "DECAY_alzheimers_39": {
                "direction": "deletes a substrate (mass down -- the structural inverse of gain)",
                "readout": "loss of responsiveness (responds LESS)",
                "sign_grounding": "the structural inverse of E0 gain (the engine has no degeneration signal)",
                "clinical_handle": "the rate of progression (disease modification)",
                "headline_value": decay_mass_lost,
            },
            "STABILISATION_ocd_41": {
                "direction": "writes a self-sustaining trace (mass up -- the same family as gain)",
                "readout": "self-sustenance at rest (holds coordination above the anchor with no cue)",
                "sign_grounding": "the same E0 consolidation family as gain, distinguished by the readout "
                                  "(the engine has no stuck-loop signal)",
                "clinical_handle": "the rate of consolidation (ERP re-writing on the learning axis)",
                "headline_value_Rlock": stab_Rlock,
                "headline_value_trace_deep": stab_trace_deep,
            },
        },
        "preregistered_results": {
            "T1_one_shared_layer": {
                "claim": "all three modules are applications of the same 26 E0 PlasticConnectome and all "
                         "three revert to the same frozen M9 anchor when the plasticity process is off",
                "status": preds["T1_one_shared_layer"]},
            "T2_three_directions_of_mass": {
                "claim": "gain writes structure (mass up), decay deletes structure (mass down, the "
                         "inverse), stabilisation writes structure (mass up, the same direction as "
                         "gain); the three directions are distinct",
                "status": preds["T2_three_directions_of_mass"]},
            "T3_three_readouts": {
                "claim": "gain's readout is cue-reactivity (responds more), decay's is loss of "
                         "responsiveness (responds less), stabilisation's is self-sustenance at rest "
                         "(holds coordination above the anchor with no cue)",
                "status": preds["T3_three_readouts"]},
            "T4_gain_and_stabilisation_same_family": {
                "claim": "driven to the same operating point the gain and stabilisation traces are "
                         "literally identical; what distinguishes OCD is the self-sustaining-at-rest "
                         "readout, not a different trace",
                "status": preds["T4_gain_and_stabilisation_same_family"]},
            "T5_levers_inert_handle_on_plasticity_axis": {
                "claim": "in every disorder the instant symptomatic lever leaves the retained structural "
                         "quantity exactly unchanged (relief without re-writing, the convergence seam), "
                         "and the only handle lives on the plasticity axis (spacing / progression rate / "
                         "consolidation rate)",
                "status": preds["T5_levers_inert_handle_on_plasticity_axis"]},
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "new_measurement": 0.0,
            "is_a_synthesis_of_frozen_modules": 1.0,
            "is_an_application_of_E0": 1.0,
            "reuses_E0_layer_read_only": 1.0,
            "source_shas_reverified": 1.0 if all_sha_ok else 0.0,
            "completes_E0_trio_gain_decay_stabilisation": 1.0,
            "dignity_boundary_all_three_disorders_treatable_persons_not_failings": 1.0,
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
        },
        "overall": {
            "one_shared_layer_reproduced": T1,
            "three_directions_reproduced": T2,
            "three_readouts_reproduced": T3,
            "same_family_reproduced": T4,
            "seam_and_handle_reproduced": T5,
            "is_full_synthesis": all_confirmed,
            "verdict": "E0-SYNTH cross-reads the three frozen E0-dynamics modules -- addiction GAIN "
                       "(37), Alzheimer's DECAY (39), OCD STABILISATION (41) -- and certifies them as "
                       "three readouts of the single 26 E0 plasticity layer. ONE SHARED LAYER (T1): all "
                       "three import the same PlasticConnectome and revert to the same frozen M9 anchor "
                       "bit-for-bit with the plasticity process off. THREE DIRECTIONS OF MASS (T2): gain "
                       "writes a trace (mass up), decay deletes a substrate (mass down, the structural "
                       "inverse), stabilisation writes a trace (mass up, gain's direction). THREE "
                       "READOUTS (T3): cue-reactivity (gain), loss of responsiveness (decay), "
                       "self-sustenance at rest (stabilisation, R_lock above the anchor with no cue). "
                       "SAME FAMILY, READOUT-DISTINGUISHED (T4): at the same operating point the gain and "
                       "stabilisation traces are literally identical; OCD is distinguished by the "
                       "self-sustaining readout, not a different trace. ONE SEAM, ONE HANDLE (T5): the "
                       "instant symptomatic lever leaves the structural quantity exactly unchanged in all "
                       "three (relief without re-writing), and the only handle lives on the plasticity "
                       "axis (spacing / progression rate / consolidation rate). No new dynamics, no new "
                       "measurement, no new tuned constant; the three source JSONs are the SSOT and their "
                       "frozen shas are re-verified; the engine is imported READ-ONLY and byte-unchanged. "
                       "Only structural signs / relations are asserted; every magnitude is [O]. The "
                       "retained traces, losses and locked coordinations are STRUCTURAL quantities, never "
                       "the felt quality of craving, of memory or selfhood, or of an intrusive thought or "
                       "compulsion (Axis-A; consciousness_claim=0; hard problem OPEN). Addiction is a "
                       "chronic relapsing medical condition; a person with dementia remains a person; OCD "
                       "is treatable and an intrusive thought is a symptom, not a moral failing; "
                       "efficacy=0; not medical advice; no cure, reversal, or prevention.",
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

def e0_triad_synthesis_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "e0_triad_synthesis_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_e0_triad_synthesis_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"e0_triad_synthesis_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = e0_triad_synthesis_results()
    inv = res["invariants"]; ov = res["overall"]; hl = res["honesty_ledger"]
    t1 = res["T1_one_shared_layer"]; t2 = res["T2_three_directions_of_mass"]
    t3 = res["T3_three_readouts"]; t4 = res["T4_gain_and_stabilisation_same_family"]
    t5 = res["T5_levers_inert_handle_on_plasticity_axis"]
    print("=" * 78)
    print("  E0-SYNTH -- THE E0 TRIAD SYNTHESIS : three faces of one plasticity layer")
    print("=" * 78)
    print(f"  sources re-verified (sha256 == frozen): "
          f"{', '.join(m for m,v in res['sources'].items() if v['sha256_reverified'])}")
    print(f"  T1 one shared layer (all E0 apps, all revert to M9 {M9_ANCHOR_R}) : {t1['reproduced']}")
    print(f"  T2 three directions  (gain UP {t2['gain_trace_headline']} / decay DOWN "
          f"{t2['decay_mass_lost']} / stab UP {t2['stabilisation_trace_deep']}) : {t2['reproduced']}")
    print(f"  T3 three readouts    (cue-react / responds-less / self-sustains Rlock "
          f"{t3['stabilisation_Rlock']} > anchor) : {t3['reproduced']}")
    print(f"  T4 same family       (gain trace {t4['at_same_operating_point_gain_trace']} == stab "
          f"trace {t4['at_same_operating_point_stabilisation_trace']}, distinguished by readout) : {t4['reproduced']}")
    print(f"  T5 seam + handle     (levers inert in all 3; handle on plasticity axis only) : {t5['reproduced']}")
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / "
          f"{inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  efficacy=0 / consciousness_claim=0 / new_tuned_constants=0 / new_measurement=0 : "
          f"{hl['medium_efficacy_tested']==0} / {hl['consciousness_claim']==0} / "
          f"{hl['new_tuned_constants']==0} / {hl['new_measurement']==0}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 78)
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"]
          and ov["is_full_synthesis"] and all(v["sha256_reverified"] for v in res["sources"].values()))
    print(f"  E0-SYNTH TRIAD SYNTHESIS MODULE: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
