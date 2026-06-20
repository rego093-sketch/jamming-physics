#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch33_schizophrenia_levers.py — emit the §33 schizophrenia threshold-levers chapter (roadmap T1a-L).

Writes docs/mind/33-schizophrenia-threshold-levers/index.html using the same head/JSON-LD/footer
scaffolding as the other Part-II chapters so the SEO markup is byte-consistent. The answer-first
<p class="answer"> and the vp-card asides are NOT written here — build_search_layer.py injects them
from mind_registry.py (single source of truth): this generator only emits the skeleton (abstract +
claim-strip + body sections + nav). Body text is English-only (VP-SPEC C0).

This chapter applies the SAME threshold-shift intervention logic that §30 (bipolar T2b-L), §31
(epilepsy T2a-L) and §32 (depression T1b-L) used, inherited from the analgesic reproducibility
package (Zenodo 10.5281/zenodo.20733420), to the §24 (T1a) OVER-IGNITION / aberrant-salience pole —
and it is the FIRST case that is L1+L3 CO-DOMINANT and the FIRST that is DOMAIN-RESTRICTED. §24 placed
the positive domain as an operating point whose ignition fold sits too low; the corrective sign is
"reduce the excess drive / raise the fold" (the same direction as epilepsy/bipolar mania), but §24
left that as ONE abstract operator. This chapter decomposes it into a DNA-grounded three-lever target
map over fourteen schizophrenia genes, with six on L1 (glutamate/NMDA) and six on L3 (dopamine), and
shows the map reaches the POSITIVE domain ONLY. Seven promoter reads (GRIN2A/CACNA1C/CACNB2 from the
bipolar cache, GRIN2B/COMT/HTR2A/GABRA1 from the depression cache) are carried over VERBATIM (gamma is
strand-symmetric). No new mechanism, no new tuned constant; the engine is READ-ONLY. The numbers quoted
in the prose are the structural reads (gamma, |h_sp|) and the burden ranking from
repro/mind/_verify/schizophrenia_threshold_levers.py and schizophrenia_burden_prioritisation.py
(efficacy=0; targets ranked, never drugs or doses); the canonical numeric artifacts are those modules'
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

SLUG = "33-schizophrenia-threshold-levers"
NO = 33
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Schizophrenia threshold levers: the over-ignition sign, decomposed (positive-domain only)"
H1 = ("Schizophrenia threshold levers &mdash; the over-ignition operating-point correction, decomposed into "
      "DNA-grounded levers (L1+L3 co-dominant, positive-domain only)")
CRUMB = "Schizophrenia: three threshold levers"
HEADLINE = ("The schizophrenia over-ignition operating-point correction decomposed into a DNA-grounded "
            "three-lever target map: modulate the inward glutamatergic / NMDA current (L1) and remove the "
            "up-stream dopamine drive (L3) co-dominantly, with the outward GABA-A current (L2) as the minor "
            "lever, over fourteen schizophrenia genes &mdash; reaching the positive (aberrant-salience) "
            "domain only")
META = ("Chapter 24 placed the positive symptoms of schizophrenia as an over-ignition / aberrant-salience "
        "operating point but treated the correction as one abstract operator. This chapter applies the same "
        "threshold-shift intervention logic used for bipolar disorder, epilepsy and depression (inherited "
        "from the analgesic reproducibility package, Zenodo 10.5281/zenodo.20733420) and decomposes that "
        "correction into three concrete levers -- modulate the inward glutamatergic / NMDA current (L1) and "
        "remove the up-stream dopamine drive (L3) co-dominantly, increase the outward GABA-A current (L2) -- "
        "over fourteen schizophrenia genes placed by their own promoter switch stiffness. The first L1+L3 "
        "co-dominant case and the first domain-restricted case: the lever map reaches the positive domain "
        "only; the negative and cognitive domains are not reached. Targets are ranked, never drugs or doses. "
        "efficacy=0; not medical advice.")

ABSTRACT = (
    "The <a href=\"/mind/24-schizophrenia-mirror/\">schizophrenia chapter</a> read the disorder's positive "
    "symptoms as an <strong>over-ignition / aberrant-salience</strong> operating point: the ignition fold "
    "that should gate a percept or belief sits <em>too low</em>, so weak, internally generated assemblies "
    "ignite as hallucinations and delusions. That chapter proved the <em>pole</em> and the corrective "
    "<em>sign</em> &mdash; the positive domain is an <strong>over-ignition</strong> pole, so the corrective "
    "push is whatever <strong>reduces the excess drive</strong> or <strong>raises the fold</strong>, the "
    "<em>same</em> direction as epilepsy and bipolar mania &mdash; but it left that push <em>abstract</em>, "
    "and it carried a second, sharper result the others did not: the disorder splits into three "
    "<strong>distinct domains</strong> (positive / negative / cognitive) that are <em>not</em> a single "
    "severity axis. This chapter fills the first gap and respects the second, with the <strong>same piece "
    "of inherited technology</strong> the <a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a>, "
    "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a> and "
    "<a href=\"/mind/32-depression-threshold-levers/\">depression</a> levers chapters used: the "
    "<strong>threshold-shift intervention logic</strong> from the analgesic reproducibility package "
    "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>). Its three "
    "abstract levers &mdash; <strong>L1</strong> change the inward (excitatory) current, "
    "<strong>L2</strong> change the outward (potassium / inhibitory) current, <strong>L3</strong> change "
    "the up-stream drive &mdash; carry over unchanged, but schizophrenia is where the frame meets <strong>two "
    "firsts</strong>. It is the first case that is <strong>L1+L3 co-dominant</strong>: of <strong>fourteen</strong> "
    "schizophrenia genes, <strong>six</strong> sit on the glutamate/NMDA inward lever (L1) and <strong>six</strong> "
    "on the dopamine up-stream lever (L3), with only two on the channel-restore lever (L2) &mdash; the two "
    "leading pathophysiologies of the disorder loaded onto the map <em>at once</em>. The L1 set is the "
    "glutamatergic axis (<span class=\"mono\">GRIN1</span>, <span class=\"mono\">GRIN2A</span>, "
    "<span class=\"mono\">GRIN2B</span>, <span class=\"mono\">GRIA3</span>, <span class=\"mono\">CACNA1C</span>, "
    "<span class=\"mono\">CACNB2</span>); the L3 set is the dopamine antipsychotic axis in three sub-axes "
    "&mdash; receptors (<span class=\"mono\">DRD2</span>, <span class=\"mono\">DRD4</span>), "
    "synthesis/transport (<span class=\"mono\">TH</span>, <span class=\"mono\">SLC6A3</span>), and "
    "serotonergic / catabolic modulation (<span class=\"mono\">HTR2A</span>, <span class=\"mono\">COMT</span>) "
    "&mdash; while L2 carries the GABA-A pair (<span class=\"mono\">GABRA1</span>, <span class=\"mono\">GABRB3</span>). "
    "And it is the first case that is <strong>domain-restricted</strong>: the gain-reducing scalar lever "
    "reverses the <strong>positive</strong> domain <em>only</em>; the <strong>negative</strong> "
    "(output-deficit) and <strong>cognitive</strong> (long-range wiring) domains are <em>not</em> reached, "
    "because a threshold shift cannot re-route geometry nor restore a deficit by lowering a fold. Each gene "
    "is placed by reading its <strong>own promoter switch stiffness</strong> &mdash; "
    "<span class=\"mono\">&gamma; = &minus;mean</span> nearest-neighbour stacking free energy (SantaLucia "
    "1998) over its promoter window, turned into <span class=\"mono\">|h_sp| = spinodal(&gamma;)</span> with "
    "the frozen engine <strong>read-only</strong>, and seven of the reads "
    "(<span class=\"mono\">GRIN2A</span>, <span class=\"mono\">CACNA1C</span>, <span class=\"mono\">CACNB2</span> "
    "from the bipolar cache, <span class=\"mono\">GRIN2B</span>, <span class=\"mono\">COMT</span>, "
    "<span class=\"mono\">HTR2A</span>, <span class=\"mono\">GABRA1</span> from the depression cache) are "
    "carried over <strong>verbatim</strong>. Two honest caveats are recorded, not hidden: the L1 "
    "NMDA-hypofunction direction is <strong>sign-subtle</strong> (the leading model is a "
    "parvalbumin-interneuron NMDA hypofunction that <em>disinhibits</em> downstream circuits, so a "
    "glycine-site <em>agonist</em> direction appears alongside the naive reduce-excitation sign &mdash; the "
    "schizophrenia analogue of depression's ketamine caveat), and the <span class=\"mono\">HTR2A</span> "
    "direction is <strong>non-monotone</strong>. Three fail-closed disciplines ride along: every dopamine "
    "and glutamate link stays graded <span class=\"mono\">[O]</span> cited biology, a forbidden-claim "
    "scanner rejects any dose / efficacy / safety / synthesis statement (including treats-psychosis, "
    "remission, and relapse-prevention language), and a burden-weighted ranking orders <strong>targets, "
    "never drugs or doses</strong>. The <strong>firewall</strong> is absolute: the promoter "
    "<span class=\"mono\">|h_sp|</span> is a gene's own switch stiffness, <strong>never</strong> the §24 "
    "network over-ignition threshold, a receptor occupancy, a synaptic dopamine level, a potency, a dose, "
    "or a clinical effect. <span class=\"mono\">efficacy = 0</span>; not medical advice; the hard problem "
    "stays open."
)

BODY = "\n".join([
    "<h2>What §24 left abstract</h2>",
    "".join([
        "<p>The <a href=\"/mind/24-schizophrenia-mirror/\">schizophrenia chapter</a> placed the positive "
        "symptoms at the <strong>over-ignition operating point</strong> of the atlas: health is a population "
        "of micro-eddies igniting in gamma only when a percept or belief clears a threshold (the ignition "
        "<em>fold</em>), and the positive symptoms of schizophrenia are what happens when that fold sits "
        "<strong>too low</strong> &mdash; weak, internally generated assemblies cross it and ignite as "
        "<em>aberrant salience</em>: a stray association is experienced as a revelation, an internal voice as "
        "an external one. That chapter proved two things and stopped. The first is the <em>pole</em>: the "
        "positive domain is an <strong>over-ignition</strong> pole &mdash; the same side of the line as the "
        "over-synchronisation disorders &mdash; so the corrective <em>sign</em> is whatever <strong>reduces "
        "the excess drive</strong> or <strong>raises the fold</strong>, the mirror of depression's "
        "restore-the-deficit and the twin of epilepsy's and bipolar mania's reduce-the-excess. The second is "
        "sharper and is the reason this chapter is unlike the three before it: §24 also proved that "
        "schizophrenia is <strong>not one axis</strong>. Its symptoms split into three "
        "<strong>distinct domains</strong> &mdash; <strong>positive</strong> (the over-ignition just "
        "described), <strong>negative</strong> (an <em>output / gain deficit</em>: blunted affect, "
        "avolition, poverty of speech), and <strong>cognitive</strong> (a <em>long-range wiring</em> / "
        "dysconnection problem: working memory, executive control) &mdash; and these are <em>not</em> three "
        "severities of one thing. The corrective sign §24 proved applies to the <strong>positive</strong> "
        "domain; it says nothing about restoring the negative or re-routing the cognitive. A mechanism atlas "
        "should be able to say <em>which</em> molecular targets realise the positive correction <strong>and</strong> "
        "be honest about which domains a threshold lever cannot reach. That is exactly what this chapter does.</p>",
    ]),

    "<h2>The inherited technology, applied a fourth time &mdash; and the first L1+L3 co-dominant case</h2>",
    "".join([
        "<p>The handle is not invented here and it is not adapted here &mdash; it is the <em>same</em> logic the "
        "<a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a>, "
        "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a> and "
        "<a href=\"/mind/32-depression-threshold-levers/\">depression</a> chapters inherited from the "
        "<strong>analgesic reproducibility package</strong> "
        "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>), now turned on a "
        "fourth disorder. Its premise is general: an operating point is set by a balance of currents and the "
        "drives that bias them, so there are exactly <strong>three levers</strong> on it. <strong>L1</strong> "
        "&mdash; <em>change the inward, excitatory current</em>. <strong>L2</strong> &mdash; <em>change the "
        "outward, repolarising (or inhibitory) current</em>. <strong>L3</strong> &mdash; <em>change the "
        "up-stream drive</em> that sets where the operating point sits. The frame applies unchanged because "
        "the schizophrenia chapter, the three levers chapters, and the analgesic package all share the "
        "<strong>same R19 substrate</strong> &mdash; the engine's supercritical pitchfork "
        "<span class=\"mono\">&#7779; = g&middot;s &minus; s&sup3; + h</span>, whose spinodal fold IS the "
        "switching barrier.</p>",
        "<p>Schizophrenia makes the frame's generality vivid in a way the first three disorders did not, "
        "because of a shift of <strong>distribution</strong>. Where bipolar leaned on L1 (its replicated GWAS "
        "loci are calcium channels), epilepsy on L2 (the <span class=\"mono\">KCNQ2</span>/<span class=\"mono\">KCNQ3</span> "
        "M-current), and depression on L3 (the up-stream HPA / monoamine / neurotrophic drives, L3-dominant), "
        "schizophrenia is the first case that is <strong>L1+L3 co-dominant</strong>: of the fourteen genes, "
        "<strong>six sit on L1</strong> and <strong>six on L3</strong>, with only two on L2. The two leading "
        "pathophysiologies of the disorder &mdash; the <strong>glutamate / NMDA-hypofunction</strong> "
        "hypothesis and the <strong>dopamine</strong> hypothesis &mdash; load the positive-domain correction "
        "onto the map <em>at once</em>, neither one subordinate. That is not a defect of the frame; it is the "
        "frame reporting, faithfully, that schizophrenia's positive domain is driven from <em>two</em> "
        "directions where the other disorders were driven from one. The pipeline is reused at the level of "
        "code, not analogy: <strong>seven</strong> of the reads &mdash; <span class=\"mono\">GRIN2A</span>, "
        "<span class=\"mono\">CACNA1C</span>, <span class=\"mono\">CACNB2</span> from the bipolar cache and "
        "<span class=\"mono\">GRIN2B</span>, <span class=\"mono\">COMT</span>, <span class=\"mono\">HTR2A</span>, "
        "<span class=\"mono\">GABRA1</span> from the depression cache &mdash; are carried over "
        "<strong>verbatim</strong>, because <span class=\"mono\">&gamma;</span> is a strand-symmetric property "
        "of the sequence and does not change between problems. Nothing about the engine is touched; the module "
        "re-emerges the frozen tree read-only and confirms it byte-unchanged, and registers as the "
        "<strong>eleventh atlas citizen</strong> (<span class=\"mono\">SZ-T1a-L</span>).</p>",
    ]),

    "<h2>The new finding: a domain-restricted map (the positive domain only)</h2>",
    "".join([
        "<p>This is the result that makes schizophrenia the most honest chapter in the levers series, and the "
        "model states it as a <strong>structural restriction</strong>, not a hedge. The three levers are all "
        "<em>scalar</em> operators on a single operating point: they raise or lower a current or a drive, and "
        "thereby raise or lower the ignition fold. That is precisely the right tool for the "
        "<strong>positive</strong> domain, which §24 defined as a <em>fold set too low</em> &mdash; a "
        "gain-reducing lever raises the fold and the aberrant ignitions stop crossing it. But it is the "
        "<em>wrong</em> tool for the other two domains, and the model says so rather than quietly claiming "
        "credit for them. The <strong>negative</strong> domain is an <em>output / gain deficit</em>: the "
        "problem is too <em>little</em> ignition, not too much, so a gain-reducing lever pushes in the wrong "
        "direction entirely &mdash; you cannot lift a deficit by lowering a fold. The <strong>cognitive</strong> "
        "domain is a <em>long-range wiring</em> problem: the deficit is in the <em>geometry</em> of "
        "connectivity (the §19 dysconnection result), and a scalar current or drive lever leaves the locality "
        "imbalance <strong>exactly invariant</strong> &mdash; geometry cannot be re-routed by a threshold "
        "shift. So the lever map reaches the <strong>positive domain and only the positive domain</strong>, "
        "and the module records this in a <strong>domain-restriction witness</strong>: positive = reached, "
        "negative = not reached, cognitive = not reached. This is the first time the inherited frame has "
        "encountered a disorder it can only <em>partly</em> address, and capturing that partiality precisely "
        "&mdash; axis-structured, not dose-structured &mdash; is more informative than a map that pretended to "
        "cover all three. It is also why the <em>fail-closed L3-honesty gate</em> for this chapter checks not "
        "only that the dopamine links stay <span class=\"mono\">[O]</span> but that the co-dominance and the "
        "domain restriction are both recorded; it FAILS the build if either slips.</p>",
    ]),

    "<h2>L1 (co-dominant) &mdash; the inward glutamatergic / NMDA levers (and the NMDA-hypofunction subtlety)</h2>",
    "".join([
        "<p>The first co-dominant lever is the <strong>glutamate / NMDA axis</strong>, and it carries the "
        "chapter's <strong>first and most important honest caveat</strong>. Six genes sit here. "
        "<span class=\"mono\">GRIN1</span> is the obligate NMDA-receptor subunit (GluN1) and the glycine-site "
        "node; <span class=\"mono\">GRIN2A</span> and <span class=\"mono\">GRIN2B</span> are the GluN2A and "
        "GluN2B modulatory subunits (<span class=\"mono\">GRIN2A</span> is one of the few genes with "
        "<em>both</em> genome-wide common-variant and exome rare-variant evidence); "
        "<span class=\"mono\">GRIA3</span> is an AMPA-receptor subunit carrying the fast-excitatory sub-route; "
        "and <span class=\"mono\">CACNA1C</span> (the L-type calcium channel Ca<sub>V</sub>1.2, the same "
        "top-replicated cross-disorder locus that anchored the bipolar L1) and <span class=\"mono\">CACNB2</span> "
        "(its auxiliary &beta;2 subunit) carry the voltage-gated calcium sub-route. The naive reading of L1 "
        "would be <em>reduce inward excitatory current</em> &mdash; but in schizophrenia the leading "
        "glutamatergic model is <strong>NMDA hypofunction</strong>, and its sign is not that simple. The "
        "current understanding is that NMDA receptors on fast-spiking <strong>parvalbumin interneurons</strong> "
        "are hypofunctional, which <em>disinhibits</em> downstream pyramidal circuits and produces the "
        "<em>downstream</em> over-ignition the positive symptoms reflect. So the L1 agent direction is "
        "<strong>sign-subtle</strong>: a glycine-site or <span class=\"mono\">GRIN1</span>-potentiating "
        "<em>agonist</em> direction (raising NMDA function on the interneurons) appears <em>alongside</em> the "
        "naive reduce-excitation reading, because the lever's effect runs through an interneuron-then-"
        "disinhibition route rather than a direct one. This is the schizophrenia analogue of depression's "
        "ketamine caveat, and the model flags it explicitly: the lever <em>placement</em> (the gene is on the "
        "inward-current lever) is structural and trait-blind, but the <em>direction</em> of the clinically "
        "relevant agent runs through a downstream route and is gene-, dose-, and mechanism-specific, and stays "
        "graded <span class=\"mono\">[O]</span>. A promoter read places a gene on a lever; it says "
        "<strong>nothing</strong> about whether an agonist or an antagonist is the therapeutic direction. A "
        "direction, never a dose.</p>",
    ]),

    "<h2>L3 (co-dominant) &mdash; remove the up-stream dopamine drive (the antipsychotic axis)</h2>",
    "".join([
        "<p>The second co-dominant lever does not touch a channel; it changes the <em>up-stream dopamine "
        "drive</em> that sets the aberrant-salience operating point, and it is the <strong>single most "
        "established target axis in psychiatry</strong>. Six genes sit here, in three sub-axes. The first is "
        "the dopamine <strong>receptor</strong> set: <span class=\"mono\">DRD2</span> &mdash; the dopamine D2 "
        "receptor, the target shared by <em>every</em> licensed agent for the disorder and a genome-wide "
        "significant GWAS locus, the most established single node in the whole map &mdash; and "
        "<span class=\"mono\">DRD4</span>, the D4 receptor whose high clozapine affinity once made it a "
        "candidate (a clean D4-selective direction stays exploratory). The second is the dopamine "
        "<strong>synthesis / transport</strong> set: <span class=\"mono\">TH</span> (tyrosine hydroxylase, the "
        "rate-limiting enzyme &mdash; the elevated presynaptic striatal dopamine-synthesis capacity is the "
        "most-replicated imaging abnormality in the disorder, and it is a <em>presynaptic</em> handle distinct "
        "from the postsynaptic D2 route) and <span class=\"mono\">SLC6A3</span> (the dopamine transporter, "
        "DAT). The third is <strong>serotonergic and catabolic modulation</strong>: "
        "<span class=\"mono\">HTR2A</span> (the 5-HT2A receptor, the serotonin-dopamine atypical axis, with a "
        "<strong>non-monotone</strong> direction the model records rather than picking a side) and "
        "<span class=\"mono\">COMT</span> (catechol-O-methyltransferase, the prefrontal catecholamine "
        "Val158Met set-point modifier). The mechanism direction across this lever is to "
        "<strong>reduce the up-stream dopamine drive</strong> &mdash; lowering the aberrant-salience signal "
        "that drops the over-ignition fold &mdash; and it reaches the <strong>positive domain only</strong>, "
        "which is exactly why the established route, for all its reach over positive symptoms, leaves the "
        "negative and cognitive domains largely untouched. Every L3 link is held at grade "
        "<span class=\"mono\">[O]</span> &mdash; <strong>open, cited biology, never derived from the substrate</strong>. "
        "The model does <em>not</em> claim to compute that dopamine sets the network fold; it records, as "
        "cited upstream biology, that this is the drive whose reduction would raise it. A direction, never a "
        "dose &mdash; <span class=\"mono\">efficacy = 0</span>.</p>",
    ]),

    "<h2>L2 &mdash; the minor outward GABA-A restore lever</h2>",
    "".join([
        "<p>The third lever is <em>minor</em> in schizophrenia &mdash; two genes &mdash; and it is the "
        "restoring mirror of the inward levers, realised through inhibition. <span class=\"mono\">GABRA1</span> "
        "(the GABA-A &alpha;1 subunit, its read reused from the depression cache verbatim) and "
        "<span class=\"mono\">GABRB3</span> (the GABA-A &beta;3 subunit on 15q11&ndash;13) raise the "
        "<strong>inhibitory chloride conductance</strong> &mdash; the same restoring side of the "
        "positive-domain over-ignition axis, approached through the cortical <strong>parvalbumin-interneuron</strong> "
        "deficit that also underlies the L1 sign subtlety. This lever is the direct counterpart of the "
        "interneuron-restore idea: where L1 raises NMDA function <em>on</em> the interneurons, L2 raises the "
        "inhibitory current those interneurons deliver. It is carried as a minor lever because the replicated "
        "genetic and pharmacological weight of the disorder sits on the glutamate and dopamine axes, not on "
        "the GABA-A channels &mdash; but the two genes are real targets on the restoring side, and they ride "
        "<strong>L2-adjacent</strong> exactly as <span class=\"mono\">GABRA1</span> did in the depression "
        "chapter. Every claim on this lever is a <strong>mechanism direction only</strong>; no opener, "
        "modulator, dose, or patient is named.</p>",
    ]),

    "<h2>The DNA grounding: a promoter's own switch stiffness</h2>",
    "".join([
        "<p>What places each of the fourteen genes is not a list but a <strong>read</strong>. For every gene, "
        "the module takes its promoter window (transcription start &minus;2000 to +500 bases, <em>Homo "
        "sapiens</em>) and computes <span class=\"mono\">&gamma; = &minus;mean</span> of the "
        "nearest-neighbour base-stacking free energies along that window (the SantaLucia 1998 nearest-neighbour "
        "thermodynamics), then turns that <span class=\"mono\">&gamma;</span> into the promoter's switch "
        "stiffness through the <em>frozen engine's own</em> functions: "
        "<span class=\"mono\">|h_sp| = spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></span> and "
        "<span class=\"mono\">barrier = &gamma;&sup2;/4</span>. The reads span a real range &mdash; the "
        "stiffest promoter in the set is the dopamine transporter <span class=\"mono\">SLC6A3</span> at "
        "<span class=\"mono\">&gamma; &approx; 1.60</span> (<span class=\"mono\">|h_sp| &approx; 0.78</span>), "
        "followed by the D4 receptor <span class=\"mono\">DRD4</span> (<span class=\"mono\">&gamma; &approx; "
        "1.58</span>, <span class=\"mono\">|h_sp| &approx; 0.76</span>) and the obligate NMDA subunit "
        "<span class=\"mono\">GRIN1</span> (<span class=\"mono\">&gamma; &approx; 1.57</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.76</span>); the softest is the GABA-A subunit "
        "<span class=\"mono\">GABRA1</span> at <span class=\"mono\">&gamma; &approx; 1.25</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.54</span>), with the cross-disorder calcium channel "
        "<span class=\"mono\">CACNA1C</span> also near the soft end (<span class=\"mono\">&gamma; &approx; "
        "1.26</span>, <span class=\"mono\">|h_sp| &approx; 0.55</span>), and the lead glutamatergic target "
        "<span class=\"mono\">GRIN2A</span> reading <strong>mid-range</strong> (<span class=\"mono\">&gamma; "
        "&approx; 1.47</span>, <span class=\"mono\">|h_sp| &approx; 0.69</span>). These are read on the "
        "<strong>same R19 substrate, with the same engine, that the bipolar, epilepsy, depression and "
        "analgesic packages used</strong>, which is the whole point of the inheritance: one substrate, one "
        "pipeline, now five problems. The <span class=\"mono\">&gamma;</span> read is a property of the gene's "
        "<strong>promoter sequence</strong>, blind to whether the gene is on or off and to gain / loss / "
        "expression level, and that is <em>all</em> it is.</p>",
    ]),

    "<h2>Ranking targets, and the firewall that keeps gamma honest</h2>",
    "".join([
        "<p>The last component prioritises, and it prioritises <strong>targets, never drugs or doses</strong>. "
        "A burden-weighted score combines three declared, cited weights &mdash; clinical burden "
        "(<span class=\"mono\">0.40</span>), unmet need (<span class=\"mono\">0.35</span>), and "
        "genetic-evidence / druggability (<span class=\"mono\">0.25</span>) &mdash; on cited 1&ndash;5 tiers, "
        "and ranks the genes by that score alone. The top actionable target is <span class=\"mono\">GRIN2A</span> "
        "&mdash; the glutamatergic subunit with both common- and rare-variant support, addressing the "
        "treatment-resistant and negative/cognitive remainder the dopamine route misses &mdash; followed by "
        "<span class=\"mono\">GRIN2B</span> and then the established dopamine receptor "
        "<span class=\"mono\">DRD2</span>. A substantive consequence of the unmet-need weight is that it lifts "
        "the <strong>glutamatergic L1 axis above the established D2 route</strong>: the D2 receptor carries the "
        "highest burden but the lowest unmet need precisely <em>because</em> it is already the established "
        "axis, so the ranking surfaces the NMDA route as the higher-leverage unmet direction &mdash; the L1+L3 "
        "co-dominant map turned into a priority order, with the unmet-need tier breaking the L1/L3 symmetry in "
        "L1's favour. Several genes are flagged <strong>not actionable by the generic lever sign</strong>: "
        "<span class=\"mono\">CACNA1C</span> and <span class=\"mono\">CACNB2</span> (cross-disorder calcium "
        "set-point), <span class=\"mono\">DRD4</span> (exploratory), <span class=\"mono\">GABRB3</span> "
        "(exploratory), and <span class=\"mono\">SLC6A3</span> &mdash; the transporter is flagged because DAT "
        "blockade <em>raises</em> dopamine (the stimulant direction that worsens the positive domain), the "
        "wrong direction entirely. Crucially, the <span class=\"mono\">&gamma;</span> read is carried "
        "<em>alongside</em> each target as structural context but is <strong>never folded into the score</strong> "
        "&mdash; and the result is a clean demonstration of the firewall: the priority ranking and the "
        "<span class=\"mono\">&gamma; / |h_sp|</span> ranking are <strong>decoupled</strong>. The "
        "<strong>stiffest</strong> promoter read in the whole set, <span class=\"mono\">SLC6A3</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.78</span>), sits near the <strong>bottom</strong> of priority "
        "and is non-actionable; the <strong>top-priority</strong> target <span class=\"mono\">GRIN2A</span> "
        "has only a <em>mid-range</em> read (<span class=\"mono\">|h_sp| &approx; 0.69</span>). If promoter "
        "stiffness drove the ranking, neither could sit where it does. That decoupling is the firewall made "
        "visible, and it must be stated once more in full: the promoter <span class=\"mono\">|h_sp|</span> is "
        "a gene's <strong>own switch stiffness</strong>, and it is <strong>never</strong> equated with the §24 "
        "network over-ignition threshold on <span class=\"mono\">R</span>, nor with a receptor occupancy, a "
        "synaptic dopamine level, a compound's potency, a dose, an in-vivo selectivity, or any clinical "
        "effect. A <strong>fail-closed forbidden-claim scanner</strong> guards the whole package: it scans the "
        "written results for any dose, efficacy-as-fact, safety-as-fact, or synthesis statement &mdash; "
        "including <em>treats psychosis</em>, <em>remission</em>, <em>relapse-prevention</em>, and "
        "<em>antipsychotic-efficacy</em> language &mdash; carries a negation guard, and includes a planted "
        "self-test that <em>must</em> fire on its own bait, failing the build if it ever does not. This module "
        "reproduces bit-for-bit with the engine byte-unchanged.</p>",
        "<p>Everything here is an in-silico <em>reading</em> of promoter sequence and a <em>frame</em> for "
        "organising targets, not a clinical measure, a diagnosis, or a prescription. The model asserts "
        "<em>mechanism directions and target placements</em> &mdash; an over-ignition fold can be raised two "
        "ways at once; these fourteen genes populate the levers; schizophrenia loads them co-dominantly on "
        "glutamate (L1) and dopamine (L3); the map reaches the positive domain only; these targets carry the "
        "highest genetic and unmet-need burden &mdash; and <strong>nothing</strong> about which agent acts on "
        "any lever, at what dose, in whom, whether any real compound changes anyone's symptoms, or that anyone "
        "should change a treatment. The agents named as <em>directions</em> (the D2-antagonist route on the "
        "receptor sub-axis, the presynaptic-synthesis route, the glycine-site / NMDA-potentiating route "
        "flagged sign-subtle on L1, the 5-HT2A route flagged non-monotone) are illustrations of a <em>sign</em>, "
        "never a recommendation &mdash; and the two recorded caveats (the interneuron-disinhibition route of "
        "the L1 NMDA-hypofunction direction, the non-monotone <span class=\"mono\">HTR2A</span> direction) are "
        "there precisely because a generic lever sign is <strong>not</strong> a clinical direction. Real "
        "schizophrenia is heterogeneous and is <strong>three domains</strong>, not one &mdash; positive, "
        "negative, and cognitive, with distinct courses and only partial overlap &mdash; and that "
        "heterogeneity, including the two domains this lever map explicitly <em>cannot</em> reach, is "
        "<strong>locked</strong>. A promoter read and a lever assignment are mechanism boundaries, "
        "<strong>not</strong> a claim about the felt quality of psychosis (Axis-A firewall &mdash; "
        "<span class=\"mono\">consciousness_claim = 0</span>, the hard problem stays <strong>open</strong>). "
        "<strong>This is not medical advice, not a diagnosis, not a treatment protocol, and not a cure.</strong> "
        "<span class=\"mono\">medium_efficacy_tested = 0</span>; targets ranked, never drugs or doses.</p>",
    ]),
])

PREV = '<a rel="prev" href="/mind/32-depression-threshold-levers/">&larr; §32 Depression: three threshold levers</a>'
NEXT = '<a rel="next" href="/mind/34-autism-threshold-levers/">§34 Autism: three threshold levers &rarr;</a>'

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
  <a href="{GH}/{SLUG}/" rel="noopener">reproduce (GitHub)</a>
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
