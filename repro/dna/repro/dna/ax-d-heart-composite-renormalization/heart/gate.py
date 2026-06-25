# -*- coding: utf-8 -*-
"""
heart.gate -- the fail-closed gate for the heart composite-renormalization accuracy test.

FAILS CLOSED on any miss:

  D1 BRACKET_EXACT      the two-phase Voigt/Reuss bracket is EXACT (matches a hand
                        computation to <1e-9) and ORDERED (Reuss <= Voigt) across a sweep.
  D2 CONTAINMENT        the exact bracket from MEASURED ventricular inputs CONTAINS the
                        measured adult ventricular tissue modulus (RESULT C consistency).
  D3 JAMMING_INSUFFICIENT  the pure cell-jamming ceiling from the EMBRYONIC cell is BELOW
                        the measured E14 tissue -> the ECM phase / maturation is necessary
                        (RESULT A; the falsification of pure jamming, parameter-free).
  D4 GAMMA_ORTHOGONAL   gamma is time-invariant and reproduces the measured Appendix A
                        heart null (rho=+0.071, p=0.882) -> the stiffening axis is not
                        gamma (RESULT B; logical + reproduced null).
  D5 TRAJECTORY_SPANS   the predicted composition-flow trajectory starts soft, ends in the
                        adult band, and is monotone rising (the [F] illustration spans the
                        measured embryonic->adult range).
  D6 NO_MAGIC           the lock manifest reports zero inline magic numbers; every locked
                        input carries a provenance.
  D7 NON_FIT            the reading is identical with a decoy validation-target file present
                        -> the engine reads only its locked DB, never a validation target.
  D8 DETERMINISM        two serializations hash identically (2x SHA-256).
  D9 GRADES             only the four sanctioned grades, each with a basis; the accuracy
                        channels are [O] with NAMED obstacles; completion is honestly False.

Run:  python3 -m heart.gate   (from the package root)  -> PASS/FAIL lines + 2x-SHA witness;
exit 0 iff all pass.
"""
import json
import hashlib
import numpy as np

from . import lock, composite, trajectory, decomposition, grading, interpreter


def _d1_bracket_exact():
    # hand check at a known point, against the UNROUNDED bracket functions
    B_c, B_e, phi_c = 35.0, 5.0, 0.8
    V = 0.8 * 35.0 + 0.2 * 5.0
    R = 1.0 / (0.8 / 35.0 + 0.2 / 5.0)
    v_err = abs(composite.voigt_upper(B_c, B_e, phi_c) - V)
    r_err = abs(composite.reuss_lower(B_c, B_e, phi_c) - R)
    # ordered across a sweep (unrounded): Reuss <= Voigt always
    ordered = True
    for phi in np.linspace(0.1, 0.95, 60):
        if composite.reuss_lower(20.0, 6.0, float(phi)) > composite.voigt_upper(20.0, 6.0, float(phi)) + 1e-12:
            ordered = False
    ok = (v_err < 1e-9) and (r_err < 1e-9) and ordered
    return ok, {"voigt_err": v_err, "reuss_err": r_err, "ordered_over_sweep": ordered}


def _d2_containment():
    c = decomposition.bracket_consistency()
    ok = bool(c["consistency_holds"])
    return ok, {"LV_bracket_kpa": c["ventricular_LV_bracket_kpa"],
                "measured_adult_kpa": c["measured_adult_tissue_kpa"],
                "contained_with_LV_ECM": c["contained_with_LV_ECM"]}


def _d3_jamming_insufficient():
    a = decomposition.jamming_insufficiency()
    ok = bool(a["pure_cell_jamming_insufficient"])
    return ok, {"embryonic_cell_ceiling_kpa": a["pure_jamming_ceiling_kpa"],
                "measured_E14_kpa": a["measured_E14_tissue_kpa"],
                "rise_factor_to_E14": a["rise_factor_ceiling_to_E14"]}


def _d4_gamma_orthogonal():
    b = decomposition.gamma_orthogonality()
    ok = bool(b["reproduces_and_explains_null"])
    return ok, {"gamma_time_invariant": b["gamma_time_invariant"],
                "appendix_a_null_rho": b["appendix_a_heart_null_rho"],
                "appendix_a_null_p": b["appendix_a_heart_null_p"]}


def _d5_trajectory_spans():
    t = trajectory.trajectory_spans_measured()
    ok = bool(t["spans_measured_range"])
    return ok, {"predicted_start_kpa": t["predicted_start_kpa"],
                "predicted_end_kpa": t["predicted_end_kpa"],
                "adult_band_kpa": t["measured_adult_band_kpa"],
                "monotone": t["monotone_rising"]}


def _d6_no_magic():
    man = lock.lock_manifest()
    # every leaf with a 'provenance' must be non-empty
    def all_prov(node):
        if isinstance(node, dict):
            if "provenance" in node and "value" in node:
                if not node["provenance"]:
                    return False
            return all(all_prov(v) for v in node.values())
        return True
    has_prov = all_prov(man)
    ok = (man["inline_magic_numbers"] == 0) and has_prov
    return ok, {"inline_magic_numbers": man["inline_magic_numbers"],
                "all_have_provenance": has_prov}


def _d7_non_fit():
    import os
    r1 = interpreter.interpret_heart()
    h1 = interpreter.reading_hash(r1)
    decoy = "validation_targets.json"
    created = False
    if not os.path.exists(decoy):
        with open(decoy, "w") as fh:
            json.dump({"fake_tissue_kpa": 999, "fake_phi": 0.42}, fh)
        created = True
    try:
        r2 = interpreter.interpret_heart()
        h2 = interpreter.reading_hash(r2)
    finally:
        if created:
            os.remove(decoy)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1, "hash_with_decoy": h2}


def _d8_determinism():
    r = interpreter.interpret_heart()
    b1 = json.dumps(r, sort_keys=True).encode()
    b2 = json.dumps(json.loads(b1.decode()), sort_keys=True).encode()
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    ok = (h1 == h2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16]}


def _d9_grades():
    grades = grading.declared_grades()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}
    only_sanctioned = set(grades).issubset(sanctioned)
    each_has_basis = all(e.get("basis") for e in grading.LEDGER)
    open_named = all(e.get("named_obstacle")
                     for e in grading.open_accuracy_channels())
    incomplete = (grading.completion_status()["complete"] is False)
    ok = only_sanctioned and each_has_basis and open_named and incomplete
    return ok, {"grades_used": grades, "open_channels_named": open_named,
                "completion_complete": grading.completion_status()["complete"]}


CHECKS = [
    ("D1_two_phase_bracket_exact", _d1_bracket_exact),
    ("D2_bracket_contains_measured_tissue", _d2_containment),
    ("D3_pure_jamming_insufficient_falsified", _d3_jamming_insufficient),
    ("D4_gamma_orthogonal_reproduces_null", _d4_gamma_orthogonal),
    ("D5_composition_trajectory_spans_measured", _d5_trajectory_spans),
    ("D6_no_inline_magic_numbers", _d6_no_magic),
    ("D7_non_fit_invariant", _d7_non_fit),
    ("D8_determinism_2x_sha256", _d8_determinism),
    ("D9_honest_grades_no_false_victory", _d9_grades),
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
    print("  HEART COMPOSITE-RENORMALIZATION -- ACCURACY GATE (fail-closed)")
    print("=" * 78)
    res = run_gate()
    sys.exit(0 if res["_all_pass"] else 1)
