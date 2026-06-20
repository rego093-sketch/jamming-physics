#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_multipage_analgesic.py — generate the analgesic_threshold_logic site as a
multi-page canonical HTML edition, mirroring vp_physics_v0_11_0 structure under VP-SPEC v1.8.

Layout produced (under docs/):
  docs/assets/css/site.css                      (canonical VP-SPEC stylesheet + analgesic badges)
  docs/analgesic/index.html                     (hub: CollectionPage + CreativeWorkSeries hasPart + ToC)
  docs/analgesic/{slug}/index.html              (one §6 self-contained page per section AND per target)
  docs/robots.txt  docs/sitemap.xml  docs/llms.txt
  docs/analgesic/_meta.json

Discipline (unchanged, non-negotiable): every page is answer-first + self-contained (C4/6-R),
carries JSON-LD ScholarlyArticle + BreadcrumbList, a claim-strip, prev/next nav, footer.
gamma reads promoter switch-threshold STRUCTURE only; every clinical magnitude is [O].
No DOI fabricated (pending). All gamma/|h_sp| values byte-faithful to the canonical engine JSON.
"""
import json, os, html, shutil, datetime, re

PKG = "/home/claude/work/analgesic_handover_v1_to_v2/analgesic_threshold_logic_v2_0"
DOCS = f"{PKG}/docs"
TMAP = json.load(open(f"{PKG}/repro/03-threshold-map/expected/threshold_map.json"))
PRIO = json.load(open(f"{PKG}/repro/10-burden-prioritisation/expected/priority_ranking.json"))
PREC = json.load(open(f"{PKG}/repro/12-precision-local-anaesthesia/expected/precision_block_map.json"))

REPO = "https://github.com/rego093-sketch/jamming-physics"
REPRO_URL = f"{REPO}/tree/main/repro"
ORCID = "https://orcid.org/0009-0002-7535-8245"
SITE = "https://jamming-physics.org"
BASE = f"{SITE}/analgesic"
SHORT = "Analgesic Map"
DOI = "10.5281/zenodo.20733420"          # Zenodo concept DOI (resolves to the latest version)
DOI_URL = f"https://doi.org/{DOI}"
TODAY = datetime.date.today().isoformat()
VERSION = "2.0"

entries = TMAP["entries"]
by_gene = {e["gene"]: e for e in entries}

# ---------- formatters --------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=False) if s is not None else ""

def att(s):
    return html.escape(str(s), quote=True) if s is not None else ""

def chan(s):
    if not s:
        return ""
    s = esc(s)
    for p in ("Na", "Ca", "K"):
        s = s.replace(f"{p}_V", f"{p}<sub>V</sub>").replace(f"{p}_v", f"{p}<sub>V</sub>")
    return s

def chan_plain(s):
    return (s or "").replace("_V", "V").replace("_v", "V")

def ions(s):
    if s is None:
        return ""
    s = esc(s)
    for a, b in {"Ca2+": "Ca²⁺", "Na+": "Na⁺", "K+": "K⁺", "H+": "H⁺"}.items():
        s = s.replace(a, b)
    return s

def gbadge(token):
    t = (token or "").strip()
    cls = {"[V]": "g-v", "[F]": "g-f", "[O]": "g-o", "[H]": "g-h"}.get(t[:3], "g-o")
    return f'<b class="g {cls}">{esc(t[:3])}</b> {esc(t[3:].strip())}'

# ---------- page registry (ordered for prev/next) -----------------------------
LV = {"L1": [], "L1-adjacent": [], "L2": [], "L3": [], "master": [], "context": []}
for e in entries:
    LV.setdefault(e["lever"], []).append(e)

LEVER_PAGE = {
    "L1": ("lever-1-reduce-inward-current", "§L1",
           "Lever 1 — reduce the inward current",
           "Reduce the inward (depolarising) current to raise the firing threshold"),
    "L2": ("lever-2-increase-outward-current", "§L2",
           "Lever 2 — increase the outward K⁺ current",
           "Increase the outward K⁺ (M-current) brake to restore the OFF basin"),
    "L3": ("lever-3-remove-sensitising-drive", "§L3",
           "Lever 3 — remove the sensitising drive",
           "Remove the upstream sensitising drive (growth-factor and CGRP signalling)"),
    "master": ("master-switch-nociceptor-identity", "§M",
               "Master switch — nociceptor identity",
               "PRDM12, the developmental identity switch of the nociceptor lineage"),
    "context": ("context-comparators-routed-away", "§C",
                "Context comparators — routed away from reward",
                "Opioid and cannabinoid receptors, listed only as comparators"),
}
LEVER_LEAD = {
    "L1": "Lever 1 lowers the inward depolarising current (Na⁺, Ca²⁺, or proton/ATP-gated) so the pain fibre needs a stronger stimulus to fire. The promoter reads place each gene on the firing-threshold scale; the direction of intervention is anchored to cited agents such as the FDA-approved Na_V1.8 blocker. Reads are reproducible [V]; clinical magnitudes are open [O].",
    "L2": "Lever 2 increases the outward K⁺ (M-current) brake, hyperpolarising the neuron and restoring its OFF basin. The K_V7 family is the template (a clinically realised opener arm). The promoter reads place each gene on the threshold scale; direction is cited Layer-2 biology, reads are [V], clinical magnitudes are [O].",
    "L3": "Lever 3 removes the upstream sensitising drive — nerve-growth-factor (NGF→TrkA) and CGRP signalling that turn up the gain of the pain pathway. For every L3 target, γ only places the gene in the map; the ligand→receptor→sensitisation mechanism is cited biology, never derived by the read, and is enforced as [O] by a fail-closed L3-honesty gate.",
    "master": "PRDM12 is the developmental identity switch that specifies the nociceptor lineage; loss-of-function abolishes pain perception (congenital insensitivity). It is listed because the emergence chain reached the nociceptor through it — it is not an acute small-molecule analgesic target. The read is reproducible [V]; the developmental role is cited biology [O] for therapeutics.",
    "context": "Opioid (µ/κ/δ) and cannabinoid CB2 receptors are listed only as comparators, to be routed deliberately away from the central reward circuitry that drives opioid addiction and respiratory risk. They are flagged non-actionable in the prioritisation. Reads are reproducible [V]; their liabilities are cited biology, and all clinical magnitudes are [O].",
}

# section (non-target) pages
SECTIONS = [
    ("how-to-read-this-map", "§0", "How to read this map",
     "How to read the map: one DNA read per gene, three levers, every clinical magnitude open"),
    ("prioritisation", "§P", "Burden-weighted target prioritisation",
     "Targets ranked by burden, unmet need, and druggability — never by their map place"),
    ("precision-local-anaesthesia", "§PB", "Precision local anaesthesia",
     "A pain-selective differential block: a nociceptor-selective entry port × a charged threshold raiser"),
    ("proposals", "§Pr", "Proposals (P1–P6)",
     "Six directional proposals that follow from the map — hypotheses to test, not results"),
    ("falsification", "§Fx", "Falsification",
     "The observation that would refute each proposal; a map that cannot be wrong is not science"),
    ("grading-and-honesty", "§G", "Grading and honesty",
     "Three grades [V]/[F]/[O], a fail-closed claim scanner, an L3-honesty gate, and an open ledger"),
    ("for-pharma-and-researchers", "§RX", "For pharmaceutical companies and researchers",
     "Free reuse under CC BY 4.0 (including commercial) to broaden the search for non-opioid analgesics"),
    ("for-patients-and-public", "§Pub", "For patients and the public",
     "Plain language: a research map, shared free; not a medicine and not medical advice"),
]

def target_slug(g):
    return f"target-{g.lower()}"

# Build ordered page list: front, then lever+its targets, then remaining sections.
ORDER = []  # list of dicts: {slug, code, title_subj, kind, gene?}
ORDER.append({"slug": "how-to-read-this-map", "code": "§0",
              "title": "How to read this map", "kind": "section", "key": "how-to-read-this-map"})
for lev in ["L1", "L2", "L3", "master", "context"]:
    slug, code, title, _desc = LEVER_PAGE[lev]
    ORDER.append({"slug": slug, "code": code, "title": title, "kind": "lever", "lever": lev})
    grp = LV.get(lev, [])
    if lev == "L1":
        grp = grp + LV.get("L1-adjacent", [])  # fold adjacent into L1 stream
    for e in grp:
        ORDER.append({"slug": target_slug(e["gene"]), "code": e["gene"],
                      "title": e["gene"], "kind": "target", "gene": e["gene"]})
for slug, code, title, _desc in SECTIONS:
    if slug == "how-to-read-this-map":
        continue
    ORDER.append({"slug": slug, "code": code, "title": title, "kind": "section", "key": slug})

# index by position for prev/next
for i, p in enumerate(ORDER):
    p["prev"] = ORDER[i - 1] if i > 0 else None
    p["nxt"] = ORDER[i + 1] if i < len(ORDER) - 1 else None

# ---------- per-page JSON-LD ---------------------------------------------------
def ld_scholarly(slug, headline, position, desc, gene=None):
    knows = ["non-opioid analgesia", "nociceptor firing threshold", "promoter switch-threshold read",
             "jamming-lattice DNA Layer-1 (gamma)", "three-lever intervention frame"]
    if gene:
        e = by_gene[gene]
        cp = chan_plain(e.get("channel") or e.get("protein") or "")
        knows = [f"{gene} ({cp})" if cp else gene, "nociceptor firing threshold",
                 "promoter switch-threshold read", "non-opioid analgesia"]
    o = {"@context": "https://schema.org", "@type": "ScholarlyArticle",
         "headline": headline,
         "isPartOf": {"@type": "CreativeWork",
                      "name": "A DNA-Grounded Map of 27 Non-Opioid Analgesic Targets",
                      "url": BASE + "/"},
         "position": str(position),
         "description": desc,
         "author": {"@type": "Person", "name": "Young Jae Lee", "sameAs": ORCID},
         "creativeWorkStatus": "Proposal / preprint (Zenodo record)", "sameAs": DOI_URL, "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI},
         "isBasedOn": REPRO_URL,
         "isAccessibleForFree": True,
         "license": "https://creativecommons.org/licenses/by/4.0/",
         "datePublished": TODAY, "dateModified": TODAY,
         "knowsAbout": knows}
    return '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False) + "\n</script>"

def ld_breadcrumb(code, title):
    o = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Non-Opioid Analgesic Map", "item": BASE + "/"},
        {"@type": "ListItem", "position": 3, "name": f"{code} {title}"}]}
    return '<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False) + "\n</script>"

# ---------- §6 page shell -----------------------------------------------------
def page_shell(slug, code, title_subj, full_h1, description, answer, abstract,
               grade=None, vp_cards="", body="", prev=None, nxt=None, gene=None,
               position=0, title_code=None):
    desc = att(re.sub(r"<[^>]+>", "", description))[:158]
    code_part = code if title_code is None else title_code
    t = f"{title_subj} — {SHORT} {code_part} | Jamming Physics" if code_part else f"{title_subj} — {SHORT} | Jamming Physics"
    if len(t) > 90:
        t = f"{title_subj} — {SHORT} | Jamming Physics"
    canonical = f"{BASE}/{slug}/"
    grade_span = ""
    if grade:
        cls = {"[V]": "g-v", "[F]": "g-f", "[O]": "g-o", "[H]": "g-h"}.get(grade[:3], "g-o")
        grade_span = f'<span class="grade {cls}">{esc(grade)}</span>'
    crumb_prev = ""
    pn_prev = f'<a rel="prev" href="{BASE}/{prev["slug"]}/">← {esc(prev["code"])}</a>' if prev else '<span></span>'
    pn_next = f'<a rel="next" href="{BASE}/{nxt["slug"]}/">{esc(nxt["code"])} →</a>' if nxt else '<span></span>'
    head_ld = ld_scholarly(slug, full_h1, position, re.sub(r"<[^>]+>", "", description), gene) \
              + "\n" + ld_breadcrumb(code, title_subj)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t)}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/assets/css/site.css">
{head_ld}
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › <a href="/analgesic/">{SHORT}</a> › {esc(code)}</nav></header>
<main>
<h1>{full_h1}</h1>
<p class="answer">{answer}</p>
<p class="abstract">{abstract}</p>
<aside class="claim-strip page">{grade_span}<span class="gate">LOCK → Derive → Gate</span><a href="{REPRO_URL}" rel="noopener">reproduce (GitHub)</a><a class="ver" href="{DOI_URL}" rel="noopener">DOI {DOI}</a></aside>
{vp_cards}
{body}
<nav class="pn">{pn_prev} <a href="/analgesic/">map contents</a> {pn_next}</nav>
</main>
<footer><a href="{ORCID}" rel="noopener">ORCID 0009-0002-7535-8245</a> · Young Jae Lee · CC BY 4.0 · <a href="{DOI_URL}" rel="noopener">DOI {DOI}</a> · part of the <a href="{SITE}/" rel="noopener">Jamming Physics</a> programme · reproduce: <code>repro/run_all.py</code></footer>
</body>
</html>"""

# ---------- body builders -----------------------------------------------------
def body_how_to_read():
    return """<h2>One read per gene</h2>
<p>Each gene gets a single number from the DNA — γ, a read of its promoter's switch-threshold <em>structure</em> — placed on the R19 firing-threshold scale, |h<sub>sp</sub>| = (2/3√3) γ<sup>1.5</sup>. That read tells you where the gene sits in the map and which lever it belongs to.</p>
<p class="fw"><b>Firewall (non-negotiable).</b> γ is <b>not</b> a channel's activation voltage, a candidate's potency, a dosing quantity, an in-vivo selectivity, or a clinical effect. Those magnitudes are <b class="g g-o">[O]</b> open and come only from laboratory and clinical work. The engine reads structure; it never asserts a clinical number.</p>
<h2>The three levers</h2>
<p>Pain fibres fire when inward current overwhelms the outward brake. The map intervenes along three levers, each of which raises the effective firing threshold:</p>
<table>
<thead><tr><th>lever</th><th>direction</th><th>where</th></tr></thead>
<tbody>
<tr><td><a href="/analgesic/lever-1-reduce-inward-current/"><b>L1</b></a></td><td>reduce the inward (depolarising) current</td><td>Na⁺, Ca²⁺, proton/ATP-gated channels</td></tr>
<tr><td><a href="/analgesic/lever-2-increase-outward-current/"><b>L2</b></a></td><td>increase the outward K⁺ current</td><td>K_V7 / M-current</td></tr>
<tr><td><a href="/analgesic/lever-3-remove-sensitising-drive/"><b>L3</b></a></td><td>remove the upstream sensitising drive</td><td>NGF–TrkA, CGRP signalling</td></tr>
</tbody>
</table>
<p>Two further groups are listed for completeness: the <a href="/analgesic/master-switch-nociceptor-identity/">master identity switch</a> (PRDM12) and <a href="/analgesic/context-comparators-routed-away/">context comparators</a> (opioid / cannabinoid receptors), routed deliberately away from the central reward axis.</p>
<h2>How to read a grade</h2>
<p>Every claim carries one of three grades: <b class="g g-v">[V]</b> verified / reproducible, <b class="g g-f">[F]</b> forced by the reads (structural, not chosen), and <b class="g g-o">[O]</b> open (needs external data; asserted nowhere). Every clinical magnitude is [O]. The full legend and the open ledger are on the <a href="/analgesic/grading-and-honesty/">grading and honesty</a> page.</p>"""

def body_lever(lev):
    slug, code, title, _ = LEVER_PAGE[lev]
    grp = LV.get(lev, [])
    if lev == "L1":
        grp = grp + LV.get("L1-adjacent", [])
    rows = ""
    for e in grp:
        cp = chan(e.get("channel")) if e.get("channel") else esc(e.get("protein") or "")
        adj = ' <span class="note">(adjacent)</span>' if e["lever"] == "L1-adjacent" else ""
        rows += (f'<tr><td><a href="/analgesic/{target_slug(e["gene"])}/"><b>{esc(e["gene"])}</b></a>{adj}</td>'
                 f'<td>{cp}</td><td>γ {e["gamma"]}</td><td>|h<sub>sp</sub>| {e["spinodal_h_sp"]}</td>'
                 f'<td class="note">{esc(e["selectivity_tier"])}</td></tr>')
    return f"""<h2>What this lever does</h2>
<p>{esc(LEVER_LEAD[lev])}</p>
<h2>Targets in this lever</h2>
<p>Each row links to that target's own self-contained page (its read, grades, citation, and firewall).</p>
<table>
<thead><tr><th>gene</th><th>channel / protein</th><th>γ</th><th>|h<sub>sp</sub>|</th><th>selectivity (cited)</th></tr></thead>
<tbody>{rows}</tbody>
</table>"""

def body_target(gene):
    e = by_gene[gene]
    cp = chan(e.get("channel")) if e.get("channel") else esc(e.get("protein") or "")
    push = ions(e["push_direction"])
    rows = [("read", e.get("grade_read")), ("order", e.get("grade_order")),
            ("lever", e.get("grade_lever")), ("mechanism", e.get("grade_mechanism")),
            ("clinical magnitude", e.get("grade_clinical_map"))]
    grades = "".join(f'<li><span class="gk">{esc(k)}</span> {gbadge(v)}</li>' for k, v in rows if v)
    burden = e.get("burden_tier")
    burden_html = f'<p class="note"><span class="gk">burden</span> {esc(burden)}</p>' if burden else ""
    return f"""<h2>The read</h2>
<p>{esc(gene)}{(' — ' + cp) if cp else ''} sits in the threshold map at <b>γ = {e["gamma"]}</b>, <b>|h<sub>sp</sub>| = {e["spinodal_h_sp"]}</b> (barrier {e["barrier"]}). It belongs to lever <b>{esc(e["lever"])}</b>; the intervention direction is to <b>{push}</b>.</p>
<p class="note"><span class="gk">selectivity (cited)</span> {esc(e["selectivity_tier"])}</p>
{burden_html}
<h2>Grades</h2>
<ul class="grades">{grades}</ul>
<p class="fw"><b>Firewall.</b> γ here is a read of promoter switch-threshold <em>structure</em> only — never this channel's activation voltage, a candidate's potency, a dosing quantity, an in-vivo selectivity, or a clinical effect. Those magnitudes are <b class="g g-o">[O]</b> open.</p>
<h2>Source</h2>
<p class="note">{esc(e["src"])} · <a href="{REPRO_URL}" rel="noopener">reproduce the read (engine)</a></p>
<p class="note">See also: <a href="/analgesic/{LEVER_PAGE[e['lever'] if e['lever'] in LEVER_PAGE else 'L1'][0]}/">its lever</a> · <a href="/analgesic/prioritisation/">prioritisation</a> · <a href="/analgesic/grading-and-honesty/">grading</a>.</p>"""

def body_prioritisation():
    w = PRIO["weights_declared"]
    trows = ""
    for r in PRIO["ranking_actionable"][:12]:
        mp = r.get("map_place", {})
        trows += (f'<tr><td>{r["rank"]}</td><td><a href="/analgesic/{target_slug(r["gene"])}/">{esc(r["gene"])}</a></td>'
                  f'<td>{chan(r.get("channel_or_protein"))}</td><td>{esc(r["lever"])}</td>'
                  f'<td>{r["B_burden"]}</td><td>{r["U_unmet"]}</td><td>{r["D_druggability"]}</td>'
                  f'<td><b>{r["priority_score"]}</b></td><td class="note">γ|h<sub>sp</sub> {mp.get("gamma_h_sp","")}</td></tr>')
    comps = ", ".join(f'{esc(c["gene"])} ({chan(c.get("channel_or_protein"))})' for c in PRIO["comparators_context"])
    return f"""<h2>Ranked by burden, not by map place</h2>
<p>The priority score is a <b>declared editorial weighting</b> — burden {w["B"]}, unmet need {w["U"]}, druggability {w["D"]} — over cited 1–5 tiers. The γ-|h<sub>sp</sub>| map place is carried <em>alongside</em> each row but is <b>never folded into</b> the score (firewall: promoter stiffness ≠ clinical magnitude).</p>
<p class="note"><span class="gk">grade</span> <b class="g g-f">[F]</b> from cited B/U/D tiers + declared weights (a Layer-2 ranking, not a <b class="g g-v">[V]</b> engine output). {esc(PRIO["n_actionable"])} actionable targets; {esc(PRIO["n_comparators"])} comparators held out.</p>
<table>
<thead><tr><th>#</th><th>target</th><th>channel / protein</th><th>lever</th><th>B</th><th>U</th><th>D</th><th>score</th><th>map place</th></tr></thead>
<tbody>{trows}</tbody>
</table>
<p class="note"><span class="gk">comparators (routed away from reward, non-actionable)</span> {comps}.</p>"""

def body_precision():
    inner = VERBATIM["precision"]
    return f'<section data-claim="precision">\n{inner}\n</section>'

def body_proposals():
    inner = VERBATIM["proposal"]
    return ('<p>Six directional proposals follow from the map. Each is a hypothesis to be tested, not a result; '
            'each names its falsifier on the <a href="/analgesic/falsification/">falsification</a> page.</p>'
            f'<section data-claim="proposal">\n{inner}\n</section>')

def body_falsification():
    items = [
        ("P1/P2 — gate &amp; direction", "If raising the nociceptor firing threshold at these peripheral gates does not reduce nociceptive signalling in a controlled assay, the direction is wrong.", "g-f"),
        ("P3 — Na_V triad axis", "If the sodium-channel triad does not behave as the most nociceptor-selective inward-current axis relative to the other levers, the ranking premise fails.", "g-f"),
        ("P4 — state-dependent shape", "If a closed/inactivated-state stabiliser cannot lift the firing threshold while sparing ordinary low-frequency conduction, the favoured mechanism shape is falsified.", "g-f"),
        ("P5 — opioid-alternative claim", "If a peripheral, nociceptor-restricted intervention nonetheless engages central reward circuitry, the opioid-alternative framing is falsified.", "g-f"),
        ("P6 — differential block", "If opening a nociceptor-selective entry port (TRPV1/TRPA1) does not confine a charged Na_V blocker to nociceptive fibres — no differential block versus motor/touch fibres — the precision claim fails.", "g-f"),
        ("Framework", "If the promoter γ read does not track expression-switch behaviour at these loci, the Layer-1 grounding of the whole map is falsified. This is the framework-level open question, stated not assumed.", "g-o"),
    ]
    lis = "".join(f'<li><b>{name}.</b> {esc(txt)} <b class="g {g}">[{ "F" if g=="g-f" else "O"}]</b></li>' for name, txt, g in items)
    return f"""<h2>What would break each claim</h2>
<p>Each proposal names the observation that would refute it. A map that cannot be wrong is not science; these are the tests that can break it.</p>
<ol>{lis}</ol>"""

def body_grading():
    return f"""<h2>Three grades</h2>
<ul>
<li><b class="g g-v">[V]</b> <b>verified / reproducible</b> — bit-reproducible from public promoter sequence (the 27 γ reads; corr(γ,GC) = 0.99898 over the full set, drift 0, offline).</li>
<li><b class="g g-f">[F]</b> <b>forced by the reads</b> — structural and not chosen (the ordering by |h<sub>sp</sub>|; the lever placement and direction, anchored to cited agents).</li>
<li><b class="g g-o">[O]</b> <b>open</b> — needs external laboratory / clinical data; asserted nowhere. <b>Every clinical magnitude is [O].</b></li>
</ul>
<h2>The discipline is mechanical</h2>
<p>An <b>L3-honesty gate</b> verifies that for every upstream-sensitiser target (NGF, NTRK1, CALCA, CALCB, CALCRL, RAMP1) the receptor/network mechanism is graded <b class="g g-o">[O]</b> cited-biology-never-derived. A <b>forbidden-claim scanner</b> fails the build closed if any dosing, synthesis, efficacy, or safety claim appears in the asserted text. An <b>irreproducibility ledger</b> lists all nine open classes with their reasons.</p>
<p>Reproduce every gate: <code>repro/run_all.py</code> (11/11 checks, drift 0). The full open ledger is <code>IRREPRODUCIBILITY_LEDGER.md</code> in the package.</p>"""

def body_pharma():
    return f"""<h2>Free to reuse</h2>
<p>This map is free to reuse — including commercially — under CC BY 4.0, to lower the cost and broaden the search for non-opioid analgesics.</p>
<ul>
<li><b>License.</b> CC BY 4.0. Reuse, adapt, and build on the reads and the lever map with attribution; commercial use is permitted.</li>
<li><b>Reproduce.</b> Every read and gate regenerates deterministically (offline, drift 0) from public promoter sequence: clone <a href="{REPO}" rel="noopener">{REPO}</a> and run <code>repro/run_all.py</code>.</li>
<li><b>What you get.</b> 27 graded target reads, a three-lever direction of intervention, a burden-weighted prioritisation, an L3-honesty gate, and a precision local-anaesthesia map — each target a separate page.</li>
<li><b>What you must supply.</b> All clinical magnitudes — potency, selectivity in vivo, efficacy, safety, formulation, dose — are <b class="g g-o">[O]</b> open here and remain your own scientific, ethical, and regulatory responsibility.</li>
<li><b>Contact / cite.</b> Young Jae Lee, <a href="{ORCID}" rel="noopener">ORCID 0009-0002-7535-8245</a>. A Zenodo DOI is pending and will be inserted on publication.</li>
</ul>"""

def body_patients():
    inner = VERBATIM["disclaimer"]
    return ('<p>In plain language: this is a research map that points scientists toward non-opioid ways to quiet pain '
            'nerves. It is shared free so that work can move faster and cost less. It is not a medicine and not advice '
            'for any person.</p>'
            f'<section data-claim="disclaimer"><p>{inner}</p></section>')

# ---------- answer + abstract per page ----------------------------------------
def target_answer(gene):
    e = by_gene[gene]
    cp = chan_plain(e.get("channel") or e.get("protein") or "")
    cp = f" ({cp})" if cp else ""
    push = re.sub(r"\s*\(.*?\)", "", e["push_direction"]).strip()
    push = push.replace("Ca2+", "Ca²⁺").replace("Na+", "Na⁺").replace("K+", "K⁺")
    return (f'{esc(gene)}{esc(cp)} is a lever-{esc(e["lever"])} non-opioid analgesic target. Its promoter reads '
            f'γ = {e["gamma"]}, placing it on the firing-threshold scale at |h<sub>sp</sub>| = {e["spinodal_h_sp"]}; '
            f'the intervention direction is to {esc(push)}. The read is reproducible [V]; the clinical magnitude is open [O].')

def target_abstract(gene):
    e = by_gene[gene]
    return (f'{esc(gene)} is read from its human promoter by the same deterministic engine used across the map '
            f'(nearest-neighbour stacking energy → γ = {e["gamma"]}; R19 scale → |h<sub>sp</sub>| = {e["spinodal_h_sp"]}). '
            f'The read places the gene in lever {esc(e["lever"])}; its selectivity is cited Layer-2 biology, '
            f'and every clinical magnitude (potency, dose, efficacy, safety) is graded [O].')

# ---------- write all ---------------------------------------------------------
def extract_verbatim():
    """Pull the scanner-passing claim sections from the single-file backup."""
    src = "/tmp/docs_singlefile_bak/index.html"
    htext = open(src, encoding="utf-8").read()
    out = {}
    for tag in ["proposal", "precision", "disclaimer"]:
        m = re.search(r"<section[^>]*data-claim=['\"]" + tag + r"['\"][^>]*>(.*?)</section>", htext, re.S | re.I)
        out[tag] = m.group(1).strip() if m else ""
    return out

VERBATIM = extract_verbatim()

CSS_BASE = """/* Jamming Physics — site.css (VP-SPEC v1.8 canonical, analgesic edition) */
:root{
  --ink:#1a1a1a; --muted:#5a5a5a; --line:#e2e2e2; --bg:#fff; --accent:#1f5c8b;
  --g-forced:#0a7d33; --g-cal:#b06a00; --g-open:#8a8a8a;
  --gv:#0a7d33; --gf:#1452c4; --go:#9a6300; --gh:#6a3fb0;
  --maxw:760px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
main{max-width:var(--maxw);margin:0 auto;padding:0 20px 64px}
header{max-width:var(--maxw);margin:0 auto;padding:18px 20px 0}
footer{max-width:var(--maxw);margin:48px auto 0;padding:20px;border-top:1px solid var(--line);
  color:var(--muted);font-size:14px}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
h1{font-size:1.72rem;line-height:1.25;margin:.4em 0 .2em;letter-spacing:-.01em}
h2{font-size:1.28rem;margin:1.8em 0 .5em;letter-spacing:-.01em}
h3{font-size:1.06rem;margin:1.4em 0 .4em}
p{margin:.7em 0}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;
  background:#f3f5f7;border:1px solid var(--line);border-radius:4px;padding:1px 5px}
.crumb{font-size:13.5px;color:var(--muted)}
.crumb a{color:var(--muted)}
.answer{font-size:1.12rem;line-height:1.55;color:#23262b}
.abstract{font-size:1.04rem;line-height:1.6;background:#f7f9fb;border-left:3px solid var(--accent);
  padding:14px 18px;margin:1em 0;border-radius:0 4px 4px 0}
.claim-strip{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;
  margin:1em 0 1.6em;padding:10px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  font-size:13.5px}
.claim-strip .grade{font-weight:600;padding:2px 9px;border-radius:999px;color:#fff;text-transform:lowercase}
.claim-strip .gate{color:var(--muted);font-variant:all-small-caps;letter-spacing:.04em}
.claim-strip .ver{color:var(--muted)}
.grade.g-v{background:var(--gv)} .grade.g-f{background:var(--gf)}
.grade.g-o{background:var(--go)} .grade.g-h{background:var(--gh)}
.g{font-weight:700;border-radius:4px;padding:0 5px;color:#fff;font-size:.86em;white-space:nowrap}
.g.g-v{background:var(--gv)} .g.g-f{background:var(--gf)} .g.g-o{background:var(--go)} .g.g-h{background:var(--gh)}
.gk{display:inline-block;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:#7a8089;
  border:1px solid var(--line);border-radius:4px;padding:1px 6px;margin-right:6px}
table{border-collapse:collapse;width:100%;margin:1.1em 0;font-size:14.5px}
th,td{border:1px solid var(--line);padding:7px 10px;text-align:left;vertical-align:top}
th{background:#f3f5f7;font-weight:600}
.fw{background:#fff;border:1px dashed var(--line);border-radius:6px;padding:10px 14px;font-size:14.5px;color:#333}
ul.grades{list-style:none;padding:0;margin:.6em 0;font-size:14.5px}
ul.grades li{margin:.3em 0}
.pn{display:flex;justify-content:space-between;gap:12px;margin:2.4em 0 0;padding-top:14px;
  border-top:1px solid var(--line);font-size:14.5px}
.pn a{white-space:nowrap}
ol.toc{list-style:none;padding:0;margin:1.2em 0}
ol.toc li{border-bottom:1px solid var(--line);padding:10px 2px}
ol.toc .ol{display:block;color:var(--muted);font-size:14px;margin-top:2px}
ol.toc .lv{background:#f7f9fb;font-weight:600}
.lede{font-size:1.12rem;color:#333}
.note{font-size:14px;color:var(--muted)}
.xlinks{list-style:none;padding:0}
.xlinks li{padding:8px 2px;border-bottom:1px solid var(--line)}
.xlinks .kf{font-family:ui-monospace,Menlo,monospace;font-size:.92em;color:#333;margin-right:6px}
sub{font-size:.72em}
ul,ol{padding-left:1.3em}
li{margin:.25em 0}
@media(max-width:480px){body{font-size:16px}h1{font-size:1.5rem}table{display:block;overflow-x:auto}}
"""

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)

def build_all():
    # fresh docs/
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    write(f"{DOCS}/assets/css/site.css", CSS_BASE)

    # ----- each ordered page -----
    pos = 1
    for p in ORDER:
        slug, code, kind = p["slug"], p["code"], p["kind"]
        if kind == "section":
            key = p["key"]
            title = next(t for s, c, t, d in [("how-to-read-this-map", "§0", "How to read this map", "")] + SECTIONS if s == key)
            desc = next(d for s, c, t, d in [("how-to-read-this-map", "§0", "How to read this map",
                       "How to read the map: one DNA read per gene, three levers, every clinical magnitude open")] + SECTIONS if s == key)
            builders = {"how-to-read-this-map": body_how_to_read, "prioritisation": body_prioritisation,
                        "precision-local-anaesthesia": body_precision, "proposals": body_proposals,
                        "falsification": body_falsification, "grading-and-honesty": body_grading,
                        "for-pharma-and-researchers": body_pharma, "for-patients-and-public": body_patients}
            body = builders[key]()
            answers = {
                "how-to-read-this-map": "This map reads one number per gene from the DNA — γ, the promoter's switch-threshold structure — and places it on a firing-threshold scale, sorting 27 non-opioid targets into three levers: reduce inward current, increase outward current, remove the sensitising drive. Every read is graded; every clinical magnitude is open. The firewall is non-negotiable.",
                "prioritisation": "Targets are ranked by burden, unmet need, and druggability under declared weights (0.40 / 0.35 / 0.25), not by their map place. SCN10A (Na_V1.8) leads, then NGF, SCN9A, CALCA. The γ-|h_sp| map place is carried alongside but never folded into the score. The ranking is forced from cited tiers [F]; clinical magnitudes stay open [O].",
                "precision-local-anaesthesia": "Precision local anaesthesia pairs a nociceptor-selective entry port (TRPV1 or TRPA1) with a permanently charged firing-threshold raiser that enters only through that open port, so the block is differential — pain fibres silenced, motor and touch fibres largely spared. The mechanism shape is forced [F], anchored to Binshtok 2007; every differential-block magnitude is open [O].",
                "proposals": "Six directional proposals follow from the map: intervene at the peripheral nociceptor gate (P1), push it to raise the firing threshold (P2), rank effectors by selectivity and map place pursuing the Na_V triad (P3), favour a state-dependent shape (P4), pursue a structurally non-reward opioid alternative (P5), and pursue pain-selective local anaesthesia (P6). Each is a hypothesis, not a result.",
                "falsification": "Each proposal names the observation that would refute it: no threshold-driven reduction in nociceptive signalling, no Na_V-triad selectivity advantage, no state-dependent sparing of conduction, central reward engagement, or no differential block. The framework-level open question is whether the promoter γ read tracks expression-switch behaviour — stated, not assumed.",
                "grading-and-honesty": "Every claim carries one of three grades: [V] verified and reproducible, [F] forced by the reads, [O] open. Every clinical magnitude is [O]. The discipline is mechanical: an L3-honesty gate, a fail-closed forbidden-claim scanner, and an irreproducibility ledger of nine open classes. Reproduce all gates with repro/run_all.py — 11/11, drift 0.",
                "for-pharma-and-researchers": "This map is free to reuse under CC BY 4.0, including commercially, to lower the cost and broaden the search for non-opioid analgesics. Every read and gate regenerates deterministically offline from public promoter sequence. All clinical magnitudes are open and remain the reusing party's own scientific, ethical, and regulatory responsibility. A Zenodo DOI is pending.",
                "for-patients-and-public": "In plain language, this is a research map that points scientists toward non-opioid ways to quiet pain nerves, shared free so the work can move faster and cost less. It is not a medicine and not medical advice; nothing here diagnoses, treats, cures, or prevents any condition, and no person should act on it. It carries no medical responsibility.",
            }
            abstracts = {
                "how-to-read-this-map": "A single jamming-lattice read (γ, a nearest-neighbour stacking-energy read of the promoter) is mapped onto the R19 firing-threshold scale |h<sub>sp</sub>| = (2/3√3) γ<sup>1.5</sup> for 27 nociception genes. The read fixes each gene's lever; it is never a channel voltage, potency, dose, or clinical effect, all of which are [O].",
                "prioritisation": "The priority score is a declared editorial weighting (burden 0.40, unmet need 0.35, druggability 0.25) over cited 1–5 tiers, ranking 22 actionable targets with 5 comparators held out. It ranks targets/reads, never drugs or doses, and the γ-|h<sub>sp</sub>| map place is carried alongside but never folded into the score.",
                "precision-local-anaesthesia": "Seven entry-port × charged-blocker pairings are tabulated (TRPV1/TRPA1 × Na_V1.8/Na_V1.7 and alternatives). The mechanism shape (selective entry → selective block) is [F], anchored to Binshtok, Bean &amp; Woolf (Nature 2007); QX-314 and chloroprocaine are named only as experimental anchors. The differential-block ratio, duration, and every clinical magnitude are [O].",
                "proposals": "Six proposals (P1–P6) state directional hypotheses that follow from the map — where to intervene, which way to push, which axis to pursue, which mechanism shape to favour, why it is a structural opioid alternative, and how to make a differential block. Each is a hypothesis to test; whether any molecule reaches the goal is an open empirical question.",
                "falsification": "Each proposal is paired with the observation that would refute it, and the framework names its own falsifier — that the promoter γ read tracks expression-switch behaviour at these loci. Forced structural claims [F] are separated from the framework-level open question [O], which is stated rather than assumed.",
                "grading-and-honesty": "Grades are [V] verified/reproducible, [F] forced by the reads, [O] open. The discipline is enforced mechanically by an L3-honesty gate (fail-closed), a forbidden-claim scanner (fail-closed), and an irreproducibility ledger that aggregates nine open classes with reasons. The 27 reads reproduce bit-for-bit (corr(γ,GC) = 0.99898, drift 0, offline).",
                "for-pharma-and-researchers": "Reuse is governed by CC BY 4.0 (commercial use permitted). The reproducibility path is closed inside the package: clone the repository and run repro/run_all.py for 11/11 gate checks at drift 0. The map supplies graded target reads and a direction of intervention; potency, selectivity in vivo, efficacy, safety, formulation, and dose are [O] and supplied by the reuser.",
                "for-patients-and-public": "This document is a free, public-benefit scientific hypothesis, not medical advice and not a treatment. It designs no molecule and gives no dose; it asserts no efficacy, potency, or safety result. Those can come only from proper laboratory and clinical validation, which this work does not perform. The author assumes no medical or clinical responsibility.",
            }
            grade = {"prioritisation": "[F] forced", "precision-local-anaesthesia": "[F] forced"}.get(key)
            html_doc = page_shell(slug, code, title, esc(title), desc, answers[key], abstracts[key],
                                  grade=grade, body=body, prev=p["prev"], nxt=p["nxt"], position=pos)
        elif kind == "lever":
            lev = p["lever"]
            _slug, _code, title, desc = LEVER_PAGE[lev]
            body = body_lever(lev)
            grade = "[F] forced"
            ans = (f"{esc(title)}. " + esc(LEVER_LEAD[lev]))
            ans = re.sub(r"\s+", " ", ans)
            ans_words = ans.split()
            answer = " ".join(ans_words[:58])
            abstract = (f"This lever groups the targets whose promoter reads place them in the "
                        f"{esc(LEVER_PAGE[lev][2].lower())}. Each target keeps its own page with its read, grades, "
                        f"citation, and firewall; the lever direction is cited Layer-2 biology, the reads are [V], "
                        f"and all clinical magnitudes are [O].")
            html_doc = page_shell(slug, code, title, esc(title), desc, answer, abstract,
                                  grade=grade, body=body, prev=p["prev"], nxt=p["nxt"], position=pos)
        else:  # target
            gene = p["gene"]
            e = by_gene[gene]
            cp = chan_plain(e.get("channel") or e.get("protein") or "")
            subj = f"{gene} ({cp})" if cp else f"{gene}"
            full_h1 = f"{esc(gene)}" + (f" — {chan(e.get('channel')) if e.get('channel') else esc(e.get('protein'))}" if cp else "")
            desc = (f"{gene}{(' (' + cp + ')') if cp else ''}: a lever-{e['lever']} non-opioid analgesic target read "
                    f"at γ={e['gamma']}, |h_sp|={e['spinodal_h_sp']}. Reproducible read [V]; clinical magnitude open [O].")
            body = body_target(gene)
            html_doc = page_shell(slug, code, subj, full_h1, desc, target_answer(gene), target_abstract(gene),
                                  grade="[F] forced", body=body, prev=p["prev"], nxt=p["nxt"], gene=gene,
                                  position=pos, title_code="")
        write(f"{DOCS}/analgesic/{slug}/index.html", html_doc)
        pos += 1

    # ----- hub -----
    write(f"{DOCS}/analgesic/index.html", build_hub())
    # ----- access layer -----
    write(f"{DOCS}/robots.txt", build_robots())
    write(f"{DOCS}/sitemap.xml", build_sitemap())
    write(f"{DOCS}/llms.txt", build_llms())
    write(f"{DOCS}/analgesic/_meta.json", json.dumps(build_meta(), ensure_ascii=False, indent=2))

def build_hub():
    # CreativeWorkSeries hasPart
    has = [{"@type": "CreativeWork", "@id": f"{BASE}/{p['slug']}/"} for p in ORDER]
    series = {"@context": "https://schema.org", "@type": "CreativeWorkSeries",
              "name": "A DNA-Grounded Map of 27 Non-Opioid Analgesic Targets",
              "url": BASE + "/",
              "author": {"@type": "Person", "name": "Young Jae Lee", "sameAs": ORCID},
              "creativeWorkStatus": "Proposal / preprint (Zenodo record)", "sameAs": DOI_URL, "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI},
              "license": "https://creativecommons.org/licenses/by/4.0/",
              "isAccessibleForFree": True, "isBasedOn": REPRO_URL, "hasPart": has}
    coll = {"@context": "https://schema.org", "@type": "CollectionPage",
            "name": "A DNA-Grounded Map of 27 Non-Opioid Analgesic Targets",
            "url": BASE + "/",
            "sameAs": DOI_URL, "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI}, "isPartOf": {"@type": "WebSite", "name": "Jamming Physics", "url": SITE + "/"},
            "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Non-Opioid Analgesic Map", "item": BASE + "/"}]}}
    # ToC
    toc = ['<ol class="toc">']
    toc.append('<li class="lv"><a href="/analgesic/how-to-read-this-map/">§0 · How to read this map</a> <span class="ol">One DNA read per gene, three levers, the firewall, and the grading legend.</span></li>')
    for lev in ["L1", "L2", "L3", "master", "context"]:
        slug, code, title, desc = LEVER_PAGE[lev]
        toc.append(f'<li class="lv"><a href="/analgesic/{slug}/">{esc(code)} · {esc(title)}</a> <span class="ol">{esc(desc)}.</span></li>')
        grp = LV.get(lev, [])
        if lev == "L1":
            grp = grp + LV.get("L1-adjacent", [])
        for e in grp:
            cp = chan_plain(e.get("channel") or e.get("protein") or "")
            adj = " (adjacent)" if e["lever"] == "L1-adjacent" else ""
            toc.append(f'<li><a href="/analgesic/{target_slug(e["gene"])}/">{esc(e["gene"])}{esc(adj)}{(" — " + chan(e.get("channel"))) if e.get("channel") else ((" — " + esc(e.get("protein"))) if e.get("protein") else "")}</a> <span class="ol">γ {e["gamma"]} · |h<sub>sp</sub>| {e["spinodal_h_sp"]} · read [V], clinical [O].</span></li>')
    for slug, code, title, desc in SECTIONS:
        if slug == "how-to-read-this-map":
            continue
        toc.append(f'<li class="lv"><a href="/analgesic/{slug}/">{esc(code)} · {esc(title)}</a> <span class="ol">{esc(desc)}.</span></li>')
    toc.append('</ol>')
    toc_html = "\n".join(toc)
    n_pages = len(ORDER) + 1
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Non-Opioid Analgesic Target Map — 27 DNA-grounded targets | Jamming Physics</title>
<meta name="description" content="A reproducible, DNA-grounded map of 27 non-opioid pain targets across three intervention levers — each its own page, each graded for honesty. Free, open, proposal-only (CC BY 4.0).">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{BASE}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{json.dumps(coll, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(series, ensure_ascii=False)}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › Non-Opioid Analgesic Map</nav></header>
<main>
<h1>A DNA-Grounded Map of 27 Non-Opioid Analgesic Targets</h1>
<p class="lede">From sequence alone: one read per gene (γ), three levers, every clinical magnitude open [O].</p>
<p class="abstract">A single jamming-lattice read — Layer-1 γ, a nearest-neighbour stacking-energy read of the promoter (SantaLucia 1998) — is taken for 27 nociception genes and mapped onto the R19 firing-threshold scale, |h<sub>sp</sub>| = (2/3√3) γ<sup>1.5</sup>. The reads are bit-reproducible (corr(γ,GC) = 0.99898 over the full set, drift 0, offline). γ reads promoter switch-threshold structure only; it is never equated with any channel voltage, potency, dose, in-vivo selectivity, or clinical effect — all of which are graded [O]. The map sorts the targets into three levers (reduce inward current, increase outward current, remove the sensitising drive), ranks them by burden, and adds a precision local-anaesthesia map — each target on its own page.</p>
<aside class="claim-strip page"><span class="gate">LOCK → Derive → Gate</span><a href="{REPRO_URL}" rel="noopener">reproduce (GitHub)</a><a class="ver" href="{DOI_URL}" rel="noopener">DOI {DOI}</a></aside>
<p class="note">{n_pages} pages · 27 target reads · 11/11 reproducibility gates, drift 0, offline · CC BY 4.0. Every page is self-contained and answer-first; every clinical magnitude is [O] (open). This is a free, public-benefit, proposal-only hypothesis.</p>
<h2>Map contents</h2>
{toc_html}
<h2>Cross-links</h2>
<ul class="xlinks">
<li><span class="kf">Na_V1.8 (SCN10A)</span> → <a href="/analgesic/target-scn10a/">primary peripheral L1 target</a> (FDA-validated axis)</li>
<li><span class="kf">NGF–TrkA</span> → <a href="/analgesic/target-ngf/">L3 sensitiser</a> · <a href="/analgesic/target-ntrk1/">NTRK1</a></li>
<li><span class="kf">CGRP receptor</span> → <a href="/analgesic/target-calcrl/">CALCRL</a> + <a href="/analgesic/target-ramp1/">RAMP1</a></li>
<li><span class="kf">precision block</span> → <a href="/analgesic/precision-local-anaesthesia/">entry port × charged threshold raiser</a></li>
</ul>
</main>
<footer><a href="{ORCID}" rel="noopener">ORCID 0009-0002-7535-8245</a> · Young Jae Lee · CC BY 4.0 · <a href="{DOI_URL}" rel="noopener">DOI {DOI}</a> · part of the <a href="{SITE}/" rel="noopener">Jamming Physics</a> programme · reproduce: <code>repro/run_all.py</code></footer>
</body>
</html>"""

def build_robots():
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    lines = ["# VP-SPEC v1.8 — machine access (C4 retrieval-readiness). 7 named agents + default: full allow.",
             f"# analgesic_threshold_logic v{VERSION}; generated {TODAY} (deterministic)", ""]
    for b in bots:
        lines += [f"User-agent: {b}", "Allow: /", ""]
    lines += ["User-agent: *", "Allow: /", "", f"Sitemap: {SITE}/sitemap.xml"]
    return "\n".join(lines) + "\n"

def build_sitemap():
    urls = [(BASE + "/", "1.0")]
    for p in ORDER:
        urls.append((f"{BASE}/{p['slug']}/", "0.8"))
    body = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{pr}</priority>\n  </url>"
        for u, pr in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n")

def build_llms():
    lines = ["# Jamming Physics — Non-Opioid Analgesic Target Map", "",
             "> Canonical, citable multi-page HTML edition of a DNA-grounded map of 27 non-opioid analgesic "
             "targets in pain-sensing neurons. From sequence alone, one deterministic read (γ, a nearest-neighbour "
             "stacking-energy read of the promoter) places each gene on the R19 firing-threshold scale and into one "
             "of three intervention levers. Every page is self-contained and answer-first; γ reads promoter "
             "switch-threshold STRUCTURE only, and every clinical magnitude is graded [O] (open). Free, "
             "proposal-only, CC BY 4.0.", "",
             f"Author: Young Jae Lee ({ORCID}). DOI: {DOI} ({DOI_URL}).",
             "Principle: LOCK → Derive → Gate (reads locked + cited, derived deterministically, verified by counts; "
             "drift 0, offline). 11/11 reproducibility gates pass.", "",
             "## Core facts",
             "- corr(γ, GC) = 0.99898 over the 27-target set (reproducible [V])",
             "- |h_sp| = (2/3√3) γ^1.5 (R19 firing-threshold scale)",
             "- three levers: L1 reduce inward current · L2 increase outward K+ · L3 remove sensitising drive",
             "- every clinical magnitude (potency, dose, efficacy, safety) is [O] — asserted nowhere", "",
             "## Hub",
             f"- [Non-Opioid Analgesic Map]({BASE}/)", "",
             "## Sections"]
    lines.append(f"- §0 {BASE}/how-to-read-this-map/")
    for lev in ["L1", "L2", "L3", "master", "context"]:
        slug, code, title, _ = LEVER_PAGE[lev]
        lines.append(f"- {code} {BASE}/{slug}/")
        grp = LV.get(lev, [])
        if lev == "L1":
            grp = grp + LV.get("L1-adjacent", [])
        for e in grp:
            lines.append(f"- {e['gene']} {BASE}/{target_slug(e['gene'])}/")
    for slug, code, title, _ in SECTIONS:
        if slug == "how-to-read-this-map":
            continue
        lines.append(f"- {code} {BASE}/{slug}/")
    return "\n".join(lines) + "\n"

def build_meta():
    chapters = []
    pos = 1
    for p in ORDER:
        ch = {"no": p["code"], "slug": p["slug"], "title": p["title"], "kind": p["kind"]}
        if p["kind"] == "target":
            e = by_gene[p["gene"]]
            ch["gene"] = p["gene"]
            ch["gamma"] = e["gamma"]
            ch["h_sp"] = e["spinodal_h_sp"]
            ch["lever"] = e["lever"]
            ch["grade"] = "forced"
        elif p["kind"] == "lever":
            ch["grade"] = "forced"
        chapters.append(ch)
        pos += 1
    return {
        "paper_id": "analgesic", "code": "anl", "version": VERSION,
        "layout": ("multi-page canonical: hub at docs/analgesic/index.html; each section AND each of the 27 targets "
                   "is its own self-contained page at docs/analgesic/{slug}/index.html (clean URL /analgesic/{slug}/), "
                   "mirroring vp_physics_v0_11_0. VP-SPEC v1.8 C1–C4 substance preserved; every clinical magnitude [O]."),
        "title": "A DNA-Grounded Map of 27 Non-Opioid Analgesic Targets",
        "short": SHORT, "doi": DOI, "hub_url": "/analgesic/", "branch": "jamming (neuro/dna offshoot)",
        "abstract": ("A single jamming-lattice read (γ) is taken for 27 nociception genes and mapped onto the R19 "
                     "firing-threshold scale; reads are bit-reproducible (corr(γ,GC)=0.99898, drift 0). γ reads "
                     "promoter switch-threshold structure only — every clinical magnitude is [O]. Targets are sorted "
                     "into three levers, ranked by burden, and a precision local-anaesthesia map is added. "
                     "Proposal-only, CC BY 4.0."),
        "headline_results": ["corr(γ, GC) = 0.99898", "27 targets, three levers", "every clinical magnitude [O]"],
        "firewall": "γ = promoter switch-threshold structure; never a voltage, potency, dose, in-vivo selectivity, or clinical effect.",
        "reproduce": "repro/run_all.py — 11/11 checks, drift 0, offline",
        "n_pages": len(ORDER) + 1,
        "chapters": chapters,
    }

if __name__ == "__main__":
    build_all()
    # report
    n = sum(len(files) for _, _, files in os.walk(f"{DOCS}/analgesic"))
    print("multi-page site written under", DOCS)
    print("pages (analgesic/**):", len([1 for r, d, f in os.walk(f"{DOCS}/analgesic") for x in f if x == "index.html"]))
    print("site files:", os.listdir(DOCS))
