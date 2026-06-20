#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oncology_roster.py  --  Circulatory Transport ONCOLOGY, full carcinogen roster + multi-driver prevention.

Per the framework OWNERSHIP CONTRACT (MASTER MAP section 6), circulatory owns the ACQUIRED, common,
dynamics-defined cancers of its flow+clearance organs -- renal cell carcinoma (RCC) and hepatocellular
carcinoma (HCC) -- via the SAME R19 barrier-lowering kernel (carcinogen_dose_response.py). The
flagship-carcinogen layer (smoking->RCC, aflatoxin x HBV->HCC) is already built. This module COMPLETES
the etiologic roster (every IARC-classified driver for each cancer) and derives the prevention
consequence per driver, reusing the kernel with NO new mechanism.

Each carcinogen is placed on the organ's R19 drive axis by inverting the (forced, monotone) barrier
law at its CITED relative risk (carcinogen_dose_response._h_for_decrement). The de-escalation result
(removing a driver DIVIDES combined risk by its RR -- the inverse of the multiplicative-synergy
theorem) generalises to N drivers: prevention priority = the highest-RR driver.

CITED ANCHORS [L] (no fabricated numbers):
  RCC (kidney, SIX2 gamma=1.5556):
    - tobacco smoke      RR ~1.6 ever / ~2.0 heavy   (Hunt 2005 meta, PMID 15523697)        IARC Group 1
    - trichloroethylene  RR  1.42 (95% CI 1.17-1.77) (Karami/Scott meta, PMID 23000822)     IARC Group 1 (2012)
  UUC (upper-tract UROTHELIAL carcinoma -- NOT RCC; honest reclassification):
    - aristolochic acid  OR  1-49, dose-dependent     (Hoang meta, PMC3650093)               IARC Group 1
                         + aristolochic-acid nephropathy -> CKD; TP53 A:T->T:A signature.
  HCC (liver, HHEX gamma=1.525):
    - aflatoxin B1       RR  6.37  (Liu 2012 meta, PMID 22405700)                            IARC Group 1
    - chronic HBV        RR 11.3   (Liu 2012 meta)                                           IARC Group 1
    - chronic HCV        HR 10.4 (95% CI 4.9-22.1) (Korean cohort, PMC3520797; meta 7.9-15)  IARC Group 1
    - heavy ethanol      RR ~2.2 (aHR, >60 g/day; dose-dependent HR 1.16/meta)               IARC Group 1
  HCC SYNERGIES (two cited datasets bracketed by the kernel's two combination modes):
    - aflatoxin x HBV    combined RR 72 (~product, MULTIPLICATIVE; Liu 2012)
    - HBV x HCV          combined HR 115 vs HBV 17.1 / HCV 10.4 (Korean cohort, PMC3520797):
                         more-than-additive (SI=4.5) yet SUB-multiplicative of the ~178 product
                         -> sits BETWEEN the additive (~26) and multiplicative (~178) modes, exactly
                         the framework's prediction that real synergies lie between the two modes and
                         approach multiplicative/supra only near the spinodal.

GRADES (C3): cited RR/RR-ratio anchors [L]; round-trip placement + de-escalation + synergy bracketing
reproduced [V]; the prevention/priority reading is a prediction [H]; absolute incidence and the
barrier=gamma^2/4 grounding are [O] (see IRREPRODUCIBILITY_LEDGER). The drive-axis unit (D, h) is [CAL].
Established curative/systemic standard-of-care (nephrectomy/ablation/TKI/IO for RCC; resection/
transplant/ablation/TACE/atezo-bev for HCC) is NOT derived here -- the framework's therapeutic content
is PREVENTION (drive-removal, de-escalation) and STRATIFICATION (reversibility threshold), stated honestly.
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import importlib
onco = importlib.import_module("carcinogen_dose_response")
xref = importlib.import_module("cross_references")   # single-source cross-volume gene-key references


def cross_references():
    """Cross-volume gene-key references consumed (not re-emerged) by circulatory: hereditary RCC (VHL)
    and hereditary HCC (HFE), both owned by disease_wp. Loaded from inherited/cross_references.json."""
    return {"hereditary_RCC": xref.for_entity("hereditary_RCC"),
            "hereditary_HCC": xref.for_entity("hereditary_HCC")}

GAMMA_KIDNEY = 1.5556
GAMMA_LIVER  = 1.525
D_RCC        = onco.D_RCC      # kidney drive-axis Kramers scale [CAL]
D_HCC        = onco.D_HCC      # liver drive-axis Kramers scale [CAL]

# ---- cited relative risks [L] ----
RR_RCC = {"tobacco_smoke": 1.60, "trichloroethylene": 1.42}                 # genuine RCC carcinogens
RR_UUC = {"aristolochic_acid": 7.0}                                          # UUC (urothelial), dose-dep OR 1-49
RR_HCC = {"aflatoxin_B1": onco.RR_AFLA_META, "chronic_HBV": onco.RR_HBV_META,
          "chronic_HCV": 10.4, "heavy_ethanol": 2.2}

# second synergy dataset (Korean cohort, PMC3520797) -- single HRs + observed coinfection HR
HBV_HCV = {"RR_HBV": 17.1, "RR_HCV": 10.4, "RR_coinfection_observed": 115.0}


def place_on_axis(gamma, D, rr):
    """Place a carcinogen on the organ R19 drive axis by inverting the barrier law at its cited RR.
    Returns (drive h, round-tripped RR) -- the round-trip RR must match the cited RR (forced)."""
    delta = D * math.log(rr)
    h = onco._h_for_decrement(gamma, delta)
    rr_back = onco.relative_risk(gamma, h, D)
    return h, rr_back


def roster(gamma, D, rr_map):
    """Place every carcinogen in a roster; report drive, round-tripped RR, and barrier decrement."""
    out = {}
    for name, rr in rr_map.items():
        h, rr_back = place_on_axis(gamma, D, rr)
        out[name] = {"cited_RR": rr, "drive_h": round(h, 5), "roundtrip_RR": round(rr_back, 3),
                     "barrier_decrement": round(onco.barrier(gamma) - onco.barrier_eff(gamma, h), 5)}
    return out


def deescalation(rr_map):
    """Multi-driver de-escalation (multiplicative mode): combined risk = product of RRs; removing a
    driver DIVIDES combined by its RR. Returns the per-driver division factor (= its RR) and the
    prevention priority (highest-RR driver first)."""
    drivers = list(rr_map.items())
    combined = 1.0
    for _, rr in drivers:
        combined *= rr
    removal = {}
    for name, rr in drivers:
        removal[name] = {"divide_combined_by": round(rr, 2),
                         "residual_RR_after_removal": round(combined / rr, 2)}
    priority = sorted(rr_map, key=lambda k: rr_map[k], reverse=True)
    n = len(drivers)
    # Machine-explicit grade on the COMBINED product (handoff section 4 item 2, 4-way HCC):
    # single agents and PAIRWISE synergies are epidemiologically anchored; a simultaneous N>=3-way
    # multiplicative product has no anchored cohort, so it is ILLUSTRATIVE [H] (model extrapolation),
    # never claimed as data. The per-driver de-escalation ratios below are forced and stay [V].
    if n <= 2:
        combined_status = "[V] pairwise-anchored"
    else:
        combined_status = ("[H] ILLUSTRATIVE: the simultaneous %d-way multiplicative product has no "
                           "anchored cohort; single agents and pairwise synergies are anchored, the "
                           "full %d-way product is a model extrapolation, not data" % (n, n))
    return {"combined_RR_multiplicative": round(combined, 1), "per_driver_removal": removal,
            "prevention_priority": priority, "n_drivers": n,
            "combined_product_status": combined_status}


def synergy_bracket(gamma, D, rr_a, rr_b, observed):
    """Bracket an observed coinfection RR between the kernel's two combination modes:
    additive-RR (lower) and multiplicative-RR (upper). The framework predicts real synergies sit
    between these and approach multiplicative near the spinodal."""
    additive = rr_a + rr_b - 1.0
    multiplicative = rr_a * rr_b
    within = additive <= observed <= multiplicative * 1.05
    # where in the bracket (0=additive, 1=multiplicative)
    frac = (observed - additive) / (multiplicative - additive) if multiplicative > additive else 0.0
    return {"RR_a": rr_a, "RR_b": rr_b, "observed": observed,
            "additive_mode": round(additive, 1), "multiplicative_mode": round(multiplicative, 1),
            "observed_within_bracket": bool(within), "position_in_bracket": round(frac, 3)}


if __name__ == "__main__":
    import json
    print("RCC roster:", json.dumps(roster(GAMMA_KIDNEY, D_RCC, RR_RCC), ensure_ascii=False))
    print("HCC roster:", json.dumps(roster(GAMMA_LIVER, D_HCC, RR_HCC), ensure_ascii=False))
    print("HCC de-escalation:", json.dumps(deescalation(RR_HCC), ensure_ascii=False))
    print("HBV x HCV bracket:", json.dumps(
        synergy_bracket(GAMMA_LIVER, D_HCC, HBV_HCV["RR_HBV"], HBV_HCV["RR_HCV"],
                        HBV_HCV["RR_coinfection_observed"]), ensure_ascii=False))
    print("cross-references:", json.dumps(cross_references(), ensure_ascii=False))
