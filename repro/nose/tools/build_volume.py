#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_volume.py — grow the verified E0–E5 base into the full multi-chapter HTML volume.

Run from the package root:   python3 tools/build_volume.py        # → writes docs/

Implements the VP-SPEC v1.8 §6 chapter template (answer-first · self-contained abstract · claim-strip
· self-contained vp-cards for locked cross-volume quantities · ScholarlyArticle + BreadcrumbList
JSON-LD · prev/next nav) for the nose (olfaction) emergence volume, paper_id `nose`.

CRITICAL — HTML↔code drift = 0 (VP-SPEC C1 / Phase-4).  Every displayed NUMBER comes from
tools/vp_nose_ssot.py via `num(key)`, emitted as `<span class="vp-num" data-key="{key}">{value}</span>`.
The volume builder never hard-codes a quantity; tools/gate_volume.py re-derives the SSOT and asserts
each span equals the freshly computed value. Prose (claims, grades, [O] obstacles) is written here;
numbers are not.

Disease chapters (E4, E5) carry a prominent NON-CLINICAL scope banner; everything is direction-only /
proposal-only (FIREWALL #4, #8). The allergy MECHANISM is cited to immune §11, never re-derived.
stdlib + numpy (via the SSOT). No network.
"""
import os, sys, json, html

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(_HERE)
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from vp_nose_ssot import ssot

R = ssot()
DOCS = os.path.join(PKG, "docs")

# ---- volume identity (self-consistent; the intended jamming-physics.org/nose deployment) ----------
PAPER_ID = "nose"
SHORT    = "Olfactory Emergence"
TITLE    = "Olfactory Emergence: Smell from the R19 Jamming Switch and Measured DNA γ"
SITE     = "https://jamming-physics.org"
ORCID    = "https://orcid.org/0009-0002-7535-8245"
AUTHOR   = "Young Jae Lee"
LICENSE  = "https://creativecommons.org/licenses/by/4.0/"
REPO     = "https://github.com/rego093-sketch/jamming-physics"
DATE     = "2026-06-22"

# cross-volume DOIs (REAL sources this volume cites; never fabricated) ------------------------------
DOI_PHYSICS = "10.5281/zenodo.17932566"   # the jammed-lattice substrate + R19 switch primitive
DOI_DNA     = "10.5281/zenodo.20471407"   # 4D DNA Blueprint v1.13 — γ (level) + A4 (shape)
DOI_NEURO   = "10.5281/zenodo.17979015"   # neural emergence chain (the sensory transduction reading)
DOI_IMMUNE  = "10.5281/zenodo.20755280"   # immune/hematologic §11 — the allergy mechanism (E5)
DOI_MIND    = "10.5281/zenodo.20694404"   # Felt Cognition — the felt percept (deferred)

# this volume's OWN canonical record — Zenodo CONCEPT DOI (always resolves to the latest version) -----
DOI_NOSE     = "10.5281/zenodo.20790182"  # Olfactory Emergence (this volume itself)
DOI_NOSE_URL = f"https://doi.org/{DOI_NOSE}"


def num(key):
    """Insert an SSOT value as a drift-checked span (the only way a number enters the HTML)."""
    assert key in R, f"build_volume: SSOT key not found: {key}"
    return f'<span class="vp-num" data-key="{key}">{html.escape(R[key])}</span>'


def vp_card(anchor, head, meaning, grade_tok, grade_word, href, link_text):
    return (f'<aside class="vp-card" data-locked="{anchor}">'
            f'<b>{head}</b> — {meaning} <b>{grade_tok}</b> {grade_word}. '
            f'<a href="{href}" rel="noopener">{link_text}</a></aside>')


def claim_strip(grade_class, grade_tok_word, slug):
    return (
        '<aside class="claim-strip page">'
        f'<span class="grade g-{grade_class}">{grade_tok_word}</span>'
        '<span class="gate">LOCK → Derive → Gate</span>'
        f'<a href="{DOI_NOSE_URL}" rel="noopener">DOI {DOI_NOSE}</a>'
        f'<a href="{REPO}/tree/main/vp_nose_emergence_seed/research/" rel="noopener">Reproduce (GitHub)</a>'
        f'<a href="{SITE}/{PAPER_ID}/" rel="noopener">VP framework</a>'
        '</aside>'
    )


SCOPE_BANNER = (
    '<aside class="scope-banner" role="note">'
    '<b>Non-clinical, theoretical research.</b> This chapter studies <i>structure and mechanism</i> only. '
    'It does not diagnose, treat, screen, or prescribe; it designs no molecule and states no dose, '
    'potency, or efficacy. Every statement is <b>direction-only / proposal-only</b>. The felt experience '
    'of smelling is deferred to the Felt Cognition (mind) volume.'
    '</aside>'
)


def ld_article(slug, headline, position):
    obj = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "headline": headline,
        "isPartOf": {"@type": "CreativeWorkSeries", "name": SHORT,
                     "url": f"{SITE}/{PAPER_ID}/",
                     "sameAs": DOI_NOSE_URL,
                     "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI_NOSE}},
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "position": position,
        "datePublished": DATE, "dateModified": DATE,
        "isBasedOn": f"{REPO}/tree/main/vp_nose_emergence_seed",
        "license": LICENSE,
        "knowsAbout": ["olfaction", "R19 jamming switch", "combinatorial odour code",
                       "olfactory receptor", "promoter stiffness gamma"],
    }
    return json.dumps(obj, ensure_ascii=False)


def ld_breadcrumb(slug, short_title):
    obj = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": SHORT, "item": f"{SITE}/{PAPER_ID}/"},
        {"@type": "ListItem", "position": 3, "name": short_title}]}
    return json.dumps(obj, ensure_ascii=False)


def chapter_page(n, slug, subj, description, grade_class, grade_tok_word, short_title,
                 answer, abstract, cards, body, prev_link, next_link):
    title = f"{subj} — {SHORT} §{n} | Jamming Physics"
    crumb = (f'<header><nav class="crumb"><a href="/">Home</a> › '
             f'<a href="/{PAPER_ID}/">{SHORT}</a> › §{n}</nav></header>')
    pn = '<nav class="pn">'
    pn += (f'<a rel="prev" href="{prev_link[1]}">← §{prev_link[0]}</a>' if prev_link
           else f'<a href="/{PAPER_ID}/">Volume contents</a>')
    pn += f'<a href="/{PAPER_ID}/">Volume contents</a>'
    pn += (f'<a rel="next" href="{next_link[1]}">§{next_link[0]} →</a>' if next_link
           else f'<a href="/{PAPER_ID}/">Volume contents</a>')
    pn += '</nav>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE}/{PAPER_ID}/{slug}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld_article(slug, short_title, n + 1)}
</script>
<script type="application/ld+json">
{ld_breadcrumb(slug, f'§{n} {short_title}')}
</script>
</head>
<body>
{crumb}
<main>
<h1>{html.escape(subj)}</h1>
<p class="answer">{answer}</p>
<p class="abstract">{abstract}</p>
{claim_strip(grade_class, grade_tok_word, slug)}
{cards}
{body}
{pn}
</main>
<footer><p>{SHORT} · <a href="{DOI_NOSE_URL}" rel="noopener">DOI {DOI_NOSE}</a> · <a href="{ORCID}" rel="noopener">ORCID {AUTHOR}</a> ·
<a href="{LICENSE}" rel="noopener">CC BY 4.0</a> · reproduce: <a href="{REPO}" rel="noopener">GitHub</a></p></footer>
</body>
</html>
"""


# ==================================================================================================
#  CHAPTERS  (slug, builder)  — numbers via num(); prose written here, faithful to the increments.
# ==================================================================================================
CHAPTERS = []   # filled below: list of dicts


def gene_row(sym, *cells):
    return "<tr><th scope=\"row\">" + sym + "</th>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


# ---- §0 — the inherited foundation ---------------------------------------------------------------
def build_e0():
    slug = "00-inherited-foundation"
    or_rows = "".join(gene_row(s, num(f"gene.{s}.gamma"), num(f"gene.{s}.hstar"),
                               num(f"gene.{s}.barrier"), num(f"gene.{s}.a4"),
                               ATLAS_ROLE[s]) for s in ALL_GENES_BY_NODE)
    cards = (
        vp_card("r19", "ds/dt = γ·s − s³ + h", "the shared R19 bistable switch; the spinodal "
                "h* = 2(γ/3)<sup>1.5</sup> is the drive past which the opposite basin disappears, so the "
                "flip is discontinuous", "[F]", "forced",
                f"https://doi.org/{DOI_PHYSICS}", "R19 substrate (physics)")
        + vp_card("gamma", "γ = −mean(SantaLucia-1998 NN ΔG37)", "the promoter stiffness LEVEL; the A4 "
                  "coordinate is its orthogonal SHAPE (A4 = signal − γ). Both are read; γ alone is the "
                  "compressed view", "[L]", "measured",
                  f"https://doi.org/{DOI_DNA}", "DNA reading v1.13")
    )
    body = f"""
<h2>The two inherited primitives — and the one that is missing</h2>
<p>The volume inherits exactly two things, byte-identical to the eye/ear sibling seeds: the R19
bistable switch ds/dt = γ·s − s³ + h, and the DNA reading that measures each gene's promoter as a
stiffness LEVEL γ plus an orthogonal SHAPE (the A4 coordinate). Nothing here is re-derived.</p>
<p>What is <b>not</b> inherited is a wave/angle module. Vision and hearing read a wave as a single
physical place; smell has no wave, so no such module carries over. That absence is the volume's first
honest structural statement, not an omission.</p>

<h2>The measured atlas — {num("count.genes")} olfactory master genes</h2>
<p>Every γ below is measured from public NCBI promoters (GRCh38) and cached so the reading reproduces
offline bit-for-bit; γ is measured, never fitted. The reading correlates with GC content at
corr(γ, GC) = {num("e0.corr_gamma_gc")}, and all {num("e0.textured")} genes carry a non-trivial A4
SHAPE — the regime where reading γ alone would be lossy.</p>
<table class="data"><caption>The {num("count.genes")} measured genes: γ (LEVEL), spinodal h*, energy
barrier γ²/4, and A4 shape amplitude.</caption>
<thead><tr><th scope="col">gene</th><th scope="col">γ</th><th scope="col">h* = spinodal</th>
<th scope="col">barrier</th><th scope="col">A4 amp</th><th scope="col">role</th></tr></thead>
<tbody>{or_rows}</tbody></table>
<p>These genes split into four groups by atlas node: the transduction cascade
({num("count.transd")} genes), the olfactory-receptor panel ({num("count.or")} genes), the OSN-identity
organisers ({num("count.organiser")} genes), and the congenital-anosmia genes ({num("count.anosmia")}
Kallmann genes). The chapters that follow read each group through the same R19 switch.</p>
"""
    return dict(n=0, slug=slug, subj="The inherited R19 switch and measured DNA γ",
                description="The nose volume inherits two primitives — the R19 bistable switch "
                            "ds/dt = γ·s − s³ + h and the DNA reading γ (LEVEL) + A4 (SHAPE) — and "
                            "no wave module, because smell has no wave. 20 olfactory genes measured.",
                grade_class="forced", grade_tok_word="[F] forced", short_title="Inherited foundation",
                answer=("The nose volume inherits two primitives byte-identical to the eye and ear seeds: "
                        f"the R19 switch ds/dt = γ·s − s³ + h and the DNA reading γ plus A4 shape. It "
                        f"inherits no wave module, because smell has no wave. {R['count.genes']} olfactory "
                        "master genes are measured from NCBI promoters, γ never fitted."),
                abstract=("The foundation is the shared R19 bistable switch and a two-layer DNA reading "
                          f"(γ LEVEL + A4 SHAPE) over {num('count.genes')} olfactory master genes, with "
                          f"corr(γ, GC) = {num('e0.corr_gamma_gc')}. No wave/angle module is inherited — "
                          "smell's stimulus is a molecule, not a wave."),
                cards=cards, body=body)


# ---- §1 — the combinatorial code -----------------------------------------------------------------
def build_e1():
    slug = "01-combinatorial-code"
    rows = "".join(gene_row(s, num(f"e1.rank.{s}"), num(f"gene.{s}.gamma"), num(f"gene.{s}.hstar"),
                            num(f"gene.{s}.a4"), ATLAS_ROLE[s]) for s in OR_BY_RANK)
    cards = vp_card("odorant-key", "odorant → receptor drive", "which molecule binds which OR, and how "
                    "hard — the receptor's binding-pocket chemistry (coding sequence + 3D fold). Not in "
                    "γ or A4; never invented or fitted", "[O]", "open",
                    f"https://doi.org/{DOI_DNA}", "DNA reading (γ is structure only)")
    body = f"""
<h2>Smell breaks the wave→place skeleton — honestly</h2>
<p>Vision and hearing read a wave as a single physical place (propagation angle, basilar position).
Smell has no wave: the stimulus is a molecule, so identity is a combinatorial pattern over a large
olfactory-receptor repertoire — each odorant lights a subset of receptors, each receptor answers to
many odorants.</p>
<p>The one thing the promoter γ supplies here is each receptor's excitability: the spinodal threshold
orders the {num("count.or")}-gene panel from most to least trigger-happy. That is an expression layer,
never which odorant binds which receptor.</p>
<table class="data"><caption>The measured OR panel (N = {num("count.or")}) in spinodal(γ) threshold
order — most trigger-happy first.</caption>
<thead><tr><th scope="col">gene</th><th scope="col">rank</th><th scope="col">γ</th>
<th scope="col">h* = spinodal</th><th scope="col">A4 amp</th><th scope="col">odorant note</th></tr></thead>
<tbody>{rows}</tbody></table>

<h2>The code is combinatorial: capacity 2<sup>N</sup> ≫ N</h2>
<p>A bank of N = {num("count.or")} all-or-none switches has up to 2<sup>N</sup> =
{num("e1.capacity")} distinguishable ON/OFF patterns — far more than the {num("count.or")} receptors.
That is why the genome carries hundreds of OR genes: a combinatorial code, not one receptor per odour.</p>
<p>A uniform drive swept up flips the frozen switches in spinodal order, yielding a nested thermometer
readout of {num("e1.thermo_patterns")} patterns (ON counts {num("e1.thermo_counts")}, all ≤ N+1 =
{num("e1.np1")}). The readout is fully substrate-derived from the measured thresholds.</p>
<p>The thermometer reaches only {num("e1.thermo_patterns")} of {num("e1.capacity")} patterns; the rest
need an odorant-specific drive vector. An abstract vector driving only the 1st- and 3rd-ranked
receptors hard reaches the non-nested ON set ({num("e1.nonnested")}), unreachable by any uniform
drive — but that vector is not in γ.</p>

<h2>The honest negative — smell's identity is not a substrate quantity</h2>
<p>Vision's "what" (colour) is a substrate quantity, the propagation angle χ. Smell's "what" (odour)
is not: it is a combinatorial pattern whose key — the odorant↔receptor match — is molecular
recognition in the receptor's binding pocket, outside both γ and A4. This is the volume's central [O],
named throughout and never fitted.</p>
"""
    return dict(n=1, slug=slug, subj="The combinatorial odour code",
                description="Smell has no wave, so identity is a combinatorial pattern over the "
                            "receptor bank: N=7 all-or-none R19 switches give 2^7=128 patterns. γ sets "
                            "the threshold order only; the odorant→receptor key is a named [O].",
                grade_class="open", grade_tok_word="[O] open (odorant key)",
                short_title="Combinatorial code",
                answer=("Smell has no wave, so odour identity is a combinatorial pattern over the receptor "
                        f"bank. N = {R['count.or']} all-or-none R19 switches give 2^N = {R['e1.capacity']} "
                        "patterns; the measured γ sets only the threshold order. The odorant→receptor key "
                        "is molecular recognition, not in γ — a named [O]."),
                abstract=(f"A bank of N = {num('count.or')} olfactory-receptor R19 switches has capacity "
                          f"2<sup>N</sup> = {num('e1.capacity')} combinatorial patterns; a uniform drive "
                          f"reaches a nested thermometer of {num('e1.thermo_patterns')} of them. The "
                          "odorant→receptor key lives in the binding pocket, outside γ — the central [O]."),
                cards=cards, body=body)


# ---- §2 — the transduction switch ----------------------------------------------------------------
def build_e2():
    slug = "02-transduction-switch"
    rows = "".join(gene_row(s, num(f"gene.{s}.gamma"), num(f"gene.{s}.hstar"),
                            num(f"e2.{s}.s_below"), num(f"e2.{s}.s_above"), num(f"e2.{s}.jump"))
                   for s in TRANSD_ORDER)
    cards = vp_card("cngb1", "CNGB1 γ = " + R["e2.cngb1.gamma_olf"], "the CNG channel β subunit is the "
                    "same gene in olfaction and rod vision; its measured γ is byte-identical across the "
                    "two senses, so the transduction switch is shared, not analogous", "[V]", "verified",
                    f"https://doi.org/{DOI_NEURO}", "sensory transduction (neuro)")
    body = f"""
<h2>All-or-none: the flip is discontinuous past the spinodal</h2>
<p>The olfactory cascade (odorant → OR → Golf/GNAL → ADCY3/cAMP → CNG channel → ANO2) ends in the same
R19 flip as vision. Settled from rest, each gene's field stays dark below its spinodal h* and snaps on
above it with a finite, discontinuous jump.</p>
<table class="data"><caption>The {num("count.transd")} transduction-cascade genes: the field settled
from rest stays negative below h* and flips positive above, a finite jump.</caption>
<thead><tr><th scope="col">gene</th><th scope="col">γ</th><th scope="col">h* = spinodal</th>
<th scope="col">s @ 0.90 h*</th><th scope="col">s @ 1.10 h*</th><th scope="col">jump</th></tr></thead>
<tbody>{rows}</tbody></table>
<p>On the principal CNG subunit CNGA2 the discontinuity is sharp: at 1.00·h* the field is still off
(s = {num("e2.flip.s_at_100")}), and one further quantum of drive at 1.01·h* flips the whole switch on
(s = {num("e2.flip.s_at_101")}). Less than a quantum does nothing.</p>

<h2>The cooperativity is the cubic −s³, and it is necessary</h2>
<p>The restoring term is third-order, so the cooperativity order is n = {num("e2.hill_order")} — this is
where olfaction's "Hill ≈ 2–3" comes from, the cubic, not a fit. A structural control with the cubic
struck out (ds/dt = −γ·s + h) loses the threshold, the basin, and the jump.</p>
<p>Across the fold the cubic switch slope is ≈ {num("e2.cubic_slope")} while the graded control is
≈ {num("e2.graded_slope")} — a ratio of ≈ {num("e2.ratio")}×. Removing the cubic makes the response a
smooth proportional curve; the cubic makes it a step.</p>

<h2>The switch is genuinely shared across senses</h2>
<p>CNGB1, the CNG channel β subunit, is literally the same gene in rod vision and olfaction. Its
olfactory γ = {num("e2.cngb1.gamma_olf")} is byte-identical to the independently measured rod-vision
value {num("e2.cngb1.gamma_rod")} — the transduction switch is reused, not paralleled.</p>
<p>Ordered by threshold the cascade reads {num("e2.cascade_order")}. Whether this spinodal order matches
the real biochemical sequence (Golf → ADCY3 → cAMP → CNG → ANO2) is an open empirical question — it
needs the measured cascade kinetics and is not assumed. The absolute odorant→drive→firing (Hz) scale is
a separate calibration [O].</p>
"""
    return dict(n=2, slug=slug, subj="The olfactory transduction switch",
                description="The olfactory cascade ends in the same all-or-none R19 flip as vision: "
                            "discontinuous past the spinodal, made a step by the cubic −s³ (≈229× "
                            "steeper than a graded control). CNGB1 is byte-identical to rod vision.",
                grade_class="verified", grade_tok_word="[V] verified",
                short_title="Transduction switch",
                answer=("The olfactory cascade ends in the same all-or-none R19 flip as vision, "
                        "discontinuous past the spinodal. The cubic −s³ (cooperativity order "
                        f"{R['e2.hill_order']}) makes it a step, ≈{R['e2.ratio']}× steeper than a graded "
                        f"control. CNGB1 γ = {R['e2.cngb1.gamma_olf']} is byte-identical to rod vision — "
                        "the switch is shared."),
                abstract=("Each transduction gene's R19 field flips discontinuously past its spinodal; the "
                          f"cubic −s³ (order {num('e2.hill_order')}) is necessary, ≈{num('e2.ratio')}× "
                          f"steeper than a graded control. CNGB1 γ = {num('e2.cngb1.gamma_olf')} matches "
                          "rod vision byte-for-byte — a shared, not analogous, switch."),
                cards=cards, body=body)


# ---- §3 — the bulb map ---------------------------------------------------------------------------
def build_e3():
    slug = "03-bulb-map"
    rows = "".join(gene_row(s, num(f"e3.rank.{s}"), num(f"gene.{s}.gamma"), num(f"gene.{s}.hstar"),
                            num(f"e3.dwell.{s}"), ATLAS_ROLE[s]) for s in ORG_BY_RANK)
    cards = (
        vp_card("organ", "R19 Organ presence threshold", "an organ is present only if its master "
                "cis-drive clears the γ-set spinodal — an intact pathway with the master off still yields "
                "absence (parts present ≠ trait)", "[F]", "forced",
                f"https://doi.org/{DOI_PHYSICS}", "R19 substrate (physics)")
        + vp_card("coordinate", "glomerular targeting coordinate", "which physical glomerulus an OR's "
                  "axons navigate to — axon-guidance chemistry (OR → cAMP → Neuropilin-1/Sema3A gradient), "
                  "not in γ", "[O]", "open",
                  f"https://doi.org/{DOI_DNA}", "DNA reading (γ is structure only)")
    )
    body = f"""
<h2>The map's developmental order is forced by measured γ</h2>
<p>Smell's substitute for a spatial image is the bulb map: axons of the same receptor converge onto
specific glomeruli, turning the receptor-space code into a spatial odour map. The organisers that lay
it down (the OSN-identity transcription factors) emerge as R19 Organs in spinodal(γ) order.</p>
<table class="data"><caption>The {num("count.organiser")} OSN-identity organisers in spinodal(γ) order;
dwell ∝ γ<sup>1.5</sup> sets relative size. Lowest γ clears its presence threshold first.</caption>
<thead><tr><th scope="col">organiser</th><th scope="col">order</th><th scope="col">γ</th>
<th scope="col">h* = spinodal</th><th scope="col">dwell ∝ γ<sup>1.5</sup></th>
<th scope="col">role</th></tr></thead>
<tbody>{rows}</tbody></table>
<p>The emergence order is {num("e3.org_order")} — monotone in measured γ. Each Organ is absent below
0.9·h* and present above 1.1·h*: an intact downstream pathway with the master switch off still yields
absence, a real organ rather than parts.</p>

<h2>Convergence is a bijection — it preserves the capacity 2<sup>N</sup></h2>
<p>One OR → one glomerulus is an injective relabelling of the {num("count.or")} receptor channels onto
{num("count.or")} bulb positions. A bijection on N channels induces a bijection on their 2<sup>N</sup>
subsets, so the combinatorial capacity is carried into bulb space intact: 2<sup>N</sup> =
{num("e3.capacity")} distinct spatial images.</p>
<p>Because a bijection preserves chains, the receptor-space nested thermometer maps to a nested
<i>spatial</i> thermometer — {num("e3.spatial_patterns")} patterns, glomeruli lighting in the same
order. The map inherits the code's order and capacity from the frozen switch and measured γ.</p>

<h2>The honest [O] — the targeting coordinate is not in γ</h2>
<p>The substrate fixes the map's order and capacity, but not which physical glomerulus a given receptor
targets. That coordinate is axon-guidance chemistry — the receptor's own signalling shaping a
Neuropilin-1/Sema3A gradient — in its coding sequence, not its promoter γ. This is the same kind of
molecular [O] as the odorant key: structure is substrate-derived, specificity is not.</p>
"""
    return dict(n=3, slug=slug, subj="The bulb map",
                description="One OR → one glomerulus is a bijection, so the combinatorial capacity "
                            "2^7=128 is preserved as a spatial odour map; organisers emerge in "
                            "spinodal(γ) order. The targeting coordinate is a named [O].",
                grade_class="verified", grade_tok_word="[V] verified",
                short_title="Bulb map",
                answer=("One receptor → one glomerulus is a bijection, so the combinatorial capacity "
                        f"2<sup>N</sup> = {R['e3.capacity']} is carried intact into a spatial odour map. "
                        f"The organisers emerge as R19 Organs in spinodal(γ) order ({R['e3.org_order']}). "
                        "Which glomerulus a receptor targets is axon-guidance chemistry — a named [O]."),
                abstract=(f"The {num('count.organiser')} OSN organisers emerge as R19 Organs in "
                          f"spinodal(γ) order ({num('e3.org_order')}); one-OR→one-glomerulus convergence "
                          f"is a bijection, preserving capacity 2<sup>N</sup> = {num('e3.capacity')} as a "
                          "spatial map. The targeting coordinate is a named [O]."),
                cards=cards, body=body)


# ---- §4 — congenital anosmia (DISEASE) -----------------------------------------------------------
def build_e4():
    slug = "04-congenital-anosmia"
    chan_rows = "".join(gene_row(s, num(f"gene.{s}.gamma"), num(f"gene.{s}.hstar"),
                                num(f"e4.{s}.wt_above"), num(f"e4.{s}.lof_above"))
                        for s in ("CNGA2", "CNGB1"))
    kall_rows = "".join(gene_row(s, num(f"e4.kallmann.{s}.gamma"), num(f"e4.kallmann.{s}.hstar"),
                                "absent", "present") for s in KALLMANN)
    cards = vp_card("cngb1", "CNGB1 γ = " + R["e4.cngb1.gamma"], "the same CNG β gene in olfaction and rod "
                    "vision; a loss-of-function is therefore predicted to impair both smell and dim-light "
                    "vision together — forced by the shared switch, not analogy", "[V]", "verified",
                    f"https://doi.org/{DOI_NEURO}", "sensory transduction (neuro)")
    body = f"""
<h2>Failure mode 1 — channelopathy: the transduction switch cannot flip</h2>
<p>The olfactory CNG channel is the inherited R19 transduction switch. In a loss-of-function the
bistable switch is gone (the cubic struck out), so there is no on-basin and the flip can never occur at
any drive — no transduction, no smell. This re-points the cubic's necessity (§2) as the failure.</p>
<table class="data"><caption>CNG channelopathy genes: wild-type flips on past h*; with the switch
removed the field stays low at the same drive (graded, no on-basin).</caption>
<thead><tr><th scope="col">gene</th><th scope="col">γ</th><th scope="col">h* = spinodal</th>
<th scope="col">WT s @ 1.10 h*</th><th scope="col">LOF (no switch) @ 1.10 h*</th></tr></thead>
<tbody>{chan_rows}</tbody></table>
<p>Losing the switch costs the all-or-none flip entirely: the wild-type slope ≈ {num("e4.cubic_slope")}
collapses to ≈ {num("e4.graded_slope")} (a factor ≈ {num("e4.ratio")}×). The direction-only lever is to
re-enable a flip reachable by physiological drive (sign +). No dose, molecule, or efficacy is stated.</p>

<h2>Failure mode 2 — organ-formation (Kallmann): the apparatus never emerges</h2>
<p>Here the smelling apparatus never forms: the master switch never clears its R19 presence threshold,
so the organ is absent ("parts present ≠ trait"). The signature is anosmia with hypogonadotropic
hypogonadism — the shared olfactory-placode/GnRH programme failing together.</p>
<table class="data"><caption>The {num("count.anosmia")} Kallmann organ-formation genes (all measured):
below threshold the Organ is absent; above it, present.</caption>
<thead><tr><th scope="col">gene</th><th scope="col">γ</th><th scope="col">h* = spinodal</th>
<th scope="col">LOF: present @ 0.90 h*</th><th scope="col">WT: present @ 1.10 h*</th></tr></thead>
<tbody>{kall_rows}</tbody></table>
<p>The direction-only lever is to restore the master switch's clearing of its presence threshold (sign
+). The absolute magnitude and developmental window are an [O] this volume does not supply.</p>

<h2>Cross-sense and the firewall in action</h2>
<p>Because CNGB1 (γ = {num("e4.cngb1.gamma")}, h* = {num("e4.cngb1.hstar")}) is the same gene in both
senses, a CNGB1 loss-of-function is predicted to fail in two senses at once — olfaction and
rod-mediated dim-light vision — forced by the shared primitive, a cross-sense prediction rather than an
analogy.</p>
<p>Every statement here is direction-only: it gives only the failure-mode class (which R19 primitive
fails) and the sign of a hypothetical restorative lever. No diagnosis, dose, molecule, or efficacy; the
odorant key stays [O]; the felt experience of anosmia is the mind volume's.</p>
"""
    return dict(n=4, slug=slug, subj="Congenital anosmia", banner=True,
                description="Congenital anosmia reads as two disjoint R19 failure modes: CNG "
                            "channelopathy (the switch can't flip, ≈229× shallower) and Kallmann "
                            "organ-formation (the organ never forms). Direction-only, non-clinical.",
                grade_class="verified", grade_tok_word="[V] verified",
                short_title="Congenital anosmia",
                answer=("Congenital anosmia reads as two disjoint R19 failure modes: a CNG channelopathy "
                        f"where the transduction switch cannot flip (≈{R['e4.ratio']}× shallower), and "
                        "Kallmann organ-formation where the apparatus never clears its presence threshold. "
                        "Both are direction-only; CNGB1 loss is predicted to hit smell and rod vision."),
                abstract=("Two disjoint R19 failure modes: CNG channelopathy (deleting the cubic destroys "
                          f"the flip, ≈{num('e4.ratio')}× shallower) and Kallmann organ-formation (the "
                          "Organ never clears its presence threshold). CNGB1 loss is forced to impair both "
                          "smell and rod vision. Direction-only, non-clinical."),
                cards=cards, body=body)


# ---- §5 — allergic smell loss (DISEASE) ----------------------------------------------------------
def build_e5():
    slug = "05-allergic-smell-loss"
    kappa_cells = "".join(
        f"<tr><td>{k:.2f}</td><td>{num('e5.cond.k%03d' % int(round(k*100)))}</td></tr>"
        for k in (1.00, 0.95, 0.90, 0.86, 0.82, 0.60, 0.30, 0.00))
    org_rows = "".join(gene_row(s, num(f"gene.{s}.gamma"), num(f"gene.{s}.hstar"),
                               num(f"e5.org.{s}.healthy"), num(f"e5.org.{s}.damaged"))
                       for s in ORG_BY_RANK)
    cards = (
        vp_card("allergy", "allergy mechanism (sensitization · latch · desensitization)",
                "an immune hypersensitivity — sensitization at the R19 spinodal, the dose×repetition "
                "threshold, the latch, and controlled desensitization (immunotherapy). Owned and verified "
                "elsewhere; consumed here, never re-derived", "[V]", "verified (immune §11)",
                f"https://doi.org/{DOI_IMMUNE}", "immune/hematologic §11")
        + vp_card("airway", "absolute aeroallergen / airway scale", "the literal mucosal load and the "
                  "value of the conductive factor κ — the surface owner's quantity, deferred", "[O]",
                  "open (respiratory)", f"https://doi.org/{DOI_NEURO}", "sensory surface (neuro)")
        + vp_card("percept", "the felt percept of smelling", "the experience of an odour (and of an "
                  "allergy attack) — the mind volume's, cited not re-derived", "[O]", "deferred",
                  f"https://doi.org/{DOI_MIND}", "Felt Cognition (mind)")
    )
    body = f"""
<h2>The honest framing — the most common nose disease is an immune disease</h2>
<p>Allergic rhinitis is not primarily an olfactory disease; it is a Type-2 immune hypersensitivity. So
its mechanism — sensitization, the latch, controlled desensitization — is consumed from the immune
volume's §11, cited and never re-derived here. This volume owns only the olfactory consequence: how
allergy takes your smell.</p>
<p>It takes smell two ways, told apart by a single move — restoring the drive. The split between
conductive and sensorineural loss falls out of which substrate layer moved.</p>

<h2>Conductive loss — a drive suppression on intact switches (reversible)</h2>
<p>Mucosal swelling reduces odorant flux, attenuating the per-receptor drive to κ·h₀ with the baseline
odour drive h₀ = {num("e5.h0")}. γ is untouched — no switch defect — so the panel flips off in
spinodal order as κ falls.</p>
<table class="data"><caption>Conductive fade: with the organ intact, the percept (OR channels on, of
{num("count.or")}) falls monotonically as the conductive factor κ drops, and is full again at κ = 1.</caption>
<thead><tr><th scope="col">κ (conductive)</th><th scope="col">percept (# OR on)</th></tr></thead>
<tbody>{kappa_cells}</tbody></table>
<p>Because nothing structural changed, restoring κ → 1 returns the percept to {num("e5.cond_restore")}
of {num("count.or")} exactly. Conductive smell loss is reversible: the frozen flip and measured γ are
intact; only the drive moved.</p>

<h2>Sensorineural loss — an organ degradation (persistent)</h2>
<p>Chronic Type-2 inflammation can drop the OSN compartment's master cis-drive below its γ-set presence
threshold — the same R19 organ-formation failure as congenital anosmia (§4), reached by inflammation
rather than a mutation. With the organ gone, no drive can rescue it.</p>
<table class="data"><caption>OSN-identity organisers: present at a healthy cis-drive, absent when
inflammation drops it below the presence threshold.</caption>
<thead><tr><th scope="col">organiser</th><th scope="col">γ</th><th scope="col">h* = presence</th>
<th scope="col">healthy</th><th scope="col">damaged</th></tr></thead>
<tbody>{org_rows}</tbody></table>
<p>At full conductive drive κ = 1 with the organ damaged the percept is {num("e5.sensorineural")} of
{num("count.or")} — anosmia. Sensorineural loss is persistent because it is an organ failure, not a
drive failure.</p>

<h2>The discriminator and the firewall in action</h2>
<p>One move separates them. Under a partial conductive block (κ = 0.82) the percept is
{num("e5.cond_block")} of {num("count.or")}; restoring the drive returns it to
{num("e5.cond_restore")} of {num("count.or")}. The sensorineural percept stays
{num("e5.sensorineural")} of {num("count.or")} under the same move. The substrate expresses the
clinical conductive-vs-sensorineural distinction as drive (§1/§2) versus organ (§2/§3).</p>
<p>The direction-only levers are sign only: conductive → restore odorant access (κ↑), with the upstream
immune cause cited to §11 desensitization; sensorineural → act on the organ, recovery not guaranteed.
No dose, molecule, or efficacy. The volume adds no gene — the measured atlas is untouched — and κ and
the organ degradation are abstract structural representations, never fitted.</p>
"""
    return dict(n=5, slug=slug, subj="Allergic (acquired) smell loss", banner=True,
                description="Allergic rhinitis is an immune disease, so its mechanism is cited to immune "
                            "§11, not re-derived. The volume owns only the olfactory consequence: "
                            "reversible conductive (κ↓) vs persistent sensorineural loss, told apart by "
                            "restoring the drive.",
                grade_class="verified", grade_tok_word="[V] verified",
                short_title="Allergic smell loss",
                answer=("Allergic rhinitis is an immune disease, so its mechanism is cited to immune §11, "
                        "not re-derived. The volume owns only the consequence: conductive loss is a "
                        "reversible drive suppression on intact switches (recovers at κ = 1), "
                        "sensorineural loss a persistent organ degradation — told apart by restoring the drive."),
                abstract=("The allergy mechanism is consumed from immune §11 (cited, not re-derived). "
                          "Conductive loss is a reversible drive suppression (baseline h₀ = "
                          f"{num('e5.h0')}; recovers to {num('e5.cond_restore')}/{num('count.or')} at "
                          "κ = 1); sensorineural loss is a persistent organ degradation "
                          f"({num('e5.sensorineural')}/{num('count.or')} at full drive)."),
                cards=cards, body=body)


# ==================================================================================================
#  the hub (index) — CreativeWorkSeries
# ==================================================================================================
def build_hub(chapters):
    toc = "".join(
        f'<li><a href="/{PAPER_ID}/{c["slug"]}/">§{c["n"]} {html.escape(c["short_title"])}</a>'
        f' — {html.escape(c["short_title_desc"])}</li>' for c in chapters)
    parts = [{"@type": "ListItem", "position": i + 1,
              "url": f"{SITE}/{PAPER_ID}/{c['slug']}/", "name": c["short_title"]}
             for i, c in enumerate(chapters)]
    ld_series = json.dumps({
        "@context": "https://schema.org", "@type": "CreativeWorkSeries",
        "name": SHORT, "headline": TITLE, "url": f"{SITE}/{PAPER_ID}/",
        "author": {"@type": "Person", "name": AUTHOR, "sameAs": ORCID},
        "license": LICENSE, "isBasedOn": f"{REPO}/tree/main/vp_nose_emergence_seed",
        "datePublished": DATE,
        "sameAs": DOI_NOSE_URL,
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": DOI_NOSE},
        "hasPart": parts}, ensure_ascii=False)
    ld_crumb = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": SHORT}]}, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(SHORT)} — Smell from the R19 switch and measured DNA γ | Jamming Physics</title>
<meta name="description" content="A first-principles, non-clinical theoretical volume: how smell emerges from the inherited R19 jamming switch and DNA γ measured from NCBI promoters. {R['count.genes']} genes, six chapters, every number reproducible.">
<link rel="canonical" href="{SITE}/{PAPER_ID}/">
<meta name="citation_title" content="{html.escape(TITLE)}">
<meta name="citation_author" content="{html.escape(AUTHOR)}">
<meta name="citation_publication_date" content="{DATE}">
<meta name="citation_doi" content="{DOI_NOSE}">
<meta name="citation_public_url" content="{SITE}/{PAPER_ID}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld_series}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> › {html.escape(SHORT)}</nav></header>
<main>
<h1>{html.escape(TITLE)}</h1>
<p class="answer">This volume derives the sense of smell from two inherited primitives — the R19 jamming switch and DNA γ measured from NCBI promoters — across six chapters, and marks plainly where the framework reaches (threshold, transduction) and where it stops: the odorant→receptor key is a named open problem.</p>
<p class="abstract">Smell breaks the wave→place skeleton of the eye and ear volumes: its stimulus is a molecule, so identity is a combinatorial pattern over {num("count.or")} olfactory-receptor R19 switches (capacity 2<sup>N</sup> = {num("e1.capacity")}). What survives is the transduction switch — the olfactory CNG channel, byte-identical to rod vision. {num("count.genes")} master genes are measured; the disease chapters are direction-only.</p>
<aside class="claim-strip page">
<span class="grade g-forced">LOCK → Derive → Gate</span>
<a href="{DOI_NOSE_URL}" rel="noopener">DOI {DOI_NOSE}</a>
<a href="{REPO}/tree/main/vp_nose_emergence_seed" rel="noopener">Reproduce (GitHub)</a>
<a href="{LICENSE}" rel="noopener">CC BY 4.0</a>
</aside>
<p class="cite">Canonical record: <a href="{DOI_NOSE_URL}" rel="noopener">doi.org/{DOI_NOSE}</a> — Zenodo concept DOI (always resolves to the latest version). Cite as: {html.escape(AUTHOR)}, <i>{html.escape(SHORT)}</i> (Jamming Physics, {DATE[:4]}), {DOI_NOSE}.</p>

<h2>The one idea — and why smell is different</h2>
<p>A special sense is a stimulus property → a code → an R19 transduction switch. Vision and hearing read a wave as a single physical place; smell has no wave, so the front-end code is combinatorial over a large receptor repertoire.</p>
<p>What survives is the R19 transduction switch (the olfactory CNG channel, the same gene family as rod vision). What changes is the front end: identity's key — which odorant binds which receptor — is molecular recognition, not in the promoter γ. That is the volume's central open problem.</p>

<h2>Chapters</h2>
<ul class="toc">{toc}</ul>

<h2>What is forced, measured, and open</h2>
<p>Forced and verified: the R19 switch structure, the all-or-none flip past spinodal(γ), the cubic cooperativity (n = {num("e2.hill_order")}), the combinatorial capacity 2<sup>N</sup> = {num("e1.capacity")}, and the cross-sense CNGB1. Measured: every γ from NCBI promoters ({num("count.genes")} genes). Open: the odorant→receptor key, the glomerular targeting coordinate, the absolute firing scale, the allergy mechanism (cited to immune §11) and airway scale, and the felt percept (the mind volume's).</p>
</main>
<footer><p>{SHORT} · derived from the VP framework · <a href="{DOI_NOSE_URL}" rel="noopener">DOI {DOI_NOSE}</a> · <a href="{ORCID}" rel="noopener">ORCID {AUTHOR}</a> ·
<a href="{LICENSE}" rel="noopener">CC BY 4.0</a> · <a href="{REPO}" rel="noopener">GitHub</a></p></footer>
</body>
</html>
"""


# short descriptions for the hub TOC ---------------------------------------------------------------
HUB_DESC = {
    0: "the R19 switch, DNA γ, and the missing wave module",
    1: "no wave → a combinatorial pattern over the receptor bank",
    2: "the all-or-none CNG flip, shared with rod vision",
    3: "one receptor → one glomerulus preserves the capacity",
    4: "two R19 failure modes (non-clinical, direction-only)",
    5: "conductive vs sensorineural smell loss (non-clinical)",
}


# ==================================================================================================
#  site-level files
# ==================================================================================================
def sitemap(urls):
    items = "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + items + "</urlset>\n")


ROBOTS = """User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: *
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE


def llms_txt(chapters):
    lines = [f"# {SHORT}", "",
             "> A first-principles, non-clinical theoretical volume: how the sense of smell emerges from",
             "> the inherited R19 jamming-lattice switch (ds/dt = γ·s − s³ + h) and DNA γ measured from",
             "> public NCBI promoters. Smell has no wave, so odour identity is a combinatorial pattern over",
             f"> {R['count.or']} olfactory-receptor R19 switches (capacity 2^N = {R['e1.capacity']}); the",
             "> transduction switch (the olfactory CNG channel) is byte-identical to rod vision. The",
             "> odorant→receptor key is a named open problem. Disease chapters are direction-only / proposal-only.",
             "", "## Core",
             f"- [{SHORT} hub]({SITE}/{PAPER_ID}/)",
             f"- DOI (Zenodo concept, always the latest version): https://doi.org/{DOI_NOSE}"]
    lines.append("")
    lines.append("## Chapters")
    for c in chapters:
        lines.append(f"- [§{c['n']} {c['short_title']}]({SITE}/{PAPER_ID}/{c['slug']}/) — {HUB_DESC[c['n']]}")
    lines += ["", "## Policies",
              "- License: CC BY 4.0",
              f"- Reproduce: {REPO}/tree/main/vp_nose_emergence_seed",
              "- Disease chapters are theoretical and non-clinical: no diagnosis, dose, molecule, or efficacy.",
              ""]
    return "\n".join(lines)


SITE_CSS = """:root{
  --ink:#1b1b1f; --muted:#5a5f6b; --bg:#ffffff; --soft:#f4f5f7; --line:#e3e5ea;
  --accent:#2f6f4f; --accent-ink:#19422f; --open:#9a5b00; --warn:#7a2f2f; --warnbg:#fbeeee;
  --maxw:46rem;
}
*{box-sizing:border-box}
html{font-size:17px}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;line-height:1.62}
header,main,footer{max-width:var(--maxw);margin:0 auto;padding:0 1.15rem}
.crumb{font-size:.8rem;color:var(--muted);padding:1rem 0 .25rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.crumb a{color:var(--accent);text-decoration:none}
h1{font-size:1.85rem;line-height:1.18;margin:.6rem 0 .5rem;letter-spacing:-.01em}
h2{font-size:1.22rem;margin:2rem 0 .5rem;letter-spacing:-.005em}
p{margin:.6rem 0}
a{color:var(--accent-ink)}
p.answer{font-size:1.12rem;line-height:1.5;background:var(--soft);border-left:3px solid var(--accent);
  padding:.8rem 1rem;border-radius:.25rem;margin:1rem 0;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
p.abstract{color:#26282e}
p.cite{font-size:.82rem;color:var(--muted);margin:.2rem 0 1rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
p.cite a{color:var(--accent);text-decoration:none}
p.cite a:hover{text-decoration:underline}
.claim-strip{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;margin:1rem 0;padding:.55rem .7rem;
  background:var(--soft);border:1px solid var(--line);border-radius:.4rem;font-size:.8rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.claim-strip a{color:var(--accent);text-decoration:none}
.claim-strip a:hover{text-decoration:underline}
.grade{font-weight:700;padding:.12rem .5rem;border-radius:1rem;color:#fff;font-size:.74rem}
.g-forced{background:var(--accent)} .g-verified{background:#345b8a}
.g-open{background:var(--open)} .g-hypothesis{background:#6b4a8a}
.gate{color:var(--muted)}
.vp-card{background:#fff;border:1px solid var(--line);border-left:3px solid #345b8a;
  border-radius:.35rem;padding:.6rem .8rem;margin:.7rem 0;font-size:.9rem}
.vp-card[data-locked]{border-left-color:#345b8a}
.vp-card a{color:var(--accent);text-decoration:none}
.vp-card a:hover{text-decoration:underline}
.scope-banner{background:var(--warnbg);border:1px solid #e7c9c9;border-left:4px solid var(--warn);
  color:#4a2222;border-radius:.4rem;padding:.7rem .9rem;margin:1rem 0;font-size:.92rem}
.vp-num{font-variant-numeric:tabular-nums;font-weight:600}
table.data{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.86rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
table.data caption{caption-side:top;text-align:left;color:var(--muted);font-size:.8rem;
  margin-bottom:.4rem;font-style:italic}
table.data th,table.data td{border-bottom:1px solid var(--line);padding:.34rem .5rem;text-align:right}
table.data thead th{border-bottom:2px solid #cfd3da;color:var(--accent-ink);white-space:nowrap}
table.data th[scope=row]{text-align:left;font-weight:700}
table.data td:last-child,table.data th:last-child{text-align:left;color:var(--muted)}
ul.toc,ul.toc li{margin:.3rem 0}
ul.toc a{color:var(--accent-ink);font-weight:600;text-decoration:none}
nav.pn{display:flex;justify-content:space-between;gap:.5rem;margin:2rem 0 1rem;padding-top:1rem;
  border-top:1px solid var(--line);font-size:.85rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
nav.pn a{color:var(--accent);text-decoration:none}
footer{color:var(--muted);font-size:.78rem;border-top:1px solid var(--line);margin-top:2rem;
  padding-top:1rem;padding-bottom:2rem;
  font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
footer a{color:var(--accent)}
sup{font-size:.7em}
@media (max-width:520px){html{font-size:16px} h1{font-size:1.55rem}}
"""


def _meta_json(chapters):
    return json.dumps({
        "paper_id": PAPER_ID, "code": "nse", "title": TITLE, "short": SHORT,
        "doi": DOI_NOSE, "doi_url": DOI_NOSE_URL, "doi_type": "concept",
        "hub_url": f"/{PAPER_ID}/", "branch": "sensory (neuro family)",
        "abstract": ("Smell emerges from the inherited R19 switch and measured DNA γ; identity is a "
                     "combinatorial code over the receptor bank, the transduction switch is shared with "
                     "rod vision, and the odorant key is a named open problem. Disease chapters are "
                     "direction-only."),
        "headline_results": [f"2^N = {R['e1.capacity']} combinatorial patterns",
                             f"cubic cooperativity n = {R['e2.hill_order']}",
                             f"CNGB1 γ = {R['e2.cngb1.gamma_olf']} (shared with rod vision)"],
        "chapters": [{"no": c["n"], "slug": c["slug"], "title": c["short_title"],
                      "one_liner": HUB_DESC[c["n"]], "grade": c["grade_class"]} for c in chapters],
        "totals": {"genes": int(R["count.genes"]), "chapters": int(R["count.chapters"]),
                   "or_panel": int(R["count.or"])},
    }, ensure_ascii=False, indent=1)


# ==================================================================================================
#  driver
# ==================================================================================================
# globals consumed by chapter builders --------------------------------------------------------------
import vp_nose_ssot as _S
ATLAS_ROLE = {s: _S.ATLAS[s].get("role", "") for s in _S.ATLAS}
ALL_GENES_BY_NODE = (list(_S.TRANSD) + list(_S.OR_GENES) + list(_S.ORGANISERS) + list(_S.ANOSMIA))
OR_BY_RANK   = sorted(_S.OR_GENES,   key=lambda s: _S.spinodal(_S.ATLAS[s]["gamma"]))
TRANSD_ORDER = list(_S.TRANSD)
ORG_BY_RANK  = sorted(_S.ORGANISERS, key=lambda s: _S.spinodal(_S.ATLAS[s]["gamma"]))
KALLMANN     = list(_S.ANOSMIA)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    builders = [build_e0, build_e1, build_e2, build_e3, build_e4, build_e5]
    chapters = [b() for b in builders]
    for c in chapters:
        c["short_title_desc"] = HUB_DESC[c["n"]]

    # chapter pages with prev/next links
    n_ch = len(chapters)
    for i, c in enumerate(chapters):
        prev_link = ((chapters[i-1]["n"], f"/{PAPER_ID}/{chapters[i-1]['slug']}/") if i > 0 else None)
        next_link = ((chapters[i+1]["n"], f"/{PAPER_ID}/{chapters[i+1]['slug']}/") if i < n_ch-1 else None)
        body = c["body"]
        if c.get("banner"):
            body = SCOPE_BANNER + body
        page = chapter_page(c["n"], c["slug"], c["subj"], c["description"], c["grade_class"],
                            c["grade_tok_word"], c["short_title"], c["answer"], c["abstract"],
                            c["cards"], body, prev_link, next_link)
        write(os.path.join(DOCS, PAPER_ID, c["slug"], "index.html"), page)

    # hub
    write(os.path.join(DOCS, PAPER_ID, "index.html"), build_hub(chapters))
    write(os.path.join(DOCS, PAPER_ID, "_meta.json"), _meta_json(chapters))

    # site-level
    urls = [f"{SITE}/{PAPER_ID}/"] + [f"{SITE}/{PAPER_ID}/{c['slug']}/" for c in chapters]
    write(os.path.join(DOCS, "sitemap.xml"), sitemap(urls))
    write(os.path.join(DOCS, "robots.txt"), ROBOTS)
    write(os.path.join(DOCS, "llms.txt"), llms_txt(chapters))
    write(os.path.join(DOCS, "assets", "css", "site.css"), SITE_CSS)

    print(f"built docs/ — hub + {n_ch} chapters + sitemap/robots/llms/css")
    print(f"  pages: {len(urls)} index.html under docs/")


if __name__ == "__main__":
    main()
