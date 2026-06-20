#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cycle_verify.py  --  Hair-follicle-cycle STRESS BATTERY + gate (analogue of stress_tests.py for the
new oscillator target, and of pathology_verify.py for its diseases).

Two layers of check, each auditable (a silent pass is not allowed):
  (A) MECHANISM suite -- does the EDAR appendage, run as the shared FHN, actually become an
      AUTONOMOUS RELAXATION OSCILLATOR with an anagen-DOMINANT duty cycle? (the [V] substrate claim).
  (B) DISEASE suites -- each alopecia is a clinical-sign + intervention-reversal test on that one
      oscillator, plus the opposite-sign / opposite-timing discriminant (the headline check).

cycle_gate() is GREEN iff the mechanism suite passes, every disease passes, the discriminant holds,
AND the layer is bit-reproducible (2x sha256). This gate is the hair-cycle layer's own research-first
lock: its disease section is written only when this is green. It does NOT touch the core run_all.py
gate (repro/_verify/gates.py) -- the core T1..T5+ONCO battery is left frozen.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import hair_cycle as H


def _mechanism_suite(summary):
    c = summary["_oscillator"]
    ok = bool(c["oscillates"] and c["anagen_dominant"] and c["relaxation_waveform"])
    return dict(target="OSC (hair-follicle cycle)", status="PASS" if ok else "FAIL",
                description="the EDAR appendage, run as the shared FHN on its MEASURED gamma, becomes an autonomous relaxation oscillator: it cycles (beats>=3), its waveform is a plateau-and-collapse relaxation (not harmonic), and the active phase (anagen) DOMINATES the cycle",
                value={"gamma": c["gamma"], "growth_bias": c["growth_bias"], "anagen_fraction": c["anagen_fraction"],
                       "period_arb": c["period_arb"], "beats": c["beats"], "plateau_dominance": c["plateau_dominance"]},
                grade="shape [V]",
                obstacle_if_open="absolute anagen FRACTION (cited ~85-90%) and absolute PERIOD (years) are [L]/[O]: the substrate is graded on dominance+direction, not as a fitted match; absolutes need a per-follicle cycle calibration")


def _disease_suite(d):
    ok = bool(d.get("sign_matches_clinic") and d.get("intervention_reverses"))
    return dict(disease=d["disease"], target=d["target"], organ=d["organ"], status="PASS" if ok else "FAIL",
                mechanism=d["mechanism"], anchor=d["anchor"],
                sign_matches_clinic=d.get("sign_matches_clinic"), intervention_reverses=d.get("intervention_reverses"),
                grade=d["grade_shape"], obstacle_if_open=d["grade_absolute"])


def run_battery(summary=None):
    res = summary if summary is not None else H.hair_cycle_summary()
    mech = _mechanism_suite(res)
    dis = [_disease_suite(v) for k, v in res.items() if not k.startswith("_")]
    disc = res["_opposite_sign_discriminant"]
    all_pass = bool(mech["status"] == "PASS"
                    and all(s["status"] == "PASS" for s in dis)
                    and disc["all_opposite_pairs_reproduced"])
    return dict(mechanism_suite=mech, n_diseases=res["_n_diseases"], disease_suites=dis,
                opposite_sign_discriminant=disc, all_pass=all_pass)


def determinism_ok():
    _, h1 = H._emit(H.hair_cycle_summary()); _, h2 = H._emit(H.hair_cycle_summary())
    return h1 == h2, h1


def cycle_gate():
    """The hair-cycle layer's research-first gate (its analogue of gates.research_gate())."""
    det, h = determinism_ok()
    b = run_battery()
    green = bool(det and b["all_pass"])
    return {"determinism_2xsha256_identical": det, "result_sha256": h,
            "mechanism_ok": b["mechanism_suite"]["status"] == "PASS",
            "all_diseases_pass": all(s["status"] == "PASS" for s in b["disease_suites"]),
            "discriminant_ok": b["opposite_sign_discriminant"]["all_opposite_pairs_reproduced"],
            "all_green": green}


if __name__ == "__main__":
    b = run_battery(); g = cycle_gate()
    print(json.dumps(b, ensure_ascii=False, indent=2))
    print("\ncycle_gate:", json.dumps(g, ensure_ascii=False))
    print("ALL PASS:", b["all_pass"], "(the hair-cycle section is written only when this is green)")
