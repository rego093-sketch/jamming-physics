#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch32_depression_levers.py — emit the §32 depression threshold-levers chapter (roadmap T1b-L).

Writes docs/mind/32-depression-threshold-levers/index.html using the same head/JSON-LD/footer
scaffolding as the other Part-II chapters so the SEO markup is byte-consistent. The answer-first
<p class="answer"> and the vp-card asides are NOT written here — build_search_layer.py injects them
from mind_registry.py (single source of truth): this generator only emits the skeleton (abstract +
claim-strip + body sections + nav). Body text is English-only (VP-SPEC C0).

This chapter applies the SAME threshold-shift intervention logic that §30 (bipolar T2b-L) and §31
(epilepsy T2a-L) used, inherited from the analgesic reproducibility package
(Zenodo 10.5281/zenodo.20733420), to the TEMPORAL low-coordination pole that §27 (T1b) established —
and it is the FIRST case that is L3-DOMINANT rather than channel-led. §27 placed major depression as
the chronification of an operating point with R below health, driven by a sustained up-stream (HPA)
withdrawal; the corrective sign is "restore the deficient drive" (the mirror of the epilepsy/bipolar
"reduce the excess"), but §27 left that restoration as ONE abstract operator. This chapter decomposes
it into a DNA-grounded three-lever target map over eighteen depression genes, with twelve of the
eighteen sitting on L3. Seven promoter reads (NR3C1/CRHR1/GRIN2A/CACNA1C/KCNQ2/KCNQ3 from the bipolar
cache, GABRA1 from the epilepsy cache) are carried over VERBATIM (gamma is strand-symmetric). No new
mechanism, no new tuned constant; the engine is READ-ONLY. The numbers quoted in the prose are the
structural reads (gamma, |h_sp|) and the burden ranking from
repro/mind/_verify/depression_threshold_levers.py and depression_burden_prioritisation.py
(efficacy=0; targets ranked, never drugs or doses); the canonical numeric artifacts are those
modules' results.json files.

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

NO = 32
SLUG = "32-depression-threshold-levers"
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Depression threshold levers: the restore-the-operating-point sign, decomposed"
H1 = "Depression threshold levers &mdash; the low-coordination operating-point restoration, decomposed into three DNA-grounded levers (L3-dominant)"
CRUMB = "Depression: three threshold levers"
HEADLINE = ("The depression low-coordination operating-point restoration decomposed into a DNA-grounded "
            "three-lever target map: remove the upstream HPA drive and restore the deficient monoamine and "
            "neurotrophic drives (L3, the dominant lever), increase outward potassium / GABA-A current (L2), "
            "or modulate the inward glutamatergic / calcium current (L1), over eighteen depression genes")
META = ("Chapter 27 placed major depression as the chronification of a low-coordination operating point but "
        "treated the corrective restoration as one abstract operator. This chapter applies the same "
        "threshold-shift intervention logic used for bipolar disorder and epilepsy (inherited from the "
        "analgesic reproducibility package, Zenodo 10.5281/zenodo.20733420) and decomposes that restoration "
        "into three concrete levers -- remove the upstream HPA / restore the deficient monoamine and "
        "neurotrophic drives (L3, dominant here), increase outward potassium / GABA-A current (L2), modulate "
        "inward glutamatergic / calcium current (L1) -- over eighteen depression genes placed by their own "
        "promoter switch stiffness. The first L3-dominant case; the corrective sign is flipped (restore "
        "deficient, not reduce excess). Targets are ranked, never drugs or doses. efficacy=0; not medical advice.")

ABSTRACT = (
    "The <a href=\"/mind/27-depression-chronification/\">depression chapter</a> read major depression as "
    "the <strong>chronification of a low-coordination operating point</strong>: a sustained, HPA-driven "
    "withdrawal pulls the global order parameter <span class=\"mono\">R</span> <em>below</em> the band "
    "health lives in, and with plasticity that excursion writes a retained structural trace. That chapter "
    "proved the <em>pole</em> and the corrective <em>sign</em> &mdash; depression sits at the "
    "<strong>opposite pole from epilepsy</strong>, so the therapeutic push is whatever <strong>restores "
    "the deficient drive</strong> (or removes the chronic-stress drive that lowers the operating point) "
    "&mdash; but it left that push <em>abstract</em>: it said <em>restore coordination</em> without saying "
    "<strong>which genes or drives actually realise the restoration</strong>. This chapter fills exactly "
    "that gap, with the <strong>same piece of inherited technology</strong> the "
    "<a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a> and "
    "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a> levers chapters used: the "
    "<strong>threshold-shift intervention logic</strong> from the analgesic reproducibility package "
    "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>). Its three "
    "abstract levers &mdash; <strong>L1</strong> change the inward (excitatory) current, "
    "<strong>L2</strong> change the outward (potassium / inhibitory) current, <strong>L3</strong> change "
    "the up-stream drive &mdash; carry over unchanged, but depression is where the frame's "
    "<strong>generality is genuinely tested</strong>, because it is the <strong>first L3-dominant "
    "case</strong>: of <strong>eighteen</strong> depression genes, <strong>twelve</strong> sit on L3, and "
    "only three each on the channel levers. The L3 set splits into three sub-axes &mdash; the "
    "<strong>HPA-removal</strong> trio (<span class=\"mono\">NR3C1</span>, <span class=\"mono\">CRHR1</span>, "
    "<span class=\"mono\">FKBP5</span>), the <strong>monoamine-restoration</strong> set "
    "(<span class=\"mono\">SLC6A4</span>, <span class=\"mono\">SLC6A2</span>, <span class=\"mono\">MAOA</span>, "
    "<span class=\"mono\">TPH2</span>, <span class=\"mono\">HTR1A</span>, <span class=\"mono\">HTR2A</span>, "
    "<span class=\"mono\">COMT</span>), and the <strong>neurotrophic-restoration</strong> pair "
    "(<span class=\"mono\">BDNF</span>, <span class=\"mono\">NTRK2</span>) &mdash; while L1 carries the "
    "glutamatergic / calcium set (<span class=\"mono\">GRIN2A</span>, <span class=\"mono\">GRIN2B</span>, "
    "<span class=\"mono\">CACNA1C</span>) and L2 the outward set (<span class=\"mono\">KCNQ2</span>, "
    "<span class=\"mono\">KCNQ3</span>, <span class=\"mono\">GABRA1</span>). Each gene is placed by reading "
    "its <strong>own promoter switch stiffness</strong> &mdash; <span class=\"mono\">&gamma; = &minus;mean</span> "
    "nearest-neighbour stacking free energy (SantaLucia 1998) over its promoter window, turned into "
    "<span class=\"mono\">|h_sp| = spinodal(&gamma;)</span> with the frozen engine <strong>read-only</strong>, "
    "and seven of the reads (<span class=\"mono\">NR3C1</span>, <span class=\"mono\">CRHR1</span>, "
    "<span class=\"mono\">GRIN2A</span>, <span class=\"mono\">CACNA1C</span>, <span class=\"mono\">KCNQ2</span>, "
    "<span class=\"mono\">KCNQ3</span> from the bipolar cache, <span class=\"mono\">GABRA1</span> from the "
    "epilepsy cache) are carried over <strong>verbatim</strong>. Two honest caveats are recorded, not "
    "hidden: the L1 glutamatergic direction is an <strong>NMDA antagonist</strong> (the ketamine route) "
    "acting through <em>downstream</em> neurotrophic signalling, <strong>not</strong> an excitation "
    "reduction, so its naive L1 sign is flagged sign-subtle; and the <span class=\"mono\">HTR2A</span> "
    "direction is <strong>non-monotone</strong> (an agonist psychedelic route and an antagonist route both "
    "appear). Three fail-closed disciplines ride along: every L3 link stays graded "
    "<span class=\"mono\">[O]</span> cited biology, a forbidden-claim scanner rejects any dose / efficacy / "
    "safety / synthesis statement (including mood-lift and remission language), and a burden-weighted "
    "ranking orders <strong>targets, never drugs or doses</strong>. The <strong>firewall</strong> is "
    "absolute: the promoter <span class=\"mono\">|h_sp|</span> is a gene's own switch stiffness, "
    "<strong>never</strong> the §27 network operating-point on <span class=\"mono\">R</span>, a receptor "
    "occupancy, a synaptic monoamine level, a potency, a dose, or a clinical effect. "
    "<span class=\"mono\">efficacy = 0</span>; not medical advice; the hard problem stays open."
)


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


BODY = "\n\n".join([
    sec("What §27 left abstract", [
        "The <a href=\"/mind/27-depression-chronification/\">depression chapter</a> placed the disorder at "
        "the <strong>low-coordination operating point</strong> of the atlas, built on top of the E0 "
        "plasticity layer: health is a population of micro-eddies running in parallel at a moderate global "
        "coherence, and major depression is a <strong>sustained downward excursion</strong> of the order "
        "parameter <span class=\"mono\">R</span> &mdash; an HPA-driven withdrawal that holds the system "
        "below its healthy band &mdash; which plasticity then <em>consolidates</em> into a retained "
        "structural trace (the chronification). That chapter proved two things and stopped: the "
        "<em>pole</em> (depression is the under-coordination side, the mirror of the over-synchronisation "
        "disorders) and the corrective <em>sign</em> (the therapeutic push is whatever <strong>restores "
        "the deficient drive</strong> or <strong>removes the chronic-stress drive</strong> that lowers the "
        "operating point). That sign is forced and honest, but it describes the intervention as a "
        "<em>single abstract operator</em>: <q>restore coordination.</q> It does not say <strong>through "
        "what physical drive</strong> the restoration is realised &mdash; which axis, which receptor, which "
        "gene. A mechanism atlas should be able to say more than <em>something restores the operating "
        "point</em>; it should enumerate the <strong>ways</strong> an operating point can be lifted and "
        "attach real molecular targets to each. The bipolar and epilepsy chapters showed that this "
        "enumeration is exactly what the inherited threshold-shift technology supplies &mdash; and "
        "depression is where that technology is <em>most</em> tested, because here the answer is not a "
        "channel at all."
    ]),
    sec("The inherited technology, applied a third time &mdash; and the first L3-dominant case", [
        "The handle is not invented here, and it is not adapted here &mdash; it is the <em>same</em> logic "
        "the <a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a> and "
        "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a> chapters inherited from the "
        "<strong>analgesic reproducibility package</strong> "
        "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>), now turned "
        "on a third disorder. Its premise is general: an operating point is set by a balance of currents "
        "and the drives that bias them, so there are exactly <strong>three levers</strong> on it. "
        "<strong>L1</strong> &mdash; <em>change the inward, excitatory current</em>. <strong>L2</strong> "
        "&mdash; <em>change the outward, repolarising (or inhibitory) current</em>. <strong>L3</strong> "
        "&mdash; <em>change the up-stream drive</em> that sets where the operating point sits in the first "
        "place. The frame applies unchanged because the depression chapter, the bipolar chapter, the "
        "epilepsy chapter, and the analgesic package all share the <strong>same R19 substrate</strong> "
        "&mdash; the engine's supercritical pitchfork <span class=\"mono\">&#7779; = g&middot;s &minus; "
        "s&sup3; + h</span>, whose spinodal fold IS the switching barrier.",
        "Depression makes two things vivid that the channel-led disorders did not. The first is a "
        "<strong>sign flip at the disorder level</strong>, and the model states it rather than smoothing "
        "it away: epilepsy and bipolar mania sit <em>above</em> health (the lever sign is <em>reduce the "
        "excess</em> drive), but depression sits <em>below</em> health, so the corrective sign is the "
        "<strong>mirror</strong> &mdash; <em>restore the deficient drive</em>, or remove the chronic "
        "withdrawal drive that is holding the operating point down. The three abstract levers carry over "
        "intact; what flips is their <em>direction</em>. The second is a shift of <strong>distribution</strong>. "
        "Where bipolar leaned on L1 (its replicated GWAS loci are calcium channels) and epilepsy leaned on "
        "L2 (the <span class=\"mono\">KCNQ2</span>/<span class=\"mono\">KCNQ3</span> M-current), depression "
        "is the first case that is <strong>L3-dominant</strong>: of the eighteen genes, <strong>twelve "
        "sit on L3</strong> &mdash; the up-stream HPA, monoamine, and neurotrophic drives &mdash; and only "
        "three each on the channel levers. This is the frame's generality genuinely exercised: the "
        "<em>same</em> three levers re-distribute onto up-stream biology when that is where the disorder "
        "lives, instead of forcing depression into a channel mould it does not fit. The pipeline is reused "
        "at the level of code, not analogy: <strong>seven</strong> of the reads &mdash; "
        "<span class=\"mono\">NR3C1</span>, <span class=\"mono\">CRHR1</span>, <span class=\"mono\">GRIN2A</span>, "
        "<span class=\"mono\">CACNA1C</span>, <span class=\"mono\">KCNQ2</span>, <span class=\"mono\">KCNQ3</span> "
        "from the bipolar cache and <span class=\"mono\">GABRA1</span> from the epilepsy cache &mdash; are "
        "carried over <strong>verbatim</strong>, because <span class=\"mono\">&gamma;</span> is a "
        "strand-symmetric property of the sequence and does not change between problems. Nothing about the "
        "engine is touched; the module re-emerges the frozen tree read-only and confirms it byte-unchanged, "
        "and registers as the <strong>tenth atlas citizen</strong> (<span class=\"mono\">DEP-T1b-L</span>)."
    ]),
    sec("L3 (dominant) &mdash; remove the upstream drive and restore the deficient drives", [
        "The dominant lever in depression does not touch a channel; it changes the <em>up-stream drive</em> "
        "that sets the operating point. Twelve of the eighteen genes sit here, and they split cleanly into "
        "<strong>three sub-axes</strong> that map onto the three great families of antidepressant "
        "mechanism. The first sub-axis is <strong>HPA removal</strong> &mdash; turning down the chronic "
        "stress drive that holds <span class=\"mono\">R</span> below health. Three genes anchor it: "
        "<span class=\"mono\">NR3C1</span> (the glucocorticoid receptor; the mechanism direction is to "
        "<em>restore</em> its negative feedback, so the stress hyperdrive that lowers the operating point "
        "is removed), <span class=\"mono\">CRHR1</span> (the CRH receptor that initiates the axis), and "
        "<span class=\"mono\">FKBP5</span> (the co-chaperone that tunes glucocorticoid-receptor "
        "sensitivity, one of the most-replicated stress-interaction loci in psychiatric genetics). The "
        "second sub-axis is <strong>monoamine restoration</strong> &mdash; lifting the deficient "
        "serotonergic and noradrenergic drive, which is the classical antidepressant target. Seven genes "
        "carry it: the transporters <span class=\"mono\">SLC6A4</span> (the serotonin transporter, the SSRI "
        "site) and <span class=\"mono\">SLC6A2</span> (the noradrenaline transporter, the SNRI site); the "
        "catabolic enzymes <span class=\"mono\">MAOA</span> (monoamine oxidase A, the MAOI site) and "
        "<span class=\"mono\">COMT</span> (catechol-O-methyltransferase); the synthetic enzyme "
        "<span class=\"mono\">TPH2</span> (neuronal tryptophan hydroxylase, the rate-limiter of serotonin "
        "synthesis); and the receptors <span class=\"mono\">HTR1A</span> and <span class=\"mono\">HTR2A</span>. "
        "The third sub-axis is <strong>neurotrophic restoration</strong> &mdash; rebuilding the "
        "plasticity drive that lets a chronified operating point un-write. Two genes anchor it: "
        "<span class=\"mono\">BDNF</span> (brain-derived neurotrophic factor) and its receptor "
        "<span class=\"mono\">NTRK2</span> (TrkB). This last pair matters out of proportion to its size, "
        "because it is the <strong>convergence point</strong>: the rapid-acting glutamatergic route and the "
        "slow monoamine route both appear to lift the operating point <em>through</em> downstream BDNF / "
        "TrkB signalling, which is why neurotrophic restoration tops the priority ranking below.",
        "This is the lever that demands the most discipline, and it gets it. Every L3 link is held at grade "
        "<span class=\"mono\">[O]</span> &mdash; <strong>open, cited biology, never derived from the "
        "substrate</strong>. The model does <em>not</em> claim to compute that the HPA axis or BDNF sets "
        "the network operating point; it records, as cited upstream biology, that these are the drives "
        "whose restoration (or, for the stress axis, removal) would lift it. A <strong>fail-closed "
        "L3-honesty gate</strong> enforces exactly this: it checks that the declared twelve-gene L3 set is "
        "present, that each member is graded <span class=\"mono\">[O]</span> and carries no current-channel "
        "mislabelling, that the firewall sentence separating the promoter <span class=\"mono\">|h_sp|</span> "
        "from the §27 network operating-point is present, and &mdash; the check unique to this chapter "
        "&mdash; that L3 is genuinely <strong>dominant</strong> (more L3 members than L1 or L2). It FAILS "
        "the build if any of these slips. And the <span class=\"mono\">HTR2A</span> entry carries the "
        "chapter's <strong>second honest caveat</strong> openly: its direction is <strong>non-monotone</strong> "
        "&mdash; both an <em>agonist</em> route (the serotonergic-psychedelic direction) and an "
        "<em>antagonist</em> route (the direction shared with several sedating antidepressants) appear in "
        "the literature, so a single signed lever cannot capture it, and the model records the ambiguity "
        "rather than picking a side. A direction, never a dose &mdash; <span class=\"mono\">efficacy = 0</span>."
    ]),
    sec("L1 &mdash; the inward glutamatergic / calcium levers (and the ketamine subtlety)", [
        "The first channel lever is <em>minor</em> in depression &mdash; three genes &mdash; but it carries "
        "the chapter's <strong>first and most important honest caveat</strong>. "
        "<span class=\"mono\">GRIN2A</span> and <span class=\"mono\">GRIN2B</span> are NMDA-receptor "
        "subunits (the GluN2A and GluN2B glutamatergic, calcium-permeable channels), and "
        "<span class=\"mono\">CACNA1C</span> is the L-type calcium channel Ca<sub>V</sub>1.2 (the same "
        "top-replicated cross-disorder locus that anchored the bipolar L1). The naive reading of L1 would "
        "be <em>reduce inward excitatory current</em> &mdash; but in depression the most important "
        "glutamatergic agent, <strong>ketamine</strong> (and esketamine), is an NMDA "
        "<strong>antagonist</strong>, and its rapid antidepressant direction is <em>not</em> a simple "
        "excitation reduction. The current understanding is that NMDA antagonism on inhibitory interneurons "
        "produces a downstream <em>disinhibition</em> and a surge of <strong>BDNF / TrkB</strong> "
        "signalling &mdash; i.e. the L1 agent acts by lifting the <em>L3 neurotrophic drive</em>, not by "
        "quieting excitation at the operating point. The model flags this explicitly as a "
        "<strong>sign-subtle</strong> entry: the lever placement (the gene is on the inward-current lever) "
        "is structural and trait-blind, but the <em>direction</em> of the clinically relevant agent runs "
        "through a downstream route and is gene-, dose-, and mechanism-specific, and stays graded "
        "<span class=\"mono\">[O]</span>. This is exactly the case the firewall exists for: a promoter read "
        "places a gene on a lever; it says <strong>nothing</strong> about whether an agonist or an "
        "antagonist is the therapeutic direction. A direction, never a dose."
    ]),
    sec("L2 &mdash; the outward potassium / GABA-A levers", [
        "The second channel lever is also <em>minor</em> in depression &mdash; three genes &mdash; and it "
        "is the direct mirror of the inward levers: strengthen the outward, restoring side. "
        "<span class=\"mono\">KCNQ2</span> and <span class=\"mono\">KCNQ3</span> are the neuronal "
        "<strong>M-current</strong> pair (K<sub>V</sub>7.2 / K<sub>V</sub>7.3) &mdash; the same channels "
        "that were the <em>dominant</em> lever in epilepsy &mdash; and here a K<sub>V</sub>7 opener has "
        "been studied (exploratory) for the reward / anhedonia dimension of depression, so the gene is "
        "carried as a minor lever with its promoter read reused verbatim from the bipolar / epilepsy "
        "caches. <span class=\"mono\">GABRA1</span> (the GABA&#8209;A &alpha;1 subunit, its read reused "
        "from the epilepsy cache) rides <strong>L2-adjacent</strong>: it carries no potassium current, but "
        "it raises the same restoring side through inhibitory chloride conductance &mdash; the same L2 "
        "<em>logic</em> realised through a different ion. The contrast with epilepsy is the whole point of "
        "the distribution finding: the identical <span class=\"mono\">KCNQ2</span>/"
        "<span class=\"mono\">KCNQ3</span> channels that <em>dominate</em> the epilepsy map sit at the "
        "<em>periphery</em> of the depression map, because depression's centre of gravity is up-stream, "
        "not at the firing threshold. Every claim on this lever is a <strong>mechanism direction "
        "only</strong>; no opener, blocker, dose, or patient is named."
    ]),
    sec("The DNA grounding: a promoter's own switch stiffness", [
        "What places each of the eighteen genes is not a list but a <strong>read</strong>. For every gene, "
        "the module takes its promoter window (transcription start &minus;2000 to +500 bases, "
        "<em>Homo sapiens</em>) and computes <span class=\"mono\">&gamma; = &minus;mean</span> of the "
        "nearest-neighbour base-stacking free energies along that window (the SantaLucia 1998 "
        "nearest-neighbour thermodynamics), then turns that <span class=\"mono\">&gamma;</span> into the "
        "promoter's switch stiffness through the <em>frozen engine's own</em> functions: "
        "<span class=\"mono\">|h_sp| = spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></span> and "
        "<span class=\"mono\">barrier = &gamma;&sup2;/4</span>. The reads span a real range &mdash; the "
        "stiffest promoter in the set is <span class=\"mono\">KCNQ2</span> at "
        "<span class=\"mono\">&gamma; &approx; 1.58</span> (<span class=\"mono\">|h_sp| &approx; 0.76</span>), "
        "closely followed by the HPA-axis gene <span class=\"mono\">CRHR1</span> "
        "(<span class=\"mono\">&gamma; &approx; 1.56</span>, <span class=\"mono\">|h_sp| &approx; 0.75</span>) "
        "and the serotonin transporter <span class=\"mono\">SLC6A4</span> "
        "(<span class=\"mono\">&gamma; &approx; 1.52</span>, <span class=\"mono\">|h_sp| &approx; 0.72</span>); "
        "the softest is <span class=\"mono\">GABRA1</span> at <span class=\"mono\">&gamma; &approx; 1.25</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.54</span>), with the glucocorticoid receptor "
        "<span class=\"mono\">NR3C1</span> also near the soft end "
        "(<span class=\"mono\">&gamma; &approx; 1.26</span>, <span class=\"mono\">|h_sp| &approx; 0.55</span>), "
        "and the neurotrophic gene <span class=\"mono\">BDNF</span> reading mid-range "
        "(<span class=\"mono\">&gamma; &approx; 1.43</span>, <span class=\"mono\">|h_sp| &approx; 0.66</span>). "
        "These are read on the <strong>same R19 substrate, with the same engine, that the bipolar, "
        "epilepsy, and analgesic packages used</strong>, which is the whole point of the inheritance: one "
        "substrate, one pipeline, now four problems. The <span class=\"mono\">&gamma;</span> read is a "
        "property of the gene's <strong>promoter sequence</strong>, blind to whether the gene is on or off "
        "and to gain / loss / expression level, and that is <em>all</em> it is."
    ]),
    sec("Ranking targets, and the firewall that keeps gamma honest", [
        "The last component prioritises, and it prioritises <strong>targets, never drugs or doses</strong>. "
        "A burden-weighted score combines three declared, cited weights &mdash; clinical burden "
        "(<span class=\"mono\">0.40</span>), unmet need (<span class=\"mono\">0.35</span>), and "
        "genetic-evidence / druggability (<span class=\"mono\">0.25</span>) &mdash; on cited 1&ndash;5 "
        "tiers, and ranks the genes by that score alone. The top actionable target is <span class=\"mono\">"
        "BDNF</span> &mdash; the neurotrophic convergence point where the rapid-acting and monoamine routes "
        "meet, maximal on every tier &mdash; followed by the HPA gene <span class=\"mono\">FKBP5</span>, "
        "the glutamatergic <span class=\"mono\">GRIN2B</span>, and the glucocorticoid receptor "
        "<span class=\"mono\">NR3C1</span>; a substantive consequence of the unmet-need weight is that it "
        "lifts these up-stream HPA / neurotrophic / glutamate targets <em>above</em> the high-burden but "
        "well-served monoamine transporters such as <span class=\"mono\">SLC6A4</span>. The three channel "
        "genes <span class=\"mono\">KCNQ2</span>, <span class=\"mono\">KCNQ3</span>, and "
        "<span class=\"mono\">CACNA1C</span> are flagged <strong>not actionable by the generic lever "
        "sign</strong> in depression, carrying their exploratory / indirect status right in the ranking. "
        "Crucially, the <span class=\"mono\">&gamma;</span> read is carried <em>alongside</em> each target "
        "as structural context but is <strong>never folded into the score</strong> &mdash; and the result "
        "is a clean demonstration of the firewall: the priority ranking and the "
        "<span class=\"mono\">&gamma; / |h_sp|</span> ranking are <strong>decoupled</strong>. The "
        "<strong>stiffest</strong> promoter read in the whole set, <span class=\"mono\">KCNQ2</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.76</span>), is a <em>minor, exploratory</em> L2 lever and "
        "sits near the <strong>bottom</strong> of priority; the <strong>top-priority</strong> target "
        "<span class=\"mono\">BDNF</span> has only a <em>mid-range</em> read "
        "(<span class=\"mono\">|h_sp| &approx; 0.66</span>). If promoter stiffness drove the ranking, "
        "neither could sit where it does. That decoupling is the firewall made visible, and it must be "
        "stated once more in full: the promoter <span class=\"mono\">|h_sp|</span> is a gene's "
        "<strong>own switch stiffness</strong>, and it is <strong>never</strong> equated with the §27 "
        "network operating-point on <span class=\"mono\">R</span>, nor with a receptor occupancy, a "
        "synaptic monoamine level, a compound's potency, a dose, an in-vivo selectivity, or any clinical "
        "effect. A <strong>fail-closed forbidden-claim scanner</strong> guards the whole package: it scans "
        "the written results for any dose, efficacy-as-fact, safety-as-fact, or synthesis statement &mdash; "
        "including <em>lifts mood</em>, <em>remission</em>, <em>relapse-prevention</em>, and "
        "<em>antidepressant-efficacy</em> language &mdash; carries a negation guard, and includes a "
        "planted self-test that <em>must</em> fire on its own bait, failing the build if it ever does not. "
        "This module reproduces bit-for-bit with the engine byte-unchanged.",
        "Everything here is an in-silico <em>reading</em> of promoter sequence and a <em>frame</em> for "
        "organising targets, not a clinical measure, a diagnosis, or a prescription. The model asserts "
        "<em>mechanism directions and target placements</em> &mdash; an operating point can be lifted three "
        "ways; these eighteen genes populate the three levers; depression loads them up-stream "
        "(L3-dominant); these targets carry the highest genetic and unmet-need burden &mdash; and "
        "<strong>nothing</strong> about which agent acts on any lever, at what dose, in whom, whether any "
        "real drug lifts anyone's mood, or that anyone should change a treatment. The agents named as "
        "<em>directions</em> (the SSRIs / SNRIs / MAOIs on the monoamine sub-axis, the glucocorticoid and "
        "CRH routes on the HPA sub-axis, the ketamine route flagged sign-subtle on L1, the M-current "
        "opener on L2) are illustrations of a <em>sign</em>, never a recommendation &mdash; and the two "
        "recorded caveats (the downstream-BDNF route of the L1 NMDA antagonist, the non-monotone "
        "<span class=\"mono\">HTR2A</span> direction) are there precisely because a generic lever sign is "
        "<strong>not</strong> a clinical direction. Real depression is heterogeneous &mdash; melancholic, "
        "atypical, psychotic, peripartum, seasonal, and bipolar depression; monoaminergic, HPA, "
        "inflammatory, circadian, and psychosocial contributors; roughly a third treatment-resistant "
        "&mdash; and that heterogeneity is <strong>locked</strong>. A promoter read and a lever assignment "
        "are mechanism boundaries, <strong>not</strong> a claim about the felt quality of depression or "
        "its lifting (Axis-A firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>, the hard "
        "problem stays <strong>open</strong>). <strong>This is not medical advice, not a diagnosis, not a "
        "treatment protocol, and not a cure.</strong> <span class=\"mono\">medium_efficacy_tested = 0</span>; "
        "targets ranked, never drugs or doses."
    ]),
])

PREV = '<a rel="prev" href="/mind/31-epilepsy-threshold-levers/">&larr; §31 Epilepsy: three threshold levers</a>'
NEXT = '<a rel="next" href="/mind/33-schizophrenia-threshold-levers/">§33 Schizophrenia: three threshold levers &rarr;</a>'

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
  <a href="{GH}/32-depression-threshold-levers/" rel="noopener">reproduce (GitHub)</a>
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
