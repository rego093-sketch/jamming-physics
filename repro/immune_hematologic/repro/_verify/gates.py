#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gates.py  --  Immune / Hematologic research/writing PHASE gate (VP-SPEC C1/C3 + research-first rule).
research_gate(): determinism (2x sha256) + emergence runs + stress all PASS.
writing_locked(): True UNLESS PHASE=="writing" AND reports/research_complete.json all_green=true.
"""
import os, sys, json
_HERE = os.path.dirname(__file__); _PKG = os.path.join(_HERE, "..", "..")
_REPORTS = os.path.join(_PKG, "reports"); _PHASE = os.path.join(_PKG, "PHASE")
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import importlib
eng = importlib.import_module("vp_imm_engine")
stress = importlib.import_module("stress_tests") if os.path.exists(os.path.join(_HERE, "stress_tests.py")) else None

# Inherited analgesic_threshold_logic_v2_0 discipline layer (DOI 10.5281/zenodo.20733420), fail-closed.
sys.path.insert(0, os.path.join(_HERE, "..", "_discipline"))
try:
    _discipline = importlib.import_module("run_discipline")
except Exception:                    # any import failure => discipline UNAVAILABLE => gate fails closed
    _discipline = None

def discipline_ok():
    """Inherited fail-closed discipline (D1..D5 + determinism). Missing/erroring module => fail closed."""
    if _discipline is None:
        return False, {"overall": "FAIL", "reason": "discipline module unavailable"}
    try:
        out = _discipline.run()
        return out.get("overall") == "PASS", out
    except Exception as e:
        return False, {"overall": "FAIL", "reason": "discipline raised: " + str(e)}

def determinism_ok():
    _, h1 = eng.emit(eng.circulate()); _, h2 = eng.emit(eng.circulate())
    return h1 == h2, h1

def provenance_ok():
    """v0.3.0: offline NCBI primary-source provenance check (byte-exact γ sequences vs live NCBI, frozen)."""
    p = eng.provenance_report()
    return bool(p.get("all_verified")), p

def research_gate():
    det, h = determinism_ok()
    prov_ok, prov = provenance_ok()
    disc_ok, disc = discipline_ok()
    batt = stress.run_battery() if stress else {"all_targets_pass": False, "emergence_ok": False}
    green = bool(det and prov_ok and disc_ok and batt.get("emergence_ok") and batt.get("all_targets_pass"))
    return {"determinism_2xsha256_identical": det, "result_sha256": h, "emergence_ok": batt.get("emergence_ok"),
            "stress_all_targets_pass": batt.get("all_targets_pass"),
            "ncbi_provenance_verified": prov_ok, "ncbi_assembly": prov.get("assembly"),
            "ncbi_verified_on": prov.get("verified_on"),
            "inherited_discipline_pass": disc_ok,
            "inherited_discipline_doi": "10.5281/zenodo.20733420",
            "inherited_discipline_checks": (str(disc.get("checks_passed")) + "/" + str(disc.get("checks_total"))) if disc_ok else disc.get("reason", disc.get("failed_at", "FAIL")),
            "all_green": green}

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
