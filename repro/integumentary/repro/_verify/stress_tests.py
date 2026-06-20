#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Integumentary STRESS BATTERY. Very high bar: each CHARTER target T1..T5 is
graded from a WIDE substrate-grounded sweep (no per-target tuning); the carcinogenesis dichotomy is
graded too (ONCO). Failures are honest; [O] is acceptable WITH a stated obstacle; a silent pass is
not. Writing stays LOCKED until run_battery() is all PASS and gates.write_research_complete() runs.

Each suite reports the discriminant value(s) it checked, the grade, and -- if anything is [O] -- the
obstacle, so the report is auditable rather than a bare PASS/FAIL.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_oncology"))
import importlib
eng = importlib.import_module("vp_skn_engine")
dyn = importlib.import_module("skn_dynamics")
onco = importlib.import_module("carcinogen_dose_response")


def _suite_T1(d):
    t = d["T1"]
    ok = bool(t["thinning_threshold_at_half"] and t["thinning_monotone"] and t["insult_discontinuous"]
              and t["gamma1p5_tolerance_order"][0] == "KRT14")
    return dict(target="T1", status="PASS" if ok else "FAIL",
                description="TEWL crosses a permeability threshold as the barrier thins (smooth, at half-thickness); collapses discontinuously at the spinodal under insult; absolute insult tolerance ~ gamma^1.5",
                value={"thinning_2x_at_layers": t["thinning_crosses_2x_at_layers"],
                       "insult_robust_until_frac": t["insult_robust_until_frac"],
                       "abs_insult_tolerance": t["abs_insult_tolerance"],
                       "gamma1p5_order": t["gamma1p5_tolerance_order"]},
                grade="shape [V]", obstacle_if_open="absolute TEWL (g/m^2/h) is [O]: needs lipid permeability D + dC calibration")

def _suite_T2(d):
    t = d["T2"]
    ok = bool(t["closed"] and t["unjammed_during"] and t["rejammed_at_confluence"]
              and t["chronic_wound_critical_drive"] is not None)
    return dict(target="T2", status="PASS" if ok else "FAIL",
                description="injury -> unjamming (q>q*=3.81) -> collective migration -> re-jamming (q<q*) closure; below a critical unjamming drive the wound fails to close (chronic wound)",
                value={"closed": t["closed"], "q_max": t["q_max"], "q_final": t["q_final"],
                       "rejammed": t["rejammed_at_confluence"], "chronic_wound_critical_drive": t["chronic_wound_critical_drive"]},
                grade="shape [V] ; q*=3.81 [L]", obstacle_if_open="absolute closure rate (um/h) is [O]: needs cell-speed calibration")

def _suite_T3(d):
    t = d["T3"]
    ok = bool(t["melanin_plateaus"] and t["photoprotects"] and t["feedback_causes_protection"])
    return dict(target="T3", status="PASS" if ok else "FAIL",
                description="UV raises melanin concavely toward a plateau (negative feedback); melanin screens the UV reaching DNA (partial photoprotection); removing the feedback abolishes the protection (control)",
                value={"melanin_concave": t["melanin_concave"], "sublinear_ratio": t["sublinear_ratio_hi_over_mid"],
                       "delivered_uv_attenuation": t["delivered_uv_attenuation"],
                       "no_feedback_attenuation": t["control_no_feedback_attenuation"]},
                grade="shape [V]", obstacle_if_open="absolute MED / melanin optical density is [O]: needs extinction-coefficient calibration")

def _suite_T4(d):
    t = d["T4"]
    ok = bool(t["conveyor_is_sum"] and t["in_cited_window_28_40"] and t["dwell_order_gamma1p5"][0] == "KRT14")
    return dict(target="T4", status="PASS" if ok else "FAIL",
                description="turnover = sum of comparable substrate-dwell phases (viable epidermis + stratum corneum, equal gamma_TP63 dwell); with SC transit ~14 d the total ~28 d lands in the cited 28-40 d window",
                value={"total_turnover_days": t["total_turnover_days"], "in_window": t["in_cited_window_28_40"],
                       "dwell_order": t["dwell_order_gamma1p5"]},
                grade="structure [V] ; rate [L]", obstacle_if_open="absolute basal cycle time is [O]: needs per-cell calibration")

def _suite_T5(d):
    t = d["T5"]
    ok = bool(t["thresholded_onset"] and t["flux_regulated"] and t["runaway_above_capacity"])
    return dict(target="T5", status="PASS" if ok else "FAIL",
                description="sweat is recruited past a thermal threshold (EDAR switch); the evaporative interface flux regulates core temp (slope drops sharply); above max sweat capacity temperature runs away (heat-stroke limit)",
                value={"onset_load": t["onset_load"], "slope_passive": t["slope_passive"],
                       "slope_sweating": t["slope_sweating"], "slope_runaway": t["slope_runaway"]},
                grade="shape [V]", obstacle_if_open="set-point (37C) and absolute sweat rate are [L]/[O]: need per-gland + heat-capacity calibration")

def _suite_ONCO():
    disc = onco.discriminant()
    ok = bool(disc["reproduces_scc_melanoma_dichotomy"])
    return dict(target="ONCO", status="PASS" if ok else "FAIL",
                description="UV carcinogenesis dichotomy: SCC near-linear in cumulative dose; melanoma RR rises with intermittent/burst delivery (Jensen on the multistage rate); the chronic-exposure tan protects against melanoma (paradox)",
                value={"scc_low_dose_linearity_r": disc["scc_low_dose_r"],
                       "melanoma_intermittent_max_rr": disc["melanoma_intermittent_max_rr"],
                       "melanoma_intermittent_rising": disc["melanoma_intermittent_rising"],
                       "tan_protection_factor": disc["tan_protection_factor"]},
                grade="anchor [L] / shape [V]", obstacle_if_open="absolute incidence is [O]: needs rate0 + population baseline calibration")


def run_battery():
    base = eng.circulate()
    d = base["dynamics"]
    suites = [_suite_T1(d), _suite_T2(d), _suite_T3(d), _suite_T4(d), _suite_T5(d), _suite_ONCO()]
    results = {"emergence_ok": bool(base["organs"]["organs"]),
               "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values())
                                  if base["oscillators"] else None),
               "deferred_gamma": base["organs"].get("deferred_gamma", []), "suites": suites}
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in suites)
    return results


if __name__ == "__main__":
    r = run_battery()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
