#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_ch34_autism_levers.py — emit the §34 autism threshold-levers chapter (roadmap ASD-T-L).

Writes docs/mind/34-autism-threshold-levers/index.html using the same head/JSON-LD/footer
scaffolding as the other Part-II chapters so the SEO markup is byte-consistent. The answer-first
<p class="answer"> and the vp-card asides are NOT written here — build_search_layer.py injects them
from mind_registry.py (single source of truth): this generator only emits the skeleton (abstract +
claim-strip + body sections + nav). Body text is English-only (VP-SPEC C0).

This chapter applies the SAME threshold-shift intervention logic that §30 (bipolar T2b-L), §31
(epilepsy T2a-L), §32 (depression T1b-L) and §33 (schizophrenia T1a-L) used, inherited from the
analgesic reproducibility package (Zenodo 10.5281/zenodo.20733420), to the §18-19 autism E/I
OVER-EXCITATION pole — and it is the UNIFICATION case: rather than introducing a new lever
combination it re-expresses the pre-existing autism_multilever_threshold.py (which carried the idea
under informal A1/A2/A3 levers) under the formal L1/L2/L3 frame. §18-19 proved autism is three fault
axes (T excitability, O output-deficit, W long-range wiring), that only the T axis is reachable by a
scalar chemical lever, and (§19) that the W axis is provably unreachable. This chapter decomposes the
T-axis correction into a DNA-grounded three-lever target map over ten autism E/I genes (L1-dominant,
L3-sparse) and NAMES the six out-of-reach O/W/syndromic genes. Seven promoter reads (GRIN2A/GRIN2B/
CACNA1C/GABRB3 from the schizophrenia cache, SCN2A/KCNQ3 from the bipolar cache, SLC6A4 from the
depression cache) are carried over VERBATIM (gamma is strand-symmetric). No new mechanism, no new
tuned constant; the engine is READ-ONLY. The numbers quoted in the prose are the structural reads
(gamma, |h_sp|) and the burden ranking from repro/mind/_verify/autism_threshold_levers.py and
autism_burden_prioritisation.py (efficacy=0; targets ranked, never drugs or doses); the canonical
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

SLUG = "34-autism-threshold-levers"
NO = 34
GRADE = "model"
GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}

TITLE_TAG = "Autism threshold levers: the E/I over-excitation sign, decomposed (T-axis only; O/W out of reach)"
H1 = ("Autism threshold levers &mdash; the E/I over-excitation operating-point correction, decomposed into "
      "DNA-grounded levers (L1-dominant; the output and wiring axes named, out of reach)")
CRUMB = "Autism: three threshold levers"
HEADLINE = ("The autism E/I over-excitation operating-point correction decomposed into a DNA-grounded "
            "three-lever target map: reduce the inward excitatory current (L1, dominant), increase the "
            "outward potassium / restore the GABA-A inhibitory current (L2), with a single sparse "
            "serotonergic up-stream lever (L3), over ten autism genes &mdash; reaching the excitability "
            "(threshold) axis only, with the output-deficit and long-range-wiring axes named but out of reach")
META = ("Chapters 18-19 placed autism as three distinct fault axes (excitability / output-deficit / "
        "long-range-wiring) and proved only the excitability axis is reachable by a scalar chemical lever. "
        "This chapter applies the same threshold-shift intervention logic used for bipolar disorder, "
        "epilepsy, depression and schizophrenia (inherited from the analgesic reproducibility package, "
        "Zenodo 10.5281/zenodo.20733420) and decomposes that excitability correction into three concrete "
        "levers -- reduce the inward excitatory current (L1, dominant), increase the outward potassium / "
        "restore the GABA-A current (L2), remove a single sparse up-stream serotonergic drive (L3) -- over "
        "ten autism genes placed by their own promoter switch stiffness, unifying the pre-existing autism "
        "multilever module under the formal frame. The map reaches the excitability axis only; the "
        "output-deficit and wiring axes are named with real genes but out of reach, and the wiring axis is "
        "provably unreachable. Targets are ranked, never drugs or doses. efficacy=0; not medical advice; "
        "autism is a neurodevelopmental difference, not only a deficit.")

ABSTRACT = (
    "The autism chapters &mdash; <a href=\"/mind/18-autism-three-axis/\">the three-axis chapter</a> and "
    "<a href=\"/mind/19-autism-chemical-limits/\">the chemical-limits chapter</a> &mdash; read autism not as "
    "one severity dial but as <strong>three distinct fault axes</strong>: <strong>T</strong>, an "
    "<em>excitability / E-I threshold</em> axis (an <strong>over-excitation</strong> operating point whose "
    "ignition fold sits <em>too low</em>); <strong>O</strong>, a <em>synaptic output / gain deficit</em>; and "
    "<strong>W</strong>, a <em>long-range wiring / connectivity</em> axis. They proved the <em>pole</em> and "
    "the corrective <em>sign</em> for the reachable axis &mdash; the T axis is an over-excitation pole, so the "
    "corrective push is whatever <strong>reduces the excess drive</strong> or <strong>restores inhibition</strong> "
    "(raises the fold), the <em>same</em> direction as epilepsy and the schizophrenia positive domain &mdash; "
    "but they carried a second, sharper result the symptom-checklist view cannot: a scalar chemical lever "
    "reaches the <strong>T axis only</strong>, and <a href=\"/mind/19-autism-chemical-limits/\">§19</a> "
    "<em>proved</em> the W axis is <strong>unreachable</strong> &mdash; a threshold shift can only <em>mask</em> "
    "a wiring fault by over-synchronisation (the seizure analogue), never <em>correct</em> it. This chapter "
    "does not invent a new map; it <strong>unifies</strong> the pre-existing autism multilever module under the "
    "<strong>same piece of inherited technology</strong> the "
    "<a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a>, "
    "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a>, "
    "<a href=\"/mind/32-depression-threshold-levers/\">depression</a> and "
    "<a href=\"/mind/33-schizophrenia-threshold-levers/\">schizophrenia</a> levers chapters used: the "
    "<strong>threshold-shift intervention logic</strong> from the analgesic reproducibility package "
    "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>). Its three abstract "
    "levers &mdash; <strong>L1</strong> change the inward (excitatory) current, <strong>L2</strong> change the "
    "outward (potassium / inhibitory) current, <strong>L3</strong> change the up-stream drive &mdash; carry "
    "over unchanged, and autism is the <strong>fifth distribution pattern</strong> across the series: it is "
    "<strong>L1-dominant with a nearly-empty L3</strong>. Of <strong>ten</strong> lever genes, <strong>five</strong> "
    "sit on the excitatory-reduce lever (L1: <span class=\"mono\">GRIN2A</span>, <span class=\"mono\">GRIN2B</span>, "
    "<span class=\"mono\">GRIA1</span>, <span class=\"mono\">SCN2A</span>, <span class=\"mono\">CACNA1C</span>), "
    "<strong>four</strong> on the inhibitory-restore lever (L2: <span class=\"mono\">KCNQ3</span>, "
    "<span class=\"mono\">GABRB3</span>, <span class=\"mono\">GABRA5</span>, <span class=\"mono\">GABRA2</span>), "
    "and just <strong>one</strong> on the up-stream lever (L3: <span class=\"mono\">SLC6A4</span>, a cautious, "
    "non-monotone serotonergic node graded <span class=\"mono\">[O]</span>) &mdash; the L3-sparsity is itself the "
    "finding, that autism's actionable biology sits <em>locally</em> on the excitation/inhibition set with no "
    "clean up-stream drug drive. Two structural strengthenings set this chapter apart from the schizophrenia "
    "domain-restriction template. First, the <strong>out-of-reach axes are named with real genes</strong>: the "
    "<strong>O</strong> (output-deficit) axis carries <span class=\"mono\">SHANK3</span>, "
    "<span class=\"mono\">SYNGAP1</span>, <span class=\"mono\">NRXN1</span>; the <strong>W</strong> "
    "(long-range-wiring) axis carries <span class=\"mono\">CNTNAP2</span>, <span class=\"mono\">RELN</span>; and "
    "the syndromic master <span class=\"mono\">MECP2</span> rides alongside &mdash; carried on the map but "
    "explicitly <strong>not levers</strong>. Second, the W-axis unreachability is <strong>proven, not asserted</strong>: "
    "§19 showed a scalar threshold lever can only mask the wiring fault, never correct it. Each gene is placed by "
    "reading its <strong>own promoter switch stiffness</strong> &mdash; <span class=\"mono\">&gamma; = &minus;mean</span> "
    "nearest-neighbour stacking free energy (SantaLucia 1998) over its promoter window, turned into "
    "<span class=\"mono\">|h_sp| = spinodal(&gamma;)</span> with the frozen engine <strong>read-only</strong>, and "
    "seven of the reads (<span class=\"mono\">GRIN2A</span>, <span class=\"mono\">GRIN2B</span>, "
    "<span class=\"mono\">CACNA1C</span>, <span class=\"mono\">GABRB3</span> from the schizophrenia cache, "
    "<span class=\"mono\">SCN2A</span>, <span class=\"mono\">KCNQ3</span> from the bipolar cache, "
    "<span class=\"mono\">SLC6A4</span> from the depression cache) are carried over <strong>verbatim</strong>. Two "
    "honest caveats are recorded, not hidden: <span class=\"mono\">SCN2A</span> and <span class=\"mono\">GRIN2B</span> "
    "are <strong>gain/loss sign-subtle</strong> (a gain-of-function pushes the early-infantile developmental-"
    "epileptic-encephalopathy / seizure pole while a loss-of-function pushes the milder autism / intellectual-"
    "disability pole &mdash; opposite directions), and the threshold lever pushed <em>too hard</em> is itself the "
    "<strong>seizure edge</strong> (the real autism&plus;epilepsy comorbidity). Three fail-closed disciplines ride "
    "along: every channel and serotonergic link stays graded <span class=\"mono\">[O]</span> cited biology, a "
    "forbidden-claim scanner rejects any dose / efficacy / safety / synthesis statement <em>and</em> &mdash; "
    "uniquely for this topic &mdash; an autism <strong>quackery</strong> class (chelation, bleach / "
    "miracle-mineral protocols) and a <strong>normalise-framing</strong> class that protects neurodiversity "
    "respect, and a burden-weighted ranking orders <strong>targets, never drugs or doses</strong>. The "
    "<strong>firewall</strong> is absolute: the promoter <span class=\"mono\">|h_sp|</span> is a gene's own switch "
    "stiffness, <strong>never</strong> the §18 network over-excitation threshold, a receptor occupancy, a synaptic "
    "level, a potency, a dose, or a clinical effect. <span class=\"mono\">efficacy = 0</span>; not medical advice; "
    "autism is a neurodevelopmental <strong>difference</strong>, not only a deficit; the hard problem stays open."
)

BODY = "\n".join([
    "<h2>What §18-19 left abstract (and what they proved cannot be reached)</h2>",
    "".join([
        "<p>The two autism chapters &mdash; <a href=\"/mind/18-autism-three-axis/\">the three-axis chapter</a> "
        "and <a href=\"/mind/19-autism-chemical-limits/\">the chemical-limits chapter</a> &mdash; did something "
        "the symptom-checklist view of autism cannot: they replaced a single severity dial with <strong>three "
        "distinct fault axes</strong>, each a different <em>kind</em> of difference. The <strong>T axis</strong> "
        "is <em>excitability</em> &mdash; the excitation/inhibition (E-I) balance &mdash; and on the atlas it is "
        "an <strong>over-excitation operating point</strong>: health is a population of micro-eddies igniting in "
        "gamma only when activity clears a threshold (the ignition <em>fold</em>), and the T-fault is that fold "
        "sitting <strong>too low</strong>, so circuits over-respond. The <strong>O axis</strong> is an "
        "<em>output / gain deficit</em> at the synapse &mdash; too <em>little</em> effective transmission, a "
        "different failure entirely. The <strong>W axis</strong> is <em>long-range wiring</em> &mdash; a "
        "connectivity / geometry problem, local circuits over-connected and long-range links under-connected. "
        "These are <em>not</em> three severities of one thing; they are three axes that can vary independently, "
        "which is why autism presents so differently from person to person.</p>",
        "<p>§18-19 proved two things about these axes and stopped. The first is the <em>pole and sign</em> of the "
        "reachable one: the T axis is an <strong>over-excitation</strong> pole &mdash; the same side of the line "
        "as the over-synchronisation disorders &mdash; so the corrective <em>sign</em> is whatever <strong>reduces "
        "the excess drive</strong> or <strong>restores inhibition</strong> (raises the fold), the mirror of "
        "depression's restore-the-deficit and the twin of epilepsy's and the schizophrenia positive domain's "
        "reduce-the-excess. But §18-19 left that push <em>abstract</em>. The second result is the reason this "
        "chapter is unlike the four before it: §18-19 also proved a <strong>reach limit</strong>. A scalar "
        "chemical lever &mdash; a drug that raises or lowers a current or a drive &mdash; can act on the T axis, "
        "but it <em>cannot</em> lift the O deficit (a gain-reducing lever pushes a deficit further down), and "
        "<a href=\"/mind/19-autism-chemical-limits/\">§19</a> went further and <strong>proved</strong> the W axis "
        "is <strong>unreachable</strong>: a threshold shift can only <em>mask</em> a wiring fault by forcing "
        "over-synchronisation &mdash; the seizure analogue &mdash; and can <em>never</em> re-route the geometry "
        "that the fault lives in. A mechanism atlas should be able to say <em>which</em> molecular targets realise "
        "the T-axis correction <strong>and</strong> be honest, by name, about the axes a chemical lever cannot "
        "reach. That is exactly what this chapter does.</p>",
    ]),

    "<h2>The inherited technology, applied a fifth time &mdash; as a unification, and the L1-dominant pattern</h2>",
    "".join([
        "<p>The handle is not invented here and it is not adapted here &mdash; and in autism's case it is not even "
        "newly <em>applied</em>. Autism already had a multilever threshold module that carried this exact idea "
        "under informal <span class=\"mono\">A1</span>/<span class=\"mono\">A2</span>/<span class=\"mono\">A3</span> "
        "labels. What this chapter does is <strong>unify</strong> that module under the <em>same</em> formal frame "
        "the <a href=\"/mind/30-bipolar-threshold-levers/\">bipolar</a>, "
        "<a href=\"/mind/31-epilepsy-threshold-levers/\">epilepsy</a>, "
        "<a href=\"/mind/32-depression-threshold-levers/\">depression</a> and "
        "<a href=\"/mind/33-schizophrenia-threshold-levers/\">schizophrenia</a> chapters inherited from the "
        "<strong>analgesic reproducibility package</strong> "
        "(<a href=\"https://doi.org/" + ANALGESIC_DOI + "\">Zenodo " + ANALGESIC_DOI + "</a>). Its premise is "
        "general: an operating point is set by a balance of currents and the drives that bias them, so there are "
        "exactly <strong>three levers</strong> on it. <strong>L1</strong> &mdash; <em>change the inward, "
        "excitatory current</em>. <strong>L2</strong> &mdash; <em>change the outward, repolarising (or "
        "inhibitory) current</em>. <strong>L3</strong> &mdash; <em>change the up-stream drive</em> that sets where "
        "the operating point sits. The frame applies unchanged because the autism chapters, the four levers "
        "chapters, and the analgesic package all share the <strong>same R19 substrate</strong> &mdash; the "
        "engine's supercritical pitchfork <span class=\"mono\">&#7779; = g&middot;s &minus; s&sup3; + h</span>, "
        "whose spinodal fold IS the switching barrier &mdash; so the informal A1/A2/A3 levers and the formal "
        "L1/L2/L3 levers are the <em>same</em> three operators, and the unification loses nothing.</p>",
        "<p>Autism is the <strong>fifth distribution pattern</strong> across the series, and a distinctive one. "
        "Where bipolar leaned on L1 (calcium channels), epilepsy on L1&plus;L2 (the "
        "<span class=\"mono\">KCNQ2</span>/<span class=\"mono\">KCNQ3</span> M-current), depression on L3 (the "
        "up-stream HPA / monoamine / neurotrophic drives, L3-dominant), and schizophrenia on L1&plus;L3 "
        "co-dominantly, autism is <strong>L1-dominant with a nearly-empty L3</strong>: of the ten lever genes, "
        "<strong>five sit on L1</strong>, <strong>four on L2</strong>, and <strong>just one on L3</strong>. That "
        "single-gene L3 is not an omission &mdash; it is a <em>finding</em>. Autism's replicated genetic signal "
        "is overwhelmingly in the <strong>excitation/inhibition machinery itself</strong> (glutamate and GABA "
        "receptors, voltage-gated channels), not in a clean up-stream neuromodulatory drive the way depression's "
        "HPA axis is; so the map reports, faithfully, that autism's actionable biology sits <em>locally</em> on "
        "the E/I set, with no clean up-stream drug handle. The pipeline is reused at the level of code, not "
        "analogy: <strong>seven</strong> of the reads &mdash; <span class=\"mono\">GRIN2A</span>, "
        "<span class=\"mono\">GRIN2B</span>, <span class=\"mono\">CACNA1C</span>, <span class=\"mono\">GABRB3</span> "
        "from the schizophrenia cache and <span class=\"mono\">SCN2A</span>, <span class=\"mono\">KCNQ3</span> from "
        "the bipolar cache and <span class=\"mono\">SLC6A4</span> from the depression cache &mdash; are carried "
        "over <strong>verbatim</strong>, because <span class=\"mono\">&gamma;</span> is a strand-symmetric "
        "property of the sequence and does not change between problems. Nothing about the engine is touched; the "
        "module re-emerges the frozen tree read-only and confirms it byte-unchanged, and registers as the "
        "<strong>twelfth atlas citizen</strong> (<span class=\"mono\">ASD-T-L</span>).</p>",
    ]),

    "<h2>The new finding: a T-axis map whose out-of-reach axes are named (and one is provably unreachable)</h2>",
    "".join([
        "<p>This is the result that makes autism the most structurally explicit chapter in the levers series. The "
        "<a href=\"/mind/33-schizophrenia-threshold-levers/\">schizophrenia chapter</a> introduced "
        "<em>domain restriction</em> &mdash; the lever map reached the positive domain only &mdash; but it left "
        "the unreached domains as categories. Autism does two things schizophrenia did not. First, it <strong>names "
        "the out-of-reach axes with real genes</strong>, and carries them on the map as explicitly "
        "<em>non-levers</em>. The <strong>O axis</strong> (synaptic output / gain deficit) carries "
        "<span class=\"mono\">SHANK3</span> (the postsynaptic master scaffold of Phelan&ndash;McDermid syndrome), "
        "<span class=\"mono\">SYNGAP1</span> (a synaptic Ras-GAP gain regulator), and <span class=\"mono\">NRXN1</span> "
        "(presynaptic neurexin-1). The <strong>W axis</strong> (long-range wiring) carries "
        "<span class=\"mono\">CNTNAP2</span> (Caspr2, a long-range cell-adhesion molecule) and "
        "<span class=\"mono\">RELN</span> (reelin, the cortical-lamination / migration signal). The syndromic "
        "master <span class=\"mono\">MECP2</span> (X-linked, the chromatin / transcriptional regulator behind "
        "Rett and MECP2-duplication syndromes) rides alongside as a whole-program perturbation. None of these is a "
        "lever, because a gain-reducing scalar push would drive an O-axis output deficit <em>lower</em>, not "
        "higher, and cannot re-route a W-axis geometry at all.</p>",
        "<p>Second, and more sharply, the W-axis unreachability is not a hedge &mdash; it is a <strong>result the "
        "model imports as proven</strong>. <a href=\"/mind/19-autism-chemical-limits/\">§19</a> showed, on this "
        "same substrate, that a scalar threshold lever applied to a wiring fault can only <em>mask</em> it by "
        "forcing the network into <strong>over-synchronisation</strong> &mdash; the very seizure analogue the T "
        "lever pushed too far produces &mdash; and can <em>never</em> correct the geometry "
        "(<span class=\"mono\">P4_chemical_cannot_fix_W</span>, "
        "<span class=\"mono\">P5_threshold_lowering_is_mask_not_correction</span>). So the lever map reaches the "
        "<strong>T axis and only the T axis</strong>, the O and W axes are <em>named</em> but unreached, and the "
        "W axis is <em>provably</em> unreachable. The module records this in a <strong>domain-restriction "
        "witness</strong> (T = reached, O = not reached, W = not reached) and a separate "
        "<strong>out-of-reach-targets</strong> section that lists the six genes by axis. Capturing the partiality "
        "precisely &mdash; axis-structured and gene-named, not dose-structured &mdash; is far more informative "
        "than a map that pretended to cover all three, and it is why the fail-closed L3-honesty gate for this "
        "chapter checks not only that the serotonergic link stays <span class=\"mono\">[O]</span> but that L1 is "
        "the <em>unique</em> dominant lever, that L3 is <em>sparse</em>, that the T-axis restriction holds, and "
        "that at least one O gene and one W gene are named and flagged unreached with the §19 citation; it FAILS "
        "the build if any of these slips.</p>",
    ]),

    "<h2>L1 (dominant) &mdash; the inward excitatory-reduce levers (and the gain/loss seizure-edge subtlety)</h2>",
    "".join([
        "<p>The dominant lever is the <strong>excitatory-reduce axis</strong>, and it carries the chapter's "
        "<strong>most important honest caveat</strong>. Five genes sit here. <span class=\"mono\">GRIN2A</span> "
        "and <span class=\"mono\">GRIN2B</span> are the NMDA-receptor GluN2A and GluN2B subunits (glutamate, "
        "calcium-permeable); <span class=\"mono\">GRIA1</span> is an AMPA-receptor subunit carrying the "
        "fast-excitatory sub-route; <span class=\"mono\">SCN2A</span> is the voltage-gated sodium channel "
        "Na<sub>V</sub>1.2, one of the most recurrently mutated autism genes; and <span class=\"mono\">CACNA1C</span> "
        "is the L-type calcium channel Ca<sub>V</sub>1.2, the most-replicated cross-disorder locus (the same one "
        "that anchored the bipolar and schizophrenia L1 axes). The naive reading of L1 would be <em>reduce inward "
        "excitatory current</em> &mdash; raise the fold, stop the over-excitation &mdash; but in autism the sign "
        "is not that simple for two of these genes, and the model flags it explicitly. <span class=\"mono\">SCN2A</span> "
        "and <span class=\"mono\">GRIN2B</span> are <strong>gain/loss sign-subtle</strong>: a "
        "<em>gain</em>-of-function variant pushes the early-infantile developmental-epileptic-encephalopathy / "
        "seizure pole, while a <em>loss</em>-of-function variant pushes the milder autism / intellectual-disability "
        "pole &mdash; the <em>same gene</em> produces opposite clinical directions depending on the variant, so "
        "&lsquo;reduce excitation&rsquo; is not a clean direction for it. This is the autism analogue of "
        "depression's ketamine caveat and the schizophrenia NMDA-hypofunction caveat, and it has a second, "
        "autism-specific face: the T lever pushed <strong>too hard</strong> is itself the <strong>seizure edge</strong>. "
        "Drive the over-excitation correction too far and the network tips into the over-synchronisation pole &mdash; "
        "exactly the autism&plus;epilepsy comorbidity that is clinically real. So the lever <em>placement</em> (the "
        "gene is on the inward-current lever) is structural and trait-blind, but the <em>direction and magnitude</em> "
        "of any clinically relevant agent are variant-, dose-, and mechanism-specific and stay graded "
        "<span class=\"mono\">[O]</span>. A promoter read places a gene on a lever; it says <strong>nothing</strong> "
        "about whether reducing or raising a current is the therapeutic direction, or how far is too far. A "
        "direction, never a dose.</p>",
    ]),

    "<h2>L2 &mdash; the inhibitory-restore levers (potassium and GABA-A)</h2>",
    "".join([
        "<p>The second lever is the <strong>inhibitory-restore axis</strong>, and it is the restoring mirror of L1 "
        "&mdash; instead of reducing the inward excitatory current, it raises the outward / inhibitory current that "
        "holds the fold up. Four genes sit here. <span class=\"mono\">KCNQ3</span> is the K<sub>V</sub>7.3 "
        "potassium channel (the M-current), and restoring its outward current is the most <em>direction-consistent</em> "
        "move on the whole map: more outward current raises the fold directly, and the channel is druggable (the "
        "same M-current axis epilepsy leaned on). <span class=\"mono\">GABRB3</span> (the GABA-A &beta;3 subunit, on "
        "15q11&ndash;13, the Dup15q / Angelman overlap that raises its burden), <span class=\"mono\">GABRA5</span> "
        "(the extrasynaptic &alpha;5 subunit carrying <em>tonic</em> inhibition, with &alpha;5-selective ligands "
        "already in the literature), and <span class=\"mono\">GABRA2</span> (the synaptic &alpha;2 subunit carrying "
        "<em>phasic</em> inhibition) raise the inhibitory chloride conductance &mdash; the same restoring side of "
        "the E/I axis, approached through inhibition rather than through reducing excitation. This is the lever the "
        "burden ranking will surface as the <strong>cleanest actionable direction</strong>, precisely because it "
        "does <em>not</em> carry the gain/loss sign problem the L1 channels do: restoring inhibition raises the fold "
        "regardless of variant direction. Every claim on this lever is a <strong>mechanism direction only</strong>; "
        "no opener, modulator, dose, or patient is named.</p>",
    ]),

    "<h2>L3 (sparse) &mdash; the single up-stream serotonergic node, and why sparsity is the finding</h2>",
    "".join([
        "<p>The third lever does not touch a channel; it changes an <em>up-stream drive</em> &mdash; and in autism "
        "it is almost <strong>empty</strong>. A single gene sits here: <span class=\"mono\">SLC6A4</span>, the "
        "serotonin transporter. It is carried as a <strong>cautious</strong> L3 node and graded "
        "<span class=\"mono\">[O]</span> for a specific reason: the serotonergic evidence in autism is "
        "<strong>non-monotone</strong> and mixed &mdash; it is an <em>adjunct</em> signal, not a clean up-stream "
        "correction the way depression's HPA / monoamine drives are. The contrast with depression is the whole "
        "point. Depression was <strong>L3-dominant</strong>: twelve of its eighteen genes sat on up-stream HPA, "
        "monoamine, and neurotrophic drives, because depression <em>is</em> a disorder of an up-stream drive "
        "biasing an operating point. Autism is the opposite extreme &mdash; <strong>L3-sparse</strong> &mdash; "
        "because autism's replicated signal sits in the <strong>excitation/inhibition machinery itself</strong>, "
        "not in a clean neuromodulatory drive. The sparsity is therefore not a gap in the search; it is a "
        "<em>structural fact about where autism's actionable biology lives</em>: locally, on the E/I set, where "
        "the L1 and L2 levers act, with no clean up-stream drug handle to pull. The fail-closed L3-honesty gate "
        "enforces both halves of this &mdash; that the one serotonergic link stays <span class=\"mono\">[O]</span> "
        "cited biology (never derived from the substrate), and that L3 is genuinely <em>sparse</em> while L1 is the "
        "<em>unique</em> dominant lever. A direction, never a dose &mdash; <span class=\"mono\">efficacy = 0</span>.</p>",
    ]),

    "<h2>The DNA grounding: a promoter's own switch stiffness, and a decoupling that names itself</h2>",
    "".join([
        "<p>What places each of the sixteen genes &mdash; the ten levers and the six out-of-reach targets &mdash; "
        "is not a list but a <strong>read</strong>. For every gene, the module takes its promoter window "
        "(transcription start &minus;2000 to +500 bases, <em>Homo sapiens</em>) and computes "
        "<span class=\"mono\">&gamma; = &minus;mean</span> of the nearest-neighbour base-stacking free energies "
        "along that window (the SantaLucia 1998 nearest-neighbour thermodynamics), then turns that "
        "<span class=\"mono\">&gamma;</span> into the promoter's switch stiffness through the <em>frozen engine's "
        "own</em> functions: <span class=\"mono\">|h_sp| = spinodal(&gamma;) = 2(&gamma;/3)<sup>1.5</sup></span> "
        "and <span class=\"mono\">barrier = &gamma;&sup2;/4</span>. The reads span a real range, and that range "
        "tells its own story. The <strong>stiffest</strong> promoters in the whole set are the "
        "<em>out-of-reach</em> genes and the <em>sparse L3</em> node: the O-axis scaffold "
        "<span class=\"mono\">SHANK3</span> at <span class=\"mono\">&gamma; &approx; 1.52</span> "
        "(<span class=\"mono\">|h_sp| &approx; 0.72</span>), the W-axis lamination gene "
        "<span class=\"mono\">RELN</span> (<span class=\"mono\">&gamma; &approx; 1.51</span>), and the serotonin "
        "transporter <span class=\"mono\">SLC6A4</span> (<span class=\"mono\">&gamma; &approx; 1.52</span>, "
        "<span class=\"mono\">|h_sp| &approx; 0.72</span>). The <strong>softest</strong> reads are the canonical "
        "<em>actionable E/I levers</em>: the sodium channel <span class=\"mono\">SCN2A</span> at "
        "<span class=\"mono\">&gamma; &approx; 1.20</span> (<span class=\"mono\">|h_sp| &approx; 0.50</span>, the "
        "softest in the set) and the calcium channel <span class=\"mono\">CACNA1C</span> "
        "(<span class=\"mono\">&gamma; &approx; 1.26</span>, <span class=\"mono\">|h_sp| &approx; 0.55</span>). In "
        "other words, promoter stiffness runs <strong>opposite</strong> to reachability and actionability here: "
        "the genes a chemical lever <em>cannot</em> touch read stiffest, and the genes it can touch read softest. "
        "These are read on the <strong>same R19 substrate, with the same engine, that the bipolar, epilepsy, "
        "depression, schizophrenia and analgesic packages used</strong>, which is the whole point of the "
        "inheritance: one substrate, one pipeline, now six problems. The <span class=\"mono\">&gamma;</span> read "
        "is a property of the gene's <strong>promoter sequence</strong>, blind to whether the gene is on or off "
        "and to gain / loss / expression level, and that is <em>all</em> it is.</p>",
    ]),

    "<h2>Ranking targets, the autism unmet-need signature, and the firewall that keeps gamma honest</h2>",
    "".join([
        "<p>The last component prioritises, and it prioritises <strong>targets, never drugs or doses</strong>, over "
        "the <strong>ten lever genes only</strong> &mdash; the six out-of-reach genes are not ranked, because "
        "ranking a target you have already declared unreachable would be incoherent. A burden-weighted score "
        "combines three declared, cited weights &mdash; clinical burden (<span class=\"mono\">0.40</span>), unmet "
        "need (<span class=\"mono\">0.35</span>), and genetic-evidence / druggability (<span class=\"mono\">0.25</span>) "
        "&mdash; on cited 1&ndash;5 tiers. The <strong>autism signature</strong> shows up immediately in the "
        "unmet-need tier: there is <strong>no approved pharmacology for the core features</strong> of autism &mdash; "
        "the only licensed agents target the irritability <em>adjunct</em>, not the social-communication core or "
        "the E/I set-point itself &mdash; so, unlike schizophrenia (where the established D2 route drove the D2 "
        "receptor's unmet need <em>low</em>), <strong>no autism gene has its unmet need lowered by an established "
        "core route</strong>. The unmet-need floor here is higher than in any prior levers chapter; need is "
        "uniformly high. The substantive consequence is that the <strong>L2 inhibitory-restore route surfaces as "
        "the cleanest actionable direction</strong>: the GABA-A &beta;3 subunit <span class=\"mono\">GABRB3</span> "
        "tops the actionable ranking, and the top actionable set is dominated by the L2 genes "
        "(<span class=\"mono\">GABRB3</span>, <span class=\"mono\">GABRA5</span>, <span class=\"mono\">KCNQ3</span>, "
        "<span class=\"mono\">GABRA2</span>) &mdash; not because L2 scores highest in the abstract, but because the "
        "high-scoring L1 excitatory genes are flagged <strong>not actionable by the generic sign</strong>: "
        "<span class=\"mono\">SCN2A</span> and <span class=\"mono\">GRIN2B</span> because their gain/loss "
        "sign-subtlety makes &lsquo;reduce excitation&rsquo; a non-clean direction, and "
        "<span class=\"mono\">CACNA1C</span> because it is a cross-disorder calcium set-point rather than an "
        "autism-selective handle. Filtering to clean directions lifts the inhibitory-restore lever to the top: "
        "restoring inhibition raises the fold regardless of variant direction, whereas reducing excitation runs "
        "straight into the sign problem. The single L3 node <span class=\"mono\">SLC6A4</span> is flagged "
        "not-actionable (non-monotone) and ranks last.</p>",
        "<p>Crucially, the <span class=\"mono\">&gamma;</span> read is carried <em>alongside</em> each target as "
        "structural context but is <strong>never folded into the score</strong> &mdash; and the result is a clean "
        "demonstration of the firewall: the priority ranking and the <span class=\"mono\">&gamma; / |h_sp|</span> "
        "ranking are <strong>decoupled</strong>. The <strong>stiffest</strong> lever read in the set, the "
        "serotonin transporter <span class=\"mono\">SLC6A4</span> (<span class=\"mono\">|h_sp| &approx; 0.72</span>), "
        "sits at the <strong>bottom</strong> of priority and is non-actionable; the <strong>top-priority</strong> "
        "target <span class=\"mono\">GABRB3</span> has only a <em>mid-range</em> read "
        "(<span class=\"mono\">|h_sp| &approx; 0.64</span>). If promoter stiffness drove the ranking, neither could "
        "sit where it does &mdash; and across the full sixteen-gene set the decoupling is even starker, since the "
        "stiffest reads are the out-of-reach <span class=\"mono\">SHANK3</span> and <span class=\"mono\">RELN</span> "
        "while the softest are the actionable <span class=\"mono\">SCN2A</span> and <span class=\"mono\">CACNA1C</span>. "
        "That decoupling is the firewall made visible, and it must be stated once more in full: the promoter "
        "<span class=\"mono\">|h_sp|</span> is a gene's <strong>own switch stiffness</strong>, and it is "
        "<strong>never</strong> equated with the §18 network over-excitation threshold on <span class=\"mono\">R</span>, "
        "nor with a receptor occupancy, a synaptic level, a compound's potency, a dose, an in-vivo selectivity, or "
        "any clinical effect. A <strong>fail-closed forbidden-claim scanner</strong> guards the whole package, and "
        "for autism it is the strictest in the series: beyond the usual dose / efficacy-as-fact / safety-as-fact / "
        "synthesis classes, it adds an autism <strong>quackery</strong> class &mdash; it rejects "
        "<em>chelation</em>, <em>MMS</em> / <em>miracle-mineral</em> / <em>chlorine-dioxide</em> bleach-protocol "
        "vocabulary outright, because that industry has harmed autistic children &mdash; and a "
        "<strong>normalise-framing</strong> class that rejects <em>cure-autism</em>, <em>reverse-autism</em>, and "
        "<em>make-normal</em> language, because autism is a neurodevelopmental <strong>difference</strong>, not "
        "only a deficit, and the map must never emit a disrespecting frame. Each class carries a planted self-test "
        "that <em>must</em> fire on its own bait, failing the build if it ever does not. This module reproduces "
        "bit-for-bit with the engine byte-unchanged.</p>",
        "<p>Everything here is an in-silico <em>reading</em> of promoter sequence and a <em>frame</em> for "
        "organising targets, not a clinical measure, a diagnosis, or a prescription. The model asserts "
        "<em>mechanism directions and target placements</em> &mdash; an over-excitation fold can be raised by "
        "reducing inward current or restoring inhibition; these ten genes populate the levers; autism loads them "
        "L1-dominantly with a sparse L3; the map reaches the excitability axis only; the output and wiring axes are "
        "named and out of reach, the wiring axis provably so; restoring inhibition is the cleanest actionable "
        "direction because the excitatory channels are gain/loss sign-subtle &mdash; and <strong>nothing</strong> "
        "about which agent acts on any lever, at what dose, in whom, whether any real compound changes anyone's "
        "traits, or that anyone should change anything. The agents named as <em>directions</em> are illustrations "
        "of a <em>sign</em>, never a recommendation, and the recorded caveats (the gain/loss sign-subtlety of "
        "<span class=\"mono\">SCN2A</span> and <span class=\"mono\">GRIN2B</span>, the seizure edge of an "
        "over-pushed T lever, the non-monotone serotonergic node) are there precisely because a generic lever sign "
        "is <strong>not</strong> a clinical direction. Real autism is heterogeneous and is <strong>three axes</strong>, "
        "not one &mdash; excitability, output, and wiring &mdash; and that heterogeneity, including the two axes "
        "this lever map explicitly <em>cannot</em> reach, is <strong>locked</strong>. Autism is a neurodevelopmental "
        "<strong>difference, not only a deficit</strong>; this chapter ranks where a clean unmet mechanistic "
        "direction exists, and it does <em>not</em> assert that any direction treats, normalises, or cures autism. "
        "A promoter read and a lever assignment are mechanism boundaries, <strong>not</strong> a claim about the "
        "felt quality of an autistic mind (Axis-A firewall &mdash; <span class=\"mono\">consciousness_claim = 0</span>, "
        "the hard problem stays <strong>open</strong>). <strong>This is not medical advice, not a diagnosis, not a "
        "treatment protocol, and not a cure.</strong> <span class=\"mono\">medium_efficacy_tested = 0</span>; "
        "targets ranked, never drugs or doses.</p>",
    ]),
])

PREV = '<a rel="prev" href="/mind/33-schizophrenia-threshold-levers/">&larr; §33 Schizophrenia: three threshold levers</a>'
NEXT = '<a rel="next" href="/mind/35-adhd-threshold-levers/">§35 ADHD: drive-tone levers &rarr;</a>'

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
