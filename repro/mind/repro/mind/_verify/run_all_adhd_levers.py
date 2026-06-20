#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_adhd_levers.py  —  ADHD-T-L harness. Runs the four inherited components in order and reports
OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. adhd_threshold_levers.py        the DNA-grounded drive-tone map (deterministic, 2x sha256)
  2. adhd_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. adhd_l3_honesty.py               fail-closed: every L3 drive-tone link graded [O]; also asserts
                                      L3 UNIQUE dominance + L1/L2 BOTH empty (L3-only), the DT-axis
                                      domain restriction, the GA out-of-reach axis NAMED, the W axis
                                      ABSENT (the discriminant), and the PARTIAL [L] fit
  4. adhd_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis claim leaks, and
                                      no stimulant-misuse or cognitive-enhancement licence

Inherited from the schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism
ASD-T-L harness (analgesic_threshold_logic v2.0, DOI 10.5281/zenodo.20733420). ADHD is the FIRST PARTIAL
[L] fit of the series: it re-expresses the sec.22 adhd_axis_specific substrate (gain/arousal with INTACT
wiring) under the formal L1/L2/L3 frame by REACHABILITY, and the frame reaches only the SECONDARY axis.
Three ADHD-specific properties distinguish it from the autism domain-restriction template:
  (1) ADHD is L3-ONLY (L1 and L2 BOTH empty) -- the 6th and purest distribution pattern across the T-L
      series; every reachable lever is an upstream catecholamine/monoaminergic drive-tone node;
  (2) the out-of-reach axis is the DOMINANT one: the GA gain-amplitude genes (TH/DBH/SNAP25 synthesis/
      release, + COMT clearance boundary) are NAMED out-of-reach -- a drive-tone lever has no handle on
      synthesis/release -- which is exactly why the fit is PARTIAL [L], not the clean [V] of the five
      prior disorders (the dominant axis is the out-of-reach one);
  (3) the W (long-range wiring) axis is ABSENT from the disorder -- ADHD has INTACT wiring (sec.22) -- the
      DISCRIMINANT from autism and the autism INVERSE (autism reached its dominant T axis and missed O+W;
      ADHD reaches only the secondary DT axis and misses the dominant GA axis, with no W axis at all).
The promoter gamma values reuse the schizophrenia/depression caches verbatim where the genes overlap
(SLC6A3/DRD4/COMT/TH from schizophrenia; SLC6A4/SLC6A2 from depression) and live-fetch the three new
genes (ADRA2A/DBH/SNAP25, GRCh38, strand-aware); gamma is strand-symmetric. Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   drive-tone map",          "adhd_threshold_levers.py"),
    ("PRIO  burden prioritisation",   "adhd_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "adhd_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "adhd_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("ADHD-T-L  ADHD DRIVE-TONE HARNESS  (inherited schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism ASD-T-L; FIRST PARTIAL [L] fit)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_adhd_threshold_levers_sha256.json")))
    digest = h["adhd_threshold_levers_results.json"]
    rc2, _, _ = run("adhd_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_adhd_threshold_levers_sha256.json")))["adhd_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  ADHD-T-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
