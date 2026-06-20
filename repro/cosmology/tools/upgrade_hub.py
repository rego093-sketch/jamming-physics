#!/usr/bin/env python3
"""
upgrade_hub.py — VP_SPEC v1.8 6-R.4 hub treatment for docs/cosmology/index.html

Idempotent. Performs four edits, each delimited so re-runs replace cleanly:

  1. Highwire citation tags (5) into the `<!-- citation_tags: Phase 7 -->` slot.
  2. JSON-LD: replace the legacy CollectionPage block with
       CreativeWorkSeries (name+identifier reused by every chapter isPartOf,
       author+ORCID, dates, isBasedOn, license, knowsAbout, hasPart[28])
     + a standalone BreadcrumbList.
  3. answer-first <p class="answer"> (40-60 words) immediately after <h1>.
  4. refresh the overview line's counts from the reconciled _meta totals
     so displayed == regenerated (C1).
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
HUB = ROOT / "docs" / "cosmology" / "index.html"
META = json.load(open(ROOT / "docs" / "cosmology" / "_meta.json", encoding="utf-8"))

SITE = "https://jamming-physics.org"
HUB_URL = f"{SITE}/cosmology/"
DOI = META["doi"]
DOI_URL = f"https://doi.org/{DOI}"
AUTHOR = "Young Jae Lee"
ORCID = "https://orcid.org/0009-0002-7535-8245"
REPRO = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/cosmology"
LICENSE = "https://creativecommons.org/licenses/by/4.0/"
DATE_PUB, DATE_MOD = "2026-06-13", "2026-06-15"

ANSWER = ("This volume reinterprets gravity and cosmology as consequences of "
          "vacuum inflow: every particle annihilates vacuum quanta at a fixed "
          "rate, driving a permanent inflow whose momentum is gravity. From this "
          "one locked input it derives planetary orbits, the galactic scale "
          "a\u2080 = cH\u2080/2\u03c0 \u2248 1.08\u00d710\u207b\u00b9\u2070 m s\u207b\u00b2, "
          "dark-matter phenomenology, and a non-expanding lattice-optics cosmology.")


def wc(s):
    return len([w for w in re.split(r"\s+", s.strip()) if w])


def clean_title(t):
    t = t.replace("``", "\u201c").replace("''", "\u201d").replace("&#x27;", "'")
    t = t.replace("$", "")
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    return re.sub(r"\s+", " ", t).strip()


def between(s, a, b, repl):
    """Replace text between markers a..b (inclusive) with repl; if markers
    absent return None so caller can do the first-time insertion."""
    pat = re.compile(re.escape(a) + r".*?" + re.escape(b), re.S)
    if pat.search(s):
        return pat.sub(repl, s)
    return None


def build_citation():
    A, B = "<!--vp-cite-start-->", "<!--vp-cite-end-->"
    tags = [
        f'<meta name="citation_title" content="{META["title"]}">',
        f'<meta name="citation_author" content="{AUTHOR}">',
        f'<meta name="citation_publication_date" content="{DATE_PUB.replace("-", "/")}">',
        f'<meta name="citation_doi" content="{DOI}">',
        f'<meta name="citation_pdf_url" content="{DOI_URL}">',
    ]
    return A + "\n" + "\n".join(tags) + "\n" + B


def build_jsonld():
    A, B = "<!--vp-hub-jsonld-start-->", "<!--vp-hub-jsonld-end-->"
    haspart = []
    for i, c in enumerate(META["chapters"], start=1):
        haspart.append({
            "@type": "ScholarlyArticle",
            "position": i,
            "name": clean_title(c["title"]),
            "url": f"{HUB_URL}{c['slug']}/",
        })
    series = {
        "@context": "https://schema.org",
        "@type": "CreativeWorkSeries",
        "name": META["short"],
        "alternateName": META["title"],
        "url": HUB_URL,
        "identifier": DOI,
        "sameAs": DOI_URL,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "datePublished": DATE_PUB,
        "dateModified": DATE_MOD,
        "isBasedOn": f"{REPRO}/",
        "license": LICENSE,
        "knowsAbout": ["vacuum inflow", "jamming lattice", "galactic rotation",
                       "acceleration scale a0", "lattice-optics cosmology",
                       "dark matter as vacuum deficit"],
        "hasPart": haspart,
    }
    crumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": META["short"], "item": HUB_URL},
        ],
    }
    s = ('<script type="application/ld+json">'
         + json.dumps(series, ensure_ascii=False) + "</script>\n"
         + '<script type="application/ld+json">'
         + json.dumps(crumb, ensure_ascii=False) + "</script>")
    return A + "\n" + s + "\n" + B


def main():
    assert 40 <= wc(ANSWER) <= 60, f"hub answer {wc(ANSWER)} words out of [40,60]"
    t = HUB.read_text(encoding="utf-8")

    # 1. citation tags
    cite = build_citation()
    done = between(t, "<!--vp-cite-start-->", "<!--vp-cite-end-->", cite)
    if done is None:
        t = t.replace("<!-- citation_tags: Phase 7 -->",
                      "<!-- citation_tags: Phase 7 -->\n" + cite, 1)
    else:
        t = done

    # 2. JSON-LD
    jl = build_jsonld()
    done = between(t, "<!--vp-hub-jsonld-start-->", "<!--vp-hub-jsonld-end-->", jl)
    if done is None:
        t = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "CollectionPage".*?</script>',
                   jl, t, count=1, flags=re.S)
    else:
        t = done

    # 3. answer-first after <h1>...</h1>
    t = re.sub(r'(<h1>.*?</h1>)\s*<p class="answer">.*?</p>', r"\1", t, flags=re.S)
    t = re.sub(r"(<h1>.*?</h1>)",
               r'\1\n<p class="answer">' + ANSWER + "</p>", t, count=1, flags=re.S)

    # 4. refresh overview counts from reconciled _meta totals
    tot = META["totals"]
    n_ch = len(META["chapters"])
    t = re.sub(r"\d+ chapters · \d+ equations · \d+ tables · \d+ source words",
               f"{n_ch} chapters · {tot['eq']} equations · {tot['tables']} tables "
               f"· {tot['words']} source words", t, count=1)

    HUB.write_text(t, encoding="utf-8")

    # report
    checks = {
        "citation_title": 'name="citation_title"' in t,
        "citation_doi": 'name="citation_doi"' in t,
        "CreativeWorkSeries": '"CreativeWorkSeries"' in t,
        "standalone BreadcrumbList": t.count('"BreadcrumbList"') >= 1,
        "no CollectionPage": "CollectionPage" not in t,
        "answer-first": '<p class="answer">' in t,
        "answer words in [40,60]": 40 <= wc(ANSWER) <= 60,
        f"overview eq={tot['eq']}": f"{tot['eq']} equations" in t,
        f"overview words={tot['words']}": f"{tot['words']} source words" in t,
    }
    for k, v in checks.items():
        print(f"  [{'OK' if v else 'XX'}] {k}")
    assert all(checks.values()), "hub upgrade incomplete"
    print(f"hub answer words: {wc(ANSWER)}")


if __name__ == "__main__":
    main()
