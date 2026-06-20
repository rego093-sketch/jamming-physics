#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  Immune / Hematologic RESEARCH entry point. Drop into a fresh chat and run: python repro/run_all.py
Emerges organs from measured gamma (defers to_measure masters honestly), circulates dynamics so far,
runs the stress battery + oncology status, writes results to reports/, reports the writing lock. No HTML.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_oncology", "_dynamics", "_therapy", "_discipline"): sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng = importlib.import_module("vp_imm_engine"); stress = importlib.import_module("stress_tests")
gates = importlib.import_module("gates"); onco = importlib.import_module("carcinogen_dose_response")
therapy = importlib.import_module("fundamental_therapy")
discipline = importlib.import_module("run_discipline")   # inherited analgesic_threshold_logic_v2_0 (DOI 10.5281/zenodo.20733420)

def main():
    print("=" * 78); print("Immune / Hematologic  --  RESEARCH PHASE (writing is locked until gates are green)"); print("=" * 78)
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

    print("\n[3] STRESS BATTERY")
    batt = stress.run_battery()
    for su in batt["suites"]: print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[4] ONCOLOGY (carcinogen dose-response)")
    for s2 in onco.status()["sites"]: print("    %-30s <- %s" % (s2["site"], s2["carcinogens"]))
    print("    status: %s" % onco.status()["status"])

    print("\n[5] FUNDAMENTAL THERAPY (treatments derived from the R19 attractor landscape, not cell count)")
    G = {o["organ"]: o["gamma"] for o in res["organs"]["organs"] if o.get("gamma") is not None}
    trep = therapy.therapy_report(G)
    print("    Lever A  basin re-flip (differentiation)   pass=%s   anchor: ATRA+arsenic in APL [L]" % trep["lever_A"]["all_pass"])
    print("    Lever B  barrier restoration               pass=%s   Kramers rate collapses exponentially [V]" % trep["lever_B"]["all_pass"])
    print("    Lever C  drive removal (etiologic)         pass=%s   preventive, not curative once committed [V]/[L]" % trep["lever_C"]["all_pass"])
    print("    Lever D  surveillance restoration (seam)   pass=%s   anchor: CAR-T / checkpoint blockade [L]" % trep["lever_D"]["all_pass"])
    print("    cytotoxic-only relapse contrast            pass=%s   barrier+basin unchanged -> basin refills" % trep["cytotoxic_contrast"]["all_pass"])
    print("    -> fundamental cures are attractor/field-level + non-cytotoxic; cytotoxic-only relapses.")

    print("\n[6] PROVENANCE (γ verified against NCBI primary source -- offline gate)")
    prov = eng.provenance_report()
    for sym, v in sorted(prov["per_gene"].items()):
        print("    %-26s <- %-14s sha-chain=%s  γ-recompute=%s  RefSeq-chr=%s  [%s]"
              % (v["organ"], v["accession"], v["sha256_chain_ok"], v["gamma_chain_ok"],
                 v["refseq_chromosome_ok"], "V" if v["verified"] else "FAIL"))
    print("    all four byte-exact vs live NCBI %s (verified %s): %s"
          % (prov["assembly"], prov["verified_on"], prov["all_verified"]))
    print("    (online re-audit: inherited/ncbi_verify.py ONLINE_reverify())")

    print("\n[7] INHERITED DISCIPLINE (analgesic_threshold_logic_v2_0, DOI 10.5281/zenodo.20733420 -- fail-closed)")
    drep = discipline.run()
    if drep["overall"] == "PASS":
        for label in ("D1 inherit-reverify", "D2 burden-prioritisation", "D3 mechanism-honesty (gate)",
                      "D4 falsification", "D5 forbidden-claim (gate)"):
            print("    %-32s [%s]" % (label, "PASS" if drep["results"].get(label) else "FAIL"))
        print("    determinism (5 frozen hashes, drift 0): PASS   checks=%d/%d"
              % (drep["checks_passed"], drep["checks_total"]))
    else:
        print("    DISCIPLINE FAIL at: %s  (drift=%s)" % (drep.get("failed_at"), drep.get("determinism_drift")))
    print("    -> threshold engineering ranks DISEASE TARGETS only; no dose/regimen/synthesis/novel-efficacy claims.")

    print("\n[8] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    NCBI γ provenance verified: %s  (%s, %s)" % (rg["ncbi_provenance_verified"], rg["ncbi_assembly"], rg["ncbi_verified_on"]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked(); print("    WRITING LOCKED: %s  (%s)" % (locked, why))
    if rg["all_green"]:
        print("\nResearch battery is GREEN (T1-T35 + 4 therapy levers; incl. emergent lineage T6, carcinogenesis "
              "T7, memory-lifetime T8, acute/chronic boundary T9, surveillance seam T10, clonal-selection "
              "threshold T11, immunodominance T12, therapy trajectories T13, Lever-B barrier restoration T14, "
              "Lever-D surveillance clearance T15, N-clone repertoire T16, cytotoxic relapse regrowth T17, "
              "affinity maturation T18, combination-therapy conversion T19, original-antigenic-sin imprinting T20, "
              "central-tolerance/clonal-deletion T21, prime-boost scheduling T22, autoimmune tolerance break T23, "
              "peripheral tolerance / regulatory suppression T24, immune exhaustion T25, tolerance-immunity dose "
              "window T26; and the DISEASE/TREATMENT axis: therapeutic re-tolerization T27, epitope spreading T28, "
              "allergic sensitization / desensitization T29, immunodeficiency reconstitution T30, systemic "
              "inflammatory latch / break-window T31, transplant allo-tolerance induction T32 & lineage-targeted "
              "autoimmune cytopenia T33, thymic involution / immunosenescence T34 & durability-optimal re-boosting "
              "T35, deterministic). Treatment results are DIRECTION/CLASS only -- not VP "
              "validation, not medical advice. To publish the site:")
        print("gates.write_research_complete()  ->  set PHASE=writing  ->  python tools/build_docs.py")
    else:
        print("\nResearch not yet green; fix failing targets before sign-off.")

if __name__ == "__main__":
    main()
