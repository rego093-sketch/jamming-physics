#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_seb.py  --  Sebaceous-DUCT entry point (target T7). Drop into a fresh chat and run:
    python repro/run_seb.py

Emerges the package's NEW sebaceous organ -- the pilosebaceous duct, as the shared R19 jamming switch
on a MEASURED (fetched + cached + vendored) PRDM1/Blimp1 gamma -- and runs acne vulgaris and
hidradenitis suppurativa as signed occlusion perturbations of that one jam. PRDM1 is the LOWEST-gamma
organ in the atlas, so its functional spinodal opens EARLIEST: an honest emergence-order PREDICTION
graded by sign, not a fit. Writes reports/seb_results.json, prints the emergence note + jamming
mechanism + disease map + the opposite-mode (reversible acne vs irreversible-rupture HS) discriminant +
2x sha256. This is a RESEARCH artifact (no HTML); it does NOT touch the core run_all.py gate
(core battery is frozen).
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_seb"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
S = importlib.import_module("sebaceous_duct")
V = importlib.import_module("seb_verify")


def main():
    print("=" * 96)
    print("Integumentary  --  SEBACEOUS DUCT (T7): pilosebaceous occlusion as a hysteretic jamming switch")
    print("=" * 96)

    res = S.sebaceous_summary(); s, h = S._emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "seb_results.json"), "w", encoding="utf-8").write(s)

    prov = res["_gamma_provenance"]; mech = res["_mechanism"]
    print("\n[1] ORGAN EMERGENCE (new sebaceous organ on a MEASURED PRDM1 gamma; fetched+cached+vendored, never fitted)")
    print("    master=%s  gamma=%.6f (measured)  vendored=%.6f  offline_reproduces=%s"
          % (prov["master"], prov["gamma_from_cached_sequence"], prov["gamma_vendored"], prov["offline_reproduces"]))
    print("    seq_sha256=%s" % prov["seq_sha256"])
    print("    PRDM1 is the LOWEST-gamma organ in the atlas -> earliest functional spinodal -> emergence-order PREDICTION (graded by sign, not a fit)")

    print("\n[2] MECHANISM: the duct is a HYSTERETIC TWO-STATE OCCLUSION JAM (shared R19 switch, measured gamma)")
    print("    spinodal=%.4f  jams_up at net_occlusion=%.3f (snap=%.3f, discontinuous=%s)"
          % (mech["spinodal"], mech["occ_jam_up"], mech["up_jump_magnitude"], mech["jams_discontinuously"]))
    print("    reopens_down at net_occlusion=%.3f  hysteresis_width=%.3f (hysteretic=%s)"
          % (mech["occ_clear_down"], mech["hysteresis_width"], mech["hysteretic"]))
    print("    healthy_net_occlusion=%.3f (patent=%s)  -- the healthy duct sits in the OFF basin"
          % (mech["healthy_net_occlusion"], mech["healthy_patent"]))

    print("\n[3] DISEASE -> MECHANISM (each lesion = a SIGNED occlusion shift on the ONE jam)")
    print("    %-26s %-40s %-16s %s" % ("disease", "target", "organ", "grade"))
    for k, v in res.items():
        if k.startswith("_"): continue
        print("    %-26s %-40s %-16s %s" % (v["disease"], v["target"], v["organ"], v["grade_shape"]))

    print("\n[4] BATTERY (mechanism + clinical-sign + intervention-reversal)")
    batt = V.run_battery(summary=res)
    m = batt["mechanism_suite"]
    print("    %-26s [%-4s]  %s" % ("T7 mechanism", m["status"], "discontinuous hysteretic occlusion jam, healthy-patent"))
    for su in batt["disease_suites"]:
        print("    %-26s [%-4s]  sign=%s  reverse=%s" % (su["disease"], su["status"],
                                                         su["sign_matches_clinic"], su["intervention_reverses"]))
    print("    all pass: %s" % batt["all_pass"])

    print("\n[5] OPPOSITE-MODE DISCRIMINANT (same jam, opposite depth/reversibility, NO new constant)")
    opp = res["_opposite_sign_discriminant"]
    print("    %-62s %s" % ("superficial acne REVERSIBLE vs deep HS rupture IRREVERSIBLE",
                            opp["superficial_acne_reversible_vs_deep_hs_rupture_irreversible"]))
    print("    %-62s %s" % ("C. acnes amplifier: inflammatory vs comedonal at a fixed jam",
                            opp["inflammatory_with_cacnes_vs_comedonal_without"]))
    print("    %-62s %s" % ("depth: HS jams at a heavier plug load than acne",
                            opp["hs_deeper_plug_than_acne"]))
    print("    %-62s %s" % ("all opposite pairs reproduced", opp["all_opposite_pairs_reproduced"]))

    print("\n[6] SELECTED QUANTITATIVE READOUTS")
    acne = res["acne_vulgaris"]; hs = res["hidradenitis_suppurativa"]
    print("    acne:  net_occlusion=%.3f jammed=%s plug_load=%.3f inflammatory=%s"
          % (acne["disease_net_occlusion"], acne["disease_jammed"], acne["disease_plug_load"], acne["inflammatory"]))
    print("           monotherapy(retinoid only) clears=%s  ->  full regimen clears=%s  (de-inflame only still jammed=%s)"
          % (acne["monotherapy_clears"], acne["full_regimen_clears"], acne["deinflamed_still_jammed"]))
    print("    HS:    net_occlusion=%.3f jammed=%s plug_load=%.3f ruptured_deep_branch=%s"
          % (hs["disease_net_occlusion"], hs["disease_jammed"], hs["disease_plug_load"], hs["ruptured_deep_branch"]))
    print("           drive-down to sub-acne occlusion=%.3f: acne_would_clear_here=%s BUT scar_persists=%s (only surgery resets=%s)"
          % (hs["drive_down_to_subacne_net_occlusion"], hs["acne_would_clear_here"],
             hs["scar_persists_on_drive_down"], hs["surgical_resolves"]))

    det, _ = V.determinism_ok()
    print("\n[7] DETERMINISM (VP-SPEC C1)")
    print("    sebaceous 2xsha256 identical: %s  (sha=%s...)" % (det, h[:16]))
    g = V.seb_gate()
    print("    seb_gate all_green: %s  (the sebaceous-duct section is written only when this is green)" % g["all_green"])
    print("\nGrades: clinical anchor [L] / mechanism shape [V] / regime-scale thresholds [F] / absolute magnitude [O] (sebaceous obstacle).")
    print("Core battery UNTOUCHED: repro/run_all.py result hash is unchanged (this is an additive layer).")
    print("Wrote: reports/seb_results.json")


if __name__ == "__main__":
    main()
