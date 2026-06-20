#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch27_depression.py — emit the §27 depression / TRD chapter (roadmap T1b).

Writes docs/mind/27-depression-chronification/index.html from the content below, using the
same head/JSON-LD/footer scaffolding as the other Part-II chapters so the SEO markup is
byte-consistent. The answer-first <p class="answer"> and the vp-card asides are NOT written
here — build_search_layer.py injects them from mind_registry.py (single source of truth):
this generator only emits the skeleton (abstract + claim-strip + body sections + nav). Body
text is English-only (VP-SPEC C0). The numbers quoted in the prose are the SIGN/direction
results from repro/mind/_verify/depression_chronification.py (efficacy=0; sign-only); the
canonical numeric artifact is that module's depression_chronification_results.json.

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

NO = 27
SLUG = "27-depression-chronification"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Depression &amp; TRD: the chronification of a low-coordination operating point"
H1 = "Depression and treatment resistance &mdash; the chronification of a low-coordination operating point"
CRUMB = "Depression: chronification &amp; TRD"
HEADLINE = ("Depression as the chronification of a low-coordination operating point: an HPA-driven "
            "withdrawal that the plasticity layer writes into the connectome")
META = ("Major depression read as the chronification of a low-coordination operating point. A sustained "
        "HPA / stress-driven withdrawal bias lowers the global order parameter below health (acute, "
        "reversible); under the plasticity layer the excursion writes a retained structural trace -- the "
        "reversible-to-chronified switch. Antidepressant delayed onset is a consolidation timescale, and "
        "treatment resistance is the depth of the chronified trace. The first temporal disorder, built on "
        "top of E0. efficacy=0; not medical advice.")

ABSTRACT = (
    "The structural atlas placed conditions on the ignition / synchrony axis: autism-T "
    "<a href=\"/mind/18-autism-three-axis/\">under-ignites</a>, schizophrenia "
    "<a href=\"/mind/24-schizophrenia-mirror/\">over-ignites</a>, epilepsy "
    "<a href=\"/mind/25-epilepsy-oversync/\">over-synchronises</a>. Depression sits lower on the same "
    "coupling axis <em>and</em> on the new <strong>temporal</strong> axis the "
    "<a href=\"/mind/26-plasticity-consolidation/\">plasticity layer</a> opened, and it is the first "
    "disorder to <em>use</em> that layer rather than build it. The handle is the engine's own "
    "<strong>HPA / stress axis</strong> (the M18 cortisol cascade and the M17 valence geometry, where "
    "cortisol sits on the withdrawal pole), mapped &mdash; with <strong>no new constant</strong> &mdash; to a "
    "sustained <strong>withdrawal bias</strong> through the same coupling map the schizophrenia and "
    "epilepsy modules use. Four sign-only results follow, all holding over a rate sweep. A sustained "
    "withdrawal lowers the global order parameter <strong>below health</strong> &mdash; the acute, "
    "reactive depressed operating point, fully reversible on the static substrate. <strong>With</strong> "
    "plasticity the same excursion writes a <strong>retained structural trace</strong> that does not "
    "revert when the stressor lifts: the <strong>reversible&rarr;chronified switch</strong>, now driven by "
    "the HPA handle, deepening with exposure. Antidepressant <strong>delayed onset</strong> is the slow, "
    "cumulative accumulation of restoring structural movement &mdash; a <em>consolidation timescale</em>, "
    "not a pharmacokinetic delay. And <strong>treatment resistance</strong> is the <em>depth</em> of the "
    "chronified trace: at a fixed restoring budget a deeper trace is proportionally less reachable. The "
    "module <strong>imports</strong> the plasticity layer rather than re-deriving it, adds no tuned "
    "constant, and with the rate and stress off reproduces the frozen engine bit-for-bit. "
    "<span class=\"mono\">efficacy = 0</span>; not medical advice; the hard problem stays open."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("Depression on the coupling axis &mdash; and the temporal axis E0 opened", [
        "Every disorder in the atlas so far has been a fault on the ignition / synchrony axis, read off "
        "a <em>static</em> operating point. Depression does not fit there. Its core electrophysiological "
        "signature is, in direction, a <em>reduction</em> in large-scale functional coordination &mdash; a "
        "<em>hypo</em>-coupled state, not an over-ignited or over-synchronised one &mdash; and its defining "
        "clinical feature is not a momentary state at all but a state that <em>persists</em>: a low mood "
        "that has stopped lifting. Those two facts place depression on two axes at once: the lower part of "
        "the coupling axis, and the <strong>temporal</strong> axis the plasticity layer opened. That is "
        "why depression is the first disorder built <em>on top of</em> E0 rather than alongside it: it "
        "<strong>imports</strong> the plasticity layer (the reusable <span class=\"mono\">PlasticConnectome</span>) "
        "and drives it; it does not re-derive the rule.",
    ]),
    sec("The HPA handle: chronic stress as a withdrawal bias (grounded, not invented)", [
        "The driver is not a free knob. The engine already emerged the stress axis. The "
        "<a href=\"/mind/17-faculties-of-mind/\">global-state layer</a> places cortisol on the "
        "<em>avoid / withdrawal</em> pole of the valence axis (valence is approach[dopamine] minus "
        "avoid[cortisol]); the interoceptive layer emerges the <strong>HPA cortisol cascade</strong> "
        "&mdash; the PVN/SIM1 hub through ACTH to cortisol, with the cortisol peak landing in the cited "
        "15&ndash;40&nbsp;minute window and glucocorticoid negative feedback in place. Chronic HPA drive "
        "&mdash; a sustained, dysregulated stress signal &mdash; is mapped to a sustained "
        "<strong>withdrawal bias</strong> <span class=\"mono\">b&nbsp;&lt;&nbsp;0</span>, which <em>lowers</em> "
        "the effective ephaptic coupling exactly as an inhibitory bias does in the schizophrenia and "
        "epilepsy maps, <span class=\"mono\">k = &kappa;/(1+|b|)</span>. Only the <strong>sign</strong> of "
        "that mapping is asserted &mdash; chronic stress &rarr; withdrawal &rarr; hypo-coordination, the "
        "direction the M17 valence geometry already fixes; the <em>magnitude</em> of the stress-to-bias "
        "gain is <span class=\"mono\">[O]</span> (representative), and every sign below is required to hold "
        "over a sweep. The HPA kinetics themselves are <strong>cited</strong> from M18. "
        "<strong>No new constant enters.</strong>",
    ]),
    sec("The acute depressed operating point (D1)", [
        "Start with the static substrate, no plasticity. Apply the sustained withdrawal (chronic-stress) "
        "bias and read the global order parameter. It sits <strong>below health</strong>: every withdrawal "
        "level lowers coordination beneath the healthy anchor (<span class=\"mono\">R&nbsp;=&nbsp;0.390</span>), "
        "and a deeper withdrawal lowers it further &mdash; a severe withdrawal reaches "
        "<span class=\"mono\">R&nbsp;&asymp;&nbsp;0.331</span>, well under a mild one. This is the acute, "
        "<em>reactive</em> depressed operating point: a hypo-coordinated state, the mechanistic direction "
        "of the reduced large-scale connectivity reported in depression. On this static substrate the "
        "excursion is <strong>fully reversible</strong> &mdash; remove the stressor and coordination "
        "returns. What turns a reactive dip into a chronic illness is the next layer.",
    ]),
    sec("Chronification: the reversible&rarr;chronified switch on the stress handle (D2)", [
        "This is the distinguishing result, and it is the plasticity layer's reversible&rarr;chronified "
        "switch driven by the HPA handle. Run the same sustained withdrawal, now under plasticity, then "
        "remove the stressor. <strong>Without</strong> plasticity "
        "(<span class=\"mono\">&eta;&nbsp;=&nbsp;0</span>) the excursion reverts <em>exactly</em> to baseline "
        "&mdash; a <em>reactive</em> low mood that lifts when the stressor ends. <strong>With</strong> "
        "plasticity (<span class=\"mono\">&eta;&nbsp;&gt;&nbsp;0</span>) the same excursion leaves a "
        "<strong>retained structural trace</strong> that does <em>not</em> revert when the stressor is "
        "removed &mdash; the structural substrate of <em>chronic</em> depression &mdash; and that trace "
        "<strong>deepens monotonically with exposure</strong> "
        "(<span class=\"mono\">&#8741;&Delta;W&#8741;</span> grows 0.075 &rarr; 0.151 &rarr; 0.227 &rarr; 0.338 "
        "as the stress is sustained longer), a kindling-direction sign that holds across the rate sweep. "
        "Two cautions are part of the result. First, the robust, sign-stable signal is the retained "
        "<em>structural</em> trace <span class=\"mono\">&#8741;&Delta;W&#8741;</span>; the post-removal "
        "<em>coordination</em> R is <strong>not</strong> asserted to sit below baseline (phase-correlation "
        "Hebb consolidates the surviving in-phase structure, so R can tick up) &mdash; it is reported, not "
        "claimed. The persistent object is the trace. Second, the Axis-A firewall: a retained structural "
        "trace is a <strong>mechanism boundary, not a claim about the felt quality of chronic low mood</strong> "
        "(<span class=\"mono\">consciousness_claim = 0</span>; the hard problem stays open).",
    ]),
    sec("Antidepressant delayed onset as a consolidation timescale (D3)", [
        "Antidepressants characteristically take <em>weeks</em> to reach clinical effect &mdash; a delay "
        "classically tied to slow downstream / plasticity changes rather than the immediate monoamine "
        "shift. The layer reproduces that delay as a <em>timescale</em>, not a pharmacokinetic lag. Build "
        "the chronified substrate, then apply a coordination-restoring (antidepressant-class) push. The "
        "restoring structural movement <span class=\"mono\">&#8741;W<sub>k</sub>&minus;W<sub>dep</sub>&#8741;</span> "
        "accumulates <strong>monotonically over epochs</strong> and is <strong>small after a single epoch</strong> "
        "(0.018 after one, 0.138 after eight): the effect builds over a consolidation timescale, not "
        "instantly. Its <em>direction</em> is therapeutic &mdash; coordination R after the full course "
        "exceeds the chronified R &mdash; and that sign holds over a rate&times;strength sweep. It is a "
        "direction and a timescale, not a dose and not an efficacy: <span class=\"mono\">efficacy = 0</span>.",
    ]),
    sec("Treatment resistance is the depth of the trace (D4) &mdash; and the firewall", [
        "Treatment-resistant depression has the cleanest structural reading of all. Resistance is the "
        "<strong>depth</strong> of the chronified trace. At a <em>fixed</em> restoring budget, the "
        "<strong>fraction</strong> of the depressive structural trace an antidepressant-class push "
        "neutralises <strong>decreases as the trace deepens</strong>: a deeper, longer-consolidated "
        "chronification is proportionally <em>less reachable</em> at the same budget, leaving a larger "
        "residual &mdash; the same fixed budget that nearly clears a shallow trace clears only a fraction "
        "of a deep one. The ordering holds across a rate&times;budget sweep. This is the mechanism-level "
        "picture of why a longer, deeper depression is harder to move at fixed effort.",
        "It must be said exactly what this chapter is and is not. Every quantity is an in-silico "
        "<em>coupling state</em>, not a clinical measure, a diagnosis, or a prescription. The model "
        "asserts <em>mechanism directions</em> &mdash; a sustained HPA-driven withdrawal lowers "
        "coordination; with plasticity it chronifies; restoration is slow and depth-limited &mdash; and "
        "<strong>nothing</strong> about which depression any individual has, whether any drug treats "
        "theirs, or that anyone should change a treatment. <span class=\"mono\">medium_efficacy_tested = 0</span> "
        "everywhere; real depression is heterogeneous (melancholic, atypical, psychotic, peripartum, "
        "seasonal, bipolar, with monoaminergic, HPA, inflammatory, circadian and psychosocial "
        "contributors) and that heterogeneity is <strong>locked</strong>; a retained structural trace is a "
        "mechanism boundary, <strong>not</strong> a claim about the felt quality of depression (Axis-A "
        "firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>, the hard problem of experience "
        "stays <strong>open</strong>). Bipolar depression, which adds episode <em>switching</em>, needs "
        "the state-switching layer (E2) and the two poles that follow in &sect;28&ndash;&sect;29; addiction "
        "needs sensitisation and remains owed. "
        "<strong>This is not medical advice, not a diagnosis, not a treatment protocol, and not a cure.</strong> "
        "<span class=\"mono\">efficacy = 0</span>.",
    ]),
])

PREV = '<a rel="prev" href="/mind/26-plasticity-consolidation/">&larr; §26 The plasticity layer</a>'
NEXT = '<a rel="next" href="/mind/28-state-switching/">§28 The state-switching layer &rarr;</a>'

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
  <a href="{GH}/27-depression-chronification/" rel="noopener">reproduce (GitHub)</a>
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
