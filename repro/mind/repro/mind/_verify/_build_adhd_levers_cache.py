#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-time builder for adhd_levers_promoters.cache.json (9 genes = 5 drive-tone levers + 4 gain-axis
out-of-reach). REUSE-FIRST discipline: the 6 shared genes (SLC6A4, SLC6A3, DRD4, COMT, TH from the
schizophrenia/depression caches; SLC6A2 from depression) are copied VERBATIM (gamma is strand-symmetric,
so the seq is byte-identical across caches). The 3 ADHD-specific genes (ADRA2A, DBH, SNAP25) are fetched
live from NCBI eutils on the SAME window (TSS-2000..+500, GRCh38, strand-aware) used by every other
levers cache.

ADHD substrate (sec.22 adhd_axis_specific lock, the SSOT):
  REACHED  drive-tone levers (L3): SLC6A3(DAT), SLC6A2(NET), SLC6A4(SERT), ADRA2A(a2A), DRD4(D4)
  OUT-OF-REACH gain axis (sec.22-O core): TH, DBH, SNAP25, COMT  (synthesis/release/catabolism)
  W (wiring): NONE -- the discriminant from autism (intact wiring).
"""
import os, sys, json, ssl, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "adhd_levers_promoters.cache.json")
ORG  = "Homo sapiens"

# ---- reuse sources (byte-identical seq already verified across these caches) ----
REUSE = {
    "SLC6A4": "depression_levers_promoters.cache.json",   # SERT (arousal tone, sec.22-T)
    "SLC6A3": "schizophrenia_levers_promoters.cache.json",# DAT (drive tone; sec.22-O by fault)
    "DRD4":   "schizophrenia_levers_promoters.cache.json",# D4 receptor (drive tone; sec.22-O by fault)
    "COMT":   "schizophrenia_levers_promoters.cache.json",# catabolism (gain axis, sec.22-O)
    "TH":     "schizophrenia_levers_promoters.cache.json",# synthesis (gain axis, sec.22-O)
    "SLC6A2": "depression_levers_promoters.cache.json",   # NET (drive tone; the atomoxetine arm)
}
# ADHD-specific genes to fetch (drive-tone lever ADRA2A ; gain-axis out-of-reach DBH/SNAP25)
FETCH = ["ADRA2A", "DBH", "SNAP25"]

NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}
def gamma(seq):
    s=seq.upper(); v=[-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(sum(v)/len(v)) if v else float("nan")

EU="https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CTX=ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
def _get(u,tries=6):
    for k in range(tries):
        try:
            req=urllib.request.Request(u,headers={"User-Agent":"vp-adhd-levers"})
            return urllib.request.urlopen(req,timeout=60,context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e): time.sleep(3*(k+1)); continue
            if k==tries-1: raise
            time.sleep(1.5*(k+1))
def _coords(sym):
    term=urllib.parse.quote(f'{sym}[Gene Name] AND "{ORG}"[Organism]')
    ids=json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")).get("esearchresult",{}).get("idlist",[])
    for gid in ids[:6]:
        time.sleep(0.34)
        try: doc=json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception: continue
        for g in doc.get("genomicinfo",[]):
            if not g.get("chraccver","").startswith("NC_"): continue
            a,b=int(g["chrstart"]),int(g["chrstop"])
            strand="+" if a<=b else "-"; gs,ge=(a,b) if strand=="+" else (b,a)
            return dict(acc=g["chraccver"], strand=strand, gene_start=gs, gene_end=ge)
    return None
def _promoter(acc,gs,ge,strand):
    tss=gs if strand=="+" else ge
    lo,hi=(tss-2000,tss+500) if strand=="+" else (tss-500,tss+2000)
    u=(f"{EU}/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text"
       f"&seq_start={lo+1}&seq_stop={hi+1}")
    txt=_get(u)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()

def main():
    cache = json.load(open(OUT)) if os.path.exists(OUT) else {}
    # 1) reuse
    for sym, src in REUSE.items():
        if sym in cache: continue
        d=json.load(open(os.path.join(HERE, src)))
        cache[sym]=dict(seq=d[sym]["seq"], coords=d[sym]["coords"],
                        src=f"REUSE verbatim from {src} (byte-identical; gamma strand-symmetric)")
        print(f"  {sym:<9} REUSE  gamma={gamma(cache[sym]['seq']):.4f} len={len(cache[sym]['seq'])} <- {src}")
    # 2) fetch
    for sym in FETCH:
        if sym in cache: print(f"  {sym:<9} already cached"); continue
        co=_coords(sym)
        if not co: print(f"  {sym:<9} NOT FOUND"); continue
        time.sleep(0.34)
        seq=_promoter(co["acc"], co["gene_start"], co["gene_end"], co["strand"])
        cache[sym]=dict(seq=seq, coords=co, src="ncbi_efetch TSS-2000..+500")
        json.dump(cache, open(OUT,"w"), indent=1)
        print(f"  {sym:<9} LIVE   gamma={gamma(seq):.4f} len={len(seq)} {co['acc']} {co['strand']}")
        time.sleep(0.20)
    json.dump(cache, open(OUT,"w"), indent=1)
    print(f"\ncache -> {OUT}  ({len(cache)} genes)")
    print("\ngene       gamma   |h_sp|=2(g/3)^1.5")
    for s in sorted(cache, key=lambda s: gamma(cache[s]['seq']), reverse=True):
        g=gamma(cache[s]['seq']); hsp=2*(g/3)**1.5
        print(f"  {s:<9} {g:6.4f}  {hsp:6.4f}")

if __name__=="__main__":
    main()
