#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  --  Cardiorespiratory RESEARCH entry point.
Drop the package into a fresh chat and run:  python repro/run_all.py
Emerges organs from measured gamma, circulates dynamics (what exists so far), runs the stress battery
+ oncology status, writes results to reports/, and reports whether WRITING is unlocked. Builds no HTML.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("_engine", "_verify", "_oncology", "_disease"):
    sys.path.insert(0, os.path.join(_HERE, sub))
import importlib
eng    = importlib.import_module("vp_car_engine")
stress = importlib.import_module("stress_tests")
gates  = importlib.import_module("gates")
onco   = importlib.import_module("carcinogen_dose_response")
manifest = importlib.import_module("repro_manifest")
scanner  = importlib.import_module("claim_scanner")
docintg  = importlib.import_module("doc_integrity")

def main():
    print("=" * 78)
    print("Cardiorespiratory  --  RESEARCH PHASE (writing is locked until gates are green)")
    print("=" * 78)
    res = eng.circulate(); s, h = eng.emit(res)
    reports = os.path.join(_HERE, "..", "reports"); os.makedirs(reports, exist_ok=True)
    open(os.path.join(reports, "emergence_results.json"), "w", encoding="utf-8").write(s)

    print("\n[1] ORGAN EMERGENCE (from measured gamma)")
    for o in res["organs"]["organs"]:
        g = o.get("gamma"); tag = ("g=" + str(g)) if g is not None else o.get("note", "")
        print("    %-11s <- %-8s %s  [%s]  %s" % (o["organ"], o["master"], tag, o["dyn_class"], o["role"]))
    print("    developmental order (gamma asc): %s" % res["organs"]["gamma_order_ascending"])

    print("\n[2] OSCILLATOR CONFIRMATION (shared FHN; rate=[L] anchor, not emergent)")
    for name, v in res["oscillators"].items():
        print("    %-11s oscillates=%s beats=%s  anchor: %s" % (name, v["oscillates"], v["beats"], v["rate_anchor"]))

    print("\n[3] STRESS BATTERY")
    batt = stress.run_battery()
    for su in batt["suites"]:
        print("    %s  [%-4s]  %s" % (su["target"], su["status"], su["description"]))
    print("    all targets pass: %s" % batt["all_targets_pass"])

    print("\n[4] ONCOLOGY (carcinogen dose-response)")
    onc = onco.results()
    for s2 in onc["sites"]:
        print("    %-24s <- %s" % (s2["site"], s2["carcinogens"]))
    print("    R19 barrier(h=0)==substrate barrier: %s   RR(0)=1: %s"
          % (onc["barrier_h0_equals_substrate"], onc["RR_at_0_is_1"]))
    print("    lung RR vs pack-years: " +
          ", ".join("%g->%.2fx" % (p["pack_years"], p["RR"]) for p in onc["RR_curve"]))
    print("    no-threshold (LNT): %s  [origin slope=sqrt(gamma): %s]"
          % (onc["lnt"]["no_threshold"], onc["lnt"]["slope_equals_sqrt_gamma"]))
    print("    grades: RR(0)=1 [F], monotone/no-threshold [F], shape [V], absolute RR [O]")

    print("\n[5] GATES")
    rg = gates.research_gate()
    print("    determinism 2xsha256 identical: %s  (sha=%s...)" % (rg["determinism_2xsha256_identical"], h[:12]))
    print("    research all_green: %s" % rg["all_green"])
    locked, why = gates.writing_locked()
    print("    WRITING LOCKED: %s  (%s)" % (locked, why))

    # ---- DISEASE EXTENSION (separate research artifact; NOT gated into docs) ----------------------
    db = None
    try:
        dis = importlib.import_module("disease_battery")
        db = dis.run_battery()
        print("\n[6] DISEASE EXTENSION  (research artifact; reuses T1-T5 + oncology kernel; not in docs/)")
        for s in db["suites"]:
            print("    %s  [%-4s]  %-34s %s" % (s["target"], s["status"], s["disease"], s["grade"]))
        print("    disease targets pass: %d/%d   (see DISEASE_FINDINGS.md)" % (db["n_pass"], db["n_total"]))
        print("    note: no new substrate primitive; ALL absolute magnitudes remain [O]")
    except Exception as e:
        print("\n[6] DISEASE EXTENSION: not available (%s)" % e)

    # ---- REPRODUCIBILITY SUITE (technology inherited from analgesic_threshold_logic v2.0) ---------
    print("\n[7] REPRODUCIBILITY SUITE  (inherited from analgesic_threshold_logic v2.0; DOI 10.5281/zenodo.20733420)")
    det, _ = gates.determinism_ok()
    drift  = gates.drift_ok()
    onco_shape = bool(onc["RR_at_0_is_1"] and onc["lnt"]["no_threshold"] and onc["barrier_h0_equals_substrate"])
    disease_ok = bool(db and db["n_pass"] == db["n_total"] and db["n_total"] > 0)
    man  = manifest.verify()
    scn  = scanner.scan()
    grd  = docintg.grades_ok()
    led  = docintg.ledger_ok()
    doi  = docintg.doi_ok()
    offl = gates.offline_ok()

    checks = [
        ("R1  engine determinism (2xsha256)",      det,                  "two engine runs identical"),
        ("R2  report drift-0 (whole harness)",     drift["ok"],          "blob sha %s" % drift["blob_sha256"][:12]),
        ("R3  stress battery T1-T5",               batt["all_targets_pass"], "5/5 discriminants"),
        ("R4  oncology kernel forced shape",       onco_shape,           "RR(0)=1, no-threshold, barrier match"),
        ("R5  disease battery",                    disease_ok,           "%s/%s reuse R19+FHN" % ((db or {}).get("n_pass","?"), (db or {}).get("n_total","?"))),
        ("R6  file manifest (SHA256SUMS)",         man["ok"],            "%d files pinned" % man["n_recorded"]),
        ("R7  forbidden-claim scan (fail-closed)", scn["ok"],            "%d patterns over %d pages" % (scn["n_patterns"], scn["n_files"])),
        ("R8  grade-token legality {F,V,L,O}",     grd["ok"],            "no un-legended grade"),
        ("R9  [O] <-> ledger cross-check",         led["ok"],            "open sections %s covered" % led["site_open_sections"]),
        ("R10 concept DOI consistency",            doi["ok"],            doi["doi"]),
        ("R11 offline self-containment",           offl["ok"],           "socket disabled, still reproduces"),
    ]
    n_pass = sum(1 for _l, ok, _n in checks if ok)
    n_tot  = len(checks)
    for label, ok, note in checks:
        print("    [%s]  %-38s %s" % ("PASS" if ok else "FAIL", label, note))

    # deterministic per-gate snapshots (no wall-clock; safe for drift-0 and excluded from the manifest)
    snap = {"result_sha256": h, "drift_blob_sha256": drift["blob_sha256"],
            "checks": {label.split()[0]: ok for label, ok, _n in checks},
            "n_pass": n_pass, "n_total": n_tot, "overall_pass": n_pass == n_tot,
            "manifest": man, "claim_scan": {"ok": scn["ok"], "hits": scn["hits"]},
            "doc_integrity": {"grades": grd, "ledger": led, "doi": doi},
            "offline": offl, "inherited_from": "analgesic_threshold_logic v2.0 (10.5281/zenodo.20733420)"}
    json.dump(snap, open(os.path.join(reports, "repro_suite.gate.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, sort_keys=True)

    print("\n" + "=" * 78)
    status = "PASS" if n_pass == n_tot else "FAIL"
    print("OVERALL: %s (%d/%d checks)   drift %d   DOI %s" %
          (status, n_pass, n_tot, 0 if drift["ok"] else 1, doi["doi"]))
    print("=" * 78)
    if n_pass != n_tot:
        print("note: R6 fails until the manifest is frozen -> run  python repro/_verify/repro_manifest.py freeze")
    return 0 if n_pass == n_tot else 1

if __name__ == "__main__":
    raise SystemExit(main())
