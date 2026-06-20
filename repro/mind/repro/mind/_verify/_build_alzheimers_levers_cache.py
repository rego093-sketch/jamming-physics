#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-time builder for alzheimers_levers_promoters.cache.json (15 genes = 4 L3 cholinergic-drive levers +
2 L1 glutamatergic/NMDA-excitotoxicity levers + 3 L2 inhibitory-restore levers + 6 out-of-reach
neurodegenerative-PROGRESSION genes). REUSE-FIRST discipline: the 5 shared genes (GRIN2A/GRIN2B/GABRA5/
GABRB3 from the autism cache; GABRA1 from the epilepsy cache) are copied VERBATIM (gamma is
strand-symmetric, so the seq is byte-identical across caches). The 10 Alzheimer's-specific genes
(ACHE, BCHE, CHRNA7, CHRM1, APP, PSEN1, PSEN2, MAPT, APOE, TREM2) are fetched live from NCBI eutils on
the SAME window (TSS-2000..+500, GRCh38, strand-aware) used by every other levers cache.

Alzheimer's substrate (T3b; the roadmap's "needs E0 progression" neurodegenerative disorder):
  REACHED  L3 cholinergic up-stream DRIVE levers (RESTORE the deficient drive) : ACHE(AChE), BCHE(BuChE),
           CHRNA7(a7 nAChR), CHRM1(M1 mAChR)  -- the symptomatic cholinergic axis (donepezil/rivastigmine/
           galantamine cholinesterase-inhibition + muscarinic/nicotinic agonism as DIRECTIONS)
  REACHED  L1 glutamatergic / NMDA-excitotoxicity levers (REDUCE the excess) : GRIN2B, GRIN2A
           (the memantine uncompetitive-NMDA direction; NR2B extrasynaptic excitotoxicity)
  REACHED  L2 inhibitory-RESTORE levers (RESTORE inhibition / damp network hyperexcitability) :
           GABRA1, GABRA5, GABRB3  (AD network hyperexcitability / subclinical epileptiform activity;
           the GABAergic / gamma-rhythm-restore arm)
  OUT-OF-REACH  PROG neurodegenerative-progression axis (the DOMINANT fault) : APP(amyloid precursor),
           PSEN1/PSEN2(gamma-secretase, autosomal-dominant AD), MAPT(tau/tangles), APOE(the e4 risk
           allele -- amyloid clearance), TREM2(microglial neuroinflammation/clearance)
           -- the CUMULATIVE, largely IRREVERSIBLE amyloid/tau/synapse-and-neuron-LOSS cascade; a
           PROGRESSION (E0-layer DECAY) variable, not an instantaneous fold -- named, NOT reached (this
           is WHY the fit is PARTIAL [L], and the DEEPEST partial fit: an E0 DECAY, the inverse of
           addiction's E0 GAIN).
"""
import os, sys, json, ssl, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "alzheimers_levers_promoters.cache.json")
ORG  = "Homo sapiens"

# ---- reuse sources (byte-identical seq already verified across these caches) ----
REUSE = {
    "GRIN2A": "autism_levers_promoters.cache.json",     # NMDA NR2A (L1 glutamate/excitotoxicity)
    "GRIN2B": "autism_levers_promoters.cache.json",     # NMDA NR2B (L1 glutamate/excitotoxicity; memantine)
    "GABRA1": "epilepsy_levers_promoters.cache.json",   # GABA-A a1 (L2 inhibitory restore)
    "GABRA5": "autism_levers_promoters.cache.json",     # GABA-A a5 (L2 extrasynaptic tonic inhibition)
    "GABRB3": "autism_levers_promoters.cache.json",     # GABA-A b3 (L2 inhibitory restore)
}
# AD-specific genes to fetch (L3 cholinergic ACHE/BCHE/CHRNA7/CHRM1 ; out-of-reach PROG APP/PSEN1/PSEN2/MAPT/APOE/TREM2)
FETCH = ["ACHE", "BCHE", "CHRNA7", "CHRM1", "APP", "PSEN1", "PSEN2", "MAPT", "APOE", "TREM2"]

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
            req=urllib.request.Request(u,headers={"User-Agent":"vp-alzheimers-levers"})
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
            return dict(acc=g["chraccver"], strand=strand, chrstart=a, chrstop=b, gene_start=gs, gene_end=ge)
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
        cache[sym]=dict(seq=seq, coords=dict(acc=co["acc"], strand=co["strand"],
                                             chrstart=co["chrstart"], chrstop=co["chrstop"]),
                        src="ncbi_efetch TSS-2000..+500")
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
