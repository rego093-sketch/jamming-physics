#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_integrity.py  --  canonical-site integrity gates (inherited discipline from analgesic v2.0).

grades_ok()  -- every single-letter bracket grade token on the site is in the legend {F,V,L,O}.
                A stray grade (e.g. an un-legended [H] or [X]) is a FAIL.
ledger_ok()  -- every [O] row in IRREPRODUCIBILITY_LEDGER.md states a non-empty obstacle, and every
                site section that asserts an [O] is covered by a ledger location. This enforces the
                ledger's own rule: "an [O] without a stated obstacle is a gate FAIL."
doi_ok()     -- the live concept DOI is embedded across the site (every section page + hub), the
                content manifests agree, and no "pending"/placeholder DOI string survives anywhere.
"""
import os, re, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG  = os.path.abspath(os.path.join(_HERE, "..", ".."))
_DOCS = os.path.join(_PKG, "docs")
_LEDGER = os.path.join(_PKG, "IRREPRODUCIBILITY_LEDGER.md")
_META = os.path.join(_DOCS, "cardioresp_vp_site", "_meta.json")
_LLMS = os.path.join(_DOCS, "llms.txt")

DOI = "10.5281/zenodo.20755371"
LEGAL_GRADES = {"F", "V", "L", "O"}
_GRADE = re.compile(r"\[([A-Z])\]")
_TAG = re.compile(r"<[^>]+>")


def _section_pages():
    base = os.path.join(_DOCS, "cardioresp_vp_site")
    out = []
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        d = os.path.join(base, name)
        idx = os.path.join(d, "index.html")
        m = re.match(r"^(\d+)-", name)
        if os.path.isfile(idx) and m:
            out.append((int(m.group(1)), idx))
    return out


def _all_html():
    out = []
    for root, _d, files in os.walk(_DOCS):
        for fn in files:
            if fn.endswith(".html"):
                out.append(os.path.join(root, fn))
    return sorted(out)


def grades_ok():
    illegal = {}
    for ap in _all_html():
        txt = _TAG.sub(" ", open(ap, encoding="utf-8").read())
        for g in set(_GRADE.findall(txt)):
            if g not in LEGAL_GRADES:
                illegal.setdefault(os.path.relpath(ap, _PKG).replace(os.sep, "/"), []).append("[%s]" % g)
    return {"ok": not illegal, "legend": sorted(LEGAL_GRADES), "illegal": illegal}


def ledger_ok():
    rows_open, missing_obstacle, locs = 0, [], set()
    if os.path.exists(_LEDGER):
        for ln in open(_LEDGER, encoding="utf-8"):
            if not ln.strip().startswith("|"):
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 4 or cells[1] != "[O]":
                continue
            rows_open += 1
            obstacle, location = cells[2], cells[3]
            if not obstacle or obstacle in ("-", "—"):
                missing_obstacle.append(cells[0])
            locs.update(int(x) for x in re.findall(r"\u00a7?\s*(\d+)", location))
    # sections on the site that assert an [O]
    open_sections = []
    for no, idx in _section_pages():
        if "[O]" in _TAG.sub(" ", open(idx, encoding="utf-8").read()):
            open_sections.append(no)
    uncovered = sorted(set(open_sections) - locs)
    ok = rows_open > 0 and not missing_obstacle and not uncovered
    return {"ok": ok, "ledger_open_rows": rows_open, "missing_obstacle": missing_obstacle,
            "ledger_locations": sorted(locs), "site_open_sections": sorted(set(open_sections)),
            "uncovered_open_sections": uncovered}


def doi_ok():
    secs = _section_pages()
    pages_with = [os.path.relpath(p, _PKG).replace(os.sep, "/") for _n, p in secs if DOI in open(p, encoding="utf-8").read()]
    hub = os.path.join(_DOCS, "cardioresp_vp_site", "index.html")
    hub_has = os.path.exists(hub) and DOI in open(hub, encoding="utf-8").read()
    placeholder = []
    for ap in _all_html() + ([_META] if os.path.exists(_META) else []) + ([_LLMS] if os.path.exists(_LLMS) else []):
        t = open(ap, encoding="utf-8").read()
        if re.search(r"DOI:?\s*pending|pending archival", t, re.I):
            placeholder.append(os.path.relpath(ap, _PKG).replace(os.sep, "/"))
    meta_doi = json.load(open(_META, encoding="utf-8")).get("doi") if os.path.exists(_META) else None
    llms_has = os.path.exists(_LLMS) and DOI in open(_LLMS, encoding="utf-8").read()
    ok = (len(pages_with) == len(secs) and len(secs) > 0 and hub_has
          and not placeholder and meta_doi == DOI and llms_has)
    return {"ok": ok, "doi": DOI, "section_pages": len(secs), "section_pages_with_doi": len(pages_with),
            "hub_has_doi": hub_has, "meta_doi": meta_doi, "llms_has_doi": llms_has,
            "placeholder_doi_files": placeholder}


def all_checks():
    g, l, d = grades_ok(), ledger_ok(), doi_ok()
    return {"grades": g, "ledger": l, "doi": d, "ok": g["ok"] and l["ok"] and d["ok"]}


if __name__ == "__main__":
    print(json.dumps(all_checks(), ensure_ascii=False, indent=2))
