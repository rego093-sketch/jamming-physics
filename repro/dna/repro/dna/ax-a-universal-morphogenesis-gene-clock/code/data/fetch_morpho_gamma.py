#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_morpho_gamma.py -- REAL measured gamma for the EXPANDED morphogenesis atlas.

Adds the master genes needed to grow the richer human head (scalp hair, eyebrows,
eyelashes, iris, teeth, philtrum, ...) and the gene-tagged animal appendages (limbs,
digits, fins, beak, feathers, scales, whiskers) on top of the original 26-gene
sensory_organ_gamma.json table.

PIPELINE IS IDENTICAL to the kit atlases and fetch_taste_gamma.py (never fitted):
  bare gene symbol -> NCBI exact TSS -> promoter window (TSS-2000..+500) ->
  gamma = -mean(NN stacking dG37, SantaLucia 1998).
gamma is READ-ONLY (we only read human promoters). Sequences are cached so the
gamma values reproduce offline afterward. corr(gamma,GC) ~ 0.99 (sanity, same as kit).

Output: morpho_gamma.json = the original 26 genes (copied bit-for-bit) + the new genes,
each new gene carrying its promoter accession/strand as provenance.
"""
import os, sys, json, time, math, urllib.request, urllib.parse, ssl
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_JSON = os.path.join(HERE, "sensory_organ_gamma.json")      # original 26 genes (read-only)
CACHE = os.path.join(HERE, "morpho_promoters.cache.json")
OUT = os.path.join(HERE, "morpho_gamma.json")
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG = "Homo sapiens"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# SantaLucia 1998 unified NN dG37 (kcal/mol) -- identical READ-ONLY table to the kit.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

# New master genes for the expanded atlas. Comments give the role + confidence label.
GENES = [
    # --- ectodermal-appendage program: hair / eyebrows / eyelashes / whiskers / feathers / scales
    "EDAR",     # [V] ectodysplasin receptor -- ectodermal-appendage MASTER (hair/feather/scale)
    "FOXN1",    # [V] hair-shaft keratinisation ("nude")
    "LEF1",     # [V] Wnt effector -- hair follicle + whisker + tooth placode
    "FGF5",     # [F] hair-LENGTH regulator (long-hair phenotype)
    "HOXC13",   # [V] hair-keratin master
    # --- pigment (iris / coat colour)
    "MITF",     # [V] melanocyte MASTER (iris stroma + coat)
    "TYR",      # [F] tyrosinase -- pigment effector
    # --- teeth
    "PAX9",     # [V] tooth MASTER (with MSX1)
    "MSX1",     # [V] tooth + craniofacial midline
    # --- limb / fin identity + outgrowth + digits
    "TBX5",     # [V] FORELIMB / pectoral-fin identity
    "TBX4",     # [V] HINDLIMB / pelvic-fin identity
    "FGF8",     # [V] AER -- limb/fin outgrowth (+ midface)
    "HOXD13",   # [V] autopod / DIGITS
    "GLI3",     # [F] anterior limb -- digit NUMBER
    # --- beak / jaw shape (Darwin's-finch program)
    "BMP4",     # [V] beak depth/width + jaw + feather bud
    "SOX9",     # [F] cartilage/skeleton + otic + feather
]

def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "morpho-atlas-4d"}),
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
    base = json.load(open(BASE_JSON, encoding="utf-8"))
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    new = {}
    prov = {}
    print(f"{'gene':<9}{'gamma':>9}{'GC':>8}   provenance")
    for sym in GENES:
        if sym in base["genes"]:
            print(f"  {sym:<9}{'(in base)':>9}"); continue
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
        new[sym] = comp; prov[sym] = p
        print(f"  {sym:<9}{comp['gamma']:>9.4f}{comp['gc']:>8.4f}   {p} (len {len(seq)})")

    # assemble the extended table: original 26 copied bit-for-bit + the new genes
    out = dict(base)
    out["genes"] = dict(base["genes"])     # copy (do not mutate the base object)
    out["genes"].update(new)
    out["_provenance_plus"] = (
        "EXTENDED atlas: original 26 genes are copied bit-for-bit from "
        "sensory_organ_gamma.json (measured, read-only). New genes fetched by the IDENTICAL "
        "pipeline (NCBI exact TSS -> promoter TSS-2000..+500 -> gamma = -mean(NN dG37, "
        "SantaLucia 1998)); each carries its accession/strand. gamma is never fitted.")
    json.dump(out, open(OUT, "w"), indent=1)

    # corr(gamma,GC) sanity over the NEW genes (the kit reports ~0.99)
    if len(new) >= 3:
        gs = [v["gamma"] for v in new.values()]; gc = [v["gc"] for v in new.values()]
        r = float(np.corrcoef(gs, gc)[0, 1])
        print(f"\ncorr(gamma,GC) over {len(new)} NEW genes = {r:.3f}  (kit human atlas: 0.994)")
    print(f"\nwrote {len(out['genes'])} total genes ({len(new)} new) -> {OUT}")

if __name__ == "__main__":
    main()
