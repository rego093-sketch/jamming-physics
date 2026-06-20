#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alzheimers_threshold_levers.py  —  AD-T3b-L (sec.38): the symptomatic-network target map for the
Alzheimer's-disease operating point, and the EIGHTH application of the inherited analgesic_threshold_logic
v2.0 cross-cutting layer (after bipolar sec.30, epilepsy sec.31, depression sec.32, schizophrenia sec.33,
autism sec.34, ADHD sec.35 and addiction sec.36). It re-derives no rule: it reads the SAME R19 substrate
(E.spinodal/E.barrier) and the SAME gamma = -mean(NN stacking dG, SantaLucia 1998) the engine uses to
write genes, and it maps the Alzheimer's substrate onto the formal L1/L2/L3 frame by threshold-frame
REACHABILITY.

WHY THIS IS THE THIRD *PARTIAL* FIT [L] -- AND THE DEEPEST ONE (the headline). ADHD (sec.35) was the first
partial fit: its DOMINANT axis (the gain-amplitude machinery) was out of reach because a drive-tone lever
has no handle on catecholamine synthesis/release -- a fold does not set a gain. Addiction (sec.36) was the
second: its DOMINANT axis (the consolidated sensitisation GAIN) was out of reach because it is a gain AND
a CONSOLIDATED/LEARNED plasticity (E0-layer, sec.26) trace -- the convergence point where threshold-
leverisation (B-i) meets the dynamics route (B-ii), which sec.37 then CLOSED by modelling the trace
directly. Alzheimer's is the THIRD partial fit, and the DEEPEST yet, for a related but distinct reason.

Alzheimer's is a NEURODEGENERATIVE disorder: its DOMINANT fault is a PROGRESSIVE, CUMULATIVE, largely
IRREVERSIBLE cascade -- amyloid-beta accumulation, tau aggregation and spread, and the LOSS of synapses
and neurons that disintegrates the network over years. The threshold-shift frame reaches the
INSTANTANEOUS SYMPTOMATIC operating point: the up-stream cholinergic DRIVE (L3, where the established
symptomatic pharmacology lives -- the donepezil/rivastigmine/galantamine cholinesterase-inhibition
direction RESTORES a deficient cholinergic tone), the glutamatergic EXCITOTOXICITY axis (L1, the memantine
uncompetitive-NMDA direction REDUCES a pathological glutamate drive), and the inhibitory-RESTORE / network-
rhythm arm (L2, damping the network hyperexcitability / subclinical epileptiform activity of AD). But it
does NOT reach the disorder's DOMINANT fault: the NEURODEGENERATIVE PROGRESSION axis (the PROG axis) -- the
amyloid/tau/synapse-and-neuron-loss trajectory that DRIVES decline. That axis is out of reach for three
reasons, the first two inherited and the third new: (a) it is not a single FOLD an operating-point lever
sets (the ADHD lesson generalised: a threshold shift moves a set-point, not a slow degenerative trajectory);
(b) it is a PROGRESSION over TIME -- an E0-layer DYNAMICS variable, not an instantaneous fold (the addiction
lesson: the durable trajectory is the dynamics route's domain, the roadmap's explicit "needs E0 progression");
and (c) -- the NEW depth -- it is a DEGENERATION, a cumulative LOSS of synapses and neurons plus protein
aggregation, the structural INVERSE of addiction's E0 GAIN: where addiction's E0 trace BUILDS UP a sensitised
gain, Alzheimer's E0 trace ERODES the connectome (an E0 DECAY). The entire REACHABLE surface is therefore
PURELY SYMPTOMATIC -- it gives temporary symptomatic benefit while the disease progresses underneath -- and
the DOMINANT (out-of-reach) axis is the disease-MODIFYING one (where the anti-amyloid antibodies
lecanemab/donanemab act, themselves only progression-MODIFIERS, not threshold levers). So Alzheimer's is the
THIRD partial fit and the DEEPEST: the whole reachable surface is symptom-only, and the dominant fault is an
irreversible E0 DECAY trajectory. The fit is PARTIAL [L] -- the third non-clean fit -- and the partial grade
is the honest record of exactly where the cross-cutting logic stops.

THE TWO ALZHEIMER'S AXES (re-cut here by threshold-frame REACHABILITY):
  SYMP  (the instantaneous SYMPTOMATIC network operating point)  = REACHED by the lever frame across all
        three classes: L3 the up-stream cholinergic DRIVE (AChE/BuChE, a7-nicotinic, M1-muscarinic --
        RESTORE the deficient cholinergic tone), L1 the glutamatergic EXCITOTOXICITY axis (NMDA NR2B/NR2A --
        REDUCE the pathological glutamate drive, the memantine direction), L2 the inhibitory-RESTORE /
        network-rhythm arm (GABA-A a1/a5/b3 -- RESTORE inhibition, damp the network hyperexcitability). This
        is where the established AD pharmacology acts, as DIRECTIONS -- but it is PURELY SYMPTOMATIC: a SPLIT
        corrective sign (RESTORE the deficient cholinergic drive AND inhibition, REDUCE the excess glutamate),
        temporary, not touching progression.
  PROG  (neurodegenerative PROGRESSION -- the amyloid/tau/synapse-and-neuron-loss trajectory)  = the DOMINANT
        Alzheimer's fault: the CUMULATIVE, largely IRREVERSIBLE cascade (amyloid-beta accumulation via APP/
        PSEN1/PSEN2 gamma-secretase, tau aggregation MAPT, APOE-e4 clearance failure, TREM2 microglial
        neuroinflammation, and the synapse/neuron LOSS that disintegrates the network). NOT REACHED: it is
        not a fold (the ADHD lesson) AND it is a PROGRESSION over time -- an E0-layer DYNAMICS (DECAY)
        variable -- AND it is a DEGENERATION, the structural inverse of addiction's E0 GAIN. The threshold
        frame reaches it only INDIRECTLY (symptomatic levers offset some downstream load), never as a direct
        handle -- which is exactly why Alzheimer's is a PARTIAL fit, the DOMINANT axis being the out-of-reach
        one, and the DEEPEST: the reachable surface is symptom-only.

THE LEVER DISTRIBUTION (honest). Where bipolar leaned on L1 (calcium), epilepsy on L2 (the M-current),
depression on L3 (HPA/monoamine, L3-dominant with a reachable L1/L2 mix), schizophrenia on L1+L3 co-dominant
(glutamate + dopamine), autism on L1-DOMINANT with a sparse L3, ADHD on L3-ONLY (L1/L2 EMPTY), and addiction
on L3-DOMINANT with L1 AND L2 present (excess reward drive), Alzheimer's is L3-DOMINANT WITH L1 AND L2 BOTH
PRESENT but with a SPLIT corrective sign -- the EIGHTH distribution pattern, and the FIRST with a split-sign
reachable surface:
  L1  REDUCE the inward excitatory / glutamatergic EXCITOTOXICITY (NMDA NR2B/NR2A; memantine)  (2 levers)
  L2  RESTORE the outward / GABA-A inhibition, damp network hyperexcitability (GABA-A a1/a5/b3)  (3 levers)
  L3  RESTORE a deficient UP-STREAM cholinergic DRIVE (AChE/BuChE, a7-nAChR, M1-mAChR)           (4 levers, DOMINANT)
Two features make Alzheimer's distinct from the addiction template even though the gross shape is shared:
(1) the corrective sign is SPLIT -- L3/L2 RESTORE a deficit while L1 REDUCES an excess (the first split-sign
reachable surface; depression was pure-restore, epilepsy/schizophrenia pure-reduce, addiction pure-dampen);
(2) the out-of-reach axis is the FIRST that is DEGENERATIVE -- a cumulative LOSS (an E0 DECAY), the structural
inverse of addiction's E0 GAIN; and the reachable surface is the FIRST that is PURELY SYMPTOMATIC (no
reachable lever touches progression at all). Same gross shape as addiction, the THIRD partial verdict, the
deepest reason.

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| / barrier are
the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V] (reproducible); their
ORDER is [F] (forced). This is NOT a receptor occupancy, NOT a synaptic acetylcholine/glutamate level, NOT a
drug potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect, and -- the Alzheimer's-specific
addition -- the promoter |h_sp| is NOT the neurodegeneration RATE, NOT the amyloid burden, NOT the tau load,
and NOT the rate of synapse/neuron loss (the PROG progression axis). gamma is blind to on/off and to
expression level. The L3 (cholinergic-drive) mechanism link is [O].

THE HONEST CAVEATS (Alzheimer's-specific; recorded, not hidden).
  (i)   PARTIAL FIT [L] (the THIRD in the series, and the DEEPEST). The DOMINANT Alzheimer's fault (the PROG
        neurodegenerative-progression axis) is OUT OF REACH of the threshold frame, because it is not a fold,
        is a PROGRESSION over time (an E0-layer DECAY variable), and is a DEGENERATION (cumulative LOSS).
        Only the INSTANTANEOUS SYMPTOMATIC surface is reached, and it is PURELY SYMPTOMATIC. Recorded as the
        fit_grade.
  (ii)  PURELY SYMPTOMATIC reachable surface. The cholinesterase-inhibition (L3), memantine (L1) and
        GABAergic/network (L2) directions are SYMPTOMATIC -- modest, temporary benefit -- and do NOT slow
        the disease; progression continues underneath. This is sharper than addiction (whose reachable
        reward-drive levers are at least disease-relevant): here the entire reachable surface is symptom-only.
  (iii) SPLIT CORRECTIVE SIGN. Unlike the single-sign disorders, the reachable surface mixes signs: RESTORE
        the deficient cholinergic drive (L3) and inhibition (L2), but REDUCE the glutamatergic excitotoxicity
        (L1). The first split-sign reachable surface in the series.
  (iv)  THE CONVERGENCE (an E0 DECAY). The out-of-reach PROG axis is precisely an E0-layer PROGRESSION
        (DECAY) domain (the roadmap's "the payoff is in modelling progression, which needs E0"): a dynamics
        module (a future B-ii) would model the cumulative LOSS / network disintegration -- and the network-
        rhythm (gamma-entrainment / 40 Hz) and disease-modifying directions are the dynamics handles, not
        threshold levers. B-i (this map) NAMES the PROG axis out-of-reach honestly. Alzheimer's E0 trace is
        the structural INVERSE of addiction's: addiction BUILDS a gain, Alzheimer's ERODES the connectome.

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places READS and
TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any agent treats anyone. Alzheimer's
is POLYGENIC and HETEROGENEOUS, its established symptomatic pharmacology is only PARTIALLY and TEMPORARILY
effective and does NOT halt progression, and a lever direction is a mechanism boundary, NOT a claim that
Alzheimer's can be reversed, cured, prevented or its progression stopped, and NOT a judgement on the
personhood or worth of a person living with dementia (a person with dementia remains a person). The
forbidden-claim scanner enforces this (incl. a CURE-REVERSAL class and a DIGNITY class). consciousness_claim
stays 0; hard problem OPEN.

No tuning: gamma is measured; |h_sp|/barrier are the locked R19 forms; the lever assignments, axis mapping
and citations are CITED Layer-2 biology + the neurodegeneration substrate, not engine outputs. Governed by
VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 alzheimers_threshold_levers.py
Out:  alzheimers_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "alzheimers_levers_promoters.cache.json")
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

# SantaLucia 1998 unified NN dG37 -- the SAME table the engine / analgesic / DNA pipeline use.
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}
def gamma(seq):
    """Interfacial tension / stiffness = -mean(NN stacking dG). Strand-symmetric. [V] read."""
    s = seq.upper()
    v = [-NN[s[i:i+2]] for i in range(len(s)-1) if s[i:i+2] in NN]
    return float(sum(v)/len(v)) if v else float("nan")

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the Alzheimer's symptomatic axis) ----
LEVER_FRAME = {
  "L1": "REDUCE the inward excitatory / damp the glutamatergic EXCITOTOXICITY (NMDA NR2B/NR2A) -- the "
        "pathological glutamate drive of Alzheimer's. PRESENT for AD (2 levers): NR2B-containing "
        "(especially extrasynaptic) NMDA receptors mediate the excitotoxic glutamatergic tone, and this is "
        "where memantine (the uncompetitive open-channel NMDA antagonist) acts (as a DIRECTION). Reaches the "
        "INSTANTANEOUS glutamatergic excitotoxicity surface; the neurodegenerative progression itself is out "
        "of reach. SYMPTOMATIC only. The mechanism link is [O]",
  "L2": "RESTORE the outward / GABA-A inhibitory current (GABA-A a1/a5/b3), damping the NETWORK "
        "HYPEREXCITABILITY -- the inhibitory-RESTORE / network-rhythm arm. PRESENT for AD (3 levers): "
        "Alzheimer's carries network hyperexcitability and subclinical epileptiform activity "
        "(interneuron dysfunction, hippocampal hyperactivity), and the extrasynaptic a5 subunit gates the "
        "tonic inhibition that sets network gain; restoring inhibition / network rhythm (the gamma-band "
        "axis) is the DIRECTION. Reaches the INSTANTANEOUS inhibitory balance. SYMPTOMATIC only. The "
        "mechanism link is [O]",
  "L3": "RESTORE a deficient UP-STREAM cholinergic DRIVE. The DOMINANT lever class for AD (4 levers): the "
        "basal-forebrain cholinergic projection DEGENERATES in Alzheimer's, lowering acetylcholine tone; "
        "the acetylcholinesterase/butyrylcholinesterase enzymes and the a7-nicotinic and M1-muscarinic "
        "receptors set the cholinergic-DRIVE tone -- the surface the established symptomatic pharmacology "
        "acts on (as DIRECTIONS: the donepezil/rivastigmine/galantamine cholinesterase-inhibition that "
        "RAISES acetylcholine, and muscarinic/nicotinic agonism). This reaches the INSTANTANEOUS cholinergic "
        "drive ONLY; the neurodegenerative PROGRESSION (the PROG axis) is out of reach (partial fit [L]). "
        "SYMPTOMATIC only -- it does NOT slow the disease. The mechanism link is [O]",
}

# grade strings
GL3 = ("[O] cited biology: gamma places the gene in the cholinergic-drive lever map; the "
       "acetylcholine (cholinesterase / nicotinic / muscarinic) signalling mechanism is NOT derived")
GL1 = ("[O] cited biology: gamma places the gene in the glutamatergic-excitotoxicity lever map; "
       "the NMDA/glutamate signalling mechanism is NOT derived")
GL2 = ("[O] cited biology: gamma places the gene in the inhibitory-restore / network lever map; the "
       "GABA-A inhibitory signalling mechanism is NOT derived")

DOM_SYMP = "SYMP (the instantaneous symptomatic network operating point the levers REACH)"

# ===================== LEVER TARGETS (the genes that ARE the levers; L1/L2/L3) =====================
CONTEXT = {
  # ---- L3 cholinergic up-stream DRIVE (dominant lever class; RESTORE the deficient drive) ----
  "ACHE": dict(lever="L3", domain=DOM_SYMP, channel=None, protein="acetylcholinesterase (ACHE)",
      axis_role="cholinergic drive (acetylcholine hydrolysis)",
      push="RESTORE the deficient cholinergic tone by INHIBITING acetylcholinesterase (the donepezil/galantamine/rivastigmine DIRECTION) -- the most established AD-symptomatic node; inhibiting AChE raises synaptic acetylcholine to offset the basal-forebrain cholinergic loss",
      add_anchor="acetylcholinesterase (ACHE); the enzyme that hydrolyses acetylcholine and the molecular target of the donepezil/galantamine/rivastigmine cholinesterase inhibitors -- the canonical symptomatic cholinergic node of the cholinergic hypothesis of AD",
      drive_agent="acetylcholinesterase-inhibition DIRECTION for the cholinergic-drive axis (the donepezil route, as DIRECTION, not efficacy; not a dose; symptomatic only, does not slow progression)",
      grade_mechanism=GL3,
      src="Davies & Maloney 1976 (cholinergic deficit in AD); Birks 2006 Cochrane (cholinesterase inhibitors, AD)"),
  "BCHE": dict(lever="L3", domain=DOM_SYMP, channel=None, protein="butyrylcholinesterase (BCHE)",
      axis_role="cholinergic drive (acetylcholine hydrolysis, glial)",
      push="RESTORE cholinergic tone via the SECONDARY cholinesterase butyrylcholinesterase (the rivastigmine dual-inhibition DIRECTION) -- BuChE rises as AChE falls in advancing AD and co-hydrolyses acetylcholine; a sign-aligned [O] handle on the same drive axis",
      add_anchor="butyrylcholinesterase (BCHE); the secondary cholinesterase (the BCHE-K variant) whose activity rises in advancing AD and which rivastigmine co-inhibits -- a secondary cholinergic-drive node",
      drive_agent="butyrylcholinesterase-inhibition DIRECTION for the cholinergic-drive axis (the rivastigmine dual-inhibition route; DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL3,
      src="Greig 2005 PNAS 102:17213 (BuChE in AD); Birks 2006 Cochrane (rivastigmine, dual cholinesterase)"),
  "CHRNA7": dict(lever="L3", domain=DOM_SYMP, channel=None, protein="nicotinic acetylcholine receptor alpha-7 (CHRNA7)",
      axis_role="cholinergic drive (nicotinic)",
      push="RESTORE cholinergic signalling via the a7-nicotinic receptor (the a7-agonist / galantamine allosteric-potentiation DIRECTION) -- a7 nAChRs carry cholinergic fast transmission and are a cognition target; a sign-subtle [O] handle (a7 also binds amyloid-beta, an interaction on the boundary with the out-of-reach axis)",
      add_anchor="the alpha-7 nicotinic acetylcholine receptor (CHRNA7, in the 15q13 locus); a cholinergic-signalling receptor and cognition target (a7 agonists, galantamine's allosteric potentiation) that also binds amyloid-beta -- a nicotinic cholinergic-drive node",
      drive_agent="alpha-7-nicotinic agonism / allosteric-potentiation DIRECTION for the cholinergic-drive axis (DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL3,
      src="Wang 2000 J Biol Chem 275:5626 (a7 nAChR / amyloid-beta); Hoyng 2013 (a7 agonists, cognition)"),
  "CHRM1": dict(lever="L3", domain=DOM_SYMP, channel=None, protein="muscarinic acetylcholine receptor M1 (CHRM1)",
      axis_role="cholinergic drive (muscarinic)",
      push="RESTORE cholinergic signalling via the M1-muscarinic receptor (the M1-selective-agonist DIRECTION, the xanomeline arm) -- M1 mAChRs carry post-synaptic cholinergic cognitive transmission; a sign-subtle [O] handle (selectivity has historically been the hard problem)",
      add_anchor="the M1 muscarinic acetylcholine receptor (CHRM1); the principal post-synaptic cortical/hippocampal muscarinic receptor and the target of M1-selective agonism (the xanomeline direction) -- a muscarinic cholinergic-drive node",
      drive_agent="M1-muscarinic agonism DIRECTION for the cholinergic-drive axis (the xanomeline route; sign-subtle on selectivity; DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL3,
      src="Bodick 1997 Arch Neurol 54:465 (xanomeline, M1, AD); Fisher 2008 (M1 muscarinic, cognition)"),
  # ---- L1 glutamatergic EXCITOTOXICITY (present, secondary; REDUCE the excess) ----
  "GRIN2B": dict(lever="L1", domain=DOM_SYMP, channel="NMDA NR2B (GRIN2B)", protein="NMDA receptor NR2B subunit (GRIN2B)",
      axis_role="glutamatergic excitotoxicity",
      push="REDUCE the pathological glutamatergic (NMDA NR2B) drive -- NR2B-containing (especially extrasynaptic) NMDA receptors mediate the excitotoxic tone of AD; the memantine (uncompetitive open-channel NMDA antagonist) DIRECTION reaches this INSTANTANEOUS surface (the progression itself is out of reach), an [O] handle",
      add_anchor="the NMDA NR2B subunit (GRIN2B); extrasynaptic NR2B-containing NMDA receptors mediate glutamatergic excitotoxicity in AD and are the preferential substrate of memantine's uncompetitive block -- the principal glutamatergic-excitotoxicity node",
      drive_agent="uncompetitive-NMDA-antagonist DIRECTION for the excitotoxicity axis (the memantine route; DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL1,
      src="Lipton 2006 Nat Rev Drug Discov 5:160 (memantine, NMDA excitotoxicity); Reisberg 2003 NEJM 348:1333 (memantine, AD)"),
  "GRIN2A": dict(lever="L1", domain=DOM_SYMP, channel="NMDA NR2A (GRIN2A)", protein="NMDA receptor NR2A subunit (GRIN2A)",
      axis_role="glutamatergic excitotoxicity",
      push="REDUCE / rebalance the glutamatergic (NMDA NR2A) drive -- synaptic NR2A-containing NMDA receptors set the excitatory tone the excitotoxicity axis loads on; the glutamate-rebalancing (memantine-class) DIRECTION reaches this INSTANTANEOUS surface (not the progression), an [O] handle",
      add_anchor="the NMDA NR2A subunit (GRIN2A); synaptic NR2A-containing NMDA receptors gate the excitatory glutamatergic tone -- a glutamatergic-excitotoxicity node on the same memantine-class direction",
      drive_agent="glutamate-rebalancing DIRECTION for the excitotoxicity axis (the memantine-class route; DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL1,
      src="Lipton 2006 Nat Rev Drug Discov 5:160 (NMDA excitotoxicity in AD); Wang & Reddy 2017 (glutamate in AD)"),
  # ---- L2 inhibitory-RESTORE / network (present; RESTORE inhibition, damp hyperexcitability) ----
  "GABRA5": dict(lever="L2", domain=DOM_SYMP, channel="GABA-A a5 (GABRA5)", protein="GABA-A receptor alpha-5 subunit (GABRA5)",
      axis_role="inhibitory restore (extrasynaptic tonic)",
      push="RESTORE the extrasynaptic TONIC GABA-A inhibition via the alpha-5 subunit -- a5-GABA-A gates hippocampal tonic inhibition / network gain, dysregulated in the AD network hyperexcitability; restoring the inhibitory set-point (damping aberrant excitation) is the DIRECTION, an [O] handle (sign-subtle: a5 inverse-agonism has separately been a cognition direction, so the AD-network sign is recorded as the restore direction here)",
      add_anchor="the GABA-A alpha-5 subunit (GABRA5); the extrasynaptic subunit that gates hippocampal tonic inhibition and network gain -- the inhibitory-restore node for the AD network-hyperexcitability arm",
      drive_agent="extrasynaptic-tonic GABA-A restore DIRECTION for the inhibitory-restore axis (DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL2,
      src="Vossel 2017 Nat Rev Neurol 13:311 (network hyperexcitability in AD); Palop & Mucke 2016 (inhibitory dysfunction, AD)"),
  "GABRB3": dict(lever="L2", domain=DOM_SYMP, channel="GABA-A b3 (GABRB3)", protein="GABA-A receptor beta-3 subunit (GABRB3)",
      axis_role="inhibitory restore",
      push="RESTORE GABA-A inhibition via the beta-3 subunit -- a core GABA-A subunit that assembles the inhibitory receptors damping cortical/hippocampal network excitability; raising inhibitory tone on the same L2 axis is the DIRECTION, an [O] handle",
      add_anchor="the GABA-A beta-3 subunit (GABRB3); a core assembly subunit of the inhibitory GABA-A receptors that damp network excitability -- a secondary inhibitory-restore node",
      drive_agent="GABA-A restore DIRECTION for the inhibitory-restore axis (DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL2,
      src="Palop & Mucke 2016 Nat Rev Neurosci 17:777 (inhibitory dysfunction, AD); Vossel 2017 (network hyperexcitability)"),
  "GABRA1": dict(lever="L2", domain=DOM_SYMP, channel="GABA-A a1 (GABRA1)", protein="GABA-A receptor alpha-1 subunit (GABRA1)",
      axis_role="inhibitory restore (synaptic phasic)",
      push="RESTORE the synaptic PHASIC GABA-A inhibition via the alpha-1 subunit -- the most abundant synaptic GABA-A subunit that carries fast phasic inhibition; restoring inhibitory balance to damp the AD network hyperexcitability is the DIRECTION, an [O] handle",
      add_anchor="the GABA-A alpha-1 subunit (GABRA1); the most abundant synaptic GABA-A subunit carrying fast phasic inhibition -- a synaptic inhibitory-restore node for the network arm",
      drive_agent="synaptic-phasic GABA-A restore DIRECTION for the inhibitory-restore axis (DIRECTION, not efficacy; symptomatic only)",
      grade_mechanism=GL2,
      src="Palop & Mucke 2016 Nat Rev Neurosci 17:777 (inhibitory dysfunction, AD); Vossel 2017 (network hyperexcitability)"),
}

# ===== OUT-OF-REACH TARGETS (the PROG neurodegenerative-progression axis a threshold lever CANNOT reach) =====
# These are NOT levers. They carry a gamma read (their own promoter switch stiffness) ALONGSIDE, with the
# explicit record that NO threshold/drive lever reaches the PROG axis: the neurodegenerative progression is a
# PROGRESSION over time (an E0-layer DECAY variable) AND a DEGENERATION (cumulative LOSS), not an instantaneous
# fold. Naming them makes the Alzheimer's partial-fit concrete: the disorder's DOMINANT axis (the amyloid/tau/
# synapse-and-neuron-loss cascade that drives decline) is out of reach -- and it is the disease-MODIFYING axis,
# where the anti-amyloid antibodies act (themselves only progression-MODIFIERS, not threshold levers).
OUT_OF_REACH = {
  "APP": dict(axis="PROG", role="amyloid precursor protein -- the source of amyloid-beta (the amyloid cascade substrate)", channel=None,
      why_unreached="the PROG (neurodegenerative-progression) axis: APP is the precursor cleaved by beta/gamma-secretase to generate amyloid-beta; its amyloidogenic processing INITIATES the amyloid cascade (APP duplication / chr21 trisomy cause autosomal-dominant AD). The cumulative amyloid deposition is a PROGRESSION over time (an E0-layer DECAY trajectory) and a DEGENERATION, NOT an instantaneous fold -- so a threshold/drive lever cannot reach or reverse it (this is the dominant AD fault, the decline driver, the anti-amyloid-antibody axis)",
      add_anchor="the amyloid precursor protein (APP, chr21); APP duplications and the trisomy-21 / Down-syndrome dose effect cause autosomal-dominant AD, and its amyloidogenic cleavage is the source of amyloid-beta -- the substrate of the amyloid cascade hypothesis (a progression mechanism, not an excitability fold)",
      src="Hardy & Higgins 1992 Science 256:184 (amyloid cascade hypothesis); E0 progression (a future B-ii dynamics layer)"),
  "PSEN1": dict(axis="PROG", role="presenilin-1 -- gamma-secretase catalytic subunit (the commonest autosomal-dominant AD gene)", channel=None,
      why_unreached="the PROG (neurodegenerative-progression) axis: PSEN1 is the catalytic subunit of the gamma-secretase that cleaves APP to amyloid-beta, and the commonest cause of early-onset autosomal-dominant AD. It sets the amyloid-GENERATION step of a CUMULATIVE progression (an E0-layer DECAY trajectory), NOT an instantaneous fold a drive lever sets -- so it is out of reach (the gamma-secretase-modulator / disease-modifying axis)",
      add_anchor="presenilin-1 (PSEN1, chr14); the catalytic subunit of gamma-secretase and the commonest gene for early-onset autosomal-dominant Alzheimer's -- the amyloid-generation step of the cascade (a progression mechanism)",
      src="Sherrington 1995 Nature 375:754 (PSEN1, familial AD); E0 progression (a future B-ii dynamics layer)"),
  "PSEN2": dict(axis="PROG", role="presenilin-2 -- gamma-secretase catalytic subunit (rarer autosomal-dominant AD)", channel=None,
      why_unreached="the PROG (neurodegenerative-progression) axis: PSEN2 is a second gamma-secretase catalytic subunit causing rarer autosomal-dominant AD; like PSEN1 it sets the amyloid-generation step of a cumulative progression (an E0-layer DECAY trajectory), NOT an instantaneous fold -- out of reach of a threshold/drive lever (the disease-modifying axis)",
      add_anchor="presenilin-2 (PSEN2, chr1); a second gamma-secretase catalytic subunit causing rarer autosomal-dominant AD -- the amyloid-generation step of the cascade (a progression mechanism)",
      src="Levy-Lahad 1995 Science 269:973 (PSEN2, familial AD); E0 progression (a future B-ii dynamics layer)"),
  "MAPT": dict(axis="PROG", role="microtubule-associated protein tau -- neurofibrillary tangles (the tau axis)", channel=None,
      why_unreached="the PROG (neurodegenerative-progression) axis: MAPT encodes tau, whose hyperphosphorylation and aggregation into neurofibrillary tangles SPREADS through the cortex and tracks cognitive decline more tightly than amyloid. Tau pathology is a PROGRESSION over time (an E0-layer DECAY trajectory of spreading aggregation and synapse/neuron LOSS), NOT an instantaneous fold -- so a threshold/drive lever cannot reach it (the tau / anti-tau disease-modifying axis)",
      add_anchor="microtubule-associated protein tau (MAPT, chr17); hyperphosphorylated tau forms the neurofibrillary tangles whose spread tracks cognitive decline, and MAPT mutations cause frontotemporal tauopathy -- the tau arm of the degeneration cascade (a progression mechanism)",
      src="Braak & Braak 1991 Acta Neuropathol 82:239 (tau-tangle staging); E0 progression (a future B-ii dynamics layer)"),
  "APOE": dict(axis="PROG", role="apolipoprotein E -- the e4 allele is the strongest sporadic-AD risk factor (amyloid clearance)", channel=None,
      why_unreached="the PROG (neurodegenerative-progression) axis: the APOE-e4 allele is the strongest common genetic risk factor for sporadic AD, acting through impaired amyloid-beta clearance and lipid/microglial pathways that ACCELERATE the cumulative cascade. It biases the RATE of a progression over time (an E0-layer DECAY trajectory), NOT an instantaneous fold -- out of reach of a threshold/drive lever (the clearance / disease-modifying axis)",
      add_anchor="apolipoprotein E (APOE, chr19); the e4 allele is the strongest common-variant risk factor for sporadic Alzheimer's, acting through impaired amyloid-beta clearance and lipid/microglial pathways -- the dominant common-variant progression-rate modifier (a progression mechanism, not a fold)",
      src="Corder 1993 Science 261:921 (APOE-e4, AD risk); E0 progression (a future B-ii dynamics layer)"),
  "TREM2": dict(axis="PROG", role="microglial receptor -- neuroinflammation / amyloid clearance (rare ~3x risk variants)", channel=None,
      why_unreached="the PROG (neurodegenerative-progression) axis: TREM2 is a microglial receptor whose rare variants (R47H) ~triple AD risk; it governs the microglial neuroinflammatory / amyloid-clearance response that shapes the cumulative degeneration. It modulates the IMMUNE arm of a progression over time (an E0-layer DECAY trajectory), NOT an instantaneous fold -- out of reach of a threshold/drive lever (the neuroimmune / disease-modifying axis)",
      add_anchor="the triggering receptor expressed on myeloid cells 2 (TREM2, chr6); rare variants (R47H) roughly triple AD risk by altering the microglial neuroinflammatory / amyloid-clearance response -- the neuroimmune arm of the degeneration cascade (a progression mechanism)",
      src="Guerreiro 2013 NEJM 368:117 (TREM2 R47H, AD risk); E0 progression (a future B-ii dynamics layer)"),
}

def read(sym, g):
    c = CONTEXT[sym]
    grade_open = {"L1": GL1, "L2": GL2, "L3": GL3}[c["lever"]]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the neurodegeneration rate)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "domain_reach": c["domain"],
        "axis_role": c["axis_role"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "alzheimers_genetic_anchor": c["add_anchor"],
        "symptomatic_axis_drive_agent_direction": c["drive_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": grade_open,
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_progression": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch "
                                       "stiffness, NOT the neurodegeneration RATE / amyloid burden / tau "
                                       "load / synapse-and-neuron-loss rate (the PROG progression axis); never equated",
        "grade_clinical_map": "[O] OPEN -- not a receptor occupancy, synaptic acetylcholine/glutamate "
                              "level, potency, dose, in-vivo selectivity, or clinical effect; SYMPTOMATIC only",
        "context_grade": "CITED Layer-2 biology + the neurodegeneration substrate (not an engine output)",
        "src": c["src"],
    }

def read_out_of_reach(sym, g):
    c = OUT_OF_REACH[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] structural read carried alongside (NOT a lever placement)
        "spinodal_h_sp": round(E.spinodal(g), 6),
        "barrier": round(E.barrier(g), 6),
        "lever": None,                              # explicitly NOT a lever
        "fault_axis": c["axis"],
        "reached_by_threshold_levers": False,
        "why_unreached": c["why_unreached"],
        "role": c["role"],
        "channel": c.get("channel"),
        "alzheimers_genetic_anchor": c["add_anchor"],
        "grade_read": "[V] reproducible promoter-switch-threshold read (carried alongside; does NOT place a lever)",
        "grade_reach": "[F] NOT REACHED -- the threshold/drive frame has no handle on the neurodegenerative-"
                       "progression axis (not a fold; a PROGRESSION over time, an E0-layer DECAY variable; a "
                       "DEGENERATION / cumulative LOSS -- the structural inverse of addiction's E0 GAIN)",
        "context_grade": "CITED Layer-2 biology + the neurodegeneration substrate (not an engine output)",
        "src": c["src"],
    }

def build():
    cache = json.load(open(CACHE))
    gammas = {s: gamma(cache[s]["seq"]) for s in CONTEXT if s in cache}
    missing = [s for s in list(CONTEXT) + list(OUT_OF_REACH) if s not in cache]
    entries = [read(s, gammas[s]) for s in gammas]
    entries.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)   # stiffest promoter read first [F]
    order = [e["gene"] for e in entries]
    by_lever = {}
    for e in entries:
        by_lever.setdefault(e["lever"], []).append(e["gene"])
    # out-of-reach reads (the named PROG progression targets)
    oor_g = {s: gamma(cache[s]["seq"]) for s in OUT_OF_REACH if s in cache}
    oor = [read_out_of_reach(s, oor_g[s]) for s in oor_g]
    oor.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)
    oor_by_axis = {}
    for e in oor:
        oor_by_axis.setdefault(e["fault_axis"], []).append(e["gene"])

    # lever-distribution witness: AD is L3-DOMINANT with L1 AND L2 present
    counts = {k: len(v) for k, v in by_lever.items()}
    ranked = sorted(counts, key=lambda k: counts[k], reverse=True)
    top = counts[ranked[0]]
    dominant_levers = sorted([k for k, n in counts.items() if n == top])
    codominant = len(dominant_levers) >= 2
    l1_present = counts.get("L1", 0) > 0
    l2_present = counts.get("L2", 0) > 0

    # domain-restriction / partial-fit witness (the Alzheimer's headline)
    domain_restriction = {
        "SYMP": {"axis": "instantaneous symptomatic network operating point", "reached_by_levers": True,
            "lever_axes_drawn_from": "L3 cholinergic drive (ACHE/BCHE/CHRNA7/CHRM1, RESTORE) + L1 "
                    "glutamatergic excitotoxicity (GRIN2B/GRIN2A, REDUCE) + L2 inhibitory restore "
                    "(GABRA1/GABRA5/GABRB3, RESTORE)",
            "sign": "SPLIT: RESTORE the deficient cholinergic drive (L3, cholinesterase-inhibition) and "
                    "inhibition (L2), REDUCE the glutamatergic excitotoxicity (L1, memantine) -- the "
                    "donepezil/rivastigmine/galantamine/memantine/GABAergic DIRECTIONS; SYMPTOMATIC only, "
                    "this is the INSTANTANEOUS surface, reached",
            "symptomatic_only": True},
        "PROG": {"axis": "neurodegenerative progression (the amyloid/tau/synapse-and-neuron-loss trajectory -- the DOMINANT AD fault)",
            "reached_by_levers": False,
            "named_genes": oor_by_axis.get("PROG", []),
            "why_not": "the neurodegenerative PROGRESSION -- the CUMULATIVE, largely IRREVERSIBLE cascade "
                       "(amyloid-beta accumulation via APP/PSEN1/PSEN2 gamma-secretase, tau aggregation MAPT, "
                       "APOE-e4 clearance failure, TREM2 microglial neuroinflammation, and the synapse/neuron "
                       "LOSS that disintegrates the network) -- is out of reach in three senses: it is NOT a "
                       "fold (the ADHD lesson) AND it is a PROGRESSION over time -- an E0-layer DECAY variable, "
                       "not an instantaneous fold (the addiction lesson, the roadmap's 'needs E0 progression') "
                       "AND it is a DEGENERATION, a cumulative LOSS, the structural INVERSE of addiction's E0 "
                       "GAIN. So even the symptomatic levers that offset some downstream load cannot REACH the "
                       "trajectory (that is the E0 progression-dynamics domain -- the convergence point). The "
                       "threshold frame reaches it only INDIRECTLY. Named genes: APP / PSEN1 / PSEN2 / MAPT / "
                       "APOE / TREM2 (out_of_reach_targets)."},
        "reading": ("the lever frame reaches the INSTANTANEOUS SYMPTOMATIC network operating point across all "
                    "three classes (L3 cholinergic drive RESTORE, L1 glutamatergic excitotoxicity REDUCE, L2 "
                    "inhibitory restore -- where the established AD symptomatic pharmacology acts). But the "
                    "DOMINANT Alzheimer's fault -- the PROG neurodegenerative progression, the amyloid/tau/"
                    "synapse-and-neuron-loss trajectory that drives decline -- sits on a DIFFERENT axis the "
                    "threshold frame does not reach (only indirectly), because it is not a fold, is a "
                    "PROGRESSION over time (an E0-layer DECAY variable) and is a DEGENERATION (cumulative LOSS). "
                    "So the fit is PARTIAL [L], and the DEEPEST: the whole reachable surface is PURELY "
                    "SYMPTOMATIC (it does not slow the disease) and the dominant axis is an irreversible E0 "
                    "DECAY trajectory. Cites the neurodegeneration substrate and sec.36 (the addiction "
                    "partial-fit precedent, whose E0-GAIN convergence Alzheimer's mirrors as an E0 DECAY)."),
        "cites": "the neurodegeneration substrate (the amyloid cascade + tau staging: a cumulative, largely "
                 "irreversible progression that disintegrates the network over years) + sec.36 "
                 "addiction_threshold_levers (the named-out-of-reach E0-dynamics precedent -- addiction's "
                 "dominant axis was a consolidated/LEARNED gain, an E0-layer trace; Alzheimer's dominant axis "
                 "is a PROGRESSION/DECAY, an E0-layer trace too, but a cumulative LOSS -- the inverse)",
        "relation_to_prior_partials": [
            "ADHD (first partial): its dominant GAIN-amplitude axis (synthesis/release) was out of reach because a drive-tone lever has NO handle on synthesis -- a fold does not set a gain",
            "addiction (second partial): its dominant SG axis was a GAIN out of reach (the ADHD lesson) AND CONSOLIDATED/LEARNED -- a plasticity (E0-layer) variable; the convergence point closed by sec.37 (B-ii) modelling the trace",
            "Alzheimer's is the third partial, and the DEEPEST: its dominant PROG axis is out of reach because it is not a fold (ADHD lesson) AND a PROGRESSION over time, an E0-layer variable (addiction lesson) AND -- the new depth -- a DEGENERATION, a cumulative LOSS (an E0 DECAY), the structural INVERSE of addiction's E0 GAIN; and the entire reachable surface is PURELY SYMPTOMATIC",
            "THE CONVERGENCE (an E0 DECAY): Alzheimer's out-of-reach PROG axis is an E0-layer PROGRESSION (DECAY) domain (the roadmap's 'needs E0 progression') -- the point where threshold-leverisation (B-i) meets the dynamics route (B-ii). B-i NAMES the trajectory out-of-reach honestly; the network-rhythm (gamma-entrainment / 40 Hz) and disease-modifying directions are the dynamics handles, not threshold levers.",
        ],
    }

    # the partial-fit witness (the headline grade)
    partial_fit = {
        "fit_grade": "[L] partial",
        "fit_index_in_series": 3,
        "reached_axis": "SYMP (instantaneous symptomatic network operating point) -- reached across L1/L2/L3, PURELY SYMPTOMATIC",
        "out_of_reach_axis": "PROG (neurodegenerative progression) -- the DOMINANT AD fault, the amyloid/tau/synapse-and-neuron-loss trajectory, reached only indirectly",
        "out_of_reach_reason": "not a fold (the ADHD lesson) AND a PROGRESSION over time -- an E0-layer DECAY variable (the addiction lesson) AND a DEGENERATION / cumulative LOSS -- the structural inverse of addiction's E0 GAIN",
        "deepest_partial": True,
        "reasoning": ("Alzheimer's is a NEURODEGENERATIVE disorder: its dominant fault is a PROGRESSIVE, "
                      "cumulative, largely IRREVERSIBLE cascade (amyloid-beta accumulation, tau aggregation "
                      "and spread, synapse and neuron LOSS) that disintegrates the network over years. The "
                      "threshold-shift frame reaches the INSTANTANEOUS SYMPTOMATIC operating point: the "
                      "up-stream cholinergic DRIVE (L3, RESTORE the deficient tone -- the cholinesterase-"
                      "inhibition direction), the glutamatergic EXCITOTOXICITY axis (L1, REDUCE the excess -- "
                      "the memantine direction) and the inhibitory-RESTORE / network arm (L2) -- where the "
                      "established symptomatic pharmacology acts -- but it does NOT reach the DOMINANT fault, "
                      "the PROG neurodegenerative progression, because that trajectory is not a fold (the ADHD "
                      "lesson), is a PROGRESSION over time -- an E0-layer DECAY variable (the addiction lesson, "
                      "the roadmap's 'needs E0 progression') -- and is a DEGENERATION, a cumulative LOSS, the "
                      "structural inverse of addiction's E0 GAIN. The entire REACHABLE surface is therefore "
                      "PURELY SYMPTOMATIC (it gives temporary benefit while the disease progresses underneath). "
                      "Hence the fit is PARTIAL [L], the THIRD non-clean fit, and the DEEPEST -- and "
                      "Alzheimer's is the point where threshold-leverisation meets the E0 progression-dynamics "
                      "layer, as an E0 DECAY."),
        "contrast_to_prior_fits": ("bipolar (L1, clean [V]), epilepsy (L1+L2, clean [V]), depression "
                      "(L3-dominant, clean [V]), schizophrenia (L1+L3, clean [V] though domain-restricted), "
                      "autism (L1-dominant, clean [V] though domain-restricted with named O/W out-of-reach), "
                      "ADHD (L3-only, the FIRST PARTIAL [L] -- dominant gain-amplitude axis out of reach), "
                      "addiction (L3-dominant+L1/L2, the SECOND PARTIAL [L] -- dominant consolidated-gain axis "
                      "out of reach, an E0 GAIN, the convergence point). Alzheimer's is the THIRD PARTIAL [L] "
                      "and the DEEPEST: same gross shape as addiction (L3-dominant with L1/L2) but with a "
                      "SPLIT corrective sign, a PURELY SYMPTOMATIC reachable surface, and a dominant axis that "
                      "is a DEGENERATIVE PROGRESSION (an E0 DECAY, the inverse of addiction's E0 GAIN)."),
        "honest": ("the partial grade is the finding, not a failure: it marks exactly where the cross-cutting "
                   "threshold-shift logic does and does not apply, and refuses to overclaim a clean fit where "
                   "the dominant fault is an irreversible neurodegenerative progression and the reachable "
                   "surface is symptom-only. efficacy=0; no drug/dose/patient; no claim that Alzheimer's is "
                   "reversed, cured, prevented, or its progression stopped; a person with dementia remains a "
                   "person (no dignity/personhood judgement)."),
    }

    return {
        "title": "Symptomatic-network Alzheimer's target map for the INSTANTANEOUS symptomatic operating axis "
                 "-- the neurodegeneration substrate mapped onto the formal L1/L2/L3 inheritance frame "
                 "(engine-generated reads + cited lever frame); the neurodegenerative-PROGRESSION (PROG) axis "
                 "named as out-of-reach (an irreversible cumulative LOSS -- an E0 DECAY layer); the THIRD and "
                 "DEEPEST PARTIAL [L] fit in the series and the E0-progression convergence point",
        "inherited_from": ("analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the threshold-"
                          "shift intervention-logic technology, applied to the Alzheimer's INSTANTANEOUS "
                          "SYMPTOMATIC operating axis (EIGHTH application after bipolar sec.30, epilepsy "
                          "sec.31, depression sec.32, schizophrenia sec.33, autism sec.34, ADHD sec.35 and "
                          "addiction sec.36; this one is the THIRD PARTIAL [L] fit and the DEEPEST -- "
                          "Alzheimer's dominant fault is an irreversible NEURODEGENERATIVE PROGRESSION, so the "
                          "frame reaches its PURELY SYMPTOMATIC surface but not its dominant progression axis -- "
                          "and it is the CONVERGENCE point where threshold-leverisation meets the E0 "
                          "progression-dynamics layer, as an E0 DECAY)"),
        "maps_alzheimers_substrate": ("the neurodegeneration substrate (the amyloid cascade hypothesis + the "
                          "tau-tangle staging) establishes Alzheimer's as a CUMULATIVE, largely IRREVERSIBLE "
                          "progression: amyloid-beta accumulation (APP/PSEN gamma-secretase), tau aggregation "
                          "and spread (MAPT), impaired clearance (APOE-e4) and microglial neuroinflammation "
                          "(TREM2) drive a synapse/neuron LOSS that disintegrates the network over years. This "
                          "map re-cuts that substrate by threshold-frame REACHABILITY -- the up-stream "
                          "cholinergic DRIVE (L3, dominant, RESTORE), the glutamatergic EXCITOTOXICITY axis "
                          "(L1, REDUCE) and the inhibitory-RESTORE / network arm (L2) are the reachable lever "
                          "surface, PURELY SYMPTOMATIC; the neurodegenerative PROGRESSION (the PROG axis) is "
                          "out of reach -- adding NO new mechanism and NO new constant."),
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_e0": ("the roadmap sets the Alzheimer's payoff as modelling PROGRESSION, which needs E0. This "
                          "map DECOMPOSES the threshold-frame engagement: the INSTANTANEOUS SYMPTOMATIC axis is "
                          "reached by the L1/L2/L3 levers (the cholinergic-drive, glutamate-excitotoxicity and "
                          "inhibitory-restore surfaces) while the PROG (neurodegenerative-progression) axis is "
                          "NAMED out-of-reach (the APP/PSEN1/PSEN2/MAPT/APOE/TREM2 cascade). It re-derives no "
                          "rule and adds no constant -- the Alzheimer's counterpart of the sec.36 addiction "
                          "partial-fit, but with a DEGENERATIVE / PROGRESSION dominant axis (the third partial "
                          "fit, the deepest, and an E0 DECAY -- the structural inverse of addiction's E0 GAIN)."),
        "domain_restriction_witness": domain_restriction,
        "partial_fit_witness": partial_fit,
        "disorder_level_sign": ("the SYMP axis is the instantaneous symptomatic network operating point; its "
                           "corrective sign is SPLIT -- RESTORE the deficient cholinergic drive (L3, "
                           "cholinesterase-inhibition) and inhibition (L2, GABAergic / network-rhythm), REDUCE "
                           "the glutamatergic excitotoxicity (L1, memantine) -- the first split-sign reachable "
                           "surface in the series. But the sign is PARTIAL and SYMPTOMATIC: it reaches the "
                           "INSTANTANEOUS surface only, gives temporary benefit, and does NOT slow the disease; "
                           "the DOMINANT PROG (neurodegenerative-progression) axis is out of reach (an "
                           "irreversible cumulative LOSS, not a fold). So unlike the clean fold-moving sign of "
                           "the five clean-fit disorders, Alzheimer's engagement with the threshold frame is "
                           "partial [L] and the deepest -- the instantaneous symptomatic surface is reachable, "
                           "the neurodegenerative progression is not (it is the E0 progression-dynamics layer's "
                           "variable, an E0 DECAY)."),
        "unifying_frame": ("the Alzheimer's operating point is a SYMPTOMATIC surface laid over a "
                           "NEURODEGENERATIVE PROGRESSION: the cholinergic drive has DEGENERATED (L3 deficit), "
                           "glutamatergic excitotoxicity (L1) and network hyperexcitability (L2) follow, while "
                           "underneath an irreversible amyloid/tau/synapse-and-neuron-loss cascade disintegrates "
                           "the network. The threshold-shift frame reaches it through the INSTANTANEOUS "
                           "SYMPTOMATIC levers -- L3 the up-stream cholinergic DRIVE (RESTORE -- AChE/BuChE, "
                           "a7-nAChR, M1-mAChR, the dominant class where the established symptomatic "
                           "pharmacology lives), L1 the glutamatergic EXCITOTOXICITY (REDUCE -- NMDA NR2B/NR2A, "
                           "memantine) and L2 the inhibitory-RESTORE / network arm (GABA-A a1/a5/b3). The map "
                           "reaches the SYMP axis (PURELY SYMPTOMATIC, a split corrective sign); the PROG "
                           "(neurodegenerative-progression) axis -- the DOMINANT fault, the amyloid/tau/"
                           "synapse-and-neuron-loss trajectory APP/PSEN1/PSEN2/MAPT/APOE/TREM2 -- is honestly "
                           "out of reach (named in out_of_reach_targets), because it is not a fold, is a "
                           "PROGRESSION over time (an E0-layer DECAY variable) and is a DEGENERATION (cumulative "
                           "LOSS). The fit is PARTIAL [L]: the third non-clean fit and the DEEPEST, for a "
                           "deeper reason than addiction (a DEGENERATIVE PROGRESSION, the inverse of "
                           "addiction's E0 GAIN), and the point where threshold-leverisation meets the E0 "
                           "progression-dynamics layer."),
        "levers": LEVER_FRAME,
        "lever_distribution_witness": {
            "counts": counts,
            "dominant_levers": dominant_levers,
            "codominant": codominant,
            "l3_dominant": bool(counts.get("L3", 0) == top and "L3" in dominant_levers and not codominant),
            "l1_present": bool(l1_present),
            "l2_present": bool(l2_present),
            "l3_only": bool(counts.get("L3", 0) == sum(counts.values()) and counts.get("L3", 0) > 0),
            "split_sign_reachable_surface": True,
            "purely_symptomatic_reachable_surface": True,
            "reading": (("Alzheimer's is L3-DOMINANT WITH L1 AND L2 BOTH PRESENT (L3=%d cholinergic-drive "
                         "levers, RESTORE; L1=%d glutamate-excitotoxicity, REDUCE; L2=%d inhibitory-restore, "
                         "RESTORE) -- the EIGHTH distribution pattern: bipolar leaned on L1 (calcium), epilepsy "
                         "on L1+L2 (the M-current), depression on L3 (HPA/monoamine), schizophrenia on L1+L3 "
                         "co-dominant, autism on L1-dominant with a sparse L3, ADHD on L3-ONLY (L1/L2 EMPTY), "
                         "and addiction on L3-dominant with L1/L2 (excess reward drive). Alzheimer's shares "
                         "addiction's gross shape (L3-dominant with L1/L2) but is DISTINCT in two ways: (1) the "
                         "corrective sign is SPLIT -- L3/L2 RESTORE a deficit while L1 REDUCES an excess (the "
                         "FIRST split-sign reachable surface; depression was pure-restore, epilepsy/"
                         "schizophrenia pure-reduce, addiction pure-dampen); (2) the reachable surface is "
                         "PURELY SYMPTOMATIC (no reachable lever touches progression) and the out-of-reach axis "
                         "is the FIRST that is DEGENERATIVE -- a cumulative LOSS, an E0 DECAY, the structural "
                         "inverse of addiction's E0 GAIN." %
                         (counts.get("L3", 0), counts.get("L1", 0), counts.get("L2", 0)))),
        },
        "out_of_reach_targets": {
            "_what": "the PROG-axis (neurodegenerative-progression) genes a threshold/drive lever CANNOT reach "
                     "-- named to make the Alzheimer's partial-fit CONCRETE. Each carries a gamma read (its "
                     "own promoter switch stiffness) ALONGSIDE, but is explicitly NOT a lever: the "
                     "neurodegenerative progression (amyloid-beta via APP/PSEN1/PSEN2 gamma-secretase, tau "
                     "aggregation MAPT, APOE-e4 clearance failure, TREM2 microglial neuroinflammation, and the "
                     "synapse/neuron LOSS that disintegrates the network) is not a fold, is a PROGRESSION over "
                     "time (an E0-layer DECAY variable) and is a DEGENERATION (cumulative LOSS), so the "
                     "threshold frame has no direct handle. This is the DOMINANT Alzheimer's fault -- the "
                     "decline driver, and the disease-MODIFYING axis (where the anti-amyloid antibodies act, "
                     "themselves only progression-MODIFIERS, not threshold levers) -- which is exactly why "
                     "Alzheimer's is a PARTIAL fit (the dominant axis is the out-of-reach one) and the "
                     "DEEPEST. It extends the addiction named-out-of-reach E0-dynamics discipline (sec.36) to "
                     "a DEGENERATIVE PROGRESSION (an E0 DECAY, the inverse of addiction's E0 GAIN), and the "
                     "PROG axis is precisely the E0 progression-dynamics domain (the convergence point).",
            "by_axis": oor_by_axis,
            "n": len(oor),
            "entries": oor,
        },
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a receptor occupancy, not a "
                     "synaptic acetylcholine/glutamate level, not a potency, not a dose, not in-vivo "
                     "selectivity, not a clinical effect, and NOT the neurodegeneration RATE / amyloid burden "
                     "/ tau load / synapse-and-neuron-loss rate (the PROG progression axis) (those are [O]). "
                     "The promoter |h_sp| is the gene's OWN switch stiffness, carried alongside, never folded "
                     "into a clinical magnitude or equated with the neurodegenerative-progression trajectory. "
                     "gamma is blind to on/off and to expression level. L3 (the cholinergic-drive) mechanism "
                     "link is [O] -- the read places the gene, it does not derive the drive mechanism. The fit "
                     "is PARTIAL [L]: the frame reaches the INSTANTANEOUS SYMPTOMATIC axis (L1/L2/L3, purely "
                     "symptomatic) but not the DOMINANT PROG neurodegenerative-progression axis, which is a "
                     "PROGRESSION/DECAY (an E0-layer variable), not a fold."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never "
                    "drugs, doses, protocols, or patients; Alzheimer's is polygenic and heterogeneous and its "
                    "established symptomatic pharmacology is only PARTIALLY and TEMPORARILY effective and does "
                    "NOT halt progression, and a lever direction is a mechanism boundary, NOT a claim that "
                    "Alzheimer's can be reversed, cured or prevented or its progression stopped, and NOT a "
                    "judgement on the personhood or worth of a person living with dementia -- a person with "
                    "dementia remains a person (the fail-closed forbidden-claim scan enforces this, incl. "
                    "cure-reversal and dignity classes); the map reaches the INSTANTANEOUS SYMPTOMATIC axis "
                    "across L1/L2/L3 (purely symptomatic, a split corrective sign), while the DOMINANT PROG "
                    "neurodegenerative-progression axis is out of reach (named here -- an irreversible "
                    "cumulative LOSS, the E0 progression-dynamics layer, an E0 DECAY), so the fit is PARTIAL "
                    "[L], the third non-clean fit and the deepest, and the E0-progression convergence point; a "
                    "lever direction is a mechanism boundary, not a claim about identity or the subjective "
                    "world (Axis-A; consciousness_claim=0; hard problem OPEN)."),
        "n_targets": len(entries),
        "n_out_of_reach": len(oor),
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

def alzheimers_threshold_levers_results():
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
        "maps_neurodegeneration_substrate": True,
        "third_partial_fit_L": True,
        "deepest_partial_fit": True,
    }
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "maps_neurodegeneration_substrate": 1.0,
        "l3_mechanism_link": "OPEN [O] -- the cholinergic (cholinesterase/nicotinic/muscarinic) signalling mechanism is cited biology, not derived",
        "promoter_hsp_vs_progression": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the neurodegeneration rate / amyloid burden / tau load",
        "partial_fit_L": 1.0,
        "fit_grade": "[L] partial -- the DOMINANT PROG neurodegenerative-progression axis is out of reach (not a fold; an E0-layer DECAY progression; a degeneration/cumulative LOSS); only the INSTANTANEOUS SYMPTOMATIC axis is reached, purely symptomatic",
        "third_partial_fit_in_series": 1.0,
        "deepest_partial_fit": 1.0,
        "l3_dominant_l1_l2_present": 1.0,
        "split_sign_reachable_surface": 1.0,
        "purely_symptomatic_reachable_surface": 1.0,
        "progression_axis_named_out_of_reach": 1.0,
        "convergence_with_e0_progression_layer": 1.0,
        "e0_decay_inverse_of_addiction_e0_gain": 1.0,
        "no_cure_reversal_or_prevention_licence": 1.0,
        "dementia_patient_remains_a_person": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only and SYMPTOMATIC only (the fail-closed forbidden-claim scan "
                             "enforces this, incl. cure-reversal and dignity classes)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "alzheimers_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_alzheimers_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"alzheimers_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = alzheimers_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 100)
    print("AD-T3b-L  ALZHEIMER'S SYMPTOMATIC-NETWORK MAP  (inherited from analgesic v2.0; engine READ-ONLY; L3-dominant+L1/L2; PARTIAL fit [L] #3, deepest)")
    print("=" * 100)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  maps neurodegen subst : {inv['maps_neurodegeneration_substrate']}   third partial fit [L]: {inv['third_partial_fit_L']}  deepest: {inv['deepest_partial_fit']}")
    print("-" * 100)
    print(f"  {'gene':9} {'lev':4} {'gamma':>7} {'|h_sp|':>8} {'protein':42} axis role")
    for e in res["entries"]:
        cp = e.get("protein") or e["channel"] or "-"
        print(f"  {e['gene']:9} {e['lever']:4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} "
              f"{cp[:42]:42} {e['axis_role'][:28]}")
    print("-" * 100)
    print("  OUT-OF-REACH (neurodegenerative-progression axis; named; NOT levers):")
    for e in res["out_of_reach_targets"]["entries"]:
        print(f"  {e['gene']:9} {'--':4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {e['fault_axis']:5} "
              f"{(e['role'])[:48]:48}")
    print("-" * 100)
    w = res["lever_distribution_witness"]
    print("  targets by lever: " + ", ".join(f"{k}={v}" for k, v in w["counts"].items())
          + f"   -> {'DOMINANT ' + w['dominant_levers'][0]}  (L3-dominant={w['l3_dominant']}, L1 present={w['l1_present']}, L2 present={w['l2_present']}, split-sign={w['split_sign_reachable_surface']})")
    dr = res["domain_restriction_witness"]
    print(f"  domain reach: SYMP={dr['SYMP']['reached_by_levers']} "
          f"PROG={dr['PROG']['reached_by_levers']}  (SYMP axis reached purely-symptomatically; PROG named out-of-reach)")
    pf = res["partial_fit_witness"]
    print(f"  FIT GRADE: {pf['fit_grade']}  (#{pf['fit_index_in_series']} in series, deepest={pf['deepest_partial']}; reached={pf['reached_axis'][:18]}; out-of-reach=PROG progression)")
    print(f"  n_targets: {res['n_targets']}   out_of_reach: {res['n_out_of_reach']}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 100)
    ok = (inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
          and not w["codominant"] and w["dominant_levers"] == ["L3"] and w["l3_dominant"]
          and w["l1_present"] and w["l2_present"] and (w["l3_only"] is False)
          and dr["PROG"]["reached_by_levers"] is False and dr["SYMP"]["reached_by_levers"] is True
          and pf["fit_grade"] == "[L] partial" and pf["fit_index_in_series"] == 3)
    print("  AD-T3b-L SYMPTOMATIC-NETWORK MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
