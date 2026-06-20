#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Reproductive / gonadal-endocrine STRESS BATTERY.

Very high bar: each discriminant target is swept with structural PASS criteria, no per-target tuning,
failures honest, [O]+obstacle acceptable, silent pass not. Writing stays LOCKED until run_battery() is
all PASS and gates.write_research_complete() is called.

Targets (all run live from repro/_dynamics):
  T1 GnRH pulse generator (FHN relaxation oscillator) + frequency decoding (LH/FSH)
  T2 menstrual cycle as a slow relaxation oscillator (waveform asymmetry, not sinusoid)
  T3 oestrogen feedback switch -> mid-cycle LH surge (discontinuous flip + hysteresis)
  T4 seminiferous (spermatogenic) cycle -- intermediate relaxation clock + period ordering
  T5 puberty onset as a discontinuous spinodal crossing
  G1..G6 the GAMETE itself, emerged from DNA (repro/_germline/gametogenesis.py): meiosis structure,
         gamete non-identity, sperm flagellar oscillator, egg held switch, gamma atlas, sperm/egg duality
  E1..E6 the EMBRYO, from the meeting of the two gametes to a fetus (repro/_embryo/embryogenesis.py):
         syngamy + DNA emergence, cleavage, zygotic genome activation, the gene-clock body plan,
         the end-to-end arc, and the honest scoreboard
  F1..F6 INFERTILITY vs SUBFERTILITY (repro/_fertility/infertility.py): the fertility chain as an AND
         of substrate gates, the categorical (past-spinodal) vs probabilistic (near-threshold Kramers)
         distinction, the male oscillator-throughput factor, the female ovulation-switch + REC8
         cohesin-fatigue (age/aneuploidy) factor, treatment-as-a-drive, and the honest scoreboard
  S1..S6 SEX determination + sex-ratio DISTORTION (repro/_sexratio/sex_ratio.py): sex as the
         SOX9<->FOXL2 bistable, Mendel as a fair coin, meiotic drive as a tilt, sex-chromosome drive as
         a signed secondary-sex-ratio skew, Fisher's 1:1 restoring force, and the measured-gamma atlas
"""

import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_dynamics"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_germline"))
import importlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_embryo"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_fertility"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_sexratio"))
eng = importlib.import_module("vp_rep_engine")
hpg = importlib.import_module("hpg_axis")
menstrual = importlib.import_module("menstrual_cycle")
spermato = importlib.import_module("spermatogenesis")
germline = importlib.import_module("gametogenesis")
embryo = importlib.import_module("embryogenesis")
fertility = importlib.import_module("infertility")
sexratio = importlib.import_module("sex_ratio")

def run_battery():
    base = eng.circulate()
    suites = [hpg.run_T1(), menstrual.run_T2(), menstrual.run_T3(), spermato.run_T4(), hpg.run_T5()]
    germ = germline.run_germline_battery()
    suites += germ["suites_full"]
    emb = embryo.run_embryo_battery()
    suites += emb["suites_full"]
    fert = fertility.run_fertility_battery()
    suites += fert["suites_full"]
    sxr = sexratio.run_sexratio_battery()
    suites += sxr["suites_full"]
    results = {
        "emergence_ok": bool(base["organs"]["organs"]),
        "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values())
                           if base["oscillators"] else None),
        "deferred_gamma": base["organs"].get("deferred_gamma", []),
        "suites": [{"target": s["target"], "title": s.get("title", ""), "status": s["status"],
                    "grade": s.get("grade")} for s in suites],
        "suites_full": suites,
        "germline_all_pass": germ["all_germline_pass"],
        "embryo_all_pass": emb["all_embryo_pass"],
        "fertility_all_pass": fert["all_fertility_pass"],
        "sexratio_all_pass": sxr["all_sexratio_pass"],
    }
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in suites)
    return results

if __name__ == "__main__":
    r = run_battery()
    for s in r["suites"]:
        print("  %-3s [%-4s] %s  %s" % (s["target"], s["status"], s["grade"], s["title"]))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
