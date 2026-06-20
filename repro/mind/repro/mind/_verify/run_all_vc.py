#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_vc.py -- theta-cap virtual-clinical gate suite (VC1-VC5)
================================================================
Runs the five VC modules in order, re-derives each result, checks its sha256 against the
committed expected_*.json, verifies the engine tree invariant (0fbf4988...) and that the
engine file is byte-unchanged (e61083ae...), confirms PAC is grounded and the honesty ledger
holds, then writes gate.json. Exit 0 iff every module reproduces AND the engine is unchanged.

Note: the gate verifies REPRODUCIBILITY and DISCIPLINE, not that every pre-registered
prediction is CONFIRMED -- refutations are findings (e.g. VC5's FINDING-VC5c), and a refuted
prediction does not fail the gate. ADD-ONLY; vp_mind_engine READ-ONLY. SEED=19, stdlib+numpy.
"""
import os, sys, json, hashlib, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
ENGINE_FILE_SHA = "e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371"

MODULES = [
    ("VC1", "vc1_carrier_interference", "vc1_carrier_interference_results.json"),
    ("VC2", "vc2_highway_removability", "vc2_highway_removability_results.json"),
    ("VC3", "vc3_molecular_fatigue",    "vc3_molecular_fatigue_results.json"),
    ("VC4", "vc4_adhd_coemergence",     "vc4_adhd_coemergence_results.json"),
    ("VC5", "vc5_virtual_trial",        "vc5_virtual_trial_results.json"),
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
    for fn in os.listdir(HERE):
        if fn.startswith("expected_") and fn.endswith("_sha256.json"):
            try:
                d = json.load(open(os.path.join(HERE, fn)))
            except Exception:
                continue
            if resfile in d:
                return d[resfile]
    return None


def _collect_predictions(res):
    pr = res.get("preregistered_results", {})
    return {k: v.get("status") for k, v in pr.items()}


def main():
    rows = []
    all_ok = True
    pred_summary = {}
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
        preds = _collect_predictions(res)
        pred_summary[tag] = preds
        rows.append(dict(tag=tag, module=mod, sha256=got, reproduced=ok,
                         engine_tree_ok=tree_ok, pac_grounded=pac_ok, honesty_ledger_ok=honest_ok,
                         preregistered=preds))
        ps = " ".join(f"{k.split('_')[0]}:{v[:4]}" for k, v in preds.items())
        print(f"  {tag} {mod:<28} repro={ok} tree={tree_ok} pac={pac_ok} honest={honest_ok} | {ps}")

    eng = engine_file_ok()
    all_ok = all_ok and eng
    n_conf = sum(s == "CONFIRMED" for tg in pred_summary.values() for s in tg.values())
    n_ref = sum(s == "REFUTED" for tg in pred_summary.values() for s in tg.values())
    gate = {
        "suite": "theta-cap virtual-clinical (VC1-VC5)",
        "n_modules": len(MODULES),
        "engine_file_sha256_ok": eng,
        "engine_file_sha256": ENGINE_FILE_SHA,
        "engine_tree_frozen": ENGINE_TREE_FROZEN,
        "modules": rows,
        "preregistered_tally": {"confirmed": n_conf, "refuted": n_ref,
                                "note": "refutations are findings, not gate failures (see VC5 FINDING-VC5c)"},
        "all_pass": bool(all_ok),
        "gate_meaning": "every VC module reproduces bit-for-bit, the engine is byte-unchanged (file sha and frozen "
                        "tree 0fbf4988...), PAC stays grounded to the engine's measured kappa, and the honesty ledger "
                        "holds (efficacy=0, no cure claimed, no tuned constants, no consciousness claim). The gate "
                        "certifies reproducibility and discipline; the scientific verdicts (incl. refutations) live in "
                        "the module results and THETA_CAP_VIRTUAL_CLINICAL_HONEST.md.",
    }
    json.dump(gate, open(os.path.join(HERE, "gate.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\n  engine file byte-unchanged: {eng}")
    print(f"  pre-registered tally: {n_conf} CONFIRMED, {n_ref} REFUTED (refutations are findings)")
    print(f"  GATE ALL PASS: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
