#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gates.py  --  Circulatory Transport research/writing PHASE gate (VP-SPEC C1/C3 + research-first rule).

research_gate()   -- determinism (2x sha256 identical) + emergence runs + stress battery all PASS.
writing_locked()  -- True UNLESS PHASE=="writing" AND reports/research_complete.json all_green=true.
                     tools/build_docs.py refuses while True. Call write_research_complete() only when
                     run_battery() is genuinely green. This enforces "research first, then write".
"""
import os, sys, json
_HERE = os.path.dirname(__file__)
_PKG  = os.path.join(_HERE, "..", "..")
_REPORTS = os.path.join(_PKG, "reports")
_PHASE   = os.path.join(_PKG, "PHASE")
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import importlib
eng = importlib.import_module("vp_cir_engine")
stress = importlib.import_module("stress_tests") if os.path.exists(os.path.join(_HERE, "stress_tests.py")) else None

def determinism_ok():
    _, h1 = eng.emit(eng.circulate()); _, h2 = eng.emit(eng.circulate())
    return h1 == h2, h1

def research_gate():
    det, h = determinism_ok()
    batt = stress.run_battery() if stress else {"all_targets_pass": False, "emergence_ok": False}
    green = bool(det and batt.get("emergence_ok") and batt.get("all_targets_pass"))
    return {"determinism_2xsha256_identical": det, "result_sha256": h,
            "emergence_ok": batt.get("emergence_ok"), "stress_all_targets_pass": batt.get("all_targets_pass"),
            "all_green": green}

def read_phase():
    try: return open(_PHASE, encoding="utf-8").read().strip()
    except FileNotFoundError: return "research"

def writing_locked():
    if read_phase() != "writing": return True, "PHASE != writing"
    rc = os.path.join(_REPORTS, "research_complete.json")
    if not os.path.exists(rc): return True, "reports/research_complete.json absent (research not signed off)"
    try:
        if not json.load(open(rc, encoding="utf-8")).get("all_green"):
            return True, "research_complete.json present but all_green != true"
    except Exception as e:
        return True, "research_complete.json unreadable: " + str(e)
    return False, "writing unlocked"

def write_research_complete():
    g = research_gate(); os.makedirs(_REPORTS, exist_ok=True)
    json.dump(g, open(os.path.join(_REPORTS, "research_complete.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return g

if __name__ == "__main__":
    print("research_gate:", json.dumps(research_gate(), ensure_ascii=False, indent=2))
    print("writing_locked:", writing_locked())
