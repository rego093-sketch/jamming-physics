#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_morpho_gamma.py  --  VENDORED DNA morphogenesis-gamma pipeline (single source; DO NOT re-derive).

gamma(gene) = -mean( NN-stacking dG37 , SantaLucia 1998 ) over the proximal-promoter window
TSS-2000..+500 of the cited human RefSeq/MANE TSS. The value is a MEASURED read-only input from the
genome -- never fitted. Sequences are cached in organ_promoters.cache.json so the value reproduces
OFFLINE bit-for-bit (VP-SPEC C1). Re-fetching from NCBI is provided for provenance only; the cached
sequence is authoritative for reproduction.

This mirrors the DNA package's fetch_morpho_gamma.py (NN-stacking thermodynamics). A 'to-measure' master
is fetched by this pipeline, then VENDORED into organ_gamma.json (SSOT: identity/order live in DNA).
"""
import os, json, math

_HERE  = os.path.dirname(os.path.abspath(__file__))
_CACHE = os.path.join(_HERE, "organ_promoters.cache.json")

# SantaLucia (1998) "A unified view" nearest-neighbour stacking dG37 (kcal/mol), read 5'->3' top strand.
NN_DG37 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}

def gamma_from_sequence(seq):
    """gamma = -mean(NN-stacking dG37) over all Watson-Crick NN steps (N steps skipped)."""
    seq = seq.upper()
    vals = [NN_DG37[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN_DG37]
    if not vals:
        raise ValueError("no valid NN steps")
    mean = sum(vals) / len(vals)
    acgt = sum(seq.count(b) for b in "ACGT")
    gc = (seq.count("G") + seq.count("C")) / acgt if acgt else 0.0
    return {"gamma": -mean, "mean_dG37": mean, "gc": gc, "n_steps": len(vals), "n_bases": len(seq)}

def measure_cached(master):
    """Compute gamma for a cached master from the authoritative cached sequence (offline, deterministic)."""
    cache = json.load(open(_CACHE, encoding="utf-8"))
    rec = cache[master]
    out = gamma_from_sequence(rec["sequence"])
    out.update({"master": master, "src": rec["fetch_region"], "assembly": rec.get("assembly"),
                "mane_select": rec.get("mane_select"), "tss_1based": rec.get("tss_1based")})
    return out

if __name__ == "__main__":
    import sys
    m = sys.argv[1] if len(sys.argv) > 1 else "RUNX2"
    r = measure_cached(m)
    print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()},
                     ensure_ascii=False, indent=2))
