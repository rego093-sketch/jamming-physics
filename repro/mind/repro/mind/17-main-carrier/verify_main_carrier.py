#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHAPTER 17 -- MAIN HIGH-FREQUENCY CARRIER  (promoted verify, v1.19)
===================================================================
The main carrier was promoted from the standalone study into the engine as M16 (v1.19,
Task 2A). This chapter verify asserts that the PROMOTED ENGINE reproduces the carrier
result bit-for-bit and that the study's 13 gates still pass on it. Exit 0 iff:

  (a) the engine's M16 headline sha256 (read from the frozen engine output
      mind_emergence_results.json) equals the locked study headline 8d05cfec... -- a single
      hash equality that certifies EVERY field of the promoted M16 (the 13-gate inputs and
      the 11 invariants) matches the study output bit-for-bit;
  (b) the engine's M16 eleven frozen invariants match expected_main_carrier_sha256.json;
  (c) re-running the study reproduces the SAME headline and all 13 gate self-checks PASS
      (the gates are thus validated against exactly the result the engine reproduces);
  (d) the engine regression_scalars mc_* carrier invariants equal the same frozen values
      (the carrier is locked in the always-run regression, not only here).

NOTE: M16 is a measured-grounded MEASUREMENT, NOT a consciousness claim -- medium efficacy 0,
hard problem OPEN, consciousness_claim 0, PCI honest negative. The slow leg the carrier:slow
ratio rides on is the engine [O] tau_inh=60; the theta-pacing anchor is OWED [O] (Task 2B).

Run:  python3 verify_main_carrier.py          (from 17-main-carrier/)
"""
import os, sys, json

_HERE   = os.path.dirname(os.path.abspath(__file__))
_ENGINE = os.path.normpath(os.path.join(_HERE, "..", "_engine"))
_STUDY  = os.path.normpath(os.path.join(_HERE, "..", "_consciousness"))
sys.path.insert(0, _ENGINE)
sys.path.insert(0, _STUDY)

TOL = 1e-9
exp = json.load(open(os.path.join(_HERE, "expected_main_carrier_sha256.json")))

# the promoted engine output (frozen by run_all.py) and its locked regression scalars
RES = json.load(open(os.path.join(_ENGINE, "results", "mind_emergence_results.json")))
SCAL = json.load(open(os.path.join(_ENGINE, "results", "regression_scalars.json")))
M16 = RES["M16_main_carrier"]

PATHS = {
    "carrier_over_slow_ratio": ("A_source", "carrier_over_slow_ratio"),
    "parallel_capacity_slots": ("D_parallel", "parallel_capacity_slots"),
    "recall_structured_carrier": ("B_state", "recall_structured_carrier"),
    "big_unstructured_recall": ("B_state", "big_unstructured_recall"),
    "recall_metastable_measured": ("C_metastable", "recall_metastable_measured"),
    "recall_globalsync_seizure": ("C_metastable", "recall_globalsync_seizure"),
    "reinstatement_fidelity_mean": ("D_parallel", "reinstatement_fidelity_mean"),
    "crosstalk_mean": ("D_parallel", "crosstalk_mean"),
    "medium_efficacy_tested": ("honesty", "medium_efficacy_tested"),
    "hard_problem_open": ("honesty", "hard_problem_open"),
    "new_tuned_constants": ("honesty", "new_tuned_constants"),
}
# the matching flat names in regression_scalars (mc_*)
SCAL_KEYS = {
    "carrier_over_slow_ratio": "mc_carrier_over_slow_ratio",
    "parallel_capacity_slots": "mc_parallel_capacity_slots",
    "recall_structured_carrier": "mc_recall_structured_carrier",
    "big_unstructured_recall": "mc_big_unstructured_recall",
    "recall_metastable_measured": "mc_recall_metastable_measured",
    "recall_globalsync_seizure": "mc_recall_globalsync_seizure",
    "reinstatement_fidelity_mean": "mc_reinstatement_fidelity_mean",
    "crosstalk_mean": "mc_crosstalk_mean",
    "medium_efficacy_tested": "mc_medium_efficacy_tested",
    "hard_problem_open": "mc_hard_problem_open",
    "new_tuned_constants": "mc_new_tuned_constants",
}


def _eq(a, b):
    return (abs(float(a) - float(b)) < TOL) if isinstance(b, (int, float)) else (a == b)


def main():
    ok = True

    # (a) engine M16 headline == locked study headline (certifies all M16 fields bit-for-bit)
    if M16["headline_sha256"] != exp["headline_sha256"]:
        print(f"  [FAIL] engine M16 headline drift\n    got {M16['headline_sha256']}\n    exp {exp['headline_sha256']}")
        ok = False
    else:
        print(f"  [PASS] engine M16 headline_sha256 = {M16['headline_sha256']}")

    # (b) engine M16 invariants match the frozen study invariants
    for name, ref in exp["frozen_invariants"].items():
        a, b = PATHS[name]
        got = M16[a][b]
        same = _eq(got, ref)
        print(f"  [{'PASS' if same else 'FAIL'}] engine M16 {name}: {got}" + ("" if same else f" (exp {ref})"))
        ok = ok and same

    # (c) re-run the study: same headline + all 13 gates pass on the reproduced result
    import vp_main_carrier_emergence as M  # noqa: E402
    sres, checks, n_pass = M.run()
    if sres["headline_sha256"] != exp["headline_sha256"]:
        print(f"  [FAIL] study headline drift {sres['headline_sha256']}"); ok = False
    if sres["headline_sha256"] != M16["headline_sha256"]:
        print(f"  [FAIL] engine M16 != study result (headline mismatch)"); ok = False
    else:
        print(f"  [PASS] engine M16 == study result (bit-for-bit, same headline)")
    for cname, cok in checks:
        if not cok:
            print(f"  [FAIL] gate.{cname}"); ok = False
    print(f"  [{'PASS' if n_pass == len(checks) else 'FAIL'}] study gates: {n_pass}/{len(checks)} "
          f"(expected {exp['gate_checks_pass']}/{exp['gate_checks_total']})")
    ok = ok and (n_pass == len(checks) == exp["gate_checks_total"])

    # (d) the always-run regression locks the same carrier invariants (mc_*)
    for name, ref in exp["frozen_invariants"].items():
        got = SCAL[SCAL_KEYS[name]]
        same = _eq(got, ref)
        if not same:
            print(f"  [FAIL] regression mc {name}: {got} (exp {ref})"); ok = False
    print(f"  [{'PASS' if ok else 'FAIL'}] regression_scalars mc_* carrier invariants locked")

    print("-" * 64)
    if ok:
        print(f"VERIFY PASS -- promoted engine M16 reproduces the carrier "
              f"({exp['gate_checks_total']} gates + {len(exp['frozen_invariants'])} invariants + "
              f"bit-identical headline); NOT a consciousness claim (efficacy 0, hard problem OPEN).")
        sys.exit(0)
    print("VERIFY FAIL")
    sys.exit(1)


if __name__ == "__main__":
    main()
