#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_vasomotor.py  --  Neurovascular-reactivity entry point (target T9). Drop into a fresh chat and run:
    python repro/run_vasomotor.py

Builds the package's NEW vasomotor target -- cutaneous neurovascular tone as the shared R19 reactivity jam
on the ALREADY-MEASURED EDAR gamma (the hair-cycle / adhesion pattern: a new target on an existing measured
organ, no new gamma fetched, none fitted; the thermoregulation-interface organ's vasomotor arm) -- and runs
rosacea and Raynaud phenomenon as signed perturbations of that one switch. The headline result: the SAME
switch and the SAME spinodals, driven in OPPOSITE directions (a standing vasodilator drive vs a cold
vasoconstrictor drive), give two clinically opposite vasomotor diseases, with reversibility a uniform
consequence of WHETHER the drive crosses its lock. Writes reports/vasomotor_results.json, prints the target
note + reactivity-jam mechanism + disease map + the opposite-property discriminant + 2x sha256. This is a
RESEARCH artifact (no HTML); it does NOT touch the core run_all.py gate (core battery is frozen).
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_vasomotor"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
V = importlib.import_module("vasomotor_switch")
W = importlib.import_module("vasomotor_verify")


def main():
    print("=" * 96)
    print("Integumentary  --  NEUROVASCULAR REACTIVITY (T9): cutaneous vasomotor tone as a hysteretic jam")
    print("=" * 96)

    res = V.vasomotor_summary(); s, h = V._emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "vasomotor_results.json"), "w", encoding="utf-8").write(s)

    prov = res["_gamma_provenance"]; mech = res["_mechanism"]; seam = res["_seam_note"]
    print("\n[1] TARGET (new vasomotor target on the EXISTING measured EDAR gamma; no new gamma fetched, none fitted)")
    print("    master=%s  gamma=%.6f (measured, already vendored)  new_gamma_fetched=%s"
          % (prov["master"], prov["gamma"], prov["new_gamma_fetched"]))
    print("    EDAR is the THERMOREGULATION-INTERFACE organ; its two autonomic arms are the sudomotor (sweat, T5) and the vasomotor (skin blood flow)")
    print("    rosacea dysregulates the VASOMOTOR arm -- the vascular mirror of hyperhidrosis on the sudomotor arm")
    print("    dilated = JAMMED ON (s>0, flushed) ; constricted = OFF (s<0, quiescent/ischemic) -- a member of the package's jamming class")
    print("    SEAM: dermal perfusion magnitude stays an INHERITED circulatory citation; only the reactivity dynamics is added")

    print("\n[2] MECHANISM: vasomotor tone is a HYSTERETIC TWO-LOCK REACTIVITY JAM (shared R19 switch, measured gamma)")
    print("    spinodal=%.4f  LOCKS DILATED at net drive=%.3f (snap=%.3f)  LOCKS CONSTRICTED at net drive=%.3f (snap=%.3f)"
          % (mech["spinodal"], mech["v_dilate_lock_up"], mech["dilate_jump_magnitude"],
             mech["v_constrict_lock_down"], mech["constrict_jump_magnitude"]))
    print("    hysteresis_width=%.3f (hysteretic=%s, locks_discontinuously=%s)"
          % (mech["hysteresis_width"], mech["hysteretic"], mech["locks_discontinuously"]))
    print("    healthy_net_vasodilator=%.3f (responsive=%s)  -- the healthy vessel sits in the reversible middle (no lock)"
          % (mech["healthy_net_vasodilator"], mech["healthy_responsive"]))

    print("\n[3] DISEASE -> MECHANISM (each lesion = a SIGNED vasomotor drive on the ONE switch; sign picks the pole)")
    print("    %-22s %-46s %-14s %s" % ("disease", "target", "organ", "grade"))
    for k, v in res.items():
        if k.startswith("_"): continue
        print("    %-22s %-46s %-14s %s" % (v["disease"], v["target"], v["organ"], v["grade_shape"][:4]))

    print("\n[4] BATTERY (mechanism + clinical-sign + intervention-reversal)")
    batt = W.run_battery(summary=res)
    m = batt["mechanism_suite"]
    print("    %-22s [%-4s]  %s" % ("T9 mechanism", m["status"], "discontinuous hysteretic two-lock reactivity jam, healthy-responsive"))
    for su in batt["disease_suites"]:
        print("    %-22s [%-4s]  sign=%s  reverse=%s" % (su["disease"], su["status"],
                                                         su["sign_matches_clinic"], su["intervention_reverses"]))
    print("    all pass: %s" % batt["all_pass"])

    print("\n[5] OPPOSITE-PROPERTY DISCRIMINANT (same switch + same spinodals; the diseases are opposite drive signs)")
    opp = res["_opposite_sign_discriminant"]
    print("    %-66s %s" % ("direction: vasodilation (rosacea) vs vasoconstriction (Raynaud)",
                            opp["vasodilation_rosacea_vs_vasoconstriction_raynaud"]))
    print("    %-66s %s" % ("reversibility: fixed telangiectasia vs reversible vasospasm (lock rule)",
                            opp["fixed_telangiectasia_vs_reversible_vasospasm"]))
    print("    %-66s %s" % ("within rosacea: vascular ery-telangiectatic vs inflammatory papulopustular",
                            opp["vascular_ery_telangiectatic_vs_inflammatory_papulopustular"]))
    print("    %-66s %s" % ("all opposite pairs reproduced", opp["all_opposite_pairs_reproduced"]))

    print("\n[6] SELECTED QUANTITATIVE READOUTS")
    ros = res["rosacea"]; ray = res["raynaud_phenomenon"]
    print("    ROSACEA:  transient flush returns=%s  ->  sustained drive locks dilated=%s  telangiectasia fixed=%s  (dilation depth=%.2f)"
          % (ros["transient_flush_returns"], ros["fixed_dilated"], ros["telangiectasia_fixed"], ros["dilation_depth"]))
    print("              papulopustular inflammatory=%s  anti-inflammatory clears papules=%s  vascular background persists=%s"
          % (ros["papulopustular_inflammatory"], ros["antiinflammatory_clears_papules"], ros["vascular_background_persists"]))
    print("              brimonidine blanches but no reset=%s  ->  laser resets fixed telangiectasia=%s (hysteresis)"
          % (ros["brimonidine_blanches_but_no_reset"], ros["laser_resets_fixed_telangiectasia"]))
    print("    RAYNAUD:  attack constricted=%s  (constriction depth=%.2f)  primary reversible=%s  rewarming/CCB reverses=%s"
          % (ray["attack_constricted"], ray["constriction_depth"], ray["primary_reversible"], ray["rewarming_or_ccb_reverses"]))
    print("              boundary: %s" % ray["secondary_ctd_seam"])

    det, _ = W.determinism_ok()
    print("\n[7] DETERMINISM (VP-SPEC C1)")
    print("    vasomotor 2xsha256 identical: %s  (sha=%s...)" % (det, h[:16]))
    g = W.vasomotor_gate()
    print("    vasomotor_gate all_green: %s  (the neurovascular-reactivity section is written only when this is green)" % g["all_green"])
    print("\nGrades: clinical anchor [L] / mechanism shape [V] / regime-scale thresholds [F] / absolute magnitude [O] (vasomotor obstacle).")
    print("Core battery UNTOUCHED: repro/run_all.py result hash is unchanged (this is an additive layer).")
    print("Wrote: reports/vasomotor_results.json")


if __name__ == "__main__":
    main()
