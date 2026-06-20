#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py  —  M7 reproduction harness (v2.0). Runs every module gate to OVERALL: PASS
and freezes the determinism hashes of the engine-generated outputs.

From the package root:   python3 repro/run_all.py
(Network is needed ONLY if 02's promoter cache is absent; with the bundled cache for all
22 expanded targets it runs fully offline.)

v2.0 module map (executed in dependency order):
    M1  01-inherit-reverify         re-derive the inherited gamma anchor, drift 0
    M8  02-read-nav-channels        fetch/READ the 22-gene expanded promoter set (offline via cache)
    M8  02 gate                     re-derive all 22 gamma offline; corr(gamma,GC); provenance pinned
    M9  03-threshold-map            three-lever (L1/L2/L3) threshold map over all 27 targets
    M4  04-channelopathy-anchor     DNA channelopathy anchor (CIP/PEPD/IEM direction)
    M10 10-burden-prioritisation    burden/unmet-need/druggability-weighted TARGET prioritisation
    M11 11-l3-honesty               fail-closed: every L3 (NGF/CGRP) mechanism link graded [O]
    M12 12-precision-local-anaesth. nociceptor entry-port x charged-blocker differential-block map
    M5  05-intervention-logic       fail-closed forbidden-claim scan over proposal + all 4 modules + whitepaper
    M6  06-falsification            a named, measurable falsifier for every proposal (incl. P6 precision)

M5 runs AFTER M9/M10/M11/M12 because it scans their emitted JSON. M11/M10 run after M9
because they read 03's threshold_map.json.
"""
import os, sys, json, hashlib, subprocess

REPRO = os.path.dirname(os.path.abspath(__file__))

# (label, working_dir, script) — order matters (dependencies above)
STEPS = [
    ("M1 inherit-reverify",      "01-inherit-reverify",       "reverify_threshold.py"),
    ("M8 read-22-targets",       "02-read-nav-channels",      "fetch_nav_channels.py"),   # offline if cache present
    ("M8 gate (corr,drift,prov)","02-read-nav-channels",      "gate_nav_channels.py"),
    ("M9 three-lever map",       "03-threshold-map",          "build_threshold_map.py"),
    ("M4 channelopathy",         "04-channelopathy-anchor",   "channelopathy_anchor.py"),
    ("M10 burden-prioritisation","10-burden-prioritisation",  "build_prioritisation.py"),
    ("M11 L3-honesty (gate)",    "11-l3-honesty",             "l3_honesty.py"),
    ("M12 precision-local-anaes","12-precision-local-anaesthesia","build_precision_map.py"),
    ("M5 claim-scan (gate)",     "05-intervention-logic",     "forbidden_claim_scan.py"),
    ("M6 falsification",         "06-falsification",          "falsification_register.py"),
]

# engine-generated outputs whose bytes are frozen for determinism
FROZEN = [
    "01-inherit-reverify/expected/reverify.json",
    "02-read-nav-channels/nav_channels_gamma.json",
    "02-read-nav-channels/expected/nav_gate.json",
    "03-threshold-map/expected/threshold_map.json",
    "04-channelopathy-anchor/expected/channelopathy_anchor.json",
    "10-burden-prioritisation/expected/priority_ranking.json",
    "11-l3-honesty/expected/l3_honesty.json",
    "12-precision-local-anaesthesia/expected/precision_block_map.json",
    "05-intervention-logic/expected/claim_scan.json",
    "06-falsification/expected/falsification.json",
]

def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

def main():
    passed = 0
    print("=" * 64)
    for label, d, script in STEPS:
        wd = os.path.join(REPRO, d)
        r = subprocess.run([sys.executable, script], cwd=wd, capture_output=True, text=True)
        ok = (r.returncode == 0)
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
        if not ok:
            print(r.stdout[-1500:]); print(r.stderr[-800:])
            print("=" * 64); print(f"OVERALL: FAIL at {label}"); sys.exit(1)
        passed += 1

    # determinism: hash frozen outputs; compare to expected_sha256.json if present, else write it
    cur = {p: sha(os.path.join(REPRO, p)) for p in FROZEN}
    exp_path = os.path.join(REPRO, "expected_sha256.json")
    if os.path.exists(exp_path):
        exp = json.load(open(exp_path))
        drift = [p for p in FROZEN if exp.get(p) != cur[p]]
        if drift:
            print("=" * 64)
            print(f"OVERALL: FAIL — hash drift in: {drift}")
            sys.exit(1)
        print(f"[PASS] determinism — {len(FROZEN)} frozen hashes match (drift 0)")
        passed += 1
    else:
        json.dump(cur, open(exp_path, "w"), indent=1)
        print(f"[INIT] wrote expected_sha256.json ({len(FROZEN)} hashes) — re-run to verify drift 0")
        passed += 1

    print("=" * 64)
    print(f"OVERALL: PASS ({passed}/{len(STEPS)+1} checks)")

if __name__ == "__main__":
    main()
