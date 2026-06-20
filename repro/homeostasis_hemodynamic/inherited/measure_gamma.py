#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
measure_gamma.py  --  VENDORED master-gene gamma measurement (offline, deterministic).

This is the in-package analog of the DNA package's fetch_morpho_gamma.py, operating on the cached
proximal-promoter sequences in organ_promoters.cache.json so that every master-gene gamma reproduces
OFFLINE, bit-for-bit, with no network call (VP-SPEC C1).

  gamma = -mean(NN stacking dG37, SantaLucia 1998 unified parameters)  over the proximal-promoter
  window TSS-2000..+500 (gene orientation), taken from the NCBI exact gene-model 5' end.

NN-stacking dG37 is reverse-complement invariant, so gamma (and GC) are strand-independent; the genomic
window alone fixes the value. The pipeline is VALIDATED by reproducing the locked DNA-atlas value for
SIX2 (gamma = 1.5556, gc = 0.6381) EXACTLY from the documented convention with NO fitting. REN is then
measured on the SAME convention -- a measured input, never fitted (CHARTER: gamma measured, never fitted).

Provenance for each promoter (accession, strand, exact TSS, genomic window, length) lives beside the
cached sequence in organ_promoters.cache.json. To re-fetch from source instead of the cache, the
window is [TSS-500, TSS+2000] for a minus-strand gene (or [TSS-2000, TSS+500] for plus), efetch from
the cited NC_ accession; the result equals the cache.
"""
import os, json

_HERE  = os.path.dirname(os.path.abspath(__file__))
_CACHE = os.path.join(_HERE, "organ_promoters.cache.json")

# SantaLucia 1998 unified nearest-neighbor dG37 (kcal/mol); 16-entry, reverse-complement symmetric.
SL98 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}


def gamma_gc(seq):
    """gamma = -mean(NN dG37); gc = (G+C)/len. Deterministic, pure function of the sequence."""
    seq = seq.upper()
    nn = [SL98[seq[i:i + 2]] for i in range(len(seq) - 1) if seq[i:i + 2] in SL98]
    if not nn:
        return None, None, 0
    return -sum(nn) / len(nn), (seq.count("G") + seq.count("C")) / len(seq), len(seq)


def measure(master):
    """Recompute (gamma, gc, length) for a cached master-gene promoter, offline."""
    cache = json.load(open(_CACHE, encoding="utf-8"))
    p = cache["promoters"][master]
    g, gc, L = gamma_gc(p["sequence_5to3_transcribed"])
    return dict(master=master, accession=p["accession"], strand=p["strand"],
                tss_genomic=p["tss_genomic"], window_genomic=p["window_genomic"],
                length_bp=L, gamma=round(g, 4), gc=round(gc, 4), gamma_full=g)


def validate_pipeline():
    """The honesty gate: the pipeline must reproduce the locked SIX2 atlas value EXACTLY."""
    s = measure("SIX2")
    ok = (s["gamma"] == 1.5556 and s["gc"] == 0.6381 and s["length_bp"] == 2501)
    return ok, s


if __name__ == "__main__":
    ok, six2 = validate_pipeline()
    ren = measure("REN")
    print("SantaLucia-1998 NN-dG37 gamma pipeline (offline from organ_promoters.cache.json)")
    print("-" * 78)
    print("VALIDATION  SIX2  gamma=%.4f gc=%.4f len=%d  -> reproduces locked atlas (1.5556/0.6381): %s"
          % (six2["gamma"], six2["gc"], six2["length_bp"], ok))
    print("MEASURED    REN   gamma=%.4f gc=%.4f len=%d  [%s, %s, window %s]"
          % (ren["gamma"], ren["gc"], ren["length_bp"], ren["accession"], ren["strand"], ren["window_genomic"]))
    print("-" * 78)
    if not ok:
        raise SystemExit("PIPELINE VALIDATION FAILED: SIX2 not reproduced -> REN gamma NOT certifiable as [V]")
    print("OK: pipeline validated on SIX2; REN gamma = %.4f is a measured input on the identical convention [V]."
          % ren["gamma"])
