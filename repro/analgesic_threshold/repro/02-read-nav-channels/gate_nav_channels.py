#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_nav_channels.py  —  M8 gate (fail-closed), v2 expanded-target set.

(1) Determinism: gamma for EVERY fetched target re-derives byte-for-byte from the cached
    promoter using the locked engine — no network, pure arithmetic (drift 0).
(2) Scale sanity: corr(gamma,GC) across the FULL target set (5 inherited nociceptor reads +
    every v2 fetched gene) is >= 0.95 (the atlas reports ~0.99), i.e. every new read sits on
    the same scale as the inherited reads — a precondition for slotting them into one map.
(3) Provenance pinned: every fetched gene carries an NCBI accession (NC_*) and gene coords.
Writes expected/nav_gate.json.
"""
import os, sys, json

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
INHER  = os.path.normpath(os.path.join(HERE, "..", "_inherited_data"))
sys.path.insert(0, ENGINE)
import dna_interpreter as D

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

cache   = json.load(open(os.path.join(HERE, "nav_promoters.cache.json")))
read    = json.load(open(os.path.join(HERE, "nav_channels_gamma.json")))
fetched = read["genes"]
prov    = read["ncbi"]

print("M8 gate (expanded-target reads)")

# (1) determinism vs cache — every fetched gene
drift = 0
for sym in fetched:
    rede   = round(D.gamma(cache[sym]["seq"]), 4)
    frozen = fetched[sym]["gamma"]
    if rede != frozen:
        drift += 1
        print(f"  [FAIL] {sym} gamma drift: re-derived {rede} != frozen {frozen}")
check(f"all {len(fetched)} fetched gamma re-derive offline (drift 0)", drift == 0)

# (3) provenance pinned per gene (accession NC_* + coords)
prov_ok = all(
    prov.get(s, {}).get("ncbi_acc", "").startswith("NC_")
    and isinstance(prov.get(s, {}).get("gene_start"), int)
    and isinstance(prov.get(s, {}).get("gene_end"), int)
    for s in fetched
)
check("NCBI accession (NC_*) + coords pinned per fetched gene", prov_ok)

# (2) scale sanity: corr(gamma, GC) over the full target set
inher = json.load(open(os.path.join(INHER, "full_sensory_gamma.json")))["genes"]
PAIN  = ["PRDM12", "NTRK1", "SCN9A", "TRPV1", "TRPA1"]
g  = [inher[k]["gamma"] for k in PAIN] + [fetched[s]["gamma"] for s in fetched]
gc = [inher[k]["gc"]    for k in PAIN] + [fetched[s]["gc"]    for s in fetched]
n  = len(g); mg = sum(g)/n; mc = sum(gc)/n
cov = sum((a-mg)*(b-mc) for a, b in zip(g, gc))
sg  = sum((a-mg)**2 for a in g) ** 0.5; sc = sum((b-mc)**2 for b in gc) ** 0.5
corr = cov/(sg*sc)
print(f"  corr(gamma,GC) over {n} targets = {corr:.5f}")
check("corr(gamma,GC) >= 0.95 (all reads on one scale)", corr >= 0.95)

result = {"determinism": f"{len(fetched)} fetched genes re-derive from cache (drift {drift})",
          "n_targets_for_corr": n,
          "corr_gamma_gc_alltargets": round(corr, 6),
          "provenance_pinned": prov_ok,
          "fetched_genes": sorted(fetched.keys()),
          "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL}
json.dump(result, open(os.path.join(HERE, "expected", "nav_gate.json"), "w"), indent=1)

print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
