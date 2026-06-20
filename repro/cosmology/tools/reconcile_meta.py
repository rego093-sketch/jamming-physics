#!/usr/bin/env python3
"""
reconcile_meta.py  —  VP_SPEC v1.8 / Constitution C1 (max reproducibility)

The manifest (manifest/cosmology.csv) is the authoritative post-v2.1 source of
per-chapter counts. docs/cosmology/_meta.json is a derived display artifact and
MUST agree with it (the v1.8 gate compares displayed vs regenerated values).

This tool rewrites, for every chapter row in _meta.json, the words / eq_inline /
eq_display fields from the manifest (matched by slug), then recomputes
totals.words and totals.eq (= sum eq_inline + sum eq_display). figures/tables
totals are taken from the manifest sums. All other _meta fields (one_liner,
grade, title, ordering, abstract, headline_results, ...) are preserved verbatim.

Idempotent. Run with --check to verify agreement without writing.
"""
import json, csv, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
META = ROOT / "docs" / "cosmology" / "_meta.json"
MANIFEST = ROOT / "manifest" / "cosmology.csv"


def load_manifest():
    rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8")))
    by_slug = {}
    sums = {"words": 0, "eq_inline": 0, "eq_display": 0, "figures": 0, "tables": 0}
    for r in rows:
        slug = r["slug"].strip()
        rec = {k: int(float(r[k])) for k in
               ("words", "eq_inline", "eq_display", "figures", "tables")}
        by_slug[slug] = rec
        for k in sums:
            sums[k] += rec[k]
    return by_slug, sums


def reconcile(check=False):
    meta = json.load(open(META, encoding="utf-8"))
    by_slug, sums = load_manifest()
    diffs = []

    for ch in meta["chapters"]:
        slug = ch["slug"]
        if slug not in by_slug:
            diffs.append(f"  [!] chapter slug not in manifest: {slug}")
            continue
        src = by_slug[slug]
        for k in ("words", "eq_inline", "eq_display"):
            old = ch.get(k)
            new = src[k]
            if old != new:
                diffs.append(f"  ch {ch['code']} {k}: {old} -> {new}")
                if not check:
                    ch[k] = new

    new_totals = {
        "words": sums["words"],
        "eq": sums["eq_inline"] + sums["eq_display"],
        "figures": sums["figures"],
        "tables": sums["tables"],
    }
    for k, v in new_totals.items():
        old = meta["totals"].get(k)
        if old != v:
            diffs.append(f"  totals.{k}: {old} -> {v}")
            if not check:
                meta["totals"][k] = v

    if check:
        if diffs:
            print("DRIFT (meta vs manifest):")
            print("\n".join(diffs))
            return 1
        print("OK: _meta.json agrees with manifest")
        return 0

    if diffs:
        json.dump(meta, open(META, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        open(META, "a", encoding="utf-8").write("\n")
        print("reconciled _meta.json:")
        print("\n".join(diffs))
    else:
        print("no changes (already reconciled)")
    return 0


if __name__ == "__main__":
    sys.exit(reconcile(check="--check" in sys.argv))
