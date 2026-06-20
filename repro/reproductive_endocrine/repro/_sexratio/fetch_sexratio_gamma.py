#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_sexratio_gamma.py  --  SEX-DETERMINATION master-gene gamma RECEPTION (DNA emergence).

WHY THIS EXISTS
  v0.6.x emerged the four reproductive ORGANS (SOX9/FOXL2/DAZL/WT1), the HPG/germline RHYTHMS
  (T1..T5), the gamete itself (G1..G6) and the embryo (E1..E6). None of those opened the question
  the user now poses: which SEX is built, and why a gene can make one sex (or one allele) PREDOMINATE.
  Mammalian sex is one bistable switch -- a testis-determining axis (SRY -> SOX9 -> DMRT1) mutually
  antagonistic with an ovary-determining axis (FOXL2 / RSPO1 / WNT4). The depth of each basin is
  written in the promoters of those master genes. This module RECEIVES that axis's gamma the SAME way
  the DNA atlas receives any master gene -- it is the "emerge from DNA" step for sex determination.

PIPELINE (BYTE-IDENTICAL to repro/_gamma/fetch_gamma.py, repro/_germline/fetch_germline_gamma.py and
          DNA fetch_morpho_gamma.py)
  gamma = -mean over consecutive dinucleotide steps of the SantaLucia (1998) unified nearest-neighbour
          stacking dG37 (kcal/mol), on the human proximal promoter window TSS-2000..+500
          (GRCh38.p14 / GCF_000001405.40, NCBI exact TSS). GC = (G+C)/ACGT. No initiation / terminal
          / symmetry correction -- a pure mean of stacking terms.
  TSS convention: plus strand -> gene-range begin ; minus strand -> gene-range end.

NO-TUNING / FIDELITY
  Accepted ONLY because it reproduces TWO vendored in-package anchors bit-for-bit:
    SOX9  (gamma=1.4598, GC=0.545)  -- cross-paper organ anchor (testis determinant)
    FOXL2 (gamma=1.4829, GC=0.5754) -- v0.3.0 ovary determinant (the opposite basin)
  Having reproduced the two anchors with the identical code, the four new measurements (SRY, DMRT1,
  RSPO1, WNT4) are measurements, not fits. The panel is declared by FUNCTION (testis-axis vs ovary-axis)
  BEFORE any gamma is seen; no gene is added or dropped to shape a result, and the gamma-vs-function
  readout is reported as it falls (including nulls -- SRY's AT-rich promoter is a known low-gamma outlier
  and is kept).

PANEL (declared by axis, never by gamma):
  testis-determining axis:  SRY (Y master switch), SOX9 (testis determinant; anchor), DMRT1 (testis
                            maintenance, FOXL2 antagonist)
  ovary-determining axis:   FOXL2 (ovary determinant; anchor), RSPO1 (beta-catenin/ovary), WNT4 (ovary,
                            anti-testis)

MODES
  (default, OFFLINE)  verify() : recompute gamma from inherited/sexdet_promoters.cache.json, cross-check
                                 SOX9 + FOXL2 anchors, confirm sexdet_gamma.json. No network.
  --fetch (ONLINE)    fetch()  : resolve GRCh38.p14 coordinates (datasets v2alpha), pull each promoter
                                 (E-utilities, strand-aware), rebuild the cache, write sexdet_gamma.json.
"""
import os, sys, json, math, argparse, hashlib

_HERE      = os.path.dirname(os.path.abspath(__file__))
_INHERITED = os.path.join(_HERE, "..", "..", "inherited")
_CACHE     = os.path.join(_INHERITED, "sexdet_promoters.cache.json")
_GAMMA     = os.path.join(_INHERITED, "sexdet_gamma.json")

# SantaLucia (1998) unified NN stacking dG37 (kcal/mol). RC-symmetric -> mean & GC strand-invariant.
NN_DG37 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}

ASSEMBLY = "GCF_000001405.40"   # GRCh38.p14 -- the annotation that reproduces the SOX9/FOXL2 anchors.

# Sex-determination panel. axis/role declared up front; coordinates RESOLVED online (not hardcoded),
# then cached. axis is metadata only -- it never enters the gamma computation.
PANEL = {
    "SRY":   dict(axis="testis", role="Y-linked testis-determining master switch (sets SOX9 ON)"),
    "SOX9":  dict(axis="testis", role="testis determinant (Sertoli fate); cross-paper anchor"),
    "DMRT1": dict(axis="testis", role="testis maintenance; represses FOXL2 (the antagonist)"),
    "FOXL2": dict(axis="ovary",  role="ovary determinant (granulosa fate); v0.3.0 anchor"),
    "RSPO1": dict(axis="ovary",  role="R-spondin1; beta-catenin/ovary-promoting"),
    "WNT4":  dict(axis="ovary",  role="WNT4; ovary-promoting, anti-testis"),
}
# Anchors that must reproduce for the pipeline to be accepted (no-tuning gate).
ANCHORS = {
    "SOX9":  dict(gamma=1.4598, gc=0.545),    # vendored organ anchor (cross-paper, testis)
    "FOXL2": dict(gamma=1.4829, gc=0.5754),   # v0.3.0 ovary determinant (in-package, the opposite basin)
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
    """ONLINE: resolve coords, fetch promoters, rebuild cache, write sexdet_gamma.json (anchor-gated)."""
    cache_genes = {}
    rows = {}
    for sym in sorted(PANEL):
        c = _resolve_coords(sym)
        tss, start, stop, strand = window_for(c["orientation"], c["begin"], c["end"])
        seq = _efetch(c["accession"], start, stop, strand)
        g, gc, n, nsteps = gamma_gc(seq)
        cache_genes[sym] = dict(
            axis=PANEL[sym]["axis"], role=PANEL[sym]["role"], gene_id=c["gene_id"],
            accession=c["accession"], strand=("+" if strand == 1 else "-"), tss=tss,
            window="TSS-2000..+500", win_start=start, win_stop=stop, length_bp=len(seq),
            gc=round(gc, 4), gamma=round(g, 4), seq_sha256=hashlib.sha256(seq.encode()).hexdigest(),
            promoter_seq=seq)
        rows[sym] = (round(g, 4), round(gc, 4))
        print("  fetched %-6s [%-6s] %s %s TSS=%d  gamma=%.4f  GC=%.4f"
              % (sym, PANEL[sym]["axis"], c["accession"], ("+" if strand == 1 else "-"), tss, g, gc))
    # fidelity cross-check on BOTH anchors before persisting (no-tuning gate)
    for a, ref in ANCHORS.items():
        ga, gca = rows[a]
        assert abs(ga - ref["gamma"]) < 1e-4 and abs(gca - ref["gc"]) < 1e-3, \
            "%s anchor not reproduced (%.4f/%.4f) -- pipeline drift, refusing to write" % (a, ga, gca)
    cache = {
        "_what": "Cached human proximal-promoter sequences (GRCh38.p14, NCBI exact TSS, window "
                 "TSS-2000..+500) for the SEX-DETERMINATION master genes (testis axis SRY/SOX9/DMRT1, "
                 "ovary axis FOXL2/RSPO1/WNT4). Enables OFFLINE bit-for-bit reproduction of gamma = "
                 "-mean(NN-stacking dG37, SantaLucia 1998). Measured input, never fitted.",
        "_assembly": "GRCh38.p14 (GCF_000001405.40)",
        "_method": "gamma = -mean over consecutive dinucleotide steps of SantaLucia (1998) unified NN "
                   "stacking dG37 (kcal/mol); GC = (G+C)/ACGT. Pipeline identical to DNA "
                   "fetch_morpho_gamma.py; validated by reproducing SOX9 (1.4598/0.545) AND FOXL2 "
                   "(1.4829/0.5754).",
        "_tss_convention": "plus strand -> gene-range begin; minus strand -> gene-range end "
                           "(NCBI datasets v2alpha gene/symbol GRCh38 genomic_locations). Validated on SOX9.",
        "genes": cache_genes,
    }
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    _write_gamma_json(cache_genes)
    print("  cache + sexdet_gamma.json updated.")
    return rows


def _write_gamma_json(cache_genes):
    d = {
        "_what": "Measured sex-determination master-gene gamma (testis axis vs ovary axis), received via "
                 "repro/_sexratio/fetch_sexratio_gamma.py using the DNA fetch_morpho_gamma pipeline. "
                 "Measured input, never fitted; offline bit-for-bit from sexdet_promoters.cache.json.",
        "_source": "fetch_sexratio_gamma.py reception (anchors SOX9 1.4598/0.545 + FOXL2 1.4829/0.5754)",
        "genes": {s: {"gamma": r["gamma"], "gc": r["gc"], "axis": r["axis"],
                      "src": "%s %s TSS-2000..+500" % (r["accession"], r["strand"])}
                  for s, r in cache_genes.items()},
    }
    json.dump(d, open(_GAMMA, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


# ----------------------------------------------------------------------------- OFFLINE (default)
def panel_gamma():
    """{symbol: {gamma, gc, axis, role}} from the cache (offline, deterministic)."""
    cache = json.load(open(_CACHE, encoding="utf-8"))["genes"]
    out = {}
    for s, rec in cache.items():
        g, gc, n, nsteps = gamma_gc(rec["promoter_seq"])
        out[s] = dict(gamma=round(g, 4), gc=round(gc, 4), axis=rec["axis"], role=rec["role"])
    return out


def verify():
    """OFFLINE: recompute gamma from cache, cross-check SOX9+FOXL2, confirm sexdet_gamma.json."""
    if not os.path.exists(_CACHE):
        return {"ok": False, "reason": "cache absent -- run with --fetch once (network)"}
    cache = json.load(open(_CACHE, encoding="utf-8"))["genes"]
    gj = json.load(open(_GAMMA, encoding="utf-8"))["genes"] if os.path.exists(_GAMMA) else {}
    out = {"genes": {}, "anchors_ok": None, "all_match_gamma_json": True, "all_seq_sha_ok": True}
    for sym, rec in sorted(cache.items()):
        g, gc, n, nsteps = gamma_gc(rec["promoter_seq"])
        seq_ok = hashlib.sha256(rec["promoter_seq"].encode()).hexdigest() == rec["seq_sha256"]
        recomputed = (round(g, 4), round(gc, 4))
        cached = (round(rec["gamma"], 4), round(rec["gc"], 4))
        match_cache = recomputed == cached
        match_json = (sym not in gj) or abs(round(g, 4) - round(gj[sym]["gamma"], 4)) < 1e-4
        out["genes"][sym] = dict(axis=rec["axis"], gamma=round(g, 4), gc=round(gc, 4),
                                 length_bp=rec["length_bp"], recompute_matches_cache=match_cache,
                                 matches_gamma_json=match_json, seq_sha_ok=seq_ok)
        out["all_seq_sha_ok"] &= seq_ok
        if not match_json:
            out["all_match_gamma_json"] = False
    anchors_ok = True
    for a, ref in ANCHORS.items():
        s = out["genes"].get(a, {})
        anchors_ok &= bool(abs(s.get("gamma", 0) - ref["gamma"]) < 1e-4
                           and abs(s.get("gc", 0) - ref["gc"]) < 1e-3)
    out["anchors_ok"] = bool(anchors_ok)
    out["ok"] = bool(anchors_ok and out["all_match_gamma_json"] and out["all_seq_sha_ok"]
                     and all(g["recompute_matches_cache"] for g in out["genes"].values()))
    return out


def main():
    ap = argparse.ArgumentParser(description="Sex-determination master-gene gamma reception.")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: fetch from NCBI + rebuild cache + write gamma")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    if not v["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
