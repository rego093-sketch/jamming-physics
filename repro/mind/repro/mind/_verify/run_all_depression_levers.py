#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_depression_levers.py  —  T1b-L harness. Runs the four inherited components in order and
reports OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. depression_threshold_levers.py        the DNA-grounded three-lever map (deterministic, 2x sha256)
  2. depression_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. depression_l3_honesty.py               fail-closed: every L3 upstream-drive link graded [O]
  4. depression_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis claim leaks

Inherited from the epilepsy T2a-L / bipolar T2b-L harness (analgesic_threshold_logic v2.0,
DOI 10.5281/zenodo.20733420). Unlike the channel-led bipolar/epilepsy cases, depression is
L3-DOMINANT (upstream HPA / monoamine / neurotrophic drives carry the map). NR3C1/CRHR1/GRIN2A/
CACNA1C/KCNQ2/KCNQ3 gamma values reuse the bipolar promoter cache verbatim; GABRA1 reuses the
epilepsy cache verbatim (gamma is strand-symmetric). Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   three-lever map",        "depression_threshold_levers.py"),
    ("PRIO  burden prioritisation",  "depression_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "depression_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "depression_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("T1b-L  DEPRESSION THREE-LEVER HARNESS  (inherited epilepsy T2a-L / bipolar T2b-L)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_depression_threshold_levers_sha256.json")))
    digest = h["depression_threshold_levers_results.json"]
    rc2, _, _ = run("depression_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_depression_threshold_levers_sha256.json")))["depression_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  T1b-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
