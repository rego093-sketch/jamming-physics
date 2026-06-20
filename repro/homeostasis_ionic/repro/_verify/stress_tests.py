#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stress_tests.py  --  Mineral / Acid-Base / Electrolyte STRESS BATTERY over the excavated research
program. Each target is now RUN (vp_loops), not a TODO. Very high bar: each target is a disturbance-
rejection / two-timescale / trade-off / threshold experiment with honest grades; [O]+obstacle acceptable,
silent pass not. Writing stays LOCKED until run_battery() is all PASS and gates.write_research_complete()."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import importlib
eng = importlib.import_module("vp_ion_engine")
loops = importlib.import_module("vp_loops")

DESC = {
 "RI1":"calcium setpoint: serum Ca ~2.4 mM defended by the PTH<->vitD<->bone<->kidney loop; a Ca load/deficit is corrected [V], setpoint [L]",
 "RI2":"acid-base: blood pH ~7.4 defended by respiratory CO2 (fast) + renal HCO3 (slow) -- Henderson-Hasselbalch two-timescale buffer [V], setpoint [L]",
 "RI3":"bone buffer: chronic Ca demand draws on the bone reservoir via remodeling (reservoir/setpoint trade-off) [V]",
 "RI4":"electrolyte: Na/K setpoints corrected by renal handling; the volume<->pressure coupling (seam to hemodynamic) [V]",
 "RI5":"phosphate: Ca-PO4 product held; FGF23 as the phosphate-lowering arm [V]/[O]",
}

def run_battery():
    base = eng.circulate()
    checks, ok, L = loops.loop_pass()
    suites=[]
    def add(tid, passed, value, grade, obstacle=None):
        suites.append({"target":tid, "description":DESC[tid], "status":("PASS" if passed else "FAIL"),
                       "value":value, "grade":grade, "obstacle_if_open":obstacle})
    add("RI1", checks["RI1"], {"ca_final":L["RI1_calcium"]["ca_final"]}, "[V]/[L]")
    add("RI2", checks["RI2"], {"pH_final":L["RI2_acidbase"]["pH_final"], "winters_slope":L["RI2_acidbase"]["respiratory_compensation_slope_dPCO2_dHCO3"]}, "[V]/[L]")
    add("RI3", checks["RI3"], {"ca_dev":L["RI3_bone_reservoir"]["serum_ca_max_deviation"], "B_end":L["RI3_bone_reservoir"]["bone_reserve_end"]}, "[V]")
    add("RI4", checks["RI4"], {"na_final":L["RI4_electrolyte"]["na_final"], "k_final":L["RI4_electrolyte"]["k_final"]}, "[V]/[L]")
    add("RI5", checks["RI5"], {"po4_final":L["RI5_phosphate"]["po4_final"], "ca_po4_max":L["RI5_phosphate"]["ca_po4_product_max"]}, "[V]/[O]",
        obstacle="absolute renal TmP/GFR (tubular transport maxima) need external calibration")
    # substrate laws as additional gates (gain law + OU law)
    law_ok = checks["gain_law"] and checks["ou_law"]
    return {"emergence_ok": bool(base["organs"]["organs"]),
            "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values()) if base["oscillators"] else None),
            "deferred_gamma": base["organs"].get("deferred_gamma", []),
            "substrate_laws_ok": bool(law_ok),
            "gain_law_monotone": checks["gain_law"], "ou_law_holds": checks["ou_law"],
            "suites": suites,
            "all_targets_pass": bool(all(s["status"]=="PASS" for s in suites) and law_ok)}

if __name__ == "__main__":
    r = run_battery(); print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
