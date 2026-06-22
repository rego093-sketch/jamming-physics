#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engine_tripwire.py  --  the frontal sim's substrate-integrity check
===================================================================
Proves the frozen R19 substrate the frontal sim runs on is BYTE-UNCHANGED and that
a uniform drive reproduces the M9 anchor EXACTLY.  Any 1-byte drift in the engine
file or in a copied reusable layer, or any failure to reproduce the anchor
bit-for-bit, fails the tripwire and therefore the frontal gate.

Checks (fast path, ~3 s):
  1. engine file sha256                     == frozen (provenance.json)
  2. the THREE copied reusable layer sha256 == frozen (LAYER_SHA256.json)
  3. M9 anchor R via the ENGINE integrator  == 0.38961455156044245  (bit-for-bit)
  4. frontal integrator (uniform drive)     == engine integrator    (bit-for-bit)

Optional (--full-tree, ~29 s):
  5. re-emerge the engine tree READ-ONLY and assert tree sha256 == frozen
     (0fbf4988...) and the M0..M16 subtree unchanged.

This tripwire NEVER imports or runs the mind atlas runner (run_all_atlas.py).
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")                       # repro/frontal/
ENGINE_DIR = os.path.join(ROOT, "_engine")
LAYERS_DIR = os.path.join(ROOT, "_layers")
FRONTAL_DIR = os.path.join(ROOT, "_frontal")


def _sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run(full_tree=False):
    prov = json.load(open(os.path.join(HERE, "provenance.json")))
    layer_pin = json.load(open(os.path.join(LAYERS_DIR, "LAYER_SHA256.json")))
    checks = {}

    # 1. engine file byte-identical
    eng_sha = _sha(os.path.join(ENGINE_DIR, "vp_mind_engine.py"))
    checks["engine_file_sha256_ok"] = bool(eng_sha == prov["engine_file_sha256"])
    checks["engine_file_sha256"] = eng_sha

    # 2. the three reusable layers byte-identical
    layer_ok = {}
    for fn, want in layer_pin["layers"].items():
        got = _sha(os.path.join(LAYERS_DIR, fn))
        layer_ok[fn] = bool(got == want)
    checks["layers_sha256_ok"] = bool(all(layer_ok.values()))
    checks["layers_detail"] = layer_ok

    # 3 + 4. M9 anchor bit-for-bit (imports frontal_common, which loads the engine)
    if FRONTAL_DIR not in sys.path:
        sys.path.insert(0, FRONTAL_DIR)
    import frontal_common as FC
    g = FC.engine_anchor_bitforbit()
    checks["m9_anchor_engine_bitforbit"] = bool(g["engine_matches_anchor_bitforbit"])
    checks["m9_anchor_frontal_matches_engine"] = bool(g["frontal_matches_engine_bitforbit"])
    checks["m9_anchor_R"] = g["engine_integrator_R"]

    # 5. optional full-tree re-emerge (READ-ONLY)
    if full_tree:
        inv = FC.engine_tree_invariants()
        checks["engine_tree_unchanged"] = bool(inv["engine_tree_unchanged"])
        checks["m0_16_subtree_unchanged"] = bool(inv["m0_16_subtree_unchanged"])
        checks["engine_tree_sha256"] = inv["engine_tree_sha256_live"]

    core = [checks["engine_file_sha256_ok"], checks["layers_sha256_ok"],
            checks["m9_anchor_engine_bitforbit"], checks["m9_anchor_frontal_matches_engine"]]
    if full_tree:
        core += [checks["engine_tree_unchanged"], checks["m0_16_subtree_unchanged"]]
    checks["TRIPWIRE_PASS"] = bool(all(core))
    return checks


if __name__ == "__main__":
    full = "--full-tree" in sys.argv
    c = run(full_tree=full)
    print("=" * 70)
    print("ENGINE TRIPWIRE" + ("  (+full tree re-emerge)" if full else "  (fast path)"))
    print("=" * 70)
    print(f"  engine file sha256 byte-identical : {c['engine_file_sha256_ok']}  ({c['engine_file_sha256'][:16]}...)")
    print(f"  3 reusable layers byte-identical  : {c['layers_sha256_ok']}  {c['layers_detail']}")
    print(f"  M9 anchor == engine (bit-for-bit) : {c['m9_anchor_engine_bitforbit']}  ({c['m9_anchor_R']})")
    print(f"  frontal integrator == engine      : {c['m9_anchor_frontal_matches_engine']}")
    if full:
        print(f"  engine tree unchanged             : {c['engine_tree_unchanged']}  ({c['engine_tree_sha256'][:16]}...)")
        print(f"  M0..M16 subtree unchanged         : {c['m0_16_subtree_unchanged']}")
    print("=" * 70)
    print("  TRIPWIRE: " + ("PASS" if c["TRIPWIRE_PASS"] else "FAIL"))
    sys.exit(0 if c["TRIPWIRE_PASS"] else 1)
