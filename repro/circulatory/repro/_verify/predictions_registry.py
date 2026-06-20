#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
predictions_registry.py  --  Circulatory Transport FALSIFIABLE-PREDICTIONS REGISTRY.

Drop-in targets for handoff section 4 item 5 (empirical tests of the falsifiable core). This module
EMITS the package's locked quantitative predictions for the oncology therapeutics layer (sections
20-21 / T18-T21) -- the numbers a real experiment would test -- each with an explicit FALSIFICATION
criterion and a candidate data source. Values are computed from the SAME vendored substrate functions
used by the stress battery (vp_substrate.barrier = gamma^2/4, spinodal = 2(gamma/3)^1.5), so they are
FORCED, not retyped, and stay byte-consistent with T18-T21. These are testable TARGET HYPOTHESES
(grade [O]/[H]) -- not clinical guidance, and no fabricated data. The full pre-registration (hypothesis
/ measurement / falsification threshold per prediction) is in FALSIFICATION_PROTOCOL.md.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal

GAMMA = {"kidney_SIX2": 1.5556, "liver_HHEX": 1.525}   # measured master-gene gamma (read-only)
CRIT_EXPONENT = 0.5                                     # universal fold / critical-slowing exponent


def predictions():
    """Return the falsifiable-predictions registry (forced values + falsification criteria)."""
    out = []

    # P1 -- reversibility threshold = spinodal, per organ
    sp = {k: round(spinodal(g), 6) for k, g in GAMMA.items()}
    out.append({
        "id": "P1_reversibility_threshold_is_spinodal",
        "layer": "section 20 (T18)",
        "statement": "A carcinogen-driven pre-malignant cell reverts on drive-removal below a SHARP "
                     "threshold and commits irreversibly above it; the threshold is the R19 spinodal "
                     "h_sp = 2(gamma/3)^1.5 read from the master-gene promoter stacking energy.",
        "forced_value": {"h_spinodal_drive": sp, "formula": "h_sp = 2*(gamma/3)**1.5"},
        "grade": "[F]/[V] on the kernel; therapeutic responder-boundary reading [H]",
        "falsification": "Map differentiation-/de-driving-therapy RESPONDERS vs NON-RESPONDERS onto a "
                         "drive proxy. PASS if the responder/non-responder boundary tracks h_sp (sharp, "
                         "not gradual). FALSIFIED if responders extend well past the spinodal, or if no "
                         "sharp boundary exists (a smooth dose-response with no threshold).",
        "candidate_data": "RCC/HCC differentiation- or de-driving-therapy responder cohorts "
                          "(e.g. HCV-cure -> HCC-risk-reversal series; retinoid/IDH analogues where available)",
        "status": "OPEN -- awaiting external responder data"})

    # P2 -- critical-slowing exponent = 1/2
    out.append({
        "id": "P2_critical_slowing_exponent_one_half",
        "layer": "section 20 (T19)",
        "statement": "Reversion time diverges as the drive approaches the threshold with the UNIVERSAL "
                     "fold exponent 1/2 (t_rev ~ (h_sp - h)^(-1/2)); near-threshold lesions are "
                     "marginally stable / relapse-prone.",
        "forced_value": {"exponent": CRIT_EXPONENT, "battery_fit": "T19 fits -0.506 (kidney) / -0.507 (liver)"},
        "grade": "[F]/[V] on the kernel; relapse-proneness reading [H]",
        "falsification": "Measure reversion/relapse latency vs distance-to-threshold for near-boundary "
                         "lesions. PASS if the divergence exponent is 1/2 within error. FALSIFIED if the "
                         "exponent differs from 1/2, or if there is no critical slowing (latency flat near threshold).",
        "candidate_data": "longitudinal relapse-latency vs lesion-grade series for near-threshold "
                          "pre-malignant lesions under drive-removal",
        "status": "OPEN -- awaiting external latency data"})

    # P3 -- cell-fate barrier = gamma^2/4  (the weakest link)
    bar = {k: round(barrier(g), 6) for k, g in GAMMA.items()}
    out.append({
        "id": "P3_cellfate_barrier_equals_gamma_squared_over_4",
        "layer": "sections 20-21 (T18-T21 grounding) -- THE WEAKEST LINK",
        "statement": "The cell-fate ESCAPE BARRIER out of the healthy basin equals gamma^2/4, where gamma "
                     "is the measured master-gene promoter nearest-neighbour stacking energy "
                     "(-mean NN dG37, SantaLucia 1998).",
        "forced_value": {"barrier_height_gamma2_over_4": bar, "formula": "barrier = gamma**2 / 4"},
        "grade": "[O]/[H] -- no experiment yet links promoter stacking energy to a measured barrier height",
        "falsification": "Measure a cell-fate escape-barrier PROXY (transition rate -> Arrhenius barrier, or "
                         "basin depth from single-cell fate-switching statistics) across master genes with "
                         "DIFFERENT measured gamma. PASS if the proxy scales as gamma^2/4 (slope 1 on a "
                         "barrier-vs-gamma^2/4 plot). FALSIFIED if there is no correlation, or a different functional form.",
        "candidate_data": "single-cell fate-switching / reprogramming-barrier assays paired with promoter "
                          "NN-stacking dG37 for the relevant master genes (SIX2, HHEX, ...)",
        "status": "OPEN -- awaiting external barrier-proxy measurement"})

    return out


def registry():
    return {"volume": "circulatory_vp_site", "code": "cir",
            "scope": "falsifiable predictions of the oncology therapeutics layer (sections 20-21)",
            "note": "testable target hypotheses, not clinical guidance; values FORCED from the vendored "
                    "substrate (barrier=gamma^2/4, spinodal=2(gamma/3)^1.5); no fabricated data",
            "predictions": predictions()}


if __name__ == "__main__":
    print(json.dumps(registry(), ensure_ascii=False, indent=2))
