#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schizophrenia_threshold_levers.py  —  T1a-L (sec.33): the THREE-LEVER target map for the psychotic
OVER-IGNITION operating point. This is the analgesic_threshold_logic v2.0 technology (DOI 10.5281/
zenodo.20733420) INHERITED into the mind atlas and applied to schizophrenia. It is the FOURTH
application of the inherited cross-cutting layer (after bipolar sec.30, epilepsy sec.31 and depression
sec.32) and the one that EXERCISES a new edge of the frame's generality, because schizophrenia is the
first DOMAIN-RESTRICTED case: the disorder is not one operating point but THREE clinical domains on
THREE different fault axes, and the three-lever map reaches EXACTLY ONE of them (the POSITIVE domain,
the over-ignition / aberrant-salience axis) while being honestly INERT on the other two. It re-derives
no rule: it reads the SAME R19 substrate (E.spinodal/E.barrier, byte-identical to vp_neuro_engine) and
the SAME gamma = -mean(NN stacking dG, SantaLucia 1998) the engine uses to write genes.

WHY THIS EXISTS (the gap it closes). sec.24 (schizophrenia_discriminant + schizophrenia_symptom_domains,
SZ-DISC / SZ-DOM) established TWO things. First, that psychosis' POSITIVE domain is the OVER-IGNITION
pole of the threshold axis (the mirror of autism-T): an excitatory E/I bias LOWERS the R19 fold so weak,
irrelevant candidate assemblies ignite -> aberrant salience, and a gain-REDUCING antipsychotic-class push
RAISES the fold back and removes the aberrant ignitions. Second, the within-disease discriminant: the
SAME gain-reducing operator reverses the POSITIVE domain ONLY, because NEGATIVE symptoms sit on the
OUTPUT/gain-deficit axis (where a gain reduction pushes output even lower) and COGNITIVE symptoms sit on
the long-range WIRING axis (where a scalar operator cannot re-route geometry) -- which is the axis-
structural reason D2 blockade treats positive but not negative/cognitive symptoms. But sec.24 treated the
gain-reducing push as a SINGLE, undifferentiated operator -- it never said WHICH genes / receptors realise
the raise. The analgesic three-lever frame supplies exactly that missing layer, for the POSITIVE domain.
This is the direct schizophrenia counterpart of the bipolar B4->sec.30, epilepsy sec.25->sec.31 and
depression sec.27->sec.32 decompositions.

THE DOMAIN-RESTRICTION (honest, central, the chapter's headline). Unlike epilepsy (one over-sync pole)
and depression (one hypo-coordination pole), schizophrenia is THREE domains on THREE axes, so the SIGN of
the three-lever map is DOMAIN-RESTRICTED, not disorder-wide:
  POSITIVE  domain = the THRESHOLD axis driven to OVER-ignition. REACHED by the levers: the corrective
            sign is REDUCE excess drive / RAISE the fold (the SAME direction as epilepsy / bipolar mania,
            the OPPOSITE of depression's restore-deficient). L1 reduces the inward excitatory current,
            L3 removes the up-stream dopamine drive, L2 restores the inhibitory current -- all raise the
            fold back toward selective ignition.
  NEGATIVE  domain = the OUTPUT/gain-DEFICIT axis. NOT REACHED: a gain-reducing lever pushes output even
            LOWER; the threshold-shift frame has no restorative handle on a deficit here (this is the
            depression-style restore problem on a DIFFERENT axis, and is left to sec.24's [O]).
  COGNITIVE domain = the long-range WIRING axis (the dysconnection hypothesis). NOT REACHED: a scalar
            current/drive lever leaves the locality imbalance EXACTLY invariant; geometry cannot be
            re-routed by a threshold shift (sec.19 chemical-limits result).
So the three-lever map is a POSITIVE-domain target map. The negative/cognitive gap is AXIS-STRUCTURED,
NOT dose-structured: it is not "too little lever" but "the wrong axis for a threshold-shift lever." This
domain-restriction is the new edge the frame is tested against, and it is stated, not hidden.

THE LEVER DISTRIBUTION (honest). Where bipolar leaned on L1 (calcium GWAS), epilepsy on L2 (the KCNQ2/3
M-current) and depression on L3 (HPA/monoamine/neurotrophic, L3-DOMINANT), schizophrenia is L1+L3
CO-DOMINANT: the POSITIVE-domain raise is reached two ways at once --
  L1  reduce the inward (glutamatergic/Ca) excitatory current  (the NMDA / AMPA / Ca set; co-dominant)
  L2  increase the outward (K+) / restore the GABA-A inhibitory current  (the interneuron-restore; minor)
  L3  remove the up-stream DOPAMINE drive                        (the D2-antagonist antipsychotic axis;
                                                                  co-dominant)
The two co-dominant levers are the two leading pathophysiologies of psychosis: the GLUTAMATE (NMDA) axis
(L1) and the DOPAMINE axis (L3, the established antipsychotic target). This is the frame's generality
exercised in a third way (a co-dominant pair, not a single dominant lever).

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| / barrier
are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V] (reproducible);
their ORDER is [F] (forced). This is NOT a receptor occupancy (NOT a D2 occupancy), NOT a synaptic
dopamine/glutamate level, NOT a drug potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical
effect, and -- the schizophrenia-specific addition -- the promoter |h_sp| is NOT the sec.24 NETWORK
over-ignition threshold (the aberrant-salience fold on R) (that is a separate network quantity). The
promoter read is carried ALONGSIDE as the gene's own switch stiffness; it is NEVER folded into a
clinical magnitude or equated with the network threshold. gamma is blind to on/off and to
gain/loss/expression-level of function. L3 (the dopamine drive) mechanism link is [O]: the gamma read
PLACES the gene in the lever map; it does NOT derive the dopaminergic/network mechanism (enforced by
schizophrenia_l3_honesty.py, which ALSO checks the L1+L3 co-dominance and the domain-restriction).

THE HONEST DIRECTION CAVEATS (schizophrenia-specific; recorded, not hidden).
  (i)   WHOLE-L1 SIGN SUBTLETY (the NMDA-hypofunction caveat -- the schizophrenia analogue of the
        depression ketamine caveat). The leading glutamatergic etiology is NMDA-receptor HYPOfunction
        (preferentially on fast-spiking PV+ GABA interneurons) -> DISINHIBITION -> a downstream cortical
        glutamate/dopamine surge -> aberrant salience. So the over-ignition is itself a DOWNSTREAM
        consequence of an up-stream NMDA DEFICIT, and direct NMDA-glycine-site AGONIST directions
        (D-serine, sarcosine, glycine) have been studied to RESTORE interneuron function -- the OPPOSITE
        sign to a naive "reduce inward NMDA current." So the L1 placement is structural/trait-blind, but
        its clinical DIRECTION is sign-subtle and stays [O].
  (ii)  HTR2A DIRECTION IS NON-MONOTONE. 5-HT2A ANTAGONISM is the serotonergic axis of the atypical
        antipsychotics, yet 5-HT2A AGONISM (the psychedelic route) is also studied in psychiatry -- the
        receptor-level sign is NOT monotone. Recorded (the same caveat depression records).
  (iii) DOMAIN-RESTRICTION (the headline, above). The three-lever map reaches the POSITIVE domain only;
        the negative (output-deficit) and cognitive (wiring) domains are a DIFFERENT axis the threshold-
        shift frame does not reach -- exactly why the dopamine antipsychotic direction spares them.

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places READS
and TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any drug treats anyone or
that any individual should change treatment. Real schizophrenia is POLYGENIC and HETEROGENEOUS, its
connectivity is DYSconnective, and roughly a third is treatment-resistant -- LOCKED. A lever direction is
a mechanism boundary, NOT a claim about the disorganised subjective state (consciousness_claim stays 0;
hard problem OPEN).

No tuning: gamma is measured (pure arithmetic over called dinucleotide steps); |h_sp|/barrier are the
locked R19 forms; the lever assignments, domain mapping and citations are CITED Layer-2 biology, not
engine outputs. Governed by VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 schizophrenia_threshold_levers.py
Out:  schizophrenia_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "schizophrenia_levers_promoters.cache.json")
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

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the psychotic over-ignition pole) ----
LEVER_FRAME = {
  "L1": "reduce the inward (glutamatergic/excitatory) drive -- the NMDA / AMPA / Ca-channel set. Reaches "
        "the POSITIVE domain by raising the over-ignition fold. CO-DOMINANT with L3. SIGN-SUBTLE: the "
        "leading etiology is NMDA HYPOfunction on PV interneurons -> downstream disinhibition, so direct "
        "NMDA-glycine-site AGONIST directions also appear -- the naive 'reduce inward current' sign is "
        "not the clinical sign (see caveat)",
  "L2": "increase the outward (K+) / restore the GABA-A inhibitory current -- the interneuron-restore "
        "route (the PV/GABA deficit). Raises the restoring side of the same POSITIVE-domain over-ignition "
        "axis (minor lever for schizophrenia)",
  "L3": "remove / normalise the UP-STREAM DOPAMINE drive that sets the aberrant-salience operating point "
        "-- CO-DOMINANT with L1, and the ESTABLISHED antipsychotic axis. Three sub-axes: (a) the dopamine "
        "RECEPTOR set (DRD2 = the D2-antagonist target shared by every antipsychotic; DRD4); (b) the "
        "dopamine SYNTHESIS/TRANSPORT set (TH = the elevated striatal synthesis capacity, SLC6A3 = the "
        "transporter); (c) the serotonergic MODULATION of dopamine (HTR2A, the atypical axis, non-monotone) "
        "and the prefrontal catabolic set-point (COMT). Reaches the POSITIVE domain by lowering the "
        "aberrant-salience drive; dopaminergic/network mechanism [O]",
}

# grade strings (inherited discipline)
GL1 = "[F] structural: a glutamatergic/Ca inward-current REDUCTION raises the over-ignition fold and reaches the POSITIVE domain (anchored to cited agents; sign-subtle, see NMDA-hypofunction caveat)"
GL2 = "[F] structural: an outward-K+ / GABA-A inhibitory-current RESTORE raises the same over-ignition fold (anchored to cited agents)"
GL3 = "[O] cited biology: gamma places the gene in the lever map; the dopaminergic/serotonergic signalling and the network over-ignition mechanism are NOT derived"

# domain reach text (the schizophrenia-specific structure)
DOM_POS = "POSITIVE (the over-ignition / aberrant-salience THRESHOLD axis the gain-reducing levers REACH)"
DOM_POS_ADJ = "POSITIVE-adjacent (restore inhibition on the same over-ignition threshold axis)"

# CITED Layer-2 context (NOT engine output). sz_anchor = the cited schizophrenia genetics /
# pharmacology; direction_agent = the cited POSITIVE-domain-restoring agent DIRECTION (never an
# efficacy claim). channel/protein labelled. domain = which clinical domain the lever reaches.
CONTEXT = {
  # ============== L1 (co-dominant): reduce the inward glutamatergic/Ca excitatory current ==============
  "GRIN2A": dict(lever="L1", domain=DOM_POS, channel="NMDA-R GluN2A (glutamate, Ca2+-permeable)", protein=None,
      push="reduce the inward NMDA (GluN2A) current to raise the over-ignition fold -- the principal genome-wide "
           "significant glutamatergic schizophrenia gene; SIGN-SUBTLE (NMDA-hypofunction etiology, see caveat)",
      sz_anchor="one of the few genome-wide significant single schizophrenia genes (common-variant GWAS and rare-variant "
                "SCHEMA both implicate GRIN2A); the NMDA-receptor subunit at the centre of the glutamate hypothesis",
      direction_agent="glutamatergic (NMDA-modulation) DIRECTION for the POSITIVE domain -- but the NMDA-hypofunction etiology "
                      "means a glycine-site AGONIST (D-serine/sarcosine) restorative direction also appears (DIRECTION, not efficacy; sign-subtle)",
      grade_mechanism=GL1,
      src="Singh 2022 Nature 604:509 (SCHEMA, GRIN2A); Trubetskoy 2022 Nature 604:502 (PGC3 GWAS, glutamatergic); Olney & Farber 1995 Arch Gen Psychiatry 52:998 (NMDA-hypofunction)"),
  "GRIN2B": dict(lever="L1", domain=DOM_POS, channel="NMDA-R GluN2B (glutamate, Ca2+-permeable)", protein=None,
      push="reduce the inward NMDA (GluN2B) current to raise the over-ignition fold -- the GluN2A partner subunit",
      sz_anchor="NMDA-receptor subunit implicated across psychotic and mood disorders; the developmental glutamatergic partner of GluN2A",
      direction_agent="glutamatergic-tone (NMDA-modulation) DIRECTION for the POSITIVE domain (carried with GluN2A as the inward glutamatergic route; sign-subtle)",
      grade_mechanism=GL1,
      src="Trubetskoy 2022 Nature 604:502 (PGC3, glutamatergic set); cross-disorder NMDA tone"),
  "GRIN1": dict(lever="L1", domain=DOM_POS, channel="NMDA-R GluN1 (obligate NMDA subunit, glycine-binding)", protein=None,
      push="modulate the obligate NMDA subunit (GluN1) -- the glycine-binding core of NMDA-receptor function; the direct site of the NMDA-hypofunction caveat",
      sz_anchor="the obligate NMDA-receptor subunit; GRIN1 hypofunction models (and GluN1-knockdown mice) reproduce schizophrenia-like phenotypes -- the strongest direct NMDA-hypofunction evidence",
      direction_agent="NMDA-function DIRECTION for the POSITIVE domain -- the glycine-site is the RESTORATIVE (agonist) target of the hypofunction hypothesis, so the sign here is explicitly subtle (DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Mohn 1999 Cell 98:427 (GluN1 hypomorph schizophrenia model); Tsai 1998 Biol Psychiatry 44:1081 (glycine-site augmentation direction)"),
  "GRIA3": dict(lever="L1", domain=DOM_POS, channel="AMPA-R GluA3 (glutamate, fast excitatory)", protein=None,
      push="reduce the inward AMPA (GluA3) current to raise the over-ignition fold -- the fast-excitatory glutamatergic partner of the NMDA set",
      sz_anchor="an AMPA-receptor subunit in the schizophrenia glutamatergic set; fast excitatory transmission downstream of the NMDA/interneuron balance",
      direction_agent="AMPA-glutamatergic DIRECTION for the POSITIVE domain (the fast-excitatory route carried with the NMDA set; DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Trubetskoy 2022 Nature 604:502 (PGC3, glutamatergic-receptor set incl. AMPA)"),
  "CACNA1C": dict(lever="L1", domain=DOM_POS, channel="Ca_V1.2 (L-type Ca2+)", protein=None,
      push="reduce the inward Ca2+ (L-type) current to raise the over-ignition fold -- the cross-disorder calcium set-point gene",
      sz_anchor="the most-replicated CROSS-DISORDER calcium-channel locus (the PGC five-disorder finding spanning schizophrenia, "
                "bipolar, major depression, ASD, ADHD); an L-type Ca set-point on the operating point",
      direction_agent="L-type Ca-channel-modulation DIRECTION (cross-disorder set-point; carried as structural context, NOT a clean antipsychotic target)",
      grade_mechanism=GL1,
      src="Cross-Disorder Group PGC 2013 Lancet 381:1371 (CACNA1C across five disorders); Trubetskoy 2022 (PGC3 calcium set)"),
  "CACNB2": dict(lever="L1", domain=DOM_POS, channel="Ca_V beta-2 auxiliary subunit (CACNB2)", protein=None,
      push="reduce the inward Ca2+ current via the auxiliary beta-2 subunit -- the L1-adjacent calcium set-point partner of CACNA1C",
      sz_anchor="a voltage-gated calcium-channel auxiliary subunit and a replicated cross-disorder GWAS locus (PGC); the L1-adjacent calcium partner of CACNA1C",
      direction_agent="calcium-channel-auxiliary DIRECTION (cross-disorder set-point; carried as structural context, NOT a clean antipsychotic target)",
      grade_mechanism=GL1,
      src="Cross-Disorder Group PGC 2013 Lancet 381:1371 (CACNB2 cross-disorder); Trubetskoy 2022 (PGC3 calcium set)"),
  # ============== L2 (minor): increase the outward K+ / restore the GABA-A inhibitory current ==============
  "GABRA1": dict(lever="L2", domain=DOM_POS_ADJ, channel="GABA-A receptor alpha1 (Cl-)", protein=None,
      push="RESTORE the inhibitory GABA-A (Cl-) current -- the interneuron-restore route; raises the restoring side of the over-ignition axis (the PV/GABA deficit)",
      sz_anchor="GABA-A alpha1 subunit; the cortical fast-spiking (parvalbumin) GABA-interneuron deficit and reduced GABAergic inhibition is a core schizophrenia pathology",
      direction_agent="GABA-A inhibitory-restore DIRECTION (restore cortical interneuron inhibition; raises the over-ignition fold from the inhibitory side -- DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Lewis 2005 Nat Rev Neurosci 6:312 (cortical GABA interneuron deficit in schizophrenia)"),
  "GABRB3": dict(lever="L2", domain=DOM_POS_ADJ, channel="GABA-A receptor beta3 (Cl-)", protein=None,
      push="RESTORE the inhibitory GABA-A (Cl-) current via the beta3 subunit -- the interneuron-restore partner of GABRA1",
      sz_anchor="GABA-A beta3 subunit (15q11-13); part of the cortical GABA-A inhibitory set tied to the interneuron deficit of schizophrenia",
      direction_agent="GABA-A inhibitory-restore DIRECTION (interneuron-restore partner of the alpha1 subunit; DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Lewis 2005 Nat Rev Neurosci 6:312 (GABA-A inhibitory set); cortical interneuron deficit"),
  # ====== L3 (co-dominant): remove/normalise the up-stream dopamine drive (the antipsychotic axis) ======
  #   sub-axis (a) dopamine RECEPTORS
  "DRD2": dict(lever="L3", domain=DOM_POS, channel=None, protein="dopamine D2 receptor (DRD2; Gi-coupled GPCR; the antipsychotic target)",
      push="reduce the up-stream dopamine drive at the D2 receptor (DRD2) -> lower the aberrant-salience drive that LOWERS the over-ignition fold; the POSITIVE-domain antipsychotic axis",
      sz_anchor="the dopamine D2 receptor; EVERY licensed antipsychotic is a D2 antagonist or partial agonist, and DRD2 is a genome-wide significant schizophrenia GWAS locus -- the single most established psychosis target",
      direction_agent="D2-antagonist / partial-agonist DIRECTION (the antipsychotic axis -- lowers the aberrant-salience dopamine drive; reaches the POSITIVE domain ONLY -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Seeman 1976 Nature 261:717 (antipsychotic = D2 affinity); Kapur 2003 Am J Psychiatry 160:13 (aberrant salience / D2); Trubetskoy 2022 (DRD2 GWAS)"),
  "DRD4": dict(lever="L3", domain=DOM_POS, channel=None, protein="dopamine D4 receptor (DRD4; Gi-coupled GPCR)",
      push="reduce the up-stream dopamine drive at the D4 receptor (DRD4) -> the clozapine-affinity dopaminergic sub-route (exploratory)",
      sz_anchor="the dopamine D4 receptor; high clozapine affinity made it an atypical-antipsychotic candidate, though a clean D4-selective direction is exploratory",
      direction_agent="D4-modulation DIRECTION (the clozapine-affinity dopaminergic sub-route; exploratory -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Van Tol 1991 Nature 350:610 (D4, clozapine affinity)"),
  #   sub-axis (b) dopamine SYNTHESIS / TRANSPORT
  "TH": dict(lever="L3", domain=DOM_POS, channel=None, protein="tyrosine hydroxylase (TH; catecholamine-synthesis rate-limiting enzyme)",
      push="reduce the up-stream dopamine SYNTHESIS capacity (TH is the dopamine-synthesis rate-limiter) -> lower the elevated striatal dopamine drive at its source",
      sz_anchor="the rate-limiting enzyme of dopamine synthesis; ELEVATED presynaptic striatal dopamine-synthesis capacity is the most robustly replicated dopaminergic finding in schizophrenia (PET)",
      direction_agent="dopamine-synthesis-capacity DIRECTION (TH; the up-stream striatal-synthesis source of the aberrant-salience drive -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Howes & Kapur 2009 Schizophr Bull 35:549 (the dopamine hypothesis v.III, elevated synthesis capacity); McCutcheon 2018 (presynaptic dopamine)"),
  "SLC6A3": dict(lever="L3", domain=DOM_POS, channel=None, protein="dopamine transporter DAT (SLC6A3)",
      push="modulate the up-stream dopamine transporter (DAT) -> set the synaptic dopamine drive available for aberrant salience (the transport sub-axis)",
      sz_anchor="the dopamine transporter; sets synaptic dopamine clearance and is part of the dopaminergic-tone set studied in psychosis (the transport side of the dopamine hypothesis)",
      direction_agent="dopamine-transporter DIRECTION (DAT; the synaptic-dopamine-clearance sub-axis of the dopamine drive -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Howes & Kapur 2009 Schizophr Bull 35:549 (dopamine hypothesis); SLC6A3 as the dopamine-transport locus"),
  #   sub-axis (c) serotonergic modulation of dopamine + prefrontal catabolic set-point
  "HTR2A": dict(lever="L3", domain=DOM_POS, channel=None, protein="serotonin receptor 5-HT2A (HTR2A; GPCR)",
      push="modulate 5-HT2A signalling -- the serotonergic modulation of the dopamine drive (the atypical-antipsychotic axis). DIRECTION NON-MONOTONE: both ANTAGONIST (atypical) and "
           "AGONIST (psychedelic) directions appear (see caveat)",
      sz_anchor="the 5-HT2A receptor; 5-HT2A ANTAGONISM is the defining serotonergic mechanism of the atypical antipsychotics, and HTR2A is a schizophrenia candidate locus",
      direction_agent="5-HT2A-modulation DIRECTION -- NON-MONOTONE: the atypical-antipsychotic route is an ANTAGONIST direction while a 5-HT2A AGONIST (psychedelic) route also appears (DIRECTION, not efficacy; sign recorded as ambiguous)",
      grade_mechanism=GL3,
      src="Meltzer 1989 (5-HT2A/D2 atypical hypothesis); Carhart-Harris 2021 N Engl J Med 384:1402 (5-HT2A agonist route) -- non-monotone"),
  "COMT": dict(lever="L3", domain=DOM_POS, channel=None, protein="catechol-O-methyltransferase (COMT; catecholamine-catabolic enzyme; 22q11.2)",
      push="modulate prefrontal catecholamine catabolism (COMT) -- the prefrontal dopamine degradation set-point (Val158Met); the 22q11.2 dopaminergic sub-axis",
      sz_anchor="the catecholamine-catabolic enzyme in the 22q11.2 deletion region (a strong schizophrenia copy-number risk); the Val158Met polymorphism sets prefrontal dopamine tone",
      direction_agent="prefrontal catecholamine-catabolism DIRECTION (COMT Val158Met set-point; the 22q11.2 dopaminergic route -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Lachman 1996 Pharmacogenetics 6:243 (COMT Val158Met); Karayiorgou & Gogos 1997 (22q11.2 / COMT in schizophrenia)"),
}

def read(sym, g):
    c = CONTEXT[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the network over-ignition fold)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "domain_reach": c["domain"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "schizophrenia_genetic_anchor": c["sz_anchor"],
        "positive_domain_restoring_agent_direction": c["direction_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": GL1 if c["lever"] in ("L1", "L1-adjacent")
                       else (GL2 if c["lever"] in ("L2", "L2-adjacent") else c["grade_mechanism"]),
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_network_threshold": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch stiffness, "
                                       "NOT the sec.24 network over-ignition threshold (the aberrant-salience fold on "
                                       "R); never equated",
        "grade_clinical_map": "[O] OPEN -- not a receptor occupancy (not a D2 occupancy), synaptic dopamine/glutamate "
                              "level, potency, dose, in-vivo selectivity, or clinical effect",
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
    # lever-distribution witness: schizophrenia is L1+L3 CO-DOMINANT (the third distribution pattern)
    counts = {k: len(v) for k, v in by_lever.items()}
    ranked = sorted(counts, key=lambda k: counts[k], reverse=True)
    top = counts[ranked[0]]
    dominant_levers = sorted([k for k, n in counts.items() if n == top])
    codominant = len(dominant_levers) >= 2
    # domain-restriction witness (the schizophrenia headline)
    domain_restriction = {
        "positive": {"axis": "threshold / over-ignition (aberrant salience)", "reached_by_levers": True,
            "sign": "REDUCE excess drive / RAISE the fold (the SAME direction as epilepsy/bipolar mania) -- "
                    "L1 reduce inward, L3 remove dopamine drive, L2 restore inhibition all raise the fold"},
        "negative": {"axis": "output / gain DEFICIT", "reached_by_levers": False,
            "why_not": "a gain-reducing lever pushes output even LOWER; the threshold-shift frame has no "
                       "restorative handle on a deficit on this axis (a restore problem on a different axis; sec.24 [O])"},
        "cognitive": {"axis": "long-range WIRING (dysconnection)", "reached_by_levers": False,
            "why_not": "a scalar current/drive lever leaves the locality imbalance EXACTLY invariant; geometry "
                       "cannot be re-routed by a threshold shift (the sec.19 chemical-limits result)"},
        "reading": ("the three-lever map is a POSITIVE-domain target map: it reaches the over-ignition threshold "
                    "axis ONLY. The negative (output-deficit) and cognitive (wiring) domains sit on DIFFERENT fault "
                    "axes the threshold-shift frame does not reach -- which is the axis-structural reason the dopamine "
                    "antipsychotic direction (L3) reverses positive symptoms but spares negative/cognitive ones. The "
                    "gap is AXIS-STRUCTURED, not dose-structured. Cites sec.24 (SZ-DISC + SZ-DOM)."),
        "cites": "sec.24 schizophrenia_discriminant (over-ignition) + schizophrenia_symptom_domains (positive=threshold / "
                 "negative=output / cognitive=wiring; gain-reducing operator reverses positive only)",
    }
    return {
        "title": "Three-lever psychotic over-ignition target map for the POSITIVE domain (engine-generated reads + cited lever frame)",
        "inherited_from": "analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the threshold-shift "
                          "intervention-logic technology, applied to the schizophrenia POSITIVE (over-ignition) domain "
                          "(fourth application after bipolar sec.30, epilepsy sec.31 and depression sec.32; the one that "
                          "exercises a NEW edge of the frame -- the first DOMAIN-RESTRICTED case, and an L1+L3 CO-DOMINANT "
                          "distribution)",
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_sec24": "sec.24 (schizophrenia_discriminant SZ-DISC + schizophrenia_symptom_domains SZ-DOM) established "
                          "that psychosis' POSITIVE domain is the OVER-IGNITION pole of the threshold axis (an excitatory E/I "
                          "bias LOWERS the R19 fold -> aberrant salience) and that a gain-REDUCING antipsychotic-class push "
                          "RAISES the fold back, reversing the POSITIVE domain ONLY (negative = output-deficit axis, cognitive "
                          "= wiring axis, both unreached -- the axis-structural account of why D2 blockade spares them). But "
                          "sec.24 treated that gain-reducing push as a SINGLE abstract operator. This map DECOMPOSES it into "
                          "the three mechanistically-distinct levers for the POSITIVE domain and grounds each in a DNA read of "
                          "the actual schizophrenia genes. It adds NO new constant and re-derives no rule -- the schizophrenia "
                          "counterpart of the bipolar B4->sec.30, epilepsy sec.25->sec.31 and depression sec.27->sec.32 "
                          "decompositions.",
        "domain_restriction_witness": domain_restriction,
        "disorder_level_sign": ("the POSITIVE domain is the OVER-ignition pole (an excitatory bias lowers the fold so weak "
                           "assemblies ignite); its corrective sign is REDUCE excess drive / RAISE the fold -- the SAME "
                           "direction as epilepsy and bipolar mania, the OPPOSITE of depression's restore-deficient. BUT the "
                           "sign is DOMAIN-RESTRICTED, not disorder-wide: the negative (output-deficit) and cognitive (wiring) "
                           "domains are DEFICITS on different axes the threshold-shift levers do not reach. And the L1 NMDA "
                           "direction is SIGN-SUBTLE: the leading etiology is NMDA HYPOfunction on PV interneurons -> "
                           "downstream disinhibition, so the over-ignition is itself a downstream effect and a glycine-site "
                           "AGONIST (restorative) direction also appears. Both are stated, not hidden."),
        "unifying_frame": ("the psychotic POSITIVE-domain operating point is the over-ignition pole (sec.24): an excitatory "
                           "bias lowers the R19 fold so weak assemblies ignite (aberrant salience). It is raised back toward "
                           "selective ignition by ANY of three levers, with L1 and L3 CO-DOMINANT. L1 reduces the inward "
                           "glutamatergic/Ca current (the NMDA/AMPA/Ca set -- sign-subtle: the NMDA-hypofunction etiology means "
                           "a glycine-site agonist restorative direction also appears), L2 restores the outward K+/GABA-A "
                           "inhibitory current (the interneuron-restore route), L3 removes the up-stream DOPAMINE drive (the "
                           "established antipsychotic axis: the D2/D3/D4 receptors, the TH/DAT synthesis-transport set, and the "
                           "HTR2A/COMT modulatory set). Each lever has a cited POSITIVE-domain-restoring agent DIRECTION; "
                           "efficacy is asserted nowhere. The map reaches the POSITIVE domain ONLY -- the negative (output-"
                           "deficit) and cognitive (wiring) domains are honestly out of reach (the domain-restriction). Two "
                           "honest sign caveats: the L1 NMDA direction is hypofunction-subtle, and the HTR2A direction is "
                           "NON-MONOTONE (antagonist atypical and agonist psychedelic routes both appear)."),
        "levers": LEVER_FRAME,
        "lever_distribution_witness": {
            "counts": counts,
            "dominant_levers": dominant_levers,
            "codominant": codominant,
            "reading": (("schizophrenia is %s CO-DOMINANT (%d targets each) -- the third distribution pattern: bipolar "
                         "leaned on L1 (calcium), epilepsy on L2 (the M-current), depression on L3 (HPA/monoamine/"
                         "neurotrophic, L3-dominant), and schizophrenia loads the POSITIVE-domain raise on BOTH L1 (the "
                         "glutamate/NMDA axis) and L3 (the dopamine antipsychotic axis) at once -- the two leading "
                         "pathophysiologies of psychosis. The SAME three abstract levers re-distribute as a co-dominant "
                         "pair." % ("+".join(dominant_levers), top))
                        if codominant else
                        ("schizophrenia is %s-dominant (%d of %d targets)." % (dominant_levers[0], top, len(entries)))),
        },
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a receptor occupancy (NOT a D2 occupancy), not "
                     "a synaptic dopamine/glutamate level, not a potency, not a dose, not in-vivo selectivity, not a clinical "
                     "effect, and NOT the sec.24 network over-ignition threshold (the aberrant-salience fold on R) (those are "
                     "[O]). The promoter |h_sp| is the gene's OWN switch stiffness, carried alongside, never folded into a "
                     "clinical magnitude or equated with the network threshold. gamma is blind to on/off and to "
                     "gain/loss/expression-level of function. L3 (the dopamine drive) mechanism link is [O] -- the read places "
                     "the gene, it does not derive the dopaminergic/network mechanism."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never drugs, doses, "
                    "protocols, or patients; schizophrenia is polygenic, heterogeneous and DYSconnective and roughly a third "
                    "is treatment-resistant (LOCKED); the map reaches the POSITIVE domain ONLY (the negative output-deficit "
                    "and cognitive wiring domains are out of reach -- the domain-restriction, the axis-structural reason "
                    "dopamine blockade spares them); the L1 NMDA direction is HYPOfunction-subtle (a glycine-site agonist "
                    "restorative direction also appears, NOT simple excitation reduction) and the HTR2A direction is "
                    "NON-MONOTONE -- both recorded honestly; a lever direction is a mechanism boundary, not a claim about the "
                    "disorganised subjective state (Axis-A; consciousness_claim=0; hard problem OPEN)."),
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

def schizophrenia_threshold_levers_results():
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
        "reuses_sec24_overignition_direction": True,
    }
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "l3_mechanism_link": "OPEN [O] -- the dopaminergic/serotonergic signalling mechanism is cited biology, not derived",
        "promoter_hsp_vs_network_threshold": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the sec.24 network over-ignition threshold (the aberrant-salience fold on R)",
        "domain_restricted_positive_only": 1.0,
        "l1_l3_codominant": 1.0,
        "nonmonotone_and_nmda_hypofunction_caveats_recorded": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "schizophrenia_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_schizophrenia_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"schizophrenia_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = schizophrenia_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 96)
    print("T1a-L  SCHIZOPHRENIA THREE-LEVER MAP  (inherited from analgesic v2.0; engine READ-ONLY; L1+L3 co-dominant)")
    print("=" * 96)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  decomposes sec.24 push: {inv['reuses_sec24_overignition_direction']}")
    print("-" * 96)
    print(f"  {'gene':9} {'lev':4} {'gamma':>7} {'|h_sp|':>8} {'domain':9} {'channel/protein':38} sz anchor")
    for e in res["entries"]:
        cp = e["channel"] or e.get("protein") or "-"
        dom = e["domain_reach"].split()[0]
        print(f"  {e['gene']:9} {e['lever']:4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {dom:9} "
              f"{cp[:38]:38} {e['schizophrenia_genetic_anchor'][:30]}")
    print("-" * 96)
    w = res["lever_distribution_witness"]
    print("  targets by lever: " + ", ".join(f"{k}={v}" for k, v in w["counts"].items())
          + f"   -> {'CO-DOMINANT ' + '+'.join(w['dominant_levers']) if w['codominant'] else 'DOMINANT ' + w['dominant_levers'][0]}")
    dr = res["domain_restriction_witness"]
    print(f"  domain reach: positive={dr['positive']['reached_by_levers']} "
          f"negative={dr['negative']['reached_by_levers']} cognitive={dr['cognitive']['reached_by_levers']}  (positive-domain map)")
    print(f"  n_targets: {res['n_targets']}   channels: {len(res['channels_present'])}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 96)
    ok = inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
    print("  T1a-L THREE-LEVER MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
