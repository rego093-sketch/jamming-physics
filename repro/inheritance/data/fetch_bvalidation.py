#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_bvalidation.py  --  RECEPTION of the (B) HELD-OUT validation target (Replogle 2022 CRISPRi).

WHAT THIS IS
  The (B) score (engine/feasibility_validation.py) needs a MEASURED, genuinely held-out pre/post
  expression target to score the kit's no-tuning (A)-map gamma-ordering against. It receives that target
  from the Replogle et al. 2022 Cell genome-scale Perturb-seq (CRISPRi) resource and vendors ONLY the
  small matched-panel slice (the genes that intersect the kit's frozen gamma atlases) into
  bvalidation/replogle2022_heldout.cache.json. The expression numbers are stored VERBATIM from the public
  source; the kit never fits anything to them -- it scores frozen predictions against them.

HELD-OUT WARRANT
  The kit's gamma is measured PURELY from promoter DNA thermodynamics (NN-stacking dG37, SantaLucia 1998,
  GRCh38 TSS-2000..+500) and was frozen before any expression data was consulted. The CRISPRi readout
  (obs/fold_expr = on-target fraction of transcript remaining) expresses none of that information, so it
  is a legitimate held-out target. No parameter or gamma is tuned to it.

MODES
  (default, OFFLINE)  verify() : structural + provenance integrity of the cache, and recompute the
                                 headline Spearman rho on the primary set FROM THE CACHE to confirm it
                                 reproduces the recorded (B) result. Deterministic, no network, no numpy.
  --fetch  (ONLINE)   fetch()  : download the Replogle pseudobulk .h5ad files from figshare, parse the
                                 on-target fold_expr per perturbation, match to the frozen atlases by the
                                 fixed union rule, and rebuild the cache. This is how the cache was built;
                                 not needed to reproduce. (Requires h5py + ~540 MB download.)

SOURCE
  Replogle et al., "Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq",
  Cell 185(14):2559-2575 (2022). DOI 10.1016/j.cell.2022.05.013. figshare article 20029387.
"""
import os, sys, json, math, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
_BVAL = os.path.join(_HERE, "..", "bvalidation")
_CACHE = os.path.join(_BVAL, "replogle2022_heldout.cache.json")
_INH = os.path.join(_HERE, "..", "inherited")

# figshare file ids (article 20029387). Direct: https://ndownloader.figshare.com/files/{id}
_FIGSHARE_BASE = "https://ndownloader.figshare.com/files/"
_DATASETS = [
    # (label, file_id, cell_line, description)
    ("K562_GWPS",      "35773217", "K562", "genome-wide Perturb-seq (primary, pre-registered)"),
    ("RPE1",           "35775512", "RPE1", "RPE1 essential-gene Perturb-seq (robustness, 2nd cell line)"),
    ("K562_essential", "35780870", "K562", "K562 essential-gene Perturb-seq (robustness)"),
]
_ATLAS_FILES = [("neuro", "neuro_gamma.json"), ("onco", "onco_gamma.json"),
                ("neurodegen", "neurodegen_gamma.json"), ("rna", "rna_carrier_gamma.json"),
                ("imprint", "imprint_gamma.json"), ("germline", "germline_gamma.json"),
                ("immune", "immune_gamma.json")]
_ALIAS = {"GBA1": "GBA"}
_DOI = "10.1016/j.cell.2022.05.013"
_ARTICLE = "20029387"


# ----------------------------------------------------------------------------- compact pure-python stats
def _rankdata(a):
    idx = sorted(range(len(a)), key=lambda i: a[i])
    ranks = [0.0] * len(a)
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and a[idx[j + 1]] == a[idx[i]]:
            j += 1
        r = 0.5 * (i + j) + 1.0
        for k in range(i, j + 1):
            ranks[idx[k]] = r
        i = j + 1
    return ranks


def _spearman_rho(x, y):
    n = len(x)
    if n < 3:
        return float("nan")
    rx = _rankdata(x); ry = _rankdata(y)
    mx = sum(rx) / n; my = sum(ry) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx); syy = sum((b - my) ** 2 for b in ry)
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def _frozen_gamma():
    gamma = {}
    for _, fn in _ATLAS_FILES:
        d = json.load(open(os.path.join(_INH, fn), encoding="utf-8"))
        genes = d.get("genes", d)
        for g, v in genes.items():
            if isinstance(v, dict) and "gamma" in v and g not in gamma:
                gamma[g] = round(float(v["gamma"]), 4)
    return gamma


# ----------------------------------------------------------------------------- ONLINE rebuild
def _download(file_id, dest, timeout=600):
    import urllib.request
    url = _FIGSHARE_BASE + file_id
    print("  downloading %s -> %s" % (url, os.path.basename(dest)))
    urllib.request.urlretrieve(url, dest)
    return dest


def fetch(workdir=None):
    """ONLINE: download the Replogle pseudobulk, parse on-target fold_expr, rebuild the cache. Anchor of
    this layer = the held-out warrant: gamma is re-read frozen, never fitted to the downloaded numbers."""
    import h5py  # only needed for the (rare) rebuild
    workdir = workdir or os.path.join(_HERE, "..", "_bval_download")
    os.makedirs(workdir, exist_ok=True)
    gamma = _frozen_gamma()
    cache_datasets = {}
    for label, fid, cell, desc in _DATASETS:
        fn = os.path.join(workdir, "%s.h5ad" % label)
        if not os.path.exists(fn):
            _download(fid, fn)
        f = h5py.File(fn, "r")
        pert = [x.decode() for x in f["obs/gene_transcript"][:]]
        fold = list(f["obs/fold_expr"][:]); ctrl = list(f["obs/control_expr"][:])
        f.close()
        s2f = {}; n_pert = 0; n_nt = 0; finite_fold = []
        for p, fo, ce in zip(pert, fold, ctrl):
            if "NON-TARGETING" in p.upper():
                n_nt += 1; continue
            n_pert += 1
            if fo == fo:  # finite
                finite_fold.append(float(fo))
                s2f[p.split("_")[1]] = (float(fo), float(ce))
        med = sorted(finite_fold)[len(finite_fold) // 2] if finite_fold else float("nan")
        matched = []
        for g, gv in gamma.items():
            key = g if g in s2f else _ALIAS.get(g, "")
            if key in s2f:
                fo, ce = s2f[key]
                matched.append(dict(gene=g, gamma=gv, matched_as=(g if g in s2f else key),
                                    fold_expr=round(fo, 6), control_expr=round(ce, 6)))
        matched.sort(key=lambda r: (r["gamma"], r["gene"]))
        cache_datasets[label] = dict(figshare_file_id=fid, cell_line=cell, description=desc,
                                     n_perturbations_total=n_pert, n_nontargeting_excluded=n_nt,
                                     dataset_median_fold_expr=round(med, 6),
                                     n_matched=len(matched), matched=matched)
        print("  %-16s matched n=%d" % (label, len(matched)))
    cache = json.load(open(_CACHE, encoding="utf-8")) if os.path.exists(_CACHE) else {}
    cache["datasets"] = cache_datasets
    cache["_panel_size"] = len(gamma)
    json.dump(cache, open(_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("  cache rebuilt (%d datasets)." % len(cache_datasets))
    return verify()


# ----------------------------------------------------------------------------- OFFLINE verify (default)
def verify():
    """OFFLINE: provenance + structural integrity, and recompute the headline (B) Spearman from the cache."""
    if not os.path.exists(_CACHE):
        return {"ok": False, "reason": "bvalidation cache absent -- run with --fetch once (network + h5py)"}
    cache = json.load(open(_CACHE, encoding="utf-8"))
    src = cache.get("_source", {})
    prov_ok = (src.get("doi") == _DOI and src.get("figshare_article") == _ARTICLE
               and "fold_expr" in src.get("readout_column", ""))
    warrant_ok = ("DNA" in cache.get("_held_out_warrant", ""))
    sign_ok = ("rho(gamma, fold_expr) > 0" in cache.get("_prediction_sign_locked", ""))
    panel_ok = ("union" in cache.get("_panel_rule", "").lower())

    # structural: every dataset's matched rows are well-formed and counted correctly
    struct_ok = True
    ds_summary = {}
    for label, ds in cache.get("datasets", {}).items():
        rows = ds.get("matched", [])
        well_formed = all(all(k in r for k in ("gene", "gamma", "fold_expr", "control_expr")) for r in rows)
        count_ok = (ds.get("n_matched") == len(rows))
        struct_ok &= bool(well_formed and count_ok)
        ds_summary[label] = {"n_matched": len(rows), "count_ok": bool(count_ok),
                             "well_formed": bool(well_formed)}

    # recompute the headline Spearman on the primary set FROM THE CACHE (self-consistency to the record)
    headline_ok = None; rho_primary = None
    prim = cache.get("datasets", {}).get("K562_GWPS")
    if prim:
        rows = sorted(prim["matched"], key=lambda r: (r["gamma"], r["gene"]))
        G = [float(r["gamma"]) for r in rows]; F = [float(r["fold_expr"]) for r in rows]
        rho_primary = round(_spearman_rho(G, F), 4)
        # the recorded (B) headline is rho = -0.0760 at n = 43
        headline_ok = bool(abs(rho_primary - (-0.0760)) < 1e-3 and len(rows) == 43)

    out = {
        "provenance_ok": bool(prov_ok), "held_out_warrant_ok": bool(warrant_ok),
        "prediction_sign_locked_ok": bool(sign_ok), "panel_rule_ok": bool(panel_ok),
        "structure_ok": bool(struct_ok), "datasets": ds_summary,
        "primary_spearman_rho_from_cache": rho_primary, "n_primary": (len(prim["matched"]) if prim else 0),
        "headline_reproduced": headline_ok,
        "n": cache.get("_panel_size"),
    }
    out["ok"] = bool(prov_ok and warrant_ok and sign_ok and panel_ok and struct_ok and headline_ok)
    return out


def main():
    ap = argparse.ArgumentParser(description="(B) held-out validation target reception (Replogle 2022).")
    ap.add_argument("--fetch", action="store_true", help="ONLINE: download figshare pseudobulk + rebuild cache")
    a = ap.parse_args()
    if a.fetch:
        fetch()
    v = verify()
    print(json.dumps(v, ensure_ascii=False, indent=2))
    if not v["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
