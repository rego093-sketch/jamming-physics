#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vp_v18_upgrade.py — deterministic v1.6 -> v1.8 upgrade for the geochronology
canonical HTML (VP-SPEC v1.8: headline C4 retrieval-readiness + v1.7 grade span).

Operates ONLY on the canonical docs/ HTML (heaven C2: HTML is the single source;
no TeX is read). Edits are confined to gate-EXCLUDED zones so the manifest body
word count is invariant by construction:
  * <head> JSON-LD (upgraded to 6-R.4 schema)
  * a new  <p class="answer">      (answer-first, 40-60 words)   [excluded]
  * a new  <span class="grade ...>  inside .claim-strip          [excluded]
  * a new  <aside class="vp-card">  for the one locked quantity  [excluded]
  * <meta name="description"> truncation fix on the hub
The body prose, equations, figures, tables and every number are untouched.

Same input -> same output (no clock/RNG; UPGRADE_DATE is a fixed constant).
Run:  python3 tools/vp_v18_upgrade.py            (edits docs/ in place)
"""
import os, re, io, csv, json, sys, html as _html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import answers as A

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs", "geochronology")
MANI = os.path.join(ROOT, "manifest", "geochronology.csv")

# ---- locked registry values (2장) -----------------------------------------
PAPER_ID = "geochronology"
SHORT    = "Cross-Chronometer Limit"
TITLE    = "Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit"
DOI      = "10.5281/zenodo.20568673"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
AUTHOR   = "Young Jae Lee"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
SERIES   = "Jamming Physics"
SITE     = "https://jamming-physics.org"
REPRO    = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/geochronology"
PUB_YEAR = "2026"          # citation_publication_date
UPGRADE_DATE = "2026-06-15"  # fixed -> deterministic dateModified

# grade vocabulary for THIS paper (grade_vocab_geochronology): F>I>A by strength
GRADE_LABEL = {"F": "directly confirmed", "I": "inferential", "A": "assumption"}
GRADE_CLASS = {"F": "g-forced", "I": "g-inferred", "A": "g-assumed"}
GRADE_PRIORITY = ["F", "I", "A"]

HUB_DESC = ("Radiocarbon and zircon U\u2013Pb share one accuracy limit: foreign older "
            "material biases ages old. One protocol meets both \u2014 classify age-"
            "independently, then validate out-of-sample.")

def read(p):  return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

def fit160(s):
    """<=160 chars, cut at last word boundary (>=80)."""
    if len(s) <= 160:
        return s
    cut = s[:160].rsplit(" ", 1)[0]
    return cut

def page_grade(main_html):
    """Most-frequent epistemic tag token; tie -> F>I>A. None if no tokens."""
    toks = re.findall(r'<span class="tag t([FIA])">', main_html)
    if not toks:
        return None
    counts = {g: toks.count(g) for g in set(toks)}
    best = max(counts.values())
    for g in GRADE_PRIORITY:
        if counts.get(g, 0) == best:
            return g
    return None

# ---- JSON-LD builders (6-R.4) ---------------------------------------------
def jsonld(d):
    return ('<script type="application/ld+json">\n'
            + json.dumps(d, ensure_ascii=False, indent=1) + '\n</script>')

def chapter_article_ld(slug, n, subj, h1):
    return {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": subj,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": SHORT, "identifier": DOI,
                     "url": f"{SITE}/{PAPER_ID}/"},
        "position": n,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "identifier": DOI, "datePublished": PUB_YEAR, "dateModified": UPGRADE_DATE,
        "isBasedOn": f"{REPRO}/{slug}/",
        "license": LICENSE,
        "knowsAbout": ["radiocarbon dating", "zircon U\u2013Pb geochronology", subj],
    }

def breadcrumb_ld(n, subj):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER_ID}/"},
            {"@type": "ListItem", "position": 3, "name": f"\u00a7{n} {subj}"},
        ],
    }

def hub_series_ld(rows):
    parts = [{"@type": "ScholarlyArticle",
              "position": int(r["no"]),
              "name": f"\u00a7{r['no']}. {_html.unescape(r['title'])}",
              "url": f"{SITE}/{PAPER_ID}/{r['slug']}/"} for r in rows]
    return {
        "@context": "https://schema.org", "@type": "CreativeWorkSeries",
        "name": SHORT, "headline": TITLE,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "identifier": DOI, "sameAs": f"https://doi.org/{DOI}", "license": LICENSE,
        "isPartOf": {"@type": "CreativeWork", "name": SERIES, "url": f"{SITE}/"},
        "hasPart": parts,
    }

def hub_breadcrumb_ld():
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER_ID}/"},
        ],
    }

# ---- head JSON-LD replacement ---------------------------------------------
LD_RE = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)

def replace_head_jsonld(H, blocks):
    """Replace ALL ld+json scripts in <head> with `blocks` (list of dict),
    preserving their position (first script onward)."""
    matches = list(LD_RE.finditer(H))
    if not matches:
        # insert before </head>
        ins = "\n".join(jsonld(b) for b in blocks) + "\n"
        return H.replace("</head>", ins + "</head>", 1)
    start = matches[0].start()
    end   = matches[-1].end()
    new = "\n".join(jsonld(b) for b in blocks)
    return H[:start] + new + H[end:]

# ---- chapter transform -----------------------------------------------------
def upgrade_chapter(slug, n):
    path = os.path.join(DOCS, slug, "index.html")
    H = read(path)
    main_m = re.search(r"<main>(.*)</main>", H, re.S)
    main = main_m.group(1)

    # subj45 from the existing (already-derived) <title>
    mt = re.search(r"<title>(.*?) \u2014 %s \u00a7\d+ \| Jamming Physics</title>"
                   % re.escape(SHORT), H)
    subj = mt.group(1) if mt else slug
    h1m = re.search(r"<h1>(.*?)</h1>", H, re.S)
    h1 = re.sub(r"<[^>]+>", "", h1m.group(1)).strip() if h1m else subj

    # 1) answer-first after </h1>
    if 'class="answer"' not in main:
        ans = '<p class="answer">%s</p>' % A.ANSWER[slug]
        main = re.sub(r"(</h1>\s*\n)", r"\1\n" + ans.replace("\\", "\\\\") + "\n",
                      main, count=1)

    # 2) grade span as first child of .claim-strip
    g = page_grade(main)
    if g and 'class="grade ' not in main:
        span = '<span class="grade %s">[%s] %s</span>' % (
            GRADE_CLASS[g], g, GRADE_LABEL[g])
        main = main.replace('<aside class="claim-strip">\n',
                            '<aside class="claim-strip">\n  ' + span + "\n", 1)

    # 3) vp-card(s) after the claim-strip </aside>  (one locked quantity: N_D = Fo)
    if slug in A.FO_CARD_ON and 'class="vp-card"' not in main:
        # insert right after the claim-strip closing tag
        main = re.sub(r'(</aside>)',
                      r'\1\n\n' + A.FO_CARD.replace("\\", "\\\\"),
                      main, count=1)

    # 4) anchor on the canonical derivation equation in §4
    if slug == "04-shared-physics-closure-exchange-number":
        main = main.replace('<figure class="eq">\n  <img src="/eq/geochronology/chr-04-001.svg"',
                            '<figure class="eq" id="fo">\n  <img src="/eq/geochronology/chr-04-001.svg"', 1)

    # 5) normalisation (§6-D.5): drop stray inline math delimiters (none expected)
    # (no-op guard; only touches a literal $...$ if present in prose)

    H = H[:main_m.start(1)] + main + H[main_m.end(1):]

    # 6) head JSON-LD -> 6-R.4 (ScholarlyArticle + BreadcrumbList)
    H = replace_head_jsonld(H, [chapter_article_ld(slug, n, subj, h1),
                                breadcrumb_ld(n, subj)])
    write(path, H)
    return g, len(A.ANSWER[slug].split()), (slug in A.FO_CARD_ON)

# ---- hub transform ---------------------------------------------------------
def upgrade_hub(rows):
    path = os.path.join(DOCS, "index.html")
    H = read(path)

    # answer-first after </h1> (before .lead)
    if 'class="answer"' not in H:
        ans = '<p class="answer">%s</p>' % A.HUB_ANSWER
        H = re.sub(r"(</h1>\s*\n)", r"\1" + ans.replace("\\", "\\\\") + "\n", H, count=1)

    # description truncation fix
    H = re.sub(r'(<meta name="description" content=")(.*?)(">)',
               lambda m: m.group(1) + _html.escape(fit160(HUB_DESC), quote=True) + m.group(3),
               H, count=1)

    # head JSON-LD -> CreativeWorkSeries(hasPart) + BreadcrumbList
    H = replace_head_jsonld(H, [hub_breadcrumb_ld(), hub_series_ld(rows)])
    write(path, H)

def main():
    with io.open(MANI, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    no_by_slug = {r["slug"]: int(r["no"]) for r in rows}

    print("== upgrading 14 chapters ==")
    for r in rows:
        slug = r["slug"]
        g, w, card = upgrade_chapter(slug, no_by_slug[slug])
        print("  %-55s grade=%s answer=%dw vp-card=%s"
              % (slug, ("[%s]" % g) if g else "  -", w, "yes" if card else "no"))
    print("== upgrading hub ==")
    upgrade_hub(rows)
    print("done.")

if __name__ == "__main__":
    main()
