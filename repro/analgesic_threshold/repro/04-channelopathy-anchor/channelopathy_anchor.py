#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
channelopathy_anchor.py  —  M4: anchor the read threshold axis to MEASURED human biology.

The framework reads a promoter switch-threshold structure. Human genetics independently
shows that DNA changes on these same loci move pain in a DIRECTION consistent with a
firing-threshold axis. This module records that anchor with citations and grades it honestly:
the DIRECTION/ORDER is anchored to measured biology [V/F]; NO quantitative clinical magnitude
(no delta-Vm, no potency, no dose, no efficacy number) is asserted [O].

Run:  python3 channelopathy_anchor.py   -> expected/channelopathy_anchor.json
Gate: gate_channelopathy.py (every anchor cited; no forbidden quantitative-clinical claim).
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))

ANCHORS = [
    {
        "locus": "SCN9A (Na_V1.7)",
        "dna_change": "loss-of-function / null",
        "threshold_direction": "firing threshold -> infinity (gate never opens)",
        "measured_phenotype": "congenital insensitivity/indifference to pain (no pain under any circumstance)",
        "citation": "Cox et al. 2006, Nature 444:894; Goldberg et al. 2007, Clin Genet 71:311",
        "grade": "[V/F] direction anchored to measured phenotype",
    },
    {
        "locus": "SCN9A (Na_V1.7)",
        "dna_change": "gain-of-function lowering activation threshold",
        "threshold_direction": "firing threshold lowered (gate opens too easily)",
        "measured_phenotype": "inherited erythromelalgia (burning extremity pain)",
        "citation": "Drenth et al. 2005, J Invest Dermatol 124:1333; Yang/Waxman lineage",
        "grade": "[V/F] direction anchored to measured phenotype",
    },
    {
        "locus": "SCN9A (Na_V1.7)",
        "dna_change": "gain-of-function impairing inactivation",
        "threshold_direction": "sustained firing (gate fails to re-close)",
        "measured_phenotype": "paroxysmal extreme pain disorder (PEPD)",
        "citation": "Fertleman et al. 2006; Estacion et al. 2008, J Neurosci 28:11079",
        "grade": "[V/F] direction anchored to measured phenotype",
    },
    {
        "locus": "NTRK1 (TrkA)",
        "dna_change": "loss-of-function",
        "threshold_direction": "nociceptor developmental arm absent",
        "measured_phenotype": "congenital insensitivity to pain with anhidrosis (CIPA)",
        "citation": "Indo et al. 1996, Nat Genet 13:485",
        "grade": "[V/F] direction anchored to measured phenotype",
    },
    {
        "locus": "SCN10A (Na_V1.8)",
        "dna_change": "pharmacological closed-state stabilisation (VSD2 binder)",
        "threshold_direction": "firing threshold RAISED (gate held closed) -- the realised analgesic move",
        "measured_phenotype": "approved non-opioid analgesia for moderate-severe acute pain",
        "citation": "suzetrigine (VX-548/Journavx), FDA approval 2025-01-30; Vertex Phase-III program",
        "grade": "[V/F] direction anchored to approved mechanism (magnitudes [O])",
    },
]

# DIRECTION-OF-INTERVENTION summary that the proposal (M5) uses -- structural, no magnitudes.
SUMMARY = {
    "axis": "nociceptor firing threshold (R19 OFF<->ON basin)",
    "pathological_pole": "threshold LOWERED / barrier REDUCED (GOF channelopathy or up-regulation)",
    "protective_pole": "threshold HIGH (innocuous input stays sub-threshold; CIP at the limit)",
    "analgesic_direction": "controlled RETURN toward the protective pole (raise |h_sp| / restore barrier)",
    "selectivity_principle": ("intervene at nociceptor-restricted effectors (Na_V1.8 > Na_V1.9 > Na_V1.7 "
                              "by peripheral selectivity) so motor/CNS function and reward circuits are spared "
                              "-> the non-addictive, non-sedating corollary, a-priori from the read and now "
                              "FDA-validated by the Na_V1.8 case"),
    "grade": "[F] structural direction; clinical magnitude/efficacy/safety [O]",
}

if __name__ == "__main__":
    out = {"title": "Channelopathy anchor -- measured biology validates the threshold DIRECTION",
           "anchors": ANCHORS, "intervention_summary": SUMMARY,
           "honesty": "DIRECTION/ORDER anchored to measured phenotypes; NO quantitative clinical magnitude asserted."}
    json.dump(out, open(os.path.join(HERE, "expected", "channelopathy_anchor.json"), "w"), indent=1)
    print("M4 channelopathy anchor:")
    for a in ANCHORS:
        print(f"  {a['locus']:18} {a['dna_change']:42} -> {a['measured_phenotype']}")
    print("  intervention direction:", SUMMARY["analgesic_direction"])
    print("wrote expected/channelopathy_anchor.json")
