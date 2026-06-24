#!/usr/bin/env python3
"""Build docs/concepts/index.html (the unified DefinedTermSet glossary)
from registry/concepts.json. Regenerate, never hand-edit the page.

Implements VP-SPEC v1.8 §6-R.2 (self-contained card per locked quantity)
and §6-R.4 (DefinedTerm / DefinedTermSet JSON-LD)."""
import json, html, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "registry", "concepts.json")
OUT = os.path.join(ROOT, "docs", "concepts", "index.html")
SITE = "https://jamming-physics.org"

GRADE_CLASS = {"F": "g-f", "V": "g-v", "L": "g-l", "O": "g-o"}


def esc(s):
    return html.escape(s, quote=True)


def grade_badge(g):
    label = {"F": "[F] forced", "V": "[V] verified", "L": "[L] anchored",
             "O": "[O] open", "imported": "[imported]", "admissible": "[admissible]",
             "discipline": "[discipline]", "principle": "[principle]",
             "distinguishing": "[distinguishing]", "LOCK": "[LOCK]"}.get(g, f"[{g}]")
    cls = GRADE_CLASS.get(g, "g-x")
    return f'<b class="grade {cls}">{esc(label)}</b>'


def card(e):
    head = e.get("symbol") or e["term"]
    sub = "" if head == e["term"] else f' <span class="tname">\u2014 {esc(e["term"])}</span>'
    loc = f' {esc(e["loc"])}' if e.get("loc") else ""
    link = f'<a href="{esc(e["href"])}">canonical{loc}</a>' if e.get("href") else ""
    dis = f'<div class="disambig">\u26a0 {esc(e["disambig"])}</div>' if e.get("disambig") else ""
    aka = ""
    others = [a for a in e.get("aka", []) if a != e["id"]]
    if others:
        aka = f'<div class="aka">unifies: {esc(", ".join(others))}</div>'
    return (f'<aside class="vp-card" id="{esc(e["id"])}" data-locked="{esc(e["id"])}">'
            f'<b class="sym">{esc(head)}</b>{sub} \u2014 {esc(e["statement"])} '
            f'{grade_badge(e["grade"])}. {link}{dis}{aka}</aside>')


def defined_term(e):
    d = {"@type": "DefinedTerm", "name": e["term"], "termCode": e["id"],
         "description": e["statement"],
         "inDefinedTermSet": f"{SITE}/concepts/"}
    if e.get("href"):
        d["url"] = SITE + e["href"] if e["href"].startswith("/") else e["href"]
    return d


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    entries = data["entries"]
    order = data["register_order"]
    regs = data["registers"]
    by_reg = {r: [x for x in entries if x["register"] == r] for r in order}

    today = datetime.date.today().isoformat()

    # JSON-LD: a CreativeWork carrying the DefinedTermSet (terms), + BreadcrumbList
    term_set = {"@context": "https://schema.org", "@type": "DefinedTermSet",
                "@id": f"{SITE}/concepts/", "name": data["title"],
                "description": data["note"],
                "hasDefinedTerm": [defined_term(e) for e in entries]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": "Concept Dictionary"}]}

    # alphabetical symbol index
    idx = sorted(entries, key=lambda e: (e.get("symbol") or e["term"]).lower())
    index_links = " \u00b7 ".join(
        f'<a href="#{esc(e["id"])}">{esc(e.get("symbol") or e["term"])}</a>' for e in idx)

    # legend strip
    leg = data["legend"]
    legend_html = "".join(
        f'<div class="legrow"><b class="grade {GRADE_CLASS.get(k,"g-x")}">[{k}]</b> {esc(v)}</div>'
        for k, v in leg.items())

    sections = []
    for r in order:
        items = by_reg[r]
        if not items:
            continue
        cards = "\n".join(card(e) for e in items)
        sections.append(
            f'<section><h2 id="reg-{r}">{esc(regs[r])} '
            f'<span class="rcount">{len(items)}</span></h2>\n{cards}\n</section>')

    answer = ("This dictionary is the unified internal lexicon of the VP framework: "
              "every cross-volume term and every locked core number, each with its plain "
              "meaning, its grade, and a link to the single canonical source. Same-glyph "
              "collisions are disambiguated; per-disease and per-gene data are pointed to, not copied.")

    css = """
:root{--ink:#1c1d21;--mut:#5b5e66;--bg:#fff;--line:#e6e6ea;--ac:#0a5a8a;--amber:#8a5a00;--amberbg:#fff6e0}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--bg);font:17px/1.65 Georgia,'Times New Roman',serif}
main{max-width:820px;margin:0 auto;padding:0 18px 64px}
header{border-bottom:1px solid var(--line)}
footer{border-top:1px solid var(--line);max-width:820px;margin:40px auto 0;padding:14px 18px;color:var(--mut);font-size:.85em}
.crumb{max-width:820px;margin:0 auto;padding:10px 18px;font:14px/1.4 system-ui,sans-serif;color:var(--mut)}
a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:1.7em;margin:.6em 0 .2em}
h2{font-size:1.18em;margin:1.8em 0 .5em;padding-bottom:.2em;border-bottom:1px solid var(--line)}
.rcount{font:12px/1 system-ui,sans-serif;color:var(--mut);border:1px solid var(--line);border-radius:10px;padding:.15em .5em;vertical-align:middle;margin-left:.4em}
.answer{font-size:1.04em;color:#2a2c33;border-left:3px solid var(--ac);padding:.3em 0 .3em .8em;margin:1em 0}
.idxbar{font:13.5px/1.9 system-ui,sans-serif;color:var(--mut);background:#f6f7f9;border:1px solid var(--line);border-radius:8px;padding:.6em .8em;margin:1em 0}
.legend{font:13.5px/1.5 system-ui,sans-serif;background:#fafafa;border:1px solid var(--line);border-radius:8px;padding:.6em .8em;margin:1em 0}
.legrow{margin:.15em 0}
.vp-card{border:1px solid var(--line);border-left:3px solid var(--ac);border-radius:8px;padding:.6em .8em;margin:.7em 0;background:#fff}
.vp-card .sym{font-weight:700}
.vp-card .tname{color:var(--mut);font-weight:400}
.vp-card .disambig{color:var(--amber);background:var(--amberbg);border-radius:6px;padding:.25em .5em;margin:.45em 0 0;font-size:.92em}
.vp-card .aka{color:var(--mut);font-size:.85em;margin-top:.3em;font-family:system-ui,sans-serif}
.grade{font-family:system-ui,sans-serif;font-size:.82em;white-space:nowrap}
.g-f{color:#0a5a8a}.g-v{color:#1d6b2e}.g-l{color:#6a4b00}.g-o{color:#9c1f1f}.g-x{color:var(--mut)}
@media(max-width:480px){body{font-size:16px}main{padding-bottom:48px}}
"""

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concept Dictionary \u2014 unified lexicon &amp; locked constants | Jamming Physics</title>
<meta name="description" content="The unified internal lexicon of the VP framework: every cross-volume term and locked core number with its plain meaning, grade, and canonical source.">
<link rel="canonical" href="{SITE}/concepts/">
<style>{css}</style>
<script type="application/ld+json">
{json.dumps(term_set, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, ensure_ascii=False)}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> \u203a Concept Dictionary</nav></header>
<main>
<h1>Concept Dictionary</h1>
<p class="answer">{esc(answer)}</p>
<div class="idxbar">{index_links}</div>
<div class="legend"><b>Grades.</b> {legend_html}</div>
{chr(10).join(sections)}
<footer>Generated from <code>registry/concepts.json</code> on {today} \u00b7 {len(entries)} terms \u00b7
CC BY 4.0 \u00b7 Young Jae Lee \u00b7 <a href="/AGENTS.md">AGENTS.md</a></footer>
</main>
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"wrote {OUT}  ({len(entries)} terms, {len(page)} bytes)")


if __name__ == "__main__":
    main()
