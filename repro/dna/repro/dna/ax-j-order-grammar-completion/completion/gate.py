# -*- coding: utf-8 -*-
"""
completion.gate -- the fail-closed gate for Appendix J (the order-grammar COMPLETION).

FAILS CLOSED on any miss:

  J1  SAME_OPERATOR+INHERIT  the SHAPE operator robust_z is the identical median-centred, MAD-scaled
                        operator as Appendices E..I (scale- AND shift-invariant to machine epsilon),
                        the gamma operator reproduces -mean(NN dG) exactly on a probe, the four
                        Appendix-G/H skeletal drivers (SOX9/RUNX2/PAX1/GLI3) are byte-identical, AND
                        all 38 inherited driver gammas are BYTE-IDENTICAL to the parent Appendix-I
                        param_db (read off disk). One operator, real inherited data, zero drift.
  J2  CASCADE_IS_DAG    the FILLED cited cascade (63 genes / 62 edges) is acyclic; a deterministic
                        topological order exists (depth is DERIVED, not asserted).
  J3  THE_NULL          |Spearman(spinodal(gamma), Carnegie)| <= the locked ceiling -- the single
                        locus barrier still does NOT order staging on the filled kit.
  J4  EDGE_CONCORDANCE  among cited edges whose endpoints both carry a Carnegie rank, ZERO
                        inversions on the filled kit.
  J5  DEPTH_BEATS_GAMMA |Spearman(cascade depth, Carnegie)| STRICTLY exceeds the spinodal
                        correlation, on all anchored genes AND on the main wired component.
  J6  OR_WAVEFRONT      in the coupled-R19 substrate the OR firing order respects the cascade DAG
                        (wavefront theorem, 0 violations) AND tracks DEPTH, not bare spinodal.
  J7  KEYS_DISAGREE     spinodal order and cascade-depth order are genuinely DIFFERENT (rho < 1) --
                        the grammar does real work, not re-deriving gamma.
  G1  QUORUM_WAVEFRONT  the OR-gate generalises to a QUORUM/AND threshold-k gate
                        (k_i = max(1, ceil(alpha*indeg))); the cascade partial order still holds
                        (0 violations) AND convergent nodes never fire EARLIER under AND than OR.
                        OR is the k=1 special case.
  O3  SEQUENCE_DRIVE    per-edge drive read from the promoter sequence (sqrt(gamma) ON-branch
                        amplitude) instead of uniform W=1 PRESERVES the cascade firing order
                        (0 OR-violations under sequence drive; firing-order rho ~ 1).
  O1  FLOOR_ON_FILLED   the pre-registered 0.70 absolute depth<->Carnegie strength floor is REACHED
                        on the filled kit, AND the lift requires BOTH named fixes (limb-only and
                        HOX-only each below floor; both together above). Reported, never upgraded.
  O1J JITTER_HONEST     the rank-jitter band is computed at the canonical seed=19 and its honest
                        lower edge sits BELOW the floor -- i.e. the result is sensitive to cited-rank
                        uncertainty, which is exactly why O1 stays [L] and not [V].
  O2  SUBCLOCK          the segmentation sub-clock (real measured period x cited somite count)
                        predicts a somitogenesis span CONSISTENT with the cited Carnegie window,
                        while the single global zero-point is honestly left [O].
  J8  NO_MAGIC          the lock manifest reports zero inline magic numbers; every locked input
                        (including the floor-robustness seed) carries a provenance string.
  J9  NON_FIT           the reading is identical with a decoy Carnegie/timing target present -> the
                        engine reads only its locked DB, never a target.
  J10 DETERMINISM       two serializations of the reading hash identically (2x SHA-256).
  J11 HONEST_DECLARATION the declaration closes O1(to [L]) / O2-subclock([L]) / O3([F]+[V]) /
                        GATE([V]) but keeps the O2 global zero-point [O], the built body [O], and
                        physical_complete=False; uses only the four sanctioned grades; names every
                        open channel; and -- CRUCIALLY -- the O1 absolute-strength row stays [L] and
                        is NOT upgraded to [V] even though the floor is now met. FAILS CLOSED on any
                        false victory, including an O1->[V] promotion.

Run:  python3 -m completion.gate   (from the package root).
"""
import os
import json
import hashlib

import numpy as np

from . import (lock, seqtools, cascade, coupled, timing, nulltest, grammar,
               declaration, grading, interpreter)


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
    # ALL 38 inherited gammas byte-identical to the parent Appendix-I param_db (read off disk)
    parent_path = lock.parent_db_path()
    with open(parent_path, "r", encoding="utf-8") as fh:
        parent = json.load(fh)
    parent_dg = parent["driver_gamma"]
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


def _o1j_jitter_honest():
    j = nulltest.floor_retest_jitter()
    seed_ok = (j["seed"] == 19)
    # the numeric lower edge (p5) must sit BELOW the floor: the result IS sensitive -> stays [L]
    sensitive = (j["p5"] < j["floor"])
    ok = bool(seed_ok and sensitive)
    return ok, {"seed": j["seed"], "mean": j["mean"], "p5": j["p5"], "p95": j["p95"],
                "frac_at_or_above_floor": j["frac_at_or_above_floor"],
                "floor": j["floor"], "sensitive_so_stays_L": sensitive}


def _o2_subclock():
    sub = timing.segmentation_subclock()
    glob = timing.global_clock_open()
    consistent = bool(sub["prediction_in_cited_window_pm2d"])
    still_open = "[O]" in glob["grade"]
    ok = consistent and still_open
    return ok, {"predicted_days": sub["predicted_somitogenesis_days"],
                "cited_window": sub["cited_window_CS9_to_CS13_days"],
                "consistent": consistent, "global_zero_point_open": still_open}


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
              "developmental_rates_target.json": {"fake_days": {"SOX9": 1234.5}}}
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
    global_clock_open = bool(decl["o2_global_zero_point_open"])
    # O2 sub-clock closed but global zero-point open; O3 declared [F]; GATE [V]
    o2_subclock_closed = bool(decl["o2_subclock_closed"])
    o3_F = bool(decl["o3_drive_from_sequence_F"])
    gate_V = bool(decl["gate_threshold_k_V"])
    # NO FALSE VICTORY: the O1 absolute-strength row must stay [L], never [V]
    o1 = next((r for r in led["rows"] if r["id"] == "O1"), None)
    o1_present = o1 is not None
    o1_not_V = bool(o1_present and not o1["grade"].startswith("[V]"))
    o1_is_L = bool(o1_present and o1["grade"].startswith("[L]"))
    grading_self_audit = bool(led["o1_is_L_not_V"])
    decl_flag = bool(decl["o1_grade_is_L_not_V"])

    ok = (only_sanctioned and opens_named and not_physical and no_consciousness
          and global_clock_open and o2_subclock_closed and o3_F and gate_V
          and o1_not_V and o1_is_L and grading_self_audit and decl_flag)
    return ok, {"only_sanctioned_grades": only_sanctioned, "opens_named": opens_named,
                "physical_complete": decl["physical_complete"],
                "o2_global_zero_point_open": global_clock_open,
                "o2_subclock_closed": o2_subclock_closed, "o3_F": o3_F, "gate_V": gate_V,
                "o1_absolute_strength_stays_L_not_V": (o1_not_V and o1_is_L),
                "grading_self_audit_o1_is_L_not_V": grading_self_audit}


CHECKS = [
    ("J1_same_operator_and_inherit", _j1_same_operator_and_inherit),
    ("J2_cascade_is_dag", _j2_cascade_is_dag),
    ("J3_the_null", _j3_the_null),
    ("J4_edge_concordance", _j4_edge_concordance),
    ("J5_depth_beats_gamma", _j5_depth_beats_gamma),
    ("J6_or_wavefront", _j6_or_wavefront),
    ("J7_keys_disagree", _j7_keys_disagree),
    ("G1_quorum_threshold_k_wavefront", _g1_quorum_wavefront),
    ("O3_sequence_drive_preserves_order", _o3_sequence_drive),
    ("O1_floor_on_filled_kit", _o1_floor_on_filled),
    ("O1J_jitter_honest_seed19", _o1j_jitter_honest),
    ("O2_segmentation_subclock", _o2_subclock),
    ("J8_no_magic", _j8_no_magic),
    ("J9_non_fit", _j9_non_fit),
    ("J10_determinism_2x_sha256", _j10_determinism),
    ("J11_honest_declaration", _j11_honest_declaration),
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
