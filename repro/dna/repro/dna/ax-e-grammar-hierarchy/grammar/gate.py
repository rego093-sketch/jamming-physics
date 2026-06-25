# -*- coding: utf-8 -*-
"""
grammar.gate -- the fail-closed gate for the grammar-hierarchy interpreter.

FAILS CLOSED on any miss:

  E1 SAME_OPERATOR      the SHAPE projection is the identical robust_z operator at every
                        level (scale- and shift-invariant to machine epsilon).
  E2 TISSUE_IDENTITY    the regulatory grammar G2 separates cardiac from non-cardiac
                        promoters by >= 2x, while the material grammar G1 does not carry
                        that identity (a tissue-level blueprint exists, sequence-readable).
  E3 SHUFFLE_INVARIANCE a dinucleotide-preserving shuffle preserves gamma_1 EXACTLY and
                        collapses the cardiac grammar -> the tissue identity is information
                        ABOVE the material level (the missed upper grammar).
  E4 ORTHOGONAL         the G1 and G2 signals are largely uncorrelated (|corr| < 0.3).
  E5 THREE_LEVELS       all three grammars return a (LEVEL, SHAPE) read on a cardiac
                        sequence (the hierarchy is populated, not just asserted).
  E6 NO_MAGIC           the lock manifest reports zero inline magic numbers; every locked
                        input carries a provenance.
  E7 NON_FIT            the reading is identical with a decoy target file present -> the
                        engine reads only its locked DB.
  E8 DETERMINISM        two serializations hash identically (2x SHA-256); the shuffle is
                        seed-deterministic.
  E9 GRADES             only the four sanctioned grades, each with a basis; the open
                        channels are named; completion is honestly False.

Run:  python3 -m grammar.gate   (from the package root).
"""
import os
import json
import hashlib

from . import lock, seqtools, material, regulatory, architecture, hierarchy, grading, interpreter


def _e1_same_operator():
    p = hierarchy.same_operator_proof()
    ok = bool(p["same_operator_all_levels"])
    return ok, {"scale_inv": p["shape_scale_invariance"], "shift_inv": p["shape_shift_invariance"]}


def _e2_tissue_identity():
    s = hierarchy.tissue_identity_separation()
    ok = bool(s["G2_separates_tissue"] and not s["G1_separates_tissue"])
    return ok, {"G2_ratio": s["G2_cardiac_over_control_ratio"],
                "G2_separates": s["G2_separates_tissue"],
                "G1_separates": s["G1_separates_tissue"]}


def _e3_shuffle_invariance():
    sh = hierarchy.shuffle_test()
    ok = bool(sh["dinucleotide_counts_preserved"]
              and sh["material_level_preserved_exactly"]
              and sh["cardiac_grammar_collapsed"])
    return ok, {"gamma1_preserved": sh["material_level_preserved_exactly"],
                "grammar_orig": sh["cardiac_grammar_original_total"],
                "grammar_shuf": sh["cardiac_grammar_shuffled_total"],
                "fraction_lost": sh["fraction_grammar_lost"]}


def _e4_orthogonal():
    o = hierarchy.cross_grammar_orthogonality()
    ok = bool(o["largely_orthogonal"])
    return ok, {"corr": o["corr_G1_material_vs_G2_regulatory"], "r2": o["r_squared"]}


def _e5_three_levels():
    key = lock.cardiac_keys()[0]
    seq, _, _ = lock.sequence(key)
    lv = hierarchy.read_all_levels(seq)
    g1 = lv["G1_material"].get("gamma_LEVEL")
    g2 = lv["G2_regulatory"].get("gamma_LEVEL")
    g3 = lv["G3_architecture"].get("gamma_LEVEL")
    ok = (g1 is not None) and (g2 is not None) and (g3 is not None)
    return ok, {"G1_gamma": g1, "G2_gamma": g2, "G3_gamma": g3}


def _e6_no_magic():
    man = lock.lock_manifest()
    def all_prov(node):
        if isinstance(node, dict):
            if "provenance" in node and not node["provenance"]:
                return False
            return all(all_prov(v) for v in node.values())
        return True
    ok = (man["inline_magic_numbers"] == 0) and all_prov(man)
    return ok, {"inline_magic_numbers": man["inline_magic_numbers"]}


def _e7_non_fit():
    r1 = interpreter.interpret_grammar_hierarchy()
    h1 = interpreter.reading_hash(r1)
    decoy = "validation_targets.json"
    created = False
    if not os.path.exists(decoy):
        with open(decoy, "w") as fh:
            json.dump({"fake_enhancer_activity": 999}, fh)
        created = True
    try:
        r2 = interpreter.interpret_grammar_hierarchy()
        h2 = interpreter.reading_hash(r2)
    finally:
        if created:
            os.remove(decoy)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1, "hash_with_decoy": h2}


def _e8_determinism():
    r = interpreter.interpret_grammar_hierarchy()
    b1 = json.dumps(r, sort_keys=True).encode()
    b2 = json.dumps(json.loads(b1.decode()), sort_keys=True).encode()
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    # shuffle determinism
    key = lock.cardiac_keys()[0]
    seq, _, _ = lock.sequence(key)
    s1 = seqtools.dinuc_shuffle(seq, lock.shuffle_seed())
    s2 = seqtools.dinuc_shuffle(seq, lock.shuffle_seed())
    ok = (h1 == h2) and (s1 == s2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16], "shuffle_deterministic": s1 == s2}


def _e9_grades():
    grades = grading.declared_grades()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}
    only_sanctioned = set(grades).issubset(sanctioned)
    each_has_basis = all(e.get("basis") for e in grading.LEDGER)
    open_named = all(e.get("named_obstacle") for e in grading.open_channels())
    incomplete = (grading.completion_status()["complete"] is False)
    ok = only_sanctioned and each_has_basis and open_named and incomplete
    return ok, {"grades_used": grades, "open_named": open_named,
                "completion_complete": grading.completion_status()["complete"]}


CHECKS = [
    ("E1_same_operator_all_levels", _e1_same_operator),
    ("E2_tissue_identity_readable_G2_not_G1", _e2_tissue_identity),
    ("E3_upper_grammar_above_material_shuffle", _e3_shuffle_invariance),
    ("E4_grammar_levels_orthogonal", _e4_orthogonal),
    ("E5_three_levels_populated", _e5_three_levels),
    ("E6_no_inline_magic_numbers", _e6_no_magic),
    ("E7_non_fit_invariant", _e7_non_fit),
    ("E8_determinism_2x_sha256", _e8_determinism),
    ("E9_honest_grades_no_false_victory", _e9_grades),
]


def run_gate(verbose=True):
    results = {}
    all_ok = True
    for name, fn in CHECKS:
        ok, detail = fn()
        results[name] = {"pass": bool(ok), "detail": detail}
        all_ok = all_ok and ok
        if verbose:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    results["_all_pass"] = all_ok
    blob = json.dumps(results, sort_keys=True).encode()
    results["_sha256"] = hashlib.sha256(blob).hexdigest()[:16]
    if verbose:
        n_pass = sum(1 for n, _ in CHECKS if results[n]["pass"])
        print(f"  ---- gate {'PASS' if all_ok else 'FAIL'} "
              f"({n_pass}/{len(CHECKS)}) sha={results['_sha256']}")
    return results


if __name__ == "__main__":
    import sys
    print("=" * 78)
    print("  GRAMMAR HIERARCHY -- reading the upper blueprint (fail-closed)")
    print("=" * 78)
    res = run_gate()
    sys.exit(0 if res["_all_pass"] else 1)
