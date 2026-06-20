#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py  --  Chronobiology (Circadian) RESEARCH entry. Drop into a fresh chat: python repro/run_all.py"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_pathology"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng = importlib.import_module("vp_clk_engine"); stress = importlib.import_module("stress_tests")
gates = importlib.import_module("gates"); path = importlib.import_module("setpoint_failure")

def main():
    print("=" * 78); print("Chronobiology (Circadian)  --  RESEARCH PHASE (writing is locked until gates are green)"); print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] NODE EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-28s <- %-9s %s  [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (measured, gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"):
        print("    gamma TO-MEASURE (research input, DNA pipeline): %s" % res["organs"]["deferred_gamma"])

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    if not res["oscillators"]: print("    (none)")
    for name, v in res["oscillators"].items():
        print("    %-28s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    for k, v in res.items():
        if isinstance(v, dict) and "question" in v:
            print("\n[2b] PROBE: %s" % k)
            print("    Q: %s" % v["question"])
            for kk in ("free_running_freq_arb", "r19_spinodal", "discriminant", "status"):
                if kk in v: print("    %s: %s" % (kk, v[kk]))

    print("\n[3] STRESS BATTERY (excavated research targets)")
    batt = stress.run_battery()
    for su in batt["suites"]: print("    %-5s [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[4] PATHOLOGY (major non-rare diseases; rare -> disease_wp)")
    for f in path.status()["failures"]: print("    %-34s <- %s" % (f["site"], f["mechanism"]))
    print("    status: %s" % path.status()["status"])

    print("\n[5] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    print("\nNext: fetch to_measure gamma, build the loops/oscillators + disease attractor-shifts until all_green,")
    print("then gates.write_research_complete(), set PHASE=writing, THEN tools/build_docs.py.")

if __name__ == "__main__":
    main()
