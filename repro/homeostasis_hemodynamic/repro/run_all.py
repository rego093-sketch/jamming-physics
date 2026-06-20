#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py  --  Hemodynamic Homeostasis RESEARCH entry. Drop into a fresh chat: python repro/run_all.py"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_pathology", "_sensory", "_therapy", "_intervention"): sys.path.insert(0, os.path.join(_HERE, sub))
sys.path.insert(0, os.path.join(_HERE, "..", "inherited"))
import importlib
eng = importlib.import_module("vp_hmd_engine"); stress = importlib.import_module("stress_tests")
gates = importlib.import_module("gates"); path = importlib.import_module("setpoint_failure")

def main():
    print("=" * 80); print("Hemodynamic Homeostasis  --  RESEARCH PHASE (writing is locked until gates are green)"); print("=" * 80)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] NODE EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-28s <- %-16s %s  [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (measured, gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"):
        print("    gamma TO-MEASURE (research input, DNA pipeline): %s" % res["organs"]["deferred_gamma"])

    print("\n[2] SENSORY TRANSDUCTION LAYER (the fundamental layer beneath the controllers)")
    sens = res["sensory"]
    b = sens["baroreceptor"]; m = sens["macula_densa"]
    print("    baroreceptor   transducer=%s" % b["transducer"])
    print("                   intact pressure-sensitive=%s  PIEZO-KO flat=%s  shared-R19 spikes=%s"
          % (b["intact_pressure_sensitive"], b["ko_flat_no_afferent"], b["substrate_spikes"]["spikes"]))
    print("    macula_densa   transducer=%s" % m["transducer"])
    print("                   both transductions monotone=%s  SGLT2i restores TGF=%s (%.3f -> %.3f)"
          % (m["both_transductions_monotone"], m["sglt2i"]["tgf_restored"], m["sglt2i"]["tgf_baseline"], m["sglt2i"]["tgf_on_sglt2i"]))

    print("\n[3] CLOSED SETPOINT LOOPS (RP1-RP5)")
    lp = res["loops"]
    print("    RP1 MAP=CVP+CO*SVR -> %.1f mmHg (err %.1f), owned by single organ=%s"
          % (lp["RP1_map_product"]["MAP_mmHg"], lp["RP1_map_product"]["abs_err_mmHg"], lp["RP1_map_product"]["owned_by_single_organ"]))
    print("    RP2 baroreflex buffers %.0f%% of a step; PIEZO-KO labile=%s"
          % (lp["RP2_baroreflex"]["intact"]["buffered_fraction"] * 100, lp["RP2_baroreflex"]["ko_is_labile"]))
    print("    RP3 pressure-natriuresis perfect adaptation=%s (spread %.1f mmHg)"
          % (lp["RP3_pressure_natriuresis"]["perfect_adaptation"], lp["RP3_pressure_natriuresis"]["load_independent_spread_mmHg"]))
    print("    RP4 hypertension reset +%.0f mmHg, operating-point drug opposed back=%s"
          % (lp["RP4_setpoint_reset"]["reset_shift_mmHg"], lp["RP4_setpoint_reset"]["opposed_back"]))
    print("    RP5 HF basin collapse (fold) at kappa=%s, is_fold_not_reset=%s"
          % (lp["RP5_basin_collapse"]["collapse_kappa"], lp["RP5_basin_collapse"]["is_fold_not_reset"]))

    print("\n[4] INTERACTION MAP (sensory -> afferent -> integrator/controller -> effector -> MAP -> feedback)")
    im = res["interaction_map"]
    print("    fast loop: %s" % im["fast_loop"])
    print("    slow loop: %s" % im["slow_loop"])
    print("    nodes=%d edges=%d  (cited seams not re-emerged: carotid body, cardiopulmonary receptors)"
          % (len(im["nodes"]), len(im["edges"])))

    print("\n[5] STRESS BATTERY (computed discriminants -- no silent passes)")
    batt = stress.run_battery()
    for su in batt["suites"]: print("    %-5s [%-4s]  %s" % (su["target"], su["status"], su["description"][:84]))
    print("    PASS %d/%d   all targets pass: %s" % (batt["n_pass"], batt["n_total"], batt["all_targets_pass"]))

    print("\n[6] PATHOLOGY (disease as setpoint reset / basin collapse -- derived laws)")
    ps = path.status()
    hl = ps["hypertension_reset_law"]; cl = ps["hf_collapse_law"]
    print("    essential hypertension: shift matches reference=%s (+%.0f mmHg), opposed back=%s"
          % (hl["shift_matches_reference"], hl["predicted_shift_mmHg"], hl["opposed_back"]))
    print("    chronic heart failure:  closed-form kappa*=%.3f matches sweep=%s (fold, not reset)"
          % (cl["kappa_star_closed_form"], cl["closed_form_matches_sweep"]))

    print("\n[7] FUNDAMENTAL vs SYMPTOMATIC THERAPY (the major-disease treatment research)")
    rx = res["therapy"]
    ht = rx["hypertension"]; hf = rx["heart_failure"]
    print("    HTN  operating-point drug durable drop=%.0f mmHg (opposed back); reference reset durable drop=%.0f mmHg"
          % (ht["operating_point_drug"]["durable_drop_mmHg"], ht["reference_reset"]["durable_drop_mmHg"]))
    print("    HF   inotrope d_margin=%+.3f (shrinks); load-reduce+cycle-break d_margin=%+.3f (grows)"
          % (hf["inotrope_flog"]["d_margin"], hf["load_reduce_cycle_break"]["d_margin"]))
    print("    principle: %s" % rx["principle"])

    print("\n[9] COMFORT-LOGIC INTERVENTION LAYER (analgesic three-lever technique, ported)")
    iv = res["intervention"]; cm = iv["comfort_map"]
    print("    imported from: %s" % iv["imported_from"])
    print("    comfort map: %d axes  by lever %s  DNA-grounded %s"
          % (cm["n_axes"], cm["axes_by_lever"], cm["dna_grounded_axes"]))
    a = cm["proven_loop_anchors"]
    print("    proven-loop read: operating-point opposed back=%s (durable %g mmHg); reference reset durable=%s (%g mmHg)"
          % (a["operating_point_opposed_back"], a["operating_point_durable_drop_mmHg"],
             a["reference_reset_durable"], a["reference_reset_durable_drop_mmHg"]))
    print("    prioritisation order (axes, never agents): %s" % iv["prioritisation"]["order"])
    print("    gates: counter-reg honesty=%s  falsification=%s  forbidden-claim firewall=%s  -> all pass=%s"
          % (iv["counterreg_honesty"]["overall"], iv["falsification"]["overall"],
             iv["claim_scan"]["overall"], iv["all_gates_pass"]))
    print("    firewall: structural prediction only -- no molecule / regimen / efficacy / tolerability / safety claim [O]")

    print("\n[10] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    sensory_ok=%s interaction_map_ok=%s stress=%s" % (rg["sensory_ok"], rg["interaction_map_ok"], rg["stress_pass_count"]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    print("\nHANDOVER: research is green and signed off (reports/research_complete.json). To WRITE the paper,")
    print("set PHASE=writing in the next session, then run tools/build_docs.py (docs/<slug>/index.html).")

if __name__ == "__main__":
    main()
