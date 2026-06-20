#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_neuro_pain_chapters.py — deterministic builder for the v1.11 pain chapters (sec.21-23).

VP-SPEC v1.8 sec.1: code is the agent of transformation. This builder reads the frozen repro
outputs (the engine-derived numbers) and emits the sec.6 canonical-template pages, byte-identical
on every run. Emits the richer v1.8 JSON-LD (CreativeWorkSeries + datePublished/dateModified +
isBasedOn + knowsAbout), answer-first <p class="answer">, abstract, claim-strip, vp-card asides,
self-contained tables, the firewall paragraph, prev/contents/next, footer.

Standard library only.  Run:  python3 build_neuro_pain_chapters.py
"""
import os, sys, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs", "neuro")
REPRO = os.path.join(ROOT, "repro", "neuro")
DOI = "10.5281/zenodo.17979015"
ANALG_DOI = "10.5281/zenodo.20733420"
DNA_DOI = "10.5281/zenodo.20471407"
ORCID = "0009-0002-7535-8245"
ABBREV = "Neural Emergence"
GH = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/neuro"
DATE = "2026-06-19"

AP = "\u2019"     # right single quote (apostrophe), to avoid bare ' in HTML body
DEG = "\u00b0"
SQ = "\u221a"     # sqrt


def esc(s):
    return html.escape(str(s), quote=True)


def head(no, slug, title_subject, headline, desc, knows):
    A = []
    a = A.append
    a('<!DOCTYPE html>')
    a('<html lang="en">')
    a('<head>')
    a('<meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width, initial-scale=1">')
    a(f'<title>{esc(title_subject)} \u2014 {ABBREV} \u00a7{no} | Jamming Physics</title>')
    a(f'<meta name="description" content="{esc(desc)}">')
    a(f'<link rel="canonical" href="https://jamming-physics.org/neuro/{slug}/">')
    a('<link rel="stylesheet" href="/assets/css/site.css">')
    ld = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": headline,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": ABBREV, "identifier": DOI},
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI},
        "sameAs": f"https://doi.org/{DOI}",
        "position": no,
        "author": {"@type": "Person", "name": "Young Jae Lee", "sameAs": f"https://orcid.org/{ORCID}"},
        "datePublished": DATE, "dateModified": DATE,
        "isBasedOn": f"{GH}/{slug}/",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "knowsAbout": knows,
    }
    a('<script type="application/ld+json">')
    a(json.dumps(ld, ensure_ascii=False))
    a('</script>')
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://jamming-physics.org/"},
        {"@type": "ListItem", "position": 2, "name": ABBREV, "item": "https://jamming-physics.org/neuro/"},
        {"@type": "ListItem", "position": 3, "name": f"\u00a7{no} {headline}"}]}
    a('<script type="application/ld+json">')
    a(json.dumps(bc, ensure_ascii=False))
    a('</script>')
    a('</head>')
    a('<body>')
    a(f'<header><nav class="crumb"><a href="/">Home</a> \u203a <a href="/neuro/">{ABBREV}</a> \u203a \u00a7{no}</nav></header>')
    a('<main>')
    return A


def claim_strip(grade_class, grade_text, slug):
    return ('<aside class="claim-strip">'
            f'<span class="grade {grade_class}">{grade_text}</span>'
            '<span class="gate">LOCK \u2192 Derive \u2192 Gate</span>'
            f'<a href="{GH}/{slug}/" rel="noopener">reproduction code (GitHub)</a>'
            f'<span class="doi">DOI: <a href="https://doi.org/{DOI}" rel="noopener">{DOI}</a></span>'
            '</aside>')


def pn(prev, nxt):
    parts = ['<nav class="pn">']
    if prev:
        parts.append(f'<a rel="prev" href="/neuro/{prev[1]}/">\u2190 \u00a7{prev[0]}</a>')
    parts.append('<a href="/neuro/">paper contents</a>')
    if nxt:
        parts.append(f'<a rel="next" href="/neuro/{nxt[1]}/">\u00a7{nxt[0]} \u2192</a>')
    parts.append('</nav>')
    return "".join(parts)


def footer():
    return (f'<footer><p>Young Jae Lee \u00b7 ORCID <a href="https://orcid.org/{ORCID}" rel="noopener">{ORCID}</a> '
            f'\u00b7 DOI: <a href="https://doi.org/{DOI}" rel="noopener">{DOI}</a> '
            f'\u00b7 <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener license">CC BY 4.0</a></p></footer>'
            '</body></html>')


def write(slug, lines):
    outdir = os.path.join(DOCS, slug)
    os.makedirs(outdir, exist_ok=True)
    htmltext = "\n".join(lines) + "\n"
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(htmltext)
    print(f"built docs/neuro/{slug}/index.html  ({len(htmltext)} bytes)")


# ===========================================================================
#  sec.21 — the 27-target three-lever map (inherited, re-derived, drift 0)
# ===========================================================================
def build_21():
    tm = json.load(open(os.path.join(REPRO, "21-analgesic-nociceptor-threshold/expected/threshold_map.json")))
    summ = json.load(open(os.path.join(REPRO, "21-analgesic-nociceptor-threshold/expected/rederive_summary.json")))
    lc = summ["lever_counts"]
    eng = summ["engine_identity"]["this_engine_sha256"]
    slug = "21-analgesic-nociceptor-threshold-map"
    subj = "Analgesic target logic for the nociceptor (inherited)"
    headline = ("Analgesic target logic for the primary somatosensory nociceptor (inherited and re-derived on this "
                "volume own R19 engine): a DNA-grounded 27-target firing-threshold map sorted into three drug-class levers")
    desc = ("INHERITED from analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420, CC BY 4.0) and re-derived on this "
            "volume own engine (drift 0): 27 non-opioid analgesic targets placed on the R19 firing-threshold scale "
            "|h_sp| = spinodal(gamma), which IS the nociceptor firing threshold this volume already runs. Three levers raise "
            "it: L1 reduce inward current (Na_V/Ca_V/ASIC/P2X/TRP), L2 open K_V7, L3 remove the NGF/CGRP drive. gamma reads "
            "promoter STRUCTURE only; every clinical magnitude and the felt pain are [O]/mind.")
    knows = ["non-opioid analgesic", "nociceptor firing threshold", "Nav1.7 SCN9A", "Nav1.8 suzetrigine", "P2X3",
             "gabapentinoid alpha2delta", "Kv7 retigabine", "anti-NGF", "anti-CGRP gepant", "pain target", "which painkiller"]
    A = head(21, slug, subj, headline, desc, knows)
    a = A.append
    a(f'<h1>{esc(headline)}</h1>')
    a('<p class="answer">This section brings home a sibling whitepaper \u2014 analgesic_threshold_logic v2.0 '
      f'(DOI {ANALG_DOI}), a DNA-grounded map of 27 non-opioid analgesic targets \u2014 to its native organ, the primary '
      'somatosensory nociceptor (this volume master PRDM12, Na_V1.7 = SCN9A). Each pain gene measured promoter '
      'gamma sits on the R19 firing-threshold scale |h_sp| = spinodal(gamma), which is identically the firing threshold this '
      'volume sec.2/sec.19 already run, so re-deriving all 27 on this engine reproduces the inherited thresholds '
      'bit-for-bit (drift 0). The targets sort into three drug-class levers \u2014 reduce the inward current, open K_V7, remove '
      'the NGF/CGRP drive \u2014 each raising the firing threshold; efficacy, dose, and the felt pain stay [O]/mind.</p>')
    a('<p class="abstract">analgesic_threshold_logic v2.0 (concept DOI ' + ANALG_DOI + ', CC BY 4.0) was itself built ON '
      'this volume neuro engine: its reproduction engine is byte-identical to repro/neuro/_engine/vp_neuro_engine.py '
      '(asserted in-module, sha256 ' + eng[:12] + '\u2026). So the nociceptor '
      'firing threshold the analgesic map raises IS the |h_sp| = 2(g/3)^1.5 = spinodal(gamma) every cell in this volume runs. '
      'The engine reads each pain gene human promoter and returns gamma = \u2212mean(NN stacking \u0394G, SantaLucia 1998), '
      'places it on |h_sp|, and re-deriving all 27 target reads on this engine reproduces the inherited firing thresholds '
      'bit-for-bit (every displayed |h_sp| and barrier exact at the frozen precision, order identical, drift 0). The 27 '
      'targets sort into three intervention levers, all raising the same firing threshold from different directions: '
      f'L1 reduce the inward (excitatory) current ({lc.get("L1",0)} channels + {lc.get("L1-adjacent",0)} adjacent), '
      f'L2 increase the outward K+ current ({lc.get("L2",0)} K_V7), L3 remove the NGF/CGRP sensitising drive '
      f'({lc.get("L3",0)} ligand/receptor), with the master TF PRDM12 and {lc.get("context",0)} opioid/cannabinoid comparators '
      'read for contrast. The firewall is inherited verbatim: gamma reads promoter switch-threshold STRUCTURE only \u2014 never a '
      'channel voltage, a drug potency, a dose, an in-vivo selectivity, or a clinical effect; every such magnitude is [O]; the '
      'felt/affective pain is the Felt Cognition volume. No molecule is designed and nothing prescribes. The drift-0 '
      're-derivation and the three-lever frame are [V]/[F]; every clinical magnitude is [O] with stated obstacles.</p>')
    a(claim_strip("g-verified", "[V] simulation-verified", slug))
    a('<p>Every pain reading in this volume ends at the same question: which intervention raises the nociceptor firing '
      'threshold, and toward which drug class does the mechanism point. This section answers it by <b>inheriting</b> a sibling '
      f'whitepaper, <code>analgesic_threshold_logic</code> v2.0 (<b>DOI {ANALG_DOI}</b>, CC BY 4.0). It is not a paste: that '
      'sibling was built on this very engine, so the inheritance is the same substrate read a second way.</p>')
    a('<aside class="vp-card" data-locked="analgesic"><b>analgesia = raise the firing threshold |h_sp| = spinodal(\u03b3) = '
      '2(g/3)<sup>1.5</sup></b> \u2014 INHERITED from <code>analgesic_threshold_logic</code> v2.0 (DOI ' + ANALG_DOI + '): '
      'each pain gene promoter \u03b3 (NN-stacking \u0394G) is placed on the SAME R19 firing-threshold scale this volume '
      'nociceptor runs; three levers (reduce inward / open K\u1d651 / remove NGF\u2013CGRP drive) raise it. \u03b3 reads STRUCTURE '
      'only \u2014 never a voltage, potency, dose, or effect ([O]). <b>[F]</b> forced. <a href="/neuro/20-complete-sensory-atlas/">'
      'sensory-atlas \u03b3 source \u00a720</a></aside>')
    a('<p>The engine reads each pain gene human promoter and returns <span class="m">\u03b3 = \u2212mean(NN stacking \u0394G, '
      'SantaLucia 1998)</span>, then places <span class="m">\u03b3</span> on the R19 double-well firing-threshold scale '
      '<span class="m">|h_sp| = 2(g/3)^1.5 = (2/3\u221a3)\u03b3^1.5</span>. That scale is <i>this</i> volume own '
      '<span class="m">spinodal(\u03b3)</span>: re-deriving all <span class="m">27</span> reads on it reproduces the inherited '
      'firing thresholds <b>bit-for-bit</b> (every displayed |h_sp| and barrier exact at the frozen precision, order identical '
      '\u2014 drift zero). The analgesic firing-threshold axis <i>is</i> the nociceptor spinodal of sec.2/sec.19; that identity '
      'is why the inheritance is principled.</p>')
    a('<p>The 27 targets sort into <b>three intervention levers</b>, all raising the same firing threshold from different '
      'directions: <b>L1</b> reduce the inward (excitatory) current (block depolarising Na<sub>V</sub> / Ca<sub>V</sub> / ASIC '
      '/ P2X / TRP channels), <b>L2</b> increase the outward K<sup>+</sup> current (open K<sub>V</sub>7), <b>L3</b> remove the '
      'up-stream sensitising drive (block NGF / CGRP). Ordered by the stiffest firing gate first:</p>')
    a('<table><thead><tr><th>gene</th><th>lever</th><th>channel / protein</th><th>\u03b3</th><th>|h_sp|</th></tr></thead><tbody>')
    for e in tm["entries"]:
        cp = e["channel"] or e["protein"] or ""
        a(f'<tr><td>{esc(e["gene"])}</td><td>{esc(e["lever"])}</td><td>{esc(cp)}</td>'
          f'<td>{e["gamma"]:.4f}</td><td>{e["spinodal_h_sp"]:.4f}</td></tr>')
    a('</tbody></table>')
    a('<p><b>Engine identity and drift.</b> This volume engine is byte-identical to the engine the frozen sibling map was '
      'built on (sha256 ' + eng[:16] + '\u2026, asserted in-module). Re-deriving all '
      f'{summ["n_targets"]} target reads on it reproduces the frozen |h_sp| and barrier exactly at the frozen precision, with '
      'identical spinodal order \u2014 the drift-zero inheritance that makes this volume the canonical home of the somatosensory '
      'reading (the digestive volume visceral-pain section points here).</p>')
    a('<p><b>Treatment (model reading).</b> INHERITED analgesic target logic, read on this volume nociceptor. The firing '
      'threshold |h_sp| is raised \u2014 equivalently the afferent gain is lowered \u2014 by ANY of three levers: L1 reduce the '
      'inward current (the \u03b1\u03b4-1 gabapentinoid class; the Na_V1.8 / P2X3 nociceptor-selective classes), L2 open the K_V7 '
      'brake (retigabine/flupirtine template), L3 remove the NGF/CGRP drive (anti-NGF / anti-CGRP). Class placement is [F] '
      'structural; efficacy, dose, and selectivity-in-vivo are [O]; the felt/affective pain is the Felt Cognition volume. '
      'No molecule is designed; nothing prescribes.</p>')
    a('<p>The firewall is non-negotiable and inherited verbatim: <span class="m">\u03b3</span> reads promoter switch-threshold '
      'STRUCTURE only \u2014 it is never a channel activation voltage, a drug potency, a dose, an in-vivo selectivity, or a '
      'clinical effect; every such magnitude and absolute efficacy are <span class="m">[O]</span>; the lever strength is '
      'structural, not a dose; the L3 (NGF/CGRP) mechanism link is <span class="m">[O]</span> cited biology; and the felt / '
      'affective pain is the Felt Cognition volume. This is a proposal-only target hypothesis.</p>')
    a(pn((20, "20-complete-sensory-atlas"), (22, "22-neuropathic-pain-improvement-levers")))
    a('</main>')
    a(footer())
    write(slug, A)


# ===========================================================================
#  sec.22 — neuropathic pain dynamics + the three improvement levers
# ===========================================================================
def build_22():
    d = json.load(open(os.path.join(REPRO, "22-neuropathic-pain-firing-threshold/expected/neuropathic_pain_levers.json")))
    ds = d["de_sensitisation"]
    slug = "22-neuropathic-pain-improvement-levers"
    subj = "Neuropathic pain as a firing-threshold shift, and three improvement levers"
    headline = ("Neuropathic / sensitised pain read as a firing-threshold shift on the shared R19 nociceptor, and the three "
                "improvement levers that raise the threshold back, derived on this volume own engine")
    desc = ("Neuropathic pain is an acquired firing-threshold disorder: nerve injury and the NGF/CGRP drive lower the "
            "nociceptor threshold so an innocuous input fires (allodynia) and the cell fires un-provoked. On this volume "
            "R19 engine a sensitisation bias b raises the afferent gain chi=1/(3s*^2-g); each of the three levers lowers "
            "b_eff so the firing threshold rises and the gain falls monotonically back to the baseline 1/(2g). A drug-class "
            "pointer; magnitudes [O], felt pain is mind.")
    knows = ["neuropathic pain", "allodynia", "central sensitisation", "afferent gain", "gabapentinoid", "Nav1.8",
             "Kv7 opener", "anti-NGF", "anti-CGRP", "diabetic neuropathy pain", "which painkiller for nerve pain"]
    A = head(22, slug, subj, headline, desc, knows)
    a = A.append
    a(f'<h1>{esc(headline)}</h1>')
    a('<p class="answer">Neuropathic pain is, on the shared substrate, an acquired <b>firing-threshold shift</b>: peripheral '
      'nerve injury up-regulates depolarising channels (e.g. Na_V1.3) and the NGF/CGRP drive lowers the nociceptor threshold, '
      'so an innocuous input now fires the cell (allodynia) and it fires un-provoked (spontaneous pain). On this volume '
      'R19 engine a sensitisation bias b raises the afferent gain chi = 1/(3s*\u00b2\u2212g) \u2014 '
      f'\u00d7{ds["gain_amplification"]} at b = {ds["b0_fraction_of_spinodal"]}\u00d7spinodal. '
      'Each of the three inherited levers lowers the effective bias, so the firing threshold rises and the gain falls '
      'monotonically back to the baseline 1/(2g). That is the improvement: raise the threshold, by any of three doors.</p>')
    a('<p class="abstract">This is this volume native disease reading (VP_FRAMEWORK_MAP ownership): the primary '
      'somatosensory nociceptor is a neuro entity, and neuropathic pain is an acquired, dynamics-key condition, so it is owned '
      'here by dynamics (the monogenic pain channelopathies are gene-key entities owned by disease_wp and cross-referenced in '
      'sec.23). One R19 element, nothing fitted: from the quiescent rest s0 = \u2212\u221ag a peripheral sensitisation bias '
      'b \u2265 0 slides the operating point toward yield, and two locked readings of the SAME element are the firing-threshold '
      'margin T(b) = spinodal(g) \u2212 b and the afferent gain chi(b) = 1/(3s*\u00b2\u2212g), which diverges at the R19 spinodal '
      f'(allodynia/hyperalgesia as a saddle-node critical gain). At b = {ds["b0_fraction_of_spinodal"]}\u00d7spinodal the gain is '
      f'{ds["sensitised_gain"]} \u2014 \u00d7{ds["gain_amplification"]} above the baseline {ds["baseline_gain_1_over_2g"]} = 1/(2g). '
      'Applying each lever at increasing structural strength \u03b4 lowers b_eff = b \u2212 \u03b4: for ALL THREE the firing '
      'threshold rises monotonically and the gain falls monotonically back toward the baseline, and a full reversal returns the '
      'gain exactly to 1/(2g). The de-sensitisation, the monotone behaviour, and the baseline return are [V]/[F]; \u03b4 is '
      'structural (not a dose) and every clinical magnitude is [O]; the felt/affective pain is the Felt Cognition volume.</p>')
    a(claim_strip("g-verified", "[V] simulation-verified", slug))
    a('<aside class="vp-card" data-locked="afferent_gain"><b>afferent gain \u03c7 = 1/(3 s*\u00b2 \u2212 g)</b> \u2014 the R19 '
      'restoring-curvature inverse at the operating point a sensitisation bias b sets; baseline \u03c7 = 1/(2g), rising to '
      '\u221e at the spinodal (allodynia as a saddle-node critical gain). Lowering b_eff (any lever) raises the firing threshold '
      'T = spinodal \u2212 b_eff and lowers \u03c7. Peripheral term only; felt pain is <code>mind</code>. <b>[F]</b> forced. '
      '<a href="/neuro/21-analgesic-nociceptor-threshold-map/">three-lever map \u00a721</a></aside>')
    a('<p>The three levers, read on the sensitised nociceptor, do one thing. Take an afferent sensitised to '
      f'<span class="m">b\u2080 = {ds["b0_fraction_of_spinodal"]}\u00d7spinodal</span> (gain raised '
      f'<span class="m">\u00d7{ds["gain_amplification"]}</span> above baseline); apply a lever at increasing <i>structural</i> '
      'strength <span class="m">\u03b4</span> (a fraction of the sensitisation removed \u2014 not a dose). For <b>every</b> lever '
      'the firing-threshold margin <span class="m">T = spinodal \u2212 b_eff</span> rises and the gain '
      '<span class="m">\u03c7 = 1/(3s*\u00b2\u2212g)</span> falls monotonically back toward the baseline '
      f'<span class="m">{ds["baseline_gain_1_over_2g"]} = 1/(2g)</span>:</p>')
    a('<table><thead><tr><th>lever strength \u03b4 (structural)</th><th>firing threshold margin T</th>'
      '<th>afferent gain \u03c7 = 1/(3s*\u00b2\u2212g)</th></tr></thead><tbody>')
    for r in ds["sweep"]:
        a(f'<tr><td>{r["delta"]:.5f}</td><td>{r["firing_threshold_margin"]:.5f}</td><td>{r["afferent_gain"]:.5f}</td></tr>')
    a('</tbody></table>')
    a('<p>This makes the inherited map a <b>drug-class pointer</b> for the neuro-native pain disorders \u2014 which lever, and '
      'which cited validated agent class realises it. It does <i>not</i> prescribe: it points to the mechanism class an '
      'effective agent moves.</p>')
    a('<table><thead><tr><th>disorder</th><th>mechanism (threshold reading)</th><th>lever(s)</th>'
      '<th>pointer classes (cited)</th></tr></thead><tbody>')
    for p in d["disease_lever_pointers"]:
        a(f'<tr><td>{esc(p["disorder"])}</td><td>{esc(p["mechanism"])}</td>'
          f'<td>{esc(", ".join(p["levers"]))}</td><td>{esc(p["pointer_classes"])}</td></tr>')
    a('</tbody></table>')
    a('<p><b>Improvement, stated as a mechanism class.</b> The single improvement these readings converge on is to <i>raise '
      'the nociceptor firing threshold</i>; the three levers are three structural doors onto the same axis, each pointing to a '
      'cited validated drug class. The realised peripheral case is the Na_V1.8 closed-state stabiliser (an L1 move, '
      'approved 2025); the most-prescribed adjuvant is the \u03b1\u03b4-1 gabapentinoid (also L1); migraine/trigeminal pain is '
      'the L3 (anti-CGRP) door; refractory central pain is the N-type Ca_V2.2 (intrathecal) door. The model says <i>which '
      'door</i>; it never says how far to open it \u2014 \u03b4 is structural and every clinical magnitude is '
      '<span class="m">[O]</span>.</p>')
    a('<p>The firewall is kept verbatim: this layer moves only the peripheral afferent firing-threshold term; the felt / '
      'affective pain is the Felt Cognition volume; \u03b4 is structural, not a dose; potency, dose, in-vivo selectivity and '
      'efficacy are <span class="m">[O]</span>. No molecule is designed and nothing diagnoses, treats, or prescribes \u2014 it '
      'is a proposal-only target hypothesis.</p>')
    a(pn((21, "21-analgesic-nociceptor-threshold-map"), (23, "23-pain-channelopathy-and-dna-grounding")))
    a('</main>')
    a(footer())
    write(slug, A)


# ===========================================================================
#  sec.23 — pain channelopathy direction anchor + DNA-emergence grounding
# ===========================================================================
def build_23():
    d = json.load(open(os.path.join(REPRO, "22-neuropathic-pain-firing-threshold/expected/neuropathic_pain_levers.json")))
    ca = d["channelopathy_anchor"]
    dna = json.load(open(os.path.join(REPRO, "20b-dna-emergence-inheritance/expected/dna_emergence.json")))
    slug = "23-pain-channelopathy-and-dna-grounding"
    subj = "The pain channelopathy anchor and the DNA-emergence grounding"
    headline = ("The measured pain channelopathies anchor the firing-threshold direction, and one inherited measured gamma "
                "grounds the nociceptor that sec.21 and sec.22 read \u2014 the DNA-emergence inheritance, made explicit")
    desc = ("Measured biology fixes the firing-threshold direction: Na_V1.7 loss-of-function drives the threshold to infinity "
            "(congenital insensitivity to pain) and gain-of-function lowers it (inherited erythromelalgia / PEPD), bracketing "
            "the lever axis; the approved Na_V1.8 closed-state stabiliser sits on the same axis pushed the protective way. The "
            "nociceptor lineage emerges from one inherited measured promoter gamma (form <- gamma; DOI 10.5281/zenodo.20471407), "
            "the same gamma the sec.21 map and sec.22 dynamics read. Gene-key entities owned by disease_wp; magnitudes [O].")
    knows = ["pain channelopathy", "Nav1.7 SCN9A", "congenital insensitivity to pain", "inherited erythromelalgia",
             "paroxysmal extreme pain disorder", "CIPA NTRK1", "DNA emergence", "promoter gamma", "nociceptor lineage"]
    A = head(23, slug, subj, headline, desc, knows)
    a = A.append
    a(f'<h1>{esc(headline)}</h1>')
    a('<p class="answer">Two measured DNA directions bracket the lever map and prove the axis is real, not an analogy. '
      'A Na_V1.7 (SCN9A) loss-of-function drives the firing threshold to infinity \u2014 congenital insensitivity to pain, no '
      'pain under any circumstance; a gain-of-function lowers it \u2014 inherited erythromelalgia and paroxysmal extreme pain '
      'disorder. The realised analgesic (a Na_V1.8 closed-state stabiliser, approved 2025) sits on the SAME axis, pushed the '
      'protective way. And the nociceptor that sec.21 and sec.22 read emerges from one inherited measured promoter gamma '
      '(form <- gamma) \u2014 so the map, the disease dynamics, and the cell all sit on one DNA grounding.</p>')
    a('<p class="abstract">The firing-threshold frame the analgesic map (sec.21) and the neuropathic-pain dynamics (sec.22) use '
      'is anchored at both ends by measured human biology. The nociceptor firing threshold is the pain knob: lower it and there '
      'is more pain, raise it and there is less. A Na_V1.7 loss-of-function sends the threshold to infinity (the gate never '
      'opens) and the measured phenotype is congenital insensitivity to pain (Cox 2006); a gain-of-function lowers or sustains '
      'the gate and the measured phenotypes are inherited erythromelalgia (Drenth 2005) and paroxysmal extreme pain disorder '
      '(Fertleman 2006; Estacion 2008); an NTRK1 loss-of-function removes the nociceptor developmental arm (CIPA, Indo 1996). '
      'The realised analgesic move, a Na_V1.8 (SCN10A) closed-state stabiliser, raises the threshold and is the FDA-approved '
      'non-opioid suzetrigine (2025-01-30). These monogenic entities are gene-key and owned by the rare-disease volume '
      '(disease_wp); this volume owns only the threshold DYNAMICS and cross-references that volume for the named entity. The '
      'second half makes the DNA-emergence inheritance explicit: the nociceptor lineage emerges from one inherited measured '
      'promoter gamma = \u2212mean(NN stacking \u0394G, SantaLucia 1998), read on the shared R19 Organ primitive (presence '
      'threshold = spinodal(gamma), emergence order = argsort spinodal, relative dwell ~ gamma^1.5) exactly the DNA volume rule '
      f'(form <- gamma; 4D DNA Blueprint, DOI {DNA_DOI}). That inherited gamma is bit-for-bit the measured atlas gamma the '
      'sec.21 map and sec.22 dynamics read, so all three sit on one grounding. The channelopathy directions are [V/F] anchored '
      'to measured phenotypes; gamma is measured [V], never fitted; every clinical magnitude is [O].</p>')
    a(claim_strip("g-calibrated", "[V/F] anchored to measured phenotypes", slug))
    a('<aside class="vp-card" data-locked="firing_threshold"><b>the nociceptor firing threshold IS the pain axis</b> \u2014 '
      'measured: Na_V1.7 LOF \u2192 threshold \u2192 \u221e \u2192 no pain (CIP); GOF \u2192 threshold lowered \u2192 spontaneous '
      'pain (IEM/PEPD). The approved Na_V1.8 closed-state stabiliser raises it (the realised analgesic). So |h_sp| is not an '
      'analogy \u2014 it is the measured pain axis. <b>[V/F]</b> anchored. <a href="/neuro/02-substrate-neuron-switch/">R19 '
      'switch \u00a72</a></aside>')
    a('<p>The measured channelopathies, read as firing-threshold directions:</p>')
    a('<table><thead><tr><th>locus</th><th>DNA change</th><th>threshold direction</th><th>measured phenotype</th>'
      '<th>owns entity</th></tr></thead><tbody>')
    for an in ca["anchors"]:
        a(f'<tr><td>{esc(an["locus"])}</td><td>{esc(an["dna_change"])}</td><td>{esc(an["threshold_direction"])}</td>'
          f'<td>{esc(an["measured_phenotype"])}</td><td>{esc(an["owns_entity"])}</td></tr>')
    a('</tbody></table>')
    a(f'<p>{esc(ca["reading"])}</p>')
    a('<h2>The DNA-emergence grounding (made explicit)</h2>')
    a('<aside class="vp-card" data-locked="gamma"><b>form &larr; \u03b3 (Layer 1)</b> \u2014 the measured promoter '
      '\u03b3 = \u2212mean(NN stacking \u0394G, SantaLucia 1998) emerges the cell/organ on the shared R19 switch; emergence '
      'order = argsort spinodal(\u03b3), relative size ~ \u03b3<sup>1.5</sup>. INHERITED from the DNA volume (4D DNA Blueprint, '
      f'DOI {DNA_DOI}). \u03b3 is MEASURED [V], never fitted. <a href="https://doi.org/{DNA_DOI}" rel="noopener">DNA volume</a></aside>')
    a('<p>The whole chain stands on one inherited fact: the measured promoter gamma of a master gene, read on the shared R19 '
      'switch, emerges the cell. This volume already used it (sec.12 sensory-organ-4d, sec.20 atlas); here it is made explicit '
      'for the nociceptor lineage. For each lineage gene the element emerges via this volume own R19 Organ primitive \u2014 '
      'presence threshold = <span class="m">spinodal(\u03b3)</span>, relative dwell <span class="m">~ \u03b3^1.5</span> \u2014 '
      'and the inherited gamma is <b>bit-for-bit</b> the measured atlas gamma that the sec.21 map and sec.22 dynamics read '
      f'(grounding match: {str(dna["inherited_gamma_is_measured_atlas"]).lower()}). One grounding, three readings.</p>')
    a('<table><thead><tr><th>gene</th><th>\u03b3 (measured)</th><th>presence threshold spinodal(\u03b3)</th>'
      '<th>barrier</th><th>relative dwell ~ \u03b3^1.5</th></tr></thead><tbody>')
    for e in dna["elements"]:
        a(f'<tr><td>{esc(e["gene"])}</td><td>{e["gamma"]:.4f}</td><td>{e["presence_threshold_spinodal"]:.4f}</td>'
          f'<td>{e["barrier"]:.4f}</td><td>{e["relative_dwell"]:.4f}</td></tr>')
    a('</tbody></table>')
    a('<p>Emergence order (argsort spinodal, the DNA gene-clock rule): <span class="m">'
      + esc(" &lt; ".join(dna["emergence_order_by_spinodal"])) + '</span>. The order is the morphogen/threshold spinodal, not a '
      'fitted ranking; gamma is measured and only the inherited grounding is used.</p>')
    a('<p>The plan for the existing chapters (sec.00\u2013sec.20) is the same inheritance, stated forward: every chapter that '
      'names a master gene already carries its measured gamma in the sec.20 atlas, so the DNA-emergence grounding is applied by '
      'reading that gamma on the R19 Organ/Neuron primitive rather than asserting the cell \u2014 the route this section '
      'demonstrates for the nociceptor lineage and the route sec.12/sec.17 already take for the sensory organs and the spinal '
      'cord. gamma is measured [V], never fitted; identity and order are owned by the DNA volume; this volume emerges via R19.</p>')
    a(pn((22, "22-neuropathic-pain-improvement-levers"), None))
    a('</main>')
    a(footer())
    write(slug, A)


def main():
    build_21()
    build_22()
    build_23()


if __name__ == "__main__":
    main()
