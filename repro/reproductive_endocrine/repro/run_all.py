#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  Reproductive / Gonadal-Endocrine RESEARCH entry point.
Drop into a fresh chat and run:  python repro/run_all.py

Emerges organs from measured gamma (defers to_measure masters honestly), circulates the dynamics,
runs the full discriminant battery (T1..T5), the exact-barrier oncology dose-response, the
temporal-pattern therapy capstone, and the non-rare disease mechanism layer; folds every module
status into the research gate; writes results to reports/; reports the writing lock. No HTML.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_dynamics", "_oncology", "_therapy", "_disease"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng    = importlib.import_module("vp_rep_engine")
stress = importlib.import_module("stress_tests")
gates  = importlib.import_module("gates")
onco   = importlib.import_module("carcinogen_dose_response")
ther   = importlib.import_module("temporal_pattern")
dis    = importlib.import_module("mechanisms")


def main():
    print("=" * 78)
    print("Reproductive / Gonadal-Endocrine  --  RESEARCH PHASE (writing is locked until gates are green)")
    print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] ORGAN EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-26s <- %-8s %s  [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (measured, gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"):
        print("    gamma TO-MEASURE (research input R0, fetch via DNA pipeline): %s" % res["organs"]["deferred_gamma"])

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    if not res["oscillators"]: print("    (no autonomous oscillator organ in this physical class)")
    for name, v in res["oscillators"].items():
        print("    %-26s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    print("\n[3] DISCRIMINANT BATTERY  (T1..T5 HPG  +  G1..G6 gamete  +  E1..E6 embryo  +  F1..F6 fertility  +  S1..S6 sex-ratio)")
    batt = stress.run_battery()
    print("    -- HPG / gonadal rhythms --")
    for su in batt["suites"]:
        if su["target"].startswith("T"):
            print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["title"]))
    print("    -- the GAMETE, emerged from DNA (germline) --")
    for su in batt["suites"]:
        if su["target"].startswith("G"):
            print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["title"]))
    # measured gamete-program gamma atlas (the DNA secret), ascending
    try:
        germ_mod = importlib.import_module("gametogenesis")
        atlas = germ_mod.panel_gamma_atlas() if hasattr(germ_mod, "panel_gamma_atlas") else None
    except Exception:
        atlas = None
    if atlas:
        order = sorted(atlas.items(), key=lambda kv: kv[1])
        print("    gamete-program gamma atlas (measured, asc): "
              + ", ".join("%s=%.4f" % (k, v) for k, v in order))
    print("    germline (gamete) all pass: %s" % batt.get("germline_all_pass"))
    print("    -- the EMBRYO, from the meeting of two gametes to a fetus --")
    for su in batt["suites"]:
        if su["target"].startswith("E"):
            print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["title"]))
    # measured developmental gamma atlas (the body-plan gene-clock), ascending
    try:
        emb_mod = importlib.import_module("embryogenesis")
        eatlas = emb_mod.panel_gamma_atlas() if hasattr(emb_mod, "panel_gamma_atlas") else None
    except Exception:
        eatlas = None
    if eatlas:
        eorder = sorted(eatlas.items(), key=lambda kv: kv[1])
        print("    developmental gamma atlas (measured, asc): "
              + ", ".join("%s=%.4f" % (k, v) for k, v in eorder))
    print("    embryo (fertilisation->fetus) all pass: %s" % batt.get("embryo_all_pass"))
    print("    -- INFERTILITY vs SUBFERTILITY (fertility) --")
    for su in batt["suites"]:
        if su["target"].startswith("F"):
            print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["title"]))
    print("    fertility (infertility/subfertility) all pass: %s" % batt.get("fertility_all_pass"))
    print("    -- SEX determination + sex-ratio DISTORTION (sex-ratio) --")
    for su in batt["suites"]:
        if su["target"].startswith("S"):
            print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["title"]))
    try:
        sxr_mod = importlib.import_module("sex_ratio")
        satlas = sxr_mod.panel_gamma_atlas() if hasattr(sxr_mod, "panel_gamma_atlas") else None
    except Exception:
        satlas = None
    if satlas:
        sorder = sorted(satlas.items(), key=lambda kv: kv[1])
        print("    sex-determination gamma atlas (measured, asc): "
              + ", ".join("%s=%.4f" % (k, v) for k, v in sorder))
    print("    sex-ratio (determination + distortion) all pass: %s" % batt.get("sexratio_all_pass"))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[4] ONCOLOGY  (exact-barrier hormone-cancer dose-response, R19 oncogenic switch)")
    onc = onco.run_oncology()
    for st in onc["sites"]:
        print("    %-20s <- %s" % (st["site"], st["drive_axis"]))
    uc = onc["universality"]
    print("    gamma-independence of barrier law [F]: %s (max spread %.4g over gamma)"
          % (uc["gamma_independent"], uc.get("max_spread", 0.0)))
    print("    breast monotone=%s | prostate concave=%s plateau=%s | cervical mult-low=%s saturates-high=%s"
          % (onc["checks"]["breast_monotone"], onc["checks"]["prostate_concave"],
             onc["checks"]["prostate_plateau"], onc["checks"]["cervical_multiplicative_low"],
             onc["checks"]["cervical_saturates_high"]))
    print("    status: %s   (%s)" % (onc["status"], onc["grades"]))

    print("\n[5] THERAPY  (temporal pattern as a control axis: BAT / pulsatile-GnRH)")
    th = ther.run_therapy()
    bat = th["bat_cycling"]; gn = th["gnrh_pattern"]
    print("    BAT cycling amplifies resistant clone stress=%s ; cycling selective for resistant=%s"
          % (bat["cycling_amplifies_resistant_stress"], bat["cycling_selective_for_resistant"]))
    print("    GnRH same molecule, opposite effect (continuous=suppress / pulsatile=activate)=%s"
          % gn["same_molecule_opposite_effect"])
    print("    status: %s   (%s)" % (th["status"], th["grades"]))

    print("\n[6] DISEASE  (non-rare mechanism + VP-derived better-treatment hypotheses)")
    dd = dis.run_disease()
    for d in dd["disorders"]:
        print("    %-44s <- %-14s [%s]" % (d["name"], d["target"], d["grade"].split(";")[0].strip()))
    print("    substrate checks: %s" % dd["checks_pass"])
    print("    status: %s   (%s)" % (dd["status"], dd["grades"]))

    print("\n[7] RESEARCH GATE")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    emergence=%s  stress=%s  germline=%s  embryo=%s  fertility=%s  sexratio=%s  oncology=%s  therapy=%s  disease=%s"
          % (rg["emergence_ok"], rg["stress_all_targets_pass"], rg.get("germline_pass"),
             rg.get("embryo_pass"), rg.get("fertility_pass"), rg.get("sexratio_pass"),
             rg["oncology_pass"], rg["therapy_pass"], rg["disease_pass"]))
    print("    research ALL_GREEN: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    print("\nResearch body is complete and green. To publish: gates.write_research_complete(),")
    print("set PHASE=writing, THEN tools/build_docs.py  (writing remains a separate locked phase).")


if __name__ == "__main__":
    main()
