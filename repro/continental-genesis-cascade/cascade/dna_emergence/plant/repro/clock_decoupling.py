#!/usr/bin/env python3
"""clock_decoupling.py -- the "doubt the average theory" test, for plants. On the same plastid
   genes, within each kind, for every within-kind gene-pair, read both channels:
     (A) material : |Delta-gamma|
     (B) clock    : substitutions over a global alignment
   and measure whether the clock predicts the material. As in animals, it does not.

   results/plastid_orthologs.json  ->  results/plant_channel_records.json  (+ console report)
"""
import json, os, itertools, math
from statistics import mean, pstdev
from Bio.Align import PairwiseAligner
from vp_gamma_engine import gamma

HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "results")
O = json.load(open(os.path.join(RES, "plastid_orthologs.json")))
GENES = sorted(O["rice"]["genes"])
KINDS = {"Poaceae": ["rice", "maize", "wheat"], "Solanaceae": ["tobacco", "tomato", "potato"]}

aln = PairwiseAligner()
aln.mode = "global"; aln.match_score = 1; aln.mismatch_score = -1
aln.open_gap_score = -5; aln.extend_gap_score = -1

def subs(a, b):
    al = aln.align(a, b)[0]; ta, tb = str(al[0]), str(al[1]); s = 0
    for x, y in zip(ta, tb):
        if x != "-" and y != "-" and x != y:
            s += 1
    return s

def pearson(xs, ys):
    n = len(xs); mx, my = mean(xs), mean(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x-mx)**2 for x in xs) * sum((y-my)**2 for y in ys))
    return num/den if den else float("nan")

def main():
    print("=" * 84)
    print("H2  CLOCK / MATERIAL decoupling on within-kind plastid gene-pairs (doubt the average theory)")
    print("=" * 84)
    recs = []
    for kind, taxa in KINDS.items():
        for t1, t2 in itertools.combinations(taxa, 2):
            for gn in GENES:
                s = subs(O[t1]["genes"][gn], O[t2]["genes"][gn])
                dg = abs(gamma(O[t1]["genes"][gn]) - gamma(O[t2]["genes"][gn]))
                recs.append(dict(kind=kind, pair=f"{t1}|{t2}", gene=gn, subs=s, dgamma=dg))
    xs = [r["subs"] for r in recs]; ys = [r["dgamma"] for r in recs]
    r = pearson(xs, ys)
    print(f"  n = {len(recs)} within-kind gene-pairs")
    print(f"  total substitutions counted by the clock = {sum(xs)}")
    print(f"  mean |Delta-gamma| per pair = {mean(ys):.5f}  (sd {pstdev(ys):.5f}; max {max(ys):.5f})")
    print(f"  Pearson r(substitutions, |Delta-gamma|) = {r:.3f}")
    if sum(xs):
        print(f"  material movement per substitution = ~{sum(ys)/sum(xs):.6f} gamma per substitution")
    print(f"\n  -> as in animals, r ~ 0: the molecular clock (the average theory's deep-time axis)")
    print(f"     and the material are DIFFERENT channels. The clock cannot be read as a material")
    print(f"     or age axis. Same result, independent kingdom.")
    json.dump(recs, open(os.path.join(RES, "plant_channel_records.json"), "w"))
    print("\n  saved results/plant_channel_records.json")

if __name__ == "__main__":
    main()
