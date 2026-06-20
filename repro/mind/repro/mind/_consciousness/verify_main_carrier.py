#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_main_carrier.py  --  re-emerge the M16-study and check it against the frozen
hash + invariants. Exit 0 iff (a) the headline sha256 reproduces bit-for-bit, (b) the
frozen scalar invariants match, and (c) all gate self-checks pass.
Run:  python3 verify_main_carrier.py
"""
import os, sys, json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import vp_main_carrier_emergence as M   # noqa: E402

TOL = 1e-9
exp = json.load(open(os.path.join(_HERE, "expected_main_carrier_sha256.json")))


def _get(res, dotted):
    cur = res
    for k in dotted.split("."):
        cur = cur[k]
    return cur


# map the flat invariant names back to their result paths
PATHS = {
    "carrier_over_slow_ratio": "A_source.carrier_over_slow_ratio",
    "parallel_capacity_slots": "D_parallel.parallel_capacity_slots",
    "recall_structured_carrier": "B_state.recall_structured_carrier",
    "big_unstructured_recall": "B_state.big_unstructured_recall",
    "recall_metastable_measured": "C_metastable.recall_metastable_measured",
    "recall_globalsync_seizure": "C_metastable.recall_globalsync_seizure",
    "reinstatement_fidelity_mean": "D_parallel.reinstatement_fidelity_mean",
    "crosstalk_mean": "D_parallel.crosstalk_mean",
    "medium_efficacy_tested": "honesty.medium_efficacy_tested",
    "hard_problem_open": "honesty.hard_problem_open",
    "new_tuned_constants": "honesty.new_tuned_constants",
}


def main():
    res, checks, n_pass = M.run()
    ok = True

    # (a) bit-identical hash
    if res["headline_sha256"] != exp["headline_sha256"]:
        print(f"  [FAIL] headline_sha256 drift\n    got {res['headline_sha256']}\n    exp {exp['headline_sha256']}")
        ok = False
    else:
        print(f"  [PASS] headline_sha256 = {res['headline_sha256']}")

    # (b) frozen invariants
    for name, ref in exp["frozen_invariants"].items():
        got = _get(res, PATHS[name])
        same = (abs(float(got) - float(ref)) < TOL) if isinstance(ref, (int, float)) else (got == ref)
        print(f"  [{'PASS' if same else 'FAIL'}] {name}: {got}" + ("" if same else f" (exp {ref})"))
        ok = ok and same

    # (c) full gate
    for cname, cok in checks:
        if not cok:
            print(f"  [FAIL] gate.{cname}")
            ok = False
    print(f"  gate: {n_pass}/{len(checks)} checks PASS")

    print("-" * 60)
    if ok and n_pass == len(checks):
        print(f"VERIFY PASS -- {len(checks)} gate checks + {len(exp['frozen_invariants'])} invariants + bit-identical hash")
        sys.exit(0)
    print("VERIFY FAIL")
    sys.exit(1)


if __name__ == "__main__":
    main()
