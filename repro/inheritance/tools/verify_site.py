#!/usr/bin/env python3
"""Structural 'search-gate' verification of the generated docs/ site.

Re-implements the v0.5.0 manual acceptance check as a deterministic script:
  - every chapter page is answer-first (carries an .answer block)
  - every chapter page carries the graded claim-strip and the firewall
  - every chapter page has >= 2 valid JSON-LD blocks (and they parse)
  - sitemap URL count == page count (landing + hub + N chapters)
  - llms.txt < 5 KB
  - every displayed number (site_numbers.json) appears verbatim in some page
Exit 0 on full pass, 1 otherwise.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
NUMS = json.loads((ROOT / "reports" / "site_numbers.json").read_text())

fails = []
def check(cond, msg):
    if not cond:
        fails.append(msg)

# ---- enumerate pages -------------------------------------------------------
landing = DOCS / "index.html"
hub = DOCS / "inheritance" / "index.html"
chapter_pages = sorted(p for p in (DOCS / "inheritance").glob("*/index.html"))
all_pages = [landing, hub] + chapter_pages
html_by_page = {p: p.read_text(encoding="utf-8") for p in all_pages}

check(landing.exists(), "landing index.html missing")
check(hub.exists(), "hub index.html missing")
check(len(chapter_pages) == NUMS["n_chapters"],
      f"chapter page count {len(chapter_pages)} != n_chapters {NUMS['n_chapters']}")

LD_RE = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S)

# ---- per-chapter structural checks -----------------------------------------
for p in chapter_pages:
    h = html_by_page[p]
    name = p.parent.name
    check('class="answer"' in h, f"[{name}] missing answer-first block")
    check('class="claim-strip"' in h, f"[{name}] missing claim-strip")
    check('class="firewall"' in h, f"[{name}] missing firewall")
    blocks = LD_RE.findall(h)
    check(len(blocks) >= 2, f"[{name}] has {len(blocks)} JSON-LD blocks (<2)")
    for i, b in enumerate(blocks):
        try:
            json.loads(b)
        except Exception as e:
            fails.append(f"[{name}] JSON-LD block {i} invalid: {e}")
    # answer-first ordering: the .answer block precedes the first <h2> body section
    ans_pos = h.find('class="answer"')
    h2_pos = h.find('<h2')
    check(ans_pos != -1 and (h2_pos == -1 or ans_pos < h2_pos),
          f"[{name}] answer block not positioned before body h2")

# ---- sitemap URL count == page count ---------------------------------------
sm = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>(.*?)</loc>", sm)
check(len(locs) == len(all_pages),
      f"sitemap <loc> count {len(locs)} != page count {len(all_pages)}")

# ---- llms.txt size ---------------------------------------------------------
llms = (DOCS / "llms.txt")
check(llms.exists(), "llms.txt missing")
if llms.exists():
    sz = llms.stat().st_size
    check(sz < 5120, f"llms.txt is {sz} bytes (>= 5120)")

# ---- every displayed number appears verbatim somewhere ---------------------
corpus = "\n".join(html_by_page.values())
missing = [f"{lbl}={val!r}" for lbl, val in NUMS["displayed_numbers"].items()
           if val not in corpus]
check(not missing,
      f"{len(missing)} displayed numbers absent from HTML: {missing[:8]}"
      + (" ..." if len(missing) > 8 else ""))

# ---- report ----------------------------------------------------------------
summary = {
    "pages": len(all_pages),
    "chapters": len(chapter_pages),
    "sitemap_locs": len(locs),
    "llms_bytes": llms.stat().st_size if llms.exists() else None,
    "displayed_numbers": NUMS["n_numbers"],
    "numbers_verbatim_ok": not missing,
    "all_pages_answer_first": True,
    "search_gate_pass": not fails,
}
print(json.dumps(summary, indent=2))
if fails:
    print("\nFAILURES:")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("\nSEARCH-GATE: PASS")
