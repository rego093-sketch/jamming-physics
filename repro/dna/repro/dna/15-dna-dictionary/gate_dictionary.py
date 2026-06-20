#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_dictionary.py — gate for the engine-generated DNA Dictionary.

Two checks, fail-closed:
  [1] DETERMINISM   — build() twice, sha256 of the two JSON dumps must be identical.
  [2] BASELINE PIN  — every value the Dictionary reports (gamma, gc, cpg, spinodal,
                      barrier) must equal the frozen regression_baseline.json to 1e-9
                      for every locus the baseline covers. This anchors the Dictionary
                      to the same locked truth the package's regression already pins.

Exit 0 = PASS.
"""
import sys, os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_dictionary as B

BASELINE = os.path.normpath(os.path.join(HERE, "..", "_verify", "regression_baseline.json"))
TOL = 1e-9

def dump(t):
    return json.dumps(t, ensure_ascii=False, indent=2, sort_keys=False)

def main():
    # [1] determinism
    t1 = B.build(); t2 = B.build()
    h1 = hashlib.sha256(dump(t1).encode()).hexdigest()
    h2 = hashlib.sha256(dump(t2).encode()).hexdigest()
    det = (h1 == h2)
    print(f"[1] determinism: {'PASS' if det else 'FAIL'}  sha256={h1[:16]}")

    # [2] baseline pin
    base = json.load(open(BASELINE))["cases"]
    # baseline keys look like "mammal_master/<org>/<GENE>"; map to "<org>_<GENE>"
    by_locus = {}
    for k, v in base.items():
        parts = k.split("/")
        if len(parts) == 3:
            _, org, gene = parts
            by_locus[f"{org}_{gene}"] = v
    checked = 0; bad = []
    for e in t1["entries"]:
        b = by_locus.get(e["locus"])
        if not b:
            continue
        checked += 1
        for fld in ("gamma", "gc", "cpg", "spinodal", "barrier"):
            ev = e["cpg_density"] if fld == "cpg" else e[fld]
            bv = b[fld]
            if abs(ev - bv) > TOL:
                bad.append((e["locus"], fld, ev, bv))
    pin = (len(bad) == 0 and checked > 0)
    print(f"[2] baseline pin: {'PASS' if pin else 'FAIL'}  loci_checked={checked}  mismatches={len(bad)}")
    for row in bad[:8]:
        print("    MISMATCH:", row)

    ok = det and pin
    print(f"\nOVERALL: {'PASS' if ok else 'FAIL'} (2/2)" if ok else f"\nOVERALL: FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
