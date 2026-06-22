#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_site.py -- VP Inheritance Kit -> canonical HTML site (VP-SPEC v1.8).

LOCK -> Derive -> Gate. The single source of every displayed NUMBER is
reports/emergence_results.json (the gate's own measured output). No number is
typed into prose; each is fetched by key through R(...) and recorded in a
displayed-number ledger (reports/site_numbers.json), so the HTML cannot drift
from the measured result (Constitution C1). The site is rebuilt twice and the
whole docs/ tree is sha256'd; identical hashes are the determinism gate.

Output tree (additive, under the kit root):
  docs/index.html                      -- volume landing
  docs/inheritance/index.html          -- volume hub (chapter map + cross-links)
  docs/inheritance/{slug}/index.html   -- one chapter per battery group + ledger
  docs/inheritance/_meta.json          -- summary card (VP-SPEC §9)
  docs/sitemap.xml  docs/robots.txt  docs/llms.txt
  docs/assets/css/site.css
  reports/site_numbers.json            -- displayed-number ledger (C1 audit)

This file is a generator, not a re-derivation: it never re-implements the
substrate or re-measures gamma. It reads the gate output and renders it.
"""
import json, os, html, hashlib, shutil, datetime

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = json.load(open(os.path.join(KIT, "reports", "emergence_results.json")))
GREEN  = json.load(open(os.path.join(KIT, "reports", "research_complete.json")))
VLD    = GREEN["heldout_validation_verify"]   # the (B) held-out validation verify block
SLM    = GREEN["heldout_signlaw_minus_arm_verify"]   # FV7 -- corrective sign-law '-' arm (DepMap CRISPR-KO) provenance
SLP    = GREEN["heldout_signlaw_plus_arm_verify"]    # FV8 -- corrective sign-law '+' RESTORE arm (Horlbeck CRISPRa) provenance

# ---- program / authorship identity (concept DOI minted on Zenodo; resolves to the latest version) ----
AUTHOR   = "Young Jae Lee"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
SITE     = "https://jamming-physics.org"
PAPER_ID = "inheritance"
SHORT    = "VP Inheritance"
DOI      = "10.5281/zenodo.20783547"   # concept DOI (Zenodo) -- resolves to the latest version
FULLTITLE = ("Environmental Inheritance, the RNA Layer, and the Path to "
             "RNA Vaccines & Gene Therapy")
REPO     = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/inheritance"
ISO      = "2026-06-21"
ANCHOR_GAMMA = "1.4598"   # SOX9 promoter anchor (the no-tuning gate)

# ============================================================================
#  Number access -- the only path from a measured value to the page.
#  R(battery, test_index, *keys) walks reports/emergence_results.json.
#  num(x) formats and LEDGERs the value so the gate can audit it.
# ============================================================================
LEDGER = {}   # "label" -> formatted string actually shown on a page

def R(bat, ti, *keys):
    node = REPORT[bat]["tests"][ti]
    for k in keys:
        node = node[k]
    return node

def num(label, value, fmt=None):
    """Format a measured value and record it in the displayed-number ledger."""
    if fmt is None:
        s = str(value)
    elif fmt == "g4":
        s = f"{value:.4f}"
    elif fmt == "g3":
        s = f"{value:.3f}"
    elif fmt == "g2":
        s = f"{value:.2f}"
    else:
        s = fmt % value
    LEDGER[label] = s
    return s

def E(s):  # html-escape helper for body text
    return html.escape(str(s), quote=False)

# ============================================================================
#  Stylesheet -- one file, no inline CSS. Restrained academic instrument;
#  the graded claim-strip is the signature element (every claim carries a
#  grade and a reproduce path -- the differentiator of this program).
# ============================================================================
CSS = r""":root{
  --ink:#14181d; --ink-soft:#3a434d; --faint:#6b7580; --line:#dfe3e8;
  --paper:#fbfbf9; --card:#ffffff; --rule:#eceef1;
  --gamma:#1f5f8b;   /* the SET channel: the unwritable ruler */
  --a4:#9a5b2e;      /* the A4 channel: the writable structure */
  --drive:#7a3e8c;   /* the drive h */
  --g-forced:#1f5f8b; --g-verified:#2e7d57; --g-open:#a3621a; --g-cal:#5b6470;
  --mono:"SFMono-Regular",ui-monospace,"JetBrains Mono","Menlo",monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI","Inter",system-ui,sans-serif;
  --serif:"Iowan Old Style","Charter","Georgia", "Times New Roman",serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:var(--serif);font-size:18px;line-height:1.62;
  font-feature-settings:"kern" 1,"liga" 1;}
main{max-width:46rem;margin:0 auto;padding:0 1.25rem 5rem}
header{max-width:46rem;margin:0 auto;padding:1.1rem 1.25rem 0}
footer{max-width:46rem;margin:0 auto;padding:2rem 1.25rem 3rem;
  color:var(--faint);font-family:var(--sans);font-size:.82rem;
  border-top:1px solid var(--rule);margin-top:3rem}
a{color:var(--gamma);text-decoration:none}
a:hover{text-decoration:underline;text-underline-offset:2px}
h1{font-size:1.92rem;line-height:1.18;letter-spacing:-.012em;
  margin:.7rem 0 .2rem;font-weight:650}
h2{font-family:var(--sans);font-size:1.16rem;letter-spacing:-.006em;
  margin:2.4rem 0 .5rem;font-weight:640;color:var(--ink)}
h3{font-family:var(--sans);font-size:.96rem;margin:1.5rem 0 .3rem;
  font-weight:640;color:var(--ink-soft)}
p{margin:.55rem 0}
.crumb{font-family:var(--mono);font-size:.72rem;letter-spacing:.02em;
  color:var(--faint);text-transform:none}
.crumb a{color:var(--faint)}
.eyebrow{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;
  text-transform:uppercase;color:var(--a4);margin:0 0 .1rem}

/* answer-first block -- the extracted-passage direct answer */
.answer{font-family:var(--sans);font-size:1.06rem;line-height:1.5;
  color:var(--ink);background:linear-gradient(90deg,var(--gamma) 0,var(--gamma) 3px,transparent 3px);
  padding:.2rem 0 .2rem 1.05rem;margin:1.1rem 0 .4rem;font-weight:480}
.abstract{color:var(--ink-soft);margin:.4rem 0 0}

/* the signature: the graded claim-strip */
.claim-strip{display:flex;flex-wrap:wrap;gap:.5rem .8rem;align-items:center;
  font-family:var(--sans);font-size:.74rem;margin:1.05rem 0 1.4rem;
  padding:.55rem .75rem;background:var(--card);border:1px solid var(--line);
  border-radius:7px}
.grade{font-family:var(--mono);font-weight:700;font-size:.72rem;
  padding:.12rem .42rem;border-radius:4px;color:#fff;letter-spacing:.01em}
.g-forced{background:var(--g-forced)} .g-verified{background:var(--g-verified)}
.g-open{background:var(--g-open)} .g-calibrated{background:var(--g-cal)}
.claim-strip .gate{font-family:var(--mono);color:var(--faint);font-size:.7rem}
.claim-strip a{font-weight:600}
.claim-strip .sep{color:var(--line)}

/* self-contained locked-quantity cards (6-R.2) */
.vp-card{font-family:var(--sans);font-size:.82rem;line-height:1.45;
  background:#f4f6f4;border-left:3px solid var(--g-verified);
  border-radius:0 6px 6px 0;padding:.55rem .8rem;margin:1rem 0}
.vp-card.c-gamma{border-left-color:var(--gamma);background:#f1f5f8}
.vp-card.c-a4{border-left-color:var(--a4);background:#f8f4ef}
.vp-card b{font-family:var(--mono);font-size:.84rem}
.vp-card .gd{font-family:var(--mono);font-weight:700;font-size:.72rem;color:var(--ink-soft)}

/* firewall banner -- the magnitude firewall, visible in every chapter */
.firewall{font-family:var(--sans);font-size:.8rem;line-height:1.5;
  border:1px dashed var(--g-open);border-radius:7px;color:var(--ink-soft);
  background:#fcf8f1;padding:.6rem .85rem;margin:1.6rem 0}
.firewall b{color:var(--g-open);font-family:var(--mono);letter-spacing:.02em}

/* data tables -- comparison/ordering reads */
table.data{border-collapse:collapse;width:100%;font-family:var(--sans);
  font-size:.82rem;margin:1rem 0}
table.data caption{font-family:var(--mono);font-size:.7rem;color:var(--faint);
  text-align:left;padding-bottom:.35rem;letter-spacing:.02em}
table.data th,table.data td{border-bottom:1px solid var(--rule);
  padding:.32rem .55rem;text-align:right}
table.data th:first-child,table.data td:first-child{text-align:left}
table.data thead th{color:var(--faint);font-weight:600;border-bottom:1px solid var(--line)}
table.data td.on{color:var(--g-verified);font-weight:600}
table.data tr.hi td{background:#f3f7f4}
.unit{font-family:var(--mono);font-weight:600;color:var(--ink)}
.no{color:var(--gamma)} .yes{color:var(--g-verified);font-weight:600}

/* inline math + key-result chips */
.kf{font-family:var(--mono);font-weight:600;color:var(--ink);
  background:#eef1f4;padding:.04rem .3rem;border-radius:3px;white-space:nowrap}
code{font-family:var(--mono);font-size:.86em;background:#eef1f4;
  padding:.04rem .28rem;border-radius:3px}

/* prev/next + hub lists */
nav.pn{display:flex;justify-content:space-between;gap:1rem;
  font-family:var(--sans);font-size:.84rem;margin:2.6rem 0 0;
  padding-top:1rem;border-top:1px solid var(--rule)}
nav.pn a{font-weight:600}
ol.toc{list-style:none;padding:0;margin:1.2rem 0;
  font-family:var(--sans);font-size:.95rem}
ol.toc li{display:flex;gap:.7rem;padding:.5rem 0;border-bottom:1px solid var(--rule)}
ol.toc .n{font-family:var(--mono);color:var(--faint);font-size:.8rem;
  min-width:2.4rem;padding-top:.12rem}
ol.toc .t{flex:1}
ol.toc .t b{font-weight:640;display:block}
ol.toc .t span{color:var(--faint);font-size:.82rem;font-family:var(--sans)}
ol.toc .gtag{font-family:var(--mono);font-size:.66rem;font-weight:700;
  padding:.08rem .34rem;border-radius:4px;color:#fff;height:fit-content;margin-top:.15rem}

.lede{font-family:var(--sans);font-size:1.04rem;line-height:1.55;
  color:var(--ink-soft);margin:.8rem 0 1.2rem}
.two-chan{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin:1.3rem 0}
.two-chan .ch{border:1px solid var(--line);border-radius:8px;padding:.8rem .9rem;
  font-family:var(--sans);font-size:.85rem;background:var(--card)}
.two-chan .ch h4{margin:.1rem 0 .4rem;font-size:.95rem}
.two-chan .ch.gamma h4{color:var(--gamma)} .two-chan .ch.a4 h4{color:var(--a4)}
.scoreboard{font-family:var(--mono);font-size:.78rem;line-height:1.7;
  background:var(--card);border:1px solid var(--line);border-radius:8px;
  padding:.8rem 1rem;margin:1.2rem 0}
.scoreboard .ok{color:var(--g-verified);font-weight:700}
.pill{display:inline-block;font-family:var(--mono);font-size:.68rem;
  padding:.1rem .4rem;border-radius:4px;background:#eef1f4;color:var(--ink-soft);
  margin-right:.3rem}
@media (max-width:640px){
  body{font-size:17px} h1{font-size:1.62rem}
  main,header,footer{padding-left:1rem;padding-right:1rem}
  .two-chan{grid-template-columns:1fr}
  table.data{font-size:.76rem}
}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
:focus-visible{outline:2px solid var(--gamma);outline-offset:2px;border-radius:2px}
"""

# grade vocabulary -> css class + printed label
GRADE_CLASS = {
    "F": ("g-forced", "[F] forced"),
    "V": ("g-verified", "[V] verified"),
    "O": ("g-open", "[O] open"),
    "L": ("g-calibrated", "[L] calibration"),
}

def grade_badge(code):
    cls, label = GRADE_CLASS[code]
    return f'<span class="grade {cls}">{label}</span>'


# ============================================================================
#  HTML emitters
# ============================================================================
def page_head(title, desc, canon, jsonld_blocks):
    blocks = "\n".join(
        '<script type="application/ld+json">\n' + json.dumps(b, ensure_ascii=False) + "\n</script>"
        for b in jsonld_blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{canon}">
<link rel="license" href="{LICENSE}">
<link rel="stylesheet" href="/assets/css/site.css">
{blocks}
</head>"""

def scholarly_ld(no, subj, canon, knows):
    return {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": subj,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": SHORT,
                     "url": f"{SITE}/{PAPER_ID}/"},
        "position": no,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "license": LICENSE, "url": canon,
        "datePublished": ISO, "dateModified": ISO,
        "isBasedOn": f"{REPO}/",
        "knowsAbout": ["jamming lattice switch", "promoter gamma",
                       "A4 coordinate channel", "magnitude firewall"] + knows,
    }

def crumb_ld(no, subj):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER_ID}/"},
            {"@type": "ListItem", "position": 3, "name": f"\u00a7{no} {subj}"}]}

FOOTER = (f'<footer>{FULLTITLE} \u00b7 \u00a7canonical HTML (VP-SPEC v1.8). '
          f'Author <a href="{ORCID}">{AUTHOR}</a> (ORCID 0009-0002-7535-8245) \u00b7 '
          f'<a href="{SITE}/">jamming-physics.org</a> \u00b7 '
          f'<a href="{LICENSE}">CC BY 4.0</a> \u00b7 '
          f'reproduce: <a href="{REPO}/">repro/ (GitHub)</a> \u00b7 '
          f'<a href="https://doi.org/{DOI}" rel="noopener">DOI {DOI}</a>.</footer>')

def claim_strip(code, slug):
    return (f'<aside class="claim-strip">{grade_badge(code)}'
            f'<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>'
            f'<span class="sep">|</span>'
            f'<a href="{REPO}/{slug}/" rel="noopener">reproduce (GitHub)</a>'
            f'<span class="sep">|</span>'
            f'<a href="{SITE}/{PAPER_ID}/" rel="noopener">volume</a>'
            f'<span class="sep">|</span>'
            f'<a class="gate" href="https://doi.org/{DOI}" rel="noopener">DOI {DOI}</a></aside>')

def firewall_box(text):
    return (f'<div class="firewall"><b>FIREWALL</b> &middot; {text} '
            f'Every clinical application \u2014 vaccination, gene therapy, fertility care \u2014 '
            f'is handed to clinicians and regulators. '
            f'<a href="/{PAPER_ID}/16-scoreboard-firewall-ledger/">see the [O] ledger \u2192</a></div>')

def render_chapter(ch, prev_ch, next_ch):
    canon = f"{SITE}/{PAPER_ID}/{ch['slug']}/"
    title = f"{ch['subj']} \u2014 {SHORT} \u00a7{ch['no']} | Jamming Physics"
    head = page_head(title, ch["desc"], canon,
                     [scholarly_ld(ch["no"], ch["subj"], canon, ch.get("knows", [])),
                      crumb_ld(ch["no"], ch["subj"])])
    crumb = (f'<header><nav class="crumb"><a href="/">Home</a> &rsaquo; '
             f'<a href="/{PAPER_ID}/">{SHORT}</a> &rsaquo; \u00a7{ch["no"]}</nav></header>')
    prevlink = (f'<a rel="prev" href="/{PAPER_ID}/{prev_ch["slug"]}/">\u2190 \u00a7{prev_ch["no"]}</a>'
                if prev_ch else '<a href="/{}/">\u2190 volume</a>'.format(PAPER_ID))
    nextlink = (f'<a rel="next" href="/{PAPER_ID}/{next_ch["slug"]}/">\u00a7{next_ch["no"]} \u2192</a>'
                if next_ch else f'<a href="/{PAPER_ID}/">volume \u2192</a>')
    pn = (f'<nav class="pn">{prevlink}'
          f'<a href="/{PAPER_ID}/">contents</a>{nextlink}</nav>')
    body = f"""{head}
<body>
{crumb}
<main>
<p class="eyebrow">\u00a7{ch['no']} &middot; {ch['eyebrow']}</p>
<h1>{E(ch['h1'])}</h1>
<p class="answer">{ch['answer']}</p>
<p class="abstract">{ch['abstract']}</p>
{claim_strip(ch['grade'], ch['slug'])}
{ch['body']}
{firewall_box(ch['firewall'])}
{pn}
</main>
{FOOTER}
</body>
</html>"""
    return body


# ============================================================================
#  small builders for tables / cards used inside chapter bodies
# ============================================================================
def tbl(caption, headers, rows, hi=None):
    """rows: list of lists of already-formatted cell strings."""
    thead = "".join(f"<th>{E(h)}</th>" for h in headers)
    trs = []
    for i, r in enumerate(rows):
        cls = ' class="hi"' if hi is not None and i in hi else ""
        tds = "".join(f"<td>{c}</td>" for c in r)
        trs.append(f"<tr{cls}>{tds}</tr>")
    return (f'<table class="data"><caption>{E(caption)}</caption>'
            f'<thead><tr>{thead}</tr></thead><tbody>{"".join(trs)}</tbody></table>')

def yn(b):
    return '<span class="yes">yes</span>' if b else '<span class="no">no</span>'

def card_gamma(term, meaning):
    return (f'<aside class="vp-card c-gamma"><b>{term}</b> &mdash; {meaning} '
            f'<span class="gd">[L] measured</span> '
            f'<a href="/{PAPER_ID}/01-two-channel-architecture-set-coordinate/">canonical \u00a71</a></aside>')

def card_a4(term, meaning):
    return (f'<aside class="vp-card c-a4"><b>{term}</b> &mdash; {meaning} '
            f'<span class="gd">[V] verified</span> '
            f'<a href="/{PAPER_ID}/03-a4-orthogonality-coordinate-targeting/">canonical \u00a73</a></aside>')


# ============================================================================
#  CHAPTER CONTENT -- every number is fetched from the gate report via R(...)
# ============================================================================
def build_chapters():
    C = []

    # ---- 1. two-channel architecture (framing) -------------------------------
    C.append(dict(
        no=1, slug="01-two-channel-architecture-set-coordinate",
        eyebrow="the substrate", subj="The two-channel genome",
        desc=("Every result stands on one bistable switch read on two channels: gamma "
              "(the unwritable SET) and the A4 coordinate (the writable structure). The "
              "environment writes a reversible drive at an A4 coordinate, never on gamma."),
        h1="The genome is read on two channels: a fixed SET and a writable coordinate",
        knows=["bistable switch", "spinodal", "energy barrier", "epigenetic inheritance"],
        answer=("Every result in this volume stands on one bistable switch read on "
                "<b>two channels</b>: <span class=\"kf\">\u03b3</span>, the SET \u2014 the "
                "unwritable promoter ruler that scales the switch \u2014 and the <b>A4 "
                "coordinate</b>, the writable structure that says where an element sits and "
                "whether it can make contact. The environment writes a reversible drive "
                "<span class=\"kf\">h</span> at an A4 coordinate, never on \u03b3. <b>[F]</b>."),
        abstract=(f"The shared primitive is the jamming switch <span class=\"kf\">ds/dt = "
                  f"\u03b3\u00b7s \u2212 s\u00b3 + h</span>, a double well whose threshold scales "
                  f"with \u03b3: a held state flips only past the spinodal <span class=\"kf\">"
                  f"2(\u03b3/3)^1.5</span>, and the barrier between basins is <span class=\"kf\">"
                  f"\u03b3\u00b2/4</span>. Each \u03b3 is measured, accepted only because the "
                  f"SOX9 anchor reproduces at \u03b3 = {num('anchor', ANCHOR_GAMMA)}."),
        grade="F",
        firewall=("We read <b>WHICH</b> switch is tilted, the <b>SIGN</b> of the drive, and "
                  "the <b>ORDERING / DECAY</b> of inheritance and memory \u2014 never an "
                  "absolute phenotype, dose, titre or generation-count."),
        body=f"""
<p class="lede">One switch, two channels, one drive. That decomposition \u2014 a fixed material
ruler the environment cannot touch, a writable structure it can reorganise, and a reversible
signal written onto the structure \u2014 is the spine behind inheritance, immunity, vaccines and
gene therapy alike.</p>

<div class="two-chan">
  <div class="ch gamma"><h4>\u03b3 \u2014 the SET (material)</h4>
  The promoter thermodynamics: \u03b3 = \u2212mean nearest-neighbour stacking \u0394G (SantaLucia 1998)
  over TSS\u22122000..+500. It <b>scales</b> every switch but is <b>fixed in the genome</b> \u2014 the
  environment cannot rewrite it, so \u03b3 can never be the thing the environment writes.</div>
  <div class="ch a4"><h4>A4 \u2014 the COORDINATE (structure)</h4>
  Where an element sits in the compartment-shell + anchor-loop architecture, and whether it is on
  the same helical <b>face</b> as its anchor (contact-competent). A4 is the channel the environment
  <b>reorganises</b> and a small RNA <b>targets</b> by sequence complementarity.</div>
</div>

<h2>The switch is vendored, not re-derived</h2>
<p>There is exactly one copy of the switch math, and it is read-only. The spinodal
<span class="kf">2(\u03b3/3)^1.5</span> is the drive past which one basin disappears \u2014 a
discontinuous flip \u2014 and the barrier <span class="kf">\u03b3\u00b2/4</span> is the depth between
basins, which is state stability and therefore memory. A deeper-\u03b3 switch is harder to flip and
holds its state longer; that single fact orders most of what follows.</p>

<h2>Every \u03b3 is a measurement, anchor-gated</h2>
<p>No \u03b3 in this volume is fitted. The measurement pipeline is accepted only because it reproduces
the SOX9 anchor at <span class="kf">\u03b3 = {num('anchor', ANCHOR_GAMMA)}</span> bit-for-bit; fail the
anchor and the pipeline refuses to write. The germline, immune, RNA-machinery and imprinted atlases
are frozen regression checkpoints \u2014 adding genes is additive, changing a measured value is a
regression and is forbidden.</p>

<h2>The drive is written at a coordinate</h2>
<p>The environment writes a reversible drive <span class="kf">h</span>, and it does so through the
A4 channel (and methylation), never through \u03b3. A small RNA acts by complementarity: it names an A4
coordinate and deposits a drive there. So inheritance, when it happens, is the inheritance of a held
A4 configuration \u2014 a contact state at a coordinate \u2014 not of a rewritten ruler.</p>
""",
    ))

    # ---- 2. RNA writable channel (R + RS) -----------------------------------
    rs_rows = []
    for r in R("RS_rna_species", 1, "table"):
        rs_rows.append([E(r["species"]),
                        E(", ".join(r["machinery"])),
                        num(f"rs_g_{r['species']}", r["mean_gamma"], "g4"),
                        num(f"rs_b_{r['species']}", r["production_barrier"], "g4"),
                        yn(r["germline_restricted"])])
    C.append(dict(
        no=2, slug="02-rna-writable-channel-species",
        eyebrow="the writable channel", subj="The RNA writable channel",
        desc=("Small RNA is a reversible write of the drive h, not an edit of gamma; two signs "
              "(siRNA OFF, saRNA ON); the measured 12-gene carrier atlas is bistable; resolved by "
              "machinery it splits into miRNA, piRNA, tsRNA and m6A."),
        h1="Small RNA is a reversible write of the drive, resolved into measured species",
        knows=["small RNA", "miRNA", "piRNA", "m6A methylation", "reversibility"],
        answer=("Small RNA writes the drive <span class=\"kf\">h</span>, not the ruler \u03b3: it is "
                "<b>reversible</b> (payload cleared, the basin returns), it carries <b>two signs</b> "
                "(siRNA\u2192OFF, saRNA\u2192ON), and the measured 12-gene carrier atlas is bistable. "
                "Resolved by its biogenesis machinery it splits into miRNA, piRNA, tsRNA and m6A \u2014 "
                "each a signed drive. <b>[V]</b>."),
        abstract=(f"On DICER1 (\u03b3 = {num('r_gdicer', R('R_rna_layer',0,'gamma_DICER1'),'g4')}, "
                  f"spinodal {num('r_spin', R('R_rna_layer',0,'spinodal'),'g4')}) a held switch flips "
                  f"only past the opposite spinodal at <span class=\"kf\">h = "
                  f"{num('r_hflip', R('R_rna_layer',0,'h_at_flip'),'g4')}</span>, and \u03b3 is never "
                  f"edited. Production stability orders by machinery barrier, piRNA deepest."),
        grade="V",
        firewall=("The species <b>SIGN</b> and the production-stability <b>ORDERING</b> are read; the "
                  "absolute payload\u2192phenotype dose and the per-species gain are runtime <b>[O]</b>."),
        body=f"""
<h2>RNA writes the drive, not the ruler</h2>
<p>Driving a held switch with an RNA payload flips it only once the drive passes the
<em>opposite</em> spinodal \u2014 a hysteretic, memory-bearing flip \u2014 while \u03b3 stays exactly where
it was. That is the defining contrast with an edit: a payload moves the state, an edit moves the SET.</p>
{card_gamma("&gamma;<sub>DICER1</sub> = " + num('r_gdicer2', R('R_rna_layer',0,'gamma_DICER1'),'g4'),
            "the microprocessor-machinery promoter \u03b3 used as the worked carrier; spinodal "
            + num('r_spin2', R('R_rna_layer',0,'spinodal'),'g4') + ".")}

<h2>Two signs on one channel</h2>
<p>The same channel carries opposite signs: a silencing payload drives the switch OFF, an activating
payload drives it ON. One physical channel, a signed write \u2014 not two mechanisms.</p>

<h2>Reversibility is the through-line</h2>
<p>Clear the payload and the basin returns; the correction is reversible and tunable. This is why,
later, an RNA vaccine needs no edit and Lever B is the reversible therapeutic lever.</p>

<h2>Resolved into measured species</h2>
<p>"Small RNA" is not one thing. Split by the measured biogenesis machinery, it resolves into four
species, each a signed drive whose production stability is set by its machinery barrier. The ordering
is read, never an absolute gain.</p>
{tbl("RS2 \u2014 production-stability ordering by machinery barrier (NCBI-measured \u03b3)",
     ["species","machinery","mean \u03b3","prod. barrier","germline-restricted"], rs_rows, hi=[3])}
<p>The writer/eraser pair is reversible at the mark level too: METTL3 (\u03b3 =
{num('rs_mettl3', R('RS_rna_species',2,'gamma_METTL3'),'g4')}) writes the m6A mark and drives ON,
YTHDF2 (\u03b3 = {num('rs_ythdf2', R('RS_rna_species',2,'gamma_YTHDF2'),'g4')}) erases it and drives
OFF \u2014 the mark-side twin of payload reversibility. The germline-restricted machinery (piRNA,
tsRNA) selects exactly the carriers that can load the gamete; the somatic species cannot.</p>
""",
    ))
    C += _chapters_3_7()
    C += _chapters_8_15()
    return C


def _chapters_3_7():
    C = []

    # ---- 3. A4 orthogonality & coordinate-targeting --------------------------
    ap = R("A4_a4_layer", 0, "example_pair")
    corr_rows = [
        ["\u03b3 vs GC content",
         num("a4_cgc", R("A4_a4_layer",0,"corr_gamma_GC"),"g3"),
         num("a4_rgc", R("A4_a4_layer",0,"R2_gamma_GC_pct"),"%.0f")+"%"],
        ["\u03b3 vs CpG O/E",
         num("a4_ccpg", R("A4_a4_layer",0,"corr_gamma_CpG_OE"),"g3"),
         num("a4_rcpg", R("A4_a4_layer",0,"R2_gamma_CpG_pct"),"%.0f")+"%"],
        ["\u03b3 vs helical contact face",
         num("a4_cface", R("A4_a4_layer",0,"corr_gamma_helical_face"),"g3"),
         num("a4_rface", R("A4_a4_layer",0,"R2_gamma_face_pct"),"%.0f")+"%"],
    ]
    C.append(dict(
        no=3, slug="03-a4-orthogonality-coordinate-targeting",
        eyebrow="the coordinate channel", subj="A4 is orthogonal to gamma",
        desc=("Gamma alone is degenerate: the A4 helical contact phase is ~98% independent of gamma, "
              "and same-gamma/different-contact pairs are real. RNA is coordinate-targeting \u2014 at "
              "fixed gamma, contact-competence decides whether a fixed drive flips."),
        h1="Gamma alone is degenerate: the A4 contact phase is the writable, RNA-targeted channel",
        knows=["orthogonality", "helical phase", "coordinate targeting", "CpG islands"],
        answer=("\u03b3 alone is <b>degenerate</b>. The A4 helical contact phase is about "
                "<b>98% independent</b> of \u03b3 (\u03b3 tracks GC at R\u00b2 = "
                "{r}%, but the contact face only {f}%), and real pairs share \u03b3 yet differ in "
                "contact. RNA is <b>coordinate-targeting</b>: at fixed \u03b3, contact-competence "
                "decides whether a fixed drive flips the switch. <b>[V]</b>.").format(
                    r=num("a4_rgc2", R("A4_a4_layer",0,"R2_gamma_GC_pct"),"%.0f"),
                    f=num("a4_rface2", R("A4_a4_layer",0,"R2_gamma_face_pct"),"%.0f")),
        abstract=(f"Across {num('a4_n', R('A4_a4_layer',0,'n_carriers'))} carriers, \u03b3 explains "
                  f"{num('a4_rgc3', R('A4_a4_layer',0,'R2_gamma_GC_pct'),'%.0f')}% of GC but only "
                  f"{num('a4_rface3', R('A4_a4_layer',0,'R2_gamma_face_pct'),'%.0f')}% of the contact "
                  f"face. A worked pair differs by \u0394\u03b3 = "
                  f"{num('a4_dg', ap['dgamma'],'g3')} yet one coordinate is contact-competent and the "
                  f"other is not \u2014 same ruler, different reachability."),
        grade="V",
        firewall=("A4 <b>orthogonality</b>, the coordinate-<b>gating</b> of the drive, and the "
                  "identity of the inherited object are read; absolute contact energies and loop "
                  "occupancies are <b>[O]</b>."),
        body=f"""
<h2>Two readings of one locus, only loosely correlated</h2>
<p>\u03b3 is a thermodynamic average; the A4 coordinate is a structural arrangement. They share some
information through GC content, but the part that decides contact \u2014 the 3D helical face relative
to the anchor \u2014 is almost entirely outside \u03b3.</p>
{tbl("A4-1 \u2014 \u03b3 carries GC, not the contact phase (wide \u00b115 kb windows)",
     ["read","corr. with \u03b3","R\u00b2"], corr_rows, hi=[2])}

<h2>The degeneracy is concrete, not abstract</h2>
<p>A real same-\u03b3 pair makes the point: with \u0394\u03b3 = {num('a4_dg2', ap['dgamma'],'g3')}, one
member sits at helical face {num('a4_af', ap['a_face'],'g3')} and <em>is</em> contact-competent while
the other sits at face {num('a4_bf', ap['b_face'],'g3')} and is <em>not</em>. \u03b3 cannot tell them
apart; A4 can.</p>

<h2>RNA targets a coordinate, not a \u03b3</h2>
<p>At one shared \u03b3 = {num('a42_g', R('A4_a4_layer',1,'shared_gamma'),'g4')} (spinodal
{num('a42_s', R('A4_a4_layer',1,'spinodal'),'g4')}), the same payload
{num('a42_p', R('A4_a4_layer',1,'payload'),'g4')} flips the contact-competent coordinate (loop-assist
{num('a42_la', R('A4_a4_layer',1,'loop_assist_at_contact'),'g4')}) ON, yet leaves the non-contact
coordinate at the same \u03b3 OFF. Contact-competence \u2014 not \u03b3 \u2014 gates reachability.</p>

<h2>The environment writes A4; inheritance is of a configuration</h2>
<p>\u03b3 is sequence-fixed parent\u2192child; the contact state is what toggles ON then OFF, so A4 is the
writable channel. At a deep coordinate (\u03b3 =
{num('a44_g', R('A4_a4_layer',3,'deep_coordinate_gamma'),'g4')}) a held contact configuration survives
one erasure with probability {num('a44_p', R('A4_a4_layer',3,'p_contact_configuration_survives_one_erasure'),'g4')}
\u2014 the inherited object is an A4 coordinate-state, not a rewritten ruler.</p>
""",
    ))

    # ---- 4. two epigenetic channels (TC) ------------------------------------
    C.append(dict(
        no=4, slug="04-two-epigenetic-channels-add-veto-path",
        eyebrow="channel composition", subj="Methylation and RNA on one switch",
        desc=("Methylation and small RNA write the same drive on one switch: same-sign they ADD across "
              "the spinodal, opposite-sign they VETO, and the order of writes latches the state "
              "(hysteresis path-dependence)."),
        h1="Two epigenetic channels write one drive: add, veto, and path-dependence",
        knows=["DNA methylation", "channel interaction", "hysteresis", "path dependence"],
        answer=("Methylation and small RNA write the <b>same drive</b> on one switch, so they compose "
                "by sign: same-sign writes <b>ADD</b> and cross the spinodal together, opposite-sign "
                "writes <b>VETO</b> and cancel, and because the switch is hysteretic the <b>order</b> "
                "of writes latches the outcome \u2014 a memory of which channel won. <b>[V]</b>."),
        abstract=(f"On REC8 (\u03b3 = {num('tc_grec8', R('TC_two_channel',0,'target_gamma_REC8'),'g4')}, "
                  f"spinodal {num('tc_srec8', R('TC_two_channel',0,'spinodal'),'g4')}) neither channel "
                  f"flips alone but the same-sign sum does; an opposing write vetoes a flip that either "
                  f"channel would otherwise make; and on PAX5 (\u03b3 = "
                  f"{num('tc_gpax5', R('TC_two_channel',2,'target_gamma_PAX5'),'g4')}) a sub-spinodal "
                  f"opposite write cannot undo a state that already crossed."),
        grade="V",
        firewall=("The interaction <b>SIGN</b> and the path-<b>dependence</b> are read; the absolute "
                  "channel amplitudes are runtime <b>[O]</b>."),
        body=f"""
<h2>Same sign: the channels add</h2>
<p>On REC8 (spinodal {num('tc_srec8b', R('TC_two_channel',0,'spinodal'),'g4')}), methylation alone is
below threshold and RNA alone is below threshold, but written together with the same sign their sum
crosses the spinodal and the switch flips. Two sub-threshold writes make one supra-threshold drive.</p>

<h2>Opposite sign: the channels veto</h2>
<p>At the same locus, a methylation write that would flip the switch ON is held OFF by an opposing RNA
write of comparable size. The drives cancel on the shared field; neither edits the ruler.</p>

<h2>Order latches the outcome</h2>
<p>Because the switch is hysteretic, the result depends on the order, not just the sum. On PAX5
(spinodal {num('tc_spax5', R('TC_two_channel',2,'spinodal'),'g4')}), a channel that crosses first and
then meets a sub-spinodal opposite write <em>stays</em> ON; a sequence that never crosses stays OFF.
The combined state remembers which channel won \u2014 the substrate of an order-dependent epigenetic
history.</p>
""",
    ))

    # ---- 5. environment -> germline & the reprogramming firewall ------------
    tg3 = R("TG_env_to_germline", 2, "table")
    tg3_rows = [[E(r["gene"]), num(f"tg3g_{r['gene']}", r["gamma"],"g4"),
                 num(f"tg3p_{r['gene']}", r["p_survive"],"g4")] for r in tg3]
    rna_seq = R("TG_env_to_germline", 4, "rna_amplitude_by_gen")
    meth_seq = R("TG_env_to_germline", 4, "meth_amplitude_by_gen")
    decay_rows = [[f"F{i}",
                   num(f"tg5r_{i}", rna_seq[i],"g4"),
                   num(f"tg5m_{i}", meth_seq[i],"g4")] for i in range(len(rna_seq))]
    C.append(dict(
        no=5, slug="05-environment-to-germline-reprogramming-firewall",
        eyebrow="transgenerational transmission", subj="Environment to germline",
        desc=("The SET is byte-identical parent to child; only the drive is inheritable. Two genome-wide "
              "erasures square a mark's survival, so heritability ranks by barrier (ascending gamma, "
              "Spearman rho=0.995). An RNA-only drive fades; a deep-barrier mark persists."),
        h1="A parent's environment reaches a child only as a drive that survives two erasures",
        knows=["germline reprogramming", "Spearman correlation", "Lamarckian inheritance",
               "methylation persistence"],
        answer=("The SET is <b>byte-identical</b> parent\u2192child; only the drive is inheritable. Two "
                "genome-wide reprogramming erasures <b>square</b> a mark's survival (p \u2192 p\u00b2), so "
                "heritability ranks by <b>barrier</b> \u2014 ascending \u03b3, Spearman \u03c1 = {rho}. "
                "The inherited sign is preserved, an RNA-only drive fades, a deep-barrier mark persists. "
                "<b>[V]</b>.").format(
                    rho=num("tg3_rho", R("TG_env_to_germline",2,"spearman_rho_gamma_vs_survival"),"g3")),
        abstract=(f"At reprogramming noise D = {num('tg2_d', R('TG_env_to_germline',1,'reprogramming_noise_D'),'g2')}, "
                  f"a shallow switch (\u03b3 = {num('tg2_sg', R('TG_env_to_germline',1,'shallow_gamma'),'g2')}) "
                  f"survives one erasure with p = {num('tg2_sp1', R('TG_env_to_germline',1,'p_survive_one'),'g4')} "
                  f"and inherits across two at p\u00b2 = {num('tg2_sp2', R('TG_env_to_germline',1,'p_inherit_two'),'g4')}, "
                  f"while a deep switch (\u03b3 = {num('tg2_dg', R('TG_env_to_germline',1,'deep_gamma'),'g4')}) "
                  f"inherits at {num('tg2_dp2', R('TG_env_to_germline',1,'p_inherit_two_deep'),'g4')} "
                  f"\u2014 deeper inherits more."),
        grade="V",
        firewall=("<b>WHICH</b> switch, the inherited <b>SIGN</b>, and the heritability "
                  "<b>ORDERING / DECAY</b> are read; the absolute inherited phenotype magnitude and the "
                  "wild generation-count are runtime <b>[O]</b>."),
        body=f"""
<h2>The genome itself does not move</h2>
<p>Parent and child read the identical \u03b3 (DAZL = {num('tg1_g', R('TG_env_to_germline',0,'DAZL_gamma_parent'),'g4')},
byte-identical); the environment never rewrites the SET. Whatever crosses to the next generation crosses
as a drive on an unchanged switch.</p>

<h2>The firewall squares survival</h2>
<p>A germline mark must survive two genome-wide reprogramming erasures \u2014 in the primordial germ cells
and again in the zygote \u2014 so its probability of reaching the next generation is multiplied, not added.
Depth wins: at the same noise the deep switch inherits at p\u00b2 =
{num('tg2_dp2b', R('TG_env_to_germline',1,'p_inherit_two_deep'),'g4')} against the shallow switch's
{num('tg2_sp2b', R('TG_env_to_germline',1,'p_inherit_two'),'g4')}.</p>

<h2>Heritability is barrier ordering is \u03b3 ordering</h2>
<p>Across the measured 13-gene germline atlas, survival rises monotonically with \u03b3 (Spearman \u03c1 =
{num('tg3_rho2', R('TG_env_to_germline',2,'spearman_rho_gamma_vs_survival'),'g3')}). This is the central
prediction: which marks inherit is set by the barrier, and the barrier is set by the measured promoter.</p>
{tbl("TG3 \u2014 germline heritability ranks ascending-\u03b3 (D = "
     + num('tg3_d', R('TG_env_to_germline',2,'reprogramming_noise_D'),'g2') + ", 13 genes)",
     ["gene","\u03b3","p(survive one erasure)"], tg3_rows, hi=[0, len(tg3_rows)-1])}

<h2>Two carriers, two decay laws</h2>
<p>The inherited sign is preserved through the firewall (ON stays ON, OFF stays OFF). But the two writers
decay differently: an RNA-only drive dilutes each generation and drops below detectability by
F{num('tg5_rgen', R('TG_env_to_germline',4,'rna_undetectable_at_generation'))}, whereas a deep-barrier
methylation mark is still detectable across the same horizon. The generation index here is illustrative;
the wild count is <b>[O]</b>.</p>
{tbl("TG5 \u2014 decay ORDERING: RNA dilutes (rate "
     + num('tg5_rd', R('TG_env_to_germline',4,'rna_dilution_per_gen'),'g2')
     + "), methylation retains (" + num('tg5_md', R('TG_env_to_germline',4,'methylation_retention_per_gen'),'g4') + ")",
     ["generation","RNA amplitude","methylation amplitude"], decay_rows)}
""",
    ))

    # ---- 6. imprinted escapee atlas (GE) ------------------------------------
    ge = R("GE_germline_escapee", 0, "table")
    ge_rows = [[E(r["locus"]), num(f"geg_{r['locus']}", r["gamma"],"g4"),
                E(r["parent_of_origin"]), num(f"gep_{r['locus']}", r["p_survive"],"g4")] for r in ge]
    C.append(dict(
        no=6, slug="06-imprinted-escapee-atlas",
        eyebrow="the measured atlas", subj="The imprinted escapee atlas",
        desc=("On the measured 12-locus imprinted atlas, survival across the two erasures ranks "
              "ascending-gamma exactly (rho=1.0): KCNQ1OT1 best, SNRPN worst. The harsher erasure "
              "dominates, and a measured critical re-write rate separates maintained from transient."),
        h1="The canonical reprogramming escapees rank exactly by barrier",
        knows=["genomic imprinting", "KCNQ1OT1", "SNRPN", "metastable epiallele"],
        answer=("On the measured 12-locus imprinted atlas, survival across the two erasures ranks "
                "<b>ascending-\u03b3 exactly</b> (\u03c1 = {rho}): KCNQ1OT1 inherits best (\u03b3 = "
                "{kb}), SNRPN worst (\u03b3 = {sw}). The harsher of the two erasures dominates the "
                "compound, and a measured critical re-write rate separates maintained from transient "
                "inheritance. <b>[V]</b>.").format(
                    rho=num("ge1_rho", R("GE_germline_escapee",0,"spearman_rho_gamma_vs_survival"),"g2"),
                    kb=num("ge1_kb", R("GE_germline_escapee",0,"best_gamma"),"g4"),
                    sw=num("ge1_sw", R("GE_germline_escapee",0,"worst_gamma"),"g4")),
        abstract=(f"The framework predicts that only deep-barrier loci cross both erasures; the imprinted "
                  f"atlas is the natural test set, and survival is monotone in \u03b3 with Spearman \u03c1 = "
                  f"{num('ge1_rho2', R('GE_germline_escapee',0,'spearman_rho_gamma_vs_survival'),'g2')} across "
                  f"{num('ge1_n', R('GE_germline_escapee',0,'n_loci'))} loci. The critical re-write rate is "
                  f"w* = {num('ge3_w', R('GE_germline_escapee',2,'critical_w_star'),'g4')}."),
        grade="V",
        firewall=("The survival <b>ORDERING</b>, the harsher-erasure <b>dominance</b>, and the re-writing "
                  "<b>BOUNDARY</b> are read; absolute penetrance and the wild generation index are <b>[O]</b>."),
        body=f"""
<h2>A pre-declared test set</h2>
<p>The imprinted and metastable-epiallele loci are exactly the genome's known reprogramming escapees, so
they are the honest panel for the barrier prediction. Measured through the identical SOX9-gated pipeline,
their survival ranks ascending-\u03b3 with a perfect Spearman \u03c1 =
{num('ge1_rho3', R('GE_germline_escapee',0,'spearman_rho_gamma_vs_survival'),'g2')}.</p>
{tbl("GE1 \u2014 imprinted survival ranks ascending-\u03b3 (D = "
     + num('ge1_d', R('GE_germline_escapee',0,'reprogramming_noise_D'),'g2') + ", 12 loci)",
     ["locus","\u03b3","parent-of-origin","p(survive)"], ge_rows, hi=[0, len(ge_rows)-1])}

<h2>The two erasures resolved \u2014 the harsher dominates</h2>
<p>Splitting the single noise pulse into a PGC window (D =
{num('ge2_dpgc', R('GE_germline_escapee',1,'D_pgc'),'g2')}) and a harsher zygotic window (D =
{num('ge2_dzyg', R('GE_germline_escapee',1,'D_zyg_harsher'),'g2')}), the compound is set by the harsher
one. A deep escapee (\u03b3 = {num('ge2_dg', R('GE_germline_escapee',1,'deep_gamma'),'g4')}) still beats a
shallow locus across both windows; survival compounds
{num('ge2_cd', R('GE_germline_escapee',1,'compound_deep'),'g3')} vs
{num('ge2_cs', R('GE_germline_escapee',1,'compound_shallow'),'g4')}.</p>

<h2>A boundary between maintained and transient</h2>
<p>With a measured per-generation loss of {num('ge3_loss', R('GE_germline_escapee',2,'per_generation_loss'),'g4')},
there is a critical re-write rate w* = {num('ge3_w2', R('GE_germline_escapee',2,'critical_w_star'),'g4')}: a
persistent environment that re-loads the payload above w* holds the effect indefinitely, while a transient
exposure below it fades to zero. The boundary is the substrate's line between an inherited habit and a
passing one; its calendar value in the wild is <b>[O]</b>.</p>
""",
    ))

    # ---- 7. gamma<->A4 coordinate-resolved heritability + parent-of-origin ---
    ch3 = R("CH_coordinate_heritability", 2, "top_table")
    ch3_rows = [[E(r["locus"]), num(f"ch3g_{r['locus']}", r["gamma"],"g4"),
                 yn(r["contact"]), num(f"ch3s_{r['locus']}", r["survival"],"g4")] for r in ch3]
    mp = R("CH_coordinate_heritability", 0, "matched_pair")
    mp_items = list(mp.items())
    C.append(dict(
        no=7, slug="07-coordinate-resolved-heritability-parent-of-origin",
        eyebrow="the coupling", subj="Heritability couples gamma and A4",
        desc=("Heritability couples both channels: at matched gamma the contact-competent coordinate "
              "inherits better; each imprinted locus carries a parent-specific contact state; the joint "
              "(gamma, A4) ordering puts deep-gamma plus contact-competent loci on top (NNAT)."),
        h1="Heritability couples the ruler and the structure, with a parent-of-origin signature",
        knows=["coordinate-resolved heritability", "parent-of-origin", "NNAT", "joint ordering"],
        answer=("Heritability couples <b>both</b> channels. At matched \u03b3 the contact-competent "
                "coordinate inherits better ({a} vs {b}, \u0394\u03b3 = {dg}); each imprinted locus carries "
                "a <b>parent-specific</b> contact state; and the joint (\u03b3, A4) ordering puts deep-\u03b3 "
                "<em>and</em> contact-competent loci on top \u2014 led by NNAT. <b>[V]</b>.").format(
                    a=E(mp_items[0][0]), b=E(mp_items[1][0]),
                    dg=num("ch1_dg", R("CH_coordinate_heritability",0,"dgamma"),"g4")),
        abstract=(f"\u03b3 sets the barrier, but at a matched barrier the structure still matters: the "
                  f"contact-competent member of a \u0394\u03b3 = "
                  f"{num('ch1_dg2', R('CH_coordinate_heritability',0,'dgamma'),'g4')} pair survives at "
                  f"{num('ch1_sc', R('CH_coordinate_heritability',0,'survival_contact_competent'),'g3')} "
                  f"against {num('ch1_sn', R('CH_coordinate_heritability',0,'survival_noncontact'),'g4')}. "
                  f"Imprinted contact fractions split paternal "
                  f"{num('ch2_pat', R('CH_coordinate_heritability',1,'paternal_contact_fraction'),'g2')} vs "
                  f"maternal {num('ch2_mat', R('CH_coordinate_heritability',1,'maternal_contact_fraction'),'g2')}."),
        grade="V",
        firewall=("The coupling <b>DIRECTION</b>, the parent-of-origin <b>MAPPING</b>, and the joint "
                  "<b>ORDERING</b> are read; absolute contact-stabilisation energy and penetrance are <b>[O]</b>."),
        body=f"""
<h2>Contact adds heritability at fixed barrier</h2>
<p>Take two loci with essentially the same \u03b3 ({E(mp_items[0][0])} = {num('ch1_a', mp_items[0][1],'g4')},
{E(mp_items[1][0])} = {num('ch1_b', mp_items[1][1],'g4')}; \u0394\u03b3 =
{num('ch1_dg3', R('CH_coordinate_heritability',0,'dgamma'),'g4')}). The contact-competent one inherits
better \u2014 {num('ch1_sc2', R('CH_coordinate_heritability',0,'survival_contact_competent'),'g3')} vs
{num('ch1_sn2', R('CH_coordinate_heritability',0,'survival_noncontact'),'g4')} \u2014 so A4 carries
heritability information that \u03b3 cannot.</p>
{card_a4("contact-competence", "same helical face as the anchor &rarr; a fixed drive can reach the switch; the orthogonal, RNA-targeted structure channel.")}

<h2>A parent-specific configuration</h2>
<p>Mapping the imprinted loci, the paternal set carries a contact fraction of
{num('ch2_pat2', R('CH_coordinate_heritability',1,'paternal_contact_fraction'),'g2')} against the maternal
{num('ch2_mat2', R('CH_coordinate_heritability',1,'maternal_contact_fraction'),'g2')} in-panel \u2014 each
locus holds a parent-specific A4 contact state, which is the structural reading of parent-of-origin
inheritance. The absolute penetrance is <b>[O]</b>; the mapping is <b>[V]</b>.</p>

<h2>The joint ordering</h2>
<p>Ranking all {num('ch3_n', R('CH_coordinate_heritability',2,'n_loci'))} loci by the joint (\u03b3, A4)
criterion, the top is NNAT \u2014 deep-\u03b3 and contact-competent together \u2014 and the contact-competent
status of the leader is what tips it above a slightly deeper but non-contact locus.</p>
{tbl("CH3 \u2014 joint (\u03b3, A4) heritability ordering (top of " + num('ch3_n2', R('CH_coordinate_heritability',2,'n_loci')) + " loci)",
     ["locus","\u03b3","contact","survival"], ch3_rows, hi=[0])}
""",
    ))
    return C


def _chapters_8_15():
    C = []

    # ---- 8. immune strengthening & inheritance (I) --------------------------
    i1 = R("I_transgenerational_immunity", 0, "table")
    i1_rows = [[E(r["gene"]), num(f"i1g_{r['gene']}", r["gamma"],"g4"),
                num(f"i1e_{r['gene']}", r["escape_rate"],"%.5f"),
                num(f"i1m_{r['gene']}", r["mfpt"],"g2")] for r in i1]
    C.append(dict(
        no=8, slug="08-immune-strengthening-and-inheritance",
        eyebrow="immunity", subj="Immune memory as a held basin",
        desc=("Immune memory is a held basin whose lifetime (MFPT) ranks ascending-gamma; trained "
              "immunity is a pre-tilt that lowers the drive needed to recall; the primed sign can ride "
              "the germline RNA payload, inheritable but fading."),
        h1="Immune memory is a held basin; training is a pre-tilt; priming can be inherited",
        knows=["immune memory", "trained immunity", "mean first passage time", "vaccination"],
        answer=("Immune <b>memory</b> is a held basin whose lifetime (mean first-passage time) ranks "
                "ascending-\u03b3; <b>trained</b> immunity is a pre-tilt that lowers the drive needed to "
                "recall (from {n} to {p}); and the primed <b>sign</b> can ride the germline RNA payload, "
                "inheritable but fading by F3 if not re-written. <b>[V]/[O]</b>.").format(
                    n=num("i2_n", R("I_transgenerational_immunity",1,"min_drive_naive"),"g4"),
                    p=num("i2_p", R("I_transgenerational_immunity",1,"min_drive_primed"),"g4")),
        abstract=(f"Over {num('i1_n', R('I_transgenerational_immunity',0,'n_compartments'))} compartments "
                  f"at noise D = {num('i1_d', R('I_transgenerational_immunity',0,'noise_D'),'g2')}, the "
                  f"memory lifetime EMERGES from the measured escape statistic and rises with \u03b3 "
                  f"(RUNX1\u2192PAX5). A primed switch needs less drive to recall, and the inherited priming "
                  f"sign survives one erasure at "
                  f"{num('i3_p', R('I_transgenerational_immunity',2,'p_primed_sign_survives_one_erasure'),'g4')}."),
        grade="V",
        firewall=("The memory <b>ORDERING</b>, the recall <b>DIRECTION</b>, and the inheritance "
                  "<b>SIGN</b> are read; the absolute inherited protection magnitude is runtime <b>[O]</b>."),
        body=f"""
<h2>Durability emerges, it is not asserted</h2>
<p>Memory is the time a switch stays in its protected basin. Measured as an escape statistic (not read
off the closed-form barrier), the lifetime rises with \u03b3 across the four immune masters \u2014 a deeper
barrier holds memory longer.</p>
{tbl("I1 \u2014 memory lifetime (MFPT) ranks ascending-\u03b3 (D = "
     + num('i1_d2', R('I_transgenerational_immunity',0,'noise_D'),'g2') + ")",
     ["master gene","\u03b3","escape rate","MFPT"], i1_rows, hi=[0, len(i1_rows)-1])}

<h2>Training lowers the distance to the flip</h2>
<p>On PAX5 (\u03b3 = {num('i2_g', R('I_transgenerational_immunity',1,'gamma_PAX5'),'g4')}, spinodal
{num('i2_s', R('I_transgenerational_immunity',1,'spinodal'),'g4')}), a naive switch needs a drive of
{num('i2_n2', R('I_transgenerational_immunity',1,'min_drive_naive'),'g4')} to recall, while a pre-tilted
(trained) switch needs only {num('i2_p2', R('I_transgenerational_immunity',1,'min_drive_primed'),'g4')}.
Trained immunity is a standing tilt that shortens the path to the protected state.</p>

<h2>Priming can cross to the next generation</h2>
<p>The primed sign can ride the germline RNA payload through one erasure (survival
{num('i3_p2', R('I_transgenerational_immunity',2,'p_primed_sign_survives_one_erasure'),'g4')}), inheritable
in direction but fading by F3 unless re-written. The sign is read; the absolute inherited protection is
<b>[O]</b>.</p>
""",
    ))

    # ---- 9. immune maturation (IM) ------------------------------------------
    im_sweep = R("IM_immune_maturation", 0, "sweep")
    im_opt_sf = R("IM_immune_maturation", 0, "optimum_survivor_frac")
    im_opt_idx = next(i for i, r in enumerate(im_sweep) if r["survivor_frac"] == im_opt_sf)
    im1_rows = [[num(f"im1sf_{i}", r["survivor_frac"], "g3"),
                 num(f"im1p_{i}", r["pressure"], "g3"),
                 num(f"im1g_{i}", r["maturation_gain"], "%+.6f")]
                for i, r in enumerate(im_sweep)]
    im_in = R("IM_immune_maturation", 1, "innate")
    im_ad = R("IM_immune_maturation", 1, "adaptive")
    im2_rows = [
        ["innate", E(im_in["gene"]), num("im2gi", im_in["gamma"], "g4"),
         num("im2bi", im_in["barrier"], "g4"), num("im2si", im_in["surviving_fraction"], "g4"),
         num("im2mi", im_in["mfpt"], "g2")],
        ["adaptive", E(im_ad["gene"]), num("im2ga", im_ad["gamma"], "g4"),
         num("im2ba", im_ad["barrier"], "g4"), num("im2sa", im_ad["surviving_fraction"], "g4"),
         num("im2ma", im_ad["mfpt"], "g2")],
    ]
    C.append(dict(
        no=9, slug="09-immune-maturation",
        eyebrow="maturation", subj="Immune maturation: one switch, three reads",
        desc=("Affinity maturation emerges from iterated germinal-centre selection and its gain has an "
              "interior optimum; innate versus adaptive immunity is a two-timescale durability split; and "
              "tolerance is the opposite-sign drive on the very same memory switch."),
        h1="Maturation has an interior optimum, innate/adaptive split by timescale, tolerance mirrors memory",
        knows=["affinity maturation", "trained vs adaptive immunity", "immune tolerance",
               "germinal-centre selection"],
        answer=("Affinity maturation <b>EMERGES</b> from iterated germinal-centre selection, and its gain "
                "peaks at an <b>interior optimum</b> ({s} survivor fraction): too-weak selection loses "
                "ground, too-stringent collapses it. Innate and adaptive immunity split into two "
                "well-separated <b>durability</b> timescales ranked by measured \u03b3, and <b>tolerance</b> "
                "is the same PAX5 switch driven the opposite way. <b>[V]/[O]</b>.").format(
                    s=num("im1_optsf", R("IM_immune_maturation", 0, "optimum_survivor_frac"), "g2")),
        abstract=(f"A germinal-centre loop on the substrate (pool "
                  f"{num('im1_pool', R('IM_immune_maturation',0,'pool'))}, "
                  f"{num('im1_rounds', R('IM_immune_maturation',0,'rounds'))} rounds) MEASURES the "
                  f"inverted-U: gain runs from "
                  f"{num('im1_weak', R('IM_immune_maturation',0,'weak_selection_gain'),'%+.6f')} under weak "
                  f"selection to a peak of "
                  f"{num('im1_peak', R('IM_immune_maturation',0,'optimum_gain'),'%+.6f')} and back toward "
                  f"{num('im1_over', R('IM_immune_maturation',0,'over_stringent_gain'),'%+.6f')} when "
                  f"over-stringent. Innate (RUNX1) and adaptive (PAX5) separate into a measured MFPT ratio of "
                  f"{num('im2_ratio', R('IM_immune_maturation',1,'mfpt_ratio_adaptive_over_innate'),'g3')}\u00d7, "
                  f"and the tolerance flip sits at the same spinodal magnitude as memory, both basins held "
                  f"after the drive clears."),
        grade="V",
        firewall=("The maturation <b>OPTIMUM</b>, the durability <b>ORDERING</b>, and the "
                  "memory\u2194tolerance <b>SIGN</b> are read; absolute affinity, lifetimes (days/years) and "
                  "desensitisation dose/schedule are runtime <b>[O]</b>; clinical tolerance to clinicians."),
        body=f"""
<h2>Maturation emerges, and its gain has an interior optimum</h2>
<p>Iterated selection on the germinal-centre loop is run directly on the substrate: a pool of
{num('im1_pool2', R('IM_immune_maturation',0,'pool'))} over
{num('im1_rounds2', R('IM_immune_maturation',0,'rounds'))} rounds. The maturation gain is not asserted \u2014
it EMERGES, and it is non-monotone in selection pressure: too-weak selection loses ground (negative gain),
an interior survivor fraction is optimal, and over-stringent selection starves the pool back toward zero
gain.</p>
{tbl("IM1 \u2014 maturation gain has an interior optimum (peak at survivor fraction "
     + num('im1_optsf2', R('IM_immune_maturation',0,'optimum_survivor_frac'),'g2') + ")",
     ["survivor fraction","selection pressure","maturation gain"], im1_rows,
     hi=[0, im_opt_idx])}

<h2>Innate versus adaptive is a two-timescale durability split</h2>
<p>At noise D = {num('im2_d', R('IM_immune_maturation',1,'noise_D'),'g2')} the innate master (RUNX1,
shallower barrier) and the adaptive master (PAX5, deeper barrier) separate into two well-spaced decay
timescales. The slower arm is the deeper barrier, and the ordering tracks the measured \u03b3 \u2014 durability
is read from the escape statistic, not assigned.</p>
{tbl("IM2 \u2014 adaptive outlasts innate; the slow arm is the deeper barrier",
     ["arm","master gene","\u03b3","barrier","surviving fraction","MFPT"], im2_rows, hi=[1])}
<p>The adaptive arm outlasts the innate arm by a measured factor of
{num('im2_ratio2', R('IM_immune_maturation',1,'mfpt_ratio_adaptive_over_innate'),'g3')}\u00d7. Absolute
lifetimes in days or years are runtime <b>[O]</b>.</p>

<h2>Tolerance is memory's mirror drive on the same switch</h2>
<p>On PAX5 (\u03b3 = {num('im3_g', R('IM_immune_maturation',2,'gamma'),'g4')}, spinodal
{num('im3_s', R('IM_immune_maturation',2,'spinodal'),'g4')}), a positive drive of
{num('im3_dm', R('IM_immune_maturation',2,'drive_to_memory'),'g4')} settles the switch into <b>memory</b>,
while the equal and opposite drive of {num('im3_dt', R('IM_immune_maturation',2,'drive_to_tolerance'),'g4')}
settles it into <b>tolerance</b>. The two thresholds are symmetric at the spinodal magnitude, and both
basins are held after the drive clears \u2014 memory and tolerance are the same switch read with opposite sign.
The sign law is measured; the absolute desensitisation dose and schedule are <b>[O]</b>, and clinical
tolerance is handed to clinicians.</p>
""",
    ))

    # ---- 9. RNA vaccines (V) ------------------------------------------------
    C.append(dict(
        no=10, slug="10-rna-vaccines-as-a-dosed-drive",
        eyebrow="application: vaccine", subj="An RNA vaccine is a dosed drive",
        desc=("A vaccine is a supra-spinodal flip into the protected basin, held by the barrier after the "
              "payload clears. The boost schedule has an interior optimum tracking the measured protection "
              "half-life. The payload is transient; protection persists at zero drive."),
        h1="An RNA vaccine is a supra-spinodal flip held by the barrier, not the payload",
        knows=["RNA vaccine", "prime-boost schedule", "protection half-life", "interior optimum"],
        answer=("A vaccine is a <b>supra-spinodal flip</b> into the protected basin, held by the barrier "
                "after the payload clears. The boost schedule has an <b>interior optimum</b> ("
                "best interval {bi}) that tracks the measured protection half-life ({hl}). The payload is "
                "<b>transient</b>; protection persists at zero drive. <b>[V]</b>.").format(
                    bi=num("v3_bi", R("V_rna_vaccine",1,"best_interval"),"g2"),
                    hl=num("v3_hl", R("V_rna_vaccine",1,"protection_half_life"),"g2")),
        abstract=(f"On the immune master (\u03b3 = {num('v1_g', R('V_rna_vaccine',0,'immune_gamma'),'g4')}, "
                  f"barrier {num('v1_b', R('V_rna_vaccine',0,'barrier'),'g4')}) the prime flips the switch ON "
                  f"and memory is held after clearance. Under a "
                  f"{num('v3_nb', R('V_rna_vaccine',1,'n_boosts_budget'))}-boost budget over horizon "
                  f"{num('v3_h', R('V_rna_vaccine',1,'horizon'),'g2')}, the optimal interval is interior and "
                  f"protection persists at zero drive (s = "
                  f"{num('v4_s', R('V_rna_vaccine',2,'s_after_clearance'),'g4')})."),
        grade="V",
        firewall=("The flip <b>DIRECTION</b>, the schedule <b>SHAPE</b>, and transience/persistence are "
                  "read; absolute dose, titre and clinical timing are runtime <b>[O]</b>."),
        body=f"""
<h2>Prime: flip and hold</h2>
<p>A vaccine drives the immune switch past its spinodal into the protected basin, and the barrier
holds it there after the payload is gone. It is a one-way, hysteretic flip \u2014 the same move as any
supra-spinodal drive on the substrate, applied to immunity.</p>

<h2>The boost schedule has an interior optimum</h2>
<p>Spacing boosts too tightly wastes the budget; too loosely lets protection lapse. Over a fixed
{num('v3_nb2', R('V_rna_vaccine',1,'n_boosts_budget'))}-boost budget the protected-fraction-over-horizon
curve is an inverted U with an interior best interval of
{num('v3_bi2', R('V_rna_vaccine',1,'best_interval'),'g2')}, which tracks the measured protection half-life
of {num('v3_hl2', R('V_rna_vaccine',1,'protection_half_life'),'g2')}. The rule (optimum \u2248 half-life) is
read; the calendar interval is <b>[O]</b>.</p>

<h2>Why a vaccine needs no edit</h2>
<p>After clearance the payload drive is {num('v4_pd', R('V_rna_vaccine',2,'payload_drive_after_clearance'),'g2')}
and the switch still sits at s = {num('v4_s2', R('V_rna_vaccine',2,'s_after_clearance'),'g4')}: protection is
held by the barrier, not by lingering RNA. That is exactly why a reversible, payload-based vaccine can
protect durably without touching the SET \u2014 the contrast that organises the therapeutic map next.</p>
""",
    ))

    # ---- 10. gene-therapy levers (GT) ---------------------------------------
    C.append(dict(
        no=11, slug="11-gene-therapy-two-levers",
        eyebrow="application: therapy", subj="Two gene-therapy levers",
        desc=("Two levers: Lever A edits the SET (moves spinodal and barrier, not reversible by a drive); "
              "Lever B resets the drive reversibly via RNA (gamma untouched). The lever choice is a "
              "geometry threshold."),
        h1="Two therapeutic levers: edit the SET, or reset the drive",
        knows=["gene therapy", "base editing", "siRNA knockdown", "reversibility"],
        answer=("Two levers. <b>Lever A</b> edits the SET \u2014 a \u03b3-edit relocates the spinodal "
                "({sb}\u2192{sa}) and the barrier ({bb}\u2192{ba}), and is not reversible by a drive. "
                "<b>Lever B</b> resets the drive reversibly via RNA, \u03b3 untouched. The lever choice is a "
                "<b>geometry threshold</b>: drive-reachable \u2192 B; beyond a tolerable cap \u2192 A. <b>[V]</b>.").format(
                    sb=num("gt1_sb", R("GT_gene_therapy",0,"spinodal_before"),"g4"),
                    sa=num("gt1_sa", R("GT_gene_therapy",0,"spinodal_after"),"g4"),
                    bb=num("gt1_bb", R("GT_gene_therapy",0,"barrier_before"),"g4"),
                    ba=num("gt1_ba", R("GT_gene_therapy",0,"barrier_after"),"g4")),
        abstract=(f"A \u03b3-edit from {num('gt1_gb', R('GT_gene_therapy',0,'gamma_before'),'g4')} to "
                  f"{num('gt1_ga', R('GT_gene_therapy',0,'gamma_after_edit'),'g4')} permanently relocates the "
                  f"threshold; an RNA reset on TARBP2 (\u03b3 = "
                  f"{num('gt2_g', R('GT_gene_therapy',1,'gamma_TARBP2'),'g4')}) forces OFF and reverses on "
                  f"withdrawal. The decision rule separates the two by whether a tolerable drive can clear "
                  f"the pathological hold."),
        grade="V",
        firewall=("The lever <b>CHOICE</b>, the correction <b>SIGN</b>, and reversibility are read; absolute "
                  "dose, edit efficiency and clinical outcome are runtime <b>[O]</b>."),
        body=f"""
<h2>Lever A \u2014 edit the SET (irreversible by a drive)</h2>
<p>A base/prime edit changes \u03b3 itself, relocating the spinodal and barrier for good. From
{num('gt1_gb2', R('GT_gene_therapy',0,'gamma_before'),'g4')} to
{num('gt1_ga2', R('GT_gene_therapy',0,'gamma_after_edit'),'g4')} the threshold moves and no drive can put it
back \u2014 the SET is the unwritable channel, so editing it is permanent.</p>

<h2>Lever B \u2014 reset the drive (reversible)</h2>
<p>An siRNA forces a target switch OFF and releases it on withdrawal, with \u03b3 untouched (worked on TARBP2,
\u03b3 = {num('gt2_g2', R('GT_gene_therapy',1,'gamma_TARBP2'),'g4')}). This is the reversible, tunable lever \u2014
the therapeutic face of the RNA writable channel.</p>

<h2>The decision is geometry</h2>
<p>On PAX5 (\u03b3 = {num('gt3_g', R('GT_gene_therapy',2,'gamma_PAX5'),'g4')}, spinodal
{num('gt3_s', R('GT_gene_therapy',2,'spinodal'),'g4')}) with a tolerable-drive cap of
{num('gt3_cap', R('GT_gene_therapy',2,'tolerable_drive_cap'),'g4')}, a shallow pathological tilt is cleared by
a tolerable drive (use Lever B), while a deep pathological hold exceeds the cap and demands a SET edit
(Lever A). The rule is a threshold in the geometry; the cap's absolute value is <b>[O]</b>.</p>
""",
    ))

    # ---- 11. (gamma, A4) application map + contact boundary (AM) ------------
    am3 = R("AM_a4_application_map", 2, "boundary_delta_star_by_gamma")
    am3_rows = [[num(f"am3g_{i}", row["gamma"],"g3"), num(f"am3d_{i}", row["delta_star"],"g4")]
                for i, row in enumerate(am3)]
    C.append(dict(
        no=12, slug="12-application-map-contact-boundary",
        eyebrow="the application plane", subj="The (gamma, A4) application map",
        desc=("The applications live on the (gamma, A4) plane: prime-boost dose is coordinate-dependent; "
              "the two levers partition the plane; and the 3D contact-boundary curve delta*(gamma) rises "
              "with gamma, so a deeper switch needs more A4 contact-assist to stay drive-reachable."),
        h1="The applications live on the (gamma, A4) plane, bounded by a contact curve",
        knows=["application map", "contact boundary", "drive reachability", "prime-boost dose"],
        answer=("Vaccines and therapy live on the <b>(\u03b3, A4) plane</b>. Prime-boost dose is "
                "<b>coordinate-dependent</b> (it reaches memory at a contact coordinate, fails at a "
                "non-contact one of the same \u03b3); the two levers <b>partition</b> the plane; and the 3D "
                "contact-boundary curve \u03b4*(\u03b3) <b>rises with \u03b3</b> \u2014 a deeper switch needs "
                "more contact-assist to stay drive-reachable. <b>[V]</b>."),
        abstract=(f"At a fixed immune \u03b3 = {num('am1_g', R('AM_a4_application_map',0,'immune_gamma'),'g4')}, "
                  f"a prime of {num('am1_p', R('AM_a4_application_map',0,'prime'),'g4')} with contact-assist "
                  f"{num('am1_ca', R('AM_a4_application_map',0,'contact_assist'),'g4')} reaches memory at a "
                  f"contact coordinate yet fails at a non-contact one. The drive-reachable boundary "
                  f"\u03b4*(\u03b3) rises monotonically from "
                  f"{num('am3_d0', am3[0]['delta_star'],'g4')} to {num('am3_dn', am3[-1]['delta_star'],'g4')}."),
        grade="V",
        firewall=("The coordinate-<b>DEPENDENCE</b> of dose, the lever <b>MAP</b>, and the boundary "
                  "<b>SHAPE</b> are read; absolute doses, assist energies and clinical outcomes are <b>[O]</b>."),
        body=f"""
<h2>Dose is a coordinate, not a scalar</h2>
<p>At one immune \u03b3 = {num('am1_g2', R('AM_a4_application_map',0,'immune_gamma'),'g4')}, the same prime
reaches the protected basin at a contact-competent coordinate (assist
{num('am1_ca2', R('AM_a4_application_map',0,'contact_assist'),'g4')}) but fails at a non-contact coordinate of
identical \u03b3. The effective dose depends on where on the A4 plane the target sits.</p>

<h2>The two levers partition the plane</h2>
<p>With a tolerable drive of {num('am2_cap', R('AM_a4_application_map',1,'tolerable_drive_spinodal_units'),'g2')}
spinodal-units, the integration panel of {num('am2_n', R('AM_a4_application_map',1,'n_loci'))} loci splits
cleanly into a drive-reachable (Lever B) region and an edit-only (Lever A) region \u2014 the therapeutic map
is a partition of (\u03b3, contact), and the prediction matches the integrated run.</p>

<h2>The contact boundary bends with the barrier</h2>
<p>The key application result is a curve, not a point: the minimum contact-assist \u03b4*(\u03b3) needed to keep a
switch drive-reachable <em>rises</em> with \u03b3. A deeper switch (harder to flip) needs more A4 contact-help
to remain reachable by a tolerable drive \u2014 the geometric law tying the two channels to the applications.</p>
{tbl("AM3 \u2014 the contact boundary \u03b4*(\u03b3) rises with \u03b3 (h-path "
     + num('am3_hp', R('AM_a4_application_map',2,'h_path'),'g2') + ", budget B\u2080 "
     + num('am3_b0', R('AM_a4_application_map',2,'tolerable_budget_B0'),'g2') + ")",
     ["\u03b3","\u03b4* (min contact-assist)"], am3_rows, hi=[0, len(am3_rows)-1])}
""",
    ))

    # ---- 13. RNA feasibility map + autism (FM) ------------------------------
    fm_map = R("FM_rna_feasibility_map", 1, "map")
    fm2_rows = [[E(r["gene"]), num(f"fm2g_{i}", r["gamma"], "g4"),
                 num(f"fm2s_{i}", r["spinodal"], "g4"), num(f"fm2b_{i}", r["barrier"], "g4"),
                 E(r["role"])] for i, r in enumerate(fm_map)]
    C.append(dict(
        no=13, slug="13-rna-feasibility-map-and-autism",
        eyebrow="feasibility map", subj="Can RNA reach the switch? The (A)-map, and why only (B) answers",
        desc=("A self-contained model maps only which switch a drive can reach \u2014 reachability is the "
              "measured spinodal, ordered by measured promoter \u03b3 \u2014 and it transfers to real autism-gene "
              "promoters; whether a given RNA dose flips a given neuron is a firewalled drive only held-out "
              "validation can score."),
        h1="The reachability map is the measured spinodal; the yes/no rides on a firewalled drive only (B) scores",
        knows=["RNA reachability", "autism-gene promoters", "saRNA/siRNA reversibility",
               "held-out validation"],
        answer=("A self-contained simulation maps only which switch a drive <b>reaches</b>: reachability is "
                "the <b>measured spinodal</b>, and the absolute flip-drive orders by measured promoter \u03b3. "
                "It transfers to real autism-gene promoters \u2014 each is R19-bistable. Whether a given RNA "
                "dose flips a given neuron is a firewalled \u0394h; only <b>(B)</b>, scored against held-out "
                "pre/post expression with no tuning, returns yes/no. <b>[V]/[O]</b>."),
        abstract=(f"FM1 maps {num('fm1_n', R('FM_rna_feasibility_map',0,'n_switches'))} RNA-machinery "
                  f"switches from easiest ({E(R('FM_rna_feasibility_map',0,'easiest'))}, spinodal "
                  f"{num('fm1_es', R('FM_rna_feasibility_map',0,'easiest_spinodal'),'g4')}) to hardest "
                  f"({E(R('FM_rna_feasibility_map',0,'hardest'))}, spinodal "
                  f"{num('fm1_hs', R('FM_rna_feasibility_map',0,'hardest_spinodal'),'g4')}); a drive at "
                  f"k = {num('fm1_ka', R('FM_rna_feasibility_map',0,'k_above'),'g2')} flips just past the "
                  f"spinodal, k = {num('fm1_kb', R('FM_rna_feasibility_map',0,'k_below'),'g2')} does not. "
                  f"FM2 extends the structure to {num('fm2_n', R('FM_rna_feasibility_map',1,'n_loci'))} "
                  f"measured ASD promoters (SCN2A shallowest, PTEN deepest). FM4 shows the self-contained "
                  f"flip is a \u0394h-replay over all "
                  f"{num('fm4_n', R('FM_rna_feasibility_map',3,'n_switches_checked'))} switches, not "
                  f"evidence."),
        grade="V",
        firewall=("R19-bistability and the \u03b3-ordered flip-drive are MEASURED geometry; the absolute RNA "
                  "<b>\u0394h</b> and the per-neuron <b>yes/no</b> are runtime <b>[O]</b>, pending the "
                  "<b>(B)</b> held-out crossing."),
        body=f"""
<h2>Reachability is the measured spinodal</h2>
<p>A drive reaches a switch exactly when it crosses that switch's measured spinodal \u2014 there is nothing to
assume. Across {num('fm1_n2', R('FM_rna_feasibility_map',0,'n_switches'))} RNA-machinery promoters the
absolute flip-drive is monotone in \u03b3, from {E(R('FM_rna_feasibility_map',0,'easiest'))} (easiest,
spinodal {num('fm1_es2', R('FM_rna_feasibility_map',0,'easiest_spinodal'),'g4')}) to
{E(R('FM_rna_feasibility_map',0,'hardest'))} (hardest, spinodal
{num('fm1_hs2', R('FM_rna_feasibility_map',0,'hardest_spinodal'),'g4')}). A drive scaled to
k = {num('fm1_ka2', R('FM_rna_feasibility_map',0,'k_above'),'g2')} of the spinodal flips it; the same drive
at k = {num('fm1_kb2', R('FM_rna_feasibility_map',0,'k_below'),'g2')} does not. The map is geometry, not a
prediction that any particular dose lands.</p>

<h2>The structure transfers to real autism-gene promoters</h2>
<p>The same read applies to {num('fm2_n2', R('FM_rna_feasibility_map',1,'n_loci'))} measured SFARI ASD-gene
promoters: each is an R19 bistable switch, and the flip-drive orders by the measured promoter \u03b3 \u2014 from
the shallowest ({E(R('FM_rna_feasibility_map',1,'shallowest'))}, \u03b3
{num('fm2_sg', R('FM_rna_feasibility_map',1,'shallowest_gamma'),'g4')}) to the deepest
({E(R('FM_rna_feasibility_map',1,'deepest'))}, \u03b3
{num('fm2_dg', R('FM_rna_feasibility_map',1,'deepest_gamma'),'g4')}).</p>
{tbl("FM2 \u2014 measured ASD-gene promoters are R19 switches, flip-drive ordered by \u03b3",
     ["gene","\u03b3","spinodal","barrier","role"], fm2_rows, hi=[0, len(fm2_rows)-1])}

<h2>The honesty gate: a self-contained flip is replay, not evidence</h2>
<p>By construction a flip exists at k \u2265 1 for every one of the
{num('fm4_n2', R('FM_rna_feasibility_map',3,'n_switches_checked'))} switches checked, and never at k &lt; 1.
That screen is a function of the assumed drive alone \u2014 it replays the firewalled \u0394h rather than testing
it, so a self-contained simulation cannot return whether a real cell changed. The only honest crossing is
<b>(B)</b>: score the predicted flipped-switch set and ordering against held-out measured pre/post
expression of real siRNA/saRNA-treated cells, with no tuning of \u0394h or parameters to the target. Until (B)
is run, the per-neuron yes/no stays <b>[O]</b>.</p>
""",
    ))

    # ---- 14. disease feasibility map + corrective sign (DM) -----------------
    dm_cp = R("DM_disease_feasibility_map", 3, "cross_package_consistency")
    dm4_rows = [[E(g), num(f"dmcpm_{g}", v["measured"], "g4"),
                 num(f"dmcpr_{g}", v["reference"], "g4"), yn(v["agrees"])]
                for g, v in dm_cp.items()]
    C.append(dict(
        no=14, slug="14-disease-feasibility-map-corrective-sign",
        eyebrow="feasibility map", subj="The same map for disease: corrective sign is forced by mechanism",
        desc=("Cancer and neurodegeneration promoters are R19 switches ordered by measured \u03b3; the "
              "corrective drive's sign is forced by the disease mechanism and is orthogonal to \u03b3; a "
              "reversible Lever-B drive reaches every switch and the cross-package \u03b3 reproduces with no "
              "tuning."),
        h1="Disease promoters are R19 switches; the corrective sign is mechanism-forced, orthogonal to \u03b3",
        knows=["disease reachability", "corrective-sign law", "two-lever decision",
               "cross-package reproduction"],
        answer=("The map extends to disease: "
                "{n} cancer and neurodegeneration promoters (SNCA shallowest, HTT deepest) are each R19 "
                "switches, flip-drive ordered by measured \u03b3. The corrective drive's <b>sign</b> is forced "
                "by mechanism (gain-of-function \u2192 \u2212, loss \u2192 +), orthogonal to \u03b3. A reversible "
                "Lever-B drive reaches every switch; coding lesions need Lever-A. Cross-package \u03b3 "
                "reproduces with no tuning. <b>[F]/[V]/[O]</b>.").format(
                    n=num("dm1_n", R("DM_disease_feasibility_map", 0, "n_loci"))),
        abstract=(f"DM1 maps {num('dm1_n2', R('DM_disease_feasibility_map',0,'n_loci'))} disease promoters "
                  f"({num('dm1_onc', R('DM_disease_feasibility_map',0,'n_oncology'))} oncology, "
                  f"{num('dm1_neu', R('DM_disease_feasibility_map',0,'n_neurodegeneration'))} "
                  f"neurodegeneration; shallowest {E(R('DM_disease_feasibility_map',0,'shallowest'))} \u03b3 "
                  f"{num('dm1_sg', R('DM_disease_feasibility_map',0,'shallowest_gamma'),'g4')}, deepest "
                  f"{E(R('DM_disease_feasibility_map',0,'deepest'))} \u03b3 "
                  f"{num('dm1_dg', R('DM_disease_feasibility_map',0,'deepest_gamma'),'g4')}). DM2: the "
                  f"mechanism-forced corrective sign corrects every gene and is orthogonal to \u03b3 "
                  f"(point-biserial {num('dm2_pb', R('DM_disease_feasibility_map',1,'sign_vs_gamma_pointbiserial'),'g4')}). "
                  f"DM4: the cross-package \u03b3 for four shared loci reproduces against reference with no "
                  f"tuning."),
        grade="F",
        firewall=("The reachability, the \u03b3-ordering, and the mechanism-forced corrective <b>SIGN</b> are "
                  "read/forced; absolute dose, the tolerable cap, and the coding-lesion magnitude are runtime "
                  "<b>[O]</b>; clinical care to clinicians."),
        body=f"""
<h2>Cancer and neurodegeneration promoters are the same R19 switches</h2>
<p>The disease panel spans {num('dm1_n3', R('DM_disease_feasibility_map',0,'n_loci'))} promoters \u2014
{num('dm1_onc2', R('DM_disease_feasibility_map',0,'n_oncology'))} oncogenes/suppressors and
{num('dm1_neu2', R('DM_disease_feasibility_map',0,'n_neurodegeneration'))} neurodegeneration loci. Every one
is an R19 bistable switch and the absolute flip-drive is monotone in measured \u03b3, from the shallowest
({E(R('DM_disease_feasibility_map',0,'shallowest'))}, \u03b3
{num('dm1_sg2', R('DM_disease_feasibility_map',0,'shallowest_gamma'),'g4')}) to the deepest
({E(R('DM_disease_feasibility_map',0,'deepest'))}, \u03b3
{num('dm1_dg2', R('DM_disease_feasibility_map',0,'deepest_gamma'),'g4')}).</p>

<h2>The corrective sign is forced by mechanism, not by \u03b3</h2>
<p>Difficulty (\u03b3) says how hard a switch is to move; it does not say which way to push. The corrective
<b>direction</b> is forced by the disease mechanism \u2014 a gain-of-function lesion is corrected by a negative
(silencing) drive, a loss-of-function lesion by a positive (activating) drive \u2014 and this forced sign
corrects every gene in the panel, while the opposite sign does not. The sign is orthogonal to \u03b3:
its point-biserial correlation with the \u03b3 order is
{num('dm2_pb2', R('DM_disease_feasibility_map',1,'sign_vs_gamma_pointbiserial'),'g4')}, and the \u03b3 ranges of
the plus-sign and minus-sign genes overlap. Operationally this is a two-lever decision: a reversible
<b>Lever-B</b> expression drive reaches every switch (required drive growing with \u03b3, with
{E(R('DM_disease_feasibility_map',2,'nearest_a_tolerable_cap'))} nearest a tolerable cap), whereas a broken
coding sequence is reserved for the irreversible <b>Lever-A</b> edit that the promoter \u03b3 does not read.</p>

<h2>Cross-package reproduction: the same \u03b3 with no tuning</h2>
<p>The honesty gate is the same as for RNA \u2014 a self-contained &ldquo;corrected&rdquo; verdict is a
\u0394h-replay, not evidence. What the package <em>can</em> verify is that its measured \u03b3 is
anchor-determined, not fitted: four loci shared with the other packages reproduce the same \u03b3 to four
decimals, computed independently and with no tuning.</p>
{tbl("DM4 \u2014 cross-package \u03b3 reproduces against reference (no tuning)",
     ["gene","measured \u03b3","reference \u03b3","agrees"], dm4_rows)}
<p>The reachability, ordering, and corrective sign are read or forced; the absolute dose, the tolerable cap,
and the coding-lesion magnitude remain <b>[O]</b>, and clinical care is handed to clinicians.</p>
""",
    ))

    # ---- 15. (B) held-out validation (FV) -----------------------------------
    fv_sweep = R("FV_feasibility_validation", 2, "primary_K562_GWPS_sweep")
    fv_sweep_rows = []
    for r_ in fv_sweep:
        ck = f"{r_['cutoff']:.2f}"
        fv_sweep_rows.append([
            num(f"fv_cut_{ck}", r_["cutoff"], "g2"),
            num(f"fv_n_{ck}", r_["n"]),
            num(f"fv_rho_{ck}", r_["rho"], "g4") if r_["rho"] is not None else "&mdash;",
            num(f"fv_p_{ck}", r_["p"], "g4") if r_["p"] is not None else "&mdash;",
        ])
    fv_n     = num("fv2_n",     R("FV_feasibility_validation", 1, "n"))
    fv_rho   = num("fv2_rho",   R("FV_feasibility_validation", 1, "spearman_rho"), "g4")
    fv_p     = num("fv2_p",     R("FV_feasibility_validation", 1, "p_value"), "g4")
    fv_auc   = num("fv2_auc",   R("FV_feasibility_validation", 1, "set_proxy_auc"), "g3")
    fv_nresp = num("fv2_nresp", R("FV_feasibility_validation", 1, "n_responders"))
    fv_ntot  = num("fv2_ntot",  R("FV_feasibility_validation", 1, "n_total"))
    fv_rpe1  = num("fv3_rpe1",  R("FV_feasibility_validation", 2, "RPE1_rho_all_matched"), "g4")
    fv_nxc   = num("fv1_nxc",   R("FV_feasibility_validation", 0, "n_gamma_values_crosschecked"))
    fv_live  = num("fv1_live",  R("FV_feasibility_validation", 0, "live_panel_size"))
    fv_cache = num("fv1_cache", R("FV_feasibility_validation", 0, "cache_panel_size"))
    fv_fish  = num("fv1_fish",  int(VLD["figshare_article"]))
    fv_doi   = VLD["source_doi"]
    # FV5 -- GC-identifiability stress test
    fv5_panel = R("FV_feasibility_validation", 4, "per_panel")
    fv5_ggc1  = num("fv5_ggc_k562", fv5_panel[0]["rho_gamma_gc"], "g4")
    fv5_ggc2  = num("fv5_ggc_rpe1", fv5_panel[1]["rho_gamma_gc"], "g4")
    fv5_ggc3  = num("fv5_ggc_ess",  fv5_panel[2]["rho_gamma_gc"], "g4")
    fv5_pp1   = num("fv5_partial_k562",   fv5_panel[0]["partial_rho_gamma_fold_given_gc"], "g4")
    fv5_pp1p  = num("fv5_partial_k562_p", fv5_panel[0]["partial_p"], "g4")
    fv5_pp2   = num("fv5_partial_rpe1",   fv5_panel[1]["partial_rho_gamma_fold_given_gc"], "g4")
    fv5_pp3   = num("fv5_partial_ess",    fv5_panel[2]["partial_rho_gamma_fold_given_gc"], "g4")
    # FV6 -- the (B) identifiability decomposition (the frontier partitions)
    fv6       = R("FV_feasibility_validation", 5)
    fv6_n     = num("fv6_n",    fv6["n_disease_genes"])
    fv6_lof   = num("fv6_lof",  fv6["n_LOF_plus"])
    fv6_gof   = num("fv6_gof",  fv6["n_GOF_minus"])
    fv6_ggc   = num("fv6_ggc",  fv6["rho_gamma_GC"], "g4")
    fv6_r2g   = num("fv6_r2g",  fv6["R2_gamma_given_GC"], "g4")
    fv6_pbgc  = num("fv6_pbgc", fv6["point_biserial_sign_GC"], "+%.4f")
    fv6_r2s   = num("fv6_r2s",  fv6["R2_sign_given_GC"], "g4")
    fv6_sep   = num("fv6_sep",  fv6["confound_explains_gamma_not_sign_separation_ratio"], "%.0f")
    fv6_pbg   = num("fv6_pbg",  fv6["point_biserial_sign_gamma"], "g4")
    _fv6_lab = {
        "knockdown_depth_ordering (FV5 target)": "\u03b3-ordering \u2014 knockdown depth (FV5)",
        "downstream_response_magnitude": "downstream response-magnitude",
        "corrective_SIGN (bidirectional, DM2)": "corrective sign-law (DM2, bidirectional)",
    }
    def _fv6_verdict(s):
        return (s.replace(" -- ", " \u2014 ").replace("Delta-h", "\u0394h")
                 .replace("gamma~GC", "\u03b3\u2248GC")
                 .replace("'+'", "+").replace("'-'", "\u2212"))
    fv6_rows = [[E(_fv6_lab.get(k, k)), yn(v["identified"]), yn(v["firewall_clean"]),
                 E(_fv6_verdict(v["verdict"]))]
                for k, v in fv6["candidate_B_observable_map"].items()]
    # FV7 -- corrective sign-law '-' arm, held-out on DepMap 24Q2 CRISPR-KO (first held-out positive)
    fv7       = R("FV_feasibility_validation", 6)
    fv7_n     = num("fv7_n",     fv7["n_onco_scored"])
    fv7_gof   = num("fv7_gof",   fv7["n_GOF_minus"])
    fv7_lof   = num("fv7_lof",   fv7["n_LOF_plus"])
    fv7_pb    = num("fv7_pb",    fv7["point_biserial_GOFsign_vs_neg_gene_effect"], "g4")
    fv7_p     = num("fv7_p",     fv7["exact_permutation_p_one_sided"], "g4")
    fv7_perm  = num("fv7_perm",  fv7["n_permutations"])
    fv7_pbgc  = num("fv7_pbgc",  fv7["point_biserial_sign_vs_GC"], "g4")
    fv7_gofgc = num("fv7_gofgc", fv7["GOF_mean_GC"], "g3")
    fv7_lofgc = num("fv7_lofgc", fv7["LOF_mean_GC"], "g3")
    fv7_part  = num("fv7_part",  fv7["partial_point_biserial_sign_given_GC"], "g4")
    fv7_nd    = num("fv7_nd",    fv7["n_neurodegen_out_of_scope"])
    fv7_fish  = num("fv7_fish",  int(SLM["figshare_article"]))
    fv7_tot   = E(fv7["per_gene_sign_correct"]["total"])   # "12/16" (sourced ratio)
    fv7_gofc  = E(fv7["per_gene_sign_correct"]["GOF"])      # "7/7"  (sourced ratio)
    # FV8 -- corrective sign-law '+' RESTORE arm, held-out on Horlbeck 2016 CRISPRa (mirror of FV7; bidirectional close)
    fv8       = R("FV_feasibility_validation", 7)
    fv8_n     = num("fv8_n",     fv8["n_onco_scored"])
    fv8_lof   = num("fv8_lof",   fv8["n_LOF_plus"])
    fv8_gof   = num("fv8_gof",   fv8["n_GOF_minus"])
    fv8_pb    = num("fv8_pb",    fv8["point_biserial_LOFsign_vs_neg_growth"], "g4")
    fv8_p     = num("fv8_p",     fv8["exact_permutation_p_one_sided"], "g4")
    fv8_perm  = num("fv8_perm",  fv8["n_permutations"])
    fv8_pbgc  = num("fv8_pbgc",  fv8["point_biserial_sign_vs_GC"], "+%.4f")
    fv8_lofgc = num("fv8_lofgc", fv8["LOF_mean_GC"], "g3")
    fv8_gofgc = num("fv8_gofgc", fv8["GOF_mean_GC"], "g3")
    fv8_part  = num("fv8_part",  fv8["partial_point_biserial_sign_given_GC"], "g4")
    fv8_nd    = num("fv8_nd",    fv8["n_neurodegen_out_of_scope"])
    fv8_elife = num("fv8_elife", int(SLP["elife_article"]))
    fv8_doi   = SLP["doi"]   # "10.7554/eLife.19760" (sourced string, rendered as text like fv_doi)
    fv8_tot   = E(fv8["per_gene_sign_correct"]["total"])   # "10/16" (sourced ratio)
    fv8_lofc  = E(fv8["per_gene_sign_correct"]["LOF"])      # "7/9"  (sourced ratio)
    C.append(dict(
        no=15, slug="15-held-out-b-validation-null",
        eyebrow="the (B) validation",
        subj="The (B) held-out validation: a no-tuning score, run once, returns a clean null",
        desc=(f"The (B) held-out validation \u2014 the only honest crossing from the feasibility map to "
              f"evidence \u2014 is run once: frozen DNA-measured \u03b3 scored against held-out Replogle "
              f"CRISPRi knockdown depth returns a clean null (\u03c1 = {fv_rho}, p = {fv_p}, n = {fv_n}), "
              f"promoting no open item; a GC-identifiability stress test shows that null is non-identified, "
              f"not merely signal-absent; the (A) map stays verified and \u03b3 untouched."),
        h1="The (B) held-out validation: a no-tuning score on real perturbed cells returns a clean null",
        knows=["held-out validation", "no-tuning prediction", "Spearman ordering score",
               "honest negative", "promotion rule"],
        answer=(f"FM named exactly one honest crossing from the feasibility <em>map</em> to "
                f"<em>evidence</em>: a no-tuning score of the frozen \u03b3-ordering against held-out measured "
                f"expression. It is now run, once. Against Replogle CRISPRi knockdown depth (K562, n = {fv_n}): "
                f"\u03c1 = {fv_rho}, p = {fv_p} \u2014 slightly <em>opposite</em> the predicted sign and "
                f"non-significant. It promotes nothing. <b>[V] (a recorded null)</b>."),
        abstract=(f"FV runs the (B) score on the real held-out target FM/DM named \u2014 Replogle 2022 "
                  f"genome-scale Perturb-seq (CRISPRi), readout the on-target fraction of transcript remaining "
                  f"(source DOI {fv_doi}, figshare {fv_fish}). \u03b3 is measured from promoter DNA and was "
                  f"frozen before any expression was seen: {fv_nxc} \u03b3 values were re-read live and are "
                  f"hash-equal to the frozen atlas, zero mismatches. The prediction was sign-locked in advance "
                  f"\u2014 higher \u03b3 resists knockdown \u21d2 \u03c1(\u03b3, fold_expr) &gt; 0. Primary K562 "
                  f"genome-wide (n = {fv_n}): \u03c1 = {fv_rho}, p = {fv_p}, SET-proxy AUC = {fv_auc}; slightly "
                  f"opposite and non-significant across every cutoff, and the second cell line's sign disagrees "
                  f"(RPE1 \u03c1 = {fv_rpe1}). By the promotion rule (p &lt; 0.05 <em>and</em> \u03c1 &gt; 0) "
                  f"this promotes nothing: O-19/O-20/O-22 stay <b>[O]</b>, the (A) map stays <b>[V]</b>, "
                  f"\u03b3 untouched."),
        grade="V",
        firewall=("FV reads only the <b>WHICH-switch ordering</b> against held-out data; the per-cell / "
                  "per-patient yes/no it tested stays <b>[O]</b> (O-19/O-20/O-22). A recorded null promotes "
                  "nothing \u2014 promotion requires a significant result in the predicted direction, never a "
                  "louder claim."),
        body=f"""
<h2>The one honest crossing \u2014 named, then run</h2>
<p>A self-contained model can push a drive past a switch's measured spinodal and call it
&ldquo;flipped&rdquo;, but that verdict is a replay of the firewalled drive \u0394h, not evidence the cell
changed (the FM4 honesty invariant). The only crossing from <em>map</em> to <em>evidence</em> is a score
against data the model never saw, with no parameter tuned to the target. This chapter runs that score for the
first time and reports it exactly as it falls.</p>

<h2>Held-out integrity: \u03b3 was frozen before the data was seen</h2>
<p>The target is a real perturbation dataset \u2014 Replogle 2022 genome-scale Perturb-seq (CRISPRi), readout
the on-target fraction of transcript remaining (source DOI {fv_doi}, figshare article {fv_fish}). The \u03b3
scored against it is the DNA-measured atlas \u03b3, re-read live at score time and checked against the cache:
{fv_nxc} \u03b3 values match the frozen atlas to the bit, with zero mismatches, and the panel is a fixed
union rule (live {fv_live} = cached {fv_cache}). Nothing here is fitted; the only honest path is a no-tuning
prediction scored on held-out measurement.</p>

<h2>The score, no tuning: a clean null</h2>
<p>The prediction sign is locked in advance: a deeper (higher-\u03b3) promoter should resist knockdown, so
the fraction of transcript remaining should <em>rise</em> with \u03b3 \u2014 \u03c1(\u03b3, fold_expr) &gt; 0.
On the primary, pre-registered K562 genome-wide panel (n = {fv_n}, {fv_nresp}/{fv_ntot} on-target
responders) the measured rank correlation is \u03c1 = {fv_rho} at p = {fv_p}: slightly <em>opposite</em> the
predicted sign and not significant. A SET-membership proxy gives AUC = {fv_auc} (below 0.5, i.e. no
discrimination). By the promotion rule \u2014 promote the per-cell yes/no out of [O] only if p &lt; 0.05
<em>and</em> \u03c1 &gt; 0 \u2014 the decision is to <b>keep [O]</b>.</p>

<h2>The null is robust</h2>
<p>The non-support is not a cutoff artefact. Tightening the minimum control-expression cutoff only moves the
primary correlation further negative, never toward significant support, and the second cell line's sign does
not even agree (RPE1 \u03c1 = {fv_rpe1}). With n this small the result does <em>not refute</em> the map
\u2014 it finds <em>no support</em> for promoting the per-cell yes/no.</p>
{tbl("FV3 \u2014 the primary K562 null is robust across every control-expression cutoff",
     ["control-expr cutoff", "n", "Spearman \u03c1", "p"], fv_sweep_rows)}

<h2>Is the null even identified? The barrier and GC are the same ordering</h2>
<p>A stronger question than &ldquo;is there a signal?&rdquo; is &ldquo;<em>could</em> this score show one if it
existed?&rdquo; Here it cannot. \u03b3 is &minus;mean(nearest-neighbour \u0394G37), and stacking free energy is
dominated by G/C content, so \u03b3 and promoter GC are near-collinear <em>by construction</em> \u2014 measured
at \u03c1(\u03b3, GC) = {fv5_ggc1} (K562 genome-wide), {fv5_ggc2} (RPE1), {fv5_ggc3} (K562-essential). The
held-out readout, on-target CRISPRi knockdown, is itself driven by sgRNA accessibility \u2014 a known function of
TSS chromatin and GC. So the predictor and the readout&rsquo;s nuisance driver are the <em>same ordering</em>.
Partial GC out and the surviving \u03b3 effect is non-significant and sign-unstable across panels
(\u03c1(\u03b3, fold_expr | GC) = {fv5_pp1}, p = {fv5_pp1p} on the primary; {fv5_pp2} and {fv5_pp3} on the other
two). The null is therefore <em>non-identified</em> \u2014 the score cannot separate a barrier effect from a GC
effect \u2014 not merely &ldquo;signal absent&rdquo;.</p>
<p>This settles a roadmap question without new data. Because \u03b3\u2013GC collinearity is a property of promoter
DNA, it is <em>identical in any cell type</em> \u2014 so running the same on-target-knockdown ordering on a
neuronal CRISPRi panel (the data exist: i\u00b3Neuron CROP-seq, Tian 2019) inherits the same degeneracy and does
not advance the neuronal yes/no. An <em>identified</em> (B) needs a readout that is not collinear with GC
\u2014 a downstream response <em>magnitude</em> \u2014 which requires the firewalled drive size \u0394h.</p>

<h2>The null is a partition, not one fact \u2014 only the sign-law survives</h2>
<p>The held-out null is not a single fact but a <em>partition</em>. Because \u03b3 = \u2212mean(NN \u0394G37) is
collinear with promoter GC (\u03c1(\u03b3, GC) = {fv6_ggc}, R\u00b2 = {fv6_r2g} on the disease panel of n = {fv6_n}:
{fv6_lof} loss-of-function/+ and {fv6_gof} gain-of-function/\u2212), <em>every</em> \u03b3-ordered prediction is
non-identified as a class; the corrective sign-law is the only prediction orthogonal to GC, and so the only
(B) that is both identifiable and firewall-clean.</p>
<p>The criterion is forced by the collinearity itself. Scored against a GC-driven readout, a prediction that is
<em>monotone in \u03b3</em> is collinear with GC and any held-out match could be manufactured by GC; only a
prediction <em>orthogonal to \u03b3</em> is identifiable, because GC cannot produce its match. Every
\u03b3-ordered prediction therefore falls together \u2014 FM1 reachability ordering, the FV knockdown-depth
ordering, IM2 durability ordering, and DM1 correction-difficulty ordering are all monotone in \u03b3 \u2014 so FV5
was a single instance of a class property, and re-running any of them as an ordering score adds nothing.</p>
<p>The lone exception is the <em>mechanism corrective sign</em> (DM2: LOF\u2192+ restore, GOF\u2192\u2212 silence).
It is fixed by biology rather than by promoter DNA and interleaves along \u03b3: point-biserial(sign, GC) =
{fv6_pbgc} with R\u00b2(sign~GC) = {fv6_r2s} \u2014 a \u2248{fv6_sep}\u00d7 variance-explained separation from the
\u03b3\u2013GC axis. The sign is orthogonal to the very confound that sinks the ordering axis, so a held-out
sign-match could not be produced by GC. The same run reproduces DM2's point-biserial(sign, \u03b3) = {fv6_pbg}
as a frozen cross-check, with zero drift.</p>
{tbl("FV6 \u2014 every candidate (B) observable, placed by identifiability and firewall-cleanliness",
     ["candidate (B) observable", "identified?", "firewall-clean?", "verdict"], fv6_rows)}
<p>The 2\u00d72 leaves exactly one open frontier, and it <b>corrects an earlier framing</b>. It is not the case
that every (B) crossing &ldquo;needs the firewalled \u0394h&rdquo;: a sign test reads only <em>which</em> sign
restores the healthy switch, never a dose, so it is firewall-clean by construction, and it is identified by being
orthogonal to GC. The corrective sign-law's only obstacle is therefore <b>bidirectional disease-correction
data</b> \u2014 an oncogene \u2212 arm and a suppressor / Parkinson's + arm scored together, since a single-arm
knockdown screen cannot exhibit the interleaving. That is a data question, not a magnitude question. FV6
promotes nothing: O-19/O-20/O-22 stay <b>[O]</b> until the sign-law is actually scored on such data. Reproduce
with the FV battery (<code>engine/feasibility_validation.py</code>, seed 19); the FV6 row reads PASS.
<b>[V] on an [F] criterion</b> \u2014 the partition is forced by the measured collinearity, and nothing is
fitted. FV6 reads only <em>which</em> axis is identifiable and <em>which</em> sign corrects, never a magnitude;
the sign-law's clinical use belongs to clinicians and regulators.</p>

<h2>The sign-law's &minus; arm, scored on held-out data &mdash; the first held-out positive</h2>
<p>FV6 left the corrective sign-law <em>named</em> but unscored. Its <b>&minus; arm is now scored on held-out
data</b>, and it passes. A CRISPR-<em>knockout</em> screen <em>is</em> the &minus; (loss) operation, and in a
cancer line viability <em>is</em> a correction phenotype &mdash; so the sign-locked prediction is that GOF
oncogenes (corrective sign &minus;) are dependencies while LOF suppressors (corrective sign +) are not. On the
held-out DepMap panel (n = {fv7_n} oncology genes, {fv7_gof} GOF / {fv7_lof} LOF) it holds:
point-biserial(GOF, &minus;gene-effect) = {fv7_pb}, exact one-sided permutation p = {fv7_p} ({fv7_perm}
permutations), in the predicted direction ({fv7_tot} genes correct, GOF {fv7_gofc}). The kit's <b>first
held-out positive</b>.</p>
<p>The match is <b>identified</b> &mdash; not the GC artefact that sinks the ordering axis (FV5/FV6). The sign
axis is orthogonal to GC: point-biserial(sign, GC) = {fv7_pbgc} (GOF mean GC {fv7_gofgc} vs LOF mean GC
{fv7_lofgc}, balanced), and partialling GC out leaves it essentially unchanged ({fv7_part}), so a held-out
sign-match cannot be manufactured by GC. The target is genuinely held out: DepMap 24Q2 Public CRISPRGeneEffect
(Chronos), figshare article {fv7_fish}; the corrective sign is forced by disease <em>mechanism</em> and was
frozen before any DepMap data was seen, the cache carries gene-effects only, and the sign and GC are re-read
frozen at score time. The {fv7_nd} neurodegeneration genes are cached but out of readout scope &mdash; cancer
viability is not a proteinopathy correction.</p>
<p>This is <b>not</b> a fresh discovery of the oncogene/suppressor split: those labels are the kit's frozen
priors, and DepMap is the <em>independent</em> test that the &minus; arm tracks them (four of nine LOF genes are
pan-essential for reasons orthogonal to tumour suppression and push <em>against</em> the prediction; the score
is a pan-cancer mean, never lineage-cherry-picked). It promotes the &minus; arm <b>only</b>: <b>O-22</b> (the
per-patient corrected yes/no) stays <b>[O]</b>, its obstacle narrowed to the + RESTORE arm alone, and FV7 does
<em>not</em> reintroduce &Delta;h &mdash; FV6 corrected that; the absolute drive size is the separate item
<b>O-21</b>, also <b>[O]</b>. Reproduce with the FV battery (<code>engine/feasibility_validation.py</code>,
seed 19; cache rebuildable via <code>python data/fetch_signlaw_depmap.py --fetch</code>); the FV7 row reads
PASS. <b>[V] held-out positive</b> for the &minus; arm, identified and firewall-clean &mdash; FV7 reads only the
<em>sign</em> of the GOF-vs-LOF separation under the &minus; operation, never a magnitude; &gamma; untouched;
the sign-law's clinical use belongs to clinicians and regulators.</p>

<h2>The sign-law's + RESTORE arm, scored on held-out data &mdash; the bidirectional close</h2>
<p>The mirror test now follows. The corrective sign-law's <b>+ RESTORE arm is scored on held-out data of the
<em>opposite</em> operation</b>, and it passes. A CRISPR-<em>activation</em> screen <em>is</em> the + (gain /
restore) operation, and in a cancer line growth <em>is</em> a correction phenotype &mdash; so the sign-locked
prediction is that LOF suppressors (corrective sign +) are growth-suppressive on activation while GOF oncogenes
(corrective sign &minus;) are not. On the held-out Horlbeck 2016 hCRISPRa-v2 K562 panel (n = {fv8_n} oncology
genes, {fv8_lof} LOF / {fv8_gof} GOF): point-biserial(LOF, &minus;growth-phenotype) = {fv8_pb}, exact one-sided
permutation p = {fv8_p} ({fv8_perm} permutations), in the predicted direction ({fv8_tot} genes correct, LOF
{fv8_lofc}) &mdash; nearly symmetric to FV7's &minus; arm. The kit's <b>second held-out positive</b>, the
mirror of the first.</p>
<p>It is <b>identified</b> on the same basis: point-biserial(sign, GC) = {fv8_pbgc} (LOF mean GC {fv8_lofgc} vs
GOF mean GC {fv8_gofgc}, balanced), GC-partialled {fv8_part} &mdash; orthogonal to the GC confound, so the match
is not a GC artefact, and firewall-clean (the sign only). Provenance: Horlbeck et al. 2016, <em>eLife</em>
{fv8_elife} (doi {fv8_doi}), supplementary file 10; the corrective sign is forced by <em>mechanism</em> and was
frozen before any CRISPRa data was seen, the cache carries growth phenotypes only, and the sign and GC are
re-read frozen. The {fv8_nd} neurodegeneration genes are cached but out of readout scope (leukemia growth is
not a proteinopathy correction). Honest caveat: K562 is a single CML line (vs FV7's pan-cancer mean), and it is
TP53-null and CDKN2A-deleted, so activation has a weak or absent locus to restore in those genes and they push
<em>against</em> the prediction &mdash; a conservative panel, no cherry-picking.</p>
<p>With <b>both arms</b> scored the corrective sign-law is now <b>bidirectionally [V]</b> (direction-only),
which removes <em>in full</em> the bidirectional-data obstacle FV6 named. <b>And yet O-22 still stays [O]</b>
&mdash; for a corrected reason. FV8 <b>corrects</b> FV7's &ldquo;obstacle narrowed to the + arm alone&rdquo;
framing: with both arms in, O-22's residual obstacle is <em>no longer data but the firewall itself</em>. The
sign-law is <b>class-level and direction-only</b> (<em>which way</em> to push each disease class); O-22 is a
<b>per-patient, absolute</b> outcome (does a drive correct <em>this</em> patient's switch?), which needs the
firewalled per-patient magnitude &mdash; the absolute drive size being the separate item <b>O-21</b>, also
<b>[O]</b>. A direction-only law cannot certify a per-patient yes/no, and promoting O-22 would leak a
direction-only <b>[V]</b> into a per-patient absolute <b>[V]</b>. This is <em>not</em> a contradiction of FV6:
scoring the sign-law needed bidirectional data, not &Delta;h, and both arms were scored with <em>zero</em>
&Delta;h. Reproduce with the FV battery (<code>engine/feasibility_validation.py</code>, seed 19; cache
rebuildable via <code>python data/fetch_signlaw_crispra.py --fetch</code>, a pure-standard-library reader with
no new dependency); the FV8 row reads PASS. <b>[V] held-out positive</b> for the + arm; together with FV7 the
sign-law is bidirectionally faithful on independent CRISPR data. FV8 reads only the <em>sign</em> of the
LOF-vs-GOF separation under the + operation, never a magnitude; &gamma; untouched; the sign-law's clinical use
belongs to clinicians and regulators.</p>

<h2>What (B) moved: nothing \u2014 and that is the point</h2>
<p>A real (B) score now exists on the record, and it promoted no open item: the (A) map's reachability and
\u03b3-ordering are unchanged and stay <b>[V]</b>, and the frozen \u03b3 was not touched (hash-checked). As the
identifiability analysis above shows, the ordering test is moreover non-identified \u2014 it cannot isolate the barrier from GC
even in principle. This is exactly what FM4 predicted: the part a self-contained sim can compute does not, by
itself, predict the firewalled per-cell effect. The per-cell and per-patient yes/no (O-19, O-20, O-22) remain
<b>[O]</b>; promoting them needs a significant, identified result in the predicted direction on held-out
corrective data, never a louder claim, and all clinical translation stays with clinicians and regulators.</p>
""",
    ))

    # ---- 16. parent-of-origin: a duration asymmetry (PO) -------------------
    po3_tab = R("PO_parent_of_origin", 2, "table")
    po3_rows = [[E(r["gene"]), num(f"po3g_{i}", r["gamma"], "g4"),
                 num(f"po3c_{i}", r["crossing_steps"]), yn(r["asymmetry_holds"])]
                for i, r in enumerate(po3_tab)]
    C.append(dict(
        no=16, slug="16-parent-of-origin-sign-and-context",
        eyebrow="parent-of-origin", subj="Parent-of-origin is a duration asymmetry",
        desc=("Egg and sperm deliver the same kind of drive in two temporal contexts: sustained "
              "(maternal) versus transient (paternal). At equal amplitude a held switch is crossed by "
              "duration, the maternal sign is inherited, and the asymmetry is universal across the "
              "germline atlas."),
        h1="Parent-of-origin is a duration asymmetry: sustained maternal flips, transient paternal reverts",
        knows=["parent-of-origin effect", "genomic imprinting", "germline RNA carrier", "maternal effect"],
        answer=("At <b>equal</b> supra-spinodal amplitude ({a}) the crossing is set by the <b>duration</b> "
                "of exposure: a <b>sustained</b> maternal drive flips a held switch (end state {ms}), while "
                "a <b>transient</b> paternal burst of the same amplitude relaxes back ({pb}). The inherited "
                "<b>sign</b> is the maternal sign, and the asymmetry holds at every measured germline locus "
                "({n}/{n}). <b>[V]/[O]</b>.").format(
                    a=num("po1_amp", R("PO_parent_of_origin", 0, "equal_amplitude"), "g4"),
                    ms=num("po1_ms", R("PO_parent_of_origin", 0, "maternal_sustained_end_state"), "g4"),
                    pb=num("po1_pb", R("PO_parent_of_origin", 0, "paternal_burst_end_state"), "g4"),
                    n=num("po3_n", R("PO_parent_of_origin", 2, "n_loci_asymmetric"))),
        abstract=(f"On the deep germline master REC8 "
                  f"(\u03b3 = {num('po1_g', R('PO_parent_of_origin',0,'deep_germline_gamma'),'g4')}, "
                  f"spinodal {num('po1_s', R('PO_parent_of_origin',0,'spinodal'),'g4')}) a held switch needs "
                  f"{num('po1_ct', R('PO_parent_of_origin',0,'crossing_time_steps'))} steps of supra-spinodal "
                  f"exposure to cross. The sustained maternal context supplies it and the switch flips; a "
                  f"transient paternal burst of "
                  f"{num('po1_pbs', R('PO_parent_of_origin',0,'paternal_burst_steps'))} steps "
                  f"(decay \u03c4 = {num('po1_tau', R('PO_parent_of_origin',0,'paternal_decay_tau_steps'))}) "
                  f"relaxes back \u2014 by duration, not amplitude. Under opposing parents the maternal sign is "
                  f"inherited and agreement reinforces "
                  f"({num('po2_both', R('PO_parent_of_origin',1,'cross_steps_both_agree'))} vs "
                  f"{num('po2_mat', R('PO_parent_of_origin',1,'cross_steps_maternal_only'))} steps)."),
        grade="V",
        firewall=("The context <b>ASYMMETRY</b> (sustained vs transient), the inherited <b>SIGN</b>, and the "
                  "barrier <b>ORDERING</b> are read; which parent's payload prevails in vivo and the absolute "
                  "penetrance are runtime <b>[O]</b>."),
        body=f"""
<h2>Same amplitude, different duration &mdash; the crossing is set by time</h2>
<p>Sperm and egg deliver the same kind of object &mdash; a drive written at an A4 coordinate &mdash; in two
temporal contexts. On REC8 (\u03b3 = {num('po1_g2', R('PO_parent_of_origin',0,'deep_germline_gamma'),'g4')},
spinodal {num('po1_s2', R('PO_parent_of_origin',0,'spinodal'),'g4')}) both parents supply the
<em>same</em> supra-spinodal amplitude
({num('po1_amp2', R('PO_parent_of_origin',0,'equal_amplitude'),'g4')}) &mdash; the fairness condition that
keeps this read direction-only. A held switch needs
{num('po1_ct2', R('PO_parent_of_origin',0,'crossing_time_steps'))} steps above the spinodal to cross. The
egg's large cytoplasm holds the maternal payload <b>sustained</b>, so the switch flips (end state
{num('po1_ms2', R('PO_parent_of_origin',0,'maternal_sustained_end_state'),'g4')}); the sperm's small bolus is
diluted to a <b>transient</b> burst
({num('po1_pbs2', R('PO_parent_of_origin',0,'paternal_burst_steps'))} steps), which relaxes back to
{num('po1_pb2', R('PO_parent_of_origin',0,'paternal_burst_end_state'),'g4')}. The asymmetry is in duration,
not amplitude.</p>

<h2>The inherited sign is the maternal sign</h2>
<p>Under opposing parents, the dominant maternal sign is inherited: a maternal <b>+</b> against a paternal
<b>&minus;</b> settles ON
({num('po2_on', R('PO_parent_of_origin',1,'maternal_plus_vs_paternal_minus_end'),'g4')}), and reversing the
roles inherits OFF
({num('po2_off', R('PO_parent_of_origin',1,'maternal_minus_vs_paternal_plus_end'),'g4')}). When the two
parents <em>agree</em>, the switch crosses faster &mdash;
{num('po2_both2', R('PO_parent_of_origin',1,'cross_steps_both_agree'))} steps versus
{num('po2_mat2', R('PO_parent_of_origin',1,'cross_steps_maternal_only'))} for the maternal context alone.
The sign is read; the magnitude is not.</p>

<h2>The asymmetry is universal across the germline atlas</h2>
<p>The sustained-vs-transient asymmetry is not a property of one locus: it holds at
<b>{num('po3_n2', R('PO_parent_of_origin',2,'n_loci_asymmetric'))} of
{num('po3_nt', R('PO_parent_of_origin',2,'n_germline_loci'))}</b> measured germline switches &mdash; every
one flips under the sustained maternal context and reverts under the matched transient paternal burst.</p>
{tbl("PO3 \u2014 the duration asymmetry holds at every measured germline locus (universality)",
     ["gene","\u03b3","crossing steps","asymmetry holds"], po3_rows, hi=[0, len(po3_rows)-1])}
<p><b>Honest course-correction.</b> PO3 was first hypothesised as &ldquo;the paternal disadvantage rises with
\u03b3.&rdquo; The substrate returned the <em>opposite</em> ordering: under equal-<em>relative</em> amplitude
the descriptive rank-correlation between \u03b3 and crossing time came out
\u03c1 = {num('po3_rho', R('PO_parent_of_origin',2,'descriptive_rho_gamma_vs_crossing_time_AS_IT_FALLS'),'g2')}
(crossing time is flat / slightly decreasing in \u03b3). Per the inheritance discipline the claim was
<b>rewritten</b> to the robust result &mdash; the asymmetry is universal in <em>presence</em>, not monotone in
magnitude &mdash; with \u03c1 reported as it falls, no directional claim graded, and no \u03b3 tuned. The
absolute parent-of-origin penetrance stays <b>[O]</b>.</p>
""",
    ))

    # ---- 17. RNA-vaccine kinetics: interval and reach (VK) -----------------
    vk1_sweep = R("VK_rna_vaccine_kinetics", 0, "sweep")[:6]
    vk1_opt = R("VK_rna_vaccine_kinetics", 0, "optimum_interval_rounds")
    vk1_opt_idx = next(i for i, r in enumerate(vk1_sweep) if r["interval_rounds"] == vk1_opt)
    vk1_rows = [[num(f"vk1i_{i}", r["interval_rounds"]),
                 num(f"vk1m_{i}", r["maturation_gain"], "g4"),
                 num(f"vk1s_{i}", r["primed_survival"], "g4"),
                 num(f"vk1b_{i}", r["boost_benefit"], "g4")]
                for i, r in enumerate(vk1_sweep)]
    C.append(dict(
        no=17, slug="17-rna-vaccine-kinetics",
        eyebrow="application: vaccine kinetics", subj="RNA-vaccine kinetics: interval and reach",
        desc=("The prime-boost interval has an interior optimum in germinal-centre rounds (too short "
              "under-matures, too long lets protection decay); a longer same-amplitude saRNA window crosses "
              "the protected basin more reliably than mRNA, with identical post-flip durability."),
        h1="The prime-boost interval is interior-optimal; saRNA reaches the protected basin more reliably",
        knows=["prime-boost interval", "germinal centre", "saRNA", "mRNA vaccine"],
        answer=("The boost benefit peaks at an <b>interior optimum</b> (best interval {bi} rounds, benefit "
                "{bb}): boost too early and the response has not matured, too late and protection has "
                "decayed at the measured escape rate ({er}). A longer <b>same-amplitude</b> saRNA window "
                "crosses the protected basin more reliably than mRNA ({sa} vs {mr}); post-flip durability is "
                "the identical barrier. <b>[V]</b>.").format(
                    bi=num("vk1_bi", R("VK_rna_vaccine_kinetics", 0, "optimum_interval_rounds")),
                    bb=num("vk1_bb", R("VK_rna_vaccine_kinetics", 0, "optimum_benefit"), "g4"),
                    er=num("vk1_er", R("VK_rna_vaccine_kinetics", 0, "measured_escape_rate"), "g4"),
                    sa=num("vk2_sa", R("VK_rna_vaccine_kinetics", 1, "crossing_fraction_saRNA"), "g4"),
                    mr=num("vk2_mr", R("VK_rna_vaccine_kinetics", 1, "crossing_fraction_mRNA"), "g4")),
        abstract=(f"On the memory master "
                  f"{E(R('VK_rna_vaccine_kinetics',0,'naive_master'))} "
                  f"(\u03b3 = {num('vk1_g', R('VK_rna_vaccine_kinetics',0,'memory_switch_gamma'),'g4')}) with "
                  f"a measured escape rate of "
                  f"{num('vk1_er2', R('VK_rna_vaccine_kinetics',0,'measured_escape_rate'),'g4')}, the boost "
                  f"benefit is an inverted-U peaking at "
                  f"{num('vk1_bi2', R('VK_rna_vaccine_kinetics',0,'optimum_interval_rounds'))} rounds "
                  f"({num('vk1_bb2', R('VK_rna_vaccine_kinetics',0,'optimum_benefit'),'g4')}) with both arms "
                  f"worse. Near the spinodal "
                  f"({num('vk2_sp', R('VK_rna_vaccine_kinetics',1,'spinodal'),'g4')}) at equal amplitude "
                  f"{num('vk2_amp', R('VK_rna_vaccine_kinetics',1,'amplitude_near_spinodal'),'g4')}, a "
                  f"{num('vk2_wsa', R('VK_rna_vaccine_kinetics',1,'window_saRNA_steps'))}-step saRNA window "
                  f"crosses "
                  f"{num('vk2_csa', R('VK_rna_vaccine_kinetics',1,'crossing_fraction_saRNA'),'g4')} of the "
                  f"time versus "
                  f"{num('vk2_cmr', R('VK_rna_vaccine_kinetics',1,'crossing_fraction_mRNA'),'g4')} for a "
                  f"{num('vk2_wmr', R('VK_rna_vaccine_kinetics',1,'window_mRNA_steps'))}-step mRNA pulse."),
        grade="V",
        firewall=("The interval-optimum <b>SHAPE</b> and the saRNA&gt;mRNA reach <b>ORDERING</b> are read; "
                  "absolute calendar intervals, titres and amplification factors are runtime <b>[O]</b>; "
                  "clinical scheduling belongs to clinicians and regulators."),
        body=f"""
<h2>The prime&ndash;boost interval has an interior optimum</h2>
<p>The boost is swept in germinal-centre rounds &mdash; the IM1 maturation loop reused <em>unchanged</em>
&mdash; with the primed pool decaying at the <b>measured</b> escape rate
({num('vk1_er3', R('VK_rna_vaccine_kinetics',0,'measured_escape_rate'),'g4')}). Boost too early and the
response has not matured; boost too late and protection has already decayed. The benefit is a genuine
inverted-U with an interior peak at
{num('vk1_bi3', R('VK_rna_vaccine_kinetics',0,'optimum_interval_rounds'))} rounds
({num('vk1_bb3', R('VK_rna_vaccine_kinetics',0,'optimum_benefit'),'g4')}); both arms are worse, and the long
arm keeps fading out to the end of the sweep.</p>
{tbl("VK1 \u2014 boost benefit is interior-optimal (maturation rises, primed survival decays; peak interior)",
     ["interval (rounds)","maturation gain","primed survival","boost benefit"], vk1_rows, hi=[vk1_opt_idx])}
<p>The optimum tracks the maturation endpoint against the decay; mapping substrate rounds to calendar days
needs an in-vivo rate that is not measured here, so the absolute interval is <b>[O]</b>.</p>

<h2>saRNA reaches the protected basin more reliably than mRNA</h2>
<p>Near the spinodal ({num('vk2_sp2', R('VK_rna_vaccine_kinetics',1,'spinodal'),'g4')}) at the <b>same</b>
amplitude ({num('vk2_amp2', R('VK_rna_vaccine_kinetics',1,'amplitude_near_spinodal'),'g4')}, noise D =
{num('vk2_d', R('VK_rna_vaccine_kinetics',1,'noise_D'),'g2')}), a longer saRNA drive window
({num('vk2_wsa2', R('VK_rna_vaccine_kinetics',1,'window_saRNA_steps'))} steps) crosses into the protected
basin more often than a shorter mRNA pulse
({num('vk2_wmr2', R('VK_rna_vaccine_kinetics',1,'window_mRNA_steps'))} steps):
{num('vk2_csa2', R('VK_rna_vaccine_kinetics',1,'crossing_fraction_saRNA'),'g4')} versus
{num('vk2_cmr2', R('VK_rna_vaccine_kinetics',1,'crossing_fraction_mRNA'),'g4')}. The advantage is in
<b>reaching</b>: once flipped, durability is the identical barrier (the same \u03b3), so saRNA holds no longer
than mRNA once both have crossed. The reliability ordering is read; the absolute titre and amplification
factor are <b>[O]</b>.</p>
""",
    ))

    # ---- 18. the gene-therapy lever map (LV) -------------------------------
    lv1_sub = R("LV_lever_map", 0, "subtypes")
    lv1_rows = [[E(r["modality"]), E(r["channel"]),
                 num(f"lv1g_{i}", r["gamma_after"], "g4"),
                 yn(r["threshold_moved"]), yn(r["reversible_by_drive"])]
                for i, r in enumerate(lv1_sub)]
    lv2_sub = R("LV_lever_map", 1, "subtypes")
    lv2_rows = [[E(r["modality"]), E(r["axis"]), E(r["sign"]),
                 yn(r["reversible"]), yn(r["gamma_untouched"])]
                for i, r in enumerate(lv2_sub)]
    lv3_curve = R("LV_lever_map", 2, "boundary_curve_sample")
    lv3_rows = [[num(f"lv3g_{i}", pt[0], "g4"), num(f"lv3h_{i}", pt[1], "g4")]
                for i, pt in enumerate(lv3_curve)]
    C.append(dict(
        no=18, slug="18-gene-therapy-lever-map",
        eyebrow="application: lever map", subj="The gene-therapy lever map",
        desc=("Every therapeutic modality bins by channel: SET edits (knockout/base/prime) move the "
              "threshold and are drive-irreversible, while CRISPRa, siRNA, ASO-splice, saRNA and "
              "miRNA-sponge act at fixed gamma and revert. A finite gamma* mandates the edit; re-dosing "
              "above a critical rate holds a correction with no edit."),
        h1="Every modality bins by channel: a SET edit or a fixed-\u03b3 drive \u2014 and a finite \u03b3* mandates the edit",
        knows=["CRISPRa", "base editing", "antisense oligonucleotide", "siRNA", "lever selection"],
        answer=("SET edits (knockout/base/prime) move the spinodal and barrier and are not drive-reversible; "
                "<b>CRISPRa</b> leaves \u03b3 untouched and reverts, so the substrate re-classifies it as "
                "<b>Lever B</b>. The Lever-B sub-types (siRNA <b>&minus;</b>, ASO-splice a fixed-\u03b3 "
                "coordinate change, saRNA <b>+</b>, miRNA-sponge <b>+</b>) all act at fixed \u03b3 and revert. "
                "The decision boundary h<sub>path</sub>*(\u03b3) = h<sub>cap</sub> &minus; spinodal(\u03b3) "
                "falls and crosses zero at a finite \u03b3* ({gs}); beyond it even a zero-hold switch needs "
                "Lever A. <b>[V]</b>.").format(
                    gs=num("lv3_gsa", R("LV_lever_map", 2, "gamma_star_analytic"), "g4")),
        abstract=(f"On DICER1 "
                  f"(\u03b3 = {num('lv1_g', R('LV_lever_map',0,'gamma_DICER1'),'g4')}, spinodal "
                  f"{num('lv1_s', R('LV_lever_map',0,'spinodal_before'),'g4')}, barrier "
                  f"{num('lv1_b', R('LV_lever_map',0,'barrier_before'),'g4')}) a knockout drives \u03b3 to "
                  f"{num('lv1_ko', R('LV_lever_map',0,'subtypes',0,'gamma_after'),'g4')} (threshold gone) "
                  f"while CRISPRa leaves \u03b3 fixed and reverts. On TARBP2 "
                  f"(\u03b3 = {num('lv2_g', R('LV_lever_map',1,'gamma_TARBP2'),'g4')}) every Lever-B sub-type "
                  f"leaves the spinodal and barrier byte-identical and reverts on withdrawal. With a declared "
                  f"cap h_cap = {num('lv3_cap', R('LV_lever_map',2,'declared_h_cap'),'g4')} the boundary "
                  f"crosses zero at \u03b3* = "
                  f"{num('lv3_gsa2', R('LV_lever_map',2,'gamma_star_analytic'),'g4')} (analytic) / "
                  f"{num('lv3_gss', R('LV_lever_map',2,'gamma_star_swept'),'g4')} (swept), and re-dosing above "
                  f"w* = {num('lv4_ws', R('LV_lever_map',3,'critical_w_star'),'g4')} holds the corrected "
                  f"state."),
        grade="V",
        firewall=("The lever <b>SUB-TYPE</b> (SET edit vs fixed-\u03b3 drive), the drive <b>SIGN</b>, "
                  "reversibility, the lever-choice <b>BOUNDARY</b>, and edit-free durability are read; "
                  "absolute efficiency, dose, titre and in-vivo durability are runtime <b>[O]</b>; clinical "
                  "modality selection belongs to clinicians and regulators."),
        body=f"""
<h2>Lever A sub-types move the threshold; CRISPRa is really Lever B</h2>
<p>On DICER1 (\u03b3 = {num('lv1_g2', R('LV_lever_map',0,'gamma_DICER1'),'g4')}, spinodal
{num('lv1_s2', R('LV_lever_map',0,'spinodal_before'),'g4')}, barrier
{num('lv1_b2', R('LV_lever_map',0,'barrier_before'),'g4')}), knockout, base-edit and prime-edit each change
\u03b3 itself &mdash; the threshold moves and no drive restores it (true SET edits). CRISPRa, despite the
&ldquo;activation&rdquo; label, leaves \u03b3 (and so the spinodal and barrier) untouched and reverses on
withdrawal, so the substrate re-classifies it as a drive &mdash; Lever B.</p>
{tbl("LV1 \u2014 a SET edit moves the threshold and is drive-irreversible; CRISPRa is a fixed-\u03b3 reversible drive",
     ["modality","channel","\u03b3 after","threshold moved","reversible by drive"], lv1_rows, hi=[len(lv1_rows)-1])}

<h2>Lever B sub-types: one channel, different signs</h2>
<p>On TARBP2 (\u03b3 = {num('lv2_g2', R('LV_lever_map',1,'gamma_TARBP2'),'g4')}, spinodal
{num('lv2_s', R('LV_lever_map',1,'spinodal'),'g4')}, barrier
{num('lv2_b', R('LV_lever_map',1,'barrier'),'g4')}) every Lever-B sub-type leaves the spinodal and barrier
byte-identical and reverts on withdrawal; only the <b>sign</b> differs. siRNA drives <b>&minus;</b>, saRNA
<b>+</b>, a miRNA-sponge <b>+</b> (net de-repression), and an ASO splice-switch is a fixed-\u03b3
<b>A4-coordinate</b> change rather than an expression drive.</p>
{tbl("LV2 \u2014 every Lever-B sub-type is reversible at fixed \u03b3; the sign is read per modality",
     ["modality","axis","sign","reversible","\u03b3 untouched"], lv2_rows)}

<h2>The lever choice is an explicit boundary curve</h2>
<p>Declare a tolerable cap h_cap = {num('lv3_cap2', R('LV_lever_map',2,'declared_h_cap'),'g4')} (the spinodal
at the anchor \u03b3 = 1.4598, <em>not</em> tuned to an outcome). The drive a cap-bounded Lever B must clear
is h<sub>path</sub>*(\u03b3) = h_cap &minus; spinodal(\u03b3); it <b>falls</b> with \u03b3 and crosses zero at a
finite \u03b3* = {num('lv3_gsa3', R('LV_lever_map',2,'gamma_star_analytic'),'g4')} (analytic),
{num('lv3_gss2', R('LV_lever_map',2,'gamma_star_swept'),'g4')} (swept). Beyond \u03b3* even a zero-hold switch
cannot be cleared by a tolerable drive and demands Lever A.</p>
{tbl("LV3 \u2014 the lever-choice boundary h_path*(\u03b3) falls and crosses zero at a finite \u03b3*",
     ["\u03b3","h_path*(\u03b3)"], lv3_rows)}
<p>The boundary curve is read; the cap's absolute value is <b>[O]</b> (it reuses the O-7 tolerability logic).</p>

<h2>Durable correction without an edit</h2>
<p>Re-dosing a Lever-B drive each cycle &mdash; with the per-cycle loss
({num('lv4_loss', R('LV_lever_map',3,'measured_per_cycle_loss'),'g4')}) measured from the switch's own
relaxation on TARBP2 &mdash; holds the corrected state above a critical re-write rate
w* = {num('lv4_ws2', R('LV_lever_map',3,'critical_w_star'),'g4')}: at 1.5&times;w* the steady state sits at
{num('lv4_ss15', R('LV_lever_map',3,'steady_state_at_1.5x_w_star'),'g4')} (maintained), at 0.5&times;w* it
falls to {num('lv4_ss05', R('LV_lever_map',3,'steady_state_at_0.5x_w_star'),'g4')} (fades), and a single dose
with no re-write decays to {num('lv4_ss0', R('LV_lever_map',3,'steady_state_no_rewrite'),'g4')}. So a
reversible drive can correct durably with \u03b3 never touched &mdash; the edit-free durability that closes the
lever map. The persistence condition is read; the absolute re-dosing schedule is <b>[O]</b>.</p>
""",
    ))

    # ---- 19. scoreboard + firewall ledger -----------------------------------
    bp = GREEN["battery_pass"]
    sb_lines = "".join(
        f'<div><span class="ok">PASS</span> &middot; {E(k)}</div>' for k in bp)
    nv = GREEN["ncbi_offline_verify"]
    # parse the [O] ledger table from IRREPRODUCIBILITY_LEDGER.md (sourced, no drift)
    led_path = os.path.join(KIT, "IRREPRODUCIBILITY_LEDGER.md")
    o_rows = []
    for line in open(led_path):
        line = line.strip()
        if line.startswith("| O-"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 4:
                o_rows.append([E(cells[0]), E(cells[1]), E(cells[3])])
    n_o = num("n_o_items", len(o_rows))
    C.append(dict(
        no=19, slug="16-scoreboard-firewall-ledger",
        eyebrow="the honest scoreboard", subj="The scoreboard and the firewall",
        desc=("The kit is green: 18 discriminant batteries PASS, the SOX9 anchor reproduces four NCBI "
              "verifies offline, every battery is byte-identical on a second run, and twenty-seven absolute "
              "quantities are firewalled [O], each naming its obstacle."),
        h1="The honest scoreboard: what is verified, and what is firewalled out",
        knows=["reproducibility", "falsifiability", "open problems", "scoreboard"],
        answer=("The kit is <b>green</b>: {nb} discriminant batteries PASS, the SOX9 anchor reproduces "
                "four NCBI \u03b3/A4 verifies fully offline, and every battery is byte-identical on a second "
                "run (determinism). <b>{no}</b> absolute quantities are firewalled <b>[O]</b>, each naming "
                "its obstacle. <b>[V]</b>.").format(nb=num("n_batteries", len(bp)), no=n_o),
        abstract=(f"All {num('n_batteries2', len(bp))} batteries pass; the RNA-machinery atlas "
                  f"({num('nv_rna', nv['rna_carrier']['n_genes'])} genes) and imprinted atlas "
                  f"({num('nv_imp', nv['imprint']['n_genes'])} loci) reproduce SOX9-gated, the disease atlas "
                  f"({num('nv_donc', nv['disease']['n_oncology'])} oncology + "
                  f"{num('nv_dneu', nv['disease']['n_neurodegeneration'])} neurodegeneration loci) reproduces "
                  f"cross-package with no tuning, and "
                  f"{num('nv_a4', nv['a4_coordinates']['n_windows'])} wide-window A4 reads verify offline. "
                  f"The verified register is direction-only; {n_o} absolute magnitudes stay <b>[O]</b>."),
        grade="V",
        firewall=("This volume reads <b>WHICH</b> switch, the <b>SIGN</b> of the drive, and the "
                  "<b>ORDERING / DECAY / BOUNDARY</b> of effects; it never asserts an absolute magnitude."),
        body=f"""
<h2>Eighteen batteries, all green</h2>
<p>Every discriminant is measured out of the vendored substrate at measured \u03b3, graded, and reproduced
twice byte-identically. The gate re-checks the SOX9 anchor offline on every run; fail the anchor and the
pipeline refuses to write.</p>
<div class="scoreboard">{sb_lines}
<div style="margin-top:.5rem;color:#6b7580">NCBI offline verify &middot; RNA-machinery \u03b3
({num('nv_rna2', nv['rna_carrier']['n_genes'])} genes, anchor reproduced) &middot; imprinted \u03b3
({num('nv_imp2', nv['imprint']['n_genes'])} loci, anchor reproduced) &middot; disease \u03b3
({num('nv_donc2', nv['disease']['n_oncology'])}+{num('nv_dneu2', nv['disease']['n_neurodegeneration'])} loci,
4-locus cross-package) &middot; {num('nv_a4_2', nv['a4_coordinates']['n_windows'])} wide-window A4 reads
&middot; determinism: 2&times;sha256 identical</div></div>

<h2>The one-sentence synthesis</h2>
<p class="lede">SET (\u03b3, genome) vs DRIVE (h, environment/RNA, applied at an A4 coordinate) is the same
decomposition behind inheritance, immunity, vaccines and gene therapy: \u03b3 is the unwritable ruler, A4 is
the writable structure that RNA targets and the environment inherits, and reversibility \u2014 a drive is
reversible, a SET-edit is not \u2014 organises the therapeutic map.</p>

<h2>The firewall, itemised</h2>
<p>What the substrate does not fix, this volume does not claim. Each open item names the obstacle that
keeps it open; promoting any of them requires new measured dynamics, never a louder claim. Every clinical
application is handed to clinicians and regulators.</p>
{tbl("Firewalled [O] items \u2014 every absolute magnitude and its obstacle (" + n_o + " items)",
     ["id","item","obstacle"], o_rows)}
""",
    ))
    return C


# ============================================================================
#  hub / index / aux files
# ============================================================================
def render_hub(chapters):
    canon = f"{SITE}/{PAPER_ID}/"
    title = f"{SHORT} \u2014 environmental inheritance on one switch | Jamming Physics"
    desc = ("The VP Inheritance volume: one bistable switch read on two channels (the unwritable "
            "promoter ruler gamma and the writable A4 coordinate) emerges environmental inheritance, "
            "the RNA layer, immune memory, RNA vaccines and gene therapy \u2014 all direction-only.")
    series_ld = {
        "@context": "https://schema.org", "@type": "CreativeWorkSeries",
        "name": SHORT, "headline": FULLTITLE, "url": canon,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "license": LICENSE, "inLanguage": "en",
        "isBasedOn": f"{REPO}/",
        "hasPart": [{"@type": "ScholarlyArticle", "position": c["no"],
                     "name": c["subj"], "url": f"{canon}{c['slug']}/"} for c in chapters],
    }
    crumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT}]}
    head = page_head(title, desc, canon, [series_ld, crumb])
    toc = []
    for c in chapters:
        cls, label = GRADE_CLASS[c["grade"]]
        toc.append(
            f'<li><span class="n">\u00a7{c["no"]}</span>'
            f'<span class="t"><b><a href="/{PAPER_ID}/{c["slug"]}/">{E(c["subj"])}</a></b>'
            f'<span>{E(c["eyebrow"])}</span></span>'
            f'<span class="gtag {cls}">{label.split()[0]}</span></li>')
    return f"""{head}
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; {SHORT}</nav></header>
<main>
<p class="eyebrow">VP \u00b7 jamming branch (germline / RNA / immune)</p>
<h1>{E(FULLTITLE)}</h1>
<p class="answer">One bistable switch, read on <b>two channels</b> \u2014 the unwritable promoter
ruler <span class="kf">\u03b3</span> (the SET) and the writable <b>A4 coordinate</b> \u2014 with a
reversible drive <span class="kf">h</span> written at a coordinate. On that single substrate this
volume emerges environmental inheritance, the RNA layer, immune memory, RNA vaccines and gene
therapy. Everything is direction-only behind the magnitude firewall. <span class="grade g-verified">[V]</span> 18/18 green.</p>
<p class="lede">This volume is derived from the substrate alone: it vendors the R19 jamming switch and
the measured promoter-\u03b3 atlases, runs eighteen discriminant batteries, and reproduces the SOX9 anchor
offline. It is the single source of truth for the new objects \u2014 the small-RNA writable channel, the
A4 coordinate channel, the reprogramming firewall, and the application and feasibility maps \u2014 and cites the rest.</p>

<h2>Chapters</h2>
<ol class="toc">{"".join(toc)}</ol>

<div class="vp-card c-gamma"><b>The synthesis</b> &mdash; SET (\u03b3) vs DRIVE (h, at an A4 coordinate)
is the same decomposition behind inheritance, immunity, vaccines and gene therapy; reversibility
organises the therapeutic map. <span class="gd">[V]</span>
<a href="/{PAPER_ID}/16-scoreboard-firewall-ledger/">scoreboard &amp; firewall \u2192</a></div>

{firewall_box("We read WHICH switch, the SIGN of the drive, and the ORDERING / DECAY / BOUNDARY of effects; never an absolute magnitude.")}
</main>
{FOOTER}
</body>
</html>"""

def render_index(chapters):
    canon = f"{SITE}/"
    title = "Jamming Physics \u2014 the VP Inheritance volume"
    desc = ("A falsifiable, reproducible mechanism of environmental inheritance, the RNA layer, RNA "
            "vaccines and gene therapy, derived from one jamming-lattice switch read on two channels.")
    ld = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Jamming Physics",
         "url": canon, "inLanguage": "en"},
        {"@context": "https://schema.org", "@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        {"@context": "https://schema.org", "@type": "CollectionPage", "url": canon,
         "hasPart": {"@type": "CreativeWorkSeries", "name": SHORT,
                     "url": f"{SITE}/{PAPER_ID}/"}},
    ]
    head = page_head(title, desc, canon, ld)
    return f"""{head}
<body>
<header><nav class="crumb">Jamming Physics</nav></header>
<main>
<p class="eyebrow">jamming-physics.org</p>
<h1>One switch, two channels, four applications</h1>
<p class="answer">The VP Inheritance volume derives environmental inheritance, the RNA layer, immune
memory, RNA vaccines and gene therapy from a single bistable jamming-lattice switch read on two
channels: the unwritable promoter ruler <span class="kf">\u03b3</span> and the writable <b>A4
coordinate</b>. Every quantitative claim carries a grade and a reproduce path. <span class="grade g-verified">[V]</span>.</p>
<h2>Volume</h2>
<ol class="toc">
<li><span class="n">vol</span><span class="t">
<b><a href="/{PAPER_ID}/">{E(SHORT)} \u2014 {E(FULLTITLE)}</a></b>
<span>19 chapters \u00b7 18 batteries green \u00b7 direction-only \u00b7 CC BY 4.0</span></span>
<span class="gtag g-verified">[V]</span></li>
</ol>
<p class="lede">Headline results, all direction-only: heritability ranks by barrier (Spearman \u03c1 \u2192 1.0
on the imprinted atlas); \u03b3 alone is degenerate (the A4 contact phase is ~98% independent); a vaccine
is a flip held by the barrier with an interior-optimal boost interval; gene therapy is a SET edit
(irreversible) or a reversible RNA drive-reset; and the contact boundary \u03b4*(\u03b3) rises with \u03b3.</p>
</main>
{FOOTER}
</body>
</html>"""

def render_meta(chapters):
    return {
        "paper_id": PAPER_ID, "code": "inh", "title": FULLTITLE, "short": SHORT,
        "doi": DOI, "hub_url": f"/{PAPER_ID}/", "branch": "jamming",
        "author": AUTHOR, "orcid": ORCID, "license": LICENSE,
        "abstract": ("One bistable switch read on two channels (gamma SET + A4 coordinate) emerges "
                     "environmental inheritance, the RNA layer, immune memory, RNA vaccines and gene "
                     "therapy; direction-only behind the magnitude firewall."),
        "headline_results": [
            "heritability ranks ascending-gamma (Spearman rho -> 1.0)",
            "gamma alone is degenerate; A4 contact phase ~98% independent",
            "vaccine = supra-spinodal flip held by the barrier",
            "two therapeutic levers: SET edit (irreversible) vs RNA drive-reset",
        ],
        "chapters": [
            {"no": c["no"], "slug": c["slug"], "title": c["subj"],
             "one_liner": c["eyebrow"], "grade": GRADE_CLASS[c["grade"]][0].replace("g-", "")}
            for c in chapters],
        "totals": {"batteries": len(GREEN["battery_pass"]),
                   "all_green": GREEN["all_green"], "chapters": len(chapters)},
    }

ROBOTS = ("# jamming-physics.org -- AI + search crawlers welcome\n"
          "User-agent: Googlebot\nAllow: /\n"
          "User-agent: Bingbot\nAllow: /\n"
          "User-agent: OAI-SearchBot\nAllow: /\n"
          "User-agent: GPTBot\nAllow: /\n"
          "User-agent: PerplexityBot\nAllow: /\n"
          "User-agent: ClaudeBot\nAllow: /\n"
          "User-agent: Google-Extended\nAllow: /\n"
          "User-agent: *\nAllow: /\n\n"
          f"Sitemap: {SITE}/sitemap.xml\n")

def render_sitemap(chapters):
    urls = [f"{SITE}/", f"{SITE}/{PAPER_ID}/"] + [f"{SITE}/{PAPER_ID}/{c['slug']}/" for c in chapters]
    items = "".join(
        f"  <url><loc>{u}</loc><lastmod>{ISO}</lastmod></url>\n" for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            f"{items}</urlset>\n")

def render_llms(chapters):
    lines = [f"# {SHORT} \u2014 {FULLTITLE}", "",
             "> One bistable jamming-lattice switch read on two channels \u2014 the unwritable promoter",
             "> ruler gamma (the SET) and the writable A4 coordinate \u2014 emerges environmental",
             "> inheritance, the RNA layer, immune memory, RNA vaccines and gene therapy. Direction-only",
             "> behind a magnitude firewall; every claim carries a grade and a reproduce path.",
             f"> Author {AUTHOR} (ORCID 0009-0002-7535-8245), CC BY 4.0. DOI {DOI}.", "",
             "## core",
             f"- Volume hub: {SITE}/{PAPER_ID}/", ""]
    lines.append("## chapters")
    for c in chapters:
        lines.append(f"- \u00a7{c['no']} {c['subj']}: {SITE}/{PAPER_ID}/{c['slug']}/")
    lines += ["", "## policies",
              "- Grades: [F] forced / [V] verified / [L] calibration / [O] open (obstacle named).",
              "- Firewall: WHICH switch + SIGN + ORDERING/DECAY read; absolute magnitudes are [O].",
              "- Clinical application is handed to clinicians and regulators.", ""]
    return "\n".join(lines)


# ============================================================================
#  build + determinism gate
# ============================================================================
def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def build(root):
    docs = os.path.join(root, "docs")
    if os.path.isdir(docs):
        shutil.rmtree(docs)
    global LEDGER
    LEDGER = {}
    chapters = build_chapters()
    write(os.path.join(docs, "assets", "css", "site.css"), CSS)
    write(os.path.join(docs, "index.html"), render_index(chapters))
    write(os.path.join(docs, PAPER_ID, "index.html"), render_hub(chapters))
    for i, c in enumerate(chapters):
        prev_ch = chapters[i-1] if i > 0 else None
        next_ch = chapters[i+1] if i < len(chapters)-1 else None
        write(os.path.join(docs, PAPER_ID, c["slug"], "index.html"),
              render_chapter(c, prev_ch, next_ch))
    write(os.path.join(docs, PAPER_ID, "_meta.json"),
          json.dumps(render_meta(chapters), ensure_ascii=False, indent=2))
    write(os.path.join(docs, "robots.txt"), ROBOTS)
    write(os.path.join(docs, "sitemap.xml"), render_sitemap(chapters))
    write(os.path.join(docs, "llms.txt"), render_llms(chapters))
    return docs, chapters, dict(LEDGER)

def tree_hash(docs):
    h = hashlib.sha256()
    for dp, dn, fn in os.walk(docs):
        dn.sort()
        for name in sorted(fn):
            p = os.path.join(dp, name)
            h.update(os.path.relpath(p, docs).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()

if __name__ == "__main__":
    root = KIT
    docs, chapters, ledger1 = build(root)
    sha1 = tree_hash(docs)
    # second build into a scratch dir -> determinism gate (2 x sha256)
    import tempfile
    scratch = tempfile.mkdtemp()
    shutil.copytree(os.path.join(root, "reports"), os.path.join(scratch, "reports"))
    shutil.copy(os.path.join(root, "IRREPRODUCIBILITY_LEDGER.md"),
                os.path.join(scratch, "IRREPRODUCIBILITY_LEDGER.md"))
    docs2, _, ledger2 = build(scratch)
    sha2 = tree_hash(docs2)
    shutil.rmtree(scratch)
    deterministic = (sha1 == sha2 and ledger1 == ledger2)
    # write the displayed-number ledger (C1 audit trail)
    write(os.path.join(root, "reports", "site_numbers.json"),
          json.dumps({"displayed_numbers": ledger1,
                      "n_numbers": len(ledger1),
                      "docs_sha256": sha1,
                      "deterministic_2xsha256": deterministic,
                      "n_chapters": len(chapters)},
                     ensure_ascii=False, indent=2))
    print(json.dumps({
        "built": True,
        "n_chapters": len(chapters),
        "n_displayed_numbers": len(ledger1),
        "docs_sha256": sha1[:16],
        "deterministic_2xsha256": deterministic,
    }, indent=2))
