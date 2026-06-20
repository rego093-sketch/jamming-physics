#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pathology_verify.py  --  Integumentary DISEASE battery (analogue of stress_tests.py for pathology).

Each disease is graded on a binary CLINICAL-SIGN test (does the mechanism reproduce the cited
direction / threshold / discontinuity?) AND an INTERVENTION test (does reversing the same knob undo
it?). A silent pass is not allowed: every suite reports the discriminant values it checked, the grade,
and the [O] obstacle (inherited from the parent target). The opposite-sign discriminant -- the same
R19 switch reproducing clinically OPPOSITE pairs with NO new constant -- is the headline check.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import skin_pathology as P


def _suite(d):
    ok = bool(d.get("sign_matches_clinic") and d.get("intervention_reverses"))
    return dict(disease=d["disease"], target=d["target"], organ=d["organ"], status="PASS" if ok else "FAIL",
                mechanism=d["mechanism"], anchor=d["anchor"],
                sign_matches_clinic=d.get("sign_matches_clinic"), intervention_reverses=d.get("intervention_reverses"),
                grade=d["grade_shape"], obstacle_if_open=d["grade_absolute"])


def run_battery(summary=None):
    res = summary if summary is not None else P.pathology_summary()
    suites = [_suite(v) for k, v in res.items() if not k.startswith("_")]
    disc = res["_opposite_sign_discriminant"]
    all_pass = all(s["status"] == "PASS" for s in suites) and bool(disc["all_opposite_pairs_reproduced"])
    return dict(n_diseases=res["_n_diseases"], suites=suites,
                opposite_sign_discriminant=disc, all_diseases_pass=all_pass)


def determinism_ok():
    _, h1 = P._emit(P.pathology_summary()); _, h2 = P._emit(P.pathology_summary())
    return h1 == h2, h1


if __name__ == "__main__":
    b = run_battery()
    det, h = determinism_ok()
    print(json.dumps(b, ensure_ascii=False, indent=2))
    print("\ndeterminism 2xsha256 identical:", det, "(sha=%s...)" % h[:16])
    print("ALL DISEASES PASS:", b["all_diseases_pass"])
