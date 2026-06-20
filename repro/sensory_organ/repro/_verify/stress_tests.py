#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stress_tests.py  --  Special-Sense STRESS BATTERY over the excavated program. High bar: each target
runs a REAL deterministic computation, checks a concrete predicate, grades honestly. A target PASSes when
it is rigorously resolved at its honest grade (classical-arithmetic match / [V] structure / [L] cited /
[O]+obstacle) -- never a silent pass. Writing stays LOCKED until run_battery() is all PASS AND
gates.write_research_complete() is called."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import importlib
eng = importlib.import_module("vp_sns_engine")


def run_battery():
    base = eng.circulate()
    opt = base["organ_optics_acoustics"]
    trans = base["transduction"]
    amp = base["cochlear_amplifier"]
    # per-transducer switch ok
    photo = next((t for t in trans["transducers"] if t["node"] == "eye_photoreceptor"), None)
    hair = next((t for t in trans["transducers"] if t["node"] == "inner_ear_haircell"), None)
    taste = next((t for t in trans["transducers"] if t["node"] == "taste_chemodetection"), None)

    def sw_ok(t):
        return bool(t and t["switch"] and t["switch"]["bistable"] and t["switch"]["discontinuous_flip"])

    suites = [
        {"target": "RS1", "status": "PASS" if opt["pass_"] else "FAIL",
         "description": "ocular optics CLASSICAL: reduced eye -> emmetropic axial %.2f mm, %.2f D/mm, presbyopia by Hofstetter (documented+linked, NOT R19)" % (opt["reduced_eye_axial_length_mm"], opt["diopters_per_mm_axial"]),
         "value": {"axial_mm": opt["reduced_eye_axial_length_mm"], "D_per_mm": opt["diopters_per_mm_axial"]},
         "grade": "classical (cited); arithmetic matches anchor [V-arith]", "obstacle_if_open": None},
        {"target": "RS2", "status": "PASS" if sw_ok(photo) else "FAIL",
         "description": "phototransduction: rod CNG channel is an R19 bistable/cooperative switch (all-or-none, discontinuous flip) [V]; cGMP threshold cited [L]",
         "value": (photo["switch"] if photo else None),
         "grade": "[V] switch structure ; [L] cited threshold (Hill ~3)", "obstacle_if_open": None},
        {"target": "RS3", "status": "PASS" if (opt["greenwood_range_match"] and sw_ok(hair) and amp["pass_"]) else "FAIL",
         "description": "cochlear tonotopy: Greenwood place-map 20 Hz..%.0f kHz [L] + MET gating-spring switch [V] + Hopf amplifier cube-root compression exp=%.3f at criticality [V]" % (opt["greenwood_base_hz"] / 1000.0, amp["critical_compression_exponent"]),
         "value": {"greenwood_base_hz": opt["greenwood_base_hz"], "met_switch": sw_ok(hair), "compression_exponent": amp["critical_compression_exponent"]},
         "grade": "[L] map ; [V] switch ; [V] parameter-free 1/3 compression", "obstacle_if_open": None},
        {"target": "RS4", "status": "PASS" if (opt["canal_velocity_band_ok"]) else "FAIL",
         "description": "vestibular: semicircular-canal torsion pendulum computes angular VELOCITY over 0.1-6 Hz (flatness=%.3f); VOR gain ~%.1f; canal dynamics classical [V]" % (opt["canal_velocity_band_flatness_ratio"], opt["vor_gain_cited"]),
         "value": {"velocity_band_flatness": opt["canal_velocity_band_flatness_ratio"], "vor_gain": opt["vor_gain_cited"]},
         "grade": "[V] transfer-function shape ; [L] cited time constants / VOR gain", "obstacle_if_open": None},
        {"target": "RS5", "status": "PASS" if sw_ok(taste) else "FAIL",
         "description": "chemodetection: taste/olfaction receptor -> cation channel as an R19 threshold switch [V]; olfaction shares the SAME CNG family as the rod; EC50 cited [L]",
         "value": (taste["switch"] if taste else None),
         "grade": "[V] switch structure ; [L] cited EC50", "obstacle_if_open": None},
    ]
    results = {
        "emergence_ok": bool(base["organs"]["organs"]),
        "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values()) if base["oscillators"] else None),
        "deferred_gamma": base["organs"].get("deferred_gamma", []),
        "transducer_genes_to_measure_gamma": trans["transducer_genes_to_measure_gamma"],
        "developmental_order_broad_validated": base["developmental_order"]["broad_validated"],
        "suites": suites,
    }
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in suites)
    return results


if __name__ == "__main__":
    r = run_battery(); print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
