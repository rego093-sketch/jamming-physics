#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_addiction_levers.py  —  ADD-T-L harness. Runs the four inherited components in order and reports
OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. addiction_threshold_levers.py        the DNA-grounded reward-drive map (deterministic, 2x sha256)
  2. addiction_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. addiction_l3_honesty.py               fail-closed: every L3 reward-drive link graded [O]; also asserts
                                           L3 UNIQUE dominance + L1/L2 BOTH present (the ADHD inverse), the
                                           INSTANT-axis domain restriction, and the SG out-of-reach axis
                                           NAMED -- the SECOND PARTIAL [L] fit
  4. addiction_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis claim leaks, and
                                           no drug-seeking or cure-miracle licence

Inherited from the schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism
ASD-T-L / ADHD T3a-L harness (analgesic_threshold_logic v2.0, DOI 10.5281/zenodo.20733420). Addiction is
the SECOND PARTIAL [L] fit of the series: it re-expresses the sec.28 state-switching / sec.26 E0 plasticity
incentive-sensitisation substrate under the formal L1/L2/L3 frame by REACHABILITY, and the frame reaches
the INSTANTANEOUS drive/excitability operating point richly but NOT the dominant consolidated-gain fault.
Three addiction-specific properties distinguish it from the ADHD partial-fit template:
  (1) addiction is L3-DOMINANT but NOT L3-only: L1 (glutamate-plasticity substrate) and L2 (inhibitory
      restore) are BOTH present -- the 7th distribution pattern and the TEXTURAL INVERSE of ADHD's
      L3-only emptiness (ADHD was 'not a channelopathy'; addiction engages the ionic levers too);
  (2) the out-of-reach axis is the DOMINANT one and is reached for a DEEPER reason than ADHD: the SG
      consolidated-sensitisation-gain genes (FOSB/BDNF/CREB1/ARC) are NAMED out-of-reach because SG is a
      GAIN not a fold (the ADHD lesson) AND moreover CONSOLIDATED/LEARNED -- a plasticity (E0-layer)
      variable -- so even a drive lever that dampens the instantaneous response cannot ERASE the durable
      trace; this is exactly why the fit is PARTIAL [L];
  (3) the SG axis is precisely the E0 plasticity layer (sec.26) -- addiction is the CONVERGENCE point
      where threshold-leverisation (B-i) structurally meets the dynamics route (B-ii); B-i NAMES the
      learned trace out-of-reach honestly.
The promoter gamma values reuse the schizophrenia/depression/autism/ADHD caches verbatim where the genes
overlap (DRD2 from schizophrenia; BDNF from depression; GRIN2A/GRIN2B/GABRA2 from autism; SLC6A3 from
ADHD) and live-fetch the new genes (OPRM1/OPRK1/CHRNA5/GABRG3/FOSB/CREB1/ARC, GRCh38, strand-aware);
gamma is strand-symmetric. Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   reward-drive map",         "addiction_threshold_levers.py"),
    ("PRIO  burden prioritisation",    "addiction_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "addiction_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "addiction_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

if __name__ == "__main__":
    print("=" * 78); print("ADD-T-L  ADDICTION REWARD-DRIVE HARNESS  (inherited schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism ASD-T-L / ADHD T3a-L; SECOND PARTIAL [L] fit)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + determinism re-check
    h = json.load(open(os.path.join(HERE, "expected_addiction_threshold_levers_sha256.json")))
    digest = h["addiction_threshold_levers_results.json"]
    rc2, _, _ = run("addiction_threshold_levers.py")
    h2 = json.load(open(os.path.join(HERE, "expected_addiction_threshold_levers_sha256.json")))["addiction_threshold_levers_results.json"]
    determ = bool(digest == h2)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  ADD-T-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
