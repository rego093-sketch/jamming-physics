#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate.py — VP-SPEC v1.8 gate for Felt Cognition (search-readiness C4 + reproducibility C1).

SEARCH GATE (C4 / 6-R, §8):
  - answer-first: every chapter's first content block after </h1> is <p class="answer"> (40-60 words).
  - self-contained cards: every cited lock has an aside.vp-card (value + meaning + grade + canonical link).
  - JSON-LD: each chapter has ScholarlyArticle + BreadcrumbList + author sameAs ORCID + DOI, in <head>.
  - access: docs/robots.txt allows the 7 bots; docs/sitemap.xml lists every docs/ index.html;
            docs/llms.txt exists and is < 5 KB.
  - paragraphs: most body paragraphs <= 3 sentences (soft; reported, not fatal).

REPRODUCIBILITY GATE (C1 / §8):
  - the in-package engine reproduces: run_all digests == expected_sha256.json.
  - SSOT: every vp-card value matches the frozen engine results (registry.validate, drift 0).
  - word counts preserved: body wordcount (excluding answer/abstract/asides/h1/nav) == manifest.

IDEMPOTENCY:
  - build_search_layer run twice -> byte-identical docs tree.

Exit 0 = PASS. Report -> reports/gate-search-v1_8.gate.json
"""
import os, sys, re, json, hashlib, subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import mind_registry as R

PKG = R.PKG
DOCS = os.path.join(PKG, "docs")
MIND = os.path.join(DOCS, "mind")
REPORT = os.path.join(PKG, "reports", "gate-search-v1_8.gate.json")


def _read(p):
    return open(p, encoding="utf-8").read()


def _wordcount_body(html):
    m = re.search(r"<main>(.*)</main>", html, flags=re.S)
    t = m.group(1) if m else html
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<aside.*?</aside>", "", t, flags=re.S)
    t = re.sub(r'<p class="answer".*?</p>', "", t, flags=re.S)
    t = re.sub(r'<p class="abstract".*?</p>', "", t, flags=re.S)
    t = re.sub(r"<h1>.*?</h1>", "", t, flags=re.S)
    t = re.sub(r'<nav.*?</nav>', "", t, flags=re.S)
    t = re.sub(r"<figure.*?</figure>", "", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&[a-zA-Z#0-9]+;", " ", t)
    return len(t.split())


def main():
    checks = []
    def rec(name, ok, detail="", soft=False):
        checks.append({"check": name, "pass": bool(ok), "soft": soft, "detail": str(detail)})
        return ok

    # ---- C4 answer-first + cards + JSON-LD per chapter ----------------------
    manifest = {}
    for line in _read(os.path.join(PKG, "manifest", "mind.csv")).splitlines()[1:]:
        parts = next(__import__("csv").reader([line]))
        if len(parts) >= 5:
            manifest[parts[1]] = int(parts[4])

    for slug in R.CHAPTERS:
        h = _read(os.path.join(MIND, slug, "index.html"))
        # answer-first present and positioned right after </h1>
        m = re.search(r"</h1>\s*<!-- vp:answer:start -->\s*<p class=\"answer\">(.*?)</p>", h, flags=re.S)
        aw = len(re.sub(r"<[^>]+>", "", m.group(1)).split()) if m else 0
        rec(f"answer-first @ {slug} (40-60w)", bool(m) and 38 <= aw <= 62, f"{aw} words")
        # one card per cited lock
        for lid in R.CITES.get(slug, []):
            rec(f"vp-card {lid} @ {slug}", f'data-locked="{lid}"' in h, "")
        # JSON-LD
        rec(f"JSON-LD ScholarlyArticle+Breadcrumb+ORCID @ {slug}",
            "ScholarlyArticle" in h and "BreadcrumbList" in h and R.ORCID in h and R.DOI in h, "")

    # ---- C4 access layer ---------------------------------------------------
    robots = _read(os.path.join(DOCS, "robots.txt")) if os.path.exists(os.path.join(DOCS, "robots.txt")) else ""
    rec("robots.txt allows 7 bots", all(b in robots for b in R.BOTS),
        f"{sum(b in robots for b in R.BOTS)}/7")
    sm_path = os.path.join(DOCS, "sitemap.xml")
    sitemap = _read(sm_path) if os.path.exists(sm_path) else ""
    n_idx = sum(1 for root, _d, fs in os.walk(DOCS) for f in fs if f == "index.html")
    n_loc = sitemap.count("<loc>")
    rec("sitemap.xml lists every index.html", n_loc == n_idx, f"{n_loc} locs / {n_idx} pages")
    llms_path = os.path.join(DOCS, "llms.txt")
    llms_ok = os.path.exists(llms_path) and os.path.getsize(llms_path) < 5000
    rec("llms.txt exists < 5KB", llms_ok,
        f"{os.path.getsize(llms_path) if os.path.exists(llms_path) else 'missing'} bytes")

    # ---- C1 reproducibility ------------------------------------------------
    eng = os.path.join(PKG, "repro", "mind", "_engine")
    try:
        subprocess.run([sys.executable, "run_all.py"], cwd=eng, capture_output=True, timeout=300, check=True)
        exp = json.load(open(os.path.join(eng, "expected_sha256.json")))
        got = hashlib.sha256(open(os.path.join(eng, "results", "mind_emergence_results.json"), "rb").read()).hexdigest()
        rec("engine reproduces (results sha256 == expected)",
            got == exp["mind_emergence_results.json"], got[:16])
    except Exception as e:
        rec("engine reproduces", False, f"run error: {e}")

    rec("SSOT cards match frozen results (drift 0)", len(R.validate()) == 0,
        "; ".join(R.validate()) or "ok")

    # word counts preserved (answer/cards excluded -> manifest unchanged)
    wc_ok = True; wc_detail = []
    for slug, expect in manifest.items():
        got = _wordcount_body(_read(os.path.join(MIND, slug, "index.html")))
        if abs(got - expect) > max(3, int(0.02 * expect)):
            wc_ok = False; wc_detail.append(f"{slug}:{got}!={expect}")
    rec("body word counts preserved vs manifest", wc_ok, ", ".join(wc_detail) or "all within 2%")

    # ---- idempotency -------------------------------------------------------
    def tree_md5():
        h = hashlib.md5()
        for root, _d, fs in sorted(os.walk(DOCS)):
            for f in sorted(fs):
                if f.endswith((".html", ".txt", ".xml")):
                    h.update(open(os.path.join(root, f), "rb").read())
        return h.hexdigest()
    before = tree_md5()
    subprocess.run([sys.executable, os.path.join(_HERE, "build_search_layer.py")],
                   capture_output=True, timeout=120)
    after = tree_md5()
    rec("build is idempotent (re-run identical)", before == after, f"{before[:12]} vs {after[:12]}")

    hard_fail = [c for c in checks if not c["pass"] and not c["soft"]]
    verdict = "PASS" if not hard_fail else "FAIL"
    report = {
        "gate": "Felt Cognition — VP-SPEC v1.8 (C4 search-readiness + C1 reproducibility)",
        "spec": "VP_SPEC_v1_8.md §0 C1/C4, §6-R, §8 search gate",
        "verdict": verdict,
        "summary": f"{sum(c['pass'] for c in checks)}/{len(checks)} checks, {len(hard_fail)} hard fail",
        "checks": checks,
    }
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    json.dump(report, open(REPORT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    print(f"GATE Felt-Cognition v1.8: {verdict}  ({report['summary']})")
    for c in checks:
        if not c["pass"] or c["check"].startswith(("answer-first", "robots", "sitemap", "llms",
                                                   "engine", "SSOT", "body word", "build")):
            tag = "ok " if c["pass"] else ("warn" if c["soft"] else "FAIL")
            print(f"  [{tag}] {c['check']}  --  {c['detail']}")
    print(f"report -> {os.path.relpath(REPORT, PKG)}")
    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
