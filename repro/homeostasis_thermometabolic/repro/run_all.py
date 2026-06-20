#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py  --  Thermometabolic Homeostasis RESEARCH entry. Drop into a fresh chat: python repro/run_all.py"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_pathology"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng = importlib.import_module("vp_trm_engine"); stress = importlib.import_module("stress_tests")
gates = importlib.import_module("gates"); path = importlib.import_module("setpoint_failure")
restore = importlib.import_module("restoration_levers"); precision = importlib.import_module("precision_routing")

def main():
    print("=" * 80)
    print("Thermometabolic Homeostasis  --  endotherm vs ectotherm, the setpoint, and metabolic disease")
    print("=" * 80)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[0] FOUNDATIONAL: endotherm vs ectotherm (observation only -- no evolution language)")
    fa = eng.foundational_analysis()
    gc = fa["gene_criterion"]
    print("    Q1 gene criterion:", gc["criterion"][:96], "...")
    print("       endotherms have the {UCP1 furnace + ADRB3 command} pair:", gc["observed_endotherms_have_command_pair"])
    print("       ectotherms lack the ADRB3 command (no ortholog resolves):", gc["observed_ectotherms_lack_ADRB3_command"])
    print("    NULL-1 (firewall): UCP1 gamma does NOT separate endo/ecto by value;",
          "pig pseudogene gamma sits among functional rodents:",
          fa["null_ucp1"]["pig_pseudogene_gamma_inside_functional_rodent_envelope"])
    print("    NULL-2 (RH4): PDK4 gamma does NOT mark hibernation; deep-hibernator gamma elevated:",
          fa["null_pdk4"]["hibernator_gamma_elevated_vs_nonhibernators"])
    ntp = fa["null_torpor_panel"]
    print("    NULL-3 (RH8): across %d torpor/BAT genes x 14 species, genes whose gamma separates hibernators: %d"
          % (ntp["genes_tested"], ntp["genes_that_cleanly_separate_by_gamma"]),
          "| group gaps ARE GC gaps, cross-gene r(dGamma,dGC)=%s"
          % ntp["cross_gene_pearson_r_delta_gamma_vs_delta_gc"])
    ncp = fa["null_cpg_oe_panel"]
    print("    NULL-4 (RH9): methylation-substrate CpG O/E of the same %d genes -- genes that separate hibernators: %d"
          % (ncp["genes_tested"], ncp["genes_that_cleanly_separate_by_cpg_oe"]),
          "| distinct from gamma r(gamma,CpG_OE)=%s (GC-loading gamma=%s vs CpG_OE=%s); dynamic regulation [O] external"
          % (ncp["cross_cell_pearson_r_gamma_vs_cpg_oe"], ncp["cross_cell_pearson_r_gamma_vs_gc"],
             ncp["cross_cell_pearson_r_cpg_oe_vs_gc"]))
    sd = fa["setpoint_defense"]
    print("    Q2 mechanism: endotherm pins (sens=%.3f) vs ectotherm tracks (sens=%.3f)"
          % (sd["endotherm_loop"]["ambient_sensitivity"], sd["ectotherm_loop"]["ambient_sensitivity"]))
    print("    offline re-derivation bit-identical:", fa["rederive"]["offline_identical"])

    print("\n[1] NODE EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-28s <- %-9s %s  [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (measured, gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"):
        print("    gamma TO-MEASURE: %s" % res["organs"]["deferred_gamma"])
    else:
        print("    gamma TO-MEASURE: [] (PDK4 promoted to measured this line of work)")

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor)")
    for name, v in res["oscillators"].items():
        print("    %-28s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    print("\n[3] STRESS BATTERY (the 16 excavated research targets)")
    batt = stress.run_battery()
    for su in batt["suites"]:
        print("    %-5s [%-4s] %-10s %s" % (su["target"], su["status"], su.get("grade", "") or "", su["description"][:60]))
    print("    ALL TARGETS PASS: %s" % batt["all_targets_pass"])

    print("\n[4] PATHOLOGY (disease = setpoint drift / attractor-shift -- a SUBSET)")
    for f in path.status()["failures"]:
        r = f["r19"]
        print("    %-34s %s  (crossed=%s)" % (f["site"], r["regime"][:34], r["attractor_crossed"]))

    print("\n[5] RESTORATION LEVERS (analgesic three-lever tech; HYPOTHESES, firewall-bound)")
    rb = restore.build()
    from collections import Counter
    dist = Counter(r["lever"] for r in rb["lever_map"]["rows"])
    print("    lever map: S1(restore-gain)=%d  S2(reduce-forcing)=%d  S3(remove-sensitiser, [O])=%d"
          % (dist["S1"], dist["S2"], dist["S3"]))
    print("    top restoration targets (ranked, gamma NEVER folded into score): %s"
          % [(r["target"], r["score"]) for r in rb["prioritisation"]["ranking"][:3]])
    print("    S3 honesty gate: %s | forbidden-claim scan: %s | falsifiers: %s"
          % (rb["s3_honesty"]["overall"], rb["forbidden_scan"]["overall"],
             rb["falsification"]["all_have_falsifier"]))
    print("    ALL RESTORATION GATES PASS: %s" % rb["all_gates_pass"])

    print("\n[5b] PRECISION ROUTING (analgesic local-anaesthesia mirror; HYPOTHESES, firewall-bound)")
    pr = precision.build()
    td = pr["routing_map"]["tier_distribution"]
    print("    routing tiers: PRECISION=%d (one cited compartment) REGIONAL=%d (2-3) SYSTEMIC=%d (>=4 / distributed)"
          % (td.get("PRECISION", 0), td.get("REGIONAL", 0), td.get("SYSTEMIC", 0)))
    print("    named routes: %s" % ", ".join(pr["routing_map"]["named_routes"].keys()))
    gi = pr["gamma_independence"]
    print("    gamma-independence PROVEN: routing invariant under gamma perturbation=%s, context-column tracks gamma=%s (gamma firewalled OUT of the routing score)"
          % (gi["routing_geometry_invariant_under_gamma_perturbation"], gi["carried_context_column_does_track_gamma"]))
    print("    anatomy-honesty gate: %s | forbidden-claim scan (incl. DELIVERY): %s | falsifiers: %s"
          % (pr["anatomy_honesty"]["overall"], pr["forbidden_scan"]["overall"], pr["falsification"]["all_have_falsifier"]))
    _, prh = precision.emit(); _, prh2 = precision.emit()
    print("    determinism 2xsha256 identical: %s  (routing sha=%s...)" % (prh == prh2, prh[:12]))
    print("    ALL PRECISION-ROUTING GATES PASS: %s" % pr["all_gates_pass"])

    print("\n[6] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))

if __name__ == "__main__":
    main()
