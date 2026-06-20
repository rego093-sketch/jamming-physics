#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch35_adhd_levers.py — emit the §35 ADHD threshold-levers chapter (roadmap ADHD-T-L).

Writes docs/mind/35-adhd-threshold-levers/index.html using the same head/JSON-LD/footer
scaffolding as the other Part-II chapters so the SEO markup is byte-consistent. The answer-first
<p class="answer"> and the vp-card asides are NOT written here — build_search_layer.py injects them
from mind_registry.py (single source of truth): this generator only emits the skeleton (abstract +
claim-strip + body sections + nav). Body text is English-only (VP-SPEC C0).

This chapter applies the SAME threshold-shift intervention logic that §30 (bipolar T2b-L), §31
(epilepsy T2a-L), §32 (depression T1b-L), §33 (schizophrenia T1a-L) and §34 (autism ASD-T-L) used,
inherited from the analgesic reproducibility package (Zenodo 10.5281/zenodo.20733420), to the §22
adhd_axis_specific substrate — and it is the FIRST PARTIAL [L] fit in the series. §22 placed ADHD as
a gain/arousal disorder with INTACT WIRING (six output/gain genes, two arousal/threshold genes, zero
wiring genes; axis-ambiguous/syndromic genes pre-registered out). Mapped onto the threshold frame by
REACHABILITY, ADHD loads ALL its engagement on L3 (the up-stream catecholamine/monoaminergic drive):
five drive-tone levers, with L1 and L2 BOTH EMPTY — the sixth distribution pattern and the purest L3
case. The fit is PARTIAL [L], not the clean [V] of the five prior disorders, because the DOMINANT
ADHD axis — GA, the §22-O gain-amplitude core (catecholamine SYNTHESIS, RELEASE, catabolic clearance)
— is OUT OF REACH of a drive-tone lever and is NAMED, not reached. And W (wiring) is ABSENT, the
discriminant from autism (which carried a W axis §19-PROVEN unreachable). Nine promoter reads place
the five levers and the four out-of-reach gain genes; six are carried VERBATIM from the depression /
schizophrenia caches (gamma is strand-symmetric), and ADRA2A / DBH / SNAP25 are live GRCh38
strand-aware reads. No new mechanism, no new tuned constant; the engine is READ-ONLY. The numbers
quoted in the prose are the structural reads (gamma, |h_sp|) and the burden ranking from
repro/mind/_verify/adhd_threshold_levers.py and adhd_burden_prioritisation.py (efficacy=0; targets
ranked, never drugs or doses; no stimulant-misuse or cognitive-enhancement licence); the canonical
numeric artifacts are those modules' results.json files.

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

SLUG = "35-adhd-threshold-levers"
NO = 35
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "ADHD threshold levers: the drive-tone axis, decomposed (L3-only; the gain-amplitude core out of reach — the first partial fit)"
H1 = ("ADHD threshold levers &mdash; the drive-tone / arousal operating-point correction, decomposed into "
      "DNA-grounded levers (L3-only; the gain-amplitude core named, out of reach &mdash; the first PARTIAL fit "
      "in the series)")
CRUMB = "ADHD: drive-tone levers (partial fit)"
HEADLINE = ("The ADHD drive-tone / arousal operating-point correction decomposed into a DNA-grounded lever map "
            "that loads entirely on the up-stream drive lever (L3) &mdash; five drive-tone genes &mdash; with the "
            "inward-current and outward-current levers (L1, L2) both EMPTY: the map reaches the secondary "
            "drive-tone axis only, while the DOMINANT gain-amplitude axis (catecholamine synthesis, release and "
            "clearance) is named but out of reach, and the long-range-wiring axis is absent (intact wiring), "
            "making ADHD the first PARTIAL fit in the threshold-levers series")
META = ("Chapter 22 placed ADHD as a gain/arousal disorder with intact wiring &mdash; six output/gain genes, two "
        "arousal/threshold genes, zero wiring genes &mdash; the discriminant from autism. This chapter applies "
        "the same threshold-shift intervention logic used for bipolar disorder, epilepsy, depression, "
        "schizophrenia and autism (inherited from the analgesic reproducibility package, Zenodo "
        "10.5281/zenodo.20733420) and finds ADHD loads its entire threshold-frame engagement on the up-stream "
        "drive lever (L3): five drive-tone levers (the dopamine, noradrenaline and serotonin transporters, the "
        "alpha-2A and D4 receptors), with the inward-current (L1) and outward-current (L2) levers both empty. "
        "The fit is partial, not clean, because the dominant ADHD axis -- the gain-amplitude core of catecholamine "
        "synthesis, release and clearance -- is out of reach of a drive-tone lever and is named, not reached; and "
        "the wiring axis is absent. Targets are ranked, never drugs or doses. efficacy=0; not medical advice; no "
        "stimulant-misuse or cognitive-enhancement claim.")

ABSTRACT = (
    "The <a href=\"/mind/22-adhd-vs-autism/\">ADHD-vs-autism chapter</a> read ADHD not as a milder autism but as a "
    "<strong>different kind of fault entirely</strong>: a disorder of <strong>gain and arousal</strong> with the "
    "long-range <strong>wiring left intact</strong>. That intact wiring is the <em>discriminant</em> &mdash; it is "
    "what separates ADHD from autism, where a long-range connectivity axis was not only present but "
    "<a href=\"/mind/19-autism-chemical-limits/\">§19-proven unreachable</a>. §22 grounded ADHD in an explicit "
    "gene substrate: a <strong>gain-amplitude (output) core</strong> &mdash; the catecholamine machinery that sets "
    "<em>how much</em> signal is made, released and cleared &mdash; and a smaller <strong>arousal / drive-tone</strong> "
    "set that sets <em>where the firing level sits</em>, with <strong>zero</strong> wiring genes and the "
    "axis-ambiguous / syndromic genes pre-registered <em>out</em>. This chapter applies the <strong>same piece of "
    "inherited technology</strong> the <a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a>, "
    "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a>, "
    "<a href=\"/mind/32-depression-threshold-levers/\">depression</a>, "
    "<a href=\"/mind/33-schizophrenia-threshold-levers/\">schizophrenia</a> and "
    "<a href=\"/mind/34-autism-threshold-levers/\">autism</a> levers chapters used &mdash; the "
    "<strong>threshold-shift intervention logic</strong> from the analgesic reproducibility package "
    "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>), whose three abstract "
    "levers are <strong>L1</strong> change the inward (excitatory) current, <strong>L2</strong> change the outward "
    "(potassium / inhibitory) current, <strong>L3</strong> change the up-stream drive &mdash; and it produces the "
    "<strong>first PARTIAL fit in the whole series</strong>. ADHD is the <strong>sixth distribution pattern</strong>, "
    "and the most lopsided: it is <strong>L3-only</strong>. Of <strong>five</strong> lever genes, <strong>all five</strong> "
    "sit on the up-stream drive lever (L3: <span class=\"mono\">SLC6A3</span> the dopamine transporter, "
    "<span class=\"mono\">SLC6A2</span> the noradrenaline transporter, <span class=\"mono\">SLC6A4</span> the serotonin "
    "transporter, <span class=\"mono\">ADRA2A</span> the &alpha;<sub>2A</sub>-adrenergic receptor, and "
    "<span class=\"mono\">DRD4</span> the D<sub>4</sub> dopamine receptor) &mdash; and <strong>L1 and L2 are both "
    "EMPTY</strong>. That emptiness is itself the finding: ADHD is <strong>not a channelopathy</strong>; it has no "
    "ionic fold lever at all, only the <span class=\"mono\">[O]</span> cited-biology drive surface where the stimulant, "
    "atomoxetine and guanfacine arms live (as <em>directions</em>, never doses). The fit is <strong>partial</strong> "
    "for a precise, two-sided reason. First, the <strong>dominant</strong> ADHD axis is <em>out of reach</em>: ADHD's "
    "core fault is the <strong>gain-amplitude</strong> axis &mdash; the catecholamine <strong>synthesis</strong> "
    "(<span class=\"mono\">TH</span>, <span class=\"mono\">DBH</span>), <strong>release</strong> "
    "(<span class=\"mono\">SNAP25</span>) and catabolic <strong>clearance</strong> (<span class=\"mono\">COMT</span>, a "
    "boundary node) machinery that sets signal <em>amplitude</em> &mdash; and a drive-tone (reuptake / receptor) lever "
    "has <strong>no handle on synthesis or release</strong>. The threshold frame reaches ADHD only through its "
    "<em>secondary</em> drive-tone axis and <strong>misses the dominant gain core</strong>, which is <strong>named</strong> "
    "with four real genes (carried with their own promoter reads alongside) but <strong>not reached</strong>. Second, "
    "the frame has <strong>no structural <span class=\"mono\">[F]</span> grounding</strong> on ADHD at all &mdash; the "
    "<span class=\"mono\">[F]</span> ionic levers L1/L2 are empty, leaving only the <span class=\"mono\">[O]</span> "
    "drive surface. So the fit is graded <span class=\"mono\">[L]</span> <strong>partial</strong>, the first and only "
    "non-clean fit across six disorders &mdash; and the partial grade is the <em>finding</em>, marking exactly where "
    "the cross-cutting threshold logic does and does not apply, refusing to overclaim a clean fit where the biology is "
    "a gain/arousal disorder. This is the precise <strong>inverse of autism</strong>: autism reached its "
    "<em>dominant</em> excitability axis and missed the output and wiring axes; ADHD reaches only its "
    "<em>secondary</em> drive-tone axis and misses the <em>dominant</em> gain axis, with no wiring axis at all. Each "
    "gene is placed by reading its <strong>own promoter switch stiffness</strong> &mdash; "
    "<span class=\"mono\">&gamma; = &minus;mean</span> nearest-neighbour stacking free energy (SantaLucia 1998) over "
    "its promoter window, turned into <span class=\"mono\">|h_sp| = spinodal(&gamma;)</span> with the frozen engine "
    "<strong>read-only</strong> &mdash; and six of the nine reads (<span class=\"mono\">SLC6A3</span>, "
    "<span class=\"mono\">DRD4</span>, <span class=\"mono\">SLC6A4</span>, <span class=\"mono\">TH</span>, "
    "<span class=\"mono\">COMT</span> from the depression / schizophrenia caches) are carried over "
    "<strong>verbatim</strong>, with <span class=\"mono\">ADRA2A</span>, <span class=\"mono\">DBH</span> and "
    "<span class=\"mono\">SNAP25</span> live GRCh38 strand-aware reads. The DNA reads carry an inversion that names "
    "itself: the <strong>stiffest</strong> promoter in the set, the dopamine transporter "
    "<span class=\"mono\">SLC6A3</span>, is a <em>reachable</em> lever, while the <strong>softest</strong>, the SNARE "
    "release gene <span class=\"mono\">SNAP25</span>, is an <em>out-of-reach</em> gain gene &mdash; the exact opposite "
    "of autism, where the stiffest reads were the out-of-reach genes. Three fail-closed disciplines ride along, and "
    "the forbidden-claim scanner is the <strong>strictest in the series</strong>: beyond the usual dose / efficacy / "
    "safety / synthesis classes it adds &mdash; uniquely for this stimulant topic &mdash; a "
    "<strong>stimulant-misuse</strong> class (it rejects get-high / snort / euphoria / recreational / party-drug "
    "vocabulary) and a <strong>cognitive-enhancement</strong> class (it rejects smart-drug / study-drug / nootropic / "
    "limitless framing), both negation-guarded. The <strong>firewall</strong> is absolute: the promoter "
    "<span class=\"mono\">|h_sp|</span> is a gene's own switch stiffness, <strong>never</strong> a transporter "
    "occupancy, a synaptic catecholamine level, a stimulant's potency, a dose, or a clinical effect. "
    "<span class=\"mono\">efficacy = 0</span>; not medical advice; ADHD is a difference in regulation, not a deficit "
    "of worth; the hard problem stays open."
)

BODY = "\n".join([
    "<h2>What §22 established (gain and arousal, with the wiring left intact)</h2>",
    "".join([
        "<p>The <a href=\"/mind/22-adhd-vs-autism/\">ADHD-vs-autism chapter</a> did for ADHD what the autism "
        "chapters did for autism: it refused the single-dial picture and replaced it with a statement about "
        "<em>which kind</em> of fault ADHD is. Its result is sharp and it is the discriminant the whole of this "
        "chapter rests on: <strong>ADHD is a disorder of gain and arousal with the long-range wiring left "
        "intact</strong>. Two of those three words carry the load. <strong>Gain</strong> &mdash; the "
        "<em>amplitude</em> of catecholamine signalling, how much dopamine and noradrenaline is synthesised, "
        "released, and cleared &mdash; is the <strong>dominant</strong> ADHD axis. <strong>Arousal</strong> &mdash; "
        "the drive-tone, where the firing set-point sits &mdash; is a <em>secondary</em> axis. And "
        "<strong>intact wiring</strong> is the crucial negative: ADHD does <em>not</em> carry the long-range "
        "connectivity fault that defines autism's W axis. §22 grounded this in an explicit gene substrate: "
        "<strong>six output/gain genes</strong> (the catecholamine synthesis, release and clearance machinery), "
        "<strong>two arousal/threshold genes</strong> (the monoaminergic tone set), <strong>zero wiring genes</strong>, "
        "and the axis-ambiguous or syndromic genes &mdash; <span class=\"mono\">FOXP2</span> (a language-syndrome "
        "transcription factor) and <span class=\"mono\">ADGRL3</span> (an adhesion-GPCR that could smuggle a wiring "
        "fault) &mdash; pre-registered <strong>out</strong>, precisely so the &lsquo;intact wiring&rsquo; discriminant "
        "stays airtight.</p>",
        "<p>§22 also proved the behavioural consequence and stopped. The stimulant restores the ADHD gain axis to "
        "health &mdash; in both synchrony and &theta;&ndash;&gamma; coupling &mdash; where the <em>same</em> stimulant "
        "only partly reaches autism, and the dose-cap's long-range benefit is several times larger where wiring is "
        "broken; on a composite AuDHD substrate the stimulant fixes the gain axis and the cap the wiring axis without "
        "interference. But §22 left the <em>molecular handle</em> abstract. It said ADHD is a gain/arousal disorder "
        "and that a stimulant restores it; it did <em>not</em> resolve that restoration into concrete levers on the "
        "operating point, name the genes each lever touches, place those genes by their own DNA, or &mdash; the point "
        "that makes this the first partial fit &mdash; ask honestly whether the cross-cutting threshold-shift logic "
        "even <em>reaches</em> the dominant axis. A mechanism atlas should be able to say <em>which</em> molecular "
        "targets realise the reachable correction <strong>and</strong> be honest, by name, about the axis the lever "
        "frame cannot touch. That is exactly what this chapter does &mdash; and unlike the five chapters before it, "
        "the honest answer is that the frame catches the <em>secondary</em> axis and misses the <em>dominant</em> "
        "one.</p>",
    ]),

    "<h2>The inherited technology, applied a sixth time &mdash; and the L3-only pattern</h2>",
    "".join([
        "<p>The handle is not invented here. It is the <strong>same</strong> threshold-shift intervention logic the "
        "<a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a>, "
        "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a>, "
        "<a href=\"/mind/32-depression-threshold-levers/\">depression</a>, "
        "<a href=\"/mind/33-schizophrenia-threshold-levers/\">schizophrenia</a> and "
        "<a href=\"/mind/34-autism-threshold-levers/\">autism</a> chapters inherited from the <strong>analgesic "
        "reproducibility package</strong> (<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI +
        "</a>). Its premise is general: an operating point is set by a balance of currents and the drives that bias "
        "them, so there are exactly <strong>three levers</strong> on it. <strong>L1</strong> &mdash; <em>change the "
        "inward, excitatory current</em>. <strong>L2</strong> &mdash; <em>change the outward, repolarising (or "
        "inhibitory) current</em>. <strong>L3</strong> &mdash; <em>change the up-stream drive</em> that sets where the "
        "operating point sits. The frame applies unchanged because the ADHD substrate, the five levers chapters, and "
        "the analgesic package all share the <strong>same R19 substrate</strong> &mdash; the engine's supercritical "
        "pitchfork <span class=\"mono\">&#7779; = g&middot;s &minus; s&sup3; + h</span>, whose spinodal fold IS the "
        "switching barrier. Nothing about the engine is touched; the module re-emerges the frozen tree read-only, "
        "confirms it byte-unchanged, and registers as the <strong>thirteenth atlas citizen</strong> "
        "(<span class=\"mono\">ADHD-T-L</span>).</p>",
        "<p>ADHD is the <strong>sixth distribution pattern</strong> across the series, and by far the most lopsided. "
        "Where bipolar leaned on L1 (calcium channels), epilepsy on L1&plus;L2 (the "
        "<span class=\"mono\">KCNQ2</span>/<span class=\"mono\">KCNQ3</span> M-current), depression on L3 (the "
        "up-stream HPA / monoamine / neurotrophic drives, L3-dominant but with a reachable L1/L2 mix), schizophrenia "
        "on L1&plus;L3 co-dominantly, and autism on L1-dominant with a sparse L3, ADHD is <strong>L3-only</strong>: of "
        "the five lever genes, <strong>all five sit on L3</strong>, and <strong>L1 and L2 are both empty</strong>. "
        "This is the <strong>purest L3 case</strong> in the atlas, and the emptiness of L1 and L2 is not a gap in the "
        "search &mdash; it is a <em>structural fact</em>. ADHD's actionable biology is the <strong>up-stream "
        "catecholamine and monoaminergic drive</strong>: the reuptake transporters and the tone receptors, exactly "
        "where ADHD pharmacology lives. There is <strong>no ionic fold lever</strong> &mdash; no channel whose inward "
        "or outward current you would change to raise or lower a firing threshold &mdash; because ADHD is "
        "<strong>not a channelopathy</strong>. The pipeline is reused at the level of code, not analogy: "
        "<strong>six</strong> of the nine reads &mdash; <span class=\"mono\">SLC6A3</span>, "
        "<span class=\"mono\">DRD4</span>, <span class=\"mono\">SLC6A4</span> on the lever side and "
        "<span class=\"mono\">TH</span>, <span class=\"mono\">COMT</span> on the out-of-reach side (and "
        "<span class=\"mono\">SLC6A4</span> again) &mdash; are carried over <strong>verbatim</strong> from the "
        "depression and schizophrenia caches, because <span class=\"mono\">&gamma;</span> is a strand-symmetric "
        "property of the sequence and does not change between problems; only <span class=\"mono\">ADRA2A</span>, "
        "<span class=\"mono\">DBH</span> and <span class=\"mono\">SNAP25</span> are fetched fresh (GRCh38, "
        "strand-aware).</p>",
    ]),

    "<h2>The first partial fit: why the dominant axis is out of reach (and the discriminant that wiring is absent)</h2>",
    "".join([
        "<p>This is the result that makes ADHD the most structurally <em>honest</em> chapter in the levers series, "
        "and the first that does not produce a clean fit. The five chapters before it produced clean "
        "<span class=\"mono\">[V]</span> fits: bipolar, epilepsy and depression mapped fully onto the frame, and "
        "schizophrenia and autism were domain-restricted but <em>exact on the axes they reached</em>. ADHD is "
        "different, and the module says so in a <strong>partial-fit witness</strong> that grades the fit "
        "<span class=\"mono\">[L] partial</span>. The reason is two-sided. The first and decisive sense: the "
        "<strong>dominant</strong> ADHD axis is <em>out of reach</em>. ADHD is a <strong>gain / arousal</strong> "
        "disorder, not a firing-<em>fold</em> disorder. The threshold-shift frame operates on the fold via an "
        "up-stream <strong>drive</strong> lever (L3), so it reaches ADHD only through the <strong>drive-tone "
        "surface</strong> &mdash; the reuptake transporters and tone receptors, the <em>secondary</em> axis &mdash; "
        "and <strong>not</strong> through the <strong>gain-amplitude machinery</strong> (synthesis and release), which "
        "is the <em>dominant</em> fault. A reuptake / receptor lever has no handle on how much transmitter is "
        "<em>made</em> or <em>released</em>; it can only modulate the <em>tone</em> of what is already there. So the "
        "frame catches the secondary set-point but not the dominant gain core, and the fit is partial. The second "
        "sense: even on the reachable side, the frame has <strong>no structural <span class=\"mono\">[F]</span> "
        "grounding</strong> on ADHD &mdash; the <span class=\"mono\">[F]</span> ionic levers L1 and L2 are empty, "
        "leaving only the <span class=\"mono\">[O]</span> cited-biology drive surface. Either way the conclusion is "
        "the same: <span class=\"mono\">[L]</span>, not <span class=\"mono\">[V]</span>. The partial grade is the "
        "<strong>finding</strong>, not a failure &mdash; it marks exactly where the cross-cutting threshold logic does "
        "and does not apply, and it refuses to manufacture a clean fit on a biology that is fundamentally about "
        "amplitude rather than threshold.</p>",
        "<p>The second strengthening is the <strong>discriminant</strong>, and it is the cleanest way to state what "
        "separates ADHD from autism. ADHD's <strong>wiring axis is absent</strong>. Where autism carried a long-range "
        "W axis that was not only present but <a href=\"/mind/19-autism-chemical-limits/\">§19-proven unreachable</a>, "
        "ADHD has <strong>zero wiring genes</strong> &mdash; the module records "
        "<span class=\"mono\">W: present_in_disorder = false, named_genes = []</span>. ADHD has <strong>intact "
        "wiring</strong>; there is no connectivity fault to name, reach, or fail to reach. This is the precise "
        "<strong>inverse of autism</strong>, and the module spells the inversion out: autism's lever map "
        "<em>reached its dominant axis</em> (excitability) and missed the output and wiring axes; ADHD's lever map "
        "<em>reaches only its secondary axis</em> (drive-tone) and misses the dominant gain axis, with no wiring axis "
        "at all. Autism was a clean fit that was domain-restricted; ADHD is the first partial fit, and the partiality "
        "lands on the <em>dominant</em> axis. The module captures all of this in a <strong>domain-restriction "
        "witness</strong> (DT = reached, GA = named but not reached, W = absent) and an "
        "<strong>out-of-reach-targets</strong> section that lists the four gain genes by name &mdash; making the "
        "partiality <em>concrete</em>, axis-structured and gene-named rather than a vague hedge, which is far more "
        "informative than a map that pretended to cover the whole disorder.</p>",
    ]),

    "<h2>L3 is the whole map &mdash; the five drive-tone levers (ADHD pharmacology as directions)</h2>",
    "".join([
        "<p>The entire reachable map is the <strong>up-stream drive lever</strong>, and it carries five genes &mdash; "
        "the transporters and receptors that set the <em>tone</em> of catecholamine and monoamine signalling. "
        "<span class=\"mono\">SLC6A3</span> is the <strong>dopamine transporter (DAT)</strong>, the reuptake pump that "
        "sets ambient dopamine tone &mdash; the canonical methylphenidate / amphetamine target, and a §22 "
        "<em>gain</em>-axis gene that is reachable <em>here</em> as a drive-<strong>tone</strong> node (a transporter "
        "modulates tone, not synthesis). <span class=\"mono\">SLC6A2</span> is the <strong>noradrenaline transporter "
        "(NET)</strong>, the reuptake partner of DAT and the <strong>atomoxetine</strong> arm &mdash; it extends the "
        "§22 substrate onto the noradrenergic reuptake route. <span class=\"mono\">SLC6A4</span> is the "
        "<strong>serotonin transporter (SERT)</strong>, carried as a §22 arousal / E-I tone node. "
        "<span class=\"mono\">ADRA2A</span> is the <strong>&alpha;<sub>2A</sub>-adrenergic receptor</strong>, the "
        "noradrenergic arousal receptor and the <strong>guanfacine</strong> arm. And <span class=\"mono\">DRD4</span> "
        "is the <strong>D<sub>4</sub> dopamine receptor</strong>, a §22 gain gene reachable here as a drive-tone node "
        "because a receptor <em>reads</em> dopaminergic drive. These are the three real-world ADHD pharmacological "
        "routes &mdash; the stimulant (DAT), the noradrenaline reuptake inhibitor (NET), and the &alpha;<sub>2A</sub> "
        "agonist &mdash; appearing on the map as <strong>directions on a lever</strong>, never as doses, drugs, or "
        "recommendations.</p>",
        "<p>The crucial discipline is the one the whole frame turns on: a promoter read <strong>places a gene on a "
        "lever</strong>; it says <strong>nothing</strong> about whether raising or lowering that gene's activity is "
        "the therapeutic direction, or how far is too far, or in whom. Every one of the five drive-tone links is "
        "graded <span class=\"mono\">[O]</span> cited biology, never derived from the substrate. The reuptake "
        "transporters carry a built-in honesty: a drive-tone lever modulates the <em>tone</em> of catecholamine "
        "signalling, which is a real and reachable handle, but it is the <em>secondary</em> axis &mdash; it does "
        "<em>not</em> reach down into how much transmitter the synthesis enzymes <em>make</em> or the SNARE machinery "
        "<em>releases</em>, which is the dominant fault and the subject of the next section. So the drive-tone levers "
        "are genuine, actionable directions on the reachable axis, and they are explicitly <em>not</em> a claim to "
        "have reached ADHD's core. A direction, never a dose &mdash; <span class=\"mono\">efficacy = 0</span>.</p>",
    ]),

    "<h2>The out-of-reach gain axis: synthesis, release, and a catabolic boundary</h2>",
    "".join([
        "<p>The <strong>dominant</strong> ADHD fault is the <strong>gain-amplitude (GA) axis</strong> &mdash; the "
        "§22 output / gain core &mdash; and it is exactly the axis a drive-tone lever <em>cannot</em> reach. The "
        "module names it with four real genes, each carried with its own promoter read alongside but explicitly "
        "<strong>not a lever</strong>. <span class=\"mono\">TH</span> is <strong>tyrosine hydroxylase</strong>, the "
        "rate-limiting enzyme of catecholamine <strong>synthesis</strong> &mdash; it sets <em>how much</em> dopamine "
        "and noradrenaline is made, the amplitude itself. <span class=\"mono\">DBH</span> is <strong>dopamine "
        "&beta;-hydroxylase</strong>, which converts dopamine to noradrenaline &mdash; the second "
        "<strong>synthesis</strong> gain node. <span class=\"mono\">SNAP25</span> is the <strong>SNAP-25 SNARE</strong> "
        "protein of vesicle <strong>release</strong> &mdash; the presynaptic output gain, how much of what is made "
        "actually gets out. And <span class=\"mono\">COMT</span> is <strong>catechol-O-methyltransferase</strong>, the "
        "prefrontal dopamine <strong>catabolism</strong> enzyme &mdash; carried as a <strong>boundary</strong> node, "
        "because clearance sits at the edge between amplitude and tone, but it is grouped with the gain axis because it "
        "sets <em>how much signal remains</em> rather than where the firing fold sits.</p>",
        "<p>None of these is a lever, and the reason is mechanical: the catecholamine <strong>synthesis</strong> "
        "(<span class=\"mono\">TH</span>, <span class=\"mono\">DBH</span>), <strong>release</strong> "
        "(<span class=\"mono\">SNAP25</span>) and <strong>catabolic-clearance</strong> "
        "(<span class=\"mono\">COMT</span>) machinery sets signal <strong>amplitude</strong>, <em>not</em> the firing "
        "fold &mdash; and a drive-tone (reuptake / receptor) lever has no handle on synthesis or release. This is the "
        "direct analogue of autism's <strong>O axis</strong> (the synaptic output / gain deficit that a gain-reducing "
        "scalar push would only drive lower), and it is named here under the <em>same</em> discipline the "
        "<a href=\"/mind/34-autism-threshold-levers/\">autism chapter</a> introduced: out-of-reach axes are carried on "
        "the map, by name, with real genes, so the partiality is concrete rather than hand-waved. The difference is "
        "that for autism the out-of-reach axes were the <em>secondary</em> ones &mdash; the chapter still reached "
        "autism's dominant excitability axis &mdash; whereas for ADHD the out-of-reach axis is the "
        "<strong>dominant</strong> one. That is the whole reason ADHD is a partial fit and autism was a clean one: "
        "the gain-amplitude core that <em>defines</em> ADHD sits on a different axis from the one the threshold frame "
        "can pull, and the module refuses to pretend otherwise. Each of the four genes is graded "
        "<span class=\"mono\">[F] NOT REACHED</span> for the lever frame (axis-structured, not dose-structured), with "
        "its promoter <span class=\"mono\">&gamma;</span> read carried alongside as <span class=\"mono\">[V]</span> "
        "structural context only.</p>",
    ]),

    "<h2>Empty L1, empty L2, absent W &mdash; not a channelopathy, not a wiring disorder (the autism inverse)</h2>",
    "".join([
        "<p>Three of the four axes the frame can describe are, for ADHD, <strong>empty or absent</strong>, and each "
        "emptiness is a positive statement about what ADHD is <em>not</em>. <strong>L1 is empty</strong> &mdash; there "
        "is no inward-excitatory-current lever &mdash; and <strong>L2 is empty</strong> &mdash; there is no "
        "outward-potassium / inhibitory-current lever. Together that means ADHD is <strong>not a channelopathy</strong>: "
        "unlike epilepsy (which leaned on the M-current), bipolar (calcium channels), or autism (whose dominant lever "
        "was the inward excitatory current), ADHD has <strong>no ionic fold lever at all</strong>. There is no channel "
        "whose conductance you would change to raise or lower a firing threshold, because ADHD's fault is not a "
        "mis-set fold &mdash; it is a mis-set <em>amplitude and tone</em>. This is the second sense in which the fit is "
        "partial: the frame's structural <span class=\"mono\">[F]</span> levers (the ionic ones) have nothing to grip, "
        "and the only handle is the <span class=\"mono\">[O]</span> cited-biology drive surface. <strong>W is "
        "absent</strong> &mdash; zero wiring genes &mdash; because ADHD has intact long-range connectivity, the "
        "discriminant from autism.</p>",
        "<p>Laid side by side, ADHD and autism are mirror images on this frame, and the contrast is the cleanest "
        "summary of both chapters. <strong>Autism</strong> was <em>L1-dominant</em> (its fault lived in the "
        "excitation/inhibition channels, the ionic fold), it <em>reached its dominant axis</em>, and it carried a W "
        "axis that was present and <a href=\"/mind/19-autism-chemical-limits/\">proven unreachable</a>. "
        "<strong>ADHD</strong> is <em>L3-only</em> (its handle lives entirely in the up-stream drive, with the ionic "
        "levers empty), it <em>misses its dominant axis</em> (the gain core sits out of reach), and it carries "
        "<em>no</em> W axis at all (intact wiring). Autism is a channel-and-fold disorder whose wiring is broken but "
        "unreachable; ADHD is a drive-and-amplitude disorder whose wiring is intact and whose dominant amplitude core "
        "is out of the lever frame's reach. The <span class=\"mono\">[F]</span> ionic structure that grounded autism "
        "is exactly what ADHD lacks, and the wiring fault that defined autism is exactly what ADHD does not have. Two "
        "disorders, one frame, opposite signatures &mdash; and the frame is honest about both, including its own "
        "partiality on ADHD.</p>",
    ]),

    "<h2>The DNA grounding: a promoter's own switch stiffness, and a decoupling that inverts autism's</h2>",
    "".join([
        "<p>What places each of the nine genes &mdash; the five drive-tone levers and the four out-of-reach gain genes "
        "&mdash; is not a list but a <strong>read</strong>. For every gene, the module takes its promoter window "
        "(transcription start &minus;2000 to +500 bases, <em>Homo sapiens</em>) and computes "
        "<span class=\"mono\">&gamma; = &minus;mean</span> of the nearest-neighbour base-stacking free energies along "
        "that window (the SantaLucia 1998 nearest-neighbour thermodynamics), then turns that "
        "<span class=\"mono\">&gamma;</span> into the promoter's switch stiffness through the <em>frozen engine's "
        "own</em> functions: <span class=\"mono\">|h_sp| = spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></span> and "
        "<span class=\"mono\">barrier = &gamma;&sup2;/4</span>. The reads span a real range. The five drive-tone "
        "levers, stiffest to softest, are the dopamine transporter <span class=\"mono\">SLC6A3</span> at "
        "<span class=\"mono\">&gamma; &approx; 1.598</span> (<span class=\"mono\">|h_sp| &approx; 0.778</span>), the "
        "D<sub>4</sub> receptor <span class=\"mono\">DRD4</span> (<span class=\"mono\">&gamma; &approx; 1.577</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.762</span>), the serotonin transporter "
        "<span class=\"mono\">SLC6A4</span> (<span class=\"mono\">&gamma; &approx; 1.516</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.719</span>), the &alpha;<sub>2A</sub> receptor "
        "<span class=\"mono\">ADRA2A</span> (<span class=\"mono\">&gamma; &approx; 1.508</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.712</span>), and the noradrenaline transporter "
        "<span class=\"mono\">SLC6A2</span> (<span class=\"mono\">&gamma; &approx; 1.462</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.680</span>). The four out-of-reach gain genes read "
        "<span class=\"mono\">TH</span> at <span class=\"mono\">&gamma; &approx; 1.538</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.734</span>), <span class=\"mono\">DBH</span> "
        "(<span class=\"mono\">&gamma; &approx; 1.500</span>, <span class=\"mono\">|h_sp| &approx; 0.707</span>), "
        "<span class=\"mono\">COMT</span> (<span class=\"mono\">&gamma; &approx; 1.466</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.683</span>), and the SNARE release gene "
        "<span class=\"mono\">SNAP25</span> at <span class=\"mono\">&gamma; &approx; 1.438</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.664</span>, the softest in the whole set).</p>",
        "<p>That range tells a story, and it is the <strong>exact inverse of autism's</strong>. In autism, promoter "
        "stiffness ran <em>opposite</em> to reachability: the genes a chemical lever could <em>not</em> touch (the "
        "out-of-reach scaffold and wiring genes) read <em>stiffest</em>, and the actionable E/I levers read softest. "
        "In ADHD the relationship flips: the <strong>stiffest</strong> promoter in the entire set, the dopamine "
        "transporter <span class=\"mono\">SLC6A3</span> (<span class=\"mono\">|h_sp| &approx; 0.778</span>), is a "
        "<em>reachable</em> drive-tone lever &mdash; the canonical stimulant target &mdash; while the "
        "<strong>softest</strong>, the SNARE release gene <span class=\"mono\">SNAP25</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.664</span>), is an <em>out-of-reach</em> gain gene. The genes the "
        "frame can touch read stiffest; the genes it cannot read softest &mdash; the opposite of autism. These are "
        "read on the <strong>same R19 substrate, with the same engine, that the bipolar, epilepsy, depression, "
        "schizophrenia, autism and analgesic packages used</strong>, which is the whole point of the inheritance: one "
        "substrate, one pipeline, now six problems. And the <span class=\"mono\">&gamma;</span> read is a property of "
        "the gene's <strong>promoter sequence</strong>, blind to whether the gene is on or off and to gain / loss / "
        "expression level &mdash; that is <em>all</em> it is, and it is the reason the next section's ranking can carry "
        "<span class=\"mono\">&gamma;</span> alongside every target without ever letting it touch the score.</p>",
    ]),

    "<h2>Ranking targets, the ADHD unmet-need signature, and the firewall that adds two misuse guards</h2>",
    "".join([
        "<p>The last component prioritises, and it prioritises <strong>targets, never drugs or doses</strong>. Unlike "
        "autism &mdash; which ranked only its lever genes &mdash; the ADHD ranking spans all <strong>nine</strong> "
        "genes (the five levers and the four out-of-reach gain genes), precisely so the partiality is visible in the "
        "ranking itself. A burden-weighted score combines three declared, cited weights &mdash; clinical burden "
        "(<span class=\"mono\">0.40</span>), unmet need (<span class=\"mono\">0.35</span>), and genetic-evidence / "
        "druggability (<span class=\"mono\">0.25</span>) &mdash; on cited 1&ndash;5 tiers. The <strong>ADHD "
        "signature</strong> is the <em>inverse</em> of autism's, and it shows up in the unmet-need tier. Autism had "
        "<em>no</em> approved core-feature pharmacology, so its unmet-need floor was the <em>highest</em> in the series "
        "and need was uniformly high. ADHD is the opposite: it has <strong>established, effective core routes</strong> "
        "&mdash; the dopamine transporter (methylphenidate / amphetamine), the noradrenaline transporter "
        "(atomoxetine), and the &alpha;<sub>2A</sub> receptor (guanfacine) &mdash; so the reachable drive-tone "
        "transporters carry <strong>low unmet need</strong>, the <em>lowest</em> floor in the whole series. The "
        "out-of-reach gain genes (<span class=\"mono\">TH</span>, <span class=\"mono\">DBH</span>, "
        "<span class=\"mono\">SNAP25</span>) carry the unmet-need <em>ceiling</em> &mdash; nothing selectively reaches "
        "the synthesis / release core &mdash; but they are flagged <strong>not actionable</strong>, because ranking a "
        "target you have already declared out of reach as a <em>next step</em> would be incoherent.</p>",
        "<p>The consequence is a ranking that itself encodes the partial fit. The <strong>highest-burden, "
        "highest-unmet</strong> targets &mdash; <span class=\"mono\">TH</span> first, then "
        "<span class=\"mono\">DRD4</span>, <span class=\"mono\">DBH</span>, <span class=\"mono\">SNAP25</span> &mdash; "
        "are all <strong>non-actionable</strong>: the synthesis / release gain genes because they are out of the lever "
        "frame's reach, and <span class=\"mono\">DRD4</span> because there is no selective agent for it. The leading "
        "<strong>actionable</strong> target is the dopamine transporter <span class=\"mono\">SLC6A3</span> &mdash; but "
        "only at rank <strong>five</strong>, lowered by its established-route low unmet need. In other words, where "
        "the unmet need is highest the target is unreachable, and where the target is reachable the unmet need is "
        "lowest &mdash; the signature of a disorder whose treatments work on the secondary axis while the dominant axis "
        "stays out of reach. This also produces the firewall made visible. The <span class=\"mono\">&gamma;</span> "
        "read is carried <em>alongside</em> each target as structural context but is <strong>never folded into the "
        "score</strong>, and the two rankings are <strong>decoupled</strong>: the <strong>stiffest</strong> promoter "
        "in the set, the dopamine transporter <span class=\"mono\">SLC6A3</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.778</span>), sits at priority <strong>#5</strong>, not the top; and "
        "the <strong>top-priority</strong> target, the synthesis enzyme <span class=\"mono\">TH</span>, has only the "
        "<em>third</em>-stiffest read. This is the <strong>inverse of autism's decoupling</strong> (where the stiffest "
        "read sat at the bottom of priority), and it makes the same point: if promoter stiffness drove the ranking, "
        "neither target could sit where it does.</p>",
        "<p>A <strong>fail-closed forbidden-claim scanner</strong> guards the whole package, and for ADHD it is the "
        "<strong>strictest in the series</strong>. Beyond the usual dose / efficacy-as-fact / safety-as-fact / "
        "synthesis classes, it adds two classes specific to a stimulant topic. The <strong>stimulant-misuse</strong> "
        "class rejects <em>get-high</em>, <em>snort</em>, <em>euphoria</em>, <em>recreational</em> and "
        "<em>party-drug</em> vocabulary outright, because a stimulant mechanism map must never read as a misuse guide. "
        "The <strong>cognitive-enhancement</strong> class rejects <em>smart-drug</em>, <em>study-drug</em>, "
        "<em>nootropic</em>, <em>boost-focus</em> and <em>limitless</em> framing, because the map describes a "
        "<em>disorder mechanism</em>, not a performance aid for anyone. Both classes are <strong>negation-guarded</strong> "
        "&mdash; a sentence that <em>rejects</em> a misuse frame is allowed, a sentence that <em>asserts</em> one fails "
        "the build &mdash; and each carries a planted self-test that <em>must</em> fire on its own bait, failing the "
        "build if it ever does not. The firewall must be stated once more in full: the promoter "
        "<span class=\"mono\">|h_sp|</span> is a gene's <strong>own switch stiffness</strong>, and it is "
        "<strong>never</strong> equated with a transporter occupancy, a synaptic catecholamine level, a stimulant's "
        "potency, a dose, an in-vivo selectivity, or any clinical effect. This module reproduces bit-for-bit with the "
        "engine byte-unchanged.</p>",
    ]),

    "<h2>Discipline: a direction, never a dose &mdash; and not medical advice</h2>",
    "".join([
        "<p>Everything here is an in-silico <em>reading</em> of promoter sequence and a <em>frame</em> for organising "
        "targets, not a clinical measure, a diagnosis, or a prescription. The model asserts <em>mechanism directions "
        "and target placements</em> &mdash; ADHD's drive-tone set-point can be modulated through the up-stream drive "
        "lever; these five transporter and receptor genes populate that lever; ADHD loads its entire threshold-frame "
        "engagement on L3, with the ionic levers empty; the map reaches the secondary drive-tone axis only; the "
        "dominant gain-amplitude axis (synthesis, release, clearance) is named and out of reach; the wiring axis is "
        "absent; the fit is therefore the first <span class=\"mono\">[L]</span> partial fit in the series &mdash; and "
        "<strong>nothing</strong> about which agent acts on any lever, at what dose, in whom, whether any real "
        "compound changes anyone's traits, or that anyone should change anything. The agents named as "
        "<em>directions</em> (the stimulant, atomoxetine and guanfacine arms) are illustrations of a <em>sign</em> on "
        "the reachable axis, never a recommendation, and the recorded structure &mdash; the dominant axis out of "
        "reach, the empty ionic levers, the absent wiring axis &mdash; is there precisely because a generic lever "
        "placement is <strong>not</strong> a clinical direction. Real ADHD is heterogeneous, and its dominant fault is "
        "an <strong>amplitude</strong> axis this lever frame explicitly <em>cannot</em> reach &mdash; a partiality "
        "that is <strong>locked</strong>, not smoothed over.</p>",
        "<p>Two stricter boundaries close the chapter. ADHD is a difference in <strong>regulation</strong> &mdash; of "
        "attention, arousal, and drive &mdash; not a deficit of worth, intelligence, or character; the map ranks where "
        "a clean unmet mechanistic direction exists, and it does <em>not</em> assert that any direction treats, "
        "normalises, or cures ADHD, nor that anyone should be made to conform. And nothing in the stimulant biology "
        "described here is a licence for <strong>misuse or enhancement</strong>: the map is a disorder-mechanism "
        "frame, the scanner rejects get-high / recreational and smart-drug / nootropic framing outright, and the "
        "agents named as directions are mechanism signs, never performance aids. A promoter read and a lever "
        "assignment are mechanism boundaries, <strong>not</strong> a claim about the felt quality of an ADHD mind "
        "(Axis-A firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>, the hard problem stays "
        "<strong>open</strong>). <strong>This is not medical advice, not a diagnosis, not a treatment protocol, and "
        "not a cure.</strong> <span class=\"mono\">medium_efficacy_tested = 0</span>; targets ranked, never drugs or "
        "doses; no stimulant-misuse or cognitive-enhancement licence.</p>",
    ]),
])

PREV = '<a rel="prev" href="/mind/34-autism-threshold-levers/">&larr; §34 Autism: three threshold levers</a>'
NEXT = '<a rel="next" href="/mind/36-addiction-threshold-levers/">§36 Addiction: reward-drive levers &rarr;</a>'

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
