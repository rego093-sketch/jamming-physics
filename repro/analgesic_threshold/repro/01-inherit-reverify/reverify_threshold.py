#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reverify_threshold.py  —  M1: re-verify the inherited threshold read, deterministically.
Asserts the 5 inherited nociceptor gamma re-derive from cached promoters and the R19
spinodal/barrier compute — drift 0 vs the frozen inherited values. No network.
Run:  python3 reverify_threshold.py  -> expected/reverify.json
"""
import os, sys, json
HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
INHER  = os.path.normpath(os.path.join(HERE, "..", "_inherited_data"))
sys.path.insert(0, ENGINE)
import dna_interpreter as D, vp_neuro_engine as VN

gj = json.load(open(os.path.join(INHER, "full_sensory_gamma.json")))["genes"]
cache = json.load(open(os.path.join(INHER, "full_sensory_promoters.cache.json")))
PAIN = ["PRDM12","NTRK1","SCN9A","TRPV1","TRPA1"]
FAIL=[]; rows={}
for s in PAIN:
    rede=round(D.gamma(cache[s]),4); frozen=gj[s]["gamma"]
    ok=(rede==frozen); FAIL+=[] if ok else [s]
    rows[s]={"gamma":frozen,"rederived":rede,"h_sp":round(VN.spinodal(frozen),6),
             "barrier":round(VN.barrier(frozen),6),"ok":ok}
out={"title":"M1 inherited threshold re-verify","rows":rows,"overall":"PASS" if not FAIL else "FAIL","fail":FAIL}
json.dump(out, open(os.path.join(HERE,"expected","reverify.json"),"w"), indent=1)
print("M1 inherited re-verify (drift 0 expected):")
for s,r in rows.items(): print(f"  [{'PASS' if r['ok'] else 'FAIL'}] {s:8} gamma={r['gamma']:.4f} |h_sp|={r['h_sp']:.4f} barrier={r['barrier']:.4f}")
print("OVERALL:", out["overall"]); raise SystemExit(1 if FAIL else 0)
