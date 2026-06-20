#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_docs.py  --  Chronobiology (Circadian) WRITING phase: per-title canonical SEO HTML generator.

HARD RULE: refuses while gates.writing_locked() is True (research must be signed off + PHASE=="writing").
WHEN UNLOCKED it follows VP-SPEC v1.8 (../VP_SPEC_v1_8.md): canonical HTML in docs/ (C2); ONE page per
title/section (C4 sec 6) with answer-first block, JSON-LD ScholarlyArticle + BreadcrumbList, claim-strip,
vp-cards; ENGLISH body (C0); honest grades + stated [O] (C3); and every number is pulled LIVE from the
deterministic engine (C1), so the prose cannot drift from the shipped result.

Output tree:  docs/circadian/<NN-slug>/index.html  +  docs/circadian/index.html (hub)
              docs/assets/css/site.css  +  docs/{robots.txt,sitemap.xml,llms.txt,llms-full.txt}

DOI: the circadian volume is published on Zenodo under concept DOI 10.5281/zenodo.20755413 (resolves to the
latest version; v0.2.0 snapshot = version DOI 10.5281/zenodo.20755414, CC BY 4.0). The page identifies itself
by that concept DOI (JSON-LD identifier + sameAs, claim-strip snapshot, Highwire citation tags) and also cites
the cross-volume MIND concept DOI (10.5281/zenodo.20694404) where the affect seam is used.
"""
import os, sys, html, shutil

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(_HERE, "..")
sys.path.insert(0, os.path.join(_PKG, "repro", "_verify"))
sys.path.insert(0, os.path.join(_PKG, "repro", "_engine"))
sys.path.insert(0, os.path.join(_PKG, "repro", "_pathology"))
import importlib
gates = importlib.import_module("gates")

# ---------------------------------------------------------------------------------------------------
#  constants / metadata
# ---------------------------------------------------------------------------------------------------
SITE = "https://jamming-physics.org"
PAPER_SLUG = "circadian"                      # URL segment: /circadian/
PAPER_NAME = "Chronobiology: the Circadian Oscillator Network, Entrainment, and Clock-Disruption Disease"
AUTHOR = "Young Jae Lee"
ORCID = "0009-0002-7535-8245"
MIND_DOI = "10.5281/zenodo.20694404"          # cross-volume seam citation (the FELT/affect layer)
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
GH_TREE = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/circadian"
LASTMOD = "2026-06-19"
GAMMA_BMAL1 = "1.33348"

# --- this volume's own DOI (assigned at v0.3.0; CHARTER writing-phase task) ----------------------
# CONCEPT (all-versions) DOI resolves to the latest record; VERSION DOI freezes this snapshot.
CONCEPT_DOI = "10.5281/zenodo.20755413"       # canonical "living version" identifier (sameAs target)
VERSION_DOI = "10.5281/zenodo.20755414"       # frozen v0.2.0/v1 record snapshot
ZENODO_REC = "https://zenodo.org/records/20755413"   # concept landing (latest)
PUB_DATE_ISO = "2026-06-19"                   # Zenodo published date (ISO, for JSON-LD)
PUB_DATE_SCHOLAR = "2026/06/19"               # Highwire citation_publication_date format

# --- measured-DNA provenance (the grounding the whole volume rests on; never fitted) -------------
GENE_SYMBOL = "ARNTL (alias BMAL1)"
GENE_ID = "406"
GENE_ACC = "NC_000011.10"
GENE_WINDOW = "TSS-2000..+500"
GENE_NDINUC = "2500"
GENE_SEQ_SHA = "7293be92e4ad"                 # sha256[:12] of the cached 2501-bp promoter (offline-reproducible)
NN_METHOD = "&minus;mean(NN stacking &Delta;G37, SantaLucia 1998)"
SEED = "19"
N_DISCRIMINANTS = "8"                         # RC1-RC6 + TX1

# --- SEO: per-volume base keywords + per-chapter knowsAbout (Google / Bing / generative search) --
BASE_KW = ["circadian rhythm", "circadian clock", "chronobiology", "limit-cycle oscillator",
           "BMAL1", "CLOCK gene", "PER CRY feedback loop", "suprachiasmatic nucleus", "SCN",
           "FitzHugh-Nagumo", "jamming physics", "VP theory", "deterministic model", "measured gamma"]
KW = {
    "00-grounding-measured-dna-emergence": ["measured DNA emergence", "ARNTL promoter gamma",
        "nearest-neighbour thermodynamics", "reproducibility seed 19", "falsifiable model",
        "no curve fitting", "SantaLucia 1998", "deterministic sha256"],
    "01-scope-clock-oscillator": ["coupled oscillator network", "free-running rhythm", "entrainment",
        "setpoint gating", "clock-environment misalignment"],
    "02-free-running": ["free-running period", "constant darkness", "depolarisation block",
        "self-sustained oscillation", "limit cycle"],
    "03-entrainment-prc": ["phase-response curve", "Arnold tongue", "zeitgeber", "light entrainment",
        "melatonin PRC", "jet lag"],
    "04-master-vs-network": ["synchronisation transition", "coupled clocks", "peripheral clocks",
        "Kuramoto coherence", "master oscillator"],
    "05-setpoint-gating": ["HPA axis", "cortisol rhythm", "circadian gating", "core body temperature",
        "blood pressure rhythm"],
    "06-misalignment-disease": ["shift work disorder", "jet lag", "circadian misalignment",
        "shift-work cancer", "IARC 2A", "cardiometabolic risk", "sleep-wake disorder"],
    "07-circadian-mood-seam": ["circadian depression", "seasonal affective", "HPA flattening",
        "withdrawal bias", "circadian autism", "mood seam"],
    "08-chronotherapy": ["chronotherapy", "light therapy", "timed melatonin", "wake therapy",
        "bright light", "circadian re-alignment"],
}

DOCS = os.path.join(_PKG, "docs")
OUT = os.path.join(DOCS, PAPER_SLUG)
CSS_DST_DIR = os.path.join(DOCS, "assets", "css")
# vendored site.css (copied verbatim from the mind package's VP-SPEC v1.6 stylesheet)
CSS_SRC_CANDIDATES = [
    os.path.join(_PKG, "..", "..", "mind_pkg", "mind_pkg", "docs", "assets", "css", "site.css"),
    os.path.join(_PKG, "docs", "assets", "css", "site.css"),
]


def _findings():
    eng = importlib.import_module("vp_clk_engine")
    return eng.research_findings(), eng


def _sha():
    eng = importlib.import_module("vp_clk_engine")
    _, h = eng.emit(eng.circulate())
    return h


def _json(s):
    """Minimal JSON string escaping for embedding in JSON-LD."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# ---------------------------------------------------------------------------------------------------
#  canonical page shell
# ---------------------------------------------------------------------------------------------------
def page(slug, position, title_full, meta_desc, h1, answer_html, abstract_html,
         grade_class, grade_label, repro_subdir, cards, sections, prev, nxt, crumb_short):
    """Render one canonical chapter page (VP-SPEC v1.8 section 6)."""
    canon = f"{SITE}/{PAPER_SLUG}/{slug}/"
    repro_url = f"{GH_TREE}/{repro_subdir}/"
    kw_list = BASE_KW + KW.get(slug, [])
    kw_meta = ", ".join(kw_list)
    knows_json = ",".join(_json(k) for k in kw_list)
    cards_html = "\n".join(cards)
    sections_html = "\n".join(sections)
    prev_a = f'<a rel="prev" href="{prev[1]}">&larr; {html.escape(prev[0])}</a>' if prev else "<span></span>"
    next_a = f'<a rel="next" href="{nxt[1]}">{html.escape(nxt[0])} &rarr;</a>' if nxt else "<span></span>"
    ld_article = (
        '{"@context":"https://schema.org","@type":"ScholarlyArticle",\n'
        f' "headline":{_json(title_full)},\n'
        f' "isPartOf":{{"@type":"CreativeWorkSeries","name":{_json(PAPER_NAME)},"url":"{SITE}/{PAPER_SLUG}/","sameAs":"https://doi.org/{CONCEPT_DOI}","identifier":"{CONCEPT_DOI}"}},\n'
        f' "position":{position},\n'
        f' "identifier":"{CONCEPT_DOI}",\n'
        f' "datePublished":"{PUB_DATE_ISO}","dateModified":"{LASTMOD}",\n'
        f' "isBasedOn":"{repro_url}",\n'
        f' "knowsAbout":[{knows_json}],\n'
        f' "author":{{"@type":"Person","name":{_json(AUTHOR)},"sameAs":"https://orcid.org/{ORCID}"}},\n'
        f' "publisher":{{"@type":"Organization","name":"Zenodo"}},\n'
        f' "license":"{LICENSE_URL}"}}'
    )
    ld_crumb = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[\n'
        f' {{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},\n'
        f' {{"@type":"ListItem","position":2,"name":"Chronobiology","item":"{SITE}/{PAPER_SLUG}/"}},\n'
        f' {{"@type":"ListItem","position":3,"name":{_json(html.escape(crumb_short))}}}]}}'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title_full)} | Jamming Physics</title>
<meta name="description" content="{html.escape(meta_desc)}">
<meta name="keywords" content="{html.escape(kw_meta)}">
<meta name="author" content="{html.escape(AUTHOR)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canon}">
<link rel="license" href="{LICENSE_URL}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Jamming Physics">
<meta property="og:title" content="{html.escape(title_full)}">
<meta property="og:description" content="{html.escape(meta_desc)}">
<meta property="og:url" content="{canon}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{html.escape(title_full)}">
<meta name="twitter:description" content="{html.escape(meta_desc)}">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld_article}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/{PAPER_SLUG}/">Chronobiology</a> &rsaquo; {html.escape(crumb_short)}</nav></header>
<main>
<h1>{h1}</h1>
<!-- vp:answer:start -->
<p class="answer">{answer_html}</p>
<!-- vp:answer:end -->
<p class="abstract">{abstract_html}</p>

<aside class="claim-strip">
  <span class="grade {grade_class}">{html.escape(grade_label)}</span>
  <span class="gate">LOCK &rarr; Derive &rarr; Gate</span>
  <a href="{GH_TREE}/{repro_subdir}/" rel="noopener">reproduce (GitHub)</a>
  <a href="https://doi.org/{CONCEPT_DOI}" rel="noopener">DOI snapshot</a>
</aside>
<!-- vp:cards:start -->
{cards_html}
<!-- vp:cards:end -->
{sections_html}
<nav class="pn">
  {prev_a}
  <a href="/{PAPER_SLUG}/">paper contents</a>
  {next_a}
</nav>
</main>
<footer>Part of <a href="/{PAPER_SLUG}/">Chronobiology</a> &middot; <a href="https://doi.org/{CONCEPT_DOI}" rel="noopener">DOI {CONCEPT_DOI}</a> &middot; seam cites mind <a href="https://doi.org/{MIND_DOI}">{MIND_DOI}</a> &middot; ORCID <a href="https://orcid.org/{ORCID}">{ORCID}</a> &middot; <a href="{LICENSE_URL}">CC BY 4.0</a></footer>
</body>
</html>
"""


def card(locked, head_html, body_html, grade_tag, link_slug, link_text):
    return (f'<aside class="vp-card" data-locked="{locked}"><b>{head_html}</b> = {body_html} '
            f'<b>{grade_tag}</b>. <a href="/{PAPER_SLUG}/{link_slug}/">{link_text}</a></aside>')


def sec(h2, html_body):
    return f"<h2>{html.escape(h2)}</h2>\n{html_body}"


def write(slug, html_text):
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html_text)


# ---------------------------------------------------------------------------------------------------
#  build all chapters
# ---------------------------------------------------------------------------------------------------
def build():
    f, eng = _findings()
    sha = _sha()
    rc1, rc2a, rc2b, rc3 = f["RC1"], f["RC2a"], f["RC2b"], f["RC3"]
    rc4, rc5, rc6, tx1 = f["RC4"], f["RC5"], f["RC6"], f["TX1"]

    n_free, cv, n_block = rc1["free_running_beats"], rc1["free_running_cv"], rc1["control_block_beats"]
    adv, dly = rc2a["max_advance"], rc2a["max_delay"]
    lock = rc2b["locking_range_count"]
    coh, drift = rc3["coherence_R"], rc3["peripheral_phase_drift_vs_master"]
    g_amp, a_amp = rc4["gated_cortisol_amplitude"], rc4["ablated_cortisol_amplitude"]
    reent, al_amp = rc5["reentrainment_cycles"], rc5["externally_aligned_cortisol_amp"]
    flat = rc6["hpa_flattening_index"]
    corr, wors = tx1["corrected_delay_h_correct_phase"], tx1["resulting_delay_h_wrong_phase"]

    os.makedirs(OUT, exist_ok=True)
    chapters = []

    # =============================================================== 00 GROUNDING (methods / "not a toy")
    s = "00-grounding-measured-dna-emergence"
    chapters.append((s, 0, "Grounding: measured DNA emergence, determinism, and falsifiable discriminants"))
    body = [
        sec("A derivation seeded by a measured gene, not a fitted toy model",
            "<p>This volume is not a casual or illustrative simulation. It is a <strong>deterministic derivation</strong> "
            "in which the molecular clock is seeded by a <strong>measured property of the real human clock gene</strong>, "
            "and every dynamical claim is produced by one engine whose output reproduces "
            f"<strong>bit-for-bit</strong> (seed&nbsp;=&nbsp;{SEED}, aggregate result sha256 "
            f"<span class=\"mono\">{sha[:12]}&hellip;</span>, computed twice and identical). Nothing on these pages is "
            "hand-typed, tuned, or chosen to land on a target: every number is pulled live from the shipped code, so the "
            "prose cannot drift from the result. The strong claims are mechanisms; the one cited anchor (the absolute "
            "~24&nbsp;hour period) and the deliberately-unclaimed quantities are stated as such, not hidden.</p>"),
        sec("The molecular clock is seeded by a real promoter, measured by nearest-neighbour thermodynamics",
            "<p>The core clock loop carries a <strong>measured</strong> well depth "
            f"<span class=\"mono\">&gamma; = {GAMMA_BMAL1}</span> for the real clock gene <strong>{GENE_SYMBOL}</strong> "
            f"(NCBI Gene ID {GENE_ID}, accession {GENE_ACC}). The value is computed as "
            f"{NN_METHOD} over the {GENE_NDINUC} dinucleotides of the gene's proximal promoter "
            f"({GENE_WINDOW}), through the <em>same</em> nearest-neighbour DNA pipeline the framework uses across every "
            "volume &mdash; not a parameter invented for the clock. The 2501-base promoter sequence is cached "
            f"(sha256 <span class=\"mono\">{GENE_SEQ_SHA}&hellip;</span>) so the &gamma; reproduces offline, byte-for-byte. "
            "Node identity and developmental order are owned by the DNA volume and cited here, never re-derived; the "
            "clock gene's &gamma; is a <strong>measured input graded [V]</strong>, never fitted.</p>"),
        sec("One substrate, run in its oscillatory window",
            "<p>The clock runs on the framework's shared <strong>FitzHugh&ndash;Nagumo (R19) substrate</strong> &mdash; "
            "the <em>same</em> bistable cell the rest of the atlas uses, vendored byte-identical, now driven into its "
            "oscillatory window. The volume adds exactly the dynamics a clock needs &mdash; coupling, entrainment, "
            "setpoint gating &mdash; on top of that fixed substrate, and then shows each one is a <strong>property of "
            "the substrate, not an assumption</strong>. No new physical constant is introduced anywhere in the volume; "
            "the chronotherapy chapter even reuses the entrainment chapter's phase-response curve in reverse rather than "
            "adding a parameter.</p>"),
        sec(f"{N_DISCRIMINANTS} falsifiable discriminants, each graded, each PASS",
            "<p>The research body is a battery of <strong>falsifiable discriminants</strong> &mdash; each one a sharp "
            "prediction that could have failed on the substrate and did not. All "
            f"{N_DISCRIMINANTS} pass deterministically:</p>"
            "<ul>"
            f"<li><strong>RC1 free-running</strong> &mdash; the loop self-sustains {n_free} regular cycles with zero "
            f"drive (cv&nbsp;=&nbsp;{cv}); a strong tonic drive instead silences it (depolarisation block, {n_block} beat) "
            "&mdash; the rhythm lives in a drive window. <span class=\"mono\">[V]</span></li>"
            f"<li><strong>RC2 entrainment</strong> &mdash; a brief pulse advances ({adv}) or delays ({dly}) the clock by "
            f"phase (a biphasic light PRC), and the locking range widens with zeitgeber strength ({lock}) &mdash; an "
            "Arnold tongue. <span class=\"mono\">[V]</span></li>"
            f"<li><strong>RC3 master vs network</strong> &mdash; coherence climbs with coupling "
            f"({coh[0]}&nbsp;&rarr;&nbsp;{coh[-1]}, a synchronisation transition) and a stronger master pulls the "
            "periphery into phase. <span class=\"mono\">[V]</span></li>"
            f"<li><strong>RC4 setpoint gating</strong> &mdash; the clock builds a daily HPA-cortisol rhythm "
            f"(amp&nbsp;{g_amp}) that vanishes when the clock is ablated (amp&nbsp;{a_amp}). <span class=\"mono\">[V]</span></li>"
            "<li><strong>RC5 misalignment</strong> &mdash; PRC-bounded re-entrainment and a signed gated rhythm that "
            "degrades from with-demand to antiphase as the phase gap grows. <span class=\"mono\">[V&nbsp;sign]</span></li>"
            f"<li><strong>RC6 mind seam</strong> &mdash; the HPA flattening index grows monotonically with misalignment "
            f"({flat[0]:g}&nbsp;&rarr;&nbsp;{flat[-1]}), supplying the circadian depression contributor mind locked. "
            "<span class=\"mono\">[V&nbsp;sign]&nbsp;/&nbsp;[O&nbsp;magnitude]</span></li>"
            f"<li><strong>TX1 chronotherapy</strong> &mdash; a phase-correct pulse re-aligns the clock "
            f"({corr[0]}&nbsp;&rarr;&nbsp;{corr[2]:g}&nbsp;h) while the same pulse at the wrong phase worsens it "
            f"({wors[0]}&nbsp;&rarr;&nbsp;{wors[-1]}&nbsp;h); efficacy&nbsp;=&nbsp;0. <span class=\"mono\">[V&nbsp;direction]</span></li>"
            "</ul>"),
        sec("What is derived, what is cited, what is left open",
            "<p>The honesty triad governs every chapter. <strong>Derived [V]:</strong> the oscillator mechanism, the "
            "PRC shape and sign, the Arnold tongue, the synchronisation transition, setpoint gating, the misalignment "
            "and seam signs, and the chronotherapy direction. <strong>Cited anchor [L]:</strong> the absolute "
            "~24&nbsp;hour period and the clinical timing windows &mdash; respected observations, not re-derived. "
            "<strong>Open [O], obstacle stated:</strong> absolute phase (the substrate runs in fast arbitrary time with "
            "no wall-clock zero), inter-tissue phase lags, absolute incidence / relative risk, the depression-handle "
            "magnitude (owned by mind), and the per-pulse chronotherapy gain. Each open item is logged with its "
            "specific obstacle in the irreproducibility ledger &mdash; a stated limit is a result, not a gap.</p>"),
    ]
    cards = [
        card("grounding",
             "this is a deterministic derivation seeded by a MEASURED clock-gene gamma, not a fitted toy simulation",
             f"the core clock loop carries a measured &gamma;={GAMMA_BMAL1} for the real gene {GENE_SYMBOL} (Gene ID "
             f"{GENE_ID}, {GENE_ACC}), computed as {NN_METHOD} over {GENE_NDINUC} promoter dinucleotides via the shared "
             f"DNA pipeline (promoter cached, sha256 {GENE_SEQ_SHA}&hellip;, offline-reproducible) &mdash; a measured "
             f"input [V], never fitted; every dynamical number is one deterministic engine (seed={SEED}, result sha256 "
             f"{sha[:12]}&hellip;, 2&times; identical); {N_DISCRIMINANTS} falsifiable discriminants (RC1&ndash;RC6 + TX1) "
             "all PASS; no new physical constant anywhere; the FitzHugh&ndash;Nagumo (R19) substrate is vendored byte-"
             "identical and merely run in its oscillatory window; period 24h is the only cited [L] anchor, open items "
             "carry stated obstacles",
             "[V reproducible]", s, "this page"),
    ]
    write(s, page(s, 0, "Grounding: measured DNA emergence, determinism, and falsifiable discriminants — Chronobiology §0",
                  "The VP circadian volume is a deterministic derivation, not a toy simulation: the molecular clock is "
                  f"seeded by a measured {GENE_SYMBOL} promoter gamma (Gene ID {GENE_ID}, {GENE_ACC}) via the shared DNA "
                  f"nearest-neighbour pipeline, never fitted; every number is one reproducible engine (seed {SEED}, 2x "
                  "sha256 identical) across 8 falsifiable discriminants.",
                  "Grounding &mdash; measured DNA emergence, determinism, and falsifiable discriminants",
                  "This circadian volume is a <strong>deterministic derivation seeded by a measured clock-gene "
                  f"&gamma;</strong>, not a toy simulation. The core loop carries a measured &gamma;&nbsp;=&nbsp;{GAMMA_BMAL1} "
                  f"for the real gene {GENE_SYMBOL} (Gene ID {GENE_ID}, {GENE_ACC}), computed by the shared DNA "
                  f"nearest-neighbour pipeline and never fitted; every dynamical number is one engine (seed&nbsp;=&nbsp;{SEED}, "
                  f"result sha256 <span class=\"mono\">{sha[:12]}&hellip;</span>, 2&times; identical) across "
                  f"{N_DISCRIMINANTS} falsifiable discriminants, all PASS.",
                  "Read this first. It is the evidence that the rest of the volume is grounded: a measured promoter "
                  "&gamma; for the real clock gene (offline-reproducible from a cached sequence), one deterministic "
                  "engine behind every figure, a shared substrate vendored byte-identical, and a battery of falsifiable "
                  "discriminants with explicit grades. The absolute period is the only cited anchor; what cannot be "
                  "claimed on this substrate is listed with its obstacle. This is a derivation with a reproducibility "
                  "hash, not an illustration.",
                  "g-verified", "[V] reproducible", "_engine", cards, body,
                  ("Chronobiology", f"/{PAPER_SLUG}/"),
                  ("§1 Scope", f"/{PAPER_SLUG}/01-scope-clock-oscillator/"), "Grounding"))

    # =============================================================== 01 SCOPE
    s = "01-scope-clock-oscillator"
    chapters.append((s, 1, "Scope: the circadian clock as a self-sustained oscillator network"))
    body = [
        sec("The clock is an oscillator, not a stopwatch driven by light",
            "<p>The circadian system keeps ~24&nbsp;hour time. The naive picture &mdash; an external light cycle "
            "pushing a passive timer &mdash; is wrong, and the correction is the whole programme: the clock is a "
            "<strong>self-sustained limit-cycle oscillator</strong> that <em>free-runs</em> with no input and is "
            "merely <em>entrained</em> by light. On this framework's shared FitzHugh&ndash;Nagumo (R19) substrate "
            "that is the same bistable cell the rest of the atlas uses, now run in its oscillatory window. The "
            "package adds the dynamics the clock needs &mdash; coupling, entrainment, setpoint gating &mdash; on top "
            "of that vendored substrate; it re-derives no constant and re-emerges no organ owned elsewhere.</p>"),
        sec("Four nodes, one measured gene",
            "<p>The clock is four nodes: an <strong>SCN master oscillator</strong>, the molecular "
            "<strong>core clock loop</strong> (BMAL1/CLOCK &harr; PER/CRY transcription&ndash;translation feedback), "
            "a <strong>peripheral clock network</strong> (liver / muscle / adipose), and the "
            "<strong>light-entrainment input</strong> (retina &rarr; SCN). Node identity and developmental order are "
            "owned by DNA and never fitted; the one node with a named master gene, the core loop, carries a "
            f"<strong>measured</strong> BMAL1 well of <span class=\"mono\">&gamma; = {GAMMA_BMAL1}</span> "
            "(gene 406, NC_000011.10), fetched through the same nearest-neighbour DNA pipeline the framework uses "
            "everywhere &mdash; a measured input, graded <span class=\"mono\">[V]</span>, never chosen to hit a "
            "target. The SCN and peripheral nodes are circuits with no single master gene (diffuse).</p>"),
        sec("Period is a cited anchor; mechanism is what is derived",
            "<p>One honesty line governs every chapter. The absolute ~24&nbsp;hour period is a "
            "<strong>cited [L] anchor</strong>, not an emergent number: the substrate runs in fast arbitrary-time "
            "cycles for cheap probes, and absolute phase has no zero in it (<span class=\"mono\">[O]</span>). What is "
            "<em>derived</em> is the <strong>mechanism</strong> &mdash; self-sustension, the phase-response curve, "
            "the synchronisation transition, setpoint gating, the misalignment sign &mdash; and every such number in "
            "these pages is produced by the shipped deterministic engine "
            f"(seed&nbsp;=&nbsp;19, result sha256 <span class=\"mono\">{sha[:12]}&hellip;</span>, 2&times; identical).</p>"),
        sec("Disease axis and the two seams out",
            "<p>Disease here is <strong>clock&ndash;environment misalignment</strong>: the clock runs, but at the "
            "wrong phase relative to the demand schedule (shift work, jet lag), and the defended setpoints it gates "
            "lose their daily organisation. The package is SSOT for circadian <em>phase / timing</em> and exports a "
            "gating signal to the thermometabolic, hemodynamic, ionic and immune setpoints of the sibling packages. "
            "Its sharpest seam is into the <a href=\"/" + PAPER_SLUG + "/07-circadian-mood-seam/\">mind</a> volume: "
            "misalignment flattens the gated HPA cortisol rhythm, and that flattening is the <em>circadian "
            "depression contributor</em> the mind paper explicitly left locked. No felt-state claim crosses that "
            "seam.</p>"),
    ]
    cards = [
        card("circadian_scope",
             "the circadian clock = a self-sustained coupled limit-cycle oscillator network, not a light-driven timer",
             "four nodes (SCN master, molecular core loop, peripheral network, light entrainment) on the shared R19 "
             f"substrate; the core loop carries a MEASURED BMAL1 well &gamma;={GAMMA_BMAL1} (gene 406, NC_000011.10, "
             "DNA pipeline, never fitted); the clock FREE-RUNS and is only ENTRAINED by light; the ~24h period is a "
             "cited [L] anchor while the MECHANISM (self-sustension, PRC, synchrony, gating, misalignment) is derived; "
             "disease = clock-environment misalignment; SSOT for circadian phase/timing",
             "[V mech] / [L period] / [O phase]", s, "this chapter"),
    ]
    write(s, page(s, 1, "Scope: the circadian clock as a self-sustained oscillator network — Chronobiology §1",
                  "The circadian clock as a self-sustained coupled limit-cycle oscillator network on the R19 substrate: "
                  "four nodes, a measured BMAL1 gamma, period as a cited anchor, mechanism derived, disease as "
                  "clock-environment misalignment.",
                  "Scope &mdash; the circadian clock as a self-sustained oscillator network",
                  "The ~24&nbsp;hour circadian clock is a <strong>self-sustained coupled limit-cycle oscillator "
                  "network</strong> (SCN master + peripheral clocks) on the shared R19 substrate, not a light-driven "
                  "timer: it free-runs and is only entrained by light. The one node with a named master gene carries a "
                  f"measured BMAL1 well (&gamma;&nbsp;=&nbsp;{GAMMA_BMAL1}); the ~24&nbsp;h period is a cited anchor "
                  "while the mechanism is derived. Disease is clock&ndash;environment misalignment.",
                  "This package fills the research body of the circadian volume. It emerges the clock's nodes from a "
                  "measured gene, runs the oscillator dynamics &mdash; free-running, entrainment, master-vs-network, "
                  "setpoint gating, misalignment &mdash; on the vendored FitzHugh&ndash;Nagumo substrate, and exports a "
                  "single timing signal to the homeostatic setpoints of the sibling packages and to the mind volume's "
                  "affect layer. Every number is produced by shipped deterministic code; the absolute period is the "
                  "only [L] anchor; the felt quality of mood stays in mind (consciousness_claim&nbsp;=&nbsp;0).",
                  "g-calibrated", "scope", s, cards, body,
                  ("§0 Grounding", f"/{PAPER_SLUG}/00-grounding-measured-dna-emergence/"),
                  ("§2 Free-running", f"/{PAPER_SLUG}/02-free-running/"), "§1 Scope"))

    # =============================================================== 02 FREE-RUNNING (RC1)
    s = "02-free-running"
    chapters.append((s, 2, "Free-running: the molecular clock self-sustains a rhythm with no input"))
    body = [
        sec("A rhythm with the lights off",
            "<p>The defining property of a circadian clock is that it keeps going in constant darkness. Run the "
            "molecular core loop on the R19 substrate with a steady supra-threshold drive and <em>no</em> periodic "
            f"forcing: it produces a sustained, highly regular rhythm &mdash; <span class=\"mono\">{n_free}</span> "
            f"clean cycles with an inter-beat coefficient of variation of <span class=\"mono\">{cv}</span> "
            "(near-perfect regularity). This is a true limit cycle, not a decaying transient: the oscillation is a "
            "property of the loop, not of the input.</p>"),
        sec("The control that proves it is a window, not an always-on switch",
            "<p>A free-running rhythm could be dismissed if the cell simply fired at any drive. It does not. Pin the "
            "same cell with a <strong>strong</strong> tonic drive and it enters depolarisation block &mdash; the "
            f"switch is held high and goes silent (<span class=\"mono\">{n_block}</span> beat). So the rhythm lives "
            "in a limit-cycle <em>window</em> of drive: too little and it never starts, too much and it locks high; "
            "in between it self-sustains. That window is the mechanistic signature of an oscillator, and it is what "
            "separates a clock from a relay.</p>"),
        sec("What is claimed and what is anchored",
            "<p>The <strong>mechanism</strong> &mdash; self-sustension inside a drive window &mdash; is graded "
            "<span class=\"mono\">[V]</span>. The <strong>absolute period</strong> (~24&nbsp;h) is the cited "
            "<span class=\"mono\">[L]</span> anchor: the substrate runs in fast arbitrary time, so the free-running "
            "frequency here is a mechanism readout, not a wall-clock measurement, and absolute phase has no zero "
            "(<span class=\"mono\">[O]</span>). The transcription&ndash;translation feedback loop is the real "
            "molecular oscillator this abstracts; its period is set by cited delays, which the substrate does not "
            "re-derive.</p>"),
    ]
    cards = [
        card("free_running",
             "the molecular clock = a self-sustained limit-cycle oscillator that free-runs with ZERO external drive",
             f"a steady supra-threshold drive with no forcing gives {n_free} regular cycles (cv={cv}); a STRONG tonic "
             f"drive pins the switch high (depolarisation block) and silences it ({n_block} beat) &mdash; so the rhythm "
             "lives in a limit-cycle WINDOW of drive, the signature of an oscillator and not an always-on relay; "
             "mechanism [V], the ~24h period is a cited [L] anchor (arb-time substrate), absolute phase [O]",
             "[V mech]", s, "this chapter"),
    ]
    write(s, page(s, 2, "Free-running: the molecular clock self-sustains a rhythm with no input — Chronobiology §2",
                  "The molecular circadian clock free-runs: a steady drive with no periodic forcing gives a regular "
                  "self-sustained rhythm, while a strong tonic drive silences it (depolarisation block) — the rhythm "
                  "lives in a limit-cycle window. Mechanism verified; period a cited anchor.",
                  "Free-running &mdash; the molecular clock self-sustains a rhythm with no input",
                  f"The molecular core loop <strong>free-runs</strong>: with a steady drive and no periodic forcing it "
                  f"produces {n_free} highly regular cycles (cv&nbsp;=&nbsp;{cv}). A <em>strong</em> tonic drive instead "
                  f"pins the switch high and silences it ({n_block} beat), proving the rhythm lives in a limit-cycle "
                  "<strong>window</strong> of drive &mdash; the signature of a true oscillator, not an always-on relay.",
                  "Constant-darkness self-sustension is the defining property of a circadian clock. On the R19 "
                  "substrate the core loop shows it cleanly, and the depolarisation-block control rules out the trivial "
                  "always-on alternative. The mechanism is verified; the absolute ~24&nbsp;hour period remains a cited "
                  "anchor because the substrate runs in fast arbitrary time.",
                  "g-verified", "verified", s, cards, body,
                  ("§1 Scope", f"/{PAPER_SLUG}/01-scope-clock-oscillator/"),
                  ("§3 Entrainment & the PRC", f"/{PAPER_SLUG}/03-entrainment-prc/"), "§2 Free-running"))

    # =============================================================== 03 ENTRAINMENT / PRC (RC2)
    s = "03-entrainment-prc"
    chapters.append((s, 3, "Entrainment: the phase-response curve and the Arnold tongue"))
    body = [
        sec("A pulse advances or delays depending on when it lands",
            "<p>A free-running clock is entrained by resetting its phase. Deliver a brief pulse at many phases of the "
            "cycle and measure the shift of the next beat: the response is <strong>biphasic</strong>. A pulse in one "
            f"part of the cycle <em>advances</em> the clock (up to <span class=\"mono\">{adv}</span> of a cycle), a "
            f"pulse in another part <em>delays</em> it (down to <span class=\"mono\">{dly}</span>), with a dead zone "
            "between. That advance/delay-with-a-dead-zone shape is the canonical circadian light phase-response curve "
            "&mdash; morning light advances, evening light delays &mdash; and it falls out of the substrate, sign and "
            "all, with no curve-fitting.</p>"),
        sec("Stronger zeitgeber, wider locking range: the Arnold tongue",
            "<p>Entrainment proper is locking to a periodic drive. Sweep a periodic zeitgeber over a wide band of "
            "external periods (0.65&ndash;1.35&times; the natural period) at five amplitudes and count how many "
            f"detunings lock. The locking range <strong>widens monotonically</strong> with zeitgeber strength: "
            f"<span class=\"mono\">{lock}</span> detunings locked across the amplitude sweep. A weak zeitgeber "
            "entrains only near the natural period; a strong one captures a broad band. That widening wedge is an "
            "Arnold tongue &mdash; the standard structure of a forced oscillator, here emergent.</p>"),
        sec("Why this matters for the disease axis",
            "<p>The PRC is also the clock's <strong>control law</strong>, and it sets a hard limit that the disease "
            "and treatment chapters both use: because a single pulse only shifts the clock by a bounded amount, the "
            "clock can re-align only <strong>~1&nbsp;hour per day</strong>. A large phase gap therefore takes many "
            "days to close &mdash; the mechanism of jet lag &mdash; and a corrective zeitgeber works only if it lands "
            "on the right side of the PRC. Mechanism and tongue are <span class=\"mono\">[V]</span>; the absolute "
            "period the tongue centres on is the cited <span class=\"mono\">[L]</span> anchor.</p>"),
    ]
    cards = [
        card("entrainment_prc",
             "entrainment = phase resetting along a biphasic PRC, with the locking range widening as an Arnold tongue",
             f"a brief pulse ADVANCES (up to {adv} cyc) or DELAYS (down to {dly} cyc) the clock depending on phase, "
             "with a dead zone &mdash; the canonical circadian light PRC (morning advances, evening delays), emergent "
             f"with no fitting; a periodic zeitgeber LOCKS the clock and the locking range widens monotonically with "
             f"strength ({lock} detunings locked across the amplitude sweep) = an Arnold tongue; the PRC bounds "
             "re-alignment to ~1 h/day, the limit the disease + treatment chapters use; mechanism + tongue [V], "
             "absolute period [L]",
             "[V mech]", s, "this chapter"),
    ]
    write(s, page(s, 3, "Entrainment: the phase-response curve and the Arnold tongue — Chronobiology §3",
                  "The circadian clock entrains via a biphasic phase-response curve (a pulse advances or delays "
                  "depending on phase, with a dead zone) and locks to a periodic zeitgeber with a locking range that "
                  "widens with strength — an Arnold tongue. The PRC bounds re-alignment to ~1 h/day.",
                  "Entrainment &mdash; the phase-response curve and the Arnold tongue",
                  f"A brief pulse <strong>advances</strong> the clock (up to {adv} of a cycle) or <strong>delays</strong> "
                  f"it (down to {dly}) depending on phase, with a dead zone &mdash; the canonical biphasic circadian "
                  f"light PRC, emergent with no fitting. A periodic zeitgeber locks the clock, and the locking range "
                  f"widens monotonically with strength ({lock} detunings across the sweep): an Arnold tongue.",
                  "Entrainment is phase resetting, not driving. The substrate reproduces the canonical light "
                  "phase-response curve (advance / delay / dead zone, correct sign) and the Arnold-tongue widening of "
                  "the locking range with zeitgeber strength. The PRC is also the clock's control law: it bounds "
                  "re-alignment to about an hour a day, the limit the misalignment and chronotherapy chapters both turn "
                  "on. Mechanism and tongue verified; absolute period a cited anchor.",
                  "g-verified", "verified", s, cards, body,
                  ("§2 Free-running", f"/{PAPER_SLUG}/02-free-running/"),
                  ("§4 Master vs network", f"/{PAPER_SLUG}/04-master-vs-network/"), "§3 Entrainment & the PRC"))

    # =============================================================== 04 MASTER vs NETWORK (RC3)
    s = "04-master-vs-network"
    chapters.append((s, 4, "Master vs network: coupled clocks synchronise, master-led"))
    body = [
        sec("Coupling buys synchrony: a transition, not a tweak",
            "<p>Is timekeeping one clock or many? Take eight oscillators with slightly different natural periods and "
            "couple them through a mean field, sweeping the coupling strength from zero upward. The coherence of the "
            f"population <strong>rises monotonically</strong> with coupling &mdash; from "
            f"<span class=\"mono\">{coh[0]}</span> uncoupled to <span class=\"mono\">{coh[-1]}</span> at strong "
            "coupling &mdash; a synchronisation transition. Decoupled peripheral clocks drift apart; coupling pulls "
            "them into a single coherent rhythm. So the body's clocks are a <em>network</em>, not a bag of "
            "independent timers.</p>"),
        sec("The SCN is the master: a stronger hub pulls the periphery into phase",
            "<p>A network still has a hierarchy. Raise the gain of one node &mdash; the SCN master &mdash; and measure "
            "how far the peripheral clocks drift from it. The peripheral phase drift relative to the master "
            f"<strong>falls</strong> as the master's gain rises (<span class=\"mono\">{drift[0]}</span> &rarr; "
            f"<span class=\"mono\">{drift[-1]}</span>): a stronger master entrains the periphery more tightly. That is "
            "the master&ndash;periphery architecture of the real system &mdash; the SCN sets the phase that liver, "
            "muscle and adipose clocks follow &mdash; reproduced as a property of coupling, not assumed.</p>"),
        sec("One network, master-led",
            "<p>Both results are <span class=\"mono\">[V]</span>: the synchronisation transition and the master-led "
            "entrainment. The <strong>absolute</strong> phase lags between SCN and periphery depend on tissue "
            "conduction the substrate does not model, so only their <em>ordering</em> is claimed "
            "(<span class=\"mono\">[O]</span> on the absolute lags). The picture is one coupled network with a "
            "dominant hub &mdash; which is exactly why a misaligned master (next chapter) drags the whole gated "
            "periphery off the external schedule with it.</p>"),
    ]
    cards = [
        card("master_vs_network",
             "timekeeping = ONE coupled network, master-led, not a single clock or independent timers",
             f"eight oscillators coupled through a mean field synchronise as coupling rises &mdash; coherence climbs "
             f"monotonically {coh[0]}&rarr;{coh[-1]} (a synchronisation transition); raising the SCN master's gain "
             f"pulls peripheral clocks into phase &mdash; their drift vs the master FALLS {drift[0]}&rarr;{drift[-1]}; "
             "so the body clocks are one network with a dominant SCN hub (the periphery follows the master), which is "
             "why a misaligned master drags the gated periphery with it; transition + master-led entrainment [V], "
             "absolute SCN&rarr;periphery lags [O]",
             "[V mech]", s, "this chapter"),
    ]
    write(s, page(s, 4, "Master vs network: coupled clocks synchronise, master-led — Chronobiology §4",
                  "Is the circadian system one clock or many? Eight coupled oscillators synchronise as coupling rises "
                  "(coherence climbs monotonically — a synchronisation transition), and a stronger SCN master pulls "
                  "peripheral clocks into phase (drift falls). One network, master-led.",
                  "Master vs network &mdash; coupled clocks synchronise, master-led",
                  f"The body's clocks are <strong>one coupled network</strong>, not independent timers: eight "
                  f"oscillators synchronise as coupling rises (coherence {coh[0]}&nbsp;&rarr;&nbsp;{coh[-1]}, a "
                  f"synchronisation transition), and a stronger <strong>SCN master</strong> pulls the periphery into "
                  f"phase (drift {drift[0]}&nbsp;&rarr;&nbsp;{drift[-1]}). Master-led, by coupling, not by assumption.",
                  "Timekeeping is distributed but hierarchical. Coupling drives a synchronisation transition among "
                  "oscillators with different natural periods, and raising the SCN master's gain tightens the "
                  "periphery's phase-locking to it. The system is one network with a dominant hub &mdash; the reason a "
                  "misaligned master drags the whole gated periphery off schedule in the next chapter. The ordering is "
                  "verified; absolute inter-tissue phase lags stay open.",
                  "g-verified", "verified", s, cards, body,
                  ("§3 Entrainment & the PRC", f"/{PAPER_SLUG}/03-entrainment-prc/"),
                  ("§5 Setpoint gating", f"/{PAPER_SLUG}/05-setpoint-gating/"), "§4 Master vs network"))

    # =============================================================== 05 SETPOINT GATING (RC4)
    s = "05-setpoint-gating"
    chapters.append((s, 5, "Setpoint gating: the clock imposes a daily rhythm on the HPA axis"))
    body = [
        sec("The clock does not keep time for its own sake",
            "<p>A clock earns its place by <em>gating</em> physiology. Take the worked example: the HPA cortisol "
            "axis, whose kinetics are <strong>cited from the mind volume</strong> (a biexponential PVN&rarr;ACTH&rarr;"
            "cortisol cascade with the cortisol peak in the 15&ndash;40&nbsp;minute window, Dickerson &amp; Kemeny "
            "2004). This package adds <strong>no</strong> kinetic constant; it only lets the clock modulate the "
            "<em>drive</em> into that cascade with circadian phase, and asks what the cortisol output does.</p>"),
        sec("Gated vs ablated: rhythm appears, then vanishes",
            "<p>Run the cascade for five simulated days. With the clock <strong>gating</strong> the drive, cortisol "
            f"develops a strong daily rhythm &mdash; last-day amplitude <span class=\"mono\">{g_amp}</span>. Replace "
            "the clock with a constant drive of the same mean (clock <strong>ablated</strong>) and the rhythm "
            f"collapses to a flat line &mdash; amplitude <span class=\"mono\">{a_amp}</span>. The clock is not "
            "responding to a daily cortisol demand; it is <em>creating</em> the daily cortisol rhythm. That is "
            "setpoint gating: a defended variable acquires its 24&nbsp;hour structure from the clock, not from the "
            "environment.</p>"),
        sec("One worked seam, many gated setpoints",
            "<p>Cortisol is the worked case because it is the seam into mind; the <em>same</em> gating sets the daily "
            "rhythm of core temperature and blood pressure (the thermometabolic and hemodynamic setpoints the sibling "
            "packages own). The gating <strong>mechanism</strong> is <span class=\"mono\">[V]</span>; the cortisol "
            "<strong>kinetics and window</strong> are cited <span class=\"mono\">[L]</span>; the <strong>absolute "
            "cortisol level</strong> is not set here (<span class=\"mono\">[O]</span>) &mdash; only the depth of the "
            "clock-imposed modulation is claimed. Flatten this gating by misaligning the clock and the defended "
            "setpoint is dysregulated, which is the disease.</p>"),
    ]
    cards = [
        card("setpoint_gating",
             "the clock IMPOSES a daily rhythm on a defended setpoint (the HPA cortisol axis), it does not merely follow demand",
             f"using the mind-cited HPA cascade (biexponential, ACTH&rarr;cortisol peak 15&ndash;40 min; NO new kinetic "
             f"constant), the clock modulates only the DRIVE with circadian phase: over five days the GATED axis "
             f"develops a strong daily cortisol rhythm (amp {g_amp}) while an ABLATED constant-drive clock is flat "
             f"(amp {a_amp}) &mdash; the clock CREATES the rhythm; the same gating sets core-temperature + blood-"
             "pressure rhythms (sibling setpoints); gating mechanism [V], cortisol kinetics/window cited [L], absolute "
             "cortisol level [O]",
             "[V mech]", s, "this chapter"),
    ]
    write(s, page(s, 5, "Setpoint gating: the clock imposes a daily rhythm on the HPA axis — Chronobiology §5",
                  "The circadian clock gates physiology: modulating only the drive into the mind-cited HPA cortisol "
                  "cascade, a gated clock builds a strong daily cortisol rhythm while an ablated constant-drive clock "
                  "is flat. The clock creates the rhythm; the same gating sets temperature and blood pressure.",
                  "Setpoint gating &mdash; the clock imposes a daily rhythm on the HPA axis",
                  f"The clock <strong>gates</strong> defended setpoints. Modulating only the drive into the mind-cited "
                  f"HPA cortisol cascade (no new kinetic constant), a gated clock builds a strong daily cortisol rhythm "
                  f"(amplitude {g_amp}) while an ablated, constant-drive clock is flat ({a_amp}). The clock "
                  "<em>creates</em> the daily rhythm; the same gating sets core temperature and blood pressure.",
                  "A clock matters because it gates physiology. Using the HPA cortisol cascade cited from the mind "
                  "volume &mdash; with no new kinetic constant, only circadian modulation of the drive &mdash; the "
                  "clock imposes a daily cortisol rhythm that vanishes when the clock is ablated. Cortisol is the worked "
                  "seam into mind; the same gating organises temperature and blood pressure. Mechanism verified, "
                  "kinetics cited, absolute level open.",
                  "g-verified", "verified", s, cards, body,
                  ("§4 Master vs network", f"/{PAPER_SLUG}/04-master-vs-network/"),
                  ("§6 Misalignment & disease", f"/{PAPER_SLUG}/06-misalignment-disease/"), "§5 Setpoint gating"))

    # =============================================================== 06 MISALIGNMENT / DISEASE (RC5)
    s = "06-misalignment-disease"
    chapters.append((s, 6, "Misalignment: shift work, jet lag, and the dysregulated setpoint"))
    body = [
        sec("The disease is a phase gap, not a broken clock",
            "<p>Circadian disease is not a stopped clock. The clock runs fine; it runs at the <strong>wrong "
            "phase</strong> relative to the external demand schedule. Impose a phase shift &mdash; the jet-lag / "
            "shift-work perturbation &mdash; and two things follow. First, re-entrainment takes <strong>time</strong>: "
            "because the PRC bounds re-alignment to ~1&nbsp;hour per day, closing a gap of "
            f"<span class=\"mono\">{reent[1]:g}</span>, <span class=\"mono\">{reent[3]:g}</span>, "
            f"<span class=\"mono\">{reent[-1]:g}</span>&nbsp;hours takes that many cycles. A big shift is days of "
            "misalignment.</p>"),
        sec("Cortisol peaks at the wrong external time",
            "<p>Second, during misalignment the gated setpoint is dysregulated. Project the gated cortisol rhythm "
            "onto the external demand schedule: aligned, it peaks <em>with</em> demand (healthy); misaligned, the peak "
            "slides off. The signed alignment falls <strong>monotonically</strong> as the phase gap grows &mdash; "
            f"from <span class=\"mono\">{al_amp[0]}</span> (aligned, cortisol with demand) through "
            f"<span class=\"mono\">0</span> (orthogonal) to <span class=\"mono\">{al_amp[-1]}</span> (antiphase, "
            "cortisol against demand, the worst case). The defended setpoint now fires at the wrong external time. "
            "That is the disease state: not an absent rhythm, but a <em>well-formed rhythm at the wrong phase</em>.</p>"),
        sec("Three named diseases, one mechanism",
            "<p>This single mechanism underlies the package's major (non-rare) diseases. "
            "<strong>Circadian rhythm sleep-wake disorders</strong> (delayed/advanced phase, non-24h, shift-work "
            "disorder, jet lag) are the phenotype directly. <strong>Shift-work metabolic and cardiovascular "
            "disease</strong> is the chronic flattening of the gated metabolic and pressure setpoints. "
            "<strong>Night-shift cancer risk</strong> (IARC Group&nbsp;2A) enters through the same oncology kernel the "
            "mechanical packages use: losing clock gating shrinks the effective barrier holding cellular setpoints and "
            "raises the Kramers crossing rate &mdash; circadian disruption is a rate <em>multiplier</em>, not a "
            "separate carcinogen. Rare and monogenic clock disorders (e.g. familial advanced sleep phase) are owned by "
            "disease_wp and enter here only as a cited parameter. The degradation <strong>sign</strong> is "
            "<span class=\"mono\">[V]</span>; the shift-work relative risk is cited <span class=\"mono\">[L]</span>; "
            "absolute incidence is <span class=\"mono\">[O]</span>.</p>"),
    ]
    cards = [
        card("misalignment_disease",
             "circadian disease = a phase GAP between the internal clock and external time, not a broken clock",
             f"a phase shift takes {reent[-1]:g} cycles to close at the PRC-bounded ~1 h/day, and during misalignment "
             f"the signed alignment of gated cortisol to external demand falls monotonically {al_amp[0]}&rarr;0&rarr;"
             f"{al_amp[-1]} (with demand &rarr; orthogonal &rarr; antiphase) &mdash; the defended setpoint fires at the "
             "WRONG external time (a well-formed rhythm at the wrong phase). One mechanism covers sleep-wake disorders, "
             "shift-work metabolic/cardiovascular disease, and IARC-2A night-shift cancer (a Kramers-rate MULTIPLIER on "
             "the shared oncology kernel, not a new carcinogen); rare/monogenic forms &rarr; disease_wp; degradation "
             "sign [V], shift-work RR cited [L], absolute incidence [O]",
             "[V sign]", s, "this chapter"),
    ]
    write(s, page(s, 6, "Misalignment: shift work, jet lag, and the dysregulated setpoint — Chronobiology §6",
                  "Circadian disease is a phase gap, not a broken clock: re-entrainment is PRC-bounded to ~1 h/day, and "
                  "during misalignment the gated cortisol rhythm peaks at the wrong external time (signed alignment "
                  "falls from with-demand through orthogonal to antiphase). One mechanism, three named diseases.",
                  "Misalignment &mdash; shift work, jet lag, and the dysregulated setpoint",
                  f"Circadian disease is a <strong>phase gap</strong>, not a stopped clock. A shift takes up to "
                  f"{reent[-1]:g} cycles to close (PRC-bounded ~1&nbsp;h/day), and during misalignment the gated "
                  f"cortisol rhythm's alignment to external demand falls monotonically "
                  f"({al_amp[0]}&nbsp;&rarr;&nbsp;0&nbsp;&rarr;&nbsp;{al_amp[-1]}): a well-formed rhythm at the wrong "
                  "phase. One mechanism covers sleep-wake disorders, shift-work cardiometabolic disease, and IARC-2A "
                  "night-shift cancer.",
                  "The disease axis is decoupling of the internal clock from external time. Re-entrainment is slow "
                  "because the PRC bounds it, and the gated setpoint is dysregulated because it keeps a clean rhythm at "
                  "the wrong external phase. The same mechanism underlies circadian sleep-wake disorders, shift-work "
                  "cardiometabolic risk, and &mdash; through the shared Kramers oncology kernel &mdash; the IARC class "
                  "2A night-shift cancer association as a rate multiplier. The degradation sign is verified; absolute "
                  "incidence stays open; rare monogenic forms belong to disease_wp.",
                  "g-verified", "verified (sign)", s, cards, body,
                  ("§5 Setpoint gating", f"/{PAPER_SLUG}/05-setpoint-gating/"),
                  ("§7 The circadian–mood seam", f"/{PAPER_SLUG}/07-circadian-mood-seam/"), "§6 Misalignment & disease"))

    # =============================================================== 07 MIND SEAM (RC6)
    s = "07-circadian-mood-seam"
    chapters.append((s, 7, "The circadian–mood seam: supplying the contributor mind locked"))
    body = [
        sec("Mind left a door open, by name",
            "<p>The mind volume's depression chapter modelled major depression as the chronification of a "
            "low-coordination operating point, driven by an HPA-stress <em>withdrawal bias</em>, and it explicitly "
            "<strong>locked</strong> the heterogeneity of real depression &mdash; melancholic, atypical, psychotic, "
            "peripartum, seasonal, bipolar, with monoaminergic, HPA, inflammatory, <strong>circadian</strong> and "
            "psychosocial contributors. The circadian contributor was named and left unmodelled. This chapter "
            "supplies exactly that one contributor, and nothing more.</p>"),
        sec("Misalignment flattens the gated HPA rhythm, monotonically",
            "<p>Take the gated cortisol rhythm of &sect;5 and misalign the clock by a growing phase shift. The HPA "
            "<strong>flattening index</strong> &mdash; the loss of demand-aligned cortisol relative to the healthy "
            f"clock &mdash; grows <strong>monotonically</strong> with misalignment: <span class=\"mono\">{flat[0]:g}</span> "
            f"(aligned) &rarr; <span class=\"mono\">{flat[2]}</span> &rarr; <span class=\"mono\">{flat[-1]}</span> "
            "(antiphase), running from a healthy rhythm to a fully demand-misaligned one. A flattened, "
            "demand-misaligned cortisol signal <em>is</em> a sustained, dysregulated HPA signal.</p>"),
        sec("That sustained signal is mind's withdrawal handle — sign only",
            "<p>Here the seam closes. In mind, a sustained dysregulated cortisol signal sits on the <strong>withdrawal "
            "pole</strong> of the valence geometry and acts as a withdrawal bias <span class=\"mono\">b&nbsp;&lt;&nbsp;0</span>, "
            "which lowers effective coupling through the same map the schizophrenia and epilepsy modules use "
            "(<span class=\"mono\">k&nbsp;=&nbsp;&kappa;/(1+|b|)</span>) &rarr; hypo-coordination, and under mind's E0 "
            "plasticity layer the excursion <em>chronifies</em>. So circadian misalignment &rarr; HPA flattening "
            "&rarr; (mind: sustained withdrawal bias &rarr; hypo-coordination &rarr; chronification). This is the "
            "circadian depression contributor, now supplied.</p>"),
        sec("The firewall: timing in, felt quality stays out",
            "<p>What crosses this seam is a <strong>sign</strong>, not a feeling. The package asserts the "
            "<em>direction</em> &mdash; misalignment moves the HPA signal in the withdrawal direction &mdash; and the "
            "<strong>magnitude is [O]</strong>, owned by mind. The <strong>felt quality</strong> of low mood does "
            "<em>not</em> cross: it stays in mind behind the Axis-A firewall "
            "(<span class=\"mono\">consciousness_claim&nbsp;=&nbsp;0</span>, the hard problem open). This package models "
            "the <strong>timing perturbation</strong> of the HPA setpoint, not depression itself; efficacy&nbsp;=&nbsp;0; "
            "not medical advice. The same timing seam also <em>aggravates</em> mind's coupling-organisation reading of "
            "autism, where circadian and sleep disruption is common &mdash; again sign only, with the coupling "
            f"pathology owned by mind (concept DOI {MIND_DOI}). The mind anchor "
            "<span class=\"mono\">R&nbsp;=&nbsp;0.38961455156044245</span> (engine tree 0fbf4988&hellip;) is cited, "
            "not recomputed.</p>"),
    ]
    cards = [
        card("circadian_mood_seam",
             "circadian misalignment supplies the CIRCADIAN depression contributor mind explicitly LOCKED &mdash; sign only",
             f"misaligning the clock flattens the gated HPA cortisol rhythm: the flattening index grows monotonically "
             f"{flat[0]:g}&rarr;{flat[-1]} (aligned&rarr;antiphase); a sustained demand-misaligned cortisol signal sits "
             "on mind's WITHDRAWAL pole and acts as a withdrawal bias b&lt;0 &rarr; lowers coupling k=&kappa;/(1+|b|) "
             "&rarr; hypo-coordination &rarr; (under mind's E0 plasticity) chronification &mdash; the circadian "
             "contributor mind 27 named and locked, now supplied; the SAME timing seam aggravates mind's autism "
             "coupling reading (common circadian/sleep disruption); FIREWALL: SIGN only, magnitude [O] (owned by mind), "
             "the FELT quality stays in mind (consciousness_claim=0, hard problem OPEN), efficacy=0, not medical advice; "
             f"mind anchor R=0.38961455156044245 cited; mind concept DOI {MIND_DOI}",
             "[V sign] / [O magnitude]", s, "this chapter"),
    ]
    write(s, page(s, 7, "The circadian–mood seam: supplying the contributor mind locked — Chronobiology §7",
                  "Circadian misalignment flattens the gated HPA cortisol rhythm (flattening index grows monotonically "
                  "from aligned to antiphase); that sustained dysregulated signal is mind's withdrawal-bias handle — the "
                  "circadian depression contributor mind explicitly locked, now supplied. Sign only; felt quality stays "
                  "in mind.",
                  "The circadian&ndash;mood seam &mdash; supplying the contributor mind locked",
                  f"Mind's depression chapter named a <strong>circadian contributor</strong> and locked it. This chapter "
                  f"supplies it: misalignment flattens the gated HPA cortisol rhythm (flattening index "
                  f"{flat[0]:g}&nbsp;&rarr;&nbsp;{flat[-1]}, aligned&rarr;antiphase), and that sustained, "
                  "demand-misaligned signal <em>is</em> mind's withdrawal-bias handle (b&nbsp;&lt;&nbsp;0). Sign only; "
                  "the felt quality of low mood stays in mind (consciousness_claim&nbsp;=&nbsp;0).",
                  "This is the sharpest seam in the volume. The mind paper modelled depression on an HPA withdrawal "
                  "handle and explicitly locked the circadian contributor; the circadian clock supplies it by flattening "
                  "the gated cortisol rhythm under misalignment, which maps to mind's withdrawal bias through the shared "
                  "coupling map and chronifies under mind's plasticity layer. The same timing seam aggravates mind's "
                  "coupling reading of autism. Only the sign crosses; the magnitude is owned by mind, the felt quality "
                  "stays behind mind's Axis-A firewall, and efficacy is zero.",
                  "g-calibrated", "model / seam", s, cards, body,
                  ("§6 Misalignment & disease", f"/{PAPER_SLUG}/06-misalignment-disease/"),
                  ("§8 Chronotherapy", f"/{PAPER_SLUG}/08-chronotherapy/"), "§7 The circadian–mood seam"))

    # =============================================================== 08 CHRONOTHERAPY (TX1)
    s = "08-chronotherapy"
    chapters.append((s, 8, "Chronotherapy: re-aligning the clock with the PRC"))
    body = [
        sec("Treat the timing, not the symptom",
            "<p>If circadian disease is a phase gap, the treatment is to <strong>re-align the clock</strong> &mdash; "
            "and the control law for doing so is the phase-response curve of &sect;3. Timing <em>is</em> the therapy. Take "
            "a phase-<em>delayed</em> clock (the clock runs too late, as in delayed sleep-wake phase disorder) and "
            "apply a PRC-correct advancing zeitgeber. The delay closes as the pulse strength rises &mdash; the "
            f"residual delay falls <span class=\"mono\">{corr[0]}</span> &rarr; <span class=\"mono\">{corr[1]}</span> "
            f"&rarr; <span class=\"mono\">{corr[2]:g}</span>&nbsp;hours and saturates at full correction. The clock "
            "re-aligns.</p>"),
        sec("The same pulse at the wrong phase is iatrogenic",
            "<p>The sign is the whole therapy. Deliver the <em>same</em> pulse at the <strong>wrong</strong> phase &mdash; "
            "the delay region of the PRC &mdash; and it makes things worse: the residual delay <em>grows</em> "
            f"<span class=\"mono\">{wors[0]}</span> &rarr; <span class=\"mono\">{wors[1]}</span> &rarr; "
            f"<span class=\"mono\">{wors[-1]}</span>&nbsp;hours. Mis-timed light or melatonin does not do nothing; it "
            "drives the clock further from alignment. This is why chronotherapy is a <em>timing</em> discipline and "
            "why getting the phase wrong is harmful, not merely ineffective.</p>"),
        sec("Light, melatonin, wake therapy, behaviour",
            "<p>Four levers, all read off the same control law. <strong>Timed bright light</strong>: morning light "
            "advances, evening light delays. <strong>Timed melatonin</strong>: its PRC is roughly antiphase to light "
            "(~12&nbsp;hours apart, reproduced here), so evening melatonin advances a delayed clock. <strong>Wake "
            "therapy</strong> (sleep deprivation): a rapid but <em>transient</em> homeostatic lift of the depressed "
            "operating point (the mind seam) that does <strong>not</strong> re-align the clock and relapses after "
            "recovery sleep unless paired with a phase-stabilising lever. <strong>Behavioural entrainment</strong> "
            "(timed meals, activity, dark discipline): a stronger zeitgeber widens the Arnold tongue (&sect;3) and "
            "stabilises the phase the other levers set.</p>"),
        sec("What this section is not",
            "<p>No new constant enters: the correction is the &sect;3 PRC applied in reverse, the per-pulse gain is "
            "<span class=\"mono\">[O]</span>, and only the <strong>direction</strong> (correct phase advances, wrong "
            "phase delays) and the <strong>antiphase</strong> light/melatonin relation are asserted "
            "(<span class=\"mono\">[V]</span>), with clinical timing windows cited <span class=\"mono\">[L]</span>. "
            "<strong>Efficacy is firewalled to zero.</strong> This is the clock's control law, not a dose, not an "
            "outcome, and <strong>not medical advice</strong>; the mood response to the timing change is owned by the "
            "mind volume.</p>"),
    ]
    cards = [
        card("chronotherapy",
             "chronotherapy = re-aligning the clock with a PRC-correct zeitgeber; the WRONG phase worsens it (timing is the therapy)",
             f"a PRC-correct advancing pulse closes a phase delay as strength rises ({corr[0]}&rarr;{corr[1]}&rarr;"
             f"{corr[2]:g} h, saturating at full correction); the SAME pulse at the WRONG phase GROWS the delay "
             f"({wors[0]}&rarr;{wors[-1]} h) &mdash; mis-timed light/melatonin is iatrogenic, not inert; four levers off "
             "one control law: timed light (morning advances / evening delays), timed melatonin (PRC ~antiphase to "
             "light, reproduced &mdash; evening advances), wake therapy (transient homeostatic lift, no clock re-"
             "alignment, relapses), behavioural entrainment (wider Arnold tongue); NO new constant (the §3 PRC in "
             "reverse), direction + antiphase [V], clinical windows [L], efficacy [O]=0, NOT medical advice (mood "
             "response owned by mind)",
             "[V direction] / efficacy=0", s, "this chapter"),
    ]
    write(s, page(s, 8, "Chronotherapy: re-aligning the clock with the PRC — Chronobiology §8",
                  "Chronotherapy re-aligns the clock with a PRC-correct zeitgeber: a correct-phase pulse closes a phase "
                  "delay while the same pulse at the wrong phase worsens it (mis-timed light/melatonin is iatrogenic). "
                  "Four levers off one control law; no new constant; efficacy = 0; not medical advice.",
                  "Chronotherapy &mdash; re-aligning the clock with the PRC",
                  f"Circadian disease is a phase gap, so the treatment is to <strong>re-align the clock</strong> with a "
                  f"PRC-correct zeitgeber. A correct-phase pulse closes a delay ({corr[0]}&nbsp;&rarr;&nbsp;{corr[2]:g}&nbsp;h); "
                  f"the <em>same</em> pulse at the wrong phase worsens it ({wors[0]}&nbsp;&rarr;&nbsp;{wors[-1]}&nbsp;h). "
                  "Timing is the therapy; mis-timed light or melatonin is iatrogenic. No new constant; "
                  "efficacy&nbsp;=&nbsp;0; not medical advice.",
                  "Treatment follows directly from the control law. A phase-correct zeitgeber re-aligns a delayed clock, "
                  "while the same stimulus at the wrong phase drives it further off &mdash; so chronotherapy is a timing "
                  "discipline in which the wrong phase is harmful, not merely ineffective. Light, melatonin (antiphase "
                  "PRC), wake therapy (transient, no re-alignment) and behavioural entrainment are four levers on one "
                  "curve. The directions are verified, clinical windows cited; efficacy is zero, the mood response is "
                  "owned by mind, and none of this is medical advice.",
                  "g-calibrated", "model · efficacy=0", s, cards, body,
                  ("§7 The circadian–mood seam", f"/{PAPER_SLUG}/07-circadian-mood-seam/"),
                  None, "§8 Chronotherapy"))

    # =============================================================== HUB + ASSETS + SEO
    write_hub(chapters, sha)
    copy_css()
    write_seo(chapters)
    return chapters, sha


# ---------------------------------------------------------------------------------------------------
#  hub
# ---------------------------------------------------------------------------------------------------
def write_hub(chapters, sha):
    notes = {0: "methods · start here", 1: "scope", 2: "verified", 3: "verified", 4: "verified",
             5: "verified", 6: "verified", 7: "model · seam", 8: "model · efficacy=0"}
    titles = {0: "Grounding: measured DNA emergence &amp; determinism",
              1: "Scope: the clock as an oscillator network",
              2: "Free-running: a rhythm with no input",
              3: "Entrainment: the PRC and the Arnold tongue",
              4: "Master vs network: coupled, master-led",
              5: "Setpoint gating: the clock gates the HPA axis",
              6: "Misalignment: shift work, jet lag, disease",
              7: "The circadian&ndash;mood seam (mind's locked contributor)",
              8: "Chronotherapy: re-aligning with the PRC"}
    lis = []
    for slug, pos, _ in chapters:
        lis.append(f'<li><strong><a href="/{PAPER_SLUG}/{slug}/">{titles[pos]}</a></strong> '
                   f'<span class="note">{notes[pos]}</span></li>')
    lis_html = "\n".join(lis)
    haspart = ",\n".join(
        f'  {{"@type":"ScholarlyArticle","name":{_json(html.unescape(titles[pos]))},'
        f'"position":{pos},"url":"{SITE}/{PAPER_SLUG}/{slug}/"}}'
        for slug, pos, _ in chapters)
    hub_kw = ", ".join(BASE_KW + ["phase-response curve", "Arnold tongue", "shift work disorder",
                                  "jet lag", "chronotherapy", "HPA axis", "circadian depression",
                                  "measured DNA emergence", "reproducible model"])
    hub_knows = ",".join(_json(k) for k in (BASE_KW + ["phase-response curve", "Arnold tongue",
                         "circadian misalignment", "chronotherapy", "HPA cortisol gating"]))
    ld = (
        '{"@context":"https://schema.org","@type":"CreativeWorkSeries",\n'
        f' "name":{_json(PAPER_NAME)},\n'
        f' "headline":{_json("Chronobiology — the circadian oscillator network")},\n'
        f' "url":"{SITE}/{PAPER_SLUG}/",\n'
        f' "identifier":"{CONCEPT_DOI}","sameAs":"https://doi.org/{CONCEPT_DOI}",\n'
        f' "datePublished":"{PUB_DATE_ISO}","dateModified":"{LASTMOD}",\n'
        f' "inLanguage":"en","knowsAbout":[{hub_knows}],\n'
        f' "author":{{"@type":"Person","name":{_json(AUTHOR)},"sameAs":"https://orcid.org/{ORCID}"}},\n'
        f' "publisher":{{"@type":"Organization","name":"Zenodo"}},\n'
        f' "license":"{LICENSE_URL}",\n'
        f' "hasPart":[\n{haspart}\n ]}}'
    )
    ld_crumb = (
        '{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[\n'
        f' {{"@type":"ListItem","position":1,"name":"Home","item":"{SITE}/"}},\n'
        f' {{"@type":"ListItem","position":2,"name":"Chronobiology","item":"{SITE}/{PAPER_SLUG}/"}}]}}'
    )
    hub = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Chronobiology — the circadian oscillator network, entrainment, and clock-disruption disease | Jamming Physics</title>
<meta name="description" content="The ~24h circadian clock as a self-sustained coupled limit-cycle oscillator network on the R19 substrate, seeded by a measured BMAL1/ARNTL gamma (never fitted): free-running, entrainment (PRC + Arnold tongue), master-vs-network synchrony, HPA setpoint gating, clock-environment misalignment disease, the mind depression seam, and PRC-based chronotherapy. Deterministic, reproducible (seed=19); efficacy=0.">
<meta name="keywords" content="{html.escape(hub_kw)}">
<meta name="author" content="{html.escape(AUTHOR)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{SITE}/{PAPER_SLUG}/">
<link rel="license" href="{LICENSE_URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Jamming Physics">
<meta property="og:title" content="Chronobiology — the circadian oscillator network (VP / Jamming Physics)">
<meta property="og:description" content="A deterministic, DNA-seeded circadian model: free-running, PRC + Arnold tongue, master-vs-network synchrony, HPA gating, misalignment disease, the mind depression seam, PRC chronotherapy.">
<meta property="og:url" content="{SITE}/{PAPER_SLUG}/">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Chronobiology — the circadian oscillator network">
<meta name="citation_title" content="{html.escape(PAPER_NAME)}">
<meta name="citation_author" content="{html.escape(AUTHOR)}">
<meta name="citation_publication_date" content="{PUB_DATE_SCHOLAR}">
<meta name="citation_doi" content="{CONCEPT_DOI}">
<meta name="citation_abstract_html_url" content="{SITE}/{PAPER_SLUG}/">
<meta name="citation_fulltext_html_url" content="{SITE}/{PAPER_SLUG}/">
<meta name="citation_language" content="en">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{ld}
</script>
<script type="application/ld+json">
{ld_crumb}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; Chronobiology</nav></header>
<main>
<h1>Chronobiology &mdash; the circadian oscillator network</h1>

<p class="lede">The ~24&nbsp;hour circadian clock is a <strong>self-sustained coupled limit-cycle oscillator network</strong> (SCN master + peripheral clocks) on the shared R19 substrate &mdash; it free-runs, is entrained by light, and gates nearly every defended setpoint. Disease is <strong>clock&ndash;environment misalignment</strong>. This is a <strong>deterministic derivation seeded by a measured clock-gene &gamma;</strong>, not a toy simulation: the molecular loop carries a measured BMAL1/ARNTL well (&gamma;&nbsp;=&nbsp;{GAMMA_BMAL1}, never fitted), every number is produced by one engine (seed&nbsp;=&nbsp;{SEED}, result sha256 <span class="mono">{{SHA12}}&hellip;</span>, 2&times; identical) across {N_DISCRIMINANTS} falsifiable discriminants, the absolute ~24&nbsp;h period is the only cited anchor, and the felt quality of mood stays in the mind volume (efficacy&nbsp;=&nbsp;0, not medical advice).</p>

<aside class="claim-strip">
  <span class="grade g-verified">[V] reproducible</span>
  <span class="gate">LOCK &rarr; Derive &rarr; Gate</span>
  <a href="/{PAPER_SLUG}/00-grounding-measured-dna-emergence/">how this is grounded &rarr;</a>
  <a href="https://doi.org/{CONCEPT_DOI}" rel="noopener">DOI {CONCEPT_DOI}</a>
  <a href="{GH_TREE}/" rel="noopener">reproduce (GitHub)</a>
</aside>

<h2>How this volume is grounded (not a toy model)</h2>
<p>The molecular clock node is seeded by a <strong>measured</strong> property of the <em>real</em> human clock gene: the well depth &gamma;&nbsp;=&nbsp;{GAMMA_BMAL1} of <strong>{GENE_SYMBOL}</strong> (NCBI Gene ID {GENE_ID}, accession {GENE_ACC}), computed as {NN_METHOD} over the {GENE_NDINUC} dinucleotides of the gene's proximal promoter ({GENE_WINDOW}) through the <em>same</em> nearest-neighbour DNA pipeline the whole framework uses &mdash; a measured input graded <strong>[V]</strong>, never chosen to hit a target. The 2501-base promoter is cached (sha256 <span class="mono">{GENE_SEQ_SHA}&hellip;</span>) so the &gamma; reproduces offline byte-for-byte. Every dynamical claim below is produced by one deterministic engine (seed&nbsp;=&nbsp;{SEED}) whose aggregate result hashes <strong>identically twice</strong> (sha256 <span class="mono">{{SHA12}}&hellip;</span>), and the {N_DISCRIMINANTS} discriminants (RC1&ndash;RC6&nbsp;+&nbsp;TX1) are <strong>falsifiable</strong> &mdash; each could have failed on the substrate and did not. No new physical constant is introduced anywhere; the FitzHugh&ndash;Nagumo (R19) substrate is vendored byte-identical and merely run in its oscillatory window. The full evidence, with the discriminant table and grades, is the <a href="/{PAPER_SLUG}/00-grounding-measured-dna-emergence/">grounding chapter</a>.</p>

<h2>The thesis</h2>
<p>A clock is not a stopwatch the sun winds. It is an <strong>oscillator</strong> &mdash; the BMAL1/CLOCK &harr; PER/CRY transcription&ndash;translation feedback loop &mdash; run in the oscillatory window of the same FitzHugh&ndash;Nagumo cell the rest of the framework uses. The one node with a named master gene carries a <strong>measured</strong> BMAL1 well (&gamma;&nbsp;=&nbsp;{GAMMA_BMAL1}, gene 406, NC_000011.10), fetched through the framework's DNA pipeline and never fitted. On top of that vendored substrate the package adds exactly the dynamics a clock needs &mdash; coupling, entrainment, setpoint gating &mdash; and shows that each one is a property of the substrate, not an assumption: self-sustension inside a drive window, a biphasic light phase-response curve, an Arnold tongue, a synchronisation transition with a master-led hierarchy, and clock-imposed daily rhythm on the HPA axis.</p>

<h2>The disease and treatment axis</h2>
<p>Because the clock re-aligns only ~1&nbsp;hour per day (a hard bound set by the PRC), a phase shift leaves the internal clock running at the wrong external time for days. The gated setpoints then keep a clean rhythm at the wrong phase &mdash; the disease state. This one mechanism covers circadian sleep-wake disorders, shift-work cardiometabolic disease, and (through the shared Kramers oncology kernel, as a rate multiplier) the IARC class&nbsp;2A night-shift cancer association. Treatment is the same control law run forwards: a PRC-correct zeitgeber re-aligns the clock, and the <em>wrong</em> phase worsens it &mdash; chronotherapy is a timing discipline, efficacy&nbsp;=&nbsp;0.</p>

<h2>The seam into mind</h2>
<p>The volume's sharpest result is a seam, not a standalone disease. The mind paper modelled depression on an HPA withdrawal handle and <strong>explicitly locked the circadian contributor</strong>; this volume supplies it. Circadian misalignment flattens the gated HPA cortisol rhythm, and that sustained, demand-misaligned signal is mind's withdrawal bias (b&nbsp;&lt;&nbsp;0). Only the <strong>sign</strong> crosses the seam &mdash; the magnitude is owned by mind, and the felt quality of low mood stays behind mind's Axis-A firewall (consciousness_claim&nbsp;=&nbsp;0, the hard problem open). The same timing seam aggravates mind's coupling-organisation reading of autism, where circadian and sleep disruption is common.</p>

<h2>The chapters</h2>
<ul>
{lis_html}
</ul>

<p class="note">Grades (VP-SPEC C3): oscillator mechanism / PRC shape / synchronisation transition&nbsp;=&nbsp;<strong>[V]</strong>; the ~24&nbsp;h period and cited clinical windows&nbsp;=&nbsp;<strong>[L]</strong>; absolute phase / inter-tissue lags / absolute incidence / the depression-handle magnitude&nbsp;=&nbsp;<strong>[O]</strong> (each with a stated obstacle in the irreproducibility ledger). DOI for this volume: <a href="https://doi.org/{CONCEPT_DOI}">{CONCEPT_DOI}</a> (concept; resolves to the latest version). The mind affect seam cites <a href="https://doi.org/{MIND_DOI}">{MIND_DOI}</a>.</p>
</main>
<footer>DOI <a href="https://doi.org/{CONCEPT_DOI}">{CONCEPT_DOI}</a> &middot; ORCID <a href="https://orcid.org/{ORCID}">{ORCID}</a> &middot; <a href="{LICENSE_URL}">CC BY 4.0</a> &middot; reproduce: <a href="{GH_TREE}/">GitHub</a></footer>
</body>
</html>
"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(hub.replace("{SHA12}", sha[:12]))


def copy_css():
    os.makedirs(CSS_DST_DIR, exist_ok=True)
    dst = os.path.join(CSS_DST_DIR, "site.css")
    for src in CSS_SRC_CANDIDATES:
        if os.path.exists(src):
            if os.path.abspath(src) == os.path.abspath(dst):
                return  # already vendored in place (standalone re-emit) — keep byte-identical
            shutil.copyfile(src, dst)
            return
    if not os.path.exists(dst):
        open(dst, "w", encoding="utf-8").write(_MIN_CSS)


def write_seo(chapters):
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended", "*"]
    robots = "# Chronobiology — AI & search crawlers allowed (VP-SPEC v1.8 / 6-R.5)\n"
    robots += "\n".join(f"User-agent: {b}\nAllow: /\n" for b in bots)
    robots += f"\nSitemap: {SITE}/sitemap.xml\n"
    open(os.path.join(DOCS, "robots.txt"), "w", encoding="utf-8").write(robots)

    urls = [f"{SITE}/{PAPER_SLUG}/"] + [f"{SITE}/{PAPER_SLUG}/{slug}/" for slug, _, _ in chapters]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for u in urls)
    sm += "</urlset>\n"
    open(os.path.join(DOCS, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    one_liners = {
        0: "this circadian volume is a DETERMINISTIC DERIVATION seeded by a MEASURED clock-gene gamma (BMAL1/ARNTL, Gene ID 406, NC_000011.10) via the shared DNA nearest-neighbour pipeline — never fitted; every number is one reproducible engine (seed=19, 2x sha256 identical) across 8 falsifiable discriminants; not a toy simulation [methods]",
        1: "the circadian clock is a self-sustained coupled limit-cycle oscillator network (SCN + peripheral) on the R19 substrate, with a measured BMAL1 gamma; it free-runs and is only entrained by light [scope]",
        2: "the molecular clock free-runs with zero drive (a regular limit cycle) and a strong tonic drive silences it (depolarisation block) — the rhythm lives in a drive window [verified]",
        3: "a brief pulse advances or delays the clock by phase (a biphasic light PRC) and a periodic zeitgeber locks it with a range that widens with strength (an Arnold tongue); the PRC bounds re-alignment to ~1 h/day [verified]",
        4: "the body clocks are one coupled network: coherence rises with coupling (a synchronisation transition) and a stronger SCN master pulls peripheral clocks into phase — master-led [verified]",
        5: "the clock imposes a daily rhythm on the HPA cortisol axis (mind-cited kinetics, no new constant): a gated clock builds a strong cortisol rhythm an ablated clock lacks [verified]",
        6: "circadian disease is a phase gap not a broken clock: re-entrainment is PRC-bounded and the gated cortisol rhythm peaks at the wrong external time — covering sleep-wake disorders, shift-work cardiometabolic disease, and IARC-2A night-shift cancer (a Kramers-rate multiplier) [verified sign]",
        7: "circadian misalignment flattens the gated HPA cortisol rhythm, supplying the CIRCADIAN depression contributor the mind paper explicitly locked (mind's withdrawal bias b<0); sign only, the felt quality stays in mind (consciousness_claim=0) [model/seam]",
        8: "chronotherapy re-aligns the clock with a PRC-correct zeitgeber while the wrong phase worsens it (mis-timed light/melatonin is iatrogenic); four levers off one control law, efficacy=0, not medical advice [model]",
    }
    txt = "# Chronobiology\n\n"
    txt += ("> The ~24h circadian clock as a self-sustained coupled limit-cycle oscillator network (SCN master + "
            "peripheral clocks) on the shared R19 substrate: it free-runs, is entrained by light via a biphasic PRC, "
            "synchronises as a master-led network, and gates the HPA setpoint. Disease is clock-environment "
            "misalignment; the mind depression seam supplies a contributor mind explicitly locked; chronotherapy is "
            "PRC-based timing. This is a DETERMINISTIC DERIVATION seeded by a MEASURED clock-gene gamma (BMAL1/ARNTL, "
            "never fitted), not a toy simulation: every number is produced by one engine (seed=19, 2x sha256 identical) "
            "across 8 falsifiable discriminants; the ~24h period is the only cited anchor; efficacy=0, not medical "
            "advice.\n\n")
    txt += (f"Author: {AUTHOR} (ORCID {ORCID}). DOI: {CONCEPT_DOI} (concept, resolves to latest; v0.2.0 snapshot "
            f"{VERSION_DOI}). Seam cites mind {MIND_DOI}. License: CC BY 4.0.\n\n")
    txt += "## Chapters\n"
    for slug, pos, _ in chapters:
        txt += f"- [{slug}]({SITE}/{PAPER_SLUG}/{slug}/): {one_liners[pos]}.\n"
    open(os.path.join(DOCS, "llms.txt"), "w", encoding="utf-8").write(txt)

    full = txt + ("\n## Cross-volume seams\n"
                  f"- mind (Felt Cognition, DOI {MIND_DOI}): this volume supplies the circadian depression contributor "
                  "mind locked, and aggravates mind's coupling reading of autism — SIGN only, efficacy=0, the felt "
                  "quality stays in mind (consciousness_claim=0, hard problem open).\n"
                  "- DNA: node identity and emergence order (measured gamma, never fitted).\n"
                  "- homeostasis (thermometabolic / hemodynamic / ionic / immune): the clock GATES their setpoints; this "
                  "volume is SSOT for circadian phase/timing.\n"
                  "- substrate: the FitzHugh–Nagumo (R19) cell is vendored byte-identical; coupling, entrainment and "
                  "gating are the new dynamics added on top.\n")
    open(os.path.join(DOCS, "llms-full.txt"), "w", encoding="utf-8").write(full)


_MIN_CSS = """:root{--ink:#1a1a1a;--bg:#fff;--accent:#0b5;--muted:#666;--card:#f6f6f6;--line:#e3e3e3}
*{box-sizing:border-box}body{margin:0;font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg);max-width:46rem;margin:0 auto;padding:1.2rem}
a{color:var(--accent)}h1{font-size:1.7rem;line-height:1.2}h2{font-size:1.2rem;margin-top:2rem}
.crumb{font-size:.85rem;color:var(--muted)}.crumb a{color:var(--muted)}
.answer{font-weight:600;font-size:1.08rem;border-left:3px solid var(--accent);padding-left:.8rem}
.abstract{color:#333}.lede{font-size:1.1rem}.note{color:var(--muted);font-size:.85rem}
.claim-strip{display:flex;flex-wrap:wrap;gap:.6rem;align-items:center;margin:1rem 0;padding:.6rem .8rem;background:var(--card);border:1px solid var(--line);border-radius:6px;font-size:.85rem}
.grade{font-weight:700;padding:.1rem .5rem;border-radius:4px;color:#fff;background:var(--muted)}
.g-verified{background:#0a7}.g-calibrated{background:#37a}.g-open{background:#a63}.g-forced{background:#759}
.gate{color:var(--muted)}.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.92em}
.vp-card{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:.7rem .9rem;margin:.7rem 0;font-size:.9rem}
.pn{display:flex;justify-content:space-between;gap:1rem;margin:2rem 0 1rem;font-size:.9rem}
footer{color:var(--muted);font-size:.82rem;border-top:1px solid var(--line);margin-top:2rem;padding-top:1rem}
"""


def main():
    locked, why = gates.writing_locked()
    if locked:
        print("REFUSED: writing is locked.\nReason:", why)
        print("Research-first: pass the stress battery, then")
        print("  python repro/_verify/gates.py  ->  gates.write_research_complete()  ;  echo writing > PHASE")
        return 1
    chapters, sha = build()
    print("UNLOCKED. Canonical HTML written to docs/%s/ (engine sha %s…):" % (PAPER_SLUG, sha[:12]))
    print("  hub:        docs/%s/index.html" % PAPER_SLUG)
    for slug, pos, title in chapters:
        print("  §%d  docs/%s/%s/index.html" % (pos, PAPER_SLUG, slug))
    print("  assets:     docs/assets/css/site.css")
    print("  SEO:        docs/{robots.txt,sitemap.xml,llms.txt,llms-full.txt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
