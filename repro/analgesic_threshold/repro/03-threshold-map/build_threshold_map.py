#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_threshold_map.py  —  M9 (v2): the THREE-LEVER nociceptor threshold map.

v1.0 read one lever (block the inward depolarising current). v2 generalises the map to the
unifying frame: the nociceptor's firing threshold |h_sp| can be raised from THREE directions —
  L1  reduce the inward (excitatory) current      (block depolarising channels)
  L2  increase the outward (K+, inhibitory) current (open hyperpolarising channels)
  L3  remove the up-stream sensitising drive       (block the signal that LOWERED the threshold)
The engine reads, on one scale, the promoter switch-threshold STRUCTURE of the genes behind all
three. For every target the map carries: lever, push direction, channel/protein, selectivity tier
(cited), burden tier (cited), and the [V]/[F]/[O] grades.

HONESTY (binding, Axis-A analgesic):
  - gamma / spinodal |h_sp| / barrier are the engine's READ of the locus' promoter
    switch-threshold structure. They are [V] (reproducible); their ORDER is [F] (forced).
  - This is NOT a channel activation voltage, NOT a drug potency, NOT a dose, NOT a clinical
    effect. Any such mapping is Layer-2 and [O] — never asserted here.
  - lever + push direction are [F] structural, anchored to the CITED validated agents.
  - selectivity_tier / burden_tier / src are CITED Layer-2 biology (not engine outputs).
  - L3 (NGF/CGRP) mechanism link is [O]: the gamma read places the gene in the lever map but
    does NOT derive the receptor/network mechanism (enforced by M11).

No tuning: spinodal/barrier are the locked R19 forms; gamma is measured.

Run:    python3 build_threshold_map.py   -> expected/threshold_map.json
"""
import os, sys, json

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
INHER  = os.path.normpath(os.path.join(HERE, "..", "_inherited_data"))
NAV    = os.path.normpath(os.path.join(HERE, "..", "02-read-nav-channels"))
sys.path.insert(0, ENGINE)
import vp_neuro_engine as VN   # spinodal(g), barrier(g) — locked R19 forms

# --- gather every target gamma read (5 inherited nociceptor + all v2 fetched) ---
inher = json.load(open(os.path.join(INHER, "full_sensory_gamma.json")))["genes"]
nav   = json.load(open(os.path.join(NAV, "nav_channels_gamma.json")))["genes"]

GAMMA = {
    "PRDM12": inher["PRDM12"]["gamma"], "NTRK1": inher["NTRK1"]["gamma"],
    "SCN9A":  inher["SCN9A"]["gamma"],  "TRPV1": inher["TRPV1"]["gamma"],
    "TRPA1":  inher["TRPA1"]["gamma"],
}
GAMMA.update({s: nav[s]["gamma"] for s in nav})   # all fetched targets

# CITED Layer-2 context (NOT engine output) — source-tagged, carried for map + prioritisation.
# lever: L1 reduce-inward / L2 increase-K-outward / L3 remove-sensitising-drive / master / context.
L1 = "[F] structural: peripheral current block raises the firing threshold (anchored to cited agents)"
L2 = "[F] structural: open K_V7 -> hyperpolarise -> raise threshold (anchored to retigabine/flupirtine template)"
L3 = "[O] cited biology: gamma places the gene in the lever map; the receptor/network mechanism is NOT derived"
LM = "[O] developmental role cited (master TF; not an acute mechanism)"
LC = "[O] comparator only: read for contrast; NOT a recommended target"

CONTEXT = {
  # --- inherited nociceptor reads ---
  "PRDM12": dict(lever="master", push="developmental: specifies the nociceptor lineage (not an acute lever)",
                 channel=None, protein="PRDM12 (transcription factor)",
                 selectivity_tier="nociceptor-specific (developmental, not an acute drug target)",
                 burden_tier="cross-cutting (refractory channelopathy anchor)", grade_mechanism=LM,
                 src="Chen 2015 Nat Genet 47:803 (PRDM12 LOF -> congenital insensitivity to pain)"),
  "NTRK1":  dict(lever="L3", push="block the NGF->TrkA sensitising drive",
                 channel=None, protein="TrkA (NGF receptor)",
                 selectivity_tier="nociceptor + some CNS (CIPA on LOF)",
                 burden_tier="Tier-1 musculoskeletal (with NGF)", grade_mechanism=L3,
                 src="Indo 1996 Nat Genet 13:485 (NTRK1 LOF -> CIPA)"),
  "SCN9A":  dict(lever="L1", push="reduce inward Na+ (raise AP threshold at the firing gate)",
                 channel="Na_V1.7",
                 selectivity_tier="nociceptor-enriched (peripheral; +sympathetic/olfactory)",
                 burden_tier="Tier-1 neuropathic + Tier-3 channelopathy", grade_mechanism=L1,
                 src="Cox 2006 Nature 444:894 (LOF->CIP); Drenth 2005 / Estacion 2008 (GOF->IEM/PEPD)"),
  "TRPV1":  dict(lever="L1", push="reduce inward (heat/capsaicin transducer); also nociceptor entry-port (M12)",
                 channel="TRPV1", selectivity_tier="peripheral sensory (also limited CNS)",
                 burden_tier="Tier-2 inflammatory", grade_mechanism=L1,
                 src="Caterina 1997 Nature 389:816 (>43C threshold)"),
  "TRPA1":  dict(lever="L1", push="reduce inward (irritant/cold transducer); also nociceptor entry-port (M12)",
                 channel="TRPA1", selectivity_tier="peripheral sensory",
                 burden_tier="Tier-2 inflammatory", grade_mechanism=L1,
                 src="Story 2003 Cell 112:819; Bautista 2006 Cell 124:1269"),
  # --- v1.0 Na_V reads ---
  "SCN10A": dict(lever="L1", push="reduce inward Na+ (TTX-R upstroke); closed-state stabilisation = the realised move",
                 channel="Na_V1.8",
                 selectivity_tier="HIGH nociceptor-selective (DRG); FDA-validated peripheral target",
                 burden_tier="Tier-1 acute/peripheral (realised case)", grade_mechanism=L1,
                 src="Akopian 1996 Nature 379:257; suzetrigine FDA 2025-01-30 (VSD2 closed-state)"),
  "SCN11A": dict(lever="L1", push="reduce inward Na+ (TTX-R subthreshold/resting)",
                 channel="Na_V1.9",
                 selectivity_tier="nociceptor-selective (DRG); hard to express in vitro",
                 burden_tier="Tier-3 channelopathy/neuropathic", grade_mechanism=L1,
                 src="Dib-Hajj 1998 PNAS 95:8963; Huang 2017 (SCN11A pain variants)"),
  # --- new L1 inward-current channels ---
  "SCN3A":  dict(lever="L1", push="reduce inward Na+ (Na_V1.3, re-expressed/up-regulated after nerve injury)",
                 channel="Na_V1.3",
                 selectivity_tier="developmentally regulated; up-regulated in injured DRG/CNS",
                 burden_tier="Tier-1 neuropathic", grade_mechanism=L1,
                 src="Hains 2003 J Neurosci 23:8881 (Na_V1.3 up-regulation after injury)"),
  "CACNA1B":dict(lever="L1", push="reduce inward Ca2+ (N-type presynaptic transmitter release)",
                 channel="Ca_V2.2",
                 selectivity_tier="presynaptic DRG terminal (dorsal horn); ziconotide target",
                 burden_tier="Tier-3 severe/refractory (intrathecal)", grade_mechanism=L1,
                 src="ziconotide (Prialt) FDA 2004; Snutch 2005 NeuroRx 2:662"),
  "CACNA1H":dict(lever="L1", push="reduce inward Ca2+ (T-type, low-threshold)",
                 channel="Ca_V3.2",
                 selectivity_tier="DRG T-type; up-regulated in neuropathy",
                 burden_tier="Tier-1 neuropathic", grade_mechanism=L1,
                 src="Bourinet 2005 EMBO J 24:315 (Ca_V3.2 in nociception)"),
  "CACNA2D1":dict(lever="L1-adjacent", push="reduce inward Ca2+ via alpha2delta-1 (gabapentinoid target)",
                 channel="alpha2delta-1 (Ca_V auxiliary subunit)",
                 selectivity_tier="up-regulated in injured DRG; gabapentin/pregabalin target",
                 burden_tier="Tier-1 neuropathic + adjuvant (among most-prescribed)", grade_mechanism=L1,
                 src="Field 2006 PNAS 103:17537 (alpha2delta-1 is the gabapentinoid target)"),
  "TRPM8":  dict(lever="L1", push="reduce/modulate inward (cold/menthol transducer)",
                 channel="TRPM8",
                 selectivity_tier="cold-sensing C/Adelta; analgesic in human cold-pain (no core-temp change)",
                 burden_tier="Tier-2 cold allodynia; migraine-linked", grade_mechanism=L1,
                 src="Bautista 2007 Nature 448:204; Pfizer PF-05105679 human cold-pain trial"),
  "P2RX3":  dict(lever="L1", push="reduce inward (ATP-gated, ligand-gated)",
                 channel="P2X3",
                 selectivity_tier="nociceptor-restricted (DRG); gefapixant lineage",
                 burden_tier="Tier-2 visceral/chronic-cough", grade_mechanism=L1,
                 src="Cockayne 2000 Nature 407:1011; gefapixant program"),
  "ASIC1":  dict(lever="L1", push="reduce inward (proton-gated)",
                 channel="ASIC1",
                 selectivity_tier="acid-sensing (CNS + peripheral)",
                 burden_tier="Tier-2 inflammatory/ischaemic", grade_mechanism=L1,
                 src="Waldmann 1997 Nature 386:173; Wemmie 2013 Nat Rev Neurosci 14:461"),
  "ASIC3":  dict(lever="L1", push="reduce inward (proton-gated)",
                 channel="ASIC3",
                 selectivity_tier="DRG-enriched acid sensor (muscle/cardiac afferents)",
                 burden_tier="Tier-2 inflammatory/muscle", grade_mechanism=L1,
                 src="Sutherland 2001 PNAS 98:711 (ASIC3 in muscle nociception)"),
  # --- new L2 outward (K+) channels ---
  "KCNQ2":  dict(lever="L2", push="INCREASE outward K+ (open K_V7.2; hyperpolarise away from threshold)",
                 channel="K_V7.2",
                 selectivity_tier="M-current; retigabine/flupirtine template (clinical caveats on those molecules)",
                 burden_tier="Tier-1 neuropathic (excitability)", grade_mechanism=L2,
                 src="Wang 1998 Science 282:1890; Brown 2009 J Physiol 587:1815 (M-current)"),
  "KCNQ3":  dict(lever="L2", push="INCREASE outward K+ (open K_V7.3; hyperpolarise away from threshold)",
                 channel="K_V7.3",
                 selectivity_tier="M-current partner of K_V7.2",
                 burden_tier="Tier-1 neuropathic (excitability)", grade_mechanism=L2,
                 src="Wang 1998 Science 282:1890"),
  "KCNQ5":  dict(lever="L2", push="INCREASE outward K+ (open K_V7.5; hyperpolarise away from threshold)",
                 channel="K_V7.5",
                 selectivity_tier="DRG/peripheral M-current component",
                 burden_tier="Tier-1 neuropathic (excitability)", grade_mechanism=L2,
                 src="Lerche 2000 J Biol Chem 275:22395; Tzingounis 2010 PNAS 107:10232"),
  # --- new L3 sensitising-drive axes (mechanism link [O]) ---
  "NGF":    dict(lever="L3", push="block the NGF->TrkA sensitising drive (anti-NGF)",
                 channel=None, protein="NGF (nerve growth factor, ligand)",
                 selectivity_tier="peripheral sensitiser; anti-NGF efficacy in OA/LBP (rapidly-progressive-OA caveat)",
                 burden_tier="Tier-1 musculoskeletal (#1 disability burden)", grade_mechanism=L3,
                 src="Lane 2010 NEJM 363:1521 (tanezumab OA); anti-NGF Phase-III programme"),
  "CALCA":  dict(lever="L3", push="block the CGRP sensitising drive (alpha-CGRP ligand)",
                 channel=None, protein="alpha-CGRP (ligand)",
                 selectivity_tier="trigeminovascular; de-risked axis (gepants + anti-CGRP mAbs approved)",
                 burden_tier="Tier-1 migraine (~1 billion people)", grade_mechanism=L3,
                 src="Edvinsson 2018 Nat Rev Neurol 14:338; gepant / anti-CGRP approvals"),
  "CALCB":  dict(lever="L3", push="block the CGRP sensitising drive (beta-CGRP ligand)",
                 channel=None, protein="beta-CGRP (ligand)",
                 selectivity_tier="CGRP isoform (trigeminal/enteric)",
                 burden_tier="Tier-1 migraine", grade_mechanism=L3,
                 src="Russell 2014 Physiol Rev 94:1099 (CGRP physiology)"),
  "CALCRL": dict(lever="L3", push="block CGRP receptor signalling (CLR receptor component)",
                 channel=None, protein="CALCRL (calcitonin-receptor-like receptor)",
                 selectivity_tier="with RAMP1 forms the CGRP receptor; erenumab/gepant target",
                 burden_tier="Tier-1 migraine", grade_mechanism=L3,
                 src="McLatchie 1998 Nature 393:333 (RAMP1 + CLR = CGRP receptor)"),
  "RAMP1":  dict(lever="L3", push="block CGRP receptor signalling (RAMP specificity component)",
                 channel=None, protein="RAMP1 (receptor-activity-modifying protein 1)",
                 selectivity_tier="confers CGRP specificity on CLR",
                 burden_tier="Tier-1 migraine", grade_mechanism=L3,
                 src="McLatchie 1998 Nature 393:333"),
  # --- context / comparators (read for contrast only) ---
  "OPRM1":  dict(lever="context", push="comparator: mu-opioid — the REWARD-engaging axis the logic routes AWAY from",
                 channel=None, protein="mu-opioid receptor",
                 selectivity_tier="central reward + analgesia (addiction/respiratory liability)",
                 burden_tier="(comparator only — not a recommended target)", grade_mechanism=LC,
                 src="Matthes 1996 Nature 383:819 (mu-receptor mediates morphine reward + analgesia)"),
  "OPRK1":  dict(lever="context", push="comparator: peripheral kappa — a non-reward analgesia direction (dysphoria caveat)",
                 channel=None, protein="kappa-opioid receptor",
                 selectivity_tier="peripheral kappa (centrally-restricted dysphoria caveat)",
                 burden_tier="(comparator)", grade_mechanism=LC,
                 src="Stein 2013 Nat Med 19:1448 (peripheral opioid analgesia)"),
  "OPRD1":  dict(lever="context", push="comparator: delta-opioid",
                 channel=None, protein="delta-opioid receptor",
                 selectivity_tier="peripheral/central delta",
                 burden_tier="(comparator)", grade_mechanism=LC,
                 src="Gaveriaux-Ruff 2011 Br J Pharmacol 163:1117"),
  "CNR2":   dict(lever="context", push="comparator: peripheral CB2 — a non-psychoactive direction",
                 channel=None, protein="CB2 cannabinoid receptor",
                 selectivity_tier="peripheral/immune CB2 (non-psychoactive)",
                 burden_tier="(comparator)", grade_mechanism=LC,
                 src="Guindon 2008 Br J Pharmacol 153:319 (CB2 analgesia)"),
}

LEVER_FRAME = {
  "L1": "reduce the inward (excitatory) current — block depolarising channels; removes the drive that crosses threshold",
  "L2": "increase the outward (K+, inhibitory) current — open hyperpolarising channels; pulls V_m away from threshold",
  "L3": "remove the up-stream sensitising drive — block the signal that LOWERED the threshold; restores the resting threshold",
}

def read(sym):
    g = GAMMA[sym]; c = CONTEXT[sym]
    return {
        "gene": sym,
        "gamma": round(g, 6),                       # [V] read
        "spinodal_h_sp": round(VN.spinodal(g), 6),  # [V] R19 threshold scale
        "barrier": round(VN.barrier(g), 6),         # [V] R19 basin depth
        "lever": c["lever"],
        "push_direction": c["push"],
        "channel": c.get("channel"),
        "protein": c.get("protein"),
        "selectivity_tier": c["selectivity_tier"],
        "burden_tier": c["burden_tier"],
        "grade_read": "[V] reproducible promoter-switch-threshold read",
        "grade_order": "[F] forced by reads",
        "grade_lever": "[F] structural lever + direction (anchored to cited agents)"
                       if c["lever"] in ("L1", "L2", "L1-adjacent")
                       else c["grade_mechanism"],
        "grade_mechanism": c["grade_mechanism"],
        "grade_clinical_map": "[O] OPEN — not a voltage, potency, dose, selectivity-in-vivo, or effect",
        "context_grade": "CITED Layer-2 biology (not an engine output)",
        "src": c["src"],
    }

def build():
    entries = [read(s) for s in GAMMA]
    entries.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)   # stiffest gate first [F]
    order = [e["gene"] for e in entries]
    by_lever = {}
    for e in entries:
        by_lever.setdefault(e["lever"], []).append(e["gene"])
    return {
        "title": "Three-lever nociceptor threshold map (engine-generated reads + cited lever frame)",
        "primitive": "gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=(2/3sqrt3)gamma^1.5, barrier=gamma^2/4",
        "unifying_frame": ("analgesia = raise the nociceptor firing threshold |h_sp|, by ANY of three levers, "
                           "selectively. v1.0's Na_V work is the L1 prototype; approved K_V7 (L2) and "
                           "CGRP/NGF (L3) agents validate the other two directions."),
        "levers": LEVER_FRAME,
        "firewall": ("READS the promoter switch-threshold STRUCTURE only. Not channel voltage, not potency, "
                     "not dose, not in-vivo selectivity, not clinical effect (those are [O]). gamma is blind to on/off. "
                     "L3 (NGF/CGRP) mechanism link is [O] — the read places the gene, it does not derive the receptor/network."),
        "n_targets": len(entries),
        "order_by_spinodal_desc": order,
        "targets_by_lever": by_lever,
        "channels_present": sorted({e["channel"] for e in entries if e["channel"]}),
        "entries": entries,
    }

if __name__ == "__main__":
    m = build()
    json.dump(m, open(os.path.join(HERE, "expected", "threshold_map.json"), "w"), indent=1)
    print("M9 three-lever threshold map (order by spinodal |h_sp|, stiffest gate first):")
    print(f"  {'gene':9} {'lev':10} {'gamma':>7} {'|h_sp|':>8} {'barrier':>8}  {'channel/protein':22} selectivity")
    for e in m["entries"]:
        cp = e["channel"] or e.get("protein") or "-"
        print(f"  {e['gene']:9} {e['lever']:10} {e['gamma']:7.4f} {e['spinodal_h_sp']:8.4f} {e['barrier']:8.4f}  "
              f"{cp[:22]:22} {e['selectivity_tier'][:42]}")
    print(f"  targets by lever: " + ", ".join(f"{k}={len(v)}" for k, v in m["targets_by_lever"].items()))
    print(f"wrote expected/threshold_map.json  ({m['n_targets']} targets; channels: {len(m['channels_present'])})")
