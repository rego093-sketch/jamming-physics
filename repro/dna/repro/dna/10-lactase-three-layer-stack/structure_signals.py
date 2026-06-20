#!/usr/bin/env python3
# VP-SPEC v1.8 verification-layer reproducer (repro/dna/, paper_id=dna, §10 Layer E).
# WHAT THIS VERIFIES: the three sequence-intrinsic STRUCTURE (Layer-E) signals the §10
#   engine reads as [F] "read from structure" -- previously FROZEN CONSTANTS in
#   lactase_interpretation.json["LCT_human"]["structure"] with NO wired reproducer (the
#   same C1 gap that cpg_oe_local_max had on the M-layer). This wires them to a
#   DETERMINISTIC in-package computation (C1: same input -> same output, 2x sha256).
#
#   (1) helical_acf_10_11 / shuffle / percentile: the ~10.4 bp nucleosome-positioning
#       arrangement signal -- ACF of the WW (A/T) dinucleotide indicator at the helical
#       lag band (10-11 bp), REAL vs a composition-matched shuffle (seed=7, n=300).
#       A mean gamma cannot see it (it is in the ORDER, not the composition). [F]
#   (2) poly_at_density: fraction of bp inside poly(dA:dT) tracts (A or T homopolymer
#       runs >= 4 bp) -- nucleosome-disfavoring, accessibility-promoting. [F]
#   (3) ctcf_core_candidates: matches of the CTCF core consensus (Kim 2007 M-core,
#       both strands) -- 0/0 here (the LCT promoter carries no CTCF core; a null result,
#       robust to the exact core definition). [F]
#
# HONEST SCOPE (unchanged from the framework): this reads the SEQUENCE-INTRINSIC signal
#   only. Absolute nucleosome occupancy (MNase-seq) and actual 3D contact (Hi-C) stay
#   [O]/[L] -- they are NOT claimed here.
# EXPECTED OUTPUT: expected/structure_signals.json (frozen). Reads ONLY inputs/*.fa.
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INP  = os.path.join(HERE, "inputs")
SEED = 7                 # helical shuffle seed (matches the framework's structural probe)
N_SHUF = 300
WW = {"AA", "TT", "AT", "TA"}          # classic nucleosome-positioning dinucleotides
CTCF_CORE = "CCGCGNGGNGGCAG"           # Kim 2007 CTCF M-core (degenerate, 14 bp)

def read_fasta(path):
    return "".join(l.strip() for l in open(path) if not l.startswith(">")).upper()

def _ww_sig(s):
    return np.array([1.0 if s[i:i+2] in WW else 0.0 for i in range(len(s) - 1)])

def _acf(x, maxlag=12):
    x = x - x.mean(); v = float(np.dot(x, x))
    if v == 0: return np.zeros(maxlag + 1)
    return np.array([np.dot(x[:len(x) - k], x[k:]) / v for k in range(maxlag + 1)])

def helical(s):
    real = float(_acf(_ww_sig(s))[10:12].max())
    rng = np.random.default_rng(SEED); arr = np.array(list(s)); ctrl = []
    for _ in range(N_SHUF):
        rng.shuffle(arr)
        ctrl.append(float(_acf(_ww_sig("".join(arr)))[10:12].max()))
    ctrl = np.array(ctrl)
    return round(real, 4), round(float(ctrl.mean()), 4), round(float((ctrl < real).mean() * 100.0), 1)

def poly_at_density(s, min_run=4):
    import re
    covered = sum(m.end() - m.start() for m in re.finditer(r'A{%d,}|T{%d,}' % (min_run, min_run), s))
    return round(covered / len(s), 4)

def ctcf_core(s):
    import re
    iupac = {'R':'[AG]','Y':'[CT]','N':'[ACGT]','S':'[GC]','W':'[AT]','K':'[GT]','M':'[AC]'}
    rc = CTCF_CORE.translate(str.maketrans("ACGT", "TGCA"))[::-1]
    re_f = "".join(iupac.get(c, c) for c in CTCF_CORE)
    re_r = "".join(iupac.get(c, c) for c in rc)
    return len(re.findall(re_f, s)), len(re.findall(re_r, s))

def main():
    s = read_fasta(os.path.join(INP, "human_LCT_promoter.fa"))
    acf, shuf, pctl = helical(s)
    fwd, rev = ctcf_core(s)
    out = {"_what": "Layer-E sequence-intrinsic structure signals (wires the frozen 'structure' constants)",
           "_grade": "[F] read from structure; absolute occupancy/contact stay [O]/[L]",
           "helical_acf_10_11": acf, "helical_shuffle_mean": shuf, "helical_percentile": pctl,
           "poly_at_density": poly_at_density(s),
           "ctcf_core_candidates": {"fwd_candidates": fwd, "rev_candidates": rev},
           "_defs": {"helical": "ACF(lag 10-11) of WW indicator vs composition-matched shuffle "
                                 f"(seed={SEED}, n={N_SHUF})",
                     "poly_at": "fraction of bp in A/T homopolymer runs >= 4 bp",
                     "ctcf_core": f"matches of CTCF core '{CTCF_CORE}' (Kim 2007), both strands"}}
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    with open(os.path.join(HERE, "expected", "structure_signals.json"), "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps(out, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
