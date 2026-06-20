#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_germline_gamma.py  --  GAMETE-MACHINERY master-gene gamma RECEPTION (DNA emergence).

WHY THIS EXISTS
  v0.4.x emerged the four reproductive ORGANS (SOX9/FOXL2/DAZL/WT1) and the HPG/germline RHYTHMS
  (T1..T5), but it never opened the germline cell itself: how a gamete is actually MADE (meiosis),
  whether gametes are identical (recombination), and the two opposite gamete logics (the motile
  sperm vs the waiting egg). Those answers are written in the promoters of the gamete machinery.
  This module RECEIVES that machinery's gamma the SAME way the DNA atlas receives any master gene
  -- it is the "emerge from DNA" step for the gamete program.

PIPELINE (BYTE-IDENTICAL to repro/_gamma/fetch_gamma.py and DNA fetch_morpho_gamma.py)
  gamma = -mean over consecutive dinucleotide steps of the SantaLucia (1998) unified nearest-
          neighbour stacking dG37 (kcal/mol), on the human proximal promoter window TSS-2000..+500
          (GRCh38.p14 / GCF_000001405.40, NCBI exact TSS). GC = (G+C)/ACGT. No initiation / terminal
          / symmetry correction -- a pure mean of stacking terms.
  TSS convention: plus strand -> gene-range begin ; minus strand -> gene-range end.

NO-TUNING / FIDELITY
  Accepted ONLY because it reproduces the vendored anchor SOX9 (gamma=1.4598, GC=0.545) bit-for-bit
  AND reproduces the v0.4.x germline master DAZL (gamma=1.3803, GC=0.479). Having reproduced two
  known anchors with the identical code, the new measurements are measurements, not fits. The panel
  is declared by FUNCTION (the textbook canonical gene per gamete role) BEFORE any gamma is seen;
  no gene is added or dropped to shape a result, and the gamma-vs-function readout is reported as it
  falls (including nulls).

PANEL (declared by role, never by gamma):
  meiosis/recombination (the diversity generator): SPO11, PRDM9, DMC1, MLH1, REC8
  sperm motility:                                  CATSPER1, DNAH1, TEKT1
  oocyte:                                          ZP3, MOS, NLRP5, ZAR1
  germline master (anchor, re-measured):           DAZL

MODES
  (default, OFFLINE)  verify() : recompute gamma from inherited/germline_promoters.cache.json,
                                 cross-check SOX9 + DAZL anchors, confirm germline_gamma.json. No net.
  --fetch (ONLINE)    fetch()  : resolve GRCh38.p14 coordinates (datasets v2alpha), pull each promoter
                                 (E-utilities, strand-aware), rebuild the cache, write germline_gamma.json.
"""
import os, sys, json, math, argparse, hashlib

_HERE      = os.path.dirname(os.path.abspath(__file__))
_INHERITED = os.path.join(_HERE, "..", "..", "inherited")
_CACHE     = os.path.join(_INHERITED, "germline_promoters.cache.json")
_GAMMA     = os.path.join(_INHERITED, "germline_gamma.json")

# SantaLucia (1998) unified NN stacking dG37 (kcal/mol). RC-symmetric -> mean & GC strand-invariant.
NN_DG37 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}

ASSEMBLY = "GCF_000001405.40"   # GRCh38.p14 -- the annotation that reproduces the SOX9/DAZL anchors.

# Gamete-machinery panel. role/module declared up front; coordinates RESOLVED online (not hardcoded),
# then cached. module is metadata only -- it never enters the gamma computation.
PANEL = {
    "SPO11":    dict(module="meiosis",  role="meiotic DSB catalyst (initiates recombination)"),
    "PRDM9":    dict(module="meiosis",  role="recombination-hotspot designator (writes the CO map)"),
    "DMC1":     dict(module="meiosis",  role="meiotic recombinase (homolog strand invasion)"),
    "MLH1":     dict(module="meiosis",  role="crossover maturation / resolution (MutLgamma)"),
    "REC8":     dict(module="meiosis",  role="meiotic cohesin (reductional vs equational release)"),
    "CATSPER1": dict(module="sperm",    role="sperm CatSper Ca2+ channel (hyperactivation switch)"),
    "DNAH1":    dict(module="sperm",    role="axonemal dynein heavy chain (the 9+2 motor)"),
    "TEKT1":    dict(module="sperm",    role="tektin 1 (flagellar structural filament)"),
    "ZP3":      dict(module="oocyte",   role="zona pellucida glycoprotein 3 (sperm receptor)"),
    "MOS":      dict(module="oocyte",   role="c-Mos cytostatic factor (metaphase-II arrest)"),
    "NLRP5":    dict(module="oocyte",   role="maternal-effect (subcortical maternal complex)"),
    "ZAR1":     dict(module="oocyte",   role="zygote arrest 1 (oocyte-to-embryo transition)"),
    "DAZL":     dict(module="germline", role="germline master (gametogenesis); v0.4.x anchor"),
}
# Anchors that must reproduce for the pipeline to be accepted (no-tuning gate).
ANCHORS = {
    "SOX9": dict(gamma=1.4598, gc=0.545),   # vendored organ anchor (cross-paper)
    "DAZL": dict(gamma=1.3803, gc=0.479),   # v0.4.x germline master (in-package)
}


def gamma_gc(seq):
    """gamma = -mean(NN-stacking dG37); GC over ACGT. Returns (gamma, gc, n_acgt, n_steps)."""
    seq = seq.upper()
    acgt = [c for c in seq if c in "ACGT"]
    n = len(acgt)
    gc = (acgt.count("G") + acgt.count("C")) / n
    steps = [seq[i:i + 2] for i in range(len(seq) - 1)]
    dg = [NN_DG37[d] for d in steps if d in NN_DG37]
    return -sum(dg) / len(dg), gc, n, len(dg)


def window_for(orientation, begin, end):
    """plus: TSS=begin -> [TSS-2000, TSS+500]; minus: TSS=end -> [TSS-500, TSS+2000]."""
    if orientation == "plus":
        tss = begin; return tss, tss - 2000, tss + 500, 1
    tss = end;     return tss, tss - 500,  tss + 2000, 2


# ----------------------------------------------------------------------------- ONLINE helpers
def _resolve_coords(symbol, timeout=45, tries=4):
    """GRCh38.p14 (ASSEMBLY) gene range for a HGNC symbol via NCBI datasets v2alpha."""
    import urllib.request, time
    url = ("https://api.ncbi.nlm.nih.gov/datasets/v2alpha/gene/symbol/%s/taxon/9606" % symbol)
    last = None
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                d = json.load(r)
            g = d["reports"][0]["gene"]
            for ann in g.get("annotations", []):
                if ann.get("assembly_accession") == ASSEMBLY:
                    loc = ann["genomic_locations"][0]
                    rng = loc["genomic_range"]
                    return dict(gene_id=g["gene_id"], accession=loc["genomic_accession_version"],
                                orientation=rng["orientation"], begin=int(rng["begin"]), end=int(rng["end"]))
            last = "assembly %s not in annotations" % ASSEMBLY
        except Exception as e:
            last = repr(e)
        time.sleep(2.0 * (a + 1))
    raise RuntimeError("coord resolve failed for %s: %s" % (symbol, last))


def _efetch(acc, start, stop, strand, timeout=50, tries=5):
    import urllib.request, urllib.parse, time
    q = {"db": "nuccore", "id": acc, "seq_start": str(start), "seq_stop": str(stop),
         "strand": str(strand), "rettype": "fasta", "retmode": "text"}
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(q)
    last = None
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                txt = r.read().decode()
            seq = "".join(l.strip() for l in txt.splitlines() if not l.startswith(">"))
            if len(seq) >= 2000:
                return seq.upper()
            last = "short read %d" % len(seq)
        except Exception as e:
            last = repr(e)
        time.sleep(2.5 * (a + 1))
    raise RuntimeError("efetch failed for %s: %s" % (acc, last))


def fetch():
    """ONLINE: resolve coords, pull promoters, rebuild cache, write germline_gamma.json."""
    import time
    order = ["SOX9"] + list(PANEL.keys())          # SOX9 first as the cross-paper anchor
    coords = {"SOX9": dict(gene_id="6662", accession="NC_000017.11",
                           orientation="plus", begin=72121020, end=72126416)}
    cache_genes, rows = {}, {}
    for sym in order:
        meta = coords.get(sym) or _resolve_coords(sym)
        coords[sym] = meta
        tss, start, stop, strand = window_for(meta["orientation"], meta["begin"], meta["end"])
        seq = _efetch(meta["accession"], start, stop, strand)
        g, gc, n, nsteps = gamma_gc(seq)
        module = "anchor" if sym == "SOX9" else PANEL[sym]["module"]
        role   = "vendored organ anchor (SOX9)" if sym == "SOX9" else PANEL[sym]["role"]
        cache_genes[sym] = dict(
            module=module, role=role, gene_id=meta["gene_id"], accession=meta["accession"],
            strand=("+" if strand == 1 else "-"), tss=tss, window="TSS-2000..+500",
            win_start=start, win_stop=stop, length_bp=len(seq), gc=round(gc, 4),
            gamma=round(g, 4), seq_sha256=hashlib.sha256(seq.encode()).hexdigest(),
            promoter_seq=seq)
        rows[sym] = (round(g, 4), round(gc, 4))
        print("  %-9s %-9s %s %s TSS=%-10d gamma=%.4f GC=%.4f  %s"
              % (sym, module, meta["accession"], ("+" if strand == 1 else "-"), tss, g, gc, role))
        time.sleep(0.34)                            # be polite to NCBI
    # no-tuning fidelity gate -- both anchors must reproduce or we refuse to persist
    for a, exp in ANCHORS.items():
        gg, gcc = rows[a]
        assert abs(gg - exp["gamma"]) < 1e-4 and abs(gcc - exp["gc"]) < 1e-3, \
            "anchor %s not reproduced (%.4f/%.4f vs %.4f/%.4f) -- pipeline drift, refusing to write" \
            % (a, gg, gcc, exp["gamma"], exp["gc"])
    cache = {
        "_what": "Cached human proximal-promoter sequences (GRCh38.p14, NCBI exact TSS, TSS-2000..+500) "
                 "for the GAMETE-MACHINERY panel. Enables OFFLINE bit-for-bit reproduction of "
                 "gamma = -mean(NN-stacking dG37, SantaLucia 1998). Measured input, never fitted.",
        "_assembly": "GRCh38.p14 (%s)" % ASSEMBLY,
        "_method": "gamma = -mean over consecutive dinucleotide steps of SantaLucia (1998) unified NN "
                   "stacking dG37; GC = (G+C)/ACGT. Pipeline identical to repro/_gamma/fetch_gamma.py "
                   "and DNA fetch_morpho_gamma.py; accepted only because it reproduces SOX9 (1.4598/0.545) "
                   "and DAZL (1.3803/0.479).",
        "_tss_convention": "plus strand -> gene-range begin; minus strand -> gene-range end.",
        "_panel_declaration": "Panel declared by gamete-role BEFORE gamma was seen; no gene added/dropped "
                              "to shape a result; gamma-vs-module readout reported as it falls.",
        "genes": cache_genes,
    }
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    _write_gamma_json(cache_genes)
    print("  cache + germline_gamma.json written (%d genes)." % len(cache_genes))
    return rows


def _write_gamma_json(cache_genes):
    genes = {}
    for sym, rec in cache_genes.items():
        if sym == "SOX9":
            continue
        genes[sym] = {
            "gamma": rec["gamma"], "gc": rec["gc"], "module": rec["module"], "role": rec["role"],
            "src": "%s %s TSS-2000..+500" % (rec["accession"], rec["strand"]),
            "_source": "fetch_germline_gamma.py reception (DNA NN-dG37 pipeline; measured, never fitted)",
        }
    asc = sorted(genes.keys(), key=lambda s: genes[s]["gamma"])
    out = {
        "_atlas": "VP gamete-machinery master-gene gamma (measured promoter thermodynamics).",
        "_provenance": "gamma = -mean(NN stacking dG37, SantaLucia 1998) over human proximal promoter "
                       "TSS-2000..+500 (GRCh38.p14). IDENTICAL pipeline to organ gamma; never fitted. "
                       "Validated against SOX9 (1.4598) and DAZL (1.3803).",
        "_panel_declaration": "Declared by gamete role before gamma was seen (see fetch_germline_gamma.py PANEL).",
        "_order_gamma_asc": asc,
        "genes": genes,
    }
    json.dump(out, open(_GAMMA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------------- OFFLINE (default)
def verify():
    if not os.path.exists(_CACHE):
        return {"ok": False, "reason": "cache absent -- run with --fetch once (network)"}
    cache = json.load(open(_CACHE, encoding="utf-8"))["genes"]
    gj = json.load(open(_GAMMA, encoding="utf-8"))["genes"] if os.path.exists(_GAMMA) else {}
    out = {"genes": {}, "anchors_ok": {}, "all_match_gamma_json": True, "all_seq_sha_ok": True}
    for sym, rec in sorted(cache.items()):
        g, gc, n, nsteps = gamma_gc(rec["promoter_seq"])
        seq_ok = hashlib.sha256(rec["promoter_seq"].encode()).hexdigest() == rec["seq_sha256"]
        match_cache = (round(g, 4), round(gc, 4)) == (round(rec["gamma"], 4), round(rec["gc"], 4))
        match_json = (sym not in gj) or abs(round(g, 4) - round(gj[sym]["gamma"], 4)) < 1e-4
        out["genes"][sym] = dict(module=rec.get("module"), gamma=round(g, 4), gc=round(gc, 4),
                                 length_bp=rec["length_bp"], recompute_matches_cache=match_cache,
                                 matches_gamma_json=match_json, seq_sha_ok=seq_ok)
        out["all_seq_sha_ok"] &= seq_ok
        if not match_json:
            out["all_match_gamma_json"] = False
    for a, exp in ANCHORS.items():
        s = out["genes"].get(a, {})
        out["anchors_ok"][a] = bool(abs(s.get("gamma", 0) - exp["gamma"]) < 1e-4
                                    and abs(s.get("gc", 0) - exp["gc"]) < 1e-3)
    out["ok"] = bool(all(out["anchors_ok"].values()) and out["all_match_gamma_json"]
                     and out["all_seq_sha_ok"]
                     and all(g["recompute_matches_cache"] for g in out["genes"].values()))
    return out


def panel_gamma():
    """Convenience: {symbol: {gamma, gc, module, role}} from the cache (offline, deterministic)."""
    cache = json.load(open(_CACHE, encoding="utf-8"))["genes"]
    return {s: dict(gamma=round(r["gamma"], 4), gc=round(r["gc"], 4),
                    module=r.get("module"), role=r.get("role"))
            for s, r in cache.items() if s != "SOX9"}


def main():
    ap = argparse.ArgumentParser(description="Gamete-machinery master-gene gamma reception.")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: resolve coords + fetch + rebuild cache")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    sys.exit(0 if v["ok"] else 1)


if __name__ == "__main__":
    main()
