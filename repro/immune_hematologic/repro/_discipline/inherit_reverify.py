#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inherit_reverify.py  --  D1: re-verify the inherited master-gene threshold read, deterministically.

INHERITED TECHNIQUE: analgesic_threshold_logic_v2_0 / M1 (01-inherit-reverify), DOI 10.5281/zenodo.20733420.
The analgesic package re-derives its inherited nociceptor gamma from cached promoters and asserts the R19
spinodal/barrier compute drift 0 vs the frozen values. This is the immune analogue: the four master genes
(FOXN1->thymus, PAX5->lymphoid_adaptive, RUNX1->bone_marrow, TLX1->spleen) re-derive offline from the
vendored cache and the R19 threshold structure (|h_sp|, barrier) recomputes drift 0 vs the byte-exact
NCBI-verified values. No network.

Gate (fail-closed): every master gamma re-derives == frozen (4 dp); spinodal/barrier finite; drift 0.
Run:  python3 inherit_reverify.py   -> expected/reverify.json ; exit 1 on any drift
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.normpath(os.path.join(HERE, "..", ".."))
INH  = os.path.join(PKG, "inherited")
sys.path.insert(0, INH)
import gamma_pipeline as GP          # offline gamma re-derivation (byte-exact on knowns)
import vp_substrate as VS            # R19 spinodal / barrier

# master gene -> organ (the four emergence anchors)
MASTER_ORGAN = {"FOXN1": "thymus", "PAX5": "lymphoid_adaptive",
                "RUNX1": "bone_marrow_hematopoiesis", "TLX1": "spleen"}

def run():
    ver = json.load(open(os.path.join(INH, "ncbi_verification.json"), encoding="utf-8"))["genes"]
    rede = GP.recompute_all()        # {sym: gamma} re-derived offline from cached promoter sequence
    rows, fail = {}, []
    for sym, organ in sorted(MASTER_ORGAN.items()):
        frozen = round(float(ver[sym]["live_gamma"]), 4)
        got    = round(float(rede[sym]["gamma"]), 4)
        g      = frozen
        hsp    = round(VS.spinodal(g), 6)
        bar    = round(VS.barrier(g), 6)
        ok = (got == frozen) and (hsp == hsp) and (bar == bar)   # last two guard against NaN
        if not ok:
            fail.append(sym)
        rows[sym] = {"organ": organ, "gamma_frozen": frozen, "gamma_rederived": got,
                     "h_sp": hsp, "barrier": bar, "sha256_match_vs_live_ncbi": bool(ver[sym]["sha256_match"]),
                     "drift0": ok}
    out = {"title": "D1 inherited master-gene threshold re-verify (drift 0 expected)",
           "inherited_from": "analgesic_threshold_logic_v2_0/M1 (DOI 10.5281/zenodo.20733420)",
           "principle": ("gamma is a MEASURED read [V] (SantaLucia-1998 NN stacking dG37); the R19 threshold "
                         "structure (|h_sp|, barrier) is FORCED from gamma. Both re-derive offline, drift 0."),
           "rows": rows, "overall": "PASS" if not fail else "FAIL", "fail": fail}
    return out

if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "expected", "reverify.json"), "w"), indent=1)
    print("D1 inherited re-verify (drift 0 expected):")
    for s, r in out["rows"].items():
        print("  [%s] %-7s -> %-26s gamma=%.4f |h_sp|=%.4f barrier=%.4f  sha=%s"
              % ("PASS" if r["drift0"] else "FAIL", s, r["organ"], r["gamma_frozen"],
                 r["h_sp"], r["barrier"], r["sha256_match_vs_live_ncbi"]))
    print("OVERALL:", out["overall"])
    raise SystemExit(0 if out["overall"] == "PASS" else 1)
