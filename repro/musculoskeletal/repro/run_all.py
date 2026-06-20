#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  Musculoskeletal RESEARCH entry point. Drop into a fresh chat and run: python repro/run_all.py
Emerges organs from measured gamma (defers to_measure masters honestly), circulates dynamics so far,
runs the stress battery + oncology status, writes results to reports/, reports the writing lock. No HTML.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_oncology"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng = importlib.import_module("vp_msk_engine"); stress = importlib.import_module("stress_tests")
gates = importlib.import_module("gates"); onco = importlib.import_module("carcinogen_dose_response")

def main():
    print("=" * 78); print("Musculoskeletal  --  RESEARCH PHASE (writing is locked until gates are green)"); print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] ORGAN EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-26s <- %-8s %s  [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (measured, gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"):
        print("    gamma TO-MEASURE (research input R0, fetch via DNA pipeline): %s" % res["organs"]["deferred_gamma"])

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    if not res["oscillators"]: print("    (no autonomous oscillator organ in this physical class)")
    for name, v in res["oscillators"].items():
        print("    %-26s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    print("\n[3] STRESS BATTERY")
    batt = stress.run_battery()
    for su in batt["suites"]: print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[3b] DISEASE BATTERY (cited-severity perturbations of T1..T5 + master switches)")
    dis = stress.run_disease_suite()
    for su in dis["suites"]:
        sec = " (secondary)" if su.get("secondary") else ""
        print("    %-7s perturbs %-22s [%-4s]%s  %s" % (
            su["target"], str(su["perturbs"]), su["status"], sec, su["disease"]))
    print("    all disease targets pass (hard, ex-T7d): %s" % dis["all_disease_targets_pass"])

    print("\n[3c] TREATMENT BATTERY (the MIRROR of each disease: restore the barrier / drive / branch / supply)")
    txb = stress.run_treatment_suite()
    for su in txb["suites"]:
        hp = " (honest open/partial)" if su.get("honest_open_or_partial") else ""
        print("    %-9s [%-7s]%s  %-46s <- %s" % (
            su["target"], su["status"], hp, str(su["disease"])[:46], str(su["treatment"])[:58]))
    print("    all reversible (mirror) treatments restore: %s" % txb["all_reversible_treatments_restore"])

    print("\n[3d] ANALGESIC AXIS (non-opioid three-lever threshold logic on owned painful diseases; DOI inherited)")
    anl = stress.run_analgesia_suite()
    for su in anl["suites"]:
        hp = " (honest open/partial)" if su.get("honest_open_or_partial") else ""
        print("    %-8s [%-6s]%s  %-40s  L1v=%s L2v=%s | L2-coupled=%s L1-decoupled=%s" % (
            su["target"], su["status"], hp, str(su["disease"])[:40],
            su["L1_lowers"], su["L2_lowers"], su["L2_structure_coupled"], su["L1_structure_decoupled"]))
    print("    all in-scope levers lower nociception by DIRECTION: %s" % anl["all_inscope_levers_direction_ok"])
    print("    inherited technique DOI: %s ; L3 central gain -> neuro/mind seam (not re-emerged)" % anl["source_doi"])

    print("\n[4] ONCOLOGY (carcinogen dose-response)")
    onc = onco.run_oncology()
    for s2 in onc["sites"]:
        print("    %-42s <- %-44s [%s]" % (s2["site"], s2["carcinogens"], s2["status"]))
    print("    all sites dose-response shape ok: %s" % onc["all_sites_shape_ok"])

    print("\n[5] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    print("\nNext: fetch any to_measure gamma, build out _engine dynamics + _verify sweeps + _oncology anchors")
    print("until all_green, then gates.write_research_complete(), set PHASE=writing, THEN tools/build_docs.py.")

if __name__ == "__main__":
    main()
