#!/usr/bin/env python3
# =============================================================================
#  build_single_file_dna.py -- consolidate the 13 per-section DNA chapters into
#  ONE canonical self-contained HTML paper (author-directed v1.9), preserving the
#  VP-SPEC constitution substance (C1-C4): answer-first, self-contained passages,
#  vp-cards, claim-strips, grades, JSON-LD, machine-accessible static HTML.
#
#  It does NOT alter any science, number, or wording of the ported chapters. The
#  only authored edits are the v1.9 corrections, applied surgically:
#    - §10: a visible "superseded (v1.9)" note on the global ~10.4bp periodicity-
#           vs-shuffle helical claim, pointing to the §13 anchor-relative contact.
#    - §08: a retired-register tombstone for that helical claim (deprecate, keep).
#  Each chapter's <main> is ported verbatim except: headings demoted one level
#  (the paper has exactly one <h1>), per-chapter page-nav removed (replaced by the
#  single-file table of contents + section anchors). repro/ GitHub links are kept
#  (the verification layer is unchanged), so no claim-strip link breaks.
#  Deterministic: same inputs -> same output.
# =============================================================================
import os, re, json, html

REPO = os.path.dirname(os.path.abspath(__file__))
DNA  = os.path.join(REPO, "docs", "dna")
META = json.load(open(os.path.join(DNA, "_meta.json")))

DOI   = META["doi"]
TITLE = META["title"]
SHORT = META["short"]
ORCID = "0009-0002-7535-8245"

def chapter_main(slug):
    p = os.path.join(DNA, slug, "index.html")
    h = open(p, encoding="utf-8").read()
    return re.search(r"(?s)<main>(.*?)</main>", h).group(1)

def demote_headings(frag):
    # demote one level so the consolidated page keeps exactly one <h1>
    for a, b in (("h5", "h6"), ("h4", "h5"), ("h3", "h4"), ("h2", "h3"), ("h1", "h2")):
        frag = re.sub(rf"<{a}(\b[^>]*)>", rf"<{b}\1>", frag)
        frag = re.sub(rf"</{a}>", rf"</{b}>", frag)
    return frag

def strip_page_nav(frag):
    return re.sub(r"(?s)<nav class=\"pn\">.*?</nav>", "", frag)

def section_of(no, slug):
    frag = chapter_main(slug)
    frag = strip_page_nav(frag)
    frag = demote_headings(frag)            # h1->h2 (section title), h2->h3, ...
    anchor = f"s{no}-{slug}"
    # give the section's leading h2 the id so deep links land on the heading
    frag = re.sub(r"<h2(\b[^>]*)>", rf'<h2 id="{anchor}"\1>', frag, count=1)
    return anchor, f'<section data-section="{no}" data-slug="{slug}">\n{frag.strip()}\n</section>'

# ---- v1.9 surgical corrections (deprecate, do not delete) -------------------
SUPERSEDE_10 = (
 '\n<aside class="superseded" data-superseded="helical-global-periodicity">'
 '<b>⚠ Superseded (v1.9).</b> The reading just above — a ~10.4&nbsp;bp helical period scored at the '
 '100th percentile against a composition-matched shuffle — is an <i>absolute, global</i> periodicity '
 'statistic: a composition surrogate for nucleosome spacing read from an arbitrary window edge, not a '
 'statement about whether this element can contact a specific partner. The element-level structural read '
 'is the <b>anchor-relative</b> phase <code>contact_competent</code> of '
 '<a href="#s13-13-unified-deterministic-interpreter">§13</a> (whether a motor and its nearest anchor sit '
 'on the same rotational helical face). The global periodicity is kept only as a descriptive composition '
 'fact; it is <b>retired as a structural/contact claim</b> — see the '
 '<a href="#s8-08-bounds-open-questions-retired-claims">§8 retired register</a>.</aside>')

TOMBSTONE_08 = (
 ' <strong>Also retired (v1.9, irreversible):</strong> the <strong>global WW-ACF(10–11) helical '
 'periodicity</strong> as an element-level structural claim — the &ldquo;~10.4&nbsp;bp signal at the '
 '100th percentile against a composition-matched shuffle&rdquo; reading of the lactase chapter. It is '
 'superseded by the <strong>anchor-relative</strong> <code>contact_competent</code> read of '
 '<a href="#s13-13-unified-deterministic-interpreter">§13</a> and must not revive as a structural or '
 'contact claim under any name; the global periodicity statistic survives only as a descriptive '
 'composition fact about a genome, never as a coordinate read of an element.')

def apply_corrections(no, slug, section_html):
    if slug.startswith("10-"):
        # insert the superseded note right after the paragraph carrying the claim
        m = re.search(r'(?s)(<p[^>]*>[^<]*~?10\.4\s*bp helical period.*?</p>)', section_html)
        if not m:
            raise SystemExit("§10 helical-claim paragraph not found — aborting (no silent edit).")
        section_html = section_html[:m.end()] + SUPERSEDE_10 + section_html[m.end():]
    if slug.startswith("08-"):
        # append the tombstone inside the 'Retired register (irreversible)' paragraph
        anchor_txt = "The body of this paper carries no revived retired concept."
        if anchor_txt not in section_html:
            raise SystemExit("§08 retired-register anchor sentence not found — aborting.")
        section_html = section_html.replace(anchor_txt, anchor_txt + TOMBSTONE_08, 1)
    return section_html

# ---- assemble ---------------------------------------------------------------
order = sorted(META["chapters"], key=lambda c: c["no"])
anchors, sections = [], []
for c in order:
    a, s = section_of(c["no"], c["slug"])
    s = apply_corrections(c["no"], c["slug"], s)
    anchors.append((c["no"], a, c["title"], c.get("one_liner", ""), c.get("grade")))
    sections.append(s)

# table of contents (anchors -> sections)
toc_items = "\n".join(
    f'  <li><a href="#{a}"><span class="n">§{no}</span>{html.escape(title)}</a>'
    f'<span class="ol">{html.escape(ol)}</span></li>'
    for no, a, title, ol, _ in anchors)

# JSON-LD: one ScholarlyArticle for the whole paper, hasPart = the 13 sections
haspart = [{"@type": "WebPageElement", "name": f"§{no} {title}",
            "url": f"https://jamming-physics.org/dna/#{a}"} for no, a, title, _, _ in anchors]
ld_article = {
    "@context": "https://schema.org", "@type": "ScholarlyArticle",
    "headline": TITLE, "name": TITLE, "alternativeHeadline": SHORT,
    "isPartOf": {"@type": "CreativeWorkSeries", "name": "Jamming Physics"},
    "sameAs": f"https://doi.org/{DOI}", "identifier": f"https://doi.org/{DOI}",
    "version": "1.9",
    "author": {"@type": "Person", "name": "Young Jae Lee",
               "sameAs": f"https://orcid.org/{ORCID}"},
    "isBasedOn": "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/dna/",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "knowsAbout": ["DNA stacking stiffness", "R19 double-well", "DNA coordinate grammar",
                   "helical phase", "CpG O/E", "DNA methylation", "jamming lattice",
                   "reproducible computation"],
    "hasPart": haspart}
ld_crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jamming-physics.org/"},
    {"@type": "ListItem", "position": 2, "name": SHORT, "item": "https://jamming-physics.org/dna/"}]}

PAGE_ANSWER = (
 "This is one deterministic paper that reads DNA in two layers: a sequence-readable material and "
 "coordinate (Layer 1) and runtime quantities it flags but never assigns (Layer 2). The material γ "
 "(stacking stiffness) sets the R19 threshold scale but barely separates taxa; difference lives in the "
 "switch inventory, state, dwell, and the environment's methylation. §13 unifies γ, the A4 coordinate, "
 "and methylation into one engine.")

PAGE_ABSTRACT = html.escape(META["abstract"])

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A Deterministic Two-Layer Interpretation of DNA — 4D DNA Blueprint | Jamming Physics</title>
<meta name="description" content="One deterministic paper: the readable material γ sets the R19 threshold but barely separates taxa; difference lives in switch inventory, state, dwell, and environment-written methylation. A single engine unifies γ, the A4 coordinate, and the methylation regime.">
<link rel="canonical" href="https://jamming-physics.org/dna/">
<link rel="stylesheet" href="/assets/css/site.css">
<link rel="preload" href="/assets/fonts/text.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">
{json.dumps(ld_article, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(ld_crumb, ensure_ascii=False)}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › <a href="/dna/">{html.escape(SHORT)}</a></nav></header>
<main>
<h1>{html.escape(TITLE)}</h1>

<p class="answer">{PAGE_ANSWER}</p>

<p class="abstract">{PAGE_ABSTRACT}</p>

<aside class="claim-strip page">
  <span class="gate">LOCK → Derive → Gate</span>
  <a href="https://github.com/rego093-sketch/jamming-physics/tree/main/repro/dna/" rel="noopener">reproduce (GitHub)</a>
  <a href="https://doi.org/{DOI}" rel="noopener">DOI snapshot</a>
  <span class="ver">single-file canonical · v1.9</span>
</aside>

<nav class="toc" aria-label="Contents">
<ol>
{toc_items}
</ol>
</nav>

{chr(10).join(sections)}

</main>
<footer>Young Jae Lee · ORCID {ORCID} · DOI {DOI} · CC BY 4.0 · single-file canonical (v1.9)</footer>
</body>
</html>
"""

OUT = os.path.join(DNA, "index.html")
open(OUT, "w", encoding="utf-8").write(doc)
print("wrote", os.path.relpath(OUT, REPO), f"({len(doc)/1024:.1f} KB)")
print("sections:", len(sections), "| anchors:", [a for _, a, *_ in anchors][:3], "...")
