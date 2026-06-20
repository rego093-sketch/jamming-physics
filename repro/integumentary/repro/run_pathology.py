#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_pathology.py  --  Integumentary PATHOLOGY entry point. Drop into a fresh chat and run:
    python repro/run_pathology.py

Simulates the major integumentary diseases as named perturbations of the package's OWN verified
mechanisms (T1..T5 / oncology), runs the disease battery, writes reports/pathology_results.json, and
prints the disease->mechanism map with grades. This is a RESEARCH artifact (no HTML); it does not
touch the writing gate. The core T1..T5+ONCO battery (repro/run_all.py) is unchanged.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_oncology", "_pathology"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
P = importlib.import_module("skin_pathology")
V = importlib.import_module("pathology_verify")

def main():
    print("=" * 88)
    print("Integumentary  --  PATHOLOGY: major diseases on the package's own internal mechanisms")
    print("=" * 88)

    res = P.pathology_summary(); s, h = P._emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "pathology_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] DISEASE -> MECHANISM (each disease = one existing knob; intervention = the knob reversed)")
    print("    %-36s %-15s %-22s %s" % ("disease", "target", "organ", "grade"))
    for k, v in res.items():
        if k.startswith("_"): continue
        print("    %-36s %-15s %-22s %s" % (v["disease"], v["target"], v["organ"], v["grade_shape"]))

    print("\n[2] DISEASE BATTERY (clinical-sign + intervention-reversal)")
    batt = V.run_battery(summary=res)
    for su in batt["suites"]:
        print("    %-36s [%-4s]  sign=%s  reverse=%s" % (su["disease"], su["status"],
                                                         su["sign_matches_clinic"], su["intervention_reverses"]))
    print("    all diseases pass: %s" % batt["all_diseases_pass"])

    print("\n[3] OPPOSITE-SIGN DISCRIMINANT (same R19 switch, opposite drive signs, NO new constant)")
    for k, v in batt["opposite_sign_discriminant"].items():
        print("    %-58s %s" % (k, v))

    print("\n[4] SELECTED QUANTITATIVE READOUTS")
    pso = res["psoriasis"]; ad = res["atopic_dermatitis"]; ich = res["ichthyosis"]
    alb = res["albinism_OCA"]; hed = res["hypohidrotic_ectodermal_dysplasia"]; can = res["skin_cancer_melanoma_scc_bcc"]
    print("    psoriasis transit:         held below the differentiation spinodal (homeostatic ~%.0f d); autonomous & %.1fx-accelerating above it"
          % (pso["homeostatic_turnover_days"], pso["relative_acceleration_in_autonomous_regime"]))
    print("                               [cited window %s d vs healthy %s d -- absolute days [O]]"
          % (pso["cited_window_days"], pso["cited_healthy_window_days"]))
    print("    atopic barrier reserve:    %.2f of healthy (disease) -> %.2f (emollient); baseline TEWL %.2fx [magnitude O]"
          % (ad["disease_reserve_fraction"], round(ad["intervention_barrier_reserve"] / ad["healthy_barrier_reserve"], 4), ad["disease_baseline_tewl"]))
    print("    ichthyosis SC retention:   %.1fx residence (critical slowing near the spinodal)" % ich["retention_fold"])
    print("    albinism cancer hazard RR: %.2fx vs pigmented (sunscreen -> %.2fx)"
          % (alb["hazard_RR_albino_vs_pigmented"], alb["intervention_hazard_RR"]))
    print("    HED core temp @ load 2.5:  %.2f (disease) vs %.2f (healthy)  [arb]"
          % (hed["disease_core_temp_arb"], hed["healthy_core_temp_arb"]))
    print("    melanoma intermittent RR:  %.2f; pigment-loss burst RR %.2f"
          % (can["melanoma_intermittent_max_rr"], can["pigment_loss_burst_RR"]))
    mela = res["melasma_hyperpigmentation"]; hyp = res["primary_hyperhidrosis"]; ak = res["actinic_keratosis"]
    print("    melasma melanin overshoot: %.2fx baseline (depigmenting -> %.2fx) [opposite pole of vitiligo]"
          % (mela["overshoot_fold"], round(mela["intervention_melanin"] / mela["healthy_melanin"], 4)))
    print("    hyperhidrosis sweat onset: load %.2f (disease) vs %.2f (healthy) [opposite pole of HED]"
          % (hyp["disease_sweat_onset_load"], hyp["healthy_sweat_onset_load"]))
    print("    actinic keratosis field:   prevalence %.2f vs SCC %.3f at same UV (precursor abundance)"
          % (ak["ak_field_prevalence"][-1], ak["scc_incidence"][-1]))

    det, _ = V.determinism_ok()
    print("\n[5] DETERMINISM (VP-SPEC C1)")
    print("    pathology 2xsha256 identical: %s  (sha=%s...)" % (det, h[:16]))
    print("\nGrades: clinical anchor [L] / mechanism shape [V] / absolute magnitude [O] (obstacle = parent target's).")
    print("Wrote: reports/pathology_results.json")

if __name__ == "__main__":
    main()
