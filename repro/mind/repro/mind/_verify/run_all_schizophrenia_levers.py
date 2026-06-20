#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_schizophrenia_levers.py  —  T1a-L harness. Runs the four inherited components in order and
reports OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. schizophrenia_threshold_levers.py        the DNA-grounded three-lever map (deterministic, 2x sha256)
  2. schizophrenia_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. schizophrenia_l3_honesty.py               fail-closed: every L3 dopamine-axis link graded [O]; also
                                               asserts L1+L3 CO-DOMINANCE and the POSITIVE-domain restriction
  4. schizophrenia_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis claim leaks

Inherited from the depression T1b-L / epilepsy T2a-L / bipolar T2b-L harness (analgesic_threshold_logic
v2.0, DOI 10.5281/zenodo.20733420). Schizophrenia is the FIRST L1+L3 CO-DOMINANT case (the glutamate/
NMDA axis and the dopamine antipsychotic axis carry the map jointly, 6 targets each), and the FIRST
DOMAIN-RESTRICTED case (the lever map reaches the POSITIVE/aberrant-salience domain ONLY; the negative
output-deficit and cognitive wiring domains are NOT reached). GRIN2A/CACNA1C/CACNB2 gamma values reuse
the bipolar promoter cache verbatim; GRIN2B/COMT/HTR2A/GABRA1 reuse the depression cache verbatim; the
remaining genes reuse the disease/ADHD promoter caches verbatim (gamma is strand-symmetric). Engine
READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   three-lever map",        "schizophrenia_threshold_levers.py"),
    ("PRIO  burden prioritisation",  "schizophrenia_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "schizophrenia_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "schizophrenia_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("T1a-L  SCHIZOPHRENIA THREE-LEVER HARNESS  (inherited depression T1b-L / epilepsy T2a-L / bipolar T2b-L)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_schizophrenia_threshold_levers_sha256.json")))
    digest = h["schizophrenia_threshold_levers_results.json"]
    rc2, _, _ = run("schizophrenia_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_schizophrenia_threshold_levers_sha256.json")))["schizophrenia_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  T1a-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
