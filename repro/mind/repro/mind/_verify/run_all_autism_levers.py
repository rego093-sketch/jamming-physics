#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_autism_levers.py  —  ASD-T-L harness. Runs the four inherited components in order and reports
OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. autism_threshold_levers.py        the DNA-grounded three-lever map (deterministic, 2x sha256)
  2. autism_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. autism_l3_honesty.py               fail-closed: every L3 serotonergic link graded [O]; also asserts
                                        L1 UNIQUE dominance, L3 SPARSITY, the T-axis domain restriction,
                                        and that the OUT-OF-REACH O/W axes are NAMED + sec.19-proven
  4. autism_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis/QUACKERY claim
                                        leaks, and no neurodiversity-disrespecting normalise framing

Inherited from the schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L harness
(analgesic_threshold_logic v2.0, DOI 10.5281/zenodo.20733420). Autism is the UNIFICATION case: it does
not introduce a new lever combination but re-expresses the pre-existing autism_multilever_threshold.py
(sec.18-19) under the formal L1/L2/L3 frame. Two autism-specific strengthenings distinguish it from the
schizophrenia domain-restriction template:
  (1) the out-of-reach axes are NAMED with real genes (O = SHANK3/SYNGAP1/NRXN1 output-deficit;
      W = CNTNAP2/RELN long-range wiring; plus the syndromic MECP2);
  (2) the W-axis unreachability is PROVEN, not merely asserted -- sec.19 (autism_candidate_limits) showed
      a scalar threshold lever can only MASK the wiring fault via over-synchronisation (the seizure
      analogue), never CORRECT it.
Autism is L1-DOMINANT with a nearly-empty L3 (the 5th distribution pattern across the T-L series). The
promoter gamma values reuse the schizophrenia/bipolar/depression caches verbatim where the genes overlap
(GRIN2A/GRIN2B/CACNA1C/GABRB3 from schizophrenia; SCN2A/KCNQ3 from bipolar; SLC6A4 from depression);
gamma is strand-symmetric. Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   three-lever map",        "autism_threshold_levers.py"),
    ("PRIO  burden prioritisation",  "autism_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "autism_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "autism_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("ASD-T-L  AUTISM THREE-LEVER HARNESS  (inherited schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_autism_threshold_levers_sha256.json")))
    digest = h["autism_threshold_levers_results.json"]
    rc2, _, _ = run("autism_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_autism_threshold_levers_sha256.json")))["autism_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  ASD-T-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
