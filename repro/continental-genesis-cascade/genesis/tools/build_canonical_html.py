#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VP-SPEC v1.9 canonical HTML builder for the Continental-Genesis volume.

Constitution-first (VP_SPEC_v1_9 ch.0):
  C1 reproducibility  — this builder is deterministic; same sources -> same HTML.
  C2 single canonical — emits ONE self-contained HTML (CSS inlined; no TeX bundled).
                        (The §6 "no inline CSS" rule governs the multi-page live site;
                         the Constitution's "one canonical HTML / no fragmentation"
                         overrides it for a standalone volume canonical — Constitution takes precedence.)
  C3 openness ledger  — every [O]/computational-limit item is stated with its reason.
  C4 retrieval-ready  — answer-first page + per-section direct answers, self-contained
                        vp-cards, JSON-LD (ScholarlyArticle + BreadcrumbList + DefinedTerm),
                        short paragraphs.
  C5 shared infra     — inherits-strip (/modules/#id) + vp-cards (data-concept,/concepts/#id),
                        plus emitted registry/concepts.json, registry/modules.json, _decl.json.

No content is condensed: the full prose of all 25 modules and the supporting documents is
carried, only re-organised into numbered sub-chapters (§N.x).  English only (mottos kept as
the author's signature).  Grades use this volume's own LOCKed vocabulary [F]/[V]/[L]/[O]
(GOVERNANCE §1), precedence [F] > [V] > [L] > [O].
"""

import html
import json
import re
import hashlib
import pathlib
import datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
MOD = ROOT / "modules"

# --------------------------------------------------------------------------------------
# Minimal, deterministic Markdown -> HTML (no external deps; preserves unicode math).
# Handles: headings, tables (GitHub pipe), ordered/unordered lists, blockquotes,
# fenced code, inline code, bold, italic, strikethrough, links, horizontal rules.
# --------------------------------------------------------------------------------------

_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)")
_STRIKE = re.compile(r"~~([^~]+)~~")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _inline(text):
    """Inline markdown -> HTML on already-escaped text."""
    # protect code spans first
    spans = []

    def _stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    text = _INLINE_CODE.sub(_stash, text)
    text = _LINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _STRIKE.sub(r"<del>\1</del>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)

    def _unstash(m):
        return "<code>%s</code>" % spans[int(m.group(1))]

    text = re.sub(r"\x00(\d+)\x00", _unstash, text)
    return text


def _esc(s):
    return html.escape(s, quote=False)


def md_to_html(md):
    """Convert a markdown block (no leading H1/H2 — those are managed by the caller)."""
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)

    def flush_para(buf):
        if buf:
            out.append("<p>" + _inline(_esc(" ".join(buf).strip())) + "</p>")
            buf.clear()

    para = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code
        if stripped.startswith("```"):
            flush_para(para)
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            out.append("<pre><code>" + _esc("\n".join(code)) + "</code></pre>")
            continue

        # horizontal rule
        if re.match(r"^\s*---+\s*$", line):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        # heading inside a module body: ### -> h4, #### -> h5 (## handled by splitter)
        m = re.match(r"^(#{3,6})\s+(.*)$", stripped)
        if m:
            flush_para(para)
            level = min(len(m.group(1)) + 1, 6)  # demote one level under the chapter
            out.append("<h%d>%s</h%d>" % (level, _inline(_esc(m.group(2).strip())), level))
            i += 1
            continue

        # blockquote (possibly multi-line)
        if stripped.startswith(">"):
            flush_para(para)
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + md_to_html("\n".join(quote)) + "</blockquote>")
            continue

        # table (pipe). detect header + separator
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:\-\|]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            flush_para(para)
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ['<div class="tbl-wrap"><table>', "<thead><tr>"]
            for h in header:
                t.append("<th>" + _inline(_esc(h)) + "</th>")
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>")
                for c in r:
                    t.append("<td>" + _inline(_esc(c)) + "</td>")
                t.append("</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue

        # unordered list
        if re.match(r"^\s*[-*]\s+", line):
            flush_para(para)
            items = []
            while i < n and re.match(r"^\s*[-*]\s+", lines[i]):
                item = re.sub(r"^\s*[-*]\s+", "", lines[i])
                # gather continuation / nested indented lines
                i += 1
                while i < n and re.match(r"^\s{2,}\S", lines[i]) and not re.match(r"^\s*[-*]\s+", lines[i]):
                    item += " " + lines[i].strip()
                    i += 1
                items.append("<li>" + _inline(_esc(item.strip())) + "</li>")
            out.append("<ul>" + "".join(items) + "</ul>")
            continue

        # ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            flush_para(para)
            items = []
            while i < n and re.match(r"^\s*\d+\.\s+", lines[i]):
                item = re.sub(r"^\s*\d+\.\s+", "", lines[i])
                i += 1
                while i < n and re.match(r"^\s{2,}\S", lines[i]) and not re.match(r"^\s*\d+\.\s+", lines[i]):
                    item += " " + lines[i].strip()
                    i += 1
                items.append("<li>" + _inline(_esc(item.strip())) + "</li>")
            out.append("<ol>" + "".join(items) + "</ol>")
            continue

        # blank line ends paragraph
        if not stripped:
            flush_para(para)
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para(para)
    return "\n".join(out)


# --------------------------------------------------------------------------------------
# Site CSS (inlined into the single canonical file).  Grade colours ARE information:
# every claim wears its [F]/[V]/[L]/[O] grade — the load-bearing epistemic device.
# --------------------------------------------------------------------------------------

SITE_CSS = r"""
:root{
  --ink:#16181d; --ink-soft:#3b4250; --faint:#727a8a; --line:#e3e1d8; --line-2:#cfccc0;
  --paper:#faf8f2; --paper-2:#f3f0e6; --card:#fffdf7; --link:#7a2d1f; --link-h:#a13a26;
  --F:#1f6f4a; --F-bg:#e7f3ec; --V:#1d5fa8; --V-bg:#e6eff7; --L:#9a6a12; --L-bg:#f6efdd;
  --O:#6a6f7b; --O-bg:#eceef1; --reject:#9a1f2b; --reject-bg:#f7e7e8;
  --mono:"SFMono-Regular",ui-monospace,"JetBrains Mono",Menlo,Consolas,monospace;
  --serif:"Iowan Old Style","Charter","Source Serif 4",Cambria,Georgia,serif;
  --sans:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--serif);font-size:18px;line-height:1.62;
  font-feature-settings:"kern" 1,"liga" 1;text-rendering:optimizeLegibility}
.wrap{max-width:54rem;margin:0 auto;padding:0 1.4rem 6rem}
a{color:var(--link);text-decoration:none;border-bottom:1px solid rgba(122,45,31,.28)}
a:hover{color:var(--link-h);border-bottom-color:var(--link-h)}
a:focus-visible{outline:2px solid var(--V);outline-offset:2px;border-radius:2px}
h1,h2,h3,h4,h5{font-family:var(--sans);line-height:1.18;color:var(--ink);
  font-weight:680;letter-spacing:-.012em;margin:0 0 .5rem}
h1{font-size:2.15rem;font-weight:760;margin:.2rem 0 .3rem}
h2{font-size:1.62rem;margin:0 0 .35rem;padding-top:.2rem}
h3{font-size:1.22rem;margin:1.9rem 0 .4rem}
h4{font-size:1.04rem;margin:1.4rem 0 .3rem;font-weight:660}
h5{font-size:.96rem;margin:1.1rem 0 .25rem;color:var(--ink-soft)}
p{margin:.55rem 0}
strong{font-weight:680}
small{color:var(--faint)}
hr{border:0;border-top:1px solid var(--line);margin:1.6rem 0}
code{font-family:var(--mono);font-size:.86em;background:var(--paper-2);
  padding:.06em .34em;border-radius:4px;border:1px solid var(--line)}
pre{background:#1c1f26;color:#e8e6df;border-radius:10px;padding:1rem 1.1rem;overflow:auto;
  font-size:.82rem;line-height:1.5;border:1px solid #2a2e38}
pre code{background:none;border:0;color:inherit;padding:0;font-size:inherit}
blockquote{margin:.9rem 0;padding:.55rem 1rem;border-left:3px solid var(--line-2);
  background:var(--paper-2);border-radius:0 8px 8px 0;color:var(--ink-soft);font-size:.97em}
blockquote p:first-child{margin-top:0}blockquote p:last-child{margin-bottom:0}
.tbl-wrap{overflow-x:auto;margin:1rem 0;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-family:var(--sans);font-size:.86rem}
th,td{padding:.5rem .7rem;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:var(--paper-2);font-weight:660;color:var(--ink);
  border-bottom:2px solid var(--line-2);position:sticky;top:0}
tbody tr:last-child td{border-bottom:0}
tbody tr:nth-child(even){background:rgba(0,0,0,.014)}

/* ---- masthead ---------------------------------------------------------------- */
.crumb{font-family:var(--sans);font-size:.8rem;color:var(--faint);padding:1.3rem 0 .2rem}
.crumb a{border:0}
.masthead{padding:.4rem 0 1.1rem;border-bottom:2px solid var(--ink);margin-bottom:1.6rem}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--link);margin:0 0 .6rem}
.byline{font-family:var(--sans);font-size:.85rem;color:var(--ink-soft);margin:.6rem 0 .2rem;line-height:1.7}
.byline b{color:var(--ink)}
.motto{font-family:var(--sans);font-size:.84rem;color:var(--faint);margin:.3rem 0 0}
.motto b{color:var(--L)}

/* ---- answer-first / abstract ------------------------------------------------- */
.answer{font-family:var(--sans);font-size:1.06rem;line-height:1.55;font-weight:500;
  color:var(--ink);background:var(--card);border:1px solid var(--line-2);
  border-left:4px solid var(--link);border-radius:0 10px 10px 0;padding:1rem 1.15rem;margin:1.3rem 0}
.abstract{font-size:1.02rem;color:var(--ink-soft);margin:1rem 0 1.2rem}
.abstract b{color:var(--ink)}

/* ---- claim strip ------------------------------------------------------------- */
.claim-strip{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-family:var(--sans);
  font-size:.78rem;margin:1rem 0 1.4rem;padding:.6rem .2rem;border-top:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.claim-strip a{border:0;background:var(--paper-2);padding:.28rem .6rem;border-radius:999px;
  color:var(--ink-soft);border:1px solid var(--line)}
.claim-strip a:hover{background:var(--card);color:var(--link)}
.gate{font-family:var(--mono);font-size:.72rem;letter-spacing:.04em;color:var(--faint);
  background:var(--paper-2);padding:.28rem .6rem;border-radius:999px;border:1px solid var(--line)}

/* ---- grade badges ------------------------------------------------------------ */
.g{font-family:var(--mono);font-weight:700;font-size:.74rem;letter-spacing:.02em;
  padding:.1rem .42rem;border-radius:5px;border:1px solid;white-space:nowrap;line-height:1.5}
.g-F{color:var(--F);background:var(--F-bg);border-color:#bfe0cd}
.g-V{color:var(--V);background:var(--V-bg);border-color:#c3d8ef}
.g-L{color:var(--L);background:var(--L-bg);border-color:#e6d39a}
.g-O{color:var(--O);background:var(--O-bg);border-color:#d3d7df}
.g-reject{color:var(--reject);background:var(--reject-bg);border-color:#e9c5c9}

/* ---- inherits strip ---------------------------------------------------------- */
.inherits-strip{display:flex;flex-wrap:wrap;gap:.45rem;align-items:center;font-family:var(--sans);
  font-size:.78rem;margin:0 0 1.4rem;padding:.55rem .75rem;background:var(--paper-2);
  border:1px solid var(--line);border-radius:10px}
.inherits-strip .lbl{font-weight:660;color:var(--faint);text-transform:uppercase;letter-spacing:.08em;
  font-size:.7rem;margin-right:.2rem}
.inherits-strip a{border:0;background:var(--card);padding:.22rem .55rem;border-radius:6px;
  border:1px solid var(--line-2);color:var(--ink-soft);font-weight:550}
.inherits-strip a:hover{color:var(--link)}

/* ---- vp-card (locked quantity, self-contained) ------------------------------- */
.vp-card{font-family:var(--sans);font-size:.86rem;line-height:1.5;background:var(--card);
  border:1px solid var(--line-2);border-left:3px solid var(--V);border-radius:0 9px 9px 0;
  padding:.7rem .9rem;margin:1rem 0}
.vp-card b:first-child{font-family:var(--mono);font-size:.92em;color:var(--ink)}
.vp-card .links{display:block;margin-top:.35rem;font-size:.78rem}
.vp-card .links a{border:0;color:var(--faint)}
.vp-card .links a:hover{color:var(--link)}
.vp-card.owned{border-left-color:var(--F)}

/* ---- chapter scaffolding ----------------------------------------------------- */
.chapter{margin:3.2rem 0 0;padding-top:1.4rem;border-top:1px solid var(--line)}
.chapter>.secno{font-family:var(--mono);font-size:.74rem;letter-spacing:.14em;color:var(--link);
  text-transform:uppercase;display:block;margin-bottom:.3rem}
.subchapter{margin:1.7rem 0 0}
.subchapter>h3>.sn{font-family:var(--mono);font-size:.8em;color:var(--faint);margin-right:.5rem;font-weight:600}
.eq{font-family:var(--mono);font-size:.95rem;background:var(--paper-2);border:1px solid var(--line);
  border-radius:8px;padding:.7rem .95rem;margin:.9rem 0;overflow-x:auto;text-align:center;color:var(--ink)}
.eq .lbl{float:right;color:var(--faint);font-size:.78rem;font-family:var(--sans)}
.note{font-size:.9rem;color:var(--ink-soft);background:var(--paper-2);border:1px dashed var(--line-2);
  border-radius:8px;padding:.6rem .85rem;margin:.9rem 0}
.note .k{font-family:var(--sans);font-weight:660;color:var(--ink);font-size:.78rem;
  text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:.2rem}

/* ---- table of contents ------------------------------------------------------- */
.toc{font-family:var(--sans);background:var(--paper-2);border:1px solid var(--line);
  border-radius:12px;padding:1.1rem 1.3rem;margin:1.8rem 0}
.toc h2{font-size:1.05rem;margin:0 0 .6rem;font-family:var(--sans)}
.toc ol{margin:0;padding-left:1.4rem;columns:2;column-gap:2rem;font-size:.84rem;line-height:1.7}
.toc li{break-inside:avoid;margin:0}
.toc a{border:0;color:var(--ink-soft)}
.toc a:hover{color:var(--link)}
@media (max-width:640px){.toc ol{columns:1}}

/* ---- spine list -------------------------------------------------------------- */
.spine{counter-reset:spine;list-style:none;padding:0;margin:1rem 0}
.spine li{position:relative;padding:.5rem .5rem .5rem 2.4rem;margin:.4rem 0;background:var(--card);
  border:1px solid var(--line);border-radius:9px;font-size:.94rem}
.spine li::before{counter-increment:spine;content:counter(spine);position:absolute;left:.7rem;top:.55rem;
  font-family:var(--mono);font-weight:700;font-size:.8rem;color:var(--link)}

/* ---- footer ------------------------------------------------------------------ */
footer{margin-top:4rem;padding-top:1.4rem;border-top:2px solid var(--ink);
  font-family:var(--sans);font-size:.82rem;color:var(--faint);line-height:1.7}
footer a{color:var(--ink-soft)}
footer b{color:var(--ink)}

/* ---- glossary / defined terms ------------------------------------------------ */
.term{background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:.85rem 1rem;margin:.8rem 0}
.term .head{font-family:var(--sans);font-weight:660;color:var(--ink);font-size:.98rem;
  display:flex;gap:.5rem;align-items:baseline;flex-wrap:wrap}
.term .sym{font-family:var(--mono);color:var(--link);font-size:.92rem}
.term .body{font-size:.92rem;color:var(--ink-soft);margin-top:.35rem}
.term .meta{font-family:var(--mono);font-size:.74rem;color:var(--faint);margin-top:.35rem}

@media (max-width:560px){
  body{font-size:16.5px}.wrap{padding:0 1rem 4rem}
  h1{font-size:1.8rem}h2{font-size:1.4rem}.toc ol{columns:1}
}
"""


# ======================================================================================
# Shared-infrastructure registries (Constitution C5 / SPEC §6-M).
# concepts.json  = locked quantities (each a self-contained DefinedTerm, one-line statement).
# modules.json   = inherited common modules (the /modules/ link targets).
# Owner "continental-genesis" terms are owns_terms; inherited terms are uses_terms.
# ======================================================================================

PAPER_ID = "continental-genesis"
ORCID = "https://orcid.org/0009-0002-7535-8245"
HUB = "https://jamming-physics.org/" + PAPER_ID + "/"
REPO = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/" + PAPER_ID + "/"
DOI_PHYSICS = "10.5281/zenodo.17932566"
DOI_GEODYN = "10.5281/zenodo.17978934"
DOI_FLUID = "10.5281/zenodo.17972568"
DOI_THIS = "10.5281/zenodo.20827711"  # concept DOI (resolves to the latest version); living version on the hub

# --- inherited common modules (uses) --------------------------------------------------
MODULES = {
    "kernel": {
        "id": "kernel", "name": "R19 jamming kernel",
        "forces": ["jammed\u21c4unjammed bistable switch", "marginal-substrate elastic-wave law c\u00b2=B/\u03c1"],
        "reach": "bedrock", "grade": "F",
        "canonical": "https://doi.org/" + DOI_PHYSICS,
        "statement": ("The R19 jammed\u21c4unjammed bistable switch (void-suction / unjamming rupture) on a "
                      "jammed elastic substrate whose relaxed shear modulus \u2192 0 at the unjamming margin "
                      "while the bulk modulus B stays finite, so c\u00b2 = B/\u03c1. Inherited at full strength; "
                      "not re-derived here."),
        "inherited_by": [PAPER_ID],
    },
    "rotor_inflow": {
        "id": "rotor_inflow", "name": "Three-rotor co-rotation / Ekman inflow",
        "forces": ["odd-cycle C\u2083 frustration forces co-rotation", "co-rotating vortices merge",
                   "coherent rotation drives an Ekman through-flow (radial inflow \u221d\u221a(\u03bd/\u03a9))"],
        "reach": "rotating marginal fluid", "grade": "F",
        "canonical": "https://doi.org/" + DOI_FLUID,
        "statement": ("Three-body (C\u2083) frustration forces co-rotation; co-rotating vortices merge into one "
                      "coherent rotation; a coherent rotation drives an Ekman through-flow with radial inflow "
                      "\u221d \u221a(\u03bd/\u03a9). Supplies the organizing vortex + convergent feed of the "
                      "upwelling-cell hypothesis (\u00a718)."),
        "inherited_by": [PAPER_ID],
    },
}

# --- locked quantities (concepts). owner: 'physics'/'fluid-dynamics'/'geodynamics' = inherited;
#     owner: 'continental-genesis' = owned here. Each statement is self-contained (one line). ---
CONCEPTS = [
    # ---- inherited (uses_terms) ----
    dict(id="c2_brho", term="Elastic-wave / marginal-substrate law", symbol="c\u00b2 = B/\u03c1",
         value="c\u00b2 = B/\u03c1", grade="F", owner="physics", href="https://doi.org/" + DOI_PHYSICS,
         statement="At the unjamming margin the relaxed shear modulus \u2192 0 while the bulk modulus B stays "
                   "finite, so the wave speed is set by c\u00b2 = B/\u03c1 \u2014 a medium that is a fluid by "
                   "arrangement. Inherited from VP physics."),
    dict(id="r19_switch", term="R19 jammed\u21c4unjammed bistable switch", symbol="R19",
         value="bistable", grade="F", owner="physics", href="https://doi.org/" + DOI_PHYSICS,
         statement="The void-suction / unjamming-rupture switch: a medium poised below its unjamming threshold "
                   "ruptures locally where the threshold is crossed (bulk jammed, local unjamming). Inherited."),
    dict(id="marginal_substrate", term="Marginal jammed substrate", symbol="G_relaxed\u21920",
         value="relaxed shear \u2192 0", grade="F", owner="fluid-dynamics", href="https://doi.org/" + DOI_FLUID,
         statement="A substrate poised at the isostatic margin has zero relaxed shear stiffness, so it offers no "
                   "restoring force against a transport perturbation \u2014 symmetry-breaking is permitted, not "
                   "forbidden. Inherited from the Configured Continuum."),
    dict(id="ekman_inflow", term="Co-rotation \u2192 merge \u2192 Ekman inflow", symbol="\u221d\u221a(\u03bd/\u03a9)",
         value="forced inflow", grade="F", owner="fluid-dynamics", href="https://doi.org/" + DOI_FLUID,
         statement="C\u2083 frustration forces co-rotation; co-rotating vortices merge; the coherent rotation pumps "
                   "a convergent Ekman through-flow with radial inflow \u221d \u221a(\u03bd/\u03a9). Inherited."),
    dict(id="firewall", term="Bidirectional chronology firewall", symbol="[O] both ways",
         value="dates = RECORD", grade="F", owner="geodynamics", href="https://doi.org/" + DOI_GEODYN,
         statement="Every absolute date is RECORD and forbidden as load-bearing in BOTH directions; every "
                   "past-occurrence statement is [O]. Only present-tense, non-rate observables carry the argument."),
    # ---- owned by this volume (owns_terms) ----
    dict(id="two_tier_crust", term="Two-tier crust", symbol="\u03c1: 2.8 / 2.9 / 3.3",
         value="felsic ~2.8 / basalt ~2.9 / mantle ~3.3 g cm\u207b\u00b3", grade="V", owner=PAPER_ID,
         href="#ch3", statement="Felsic continental crust (~2.8 g cm\u207b\u00b3, ~35 km) and basaltic ocean skin "
                   "(~2.9, ~7 km) over mantle (~3.3): density\u00d7thickness is the only reason dry land and ocean "
                   "basins coexist \u2014 composition, not age."),
    dict(id="buckling_bar", term="Compression-face buckling bar", symbol="\u03c3_cr(\u03bb)",
         value="154\u2013614 MPa at \u03bb 300\u2013600 km", grade="F", owner=PAPER_ID, href="#ch5",
         statement="The lateral stress to buckle a 30 km skin falls with wavelength (614 MPa at 300 km \u2192 154 MPa "
                   "at 600 km): the \u201chuge push\u201d becomes a calculable, feasible stress threshold."),
    dict(id="wet_solidus", term="Wet vs dry granitic solidus", symbol="~650 vs ~950 \u00b0C",
         value="solidus ~650 \u00b0C wet / ~950 \u00b0C dry", grade="F", owner=PAPER_ID, href="#ch6",
         statement="Water lowers the granitic solidus by ~300 \u00b0C: a 600\u2013800 \u00b0C lower crust does not "
                   "melt dry (no granite) but the same crust wet crosses the solidus \u2192 partial melt \u2192 "
                   "granite. The submarine start supplies the water."),
    dict(id="airy_freeboard", term="Airy rock freeboard", symbol="4.45 km",
         value="4.45 km continent-top minus ocean-floor", grade="F", owner=PAPER_ID, href="#ch7",
         statement="A 2.8 g cm\u207b\u00b3, 35 km felsic column floats with its top 4.45 km above oceanic-crust top "
                   "by Airy balance \u2014 no upward force; the basin subsides and emergence follows."),
    dict(id="isochron_nonunique", term="Isochron non-uniqueness caveat", symbol="mixing \u2261 isochron",
         value="mixing line \u2261 isochron", grade="V", owner=PAPER_ID, href="#ch8",
         statement="A two-component mixing line is algebraically identical to an isochron, so an isochron age is "
                   "NON-UNIQUE. This supports the firewall and is never load-bearing for \u201cyoung.\u201d"),
    dict(id="buoyancy_gate", term="Buoyancy gate (sign law)", symbol="B = \u03a3(\u03c1_asth\u2212\u03c1_i)h_i",
         value="B>0 floats / B<0 subducts", grade="F", owner=PAPER_ID, href="#ch9",
         statement="A compressed column's response is gated by net buoyancy B: net-negative old ocean skin sheds "
                   "compression by subducting (smooth deep floor); net-positive felsic cannot sink and must crumple."),
    dict(id="signflip_age", term="Ocean buoyancy sign-flip", symbol="t* \u2248 11 Ma",
         value="net-buoyancy flips at ~11 Ma, ~3.7 km depth", grade="F", owner=PAPER_ID, href="#ch10",
         statement="Half-space cooling flips the ocean skin's net buoyancy from positive to negative at t* \u2248 11 Ma "
                   "(~3.7 km depth); most deep floor is older/deeper and net-negative."),
    dict(id="compensation_law", term="Isostatic-compensation law", symbol="h_max\u2248\u0394H(\u03c1m\u2212\u03c1c)/(\u03c1m\u2212\u03c1top)",
         value="bare skin caps ~1 km; felsic ~5 km", grade="F", owner=PAPER_ID, href="#ch11",
         statement="Maximum compensated relief needs a deep light root: normal 7 km basalt skin (even doubled) caps "
                   "at ~1 km, felsic collision reaches ~5 km. Live test = free-air gravity + Moho depth."),
    dict(id="jamming_state", term="Mantle jamming state", symbol="T/T_solidus ~0.7\u20130.95",
         value="jammed solid near unjamming, not magma", grade="F", owner=PAPER_ID, href="#ch12",
         statement="The mantle is a jammed solid near unjamming (T/T_solidus ~0.7\u20130.95): it flows as a heavy "
                   "fluid on Myr but transmits S-waves (\u03bc>0, solid) \u2014 ~10\u00b9\u2075\u201310\u00b9\u2079\u00d7 "
                   "magma viscosity. Magma is the local unjammed state."),
    dict(id="assembly_entailment", term="Assembly entailment chain", symbol="opening \u21d2 one-sided mass",
         value="one-sided felsic mass is forced", grade="F", owner=PAPER_ID, href="#ch16",
         statement="On a fixed-area sphere (A = 5.101\u00d710\u00b9\u2074 m\u00b2), opening forces antipodal closing "
                   "(conservation) \u2192 skin subducts/raft cannot (buoyancy) \u2192 raft collects at the sink "
                   "(kinematics) \u21d2 a one-sided felsic mass is entailed. A dependency graph, not a timeline."),
    dict(id="downwelling_convergence", term="Convergence = downwelling limb", symbol="Ra\u22485.85\u00d710\u2076",
         value="convergence is the forced downwelling limb", grade="F", owner=PAPER_ID, href="#ch21",
         statement="A hot fluid sphere must convect (Ra \u2248 5.85\u00d710\u2076 \u226b critical); closed-sphere "
                   "convection has up- and down-limbs by conservation, so the convergence IS the downwelling limb \u2014 "
                   "not a separate assumption. The first seed is the first downwelling's flux-melt."),
    dict(id="freeboard_fixedpoint", term="Freeboard fixed point (R1)", symbol="+840 m (measured)",
         value="isostasy + measured water \u2192 observed freeboard", grade="F", owner=PAPER_ID, href="#ch22",
         statement="A present-tense fixed point (no time): textbook \u03c1_c=2800 overshoots to +1915 m, but the "
                   "measured bulk density/thickness lands at +840 m = observed. The lever is the distilled-felsic "
                   "density deficit."),
    dict(id="bimodal_hypsometry", term="Bimodal hypsometry", symbol="+1544 / \u22123686 m",
         value="two peaks, separation ~5.2 km", grade="F", owner=PAPER_ID, href="#ch22",
         statement="The same isostatic system yields two elevation peaks (land +1544 m, ocean \u22123686 m, separation "
                   "~5.2 km); sea level sits ~70% up the relief, so continents are near-marginal \u2014 emergent by "
                   "only the top ~30%."),
    dict(id="percolation_attractor", term="Area-fraction percolation attractor", symbol="f* \u2248 0.407",
         value="ocean-network percolation bound", grade="L", owner=PAPER_ID, href="#ch23",
         statement="The ~40% continental area fraction is a self-organized marginal-connectivity (percolation) "
                   "attractor of the complementary ocean network (planar f* \u2248 0.407): a fragmenting ocean throttles "
                   "its own subduction, pinning the fraction rate-insensitively."),
    dict(id="percolation_z", term="Connectivity-dependent ceiling", symbol="z = 6\u221212/F",
         value="f*\u22480.41(z=4)\u20130.50(z=6); natural net z\u22485\u20136", grade="L", owner=PAPER_ID, href="#ch26",
         statement="The percolation ceiling is connectivity-dependent: f* \u2248 0.41 (z=4) \u2192 0.50 (z=6). Euler "
                   "topology gives the plate network z = 6\u221212/F \u2248 5\u20136, so its ceiling ~0.46\u20130.50 "
                   "overshoots 0.41 \u2014 regime-right, exact value not uniquely forced."),
    dict(id="three_margins", term="Three marginal attractors (R2)", symbol="substrate / freeboard / area",
         value="one marginal-criticality kernel", grade="L", owner=PAPER_ID, href="#ch23",
         statement="Where land sits (over downwellings), how high it stands (marginal freeboard) and how much there "
                   "is (marginal percolation) are three faces of the c\u00b2=B/\u03c1 kernel's marginal criticality: "
                   "VP is the foundation beneath mantle convection, not a competitor."),
    dict(id="ra_onset", term="Boussinesq onset (solver validation)", symbol="Ra_c = 27\u03c0\u2074/4 \u2248 657.5",
         value="validated to ~1e-7", grade="F", owner=PAPER_ID, href="#ch23",
         statement="The infinite-Pr 3D Boussinesq solver is validated against the analytic free-slip onset "
                   "Ra_c = 27\u03c0\u2074/4 \u2248 657.5 (single-mode growth matches linear theory to ~1e-7), so the "
                   "area-fraction stress tests run on a verified convection engine."),
]

CONCEPT_BY_ID = {c["id"]: c for c in CONCEPTS}
OWNS = [c["id"] for c in CONCEPTS if c["owner"] == PAPER_ID]
USES = [c["id"] for c in CONCEPTS if c["owner"] != PAPER_ID]

GRADE_NAME = {"F": "forced", "V": "verified", "L": "leaning", "O": "open", "reject": "rejected"}


def grade_badge(letter):
    cls = "g-" + letter
    nm = GRADE_NAME.get(letter, letter)
    return '<span class="g %s" title="%s">[%s]</span>' % (cls, nm, letter if letter != "reject" else "rejected")


def grades(*letters):
    return " ".join(grade_badge(l) for l in letters)


def vp_card(cid):
    """Self-contained locked-quantity card (SPEC §6-R.2 + §6-M.3)."""
    c = CONCEPT_BY_ID[cid]
    owned = c["owner"] == PAPER_ID
    canon_label = "canonical derivation" if not owned else "derivation"
    canon_href = c["href"] if owned else c["href"]
    klass = "vp-card owned" if owned else "vp-card"
    g = grade_badge(c["grade"])
    return (
        '<aside class="%s" data-locked="%s" data-concept="%s">'
        '<b>%s</b> \u2014 %s %s'
        '<span class="links"><a href="%s">%s</a> \u00b7 <a href="#concept-%s">term</a></span>'
        '</aside>'
    ) % (klass, cid, cid, _esc(c["value"]), _inline(_esc(c["statement"])), g,
         canon_href, canon_label, cid)


def inherits_strip():
    links = "".join('<a href="#module-%s">%s</a>' % (m, MODULES[m]["name"]) for m in MODULES)
    return ('<aside class="inherits-strip" aria-label="Inherited common modules">'
            '<span class="lbl">Inherits</span>%s</aside>') % links


def eq(expr, label=None):
    lab = '<span class="lbl">%s</span>' % _esc(label) if label else ""
    return '<div class="eq">%s%s</div>' % (lab, _inline(_esc(expr)))


# ======================================================================================
# Language normalisation (Constitution: English only). The author's recurring motto is
# kept once, in the masthead, as a signature; in-body occurrences are rendered in English.
# Korean reasoning-quotes are translated inline, meaning preserved.
# ======================================================================================
LANG_MAP = []  # source is English-only; no Korean tokens remain to normalise


def normalise_lang(s):
    for k, v in LANG_MAP:
        s = s.replace(k, v)
    # any stray remaining Hangul -> drop (keeps the file English-only); log via marker
    return s


# ======================================================================================
# Module -> chapter transform.  Strips the module H1 + Screen/Motto metadata (folded into
# a per-chapter claim-strip), then splits the body on '## ' into numbered sub-chapters.
# NO prose is dropped: every '## ' section of every module becomes a §N.x sub-chapter.
# ======================================================================================
_SCREEN_RE = re.compile(r"\*\*Screen:\*\*\s*`([^`]+)`\s*(?:\u2192|->|\u2014>)?\s*gate\s*`([0-9a-f]+)`", re.I)
_SCREEN_RE2 = re.compile(r"\*\*Screen:\*\*\s*`([^`]+)`", re.I)


def parse_module(path):
    raw = normalise_lang(path.read_text(encoding="utf-8"))
    lines = raw.split("\n")
    # drop leading H1
    while lines and not lines[0].startswith("# "):
        lines.pop(0)
    if lines:
        lines.pop(0)
    body = "\n".join(lines)

    screen = None
    gate = None
    m = _SCREEN_RE.search(body)
    if m:
        screen, gate = m.group(1), m.group(2)
    else:
        m2 = _SCREEN_RE2.search(body)
        if m2:
            screen = m2.group(1)

    # remove the metadata lines (Screen / Motto / Inherits / Method / Outcome / Charge /
    # Purpose / Simulations) that sit before the first '## '
    head, _, rest = body.partition("\n## ")
    rest = "## " + rest if rest else ""
    keep_head = []
    for ln in head.split("\n"):
        st = ln.strip()
        if re.match(r"^\*\*(Screen|Motto|Inherits|Method|Outcome|Charge|Purpose|Simulations|Simulations \(shipped[^)]*\))\*\*:", st):
            continue
        if st.startswith("**Screen:**") or st.startswith("**Motto:**"):
            continue
        keep_head.append(ln)
    head = "\n".join(keep_head).strip()
    full = (head + "\n\n" + rest).strip() if head else rest.strip()
    return full, screen, gate


def render_module_body(num, body):
    """Split a module body on '## ' headings into numbered §num.x sub-chapters."""
    parts = re.split(r"\n## ", "\n" + body)
    html_parts = []
    sub = 0
    # leading text before the first '## ' (rare)
    lead = parts[0].strip()
    if lead and not lead.startswith("## "):
        html_parts.append(md_to_html(lead))
        parts = parts[1:]
    else:
        parts = parts[1:] if parts and parts[0].strip() == "" else parts
    for p in parts:
        p = p.strip()
        if not p:
            continue
        line, _, inner = p.partition("\n")
        title = line.strip().lstrip("# ").strip()
        sub += 1
        sn = "\u00a7%d.%d" % (num, sub)
        html_parts.append(
            '<section class="subchapter" id="ch%d-%d">'
            '<h3><span class="sn">%s</span>%s</h3>%s</section>'
            % (num, sub, sn, _inline(_esc(title)), md_to_html(inner.strip()))
        )
    return "\n".join(html_parts)


def render_doc_body(num, path, drop_meta=True):
    """Transform a top-level .md document the same way (strip H1 + author/motto block)."""
    raw = normalise_lang(path.read_text(encoding="utf-8"))
    lines = raw.split("\n")
    while lines and not lines[0].startswith("# "):
        lines.pop(0)
    if lines:
        lines.pop(0)
    body = "\n".join(lines)
    if drop_meta:
        kept = []
        for ln in body.split("\n"):
            st = ln.strip()
            if re.match(r"^\*\*(Author|ORCID|License|Motto|Scope|Method|Purpose|Foundations inherited)\*\*", st):
                continue
            kept.append(ln)
        body = "\n".join(kept)
    # collapse a leading run of blank lines
    body = re.sub(r"^\s*\n+", "", body)
    return render_module_body(num, body)


# ======================================================================================
# Page-level answer-first + abstract (Constitution C4 / SPEC section 6).
# ======================================================================================
FRONT_ANSWER = (
    "Dry land exists because of <b>composition and buoyancy, not age</b>: continents are light "
    "felsic crust (\u03c1 \u2248 2.8 g cm\u207b\u00b3) distilled by water-fluxed partial melting on the "
    "compressional, downwelling face of a convecting mantle, too light to re-sink, standing proud by "
    "isostasy as the ocean basin subsides. The mechanism chain is forced and chronology-free; "
    "occurrence and timing stay <b>[O]</b> forever."
)
ABSTRACT = (
    "This volume derives why a <b>two-tier crust</b> \u2014 light felsic continents over a heavy basaltic "
    "ocean skin \u2014 exists at all, from a single inherited jamming kernel (c\u00b2 = B/\u03c1, R19 switch) "
    "with <b>no fitted parameter</b>. A connected, chronology-free [F]/[V] spine runs from a hot "
    "near-unjamming mantle (T/T_solidus ~0.7\u20130.95) through forced convection (Ra \u2248 5.85\u00d710\u2076) "
    "whose downwelling limb <b>is</b> the convergence that flux-melts hydrated skin into granite, to "
    "one-sided dry land emergent by basin subsidence. Isostasy plus the measured ocean water volume "
    "reproduces the observed freeboard (~+840 m) and bimodal hypsometry (peaks +1544 / \u22123686 m, "
    "separation ~5.2 km). The ~40% area fraction is a percolation-bounded sub-majority (~0.4\u20130.5); its "
    "exact value stays [O], and occurrence/timing stays [O] forever. 25 modules, 23 SEED=19 "
    "double-SHA-256 gated screens, honestly graded."
)

# ---- inline markdown for the synthesis chapters --------------------------------------
CH1_MD = r"""## The origin question

Mainstream geology explains how the two-tier crust is *recycled*, but not cleanly why it *exists in the first place* — why there is light, emergent dry land at all, sitting above heavy ocean floor. This volume asks that origin question under a firewall, and answers it with **composition + buoyancy, not age**.

Begin from a water-covered world with only a thin mantle skin and no continents. A rift opens; its centre founders into a deep basin floored by bare mantle skin; the displaced skin is pushed sideways, thickened and folded; the lateral push and burial **heat** the thickened, **water-bearing** pile; the wet pile **partially melts**, distilling a light **felsic** (granitic) fraction that rises, cools, and — being too light to sink back — **accumulates** as buoyant crust. Dry land is that distilled, accumulated felsic; the ocean is the basic mantle skin it stands above. Land need not *rise*; the basin *subsides*, and emergence follows by isostasy.

This reframes "why land" away from the clock and onto the **mechanism that makes light crust** — the hard part, which is composition.

## The bidirectional chronology firewall (the core rule)

Every past-occurrence statement is [O]; every absolute date is RECORD, forbidden as load-bearing in **both** directions. The firewall is symmetric: it removes the mainstream's deep-time dates **and** withholds the convenient young numbers. Neither "billions of years" nor "recent" is load-bearing.

The theory's distinctive content, on every axis, reduces to **rate / magnitude / timing / order**, which the firewall caps at [O] both ways. Only present-tense, non-rate observables can be load-bearing. This is the constitution; where any later clause conflicts with it, the firewall wins.

## The grading system

Processing degree **D0–D5**: D0 = raw observation (top); **D0–D3 = load-bearing (ACTIVE)**; **D4 (model output) and D5 (absolute chronology) = RECORD, never load-bearing**.

Status grades, with precedence **[F] > [V] > [L] > [O]**:

- **[F]** — physically forced / permitted by measured constants (a screen result).
- **[V]** — observed / verified present-tense (measured, or engine-reproduced).
- **[L]** — leaning: a well-anchored inference, short of forced.
- **[O]** — open / undecided. **Occurrence is capped at [O] forever.**

Nothing downstream may launder an [O] into a higher grade. **No external interpretation may settle the meaning of an observation** — a favoured and a disfavoured interpretation of the same observation get the **same** grade. Every datum is recomputed from the primary source, not recalled; only the recomputed quantity is [V]. The rule binds the inconvenient direction as well as the welcome one.

Reproducibility is enforced: **no fitted parameter** in any Tier-A object; **SEED = 19** convention; determinism proven by **double-SHA-256** self-gates; changing any LOCK constant defines a new version; corrections **mark, never erase**.

## The specific failure mode this volume must not repeat

A tempting but forbidden move would be to **positively refute** the 4 Ga zircon ages (thermal reset → "young") to make recent continent-formation load-bearing. That would be the canonical error this firewall forbids — **attacking a firewalled date to privilege the convenient direction**. This volume does **not** do that. It holds the U-Pb ages as RECORD, routes *when/how-fast* to [O], and load-bears only on present-tense mechanism screens. The zircon understanding here is a **caveat** (isochron non-uniqueness, §8), never a refutation."""

CH2_EXTRA_MD = r"""## The inherited results, carried in full

The argument uses — and ships — five upstream results so the package is self-contained without Zenodo:

- **I1 — c² = B/ρ marginal-substrate fluid.** At the unjamming margin the relaxed shear modulus → 0 while the bulk modulus B stays finite; the medium is a fluid by arrangement (the same substrate as the hot mantle, §12).
- **I2 — R19 unjamming switch.** The void-suction / unjamming-rupture bistable switch: bulk jammed, local unjamming where the threshold is crossed.
- **I3 — rotation → three-body C₃ core.** Odd-cycle (C₃) frustration forces co-rotation.
- **I4 — co-rotation → merger → Ekman through-flow.** Co-rotating vortices merge; a coherent rotation drives a convergent Ekman inflow; inflow and updraft are one loop (§18).
- **I5 — the firewall.** The bidirectional chronology firewall (§1), inherited as the constitution.

The fluid-dynamics foundational PDF and four runnable inherited scripts (`marginal_fluidity.py`, `unjam_inflow.py`, `axioms.py`, `corotation.py`) are shipped under `inherited/`; each runs offline and reproduces its inherited mechanism. The physics (DOI 10.5281/zenodo.17932566) and Atlantic-geodynamics (DOI 10.5281/zenodo.17978934) source packages remain external, their load-bearing results stated in `inherited/INHERITED_RESULTS_CARD.md`."""

CH29_MD = r"""## The 23 gated screens

Every quantitative screen is self-contained, deterministic (SEED = 19), and prints `REPRO GATE: PASS` on its last line; its displayed numbers are recomputed and checked against a double-SHA-256 gate, so a wrong number cannot pass silently. The screens, with the chapter each supports and its gate prefix:

| screen (`repro/…`) | supports | gate (2×SHA-256) |
|---|---|---|
| `buckling_stress_screen.py` | §5 compression-face stress bar | `811aba1d…20f3` |
| `wet_solidus_thermal_screen.py` | §6 heat → granite, wet solidus | `01e659c1…3a64` |
| `pseudo_isochron_caveat.py` | §8 isochron non-uniqueness | `3f835b8c…f610` |
| `isostasy_emergence_screen.py` | §7 emergence-by-subsidence + Moho | `f2c426e5…e805` |
| `buoyancy_gating_screen.py` | §9 buoyant load gates compression | `a87f1a89…51b3` |
| `buoyancy_signflip_screen.py` | §10 sign-flip + CG-22 breaker | `a51a6693…ee1e` |
| `isostatic_compensation_law_screen.py` | §11 compensation law + gravity | `b309631e…38ed` |
| `mantle_jamming_state_screen.py` | §12 jammed solid near unjamming | `8c732f37…c9c0` |
| `convective_state_screen.py` | §13 present-state synthesis | `f5b55cbd…35bb` |
| `asymmetry_and_divergence_screen.py` | §14 asymmetry degenerate; origin diverges | `985b4c39…d6b6` |
| `firewall_self_audit_screen.py` | §15 imported-chronology breaches + fixes | `f783764c…61d2` |
| `assembly_causal_chain_screen.py` | §16 opening → one-sided-mass chain | `6ed0210a…c79a` |
| `symmetry_breaking_inheritance_screen.py` | §17 inherited symmetry-breaking capacity | `ca63495c…a551` |
| `upwelling_cell_hypothesis_screen.py` | §18 forced up-and-out vent (v2) | `399566a3…9716` |
| `granite_carbonate_dichotomy_screen.py` | §20 granite/limestone two faces | `7cbaa628…0efb` |
| `closed_loop_dissolution_screen.py` | §21 convergence = downwelling limb | `779a2269…cb0c` |
| `r1_budget_screen.py` | §22 freeboard + hypsometry + volume | `99972920…b2fa` |
| `area_fraction_attractor_screen.py` | §23 percolation attractor; R2 | `bfd00bd9…2cb0` |
| `no_tuning_falsifier_screen.py` | §27 NT-1/NT-2 falsifier surface | `e50d212e…9fac` |
| `continental_rheology_screen.py` | §24 coherence lifts f toward the ceiling | `a8badd89…4226` |
| `continental_yield_screen.py` | §24 yield rheology falsified as the closer | `a4683e2f…ede9` |
| `percolation_connectivity_screen.py` | §25 ceiling is z-dependent | `49a92b6c…9f98` |
| `plate_connectivity_screen.py` | §26 plate network z ≈ 6 → 0.41 not forced | `c34e8ada…025b` |

## Verify in five minutes (offline, no network)

```bash
cd repro
for s in *.py; do python3 "$s" | tail -1; done   # expect 23x REPRO GATE: PASS
```

Integrity of the whole tree, from the package root:

```bash
sha256sum -c MANIFEST.sha256   # expect: all OK
```

## The genuine computational-reproducibility caveat

One quantity has a real reproducibility obstacle and is graded accordingly. The area-fraction **value** from the fully-coupled high-Rayleigh-number run is computationally bounded: at the strongly-supercritical Ra = 10⁴, a 64×64×12 grid is numerically stable only for a finite window (~7000 steps) — even the q = 0 baseline eventually blows up — so the long-time limit is the under-resolved convection, not the coupling. A fully-converged long run needs higher resolution or implicit / hyperviscous / adaptive-time-step stabilisation. The coupled solver, driver, and recorded run are shipped in `repro/simulations_session/` so the bound is reproducible even though the converged value is not. The area-fraction value is therefore reported as a bracket, not a point, and graded **[O]** for the exact value (§26).

## Why the [O] grades are not reproducibility failures

This volume's **[O]** grades are an *epistemic* cap, not a computational one: occurrence, rate, magnitude, order, and absolute date are held [O] **by construction of the firewall** (§1), for and against, regardless of how reproducible any number is. They are not entries in a calculation-blocked ledger; they are quantities the constitution forbids from carrying the argument. The one exception that *is* a computational limit — the coupled area-fraction value — is stated above. Everything load-bearing is present-tense and reproducible."""

# ======================================================================================
# Chapter table.  kind: "module" | "doc" | "inline" | "module+extra".
# cards: locked-quantity ids surfaced in that chapter (first-use).  inherits: show strip.
# ======================================================================================
def MP(name):
    return MOD / name

CHAPTERS = [
    dict(n=1, id="ch1", title="The question and the firewall", kind="inline", src=CH1_MD,
         answer=("This volume asks why light, emergent dry land exists at all, and answers "
                 "<b>composition + buoyancy, not age</b>, under a bidirectional chronology firewall that caps every "
                 "occurrence, rate, and absolute date at [O] in both directions \u2014 so only present-tense, "
                 "non-rate observables carry the argument."),
         cards=["firewall"], inherits=False, screen=None, gate=None),

    dict(n=2, id="ch2", title="Inheritance and the engine", kind="module+extra",
         src=MP("01_inheritance_and_engine.md"), extra=CH2_EXTRA_MD,
         answer=("The volume <b>inherits, does not re-derive</b>, the R19 jammed\u21c4unjammed bistable switch and the "
                 "c\u00b2 = B/\u03c1 marginal substrate; on a fixed-area sphere an opening face and a compression face "
                 "are one motion, two ledgers \u2014 no new mechanism per phenomenon."),
         cards=["r19_switch", "c2_brho"], inherits=True),

    dict(n=3, id="ch3", title="The two-tier crust: why dry land and ocean basins coexist",
         kind="module", src=MP("02_thesis_two_tier_origin.md"),
         answer=("Dry land and ocean basins coexist <b>only</b> because the crust is two-tier: felsic continents "
                 "(~2.8 g cm\u207b\u00b3) float high and the basaltic ocean skin (~2.9) floats low over mantle (~3.3). "
                 "\u201cWhy dry land\u201d is therefore how light felsic crust is made and kept at the surface \u2014 a "
                 "composition question, not an age question."),
         cards=["two_tier_crust"], inherits=False),

    dict(n=4, id="ch4", title="Submarine extension, the mantle skin, and basin subsidence",
         kind="module", src=MP("03_extension_skin_and_basin.md"),
         answer=("From a water-covered start, a rift opens and its centre founders into a deep basin floored by "
                 "upwelled mantle skin (observed as seafloor spreading, [V]). The ocean floor is the mantle's thin, "
                 "chemically-basaltic, transient skin \u2014 subducted within ~200 Myr \u2014 not a permanent crust; "
                 "the Moho records the basalt/mantle contrast."),
         cards=[], inherits=False),

    dict(n=5, id="ch5", title="The compressional face: folding and thickening",
         kind="module", src=MP("04_compression_face_buckling.md"),
         answer=("Folding is compression \u2014 the opposite ledger of the opening \u2014 and it is feasible: the "
                 "lateral stress to buckle a 30 km skin falls with wavelength (614 MPa at 300 km \u2192 154 MPa at "
                 "600 km). The \u201chuge push\u201d becomes a stress threshold; its magnitude and rate stay [O]."),
         cards=["buckling_bar"], inherits=False),

    dict(n=6, id="ch6", title="Heat to granite: the wet partial-melting step",
         kind="module", src=MP("05_heat_to_granite_wet_remelt.md"),
         answer=("This is the heart of the volume: a buried, heated, <b>wet</b> pile partially melts and distils a "
                 "light felsic fraction that freezes as granite. Water is decisive \u2014 solidus ~650 \u00b0C wet vs "
                 "~950 \u00b0C dry \u2014 and the submarine start supplies it. Continent-scale felsic via pure "
                 "extension alone is only [L]."),
         cards=["wet_solidus"], inherits=False),

    dict(n=7, id="ch7", title="Buoyancy, accumulation, and emergence",
         kind="module", src=MP("06_buoyancy_emergence_isostasy.md"),
         answer=("Once made, felsic is too light to re-sink and accumulates as permanent crust; emergence then needs "
                 "<b>no special lift</b>. By Airy balance a 2.8 g cm\u207b\u00b3, 35 km column stands 4.45 km above "
                 "the ocean-crust top \u2014 the basin subsides and land follows. The Moho asymmetry (~7 vs ~35 km) is "
                 "the consistent configuration."),
         cards=["airy_freeboard"], inherits=False),

    dict(n=8, id="ch8", title="The zircon clock: understanding and the one valid caveat",
         kind="module", src=MP("07_zircon_understanding_and_caveat.md"),
         answer=("This volume does <b>not</b> claim the 4 Ga U-Pb ages are fake \u2014 the thermal-reset route fails "
                 "by ~8\u201311 orders on its own constants, uses circular data, and violates the firewall. It keeps "
                 "only the valid caveat that an isochron age is non-unique (a mixing line is algebraically identical "
                 "to an isochron), which supports the firewall and is never load-bearing for \u201cyoung.\u201d"),
         cards=["isochron_nonunique"], inherits=False),

    dict(n=9, id="ch9", title="Buoyant load gates compression: why the deep floor stays smooth",
         kind="module", src=MP("08_buoyant_load_gates_compression.md"),
         answer=("The smooth deep ocean floor and the crumpled, felsic-loaded land are one buoyancy gate: net "
                 "buoyancy B = \u03a3(\u03c1_asth\u2212\u03c1_i)h_i decides the response. Net-negative old ocean skin "
                 "sheds compression by subducting (smooth floor); net-positive felsic cannot sink and must crumple. "
                 "One engine, but degenerate as a discriminator."),
         cards=["buoyancy_gate"], inherits=False),

    dict(n=10, id="ch10", title="The buoyancy sign-flip and the breaker",
         kind="module", src=MP("09_cg22_signflip_and_breaker.md"),
         answer=("Half-space cooling flips the ocean skin's net buoyancy at t* \u2248 11 Ma (~3.7 km depth), so most "
                 "deep floor is net-negative. But the central Indian Ocean \u2014 old, net-negative skin folding "
                 "<b>without</b> subducting \u2014 falsifies the gate's strong form. Surviving claim: thick relief "
                 "needs felsic load; bare skin folds only long-\u03bb/low-amplitude. CG-22 [F]\u2192[L]."),
         cards=["signflip_age"], inherits=False),

    dict(n=11, id="ch11", title="The isostatic-compensation law",
         kind="module", src=MP("10_isostatic_compensation_law.md"),
         answer=("Maximum compensated relief needs a deep light root: h_max \u2248 \u0394H(\u03c1_m\u2212\u03c1_c)/"
                 "(\u03c1_m\u2212\u03c1_top). Normal 7 km basalt skin, even doubled, caps at ~1 km; felsic collision "
                 "reaches ~5 km. The single present-tense test is free-air gravity + Moho depth, verified against the "
                 "central Indian Ocean (capped) and Gorringe Bank (uncompensated)."),
         cards=["compensation_law"], inherits=False),

    dict(n=12, id="ch12", title="The mantle is a jammed solid near unjamming, not magma",
         kind="module", src=MP("11_mantle_jamming_state.md"),
         answer=("The heavy fluid that lets the deep floor flatten is a <b>jammed solid near unjamming</b> "
                 "(T/T_solidus ~0.7\u20130.95) \u2014 it flows on Myr but transmits S-waves (\u03bc>0, solid) and is "
                 "~10\u00b9\u2075\u201310\u00b9\u2079\u00d7 more viscous than magma. Magma is the local unjammed state; "
                 "\u201cbulk magma mantle\u201d is falsified by the S-wave shadow at the core."),
         cards=["jamming_state", "c2_brho"], inherits=False),

    dict(n=13, id="ch13", title="Present-state synthesis: a convecting interior under a frozen, asymmetric lid",
         kind="module", src=MP("12_present_state_synthesis.md"),
         answer=("The present state is mantle convection (Ra \u2248 5.85\u00d710\u2076 \u226b critical, [F]) under a "
                 "cooled rigid lid ([V]), driven by a slow but continuous heat engine (~46 TW; quasi-steady on Myr). "
                 "Coherent but degenerate. The one non-degenerate edge is the hemispheric asymmetry: ~81% of land in "
                 "one hemisphere, with no settled mainstream \u201cwhy.\u201d"),
         cards=[], inherits=False),

    dict(n=14, id="ch14", title="Where the thesis really diverges: the origin, not the asymmetry",
         kind="module", src=MP("13_where_it_diverges_origin.md"),
         answer=("As a discriminator the hemispheric asymmetry is <b>degenerate</b> (Pacific = the persistent "
                 "Panthalassa; continents reconfigure; the asymmetry is fading), so it is demoted. The real "
                 "divergence is the <b>origin</b> \u2014 why felsic crust exists at all (CG-12) \u2014 tested by the "
                 "arc geochemical signature, which currently leans mainstream."),
         cards=[], inherits=False),

    dict(n=15, id="ch15", title="Firewall self-audit: where imported interpretation was scored as data",
         kind="module", src=MP("14_firewall_self_audit.md"),
         answer=("A self-audit found seven breaches where a dataset's <b>chronological reading</b> (age progression, "
                 "deep-time sequence, secular rate) was scored as present-tense fact \u2014 mostly against the thesis. "
                 "Corrected: keep the present-tense geometry as [V], demote the imported chronology to [O]. The net "
                 "effect is that the thesis is <b>less penalized, not validated</b>."),
         cards=[], inherits=False),

    dict(n=16, id="ch16", title="Assembling the causal chain: opening to a one-sided mass",
         kind="module", src=MP("15_assembly_causal_chain.md"),
         answer=("From data and pure physics alone \u2014 no clock, no geological history \u2014 an opening on a "
                 "fixed-area sphere (A = 5.101\u00d710\u00b9\u2074 m\u00b2) forces antipodal closing (conservation), the "
                 "skin subducts while the buoyant raft cannot (buoyancy), and the raft collects at the sink "
                 "(kinematics): a one-sided felsic mass is entailed. A dependency graph, not a timeline; first seed, "
                 "trigger, welding, rate, and order stay [O]."),
         cards=["assembly_entailment"], inherits=False),

    dict(n=17, id="ch17", title="Why one side: inheriting the symmetry-breaking capacity",
         kind="module", src=MP("16_symmetry_breaking_and_band.md"),
         answer=("Why one side? A marginal jammed substrate (relaxed shear \u2192 0, c\u00b2=B/\u03c1) has no restoring "
                 "force against a transport perturbation, so a symmetry break is permitted \u2014 even favoured \u2014 "
                 "not forbidden [F]. Inevitability, side, count, and timing stay [O] (\u201cnot opposed\u201d \u2260 "
                 "\u201cforced\u201d). The \u201clong band\u201d geometry is not established, and magnetic body-force "
                 "steering of continents is disfavoured."),
         cards=["marginal_substrate"], inherits=False),

    dict(n=18, id="ch18", title="The mid-Pacific upwelling cell (typhoon analogue)",
         kind="module", src=MP("17_upwelling_cell_hypothesis.md"),
         answer=("Energy supplied from below forces a bottom-heated rotating cell to vent up at the axis and spread "
                 "at the top \u2014 it cannot sink to the core (reductio). Buoyancy supplies the lift [L]; inherited "
                 "co-rotation (C\u2083 \u2192 merge \u2192 Ekman) forces the organizing vortex and convergent feed [F]; "
                 "base-inflow and centre-uprise are one loop. Vent fixity and the equatorial/centrifugal bias "
                 "(0.34% g) stay [O]/[L]."),
         cards=["ekman_inflow"], inherits=False),

    dict(n=19, id="ch19", title="Standing synthesis: the spine that holds and the tasks by leverage",
         kind="module", src=MP("18_standing_synthesis_and_open_problems.md"),
         answer=("Stepping back: an eight-link present-tense [F]/[V] spine holds \u2014 from a hot near-unjamming "
                 "mantle to one-sided dry land \u2014 importing no deep time anywhere. Everything is conditional on "
                 "felsic existing, routing through one structural gap (CG-12 felsic scale / CG-20 first seed). The "
                 "tasks are ranked by leverage; the next decisive build is the felsic-scale fork."),
         cards=[], inherits=False),

    dict(n=20, id="ch20", title="The granite map vs the limestone map: two faces of one engine",
         kind="module", src=MP("19_granite_carbonate_dichotomy.md"),
         answer=("The granite map and the limestone map are the two faces of one rupture engine: granite is a deep "
                 "wet-melt at compression (bottom-up, convergent belts; Korea, Andes), limestone a surface "
                 "precipitate at extension (top-down, passive shelves). This resolves CG-12 by splitting it \u2014 "
                 "continent-scale felsic tracks the convergent wet path \u2014 while VP's claim that the convergence "
                 "is the antipodal closing face of a primordial rupture survives."),
         cards=[], inherits=False),

    dict(n=21, id="ch21", title="Closing the loop: the big problem dissolves",
         kind="module", src=MP("20_closed_loop_dissolution.md"),
         answer=("The \u201cbig remaining problem\u201d \u2014 the origin of the convergence \u2014 dissolves. A hot "
                 "fluid sphere must convect (Ra \u2248 5.85\u00d710\u2076 \u226b critical); closed-sphere convection has "
                 "up- and down-limbs by conservation, so the convergence <b>is</b> the downwelling limb, not a "
                 "separate assumption. The first seed largely dissolves too. What remains is a number (R1) and an "
                 "identity (R2), not a mechanism gap."),
         cards=["downwelling_convergence"], inherits=False),

    dict(n=22, id="ch22", title="R1: the quantitative budget",
         kind="module", src=MP("21_r1_quantitative_budget.md"),
         answer=("R1 \u2014 does the loop distil the observed crust? \u2014 is reformulated as a present-tense fixed "
                 "point so no duration enters. Isostasy + the measured ocean water volume reproduces the observed "
                 "freeboard (textbook \u03c1_c=2800 overshoots to +1915 m; the measured bulk value lands at +840 m), "
                 "the bimodal hypsometry (separation ~5.2 km), and a sustainable steady-state volume (P/D ~ O(1)) "
                 "\u2014 with no fitted parameter and no deep-time curve."),
         cards=["freeboard_fixedpoint", "bimodal_hypsometry"], inherits=False),

    dict(n=23, id="ch23", title="The area fraction as a marginal-connectivity attractor",
         kind="module", src=MP("22_area_fraction_attractor.md"),
         answer=("The remaining number \u2014 the ~40% area fraction \u2014 is a self-organized marginal-connectivity "
                 "(percolation) attractor of the complementary ocean network (planar f* \u2248 0.407): a fragmenting "
                 "ocean throttles its own subduction. On a validated 3D Boussinesq solver (Ra_c \u2248 657.5) the "
                 "attractor survives but is coupling-sensitive; the two-way-coupled run settles ~0.30, not 0.41. R2: "
                 "substrate, freeboard, and area are three faces of the c\u00b2=B/\u03c1 kernel."),
         cards=["percolation_attractor", "ra_onset", "three_margins"], inherits=False),

    dict(n=24, id="ch24", title="Continental coherence (rheology) vs the area fraction: CG-39",
         kind="module", src=MP("23_continental_rheology.md"),
         answer=("The 0.30\u21920.41 residual is tested, not hand-waved. Continental coherence (a real rheology, "
                 "\u03ba scanned not tuned) lifts the stirred fraction toward the ceiling \u2014 recovering ~75% of the "
                 "gap but saturating ~0.38 \u2014 and cannot exceed it. The v1.5 conjecture that a true yield rheology "
                 "closes the gap is implemented and <b>falsified</b>: rigid rafts saturate ~0.34. The percolation "
                 "ceiling is the binding bound, approached but not reached from below."),
         cards=[], inherits=False),

    dict(n=25, id="ch25", title="The percolation ceiling is connectivity-dependent",
         kind="module", src=MP("24_percolation_geometry.md"),
         answer=("The percolation ceiling is not universal \u2014 it depends on coordination z: f* \u2248 0.41 (z=4) "
                 "\u2192 0.50 (z=6) \u2192 0.61 (z=8). So 0.41 is the z=4 value the grid happened to use, and reaching "
                 "it is <b>not</b> a missing-convection-physics gap. The match to observation becomes a falsifiable "
                 "empirical claim about the real ocean network's connectivity, which downgrades the certainty of the "
                 "value."),
         cards=[], inherits=False),

    dict(n=26, id="ch26", title="CG-39 closeout: the plate network is ~6-connected",
         kind="module", src=MP("25_plate_connectivity.md"),
         answer=("Exact topology decides it: a sphere of F plates with triple junctions gives mean coordination "
                 "z = 6 \u2212 12/F \u2248 5\u20136, so the natural-network ceiling f* \u2248 0.46\u20130.50 overshoots "
                 "observed 0.41. The fraction is therefore regime-right (a percolation-bounded sub-majority "
                 "~0.4\u20130.5, kernel-fixed, [L]) but the exact 0.41 is not uniquely forced ([O], within a "
                 "~0.30\u20130.50 bracket). CG-39 closes: regime-yes, exact-value-no."),
         cards=["percolation_z"], inherits=False),

    dict(n=27, id="ch27", title="The no-tuning thesis: one kernel, no fitted parameter",
         kind="doc", src=ROOT / "NO_TUNING_THESIS.md",
         answer=("The full chain derives from one inherited kernel (c\u00b2=B/\u03c1, R19 switch) with <b>no fitted "
                 "parameter</b> (NT-1) and <b>no per-stage added mechanism</b> (NT-2). NT-1 is structural because the "
                 "firewall removes the one tunable knob \u2014 duration; NT-2's strongest evidence is a subtraction "
                 "(the convergence is the forced downwelling limb, not an extra posit). The architecture is "
                 "constrained and breakable, not confirmed."),
         cards=[], inherits=False),

    dict(n=28, id="ch28", title="The puzzle map: open problems vs the hypothesis",
         kind="doc", src=ROOT / "PUZZLE_MAP.md",
         answer=("Surveyed against real open problems, the hypothesis gains only from <b>non-degenerate edges</b> and "
                 "from <b>surviving the present-tense strains</b> \u2014 not from enumerating wins. The map shows "
                 "~3\u20134 genuine edges (hemispheric asymmetry, freeboard constancy, tectonic mode), ~12 degenerate "
                 "items that are NOT evidence, ~7 shared gaps it does not solve, and 6 strain items that test it."),
         cards=[], inherits=False),

    dict(n=29, id="ch29", title="Reproducibility and openness ledger", kind="inline", src=CH29_MD,
         answer=("Every quantitative claim is regenerated by a self-contained, deterministic (SEED=19) screen that "
                 "prints REPRO GATE: PASS and is checked against a double-SHA-256 gate \u2014 23 in all, verifiable "
                 "offline in five minutes. One value (the coupled high-Ra area fraction) has a genuine computational "
                 "limit and is bracketed; the [O] grades are firewall caps, not reproducibility failures."),
         cards=[], inherits=False),

    dict(n=30, id="ch30", title="The graded ledger (CG-1 \u2026 CG-39 + AUDIT-1)",
         kind="doc", src=ROOT / "BLUEPRINT_and_GRADED_LEDGER.md",
         answer=("The complete row-by-row record, CG-1 \u2026 CG-39 + AUDIT-1, with each sub-hypothesis at its honest "
                 "grade and its location. Precedence [F] > [V] > [L] > [O]; nothing downstream launders an [O] "
                 "upward; superseded rows are kept (mark-never-erase)."),
         cards=[], inherits=False),
]


# ======================================================================================
# Assembly
# ======================================================================================
def chapter_claim_strip(screen, gate):
    bits = ['<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>']
    if screen:
        bits.append('<a href="repro/%s">screen: %s</a>' % (screen.split("/")[-1], _esc(screen.split("/")[-1])))
    if gate:
        bits.append('<span class="gate">gate %s\u2026%s</span>' % (gate[:8], gate[-4:]))
    bits.append('<a href="https://doi.org/%s">DOI snapshot</a>' % DOI_THIS)
    return '<aside class="claim-strip">' + "".join(bits) + "</aside>"


def render_chapter(ch):
    n = ch["n"]
    secno = "\u00a7%d" % n
    body_html = ""
    screen = ch.get("screen")
    gate = ch.get("gate")

    if ch["kind"] == "inline":
        body_html = render_module_body(n, ch["src"])
    elif ch["kind"] == "doc":
        body_html = render_doc_body(n, ch["src"])
    elif ch["kind"] == "module":
        body, screen, gate = parse_module(ch["src"])
        body_html = render_module_body(n, body)
    elif ch["kind"] == "module+extra":
        body, screen, gate = parse_module(ch["src"])
        body_html = render_module_body(n, body)
        # number the extra sub-chapters continuing after the module's sub-chapters
        nsub = body_html.count('class="subchapter"')
        extra_parts = re.split(r"\n## ", "\n" + ch["extra"])
        extra_html = []
        sub = nsub
        for p in extra_parts:
            p = p.strip()
            if not p:
                continue
            line, _, inner = p.partition("\n")
            title = line.strip().lstrip("# ").strip()
            sub += 1
            extra_html.append(
                '<section class="subchapter" id="ch%d-%d"><h3><span class="sn">\u00a7%d.%d</span>%s</h3>%s</section>'
                % (n, sub, n, sub, _inline(_esc(title)), md_to_html(inner.strip())))
        body_html += "\n".join(extra_html)

    cards = "".join(vp_card(c) for c in ch.get("cards", []))
    strip = chapter_claim_strip(screen, gate) if (screen or gate or ch["kind"] != "inline") else ""
    inh = inherits_strip() if ch.get("inherits") else ""
    return (
        '<section class="chapter" id="%s">'
        '<span class="secno">%s</span>'
        '<h2>%s</h2>'
        '<p class="answer">%s</p>'
        '%s%s%s%s'
        '</section>'
    ) % (ch["id"], secno, _inline(_esc(ch["title"])), ch["answer"], strip, inh, cards, body_html)


def build_toc():
    items = []
    for ch in CHAPTERS:
        items.append('<li><a href="#%s">\u00a7%d. %s</a></li>' % (ch["id"], ch["n"], _esc(ch["title"])))
    items.append('<li><a href="#modules">Appendix A. Inherited modules</a></li>')
    items.append('<li><a href="#concepts">Appendix B. Concepts glossary</a></li>')
    return ('<nav class="toc" aria-label="Contents"><h2>Contents</h2><ol>%s</ol></nav>'
            % "".join(items))


def build_spine_box():
    spine = [
        ("Two-tier crust \u21d2 dry land exists", "ch3", "V"),
        ("Hot near-unjamming mantle = heavy fluid", "ch12", "F"),
        ("Energy-from-below + rotation \u21d2 forced up-and-out vent", "ch18", "F"),
        ("Marginal substrate permits the symmetry break", "ch17", "F"),
        ("Opening \u21d2 a one-sided felsic mass is forced", "ch16", "F"),
        ("Compression feasible + buoyancy-gated; bare skin stays smooth", "ch9", "F"),
        ("A wet pile distils granite", "ch6", "F"),
        ("Emergence by basin subsidence", "ch7", "F"),
    ]
    lis = "".join('<li><a href="#%s">%s</a> %s</li>' % (a, _esc(t), grade_badge(g)) for t, a, g in spine)
    return ('<div><h2 style="font-size:1.18rem;margin:2rem 0 .4rem">The spine that holds '
            '<small>(present-tense, firewall-clean)</small></h2>'
            '<ol class="spine">%s</ol>'
            '<p style="font-size:.92rem;color:var(--ink-soft)">A connected, chronology-free chain from hot fluid '
            'mantle to one-sided dry land \u2014 each link forced or measured (\u00a719). The one structural gap is '
            'that all of it is conditional on felsic existing (\u00a720\u2013\u00a721 dissolve it in direction); the '
            'one quantitative residual is the area-fraction value (\u00a723\u2013\u00a726).</p>') % lis


def build_modules_appendix():
    out = ['<section class="chapter" id="modules"><span class="secno">Appendix A</span>'
           '<h2>Inherited common modules</h2>'
           '<p class="answer">This volume inherits two common modules from the shared core and re-derives neither: '
           'the <b>R19 jamming kernel</b> (c\u00b2=B/\u03c1, the bistable switch) and the <b>three-rotor '
           'co-rotation / Ekman inflow</b> motif. Each is stated in full so the chain is legible without the source '
           'packages.</p>']
    for mid, m in MODULES.items():
        forces = "; ".join(m["forces"])
        out.append(
            '<div class="term" id="module-%s"><div class="head">%s <span class="g g-%s">[%s]</span></div>'
            '<div class="body">%s</div>'
            '<div class="body"><b>Forces:</b> %s</div>'
            '<div class="meta">reach: %s \u00b7 inherited from <a href="%s">canonical source</a></div></div>'
            % (mid, _esc(m["name"]), m["grade"], m["grade"], _inline(_esc(m["statement"])),
               _inline(_esc(forces)), _esc(m["reach"]), m["canonical"]))
    out.append('</section>')
    return "".join(out)


def build_concepts_appendix():
    out = ['<section class="chapter" id="concepts"><span class="secno">Appendix B</span>'
           '<h2>Concepts glossary <small>(locked quantities)</small></h2>'
           '<p class="answer">Every locked quantity the argument cites, each a self-contained defined term: value, '
           'one-line statement, grade, owner, and a link to its canonical derivation. Terms owned by this volume are '
           'marked; the rest are inherited from the sibling volumes named.</p>']
    # owned first, then inherited
    order = [c for c in CONCEPTS if c["owner"] == PAPER_ID] + [c for c in CONCEPTS if c["owner"] != PAPER_ID]
    for c in order:
        owned = c["owner"] == PAPER_ID
        own_lbl = "owned here" if owned else ("inherited \u00b7 " + c["owner"])
        out.append(
            '<div class="term" id="concept-%s"><div class="head"><span class="sym">%s</span> %s '
            '<span class="g g-%s">[%s]</span></div>'
            '<div class="body">%s</div>'
            '<div class="meta">%s \u00b7 <a href="%s">derivation</a></div></div>'
            % (c["id"], _esc(c["symbol"]), _esc(c["term"]), c["grade"], c["grade"],
               _inline(_esc(c["statement"])), own_lbl, c["href"]))
    out.append('</section>')
    return "".join(out)


def jsonld_blocks():
    article = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": "Continental Genesis: why dry land exists",
        "isPartOf": {"@type": "CreativeWorkSeries", "name": "Jamming Physics",
                     "identifier": "https://doi.org/" + DOI_THIS},
        "author": {"@type": "Person", "name": "Young Jae Lee", "sameAs": ORCID},
        "identifier": "https://doi.org/" + DOI_THIS,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "isBasedOn": REPO,
        "inLanguage": "en",
        "knowsAbout": ["jamming lattice", "marginal-substrate elastic-wave law c^2=B/rho",
                       "continental crust origin", "isostasy and freeboard",
                       "percolation area-fraction attractor", "wet partial melting", "mantle convection"],
        "abstract": re.sub("<[^>]+>", "", ABSTRACT),
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jamming-physics.org/"},
            {"@type": "ListItem", "position": 2, "name": "Continental Genesis", "item": HUB},
        ],
    }
    termset = {
        "@context": "https://schema.org", "@type": "DefinedTermSet",
        "name": "Continental-Genesis locked quantities",
        "url": HUB + "#concepts",
        "hasDefinedTerm": [
            {"@type": "DefinedTerm", "name": c["term"], "termCode": c["id"],
             "description": re.sub("<[^>]+>", "", c["statement"])} for c in CONCEPTS
        ],
    }
    return "\n".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(b, ensure_ascii=False)
        for b in (article, crumbs, termset))


def build_html():
    today = datetime.date.today().isoformat()
    chapters_html = "\n".join(render_chapter(ch) for ch in CHAPTERS)
    head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Continental Genesis: why dry land exists | Jamming Physics</title>
<meta name="description" content="Why a two-tier crust and dry land exist: light felsic continents distilled by water-fluxed melting on the downwelling face of a convecting mantle, from one c2=B/rho jamming kernel, no fitted parameter. 25 modules, 23 gated screens, honestly graded.">
<link rel="canonical" href="{hub}">
<meta name="author" content="Young Jae Lee">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
{jsonld}
<style>{css}</style>
</head>
<body>
<div class="wrap">
<nav class="crumb"><a href="https://jamming-physics.org/">Home</a> &rsaquo; <a href="{hub}">Continental Genesis</a> &rsaquo; whitepaper</nav>
<header class="masthead">
  <p class="eyebrow">VP \u00b7 Continental-Genesis volume \u00b7 VP-SPEC v1.9 canonical</p>
  <h1>Continental Genesis: why dry land exists</h1>
  <p class="byline"><b>Young Jae Lee</b> \u00b7 ORCID <a href="{orcid}">0009-0002-7535-8245</a> \u00b7 CC BY 4.0 \u00b7 <a href="https://jamming-physics.org/">jamming-physics.org</a><br>
  Inherited: VP physics <a href="https://doi.org/{dphy}">DOI 10.5281/zenodo.17932566</a> \u00b7 Atlantic geodynamics <a href="https://doi.org/{dgeo}">DOI 10.5281/zenodo.17978934</a> \u00b7 Configured Continuum <a href="https://doi.org/{dflu}">DOI 10.5281/zenodo.17972568</a></p>
  <p class="motto">Motto: <b>falsification = discovery</b>.</p>
</header>

<p class="answer">{answer}</p>
<p class="abstract">{abstract}</p>

<aside class="claim-strip">
  <span class="gate">LOCK \u2192 Derive \u2192 Gate</span>
  <a href="repro/">reproduction (23 gated screens)</a>
  <a href="MANIFEST.sha256">integrity manifest</a>
  <a href="https://doi.org/{dthis}">DOI snapshot</a>
</aside>
{inherits}
{spine}
{toc}
""".format(hub=HUB, orcid=ORCID, dphy=DOI_PHYSICS, dgeo=DOI_GEODYN, dflu=DOI_FLUID, dthis=DOI_THIS,
           jsonld=jsonld_blocks(), css=SITE_CSS, answer=FRONT_ANSWER, abstract=ABSTRACT,
           inherits=inherits_strip(), spine=build_spine_box(), toc=build_toc())

    foot = """
{modules}
{concepts}
<footer>
  <p><b>Continental Genesis</b> \u2014 a composition-and-buoyancy account of why dry land exists, built on the VP jamming engine. A seed, built to grow. Everything dated stays RECORD; everything that happened stays <b>[O]</b>; only mechanisms and present-tense observables carry the argument.</p>
  <p>Young Jae Lee \u00b7 ORCID <a href="{orcid}">0009-0002-7535-8245</a> \u00b7 licensed <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a> \u00b7 living version: <a href="{hub}">{hub}</a> \u00b7 DOI <a href="https://doi.org/{dthis}">{dthis}</a></p>
  <p><small>This canonical HTML was generated deterministically from the package modules by <code>tools/build_canonical_html.py</code> (VP-SPEC v1.9; Constitution C1\u2013C5). Built {today}. No content condensed \u2014 the full prose of all 25 modules and the supporting documents is carried, re-organised into numbered sub-chapters. Motto: falsification = discovery.</small></p>
</footer>
</div>
</body>
</html>""".format(modules=build_modules_appendix(), concepts=build_concepts_appendix(),
                  orcid=ORCID, hub=HUB, dthis=DOI_THIS, today=today)

    return head + chapters_html + foot


# ======================================================================================
# Emit
# ======================================================================================
def emit():
    html_doc = build_html()
    # stray-Hangul guard (Constitution: English only; the masthead motto signature is allowed)
    stray = re.findall(r"[\uac00-\ud7a3]", html_doc)
    if stray:
        raise SystemExit("BUILD ABORTED: %d Hangul codepoint(s) in output; this volume is English-only." % len(stray))

    out_html = ROOT / "WHITEPAPER.html"
    out_html.write_text(html_doc, encoding="utf-8")

    docs = ROOT / "docs"
    (docs / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (docs / "registry").mkdir(parents=True, exist_ok=True)

    (docs / "assets" / "css" / "site.css").write_text(SITE_CSS.strip() + "\n", encoding="utf-8")

    # ---- _meta.json (SPEC section 9 summary card) ----
    grade_counts = {"forced": 0, "verified": 0, "leaning": 0, "open": 0}
    meta = {
        "paper_id": PAPER_ID, "code": "cge",
        "title": "Continental Genesis: why dry land exists",
        "short": "Continental Genesis",
        "doi": DOI_THIS, "hub_url": HUB, "branch": "convergence",
        "abstract": re.sub("<[^>]+>", "", ABSTRACT),
        "headline_results": ["composition + buoyancy, not age", "freeboard +840 m (measured, no fit)",
                             "convergence = downwelling limb (Ra \u2248 5.85\u00d710\u2076)",
                             "area fraction = percolation-bounded ~0.4\u20130.5"],
        "chapters": [{"no": ch["n"], "id": ch["id"], "title": ch["title"]} for ch in CHAPTERS],
        "totals": {"chapters": len(CHAPTERS), "screens": 23, "modules_source": 25,
                   "ledger_rows": "CG-1\u2026CG-39 + AUDIT-1"},
        "canonical_html": "WHITEPAPER.html",
        "generated": datetime.date.today().isoformat(),
    }
    (docs / "_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- _decl.json (SPEC section 6-M.1 incorporation declaration) ----
    decl = {
        "paper_id": PAPER_ID, "tier": 5,
        "inherits_volumes": ["physics", "geodynamics", "fluid-dynamics"],
        "inherits_modules": list(MODULES.keys()),
        "adds": ["continental-genesis = two-face rupture distillation of felsic crust (opening floors a basin; "
                 "the antipodal downwelling/compression face flux-melts hydrated skin to granite)"],
        "primitives": ["R19", "jammed_c2", "emergence", "conservation_fixed_area", "buoyancy_sign", "percolation"],
        "owns_terms": OWNS,
        "uses_terms": USES,
        "grades": {"forced": "see ledger", "verified": "see ledger", "leaning": "see ledger", "open": "see ledger",
                   "note": "occurrence/timing capped at [O] by the firewall; per-row grades in BLUEPRINT ledger"},
    }
    (docs / "_decl.json").write_text(json.dumps(decl, ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- registry/concepts.json + modules.json (C5 SSOT) ----
    (docs / "registry" / "concepts.json").write_text(
        json.dumps({"schema": "vp.concepts/0.1", "owner_volume": PAPER_ID, "terms": CONCEPTS},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (docs / "registry" / "modules.json").write_text(
        json.dumps({"schema": "vp.modules/0.1", "inherited_by": PAPER_ID, "modules": MODULES},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    # ---- llms.txt (<5KB retrieval helper) ----
    llms = (
        "# Continental Genesis \u2014 why dry land exists (VP jamming physics)\n\n"
        "> Dry land exists by composition + buoyancy, not age: continents are light felsic crust distilled by "
        "water-fluxed partial melting on the downwelling/compression face of a convecting mantle, too light to "
        "re-sink, emergent by basin subsidence. From one c\u00b2=B/\u03c1 jamming kernel, no fitted parameter. "
        "Occurrence/timing stays [O] forever. Motto: falsification = discovery.\n\n"
        "## Core\n"
        "- Canonical whitepaper: WHITEPAPER.html (single self-contained file; \u00a71\u2013\u00a730 + appendices)\n"
        "- Constitution/firewall + grading [F]/[V]/[L]/[O]: WHITEPAPER.html#ch1 ; GOVERNANCE.md\n"
        "- Inheritance (c\u00b2=B/\u03c1, R19 switch): WHITEPAPER.html#ch2 ; inherited/INHERITED_RESULTS_CARD.md\n\n"
        "## Research (the spine, present-tense [F]/[V])\n"
        "- Two-tier crust \u2192 dry land: #ch3 ; wet melt \u2192 granite: #ch6 ; emergence by subsidence: #ch7\n"
        "- Buoyancy gate / smooth deep floor: #ch9 ; compensation law: #ch11 ; mantle jamming state: #ch12\n"
        "- Assembly (opening \u21d2 one-sided mass): #ch16 ; loop closes (convergence = downwelling limb): #ch21\n"
        "- R1 budget (freeboard +840 m, hypsometry ~5.2 km): #ch22 ; area fraction percolation attractor: #ch23\n\n"
        "## Concepts (locked quantities)\n"
        "- Glossary: WHITEPAPER.html#concepts ; machine-readable: docs/registry/concepts.json\n\n"
        "## Reproducibility\n"
        "- 23 SEED=19 double-SHA-256 gated screens in repro/ ; verify offline: see WHITEPAPER.html#ch29\n"
        "- Integrity: MANIFEST.sha256\n\n"
        "## Policies\n"
        "- Firewall: absolute dates = RECORD, occurrence = [O] both ways. No fitted parameter. Mark, never erase.\n"
    )
    (docs / "llms.txt").write_text(llms, encoding="utf-8")

    size = out_html.stat().st_size
    print("WROTE WHITEPAPER.html  (%d bytes, %.0f KB)" % (size, size / 1024))
    print("WROTE docs/_meta.json, docs/_decl.json, docs/registry/{concepts,modules}.json, docs/llms.txt, "
          "docs/assets/css/site.css")
    print("chapters: %d  concepts: %d (owns %d / uses %d)  modules: %d"
          % (len(CHAPTERS), len(CONCEPTS), len(OWNS), len(USES), len(MODULES)))


if __name__ == "__main__":
    emit()
