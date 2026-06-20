#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ncbi_verify.py  --  PRIMARY-SOURCE provenance for the four master-gene γ (offline gate + online audit).

WHY THIS EXISTS. The whole volume rests on one measured number per organ: γ = −mean(SantaLucia-1998 NN
stacking ΔG37) over the proximal-promoter window TSS−2000..+500. v0.2.0 measured those four γ from a
LOCAL cache (organ_promoters.cache.json) and validated the *pipeline* by reproducing the two known
values bit-exact. The remaining provenance question was: do the cached promoter sequences actually equal
the NIH reference genome? v0.3.0 answers it. Every cached sequence was re-fetched LIVE from NCBI by its
exact accession + 1-based window + efetch strand and compared byte-for-byte; the frozen result lives in
inherited/ncbi_verification.json, and NCBI-Gene RefSeq corroboration of each gene→organ master lives in
inherited/ncbi_gene_refseq.json.

TWO ENTRY POINTS.
  OFFLINE_check()    -- DETERMINISTIC, NO NETWORK (VP-SPEC C1). Confirms the frozen NCBI record is
                        self-consistent with the shipped cache and atlas: for all four genes the frozen
                        live_sha256 equals the cache seq_sha256 equals a fresh sha256 of the cached
                        sequence, the recomputed γ equals the atlas γ, and each accession's chromosome
                        matches the RefSeq map location. This is what the research gate calls.
  ONLINE_reverify()  -- NETWORK audit/refresh. Actually re-fetches from NCBI and re-confirms (optionally
                        rewrites the frozen record). Run this to re-audit against a newer assembly.

HONESTY. This module changes NO computed value. γ is owned by the DNA volume (SSOT) and only vendored
here; OFFLINE_check confirms provenance, it does not re-fit or move a single number. Grades (C3):
sequence identity + γ recompute [V]; gene→organ master [L] (RefSeq cited); the map from γ to organ
identity is still the DNA volume's [V], cited not re-derived.
"""
import os, json, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
_CACHE = os.path.join(_HERE, "organ_promoters.cache.json")
_GAMMA = os.path.join(_HERE, "organ_gamma.json")
_VER   = os.path.join(_HERE, "ncbi_verification.json")
_REF   = os.path.join(_HERE, "ncbi_gene_refseq.json")

# SantaLucia 1998 unified NN stacking dG37 (kcal/mol) -- identical table to gamma_pipeline.py.
NN_DG37 = {'AA':-1.00,'TT':-1.00,'AT':-0.88,'TA':-0.58,'CA':-1.45,'TG':-1.45,
           'GT':-1.44,'AC':-1.44,'CT':-1.28,'AG':-1.28,'GA':-1.30,'TC':-1.30,
           'CG':-2.17,'GC':-2.24,'GG':-1.84,'CC':-1.84}


def gamma_of(seq):
    seq = "".join(c for c in seq.upper() if c in "ACGT")
    steps = [NN_DG37[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN_DG37]
    return -sum(steps) / len(steps) if steps else None


def _load(p):
    return json.load(open(p, encoding="utf-8"))


# =================================================================================================
# OFFLINE -- deterministic, no network. The research gate uses this.
# =================================================================================================
def OFFLINE_check():
    """Confirm the frozen NCBI proof is self-consistent with the shipped cache + atlas (no network)."""
    cache = _load(_CACHE)["genes"]
    atlas = _load(_GAMMA)["genes"]
    ver   = _load(_VER)
    ref   = _load(_REF)
    rows = {}
    all_ok = True
    for sym, vrec in ver["genes"].items():
        crec = cache.get(sym, {})
        seq = crec.get("seq", "")
        fresh_sha = hashlib.sha256(seq.encode()).hexdigest()
        # frozen live sha == cache sha == fresh sha of the cached bytes
        sha_chain = (vrec["live_sha256"] == vrec["cached_sha256"] == crec.get("seq_sha256") == fresh_sha)
        # frozen live γ == γ recomputed from the cached bytes == atlas γ
        gfresh = round(gamma_of(seq), 4) if seq else None
        gamma_chain = (vrec["live_gamma"] == vrec["cached_gamma"] == gfresh == atlas.get(sym, {}).get("gamma"))
        # accession chromosome consistent with RefSeq map location
        chr_ok = bool(ref["genes"].get(sym, {}).get("chromosome_consistent", False))
        ok = bool(vrec.get("verified") and sha_chain and gamma_chain and chr_ok)
        all_ok = all_ok and ok
        rows[sym] = dict(organ=vrec["organ"], accession=vrec["accession"], assembly=vrec["assembly"],
                         sha256_chain_ok=bool(sha_chain), gamma_chain_ok=bool(gamma_chain),
                         gamma=gfresh, refseq_chromosome_ok=chr_ok, verified=ok)
    return dict(all_verified=bool(all_ok and ver.get("_all_four_verified", False)),
                assembly=ver.get("_assembly"), verified_on=ver.get("_verified_on"),
                database=ver.get("_database"), per_gene=rows,
                grade="[V] cached promoter sequences byte-exact vs live NCBI primary assembly; "
                      "γ recomputed identical; gene→organ master corroborated by RefSeq [L]")


# =================================================================================================
# ONLINE -- network audit / refresh. NOT called by the deterministic gate.
# =================================================================================================
def _efetch(acc, start, stop, strand, timeout=60):
    import urllib.request
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
           f"?db=nuccore&id={acc}&rettype=fasta&retmode=text"
           f"&seq_start={start}&seq_stop={stop}&strand={strand}")
    req = urllib.request.Request(url, headers={"User-Agent":
          "vp-verify/0.3 (jamming-physics.org cache audit; ORCID 0009-0002-7535-8245)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode()
    lines = raw.splitlines()
    header = lines[0][1:] if lines and lines[0].startswith(">") else "(no header)"
    seq = "".join(l.strip() for l in lines if not l.startswith(">")).upper()
    return header, seq


def ONLINE_reverify(write=False, sleep=0.5):
    """Re-fetch each promoter window from live NCBI and re-confirm byte-for-byte (network required)."""
    import time
    cache = _load(_CACHE)["genes"]
    out = {}
    all_ok = True
    for sym, crec in cache.items():
        acc = crec["acc"]; start, stop = crec["genomic_window"]; strand = crec["efetch_strand"]
        time.sleep(sleep)
        header, live = _efetch(acc, start, stop, strand)
        live_sha = hashlib.sha256(live.encode()).hexdigest()
        ok = (live_sha == crec["seq_sha256"]) and (live == crec["seq"]) \
             and (round(gamma_of(live), 4) == crec["gamma"])
        all_ok = all_ok and ok
        out[sym] = dict(organ=crec["organ"], accession=acc, defline=header,
                        live_sha256=live_sha, sha256_match=bool(live_sha == crec["seq_sha256"]),
                        live_gamma=round(gamma_of(live), 4), verified=bool(ok))
    if write and all_ok:
        ver = _load(_VER); ver["_all_four_verified"] = True
        for sym in out:
            ver["genes"][sym]["live_sha256"] = out[sym]["live_sha256"]
            ver["genes"][sym]["ncbi_defline"] = out[sym]["defline"]
        json.dump(ver, open(_VER, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
    return dict(all_verified=bool(all_ok), per_gene=out, refreshed=bool(write and all_ok))


if __name__ == "__main__":
    rep = OFFLINE_check()
    print("OFFLINE provenance check (no network)")
    for sym, v in rep["per_gene"].items():
        print(f"  {sym:6s} {v['organ']:26s} acc={v['accession']:14s} "
              f"sha_chain={v['sha256_chain_ok']} gamma_chain={v['gamma_chain_ok']} "
              f"refseq_chr={v['refseq_chromosome_ok']} γ={v['gamma']} verified={v['verified']}")
    print("  assembly:", rep["assembly"], "| verified_on:", rep["verified_on"])
    print("  ALL FOUR PROVENANCE-VERIFIED:", rep["all_verified"])
