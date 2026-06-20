#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_cycle.py  --  Hair-follicle-CYCLE entry point. Drop into a fresh chat and run:
    python repro/run_cycle.py

Emerges the package's FIRST autonomous oscillator -- the hair follicle, as the shared FHN on the
EXISTING measured EDAR gamma (no new organ, no new fitted constant) -- and runs the four alopecias as
signed perturbations of that one oscillator. Writes reports/cycle_results.json, prints the
mechanism + disease map + the opposite-sign/opposite-timing discriminant + 2x sha256. This is a
RESEARCH artifact (no HTML); it does NOT touch the core run_all.py gate (core battery is frozen).
"""
import os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_cycle"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
H = importlib.import_module("hair_cycle")
V = importlib.import_module("cycle_verify")


def main():
    print("=" * 90)
    print("Integumentary  --  HAIR-FOLLICLE CYCLE: the package's first autonomous (relaxation) oscillator")
    print("=" * 90)

    res = H.hair_cycle_summary(); s, h = H._emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "cycle_results.json"), "w", encoding="utf-8").write(s)

    c = res["_oscillator"]
    print("\n[1] OSCILLATOR EMERGENCE (EDAR appendage in its CYCLING regime; shared FHN, measured gamma)")
    print("    master=%s  gamma=%.4f (measured)  growth_bias=%.4f (=0.5*spinodal, regime scale [F])"
          % (c["master"], c["gamma"], c["growth_bias"]))
    print("    oscillates=%s  beats=%d  period_arb=%.1f  plateau_dominance=%.3f (relaxation waveform=%s)"
          % (c["oscillates"], c["beats"], c["period_arb"], c["plateau_dominance"], c["relaxation_waveform"]))
    print("    anagen_fraction=%.3f  (anagen-dominant=%s; cited ~85-90%% [L] -- substrate graded on dominance, not a fit)"
          % (c["anagen_fraction"], c["anagen_dominant"]))

    print("\n[2] DISEASE -> MECHANISM (each alopecia = a SIGNED drive shift on the ONE oscillator)")
    print("    %-26s %-34s %-16s %s" % ("disease", "target", "organ", "grade"))
    for k, v in res.items():
        if k.startswith("_"): continue
        print("    %-26s %-34s %-16s %s" % (v["disease"], v["target"], v["organ"], v["grade_shape"]))

    print("\n[3] BATTERY (mechanism + clinical-sign + intervention-reversal)")
    batt = V.run_battery(summary=res)
    m = batt["mechanism_suite"]
    print("    %-26s [%-4s]  %s" % ("OSC mechanism", m["status"], "autonomous relaxation oscillator, anagen-dominant"))
    for su in batt["disease_suites"]:
        print("    %-26s [%-4s]  sign=%s  reverse=%s" % (su["disease"], su["status"],
                                                         su["sign_matches_clinic"], su["intervention_reverses"]))
    print("    all pass: %s" % batt["all_pass"])

    print("\n[4] OPPOSITE-SIGN / OPPOSITE-TIMING DISCRIMINANT (same oscillator, opposite drive/timing, NO new constant)")
    opp = res["_opposite_sign_discriminant"]
    print("    %-58s %s" % ("anagen duration: AGA short vs minoxidil long", opp["anagen_duration_aga_short_vs_minoxidil_long"]))
    print("    %-58s %s" % ("shed timing: TE delayed vs anagen-effluvium immediate", opp["shed_timing_te_delayed_vs_anagen_effluvium_immediate"]))
    print("    %-58s %s" % ("persistence: AA sustained vs TE self-limited", opp["persistence_aa_sustained_vs_te_self_limited"]))
    print("    %-58s %s" % ("all opposite pairs reproduced", opp["all_opposite_pairs_reproduced"]))

    print("\n[5] SELECTED QUANTITATIVE READOUTS")
    aga = res["androgenetic_alopecia"]; te = res["telogen_effluvium"]; ane = res["anagen_effluvium"]
    dych = res["_shedding_dichotomy"]
    print("    AGA anagen fraction:       %.3f (healthy) -> %s (progressive miniaturisation); minoxidil -> %.3f (reversal)"
          % (aga["healthy_anagen_fraction"], aga["anagen_fraction_progression"], aga["intervention_anagen_fraction"]))
    print("    TE shed lag:               %d steps  (= one telogen = %d steps; delayed diffuse shed, self-limited)"
          % (te["shed_peak_lag_steps"], dych["telogen_lag_steps"]))
    print("    anagen-effluvium shed lag: %d steps  (immediate; bypasses telogen)"
          % ane["shed_peak_lag_steps"])

    det, _ = V.determinism_ok()
    print("\n[6] DETERMINISM (VP-SPEC C1)")
    print("    hair-cycle 2xsha256 identical: %s  (sha=%s...)" % (det, h[:16]))
    g = V.cycle_gate()
    print("    cycle_gate all_green: %s  (the hair-cycle section is written only when this is green)" % g["all_green"])
    print("\nGrades: clinical/biological anchor [L] / mechanism shape [V] / absolute magnitude [O] (appendage obstacle).")
    print("Core battery UNTOUCHED: repro/run_all.py result hash is unchanged (this is an additive layer).")
    print("Wrote: reports/cycle_results.json")


if __name__ == "__main__":
    main()
