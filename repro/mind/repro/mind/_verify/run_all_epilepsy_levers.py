#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_epilepsy_levers.py  —  T2a-L harness. Runs the four inherited components in order and
reports OVERALL. The map is built first; the two fail-closed gates and the prioritisation read it.

  1. epilepsy_threshold_levers.py        the DNA-grounded three-lever map (deterministic, 2x sha256)
  2. epilepsy_burden_prioritisation.py   burden-weighted TARGET prioritisation (declared weights)
  3. epilepsy_l3_honesty.py              fail-closed: every L3 mTOR mechanism link graded [O]
  4. epilepsy_forbidden_claim_scan.py    fail-closed: no dose/efficacy/safety/synthesis claim leaks

Inherited from the bipolar T2b-L harness (analgesic_threshold_logic v2.0, DOI 10.5281/zenodo.20733420).
KCNQ2/KCNQ3/KCNB1/SCN2A/GRIN2A gamma values reuse the bipolar promoter cache verbatim. Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   three-lever map",        "epilepsy_threshold_levers.py"),
    ("PRIO  burden prioritisation",  "epilepsy_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "epilepsy_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "epilepsy_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("T2a-L  EPILEPSY THREE-LEVER HARNESS  (inherited bipolar T2b-L / analgesic v2.0)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_epilepsy_threshold_levers_sha256.json")))
    digest = h["epilepsy_threshold_levers_results.json"]
    rc2, _, _ = run("epilepsy_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_epilepsy_threshold_levers_sha256.json")))["epilepsy_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  T2a-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
