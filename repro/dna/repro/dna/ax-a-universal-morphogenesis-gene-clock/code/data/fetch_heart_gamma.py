#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_heart_gamma.py -- REAL measured gamma for the cardiac SUB-STAGE master genes.

v12 single-organ deep dive (the heart). Where v10/v11 treated the heart as ONE organ
with ONE master (NKX2-5), this fetches the master/specifier of each crisp cardiac
DEVELOPMENTAL MILESTONE so the heart's OWN sub-stage program can be tested against the
SAME gene clock -- a fair, single-system version of the organ-timing test.

PIPELINE IS IDENTICAL to fetch_organ_gamma.py / fetch_morpho_gamma.py / the kit
(never fitted):
  bare gene symbol -> NCBI exact TSS -> promoter window (TSS-2000..+500) ->
  gamma = -mean(NN stacking dG37, SantaLucia 1998).
gamma is READ-ONLY (human promoters only). Sequences are cached
(heart_promoters.cache.json) so the gamma values reproduce OFFLINE bit-for-bit.
NKX2-5 is re-fetched here and MUST match its value in organ_gamma.json (consistency).

Output: heart_gamma.json = each cardiac sub-stage master with accession/strand provenance.
Read (read-only) by heart_substages.py exactly as organ_gamma.json is read by organ_atlas.py.
"""
import os, sys, json, time, math, urllib.request, urllib.parse, ssl
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "heart_promoters.cache.json")
OUT = os.path.join(HERE, "heart_gamma.json")
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG = "Homo sapiens"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# SantaLucia 1998 unified NN dG37 (kcal/mol) -- identical READ-ONLY table to the kit.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

# Cardiac SUB-STAGE specifier master genes, one canonical specifier per crisp milestone.
# Comment = milestone it specifies + its most characteristic role. The one-specifier-per-
# milestone mapping is a documented forced choice ([F] in LEDGER_heart): cardiac TFs are
# pleiotropic across stages; each gene is taken here for its single most canonical role.
GENES = [
    "NKX2-5",   # cardiac crescent / specification (cardiac master TF; earliest cardiac marker)
    "GATA4",    # heart-tube fusion (loss -> cardia bifida; tubes fail to fuse)
    "HAND2",    # cardiac looping / right ventricle (essential for d-loop & RV)
    "ISL1",     # second heart field / outflow-tract elongation (the SHF master)
    "TBX5",     # chamber formation / identity (chamber-specific; Holt-Oram ASD/VSD)
    "SOX9",     # endocardial-cushion / valve-primordium EMT (cushion mesenchyme)
    "MEF2C",    # ventricular myocardial differentiation / septation (RV/OFT myocardium)
    "TBX1",     # outflow-tract (conotruncal) septation (DiGeorge 22q11; aortopulmonary septum)
]

def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "heart-substage-4d"}),
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
    genes = {}
    print(f"{'gene':<9}{'gamma':>9}{'GC':>8}   provenance")
    for sym in GENES:
        if sym in cache:
            seq, p = cache[sym]["seq"], cache[sym]["prov"]
        else:
            co = gene_coords(sym)
            if not co:
                print(f"  {sym:<9}{'--':>9}{'--':>8}   NOT FOUND"); continue
            time.sleep(0.34)
            seq = fetch_promoter(*co)
            p = f"{co[0]} {co[3]} TSS-2000..+500"
            cache[sym] = dict(seq=seq, prov=p)
            json.dump(cache, open(CACHE, "w"))
        comp = composition(seq)
        comp["src"] = p
        genes[sym] = comp
        print(f"  {sym:<9}{comp['gamma']:>9.4f}{comp['gc']:>8.4f}   {p} (len {len(seq)})")

    out = dict(
        _atlas="cardiac sub-stage specifier master genes (v12, single-organ deep dive)",
        _provenance=(
            "gamma = -mean(NN stacking dG37, SantaLucia 1998); READ-ONLY measured values from "
            "human proximal promoters (NCBI exact TSS -> window TSS-2000..+500). IDENTICAL pipeline "
            "to fetch_organ_gamma.py / the kit; never fitted. Each gene carries its accession/strand. "
            "Sequences cached in heart_promoters.cache.json so gamma reproduces offline bit-for-bit."),
        genes=genes,
    )
    json.dump(out, open(OUT, "w"), indent=1)

    if len(genes) >= 3:
        gs = [v["gamma"] for v in genes.values()]; gc = [v["gc"] for v in genes.values()]
        r = float(np.corrcoef(gs, gc)[0, 1])
        print(f"\ncorr(gamma,GC) over {len(genes)} cardiac sub-stage genes = {r:.3f}  (kit human atlas: ~0.99)")
    print(f"\nwrote {len(genes)} cardiac sub-stage genes -> {OUT}")

if __name__ == "__main__":
    main()
