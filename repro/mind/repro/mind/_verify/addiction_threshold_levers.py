#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
addiction_threshold_levers.py  —  ADD-T-L (sec.36): the reward-drive target map for the addiction
incentive-sensitisation operating point, and the SEVENTH application of the inherited
analgesic_threshold_logic v2.0 cross-cutting layer (after bipolar sec.30, epilepsy sec.31,
depression sec.32, schizophrenia sec.33, autism sec.34 and ADHD sec.35). It re-derives no rule: it
reads the SAME R19 substrate (E.spinodal/E.barrier) and the SAME gamma = -mean(NN stacking dG,
SantaLucia 1998) the engine uses to write genes, and it maps the addiction substrate (the sec.28
state-switching / E0 plasticity incentive-sensitisation model) onto the formal L1/L2/L3 frame by
threshold-frame REACHABILITY.

WHY THIS IS THE SECOND *PARTIAL* FIT [L] -- AND THE CONVERGENCE POINT (the headline). ADHD (sec.35)
was the first partial fit: its DOMINANT axis (the gain-amplitude machinery) was out of reach because a
drive-tone lever has no handle on catecholamine synthesis/release. Addiction is the SECOND partial fit,
for a DIFFERENT and deeper reason. Addiction is a disorder of INCENTIVE SENSITISATION: repeated drug/cue
exposure TRAINS the reward circuit (a plasticity process -- the E0 layer of sec.26) into a low-threshold
attractor whose reward GAIN has GROWN and CONSOLIDATED, so that cues drive excessive dopaminergic
"wanting" that persists after withdrawal (relapse, cue-reactivity). The threshold-shift frame reaches the
INSTANTANEOUS operating point richly -- the up-stream reward DRIVE (L3, where the established addiction
pharmacology lives: naltrexone, varenicline, bupropion, nalmefene), the glutamatergic plasticity
SUBSTRATE (L1, the NMDA side acamprosate/N-acetylcysteine touch), and the inhibitory-RESTORE arm (L2,
the topiramate direction). But it does NOT reach the disorder's DOMINANT fault: the CONSOLIDATED
SENSITISATION GAIN (the SG axis) -- the LEARNED amplitude growth of the reward response, the durable
plastic trace that drives chronicity and relapse. That axis is out of reach in BOTH senses ADHD taught
and a third: (a) it is a GAIN, not a FOLD (a fold lever does not set a gain -- the ADHD lesson); (b) it
is CONSOLIDATED / LEARNED -- a PLASTICITY (E0-layer) variable, not an instantaneous fold, so even the
drive levers that dampen the instantaneous response cannot ERASE the durable trace; this is precisely
the E0 plasticity layer (the domain a dynamics module would model, sec.26 / the handover's B-ii route).
So addiction is where threshold-leverisation (B-i) STRUCTURALLY MEETS the plasticity layer: the frame
catches the instantaneous reward drive but not the consolidated learned gain. The fit is therefore
PARTIAL [L] -- the second non-clean fit -- and the partial grade is the honest record of exactly where
the cross-cutting logic stops.

THE TWO ADDICTION AXES (re-cut here by threshold-frame REACHABILITY):
  INSTANT  (the instantaneous drive / excitability operating point)  = REACHED by the lever frame across
        all three classes: L3 the up-stream reward DRIVE (mu/kappa-opioid, D2, DAT, nAChR), L1 the
        glutamatergic plasticity SUBSTRATE (NMDA NR2A/NR2B), L2 the inhibitory-RESTORE arm (GABA-A). This
        is where the established addiction pharmacology acts, as DIRECTIONS. Corrective sign = DAMPEN /
        NORMALISE the sensitised reward drive and RESTORE inhibitory balance.
  SG  (consolidated sensitisation GAIN -- the learned plastic trace)  = the DOMINANT addiction fault: the
        CONSOLIDATED amplitude growth of the reward response (deltaFosB accumulation, BDNF-driven
        remodelling, the CREB tolerance/dependence programme, ARC-mediated consolidation). NOT REACHED: it
        is a GAIN not a fold (the ADHD lesson) AND it is LEARNED / consolidated -- a PLASTICITY (E0-layer)
        variable, not an instantaneous fold -- so no threshold/drive lever erases it (it is the E0
        dynamics domain). The threshold frame reaches it only INDIRECTLY (dampen the instantaneous drive
        -> the trace is exercised less), never as a direct handle -- which is exactly why addiction is a
        PARTIAL fit, the DOMINANT axis being the out-of-reach one.

THE LEVER DISTRIBUTION (honest). Where bipolar leaned on L1 (calcium), epilepsy on L2 (the M-current),
depression on L3 (HPA/monoamine, L3-dominant with a reachable L1/L2 mix), schizophrenia on L1+L3
co-dominant (glutamate + dopamine), autism on L1-DOMINANT with a sparse L3, and ADHD on L3-ONLY (L1/L2
EMPTY), addiction is L3-DOMINANT WITH L1 AND L2 BOTH PRESENT -- the SEVENTH distribution pattern:
  L1  reduce the inward excitatory / restore glutamate homeostasis (NMDA NR2A/NR2B)   (2 levers)
  L2  increase the outward / restore GABA-A inhibition (GABA-A a2/g3)                  (2 levers)
  L3  normalise an UP-STREAM reward DRIVE (mu/kappa-opioid, D2, DAT, nAChR)            (5 levers, DOMINANT)
This is the exact TEXTURAL INVERSE of ADHD's emptiness: ADHD was L3-ONLY because it is "not a
channelopathy" -- it had NO ionic lever; addiction ENGAGES the ionic levers too (it is not channel-free),
yet is STILL partial, because its dominant fault is a CONSOLIDATED plastic gain, not an instantaneous
excitability the levers can move. Richer reachable surface than ADHD, same partial verdict, deeper reason.

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| / barrier
are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V] (reproducible);
their ORDER is [F] (forced). This is NOT a receptor occupancy, NOT a synaptic dopamine/opioid level, NOT
a drug potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect, and -- the addiction-
specific addition -- the promoter |h_sp| is NOT the consolidated sensitisation GAIN (the learned reward-
circuit amplitude / the deltaFosB trace). gamma is blind to on/off and to expression level. The L3
(reward-drive) mechanism link is [O].

THE HONEST CAVEATS (addiction-specific; recorded, not hidden).
  (i)   PARTIAL FIT [L] (the SECOND in the series). The DOMINANT addiction fault (the SG consolidated
        sensitisation-gain axis) is OUT OF REACH of the threshold frame, because it is a LEARNED /
        plastic gain (an E0-layer variable), not an instantaneous fold. Only the INSTANTANEOUS drive/
        excitability surface is reached. Recorded as the fit_grade.
  (ii)  L3 SIGN-SUBTLETY. The reward-drive sign is not a single "block": naltrexone/nalmefene ANTAGONISE
        opioid reward (mu) while kappa (OPRK1) is the ANTI-reward arm (opposite valence); DAT/bupropion
        and nicotinic/varenicline use SUBSTITUTION/partial-agonist logic (not pure block); striatal D2 is
        REDUCED in addiction (so "block D2" is not the direction). gamma is [V] for promoter STRUCTURE
        only; every clinical DIRECTION is graded [O].
  (iii) THE CONVERGENCE. The out-of-reach SG axis is precisely the E0 plasticity layer (sec.26): a
        dynamics module (the handover's B-ii) would model the consolidated trace directly. B-i (this map)
        NAMES it out-of-reach honestly. Addiction is the point where the two routes meet.

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places READS and
TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any agent treats anyone. Addiction
is POLYGENIC and HETEROGENEOUS, its established pharmacology is only PARTIALLY effective (high relapse),
and a lever direction is a mechanism boundary, NOT a route to obtain or use any substance, NOT a claim
that addiction can be "cured", and NOT a moral judgement (addiction is a treatable medical condition, not
a failure of will). The forbidden-claim scanner enforces this (incl. a DRUG-SEEKING/MISUSE class and a
CURE-MIRACLE class). consciousness_claim stays 0; hard problem OPEN.

No tuning: gamma is measured; |h_sp|/barrier are the locked R19 forms; the lever assignments, axis
mapping and citations are CITED Layer-2 biology + the sec.28/E0 sensitisation substrate, not engine
outputs. Governed by VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 addiction_threshold_levers.py
Out:  addiction_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "addiction_levers_promoters.cache.json")
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

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the addiction reward-drive axis) ----
LEVER_FRAME = {
  "L1": "reduce the inward excitatory / restore glutamate homeostasis (NMDA NR2A/NR2B) -- the "
        "glutamatergic plasticity SUBSTRATE of incentive sensitisation. PRESENT for addiction (2 levers): "
        "NMDA-dependent LTP in the reward circuit is the substrate the sensitisation trace is written on, "
        "and the glutamate side is where acamprosate / N-acetylcysteine / memantine act (as DIRECTIONS). "
        "Reaches the INSTANTANEOUS glutamatergic drive; the CONSOLIDATED trace itself is out of reach. "
        "The mechanism link is [O]",
  "L2": "increase the outward / restore the GABA-A inhibitory current (GABA-A a2/g3) -- the "
        "inhibitory-RESTORE arm. PRESENT for addiction (2 levers): the alcohol-dependence GABA-A GWAS arm "
        "(GABRA2/GABRG3), the topiramate (GABA-A enhance + AMPA/kainate block) DIRECTION. Reaches the "
        "INSTANTANEOUS inhibitory balance. The mechanism link is [O]",
  "L3": "normalise an UP-STREAM reward DRIVE. The DOMINANT lever class for addiction (5 levers): the "
        "mu/kappa-opioid receptors, the D2 receptor, the dopamine transporter and the nicotinic receptor "
        "set the reward-DRIVE TONE -- the surface the established addiction pharmacology acts on (as "
        "DIRECTIONS: naltrexone/nalmefene, varenicline, bupropion). This reaches the INSTANTANEOUS reward "
        "drive ONLY; the CONSOLIDATED sensitisation GAIN (the SG axis) is out of reach (partial fit [L]). "
        "The mechanism link is [O]",
}

# grade strings
GL3 = ("[O] cited biology: gamma places the gene in the reward-drive lever map; the reward/incentive "
       "(opioid/dopamine/nicotinic) signalling mechanism is NOT derived")
GL1 = ("[O] cited biology: gamma places the gene in the glutamatergic plasticity-substrate lever map; "
       "the NMDA/glutamate signalling mechanism is NOT derived")
GL2 = ("[O] cited biology: gamma places the gene in the inhibitory-restore lever map; the GABA-A "
       "inhibitory signalling mechanism is NOT derived")

DOM_INSTANT = "INSTANT (the instantaneous drive/excitability operating point the levers REACH)"

# ===================== LEVER TARGETS (the genes that ARE the levers; L1/L2/L3) =====================
CONTEXT = {
  # ---- L3 reward/incentive DRIVE (dominant lever class) ----
  "OPRM1": dict(lever="L3", domain=DOM_INSTANT, channel=None, protein="mu-opioid receptor (OPRM1)",
      axis_role="reward drive (opioid)",
      push="ANTAGONISE the mu-opioid reward drive (the naltrexone/naloxone/nalmefene DIRECTION) -- the most established addiction-pharmacology node; mu signalling sets opioid reward tone",
      add_anchor="the mu-opioid receptor (OPRM1); the A118G (rs1799971) variant is the most-studied addiction pharmacogenetic locus and OPRM1 is the target of naltrexone/nalmefene in alcohol and opioid use disorder -- the canonical reward-drive node",
      drive_agent="mu-opioid antagonism DIRECTION for the reward-drive axis (the naltrexone route, as DIRECTION, not efficacy; not a dose; not a route to obtain or use any substance)",
      grade_mechanism=GL3,
      src="Ray 2007 (OPRM1 A118G, naltrexone response); Volkow 2016 NEJM 374:363 (opioid reward, OPRM1)"),
  "OPRK1": dict(lever="L3", domain=DOM_INSTANT, channel=None, protein="kappa-opioid receptor (OPRK1)",
      axis_role="anti-reward / dysphoria drive (opioid)",
      push="MODULATE the kappa-opioid ANTI-reward / dysphoria arm (the nalmefene/kappa-antagonist DIRECTION) -- kappa is the OPPOSITE-valence opioid arm (dynorphin drives the negative-affect, stress-induced relapse state); a sign-subtle [O] handle",
      add_anchor="the kappa-opioid receptor (OPRK1); the dynorphin/kappa system drives the anti-reward / dysphoric state and stress-induced relapse, the target of kappa modulation (nalmefene partial activity) -- the opposite-valence opioid drive",
      drive_agent="kappa-opioid modulation DIRECTION for the reward-drive axis (the anti-reward arm; sign-subtle; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Bruchas 2010 (dynorphin/kappa, dysphoria, relapse); Volkow 2016 NEJM 374:363 (anti-reward, kappa)"),
  "DRD2": dict(lever="L3", domain=DOM_INSTANT, channel=None, protein="dopamine receptor D2 (DRD2)",
      axis_role="reward drive (dopamine)",
      push="normalise the dopaminergic reward readout via the D2 receptor -- striatal D2 is REDUCED in addiction (the Taq1A/ANKK1 locus), so the direction is to RESTORE reward-prediction balance, NOT to block D2; a sign-subtle [O] handle",
      add_anchor="the dopamine D2 receptor (DRD2); the Taq1A/ANKK1 locus is among the most-replicated addiction susceptibility variants and low striatal D2 availability is a hallmark of addiction -- the dopaminergic reward-drive readout",
      drive_agent="D2 dopaminergic-readout DIRECTION for the reward-drive axis (sign-subtle: D2 is reduced in addiction; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Blum 1990 / Noble 2003 (DRD2 Taq1A, addiction); Volkow 2009 (low striatal D2 in addiction)"),
  "SLC6A3": dict(lever="L3", domain=DOM_INSTANT, channel=None, protein="dopamine transporter DAT (SLC6A3)",
      axis_role="reward drive (dopamine tone)",
      push="modulate the dopaminergic reward tone via DAT reuptake -- the bupropion (DAT/NET inhibitor) DIRECTION in smoking cessation; SUBSTITUTION/replacement logic (raise tonic dopamine to offset the drug), a sign-subtle [O] handle",
      add_anchor="the dopamine transporter (DAT/SLC6A3); the target of bupropion in smoking cessation and the reuptake node that sets ambient dopamine tone -- the dopaminergic reward-tone lever",
      drive_agent="dopaminergic reuptake-modulation DIRECTION for the reward-drive axis (the bupropion/substitution route; sign-subtle; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Hughes 2014 (bupropion, smoking cessation); Volkow 2016 NEJM 374:363 (DAT, dopamine reward)"),
  "CHRNA5": dict(lever="L3", domain=DOM_INSTANT, channel=None, protein="nicotinic acetylcholine receptor alpha-5 (CHRNA5)",
      axis_role="reward drive (nicotinic)",
      push="modulate the nicotinic reward drive via the alpha-5 nAChR subunit -- the varenicline (partial-agonist) DIRECTION; partial agonism reduces nicotine reward while blunting withdrawal, a sign-subtle [O] handle",
      add_anchor="the nicotinic alpha-5 subunit (CHRNA5); the D398N (rs16969968) variant in the 15q25 cluster is the strongest nicotine-dependence GWAS hit, and the nAChR is the target of varenicline -- the nicotinic reward-drive node",
      drive_agent="nicotinic partial-agonist DIRECTION for the reward-drive axis (the varenicline route; sign-subtle; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Bierut 2008 (CHRNA5 rs16969968, nicotine dependence); Cahill 2016 Cochrane (varenicline, nAChR)"),
  # ---- L1 glutamatergic plasticity SUBSTRATE (present, secondary) ----
  "GRIN2A": dict(lever="L1", domain=DOM_INSTANT, channel="NMDA NR2A (GRIN2A)", protein="NMDA receptor NR2A subunit (GRIN2A)",
      axis_role="glutamatergic plasticity substrate",
      push="reduce / restore the glutamatergic (NMDA NR2A) drive -- the substrate of reward-circuit LTP; the acamprosate / N-acetylcysteine glutamate-homeostasis DIRECTION reaches this INSTANTANEOUS glutamatergic surface (the consolidated trace itself is out of reach), an [O] handle",
      add_anchor="the NMDA NR2A subunit (GRIN2A); NMDA-dependent synaptic plasticity in the VTA/nucleus accumbens is the substrate on which incentive sensitisation is written -- the glutamatergic side acamprosate/NAC modulate",
      drive_agent="glutamate-homeostasis DIRECTION for the plasticity-substrate axis (the acamprosate/NAC route; DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Kalivas 2009 Nat Rev Neurosci 10:561 (glutamate homeostasis in addiction); Mason 2014 (acamprosate)"),
  "GRIN2B": dict(lever="L1", domain=DOM_INSTANT, channel="NMDA NR2B (GRIN2B)", protein="NMDA receptor NR2B subunit (GRIN2B)",
      axis_role="glutamatergic plasticity substrate",
      push="reduce / restore the glutamatergic (NMDA NR2B) drive -- the NR2B-containing NMDA receptors that gate reward-circuit LTP; the memantine / glutamate-modulation DIRECTION reaches this INSTANTANEOUS surface (not the consolidated trace), an [O] handle",
      add_anchor="the NMDA NR2B subunit (GRIN2B); NR2B-containing NMDA receptors gate plasticity in the reward circuit -- a glutamatergic plasticity-substrate node touched by memantine/glutamate-modulating agents",
      drive_agent="glutamate-modulation DIRECTION for the plasticity-substrate axis (the memantine route; DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Kalivas 2009 Nat Rev Neurosci 10:561 (glutamate/NMDA in addiction); sec.26 (the plasticity layer)"),
  # ---- L2 inhibitory-RESTORE (present, minor) ----
  "GABRA2": dict(lever="L2", domain=DOM_INSTANT, channel="GABA-A a2 (GABRA2)", protein="GABA-A receptor alpha-2 subunit (GABRA2)",
      axis_role="inhibitory restore",
      push="restore GABA-A inhibition via the alpha-2 subunit -- the alcohol-dependence GABA-A GWAS arm; the topiramate (GABA-A enhance) DIRECTION raises inhibitory tone in the reward circuit, an [O] handle",
      add_anchor="the GABA-A alpha-2 subunit (GABRA2); the most-replicated GABA-A association in alcohol dependence (Edenberg 2004) -- the ionotropic inhibitory-restore node",
      drive_agent="GABA-A enhancement DIRECTION for the inhibitory-restore axis (the topiramate route; DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Edenberg 2004 Am J Hum Genet 74:705 (GABRA2, alcohol dependence); Johnson 2007 (topiramate)"),
  "GABRG3": dict(lever="L2", domain=DOM_INSTANT, channel="GABA-A g3 (GABRG3)", protein="GABA-A receptor gamma-3 subunit (GABRG3)",
      axis_role="inhibitory restore",
      push="restore GABA-A inhibition via the gamma-3 subunit -- a GABA-A cluster gene associated with alcohol dependence; raises inhibitory tone on the same L2 axis, an [O] handle",
      add_anchor="the GABA-A gamma-3 subunit (GABRG3); a GABA-A receptor-cluster gene associated with alcohol dependence -- a secondary ionotropic inhibitory-restore node",
      drive_agent="GABA-A enhancement DIRECTION for the inhibitory-restore axis (DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Dick 2004 (GABRG3, alcohol dependence); Edenberg 2004 (the GABA-A alcohol arm)"),
}

# ===== OUT-OF-REACH TARGETS (the SG consolidated sensitisation-gain axis a threshold lever CANNOT reach) =====
# These are NOT levers. They carry a gamma read (their own promoter switch stiffness) ALONGSIDE, with the
# explicit record that NO threshold/drive lever reaches the SG axis: the consolidated gain is a LEARNED /
# plastic (E0-layer) variable, not an instantaneous fold. Naming them makes the addiction partial-fit
# concrete: the disorder's DOMINANT axis (the consolidated trace driving chronicity/relapse) is out of reach.
OUT_OF_REACH = {
  "FOSB": dict(axis="SG", role="deltaFosB -- the master sensitisation transcription switch (accumulates with exposure)", channel=None,
      why_unreached="the SG (consolidated sensitisation-gain) axis: deltaFosB is the stable transcription factor that ACCUMULATES with repeated exposure and is the master molecular switch of the consolidated reward gain -- a LEARNED / plastic (E0-layer) state, NOT an instantaneous fold, so a threshold/drive lever cannot reach or erase it (this is the dominant addiction fault, the relapse driver)",
      add_anchor="deltaFosB (FOSB); the stable, accumulating transcription factor widely identified as the molecular switch of addiction -- it records the CONSOLIDATED reward gain and persists after withdrawal (a plasticity trace, not an excitability fold)",
      src="Nestler 2008 Philos Trans R Soc B 363:3245 (deltaFosB, addiction switch); sec.26 (E0 plasticity layer)"),
  "BDNF": dict(axis="SG", role="brain-derived neurotrophic factor -- activity-dependent reward-circuit remodelling", channel=None,
      why_unreached="the SG (consolidated sensitisation-gain) axis: BDNF drives the activity-dependent synaptic REMODELLING that consolidates the sensitised reward gain in the VTA/accumbens -- a plasticity (E0-layer) mechanism that BUILDS the durable trace, not an instantaneous fold a drive lever can move",
      add_anchor="brain-derived neurotrophic factor (BDNF); the neurotrophin driving experience-dependent remodelling of the reward circuit during sensitisation -- a consolidation mechanism, not a tone",
      src="Russo 2009 Trends Neurosci 32:267 (BDNF, reward plasticity); sec.26 (E0 plasticity layer)"),
  "CREB1": dict(axis="SG", role="CREB -- the tolerance/dependence transcription programme", channel=None,
      why_unreached="the SG (consolidated sensitisation-gain) axis: CREB drives the transcription programme underlying tolerance and the negative-affect of dependence -- a learned (E0-layer) adaptation that sets the consolidated set-point, not an instantaneous fold reachable by a threshold lever",
      add_anchor="CREB (CREB1); the cAMP-response-element-binding transcription factor whose programme underlies tolerance and dependence-related plasticity -- a consolidation mechanism",
      src="Nestler 2008 Philos Trans R Soc B 363:3245 (CREB, tolerance/dependence); sec.26 (E0 plasticity layer)"),
  "ARC": dict(axis="SG", role="ARC/Arg3.1 -- activity-regulated synaptic consolidation", channel=None,
      why_unreached="the SG (consolidated sensitisation-gain) axis: ARC is the immediate-early effector of synaptic CONSOLIDATION (AMPA-receptor trafficking, late-phase plasticity) that stabilises the sensitised trace -- a plasticity (E0-layer) effector, not an instantaneous excitability fold a drive lever sets",
      add_anchor="ARC/Arg3.1 (ARC); the activity-regulated cytoskeleton-associated effector of synaptic consolidation and AMPA trafficking that stabilises plastic changes -- a consolidation mechanism, not a tone",
      src="Shepherd 2011 (ARC, synaptic consolidation); sec.26 (E0 plasticity layer)"),
}

def read(sym, g):
    c = CONTEXT[sym]
    grade_open = {"L1": GL1, "L2": GL2, "L3": GL3}[c["lever"]]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the consolidated sensitisation gain)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "domain_reach": c["domain"],
        "axis_role": c["axis_role"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "addiction_genetic_anchor": c["add_anchor"],
        "instant_axis_drive_agent_direction": c["drive_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": grade_open,
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_sensitisation_gain": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch "
                                       "stiffness, NOT the consolidated sensitisation GAIN (the learned "
                                       "reward-circuit amplitude / the deltaFosB trace); never equated",
        "grade_clinical_map": "[O] OPEN -- not a receptor occupancy, synaptic dopamine/opioid level, "
                              "potency, dose, in-vivo selectivity, or clinical effect",
        "context_grade": "CITED Layer-2 biology + the sec.28/E0 sensitisation substrate (not an engine output)",
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
        "addiction_genetic_anchor": c["add_anchor"],
        "grade_read": "[V] reproducible promoter-switch-threshold read (carried alongside; does NOT place a lever)",
        "grade_reach": "[F] NOT REACHED -- the threshold/drive frame has no handle on the consolidated "
                       "sensitisation-gain axis (a learned/plastic E0-layer variable, not an instantaneous fold)",
        "context_grade": "CITED Layer-2 biology + the sec.28/E0 sensitisation substrate (not an engine output)",
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
    # out-of-reach reads (the named SG sensitisation-gain targets)
    oor_g = {s: gamma(cache[s]["seq"]) for s in OUT_OF_REACH if s in cache}
    oor = [read_out_of_reach(s, oor_g[s]) for s in oor_g]
    oor.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)
    oor_by_axis = {}
    for e in oor:
        oor_by_axis.setdefault(e["fault_axis"], []).append(e["gene"])

    # lever-distribution witness: addiction is L3-DOMINANT with L1 AND L2 present
    counts = {k: len(v) for k, v in by_lever.items()}
    ranked = sorted(counts, key=lambda k: counts[k], reverse=True)
    top = counts[ranked[0]]
    dominant_levers = sorted([k for k, n in counts.items() if n == top])
    codominant = len(dominant_levers) >= 2
    l1_present = counts.get("L1", 0) > 0
    l2_present = counts.get("L2", 0) > 0

    # domain-restriction / partial-fit witness (the addiction headline)
    domain_restriction = {
        "INSTANT": {"axis": "instantaneous drive / excitability operating point", "reached_by_levers": True,
            "lever_axes_drawn_from": "L3 reward drive (OPRM1/OPRK1/DRD2/SLC6A3/CHRNA5) + L1 glutamatergic "
                    "plasticity substrate (GRIN2A/GRIN2B) + L2 inhibitory restore (GABRA2/GABRG3)",
            "sign": "DAMPEN / NORMALISE the sensitised reward drive and RESTORE inhibitory balance (the "
                    "naltrexone/varenicline/bupropion/acamprosate/topiramate DIRECTIONS) -- across L1/L2/L3; "
                    "this is the INSTANTANEOUS surface, reached"},
        "SG": {"axis": "consolidated sensitisation gain (the learned plastic trace -- the DOMINANT addiction fault)",
            "reached_by_levers": False,
            "named_genes": oor_by_axis.get("SG", []),
            "why_not": "the consolidated reward GAIN -- the LEARNED amplitude growth of the reward response "
                       "(deltaFosB accumulation, BDNF remodelling, the CREB tolerance/dependence programme, "
                       "ARC consolidation) -- is a PLASTICITY (E0-layer, sec.26) variable, NOT an "
                       "instantaneous fold. It is out of reach in two senses: it is a GAIN not a fold (the "
                       "ADHD lesson) AND it is CONSOLIDATED/LEARNED, so even the drive levers that dampen "
                       "the instantaneous response cannot ERASE the durable trace (that is the E0 dynamics "
                       "domain -- the convergence point). The threshold frame reaches it only INDIRECTLY. "
                       "Named genes: FOSB / BDNF / CREB1 / ARC (out_of_reach_targets)."},
        "reading": ("the lever frame reaches the INSTANTANEOUS drive/excitability operating point across all "
                    "three classes (L3 reward drive, L1 glutamate-plasticity substrate, L2 inhibitory "
                    "restore -- where the established addiction pharmacology acts). But the DOMINANT "
                    "addiction fault -- the SG consolidated sensitisation GAIN, the learned plastic trace "
                    "that drives chronicity and relapse -- sits on a DIFFERENT axis the threshold frame does "
                    "not reach (only indirectly), because it is a LEARNED / plastic (E0-layer) gain, not an "
                    "instantaneous fold. So the fit is PARTIAL [L]: the frame catches the instantaneous "
                    "reward drive but not the consolidated learned gain. Cites the sec.28 state-switching / "
                    "sec.26 E0 plasticity sensitisation substrate, and sec.35 (the ADHD partial-fit "
                    "precedent, whose gain-axis lesson addiction extends to a consolidated/plastic gain)."),
        "cites": "the sec.28 state-switching / sec.26 E0 plasticity incentive-sensitisation substrate (the "
                 "addiction model: repeated exposure consolidates a sensitised reward gain that persists "
                 "after withdrawal) + sec.35 adhd_threshold_levers (the named-out-of-reach gain-axis "
                 "precedent -- ADHD's gain was out of reach because a fold lever does not set a gain; "
                 "addiction's gain is moreover LEARNED/consolidated, so it is doubly out of reach)",
        "relation_to_adhd": [
            "ADHD was the first partial fit: its dominant GAIN-amplitude axis (synthesis/release) was out of reach because a drive-tone lever has NO handle on synthesis -- a fold does not set a gain",
            "addiction is the second partial fit: its dominant SG axis is also a GAIN out of reach (the ADHD lesson) AND moreover CONSOLIDATED/LEARNED -- a plasticity (E0-layer) variable, doubly out of reach",
            "TEXTURAL INVERSE of ADHD's emptiness: ADHD was L3-ONLY (L1/L2 EMPTY -- 'not a channelopathy'); addiction ENGAGES L1 and L2 too (richer reachable surface) yet is STILL partial -- the dominant fault is a consolidated plastic gain, not an instantaneous excitability",
            "THE CONVERGENCE: addiction's out-of-reach SG axis is precisely the E0 plasticity layer -- the point where threshold-leverisation (B-i) meets the dynamics route (B-ii). B-i NAMES the trace out-of-reach honestly.",
        ],
    }

    # the partial-fit witness (the headline grade)
    partial_fit = {
        "fit_grade": "[L] partial",
        "fit_index_in_series": 2,
        "reached_axis": "INSTANT (instantaneous drive/excitability) -- reached across L1/L2/L3",
        "out_of_reach_axis": "SG (consolidated sensitisation gain) -- the DOMINANT addiction fault, the learned plastic trace, reached only indirectly",
        "out_of_reach_reason": "a GAIN not a fold (the ADHD lesson) AND consolidated/LEARNED -- a plasticity (E0-layer) variable, not an instantaneous fold",
        "reasoning": ("addiction is a disorder of INCENTIVE SENSITISATION: repeated exposure TRAINS the "
                      "reward circuit (a plasticity process, the E0 layer) into a consolidated low-threshold "
                      "attractor whose reward GAIN has grown and persists after withdrawal. The "
                      "threshold-shift frame reaches the INSTANTANEOUS operating point richly -- the "
                      "up-stream reward DRIVE (L3), the glutamatergic plasticity SUBSTRATE (L1) and the "
                      "inhibitory-RESTORE arm (L2), where the established pharmacology acts -- but it does "
                      "NOT reach the DOMINANT fault, the SG consolidated sensitisation GAIN, because that "
                      "gain is a LEARNED / plastic (E0-layer) variable, not an instantaneous fold: a fold "
                      "lever does not set a gain (the ADHD lesson) and no drive lever ERASES a consolidated "
                      "trace. Hence the fit is PARTIAL [L], the SECOND non-clean fit, for a DEEPER reason "
                      "than ADHD -- and addiction is the point where threshold-leverisation meets the E0 "
                      "plasticity layer."),
        "contrast_to_prior_fits": ("bipolar (L1, clean [V]), epilepsy (L1+L2, clean [V]), depression "
                      "(L3-dominant, clean [V]), schizophrenia (L1+L3, clean [V] though domain-restricted), "
                      "autism (L1-dominant, clean [V] though domain-restricted with named O/W out-of-reach), "
                      "ADHD (L3-only, the FIRST PARTIAL [L] -- dominant gain-amplitude axis out of reach). "
                      "Addiction is the SECOND PARTIAL [L]: richer reachable surface than ADHD (it engages "
                      "L1 and L2, not just L3) but STILL partial, because its dominant axis is a "
                      "consolidated/LEARNED gain (a plasticity variable), not an instantaneous fold."),
        "honest": ("the partial grade is the finding, not a failure: it marks exactly where the "
                   "cross-cutting threshold-shift logic does and does not apply, and refuses to overclaim a "
                   "clean fit where the dominant fault is a consolidated plastic trace. efficacy=0; no "
                   "drug/dose/patient; no route to obtain or use any substance; no claim that addiction is "
                   "cured; addiction is a treatable medical condition, not a failure of will."),
    }

    return {
        "title": "Reward-drive addiction target map for the INSTANTANEOUS drive/excitability axis -- the "
                 "sec.28/E0 incentive-sensitisation substrate mapped onto the formal L1/L2/L3 inheritance "
                 "frame (engine-generated reads + cited lever frame); the consolidated sensitisation-gain "
                 "(SG) axis named as out-of-reach (a learned plastic trace -- the E0 layer); the SECOND "
                 "PARTIAL [L] fit in the series and the convergence point of the two routes",
        "inherited_from": ("analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the "
                          "threshold-shift intervention-logic technology, applied to the addiction "
                          "INSTANTANEOUS drive/excitability axis (SEVENTH application after bipolar sec.30, "
                          "epilepsy sec.31, depression sec.32, schizophrenia sec.33, autism sec.34 and ADHD "
                          "sec.35; this one is the SECOND PARTIAL [L] fit -- addiction's dominant fault is a "
                          "consolidated/LEARNED sensitisation gain, so the frame reaches its instantaneous "
                          "drive surface but not its dominant plastic-gain axis -- and it is the CONVERGENCE "
                          "point where threshold-leverisation meets the E0 plasticity layer)"),
        "maps_addiction_substrate": ("the sec.28 state-switching / sec.26 E0 plasticity incentive-"
                          "sensitisation model establishes addiction as a CONSOLIDATED low-threshold reward "
                          "attractor: repeated drug/cue exposure TRAINS the reward circuit (a plasticity "
                          "process) into a sensitised state whose reward GAIN has grown and persists after "
                          "withdrawal (relapse, cue-reactivity, extinction not returning the trace to zero). "
                          "This map re-cuts that substrate by threshold-frame REACHABILITY -- the up-stream "
                          "reward DRIVE (L3, dominant), the glutamatergic plasticity SUBSTRATE (L1) and the "
                          "inhibitory-RESTORE arm (L2) are the reachable lever surface; the CONSOLIDATED "
                          "sensitisation GAIN (the SG axis) is out of reach -- adding NO new mechanism and "
                          "NO new constant."),
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_e0": ("sec.26 (the E0 plasticity layer) and sec.28 (state-switching) established the "
                          "addiction substrate: a sensitised reward gain CONSOLIDATED by plasticity. This "
                          "map DECOMPOSES the threshold-frame engagement: the INSTANTANEOUS drive/"
                          "excitability axis is reached by the L1/L2/L3 levers (the reward-drive, "
                          "glutamate-substrate and inhibitory-restore surfaces) while the SG (consolidated "
                          "sensitisation-gain) axis is NAMED out-of-reach (the deltaFosB/BDNF/CREB/ARC "
                          "plasticity trace). It re-derives no rule and adds no constant -- the addiction "
                          "counterpart of the sec.35 ADHD partial-fit, but with a consolidated/PLASTIC "
                          "dominant axis (the second partial fit, and the route-convergence point)."),
        "domain_restriction_witness": domain_restriction,
        "partial_fit_witness": partial_fit,
        "disorder_level_sign": ("the INSTANT axis is the instantaneous reward-drive / excitability "
                           "operating point; its corrective sign is DAMPEN / NORMALISE the sensitised "
                           "reward drive and RESTORE inhibitory balance (the naltrexone/varenicline/"
                           "bupropion/acamprosate/topiramate DIRECTIONS) -- across L1/L2/L3. But the sign "
                           "is PARTIAL: it reaches the INSTANTANEOUS surface only; the DOMINANT SG "
                           "(consolidated sensitisation-gain) axis is out of reach (a learned plastic "
                           "trace, not an instantaneous fold). So unlike the clean fold-moving sign of the "
                           "five clean-fit disorders, addiction's engagement with the threshold frame is "
                           "partial [L] -- the instantaneous drive is reachable, the consolidated gain is "
                           "not (it is the E0 layer's variable)."),
        "unifying_frame": ("the addiction operating point is a CONSOLIDATED sensitised reward attractor: the "
                           "reward gain has been TRAINED upward by plasticity (the E0 layer) and persists. "
                           "The threshold-shift frame reaches it through the INSTANTANEOUS drive/excitability "
                           "levers -- L3 the up-stream reward DRIVE (mu/kappa-opioid, D2, DAT, nAChR, the "
                           "dominant class where the established pharmacology lives), L1 the glutamatergic "
                           "plasticity SUBSTRATE (NMDA NR2A/NR2B) and L2 the inhibitory-RESTORE arm (GABA-A "
                           "a2/g3). The map reaches the INSTANT axis; the SG (consolidated sensitisation-"
                           "gain) axis -- the DOMINANT fault, the learned plastic trace deltaFosB/BDNF/CREB/"
                           "ARC -- is honestly out of reach (named in out_of_reach_targets), because it is a "
                           "gain not a fold AND a consolidated/learned (E0-layer) variable. The fit is "
                           "PARTIAL [L]: the second non-clean fit, for a deeper reason than ADHD, and the "
                           "point where threshold-leverisation meets the plasticity layer."),
        "levers": LEVER_FRAME,
        "lever_distribution_witness": {
            "counts": counts,
            "dominant_levers": dominant_levers,
            "codominant": codominant,
            "l3_dominant": bool(counts.get("L3", 0) == top and "L3" in dominant_levers and not codominant),
            "l1_present": bool(l1_present),
            "l2_present": bool(l2_present),
            "l3_only": bool(counts.get("L3", 0) == sum(counts.values()) and counts.get("L3", 0) > 0),
            "reading": (("addiction is L3-DOMINANT WITH L1 AND L2 BOTH PRESENT (L3=%d reward-drive levers; "
                         "L1=%d glutamate-plasticity-substrate; L2=%d inhibitory-restore) -- the SEVENTH "
                         "distribution pattern: bipolar leaned on L1 (calcium), epilepsy on L1+L2 (the "
                         "M-current), depression on L3 (HPA/monoamine, with a reachable L1/L2 mix), "
                         "schizophrenia on L1+L3 co-dominant (glutamate + dopamine), autism on L1-dominant "
                         "with a sparse L3, and ADHD on L3-ONLY (L1/L2 EMPTY). Addiction loads MOST on L3 "
                         "(the up-stream reward drive) but ENGAGES the ionic levers too -- the TEXTURAL "
                         "INVERSE of ADHD's emptiness (ADHD was 'not a channelopathy'; addiction engages "
                         "L1/L2), yet STILL partial because its DOMINANT fault is the consolidated "
                         "sensitisation gain, a learned plastic trace, not an instantaneous excitability "
                         "the levers can move." %
                         (counts.get("L3", 0), counts.get("L1", 0), counts.get("L2", 0)))),
        },
        "out_of_reach_targets": {
            "_what": "the SG-axis (consolidated sensitisation-gain) genes a threshold/drive lever CANNOT "
                     "reach -- named to make the addiction partial-fit CONCRETE. Each carries a gamma read "
                     "(its own promoter switch stiffness) ALONGSIDE, but is explicitly NOT a lever: the "
                     "consolidated reward GAIN (deltaFosB accumulation, BDNF remodelling, the CREB "
                     "tolerance/dependence programme, ARC consolidation) is a LEARNED / plastic (E0-layer, "
                     "sec.26) variable, not an instantaneous fold, so the threshold frame has no direct "
                     "handle. This is the DOMINANT addiction fault -- the relapse driver -- which is "
                     "exactly why addiction is a PARTIAL fit (the dominant axis is the out-of-reach one). "
                     "It extends the ADHD named-out-of-reach gain-axis discipline (sec.35) to a "
                     "consolidated/PLASTIC gain, and the SG axis is precisely the E0 dynamics domain (the "
                     "convergence point).",
            "by_axis": oor_by_axis,
            "n": len(oor),
            "entries": oor,
        },
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a receptor occupancy, not a "
                     "synaptic dopamine/opioid level, not a potency, not a dose, not in-vivo selectivity, "
                     "not a clinical effect, and NOT the consolidated sensitisation GAIN (the learned "
                     "reward-circuit amplitude / the deltaFosB trace) (those are [O]). The promoter |h_sp| "
                     "is the gene's OWN switch stiffness, carried alongside, never folded into a clinical "
                     "magnitude or equated with the consolidated sensitisation gain. gamma is blind to "
                     "on/off and to expression level. L3 (the reward-drive) mechanism link is [O] -- the "
                     "read places the gene, it does not derive the drive mechanism. The fit is PARTIAL [L]: "
                     "the frame reaches the INSTANTANEOUS drive/excitability axis (L1/L2/L3) but not the "
                     "DOMINANT SG consolidated sensitisation-gain axis, which is a learned/plastic (E0) "
                     "variable, not a fold."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never "
                    "drugs, doses, protocols, or patients; addiction is polygenic and heterogeneous and its "
                    "established pharmacology is only PARTIALLY effective (high relapse), and a lever "
                    "direction is a mechanism boundary, NOT a route to obtain or use any substance, NOT a "
                    "claim that addiction can be cured, and NOT a moral judgement -- addiction is a "
                    "treatable medical condition, not a failure of will (the fail-closed forbidden-claim "
                    "scan enforces this, incl. drug-seeking/misuse and cure-miracle classes); the map "
                    "reaches the INSTANTANEOUS drive/excitability axis across L1/L2/L3, while the DOMINANT "
                    "SG consolidated sensitisation-gain axis is out of reach (named here -- a learned "
                    "plastic trace, the E0 layer), so the fit is PARTIAL [L], the second non-clean fit and "
                    "the route-convergence point; a lever direction is a mechanism boundary, not a claim "
                    "about identity or the subjective world (Axis-A; consciousness_claim=0; hard problem "
                    "OPEN)."),
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

def addiction_threshold_levers_results():
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
        "maps_e0_sensitisation_substrate": True,
        "second_partial_fit_L": True,
    }
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "maps_e0_sensitisation_substrate": 1.0,
        "l3_mechanism_link": "OPEN [O] -- the reward/incentive (opioid/dopamine/nicotinic) signalling mechanism is cited biology, not derived",
        "promoter_hsp_vs_sensitisation_gain": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the consolidated sensitisation gain (the deltaFosB trace)",
        "partial_fit_L": 1.0,
        "fit_grade": "[L] partial -- the DOMINANT SG consolidated sensitisation-gain axis is out of reach (a learned/plastic E0-layer variable, not a fold); only the INSTANTANEOUS drive/excitability axis is reached",
        "second_partial_fit_in_series": 1.0,
        "l3_dominant_l1_l2_present": 1.0,
        "sensitisation_gain_axis_named_out_of_reach": 1.0,
        "convergence_with_e0_plasticity_layer": 1.0,
        "no_drug_seeking_or_cure_licence": 1.0,
        "addiction_is_treatable_not_a_moral_failing": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this, incl. "
                             "drug-seeking/misuse and cure-miracle classes)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "addiction_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_addiction_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"addiction_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = addiction_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 100)
    print("ADD-T-L  ADDICTION REWARD-DRIVE MAP  (inherited from analgesic v2.0; engine READ-ONLY; L3-dominant+L1/L2; PARTIAL fit [L] #2)")
    print("=" * 100)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  maps E0 substrate     : {inv['maps_e0_sensitisation_substrate']}   second partial fit [L]: {inv['second_partial_fit_L']}")
    print("-" * 100)
    print(f"  {'gene':9} {'lev':4} {'gamma':>7} {'|h_sp|':>8} {'protein':40} axis role")
    for e in res["entries"]:
        cp = e.get("protein") or e["channel"] or "-"
        print(f"  {e['gene']:9} {e['lever']:4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} "
              f"{cp[:40]:40} {e['axis_role'][:26]}")
    print("-" * 100)
    print("  OUT-OF-REACH (consolidated sensitisation-gain axis; named; NOT levers):")
    for e in res["out_of_reach_targets"]["entries"]:
        print(f"  {e['gene']:9} {'--':4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {e['fault_axis']:5} "
              f"{(e['role'])[:46]:46}")
    print("-" * 100)
    w = res["lever_distribution_witness"]
    print("  targets by lever: " + ", ".join(f"{k}={v}" for k, v in w["counts"].items())
          + f"   -> {'DOMINANT ' + w['dominant_levers'][0]}  (L3-dominant={w['l3_dominant']}, L1 present={w['l1_present']}, L2 present={w['l2_present']})")
    dr = res["domain_restriction_witness"]
    print(f"  domain reach: INSTANT={dr['INSTANT']['reached_by_levers']} "
          f"SG={dr['SG']['reached_by_levers']}  (INSTANT axis reached; SG named out-of-reach)")
    pf = res["partial_fit_witness"]
    print(f"  FIT GRADE: {pf['fit_grade']}  (#{pf['fit_index_in_series']} in series; reached={pf['reached_axis'][:18]}; out-of-reach=SG consolidated gain)")
    print(f"  n_targets: {res['n_targets']}   out_of_reach: {res['n_out_of_reach']}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 100)
    ok = (inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
          and not w["codominant"] and w["dominant_levers"] == ["L3"] and w["l3_dominant"]
          and w["l1_present"] and w["l2_present"] and (w["l3_only"] is False)
          and dr["SG"]["reached_by_levers"] is False and dr["INSTANT"]["reached_by_levers"] is True
          and pf["fit_grade"] == "[L] partial")
    print("  ADD-T-L REWARD-DRIVE MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
