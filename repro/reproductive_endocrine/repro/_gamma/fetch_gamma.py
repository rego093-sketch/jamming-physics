#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_gamma.py  --  Master-gene gamma RECEPTION for the reproductive / gonadal package.

WHAT THIS IS
  The DNA morphogenesis gene-clock owns organ identity + emergence ORDER from MEASURED master-gene
  gamma. Three reproductive masters (FOXL2 / DAZL / WT1) were named but not yet in the vendored DNA
  subset -- carried as honest TO-MEASURE inputs. This module RECEIVES them via the SAME pipeline the
  DNA atlas uses (NN-stacking dG37, SantaLucia 1998, on the cited proximal promoter), then vendors the
  result. gamma is a MEASURED input, never fitted.

PIPELINE (identical to DNA fetch_morpho_gamma.py)
  gamma = -mean over consecutive dinucleotide steps of the SantaLucia (1998) unified nearest-neighbour
          stacking dG37 (kcal/mol), taken over the human proximal promoter window TSS-2000..+500
          (GRCh38, NCBI exact TSS). GC = (G+C)/ACGT. No initiation / terminal / symmetry correction --
          a pure mean of stacking terms (matches the vendored SOX9 anchor to 4 dp).
  TSS convention: plus strand -> gene-range begin ; minus strand -> gene-range end
          (NCBI datasets v2alpha gene/symbol, GRCh38 genomic_locations). Validated on SOX9.

FIDELITY CHECK (no-tuning discipline)
  The pipeline is accepted ONLY because it reproduces the vendored anchor SOX9 (gamma=1.4598, GC=0.545)
  bit-for-bit. Having reproduced the known anchor, the three unknowns measured with the identical code
  are legitimate measurements, not fits.

MODES
  (default, OFFLINE)   verify()  : recompute gamma from inherited/organ_promoters.cache.json, cross-
                                   check SOX9, and confirm it matches inherited/organ_gamma.json.
                                   Deterministic, no network -- this is what reproduces the package.
  --fetch  (ONLINE)    fetch()   : pull each promoter from NCBI E-utilities (strand-aware), rebuild the
                                   cache, and write the measured gamma back into organ_gamma.json.
                                   This is how the cache was built; not needed to reproduce.
"""
import os, sys, json, math, argparse, hashlib

_HERE      = os.path.dirname(os.path.abspath(__file__))
_INHERITED = os.path.join(_HERE, "..", "..", "inherited")
_CACHE     = os.path.join(_INHERITED, "organ_promoters.cache.json")
_GAMMA     = os.path.join(_INHERITED, "organ_gamma.json")

# SantaLucia (1998) unified NN nearest-neighbour stacking dG37 (kcal/mol), 16-entry 5'->3' top strand.
# Reverse-complement-symmetric, so mean(NN dG37) and GC are strand-invariant.
NN_DG37 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}

# Master genes received by this module. accession/begin/end are GRCh38 gene-range (NCBI datasets v2).
RECEIVE = {
    "FOXL2": dict(organ="gonad_ovary",        accession="NC_000003.12", orientation="minus",
                  begin=138944224, end=138947137),
    "DAZL":  dict(organ="germline",           accession="NC_000003.12", orientation="minus",
                  begin=16586792,  end=16605423),
    "WT1":   dict(organ="reproductive_tract", accession="NC_000011.10", orientation="minus",
                  begin=32387775,  end=32435539),
}
# Vendored anchor used as the fidelity cross-check (must reproduce gamma=1.4598, GC=0.545).
ANCHOR = dict(symbol="SOX9", organ="gonad_testis", accession="NC_000017.11", orientation="plus",
              begin=72121020, end=72126416, gamma=1.4598, gc=0.545)


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
    """Genomic window for TSS-2000..+500. plus: TSS=begin; minus: TSS=end. Returns (tss, start, stop, strand)."""
    if orientation == "plus":
        tss = begin; return tss, tss - 2000, tss + 500, 1
    tss = end;     return tss, tss - 500,  tss + 2000, 2


# ----------------------------------------------------------------------------- ONLINE
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
    """ONLINE: fetch promoters, rebuild the cache, write measured gamma into organ_gamma.json."""
    rows = {}
    allrows = {ANCHOR["symbol"]: {k: ANCHOR[k] for k in ("organ", "accession", "orientation", "begin", "end")}}
    allrows.update(RECEIVE)
    cache_genes = {}
    for sym in ("SOX9", "FOXL2", "DAZL", "WT1"):
        meta = allrows[sym]
        tss, start, stop, strand = window_for(meta["orientation"], meta["begin"], meta["end"])
        seq = _efetch(meta["accession"], start, stop, strand)
        g, gc, n, nsteps = gamma_gc(seq)
        cache_genes[sym] = dict(
            organ=meta["organ"], accession=meta["accession"],
            strand=("+" if strand == 1 else "-"), tss=tss, window="TSS-2000..+500",
            win_start=start, win_stop=stop, length_bp=len(seq), gc=round(gc, 4),
            gamma=round(g, 4), seq_sha256=hashlib.sha256(seq.encode()).hexdigest(),
            promoter_seq=seq)
        rows[sym] = (round(g, 4), round(gc, 4))
        print("  fetched %-6s %-18s %s %s TSS=%d  gamma=%.4f  GC=%.4f"
              % (sym, meta["organ"], meta["accession"], ("+" if strand == 1 else "-"), tss, g, gc))
    # fidelity cross-check before persisting
    ag, agc = rows["SOX9"]
    assert abs(ag - ANCHOR["gamma"]) < 1e-4 and abs(agc - ANCHOR["gc"]) < 1e-3, \
        "SOX9 anchor not reproduced (%.4f/%.4f) -- pipeline drift, refusing to write" % (ag, agc)
    cache = {
        "_what": "Cached human proximal-promoter sequences (GRCh38, NCBI exact TSS, window TSS-2000..+500) "
                 "for the reproductive/gonadal master genes. Enables OFFLINE bit-for-bit reproduction of "
                 "gamma = -mean(NN-stacking dG37, SantaLucia 1998). Measured input, never fitted.",
        "_assembly": "GRCh38.p14 (GCF_000001405.40)",
        "_method": "gamma = -mean over consecutive dinucleotide steps of SantaLucia (1998) unified NN "
                   "stacking dG37 (kcal/mol); GC = (G+C)/ACGT. Pipeline identical to DNA "
                   "fetch_morpho_gamma.py; validated by reproducing SOX9 gamma=1.4598, GC=0.545.",
        "_tss_convention": "plus strand -> gene-range begin; minus strand -> gene-range end "
                           "(NCBI datasets v2alpha gene/symbol GRCh38 genomic_locations). Validated on SOX9.",
        "genes": cache_genes,
    }
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    _write_gamma_json(rows)
    print("  cache + organ_gamma.json updated.")
    return rows


def _write_gamma_json(rows):
    """Move FOXL2/DAZL/WT1 from _to_measure into genes{} with measured gamma."""
    d = json.load(open(_GAMMA, encoding="utf-8"))
    for sym, meta in RECEIVE.items():
        g, gc = rows[sym]
        tss, start, stop, strand = window_for(meta["orientation"], meta["begin"], meta["end"])
        d["genes"][sym] = {
            "gamma": g, "gc": gc,
            "src": "%s %s TSS-2000..+500" % (meta["accession"], "+" if strand == 1 else "-"),
            "_source": "fetch_gamma.py reception (DNA fetch_morpho_gamma pipeline; measured, never fitted)",
        }
    d["_to_measure"] = []  # all received
    d["_reception_note"] = ("FOXL2/DAZL/WT1 received via repro/_gamma/fetch_gamma.py using the DNA "
                            "fetch_morpho_gamma pipeline (NN-stacking dG37, SantaLucia 1998, promoter "
                            "TSS-2000..+500). Sequences cached in organ_promoters.cache.json for offline "
                            "bit-for-bit reproduction. Pipeline validated by reproducing SOX9 (1.4598/0.545).")
    json.dump(d, open(_GAMMA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------------- OFFLINE (default)
def verify():
    """OFFLINE: recompute gamma from cache, cross-check SOX9, confirm organ_gamma.json agreement."""
    if not os.path.exists(_CACHE):
        return {"ok": False, "reason": "cache absent -- run with --fetch once (network)"}
    cache = json.load(open(_CACHE, encoding="utf-8"))["genes"]
    gj = json.load(open(_GAMMA, encoding="utf-8"))["genes"]
    out = {"genes": {}, "anchor_ok": None, "all_match_gamma_json": True, "all_seq_sha_ok": True}
    for sym, rec in sorted(cache.items()):
        g, gc, n, nsteps = gamma_gc(rec["promoter_seq"])
        seq_ok = hashlib.sha256(rec["promoter_seq"].encode()).hexdigest() == rec["seq_sha256"]
        recomputed = (round(g, 4), round(gc, 4))
        cached = (round(rec["gamma"], 4), round(rec["gc"], 4))
        match_cache = recomputed == cached
        match_json = (sym not in gj) or abs(round(g, 4) - round(gj[sym]["gamma"], 4)) < 1e-4
        out["genes"][sym] = dict(organ=rec["organ"], gamma=round(g, 4), gc=round(gc, 4),
                                 length_bp=rec["length_bp"], recompute_matches_cache=match_cache,
                                 matches_gamma_json=match_json, seq_sha_ok=seq_ok)
        out["all_seq_sha_ok"] &= seq_ok
        if not match_json:
            out["all_match_gamma_json"] = False
    s = out["genes"].get(ANCHOR["symbol"], {})
    out["anchor_ok"] = bool(abs(s.get("gamma", 0) - ANCHOR["gamma"]) < 1e-4
                            and abs(s.get("gc", 0) - ANCHOR["gc"]) < 1e-3)
    out["ok"] = bool(out["anchor_ok"] and out["all_match_gamma_json"] and out["all_seq_sha_ok"]
                     and all(g["recompute_matches_cache"] for g in out["genes"].values()))
    return out


def main():
    ap = argparse.ArgumentParser(description="Reproductive master-gene gamma reception.")
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
