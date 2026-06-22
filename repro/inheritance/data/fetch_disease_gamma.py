#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_disease_gamma.py  --  DISEASE master-gene promoter gamma RECEPTION (cancer + neurodegeneration).

WHAT THIS IS  (v0.8.0, the disease-class extension of the feasibility map)
  The kit already carries the MEASURED autism-spectrum atlas (inherited/neuro_gamma.json) and runs it
  through the RNA feasibility map (engine/rna_feasibility_map.py, battery FM). The user asked to extend
  the SAME map to more disease classes -- cancer, Parkinson's, "various genetic diseases" -- by inheriting
  the disease/gene declarations already curated in the sibling vp-site program (repro/disease_kit: each
  monogenic disease carries a measured promoter gamma, a gene ROLE brake/driver, a disease MECHANISM
  GOF/LOF, and a corrective DIRECTION, all under the identical magnitude firewall). We do NOT import any
  gamma from that program; we RE-MEASURE every gene here through this kit's own anchor-gated pipeline
  (NN-stacking dG37, SantaLucia 1998; human proximal promoter TSS-2000..+500, GRCh38), then vendor the
  result. gamma is a MEASURED input, never fitted. Sampling, not exhaustion: two disease classes
  (oncology, neurodegeneration) declared by function -- the named request, not the whole of medicine.

NO-TUNING DISCIPLINE  (inherited, binding)
  The pipeline is accepted ONLY because it reproduces the vendored anchor SOX9 (gamma=1.4598, GC=0.545)
  bit-for-bit. Each panel is declared BY FUNCTION -- with its role/mechanism/corrective sign fixed -- BEFORE
  any gamma is seen. No gamma is moved to rescue any result. The promoter gamma reads the locus switch
  STRUCTURE only; the disease-causing coding lesions (and their magnitudes) sit OUTSIDE the promoter
  firewall and are runtime [O].

CROSS-PACKAGE CONSISTENCY (a no-tuning cross-validation, new in this kit)
  Four genes here are independently measured by the sibling program through the same method but a separate
  codebase: PTEN (also an ASD gene, neuro_gamma=1.5694), VHL (disease_kit hereditary-RCC=1.4325), SOD1
  (disease_kit ALS=1.4443), HTT (disease_kit Huntington=1.6142). After measuring, we CHECK that our fresh
  reads reproduce those independently-measured values (tol 2e-3). Agreement is evidence the pipeline is
  the same measurement, not a fit; it is reported, not used to tune anything.

MODES
  (default, OFFLINE)  verify() : recompute gamma from the cached promoters, cross-check the SOX9 anchor
                                 reproduces, confirm agreement with the vendored atlases. No network.
  --fetch  (ONLINE)   fetch()  : resolve each gene's GRCh38 coordinates from NCBI esummary (selecting the
                                 OFFICIAL-symbol record -- 'HTT[sym]' otherwise returns SLC6A4 first), pull
                                 the promoter window via efetch, rebuild the two caches + two atlases.
"""
import os, sys, json, math, time, hashlib, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
_INH  = os.path.join(_HERE, "..", "inherited")

# SantaLucia (1998) unified NN stacking dG37 (kcal/mol) -- IDENTICAL table to fetch_rna_gamma.py.
NN_DG37 = {
    "AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88,
    "CA": -1.45, "CC": -1.84, "CG": -2.17, "CT": -1.28,
    "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
    "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00,
}

# ============================================================================================
#  PANELS DECLARED BY FUNCTION (role / mechanism / corrective drive sign fixed BEFORE gamma).
#    role        : 'suppressor'|'oncogene' (cancer) ; 'brake'|'driver' (neurodegeneration)
#    mechanism   : LOF (loss/under-active) | GOF (gain/over-active, incl. toxic aggregation)
#    corr_sign   : the sign of the corrective drive on the GENE'S OWN switch -- FORCED by mechanism:
#                    GOF -> '-' (knock it DOWN: siRNA / Lever-B knockdown / kinase-inhibit)
#                    LOF -> '+' (restore it UP : saRNA / CRISPRa / Lever-B activation / Lever-A repair)
#    therapy     : a real, named molecular lever (evidence the LeverExistence factor is non-empty).
#  No cherry-picking: the panel is the canonical driver set for each class, declared whole.
# ============================================================================================
ONCO = {
    # tumour suppressors -- lost (LOF) -> corrective drive is to RESTORE (+)
    "TP53":   dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="restore p53 pathway / MDM2-i in WT context", note="guardian of the genome (apoptosis + cell-cycle gate)"),
    "RB1":    dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="CDK4/6-i exploits an intact RB axis", note="retinoblastoma cell-cycle brake (E2F restraint)"),
    "PTEN":   dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="PI3K/AKT/mTOR-i downstream of PTEN loss", note="PI3K phosphatase brake (also a SFARI ASD gene -- cross-check vs neuro_gamma)"),
    "VHL":    dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="HIF2a-i (belzutifan) downstream of VHL loss", note="HIF E3-ligase substrate recognition (hereditary RCC -- cross-check vs disease_kit)"),
    "APC":    dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="Wnt/tankyrase-i downstream of APC loss", note="Wnt destruction-complex scaffold (colorectal)"),
    "BRCA1":  dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="PARP-i synthetic-lethal with HR loss", note="homologous-recombination DNA repair"),
    "NF1":    dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="MEK-i downstream of RAS-GAP loss (selumetinib)", note="RAS-GTPase-activating brake (neurofibromatosis)"),
    "CDKN2A": dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="CDK4/6-i for p16 loss", note="p16INK4a / p14ARF cell-cycle + p53 brake"),
    "STK11":  dict(role="suppressor", mechanism="LOF", corr_sign="+", therapy="mTOR/metabolic axis downstream of LKB1 loss", note="LKB1 energy-sensing kinase brake (Peutz-Jeghers)"),
    # oncogenes -- hyperactive (GOF) -> corrective drive is to KNOCK DOWN (-)
    "KRAS":   dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="KRAS-G12C-i (sotorasib) / siRNA knockdown", note="RAS GTPase proliferation driver"),
    "MYC":    dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="BET-i / MYC-targeted knockdown", note="transcriptional amplifier driver"),
    "EGFR":   dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="EGFR-TKI (osimertinib)", note="receptor tyrosine-kinase driver"),
    "BRAF":   dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="BRAF-i (vemurafenib/dabrafenib)", note="RAF kinase driver (V600E)"),
    "MDM2":   dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="MDM2-i (nutlin-class) re-activates p53", note="p53 negative regulator (amplified)"),
    "BCL2":   dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="BCL2-i (venetoclax)", note="anti-apoptotic survival driver"),
    "PIK3CA": dict(role="oncogene",   mechanism="GOF", corr_sign="-", therapy="PI3Ka-i (alpelisib)", note="PI3-kinase catalytic-alpha driver"),
}

NEURODEGEN = {
    # Parkinson's disease -- dominant toxic / hyperactive (GOF) -> knock DOWN (-)
    "SNCA":   dict(role="driver", mechanism="GOF", corr_sign="-", therapy="SNCA-lowering ASO (clinical trials)", note="alpha-synuclein; toxic aggregation, gene-dosage PD"),
    "LRRK2":  dict(role="driver", mechanism="GOF", corr_sign="-", therapy="LRRK2 kinase-i / ASO (clinical trials)", note="leucine-rich-repeat kinase; hyperactive G2019S"),
    "VPS35":  dict(role="driver", mechanism="GOF", corr_sign="-", therapy="retromer-stabilising (preclinical)", note="retromer; dominant D620N PD"),
    # Parkinson's disease -- recessive loss (LOF) -> RESTORE (+)
    "PRKN":   dict(role="brake",  mechanism="LOF", corr_sign="+", therapy="restore mitophagy / PRKN gene-replacement (preclinical)", note="Parkin E3 ligase; recessive early-onset PD (mitophagy)"),
    "PINK1":  dict(role="brake",  mechanism="LOF", corr_sign="+", therapy="PINK1-pathway activation (preclinical)", note="mitochondrial kinase; recessive PD (mitophagy)"),
    "PARK7":  dict(role="brake",  mechanism="LOF", corr_sign="+", therapy="oxidative-stress-axis support (preclinical)", note="DJ-1 redox sensor; recessive PD"),
    "GBA1":   dict(role="brake",  mechanism="LOF", corr_sign="+", therapy="substrate-reduction / chaperone (ambroxol trials)", note="glucocerebrosidase; strongest PD risk gene (lysosomal)"),
    # proteinopathy bridge + cross-package consistency anchors (toxic GOF -> knock DOWN -)
    "HTT":    dict(role="brake",  mechanism="GOF", corr_sign="-", therapy="HTT-lowering ASO (tominersen-class)", note="huntingtin; toxic polyQ (Huntington -- cross-check vs disease_kit)"),
    "SOD1":   dict(role="brake",  mechanism="GOF", corr_sign="-", therapy="SOD1 ASO (tofersen, FDA 2023)", note="Cu/Zn dismutase; toxic misfold (ALS1 -- cross-check vs disease_kit)"),
}

# Vendored fidelity anchor (must reproduce gamma=1.4598, GC=0.545) -- identical to the RNA fetcher.
ANCHOR = dict(symbol="SOX9", accession="NC_000017.11", orientation="plus",
              begin=72121020, end=72126416, gamma=1.4598, gc=0.545)

# Independently-measured sibling-program reads (vp-site), for the no-tuning cross-validation only.
# These are NOT imported as our gamma; we re-measure and CHECK agreement (tol 2e-3).
CROSSCHECK = {
    "PTEN": ("neuro_gamma.json (this kit, ASD atlas)", 1.5694),
    "VHL":  ("vp-site disease_kit von_hippel_lindau", 1.4325),
    "SOD1": ("vp-site disease_kit SOD1-ALS",           1.4443),
    "HTT":  ("vp-site disease_kit Huntington",          1.6142),
}


def gamma_gc(seq):
    """gamma = -mean(NN-stacking dG37); GC over ACGT.  IDENTICAL to fetch_rna_gamma.gamma_gc."""
    seq = seq.upper()
    acgt = [c for c in seq if c in "ACGT"]
    n = len(acgt)
    gc = (acgt.count("G") + acgt.count("C")) / n
    steps = [seq[i:i + 2] for i in range(len(seq) - 1)]
    dg = [NN_DG37[d] for d in steps if d in NN_DG37]
    return -sum(dg) / len(dg), gc, n


def window_for(orientation, begin, end):
    """TSS-2000..+500. plus: TSS=begin; minus: TSS=end.  IDENTICAL to fetch_rna_gamma.window_for."""
    if orientation == "plus":
        tss = begin; return tss, tss - 2000, tss + 500, 1
    tss = end;     return tss, tss - 500,  tss + 2000, 2


# ----------------------------------------------------------------------------- ONLINE
def _get(url, timeout=45, tries=4):
    import urllib.request
    last = None
    for a in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.read().decode()
        except Exception as e:
            last = e; time.sleep(2.0 * (a + 1))
    raise RuntimeError("GET failed: %r" % last)


def _gene_coords(sym):
    """Resolve GRCh38 (accession, orientation, begin, end) from NCBI -- selecting the record whose
    OFFICIAL symbol equals `sym` (alias collisions otherwise return the wrong locus, e.g. HTT->SLC6A4)."""
    import urllib.parse
    q = {"db": "gene", "term": "%s[sym] AND Homo sapiens[orgn] AND alive[prop]" % sym, "retmode": "json"}
    js = json.loads(_get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(q)))
    ids = js["esearchresult"]["idlist"]
    if not ids:
        raise RuntimeError("%s: no gene id" % sym)
    s = json.loads(_get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" +
                        urllib.parse.urlencode({"db": "gene", "id": ",".join(ids), "retmode": "json"})))
    chosen = None
    for gid in ids:
        rec = s["result"].get(gid, {})
        if str(rec.get("name", "")).upper() == sym.upper() and rec.get("genomicinfo"):
            chosen = (gid, rec); break
    if chosen is None:                       # fall back to first with coordinates (then assert symbol)
        for gid in ids:
            rec = s["result"].get(gid, {})
            if rec.get("genomicinfo"):
                chosen = (gid, rec); break
    if chosen is None:
        raise RuntimeError("%s: no record with genomic coordinates" % sym)
    gid, rec = chosen
    assert str(rec.get("name", "")).upper() == sym.upper(), \
        "%s: official-symbol mismatch (got %r) -- refusing to fetch a different locus" % (sym, rec.get("name"))
    gi = rec["genomicinfo"][0]
    acc = gi["chraccver"]; a = int(gi["chrstart"]); b = int(gi["chrstop"])
    if a <= b:
        return dict(symbol=sym, gene_id=gid, accession=acc, orientation="plus", begin=a + 1, end=b + 1)
    return dict(symbol=sym, gene_id=gid, accession=acc, orientation="minus", begin=b + 1, end=a + 1)


def _efetch(acc, start, stop, strand, timeout=55):
    import urllib.parse
    q = {"db": "nuccore", "id": acc, "seq_start": str(start), "seq_stop": str(stop),
         "strand": str(strand), "rettype": "fasta", "retmode": "text"}
    txt = _get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?" + urllib.parse.urlencode(q), timeout=timeout)
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">")).upper()


def _measure_panel(panel, classname):
    genes = {}
    for sym, decl in panel.items():
        c = _gene_coords(sym)
        tss, a, b, strand = window_for(c["orientation"], c["begin"], c["end"])
        seq = _efetch(c["accession"], a, b, strand)
        g, gc, n = gamma_gc(seq)
        genes[sym] = dict(disease_class=classname, role=decl["role"], mechanism=decl["mechanism"],
                          corr_sign=decl["corr_sign"], therapy=decl["therapy"], note=decl["note"],
                          gene_id=c["gene_id"], accession=c["accession"],
                          strand=("+" if strand == 1 else "-"), tss=tss, window="TSS-2000..+500",
                          length_bp=len(seq), gc=round(gc, 4), gamma=round(g, 4),
                          seq_sha256=hashlib.sha256(seq.encode()).hexdigest(), promoter_seq=seq)
        print("  %-7s %-12s %s TSS=%-10d gamma=%.4f GC=%.4f  %s/%s corr=%s"
              % (sym, c["accession"], ("+" if strand == 1 else "-"), tss, g, gc,
                 decl["role"], decl["mechanism"], decl["corr_sign"]))
        time.sleep(0.8)
    return genes


def _write(classname, atlas_path, cache_path, panel_decl, genes):
    cache = {
        "_what": "Cached human proximal-promoter sequences (GRCh38, NCBI exact TSS, window TSS-2000..+500) "
                 "for the %s disease master-gene panel. Offline bit-for-bit gamma reproduction." % classname,
        "_assembly": "GRCh38 (NCBI RefSeq, esummary genomicinfo per OFFICIAL gene symbol; alive[prop])",
        "_method": "gamma = -mean(NN-stacking dG37, SantaLucia 1998); GC=(G+C)/ACGT. IDENTICAL pipeline to "
                   "the RNA/germline/immune atlases; validated by reproducing SOX9 gamma=1.4598, GC=0.545.",
        "_panel_declaration": "Panel declared by %s function (role/mechanism/corrective sign) BEFORE gamma "
                              "was seen. Corrective drive sign is FORCED by mechanism: GOF->'-', LOF->'+'." % classname,
        "_anchor_ok": True, "genes": genes,
    }
    json.dump(cache, open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    atlas = {
        "_atlas": "VP %s disease master-gene gamma (NCBI-direct, v0.8.0)." % classname,
        "_provenance": "gamma = -mean(NN stacking dG37, SantaLucia 1998), promoter TSS-2000..+500 (GRCh38). "
                       "IDENTICAL pipeline to the RNA/germline/immune/autism atlases; never fitted. Validated "
                       "against SOX9. The promoter gamma reads the locus switch STRUCTURE only; disease coding "
                       "lesions and their magnitudes sit OUTSIDE the firewall and are runtime [O].",
        "_panel_basis": panel_decl,
        "_corrective_sign_rule": "Sign of the corrective drive on the gene's OWN switch is FORCED by the "
                                 "disease mechanism: GOF (over-active) -> '-' (knock DOWN; siRNA / Lever-B "
                                 "knockdown); LOF (under-active) -> '+' (restore UP; saRNA / Lever-B activation "
                                 "/ Lever-A repair). Sign [F]/[V]; absolute dose [O].",
        "_order_gamma_asc": sorted(genes, key=lambda k: genes[k]["gamma"]),
        "genes": {k: {"gamma": v["gamma"], "gc": v["gc"], "role": v["role"], "mechanism": v["mechanism"],
                      "corr_sign": v["corr_sign"], "therapy": v["therapy"], "note": v["note"],
                      "gene_id": v["gene_id"], "src": v["accession"] + " " + v["strand"] + " TSS-2000..+500"}
                  for k, v in genes.items()},
    }
    json.dump(atlas, open(atlas_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def fetch():
    """ONLINE: resolve coords + fetch promoters + rebuild caches and atlases. Anchor-gated; cross-validated."""
    # anchor first -- refuse to write anything if SOX9 does not reproduce
    tss, a, b, strand = window_for(ANCHOR["orientation"], ANCHOR["begin"], ANCHOR["end"])
    ag, agc, _ = gamma_gc(_efetch(ANCHOR["accession"], a, b, strand))
    print("  ANCHOR SOX9 gamma=%.4f GC=%.4f" % (ag, agc))
    assert abs(round(ag, 4) - ANCHOR["gamma"]) < 1e-3 and abs(round(agc, 4) - ANCHOR["gc"]) < 2e-3, \
        "SOX9 anchor not reproduced (%.4f/%.4f) -- pipeline drift, refusing to write" % (ag, agc)

    print(" [oncology]")
    onco = _measure_panel(ONCO, "oncology")
    print(" [neurodegeneration]")
    ndg = _measure_panel(NEURODEGEN, "neurodegeneration")

    _write("oncology", os.path.join(_INH, "onco_gamma.json"),
           os.path.join(_INH, "onco_promoters.cache.json"),
           "Canonical cancer driver master-genes (tumour suppressors + oncogenes), declared by function "
           "before measurement; grounded in the sibling vp-site oncology/disease_kit curation.", onco)
    _write("neurodegeneration", os.path.join(_INH, "neurodegen_gamma.json"),
           os.path.join(_INH, "neurodegen_promoters.cache.json"),
           "Parkinson's-disease master-genes (dominant toxic-GOF + recessive LOF) plus a proteinopathy "
           "bridge (HTT, SOD1); declared by function before measurement; grounded in vp-site disease_kit.", ndg)

    # cross-package consistency check (reported, never used to tune)
    allg = {}; allg.update(onco); allg.update(ndg)
    print(" [cross-package consistency]")
    for sym, (src, ref) in CROSSCHECK.items():
        got = allg[sym]["gamma"]; ok = abs(got - ref) < 2e-3
        print("  %-6s measured=%.4f  ref=%.4f (%s)  %s" % (sym, got, ref, src, "OK" if ok else "DRIFT"))
    print("  caches + atlases written (oncology=%d, neurodegeneration=%d genes)." % (len(onco), len(ndg)))


# ----------------------------------------------------------------------------- OFFLINE (default)
def _verify_one(cache_path, atlas_path):
    if not os.path.exists(cache_path):
        return {"ok": False, "reason": "cache absent -- run with --fetch once (network)"}
    cache = json.load(open(cache_path, encoding="utf-8"))["genes"]
    atlas = json.load(open(atlas_path, encoding="utf-8"))["genes"]
    out = {"genes": {}, "anchor_reproduced": None, "all_match_atlas": True, "all_seq_sha_ok": True, "n": len(cache)}
    for sym, rec in sorted(cache.items()):
        g, gc, n = gamma_gc(rec["promoter_seq"])
        seq_ok = hashlib.sha256(rec["promoter_seq"].encode()).hexdigest() == rec["seq_sha256"]
        match_cache = (round(g, 4), round(gc, 4)) == (round(rec["gamma"], 4), round(rec["gc"], 4))
        match_atlas = (sym not in atlas) or abs(round(g, 4) - round(atlas[sym]["gamma"], 4)) < 1e-4
        out["genes"][sym] = dict(gamma=round(g, 4), gc=round(gc, 4), recompute_matches_cache=match_cache,
                                 matches_atlas=match_atlas, seq_sha_ok=seq_ok)
        out["all_seq_sha_ok"] &= seq_ok
        if not match_atlas:
            out["all_match_atlas"] = False
    out["anchor_reproduced"] = bool(json.load(open(cache_path, encoding="utf-8")).get("_anchor_ok"))
    out["ok"] = bool(out["anchor_reproduced"] and out["all_match_atlas"] and out["all_seq_sha_ok"]
                     and all(v["recompute_matches_cache"] for v in out["genes"].values()))
    return out


def verify():
    """OFFLINE: recompute gamma from both disease caches, confirm atlas agreement + sha + anchor flag.
    Also reports the cross-package consistency check against the sibling-program reads (tol 2e-3)."""
    onco = _verify_one(os.path.join(_INH, "onco_promoters.cache.json"),
                       os.path.join(_INH, "onco_gamma.json"))
    ndg = _verify_one(os.path.join(_INH, "neurodegen_promoters.cache.json"),
                      os.path.join(_INH, "neurodegen_gamma.json"))
    cross = {}
    merged = {}
    for r in (onco, ndg):
        for sym, v in r.get("genes", {}).items():
            merged[sym] = v["gamma"]
    for sym, (src, ref) in CROSSCHECK.items():
        if sym in merged:
            cross[sym] = dict(measured=merged[sym], reference=ref, source=src,
                              agrees=bool(abs(merged[sym] - ref) < 2e-3))
    return {"oncology": onco, "neurodegeneration": ndg,
            "cross_package_consistency": cross,
            "cross_all_agree": bool(cross) and all(v["agrees"] for v in cross.values()),
            "ok": bool(onco.get("ok") and ndg.get("ok"))}


def main():
    ap = argparse.ArgumentParser(description="Disease-class promoter gamma reception (NCBI-direct).")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: resolve coords + fetch + rebuild caches/atlases")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    if not v["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
