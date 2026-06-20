#!/usr/bin/env python3
# =============================================================================
#  structural_periodicity_probe.py  --  1차 조사 for Workstream E (structural/3D layer)
#
#  THE QUESTION (the user's insight): DNA is read structurally, not linearly. The
#  double helix puts bases ~10.4 bp apart on the SAME helical face, so they act
#  TOGETHER (bending / nucleosome rotational positioning / accessibility). A single
#  mean gamma -- or any linear average -- erases this by construction. Is the helical
#  arrangement signal actually present in the sequence, and is it invisible to gamma?
#
#  ESTABLISHED SCIENCE (grounding, not novel here):
#    The ~10.4 bp periodicity of AA/TT/TA (and RR/YY, and CpG) dinucleotides is the
#    nucleosome-positioning "genomic code" (Segal 2006; Trifonov; Ioshikhes). Bendable
#    dinucleotides phased at the helical repeat set the rotational position of the
#    histone octamer -> which DNA faces in/out -> accessibility of the +1 nucleosome at
#    the TSS -> transcription. It varies by genome (mouse weak) and in-vivo positioning
#    is dynamic, so single-window detection is method-dependent.
#
#  TEST: autocorrelation (ACF) of the WW (A/T) dinucleotide indicator signal at the
#  helical lag band (10-11 bp), REAL vs a composition-matched shuffle (same base counts,
#  arrangement destroyed). If real ACF(10-11) sits at a high percentile of the shuffle
#  distribution, the periodicity is in the ARRANGEMENT -> gamma (a mean) cannot see it.
#
#  HONEST SCOPE: this reads the SEQUENCE-INTRINSIC helical signal only. WHETHER a CpG is
#  actually accessible (nucleosome occupancy in a given cell) and WHICH distal elements
#  are in 3D contact (enhancer-promoter looping) need EXTERNAL structural data
#  (MNase-seq nucleosome maps, Hi-C). Those are [O] from sequence -- see Workstream E.
#
#  Run:  python3 structural_periodicity_probe.py [kit_root]
#  Deps: numpy. Reads promoter caches + sequences_v6 if present; else any *.fa passed.
# =============================================================================
import sys, glob, os
import numpy as np

WW = {"AA", "TT", "AT", "TA"}     # classic nucleosome-positioning dinucleotides
CG = {"CG"}                        # methylation substrate -- also helically phased

def sig_of(s, members):
    return np.array([1.0 if s[i:i+2] in members else 0.0 for i in range(len(s)-1)])

def acf(x, maxlag=40):
    x = x - x.mean(); v = np.dot(x, x)
    if v == 0: return np.zeros(maxlag+1)
    return np.array([np.dot(x[:len(x)-k], x[k:]) / v for k in range(maxlag+1)])

def helical_score(s, members, n=300, seed=7):
    """REAL ACF in helical band (lags 10-11) vs composition-matched shuffle distribution."""
    real = float(acf(sig_of(s, members))[10:12].max())
    rng = np.random.default_rng(seed); arr = np.array(list(s)); ctrl = []
    for _ in range(n):
        rng.shuffle(arr); ctrl.append(float(acf(sig_of("".join(arr), members))[10:12].max()))
    ctrl = np.array(ctrl)
    return real, float(ctrl.mean()), float((ctrl < real).mean() * 100.0)

def load_seqs(root):
    out = {}
    for f in glob.glob(os.path.join(root, "repro/dna/_engine/*promoters.cache.json")):
        import json
        for k, v in json.load(open(f)).items():
            if isinstance(v, str) and len(v) > 800 and set(v.upper()) <= set("ACGTN"):
                out[k.split("|")[-1]] = v.upper()
    for fa in glob.glob(os.path.join(root, "repro/dna/_verify/inputs/sequences_v6/*.fa")):
        s = "".join(l.strip() for l in open(fa) if not l.startswith(">")).upper()
        if len(s) > 800: out[os.path.basename(fa)[:-3]] = s
    # also any *.fa passed alongside
    for fa in glob.glob(os.path.join(root, "*.fa")):
        s = "".join(l.strip() for l in open(fa) if not l.startswith(">")).upper()
        if len(s) > 800: out[os.path.basename(fa)[:-3]] = s
    return out

def main(root="."):
    seqs = load_seqs(root)
    if not seqs:
        print("no sequences found; pass a kit root or a dir with *.fa"); return
    print("=" * 80)
    print("STRUCTURAL (HELICAL) LAYER 1차 조사 -- is the ~10.4 bp arrangement signal present,")
    print("and invisible to the scalar gamma? ACF(lag 10-11) real vs composition-matched shuffle.")
    print("=" * 80)
    print(f"{'sequence':<22}{'ACF(10-11)':>12}{'shuffle':>10}{'percentile':>12}  verdict")
    hits = 0
    for name in sorted(seqs):
        real, cm, pctl = helical_score(seqs[name], WW)
        verdict = ("arrangement signal (gamma-blind)" if pctl >= 90
                   else "weak/borderline" if pctl >= 70 else "not detected in single window")
        if pctl >= 90: hits += 1
        print(f"{name:<22}{real:>+12.3f}{cm:>+10.3f}{pctl:>11.0f}%  {verdict}")
    n = len(seqs)
    print("-" * 80)
    print(f"helical arrangement signal (>=90th pctl) in {hits}/{n} sequences "
          f"({hits/n*100:.0f}%). gamma (a mean) sees NONE of it -- the signal is in the ORDER.")
    print()
    print("HONEST BOUNDARY: this is the sequence-intrinsic helical signal only, and it is not")
    print("uniform (varies by locus/genome; mouse weaker -- matches literature). WHETHER a site is")
    print("accessible (nucleosome occupancy) and WHICH distal elements are in 3D contact (looping)")
    print("require EXTERNAL data (MNase-seq, Hi-C) -- [O] from sequence. That is Workstream E:")
    print("take nucleosome/contact maps as COORDINATES and lay them over the gamma + methylation")
    print("layers, so 'before-and-after' that the helix/folding bring together are read together.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
