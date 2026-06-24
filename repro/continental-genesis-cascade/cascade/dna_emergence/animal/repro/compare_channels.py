#!/usr/bin/env python3
"""compare_channels.py -- read the SAME orthologous genes through TWO channels and ask
   whether they are one channel or decoupled:
     (A) VP MATERIAL channel  : gamma = -mean(NN stacking dG)        -> |Delta-gamma| per pair
     (B) AVERAGE/CLOCK channel: substitutions over a global alignment -> the clock distance
   The question (this is the "doubt the average theory" test): does the clock (B), which
   the average theory turns into deep-time trees, PREDICT material change (A)? If r ~ 0,
   the two are different physical channels and the clock cannot be read as a material/age axis.

   results/orthologs.json  ->  results/channel_records.json   (+ console report)
"""
import json, itertools, math, os
from statistics import mean, pstdev
from Bio.Align import PairwiseAligner
from vp_gamma_engine import gamma

HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "results")
O = json.load(open(os.path.join(RES, "orthologs.json")))

GENES = ["ND1","ND2","COX1","COX2","ATP8","ATP6","COX3","ND3","ND4L","ND4","ND5","ND6","CYTB"]
CLADES = {"Elephantidae":["mammoth","asian_elephant","african_elephant"],
          "Homo":["human","neanderthal","denisovan"]}
LABEL = {"mammoth":"mammoth","asian_elephant":"Asian elephant","african_elephant":"African elephant",
         "human":"human(rCRS)","neanderthal":"Neanderthal","denisovan":"Denisovan"}

aln = PairwiseAligner()
aln.mode = "global"; aln.match_score = 1; aln.mismatch_score = -1
aln.open_gap_score = -5; aln.extend_gap_score = -1

def subs_and_pdist(a, b):
    """substitutions (mismatch columns) + indels over the best global alignment."""
    al = aln.align(a, b)[0]
    ta, tb = str(al[0]), str(al[1])
    sub = ind = algn = 0
    for x, y in zip(ta, tb):
        if x == "-" or y == "-":
            ind += 1
        else:
            algn += 1
            if x != y:
                sub += 1
    return sub, ind, sub / max(1, algn)

def pearson(xs, ys):
    n = len(xs); mx, my = mean(xs), mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys))
    return num/den if den else float("nan")

def main():
    print("="*92)
    print("PER-GENE gamma (VP material channel) across all six taxa")
    print("="*92)
    hdr = "gene  " + "".join(f"{LABEL[t][:11]:>12s}" for c in CLADES for t in CLADES[c])
    print(hdr)
    gam = {}
    for gn in GENES:
        row = f"{gn:5s} "
        for c in CLADES:
            for t in CLADES[c]:
                g = gamma(O[t]["genes"][gn]); gam[(t, gn)] = g
                row += f"{g:12.4f}"
        print(row)

    print("\n" + "="*92)
    print("H1  per-gene gamma RANGE within each clade (max-min)   [archaic/modern precedent: <0.0016]")
    print("="*92)
    for c, taxa in CLADES.items():
        print(f"\n  {c}: {[LABEL[t] for t in taxa]}")
        ranges = []
        for gn in GENES:
            vals = [gam[(t, gn)] for t in taxa]; r = max(vals) - min(vals); ranges.append(r)
            print(f"    {gn:5s} gamma_range = {r:.4f}   (min {min(vals):.4f} .. max {max(vals):.4f})")
        print(f"    --> clade max per-gene gamma range = {max(ranges):.4f}; mean = {mean(ranges):.4f}")

    print("\n" + "="*92)
    print("H2  DECOUPLING: substitutions (clock) vs |Delta-gamma| (material), per within-clade gene-pair")
    print("="*92)
    records = []
    for c, taxa in CLADES.items():
        print(f"\n  --- {c} ---")
        print(f"  {'pair':30s} {'gene':5s} {'subs':>5s} {'indel':>5s} {'p-dist':>8s} {'|d_gamma|':>10s}")
        for t1, t2 in itertools.combinations(taxa, 2):
            for gn in GENES:
                s1, s2 = O[t1]["genes"][gn], O[t2]["genes"][gn]
                sub, ind, pd = subs_and_pdist(s1, s2)
                dg = abs(gam[(t1, gn)] - gam[(t2, gn)])
                records.append(dict(clade=c, pair=f"{t1}|{t2}", gene=gn,
                                    subs=sub, indel=ind, pdist=pd, dgamma=dg))
                print(f"  {LABEL[t1][:13]+'/'+LABEL[t2][:13]:30s} {gn:5s} {sub:5d} {ind:5d} {pd:8.4f} {dg:10.5f}")

    print("\n" + "="*92)
    print("H2 SUMMARY: does the clock (substitutions) predict material change (|d gamma|)?")
    print("="*92)
    allsub = [r["subs"] for r in records]; alldg = [r["dgamma"] for r in records]
    r_overall = pearson(allsub, alldg)
    print(f"  overall Pearson r(subs, |d gamma|) = {r_overall:.3f}  (n={len(records)} gene-pairs)")
    tot_sub = sum(allsub)
    print(f"  total substitutions counted by the clock across all within-clade gene-pairs: {tot_sub}")
    print(f"  mean |d gamma| per gene-pair: {mean(alldg):.5f}  (sd {pstdev(alldg):.5f}); max {max(alldg):.5f}")
    allg = [gam[k] for k in gam]
    print(f"  gamma operating scale (all genes/taxa): mean {mean(allg):.4f}, range {min(allg):.4f}..{max(allg):.4f}")
    if tot_sub:
        print(f"  material movement per substitution: ~{sum(alldg)/tot_sub:.6f} gamma per substitution")
    json.dump(records, open(os.path.join(RES, "channel_records.json"), "w"))
    print("\nsaved results/channel_records.json")
    return r_overall

if __name__ == "__main__":
    main()
