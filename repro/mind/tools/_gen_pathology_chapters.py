#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_gen_pathology_chapters.py — emit the six Part-II pathology chapters (autism + theta-cap + ADHD).

Writes docs/mind/<slug>/index.html for each chapter from the per-chapter content below, using one
shared head/JSON-LD/footer template so the SEO scaffolding is byte-consistent. The answer-first
<p class="answer"> and the vp-card asides are NOT written here — build_search_layer.py injects them
from mind_registry.py (single source of truth). Body text is English-only (VP-SPEC C0).

This is a one-shot authoring helper; the emitted HTML is the canonical artifact.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(HERE, os.pardir))
MIND = os.path.join(PKG, "docs", "mind")
DOI = "10.5281/zenodo.20694404"
ORCID = "0009-0002-7535-8245"
PAPER = "Felt Cognition: Parallel Micro-Eddies, the Stream of Thought, and the Open Problem of Experience"
GH = "https://github.com/rego093-sketch/jamming-physics/tree/main/repro/mind"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag} — Felt Cognition §{no} | Jamming Physics</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="https://jamming-physics.org/mind/{slug}/">
<link rel="stylesheet" href="/assets/css/site.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"ScholarlyArticle",
 "headline":"{headline}",
 "isPartOf":{{"@type":"CreativeWork","name":"{paper}",
   "sameAs":"https://doi.org/{doi}"}},
 "position":{no},
 "author":{{"@type":"Person","name":"Young Jae Lee",
   "sameAs":"https://orcid.org/{orcid}"}},
 "license":"https://creativecommons.org/licenses/by/4.0/"}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
 {{"@type":"ListItem","position":1,"name":"Home","item":"https://jamming-physics.org/"}},
 {{"@type":"ListItem","position":2,"name":"Felt Cognition","item":"https://jamming-physics.org/mind/"}},
 {{"@type":"ListItem","position":3,"name":"\\u00a7{no} {crumb}"}}]}}
</script>
</head>
<body>
<header><nav class="crumb"><a href="/">Home</a> &rsaquo; <a href="/mind/">Felt Cognition</a> &rsaquo; §{no}</nav></header>
<main>
<h1>{h1}</h1>
<p class="abstract">{abstract}</p>

<aside class="claim-strip">
  <span class="grade {gclass}">{grade}</span>
  <span class="gate">LOCK → Derive → Gate</span>
  <a href="{gh}/{slug}/" rel="noopener">reproduce (GitHub)</a>
  <a href="https://doi.org/{doi}" rel="noopener">DOI snapshot</a>
</aside>
{body}
<nav class="pn">
  {prev}
  <a href="/mind/">paper contents</a>
  {next}
</nav>
</main>
<footer>DOI <a href="https://doi.org/{doi}">{doi}</a> · ORCID <a href="https://orcid.org/{orcid}">{orcid}</a> · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></footer>
</body>
</html>
"""

GRADE_CLASS = {"model": "grade g-calibrated", "open": "grade g-open", "verified": "grade g-verified"}


def sec(h2, paras):
    out = [f"<h2>{h2}</h2>"]
    for p in paras:
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Per-chapter content. FW = the standing firewall sentence reused where needed.
# ---------------------------------------------------------------------------
FW = ('Every fraction and coupling value here is an <strong>in-silico coupling state</strong>, '
      'not a clinical response rate or a dose; <span class="mono">efficacy = 0</span> throughout. '
      'This is a mechanism-level result about the fault structure of autism <em>as represented in '
      'the VP framework</em> &mdash; not medical advice, a diagnosis, a treatment protocol, or a cure.')

CH = []

# ===== §18 — Autism as a three-axis fault =====
CH.append(dict(
    no=18, slug="18-autism-three-axis", grade="model",
    title_tag="The autism fault, in three axes",
    headline="Autism as a three-axis fault: threshold, gain, wiring",
    crumb="The autism fault in three axes",
    h1="Autism as a three-axis fault &mdash; threshold, gain, and wiring",
    meta=("Autism modeled on the emerged cerebrum as three separable faults — an E-I threshold (T), "
          "an output/gain (O), and a long-range wiring (W) fault — each with a distinct, "
          "bit-reproducible fingerprint in synchrony, theta-gamma coupling, and ignition. efficacy=0; "
          "not medical advice."),
    abstract=("This chapter applies the paper&rsquo;s pathology faculty (<a href=\"/mind/17-faculties-of-mind/\">F10</a>) "
              "to autism on the same emerged, measured cerebrum the rest of the paper builds. Autism is read not as one "
              "lesion but as <strong>three separable faults</strong> on the coordination substrate: a threshold (E-I) fault "
              "<strong>T</strong>, an output/gain fault <strong>O</strong>, and a long-range wiring fault <strong>W</strong>. "
              "Seventeen real autism risk genes, each carrying a measured stacking-energy &gamma;, sort onto the three axes, "
              "and each axis leaves a distinct, bit-reproducible fingerprint in global synchrony, &theta;&ndash;&gamma; coupling, "
              "and ignition. The model asserts the fingerprints; <em>which</em> axis any individual&rsquo;s autism is remains open."),
    sections=[
        ("Why three axes and not one",
         ["Autism is behaviourally one diagnosis but mechanistically heterogeneous, so the model does not posit a single broken part. "
          "It takes the emerged cerebrum of <a href=\"/mind/13-em-coordination/\">§13</a> &mdash; twelve central organs coupled only by "
          "the measured ephaptic near-field at the measured strength &kappa;&nbsp;=&nbsp;0.5496 &mdash; and asks the narrow question it can "
          "answer: in how many <em>mechanically distinct</em> ways can that coordination fail? The answer the dynamics give is three, and "
          "they are separable because they act on different terms of the same coupling.",
          "A <strong>threshold (T)</strong> fault raises the excitability fold &mdash; the E-I balance shifts so an assembly needs more drive "
          "to ignite. An <strong>output (O)</strong> fault lowers the drive each node delivers (the coupling numerator falls) without moving "
          "the fold. A <strong>wiring (W)</strong> fault leaves both the fold and the per-node drive intact but changes the <em>geometry</em>: "
          "local edges over-connect and long-range edges under-connect. The three are not three names for low synchrony; they are three "
          "different operators on the same equation, and that is why a single readout cannot tell them apart but two can."]),
        ("The cohort: seventeen risk genes, each with a measured &gamma;",
         ["The axes are not assigned by hand. A pre-registered cohort of seventeen autism risk genes &mdash; fifteen drawn from the "
          "verified risk-gene atlas and two fetched live from NCBI RefSeq (GABRA5, MACROD2) &mdash; is read through the same pipeline the "
          "organs use: the promoter window [TSS&minus;2000, TSS+500] (2501&nbsp;bp, coding strand) gives a mean nearest-neighbour stacking "
          "energy &gamma; by SantaLucia&nbsp;1998. The cohort is deliberately <strong>moderate-or-below</strong>: severe developmental and "
          "epileptic-encephalopathy syndromes (CHD8, FOXG1, FMR1, GRIN2B, DYRK1A and the like) are pre-registered out, because forcing a "
          "single profound-pole master onto the cohort would overclaim. What is kept is the legible, axis-mappable end.",
          "Each gene&rsquo;s mechanism places it on one axis: the <strong>T</strong> axis carries the ion and GABA-A levers (CACNA1C, GABRA2, "
          "GABRA5, GABRB3, KCNQ3, SCN2A); the <strong>O</strong> axis carries the synaptic-gain scaffolds and splice/output regulators "
          "(CTTNBP2, MACROD2, NRXN1, RBFOX1, SHANK2, SHANK3, SYNGAP1); the <strong>W</strong> axis carries the adhesion and lamination genes "
          "that build long-range connections (CNTN6, CNTNAP2, DSCAM, RELN). Mapping mechanism to axis is the only interpretive step; the "
          "&gamma; values themselves are measured and re-derive offline bit-for-bit."]),
        ("The fingerprint: what each fault does to the field",
         ["Run on the cohort cerebrum, the three faults all pull global synchrony below the healthy metastable value "
          "(R<sub>health</sub>&nbsp;=&nbsp;0.390): the output fault settles at R&nbsp;=&nbsp;0.354, the threshold fault at R&nbsp;=&nbsp;0.366, "
          "the wiring fault at R&nbsp;=&nbsp;0.340. If R were the only instrument, the three would be a smear. They are not, because "
          "&theta;&ndash;&gamma; phase&ndash;amplitude coupling (PAC) and the ignition threshold separate them.",
          "The decisive observable is the pair <strong>(&Delta;PAC, ignition)</strong>. The <strong>O</strong> fault drops PAC and keeps the "
          "ignition fold normal. The <strong>T</strong> fault drops PAC and <em>raises</em> the ignition fold &mdash; the signature of a shifted "
          "E-I balance. The <strong>W</strong> fault is the clean one: its PAC is <em>unchanged</em>, equal to health to within the simulation&rsquo;s "
          "precision, and its fold stays normal, while a locality imbalance (local-over, long-range-under) appears that the other two do not "
          "have. So &Delta;PAC&nbsp;&lt;&nbsp;0 with a raised fold is T; &Delta;PAC&nbsp;&lt;&nbsp;0 with a normal fold is O; &Delta;PAC&nbsp;=&nbsp;0 "
          "is W. The fingerprint is exact and reproduces under SEED&nbsp;=&nbsp;19."]),
        ("What is forced, and what stays open",
         ["Two things are owed in the open register, and naming them is the same no-tuning discipline that lets the rest stand. First, "
          "<strong>O and T are degenerate at the coupling level</strong> &mdash; both scale the same &kappa; &mdash; and separate only at the "
          "fold; distinguishing them in a real brain therefore needs an excitability or ignition measure (a TMS&ndash;EEG threshold), not a "
          "spectral one alone. Second, and more important, the model asserts the <em>fingerprints and their reversibility</em>, <strong>not "
          "which fault any individual&rsquo;s autism is</strong>. That mapping requires per-person external data &mdash; connectome, spectrum, "
          "genetics &mdash; and is held <span class=\"mono\">[O]</span>.",
          "This three-axis picture is the foundation the next chapters stand on. It already implies the clinical asymmetry the rest of Part&nbsp;II "
          "explores: because O and T are gain faults and W is a geometry fault, a chemical that shifts gain will behave very differently on the "
          "three &mdash; reaching some and only masking others (<a href=\"/mind/19-autism-chemical-limits/\">§19</a>). " + FW]),
    ],
    prev=("18", None), nxt=("19-autism-chemical-limits", "§19 What a chemical reaches"),
))

# ===== §19 — What a chemical can and cannot reach =====
CH.append(dict(
    no=19, slug="19-autism-chemical-limits", grade="model",
    title_tag="What a chemical can and cannot reach",
    headline="What a chemical can and cannot reach in autism",
    crumb="What a chemical can and cannot reach",
    h1="What a chemical can and cannot reach &mdash; mask versus correction",
    meta=("On the three-axis autism model a threshold-lowering (gain) chemical fully reverses the E-I "
          "fault, partly helps the output fault, and only MASKS the wiring fault by over-synchronisation "
          "— it cannot re-route geometry. Why a stimulant relieves some autism and not others. efficacy=0; "
          "not medical advice."),
    abstract=("A scalar, threshold-lowering chemical &mdash; the mechanism by which the catecholaminergic stimulant class "
              "raises gain &mdash; is applied to each of the three faults of <a href=\"/mind/18-autism-three-axis/\">§18</a>. "
              "It <strong>fully reverses</strong> the threshold fault, <strong>partly helps</strong> the output fault, and "
              "<strong>cannot correct</strong> the wiring fault: brute gain there raises synchrony a little but leaves the "
              "geometry untouched, so the long-range deficit is <em>masked by over-synchronisation</em>, not fixed. This is the "
              "model&rsquo;s account of why a stimulant relieves some presentations of autism and not others &mdash; and it is "
              "stated with <span class=\"mono\">efficacy = 0</span>: a mechanism, not a recommendation."),
    sections=[
        ("The operator: what a gain chemical actually is",
         ["A threshold-lowering chemical is, in the model, a <strong>scalar gain/bias operator</strong>: it lowers the fold or raises the "
          "per-node drive uniformly across the network. That is the right abstraction for the catecholaminergic stimulant class, which acts "
          "by raising excitability/gain. It is emphatically <em>not</em> a claim that any medication treats autism; it is a question about "
          "what a uniform gain change can and cannot do to each of the three faults. The honest reading is the user&rsquo;s own intuition tested: "
          "if a gain chemical relieves a deficit, that deficit had a <em>gain</em> component; if it cannot, the deficit is geometric."]),
        ("Threshold: fully reversed",
         ["On the <strong>T</strong> (threshold) fault the gain operator is exactly matched to the lesion. Lowering the fold restores the "
          "ignition threshold to normal and brings synchrony back to the healthy value (R returns to 0.390) with &theta;&ndash;&gamma; coupling "
          "restored. The fault was a shifted E-I balance and the chemical shifts it back. This is the cleanest case: a gain fault met by a gain "
          "operator, fully corrected in both R and the fold."]),
        ("Output: partly helped",
         ["On the <strong>O</strong> (output) fault the operator helps but does not complete. Raising the effective coupling lifts R only "
          "slightly (from 0.354 toward 0.357) because the deficit is in the drive the node delivers, not only in where the fold sits; uniform "
          "gain raises the denominator but cannot fully restore an output that is intrinsically low. So a gain chemical is partial here &mdash; "
          "real but incomplete &mdash; and that partiality is itself diagnostic: a deficit a gain chemical only half-reaches has an output "
          "component the threshold case does not."]),
        ("Wiring: masked, not corrected",
         ["On the <strong>W</strong> (wiring) fault the operator fails in the way that matters most. Brute uniform gain raises R from 0.340 to "
          "0.377 &mdash; still below health &mdash; but the <strong>locality is invariant</strong>: the local-over / long-range-under imbalance "
          "(0.842) is exactly unchanged. Scalar gain cannot re-route geometry; it can only drive the existing topology harder. Pushed far enough "
          "(coupling &times;2.0) synchrony does reach health, but only because the whole network is driven into <em>over-synchronisation</em> &mdash; "
          "PAC overshoots, the metastable regime is lost. That is a <strong>mask</strong>, not a correction: the coordination number looks healthier "
          "while the wiring that was broken is still broken, now hidden under a globally over-coupled state. A deficit that a gain chemical can "
          "<em>mask but not re-route</em> is, by this discriminant, a wiring fault."]),
        ("The selectivity question, and why it does not change the verdict",
         ["One might hope a more <em>selective</em> chemical &mdash; correcting only the faulted cells, sparing the rest &mdash; could do better. "
          "The model tests this directly: a blunt single lever, a selective single lever, and a split three-lever scheme. The result is sobering and "
          "honest. Where coverage is full, every scheme corrects the threshold fault <em>identically</em> &mdash; selectivity buys no extra efficacy. "
          "What the three-lever split does buy is a <strong>safety margin</strong>: it cuts the off-target push (0.083 versus 0.25) and widens the "
          "margin before an off-target cell is itself pushed into fault. That is a genuine but modest gain &mdash; a tolerability improvement, not a "
          "new capability &mdash; and it does nothing for the wiring axis, which no chemical lever in the scheme touches.",
          "So the chemical&rsquo;s reach is fixed and asymmetric: full on threshold, partial on output, mask-only on wiring. The wiring axis is left "
          "for a different kind of intervention entirely &mdash; one that supplies the missing long-range coordination directly rather than turning "
          "the gain up &mdash; which is where the &theta;-supply, and the &theta;-cap, enter (<a href=\"/mind/20-theta-cap-pacemaker/\">§20</a>). " + FW]),
    ],
    prev=("18-autism-three-axis", "§18 The three-axis fault"),
    nxt=("20-theta-cap-pacemaker", "§20 The θ-cap pacemaker"),
))

# ===== §20 — The theta-cap: pacemaker for the wiring axis =====
CH.append(dict(
    no=20, slug="20-theta-cap-pacemaker", grade="model",
    title_tag="The θ-cap: a pacemaker for the wiring axis",
    headline="The theta-cap: an external pacemaker for the wiring axis",
    crumb="The θ-cap: a pacemaker for the wiring axis",
    h1="The &theta;-cap &mdash; an external pacemaker for the wiring axis",
    meta=("A wearable theta carrier (theta-tACS) is the only handle on the wiring axis no chemical "
          "reaches — but only as an external pacemaker, not a benign extra lane: it forces long-range "
          "coordination inside a narrow window, is cleanly removable with no dependence, and is "
          "molecularly safe below the spinodal fold. efficacy=0; not medical advice."),
    abstract=("The wiring fault needs the long-range coordination supplied directly. A reviewer proposed reading that supply "
              "as a wearable <strong>&theta;-cap</strong> (a &theta;-band tACS device) and asked three fair questions, answered here "
              "one experiment at a time: is its coupling a <em>benign extra lane</em> or a coherence-forcing pacemaker; is the function "
              "it supplies <em>removable</em>; and does years of carrier cause <em>molecular fatigue</em>? The verdicts: it is a "
              "<strong>pacemaker, not a lane</strong> (the keystone negative); it is <strong>cleanly removable</strong> because it paces "
              "rather than repairs; and it is <strong>molecularly safe</strong> &mdash; the binding danger is circuit over-synchronisation, "
              "not molecular wear. <span class=\"mono\">efficacy = 0</span> throughout."),
    sections=[
        ("The keystone: a pacemaker, not a benign lane",
         ["The tempting reframing is that the cap is a harmless <em>additive lane</em> &mdash; you simply add a carrier channel on top of the "
          "broken substrate and it supplies an extra routing path. The model forks the cap&rsquo;s coupling four ways on the wiring-faulted cohort "
          "and asks which one actually routes. An <strong>external clock</strong> (a forced carrier, inj&middot;&Omega;<sub>0</sub>&middot;sin(&omega;t&minus;&theta;)) "
          "is the only coupling that lifts synchrony toward health &mdash; and only inside a narrow window, inj&nbsp;&asymp;&nbsp;0.08&ndash;0.10, "
          "tipping into over-synchronisation by inj&nbsp;&asymp;&nbsp;0.15. Every <em>passive</em> coupling is inert: a broadcast relay of the "
          "network&rsquo;s own mean phase never lifts R (R<sub>max</sub>&nbsp;0.346); a far-pair relay never lifts R (0.345), because the far-pair "
          "phases are near-random and there is nothing coherent to relay; a pure superposition cancels exactly.",
          "This is the decisive result of the whole θ-cap analysis: <strong>no passive lane routes on a broken substrate</strong>. A lane can only "
          "carry coherence that already exists, and the wiring fault <em>is</em> the loss of that coherence. The cap can work only by <em>forcing</em> "
          "coherence as an external pacemaker &mdash; which is why everything downstream is framed as a pacemaker crutch, never a repaired highway. "
          "The benign-lane reframing is refuted; refutations are findings."]),
        ("Removable: the function is supplied only while the cap is on",
         ["Using the winning external-clock coupling at the window amplitude, the model measures the long-range coordination the wiring fault "
          "destroys (far-pair coherence: health&nbsp;0.170, deficit&nbsp;0.050). With the cap <strong>on</strong>, far-coherence is restored to "
          "0.213 (at or above health) while global synchrony sits at the healthy metastable 0.393 &mdash; function restored <em>without</em> "
          "over-synchronisation. Cycled through OFF/ON/OFF/ON/OFF epochs with the phase carried continuously (so any acquired dependence would "
          "show), every ON epoch returns to health and every OFF epoch returns to the deficit: OFF-epoch drift 0.004, ON-epoch drift 0.005, no "
          "rebound undershoot, and the first fresh OFF epoch matches the last post-cycling one.",
          "The reason removability holds is the same reason no passive lane routed: the cap is <em>only</em> an additive drive term, and the "
          "oscillator substrate carries <strong>no plasticity variable</strong> &mdash; no slow weight, no memory that persists past the drive. "
          "Remove the drive and the intrinsic wiring deficit resumes instantly. The &ldquo;off during sleep, no dependence&rdquo; intuition is "
          "confirmed &mdash; but via the pacemaker mechanism, not a benign lane. The cap does not repair the wiring; the geometry is untouched."]),
        ("Molecularly safe: the substrate is more robust than the circuit",
         ["The slow-photodamage worry is tested where the whole framework rests &mdash; the R19 bistable switch (ds/dt&nbsp;=&nbsp;g&middot;s&nbsp;&minus;&nbsp;s&sup3;&nbsp;+&nbsp;h) "
          "&mdash; with the fatigue law <em>derived</em> from the switch&rsquo;s own dynamics and no new tuned constant. The switch&rsquo;s relaxation "
          "rate is &lambda;&nbsp;=&nbsp;2g, and the physiological &theta; carrier sits deep in the quasi-static regime "
          "(&Omega;&nbsp;=&nbsp;&omega;/&lambda;&nbsp;=&nbsp;0.018: the switch relaxes about 56&times; faster than the carrier cycles). Two fatigue "
          "observables follow. <strong>Irreversibly</strong>, below the spinodal fold the bare switch is a memoryless relaxor: cycling at the window "
          "amplitude (margin to the fold 0.425, about 8&times; the amplitude) never flips the basin <em>at any cycle count</em>; the first flip appears "
          "only at amplitude 0.70, past the fold &mdash; so the boundary on long-term use is an <em>amplitude</em> (the spinodal), not a cycle count. "
          "<strong>Reversibly</strong>, the only molecular cost is the per-cycle hysteresis loop, recovered each cycle, tiny in the quasi-static "
          "regime and scaling as amplitude&sup2;; duty-cycling (&ldquo;cap off during sleep&rdquo;) cuts the time-integrated load to about 4% of "
          "continuous strong drive.",
          "The deeper finding inverts the worry: across the entire sub-fold range there are <strong>zero</strong> irreversible events at any cycle "
          "count, so the cap&rsquo;s real failure mode is <strong>network over-synchronisation</strong>, not molecular damage. The binding constraint "
          "is the circuit, not the molecule. The engine contains no cumulative-damage variable, and inventing one would require a tuned constant that "
          "no-tuning forbids &mdash; so this is the faithful bound the actual dynamics give. " + FW]),
    ],
    prev=("19-autism-chemical-limits", "§19 What a chemical reaches"),
    nxt=("21-theta-cap-operating-principle", "§21 Operating principle & feasibility"),
))

# ===== §21 — Operating principle + physical feasibility =====
CH.append(dict(
    no=21, slug="21-theta-cap-operating-principle", grade="model",
    title_tag="The θ-cap operating principle, and its feasibility",
    headline="The theta-cap operating principle, and whether it is physically buildable",
    crumb="The θ-cap operating principle and feasibility",
    h1="The &theta;-cap operating principle &mdash; and whether it is physically buildable",
    meta=("If a theta-cap is to supply the wiring-axis function at all, the dynamics force one operating "
          "mode: minimum-effective, deficit-matched amplitude, applied continuously — a wearable drug with "
          "no half-life past removal. Plus a physical-feasibility review: every component (theta-tACS, "
          "closed-loop phase-locking, multi-electrode long-range montages) exists, the assembly does not. "
          "efficacy=0; not medical advice."),
    abstract=("Putting the four experiments of <a href=\"/mind/20-theta-cap-pacemaker/\">§20</a> and the population picture of "
              "<a href=\"/mind/23-virtual-trial/\">§23</a> together pins the operating point on all sides: drive at the "
              "<strong>minimum amplitude that produces a real routing change, matched to the individual wiring deficit, and do so "
              "continuously</strong>. Weaker is inert, stronger over-synchronises, intermittent reverts, and nothing is banked because "
              "the substrate has no plasticity. The cap is a <em>wearable drug with no half-life past removal</em>. This chapter states "
              "that forced operating principle, grades the one open variable (duty cycle), and then asks the engineering question the "
              "user posed directly: is such a device <strong>physically realisable today</strong>? Feasibility of the apparatus is graded "
              "<span class=\"mono\">[O]</span>, and is <em>not</em> evidence of benefit &mdash; <span class=\"mono\">efficacy = 0</span>."),
    sections=[
        ("The drug principle: effect present only during exposure",
         ["The cap restores the wiring-axis coordination only while it is on, with no carryover, no consolidation, and no acquired dependence "
          "(<a href=\"/mind/20-theta-cap-pacemaker/\">§20</a>). The pharmacokinetic analogy is not a metaphor here: the cap is an additive drive "
          "term and the substrate carries no state variable that persists past the drive, so the moment the drive stops the deficit dynamics "
          "resume in full. That is exactly a drug&rsquo;s kinetics &mdash; effect present only during exposure, zero residual after clearance. A "
          "pacemaker is a drug you wear instead of swallow."]),
        ("Minimum-effective is two-sided, and the amplitude must be matched",
         ["&ldquo;Minimum effective&rdquo; is a real constraint pinned on both sides, not a slogan for &ldquo;as weak as possible.&rdquo; Below the "
          "window the cap does <strong>nothing</strong>: only the coherence-forcing external clock routes, only inside inj&nbsp;&asymp;&nbsp;0.08&ndash;0.10, "
          "and a drive that produces no routing change is not gentle &mdash; it is absent. Above the window the cap <strong>over-synchronises</strong>: "
          "the over-sync fraction rises monotonically with amplitude and is minimised at the window (<a href=\"/mind/23-virtual-trial/\">§23</a>). And a "
          "<em>fixed</em> amplitude is itself wrong &mdash; a single window value over-syncs the milder-deficit cases &mdash; so the amplitude must be "
          "<strong>matched to the individual wiring deficit</strong>, the smallest value inside that person&rsquo;s routing window. The safe band is "
          "narrow and deficit-specific."]),
        ("Therefore: minimum-effective, matched, continuous &mdash; and why it is the only mode",
         ["Every alternative is closed. <strong>Chemistry cannot do it</strong>: no chemical reaches the wiring axis "
          "(<a href=\"/mind/19-autism-chemical-limits/\">§19</a>); the cap-type &theta;-supply is the only handle on W. <strong>There is no permanent "
          "repair in the model</strong>: the substrate has no plasticity, so the benefit cannot be banked and must be continuously supplied. "
          "<strong>Over and under both fail</strong>: weaker is inert, stronger over-syncs &mdash; there is no safe high dose and no set-it-low-and-forget-it. "
          "<strong>Intermittent reverts</strong>: a gap in dosing is a gap in function. So the mode is forced &mdash; the minimum effective, "
          "deficit-matched amplitude, applied continuously &mdash; and it is also the molecularly safe operating point, since the sub-fold carrier "
          "accumulates no irreversible fatigue and the gentlest amplitude is also the lowest thermal cost (<a href=\"/mind/20-theta-cap-pacemaker/\">§20</a>)."]),
        ("The one open variable: duty cycle and plasticity [O]",
         ["The principle fixes the amplitude and the necessity of ongoing dosing unconditionally. It leaves <strong>one</strong> variable open, and "
          "honesty requires grading it <span class=\"mono\">[O]</span> rather than asserting it: must dosing be strictly continuous, or could it relax "
          "to periodic re-dosing? This model answers <em>strictly continuous</em> &mdash; because it has no plasticity. But the real-world rationale for "
          "low-intensity stimulation is precisely that its effects can outlast the stimulation through synaptic plasticity. If gentle, correctly-phased "
          "pacing induced lasting potentiation of the broken long-range edges, the duty cycle could relax to periodic re-dosing as that after-effect "
          "decays. Three qualifications keep this firmly open: this model cannot show it (no plasticity variable, by construction); reported "
          "after-effects decay over tens of minutes to a couple of hours, not permanently; and even at its best the <em>drug principle still holds</em> "
          "&mdash; the effect must be re-supplied, only the interval is open. Crucially, the <em>sign</em> of any such plasticity is set by the cap&rsquo;s "
          "<strong>phase</strong>: in-phase coupling potentiates a connection, anti-phase depotentiates it &mdash; so a plasticity-aware cap could in "
          "principle repair <em>or further damage</em> the wiring depending on phase. That is a reason for caution, not optimism."]),
        ("Is it physically buildable? A feasibility review [O]",
         ["The user asked the engineering question plainly: granting the model, is such a device realisable now? The honest answer is that <strong>every "
          "component the operating principle demands exists today in research form, but the specific assembly does not &mdash; and feasibility of the "
          "apparatus says nothing about benefit.</strong> Take the demands one by one. A <em>&theta;-band oscillatory drive</em> is transcranial "
          "alternating current stimulation (tACS) in the theta band, a low-intensity sinusoidal current that entrains oscillations &mdash; routine. A "
          "<em>structured, forced</em> carrier (the model&rsquo;s decisive requirement, since passive lanes are inert) is closed-loop, phase-locked "
          "EEG-tACS, which tracks the instantaneous phase of the ongoing rhythm and drives in-phase &mdash; demonstrated, including the in-phase / "
          "anti-phase contrast. A drive that targets <em>long-range coordination</em> rather than one spot is multi-electrode, phase-shifted tACS, "
          "developed specifically to alter between-area connectivity, where in-phase stimulation increases coordination and anti-phase disorganises it "
          "&mdash; the same sign rule the plasticity caution above turns on; such montages have even produced a moving &ldquo;travelling-wave&rdquo; field, "
          "echoing the paper&rsquo;s own §13 result. <em>Individualised</em> targeting is standard practice: subject-specific MRI-optimised montages, an "
          "individual carrier frequency, and intensities kept below the sensation threshold. And <em>continuous, wearable</em> delivery exists as "
          "cap-style home tACS systems, tele-supervised, with per-electrode currents held below conventional safety limits.",
          "So the parts are real. What is <em>not</em> real is the combination the principle requires all at once: individualised <em>and</em> "
          "phase-structured <em>and</em> amplitude-windowed <em>and</em> network-targeted on the broken long-range edges specifically <em>and</em> "
          "continuous. Four obstacles keep this <span class=\"mono\">[O]</span>. (1) <strong>No deficit readout.</strong> The principle demands an "
          "amplitude matched to the individual wiring deficit, but there is no validated in-vivo measure of &ldquo;that person&rsquo;s wiring deficit&rdquo; "
          "to set the window &mdash; the matching target is currently unmeasurable. (2) <strong>The narrow window is a real risk.</strong> The same dynamics "
          "that make the cap work make over-shooting it over-synchronise the network &mdash; the seizure analogue &mdash; so an un-titrated or open-loop "
          "device is not merely ineffective but potentially harmful. (3) <strong>Spatial targeting of the broken edges</strong> at depth and across "
          "distributed long-range pathways is at the edge of what scalp montages (and emerging temporal-interference methods) can do. (4) <strong>The "
          "plasticity sign problem</strong>: if after-effects exist, the wrong phase depotentiates rather than potentiates &mdash; the device could entrench "
          "the deficit. Above all, the model assigns <span class=\"mono\">efficacy = 0</span>: that the drive is buildable is a statement about hardware, not "
          "about whether wearing it helps anyone. " + FW]),
    ],
    prev=("20-theta-cap-pacemaker", "§20 The θ-cap pacemaker"),
    nxt=("22-adhd-vs-autism", "§22 ADHD vs autism"),
))

# ===== §22 — ADHD, and why it separates from autism =====
CH.append(dict(
    no=22, slug="22-adhd-vs-autism", grade="model",
    title_tag="ADHD, and why it separates from autism",
    headline="ADHD, and why it separates from autism",
    crumb="ADHD, and why it separates from autism",
    h1="ADHD &mdash; and why it separates from autism",
    meta=("An explicit gene-grounded ADHD substrate (gain/arousal axes, intact wiring) emerged on the same "
          "engine: a stimulant restores ADHD to health where it only partly helps autism, the theta-cap is "
          "redundant for ADHD but essential for autism's wiring, and on an AuDHD substrate the two compose. "
          "Why severe ADHD can look like autism, and why it is not. efficacy=0; not medical advice."),
    abstract=("Earlier work read ADHD only as a relabelled autism cohort; here it gets its own <strong>explicit, gene-grounded "
              "substrate</strong>. Eight ADHD genes &mdash; six on the output/gain axis, two on the arousal/threshold axis, "
              "with <strong>wiring intact</strong> as the discriminant &mdash; are emerged on the same read-only engine and run "
              "side-by-side with the autism cohort. Three results follow: the stimulant is for the gain axis (it fully restores "
              "ADHD, only partly autism), the cap is for the wiring axis (its long-range benefit is over three times larger where "
              "wiring is broken), and on an explicit <strong>AuDHD</strong> substrate the two compose without interference. This is "
              "the engine&rsquo;s account of why severe ADHD can look like autism, and why it is not the same fault. "
              "<span class=\"mono\">efficacy = 0</span>; the ADHD model&rsquo;s own validity is open."),
    sections=[
        ("An explicit ADHD substrate, not a relabelled cohort",
         ["The discriminating claim &mdash; that ADHD shares autism&rsquo;s gain/arousal surface but has <em>intact wiring</em> &mdash; only "
          "means something if the ADHD substrate is built from ADHD genes, not borrowed. Eight are used, each read through the same SantaLucia "
          "&gamma; pipeline (four fetched live from NCBI RefSeq). The <strong>output/gain (O)</strong> axis carries the catecholamine machinery: "
          "DRD4 (the 7-repeat ADHD locus), SLC6A3 (the dopamine transporter), COMT, DBH, TH (synthesis and catabolism), and SNAP25 (presynaptic "
          "release). The <strong>arousal/threshold (T)</strong> axis carries ADRA2A (the guanfacine target) and SLC6A4 (serotonergic tone). "
          "Critically, <strong>W&nbsp;=&nbsp;none</strong>: there is no wiring lever, and the axis-ambiguous or syndromic candidates (ADGRL3, FOXP2) "
          "are pre-registered <em>excluded</em> so that &ldquo;ADHD has intact wiring&rdquo; is airtight rather than assumed. The per-axis gain "
          "factors are inherited byte-for-byte from the autism work &mdash; no new tuned constant."]),
        ("The stimulant is for the gain axis",
         ["Side-by-side, the asymmetry is sharp. ADHD baseline synchrony (R&nbsp;=&nbsp;0.362) sits closer to health than autism&rsquo;s wiring-faulted "
          "0.322. On the <strong>intact</strong> ADHD geometry the stimulant (raising catecholamine gain) restores ADHD to health in <em>both</em> "
          "synchrony and &theta;&ndash;&gamma; coupling at a finite dose. On the <strong>broken</strong> autism geometry the same stimulant restores "
          "the &theta;&ndash;&gamma; coupling (the gain axis) but synchrony stays <em>capped below health</em> and the locality stays at the broken value "
          "&mdash; gain never touches the wiring. This reproduces the §19 result on an explicit ADHD substrate: a gain operator completes a gain fault and "
          "only masks a wiring fault."]),
        ("The cap is for the wiring axis",
         ["The complementary test is the cap. Its long-range (far-pair) benefit is <strong>3.3&times; larger</strong> where the wiring is broken "
          "(autism &Delta;far&nbsp;0.136) than where it is intact (ADHD&nbsp;0.041). On stimulant-restored states the cap still adds long-range routing to "
          "autism but little to ADHD &mdash; once the gain is restored, the ADHD highway is already intact, so the cap is redundant. The two operators are "
          "axis-appropriate mirror images: the stimulant fixes the gain axis ADHD owns, the cap fixes the wiring axis only autism has."]),
        ("They compose: the AuDHD substrate",
         ["The combination is tested where it should matter most: an explicit <strong>AuDHD</strong> cohort built from ADHD&rsquo;s gain/arousal genes "
          "<em>and</em> autism&rsquo;s wiring genes &mdash; a gain deficit on broken geometry. There the stimulant fixes the gain axis "
          "(&theta;&ndash;&gamma; coupling to health) and the cap fixes the routing axis (far-coherence 0.213); together they cover <em>both</em>, exceeding "
          "either alone, while synchrony (0.393) stays below the over-sync edge. Different axes, no interference. This is the model&rsquo;s account of two "
          "clinical facts at once: why <em>severe ADHD can look like autism</em> (they share the gain/arousal surface, so on that readout they blur), and "
          "why they are nonetheless <em>different faults</em> (autism carries gain/arousal <em>plus</em> wiring; ADHD carries gain/arousal alone)."]),
        ("What is owed",
         ["The honest debt is stated plainly: the engine has <strong>no separately-validated ADHD model</strong>. This chapter is a principled, "
          "gene-grounded <em>interpretation</em> &mdash; catecholamine genes onto the gain axis, intact wiring as the discriminant &mdash; that is "
          "internally tested and bit-reproducible, but whose mapping to clinical ADHD is held <span class=\"mono\">[O]</span>. The stimulant here is the "
          "mechanism by which the catecholaminergic class acts, not a claim that any medication treats either condition. " + FW]),
    ],
    prev=("21-theta-cap-operating-principle", "§21 Operating principle & feasibility"),
    nxt=("23-virtual-trial", "§23 The virtual trial"),
))

# ===== §23 — The virtual trial: who responds =====
CH.append(dict(
    no=23, slug="23-virtual-trial", grade="model",
    title_tag="The virtual trial: who the model says responds",
    headline="The virtual trial: who the model says responds, and who does not",
    crumb="The virtual trial",
    h1="The virtual trial &mdash; who the model says responds, and who does not",
    meta=("A synthetic population of 80 emerged cerebra with sampled fault mixes, run under stimulant, "
          "theta-cap, and both: stimulant responders are gain-dominated, non-responders are "
          "wiring-dominated and partly cap-rescuable, and an honest refutation shows the residual is a "
          "dose-cap/stiffness limit, not a severe-wiring tail. efficacy=0; not medical advice."),
    abstract=("The closing chapter of Part&nbsp;II runs the model across a <strong>heterogeneous synthetic population</strong> &mdash; "
              "eighty emerged cerebra, each with a sampled fault mix (wiring, gain, threshold) and stiffness spread &mdash; under the "
              "stimulant, the cap, and both, and reads off the <em>distribution</em> of outcomes. Stimulant responders are gain-dominated; "
              "non-responders are wiring-dominated and partly rescued by the cap; and a bundled sub-claim is <strong>refuted and promoted "
              "to a finding</strong>: the cap-unrescued residual is not a pure severe-wiring tail but a dose-cap / stiffness limit. Every "
              "fraction is an in-silico coupling-state outcome, <strong>not</strong> a clinical response rate &mdash; "
              "<span class=\"mono\">efficacy = 0</span>."),
    sections=[
        ("The population and what is measured",
         ["The population is eighty emerged cerebra (seventy-six affected), each assigned a sampled mix of wiring, gain and threshold severity plus a "
          "stiffness dispersion, with the patient geometry held <em>bit-faithful</em> to the autism endpoints (no wiring &rarr; health synchrony, full "
          "wiring &rarr; the wiring-deficit synchrony). Each is run under a dose-capped stimulant titrated to target, the cap at the window amplitude "
          "(duty-cycled), and both. The question is not &ldquo;does it work&rdquo; &mdash; efficacy is zero &mdash; but how the coupling-state outcomes "
          "<em>distribute</em> against the fault mix and the cap amplitude."]),
        ("Stimulant responders are gain-dominated",
         ["The stimulant-responder fraction falls monotonically across rising-wiring strata &mdash; 0.76, 0.42, 0.00 for low, mid and high wiring &mdash; "
          "and correlates negatively with the wiring share of the fault (r&nbsp;=&nbsp;&minus;0.60). This is the population image of the single-patient "
          "result: gain fixes the gain axis, not the wiring. A patient whose fault is mostly gain responds to the stimulant; a patient whose fault is "
          "mostly wiring does not."]),
        ("Over-synchronisation is an amplitude phenomenon",
         ["The adverse (over-sync) fraction rises monotonically with cap amplitude &mdash; 0.14, 0.57, 0.99, 1.0, 1.0 across inj 0.08/0.15/0.30/0.60/0.90 "
          "&mdash; and is <strong>minimised at the window</strong>. Amplitude sets the instantaneous adverse fraction; duty-cycling sets the cumulative "
          "exposure (the molecular load, per <a href=\"/mind/20-theta-cap-pacemaker/\">§20</a>). Together these say the same thing the operating principle "
          "says: the window amplitude is not a preference but the minimum that routes without over-syncing the milder cases."]),
        ("The honest refutation: the residual is a dose-cap, not a wiring tail",
         ["The core claim holds: stimulant-non-responders carry a higher wiring share (0.42) than responders (0.21), and the cap rescues 32% of them by "
          "pacing the missing long-range routing &mdash; removably, not as repair. But a <em>bundled exploratory sub-claim</em> &mdash; that the "
          "cap-unrescued residual is the pure severe-wiring tail &mdash; is <strong>refuted</strong>. Because the cap is axis-appropriate for wiring, it "
          "preferentially rescues the <em>more</em> wiring-dominated non-responders (cap-rescued mean wiring share 0.45 &gt; residual 0.40), so the residual "
          "is actually <em>less</em> wiring-dominated. The residual is instead dominated by patients whose unresolved deficit is gain/threshold beyond the "
          "stimulant&rsquo;s dose cap and/or high intrinsic stiffness dispersion &mdash; which neither the dose-capped stimulant nor the wiring-targeted cap "
          "addresses &mdash; plus a small high-wiring group that a <em>fixed</em> window amplitude over-synced.",
          "Two actionable points fall out, and both feed back into the operating principle. First, the two operators are cleanly axis-specific &mdash; cap "
          "to wiring, stimulant to gain &mdash; and what is left over is a dose-cap / stiffness limit, not a wiring tail. Second, the few over-syncs, together "
          "with the non-zero adverse fraction even at the window, argue for a cap amplitude <strong>matched to the individual wiring deficit</strong> "
          "(closed-loop, titrated), not held fixed &mdash; exactly the matched-amplitude requirement of "
          "<a href=\"/mind/21-theta-cap-operating-principle/\">§21</a>. Refutations are findings; this one sharpens the verdict rather than denting it. " + FW]),
    ],
    prev=("22-adhd-vs-autism", "§22 ADHD vs autism"),
    nxt=("23", None),
))


def render(c):
    body = "\n\n".join(sec(h, ps) for h, ps in c["sections"])
    prev_slug, prev_label = c["prev"]
    nxt_slug, nxt_label = c["nxt"]
    prev = (f'<a rel="prev" href="/mind/{prev_slug}/">&larr; {prev_label}</a>' if prev_label
            else '<span></span>')
    nxt = (f'<a rel="next" href="/mind/{nxt_slug}/">{nxt_label} &rarr;</a>' if nxt_label
           else '<span></span>')
    return HEAD.format(
        title_tag=c["title_tag"], no=c["no"], meta=c["meta"], slug=c["slug"],
        headline=c["headline"], paper=PAPER, doi=DOI, orcid=ORCID, crumb=c["crumb"],
        h1=c["h1"], abstract=c["abstract"], gclass=GRADE_CLASS[c["grade"]], grade=c["grade"],
        gh=GH, body=body, prev=prev, next=nxt)


def main():
    for c in CH:
        path = os.path.join(MIND, c["slug"], "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(render(c))
        print("wrote", c["slug"])


if __name__ == "__main__":
    main()
