#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch31_epilepsy_levers.py — emit the §31 epilepsy threshold-levers chapter (roadmap T2a-L).

Writes docs/mind/31-epilepsy-threshold-levers/index.html using the same head/JSON-LD/footer
scaffolding as the other Part-II chapters so the SEO markup is byte-consistent. The answer-first
<p class="answer"> and the vp-card asides are NOT written here — build_search_layer.py injects them
from mind_registry.py (single source of truth): this generator only emits the skeleton (abstract +
claim-strip + body sections + nav). Body text is English-only (VP-SPEC C0).

This chapter applies the SAME threshold-shift intervention logic that §30 (bipolar T2b-L) used,
inherited from the analgesic reproducibility package (Zenodo 10.5281/zenodo.20733420), to the
over-synchronisation pole that §25 (T2a) established. §25 proved seizures are the network crossing
the over-sync threshold on the global order parameter R, but the corrective push ("raise the
over-sync threshold") was ONE abstract operator; this chapter decomposes it into a DNA-grounded
three-lever target map over sixteen epilepsy excitability genes. Five promoter reads
(KCNQ2/KCNQ3/KCNB1/SCN2A/GRIN2A) are carried over VERBATIM from the bipolar promoter cache (gamma
is strand-symmetric). No new mechanism, no new tuned constant; the engine is READ-ONLY. The numbers
quoted in the prose are the structural reads (gamma, |h_sp|) and the burden ranking from
repro/mind/_verify/epilepsy_threshold_levers.py and epilepsy_burden_prioritisation.py (efficacy=0;
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

NO = 31
SLUG = "31-epilepsy-threshold-levers"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Epilepsy threshold levers: the over-sync threshold-raise, decomposed"
H1 = "Epilepsy threshold levers &mdash; the over-synchronisation threshold-raise, decomposed into three DNA-grounded levers"
CRUMB = "Epilepsy: three threshold levers"
HEADLINE = ("The epilepsy over-synchronisation threshold-raise decomposed into a DNA-grounded three-lever "
            "target map: reduce inward sodium/calcium/NMDA current, increase outward potassium current, or "
            "remove the upstream mTOR drive, over sixteen epilepsy excitability genes")
META = ("Chapter 25 proved seizures are the network crossing an over-synchronisation threshold but treated "
        "the corrective raise as one abstract operator. This chapter applies the same threshold-shift "
        "intervention logic used for bipolar disorder (and inherited from the analgesic reproducibility "
        "package, Zenodo 10.5281/zenodo.20733420) and decomposes that raise into three concrete levers -- "
        "reduce inward excitatory current (L1), increase outward potassium current (L2, the dominant lever "
        "here), remove the upstream mTOR drive (L3) -- over sixteen epilepsy genes placed by their own "
        "promoter switch stiffness. Targets are ranked, never drugs or doses. efficacy=0; not medical advice.")

ABSTRACT = (
    "The <a href=\"/mind/25-epilepsy-oversync/\">epilepsy chapter</a> read a seizure as the network "
    "crossing an <strong>over-synchronisation threshold</strong> on the global order parameter "
    "<span class=\"mono\">R</span>: when coupling pushes the population past a critical point, the "
    "micro-eddies that normally run in parallel lock into one runaway rhythm. That chapter proved the "
    "<em>pole</em> and the corrective <em>sign</em> &mdash; the therapeutic push is whatever <strong>raises "
    "the over-sync threshold</strong> &mdash; but it left that push <em>abstract</em>: it said <em>raise the "
    "threshold</em> without saying <strong>which genes or channels actually realise the raise</strong>. This "
    "chapter fills exactly that gap, with the <strong>same piece of inherited technology</strong> that the "
    "<a href=\"/mind/30-bipolar-threshold-levers/\">bipolar levers chapter</a> used: the "
    "<strong>threshold-shift intervention logic</strong> from the analgesic reproducibility package "
    "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>). Its premise is "
    "that a symptom is a <strong>firing-threshold crossing</strong> and an intervention is a "
    "<strong>controlled upward shift of that threshold</strong>, reachable exactly three ways: "
    "<strong>L1</strong> reduce the inward (excitatory) current, <strong>L2</strong> increase the outward "
    "(potassium) current, <strong>L3</strong> remove the up-stream sensitising drive. Applied to epilepsy on "
    "the <em>same</em> R19 substrate the whole atlas rests on, the abstract threshold-raise resolves into a "
    "<strong>three-lever target map over sixteen epilepsy excitability genes</strong>: the voltage-gated "
    "Na&#8314;/Ca&sup2;&#8314;/NMDA set on L1 (<span class=\"mono\">SCN1A</span>, "
    "<span class=\"mono\">SCN2A</span>, <span class=\"mono\">SCN8A</span>, "
    "<span class=\"mono\">CACNA1A</span>, <span class=\"mono\">CACNA1H</span>, "
    "<span class=\"mono\">GRIN2A</span>), the <span class=\"mono\">KCNQ</span> / "
    "<span class=\"mono\">KCNB</span> / <span class=\"mono\">KCNA</span> / <span class=\"mono\">KCNT</span> "
    "potassium set on <strong>L2 &mdash; the dominant lever here</strong>, because the "
    "<span class=\"mono\">KCNQ2</span> / <span class=\"mono\">KCNQ3</span> M-current is the textbook "
    "anticonvulsant axis (the retigabine target) &mdash; with the inhibitory GABA&#8209;A pair "
    "<span class=\"mono\">GABRG2</span> / <span class=\"mono\">GABRA1</span> riding L2-adjacent, and the "
    "mTOR set on L3 (<span class=\"mono\">DEPDC5</span>, <span class=\"mono\">TSC1</span>, "
    "<span class=\"mono\">TSC2</span>). Each gene is placed by reading its <strong>own promoter switch "
    "stiffness</strong> &mdash; <span class=\"mono\">&gamma; = &minus;mean</span> nearest-neighbour stacking "
    "free energy (SantaLucia 1998) over its promoter window, turned into "
    "<span class=\"mono\">|h_sp| = spinodal(&gamma;)</span> with the frozen engine "
    "<strong>read-only</strong>, and five of the reads (<span class=\"mono\">KCNQ2</span>, "
    "<span class=\"mono\">KCNQ3</span>, <span class=\"mono\">KCNB1</span>, <span class=\"mono\">SCN2A</span>, "
    "<span class=\"mono\">GRIN2A</span>) are carried over <strong>verbatim from the bipolar cache</strong>. "
    "Two honest caveats are recorded, not hidden: <span class=\"mono\">KCNT1</span> is "
    "<strong>sign-inverted</strong> (its gain-of-function is the pathology), and the L1 sodium-block "
    "direction is <strong>contraindicated</strong> in Dravet / <span class=\"mono\">SCN1A</span> "
    "loss-of-function. Three fail-closed disciplines ride along: every L3 link stays graded "
    "<span class=\"mono\">[O]</span> cited biology, a forbidden-claim scanner rejects any dose / efficacy / "
    "safety / synthesis statement (including seizure-freedom language), and a burden-weighted ranking orders "
    "<strong>targets, never drugs or doses</strong>. The <strong>firewall</strong> is absolute: the promoter "
    "<span class=\"mono\">|h_sp|</span> is a gene's own switch stiffness, <strong>never</strong> the §25 "
    "network over-sync threshold on <span class=\"mono\">R</span>, a channel voltage, a potency, a dose, or a "
    "clinical effect. <span class=\"mono\">efficacy = 0</span>; not medical advice; the hard problem stays open."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("What §25 left abstract", [
        "The <a href=\"/mind/25-epilepsy-oversync/\">epilepsy chapter</a> placed the disorder at the "
        "<strong>over-synchronisation pole</strong> of the atlas: health is a population of micro-eddies "
        "running in <em>parallel</em> at a moderate global coherence, and a seizure is that population "
        "crossing a <strong>critical coupling threshold</strong> into one runaway, fully phase-locked "
        "rhythm &mdash; the order parameter <span class=\"mono\">R</span> climbing above the band health "
        "lives in. That chapter proved two things and stopped: the <em>pole</em> (epilepsy is "
        "over-synchronisation, the mirror of the under-coordination disorders) and the corrective "
        "<em>sign</em> (the therapeutic push is whatever <strong>raises the over-sync threshold</strong>, "
        "so the network has farther to travel before it locks). That sign is forced and honest, but it "
        "describes the intervention as a <em>single abstract operator</em>: <q>raise the threshold.</q> It "
        "does not say <strong>by what physical handle</strong> the threshold is raised &mdash; which "
        "current, which channel, which gene. A mechanism atlas should be able to say more than "
        "<em>something raises the threshold</em>; it should enumerate the <strong>ways</strong> a threshold "
        "can be raised and attach real molecular targets to each. The bipolar chapter showed that this "
        "enumeration is exactly what the inherited threshold-shift technology supplies &mdash; and epilepsy "
        "is where that technology fits most naturally of all, because the over-sync threshold is "
        "<em>literally</em> an excitability threshold."
    ]),
    sec("The inherited technology, applied a second time", [
        "The handle is not invented here, and it is not even adapted here &mdash; it is the <em>same</em> "
        "logic the <a href=\"/mind/30-bipolar-threshold-levers/\">previous chapter</a> inherited from the "
        "<strong>analgesic reproducibility package</strong> "
        "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>), now turned "
        "on a third problem. Its premise is general: if a symptom is a <strong>firing-threshold "
        "crossing</strong>, then an intervention is a <strong>controlled upward shift of that "
        "threshold</strong>, and a threshold is set by a balance of currents, so there are exactly "
        "<strong>three levers</strong> on it. <strong>L1</strong> &mdash; <em>reduce the inward, excitatory "
        "current</em> that drives the system toward the crossing. <strong>L2</strong> &mdash; "
        "<em>increase the outward, repolarising current</em> that pulls it back. <strong>L3</strong> "
        "&mdash; <em>remove the up-stream sensitising drive</em> that lowers the threshold in the first "
        "place. The frame applies unchanged because the epilepsy chapter, the bipolar chapter, and the "
        "analgesic package all share the <strong>same R19 substrate</strong> &mdash; the engine's "
        "supercritical pitchfork <span class=\"mono\">&#7779; = g&middot;s &minus; s&sup3; + h</span>, whose "
        "spinodal fold IS the switching barrier. There is, however, one difference of <em>emphasis</em> "
        "that epilepsy makes vivid: of the three levers, <strong>L2 is the dominant one here</strong>. The "
        "single most mechanistically transparent anticonvulsant principle &mdash; opening the neuronal "
        "M-current to brake excitability &mdash; is an L2 move, and it has a named molecular precedent in "
        "the <span class=\"mono\">KCNQ2</span>/<span class=\"mono\">KCNQ3</span> channels. Where bipolar "
        "disorder leaned on L1 (its replicated GWAS loci are calcium channels), epilepsy leans on L2.",
        "The reuse is literal at the level of code, not just analogy. The pipeline reads each gene's "
        "promoter on a fixed window and turns it into a switch stiffness through the engine's own "
        "<span class=\"mono\">spinodal</span> and <span class=\"mono\">barrier</span> functions; this "
        "chapter runs that <em>identical</em> pipeline on the epilepsy genes, and <strong>five</strong> of "
        "the reads &mdash; <span class=\"mono\">KCNQ2</span>, <span class=\"mono\">KCNQ3</span>, "
        "<span class=\"mono\">KCNB1</span>, <span class=\"mono\">SCN2A</span>, "
        "<span class=\"mono\">GRIN2A</span> &mdash; are carried over <strong>verbatim from the bipolar "
        "promoter cache</strong>: the same gene, the same promoter window, the same number, because "
        "<span class=\"mono\">&gamma;</span> is a strand-symmetric property of the sequence and does not "
        "change between problems. Nothing about the engine is touched; the module re-emerges the frozen "
        "tree read-only and confirms it byte-unchanged, and registers as the <strong>ninth atlas "
        "citizen</strong> (<span class=\"mono\">EPI-T2a-L</span>)."
    ]),
    sec("L1 &mdash; reduce the inward sodium / calcium / NMDA current", [
        "The first lever lowers the drive <em>toward</em> the over-sync crossing. Epilepsy genetics "
        "populates it densely, because the monogenic epilepsies are dominated by "
        "<strong>voltage-gated ion-channel</strong> defects. Three sodium channels sit here: "
        "<span class=\"mono\">SCN1A</span> (Na<sub>V</sub>1.1, the most-replicated monogenic epilepsy gene, "
        "central to Dravet syndrome), <span class=\"mono\">SCN2A</span> (Na<sub>V</sub>1.2) and "
        "<span class=\"mono\">SCN8A</span> (Na<sub>V</sub>1.6, gain-of-function epileptic "
        "encephalopathy). Two calcium channels extend it: <span class=\"mono\">CACNA1A</span> "
        "(Ca<sub>V</sub>2.1, the P/Q-type channel implicated in absence epilepsy and episodic ataxia) and "
        "<span class=\"mono\">CACNA1H</span> (Ca<sub>V</sub>3.2, the low-threshold <strong>T-type</strong> "
        "channel of the thalamocortical absence rhythm). <span class=\"mono\">GRIN2A</span> carries the "
        "NMDA-receptor (glutamatergic, calcium-permeable) side, central to the epilepsy-aphasia spectrum. "
        "The mechanism DIRECTION on this lever is the textbook one: agents that <em>reduce</em> "
        "voltage-gated inward current &mdash; the sodium-channel-blocking anticonvulsants on the Na side, "
        "the T-type blockade that defines the absence-seizure drugs on the Ca side &mdash; are "
        "threshold-raising in the L1 sense. <strong>But here the model records a caveat it must not "
        "hide.</strong> In Dravet syndrome the <span class=\"mono\">SCN1A</span> defect is a "
        "<em>loss</em>-of-function in inhibitory interneurons, so a blunt sodium-channel <em>blocker</em> "
        "&mdash; the generic L1 move &mdash; <strong>worsens</strong> the disorder and is clinically "
        "<strong>contraindicated</strong>. This is precisely why the promoter read "
        "<span class=\"mono\">&gamma;</span> is graded <span class=\"mono\">[V]</span> for "
        "<em>structure only</em>, trait-blind: it places the gene on the lever by the stiffness of its "
        "promoter switch, and says <strong>nothing</strong> about the sign of the clinical intervention, "
        "which is gene-, variant-, and cell-type-specific and stays graded <span class=\"mono\">[O]</span>. "
        "A direction, never a dose &mdash; <span class=\"mono\">efficacy = 0</span>.",
    ]),
    sec("L2 &mdash; increase the outward potassium current (the dominant lever)", [
        "The second lever raises the pull <em>back</em> from the crossing by strengthening the outward, "
        "repolarising potassium current &mdash; and in epilepsy this is the lever with the clearest "
        "mechanism of all. Four channels carry it. <span class=\"mono\">KCNQ2</span> and "
        "<span class=\"mono\">KCNQ3</span> (K<sub>V</sub>7.2 / K<sub>V</sub>7.3) are the neuronal "
        "<strong>M-current</strong> pair &mdash; the canonical excitability brake, mutated in benign "
        "familial neonatal epilepsy and in severe <span class=\"mono\">KCNQ2</span> encephalopathy, and the "
        "target of <strong>retigabine</strong>, the one marketed anticonvulsant whose entire mechanism is "
        "<em>opening</em> a potassium channel. That is the named molecular precedent that makes L2 the "
        "dominant lever here: an M-current <em>opener</em> is threshold-raising in the L2 sense, the mirror "
        "image of the L1 inward-current reduction, and it is the cleanest example in the whole "
        "anticonvulsant pharmacopoeia. <span class=\"mono\">KCNB1</span> (K<sub>V</sub>2.1) is the major "
        "somatic delayed-rectifier; <span class=\"mono\">KCNA1</span> (K<sub>V</sub>1.1) carries the "
        "episodic-ataxia-with-epilepsy phenotype. The fourth channel forces a <strong>second honest "
        "caveat</strong>: <span class=\"mono\">KCNT1</span> (the sodium-activated potassium channel Slack) "
        "is on the potassium lever by biophysics, but its epilepsy variants are "
        "<strong>gain</strong>-of-function &mdash; <em>too much</em> of this outward current is the "
        "pathology in malignant migrating partial seizures of infancy &mdash; so its therapeutic direction "
        "is <strong>inverted</strong> relative to the generic L2 move (the precedent here, quinidine, is a "
        "channel <em>blocker</em>). The model carries that inverted sign explicitly rather than smoothing "
        "it away. Riding <strong>L2-adjacent</strong> are the inhibitory GABA&#8209;A subunits "
        "<span class=\"mono\">GABRG2</span> (the &gamma;2 subunit of GEFS+ / febrile seizures) and "
        "<span class=\"mono\">GABRA1</span> (the &alpha;1 subunit of juvenile myoclonic epilepsy): they do "
        "not carry a potassium current, but they raise the same threshold by increasing inhibitory chloride "
        "conductance &mdash; the benzodiazepine / barbiturate axis &mdash; which is the L2 <em>logic</em> "
        "(strengthen the restoring pull) realised through a different ion. Every claim on this lever is a "
        "<strong>mechanism direction only</strong>; no opener, blocker, dose, or patient is named.",
    ]),
    sec("L3 &mdash; remove the upstream mTOR drive (the [O] lever)", [
        "The third lever does not touch the channel at all; it removes the <em>up-stream</em> drive that "
        "keeps the threshold low. In a large and growing class of epilepsies that drive is a single "
        "signalling pathway: <strong>mTOR</strong>. When the mTORC1 complex is disinhibited, neurons and "
        "cortical architecture become chronically hyperexcitable &mdash; the <em>mTORopathies</em>. Three "
        "genes anchor this lever, all of them <strong>repressors</strong> of mTOR whose loss releases the "
        "drive: <span class=\"mono\">DEPDC5</span> (a subunit of the GATOR1 complex, the leading cause of "
        "familial focal epilepsy and a frequent driver of focal cortical dysplasia), and "
        "<span class=\"mono\">TSC1</span> (hamartin) and <span class=\"mono\">TSC2</span> (tuberin), the "
        "two subunits of the tuberous-sclerosis complex, whose loss causes the severe, often "
        "drug-resistant epilepsy of tuberous sclerosis. The mechanism DIRECTION here has a named precedent "
        "&mdash; <strong>mTOR inhibition</strong>, the everolimus principle &mdash; but this is the lever "
        "that demands the most discipline, and it gets it. Every L3 link is held at grade "
        "<span class=\"mono\">[O]</span> &mdash; <strong>open, cited biology, never derived from the "
        "substrate</strong>. The model does <em>not</em> claim to compute that mTOR sets the over-sync "
        "threshold; it records, as cited upstream biology, that this is the drive whose removal would raise "
        "it. A <strong>fail-closed L3-honesty gate</strong> enforces exactly this: it checks that the "
        "declared L3 set is present, that each member is graded <span class=\"mono\">[O]</span> and marked "
        "not-derived, that no mTOR-pathway gene is mislabelled as a current-carrying ion channel, and that "
        "the firewall sentence separating the promoter <span class=\"mono\">|h_sp|</span> from the §25 "
        "network over-sync threshold is present &mdash; and it FAILS the build if any of these slips.",
    ]),
    sec("The DNA grounding: a promoter's own switch stiffness", [
        "What places each of the sixteen genes is not a list but a <strong>read</strong>. For every gene, "
        "the module takes its promoter window (transcription start &minus;2000 to +500 bases, "
        "<em>Homo sapiens</em>) and computes <span class=\"mono\">&gamma; = &minus;mean</span> of the "
        "nearest-neighbour base-stacking free energies along that window (the SantaLucia 1998 "
        "nearest-neighbour thermodynamics), then turns that <span class=\"mono\">&gamma;</span> into the "
        "promoter's switch stiffness through the <em>frozen engine's own</em> functions: "
        "<span class=\"mono\">|h_sp| = spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></span> and "
        "<span class=\"mono\">barrier = &gamma;&sup2;/4</span>. The reads span a real range &mdash; the "
        "stiffest promoter in the set is <span class=\"mono\">CACNA1H</span> at "
        "<span class=\"mono\">&gamma; &approx; 1.64</span> (<span class=\"mono\">|h_sp| &approx; 0.81</span>, "
        "the T-type calcium channel), and the softest is <span class=\"mono\">SCN2A</span> at "
        "<span class=\"mono\">&gamma; &approx; 1.20</span> (<span class=\"mono\">|h_sp| &approx; 0.50</span>) "
        "&mdash; with the M-current brake <span class=\"mono\">KCNQ2</span> reading stiff "
        "(<span class=\"mono\">&gamma; &approx; 1.58</span>, <span class=\"mono\">|h_sp| &approx; 0.76</span>) "
        "and the Dravet gene <span class=\"mono\">SCN1A</span> reading near the soft end "
        "(<span class=\"mono\">&gamma; &approx; 1.25</span>, <span class=\"mono\">|h_sp| &approx; 0.53</span>). "
        "These are read on the <strong>same R19 substrate, with the same engine, that the bipolar and "
        "analgesic packages used</strong>, which is the whole point of the inheritance: one substrate, one "
        "pipeline, three problems. The <span class=\"mono\">&gamma;</span> read is a property of the gene's "
        "<strong>promoter sequence</strong>, and that is <em>all</em> it is.",
    ]),
    sec("Ranking targets, and the firewall that keeps gamma honest", [
        "The last component prioritises, and it prioritises <strong>targets, never drugs or doses</strong>. "
        "A burden-weighted score combines three declared, cited weights &mdash; clinical burden "
        "(<span class=\"mono\">0.40</span>), unmet need (<span class=\"mono\">0.35</span>), and "
        "genetic-evidence / druggability (<span class=\"mono\">0.25</span>) &mdash; on cited 1&ndash;5 tiers, "
        "and ranks the genes by that score alone. <span class=\"mono\">SCN1A</span> tops the list (Dravet, "
        "high SUDEP burden, the most-replicated monogenic gene), followed by <span class=\"mono\">KCNQ2</span> "
        "and the tuberous-sclerosis / GATOR1 mTOR set; <span class=\"mono\">SCN1A</span> is also flagged "
        "<strong>not actionable by the generic lever sign</strong>, carrying its Dravet contraindication "
        "right in the ranking. Crucially, the <span class=\"mono\">&gamma;</span> read is carried "
        "<em>alongside</em> each target as structural context but is <strong>never folded into the "
        "score</strong> &mdash; and the result is a clean demonstration of the firewall: the priority "
        "ranking and the <span class=\"mono\">&gamma; / |h_sp|</span> ranking are "
        "<strong>decoupled</strong>. The <strong>stiffest</strong> promoter read in the whole set, "
        "<span class=\"mono\">CACNA1H</span> (<span class=\"mono\">|h_sp| &approx; 0.81</span>), sits near "
        "the <em>bottom</em> of priority; the <strong>top-priority</strong> target "
        "<span class=\"mono\">SCN1A</span> has one of the <em>softest</em> reads in the set "
        "(<span class=\"mono\">|h_sp| &approx; 0.53</span>). If promoter stiffness drove the ranking, "
        "neither could sit where it does. That decoupling is the firewall made visible, and it must be "
        "stated once more in full: the promoter <span class=\"mono\">|h_sp|</span> is a gene's "
        "<strong>own switch stiffness</strong>, and it is <strong>never</strong> equated with the §25 "
        "network over-synchronisation threshold on <span class=\"mono\">R</span>, nor with a channel's "
        "activation voltage, a compound's potency, a dose, an in-vivo selectivity, or any clinical effect. "
        "A <strong>fail-closed forbidden-claim scanner</strong> guards the whole package: it scans the "
        "written results for any dose, efficacy-as-fact, safety-as-fact, or synthesis statement &mdash; "
        "including <em>seizure-freedom</em> and <em>stops-seizures</em> language &mdash; carries a negation "
        "guard, and includes a planted self-test that <em>must</em> fire on its own bait, failing the build "
        "if it ever does not. This module reproduces bit-for-bit with the engine byte-unchanged.",
        "Everything here is an in-silico <em>reading</em> of promoter sequence and a <em>frame</em> for "
        "organising targets, not a clinical measure, a diagnosis, or a prescription. The model asserts "
        "<em>mechanism directions and target placements</em> &mdash; a threshold can be raised three ways; "
        "these sixteen genes populate the three levers; these targets carry the highest genetic burden "
        "&mdash; and <strong>nothing</strong> about which agent acts on any lever, at what dose, in whom, "
        "whether any real drug raises anyone's seizure threshold, or that anyone should change a treatment. "
        "The agents named as <em>directions</em> (the sodium-channel blockers and T-type blockers on L1, "
        "retigabine via the M-current on L2, everolimus via mTOR on L3) are illustrations of a "
        "<em>sign</em>, never a recommendation &mdash; and the two recorded caveats (the Dravet "
        "contraindication on <span class=\"mono\">SCN1A</span>, the inverted sign on "
        "<span class=\"mono\">KCNT1</span>) are there precisely because a generic lever sign is "
        "<strong>not</strong> a clinical direction. Real epilepsy is heterogeneous, frequently polygenic, "
        "and often drug-resistant, and that heterogeneity is <strong>locked</strong>. A promoter read and a "
        "lever assignment are mechanism boundaries, <strong>not</strong> a claim about the felt quality of a "
        "seizure or its aftermath (Axis-A firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>, "
        "the hard problem stays <strong>open</strong>). <strong>This is not medical advice, not a diagnosis, "
        "not a treatment protocol, and not a cure.</strong> "
        "<span class=\"mono\">medium_efficacy_tested = 0</span>; targets ranked, never drugs or doses."
    ]),
])

PREV = '<a rel="prev" href="/mind/30-bipolar-threshold-levers/">&larr; §30 Bipolar: three threshold levers</a>'
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
  <a href="{GH}/31-epilepsy-threshold-levers/" rel="noopener">reproduce (GitHub)</a>
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
