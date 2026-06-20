#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_taste_gamma.py — REAL measured γ for the tongue/taste organ from NCBI.

Same pipeline as the kit atlases: bare gene symbol -> NCBI exact TSS ->
promoter window (TSS-2000..+500) -> γ = -mean(NN stacking ΔG, SantaLucia 1998).
γ is READ-ONLY (we only read human promoters). Sequences are cached so the
γ values are reproducible offline afterward.
"""
import os, sys, json, time, math, urllib.request, urllib.parse, ssl
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "taste_promoters.cache.json")
OUT = os.path.join(HERE, "taste_gamma.json")
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG = "Homo sapiens"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# SantaLucia 1998 unified NN dG37 (kcal/mol) — identical READ-ONLY table to the kit.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

# tongue / taste organ: master = POU2F3 (taste-receptor-cell master TF), with
# the receptor + transduction effectors as partners.
GENES = ["POU2F3", "TAS1R1", "TAS1R2", "TAS1R3", "TAS2R38", "TRPM5", "PLCB2"]

def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "taste-atlas-4d"}),
                timeout=60, context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e):
                time.sleep(4*(k+1)); continue
            if k == tries-1: raise
            time.sleep(2.0*(k+1))

def gene_coords(sym):
    term = urllib.parse.quote(f'{sym}[Gene Name] AND "{ORG}"[Organism]')
    ids = json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")) \
            .get("esearchresult", {}).get("idlist", [])
    for gid in ids[:5]:
        time.sleep(0.34)
        try:
            doc = json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception:
            continue
        for g in doc.get("genomicinfo", []):
            if not g.get("chraccver", "").startswith("NC_"):
                continue
            a, b = int(g["chrstart"]), int(g["chrstop"])
            strand = "+" if a <= b else "-"
            gs, ge = (a, b) if strand == "+" else (b, a)
            return [g["chraccver"], gs, ge, strand]
    return None

def fetch_promoter(acc, gs, ge, strand):
    tss = gs if strand == "+" else ge
    lo, hi = (tss-2000, tss+500) if strand == "+" else (tss-500, tss+2000)
    u = (f"{EU}/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text"
         f"&seq_start={lo+1}&seq_stop={hi+1}")
    txt = _get(u)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()

def composition(seq):
    steps = [-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    g = float(np.mean(steps)) if steps else float("nan")
    n = max(1, len(seq))
    gc = sum(c in "GC" for c in seq) / n
    return dict(gamma=round(g, 4), gc=round(gc, 4))

def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    out = {}
    print(f"{'gene':<9}{'gamma':>9}{'GC':>8}   provenance")
    for sym in GENES:
        if sym in cache:
            seq, prov = cache[sym], "cache"
        else:
            co = gene_coords(sym)
            if not co:
                print(f"  {sym:<9}{'--':>9}{'--':>8}   NOT FOUND"); continue
            time.sleep(0.34)
            seq = fetch_promoter(*co)
            cache[sym] = seq; prov = f"{co[0]} {co[3]}"
            json.dump(cache, open(CACHE, "w"))
        comp = composition(seq)
        out[sym] = comp
        print(f"  {sym:<9}{comp['gamma']:>9.4f}{comp['gc']:>8.4f}   {prov} (len {len(seq)})")
    json.dump(out, open(OUT, "w"), indent=1)
    # corr(γ,GC) sanity (the kit reports ~0.99)
    if len(out) >= 3:
        gs = [v["gamma"] for v in out.values()]; gc = [v["gc"] for v in out.values()]
        r = float(np.corrcoef(gs, gc)[0, 1])
        print(f"\ncorr(γ,GC) over taste genes = {r:.3f}  (kit human atlas: 0.994)")
    print(f"\nwrote {len(out)} taste-gene γ -> {OUT}")

if __name__ == "__main__":
    main()
