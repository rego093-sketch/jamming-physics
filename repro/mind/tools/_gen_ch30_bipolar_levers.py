#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch30_bipolar_levers.py — emit the §30 bipolar threshold-levers chapter (roadmap T2b-L).

Writes docs/mind/30-bipolar-threshold-levers/index.html from the content below, using the same
head/JSON-LD/footer scaffolding as the other Part-II chapters so the SEO markup is byte-
consistent. The answer-first <p class="answer"> and the vp-card asides are NOT written here —
build_search_layer.py injects them from mind_registry.py (single source of truth): this
generator only emits the skeleton (abstract + claim-strip + body sections + nav). Body text is
English-only (VP-SPEC C0).

This chapter INHERITS the threshold-shift intervention logic from the analgesic reproducibility
package (Zenodo 10.5281/zenodo.20733420) and uses it to DECOMPOSE the single abstract barrier-
raising operator that §29's B4 result proved (the mood-stabiliser sign) into a DNA-grounded
three-lever target map. No new mechanism, no new tuned constant; the engine is READ-ONLY. The
numbers quoted in the prose are the structural reads (gamma, |h_sp|) and the burden ranking from
repro/mind/_verify/bipolar_threshold_levers.py and bipolar_burden_prioritisation.py (efficacy=0;
targets ranked, never drugs or doses); the canonical numeric artifacts are those modules'
results.json files.

One-shot authoring helper; the emitted HTML is the canonical artifact.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, os.pardir))
MIND = os.path.join(PKG, "docs", "mind")
DOI = "10.5281/zenodo.20694404"                 # mind paper concept DOI (JSON-LD / footer)
ANALGESIC_DOI = "10.5281/zenodo.20733420"        # inherited threshold-logic technology (cited in body)
ORCID = "0009-0002-7535-8245"
PAPER = "Felt Cognition: Parallel Micro-Eddies, the Stream of Thought, and the Open Problem of Experience"
GH = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/mind"

NO = 30
SLUG = "30-bipolar-threshold-levers"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Bipolar threshold levers: the mood-stabiliser barrier-raise, decomposed"
H1 = "Bipolar threshold levers &mdash; the mood-stabiliser barrier-raise, decomposed into three DNA-grounded levers"
CRUMB = "Bipolar: three threshold levers"
HEADLINE = ("The bipolar mood-stabiliser sign decomposed into a DNA-grounded three-lever target map: "
            "reduce inward excitatory current, increase outward potassium current, or remove the "
            "upstream circadian/HPA drive, over sixteen bipolar excitability genes")
META = ("The previous chapter proved the mood-stabiliser sign is barrier-raising but treated the "
        "stabiliser as one abstract operator. This chapter inherits the threshold-shift intervention "
        "logic (analgesic reproducibility package, Zenodo 10.5281/zenodo.20733420) and decomposes that "
        "operator into three concrete levers -- reduce inward excitatory current (L1), increase outward "
        "potassium current (L2), remove the upstream circadian/HPA drive (L3) -- over sixteen bipolar "
        "genes placed by their own promoter switch stiffness. Targets are ranked, never drugs or doses. "
        "efficacy=0; not medical advice.")

ABSTRACT = (
    "The <a href=\"/mind/29-bipolar-state-switching/\">bipolar chapter</a> closed with a forced sign: a "
    "<strong>mood stabiliser is whatever raises the barrier</strong> between the manic and depressive "
    "poles (result B4). That is correct and direction-only, but it leaves the operator <em>abstract</em> "
    "&mdash; it says <em>raise the barrier</em> without saying <strong>which genes or channels actually "
    "realise the raise</strong>. This chapter fills exactly that gap, and it does so with a piece of "
    "technology built elsewhere and inherited wholesale: the <strong>threshold-shift intervention "
    "logic</strong> from the analgesic reproducibility package "
    "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>). Its core idea "
    "is that a symptom is a <strong>firing-threshold crossing</strong> and an intervention is a "
    "<strong>controlled upward shift of that threshold</strong>, reachable exactly three ways: "
    "<strong>L1</strong> reduce the inward (excitatory) current, <strong>L2</strong> increase the "
    "outward (potassium) current, <strong>L3</strong> remove the up-stream sensitising drive. Applied "
    "to bipolar disorder on the <em>same</em> R19 substrate the whole atlas rests on, the abstract "
    "barrier-raise resolves into a <strong>three-lever target map over sixteen bipolar excitability "
    "genes</strong>: the voltage-gated Ca&sup2;&#8314;/Na&#8314;/NMDA set on L1 (with "
    "<span class=\"mono\">CACNA1C</span> and <span class=\"mono\">ANK3</span>, the two classic GWAS "
    "loci), the <span class=\"mono\">KCNQ</span> / <span class=\"mono\">KCNB</span> potassium set on L2, "
    "and the circadian / HPA set on L3 (with <span class=\"mono\">GSK3B</span>, lithium's "
    "best-characterised molecular target). Each gene is placed by reading its <strong>own promoter "
    "switch stiffness</strong> &mdash; <span class=\"mono\">&gamma; = &minus;mean</span> nearest-"
    "neighbour stacking free energy (SantaLucia 1998) over its promoter window, turned into "
    "<span class=\"mono\">|h_sp| = spinodal(&gamma;)</span> with the frozen engine <strong>read-only</strong>. "
    "Three fail-closed disciplines ride along: every L3 link stays graded <span class=\"mono\">[O]</span> "
    "cited biology, a forbidden-claim scanner rejects any dose / efficacy / safety / synthesis "
    "statement, and a burden-weighted ranking orders <strong>targets, never drugs or doses</strong>. The "
    "<strong>firewall</strong> is absolute: the promoter <span class=\"mono\">|h_sp|</span> is a gene's "
    "own switch stiffness, <strong>never</strong> a channel voltage, a potency, a dose, or a clinical "
    "effect. <span class=\"mono\">efficacy = 0</span>; not medical advice; the hard problem stays open."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("What B4 left abstract", [
        "The <a href=\"/mind/29-bipolar-state-switching/\">previous chapter</a> read bipolar disorder as "
        "two poles on one valence axis and proved five sign-only results. The fourth, B4, is the one this "
        "chapter builds on: the <strong>mood-stabiliser sign is barrier-raising</strong> &mdash; anything "
        "that deepens the well around euthymia raises the threshold to switch, so both manic and "
        "depressive episodes become harder to enter. That result is forced and it is honest, but it "
        "describes the stabiliser as a <em>single abstract operator</em>: <q>raise the barrier.</q> It "
        "does not say <strong>by what physical handle</strong> the barrier is raised &mdash; which "
        "current, which channel, which gene. A mechanism atlas should be able to say more than "
        "<em>something raises the barrier</em>; it should be able to enumerate the <strong>ways</strong> "
        "a barrier can be raised and attach real molecular targets to each. That enumeration is precisely "
        "what the inherited technology supplies.",
    ]),
    sec("The inherited technology: threshold-shift intervention logic", [
        "The handle is not invented here. It is taken intact from the <strong>analgesic reproducibility "
        "package</strong> (<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI +
        "</a>), which built a <strong>threshold-shift intervention logic</strong> for a different "
        "problem (a pain-signalling threshold) and proved it on the voltage-gated sodium channels. Its "
        "premise is general: if a symptom is a <strong>firing-threshold crossing</strong>, then an "
        "intervention is a <strong>controlled upward shift of that threshold</strong>, and a threshold is "
        "set by a balance of currents, so there are exactly <strong>three levers</strong> on it. "
        "<strong>L1</strong> &mdash; <em>reduce the inward, excitatory current</em> that drives the "
        "system toward the crossing. <strong>L2</strong> &mdash; <em>increase the outward, repolarising "
        "current</em> that pulls it back. <strong>L3</strong> &mdash; <em>remove the up-stream "
        "sensitising drive</em> that lowers the threshold in the first place. The same frame applies "
        "unchanged to the bipolar mood switch, because the bipolar chapter and the analgesic package "
        "share the <strong>same R19 substrate</strong> &mdash; the engine's supercritical pitchfork "
        "<span class=\"mono\">&#7779; = g&middot;s &minus; s&sup3; + h</span>, whose spinodal fold IS the "
        "switching barrier. Inheriting the logic means the bipolar barrier-raise of B4 is not one operator "
        "but <strong>three named levers</strong>, and each lever points at a concrete set of genes.",
        "The reuse is literal at the level of code, not just analogy. The analgesic package read each "
        "channel gene's promoter on a fixed pipeline and turned it into a switch stiffness through the "
        "engine's own <span class=\"mono\">spinodal</span> and <span class=\"mono\">barrier</span> "
        "functions; this chapter runs that <em>identical</em> pipeline on the bipolar genes, and two of "
        "the potassium-channel reads (<span class=\"mono\">KCNQ2</span>, "
        "<span class=\"mono\">KCNQ3</span>) are carried over <strong>verbatim from the analgesic "
        "cache</strong> &mdash; the same gene, the same number. Nothing about the engine is touched; the "
        "module re-emerges the frozen tree read-only and confirms it byte-unchanged."
    ]),
    sec("L1 &mdash; reduce the inward excitatory current", [
        "The first lever lowers the drive <em>toward</em> the switch. In bipolar genetics this is the "
        "richest lever, because the disorder's most-replicated common-variant signals sit on "
        "<strong>voltage-gated calcium channels</strong>. <span class=\"mono\">CACNA1C</span> "
        "(Ca<sub>V</sub>1.2) is the single most-replicated bipolar GWAS locus; "
        "<span class=\"mono\">CACNA1D</span> (Ca<sub>V</sub>1.3) and <span class=\"mono\">CACNA1I</span> "
        "(Ca<sub>V</sub>3.3) extend the calcium-channel signal across the cross-disorder analyses; "
        "<span class=\"mono\">SCN2A</span> (Na<sub>V</sub>1.2) carries the voltage-gated sodium side and "
        "<span class=\"mono\">GRIN2A</span> the NMDA-receptor (glutamatergic, calcium-permeable) side. "
        "Two more sit <strong>L1-adjacent</strong>: <span class=\"mono\">CACNB2</span>, the auxiliary "
        "calcium-channel &beta;2 subunit that is itself a cross-disorder GWAS hit, and "
        "<span class=\"mono\">ANK3</span> (ankyrin-G), the second classic bipolar locus, which organises "
        "the sodium channels at the axon initial segment rather than carrying current itself. The mechanism "
        "DIRECTION on this lever is the one the existing mood stabilisers already illustrate: agents that "
        "<em>reduce</em> voltage-gated inward current (the sodium-channel-blocking anticonvulsant "
        "stabilisers are the textbook example) are barrier-raising in the L1 sense. That is a "
        "<strong>direction, never a dose</strong> &mdash; <span class=\"mono\">efficacy = 0</span>.",
    ]),
    sec("L2 &mdash; increase the outward potassium current", [
        "The second lever raises the pull <em>back</em> from the switch by strengthening the outward, "
        "repolarising potassium current. Three channels carry it here: "
        "<span class=\"mono\">KCNQ2</span> and <span class=\"mono\">KCNQ3</span> "
        "(K<sub>V</sub>7.2 / K<sub>V</sub>7.3, the neuronal <strong>M-current</strong> pair that is the "
        "canonical excitability brake), and <span class=\"mono\">KCNB1</span> (K<sub>V</sub>2.1, the "
        "major somatic delayed-rectifier). On the inherited frame, an M-current <em>opener</em> &mdash; "
        "anything that increases this outward current &mdash; is barrier-raising in the L2 sense, the "
        "mirror image of the L1 inward-current reduction. The two KCNQ reads are the genes carried over "
        "verbatim from the analgesic package's potassium set, which is what makes the L1/L2 symmetry exact "
        "rather than approximate: the same channels that brake a pain-signalling threshold brake the mood "
        "switch, read on the same pipeline. Again the claim is a <strong>mechanism direction only</strong>; "
        "no opener, dose, or patient is named.",
    ]),
    sec("L3 &mdash; remove the upstream circadian / HPA drive (the [O] lever)", [
        "The third lever does not touch the channel at all; it removes the <em>up-stream</em> drive that "
        "keeps the threshold low. In bipolar disorder this drive is the one the disorder is most "
        "characteristically tied to: the <strong>circadian clock</strong> and the "
        "<strong>HPA stress axis</strong>. The clock genes <span class=\"mono\">ARNTL</span> (BMAL1), "
        "<span class=\"mono\">CLOCK</span> and <span class=\"mono\">PER2</span> sit here &mdash; the "
        "<em>Clock-&Delta;19</em> mouse shows a mania-like phenotype, and lithium lengthens circadian "
        "period &mdash; alongside the HPA effectors <span class=\"mono\">NR3C1</span> (the glucocorticoid "
        "receptor) and <span class=\"mono\">CRHR1</span> (CRF-receptor-1, at the top of the axis). And "
        "the lever's anchor gene is <span class=\"mono\">GSK3B</span>: <strong>GSK-3&beta; is lithium's "
        "best-characterised molecular target</strong>, sitting where the circadian and mood-stabilising "
        "actions converge. This is the lever that demands the most discipline, and it gets it. Every L3 "
        "link is held at grade <span class=\"mono\">[O]</span> &mdash; <strong>open, cited biology, never "
        "derived from the substrate</strong>. The model does not claim to <em>compute</em> that "
        "GSK-3&beta; or BMAL1 sets the bipolar threshold; it records, as cited upstream biology, that "
        "these are the drives whose removal would raise it. A <strong>fail-closed L3-honesty gate</strong> "
        "enforces exactly this: it checks that the declared L3 set is present, that each member is graded "
        "<span class=\"mono\">[O]</span> and marked not-derived, that no L3 gene is mislabelled as a "
        "current-carrying ion channel, and that the firewall sentence is present &mdash; and it FAILS the "
        "build if any of these slips.",
    ]),
    sec("The DNA grounding: a promoter's own switch stiffness", [
        "What places each of the sixteen genes is not a list but a <strong>read</strong>. For every gene, "
        "the module takes its promoter window (transcription start &minus;2000 to +500 bases, "
        "<em>Homo sapiens</em>) and computes "
        "<span class=\"mono\">&gamma; = &minus;mean</span> of the nearest-neighbour base-stacking free "
        "energies along that window (the SantaLucia 1998 nearest-neighbour thermodynamics), then turns "
        "that <span class=\"mono\">&gamma;</span> into the promoter's switch stiffness through the "
        "<em>frozen engine's own</em> functions: "
        "<span class=\"mono\">|h_sp| = spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></span> and "
        "<span class=\"mono\">barrier = &gamma;&sup2;/4</span>. The reads span a real range &mdash; from "
        "<span class=\"mono\">KCNQ2</span> at <span class=\"mono\">&gamma; &approx; 1.58</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.76</span>, the stiffest promoter in the set) down to "
        "<span class=\"mono\">SCN2A</span> at <span class=\"mono\">&gamma; &approx; 1.20</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.50</span>) &mdash; and they are read on the "
        "<strong>same R19 substrate, with the same engine, that the analgesic package used</strong>, "
        "which is the whole point of the inheritance: one substrate, one pipeline, two problems. The "
        "<span class=\"mono\">&gamma;</span> read is a property of the gene's <strong>promoter "
        "sequence</strong>, and that is <em>all</em> it is.",
    ]),
    sec("Ranking targets, and the firewall that keeps gamma honest", [
        "The last component prioritises, and it prioritises <strong>targets, never drugs or doses</strong>. "
        "A burden-weighted score combines three declared, cited weights &mdash; clinical burden, unmet "
        "need, and genetic-evidence / druggability &mdash; and ranks the genes by that score alone. "
        "<span class=\"mono\">CACNA1C</span> and <span class=\"mono\">ANK3</span> top the list (the two "
        "highest-burden bipolar loci), <span class=\"mono\">GSK3B</span> and the circadian / HPA set "
        "follow. Crucially, the <span class=\"mono\">&gamma;</span> read is carried <em>alongside</em> "
        "each target as structural context but is <strong>never folded into the score</strong> &mdash; "
        "and the result is a clean demonstration of the firewall: the priority ranking and the "
        "<span class=\"mono\">&gamma; / |h_sp|</span> ranking are <strong>decoupled</strong>. "
        "<span class=\"mono\">CACNA1C</span> is the top-priority target yet has nearly the "
        "<em>softest</em> promoter read in the set; <span class=\"mono\">KCNQ2</span> has the stiffest "
        "read yet sits low on priority. If the stiffness drove the ranking, those two could not sit where "
        "they do. That decoupling is the firewall made visible, and it must be stated once more in full: "
        "the promoter <span class=\"mono\">|h_sp|</span> is a gene's <strong>own switch stiffness</strong>, "
        "and it is <strong>never</strong> equated with the network mood-switch barrier "
        "<span class=\"mono\">g</span> of the previous chapter, nor with a channel's activation voltage, a "
        "compound's potency, a dose, an in-vivo selectivity, or any clinical effect. A "
        "<strong>fail-closed forbidden-claim scanner</strong> guards the whole package: it scans the "
        "written results for any dose, efficacy-as-fact, safety-as-fact, or synthesis statement, carries a "
        "negation guard, and includes a planted self-test that <em>must</em> fire &mdash; if it ever "
        "fails to catch its own bait, the build fails. This module is registered as the eighth atlas "
        "citizen (<span class=\"mono\">BIP-T2b-L</span>) and reproduces bit-for-bit with the engine "
        "byte-unchanged.",
        "Everything here is an in-silico <em>reading</em> of promoter sequence and a <em>frame</em> for "
        "organising targets, not a clinical measure, a diagnosis, or a prescription. The model asserts "
        "<em>mechanism directions and target placements</em> &mdash; a barrier can be raised three ways; "
        "these sixteen genes populate the three levers; these targets carry the highest genetic burden "
        "&mdash; and <strong>nothing</strong> about which agent acts on any lever, at what dose, in whom, "
        "whether any real drug raises anyone's barrier, or that anyone should change a treatment. The "
        "mood stabilisers named as <em>directions</em> (the sodium-channel-blocking anticonvulsants on L1, "
        "lithium via GSK-3&beta; / circadian on L3) are illustrations of a <em>sign</em>, never a "
        "recommendation. Real bipolar disorder is heterogeneous and polygenic, and that heterogeneity is "
        "<strong>locked</strong>. A promoter read and a lever assignment are mechanism boundaries, "
        "<strong>not</strong> a claim about the felt quality of a mood state (Axis-A firewall &mdash; "
        "<span class=\"mono\">consciousness_claim = 0</span>, the hard problem stays <strong>open</strong>). "
        "<strong>This is not medical advice, not a diagnosis, not a treatment protocol, and not a cure.</strong> "
        "<span class=\"mono\">medium_efficacy_tested = 0</span>; targets ranked, never drugs or doses."
    ]),
])

PREV = '<a rel="prev" href="/mind/29-bipolar-state-switching/">&larr; §29 Bipolar: two poles on one axis</a>'
NEXT = '<a rel="next" href="/mind/31-epilepsy-threshold-levers/">§31 Epilepsy: three threshold levers &rarr;</a>'

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
  <a href="{GH}/30-bipolar-threshold-levers/" rel="noopener">reproduce (GitHub)</a>
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
