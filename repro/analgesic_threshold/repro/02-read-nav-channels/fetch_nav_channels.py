#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_nav_channels.py  —  M8 (v2): read the EXPANDED analgesic target set.

v1.0 read the two missing nociceptor Na_V channels (SCN10A/Na_V1.8, SCN11A/Na_V1.9).
v2 extends GENES to the full burden-weighted target set across the three firing-threshold
levers (TARGET_EXPANSION_DESIGN §5):
  L1 (reduce inward current):  SCN3A, CACNA1B, CACNA1H, CACNA2D1, TRPM8, P2RX3, ASIC1, ASIC3
  L2 (increase K+ outward):    KCNQ2, KCNQ3, KCNQ5
  L3 (remove sensitising drive): NGF, CALCA, CALCB, CALCRL, RAMP1
  context/comparators:         OPRM1, OPRK1, OPRD1, CNR2
All on the IDENTICAL pipeline the neuro §20 atlas used (Homo sapiens, promoter window
TSS-2000..+500, SantaLucia 1998 NN dG37 table) so every γ lands on the SAME scale as the
inherited reads (PRDM12/NTRK1/SCN9A/TRPV1/TRPA1) and the v1.0 Na_V reads. READ-ONLY.
Sequences cached for offline reproduction; NCBI accession+coords pinned per gene.

FIREWALL (binding): γ reads the promoter switch-threshold STRUCTURE only. It is NOT a channel
voltage, ligand affinity, potency, dose, or clinical effect — those are [O] and asserted nowhere.

No tuning: γ = -mean(NN stacking dG) over called dinucleotide steps, pure arithmetic.

Run (network):   python3 fetch_nav_channels.py
Output:          nav_channels_gamma.json   (γ, GC, NCBI accession+coords)
                 nav_promoters.cache.json  (raw promoter strings for offline re-derivation)
"""
import os, json, time, ssl, urllib.request, urllib.parse

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "nav_promoters.cache.json")
OUT   = os.path.join(HERE, "nav_channels_gamma.json")
EU    = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ORG   = "Homo sapiens"
CTX   = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# SantaLucia 1998 unified NN dG37 — identical READ-ONLY table to the inherited pipeline.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

GENES = [
    # carried from v1.0 (already cached): the two missing nociceptor Na_V effectors
    "SCN10A", "SCN11A",                          # Na_V1.8, Na_V1.9
    # --- L1: reduce inward (excitatory) current ---
    "SCN3A",                                     # Na_V1.3 (neuropathic re-expression)
    "CACNA1B", "CACNA1H", "CACNA2D1",            # Ca_V2.2, Ca_V3.2, alpha2delta-1
    "TRPM8",                                     # cold/menthol transducer
    "P2RX3",                                     # P2X3 (ligand-gated)
    "ASIC1", "ASIC3",                            # acid-sensing
    # --- L2: increase outward (K+, inhibitory) current ---
    "KCNQ2", "KCNQ3", "KCNQ5",                   # K_V7.2/7.3/7.5
    # --- L3: remove the sensitising drive ---
    "NGF",                                       # nerve growth factor (TrkA ligand)
    "CALCA", "CALCB", "CALCRL", "RAMP1",         # CGRP ligand + receptor + RAMP
    # --- context / comparators (read for contrast; the logic routes AWAY from reward) ---
    "OPRM1", "OPRK1", "OPRD1", "CNR2",           # mu/kappa/delta opioid + CB2
]

def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "analgesic-threshold-logic"}),
                timeout=60, context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e): time.sleep(4*(k+1)); continue
            if k == tries-1: raise
            time.sleep(2.0*(k+1))

def gene_coords(sym):
    term = urllib.parse.quote(f'{sym}[Gene Name] AND "{ORG}"[Organism]')
    ids = json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")
                     ).get("esearchresult", {}).get("idlist", [])
    for gid in ids[:6]:
        time.sleep(0.34)
        try:
            doc = json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception:
            continue
        if doc.get("name", "").upper() != sym.upper():   # exact official-symbol match only
            continue
        for g in doc.get("genomicinfo", []):
            if not g.get("chraccver", "").startswith("NC_"):
                continue
            a, b = int(g["chrstart"]), int(g["chrstop"])
            strand = "+" if a <= b else "-"
            gs, ge = (a, b) if strand == "+" else (b, a)
            return {"acc": g["chraccver"], "gene_start": gs, "gene_end": ge, "strand": strand}
    return None

def fetch_promoter(c):
    tss = c["gene_start"] if c["strand"] == "+" else c["gene_end"]
    lo, hi = (tss-2000, tss+500) if c["strand"] == "+" else (tss-500, tss+2000)
    u = (f"{EU}/efetch.fcgi?db=nuccore&id={c['acc']}&rettype=fasta&retmode=text"
         f"&seq_start={lo+1}&seq_stop={hi+1}")
    txt = _get(u)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()

def gamma(seq):
    v = [-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    return float(sum(v)/len(v)) if v else float("nan")

def gc_frac(seq):
    n = max(1, len(seq)); return sum(c in "GC" for c in seq)/n

def main():
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    genes, prov = {}, {}
    for sym in GENES:
        if sym in cache:
            seq = cache[sym]["seq"]; coords = cache[sym]["coords"]
        else:
            coords = gene_coords(sym)
            if coords is None:
                raise SystemExit(f"could not resolve coordinates for {sym}")
            time.sleep(0.34)
            seq = fetch_promoter(coords)
            cache[sym] = {"seq": seq, "coords": coords}
        genes[sym] = {"gamma": round(gamma(seq), 4), "gc": round(gc_frac(seq), 4), "len_bp": len(seq)}
        prov[sym]  = {"ncbi_acc": coords["acc"], "gene_start": coords["gene_start"],
                      "gene_end": coords["gene_end"], "strand": coords["strand"],
                      "window": "TSS-2000..+500"}
    json.dump(cache, open(CACHE, "w"), indent=1)
    out = {
        "_provenance": ("gamma = -mean(NN stacking dG), SantaLucia 1998; READ-ONLY human promoters "
                        "(Homo sapiens, TSS-2000..+500) via NCBI eutils. Identical window/NN table as "
                        "neuro sec.20 sensory atlas, so gamma is on the same scale as the inherited reads."),
        "genes": genes, "ncbi": prov,
    }
    json.dump(out, open(OUT, "w"), indent=1)
    for s, v in genes.items():
        print(f"{s:8} gamma={v['gamma']:.4f}  gc={v['gc']:.4f}  len={v['len_bp']}  acc={prov[s]['ncbi_acc']}")
    print(f"wrote {OUT}")

if __name__ == "__main__":
    main()
