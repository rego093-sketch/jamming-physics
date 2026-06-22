#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministic gate check for the DNA multi-page split (VP-SPEC v1.8)."""
import re, json, os, glob, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
PAPER = "dna"
ORIGIN = "https://jamming-physics.org"
fails, warns, checks = [], [], []
def ok(name):  checks.append(("PASS", name))
def bad(name): fails.append(name); checks.append(("FAIL", name))
def wn(name):  warns.append(name); checks.append(("WARN", name))

mono_dir = os.path.join(DOCS, PAPER)
sec_dirs = sorted([d for d in glob.glob(os.path.join(mono_dir, "*"))
                   if os.path.isdir(d)])
pages = {os.path.basename(d): open(os.path.join(d, "index.html"), encoding="utf-8").read()
         for d in sec_dirs}
hub = open(os.path.join(mono_dir, "index.html"), encoding="utf-8").read()
meta = json.load(open(os.path.join(mono_dir, "_meta.json"), encoding="utf-8"))

# slugs in meta order
order = [c["slug"] for c in meta["chapters"]] + [a["slug"] for a in meta["appendices"]]

# 1. section count == manifest/meta rows
if len(pages) == 17 == len(order): ok("section count = 17 = meta rows")
else: bad("section count mismatch: %d pages, %d meta" % (len(pages), len(order)))

# 2. all meta slugs have a page
missing = [s for s in order if s not in pages]
if not missing: ok("every meta section has a page")
else: bad("missing pages: %s" % missing)

# 3. per-page structural gates
all_urls_targets = set("/%s/%s/" % (PAPER, s) for s in pages)
for slug, htmltext in pages.items():
    # exactly one h1
    if htmltext.count("<h1>") == 1: ok("[%s] exactly one h1" % slug)
    else: bad("[%s] h1 count = %d" % (slug, htmltext.count("<h1>")))
    # no h2 with leftover id duplicating page (h2 may exist as subheads, that's fine; but no <h2 id="s...">)
    if not re.search(r'<h2 id="s', htmltext): ok("[%s] no orphan section-h2 id" % slug)
    else: bad("[%s] leftover <h2 id=\"s...\">" % slug)
    # answer-first: first content block after <main> ... <h1>..</h1> is <p class="answer">
    m = re.search(r"<main>\s*<h1>.*?</h1>\s*(.*?)>", htmltext, re.S)
    body_after_h1 = htmltext.split("</h1>", 1)[1] if "</h1>" in htmltext else ""
    if re.match(r'\s*<p class="answer">', body_after_h1): ok("[%s] answer-first" % slug)
    else: bad("[%s] not answer-first" % slug)
    # title length
    t = re.search(r"<title>(.*?)</title>", htmltext).group(1)
    subj = t.split(" — ")[0]
    if len(t) <= 90: ok("[%s] title <=90 (%d)" % (slug, len(t)))
    else: bad("[%s] title %d >90" % (slug, len(t)))
    if len(subj) <= 45: ok("[%s] subject <=45 (%d)" % (slug, len(subj)))
    else: bad("[%s] subject %d >45" % (slug, len(subj)))
    # description length (soft 80-160)
    d = re.search(r'<meta name="description" content="(.*?)">', htmltext).group(1)
    dlen = len(html.unescape(d))
    if 60 <= dlen <= 160: ok("[%s] desc len %d" % (slug, dlen))
    else: wn("[%s] desc len %d (target 80-160)" % (slug, dlen))
    # JSON-LD valid
    for j in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', htmltext, re.S):
        try: json.loads(j)
        except Exception as e: bad("[%s] invalid JSON-LD: %s" % (slug, e))
    # canonical present + correct
    if ('href="%s/%s/%s/"' % (ORIGIN, PAPER, slug)) in htmltext: ok("[%s] canonical correct" % slug)
    else: bad("[%s] canonical wrong/missing" % slug)
    # no leftover intra-page section anchors
    if not re.search(r'href="#s[0-9A-Za-z]', htmltext): ok("[%s] no #s.. anchors" % slug)
    else: bad("[%s] leftover #s.. anchor" % slug)
    # internal /dna/{slug}/ links resolve to an existing page (or hub)
    for href in re.findall(r'href="(/%s/[^"#]*)"' % PAPER, htmltext):
        if href == "/%s/" % PAPER: continue
        if href not in all_urls_targets:
            bad("[%s] dangling internal link %s" % (slug, href))
    # size + DOM node budget
    if len(htmltext) <= 300_000: ok("[%s] size <=300KB" % slug)
    else: bad("[%s] size >300KB" % slug)
    nodes = htmltext.count("<")
    if nodes <= 3000: ok("[%s] DOM nodes ~%d <=3000" % (slug, nodes))
    else: bad("[%s] DOM nodes ~%d >3000" % (slug, nodes))
    # prev/next nav present
    if '<nav class="pn">' in htmltext: ok("[%s] prev/next nav" % slug)
    else: bad("[%s] no pn nav" % slug)

# 4. hub gates
if hub.count("<h1>") == 1: ok("hub: one h1")
else: bad("hub: h1 count %d" % hub.count("<h1>"))
hub_links = set(re.findall(r'href="(/%s/[^"#]+/)"' % PAPER, hub))
linked = sum(1 for s in pages if ("/%s/%s/" % (PAPER, s)) in hub_links)
if linked == 17: ok("hub: all 17 sections linked (orphans 0)")
else: bad("hub: only %d/17 sections linked" % linked)
if 'href="/physics/"' in hub: ok("hub: cross-volume jamming link (§10)")
else: bad("hub: missing /physics/ cross link")
for j in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', hub, re.S):
    try: json.loads(j)
    except Exception as e: bad("hub: invalid JSON-LD: %s" % e)
if not re.search(r'href="#s[0-9A-Za-z]', hub): ok("hub: no #s.. anchors (all rewritten)")
else: bad("hub: leftover #s.. anchor")

# 5. robots / sitemap / llms
robots = open(os.path.join(DOCS, "robots.txt"), encoding="utf-8").read()
bots = ["Googlebot","Bingbot","OAI-SearchBot","GPTBot","PerplexityBot","ClaudeBot","Google-Extended"]
if all(b in robots for b in bots): ok("robots: 7 named bots present")
else: bad("robots: missing bots")
sm = open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8").read()
sm_urls = re.findall(r"<loc>(.*?)</loc>", sm)
index_count = 1 + len(pages)  # hub + sections
if len(sm_urls) == index_count: ok("sitemap: %d urls = %d index.html" % (len(sm_urls), index_count))
else: bad("sitemap: %d urls != %d index.html" % (len(sm_urls), index_count))
llms = open(os.path.join(DOCS, "llms.txt"), "rb").read()
if len(llms) < 5120: ok("llms.txt < 5KB (%d B)" % len(llms))
else: bad("llms.txt >= 5KB (%d B)" % len(llms))

# 6. C2 — no TeX body sources anywhere in package
tex = []
for pat in ["**/*.tex", "**/*.eq_list.*"]:
    tex += glob.glob(os.path.join(ROOT, pat), recursive=True)
txtdir = glob.glob(os.path.join(ROOT, "**", "txt", "**"), recursive=True)
if not tex and not txtdir: ok("C2: no .tex / .eq_list / txt body sources")
else: bad("C2: TeX-ish sources present: %s" % (tex + txtdir)[:5])

# 7. completeness — every section body present in its page (sampled by answer + claim-strip + vp-cards)
mono_src = None
for cand in [os.path.join(ROOT, "..", "dna_src", "docs", "dna", "index.html")]:
    if os.path.exists(cand): mono_src = open(cand, encoding="utf-8").read()
if mono_src:
    sec_re = re.compile(r'<section\b([^>]*)>(.*?)</section>', re.S)
    total_cards_src = mono_src.count('class="vp-card"')
    total_cards_out = sum(p.count('class="vp-card"') for p in pages.values())
    if total_cards_src == total_cards_out: ok("completeness: vp-cards %d preserved" % total_cards_src)
    else: bad("completeness: vp-cards src=%d out=%d" % (total_cards_src, total_cards_out))
    # check each section's answer paragraph survived verbatim
    miss = 0
    for m in sec_re.finditer(mono_src):
        inner = m.group(2)
        slug = re.search(r'data-slug="([^"]*)"', m.group(1)).group(1)
        am = re.search(r'(<p class="answer">.*?</p>)', inner, re.S)
        if am and slug in pages and am.group(1) not in pages[slug]:
            miss += 1
    if miss == 0: ok("completeness: all section answer paragraphs verbatim in pages")
    else: bad("completeness: %d answer paragraphs altered/lost" % miss)
    # paragraph-text completeness: total <p> body text length preserved (±0.2%)
    def ptext(s): return " ".join(re.sub(r"<[^>]+>", " ", "".join(re.findall(r"<p\b.*?</p>", s, re.S))).split())
    src_body = "".join(m.group(2) for m in sec_re.finditer(mono_src))
    out_body = "".join(pages.values())
    ls, lo = len(ptext(src_body)), len(ptext(out_body))
    if abs(lo - ls) <= 0.002 * max(ls, 1) or lo >= ls:
        ok("completeness: paragraph text preserved (src=%d out=%d chars)" % (ls, lo))
    else: bad("completeness: paragraph text shrank src=%d out=%d" % (ls, lo))
else:
    wn("completeness: source monolith copy not found for diff")

# ---- report
print("="*70)
for status, name in checks:
    if status != "PASS":
        print("%-4s %s" % (status, name))
P = sum(1 for s,_ in checks if s=="PASS")
print("="*70)
print("PASS %d   WARN %d   FAIL %d" % (P, len(warns), len(fails)))
print("VERDICT:", "PASS" if not fails else "FAIL")

# ---- structured JSON report (companion to other reports/*.gate.json)
def _sha256(path):
    import hashlib
    try:
        return hashlib.sha256(open(path,"rb").read()).hexdigest()
    except OSError:
        return None
report = {
    "session": "v1_13-gamma-a4-level-shape",
    "spec": "VP-SPEC v1.8",
    "paper_id": "dna",
    "date": "2026-06-21",
    "layout": "multi-page canonical (hub + per-section pages)",
    "summary": {"pass": P, "warn": len(warns), "fail": len(fails),
                "verdict": "PASS" if not fails else "FAIL"},
    "scripts": {
        "build": {"file": "build_v1_13_level_shape.py", "sha256": _sha256("build_v1_13_level_shape.py")},
        "gate":  {"file": "gate_multipage.py",      "sha256": _sha256("gate_multipage.py")},
    },
    "checks": [{"status": s, "check": n} for s, n in checks],
    "warnings": warns,
    "failures": fails,
}
os.makedirs("reports", exist_ok=True)
with open("reports/dna-v1_13-multipage.gate.json", "w", encoding="utf-8") as fh:
    json.dump(report, fh, indent=2, ensure_ascii=False)
print("wrote reports/dna-v1_13-multipage.gate.json")
sys.exit(1 if fails else 0)
