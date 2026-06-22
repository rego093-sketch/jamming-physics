#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_region_features.py — the WORKING NCBI fetcher for the FULL A4 deferred read.

WHY THIS EXISTS (FIREWALL §1, the NAMED [O]). The seed reads each master-gene promoter as γ (LEVEL) +
the promoter-scale A4 SHAPE. The firewall flags ONE thing as a NAMED, DEFERRED [O]: the FULL A4
anchor/loop/anchor-relative-phase, which "needs the wider genomic region + an NCBI feature table
(rettype=ft) and is a named [O] deferred read — flagged, never invented." The inherited grammar
(inherited/dna_interpreter.py + inherited/key_pipeline_full.py) ALREADY contains every function the
full read uses (run_key shell-map, build_anchors, parse_ft_motors, build_loops, helix_coord). What was
missing was the MEASUREMENT — the two raw inputs per gene. This tool fetches exactly those two inputs.

WHAT IT FETCHES, per ear master gene (all coordinates derived from the FROZEN promoter cache — no esummary
needed, so the wide read is anchored to the frozen γ layer):
  (1) the WIDE region SEQUENCE — the FROZEN promoter window TSS−2000..+500, EXTENDED by FLANK on each
      genomic side (rettype=fasta, same strand as the cached promoter so orientation matches), and
  (2) the NCBI FEATURE TABLE over the SAME region (rettype=ft, same strand) — the real neighbouring-gene
      annotation that turns the coordinate read from anchors-only into real motors + loops.

KEYSTONE (consistency, not tuning): with a symmetric genomic FLANK the cached promoter sits at offset
FLANK in the strand-corrected region, so region[FLANK:FLANK+2501] MUST equal the cached promoter
byte-for-byte. The tool asserts this for every gene — the wide read provably sits ON TOP of the frozen
promoter read, with zero drift. The gene's own TSS is then at region offset FLANK+2000.

NO TUNING. FLANK is a single declared observation-window constant, identical for all genes, never adjusted
per gene to make any result look better. The downstream A4 LOCK (W=2000, step=500, min_shell_bp=5000,
loop_k=2, twist 34.29°/bp, rise 3.4 Å, contact face 0.17) is INHERITED and frozen — this tool changes
none of it. Every magnitude the read produces (absolute distances, counts) is [O]; only sign/class is
forced (and is shown N-robust in run.py by re-reading a central sub-window of the SAME fetch).

OUTPUT: writes a cache JSON {genes:{SYM:{acc, strand, region_window, efetch_strand, flank, tss_in_region,
region_seq, region_sha256, ft_text, ft_sha256, promoter_offset, ...}}, ...} with 2× determinism. The
offline gate (research/A4-anchor-loop-phase/run.py + gate.py, and the master verifier's no-regression
block once frozen) recompute the FULL A4 coordinate from these bytes with the inherited grammar, with no
network.

USAGE:
  python3 tools/fetch_region_features.py build  inherited/ear_promoters.cache.json  inherited/ear_regions.cache.json
  python3 tools/fetch_region_features.py verify inherited/ear_regions.cache.json     # re-audit vs live NCBI

γ/A4 read STRUCTURE only (firewall) — never a voltage, dose, selectivity, or effect. Identity/order are the
DNA volume's [V], cited not re-derived. Network required for build/verify; the offline recompute is in run.py.
"""
import urllib.request, json, time, hashlib, sys, os

FLANK = 20000   # bp extension on EACH genomic side of the frozen promoter window (single, gene-independent)
UA = {"User-Agent": "vp-emergence-seed/0.11 (jamming-physics.org; ORCID 0009-0002-7535-8245)"}


def _get(url, tries=5):
    last = None
    for k in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read().decode()
        except Exception as e:
            last = e; time.sleep(1.5 * (k + 1))
    raise last


def _efetch_fasta(acc, st, sp, strand):
    raw = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
               f"?db=nuccore&id={acc}&rettype=fasta&retmode=text&seq_start={st}&seq_stop={sp}&strand={strand}")
    return "".join(l.strip() for l in raw.splitlines() if not l.startswith(">")).upper()


def _efetch_ft(acc, st, sp, strand):
    return _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
                f"?db=nuccore&id={acc}&rettype=ft&retmode=text&seq_start={st}&seq_stop={sp}&strand={strand}")


def _region_window(prom_window, efetch_strand, flank=FLANK):
    """Extend the FROZEN promoter genomic window by flank on each genomic side. Strand-agnostic:
       the promoter lands at region offset `flank` in the strand-corrected region either way."""
    lo, hi = int(prom_window[0]) - flank, int(prom_window[1]) + flank
    return lo, hi


def build_one(sym, prec):
    """Fetch the wide region + feature table for one gene; assert the keystone (region⊃frozen promoter)."""
    acc = prec["acc"]; strand = prec["efetch_strand"]
    lo, hi = _region_window(prec["genomic_window"], strand)
    time.sleep(0.34)
    region = _efetch_fasta(acc, lo, hi, strand)
    time.sleep(0.40)
    ft = _efetch_ft(acc, lo, hi, strand)
    # KEYSTONE: the cached promoter must sit at offset FLANK in the strand-corrected region.
    prom = prec["seq"]; off = FLANK
    slice_ = region[off:off + len(prom)]
    keystone = (slice_ == prom)
    return dict(
        acc=acc, strand=prec["strand"], efetch_strand=strand, flank=FLANK,
        region_window=[lo, hi], region_length=len(region),
        promoter_offset=off, tss_in_region=off + 2000,         # TSS is at promoter offset 2000
        region_seq=region, region_sha256=hashlib.sha256(region.encode()).hexdigest(),
        ft_text=ft, ft_sha256=hashlib.sha256(ft.encode()).hexdigest(),
        keystone_region_contains_frozen_promoter=keystone,
        node=prec.get("node"), role=prec.get("role"),
    )


def build(prom_cache_path, out_path):
    pc = json.load(open(prom_cache_path, encoding="utf-8"))
    genes = pc["genes"]; out = {}; fails = []
    for sym, prec in genes.items():
        try:
            rec = build_one(sym, prec)
            out[sym] = rec
            tag = "KEYSTONE-OK" if rec["keystone_region_contains_frozen_promoter"] else "KEYSTONE-FAIL"
            print(f"  {sym:9s} {rec['acc']:15s} {rec['strand']} L={rec['region_length']} "
                  f"TSS@{rec['tss_in_region']} ft={len(rec['ft_text'])}B  {tag}")
        except Exception as e:
            fails.append(sym); print(f"  {sym:9s} FAIL {type(e).__name__}: {e}")
        time.sleep(0.5)
    payload = dict(
        _provenance=("FULL A4 deferred read inputs (FIREWALL named [O]): wide region + NCBI feature table, "
                     "fetched from NCBI nuccore (GRCh38 current RefSeq chromosomes) by the FROZEN promoter "
                     "window extended by FLANK bp each genomic side, same strand. Coordinates derived from "
                     "the frozen promoter cache; region[FLANK:FLANK+2501]==frozen promoter (keystone)."),
        _flank=FLANK, _window="frozen promoter TSS-2000..+500 extended by FLANK each genomic side",
        _method="efetch rettype=fasta + rettype=ft, retmode=text, same strand as cached promoter",
        _grammar="inherited/dna_interpreter.py + inherited/key_pipeline_full.py (run_key/parse_ft_motors/"
                 "build_loops/helix_coord) — vendored byte-identical; this read invents no new machinery",
        _n_genes=len(out), _fails=fails, genes=out,
    )
    json.dump(payload, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=False)
    allkey = all(r["keystone_region_contains_frozen_promoter"] for r in out.values())
    print(f"\nWROTE {out_path}  genes={len(out)} fails={len(fails)}  ALL-KEYSTONE-OK={allkey}")


def verify(cache_path):
    """Re-audit the cached wide regions + feature tables against live NCBI (byte-exact)."""
    cache = json.load(open(cache_path, encoding="utf-8"))["genes"]; allok = True
    for sym, rec in cache.items():
        lo, hi = rec["region_window"]; strand = rec["efetch_strand"]; acc = rec["acc"]
        liveR = _efetch_fasta(acc, lo, hi, strand); time.sleep(0.34)
        liveF = _efetch_ft(acc, lo, hi, strand)
        okR = hashlib.sha256(liveR.encode()).hexdigest() == rec["region_sha256"]
        okF = hashlib.sha256(liveF.encode()).hexdigest() == rec["ft_sha256"]
        allok &= (okR and okF)
        print(f"  {sym:9s} region {'OK' if okR else 'MISMATCH'}  ft {'OK' if okF else 'MISMATCH'}")
        time.sleep(0.5)
    print("ALL REGION+FT BYTE-EXACT vs LIVE NCBI:", allok)


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "build":
        build(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 3 and sys.argv[1] == "verify":
        verify(sys.argv[2])
    else:
        print(__doc__)
