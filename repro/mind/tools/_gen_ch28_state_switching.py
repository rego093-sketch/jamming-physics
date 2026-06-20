#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch28_state_switching.py — emit the §28 state-switching chapter (roadmap E2).

Writes docs/mind/28-state-switching/index.html from the content below, using the same
head/JSON-LD/footer scaffolding as the other Part-II chapters so the SEO markup is byte-
consistent. The answer-first <p class="answer"> and the vp-card asides are NOT written here —
build_search_layer.py injects them from mind_registry.py (single source of truth): this
generator only emits the skeleton (abstract + claim-strip + body sections + nav). Body text
is English-only (VP-SPEC C0). The numbers quoted in the prose are the SIGN/direction results
from repro/mind/_verify/e2_state_switching.py (efficacy=0; sign-only); the canonical numeric
artifact is that module's e2_state_switching_results.json.

This is the LAYER, not an application: it is the R19 bistable cell read OVER TIME. It also
closes the §25 epilepsy ictal time-course that was explicitly OWED to E2.

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

NO = 28
SLUG = "28-state-switching"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "The state-switching layer: hysteresis, the fold, &amp; the ictal time-course"
H1 = "The state-switching layer &mdash; the R19 bistable cell read over time"
CRUMB = "State-switching: hysteresis &amp; the fold"
HEADLINE = ("The state-switching layer: the R19 bistable cell read over time -- hysteresis, a "
            "transition latency that diverges at the fold, and the barrier that sets the switching "
            "threshold")
META = ("The state-switching layer the temporal atlas needs: the R19 bistable cell read OVER TIME. "
        "Hysteresis gives a finite loop width of twice the spinodal; the transition latency diverges "
        "at the fold (critical slowing) -- which closes the epilepsy ictal time-course owed to this "
        "layer; and the barrier sets the switching threshold. g=1 universal scale, fold taken from "
        "the engine, constant-drive integration reproduces the engine settle bit-for-bit. The layer "
        "the mood-cycle disorders stand on. efficacy=0; not medical advice.")

ABSTRACT = (
    "The <a href=\"/mind/26-plasticity-consolidation/\">plasticity layer</a> gave the atlas a "
    "<em>slow</em> structural variable &mdash; a connectome that changes with use. It did not give "
    "the atlas a <em>fast</em> one: a state that can <strong>switch</strong> and <strong>stay "
    "switched</strong> until pushed back. Yet that bistable switch has been in the engine from the "
    "start &mdash; the <strong>R19 cell</strong>, "
    "<span class=\"mono\">s&#775; = g&middot;s &minus; s&sup3; + h</span>, the pitchfork whose two "
    "stable branches the whole framework rests on. Every earlier chapter read it at a single instant. "
    "This chapter reads it <strong>over time</strong>, and that is the entire layer: no new equation, "
    "no new constant, just the dynamics of the cell already there. Four sign-only results, each over a "
    "swept stimulus (anti-tuning). <strong>Hysteresis</strong>: sweeping the field up then down, the "
    "up- and down-transitions sit on opposite sides of zero, a finite loop of width "
    "<span class=\"mono\">2&times;spinodal &asymp; 0.77</span> &mdash; a state, once switched, resists "
    "switching back. <strong>The ictal time-course</strong>: the transition latency <em>diverges</em> "
    "as the drive approaches the fold (critical slowing) and falls monotonically as it overshoots &mdash; "
    "which <strong>closes the open ictal time-course the <a href=\"/mind/25-epilepsy-oversync/\">epilepsy "
    "chapter</a> explicitly owed to this layer</strong>. <strong>The barrier</strong>: the spinodal rises "
    "monotonically with the well depth <span class=\"mono\">g</span>, so the same handle that sets the "
    "barrier sets the <em>switching threshold</em> &mdash; shallow wells flip under a fixed drive, deep "
    "wells hold. And the <strong>guard</strong>: constant-drive integration reproduces the engine's own "
    "<span class=\"mono\">settle</span> <strong>bit-for-bit</strong>, with the fold read from the engine, "
    "so the layer adds without altering. The layer, not an application: bipolar (episode switching), the "
    "ictal onset, and the cycle disorders that use it are owed to the modules that import it. "
    "<span class=\"mono\">efficacy = 0</span>."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("The fast variable the atlas was missing", [
        "Two kinds of change matter for a temporal disorder, and the atlas so far had only one. The "
        "<a href=\"/mind/26-plasticity-consolidation/\">plasticity layer</a> supplied the <em>slow</em> "
        "one &mdash; a connectome that consolidates, that writes a state into structure and keeps it. "
        "What it did not supply is the <em>fast</em> one: an operating point that <strong>jumps</strong> "
        "between two stable values and <strong>holds</strong> the new one until something pushes it "
        "back. A mood episode is exactly that &mdash; not a slow drift but a switch into a regime that "
        "persists, then a switch out. To represent it you need a bistable state read as a dynamical "
        "process, not as a snapshot.",
        "The remarkable thing is that this switch needs no new machinery at all. The "
        "<strong>R19 cell</strong> &mdash; <span class=\"mono\">s&#775; = g&middot;s &minus; s&sup3; + "
        "h</span>, the supercritical pitchfork that the entire VP framework is built on &mdash; is a "
        "bistable element. For <span class=\"mono\">g &gt; 0</span> it has two stable branches separated "
        "by a barrier, and a field <span class=\"mono\">h</span> that tilts between them. Every chapter "
        "up to here evaluated that cell at a single instant: <span class=\"mono\">settle</span> to the "
        "branch the field selects, read the value, move on. This chapter does one thing differently. It "
        "watches the cell <em>cross</em> &mdash; sweeps the field, times the transitions &mdash; and the "
        "switching layer falls out of the dynamics that were always there. No new equation. No free "
        "constant. The universal R19 scale <span class=\"mono\">g = 1</span>, and the fold taken from "
        "the engine's own <span class=\"mono\">spinodal(g)</span>.",
    ]),
    sec("Hysteresis: a state that resists switching back (E2.1)", [
        "Sweep the tilting field slowly upward from a state resting on the lower branch. The state does "
        "<em>not</em> jump as soon as the field turns positive; it clings to the lower branch until the "
        "field reaches the <strong>upper fold</strong>, then snaps up. Now sweep back down: the state "
        "clings to the <em>upper</em> branch past zero, until the field reaches the <strong>lower "
        "fold</strong>, then snaps down. The up-transition and the down-transition sit on "
        "<strong>opposite sides of zero</strong> (here at <span class=\"mono\">h = +0.39</span> and "
        "<span class=\"mono\">h = &minus;0.39</span> on the sweep grid), enclosing a "
        "<strong>hysteresis loop</strong> of finite width "
        "<span class=\"mono\">&asymp; 2&times;spinodal = 0.77</span>. The width is not fit &mdash; it is "
        "<em>predicted</em> as twice the engine's fold, and the measured loop matches to within the "
        "sweep step. The meaning is the property a mood episode needs: a state that has switched "
        "<strong>resists switching back</strong>. Removing the push that caused the episode does not "
        "end it; the field must reverse past the opposite fold. That asymmetry &mdash; easy to enter at "
        "one fold, only leaving at the other &mdash; is the signature of bistability over time, and it "
        "is here with no parameter added.",
    ]),
    sec("The ictal time-course, closing the debt to §25 (E2.2)", [
        "The <a href=\"/mind/25-epilepsy-oversync/\">epilepsy chapter</a> placed the seizure at the "
        "over-synchronisation pole and showed the static structure of an ictal state, but it left one "
        "thing explicitly <strong>owed</strong>: the <em>time-course</em> of the transition into ictus "
        "&mdash; why onset can be abrupt yet preceded by a slowing &mdash; because the static engine had "
        "no switching dynamics to express it. This layer pays that debt. Drive the cell toward the fold "
        "and time how long the transition takes. As the drive approaches the fold from below the "
        "transition latency <strong>diverges</strong>: right at the fold the barrier between branches "
        "vanishes and the state creeps through an arbitrarily flat landscape &mdash; "
        "<strong>critical slowing</strong>. Push the drive <em>past</em> the fold and the latency falls "
        "monotonically (here from <span class=\"mono\">73.4</span> just over threshold down to "
        "<span class=\"mono\">1.36</span> at strong overshoot). A small overshoot gives a long, slow "
        "approach; a large overshoot gives a sharp jump. That is the qualitative ictal time-course &mdash; "
        "a slowing as the system rides the edge, an abrupt transition once it tips &mdash; emerging from "
        "the same fold the epilepsy chapter used for the spatial picture. <strong>The §25 ictal "
        "time-course is closed.</strong> It is a mechanism direction, not a clinical timing and not a "
        "prediction about any patient's seizure: <span class=\"mono\">efficacy = 0</span>.",
    ]),
    sec("The barrier is the switching threshold (E2.3)", [
        "What decides whether a given push actually flips the state? The <strong>barrier</strong> between "
        "the two branches, and the engine already sets it: the fold "
        "<span class=\"mono\">spinodal(g) = 2(g/3)<sup>3/2</sup></span> rises monotonically with the well "
        "depth <span class=\"mono\">g</span> (here <span class=\"mono\">0.18</span> at "
        "<span class=\"mono\">g=0.6</span> climbing to <span class=\"mono\">0.64</span> at "
        "<span class=\"mono\">g=1.4</span>). A <strong>shallow</strong> well (small barrier) flips under a "
        "fixed drive; a <strong>deep</strong> well (large barrier) holds against the same drive. The "
        "<em>same</em> handle that sets the barrier therefore sets the <strong>switching threshold</strong> "
        "&mdash; one parameter, two faces. This is the lever the disorder modules need in both directions. "
        "A state that switches <em>too easily</em> is a barrier set too low (episodes triggered by small "
        "perturbations); a state that <em>cannot be moved</em> is a barrier set too high. And it gives the "
        "sign of a stabiliser without ever asserting a dose: anything that <em>raises</em> the barrier "
        "<em>raises</em> the threshold to switch, so episodes become harder to enter. The numeric depths "
        "are sweep probes, not tuned constants &mdash; the result is the monotone <em>direction</em>, "
        "which holds across the whole sweep.",
    ]),
    sec("A pure add-on, and what it unlocks (E2.4)", [
        "The guard makes the discipline operational, exactly as in the plasticity layer. Held at a "
        "constant drive, the time-integration of the cell reproduces the engine's own "
        "<span class=\"mono\">settle</span> routine <strong>bit-for-bit</strong>, and the fold used "
        "throughout is read from the engine's <span class=\"mono\">spinodal</span>, not hand-set. Turning "
        "the sweep off recovers the frozen engine <em>exactly</em>: the engine file stays "
        "<span class=\"mono\">e61083ae&hellip;</span>, the emergence tree stays "
        "<span class=\"mono\">0fbf4988&hellip;</span>, byte-unchanged. <strong>E2 adds; it does not "
        "alter.</strong>",
        "And it is a layer, not a disorder. Its purpose is to be the fast counterpart to the plasticity "
        "layer &mdash; the substrate the <em>switching</em> conditions stand on. Bipolar as two operating "
        "poles with episodes that are bistable transitions, the ictal <em>onset</em> as a fold crossing, "
        "the cycle disorders as repeated switching &mdash; each needs a state that can jump and hold. E2 "
        "supplies that state once, as a reusable object built from the R19 cell already in the engine; the "
        "mood and cycle modules that follow <em>import</em> it rather than re-deriving it, and pair it with "
        "the plasticity layer (the slow trace) to get episodes that both switch and leave a mark. "
        "Everything here is an in-silico coupling state, not a clinical measure. A bistable transition is a "
        "<strong>mechanism boundary, not a claim about the felt quality of a mood state</strong> (Axis-A "
        "firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>; the hard problem of "
        "experience stays <strong>open</strong>). This is a mechanism-level result about state-switching "
        "<em>as represented in the VP framework</em> &mdash; not medical advice, not a diagnosis, not a "
        "treatment protocol, and not a cure. <span class=\"mono\">efficacy = 0</span>; the hard problem "
        "stays open.",
    ]),
])

PREV = '<a rel="prev" href="/mind/27-depression-chronification/">&larr; §27 Depression &amp; treatment resistance</a>'
NEXT = '<a rel="next" href="/mind/29-bipolar-state-switching/">§29 Bipolar disorder &rarr;</a>'

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
  <a href="{GH}/28-state-switching/" rel="noopener">reproduce (GitHub)</a>
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
