#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Aging / Senescence WRITING phase entry point.
HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").
When unlocked, delegates to render_site.py, which emits the canonical per-section SEO HTML in docs/
per VP-SPEC v1.8 (answer-first, JSON-LD ScholarlyArticle + BreadcrumbList, claim-strip, vp-cards;
English body; honest grades with stated [O]; deterministic numbers pulled from the engine; DOI TBD).
"""
import os, sys, importlib, importlib.util
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "repro", "_verify"))
gates = importlib.import_module("gates")


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Research-first: pass the stress battery, then")
        print("  python repro/_verify/gates.py  ->  gates.write_research_complete()  ;  echo writing > PHASE")
        return 1
    spec = importlib.util.spec_from_file_location("render_site", os.path.join(_HERE, "render_site.py"))
    rs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rs)
    return rs.main()


if __name__ == "__main__":
    import importlib.util
    raise SystemExit(main())
