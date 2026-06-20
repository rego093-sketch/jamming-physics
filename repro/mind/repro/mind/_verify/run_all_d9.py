#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_d9.py -- D9 autism threshold-drug gate suite
====================================================
Runs the five D9 modules in order, re-derives each result, checks its sha256 against the
committed expected_*.json, verifies the engine tree invariant (0fbf4988...), and writes
gate.json. Exit 0 iff every module reproduces AND the engine is byte-unchanged.
ADD-ONLY; vp_mind_engine READ-ONLY. SEED=19, stdlib+numpy only.
"""
import os, sys, json, hashlib, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
ENGINE_FILE_SHA = "e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371"

MODULES = [
    ("D9.0", "autism_cohort_moderate_ncbi",   "autism_cohort_moderate_results.json"),
    ("D9.1", "autism_candidate_encoding",      "autism_candidate_encoding_results.json"),
    ("D9.2", "autism_cohort_cerebrum",         "autism_cohort_cerebrum_results.json"),
    ("D9.3", "autism_multilever_threshold",    "autism_multilever_threshold_results.json"),
    ("D9.4", "autism_candidate_limits",        "autism_candidate_limits_results.json"),
]

def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o

def sha_of(obj):
    return hashlib.sha256(json.dumps(_round(obj), sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()

def engine_file_ok():
    p = os.path.join(HERE, "..", "_engine", "vp_mind_engine.py")
    return hashlib.sha256(open(p, "rb").read()).hexdigest() == ENGINE_FILE_SHA

def find_expected(resfile):
    """scan every expected_*_sha256.json and return the committed hash stored under the
    result-file key (robust to module-vs-result filename differences)."""
    for fn in os.listdir(HERE):
        if fn.startswith("expected_") and fn.endswith("_sha256.json"):
            try:
                d = json.load(open(os.path.join(HERE, fn)))
            except Exception:
                continue
            if resfile in d:
                return d[resfile]
    return None

def main():
    rows = []
    all_ok = True
    for tag, mod, resfile in MODULES:
        m = importlib.import_module(mod)
        res = m.run()
        got = sha_of(res)
        exp = find_expected(resfile)
        ok = (exp == got)
        tree_ok = bool(res.get("invariants", {}).get("engine_tree_frozen") == ENGINE_TREE_FROZEN)
        pac_ok = bool(res.get("invariants", {}).get("pac_grounded", True))
        hl = res.get("honesty_ledger", {})
        honest_ok = bool(hl.get("medium_efficacy_tested", 0) == 0 and hl.get("consciousness_claim", 0) == 0
                         and hl.get("new_tuned_constants", 0) == 0 and hl.get("no_cure_claimed", 0) == 1)
        all_ok = all_ok and ok and tree_ok and pac_ok and honest_ok
        rows.append(dict(tag=tag, module=mod, sha256=got, reproduced=ok,
                         engine_tree_ok=tree_ok, pac_grounded=pac_ok, honesty_ledger_ok=honest_ok))
        print(f"  {tag} {mod:<34} repro={ok} tree={tree_ok} pac={pac_ok} honest={honest_ok}")

    eng = engine_file_ok()
    all_ok = all_ok and eng
    gate = {
        "suite": "D9 autism threshold-drug",
        "n_modules": len(MODULES),
        "engine_file_sha256_ok": eng,
        "engine_tree_frozen": ENGINE_TREE_FROZEN,
        "modules": rows,
        "all_pass": bool(all_ok),
        "gate_meaning": "every D9 module reproduces bit-for-bit, the engine is byte-unchanged, PAC is "
                        "grounded to M9.6, and the honesty ledger holds (efficacy=0, no cure claimed, "
                        "no tuned constants, no consciousness claim).",
    }
    json.dump(gate, open(os.path.join(HERE, "gate.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\n  engine file byte-unchanged: {eng}")
    print(f"  GATE ALL PASS: {all_ok}")
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
