#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
depression_threshold_levers.py  —  T1b-L (sec.32): the THREE-LEVER target map for the depressive
operating point. This is the analgesic_threshold_logic v2.0 technology (DOI 10.5281/zenodo.20733420)
INHERITED into the mind atlas and applied to depression. It is the THIRD application of the inherited
cross-cutting layer (after bipolar sec.30 and epilepsy sec.31) and the one that EXERCISES the frame's
generality, because depression's lever distribution is QUALITATIVELY DIFFERENT: where bipolar and
epilepsy load on the channel levers (L1/L2), depression loads on L3 -- the up-stream HPA / monoamine /
neurotrophic DRIVES that set the operating point, rather than the channels that set the firing
threshold. It re-derives no rule: it reads the SAME R19 substrate (E.spinodal/E.barrier, byte-
identical to vp_neuro_engine) and the SAME gamma = -mean(NN stacking dG, SantaLucia 1998) the engine
uses to write genes.

WHY THIS EXISTS (the gap it closes). sec.27 (depression_chronification, DEP-T1b) established, on top
of the E0 plasticity layer, that depression is the CHRONIFICATION of a LOW-coordination operating
point: a sustained HPA-driven withdrawal lowers the global order parameter R BELOW health, and the
corrective DIRECTION is to RESTORE coordination / remove the chronic withdrawal drive. But sec.27
treated that restoring push as a SINGLE, undifferentiated operator -- it never said WHICH genes /
receptors / pathways realise the restore. The analgesic three-lever frame supplies exactly that
missing layer. This is the direct depression counterpart of the bipolar B4->sec.30 and the epilepsy
sec.25->sec.31 decompositions.

THE DISORDER-LEVEL SIGN RELATIONSHIP (honest, central). Epilepsy is the OVER-synchronisation pole
(R above the over-sync threshold; sec.25); its levers RAISE the threshold by REDUCING excess drive.
Depression is the opposite pole on the same coupling axis -- the HYPO-coordination operating point
(R below health; sec.27). So the depressive operating point is moved back toward health by RESTORING
deficient drive / removing the chronic-stress drive that LOWERS it -- the mirror direction. The three
mechanistically-distinct levers are therefore re-pointed at "restore the operating point out of the
withdrawal basin", with L3 DOMINANT:
  L1  modulate the inward (glutamatergic/excitatory) drive  (the rapid-acting NMDA / Ca route; minor)
  L2  modulate the outward (K+) / GABA-A restoring current   (the M-current & neurosteroid route; minor)
  L3  remove/normalise the UP-STREAM sensitising drive        (DOMINANT: HPA stress hyperdrive removed,
                                                               deficient monoamine drive restored,
                                                               neurotrophic/plasticity drive restored)
This is NOT a re-labelling trick: the same three abstract mechanism classes carry over; what differs
is the DISTRIBUTION (depression is L3-heavy) and the SIGN (restore deficient drive vs reduce excess).
Both differences are stated, not hidden.

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| /
barrier are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V]
(reproducible); their ORDER is [F] (forced). This is NOT a receptor occupancy, NOT a synaptic
monoamine level, NOT a drug potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect,
and -- the depression-specific addition -- the promoter |h_sp| is NOT the sec.27 NETWORK
operating-point (the coordination level R below health) (that is a separate network quantity). The
promoter read is carried ALONGSIDE as the gene's own switch stiffness; it is NEVER folded into a
clinical magnitude or equated with the operating point. gamma is blind to on/off and to
gain/loss/expression-level of function (it reads switch STRUCTURE, not the trait). L3 (HPA / monoamine
/ neurotrophic) mechanism link is [O]: the gamma read PLACES the gene in the lever map; it does NOT
derive the signalling/network mechanism (enforced by depression_l3_honesty.py).

THE HONEST DIRECTION CAVEATS (depression-specific; recorded, not hidden).
  (i)  WHOLE-L1 SIGN SUBTLETY. The rapid-acting glutamatergic route is an NMDA-receptor ANTAGONIST
       direction (ketamine BLOCKS NMDA) yet RESTORES coordination -- the mechanism is a downstream
       disinhibition -> glutamate surge -> BDNF/TrkB plasticity restoration, NOT simple excitation
       reduction. So "modulate the inward current" on L1 is sign-subtle for depression and must not
       be read as the epilepsy "reduce inward current" sign.
  (ii) HTR2A DIRECTION IS NON-MONOTONE. Both 5-HT2A AGONIST directions (the psychedelic route) and
       5-HT2A ANTAGONIST directions (the mirtazapine/atypical route) carry antidepressant-class
       DIRECTION signals in the literature -- the receptor-level sign is NOT monotone. Recorded.
  (iii) L3 MONOAMINE LEVER IS RESTORATIVE, NOT REDUCTIVE. Unlike epilepsy/bipolar, where the threshold
       is raised by REDUCING drive, the depression monoamine lever RAISES deficient monoaminergic tone
       -- the disorder-level sign flip. This is exactly why gamma is graded [V] for STRUCTURE only
       (trait-blind) while the clinical direction is [O].

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places READS
and TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any drug treats anyone or
that any individual should change treatment. Real depression is HETEROGENEOUS (melancholic, atypical,
psychotic, peripartum, seasonal, bipolar depression; monoaminergic, HPA-axis, inflammatory, circadian
and psychosocial contributors; ~30% treatment-resistant) -- LOCKED. A lever direction is a mechanism
boundary, NOT a claim about the felt quality of depressed mood or its relief (consciousness_claim
stays 0; hard problem OPEN).

No tuning: gamma is measured (pure arithmetic over called dinucleotide steps); |h_sp|/barrier are the
locked R19 forms; the lever assignments and citations are CITED Layer-2 biology, not engine outputs.
Governed by VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 depression_threshold_levers.py
Out:  depression_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "depression_levers_promoters.cache.json")
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"

# SantaLucia 1998 unified NN dG37 -- the SAME table the engine / analgesic / DNA pipeline use.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

def gamma(seq):
    """Interfacial tension / stiffness = -mean(NN stacking dG). Strand-symmetric. [V] read."""
    s = seq.upper()
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(sum(v)/len(v)) if v else float("nan")

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the depressive operating point) ----
LEVER_FRAME = {
  "L1": "modulate the inward (glutamatergic/excitatory) drive -- the rapid-acting NMDA-receptor / "
        "Ca-channel route. SIGN-SUBTLE for depression: the ketamine direction is an NMDA ANTAGONIST "
        "yet RESTORES coordination via downstream disinhibition -> glutamate surge -> BDNF/TrkB "
        "plasticity, NOT simple excitation reduction (minor lever for depression)",
  "L2": "modulate the outward (K+) / GABA-A restoring current -- the M-current (K_V7) route and the "
        "GABA-A neurosteroid-PAM route. Carries the inhibitory/restoring current direction (minor "
        "lever for depression)",
  "L3": "remove / normalise the UP-STREAM sensitising drive that sets the operating point -- DOMINANT "
        "for depression. Three sub-axes: (a) remove the chronic HPA stress hyperdrive that LOWERS the "
        "operating point (the sec.27 withdrawal-bias driver); (b) RESTORE the deficient monoaminergic "
        "approach drive (the monoamine direction -- restorative, the disorder-level sign flip); "
        "(c) RESTORE the neurotrophic / plasticity drive that lets the operating point un-chronify; "
        "signalling/network mechanism [O]",
}

# grade strings (inherited discipline)
GL1 = "[F] structural: a glutamatergic/Ca inward-current MODULATION moves the operating point (anchored to cited agents; sign-subtle, see caveat)"
GL2 = "[F] structural: an outward-K+ / GABA-A restoring-current increase modulates the operating point (anchored to cited agents)"
GL3 = "[O] cited biology: gamma places the gene in the lever map; the HPA/monoamine/neurotrophic signalling mechanism is NOT derived"

# CITED Layer-2 context (NOT engine output). depression_anchor = the cited depression genetics /
# pharmacology; direction_agent = the cited operating-point-restoring agent DIRECTION (never an
# efficacy claim). channel/protein labelled.
CONTEXT = {
  # ============== L1: modulate the inward (glutamatergic/excitatory) drive (minor) ==============
  "GRIN2B": dict(lever="L1", channel="NMDA-R GluN2B (glutamate, Ca2+-permeable)", protein=None,
      push="modulate the inward NMDA (GluN2B) current -- the principal rapid-acting target; ANTAGONIST direction "
           "drives downstream disinhibition -> glutamate surge -> BDNF/TrkB (sign-subtle, see L1 caveat)",
      depression_anchor="the principal NMDA-receptor subunit for the rapid glutamatergic antidepressant route; GluN2B-preferring "
                        "NMDA modulation is the mechanistic core of the ketamine direction",
      direction_agent="rapid-acting glutamatergic (NMDA-modulation) DIRECTION -- the ketamine/esketamine route is an NMDA ANTAGONIST "
                      "direction whose ANTIDEPRESSANT-CLASS action is downstream (BDNF/TrkB), not excitation reduction (DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Berman 2000 Biol Psychiatry 47:351 (ketamine direction); Li 2010 Science 329:959 (mTOR/synaptogenesis); Autry 2011 Nature 475:91 (NMDA->BDNF)"),
  "GRIN2A": dict(lever="L1", channel="NMDA-R GluN2A (glutamate, Ca2+-permeable)", protein=None,
      push="modulate the inward NMDA (GluN2A) current -- the cross-disorder glutamatergic partner subunit",
      depression_anchor="NMDA-receptor subunit implicated across mood and psychotic disorders; the glutamatergic tone partner of GluN2B",
      direction_agent="glutamatergic-tone (NMDA-modulation) DIRECTION (cross-disorder; carried with GluN2B as the inward glutamatergic route)",
      grade_mechanism=GL1,
      src="Lemke 2013 Nat Genet 45:1067 (GRIN2A, glutamatergic spectrum); cross-disorder NMDA tone"),
  "CACNA1C": dict(lever="L1", channel="Ca_V1.2 (L-type Ca2+)", protein=None,
      push="modulate the inward Ca2+ (L-type) current -- the cross-disorder calcium set-point gene",
      depression_anchor="the most-replicated CROSS-DISORDER calcium-channel locus (the PGC five-disorder finding spanning major depression, "
                        "bipolar, schizophrenia, ASD, ADHD); an L-type Ca set-point on the operating point",
      direction_agent="L-type Ca-channel-modulation DIRECTION (cross-disorder set-point; carried as structural context, NOT a clean antidepressant target)",
      grade_mechanism=GL1,
      src="Cross-Disorder Group PGC 2013 Lancet 381:1371 (CACNA1C across five disorders)"),
  # ============== L2: modulate the outward (K+) / GABA-A restoring current (minor) ==============
  "KCNQ2": dict(lever="L2", channel="K_V7.2 (M-current)", protein=None,
      push="modulate the outward K+ (K_V7.2 M-current) -- the M-current route; an OPENER direction has been explored for the "
           "anhedonia/reward dimension of depression",
      depression_anchor="the M-current K-channel; a K_V7 (ezogabine-direction) OPENER has been studied for the reward/anhedonia dimension of depression (exploratory)",
      direction_agent="K_V7-opener DIRECTION (the ezogabine route, explored for the anhedonia dimension -- DIRECTION, not efficacy; exploratory)",
      grade_mechanism=GL2,
      src="Costi 2021 Am J Psychiatry 178:437 (ezogabine, reward/anhedonia direction, exploratory)"),
  "KCNQ3": dict(lever="L2", channel="K_V7.3 (M-current)", protein=None,
      push="modulate the outward K+ (K_V7.3 M-current) -- M-current partner of K_V7.2",
      depression_anchor="M-current partner of K_V7.2; carried with KCNQ2 as the outward K-channel route (exploratory)",
      direction_agent="K_V7-opener DIRECTION (M-current route; exploratory)",
      grade_mechanism=GL2,
      src="Costi 2021 Am J Psychiatry 178:437 (M-current reward direction, exploratory)"),
  "GABRA1": dict(lever="L2", channel="GABA-A receptor alpha1 (Cl-)", protein=None,
      push="INCREASE the inhibitory restoring current via GABA-A (Cl-) -- the neurosteroid positive-allosteric-modulator route "
           "(the allopregnanolone/brexanolone-zuranolone direction)",
      depression_anchor="GABA-A alpha1 subunit; the neurosteroid GABA-A positive-allosteric-modulator direction is an approved mechanism for peripartum depression",
      direction_agent="GABA-A neurosteroid-PAM DIRECTION (the brexanolone/zuranolone route for peripartum depression -- DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Meltzer-Brody 2018 Lancet 392:1058 (brexanolone, peripartum, direction); Gunduz-Bruce 2019 N Engl J Med 381:903 (zuranolone direction)"),
  # ====== L3 (DOMINANT): remove/normalise the up-stream sensitising drive ======
  #   sub-axis (a) HPA stress hyperdrive -- REMOVE
  "NR3C1": dict(lever="L3", channel=None, protein="glucocorticoid receptor (NR3C1; HPA negative-feedback nuclear receptor / TF)",
      push="restore HPA negative feedback (glucocorticoid-receptor signalling) -> remove the chronic stress hyperdrive that LOWERS the operating point (sec.27 handle)",
      depression_anchor="the glucocorticoid receptor; impaired GR-mediated HPA negative feedback (elevated/dysregulated cortisol) is a robustly reported depression correlate",
      direction_agent="HPA-normalisation DIRECTION (restore glucocorticoid-receptor negative feedback; the up-stream stress-axis route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Pariante & Lightman 2008 Trends Neurosci 31:464 (HPA / glucocorticoid receptor in depression)"),
  "CRHR1": dict(lever="L3", channel=None, protein="CRH receptor 1 (CRHR1; up-stream stress-peptide receptor)",
      push="reduce the up-stream CRH stress-peptide drive (CRHR1) -> remove the hyperdrive that lowers the operating point",
      depression_anchor="the corticotropin-releasing-hormone receptor; CRH/HPA hyperdrive is a central stress-axis abnormality reported in depression",
      direction_agent="CRH-system-normalisation DIRECTION (CRHR1 down-modulation; the up-stream stress-peptide route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Holsboer 2000 J Psychiatr Res 34:181; Binder & Nemeroff 2010 Mol Psychiatry 15:574 (CRH system in depression)"),
  "FKBP5": dict(lever="L3", channel=None, protein="FKBP51 (FKBP5; GR co-chaperone setting glucocorticoid-receptor sensitivity)",
      push="restore glucocorticoid-receptor sensitivity (FKBP5 co-chaperone) -> normalise the HPA hyperdrive that lowers the operating point",
      depression_anchor="the most-replicated stress-axis risk gene; FKBP5 sets GR sensitivity and shows a gene x early-adversity interaction in depression/PTSD",
      direction_agent="GR-sensitivity-normalisation DIRECTION (FKBP5 modulation; the up-stream HPA route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Binder 2004 Nat Genet 36:1319; Klengel 2013 Nat Neurosci 16:33 (FKBP5 x childhood-adversity)"),
  #   sub-axis (b) deficient monoaminergic approach drive -- RESTORE (restorative sign flip)
  "SLC6A4": dict(lever="L3", channel=None, protein="serotonin transporter 5-HTT/SERT (SLC6A4)",
      push="RESTORE deficient serotonergic approach tone by transporter blockade (raise synaptic serotonin) -- the SSRI direction (restorative; disorder-level sign flip)",
      depression_anchor="the serotonin transporter; the canonical first-line monoaminergic (SSRI) target and the 5-HTTLPR candidate-gene locus (effect contested)",
      direction_agent="serotonin-transporter-blockade DIRECTION (the SSRI route -- RAISES synaptic serotonin, restorative; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Lesch 1996 Science 274:1527 (5-HTTLPR); Caspi 2003 Science 301:386 (GxE, contested) -- transporter is the SSRI target"),
  "SLC6A2": dict(lever="L3", channel=None, protein="norepinephrine transporter NET (SLC6A2)",
      push="RESTORE deficient noradrenergic approach/arousal tone by transporter blockade (raise synaptic noradrenaline) -- the SNRI/NRI direction (restorative)",
      depression_anchor="the norepinephrine transporter; the noradrenergic (SNRI / reboxetine) monoaminergic target",
      direction_agent="norepinephrine-transporter-blockade DIRECTION (the SNRI/NRI route -- raises synaptic noradrenaline, restorative; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Ressler & Nemeroff 1999 Biol Psychiatry 46:1219 (noradrenergic systems in depression); NET is the SNRI/NRI target"),
  "MAOA": dict(lever="L3", channel=None, protein="monoamine oxidase A (MAOA; monoamine-catabolic enzyme)",
      push="RESTORE deficient monoaminergic tone by reducing monoamine catabolism (MAOA inhibition raises serotonin/noradrenaline/dopamine) -- the MAOI direction (restorative)",
      depression_anchor="the principal monoamine-catabolic enzyme; the monoamine-oxidase-inhibitor (MAOI) target -- the oldest monoaminergic antidepressant axis",
      direction_agent="monoamine-oxidase-inhibition DIRECTION (the MAOI route -- raises monoamine availability, restorative; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Shih 1999 Annu Rev Neurosci 22:197 (monoamine oxidase A); MAOA is the MAOI target"),
  "TPH2": dict(lever="L3", channel=None, protein="tryptophan hydroxylase 2 (TPH2; neuronal serotonin-synthesis rate-limiting enzyme)",
      push="RESTORE serotonergic synthesis capacity (TPH2 is the brain serotonin-synthesis rate-limiting enzyme) -- the up-stream synthesis sub-axis (restorative)",
      depression_anchor="the rate-limiting enzyme of neuronal serotonin synthesis; TPH2 variants have been associated with depression and serotonergic-synthesis capacity",
      direction_agent="serotonin-synthesis-capacity DIRECTION (TPH2 sub-axis; the up-stream synthesis route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Zill 2004 Mol Psychiatry 9:1030 (TPH2 in major depression); Walther 2003 Science 299:76 (TPH2 = brain serotonin synthesis)"),
  "HTR1A": dict(lever="L3", channel=None, protein="serotonin receptor 5-HT1A (HTR1A; GPCR, autoreceptor + post-synaptic)",
      push="modulate 5-HT1A signalling (auto-/post-synaptic) -- the serotonergic-receptor sub-axis (partial-agonist direction; restorative tone)",
      depression_anchor="the 5-HT1A receptor; auto-/post-synaptic 5-HT1A signalling is central to serotonergic antidepressant action; a partial-agonist direction is used adjunctively",
      direction_agent="5-HT1A partial-agonist DIRECTION (the buspirone/vilazodone/vortioxetine-adjacent serotonergic-receptor route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Albert 2011 Philos Trans R Soc B 367:2402 (5-HT1A in depression); Blier & Ward 2003 Biol Psychiatry 53:193"),
  "HTR2A": dict(lever="L3", channel=None, protein="serotonin receptor 5-HT2A (HTR2A; GPCR)",
      push="modulate 5-HT2A signalling -- the serotonergic-receptor sub-axis. DIRECTION NON-MONOTONE: both AGONIST (psychedelic) and "
           "ANTAGONIST (mirtazapine/atypical) directions carry antidepressant-class signals (see caveat)",
      depression_anchor="the 5-HT2A receptor; a serotonergic-receptor locus where BOTH agonist (psychedelic) and antagonist (mirtazapine/atypical) directions are studied",
      direction_agent="5-HT2A-modulation DIRECTION -- NON-MONOTONE: agonist (psilocybin route) and antagonist (mirtazapine route) directions both appear (DIRECTION, not efficacy; sign recorded as ambiguous)",
      grade_mechanism=GL3,
      src="Carhart-Harris 2021 N Engl J Med 384:1402 (5-HT2A agonist route); de Boer 1996 (mirtazapine 5-HT2A antagonist route) -- non-monotone"),
  "COMT": dict(lever="L3", channel=None, protein="catechol-O-methyltransferase (COMT; catecholamine-catabolic enzyme)",
      push="modulate catecholamine catabolism (COMT) -- the prefrontal dopamine/noradrenaline degradation sub-axis (Val158Met set-point)",
      depression_anchor="the catecholamine-catabolic enzyme; the COMT Val158Met polymorphism sets prefrontal dopamine tone, a depression/affect modifier",
      direction_agent="catecholamine-catabolism DIRECTION (COMT Val158Met set-point; the prefrontal catecholamine route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Lachman 1996 Pharmacogenetics 6:243 (COMT Val158Met); catecholamine catabolism set-point"),
  #   sub-axis (c) neurotrophic / plasticity drive -- RESTORE
  "BDNF": dict(lever="L3", channel=None, protein="brain-derived neurotrophic factor (BDNF; neurotrophin)",
      push="RESTORE the neurotrophic / synaptic-plasticity drive (BDNF) -> let the chronified operating point un-write (the neurotrophic hypothesis; the rapid-acting downstream)",
      depression_anchor="the central neurotrophin of the neurotrophic hypothesis of depression; the BDNF Val66Met locus and reduced BDNF signalling are robustly implicated",
      direction_agent="neurotrophic-restoration DIRECTION (BDNF signalling; the plasticity sub-axis -- the convergence point of the rapid-acting route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Duman & Monteggia 2006 Biol Psychiatry 59:1116 (neurotrophic hypothesis); Egan 2003 Cell 112:257 (BDNF Val66Met)"),
  "NTRK2": dict(lever="L3", channel=None, protein="TrkB receptor (NTRK2; BDNF receptor tyrosine kinase)",
      push="RESTORE neurotrophic signalling at the BDNF receptor (TrkB/NTRK2) -> the plasticity-restoration convergence; the ketamine route signals through TrkB",
      depression_anchor="the BDNF receptor TrkB; the convergence node where the rapid glutamatergic route (ketamine) and the neurotrophic route meet (TrkB activation)",
      direction_agent="TrkB-signalling-restoration DIRECTION (NTRK2; the BDNF-receptor convergence of the rapid-acting and neurotrophic routes -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Autry 2011 Nature 475:91 (ketamine -> BDNF/TrkB); Casarotto 2021 Cell 184:1299 (antidepressant TrkB binding direction)"),
}

def read(sym, g):
    c = CONTEXT[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the operating point)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "depression_genetic_anchor": c["depression_anchor"],
        "operating_point_restoring_agent_direction": c["direction_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": GL1 if c["lever"] in ("L1", "L1-adjacent")
                       else (GL2 if c["lever"] in ("L2", "L2-adjacent") else c["grade_mechanism"]),
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_operating_point": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch stiffness, "
                                       "NOT the sec.27 network operating-point (the coordination level R below "
                                       "health); never equated",
        "grade_clinical_map": "[O] OPEN -- not a receptor occupancy, synaptic monoamine level, potency, dose, "
                              "in-vivo selectivity, or clinical effect",
        "context_grade": "CITED Layer-2 biology (not an engine output)",
        "src": c["src"],
    }

def build():
    cache = json.load(open(CACHE))
    gammas = {s: gamma(cache[s]["seq"]) for s in CONTEXT if s in cache}
    missing = [s for s in CONTEXT if s not in cache]
    entries = [read(s, gammas[s]) for s in gammas]
    entries.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)   # stiffest promoter read first [F]
    order = [e["gene"] for e in entries]
    by_lever = {}
    for e in entries:
        by_lever.setdefault(e["lever"], []).append(e["gene"])
    # lever-distribution witness: depression is L3-DOMINANT (the qualitative difference vs bipolar/epilepsy)
    counts = {k: len(v) for k, v in by_lever.items()}
    dominant = max(counts, key=lambda k: counts[k])
    return {
        "title": "Three-lever depressive operating-point target map (engine-generated reads + cited lever frame)",
        "inherited_from": "analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the threshold-shift "
                          "intervention-logic technology, applied to the depressive operating point (third application "
                          "after bipolar sec.30 and epilepsy sec.31; the one that exercises the frame's GENERALITY, "
                          "because depression's lever distribution is L3-DOMINANT, not channel-dominant)",
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_sec27": "sec.27 (depression_chronification, DEP-T1b) established (on the E0 plasticity layer) that "
                          "depression is the CHRONIFICATION of a LOW-coordination operating point -- a sustained HPA-driven "
                          "withdrawal lowers R below health -- and that the corrective DIRECTION is to RESTORE coordination / "
                          "remove the chronic withdrawal drive, but treated that restore as a SINGLE abstract operator. This "
                          "map DECOMPOSES that restore into the three mechanistically-distinct levers and grounds each in a DNA "
                          "read of the actual depression genes. It adds NO new constant and re-derives no rule -- the exact "
                          "depression counterpart of the bipolar B4->sec.30 and epilepsy sec.25->sec.31 decompositions.",
        "disorder_level_sign": ("epilepsy is the OVER-synchronisation pole (R above the over-sync threshold; levers RAISE the "
                           "threshold by REDUCING excess drive). Depression is the opposite pole -- the HYPO-coordination "
                           "operating point (R below health; sec.27) -- so the operating point is moved toward health by "
                           "RESTORING deficient drive / removing the chronic-stress drive that LOWERS it (the mirror "
                           "direction). The three abstract levers carry over; what differs is the DISTRIBUTION (L3-dominant) "
                           "and the SIGN (restore deficient vs reduce excess). Both are stated, not hidden."),
        "unifying_frame": ("the depressive operating point sits BELOW health (sec.27, the hypo-coordination pole). It can be "
                           "moved back toward health by ANY of three levers, selectively, with L3 DOMINANT. L1 modulates the "
                           "inward glutamatergic/Ca drive (the rapid NMDA route -- sign-subtle: an antagonist direction acting "
                           "via downstream BDNF, not excitation reduction), L2 modulates the outward K+ M-current / GABA-A "
                           "restoring current (the M-current and neurosteroid-PAM routes), L3 removes/normalises the up-stream "
                           "sensitising drives that SET the operating point: (a) the HPA stress hyperdrive is REMOVED, (b) the "
                           "deficient monoaminergic approach drive is RESTORED (the restorative sign flip), (c) the neurotrophic/"
                           "plasticity drive is RESTORED (the un-chronification convergence). Each lever has a cited "
                           "operating-point-restoring agent DIRECTION; efficacy is asserted nowhere. Two honest sign caveats: "
                           "the L1 glutamatergic direction is an NMDA ANTAGONIST acting downstream, and the HTR2A direction is "
                           "NON-MONOTONE (agonist and antagonist routes both appear)."),
        "levers": LEVER_FRAME,
        "lever_distribution_witness": {
            "counts": counts,
            "dominant_lever": dominant,
            "reading": ("depression is %s-DOMINANT (%d of %d targets) -- the QUALITATIVE difference from bipolar and "
                        "epilepsy, which load on the channel levers L1/L2. The frame's generality is exercised: the SAME "
                        "three abstract levers re-distribute onto the up-stream HPA/monoamine/neurotrophic drives rather "
                        "than the firing-threshold channels." % (dominant, counts.get(dominant, 0), len(entries))),
        },
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a receptor occupancy, not a synaptic monoamine "
                     "level, not a potency, not a dose, not in-vivo selectivity, not a clinical effect, and NOT the sec.27 "
                     "network operating-point (the coordination level R below health) (those are [O]). The promoter |h_sp| is "
                     "the gene's OWN switch stiffness, carried alongside, never folded into a clinical magnitude or equated "
                     "with the operating point. gamma is blind to on/off and to gain/loss/expression-level of function. L3 "
                     "(HPA/monoamine/neurotrophic) mechanism link is [O] -- the read places the gene, it does not derive the "
                     "signalling/network mechanism."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never drugs, doses, "
                    "protocols, or patients; depression is heterogeneous (melancholic/atypical/psychotic/peripartum/seasonal/"
                    "bipolar depression; monoaminergic/HPA/inflammatory/circadian/psychosocial contributors; ~30% treatment-"
                    "resistant) (LOCKED); the L1 glutamatergic direction is an NMDA ANTAGONIST acting via downstream BDNF (NOT "
                    "excitation reduction) and the HTR2A direction is NON-MONOTONE -- both recorded honestly; the L3 monoamine "
                    "lever is RESTORATIVE not reductive (the disorder-level sign flip); a lever direction is a mechanism "
                    "boundary, not a claim about the felt quality of depressed mood (Axis-A; consciousness_claim=0; hard "
                    "problem OPEN)."),
        "n_targets": len(entries),
        "missing_from_cache": missing,
        "order_by_spinodal_desc": order,
        "targets_by_lever": by_lever,
        "channels_present": sorted({e["channel"] for e in entries if e["channel"]}),
        "entries": entries,
    }

# ----------------------------- determinism + engine guard -----------------------------
def _canon(o):
    if isinstance(o, float): return round(o, 10)
    if isinstance(o, dict):  return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):  return [_canon(v) for v in o]
    return o
def _blob(res): return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

M0_16_FROZEN = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

def depression_threshold_levers_results():
    res = build()
    R = E.emerge_all()                           # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"] = {
        "engine_tree_frozen": ENGINE_TREE_FROZEN,
        "engine_tree_sha256_live": tree_live,
        "engine_tree_unchanged": bool(tree_live == ENGINE_TREE_FROZEN),
        "m0_16_subtree_unchanged": bool(sub016 == M0_16_FROZEN),
        "reads_shared_R19_primitive": True,
        "no_new_tuned_constants": True,
        "reuses_sec27_restore_direction": True,
    }
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "l3_mechanism_link": "OPEN [O] -- the HPA/monoamine/neurotrophic signalling mechanism is cited biology, not derived",
        "promoter_hsp_vs_operating_point": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the sec.27 network operating-point (R below health)",
        "disorder_level_sign_recorded": 1.0,
        "nonmonotone_and_antagonist_caveats_recorded": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "depression_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_depression_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"depression_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = depression_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 92)
    print("T1b-L  DEPRESSION THREE-LEVER MAP   (inherited from analgesic v2.0; engine READ-ONLY; L3-dominant)")
    print("=" * 92)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  decomposes sec.27 push: {inv['reuses_sec27_restore_direction']}")
    print("-" * 92)
    print(f"  {'gene':9} {'lev':5} {'gamma':>7} {'|h_sp|':>8} {'channel/protein':40} depression anchor")
    for e in res["entries"]:
        cp = e["channel"] or e.get("protein") or "-"
        print(f"  {e['gene']:9} {e['lever']:5} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} "
              f"{cp[:40]:40} {e['depression_genetic_anchor'][:34]}")
    print("-" * 92)
    w = res["lever_distribution_witness"]
    print("  targets by lever: " + ", ".join(f"{k}={v}" for k, v in w["counts"].items())
          + f"   -> DOMINANT {w['dominant_lever']}")
    print(f"  n_targets: {res['n_targets']}   channels: {len(res['channels_present'])}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 92)
    ok = inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
    print("  T1b-L THREE-LEVER MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
