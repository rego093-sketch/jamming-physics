#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ncbi_gene_promoter.py  --  pull REAL disease-gene DNA from NCBI and read its
                           promoter switch-threshold structure (gamma).

This is the DATA PATH of the disease-emergence pivot. Given a gene SYMBOL (the
causal gene of a monogenic disease) it:

  1. resolves the official human (or any-organism) gene to a RefSeq genomic
     coordinate via NCBI E-utilities (esearch -> esummary, db=gene),
  2. fetches the PROMOTER window TSS-2000..+500 (strand-oriented) and, on request,
     the GENE BODY, via efetch (db=nuccore, rettype=fasta),
  3. computes  gamma = -mean(NN stacking dG, SantaLucia 1998)  -- the R19 promoter
     switch-threshold scale -- on the IDENTICAL window/NN table the whole VP DNA
     engine uses, so every disease gene lands on the SAME gamma scale,
  4. CACHES the raw sequence + pinned accession/coords so the analysis re-derives
     OFFLINE, bit-for-bit (VP-SPEC C1: the reproduction path never leaves the kit).

If a gene cannot be resolved (no official-symbol match, no NC_ assembly), the
fetch returns None and the caller SUSPENDS that disease -- the author's rule:
"DNA 분석이 어려우면 그 질병은 분석을 보류하라 (없으니 못한다)".

FIREWALL (binding, inherited from the analgesic threshold logic):
  gamma reads the promoter switch-threshold STRUCTURE only. It is NOT a channel
  voltage, ligand affinity, potency, dose, expression level, or clinical effect.
  Those are runtime / Layer-2 quantities -- [O], asserted nowhere.

No tuning: gamma is pure arithmetic over called dinucleotide steps.

CLI:   python3 ncbi_gene_promoter.py FGFR3 CFTR PAH        # fetch + cache + print
       python3 ncbi_gene_promoter.py --offline FGFR3       # cache-only (no network)
"""
import os, sys, json, time, ssl, urllib.request, urllib.parse

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache", "gene_promoters.cache.json")
EU    = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CTX   = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# SantaLucia 1998 unified NN dG37 (kcal/mol) -- the locked READ-ONLY table the
# whole VP DNA engine shares. Changing any value defines a new engine version.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

PROMOTER_WINDOW = "TSS-2000..+500"   # identical to the neuro/analgesic atlas window


# ----------------------------- network primitives ----------------------------
def _get(u, tries=6):
    for k in range(tries):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(u, headers={"User-Agent": "vp-disease-emergence"}),
                timeout=60, context=CTX).read().decode()
        except Exception as e:
            if "429" in str(e) or "Too Many" in str(e): time.sleep(4*(k+1)); continue
            if k == tries-1: raise
            time.sleep(2.0*(k+1))


def gene_coords(sym, organism="Homo sapiens"):
    """Resolve an OFFICIAL gene symbol to a RefSeq genomic coordinate (NC_ only).
       Returns {acc, gene_start, gene_end, strand, gene_id, description} or None."""
    term = urllib.parse.quote(f'{sym}[Gene Name] AND "{organism}"[Organism]')
    ids = json.loads(_get(f"{EU}/esearch.fcgi?db=gene&term={term}&retmode=json")
                     ).get("esearchresult", {}).get("idlist", [])
    for gid in ids[:6]:
        time.sleep(0.34)
        try:
            doc = json.loads(_get(f"{EU}/esummary.fcgi?db=gene&id={gid}&retmode=json"))["result"][gid]
        except Exception:
            continue
        if doc.get("name", "").upper() != sym.upper():      # exact official-symbol match only
            continue
        for g in doc.get("genomicinfo", []):
            if not g.get("chraccver", "").startswith("NC_"):
                continue
            a, b = int(g["chrstart"]), int(g["chrstop"])
            strand = "+" if a <= b else "-"
            gs, ge = (a, b) if strand == "+" else (b, a)
            return {"acc": g["chraccver"], "gene_start": gs, "gene_end": ge,
                    "strand": strand, "gene_id": gid,
                    "description": doc.get("description", "")}
    return None


def _fetch_window(acc, lo, hi):
    u = (f"{EU}/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta&retmode=text"
         f"&seq_start={lo+1}&seq_stop={hi+1}")
    txt = _get(u)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()


def fetch_promoter(c):
    tss = c["gene_start"] if c["strand"] == "+" else c["gene_end"]
    lo, hi = (tss-2000, tss+500) if c["strand"] == "+" else (tss-500, tss+2000)
    return _fetch_window(c["acc"], lo, hi)


# ----------------------------- sequence reads --------------------------------
def gamma(seq):
    """R19 promoter switch-threshold scale = -mean(NN stacking dG). Strand-symmetric."""
    v = [-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    return float(sum(v)/len(v)) if v else float("nan")

def gc_frac(seq):
    c = [x for x in seq if x in "ACGT"]
    return sum(1 for x in c if x in "GC")/len(c) if c else float("nan")

def cpg_density(seq):
    n = sum(1 for i in range(len(seq)-1) if seq[i:i+2] == "CG")
    return n/max(1, len(seq)-1)


# ----------------------------- the public API --------------------------------
def read_gene(sym, organism="Homo sapiens", offline=False):
    """Return the full sequence-derived read for one gene, with provenance, or None.
       Uses the cache first; only touches the network if the gene is uncached and
       offline=False. Caching makes every downstream analysis reproducible offline."""
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    key = f"{organism}::{sym.upper()}"
    if key in cache:
        seq, coords = cache[key]["seq"], cache[key]["coords"]
    else:
        if offline:
            return None                                # not cached and no network allowed
        coords = gene_coords(sym, organism)
        if coords is None:
            return None                                # SUSPEND: cannot resolve DNA
        time.sleep(0.34)
        seq = fetch_promoter(coords)
        cache[key] = {"seq": seq, "coords": coords}
        json.dump(cache, open(CACHE, "w"), indent=1)
    return {
        "gene": sym.upper(), "organism": organism,
        "gamma": round(gamma(seq), 4), "gc": round(gc_frac(seq), 4),
        "cpg_density": round(cpg_density(seq), 5), "promoter_len_bp": len(seq),
        "ncbi": {"acc": coords["acc"], "gene_start": coords["gene_start"],
                 "gene_end": coords["gene_end"], "strand": coords["strand"],
                 "window": PROMOTER_WINDOW, "description": coords.get("description", "")},
        "firewall": ("gamma reads the promoter switch-threshold STRUCTURE only; not voltage/"
                     "affinity/potency/dose/expression/effect (those are [O])."),
    }


def read_panel(symbols, organism="Homo sapiens", offline=False):
    """Read a panel of genes; returns {resolved:{...}, suspended:[...]}.
       'suspended' lists genes whose DNA could not be resolved (the author's
       'no DNA -> hold the analysis' rule, made explicit and auditable)."""
    resolved, suspended = {}, []
    for s in symbols:
        r = read_gene(s, organism, offline)
        if r is None:
            suspended.append(s)
        else:
            resolved[s.upper()] = r
    return {"resolved": resolved, "suspended": suspended}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    if not args:
        args = ["FGFR3", "CFTR", "PAH"]
    panel = read_panel(args, offline=offline)
    print(f"{'gene':8} {'gamma':>7} {'gc':>6} {'cpg':>7} {'len':>5}  accession        strand")
    for s, r in panel["resolved"].items():
        n = r["ncbi"]
        print(f"{s:8} {r['gamma']:7.4f} {r['gc']:6.4f} {r['cpg_density']:7.5f} "
              f"{r['promoter_len_bp']:>5}  {n['acc']:15} {n['strand']}")
    if panel["suspended"]:
        print("SUSPENDED (no resolvable DNA):", ", ".join(panel["suspended"]))
