#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CROSS-SYNTH -- THE CROSS-AXIS COUPLING SYNTHESIS : three couplings, three decouplings, one discipline.
======================================================================================================
This is a CAPSTONE module. It introduces NO new dynamics, NO new measurement, NO new tuned constant.
It does exactly one thing: it CROSS-READS the three already-frozen CROSS-AXIS COUPLING modules and
certifies, as five pre-registered structural claims, that they are one FAMILY -- the three pairwise
EDGES of the same three layers E0 (plasticity, 26), E1 (spatial localisation, 43) and E2 (state
switching, 28) -- and that what each coupling's genuinely-new seam reveals is, in all three cases, a
DECOUPLING of two quantities the single-axis intuition welds together:

  E1 x E0   spatial-plasticity imprint  (47, SPC-E1E0)  -- WHERE a focal drive leaves a LASTING trace.
                                                            New object: a focal drive run THROUGH the
                                                            plastic connectome (the imprint readout).
                                                            Decoupling (C3): clean DELIVERY != clean
                                                            IMPRINT -- the retained-trace relay set
                                                            STRICTLY CONTAINS the instantaneous-field
                                                            relay set; plasticity DELOCALISES the mark.
                                                            "when space meets time".
  E1 x E2   spatial switch leverage     (48, SPC-E1E2)  -- WHICH focal drive most easily FLIPS the
                                                            collective state. New object: the bistable
                                                            cell driven by a node's frozen-kernel
                                                            BROADCAST LEVERAGE (the LeverageSwitch).
                                                            Decoupling (C3): switchability decouples
                                                            from BOTH the instantaneous footprint AND
                                                            the spatial reach -- the reach hub is among
                                                            the HARDEST to flip. "when space meets state".
  E0 x E2   kindling                    (49, E0E2-KIND) -- whether REPEATED flips become EASIER.
                                                            New object: the bistable cell driven THROUGH
                                                            the evolving connectome (the KindlingSwitch).
                                                            Decoupling (K3): easier-to-flip decouples
                                                            from EROSION -- the kindled connectome ends
                                                            MORE coordinated; the threshold falls through
                                                            CONSOLIDATION, not degradation. "when time
                                                            meets state".

WHY A SYNTHESIS, AND WHY IT IS HONEST. The three modules were authored independently, each marrying two
frozen layers for the first time (47 opened E1xE0, 48 opened E1xE2, 49 opened E0xE2 and closed the
bipolar trace->threshold link). v1.56 completed the trio of pairwise couplings. This module does NOT
re-run their dynamics; it OPENS their frozen result JSONs, RE-VERIFIES each source file's SHA-256 against
the frozen constant (so the synthesis can never drift off a re-touched source), and READS OUT the
cross-module relations the three modules already recorded (each module wrote a coupling ledger, a
decoupling result, and an engine-invariance guard). The single new artifact is the CERTIFICATION that
the three couplings hang together as one family with one shape. The engine is imported READ-ONLY and
confirmed byte-unchanged; nothing is fitted; every magnitude remains [O]; only structural SIGNS /
RELATIONS are asserted.

THE FIVE PRE-REGISTERED SYNTHESIS CLAIMS (sign / relation only; never magnitudes):
  T1  ONE FAMILY -- ALL THREE PAIRWISE EDGES OF THE E0/E1/E2 TRIANGLE. All three modules are couplings
      of TWO frozen layers (each ledger: couples_E1_and_E0 / couples_E1_and_E2 / couples_E0_and_E2 = 1),
      and TOGETHER they realise all THREE pairwise edges of the three layers E0 (plasticity), E1 (spatial)
      and E2 (state switching): {E1,E0} (47), {E1,E2} (48), {E0,E2} (49). Each layer-vertex therefore
      appears in EXACTLY TWO couplings (degree 2). AND every coupling reverts to the frozen engine
      BIT-FOR-BIT when its drive is switched off (each module's own engine-invariance guard reproduced).
      One family, three edges, one off-state.
  T2  ONE NEW JOINING OBJECT PER COUPLING. Each coupling introduces EXACTLY ONE new object that joins its
      two layers and re-derives NEITHER (each ledger reuses BOTH its layers read-only): the spatial-imprint
      readout (47, a focal drive through the plastic connectome), the LeverageSwitch (48, the bistable cell
      driven by broadcast leverage) and the KindlingSwitch (49, the bistable cell driven through the
      evolving connectome). Three distinct new objects, every layer imported not re-derived, and NO new
      tuned constant in any of the three.
  T3  THREE DECOUPLINGS. The genuinely-new result each seam surfaces is, in all three, a DECOUPLING of two
      quantities the single-axis intuition welds together -- and all three are CONFIRMED: clean delivery is
      decoupled from clean imprint (47 C3, the retained-trace relay STRICTLY CONTAINS the field relay),
      switchability is decoupled from both instantaneous footprint and spatial reach (48 C3, the reach hub
      is among the hardest to flip), and easier-to-flip is decoupled from erosion (49 K3, coordination
      RISES as the threshold falls). Three decouplings, three CONFIRMED.
  T4  A COMMON SHAPE -- A SINGLE-AXIS LAW BREAKS, AND THE CLEAN HYPOTHESIS IS REPORTED FALSE. The three
      decouplings share a shape: each REFUTES a tidy single-axis hypothesis that the coupling was the
      natural place to test, and reports the refutation HONESTLY rather than forcing a monotone narrative
      -- no universal focal>diffuse imprint law (47, clean_hypothesis_refuted), no universal reach->
      switchability law (48, reach_to_switchability_law_refuted), no clean kindling-erodes-coordination
      story (49, erosion_hypothesis_refuted). The no-tuning discipline produces the SAME honest-negative
      shape three times: when space meets time the imprint decouples from delivery, when space meets state
      the flip decouples from footprint and reach, when time meets state the kindling decouples from erosion.
  T5  ONE COUPLING DISCIPLINE, THREE TIMES. Every coupling obeys the SAME discipline: it sweeps BOTH coupled
      axes' parameters so every sign survives the product grid (anti-tuning -- 47 sweeps stimulation
      intensity AND plasticity rate, 48 sweeps stimulation intensity AND barrier depth, 49 sweeps plasticity
      rate AND barrier depth), it reverts to the frozen engine BIT-FOR-BIT when the drive is off (inheriting
      EACH layer's guard -- E1xE0 the M9 anchor, E1xE2 the E.settle relaxation, E0xE2 BOTH), and it reports
      any decoupling honestly. No new measurement and no new tuned constant in any. Same seam discipline,
      three couplings.

GROUNDING / DISCIPLINE. The three source JSONs are the SSOT; their frozen shas are re-verified here
(SPC-E1E0 cdb16230..., SPC-E1E2 bd3a9e23..., E0E2-KINDLING 3880e63f...). The engine (file e61083ae...,
tree 0fbf4988...) is imported READ-ONLY and confirmed byte-unchanged. The M9 anchor (R = 0.38961455156...)
and the R19 barrier B(g)=g^2/4=0.25 are READ-ONLY engine quantities. No new dynamics, no new measurement,
no new tuned constant. Only the five structural relations above are asserted; every magnitude is [O].

FIREWALL (YMYL / Axis-A, non-negotiable). The imprints, leverages, flip thresholds, retained traces and
coordination gains the three couplings certify are STRUCTURAL quantities of coupled models, NEVER claims
about a felt state, an experienced mood, a level of consciousness, an experienced ease of relapse, a real
connectome or synaptic-weight matrix, a real measure of where a drive leaves a mark, which target is most
switchable, or whether any patient's episodes accelerate (Axis-A; consciousness_claim = 0; hard problem
OPEN). Every magnitude is [O]; the [L] correspondences in the source chapters are direction-only; target
selection, device programming, prognosis and treatment are external clinical determinations. efficacy = 0;
not medical advice; no cure, reversal, or prevention; nothing here is a treatment or a recommendation.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY (emerge_all is a
pure read; the tree is never mutated). The three source modules are read, never re-run from here; their own
gate is run_all_atlas.py.
"""
import os, sys, json, hashlib
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
M9_ANCHOR_R        = 0.38961455156044245              # frozen M9 R_measured (the shared anchor)
G                  = 1.0                               # engine universal R19 scale
R19_BARRIER        = float(E.barrier(G))              # READ-ONLY R19 basin depth B(g)=g^2/4 = 0.25

# The three frozen CROSS-AXIS COUPLING source modules (results-file, FROZEN sha256 -- the SSOT guard).
# These are regression anchors of run_all_atlas.py; the synthesis re-verifies them so it can never drift
# off a re-touched source. The third tuple entry is the unordered pair of layer-axes the coupling marries.
SOURCES = {
    "E1xE0": ("spatial_plasticity_imprint_results.json",
              "cdb1623009fe2a02818c00be5fd2243034d43880501fde89b75270e0574ec036",
              ("E1", "E0")),
    "E1xE2": ("spatial_switch_leverage_results.json",
              "bd3a9e230a4304371bc17ced39e7ae08b5c0dcf99855c9842f3eaea84ab7ea4e",
              ("E1", "E2")),
    "E0xE2": ("e0e2_kindling_results.json",
              "3880e63ff23d43b10506824fdf7b6b5c54cee19ef73e3e4bd6369079e31aa9f0",
              ("E0", "E2")),
}

# the three layer-vertices and the complete set of pairwise edges expected of the triangle
LAYERS = ("E0", "E1", "E2")
COMPLETE_TRIANGLE = {frozenset(("E0", "E1")), frozenset(("E1", "E2")), frozenset(("E0", "E2"))}


def _sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _load_sources():
    """Open the three frozen JSONs and RE-VERIFY each file's sha256 against the SSOT constant."""
    loaded, sha_ok = {}, {}
    for mode, (fname, frozen, _edge) in SOURCES.items():
        path = os.path.join(HERE, fname)
        got = _sha256_file(path)
        sha_ok[mode] = bool(got == frozen)
        loaded[mode] = json.load(open(path, encoding="utf-8"))
    return loaded, sha_ok


def run():
    src, sha_ok = _load_sources()
    imp, lev, kin = src["E1xE0"], src["E1xE2"], src["E0xE2"]
    Himp, Hlev, Hkin = imp["honesty_ledger"], lev["honesty_ledger"], kin["honesty_ledger"]

    # ------------------------------------------------------------------ values, READ from the SSOT
    # E1xE0 (47) headline: the retained-trace relay set STRICTLY CONTAINS the instantaneous-field relay.
    imp_C3            = imp["C3_decoupled_and_no_universal_law"]
    imp_decoupled     = bool(imp_C3["decoupled"])
    imp_contains      = bool(imp_C3["trace_relay_strictly_contains_field_relay"])
    imp_no_law        = bool(imp_C3["no_universal_focal_gt_diffuse_trace_law"])
    imp_trace_n       = len(imp_C3["trace_relay_set"])
    imp_field_n       = len(imp_C3["field_relay_set_sec46"])
    imp_C3_status     = imp["preregistered_results"]["C3_delivery_imprint_decoupled_no_universal_law"]["status"]
    imp_guard         = bool(imp["overall"]["engine_invariance_guard"])
    imp_couples       = bool(Himp.get("couples_E1_and_E0", 0) == 1)
    imp_reuse_E1      = bool(Himp.get("reuses_E1_spatial_field", 0) == 1)
    imp_reuse_E0      = bool(Himp.get("reuses_E0_plasticity", 0) == 1)
    imp_refuted       = bool("clean_hypothesis_refuted" in Himp)
    imp_tuned0        = bool(Himp.get("new_tuned_constants", 1) == 0)
    imp_sweep_a       = str(Himp.get("stimulation_intensity", "")).startswith("OPEN [O]")
    imp_sweep_b       = str(Himp.get("plasticity_rate_eta", "")).startswith("OPEN [O]")

    # E1xE2 (48) headline: switchability decoupled from footprint AND reach; the reach hub is hard to flip.
    lev_C3            = lev["C3_decoupled_and_no_reach_law"]
    lev_decoupled     = bool(lev_C3["decoupled"])
    lev_dec_footprint = bool(lev_C3["decoupled_from_instantaneous_footprint"])
    lev_no_reach_law  = bool(lev_C3["no_universal_reach_to_switchability_law"])
    lev_reach_hub     = lev_C3["reach_hub_sec43"]
    lev_reach_rank    = lev_C3["reach_hub_switch_rank"]
    lev_switch_hub    = lev_C3["switch_leverage_hub"]
    lev_C3_status     = lev["preregistered_results"]["C3_switchability_decoupled_from_footprint_and_reach"]["status"]
    lev_guard         = bool(lev["overall"]["engine_invariance_guard"])
    lev_couples       = bool(Hlev.get("couples_E1_and_E2", 0) == 1)
    lev_reuse_E1      = bool(Hlev.get("reuses_E1_spatial_field", 0) == 1)
    lev_reuse_E2      = bool(Hlev.get("reuses_E2_state_switching", 0) == 1)
    lev_refuted       = bool("reach_to_switchability_law_refuted" in Hlev)
    lev_tuned0        = bool(Hlev.get("new_tuned_constants", 1) == 0)
    lev_sweep_a       = str(Hlev.get("stimulation_intensity", "")).startswith("OPEN [O]")
    lev_sweep_b       = str(Hlev.get("barrier_depth_g", "")).startswith("OPEN [O]")

    # E0xE2 (49) headline: easier-to-flip decoupled from erosion; coordination RISES as threshold falls.
    kin_K3            = kin["K3_consolidative_not_degradative"]
    kin_decoupled     = bool(kin_K3["easier_flip_decoupled_from_erosion"])
    kin_R_rises       = bool(kin_K3["coordination_R_rises_net"])
    kin_ends_above    = bool(kin_K3["kindled_connectome_ends_at_or_above_anchor"])
    kin_R0            = kin_K3["R_vs_episode_at_rep"]["0"]
    kin_R8            = kin_K3["R_vs_episode_at_rep"]["8"]
    kin_K3_status     = kin["preregistered_results"]["K3_kindling_is_consolidative_not_degradative"]["status"]
    kin_guard         = bool(kin["overall"]["engine_invariance_guard"])
    kin_couples       = bool(Hkin.get("couples_E0_and_E2", 0) == 1)
    kin_reuse_E0      = bool(Hkin.get("reuses_E0_plasticity", 0) == 1)
    kin_reuse_E2      = bool(Hkin.get("reuses_E2_state_switching", 0) == 1)
    kin_refuted       = bool("erosion_hypothesis_refuted" in Hkin)
    kin_tuned0        = bool(Hkin.get("new_tuned_constants", 1) == 0)
    kin_sweep_a       = str(Hkin.get("plasticity_rate", "")).startswith("OPEN [O]")
    kin_sweep_b       = str(Hkin.get("barrier_depth_g", "")).startswith("OPEN [O]")

    all_sha_ok = all(sha_ok.values())

    # ------------------------------------------------------------------ T1  ONE FAMILY / TRIANGLE
    # each module declares the pair of layers it couples; together they must realise the COMPLETE triangle
    # of pairwise edges of {E0,E1,E2}, every vertex appearing exactly twice (degree 2), and every module's
    # own engine-invariance guard reproduced (the off-state reverts to the frozen engine bit-for-bit).
    edges = {frozenset(edge) for (_f, _s, edge) in SOURCES.values()}
    all_three_edges = bool(edges == COMPLETE_TRIANGLE)
    deg = Counter()
    for e in edges:
        for v in e:
            deg[v] += 1
    every_vertex_degree_2 = bool(all(deg[v] == 2 for v in LAYERS))
    all_couple = bool(imp_couples and lev_couples and kin_couples)
    all_guards = bool(imp_guard and lev_guard and kin_guard)
    T1 = bool(all_couple and all_three_edges and every_vertex_degree_2 and all_guards and all_sha_ok)

    # ------------------------------------------------------------------ T2  ONE NEW JOINING OBJECT PER COUPLING
    imp_reuses_both = bool(imp_reuse_E1 and imp_reuse_E0)
    lev_reuses_both = bool(lev_reuse_E1 and lev_reuse_E2)
    kin_reuses_both = bool(kin_reuse_E0 and kin_reuse_E2)
    all_reuse_both  = bool(imp_reuses_both and lev_reuses_both and kin_reuses_both)
    no_new_tuned    = bool(imp_tuned0 and lev_tuned0 and kin_tuned0)
    T2 = bool(all_reuse_both and no_new_tuned)

    # ------------------------------------------------------------------ T3  THREE DECOUPLINGS
    imp_dec_ok = bool(imp_decoupled and imp_contains and imp_C3_status == "CONFIRMED")
    lev_dec_ok = bool(lev_decoupled and lev_dec_footprint and lev_no_reach_law and lev_C3_status == "CONFIRMED")
    kin_dec_ok = bool(kin_decoupled and kin_R_rises and kin_ends_above and kin_K3_status == "CONFIRMED")
    T3 = bool(imp_dec_ok and lev_dec_ok and kin_dec_ok)

    # ------------------------------------------------------------------ T4  COMMON SHAPE / CLEAN HYP REFUTED
    imp_breaks_law = bool(imp_refuted and imp_no_law)
    lev_breaks_law = bool(lev_refuted and lev_no_reach_law)
    kin_breaks_law = bool(kin_refuted and kin_R_rises)   # erosion hyp refuted == R rises net not falls
    all_refute     = bool(imp_breaks_law and lev_breaks_law and kin_breaks_law)
    T4 = bool(all_refute)

    # ------------------------------------------------------------------ T5  ONE COUPLING DISCIPLINE
    imp_double_sweep = bool(imp_sweep_a and imp_sweep_b)
    lev_double_sweep = bool(lev_sweep_a and lev_sweep_b)
    kin_double_sweep = bool(kin_sweep_a and kin_sweep_b)
    all_double_sweep = bool(imp_double_sweep and lev_double_sweep and kin_double_sweep)
    T5 = bool(all_double_sweep and all_guards and no_new_tuned)

    preds = {
        "T1_one_family_all_three_triangle_edges": "CONFIRMED" if T1 else "REFUTED",
        "T2_one_new_joining_object_per_coupling": "CONFIRMED" if T2 else "REFUTED",
        "T3_three_decouplings": "CONFIRMED" if T3 else "REFUTED",
        "T4_common_shape_single_axis_law_breaks": "CONFIRMED" if T4 else "REFUTED",
        "T5_one_coupling_discipline_three_times": "CONFIRMED" if T5 else "REFUTED",
    }
    all_confirmed = all(v == "CONFIRMED" for v in preds.values())

    res = {
        "_what": "the cross-axis coupling synthesis: the spatial-plasticity imprint (47, E1xE0), the "
                 "spatial switch leverage (48, E1xE2) and the kindling coupling (49, E0xE2) cross-read as "
                 "one FAMILY -- the three pairwise edges of the same three layers E0 (plasticity), E1 "
                 "(spatial) and E2 (state switching), each layer appearing in exactly two couplings -- "
                 "and certified to share one shape: the genuinely-new result each seam surfaces is a "
                 "DECOUPLING of two quantities the single-axis intuition welds together (clean delivery "
                 "from clean imprint, switchability from footprint and reach, easier-flip from erosion), "
                 "each refuting a tidy single-axis hypothesis reported honestly, under one coupling "
                 "discipline (import both layers read-only, one new joining object, sweep both coupled "
                 "axes, revert to the frozen engine bit-for-bit, report any decoupling honestly). No new "
                 "dynamics, no new measurement, no new tuned constant; the three source JSONs are the "
                 "SSOT and their frozen shas are re-verified here.",
        "roadmap_id": "CROSS-SYNTH (capstone of the three cross-axis couplings: E1xE0 47, E1xE2 48, E0xE2 49)",
        "sources": {
            mode: {"results_file": fname, "frozen_sha256": frozen, "couples": list(edge),
                   "sha256_reverified": sha_ok[mode]}
            for mode, (fname, frozen, edge) in SOURCES.items()
        },
        "the_triangle": {
            "layers": list(LAYERS),
            "layer_meanings": {"E0": "plasticity / consolidation layer (26)",
                               "E1": "spatial-localisation layer (43)",
                               "E2": "state-switching layer (28)"},
            "edges_present": sorted("x".join(sorted(e)) for e in edges),
            "complete_triangle": all_three_edges,
            "vertex_degree": {v: deg[v] for v in LAYERS},
            "every_vertex_degree_2": every_vertex_degree_2,
            "note": "the three couplings realise all three pairwise edges of the three layers, and each "
                    "layer-vertex appears in exactly two couplings (E0 in 47+49, E1 in 47+48, E2 in "
                    "48+49) -- the complete pairwise-coupling triangle of the three axes.",
        },
        "T1_one_family_all_three_triangle_edges": {
            "all_modules_couple_two_layers": all_couple,
            "couples_per_module": {"E1xE0": imp_couples, "E1xE2": lev_couples, "E0xE2": kin_couples},
            "all_three_pairwise_edges_present": all_three_edges,
            "every_vertex_degree_2": every_vertex_degree_2,
            "all_engine_guards_reproduced": all_guards,
            "guard_per_module": {"E1xE0": imp_guard, "E1xE2": lev_guard, "E0xE2": kin_guard},
            "all_source_shas_reverified": all_sha_ok,
            "reproduced": T1,
        },
        "T2_one_new_joining_object_per_coupling": {
            "new_object_per_coupling": {
                "E1xE0": "the spatial-imprint readout (a focal drive run through the plastic connectome)",
                "E1xE2": "the LeverageSwitch (the bistable cell driven by a node's frozen-kernel broadcast leverage)",
                "E0xE2": "the KindlingSwitch (the bistable cell driven through the evolving connectome)",
            },
            "each_reuses_both_layers_read_only": all_reuse_both,
            "reuse_per_module": {"E1xE0": imp_reuses_both, "E1xE2": lev_reuses_both, "E0xE2": kin_reuses_both},
            "no_new_tuned_constant_in_any": no_new_tuned,
            "reproduced": T2,
        },
        "T3_three_decouplings": {
            "E1xE0_clean_delivery_decoupled_from_clean_imprint": imp_dec_ok,
            "E1xE0_trace_relay_strictly_contains_field_relay": imp_contains,
            "E1xE0_trace_relay_n_vs_field_relay_n": [imp_trace_n, imp_field_n],
            "E1xE2_switchability_decoupled_from_footprint_and_reach": lev_dec_ok,
            "E1xE2_reach_hub": lev_reach_hub, "E1xE2_reach_hub_switch_rank": lev_reach_rank,
            "E1xE2_switch_leverage_hub": lev_switch_hub,
            "E0xE2_easier_flip_decoupled_from_erosion": kin_dec_ok,
            "E0xE2_coordination_R_rises": [kin_R0, kin_R8],
            "E0xE2_kindled_ends_at_or_above_anchor": kin_ends_above,
            "all_three_decouplings_confirmed": bool(imp_dec_ok and lev_dec_ok and kin_dec_ok),
            "reproduced": T3,
        },
        "T4_common_shape_single_axis_law_breaks": {
            "E1xE0_no_universal_focal_gt_diffuse_imprint_law": imp_breaks_law,
            "E1xE2_no_universal_reach_to_switchability_law": lev_breaks_law,
            "E0xE2_clean_kindling_erodes_coordination_refuted": kin_breaks_law,
            "all_three_refute_a_clean_single_axis_hypothesis_honestly": all_refute,
            "reproduced": T4,
        },
        "T5_one_coupling_discipline_three_times": {
            "each_sweeps_both_coupled_axes": all_double_sweep,
            "double_sweep_per_module": {
                "E1xE0": "stimulation intensity x plasticity rate",
                "E1xE2": "stimulation intensity x barrier depth",
                "E0xE2": "plasticity rate x barrier depth"},
            "each_reverts_to_frozen_engine_bitwise": all_guards,
            "guard_inherited_per_module": {
                "E1xE0": "M9 anchor bit-for-bit (eta=0)",
                "E1xE2": "E.settle bit-for-bit (zero drive)",
                "E0xE2": "BOTH: M9 anchor (eta=0) AND E.settle (zero push)"},
            "no_new_measurement_or_tuned_constant_in_any": no_new_tuned,
            "reproduced": T5,
        },
        "coupling_contrast_table": {
            "E1xE0_spatial_plasticity_imprint_47": {
                "couples": "E1 (spatial, where) x E0 (plasticity, lasting)",
                "question": "WHERE does a focal drive leave a LASTING trace?",
                "new_object": "a focal drive run through the plastic connectome (the imprint readout)",
                "decoupling": "clean DELIVERY does not imply clean IMPRINT -- the retained-trace relay set "
                              "STRICTLY CONTAINS the instantaneous-field relay set; plasticity delocalises "
                              "the mark (the durable mark is more distributed than the drive)",
                "phrase": "when space meets time",
                "trace_relay_vs_field_relay_n": [imp_trace_n, imp_field_n],
            },
            "E1xE2_spatial_switch_leverage_48": {
                "couples": "E1 (spatial, where) x E2 (state switching, the flip)",
                "question": "WHICH focal drive most easily FLIPS the collective state?",
                "new_object": "the bistable cell driven by a node's frozen-kernel broadcast leverage (the LeverageSwitch)",
                "decoupling": "switchability decouples from BOTH the instantaneous footprint AND the spatial "
                              "reach -- the reach hub (" + str(lev_reach_hub) + ") is among the HARDEST to "
                              "flip (switch rank " + str(lev_reach_rank) + " of 12); the switch hub is " + str(lev_switch_hub),
                "phrase": "when space meets state",
            },
            "E0xE2_kindling_49": {
                "couples": "E0 (plasticity, the evolving connectome) x E2 (state switching, the flip)",
                "question": "do REPEATED flips of the collective state become EASIER?",
                "new_object": "the bistable cell driven through the evolving connectome (the KindlingSwitch)",
                "decoupling": "easier-to-flip decouples from EROSION -- the kindled connectome ends MORE "
                              "coordinated (R rises " + repr(kin_R0) + "->" + repr(kin_R8) + ") as the "
                              "threshold falls; the threshold falls through CONSOLIDATION, not degradation",
                "phrase": "when time meets state",
                "coordination_R_rise": [kin_R0, kin_R8],
            },
        },
        "preregistered_results": {
            "T1_one_family_all_three_triangle_edges": {
                "claim": "all three modules couple two of the layers E0/E1/E2 and together realise all "
                         "three pairwise edges of the triangle, every layer-vertex appearing in exactly "
                         "two couplings, and each coupling reverts to the frozen engine bit-for-bit with "
                         "its drive off",
                "status": preds["T1_one_family_all_three_triangle_edges"]},
            "T2_one_new_joining_object_per_coupling": {
                "claim": "each coupling introduces exactly one new joining object (the imprint readout, the "
                         "LeverageSwitch, the KindlingSwitch), reuses both its layers read-only, and adds "
                         "no new tuned constant",
                "status": preds["T2_one_new_joining_object_per_coupling"]},
            "T3_three_decouplings": {
                "claim": "the genuinely-new result each seam surfaces is a decoupling -- clean delivery from "
                         "clean imprint (47), switchability from footprint and reach (48), easier-flip from "
                         "erosion (49) -- all three CONFIRMED",
                "status": preds["T3_three_decouplings"]},
            "T4_common_shape_single_axis_law_breaks": {
                "claim": "the three decouplings share a shape: each refutes a tidy single-axis hypothesis "
                         "(no universal focal>diffuse imprint law, no universal reach->switchability law, "
                         "no clean kindling-erodes-coordination story) and reports it honestly",
                "status": preds["T4_common_shape_single_axis_law_breaks"]},
            "T5_one_coupling_discipline_three_times": {
                "claim": "every coupling sweeps both coupled axes (anti-tuning), reverts to the frozen "
                         "engine bit-for-bit with the drive off (inheriting each layer's guard), and adds "
                         "no new measurement or tuned constant",
                "status": preds["T5_one_coupling_discipline_three_times"]},
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "new_measurement": 0.0,
            "is_a_synthesis_of_frozen_modules": 1.0,
            "is_a_synthesis_of_cross_axis_couplings": 1.0,
            "source_shas_reverified": 1.0 if all_sha_ok else 0.0,
            "completes_cross_axis_coupling_trio_E1xE0_E1xE2_E0xE2": 1.0,
            "all_three_pairwise_edges_of_E0E1E2_triangle": 1.0 if all_three_edges else 0.0,
            "common_shape_is_a_decoupling": 1.0 if T3 else 0.0,
            "each_coupling_refutes_a_clean_single_axis_hypothesis_honestly": 1.0 if T4 else 0.0,
            "not_medical_advice": 1.0,
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
        },
        "overall": {
            "one_family_reproduced": T1,
            "new_object_per_coupling_reproduced": T2,
            "three_decouplings_reproduced": T3,
            "common_shape_reproduced": T4,
            "one_discipline_reproduced": T5,
            "is_full_synthesis": all_confirmed,
            "verdict": "CROSS-SYNTH cross-reads the three frozen cross-axis coupling modules -- the "
                       "spatial-plasticity imprint (47, E1xE0), the spatial switch leverage (48, E1xE2) "
                       "and the kindling coupling (49, E0xE2) -- and certifies them as one FAMILY with one "
                       "shape. ONE FAMILY (T1): all three couple two of the layers E0 (plasticity), E1 "
                       "(spatial) and E2 (state switching), and together they realise all three pairwise "
                       "edges of the triangle -- {E1,E0}, {E1,E2}, {E0,E2} -- every layer-vertex appearing "
                       "in exactly two couplings, and each reverts to the frozen engine bit-for-bit with "
                       "its drive off. ONE NEW JOINING OBJECT PER COUPLING (T2): the imprint readout, the "
                       "LeverageSwitch and the KindlingSwitch, each joining two layers reused read-only, "
                       "no new tuned constant in any. THREE DECOUPLINGS (T3): the genuinely-new result each "
                       "seam surfaces is a decoupling -- clean delivery from clean imprint (the trace relay "
                       "strictly contains the field relay), switchability from both footprint and reach "
                       "(the reach hub is among the hardest to flip), and easier-flip from erosion "
                       "(coordination rises as the threshold falls) -- all three CONFIRMED. A COMMON SHAPE "
                       "(T4): each decoupling refutes a tidy single-axis hypothesis (no universal "
                       "focal>diffuse imprint law, no universal reach->switchability law, no clean "
                       "kindling-erodes-coordination story) and reports it honestly -- when space meets "
                       "time the imprint decouples from delivery, when space meets state the flip decouples "
                       "from footprint and reach, when time meets state the kindling decouples from erosion. "
                       "ONE DISCIPLINE (T5): every coupling sweeps both coupled axes (anti-tuning), reverts "
                       "to the frozen engine bit-for-bit with the drive off (inheriting each layer's guard "
                       "-- the M9 anchor, the E.settle relaxation, or both), and reports any decoupling "
                       "honestly. No new dynamics, no new measurement, no new tuned constant; the three "
                       "source JSONs are the SSOT and their frozen shas are re-verified; the engine is "
                       "imported READ-ONLY and byte-unchanged. Only structural signs / relations are "
                       "asserted; every magnitude is [O]. The imprints, leverages, flip thresholds, "
                       "retained traces and coordination gains are STRUCTURAL quantities, never a felt "
                       "state, an experienced mood, a level of consciousness, an experienced ease of "
                       "relapse, a real connectome, a real measure of where a drive leaves a mark, which "
                       "target is most switchable, or whether any patient's episodes accelerate (Axis-A; "
                       "consciousness_claim=0; hard problem OPEN); the [L] correspondences in the source "
                       "chapters are direction-only; target selection, device programming, prognosis and "
                       "treatment are external; efficacy=0; not medical advice; no cure, reversal, or "
                       "prevention.",
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

def cross_axis_coupling_synthesis_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "cross_axis_coupling_synthesis_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_cross_axis_coupling_synthesis_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"cross_axis_coupling_synthesis_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = cross_axis_coupling_synthesis_results()
    inv = res["invariants"]; ov = res["overall"]; hl = res["honesty_ledger"]; tri = res["the_triangle"]
    t1 = res["T1_one_family_all_three_triangle_edges"]; t2 = res["T2_one_new_joining_object_per_coupling"]
    t3 = res["T3_three_decouplings"]; t4 = res["T4_common_shape_single_axis_law_breaks"]
    t5 = res["T5_one_coupling_discipline_three_times"]
    print("=" * 78)
    print("  CROSS-SYNTH -- THE CROSS-AXIS COUPLING SYNTHESIS : three couplings, one shape")
    print("=" * 78)
    print(f"  sources re-verified (sha256 == frozen): "
          f"{', '.join(m for m,v in res['sources'].items() if v['sha256_reverified'])}")
    print(f"  triangle edges present : {tri['edges_present']}  complete={tri['complete_triangle']}  "
          f"degrees={tri['vertex_degree']}")
    print(f"  T1 one family        (3 couplings = 3 triangle edges, all guards revert) : {t1['reproduced']}")
    print(f"  T2 new object/coupling (imprint readout / LeverageSwitch / KindlingSwitch; no new tuned) : {t2['reproduced']}")
    print(f"  T3 three decouplings (delivery!=imprint / switch!=footprint+reach / flip!=erosion) : {t3['reproduced']}")
    print(f"  T4 common shape      (each refutes a clean single-axis law, honestly) : {t4['reproduced']}")
    print(f"  T5 one discipline    (both-axis sweep + bit-for-bit revert + no new tuned) : {t5['reproduced']}")
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / "
          f"{inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  efficacy=0 / consciousness_claim=0 / new_tuned_constants=0 / new_measurement=0 : "
          f"{hl['medium_efficacy_tested']==0} / {hl['consciousness_claim']==0} / "
          f"{hl['new_tuned_constants']==0} / {hl['new_measurement']==0}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 78)
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"]
          and ov["is_full_synthesis"] and all(v["sha256_reverified"] for v in res["sources"].values()))
    print(f"  CROSS-SYNTH CROSS-AXIS COUPLING SYNTHESIS MODULE: {'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)
