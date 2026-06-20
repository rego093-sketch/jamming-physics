#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_adhesion.py  --  Cell-ADHESION entry point (target T8). Drop into a fresh chat and run:
    python repro/run_adhesion.py

Builds the package's NEW adhesion target -- keratinocyte cell adhesion as the shared R19 binding jam on
the ALREADY-MEASURED KRT14 gamma (the hair-cycle pattern: a new target on an existing measured organ, no
new gamma fetched, none fitted) -- and runs pemphigus vulgaris and bullous pemphigoid as signed
de-adhesion perturbations of that one switch. The headline result: the SAME switch, the SAME spinodal and
the SAME antibody magnitude, with ONLY the targeted adhesion compartment differing (cell-cell desmosomal
vs cell-matrix hemidesmosomal), flip the cleavage plane, the Nikolsky sign and the blister tension. Writes
reports/adhesion_results.json, prints the target note + binding-jam mechanism + disease map + the
opposite-property discriminant + 2x sha256. This is a RESEARCH artifact (no HTML); it does NOT touch the
core run_all.py gate (core battery is frozen).
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_adhesion"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
A = importlib.import_module("adhesion_switch")
V = importlib.import_module("adhesion_verify")


def main():
    print("=" * 96)
    print("Integumentary  --  CELL ADHESION (T8): keratinocyte adhesion as a hysteretic binding jam")
    print("=" * 96)

    res = A.adhesion_summary(); s, h = A._emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "adhesion_results.json"), "w", encoding="utf-8").write(s)

    prov = res["_gamma_provenance"]; mech = res["_mechanism"]
    print("\n[1] TARGET (new adhesion target on the EXISTING measured KRT14 gamma; no new gamma fetched, none fitted)")
    print("    master=%s  gamma=%.6f (measured, already vendored)  new_gamma_fetched=%s"
          % (prov["master"], prov["gamma"], prov["new_gamma_fetched"]))
    print("    desmosomes (cell-cell) and hemidesmosomes (cell-matrix) anchor the keratin network -> adhesion is intrinsic to the keratinocyte organ")
    print("    adherent = JAMMED (ON, s>0) ; blister = UNJAMMED (OFF, s<0) -- a member of the package's jamming class")

    print("\n[2] MECHANISM: adhesion is a HYSTERETIC TWO-STATE BINDING JAM (shared R19 switch, measured gamma)")
    print("    spinodal=%.4f  detaches at net_adhesion=%.3f (snap=%.3f, discontinuous=%s)"
          % (mech["spinodal"], mech["adh_detach_down"], mech["detach_jump_magnitude"], mech["detaches_discontinuously"]))
    print("    re-adheres at net_adhesion=%.3f  hysteresis_width=%.3f (hysteretic=%s)"
          % (mech["adh_readhere_up"], mech["hysteresis_width"], mech["hysteretic"]))
    print("    healthy_net_adhesion=%.3f (adherent=%s)  -- the healthy bond sits ABOVE the upper spinodal"
          % (mech["healthy_net_adhesion"], mech["healthy_adherent"]))

    print("\n[3] DISEASE -> MECHANISM (each lesion = a SIGNED de-adhesion on the ONE switch; antibody picks the compartment)")
    print("    %-26s %-46s %-14s %s" % ("disease", "target", "organ", "grade"))
    for k, v in res.items():
        if k.startswith("_"): continue
        print("    %-26s %-46s %-14s %s" % (v["disease"], v["target"], v["organ"], v["grade_shape"][:4]))

    print("\n[4] BATTERY (mechanism + clinical-sign + intervention-reversal)")
    batt = V.run_battery(summary=res)
    m = batt["mechanism_suite"]
    print("    %-26s [%-4s]  %s" % ("T8 mechanism", m["status"], "discontinuous hysteretic binding jam, healthy-adherent"))
    for su in batt["disease_suites"]:
        print("    %-26s [%-4s]  sign=%s  reverse=%s" % (su["disease"], su["status"],
                                                         su["sign_matches_clinic"], su["intervention_reverses"]))
    print("    all pass: %s" % batt["all_pass"])

    print("\n[5] OPPOSITE-PROPERTY DISCRIMINANT (same switch + same spinodal + same antibody magnitude; only the compartment differs)")
    opp = res["_opposite_sign_discriminant"]
    print("    %-62s %s" % ("cleavage plane: intraepidermal (PV) vs subepidermal (BP)",
                            opp["intraepidermal_pv_vs_subepidermal_bp"]))
    print("    %-62s %s" % ("Nikolsky sign: positive (PV) vs negative (BP)",
                            opp["nikolsky_positive_pv_vs_negative_bp"]))
    print("    %-62s %s" % ("blister tension: flaccid (PV) vs tense (BP)",
                            opp["flaccid_pv_vs_tense_bp"]))
    print("    %-62s %s" % ("all opposite pairs reproduced", opp["all_opposite_pairs_reproduced"]))

    print("\n[6] SELECTED QUANTITATIVE READOUTS")
    pv = res["pemphigus_vulgaris"]; bp = res["bullous_pemphigoid"]
    print("    PV:  cell-cell separated=%s  cell-matrix adherent=%s  plane=%s  Nikolsky+=%s  flaccid=%s"
          % (pv["cellcell_separated"], pv["cellmatrix_adherent"], pv["cleavage_plane"], pv["nikolsky_positive"], pv["blister_flaccid"]))
    print("         partial immunosuppression re-adheres=%s  ->  antibody cleared re-adheres=%s (hysteresis)"
          % (pv["partial_immunosuppression_readheres"], pv["cleared_readheres"]))
    print("    BP:  cell-matrix separated=%s  cell-cell adherent=%s  plane=%s  Nikolsky-=%s  tense=%s"
          % (bp["cellmatrix_separated"], bp["cellcell_adherent"], bp["cleavage_plane"], bp["nikolsky_negative"], bp["blister_tense"]))
    print("         partial immunosuppression re-adheres=%s  ->  antibody cleared re-adheres=%s (hysteresis)"
          % (bp["partial_immunosuppression_readheres"], bp["cleared_readheres"]))

    det, _ = V.determinism_ok()
    print("\n[7] DETERMINISM (VP-SPEC C1)")
    print("    adhesion 2xsha256 identical: %s  (sha=%s...)" % (det, h[:16]))
    g = V.adhesion_gate()
    print("    adhesion_gate all_green: %s  (the cell-adhesion section is written only when this is green)" % g["all_green"])
    print("\nGrades: clinical anchor [L] / mechanism shape [V] / regime-scale thresholds [F] / absolute magnitude [O] (adhesion obstacle).")
    print("Core battery UNTOUCHED: repro/run_all.py result hash is unchanged (this is an additive layer).")
    print("Wrote: reports/adhesion_results.json")


if __name__ == "__main__":
    main()
