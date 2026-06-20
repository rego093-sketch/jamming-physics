#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch29_bipolar.py — emit the §29 bipolar disorder chapter (roadmap T2b).

Writes docs/mind/29-bipolar-state-switching/index.html from the content below, using the same
head/JSON-LD/footer scaffolding as the other Part-II chapters so the SEO markup is byte-
consistent. The answer-first <p class="answer"> and the vp-card asides are NOT written here —
build_search_layer.py injects them from mind_registry.py (single source of truth): this
generator only emits the skeleton (abstract + claim-strip + body sections + nav). Body text is
English-only (VP-SPEC C0). The numbers quoted in the prose are the SIGN/direction results from
repro/mind/_verify/bipolar_state_switching.py (efficacy=0; sign-only); the canonical numeric
artifact is that module's bipolar_state_switching_results.json.

This is the second TEMPORAL disorder. It IMPORTS two layers — the state-switching layer (E2,
the fast switch) and the plasticity layer (E0, the slow trace) — and re-derives neither.

One-shot authoring helper; the emitted HTML is the canonical artifact.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, os.pardir))
MIND = os.path.join(PKG, "docs", "mind")
DOI = "10.5281/zenodo.20694404"
ORCID = "0009-0002-7535-8245"
PAPER = "Felt Cognition: Parallel Micro-Eddies, the Stream of Thought, and the Open Problem of Experience"
GH = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/mind"

NO = 29
SLUG = "29-bipolar-state-switching"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Bipolar disorder: two poles on one axis, episodes as bistable switches"
H1 = "Bipolar disorder &mdash; two poles on one valence axis, episodes as bistable transitions"
CRUMB = "Bipolar: two poles, switching &amp; kindling"
HEADLINE = ("Bipolar disorder as two operating poles on one valence axis: mania above health and "
            "depression below, episodes as bistable transitions, kindling as the retained trace, and "
            "the mood-stabiliser sign as barrier-raising")
META = ("Bipolar disorder read as two operating poles on ONE valence axis -- mania sits above the "
        "healthy order parameter, depression below -- with episodes as bistable transitions of the "
        "state-switching layer and kindling as the plasticity layer's retained trace accumulating "
        "across episodes, so each switch gets easier. The mood-stabiliser sign is barrier-raising: "
        "raise the barrier, raise the threshold to switch. The second temporal disorder, importing "
        "E2 and E0. efficacy=0; not medical advice.")

ABSTRACT = (
    "<a href=\"/mind/27-depression-chronification/\">Depression</a> was the first temporal disorder, but "
    "it lives on <em>one</em> side of the healthy operating point &mdash; below it, withdrawn. Bipolar "
    "disorder is the condition that needs <strong>both</strong> sides and the <strong>switch between "
    "them</strong>, and it is the first disorder to use the "
    "<a href=\"/mind/28-state-switching/\">state-switching layer</a> the previous chapter built. The "
    "claim is that mania and depression are <strong>two operating poles on the same valence axis</strong>, "
    "not two diseases: the engine's own valence geometry (the M17 approach / avoidance axis, with "
    "dopamine on the approach pole and the M18 cortisol cascade on the withdrawal pole) supplies the "
    "axis, and the same coupling map the atlas uses throughout supplies the poles &mdash; with "
    "<strong>no new constant</strong>. Five sign-only results, all over swept severities. The "
    "<strong>two poles</strong>: a manic (approach) bias raises the global order parameter "
    "<strong>above health</strong> (<span class=\"mono\">R 0.42 &gt; 0.39</span>), a depressive "
    "(withdrawal) bias lowers it <strong>below health</strong> (<span class=\"mono\">0.37 &lt; 0.39</span>), "
    "and euthymia is the healthy anchor between them &mdash; one axis, two excursions. An "
    "<strong>episode is a bistable transition</strong>: it inherits the switching layer's hysteresis and "
    "its diverging-at-the-fold latency, so an episode is entered at one fold and only left at the other "
    "(why a mood state persists after its trigger lifts). <strong>Kindling</strong> is the "
    "<a href=\"/mind/26-plasticity-consolidation/\">plasticity layer</a> acting across episodes: each "
    "alternating manic / depressive excursion writes a retained structural trace that "
    "<strong>accumulates</strong> (<span class=\"mono\">&#8741;&Delta;W&#8741;</span> deepening "
    "monotonically with episode count), and a deeper trace <strong>lowers the barrier</strong>, so each "
    "subsequent switch is easier &mdash; the clinical progression toward more frequent, more autonomous "
    "episodes, as a mechanism direction. The <strong>mood-stabiliser sign</strong> is "
    "<strong>barrier-raising</strong>: anything that deepens the well raises the threshold to switch, so "
    "episodes become harder to enter &mdash; a sign, never a dose. The module <strong>imports</strong> "
    "both layers rather than re-deriving them, adds no tuned constant, and with the rate and bias off "
    "reproduces the frozen engine bit-for-bit. <span class=\"mono\">efficacy = 0</span>; not medical "
    "advice; the hard problem stays open."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("The disorder that needs both sides of the axis", [
        "Depression placed a condition <em>below</em> the healthy operating point: a sustained withdrawal "
        "that lowers coordination and, with plasticity, chronifies. Bipolar disorder cannot be read that "
        "way, because its defining feature is not a single displaced operating point but a "
        "<strong>movement between two</strong> &mdash; an elevated, over-driven pole and a withdrawn, "
        "under-driven one &mdash; and the <strong>switching</strong> that carries the system from one to "
        "the other. It is therefore the first disorder that genuinely needs the "
        "<a href=\"/mind/28-state-switching/\">state-switching layer</a>, and it pairs that fast switch "
        "with the slow <a href=\"/mind/26-plasticity-consolidation/\">plasticity trace</a> to get the "
        "longitudinal course. Nothing below is built fresh: the chapter <em>imports</em> both layers and "
        "the engine's valence geometry, and reads off the consequences.",
        "The axis is the engine's own. The <strong>M17 valence geometry</strong> carries an approach / "
        "avoidance dimension &mdash; dopaminergic approach on one pole, the <strong>M18 cortisol "
        "cascade</strong> on the withdrawal pole &mdash; and that single dimension is what bipolar moves "
        "along. Mania is the approach pole driven high; depression is the withdrawal pole driven low; "
        "euthymia is the healthy point between. Mapping each pole to a sustained bias uses the "
        "<em>same</em> coupling map <span class=\"mono\">k = &kappa;/(1&minus;|b|)</span> (approach, "
        "excitatory) / <span class=\"mono\">&kappa;/(1+|b|)</span> (withdrawal, inhibitory), capped at "
        "<span class=\"mono\">2&kappa;</span>, that the schizophrenia, epilepsy and depression modules "
        "use. <strong>No new tuned constant enters.</strong>",
    ]),
    sec("Two poles on one valence axis (B1)", [
        "The first result is the structural claim, made concrete. Drive the valence handle to the "
        "<strong>approach</strong> pole and the global order parameter rises <strong>above</strong> the "
        "healthy anchor (<span class=\"mono\">R = 0.422 &gt; 0.390</span>) &mdash; the manic operating "
        "point, an over-coordinated, over-driven regime. Drive it to the <strong>withdrawal</strong> pole "
        "and the order parameter falls <strong>below</strong> health "
        "(<span class=\"mono\">R = 0.367 &lt; 0.390</span>) &mdash; the depressive operating point, the "
        "same low-coordination state the depression chapter read. Euthymia is the healthy anchor "
        "<em>between</em> the two (<span class=\"mono\">R = 0.390</span>), and the ordering "
        "<span class=\"mono\">depressive &lt; euthymic &lt; manic</span> is <strong>monotone</strong> "
        "across the severity sweep. That is the whole bipolar claim in one line: <strong>not two "
        "diseases, but two excursions on a single axis around one healthy point</strong>. It also says "
        "why unipolar depression and the depressed phase of bipolar can look alike at the bottom of the "
        "axis while differing in what the system does next &mdash; whether it can be driven past the "
        "healthy point to the opposite pole.",
    ]),
    sec("An episode is a bistable transition (B2)", [
        "What is an <em>episode</em>, mechanically? It is a <strong>switch</strong>, and the "
        "state-switching layer already characterised switches. The bipolar module inherits that layer "
        "directly: the transition between poles shows the same <strong>hysteresis loop</strong> of width "
        "<span class=\"mono\">2&times;spinodal &asymp; 0.77</span> (the up- and down-switches on opposite "
        "sides of the healthy point), the same transition <strong>latency that falls as the drive "
        "overshoots the fold</strong> (here <span class=\"mono\">31.6 &rarr; 1.9</span> across the "
        "severity sweep) and diverges as it approaches the fold, and the same static limit reproducing "
        "the engine's <span class=\"mono\">settle</span> bit-for-bit. Two clinical directions follow as "
        "mechanism, not timing. <strong>Hysteresis &rarr; persistence</strong>: because entry is at one "
        "fold and exit only at the other, an episode does <em>not</em> end when its trigger is removed &mdash; "
        "the state must be driven back past the opposite fold, which is why a mood episode outlasts its "
        "precipitant. <strong>Critical slowing &rarr; prodrome</strong>: a switch approached slowly shows "
        "a long latency &mdash; a gradual run-up &mdash; while a strong push gives an abrupt onset. The "
        "episode is the switching layer applied to the valence axis; nothing new is asserted about it.",
    ]),
    sec("Kindling: episodes accumulate a trace (B3)", [
        "The longitudinal course of bipolar disorder &mdash; episodes growing more frequent, more "
        "autonomous, less tied to external stressors over years &mdash; is clinically called "
        "<strong>kindling</strong>, and it is exactly what the <a href=\"/mind/26-plasticity-consolidation/\">"
        "plasticity layer</a> produces across repeated switches. Run alternating manic and depressive "
        "excursions with plasticity on and the retained structural trace "
        "<strong>accumulates monotonically</strong> with episode count "
        "(<span class=\"mono\">&#8741;&Delta;W&#8741;</span> deepening "
        "<span class=\"mono\">0.06 &rarr; 0.11 &rarr; 0.17 &rarr; 0.22 &rarr; 0.27 &rarr; 0.33</span> over "
        "successive episodes), and the depth grows across the whole rate sweep (anti-tuning). The "
        "consequence is the one that matters: a deeper accumulated trace <strong>lowers the barrier</strong> "
        "between poles, so each subsequent switch requires <em>less</em> drive &mdash; the drive needed to "
        "flip falls as episodes pile up. That is kindling as a mechanism direction: history makes the next "
        "episode easier, which is the model's reading of why early intervention and episode prevention are "
        "emphasised clinically. It must be said exactly what this is: a retained structural trace is a "
        "<strong>mechanism boundary, not a claim about the felt quality of mania or depression</strong>, and "
        "the numbers are sign-only directions over a sweep, not a timeline for any person. "
        "<span class=\"mono\">efficacy = 0</span>.",
    ]),
    sec("The mood-stabiliser sign (B4)", [
        "If episodes are switches and kindling lowers the barrier, the mechanism sign of a "
        "<strong>mood stabiliser</strong> is forced and direction-only: it is whatever <strong>raises the "
        "barrier</strong>. Raise the well depth and the switching threshold rises with it (the flip drive "
        "climbing <span class=\"mono\">0.38 &rarr; 0.44 &rarr; 0.51 &rarr; 0.64</span> across the "
        "barrier-raising sweep) &mdash; a state that flips under a fixed drive at low barrier "
        "<strong>holds</strong> against the same drive once the barrier is raised. A stabiliser, in this "
        "reading, is not something that pushes the system toward one pole; it is something that "
        "<strong>deepens the well around euthymia</strong> so that <em>both</em> manic and depressive "
        "switches become harder to enter. This is the direct counterpart of the kindling result: kindling "
        "lowers the barrier and makes switching easier; stabilisation raises the barrier and makes "
        "switching harder. The sign is all the model asserts &mdash; it speaks to the <em>direction</em> of "
        "a barrier change, and <strong>nothing</strong> about which agent does this, at what dose, in whom, "
        "or whether any real drug acts this way. <span class=\"mono\">medium_efficacy_tested = 0</span>.",
    ]),
    sec("Imports two layers; a pure add-on (B5)", [
        "The guard closes the discipline. With the rate set to zero and no bias applied, the bipolar module "
        "reproduces the frozen M9 coordination anchor <strong>bit-for-bit</strong> "
        "(<span class=\"mono\">R = 0.38961455156044245</span>), leaves <span class=\"mono\">W</span> "
        "identical to the kernel, and its static limit matches the engine's <span class=\"mono\">settle</span> "
        "exactly. The engine file stays <span class=\"mono\">e61083ae&hellip;</span> and the emergence tree "
        "stays <span class=\"mono\">0fbf4988&hellip;</span>, byte-unchanged. And the module <strong>imports "
        "both layers</strong> rather than re-deriving either: the fast switch from the "
        "<a href=\"/mind/28-state-switching/\">state-switching layer</a> (E2), the slow trace from the "
        "<a href=\"/mind/26-plasticity-consolidation/\">plasticity layer</a> (E0). Bipolar is what those two "
        "layers do <em>together</em> on the valence axis &mdash; a fast switch between poles, a slow trace "
        "that records the switching &mdash; with no third mechanism invented.",
        "Everything here is an in-silico <em>coupling state</em>, not a clinical measure, a diagnosis, or a "
        "prescription. The model asserts <em>mechanism directions</em> &mdash; mania and depression are poles "
        "of one axis; an episode is a bistable switch that persists past its trigger; kindling lowers the "
        "barrier; stabilisation raises it &mdash; and <strong>nothing</strong> about which bipolar any "
        "individual has, the place of bipolar I versus II versus cyclothymia, the role of mixed states, "
        "rapid cycling, or psychosis, whether any drug treats anyone's illness, or that anyone should change "
        "a treatment. Real bipolar disorder is heterogeneous, with genetic, circadian, monoaminergic and "
        "psychosocial contributors, and that heterogeneity is <strong>locked</strong>. A bistable transition "
        "and a retained trace are mechanism boundaries, <strong>not</strong> a claim about the felt quality "
        "of a mood state (Axis-A firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>, the "
        "hard problem of experience stays <strong>open</strong>). Addiction, which needs sensitisation, "
        "remains owed to a later module. <strong>This is not medical advice, not a diagnosis, not a treatment "
        "protocol, and not a cure.</strong> <span class=\"mono\">efficacy = 0</span>.",
    ]),
])

PREV = '<a rel="prev" href="/mind/28-state-switching/">&larr; §28 The state-switching layer</a>'
NEXT = "<span></span>"

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE_TAG} — Felt Cognition §{NO} | Jamming Physics</title>
<meta name="description" content="{META}">
<link rel="canonical" href="https://jamming-physics.org/mind/{SLUG}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ScholarlyArticle",
 "headline":"{HEADLINE}",
 "isPartOf":{{"@type":"CreativeWork","name":"{PAPER}",
   "sameAs":"https://doi.org/{DOI}"}},
 "position":{NO},
 "author":{{"@type":"Person","name":"Young Jae Lee",
   "sameAs":"https://orcid.org/{ORCID}"}},
 "license":"https://creativecommons.org/licenses/by/4.0/"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Home","item":"https://jamming-physics.org/"}},
 {{"@type":"ListItem","position":2,"name":"Felt Cognition","item":"https://jamming-physics.org/mind/"}},
 {{"@type":"ListItem","position":3,"name":"\\u00a7{NO} {CRUMB}"}}]}}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/mind/">Felt Cognition</a> &rsaquo; §{NO}</nav></header>
<main>
<h1>{H1}</h1>
<p class="abstract">{ABSTRACT}</p>

<aside class="claim-strip">
  <span class="{GRADE_CLASS[GRADE]}">{GRADE}</span>
  <span class="gate">LOCK → Derive → Gate</span>
  <a href="{GH}/29-bipolar-state-switching/" rel="noopener">reproduce (GitHub)</a>
  <a href="https://doi.org/{DOI}" rel="noopener">DOI snapshot</a>
</aside>
{BODY}
<nav class="pn">
  {PREV}
  <a href="/mind/">paper contents</a>
  {NEXT}
</nav>
</main>
<footer>DOI <a href="https://doi.org/{DOI}">{DOI}</a> · ORCID <a href="https://orcid.org/{ORCID}">{ORCID}</a> · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></footer>
</body>
</html>
"""


def main():
    outdir = os.path.join(MIND, SLUG)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print(f"wrote {path} ({len(HTML)} bytes)")


if __name__ == "__main__":
    main()
