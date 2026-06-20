#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_bipolar_levers.py  —  T2b-L harness. Runs the four inherited components in order and
reports OVERALL. The map is built first; the two fail-closed gates and the prioritisation read it.

  1. bipolar_threshold_levers.py        the DNA-grounded three-lever map (deterministic, 2x sha256)
  2. bipolar_burden_prioritisation.py   burden-weighted TARGET prioritisation (declared weights)
  3. bipolar_l3_honesty.py              fail-closed: every L3 mechanism link graded [O]
  4. bipolar_forbidden_claim_scan.py    fail-closed: no dose/efficacy/safety/synthesis claim leaks

Inherited from analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420). Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   three-lever map",        "bipolar_threshold_levers.py"),
    ("PRIO  burden prioritisation",  "bipolar_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "bipolar_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "bipolar_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("T2b-L  BIPOLAR THREE-LEVER HARNESS  (inherited analgesic v2.0 technology)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_bipolar_threshold_levers_sha256.json")))
    digest = h["bipolar_threshold_levers_results.json"]
    rc2, _, _ = run("bipolar_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_bipolar_threshold_levers_sha256.json")))["bipolar_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  T2b-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
