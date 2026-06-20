#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_v18_gate.py — VP-SPEC v1.8 gate for the geochronology paper.

Independent of build/ : it recomputes everything from the *written* canonical
HTML, the manifest CSV, and _meta.json. It is a strict SUPERSET of the v1.6
gate (build/gate.py): every v1.6 / v1.7 check is retained, and the v1.8
"C4 retrieval-readiness" + constitution (C1/C2/C3) checks are added on top.

Key v1.8 difference in counting (body invariance):
  count_words() additionally strips .answer and .vp-card, so the injected
  retrieval blocks do NOT perturb the body word count. Because the original
  bodies contained no .answer / .vp-card, the recomputed count equals the
  manifest value EXACTLY (0 drift), which this gate asserts (==, not +/-0.5%).

Usage:
  python3 tools/vp_v18_gate.py [--root /path/to/package]
Writes  <root>/reports/phase1-2-geochronology.gate.json  and prints PASS/FAIL.
"""
import os, re, csv, io, json, hashlib, argparse
import html as _html

# ---- locked registry (spec §2, geochronology row) -------------------------
PAPER_ID = "geochronology"
CODE     = "chr"
SHORT    = "Cross-Chronometer Limit"
TITLE    = "Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit"
DOI      = "10.5281/zenodo.20568673"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
AUTHOR   = "Young Jae Lee"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
SERIES   = "Jamming Physics"
SITE     = "https://jamming-physics.org"
REPRO_URL= "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/geochronology"

GRADE_PRIORITY = ["F", "I", "A"]
GRADE_CLASS = {"F": "g-forced", "I": "g-inferred", "A": "g-assumed"}
GRADE_LABEL = {"F": "directly confirmed", "I": "inferential", "A": "assumption"}
# Chapters that cite the single locked derived quantity (N_D = Dτ/L² ≡ Fo) in a
# self-contained way and must therefore carry a vp-card (matches answers.FO_CARD_ON).
FO_CARD_ON = {"05-unified-protocol",
              "06-demonstration-i-radiocarbon-homogeneous-case"}

# ---------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("--root", default=None,
                help="package root (default: parent of tools/)")
args = ap.parse_args()
ROOT = args.root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(ROOT)
DOCS    = os.path.join(ROOT, "docs", "geochronology")
EQDIR   = os.path.join(ROOT, "docs", "eq", "geochronology")
MANI    = os.path.join(ROOT, "manifest", "geochronology.csv")
REPRO   = os.path.join(ROOT, "repro", "geochronology")
REPORTS = os.path.join(ROOT, "reports")
LEDGER  = os.path.join(ROOT, "IRREPRODUCIBILITY_LEDGER.md")

checks = []   # (name, ok, detail)
warns  = []   # soft (name, detail) — reported, not fatal
def chk(name, ok, detail=""):  checks.append((name, bool(ok), detail))
def warn(name, detail=""):     warns.append((name, detail))
def read(p): return io.open(p, encoding="utf-8").read()

# ---- counting (v1.8: excludes abstract, claim-strip, answer, vp-card) -----
def count_words(main_html):
    s = main_html
    s = re.sub(r'<p class="abstract">.*?</p>', ' ', s, flags=re.S)
    s = re.sub(r'<aside class="claim-strip">.*?</aside>', ' ', s, flags=re.S)
    s = re.sub(r'<p class="answer">.*?</p>', ' ', s, flags=re.S)           # v1.8
    s = re.sub(r'<aside class="vp-card"[^>]*>.*?</aside>', ' ', s, flags=re.S)  # v1.8
    s = re.sub(r'<[^>]+>', ' ', s)
    s = _html.unescape(s)
    return len(s.split())

def count_inline_eq(b):  return len(re.findall(r'class="eq-inline"', b))
# robust to extra attributes (e.g. the §6-R deep-link anchor id="fo")
def count_display_eq(b): return len(re.findall(r'<figure class="eq"[\s>]', b))
def count_tables(b):     return len(re.findall(r'<table', b))
def count_figures(b):
    figs = re.findall(r'<figure(\s+class="([^"]*)")?>', b)
    return sum(1 for _, cls in figs if cls not in ('eq', 'tbl'))

ABS_EQ_CHARS = set("\u00b2\u00b3\u00b9\u2070\u2074\u2075\u2076\u2077\u2078\u2079"
                   "\u2080\u2081\u2082\u2083\u2084\u2085\u2086"
                   "\u2261\u2248\u00b1\u00d7\u00f7\u2265\u2264\u221a\u21d2\u2192"
                   "\u03c4\u03bb\u03c1\u03a8\u0394=/")
def abstract_has_eq(t): return any(c in ABS_EQ_CHARS for c in t)

def main_inner(h):
    m = re.search(r"<main>(.*)</main>", h, re.S)
    return m.group(1) if m else ""
def dom_nodes(h):
    return len(re.findall(r"<[a-zA-Z][^>]*?>", h))
def jsonld_blocks(h):
    out = []
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: out.append(json.loads(b))
        except Exception as e: out.append({"__parse_error__": str(e)})
    return out
def word_count_text(t):
    return len(t.split())
def n_sentences(t):
    t = t.strip()
    if not t: return 0
    return len([x for x in re.split(r'(?<=[.!?])\s+', t) if x.strip()])

# ---- load manifest --------------------------------------------------------
with io.open(MANI, encoding="utf-8") as f:
    man = list(csv.DictReader(f))
man_by_slug = {r["slug"]: r for r in man}

chapter_dirs = sorted(d for d in os.listdir(DOCS)
                      if os.path.isdir(os.path.join(DOCS, d)) and d != "img")
chk("section_count == manifest_rows == 14",
    len(chapter_dirs) == len(man) == 14,
    "dirs=%d manifest=%d" % (len(chapter_dirs), len(man)))

# ---- _meta.json -----------------------------------------------------------
meta = json.load(io.open(os.path.join(DOCS, "_meta.json"), encoding="utf-8"))
meta_by_slug = {c["slug"]: c for c in meta["chapters"]}

svgs = sorted(f for f in os.listdir(EQDIR) if f.endswith(".svg"))
svg_set = set(svgs)
total_display = 0
referenced_svgs = set()
broken_links = []
all_targets = {"/geochronology/%s/" % d for d in chapter_dirs}
all_targets.add("/geochronology/")

def page_grade_from_body(body):
    toks = re.findall(r'<span class="tag t([FIA])">', body)
    if not toks: return None
    counts = {g: toks.count(g) for g in set(toks)}
    best = max(counts.values())
    for g in GRADE_PRIORITY:
        if counts.get(g, 0) == best: return g
    return None

# ---- per-chapter ----------------------------------------------------------
for d in chapter_dirs:
    H = read(os.path.join(DOCS, d, "index.html"))
    row = man_by_slug.get(d)
    mi = main_inner(H)
    # body = main minus retrieval blocks (for grade + sentence checks)
    body = re.sub(r'<p class="answer">.*?</p>', ' ', mi, flags=re.S)
    body = re.sub(r'<aside class="vp-card"[^>]*>.*?</aside>', ' ', body, flags=re.S)

    eqi, eqd = count_inline_eq(mi), count_display_eq(mi)
    fig, tbl = count_figures(mi), count_tables(mi)
    wc = count_words(mi)
    total_display += eqd

    if row is not None:
        chk("[%s] eq_inline==manifest" % d, eqi == int(row["eq_inline"]),
            "html=%d man=%s" % (eqi, row["eq_inline"]))
        chk("[%s] eq_display==manifest" % d, eqd == int(row["eq_display"]),
            "html=%d man=%s" % (eqd, row["eq_display"]))
        chk("[%s] figures==manifest" % d, fig == int(row["figures"]),
            "html=%d man=%s" % (fig, row["figures"]))
        chk("[%s] tables==manifest" % d, tbl == int(row["tables"]),
            "html=%d man=%s" % (tbl, row["tables"]))
        # v1.8: EXACT word count (0 drift) — retrieval blocks excluded
        mw = int(row["words"])
        chk("[%s] wordcount==manifest (0 drift)" % d, wc == mw,
            "html=%d man=%d" % (wc, mw))

    # ---- v1.6 structural --------------------------------------------------
    chk("[%s] no katex residue" % d, 'class="katex' not in H)
    size = len(H.encode("utf-8"))
    chk("[%s] html<=300KB" % d, size <= 300 * 1024, "%d bytes" % size)
    nodes = dom_nodes(H)
    chk("[%s] dom<=3000" % d, nodes <= 3000, "%d nodes" % nodes)

    mt = re.search(r"<title>(.*?)</title>", H)
    title = mt.group(1) if mt else ""
    pat = re.match(r"^(.*?) \u2014 %s \u00a7(\d+) \| Jamming Physics$"
                   % re.escape(SHORT), title)
    chk("[%s] title pattern" % d, bool(pat), title)
    if pat:
        chk("[%s] subject<=45" % d, len(pat.group(1)) <= 45,
            "len=%d" % len(pat.group(1)))
    chk("[%s] title<=90" % d, len(title) <= 90, "len=%d" % len(title))

    md = re.search(r'<meta name="description" content="(.*?)">', H)
    desc = _html.unescape(md.group(1)) if md else ""
    chk("[%s] desc 80-160" % d, 80 <= len(desc) <= 160, "len=%d" % len(desc))

    chk("[%s] h1==1" % d, len(re.findall(r"<h1[ >]", H)) == 1)

    ma = re.search(r'<p class="abstract">(.*?)</p>', H, re.S)
    abok = bool(ma) and abstract_has_eq(_html.unescape(re.sub(r"<[^>]+>", "", ma.group(1))))
    chk("[%s] abstract+eq" % d, abok)
    chk("[%s] repro folder exists" % d, os.path.isdir(os.path.join(REPRO, d)))

    for src in re.findall(r'<img[^>]+src="/eq/geochronology/([^"]+)"', H):
        referenced_svgs.add(src)
    for href in re.findall(r'href="(/geochronology/[^"#]*)"', H):
        if href not in all_targets:
            broken_links.append("%s -> %s" % (d, href))

    # ==== v1.8 §6-R: answer-first ==========================================
    am = re.search(r'<p class="answer">(.*?)</p>', mi, re.S)
    chk("[%s] answer-first present" % d, bool(am))
    if am:
        # must be the FIRST content block after </h1>
        after_h1 = mi.split("</h1>", 1)[1] if "</h1>" in mi else mi
        first_block = re.search(r'<(p|aside|figure|section|div|ul|ol|table)\b[^>]*>',
                                after_h1)
        is_first = bool(first_block) and first_block.group(0).startswith('<p class="answer"')
        chk("[%s] answer-first is first block" % d, is_first,
            first_block.group(0) if first_block else "none")
        atext = _html.unescape(re.sub(r"<[^>]+>", "", am.group(1))).strip()
        n = word_count_text(atext)
        chk("[%s] answer 40-60 words" % d, 40 <= n <= 60, "words=%d" % n)
        # self-contained: stands alone -> must NOT defer to another section via a
        # dangling pointer ("see §x", "as shown above/below", "previous/next section").
        dangling = re.search(r'\b(see\s+\u00a7|as (shown|noted|discussed) (above|below)'
                             r'|in the (previous|next|preceding|following) section'
                             r'|\bsee above\b|\bsee below\b)', atext, re.I)
        chk("[%s] answer self-contained (no dangling ref)" % d, dangling is None,
            dangling.group(0) if dangling else "")

    # ==== v1.8 §6-R: vp-card for locked quantity ===========================
    has_card = 'class="vp-card"' in mi
    if d in FO_CARD_ON:
        chk("[%s] vp-card present (locked Fo cited)" % d, has_card)
        if has_card:
            cm = re.search(r'<aside class="vp-card"[^>]*>(.*?)</aside>', mi, re.S)
            ctext = _html.unescape(re.sub(r"<[^>]+>", " ", cm.group(1)))
            chk("[%s] vp-card carries value+grade+link" % d,
                ("N_D" in cm.group(1) or "Fo" in cm.group(1)) and
                bool(re.search(r"\[[FIA]\]", cm.group(1))) and
                "href=" in cm.group(1),
                "")

    # ==== v1.7/v1.8: grade span in claim-strip =============================
    g_expected = page_grade_from_body(body)
    span = re.search(r'<span class="grade (g-\w+)">\[([FIA])\][^<]*</span>', H)
    if g_expected is None:
        chk("[%s] grade span absent (no body tokens)" % d, span is None,
            "found=%s" % (span.group(2) if span else None))
    else:
        chk("[%s] grade span == most-frequent token" % d,
            bool(span) and span.group(2) == g_expected and
            span.group(1) == GRADE_CLASS[g_expected],
            "span=%s exp=%s" % (span.group(2) if span else None, g_expected))
    # _meta grade agreement
    if d in meta_by_slug:
        chk("[%s] _meta.grade == computed" % d,
            meta_by_slug[d].get("grade") == g_expected,
            "meta=%s comp=%s" % (meta_by_slug[d].get("grade"), g_expected))

    # ==== v1.8 §6-R.4: JSON-LD ScholarlyArticle ============================
    blocks = jsonld_blocks(H)
    art = next((b for b in blocks if b.get("@type") == "ScholarlyArticle"), None)
    bcr = next((b for b in blocks if b.get("@type") == "BreadcrumbList"), None)
    chk("[%s] JSON-LD ScholarlyArticle present" % d, art is not None)
    if art:
        ip = art.get("isPartOf", {})
        req = {
            "isPartOf=CreativeWorkSeries": ip.get("@type") == "CreativeWorkSeries",
            "isPartOf.identifier=DOI": ip.get("identifier") == DOI,
            "identifier=DOI": art.get("identifier") == DOI,
            "datePublished": bool(art.get("datePublished")),
            "dateModified": bool(art.get("dateModified")),
            "isBasedOn(repro)": str(art.get("isBasedOn", "")).startswith(REPRO_URL),
            "author.sameAs=ORCID": (art.get("author", {}) or {}).get("sameAs") == ORCID,
            "license=CCBY": art.get("license") == LICENSE,
            "knowsAbout[]": isinstance(art.get("knowsAbout"), list) and len(art["knowsAbout"]) >= 1,
        }
        missing = [k for k, v in req.items() if not v]
        chk("[%s] JSON-LD 6-R.4 fields complete" % d, not missing,
            "missing=%s" % ",".join(missing))
    chk("[%s] JSON-LD BreadcrumbList present" % d, bcr is not None)

    # ==== v1.8 soft: paragraphs <= 3 sentences =============================
    for p in re.findall(r'<p>(.*?)</p>', body, re.S):
        ptext = _html.unescape(re.sub(r"<[^>]+>", " ", p)).strip()
        ns = n_sentences(ptext)
        if ns > 3:
            warn("[%s] paragraph >3 sentences (soft)" % d, "%d sentences: %s" % (ns, ptext[:50]))

# ---- display-eq vs svg ----------------------------------------------------
chk("display_eq_total == svg_count", total_display == len(svgs),
    "display=%d svg=%d" % (total_display, len(svgs)))
chk("no missing svg", referenced_svgs <= svg_set, "missing=%s" % (referenced_svgs - svg_set))
chk("no orphan svg", svg_set <= referenced_svgs, "orphan=%s" % (svg_set - referenced_svgs))

# ---- hub ------------------------------------------------------------------
hub = read(os.path.join(DOCS, "index.html"))
ov = re.search(r'<section class="overview">(.*?)</section>', hub, re.S)
ov_words = count_words(ov.group(1)) if ov else 0
chk("hub overview 1500-3000", 1500 <= ov_words <= 3000, "words=%d" % ov_words)
toc_links = set(re.findall(r'href="/geochronology/([^"/]+)/"', hub))
chk("hub TOC links all chapters", set(chapter_dirs) <= toc_links,
    "missing=%s" % (set(chapter_dirs) - toc_links))
chk("hub cross-link /physics/", 'href="/physics/"' in hub)
chk("hub cross-link /geodynamics/", 'href="/geodynamics/"' in hub)
chk("hub <h2 id=references>", 'id="references"' in hub)
for href in re.findall(r'href="(/geochronology/[^"#]*)"', hub):
    if href not in all_targets:
        broken_links.append("hub -> %s" % href)
chk("internal links 0 broken", len(broken_links) == 0, "; ".join(broken_links[:6]))

# hub answer-first
ham = re.search(r'<p class="answer">(.*?)</p>', hub, re.S)
chk("hub answer-first present", bool(ham))
if ham:
    htext = _html.unescape(re.sub(r"<[^>]+>", "", ham.group(1))).strip()
    hn = word_count_text(htext)
    chk("hub answer 40-60 words", 40 <= hn <= 60, "words=%d" % hn)

# hub JSON-LD CreativeWorkSeries + hasPart(14)
hblocks = jsonld_blocks(hub)
series = next((b for b in hblocks if b.get("@type") in ("CreativeWorkSeries", "Book")), None)
hbcr   = next((b for b in hblocks if b.get("@type") == "BreadcrumbList"), None)
chk("hub JSON-LD CreativeWorkSeries/Book present", series is not None)
if series:
    hp = series.get("hasPart", [])
    chk("hub JSON-LD hasPart == 14", isinstance(hp, list) and len(hp) == 14,
        "hasPart=%d" % (len(hp) if isinstance(hp, list) else -1))
    chk("hub JSON-LD identifier=DOI", series.get("identifier") == DOI,
        str(series.get("identifier")))
    # ORCID identifies the author (author.sameAs); DOI identifies the work (series.sameAs)
    sa = series.get("sameAs", [])
    sa = sa if isinstance(sa, list) else [sa]
    auth = series.get("author", {}) or {}
    auth_sa = auth.get("sameAs", [])
    auth_sa = auth_sa if isinstance(auth_sa, list) else [auth_sa]
    chk("hub JSON-LD ORCID present (author/series)",
        any(ORCID in str(x) for x in sa + auth_sa), str(sa + auth_sa))
    chk("hub JSON-LD DOI in sameAs", any(DOI in str(x) for x in sa + [series.get("identifier")]),
        str(sa))
chk("hub JSON-LD BreadcrumbList present", hbcr is not None)

# ==== Constitution C1/C2/C3 ===============================================
# C2: no TeX / eq_list / txt sources anywhere in the package
forbidden = []
for dp, dn, fn in os.walk(ROOT):
    # skip the working backup + caches if present
    base = os.path.relpath(dp, ROOT)
    if base.startswith("docs__bak") or "__pycache__" in dp or base.startswith(".git"):
        continue
    for f in fn:
        low = f.lower()
        if low.endswith(".tex") or low.endswith(".sty") or "eq_list" in low:
            forbidden.append(os.path.relpath(os.path.join(dp, f), ROOT))
    for sub in list(dn):
        if sub == "txt":
            forbidden.append(os.path.relpath(os.path.join(dp, sub), ROOT) + "/")
chk("C2 no TeX/eq_list/txt in package", len(forbidden) == 0,
    "found=%s" % "; ".join(forbidden[:8]))

# C1: HTML is canonical & counts reconcile with manifest AND _meta
recon = True; rdet = []
for c in meta["chapters"]:
    slug = c["slug"]; row = man_by_slug.get(slug)
    H = read(os.path.join(DOCS, slug, "index.html"))
    wc = count_words(main_inner(H))
    if row and (wc != int(row["words"]) or wc != int(c.get("words", -1))):
        recon = False; rdet.append("%s html=%d man=%s meta=%s" %
                                    (slug, wc, row["words"], c.get("words")))
chk("C1 counts reconcile (HTML==manifest==_meta)", recon, "; ".join(rdet[:5]))

# C3: ledger present and lists [O] status
chk("C3 irreproducibility ledger present", os.path.isfile(LEDGER))
if os.path.isfile(LEDGER):
    L = read(LEDGER)
    chk("C3 ledger states [O] status", "[O]" in L or "no `[O]`" in L.lower()
        or "no [o]" in L.lower())

# ---- tools hash -----------------------------------------------------------
TOOLS = os.path.dirname(os.path.abspath(__file__))
h = hashlib.sha256()
for fn in sorted(os.listdir(TOOLS)):
    if fn.endswith((".py", ".mjs")):
        h.update(io.open(os.path.join(TOOLS, fn), "rb").read())
tools_hash = h.hexdigest()[:16]

# ---- verdict --------------------------------------------------------------
passed = all(ok for _, ok, _ in checks)
fails = [(n, d) for n, ok, d in checks if not ok]

os.makedirs(REPORTS, exist_ok=True)
report = {
    "phase": "1-2",
    "paper_id": "geochronology",
    "spec": "VP-SPEC v1.8",
    "verdict": "PASS" if passed else "FAIL",
    "n_checks": len(checks),
    "n_failed": len(fails),
    "n_warnings": len(warns),
    "tools_hash": tools_hash,
    "totals": {
        "chapters": len(chapter_dirs),
        "svgs": len(svgs),
        "display_eq": total_display,
        "manifest_rows": len(man),
        "grades": {c["slug"]: c.get("grade") for c in meta["chapters"]},
    },
    "v18_features": {
        "answer_first_chapters": 14,
        "vp_cards": sorted(FO_CARD_ON),
        "jsonld_schema": "6-R.4 (ScholarlyArticle + CreativeWorkSeries)",
        "word_count_drift": 0,
    },
    "constitution": {
        "C1_reproducible": "PASS" if all(ok for n, ok, _ in checks if n.startswith("C1")) else "FAIL",
        "C2_html_canonical_no_tex": "PASS" if all(ok for n, ok, _ in checks if n.startswith("C2")) else "FAIL",
        "C3_ledger": "PASS" if all(ok for n, ok, _ in checks if n.startswith("C3")) else "FAIL",
        "C4_retrieval_ready": "PASS" if passed else "FAIL",
    },
    "failed": [{"check": n, "detail": d} for n, d in fails],
    "warnings": [{"check": n, "detail": d} for n, d in warns],
}
io.open(os.path.join(REPORTS, "phase1-2-geochronology.gate.json"), "w",
        encoding="utf-8").write(json.dumps(report, ensure_ascii=False, indent=2))

print("=" * 60)
print("VP-SPEC v1.8 GATE — geochronology")
print("root       :", ROOT)
print("checks run :", len(checks))
print("failed     :", len(fails))
print("warnings   :", len(warns), "(soft, non-fatal)")
for n, d in fails:
    print("   FAIL", n, "|", d)
print("VERDICT    :", report["verdict"])
print("tools_hash :", tools_hash)
print("=" * 60)
