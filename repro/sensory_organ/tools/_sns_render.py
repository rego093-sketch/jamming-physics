#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_sns_render.py -- VP-SPEC v1.8 rendering engine for the Special-Sense Organs whitepaper.

Pure, deterministic rendering: authored chapter data (from _sns_content) + verified numbers ->
per-title canonical SEO HTML (sec 6/6-R), hub, index, robots, sitemap, llms.txt, llms-full.txt.
No wall-clock (BUILD_DATE fixed); concept DOI 10.5281/zenodo.20755154 is emitted in the claim-strip,
JSON-LD (identifier/sameAs), footer, landing, llms.txt, and _meta.json.
"""
import os, json, re, html

# ---- site identity (engine owns this; content owns prose + numbers) ----
PAPER = {"paper_id": "sensory-organs", "code": "sns",
         "title": "Special-Sense Organ Dynamics: Ocular Optics, Cochlear Frequency Analysis, and Vestibular Balance",
         "short": "Special-Sense Organs"}
AUTHOR     = "Young Jae Lee"
ORCID      = "https://orcid.org/0009-0002-7535-8245"
SITE       = "https://jamming-physics.org"
HUB_URL    = "/sensory-organs/"
REPRO_BASE = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/sensory-organs"
DNA_HUB    = "/dna/"
PHYS_HUB   = "/physics/"
NEURO_HUB  = "/neuro/"
BUILD_DATE = "2026-06-18"
LICENSE    = "https://creativecommons.org/licenses/by/4.0/"
DOI        = "10.5281/zenodo.20755154"          # concept DOI (always resolves to the latest version)
DOI_URL    = "https://doi.org/10.5281/zenodo.20755154"

GRADE_CLASS = {"forced": "g-forced", "verified": "g-verified", "calibrated": "g-calibrated",
               "open": "g-open", "hypothesis": "g-hypothesis"}

# ---------------------------------------------------------------- low-level helpers
def esc(s):  return html.escape(str(s), quote=True)
def jdump(o): return json.dumps(o, ensure_ascii=False, separators=(",", ":"))
def strip_tags(s): return re.sub(r"<[^>]+>", "", s)
def count_words(t): return len(re.findall(r"\S+", strip_tags(t)))

# --- deterministic title/description derivation (VP-SPEC 6-D) ---
_SUBJ_DELIMS = [": ", " \u2014 ", " - ", "; ", " from "]
def subj45(title):
    """Topic part of the title, <=45 chars: drop trailing (...), cut a trailing subtitle, word-truncate."""
    s = re.sub(r"\s*\([^()]*\)\s*$", "", title.strip())
    for d in _SUBJ_DELIMS:
        i = s.find(d)
        if i != -1:
            s = s[:i].strip(); break
    if len(s) > 45:
        cut = s[:45]
        if " " in cut:
            cut = cut[:cut.rfind(" ")]
        s = cut.strip()
    return s

def clamp_desc(s):
    """Meta description: attribute-safe, truncated at a word boundary to <=160 chars (conclusion-first)."""
    s = s.replace('"', "'").strip()
    if len(s) > 160:
        cut = s[:160]
        if " " in cut:
            cut = cut[:cut.rfind(" ")]
        s = cut.rstrip(" ,;:")
    return s

def render_blocks(blocks):
    out, body_text = [], []
    for b in blocks:
        k = b[0]
        if k == "p":
            out.append("<p>%s</p>" % b[1]); body_text.append(b[1])
        elif k == "h2":
            out.append("<h2>%s</h2>" % esc(b[1])); body_text.append(b[1])
        elif k == "h3":
            out.append("<h3>%s</h3>" % esc(b[1])); body_text.append(b[1])
        elif k == "ul":
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in b[1])); body_text.append(" ".join(b[1]))
        elif k == "t":
            _, cap, heads, rows = b
            th = "".join("<th>%s</th>" % esc(h) for h in heads)
            trs = []
            for r in rows:
                trs.append("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r))
                body_text.append(" ".join(strip_tags(str(c)) for c in r))
            caphtml = ("<caption>%s</caption>" % esc(cap)) if cap else ""
            out.append('<div class="tbl-wrap"><table>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                       % (caphtml, th, "".join(trs)))
            body_text.append(" ".join(strip_tags(str(h)) for h in heads))
        elif k == "card":
            out.append('<aside class="vp-card">%s</aside>' % b[1])      # excluded from body word count
        elif k == "bound":
            out.append('<div class="bound">%s</div>' % b[1]); body_text.append(b[1])
    return "\n".join(out), " ".join(body_text)

def claim_strip(label, kind):
    g = '<span class="grade %s">%s</span>' % (GRADE_CLASS[kind], esc(label))
    return ('<aside class="claim-strip">%s'
            '<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>'
            '<a href="%s" rel="noopener">Reproduce (GitHub)</a>'
            '<a class="doi" href="%s" rel="noopener">DOI: %s</a></aside>') % (g, REPRO_BASE, DOI_URL, DOI)

def jsonld_article(ch):
    kw = ch.get("seo", ch["knows"])
    d = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "headline": ch["title"],
         "name": ch["title"], "inLanguage": "en",
         "isPartOf": {"@type": "CreativeWorkSeries", "name": PAPER["title"], "alternateName": PAPER["short"],
                      "identifier": DOI_URL},
         "identifier": DOI_URL, "sameAs": DOI_URL,
         "position": ch["no"], "abstract": strip_tags(ch["abstract"]),
         "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
         "publisher": {"@type": "Organization", "name": "Jamming Physics"},
         "datePublished": BUILD_DATE, "dateModified": BUILD_DATE, "isBasedOn": REPRO_BASE,
         "license": LICENSE, "keywords": ", ".join(kw), "knowsAbout": ch["knows"]}
    return '<script type="application/ld+json">%s</script>' % jdump(d)

def jsonld_breadcrumb(ch):
    d = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": PAPER["short"], "item": SITE + HUB_URL},
        {"@type": "ListItem", "position": 3, "name": "\u00a7%d %s" % (ch["no"], ch["short"])}]}
    return '<script type="application/ld+json">%s</script>' % jdump(d)

def footer_html():
    return ('<footer><p><b>%s</b> \u00b7 %s. Part of the Jamming Physics whitepaper family. '
            'Single-author, no-tuning, bit-for-bit reproducible (SEED-fixed, 2\u00d7sha256 identical).</p>'
            '<p>Author: %s (<a href="%s">ORCID 0009-0002-7535-8245</a>) \u00b7 License: '
            '<a href="%s">CC BY 4.0</a> \u00b7 DOI: <a href="%s">%s</a> \u00b7 '
            '<a href="%s">Reproduction code (GitHub)</a></p></footer>') \
           % (esc(PAPER["short"]), esc(PAPER["title"]), esc(AUTHOR), ORCID, LICENSE, DOI_URL, DOI, REPRO_BASE)

PAGE = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>{title_tag}</title>\n<meta name="description" content="{desc}">\n'
        '<link rel="canonical" href="{canon}">\n<link rel="stylesheet" href="/assets/css/site.css">\n'
        '{jsonld}\n</head>\n<body>\n<header><nav class="crumb">{crumb}</nav></header>\n<main>\n{main}\n</main>\n{footer}\n</body>\n</html>\n')

# ---------------------------------------------------------------- page renderers
def render_chapter(ch, prev_ch, next_ch):
    slug = ch["slug"]
    title_tag = "%s \u2014 %s \u00a7%d | Jamming Physics" % (subj45(ch["subj"]), PAPER["short"], ch["no"])
    canon = "%s%s%s/" % (SITE, HUB_URL, slug)
    crumb = '<a href="/">Home</a> \u203a <a href="%s">%s</a> \u203a \u00a7%d' % (HUB_URL, esc(PAPER["short"]), ch["no"])
    body_html, body_text = render_blocks(ch["body"])
    cards = "".join('<aside class="vp-card">%s</aside>' % c for c in ch.get("cards", []))
    prev_a = ('<a rel="prev" href="%s%s/">\u2190 \u00a7%d</a>' % (HUB_URL, prev_ch["slug"], prev_ch["no"])) if prev_ch else "<span></span>"
    next_a = ('<a rel="next" href="%s%s/">\u00a7%d \u2192</a>' % (HUB_URL, next_ch["slug"], next_ch["no"])) if next_ch else "<span></span>"
    pn = '<nav class="pn">%s<a href="%s">Contents</a>%s</nav>' % (prev_a, HUB_URL, next_a)
    main = ('<h1>%s</h1>\n<p class="answer">%s</p>\n<p class="abstract">%s</p>\n%s\n%s\n%s\n%s'
            % (esc(ch["title"]), ch["answer"], ch["abstract"],
               claim_strip(ch["grade_label"], ch["grade_kind"]), cards, body_html, pn))
    jsonld = jsonld_article(ch) + "\n" + jsonld_breadcrumb(ch)
    page = PAGE.format(title_tag=esc(title_tag), desc=html.escape(clamp_desc(ch["desc"]), quote=False), canon=canon,
                       jsonld=jsonld, crumb=crumb, main=main, footer=footer_html())
    return page, count_words(body_text), count_words(ch["answer"])

def render_hub(chs, F, sha):
    canon = SITE + HUB_URL
    jl_series = {"@context": "https://schema.org", "@type": "CreativeWorkSeries", "name": PAPER["title"],
                 "alternateName": PAPER["short"], "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
                 "license": LICENSE, "url": canon,
                 "hasPart": [{"@type": "ScholarlyArticle", "position": c["no"], "headline": c["title"],
                              "url": "%s%s%s/" % (SITE, HUB_URL, c["slug"])} for c in chs]}
    jl_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": PAPER["short"]}]}
    jsonld = ('<script type="application/ld+json">%s</script>\n<script type="application/ld+json">%s</script>'
              % (jdump(jl_series), jdump(jl_bc)))
    toc = "".join('<li><a href="%s%s/">%s</a><span class="one">%s</span>'
                  '<span class="gcell"><span class="grade %s">%s</span></span></li>'
                  % (HUB_URL, c["slug"], esc(c["title"]), esc(c["one"]), GRADE_CLASS[c["grade_kind"]], esc(c["grade_label"]))
                  for c in chs)
    legend = ('<div class="legend">'
              '<span class="k"><span class="grade g-verified">verified</span> reproduced in-sim [V]</span>'
              '<span class="k"><span class="grade g-calibrated">calibrated</span> cited input [L]</span>'
              '<span class="k"><span class="grade g-open">open</span> stated obstacle [O]</span>'
              '<span class="k"><span class="grade g-hypothesis">hypothesis</span> [H]</span></div>')
    intro = ('<p class="lede">This whitepaper derives the human special-sense organs &mdash; the eye, the cochlea, '
             'the vestibular labyrinth, and the chemosensors of taste and smell &mdash; from physics, on a single '
             'jamming substrate. The organ nodes are not assumed: each one <b>emerges as a node from measured human '
             'DNA stacking stiffness &gamma;</b> (SantaLucia nearest-neighbour &Delta;G37 over the real proximal '
             'promoter, never fitted), and their developmental order is a parameter-free read-out of those measured '
             'numbers. Every quantity on every page is a measured input or a derived value, reproduced bit-for-bit '
             '(2&times;sha256 identical). This is a grounded, falsifiable derivation, not an illustrative toy.</p>'
             '<p class="lede" style="font-size:1.02rem">The central physical result is a <b>unification</b>: the '
             'cellular transducer at <i>every</i> special sense is the same object &mdash; a cooperative, bistable '
             'ion channel, the R19 double-well switch. On top of that switch sit the organ-level optics and '
             'acoustics (classical physics, documented and linked), the cochlear amplifier&rsquo;s parameter-free '
             'cube-root nonlinearity, a single quadratic law for the major eye and ear diseases, and a root-cause '
             'therapy program that is the inverse of that disease operation.</p>')
    derive = ('<p class="derive-line">Node identity and developmental order are inherited from the measured DNA '
              'stiffness atlas \u2192 <a href="%s">4D DNA Blueprint</a>. The transduced signal is handed off to '
              '\u2192 <a href="%s">the Neural Emergence Chain</a>. The R19 / FHN substrate is vendored from the '
              '<a href="%s">jamming foundation</a>.</p>') % (DNA_HUB, NEURO_HUB, PHYS_HUB)
    headline = ('<h2>Headline results</h2><ul>'
                '<li><b>The organs emerge from measured DNA.</b> Six special-sense nodes are read out from the '
                'measured stacking stiffness &gamma; of their master genes (PAX6 %s, RAX %s, EYA1 %s, SOX2 %s, '
                'TAS1R3 %s); sorting &gamma; gives a developmental order whose falsifiable prediction &mdash; taste '
                'specified latest &mdash; is confirmed. None of these numbers is tuned.</li>'
                '<li><b>One transducer primitive across five senses.</b> The photoreceptor (CNG), hair-cell (MET), '
                'taste (TRPM5), and olfactory (CNG) channels are all the same R19 bistable switch &mdash; verified '
                'bistable with a discontinuous flip and cooperative slopes &asymp;3.1&ndash;3.3.</li>'
                '<li><b>The cochlear amplifier is parameter-free.</b> Poised at a Hopf bifurcation, its response is '
                'R = (F/&beta;)<sup>%s</sup> &mdash; a cube-root compression with exponent %s that contains no fitted '
                'parameter; small-signal gain climbs to &asymp;%s at criticality.</li>'
                '<li><b>Classical organ instruments reproduce their anchors.</b> Reduced-eye axial length %s mm, '
                '%s D/mm, Greenwood place-map %s Hz&ndash;%s kHz, and canal velocity-band flatness %s all reproduce '
                'their cited values by arithmetic.</li>'
                '<li><b>One disease law, one therapy principle.</b> Disease is a quadratic basin collapse, barrier '
                '(g&sup2;/4)(1&minus;d)&sup2;; root-cause therapy is the inverse substrate operation, and a collapsed '
                'basin recovers %s%% of its depth in the restoration demo.</li></ul>') \
               % (F["g_pax6"], F["g_rax"], F["g_eya1"], F["g_sox2"], F["g_tas"], F["comp"], F["comp_num"],
                  F["gain0"], F["axial"], F["dpm"], F["gw_apex"], F["gw_base_k"], F["flat"], F["rd_rec"])
    repro = ('<h2>Reproduction</h2><p>One harness reproduces every section. From the package root run '
             '<code>python repro/run_all.py</code>: it emerges the six organ nodes from measured \u03b3, confirms '
             'every transducer is a bistable switch, derives the cochlear cube-root exponent, reproduces the '
             'classical organ instruments, and runs the pathology and treatment models. The result hash is '
             'deterministic (<code>%s\u2026</code>, 2\u00d7sha256 identical across processes). The canonical artifact '
             'is this HTML; numbers shown on each page are loaded from that verified result.</p>') % esc(sha[:12])
    scope = ('<p class="bound" style="margin-top:1.6rem"><b>Scope and grading discipline.</b> Every claim on this '
             'site carries an explicit grade and a reproduction path, and the boundaries are drawn deliberately. '
             'Organ-level optics and acoustics are <b>classical physics</b>, cited and reproduced by arithmetic '
             '[V-arith] rather than over-claimed as substrate results. The transducer effector-channel &gamma; is '
             'owned by the DNA pipeline as the single source of truth, so it is cited [L], not re-computed here. '
             'Clinical efficacy is reported at its true evidence level: AMD complement inhibitors are approved on '
             'an anatomic endpoint with no functional acuity gain yet, cataract chaperone reversal failed '
             'replication, and ATOH1-regenerated hair cells remain immature &mdash; each flagged so the reader is '
             'never misled. Rare and monogenic disease is owned by the disease whitepaper. Every open [O] item is '
             'listed with its specific obstacle in <code>IRREPRODUCIBILITY_LEDGER.md</code>. The grading vocabulary '
             '([V] verified &middot; [L] calibrated/cited &middot; [O] open &middot; [H] hypothesis) is what makes '
             'the program falsifiable.</p>')
    main = ('<h1>%s</h1>\n%s\n%s\n%s\n<h2>Chapters</h2>\n<ol class="toc">%s</ol>\n%s\n%s\n%s'
            % (esc(PAPER["title"]), intro, derive, legend, toc, headline, repro, scope))
    crumb = '<a href="/">Home</a> \u203a %s' % esc(PAPER["short"])
    desc = ("Special-sense organs as physical instruments: one R19 bistable-channel transducer across vision, "
            "hearing, balance, and taste; the cochlear Hopf cube-root; disease as basin collapse and therapy as its inverse.")
    return PAGE.format(title_tag=esc("%s | Jamming Physics" % PAPER["short"]), desc=esc(desc), canon=canon,
                       jsonld=jsonld, crumb=crumb, main=main, footer=footer_html())

def render_index(F):
    canon = SITE + "/"
    jl = {"@context": "https://schema.org", "@type": "WebSite", "name": "Jamming Physics \u2014 " + PAPER["short"],
          "url": canon, "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID}, "license": LICENSE,
          "mainEntity": {"@type": "CreativeWorkSeries", "name": PAPER["title"], "url": SITE + HUB_URL}}
    jsonld = '<script type="application/ld+json">%s</script>' % jdump(jl)
    card = ('<div class="card-grid"><div class="paper-card"><h3>%s</h3>'
            '<div class="res">organs emerge from measured DNA &gamma; &middot; one R19 transducer across five '
            'senses &middot; R = (F/&beta;)<sup>%s</sup></div>'
            '<p>The eye, cochlea, vestibular labyrinth, and the chemosensors of taste and smell, derived as '
            'physical instruments on the jamming substrate. The organ nodes emerge from measured human-DNA stacking '
            'stiffness; the cellular transducer at every sense is one bistable ion channel; organ optics and '
            'acoustics are classical; and a single disease law comes with a root-cause therapy program. '
            'Bit-for-bit reproducible, every quantity graded.</p>'
            '<a href="%s">Read the whitepaper &rarr;</a></div></div>') % (esc(PAPER["title"]), F["comp"], HUB_URL)
    main = ('<h1>Special-Sense Organs</h1>'
            '<p class="lede">A physics-derived whitepaper on the human special senses. The organ nodes are not '
            'assumed &mdash; they <b>emerge from measured DNA stacking stiffness &gamma;</b>, never fitted. The '
            'transducer at every special sense is the same bistable ion channel; the organ-level optics and '
            'acoustics are classical physics; and disease is the substrate failing in a way that root-cause therapy '
            'inverts. A single author, no tuning, reproduced bit-for-bit.</p>%s'
            '<p class="bound">This volume is part of the Jamming Physics family (jamming-physics.org). It follows '
            'VP-SPEC v1.8: every quantity is a measured input or a derived value (never tuned), reproduced '
            'bit-for-bit (2&times;sha256 identical), and graded honestly ([V] verified &middot; [L] calibrated '
            '&middot; [O] open with a stated obstacle). Published under concept DOI '
            '<a href="%s">%s</a>.</p>') % (card, DOI_URL, DOI)
    desc = ("Special-Sense Organs \u2014 a physics-derived whitepaper: one R19 bistable transducer across vision, "
            "hearing, balance, and taste; classical organ optics; disease as basin collapse.")
    return PAGE.format(title_tag=esc("Special-Sense Organs | Jamming Physics"), desc=esc(desc), canon=canon,
                       jsonld=jsonld, crumb="Home", main=main, footer=footer_html())

def render_robots():
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    out = ["# Special-Sense Organs (Jamming Physics) -- AI + search bots ALLOWED.",
           "# Staging alternative before domain cutover: 'User-agent: *' / 'Disallow: /'."]
    for b in bots:
        out += ["User-agent: %s" % b, "Allow: /", ""]
    out += ["User-agent: *", "Allow: /", "", "Sitemap: %s/sitemap.xml" % SITE, ""]
    return "\n".join(out)

def render_sitemap(urls):
    items = "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, BUILD_DATE) for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % items)

def render_llms(chs, sha):
    head = ("# Special-Sense Organs \u2014 Jamming Physics\n\n> A physics-derived whitepaper on the human special "
            "senses (eye, cochlea, vestibular labyrinth, taste, smell). The organ nodes are not assumed: each "
            "emerges as a node from measured human-DNA stacking stiffness \u03b3 (SantaLucia nearest-neighbour "
            "\u0394G37, never fitted), and their developmental order is a parameter-free read-out of those numbers. "
            "The cellular transducer at every special sense is one shared object \u2014 a bistable ion channel (the "
            "R19 double-well switch); organ-level optics and acoustics are classical physics (cited, reproduced by "
            "arithmetic); the cochlear amplifier gives a parameter-free cube-root law; disease is one quadratic "
            "basin collapse and root-cause therapy is its inverse. Single-author, no-tuning, bit-for-bit "
            "reproducible (2\u00d7sha256 %s\u2026). Concept DOI: 10.5281/zenodo.20755154. License: CC BY 4.0.\n\n" % sha[:12])
    core = "## Core\n- [Whitepaper hub](%s) \u2014 scope, headline results, reproduction\n\n" % HUB_URL
    research = "## Chapters\n" + "".join("- [\u00a7%d %s](%s%s/) \u2014 %s [%s]\n"
              % (c["no"], c["title"], HUB_URL, c["slug"], c["one"], c["grade_label"]) for c in chs) + "\n"
    policies = ("## Policies\n- Grades: [V] verified in-sim \u00b7 [L] calibrated/cited \u00b7 [O] open w/ stated "
                "obstacle \u00b7 [H] hypothesis.\n- Effector-channel \u03b3 owned by the DNA pipeline (SSOT). "
                "Rare/monogenic disease owned by the disease whitepaper.\n- Reproduce: python repro/run_all.py\n")
    return head + core + research + policies

def render_llms_full(chs):
    parts = ["# Special-Sense Organs \u2014 canonical text (plain)\n"]
    for c in chs:
        parts.append("\n\n## \u00a7%d %s\n\n%s\n\n%s\n" % (c["no"], c["title"], strip_tags(c["answer"]), strip_tags(c["abstract"])))
        for b in c["body"]:
            if b[0] == "p":
                parts.append(strip_tags(b[1]) + "\n")
            elif b[0] == "ul":
                parts.append("\n".join("- " + strip_tags(x) for x in b[1]) + "\n")
            elif b[0] == "bound":
                parts.append(strip_tags(b[1]) + "\n")
    return "\n".join(parts)

# ---------------------------------------------------------------- meta card + manifest
def render_meta(chs, totals):
    return {"paper_id": PAPER["paper_id"], "code": PAPER["code"], "title": PAPER["title"],
            "short": PAPER["short"], "doi": DOI, "hub_url": HUB_URL, "branch": "physical",
            "package": "sensory_organ_vp_site",
            "abstract": ("The special-sense organs as physical instruments: one R19 bistable-channel transducer "
                         "across vision, hearing, balance and taste; classical organ optics and acoustics; the "
                         "cochlear Hopf cube-root; disease as basin collapse and therapy as its inverse."),
            "headline_results": ["R = (F/\u03b2)^(1/3)", "one R19 transducer across five senses"],
            "chapters": [{"no": c["no"], "slug": c["slug"], "title": c["title"], "one_liner": c["one"],
                          "grade": c["grade_kind"], "words": c["_words"]} for c in chs],
            "totals": totals}

# ---------------------------------------------------------------- orchestrator
def build_site(chs, F, sha, docs_dir, manifest_path):
    paper_dir = os.path.join(docs_dir, PAPER["paper_id"])
    os.makedirs(paper_dir, exist_ok=True)
    urls = [SITE + "/", SITE + HUB_URL]
    total_words = 0
    # chapters
    for i, ch in enumerate(chs):
        prev_ch = chs[i - 1] if i > 0 else None
        next_ch = chs[i + 1] if i < len(chs) - 1 else None
        page, bw, aw = render_chapter(ch, prev_ch, next_ch)
        if not (40 <= aw <= 60):
            print("  WARN answer words out of [40,60]: \u00a7%d = %d" % (ch["no"], aw))
        ch["_words"] = bw; total_words += bw
        d = os.path.join(paper_dir, ch["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
        urls.append("%s%s%s/" % (SITE, HUB_URL, ch["slug"]))
    # hub + index + access layer
    open(os.path.join(paper_dir, "index.html"), "w", encoding="utf-8").write(render_hub(chs, F, sha))
    open(os.path.join(docs_dir, "index.html"), "w", encoding="utf-8").write(render_index(F))
    open(os.path.join(docs_dir, "robots.txt"), "w", encoding="utf-8").write(render_robots())
    open(os.path.join(docs_dir, "sitemap.xml"), "w", encoding="utf-8").write(render_sitemap(urls))
    open(os.path.join(docs_dir, "llms.txt"), "w", encoding="utf-8").write(render_llms(chs, sha))
    open(os.path.join(docs_dir, "llms-full.txt"), "w", encoding="utf-8").write(render_llms_full(chs))
    # meta card
    totals = {"words": total_words, "chapters": len(chs)}
    meta = render_meta(chs, totals)
    json.dump(meta, open(os.path.join(paper_dir, "_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    # manifest (derived index of canonical HTML)
    lines = ["slug,title,section_no,status,grade,words,eq_display"]
    for ch in chs:
        t = ch["title"].replace('"', "'")
        lines.append('%s,"%s",%d,built,%s,%d,0' % (ch["slug"], t, ch["no"], ch["grade_kind"], ch["_words"]))
    open(manifest_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return {"chapters": len(chs), "total_words": total_words, "urls": len(urls),
            "files": ["docs/index.html", "docs/%s/index.html" % PAPER["paper_id"],
                      "docs/%s/_meta.json" % PAPER["paper_id"], "docs/robots.txt", "docs/sitemap.xml",
                      "docs/llms.txt", "docs/llms-full.txt"]}
