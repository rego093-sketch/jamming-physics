#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reconcile_manifest.py — bring manifest/mind.csv and docs/mind/_meta.json word counts into
agreement with the canonical HTML (VP-SPEC C1: derived counts == canonical, drift 0).

The original package shipped stale, mutually inconsistent word counts (manifest vs _meta).
This recomputes the body word count of each chapter from the canonical HTML with one
deterministic rule -- excluding the answer-first, abstract, vp-card asides, h1, nav and
figures (the same exclusions the gate uses) -- and writes them back. Idempotent.

Run: python3 tools/reconcile_manifest.py
"""
import os, sys, re, csv, json, io

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import mind_registry as R

PKG = R.PKG
MIND = os.path.join(PKG, "docs", "mind")
MANIFEST = os.path.join(PKG, "manifest", "mind.csv")
META = os.path.join(MIND, "_meta.json")


def body_words(slug):
    h = open(os.path.join(MIND, slug, "index.html"), encoding="utf-8").read()
    m = re.search(r"<main>(.*)</main>", h, flags=re.S)
    t = m.group(1) if m else h
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<aside.*?</aside>", "", t, flags=re.S)
    t = re.sub(r'<p class="answer".*?</p>', "", t, flags=re.S)
    t = re.sub(r'<p class="abstract".*?</p>', "", t, flags=re.S)
    t = re.sub(r"<h1>.*?</h1>", "", t, flags=re.S)
    t = re.sub(r"<nav.*?</nav>", "", t, flags=re.S)
    t = re.sub(r"<figure.*?</figure>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-zA-Z#0-9]+;", " ", t)
    return len(t.split())


def main():
    counts = {slug: body_words(slug) for slug in R.CHAPTERS}

    # rewrite manifest/mind.csv (preserve all columns; update 'words')
    with open(MANIFEST, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    header = rows[0]
    wi = header.index("words"); si = header.index("slug")
    for row in rows[1:]:
        if row and row[si] in counts:
            row[wi] = str(counts[row[si]])
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerows(rows)
    open(MANIFEST, "w", encoding="utf-8", newline="").write(buf.getvalue())

    # rewrite _meta.json words per chapter
    meta = json.load(open(META, encoding="utf-8"))
    for ch in meta.get("chapters", []):
        if ch.get("slug") in counts:
            ch["words"] = counts[ch["slug"]]
    json.dump(meta, open(META, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print("reconciled word counts (canonical HTML):")
    for slug, n in counts.items():
        print(f"  {slug:26s} {n}")


if __name__ == "__main__":
    main()
