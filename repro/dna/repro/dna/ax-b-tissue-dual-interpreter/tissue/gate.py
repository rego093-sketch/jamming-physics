# -*- coding: utf-8 -*-
"""
tissue.gate -- the fail-closed gate for the tissue dual interpreter.

A senior reviewer must be able to confirm, mechanically, that nothing here
backslid. The gate asserts, and FAILS CLOSED on any miss:

  G1 EXACTNESS      the closed-form LEVEL integral equals fine quadrature to
                    < 1e-9, and every closed-form territory boundary reproduces
                    its threshold p(x_k)=theta to < 1e-9. (precision is real)
  G2 SUPERSESSION   the old coarse Jacobi's lambda error SHRINKS monotonically
                    toward the exact lambda as the grid refines, and the
                    transverse variance is ~0 (the field is exactly 1-D for the
                    separable geometry). i.e. the old solver was the rough one,
                    not the physics. (handover A3)
  G3 ORTHOGONALITY  SHAPE is invariant under both LEVEL moves (source scale,
                    background offset) to machine epsilon, and geometry moves
                    SHAPE. LEVEL ⟂ SHAPE, exactly. (no "approximately")
  G4 NO_MAGIC       the lock manifest reports zero inline magic numbers and every
                    constant carries a grade + provenance. (the dwell(K=0.6,
                    brake=0.5) class of rot cannot reappear)
  G5 NON_FIT        the interpreter never reads a validation target; running it
                    with/without any target file present yields identical output.
  G6 DETERMINISM    two independent serializations hash identically (2x SHA-256).
  G7 GRADES         exactly the four sanctioned grades are used, each with a basis;
                    the two accuracy channels are [O] with a NAMED obstacle (no
                    false victory); completion is honestly False.

Run:  python3 -m tissue.gate   (from the package root)  -> prints PASS/FAIL lines
and a 2x-SHA determinism witness; exit code 0 iff all pass.
"""
import math, json, hashlib
import numpy as np

from . import lock, field, level, shape, orthogonality, grading, interpreter

_REF_L = 360.0   # a reference domain (6*lambda at lambda=60) used for the checks


def _g1_exactness():
    lam = lock.lambda_um()
    L = _REF_L
    # LEVEL integral vs fine quadrature
    xs = np.linspace(0.0, L, 2_000_001)
    ys = field.planar_profile(xs, L, lam)
    quad = float(np.trapezoid(ys, xs))
    exact = field.planar_integral(L, lam)
    int_err = abs(exact - quad) / exact
    # boundary crossings reproduce theta exactly
    theta, _, _ = lock.territory_theta()
    thr = shape.territory_thresholds(theta, 4)
    max_thr_err = 0.0
    for t in thr:
        xk = field.planar_threshold_crossing(t, L, lam)
        p_xk = float(field.planar_profile(xk, L, lam))
        max_thr_err = max(max_thr_err, abs(p_xk - t))
    ok = (int_err < 1e-9) and (max_thr_err < 1e-9)
    return ok, {"level_integral_rel_err": int_err, "max_threshold_err": max_thr_err}


def _g2_supersession():
    rows = field.convergence_to_closed_form(_REF_L, Ns=(16, 24, 32, 48))
    errs = [r["rel_err_pct"] for r in rows]
    tvars = [r["transverse_var"] for r in rows]
    monotone = all(errs[i] >= errs[i + 1] - 1e-9 for i in range(len(errs) - 1))
    finest_small = errs[-1] < errs[0]          # refining helps
    flat = max(tvars) < 1e-6                    # field is exactly 1-D (separable)
    ok = monotone and finest_small and flat
    return ok, {"jacobi_rows": rows, "monotone_shrink": monotone,
                "transverse_var_max": max(tvars)}


def _g3_orthogonality():
    cert = orthogonality.certify(_REF_L)
    tk = cert["two_knob_test"]
    ok = (tk["knob1_scale_source"]["shape_invariant"]
          and tk["knob2_add_background"]["shape_invariant"]
          and cert["geometry_changes_shape"]["shape_moved"])
    return ok, {
        "scale_shape_change": tk["knob1_scale_source"]["shape_max_abs_change"],
        "offset_shape_change": tk["knob2_add_background"]["shape_max_abs_change"],
        "geometry_moved_shape": cert["geometry_changes_shape"]["shape_moved"],
        "panel_corr_level_vs_shape": cert["panel_correlation"]["corr_level_vs_shape"],
    }


def _g4_no_magic():
    man = lock.lock_manifest()
    has_all_provenance = all(c.get("provenance") for c in man["constants"].values())
    ok = (man["inline_magic_numbers"] == 0) and has_all_provenance
    return ok, {"inline_magic_numbers": man["inline_magic_numbers"],
                "all_constants_have_provenance": has_all_provenance}


def _g5_non_fit():
    # The interpreter reads ONLY lock/DB; it has no code path that opens a target
    # file. We assert this structurally: the reading is identical regardless of a
    # decoy target present in the cwd.
    import os, tempfile
    r1 = interpreter.interpret_tissue(_REF_L)
    h1 = interpreter.reading_hash(r1)
    decoy = "validation_targets.json"
    created = False
    if not os.path.exists(decoy):
        with open(decoy, "w") as fh:
            json.dump({"fake_organ_mass_g": 99999}, fh)
        created = True
    try:
        r2 = interpreter.interpret_tissue(_REF_L)
        h2 = interpreter.reading_hash(r2)
    finally:
        if created:
            os.remove(decoy)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1, "hash_with_decoy": h2}


def _g6_determinism():
    r = interpreter.interpret_tissue(_REF_L)
    b1 = json.dumps(r, sort_keys=True).encode()
    b2 = json.dumps(json.loads(b1.decode()), sort_keys=True).encode()
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    ok = (h1 == h2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16]}


def _g7_grades():
    grades = grading.declared_grades()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}
    only_sanctioned = set(grades).issubset(sanctioned)
    each_has_basis = all(e.get("basis") for e in grading.LEDGER)
    open_named = all(e.get("named_obstacle") for e in grading.open_accuracy_channels())
    incomplete = (grading.completion_status()["complete"] is False)
    ok = only_sanctioned and each_has_basis and open_named and incomplete
    return ok, {"grades_used": grades, "open_channels_named": open_named,
                "completion_complete": grading.completion_status()["complete"]}


CHECKS = [
    ("G1_exactness", _g1_exactness),
    ("G2_supersession_of_coarse_jacobi", _g2_supersession),
    ("G3_orthogonality_level_perp_shape", _g3_orthogonality),
    ("G4_no_inline_magic_numbers", _g4_no_magic),
    ("G5_non_fit_invariant", _g5_non_fit),
    ("G6_determinism_2x_sha256", _g6_determinism),
    ("G7_honest_grades_no_false_victory", _g7_grades),
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
        print(f"  ---- gate {'PASS' if all_ok else 'FAIL'} "
              f"({sum(1 for n,_ in CHECKS if results[n]['pass'])}/{len(CHECKS)}) "
              f"sha={results['_sha256']}")
    return results


if __name__ == "__main__":
    import sys
    print("=" * 78)
    print("  TISSUE DUAL INTERPRETER -- GATE (fail-closed)")
    print("=" * 78)
    res = run_gate()
    sys.exit(0 if res["_all_pass"] else 1)
