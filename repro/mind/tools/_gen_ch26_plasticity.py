#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch26_plasticity.py — emit the §26 plasticity / consolidation chapter (roadmap E0).

Writes docs/mind/26-plasticity-consolidation/index.html from the content below, using the
same head/JSON-LD/footer scaffolding as the other Part-II chapters so the SEO markup is
byte-consistent. The answer-first <p class="answer"> and the vp-card asides are NOT written
here — build_search_layer.py injects them from mind_registry.py (single source of truth):
this generator only emits the skeleton (abstract + claim-strip + body sections + nav). Body
text is English-only (VP-SPEC C0). The numbers quoted in the prose are the SIGN/direction
results from repro/mind/_verify/e0_plasticity.py (efficacy=0; sign-only); the canonical
numeric artifact is that module's e0_plasticity_results.json.

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

NO = 26
SLUG = "26-plasticity-consolidation"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "The plasticity layer: consolidation &amp; the reversible&rarr;chronified switch"
H1 = "The plasticity layer &mdash; consolidation and the reversible&rarr;chronified switch"
CRUMB = "Plasticity: consolidation &amp; chronification"
HEADLINE = ("The plasticity / consolidation layer: a phase-correlation Hebbian update on the "
            "ephaptic kernel, and the reversible-to-chronified switch")
META = ("The plasticity / consolidation layer the structural atlas never had: a slow phase-"
        "correlation Hebbian update on the frozen ephaptic kernel. It makes consolidation and "
        "stimulation after-effects representable, resolves the open continuous-vs-periodic "
        "dosing question (spaced dosing leaves a larger retained structural trace than massed, "
        "so the cap repairs and pacing beats holding), and builds the reversible-to-chronified "
        "switch every temporal disorder depends on; with plasticity off it reproduces the frozen "
        "engine bit-for-bit. efficacy=0; not medical advice.")

ABSTRACT = (
    "Every module so far read a <em>static</em> operating point: the frozen engine has no "
    "variable that changes with use. That gap is why the <a href=\"/mind/20-theta-cap-pacemaker/\">"
    "&theta;-cap</a> chapters could show the cap <em>paces</em> the network but could not ask "
    "whether holding it there <em>repairs</em> anything &mdash; the substrate had nothing to "
    "retain &mdash; and why the cap's plasticity sign was left <strong>open [O]</strong>. This "
    "chapter adds the missing layer on top of the <strong>READ-ONLY</strong> engine: a slow "
    "<strong>phase-correlation Hebbian update</strong> of the ephaptic kernel "
    "<span class=\"mono\">W</span>, "
    "<span class=\"mono\">W<sub>ij</sub> &larr; max(0, W<sub>ij</sub>(1+&eta;C<sub>ij</sub>))</span> "
    "with <span class=\"mono\">C<sub>ij</sub> = &lt;cos(&theta;<sub>j</sub>&minus;&theta;<sub>i</sub>)&gt;</span>. "
    "The rule <strong>form is forced [F]</strong> (standard phase-STDP, no free constant, "
    "row-stochastic so the ephaptic locality is preserved); the <strong>rate &eta; is [O]</strong> "
    "and every sign below survives an &eta; sweep (anti-tuning). Four results: consolidation and "
    "after-effects become representable; the open <strong>continuous-vs-periodic dosing</strong> "
    "question is <strong>resolved</strong> (spaced leaves a larger retained trace than massed &mdash; "
    "the cap <em>repairs</em>, and pacing beats holding); the <strong>reversible&rarr;chronified "
    "switch</strong> is built; and with <span class=\"mono\">&eta;=0</span> the layer reproduces the "
    "frozen M9 coordination anchor <strong>bit-for-bit</strong> (a pure add-on). The layer, not an "
    "application: the mood and cycle disorders that use it are owed to later modules. "
    "<span class=\"mono\">efficacy = 0</span>."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("The layer the structural atlas never had", [
        "Autism on the T/O/W axes, schizophrenia at the over-ignition pole, epilepsy at the "
        "over-synchronisation ceiling &mdash; every result in the atlas so far has been read off a "
        "<em>static</em> operating point. Move a bias, the order parameter moves; remove it, the "
        "network returns. Nothing in the frozen engine changes with use, because the engine has "
        "no plasticity variable at all. That is not a small omission. It is precisely why the "
        "&theta;-cap operating-principle chapter could establish that the cap <em>paces</em> the "
        "network &mdash; across ON/OFF cycling there was no rebound and no acquired dependence &mdash; "
        "but could not say whether parking the network at the cap <em>repairs</em> anything, "
        "because the substrate had nothing in which to keep a change. The plasticity sign of the "
        "operating principle was left explicitly <span class=\"mono\">[O]</span> for that reason. "
        "This chapter supplies the missing variable, and in doing so closes that open question.",
    ]),
    sec("The rule: Hebb read on phase (form forced, rate open)", [
        "On phase oscillators the time-averaged spike-timing plasticity window between two units "
        "reduces to a function of their phase difference: pairs that run in phase potentiate, pairs "
        "in anti-phase depress. It is Hebb's rule &mdash; <em>fire together, wire together</em> &mdash; "
        "read on phase. We take the steady-state pairwise phase correlation "
        "<span class=\"mono\">C<sub>ij</sub> = &lt;cos(&theta;<sub>j</sub>&minus;&theta;<sub>i</sub>)&gt;</span> "
        "as the Hebbian signal and update the ephaptic kernel multiplicatively, "
        "<span class=\"mono\">W<sub>ij</sub> &larr; max(0, W<sub>ij</sub>(1+&eta;C<sub>ij</sub>))</span>, "
        "then row-renormalise. The <strong>form has no free constant</strong>: the diagonal stays "
        "zero, weights stay non-negative, and the row-renormalisation keeps the rows stochastic so "
        "the <span class=\"mono\">~1/r&sup3;</span> ephaptic locality of the frozen kernel is "
        "preserved. The single <strong>rate &eta; is [O]</strong> &mdash; representative, exactly as "
        "the absolute Hz, the ring geometry and <span class=\"mono\">R_BRAIN</span> are [O] in M9 "
        "&mdash; and, crucially, the signs asserted below are required to hold over a <strong>sweep</strong> "
        "of &eta;, so no number is fit to a target. The map from a drive or a faulted bias to an "
        "effective coupling is the <em>same</em> "
        "<span class=\"mono\">k = &kappa;/(1&minus;|b|)</span> (excitatory) / "
        "<span class=\"mono\">&kappa;/(1+|b|)</span> (inhibitory), capped at "
        "<span class=\"mono\">2&kappa;</span>, used in the schizophrenia and epilepsy modules. "
        "<strong>No new tuned constant enters.</strong>",
    ]),
    sec("Consolidation: the network remembers (E0.1)", [
        "The first thing the layer makes possible is the most basic, and the one the static engine "
        "simply could not express. Drive the network at the <em>healthy</em> operating point under "
        "plasticity, then switch the drive off and read the order parameter. It does not fall back "
        "to where it started: it sits <em>at or above</em> baseline "
        "(<span class=\"mono\">R</span> 0.390 &rarr; 0.391, "
        "<span class=\"mono\">&Delta;R &gt; 0</span>), and the sign stays positive across the whole "
        "&eta; sweep. The coordination has been written into the structure &mdash; a stimulation "
        "<em>after-effect</em>. This is the substrate for learning, for use-dependent change, for "
        "the lasting trace of an intervention: none of which a plasticity-free engine could "
        "represent, all of which fall out of one forced rule.",
    ]),
    sec("The dosing question, resolved: pace, don&rsquo;t hold (E0.2)", [
        "The &theta;-cap chapters left a concrete device question open. If a cap-class stimulation "
        "has a fixed total budget, is it better delivered <em>continuously</em> (held at the cap) "
        "or in <em>spaced bursts</em>? With no plasticity the question is empty &mdash; nothing is "
        "retained either way. With the layer present it has an answer. Deliver the same total "
        "time-at-cap two ways: <strong>massed</strong> (one continuous run) and <strong>spaced</strong> "
        "(periodic ON/OFF bursts, the plasticity rule running through the OFF gaps). The spaced "
        "protocol leaves a <strong>larger retained structural trace</strong> per unit dose "
        "(<span class=\"mono\">&#8741;&Delta;W&#8741;</span> 0.225 vs 0.115 for massed) &mdash; a "
        "<em>spacing effect</em> emerging from pure phase-plasticity, the same direction learning "
        "science calls distributed practice. Two consequences follow, both sign-only. First, with "
        "plasticity present the cap <strong>repairs</strong>: it leaves a lasting trace, which is "
        "exactly the <span class=\"mono\">[O]</span> the &theta;-cap operating principle could not "
        "resolve. Second, <strong>pacing beats holding</strong> &mdash; pulse, do not hold. The sign "
        "holds at every point of an &eta;&times;epochs sweep. It is a direction that would change a "
        "protocol, not a dose and not an efficacy: <span class=\"mono\">efficacy = 0</span>.",
    ]),
    sec("The reversible&rarr;chronified switch (E0.3)", [
        "The most consequential result is the cleanest. Drive a sustained <em>faulted</em> "
        "(excitatory) bias and then remove it. <strong>Without</strong> plasticity "
        "(<span class=\"mono\">&eta;=0</span>) the excursion fully <strong>reverts</strong>: the "
        "order parameter returns <em>exactly</em> to baseline. That is, precisely, the chapter-20 "
        "result &mdash; <em>paces, not repairs; no rebound, no acquired dependence</em> &mdash; now "
        "shown to be a <strong>consequence of the plasticity-free substrate</strong>, not a property "
        "of the cap. <strong>With</strong> plasticity "
        "(<span class=\"mono\">&eta;&gt;0</span>) the same excursion leaves a retained trace that "
        "does <em>not</em> revert when the bias is removed "
        "(<span class=\"mono\">R</span> holds at 0.394 &gt; 0.390): a faulted state has written "
        "itself into the structure. <strong>Plasticity is the switch between a reversible state and "
        "a chronified one.</strong> It must be said exactly what this is and is not: a retained "
        "structural trace is a <strong>mechanism boundary, not a claim about the felt quality of "
        "chronic illness</strong> (Axis-A firewall &mdash; <span class=\"mono\">consciousness_claim = "
        "0</span>; the hard problem of experience stays <strong>open</strong>). The model speaks to "
        "whether a state can persist in the structure, not to what, if anything, that persistence "
        "feels like.",
    ]),
    sec("A pure add-on, and what it unlocks (E0.4)", [
        "The guard makes the discipline operational. With <span class=\"mono\">&eta;=0</span> the "
        "layer reproduces the frozen M9 coordination anchor <strong>bit-for-bit</strong> "
        "(<span class=\"mono\">R = 0.38961455156044245</span>) and leaves "
        "<span class=\"mono\">W</span> identical to the kernel. Turning plasticity off recovers the "
        "frozen engine <em>exactly</em>: the engine file stays "
        "<span class=\"mono\">e61083ae&hellip;</span>, the emergence tree stays "
        "<span class=\"mono\">0fbf4988&hellip;</span>, byte-unchanged. <strong>E0 adds; it does not "
        "alter.</strong>",
        "And it is a layer, not a disorder. Its purpose is to be the foundation the <em>temporal</em> "
        "conditions stand on. Depression as the chronification of a low-coordination operating point, "
        "bipolar as the accumulation of episodes, addiction as sensitisation &mdash; each needs a "
        "substrate in which a state can write itself in and stay. E0 supplies that substrate once, "
        "as a reusable object; the mood and cycle modules that follow <em>import</em> it rather than "
        "re-deriving it. Everything here is an in-silico coupling state, not a clinical measure. "
        "This is a mechanism-level result about plasticity <em>as represented in the VP framework</em> "
        "&mdash; not medical advice, not a diagnosis, not a treatment protocol, and not a cure. "
        "<span class=\"mono\">efficacy = 0</span>; the hard problem stays open.",
    ]),
])

PREV = '<a rel="prev" href="/mind/25-epilepsy-oversync/">&larr; §25 Epilepsy: over-synchronisation</a>'
NEXT = '<a rel="next" href="/mind/27-depression-chronification/">§27 Depression &amp; treatment resistance &rarr;</a>'

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
  <a href="{GH}/26-plasticity-consolidation/" rel="noopener">reproduce (GitHub)</a>
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
