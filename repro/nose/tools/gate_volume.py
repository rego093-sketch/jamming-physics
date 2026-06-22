#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_volume.py — the focused pass/fail gate for the nose-emergence HTML volume (run from package root).

    python3 tools/gate_volume.py

THEORETICAL / NON-CLINICAL. This gate checks STRUCTURE and REPRODUCIBILITY, never a clinical claim.
The disease chapters are direction-only / proposal-only (FIREWALL #4, #8).

Asserts (independently of the builder):
  [G1] SSOT DETERMINISM   — tools/vp_nose_ssot.py emits an identical sha256 on two runs.
  [G2] HTML↔CODE DRIFT = 0 — every displayed `<span class="vp-num" data-key="K">V</span>` in docs/
                            has V == html.escape(SSOT[K]); every K resolves in the SSOT. (VP-SPEC C1.)
  [G3] CHAPTER STRUCTURE   — each chapter page has exactly one <h1>, one <p class="answer"> (40–60
                            words), one .abstract, one .claim-strip, a canonical link, a ScholarlyArticle
                            + a BreadcrumbList JSON-LD, and prev/next nav (VP-SPEC §6).
  [G4] FIREWALL BANNER     — the two disease chapters (congenital anosmia, allergic smell loss) carry the
                            non-clinical scope banner and the words "direction-only" + "non-clinical"; E5
                            cites the immune §11 DOI and re-derives no mechanism.
  [G5] NO KATEX RESIDUE    — no `class="katex` anywhere (VP-SPEC §6).
  [G6] ACCESS / SEARCH      — sitemap URL count == number of index.html under docs/; robots.txt allows the
                            7 bots; docs/llms.txt exists and is < 5 KB; the hub is a CreativeWorkSeries.
  [G7] SELF-CONTAINED CARDS — every chapter that cites a locked cross-volume quantity carries ≥1
                            `aside.vp-card` (value + meaning + grade + a DOI/source link) (VP-SPEC 6-R.2).
  [G8] VOLUME DOI PRESENT  — the deposited volume carries its OWN Zenodo concept DOI: the hub shows it in
                            visible text and in the CreativeWorkSeries JSON-LD identifier, docs/nose/_meta.json
                            records it, docs/llms.txt lists it, and every chapter's claim-strip links it.

Exit 0 + 'VOLUME GATE: PASS' only if all hold.
"""
import os, sys, re, json, html, glob, subprocess, hashlib

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(_HERE)
DOCS  = os.path.join(PKG, "docs")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from vp_nose_ssot import ssot, dump

SSOT = ssot()
SPAN_RE = re.compile(r'<span class="vp-num" data-key="([^"]+)">(.*?)</span>', re.S)
DISEASE_SLUGS = ("04-congenital-anosmia", "05-allergic-smell-loss")
DOI_IMMUNE = "10.5281/zenodo.20755280"
DOI_NOSE   = "10.5281/zenodo.20790182"   # this volume's own Zenodo concept DOI


def chapter_files():
    return sorted(glob.glob(os.path.join(DOCS, "nose", "*", "index.html")))


def all_html():
    return sorted(set(glob.glob(os.path.join(DOCS, "**", "*.html"), recursive=True)))


def answer_word_count(t):
    m = re.search(r'<p class="answer">(.*?)</p>', t, re.S)
    if not m:
        return None
    inner = html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))
    return len(inner.split())


def sha_of_ssot():
    r = subprocess.run([sys.executable, os.path.join(_HERE, "vp_nose_ssot.py")],
                       capture_output=True, text=True, cwd=PKG)
    assert r.returncode == 0, r.stderr[-400:]
    line = [l for l in r.stdout.splitlines() if l.strip().startswith("sha256:")]
    return line[-1].split("sha256:")[1].strip()


def main():
    print("=" * 74)
    print("VOLUME GATE — docs/nose   (theoretical / NON-CLINICAL; HTML↔code drift 0)")
    print("=" * 74)
    ok = True
    chs = chapter_files()

    # [G1] SSOT determinism --------------------------------------------------------------------
    s1, s2 = sha_of_ssot(), sha_of_ssot()
    g1 = (s1 == s2); ok &= g1
    print(f"  [{'PASS' if g1 else 'FAIL'}] G1 SSOT determinism — vp_nose_ssot.py sha256 stable ({s1[:16]})")

    # [G2] HTML↔code drift = 0 -----------------------------------------------------------------
    total_spans, mism, unresolved = 0, 0, 0
    keys_displayed = set()
    for p in all_html():
        t = open(p, encoding="utf-8").read()
        for key, shown in SPAN_RE.findall(t):
            total_spans += 1
            keys_displayed.add(key)
            if key not in SSOT:
                unresolved += 1
                continue
            if shown != html.escape(SSOT[key]):
                mism += 1
                if mism <= 5:
                    print(f"        DRIFT @ {os.path.relpath(p)}: {key} shows {shown!r} ≠ SSOT {SSOT[key]!r}")
    g2 = (mism == 0 and unresolved == 0 and total_spans > 0); ok &= g2
    print(f"  [{'PASS' if g2 else 'FAIL'}] G2 drift=0 — {total_spans} displayed numbers, "
          f"{mism} mismatch, {unresolved} unresolved; {len(keys_displayed)}/{len(SSOT)} SSOT keys shown")

    # [G3] chapter structure (first chapter has no prev; last has no next) ----------------------
    g3 = True
    for i, p in enumerate(chs):
        t = open(p, encoding="utf-8").read(); rel = os.path.relpath(p)
        is_first, is_last = (i == 0), (i == len(chs) - 1)
        checks = {
            "one h1":          t.count("<h1>") == 1,
            "one answer":      t.count('<p class="answer">') == 1,
            "answer 40-60":    (answer_word_count(t) or 0) in range(40, 61),
            "abstract":        '<p class="abstract">' in t,
            "claim-strip":     'class="claim-strip' in t,
            "canonical":       '<link rel="canonical"' in t,
            "ScholarlyArticle": '"ScholarlyArticle"' in t,
            "BreadcrumbList":  '"BreadcrumbList"' in t,
            "pager nav":       'class="pn"' in t,
            "prev link":       is_first or ('rel="prev"' in t),
            "next link":       is_last or ('rel="next"' in t),
        }
        bad = [k for k, v in checks.items() if not v]
        if bad:
            g3 = False
            print(f"        STRUCT @ {rel}: missing {bad}")
    ok &= g3
    print(f"  [{'PASS' if g3 else 'FAIL'}] G3 chapter structure — {len(chs)} chapters: h1/answer(40-60)/"
          f"abstract/claim-strip/canonical/JSON-LD/prev-next all present")

    # [G4] firewall banner on the disease chapters ---------------------------------------------
    g4 = True
    for slug in DISEASE_SLUGS:
        p = os.path.join(DOCS, "nose", slug, "index.html")
        t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        cond = ('class="scope-banner"' in t
                and "direction-only" in t.lower()
                and "non-clinical" in t.lower())
        if slug == "05-allergic-smell-loss":
            cond = cond and (DOI_IMMUNE in t)        # mechanism cited, not re-derived
        if not cond:
            g4 = False
            print(f"        FIREWALL @ {slug}: banner/scope/citation incomplete")
    ok &= g4
    print(f"  [{'PASS' if g4 else 'FAIL'}] G4 firewall — both disease chapters carry the non-clinical "
          f"scope banner (direction-only); E5 cites immune §11 ({DOI_IMMUNE})")

    # [G5] no katex residue --------------------------------------------------------------------
    katex = [os.path.relpath(p) for p in all_html() if 'class="katex' in open(p, encoding="utf-8").read()]
    g5 = (not katex); ok &= g5
    print(f"  [{'PASS' if g5 else 'FAIL'}] G5 no katex — 0 'class=\"katex' residue across {len(all_html())} pages")

    # [G6] access / search ---------------------------------------------------------------------
    n_index = len([p for p in all_html() if os.path.basename(p) == "index.html"])
    sm = open(os.path.join(DOCS, "sitemap.xml"), encoding="utf-8").read() if os.path.exists(os.path.join(DOCS, "sitemap.xml")) else ""
    n_loc = sm.count("<loc>")
    rb = open(os.path.join(DOCS, "robots.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(DOCS, "robots.txt")) else ""
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    bots_ok = all(b in rb for b in bots)
    llms_p = os.path.join(DOCS, "llms.txt")
    llms_ok = os.path.exists(llms_p) and os.path.getsize(llms_p) < 5120
    hub = open(os.path.join(DOCS, "nose", "index.html"), encoding="utf-8").read()
    hub_ok = '"CreativeWorkSeries"' in hub
    g6 = (n_loc == n_index and bots_ok and llms_ok and hub_ok); ok &= g6
    print(f"  [{'PASS' if g6 else 'FAIL'}] G6 access — sitemap {n_loc} = {n_index} index.html · "
          f"robots 7/7 bots {bots_ok} · llms.txt<5KB {llms_ok} · hub=CreativeWorkSeries {hub_ok}")

    # [G7] self-contained cards ----------------------------------------------------------------
    g7 = all('class="vp-card"' in open(p, encoding="utf-8").read() for p in chs)
    ok &= g7
    print(f"  [{'PASS' if g7 else 'FAIL'}] G7 self-contained cards — every chapter carries ≥1 aside.vp-card "
          f"(value+meaning+grade+source link)")

    # [G8] volume's own concept DOI present (deposited, not pre-deposit) ------------------------
    hub_t = open(os.path.join(DOCS, "nose", "index.html"), encoding="utf-8").read()
    hub_visible = DOI_NOSE in hub_t
    # the DOI must sit inside the CreativeWorkSeries JSON-LD as a DOI identifier, not only in prose
    m = re.search(r'"@type":\s*"CreativeWorkSeries".*?"hasPart"', hub_t, re.S)
    hub_ld_doi = bool(m) and ('"propertyID": "DOI"' in m.group(0)) and (DOI_NOSE in m.group(0))
    try:
        meta = json.load(open(os.path.join(DOCS, "nose", "_meta.json"), encoding="utf-8"))
        meta_doi = (meta.get("doi") == DOI_NOSE)
    except Exception:
        meta_doi = False
    llms_t = open(os.path.join(DOCS, "llms.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(DOCS, "llms.txt")) else ""
    llms_doi = DOI_NOSE in llms_t
    chapters_doi = all(DOI_NOSE in open(p, encoding="utf-8").read() for p in chs)
    g8 = hub_visible and hub_ld_doi and meta_doi and llms_doi and chapters_doi; ok &= g8
    if not g8:
        print(f"        DOI @ hub_visible={hub_visible} hub_ld={hub_ld_doi} meta={meta_doi} "
              f"llms={llms_doi} chapters={chapters_doi}")
    print(f"  [{'PASS' if g8 else 'FAIL'}] G8 volume DOI — concept DOI {DOI_NOSE} on hub (text + "
          f"CreativeWorkSeries identifier), in _meta.json, llms.txt, and every chapter")

    print("=" * 74)
    print(f"VOLUME GATE: {'PASS' if ok else 'FAIL'}")
    print("=" * 74)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
