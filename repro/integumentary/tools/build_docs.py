#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Integumentary WRITING phase: per-title canonical SEO HTML generator.
HARD RULE: refuses while gates.writing_locked() is True (research signed off + PHASE=="writing").
WHEN UNLOCKED, follows VP-SPEC v1.8 (../VP_SPEC_v1_8.md): canonical HTML in docs/ (C2); ONE page per
title/section (C4 sec 6): answer-first <p class="answer"> 40-60 words, self-contained, JSON-LD
ScholarlyArticle + BreadcrumbList, canonical link, claim-strip (grade+repro+DOI), vp-card per cited
locked quantity; ENGLISH body (C0); honest grades + stated obstacles for [O] (C3); deterministic
numbers from the engine (C1). Output: docs/<slug>/index.html + hub + _meta.json + sitemap + robots + llms.
"""
import os, sys, json, html

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, os.path.join(_ROOT, "repro", "_verify"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_engine"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_oncology"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_pathology"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_cycle"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_seb"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_adhesion"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_vasomotor"))
sys.path.insert(0, os.path.join(_ROOT, "repro", "_seam"))
import importlib
gates = importlib.import_module("gates")

# --------------------------------------------------------------------------- identity / constants
AUTHOR = "Young Jae Lee"
ORCID = "0009-0002-7535-8245"
SITE = "https://jamming-physics.org/integumentary"
REPO = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/integumentary"
BUILD_DATE = "2026-06-19"            # fixed -> reproducible HTML (C1)
PROJECT = "VP Theory -- Jammed-Granular-Vacuum Emergence"


def _version():
    try:
        return open(os.path.join(_ROOT, "VERSION"), encoding="utf-8").read().strip()
    except Exception:
        return "0.1.0-research"


def gather():
    """Pull every displayed number from the engine/oncology/pathology (C1: HTML mirrors the engine)."""
    eng = importlib.import_module("vp_skn_engine")
    dyn = importlib.import_module("skn_dynamics")
    onco = importlib.import_module("carcinogen_dose_response")
    patho = importlib.import_module("skin_pathology")
    cyc = importlib.import_module("hair_cycle")
    seb = importlib.import_module("sebaceous_duct")
    adh = importlib.import_module("adhesion_switch")
    vaso = importlib.import_module("vasomotor_switch")
    seam = importlib.import_module("seam_manifest")
    from vp_substrate import spinodal, barrier
    res = eng.circulate()
    _, sha = eng.emit(res)
    g = {m: round(dyn.gamma_of(m), 4) for m in ("TP63", "KRT14", "MITF", "EDAR")}
    sp = {m: round(spinodal(dyn.gamma_of(m)), 4) for m in ("TP63", "KRT14", "MITF", "EDAR")}
    psum = patho.pathology_summary()
    _, patho_sha = patho._emit(psum)            # pathology's OWN 2xsha256 (separate from core battery)
    csum = cyc.hair_cycle_summary()
    _, cyc_sha = cyc._emit(csum)                 # hair-cycle's OWN 2xsha256 (separate from core + pathology)
    ssum = seb.sebaceous_summary()
    _, seb_sha = seb._emit(ssum)                 # sebaceous-duct's OWN 2xsha256 (separate from core/pathology/cycle)
    asum = adh.adhesion_summary()
    _, adh_sha = adh._emit(asum)                 # adhesion's OWN 2xsha256 (separate from core/pathology/cycle/seb)
    vsum = vaso.vasomotor_summary()
    _, vaso_sha = vaso._emit(vsum)               # vasomotor's OWN 2xsha256 (separate from core/pathology/cycle/seb/adhesion)
    seamm = seam.seam_manifest()
    _, seam_sha = seam._emit(seamm)              # seam manifest's OWN 2xsha256 (separate from core + every disease layer)
    return dict(sha=sha, gamma=g, spinodal=sp,
                order=res["organs"]["gamma_order_ascending"], dyn=res["dynamics"],
                onco=onco.discriminant(), K=onco.MULTISTAGE_K, qstar=onco and dyn and 3.81,
                patho=psum, patho_sha=patho_sha, cyc=csum, cyc_sha=cyc_sha,
                seb=ssum, seb_sha=seb_sha, adh=asum, adh_sha=adh_sha, vaso=vsum, vaso_sha=vaso_sha,
                seam=seamm, seam_sha=seam_sha)


# --------------------------------------------------------------------------- HTML helpers
def esc(s):
    return html.escape(str(s), quote=True)

GRADE_CLASS = {"V": "g-verified", "F": "g-forced", "O": "g-open", "H": "g-hypothesis", "L": "g-open"}
GRADE_WORD = {"V": "Simulation-verified", "F": "Forced (substrate)", "O": "Open (obstacle stated)", "H": "Hypothesis", "L": "Cited anchor"}

def grade_badge(letter):
    return f'<span class="grade {GRADE_CLASS[letter]}">[{letter}] {GRADE_WORD[letter]}</span>'

def vp_card(title, body_html):
    return f'<aside class="vp-card"><b>{esc(title)}</b><br>{body_html}</aside>'

def claim_strip(slug, grades, doi_note="DOI: pending (research preview)"):
    badges = " ".join(grade_badge(x) for x in grades)
    repro = f'<a href="{REPO}/{slug}/" rel="nofollow">repro &#8599;</a>'
    return ('<aside class="claim-strip">' + badges +
            '<span class="gate">LOCK &rarr; Derive &rarr; Gate</span>' +
            repro + f'<span class="tag">{esc(doi_note)}</span></aside>')

def jsonld(section, slug, abstract):
    url = f"{SITE}/{slug}/"
    article = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": section["title"], "name": section["title"],
        "abstract": abstract, "inLanguage": "en", "isAccessibleForFree": True,
        "author": {"@type": "Person", "name": AUTHOR,
                   "identifier": f"https://orcid.org/{ORCID}", "url": f"https://orcid.org/{ORCID}"},
        "isPartOf": {"@type": "CreativeWorkSeries", "name": PROJECT, "url": SITE},
        "datePublished": BUILD_DATE, "dateModified": BUILD_DATE,
        "version": _version(), "url": url, "mainEntityOfPage": url,
        "keywords": ", ".join(section["keywords"]),
        "isBasedOn": f"{REPO}/{slug}/",
        "publisher": {"@type": "Organization", "name": "jamming-physics.org", "url": "https://jamming-physics.org"},
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "VP Theory", "item": "https://jamming-physics.org"},
            {"@type": "ListItem", "position": 2, "name": "Integumentary", "item": SITE + "/"},
            {"@type": "ListItem", "position": 3, "name": section["short"], "item": url},
        ],
    }
    return ('<script type="application/ld+json">' + json.dumps(article, ensure_ascii=False) + '</script>\n'
            '<script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False) + '</script>')

def page(section, slug, prev_s, next_s):
    abstract_txt = section["abstract_txt"]
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(section['title'])} &middot; Integumentary VP</title>
<meta name="description" content="{esc(abstract_txt)}">
<meta name="author" content="{esc(AUTHOR)}">
<meta name="keywords" content="{esc(', '.join(section['keywords']))}">
<link rel="canonical" href="{SITE}/{slug}/">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(section['title'])}">
<meta property="og:description" content="{esc(abstract_txt)}">
<meta property="og:url" content="{SITE}/{slug}/">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="stylesheet" href="../assets/css/site.css">
{jsonld(section, slug, abstract_txt)}
</head>
<body>
<header>
<nav class="crumb"><a href="https://jamming-physics.org">VP Theory</a> &rsaquo; <a href="../">Integumentary</a> &rsaquo; <span>{esc(section['short'])}</span></nav>
<h1>{esc(section['h1'])}</h1>
</header>
<main>
<p class="answer">{section['answer']}</p>
{claim_strip(slug, section['grades'])}
<p class="abstract">{section['abstract']}</p>
{section['body']}
"""
    pn = '<nav class="pn">'
    pn += (f'<a href="../{prev_s[0]}/">&larr; {esc(prev_s[1])}</a>' if prev_s else '<span></span>')
    pn += (f'<a href="../{next_s[0]}/">{esc(next_s[1])} &rarr;</a>' if next_s else '<span></span>')
    pn += '</nav>'
    foot = f"""{pn}
</main>
<footer>
<p>{esc(PROJECT)} &middot; author <a href="https://orcid.org/{ORCID}">{esc(AUTHOR)}</a> (ORCID {ORCID}) &middot; version {esc(_version())} &middot; build {BUILD_DATE}.</p>
<p class="small">Reproducible from the R19 jammed-granular-vacuum substrate and measured master-gene &gamma;. No constant is fitted to a target: each is a measured input (cited, locked) or substrate-derived. Grades: [F] forced &middot; [V] simulation-verified &middot; [L] cited anchor &middot; [O] open (obstacle stated). Result SHA-256 <code>{esc(SHA8)}</code>.</p>
</footer>
</body>
</html>"""
    return head + foot


# --------------------------------------------------------------------------- content (English bodies)
def build_sections(D):
    g, sp, dy, onc = D["gamma"], D["spinodal"], D["dyn"], D["onco"]
    T1, T2, T3, T4, T5 = dy["T1"], dy["T2"], dy["T3"], dy["T4"], dy["T5"]

    S = []

    # ---- 01 emergence ----
    body = f"""
<h2>The body boundary as an emergent organ set</h2>
<p>The integumentary system is the organism's interface with the world: a barrier that holds water in, a screen that holds ultraviolet out, a sensor sheet, and a thermostat. In this framework it is not designed; it <em>emerges</em> when a small set of master genes switch on the shared bistable substrate.</p>
<p>Each organ rides the same vendored switch, the R19 bistable element <code>ds/dt = g&middot;s &minus; s&sup3; + h</code>, whose control parameter <code>g</code> is the measured master-gene &gamma; taken read-only from the DNA gene-clock. Identity and developmental order follow from those measured numbers; nothing here is tuned to a skin phenotype.</p>
<table>
<thead><tr><th>Organ</th><th>Master gene</th><th>&gamma; (measured)</th><th>Spinodal</th><th>Role class</th></tr></thead>
<tbody>
<tr><td>Epidermis</td><td>TP63</td><td class="num">{g['TP63']}</td><td class="num">{sp['TP63']}</td><td>barrier</td></tr>
<tr><td>Keratinocyte</td><td>KRT14</td><td class="num">{g['KRT14']}</td><td class="num">{sp['KRT14']}</td><td>barrier</td></tr>
<tr><td>Melanocyte</td><td>MITF</td><td class="num">{g['MITF']}</td><td class="num">{sp['MITF']}</td><td>defense</td></tr>
<tr><td>Skin appendage</td><td>EDAR</td><td class="num">{g['EDAR']}</td><td class="num">{sp['EDAR']}</td><td>appendage</td></tr>
</tbody></table>
{vp_card("Measured master-gene &gamma; (locked input)", "The four &gamma; values are measured and carried read-only from the DNA gene-clock package &mdash; never fitted here. They set both the switch stiffness and, through the substrate, the spinodal threshold at which each organ's state flips discontinuously.")}
<h2>Developmental order is read off &gamma;</h2>
<p>Ordering the organs by ascending &gamma; gives the substrate's prediction for the sequence in which they consolidate: <strong>{esc(' &rarr; '.join(D['order']))}</strong>. The epidermal field commits first, appendages and melanocytes follow, and the stiff keratinocyte programme last.</p>
<p>This ordering is a falsifiable consequence of the measured &gamma;, not an input. The remaining pages put each organ under a wide stress sweep &mdash; barrier, wound, pigment, turnover, sweat, and carcinogenesis &mdash; and grade what the substrate does and does not explain.</p>
"""
    S.append(dict(no="01", slug="01-integumentary-emergence-body-boundary",
                  short="Emergence", title="Integumentary emergence: the body boundary from measured master-gene &gamma;",
                  h1="Integumentary emergence: the body boundary from measured \u03b3",
                  keywords=["integumentary system", "skin emergence", "VP theory", "master gene", "TP63", "KRT14", "MITF", "EDAR", "jamming"],
                  grades=["V", "F"],
                  answer=("The integumentary system emerges as the body&rsquo;s boundary: four organs switch on from their measured master-gene &gamma; &mdash; "
                          f"epidermis (TP63, &gamma;={g['TP63']}), keratinocyte (KRT14, &gamma;={g['KRT14']}), melanocyte (MITF, &gamma;={g['MITF']}), and skin appendages (EDAR, &gamma;={g['EDAR']}). "
                          "Developmental order is read directly off &gamma;; identity is cited from the DNA gene-clock, never fitted."),
                  abstract_txt=("Four skin organs emerge from measured master-gene gamma on the shared R19 bistable substrate; developmental order follows from gamma ascending, with no tuning to any skin phenotype."),
                  abstract=("Four skin organs emerge from measured master-gene &gamma; on the shared R19 bistable substrate. "
                            f"Ordered by ascending &gamma; the predicted developmental sequence is {esc(' &rarr; '.join(D['order']))}, a consequence of the measured inputs rather than a fit."),
                  body=body))

    # ---- 02 barrier / TEWL (T1) ----
    body = f"""
<h2>Water loss is a Fickian flux through a living barrier</h2>
<p>The stratum corneum is a diffusion barrier; transepidermal water loss (TEWL) is the steady flux across it. For a barrier of <code>N</code> layers the flux scales as <code>1/N</code>, so thinning the barrier raises TEWL smoothly and monotonically.</p>
<p>On a {15}-layer reference barrier the flux crosses twice its baseline once thickness halves &mdash; here at <strong>{T1['thinning_crosses_2x_at_layers']} layers</strong>. This is the ordinary, graded failure mode: gradual barrier loss, gradual water-loss rise.</p>
<h2>Insult is different: a discontinuous collapse at the spinodal</h2>
<p>A chemical insult does not thin the barrier; it drives the keratinocyte switch field <code>h</code> toward its spinodal. The barrier integrity (the depth of the ON basin) is <strong>robust until the drive reaches the spinodal</strong> &mdash; up to a fraction of about {T1['insult_robust_until_frac']} of it &mdash; and then collapses discontinuously, TEWL jumping rather than drifting.</p>
<p>The absolute insult a layer can absorb before that snap scales as <code>&gamma;<sup>1.5</sup></code>, so the four organs rank in resistance as <strong>{esc(' &gt; '.join(T1['gamma1p5_tolerance_order']))}</strong>: the stiff keratinocyte tolerates the most, the epidermal field the least. The keratinocyte absolute tolerance here is {T1['abs_insult_tolerance']:.2f} (dimensionless drive units).</p>
{vp_card("Keratinocyte switch (KRT14)", f"&gamma;={g['KRT14']} (measured), spinodal={sp['KRT14']} (substrate-derived). The spinodal is where the barrier ON-state loses its basin and TEWL diverges &mdash; the physical line between a stressed-but-intact barrier and a breached one.")}
<h2>What is verified and what is open</h2>
<p>The two regimes &mdash; smooth threshold under thinning, discontinuous collapse under insult &mdash; and the &gamma;<sup>1.5</sup> resistance ordering are simulation-verified shapes {grade_badge('V')}. The conversion to an absolute clinical TEWL in g&middot;m<sup>&minus;2</sup>&middot;h<sup>&minus;1</sup> is open {grade_badge('O')}: it needs the stratum-corneum lipid permeability and the water activity gradient as cited inputs.</p>
"""
    S.append(dict(no="02", slug="02-epidermal-barrier-water-loss",
                  short="Barrier / TEWL", title="Epidermal barrier and transepidermal water loss: threshold and collapse",
                  h1="Epidermal barrier and water loss: a threshold that becomes a cliff",
                  keywords=["transepidermal water loss", "TEWL", "skin barrier", "stratum corneum", "spinodal", "barrier function"],
                  grades=["V", "O"],
                  answer=("Transepidermal water loss is a Fickian flux through the stratum-corneum barrier: it crosses twice baseline when thickness halves "
                          f"(here at {T1['thinning_crosses_2x_at_layers']} of 15 layers), then collapses discontinuously when a chemical insult drives the keratinocyte switch past its spinodal. "
                          "The absolute insult a layer tolerates scales as &gamma;<sup>1.5</sup>, so keratin is the most insult-resistant."),
                  abstract_txt=("TEWL rises smoothly as the barrier thins, crossing twice baseline at half thickness, then collapses discontinuously when an insult drives the keratinocyte switch past its spinodal; insult tolerance scales as gamma^1.5."),
                  abstract=("TEWL rises as <code>1/N</code> with barrier thickness, crossing twice baseline at half thickness, "
                            "then collapses discontinuously when an insult drives the keratinocyte switch past its spinodal. "
                            "Insult tolerance scales as &gamma;<sup>1.5</sup>, ranking keratinocyte highest."),
                  body=body))

    # ---- 03 wound healing (T2 flagship) ----
    body = f"""
<h2>A wound is an unjamming transition</h2>
<p>A confluent epithelial sheet is a <em>jammed</em> solid: cells are caged by neighbours and cannot rearrange. The tissue's jammed-vs-fluid state is set by a single geometric control, the cell shape index <code>q</code>, with a vertex-model threshold at <strong>q* = {T2['q_star']}</strong>: below it the sheet is jammed, above it it flows.</p>
<p>Injury frees an edge. The free-edge cue drives the edge cells across q*, <strong>unjamming</strong> them; in this run the shape index rises to <strong>q<sub>max</sub> = {T2['q_max']:.2f}</strong>, well into the fluid regime. The unjammed cells migrate collectively into the gap.</p>
{vp_card("Critical shape index q* = 3.81 (cited)", "The jamming/unjamming threshold of the 2D vertex model (Bi, Lopez, Schwarz &amp; Manning, 2015&ndash;2016). It is a cited geometric constant of confluent tissue, not a fitted parameter; wound re-epithelialisation is a living unjamming&ndash;rejamming cycle around it.")}
<h2>Closure is re-jamming</h2>
<p>As the gap closes the free-edge cue vanishes and the confluent crowding bias takes over, pushing the edge field back below the spinodal so the sheet <strong>re-jams</strong>: the shape index settles to <strong>q<sub>final</sub> = {T2['q_final']:.2f}</strong>, back below q*. The wound has closed and the tissue is solid again &mdash; a full unjam&rarr;migrate&rarr;rejam cycle.</p>
<h2>The honest failure mode: chronic wounds</h2>
<p>The same model predicts when healing <em>fails</em>. Below a critical unjamming drive of about <strong>{T2['chronic_wound_critical_drive']}</strong> the edge never crosses q*, the sheet stays jammed, and the gap does not close &mdash; the substrate's picture of a chronic, non-healing wound.</p>
<p>The jam&rarr;unjam&rarr;rejam sequence and the chronic-wound threshold are simulation-verified shapes {grade_badge('V')}; q* itself is a cited anchor {grade_badge('L')}. The absolute closure <em>rate</em> in &micro;m&middot;h<sup>&minus;1</sup> is open {grade_badge('O')}: it needs a measured single-cell migration speed.</p>
"""
    S.append(dict(no="03", slug="03-wound-healing-jamming-unjamming",
                  short="Wound healing", title="Wound healing as jamming, unjamming and re-jamming",
                  h1="Wound healing: unjamming, migration, and re-jamming",
                  keywords=["wound healing", "jamming transition", "unjamming", "shape index", "cell migration", "chronic wound", "re-epithelialisation"],
                  grades=["V", "L", "O"],
                  answer=("Wound healing is a jamming&rarr;unjamming&rarr;re-jamming transition. A free edge unjams (shape index q rises above the vertex-model threshold q*=3.81), "
                          "cells migrate collectively to close the gap, then confluence crowds the edge past the spinodal and the sheet re-jams (q falls below q*). "
                          f"Below a critical unjamming drive (~{T2['chronic_wound_critical_drive']}) the wound never closes &mdash; a chronic wound."),
                  abstract_txt=("Re-epithelialisation is modelled as an unjamming-rejamming cycle around the vertex-model shape index q*=3.81: a free edge unjams and migrates, confluence re-jams the sheet, and below a critical drive the wound fails to close."),
                  abstract=("Re-epithelialisation is an unjamming&ndash;rejamming cycle around the vertex-model shape index <strong>q* = {qs}</strong>. "
                            "The free edge unjams (q&uarr; to {qmax}), cells migrate, confluence re-jams the sheet (q&darr; to {qfin}); below a critical drive the wound fails to close."
                            ).format(qs=T2['q_star'], qmax=round(T2['q_max'],2), qfin=round(T2['q_final'],2)),
                  body=body))

    # ---- 04 melanin photoprotection (T3) ----
    body = f"""
<h2>Pigment is a feedback controller, not a dial</h2>
<p>Ultraviolet light drives the melanocyte master gene MITF, which makes melanin. Melanin then absorbs ultraviolet &mdash; including the ultraviolet that triggered it. Synthesis and screening therefore form a <strong>negative feedback</strong> loop: <code>h_eff = UV &middot; e<sup>&minus;k&middot;M</sup></code>.</p>
<p>The self-consistent steady melanin level is consequently <strong>concave</strong> in ultraviolet dose, rising toward a plateau rather than tracking the dose linearly. Across the swept range the melanin response flattens (the high-dose level is only about {T3['sublinear_ratio_hi_over_mid']:.2f}&times; the mid-dose level), the signature of a regulated quantity.</p>
<h2>The screen is real but partial</h2>
<p>The ultraviolet that actually reaches the DNA below is the screened flux <code>UV&middot;e<sup>&minus;k&middot;M</sup></code>. With the feedback active this is attenuated to about <strong>{int(round(T3['delivered_uv_attenuation']*100))}%</strong> of the incident dose at the top of the range &mdash; substantial photoprotection, but not total: extreme ultraviolet still gets through, which is why a tan is not sunscreen.</p>
<p>The control experiment removes the feedback (k&rarr;0). The delivered-ultraviolet attenuation then returns to {T3['control_no_feedback_attenuation']:.0f}&times; (no protection at all), identifying the melanin screening &mdash; not any synthesis cap &mdash; as the cause of the protection.</p>
{vp_card("Melanocyte switch (MITF)", f"&gamma;={g['MITF']} (measured), spinodal={sp['MITF']} (substrate-derived). MITF sets the gain of the UV&rarr;melanin response; the Beer&ndash;Lambert screening of the same UV closes a negative-feedback loop that makes the response self-limiting.")}
<h2>Grades</h2>
<p>The concave, plateauing melanin response, the partial attenuation of delivered ultraviolet, and the feedback-off control are simulation-verified shapes {grade_badge('V')}. The absolute minimal erythema dose and the melanin optical density are open {grade_badge('O')}: they need the melanin extinction coefficient as a cited input.</p>
"""
    S.append(dict(no="04", slug="04-melanin-photoprotection-uv",
                  short="Melanin / UV", title="Melanin photoprotection as ultraviolet negative feedback",
                  h1="Melanin photoprotection: a self-limiting ultraviolet screen",
                  keywords=["melanin", "photoprotection", "ultraviolet", "MITF", "negative feedback", "tanning", "Beer-Lambert"],
                  grades=["V", "O"],
                  answer=("Ultraviolet light drives MITF to make melanin, which screens the ultraviolet that produced it &mdash; a negative feedback. "
                          "The melanin response is therefore concave, rising toward a plateau, and it attenuates the ultraviolet reaching DNA to about "
                          f"{int(round(T3['delivered_uv_attenuation']*100))}% at high dose (partial photoprotection). Removing the screening abolishes the protection entirely, identifying the feedback as its cause."),
                  abstract_txt=("UV drives MITF to make melanin, which screens UV in a negative-feedback loop; the melanin response is concave and plateauing and attenuates delivered UV to about 21 percent, while removing the feedback abolishes the protection."),
                  abstract=("Ultraviolet drives MITF&rarr;melanin, and melanin screens ultraviolet, closing a negative-feedback loop. "
                            f"The melanin response is concave and plateauing; delivered ultraviolet is attenuated to about {int(round(T3['delivered_uv_attenuation']*100))}%, and removing the feedback abolishes the protection."),
                  body=body))

    # ---- 05 turnover (T4) ----
    body = f"""
<h2>Turnover is a conveyor, and conveyors add</h2>
<p>Epidermal renewal moves a cell from the basal layer to the surface and off. The total turnover time is therefore a <strong>sum of compartment residence times</strong>, not a single rate &mdash; a fact long established by labelled-cell studies that add a viable-epidermis transit to a stratum-corneum transit.</p>
<p>The two compartments here share the same master gene, TP63, so the substrate assigns them the <strong>same dwell time</strong> (the dwell ratio is {T4['phase_dwell_ratio']:.0f}). That is a prediction, not a fit: equal &gamma; gives equal substrate dwell.</p>
<h2>One cited calibration sets the clock</h2>
<p>With the stratum-corneum transit fixed to its cited value of <strong>{T4['sc_transit_days']:.0f} days</strong>, the equal-dwell viable phase is also {T4['viable_phase_days']:.0f} days, and the total epidermal turnover is <strong>{T4['total_turnover_days']:.0f} days</strong>. That lands inside the cited 28&ndash;40-day window for young-adult skin.</p>
{vp_card("Stratum-corneum transit &asymp; 14 days (cited)", "The single measured calibration in this target, taken from labelled-cell turnover studies. Everything else &mdash; the equal viable-phase dwell and the ~28-day total &mdash; follows from the substrate and the shared TP63 &gamma;, with no further tuning.")}
<h2>Ordering and grades</h2>
<p>Because dwell grows with &gamma;, the four organs rank in dwell as {esc(' &gt; '.join(T4['dwell_order_gamma1p5']))}. The conveyor-sum structure is simulation-verified {grade_badge('V')}; the rate rests on one cited anchor {grade_badge('L')} (the 14-day corneum transit). The absolute basal cycle time per cell is open {grade_badge('O')}: it needs a per-cell calibration.</p>
"""
    S.append(dict(no="05", slug="05-epidermal-turnover-dwell-cascade",
                  short="Turnover", title="Epidermal turnover as a substrate dwell-cascade",
                  h1="Epidermal turnover: residence times that add to a month",
                  keywords=["epidermal turnover", "skin renewal", "stratum corneum transit", "dwell time", "keratinocyte", "TP63"],
                  grades=["V", "L", "O"],
                  answer=("Epidermal turnover is a conveyor: total renewal time is the sum of compartment residences. "
                          "The viable epidermis and the stratum corneum share the same master gene (TP63), so the substrate predicts comparable phase dwell-times; "
                          f"calibrating the corneum transit to the cited ~{T4['sc_transit_days']:.0f} days gives a total of ~{T4['total_turnover_days']:.0f} days, inside the cited 28&ndash;40-day window."),
                  abstract_txt=("Epidermal turnover is the sum of compartment residences; the viable epidermis and stratum corneum share TP63 and so share dwell time, and calibrating the corneum to ~14 days gives a ~28-day total inside the cited 28-40 day window."),
                  abstract=("Total turnover is the sum of compartment residences. Viable epidermis and stratum corneum share TP63, so the substrate gives them equal dwell; "
                            f"with the cited ~{T4['sc_transit_days']:.0f}-day corneum transit the total is ~{T4['total_turnover_days']:.0f} days, inside the cited 28&ndash;40-day window."),
                  body=body))

    # ---- 06 thermoregulation (T5) ----
    body = f"""
<h2>Sweating is recruited, not always on</h2>
<p>A thermal load raises core temperature. The sweat gland is governed by the EDAR switch and stays off until the thermal drive clears its threshold; in this run recruitment begins at a load of about <strong>{T5['onset_load']}</strong>. Below that the skin sheds heat only passively.</p>
<p>Once recruited, the gland secretes in proportion to the temperature error, and evaporative cooling carries heat away as an interface flux. This is a feedback controller engaging at a set-point, not a linear radiator.</p>
<h2>The flux regulates &mdash; until it can&rsquo;t</h2>
<p>The regulation is visible in the slope of core temperature against thermal load. Before sweating it is about <strong>{T5['slope_passive']:.2f}</strong>; once the evaporative flux engages it falls sharply to about <strong>{T5['slope_sweating']:.2f}</strong>, the controller actively flattening the temperature rise.</p>
<p>Above the maximum sweat capacity the flux saturates: it can remove no more heat, and the slope climbs back to about <strong>{T5['slope_runaway']:.2f}</strong> as temperature runs away. That runaway above capacity is the substrate's picture of the heat-stroke limit.</p>
{vp_card("Skin-appendage switch (EDAR)", f"&gamma;={g['EDAR']} (measured), spinodal={sp['EDAR']} (substrate-derived). EDAR sets the recruitment threshold of the sweat appendage; the evaporative interface flux it gates is what converts a passive surface into a regulated thermostat.")}
<h2>Grades</h2>
<p>The thresholded onset, the flux-regulated slope drop, and the runaway above capacity are simulation-verified shapes {grade_badge('V')}. The absolute set-point (37&nbsp;&deg;C) and the absolute sweat rate are cited/open {grade_badge('O')}: they need per-gland output and body heat capacity as inputs.</p>
"""
    S.append(dict(no="06", slug="06-thermoregulation-sweat-interface-flux",
                  short="Thermoregulation", title="Thermoregulation: the sweat gland as a regulated interface flux",
                  h1="Thermoregulation: a sweat-gated interface flux with a heat-stroke limit",
                  keywords=["thermoregulation", "sweating", "evaporative cooling", "EDAR", "set-point", "heat stroke", "interface flux"],
                  grades=["V", "O"],
                  answer=("Sweating is an interface flux under feedback control. A thermal load raises core temperature until it clears the EDAR sweat-switch threshold; "
                          f"evaporative cooling then regulates temperature, dropping the temperature-versus-load slope from {T5['slope_passive']:.1f} to {T5['slope_sweating']:.2f}. "
                          f"Above the maximum sweat capacity the flux saturates and temperature runs away &mdash; the heat-stroke limit."),
                  abstract_txt=("Sweating is gated by an EDAR threshold and acts as an evaporative interface flux that regulates core temperature, flattening the temperature-load slope until sweat capacity saturates and temperature runs away."),
                  abstract=("A thermal load raises core temperature until it crosses the EDAR sweat-switch threshold; the evaporative interface flux then regulates temperature, "
                            f"dropping the temperature&ndash;load slope from {T5['slope_passive']:.1f} to {T5['slope_sweating']:.2f}, until capacity saturates and temperature runs away."),
                  body=body))

    # ---- 07 oncology ----
    scc_r = onc["scc_low_dose_r"]; mel_rr = onc["melanoma_intermittent_max_rr"]; tanf = onc["tan_protection_factor"]
    body = f"""
<h2>One convex rate, two cancers</h2>
<p>In this framework a carcinogen is a sustained aberrant drive that lowers the barrier between the normal and malignant basins of the same cell switch; the malignant-crossing rate is Kramers-like, <code>rate &sim; e<sup>|h|/spinodal</sup></code>. Because malignancy needs several independent hits, the realised rate is multistage, <code>rate<sup>K</sup></code> with K&nbsp;&asymp;&nbsp;{D['K']} &mdash; a cited biological structure, not a fitted knob. That single convex rate splits the two ultraviolet cancers.</p>
<h2>Squamous-cell carcinoma tracks cumulative dose</h2>
<p>At a fixed chronic intensity the cumulative malignant-initiation probability accumulates linearly in total dose, so squamous-cell carcinoma rises <strong>near-linearly with cumulative ultraviolet</strong>: across the low-dose range the dose&ndash;response is linear to a correlation of <strong>r = {scc_r:.3f}</strong>. This matches the recognised near-linear dependence of cutaneous SCC on cumulative, occupational ultraviolet.</p>
{vp_card("Multistage exponent K &asymp; 5 (cited)", "The Armitage&ndash;Doll multistage model: carcinogenesis requires several independent rate-limiting hits, making incidence a high power of the per-event rate. K is a cited structural feature of cancer epidemiology; it is what makes the malignant rate convex enough for intermittent exposure to dominate.")}
<h2>Melanoma tracks intermittent bursts</h2>
<p>For a <em>fixed</em> cumulative dose, concentrating it into bursts raises the integrated hazard, because a convex rate rewards peaks (Jensen's inequality). Delivering the same dose intermittently rather than spread raises the melanoma relative risk by up to about <strong>{mel_rr:.1f}&times;</strong> here &mdash; the substrate's account of melanoma's sunburn/intermittent-exposure sensitivity.</p>
<h2>The chronic-exposure paradox</h2>
<p>Chronic exposure is then <em>protective</em> against melanoma. A spread, chronic dose builds a melanin screen (the tan of the previous page) that a fast sunburn cannot, lowering the effective intensity; in this run the tan reduces the chronic-arm hazard by a factor of about <strong>{tanf:.1f}&times;</strong>. That reproduces the otherwise puzzling inverse association between chronic occupational ultraviolet and melanoma.</p>
{vp_card("Intermittent-exposure anchor (cited)", "Gandini et al. (2005), a meta-analysis of 57 studies: intermittent sun exposure raises melanoma risk (summary relative risk 1.61, 95% CI 1.31&ndash;1.99) while chronic/occupational exposure does not, and a history of sunburn roughly doubles risk. The substrate matches the direction of each.")}
<h2>Grades</h2>
<p>The SCC cumulative linearity, the melanoma intermittent-sensitivity, and the chronic-exposure tan paradox are simulation-verified directions {grade_badge('V')} resting on cited epidemiological anchors {grade_badge('L')}. The absolute incidences and the absolute relative-risk magnitudes are open {grade_badge('O')}: they need a population baseline rate and an absolute dose calibration.</p>
"""
    S.append(dict(no="07", slug="07-uv-carcinogenesis-dose-response",
                  short="UV carcinogenesis", title="Ultraviolet carcinogenesis: the squamous/melanoma dose-response dichotomy",
                  h1="Ultraviolet carcinogenesis: why squamous and melanoma read dose differently",
                  keywords=["ultraviolet carcinogenesis", "melanoma", "squamous cell carcinoma", "cumulative dose", "intermittent exposure", "sunburn", "multistage", "Armitage-Doll"],
                  grades=["V", "L", "O"],
                  answer=("Ultraviolet carcinogenesis splits cleanly on the substrate. Because the multistage malignant rate is convex in dose-intensity, squamous-cell carcinoma rises "
                          f"near-linearly with cumulative dose (r={scc_r:.3f}), while melanoma is intermittent-sensitive: the same dose in bursts raises relative risk up to ~{mel_rr:.1f}&times;. "
                          f"Chronic exposure builds a screening tan, protecting against melanoma by ~{tanf:.1f}&times; &mdash; the chronic-exposure paradox."),
                  abstract_txt=("A single convex multistage rate splits the UV cancers: SCC rises near-linearly with cumulative dose while melanoma is sensitive to intermittent bursts, and the chronic-exposure tan protects against melanoma, reproducing the documented paradox."),
                  abstract=("A single convex, multistage malignant rate splits the two ultraviolet cancers. SCC rises near-linearly with cumulative dose "
                            f"(r={scc_r:.3f}); melanoma is intermittent-sensitive (burst relative risk up to ~{mel_rr:.1f}&times;); and a chronic-exposure tan protects against melanoma (~{tanf:.1f}&times;)."),
                  body=body))

    # ---- 08 methods ----
    body = f"""
<h2>Substrate and discipline</h2>
<p>Every result here is reproduced from one vendored primitive: the R19 bistable switch <code>ds/dt = g&middot;s &minus; s&sup3; + h</code>, with its spinodal, barrier, and dwell. The only organism-specific inputs are the four measured master-gene &gamma; values, carried read-only from the DNA gene-clock package.</p>
<p>The governing rule is the no-tuning invariant: <strong>every constant is either a measured input (cited and locked) or substrate-derived &mdash; never chosen to fit a target</strong>. The measured &gamma; drive falsifiable cross-checks (the developmental order, the &gamma;<sup>1.5</sup> insult ordering, the equal-dwell turnover); the dimensionless dynamical scales set the regime in which each mechanism is exhibited and are graded honestly rather than calibrated to data.</p>
<h2>Grades</h2>
<table>
<thead><tr><th>Grade</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>{grade_badge('F')}</td><td>Forced by the substrate (e.g. a spinodal computed from measured &gamma;).</td></tr>
<tr><td>{grade_badge('V')}</td><td>Simulation-verified shape, control, or ordering.</td></tr>
<tr><td><span class="grade g-open">[L]</span></td><td>Cited external anchor (a measured number from the literature).</td></tr>
<tr><td>{grade_badge('O')}</td><td>Open, with the obstacle to closing it stated explicitly.</td></tr>
</tbody></table>
<h2>Reproducibility</h2>
<p>The research pipeline is deterministic: BLAS is pinned single-thread, all grids are fixed, and no random number generator is used. Two independent runs produce a byte-identical result, hashed to SHA-256 <code>{esc(D['sha'])}</code>. The writing phase is gated &mdash; this site cannot be generated until the research gate is green and the phase is flipped.</p>
<p>To reproduce: run <code>python repro/run_all.py</code> for the full research record, <code>python repro/_verify/stress_tests.py</code> for the graded stress battery (targets T1&ndash;T5 plus the carcinogenesis dichotomy), and <code>python repro/_verify/gates.py</code> for the determinism and gate check. The engine code is bundled in this package under <code>repro/</code> and is the canonical source for every number above.</p>
{vp_card("Result SHA-256 (determinism)", f"<code>{esc(D['sha'])}</code><br>Identical across independent processes &mdash; the C1 reproducibility gate. Any change to a number on these pages must change this hash.")}
<h2>Open items (obstacle ledger)</h2>
<p>The following are the absolute quantities this package does <em>not</em> yet derive, each with its obstacle: absolute TEWL (lipid permeability + water-activity gradient); absolute wound closure rate (single-cell migration speed); absolute minimal erythema dose (melanin extinction coefficient); absolute basal cycle time (per-cell calibration); absolute set-point and sweat rate (per-gland output + body heat capacity); absolute cancer incidence and relative-risk magnitude (population baseline rate + absolute dose calibration). The shapes, controls, orderings, and dichotomies above stand independently of these {grade_badge('O')} items.</p>
"""
    S.append(dict(no="08", slug="08-methods-grades-reproducibility",
                  short="Methods", title="Methods, grades and reproducibility",
                  h1="Methods, grades, and reproducibility",
                  keywords=["reproducibility", "methods", "no tuning", "VP theory", "determinism", "grading", "jamming substrate"],
                  grades=["V", "F", "O"],
                  answer=("Every quantity here is reproduced deterministically from the R19 jamming-lattice substrate and measured master-gene &gamma;; two runs give an identical SHA-256. "
                          "Master-gene &gamma; values are measured inputs (cited from the DNA gene-clock), never fitted; dynamical scales are dimensionless and graded honestly &mdash; "
                          "shape [V], cited anchors [L], absolute magnitudes [O] with stated obstacles."),
                  abstract_txt=("All results derive from the R19 bistable substrate and measured master-gene gamma under a strict no-tuning rule, are bit-reproducible to an identical SHA-256, and are graded F/V/L/O with every open item carrying a stated obstacle."),
                  abstract=("All results derive from the R19 bistable substrate and measured master-gene &gamma; under a strict no-tuning rule. "
                            "The pipeline is bit-reproducible to an identical SHA-256, and every claim is graded, with each open item carrying a stated obstacle."),
                  body=body))

    # ---- 09 pathology (disease layer; mirrors repro/_pathology, separate hash) ----
    PA = D["patho"]
    ad = PA["atopic_dermatitis"]; ich = PA["ichthyosis"]; pso = PA["psoriasis"]
    cw = PA["chronic_diabetic_pressure_wound"]; vit = PA["vitiligo"]; mel = PA["melasma_hyperpigmentation"]
    alb = PA["albinism_OCA"]; hed = PA["hypohidrotic_ectodermal_dysplasia"]
    hyp = PA["primary_hyperhidrosis"]; hs = PA["heat_stroke"]
    can = PA["skin_cancer_melanoma_scc_bcc"]; ak = PA["actinic_keratosis"]
    opp = PA["_opposite_sign_discriminant"]
    ad_emoll = ad["intervention_barrier_reserve"] / ad["healthy_barrier_reserve"]
    def _yn(b): return "yes" if b else "no"
    _map_rows = [
        ("Atopic dermatitis", "T1", "chronic barrier-reserve collapse"),
        ("Contact dermatitis", "T1", "acute insult past the discontinuous collapse"),
        ("Ichthyosis (dynamics)", "T1+T4", "desquamation retention near the spinodal"),
        ("Psoriasis", "T4", "differentiation-spinodal threshold + autonomous acceleration"),
        ("Chronic / diabetic / pressure wound", "T2", "non-closure below the critical unjamming drive"),
        ("Vitiligo", "T3", "discontinuous melanocyte-viability loss"),
        ("Melasma / hyperpigmentation", "T3", "regulated melanin overshoot"),
        ("Albinism / OCA (dynamics)", "T3&rarr;onco", "screen removed &rarr; hazard relative risk"),
        ("Hypohidrotic ectodermal dysplasia (dynamics)", "T5", "capped sweat &rarr; danger band at lower load"),
        ("Primary hyperhidrosis", "T5", "lowered recruitment threshold"),
        ("Heat stroke", "T5", "capacity exceeded &rarr; runaway"),
        ("Skin cancer (melanoma / SCC / BCC)", "onco", "intermittent-vs-cumulative + pigment-loss burst"),
        ("Actinic keratosis", "onco", "SCC precursor (fewer multistage hits)"),
    ]
    _map_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b, c) in _map_rows)
    _opp_rows = [
        ("Turnover", "psoriasis (accelerated)", "ichthyosis (retention)", opp["turnover_psoriasis_accelerated_vs_ichthyosis_retention"]),
        ("Barrier reserve", "intact (full reserve)", "atopic (collapsed reserve)", opp["barrier_full_reserve_vs_atopic_collapsed_reserve"]),
        ("Melanin", "melasma (overshoot)", "vitiligo (loss)", opp["melanin_melasma_overshoot_vs_vitiligo_loss"]),
        ("Sweat recruitment", "hyperhidrosis (excess)", "ectodermal dysplasia (deficit)", opp["sweat_hyperhidrosis_excess_vs_hed_deficit"]),
        ("Photoprotection", "healthy tan (screened)", "pigment loss (unscreened)", opp["photoprotection_healthy_tan_vs_pigment_loss_unprotected"]),
    ]
    _opp_html = "".join(f'<tr><td>{k}</td><td>{p}</td><td>{n}</td><td class="num">{_yn(ok)}</td></tr>'
                        for (k, p, n, ok) in _opp_rows)
    body = f"""
<h2>Disease is mechanism off its set-point; treatment is the same knob reversed</h2>
<p>The previous pages established six verified mechanisms &mdash; the water barrier (T1), wound closure (T2), the melanin screen (T3), turnover (T4), thermoregulation (T5), and the carcinogenesis kernel. This page covers the major skin diseases without adding any new physics: each disease is one of those mechanisms driven away from its set-point, and each established treatment is the <em>same</em> control pushed back. Thirteen diseases pass a clinical-sign plus intervention-reversal battery and a five-way opposite-sign discriminant, with no constant introduced.</p>
<table>
<thead><tr><th>Disease</th><th>Target</th><th>Covered as</th></tr></thead>
<tbody>
{_map_html}
</tbody></table>

<h2>Barrier failures (T1): atopic, contact, ichthyosis</h2>
<p>Atopic dermatitis is a <strong>chronic</strong> erosion of barrier reserve: the depth of the intact-barrier basin falls to about <strong>{ad['disease_reserve_fraction']:.2f}</strong> of healthy, and barrier repair (emollient) restores it to about {ad_emoll:.2f} &mdash; the knob moved back, not a new mechanism. Contact dermatitis is the <strong>acute</strong> mode of the same T1 switch: an external irritant clears the spinodal and the barrier collapses discontinuously rather than drifting. Ichthyosis sits on the retention side: a weak desquamation drive holds the corneum near its spinodal, raising stratum-corneum residence about <strong>{ich['retention_fold']:.1f}&times;</strong> (critical slowing), reversed by a keratolytic that restores a strong shedding drive.</p>
{vp_card("Atopic dermatitis anchor (cited)", "Atopic dermatitis is a barrier-defect disease (filaggrin loss-of-function) with reduced barrier function and a flare-prone course. " + grade_badge('L'))}
{vp_card("Contact dermatitis anchor (cited)", "Contact dermatitis is an acute barrier breach from an external irritant or allergen that resolves on removal plus active barrier repair. " + grade_badge('L'))}
{vp_card("Ichthyosis anchor (cited)", "Ichthyosis is retention hyperkeratosis: impaired desquamation and a thickened stratum corneum. " + grade_badge('L'))}

<h2>Turnover off both poles (T4): psoriasis versus ichthyosis</h2>
<p>Psoriasis is the turnover mechanism past its differentiation spinodal: below threshold transit is homeostatic (about {pso['homeostatic_turnover_days']:.0f} days), but above it the exit drive becomes <strong>autonomous and self-accelerating</strong>, compressing transit about <strong>{pso['relative_acceleration_in_autonomous_regime']:.1f}&times;</strong> toward the cited 3&ndash;5-day psoriatic window (against the 28&ndash;40-day healthy window). Anti-proliferative therapy lowers the exit drive back below the spinodal. Psoriasis (acceleration) and ichthyosis (retention) are the two opposite signs of one turnover switch.</p>
{vp_card("Psoriasis anchor (cited)", "Psoriatic epidermal transit is accelerated to roughly 3&ndash;5 days against the ~28&ndash;40-day healthy window &mdash; several-fold hyperproliferation; the substrate reproduces the threshold and direction, absolute days open. " + grade_badge('L'))}

<h2>Wound non-closure (T2): chronic, diabetic, pressure wounds</h2>
<p>A chronic wound is re-epithelialisation held below its own unjamming drive. With the vertex-model threshold q* = 3.81 fixed (cited), a free-edge drive of {cw['disease_drive']} stays below the package's critical unjamming drive of {cw['critical_unjam_drive']}, so the edge never crosses q*, the sheet stays jammed, and the gap does not close. Raising the drive to {cw['intervention_drive']} (debridement, growth factor, or a re-epithelialisation cue) carries it over the threshold and the wound closes &mdash; the same T2 unjam&rarr;migrate&rarr;rejam cycle, restored.</p>
{vp_card("Chronic-wound anchor (cited)", "A chronic wound is a failure to re-epithelialise within the expected window from impaired collective migration; q* = 3.81 is the cited vertex-model jamming threshold. " + grade_badge('L'))}

<h2>Pigment off both poles (T3): vitiligo, melasma, albinism</h2>
<p>Vitiligo drives the melanocyte <em>viability</em> switch below its spinodal: melanin collapses discontinuously to {vit['disease_melanin']:.1f} and the delivered-ultraviolet attenuation returns to {vit['disease_attenuation']:.1f} (no screen at all), so the patch is photoprotection-deficient &mdash; repigmentation needs active phototherapy (hysteresis). Melasma is the opposite sign of the same MITF switch: a standing pro-melanogenic drive raises regulated melanin about <strong>{mel['overshoot_fold']:.2f}&times;</strong>, reversed by removing the driver. Albinism removes the functional screen upstream, so the ultraviolet reaching DNA stays full and the shared multistage hazard rises to a relative risk of about <strong>{alb['hazard_RR_albino_vs_pigmented']:.2f}&times;</strong> versus pigmented skin &mdash; an exogenous sunscreen brings it back to about {alb['intervention_hazard_RR']:.2f}&times;.</p>
{vp_card("Vitiligo anchor (cited)", "Vitiligo is autoimmune melanocyte loss leaving depigmented, photoprotection-deficient patches; repigmentation requires active phototherapy. " + grade_badge('L'))}
{vp_card("Melasma anchor (cited)", "Melasma is acquired focal hypermelanosis driven by hormones and ultraviolet, partially reversible with photoprotection and depigmenting therapy. " + grade_badge('L'))}
{vp_card("Albinism (OCA) anchor (cited)", "Photoprotection-deficient albino skin shows markedly elevated cutaneous squamous-cell carcinoma and melanoma, especially in high-ultraviolet regions. " + grade_badge('L'))}

<h2>Thermoregulation off both poles (T5): ectodermal dysplasia, hyperhidrosis, heat stroke</h2>
<p>Hypohidrotic ectodermal dysplasia caps the sweat appendage's maximum capacity, so the evaporative interface flux is limited and the danger band is reached at a lower load: onset moves from {hed['healthy_danger_onset_load']} (healthy) to {hed['disease_danger_onset_load']} (disease), and at a test load of {hed['test_load']} the core measure runs to <strong>{hed['disease_core_temp_arb']:.2f}</strong> against {hed['healthy_core_temp_arb']:.2f} healthy &mdash; external cooling caps the load below that onset. Primary hyperhidrosis is the opposite sign of the same EDAR switch: the recruitment threshold is lowered (onset {hyp['disease_sweat_onset_load']} against {hyp['healthy_sweat_onset_load']}), so the gland fires sub-threshold, and threshold-raising therapy reverses it. Heat stroke is the capacity limit of the healthy controller: above saturation the regulated temperature&ndash;load slope ({hs['slope_regulated']:.2f}) jumps to the runaway slope ({hs['slope_runaway']:.2f}) and core temperature climbs without bound.</p>
{vp_card("Ectodermal-dysplasia anchor (cited)", "Hypohidrotic ectodermal dysplasia (EDAR pathway) reduces or removes sweat glands, producing hyperthermia and heat intolerance. " + grade_badge('L'))}
{vp_card("Hyperhidrosis anchor (cited)", "Primary focal hyperhidrosis is sweating beyond thermoregulatory need and responds to threshold-raising therapies. " + grade_badge('L'))}
{vp_card("Heat-stroke anchor (cited)", "Heat stroke is thermoregulatory failure: core temperature climbs past a critical band once evaporative capacity is overwhelmed. " + grade_badge('L'))}

<h2>Oncology: skin cancer and its precursor</h2>
<p>The carcinogenesis page's single convex multistage rate carries straight into disease. Squamous-cell carcinoma is near-linear in cumulative dose (linear to r = {can['scc_low_dose_r']:.3f}); melanoma is intermittent-sensitive, the same dose in bursts raising relative risk up to about <strong>{can['melanoma_intermittent_max_rr']:.2f}&times;</strong>; and a chronic-exposure tan protects against melanoma by about {can['tan_protection_factor']:.2f}&times; (the paradox). The pigment-loss diseases above couple in here: removing the screen raises the burst relative risk to about <strong>{can['pigment_loss_burst_RR']:.2f}&times;</strong>. Actinic keratosis is the same kernel with <em>fewer</em> hits crossed &mdash; early field damage of high prevalence ({ak['ak_field_prevalence'][-1]:.2f}) sitting above invasive squamous-cell carcinoma ({ak['scc_incidence'][-1]:.2f}) at the same dose, with only a small per-lesion fraction completing the remaining hits.</p>
{vp_card("Skin-cancer epidemiology anchor (cited)", "Gandini et al. (2005) meta-analysis: melanoma intermittent summary relative risk 1.61, chronic occupational exposure inversely associated, squamous-cell carcinoma near-linear in cumulative ultraviolet; Armitage&ndash;Doll multistage K&asymp;5. " + grade_badge('L'))}
{vp_card("Actinic-keratosis anchor (cited)", "Actinic keratosis is the most common ultraviolet precursor lesion: high prevalence in sun-damaged skin, low per-lesion progression to invasive cutaneous squamous-cell carcinoma. " + grade_badge('L'))}

<h2>The discriminant: opposite diseases from opposite drive signs</h2>
<p>The decisive test is that opposite clinical entities fall out of the <em>same</em> switch driven in opposite directions, with no constant changed between them. Each pole below is the literal sign-flip of its partner on one R19 control.</p>
<table>
<thead><tr><th>Switch</th><th>Positive-drive pole</th><th>Negative-drive pole</th><th>Reproduced</th></tr></thead>
<tbody>
{_opp_html}
</tbody></table>
<p>All five opposite pairs reproduce ({_yn(opp['all_opposite_pairs_reproduced'])}). That a single switch generates psoriasis and ichthyosis, melasma and vitiligo, hyperhidrosis and the ectodermal-dysplasia deficit from opposite signs alone is the strongest internal evidence that the lesions are dynamics, not bespoke parameters.</p>

<h2>Grades and reproducibility</h2>
<p>Every disease mechanism here is a simulation-verified shape, control, or sign {grade_badge('V')}; every clinical mapping rests on a cited anchor {grade_badge('L')}; and every absolute magnitude is open {grade_badge('O')}, each inheriting the obstacle of its parent target &mdash; absolute TEWL (T1 lipid permeability), absolute closure rate (T2 cell speed), absolute melanin optical density (T3 extinction coefficient), absolute transit days (T4 per-cell calibration), absolute set-point and sweat rate (T5 per-gland output and heat capacity), and absolute incidence and relative-risk magnitude (oncology population baseline and dose calibration). No disease introduces a new constant; each is a named perturbation of an existing knob.</p>
<p>The pathology pipeline is deterministic on its own terms: two independent runs hash to an identical SHA-256, separate from the core battery. Crucially, adding this disease layer does <strong>not</strong> touch the core T1&ndash;T5+oncology battery, whose result hash is unchanged at <code>{esc(D['sha'][:12])}&hellip;</code>.</p>
{vp_card("Pathology result SHA-256 (determinism)", f"<code>{esc(D['patho_sha'])}</code><br>The C1 reproducibility gate for the disease layer, identical across independent processes and distinct from the core-battery hash. Reproduce with <code>python repro/run_pathology.py</code>.")}
"""
    S.append(dict(no="09", slug="09-integumentary-pathology",
                  short="Pathology", title="Integumentary pathology: thirteen diseases as perturbations of the verified mechanisms",
                  h1="Integumentary pathology: disease as mechanism off its set-point",
                  keywords=["skin disease", "dermatology", "atopic dermatitis", "psoriasis", "vitiligo", "melasma",
                            "chronic wound", "hyperhidrosis", "heat stroke", "skin cancer", "actinic keratosis", "VP theory"],
                  grades=["V", "L", "O"],
                  answer=("The thirteen major skin diseases are not new physics: each is one verified mechanism (T1&ndash;T5 or the oncology kernel) "
                          "driven off its set-point, and each treatment is the same knob reversed. They pass a clinical-sign plus intervention-reversal "
                          "battery and a five-way opposite-sign discriminant &mdash; psoriasis/ichthyosis, melasma/vitiligo, hyperhidrosis/ectodermal-dysplasia &mdash; with no constant added."),
                  abstract_txt=("Thirteen common dermatoses are reproduced as signed perturbations of the same R19 switches that emerged the skin organs; opposite diseases arise from opposite drive signs on one switch, every intervention reverses its lesion, and the disease layer adds no constant and leaves the core battery hash unchanged."),
                  abstract=("Thirteen common skin diseases are reproduced as signed perturbations of the six verified mechanisms. "
                            "Opposite entities &mdash; psoriasis/ichthyosis, melasma/vitiligo, hyperhidrosis/ectodermal-dysplasia &mdash; emerge from opposite drive signs on a single R19 switch, "
                            "every intervention is the same knob reversed, and the layer adds no constant while the core-battery hash stays fixed."),
                  body=body))

    # ---- 10 hair-follicle cycle (oscillator layer; mirrors repro/_cycle, separate hash) ----
    CY = D["cyc"]
    osc = CY["_oscillator"]; aga = CY["androgenetic_alopecia"]; aa = CY["alopecia_areata"]
    te = CY["telogen_effluvium"]; ane = CY["anagen_effluvium"]
    cyopp = CY["_opposite_sign_discriminant"]; cydich = CY["_shedding_dichotomy"]
    def _yn2(b): return "yes" if b else "no"
    aga_prog = aga["anagen_fraction_progression"]
    _alo_rows = [
        ("Androgenetic alopecia", "anagen duration", "standing anti-growth drive shortens the anagen plateau &rarr; progressive miniaturisation"),
        ("Alopecia areata", "premature catagen", "sustained immune-type drive forces anagen &rarr; telogen; regrows on removal (hysteresis)"),
        ("Telogen effluvium", "phase synchronisation", "a transient stressor synchronises a cohort into telogen; sheds one telogen later, self-limited"),
        ("Anagen effluvium", "anagen-matrix arrest", "a direct cytotoxic insult sheds anagen hairs immediately, bypassing telogen"),
    ]
    _alo_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b, c) in _alo_rows)
    _cyopp_rows = [
        ("Anagen duration", "minoxidil / anti-androgen (long)", "androgenetic (short)", cyopp["anagen_duration_aga_short_vs_minoxidil_long"]),
        ("Shed timing", "telogen effluvium (delayed, one telogen)", "anagen effluvium (immediate)", cyopp["shed_timing_te_delayed_vs_anagen_effluvium_immediate"]),
        ("Persistence", "alopecia areata (sustained while driven)", "telogen effluvium (self-limited)", cyopp["persistence_aa_sustained_vs_te_self_limited"]),
    ]
    _cyopp_html = "".join(f'<tr><td>{k}</td><td>{p}</td><td>{n}</td><td class="num">{_yn2(ok)}</td></tr>'
                          for (k, p, n, ok) in _cyopp_rows)
    body = f"""
<h2>The hair follicle is the one skin structure that cycles &mdash; so it needs an oscillator, not a switch</h2>
<p>Every mechanism so far has been a <em>static</em> R19 switch: the barrier sits in one basin, the melanin screen in another. But the core battery itself reports a gap &mdash; there is no autonomous oscillator anywhere in the integumentary class, and the one structure that demands one is the hair follicle, which cycles on its own between a long growth phase (anagen), a brief regression (catagen), and a resting phase (telogen), then re-enters growth without any external clock. This page closes that gap with no new organ and no new fitted constant: it puts the <strong>same measured EDAR &gamma; = {osc['gamma']}</strong> that already emerged the skin appendage onto the <strong>same vendored relaxation oscillator</strong> the thermoregulation page (T5) already uses, and reads off the cycle.</p>
<table>
<thead><tr><th>Quantity</th><th>Value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Master gene (measured)</td><td class="num">EDAR &gamma; = {osc['gamma']}</td><td>the appendage organ's own &gamma;, read-only &mdash; not refitted</td></tr>
<tr><td>Spinodal</td><td class="num">{osc['spinodal']:.3f}</td><td>substrate-derived from &gamma; (sets the regime scale)</td></tr>
<tr><td>Growth bias</td><td class="num">{osc['growth_bias']:.3f}</td><td>half the appendage spinodal &mdash; a substrate-scaled regime scale [F], not fitted to a hair phenotype</td></tr>
<tr><td>Oscillates</td><td class="num">{_yn2(osc['oscillates'])}</td><td>the follicle cycles autonomously (limit cycle, not a fixed point)</td></tr>
<tr><td>Anagen-dominant</td><td class="num">{_yn2(osc['anagen_dominant'])}</td><td>growth occupies the larger share of the cycle</td></tr>
<tr><td>Relaxation waveform</td><td class="num">{_yn2(osc['relaxation_waveform'])}</td><td>a long plateau then a fast collapse, not a smooth sinusoid</td></tr>
</tbody></table>
<p>The cycle is <strong>anagen-dominant</strong> (the growth phase takes a fraction of about {osc['anagen_fraction']:.2f} of the cycle) and has a clear <strong>relaxation shape</strong> &mdash; the plateau occupies about <strong>{osc['plateau_dominance']:.2f}</strong> of each beat before a rapid collapse, exactly the long-growth/short-rest asymmetry the biology shows. These two facts &mdash; <em>that growth dominates</em> and <em>that the waveform is a plateau-then-collapse relaxation cycle</em> &mdash; are the simulation-verified core {grade_badge('V')} of this page; they come straight out of the substrate with nothing tuned.</p>
{vp_card("Hair-cycle anchor (cited)", "The follicle spends the great majority of its cycle in anagen &mdash; growth lasts roughly 2&ndash;6 years against a telogen of about 3 months, so anagen is on the order of 85&ndash;90&percnt; of the cycle. " + grade_badge('L'))}
<p>The package is deliberately honest about what it does <em>not</em> claim here. The <strong>absolute</strong> anagen fraction (the cited 85&ndash;90&percnt;) and the <strong>absolute</strong> period (years) are <em>not</em> fitted: a single constant drive strong enough to reach 88&percnt; would push the element through its Hopf point and kill the oscillation altogether. So the substrate is graded against those anchors by <em>dominance and direction</em>, not by magnitude &mdash; the model reproduces that anagen dominates and that the waveform relaxes, and the absolute fraction and the years-long period remain open {grade_badge('O')}, inheriting the appendage target's standing obstacle (a per-follicle calibration). This is the same no-tuning rule the rest of the package runs under, applied to a dynamical regime.</p>

<h2>Four alopecias are this one oscillator driven off its cycle</h2>
<p>With the oscillator established, the four major patterned hair-loss diseases follow with no new physics &mdash; each is the same cycle driven away from its set-point, and each established treatment is the same drive reversed. Four diseases pass a clinical-sign plus intervention-reversal battery and a three-way opposite-sign / opposite-timing discriminant, with no constant introduced.</p>
<table>
<thead><tr><th>Disease</th><th>Cycle handle</th><th>Covered as</th></tr></thead>
<tbody>
{_alo_html}
</tbody></table>

<h2>Anagen duration off both poles: androgenetic alopecia versus its therapy</h2>
<p>Androgenetic alopecia is a <strong>standing anti-growth drive</strong> on the cycle: the anagen plateau shortens, so the anagen fraction falls progressively from about <strong>{aga_prog[0]:.2f}</strong> through <strong>{aga_prog[1]:.2f}</strong> to <strong>{aga_prog[2]:.2f}</strong> &mdash; the substrate's account of terminal-to-vellus miniaturisation across successive cycles. A pro-growth drive (minoxidil or an anti-androgen) lengthens anagen back to about <strong>{aga['intervention_anagen_fraction']:.2f}</strong>: the same knob, reversed, not a new mechanism. Progressive miniaturisation reproduces ({_yn2(aga['miniaturisation_progressive'])}).</p>
{vp_card("Androgenetic alopecia anchor (cited)", "Androgenetic alopecia is androgen-driven progressive follicular miniaturisation with anagen shortening; minoxidil and finasteride prolong anagen and partially reverse it. " + grade_badge('L'))}

<h2>Anagen arrest under a sustained drive: alopecia areata</h2>
<p>Alopecia areata is a <strong>sustained premature-catagen drive</strong>: an immune-type signal forces follicles out of anagen, dropping the anagen fraction to about <strong>{aa['disease_anagen_fraction']:.2f}</strong> while the drive persists. Because the underlying element is bistable, removing the drive lets anagen resume &mdash; the fraction recovers to about <strong>{aa['recovered_anagen_fraction']:.2f}</strong>, the regrowth-on-removal hysteresis the clinic sees. Anagen suppression reproduces ({_yn2(aa['anagen_suppressed'])}); it is <em>sustained while driven</em>, which is the pole that contrasts with the self-limited effluvium below.</p>
{vp_card("Alopecia areata anchor (cited)", "Alopecia areata is immune-mediated premature catagen / anagen arrest with patchy loss and frequent spontaneous or treated regrowth. " + grade_badge('L'))}

<h2>The decisive timing test: delayed versus immediate shedding</h2>
<p>The two effluvia share a cause &mdash; a synchronising insult &mdash; but differ in <em>when</em> the hair sheds, and the oscillator reproduces both timings from one cycle. <strong>Telogen effluvium</strong> is a transient systemic stressor that pushes an anagen cohort synchronously into telogen; that cohort then sheds <strong>one telogen duration later</strong>. In the simulation the shed peak lags the stressor by exactly <strong>{te['shed_peak_lag_steps']} steps</strong> &mdash; which is precisely one telogen arc ({te['one_telogen_steps']} steps = (1 &minus; {osc['anagen_fraction']:.2f}) of the cycle) &mdash; then the cohort re-enters anagen, so the shed is <strong>self-limited</strong>. <strong>Anagen effluvium</strong>, by contrast, is a direct cytotoxic insult to the growing matrix (chemotherapy or radiation): the anagen hair sheds <strong>immediately</strong>, with a lag of <strong>{ane['shed_peak_lag_steps']} steps</strong>, bypassing telogen entirely, and reverses once the insult stops. Same oscillator, opposite timing &mdash; the delayed-versus-immediate dichotomy reproduces ({_yn2(cydich['timing_dichotomy'])}).</p>
{vp_card("Telogen effluvium anchor (cited)", "Telogen effluvium is a synchronised premature-telogen entry after a systemic stressor, with a diffuse shed about 3 months &mdash; one telogen &mdash; later, and spontaneous recovery. " + grade_badge('L'))}
{vp_card("Anagen effluvium anchor (cited)", "Anagen effluvium is rapid shedding of anagen hairs during cytotoxic therapy, distinct from the delayed telogen effluvium, and reverses after the insult. " + grade_badge('L'))}

<h2>The discriminant: opposite alopecias from opposite drive signs and timings</h2>
<p>As with the static diseases, the decisive evidence is that opposite clinical entities fall out of the <em>same</em> oscillator driven in opposite ways, with no constant changed between them.</p>
<table>
<thead><tr><th>Axis</th><th>One pole</th><th>Opposite pole</th><th>Reproduced</th></tr></thead>
<tbody>
{_cyopp_html}
</tbody></table>
<p>All three opposite pairs reproduce ({_yn2(cyopp['all_opposite_pairs_reproduced'])}). That a single relaxation cycle yields shortened anagen and lengthened anagen, sustained loss and self-limited loss, and delayed shedding and immediate shedding from opposite signs and timings alone &mdash; with the same EDAR &gamma; and no new parameter &mdash; is the strongest internal evidence that the alopecias are cycle dynamics, not bespoke fits.</p>

<h2>Grades and reproducibility</h2>
<p>Every mechanism here is a simulation-verified shape, control, or timing {grade_badge('V')} &mdash; oscillation, anagen-dominance, the relaxation waveform, the miniaturisation direction, the one-telogen shed lag, the immediate-versus-delayed dichotomy. Every clinical mapping rests on a cited anchor {grade_badge('L')}. Every absolute magnitude is open {grade_badge('O')} &mdash; the absolute anagen fraction, the years-long period, absolute hair counts and shed fractions &mdash; each inheriting the appendage target's obstacle (a per-follicle calibration). No disease introduces a new constant; each is a named perturbation of the one oscillator.</p>
<p>The hair-cycle pipeline is deterministic on its own terms: two independent runs hash to an identical SHA-256, separate from both the core battery and the pathology layer. Crucially, adding this oscillator layer does <strong>not</strong> touch the core T1&ndash;T5+oncology battery, whose result hash is unchanged at <code>{esc(D['sha'][:12])}&hellip;</code>.</p>
{vp_card("Hair-cycle result SHA-256 (determinism)", f"<code>{esc(D['cyc_sha'])}</code><br>The C1 reproducibility gate for the hair-cycle layer, identical across independent processes and distinct from both the core-battery and pathology hashes. Reproduce with <code>python repro/run_cycle.py</code>.")}
"""
    S.append(dict(no="10", slug="10-hair-follicle-cycle-anagen-telogen",
                  short="Hair cycle", title="The hair-follicle cycle: an emergent oscillator and four alopecias",
                  h1="The hair-follicle cycle: anagen&ndash;telogen as an emergent relaxation oscillator",
                  keywords=["hair follicle cycle", "anagen", "telogen", "androgenetic alopecia", "alopecia areata",
                            "telogen effluvium", "anagen effluvium", "hair loss", "relaxation oscillator", "VP theory"],
                  grades=["V", "L", "O"],
                  answer=("The hair follicle is the one skin structure that cycles autonomously, so it needs an oscillator, not a static switch. "
                          "Putting the same measured EDAR &gamma; on the same vendored relaxation oscillator yields an anagen-dominant cycle with no new constant; "
                          "four alopecias then follow as that one cycle driven off its set-point, telogen effluvium shedding exactly one telogen after the stressor."),
                  abstract_txt=("The hair-follicle cycle is reproduced as an emergent relaxation oscillator on the existing measured EDAR gamma; it is anagen-dominant with a plateau-then-collapse waveform, and four alopecias (androgenetic, areata, telogen effluvium, anagen effluvium) follow as signed perturbations with telogen effluvium shedding one telogen after the stressor, adding no constant and leaving the core battery hash unchanged."),
                  abstract=("The hair follicle &mdash; the one autonomously cycling integumentary structure &mdash; is reproduced as an emergent relaxation oscillator "
                            "on the <em>same</em> measured EDAR &gamma; that emerged the skin appendage, with no new fitted constant. The cycle is anagen-dominant with a "
                            "plateau-then-collapse waveform {V}; the absolute fraction and years-long period stay open {O}. Four alopecias follow as signed perturbations of "
                            "the one cycle &mdash; androgenetic (shortened anagen, reversed by minoxidil), areata (sustained anagen arrest with regrowth hysteresis), telogen "
                            "effluvium (a delayed self-limited shed exactly one telogen after the stressor), and anagen effluvium (an immediate shed bypassing telogen) &mdash; "
                            "passing an intervention-reversal battery and a three-way opposite-sign/opposite-timing discriminant, the layer adding no constant while the "
                            "core-battery hash stays fixed.").replace("{V}", grade_badge('V')).replace("{O}", grade_badge('O')),
                  body=body))

    # ---- 11 sebaceous-duct jamming (new measured organ; mirrors repro/_seb, separate hash) ----
    SB = D["seb"]
    prov = SB["_gamma_provenance"]; mech = SB["_mechanism"]
    acne = SB["acne_vulgaris"]; hs = SB["hidradenitis_suppurativa"]
    sebopp = SB["_opposite_sign_discriminant"]
    def _yn3(b): return "yes" if b else "no"
    _seb_dis_rows = [
        ("Acne vulgaris", "standing high net occlusion (sebum + hyperkeratinisation + <em>C. acnes</em>)",
         "drive past the upper spinodal &rarr; comedo; the <em>C. acnes</em> amplifier makes it inflammatory; comedolytic + sebostatic + antimicrobial reopens it"),
        ("Hidradenitis suppurativa", "the same jam in deeper apocrine-bearing follicles",
         "a heavier plug ruptures into the dermis &rarr; a scarring sinus-tract sub-state acne lacks; biologics de-inflame, deroofing/excision resets the scar"),
    ]
    _seb_dis_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b, c) in _seb_dis_rows)
    _sebopp_rows = [
        ("Reversibility", "superficial acne (drive-down reopens it)", "deep HS rupture (same drive-down leaves the scar)",
         sebopp["superficial_acne_reversible_vs_deep_hs_rupture_irreversible"]),
        ("Inflammatory sign", "with <em>C. acnes</em> (inflammatory)", "without <em>C. acnes</em> (comedonal, still jammed)",
         sebopp["inflammatory_with_cacnes_vs_comedonal_without"]),
        ("Plug depth", "hidradenitis suppurativa (heavier load)", "acne (lighter load)",
         sebopp["hs_deeper_plug_than_acne"]),
    ]
    _sebopp_html = "".join(f'<tr><td>{k}</td><td>{p}</td><td>{n}</td><td class="num">{_yn3(ok)}</td></tr>'
                           for (k, p, n, ok) in _sebopp_rows)
    body = f"""
<h2>The pilosebaceous duct is a channel that can jam shut &mdash; the package's own physical class</h2>
<p>The integumentary class is jamming: a barrier or channel driven past a spinodal by an external insult. The pilosebaceous duct is a textbook member the earlier targets did not cover &mdash; a follicular channel whose <strong>net occlusion drive</strong> (androgen-driven sebum, infundibular hyperkeratinisation and <em>Cutibacterium acnes</em>, minus clearance) can rise until the duct <strong>snaps shut into a comedo</strong>. This page emerges that duct as the <strong>same R19 jamming switch</strong> the barrier and wound pages use, running on a <strong>newly measured</strong> sebaceous master-gene &gamma; &mdash; <strong>PRDM1/Blimp1</strong>, the sebaceous-lineage master &mdash; with no constant fitted to a lesion.</p>
<table>
<thead><tr><th>Quantity</th><th>Value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Master gene (measured)</td><td class="num">PRDM1 &gamma; = {prov['gamma_vendored']}</td><td>fetched from NCBI, cached, vendored &mdash; the same promoter-&Delta;G pipeline that reproduces MITF/EDAR byte-for-byte</td></tr>
<tr><td>&gamma; reproduces offline</td><td class="num">{_yn3(prov['offline_reproduces'])}</td><td>recomputed from the cached promoter ({prov['gamma_from_cached_sequence']}) &mdash; not refitted</td></tr>
<tr><td>Spinodal</td><td class="num">{mech['spinodal']:.3f}</td><td>substrate-derived from &gamma; (sets the occlusion regime scale)</td></tr>
<tr><td>Healthy net occlusion</td><td class="num">{mech['healthy_net_occlusion']:.2f}</td><td>the healthy duct sits patent in the OFF basin ({_yn3(mech['healthy_patent'])})</td></tr>
</tbody></table>
{vp_card("Measured PRDM1 &gamma; (locked input)", "PRDM1 (Blimp1) is the committed sebaceous-gland lineage master. Its &gamma; is the proximal-promoter nearest-neighbour &Delta;G&#8323;&#8327; over the cached TSS&minus;2000..+500 window &mdash; the identical pipeline validated to reproduce the melanocyte (MITF) and appendage (EDAR) &gamma; byte-for-byte, so it is a measured input, never tuned. " + grade_badge('L'))}
<p>Committing the master gene on the biology <em>before</em> reading &gamma; is the discipline that makes the next result a prediction rather than a fit: PRDM1 turns out to carry the <strong>lowest &gamma; in the whole organ atlas</strong>, so its functional spinodal opens <em>earliest</em>. The substrate therefore predicts the sebaceous programme is among the first to become switchable &mdash; an emergence-order statement graded by <em>sign</em> {grade_badge('V')}, not chosen to land anywhere.</p>

<h2>The duct is a hysteretic two-state jam, not a reversible threshold</h2>
<p>Run as the R19 switch, the duct does not drift smoothly from open to closed. As the net occlusion rises it stays patent, then <strong>snaps shut discontinuously</strong> at the upper spinodal (a jump of about <strong>{mech['up_jump_magnitude']:.2f}</strong> at net occlusion &asymp; <strong>{mech['occ_jam_up']:.2f}</strong>); coming back down it does <em>not</em> reopen at the same level but only at a <strong>lower</strong> spinodal (net occlusion &asymp; <strong>{mech['occ_clear_down']:.2f}</strong>), tracing a hysteresis loop of width about <strong>{mech['hysteresis_width']:.2f}</strong>. Discontinuous closure ({_yn3(mech['jams_discontinuously'])}) and a finite hysteresis loop ({_yn3(mech['hysteretic'])}) are the signature of a first-order jam &mdash; the simulation-verified core {grade_badge('V')} of this page, taken straight from the substrate with nothing tuned. The clinical reading is immediate: a comedo, once formed, does not clear the moment the drive eases slightly &mdash; it has to be pushed back below a distinctly lower threshold, which is why effective therapy attacks several occlusion inputs at once.</p>
{vp_card("Pilosebaceous-occlusion anchor (cited)", "Acne and hidradenitis suppurativa are diseases of follicular occlusion: sebum, infundibular hyperkeratinisation and the follicular microbiome plug the duct, and the established treatments lower exactly those inputs. " + grade_badge('L'))}
<p>The package is explicit about what it does <em>not</em> claim. The hysteresis <em>shape</em> &mdash; discontinuity, the loop, the patent set-point &mdash; is verified {grade_badge('V')}; the occlusion set-points themselves are dimensionless regime scales {grade_badge('F')}. The <strong>absolute</strong> comedo and lesion counts, the Hurley-stage extent and the sebum excretion rate remain open {grade_badge('O')}, inheriting the new sebaceous target's standing obstacle &mdash; a per-gland calibration. The duct is graded on direction, discontinuity, hysteresis and reversibility, never on a fitted magnitude.</p>

<h2>Two occlusion diseases are this one jam at two depths</h2>
<p>With the jam established, acne vulgaris and hidradenitis suppurativa follow as the <em>same</em> switch driven to two different depths, and each established therapy is the same occlusion drive reversed &mdash; no new physics between them.</p>
<table>
<thead><tr><th>Disease</th><th>Occlusion handle</th><th>Covered as</th></tr></thead>
<tbody>
{_seb_dis_html}
</tbody></table>

<h2>Acne vulgaris: a standing occlusion drives the duct over the spinodal</h2>
<p>Acne is a <strong>standing elevated occlusion drive</strong>: androgen-driven sebum plus infundibular hyperkeratinisation plus the <em>C. acnes</em> amplifier carry the net occlusion to about <strong>{acne['disease_net_occlusion']:.2f}</strong>, past the upper spinodal, so the duct jams into a comedo ({_yn3(acne['disease_jammed'])}) and the <em>C. acnes</em> amplifier makes the lesion <strong>inflammatory</strong> ({_yn3(acne['inflammatory'])}). The therapeutic structure falls straight out of the hysteresis: a single agent that only nudges the drive is often <em>insufficient</em> (retinoid monotherapy clears: {_yn3(acne['monotherapy_clears'])}), because the duct must be driven below the <em>lower</em> spinodal &mdash; but a combined comedolytic + sebostatic + antimicrobial regimen (or isotretinoin) does exactly that and the duct reopens ({_yn3(acne['full_regimen_clears'])}). Treating only the inflammation leaves the duct mechanically jammed but non-inflammatory (still jammed: {_yn3(acne['deinflamed_still_jammed'])}) &mdash; the comedonal residue the clinic knows well.</p>
{vp_card("Acne vulgaris anchor (cited)", "Acne vulgaris is a pilosebaceous disorder of follicular occlusion, excess sebum, <em>C. acnes</em> and inflammation; retinoids, hormonal/isotretinoin sebostatics and antimicrobials are the effective levers. " + grade_badge('L'))}

<h2>Hidradenitis suppurativa: the same jam deeper, with an irreversible rupture branch</h2>
<p>Hidradenitis suppurativa is the <strong>same occlusion jam in deeper apocrine-gland-bearing follicles</strong>, driven heavier (net occlusion about <strong>{hs['disease_net_occlusion']:.2f}</strong>) so the plug reaches a load at which it <strong>ruptures into the dermis</strong> instead of extruding ({_yn3(hs['ruptured_deep_branch'])}) &mdash; a chronic scarring sinus-tract sub-state the superficial comedo never reaches. This produces the page's sharpest clinical contrast: dropping the occlusion drive all the way down to the same sub-acne level that <em>clears</em> acne ({_yn3(hs['acne_would_clear_here'])} &mdash; the jam itself would open) still leaves the ruptured tract in place ({_yn3(hs['scar_persists_on_drive_down'])}). So an anti-inflammatory biologic calms the active disease but cannot reopen a structural scar; only physical reset &mdash; deroofing or excision &mdash; resolves the tract ({_yn3(hs['surgical_resolves'])}). The same drive-down, opposite outcome, is the substrate's clean account of why isotretinoin clears acne but not established hidradenitis tracts.</p>
{vp_card("Hidradenitis suppurativa anchor (cited)", "Hidradenitis suppurativa is a chronic follicular-occlusion disease of apocrine-bearing skin with rupture, sinus tracts and scarring; biologics (anti-TNF/IL-17) reduce inflammation and deroofing/excision treats established tracts. " + grade_badge('L'))}

<h2>The discriminant: opposite occlusion modes from one jam</h2>
<p>As with the static diseases and the hair cycle, the decisive evidence is that clinically opposite behaviours fall out of the <em>same</em> jam driven differently, with no constant changed between them.</p>
<table>
<thead><tr><th>Axis</th><th>One pole</th><th>Opposite pole</th><th>Reproduced</th></tr></thead>
<tbody>
{_sebopp_html}
</tbody></table>
<p>All three opposite pairs reproduce ({_yn3(sebopp['all_opposite_pairs_reproduced'])}). That one occlusion switch yields a reversible superficial comedo and an irreversible deep sinus tract, an inflammatory and a comedonal lesion, and a lighter and a heavier plug &mdash; from occlusion depth and the <em>C. acnes</em> amplifier alone, on a single measured PRDM1 &gamma; with no new parameter &mdash; is the strongest internal evidence that these occlusion diseases are jamming dynamics, not bespoke fits.</p>

<h2>Grades and reproducibility</h2>
<p>Every mechanism here is a simulation-verified shape or sign {grade_badge('V')} &mdash; discontinuous closure, the hysteresis loop, the patent set-point, the comedo direction, the reopening on reversed knobs, the deep rupture branch and its drive-down irreversibility. Every clinical mapping rests on a cited anchor {grade_badge('L')}. The occlusion set-points are forced regime scales {grade_badge('F')}. Every absolute magnitude is open {grade_badge('O')} &mdash; comedo and lesion counts, Hurley-stage extent, sebum excretion rate &mdash; inheriting the sebaceous target's obstacle (a per-gland calibration). No disease introduces a new constant; each is a named perturbation of the one jam.</p>
<p>The sebaceous pipeline is deterministic on its own terms: two independent runs hash to an identical SHA-256, separate from the core battery, the pathology layer and the hair-cycle layer. Crucially, adding this organ does <strong>not</strong> touch the core T1&ndash;T5+oncology battery, whose result hash is unchanged at <code>{esc(D['sha'][:12])}&hellip;</code>.</p>
{vp_card("Sebaceous result SHA-256 (determinism)", f"<code>{esc(D['seb_sha'])}</code><br>The C1 reproducibility gate for the sebaceous layer, identical across independent processes and distinct from the core, pathology and hair-cycle hashes. Reproduce with <code>python repro/run_seb.py</code>.")}
"""
    S.append(dict(no="11", slug="11-sebaceous-duct-jamming-acne",
                  short="Sebaceous duct", title="The sebaceous duct: follicular occlusion as a hysteretic jam, with acne and hidradenitis suppurativa",
                  h1="The sebaceous duct: pilosebaceous occlusion as a hysteretic jamming switch",
                  keywords=["sebaceous gland", "pilosebaceous duct", "follicular occlusion", "comedo", "acne vulgaris",
                            "hidradenitis suppurativa", "PRDM1", "Blimp1", "isotretinoin", "jamming transition", "VP theory"],
                  grades=["V", "F", "L", "O"],
                  answer=("The pilosebaceous duct is a channel that jams shut when its net occlusion drive crosses a spinodal. "
                          "Putting a newly measured PRDM1 &gamma; on the same R19 switch yields a hysteretic comedo with no fitted constant; "
                          "acne and hidradenitis suppurativa then follow as that one jam at two depths, the deep tract rupturing irreversibly."),
                  abstract_txt=("The pilosebaceous duct is reproduced as a hysteretic two-state occlusion jam on a newly measured PRDM1 (Blimp1) gamma carried through the same promoter-deltaG pipeline as the other organs; it snaps shut discontinuously at an upper spinodal and reopens only at a lower one, and acne vulgaris and hidradenitis suppurativa follow as that one jam at two depths, with the deep ruptured tract irreversible to drive reduction, adding no constant and leaving the core battery hash unchanged."),
                  abstract=("The pilosebaceous duct &mdash; a follicular channel that occludes into a comedo &mdash; is reproduced as a hysteretic two-state "
                            "jam on the <em>same</em> R19 switch as the barrier and wound, running on a <strong>newly measured</strong> PRDM1/Blimp1 &gamma; carried through the "
                            "identical promoter-&Delta;G pipeline that reproduces MITF and EDAR byte-for-byte. The duct snaps shut discontinuously at an upper spinodal and "
                            "reopens only at a lower one {V}; the occlusion set-points are forced regime scales {F} and absolute lesion counts stay open {O}. Acne vulgaris "
                            "(reversible comedo, cleared by a combined regimen) and hidradenitis suppurativa (a deeper jam whose ruptured sinus tract resists drive reduction "
                            "and needs surgery) follow as the one jam at two depths, passing an intervention-reversal battery and a three-way opposite-mode discriminant, the "
                            "layer adding no constant while the core-battery hash stays fixed.").replace("{V}", grade_badge('V')).replace("{F}", grade_badge('F')).replace("{O}", grade_badge('O')),
                  body=body))

    # ---- 12 cell-adhesion blistering (new target on the EXISTING measured KRT14 gamma; mirrors repro/_adhesion, separate hash) ----
    AD = D["adh"]
    amech = AD["_mechanism"]; aprov = AD["_gamma_provenance"]
    pv = AD["pemphigus_vulgaris"]; bp = AD["bullous_pemphigoid"]
    aopp = AD["_opposite_sign_discriminant"]
    def _yna(b): return "yes" if b else "no"
    _ad_dis_rows = [
        ("Pemphigus vulgaris", "anti-desmoglein-3 (DSG3) &mdash; the <strong>cell-cell</strong> (desmosomal) compartment",
         "drives lateral cohesion below the spinodal &rarr; an intraepidermal (suprabasal) split with the cell-matrix bond intact (basal 'tombstone' row); clearing the antibody re-adheres it"),
        ("Bullous pemphigoid", "anti-BP180 (COL17A1) &mdash; the <strong>cell-matrix</strong> (hemidesmosomal) compartment",
         "drives basal anchoring below the spinodal &rarr; a subepidermal split with the cell-cell bonds intact (epidermis lifts whole); clearing the antibody re-adheres it"),
    ]
    _ad_dis_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b, c) in _ad_dis_rows)
    _aopp_rows = [
        ("Cleavage plane", "intraepidermal / suprabasal (pemphigus vulgaris)", "subepidermal / junctional (bullous pemphigoid)",
         aopp["intraepidermal_pv_vs_subepidermal_bp"]),
        ("Nikolsky sign", "positive (pemphigus vulgaris)", "negative (bullous pemphigoid)",
         aopp["nikolsky_positive_pv_vs_negative_bp"]),
        ("Blister tension", "flaccid (pemphigus vulgaris)", "tense (bullous pemphigoid)",
         aopp["flaccid_pv_vs_tense_bp"]),
    ]
    _aopp_html = "".join(f'<tr><td>{k}</td><td>{p}</td><td>{n}</td><td class="num">{_yna(ok)}</td></tr>'
                         for (k, p, n, ok) in _aopp_rows)
    body = f"""
<h2>Cell adhesion is a binding jam &mdash; the same physical class, on an organ already in the atlas</h2>
<p>Desmosomes and hemidesmosomes anchor the keratinocyte's keratin network to its neighbours and to the basement membrane; that junctional adhesion is what holds the epidermis together as a sheet. In this framework adhesion is not a new organ &mdash; it is an <strong>intrinsic property of the keratinocyte</strong>, so it runs on the <strong>already-measured KRT14 &gamma;</strong> with <strong>no new &gamma; fetched and none fitted</strong> (the hair-cycle pattern of a new target on an existing organ, not the sebaceous pattern of a new measured organ). A bond is a member of the package's jamming class read the natural way round: <strong>adherent = jammed ON</strong> (s&gt;0), <strong>blistered = unjammed OFF</strong> (s&lt;0). An autoantibody is a de-adhesive drive, and <em>which compartment</em> it targets is the only thing that changes between the two classic autoimmune blistering diseases.</p>
<table>
<thead><tr><th>Quantity</th><th>Value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Master gene (reused, measured)</td><td class="num">KRT14 &gamma; = {aprov['gamma']}</td><td>the keratinocyte &gamma; already vendored for the barrier and turnover pages &mdash; adhesion is intrinsic to this organ</td></tr>
<tr><td>New &gamma; fetched</td><td class="num">{_yna(aprov['new_gamma_fetched'])}</td><td>no NCBI fetch and no fit &mdash; only a new dynamical target on the existing measured &gamma;</td></tr>
<tr><td>Spinodal</td><td class="num">{amech['spinodal']:.4f}</td><td>substrate-derived from the same &gamma; (sets the de-adhesion regime scale)</td></tr>
<tr><td>Healthy net adhesion</td><td class="num">{amech['healthy_net_adhesion']:.2f}</td><td>the healthy bond sits ABOVE the upper spinodal, robustly adherent ({_yna(amech['healthy_adherent'])})</td></tr>
</tbody></table>
{vp_card("Measured KRT14 &gamma; (reused locked input)", "KRT14 is the keratinocyte master gene; its &gamma; was measured once, from the cached proximal-promoter &Delta;G, and is reused read-only here. Because desmosomal and hemidesmosomal adhesion anchor the very keratin network KRT14 builds, the bond is a property of this organ &mdash; reusing its &gamma; rather than introducing a new constant is the honest move. " + grade_badge('L'))}
<p>Acquired autoimmune blistering is keyed by <em>dynamics</em> &mdash; a de-adhesive drive on an intact bond &mdash; and is reproduced here. Its congenital mirror, epidermolysis bullosa, is keyed by a <em>defective adhesion gene</em> (KRT14, COL17A1, LAMB3) and belongs to the gene-lesion disease registry, not to this dynamical layer; naming that boundary keeps each disease where its mechanism actually lives.</p>

<h2>Adhesion is a hysteretic two-state bond, not a graded weakening</h2>
<p>Run as the R19 switch, the bond does not soften smoothly as the de-adhesive drive rises. It stays firmly adherent, then <strong>detaches discontinuously</strong> at the lower spinodal (a jump of about <strong>{amech['detach_jump_magnitude']:.2f}</strong> at net adhesion &asymp; <strong>{amech['adh_detach_down']:.3f}</strong>); restoring adhesion does <em>not</em> re-anneal at the same level but only at a <strong>higher</strong> spinodal (net adhesion &asymp; <strong>{amech['adh_readhere_up']:.3f}</strong>), tracing a hysteresis loop of width about <strong>{amech['hysteresis_width']:.2f}</strong>. Discontinuous detachment ({_yna(amech['detaches_discontinuously'])}) and a finite loop ({_yna(amech['hysteretic'])}) are the first-order signature &mdash; the simulation-verified core {grade_badge('V')} of this page, taken straight from the substrate with nothing tuned. The clinical reading is immediate: a blister, once raised, does not reseal the moment the antibody titre eases a little; the bond has to be carried back above a distinctly higher threshold, which is why a partial reduction in titre leaves disease active and only substantial clearance re-adheres.</p>
{vp_card("Autoimmune-bullous anchor (cited)", "Pemphigus and pemphigoid are antibody-mediated diseases in which an autoantibody against a specific adhesion molecule detaches keratinocytes, and lowering the antibody burden (rituximab, corticosteroids, immunosuppression) is what controls them. " + grade_badge('L'))}
<p>The page is explicit about what it does <em>not</em> claim. The hysteresis <em>shape</em> &mdash; discontinuity, the loop, the adherent set-point, and the plane/sign selection below &mdash; is verified {grade_badge('V')}; the adhesion reserve and the antibody titres are dimensionless regime scales {grade_badge('F')}; the clinical mappings are cited anchors {grade_badge('L')}. The <strong>absolute</strong> blister counts, the antibody titre in IU/mL, the cleavage depth in microns and the involved body-surface area remain open {grade_badge('O')}, inheriting the adhesion target's obstacle &mdash; a per-junction calibration. The bond is graded on direction, discontinuity, hysteresis, plane and sign, never on a fitted magnitude.</p>

<h2>Two blistering diseases are one switch hit in two compartments</h2>
<p>Adhesion runs in two coupled compartments on the <em>same</em> &gamma; and the <em>same</em> spinodal: cell-cell (desmosomal, DSG3) and cell-matrix (hemidesmosomal, BP180/COL17A1). An autoantibody of the <em>same magnitude</em> detaches whichever compartment it is specific for &mdash; and that single choice is the entire difference between the two diseases.</p>
<table>
<thead><tr><th>Disease</th><th>Autoantibody &amp; compartment</th><th>Covered as</th></tr></thead>
<tbody>
{_ad_dis_html}
</tbody></table>

<h2>Pemphigus vulgaris: the cell-cell bond detaches, splitting within the epidermis</h2>
<p>An anti-DSG3 autoantibody drives the <strong>cell-cell</strong> (desmosomal) compartment below the spinodal, so keratinocytes lose lateral cohesion ({_yna(pv['cellcell_separated'])}) while the untouched cell-matrix bond keeps basal cells anchored ({_yna(pv['cellmatrix_adherent'])}). The split is therefore <strong>{esc(pv['cleavage_plane'].replace('_', ' '))}</strong> &mdash; suprabasal, leaving the basal 'tombstone' row &mdash; and because the failing bond <em>is</em> the lateral cell-cell bond, a tangential shear propagates the separation, so the <strong>Nikolsky sign is positive</strong> ({_yna(pv['nikolsky_positive'])}); the thin suprabasal roof gives a <strong>flaccid</strong> blister ({_yna(pv['blister_flaccid'])}). The Nikolsky sign is <em>derived</em> from which compartment failed, not asserted. Reversal follows the hysteresis exactly: a partial titre reduction does <em>not</em> re-adhere ({_yna(pv['partial_immunosuppression_readheres'])}), but clearing the antibody (rituximab / immunosuppression) carries net adhesion back above the spinodal and the bond re-adheres ({_yna(pv['cleared_readheres'])}).</p>
{vp_card("Pemphigus vulgaris anchor (cited)", "Pemphigus vulgaris is an anti-desmoglein (DSG1/DSG3) disease with suprabasal acantholysis, flaccid bullae and a positive Nikolsky sign; rituximab and systemic immunosuppression are effective. " + grade_badge('L'))}

<h2>Bullous pemphigoid: the cell-matrix bond detaches, lifting the epidermis whole</h2>
<p>An anti-BP180 (COL17A1) autoantibody of the <em>same magnitude</em> instead drives the <strong>cell-matrix</strong> (hemidesmosomal) compartment below the spinodal, so basal keratinocytes detach from the dermo-epidermal junction ({_yna(bp['cellmatrix_separated'])}) while the untouched cell-cell bonds hold the epidermis together as a cohesive sheet ({_yna(bp['cellcell_adherent'])}). The split is now <strong>{esc(bp['cleavage_plane'].replace('_', ' '))}</strong> &mdash; the whole epidermis lifts as an intact roof &mdash; and because the failing bond is the basal cell-matrix bond and <em>not</em> the lateral one, a tangential shear does not propagate, so the <strong>Nikolsky sign is negative</strong> ({_yna(bp['nikolsky_negative'])}); the full-thickness roof gives a <strong>tense</strong> blister ({_yna(bp['blister_tense'])}). Reversal is again hysteretic: a partial reduction does not re-adhere ({_yna(bp['partial_immunosuppression_readheres'])}), while clearing/suppressing the antibody (corticosteroid / immunosuppression) re-adheres the bond ({_yna(bp['cleared_readheres'])}).</p>
{vp_card("Bullous pemphigoid anchor (cited)", "Bullous pemphigoid is an anti-BP180/BP230 (hemidesmosomal) disease with a subepidermal split, tense bullae and a negative Nikolsky sign; corticosteroids and immunosuppression are the mainstay. " + grade_badge('L'))}

<h2>The discriminant: opposite blistering properties from one switch, one spinodal, one antibody magnitude</h2>
<p>The decisive evidence is the same as for the static diseases, the hair cycle and the sebaceous duct: clinically opposite behaviours fall out of the <em>same</em> jam &mdash; here not even driven to different depths, but driven in different <em>compartments</em> at the <em>same</em> antibody magnitude. Nothing is changed between the two diseases except which bond the antibody is specific for.</p>
<table>
<thead><tr><th>Axis</th><th>One pole</th><th>Opposite pole</th><th>Reproduced</th></tr></thead>
<tbody>
{_aopp_html}
</tbody></table>
<p>All three opposite pairs reproduce ({_yna(aopp['all_opposite_pairs_reproduced'])}). That one adhesion switch yields an intraepidermal versus a subepidermal plane, a positive versus a negative Nikolsky sign, and a flaccid versus a tense blister &mdash; from the <em>compartment</em> alone, on a single reused KRT14 &gamma; with no new parameter and the same antibody magnitude &mdash; is the strongest internal evidence that these blistering diseases are adhesion-jamming dynamics, not bespoke fits.</p>

<h2>Grades and reproducibility</h2>
<p>Every mechanism here is a simulation-verified shape or sign {grade_badge('V')} &mdash; discontinuous detachment, the hysteresis loop, the adherent set-point, the plane selection, the derived Nikolsky sign, the blister-tension direction and the re-adhesion on antibody clearance. Every clinical mapping rests on a cited anchor {grade_badge('L')}. The adhesion reserve and antibody titres are forced regime scales {grade_badge('F')}. Every absolute magnitude is open {grade_badge('O')} &mdash; blister counts, titre in IU/mL, cleavage depth, body-surface area &mdash; inheriting the adhesion target's obstacle (a per-junction calibration). No disease introduces a new constant; each is a signed de-adhesion of the one bond, and no new &gamma; is fetched.</p>
<p>The adhesion pipeline is deterministic on its own terms: two independent runs hash to an identical SHA-256, separate from the core battery, the pathology layer, the hair-cycle layer and the sebaceous layer. Crucially, adding this target does <strong>not</strong> touch the core T1&ndash;T5+oncology battery, whose result hash is unchanged at <code>{esc(D['sha'][:12])}&hellip;</code>.</p>
{vp_card("Adhesion result SHA-256 (determinism)", f"<code>{esc(D['adh_sha'])}</code><br>The C1 reproducibility gate for the adhesion layer, identical across independent processes and distinct from the core, pathology, hair-cycle and sebaceous hashes. Reproduce with <code>python repro/run_adhesion.py</code>.")}
"""
    S.append(dict(no="12", slug="12-cell-adhesion-blistering",
                  short="Cell adhesion", title="Cell adhesion as a hysteretic binding jam: pemphigus vulgaris and bullous pemphigoid",
                  h1="Cell adhesion as a hysteretic binding jam: autoimmune blistering",
                  keywords=["cell adhesion", "desmosome", "hemidesmosome", "keratinocyte", "KRT14", "pemphigus vulgaris",
                            "bullous pemphigoid", "DSG3", "BP180", "Nikolsky sign", "acantholysis", "jamming transition", "VP theory"],
                  grades=["V", "F", "L", "O"],
                  answer=("Autoimmune blistering is cell adhesion losing its jam. Putting the already-measured KRT14 &gamma; on the same R19 switch makes "
                          "junctional adhesion a hysteretic two-state bond &mdash; adherent when jammed ON, blistered when an autoantibody drives it OFF. "
                          "Pemphigus vulgaris and bullous pemphigoid then differ only by which compartment the antibody hits, flipping the cleavage plane, "
                          "the Nikolsky sign and the blister tension with no fitted constant."),
                  abstract_txt=("Cell-cell and cell-matrix adhesion are reproduced as a hysteretic two-state binding jam on the already-measured keratinocyte KRT14 gamma "
                                "(no new gamma fetched, none fitted): adhesion snaps from adherent to detached at a spinodal and re-adheres only at a higher one, and "
                                "pemphigus vulgaris (anti-DSG3, cell-cell) and bullous pemphigoid (anti-BP180, cell-matrix) follow as the same switch hit by the same antibody "
                                "magnitude in different compartments, which flips the cleavage plane, the Nikolsky sign and the blister tension, adding no constant and leaving the core battery hash unchanged."),
                  abstract=("Junctional cell adhesion &mdash; the desmosomal and hemidesmosomal bonds that hold the epidermis together &mdash; is reproduced as a hysteretic "
                            "two-state binding jam on the <em>same</em> R19 switch as the barrier and wound, running on the <strong>already-measured</strong> keratinocyte KRT14 &gamma; "
                            "with <strong>no new &gamma; fetched and none fitted</strong>. The bond detaches discontinuously at a lower spinodal and re-adheres only at a higher one {V}; "
                            "the adhesion reserve and antibody titres are forced regime scales {F}, the clinical mappings are cited anchors {L}, and absolute blister counts and titres stay open {O}. "
                            "Pemphigus vulgaris (anti-DSG3, the cell-cell compartment) and bullous pemphigoid (anti-BP180, the cell-matrix compartment) follow as the <em>same</em> switch hit by the "
                            "<em>same</em> antibody magnitude in different compartments, passing an intervention-reversal battery and a three-axis opposite-property discriminant &mdash; intraepidermal vs "
                            "subepidermal plane, positive vs negative Nikolsky sign, flaccid vs tense blister &mdash; the layer adding no constant while the core-battery hash stays fixed."
                            ).replace("{V}", grade_badge('V')).replace("{F}", grade_badge('F')).replace("{L}", grade_badge('L')).replace("{O}", grade_badge('O')),
                  body=body))

    # ---- 13 neurovascular reactivity (new target on the EXISTING measured EDAR gamma; mirrors repro/_vasomotor, separate hash) ----
    VA = D["vaso"]
    vmech = VA["_mechanism"]; vprov = VA["_gamma_provenance"]; vseam = VA["_seam_note"]
    ros = VA["rosacea"]; ray = VA["raynaud_phenomenon"]
    vopp = VA["_opposite_sign_discriminant"]
    def _ynv(b): return "yes" if b else "no"
    _va_dis_rows = [
        ("Rosacea", "a standing <strong>vasodilator reactivity</strong> drive (lowered flush threshold; heat / alcohol / ultraviolet / spice)",
         "carries the net dilator drive above the upper spinodal &rarr; the vessel locks dilated (fixed erythema/telangiectasia); the LL-37/Demodex amplifier on the same dilated background gives the papulopustular subtype; anti-inflammatories clear the papules, brimonidine blanches transiently, laser resets the fixed vessels"),
        ("Raynaud phenomenon", "a cold / stress <strong>vasoconstrictor</strong> drive",
         "carries the net dilator drive negative into the constricted/ischemic basin &rarr; a reversible white-blue-red digital vasospastic attack (it crosses no lock); rewarming and a vasodilator / calcium-channel blocker abort it; the fixed digital-ischemia / ulcer state is the secondary (connective-tissue-disease) seam"),
    ]
    _va_dis_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for (a, b, c) in _va_dis_rows)
    _vopp_rows = [
        ("Direction", "vasodilation (rosacea: drive above the upper spinodal)", "vasoconstriction (Raynaud: drive negative into the constricted basin)",
         vopp["vasodilation_rosacea_vs_vasoconstriction_raynaud"]),
        ("Reversibility", "fixed telangiectasia (rosacea: the drive crosses the upper lock)", "reversible vasospasm (primary Raynaud: stays short of the lock)",
         vopp["fixed_telangiectasia_vs_reversible_vasospasm"]),
        ("Vascular vs inflammatory", "erythematotelangiectatic (vascular, the dilation/fixation story)", "papulopustular (the inflammatory LL-37/Demodex amplifier)",
         vopp["vascular_ery_telangiectatic_vs_inflammatory_papulopustular"]),
    ]
    _vopp_html = "".join(f'<tr><td>{k}</td><td>{p}</td><td>{n}</td><td class="num">{_ynv(ok)}</td></tr>'
                         for (k, p, n, ok) in _vopp_rows)
    body = f"""
<h2>Vasomotor tone is a reactivity jam &mdash; the same physical class, on the thermoregulation-interface organ</h2>
<p>Every disease so far has lived on a barrier, a bond, a duct or a cycle. Rosacea lives on the <strong>cutaneous vasculature's reactivity</strong>, and the core battery had no vasomotor target &mdash; which is exactly why rosacea was held back as not-yet-modelable. This page adds that target without a new organ and without a fitted constant: it puts the <strong>already-measured EDAR &gamma; = {vmech['gamma']}</strong> &mdash; the organ the atlas labels the <em>thermoregulation interface</em> &mdash; onto the <strong>same R19 switch</strong> as the barrier and wound, and reads vasomotor tone off it. The justification is anatomical: the cutaneous thermoregulatory interface has <strong>two autonomic effector arms</strong> &mdash; the <strong>sudomotor</strong> arm (sweat glands, the T5 target and the hyperhidrosis/HED diseases) and the <strong>vasomotor</strong> arm (skin blood flow, flushing). Rosacea is a dysregulation of the vasomotor arm &mdash; the <strong>vascular mirror of hyperhidrosis</strong> on the sudomotor arm &mdash; so it is intrinsic to this same organ. A vessel is read as a member of the package's jamming class the natural way round: <strong>dilated = jammed ON</strong> (s&gt;0, flushed), <strong>constricted = OFF</strong> (s&lt;0, quiescent/ischemic).</p>
<table>
<thead><tr><th>Quantity</th><th>Value</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>Master gene (reused, measured)</td><td class="num">EDAR &gamma; = {vprov['gamma']}</td><td>the appendage / thermoregulation-interface &gamma; already vendored for the sweat (T5) and hair-cycle pages &mdash; the vasomotor arm is intrinsic to this organ</td></tr>
<tr><td>New &gamma; fetched</td><td class="num">{_ynv(vprov['new_gamma_fetched'])}</td><td>no NCBI fetch and no fit &mdash; only a new dynamical target on the existing measured &gamma; (the hair-cycle / adhesion pattern)</td></tr>
<tr><td>Spinodal</td><td class="num">{vmech['spinodal']:.4f}</td><td>substrate-derived from the same &gamma; (sets the reactivity regime scale)</td></tr>
<tr><td>Healthy net vasodilator drive</td><td class="num">{vmech['healthy_net_vasodilator']:.2f}</td><td>the healthy vessel sits in the reversible middle, responsive and locked neither way ({_ynv(vmech['healthy_responsive'])})</td></tr>
</tbody></table>
{vp_card("Measured EDAR &gamma; (reused locked input)", "EDAR is the skin-appendage master gene; its &gamma; was measured once, from the cached proximal-promoter &Delta;G, and is reused read-only here. Because the cutaneous thermoregulatory interface it governs carries both the sudomotor (sweat) and the vasomotor (blood-flow) arms, the vasomotor reactivity is a property of this organ &mdash; reusing its &gamma; rather than introducing a new constant is the honest move. " + grade_badge('L'))}
<p>The dermal-perfusion <em>magnitude</em> is <strong>not</strong> re-derived here &mdash; it stays an <strong>inherited circulatory citation</strong> (a seam variable the package imports, never re-emerges). This target adds <em>only</em> the vasomotor <strong>reactivity dynamics</strong> the rosacea handoff said was missing: a reactivity threshold and a hysteretic fixation. Naming that seam keeps the vascular magnitude where it lives (the circulatory package) while the reactivity dynamics lives here.</p>

<h2>Vasomotor tone is a hysteretic two-lock switch, not a graded dial</h2>
<p>Run as the R19 switch, the vessel does not drift smoothly from dilated to constricted. It <strong>locks dilated discontinuously</strong> once the net dilator drive exceeds the <strong>upper</strong> spinodal (a jump of about <strong>{vmech['dilate_jump_magnitude']:.2f}</strong> at net drive &asymp; <strong>{vmech['v_dilate_lock_up']:.3f}</strong>), and <strong>locks constricted discontinuously</strong> once it falls below the <strong>lower</strong> spinodal (a jump of about <strong>{vmech['constrict_jump_magnitude']:.2f}</strong> at net drive &asymp; <strong>{vmech['v_constrict_lock_down']:.3f}</strong>), tracing a hysteresis loop of width about <strong>{vmech['hysteresis_width']:.2f}</strong>. Discontinuous locking ({_ynv(vmech['locks_discontinuously'])}) and a finite loop ({_ynv(vmech['hysteretic'])}) are the first-order signature &mdash; the simulation-verified core {grade_badge('V')} of this page, taken straight from the substrate with nothing tuned. Between the locks the vessel is <strong>reversibly responsive</strong>: it flushes with heat and constricts with cold and returns, crossing no lock. The clinical reading is immediate: an early flush comes and goes, but once a <em>sustained</em> drive carries the vessel past the upper lock the dilation is <strong>fixed</strong> &mdash; which is why telangiectasia does not fade when the trigger is removed, and why a partial vasoconstrictor blanches without resetting it.</p>
{vp_card("Neurovascular-reactivity anchor (cited)", "Rosacea is a chronic neurovascular / inflammatory facial disorder in which triggered flushing progresses to persistent centrofacial erythema and telangiectasia and to inflammatory papules and pustules; brimonidine gives transient vasoconstriction, anti-inflammatories treat the papulopustular subtype, and laser / intense-pulsed-light treats fixed telangiectasia. " + grade_badge('L'))}
<p>The page is explicit about what it does <em>not</em> claim. The hysteresis <em>shape</em> &mdash; the two discontinuous locks, the loop, the responsive middle, and the lock rule below &mdash; is verified {grade_badge('V')}; the resting tone, the reactivity gains and the trigger/constrictor drives are dimensionless regime scales {grade_badge('F')}; the clinical mappings are cited anchors {grade_badge('L')}. The <strong>absolute</strong> erythema index, vessel density, flush magnitude, digital temperature, attack frequency and involved body-surface area remain open {grade_badge('O')}, inheriting the vasomotor target's obstacle &mdash; a per-vessel calibration, with the perfusion magnitude itself an inherited circulatory seam. The vessel is graded on direction, discontinuity, hysteresis and the lock rule, never on a fitted magnitude.</p>

<h2>Two vasomotor diseases are one switch driven in opposite directions</h2>
<p>With the reactivity jam established, rosacea and Raynaud phenomenon follow as the <em>same</em> switch driven with <em>opposite</em> signs, and each established therapy is the same drive reversed &mdash; no new physics between them.</p>
<table>
<thead><tr><th>Disease</th><th>Drive (knob moved)</th><th>Covered as</th></tr></thead>
<tbody>
{_va_dis_html}
</tbody></table>

<h2>Rosacea: a standing dilator drive locks the vessel dilated</h2>
<p>Rosacea is a <strong>standing vasodilator reactivity</strong> drive &mdash; a lowered flush threshold under heat, alcohol, ultraviolet and spice. Early on, a transient flush is a sub-lock excursion that still <strong>returns</strong> ({_ynv(ros['transient_flush_returns'])}); but a sustained drive carries the net dilator drive past the upper spinodal, so the vessel <strong>locks dilated</strong> ({_ynv(ros['fixed_dilated'])}) and the dilation is <strong>fixed</strong> &mdash; persistent erythema and telangiectasia ({_ynv(ros['telangiectasia_fixed'])}, dilation depth {ros['dilation_depth']:.2f}). The cathelicidin LL-37 / Demodex inflammatory amplifier on the same dilated background gives the <strong>papulopustular</strong> subtype ({_ynv(ros['papulopustular_inflammatory'])}). The therapeutic structure falls straight out of the hysteresis: anti-inflammatory therapy (metronidazole / ivermectin / azelaic acid / doxycycline) clears the papules ({_ynv(ros['antiinflammatory_clears_papules'])}) but leaves the vascular background ({_ynv(ros['vascular_background_persists'])}); a vasoconstrictor (brimonidine) blanches the skin transiently but, because a partial constrictor leaves the net drive above the lower lock, it does <strong>not</strong> reset the fixed vessels ({_ynv(ros['brimonidine_blanches_but_no_reset'])} &mdash; still dilated); only <strong>laser / intense-pulsed-light</strong> physically resets the telangiectasia ({_ynv(ros['laser_resets_fixed_telangiectasia'])}), a structural reset exactly like deroofing for a hidradenitis tract.</p>
{vp_card("Rosacea anchor (cited)", "Rosacea presents as erythematotelangiectatic disease (triggered flushing, persistent erythema, telangiectasia) and papulopustular disease (inflammatory papules and pustules); brimonidine gives transient vasoconstriction, topical/oral anti-inflammatories treat the papulopustular subtype, and vascular laser treats fixed telangiectasia. " + grade_badge('L'))}

<h2>Raynaud phenomenon: the opposite drive, and a reversible attack</h2>
<p>Raynaud phenomenon is the <strong>opposite sign</strong> on the same switch: a cold or stress <strong>vasoconstrictor</strong> drive carries the net dilator drive negative, deepening the vessel into the constricted/ischemic basin ({_ynv(ray['attack_constricted'])}, constriction depth {ray['constriction_depth']:.2f}) and producing the white-blue-red digital attack. <strong>Primary</strong> Raynaud is a reversible excursion in the resting basin &mdash; it crosses no lock &mdash; so it <strong>reverses</strong> on rewarming ({_ynv(ray['primary_reversible'])}), and a vasodilator or calcium-channel blocker (nifedipine) aborts an attack ({_ynv(ray['rewarming_or_ccb_reverses'])}). The contrast with rosacea is the page's sharpest result: rosacea's drive <em>crosses</em> its lock, so its dilation is fixed; primary Raynaud's stays <em>short</em> of its lock, so its constriction reverses. The <strong>fixed</strong> digital-ischemia / ulcer state is a downstream structural change of <strong>secondary</strong> Raynaud with connective-tissue disease &mdash; an immune / rheumatology sibling-package seam, named not modeled here.</p>
{vp_card("Raynaud phenomenon anchor (cited)", "Raynaud phenomenon is episodic digital vasospasm with triphasic pallor&ndash;cyanosis&ndash;rubor on cold or stress; primary Raynaud is reversible and managed with cold avoidance and calcium-channel blockers, while secondary Raynaud (scleroderma and other connective-tissue disease) can progress to fixed ischemia and digital ulcers. " + grade_badge('L'))}

<h2>The discriminant: opposite vasomotor diseases from opposite drive signs</h2>
<p>As with the static diseases, the hair cycle, the sebaceous duct and the adhesion bond, the decisive evidence is that clinically opposite behaviours fall out of the <em>same</em> switch driven differently, with no constant changed between them &mdash; here, driven in opposite directions on one vasomotor switch.</p>
<table>
<thead><tr><th>Axis</th><th>One pole</th><th>Opposite pole</th><th>Reproduced</th></tr></thead>
<tbody>
{_vopp_html}
</tbody></table>
<p>All three opposite pairs reproduce ({_ynv(vopp['all_opposite_pairs_reproduced'])}). That one vasomotor switch yields a fixed-dilation disease and a reversible-constriction disease, a vascular and an inflammatory rosacea pole, and reversibility governed by a single lock rule &mdash; from the drive sign alone, on one reused EDAR &gamma; with no new parameter &mdash; is the strongest internal evidence that these vasomotor diseases are reactivity-jamming dynamics, not bespoke fits.</p>

<h2>Grades and reproducibility</h2>
<p>Every mechanism here is a simulation-verified shape or sign {grade_badge('V')} &mdash; the two discontinuous locks, the hysteresis loop, the responsive set-point, the vasodilation/vasoconstriction direction, the reversible-vs-fixed lock rule, the papulopustular amplifier and the brimonidine-vs-laser hysteresis. Every clinical mapping rests on a cited anchor {grade_badge('L')}. The resting tone, reactivity gains and constrictor drives are forced regime scales {grade_badge('F')}. Every absolute magnitude is open {grade_badge('O')} &mdash; erythema index, vessel density, flush magnitude, digital temperature, attack frequency, body-surface area &mdash; inheriting the vasomotor target's obstacle (a per-vessel calibration), with the dermal-perfusion magnitude an inherited circulatory seam, not calibrated here. No disease introduces a new constant; each is a signed vasomotor drive on the one switch, and no new &gamma; is fetched.</p>
<p>The vasomotor pipeline is deterministic on its own terms: two independent runs hash to an identical SHA-256, separate from the core battery, the pathology layer, the hair-cycle layer, the sebaceous layer and the adhesion layer. Crucially, adding this target does <strong>not</strong> touch the core T1&ndash;T5+oncology battery, whose result hash is unchanged at <code>{esc(D['sha'][:12])}&hellip;</code>.</p>
{vp_card("Vasomotor result SHA-256 (determinism)", f"<code>{esc(D['vaso_sha'])}</code><br>The C1 reproducibility gate for the vasomotor layer, identical across independent processes and distinct from the core, pathology, hair-cycle, sebaceous and adhesion hashes. Reproduce with <code>python repro/run_vasomotor.py</code>.")}
"""
    S.append(dict(no="13", slug="13-neurovascular-reactivity-rosacea",
                  short="Neurovascular reactivity", title="Neurovascular reactivity as a hysteretic vasomotor jam: rosacea and Raynaud phenomenon",
                  h1="Neurovascular reactivity as a hysteretic vasomotor jam: rosacea and Raynaud",
                  keywords=["rosacea", "neurovascular reactivity", "flushing", "telangiectasia", "vasomotor", "EDAR",
                            "Raynaud phenomenon", "vasospasm", "brimonidine", "erythema", "thermoregulation interface", "VP theory"],
                  grades=["V", "F", "L", "O"],
                  answer=("Rosacea is cutaneous vasomotor tone losing its reversibility. Putting the already-measured EDAR &gamma; &mdash; the thermoregulation-interface organ &mdash; on the same R19 switch "
                          "makes vasomotor tone a hysteretic two-lock jam: dilated when jammed ON, constricted when OFF, with a fixed state once a sustained drive crosses a lock. "
                          "Rosacea (a vasodilator drive that locks the vessel dilated into fixed telangiectasia) and Raynaud phenomenon (a vasoconstrictor drive giving a reversible attack) then differ only by drive sign, with no fitted constant."),
                  abstract_txt=("Cutaneous vasomotor tone is reproduced as a hysteretic two-lock reactivity jam on the already-measured EDAR gamma (the thermoregulation-interface organ's vasomotor arm; "
                                "no new gamma fetched, none fitted, the dermal-perfusion magnitude left an inherited circulatory seam): the vessel locks dilated at an upper spinodal and constricted at a lower one and is "
                                "reversibly responsive between them, and rosacea (a standing vasodilator drive that locks the vessel dilated into fixed telangiectasia, with a papulopustular inflammatory amplifier) and Raynaud "
                                "phenomenon (a cold vasoconstrictor drive giving a reversible attack) follow as the same switch driven in opposite directions, reversibility being a uniform consequence of whether the drive crosses its lock, adding no constant and leaving the core battery hash unchanged."),
                  abstract=("Cutaneous vasomotor tone &mdash; the neurovascular reactivity that flushes and blanches the skin &mdash; is reproduced as a hysteretic two-lock reactivity jam on the <em>same</em> "
                            "R19 switch as the barrier and wound, running on the <strong>already-measured</strong> EDAR &gamma; (the thermoregulation-interface organ, whose vasomotor arm is intrinsic to it) with "
                            "<strong>no new &gamma; fetched and none fitted</strong>, and with the dermal-perfusion magnitude left an inherited circulatory seam. The vessel locks dilated at an upper spinodal and "
                            "constricted at a lower one and is reversibly responsive between them {V}; the resting tone, reactivity gains and constrictor drives are forced regime scales {F}, the clinical mappings are cited "
                            "anchors {L}, and absolute erythema/vessel/temperature magnitudes stay open {O}. Rosacea (a standing vasodilator drive that locks the vessel dilated into fixed telangiectasia, with a "
                            "papulopustular inflammatory amplifier) and Raynaud phenomenon (a cold vasoconstrictor drive giving a reversible attack) follow as the <em>same</em> switch driven in opposite directions, passing "
                            "an intervention-reversal battery and a three-axis opposite-property discriminant &mdash; vasodilation vs vasoconstriction, fixed vs reversible (the lock rule), vascular vs inflammatory &mdash; the "
                            "layer adding no constant while the core-battery hash stays fixed."
                            ).replace("{V}", grade_badge('V')).replace("{F}", grade_badge('F')).replace("{L}", grade_badge('L')).replace("{O}", grade_badge('O')),
                  body=body))

    # ---- 14 cross-package seams (seam manifest; mirrors repro/_seam, separate hash; no new mechanism) ----
    SE = D["seam"]
    coup = SE["internal_live"][0]
    def _yns(b): return "yes" if b else "no"
    _in_rows = [
        ("Circulatory", "dermal-perfusion magnitude (cited)", "T9 vasomotor", "the vasomotor layer adds only the reactivity dynamics and leaves the perfusion magnitude an inherited citation"),
        ("DNA (gene-clock)", "organ identity + emergence order + measured master-gene &gamma;", "every target", "identity and order live in DNA; &gamma; is measured, read-only, never fitted, vendored and re-vendored on change"),
        ("Substrate", "the R19 bistable switch (with spinodal / barrier / dwell)", "every target + layer", "the one shared primitive, vendored once"),
    ]
    _in_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for (a, b, c, d) in _in_rows)
    _out_rows = [
        ("Gene-lesion &rarr; <code>disease_wp</code>", "single-gene rare genodermatoses (ichthyoses, ectodermal dysplasias, oculocutaneous albinism, xeroderma pigmentosum, hereditary cancer syndromes, other genodermatoses)", "the matching T-target trajectory (T1+T4, T5, T3&rarr;oncology, oncology, T8&hellip;)", "declared"),
        ("Immune-hematologic", "urticaria / angioedema (mast-cell / histamine)", "&mdash; not a skin jamming-class target", "declared"),
        ("Immune-effector", "lichen planus / inflammatory dermatoses", "&mdash; needs an immune-effector seam", "declared"),
        ("Rheumatology", "the <em>fixed</em> digital ischemia of <em>secondary</em> Raynaud (connective-tissue disease)", "T9 covers <em>primary</em> reversible Raynaud", "declared"),
        ("Immune-effector", "rosacea inflammatory chemistry beyond the LL-37 / Demodex flag", "T9 carries the vasomotor reactivity + the amplifier flag", "declared"),
        ("Out-of-class", "cutaneous infections (impetigo, cellulitis, dermatophytosis, herpes, warts)", "&mdash; not an R19-dynamics failure at all", "out-of-class"),
    ]
    _out_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td class=\"num\">{d}</td></tr>" for (a, b, c, d) in _out_rows)
    body = f"""
<h2>One body needs labelled seams, not one big model</h2>
<p>The whole VP programme is a family of organ packages that must eventually run as <em>one body</em> without any package secretly re-deriving another's result. The discipline that makes that safe is the <strong>single source of truth</strong> (SSOT): each quantity is owned by exactly one package, and every other package that needs it imports it across a named <strong>seam</strong> rather than re-computing it. This page is the integumentary package's complete, labelled seam record &mdash; it adds <strong>no new mechanism and no new constant</strong>; it only states, in one machine-readable place, what the package <em>imports</em>, what cross-target coupling it <em>exposes</em>, and what it <em>hands off</em>. The same record is emitted as <code>reports/seam_manifest.json</code> for the one-body runner.</p>
<table>
<thead><tr><th>Seam class</th><th>Meaning</th><th>Count</th><th>Live?</th></tr></thead>
<tbody>
<tr><td>Inherited-in</td><td>read-only inputs vendored from a sibling, never re-derived here</td><td class="num">{SE['_counts']['inherited_in']}</td><td>yes (vendored)</td></tr>
<tr><td>Internal-live</td><td>a cross-<em>target</em> coupling computed live in this package, now exposed as a labelled output</td><td class="num">{SE['_counts']['internal_live']}</td><td>yes</td></tr>
<tr><td>Declared-out</td><td>contracts to sibling packages &mdash; declared, not yet live wiring</td><td class="num">{SE['_counts']['declared_out']}</td><td>no (declared)</td></tr>
</tbody></table>
{vp_card("Why a seam, not a merge", "A seam is a bidirectional cross-reference between two packages that each keep their own owned quantity. The alternative &mdash; one package re-deriving another's number &mdash; would violate the no-tuning, single-source rule the whole programme runs under. Naming the seam is what lets the one-body runner assemble the organs without double-counting.")}

<h2>The exposed coupling: a pigment lesion raises the cancer hazard</h2>
<p>The one genuinely <em>internal</em> cross-target coupling in this package &mdash; the thing §5.3 asks to surface &mdash; is that a <strong>melanocyte-target (T3) lesion which removes the melanin screen raises the shared oncology-kernel hazard</strong>. It is already computed inside the pathology layer; here it is exposed verbatim (the numbers below are <em>re-exported</em> from the verified pathology functions, not recomputed, so the seam output provably <em>is</em> the internal link surfaced). Removing the screen with an albinism-type lesion raises the squamous-cell-carcinoma cumulative hazard to a relative risk of about <strong>{coup['scc_hazard_RR_screen_removed']:.2f}&times;</strong> versus pigmented skin (incidence relative risk about {coup['scc_incidence_RR_screen_removed']:.2f}&times;), and removes the screen that normally blunts a sunburn, raising the melanoma <em>burst</em> relative risk to about <strong>{coup['melanoma_burst_RR_pigment_loss']:.2f}&times;</strong>. That the lesion's delivered-ultraviolet attenuation is exactly <strong>{coup['lesion_delivered_uv_attenuation']:.2f}</strong> (no screen at all) is the mechanistic reason.</p>
<p>The coupling is <em>causal</em>, not a correlate: restoring an exogenous screen (sunscreen) brings the squamous hazard back down to about <strong>{coup['scc_hazard_RR_with_sunscreen']:.2f}&times;</strong> &mdash; the screen is the lever ({_yns(coup['screen_is_causal_lever'])}). This is the seam the one-body runner needs in order to let a pigment-target lesion modify a cancer-target rate without either target re-deriving the other.</p>
{vp_card("Pigment-loss &rarr; oncology (cited anchors)", "Albinism shows markedly elevated cutaneous squamous-cell carcinoma and melanoma, especially in high-ultraviolet regions; vitiligo patches are photoprotection-deficient; and intermittent ultraviolet drives melanoma (Gandini 2005, summary relative risk 1.61). The substrate reproduces the direction of each. " + grade_badge('L'))}

<h2>What the package imports (inherited-in seams)</h2>
<p>These are the read-only inputs the package vendors from a sibling and <strong>never re-derives</strong>. Each is owned elsewhere and carried in under <code>inherited/</code>.</p>
<table>
<thead><tr><th>From package</th><th>Imported quantity</th><th>Consumed by</th><th>Note</th></tr></thead>
<tbody>
{_in_html}
</tbody></table>

<h2>What the package hands off (declared-out seams)</h2>
<p>These are the entities that belong to a <em>sibling</em> package by etiology class &mdash; a single defining gene, an immune effector, or a pathogen &mdash; not to this jamming-class package. They are <strong>declared contracts, not yet live wiring</strong>: the integration harness that would import the sibling's parameters does not exist yet, so each is named honestly with the in-package dynamics-side back-pointer it will connect to once the harness is built. Naming them is what keeps every disease where its mechanism actually lives.</p>
<table>
<thead><tr><th>Seam target</th><th>Owned there</th><th>Dynamics side here</th><th>Status</th></tr></thead>
<tbody>
{_out_html}
</tbody></table>
{vp_card("Declared, not faked", "The gene-lesion and immune seams are contracts, not numbers: this page does not import a single value from <code>disease_wp</code> or any immune package, because the harness is not built. Flagging them as declared (rather than silently modelling them) is the same honesty rule as grading an absolute magnitude [O] &mdash; the boundary is named, not hidden.")}

<h2>Grades and reproducibility</h2>
<p>The exposed coupling is a simulation-verified cross-target <em>shape</em> {grade_badge('V')} &mdash; a pigment lesion raises the cancer hazard, and the screen is the causal lever &mdash; resting on cited epidemiology {grade_badge('L')}; the <strong>absolute</strong> relative-risk magnitude is open {grade_badge('O')}, inheriting the oncology obstacle (a population baseline rate plus an absolute dose calibration). The inherited and declared seams carry the <em>owning</em> package's grade. This layer introduces <strong>no new constant</strong>: every number on this page is re-exported from the pathology layer, and the rest are declarations.</p>
<p>The seam manifest is deterministic on its own terms: two independent runs hash to an identical SHA-256, separate from the core battery and every disease layer. Crucially, this layer only <strong>reads</strong> the disease layers &mdash; it never alters them, and it never imports the core battery &mdash; so the core T1&ndash;T5+oncology result hash is unchanged at <code>{esc(D['sha'][:12])}&hellip;</code> and the pathology hash is unchanged at <code>{esc(D['patho_sha'][:12])}&hellip;</code>.</p>
{vp_card("Seam manifest SHA-256 (determinism)", f"<code>{esc(D['seam_sha'])}</code><br>The C1 reproducibility gate for the seam layer, identical across independent processes and distinct from the core and every disease-layer hash. Reproduce with <code>python repro/run_seam.py</code>.")}
"""
    S.append(dict(no="14", slug="14-cross-package-seams",
                  short="Cross-package seams", title="Cross-package seams: what the integumentary package imports, exposes, and hands off",
                  h1="Cross-package seams: the integumentary package's declared interfaces",
                  keywords=["cross-package seam", "single source of truth", "pigment loss oncology coupling",
                            "albinism melanoma risk", "vitiligo photoprotection", "disease_wp", "one body model",
                            "integration", "VP theory"],
                  grades=["V", "L", "O"],
                  answer=("For the VP organs to run as one body, each package must import a sibling's result across a named seam rather than re-derive it. "
                          "This page is the integumentary package's labelled seam record: it adds no new mechanism, exposes the one internal cross-target "
                          "coupling (a pigment-loss lesion removes the melanin screen and raises the oncology hazard), and declares what it inherits and hands off."),
                  abstract_txt=("The integumentary package's complete labelled seam record for a one-body runner: it inherits dermal-perfusion magnitude, organ identity and the R19 substrate; "
                                "exposes the already-internal pigment-loss to oncology coupling (an albinism/vitiligo screen-loss lesion raises the SCC hazard and melanoma burst relative risk, with sunscreen as the causal lever); "
                                "and declares its gene-lesion, immune and out-of-class hand-offs as contracts, adding no new constant and leaving the core battery hash unchanged."),
                  abstract=("For the VP organ packages to assemble as one body without any package re-deriving another's owned quantity, each interface is a named "
                            "<strong>seam</strong> under a single-source-of-truth rule. This page is the integumentary package's complete labelled seam record &mdash; adding "
                            "<strong>no new mechanism and no new constant</strong>. It <em>inherits</em> the dermal-perfusion magnitude (circulatory), organ identity and measured &gamma; (DNA) "
                            "and the R19 substrate; it <em>exposes</em> the one internal cross-target coupling &mdash; a melanocyte-target lesion that removes the melanin screen raises the shared "
                            "oncology hazard, re-exported verbatim from the verified pathology layer {V} {L}, absolute relative risk open {O}; and it <em>declares</em> its hand-offs (gene-lesion &rarr; "
                            "disease_wp, immune / rheumatology seams, out-of-class infections) as contracts, not yet live wiring. Two runs hash identically and the core-battery hash stays fixed."
                            ).replace("{V}", grade_badge('V')).replace("{L}", grade_badge('L')).replace("{O}", grade_badge('O')),
                  body=body))

    return S
def build_hub(S):
    items = ""
    for s in S:
        items += (f'<li><a href="{s["slug"]}/">{s["no"]}. {esc(s["short"])}</a>'
                  f'<span class="d">{esc(s["title"])}</span></li>\n')
    series = {
        "@context": "https://schema.org", "@type": "CreativeWorkSeries",
        "name": "Integumentary emergence (VP Theory)", "url": SITE + "/",
        "author": {"@type": "Person", "name": AUTHOR, "identifier": f"https://orcid.org/{ORCID}"},
        "inLanguage": "en", "version": _version(),
        "hasPart": [{"@type": "ScholarlyArticle", "name": s["title"], "url": f"{SITE}/{s['slug']}/"} for s in S],
    }
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Integumentary emergence &middot; VP Theory</title>
<meta name="description" content="The integumentary (skin) system emerged from a jammed-granular-vacuum substrate and measured master-gene gamma: barrier, wound healing, melanin, turnover, thermoregulation, and UV carcinogenesis, each graded and reproducible.">
<meta name="author" content="{esc(AUTHOR)}">
<link rel="canonical" href="{SITE}/">
<meta name="robots" content="index, follow, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:title" content="Integumentary emergence (VP Theory)">
<meta property="og:url" content="{SITE}/">
<link rel="stylesheet" href="assets/css/site.css">
<script type="application/ld+json">{json.dumps(series, ensure_ascii=False)}</script>
</head>
<body>
<header>
<nav class="crumb"><a href="https://jamming-physics.org">VP Theory</a> &rsaquo; <span>Integumentary</span></nav>
<h1>Integumentary emergence</h1>
</header>
<main>
<p class="lede">The skin &mdash; the body's boundary &mdash; emerges from one bistable substrate and four measured master-gene &gamma; values. No constant is fitted to a skin phenotype: each is a measured input or substrate-derived, and every claim is graded and reproducible to an identical hash.</p>
<p>This research preview puts the integumentary system under a wide stress sweep: the epidermal water barrier, wound healing as an unjamming transition, melanin as an ultraviolet feedback screen, epidermal turnover as a dwell-cascade, sweating as a regulated interface flux, and ultraviolet carcinogenesis. Start anywhere:</p>
<ul class="toc">
{items}</ul>
<p class="small">Author <a href="https://orcid.org/{ORCID}">{esc(AUTHOR)}</a> (ORCID {ORCID}) &middot; {esc(PROJECT)} &middot; version {esc(_version())} &middot; build {BUILD_DATE} &middot; reproducible engine bundled under <code>repro/</code>.</p>
</main>
<footer>
<p class="small">Grades: [F] forced &middot; [V] simulation-verified &middot; [L] cited anchor &middot; [O] open (obstacle stated). DOI: pending (research preview).</p>
</footer>
</body>
</html>"""


def build_sitemap(S):
    urls = [f"  <url><loc>{SITE}/</loc><lastmod>{BUILD_DATE}</lastmod><priority>1.0</priority></url>"]
    for s in S:
        urls.append(f"  <url><loc>{SITE}/{s['slug']}/</loc><lastmod>{BUILD_DATE}</lastmod><priority>0.8</priority></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")


def build_robots():
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    out = []
    for b in bots:
        out.append(f"User-agent: {b}\nAllow: /\n")
    out.append("User-agent: *\nAllow: /\n")
    out.append(f"\nSitemap: {SITE}/sitemap.xml\n")
    return "\n".join(out)


def build_llms(S):
    lines = [f"# Integumentary emergence (VP Theory)",
             f"> The skin system emerged from a jammed-granular-vacuum substrate and four measured master-gene gamma values, under a strict no-tuning rule. Every claim is graded (F/V/L/O) and the pipeline is bit-reproducible.",
             "", f"Author: {AUTHOR} (ORCID {ORCID}). Version {_version()}. Build {BUILD_DATE}.", "",
             "## Pages"]
    for s in S:
        lines.append(f"- [{s['title']}]({SITE}/{s['slug']}/): {s['abstract_txt']}")
    lines += ["", "## Method",
              "Constants are measured inputs (cited, locked) or substrate-derived; none is fitted to a target. "
              "Grades: F forced, V simulation-verified, L cited anchor, O open with stated obstacle. "
              f"Deterministic; result SHA-256 {SHA_FULL}."]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- main
SHA8 = ""; SHA_FULL = ""

def main():
    global SHA8, SHA_FULL
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Do the research first, then  gates.write_research_complete()  ; echo writing > PHASE  and re-run.")
        return 1

    D = gather()
    SHA_FULL = D["sha"]; SHA8 = D["sha"][:12] + "..."
    docs = os.path.join(_ROOT, "docs")
    os.makedirs(docs, exist_ok=True)

    S = build_sections(D)
    meta = []
    for i, s in enumerate(S):
        prev_s = (S[i-1]["slug"], S[i-1]["short"]) if i > 0 else None
        next_s = (S[i+1]["slug"], S[i+1]["short"]) if i < len(S)-1 else None
        outdir = os.path.join(docs, s["slug"]); os.makedirs(outdir, exist_ok=True)
        htmldoc = page(s, s["slug"], prev_s, next_s)
        open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(htmldoc)
        words = len((s["body"] + s["answer"] + s["abstract"]).split())
        meta.append({"no": s["no"], "slug": s["slug"], "title": s["title"],
                     "short": s["short"], "grades": s["grades"], "words_est": words,
                     "url": f"{SITE}/{s['slug']}/"})
        print(f"  wrote docs/{s['slug']}/index.html  ({words} words, grades {s['grades']})")

    open(os.path.join(docs, "index.html"), "w", encoding="utf-8").write(build_hub(S))
    open(os.path.join(docs, "sitemap.xml"), "w", encoding="utf-8").write(build_sitemap(S))
    open(os.path.join(docs, "robots.txt"), "w", encoding="utf-8").write(build_robots())
    open(os.path.join(docs, "llms.txt"), "w", encoding="utf-8").write(build_llms(S))
    open(os.path.join(docs, "_meta.json"), "w", encoding="utf-8").write(
        json.dumps({"project": PROJECT, "author": AUTHOR, "orcid": ORCID, "version": _version(),
                    "build_date": BUILD_DATE, "result_sha256": D["sha"], "canonical_base": SITE + "/",
                    "sections": meta}, ensure_ascii=False, indent=2))
    print("  wrote docs/index.html, sitemap.xml, robots.txt, llms.txt, _meta.json")
    print(f"DONE. {len(S)} pages + hub. result SHA-256 {D['sha']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
