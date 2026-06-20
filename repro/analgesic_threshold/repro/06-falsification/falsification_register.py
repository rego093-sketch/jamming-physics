#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
falsification_register.py  —  M6: a named, measurable falsifier for every proposal.
A proposal you cannot kill is not science. Gate: every proposal id in M5 has >=1 falsifier.
Run:  python3 falsification_register.py  -> expected/falsification.json
"""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PROP = os.path.normpath(os.path.join(HERE, "..", "05-intervention-logic", "proposal.json"))

FALSIFIERS = {
  "P1": "If a peripherally-restricted modulation of the nociceptor gate fails to lower nociceptive firing in DRG recordings while a central intervention does, the peripheral-gate premise is wrong.",
  "P2": "If, at every setting that raises the gate threshold, protective withdrawal reflexes are also abolished (no therapeutic window between innocuous-input silence and loss of protection), the 'controlled return, not overshoot' premise fails.",
  "P3": "If a LESS nociceptor-selective Na_V (e.g. Na_V1.7) yields cleaner threshold elevation with fewer off-target effects than the MORE selective Na_V1.8, the selectivity-based ranking is falsified.",
  "P4": "If a non-state-dependent (tonic) gate modulator matches a closed/inactivated-state-stabilising one in raising threshold WITHOUT impairing normal low-frequency conduction, the 'closed-state shape is required' premise is unnecessary.",
  "P5": "If a peripherally-restricted nociceptor-gate modulator nonetheless produces reward/reinforcement signals (e.g. self-administration) attributable to the target, the 'structurally spares central reward circuitry' rationale is falsified.",
  "P6": "If opening the nociceptor-selective entry port (TRPV1/TRPA1) does NOT yield a differential, pain-selective block - i.e. motor and light-touch fibres are blocked as much as nociceptive fibres - then the entry-port-selectivity premise behind precision local anaesthesia is wrong for that port/tissue (the differential-block prediction of M12 is killed).",
  "FRAMEWORK": "If the gamma-derived |h_sp| ordering of the target set is uncorrelated with ANY independent promoter-switch readout (expression-threshold assay), the read's organising relevance to these loci is weakened (the read remains [V] as a number, but its claim to order the gate would not hold)."
}

if __name__ == "__main__":
    prop = json.load(open(PROP))
    ids = [p["id"] for p in prop["proposals"]]
    missing = [i for i in ids if i not in FALSIFIERS]
    out = {"title": "Falsification register", "falsifiers": FALSIFIERS,
           "proposal_ids": ids, "missing": missing,
           "overall": "PASS" if not missing else "FAIL"}
    json.dump(out, open(os.path.join(HERE, "expected", "falsification.json"), "w"), indent=1)
    print("M6 falsification register")
    for i in ids: print(f"  [{'OK' if i in FALSIFIERS else 'MISSING'}] {i}: {FALSIFIERS.get(i,'—')[:80]}...")
    print("  [OK] FRAMEWORK-level falsifier present")
    print("OVERALL:", out["overall"])
    raise SystemExit(0 if not missing else 1)
