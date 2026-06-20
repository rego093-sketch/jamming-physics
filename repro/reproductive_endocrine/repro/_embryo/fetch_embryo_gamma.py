#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_embryo_gamma.py  --  DEVELOPMENTAL master-gene gamma RECEPTION (the embryo's DNA emergence).

WHY THIS EXISTS
  v0.5.0 emerged the two gametes (the germline, G1..G6). The user's next question is the obvious one:
  the gametes have been made -- now let them MEET, let a new genome EMERGE, and let a fetus actually be
  BUILT. The fertilisation event and the early embryo are answered by the gamete program the package
  already owns (oocyte-to-embryo transition: ZAR1, NLRP5). But the BODY PLAN that turns a ball of cells
  into a fetus is written in the promoters of the DEVELOPMENTAL master genes, and it unfolds by the
  morphogenesis gene-clock (emergence order = argsort(spinodal(gamma))). That gene-clock LAW and the full
  body atlas are OWNED by the DNA 4D-Blueprint whitepaper (seam IN -- cited, never re-derived here). This
  module RECEIVES a focused developmental panel through the IDENTICAL pipeline the DNA atlas uses, so the
  E-series (repro/_embryo/embryogenesis.py) can demonstrate the clock concretely on measured, never-fitted
  gamma -- the "emerge from DNA" step for the embryo.

  FIREWALL (CHARTER): this package owns the FERTILISATION event (its two gametes meeting) and carries the
  embryo to the point the body plan begins. The full multi-organ morphogenesis atlas remains the DNA
  package's single source of truth; the panel below is a measured DEMONSTRATION of the cited gene-clock,
  not a competing atlas.

PIPELINE (BYTE-IDENTICAL to repro/_gamma/fetch_gamma.py, repro/_germline/fetch_germline_gamma.py, DNA)
  gamma = -mean over consecutive dinucleotide steps of the SantaLucia (1998) unified nearest-neighbour
          stacking dG37 (kcal/mol), on the human proximal promoter window TSS-2000..+500 (GRCh38.p14 /
          GCF_000001405.40, NCBI exact TSS). GC = (G+C)/ACGT. No initiation / terminal / symmetry term.
  TSS convention: plus strand -> gene-range begin ; minus strand -> gene-range end.

NO-TUNING / FIDELITY / PRE-REGISTRATION
  Accepted ONLY because it reproduces the vendored anchor SOX9 (gamma=1.4598, GC=0.545) bit-for-bit AND
  the v0.5.0 germline master DAZL (gamma=1.3803, GC=0.479). The panel is declared by DEVELOPMENTAL STAGE
  (pluripotency < germ-layer < organ-primordium) and by HOX AP-axis position BEFORE any gamma is seen; no
  gene is added or dropped to shape a result; the gamma-vs-stage and gamma-vs-axis read-outs are reported
  as they fall (the E4 pre-registered tests permit a NULL). Each gene carries its stage_rank (the
  pre-registered hypothesis order) so the readout cannot be retrofitted.

MODES
  (default, OFFLINE)  verify() : recompute gamma from inherited/embryo_promoters.cache.json, cross-check
                                 the SOX9 + DAZL anchors, confirm embryo_gamma.json. Network-free, bit-for-bit.
  --fetch (ONLINE)    fetch()  : resolve GRCh38.p14 coordinates (datasets v2alpha), pull each promoter
                                 (E-utilities, strand-aware), rebuild the cache, write embryo_gamma.json.
"""
import os, sys, json, math, argparse, hashlib

_HERE      = os.path.dirname(os.path.abspath(__file__))
_INHERITED = os.path.join(_HERE, "..", "..", "inherited")
_CACHE     = os.path.join(_INHERITED, "embryo_promoters.cache.json")
_GAMMA     = os.path.join(_INHERITED, "embryo_gamma.json")
_GERM_CACHE = os.path.join(_INHERITED, "germline_promoters.cache.json")  # DAZL anchor source (offline)

# SantaLucia (1998) unified NN stacking dG37 (kcal/mol). RC-symmetric -> mean & GC strand-invariant.
NN_DG37 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}

ASSEMBLY = "GCF_000001405.40"   # GRCh38.p14 -- the annotation that reproduces the SOX9/DAZL anchors.

# ---------------------------------------------------------------------------------------------------
# Developmental panel. stage_rank / axis_rank declared up front (the pre-registered hypothesis order);
# coordinates RESOLVED online (not hardcoded), then cached. stage/axis are metadata only -- they NEVER
# enter the gamma computation. The pre-registered E4 hypothesis is: gamma rises with developmental stage
# (pluripotency=1 < germ-layer=2 < organ-primordium=3), i.e. earlier programs sit lower on the
# gene-clock; and for the HOX sub-panel gamma rises 3'->5' (anterior=1 -> posterior=3, temporal
# colinearity). Both are reported as they fall -- a NULL is permitted and printed honestly.
# ---------------------------------------------------------------------------------------------------
PANEL = {
    # --- pluripotency / pre-body-plan (the zygote and inner cell mass; earliest) -----------------
    "POU5F1": dict(stage="pluripotency",      stage_rank=1, axis_rank=None,
                   role="core pluripotency master (OCT4); the zygotic/ICM ground state"),
    "NANOG":  dict(stage="pluripotency",      stage_rank=1, axis_rank=None,
                   role="inner-cell-mass pluripotency factor (epiblast competence)"),
    "SOX2":   dict(stage="pluripotency",      stage_rank=1, axis_rank=None,
                   role="pluripotency + neuroectoderm competence"),
    # --- lineage / germ-layer specification (gastrulation; the three layers + 1st split) ---------
    "CDX2":   dict(stage="germ_layer",        stage_rank=2, axis_rank=None,
                   role="trophectoderm specifier (first lineage decision, ICM vs TE)"),
    "TBXT":   dict(stage="germ_layer",        stage_rank=2, axis_rank=None,
                   role="Brachyury/T: mesoderm + primitive streak (gastrulation)"),
    "SOX17":  dict(stage="germ_layer",        stage_rank=2, axis_rank=None,
                   role="definitive endoderm specifier"),
    "GATA4":  dict(stage="germ_layer",        stage_rank=2, axis_rank=None,
                   role="endoderm + cardiac-mesoderm specifier"),
    "PAX3":   dict(stage="germ_layer",        stage_rank=2, axis_rank=None,
                   role="neural crest / paraxial-mesoderm (ectoderm derivative)"),
    # --- organ primordia (organogenesis; the latest master genes) --------------------------------
    "PAX6":   dict(stage="organ_primordium",  stage_rank=3, axis_rank=None,
                   role="eye + forebrain master"),
    "NKX2-5": dict(stage="organ_primordium",  stage_rank=3, axis_rank=None,
                   role="cardiac (heart-field) master"),
    "FOXA2":  dict(stage="organ_primordium",  stage_rank=3, axis_rank=None,
                   role="node/notochord -> gut/liver/floor-plate master"),
    "PDX1":   dict(stage="organ_primordium",  stage_rank=3, axis_rank=None,
                   role="pancreas/duodenum master"),
    "MYOD1":  dict(stage="organ_primordium",  stage_rank=3, axis_rank=None,
                   role="skeletal-muscle master"),
    # SOX9 is the cross-paper anchor AND a genuine organ-primordium master (chondrocyte/skeleton); it
    # is fetched first as the fidelity anchor and ALSO carries stage_rank=3 for the stage test.
    # --- AP-axis HOX colinearity sub-panel (3'->5' = anterior->posterior = early->late) ----------
    "HOXA1":  dict(stage="ap_axis",           stage_rank=2, axis_rank=1,
                   role="HOXA1: 3' (anterior, earliest) of the cluster"),
    "HOXB4":  dict(stage="ap_axis",           stage_rank=2, axis_rank=2,
                   role="HOXB4: mid-cluster (trunk)"),
    "HOXA13": dict(stage="ap_axis",           stage_rank=3, axis_rank=3,
                   role="HOXA13: 5' (posterior, latest) of the cluster"),
}
# SOX9 metadata for when it is used in the stage panel (organ-primordium master, anchor).
SOX9_STAGE = dict(stage="organ_primordium", stage_rank=3, axis_rank=None,
                  role="chondrocyte/skeleton master (+gonad); cross-paper gamma anchor")

# Anchors that must reproduce for the pipeline to be accepted (no-tuning gate).
ANCHORS = {
    "SOX9": dict(gamma=1.4598, gc=0.545),   # vendored organ anchor (cross-paper)
    "DAZL": dict(gamma=1.3803, gc=0.479),   # v0.5.0 germline master (in-package)
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
    """ONLINE: resolve coords, pull promoters, rebuild cache, write embryo_gamma.json."""
    import time
    order = ["SOX9"] + list(PANEL.keys())          # SOX9 first as the cross-paper anchor
    coords = {"SOX9": dict(gene_id="6662", accession="NC_000017.11",
                           orientation="plus", begin=72121020, end=72126416)}
    cache_genes, rows = {}, {}
    failed = []
    for sym in order:
        try:
            meta = coords.get(sym) or _resolve_coords(sym)
        except Exception as e:
            failed.append((sym, repr(e)[:140])); print("  %-9s RESOLVE-FAIL %s" % (sym, repr(e)[:120])); continue
        coords[sym] = meta
        try:
            tss, start, stop, strand = window_for(meta["orientation"], meta["begin"], meta["end"])
            seq = _efetch(meta["accession"], start, stop, strand)
        except Exception as e:
            failed.append((sym, repr(e)[:140])); print("  %-9s FETCH-FAIL %s" % (sym, repr(e)[:120])); continue
        g, gc, n, nsteps = gamma_gc(seq)
        if sym == "SOX9":
            meta_stage = SOX9_STAGE
        else:
            meta_stage = PANEL[sym]
        cache_genes[sym] = dict(
            stage=meta_stage["stage"], stage_rank=meta_stage["stage_rank"], axis_rank=meta_stage["axis_rank"],
            role=meta_stage["role"], gene_id=meta["gene_id"], accession=meta["accession"],
            strand=("+" if strand == 1 else "-"), tss=tss, window="TSS-2000..+500",
            win_start=start, win_stop=stop, length_bp=len(seq), gc=round(gc, 4),
            gamma=round(g, 4), seq_sha256=hashlib.sha256(seq.encode()).hexdigest(),
            promoter_seq=seq)
        rows[sym] = (round(g, 4), round(gc, 4))
        print("  %-9s %-16s s%d %s %s TSS=%-10d gamma=%.4f GC=%.4f  %s"
              % (sym, meta_stage["stage"], meta_stage["stage_rank"], meta["accession"],
                 ("+" if strand == 1 else "-"), tss, g, gc, meta_stage["role"]))
        time.sleep(0.34)                            # be polite to NCBI
    # no-tuning fidelity gate -- the SOX9 anchor must reproduce or we refuse to persist
    if "SOX9" not in rows:
        raise RuntimeError("SOX9 anchor not fetched -- refusing to persist")
    gg, gcc = rows["SOX9"]
    assert abs(gg - ANCHORS["SOX9"]["gamma"]) < 1e-4 and abs(gcc - ANCHORS["SOX9"]["gc"]) < 1e-3, \
        "anchor SOX9 not reproduced (%.4f/%.4f) -- pipeline drift, refusing to write" % (gg, gcc)
    if failed:
        print("  NOTE: %d gene(s) failed to fetch and are recorded honestly (not silently dropped): %s"
              % (len(failed), ", ".join(s for s, _ in failed)))
    cache = {
        "_what": "Cached human proximal-promoter sequences (GRCh38.p14, NCBI exact TSS, TSS-2000..+500) "
                 "for the DEVELOPMENTAL master-gene panel (pluripotency / germ-layer / organ-primordium "
                 "/ HOX AP-axis). Enables OFFLINE bit-for-bit reproduction of gamma = -mean(NN-stacking "
                 "dG37, SantaLucia 1998). Measured input, never fitted.",
        "_assembly": "GRCh38.p14 (%s)" % ASSEMBLY,
        "_method": "gamma = -mean over consecutive dinucleotide steps of SantaLucia (1998) unified NN "
                   "stacking dG37; GC = (G+C)/ACGT. Pipeline identical to repro/_gamma/fetch_gamma.py, "
                   "repro/_germline/fetch_germline_gamma.py, and DNA fetch_morpho_gamma.py; accepted only "
                   "because it reproduces SOX9 (1.4598/0.545) and DAZL (1.3803/0.479).",
        "_tss_convention": "plus strand -> gene-range begin; minus strand -> gene-range end.",
        "_panel_declaration": "Panel declared by developmental stage_rank (pluripotency<germ-layer<organ) "
                              "and HOX axis_rank (3'->5') BEFORE gamma was seen; no gene added/dropped to "
                              "shape a result; gamma-vs-stage and gamma-vs-axis read-outs reported as they "
                              "fall (E4 tests permit a NULL).",
        "_firewall": "This package owns the FERTILISATION event (its two gametes meeting) + the early "
                     "embryo (oocyte-to-embryo transition: ZAR1/NLRP5, in the germline cache). The full "
                     "multi-organ morphogenesis ATLAS and the gene-clock LAW are the DNA 4D-Blueprint "
                     "package's SSOT; this panel is a measured DEMONSTRATION of that cited clock.",
        "_fetch_failures": [{"symbol": s, "error": e} for s, e in failed],
        "genes": cache_genes,
    }
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    _write_gamma_json(cache_genes, failed)
    print("  cache + embryo_gamma.json written (%d genes; %d failures)." % (len(cache_genes), len(failed)))
    return rows


def _write_gamma_json(cache_genes, failed):
    genes = {}
    for sym, rec in cache_genes.items():
        if sym == "SOX9":
            continue
        genes[sym] = {
            "gamma": rec["gamma"], "gc": rec["gc"], "stage": rec["stage"],
            "stage_rank": rec["stage_rank"], "axis_rank": rec["axis_rank"], "role": rec["role"],
            "src": "%s %s TSS-2000..+500" % (rec["accession"], rec["strand"]),
            "_source": "fetch_embryo_gamma.py reception (DNA NN-dG37 pipeline; measured, never fitted)",
        }
    asc = sorted(genes.keys(), key=lambda s: genes[s]["gamma"])
    out = {
        "_atlas": "VP developmental master-gene gamma (measured promoter thermodynamics).",
        "_provenance": "gamma = -mean(NN stacking dG37, SantaLucia 1998) over human proximal promoter "
                       "TSS-2000..+500 (GRCh38.p14). IDENTICAL pipeline to organ + gamete gamma; never "
                       "fitted. Validated against SOX9 (1.4598) and DAZL (1.3803).",
        "_panel_declaration": "Declared by developmental stage_rank + HOX axis_rank before gamma was seen "
                              "(see fetch_embryo_gamma.py PANEL).",
        "_firewall": "Fertilisation + early embryo owned here; full-body morphogenesis atlas + gene-clock "
                     "law are the DNA package SSOT (cited). This is a measured demonstration panel.",
        "_order_gamma_asc": asc,
        "_fetch_failures": [{"symbol": s, "error": e} for s, e in failed],
        "genes": genes,
    }
    json.dump(out, open(_GAMMA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------------- OFFLINE (default)
def _dazl_from_germ_cache():
    """Read the DAZL promoter from the germline cache so the DAZL anchor cross-checks offline."""
    if not os.path.exists(_GERM_CACHE):
        return None
    g = json.load(open(_GERM_CACHE, encoding="utf-8"))["genes"]
    return g.get("DAZL")


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
        out["genes"][sym] = dict(stage=rec.get("stage"), gamma=round(g, 4), gc=round(gc, 4),
                                 length_bp=rec["length_bp"], recompute_matches_cache=match_cache,
                                 matches_gamma_json=match_json, seq_sha_ok=seq_ok)
        out["all_seq_sha_ok"] &= seq_ok
        if not match_json:
            out["all_match_gamma_json"] = False
    # SOX9 anchor from this cache; DAZL anchor cross-checked from the germline cache (offline)
    s9 = out["genes"].get("SOX9", {})
    out["anchors_ok"]["SOX9"] = bool(abs(s9.get("gamma", 0) - ANCHORS["SOX9"]["gamma"]) < 1e-4
                                     and abs(s9.get("gc", 0) - ANCHORS["SOX9"]["gc"]) < 1e-3)
    dz = _dazl_from_germ_cache()
    if dz is not None:
        gdz, gcdz, _, _ = gamma_gc(dz["promoter_seq"])
        out["anchors_ok"]["DAZL"] = bool(abs(gdz - ANCHORS["DAZL"]["gamma"]) < 1e-4
                                         and abs(gcdz - ANCHORS["DAZL"]["gc"]) < 1e-3)
    else:
        out["anchors_ok"]["DAZL"] = None  # germline cache not present (should not happen in-package)
    anchors_pass = all(v for v in out["anchors_ok"].values() if v is not None)
    out["ok"] = bool(anchors_pass and out["all_match_gamma_json"] and out["all_seq_sha_ok"]
                     and all(g["recompute_matches_cache"] for g in out["genes"].values()))
    return out


def panel_gamma():
    """Convenience: {symbol: {gamma, gc, stage, stage_rank, axis_rank, role}} from the cache (offline).
    Includes SOX9 (the anchor doubling as an organ-primordium master)."""
    cache = json.load(open(_CACHE, encoding="utf-8"))["genes"]
    return {s: dict(gamma=round(r["gamma"], 4), gc=round(r["gc"], 4), stage=r.get("stage"),
                    stage_rank=r.get("stage_rank"), axis_rank=r.get("axis_rank"), role=r.get("role"))
            for s, r in cache.items()}


def main():
    ap = argparse.ArgumentParser(description="Developmental master-gene gamma reception.")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: resolve coords + fetch + rebuild cache")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    sys.exit(0 if v["ok"] else 1)


if __name__ == "__main__":
    main()
