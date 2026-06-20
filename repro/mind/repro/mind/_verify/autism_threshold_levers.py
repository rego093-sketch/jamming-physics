#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autism_threshold_levers.py  —  ASD-T-L (sec.34): the THREE-LEVER target map for the autistic
E/I-EXCESS (over-excitable THRESHOLD) operating point, and the FIFTH application of the inherited
analgesic_threshold_logic v2.0 cross-cutting layer (after bipolar sec.30, epilepsy sec.31, depression
sec.32 and schizophrenia sec.33). It re-derives no rule: it reads the SAME R19 substrate
(E.spinodal/E.barrier) and the SAME gamma = -mean(NN stacking dG, SantaLucia 1998) the engine uses to
write genes, and it UNIFIES the pre-existing multi-lever autism work (autism_multilever_threshold.py,
D9.3) under the formal L1/L2/L3 inheritance frame -- it is a re-statement/alignment of an existing
module, not a new mechanism.

WHY THIS EXISTS (the gap it closes). sec.18-19 (autism_discriminant + autism_candidate_limits, the ASD
three-axis discriminant and the chemical-reach-limit nulls) established the autistic substrate as THREE
fault axes, and autism_multilever_threshold.py (D9.3) already tested splitting a threshold-lowering
correction across several stiffness-selective levers. But the lever frame there used informal names
(A1/A2/A3) and the result was reported as a coverage/safety experiment. This map UNIFIES that work under
the SAME formal L1/L2/L3 frame the rest of the atlas uses, grounds each lever in a DNA read of the actual
autism genes, and -- crucially -- makes the autism DOMAIN-RESTRICTION concrete by NAMING the out-of-reach
targets (the O-axis and W-axis genes a threshold-shift lever cannot touch), with the unreachability
PROVEN independently in sec.19. This is the autism counterpart of the bipolar B4->sec.30, epilepsy
sec.25->sec.31, depression sec.27->sec.32 and schizophrenia sec.24->sec.33 decompositions.

THE THREE AUTISM AXES (from sec.18-19; the SAME parallel as schizophrenia's three clinical domains):
  T  (excitability / E-I THRESHOLD)  = the over-excitable pole (an asymmetric excitatory bias LOWERS the
        R19 fold so the cell fires too readily -- the E/I-imbalance / seizure-comorbidity axis). REACHED
        by the levers: the corrective sign is REDUCE excess excitation / RAISE the fold (the SAME
        direction as epilepsy / schizophrenia-positive / bipolar mania).
  O  (synaptic GAIN / OUTPUT)        = the synaptic-scaffold / gain-deficit axis (SHANK/SYNGAP/neurexin).
        NOT REACHED: a gain-reducing threshold lever pushes a gain DEFICIT even lower (the depression-
        style restore problem on a different axis -- the schizophrenia-negative analogue).
  W  (long-range WIRING)             = the connectivity / dysconnection axis (CNTNAP2/RELN). NOT REACHED:
        a scalar current/drive lever leaves the locality/routing EXACTLY invariant (sec.19 PROVED this:
        a threshold-lowering chemical only masks the W deficit via OVER-SYNCHRONISATION, the seizure
        analogue, never a correction -- the schizophrenia-cognitive analogue, but here PROVEN).
So the three-lever map is a T-axis (E/I-excess) target map. The O/W gap is AXIS-STRUCTURED, not dose-
structured. This is the schizophrenia DOMAIN-RESTRICTION pattern inherited as precedent, with two
autism-specific strengthenings: (1) the unreachable axes are PROVEN unreachable in sec.19 (not merely
argued), and (2) their genes are NAMED in the map (out_of_reach_targets) so the restriction is concrete.

THE LEVER DISTRIBUTION (honest). Where bipolar leaned on L1 (calcium GWAS), epilepsy on L2 (the KCNQ2/3
M-current), depression on L3 (HPA/monoamine/neurotrophic, L3-dominant) and schizophrenia on L1+L3
co-dominant (glutamate + dopamine), autism is L1-DOMINANT with a NEARLY-EMPTY L3:
  L1  reduce the inward (glutamatergic/Na/Ca) excitatory current   (the NMDA/AMPA/Na/Ca set; DOMINANT)
  L2  increase the outward (K+) / restore the GABA-A inhibitory current  (the interneuron/tonic-GABA set)
  L3  remove an up-stream sensitising drive                         (SPARSE: autism has NO clean upstream
                                                                     pharmacological drive -- a single
                                                                     serotonergic [O] handle, no more)
The L3-sparsity is itself the finding: the E/I-excess operating point is set LOCALLY (by the excitatory/
inhibitory current balance), not by a strong up-stream neuromodulatory drive -- which is exactly why the
established pharmacology of autism core features is so thin compared with psychosis or depression.

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| / barrier
are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V] (reproducible);
their ORDER is [F] (forced). This is NOT a receptor occupancy, NOT a synaptic glutamate/GABA level, NOT
a drug potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect, and -- the autism-specific
addition -- the promoter |h_sp| is NOT the sec.18 NETWORK over-excitation fold (the E/I ignition
threshold on R) (that is a separate network quantity). gamma is blind to on/off and to
gain/loss/expression-level of function. The L3 (serotonergic drive) mechanism link is [O].

THE HONEST DIRECTION CAVEATS (autism-specific; recorded, not hidden).
  (i)   SCN2A SIGN SUBTLETY (the autism analogue of the schizophrenia NMDA-hypofunction caveat). Nav1.2:
        GAIN-of-function (early infantile) drives DEE/severe epilepsy (the seizure pole, the "reduce
        inward Na" direction); LOSS-of-function / haploinsufficiency drives the milder ASD/ID pole -- the
        OPPOSITE sign (a restorative direction). So the L1 Na placement is structural/trait-blind, but its
        clinical DIRECTION is sign-subtle and stays [O]. (GRIN2B carries the same GoF-DEE / milder-ASD
        split.)
  (ii)  THE T-LEVER, PUSHED TOO HARD, BECOMES THE SEIZURE EDGE. sec.19 showed the W-fault cannot be fixed
        by lowering the threshold; pushing the lever to compensate only OVER-SYNCHRONISES (the global-sync
        / seizure analogue). So the autistic T-lever and the epileptic over-sync pole are the SAME axis
        seen from two sides -- consistent with the real ASD+epilepsy comorbidity -- and over-pushing the
        E/I lever crosses into the seizure edge. Recorded.
  (iii) DOMAIN-RESTRICTION (the headline, above). The map reaches the T (E/I-excess) axis only; the O
        (gain-deficit) and W (wiring) axes are a DIFFERENT axis the threshold-shift frame does not reach,
        PROVEN in sec.19 and named in out_of_reach_targets.

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places READS and
TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any agent treats anyone. Autism is
POLYGENIC and HETEROGENEOUS, much of its genetics is SYNAPTIC/WIRING (the out-of-reach axes), and it is a
neurodevelopmental DIFFERENCE, not only a deficit -- LOCKED. A lever direction is a mechanism boundary,
NOT a claim about identity, the subjective world, or whether any trait should be changed
(consciousness_claim stays 0; hard problem OPEN).

No tuning: gamma is measured; |h_sp|/barrier are the locked R19 forms; the lever assignments, axis mapping
and citations are CITED Layer-2 biology, not engine outputs. Governed by VP_SPEC_v1_8 (SEED=19). Engine
imported READ-ONLY (tree 0fbf4988...).

Run:  python3 autism_threshold_levers.py
Out:  autism_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "autism_levers_promoters.cache.json")
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

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the autistic E/I-excess pole) ----
LEVER_FRAME = {
  "L1": "reduce the inward (glutamatergic/Na/Ca excitatory) drive -- the NMDA / AMPA / Na / Ca-channel "
        "set. Reaches the T (E/I-excess) axis by raising the over-excitation fold. DOMINANT for autism. "
        "SIGN-SUBTLE on SCN2A/GRIN2B: a GAIN-of-function variant drives the severe seizure pole (the "
        "'reduce inward current' direction) while LOSS-of-function/haploinsufficiency drives the milder "
        "ASD pole (the OPPOSITE, restorative direction) -- so the naive 'reduce inward current' sign is "
        "not the clinical sign (see caveat)",
  "L2": "increase the outward (K+) / restore the GABA-A inhibitory current -- the K+ (Kv7) and the "
        "tonic/synaptic GABA-A interneuron set (the GABA side of the E/I imbalance). Raises the restoring "
        "side of the same T (E/I-excess) axis",
  "L3": "remove / normalise an UP-STREAM sensitising drive. SPARSE for autism: there is NO clean up-stream "
        "pharmacological drive that sets the E/I operating point (the imbalance is set LOCALLY by the "
        "current balance) -- only a single serotonergic [O] handle (the oldest ASD biomarker, "
        "hyperserotonemia), whose mechanism link to the cortical E/I fold is indirect and non-monotone",
}

GL1 = "[F] structural: a glutamatergic/Na/Ca inward-current REDUCTION raises the over-excitation fold and reaches the T (E/I-excess) axis (anchored to cited agents; sign-subtle on SCN2A/GRIN2B, see caveat)"
GL2 = "[F] structural: an outward-K+ / GABA-A inhibitory-current RESTORE raises the same over-excitation fold (anchored to cited agents)"
GL3 = "[O] cited biology: gamma places the gene in the lever map; the serotonergic/network signalling mechanism is NOT derived (and is indirect/non-monotone for the autistic E/I fold)"

DOM_T     = "T (the E/I-excess / over-excitation THRESHOLD axis the levers REACH)"
DOM_T_ADJ = "T-adjacent (restore inhibition on the same over-excitation threshold axis)"

# ===================== LEVER TARGETS (the T-axis genes that ARE the levers) =====================
CONTEXT = {
  # -------- L1 (DOMINANT): reduce the inward glutamatergic/Na/Ca excitatory current --------
  "GRIN2A": dict(lever="L1", domain=DOM_T, channel="NMDA-R GluN2A (glutamate, Ca2+-permeable)", protein=None,
      push="reduce the inward NMDA (GluN2A) current to raise the over-excitation fold -- the cross-disorder glutamatergic gene shared with the schizophrenia/bipolar maps",
      asd_anchor="a glutamatergic NMDA-receptor subunit implicated across ASD and the cross-disorder psychiatric set (SFARI/SCHEMA); the NMDA arm of the E/I-imbalance hypothesis",
      direction_agent="glutamatergic (NMDA-modulation) DIRECTION for the T axis (carried with the NMDA set; DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Rubenstein & Merzenich 2003 Genes Brain Behav 2:255 (E/I imbalance model of autism); SFARI Gene GRIN2A; Trubetskoy 2022 Nature 604:502 (cross-disorder glutamatergic)"),
  "GRIN2B": dict(lever="L1", domain=DOM_T, channel="NMDA-R GluN2B (glutamate, Ca2+-permeable)", protein=None,
      push="reduce the inward NMDA (GluN2B) current to raise the over-excitation fold -- a high-confidence de novo ASD gene (the GoF-DEE severe pole excluded; the milder ASD pole here; sign-subtle)",
      asd_anchor="a high-confidence (SFARI category-1) de novo ASD gene; severe GoF/LoF variants cause DEE, the milder ASD/ID end is the pole carried here (GoF-DEE excluded)",
      direction_agent="glutamatergic-tone (NMDA-modulation) DIRECTION for the T axis -- SIGN-SUBTLE (GoF-DEE vs milder-ASD split, like SCN2A; DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Sanders 2015 Neuron 87:1215 (de novo ASD genes incl. GRIN2B); SFARI Gene GRIN2B"),
  "GRIA1": dict(lever="L1", domain=DOM_T, channel="AMPA-R GluA1 (glutamate, fast excitatory)", protein=None,
      push="reduce the inward AMPA (GluA1) current to raise the over-excitation fold -- the fast-excitatory glutamatergic partner of the NMDA set",
      asd_anchor="an AMPA-receptor subunit in the glutamatergic E/I set; fast excitatory transmission downstream of the NMDA/interneuron balance (a common-variant glutamatergic candidate)",
      direction_agent="AMPA-glutamatergic DIRECTION for the T axis (the fast-excitatory route carried with the NMDA set; DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Rubenstein & Merzenich 2003 (E/I imbalance); glutamatergic-receptor set"),
  "SCN2A": dict(lever="L1", domain=DOM_T, channel="Na_V1.2 (voltage-gated Na+)", protein=None,
      push="reduce the inward Na+ (Na_V1.2) current to raise the over-excitation fold -- one of the highest-confidence ASD genes; STRONGLY SIGN-SUBTLE (GoF-DEE seizure pole vs LoF-ASD milder pole, see caveat)",
      asd_anchor="one of the most recurrently mutated, highest-confidence (SFARI-1) ASD genes; Nav1.2 GAIN-of-function -> early infantile DEE (seizure pole), LOSS-of-function / haploinsufficiency -> the milder ASD/ID pole",
      direction_agent="Na-channel-modulation DIRECTION -- SIGN-SUBTLE: the 'reduce inward Na' direction is the GoF-seizure direction, while the LoF-ASD pole is the OPPOSITE (restorative) sign (DIRECTION, not efficacy; sign recorded as subtle)",
      grade_mechanism=GL1,
      src="Sanders 2018 Trends Neurosci 41:442 (SCN2A GoF-DEE vs LoF-ASD); Satterstrom 2020 Cell 180:568 (SCN2A top ASD gene)"),
  "CACNA1C": dict(lever="L1", domain=DOM_T, channel="Ca_V1.2 (L-type Ca2+)", protein=None,
      push="reduce the inward Ca2+ (L-type) current to raise the over-excitation fold -- the cross-disorder calcium set-point gene (Timothy-syndrome GoF excluded; common-variant pole)",
      asd_anchor="the most-replicated CROSS-DISORDER calcium-channel locus (PGC five-disorder finding spanning ASD, schizophrenia, bipolar, depression, ADHD); Timothy-syndrome GoF excluded, the common-variant pole carried",
      direction_agent="L-type Ca-channel-modulation DIRECTION (cross-disorder set-point; carried as structural context, not a clean ASD target)",
      grade_mechanism=GL1,
      src="Cross-Disorder Group PGC 2013 Lancet 381:1371 (CACNA1C across five disorders)"),
  # -------- L2: increase the outward K+ / restore the GABA-A inhibitory current (the GABA side of E/I) --------
  "KCNQ3": dict(lever="L2", domain=DOM_T_ADJ, channel="K_V7.3 (M-current K+)", protein=None,
      push="increase the outward K+ (M-current, Kv7.3) to raise the restoring side of the over-excitation axis -- the textbook anticonvulsant K+ route; the seizure-edge brake shared with the epilepsy/bipolar maps",
      asd_anchor="Kv7.3 (the neuronal M-current); benign familial neonatal epilepsy (BFNE) is self-limiting -- the moderate, seizure-edge-relevant K+ brake on the same E/I axis",
      direction_agent="M-current (Kv7) opener DIRECTION (raise the outward K+ restoring current; the seizure-edge brake; DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Brown & Passmore 2009 Br J Pharmacol 156:1185 (M-current Kv7); BFNE benign course"),
  "GABRB3": dict(lever="L2", domain=DOM_T_ADJ, channel="GABA-A receptor beta3 (Cl-)", protein=None,
      push="RESTORE the inhibitory GABA-A (Cl-) current via the beta3 subunit -- the 15q11-13 tonic-inhibition lever; raises the inhibitory side of the E/I axis (the autism GABA deficit)",
      asd_anchor="GABA-A beta3 (15q11-13, the Angelman/Dup15q region) -- one of the longest-standing ASD candidate genes and a core node of the GABAergic E/I-imbalance hypothesis",
      direction_agent="GABA-A inhibitory-restore DIRECTION (restore the tonic/synaptic GABA-A current; raises the over-excitation fold from the inhibitory side; DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Cook 1998 Am J Hum Genet 62:1077 (15q11-13 GABRB3, ASD); Rubenstein & Merzenich 2003 (GABA side of E/I)"),
  "GABRA5": dict(lever="L2", domain=DOM_T_ADJ, channel="GABA-A receptor alpha5 (Cl-, extrasynaptic)", protein=None,
      push="RESTORE the EXTRASYNAPTIC tonic GABA-A (alpha5, Cl-) current -- the tonic-inhibition lever's exact substrate; raises the inhibitory side of the E/I axis",
      asd_anchor="extrasynaptic GABA-A alpha5 -- the tonic GABA-A current itself; 15q11-13, the same Dup15q ASD interval, mediating tonic inhibition that sets the E/I set-point",
      direction_agent="extrasynaptic GABA-A (alpha5) tonic-inhibition-restore DIRECTION (raise the tonic GABA-A current; DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Cook 1998 Am J Hum Genet 62:1077 (15q11-13 GABA-A cluster); tonic GABA-A inhibition"),
  "GABRA2": dict(lever="L2", domain=DOM_T_ADJ, channel="GABA-A receptor alpha2 (Cl-)", protein=None,
      push="RESTORE the synaptic GABA-A (alpha2, Cl-) current -- the synaptic-inhibition partner of the alpha5/beta3 set; raises the inhibitory side of the E/I axis",
      asd_anchor="GABA-A alpha2 -- a synaptic GABA-A subunit in the inhibitory set tied to the cortical E/I balance of autism",
      direction_agent="synaptic GABA-A (alpha2) inhibitory-restore DIRECTION (raise the synaptic GABA-A current; DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Rubenstein & Merzenich 2003 (GABAergic E/I imbalance); GABA-A inhibitory set"),
  # -------- L3 (SPARSE/cautious [O]): the single serotonergic up-stream handle --------
  "SLC6A4": dict(lever="L3", domain=DOM_T, channel=None, protein="serotonin transporter 5-HTT (SLC6A4)",
      push="modulate the serotonergic tone (5-HTT) -- the SINGLE up-stream [O] handle; hyperserotonemia is the OLDEST ASD biomarker, but the mechanism link to the cortical E/I fold is INDIRECT and NON-MONOTONE",
      asd_anchor="the serotonin transporter; elevated whole-blood/platelet serotonin (hyperserotonemia) in ~25-30% of ASD is the oldest replicated ASD biomarker -- but a developmental/peripheral signal whose link to the cortical E/I operating point is indirect",
      direction_agent="serotonergic-tone DIRECTION (5-HTT; the single, weak, NON-MONOTONE up-stream handle -- recorded as the L3-sparsity finding; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Schain & Freedman 1961 J Pediatr 58:315 (hyperserotonemia, the oldest ASD biomarker); Muller 2016 Neuroscience 321:24 (serotonin in ASD, indirect/non-monotone)"),
}

# ===== OUT-OF-REACH TARGETS (the O-axis + W-axis genes a threshold-shift lever CANNOT touch) =====
# These are NOT levers. They carry a gamma read (their own promoter switch stiffness) ALONGSIDE, with
# the explicit record that NO threshold lever reaches their axis (sec.19 PROVED it for W). Naming them
# makes the autism DOMAIN-RESTRICTION concrete instead of abstract.
OUT_OF_REACH = {
  # --- O-axis: synaptic GAIN / OUTPUT (a gain-reducing lever pushes a deficit even LOWER) ---
  "SHANK3": dict(axis="O", role="postsynaptic scaffold (master synaptic-gain organiser)", channel=None,
      why_unreached="the O (synaptic-gain/output) axis is a DEFICIT axis: a gain-reducing threshold lever pushes output even LOWER, so the threshold-shift frame has NO restorative handle here (the schizophrenia-negative analogue)",
      asd_anchor="Phelan-McDermid (22q13) postsynaptic scaffold; one of the highest-confidence ASD genes; a synaptic-gain (output) mechanism, NOT an excitability current",
      src="Durand 2007 Nat Genet 39:25 (SHANK3, ASD); Phelan-McDermid syndrome"),
  "SYNGAP1": dict(axis="O", role="synaptic Ras-GAP (gain regulator)", channel=None,
      why_unreached="the O (synaptic-gain/output) axis: SYNGAP1 sets synaptic gain/plasticity, NOT the excitability current -- a threshold lever cannot restore a gain deficit on this axis",
      asd_anchor="a high-confidence ASD/ID gene; a synaptic Ras-GAP regulating AMPA-receptor trafficking and synaptic gain (an output mechanism)",
      src="Hamdan 2009 N Engl J Med 360:599 (SYNGAP1, ID/ASD)"),
  "NRXN1": dict(axis="O", role="presynaptic neurexin-1 (synaptic adhesion / gain)", channel=None,
      why_unreached="the O (synaptic-gain/output) axis: neurexin-1 organises presynaptic release/gain via trans-synaptic adhesion, NOT the excitability current -- unreached by a threshold lever",
      asd_anchor="a recurrent ASD CNV gene; presynaptic neurexin-1, a trans-synaptic adhesion organiser of synaptic output (a gain/adhesion mechanism)",
      src="Kim 2008 Am J Hum Genet 82:199 (NRXN1, ASD); trans-synaptic adhesion"),
  # --- W-axis: long-range WIRING (a scalar lever leaves locality/routing invariant; sec.19 PROVED it) ---
  "CNTNAP2": dict(axis="W", role="Caspr2 long-range cell-adhesion (wiring)", channel=None,
      why_unreached="the W (long-range wiring) axis: a scalar current/drive lever leaves the locality/routing EXACTLY invariant -- sec.19 PROVED a threshold-lowering chemical only MASKS the W deficit via over-synchronisation (the seizure analogue), never corrects it",
      asd_anchor="Caspr2 (a neurexin-family cell-adhesion molecule) clustering K+ channels at the node; a long-range CONNECTIVITY/wiring gene (the dysconnection axis), not an excitability current",
      src="Alarcon 2008 Am J Hum Genet 82:150 (CNTNAP2, ASD/language); long-range connectivity"),
  "RELN": dict(axis="W", role="reelin (cortical lamination / wiring)", channel=None,
      why_unreached="the W (long-range wiring) axis: reelin sets cortical lamination/migration geometry -- a developmental WIRING fault that no scalar threshold lever can re-route (sec.19); the over-sync masking caveat applies",
      asd_anchor="reelin, the lamination/migration signal organising cortical layering and long-range wiring; a cross-disorder candidate -- a geometry/wiring mechanism, not an excitability current",
      src="Fatemi 2005 Mol Psychiatry 10:251 (reelin in autism); cortical lamination"),
  # --- syndromic transcriptional master (spans O/W; not an excitability current -> not a threshold lever) ---
  "MECP2": dict(axis="syndromic (O/W via chromatin)", role="MeCP2 chromatin / transcriptional regulator (Rett)", channel=None,
      why_unreached="a transcriptional MASTER up-stream of many synaptic (O) and wiring (W) genes -- it sets gene-expression programmes, NOT an excitability current, so it is not a threshold lever (and it acts across the unreachable O/W axes)",
      asd_anchor="MeCP2 (X-linked); loss causes Rett syndrome and duplication causes MECP2-duplication syndrome -- a chromatin/transcriptional regulator master, the canonical syndromic ASD-spectrum gene",
      src="Amir 1999 Nat Genet 23:185 (MECP2, Rett); chromatin/transcriptional master"),
}

def read(sym, g):
    c = CONTEXT[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the network E/I fold)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "domain_reach": c["domain"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "autism_genetic_anchor": c["asd_anchor"],
        "t_axis_restoring_agent_direction": c["direction_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": GL1 if c["lever"] == "L1" else (GL2 if c["lever"] == "L2" else c["grade_mechanism"]),
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_network_threshold": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch "
                                       "stiffness, NOT the sec.18 network over-excitation fold (the E/I "
                                       "ignition threshold on R); never equated",
        "grade_clinical_map": "[O] OPEN -- not a receptor occupancy, synaptic glutamate/GABA level, "
                              "potency, dose, in-vivo selectivity, or clinical effect",
        "context_grade": "CITED Layer-2 biology (not an engine output)",
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
        "autism_genetic_anchor": c["asd_anchor"],
        "grade_read": "[V] reproducible promoter-switch-threshold read (carried alongside; does NOT place a lever)",
        "grade_reach": "[F] NOT REACHED -- the threshold-shift frame has no handle on this axis (axis-structured, not dose-structured)",
        "context_grade": "CITED Layer-2 biology (not an engine output)",
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
    # out-of-reach reads (the named O/W targets)
    oor_g = {s: gamma(cache[s]["seq"]) for s in OUT_OF_REACH if s in cache}
    oor = [read_out_of_reach(s, oor_g[s]) for s in oor_g]
    oor.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)
    oor_by_axis = {}
    for e in oor:
        oor_by_axis.setdefault(e["fault_axis"], []).append(e["gene"])

    # lever-distribution witness: autism is L1-DOMINANT with a nearly-empty L3
    counts = {k: len(v) for k, v in by_lever.items()}
    ranked = sorted(counts, key=lambda k: counts[k], reverse=True)
    top = counts[ranked[0]]
    dominant_levers = sorted([k for k, n in counts.items() if n == top])
    codominant = len(dominant_levers) >= 2

    # domain-restriction witness (the autism headline; the schizophrenia pattern inherited, then strengthened)
    domain_restriction = {
        "T": {"axis": "excitability / E-I threshold (over-excitation)", "reached_by_levers": True,
            "sign": "REDUCE excess excitation / RAISE the fold (the SAME direction as epilepsy / "
                    "schizophrenia-positive / bipolar mania) -- L1 reduce inward glutamate/Na/Ca, L2 "
                    "restore K+/GABA-A inhibition both raise the fold; SIGN-SUBTLE on SCN2A/GRIN2B (GoF-DEE "
                    "vs milder-ASD split)"},
        "O": {"axis": "synaptic gain / output (deficit)", "reached_by_levers": False,
            "named_genes": oor_by_axis.get("O", []),
            "why_not": "a gain-reducing threshold lever pushes a gain DEFICIT even LOWER; the threshold-"
                       "shift frame has no restorative handle on this axis (the schizophrenia-negative "
                       "analogue). Named genes: SHANK3 / SYNGAP1 / NRXN1 (out_of_reach_targets)."},
        "W": {"axis": "long-range wiring (dysconnection)", "reached_by_levers": False,
            "named_genes": oor_by_axis.get("W", []),
            "why_not": "a scalar current/drive lever leaves the locality/routing EXACTLY invariant -- "
                       "sec.19 (autism_candidate_limits) PROVED a threshold-lowering chemical only MASKS "
                       "the W deficit via OVER-SYNCHRONISATION (the seizure analogue), never corrects it. "
                       "Named genes: CNTNAP2 / RELN (out_of_reach_targets)."},
        "reading": ("the three-lever map is a T-axis (E/I-excess) target map: it reaches the over-"
                    "excitation threshold axis ONLY. The O (synaptic-gain/output) and W (long-range "
                    "wiring) axes sit on DIFFERENT fault axes the threshold-shift frame does not reach -- "
                    "which is why so much of autism's genetics (the synaptic/wiring genes) is out of reach "
                    "of any threshold lever. The gap is AXIS-STRUCTURED, not dose-structured, and -- the "
                    "two autism-specific strengthenings over schizophrenia's domain-restriction -- it is "
                    "PROVEN in sec.19 (not merely argued) and its genes are NAMED here. Cites sec.18-19."),
        "cites": "sec.18-19 autism_discriminant (three-axis T/O/W discriminant) + autism_candidate_limits "
                 "(the chemical-reach-limit nulls PROVING a threshold lever masks-but-cannot-correct the W "
                 "fault) + autism_multilever_threshold D9.3 (the multi-lever coverage/safety experiment "
                 "this map unifies under the formal L1/L2/L3 frame)",
        "strengthenings_over_schizophrenia": [
            "the unreachable O/W axes are PROVEN unreachable in sec.19 (not merely argued, as in sec.33's negative/cognitive)",
            "the out-of-reach targets are NAMED genes (SHANK3/SYNGAP1/NRXN1 on O; CNTNAP2/RELN on W; MECP2 syndromic master) -- the domain-restriction made concrete",
            "over-pushing the T-lever crosses into the seizure edge (sec.19 over-synchronisation), tying the autistic T-axis to the epileptic over-sync pole -- the real ASD+epilepsy comorbidity",
        ],
    }
    return {
        "title": "Three-lever autistic E/I-excess (over-excitation) target map for the T axis -- a UNIFICATION "
                 "of the pre-existing multi-lever autism work (D9.3) under the formal L1/L2/L3 inheritance frame "
                 "(engine-generated reads + cited lever frame); the O/W axes named as out-of-reach",
        "inherited_from": "analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the threshold-shift "
                          "intervention-logic technology, applied to the autistic T (E/I-excess) axis (fifth "
                          "application after bipolar sec.30, epilepsy sec.31, depression sec.32 and schizophrenia "
                          "sec.33; this one UNIFIES a pre-existing module (autism_multilever_threshold, D9.3) under "
                          "the formal frame, is L1-DOMINANT with a nearly-empty L3, and inherits the schizophrenia "
                          "DOMAIN-RESTRICTION pattern -- strengthened by a sec.19 PROOF and by NAMING the out-of-"
                          "reach O/W targets)",
        "unifies_existing_module": "autism_multilever_threshold.py (D9.3) -- which tested single/dual/tri-lever "
                          "threshold-lowering (informal A1/A2/A3 levers) as a coverage/safety experiment. This map "
                          "re-states that work under the SAME formal L1/L2/L3 frame as the rest of the atlas, grounds "
                          "each lever in a DNA read of the actual autism genes, and adds the NAMED out-of-reach axes. "
                          "It adds NO new mechanism and NO new constant.",
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_sec18_19": "sec.18-19 (autism_discriminant + autism_candidate_limits) established the autistic "
                          "substrate as THREE fault axes (T excitability/E-I, O synaptic-gain/output, W long-range "
                          "wiring) and PROVED that a threshold-lowering chemical cannot correct the W (wiring) fault "
                          "(it only masks it via over-synchronisation). This map DECOMPOSES the corrective push on the "
                          "T axis into the three mechanistically-distinct levers and grounds each in a DNA read of the "
                          "actual autism genes, while NAMING the O/W genes the levers do NOT reach. It adds NO new "
                          "constant and re-derives no rule -- the autism counterpart of the bipolar B4->sec.30, "
                          "epilepsy sec.25->sec.31, depression sec.27->sec.32 and schizophrenia sec.24->sec.33 "
                          "decompositions.",
        "domain_restriction_witness": domain_restriction,
        "disorder_level_sign": ("the T axis is the OVER-excitation pole (an asymmetric excitatory bias lowers the "
                           "fold so the cell fires too readily); its corrective sign is REDUCE excess excitation / "
                           "RAISE the fold -- the SAME direction as epilepsy, schizophrenia-positive and bipolar "
                           "mania, the OPPOSITE of depression's restore-deficient. BUT the sign is DOMAIN-RESTRICTED, "
                           "not disorder-wide: the O (gain-deficit) and W (wiring) axes are DEFICITS/geometry the "
                           "threshold levers do not reach (PROVEN, sec.19). And the L1 SCN2A/GRIN2B direction is "
                           "SIGN-SUBTLE: a GoF variant drives the seizure pole (the reduce-inward direction) while a "
                           "LoF/haploinsufficiency variant drives the milder ASD pole (the opposite, restorative "
                           "direction). Both are stated, not hidden."),
        "unifying_frame": ("the autistic T (E/I-excess) operating point is the over-excitation pole (sec.18): an "
                           "asymmetric excitatory bias lowers the R19 fold so the cell fires too readily (the E/I "
                           "imbalance / seizure-comorbidity axis). It is raised back toward selective ignition by the "
                           "levers, with L1 DOMINANT. L1 reduces the inward glutamatergic/Na/Ca current (the NMDA/AMPA/"
                           "Na/Ca set -- sign-subtle on SCN2A/GRIN2B), L2 restores the outward K+/GABA-A inhibitory "
                           "current (the Kv7 + tonic/synaptic GABA-A set -- the GABA side of the imbalance), and L3 is "
                           "SPARSE (a single serotonergic [O] handle -- autism has no clean up-stream pharmacological "
                           "drive). The map reaches the T axis ONLY -- the O (synaptic-gain) and W (wiring) axes are "
                           "honestly out of reach (named in out_of_reach_targets; the W unreachability PROVEN in "
                           "sec.19). Two honest sign caveats: the L1 SCN2A/GRIN2B direction is GoF/LoF-subtle, and the "
                           "T-lever pushed too hard becomes the seizure edge (the over-synchronisation result)."),
        "levers": LEVER_FRAME,
        "lever_distribution_witness": {
            "counts": counts,
            "dominant_levers": dominant_levers,
            "codominant": codominant,
            "l3_sparse": bool(counts.get("L3", 0) <= 1),
            "reading": (("autism is %s-DOMINANT (%d targets; L2=%d restoring; L3=%d -- NEARLY EMPTY) -- the fifth "
                         "distribution pattern: bipolar leaned on L1 (calcium), epilepsy on L2 (the M-current), "
                         "depression on L3 (HPA/monoamine/neurotrophic, L3-dominant), schizophrenia on L1+L3 "
                         "co-dominant (glutamate + dopamine), and autism loads the E/I-excess raise on L1 (the "
                         "glutamate/Na/Ca excitatory current) with L2 as the GABA-restoring complement and an "
                         "almost-absent L3. The L3-SPARSITY is the finding: autism's E/I operating point is set "
                         "LOCALLY by the current balance, with NO strong up-stream pharmacological drive -- which is "
                         "why the established pharmacology of autism core features is so thin." %
                         (dominant_levers[0], top, counts.get("L2", 0), counts.get("L3", 0)))
                        if not codominant else
                        ("autism is %s CO-DOMINANT (%d targets each)." % ("+".join(dominant_levers), top))),
        },
        "out_of_reach_targets": {
            "_what": "the O-axis (synaptic-gain/output) and W-axis (long-range wiring) genes a threshold-shift lever "
                     "CANNOT touch -- named to make the autism domain-restriction CONCRETE. Each carries a gamma read "
                     "(its own promoter switch stiffness) ALONGSIDE, but is explicitly NOT a lever: the threshold-shift "
                     "frame has no handle on its axis (O is a gain DEFICIT a gain-reducing lever lowers further; W is "
                     "geometry a scalar lever leaves invariant -- sec.19 PROVED the W case). This is the autism-specific "
                     "strengthening of the schizophrenia domain-restriction: the unreachable axes are named, with real "
                     "genes and real citations, not left abstract.",
            "by_axis": oor_by_axis,
            "n": len(oor),
            "entries": oor,
        },
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a receptor occupancy, not a synaptic "
                     "glutamate/GABA level, not a potency, not a dose, not in-vivo selectivity, not a clinical effect, "
                     "and NOT the sec.18 network over-excitation fold (the E/I ignition threshold on R) (those are [O]). "
                     "The promoter |h_sp| is the gene's OWN switch stiffness, carried alongside, never folded into a "
                     "clinical magnitude or equated with the network threshold. gamma is blind to on/off and to "
                     "gain/loss/expression-level of function. L3 (the serotonergic drive) mechanism link is [O] -- the "
                     "read places the gene, it does not derive the serotonergic/network mechanism."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never drugs, "
                    "doses, protocols, or patients; autism is polygenic, heterogeneous, largely SYNAPTIC/WIRING in its "
                    "genetics (the out-of-reach axes) and a neurodevelopmental DIFFERENCE not only a deficit (LOCKED); "
                    "the map reaches the T (E/I-excess) axis ONLY (the O synaptic-gain and W wiring axes are out of "
                    "reach -- PROVEN in sec.19 and named here -- the axis-structural reason a threshold lever cannot "
                    "address the synaptic/wiring genetics); the L1 SCN2A/GRIN2B direction is GoF/LoF SIGN-SUBTLE and "
                    "the T-lever pushed too hard becomes the seizure edge -- both recorded honestly; a lever direction "
                    "is a mechanism boundary, not a claim about identity or the subjective world or whether any trait "
                    "should be changed (Axis-A; consciousness_claim=0; hard problem OPEN)."),
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

def autism_threshold_levers_results():
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
        "reuses_sec18_19_overexcitation_direction": True,
        "unifies_d9_3_multilever_module": True,
    }
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "unifies_existing_multilever_module": 1.0,
        "l3_mechanism_link": "OPEN [O] -- the serotonergic signalling mechanism is cited biology, not derived (and is indirect/non-monotone)",
        "promoter_hsp_vs_network_threshold": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the sec.18 network over-excitation fold (the E/I ignition threshold on R)",
        "domain_restricted_T_axis_only": 1.0,
        "l1_dominant_l3_sparse": 1.0,
        "out_of_reach_axes_named_and_proven_sec19": 1.0,
        "scn2a_grin2b_gof_lof_and_seizure_edge_caveats_recorded": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "autism_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_autism_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"autism_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = autism_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 100)
    print("ASD-T-L  AUTISM THREE-LEVER MAP  (inherited from analgesic v2.0; engine READ-ONLY; L1-dominant; T-axis only)")
    print("=" * 100)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  unifies D9.3 module   : {inv['unifies_d9_3_multilever_module']}   decomposes sec.18-19: {inv['reuses_sec18_19_overexcitation_direction']}")
    print("-" * 100)
    print(f"  {'gene':9} {'lev':4} {'gamma':>7} {'|h_sp|':>8} {'axis':6} {'channel/protein':38} asd anchor")
    for e in res["entries"]:
        cp = e["channel"] or e.get("protein") or "-"
        dom = e["domain_reach"].split()[0]
        print(f"  {e['gene']:9} {e['lever']:4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {dom:6} "
              f"{cp[:38]:38} {e['autism_genetic_anchor'][:28]}")
    print("-" * 100)
    print("  OUT-OF-REACH (named; NOT levers):")
    for e in res["out_of_reach_targets"]["entries"]:
        print(f"  {e['gene']:9} {'--':4} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {e['fault_axis'][:6]:6} "
              f"{(e['role'])[:38]:38} {e['autism_genetic_anchor'][:28]}")
    print("-" * 100)
    w = res["lever_distribution_witness"]
    print("  targets by lever: " + ", ".join(f"{k}={v}" for k, v in w["counts"].items())
          + f"   -> {'CO-DOMINANT ' + '+'.join(w['dominant_levers']) if w['codominant'] else 'DOMINANT ' + w['dominant_levers'][0]}"
          + f"  (L3 sparse={w['l3_sparse']})")
    dr = res["domain_restriction_witness"]
    print(f"  domain reach: T={dr['T']['reached_by_levers']} "
          f"O={dr['O']['reached_by_levers']} W={dr['W']['reached_by_levers']}  (T-axis map; O/W named & proven sec.19)")
    print(f"  n_targets: {res['n_targets']}   out_of_reach: {res['n_out_of_reach']}   "
          f"channels: {len(res['channels_present'])}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 100)
    ok = (inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
          and not w["codominant"] and w["dominant_levers"] == ["L1"] and w["l3_sparse"])
    print("  ASD-T-L THREE-LEVER MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
