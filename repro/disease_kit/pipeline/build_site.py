#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_site.py  --  the CANONICAL retrieval-ready HTML site for the kit's catalytic output.  [NATIVE, ROADMAP IV-A]

  *** NATIVE to the VP Disease Emergence Kit (not inherited).  ROADMAP IV-A: render the kit's two
      catalytic outputs -- the no-approved-tail OPEN-DIRECTIONS cards (III-A) and the CROSS-DISEASE
      REPURPOSING hypotheses (III-A2) -- as a single static, answer-first, machine-readable HTML page
      so a researcher, sponsor, or AI search crawler can pick up the honestly-scoped hypotheses.  The
      repurposing + open-directions cards are the HEADLINE (the catalytic novelty); the method-check
      (direction recovery) and the firewall are stated plainly underneath. ***

  CONSTRUCTION (deterministic, VP_SPEC v1.8 §6-R / Constitution C4):
    - INPUT is FROZEN ONLY: repro/modules/expected/repurposing_hypotheses.json + open_directions_cards.json,
      and metadata parsed from VERSION (version / date / DOI / ORCID).  No timestamp is read from the
      clock -- dateModified = the VERSION date -- so two builds are BYTE-IDENTICAL (self-test asserts it).
    - The patient-facing disclaimer (disclaimer_banner.html_banner()) is the FIRST <body> element on
      every human-facing page (kit invariant since v0.27.0).
    - answer-first (§6-R.3): the page and every <section> open with a self-contained direct answer; the
      page answer is a 40-60-word <p class="answer">.
    - structured data (§6-R.4): JSON-LD in <head> (WebSite + Person[ORCID,sameAs DOI] + Dataset, and the
      two catalytic findings as Claim+Rating[O]).
    - access tier (§6-R.5): site/sitemap.xml, site/robots.txt (STAGING Disallow:/ until on-domain, with
      the production bot-allow-list inlined as a comment for a one-line cutover), site/llms.txt (<5KB).

  FIREWALL: the page renders DIRECTION + CANDIDATE CLASS + FALSIFIER only; every catalytic claim shows
  its [O] magnitude grade and the "same-axis != same-disease" caveat.  No dose / efficacy / response
  rate / individual advice anywhere.

USAGE:
  python3 pipeline/build_site.py            # build site/ + self-test, print summary
  python3 pipeline/build_site.py --write    # also freeze repro/expected_site_sha256.json
  python3 pipeline/build_site.py --selftest  # determinism + structure teeth (exit 0/1) -- for run_modules
"""
import os
import re
import sys
import json
import html
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SITE = os.path.join(ROOT, "site")
EXPECT = os.path.join(ROOT, "repro", "modules", "expected")

# import the patient-facing disclaimer (kit invariant: first body element)
sys.path.insert(0, ROOT)
from pipeline.disclaimer_banner import html_banner  # noqa: E402

CANONICAL = "https://jamming-physics.org/disease-emergence-kit/"
FAIL = []


def check(name, cond):
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {name}")
    if not cond:
        FAIL.append(name)
    return cond


def _meta():
    """Parse deterministic metadata from VERSION (key: value header).  No clock read."""
    txt = open(os.path.join(ROOT, "VERSION")).read()
    def grab(key, default=""):
        m = re.search(rf"^{re.escape(key)}\s*:\s*(.+)$", txt, re.M)
        return m.group(1).strip() if m else default
    return {
        "version": grab("version", "0.0.0"),
        "date": grab("date", "1970-01-01"),
        "orcid": grab("orcid", ""),
        "doi": grab("doi (concept)", ""),
        "author": "Young Jae Lee",
    }


def E(s):
    """HTML-escape (quote-safe) for text nodes / attributes."""
    return html.escape(str(s), quote=True)


# ==================================================================================================
# page assembly
# ==================================================================================================
def _answer_paragraph(scan, cards, meta):
    """Page-level answer-first block: 40-60 words, self-contained, names entities + values + grade."""
    n_res = scan["n_resolved"]
    n_hyp = scan["n_hypotheses"]
    n_orph = scan["n_orphan_directions"]
    n_tail = scan["n_no_approved_lead"]
    # crafted to land in 40-60 words (gate-checked)
    return (
        f"The VP Disease Emergence Kit reads {n_res} single-gene diseases as switch perturbations and "
        f"forces each corrective DIRECTION. For the {n_tail} diseases with no approved therapy, it "
        f"surfaces {n_hyp} cross-disease repurposing hypotheses from same-axis approved donors and "
        f"reports {n_orph} honest orphan directions. Every claim is direction-only, graded [O]: no "
        f"dose, efficacy, or individual medical advice."
    )


def _repurposing_section(scan):
    rows = []
    for h in scan["repurposing_hypotheses"]:
        donors = "; ".join(
            f"{E(d['donor'])} ({E(', '.join(d['approved_agent_class']))})" for d in h["donors"]
        )
        rows.append(
            "<tr>"
            f"<td>{E(h['recipient'])}</td>"
            f"<td>{E(h['shared_axis_family'])}</td>"
            f"<td>{E(h['shared_corrective_direction'])} / {E(h['shared_lever_class'])}</td>"
            f"<td>{donors}</td>"
            f"<td>{E(h['novelty'])}</td>"
            "</tr>"
        )
    n = scan["n_hypotheses"]
    intro = (
        f"{n} cross-disease repurposing hypotheses are surfaced: for each no-approved disease below, an "
        f"agent CLASS already approved for a disease sharing the same (axis-family, direction, lever) is "
        f"proposed as a testable corrective-DIRECTION hypothesis \u2014 mechanism class only, never dose "
        f"or efficacy."
    )
    body = (
        '<table><thead><tr><th>Recipient (no approved agent)</th><th>Shared axis-family</th>'
        '<th>Direction / lever</th><th>Donor (approved agent class)</th><th>Novelty</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )
    caveat = (
        '<p class="caveat"><strong>Caveat (forced):</strong> same-axis \u2260 same-disease. Each row is a '
        'mechanism-CLASS direction hypothesis, not a prediction; donor and recipient differ in tissue, '
        'delivery, allele, and off-target biology, any of which may defeat repurposing. No magnitude is '
        'claimed [O].</p>'
    )
    return (
        '<section id="repurposing" aria-labelledby="repurposing-h">'
        '<h2 id="repurposing-h">Cross-disease repurposing hypotheses</h2>'
        f'<p class="answer-sec">{intro}</p>{body}{caveat}</section>'
    )


def _opendir_section(cards):
    rows = []
    for c in cards["cards"]:
        if c["kind"] == "repurposing_candidate":
            cls = "; ".join(
                f"{E(d['agent_class'])} \u2190 {E(d['approved_for_donor'])}"
                for d in c["candidate_drug_classes"]
            )
        else:
            cls = "\u2014 (orphan: no same-axis approved donor)"
        rows.append(
            "<tr>"
            f"<td>{E(c['slug'])}</td>"
            f"<td>{E(c['forced_corrective_direction'])} / {E(c['lead_lever_class'])} "
            f"<span class=\"status\">({E(c['lead_clinical_status'])})</span></td>"
            f"<td>{cls}</td>"
            f"<td>{E(c['cheapest_falsification_experiment'])}</td>"
            "</tr>"
        )
    n = cards["n_cards"]
    nr = cards["n_repurposing_candidate"]
    no = cards["n_orphan_direction"]
    intro = (
        f"{n} open-directions cards render the no-approved tail as actionable: {nr} carry a concrete "
        f"candidate drug class from a same-axis approved donor and {no} are honest orphan directions. "
        f"Each card gives the single CHEAPEST experiment that would refute the forced direction."
    )
    body = (
        '<table><thead><tr><th>Disease</th><th>Forced direction / lever (status)</th>'
        '<th>Candidate drug class (\u2190 approved-for donor)</th>'
        '<th>Cheapest falsification experiment</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table>'
    )
    return (
        '<section id="open-directions" aria-labelledby="open-directions-h">'
        '<h2 id="open-directions-h">Open-directions cards (no-approved tail)</h2>'
        f'<p class="answer-sec">{intro}</p>{body}</section>'
    )


def _method_section(scan):
    intro = (
        "The kit is a method check, not a discovery engine. It re-derives the DIRECTION of already-known "
        "interventions from DNA-emergence structure under a strict firewall: promoter structure is read "
        "[V], the corrective axis direction is forced and cited [F], and all magnitude \u2014 efficacy, "
        "dose, safety \u2014 is ungraded [O]. The repurposing rows whose recipient already pursues the "
        "donor class are confirmatory sanity checks."
    )
    fw = (
        '<ul class="firewall">'
        '<li><strong>[V]</strong> promoter / switch structure is computed from sequence.</li>'
        '<li><strong>[F]</strong> the corrective-axis direction (UP/DOWN) is forced and cited.</li>'
        '<li><strong>[O]</strong> no magnitude: no dose, potency, efficacy, response rate, or '
        'individual medical advice.</li>'
        '</ul>'
    )
    return (
        '<section id="method" aria-labelledby="method-h">'
        '<h2 id="method-h">What this is (and the firewall)</h2>'
        f'<p class="answer-sec">{intro}</p>{fw}</section>'
    )


COMPANION_DOI = "10.5281/zenodo.20763842"   # disease_wp — sibling whitepaper: reproducible burden ordering + standard-of-care context
COMPANION_URL = f"https://doi.org/{COMPANION_DOI}"


def _jsonld(scan, cards, meta):
    doi_url = f"https://doi.org/{meta['doi']}" if meta["doi"] else CANONICAL
    graph = [
        {"@type": "WebSite", "@id": CANONICAL, "name": "VP Disease Emergence Kit",
         "url": CANONICAL, "inLanguage": "en",
         "publisher": {"@type": "Person", "name": meta["author"],
                       "sameAs": [f"https://orcid.org/{meta['orcid']}", doi_url]}},
        {"@type": "Person", "name": meta["author"],
         "sameAs": [f"https://orcid.org/{meta['orcid']}", doi_url]},
        {"@type": "Dataset", "name": "VP Disease Emergence Kit \u2014 catalytic output",
         "description": ("Single-gene diseases read as DNA-emergence switch perturbations; corrective "
                         "DIRECTION forced [F], magnitude ungraded [O]. Catalytic output: cross-disease "
                         "repurposing hypotheses and open-directions cards for the no-approved tail."),
         "creator": {"@type": "Person", "name": meta["author"],
                     "sameAs": [f"https://orcid.org/{meta['orcid']}"]},
         "identifier": meta["doi"], "version": meta["version"],
         "datePublished": meta["date"], "dateModified": meta["date"],
         "license": "https://creativecommons.org/licenses/by/4.0/",
         "isBasedOn": CANONICAL + "repro/",
         "citation": COMPANION_URL,
         "keywords": ["DNA emergence", "drug repurposing", "rare disease", "corrective direction",
                      "jamming physics"]},
        {"@type": "Claim",
         "text": (f"{scan['n_hypotheses']} cross-disease repurposing hypotheses are surfaced for the "
                  f"no-approved tail (same axis-family / direction / lever as an approved donor)."),
         "review": {"@type": "Rating", "ratingValue": "O",
                    "alternateName": "direction-only; magnitude/efficacy NOT asserted",
                    "worstRating": "O", "bestRating": "V"}},
        {"@type": "Claim",
         "text": (f"{scan['n_orphan_directions']} no-approved diseases are honest orphan directions: the "
                  f"forced corrective direction stands but no same-axis approved donor exists."),
         "review": {"@type": "Rating", "ratingValue": "O",
                    "alternateName": "forced direction [F]; no candidate class asserted",
                    "worstRating": "O", "bestRating": "V"}},
    ]
    obj = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=True)


def render_index(scan, cards, meta):
    title = f"VP Disease Emergence Kit \u2014 catalytic output (v{meta['version']})"
    desc = (f"{scan['n_resolved']} single-gene diseases read as switch perturbations; "
            f"{scan['n_hypotheses']} cross-disease repurposing hypotheses + "
            f"{scan['n_orphan_directions']} orphan directions for the no-approved tail. "
            f"Direction-only, graded [O].")
    answer = _answer_paragraph(scan, cards, meta)
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>{E(title)}</title>",
        f'<meta name="description" content="{E(desc)}">',
        f'<link rel="canonical" href="{E(CANONICAL)}">',
        f'<meta name="author" content="{E(meta["author"])}">',
        '<meta name="robots" content="index,follow">',
        f'<script type="application/ld+json">\n{_jsonld(scan, cards, meta)}\n</script>',
        "<style>",
        ":root{--ink:#222;--mut:#555;--line:#ddd;--bg:#fff;--accent:#0b5;}",
        "*{box-sizing:border-box}",
        "body{margin:0;padding:1.5rem;max-width:980px;margin-inline:auto;color:var(--ink);"
        "background:var(--bg);font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}",
        "h1{font-size:1.5rem;line-height:1.25;margin:1.2rem 0 .4rem}",
        "h2{font-size:1.18rem;margin:2rem 0 .5rem;border-bottom:2px solid var(--line);padding-bottom:.2rem}",
        ".answer{font-size:1.05rem;background:#f6fbf8;border-left:4px solid var(--accent);"
        "padding:.8rem 1rem;margin:.6rem 0 1.4rem}",
        ".answer-sec{font-weight:600;margin:.2rem 0 .8rem}",
        ".caveat{background:#fffdf3;border-left:4px solid #e0a800;padding:.6rem .9rem;margin:.8rem 0;"
        "font-size:.93rem}",
        "table{border-collapse:collapse;width:100%;margin:.6rem 0 1rem;font-size:.9rem}",
        "th,td{border:1px solid var(--line);padding:.45rem .55rem;text-align:left;vertical-align:top}",
        "th{background:#f4f6f8}",
        ".status{color:var(--mut);font-size:.85em}",
        "ul.firewall,ul.firewall li{margin:.2rem 0}",
        "footer{margin-top:2.5rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--mut);"
        "font-size:.86rem}",
        "a{color:#06c}",
        "</style>",
        "</head>",
        "<body>",
        html_banner(),                       # <-- FIRST body element (kit invariant)
        "<main>",
        f"<h1>{E(title)}</h1>",
        f'<p class="answer">{E(answer)}</p>',
        _repurposing_section(scan),
        _opendir_section(cards),
        _method_section(scan),
        "</main>",
        "<footer>",
        f"{E(meta['author'])} \u00b7 ORCID "
        f'<a href="https://orcid.org/{E(meta["orcid"])}">{E(meta["orcid"])}</a> \u00b7 '
        f'concept DOI <a href="https://doi.org/{E(meta["doi"])}">{E(meta["doi"])}</a> &middot; sibling whitepaper (burden &amp; standard-of-care) <a href="{COMPANION_URL}">{COMPANION_DOI}</a> \u00b7 '
        f"v{E(meta['version'])} ({E(meta['date'])}) \u00b7 CC BY 4.0 \u00b7 "
        "programme jamming-physics.org. Direction-only; not medical advice.",
        "</footer>",
        "</body>",
        "</html>",
        "",
    ]
    return "\n".join(parts)


def render_sitemap(meta):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url>\n    <loc>{CANONICAL}</loc>\n"
        f"    <lastmod>{meta['date']}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>\n"
        "</urlset>\n"
    )


def render_robots():
    # STAGING (pre-domain-cutover): block all indexing so no pollution before the canonical move.
    # The production allow-list is inlined as a comment so cutover is a one-line swap (VP_SPEC §6-R.5).
    return (
        "# STAGING (pre-cutover): block indexing until this kit is live on its canonical domain.\n"
        "User-agent: *\n"
        "Disallow: /\n"
        "\n"
        "# --- PRODUCTION (swap in at domain cutover; allow AI + search bots, VP_SPEC v1.8 6-R.5) ---\n"
        "# User-agent: Googlebot\n# Allow: /\n"
        "# User-agent: Bingbot\n# Allow: /\n"
        "# User-agent: OAI-SearchBot\n# Allow: /\n"
        "# User-agent: GPTBot\n# Allow: /\n"
        "# User-agent: PerplexityBot\n# Allow: /\n"
        "# User-agent: ClaudeBot\n# Allow: /\n"
        "# User-agent: Google-Extended\n# Allow: /\n"
        f"# Sitemap: {CANONICAL}sitemap.xml\n"
    )


def render_llms(scan, cards, meta):
    # < 5 KB authoritative summary + sectioned priority links (VP_SPEC v1.8 6-R.5).
    return (
        "# VP Disease Emergence Kit\n\n"
        "> The VP Disease Emergence Kit reads single-gene diseases as DNA-emergence switch "
        "perturbations and forces each corrective DIRECTION under a strict firewall: promoter "
        "structure is read [V], the axis direction is forced and cited [F], and ALL magnitude "
        "(efficacy, dose, safety) is ungraded [O]. It is a method check that re-derives the direction "
        "of known interventions \u2014 not a discovery engine and not medical advice. Its catalytic "
        f"output, for the {scan['n_no_approved_lead']} diseases with no approved therapy, is "
        f"{scan['n_hypotheses']} cross-disease repurposing hypotheses (a mechanism CLASS approved for a "
        f"same-axis disease, proposed as a testable direction) and {scan['n_orphan_directions']} honest "
        "orphan directions, each with the cheapest experiment that would refute it.\n\n"
        f"Author: {meta['author']} (ORCID {meta['orcid']}). Concept DOI: {meta['doi']}. "
        f"Sibling whitepaper (reproducible burden ordering + standard-of-care context): {COMPANION_DOI}. "
        f"Version {meta['version']} ({meta['date']}). License CC BY 4.0. "
        "Programme: jamming-physics.org (VP Theory / Jamming Physics).\n\n"
        "## core\n"
        f"- [Catalytic output (landing)]({CANONICAL}): {scan['n_resolved']} diseases, repurposing + "
        "open-directions tables, direction-only [O].\n"
        f"- [Repurposing hypotheses]({CANONICAL}#repurposing): same-axis approved donor \u2192 candidate "
        "direction for a no-approved recipient.\n"
        f"- [Open-directions cards]({CANONICAL}#open-directions): no-approved tail as actionable, "
        "falsifiable cards.\n\n"
        "## concepts\n"
        f"- [Method + firewall]({CANONICAL}#method): [V] structure / [F] forced direction / [O] no "
        "magnitude.\n\n"
        "## policies\n"
        "- Direction-only; same-axis \u2260 same-disease; not a diagnosis, treatment, or cure for any "
        "individual. Consult a physician; see Orphanet, NORD, GeneReviews, ClinicalTrials.gov.\n"
    )


# ==================================================================================================
# build / freeze / selftest
# ==================================================================================================
def _load():
    scan = json.load(open(os.path.join(EXPECT, "repurposing_hypotheses.json")))
    cards = json.load(open(os.path.join(EXPECT, "open_directions_cards.json")))
    return scan, cards, _meta()


def build_files():
    """Return {relpath: bytes} for every site file (pure function of frozen inputs)."""
    scan, cards, meta = _load()
    files = {
        "index.html": render_index(scan, cards, meta),
        "sitemap.xml": render_sitemap(meta),
        "robots.txt": render_robots(),
        "llms.txt": render_llms(scan, cards, meta),
    }
    return {k: v.encode("utf-8") for k, v in files.items()}, scan, cards, meta


def write_site(files):
    os.makedirs(SITE, exist_ok=True)
    for rel, data in files.items():
        with open(os.path.join(SITE, rel), "wb") as fh:
            fh.write(data)


def gate(files, scan, cards, meta):
    del FAIL[:]
    idx = files["index.html"].decode("utf-8")

    # banner is the FIRST element inside <body>
    after_body = idx.split("<body>", 1)[1].lstrip()
    check("patient-facing disclaimer banner is the FIRST <body> element",
          after_body.startswith('<aside role="alert" class="vp-sim-disclaimer"'))

    # answer-first: page <p class="answer"> exists and is 40-60 words
    m = re.search(r'<p class="answer">(.*?)</p>', idx, re.S)
    wc = len(re.sub(r"<[^>]+>", "", m.group(1)).split()) if m else 0
    check(f"answer-first <p class=\"answer\"> present and 40-60 words (={wc})", bool(m) and 40 <= wc <= 60)

    # every <section> opens with a self-contained answer paragraph
    secs = re.findall(r"<section\b.*?</section>", idx, re.S)
    check("every <section> opens with an answer-first paragraph (.answer-sec)",
          len(secs) >= 3 and all('class="answer-sec"' in s for s in secs))

    # JSON-LD present, valid, carries ORCID + DOI sameAs
    jm = re.search(r'<script type="application/ld\+json">(.*?)</script>', idx, re.S)
    jl_ok = False
    if jm:
        try:
            obj = json.loads(jm.group(1))
            blob = json.dumps(obj)
            jl_ok = ("schema.org" in obj.get("@context", "")
                     and meta["orcid"] in blob and meta["doi"] in blob
                     and '"@type": "Claim"' in jm.group(1))
        except Exception:
            jl_ok = False
    check("JSON-LD in <head> is valid and carries ORCID + concept DOI + Claim/Rating", jl_ok)

    # firewall: no ASSERTED numeric magnitude (dose / efficacy / response rate) leaked into the page.
    # We flag a NUMBER bound to a dose/efficacy unit -- not the disclaimer words themselves (the page
    # may, and does, say "no efficacy, dose, or response rate is asserted").  Disease COUNTS (e.g.
    # "67 diseases") are not magnitudes and must not trip this.
    text = re.sub(r"<(style|script)\b[^>]*>.*?</\1>", " ", idx, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text).lower()
    magnitude_patterns = [
        r"\d+\s*mg(?:/kg)?\b",                 # 50 mg, 10 mg/kg
        r"\d+(?:\.\d+)?\s*%",                  # 45%
        r"\d+(?:\.\d+)?\s*percent\b",
        r"(?:response rate|cure rate|efficacy|hazard ratio|odds ratio)\s+of\s+\d",
        r"\d+\s+of\s+\d+\s+patients\b",
        r"p\s*[<=]\s*0?\.\d+",                 # p<0.05
    ]
    leaked = [p for p in magnitude_patterns if re.search(p, text)]
    check("no ASSERTED numeric magnitude (dose/efficacy/rate) on the page (firewall)", not leaked)

    # robots staging blocks indexing; sitemap lists canonical; llms.txt < 5KB
    check("robots.txt STAGING blocks all indexing (Disallow: /)",
          "Disallow: /" in files["robots.txt"].decode("utf-8"))
    check("sitemap.xml lists the canonical URL",
          CANONICAL in files["sitemap.xml"].decode("utf-8"))
    llms = files["llms.txt"]
    check(f"llms.txt under 5 KB (={len(llms)} bytes)", len(llms) < 5120)
    check("llms.txt opens with an authoritative blockquote summary",
          llms.decode("utf-8").split("\n\n", 1)[1].lstrip().startswith(">"))

    return not FAIL


def hashes(files):
    return {rel: hashlib.sha256(data).hexdigest() for rel, data in sorted(files.items())}


def selftest():
    """TEETH: two independent builds must be BYTE-IDENTICAL (determinism), and the structural gate
    (banner-first, answer-first, JSON-LD, access tier) must hold."""
    f1, scan, cards, meta = build_files()
    f2, _, _, _ = build_files()
    deterministic = (hashes(f1) == hashes(f2)) and all(f1[k] == f2[k] for k in f1)
    structural = gate(f1, scan, cards, meta)
    ok = deterministic and structural
    print(f"  [self-test] site teeth: deterministic-rebuild={deterministic}  "
          f"structure-gate={structural}  -> {'OK' if ok else 'BROKEN'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    files, scan, cards, meta = build_files()
    write_site(files)
    teeth_ok = selftest()
    h = hashes(files)
    result = {
        "title": "Canonical retrieval-ready site for the kit's catalytic output (VP_SPEC v1.8 6-R)",
        "native_to": "vp_disease_emergence_kit (ROADMAP IV-A); deterministic over frozen scanner + cards",
        "version": meta["version"], "date": meta["date"],
        "canonical": CANONICAL,
        "files": list(h.keys()),
        "sha256": h,
        "overall": "PASS" if teeth_ok else "FAIL",
    }
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "repro", "expected_site_sha256.json")
        json.dump(result, open(p, "w"), indent=1)
        print(f"  wrote {os.path.relpath(p, ROOT)}")
    print("Canonical site build  [NATIVE / ROADMAP IV-A]")
    print(f"  wrote site/ : {', '.join(h.keys())}")
    for rel in h:
        print(f"    {rel:14s} {h[rel][:16]}  ({len(files[rel])} B)")
    print(f"OVERALL: {result['overall']}")
    sys.exit(0 if teeth_ok else 1)
