#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gates.py  --  Reproductive / Gonadal-Endocrine research/writing PHASE gate (VP-SPEC C1/C3 + research-first rule).

research_gate(): ALL of the following must hold for all_green:
  (1) determinism  -- circulate() emitted twice => byte-identical sha256 (hashed deterministic core).
  (2) emergence_ok -- organ emergence battery runs.
  (3) stress       -- T1..T5 HPG + G1..G6 germline (gamete) + E1..E6 embryo (fertilisation->fetus) + F1..F6 fertility (infertility/subfertility) + S1..S6 sex-ratio (sex determination + distortion) discriminant battery all PASS (live run via stress_tests).
  (4) oncology     -- exact-barrier hormone-cancer dose-response module status == PASS.
  (5) therapy      -- temporal-pattern (BAT / pulsatile-GnRH) capstone status == PASS.
  (6) disease      -- non-rare mechanism + better-treatment layer status == PASS.
Each research module is invoked exactly ONCE (speed); the hashed core stays the light circulate() emit.

writing_locked(): True UNLESS PHASE=="writing" AND reports/research_complete.json all_green=true.
"""
import os, sys, json, importlib
_HERE = os.path.dirname(__file__); _PKG = os.path.join(_HERE, "..", "..")
_REPORTS = os.path.join(_PKG, "reports"); _PHASE = os.path.join(_PKG, "PHASE")
# engine + stress on path; research module dirs added so they import as top-level
for _d in ("_engine", "_dynamics", "_oncology", "_therapy", "_disease"):
    sys.path.insert(0, os.path.join(_HERE, "..", _d))
sys.path.insert(0, _HERE)  # stress_tests lives beside this file

eng    = importlib.import_module("vp_rep_engine")
stress = importlib.import_module("stress_tests") if os.path.exists(os.path.join(_HERE, "stress_tests.py")) else None
onc    = importlib.import_module("carcinogen_dose_response")
ther   = importlib.import_module("temporal_pattern")
dis    = importlib.import_module("mechanisms")


def determinism_ok():
    _, h1 = eng.emit(eng.circulate()); _, h2 = eng.emit(eng.circulate())
    return h1 == h2, h1


def research_gate():
    det, h = determinism_ok()
    batt = stress.run_battery() if stress else {"all_targets_pass": False, "emergence_ok": False}
    onc_pass  = onc.run_oncology().get("status")  == "PASS"
    ther_pass = ther.run_therapy().get("status")  == "PASS"
    dis_pass  = dis.run_disease().get("status")   == "PASS"
    green = bool(det and batt.get("emergence_ok") and batt.get("all_targets_pass")
                 and onc_pass and ther_pass and dis_pass)
    return {
        "determinism_2xsha256_identical": det,
        "result_sha256": h,
        "emergence_ok": batt.get("emergence_ok"),
        "stress_all_targets_pass": batt.get("all_targets_pass"),
        "germline_pass": batt.get("germline_all_pass"),
        "embryo_pass": batt.get("embryo_all_pass"),
        "fertility_pass": batt.get("fertility_all_pass"),
        "sexratio_pass": batt.get("sexratio_all_pass"),
        "oncology_pass": onc_pass,
        "therapy_pass": ther_pass,
        "disease_pass": dis_pass,
        "all_green": green,
    }


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
    json.dump(g, open(os.path.join(_REPORTS, "research_complete.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return g


if __name__ == "__main__":
    print("research_gate:", json.dumps(research_gate(), ensure_ascii=False, indent=2))
    print("writing_locked:", writing_locked())
