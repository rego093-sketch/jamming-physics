#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-time builder for ocd_levers_promoters.cache.json (12 genes = 4 L3 serotonergic/dopaminergic-drive
levers + 3 L1 glutamatergic-excitatory levers + 1 L2 inhibitory-restore lever + 4 out-of-reach
circuit-FIXATION / "stuck"-attractor LOCK genes). REUSE-FIRST discipline: the 5 shared genes
(SLC6A4 from the depression cache, HTR2A from the depression cache, DRD2 from the addiction cache,
GRIN2B from the autism cache, GABRA1 from the epilepsy cache) are copied VERBATIM (gamma is
strand-symmetric, so the seq is byte-identical across caches). The 7 OCD-specific genes
(HTR1B, SLC1A1, GRIK2, DLGAP3, SLITRK5, PTPRD, BTBD3) are fetched live from NCBI eutils on the SAME
window (TSS-2000..+500, GRCh38, strand-aware) used by every other levers cache.

OCD substrate (T3c; the roadmap's "cortico-striato-thalamo-cortical loop as a pathological limit-cycle /
stuck attractor; needs E1 + E2"):
  REACHED  L3 serotonergic/dopaminergic up-stream DRIVE levers : SLC6A4(SERT, the high-dose SSRI/
           clomipramine direction -- RESTORE/rebalance serotonergic tone, the first-line route),
           HTR2A(5-HT2A), HTR1B(5-HT1B autoreceptor), DRD2(D2 -- antipsychotic AUGMENTATION for
           refractory/tic-related OCD, REDUCE excess dopaminergic drive)  -- the instantaneous CSTC
           operating-point drive (the established serotonergic first-line + dopaminergic augmentation)
  REACHED  L1 glutamatergic / excitatory levers (REDUCE the hyperactive CSTC loop drive) : SLC1A1
           (EAAT3 glutamate transporter -- the most replicated OCD candidate gene; raising clearance
           LOWERS synaptic glutamate), GRIN2B(NMDA -- the riluzole/memantine/NAC glutamate-modulator
           direction), GRIK2(GluK2 kainate -- candidate-gene support)
  REACHED  L2 inhibitory-RESTORE lever (SPARSE -- a weak arm) : GABRA1  (reduced cortical GABA is
           reported in OCD and clonazepam is an adjunct; a single, sparse synaptic inhibitory-restore
           node -- the L2 arm of OCD is THIN, itself a finding)
  OUT-OF-REACH  LOCK circuit-FIXATION / "stuck"-attractor axis (the DOMINANT fault) : DLGAP3(SAPAP3 --
           the corticostriatal postsynaptic scaffold whose KO produces compulsive overgrooming, the
           canonical OCD circuit model), SLITRK5(corticostriatal synaptic adhesion; KO produces
           OCD-like overgrooming), PTPRD(synaptic-adhesion OCD GWAS hit), BTBD3(dendritic/circuit OCD
           GWAS hit)  -- the over-consolidated, self-sustaining, pathologically STABILISED limit-cycle
           (an over-deep basin / pathological hysteresis -- an E2/E0 variable), not an instantaneous
           fold -- named, NOT reached (this is WHY the fit is PARTIAL [L], and the THIRD distinct E0
           MODE: a STABILISATION / LOCK, distinct from addiction's E0 GAIN and Alzheimer's E0 DECAY).
"""
import os, sys, json, ssl, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "ocd_levers_promoters.cache.json")
ORG  = "Homo sapiens"

# ---- reuse sources (byte-identical seq already verified across these caches) ----
REUSE = {
    "SLC6A4": "depression_levers_promoters.cache.json",  # SERT (L3 serotonergic drive; SSRI)
    "HTR2A":  "depression_levers_promoters.cache.json",  # 5-HT2A (L3 serotonergic drive)
    "DRD2":   "addiction_levers_promoters.cache.json",   # D2 (L3 dopaminergic drive; antipsychotic augmentation)
    "GRIN2B": "autism_levers_promoters.cache.json",      # NMDA NR2B (L1 glutamatergic excitatory)
    "GABRA1": "epilepsy_levers_promoters.cache.json",    # GABA-A a1 (L2 inhibitory restore, sparse)
}
# OCD-specific genes to fetch (L3 HTR1B; L1 SLC1A1/GRIK2; out-of-reach LOCK DLGAP3/SLITRK5/PTPRD/BTBD3)
FETCH = ["HTR1B", "SLC1A1", "GRIK2", "DLGAP3", "SLITRK5", "PTPRD", "BTBD3"]

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
            req=urllib.request.Request(u,headers={"User-Agent":"vp-ocd-levers"})
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
