#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gamma_pipeline.py  --  OFFLINE deterministic gamma recompute + verify (in-package, no network).

gamma = -mean( SantaLucia 1998 unified nearest-neighbour stacking dG37 ) over the proximal-promoter
window TSS-2000..+500 (2501 bp). This is the IDENTICAL measure the DNA morphogenesis gene-clock uses
(NN-stacking dG37, SantaLucia 1998); organ IDENTITY + emergence ORDER are owned by DNA and CITED here.

PIPELINE VALIDATION (why the to-measure masters are now trusted, not invented): the same code below
reproduces the two already-vendored values to 4 dp from cached sequence --
  FOXN1 -> 1.4533   TLX1 -> 1.4228   (gamma is strand-invariant; window read as revcomp for - strand).
Because the pipeline is byte-exact on the knowns, RUNX1 (1.3225) and PAX5 (1.4892), fetched by the SAME
window/method and frozen in organ_promoters.cache.json, are MEASURED inputs (grade [V]) -- never fitted.
Sequences are cached so gamma reproduces offline bit-for-bit (VP-SPEC C1).

RECONCILE OBLIGATION: organ gamma is the DNA package's SSOT. These four values were measured here via
the validated pipeline as the 'fetch' the to-measure entries called for; when re-vendored into the DNA
atlas they must match (the knowns already do, exactly). Grades (C3): [V] measured / [O] open.
"""
import os, json, hashlib, copy

# SantaLucia 1998 unified NN stacking dG37 (kcal/mol). Full 16 dinucleotides via reverse-complement
# symmetry: dG(XY) = dG(revcomp XY). (AA=TT, CA=TG, GT=AC, CT=AG, GA=TC, GG=CC; AT/TA/CG/GC self.)
NN_DG37 = {'AA':-1.00,'TT':-1.00,'AT':-0.88,'TA':-0.58,'CA':-1.45,'TG':-1.45,
           'GT':-1.44,'AC':-1.44,'CT':-1.28,'AG':-1.28,'GA':-1.30,'TC':-1.30,
           'CG':-2.17,'GC':-2.24,'GG':-1.84,'CC':-1.84}

_HERE  = os.path.dirname(os.path.abspath(__file__))
_CACHE = os.path.join(_HERE, "organ_promoters.cache.json")

def gamma_of(seq):
    """gamma = -mean(NN dG37) over a promoter sequence (ACGT only)."""
    seq = "".join(c for c in seq.upper() if c in "ACGT")
    steps = [NN_DG37[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN_DG37]
    if not steps:
        return None
    return -sum(steps) / len(steps)

def gc_of(seq):
    seq = "".join(c for c in seq.upper() if c in "ACGT")
    return (seq.count("G") + seq.count("C")) / len(seq) if seq else None

def load_cache():
    return json.load(open(_CACHE, encoding="utf-8"))

_RECOMPUTE_MEMO = None   # v0.13.0 speed: the promoter cache is vendored + static within a run, so the gamma
                         # recompute (SantaLucia dG37 over 2501 bp x 4 genes) is done once; a deep copy is
                         # returned each call so no caller can corrupt the memo. Values are byte-identical.

def recompute_all():
    """Recompute gamma/gc from cached sequence and verify the sequence sha256 (offline, deterministic).
    Memoised within the process (returns a fresh independent dict each call)."""
    global _RECOMPUTE_MEMO
    if _RECOMPUTE_MEMO is None:
        cache = load_cache(); out = {}
        for sym, rec in cache["genes"].items():
            seq = rec["seq"]
            sha = hashlib.sha256(seq.encode()).hexdigest()
            out[sym] = dict(organ=rec["organ"], gamma=round(gamma_of(seq), 4), gc=round(gc_of(seq), 4),
                            length=len(seq), seq_sha256=sha,
                            seq_sha256_ok=bool(sha == rec.get("seq_sha256")),
                            gamma_matches_cache=bool(round(gamma_of(seq), 4) == rec.get("gamma")))
        _RECOMPUTE_MEMO = out
    return copy.deepcopy(_RECOMPUTE_MEMO)

def validation_report():
    """Confirm the pipeline reproduces the KNOWN vendored values (FOXN1/TLX1) from cache -> trust the rest."""
    r = recompute_all()
    knowns = {"FOXN1": 1.4533, "TLX1": 1.4228}
    known_ok = all(r.get(s, {}).get("gamma") == v for s, v in knowns.items())
    all_seq_ok = all(v["seq_sha256_ok"] and v["gamma_matches_cache"] for v in r.values())
    return dict(per_gene=r, knowns_reproduced=known_ok, all_cache_consistent=all_seq_ok,
                pipeline_grade="[V] measured (SantaLucia 1998 NN dG37; knowns reproduced to 4 dp offline)")

if __name__ == "__main__":
    rep = validation_report()
    for s, v in rep["per_gene"].items():
        print(f"{s:6s} {v['organ']:26s} gamma={v['gamma']:.4f} gc={v['gc']:.4f} "
              f"sha_ok={v['seq_sha256_ok']} match={v['gamma_matches_cache']}")
    print("knowns reproduced (FOXN1/TLX1):", rep["knowns_reproduced"])
    print("all cache consistent:", rep["all_cache_consistent"])
