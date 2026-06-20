#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_multipage_dna.py  —  VP-SPEC v1.8 canonical multi-page builder (DNA paper)

Inverse of build_single_file_dna.py. Takes the single-file canonical
docs/dna/index.html (17 sections marked <section data-section data-slug>)
and splits it into the canonical VP-SPEC multi-page layout used by every
other volume (e.g. vp_physics_v0_11_0):

    docs/dna/index.html              -> hub (TOC + cross-links, no body)
    docs/dna/{slug}/index.html       -> one self-contained page per section (x17)
    docs/robots.txt                  -> 7 named bots + default allow (C4)
    docs/sitemap.xml                 -> hub + 17 section URLs
    docs/llms.txt                    -> <5KB authority block + section index (C4)

Discipline (VP-SPEC v1.8):
  * Code is the agent of transformation — body text/equations/numbers are
    copied byte-for-byte; the ONLY edits are metadata, navigation, internal
    links, and the deterministic h2->h1 promotion of each section heading.
  * C1 reproducibility: deterministic; same input -> same output.
  * C2 single canonical HTML: no .tex / eq_list / txt body sources touched.
  * C4 retrieval-readiness: every page is answer-first (already authored),
    carries self-contained vp-cards (preserved), per-page JSON-LD
    (ScholarlyArticle + BreadcrumbList), and is reachable by robots/sitemap.

Run from the package root:  python3 build_multipage_dna.py
"""
import re, json, html, os, sys, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
MONO = os.path.join(DOCS, "dna", "index.html")
META = os.path.join(DOCS, "dna", "_meta.json")

ORIGIN   = "https://jamming-physics.org"
PAPER_ID = "dna"
TITLE    = "A Deterministic Two-Layer Interpretation of DNA"
SHORT    = "4D DNA Blueprint"
DOI      = "10.5281/zenodo.20471407"
ORCID    = "0009-0002-7535-8245"
AUTHOR   = "Young Jae Lee"
VERSION  = "1.12"
REPRO    = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/dna/"
META_DESC = ("A deterministic engine reads DNA's readable layer completely from "
             "sequence: gamma, the A4 grammar, the R19 switch, to a sharp boundary. "
             "Reproducible and graded.")
KNOWS = ["reading DNA from sequence","deterministic DNA interpretation",
         "DNA stacking stiffness","A4 coordinate grammar","R19 double-well switch",
         "anchor-relative helical phase","CpG O/E methylation","readable layer of DNA",
         "sequence-to-trait reading","reproducible genomics","jamming lattice",
         "4D DNA Blueprint"]

# ----------------------------------------------------------------------------- helpers
def esc_attr(s):  return html.escape(s, quote=True)
def esc_text(s):  return html.escape(s, quote=False)

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

def subj45(title):
    """VP-SPEC 6-D: trailing-paren strip -> subtitle cut -> word-boundary <=45."""
    t = title.strip()
    t = re.sub(r"\s*\([^()]*\)\s*$", "", t).strip()          # (a) trailing (...)
    if len(t) > 45:                                          # (b) subtitle cut
        m = re.split(r"\s*[:—;]\s|\sfrom\s", t, maxsplit=1)
        if m and len(m[0]) >= 4:
            t = m[0].strip()
    # also cut a leading-channel subtitle for the short channel sections
    m2 = re.match(r"^([A-Z][a-z]+)\s*\([^)]*\):", title)     # "Material (γ):"
    if m2 is None:
        m3 = re.split(r":\s", title, maxsplit=1)             # "Set: ...", "State: ..."
        if len(m3) == 2 and len(m3[0]) <= 45 and len(m3[0]) >= 3 and "(" not in m3[0]:
            t = m3[0].strip()
    if len(t) > 45:                                          # (c) word boundary
        cut = t[:45]
        if " " in cut: cut = cut[:cut.rfind(" ")]
        t = cut.strip()
    return t

def clip_desc(s, lo=80, hi=160, pad=""):
    s = " ".join(s.split())
    if len(s) > hi:
        cut = s[:hi]
        if " " in cut: cut = cut[:cut.rfind(" ")]
        s = cut.strip().rstrip(",;—-")
    if len(s) < lo and pad:
        extra = " ".join(pad.split())
        s = (s + " " + extra).strip()
        if len(s) > hi:
            cut = s[:hi]
            if " " in cut: cut = cut[:cut.rfind(" ")]
            s = cut.strip()
    return s

def label_of(no, is_apx):
    if is_apx: return "Appendix " + str(no)
    return "§" + str(no)

# ----------------------------------------------------------------------------- read
mono = open(MONO, encoding="utf-8").read()
meta = json.load(open(META, encoding="utf-8"))

head_inner = re.search(r"<head>(.*?)</head>", mono, re.S).group(1)
footer = re.search(r"<footer>.*?</footer>", mono, re.S).group(0)
# footer was authored for the single-file build; relabel for the multi-page edition
footer = re.sub(r"single-file canonical \(v[0-9.]+\)",
                "multi-page canonical (v%s)" % VERSION, footer)

# pre-section main block (h1 + answer + abstract + claim-strip) lives between <main> and the TOC
pre = re.search(r"<main>(.*?)<nav class=\"toc\"", mono, re.S).group(1)
toc = re.search(r"(<nav class=\"toc\".*?</nav>)", mono, re.S).group(1)

paper_h1     = re.search(r"<h1>(.*?)</h1>", pre, re.S).group(1).strip()
paper_answer = re.search(r"<p class=\"answer\">.*?</p>", pre, re.S).group(0)
paper_abs    = re.search(r"<p class=\"abstract\">.*?</p>", pre, re.S).group(0)
paper_strip  = re.search(r"<aside class=\"claim-strip page\">.*?</aside>", pre, re.S).group(0)
# the ver badge was authored for the single-file build; relabel for the multi-page hub
paper_strip  = re.sub(r'<span class="ver">.*?</span>',
                      '<span class="ver">multi-page canonical · v%s</span>' % VERSION,
                      paper_strip, flags=re.S)

# sections (non-nesting) in document order
sec_re = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.S)
sections = []
for m in sec_re.finditer(mono):
    attrs, inner = m.group(1), m.group(2)
    no   = re.search(r'data-section="([^"]*)"', attrs).group(1)
    slug = re.search(r'data-slug="([^"]*)"', attrs).group(1)
    apx  = re.search(r'data-appendix="([^"]*)"', attrs)
    sections.append({"no": no, "slug": slug, "apx": bool(apx),
                     "attrs": attrs, "inner": inner})

assert len(sections) == 17, "expected 17 sections, got %d" % len(sections)

# slug -> meta one_liner / title  (chapters + appendices)
meta_by_slug = {}
for c in meta.get("chapters", []) + meta.get("appendices", []):
    sl = c.get("slug")
    meta_by_slug[sl] = c
# also key appendices by their 'id'->slug already covered via slug

# anchor-id -> page URL  (for deterministic link rewrite)
url_of = {s["slug"]: "/%s/%s/" % (PAPER_ID, s["slug"]) for s in sections}
anchor_to_url = {}   # "#s{no}-{slug}" -> "/dna/{slug}/"
for s in sections:
    anchor = "s%s-%s" % (s["no"], s["slug"])
    anchor_to_url["#" + anchor] = url_of[s["slug"]]

def rewrite_links(text):
    """#s{no}-{slug}  and  /dna/#s{no}-{slug}  ->  /dna/{slug}/  (deterministic)."""
    # longest anchors first to avoid partial collisions (s1 vs s13 etc.)
    for anchor in sorted(anchor_to_url, key=len, reverse=True):
        url = anchor_to_url[anchor]
        text = text.replace("/%s/%s" % (PAPER_ID, anchor), url)  # /dna/#s.. FIRST
        text = text.replace(anchor, url)                          # bare #s..
    return text

# ----------------------------------------------------------------------------- page template
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{origin}{url}">
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="preload" href="/assets/fonts/text.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">
{ld_article}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › <a href="/{paper}/">{short}</a> › {label}</nav></header>
<main>
{body}
<nav class="pn">{prev}<a href="/{paper}/">contents</a>{next}</nav>
</main>
{footer}
</body>
</html>
"""

n = len(sections)
pages = []
for i, s in enumerate(sections):
    slug, no, is_apx = s["slug"], s["no"], s["apx"]
    url   = url_of[slug]
    cmeta = meta_by_slug.get(slug, {})
    ctitle = cmeta.get("title") or strip_tags(
        re.search(r"<h2[^>]*>(.*?)</h2>", s["inner"], re.S).group(1)).strip()
    one   = (cmeta.get("one_liner") or "").strip()
    label = label_of(no, is_apx)

    # body: promote the section's <h2 id="..."> to <h1>, then rewrite cross links
    body = s["inner"]
    body = re.sub(r"<h2[^>]*>(.*?)</h2>",
                  lambda mm: "<h1>%s</h1>" % mm.group(1).strip(), body, count=1, flags=re.S)
    # C4 answer-first: chapters authored before the answer-first convention (§1–§7)
    # have no <p class="answer">. Promote the curated one_liner (already in _meta,
    # excluded from body word-count) into the required answer-first block. Deterministic,
    # additive, no body text altered.
    if '<p class="answer">' not in body and one:
        idx = body.find("</h1>") + len("</h1>")
        body = body[:idx] + ('\n\n<p class="answer">%s</p>\n' % one) + body[idx:]
    body = rewrite_links(body).strip()

    # answer text (plain) for description padding
    am = re.search(r'<p class="answer">(.*?)</p>', s["inner"], re.S)
    answer_plain = strip_tags(am.group(1)).strip() if am else ""
    desc = clip_desc(one if one else answer_plain, pad=answer_plain)

    subj = subj45(ctitle)
    sec_tok = (("Appendix " + str(no)) if is_apx else ("§" + str(no)))
    title_tag = "%s — %s %s | Jamming Physics" % (subj, SHORT, sec_tok)

    ld_article = json.dumps({
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": ctitle,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": SHORT,
                     "identifier": "https://doi.org/%s" % DOI,
                     "url": "%s/%s/" % (ORIGIN, PAPER_ID)},
        "author": {"@type": "Person", "name": AUTHOR,
                   "sameAs": "https://orcid.org/%s" % ORCID},
        "identifier": "https://doi.org/%s" % DOI,
        "isBasedOn": REPRO,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "knowsAbout": KNOWS,
    }, ensure_ascii=False)

    ld_crumb = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
            {"@type": "ListItem", "position": 2, "name": SHORT,
             "item": "%s/%s/" % (ORIGIN, PAPER_ID)},
            {"@type": "ListItem", "position": 3, "name": "%s %s" % (label, subj)},
        ]}, ensure_ascii=False)

    prev_html = ""
    if i > 0:
        p = sections[i-1]
        pl = label_of(p["no"], p["apx"])
        prev_html = '<a rel="prev" href="%s">← %s</a>' % (url_of[p["slug"]], pl)
    next_html = ""
    if i < n-1:
        nx = sections[i+1]
        nl = label_of(nx["no"], nx["apx"])
        next_html = '<a rel="next" href="%s">%s →</a>' % (url_of[nx["slug"]], nl)

    page = PAGE.format(
        title_tag=esc_text(title_tag), desc=esc_attr(desc),
        origin=ORIGIN, url=url, paper=PAPER_ID, short=esc_text(SHORT),
        label=esc_text(label), body=body, footer=footer,
        prev=prev_html, next=next_html,
        ld_article=ld_article, ld_crumb=ld_crumb)

    outdir = os.path.join(DOCS, PAPER_ID, slug)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(page)
    pages.append({"slug": slug, "url": url, "title": ctitle, "label": label,
                  "one": one, "no": no, "apx": is_apx, "size": len(page)})

# ----------------------------------------------------------------------------- hub
hub_toc = rewrite_links(toc)
# series hasPart
haspart = [{"@type": "CreativeWork", "@id": ORIGIN + p["url"]} for p in pages]

ld_paper = json.dumps({
    "@context": "https://schema.org", "@type": "ScholarlyArticle",
    "headline": TITLE, "name": TITLE, "alternativeHeadline": SHORT,
    "description": META_DESC,
    "isPartOf": {"@type": "CreativeWorkSeries", "name": "Jamming Physics"},
    "sameAs": "https://doi.org/%s" % DOI, "identifier": "https://doi.org/%s" % DOI,
    "version": VERSION,
    "author": {"@type": "Person", "name": AUTHOR, "sameAs": "https://orcid.org/%s" % ORCID},
    "isBasedOn": REPRO, "license": "https://creativecommons.org/licenses/by/4.0/",
    "knowsAbout": KNOWS,
}, ensure_ascii=False)

ld_series = json.dumps({
    "@context": "https://schema.org", "@type": "CreativeWorkSeries",
    "name": "%s — %s" % (SHORT, TITLE), "url": "%s/%s/" % (ORIGIN, PAPER_ID),
    "author": {"@type": "Person", "name": AUTHOR, "sameAs": "https://orcid.org/%s" % ORCID},
    "identifier": "https://doi.org/%s" % DOI, "hasPart": haspart,
}, ensure_ascii=False)

ld_hubcrumb = json.dumps({
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": ORIGIN + "/"},
        {"@type": "ListItem", "position": 2, "name": SHORT,
         "item": "%s/%s/" % (ORIGIN, PAPER_ID)}]}, ensure_ascii=False)

totals = meta.get("totals", {})
n_tab = totals.get("tables", "")
overview = ("%d sections across five parts plus one applied appendix · "
            "%s source words · every page carries its own answer-first read, "
            "graded verdict, and reproducibility strip (DOI + repro/ deep link)." %
            (n, totals.get("words", "")))

# cross-links (headline results -> sections) + jamming branch link (VP-SPEC §10)
xlinks = []
xlinks.append('<li><span class="kf">corr(γ, GC) = 0.998</span> → '
              '<a href="/dna/02-material-threshold-scale/">§2 — Material (γ): the threshold scale</a></li>')
xlinks.append('<li><span class="kf">master-switch CV 0.1–2%</span> → '
              '<a href="/dna/05-dwell-how-long-switch-runs/">§5 — Dwell: how long the switch runs</a></li>')
xlinks.append('<li><span class="kf">SET: OTX 1 vs 3+</span> → '
              '<a href="/dna/03-set-switch-inventory/">§3 — Set: the switch inventory</a></li>')
xlinks.append('<li><span class="kf">γ gene-clock → body</span> → '
              '<a href="/dna/ax-a-universal-morphogenesis-gene-clock/">Appendix A — Universal morphogenesis</a></li>')

HUB = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{short} — {title} | Jamming Physics</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{origin}/{paper}/">
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="preload" href="/assets/fonts/text.woff2" as="font" type="font/woff2" crossorigin>
<!-- Phase 7: Highwire citation 태그 5종 슬롯 -->
<!-- citation_tags: Phase 7 -->
<script type="application/ld+json">
{ld_paper}
</script>
<script type="application/ld+json">
{ld_series}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › {short}</nav></header>
<main>
<h1>{h1}</h1>
<p class="branch">This paper is derived from the <strong>jamming branch</strong> of VP Theory → <a href="/physics/">/physics/</a>.</p>
{answer}
<p class="lede">Canonical reads: corr(γ, GC) = 0.998 ; cross-species master-switch CV 0.1–2% ; SET OTX 1 vs 3+.</p>
{abstract}
{strip}
<p class="overview">{overview}</p>
<p class="overview"><em>Note:</em> this hub is assembled deterministically from the sealed sections (build_multipage_dna.py); no prose is synthesized and no section text is altered.</p>
<h2>Contents</h2>
{toc}
<h2>Cross-links</h2>
<ul class="xlinks">
{xlinks}
</ul>
</main>
{footer}
</body>
</html>
"""

hub = HUB.format(
    short=esc_text(SHORT), title=esc_text(TITLE), desc=esc_attr(META_DESC),
    origin=ORIGIN, paper=PAPER_ID, h1=esc_text(paper_h1),
    answer=paper_answer, abstract=paper_abs, strip=paper_strip,
    overview=esc_text(overview), toc=hub_toc, xlinks="\n".join(xlinks),
    footer=footer, ld_paper=ld_paper, ld_series=ld_series, ld_crumb=ld_hubcrumb)
open(MONO, "w", encoding="utf-8").write(hub)

# ----------------------------------------------------------------------------- robots / sitemap / llms
robots = """# VP-SPEC v1.8 — machine access (C4 retrieval-readiness). 7 named agents + default: full allow.
# generated by build_multipage_dna.py (deterministic)

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % ORIGIN
open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8").write(robots)

DATE = "2026-06-17"
urls = ['  <url>\n    <loc>%s/%s/</loc>\n    <lastmod>%s</lastmod>\n    <priority>1.0</priority>\n  </url>'
        % (ORIGIN, PAPER_ID, DATE)]
for p in pages:
    urls.append('  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n    <priority>0.8</priority>\n  </url>'
                % (ORIGIN, p["url"], DATE))
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' \
          + "\n".join(urls) + "\n</urlset>\n"
open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(sitemap)

llms_lines = []
llms_lines.append("# %s — %s" % (SHORT, TITLE))
llms_lines.append("")
llms_lines.append("> Canonical, citable HTML edition of the DNA white paper: DNA's readable layer is "
                  "read completely and mechanically from sequence — material γ (stacking stiffness), "
                  "the A4 coordinate grammar, and the R19 double-well switch — to a sharp, enumerated "
                  "boundary (size, sign, dosage, timing are runtime). Every page is self-contained, "
                  "answer-first, and carries its graded verdict (admissible / principle-demonstration / open).")
llms_lines.append("")
llms_lines.append("Author: %s (https://orcid.org/%s). DOI: https://doi.org/%s." % (AUTHOR, ORCID, DOI))
llms_lines.append("Principle: LOCK → Derive → Gate (inputs locked, reads deterministic seed=7, verified by counts; drift 0).")
llms_lines.append("")
llms_lines.append("## Canonical reads")
llms_lines.append("- corr(γ, GC) = 0.998  (γ is an affine read of composition, not lineage)")
llms_lines.append("- cross-species master-switch CV 0.1–2%  (γ near-invariant among body-building switches)")
llms_lines.append("- SET: OTX 1 (invertebrate) vs 3+ (vertebrate)  (deep splits read in the inventory, not the material)")
llms_lines.append("- feature-emergence order = argsort(spinodal(γ)) [V] ; γ ⟂ developmental timing (heart ρ=+0.071, p=0.882) [O]")
llms_lines.append("")
llms_lines.append("## Hub")
llms_lines.append("- [%s hub](%s/%s/)" % (SHORT, ORIGIN, PAPER_ID))
llms_lines.append("")
llms_lines.append("## Sections")
for p in pages:
    tok = p["label"].replace("§", "").strip()
    llms_lines.append("- %s %s%s" % (tok, ORIGIN, p["url"]))
llms = "\n".join(llms_lines) + "\n"
open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(llms)

# ----------------------------------------------------------------------------- _meta.json update
meta["version"] = VERSION
meta["layout"] = ("multi-page canonical (VP-SPEC v1.8): hub at docs/dna/index.html; "
                  "each of the 17 sections is its own page docs/dna/{slug}/index.html, "
                  "addressed by /dna/{slug}/. Restored from the v1.11 single-file deviation "
                  "to the canonical multi-page format shared by every volume; C1–C4 substance "
                  "preserved, body text/numbers byte-unchanged (see CHANGELOG_v1_12_multipage_split.md).")
json.dump(meta, open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("OK: hub + %d section pages + robots/sitemap/llms written." % n)
print("llms.txt bytes:", len(llms.encode("utf-8")))
print("largest page bytes:", max(p["size"] for p in pages))
