#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_volume.py — the DETERMINISTIC HTML builder for the ear emergence volume (VP-SPEC v1.8 §6).

Pipeline (no tuning, no network, byte-stable):
  vp_numeric_ssot.disp(KEY)  +  chapters.{META,CONCEPTS,CHAPTERS,O_LEDGER}
        |                                   |
        +--------------- build_volume.py ----+
                          |
                   docs/  (hub + 7 chapters + 3 concepts + css + sitemap/robots/llms.txt)

Every number that appears in docs/ is written ONLY as
    <span class="vp-num" data-vp="KEY">{disp(KEY)}</span>
so gate_volume.py can re-derive disp(KEY) from the verified code and assert the HTML text is
byte-identical (HTML <-> code drift = 0). Grade tokens [F]/[V]/[O]/[L]/[H] in the prose are
auto-wrapped into coloured <span class="grade ..."> nodes; the prose never hard-types a number.

Run from the package root:   python3 volume/tools/build_volume.py   -> prints  sha256: <hex>
"""
import os, sys, re, html, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.dirname(os.path.dirname(HERE))           # vp_ear_emergence_seed/
sys.path.insert(0, HERE)                                # volume/tools  (vp_numeric_ssot)
sys.path.insert(0, os.path.join(PKG, "volume", "content"))   # volume/content (chapters)

import vp_numeric_ssot as S
import chapters as C

DOCS = os.path.join(PKG, "docs")
META = C.META

# --------------------------------------------------------------------------------------------
# grade-token styling  (color ENCODES grade: green = established, amber = open obstacle)
GRADE_CLASS = {"F": "g-forced", "V": "g-verified", "O": "g-open", "L": "g-cited", "H": "g-handoff"}
GRADE_WORD  = {"F": "forced", "V": "verified", "O": "open", "L": "cited", "H": "handoff"}
PAGE_BADGE  = {  # page-level claim-strip badge: (token, label, class)
    "forced":   ("F", "forced",   "g-forced"),
    "verified": ("V", "verified", "g-verified"),
    "open":     ("O", "open",     "g-open"),
}
# chapter "cards" key -> concept slug (self-contained vp-card for the locked quantity it cites)
CARD_TO_CONCEPT = {
    "r19":      "r19-bistable-switch",
    "greenwood":"greenwood-place-map",
    "gamma":    "gamma-level-a4-shape",
}
CONCEPT_BY_SLUG = {c["slug"]: c for c in C.CONCEPTS}

_NUM_RE   = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")
_GRADE_RE = re.compile(r"\[([FVOLH])\]")


# --------------------------------------------------------------------------------------------
def esc(s):
    """HTML-escape text (&,<,>). Quotes handled separately where needed."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_inline(text):
    """Turn one prose string into safe HTML.

    Order is load-bearing:
      1) escape the raw text  -> literal <,>,& in prose become entities; [[KEY]]/[X] survive
      2) [[KEY]] -> <span class="vp-num" data-vp="KEY">esc(disp(KEY))</span>   (the ONLY number path)
      3) [F]/[V]/[O]/[L]/[H] -> coloured grade spans
    The gate decodes entities, so esc(disp(KEY)) round-trips back to disp(KEY) exactly.
    """
    out = esc(text)

    def _num(m):
        key = m.group(1)
        val = S.disp(key)                       # raises KeyError if a typo'd key ever appears
        return (f'<span class="vp-num" data-vp="{html.escape(key, quote=True)}">'
                f'{esc(val)}</span>')
    out = _NUM_RE.sub(_num, out)

    def _grade(m):
        tok = m.group(1)
        return (f'<span class="grade {GRADE_CLASS[tok]}" data-grade="{tok}" '
                f'title="{GRADE_WORD[tok]}">[{tok}]</span>')
    out = _GRADE_RE.sub(_grade, out)
    return out


def attr(s):
    """Escape a string for use in a double-quoted HTML attribute."""
    return html.escape(s, quote=True)


# ---- URL helpers ----------------------------------------------------------------------------
# Page identity = path segments under docs/.  hub=[]  chapter=[slug]  concept=["concepts",cslug]
def relurl(from_segs, to_segs):
    prefix = "../" * len(from_segs)
    if not to_segs:
        return prefix + "index.html"
    return prefix + "/".join(to_segs) + "/index.html"

def cssurl(from_segs):
    return ("../" * len(from_segs)) + "assets/css/site.css"

def canonical(segs):
    base = META["canonical_base"].rstrip("/")
    if not segs:
        return base + "/"
    return base + "/" + "/".join(segs) + "/"


# ---- shared chrome --------------------------------------------------------------------------
def rail_html(from_segs, active_n):
    """Deterministic inline-SVG 'cochlear spine': 7 chapter nodes on a vertical rail.

    A navigation MOTIF, not a data figure — the apex/base captions frame the volume's
    theme (tonotopy) without asserting any per-chapter frequency.
    """
    top, bottom, n = 26, 274, len(C.CHAPTERS)
    step = (bottom - top) / (n - 1)
    nodes = []
    line = f'<line class="spine" x1="22" y1="{top}" x2="22" y2="{bottom}"/>'
    for i, ch in enumerate(C.CHAPTERS):
        y = round(top + i * step, 2)
        is_on = (ch["n"] == active_n)
        r = 7 if is_on else 4.5
        cls = "node on" if is_on else "node"
        href = relurl(from_segs, [ch["slug"]])
        label = f'§{ch["n"]}'
        nodes.append(
            f'<a class="rail-link" href="{attr(href)}" aria-label="{attr(ch["subj"])}">'
            f'<circle class="{cls}" cx="22" cy="{y}" r="{r}"/>'
            f'<text class="rail-num" x="40" y="{y + 4}">{label}</text></a>'
        )
    svg = (
        f'<svg class="rail-svg" viewBox="0 0 168 300" role="img" '
        f'aria-label="Volume contents (tonotopic spine)">'
        f'<text class="rail-cap" x="22" y="14" text-anchor="middle">base</text>'
        f'{line}{"".join(nodes)}'
        f'<text class="rail-cap" x="22" y="294" text-anchor="middle">apex</text>'
        f'</svg>'
    )
    hub_href = relurl(from_segs, [])
    return (
        f'<nav class="rail" aria-label="Volume contents">'
        f'<a class="rail-home" href="{attr(hub_href)}">Hearing<br><span>from first principles</span></a>'
        f'{svg}</nav>'
    )


def head(title, desc, segs, jsonld_blocks, extra_meta=""):
    css = cssurl(segs)
    can = canonical(segs)

    def _ld(b):
        s = json.dumps(b, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        # safe embedding inside <script>: escape the three HTML-significant chars as \uXXXX
        s = s.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
        return f'<script type="application/ld+json">{s}</script>'

    ld = "\n".join(_ld(b) for b in jsonld_blocks)
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)}</title>\n"
        f'<meta name="description" content="{attr(desc)}">\n'
        f'<meta name="author" content="{attr(META["author"])}">\n'
        f'<link rel="canonical" href="{attr(can)}">\n'
        f'<link rel="license" href="{attr(META["license_url"])}">\n'
        '<meta name="robots" content="index,follow">\n'
        f"{extra_meta}"
        f'<link rel="stylesheet" href="{attr(css)}">\n'
        f"{ld}\n"
        "</head>\n<body>\n"
        '<a class="skip" href="#main">Skip to content</a>\n'
    )


def person_ld():
    return {"@type": "Person", "name": META["author"],
            "identifier": f'https://orcid.org/{META["orcid"]}',
            "url": f'https://orcid.org/{META["orcid"]}'}


def breadcrumb_ld(segs, name):
    items = [{"@type": "ListItem", "position": 1, "name": "Jamming Physics", "item": META["site"]},
             {"@type": "ListItem", "position": 2, "name": META["volume"], "item": canonical([])}]
    if segs:
        items.append({"@type": "ListItem", "position": 3, "name": name, "item": canonical(segs)})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def footer_html():
    return (
        '<footer class="vol-foot">'
        f'<p>{esc(META["volume"])} — {esc(META["subtitle"])}</p>'
        f'<p>{esc(META["author"])} '
        f'(<a href="https://orcid.org/{attr(META["orcid"])}">ORCID {esc(META["orcid"])}</a>). '
        f'<a href="{attr(META["license_url"])}">{esc(META["license"])}</a>. '
        f'Reproducible source: <a href="{attr(META["repo"])}">{esc(META["repo"])}</a>.</p>'
        f'<p class="doi-line">Readable-layer source (DNA volume): '
        f'<a href="https://doi.org/{attr(META["dna_doi"])}">doi:{esc(META["dna_doi"])}</a>. '
        f'This volume\u2019s concept DOI: '
        f'<a href="https://doi.org/{attr(META["volume_doi"])}">doi:{esc(META["volume_doi"])}</a>. '
        f'Canonical deployment at {esc(META["canonical_base"])} pending.</p>'
        f'<p class="ver">v{esc(META["package_version"])} · built deterministically from '
        f'vp_numeric_ssot (2\u00d7SHA-256) · numbers are reproduced, not typed.</p>'
        "</footer>\n"
    )


def claim_strip(grade, segs):
    tok, label, cls = PAGE_BADGE[grade]
    return (
        '<aside class="claim-strip" aria-label="Provenance">'
        f'<span class="badge {cls}">[{tok}] {esc(label)}</span>'
        '<span class="method" title="every page: state the lock, derive, then gate">LOCK\u2009\u2192\u2009Derive\u2009\u2192\u2009Gate</span>'
        f'<a class="repro" href="{attr(META["repo"])}">reproduce \u2197</a>'
        f'<a class="doi" href="https://doi.org/{attr(META["dna_doi"])}">doi:{esc(META["dna_doi"])}</a>'
        "</aside>"
    )


def vp_card(card_key, from_segs):
    cslug = CARD_TO_CONCEPT[card_key]
    con = CONCEPT_BY_SLUG[cslug]
    href = relurl(from_segs, ["concepts", cslug])
    return (
        '<aside class="vp-card">'
        f'<a class="vp-card-name" href="{attr(href)}">{esc(con["name"])}</a>'
        f'<code class="vp-card-term">{esc(con["term"])}</code>'
        f'<p class="vp-card-short">{render_inline(con["short"])}</p>'
        "</aside>"
    )


# --------------------------------------------------------------------------------------------
def build_chapter(ch):
    segs = [ch["slug"]]
    n, total = ch["n"], len(C.CHAPTERS)
    title = f'{ch["subj"]} \u2014 {META["volume"]}'

    article_ld = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": ch["subj"],
        "name": ch["subj"],
        "description": ch["desc"],
        "url": canonical(segs),
        "inLanguage": "en",
        "author": person_ld(),
        "creator": person_ld(),
        "datePublished": META["date_published"],
        "dateModified": META["date_modified"],
        "license": META["license_url"],
        "identifier": f'https://doi.org/{META["volume_doi"]}',
        "sameAs": f'https://doi.org/{META["volume_doi"]}',
        "isPartOf": {"@type": "CreativeWorkSeries", "name": META["volume"], "url": canonical([]),
                     "identifier": f'https://doi.org/{META["volume_doi"]}'},
        "publisher": {"@type": "Organization", "name": "Jamming Physics", "url": META["site"]},
        "position": n,
    }
    crumb_ld = breadcrumb_ld(segs, f'\u00a7{n} {ch["subj"]}')

    parts = [head(title, ch["desc"], segs, [article_ld, crumb_ld])]
    parts.append('<div class="layout">')
    parts.append(rail_html(segs, n))
    parts.append('<main id="main">')

    # breadcrumb (visible)
    parts.append(
        '<nav class="crumbs" aria-label="Breadcrumb">'
        f'<a href="{attr(relurl(segs, []))}">{esc(META["volume"])}</a>'
        f'<span aria-hidden="true">\u203a</span><span>\u00a7{n}</span></nav>'
    )

    parts.append("<article>")
    # header
    parts.append("<header>")
    parts.append(f'<p class="kicker">\u00a7{n} \u00b7 {esc(ch["subj"])}</p>')
    parts.append(f"<h1>{esc(ch['subj'])}</h1>")
    parts.append(claim_strip(ch["grade"], segs))
    parts.append(f'<p class="answer">{render_inline(ch["answer"])}</p>')
    parts.append(f'<p class="abstract">{render_inline(ch["abstract"])}</p>')
    parts.append("</header>")

    # cited locked quantities (self-contained cards)
    if ch.get("cards"):
        parts.append('<section class="cards" aria-label="Cited locked quantities">')
        for ck in ch["cards"]:
            parts.append(vp_card(ck, segs))
        parts.append("</section>")

    # body sections (each first sentence = direct answer)
    for sec in ch["sections"]:
        parts.append("<section class=\"sec\">")
        parts.append(f'<h2>{esc(sec["h2"])}</h2>')
        for p in sec["paras"]:
            parts.append(f"<p>{render_inline(p)}</p>")
        parts.append("</section>")

    # honest negatives
    parts.append('<section class="negatives" aria-label="Honest negatives">')
    parts.append("<h2>Honest negatives \u2014 what is <em>not</em> claimed</h2>")
    parts.append("<ol>")
    for neg in ch["negatives"]:
        parts.append(f"<li>{render_inline(neg)}</li>")
    parts.append("</ol></section>")

    # firewall
    parts.append('<aside class="firewall" aria-label="Firewall">')
    parts.append("<h2>Firewall</h2>")
    parts.append(f"<p>{render_inline(ch['firewall'])}</p>")
    parts.append("</aside>")

    parts.append("</article>")

    # prev / up / next
    prev_ch = C.CHAPTERS[n - 2] if n > 1 else None
    next_ch = C.CHAPTERS[n] if n < total else None
    pn = ['<nav class="prevnext" aria-label="Chapter navigation">']
    if prev_ch:
        pn.append(f'<a class="pn prev" rel="prev" href="{attr(relurl(segs, [prev_ch["slug"]]))}">'
                  f'<span>\u2190 \u00a7{prev_ch["n"]}</span>{esc(prev_ch["subj"])}</a>')
    else:
        pn.append('<span class="pn empty"></span>')
    pn.append(f'<a class="pn up" href="{attr(relurl(segs, []))}"><span>\u2191 contents</span>'
              f'{esc(META["volume"])}</a>')
    if next_ch:
        pn.append(f'<a class="pn next" rel="next" href="{attr(relurl(segs, [next_ch["slug"]]))}">'
                  f'<span>\u00a7{next_ch["n"]} \u2192</span>{esc(next_ch["subj"])}</a>')
    else:
        pn.append('<span class="pn empty"></span>')
    pn.append("</nav>")
    parts.append("".join(pn))

    parts.append(footer_html())
    parts.append("</main></div>\n</body>\n</html>\n")
    return "".join(parts)


def build_concept(con):
    segs = ["concepts", con["slug"]]
    title = f'{con["name"]} \u2014 {META["volume"]}'
    term_ld = {
        "@context": "https://schema.org",
        "@type": "DefinedTerm",
        "name": con["name"],
        "description": con["short"],
        "url": canonical(segs),
        "inLanguage": "en",
        "inDefinedTermSet": {"@type": "DefinedTermSet", "name": f'{META["volume"]} \u2014 concepts',
                             "url": canonical([]),
                             "identifier": f'https://doi.org/{META["volume_doi"]}'},
    }
    crumb_ld = breadcrumb_ld(segs, con["name"])

    parts = [head(title, con["short"], segs, [term_ld, crumb_ld])]
    parts.append('<div class="layout">')
    parts.append(rail_html(segs, -1))
    parts.append('<main id="main">')
    parts.append(
        '<nav class="crumbs" aria-label="Breadcrumb">'
        f'<a href="{attr(relurl(segs, []))}">{esc(META["volume"])}</a>'
        f'<span aria-hidden="true">\u203a</span><span>concepts</span>'
        f'<span aria-hidden="true">\u203a</span><span>{esc(con["name"])}</span></nav>'
    )
    parts.append("<article class=\"concept\">")
    parts.append("<header>")
    parts.append('<p class="kicker">concept</p>')
    parts.append(f"<h1>{esc(con['name'])}</h1>")
    parts.append(f'<code class="concept-term">{esc(con["term"])}</code>')
    parts.append(f'<p class="answer">{render_inline(con["short"])}</p>')
    parts.append("</header>")
    parts.append('<section class="sec">')
    for p in con["body"]:
        parts.append(f"<p>{render_inline(p)}</p>")
    parts.append("</section>")
    parts.append("</article>")
    parts.append(
        '<nav class="prevnext" aria-label="Navigation">'
        f'<a class="pn up" href="{attr(relurl(segs, []))}"><span>\u2191 contents</span>'
        f'{esc(META["volume"])}</a></nav>'
    )
    parts.append(footer_html())
    parts.append("</main></div>\n</body>\n</html>\n")
    return "".join(parts)


def build_hub():
    segs = []
    title = f'{META["volume"]} \u2014 {META["subtitle"]}'
    series_ld = {
        "@context": "https://schema.org",
        "@type": "CreativeWorkSeries",
        "name": META["volume"],
        "alternateName": META["subtitle"],
        "url": canonical([]),
        "inLanguage": "en",
        "author": person_ld(),
        "creator": person_ld(),
        "license": META["license_url"],
        "identifier": f'https://doi.org/{META["volume_doi"]}',
        "sameAs": f'https://doi.org/{META["volume_doi"]}',
        "datePublished": META["date_published"],
        "dateModified": META["date_modified"],
        "publisher": {"@type": "Organization", "name": "Jamming Physics", "url": META["site"]},
        "hasPart": [
            {"@type": "ScholarlyArticle", "name": ch["subj"], "position": ch["n"],
             "url": canonical([ch["slug"]]), "description": ch["desc"]}
            for ch in C.CHAPTERS
        ],
    }
    crumb_ld = breadcrumb_ld([], META["volume"])

    parts = [head(title, META["subtitle"], segs, [series_ld, crumb_ld])]
    parts.append('<div class="layout">')
    parts.append(rail_html(segs, -1))
    parts.append('<main id="main">')

    parts.append("<article class=\"hub\">")
    parts.append("<header>")
    parts.append('<p class="kicker">A falsifiable emergence \u00b7 lab notebook</p>')
    parts.append(f"<h1>{esc(META['volume'])}</h1>")
    parts.append(f'<p class="lede">{esc(META["subtitle"])}</p>')
    parts.append(claim_strip("forced", segs))
    parts.append(
        '<p class="answer">'
        + render_inline(
            "This volume emerges hearing from one inherited cubic and one inherited place map. "
            "The R19 switch \u1e61 = g\u00b7s \u2212 s\u00b3 + h supplies detection, cube-root amplification, "
            "and the deafness failure modes; the \u221a-law place map CF(x) supplies pitch-by-place across "
            "[[cf_apex]]\u2013[[cf_base]]. Every magnitude that is not forced is named as an open obstacle [O]."
        )
        + "</p>"
    )
    parts.append("</header>")

    # contents
    parts.append('<section class="toc" aria-label="Contents">')
    parts.append("<h2>Contents</h2>")
    parts.append('<ol class="toc-list">')
    for ch in C.CHAPTERS:
        tok, _, cls = PAGE_BADGE[ch["grade"]]
        parts.append(
            "<li>"
            f'<a class="toc-link" href="{attr(relurl(segs, [ch["slug"]]))}">'
            f'<span class="toc-n">\u00a7{ch["n"]}</span>'
            f'<span class="toc-title">{esc(ch["subj"])}</span>'
            f'<span class="grade {cls}" data-grade="{tok}">[{tok}]</span></a>'
            f'<p class="toc-desc">{render_inline(ch["desc"])}</p>'
            "</li>"
        )
    parts.append("</ol></section>")

    # concepts index
    parts.append('<section class="concept-index" aria-label="Concepts">')
    parts.append("<h2>Locked concepts</h2>")
    parts.append('<div class="cgrid">')
    for con in C.CONCEPTS:
        parts.append(
            '<a class="ccard" href="' + attr(relurl(segs, ["concepts", con["slug"]])) + '">'
            f'<span class="ccard-name">{esc(con["name"])}</span>'
            f'<code class="ccard-term">{esc(con["term"])}</code></a>'
        )
    parts.append("</div></section>")

    # honest open-obstacle ledger
    parts.append('<section class="oledger" aria-label="Open-obstacle ledger">')
    parts.append("<h2>Open-obstacle ledger \u2014 every named [O]</h2>")
    parts.append('<p class="oledger-note">'
                 + render_inline("Honesty is the method: each chapter forces a direction and an exponent, "
                                 "then names the magnitude it cannot supply without tuning. These are the "
                                 "live obstacles, not omissions.")
                 + "</p>")
    parts.append('<table class="oledger-table"><thead><tr>'
                 "<th>\u00a7</th><th>Open obstacle</th><th>Why it stays open</th>"
                 "</tr></thead><tbody>")
    for sec, obstacle, why in C.O_LEDGER:
        parts.append(f"<tr><td>{esc(sec)}</td><td>{render_inline(obstacle)}</td>"
                     f"<td>{render_inline(why)}</td></tr>")
    parts.append("</tbody></table></section>")

    parts.append("</article>")
    parts.append(footer_html())
    parts.append("</main></div>\n</body>\n</html>\n")
    return "".join(parts)


# --------------------------------------------------------------------------------------------
SITE_CSS = """\
/* Hearing from First Principles — tonotopic lab-notebook.
   Color ENCODES grade: green = established (forced/verified), amber = open obstacle, teal = trace. */
:root{
  --paper:#fbfaf6; --panel:#ffffff; --ink:#1a2422; --muted:#5c6a66; --faint:#8b958f;
  --rule:#e7e3d8; --rule-strong:#d8d3c4;
  --teal:#0e7c86; --teal-deep:#0a5b63; --amber:#b45309; --green:#1f6f43;
  --cited:#6b6052; --handoff:#5b6a78;
  --mono:ui-monospace,"SF Mono","Cascadia Mono","Roboto Mono",Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"Noto Sans",sans-serif;
  --measure:64ch;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--sans); font-size:17px; line-height:1.62;
  font-feature-settings:"kern" 1,"liga" 1;
}
.skip{position:absolute;left:-999px;top:0;background:var(--ink);color:#fff;padding:.5rem .8rem;z-index:20}
.skip:focus{left:.5rem;top:.5rem}
a{color:var(--teal-deep);text-decoration:none}
a:hover{color:var(--teal);text-decoration:underline;text-underline-offset:2px}

/* layout: tonotopic rail + reading column */
.layout{display:flex;align-items:flex-start;gap:0;max-width:1180px;margin:0 auto}
.rail{
  position:sticky;top:0;flex:0 0 200px;align-self:flex-start;
  height:100vh;padding:1.4rem 0 1.4rem 1.1rem;
  border-right:1px solid var(--rule);background:linear-gradient(180deg,#fbfaf6, #f6f4ec);
  display:flex;flex-direction:column;gap:.6rem;
}
.rail-home{font-weight:680;font-size:1.02rem;line-height:1.18;color:var(--ink);padding-right:1rem}
.rail-home span{display:block;font-weight:400;font-size:.74rem;letter-spacing:.02em;color:var(--muted)}
.rail-home:hover{text-decoration:none;color:var(--teal-deep)}
.rail-svg{width:170px;height:300px;margin-top:.3rem}
.rail-svg .spine{stroke:var(--rule-strong);stroke-width:2}
.rail-svg .node{fill:var(--panel);stroke:var(--teal);stroke-width:2}
.rail-svg .node.on{fill:var(--teal);stroke:var(--teal-deep)}
.rail-link:hover .node{stroke:var(--teal-deep)}
.rail-num{font-family:var(--mono);font-size:12px;fill:var(--muted)}
.rail-link:hover .rail-num{fill:var(--ink)}
.rail-cap{font-family:var(--mono);font-size:10.5px;fill:var(--faint);letter-spacing:.06em;text-transform:uppercase}

main{flex:1 1 auto;min-width:0;padding:1.5rem clamp(1rem,4vw,3rem) 4rem;max-width:860px}

.crumbs{font-size:.82rem;color:var(--muted);margin:.2rem 0 1.4rem;font-family:var(--mono)}
.crumbs span{margin:0 .45rem;color:var(--faint)}
.crumbs a{color:var(--muted)}

.kicker{font-family:var(--mono);font-size:.76rem;letter-spacing:.06em;text-transform:uppercase;
  color:var(--teal-deep);margin:0 0 .35rem}
h1{font-size:clamp(1.7rem,3.4vw,2.5rem);line-height:1.12;letter-spacing:-.012em;margin:.1rem 0 .6rem;
  font-weight:720}
.lede{font-size:1.18rem;color:var(--muted);margin:.2rem 0 1rem;max-width:var(--measure)}

/* claim strip */
.claim-strip{display:flex;flex-wrap:wrap;align-items:center;gap:.5rem .7rem;margin:.7rem 0 1.2rem;
  padding:.55rem .7rem;background:var(--panel);border:1px solid var(--rule);border-radius:8px;
  font-family:var(--mono);font-size:.78rem}
.badge{font-weight:700;padding:.12rem .5rem;border-radius:5px;border:1px solid currentColor}
.badge.g-forced,.badge.g-verified{color:var(--green)}
.badge.g-open{color:var(--amber)}
.claim-strip .method{color:var(--muted)}
.claim-strip .repro{color:var(--teal-deep)}
.claim-strip .doi{color:var(--muted)}

.answer{font-size:1.12rem;line-height:1.6;margin:.4rem 0 1rem;max-width:var(--measure);
  padding-left:1rem;border-left:3px solid var(--teal)}
.abstract{color:#33403c;max-width:var(--measure);margin:0 0 1.6rem}

/* cited locked-quantity cards */
.cards{display:flex;flex-wrap:wrap;gap:.8rem;margin:0 0 2rem}
.vp-card{flex:1 1 240px;min-width:240px;background:var(--panel);border:1px solid var(--rule);
  border-left:3px solid var(--teal);border-radius:8px;padding:.7rem .85rem}
.vp-card-name{display:block;font-weight:680;font-size:.96rem;color:var(--ink)}
.vp-card-name:hover{color:var(--teal-deep);text-decoration:none}
.vp-card-term{display:block;font-family:var(--mono);font-size:.82rem;color:var(--teal-deep);
  margin:.25rem 0 .35rem;white-space:nowrap;overflow-x:auto}
.vp-card-short{font-size:.86rem;color:var(--muted);margin:0;line-height:1.5}

section.sec{margin:0 0 1.7rem;max-width:var(--measure)}
h2{font-size:1.28rem;line-height:1.25;margin:1.8rem 0 .55rem;font-weight:690;letter-spacing:-.005em}
section.sec p,.concept .sec p{margin:.55rem 0}
p{max-width:var(--measure)}

/* the number-as-readout: every displayed value is a vp-num span (gate-checked) */
.vp-num{font-family:var(--mono);font-size:.93em;background:#f1efe6;border:1px solid var(--rule-strong);
  border-radius:4px;padding:.02em .32em;white-space:nowrap;color:#21302c}

/* grade tokens — color carries the epistemic status */
.grade{font-family:var(--mono);font-size:.82em;font-weight:700;padding:0 .18em;border-radius:3px}
.g-forced,.g-verified{color:var(--green)}
.g-open{color:var(--amber);background:#fbf1e4}
.g-cited{color:var(--cited)}
.g-handoff{color:var(--handoff)}

/* honest negatives */
.negatives{margin:2.2rem 0 1.5rem;max-width:var(--measure);background:#faf7f0;
  border:1px solid var(--rule);border-radius:10px;padding:1rem 1.2rem 1.1rem}
.negatives h2{margin-top:.2rem;color:var(--amber)}
.negatives em{font-style:italic}
.negatives ol{margin:.4rem 0 0;padding-left:1.3rem}
.negatives li{margin:.5rem 0;font-size:.95rem;line-height:1.55}

/* firewall */
.firewall{margin:1.4rem 0 0;max-width:var(--measure);border-top:2px solid var(--rule-strong);padding-top:.7rem}
.firewall h2{font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--teal-deep);
  font-family:var(--mono);margin:.2rem 0 .3rem}
.firewall p{font-size:.9rem;color:var(--muted);margin:.2rem 0}

/* prev/next */
.prevnext{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.7rem;margin:2.5rem 0 0;
  border-top:1px solid var(--rule);padding-top:1.1rem}
.pn{display:flex;flex-direction:column;gap:.15rem;padding:.6rem .75rem;border:1px solid var(--rule);
  border-radius:8px;background:var(--panel);font-size:.9rem;color:var(--ink)}
.pn:hover{text-decoration:none;border-color:var(--teal);color:var(--teal-deep)}
.pn span{font-family:var(--mono);font-size:.74rem;color:var(--muted)}
.pn.next{text-align:right}.pn.up{text-align:center}
.pn.empty{border:none;background:none}

/* footer */
.vol-foot{margin:3rem 0 0;border-top:1px solid var(--rule);padding-top:1.1rem;font-size:.82rem;
  color:var(--muted);max-width:var(--measure)}
.vol-foot p{margin:.3rem 0}
.vol-foot .ver{font-family:var(--mono);font-size:.74rem;color:var(--faint)}

/* hub */
.hub .toc-list{list-style:none;margin:.5rem 0 0;padding:0}
.hub .toc-list>li{margin:0 0 1rem;padding:0 0 1rem;border-bottom:1px solid var(--rule)}
.toc-link{display:flex;align-items:baseline;gap:.6rem;font-size:1.12rem;font-weight:640;color:var(--ink)}
.toc-link:hover{text-decoration:none;color:var(--teal-deep)}
.toc-n{font-family:var(--mono);color:var(--teal-deep);font-size:.95rem;flex:0 0 auto}
.toc-title{flex:1 1 auto}
.toc-desc{margin:.35rem 0 0;font-size:.92rem;color:var(--muted);max-width:none}
.concept-index .cgrid{display:flex;flex-wrap:wrap;gap:.8rem;margin:.6rem 0 0}
.ccard{flex:1 1 220px;min-width:220px;background:var(--panel);border:1px solid var(--rule);
  border-left:3px solid var(--teal);border-radius:8px;padding:.7rem .85rem}
.ccard:hover{text-decoration:none;border-color:var(--teal)}
.ccard-name{display:block;font-weight:660;color:var(--ink)}
.ccard-term{display:block;font-family:var(--mono);font-size:.8rem;color:var(--teal-deep);margin-top:.25rem;
  white-space:nowrap;overflow-x:auto}
.oledger{margin:2.4rem 0 0}
.oledger-note{font-size:.92rem;color:var(--muted);max-width:var(--measure)}
.oledger-table{width:100%;border-collapse:collapse;margin:.7rem 0 0;font-size:.9rem}
.oledger-table th,.oledger-table td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--rule);
  vertical-align:top}
.oledger-table th{font-family:var(--mono);font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;
  color:var(--muted);border-bottom:2px solid var(--rule-strong)}
.oledger-table td:first-child{font-family:var(--mono);color:var(--teal-deep);white-space:nowrap}

/* concept page */
.concept-term,.concept .concept-term{display:inline-block;font-family:var(--mono);font-size:1rem;
  color:var(--teal-deep);background:#f1efe6;border:1px solid var(--rule-strong);border-radius:5px;
  padding:.2rem .5rem;margin:.2rem 0 .6rem}

@media (max-width:880px){
  .rail{position:static;height:auto;flex-basis:auto;width:100%;flex-direction:row;align-items:center;
    gap:1rem;border-right:none;border-bottom:1px solid var(--rule);padding:.8rem 1rem;overflow-x:auto}
  .rail-svg{height:64px;width:auto;transform:rotate(-90deg);transform-origin:left center;display:none}
  .layout{flex-direction:column}
  main{max-width:none;padding-top:1rem}
  .prevnext{grid-template-columns:1fr}
  .pn.next{text-align:left}.pn.up{text-align:left}
}
"""


def sitemap_xml(pages):
    rows = []
    for segs in pages:
        rows.append(
            "  <url>\n"
            f"    <loc>{html.escape(canonical(segs))}</loc>\n"
            f"    <lastmod>{META['date_modified']}</lastmod>\n"
            "  </url>"
        )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(rows) + "\n</urlset>\n")


def robots_txt():
    base = META["canonical_base"].rstrip("/")
    bots = ["GPTBot", "ClaudeBot", "Claude-Web", "anthropic-ai", "Google-Extended",
            "PerplexityBot", "CCBot", "Bytespider", "Applebot-Extended"]
    lines = ["# Hearing from First Principles — research volume, openly licensed (CC BY 4.0).",
             "# AI crawlers welcome: this is meant to be read and cited by models.",
             "User-agent: *", "Allow: /", ""]
    for b in bots:
        lines += [f"User-agent: {b}", "Allow: /", ""]
    lines += [f"Sitemap: {base}/sitemap.xml", ""]
    return "\n".join(lines)


def llms_txt():
    L = []
    L.append(f"# {META['volume']}")
    L.append("")
    L.append(f"> {META['subtitle']}")
    L.append("")
    L.append(f"Author: {META['author']} (ORCID {META['orcid']}). License: {META['license']}. "
             f"Source: {META['repo']}.")
    L.append(f"Readable-layer source (DNA volume): doi:{META['dna_doi']}. "
             f"This volume's concept DOI: doi:{META['volume_doi']}.")
    L.append("")
    L.append("Method: every page LOCKs an inherited quantity, DERIVEs a forced direction or exponent, "
             "then GATEs it. Every displayed number is reproduced bit-for-bit from verified code "
             "(no number is hand-typed or fitted); every magnitude that is not forced is named as an "
             "open obstacle [O]. Grades: [F] forced, [V] verified, [O] open obstacle, [L] cited literature.")
    L.append("")
    L.append("## Chapters")
    L.append("")
    for ch in C.CHAPTERS:
        url = canonical([ch["slug"]])
        # strip [[KEY]] and [X] tokens from the description for the plain-text index
        desc = _GRADE_RE.sub(lambda m: "", _NUM_RE.sub(lambda m: S.disp(m.group(1)), ch["desc"]))
        desc = re.sub(r"\s+", " ", desc).strip()
        L.append(f"- [\u00a7{ch['n']} {ch['subj']}]({url}): {desc}")
    L.append("")
    L.append("## Concepts")
    L.append("")
    for con in C.CONCEPTS:
        url = canonical(["concepts", con["slug"]])
        short = re.sub(r"\s+", " ", _GRADE_RE.sub(lambda m: "", con["short"])).strip()
        L.append(f"- [{con['name']}]({url}): {short}")
    L.append("")
    L.append("## Open obstacles")
    L.append("")
    for sec, obstacle, why in C.O_LEDGER:
        obstacle = re.sub(r"\s+", " ", _GRADE_RE.sub(lambda m: "", obstacle)).strip()
        why = re.sub(r"\s+", " ", _GRADE_RE.sub(lambda m: "", why)).strip()
        L.append(f"- {sec}: {obstacle} — {why}")
    L.append("")
    return "\n".join(L)


# --------------------------------------------------------------------------------------------
def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    # determinism guard: SSOT must be stable within this build
    if S.canonical_sha256() != S.canonical_sha256():
        raise SystemExit("SSOT non-deterministic within build")

    outputs = []   # (relpath, text) in deterministic order -> concatenated for the build hash

    # hub
    outputs.append(("index.html", build_hub()))
    # chapters (in §-order)
    for ch in C.CHAPTERS:
        outputs.append((f'{ch["slug"]}/index.html', build_chapter(ch)))
    # concepts (in declared order)
    for con in C.CONCEPTS:
        outputs.append((f'concepts/{con["slug"]}/index.html', build_concept(con)))

    # static assets / SEO
    page_segs = [[]] + [[ch["slug"]] for ch in C.CHAPTERS] + [["concepts", c["slug"]] for c in C.CONCEPTS]
    outputs.append(("assets/css/site.css", SITE_CSS))
    outputs.append(("sitemap.xml", sitemap_xml(page_segs)))
    outputs.append(("robots.txt", robots_txt()))
    outputs.append(("llms.txt", llms_txt()))

    # write all
    for rel, text in outputs:
        write(os.path.join(DOCS, rel), text)

    # build hash = sha256 over (relpath \n length \n body) for every output, sorted by relpath
    h = hashlib.sha256()
    for rel, text in sorted(outputs):
        b = text.encode("utf-8")
        h.update(rel.encode("utf-8")); h.update(b"\n")
        h.update(str(len(b)).encode("utf-8")); h.update(b"\n")
        h.update(b); h.update(b"\n")
    digest = h.hexdigest()

    print("pages:", 1 + len(C.CHAPTERS) + len(C.CONCEPTS),
          "| files:", len(outputs),
          "| ssot:", S.canonical_sha256()[:12])
    print("\nsha256:", digest)
    return digest


if __name__ == "__main__":
    main()
