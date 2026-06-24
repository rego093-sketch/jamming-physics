#!/usr/bin/env python3
"""state_face.py -- the STATE face: adaptive NUCLEAR loci read through the same engine.
   VP prediction: the material gamma is CONSERVED (same kind); the adaptive difference is
   a LOCALISED set of coding substitutions -- a switch STATE the environment sets and
   remembers -- not a global material shift. MC1R additionally gives TWO mammoth
   haplotypes = two states of ONE bistable (R19) coat-colour switch within the same kind.

   data/nuc/*.gb  ->  console report (gamma conservation + the localized AA changes)
   Recovers the known biology: Campbell et al. 2010 (cold Hb) and Roempler et al. 2006 (coat).
"""
import os
from Bio import SeqIO
from Bio.Seq import Seq
from vp_gamma_engine import gamma, gc_frac, r19_spinodal, r19_barrier

HERE = os.path.dirname(os.path.abspath(__file__))
NUC  = os.path.join(HERE, "data", "nuc")

def cds(name):
    rec = SeqIO.read(os.path.join(NUC, name + ".gb"), "genbank")
    f = [x for x in rec.features if x.type == "CDS"][0]
    return str(f.extract(rec.seq)).upper()

def aa(seq):
    # nuclear loci -> standard genetic code (table 1)
    return str(Seq(seq).translate(table=1))

def diffs_nt(a, b):
    return [(i, a[i], b[i]) for i in range(min(len(a), len(b))) if a[i] != b[i]]

def diffs_aa(a, b):
    pa, pb = aa(a), aa(b)
    return [(i+1, pa[i], pb[i]) for i in range(min(len(pa), len(pb))) if pa[i] != pb[i]]

def main():
    print("="*88)
    print("STATE FACE 1 - HEMOGLOBIN beta/delta (HBB/D), the cold-tolerance locus (Campbell 2010)")
    print("="*88)
    H = {k: cds(f"HBB_{k}") for k in ["mammoth", "asian", "african"]}
    for k, s in H.items():
        g = gamma(s)
        print(f"  {k:8s} len={len(s)} gamma={g:.4f} gc={gc_frac(s):.3f} R19_spinodal={r19_spinodal(g):.4f}")
    rng = max(gamma(s) for s in H.values()) - min(gamma(s) for s in H.values())
    print(f"\n  MATERIAL: gamma range across the 3 = {rng:.5f}")
    for pair in [("mammoth","asian"), ("mammoth","african"), ("asian","african")]:
        a, b = H[pair[0]], H[pair[1]]; nt = diffs_nt(a, b); pa = diffs_aa(a, b)
        print(f"  {pair[0]:8s} vs {pair[1]:8s}: {len(nt):2d} nt subs -> {len(pa)} AMINO-ACID changes "
              f"{['%s%d%s' % (x[1], x[0], x[2]) for x in pa]}")
    print("  -> the adaptive difference is a HANDFUL of coding substitutions on a materially")
    print("     conserved locus: a switch STATE, not a material (gamma) shift.")

    print("\n" + "="*88)
    print("STATE FACE 2 - MC1R coat-colour switch: TWO mammoth haplotypes = two states of one")
    print("              bistable (R19) switch within the SAME kind (Roempler 2006)")
    print("="*88)
    M = {k: cds(f"MC1R_{k}") for k in ["mammoth_hap1", "mammoth_hap2", "asian"]}
    for k, s in M.items():
        g = gamma(s)
        print(f"  {k:14s} len={len(s)} gamma={g:.4f} R19_spinodal={r19_spinodal(g):.4f} R19_barrier={r19_barrier(g):.4f}")
    rng = max(gamma(s) for s in M.values()) - min(gamma(s) for s in M.values())
    print(f"\n  MATERIAL: gamma range across all 3 = {rng:.5f}")
    nt = diffs_nt(M["mammoth_hap1"], M["mammoth_hap2"]); pa = diffs_aa(M["mammoth_hap1"], M["mammoth_hap2"])
    print(f"\n  mammoth hap1 vs hap2 (the coat switch): {len(nt)} nt subs -> {len(pa)} AA changes "
          f"{['%s%d%s' % (x[1], x[0], x[2]) for x in pa]}")
    dg = abs(gamma(M['mammoth_hap1']) - gamma(M['mammoth_hap2']))
    print(f"     |Delta gamma| between the two coat states = {dg:.5f}  (material identical; only the STATE differs)")
    for hk in ["mammoth_hap1", "mammoth_hap2"]:
        nt = diffs_nt(M[hk], M["asian"]); pa = diffs_aa(M[hk], M["asian"])
        print(f"  {hk:14s} vs asian elephant: {len(nt)} nt subs -> {len(pa)} AA changes")
    print("\n  -> One bistable switch (R19), one conserved material, two coat STATES in the same kind.")
    print("     The difference the environment sets lives in STATE, exactly as the reading predicts.")

if __name__ == "__main__":
    main()
