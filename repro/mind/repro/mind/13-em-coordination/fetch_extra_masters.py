#!/usr/bin/env python3
# Fetch additional brain-region master genes via the SAME pipeline (SantaLucia NN dG37).
import json, time, urllib.request, urllib.parse, ssl
import numpy as np
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG = "Homo sapiens"
CTX = ssl.create_default_context(); CTX.check_hostname=False; CTX.verify_mode=ssl.CERT_NONE
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}
# region -> canonical master TF (well-established developmental masters)
GENES = {"GSX2":"striatum/LGE (GABAergic projection-neuron master)",
         "NKX2-1":"pallidum+hypothalamus (MGE/diencephalic master)",
         "TCF7L2":"thalamus (caudal diencephalon post-mitotic master)",
         "PHOX2B":"brainstem (hindbrain visceral-motor master)",
         "DLX2":"forebrain GABAergic interneuron master"}
def _get(u,tries=5):
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"brain-atlas-4d"}),timeout=45,context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e): time.sleep(3*(k+1)); continue
            if k==tries-1: raise
            time.sleep(1.5*(k+1))
def coords(sym):
    term=urllib.parse.quote(f'{sym}[Gene Name] AND "{ORG}"[Organism]')
    ids=json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")).get("esearchresult",{}).get("idlist",[])
    for gid in ids[:5]:
        time.sleep(0.34)
        try: doc=json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception: continue
        for g in doc.get("genomicinfo",[]):
            if not g.get("chraccver","").startswith("NC_"): continue
            a,b=int(g["chrstart"]),int(g["chrstop"]); strand="+" if a<=b else "-"
            gs,ge=(a,b) if strand=="+" else (b,a); return [g["chraccver"],gs,ge,strand]
    return None
def promoter(acc,gs,ge,strand):
    tss=gs if strand=="+" else ge
    lo,hi=(tss-2000,tss+500) if strand=="+" else (tss-500,tss+2000)
    u=f"{EU}/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text&seq_start={lo+1}&seq_stop={hi+1}"
    txt=_get(u); return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()
def comp(seq):
    steps=[-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    g=float(np.mean(steps)) if steps else float("nan")
    gc=sum(c in "GC" for c in seq)/max(1,len(seq))
    return round(g,4), round(gc,4), len(seq)
out={}
for sym,role in GENES.items():
    try:
        co=coords(sym)
        if not co: print(f"  {sym:<8} NOT FOUND"); continue
        time.sleep(0.34); seq=promoter(*co); g,gc,L=comp(seq)
        out[sym]=dict(gamma=g,gc=gc,acc=co[0],strand=co[3],length=L,role=role)
        print(f"  {sym:<8} gamma={g:.4f} gc={gc:.4f} acc={co[0]} {co[3]} len={L}")
    except Exception as e:
        print(f"  {sym:<8} ERROR {e}")
json.dump(out, open("extra_masters.json","w"), indent=1)
print("saved", len(out), "genes")
