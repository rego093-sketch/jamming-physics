#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergence_organs_wide.py -- Phase 5: organ ALLOMETRIC LAW over a WIDENED organ set.

ADD-ONLY extension of emergence_organs.py Part B. Purpose: raise the statistical
power of the allometric prediction-test by adding tissues that already carry a
single canonical published INTERSPECIFIC exponent, WITHOUT changing any pinned file.

Reads ONLY:
    param_db.json            -- the original 8 cited exponents (Stahl/Prothero)   [L]
    param_db_wide.json       -- 3 additional cited interspecific exponents        [L]
NEVER reads any validation-target file (NON-FIT, asserted by the wide gate).

The widened prediction is, as before, the SIGN+MAGNITUDE of (b-1) per organ --
coefficient-free, so no per-organ coefficient is ever chosen by us. The three new
tissues (skeleton, blood, skeletal_muscle) carry NO gene-clock master gamma in this
package, so they make the test STRICTLY MORE independent of the gamma layer.
"""
import os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB      = json.load(open(os.path.join(HERE, "param_db.json"),      encoding="utf-8"))
DB_WIDE = json.load(open(os.path.join(HERE, "param_db_wide.json"), encoding="utf-8"))

def base_table():
    """Original 8 cited exponents from param_db.json (locked)."""
    t = dict(DB["allometry"]["organ_scaling_exponent_reference"])
    t.pop("_grade", None); t.pop("_provenance", None)
    return t

def wide_table():
    """The 3 additional cited interspecific exponents from param_db_wide.json."""
    return {o: rec["value"] for o, rec in DB_WIDE["allometry_wide"].items()
            if not o.startswith("_")}

def merged_table():
    """All 11 cited exponents (8 base + 3 wide). Disjoint by construction."""
    t = base_table()
    for o, b in wide_table().items():
        assert o not in t, f"wide organ {o} already in base table -- inclusion rule violated"
        t[o] = b
    return t

BASE_ORGANS   = list(base_table().keys())
WIDE_ORGANS   = list(wide_table().keys())
MERGED_ORGANS = list(merged_table().keys())

def allometric_law(table):
    out = {}
    for o, b in table.items():
        out[o] = dict(allo_b=b, frac_scaling_exponent=round(b-1.0, 4),
                      direction=("falls" if b < 1 else ("isometric" if abs(b-1) < 0.02 else "rises")))
    return out

def result_hash():
    blob = json.dumps({"merged": allometric_law(merged_table())}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:12]

if __name__ == "__main__":
    M = allometric_law(merged_table())
    print("=" * 86)
    print("  WIDENED ALLOMETRIC GROWTH LAW (f ~ M_body^(b-1), cited interspecific b [L])")
    print("=" * 86)
    print(f"  base organs (param_db.json):       {len(BASE_ORGANS)}  {BASE_ORGANS}")
    print(f"  wide organs (param_db_wide.json):  {len(WIDE_ORGANS)}  {WIDE_ORGANS}")
    print(f"  merged:                            {len(MERGED_ORGANS)} organs")
    print(f"\n  {'organ':16s} {'allo_b':>7s} {'f~M^(b-1)':>10s}  direction   source")
    for o in sorted(M, key=lambda o: M[o]['allo_b']):
        f = M[o]; src = "wide" if o in WIDE_ORGANS else "base"
        print(f"  {o:16s} {f['allo_b']:>7.2f} {f['frac_scaling_exponent']:>10.3f}  {f['direction']:9s}  {src}")
    print("    -> PREDICTION: b<1 organs lose body-fraction as body grows; brain (lowest b) most.")
    print(f"\n  determinism: sha={result_hash()}")
    print("=" * 86)
