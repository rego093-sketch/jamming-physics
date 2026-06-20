#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_alzheimers_levers.py  —  AD-T-L harness. Runs the four inherited components in order and reports
OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. alzheimers_threshold_levers.py        the DNA-grounded symptomatic-network map (deterministic, 2x sha256)
  2. alzheimers_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. alzheimers_l3_honesty.py               fail-closed: every L3 cholinergic-drive link graded [O]; also
                                            asserts L3 UNIQUE dominance + L1/L2 BOTH present, the SYMPTOMATIC
                                            domain restriction with SPLIT corrective sign, and the PROG
                                            neurodegenerative-progression axis NAMED out-of-reach -- the
                                            THIRD and DEEPEST PARTIAL [L] fit
  4. alzheimers_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis claim leaks, and
                                            no cure/reversal/prevention licence and no dignity violation

Inherited from the schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism
ASD-T-L / ADHD T3a-L / addiction ADD-T-L harness (analgesic_threshold_logic v2.0,
DOI 10.5281/zenodo.20733420). Alzheimer's is the THIRD and DEEPEST PARTIAL [L] fit of the series: it
re-expresses the cholinergic / glutamatergic-excitotoxicity / inhibitory-network substrate under the
formal L1/L2/L3 frame by REACHABILITY, and the frame reaches the INSTANTANEOUS symptomatic operating
point but NOT the dominant neurodegenerative-progression fault. Three Alzheimer's-specific properties
distinguish it from the ADHD and addiction partial-fit templates:
  (1) the reachable surface is PURELY SYMPTOMATIC with a SPLIT corrective sign -- L3 cholinergic drive
      is RESTORED (deficient tone up), L1 glutamatergic excitotoxicity is REDUCED (excess drive down),
      L2 inhibitory tone is RESTORED against network hyperexcitability -- the FIRST reachable surface in
      the series that is both purely symptomatic AND split-sign (the 8th distribution pattern; gross
      shape shared with addiction's L3-dominant-plus-L1/L2 but distinguished by split sign and
      symptomatic-only reach);
  (2) the out-of-reach axis is the DOMINANT one and is reached for the DEEPEST reason in the series:
      the PROG neurodegenerative-progression genes (APP/PSEN1/PSEN2/MAPT/APOE/TREM2) are NAMED
      out-of-reach because PROG is a GAIN/loss not a fold (the ADHD lesson), AND a PROGRESSION over
      time -- a plasticity (E0-layer) variable (the addiction lesson), AND moreover a DEGENERATION --
      a cumulative, irreversible LOSS, an E0 DECAY that is the structural INVERSE of addiction's E0
      GAIN; so even a drive lever that restores instantaneous tone cannot HALT the cumulative loss;
      this is exactly why the fit is PARTIAL [L] and the DEEPEST one;
  (3) the symptomatic firewall is binding: the cholinesterase-inhibitor and memantine routes are
      SYMPTOMATIC ONLY and do NOT slow progression; the anti-amyloid antibodies (lecanemab/donanemab)
      target the out-of-reach PROG axis and are progression-modifiers, not threshold levers; a person
      living with dementia remains a person.
The promoter gamma values reuse the autism/epilepsy caches verbatim where the genes overlap
(GRIN2A/GRIN2B/GABRA5/GABRB3 from autism; GABRA1 from epilepsy) and live-fetch the new genes
(ACHE/BCHE/CHRNA7/CHRM1/APP/PSEN1/PSEN2/MAPT/APOE/TREM2, GRCh38, strand-aware); gamma is
strand-symmetric. Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   symptomatic-network map",   "alzheimers_threshold_levers.py"),
    ("PRIO  burden prioritisation",     "alzheimers_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)",  "alzheimers_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "alzheimers_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def _sha(fn):
    return hashlib.sha256(open(os.path.join(HERE, fn), "rb").read()).hexdigest()

if __name__ == "__main__":
    print("=" * 78); print("AD-T-L  ALZHEIMER'S SYMPTOMATIC-NETWORK HARNESS  (inherited schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism ASD-T-L / ADHD T3a-L / addiction ADD-T-L; THIRD & DEEPEST PARTIAL [L] fit)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + TRUE determinism re-check: re-run the map and re-hash the produced results.json
    expected = json.load(open(os.path.join(HERE, "expected_alzheimers_threshold_levers_sha256.json")))["alzheimers_threshold_levers_results.json"]
    run("alzheimers_threshold_levers.py")
    digest = _sha("alzheimers_threshold_levers_results.json")
    determ = bool(digest == expected)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  expected sha256   : {expected}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  AD-T-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
