#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_organ_gamma.py -- REAL measured gamma for the INTERNAL (visceral) organ atlas.

v10 add-on. Supplies the master genes needed to make the *internal* organs
(heart, liver, stomach, lung, pancreas, gut, kidney, spleen) emerge from the SAME
gene clock that already drives the external face/body features -- so the organism
fills with structure as a DNA readout, not as hand-placed ellipsoids.

PIPELINE IS IDENTICAL to fetch_morpho_gamma.py / fetch_obesity_gamma.py / the kit
(never fitted):
  bare gene symbol -> NCBI exact TSS -> promoter window (TSS-2000..+500) ->
  gamma = -mean(NN stacking dG37, SantaLucia 1998).
gamma is READ-ONLY (we only read human promoters). Sequences are cached
(organ_promoters.cache.json) so the gamma values reproduce OFFLINE afterward,
bit-for-bit. corr(gamma,GC) ~ 0.99 (sanity, same as the kit).

Output: organ_gamma.json = each visceral-organ master with its promoter accession/
strand as provenance. This table is then read (read-only) by organ_atlas.py and
organ_timing.py exactly the way morpho_gamma.json is read by the existing atlases.
"""
import os, sys, json, time, math, urllib.request, urllib.parse, ssl
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "organ_promoters.cache.json")
OUT = os.path.join(HERE, "organ_gamma.json")
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG = "Homo sapiens"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# SantaLucia 1998 unified NN dG37 (kcal/mol) -- identical READ-ONLY table to the kit.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

# Visceral-organ MASTER genes. Comment gives organ + confidence label + first-appearance note.
# Every entry is a genuine [V] specification master for its organ primordium (used by the
# timing test); CDX2/midgut is [V] master but its first-appearance stage is SOFT (progressive
# gut-tube formation), so it is carried for the EMERGENCE ATLAS but EXCLUDED from the locked
# timing test -- exactly as MYF5/myotome was excluded in the v8 dev-timing line.
GENES = [
    "NKX2-5",   # [V] heart -- cardiac master (cardiogenic plate / heart tube)
    "HHEX",     # [V] liver -- hepatic-diverticulum specifier (also thyroid/forebrain: noted)
    "BARX1",    # [V] stomach -- gastric mesenchyme master (stomach dilation of foregut)
    "NKX2-1",   # [V] lung  -- lung/thyroid master (TTF1; respiratory diverticulum / lung buds)
    "PDX1",     # [V] pancreas -- pancreatic master (dorsal pancreatic bud)
    "SIX2",     # [V] kidney -- metanephric nephron-progenitor master (ureteric bud / metanephros)
    "TLX1",     # [V] spleen -- spleen primordium master (HOX11; dorsal mesogastrium)
    "CDX2",     # [V] midgut/intestine master -- ATLAS ONLY; soft staging -> excluded from timing test
]

def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "organ-atlas-4d"}),
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
        _atlas="internal/visceral organ master genes (v10)",
        _provenance=(
            "gamma = -mean(NN stacking dG37, SantaLucia 1998); READ-ONLY measured values from "
            "human proximal promoters (NCBI exact TSS -> window TSS-2000..+500). IDENTICAL pipeline "
            "to fetch_morpho_gamma.py / the kit; never fitted. Each gene carries its accession/strand. "
            "Sequences are cached in organ_promoters.cache.json so gamma reproduces offline bit-for-bit."),
        genes=genes,
    )
    json.dump(out, open(OUT, "w"), indent=1)

    if len(genes) >= 3:
        gs = [v["gamma"] for v in genes.values()]; gc = [v["gc"] for v in genes.values()]
        r = float(np.corrcoef(gs, gc)[0, 1])
        print(f"\ncorr(gamma,GC) over {len(genes)} organ-master genes = {r:.3f}  (kit human atlas: ~0.99)")
    print(f"\nwrote {len(genes)} organ-master genes -> {OUT}")

if __name__ == "__main__":
    main()
