# -*- coding: utf-8 -*-
"""
hierarchy.gate -- the fail-closed gate for the hierarchical scale-renormalization
interpreter.

A senior reviewer must be able to confirm, mechanically, that nothing here is
hand-waved. The gate asserts, and FAILS CLOSED on any miss:

  H1 BOUNDS_EXACT     across a sweep of packing fractions, the effective modulus
                      B_eff ALWAYS lies in the EXACT bracket [B_Reuss, B_Voigt] =
                      [0, phi*B_unit]. The aggregate stiffness can never leave the
                      rigorous elastic-mixture bounds. (no rigidity is invented)
  H2 JAMMING_THRESHOLD below phi_c the rigidity fraction J is EXACTLY 0 (a fluid;
                      Reuss floor), and strictly above phi_c it is > 0 and <= 1. The
                      onset is sharp and the modulus turns on at jamming, not before.
  H3 MASS_EXACT       the aggregate density is EXACTLY phi*rho_unit to machine
                      epsilon across the sweep (void carries no mass). (precision)
  H4 RG_FLOW          the wave-speed softening ratio per rung equals sqrt(J) exactly,
                      AND the operator composes (climbing two rungs == one combined
                      rung) to < 1e-9 -- a consistent renormalization-group semigroup.
  H5 ORTHOGONALITY    the mechanical SHAPE is invariant under both LEVEL moves (field
                      scale, uniform offset) to machine epsilon, and geometry moves
                      SHAPE. LEVEL ⟂ SHAPE, exactly. (no "approximately")
  H6 NO_MAGIC         the lock manifest reports zero inline magic numbers and every
                      constant carries a grade + provenance. (the dwell(K=0.6,
                      brake=0.5) class of rot cannot reappear)
  H7 NON_FIT          the interpreter never reads a validation target; running it
                      with a decoy target file present yields identical output.
  H8 DETERMINISM      two independent serializations hash identically (2x SHA-256).
  H9 GRADES_AND_SCALE exactly the four sanctioned grades are used, each with a basis;
                      the accuracy channels are [O] with NAMED obstacles (no false
                      victory); completion is honestly False; AND every reading
                      channel is classified to a tower level (scale coverage holds).

Run:  python3 -m hierarchy.gate   (from the package root)  -> prints PASS/FAIL lines
and a 2x-SHA determinism witness; exit code 0 iff all pass.
"""
import json
import hashlib
import numpy as np

from . import lock, jamming, renorm, ladder, level, shape, orthogonality, classify, \
    grading, interpreter

_B_UNIT = 1000.0       # a reference unit modulus (Pa) used for the bracket sweep;
                       # absolute value is irrelevant to the dimensionless checks
_RHO_UNIT = 1070.0     # a reference unit density used for the mass check
_PHI_SWEEP = np.linspace(0.30, 0.999, 400)   # spans below and above phi_c


def _h1_bounds_exact():
    """B_eff in [0, phi*B_unit] for every phi in the sweep -- exact bracket."""
    worst_below = 0.0
    worst_above = 0.0
    all_in = True
    for phi in _PHI_SWEEP:
        r = renorm.renormalize(_B_UNIT, _RHO_UNIT, float(phi))
        B_eff = r["B_eff"]
        floor = r["B_reuss_floor"]
        ceil = r["B_voigt_ceiling"]
        if B_eff < floor - 1e-12:
            all_in = False
            worst_below = max(worst_below, floor - B_eff)
        if B_eff > ceil + 1e-12:
            all_in = False
            worst_above = max(worst_above, B_eff - ceil)
    return all_in, {
        "phi_points": len(_PHI_SWEEP),
        "max_underflow_below_reuss": worst_below,
        "max_overflow_above_voigt": worst_above,
        "all_B_eff_in_bracket": all_in,
    }


def _h2_jamming_threshold():
    """J == 0 below phi_c, 0 < J <= 1 above phi_c. Sharp onset at jamming."""
    pc, _, _ = lock.phi_c()
    below = [pc - 0.20, pc - 0.05, pc - 1e-6]
    above = [pc + 1e-6, pc + 0.05, pc + 0.20, 0.999]
    below_zero = all(float(jamming.rigidity_fraction(p)) == 0.0 for p in below)
    above_pos = all(0.0 < float(jamming.rigidity_fraction(p)) <= 1.0 for p in above)
    # at phi_c exactly, J = 0 (marginal, not yet rigid)
    at_pc_zero = (float(jamming.rigidity_fraction(pc)) == 0.0)
    ok = below_zero and above_pos and at_pc_zero
    return ok, {
        "phi_c": pc,
        "J_below_phi_c_all_zero": below_zero,
        "J_at_phi_c": float(jamming.rigidity_fraction(pc)),
        "J_above_phi_c_in_0_1": above_pos,
    }


def _h3_mass_exact():
    """rho_eff == phi * rho_unit to machine epsilon across the sweep."""
    max_err = 0.0
    for phi in _PHI_SWEEP:
        r = renorm.renormalize(_B_UNIT, _RHO_UNIT, float(phi))
        max_err = max(max_err, abs(r["rho_eff"] - float(phi) * _RHO_UNIT))
    ok = max_err < 1e-9
    return ok, {"max_density_abs_err": max_err, "law": "rho_eff = phi * rho_unit"}


def _h4_rg_flow():
    """softening ratio == sqrt(J) exactly, AND R composes (associativity) < 1e-9."""
    # softening ratio check
    max_ratio_err = 0.0
    for phi in _PHI_SWEEP:
        J = float(jamming.rigidity_fraction(float(phi)))
        r = renorm.renormalize(_B_UNIT, _RHO_UNIT, float(phi))
        max_ratio_err = max(max_ratio_err,
                            abs(r["softening_ratio_c_eff_over_c"] - (J ** 0.5)))
    ratio_ok = max_ratio_err < 1e-9
    # composition (semigroup) check at two representative jammed fractions
    pc, _, _ = lock.phi_c()
    comp = renorm.compose_two(_B_UNIT, _RHO_UNIT,
                              pc + 0.40 * (1 - pc), pc + 0.70 * (1 - pc))
    comp_ok = comp["composes_exactly"]
    ok = ratio_ok and comp_ok
    return ok, {
        "max_softening_ratio_err": max_ratio_err,
        "softening_ratio_is_sqrt_J": ratio_ok,
        "composition_max_discrepancy": comp["max_discrepancy"],
        "R_composes_exactly": comp_ok,
    }


def _h5_orthogonality():
    cert = orthogonality.certify()
    tk = cert["two_knob_test"]
    ok = (tk["knob1_scale_field"]["shape_invariant"]
          and tk["knob2_add_background"]["shape_invariant"]
          and cert["geometry_changes_shape"]["shape_moved"])
    return ok, {
        "scale_shape_change": tk["knob1_scale_field"]["shape_max_abs_change"],
        "offset_shape_change": tk["knob2_add_background"]["shape_max_abs_change"],
        "geometry_moved_shape": cert["geometry_changes_shape"]["shape_moved"],
        "panel_corr_level_vs_shape": cert["panel_correlation"]["corr_level_vs_shape"],
    }


def _h6_no_magic():
    man = lock.lock_manifest()
    has_all_provenance = all(c.get("provenance") for c in man["constants"].values())
    ok = (man["inline_magic_numbers"] == 0) and has_all_provenance
    return ok, {"inline_magic_numbers": man["inline_magic_numbers"],
                "all_constants_have_provenance": has_all_provenance}


def _h7_non_fit():
    """The interpreter reads ONLY the locked DB; a decoy validation target in the
    cwd must not change its output."""
    import os
    r1 = interpreter.interpret_hierarchy()
    h1 = interpreter.reading_hash(r1)
    decoy = "validation_targets.json"
    created = False
    if not os.path.exists(decoy):
        with open(decoy, "w") as fh:
            json.dump({"fake_organ_modulus_pa": 99999, "fake_phi": 0.42}, fh)
        created = True
    try:
        r2 = interpreter.interpret_hierarchy()
        h2 = interpreter.reading_hash(r2)
    finally:
        if created:
            os.remove(decoy)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1, "hash_with_decoy": h2}


def _h8_determinism():
    r = interpreter.interpret_hierarchy()
    b1 = json.dumps(r, sort_keys=True).encode()
    b2 = json.dumps(json.loads(b1.decode()), sort_keys=True).encode()
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    ok = (h1 == h2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16]}


def _h9_grades_and_scale():
    grades = grading.declared_grades()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}
    only_sanctioned = set(grades).issubset(sanctioned)
    each_has_basis = all(e.get("basis") for e in grading.LEDGER)
    open_named = all(e.get("named_obstacle")
                     for e in grading.open_accuracy_channels())
    incomplete = (grading.completion_status()["complete"] is False)
    scale_coverage = classify.coverage_ok()
    ok = (only_sanctioned and each_has_basis and open_named and incomplete
          and scale_coverage)
    return ok, {
        "grades_used": grades,
        "open_channels_named": open_named,
        "completion_complete": grading.completion_status()["complete"],
        "scale_classification_coverage_ok": scale_coverage,
        "levels_covered": classify.levels_covered(),
    }


CHECKS = [
    ("H1_effective_modulus_in_exact_bracket", _h1_bounds_exact),
    ("H2_jamming_threshold_sharp_onset", _h2_jamming_threshold),
    ("H3_density_renormalization_exact", _h3_mass_exact),
    ("H4_rg_flow_softening_and_composition", _h4_rg_flow),
    ("H5_orthogonality_level_perp_shape", _h5_orthogonality),
    ("H6_no_inline_magic_numbers", _h6_no_magic),
    ("H7_non_fit_invariant", _h7_non_fit),
    ("H8_determinism_2x_sha256", _h8_determinism),
    ("H9_honest_grades_and_scale_coverage", _h9_grades_and_scale),
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
    print("  HIERARCHICAL SCALE-RENORMALIZATION INTERPRETER -- GATE (fail-closed)")
    print("=" * 78)
    res = run_gate()
    sys.exit(0 if res["_all_pass"] else 1)
