#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_gamma_xspecies.py -- REPRODUCIBLE cross-species promoter-gamma fetcher for the aging package.

This is the ONLINE provenance path: it queries NCBI E-utilities for each (gene x species) promoter
window (TSS-2000..+500), computes gamma = -mean(SantaLucia-1998 NN dG37) over the window (MEASURED,
never fitted), and writes inherited/aging_gamma_xspecies.json + inherited/aging_promoters.cache.json.

The committed cache (aging_promoters.cache.json) is the CANONICAL offline source: the package
reproduces gamma bit-for-bit from the cache without network (see xspecies_discriminant.verify_offline_
reproduces). Re-running this script online should reproduce the same cache; NCBI annotation drift is the
only thing that could change it, which is why the cache is vendored. Methodology is identical to the DNA
fetch_morpho_gamma pipeline."""
Caches sequences so gamma reproduces offline bit-for-bit."""
import urllib.request, urllib.parse, json, time, os, hashlib

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
NN_DG37 = {"AA":-1.00,"AC":-1.44,"AG":-1.28,"AT":-0.88,"CA":-1.45,"CC":-1.84,
           "CG":-2.17,"CT":-1.28,"GA":-1.30,"GC":-2.24,"GG":-1.84,"GT":-1.44,
           "TA":-0.58,"TC":-1.30,"TG":-1.45,"TT":-1.00}
UP, DOWN = 2000, 500

# (common, organism, AnAge maximum longevity yr [L, AnAge/Tacutu 2018], note)
SPECIES = [
 ("human",            "Homo sapiens",            122.5, "primate; ref"),
 ("chimpanzee",       "Pan troglodytes",          59.4, "closest primate relative"),
 ("African_elephant", "Loxodonta africana",       65.0, "TP53 ~20 retrogene copies (Abegglen 2015)"),
 ("bowhead_whale",    "Balaena mysticetus",      211.0, "longest-lived mammal"),
 ("naked_mole_rat",   "Heterocephalus glaber",    31.0, "negligible senescence; cancer-resistant"),
 ("little_brown_bat", "Myotis lucifugus",         34.0, "extreme longevity for body size"),
 ("dog",              "Canis lupus familiaris",   24.0, "domestic; size-lifespan inverse intra-species"),
 ("cattle",           "Bos taurus",               20.0, "large domestic ungulate"),
 ("house_mouse",      "Mus musculus",              4.0, "short-lived rodent model"),
 ("brown_rat",        "Rattus norvegicus",         3.8, "short-lived rodent model"),
 ("gray_opossum",     "Monodelphis domestica",     5.1, "marsupial; short-lived"),
]
GENES = ["TP53","CDKN2A","FOXO3","TERT"]

def _get(url):
    last=None
    for a in range(5):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return r.read().decode("utf-8","replace")
        except Exception as e:
            last=e; time.sleep(1.0*(a+1))
    raise RuntimeError(f"fetch failed {url}: {last}")

def gene_uid(sym, org):
    q = urllib.parse.quote(f'{sym}[gene] AND "{org}"[orgn]')
    d = json.loads(_get(EUTILS+f"esearch.fcgi?db=gene&term={q}&retmode=json"))
    time.sleep(0.4)
    ids = d["esearchresult"].get("idlist", [])
    return ids[0] if ids else None

def genomic_info(uid):
    d = json.loads(_get(EUTILS+f"esummary.fcgi?db=gene&id={uid}&retmode=json"))
    time.sleep(0.4)
    r = d["result"][uid]
    gi = r.get("genomicinfo") or []
    return r.get("name"), (gi[0] if gi else None)

def fetch_promoter(acc, start, stop):
    plus = start < stop; P = start
    if plus: s0,s1,strand = P-UP, P+DOWN, 1
    else:    s0,s1,strand = P-DOWN, P+UP, 2
    url=(EUTILS+f"efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text"
         f"&seq_start={s0}&seq_stop={s1}&strand={strand}")
    fa=_get(url); time.sleep(0.4)
    seq="".join(l.strip() for l in fa.splitlines() if not l.startswith(">"))
    return seq.upper(), ("+" if plus else "-"), acc, (s0,s1,strand)

def gamma_of(seq):
    seq="".join(c for c in seq if c in "ACGT")
    steps=[NN_DG37[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN_DG37]
    return (-sum(steps)/len(steps)) if steps else None

def main():
    cache={}; rows=[]
    for common, org, mlsp, note in SPECIES:
        for g in GENES:
            key=f"{g}|{org}"
            try:
                uid=gene_uid(g, org)
                if not uid:
                    rows.append(dict(gene=g, common=common, organism=org, mlsp=mlsp,
                                     gamma=None, status="no_gene_uid")); 
                    print(f"  {g:7s} {common:18s} -> NO UID"); continue
                name, gi = genomic_info(uid)
                if not gi:
                    rows.append(dict(gene=g, common=common, organism=org, mlsp=mlsp,
                                     gamma=None, status="no_genomicinfo", uid=uid))
                    print(f"  {g:7s} {common:18s} -> uid {uid} no genomicinfo"); continue
                seq, strand, acc, span = fetch_promoter(gi["chraccver"], gi["chrstart"], gi["chrstop"])
                gc = round(100*sum(c in 'GC' for c in seq)/len(seq),2) if seq else None
                gam = gamma_of(seq)
                cache[key]=dict(seq=seq, acc=acc, strand=strand, span=span)
                rows.append(dict(gene=g, common=common, organism=org, mlsp=mlsp,
                                 gamma=(round(gam,6) if gam is not None else None),
                                 gc_pct=gc, n=len(seq), acc=acc, strand=strand,
                                 uid=uid, sym=name, status="ok"))
                print(f"  {g:7s} {common:18s} -> g={gam:.4f} GC={gc}% n={len(seq)} {strand} {acc}")
            except Exception as e:
                rows.append(dict(gene=g, common=common, organism=org, mlsp=mlsp,
                                 gamma=None, status=f"err:{e}"))
                print(f"  {g:7s} {common:18s} -> ERR {e}")
    out=dict(_method="gamma=-mean(NN dG37, SantaLucia 1998); window TSS-2000..+500; measured, never fitted",
             species=[dict(common=c,organism=o,mlsp_yr=m,note=n) for c,o,m,n in SPECIES],
             genes=GENES, rows=rows)
    json.dump(out, open("fetchwork/xspecies_gamma.json","w"), indent=1, sort_keys=True)
    json.dump(cache, open("fetchwork/xspecies_promoters.cache.json","w"), indent=0, sort_keys=True)
    ok=sum(1 for r in rows if r["status"]=="ok")
    print(f"\nDONE: {ok}/{len(rows)} fetched OK. cache sha256:",
          hashlib.sha256(json.dumps(cache,sort_keys=True).encode()).hexdigest()[:16])

if __name__=="__main__": main()
