#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gate_volume.py — the HTML <-> code DRIFT-0 gate for the ear emergence volume (VP-SPEC v1.8 §C1).

It proves four things and writes docs/gate.json:

  1. NUMERIC determinism (2x):  vp_numeric_ssot.py, run as a fresh process twice, prints the
     same sha256 — and that sha equals the imported canonical_sha256().
  2. BUILD determinism / on-disk match:  re-running the deterministic builder in-memory
     reproduces every file on disk byte-for-byte (so docs/ cannot drift from the builder).
  3. DISPLAY drift 0:  every <span data-vp="KEY"> in every page has text == disp(KEY).
     This is the core anti-tuning invariant: no number on the page is hand-typed.
  4. STRUCTURE + no-omission:  each page carries its required scaffold (one h1, answer,
     abstract, claim-strip, firewall, canonical, the right JSON-LD @types); the full set of
     pages/assets is present; and every internal nav link resolves to a file on disk.

Run from the package root:   python3 volume/tools/gate_volume.py   -> prints  GATE: PASS|FAIL
Exit code 0 on PASS, 1 on FAIL.  No network.
"""
import os, sys, re, json, subprocess, hashlib
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.dirname(os.path.dirname(HERE))
DOCS = os.path.join(PKG, "docs")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PKG, "volume", "content"))

import vp_numeric_ssot as S
import chapters as C
import build_volume as B


# --------------------------------------------------------------------------------------------
class PageParser(HTMLParser):
    """Extracts the bits the gate checks: tag counts, class-tagged blocks, data-vp spans,
       canonical href, JSON-LD @types, and internal <a href> targets."""
    def __init__(self):
        super().__init__(convert_charrefs=True)   # entities decoded in handle_data
        self.tags = {}
        self.classes = {}            # class-combo -> count for blocks we care about
        self.h1 = 0
        self.canonical = None
        self.ld_types = []           # list of @type values seen across JSON-LD blocks
        self.vp = []                 # (key, text) pairs
        self.hrefs = []
        self._ld_depth = 0
        self._ld_buf = []
        self._vp_depth = 0
        self._vp_key = None
        self._vp_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag == "h1":
            self.h1 += 1
        cls = a.get("class", "")
        for token in ("answer", "abstract", "claim-strip", "firewall"):
            # match as a standalone class token
            if re.search(r"(?:^|\s)" + re.escape(token) + r"(?:\s|$)", cls):
                key = token
                self.classes[key] = self.classes.get(key, 0) + 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld_depth = 1
            self._ld_buf = []
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
        if tag == "span" and "data-vp" in a:
            self._vp_depth = 1
            self._vp_key = a["data-vp"]
            self._vp_text = []
        elif tag == "span" and self._vp_depth:
            self._vp_depth += 1

    def handle_endtag(self, tag):
        if tag == "script" and self._ld_depth:
            self._ld_depth = 0
            raw = "".join(self._ld_buf).strip()
            try:
                obj = json.loads(raw)
                t = obj.get("@type")
                if isinstance(t, list):
                    self.ld_types.extend(t)
                elif t:
                    self.ld_types.append(t)
            except Exception:
                self.ld_types.append("<<invalid-json>>")
        if tag == "span" and self._vp_depth:
            self._vp_depth -= 1
            if self._vp_depth == 0:
                self.vp.append((self._vp_key, "".join(self._vp_text)))
                self._vp_key = None

    def handle_data(self, data):
        if self._ld_depth:
            self._ld_buf.append(data)
        if self._vp_depth:
            self._vp_text.append(data)


# --------------------------------------------------------------------------------------------
def expected_outputs():
    """Rebuild the full {relpath: text} map in-memory (same order/content as build_volume.main)."""
    out = {}
    out["index.html"] = B.build_hub()
    for ch in C.CHAPTERS:
        out[f'{ch["slug"]}/index.html'] = B.build_chapter(ch)
    for con in C.CONCEPTS:
        out[f'concepts/{con["slug"]}/index.html'] = B.build_concept(con)
    page_segs = [[]] + [[ch["slug"]] for ch in C.CHAPTERS] + \
                [["concepts", c["slug"]] for c in C.CONCEPTS]
    out["assets/css/site.css"] = B.SITE_CSS
    out["sitemap.xml"] = B.sitemap_xml(page_segs)
    out["robots.txt"] = B.robots_txt()
    out["llms.txt"] = B.llms_txt()
    return out


def resolve_link(file_rel, href):
    """Resolve an internal href against the page's directory; return normalized docs-rel path."""
    base_dir = os.path.dirname(file_rel)
    # strip query/fragment
    href = href.split("#")[0].split("?")[0]
    joined = os.path.normpath(os.path.join(base_dir, href))
    return joined


def main():
    checks = []        # (name, ok, detail)
    def chk(name, ok, detail=""):
        checks.append((name, bool(ok), detail))
        return bool(ok)

    # ---- 1. numeric determinism (2x, fresh processes) --------------------------------------
    def run_ssot():
        r = subprocess.run([sys.executable, os.path.join("volume", "tools", "vp_numeric_ssot.py")],
                           cwd=PKG, capture_output=True, text=True)
        m = re.search(r"sha256:\s*([0-9a-f]{64})", r.stdout)
        return m.group(1) if m else None
    s1, s2 = run_ssot(), run_ssot()
    chk("ssot_2x_process_match", s1 is not None and s1 == s2, f"{s1} == {s2}")
    chk("ssot_matches_import", s1 == S.canonical_sha256(), f"{s1} == {S.canonical_sha256()}")

    # ---- 2. build determinism / on-disk byte match -----------------------------------------
    exp = expected_outputs()
    ondisk_ok, ondisk_bad = 0, []
    for rel, text in sorted(exp.items()):
        p = os.path.join(DOCS, rel)
        if not os.path.exists(p):
            ondisk_bad.append(rel + " (missing)"); continue
        with open(p, "r", encoding="utf-8") as f:
            disk = f.read()
        if disk == text:
            ondisk_ok += 1
        else:
            ondisk_bad.append(rel + " (byte-diff)")
    chk("build_on_disk_byte_match", not ondisk_bad,
        f"{ondisk_ok}/{len(exp)} match" + ("" if not ondisk_bad else f"; bad={ondisk_bad}"))

    # second in-memory rebuild must equal the first (determinism)
    exp2 = expected_outputs()
    chk("build_in_memory_deterministic", exp == exp2, f"{len(exp)} files")

    # ---- parse every HTML page -------------------------------------------------------------
    html_files = ["index.html"] + [f'{ch["slug"]}/index.html' for ch in C.CHAPTERS] + \
                 [f'concepts/{c["slug"]}/index.html' for c in C.CONCEPTS]
    parsed = {}
    for rel in html_files:
        p = os.path.join(DOCS, rel)
        with open(p, "r", encoding="utf-8") as f:
            src = f.read()
        pp = PageParser(); pp.feed(src); pp.close()
        parsed[rel] = pp

    # ---- 3. display drift 0 ----------------------------------------------------------------
    total_spans, drift = 0, []
    for rel, pp in parsed.items():
        for key, text in pp.vp:
            total_spans += 1
            try:
                want = S.disp(key)
            except KeyError:
                drift.append(f"{rel}: unknown key {key}"); continue
            if text != want:
                drift.append(f"{rel}: {key} HTML={text!r} != SSOT={want!r}")
    chk("display_drift_zero", not drift,
        f"{total_spans} data-vp spans, drift={len(drift)}" + ("" if not drift else f" :: {drift[:5]}"))
    chk("display_spans_present", total_spans > 0, f"{total_spans} spans")

    # ---- 4. structure per page -------------------------------------------------------------
    # chapters
    struct_bad = []
    for ch in C.CHAPTERS:
        rel = f'{ch["slug"]}/index.html'; pp = parsed[rel]
        need = []
        if pp.h1 != 1: need.append(f"h1={pp.h1}")
        if pp.classes.get("answer", 0) != 1: need.append("answer")
        if pp.classes.get("abstract", 0) != 1: need.append("abstract")
        if pp.classes.get("claim-strip", 0) != 1: need.append("claim-strip")
        if pp.classes.get("firewall", 0) != 1: need.append("firewall")
        if not pp.canonical or pp.canonical != B.canonical([ch["slug"]]):
            need.append(f"canonical={pp.canonical}")
        if "ScholarlyArticle" not in pp.ld_types: need.append("ld:ScholarlyArticle")
        if "BreadcrumbList" not in pp.ld_types: need.append("ld:BreadcrumbList")
        if need:
            struct_bad.append(f'{rel}: {need}')
    chk("chapter_structure", not struct_bad,
        f"{len(C.CHAPTERS)} chapters" + ("" if not struct_bad else f"; {struct_bad}"))

    # hub
    hub = parsed["index.html"]; hub_bad = []
    if hub.h1 != 1: hub_bad.append(f"h1={hub.h1}")
    if hub.canonical != B.canonical([]): hub_bad.append(f"canonical={hub.canonical}")
    if "CreativeWorkSeries" not in hub.ld_types: hub_bad.append("ld:CreativeWorkSeries")
    if "BreadcrumbList" not in hub.ld_types: hub_bad.append("ld:BreadcrumbList")
    if hub.classes.get("claim-strip", 0) != 1: hub_bad.append("claim-strip")
    chk("hub_structure", not hub_bad, "ok" if not hub_bad else str(hub_bad))

    # concepts
    con_bad = []
    for con in C.CONCEPTS:
        rel = f'concepts/{con["slug"]}/index.html'; pp = parsed[rel]
        need = []
        if pp.h1 != 1: need.append(f"h1={pp.h1}")
        if pp.canonical != B.canonical(["concepts", con["slug"]]): need.append(f"canonical={pp.canonical}")
        if "DefinedTerm" not in pp.ld_types: need.append("ld:DefinedTerm")
        if "BreadcrumbList" not in pp.ld_types: need.append("ld:BreadcrumbList")
        if need: con_bad.append(f"{rel}: {need}")
    chk("concept_structure", not con_bad,
        f"{len(C.CONCEPTS)} concepts" + ("" if not con_bad else f"; {con_bad}"))

    # ---- no-omission: all expected files present -------------------------------------------
    expected_files = set(exp.keys())
    missing = [r for r in expected_files if not os.path.exists(os.path.join(DOCS, r))]
    chk("no_omission_files", not missing,
        f"{len(expected_files)} expected" + ("" if not missing else f"; missing={missing}"))

    # ---- nav targets resolve ----------------------------------------------------------------
    link_bad, link_ok = [], 0
    for rel, pp in parsed.items():
        for href in pp.hrefs:
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = resolve_link(rel, href)
            if os.path.exists(os.path.join(DOCS, target)):
                link_ok += 1
            else:
                link_bad.append(f"{rel} -> {href} (={target})")
    chk("internal_links_resolve", not link_bad,
        f"{link_ok} internal links ok" + ("" if not link_bad else f"; bad={link_bad[:5]}"))

    # ---- verdict ----------------------------------------------------------------------------
    all_ok = all(ok for _, ok, _ in checks)

    report = {
        "gate": "PASS" if all_ok else "FAIL",
        "spec": "VP-SPEC v1.8 §C1 (HTML<->code drift 0)",
        "volume": C.META["volume"],
        "version": C.META["package_version"],
        "ssot_sha256": S.canonical_sha256(),
        "facts": len(S.facts()),
        "pages": len(html_files),
        "files": len(exp),
        "data_vp_spans": total_spans,
        "checks": [{"name": n, "ok": ok, "detail": d} for n, ok, d in checks],
    }
    # deterministic report (sorted keys, no timestamp)
    with open(os.path.join(DOCS, "gate.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write("\n")

    width = max(len(n) for n, _, _ in checks)
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n.ljust(width)}  {d}")
    print(f"\nGATE: {'PASS' if all_ok else 'FAIL'}  "
          f"({total_spans} numbers drift-0, {len(html_files)} pages, ssot {S.canonical_sha256()[:12]})")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
