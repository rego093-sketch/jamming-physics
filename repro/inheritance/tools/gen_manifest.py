#!/usr/bin/env python3
"""Deterministic regenerator for manifest/kit_manifest.csv.

Walks every tracked file in the kit (excluding __pycache__ and the manifest
itself), recomputes byte length + sha256, and preserves the human-written
`description` column by path. New paths get a derived description. Output is
sorted lexicographically by path and written with the same CSV dialect
(double-quote on comma, CRLF line endings) as the original.

This converts a previously hand-maintained file into a reproducible artifact:
re-running it must reproduce the committed manifest byte-for-byte (modulo the
files whose contents legitimately changed).
"""
import csv, hashlib, io, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "kit_manifest.csv"

EXCLUDE_DIRS = {"__pycache__"}
EXCLUDE_FILES = {MANIFEST.relative_to(ROOT).as_posix()}

CHAPTER_DESC = "canonical site: chapter page (answer-first + JSON-LD + claim-strip + firewall)"
NEW_DESCRIPTIONS = {
    "tools/verify_site.py":
        "structural search-gate verifier (answer-first; >=2 JSON-LD; sitemap URLs == pages; numbers verbatim)",
    "tools/gen_manifest.py":
        "deterministic manifest generator (sha256 of every tracked file; excludes __pycache__)",
    "engine/feasibility_validation.py":
        "battery FV1-FV8: the (B) held-out score + identifiability decomposition + sign-law '-' and '+' arms. FV2 ordering NULL; FV5/FV6 the gamma-ordered class is non-identified (gamma~GC); FV7 the corrective sign-law '-' arm SCORES on held-out DepMap CRISPR-KO (point-biserial +0.494, exact p 0.0227); FV8 the '+' RESTORE arm SCORES on held-out Horlbeck 2016 CRISPRa (point-biserial +0.4852, exact p 0.0274) -- both identified, firewall-clean, so the sign-law is bidirectionally [V] (first+second held-out POSITIVES); O-22 stays [O] (obstacle is now the firewall, not data), O-21 stays [O]",
    "engine/parent_of_origin.py":
        "battery PO1-PO3 [II-3]: parent-of-origin from temporal context (sustained-maternal vs transient-paternal); sign law; universal across the germline atlas; penetrance [O]",
    "engine/rna_vaccine_kinetics.py":
        "battery VK1-VK2 [IV-1,IV-3]: prime-boost interval interior optimum (GC rounds); saRNA vs mRNA reachability ordering; absolute days/titre [O]",
    "engine/lever_map.py":
        "battery LV1-LV4 [V-1..V-4]: Lever-A/B sub-types (CRISPRa->Lever B); decision boundary curve h_path*(g)=h_cap-spinodal(g); edit-free durable correction (w>w*); efficiency/schedule [O]",
    "data/fetch_bvalidation.py":
        "(B) held-out target reception (Replogle 2022); offline verify() integrity+headline gate; --fetch rebuilds from figshare",
    "bvalidation/replogle2022_heldout.cache.json":
        "(B) scoring sheet: held-out matched-panel slice (fold_expr/control_expr) + provenance; gamma re-read frozen, not stored as truth",
    "data/fetch_signlaw_depmap.py":
        "(B) sign-law '-' arm target reception (DepMap 24Q2 CRISPR-KO gene-effect); offline verify() reproduces the onco '-'-arm headline from cache + frozen atlas; --fetch rebuilds from figshare (only matched columns retained)",
    "bvalidation/depmap24q2_signlaw_heldout.cache.json":
        "(B) sign-law '-' arm scoring sheet: per-gene DepMap gene-effect for the frozen disease panel + provenance/warrant/sign-locked prediction; carries gene-effects only -- corr_sign/gc/gamma re-read frozen, never stored as truth",
    "data/fetch_signlaw_crispra.py":
        "(B) sign-law '+' RESTORE arm target reception (Horlbeck 2016 hCRISPRa-v2 K562 growth, eLife 19760); pure-stdlib .xlsx reader (no openpyxl/pandas); offline verify() reproduces the onco '+'-arm headline from cache + frozen atlas; --fetch rebuilds from the eLife CDN (only matched rows retained)",
    "bvalidation/crispra_horlbeck2016_signlaw_heldout.cache.json":
        "(B) sign-law '+' arm scoring sheet: per-gene Horlbeck 2016 CRISPRa K562 growth phenotype for the frozen disease panel + provenance/warrant/sign-locked prediction/honest caveats; carries growth phenotypes only -- corr_sign/gc/gamma re-read frozen, never stored as truth",
}
CHAPTER_PAGE_RE = re.compile(r"^docs/inheritance/\d\d-[a-z0-9-]+/index\.html$")


def load_old_descriptions():
    desc = {}
    if MANIFEST.exists():
        with MANIFEST.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                desc[row["path"]] = row["description"]
    return desc


def tracked_files():
    out = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIRS for part in p.relative_to(ROOT).parts):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel in EXCLUDE_FILES:
            continue
        out.append(rel)
    return sorted(out)


def sitemap_url_count():
    sm = ROOT / "docs" / "sitemap.xml"
    if not sm.exists():
        return None
    return len(re.findall(r"<loc>", sm.read_text(encoding="utf-8")))


def describe(rel, old):
    if CHAPTER_PAGE_RE.match(rel):
        return CHAPTER_DESC
    if rel == "docs/sitemap.xml":
        n = sitemap_url_count()
        return f"canonical site: sitemap ({n} URLs)" if n is not None else old.get(rel, "")
    # curated descriptions are the intentional source of truth; old manifest is only a fallback
    # (this keeps a changed file's label current instead of pinning the first description it ever got)
    if rel in NEW_DESCRIPTIONS:
        return NEW_DESCRIPTIONS[rel]
    if old.get(rel):
        return old[rel]
    return ""


def main():
    old = load_old_descriptions()
    rows = []
    missing_desc = []
    for rel in tracked_files():
        data = (ROOT / rel).read_bytes()
        d = describe(rel, old)
        if not d:
            missing_desc.append(rel)
        rows.append([rel, len(data), hashlib.sha256(data).hexdigest(), d])

    buf = io.StringIO()
    w = csv.writer(buf)  # default dialect: quote-on-need, \r\n line terminator
    w.writerow(["path", "bytes", "sha256", "description"])
    w.writerows(rows)
    MANIFEST.write_text(buf.getvalue(), encoding="utf-8")

    print(f"manifest rows: {len(rows)} (+header)")
    if missing_desc:
        print("WARNING: no description for:", *missing_desc, sep="\n  ")
        return 1
    print("manifest regenerated OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
