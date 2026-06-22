#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_signlaw_depmap.py  --  RECEPTION of the (B) SIGN-LAW '-' ARM held-out target (DepMap 24Q2 CRISPR KO).

WHAT THIS IS
  FV6 proved the (B) frontier PARTITIONS: every gamma-ORDERED prediction is non-identified (gamma ~ GC),
  and the ONLY (B) crossing that is BOTH identified (orthogonal to GC) AND firewall-clean (reads which SIGN
  corrects, never a dose) is the mechanism corrective-SIGN law (DM2: LOF -> '+' restore / GOF -> '-' silence).
  FV6's verdict was that its sole obstacle is bidirectional disease-correction DATA -- a '-' arm (does
  SILENCING a GOF gene move the cell toward healthy?) and a '+' arm (does RESTORING a LOF gene?).

  This module receives the '-' ARM target. A CRISPR-knockout viability screen applies the '-' (loss)
  operation to every gene; for a CANCER cell the resulting viability change IS a disease-correction phenotype
  (oncogene addiction: removing the oncogenic drive collapses the cancer program). So the sign-law '-' arm is
  directly testable: a GOF oncogene (corr_sign '-') should be a DEPENDENCY (knockout impairs the cancer =>
  negative gene-effect), while a LOF suppressor (corr_sign '+') should NOT be corrected by '-' (knockout is
  neutral or pro-tumour => gene-effect >= 0). The SEPARATION between the two classes UNDER THE SAME '-'
  operation is the sign-law signature visible in one screen.

  CRITICAL SCOPE (the right phenotype for the right disease class).
    Cancer-cell VIABILITY is a correction phenotype ONLY for the ONCOLOGY panel. For the NEURODEGENERATION
    panel the disease is neuronal proteinopathy/loss, NOT proliferation; knocking SOD1/VPS35 out of a cancer
    line kills it for housekeeping reasons unrelated to neurodegeneration. So the score is ON THE ONCO PANEL
    ONLY. The neurodegen gene-effects are cached for transparency but flagged out-of-readout-scope; the
    neurodegen/proteinopathy '-' arm needs a neuronal proteotoxicity-correction readout (still data-blocked),
    and the '+' RESTORE arm (over-expression of a suppressor) needs over-expression data (still data-blocked).

  This is a SIGN test (firewall-clean): the held-out gene-effect MAGNITUDES are the measured target; the kit
  reads only the DIRECTION of the GOF-vs-LOF separation, never predicts or claims a magnitude. corr_sign and
  GC are RE-READ FROZEN from inherited/onco_gamma.json at score time, never from this cache and never fitted.

HELD-OUT WARRANT
  The kit's corrective sign is forced by each gene's known disease MECHANISM (GOF/LOF), declared by function
  and frozen in the atlas BEFORE any DepMap data was consulted. DepMap CRISPR gene-effect is an independent
  functional viability readout that expresses none of that label, so it is a legitimate held-out target. No
  parameter, gamma, sign, or threshold is tuned to it.

IDENTIFICATION (why this is NOT the FV5 confound)
  The GC collinearity that makes every gamma-ORDERING score non-identified does NOT apply here: corr_sign is
  orthogonal to promoter GC (FV6: point-biserial(sign,GC) ~ +0.015), so the GOF and LOF groups carry nearly
  equal GC and the separation cannot be manufactured by GC. The engine re-checks this live (group GC balance
  + partialling GC out of the point-biserial) as part of FV7.

MODES
  (default, OFFLINE)  verify() : structural + provenance integrity of the cache, and recompute the ONCO
                                 '-'-arm headline (point-biserial(sign, -gene_effect) + exact-permutation p)
                                 FROM THE CACHE + the FROZEN atlas to confirm it reproduces the recorded
                                 result. Deterministic, no network, no numpy/scipy.
  --fetch  (ONLINE)   fetch()  : stream the DepMap CRISPRGeneEffect matrix from figshare, extract the matched
                                 panel columns, compute per-gene mean/median gene-effect across all models,
                                 and rebuild the cache. This is how the cache was built; not needed to
                                 reproduce. (~420 MB streamed; only the matched columns are retained.)

SOURCE
  DepMap, "DepMap 24Q2 Public" (Broad Institute). figshare article 25880521;
  CRISPRGeneEffect.csv (Chronos gene-effect; <= -0.5 ~ dependency, ~ -1 ~ common-essential), file id 46489063;
  Model.csv (cell-line metadata), file id 46489732. CRISPR KO screens: Project Achilles / Sanger SCORE.
"""
import os, sys, json, math, argparse, itertools

_HERE = os.path.dirname(os.path.abspath(__file__))
_BVAL = os.path.join(_HERE, "..", "bvalidation")
_CACHE = os.path.join(_BVAL, "depmap24q2_signlaw_heldout.cache.json")
_INH = os.path.join(_HERE, "..", "inherited")

_FIGSHARE_BASE = "https://ndownloader.figshare.com/files/"
_RELEASE = "DepMap 24Q2 Public"
_ARTICLE = "25880521"
_GENE_EFFECT_FILE = "46489063"          # CRISPRGeneEffect.csv (Chronos)
_MODEL_FILE = "46489732"                # Model.csv
_DEP_THRESHOLD = -0.5                   # DepMap convention: gene-effect < -0.5 ~ a dependency in that line
_ALIAS = {"GBA1": "GBA"}               # NCBI/atlas symbol -> DepMap matrix symbol

# the recorded ONCO '-'-arm headline (built by fetch(); verify() must reproduce it from the cache)
_HEADLINE_PB = 0.4940                   # point-biserial( corr_sign=='-' , -mean_gene_effect ) on the onco panel
_HEADLINE_P = 0.0227                    # exact one-sided permutation p (11440 sign-label assignments)
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


# ----------------------------------------------------------------------------- ONLINE rebuild
def fetch(workdir=None):
    """ONLINE: stream CRISPRGeneEffect.csv, extract the matched panel columns, summarise per gene, rebuild
    the cache. Anchor of this layer = the held-out warrant: corr_sign/gc are re-read frozen, never fitted to
    the downloaded gene-effects; the kit reads only the SIGN of the GOF-vs-LOF separation."""
    import urllib.request, re
    disease = _frozen_disease()
    want = {(_ALIAS.get(g, g)): g for g in disease}       # depmap symbol -> kit symbol

    url = _FIGSHARE_BASE + _GENE_EFFECT_FILE
    print("  streaming %s (CRISPRGeneEffect.csv, ~420 MB; only matched columns retained)" % url)
    req = urllib.request.urlopen(url, timeout=120)
    buf = b""; header = None; col_for = {}
    vals = {g: [] for g in want.values()}; n_models = 0
    CH = 1 << 20
    while True:
        chunk = req.read(CH)
        if not chunk:
            break
        buf += chunk
        while True:
            nl = buf.find(b"\n")
            if nl < 0:
                break
            line = buf[:nl].decode("utf-8", "replace"); buf = buf[nl + 1:]
            if header is None:
                header = line.split(",")
                for i, c in enumerate(header):
                    m = re.match(r"^([A-Za-z0-9\-\.]+)\s*\(", c.strip())
                    if m and m.group(1) in want:
                        col_for[i] = want[m.group(1)]
                continue
            f = line.split(",")
            if not f or not f[0]:
                continue
            n_models += 1
            for i, g in col_for.items():
                if i < len(f):
                    v = f[i]
                    if v not in ("", "NA"):
                        try:
                            vals[g].append(float(v))
                        except ValueError:
                            pass

    matched = {}
    for g, xs in vals.items():
        if not xs:
            continue
        xs_s = sorted(xs); n = len(xs)
        matched[g] = dict(gene=g, matched_as=_ALIAS.get(g, g),
                          disease_class=disease[g]["disease_class"],
                          mechanism=disease[g]["mechanism"], role=disease[g]["role"],
                          n_models=n,
                          mean_gene_effect=round(sum(xs) / n, 4),
                          median_gene_effect=round(xs_s[n // 2], 4),
                          frac_dependent=round(sum(1 for x in xs if x < _DEP_THRESHOLD) / n, 4))
    not_in_matrix = sorted(set(disease) - set(matched))
    cache = {
        "_what": ("VP Inheritance Kit -- (B) SIGN-LAW '-' ARM scoring sheet (held-out). Cached per-gene DepMap "
                  "CRISPR-KO gene-effect for the frozen disease panel, used to score the kit's mechanism-forced "
                  "corrective SIGN ('-' for GOF) against REAL cancer-dependency data. SIGN test only -- the "
                  "magnitudes are the target, never a kit prediction."),
        "_source": {"release": _RELEASE, "provider": "Broad Institute DepMap (Project Achilles / Sanger SCORE)",
                    "figshare_article": _ARTICLE, "gene_effect_file_id": _GENE_EFFECT_FILE,
                    "model_file_id": _MODEL_FILE,
                    "readout_column": "CRISPRGeneEffect (Chronos gene-effect; <= -0.5 ~ dependency, ~ -1 ~ common-essential)",
                    "n_models_screened": n_models},
        "_held_out_warrant": ("The kit's corrective SIGN is forced by each gene's disease MECHANISM (GOF/LOF), "
                              "declared by function and frozen in inherited/onco_gamma.json BEFORE any DepMap data "
                              "was seen. DepMap gene-effect is an independent functional viability readout that "
                              "expresses none of that label -- a legitimate held-out target. corr_sign/gc are "
                              "re-read frozen at score time; nothing is fitted to these numbers."),
        "_prediction_sign_locked": ("Sign-law '-' arm, locked BEFORE scoring: under the '-' (knockout) operation, a "
                                    "GOF gene (corr_sign '-') is CORRECTED ('-' removes the oncogenic drive => "
                                    "dependency, gene_effect < 0), while a LOF gene (corr_sign '+') is NOT corrected "
                                    "by '-' (knockout neutral/pro-tumour => gene_effect >= 0). Predicted: GOF more "
                                    "negative than LOF, i.e. point-biserial(corr_sign=='-', -gene_effect) > 0."),
        "_readout_scope": ("Cancer-cell viability is a CORRECTION phenotype ONLY for the ONCOLOGY panel. The "
                           "neurodegeneration rows are cached for transparency but are OUT OF READOUT SCOPE for this "
                           "test (a cancer-viability screen does not measure neuronal proteinopathy correction); the "
                           "engine (FV7) scores the ONCO panel only."),
        "_dependency_threshold": _DEP_THRESHOLD,
        "_panel_rule": "The two frozen disease atlases (onco + neurodegen), declared by function; gene-effect matched by official symbol (GBA1->GBA).",
        "_genes_not_in_depmap_matrix": not_in_matrix,
        "matched": {g: matched[g] for g in sorted(matched)},
    }
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("  cache rebuilt: %d matched genes (%d models); not in matrix: %s"
          % (len(matched), n_models, not_in_matrix or "none"))
    return verify()


# ----------------------------------------------------------------------------- OFFLINE verify (default)
def verify():
    """OFFLINE: provenance + structural integrity, and recompute the ONCO '-'-arm headline from the cache +
    the FROZEN atlas (corr_sign/gc re-read live, never from the cache). Deterministic; no network/numpy."""
    if not os.path.exists(_CACHE):
        return {"ok": False, "reason": "sign-law DepMap cache absent -- run with --fetch once (network)"}
    cache = json.load(open(_CACHE, encoding="utf-8"))
    src = cache.get("_source", {})
    prov_ok = (src.get("figshare_article") == _ARTICLE
               and src.get("gene_effect_file_id") == _GENE_EFFECT_FILE
               and "gene-effect" in src.get("readout_column", "").lower())
    warrant_ok = ("MECHANISM" in cache.get("_held_out_warrant", "")
                  and "frozen" in cache.get("_held_out_warrant", ""))
    sign_locked = ("point-biserial(corr_sign=='-', -gene_effect) > 0" in cache.get("_prediction_sign_locked", ""))
    scope_ok = ("ONCOLOGY panel" in cache.get("_readout_scope", ""))

    disease = _frozen_disease()                                 # corr_sign + gc re-read FROZEN
    rows = cache.get("matched", {})
    struct_ok = all(all(k in r for k in ("gene", "disease_class", "mean_gene_effect", "n_models")) for r in rows.values())

    # the cache must not smuggle a sign/gc -- it carries gene-effects only; the engine/verify re-read the frozen atlas.
    no_smuggled = all(("corr_sign" not in r and "gc" not in r and "gamma" not in r) for r in rows.values())

    # recompute the ONCO '-'-arm headline FROM THE CACHE + FROZEN atlas
    onco = [g for g, r in rows.items() if r["disease_class"] == "oncology"]
    onco.sort()
    ind = [1.0 if disease[g]["corr_sign"] == "-" else 0.0 for g in onco]     # GOF indicator (frozen sign)
    negge = [-rows[g]["mean_gene_effect"] for g in onco]                      # -gene_effect (cache target)
    pb = round(_pearson(ind, negge), 4)
    p, ntot, _ = _exact_perm_p(ind, negge)
    p = round(p, 4)
    headline_ok = bool(abs(pb - _HEADLINE_PB) < 1e-3 and abs(p - _HEADLINE_P) < 2e-3 and len(onco) == _HEADLINE_N_ONCO)

    out = {
        "provenance_ok": bool(prov_ok), "held_out_warrant_ok": bool(warrant_ok),
        "prediction_sign_locked_ok": bool(sign_locked), "readout_scope_ok": bool(scope_ok),
        "structure_ok": bool(struct_ok), "no_smuggled_sign_or_gc": bool(no_smuggled),
        "n_onco_scored": len(onco), "n_neurodegen_out_of_scope": sum(1 for r in rows.values() if r["disease_class"] == "neurodegeneration"),
        "point_biserial_sign_minus_vs_neg_gene_effect": pb,
        "exact_permutation_p_one_sided": p, "n_permutations": ntot,
        "headline_reproduced": headline_ok,
        "genes_not_in_depmap_matrix": cache.get("_genes_not_in_depmap_matrix", []),
    }
    out["ok"] = bool(prov_ok and warrant_ok and sign_locked and scope_ok and struct_ok and no_smuggled and headline_ok)
    return out


def main():
    ap = argparse.ArgumentParser(description="(B) sign-law '-' arm held-out target reception (DepMap 24Q2 CRISPR KO).")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: stream DepMap gene-effect + rebuild cache")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    if not v["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
