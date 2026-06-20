#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bipolar_threshold_levers.py  —  T2b-L (sec.30): the THREE-LEVER target map for the bipolar mood
switch. This is the analgesic_threshold_logic v2.0 technology (DOI 10.5281/zenodo.20733420)
INHERITED into the mind atlas and applied to bipolar disorder. It re-derives no rule: it reads
the SAME R19 substrate (E.spinodal/E.barrier, byte-identical to vp_neuro_engine) and the SAME
gamma = -mean(NN stacking dG, SantaLucia 1998) the engine uses to write genes.

WHY THIS EXISTS (the gap it closes). sec.29 B4 established, CONFIRMED, that a barrier-RAISING
push is the mood-stabiliser DIRECTION: raising the switch fold makes mood-state transitions need
a larger drive, so episodes become less frequent. But B4 treated the stabiliser as a SINGLE,
undifferentiated "barrier-raising operator" -- it never said WHICH genes / channels / mechanisms
realise that barrier-raise. The analgesic three-lever frame supplies exactly that missing layer.

THE UNIFYING FRAME (inherited from analgesic v2.0, applied to mood). The bipolar episode is a
crossing of the R19 mood fold (sec.28/29). The crossing can be made HARDER -- the barrier raised
(the B4 direction) -- from THREE mechanistically-distinct directions, exactly as nociceptor
firing can be raised from three:
  L1  reduce the inward (excitatory) current      (block the depolarising drive across the fold)
  L2  increase the outward (K+, inhibitory) current (hyperpolarise; pull V_m away from the fold)
  L3  remove the up-stream sensitising / triggering drive (circadian + HPA; restore resting fold)
The engine reads, on one scale, the promoter switch-threshold STRUCTURE of the genes behind all
three. For every target the map carries: lever, push direction, channel/protein, the cited
BIPOLAR GENETIC anchor, the cited barrier-raising AGENT DIRECTION (never efficacy), and the
[V]/[F]/[O] grades.

THE FIREWALL (binding, non-negotiable; inherited verbatim in spirit). gamma / spinodal |h_sp| /
barrier are the engine's READ of the locus' promoter switch-threshold STRUCTURE. They are [V]
(reproducible); their ORDER is [F] (forced). This is NOT a channel activation voltage, NOT a drug
potency, NOT a dose, NOT an in-vivo selectivity, NOT a clinical effect, and -- the mood-specific
addition -- the promoter |h_sp| is NOT the network mood-switch barrier g of sec.29 (that is a
separate network quantity). The promoter read is carried ALONGSIDE as the gene's own switch
stiffness; it is NEVER folded into a clinical magnitude or equated with the mood fold. gamma is
blind to on/off (it reads switch structure, not the trait). L3 (circadian/HPA) mechanism link is
[O]: the gamma read PLACES the gene in the lever map; it does NOT derive the receptor/network
mechanism (enforced by bipolar_l3_honesty.py).

HONESTY (binding, Axis-A). MECHANISM-DIRECTION only. efficacy = 0 everywhere. This ranks/places
READS and TARGETS, never drugs, doses, protocols, or patients. NOTHING here says any drug treats
anyone or that any individual should change treatment. Real bipolar disorder is HETEROGENEOUS
(BD-I/II, cyclothymia, mixed, rapid-cycling, seasonal, post-partum; genetic + circadian +
monoaminergic + psychosocial) -- LOCKED. A lever direction is a mechanism boundary, NOT a claim
about the felt quality of mania or depression (consciousness_claim stays 0; hard problem OPEN).

No tuning: gamma is measured (pure arithmetic over called dinucleotide steps); |h_sp|/barrier are
the locked R19 forms; the lever assignments and citations are CITED Layer-2 biology, not engine
outputs. Governed by VP_SPEC_v1_8 (SEED=19). Engine imported READ-ONLY (tree 0fbf4988...).

Run:  python3 bipolar_threshold_levers.py
Out:  bipolar_threshold_levers_results.json  + its sha256 (2x deterministic)
"""
import os, sys, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY; provides spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4, emerge_all

HERE  = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "bipolar_levers_promoters.cache.json")
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

# ---- lever-frame text (inherited from analgesic v2.0, re-pointed at the mood fold) ----
LEVER_FRAME = {
  "L1": "reduce the inward (excitatory) current -- block the depolarising drive that crosses the "
        "mood-switch fold (raises the barrier the B4 way, from the inward side)",
  "L2": "increase the outward (K+, inhibitory) current -- hyperpolarise, pulling V_m away from the "
        "fold (raises the barrier the B4 way, from the outward side)",
  "L3": "remove the up-stream sensitising / triggering drive (circadian + HPA) -- restore the "
        "resting fold (raises the barrier the B4 way, by removing what LOWERED it); mechanism [O]",
}

# grade strings (inherited discipline)
GL1 = "[F] structural: an inward-current reduction raises the mood-switch barrier (anchored to cited agents)"
GL2 = "[F] structural: an outward-K+ increase hyperpolarises -> raises the barrier (anchored to cited agents)"
GL3 = "[O] cited biology: gamma places the gene in the lever map; the circadian/HPA receptor/network mechanism is NOT derived"

# CITED Layer-2 context (NOT engine output). bipolar_anchor = the cited BD genetics; direction_agent
# = the cited barrier-raising agent DIRECTION (never an efficacy claim). channel/protein labelled.
CONTEXT = {
  # ================= L1: reduce the inward (excitatory) current =================
  "CACNA1C": dict(lever="L1", channel="Ca_V1.2 (L-type Ca2+)", protein=None,
      push="reduce inward Ca2+ (L-type) -> lower the depolarising drive across the mood fold",
      bipolar_anchor="the single most-replicated bipolar GWAS locus; also the lead cross-disorder Ca-channel signal",
      direction_agent="L-type Ca-channel-blocker DIRECTION (verapamil/nimodipine studied in BD as a direction, NOT efficacy)",
      grade_mechanism=GL1,
      src="Ferreira 2008 Nat Genet 40:1056; Sklar 2011 Nat Genet 43:977 (PGC-BD); Cross-Disorder Group PGC 2013 Lancet 381:1371"),
  "CACNA1D": dict(lever="L1", channel="Ca_V1.3 (L-type Ca2+)", protein=None,
      push="reduce inward Ca2+ (L-type, low-threshold pacemaking component)",
      bipolar_anchor="L-type Ca-channel family implicated across the cross-disorder Ca-signal (BD/SCZ/MDD/ASD/ADHD)",
      direction_agent="L-type Ca-channel-blocker DIRECTION",
      grade_mechanism=GL1,
      src="Cross-Disorder Group PGC 2013 Lancet 381:1371 (cross-disorder L-type Ca signal)"),
  "CACNB2": dict(lever="L1-adjacent", channel="Ca_V beta2 (auxiliary Ca2+ subunit)", protein=None,
      push="reduce inward Ca2+ via the beta2 auxiliary subunit (sets Ca_V trafficking/gating)",
      bipolar_anchor="cross-disorder GWAS hit alongside CACNA1C across five psychiatric disorders",
      direction_agent="L-type Ca-channel-complex DIRECTION (auxiliary subunit of the CACNA1C target)",
      grade_mechanism=GL1,
      src="Cross-Disorder Group PGC 2013 Lancet 381:1371 (CACNA1C + CACNB2 cross five disorders)"),
  "CACNA1I": dict(lever="L1", channel="Ca_V3.3 (T-type Ca2+)", protein=None,
      push="reduce inward Ca2+ (T-type, low-threshold) -> raise the firing/switch threshold",
      bipolar_anchor="T-type Ca-channel locus in the schizophrenia/bipolar GWAS overlap",
      direction_agent="T-type Ca-channel-blocker DIRECTION",
      grade_mechanism=GL1,
      src="Schizophrenia Working Group PGC 2014 Nature 511:421 (CACNA1I among genome-wide loci)"),
  "SCN2A": dict(lever="L1", channel="Na_V1.2 (voltage-gated Na+)", protein=None,
      push="reduce inward Na+ (axonal/somatic upstroke) -> raise the AP threshold at the firing gate",
      bipolar_anchor="neuropsychiatric Na-channel gene (ASD/epilepsy/BD risk); the voltage-gated Na current is the Na-stabiliser effector",
      direction_agent="voltage-gated Na-channel-blocker DIRECTION (the lamotrigine/valproate/carbamazepine class acts on this current)",
      grade_mechanism=GL1,
      src="Sanders 2012 Nature 485:237 (SCN2A neuropsychiatric); Na-blocker anticonvulsant-stabiliser pharmacology"),
  "GRIN2A": dict(lever="L1", channel="NMDA-R GluN2A (glutamate, Ca2+-permeable)", protein=None,
      push="reduce inward (NMDA-receptor) current -> lower glutamatergic excitatory drive",
      bipolar_anchor="NMDA-receptor subunit in the schizophrenia/bipolar GWAS + exome overlap",
      direction_agent="glutamatergic-tone DIRECTION (NMDA modulation; note ketamine is an NMDA antagonist used in mood -- DIRECTION, not efficacy)",
      grade_mechanism=GL1,
      src="Singh 2022 Nature 604:509 (GRIN2A exome, SCZ); shared mood/psychosis glutamatergic axis"),
  "ANK3": dict(lever="L1-adjacent", channel=None, protein="ankyrin-G (axon-initial-segment Na_V scaffold)",
      push="ankyrin-G clusters Na_V at the axon initial segment -> it SETS where the firing threshold lives",
      bipolar_anchor="the #2 classic bipolar GWAS locus alongside CACNA1C (the AIS-excitability gene)",
      direction_agent="excitability-set-point DIRECTION (AIS Na_V density; not an acute pharmacological target)",
      grade_mechanism=GL1,
      src="Ferreira 2008 Nat Genet 40:1056; Schulze 2009 Mol Psychiatry 14:487 (ANK3 in BD)"),
  # ================= L2: increase the outward (K+, inhibitory) current =================
  "KCNQ2": dict(lever="L2", channel="K_V7.2 (M-current)", protein=None,
      push="INCREASE outward K+ (open K_V7.2) -> hyperpolarise -> raise the switch barrier",
      bipolar_anchor="neuronal M-current (the excitability brake); excitability/mood-relevant K-channel axis",
      direction_agent="K_V7 opener DIRECTION (retigabine/ezogabine template; molecule-level caveats on that agent)",
      grade_mechanism=GL2,
      src="Wang 1998 Science 282:1890; Brown 2009 J Physiol 587:1815 (M-current)"),
  "KCNQ3": dict(lever="L2", channel="K_V7.3 (M-current)", protein=None,
      push="INCREASE outward K+ (open K_V7.3) -> hyperpolarise -> raise the switch barrier",
      bipolar_anchor="M-current partner of K_V7.2",
      direction_agent="K_V7 opener DIRECTION",
      grade_mechanism=GL2,
      src="Wang 1998 Science 282:1890"),
  "KCNB1": dict(lever="L2", channel="K_V2.1 (delayed-rectifier K+)", protein=None,
      push="INCREASE outward K+ (delayed-rectifier) -> repolarise -> raise the switch barrier",
      bipolar_anchor="major somatic delayed-rectifier setting neuronal excitability and high-frequency firing",
      direction_agent="delayed-rectifier K+ DIRECTION (excitability brake)",
      grade_mechanism=GL2,
      src="Murakoshi 1999 J Neurosci 19:1728 (K_V2.1 sets excitability)"),
  # ================= L3: remove the up-stream sensitising / triggering drive (circadian + HPA) =================
  "ARNTL": dict(lever="L3", channel=None, protein="BMAL1 (core circadian clock TF)",
      push="restore the circadian gate -> remove the clock-disruption drive that triggers episodes",
      bipolar_anchor="core clock gene; circadian disruption is a cited bipolar episode trigger",
      direction_agent="circadian-stabilisation DIRECTION (chronotherapy/light/sleep regularisation; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="McClung 2007 Pharmacol Ther 114:222; Mansour 2006 Genes Brain Behav 5:150 (clock genes in BD)"),
  "CLOCK": dict(lever="L3", channel=None, protein="CLOCK (core circadian clock TF)",
      push="restore the circadian gate -> remove the clock-disruption drive",
      bipolar_anchor="Clock-Delta19 mouse shows a mania-like phenotype rescued by lithium (a direction-level animal anchor)",
      direction_agent="circadian-stabilisation DIRECTION",
      grade_mechanism=GL3,
      src="Roybal 2007 PNAS 104:6406 (Clock-Delta19 mania-like, lithium-rescued)"),
  "PER2": dict(lever="L3", channel=None, protein="PER2 (circadian period protein)",
      push="restore the circadian gate (period component) -> remove the phase-instability drive",
      bipolar_anchor="circadian period gene; lithium lengthens circadian period (a direction-level link)",
      direction_agent="circadian-period-stabilisation DIRECTION",
      grade_mechanism=GL3,
      src="Mansour 2006 Genes Brain Behav 5:150; lithium-period literature (direction only)"),
  "NR3C1": dict(lever="L3", channel=None, protein="glucocorticoid receptor (HPA effector)",
      push="restore HPA set-point -> remove the cortisol/stress sensitising drive (the sec.29 depressive-pole drive)",
      bipolar_anchor="glucocorticoid receptor / HPA dysregulation is a cited mood-episode driver (and the M18 cortisol pole)",
      direction_agent="HPA-normalisation DIRECTION (stress-axis regulation; DIRECTION, not efficacy)",
      grade_mechanism=GL3,
      src="HPA-axis mood literature; this module grounds the M18 cortisol pole (avoid/depressive)"),
  "CRHR1": dict(lever="L3", channel=None, protein="CRF receptor 1 (HPA initiator)",
      push="reduce the CRF/stress drive that initiates the HPA cascade -> remove an episode trigger",
      bipolar_anchor="CRF-receptor-1 sits at the top of the HPA stress cascade implicated in mood episodes",
      direction_agent="stress-axis (CRF) DIRECTION",
      grade_mechanism=GL3,
      src="HPA/CRF stress-axis mood literature (direction only)"),
  "GSK3B": dict(lever="L3", channel=None, protein="GSK-3beta (kinase; lithium's molecular target)",
      push="the node lithium inhibits; sits downstream of circadian + Wnt -- placed in L3, mechanism NOT derived",
      bipolar_anchor="GSK-3beta is lithium's best-characterised direct molecular target (a mechanism-DIRECTION anchor)",
      direction_agent="lithium-class DIRECTION (GSK-3beta inhibition; mechanism [O], efficacy not asserted)",
      grade_mechanism=GL3,
      src="Klein & Melton 1996 PNAS 93:8455; Stambolic 1996 Curr Biol 6:1664 (lithium inhibits GSK-3beta)"),
}

def read(sym, g):
    c = CONTEXT[sym]
    is_struct = c["lever"] in ("L1", "L2", "L1-adjacent")
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(E.spinodal(g), 6),   # [V] R19 promoter threshold scale (NOT the mood fold)
        "barrier": round(E.barrier(g), 6),          # [V] R19 promoter basin depth
        "lever": c["lever"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "bipolar_genetic_anchor": c["bipolar_anchor"],
        "barrier_raising_agent_direction": c["direction_agent"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": GL1 if c["lever"] in ("L1","L1-adjacent")
                       else (GL2 if c["lever"] == "L2" else c["grade_mechanism"]),
        "grade_mechanism": c["grade_mechanism"],
        "grade_promoter_vs_mood_fold": "[O] OPEN -- the promoter |h_sp| is the gene's OWN switch stiffness, "
                                       "NOT the sec.29 network mood-switch barrier g; never equated",
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
        "title": "Three-lever bipolar mood-switch target map (engine-generated reads + cited lever frame)",
        "inherited_from": "analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420) -- the threshold-shift "
                          "intervention-logic technology, applied to the bipolar mood switch",
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=2(g/3)^1.5 == (2/3sqrt3)gamma^1.5, "
                     "barrier=gamma^2/4 -- byte-identical to vp_neuro_engine and to this engine's E.spinodal/E.barrier",
        "connects_to_B4": "sec.29 B4 established (CONFIRMED) that a barrier-RAISING push is the mood-stabiliser "
                          "direction but treated the stabiliser as a SINGLE abstract operator. This map DECOMPOSES "
                          "that barrier-raise into the three mechanistically-distinct levers and grounds each in a "
                          "DNA read of the actual bipolar excitability genes. It adds NO new constant and re-derives "
                          "no rule.",
        "unifying_frame": ("a bipolar episode crosses the R19 mood fold (sec.28/29). The barrier can be raised -- the "
                           "B4 direction -- by ANY of three levers, selectively. L1 reduces the inward drive "
                           "(CACNA1C is the lead bipolar locus; the Na-blocker stabilisers act here), L2 increases "
                           "the outward K+ brake, L3 removes the up-stream circadian/HPA trigger (lithium's GSK-3beta "
                           "/ circadian links sit here). Each lever has a cited barrier-raising agent DIRECTION; "
                           "efficacy is asserted nowhere."),
        "levers": LEVER_FRAME,
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not a channel voltage, not a potency, not a "
                     "dose, not in-vivo selectivity, not a clinical effect, and NOT the sec.29 network mood-switch "
                     "barrier g (those are [O]). The promoter |h_sp| is the gene's OWN switch stiffness, carried "
                     "alongside, never folded into a clinical magnitude or equated with the mood fold. gamma is blind "
                     "to on/off. L3 (circadian/HPA) mechanism link is [O] -- the read places the gene, it does not "
                     "derive the receptor/network."),
        "honesty": ("MECHANISM-DIRECTION only; efficacy=0 everywhere; ranks/places READS and TARGETS, never drugs, "
                    "doses, protocols, or patients; bipolar is heterogeneous (LOCKED); a lever direction is a "
                    "mechanism boundary, not a claim about the felt quality of mania/depression (Axis-A; "
                    "consciousness_claim=0; hard problem OPEN)."),
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

def bipolar_threshold_levers_results():
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
        "reuses_B4_barrier_direction": True,
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
        "l3_mechanism_link": "OPEN [O] -- circadian/HPA/GSK-3beta mechanism is cited biology, not derived",
        "promoter_hsp_vs_mood_fold": "OPEN [O] -- the promoter |h_sp| is the gene's own switch stiffness, "
                                     "never equated with the sec.29 network mood-switch barrier g",
        "efficacy_and_dose": "efficacy=0 everywhere; no dose/protocol; not medical advice; cited agents are "
                             "DIRECTIONS only (the fail-closed forbidden-claim scan enforces this)",
    }
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "bipolar_threshold_levers_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_bipolar_threshold_levers_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"bipolar_threshold_levers_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest

if __name__ == "__main__":
    res, digest = bipolar_threshold_levers_results()
    inv = res["invariants"]
    print("=" * 90)
    print("T2b-L  BIPOLAR THREE-LEVER MAP   (inherited from analgesic v2.0; engine READ-ONLY)")
    print("=" * 90)
    print(f"  engine tree unchanged : {inv['engine_tree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  primitive shared      : {inv['reads_shared_R19_primitive']}   new tuned constants: {not inv['no_new_tuned_constants']}")
    print(f"  decomposes B4 barrier : {inv['reuses_B4_barrier_direction']}")
    print("-" * 90)
    print(f"  {'gene':9} {'lev':12} {'gamma':>7} {'|h_sp|':>8} {'channel/protein':34} bipolar anchor")
    for e in res["entries"]:
        cp = e["channel"] or e.get("protein") or "-"
        print(f"  {e['gene']:9} {e['lever']:12} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} "
              f"{cp[:34]:34} {e['bipolar_genetic_anchor'][:40]}")
    print("-" * 90)
    print("  targets by lever: " + ", ".join(f"{k}={len(v)}" for k, v in res["targets_by_lever"].items()))
    print(f"  n_targets: {res['n_targets']}   channels: {len(res['channels_present'])}   missing: {res['missing_from_cache']}")
    print(f"  RESULT sha256 = {digest}")
    print("=" * 90)
    ok = inv["engine_tree_unchanged"] and inv["no_new_tuned_constants"] and not res["missing_from_cache"]
    print("  T2b-L THREE-LEVER MAP: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
