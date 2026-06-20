#!/usr/bin/env python3
# audit.py -- offline-reproducible AUDIT of the v1.9 frozen LCT constant against a live
#   NCBI re-fetch (frozen here as LCT_human_refetch.fa). Confirms the package's frozen
#   gamma is reproducible from the primary database, not merely internally consistent.
#   Both inputs are in-package (frozen) -> this audit needs no network (Constitution C1).
#
#   The full 3-locus audit (LCT_human, MCM6_enh_human, LCT_mouse), run live against NCBI
#   on 2026-06-16, returned |dgamma| = 0.0000 for all three (see NCBI_AUDIT.md). This script
#   re-verifies the headline LCT_human case from the frozen re-fetch.
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
NN = {"AA": -1.00, "TT": -1.00, "AT": -0.88, "TA": -0.58, "CA": -1.45, "TG": -1.45,
      "GT": -1.44, "AC": -1.44, "CT": -1.28, "AG": -1.28, "GA": -1.30, "TC": -1.30,
      "CG": -2.17, "GC": -2.24, "GG": -1.84, "CC": -1.84}

def read_fa(p): return "".join(l.strip() for l in open(p) if not l.startswith(">")).upper()
def gamma(s):
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]; return sum(v)/len(v) if v else float("nan")
def gc(s): return (s.count("C")+s.count("G"))/len(s)
def cpg_oe(s):
    L=len(s); nC=s.count("C"); nG=s.count("G"); nCG=s.count("CG"); return (nCG*L)/(nC*nG) if nC and nG else 0.0

def main():
    refetch = read_fa(os.path.join(HERE, "LCT_human_refetch.fa"))
    frozen = json.load(open(os.path.join(HERE, "..", "..", "_engine", "data", "lactase_interpretation.json")))
    fz = frozen["LCT_human"]["material"]
    g, c, o = gamma(refetch), gc(refetch), cpg_oe(refetch)
    print("AUDIT: v1.9 frozen LCT_human constant vs live-NCBI re-fetch (frozen in-package)")
    print(f"  re-fetched region: NC_000002.12:135836683-135839183 (GRCh38), {len(refetch)} bp")
    print(f"  gamma   re-fetch {g:.4f}  vs frozen {fz['gamma']:.4f}   |d| = {abs(g-fz['gamma']):.6f}")
    print(f"  GC      re-fetch {c:.4f}  vs frozen {fz['gc']:.4f}")
    print(f"  CpG O/E re-fetch {o:.4f}  vs frozen {fz['cpg_oe']:.4f}")
    ok = abs(g - fz["gamma"]) < 1e-3 and abs(c - fz["gc"]) < 1e-3
    print(f"  [{'PASS' if ok else 'FAIL'}] v1.9 frozen LCT constant is reproducible from primary NCBI data")
    return ok

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
