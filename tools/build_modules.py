#!/usr/bin/env python3
"""Build docs/modules/index.html (the Common Modules page) from
registry/modules.json. Cross-links every bundled term to the Concept
Dictionary (/concepts/#id). Regenerate, never hand-edit the page."""
import json, html, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "registry", "modules.json")
CONCEPTS = os.path.join(ROOT, "registry", "concepts.json")
OUT = os.path.join(ROOT, "docs", "modules", "index.html")
SITE = "https://jamming-physics.org"
GRADE_CLASS = {"F": "g-f", "V": "g-v", "L": "g-l", "O": "g-o"}


def esc(s):
    return html.escape(s, quote=True)


def grade_badge(g):
    label = {"F": "[F] forced", "V": "[V] verified", "L": "[L] anchored", "O": "[O] open"}.get(g, f"[{g}]")
    return f'<b class="grade {GRADE_CLASS.get(g,"g-x")}">{esc(label)}</b>'


def main():
    data = json.load(open(SRC, encoding="utf-8"))
    cj = json.load(open(CONCEPTS, encoding="utf-8"))
    term_name = {e["id"]: (e.get("symbol") or e["term"]) for e in cj["entries"]}
    mods = {m["id"]: m for m in data["modules"]}
    order = data["module_order"]

    # JSON-LD: each module as a DefinedTerm in a set; the page itself a CreativeWork
    def dt(m):
        return {"@type": "DefinedTerm", "name": m["name"], "termCode": m["id"],
                "description": m["forces"], "inDefinedTermSet": f"{SITE}/modules/"}
    ld = {"@context": "https://schema.org", "@type": "DefinedTermSet",
          "@id": f"{SITE}/modules/", "name": data["title"], "description": data["thesis"],
          "hasDefinedTerm": [dt(m) for m in data["modules"]]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                  {"@type": "ListItem", "position": 2, "name": "Common Modules"}]}

    cards = []
    for n, mid in enumerate(order, 1):
        m = mods[mid]
        star = ' <span class="named">\u2605 author-named core</span>' if m.get("author_named") else ""
        role = '<span class="role bedrock">bedrock</span>' if m.get("role") == "bedrock" else '<span class="role gen">generator</span>'
        bund = " \u00b7 ".join(
            f'<a href="/concepts/#{esc(b)}">{esc(term_name.get(b, b))}</a>' for b in m.get("bundles", []))
        canon = " \u00b7 ".join(
            f'<a href="{esc(c["href"])}">{esc(c["loc"])}</a>' for c in m.get("canonical", []))
        sc = m.get("self_completeness")
        sc_html = f'\n  <p class="selfc"><b>Self-completeness.</b> {esc(sc)}</p>' if sc else ""
        cards.append(f"""<section class="mod" id="{esc(mid)}">
  <h2><span class="num">{n}</span> {esc(m['name'])} {role}{star}</h2>
  <p class="forces"><b>Forces.</b> {esc(m['forces'])} {grade_badge(m['grade'])}</p>
  <p class="reach"><b>Reach.</b> {esc(m['reach'])} <span class="inh">inherited by {esc(m['inherited_by'])}</span></p>{sc_html}
  <p class="attack"><b>Attack surface.</b> {esc(m['attack_surface'])}</p>
  <p class="meta-row"><b>Built from:</b> {bund}</p>
  <p class="meta-row"><b>Canonical derivation:</b> {canon}</p>
</section>""")

    css = """
:root{--ink:#1c1d21;--mut:#5b5e66;--bg:#fff;--line:#e6e6ea;--ac:#0a5a8a;--amber:#8a5a00;--amberbg:#fff6e0}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--bg);font:17px/1.65 Georgia,'Times New Roman',serif}
main{max-width:820px;margin:0 auto;padding:0 18px 64px}
header{border-bottom:1px solid var(--line)}
footer{border-top:1px solid var(--line);max-width:820px;margin:40px auto 0;padding:14px 18px;color:var(--mut);font-size:.85em}
.crumb{max-width:820px;margin:0 auto;padding:10px 18px;font:14px/1.4 system-ui,sans-serif;color:var(--mut)}
a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:1.7em;margin:.6em 0 .2em}
.thesis{font-size:1.05em;color:#2a2c33;border-left:3px solid var(--ac);padding:.4em 0 .4em .9em;margin:1.1em 0}
.mod{border:1px solid var(--line);border-radius:10px;padding:1em 1.1em;margin:1.3em 0;background:#fff}
.mod h2{font-size:1.22em;margin:.1em 0 .6em;border:0}
.num{display:inline-block;min-width:1.5em;height:1.5em;line-height:1.5em;text-align:center;border-radius:50%;background:var(--ac);color:#fff;font:700 .8em/1.5em system-ui,sans-serif;vertical-align:middle;margin-right:.3em}
.role{font:600 .62em/1 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.04em;border-radius:10px;padding:.3em .55em;vertical-align:middle;margin-left:.3em}
.role.bedrock{background:#eef1f4;color:var(--mut)}.role.gen{background:#e7f0f7;color:var(--ac)}
.named{font:600 .62em/1 system-ui,sans-serif;color:var(--amber);background:var(--amberbg);border-radius:10px;padding:.3em .55em;vertical-align:middle}
.mod p{margin:.55em 0}
.mod .forces b,.mod .reach b,.mod .attack b,.meta-row b{color:var(--ink)}
.attack{color:#7a2f2f;background:#fbf4f4;border-radius:8px;padding:.5em .7em}
.selfc{color:#1d5a36;background:#f1f8f3;border-radius:8px;padding:.5em .7em}
.inh{display:inline-block;color:var(--mut);font:.85em system-ui,sans-serif}
.meta-row{font-size:.95em;color:var(--mut)}
.grade{font-family:system-ui,sans-serif;font-size:.82em;white-space:nowrap}
.g-f{color:#0a5a8a}.g-v{color:#1d6b2e}.g-l{color:#6a4b00}.g-o{color:#9c1f1f}.g-x{color:var(--mut)}
.foot-links{margin:1.4em 0;font:14px/1.7 system-ui,sans-serif}
@media(max-width:480px){body{font-size:16px}}
"""

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Common Modules \u2014 the generative core | Jamming Physics</title>
<meta name="description" content="The load-bearing common modules of the VP framework: the primary attack surface and the generators. With the dictionary plus these, most of the framework is forced.">
<link rel="canonical" href="{SITE}/modules/">
<style>{css}</style>
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, ensure_ascii=False)}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> \u203a Common Modules</nav></header>
<main>
<h1>Common Modules \u2014 the generative core</h1>
<p class="thesis">{esc(data['thesis'])}</p>
<p class="foot-links">See also: <a href="/concepts/">Concept Dictionary</a> (the terms these modules are built from) \u00b7 <a href="/AGENTS.md">AGENTS.md</a> (full reading guide).</p>
{chr(10).join(cards)}
<footer>Generated from <code>registry/modules.json</code> on {datetime.date.today().isoformat()} \u00b7
{len(data['modules'])} modules \u00b7 CC BY 4.0 \u00b7 Young Jae Lee</footer>
</main>
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(page)
    print(f"wrote {OUT} ({len(data['modules'])} modules, {len(page)} bytes)")

    # validate: bundled ids exist in concepts; canonical hrefs resolve
    cids = {e["id"] for e in cj["entries"]}
    miss_terms, miss_links = [], []
    for m in data["modules"]:
        for b in m.get("bundles", []):
            if b not in cids:
                miss_terms.append((m["id"], b))
        for c in m.get("canonical", []):
            if not os.path.isfile(os.path.join(ROOT, "docs" + c["href"] + "index.html")):
                miss_links.append((m["id"], c["href"]))
    print("missing bundled terms:", miss_terms or "none")
    print("broken canonical links:", miss_links or "none")


if __name__ == "__main__":
    main()
