#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/upgrade_v1_8.py  --  VP-SPEC v1.8 retrieval-readiness upgrade (paper_id=cosmology)

Deterministic transform (LOCK -> Derive -> Gate). Edits ONLY the v1.8-allowed,
word-count-excluded regions of each docs/cosmology/*/index.html:
  (1) <p class="answer">   answer-first direct answer  (6-R.3) -- after <h1>
  (2) <aside class="vp-card">  self-contained locked-quantity cards (6-R.2) -- after claim-strip
  (3) JSON-LD ScholarlyArticle enriched to 6-R.4 form (+ author/date/isBasedOn/knowsAbout)
  (4) fills empty page-grade span from _meta.json (Phase 2 completion)
  (5) abstract LaTeX normalization (\\href, $, spacing) -- 6-D rule 5, content-preserving

Body text, equations, figures, tables are NEVER touched -> manifest word count invariant.
Idempotent: re-running detects the <!--vp-v1.8--> sentinel and rewrites in place.

Usage:
  python3 tools/upgrade_v1_8.py            # apply in place under docs/cosmology/
  python3 tools/upgrade_v1_8.py --check    # report only, exit 1 if any page not upgraded
"""
import json, re, sys, os, hashlib, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "cosmology"
META = DOCS / "_meta.json"
LOCKS = ROOT / "tools" / "cos_locks.json"

PAPER_ID = "cosmology"
HUB_SHORT = "Vacuum-Inflow Cosmology"
DOI = "10.5281/zenodo.20568874"
ORCID = "https://orcid.org/0009-0002-7535-8245"
AUTHOR = "Young Jae Lee"
REPRO_BASE = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/cosmology"
DATE_PUB = "2026-06-13"
DATE_MOD = "2026-06-15"
SENTINEL = "<!--vp-v1.8-->"

GRADE_NOTE = {
    "degenerate": "same predictions as standard theory",
    "distinguishing": "derivable only in this framework",
    "conflicting": "a falsifiable tension",
}
GRADE_CLASS = {
    "degenerate": "g-degenerate",
    "distinguishing": "g-distinguishing",
    "conflicting": "g-conflicting",
}

# ----------------------------------------------------------------------------- helpers
def load_meta():
    return json.loads(META.read_text(encoding="utf-8"))

def load_locks():
    return json.loads(LOCKS.read_text(encoding="utf-8"))["locks"]

def normalize_text(s: str) -> str:
    """Content-preserving normalization for answer/abstract (6-D rule 5)."""
    # \href{url}{ text } -> text   (keep the visible label, drop TeX wrapper)
    s = re.sub(r"\\href\{[^}]*\}\{\s*([^}]*?)\s*\}", r"\1", s)
    s = re.sub(r"\\href\{[^}]*\}\{\s*([^}]*)$", r"\1", s)  # dangling, unbalanced
    # strip remaining lone TeX spacing / delimiters that leak into prose
    s = s.replace("\\,", " ").replace("\\;", " ").replace("\\!", "")
    s = s.replace("$", "")
    s = re.sub(r"\\(href|text|mathrm|mathsf)\b", "", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    # drop a trailing incomplete clause that ends on a connective/orphan token
    s = re.sub(r"[,;:]\s*(DOI|and|with|the|of|in|to|from|a|an)\s*$", ".", s, flags=re.I)
    return s

def split_sentences(s: str):
    # split on . ! ? followed by space+capital/end; keep decimals & abbreviations intact-ish
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\u00ab])", s)
    return [p.strip() for p in parts if p.strip()]

def wc(s: str) -> int:
    return len([w for w in re.split(r"\s+", s.strip()) if w])

def build_answer(sources, grade: str) -> str:
    """40-60 word self-contained direct answer derived from sealed source text.

    Strategy: take sentences in order; choose the longest sentence-boundary prefix
    whose word count lands in [40,60]. If none fits (a giant lead sentence, or a
    jump straight past 60), fall back to a clean 60-token trim of the first prefix
    that reaches >=40. Nothing is invented -- every word comes from the sealed page.
    """
    LO, HI = 40, 60
    sents, seen_pref = [], set()
    for blk in sources:
        for s in split_sentences(normalize_text(blk)):
            if not s:
                continue
            pref = " ".join(re.sub(r"[^\w\s]", "", s.lower()).split()[:6])
            if s in sents or (pref and pref in seen_pref):
                continue
            sents.append(s); seen_pref.add(pref)

    # build cumulative prefixes
    best_prefix, run, n = None, [], 0
    first_over_lo = None
    for sent in sents:
        run = run + [sent]
        n = sum(wc(x) for x in run)
        if LO <= n <= HI:
            best_prefix = list(run)              # keep extending to the longest in-window prefix
        if n >= LO and first_over_lo is None:
            first_over_lo = list(run)
        if n > HI and best_prefix is not None:
            break                                 # we already have an in-window prefix; stop

    if best_prefix is not None:
        ans = " ".join(best_prefix).strip()
    else:
        # no sentence boundary lands in-window: clean-trim to 60 tokens incl. ellipsis
        src = first_over_lo if first_over_lo else (run if run else [" ".join(sents)])
        words = " ".join(src).split()
        ans = " ".join(words[: HI - 1]).rstrip(",;:") + " \u2026"

    # append the framework verdict if a grade exists and it still fits the window
    if grade in GRADE_NOTE:
        tail = f" VP verdict: {grade} ({GRADE_NOTE[grade]})."
        if wc(ans) + wc(tail) <= HI:
            if not ans.endswith((".", "\u2026", "!", "?")):
                ans += "."
            ans += tail

    # tidy punctuation artifacts from sentence stitching
    ans = re.sub(r"\s*;\s*\.", ".", ans)
    ans = re.sub(r"\s+([.,;:])", r"\1", ans)
    ans = re.sub(r"\.\s*\.", ".", ans)
    ans = re.sub(r"\s{2,}", " ", ans).strip()

    # final guard: never exceed 60 tokens
    words = ans.split()
    if len(words) > HI:
        ans = " ".join(words[: HI - 1]).rstrip(",;:") + " \u2026"
    return ans.strip()

def detect_locks(body_plain: str, slug: str, locks):
    """Cards for locked quantities CITED here but canonically derived elsewhere (6-R.2)."""
    cards = []
    for lk in locks:
        if lk["canon_slug"] == slug:
            continue  # this page is the source; no self-card
        if any(tok in body_plain for tok in lk["tokens"]):
            cards.append(lk)
    return cards[:4]  # cap to keep the chunk clean

def card_html(lk) -> str:
    return (
        f'<aside class="vp-card" data-locked="{lk["key"]}">'
        f'<b>{lk["display"]}</b> \u2014 {lk["meaning"]} '
        f'<b class="grade {lk["badge_class"]}">[{lk["badge"]}]</b> '
        f'<a href="/cosmology/{lk["canon_slug"]}/">{lk["canon_label"]}</a></aside>'
    )

def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", " ", s)

def clean_body_text(raw: str) -> str:
    """Prose text of <main> with non-prose blocks removed (robust to unclosed li/p)."""
    m = re.search(r"<main>(.*?)</main>", raw, flags=re.S)
    body = m.group(1) if m else raw
    for pat in [r"<aside\b.*?</aside>", r"<nav\b.*?</nav>", r"<figure\b.*?</figure>",
                r"<figcaption\b.*?</figcaption>", r"<table\b.*?</table>",
                r"<script\b.*?</script>", r'<p class="abstract".*?</p>',
                r'<p class="answer".*?</p>', r"<h1\b.*?</h1>"]:
        body = re.sub(pat, " ", body, flags=re.S)
    return re.sub(r"\s+", " ", strip_tags(body)).strip()

def key_entity(title: str) -> str:
    """One domain keyword for knowsAbout, from the chapter title (deterministic)."""
    t = title.lower()
    table = [
        ("inflow rate", "inflow rate"), ("light", "elastic-wave light"),
        ("gravity", "vacuum-inflow gravity"), ("solar system", "solar-system test"),
        ("spin", "axial spin"), ("galactic rotation", "galactic rotation curve"),
        ("cosmology", "lattice-optics cosmology"), ("dark matter", "vacuum deficit"),
        ("microwave", "microwave background"), ("post-newtonian", "post-Newtonian sector"),
        ("gravitational wave", "gravitational waves"), ("puzzle", "cosmological puzzles"),
        ("light elements", "primordial nucleosynthesis"), ("acoustic", "acoustic scale"),
        ("structure", "large-scale structure"), ("ledger", "falsifiable predictions"),
        ("constants", "core constants"), ("reproducib", "reproducibility map"),
        ("length scales", "length scales"), ("imports", "import index"),
        ("solar activity", "solar activity"), ("executive", "result scorecard"),
        ("governance", "no-tuning governance"), ("provenance", "provenance ledger"),
        ("misreading", "reviewer doubt trails"), ("version history", "version history"),
        ("meta-lessons", "epistemic audit"),
    ]
    for needle, label in table:
        if needle in t:
            return label
    return "vacuum inflow"

# ----------------------------------------------------------------------------- JSON-LD
def enrich_scholarly(block: str, slug: str, title_entity: str) -> str:
    """Rewrite the ScholarlyArticle JSON-LD to the 6-R.4 enriched form."""
    try:
        obj = json.loads(block)
    except Exception:
        return block
    if obj.get("@type") != "ScholarlyArticle":
        return block
    headline = obj.get("headline", "")
    position = obj.get("position", "")
    try:
        position = int(position)
    except Exception:
        pass
    new = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "headline": headline,
        "isPartOf": {
            "@type": "CreativeWorkSeries",
            "name": HUB_SHORT,
            "identifier": DOI,
            "sameAs": f"https://doi.org/{DOI}",
        },
        "position": position,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "identifier": DOI,
        "datePublished": DATE_PUB,
        "dateModified": DATE_MOD,
        "isBasedOn": f"{REPRO_BASE}/{slug}/",
        "knowsAbout": ["vacuum inflow", "jamming lattice", title_entity],
        "license": "https://creativecommons.org/licenses/by/4.0/",
    }
    return json.dumps(new, ensure_ascii=False)

JSONLD_RE = re.compile(
    r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)

# ----------------------------------------------------------------------------- per page
def process_page(path: Path, ch: dict, locks) -> dict:
    raw = path.read_text(encoding="utf-8")
    slug = ch["slug"]
    grade = ch.get("grade")
    title_entity = key_entity(ch["title"])
    rewritten = (SENTINEL in raw)

    # remove prior v1.8 injections so the run is idempotent
    if rewritten:
        raw = raw.replace(SENTINEL, "")
        raw = re.sub(r'<p class="answer">.*?</p>\s*', "", raw, count=1, flags=re.S)
        raw = re.sub(r'<aside class="vp-card"[^>]*>.*?</aside>\s*', "", raw, flags=re.S)

    # (5) normalize the abstract in place (content-preserving)
    def _norm_abstract(m):
        inner = m.group(2)
        return m.group(1) + normalize_text(inner) + m.group(3)
    raw = re.sub(r'(<p class="abstract"[^>]*>)(.*?)(</p>)', _norm_abstract, raw,
                 count=1, flags=re.S)

    # snapshot the body for lock-citation detection BEFORE we inject the answer,
    # so cards reflect what the body cites (6-R.2), not the generated answer.
    body_plain_src = strip_tags(raw)

    # source pool for answer-first: normalized abstract first, then clean body prose
    # (robust to unclosed <li>/<p>) so short-abstract pages still reach the 40w floor.
    m_abs = re.search(r'<p class="abstract"[^>]*>(.*?)</p>', raw, flags=re.S)
    abstract_text = strip_tags(m_abs.group(1)) if m_abs else ""
    pool = [p for p in [abstract_text, clean_body_text(raw)] if p.strip()] or [ch["title"]]
    answer = build_answer(pool, grade)

    # (1) inject answer-first immediately after the single <h1>...</h1>
    answer_block = f'\n<p class="answer">{html.escape(answer, quote=False)}</p>'
    raw, n_h1 = re.subn(r'(</h1>)', r'\1' + answer_block.replace("\\", "\\\\"),
                        raw, count=1)

    # (4) fill empty page-grade span from _meta (Phase 2 completion)
    if grade in GRADE_CLASS:
        label = f'[{grade}] {grade}'
        raw = re.sub(
            r'(<span class="g)(")( data-phase2="grade">)\s*(</span>)',
            r'\1 ' + GRADE_CLASS[grade] + r'\2\3' + label + r'\4',
            raw, count=1)

    # (2) inject vp-cards after the page claim-strip
    cards = detect_locks(body_plain_src, slug, locks)
    if cards:
        cards_html = "\n" + "\n".join(card_html(c) for c in cards)
        raw = re.sub(r'(</aside>)', r'\1' + cards_html.replace("\\", "\\\\"),
                     raw, count=1)

    # (3) enrich the ScholarlyArticle JSON-LD
    def _enrich(m):
        return m.group(1) + enrich_scholarly(m.group(2).strip(), slug, title_entity) + m.group(3)
    raw = JSONLD_RE.sub(_enrich, raw, count=1)

    # mark upgraded
    raw = raw.replace("<main>", "<main>" + SENTINEL, 1)

    path.write_text(raw, encoding="utf-8")
    return {"slug": slug, "answer_words": wc(answer), "cards": [c["key"] for c in cards],
            "grade": grade, "h1_hit": n_h1}

# ----------------------------------------------------------------------------- driver
def main():
    check = "--check" in sys.argv
    meta = load_meta()
    locks = load_locks()
    chapters = {c["slug"]: c for c in meta["chapters"]}

    if check:
        missing = []
        for slug in chapters:
            p = DOCS / slug / "index.html"
            if p.exists() and 'class="answer"' not in p.read_text(encoding="utf-8"):
                missing.append(slug)
        if missing:
            print("NOT-UPGRADED:", ", ".join(missing)); sys.exit(1)
        print("all pages carry v1.8 answer-first"); return

    results = []
    for slug, ch in chapters.items():
        p = DOCS / slug / "index.html"
        if not p.exists():
            print("  skip (missing):", slug); continue
        results.append(process_page(p, ch, locks))

    n_ans = sum(1 for r in results if r["answer_words"])
    n_card = sum(1 for r in results if r["cards"])
    bad = [r for r in results if not (40 <= r["answer_words"] <= 60) or r["h1_hit"] != 1]
    print(f"upgraded {len(results)} pages | answer-first {n_ans}/{len(results)} | "
          f"pages-with-cards {n_card}")
    for r in results:
        flag = "" if (40 <= r["answer_words"] <= 60 and r["h1_hit"] == 1) else "  <-- CHECK"
        print(f"  {r['slug']:<52} ans={r['answer_words']:>2}w "
              f"cards={','.join(r['cards']) or '-'}{flag}")
    if bad:
        print(f"\nWARN: {len(bad)} page(s) outside the 40-60 answer window or h1 anomaly")

if __name__ == "__main__":
    main()
