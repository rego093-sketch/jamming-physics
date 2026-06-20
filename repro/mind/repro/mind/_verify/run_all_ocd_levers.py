#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_ocd_levers.py  —  OCD-T-L harness. Runs the four inherited components in order and reports
OVERALL. The map is built first; the prioritisation and the two fail-closed gates read it.

  1. ocd_threshold_levers.py        the DNA-grounded CSTC-loop map (deterministic, 2x sha256)
  2. ocd_burden_prioritisation.py    burden-weighted TARGET prioritisation (declared weights)
  3. ocd_l3_honesty.py               fail-closed: every L3 serotonergic/dopaminergic-drive link graded
                                     [O]; also asserts L3 UNIQUE dominance + L1 present + L2 SPARSE, the
                                     INSTANT domain restriction with a MIXED corrective sign, and the LOCK
                                     pathological-stabilisation axis NAMED out-of-reach -- the FOURTH
                                     PARTIAL [L] fit and a NEW MODE (a STABILISATION / LOCK)
  4. ocd_forbidden_claim_scan.py     fail-closed: no dose/efficacy/safety/synthesis claim leaks, and no
                                     cure/miracle and no moral-framing/stigma violation

Inherited from the schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism
ASD-T-L / ADHD T-L / addiction ADD-T-L / Alzheimer's AD-T3b-L harness (analgesic_threshold_logic v2.0,
DOI 10.5281/zenodo.20733420). OCD is the FOURTH PARTIAL [L] fit of the series and a NEW MODE: it
re-expresses the cortico-striato-thalamo-cortical (CSTC) loop substrate under the formal L1/L2/L3 frame by
REACHABILITY, and the frame reaches the INSTANTANEOUS CSTC excitability operating point but NOT the
dominant pathological loop-LOCK. Three OCD-specific properties distinguish it from the ADHD / addiction /
Alzheimer's partial-fit templates:
  (1) the reachable surface is L3-DOMINANT with L1 STRONG and L2 SPARSE (a single weak inhibitory node) --
      the NINTH distribution pattern (OCD's GABAergic arm is thin, itself a finding) -- with a MIXED/split
      corrective sign (RESTORE the serotonergic tone and inhibition, REDUCE the dopaminergic and
      glutamatergic drive); and unlike Alzheimer's purely-symptomatic surface, the OCD levers are the
      actual mainstay/investigational routes and genuinely (PARTIALLY) help;
  (2) the out-of-reach axis is the DOMINANT one and is a NEW MODE: the LOCK pathological-stabilisation
      genes (DLGAP3/SAPAP3, SLITRK5, PTPRD, BTBD3) are NAMED out-of-reach because LOCK is a GAIN/loss not
      a fold (the ADHD lesson), AND a consolidated/learned plasticity (E0-layer) variable (the addiction
      lesson), AND moreover a pathological STABILISATION / LOCK -- an over-deep basin / hysteresis (an E2
      phenomenon), the THIRD distinct E0 mode after addiction's E0 GAIN and Alzheimer's E0 DECAY; so even
      a drive lever that nudges the instantaneous operating point cannot UNSTICK the loop; this is exactly
      why the fit is PARTIAL [L];
  (3) the firewall is binding: the serotonergic/glutamate/dopamine/GABA routes are mechanism DIRECTIONS,
      the loop-LOCK is out of reach (a deep-brain-stimulation dynamics intervention -- not a threshold
      lever -- is the handle), OCD is a treatable medical condition, and intrusive thoughts are a symptom,
      not a moral failing.
The promoter gamma values reuse the depression/addiction/autism/epilepsy caches verbatim where the genes
overlap (SLC6A4/HTR2A from depression; DRD2 from addiction; GRIN2B from autism; GABRA1 from epilepsy) and
live-fetch the new genes (HTR1B/SLC1A1/GRIK2/DLGAP3/SLITRK5/PTPRD/BTBD3, GRCh38, strand-aware); gamma is
strand-symmetric. Engine READ-ONLY.
"""
import os, sys, json, subprocess, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("MAP   CSTC-loop map",            "ocd_threshold_levers.py"),
    ("PRIO  burden prioritisation",    "ocd_burden_prioritisation.py"),
    ("GATE  L3 honesty (fail-closed)", "ocd_l3_honesty.py"),
    ("GATE  forbidden-claim (fail-closed)", "ocd_forbidden_claim_scan.py"),
]
def run(py):
    r = subprocess.run([sys.executable, os.path.join(HERE, py)], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def _sha(fn):
    return hashlib.sha256(open(os.path.join(HERE, fn), "rb").read()).hexdigest()

if __name__ == "__main__":
    print("=" * 78); print("OCD-T-L  OCD CSTC-LOOP HARNESS  (inherited schizophrenia T1a-L / depression T1b-L / epilepsy T2a-L / bipolar T2b-L / autism ASD-T-L / ADHD T-L / addiction ADD-T-L / Alzheimer's AD-T3b-L; FOURTH PARTIAL [L] fit, LOCK=3rd E0 mode)"); print("=" * 78)
    allok = True
    for label, py in STEPS:
        rc, out, err = run(py)
        tail = [l for l in out.strip().splitlines() if l.strip()][-1] if out.strip() else (err.strip().splitlines()[-1] if err.strip() else "")
        print(f"  [{'PASS' if rc == 0 else 'FAIL'}] {label:38} -> {tail[:60]}")
        allok = allok and rc == 0
    # headline hash + TRUE determinism re-check: re-run the map and re-hash the produced results.json
    expected = json.load(open(os.path.join(HERE, "expected_ocd_threshold_levers_sha256.json")))["ocd_threshold_levers_results.json"]
    run("ocd_threshold_levers.py")
    digest = _sha("ocd_threshold_levers_results.json")
    determ = bool(digest == expected)
    print("-" * 78)
    print(f"  map result sha256 : {digest}")
    print(f"  expected sha256   : {expected}")
    print(f"  determinism (2x)  : {determ}")
    print("=" * 78)
    print("  OCD-T-L HARNESS: " + ("ALL PASS" if (allok and determ) else "FAIL"))
    sys.exit(0 if (allok and determ) else 1)
