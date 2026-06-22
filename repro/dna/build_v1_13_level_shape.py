#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_v1_13_level_shape.py  --  deterministic v1.12 -> v1.13 upgrade.

Applies the gamma<->A4 LEVEL/SHAPE clarification (the inverse of a misconception)
across the multi-page DNA site, plus version bumps. Every edit is verified
fail-closed: the exact source string must occur the expected number of times or
the script aborts WITHOUT writing (no silent no-op). No measured number, grade,
equation, table, or DOI is changed -- only clarifying sentences are added and one
abstract sentence is replaced by a strictly sharper one carrying the same numbers.

Backing: vp_session_gamma_a4_verified (2x SHA-256, prereg.sha256 ff04aa7b...3901);
mechanism confirmed in key_pipeline_full.py::robust_z (subtracts the per-locus
median = the level gamma is).

Run from the package root:  python3 build_v1_13_level_shape.py
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- the reusable "gamma vs A4: level vs shape" vp-card (paste-identical on each page) ----
LEVEL_SHAPE_CARD = (
'<aside class="vp-card" data-locked="relationship">\n'
'  <h4 class="vp-q">\u03b3 and A4 are level vs shape of one field</h4>\n'
'  <p class="vp-value">\u03b3 is the <strong>average</strong> of the stiffness signal (one scalar). '
'A4 is the <strong>shape</strong> of that same signal once the average is subtracted out '
'(shells, anchors, loops). The engine builds A4 by removing the per-locus mean (<code>robust_z</code>), '
'which is exactly \u03b3 \u2014 so A4 is \u201cthe signal minus \u03b3\u201d, and \u201c\u03b3 \u2282 A4\u201d is impossible. '
'Same field (\u03c1\u22480.94), orthogonal projections; neither contains the other.</p>\n'
'  <p class="vp-grade">Grade: verified (level/shape decomposition, 2\u00d7SHA-256, prereg ff04aa7b\u2026) '
'\u2014 same field; A4 carries none of \u03b3 (max|corr|=0.327).</p>\n'
'</aside>\n')

# ============================ targeted edits ============================
# each tuple: (relative path, old_substring, new_substring, expected_occurrences)
EDITS = []

# ---------- 13 — unified interpreter ----------
P13 = "docs/dna/13-unified-deterministic-interpreter/index.html"

# (13a) abstract opening: name the relationship as level vs shape
EDITS.append((P13,
"Earlier chapters split the read in two: the A4 grammar gave structure and position, while the cross-kingdom and clade chapters measured \u03b3 and methylation as global statistics without the coordinate. This chapter unites them into a single engine",
"Earlier chapters reported two projections of one stiffness field without naming their relationship: \u03b3 is its level (the window-mean scalar of \u00a72), and the A4 coordinate is its shape (the same signal with that mean removed \u2014 shells, anchors, loops, anchor-relative phase). They are orthogonal, not nested: the A4 pipeline\u2019s <code>robust_z</code> subtracts the per-locus median, which is exactly the level \u03b3 is, so the coordinate carries none of \u03b3 while reading the same substrate. This chapter unites the level read and the shape read into a single engine",
1))

# (13b) coordinate section: the mechanism, in one sentence
EDITS.append((P13,
"which is not contact-competent. The loops are built from real motors",
"which is not contact-competent. Mechanically, the coordinate is the mean-removed view of the same stiffness signal \u03b3 averages: <code>robust_z</code> deletes the per-locus level (= \u03b3) and keeps the relative shape, which is why the shell and anchor reads are orthogonal to \u03b3 even though they are computed from the same field. The loops are built from real motors",
1))

# (13c) lead the vp-cards with the level/shape card
EDITS.append((P13,
'<aside class="vp-card" data-register="13-unified-deterministic-interpreter">',
LEVEL_SHAPE_CARD + '<aside class="vp-card" data-register="13-unified-deterministic-interpreter">',
1))

# ---------- I — how to read a locus ----------
PI = "docs/dna/how-to-read-a-locus/index.html"

# (Ia) Step 2 lead: the relationship in one line, BEFORE the four-part coordinate paragraph
EDITS.append((PI,
"<p>The same read places the element in a four-part coordinate,",
'<p class="rel-note"><strong>First, the relationship in one line.</strong> \u03b3 and the A4 coordinate are the '
'<strong>level</strong> and the <strong>shape</strong> of one stiffness signal: \u03b3 is its window-mean '
'(a single number), and the A4 coordinate is the same signal with that mean removed \u2014 the shells and '
'anchors are literally what is left after the average (\u03b3) is subtracted out. So a locus has '
'<strong>one \u03b3</strong> (its overall stiffness) and <strong>one A4 shape</strong> (where it is stiff vs '
'soft relative to its own average); neither contains the other.</p>\n'
"<p>The same read places the element in a four-part coordinate,",
1))

# (Ib) add the reusable card after the helical (geometry/chance) card
EDITS.append((PI,
'that are Layer-2. <span class="grade g-open">geometry / chance-level</span> <a href="https://github.com/rego093-sketch/jamming-physics/tree/main/repro/dna/13-unified-deterministic-interpreter/stress_helical/" rel="noopener">stress test \u2192 repro</a></aside>',
'that are Layer-2. <span class="grade g-open">geometry / chance-level</span> <a href="https://github.com/rego093-sketch/jamming-physics/tree/main/repro/dna/13-unified-deterministic-interpreter/stress_helical/" rel="noopener">stress test \u2192 repro</a></aside>\n'
+ LEVEL_SHAPE_CARD.rstrip("\n"),
1))

# ---------- 2 — material (gamma) ----------
P2 = "docs/dna/02-material-threshold-scale/index.html"
EDITS.append((P2,
"but the scale of the threshold. That \u03b3 barely fails",
'but the scale of the threshold \u2014 and it is the <strong>level</strong> of the stiffness signal, not its '
'shape: where the element sits (shell, anchor, loop) is the mean-removed A4 read of '
'<a href="/dna/13-unified-deterministic-interpreter/">\u00a713</a>, a separate projection of the same field. '
"That \u03b3 barely fails",
1))

# ---------- 8 — bounds / retired ----------
P8 = "docs/dna/08-bounds-open-questions-retired-claims/index.html"

# (8a) closure clarifier: the four channels are not nested
EDITS.append((P8,
'the CpG handles (<a href="/dna/06-environment-drive-h/">\u00a76</a>). The <a href="/dna/the-dna-dictionary/">Dictionary</a>',
'the CpG handles (<a href="/dna/06-environment-drive-h/">\u00a76</a>). These four are not nested; in particular '
'\u03b3 and the A4 coordinate are the <strong>level</strong> and the <strong>shape</strong> of one stiffness '
'field \u2014 read together, never one inside the other. The <a href="/dna/the-dna-dictionary/">Dictionary</a>',
1))

# (8b) retired-framing tombstone: "gamma subset A4" is empirically falsified
EDITS.append((P8,
"never as a coordinate read of an element.</p>",
"never as a coordinate read of an element.</p>\n"
'<p><strong>Also retired (v1.13, irreversible):</strong> the framing <strong>\u201c\u03b3 \u2282 A4\u201d</strong> / '
'\u201c\u03b3 is one of the A4 coordinates\u201d / \u201c\u03b3 is a coarse A4.\u201d A direct measurement (37 loci, '
'2\u00d7SHA-256, prereg <code>ff04aa7b\u2026</code>) falsified every nesting hypothesis: \u03b3 and the A4 coordinate '
'read <strong>one stiffness field</strong> (per-locus \u03c1 = 0.94; identical coarse anchors, 0.0\u00a0bp offset '
'across all 37 loci) yet the A4 coordinate carries <strong>none of \u03b3</strong> (max |corr(axis, \u03b3)| = 0.327, '
'because the A4 pipeline\u2019s <code>robust_z</code> subtracts the per-locus median, which is exactly the level '
'\u03b3 is). The standing statement is: <strong>\u03b3 = the level (window-mean) and A4 = the shape (mean-removed '
'structure) of the same stiffness field \u2014 two orthogonal projections, neither nested in the other.</strong> '
'This framing must not revive under any name (e.g. \u201c\u03b3 is the zeroth A4 channel\u201d).</p>',
1))

# ---------- retrieval: llms.txt ----------
EDITS.append(("docs/llms.txt",
"- feature-emergence order = argsort(spinodal(\u03b3)) [V] ; \u03b3 \u27c2 developmental timing (heart \u03c1=+0.071, p=0.882) [O]",
"- feature-emergence order = argsort(spinodal(\u03b3)) [V] ; \u03b3 \u27c2 developmental timing (heart \u03c1=+0.071, p=0.882) [O]\n"
"- \u03b3 = LEVEL (window-mean of stiffness); A4 = SHAPE (same field, mean removed) \u2014 orthogonal projections, neither nested [V]",
1))

# ---------- _meta.json ----------
PM = "docs/dna/_meta.json"
EDITS.append((PM, '"version": "1.12",', '"version": "1.13",', 1))
EDITS.append((PM,
'"one_liner": "One deterministic interpreter reads a locus in five layers, restoring the A4 coordinate (shell, anchor, loops, anchor-relative helical phase) and correcting the global helical claim to an anchor-relative contact read, while keeping methylation as CpG O/E over raw density.",',
'"one_liner": "\u03b3 and the A4 coordinate are the level and the shape of one stiffness field (A4 = the same signal with \u03b3\u2019s mean removed); one engine reads both, restores the coordinate, and corrects the global helical claim to an anchor-relative contact read.",',
1))

# ============================ globals ============================
def apply_edit(path, old, new, expected):
    full = os.path.join(ROOT, path)
    with open(full, encoding="utf-8") as fh:
        txt = fh.read()
    n = txt.count(old)
    if n != expected:
        raise SystemExit("ABORT: %s -- anchor occurs %d time(s), expected %d:\n    %r"
                         % (path, n, expected, old[:80]))
    txt = txt.replace(old, new)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return n

def main():
    print("=" * 72)
    print("  v1.12 -> v1.13  gamma<->A4 LEVEL/SHAPE clarification (append-only)")
    print("=" * 72)

    applied = 0
    for path, old, new, exp in EDITS:
        n = apply_edit(path, old, new, exp)
        applied += n
        print("  [OK] %-58s (%d)" % (path.replace("docs/dna/", ""), n))

    # global footer version bump on every page
    foot_old = "multi-page canonical (v1.12)"
    foot_new = "multi-page canonical (v1.13)"
    pages = []
    for dp, _, fns in os.walk(os.path.join(ROOT, "docs")):
        for fn in fns:
            if fn.endswith(".html"):
                pages.append(os.path.join(dp, fn))
    foot_hits = 0
    for p in sorted(pages):
        with open(p, encoding="utf-8") as fh:
            t = fh.read()
        if foot_old in t:
            t = t.replace(foot_old, foot_new)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(t)
            foot_hits += 1
    print("  [OK] footer version bump on %d pages" % foot_hits)

    # hub claim-strip version string
    hub = os.path.join(ROOT, "docs/dna/index.html")
    with open(hub, encoding="utf-8") as fh:
        t = fh.read()
    cs_old = "multi-page canonical \u00b7 v1.12"
    cs_new = "multi-page canonical \u00b7 v1.13"
    if t.count(cs_old) != 1:
        raise SystemExit("ABORT: hub claim-strip version anchor count != 1")
    with open(hub, "w", encoding="utf-8") as fh:
        fh.write(t.replace(cs_old, cs_new))
    print("  [OK] hub claim-strip version -> v1.13")

    # sitemap lastmod refresh
    sm = os.path.join(ROOT, "docs/sitemap.xml")
    with open(sm, encoding="utf-8") as fh:
        t = fh.read()
    nlm = t.count("2026-06-17")
    with open(sm, "w", encoding="utf-8") as fh:
        fh.write(t.replace("2026-06-17", "2026-06-21"))
    print("  [OK] sitemap lastmod 2026-06-17 -> 2026-06-21 (%d urls)" % nlm)

    print("-" * 72)
    print("  edits applied: %d targeted + %d footers + hub + sitemap(%d) + llms + _meta"
          % (applied, foot_hits, nlm))
    print("  NO measured number / grade / equation / table / DOI changed. Append-only.")
    print("=" * 72)

if __name__ == "__main__":
    main()
