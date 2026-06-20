#!/usr/bin/env python3
# tools/derive_search.py — VP-SPEC v1.8 Phase 2R (retrieval-readiness derivation).
# Constitution C4 / §6-R. DETERMINISTIC + IDEMPOTENT: same input -> same output.
#
# It does NOT transcribe or invent body text (Ch.1 principle 1, anti-작문).
# It only adds the three v1.8 retrieval hooks, each from a SEALED source:
#   1) <p class="answer">  — answer-first direct answer, condensed from the page's
#      own (gate-validated) .abstract (+ first body sentence only if abstract <40w).
#      Excluded from body word count (gate words_of strips it).
#   2) aside.vp-card       — for each locked cross-quantity (registry-driven) the page
#      cites but does not derive: value + one-line meaning + grade + canonical link.
#      It is an <aside>, already excluded from body word count.
#   3) Enriched JSON-LD     — chapter ScholarlyArticle gains CreativeWorkSeries isPartOf,
#      identifier (DOI), knowsAbout, isBasedOn (repro URL), dateModified; hub gains
#      CreativeWorkSeries @type + hasPart + BreadcrumbList.
#
# Edits touch only head JSON-LD + the .answer/.vp-card hooks — all outside the
# gate's body word-count region, so body words (±0.5%) are unchanged by construction.
#
# Usage: python3 tools/derive_search.py --paper fluid-dynamics [--root .] [--check]
import re, os, sys, csv, json, glob, argparse, datetime

ORCID = "https://orcid.org/0009-0002-7535-8245"
AUTHOR = "Young Jae Lee"
BUILD_DATE = datetime.date(2026, 6, 15).isoformat()   # deterministic build stamp

def read_manifest(root, p):
    return list(csv.DictReader(open(f"{root}/manifest/{p}.csv", encoding="utf-8")))

def load_meta(root, p):
    fp = f"{root}/docs/{p}/_meta.json"
    return json.load(open(fp, encoding="utf-8")) if os.path.exists(fp) else {}

def load_locked(root, p):
    fp = f"{root}/registry/locked_quantities.{p}.json"
    if not os.path.exists(fp):
        return []
    return json.load(open(fp, encoding="utf-8")).get("quantities", [])

# ---------- text helpers (deterministic) ----------
def strip_tags(s):
    s = re.sub(r"<img[^>]*?alt=\"([^\"]*)\"[^>]*>", r" \1 ", s)  # keep eq alt if any
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def sentences(t):
    # split on sentence enders followed by space+capital/end; keep the ender.
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", t)
    return [s.strip() for s in parts if s.strip()]

def wc(t):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9\-'’/×·]*", t))

def grade_of_page(html, vocab):
    # page grade = most frequent grade token on the page (first-seen tie-break).
    order = []
    counts = {}
    for m in re.finditer(r"\[(LOCK|DERIVE|GATE)\]", html):
        tok = m.group(1)
        counts[tok] = counts.get(tok, 0) + 1
        if tok not in order:
            order.append(tok)
    if not counts:
        return None
    best = max(order, key=lambda t: (counts[t], -order.index(t)))
    cls = {"LOCK": "g-lock", "DERIVE": "g-derive", "GATE": "g-gate"}[best]
    return best, cls

# ---------- derivations ----------
def strip_latex_source(s):
    # Remove raw LaTeX *source* fragments (e.g. a body echo `L=2\pi`, `\omega`,
    # `\nabla^2\psi`) while KEEPING Unicode-rendered math the source already shows.
    # Only the backslash-command source form is stripped, never semantic symbols.
    s = re.sub(r"\$[^$]*\$", " ", s)                 # $...$ inline math source
    s = re.sub(r"\\[()\[\]]", " ", s)                # \( \) \[ \] delimiters
    s = re.sub(r"\\[a-zA-Z]+\s*(\{[^{}]*\})?", " ", s)  # \cmd or \cmd{...}
    s = re.sub(r"\s+", " ", s).strip()
    return s

def clean_fragment(s):
    # Drop leading orphan code/delimiter junk like ")}", "}", ")" that some sealed
    # abstracts carry as a broken-off LaTeX tail — it has no semantic content and
    # would otherwise open the answer ungrammatically. Trailing orphans too.
    s = re.sub(r"^[)(}{\]\[;:,.\s]+", "", s.strip())
    s = re.sub(r"[\s({\[]+$", "", s).strip()
    return s

def is_code_echo(s):
    # True for a "sentence" that is really LaTeX/code source, not prose.
    letters = len(re.findall(r"[A-Za-z]", s))
    return s.count("\\") >= 3 or (s.count("\\") > 0 and letters < 12)

def complete(s):
    # A usable unit must end on terminal punctuation (optionally a closing
    # bracket/quote). Drops trailing fragments where the SEALED abstract itself
    # was cut off mid-word/clause, so the derived answer never ends dangling.
    return bool(re.search(r"[.!?][\"')\]]?\s*$", s))

def _sig(s):
    return set(w for w in re.findall(r"[a-z0-9]+", s.lower()) if len(w) >= 3)

def is_dup(s, chosen):
    # Near-duplicate guard: avoid re-adding a sentence (e.g. a body echo of the
    # abstract) whose content-word set heavily overlaps one already selected.
    a = _sig(s)
    if not a:
        return False
    for c in chosen:
        b = _sig(c)
        if b and len(a & b) / min(len(a), len(b)) > 0.6:
            return True
    return False

def prep_text(raw):
    return clean_fragment(strip_latex_source(strip_tags(raw)))

def accumulate(sents, lo=40, hi=60, floor=34):
    # Greedily take WHOLE sentences up to ~hi words; never truncate mid-sentence.
    # Stop before a sentence that would overshoot hi once we are already ≥floor.
    out = []
    for s in sents:
        if is_code_echo(s) or not complete(s) or is_dup(s, out):
            continue
        cur = wc(" ".join(out)) if out else 0
        nxt = wc(" ".join(out + [s]))
        if out and ((cur >= lo and nxt > hi) or (cur >= floor and nxt > hi)):
            break
        out.append(s)
        if wc(" ".join(out)) >= hi:
            break
    return out

def build_answer_text(html):
    """Condense the page's own SEALED abstract into an answer-first block of whole
    sentences (target 40–60 words). Code/LaTeX-source artifacts are removed and
    sentences are never cut mid-clause; all rendered symbols are preserved verbatim.
    Borrows whole body sentences only if the cleaned abstract is severely short."""
    ab = re.search(r'<p class="abstract"[^>]*>(.*?)</p>', html, re.S)
    if not ab:
        return None
    sents = sentences(prep_text(ab.group(1)))
    out = accumulate(sents)
    # Only borrow from the body if the abstract alone is well short of range.
    if wc(" ".join(out)) < 32:
        body = html[ab.end():]
        for bp in re.finditer(r"<p[^>]*>(.*?)</p>", body, re.S):
            for s in sentences(prep_text(bp.group(1))):
                if is_code_echo(s) or not complete(s) or is_dup(s, out):
                    continue
                if wc(" ".join(out + [s])) <= 60:
                    out.append(s)
                if wc(" ".join(out)) >= 40:
                    break
            if wc(" ".join(out)) >= 40:
                break
    text = " ".join(out).strip()
    return text or None

def inject_answer(html):
    if 'class="answer"' in html:
        return html, False
    text = build_answer_text(html)
    if not text:
        return html, False
    g = grade_of_page(html, None)
    badge = f' <span class="grade {g[1]}">[{g[0]}]</span>' if g else ""
    block = f'\n<p class="answer">{text}{badge}</p>'
    # insert immediately after the (single) </h1>
    new, n = re.subn(r"(</h1>)", r"\1" + block.replace("\\", "\\\\"), html, count=1)
    return (new, True) if n else (html, False)

def page_cites(html, q):
    return any(pat in html for pat in q["match"])

def inject_cards(html, slug, locked):
    added = []
    for q in locked:
        if q.get("home_slug") == slug:      # derivation home states it; does not "cite" it
            continue
        if f'data-locked="{q["id"]}"' in html:   # idempotent
            continue
        if not page_cites(html, q):
            continue
        card = (
            f'\n<aside class="vp-card" data-locked="{q["id"]}">'
            f'<b>{q["label"]}</b> — {q["meaning"]} '
            f'<b>{q["grade_token"]}</b> '
            f'<a href="{q["canonical_url"]}">{q["canonical_label"]}</a></aside>'
        )
        # place right after the claim-strip aside (template order); else after </h1>.
        m = re.search(r'(<aside class="claim-strip">.*?</aside>)', html, re.S)
        if m:
            html = html[:m.end()] + card + html[m.end():]
        else:
            html = re.sub(r"(</h1>)", r"\1" + card.replace("\\", "\\\\"), html, count=1)
        added.append(q["id"])
    return html, added

def enrich_chapter_jsonld(html, paper, meta):
    """Upgrade the chapter ScholarlyArticle JSON-LD to the §6-R.4 schema. Idempotent."""
    if '"CreativeWorkSeries"' in html and '"knowsAbout"' in html:
        return html, False
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?"ScholarlyArticle".*?\})\s*</script>', html, re.S)
    if not m:
        return html, False
    try:
        obj = json.loads(m.group(1))
    except Exception:
        return html, False
    doi = meta.get("doi", "")
    short = meta.get("short", "")
    headline = obj.get("headline", "")
    # isPartOf -> CreativeWorkSeries w/ identifier(DOI)
    obj["isPartOf"] = {"@type": "CreativeWorkSeries", "name": meta.get("title", short),
                       "identifier": doi, "sameAs": f"https://doi.org/{doi}"}
    obj["identifier"] = doi
    obj["dateModified"] = BUILD_DATE
    # isBasedOn = the page's reproduction (GitHub) URL from the claim-strip
    repro = re.search(r'href="(https://github\.com/[^"]*/repro/[^"]*)"', html)
    if repro:
        obj["isBasedOn"] = repro.group(1)
    obj.setdefault("author", {"@type": "Person", "name": AUTHOR, "sameAs": ORCID})
    obj["knowsAbout"] = ["jamming lattice", "configured continuum", headline]
    new = json.dumps(obj, ensure_ascii=False)
    return html[:m.start(1)] + new + html[m.end(1):], True

def enrich_hub_jsonld(html, paper, meta, rows):
    """Hub -> CreativeWorkSeries + hasPart + BreadcrumbList (search gate). Idempotent."""
    changed = False
    if '"CreativeWorkSeries"' not in html:
        m = re.search(r'<script type="application/ld\+json">\s*(\{.*?"CollectionPage".*?\})\s*</script>', html, re.S)
        if m:
            try:
                obj = json.loads(m.group(1))
                obj["@type"] = "CreativeWorkSeries"
                obj["hasPart"] = [
                    {"@type": "ScholarlyArticle",
                     "name": r["title"],
                     "url": f"https://jamming-physics.org/{paper}/{r['slug']}/"}
                    for r in rows]
                html = html[:m.start(1)] + json.dumps(obj, ensure_ascii=False) + html[m.end(1):]
                changed = True
            except Exception:
                pass
    if '"BreadcrumbList"' not in html:
        crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                 "itemListElement": [
                     {"@type": "ListItem", "position": 1, "name": "Home",
                      "item": "https://jamming-physics.org/"},
                     {"@type": "ListItem", "position": 2, "name": meta.get("short", ""),
                      "item": f"https://jamming-physics.org/{paper}/"}]}
        block = '<script type="application/ld+json">\n' + json.dumps(crumb, ensure_ascii=False) + '\n</script>\n'
        html = re.sub(r"(</head>)", block + r"\1", html, count=1)
        changed = True
    return html, changed

# ---------- driver ----------
def run(root, paper, check):
    rows = read_manifest(root, paper)
    meta = load_meta(root, paper)
    locked = load_locked(root, paper)
    report = {"paper": paper, "answers": 0, "cards": 0, "jsonld_chapters": 0,
              "hub": False, "per_card": {}}
    for r in rows:
        fp = f"{root}/docs/{paper}/{r['slug']}/index.html"
        if not os.path.exists(fp):
            continue
        html = open(fp, encoding="utf-8").read()
        orig = html
        html, a = inject_answer(html)
        html, cards = inject_cards(html, r["slug"], locked)
        html, j = enrich_chapter_jsonld(html, paper, meta)
        if a: report["answers"] += 1
        if cards:
            report["cards"] += len(cards)
            report["per_card"][r["slug"]] = cards
        if j: report["jsonld_chapters"] += 1
        if html != orig and not check:
            open(fp, "w", encoding="utf-8").write(html)
    hub = f"{root}/docs/{paper}/index.html"
    if os.path.exists(hub):
        html = open(hub, encoding="utf-8").read()
        new, ch = enrich_hub_jsonld(html, paper, meta, rows)
        report["hub"] = ch
        if ch and not check:
            open(hub, "w", encoding="utf-8").write(new)
    print("[derive_search]", json.dumps(report, ensure_ascii=False))
    return report

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--check", action="store_true", help="dry-run; do not write")
    a = ap.parse_args()
    run(a.root, a.paper, a.check)
