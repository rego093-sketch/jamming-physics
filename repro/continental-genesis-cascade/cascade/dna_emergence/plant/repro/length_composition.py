#!/usr/bin/env python3
"""length_composition.py -- the honest instrument note (반증 = 발견). gamma = -mean(NN stacking
   dG) is a base-composition measure: GC-rich windows stack harder (higher gamma). That is WHY
   gamma is a LINEAGE property -- a lineage's genome GC content sets its gamma scale -- and NOT
   an environment property. We show the gamma<->GC link directly, on the same plastid + stress
   sequences, so the H1'/H3 readings are interpreted correctly and not over-read.

   data/* + results/plastid_orthologs.json  ->  console report (gamma vs GC correlation).
"""
import json, os, math
from statistics import mean
from Bio import SeqIO
from vp_gamma_engine import gamma, gc_frac

HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "results")
ST   = os.path.join(HERE, "data", "stress")

def cds(name):
    rec = SeqIO.read(os.path.join(ST, name + ".gb"), "genbank")
    f = [x for x in rec.features if x.type == "CDS"][0]
    return str(f.extract(rec.seq)).upper()

def pearson(xs, ys):
    n = len(xs); mx, my = mean(xs), mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys))
    return num/den if den else float("nan")

def main():
    print("=" * 84)
    print("COMPOSITION NOTE: gamma is a base-composition measure -> it is a LINEAGE property")
    print("=" * 84)

    # plastid genes pooled across all six taxa: gamma vs GC
    O = json.load(open(os.path.join(RES, "plastid_orthologs.json")))
    TAXA = ["rice", "maize", "wheat", "tobacco", "tomato", "potato"]
    gs = []; gc = []
    for t in TAXA:
        for gn, s in O[t]["genes"].items():
            gs.append(gamma(s)); gc.append(gc_frac(s))
    print(f"  plastid genes (all 6 taxa, n={len(gs)}): r(gamma, GC) = {pearson(gc, gs):.3f}")

    # CHS across species: gamma vs GC
    chs_names = ["CHS_arabidopsis", "CHS_barley", "CHS_maize", "CHS_grape", "CHS_snapdragon", "CHS_petunia"]
    cg = [gamma(cds(n)) for n in chs_names]; cc = [gc_frac(cds(n)) for n in chs_names]
    print(f"  CHS across 6 species: r(gamma, GC) = {pearson(cc, cg):.3f}")
    for n in chs_names:
        s = cds(n)
        print(f"      {n:16s} gamma={gamma(s):.4f}  gc={gc_frac(s):.3f}")

    print(f"\n  -> gamma rises with GC content. Grass genomes are GC-rich, so grass CHS reads high")
    print(f"     whether the grass lives in cold (barley) or warmth (maize); dicot genomes are less")
    print(f"     GC-rich, so dicot CHS reads lower whatever the habitat. This composition link is")
    print(f"     exactly why the material is a LINEAGE/KIND signature and the environment cannot")
    print(f"     write to it. It also bounds reads: compare gamma WITHIN a lineage, or control GC,")
    print(f"     before reading a difference as material. Stated, not hidden.")

if __name__ == "__main__":
    main()
