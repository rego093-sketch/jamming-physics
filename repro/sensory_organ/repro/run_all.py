#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py  --  Special-Sense Organs RESEARCH entry. Drop into a fresh chat: python repro/run_all.py

Layout:
  [1] node emergence from measured gamma + developmental-order validation
  [2] oscillator confirmation (shared FHN)  [2b] probes
  [3] MOLECULAR TRANSDUCERS    -- every transducer is an R19 bistable/cooperative channel switch
  [4] COCHLEAR HOPF AMPLIFIER  -- criticality gives the parameter-free cube-root compression
  [5] ORGAN INSTRUMENTS        -- ocular optics / cochlear place-map / canal: CLASSICAL (cited, not R19)
  [6] stress battery   [7] pathology (setpoint-drift law)   [8] ROOT-CAUSE TREATMENT
  [9] gates (determinism + writing-lock)
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_pathology"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng = importlib.import_module("vp_sns_engine"); stress = importlib.import_module("stress_tests")
gates = importlib.import_module("gates"); path = importlib.import_module("setpoint_failure")
treat = importlib.import_module("treatment")

def main():
    print("=" * 78); print("Special-Sense Organs  --  RESEARCH PHASE (writing is locked until gates are green)"); print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] NODE EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-28s <- %-9s %s  [%s]" % (o["organ"], o["master"], tag, o["dyn_class"]))
    print("    developmental order (measured, gamma asc): %s" % res["organs"]["gamma_order_ascending"])
    if res["organs"].get("deferred_gamma"):
        print("    gamma TO-MEASURE (research input, DNA pipeline): %s" % res["organs"]["deferred_gamma"])
    dv = res["developmental_order"]
    print("    order validation: broad '%s' -> validated=%s  [%s]" % (dv["broad_prediction"], dv["broad_validated"], dv["grade"].split(";")[0].strip()))

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    if not res["oscillators"]: print("    (none)")
    for name, v in res["oscillators"].items():
        print("    %-28s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    for k, v in res.items():
        if isinstance(v, dict) and "question" in v:
            print("\n[2b] PROBE: %s" % k)
            print("    Q: %s" % v["question"])
            for kk in ("free_running_freq_arb", "r19_spinodal", "discriminant", "status"):
                if kk in v: print("    %s: %s" % (kk, v[kk]))

    print("\n[3] MOLECULAR TRANSDUCERS (every special-sense transducer is an R19 bistable/cooperative switch)")
    tr = res["transduction"]
    for it in tr["transducers"]:
        sw = it["switch"]
        genes = ", ".join(g[0] for g in it["channel_genes"]) if isinstance(it["channel_genes"], list) else str(it["channel_genes"])
        if sw is None:
            print("    %-26s %-30s gamma=%s -> switch deferred to DNA pipeline  [%s]"
                  % (it["node"], genes, it["gamma_state"], it.get("switch_kind", "")))
        else:
            print("    %-26s %-30s bistable=%s flip=%s slope=%.2f  [%s]"
                  % (it["node"], genes, sw["bistable"], sw["discontinuous_flip"], sw["sigmoid_max_slope"], sw["grade_structure"]))
    print("    all switches bistable & discontinuous: %s" % tr["all_switches_bistable_and_discontinuous"])
    print("    thesis: %s" % tr["thesis"])

    print("\n[4] COCHLEAR HOPF AMPLIFIER (active oscillator poised at a bifurcation)")
    amp = res["cochlear_amplifier"]
    print("    critical compression exponent = %s (expected %s at criticality) -> ok=%s"
          % (amp["critical_compression_exponent"], amp["expected_at_criticality"], amp["cube_root_compression_ok"]))
    print("    subcritical small-signal slope = %s (linear off-criticality ok=%s)"
          % (amp["subcritical_smallsignal_slope"], amp["linear_offcriticality_ok"]))
    print("    small-signal gain vs mu: %s  (rises toward criticality=%s)"
          % (amp["smallsignal_gain_vs_mu"], amp["gain_rises_toward_criticality"]))
    print("    active force: %s  [%s]" % (amp["active_force_gene"][0], amp["grade"].split(";")[0].strip()))

    print("\n[5] ORGAN INSTRUMENTS (ocular optics / cochlear place-map / canal -- CLASSICAL, cited, NOT R19)")
    op = res["organ_optics_acoustics"]
    print("    reduced eye: emmetropic axial = %.2f mm (match=%s); clinical = %.2f D/mm (match=%s)"
          % (op["reduced_eye_axial_length_mm"], op["axial_length_match"], op["diopters_per_mm_axial"], op["diopters_per_mm_match"]))
    print("    accommodation (Hofstetter): %.0f D @age15 -> %.0f D @age60 ; presbyopia match=%s"
          % (op["accommodation_D_age15"], op["accommodation_D_age60"], op["presbyopia_match"]))
    print("    Greenwood place-map: %.1f Hz (apex) .. %.0f Hz (base)  match=%s"
          % (op["greenwood_apex_hz"], op["greenwood_base_hz"], op["greenwood_range_match"]))
    print("    semicircular canal: angular-velocity band flatness=%.3f ok=%s ; VOR gain=%s  [%s]"
          % (op["canal_velocity_band_flatness_ratio"], op["canal_velocity_band_ok"], op["vor_gain_cited"], op["grade"].split(";")[0].strip()))

    print("\n[6] STRESS BATTERY (excavated research targets)")
    batt = stress.run_battery()
    for su in batt["suites"]: print("    %-5s [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[7] PATHOLOGY (major non-rare diseases; rare -> disease_wp)")
    for f in path.status()["failures"]: print("    %-34s <- %s" % (f["site"], f["mechanism"]))
    print("    status: %s" % path.status()["status"])

    print("\n[8] ROOT-CAUSE TREATMENT (therapy = inverse substrate operation)")
    tt = treat.status()
    print("    principle: %s" % tt["principle"])
    for t in tt["therapies"]:
        rt = t["root_therapies"][0]
        action = rt["substrate_action"].split("--")[0].strip()
        print("    %-42s ROOT: %s" % (t["disease"], action))
        print("        %-38s evidence: %s" % ("-> " + rt["name"][:36], rt["evidence"]))
    d = tt["restoration_demo"]
    print("    restoration demo: healthy B=%.4f -> disease B=%.4f -> treated B=%.4f (recovered frac=%s) [V-direction]"
          % (d["healthy_barrier"], d["disease_barrier"], d["treated_barrier"], d["recovered_fraction"]))
    print("    %s" % tt["honest_status"])

    print("\n[9] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    print("\nNext: research is signed off below; the explicit next-session step is to set PHASE=writing,")
    print("then run tools/build_docs.py to build the HTML whitepapers from these verified results.")

if __name__ == "__main__":
    main()
