#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_chapter_neuro.py — deterministic chapter builder (VP-SPEC §1: code is the
agent of transformation; the model authors CONTENT DATA, the builder emits the
canonical HTML). Reads content/neuro-{N}-*.json and writes the §6-template page to
docs/neuro/{slug}/index.html, byte-identical on every run.

Standard library only. The emitted HTML matches the existing neuro chapters
(answer-first, claim-strip, vp-card asides, two JSON-LD blocks, prev/contents/next).
"""
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # this script lives in tools/; ROOT is the package root
DOCS = os.path.join(ROOT, "docs", "neuro")
DOI = "10.5281/zenodo.17979015"
ORCID = "0009-0002-7535-8245"
PAPER_NAME = "From Ion Channels to Behaviour: A Falsifiable Neural Emergence Chain"
GH = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/neuro"
ABBREV = "Neural Emergence"


def build(content):
    no, slug = content["no"], content["slug"]
    subject = content["subject"]
    title = f"{subject} \u2014 {ABBREV} \u00a7{no} | Jamming Physics"
    headline = content["headline"]
    h1 = content["h1"]
    desc = content["description"]
    grade, gclass = content["grade"], content["grade_class"]
    answer, abstract = content["answer"], content["abstract"]

    out = []
    A = out.append
    A('<!DOCTYPE html>')
    A('<html lang="en">')
    A('<head>')
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A(f'<title>{title}</title>')
    A(f'<meta name="description" content="{desc}">')
    A(f'<link rel="canonical" href="https://jamming-physics.org/neuro/{slug}/">')
    A('<link rel="stylesheet" href="/assets/css/site.css">')
    # JSON-LD 1 — ScholarlyArticle
    A('<script type="application/ld+json">')
    A('{"@context":"https://schema.org","@type":"ScholarlyArticle",')
    A(f' "headline":"{headline}",')
    A(f' "isPartOf":{{"@type":"CreativeWork","name":"{PAPER_NAME}",')
    A(f'   "sameAs":"https://doi.org/{DOI}"}},')
    A(f' "position":{no},')
    A(' "author":{"@type":"Person","name":"Young Jae Lee",')
    A(f'   "sameAs":"https://orcid.org/{ORCID}"}},')
    A(' "license":"https://creativecommons.org/licenses/by/4.0/"}')
    A('</script>')
    # JSON-LD 2 — BreadcrumbList
    A('<script type="application/ld+json">')
    A('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[')
    A(' {"@type":"ListItem","position":1,"name":"Home","item":"https://jamming-physics.org/"},')
    A(' {"@type":"ListItem","position":2,"name":"Neural Emergence","item":"https://jamming-physics.org/neuro/"},')
    A(f' {{"@type":"ListItem","position":3,"name":"\\u00a7{no} {headline}"}}]}}')
    A('</script>')
    A('</head>')
    A('<body>')
    A(f'<header><nav class="crumb"><a href="/">Home</a> \u203a <a href="/neuro/">Neural Emergence</a> \u203a \u00a7{no}</nav></header>')
    A('<main>')
    A(f'<h1>{h1}</h1>')
    A('')
    A(f'<p class="answer">{answer}</p>')
    A('')
    A(f'<p class="abstract">{abstract}</p>')
    A('')
    A('<aside class="claim-strip">')
    A(f'  <span class="grade {gclass}">{grade}</span>')
    A('  <span class="gate">LOCK \u2192 Derive \u2192 Gate</span>')
    A(f'  <a href="{GH}/{slug}/" rel="noopener">reproduce (GitHub)</a>')
    A(f'  <a href="https://doi.org/{DOI}" rel="noopener">DOI snapshot</a>')
    A('</aside>')
    A('')
    # body sections
    for sec in content["sections"]:
        A(f'<h2>{sec["h2"]}</h2>')
        for p in sec["paras"]:
            A(f'<p>{p}</p>')
        for card in sec.get("cards", []):
            A(f'<aside class="vp-card" data-locked="{card["locked"]}">{card["html"]}</aside>')
        A('')
    # prev / contents / next nav
    prev, nxt = content.get("prev"), content.get("next")
    A('<nav class="pn">')
    if prev:
        A(f'  <a rel="prev" href="/neuro/{prev["slug"]}/">\u2190 \u00a7{prev["no"]}</a>')
    A('  <a href="/neuro/">paper contents</a>')
    if nxt:
        A(f'  <a rel="next" href="/neuro/{nxt["slug"]}/">\u00a7{nxt["no"]} \u2192</a>')
    A('</nav>')
    A('</main>')
    A(f'<footer>DOI <a href="https://doi.org/{DOI}">{DOI}</a> \u00b7 ORCID <a href="https://orcid.org/{ORCID}">{ORCID}</a> \u00b7 <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></footer>')
    A('</body>')
    A('</html>')
    return "\n".join(out) + "\n"


def main():
    content_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "content", "neuro-15-em-link.json")
    content = json.load(open(content_path, encoding="utf-8"))
    html = build(content)
    outdir = os.path.join(DOCS, content["slug"])
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"built docs/neuro/{content['slug']}/index.html  ({len(html)} bytes)")


if __name__ == "__main__":
    main()
