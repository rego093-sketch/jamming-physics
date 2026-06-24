#!/usr/bin/env python3
"""
vp_gamma_engine.py -- the VP DNA *material* reading, vendored faithfully from the
inherited interpreter (vp-site_mini: repro/dna/.../dna_interpreter.py).

LOCK: SantaLucia (1998) unified nearest-neighbour stacking dG (kcal/mol).
gamma(seq) = -mean(NN stacking dG)  = the stacking stiffness / interfacial tension
             of the locus.  Strand-symmetric, deterministic, bit-for-bit.
R19 switch threshold derived from gamma alone:  spinodal = (2/3sqrt3) gamma^1.5.

Nothing here is fitted. Changing any LOCK constant defines a new version.
"""
import math
from statistics import mean

# ---- LOCK (SantaLucia 1998) -- identical table to the inherited engine --------
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

def gamma(seq):
    """Material stacking stiffness = -mean(NN stacking dG). VP MATERIAL channel."""
    s = seq.upper()
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(mean(v)) if v else float("nan")

def gc_frac(seq):
    c=[x for x in seq.upper() if x in "ACGT"]
    return sum(1 for x in c if x in "GC")/len(c) if c else float("nan")

def cpg_density(seq):
    s=seq.upper(); return sum(1 for i in range(len(s)-1) if s[i:i+2]=="CG")/max(1,len(s)-1)

def r19_spinodal(g):
    """The locus's own R19 bistable threshold scale, from gamma alone."""
    return (2.0/(3.0*math.sqrt(3.0)))*g**1.5

def r19_barrier(g):
    return 0.25*g**2

if __name__=="__main__":
    import random; random.seed(7)
    s="".join(random.choice("ACGT") for _ in range(2500))
    print("gamma=",round(gamma(s),4),"gc=",round(gc_frac(s),4),
          "spinodal=",round(r19_spinodal(gamma(s)),4))
