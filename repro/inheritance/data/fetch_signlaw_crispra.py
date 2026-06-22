#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_signlaw_crispra.py  --  RECEPTION of the (B) SIGN-LAW '+' RESTORE ARM held-out target
                              (Horlbeck 2016 genome-scale CRISPRa growth screen, hCRISPRa-v2, K562).

WHAT THIS IS
  FV6 proved the (B) frontier PARTITIONS: every gamma-ORDERED prediction is non-identified (gamma ~ GC),
  and the ONLY (B) crossing that is BOTH identified (orthogonal to GC) AND firewall-clean (reads which SIGN
  corrects, never a dose) is the mechanism corrective-SIGN law (DM2: LOF -> '+' restore / GOF -> '-' silence).
  FV6's verdict was that its sole obstacle is bidirectional disease-correction DATA -- a '-' arm (does
  SILENCING a GOF gene move the cell toward healthy?) and a '+' arm (does RESTORING a LOF gene?). FV7
  (v0.17.0) scored the '-' arm on DepMap CRISPR-KO. This module receives the COMPLEMENTARY '+' ARM target.

  A CRISPR-ACTIVATION (CRISPRa) viability screen applies the '+' (gain / restore) operation to every gene
  from its own promoter; for a CANCER cell the resulting growth change IS a disease-correction phenotype
  for a LOF suppressor (restoring a tumour brake slows the cancer program). So the sign-law '+' arm is
  directly testable as a SEPARATION under one operation: a LOF suppressor (corr_sign '+') should be
  CORRECTED by '+' (activation slows growth => NEGATIVE growth phenotype), while a GOF oncogene (corr_sign
  '-') should NOT be corrected by '+' (activating an already-active driver is neutral / pro-growth =>
  growth phenotype >= 0). The SEPARATION between the two classes UNDER THE SAME '+' operation is the
  sign-law signature visible in one screen -- the mirror image of FV7's '-' arm.

  This is the natural ACTIVATION-MODE counterpart to FV7's loss screen: where DepMap/Achilles delivers a
  genome-scale loss-of-function dependency map, Horlbeck 2016 hCRISPRa-v2 is the canonical genome-scale
  gain-of-function (activation) growth screen. Both the predecessor Gilbert 2014 CRISPRa screen and this
  one independently reported that the genes whose ACTIVATION most slows growth are tumour suppressors --
  exactly the '+' arm signal -- so it is the pre-registerable target for the '+' arm (NOT cherry-picked).

  CRITICAL SCOPE (the right phenotype for the right disease class).
    Cancer-cell GROWTH is a correction phenotype ONLY for the ONCOLOGY panel. For the NEURODEGENERATION
    panel the disease is neuronal proteinopathy/loss, NOT proliferation; activating PRKN/PINK1 in a leukemia
    line does not measure neurodegeneration correction. So the score is ON THE ONCO PANEL ONLY. The
    neurodegen rows are cached for transparency but flagged out-of-readout-scope; the neurodegen/
    proteinopathy '+' arm needs a neuronal proteotoxicity-correction readout (still data-blocked).

  This is a SIGN test (firewall-clean): the held-out growth-phenotype MAGNITUDES are the measured target;
  the kit reads only the DIRECTION of the LOF-vs-GOF separation, never predicts or claims a magnitude.
  corr_sign and GC are RE-READ FROZEN from inherited/onco_gamma.json at score time, never from this cache
  and never fitted.

HELD-OUT WARRANT
  The kit's corrective sign is forced by each gene's known disease MECHANISM (GOF/LOF), declared by function
  and frozen in the atlas BEFORE any CRISPRa data was consulted. The CRISPRa K562 growth phenotype is an
  independent functional viability readout that expresses none of that label, so it is a legitimate held-out
  target. No parameter, gamma, sign, or threshold is tuned to it.

IDENTIFICATION (why this is NOT the FV5 confound)
  The GC collinearity that makes every gamma-ORDERING score non-identified does NOT apply here: corr_sign is
  orthogonal to promoter GC (FV6: point-biserial(sign,GC) ~ +0.015), so the GOF and LOF groups carry nearly
  equal GC and the separation cannot be manufactured by GC. The engine re-checks this live (group GC balance
  + partialling GC out of the point-biserial) as part of FV8.

HONEST CAVEATS (recorded, never tuned around)
  K562 is a single chronic-myeloid-leukemia line, and the '+' arm is therefore a SINGLE-LINE growth screen
  (the canonical genome-scale CRISPRa screen), whereas FV7's '-' arm was a pan-cancer mean across ~1100
  DepMap lines. Several panel suppressors are inactivatable in K562 -- TP53 is null and CDKN2A is deleted in
  K562, so CRISPRa has a weak/absent endogenous locus to restore -- and they push AGAINST the prediction
  (conservative, like FV7's pan-essential LOF genes). The score is reported as it falls with these headwinds.

MODES
  (default, OFFLINE)  verify() : structural + provenance integrity of the cache, and recompute the ONCO
                                 '+'-arm headline (point-biserial(corr_sign=='+', -growth_phenotype) +
                                 exact-permutation p) FROM THE CACHE + the FROZEN atlas to confirm it
                                 reproduces the recorded result. Deterministic, no network, no numpy/scipy.
  --fetch  (ONLINE)   fetch()  : download Supplementary file 10 (hCRISPRa-v2 K562 gene growth phenotypes)
                                 from the eLife CDN, extract the matched panel rows (ave-of-replicates
                                 'average phenotype of strongest 3' + Mann-Whitney p), and rebuild the
                                 cache. Pure-stdlib .xlsx reader (zipfile + ElementTree) -- no new dependency.

SOURCE
  Horlbeck, Gilbert, Villalta, Adamson, ... Weissman (2016), "Compact and highly active next-generation
  libraries for CRISPR-mediated gene repression and activation", eLife 5:e19760, DOI 10.7554/eLife.19760.
  Supplementary file 10: "Gene growth phenotypes and p-values for hCRISPRa-v2 screens performed in K562."
  Growth phenotype = log2 sgRNA enrichment per cell doubling (gamma_growth), averaged over the strongest 3
  sgRNAs / gene and over two replicates; NEGATIVE => activation slows growth.
"""
import os, sys, json, math, argparse, itertools

_HERE = os.path.dirname(os.path.abspath(__file__))
_BVAL = os.path.join(_HERE, "..", "bvalidation")
_CACHE = os.path.join(_BVAL, "crispra_horlbeck2016_signlaw_heldout.cache.json")
_INH = os.path.join(_HERE, "..", "inherited")

# eLife CDN supplementary file (Version of Record, v2). Supplementary file 10 = K562 hCRISPRa-v2 growth.
_SUPP_URL = "https://cdn.elifesciences.org/articles/19760/elife-19760-supp10-v2.xlsx"
_DOI = "10.7554/eLife.19760"
_ARTICLE = "19760"
_SUPP = "supp10"
# CRISPRa table older-symbol aliases (atlas symbol -> CRISPRa-table symbol). ONCO needs none.
_ALIAS = {"GBA1": "GBA", "PRKN": "PARK2"}
# growth-suppressive cut for the per-gene transparency tally (NOT a fitted threshold; a sign read only)
_SUPPRESSIVE = 0.0

# the recorded ONCO '+'-arm headline (built by fetch(); verify() must reproduce it from the cache)
_HEADLINE_PB = 0.4852                   # point-biserial( corr_sign=='+' , -growth_phenotype ) on the onco panel
_HEADLINE_P = 0.0274                    # exact one-sided permutation p (11440 sign-label assignments)
_HEADLINE_N_ONCO = 16


# ----------------------------------------------------------------------------- compact pure-python stats
def _pearson(a, b):
    """Pearson r; equals the point-biserial coefficient when one input is a +-1 sign / 0-1 indicator."""
    n = len(a)
    if n < 2:
        return float("nan")
    ma = sum(a) / n; mb = sum(b) / n
    sab = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    saa = sum((x - ma) ** 2 for x in a); sbb = sum((y - mb) ** 2 for y in b)
    return sab / math.sqrt(saa * sbb) if saa > 0 and sbb > 0 else 0.0


def _exact_perm_p(ind, val):
    """Exact one-sided permutation p for point-biserial(ind, val): over ALL C(n,k) ways to place the k
    indicator-1 labels, the fraction whose point-biserial >= the observed. k = #(ind==1). Deterministic."""
    n = len(ind); k = int(round(sum(ind)))
    obs = _pearson(ind, val)
    base = [0.0] * n; idx = list(range(n))
    ng = 0; nt = 0
    for comb in itertools.combinations(idx, k):
        perm = base[:]
        for i in comb:
            perm[i] = 1.0
        nt += 1
        if _pearson(perm, val) >= obs - 1e-12:
            ng += 1
    return (ng / nt if nt else float("nan")), nt, obs


def _frozen_disease():
    """The frozen ONCO + NEURODEGEN panel: {gene: {gamma, gc, role, mechanism, corr_sign, disease_class}}.
    Read directly from the measured atlases; nothing is fitted. corr_sign/gc are re-read here only to TAG the
    cache rows by class -- the SCORE in the engine re-reads them independently from the same frozen atlases."""
    out = {}
    for fn, cls in (("onco_gamma.json", "oncology"), ("neurodegen_gamma.json", "neurodegeneration")):
        d = json.load(open(os.path.join(_INH, fn), encoding="utf-8"))["genes"]
        for g, v in d.items():
            out[g] = dict(gamma=round(float(v["gamma"]), 4), gc=round(float(v["gc"]), 4),
                          role=v["role"], mechanism=v["mechanism"], corr_sign=v["corr_sign"],
                          disease_class=cls)
    return out


# ----------------------------------------------------------------------------- minimal stdlib .xlsx reader
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _col_index(cellref):
    """'A12' -> 0, 'K3' -> 10, 'L7' -> 11 (0-indexed spreadsheet column)."""
    import re
    letters = re.match(r"([A-Z]+)", cellref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _xlsx_rows(path):
    """Yield {col_index: value} per row of the first worksheet. Pure stdlib (zipfile + ElementTree); resolves
    shared strings and inline strings, parses numbers as float. No openpyxl / pandas dependency."""
    import zipfile, xml.etree.ElementTree as ET
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in root.findall(f"{_NS}si"):
            shared.append("".join(t.text or "" for t in si.iter(f"{_NS}t")))
    root = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    sd = root.find(f"{_NS}sheetData")
    for row in sd.findall(f"{_NS}row"):
        cells = {}
        for c in row.findall(f"{_NS}c"):
            ref = c.get("r"); t = c.get("t")
            if ref is None:
                continue
            ci = _col_index(ref)
            v = c.find(f"{_NS}v"); iss = c.find(f"{_NS}is")
            if t == "s":
                cells[ci] = shared[int(v.text)] if v is not None else ""
            elif t == "inlineStr" and iss is not None:
                cells[ci] = "".join(x.text or "" for x in iss.iter(f"{_NS}t"))
            else:
                cells[ci] = float(v.text) if (v is not None and v.text not in (None, "")) else None
        yield cells


# ----------------------------------------------------------------------------- ONLINE rebuild
def fetch(workdir=None):
    """ONLINE: download Supplementary file 10 (.xlsx), extract the matched panel rows, rebuild the cache.
    Anchor of this layer = the held-out warrant: corr_sign/gc are re-read frozen, never fitted to the
    downloaded growth phenotypes; the kit reads only the SIGN of the LOF-vs-GOF separation."""
    import urllib.request, tempfile
    disease = _frozen_disease()
    want = {(_ALIAS.get(g, g)): g for g in disease}        # crispra-table symbol -> kit symbol

    print("  downloading %s (eLife supp10, hCRISPRa-v2 K562 gene growth phenotypes)" % _SUPP_URL)
    fd, tmp = tempfile.mkstemp(suffix=".xlsx"); os.close(fd)
    urllib.request.urlretrieve(_SUPP_URL, tmp)

    # column layout (Table S10): A=gene; ave_Rep1_Rep2 block -> J transcripts, K Mann-Whitney p, L avg phenotype of strongest 3
    GENE_COL, MWP_COL, GROWTH_COL = 0, 10, 11
    rows_seen = 0
    matched = {}
    for cells in _xlsx_rows(tmp):
        g = cells.get(GENE_COL)
        if not isinstance(g, str):
            continue
        rows_seen += 1
        if g in want:
            kit = want[g]
            gp = cells.get(GROWTH_COL); mp = cells.get(MWP_COL)
            if gp is None:
                continue
            matched[kit] = dict(gene=kit, matched_as=g,
                                disease_class=disease[kit]["disease_class"],
                                mechanism=disease[kit]["mechanism"], role=disease[kit]["role"],
                                growth_phenotype=round(float(gp), 6),
                                mann_whitney_p=(round(float(mp), 6) if mp is not None else None))
    os.remove(tmp)
    not_in_table = sorted(set(disease) - set(matched))

    cache = {
        "_what": ("VP Inheritance Kit -- (B) SIGN-LAW '+' RESTORE ARM scoring sheet (held-out). Cached per-gene "
                  "hCRISPRa-v2 K562 growth phenotype for the frozen disease panel, used to score the kit's "
                  "mechanism-forced corrective SIGN ('+' for LOF) against REAL CRISPR-activation growth data. "
                  "SIGN test only -- the magnitudes are the target, never a kit prediction."),
        "_source": {"citation": "Horlbeck et al. 2016, eLife 5:e19760", "provider": "Weissman lab (UCSF)",
                    "doi": _DOI, "elife_article": _ARTICLE, "supplementary_file": _SUPP,
                    "url": _SUPP_URL,
                    "readout_column": ("ave_Rep1_Rep2 'average phenotype of strongest 3' = gene growth "
                                       "phenotype (log2 sgRNA enrichment per cell doubling); negative => "
                                       "activation slows growth"),
                    "cell_line": "K562 (CML), SunTag-VP64 CRISPRa", "n_replicates": 2,
                    "n_table_gene_rows": rows_seen},
        "_held_out_warrant": ("The kit's corrective SIGN is forced by each gene's disease MECHANISM (GOF/LOF), "
                              "declared by function and frozen in inherited/onco_gamma.json BEFORE any CRISPRa "
                              "data was seen. The CRISPRa K562 growth phenotype is an independent functional "
                              "viability readout that expresses none of that label -- a legitimate held-out "
                              "target. corr_sign/gc are re-read frozen at score time; nothing is fitted to "
                              "these numbers."),
        "_prediction_sign_locked": ("Sign-law '+' arm, locked BEFORE scoring: under the '+' (CRISPR-activation) "
                                    "operation, a LOF gene (corr_sign '+') is CORRECTED ('+' restores the tumour "
                                    "brake => activation slows growth, growth_phenotype < 0), while a GOF gene "
                                    "(corr_sign '-') is NOT corrected by '+' (activating an active driver is "
                                    "neutral/pro-growth => growth_phenotype >= 0). Predicted: LOF more negative "
                                    "than GOF, i.e. point-biserial(corr_sign=='+', -growth_phenotype) > 0."),
        "_readout_scope": ("Cancer-cell GROWTH is a CORRECTION phenotype ONLY for the ONCOLOGY panel. The "
                           "neurodegeneration rows are cached for transparency but are OUT OF READOUT SCOPE for "
                           "this test (a leukemia growth screen does not measure neuronal proteinopathy "
                           "correction); the engine (FV8) scores the ONCO panel only."),
        "_honest_caveats": ("K562 is a single CML line (the '+' arm is a single-line growth screen, vs FV7's "
                            "pan-cancer mean). TP53 is null and CDKN2A is deleted in K562, so CRISPRa has a "
                            "weak/absent endogenous locus to restore for those and they push AGAINST the "
                            "prediction (conservative panel, no cherry-picking)."),
        "_panel_rule": ("The two frozen disease atlases (onco + neurodegen), declared by function; growth "
                        "phenotype matched by gene symbol (older-symbol aliases GBA1->GBA, PRKN->PARK2)."),
        "_genes_not_in_crispra_table": not_in_table,
        "matched": {g: matched[g] for g in sorted(matched)},
    }
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("  cache rebuilt: %d matched genes (%d table rows); not in table: %s"
          % (len(matched), rows_seen, not_in_table or "none"))
    return verify()


# ----------------------------------------------------------------------------- OFFLINE verify (default)
def verify():
    """OFFLINE: provenance + structural integrity, and recompute the ONCO '+'-arm headline from the cache +
    the FROZEN atlas (corr_sign/gc re-read live, never from the cache). Deterministic; no network/numpy."""
    if not os.path.exists(_CACHE):
        return {"ok": False, "reason": "sign-law CRISPRa cache absent -- run with --fetch once (network)"}
    cache = json.load(open(_CACHE, encoding="utf-8"))
    src = cache.get("_source", {})
    prov_ok = (src.get("doi") == _DOI and src.get("elife_article") == _ARTICLE
               and "growth phenotype" in src.get("readout_column", "").lower())
    warrant_ok = ("MECHANISM" in cache.get("_held_out_warrant", "")
                  and "frozen" in cache.get("_held_out_warrant", ""))
    sign_locked = ("point-biserial(corr_sign=='+', -growth_phenotype) > 0" in cache.get("_prediction_sign_locked", ""))
    scope_ok = ("ONCOLOGY panel" in cache.get("_readout_scope", ""))

    disease = _frozen_disease()                                 # corr_sign + gc re-read FROZEN
    rows = cache.get("matched", {})
    struct_ok = all(all(k in r for k in ("gene", "disease_class", "growth_phenotype")) for r in rows.values())

    # the cache must not smuggle a sign/gc/gamma -- it carries growth phenotypes only; the engine/verify re-read the frozen atlas
    no_smuggled = all(("corr_sign" not in r and "gc" not in r and "gamma" not in r) for r in rows.values())

    # recompute the ONCO '+'-arm headline FROM THE CACHE + FROZEN atlas
    onco = [g for g, r in rows.items() if r["disease_class"] == "oncology"]
    onco.sort()
    ind = [1.0 if disease[g]["corr_sign"] == "+" else 0.0 for g in onco]    # LOF suppressor indicator (frozen sign)
    neg_growth = [-rows[g]["growth_phenotype"] for g in onco]               # -growth_phenotype (cache target)
    pb = round(_pearson(ind, neg_growth), 4)
    p, ntot, _ = _exact_perm_p(ind, neg_growth)
    p = round(p, 4)
    headline_ok = bool(abs(pb - _HEADLINE_PB) < 1e-3 and abs(p - _HEADLINE_P) < 2e-3 and len(onco) == _HEADLINE_N_ONCO)

    out = {
        "provenance_ok": bool(prov_ok), "held_out_warrant_ok": bool(warrant_ok),
        "prediction_sign_locked_ok": bool(sign_locked), "readout_scope_ok": bool(scope_ok),
        "structure_ok": bool(struct_ok), "no_smuggled_sign_or_gc": bool(no_smuggled),
        "n_onco_scored": len(onco), "n_neurodegen_out_of_scope": sum(1 for r in rows.values() if r["disease_class"] == "neurodegeneration"),
        "point_biserial_sign_plus_vs_neg_growth": pb,
        "exact_permutation_p_one_sided": p, "n_permutations": ntot,
        "headline_reproduced": headline_ok,
        "genes_not_in_crispra_table": cache.get("_genes_not_in_crispra_table", []),
    }
    out["ok"] = bool(prov_ok and warrant_ok and sign_locked and scope_ok and struct_ok and no_smuggled and headline_ok)
    return out


def main():
    ap = argparse.ArgumentParser(description="(B) sign-law '+' RESTORE arm held-out target reception (Horlbeck 2016 CRISPRa K562).")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: download eLife supp10 + rebuild cache")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    if not v["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
