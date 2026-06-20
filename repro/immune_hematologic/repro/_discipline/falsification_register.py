#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
falsification_register.py  --  D4: a named, measurable falsifier for every load-bearing claim.

INHERITED TECHNIQUE: analgesic_threshold_logic_v2_0 / M6 (06-falsification), DOI 10.5281/zenodo.20733420.
"A proposal you cannot kill is not science." The analgesic package registers a named, measurable falsifier
for every proposal id. This is the immune analogue: every load-bearing emergent claim and every treatment
lever in this volume is paired with a concrete, measurable observation that would FALSIFY it. The package
already states many of these inline (e.g. relapse is basin-determined not kill-depth-determined); this gate
collects them into one register and FAILS CLOSED if any declared claim id lacks a falsifier.

Gate (fail-closed): every CLAIM id in CLAIMS has >=1 named falsifier; a FRAMEWORK-level falsifier is present.
Run:  python3 falsification_register.py  -> expected/falsification.json ; exit 1 on any missing falsifier
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))

# the load-bearing claims of this volume (id -> one-line statement). Each MUST have a falsifier below.
CLAIMS = {
    "C-CLONAL":       "Clonal selection is a saddle-node crossing at the spinodal (threshold, not graded ramp).",
    "C-INFLAM":       "Inflammation is bistable hysteresis: critical pulse amplitude == spinodal, organ by organ.",
    "C-LINEAGE":      "Developmental lineage order is an ascending-gamma readout (bone_marrow<spleen<thymus<lymphoid).",
    "C-MEMORY":       "Immune memory is barrier-protected persistence (barrier = gamma^2/4).",
    "C-SEAM":         "Immunosurveillance escape is a multiplicative cross-cutting seam (common multiplier across sites).",
    "C-KRAMERS":      "Carcinogenesis is a convex, super-linear Kramers dose-response diverging as the barrier is erased.",
    "C-LEVER-A":      "A malignant cell re-flips to the healthy basin at drive = spinodal with NO cytotoxicity (basin re-flip).",
    "C-LEVER-B":      "Restoring the bistable barrier collapses the Kramers crossing rate exponentially.",
    "C-LEVER-C":      "Removing the etiologic drive is preventive but NOT curative once a cell is committed (hysteresis).",
    "C-LEVER-D":      "Restoring surveillance lowers net burden at FIXED crossing rate and clears the committed reservoir.",
    "C-CYTOTOXIC":    "Cytotoxic-only therapy leaves barrier+basin intact -> the basin refills -> hysteretic relapse.",
    "C-DOSEWINDOW":   "A tolerance-immunity danger band opens between ignorance and central deletion; its width tracks the insult +-1.",
    "C-CENTRAL-TOL":  "Central tolerance sets an insult-independent upper (deletion) edge at a fixed gamma fraction per organ.",
    "C-DISEASE-AXIS": "Across every immune-disease class, a durable cure is basin-acting (cross the saddle-node), not suppression-only.",
}

FALSIFIERS = {
    "C-CLONAL": "If activation rises CONTINUOUSLY with antigen drive (no discontinuous jump, no hysteresis loop) in a controlled stimulation series, the saddle-node premise is wrong and the read should grade [O].",
    "C-INFLAM": "If a sub-spinodal pulse train reliably LATCHES inflammation, or the measured critical amplitude does NOT equal the organ spinodal across organs, the bistable-hysteresis premise fails.",
    "C-LINEAGE": "If measured developmental commitment order contradicts ascending gamma at the gamma-resolved endpoints (not the spleen<->thymus near-tie, which is already graded [O]), the gamma-readout premise is falsified.",
    "C-MEMORY": "If memory persistence is INDEPENDENT of the computed R19 barrier (gamma^2/4) -- e.g. high-barrier and low-barrier states decay identically -- the barrier-persistence premise fails.",
    "C-SEAM": "If the surveillance-escape factor is NOT a common multiplier (it changes the per-site crossing RATE rather than scaling net burden at fixed rate), the cross-cutting-seam premise is wrong.",
    "C-KRAMERS": "If the simulated dose-response is linear or sub-linear (not convex/super-linear) or log-rate is NOT linear in barrier, the Kramers premise is falsified.",
    "C-LEVER-A": "If forcing drive to the spinodal does NOT re-flip the malignant basin without cytotoxicity (cells stay malignant, or are killed rather than differentiated) in the model, Lever A is falsified.",
    "C-LEVER-B": "If restoring the barrier collapses the crossing rate only LINEARLY (not exponentially), the Lever-B (Kramers) premise fails.",
    "C-LEVER-C": "If removing the drive REVERSES an already-committed cell (basin empties without a basin-acting lever), the hysteresis/preventive-only premise of Lever C is falsified.",
    "C-LEVER-D": "If restoring surveillance does NOT lower net burden at fixed crossing rate, or the escape factor is site-specific rather than a common multiplier, Lever D is falsified.",
    "C-CYTOTOXIC": "If deep cytotoxic kill alone CURES (no basin refill, no hysteretic relapse) while leaving barrier+basin unchanged, the cytotoxic-relapse contrast is falsified -- the discriminating prediction of this volume.",
    "C-DOSEWINDOW": "If the danger-band width does NOT grow one-for-one (slope ~+1) with the insult, or the lower edge does NOT track spinodal-minus-insult, the dose-window prediction fails.",
    "C-CENTRAL-TOL": "If the deletion (upper) edge MOVES with the insult (is not insult-independent) or is not a fixed gamma fraction across organs, the central-tolerance premise is falsified.",
    "C-DISEASE-AXIS": "If a purely suppression-only therapy produces DURABLE cure after withdrawal (basin does not refill) in a disease where the model says the basin is latched, the basin-acting-cure axis is falsified.",
    "FRAMEWORK": "If the gamma-derived |h_sp| ordering of the four master genes is uncorrelated with any independent promoter switch-threshold readout, the read's organising relevance to these loci is weakened (gamma remains [V] as a number, but its claim to order the thresholds would not hold).",
}


def run():
    missing = [c for c in CLAIMS if c not in FALSIFIERS]
    has_framework = "FRAMEWORK" in FALSIFIERS
    out = {"title": "D4 falsification register -- a measurable falsifier for every load-bearing claim",
           "inherited_from": "analgesic_threshold_logic_v2_0/M6 (DOI 10.5281/zenodo.20733420)",
           "firewall": ("falsifiers name a measurable observation that would KILL each claim; they assert "
                        "no efficacy, dose, or treatment -- only what evidence would refute the dynamics."),
           "claims": CLAIMS, "falsifiers": FALSIFIERS, "claim_ids": sorted(CLAIMS.keys()),
           "missing": missing, "framework_falsifier_present": has_framework,
           "overall": "PASS" if (not missing and has_framework) else "FAIL"}
    return out


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "expected", "falsification.json"), "w"), indent=1)
    print("D4 falsification register")
    for c in sorted(CLAIMS):
        print("  [%s] %-15s %s..." % ("OK" if c in FALSIFIERS else "MISSING", c, FALSIFIERS.get(c, "-")[:78]))
    print("  [%s] FRAMEWORK-level falsifier present" % ("OK" if out["framework_falsifier_present"] else "MISSING"))
    print("OVERALL:", out["overall"])
    raise SystemExit(0 if out["overall"] == "PASS" else 1)
