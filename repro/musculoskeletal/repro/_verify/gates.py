#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gates.py  --  Musculoskeletal research/writing PHASE gate (VP-SPEC C1/C3 + research-first rule).
research_gate(): determinism (2x sha256) + emergence runs + stress all PASS.
writing_locked(): True UNLESS PHASE=="writing" AND reports/research_complete.json all_green=true.
"""
import os, sys, json
_HERE = os.path.dirname(__file__); _PKG = os.path.join(_HERE, "..", "..")
_REPORTS = os.path.join(_PKG, "reports"); _PHASE = os.path.join(_PKG, "PHASE")
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import importlib
eng = importlib.import_module("vp_msk_engine")
stress = importlib.import_module("stress_tests") if os.path.exists(os.path.join(_HERE, "stress_tests.py")) else None

def determinism_ok():
    _, h1 = eng.emit(eng.circulate()); _, h2 = eng.emit(eng.circulate())
    return h1 == h2, h1

def research_gate():
    det, h = determinism_ok()
    batt = stress.run_battery() if stress else {"all_targets_pass": False, "emergence_ok": False}
    disease = stress.run_disease_suite() if stress else {"all_disease_targets_pass": False}
    treatment = stress.run_treatment_suite() if stress and hasattr(stress, "run_treatment_suite") else {"all_reversible_treatments_restore": False}
    analgesia = stress.run_analgesia_suite() if stress and hasattr(stress, "run_analgesia_suite") else {"all_inscope_levers_direction_ok": False}
    phys_ok = bool(batt.get("emergence_ok") and batt.get("all_targets_pass"))
    dis_ok = bool(disease.get("all_disease_targets_pass"))
    tx_ok = bool(treatment.get("all_reversible_treatments_restore"))
    anlg_ok = bool(analgesia.get("all_inscope_levers_direction_ok"))
    green = bool(det and phys_ok and dis_ok and tx_ok and anlg_ok)
    return {"determinism_2xsha256_identical": det, "result_sha256": h, "emergence_ok": batt.get("emergence_ok"),
            "stress_all_targets_pass": batt.get("all_targets_pass"),
            "disease_all_targets_pass": dis_ok,
            "treatment_all_reversible_restore": tx_ok,
            "analgesia_all_inscope_levers_direction_ok": anlg_ok, "all_green": green}

def read_phase():
    try: return open(_PHASE, encoding="utf-8").read().strip()
    except FileNotFoundError: return "research"

def writing_locked():
    if read_phase() != "writing": return True, "PHASE != writing"
    rc = os.path.join(_REPORTS, "research_complete.json")
    if not os.path.exists(rc): return True, "reports/research_complete.json absent (research not signed off)"
    try:
        if not json.load(open(rc, encoding="utf-8")).get("all_green"): return True, "all_green != true"
    except Exception as e:
        return True, "research_complete.json unreadable: " + str(e)
    return False, "writing unlocked"

def write_research_complete():
    g = research_gate(); os.makedirs(_REPORTS, exist_ok=True)
    json.dump(g, open(os.path.join(_REPORTS, "research_complete.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return g

if __name__ == "__main__":
    print("research_gate:", json.dumps(research_gate(), ensure_ascii=False, indent=2)); print("writing_locked:", writing_locked())
