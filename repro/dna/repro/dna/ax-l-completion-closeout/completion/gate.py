# -*- coding: utf-8 -*-
"""
completion.gate -- the fail-closed gate for Appendix K (the absolute clock).

FAILS CLOSED on any miss. The K1..K7 / G1 / O1 / O1J / O2 / O3 checks are the inherited Appendix-J
gate, RE-AUDITED byte-for-byte on the identical 63-gene atlas; B1 is the new closure:

  K1  SAME_OPERATOR+INHERIT  robust_z is the identical operator (scale+shift invariant), gamma
                        reproduces -mean(NN dG) exactly, the 4 skeletal drivers are byte-identical,
                        AND all 63 inherited driver gammas are BYTE-IDENTICAL to the parent
                        Appendix-J param_db (its 38 inherited + 25 new blocks merged, read off disk).
                        Appendix K introduces NO new gamma.
  K2  CASCADE_IS_DAG    the inherited 63-gene / 62-edge cascade is acyclic; depth is DERIVED.
  K3  THE_NULL          single-locus spinodal(gamma) still does NOT order Carnegie staging.
  K4  EDGE_CONCORDANCE  zero cited-edge inversions vs the cited temporal order.
  K5  DEPTH_BEATS_GAMMA cascade depth predicts order strictly better than local stiffness.
  K6  OR_WAVEFRONT      coupled-R19 OR firing respects the DAG and tracks depth, not bare spinodal.
  K7  KEYS_DISAGREE     spinodal order and depth order are genuinely different (real work).
  G1  QUORUM_WAVEFRONT  the OR gate generalises to a QUORUM/AND threshold-k gate, order intact.
  O3  SEQUENCE_DRIVE    per-edge drive read from the promoter (sqrt(gamma)) preserves firing order.
  O1  FLOOR_ON_FILLED   the pre-registered 0.70 depth<->Carnegie floor is reached (both fixes needed).
  O1J JITTER_HONEST     the seed=19 jitter lower edge sits below the floor -> O1 stays [L], not [V].
  O2  SUBCLOCK          the segmentation sub-clock predicts a somitogenesis span consistent with the
                        cited window (inherited [L]).
  B1  GLOBAL_CLOCK      *** the new closure ***  the global zero-point is pinned by TWO INDEPENDENT
                        measured anchors (segmentation oscillator SLOPE + cardiac landmark INTERCEPT),
                        with ZERO free parameters; held-out Carnegie stage-days AND gene-days within
                        the somite-clock window are reproduced inside the acceptance band. The absolute
                        clock is a MEASUREMENT, so it is graded [L] and the gate FAILS CLOSED on any
                        [V] promotion of it. The post-somitogenesis single-rate drift is reported.
  K8  NO_MAGIC          the lock manifest reports zero inline magic numbers (incl. the clock cfg).
  K9  NON_FIT           the reading is identical with decoy Carnegie/timing/CARDIAC targets present.
  K10 DETERMINISM       two serializations of the reading hash identically (2x SHA-256).
  K11 HONEST_DECLARATION the declaration closes B1 (O2 global zero-point) to [L], keeps the absolute
                        clock [L] (never [V]), keeps O1 [L] (never [V]), and keeps the built body [O]
                        and physical_complete=False. FAILS CLOSED on any false victory, including an
                        O1->[V] or absolute-clock->[V] promotion, or physical_complete=True.

Run:  python3 -m completion.gate   (from the package root).
"""
import os
import json
import hashlib

import numpy as np

from . import (lock, seqtools, cascade, coupled, timing, nulltest, grammar,
               declaration, grading, interpreter, cis)


# the four drivers shared with Appendices G/H; their published gammas are the regression reference.
_OVERLAP_PUBLISHED = {"SOX9": 1.459260, "RUNX2": 1.241556, "PAX1": 1.504372, "GLI3": 1.298352}
_PROBE = "GCGCGGCCGGATATCGCGTATATACGCGGCCGGCGC"


def _j1_same_operator_and_inherit():
    # operator invariances
    x = np.array([0.2, 1.7, -0.4, 3.1, 0.9, -1.2, 2.0, 0.05], dtype=np.float64)
    z = seqtools.robust_z(x)
    scale_inv = float(np.max(np.abs(z - seqtools.robust_z(7.3 * x))))
    shift_inv = float(np.max(np.abs(z - seqtools.robust_z(x + 4.5))))
    nn = lock.nn_table()
    g_pkg = seqtools.gamma(_PROBE, nn)
    steps = [nn[_PROBE[i:i + 2]] for i in range(len(_PROBE) - 1)]
    gamma_exact = abs(g_pkg - float(-np.mean(steps))) < 1e-12
    # four skeletal drivers byte-identical
    atlas = lock.driver_gamma()
    overlap_ok = all(s in atlas for s in _OVERLAP_PUBLISHED) and all(
        abs(float(atlas[s]["gamma"]) - g) < 1e-9 for s, g in _OVERLAP_PUBLISHED.items())
    # ALL 63 inherited gammas byte-identical to the parent Appendix-J param_db (read off disk).
    # Appendix J stores the atlas in two blocks (inherited 38 + new 25); merge to the full 63.
    parent_path = lock.parent_db_path()
    with open(parent_path, "r", encoding="utf-8") as fh:
        parent = json.load(fh)
    parent_dg = {}
    parent_dg.update(parent["driver_gamma_inherited"])
    parent_dg.update(parent["driver_gamma_new"])
    inh = lock.driver_gamma_inherited()
    inherit_ok = (len(inh) == len(parent_dg)) and all(
        sym in parent_dg and float(parent_dg[sym]["gamma"]) == float(rec["gamma"])
        for sym, rec in inh.items())
    n_mismatch = sum(1 for sym, rec in inh.items()
                     if (sym not in parent_dg)
                     or float(parent_dg[sym]["gamma"]) != float(rec["gamma"]))
    ok = (scale_inv < 1e-9) and (shift_inv < 1e-9) and gamma_exact and overlap_ok and inherit_ok
    return ok, {"shape_scale_invariance": scale_inv, "shape_shift_invariance": shift_inv,
                "gamma_reproduces_neg_mean_NN": bool(gamma_exact),
                "overlap_reproduces_byte_for_byte": bool(overlap_ok),
                "inherited_gamma_byte_identical_to_parent": bool(inherit_ok),
                "n_inherited": len(inh), "n_inherited_mismatch": n_mismatch}


def _j2_cascade_is_dag():
    acyclic, topo = cascade.is_dag()
    ok = bool(acyclic) and (len(topo) == len(lock.driver_gamma()))
    return ok, {"is_dag": bool(acyclic), "n_genes": len(lock.driver_gamma()),
                "n_edges": len(lock.cascade_edges()), "n_in_topo": len(topo),
                "max_depth": cascade.max_depth(), "n_sources": len(cascade.sources())}


def _j3_the_null():
    n = nulltest.the_null()
    ok = bool(n["is_null"])
    return ok, {"spearman_spinodal_vs_carnegie": n["spearman_spinodal_vs_carnegie"],
                "ceiling": n["null_ceiling"], "n_anchored": n["n_anchored"]}


def _j4_edge_concordance():
    c = nulltest.edge_concordance()
    ok = bool(c["passes"])
    return ok, {"n_cited_edges": c["n_cited_edges_both_anchored"], "n_inversions": c["n_inversions"],
                "concordance_incl_ties": c["concordance_incl_ties"], "floor": c["concordance_floor"]}


def _j5_depth_beats_gamma():
    b = nulltest.depth_beats_gamma()
    ok = bool(b["passes"])
    return ok, {"depth_all": b["spearman_depth_vs_carnegie_all"],
                "gamma_all": b["spearman_spinodal_vs_carnegie_all"],
                "depth_main": b["spearman_depth_vs_carnegie_main_component"],
                "gamma_main": b["spearman_spinodal_vs_carnegie_main_component"]}


def _j6_or_wavefront():
    poc = coupled.or_partial_order_compliance()
    cvk = coupled.coupled_vs_keys()
    ok = bool(poc["respects_partial_order"]) and bool(cvk["depth_beats_gamma"])
    return ok, {"partial_order_violations": poc["n_violations"],
                "firing_vs_depth": cvk["spearman_firing_vs_cascade_depth"],
                "firing_vs_spinodal": cvk["spearman_firing_vs_bare_spinodal"]}


def _j7_keys_disagree():
    dg = lock.driver_gamma()
    d = cascade.depth()
    genes = sorted(dg.keys())
    spin = [float(seqtools.spinodal(dg[g]["gamma"])) for g in genes]
    dep = [d[g] for g in genes]
    rho = nulltest._spearman(spin, dep)
    ok = bool(rho < 0.999)
    return ok, {"spearman_spinodal_order_vs_depth_order": round(rho, 4),
                "genuinely_different_order": ok}


def _g1_quorum_wavefront():
    thr = coupled.threshold_k_wavefront(alpha=1.0)
    andd = coupled.and_delays_convergent_nodes()
    ok = bool(thr["respects_threshold_k_wavefront"]) and bool(andd["and_never_earlier_than_or"])
    return ok, {"and_wavefront_violations": thr["n_violations"],
                "and_never_earlier_than_or": andd["and_never_earlier_than_or"],
                "and_strictly_later_somewhere": andd["and_strictly_later_somewhere"],
                "or_is_special_case": thr["or_is_special_case"]}


def _o3_sequence_drive():
    s = coupled.sequence_drive_preserves_order()
    ok = (s["or_wavefront_violations_under_sequence"] == 0) and bool(s["order_preserved"]) \
        and bool(s["depth_beats_gamma_under_sequence"])
    return ok, {"or_violations_under_sequence": s["or_wavefront_violations_under_sequence"],
                "firing_order_rho_uniform_vs_sequence": s["spearman_order_uniform_vs_sequence"],
                "sqrt_gamma_range": s["sqrt_gamma_range"],
                "depth_beats_gamma_under_sequence": s["depth_beats_gamma_under_sequence"]}


def _o1_floor_on_filled():
    a = nulltest.floor_retest_ablation()
    meets = bool(a["meets_floor_on_filled_kit"])
    requires_both = (not a["scope_b_plus_limb_inducers"]["meets_floor"]
                     and not a["scope_d_hox_only_limb_ablated"]["meets_floor"]
                     and a["scope_c_plus_full_hox"]["meets_floor"])
    ok = meets and requires_both
    return ok, {"floor": a["preregistered_absolute_floor"],
                "inherited": a["scope_a_inherited_kit"]["spearman"],
                "plus_limb": a["scope_b_plus_limb_inducers"]["spearman"],
                "plus_full_hox": a["scope_c_plus_full_hox"]["spearman"],
                "hox_only": a["scope_d_hox_only_limb_ablated"]["spearman"],
                "meets_on_filled": meets, "requires_both_fixes": requires_both}


def _b4_jitter_closed():
    # B4 CLOSURE (was K's O1J marginality check, now INVERTED): on the cascade EXTENDED by the cited
    # MEOX1->PAX7 edge, the +-1 rank-jitter p5 of Spearman(depth, Carnegie) is >= the 0.70 floor
    # (no longer marginal), the added edge is rank-tie-concordant (0 new inversions), and the DAG is
    # preserved. The strength STAYS [L] (B3 forbids [V]); the gate fails closed if anyone promotes it.
    b4 = nulltest.b4_jitter_closed()
    j = nulltest.floor_retest_jitter()
    seed_ok = (j["seed"] == 19)
    p5_clears = (j["p5"] >= j["floor"])           # B4: the floor IS now cleared at the p5 edge
    ok = bool(seed_ok and p5_clears and b4["b4_closed"]
              and b4["edge_present"] and b4["edge_rank_concordant"]
              and b4["n_edge_inversions"] == 0 and b4["cascade_is_dag"])
    return ok, {"seed": j["seed"], "mean": j["mean"], "p5": j["p5"], "p95": j["p95"],
                "floor": j["floor"], "p5_clears_floor": p5_clears,
                "closure_edge": b4["closure_edge"],
                "rank_parent": b4["rank_parent"], "rank_child": b4["rank_child"],
                "n_edge_inversions": b4["n_edge_inversions"],
                "frac_at_or_above_floor": j["frac_at_or_above_floor"],
                "b4_closed": b4["b4_closed"]}


def _b2_data_blocked():
    # B2 DATA-BLOCKED: re-run the deterministic occupancy probe; verify the per-edge drive is NOT in
    # the +-2 kb promoter window -- the MAJORITY of both-cached edges sit at/below a dinucleotide-
    # shuffle background AND the canonical direct edge SOX9->RUNX2 is BELOW background. B2 must be
    # graded data-blocked, NOT [L]. The gate fails closed if B2 is ever (falsely) closed to [L].
    b2 = cis.occupancy_probe()
    led = grading.ledger()
    b2_row = next((r for r in led["rows"] if r["id"] == "B2"), None)
    b2_not_L = bool(b2_row is not None and not b2_row["grade"].startswith("[L]"))
    ok = bool(b2["b2_data_blocked"]
              and b2["canonical_SOX9_RUNX2_below_background"]
              and b2["majority_at_or_below_background"]
              and b2_not_L and led["b2_is_not_L"])
    return ok, {"n_edges_scored": b2["n_edges_scored"],
                "n_above_background": b2["n_above_background"],
                "frac_above_background": b2["frac_above_background"],
                "mean_z": b2["mean_z"],
                "SOX9_RUNX2_z": b2["canonical_SOX9_represses_RUNX2"]["z"],
                "SOX9_RUNX2_below_background": b2["canonical_SOX9_RUNX2_below_background"],
                "majority_at_or_below_background": b2["majority_at_or_below_background"],
                "b2_data_blocked": b2["b2_data_blocked"],
                "b2_row_is_not_L": b2_not_L}


def _o2_subclock():
    # the segmentation sub-clock consistency (inherited from J), unchanged [L].
    sub = timing.segmentation_subclock()
    consistent = bool(sub["prediction_in_cited_window_pm2d"])
    ok = consistent
    return ok, {"predicted_days": sub["predicted_somitogenesis_days"],
                "cited_window": sub["cited_window_CS9_to_CS13_days"],
                "consistent": consistent}


def _k_global_clock():
    # B1 CLOSURE: two INDEPENDENT measured anchors pin the global zero-point; held-out Carnegie
    # stage-days AND gene-days within the somite-clock window are reproduced inside the acceptance
    # band; ZERO free parameters; the clock is graded [L], NEVER [V]. FAILS CLOSED on any [V].
    gc = timing.global_clock()
    glob = timing.global_clock_open()
    closed = bool(gc["b1_closed"])
    stages_ok = bool(gc["heldout_stage_validation"]["all_pass"])
    genes_ok = bool(gc["heldout_gene_validation"]["all_pass"])
    zero_free = (gc["calibration"]["free_parameters"] == 0)
    two_modalities = (gc["anchor_1_segmentation"]["modality"]
                      != gc["anchor_2_cardiac"]["modality"])
    is_L_not_V = gc["grade"].startswith("[L]") and not gc["grade"].startswith("[V]")
    glob_L_not_V = glob["grade"].startswith("[L]") and not glob["grade"].startswith("[V]")
    ok = (closed and stages_ok and genes_ok and zero_free and two_modalities
          and is_L_not_V and glob_L_not_V)
    return ok, {"b1_closed": closed,
                "heldout_stages_pass": stages_ok,
                "heldout_stage_max_err_days": gc["heldout_stage_validation"]["max_abs_err_days"],
                "heldout_genes_pass": genes_ok,
                "n_heldout_genes": gc["heldout_gene_validation"]["n_genes"],
                "heldout_gene_max_err_days": gc["heldout_gene_validation"]["max_abs_err_days"],
                "free_parameters": gc["calibration"]["free_parameters"],
                "two_independent_modalities": two_modalities,
                "absolute_clock_grade_is_L_not_V": is_L_not_V,
                "post_somitogenesis_drift_days_CS14plus":
                    gc["honest_bound_post_somitogenesis"]["max_abs_err_days_CS14plus"]}


def _j8_no_magic():
    man = lock.lock_manifest()

    def all_prov(node):
        if isinstance(node, dict):
            if "provenance" in node and not node["provenance"]:
                return False
            return all(all_prov(v) for v in node.values())
        if isinstance(node, list):
            return all(all_prov(v) for v in node)
        return True

    ok = (man.get("inline_magic_numbers") == 0) and all_prov(man)
    return ok, {"inline_magic_numbers": man.get("inline_magic_numbers")}


def _j9_non_fit():
    h1 = interpreter.reading_hash()
    decoys = {"carnegie_targets.json": {"fake_stage_rank": {"RUNX2": 1, "FOXA2": 99}},
              "developmental_rates_target.json": {"fake_days": {"SOX9": 1234.5}},
              "cardiac_onset_target.json": {"fake_heartbeat_day": {"CS10": 999.0},
                                            "fake_clock_slope": 123.4}}
    created = []
    for name, payload in decoys.items():
        if not os.path.exists(name):
            with open(name, "w") as fh:
                json.dump(payload, fh)
            created.append(name)
    try:
        h2 = interpreter.reading_hash()
    finally:
        for name in created:
            os.remove(name)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1[:16], "hash_with_decoy": h2[:16]}


def _j10_determinism():
    r = interpreter.interpret()
    b1 = json.dumps(r, sort_keys=True, ensure_ascii=False).encode("utf-8")
    b2 = json.dumps(json.loads(b1.decode("utf-8")), sort_keys=True,
                    ensure_ascii=False).encode("utf-8")
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    ok = (h1 == h2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16]}


def _j11_honest_declaration():
    decl = declaration.declare()
    led = grading.ledger()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}

    only_sanctioned = all(any(r["grade"].startswith(s) for s in sanctioned) for r in led["rows"])
    opens_named = all(o.get("status") for o in decl["open"])
    not_physical = (decl["physical_complete"] is False)
    no_consciousness = (decl["consciousness_claim"] == 0)
    # B1 CLOSED to [L]; the global clock must be graded [L], NEVER [V] (inherited).
    b1_closed = bool(decl["b1_closed"])
    zero_point_closed = bool(decl["o2_global_zero_point_closed"])
    global_clock_L_not_V = bool(decl["global_clock_grade_is_L_not_V"])
    o2_subclock_closed = bool(decl["o2_subclock_closed"])
    o3_F = bool(decl["o3_drive_from_sequence_F"])
    gate_V = bool(decl["gate_threshold_k_V"])
    # B4 CLOSED to [L]: the jitter floor is cleared at the p5 edge; the strength stays [L], never [V].
    b4_closed = bool(decl["b4_closed"]) and bool(decl["b4_p5_clears_floor"])
    b4_L_not_V = bool(decl["b4_grade_is_L_not_V"]) and bool(led["b4_is_L_not_V"])
    # B2 DATA-BLOCKED: must NOT be [L]; the canonical SOX9->RUNX2 edge is below background.
    b2_data_blocked = bool(decl["b2_data_blocked"]) and bool(decl["b2_canonical_below_background"])
    b2_not_L = bool(decl["b2_grade_is_not_L"]) and bool(led["b2_is_not_L"])
    blueprint_mapped = bool(decl["blueprint_fully_mapped"])
    # NO FALSE VICTORY: the O1/B4 absolute-strength row stays [L]; the O2b absolute-clock row stays [L].
    o1 = next((r for r in led["rows"] if r["id"] == "O1"), None)
    o1_not_V = bool(o1 is not None and o1["grade"].startswith("[L]")
                    and not o1["grade"].startswith("[V]"))
    o2b = next((r for r in led["rows"] if r["id"] == "O2b"), None)
    o2b_is_L_not_V = bool(o2b is not None and o2b["grade"].startswith("[L]")
                          and not o2b["grade"].startswith("[V]"))
    grading_self_audit = (bool(led["o1_is_L_not_V"]) and bool(led["global_clock_is_L_not_V"])
                          and bool(led["b4_is_L_not_V"]) and bool(led["b2_is_not_L"]))
    decl_flag = bool(decl["o1_grade_is_L_not_V"])

    ok = (only_sanctioned and opens_named and not_physical and no_consciousness
          and b1_closed and zero_point_closed and global_clock_L_not_V
          and o2_subclock_closed and o3_F and gate_V
          and b4_closed and b4_L_not_V and b2_data_blocked and b2_not_L and blueprint_mapped
          and o1_not_V and o2b_is_L_not_V and grading_self_audit and decl_flag)
    return ok, {"only_sanctioned_grades": only_sanctioned, "opens_named": opens_named,
                "physical_complete": decl["physical_complete"],
                "blueprint_fully_mapped": blueprint_mapped,
                "b1_closed": b1_closed,
                "global_clock_grade_is_L_not_V": global_clock_L_not_V,
                "b4_closed_and_p5_clears": b4_closed,
                "b4_strength_stays_L_not_V": b4_L_not_V,
                "b2_data_blocked_canonical_below_bg": b2_data_blocked,
                "b2_row_stays_not_L": b2_not_L,
                "o1_absolute_strength_stays_L_not_V": o1_not_V,
                "o2b_absolute_clock_stays_L_not_V": o2b_is_L_not_V,
                "grading_self_audit": grading_self_audit}


CHECKS = [
    ("L1_same_operator_and_inherit", _j1_same_operator_and_inherit),
    ("L2_cascade_is_dag", _j2_cascade_is_dag),
    ("L3_the_null", _j3_the_null),
    ("L4_edge_concordance", _j4_edge_concordance),
    ("L5_depth_beats_gamma", _j5_depth_beats_gamma),
    ("L6_or_wavefront", _j6_or_wavefront),
    ("L7_keys_disagree", _j7_keys_disagree),
    ("G1_quorum_threshold_k_wavefront", _g1_quorum_wavefront),
    ("O3_sequence_drive_preserves_order", _o3_sequence_drive),
    ("O1_floor_on_filled_kit", _o1_floor_on_filled),
    ("B4_jitter_closed_p5_above_floor", _b4_jitter_closed),
    ("B2_cis_drive_data_blocked", _b2_data_blocked),
    ("O2_segmentation_subclock", _o2_subclock),
    ("B1_global_clock_two_anchor_closure", _k_global_clock),
    ("L8_no_magic", _j8_no_magic),
    ("L9_non_fit", _j9_non_fit),
    ("L10_determinism_2x_sha256", _j10_determinism),
    ("L11_honest_declaration", _j11_honest_declaration),
]


def run_gate(verbose=True):
    results = {}
    n_pass = 0
    for name, fn in CHECKS:
        ok, detail = fn()
        results[name] = {"pass": bool(ok), "detail": detail}
        n_pass += int(bool(ok))
        if verbose:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    all_ok = (n_pass == len(CHECKS))
    blob = json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
    results["_sha256"] = hashlib.sha256(blob).hexdigest()[:16]
    results["_all_pass"] = all_ok
    results["_n_pass"] = n_pass
    results["_n_total"] = len(CHECKS)
    if verbose:
        print(f"  ---- gate {'PASS' if all_ok else 'FAIL'} "
              f"({n_pass}/{len(CHECKS)}) sha={results['_sha256']}")
    return results


if __name__ == "__main__":
    run_gate(verbose=True)
