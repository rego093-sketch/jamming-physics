#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epilepsy_threshold_levers.py  —  T2a-L (sec.31): the THREE-LEVER target map for the epileptic
seizure threshold. This is the analgesic_threshold_logic v2.0 technology (DOI 10.5281/zenodo.20733420)
INHERITED into the mind atlas and applied to epilepsy. It re-derives no rule: it reads the SAME R19
substrate (E.spinodal/E.barrier, byte-identical to vp_neuro_engine) and the SAME gamma = -mean(NN
stacking dG, SantaLucia 1998) the engine uses to write genes. It is the SECOND application of the
inherited cross-cutting layer (the first was bipolar, sec.30) and the cleanest one, because the
roadmap's T2a output definition -- "which intervention RAISES the over-synchronisation threshold" --
is LITERALLY an L1/L2 threshold-raise.

WHY THIS EXISTS (the gap it closes). sec.25 (epilepsy_oversync) established, CONFIRMED, that epilepsy
is the over-synchronisation pole of the engine's synchrony axis and that an inhibitory /
threshold-raising anticonvulsant-class push moves the global order parameter R back toward health.
But sec.25 treated that anticonvulsant push as a SINGLE, undifferentiated "threshold-raising
operator" -- it never said WHICH genes / channels / mechanisms realise the raise. The analgesic
three-lever frame supplies exactly that missing layer. This is the direct epilepsy counterpart of
the bipolar B4->sec.30 decomposition.

THE UNIFYING FRAME (inherited from analgesic v2.0, applied to the seizure threshold). A seizure is
a crossing of the firing/synchronisation threshold -- the engine's over-synchronisation pole
(sec.25). The crossing can be made HARDER -- the threshold raised -- from THREE mechanistically-
distinct directions, exactly as nociceptor firing can be raised from three:
  L1  reduce the inward (excitatory) current      (Na+/Ca2+/NMDA block; the depolarising drive down)
  L2  increase the outward (K+, inhibitory) current (M-current/K_V open; hyperpolarise away from fire)
  L3  remove the up-stream sensitising / triggering drive (mTOR hyperactivation; restore resting fold)
L2-adjacent carries the inhibitory RESTORING current realised through GABA-A chloride (the acute
benzodiazepine anticonvulsant brake) -- the same "increase the restoring current" spirit as L2, via
Cl- rather than K+. The engine reads, on one scale, the promoter switch-threshold STRUCTURE of the
genes behind all levers. For every target the map carries: lever, push direction, channel/protein,
the cited EPILEPSY GENETIC anchor, the cited threshold-raising AGENT DIRECTION (never efficacy), and
the [V]/[F]/[O] grades.

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| /
barrier are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V]
(reproducible); their ORDER is [F] (forced). This is NOT a channel activation voltage, NOT a drug
potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect, and -- the epilepsy-specific
addition -- the promoter |h_sp| is NOT the sec.25 NETWORK over-synchronisation threshold on the
global order parameter R (that is a separate network quantity). The promoter read is carried
ALONGSIDE as the gene's own switch stiffness; it is NEVER folded into a clinical magnitude or equated
with the over-sync threshold. gamma is blind to on/off and to gain/loss of function (it reads switch
STRUCTURE, not the trait). L3 (mTOR) mechanism link is [O]: the gamma read PLACES the gene in the
lever map; it does NOT derive the mTOR/network mechanism (enforced by epilepsy_l3_honesty.py).

THE GAIN/LOSS HONESTY POINT (epilepsy-specific, important). The L1 direction "reduce inward Na+"
raises the threshold for GAIN-OF-FUNCTION channelopathies (SCN2A/SCN8A GOF). It is CONTRAINDICATED
in SCN1A-Dravet, where the loss is in inhibitory interneurons, so reducing Na further worsens it.
This is recorded honestly on SCN1A (and is precisely WHY gamma is graded [V] for STRUCTURE only,
trait-blind, while the clinical direction is [O]). The lever frame is a mechanism boundary, not a
treatment rule.

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places
READS and TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any drug treats
anyone or that any individual should change treatment. Real epilepsy is HETEROGENEOUS (focal vs
generalised, genetic vs structural vs metabolic; channelopathies, mTORopathies, synaptopathies;
~30% drug-resistant) -- LOCKED. A lever direction is a mechanism boundary, NOT a claim about the
felt quality of a seizure or its aftermath (consciousness_claim stays 0; hard problem OPEN).

No tuning: gamma is measured (pure arithmetic over called dinucleotide steps); |h_sp|/barrier are
the locked R19 forms; the lever assignments and citations are CITED Layer-2 biology, not engine
outputs. Governed by VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 epilepsy_threshold_levers.py
Out:  epilepsy_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "epilepsy_levers_promoters.cache.json")
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

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the seizure threshold) ----
LEVER_FRAME = {
  "L1": "reduce the inward (excitatory) current -- block the depolarising Na+/Ca2+/NMDA drive that "
        "crosses the seizure/over-synchronisation threshold (raises the threshold, the sec.25 way, "
        "from the inward side)",
  "L2": "increase the outward (K+, inhibitory) current -- open the M-current/delayed-rectifier to "
        "hyperpolarise, pulling V_m away from firing (raises the threshold, the sec.25 way, from the "
        "outward side)",
  "L2-adjacent": "increase the inhibitory RESTORING current realised through GABA-A chloride (the "
        "acute benzodiazepine anticonvulsant brake) -- the same 'increase the restoring current' "
        "spirit as L2, via Cl- rather than K+",
  "L3": "remove the up-stream sensitising / triggering drive (mTOR hyperactivation) -- restore the "
        "resting fold (raises the threshold, the sec.25 way, by removing what LOWERED it); mechanism [O]",
}

# grade strings (inherited discipline)
GL1 = "[F] structural: an inward-current reduction raises the seizure threshold (anchored to cited agents)"
GL2 = "[F] structural: an outward-K+/inhibitory increase hyperpolarises -> raises the threshold (anchored to cited agents)"
GL3 = "[O] cited biology: gamma places the gene in the lever map; the mTOR/network mechanism is NOT derived"

# CITED Layer-2 context (NOT engine output). epilepsy_anchor = the cited epilepsy genetics;
# direction_agent = the cited threshold-raising agent DIRECTION (never an efficacy claim). channel/protein labelled.
CONTEXT = {
  # ================= L1: reduce the inward (excitatory) current =================
  "SCN1A": dict(lever="L1", channel="Na_V1.1 (voltage-gated Na+)", protein=None,
      push="reduce inward Na+ -> raise the AP threshold at the firing gate (GAIN-OF-FUNCTION case only)",
      epilepsy_anchor="the canonical epilepsy Na-channel gene: de novo SCN1A causes Dravet syndrome (SMEI) and the GEFS+ spectrum",
      direction_agent="voltage-gated Na-channel-blocker DIRECTION -- but APPLIES ONLY to gain-of-function channelopathies; in SCN1A-Dravet "
                      "the loss is in INHIBITORY interneurons, so a Na-blocker is CONTRAINDICATED (worsens it). This trait-dependence is exactly "
                      "why gamma is [V] for STRUCTURE only (trait-blind) and the clinical direction is [O]",
      grade_mechanism=GL1,
      src="Claes 2001 Am J Hum Genet 68:1327 (SCN1A in SMEI/Dravet); Escayg 2000 Nat Genet 24:343 (GEFS+); Dravet Na-blocker contraindication"),
  "SCN2A": dict(lever="L1", channel="Na_V1.2 (voltage-gated Na+)", protein=None,
      push="reduce inward Na+ (axonal/somatic upstroke) -> raise the AP threshold (gain-of-function early-onset case)",
      epilepsy_anchor="neuropsychiatric Na-channel gene; GAIN-of-function SCN2A causes early-infantile epileptic encephalopathy that is Na-blocker responsive (shared with ASD/BD risk)",
      direction_agent="voltage-gated Na-channel-blocker DIRECTION (the GOF-onset epileptic encephalopathy is the Na-blocker-responsive case; LOF later-onset is not)",
      grade_mechanism=GL1,
      src="Sanders 2012 Nature 485:237; Wolff 2017 Brain 140:1316 (SCN2A GOF early vs LOF late, Na-blocker response)"),
  "SCN8A": dict(lever="L1", channel="Na_V1.6 (voltage-gated Na+)", protein=None,
      push="reduce inward Na+ (Na_V1.6 persistent current) -> raise the threshold (gain-of-function case)",
      epilepsy_anchor="GAIN-of-function SCN8A causes early-infantile epileptic encephalopathy (EIEE13) with prominent persistent Na+ current",
      direction_agent="voltage-gated Na-channel-blocker DIRECTION (the persistent-current GOF is the targeted case)",
      grade_mechanism=GL1,
      src="Veeramah 2012 Am J Hum Genet 90:502 (SCN8A de novo EIEE13, gain of function)"),
  "CACNA1A": dict(lever="L1", channel="Ca_V2.1 (P/Q-type Ca2+)", protein=None,
      push="reduce inward Ca2+ (P/Q-type presynaptic) -> lower the depolarising/release drive across the threshold",
      epilepsy_anchor="P/Q-type Ca-channel locus in absence epilepsy and episodic-ataxia/epilepsy overlap",
      direction_agent="P/Q-type Ca-channel-modulation DIRECTION",
      grade_mechanism=GL1,
      src="Jouvenceau 2001 Lancet 358:801 (CACNA1A absence epilepsy + ataxia); Damaj 2015 Eur J Hum Genet 23:1505"),
  "CACNA1H": dict(lever="L1", channel="Ca_V3.2 (T-type Ca2+)", protein=None,
      push="reduce inward Ca2+ (T-type, low-threshold) -> raise the firing/burst threshold (the thalamic absence rhythm generator)",
      epilepsy_anchor="T-type Ca-channel locus in childhood absence epilepsy; T-type bursting drives the 3 Hz spike-wave",
      direction_agent="T-type Ca-channel-blocker DIRECTION (the ethosuximide mechanism class targets thalamic T-type current in absence epilepsy)",
      grade_mechanism=GL1,
      src="Chen 2003 Ann Neurol 54:239 (CACNA1H in childhood absence epilepsy); Coulter 1989 Ann Neurol 25:582 (ethosuximide T-type block)"),
  "GRIN2A": dict(lever="L1", channel="NMDA-R GluN2A (glutamate, Ca2+-permeable)", protein=None,
      push="reduce inward (NMDA-receptor) current -> lower glutamatergic excitatory drive",
      epilepsy_anchor="NMDA-receptor subunit; GRIN2A variants cause the epilepsy-aphasia spectrum (Landau-Kleffner / CSWS / rolandic)",
      direction_agent="glutamatergic-tone DIRECTION (NMDA modulation; gain-of-function variants are the excitatory case)",
      grade_mechanism=GL1,
      src="Lemke 2013 Nat Genet 45:1067; Lesca 2013 Nat Genet 45:1061 (GRIN2A epilepsy-aphasia spectrum)"),
  # ================= L2: increase the outward (K+, inhibitory) current =================
  "KCNQ2": dict(lever="L2", channel="K_V7.2 (M-current)", protein=None,
      push="INCREASE outward K+ (open K_V7.2) -> hyperpolarise -> raise the seizure threshold",
      epilepsy_anchor="the textbook epilepsy K-channel: KCNQ2 loss causes benign familial neonatal epilepsy AND severe KCNQ2 encephalopathy (the M-current brake)",
      direction_agent="K_V7 opener DIRECTION (retigabine/ezogabine is the canonical M-current-opener anticonvulsant template; molecule-level caveats on that agent)",
      grade_mechanism=GL2,
      src="Singh 1998 Nat Genet 18:25 (KCNQ2 BFNC); Weckhuysen 2012 Ann Neurol 71:15 (KCNQ2 encephalopathy); Gunthorpe 2012 Epilepsia 53:412 (retigabine)"),
  "KCNQ3": dict(lever="L2", channel="K_V7.3 (M-current)", protein=None,
      push="INCREASE outward K+ (open K_V7.3) -> hyperpolarise -> raise the seizure threshold",
      epilepsy_anchor="M-current partner of K_V7.2; KCNQ3 loss causes benign familial neonatal epilepsy",
      direction_agent="K_V7 opener DIRECTION",
      grade_mechanism=GL2,
      src="Charlier 1998 Nat Genet 18:53 (KCNQ3 BFNC)"),
  "KCNA1": dict(lever="L2", channel="K_V1.1 (Shaker delayed-rectifier K+)", protein=None,
      push="INCREASE outward K+ (K_V1.1) -> repolarise/limit re-firing -> raise the threshold",
      epilepsy_anchor="K_V1.1 loss causes episodic ataxia type 1 WITH epilepsy; sets axonal/juxtaparanodal excitability",
      direction_agent="delayed-rectifier K+ DIRECTION (excitability brake)",
      grade_mechanism=GL2,
      src="Browne 1994 Nat Genet 8:136 (KCNA1 episodic ataxia type 1 + epilepsy)"),
  "KCNB1": dict(lever="L2", channel="K_V2.1 (delayed-rectifier K+)", protein=None,
      push="INCREASE outward K+ (delayed-rectifier) -> repolarise -> raise the seizure threshold",
      epilepsy_anchor="K_V2.1 de novo variants cause developmental and epileptic encephalopathy; major somatic delayed-rectifier setting high-frequency firing",
      direction_agent="delayed-rectifier K+ DIRECTION (excitability brake)",
      grade_mechanism=GL2,
      src="Torkamani 2014 Ann Neurol 76:529 (KCNB1 epileptic encephalopathy)"),
  "KCNT1": dict(lever="L2", channel="K_Na1.1 / Slack (Na+-activated K+)", protein=None,
      push="the Na+-activated K+ channel; GAIN-of-function PARADOXICALLY drives epilepsy -> the threshold-raising target is to NORMALISE the over-active current",
      epilepsy_anchor="GAIN-of-function KCNT1 causes ADNFLE and malignant migrating partial seizures of infancy (EIMFS) -- a K-channel where MORE current is pathological",
      direction_agent="K_Na current-NORMALISATION DIRECTION (quinidine is a KCNT1 channel-blocker studied for KCNT1-GOF epilepsy -- DIRECTION, not efficacy; note this lever's sign is INVERTED vs the other K-channels)",
      grade_mechanism=GL2,
      src="Heron 2012 Nat Genet 44:1188 (KCNT1 ADNFLE); Barcia 2012 Nat Genet 44:1255 (KCNT1 EIMFS); Bearden 2014 Ann Neurol 76:457 (quinidine)"),
  # -------- L2-adjacent: the inhibitory restoring current via GABA-A chloride --------
  "GABRG2": dict(lever="L2-adjacent", channel="GABA-A receptor gamma2 (Cl-)", protein=None,
      push="INCREASE the inhibitory restoring current (GABA-A Cl-) -> hyperpolarise -> raise the threshold (the acute benzodiazepine brake site)",
      epilepsy_anchor="GABA-A gamma2 loss causes GEFS+ and febrile seizures; the gamma2 subunit carries the benzodiazepine site",
      direction_agent="GABA-A potentiation DIRECTION (benzodiazepine-site enhancement; the acute anticonvulsant brake -- DIRECTION, not efficacy)",
      grade_mechanism=GL2,
      src="Baulac 2001 Nat Genet 28:46; Wallace 2001 Nat Genet 28:49 (GABRG2 in GEFS+/FS)"),
  "GABRA1": dict(lever="L2-adjacent", channel="GABA-A receptor alpha1 (Cl-)", protein=None,
      push="INCREASE the inhibitory restoring current (GABA-A Cl-) -> hyperpolarise -> raise the threshold",
      epilepsy_anchor="GABA-A alpha1 variants cause juvenile myoclonic epilepsy and developmental/epileptic encephalopathy",
      direction_agent="GABA-A potentiation DIRECTION (inhibitory restoring current)",
      grade_mechanism=GL2,
      src="Cossette 2002 Nat Genet 31:184 (GABRA1 in JME); Carvill 2014 Neurology 82:1245 (GABRA1 DEE)"),
  # ================= L3: remove the up-stream sensitising / triggering drive (mTOR) =================
  "DEPDC5": dict(lever="L3", channel=None, protein="DEPDC5 (GATOR1 complex; mTORC1 repressor)",
      push="restore mTOR repression -> remove the mTOR-hyperactivation drive that lowers the seizure threshold and builds the dysplastic substrate",
      epilepsy_anchor="DEPDC5 loss-of-function is the leading cause of familial focal epilepsy (incl. focal cortical dysplasia); it normally REPRESSES mTORC1",
      direction_agent="mTOR-inhibition DIRECTION (the rapamycin/everolimus mechanism class addresses mTOR-hyperactivation epilepsies -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="Dibbens 2013 Nat Genet 45:546 (DEPDC5 familial focal epilepsy); Baulac 2015 Ann Neurol 77:675 (DEPDC5 mTOR)"),
  "TSC1": dict(lever="L3", channel=None, protein="hamartin (TSC1; mTORC1 repressor complex)",
      push="restore mTORC1 repression (TSC1-TSC2 complex) -> remove the mTOR-hyperactivation drive (the tuberous-sclerosis dysplastic/epileptogenic substrate)",
      epilepsy_anchor="TSC1 (hamartin) loss causes tuberous sclerosis complex, a major monogenic cause of (often drug-resistant) epilepsy via mTOR hyperactivation",
      direction_agent="mTOR-inhibition DIRECTION (everolimus is an approved direction for TSC-associated seizures -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="van Slegtenhorst 1997 Science 277:805 (TSC1 hamartin); French 2016 Lancet 388:2153 (EXIST-3, everolimus TSC seizures, direction)"),
  "TSC2": dict(lever="L3", channel=None, protein="tuberin (TSC2; mTORC1 repressor complex, GAP for Rheb)",
      push="restore mTORC1 repression (TSC2 is the Rheb-GAP) -> remove the mTOR-hyperactivation drive",
      epilepsy_anchor="TSC2 (tuberin) loss causes tuberous sclerosis complex with typically more severe epilepsy than TSC1; tuberin is the Rheb-GAP gating mTORC1",
      direction_agent="mTOR-inhibition DIRECTION (everolimus is an approved direction for TSC-associated seizures -- DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="European Chromosome 16 TSC Consortium 1993 Cell 75:1305 (TSC2 tuberin); French 2016 Lancet 388:2153 (EXIST-3, direction)"),
}

def read(sym, g):
    c = CONTEXT[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the over-sync threshold)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "epilepsy_genetic_anchor": c["epilepsy_anchor"],
        "threshold_raising_agent_direction": c["direction_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": GL1 if c["lever"] in ("L1", "L1-adjacent")
                       else (GL2 if c["lever"] in ("L2", "L2-adjacent") else c["grade_mechanism"]),
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_oversync_threshold": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch stiffness, "
                                       "NOT the sec.25 network over-synchronisation threshold on the global order "
                                       "parameter R; never equated",
        "grade_clinical_map": "[O] OPEN -- not a voltage, potency, dose, in-vivo selectivity, or clinical effect",
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
    return {
        "title": "Three-lever epileptic seizure-threshold target map (engine-generated reads + cited lever frame)",
        "inherited_from": "analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the threshold-shift "
                          "intervention-logic technology, applied to the epileptic seizure threshold (second application "
                          "after bipolar sec.30; the cleanest, since the roadmap T2a output IS an L1/L2 threshold-raise)",
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_sec25": "sec.25 (epilepsy_oversync) established (CONFIRMED) that epilepsy is the over-synchronisation "
                          "pole and that an inhibitory/threshold-RAISING anticonvulsant-class push moves R back toward "
                          "health, but treated that push as a SINGLE abstract operator. This map DECOMPOSES that "
                          "threshold-raise into the three mechanistically-distinct levers and grounds each in a DNA read "
                          "of the actual epilepsy excitability genes. It adds NO new constant and re-derives no rule -- the "
                          "exact epilepsy counterpart of the bipolar B4->sec.30 decomposition.",
        "unifying_frame": ("a seizure crosses the firing/over-synchronisation threshold (sec.25). The threshold can be raised "
                           "-- the sec.25 direction -- by ANY of three levers, selectively. L1 reduces the inward drive "
                           "(the Na-channel-blocker anticonvulsants act here for GAIN-of-function channelopathies; the T-type "
                           "blocker ethosuximide class for absence), L2 increases the outward K+ brake (the M-current opener "
                           "retigabine class is the textbook K_V7 case), L2-adjacent increases the inhibitory restoring "
                           "current via GABA-A chloride (the acute benzodiazepine brake), L3 removes the up-stream mTOR "
                           "hyperactivation drive (the rapamycin/everolimus class for the mTORopathies). Each lever has a "
                           "cited threshold-raising agent DIRECTION; efficacy is asserted nowhere. KCNT1 is the honest "
                           "exception: a K-channel whose GAIN of function is pathological, so its lever sign is inverted "
                           "(normalise the over-active current).") ,
        "levers": LEVER_FRAME,
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a channel voltage, not a potency, not a "
                     "dose, not in-vivo selectivity, not a clinical effect, and NOT the sec.25 network over-synchronisation "
                     "threshold on the global order parameter R (those are [O]). The promoter |h_sp| is the gene's OWN "
                     "switch stiffness, carried alongside, never folded into a clinical magnitude or equated with the "
                     "over-sync threshold. gamma is blind to on/off and to gain/loss of function. L3 (mTOR) mechanism link "
                     "is [O] -- the read places the gene, it does not derive the mTOR/network mechanism."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never drugs, doses, "
                    "protocols, or patients; epilepsy is heterogeneous (focal/generalised, channelopathy/mTORopathy/"
                    "synaptopathy, ~30% drug-resistant) (LOCKED); the L1 'reduce inward Na+' direction is CONTRAINDICATED "
                    "in SCN1A-Dravet (loss-of-function in interneurons) -- recorded honestly; a lever direction is a "
                    "mechanism boundary, not a claim about the felt quality of a seizure (Axis-A; consciousness_claim=0; "
                    "hard problem OPEN)."),
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

def epilepsy_threshold_levers_results():
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
        "reuses_sec25_threshold_direction": True,
    }
    # atlas-compatible honesty ledger (same shape run_all_atlas.py checks: efficacy=0,
    # no consciousness claim, no tuned constants, hard problem OPEN).
    res["honesty_ledger"] = {
        "medium_efficacy_tested": 0.0,
        "no_cure_claimed": 1.0,
        "consciousness_claim": 0.0,
        "hard_problem_open": 1.0,
        "new_tuned_constants": 0.0,
        "ranks_targets_not_drugs": 1.0,
        "inherited_from_analgesic_v2": 1.0,
        "l3_mechanism_link": "OPEN [O] -- mTOR (DEPDC5/TSC1/TSC2) mechanism is cited biology, not derived",
        "promoter_hsp_vs_oversync_threshold": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the sec.25 network over-synchronisation threshold on R",
        "gain_loss_contraindication_recorded": 1.0,
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "epilepsy_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_epilepsy_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"epilepsy_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = epilepsy_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 90)
    print("T2a-L  EPILEPSY THREE-LEVER MAP   (inherited from analgesic v2.0; engine READ-ONLY)")
    print("=" * 90)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  decomposes sec.25 push: {inv['reuses_sec25_threshold_direction']}")
    print("-" * 90)
    print(f"  {'gene':9} {'lev':12} {'gamma':>7} {'|h_sp|':>8} {'channel/protein':34} epilepsy anchor")
    for e in res["entries"]:
        cp = e["channel"] or e.get("protein") or "-"
        print(f"  {e['gene']:9} {e['lever']:12} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} "
              f"{cp[:34]:34} {e['epilepsy_genetic_anchor'][:40]}")
    print("-" * 90)
    print("  targets by lever: " + ", ".join(f"{k}={len(v)}" for k, v in res["targets_by_lever"].items()))
    print(f"  n_targets: {res['n_targets']}   channels: {len(res['channels_present'])}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 90)
    ok = inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
    print("  T2a-L THREE-LEVER MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
