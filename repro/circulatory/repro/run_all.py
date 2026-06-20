#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  Circulatory Transport RESEARCH entry point.
Drop the package into a fresh chat and run:  python repro/run_all.py
Emerges organs from measured gamma, circulates dynamics (what exists so far), runs the stress battery
+ oncology status, writes results to reports/, and reports whether WRITING is unlocked. Builds no HTML.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_oncology"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng    = importlib.import_module("vp_cir_engine")
stress = importlib.import_module("stress_tests")
gates  = importlib.import_module("gates")
onco   = importlib.import_module("carcinogen_dose_response")
pred   = importlib.import_module("predictions_registry")

def main():
    print("=" * 78)
    print("Circulatory Transport  --  RESEARCH PHASE (writing is locked until gates are green)")
    print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] ORGAN EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-11s <- %-8s %s  [%s]  %s" % (o["organ"], o["master"], tag, o["dyn_class"], o["role"]))
    print("    developmental order (gamma asc): %s" % res["organs"]["gamma_order_ascending"])

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    for name, v in res["oscillators"].items():
        print("    %-11s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    print("\n[3] STRESS BATTERY")
    batt = stress.run_battery()
    for su in batt["suites"]:
        print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[4] ONCOLOGY (carcinogen dose-response)")
    for s2 in onco.status()["sites"]:
        print("    %-24s <- %s" % (s2["site"], s2["carcinogens"]))
    print("    status: %s" % onco.status()["status"])

    print("\n[5] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked()
    print("    WRITING LOCKED: %s  (%s)" % (locked, why))

    print("\n[6] FALSIFIABLE PREDICTIONS REGISTRY (item 5 drop-in targets; testable hypotheses, not guidance)")
    for p in pred.predictions():
        print("    %-52s %s" % (p["id"], p["status"]))
    print("    -> forced values + falsification thresholds: repro/_verify/predictions_registry.py ; FALSIFICATION_PROTOCOL.md")

    print("\nNext: build out _engine dynamics + _verify sweeps + _oncology anchors until all_green,")
    print("then gates.write_research_complete(), set PHASE=writing, and only THEN run tools/build_docs.py.")

if __name__ == "__main__":
    main()
