#!/usr/bin/env python3
"""
gate_v1_8.py — VP_SPEC v1.8 §8 search gate + Constitution C1/C2/C3 checks.

Verifies the upgraded cosmology package and writes
reports/phase-v1_8-cosmology.gate.json. Exit 0 only if every HARD check passes;
soft checks (paragraph length) emit warnings but do not fail the gate.

HARD checks
  pages   : each chapter has answer-first (first <p> after <h1>, 40-60 words),
            a valid 6-R.4 ScholarlyArticle JSON-LD, and a BreadcrumbList.
  hub     : CreativeWorkSeries/Book JSON-LD (identifier == DOI), BreadcrumbList,
            5 Highwire citation tags, answer-first.
  infra   : robots.txt (7 bots + Sitemap), sitemap.xml (well-formed, 29 URLs),
            llms.txt (< 5 KB, sectioned), llms-full.txt (non-empty).
  C1      : _meta totals == manifest sums; hub overview line agrees.
  C2      : distribution tree carries no TeX/SSOT sources under docs/.
  C3      : IRREPRODUCIBILITY_LEDGER.md present and non-empty; registry present.
"""
import json, re, sys, pathlib, xml.dom.minidom as minidom

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
COS = DOCS / "cosmology"
META = json.load(open(COS / "_meta.json", encoding="utf-8"))
DOI = META["doi"]
ORCID_HOST = "orcid.org/0009-0002-7535-8245"

BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot",
        "PerplexityBot", "ClaudeBot", "Google-Extended"]

results = []      # (level, name, ok, detail)   level in {HARD, SOFT}


def chk(name, ok, detail="", level="HARD"):
    results.append((level, name, bool(ok), detail))
    return bool(ok)


def wc(s):
    return len([w for w in re.split(r"\s+", s.strip()) if w])


def jsonlds(html):
    out = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',
                         html, re.S):
        try:
            out.append(json.loads(m.group(1)))
        except Exception as e:
            out.append({"__parse_error__": str(e)})
    return out


def first_block_is_answer(html):
    # the first element tag after </h1> (ignoring whitespace) must be the answer
    m = re.search(r"</h1>\s*(<[^>]+>)", html, re.S)
    return bool(m) and m.group(1).startswith('<p class="answer"')


# ----------------------------------------------------------------- per page
def check_pages():
    n = 0
    bad_ans = []
    bad_jsonld = []
    bad_first = []
    for c in META["chapters"]:
        p = COS / c["slug"] / "index.html"
        if not p.exists():
            chk(f"page exists: {c['slug']}", False)
            continue
        n += 1
        t = p.read_text(encoding="utf-8")

        m = re.search(r'<p class="answer">(.*?)</p>', t, re.S)
        words = wc(re.sub(r"<[^>]+>", " ", m.group(1))) if m else 0
        if not (m and 40 <= words <= 60):
            bad_ans.append(f"{c['slug']}({words})")
        if not first_block_is_answer(t):
            bad_first.append(c["slug"])

        jl = jsonlds(t)
        sa = next((d for d in jl if d.get("@type") == "ScholarlyArticle"), None)
        ok_sa = bool(sa) and \
            sa.get("isPartOf", {}).get("@type") == "CreativeWorkSeries" and \
            sa.get("isPartOf", {}).get("identifier") == DOI and \
            ORCID_HOST in json.dumps(sa.get("author", {})) and \
            bool(sa.get("identifier")) and bool(sa.get("datePublished")) and \
            bool(sa.get("dateModified")) and bool(sa.get("isBasedOn")) and \
            isinstance(sa.get("knowsAbout"), list) and len(sa["knowsAbout"]) >= 1
        has_crumb = any(d.get("@type") == "BreadcrumbList" for d in jl)
        if not (ok_sa and has_crumb):
            bad_jsonld.append(c["slug"])

    chk("pages: count == 28", n == 28, f"{n} pages")
    chk("pages: answer-first 40-60 words", not bad_ans,
        ("offenders: " + ", ".join(bad_ans)) if bad_ans else "all 28 in window")
    chk("pages: answer is first block after h1", not bad_first,
        ("offenders: " + ", ".join(bad_first)) if bad_first else "ok")
    chk("pages: 6-R.4 JSON-LD + BreadcrumbList", not bad_jsonld,
        ("offenders: " + ", ".join(bad_jsonld)) if bad_jsonld else "all valid")
    # vp-cards: structural — at least the honest ledger + appendix A carry cards
    cards_total = 0
    for c in META["chapters"]:
        p = COS / c["slug"] / "index.html"
        if p.exists():
            cards_total += p.read_text(encoding="utf-8").count('class="vp-card"')
    chk("pages: vp-cards present", cards_total > 0, f"{cards_total} cards across volume")


# --------------------------------------------------------------------- hub
def check_hub():
    t = (COS / "index.html").read_text(encoding="utf-8")
    jl = jsonlds(t)
    series = next((d for d in jl if d.get("@type") in ("CreativeWorkSeries", "Book")),
                  None)
    chk("hub: CreativeWorkSeries/Book + identifier==DOI",
        bool(series) and series.get("identifier") == DOI,
        series.get("@type") if series else "missing")
    chk("hub: standalone BreadcrumbList",
        any(d.get("@type") == "BreadcrumbList" for d in jl))
    chk("hub: no legacy CollectionPage", "CollectionPage" not in t)
    chk("hub: 5 Highwire citation tags",
        len(re.findall(r'name="citation_', t)) == 5,
        f'{len(re.findall(chr(34)+"citation_", t))} found')
    m = re.search(r'<p class="answer">(.*?)</p>', t, re.S)
    chk("hub: answer-first 40-60 words",
        bool(m) and 40 <= wc(re.sub(r"<[^>]+>", " ", m.group(1))) <= 60)


# ------------------------------------------------------------------- infra
def check_infra():
    rb = DOCS / "robots.txt"
    if chk("infra: robots.txt exists", rb.exists()):
        txt = rb.read_text(encoding="utf-8")
        miss = [b for b in BOTS if f"User-agent: {b}" not in txt]
        chk("infra: robots lists 7 bots", not miss,
            ("missing: " + ", ".join(miss)) if miss else "all 7")
        chk("infra: robots has Sitemap:", "Sitemap:" in txt)

    sm = DOCS / "sitemap.xml"
    if chk("infra: sitemap.xml exists", sm.exists()):
        try:
            minidom.parseString(sm.read_bytes())
            locs = len(re.findall(r"<loc>", sm.read_text(encoding="utf-8")))
            chk("infra: sitemap well-formed, 29 URLs", locs == 29, f"{locs} <loc>")
        except Exception as e:
            chk("infra: sitemap well-formed", False, str(e))

    lt = DOCS / "llms.txt"
    if chk("infra: llms.txt exists", lt.exists()):
        b = lt.read_bytes()
        txt = lt.read_text(encoding="utf-8")
        chk("infra: llms.txt < 5 KB", len(b) < 5120, f"{len(b)} bytes")
        chk("infra: llms.txt sectioned",
            all(h in txt for h in ("## Core", "## Research", "## Concepts", "## Policies")))
    chk("infra: llms-full.txt non-empty",
        (DOCS / "llms-full.txt").exists() and (DOCS / "llms-full.txt").stat().st_size > 0)


# ---------------------------------------------------------------- C1/C2/C3
def manifest_sums():
    import csv
    rows = list(csv.DictReader(open(ROOT / "manifest" / "cosmology.csv", encoding="utf-8")))
    s = {k: 0 for k in ("words", "eq_inline", "eq_display", "figures", "tables")}
    for r in rows:
        for k in s:
            s[k] += int(float(r[k]))
    return s


def check_constitution():
    s = manifest_sums()
    tot = META["totals"]
    ok = (tot["words"] == s["words"] and
          tot["eq"] == s["eq_inline"] + s["eq_display"] and
          tot["figures"] == s["figures"] and tot["tables"] == s["tables"])
    chk("C1: _meta totals == manifest sums", ok,
        f"meta(w={tot['words']},eq={tot['eq']}) vs "
        f"manifest(w={s['words']},eq={s['eq_inline']+s['eq_display']})")
    hub = (COS / "index.html").read_text(encoding="utf-8")
    chk("C1: hub overview agrees with totals",
        f"{tot['eq']} equations" in hub and f"{tot['words']} source words" in hub)

    # C2: no TeX/SSOT under docs/ (the published tree)
    tex = list(DOCS.rglob("*.tex")) + list(DOCS.rglob("*.txt"))
    tex = [p for p in tex if p.name not in ("robots.txt", "llms.txt", "llms-full.txt")]
    chk("C2: no .tex / SSOT text under docs/", not tex,
        ("found: " + ", ".join(str(p.relative_to(ROOT)) for p in tex)) if tex else "clean")

    led = ROOT / "IRREPRODUCIBILITY_LEDGER.md"
    chk("C3: ledger present + non-empty",
        led.exists() and led.stat().st_size > 200,
        f"{led.stat().st_size} bytes" if led.exists() else "missing")
    chk("C3: registry present",
        (ROOT / "registry" / "cross_volume_doi.csv").exists() and
        (ROOT / "registry" / "cross_volume_doi.md").exists())


# --------------------------------------------------------- soft: paragraphs
def check_paragraphs_soft():
    over = []
    for c in META["chapters"]:
        p = COS / c["slug"] / "index.html"
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        body = re.search(r"<main>(.*?)</main>", t, re.S)
        body = body.group(1) if body else t
        for m in re.finditer(r'<p(?:\s+class="(answer|abstract)")?[^>]*>(.*?)</p>',
                             body, re.S):
            cls, inner = m.group(1), re.sub(r"<[^>]+>", " ", m.group(2))
            inner = inner.strip()
            sents = len(re.findall(r"[.!?](?:\s|$)", inner))
            if sents > 3 and cls not in ("abstract",):
                over.append(f"{c['slug']}:{cls or 'p'}({sents})")
    chk("paragraphs <= 3 sentences (soft)", not over,
        (f"{len(over)} long paras (advisory)") if over else "ok", level="SOFT")


def main():
    check_pages()
    check_hub()
    check_infra()
    check_constitution()
    check_paragraphs_soft()

    hard = [r for r in results if r[0] == "HARD"]
    soft = [r for r in results if r[0] == "SOFT"]
    hard_fail = [r for r in hard if not r[2]]
    verdict = "PASS" if not hard_fail else "FAIL"

    report = {
        "spec": "VP_SPEC_v1_8",
        "phase": "v1_8",
        "paper": "cosmology",
        "verdict": verdict,
        "hard_total": len(hard),
        "hard_passed": len(hard) - len(hard_fail),
        "soft_warnings": [r[1] for r in soft if not r[2]],
        "checks": [
            {"level": lv, "name": nm, "ok": ok, "detail": dt}
            for (lv, nm, ok, dt) in results
        ],
    }
    rep = ROOT / "reports" / "phase-v1_8-cosmology.gate.json"
    rep.parent.mkdir(exist_ok=True)
    json.dump(report, open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"=== VP_SPEC v1.8 GATE: {verdict} "
          f"({report['hard_passed']}/{report['hard_total']} hard) ===")
    for lv, nm, ok, dt in results:
        tag = "ok " if ok else ("XX " if lv == "HARD" else "!! ")
        print(f"  [{tag}] {nm}" + (f"  — {dt}" if dt else ""))
    print(f"\nreport -> {rep.relative_to(ROOT)}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
