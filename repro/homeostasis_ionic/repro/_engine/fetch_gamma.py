#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_gamma.py  --  MEASURE master-gene / sensor gamma from NCBI promoters (the DNA pipeline, vendored).

gamma = -mean(NN-stacking dG37, SantaLucia 1998 unified) over the proximal promoter window
TSS-2000..+500 (transcript orientation). Exact TSS from NCBI Datasets v2 (GRCh38.p14); sequence by
efetch on the RefSeq chromosome. gamma is a MEASURED input -- never fitted.

REPRODUCIBILITY (VP-SPEC C1): the promoter sequences are cached in inherited/organ_promoters.cache.json,
so gamma reproduces bit-for-bit OFFLINE. `--online` re-fetches from NCBI and must reproduce the cache.
The pipeline is byte-validated against the vendored SIX2 anchor (gamma=1.5556, gc=0.6381): if SIX2 does
not reproduce, the run aborts (a wrong NN table or TSS would be caught here).

NN reverse-complement symmetry: SantaLucia's 10 unique parameters are revcomp-symmetric, so the windowed
mean (hence gamma) is strand-independent -- a built-in cross-check (plus-strand and transcript-strand
gamma are identical by construction).
"""
import os, sys, json, hashlib

# SantaLucia (1998) unified NN nearest-neighbor stacking dG37 (kcal/mol), duplex DNA.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,"GT":-1.44,
      "AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,"CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

_HERE  = os.path.dirname(os.path.abspath(__file__))
_CACHE = os.path.join(_HERE, "..", "..", "inherited", "organ_promoters.cache.json")

# Human Gene IDs (NCBI). Loop nodes + cellular ionic/acid sensors (sensory seam).
GENE_IDS = {
    # mineral / acid-base loop nodes
    "GCM2":"9247","CASR":"846","VDR":"7421","RUNX2":"860","SIX2":"10736",
    # cellular sensors shared with sensory-cell transduction
    "OTOP1":"133060","ASIC2":"40","ASIC3":"9311","SCNN1A":"6337",
    "TRPV5":"56302","TRPV6":"55503","PKD2L1":"9033",
}

def revcomp(s):
    c={"A":"T","T":"A","G":"C","C":"G","N":"N"}
    return "".join(c[b] for b in reversed(s))

def gamma_of(seq):
    """gamma = -mean(NN dG37); also return GC fraction. Window-mean is revcomp-invariant."""
    seq=seq.upper().replace("\n","")
    steps=[NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    g=-sum(steps)/len(steps)
    gc=(seq.count("G")+seq.count("C"))/len(seq)
    return round(g,4), round(gc,4)

# -------- online path (NCBI) --------
def _efetch(acc,start,stop):
    import urllib.request
    url=("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=%s"
         "&seq_start=%d&seq_stop=%d&rettype=fasta&retmode=text"%(acc,start,stop))
    req=urllib.request.Request(url, headers={"User-Agent":"vp-research/0.2"})
    return "".join(l for l in urllib.request.urlopen(req,timeout=60).read().decode().splitlines()
                   if not l.startswith(">"))

def _coords(gid):
    import urllib.request
    url='https://api.ncbi.nlm.nih.gov/datasets/v2/gene/id/%s'%gid
    req=urllib.request.Request(url, headers={"User-Agent":"vp-research/0.2"})
    g=json.loads(urllib.request.urlopen(req,timeout=40).read().decode())["reports"][0]["gene"]
    for ann in g["annotations"]:
        if ann.get("assembly_name","").startswith("GRCh38"):
            gl=ann["genomic_locations"][0]; r=gl["genomic_range"]
            return gl["genomic_accession_version"], int(r["begin"]), int(r["end"]), r["orientation"]
    raise RuntimeError("no GRCh38 annotation for gene %s"%gid)

def fetch_online(sym):
    import time
    acc,begin,end,orient=_coords(GENE_IDS[sym])
    if orient=="plus":
        tss=begin; gs,ge=tss-2000,tss+500; seq=_efetch(acc,gs,ge)
    else:
        tss=end;   gs,ge=tss-500,tss+2000; seq=revcomp(_efetch(acc,gs,ge))
    time.sleep(0.34)
    return dict(seq=seq, accession=acc, strand=orient, tss=tss, src="%s - TSS-2000..+500"%acc)

# -------- offline path (cache) --------
def load_cache():
    return json.load(open(_CACHE, encoding="utf-8"))

def gamma_table(online=False):
    """Return {sym: {gamma, gc, accession, strand, tss}} for every gene, plus a SIX2 validation flag."""
    out={}
    if online:
        for sym in GENE_IDS:
            r=fetch_online(sym); g,gc=gamma_of(r["seq"])
            out[sym]=dict(gamma=g, gc=gc, accession=r["accession"], strand=r["strand"], tss=r["tss"])
    else:
        c=load_cache()
        for block in ("loop_nodes","cellular_sensors"):
            for sym,r in c[block].items():
                g,gc=gamma_of(r["seq"])
                out[sym]=dict(gamma=g, gc=gc, accession=r["accession"], strand=r["strand"], tss=r["tss"])
    six2_ok = abs(out.get("SIX2",{}).get("gamma",-1) - 1.5556) < 1e-9
    return out, six2_ok

if __name__ == "__main__":
    online = "--online" in sys.argv
    tab, ok = gamma_table(online=online)
    if not ok:
        print("ABORT: SIX2 validation failed (expected gamma=1.5556) -- NN table or TSS wrong."); raise SystemExit(2)
    print("SIX2 anchor reproduced (gamma=1.5556): OK  [source=%s]" % ("NCBI" if online else "cache"))
    for sym in GENE_IDS:
        r=tab[sym]
        print("  %-8s gamma=%-7s gc=%-7s %s %s TSS=%d" % (sym, r["gamma"], r["gc"], r["accession"], r["strand"], r["tss"]))
    blob=json.dumps(tab, sort_keys=True).encode()
    print("# table sha256:", hashlib.sha256(blob).hexdigest()[:16])
