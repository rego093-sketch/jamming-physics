#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py -- Special-Sense Organs WRITING phase: per-title canonical SEO HTML generator.

HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").

WHEN UNLOCKED it follows VP-SPEC v1.8 (../VP_SPEC_v1_8.md):
  - canonical HTML in docs/ (C2); ONE page per title/section (C4 sec 6/6-R): answer-first
    <p class="answer"> (40-60 words), JSON-LD ScholarlyArticle + BreadcrumbList, claim-strip
    (grade + repro path), vp-card for each locked quantity restated self-containedly;
  - ENGLISH body (C0); honest grades + stated [O] (C3); deterministic numbers (C1).

"Code is the agent" (sec 1): chapter prose is authored data in _sns_content; every QUANTITY is loaded
from the verified corpus (reports/emergence_results.json, 2xsha256 6a68bc48...) and injected by build_F,
so the same inputs render byte-identical HTML (no wall-clock; BUILD_DATE fixed). The rendering engine is
_sns_render. Concept DOI 10.5281/zenodo.20755154 is emitted in the claim-strip, JSON-LD, and footer.
"""
import os, sys, json
_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(_HERE, "..")
sys.path.insert(0, _HERE)                                   # _sns_render, _sns_content
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_verify"))
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_pathology"))
import importlib
gates = importlib.import_module("gates")


def _load_corpus():
    res = json.load(open(os.path.join(_PKG, "reports", "emergence_results.json"), encoding="utf-8"))
    path = importlib.import_module("setpoint_failure").status()
    treat = importlib.import_module("treatment").status()
    try:
        sha = json.load(open(os.path.join(_PKG, "reports", "research_complete.json"), encoding="utf-8"))["result_sha256"]
    except Exception:
        sha = ""
    return res, path, treat, sha


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Research-first: pass the stress battery + sign off, then")
        print("  python repro/_verify/gates.py  ->  gates.write_research_complete()  ;  echo writing > PHASE")
        return 1

    render = importlib.import_module("_sns_render")
    content = importlib.import_module("_sns_content")

    res, path, treat, sha = _load_corpus()
    F = content.build_F(res, path, treat)
    chs = content.chapters(F)

    docs_dir = os.path.join(_PKG, "docs")
    manifest = os.path.join(_PKG, "manifest", "sensory_organ_vp_site.csv")
    print("UNLOCKED -> emitting per-title canonical SEO HTML (VP-SPEC v1.8 sec 6/6-R) into docs/ ...")
    summary = render.build_site(chs, F, sha, docs_dir, manifest)

    print("  chapters : %d" % summary["chapters"])
    print("  body words: %d" % summary["total_words"])
    print("  sitemap URLs: %d" % summary["urls"])
    print("  hub: docs/%s/index.html  | index: docs/index.html" % render.PAPER["paper_id"])
    print("  access: robots.txt, sitemap.xml, llms.txt, llms-full.txt")
    print("  DOI: %s (concept)" % render.DOI)
    print("DONE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
