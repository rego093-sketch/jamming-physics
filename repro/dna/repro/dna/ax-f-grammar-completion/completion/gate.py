# -*- coding: utf-8 -*-
"""
completion.gate -- the fail-closed gate for the grammar-completion interpreter (Appendix F).

FAILS CLOSED on any miss:

  F1  SAME_OPERATOR       the SHAPE projection is the identical robust_z operator at G1, G2,
                          G4, G5 (scale- and shift-invariant to machine epsilon).
  F2  ORGAN_ATLAS         the MEAN organ x grammar confusion matrix is diagonal-dominant --
                          every organ (cardiac, neural, hepatic) peaks on its OWN grammar
                          (the regulatory grammar reads identity across organs, not heart
                          alone).
  F3  CONTROL_QUIET       the GAPDH housekeeping control's strongest organ-grammar
                          enrichment-z is below the locked ceiling (a tissue-neutral control).
  F4  G4_ORTHOGONAL       the dynamical signal (CpG O/E) is orthogonal to the material signal
                          (mean |corr| below the locked ceiling) -- G4 is a real new rung.
  F5  G5_COLINEAR         Hox colinearity on the real HOXD coordinates is at/above the locked
                          floor (rank-rank AND Pearson) -- the body-plan order code.
  F6  NO_MAGIC            the lock manifest reports zero inline magic numbers; every locked
                          input carries a provenance.
  F7  NON_FIT            the reading is identical with a decoy target file present -> the
                          engine reads only its locked DB.
  F8  DETERMINISM        two serializations hash identically (2x SHA-256); the shuffle is
                          seed-deterministic.
  F9  GRADES             only the four sanctioned grades, each with a basis; the open channels
                          are named.
  F10 HONEST_DECLARATION the decoding declaration is two-axis: STRUCTURAL complete AND
                          FUNCTIONAL False AND every functional obstacle named. Fails closed if
                          functional completion is ever asserted True (no false victory).

Run:  python3 -m completion.gate   (from the package root).
"""
import os
import json
import hashlib

from . import (lock, seqtools, atlas, dynamical, bodyplan, grammar_space,
               declaration, grading, interpreter)


def _f1_same_operator():
    p = grammar_space.same_operator_proof()
    ok = bool(p["same_operator_all_levels"])
    return ok, {"levels": p["levels_using_it"],
                "scale_inv": p["shape_scale_invariance"],
                "shift_inv": p["shape_shift_invariance"]}


def _f2_organ_atlas():
    cm = atlas.confusion_matrix()
    ok = bool(cm["mean_matrix_diagonal_dominant"])
    return ok, {"diagonal_dominance": "%d/%d" % (cm["diagonal_dominance_mean"], cm["n_organs"]),
                "mean_matrix": cm["mean_matrix"]}


def _f3_control_quiet():
    cm = atlas.confusion_matrix()
    ok = bool(cm["control_quiet"])
    return ok, {"control_max_grammar": cm["control_max_grammar"],
                "control_max_z": cm["control_max_z"],
                "ceiling": lock.control_quiet_z_max()}


def _f4_g4_orthogonal():
    o = dynamical.orthogonality_to_material()
    ok = bool(o["orthogonal"])
    return ok, {"mean_abs_corr": o["mean_abs_corr"], "ceiling": o["threshold"]}


def _f5_g5_colinear():
    c = bodyplan.colinearity()
    ok = bool(c["colinear"])
    return ok, {"rankrank": c["rankrank_genomic_vs_bodyrank"],
                "pearson": c["pearson_tss_vs_bodyrank"], "floor": c["threshold"]}


def _f6_no_magic():
    man = lock.lock_manifest()

    def all_prov(node):
        if isinstance(node, dict):
            if "provenance" in node and not node["provenance"]:
                return False
            return all(all_prov(v) for v in node.values())
        return True

    ok = (man["inline_magic_numbers"] == 0) and all_prov(man)
    return ok, {"inline_magic_numbers": man["inline_magic_numbers"]}


def _f7_non_fit():
    r1 = interpreter.interpret_grammar_completion()
    h1 = interpreter.reading_hash(r1)
    decoy = "validation_targets.json"
    created = False
    if not os.path.exists(decoy):
        with open(decoy, "w") as fh:
            json.dump({"fake_enhancer_activity": 999, "fake_methylation": 0.5}, fh)
        created = True
    try:
        r2 = interpreter.interpret_grammar_completion()
        h2 = interpreter.reading_hash(r2)
    finally:
        if created:
            os.remove(decoy)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1, "hash_with_decoy": h2}


def _f8_determinism():
    r = interpreter.interpret_grammar_completion()
    b1 = json.dumps(r, sort_keys=True).encode()
    b2 = json.dumps(json.loads(b1.decode()), sort_keys=True).encode()
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    key = lock.promoter_keys()[0]
    seq, _, _ = lock.promoter(key)
    s1 = seqtools.dinuc_shuffle(seq, lock.shuffle_seed())
    s2 = seqtools.dinuc_shuffle(seq, lock.shuffle_seed())
    ok = (h1 == h2) and (s1 == s2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16], "shuffle_deterministic": s1 == s2}


def _f9_grades():
    grades = grading.declared_grades()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}
    only_sanctioned = set(grades).issubset(sanctioned)
    each_has_basis = all(e.get("basis") for e in grading.LEDGER)
    open_named = all(e.get("named_obstacle") for e in grading.open_channels())
    ok = only_sanctioned and each_has_basis and open_named
    return ok, {"grades_used": grades, "open_named": open_named}


def _f10_honest_declaration():
    decl = declaration.decoding_declaration()
    comp = grading.completion_status()
    structural_ok = bool(decl["structural_complete"])
    functional_false = (decl["functional_complete"] is False) and \
                       (comp["functional_complete"] is False)
    obstacles_named = all(o.get("obstacle")
                          for o in decl["functional"]["open_obstacles"])
    ok = structural_ok and functional_false and obstacles_named
    return ok, {"structural_complete": structural_ok,
                "functional_complete": decl["functional_complete"],
                "obstacles_named": obstacles_named}


CHECKS = [
    ("F1_same_operator_all_levels", _f1_same_operator),
    ("F2_organ_atlas_diagonal_dominant", _f2_organ_atlas),
    ("F3_housekeeping_control_quiet", _f3_control_quiet),
    ("F4_dynamical_G4_orthogonal_to_material", _f4_g4_orthogonal),
    ("F5_bodyplan_G5_hox_colinear_real_coords", _f5_g5_colinear),
    ("F6_no_inline_magic_numbers", _f6_no_magic),
    ("F7_non_fit_invariant", _f7_non_fit),
    ("F8_determinism_2x_sha256", _f8_determinism),
    ("F9_honest_grades", _f9_grades),
    ("F10_honest_two_axis_declaration_no_false_victory", _f10_honest_declaration),
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
    print("  GRAMMAR COMPLETION -- the full grammar space + decoding declaration (fail-closed)")
    print("=" * 78)
    res = run_gate()
    sys.exit(0 if res["_all_pass"] else 1)
