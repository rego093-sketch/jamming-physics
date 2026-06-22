#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontal_gate.py  --  the INDEPENDENT frontal simulation's lightweight gate
==========================================================================
This is the frontal sim's OWN gate.  It is deliberately lightweight and SELF-
CONTAINED: it verifies the substrate is intact (engine_tripwire) and that every
frontal-local module is byte-deterministic and matches its frozen digest.

It does NOT, and must NOT, import or call the mind atlas runner run_all_atlas.py
(which re-runs all 28 atlas modules per build, ~40 min, scaling linearly).  The
whole point of decoupling the frontal sim is that adding frontal cohort sweeps to
the atlas runner would make atlas builds impossible.  A hard guard below asserts
run_all_atlas is never imported into this process.

Gate steps:
  1. engine_tripwire  (engine + 3 layers byte-identical; M9 anchor bit-for-bit)
  2. for each frontal module: run its entry TWICE -> byte-identical (determinism)
     and the digest == the registry's frozen sha (no drift)
  3. honesty-ledger discipline on each module's result (efficacy/cc/tuned = 0)

Usage:
  python3 frontal_gate.py                 (fast: tripwire fast path)
  python3 frontal_gate.py --full-tree     (also re-emerge the engine tree, ~29 s)
"""
import os, sys, json, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# ---- HARD GUARD: the atlas runner must never be importable into this process ---
_FORBIDDEN = "run_all_atlas"
if _FORBIDDEN in sys.modules:
    raise RuntimeError("frontal_gate refuses to run: the mind atlas runner "
                       "(run_all_atlas) is loaded; the frontal sim must stay decoupled.")

sys.path.insert(0, HERE)
import engine_tripwire
import frontal_registry as REG


def _load_module(entry):
    mod_dir = os.path.join(ROOT, entry["module_dir"])
    if mod_dir not in sys.path:
        sys.path.insert(0, mod_dir)
    return importlib.import_module(entry["module_file"][:-3])


def run(full_tree=False):
    report = {"steps": {}, "modules": {}}

    # ---- step 1: substrate tripwire ----
    tw = engine_tripwire.run(full_tree=full_tree)
    report["steps"]["engine_tripwire"] = tw["TRIPWIRE_PASS"]

    # ---- step 2 + 3: per-module determinism x2 + frozen-sha + discipline ----
    all_mod_ok = True
    for entry in REG.FRONTAL_MODULES:
        m = _load_module(entry)
        fn = getattr(m, entry["entry"])
        res1, d1 = fn()
        res2, d2 = fn()
        deterministic = bool(d1 == d2)
        frozen_match = bool(d1 == entry["frozen_sha256"])
        hl = res1.get("honesty_ledger", {})
        discipline = bool(hl.get("new_tuned_constants", 1) == 0.0
                          and hl.get("consciousness_claim", 1) == 0.0
                          and hl.get("efficacy", 1) == 0.0
                          and hl.get("calls_run_all_atlas", 1) == 0.0)
        inv = res1.get("invariants", {})
        engine_ok = bool(inv.get("engine_tree_unchanged") and inv.get("m0_16_subtree_unchanged"))
        mod_ok = bool(deterministic and frozen_match and discipline and engine_ok)
        all_mod_ok = all_mod_ok and mod_ok
        report["modules"][entry["name"]] = {
            "deterministic_x2": deterministic, "sha256": d1,
            "matches_frozen": frozen_match, "discipline_ok": discipline,
            "engine_unchanged": engine_ok, "PASS": mod_ok,
        }

    # ---- final guard: the atlas runner was never imported ----
    decoupled = bool(_FORBIDDEN not in sys.modules)
    report["steps"]["decoupled_from_atlas_runner"] = decoupled

    report["GATE_PASS"] = bool(tw["TRIPWIRE_PASS"] and all_mod_ok and decoupled)
    return report


if __name__ == "__main__":
    full = "--full-tree" in sys.argv
    r = run(full_tree=full)
    print("=" * 74)
    print("FRONTAL GATE   (vp_frontal; INDEPENDENT; never calls run_all_atlas)")
    print("=" * 74)
    print(f"  [1] engine tripwire            : {r['steps']['engine_tripwire']}")
    for name, m in r["modules"].items():
        print(f"  [2] {name}")
        print(f"        determinism x2={m['deterministic_x2']}  frozen-sha={m['matches_frozen']}  "
              f"discipline={m['discipline_ok']}  engine-unchanged={m['engine_unchanged']}  -> {m['PASS']}")
        print(f"        sha256 = {m['sha256']}")
    print(f"  [3] decoupled from atlas runner: {r['steps']['decoupled_from_atlas_runner']}")
    print("=" * 74)
    print("  FRONTAL GATE: " + ("PASS" if r["GATE_PASS"] else "FAIL"))
    sys.exit(0 if r["GATE_PASS"] else 1)
