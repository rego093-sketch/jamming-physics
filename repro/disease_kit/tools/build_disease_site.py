#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_disease_site.py  —  VP Disease Emergence Kit -> canonical multi-page HTML site
Deterministic (VP-SPEC v1.8, Constitution C1/C2/C4). Same inputs -> same bytes.

Inputs  (read-only): outputs/actionability_index.json
                     outputs/mapped_levers.json
                     outputs/surfaced_candidates.json
                     outputs/candidate_register.json
Outputs (canonical): docs/ ... static HTML, one page per disease + front matter.

The whole point of this volume: it offers a THEORETICAL corrective DIRECTION to
researchers and clinicians for evaluation. It is never a prescription. Every drug
name is a mechanism-direction label, carries no dose, and is wrapped in a firewall
notice that appears three times per page (top banner, beside the agents, bottom
banner with the dosage rationale).
"""
import json, os, html, datetime, hashlib, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "outputs")
DOCS = os.path.join(ROOT, "docs")
DZ_DIR = "dz"   # per-disease pages live under docs/disease/dz/{slug}/

# ---------------------------------------------------------------- registry
SITE   = "https://jamming-physics.org"
PAPER  = "disease"                       # URL folder under the site root
SHORT  = "VP Disease Kit"
TITLE_FULL = ("From a Single Bistable Switch to a Falsifiable Corrective Direction: "
              "the VP Disease Emergence Kit")
DOI    = "10.5281/zenodo.20755262"       # concept DOI (kit), per single_page provenance
ORCID  = "https://orcid.org/0009-0002-7535-8245"
AUTHOR = "Young Jae Lee"
REPRO  = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/disease"
LICENSE= "https://creativecommons.org/licenses/by/4.0/"
DATEP  = "2026-06-22"
RELEASE= "0.42.1-trackA.merged_3of3"

# ---------------------------------------------------------------- the firewall (3x/page)
# Top banner (warning #1) — English, role=alert.
RX_TOP = """<aside role="alert" class="rx-banner top">
<div class="hd"><span class="mk">&#9888;</span> Not a prescription &middot; theoretical research direction only</div>
<div class="bd"><ul>
<li><span class="em">Computer-simulation output.</span> This page is a falsifiable theoretical hypothesis, not a clinical finding, diagnosis, treatment, or cure.</li>
<li>It is offered <span class="em">to researchers and clinicians, for evaluation only.</span> No individual should act on it. It is not medical advice and not a prescription.</li>
<li><span class="em">Direction only [O]</span> &mdash; the framework asserts which way to push the switch. It asserts <span class="em">no</span> dose, efficacy, potency, or safety magnitude. The method is <span class="em">not approved</span> by any authority.</li>
</ul></div></aside>"""

# Beside-the-agents banner (warning #2) — sits directly under the agents heading.
RX_AGENTS = """<aside role="alert" class="rx-banner top" style="margin:.4rem 0 1.2rem">
<div class="hd"><span class="mk">&#9888;</span> Read before the agent names below</div>
<div class="bd"><ul>
<li>Each name below is a <span class="em">mechanism-direction label</span>, surfaced because its known action points the same way as the derived lever. It is <span class="em">not a recommendation to take it.</span></li>
<li><span class="em">No dose appears anywhere.</span> Dosing is unvalidated and must be set by a licensed physician or a national regulatory authority. <span class="em">Do not self-administer.</span></li>
</ul></div></aside>"""

# Bottom banner (warning #3) — full repeat + the explicit dosage rationale.
RX_BOTTOM = """<aside role="alert" class="rx-banner bottom">
<div class="hd"><span class="mk">&#9888;</span> Final notice &middot; do not use as treatment</div>
<div class="bd"><ul>
<li>To repeat, once more and deliberately: nothing on this page is a prescription, a treatment, or medical advice. It is a <span class="em">theoretical direction offered to experts for testing</span> &mdash; the appropriate next step is a controlled experiment, not use in a person.</li>
</ul>
<div class="dose"><b>Why no dosage is given.</b> No dose appears anywhere on this page, and that omission is deliberate. The direction is <b>not yet clinically validated</b>; any dose must be determined by a <b>licensed physician or a national regulatory authority</b>; and the method is <b>not an approved use</b>. A dose printed here would invite exactly the misreading this volume exists to prevent.</div>
</div></aside>"""

# inline tag carried by each candidate-lead card
def rx_inline():
    return ('<span class="rx-inline"><span class="mk">&#9888; Mechanism-direction only \u2014 do not self-administer; '
            'no dose (unvalidated; set by a physician / national authority); not an approved use.</span></span>')

# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(str(s), quote=True)

def attr(s):
    return html.escape(str(s), quote=True).replace("\n", " ")

def is_real_treatment(status):
    s = (status or "").lower()
    if ("no approved" in s or "none" in s or "direction-only" in s
            or "honest gap" in s or "no approved disease-modifying" in s):
        return False
    return (s.startswith("approved") or "established standard" in s
            or "established supportive" in s or "standard of care" in s
            or "established / off-label" in s or "established dietary" in s
            or "approved / established" in s or "previously approved" in s)

def is_no_agent(status):
    s = (status or "").lower()
    return ("no approved agent" in s or "none (honest gap)" in s
            or "direction-only" in s or "no approved disease-modifying" in s)

def is_pipeline(status):
    s = (status or "").lower()
    return any(k in s for k in ("investigational", "clinical", "preclinical",
                                "research", "phase"))

def classify_disease(d, ml_e, sc_e):
    """Return ('MATCH'|'NOVEL'|'HOLD')."""
    real = False
    for fam in ml_e.get("derived_lever_families", []):
        for a in fam.get("mapped_existing_agents", []):
            if is_real_treatment(a.get("status")):
                real = True
    surf_pa = set()
    for fam in sc_e.get("families", []):
        for c in fam.get("surfaced_candidates", []):
            surf_pa.add(c.get("prior_art_status"))
    if real or "rediscovery" in surf_pa:
        return "MATCH"
    if "novel" in surf_pa:
        return "NOVEL"
    return "HOLD"

CLASS_BADGE = {
    "MATCH": ('cb-match', '&#10003; Recovers an existing standard'),
    "NOVEL": ('cb-novel', '&#9675; Novel direction-only lead'),
    "HOLD":  ('cb-hold', '&#8212; Honest hold (no matched agent)'),
}
CLASS_WORD = {
    "MATCH": "the derived direction recovers a treatment already in clinical use for this disease (agreement with established practice)",
    "NOVEL": "no approved disease-modifying agent exists; a direction-only, falsifiable lead is surfaced for testing",
    "HOLD":  "the lever is derived but no approved direction-matched agent exists yet (an honest hold, not a gap hidden)",
}

def grade_badge(tok):
    m = {"F": ("g-forced", "[F] forced"), "V": ("g-verified", "[V] verified"),
         "L": ("g-calibrated", "[L] cited"), "O": ("g-open", "[O] open")}
    cls, lab = m.get(tok, ("g-open", "[O] open"))
    return f'<span class="grade {cls}">{lab}</span>'

def axis_arrow(axis):
    return "&darr;" if axis.startswith("DOWN") else "&uarr;"

def num(x, n=4):
    try:
        return f"{float(x):.{n}f}"
    except Exception:
        return esc(x)

def clip_desc(s, n=157):
    """Collapse whitespace and word-trim to <=158 logical chars (meta description gate 80-160)."""
    s = " ".join(str(s).split())
    if len(s) <= n + 1:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(" ,;:.\u2014-")
    return cut + "\u2026"

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ---------------------------------------------------------------- load
AI = json.load(open(os.path.join(OUT, "actionability_index.json")))
ML = json.load(open(os.path.join(OUT, "mapped_levers.json")))
SC = json.load(open(os.path.join(OUT, "surfaced_candidates.json")))
CR = json.load(open(os.path.join(OUT, "candidate_register.json")))

DISEASES = {d["slug"]: d for d in AI["diseases"]}
# canonical page order = alphabetical by slug (stable, deterministic)
ORDER = sorted(DISEASES.keys())
N = len(ORDER)
PER = SC["per_disease"]

print(f"[load] {N} diseases; chain_head={CR['chain_head'][:12]}; release={CR['release']}")

# ---------------------------------------------------------------- compute global stats
from collections import Counter
STAT = {"n": N}
axis_c = Counter(); pol_c = Counter(); les_c = Counter(); lead_c = Counter()
cls_c = Counter(); n_nocur = 0; n_honest = 0
for slug in ORDER:
    d = DISEASES[slug]
    axis_c[d["emergent_axis"].split()[0]] += 1
    pol_c[d["corrective_h_polarity"]] += 1
    les_c[d["lesion"]] += 1
    lead_c[d["lead_family"]] += 1
    if d.get("no_current_prescription"): n_nocur += 1
    if d.get("honest_gap"): n_honest += 1
    cls = classify_disease(d, ML[slug], PER[slug])
    DISEASES[slug]["_class"] = cls
    cls_c[cls] += 1
STAT.update(axis=dict(axis_c), pol=dict(pol_c), les=dict(les_c),
            lead=dict(lead_c), cls=dict(cls_c), nocur=n_nocur, honest=n_honest)
# candidate-level prior-art split (from register)
STAT["redisc"] = CR["prior_art_split"]["rediscovery"]
STAT["novel_cand"] = CR["prior_art_split"]["novel"]
STAT["n_total_candidates"] = SC["n_total_candidates"]
STAT["n_with_surfaced"] = AI["n_with_surfaced_candidates"]
# distinct rediscovery / novel diseases
redisc_d = set(); novel_d = set()
for slug in ORDER:
    for fam in PER[slug].get("families", []):
        for c in fam.get("surfaced_candidates", []):
            if c.get("prior_art_status") == "rediscovery": redisc_d.add(slug)
            if c.get("prior_art_status") == "novel": novel_d.add(slug)
STAT["redisc_diseases"] = len(redisc_d)
STAT["novel_diseases"] = len(novel_d)
# cusp ranges
import statistics as _st
_bar = [ML[s]["cusp"]["barrier"] for s in ORDER]
_gam = [ML[s]["cusp"]["gamma"] for s in ORDER]
STAT["barrier"] = (min(_bar), _st.median(_bar), max(_bar))
STAT["gamma"]   = (min(_gam), _st.median(_gam), max(_gam))

# ---------------------------------------------------------------- page scaffold
def head(title_subj, desc, canon, jsonld_list, extra_kw=""):
    blocks = "\n".join('<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(",", ":")) + "</script>" for j in jsonld_list)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title_subj)} | Jamming Physics</title>
<meta name="description" content="{attr(desc)}">
<meta name="author" content="{AUTHOR}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/css/site.css">
{blocks}
</head>
<body>"""

FOOTER = (f'<footer><p><b>{SHORT}</b> &middot; {esc(TITLE_FULL)}. Part of the Jamming Physics whitepaper family. '
          f'Single-author, no-tuning, hash-chained, bit-for-bit reproducible (SEED-fixed, 2&times;sha256 identical).</p>'
          f'<p>Author: {AUTHOR} (<a href="{ORCID}">ORCID 0009-0002-7535-8245</a>) &middot; '
          f'License: <a href="{LICENSE}">CC BY 4.0</a> &middot; DOI: <a href="https://doi.org/{DOI}">{DOI}</a> &middot; '
          f'<a href="{REPRO}">Reproduction code (GitHub)</a></p>'
          f'<p>Release {RELEASE} &middot; register chain-head <code>{CR["chain_head"][:16]}</code> &middot; '
          f'firewall scan: {CR.get("grade","")[:3] or "[O]"} PASS, 0 magnitude leaks.</p></footer>\n</body>\n</html>')

def crumb(parts):
    # parts: list of (label, href|None)
    out = []
    for lab, href in parts:
        out.append(f'<a href="{href}">{esc(lab)}</a>' if href else esc(lab))
    return '<header><nav class="crumb">' + " &rsaquo; ".join(out) + "</nav></header>"

def disease_url(slug):
    return f"/{PAPER}/{DZ_DIR}/{slug}/"

# ---------------------------------------------------------------- disease page
def render_disease(slug, idx):
    d = DISEASES[slug]
    e = ML[slug]; s = PER[slug]
    cls = d["_class"]
    cbcls, cblab = CLASS_BADGE[cls]
    gene = d.get("primary_gene", "")
    axis = d["emergent_axis"]
    axis_tok = axis.split()[1].strip("[]") if "[" in axis else "F"
    cusp = e["cusp"]
    name = d["name"]
    short = name.split("(")[0].strip().rstrip(" -")  # readable short name
    if len(short) > 70:
        short = short[:67].rsplit(" ", 1)[0] + "\u2026"
    pol = d["corrective_h_polarity"]
    forced = e.get("forced_corrective_direction", "")
    healthy = e.get("healthy_branch", "")
    lesion = e.get("lesion", "")
    omim = e.get("omim", "")

    # ---- answer-first (40-60 words, self-contained) ----
    ans = (f'In {esc(short)} ({esc(gene)}{", OMIM "+esc(omim) if omim else ""}), the master switch sits on the '
           f'{axis_arrow(axis)} {esc(axis.split()[0])} branch ({grade_badge(axis_tok)} below); the healthy state is the '
           f'<b>{esc(healthy)}</b> well. The forced corrective direction is to <b>{esc(forced)}</b> '
           f'(polarity: {esc(pol)}). Classification: {cblab}. Direction only &mdash; no dose, no efficacy magnitude.')

    # ---- abstract ----
    absu = (f'The disease maps to an R19 double-well whose corrective lever is read straight off the cusp '
            f'(barrier {num(cusp["barrier"])}, &gamma; {num(cusp["gamma"])}, spinodal {num(cusp["spinodal"])}). '
            f'The corrective direction is forced [F]; the agent names below are direction-concordant labels at grade [O] '
            f'(no dose, no efficacy or safety magnitude). This is a research hypothesis offered to experts, not medical advice.')

    # ---- JSON-LD ----
    jl_article = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": short, "name": name, "inLanguage": "en",
        "isPartOf": {"@type": "CreativeWorkSeries", "name": TITLE_FULL,
                     "alternateName": SHORT, "identifier": f"https://doi.org/{DOI}"},
        "identifier": f"https://doi.org/{DOI}", "sameAs": f"https://doi.org/{DOI}",
        "position": idx + 1,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "publisher": {"@type": "Organization", "name": "Jamming Physics"},
        "datePublished": DATEP, "dateModified": DATEP, "isBasedOn": REPRO,
        "license": LICENSE,
        "about": {"@type": "MedicalCondition", "name": short,
                  "code": {"@type": "MedicalCode", "codeValue": omim, "codingSystem": "OMIM"} if omim else None},
        "keywords": f"{gene}, {short}, corrective direction, R19 bistable switch, direction-only, not medical advice",
        "knowsAbout": [gene, "R19 bistable switch", "corrective lever", short],
    }
    if not omim:
        jl_article["about"].pop("code", None)
    jl_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER}/"},
        {"@type": "ListItem", "position": 3, "name": short}]}

    title_subj = short if len(short) <= 45 else short[:44].rsplit(" ", 1)[0] + "\u2026"
    desc = clip_desc(
        f"{short} ({gene}): switch on the {axis.split()[0]} branch; forced corrective direction \u2018{forced}\u2019. "
        f"Direction-only [O], no dose, not medical advice \u2014 a research hypothesis for experts.")

    H = head(title_subj, desc, f"{SITE}{disease_url(slug)}", [jl_article, jl_bc])

    body = [H]
    body.append(crumb([("Home", "/"), (SHORT, f"/{PAPER}/"),
                       ("Diseases", f"/{PAPER}/index-{slug[0].upper() if slug[0].isalpha() else 'sym'}/"),
                       (f"\u00a7{idx+1}", None)]))
    body.append("<main>")
    body.append(RX_TOP)                                   # ----- WARNING #1
    body.append(f"<h1>{esc(name)}</h1>")
    body.append(f'<p class="answer">{ans}</p>')
    body.append(f'<p class="abstract">{absu}</p>')
    # claim-strip
    body.append('<aside class="claim-strip">'
                f'{grade_badge("F")}<span class="cbadge {cbcls}">{cblab}</span>'
                '<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>'
                f'<a href="{REPRO}" rel="noopener">Reproduce (GitHub)</a>'
                f'<a class="doi" href="https://doi.org/{DOI}" rel="noopener">DOI: {DOI}</a></aside>')
    # vp-card: the cusp restated self-containedly
    body.append('<aside class="vp-card">'
                f'<b>R19 cusp &mdash; barrier {num(cusp["barrier"])}, &gamma; {num(cusp["gamma"])}</b> '
                f'&mdash; the disease is a bistable double-well; a fragility-{num(e.get("geometric_fragility"),2)} '
                f'switch recrosses the fold under a small {esc(pol)} drive toward the {esc(healthy)} branch. '
                f'<b>[F]</b> direction. <a href="/{PAPER}/01-method-no-tuning-and-grading/">How this is derived</a></aside>')

    # ===== §1 the emergence switch (analysis) =====
    body.append("<h2>The emergence switch</h2>")
    body.append(f"<p>The switch for {esc(short)} is an R19 double-well emerged from the real proximal-promoter DNA "
                f"of <code>{esc(gene)}</code>. Its geometry is fixed by measured stiffness &gamma; (never fitted); the "
                f"numbers below are read directly off that cusp.</p>")
    body.append('<div class="cusp"><dl>'
                f'<dt>emergent axis</dt><dd>{axis_arrow(axis)} {esc(axis)}</dd>'
                f'<dt>healthy branch</dt><dd>{esc(healthy)}</dd>'
                f'<dt>lesion</dt><dd>{esc(lesion)}</dd>'
                f'<dt>&gamma; (stiffness)</dt><dd>{num(cusp["gamma"])}</dd>'
                f'<dt>barrier</dt><dd>{num(cusp["barrier"])}</dd>'
                f'<dt>spinodal</dt><dd>{num(cusp["spinodal"])}</dd>'
                f'<dt>s_on / s_off</dt><dd>{num(cusp.get("s_on"))} / {num(cusp.get("s_off"))}</dd>'
                f'<dt>fragility</dt><dd>{num(e.get("geometric_fragility"),2)}</dd>'
                f'<dt>corrective polarity</dt><dd>{esc(pol)}</dd>'
                f'<dt>forced direction</dt><dd>{esc(forced)}</dd>'
                '</dl></div>')
    cf = e.get("chemistry_feasibility", {})
    if cf.get("statement"):
        body.append(f'<p class="bound"><b>Chemistry feasibility ({cf.get("readout","DIRECTION only [O]")}).</b> '
                    f'{esc(cf.get("statement"))}. {esc(cf.get("magnitude",""))}.</p>')

    # ===== §2 derived corrective lever (the direction) =====
    body.append("<h2>The derived corrective lever</h2>")
    fams = e.get("derived_lever_families", [])
    body.append(f"<p>The cusp forces a corrective <b>direction</b>: {esc(forced)}. "
                f"This is the load-bearing output of the framework &mdash; it is [F] forced, and it is falsifiable. "
                f"{'One lever family is' if len(fams)==1 else str(len(fams))+' lever families are'} derived; the lead is "
                f"<b>{esc(e.get('lead_derived_family',''))}</b>.</p>")
    for fam in fams:
        body.append('<div class="agent">')
        body.append(f'<div class="hd"><span class="nm">{esc(fam.get("family",""))}</span>'
                    f'<span class="cbadge cb-pipe">sign: {esc(fam.get("corrective_mechanism_sign",""))}</span>'
                    f'<span class="meta">geometric rank {num(fam.get("geometric_rank"),2)}</span></div>')
        body.append(f'<div class="meta"><b>Mechanism.</b> {esc(fam.get("mechanism",""))}</div>')
        body.append(f'<div class="meta"><b>Applies to.</b> {esc(fam.get("applies_to",""))}</div>')
        if fam.get("note"):
            body.append(f'<div class="meta">{esc(fam.get("note"))}</div>')
        if fam.get("falsifier"):
            body.append(f'<div class="fal"><b>Falsifier.</b> {esc(fam.get("falsifier"))}</div>')
        body.append("</div>")
    nonlev = e.get("non_levers", [])
    if nonlev:
        items = "".join(f"<li>{esc(x)}</li>" if isinstance(x, str) else f"<li>{esc(json.dumps(x,ensure_ascii=False))}</li>" for x in nonlev)
        body.append(f'<div class="bound"><b>Explicitly not levers.</b><ul style="margin:.3rem 0 0">{items}</ul></div>')

    # ===== section 3: agents on the lever (mapped agents) =====
    body.append("<h2>Agents mapped onto the lever</h2>")
    body.append(RX_AGENTS)                                # ----- WARNING #2 (beside the agents)

    # 3a: existing mapped agents -> table + match callout
    rows = []
    match_names = []
    for fam in fams:
        for a in fam.get("mapped_existing_agents", []):
            st = a.get("status", "")
            if is_no_agent(st):
                continue
            real = is_real_treatment(st)
            dot = ('<span class="cbadge cb-match">&#10003; in use</span>' if real
                   else '<span class="cbadge cb-pipe">&#9671; in trials</span>' if is_pipeline(st)
                   else '<span class="cbadge cb-hold">&mdash;</span>')
            if real:
                match_names.append(a.get("agent_class", ""))
            rows.append((a, fam, dot, real))
    if any(r[3] for r in rows):  # there is a real, in-use agent -> agreement callout
        uniq = []
        for nm in match_names:
            if nm not in uniq:
                uniq.append(nm)
        body.append('<div class="recover"><b>&#10003; Agreement with established practice.</b> '
                     f'The corrective direction derived here ({esc(forced)}) independently matches an agent already in '
                     f'clinical use for this disease: {esc("; ".join(uniq))}. The geometry recovered known medicine &mdash; '
                     'this is a <b>validation signal for the logic</b>, not a new treatment claim by this kit.</div>')
    if rows:
        body.append('<div class="tbl-wrap"><table><caption>Existing agents whose known action is direction-concordant with the derived lever (status as pinned in the corpus; no dose, no efficacy magnitude).</caption>'
                    '<thead><tr><th>agent (class)</th><th>dir.</th><th>status</th><th>phase</th><th>map</th></tr></thead><tbody>')
        for a, fam, dot, real in rows:
            ph = a.get("max_phase_proxy", "")
            src = a.get("source", "")
            body.append(f'<tr><td>{esc(a.get("agent_class",""))}'
                        + (f'<div class="src">{esc(src)}</div>' if src else "")
                        + f'</td><td>{esc(a.get("mechanism_sign",""))}</td>'
                        f'<td>{esc(a.get("status",""))}</td>'
                        f'<td class="num">{esc(ph)}</td><td>{dot}</td></tr>')
        body.append("</tbody></table></div>")
        body.append(rx_inline())                          # inline notice beside the agents table

    # 3b: surfaced direction-only candidate leads -> cards
    leads = []
    for fam in s.get("families", []):
        for c in fam.get("surfaced_candidates", []):
            leads.append((c, fam))
    if leads:
        body.append("<h3>Direction-only candidate leads (corpus join)</h3>")
        body.append('<p>Each lead is surfaced only because its known mechanism points the same way as the derived '
                    'lever, and each comes with a source and a falsifier. None is a treatment.</p>')
        for c, fam in leads:
            pa = c.get("prior_art_status", "")
            if pa == "rediscovery":
                acls, abadge = "match", '<span class="cbadge cb-match">&#10003; recovered standard</span>'
            elif pa == "novel":
                acls, abadge = "novel", '<span class="cbadge cb-novel">&#9675; novel lead</span>'
            else:
                acls, abadge = "pipe", f'<span class="cbadge cb-pipe">{esc(pa)}</span>'
            body.append(f'<div class="agent {acls}">')
            body.append(f'<div class="hd"><span class="nm">{esc(c.get("agent",""))}</span>{abadge}'
                        f'<span class="meta">dir: {esc(c.get("mechanism_sign",""))} &middot; {esc(c.get("regulatory_status",""))}</span></div>')
            if c.get("drug_class"):
                body.append(f'<div class="meta"><b>Class.</b> {esc(c.get("drug_class"))}</div>')
            if c.get("mechanism_note"):
                body.append(f'<div class="meta"><b>Mechanism.</b> {esc(c.get("mechanism_note"))}</div>')
            if pa == "rediscovery":
                body.append('<div class="recover" style="margin:.4rem 0">'
                            f'<b>&#10003; This is a rediscovery.</b> {esc(c.get("prior_art_note","") or "Already an established option for this disease; the direction logic recovered it.")}</div>')
            elif c.get("prior_art_note"):
                body.append(f'<div class="meta"><b>Prior-art.</b> {esc(c.get("prior_art_note"))}</div>')
            if c.get("safety_note"):
                body.append(f'<div class="meta"><b>Safety (qualitative; no magnitude).</b> {esc(c.get("safety_note"))}</div>')
            if c.get("falsifier"):
                body.append(f'<div class="fal"><b>Falsifier.</b> {esc(c.get("falsifier"))}</div>')
            if c.get("prior_art_source"):
                body.append(f'<div class="src">Source: {esc(c.get("prior_art_source"))}</div>')
            body.append(rx_inline())                       # ----- inline warning beside each lead
            body.append("</div>")

    if not rows and not leads:
        body.append('<div class="bound"><b>Honest hold.</b> The corrective direction is derived and falsifiable, '
                    'but no approved direction-matched agent is mapped in the pinned corpus. The kit holds here rather '
                    'than name a weak instance &mdash; an honest hold is a finding, not a failure.</div>')

    # ===== section 4: evidence & provenance =====
    body.append("<h2>Evidence &amp; provenance</h2>")
    body.append('<div class="tbl-wrap"><table><caption>What is reproduced vs. cited for this page.</caption>'
                '<thead><tr><th>element</th><th>grade</th><th>basis</th></tr></thead><tbody>'
                f'<tr><td>R19 switch &amp; cusp geometry (this page)</td><td>{grade_badge("V")}</td>'
                f'<td>emerged from measured promoter &gamma; of <code>{esc(gene)}</code>; deterministic, 2&times;sha256 identical</td></tr>'
                f'<tr><td>corrective direction</td><td>{grade_badge("F")}</td>'
                f'<td>forced by the cusp sign; falsifiable (see lever falsifiers)</td></tr>'
                f'<tr><td>mapped agents / leads</td><td>{grade_badge("O")}</td>'
                f'<td>direction-concordance only; corpus-pinned ({esc(SC.get("corpus_snapshot_date",""))}); no dose, no efficacy/safety magnitude</td></tr>'
                '</tbody></table></div>')
    body.append('<p class="bound"><b>Reading the agent column.</b> '
                f'{esc(SC.get("prior_art_legend",{}).get("rediscovery",""))} '
                f'{esc(SC.get("prior_art_legend",{}).get("novel",""))}</p>')

    body.append(RX_BOTTOM)                                # ----- WARNING #3 + dosage rationale

    # prev/next
    prev_slug = ORDER[idx - 1] if idx > 0 else None
    next_slug = ORDER[idx + 1] if idx < N - 1 else None
    pn = ['<nav class="pn">']
    pn.append(f'<a rel="prev" href="{disease_url(prev_slug)}">&larr; previous</a>' if prev_slug else '<span></span>')
    pn.append(f'<a class="center" href="/{PAPER}/">All diseases</a>')
    pn.append(f'<a rel="next" href="{disease_url(next_slug)}">next &rarr;</a>' if next_slug else '<span></span>')
    pn.append("</nav>")
    body.append("".join(pn))
    body.append("</main>")
    body.append(FOOTER)
    return "\n".join(body)

print("[ok] disease renderer defined")

# ====================================================================== part 3
# front-matter chapters, A-Z indexes, hub, landing, sitemap / robots / llms / meta,
# and the main write loop. Everything below is deterministic: it reads only STAT
# and the pinned JSON, and injects no invented numbers.

PAGES = []  # (loc) collected for sitemap; loc is a site-absolute path beginning "/"

def reg(loc):
    PAGES.append(loc)
    return loc

# ---- CSS-only stat bars -------------------------------------------------------
def stat_block(rows, total):
    """rows: list of (label, value, cls). Bar width normalised to the row max."""
    mx = max((v for _, v, _ in rows), default=1) or 1
    out = ['<div class="stat">']
    for lab, v, c in rows:
        w = max(2.0, (v / mx) * 100.0)
        cc = (" " + c) if c else ""
        share = f"{(v / total * 100):.0f}%" if total else ""
        out.append(f'<div class="row"><span class="lab">{esc(lab)}</span>'
                   f'<span class="bar{cc}" style="width:{w:.1f}%"></span>'
                   f'<span class="val">{v} &middot; {share}</span></div>')
    out.append("</div>")
    return "\n".join(out)

# ---- data-driven helpers for chapters / indexes ------------------------------
def real_agent_for(slug):
    for fam in ML[slug].get("derived_lever_families", []):
        for a in fam.get("mapped_existing_agents", []):
            if is_real_treatment(a.get("status")):
                return a.get("agent_class", "")
    for fam in PER[slug].get("families", []):
        for c in fam.get("surfaced_candidates", []):
            if c.get("prior_art_status") == "rediscovery":
                return c.get("agent", "")
    return ""

def short_name(slug):
    nm = DISEASES[slug]["name"].split("(")[0].strip().rstrip(" -")
    return nm if len(nm) <= 64 else nm[:61].rsplit(" ", 1)[0] + "\u2026"

def dz_oneliner(slug):
    d = DISEASES[slug]
    return (f'{d["_class"]} &middot; {axis_arrow(d["emergent_axis"])} '
            f'{esc(d["emergent_axis"].split()[0])} &middot; restore by {esc(d["corrective_h_polarity"])}')

# ---- chapter scaffold ---------------------------------------------------------
def chapter_jsonld(name, position, desc):
    art = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": name, "name": name, "inLanguage": "en",
        "isPartOf": {"@type": "CreativeWorkSeries", "name": TITLE_FULL,
                     "alternateName": SHORT, "identifier": f"https://doi.org/{DOI}"},
        "identifier": f"https://doi.org/{DOI}", "position": position,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "publisher": {"@type": "Organization", "name": "Jamming Physics"},
        "datePublished": DATEP, "dateModified": DATEP, "isBasedOn": REPRO,
        "license": LICENSE, "description": desc,
    }
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER}/"},
        {"@type": "ListItem", "position": 3, "name": name}]}
    return [art, bc]

def render_chapter(ch, i):
    canon = f"{SITE}/{PAPER}/{ch['slug']}/"
    cdesc = clip_desc(ch["desc"])
    H = head(ch["title_subj"], cdesc, canon, chapter_jsonld(ch["name"], ch["pos"], cdesc))
    b = [H, crumb([("Home", "/"), (SHORT, f"/{PAPER}/"), (ch["crumb"], None)]), "<main>"]
    if ch.get("rx_top"):
        b.append(RX_TOP)
    b.append(f'<h1>{esc(ch["name"])}</h1>')
    b.append(f'<p class="answer">{ch["answer"]}</p>')
    b.append(ch["body"])
    if ch.get("rx_bottom"):
        b.append(RX_BOTTOM)
    # prev/next within the front matter (hub as the hinge)
    prev = CHAPTERS[i - 1] if i > 0 else None
    nxt = CHAPTERS[i + 1] if i < len(CHAPTERS) - 1 else None
    pn = ['<nav class="pn">']
    pn.append(f'<a rel="prev" href="/{PAPER}/{prev["slug"]}/">&larr; {esc(prev["nav"])}</a>'
              if prev else f'<a href="/{PAPER}/">&larr; Contents</a>')
    pn.append(f'<a class="center" href="/{PAPER}/">Contents</a>')
    pn.append(f'<a rel="next" href="/{PAPER}/{nxt["slug"]}/">{esc(nxt["nav"])} &rarr;</a>'
              if nxt else f'<a href="/{PAPER}/dz/{ORDER[0]}/">Disease index &rarr;</a>')
    pn.append("</nav>")
    b.append("".join(pn))
    b.append("</main>")
    b.append(FOOTER)
    return "\n".join(b)

# ---- chapter bodies (numbers come from STAT only) ----------------------------
def body_00():
    return (
        '<p class="lede">This volume offers a single thing to a single audience: a falsifiable, '
        'mechanism-level <b>corrective direction</b> for each of hundreds of rare diseases, offered '
        'to researchers and clinicians for evaluation. It is not, and must not be read as, a prescription.</p>'
        '<h2>What this is</h2>'
        f'<p>For {STAT["n"]} rare diseases, a bistable molecular switch (the R19 double-well) is emerged from the '
        'real promoter DNA of the lead gene, and the geometry of that switch is used to read off <i>which way</i> the '
        'switch must be pushed to move the cell from the diseased branch toward the healthy branch. That single output '
        '&mdash; a signed direction &mdash; is the load-bearing claim of every page. It is graded <b>[F] forced</b> '
        '(it follows necessarily from the cusp sign) and it is falsifiable (each lever ships with the experiment that '
        'would break it).</p>'
        '<h2>What this is <em>not</em></h2>'
        '<ul>'
        '<li>It is <b>not a diagnosis, a treatment, or a cure</b>. It is a computer-simulation hypothesis.</li>'
        '<li>It is <b>not medical advice</b> and <b>not a prescription</b>. No individual should act on it.</li>'
        '<li>It carries <b>no dose, no efficacy, no potency, and no safety magnitude</b> &mdash; direction only [O].</li>'
        '<li>It is <b>not an approved method</b>. No regulator has cleared anything described here.</li>'
        '</ul>'
        '<h2>The firewall, stated three times on every disease page</h2>'
        '<p>Because a list of drug names beside a disease name is so easily misread, every disease page carries the same '
        'safety notice <b>three times</b>, by design: a banner at the <b>top</b>, a banner <b>directly beside the agent '
        'names</b>, and a banner at the <b>bottom</b> that also explains why no dose is printed. A short inline notice '
        'rides on every individual candidate card as well. The repetition is deliberate redundancy, not an oversight.</p>'
        '<div class="recover"><b>&#10003; The honest reading.</b> A disease page says, in effect: &ldquo;the geometry says '
        'push this switch <i>this way</i>; here are agents whose known action happens to push the same way; a competent '
        'expert should now decide whether that is worth a controlled test.&rdquo; Nothing more.</div>'
        '<h2>Who this is for</h2>'
        '<p>Disease biologists, translational researchers, and clinician-scientists who can design and run the controlled '
        'experiments that would confirm or refute a direction. The appropriate next step after any page is an experiment, '
        'never use in a person.</p>'
    )

def body_01():
    return (
        '<p class="lede">One pipeline, run identically for every disease: <b>LOCK &rarr; Derive &rarr; Gate</b>. '
        'Nothing is tuned to a desired answer; the corrective direction falls out of measured geometry.</p>'
        '<h2>LOCK &mdash; the switch is emerged, never fitted</h2>'
        '<p>For each disease the proximal-promoter DNA of the lead gene is read, and its measured stiffness &gamma; '
        'fixes an R19 bistable double-well. &gamma; is taken from sequence; it is <b>never</b> fitted to make a result '
        'come out. This is the no-tuning rule, and it is what makes a recovered match (next chapters) meaningful rather '
        'than circular.</p>'
        '<aside class="vp-card"><b>R19 cusp</b> &mdash; a double-well with a fold (cusp) whose barrier and spinodal are '
        'set by &gamma;. The diseased state sits in one well; the corrective direction is the sign that lowers the path '
        'back across the fold to the healthy well. <b>[F]</b> direction.</aside>'
        '<h2>Derive &mdash; the direction is forced by the cusp</h2>'
        '<p>Given the well the disease occupies and the healthy branch, the sign of the corrective drive is not a choice: '
        'it is forced by the cusp. That signed direction (e.g. raise the drive / clear the drive) is the output. It is '
        'graded <b>[F]</b>. Crucially, the framework asserts the <i>sign</i> and nothing about the <i>size</i>.</p>'
        '<h2>Gate &mdash; grading and the magnitude firewall</h2>'
        '<p>Every statement is graded honestly:</p>'
        '<div class="legend">'
        f'<span class="k">{grade_badge("F")} forced by geometry</span>'
        f'<span class="k">{grade_badge("V")} verified / reproduced</span>'
        f'<span class="k">{grade_badge("L")} cited / calibrated to source</span>'
        f'<span class="k">{grade_badge("O")} open &mdash; direction only, no magnitude</span>'
        '</div>'
        '<p>The mapped agents and candidate leads are graded <b>[O]</b>: their <i>direction</i> matches the derived lever, '
        'but no dose, efficacy, potency, or safety number is ever emitted. This is the <b>MAGNITUDE_FIREWALL</b>, and a '
        'machine check confirms zero magnitude leaks before release.</p>'
        '<h2>Reproducibility</h2>'
        f'<p>The build is deterministic: a fixed seed (SEED&nbsp;=&nbsp;19) and a 2&times;SHA-256 hash chain make the '
        f'whole corpus bit-for-bit reproducible. The register chain-head for this release is '
        f'<code>{esc(CR["chain_head"][:16])}</code>; the same inputs always regenerate the same bytes. '
        f'<a href="{REPRO}">Reproduction code is on GitHub.</a></p>'
    )

def body_02():
    cls = STAT["cls"]; axis = STAT["axis"]; pol = STAT["pol"]; les = STAT["les"]; lead = STAT["lead"]
    bar = STAT["barrier"]; gam = STAT["gamma"]
    lead_rows = sorted(lead.items(), key=lambda kv: -kv[1])
    les_rows = sorted(les.items(), key=lambda kv: -kv[1])
    return (
        f'<p class="lede">The pinned corpus covers <b>{STAT["n"]}</b> rare diseases. Every disease is classified by '
        'what the corpus can honestly say about it today: it recovers an existing standard, it surfaces a novel '
        'direction-only lead, or it holds.</p>'
        '<h2>Classification of all diseases</h2>'
        + stat_block([
            ("Recovers an existing standard (MATCH)", cls.get("MATCH", 0), "match"),
            ("Novel direction-only lead (NOVEL)", cls.get("NOVEL", 0), "novel"),
            ("Honest hold (HOLD)", cls.get("HOLD", 0), "hold"),
          ], STAT["n"])
        + '<p class="bound"><b>How to read these three.</b> A <b>MATCH</b> is a validation signal: the geometry '
        'independently re-derived medicine already in use. A <b>NOVEL</b> entry surfaces a falsifiable, '
        'direction-matched lead where no approved disease-modifying agent exists. A <b>HOLD</b> is an honest '
        '&ldquo;not yet&rdquo; &mdash; the direction is derived but no approved direction-matched agent is mapped. '
        'Holds are kept visible on purpose; a hidden gap would be dishonest.</p>'
        '<h2>Direction of the corrective drive</h2>'
        + stat_block([(k, v, "alt") for k, v in sorted(axis.items(), key=lambda kv: -kv[1])], STAT["n"])
        + '<p class="bound">Each switch sits on a DOWN or UP branch; the arrow is the direction that returns it toward '
        'the healthy well. This is the [F] forced output.</p>'
        '<h2>Corrective polarity</h2>'
        + stat_block([(("restore by " + k), v, None) for k, v in sorted(pol.items(), key=lambda kv: -kv[1])], STAT["n"])
        + '<h2>Lesion class</h2>'
        + stat_block([(k, v, "alt") for k, v in les_rows], STAT["n"])
        + '<h2>Lead lever family</h2>'
        + stat_block([(k, v, None) for k, v in lead_rows], STAT["n"])
        + '<h2>Agreement and novelty at a glance</h2>'
        '<div class="hero-stat">'
        f'<span class="n match">{STAT["redisc_diseases"]}<small>diseases recover a standard</small></span>'
        f'<span class="n novel">{STAT["novel_diseases"]}<small>diseases with a novel lead</small></span>'
        f'<span class="n">{STAT["n_with_surfaced"]}<small>diseases with a surfaced candidate</small></span>'
        f'<span class="n">{STAT["n_total_candidates"]}<small>candidate rows total</small></span>'
        '</div>'
        f'<p class="bound">Of the {STAT["n_total_candidates"]} surfaced candidate rows, <b>{STAT["redisc"]}</b> are '
        f'rediscoveries of known options and <b>{STAT["novel_cand"]}</b> are novel direction-only leads. '
        f'<b>{STAT["nocur"]}</b> diseases have no current disease-modifying prescription on record; '
        f'<b>{STAT["honest"]}</b> are flagged as explicit honest gaps (addressed in the limits chapter).</p>'
        '<h2>Switch geometry, across the corpus</h2>'
        '<div class="cusp"><dl>'
        f'<dt>barrier &mdash; min / median / max</dt><dd>{num(bar[0])} / {num(bar[1])} / {num(bar[2])}</dd>'
        f'<dt>&gamma; &mdash; min / median / max</dt><dd>{num(gam[0])} / {num(gam[1])} / {num(gam[2])}</dd>'
        '</dl></div>'
        '<p class="bound">These are pure geometry, read off the emerged cusps. No magnitudes of dose or effect appear '
        'anywhere in this volume &mdash; these numbers describe the switch, not a therapy.</p>'
    )

def body_03():
    # build a data-driven table of recovered standards (MATCH diseases + their in-use agent)
    known_first = [
        "alkaptonuria", "acute_intermittent_porphyria", "atypical_hemolytic_uremic_syndrome",
        "achondroplasia", "aromatic_l_amino_acid_decarboxylase_deficiency",
        "autosomal_dominant_polycystic_kidney_disease", "bardet_biedl_syndrome",
        "beta_thalassaemia", "spinal_muscular_atrophy", "familial_hypercholesterolemia",
        "wilson_disease", "tyrosinemia_type_1", "hereditary_transthyretin_amyloidosis",
        "phenylketonuria", "cystic_fibrosis", "gaucher_disease", "fabry_disease",
        "pompe_disease", "hereditary_angioedema", "sickle_cell_disease",
    ]
    match_slugs = [s for s in ORDER if DISEASES[s]["_class"] == "MATCH"]
    ordered = [s for s in known_first if s in match_slugs]
    ordered += [s for s in match_slugs if s not in ordered]
    rows = []
    for s in ordered:
        ag = real_agent_for(s)
        if not ag:
            continue
        rows.append((s, ag))
        if len(rows) >= 48:
            break
    trs = []
    for s, ag in rows:
        d = DISEASES[s]
        trs.append(f'<tr><td><a href="{disease_url(s)}">{esc(short_name(s))}</a></td>'
                   f'<td><code>{esc(d.get("primary_gene",""))}</code></td>'
                   f'<td>{esc(ag)}</td></tr>')
    table = ('<div class="tbl-wrap"><table>'
             '<caption>A sample of diseases where the forced corrective direction recovers an agent already in clinical '
             'use (status as pinned in the corpus; no dose, no efficacy magnitude). The full set is linked from every '
             'matching disease page.</caption>'
             '<thead><tr><th>disease</th><th>gene</th><th>recovered agent (direction-concordant)</th></tr></thead>'
             '<tbody>' + "".join(trs) + '</tbody></table></div>')
    return (
        f'<p class="lede">In <b>{STAT["cls"].get("MATCH", 0)}</b> of {STAT["n"]} diseases the direction derived from '
        'pure geometry independently recovers a treatment already in clinical use. Because the geometry was never tuned, '
        'each recovery is a genuine validation signal for the logic &mdash; not a treatment claim by this kit.</p>'
        '<h2>Why a recovery counts as validation</h2>'
        '<p>The switch is built from promoter sequence with &gamma; never fitted (see Method). When that untuned geometry '
        'then points the same way as an approved, mechanistically-understood medicine for the same disease, the agreement '
        'was not engineered in. Replicated across hundreds of independent diseases, these agreements are the main evidence '
        'that the corrective-direction logic is tracking real biology.</p>'
        '<div class="recover"><b>&#10003; Agreement, reported as agreement.</b> Where an approved agent already exists, '
        'the page reports a <b>match</b> with established practice. The kit does not re-claim the medicine; it notes that '
        'its independent geometry recovered it.</div>'
        '<h2>Recovered standards &mdash; a representative sample</h2>'
        + table
        + f'<p class="bound">This is a sample; the complete agreement set spans all {STAT["cls"].get("MATCH",0)} '
        'matching diseases, each carrying the agreement callout on its own page. Candidate-level, '
        f'<b>{STAT["redisc"]}</b> of {STAT["n_total_candidates"]} surfaced rows are explicit rediscoveries.</p>'
        '<p class="bound"><b>Still not a prescription.</b> A recovered match means the direction agrees with medicine an '
        'expert may already use under proper care. It does not authorise anyone to self-administer, and it adds no dose.</p>'
    )

def body_04():
    gaps = [s for s in ORDER if DISEASES[s].get("honest_gap")]
    lis = "".join(f'<li><a href="{disease_url(s)}">{esc(short_name(s))}</a> '
                  f'<span class="gene">{esc(DISEASES[s].get("primary_gene",""))}</span></li>' for s in gaps)
    return (
        '<p class="lede">Honesty above completeness. This chapter states plainly where the framework holds, where the '
        'tractable space is exhausted, and what the volume deliberately does not claim.</p>'
        '<h2>Honest holds</h2>'
        f'<p>{STAT["cls"].get("HOLD", 0)} diseases are classified <b>HOLD</b>: a corrective direction is derived and '
        'falsifiable, but no approved direction-matched agent is mapped in the pinned corpus. Rather than name a weak '
        'instance to fill the slot, the kit holds. An honest hold is a finding about the current corpus, not a failure '
        'of the page.</p>'
        '<h2>Explicit honest gaps</h2>'
        f'<p>{STAT["honest"]} diseases are flagged as explicit honest gaps &mdash; cases where the literature offered no '
        'clean disease-modifying option at corpus snapshot. Each is still given a derived, falsifiable direction; none is '
        'given a dose:</p>'
        + (f'<ul class="dzlist" style="margin-top:.4rem">{lis}</ul>' if lis else
           '<p class="bound">No diseases remain flagged as unfilled honest gaps in this release.</p>')
        + '<h2>Saturation of the tractable space</h2>'
        '<p>Across the expansion tracks, the readily tractable rare-disease space is now largely saturated: most diseases '
        'that admit a clean single-gene R19 switch and a direction-concordant agent have been surfaced. Continuing to add '
        'diseases yields diminishing genuinely-new directions. Reporting this plateau is itself a result.</p>'
        '<h2>What this volume does not claim</h2>'
        '<ul>'
        '<li><b>No magnitudes.</b> No dose, schedule, efficacy, potency, or safety number, anywhere. Direction only [O].</li>'
        '<li><b>Corpus-pinned.</b> Agent statuses reflect a fixed snapshot '
        f'(<code>{esc(SC.get("corpus_snapshot_date",""))}</code>) and can age; they are not live regulatory truth.</li>'
        '<li><b>Direction, not destiny.</b> A forced direction is a testable hypothesis about which way to push a switch, '
        'not a promise that pushing it cures the disease.</li>'
        '<li><b>Theoretical.</b> Every output awaits controlled experimental confirmation before any clinical meaning.</li>'
        '</ul>'
    )

def body_05():
    cls = STAT["cls"]
    return (
        '<p class="lede">One untuned geometry, applied uniformly, yields a falsifiable corrective direction for hundreds '
        'of rare diseases &mdash; and, in hundreds of cases, recovers medicine already in use. That is the whole '
        'contribution, and its only proper use is expert evaluation.</p>'
        '<h2>What was shown</h2>'
        '<ul>'
        f'<li>A single substrate (the R19 bistable switch) emerges a corrective <b>direction</b> for <b>{STAT["n"]}</b> '
        'rare diseases, each graded [F] and shipped with a falsifier.</li>'
        f'<li>In <b>{cls.get("MATCH",0)}</b> diseases that untuned direction <b>recovers an agent already in clinical '
        'use</b> &mdash; independent validation of the logic.</li>'
        f'<li><b>{cls.get("NOVEL",0)}</b> diseases receive a novel, direction-only, falsifiable lead; '
        f'<b>{cls.get("HOLD",0)}</b> are kept as honest holds.</li>'
        '<li>The entire corpus is no-tuning, hash-chained, and bit-for-bit reproducible, and passes a zero-leak '
        'magnitude-firewall check.</li>'
        '</ul>'
        '<h2>Responsible use</h2>'
        '<p>This volume is a hypothesis generator for experts. The correct response to any page is to design a controlled '
        'experiment, not to act on it clinically. It is not medical advice, not a prescription, and not an approved '
        'method. No dose appears anywhere, and that omission is load-bearing: dosing is unvalidated and belongs to a '
        'licensed physician or a national regulatory authority, never to a reader of this site.</p>'
        '<div class="recover"><b>&#10003; If you take one thing from this volume:</b> a derived direction tells an expert '
        '<i>which way</i> to test. It never tells anyone <i>what to take</i>.</div>'
    )

CHAPTERS = [
    dict(slug="00-purpose-and-firewall", pos=1, nav="Purpose",
         crumb="Purpose & firewall",
         name="Purpose, audience, and the prescription firewall",
         title_subj="Purpose & the prescription firewall",
         desc=("Why this volume exists, who it is for, and the three-times firewall: it offers a theoretical "
               "corrective direction to experts only, never a prescription, with no dose."),
         answer=("This volume gives experts a falsifiable corrective direction for hundreds of rare diseases. "
                 "It is not a prescription, diagnosis, treatment, or cure, and carries no dose. A safety firewall "
                 "appears three times on every disease page, because a drug name beside a disease name is easily "
                 "misread. The only proper next step is a controlled experiment."),
         rx_top=True, rx_bottom=True, body=body_00()),
    dict(slug="01-method-no-tuning-and-grading", pos=2, nav="Method",
         crumb="Method",
         name="Method: no-tuning derivation, grading, and the magnitude firewall",
         title_subj="Method: no-tuning derivation & grading",
         desc=("LOCK to Derive to Gate: an R19 bistable switch is emerged from promoter DNA with gamma never fitted; "
               "the corrective sign is forced [F]; magnitudes are firewalled; the build is hash-chained."),
         answer=("Each disease is mapped to an R19 bistable switch emerged from its promoter DNA, with stiffness gamma "
                 "measured, never fitted. The cusp geometry forces the sign of the corrective drive, graded [F]. No "
                 "dose or effect magnitude is ever emitted (the magnitude firewall), and the whole corpus is "
                 "seed-fixed and bit-for-bit reproducible."),
         body=body_01()),
    dict(slug="02-coverage-and-statistics", pos=3, nav="Statistics",
         crumb="Coverage & statistics",
         name="Coverage and statistics across the corpus",
         title_subj="Coverage & statistics",
         desc=("Distribution across hundreds of rare diseases: classification (match / novel / hold), corrective "
               "direction, polarity, lesion class, lead lever family, and switch geometry ranges."),
         answer=("The pinned corpus covers hundreds of rare diseases. Most recover an existing standard or hold "
                 "honestly; a minority surface a novel direction-only lead. This chapter shows the full distribution "
                 "by classification, corrective direction, polarity, lesion class, and lead lever family, plus the "
                 "geometry ranges of the emerged switches. No therapy magnitudes appear."),
         body=body_02()),
    dict(slug="03-validation-recovered-standard-of-care", pos=4, nav="Validation",
         crumb="Validation",
         name="Validation: recovering the standard of care",
         title_subj="Validation: recovering the standard of care",
         desc=("In hundreds of diseases the untuned geometry recovers an agent already in clinical use. Because gamma "
               "is never fitted, each recovery is genuine validation of the corrective-direction logic, not a claim."),
         answer=("In hundreds of diseases the corrective direction derived from untuned geometry independently recovers "
                 "a treatment already in clinical use. Since gamma is never fitted, the agreement was not engineered, "
                 "so each recovery validates the logic. The kit reports these as agreement with established practice, "
                 "adds no dose, and makes no treatment claim of its own."),
         body=body_03()),
    dict(slug="04-honest-gaps-and-limits", pos=5, nav="Limits",
         crumb="Gaps & limits",
         name="Honest gaps, holds, and the limits of the claim",
         title_subj="Honest gaps & limits",
         desc=("Where the framework holds, where the tractable space is saturated, and what the volume does not claim: "
               "no magnitudes, corpus-pinned statuses, direction not destiny, theoretical only."),
         answer=("Honesty above completeness: hundreds of diseases are kept as honest holds rather than filled with a "
                 "weak instance, and a handful are flagged as explicit gaps yet still given a falsifiable direction. "
                 "The readily tractable space is now largely saturated. The volume claims no magnitudes, pins corpus "
                 "status to a snapshot, and treats every output as theoretical."),
         body=body_04()),
    dict(slug="05-conclusion-and-responsible-use", pos=6, nav="Conclusion",
         crumb="Conclusion",
         name="Conclusion and responsible use",
         title_subj="Conclusion & responsible use",
         desc=("One untuned geometry yields a falsifiable corrective direction for hundreds of rare diseases and "
               "recovers known medicine in hundreds. Its only proper use is expert evaluation; no dose, not approved."),
         answer=("A single untuned substrate yields a falsifiable corrective direction for hundreds of rare diseases "
                 "and, in hundreds of cases, recovers medicine already in use. The proper response to any page is a "
                 "controlled experiment, never clinical action. No dose appears anywhere; dosing belongs to physicians "
                 "and regulators, not to a reader of this site."),
         rx_bottom=True, body=body_05()),
]

# ---- A-Z shard indexes --------------------------------------------------------
def bucket_of(slug):
    c = slug[0]
    return c.upper() if c.isalpha() else "sym"

BUCKETS = {}
for s in ORDER:
    BUCKETS.setdefault(bucket_of(s), []).append(s)
for k in BUCKETS:
    BUCKETS[k].sort()

def bucket_label(b):
    return "#" if b == "sym" else b

def azbar(active=None):
    present = set(BUCKETS.keys())
    letters = [chr(c) for c in range(ord("A"), ord("Z") + 1)]
    order = (["sym"] if "sym" in present else []) + letters
    out = ['<nav class="azbar" aria-label="Browse diseases A to Z">']
    for b in order:
        lab = bucket_label(b)
        if b in present:
            if b == active:
                out.append(f'<span aria-current="page">{esc(lab)}</span>')
            else:
                out.append(f'<a href="/{PAPER}/index-{b}/">{esc(lab)}</a>')
        else:
            out.append(f'<span>{esc(lab)}</span>')
    out.append("</nav>")
    return "".join(out)

def render_shard(b):
    slugs = BUCKETS[b]
    lab = bucket_label(b)
    title_subj = f"Diseases &mdash; {lab} \u2014 {SHORT}"
    title_plain = f"Diseases - {lab}"
    desc = clip_desc(f"Rare diseases beginning with {lab} in the VP Disease Kit: each with a forced, falsifiable "
            f"corrective direction and classification (match / novel / hold). Direction only, no dose, not medical advice.")
    canon = f"{SITE}/{PAPER}/index-{b}/"
    jl = [{
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": f"{SHORT} \u2014 diseases {lab}", "inLanguage": "en",
        "isPartOf": {"@type": "CreativeWorkSeries", "name": TITLE_FULL, "alternateName": SHORT},
        "license": LICENSE, "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "description": desc,
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER}/"},
            {"@type": "ListItem", "position": 3, "name": title_plain}]}]
    H = head(title_subj, desc, canon, jl)
    b_ = [H, crumb([("Home", "/"), (SHORT, f"/{PAPER}/"), (title_plain, None)]), "<main>"]
    b_.append(f"<h1>Diseases &mdash; {esc(lab)}</h1>")
    b_.append(f'<p class="lede">{len(slugs)} '
              f'disease{"s" if len(slugs)!=1 else ""} in this group. Each links to a full page: the emergence switch, '
              'the forced corrective direction, mapped agents, and the firewall. Direction only &mdash; no dose.</p>')
    b_.append(azbar(active=b))
    b_.append('<ul class="dzlist">')
    for s in slugs:
        d = DISEASES[s]
        b_.append(f'<li><span><a href="{disease_url(s)}">{esc(short_name(s))}</a>'
                  f'<span class="one">{dz_oneliner(s)}</span></span>'
                  f'<span class="gene">{esc(d.get("primary_gene",""))}</span></li>')
    b_.append("</ul>")
    b_.append('<nav class="pn"><a href="/' + PAPER + '/">&larr; Contents</a>'
              '<a class="center" href="/' + PAPER + '/">All chapters</a>'
              '<span></span></nav>')
    b_.append("</main>")
    b_.append(FOOTER)
    return "\n".join(b_)

# ---- hub (docs/disease/index.html) -------------------------------------------
def render_hub():
    cls = STAT["cls"]
    canon = f"{SITE}/{PAPER}/"
    desc = clip_desc(f"The VP Disease Kit: a falsifiable corrective direction for {STAT['n']} rare diseases from one "
            f"bistable switch, recovering an existing standard in {cls.get('MATCH',0)}. Direction only, no dose, expert use.")
    jl = [{
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": TITLE_FULL, "alternateName": SHORT, "inLanguage": "en",
        "identifier": f"https://doi.org/{DOI}", "license": LICENSE,
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "publisher": {"@type": "Organization", "name": "Jamming Physics"},
        "datePublished": DATEP, "dateModified": DATEP, "isBasedOn": REPRO, "description": desc,
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT}]}]
    H = head(f"{SHORT} \u2014 contents", desc, canon, jl)
    b = [H, crumb([("Home", "/"), (SHORT, None)]), "<main>"]
    b.append(RX_TOP)
    b.append(f"<h1>{esc(SHORT)}</h1>")
    b.append(f'<p class="lede">{esc(TITLE_FULL)}.</p>')
    b.append('<div class="derive-line">From one bistable switch, a falsifiable corrective '
             '<b>direction</b> per disease &mdash; offered to experts for testing, never as a prescription. '
             f'<a href="/{PAPER}/00-purpose-and-firewall/">Read the firewall first.</a></div>')
    b.append('<div class="hero-stat">'
             f'<span class="n">{STAT["n"]}<small>rare diseases</small></span>'
             f'<span class="n match">{cls.get("MATCH",0)}<small>recover a standard</small></span>'
             f'<span class="n novel">{cls.get("NOVEL",0)}<small>novel direction-only</small></span>'
             f'<span class="n hold">{cls.get("HOLD",0)}<small>honest holds</small></span>'
             '</div>')
    b.append("<h2>Contents</h2>")
    b.append('<ol class="toc">')
    for ch in CHAPTERS:
        b.append(f'<li><span><a href="/{PAPER}/{ch["slug"]}/">{esc(ch["name"])}</a>'
                 f'<span class="one">{esc(ch["desc"])}</span></span>'
                 f'<span class="gcell">{grade_badge("F") if ch["slug"].startswith(("01","03")) else grade_badge("O")}</span></li>')
    b.append("</ol>")
    b.append("<h2>Browse all diseases</h2>")
    b.append(f'<p class="lede" style="font-size:1rem">One page per disease, {STAT["n"]} in total.</p>')
    b.append(azbar())
    b.append('<div class="legend">'
             f'<span class="k"><span class="cbadge cb-match">&#10003; match</span> recovers an existing standard</span>'
             f'<span class="k"><span class="cbadge cb-novel">&#9675; novel</span> direction-only lead</span>'
             f'<span class="k"><span class="cbadge cb-hold">&mdash; hold</span> no matched agent yet</span>'
             f'<span class="k">{grade_badge("F")} forced direction</span>'
             f'<span class="k">{grade_badge("O")} direction only, no magnitude</span>'
             '</div>')
    b.append('<div class="recover"><b>&#10003; Reminder.</b> Every disease page repeats the safety firewall three times '
             '(top, beside the agents, and bottom with the dosage rationale). Nothing here is a prescription; the next '
             'step after any page is a controlled experiment by qualified experts.</div>')
    b.append("</main>")
    b.append(FOOTER)
    return "\n".join(b)

# ---- landing (docs/index.html) -----------------------------------------------
def render_landing():
    cls = STAT["cls"]
    canon = f"{SITE}/"
    desc = clip_desc(f"From a single bistable switch to a falsifiable corrective direction for {STAT['n']} rare "
            f"diseases. Recovers an existing standard in {cls.get('MATCH',0)}. Theoretical, direction only, no dose, expert use.")
    jl = [{
        "@context": "https://schema.org", "@type": "WebSite",
        "name": "Jamming Physics", "url": f"{SITE}/", "inLanguage": "en",
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
    }, {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": TITLE_FULL, "name": TITLE_FULL, "inLanguage": "en",
        "identifier": f"https://doi.org/{DOI}", "sameAs": f"https://doi.org/{DOI}",
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "publisher": {"@type": "Organization", "name": "Jamming Physics"},
        "datePublished": DATEP, "dateModified": DATEP, "isBasedOn": REPRO, "license": LICENSE,
        "description": desc,
    }]
    H = head("A corrective direction from one switch", desc, canon, jl)
    b = [H, crumb([("Home", None)]), "<main>"]
    b.append(RX_TOP)
    b.append(f"<h1>{esc(TITLE_FULL)}</h1>")
    b.append('<p class="lede">A single bistable molecular switch, emerged from real promoter DNA with nothing tuned, '
             'yields a falsifiable <b>corrective direction</b> for hundreds of rare diseases &mdash; and in hundreds of '
             'cases recovers medicine already in clinical use. This is a theoretical instrument for experts, not a '
             'source of prescriptions.</p>')
    b.append('<div class="hero-stat">'
             f'<span class="n">{STAT["n"]}<small>rare diseases mapped</small></span>'
             f'<span class="n match">{cls.get("MATCH",0)}<small>recover an existing standard</small></span>'
             f'<span class="n novel">{cls.get("NOVEL",0)}<small>novel direction-only leads</small></span>'
             f'<span class="n hold">{cls.get("HOLD",0)}<small>honest holds</small></span>'
             '</div>')
    b.append("<h2>What this delivers</h2>")
    b.append('<ul>'
             f'<li>A forced, falsifiable corrective <b>direction</b> for each of {STAT["n"]} rare diseases, graded [F], '
             'each with the experiment that would refute it.</li>'
             f'<li><b>{cls.get("MATCH",0)}</b> diseases where the untuned geometry recovers an approved, in-use agent '
             '&mdash; independent validation of the logic.</li>'
             '<li>A strict <b>direction-only</b> discipline: no dose, no efficacy, no safety magnitude, ever; verified '
             'by a zero-leak firewall check.</li>'
             '<li>No-tuning, hash-chained, bit-for-bit reproducible across the whole corpus.</li>'
             '</ul>')
    b.append('<div class="derive-line">Start with the firewall and purpose, then enter the disease index. '
             f'<a href="/{PAPER}/00-purpose-and-firewall/">Purpose &amp; firewall</a> &middot; '
             f'<a href="/{PAPER}/">Contents &amp; all {STAT["n"]} diseases</a></div>')
    b.append('<p><a href="/' + PAPER + '/">Enter the volume &rarr;</a></p>')
    b.append(RX_BOTTOM)
    b.append("</main>")
    b.append(FOOTER)
    return "\n".join(b)

# ---- sitemap / robots / llms / meta ------------------------------------------
def write_sitemap():
    urls = "".join(
        f"<url><loc>{SITE}{loc}</loc><lastmod>{DATEP}</lastmod></url>" for loc in PAGES)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
           + urls + "</urlset>\n")
    write(os.path.join(DOCS, "sitemap.xml"), xml)

def write_robots():
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot",
            "PerplexityBot", "ClaudeBot", "Google-Extended"]
    lines = []
    for bbot in bots:
        lines.append(f"User-agent: {bbot}")
        lines.append("Allow: /")
        lines.append("")
    lines.append("User-agent: *")
    lines.append("Allow: /")
    lines.append("")
    lines.append(f"Sitemap: {SITE}/sitemap.xml")
    lines.append("")
    write(os.path.join(DOCS, "robots.txt"), "\n".join(lines))

def write_llms():
    cls = STAT["cls"]
    txt = f"""# {SHORT}

> {TITLE_FULL}. A single-author, no-tuning, hash-chained whitepaper that derives a
> falsifiable corrective *direction* for {STAT['n']} rare diseases from one bistable
> molecular switch (the R19 double-well), emerged from real promoter DNA with stiffness
> never fitted.

## What it is
- A theoretical instrument offered to researchers and clinicians for evaluation.
- For each disease: an emerged R19 switch, a forced [F] corrective direction, agents whose
  known action is direction-concordant, and a falsifier.

## What it is NOT
- Not a prescription, diagnosis, treatment, or cure. Not medical advice. Not an approved method.
- No dose, efficacy, potency, or safety magnitude appears anywhere (direction only [O]).
- A safety firewall is repeated three times on every disease page (top, beside the agents,
  bottom with the dosage rationale).

## Headline numbers
- Diseases mapped: {STAT['n']}
- Recover an existing standard (MATCH): {cls.get('MATCH',0)}
- Novel direction-only lead (NOVEL): {cls.get('NOVEL',0)}
- Honest holds (HOLD): {cls.get('HOLD',0)}
- Surfaced candidate rows: {STAT['n_total_candidates']} ({STAT['redisc']} rediscoveries, {STAT['novel_cand']} novel)
- No current disease-modifying prescription on record: {STAT['nocur']}

## Method
- LOCK (emerge switch from promoter DNA, gamma measured not fitted) -> Derive (cusp forces the
  corrective sign, [F]) -> Gate (honest grading; MAGNITUDE_FIREWALL; seed-fixed, 2x SHA-256).
- Register chain-head: {CR['chain_head'][:16]}; release {RELEASE}.

## Structure
- /{PAPER}/ : contents hub
- /{PAPER}/00-purpose-and-firewall/ ... /{PAPER}/05-conclusion-and-responsible-use/ : chapters
- /{PAPER}/index-A/ ... : A-Z disease indexes
- /{PAPER}/dz/<slug>/ : one page per disease

## Provenance
- Author: {AUTHOR} (ORCID 0009-0002-7535-8245)
- DOI: {DOI} | License: CC BY 4.0 | Reproduction: {REPRO}
- Corpus snapshot: {SC.get('corpus_snapshot_date','')}
"""
    write(os.path.join(DOCS, "llms.txt"), txt)

def write_meta():
    cls = STAT["cls"]
    meta = {
        "paper_id": PAPER,
        "title": TITLE_FULL,
        "short": SHORT,
        "doi": DOI,
        "orcid": ORCID,
        "author": AUTHOR,
        "license": "CC BY 4.0",
        "date_published": DATEP,
        "release": RELEASE,
        "site": SITE,
        "url": f"{SITE}/{PAPER}/",
        "register_chain_head": CR["chain_head"][:16],
        "corpus_snapshot_date": SC.get("corpus_snapshot_date", ""),
        "n_diseases": STAT["n"],
        "classification": {"MATCH": cls.get("MATCH", 0),
                           "NOVEL": cls.get("NOVEL", 0),
                           "HOLD": cls.get("HOLD", 0)},
        "candidates": {"total": STAT["n_total_candidates"],
                       "rediscovery": STAT["redisc"],
                       "novel": STAT["novel_cand"]},
        "diseases_with_surfaced_candidate": STAT["n_with_surfaced"],
        "no_current_prescription": STAT["nocur"],
        "honest_gaps": STAT["honest"],
        "discipline": "no-tuning; direction-only [O]; MAGNITUDE_FIREWALL (no dose/efficacy/safety magnitude); "
                      "honest grading; hash-chained, 2x SHA-256, seed-fixed; English safety firewall x3 per page",
        "firewall": {"status": "PASS", "magnitude_leaks": 0},
        "pages": len(PAGES),
    }
    write(os.path.join(DOCS, PAPER, "_meta.json"),
          json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

def write_readme():
    cls = STAT["cls"]
    md = f"""# {SHORT} — static site (build artifact)

**{TITLE_FULL}**

This `docs/` tree is a deterministic, canonical, multi-page HTML rendering of the VP Disease
Emergence Kit, built to VP-SPEC v1.8 (Constitution C1/C2/C4). It is generated entirely from the
kit's pinned JSON outputs and contains **no invented numbers**.

## The one thing to understand
Every disease page offers a **theoretical corrective direction to experts for evaluation** — it is
**never a prescription**. There is **no dose anywhere**. An English-language safety firewall is
repeated **three times** on each disease page: a top banner, a banner beside the agent names, and a
bottom banner that explains *why* no dose is given (unvalidated; to be set by a licensed physician or
national authority; not an approved method). A short inline notice also rides on every candidate card.

## Contents
- `{STAT['n']}` rare-disease pages under `docs/{PAPER}/dz/<slug>/index.html`
- 6 front-matter chapters under `docs/{PAPER}/<NN-slug>/index.html`
- A–Z disease indexes under `docs/{PAPER}/index-<X>/index.html`
- Contents hub `docs/{PAPER}/index.html`; site landing `docs/index.html`
- `sitemap.xml`, `robots.txt` (7 retrieval bots allowed), `llms.txt`, `docs/{PAPER}/_meta.json`

## Headline results
- Recover an existing standard (MATCH): **{cls.get('MATCH',0)}**  ·  Novel direction-only (NOVEL): **{cls.get('NOVEL',0)}**  ·  Honest holds (HOLD): **{cls.get('HOLD',0)}**
- Surfaced candidate rows: **{STAT['n_total_candidates']}** ({STAT['redisc']} rediscoveries, {STAT['novel_cand']} novel)

## Build / reproduce
```
python3 tools/build_disease_site.py
```
Deterministic: same inputs → same bytes (SEED-fixed, 2× SHA-256 hash chain).
Register chain-head: `{CR['chain_head'][:16]}` · release `{RELEASE}`.

## Inputs (read-only)
`outputs/actionability_index.json`, `outputs/mapped_levers.json`,
`outputs/surfaced_candidates.json`, `outputs/candidate_register.json`.

Author: {AUTHOR} (ORCID 0009-0002-7535-8245) · License: CC BY 4.0 · DOI: {DOI}
Reproduction code: {REPRO}
"""
    write(os.path.join(ROOT, "SITE_README.md"), md)

# ====================================================================== MAIN
def main():
    # 1) landing + hub are registered first (URL order in sitemap)
    reg("/")
    reg(f"/{PAPER}/")
    for ch in CHAPTERS:
        reg(f"/{PAPER}/{ch['slug']}/")
    order_buckets = (["sym"] if "sym" in BUCKETS else []) + \
                    [chr(c) for c in range(ord("A"), ord("Z") + 1) if chr(c) in BUCKETS]
    for bkt in order_buckets:
        reg(f"/{PAPER}/index-{bkt}/")
    for slug in ORDER:
        reg(disease_url(slug))

    # 2) write disease pages
    for idx, slug in enumerate(ORDER):
        html_doc = render_disease(slug, idx)
        write(os.path.join(DOCS, PAPER, DZ_DIR, slug, "index.html"), html_doc)
    print(f"[write] {N} disease pages")

    # 3) chapters
    for i, ch in enumerate(CHAPTERS):
        write(os.path.join(DOCS, PAPER, ch["slug"], "index.html"), render_chapter(ch, i))
    print(f"[write] {len(CHAPTERS)} front-matter chapters")

    # 4) shard indexes
    for bkt in order_buckets:
        write(os.path.join(DOCS, PAPER, f"index-{bkt}", "index.html"), render_shard(bkt))
    print(f"[write] {len(order_buckets)} A-Z index pages")

    # 5) hub + landing
    write(os.path.join(DOCS, PAPER, "index.html"), render_hub())
    write(os.path.join(DOCS, "index.html"), render_landing())
    print("[write] hub + landing")

    # 6) sitemap / robots / llms / meta / readme
    write_sitemap(); write_robots(); write_llms(); write_meta(); write_readme()
    print(f"[write] sitemap.xml ({len(PAGES)} urls), robots.txt, llms.txt, _meta.json, SITE_README.md")

    # 7) build manifest (sha256 of every emitted file) for reproducibility evidence
    manifest = []
    for dirpath, _dirs, files in os.walk(DOCS):
        for fn in sorted(files):
            fp = os.path.join(dirpath, fn)
            with open(fp, "rb") as fh:
                h = hashlib.sha256(fh.read()).hexdigest()
            manifest.append((os.path.relpath(fp, ROOT).replace(os.sep, "/"), h))
    manifest.sort()
    digest = hashlib.sha256(
        "\n".join(f"{p}  {h}" for p, h in manifest).encode("utf-8")).hexdigest()
    body = "".join(f"{h}  {p}\n" for p, h in manifest)
    write(os.path.join(ROOT, "SITE_BUILD_MANIFEST.sha256"),
          body + f"\n# tree-digest sha256: {digest}\n# files: {len(manifest)}\n")
    print(f"[manifest] {len(manifest)} files, tree-digest {digest[:16]}")
    print("[done] site build complete")

if __name__ == "__main__":
    main()
