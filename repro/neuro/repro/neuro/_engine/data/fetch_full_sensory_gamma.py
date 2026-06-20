#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch REAL measured γ for the remaining sensory modalities (touch, pain,
proprioception, vestibular) from NCBI — IDENTICAL pipeline/window/NN table as
fetch_taste_gamma.py so the γ values are on the same scale as the existing atlas.
γ is READ-ONLY (human promoters only). Sequences cached for offline reproduction."""
import os, json, time, urllib.request, urllib.parse, ssl
import numpy as np
HERE = "/home/claude/work/pkg/neuro_emergence_chain_integrated_v1_9_5/repro/neuro/_engine/data"
CACHE = os.path.join(HERE, "full_sensory_promoters.cache.json")
OUT   = os.path.join(HERE, "full_sensory_gamma.json")
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG = "Homo sapiens"
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
# SantaLucia 1998 unified NN dG37 — identical READ-ONLY table to the kit/taste pipeline.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}
# new sensory modalities: master TF + receptor/transduction effectors
GENES = ["PRDM12","NTRK1","SCN9A","TRPV1","TRPA1",      # nociception (pain)
         "RUNX3","ETV1","PIEZO2","NTRK3",               # proprioception (spindle)
         "ATOH1","POU4F3","OTOP1","OTOG"]               # vestibular (hair cell/otolith)
def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"sensory-atlas-4d"}),
                                          timeout=60, context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e): time.sleep(4*(k+1)); continue
            if k==tries-1: raise
            time.sleep(2.0*(k+1))
def gene_coords(sym):
    term = urllib.parse.quote(f'{sym}[Gene Name] AND "{ORG}"[Organism]')
    ids = json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")).get("esearchresult",{}).get("idlist",[])
    for gid in ids[:6]:
        time.sleep(0.34)
        try: doc = json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception: continue
        # require the official symbol to match (avoid paralog/ortholog mis-hits)
        if doc.get("name","").upper() != sym.upper(): continue
        for g in doc.get("genomicinfo", []):
            if not g.get("chraccver","").startswith("NC_"): continue
            a,b = int(g["chrstart"]), int(g["chrstop"])
            strand = "+" if a<=b else "-"
            gs,ge = (a,b) if strand=="+" else (b,a)
            return [g["chraccver"], gs, ge, strand]
    return None
def fetch_promoter(acc, gs, ge, strand):
    tss = gs if strand=="+" else ge
    lo,hi = (tss-2000, tss+500) if strand=="+" else (tss-500, tss+2000)
    u = (f"{EU}/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text&seq_start={lo+1}&seq_stop={hi+1}")
    txt = _get(u)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()
def composition(seq):
    steps=[-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    g=float(np.mean(steps)) if steps else float("nan")
    n=max(1,len(seq)); gc=sum(c in "GC" for c in seq)/n
    return dict(gamma=round(g,4), gc=round(gc,4))
def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    out={}
    print(f"{'gene':<9}{'gamma':>9}{'GC':>8}   provenance")
    for sym in GENES:
        if sym in cache: seq,prov = cache[sym], "cache"
        else:
            co=gene_coords(sym)
            if not co: print(f"  {sym:<9}{'--':>9}{'--':>8}   NOT FOUND"); continue
            time.sleep(0.34); seq=fetch_promoter(*co); cache[sym]=seq; prov=f"{co[0]} {co[3]}"
            json.dump(cache, open(CACHE,"w"))
        comp=composition(seq); out[sym]=comp
        print(f"  {sym:<9}{comp['gamma']:>9.4f}{comp['gc']:>8.4f}   {prov} (len {len(seq)})")
    json.dump(out, open(OUT,"w"), indent=1)
    if len(out)>=3:
        gs=[v["gamma"] for v in out.values()]; gc=[v["gc"] for v in out.values()]
        r=float(np.corrcoef(gs,gc)[0,1])
        print(f"\ncorr(γ,GC) over {len(out)} new sensory genes = {r:.3f}  (taste atlas: 0.995, organ atlas: 0.994)")
    print(f"wrote {len(out)} gene γ -> {OUT}")
if __name__=="__main__": main()
