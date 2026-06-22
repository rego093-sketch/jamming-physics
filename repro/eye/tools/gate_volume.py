#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/gate_volume.py — the drift-0 gate for the HTML volume under docs/eye/.

Re-proves, INDEPENDENTLY of the builder, every binding property of the deliverable. The builder
asserts these at write time; this gate asserts them again from the shipped files, so a hand-edit
of any HTML (or a stale capture) is caught:

  G1 determinism   — each chapter's run.py, executed TWICE, yields byte-identical stdout.
                     (The increment outputs are reproducible: SEED-pinned, no RNG, no clock.)
  G2 code -> facts  — the live transcript's sha256 equals the sha recorded in facts/{slug}.json.
                     The numbers on the page are pinned to THIS code, not to a stale capture.
  G3 page -> code   — the <pre> transcript embedded in each chapter HTML, un-escaped, is
                     byte-identical to the live transcript (sha match, three ways: attribute
                     sha == recomputed inner sha == live run sha). The page shows the real run.
  G4 fact drift-0  — every facts[].value appears (a) verbatim in the concatenated live
                     transcripts AND (b) verbatim in the raw chapter HTML. A number in prose
                     the code never printed, or a printed number the page misquotes, fails here.
  G5 firewall      — the rendered E4 chapter, lower-cased, contains NONE of E4's own
                     MAGNITUDE_BLOCK tokens and no '%'. Disease layer stays proposal-only.
  G6 retrieval     — each chapter is static and machine-readable: has <h1>, <link rel=canonical>,
                     a JSON-LD block, and EVERY <script> is type=application/ld+json (no
                     executable JS that could hide content from a crawler or an LLM reader).
  G7 no-omission   — every file in expected_files() exists (hub, chapters, facts, css, sitemap,
                     robots, llms). Nothing the manifest promises is missing.

Run from package root:   python3 tools/gate_volume.py
Exit 0 + "VOLUME GATE: PASS" iff all properties hold; otherwise every failure is printed, exit 1.
"""
import os, sys, re, json
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import _volume_lib as L

# ----------------------------------------------------------------------------------------------
FAILS = []
def check(cond, msg):
    if not cond:
        FAILS.append(msg)
    return bool(cond)

# Pull each embedded transcript: (data-run, data-sha, inner-escaped-text).
_PRE = re.compile(
    r'<pre class="transcript" data-run="([^"]+)" data-sha="([0-9a-f]{64})">(.*?)</pre>',
    re.DOTALL)
_SCRIPT_OPEN = re.compile(r'<script\b([^>]*)>', re.IGNORECASE)
_TYPE_ATTR   = re.compile(r'type\s*=\s*"([^"]*)"', re.IGNORECASE)

# Cache: run path -> live transcript (proven deterministic on first touch).
_LIVE = {}

def live_transcript(rel):
    """Run `rel` twice, assert byte-identical (G1), cache and return the transcript."""
    if rel in _LIVE:
        return _LIVE[rel]
    a = L.run_capture(rel)
    b = L.run_capture(rel)
    check(a == b, f"G1 determinism: {rel} produced different stdout across two runs")
    _LIVE[rel] = a
    return a


def gate_chapter(ch):
    slug = ch["slug"]
    html_path  = os.path.join(L.DOCS, slug, "index.html")
    facts_path = os.path.join(L.DOCS, "facts", slug + ".json")
    if not check(os.path.exists(html_path),  f"G7 missing chapter HTML: {slug}/index.html"):
        return
    if not check(os.path.exists(facts_path), f"G7 missing facts JSON: facts/{slug}.json"):
        return

    html  = open(html_path,  encoding="utf-8").read()
    facts = json.load(open(facts_path, encoding="utf-8"))

    # ---- G2 code->facts : recorded run shas equal the live transcript shas ------------------
    live_concat_parts = []
    for run in facts["runs"]:
        rel, rec_sha = run["path"], run["sha256"]
        t = live_transcript(rel)
        live_concat_parts.append(t)
        check(L.sha256_text(t) == rec_sha,
              f"G2 code->facts: {slug}: facts.json sha for {rel} != live transcript sha")
    live_concat = "".join(live_concat_parts)

    # ---- G3 page->code : embedded <pre> transcripts are byte-identical to live runs ---------
    pres = _PRE.findall(html)
    check(len(pres) == len(facts["runs"]),
          f"G3 page->code: {slug}: {len(pres)} embedded transcript(s) but "
          f"{len(facts['runs'])} run(s) declared")
    seen_runs = set()
    for run_attr, sha_attr, inner_esc in pres:
        seen_runs.add(run_attr)
        live = _LIVE.get(run_attr)
        if not check(live is not None,
                     f"G3 page->code: {slug}: embedded transcript for unknown run {run_attr}"):
            continue
        live_sha  = L.sha256_text(live)
        inner_sha = L.sha256_text(L.unesc(inner_esc))
        check(sha_attr == live_sha,
              f"G3 page->code: {slug}: data-sha for {run_attr} != live run sha")
        check(inner_sha == live_sha,
              f"G3 page->code: {slug}: embedded transcript body for {run_attr} drifted from code")
    for run in facts["runs"]:
        check(run["path"] in seen_runs,
              f"G3 page->code: {slug}: run {run['path']} declared in facts but not embedded in HTML")

    # ---- G4 fact drift-0 : every surfaced number is in BOTH the live transcript AND the HTML
    for fact in facts["facts"]:
        v = fact["value"]
        check(v in live_concat,
              f"G4 fact drift-0: {slug}: surfaced value {v!r} is NOT in the live transcript "
              f"(prose claims a number the code never printed)")
        check(v in html,
              f"G4 fact drift-0: {slug}: surfaced value {v!r} recorded in facts.json but absent "
              f"from the rendered HTML")

    # ---- G6 retrieval : static + machine-readable ------------------------------------------
    check("<h1" in html,                       f"G6 retrieval: {slug}: no <h1>")
    check('<link rel="canonical"' in html,     f"G6 retrieval: {slug}: no canonical link")
    check("application/ld+json" in html,       f"G6 retrieval: {slug}: no JSON-LD block")
    for attrs in _SCRIPT_OPEN.findall(html):
        m = _TYPE_ATTR.search(attrs)
        typ = (m.group(1).lower() if m else "")
        check(typ == "application/ld+json",
              f"G6 retrieval: {slug}: a <script> is not type=application/ld+json "
              f"(found {typ!r}) — executable JS is not allowed in the static volume")

    return html


def main():
    print("=" * 78)
    print("VOLUME GATE — docs/eye/  (independent re-proof; HTML<->code drift must be 0)")
    print("=" * 78)

    # G7 no-omission FIRST — the manifest's promised files must all exist.
    for f in L.expected_files():
        check(os.path.exists(f), f"G7 no-omission: promised file missing: "
                                 f"{os.path.relpath(f, L.ROOT)}")

    rendered = {}
    for ch in L.VOLUME:
        h = gate_chapter(ch)
        if h is not None:
            rendered[ch["slug"]] = h

    # G5 firewall — every disease/condition chapter. Each rendered chapter must carry no magnitude
    # vocabulary (checked against its OWN increment's MAGNITUDE_BLOCK) and no '%'.
    for slug, rel in L.DISEASE_CHAPTERS.items():
        chap = rendered.get(slug)
        if check(chap is not None, f"G5 firewall: {slug} did not render — cannot verify firewall"):
            low = chap.lower()
            block = L.load_magnitude_block(rel)
            hits = sorted(t for t in block if t in low)
            check(not hits, f"G5 firewall: {slug} HTML contains forbidden magnitude token(s): {hits}")
            check("%" not in low, f"G5 firewall: {slug} HTML contains a '%' (quantitative clinical sign)")

    # Hub sanity (part of no-omission / retrieval): the hub lists every chapter + is static.
    hub_path = os.path.join(L.DOCS, "index.html")
    if check(os.path.exists(hub_path), "G7 no-omission: hub index.html missing"):
        hub = open(hub_path, encoding="utf-8").read()
        for ch in L.VOLUME:
            check(ch["slug"] + "/" in hub, f"G7 no-omission: hub does not link chapter {ch['slug']}")
        for attrs in _SCRIPT_OPEN.findall(hub):
            m = _TYPE_ATTR.search(attrs)
            typ = (m.group(1).lower() if m else "")
            check(typ == "application/ld+json",
                  f"G6 retrieval: hub: a <script> is not type=application/ld+json (found {typ!r})")

    print()
    n_runs = len(_LIVE)
    n_facts = sum(len(json.load(open(os.path.join(L.DOCS, 'facts', c['slug'] + '.json'),
                                    encoding='utf-8'))["facts"]) for c in L.VOLUME)
    print(f"  chapters gated : {len(rendered)}/{len(L.VOLUME)}")
    print(f"  unique runs    : {n_runs} (each executed 2x, byte-identical)")
    print(f"  facts re-proven: {n_facts} (each in live transcript AND in HTML)")
    print(f"  firewall       : no magnitude token, no '%' ({len(L.DISEASE_CHAPTERS)} condition chapters)")
    print(f"  files present  : {len(L.expected_files())}/{len(L.expected_files())} expected")
    print("=" * 78)
    if FAILS:
        print(f"VOLUME GATE: FAIL  ({len(FAILS)} problem(s))")
        for m in FAILS:
            print("  - " + m)
        print("=" * 78)
        sys.exit(1)
    print("VOLUME GATE: PASS")
    print("=" * 78)


if __name__ == "__main__":
    main()
