#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_promoter_gamma.py — the WORKING NCBI promoter γ fetcher this seed ships with.

The research this seed launches is data-driven: every master gene's γ is a MEASURED input,
γ = −mean(SantaLucia-1998 unified NN stacking ΔG37) over the human proximal-promoter window
TSS−2000..+500 (2501 bp), fetched from NCBI by exact accession + 1-based window + strand. The
inherited cache (inherited/*_promoters.cache.json) was built with THIS code; the offline gate
(tools/verify_seed.py) recomputes γ from the cache bit-for-bit, so the seed reproduces with no
network. Use this script to ADD a new master gene during research (then re-freeze its hash).

Two modes:
  python3 tools/fetch_promoter_gamma.py SYM1 SYM2 ...        # fetch named genes, print γ
  python3 tools/fetch_promoter_gamma.py --cache path.json    # re-verify a cache against live NCBI

γ is MEASURED [V], never fitted. Identity/order of the gene→organ master is the DNA volume's [V],
cited not re-derived. Network required for live fetch; offline recompute lives in verify_seed.py.
"""
import urllib.request, json, time, hashlib, sys

NN_DG37 = {'AA':-1.00,'TT':-1.00,'AT':-0.88,'TA':-0.58,'CA':-1.45,'TG':-1.45,
           'GT':-1.44,'AC':-1.44,'CT':-1.28,'AG':-1.28,'GA':-1.30,'TC':-1.30,
           'CG':-2.17,'GC':-2.24,'GG':-1.84,'CC':-1.84}
UA = {"User-Agent": "vp-emergence-seed/0.1 (jamming-physics.org; ORCID 0009-0002-7535-8245)"}


def gamma_of(seq):
    seq = "".join(c for c in seq.upper() if c in "ACGT")
    st = [NN_DG37[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN_DG37]
    return -sum(st)/len(st) if st else None
def gc_of(seq):
    seq = "".join(c for c in seq.upper() if c in "ACGT")
    return (seq.count("G")+seq.count("C"))/len(seq) if seq else None
def _get(url, tries=4):
    last = None
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read().decode()
        except Exception as e:
            last = e; time.sleep(1.5*(k+1))
    raise last
def _gene_id(sym):
    d = json.loads(_get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                        f"?db=gene&term={sym}[sym]+AND+Homo+sapiens[orgn]+AND+alive[prop]&retmode=json"))
    return d["esearchresult"]["idlist"][0]
def _genomic_info(gid):
    d = json.loads(_get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id={gid}&retmode=json"))
    gi = d["result"][gid]["genomicinfo"][0]
    return gi["chraccver"], int(gi["chrstart"]), int(gi["chrstop"])
def _window(cs, ce):
    minus = cs > ce; tss = cs
    if not minus: st, sp, strand = tss-2000+1, tss+500+1, 1
    else:         st, sp, strand = tss-500+1,  tss+2000+1, 2
    return st, sp, strand, ("-" if minus else "+")
def _efetch(acc, st, sp, strand):
    raw = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
               f"?db=nuccore&id={acc}&rettype=fasta&retmode=text&seq_start={st}&seq_stop={sp}&strand={strand}")
    return "".join(l.strip() for l in raw.splitlines() if not l.startswith(">")).upper()


def measure(sym):
    """Full pipeline for one human gene symbol → measured-promoter γ record (network)."""
    gid = _gene_id(sym); time.sleep(0.34)
    acc, cs, ce = _genomic_info(gid); time.sleep(0.34)
    st, sp, strand, sign = _window(cs, ce); time.sleep(0.34)
    seq = _efetch(acc, st, sp, strand)
    return dict(acc=acc, ncbi_gene=gid, strand=sign, genomic_window=[st, sp], efetch_strand=strand,
                seq=seq, length=len(seq), gamma=round(gamma_of(seq), 4), gc=round(gc_of(seq), 4),
                seq_sha256=hashlib.sha256(seq.encode()).hexdigest())


def reverify_cache(path):
    cache = json.load(open(path, encoding="utf-8"))["genes"]
    allok = True
    for sym, crec in cache.items():
        live = _efetch(crec["acc"], crec["genomic_window"][0], crec["genomic_window"][1], crec["efetch_strand"])
        ok = (hashlib.sha256(live.encode()).hexdigest() == crec["seq_sha256"]) and (round(gamma_of(live), 4) == crec["gamma"])
        allok &= ok
        print(f"  {sym:9s} live γ={round(gamma_of(live),4):.4f}  cache γ={crec['gamma']:.4f}  {'OK' if ok else 'MISMATCH'}")
        time.sleep(0.5)
    print("ALL CACHE BYTE-EXACT vs LIVE NCBI:", allok)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--cache":
        reverify_cache(sys.argv[2])
    elif len(sys.argv) >= 2:
        for sym in sys.argv[1:]:
            try:
                r = measure(sym)
                print(f"{sym:9s} {r['acc']:15s} {r['strand']} len={r['length']} "
                      f"γ={r['gamma']:.4f} gc={r['gc']:.4f} sha={r['seq_sha256'][:16]}")
            except Exception as e:
                print(f"{sym:9s} FAIL {type(e).__name__}: {e}")
            time.sleep(0.5)
    else:
        print(__doc__)
