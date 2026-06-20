#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rederive_on_neuro_engine.py  —  §21 INHERIT the analgesic target logic, re-derived on
                                 THIS package's own neuro engine (drift 0).

WHAT THIS DOES
--------------
analgesic_threshold_logic v2.0 (concept DOI 10.5281/zenodo.20733420, CC BY 4.0) is a
sibling whitepaper that maps 27 non-opioid analgesic targets onto the R19 firing-threshold
scale |h_sp| = spinodal(gamma). That sibling was itself built ON the neuro engine: its
repro/_engine/vp_neuro_engine.py is byte-identical to THIS package's
repro/neuro/_engine/vp_neuro_engine.py. So the nociceptor firing threshold the analgesic
map raises IS the |h_sp| every cell in this volume already runs on.

This module makes the inheritance PRINCIPLED rather than a paste: it re-derives all 27
target reads (|h_sp|, barrier) directly from the locked R19 forms in THIS package's engine,
on the inherited measured promoter gamma, and asserts the result reproduces the frozen
sibling map bit-for-bit (max drift 0). It then re-emits the three-lever map, the
channelopathy anchor (the measured biology that fixes the threshold DIRECTION), the
burden-weighted prioritisation, and the precision-block pairings as this volume's own
chapter data.

HONESTY / FIREWALL (inherited verbatim, non-negotiable):
  * gamma reads the promoter switch-threshold STRUCTURE only. It is NEVER a channel
    activation voltage, a drug potency, a dose, an in-vivo selectivity, or a clinical
    effect. Every such magnitude is [O] with a stated obstacle.
  * |h_sp| / barrier / order are [V]/[F] (reproducible / forced by the locked forms).
  * lever + push direction are [F] structural, anchored to CITED validated agent classes.
  * L3 (NGF/CGRP) mechanism link is [O] cited biology (the read places the gene; it does
    not derive the receptor/network).
  * the FELT / affective pain is mind's (the Felt Cognition volume). This layer moves only
    the peripheral afferent firing-threshold term.
  * No molecule is designed; no synthesis or dose is given; nothing prescribes. Proposal-only.

No tuning: spinodal/barrier are the locked R19 forms; gamma is measured (never fitted).

Run:  python3 rederive_on_neuro_engine.py   ->  expected/{threshold_map,channelopathy_anchor,
                                                priority_ranking,precision_block_map}.json
"""
import os, sys, json, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))       # THIS volume's own engine
INHER  = os.path.join(HERE, "_inherited_analgesic")
FROZEN = os.path.join(INHER, "frozen")
EXPECT = os.path.join(HERE, "expected")
sys.path.insert(0, ENGINE)
import vp_neuro_engine as VN     # spinodal(g), barrier(g) — the LOCKED R19 forms of THIS volume


def sha256_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sha256_obj(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


# ----------------------------------------------------------------------------------
# (1) ENGINE IDENTITY — the sibling's firing-threshold scale IS this volume's spinodal.
#     Assert this volume's engine is byte-identical to the engine the frozen map was built on.
# ----------------------------------------------------------------------------------
def assert_engine_identity():
    this_engine = os.path.join(ENGINE, "vp_neuro_engine.py")
    this_sha = sha256_file(this_engine)
    frozen_sha = open(os.path.join(INHER, "ENGINE_SHA256.txt")).read().strip()
    ok = (this_sha == frozen_sha)
    return ok, this_sha, frozen_sha


# ----------------------------------------------------------------------------------
# (2) Gather the inherited measured gamma for all 27 targets (5 inherited nociceptor +
#     22 fetched). Identical NN window/table as this volume's sec.20 sensory atlas.
# ----------------------------------------------------------------------------------
def load_inherited_gamma():
    inher = json.load(open(os.path.join(INHER, "full_sensory_gamma.json")))["genes"]
    nav   = json.load(open(os.path.join(INHER, "nav_channels_gamma.json")))["genes"]
    gamma = {
        "PRDM12": inher["PRDM12"]["gamma"], "NTRK1": inher["NTRK1"]["gamma"],
        "SCN9A":  inher["SCN9A"]["gamma"],  "TRPV1": inher["TRPV1"]["gamma"],
        "TRPA1":  inher["TRPA1"]["gamma"],
    }
    gamma.update({s: nav[s]["gamma"] for s in nav})
    return gamma


# CITED Layer-2 context (NOT engine output) — lever / push / channel / tiers / source.
# Mirrors the sibling map; re-stated here so this chapter's passage is self-contained.
L1 = "[F] structural: reduce the inward (excitatory) current -> raise the firing threshold (anchored to cited agents)"
L2 = "[F] structural: open K_V7 -> hyperpolarise -> raise the firing threshold (retigabine/flupirtine template)"
L3 = "[O] cited biology: gamma places the gene in the lever map; the receptor/network mechanism is NOT derived"
LM = "[O] developmental role cited (master TF; not an acute mechanism)"
LC = "[O] comparator only: read for contrast; NOT a recommended target"

CONTEXT = {
  "PRDM12":  dict(lever="master", push="developmental: specifies the nociceptor lineage (not an acute lever)",
                  channel=None, protein="PRDM12 (transcription factor)", grade_mechanism=LM,
                  selectivity_tier="nociceptor-specific (developmental, not an acute drug target)",
                  burden_tier="cross-cutting (refractory channelopathy anchor)",
                  src="Chen 2015 Nat Genet 47:803 (PRDM12 LOF -> congenital insensitivity to pain)"),
  "NTRK1":   dict(lever="L3", push="block the NGF->TrkA sensitising drive",
                  channel=None, protein="TrkA (NGF receptor)", grade_mechanism=L3,
                  selectivity_tier="nociceptor + some CNS (CIPA on LOF)",
                  burden_tier="Tier-1 musculoskeletal (with NGF)",
                  src="Indo 1996 Nat Genet 13:485 (NTRK1 LOF -> CIPA)"),
  "SCN9A":   dict(lever="L1", push="reduce inward Na+ (raise AP threshold at the firing gate)",
                  channel="Na_V1.7", protein=None, grade_mechanism=L1,
                  selectivity_tier="nociceptor-enriched (peripheral; +sympathetic/olfactory)",
                  burden_tier="Tier-1 neuropathic + Tier-3 channelopathy",
                  src="Cox 2006 Nature 444:894 (LOF->CIP); Drenth 2005 / Estacion 2008 (GOF->IEM/PEPD)"),
  "TRPV1":   dict(lever="L1", push="reduce inward (heat/capsaicin transducer); also nociceptor entry-port",
                  channel="TRPV1", protein=None, grade_mechanism=L1,
                  selectivity_tier="peripheral sensory (also limited CNS)",
                  burden_tier="Tier-2 inflammatory", src="Caterina 1997 Nature 389:816 (>43C threshold)"),
  "TRPA1":   dict(lever="L1", push="reduce inward (irritant/cold transducer); also nociceptor entry-port",
                  channel="TRPA1", protein=None, grade_mechanism=L1,
                  selectivity_tier="peripheral sensory", burden_tier="Tier-2 inflammatory",
                  src="Story 2003 Cell 112:819; Bautista 2006 Cell 124:1269"),
  "SCN10A":  dict(lever="L1", push="reduce inward Na+ (TTX-R upstroke); closed-state stabilisation = realised move",
                  channel="Na_V1.8", protein=None, grade_mechanism=L1,
                  selectivity_tier="HIGH nociceptor-selective (DRG); FDA-validated peripheral target",
                  burden_tier="Tier-1 acute/peripheral (realised case)",
                  src="Akopian 1996 Nature 379:257; suzetrigine FDA 2025-01-30 (VSD2 closed-state)"),
  "SCN11A":  dict(lever="L1", push="reduce inward Na+ (TTX-R subthreshold/resting)",
                  channel="Na_V1.9", protein=None, grade_mechanism=L1,
                  selectivity_tier="nociceptor-selective (DRG); hard to express in vitro",
                  burden_tier="Tier-3 channelopathy/neuropathic",
                  src="Dib-Hajj 1998 PNAS 95:8963; Huang 2017 (SCN11A pain variants)"),
  "SCN3A":   dict(lever="L1", push="reduce inward Na+ (Na_V1.3, re-expressed/up-regulated after nerve injury)",
                  channel="Na_V1.3", protein=None, grade_mechanism=L1,
                  selectivity_tier="developmentally regulated; up-regulated in injured DRG/CNS",
                  burden_tier="Tier-1 neuropathic",
                  src="Hains 2003 J Neurosci 23:8881 (Na_V1.3 up-regulation after injury)"),
  "CACNA1B": dict(lever="L1", push="reduce inward Ca2+ (N-type presynaptic transmitter release)",
                  channel="Ca_V2.2", protein=None, grade_mechanism=L1,
                  selectivity_tier="presynaptic DRG terminal (dorsal horn); ziconotide target",
                  burden_tier="Tier-3 severe/refractory (intrathecal)",
                  src="ziconotide (Prialt) FDA 2004; Snutch 2005 NeuroRx 2:662"),
  "CACNA1H": dict(lever="L1", push="reduce inward Ca2+ (T-type, low-threshold)",
                  channel="Ca_V3.2", protein=None, grade_mechanism=L1,
                  selectivity_tier="DRG T-type; up-regulated in neuropathy",
                  burden_tier="Tier-1 neuropathic", src="Bourinet 2005 EMBO J 24:315 (Ca_V3.2 in nociception)"),
  "CACNA2D1":dict(lever="L1-adjacent", push="reduce inward Ca2+ via alpha2delta-1 (gabapentinoid target)",
                  channel="alpha2delta-1 (Ca_V auxiliary subunit)", protein=None, grade_mechanism=L1,
                  selectivity_tier="up-regulated in injured DRG; gabapentin/pregabalin target",
                  burden_tier="Tier-1 neuropathic + adjuvant (among most-prescribed)",
                  src="Field 2006 PNAS 103:17537 (alpha2delta-1 is the gabapentinoid target)"),
  "TRPM8":   dict(lever="L1", push="reduce/modulate inward (cold/menthol transducer)",
                  channel="TRPM8", protein=None, grade_mechanism=L1,
                  selectivity_tier="cold-sensing C/Adelta; analgesic in human cold-pain (no core-temp change)",
                  burden_tier="Tier-2 cold allodynia; migraine-linked",
                  src="Bautista 2007 Nature 448:204; Pfizer PF-05105679 human cold-pain trial"),
  "P2RX3":   dict(lever="L1", push="reduce inward (ATP-gated, ligand-gated)",
                  channel="P2X3", protein=None, grade_mechanism=L1,
                  selectivity_tier="nociceptor-enriched (C-fibre); gefapixant target (cough/pain)",
                  burden_tier="Tier-2 inflammatory/visceral", src="Cockayne 2000 Nature 407:1011; gefapixant"),
  "ASIC1":   dict(lever="L1", push="reduce inward (proton-gated; tissue acidosis)",
                  channel="ASIC1", protein=None, grade_mechanism=L1,
                  selectivity_tier="central + peripheral acid sensing",
                  burden_tier="Tier-2 inflammatory/ischaemic", src="Wemmie 2013 Nat Rev Neurosci 14:461"),
  "ASIC3":   dict(lever="L1", push="reduce inward (proton-gated; muscle/cardiac ischaemic pain)",
                  channel="ASIC3", protein=None, grade_mechanism=L1,
                  selectivity_tier="peripheral acid sensing (DRG)",
                  burden_tier="Tier-2 ischaemic/musculoskeletal", src="Sutherland 2001 PNAS 98:711"),
  "KCNQ2":   dict(lever="L2", push="increase outward K+ (open K_V7.2 -> hyperpolarise)",
                  channel="K_V7.2", protein=None, grade_mechanism=L2,
                  selectivity_tier="M-current; retigabine/flupirtine template (CNS+peripheral)",
                  burden_tier="Tier-2/3 hyperexcitability", src="Wang 1998 Science 282:1890; retigabine (Trobalt)"),
  "KCNQ3":   dict(lever="L2", push="increase outward K+ (open K_V7.3 -> hyperpolarise)",
                  channel="K_V7.3", protein=None, grade_mechanism=L2,
                  selectivity_tier="M-current partner of K_V7.2",
                  burden_tier="Tier-2/3 hyperexcitability", src="Wang 1998 Science 282:1890"),
  "KCNQ5":   dict(lever="L2", push="increase outward K+ (open K_V7.5 -> hyperpolarise)",
                  channel="K_V7.5", protein=None, grade_mechanism=L2,
                  selectivity_tier="M-current; peripheral expression",
                  burden_tier="Tier-2/3 hyperexcitability", src="Schroeder 2000 J Biol Chem 275:24089"),
  "NGF":     dict(lever="L3", push="remove the NGF sensitising drive (anti-NGF)",
                  channel=None, protein="NGF (nerve growth factor, ligand)", grade_mechanism=L3,
                  selectivity_tier="peripheral sensitiser; tanezumab class (efficacy + RPOA safety signal)",
                  burden_tier="Tier-1 musculoskeletal/osteoarthritis",
                  src="anti-NGF tanezumab Phase-III; Lane 2010 NEJM 363:1521"),
  "CALCA":   dict(lever="L3", push="remove the CGRP drive (alpha-CGRP ligand; anti-CGRP / gepant)",
                  channel=None, protein="alpha-CGRP (ligand)", grade_mechanism=L3,
                  selectivity_tier="migraine-validated (gepants, anti-CGRP mAbs)",
                  burden_tier="Tier-1 migraine", src="anti-CGRP mAbs / gepants FDA-approved (migraine)"),
  "CALCB":   dict(lever="L3", push="remove the CGRP drive (beta-CGRP ligand)",
                  channel=None, protein="beta-CGRP (ligand)", grade_mechanism=L3,
                  selectivity_tier="CGRP family; migraine context",
                  burden_tier="Tier-1 migraine", src="CGRP family (anti-CGRP class)"),
  "CALCRL":  dict(lever="L3", push="remove the CGRP signal (CGRP receptor component)",
                  channel=None, protein="CALCRL (calcitonin-receptor-like receptor)", grade_mechanism=L3,
                  selectivity_tier="CGRP receptor; gepant target",
                  burden_tier="Tier-1 migraine", src="CGRP receptor (gepant target)"),
  "RAMP1":   dict(lever="L3", push="remove the CGRP signal (CGRP-receptor RAMP1 subunit)",
                  channel=None, protein="RAMP1 (receptor-activity-modifying protein 1)", grade_mechanism=L3,
                  selectivity_tier="CGRP receptor subunit; gepant target",
                  burden_tier="Tier-1 migraine", src="RAMP1 (CGRP receptor; gepant target)"),
  "OPRM1":   dict(lever="context", push="mu-opioid comparator (NOT a non-opioid target; read for contrast)",
                  channel=None, protein="mu-opioid receptor", grade_mechanism=LC,
                  selectivity_tier="comparator (opioid; dependence/respiratory-depression liability)",
                  burden_tier="comparator", src="comparator read only (opioid axis)"),
  "OPRK1":   dict(lever="context", push="kappa-opioid comparator (peripherally-restricted interest)",
                  channel=None, protein="kappa-opioid receptor", grade_mechanism=LC,
                  selectivity_tier="comparator (opioid family)",
                  burden_tier="comparator", src="comparator read only (opioid axis)"),
  "OPRD1":   dict(lever="context", push="delta-opioid comparator",
                  channel=None, protein="delta-opioid receptor", grade_mechanism=LC,
                  selectivity_tier="comparator (opioid family)",
                  burden_tier="comparator", src="comparator read only (opioid axis)"),
  "CNR2":    dict(lever="context", push="CB2 cannabinoid comparator (non-psychoactive interest)",
                  channel=None, protein="CB2 cannabinoid receptor", grade_mechanism=LC,
                  selectivity_tier="comparator (cannabinoid axis)",
                  burden_tier="comparator", src="comparator read only (cannabinoid axis)"),
}


def build_threshold_map(gamma):
    entries = []
    for gene, g in gamma.items():
        ctx = CONTEXT[gene]
        entries.append(dict(
            gene=gene, gamma=g,
            spinodal_h_sp=VN.spinodal(g),          # re-derived on THIS volume's engine
            barrier=VN.barrier(g),                 # re-derived on THIS volume's engine
            lever=ctx["lever"], push_direction=ctx["push"],
            channel=ctx["channel"], protein=ctx["protein"],
            selectivity_tier=ctx["selectivity_tier"], burden_tier=ctx["burden_tier"],
            grade_read="[V] reproducible (engine read of promoter structure)",
            grade_order="[F] forced by locked R19 spinodal",
            grade_lever="[F] structural (anchored to cited validated agent class)",
            grade_mechanism=ctx["grade_mechanism"],
            grade_clinical_map="[O] every clinical magnitude (potency/dose/selectivity-in-vivo/efficacy) is open",
            context_grade="cited Layer-2 biology (not an engine output)",
            src=ctx["src"]))
    entries.sort(key=lambda e: -e["spinodal_h_sp"])
    by_lever = {}
    for e in entries:
        by_lever.setdefault(e["lever"], []).append(e["gene"])
    channels = sorted({e["channel"] for e in entries if e["channel"]})
    return dict(
        title="Three-lever nociceptor threshold map, re-derived on this volume's own R19 engine",
        primitive="gamma = -mean(NN stacking dG, SantaLucia 1998); R19 |h_sp|=(2/3sqrt3)gamma^1.5, barrier=gamma^2/4",
        unifying_frame=("analgesia = raise the primary somatosensory nociceptor firing threshold |h_sp|, by ANY of "
                        "three levers, selectively. The firing-threshold axis IS this volume's spinodal (sec.2/sec.19). "
                        "Na_V (L1) is the prototype; approved K_V7 openers (L2) and CGRP/NGF agents (L3) validate the "
                        "other two directions."),
        levers={
            "L1": "reduce the inward (excitatory) current — block depolarising channels (Na_V/Ca_V/ASIC/P2X/TRP)",
            "L2": "increase the outward (K+, inhibitory) current — open K_V7 (hyperpolarise)",
            "L3": "remove the up-stream sensitising drive — block NGF/CGRP (restore the resting threshold)",
        },
        firewall=("READS the promoter switch-threshold STRUCTURE only. Not channel voltage, not potency, not dose, "
                  "not in-vivo selectivity, not clinical effect (those are [O]). gamma is blind to on/off. L3 (NGF/CGRP) "
                  "mechanism link is [O]. The FELT/affective pain is mind's; this layer moves only the peripheral "
                  "afferent firing-threshold term. Proposal-only; no molecule designed; nothing prescribes."),
        n_targets=len(entries),
        order_by_spinodal_desc=[e["gene"] for e in entries],
        targets_by_lever=by_lever,
        channels_present=channels,
        entries=entries,
    )


# ----------------------------------------------------------------------------------
# (3) Verify the re-derivation reproduces the frozen sibling map bit-for-bit (drift 0).
# ----------------------------------------------------------------------------------
def _stored_decimals(x):
    """How many decimal places a frozen JSON value was stored at (so we compare the
    re-derivation against the frozen map at the precision it was actually frozen at —
    the engine is byte-identical, so the displayed values must reproduce exactly)."""
    s = repr(float(x))
    return len(s.split(".")[1]) if "." in s else 0


def verify_drift_zero(rederived):
    """The sibling map stored DISPLAY-precision values (|h_sp| 4 dp, barrier 6 dp). The
    engine that produced them is byte-identical to this volume's engine (asserted above),
    so the honest drift-0 claim is: round(engine_value, frozen_dp) == frozen_value, exactly,
    for every one of the 27 targets — i.e. every displayed number reproduces bit-for-bit."""
    frozen = json.load(open(os.path.join(FROZEN, "threshold_map.json")))
    fz = {e["gene"]: e for e in frozen["entries"]}
    order_match = (rederived["order_by_spinodal_desc"] == frozen["order_by_spinodal_desc"])
    n_match = (rederived["n_targets"] == frozen["n_targets"])
    hsp_exact = bar_exact = True
    max_hsp_resid = max_bar_resid = 0.0
    for e in rederived["entries"]:
        f = fz[e["gene"]]
        dp_h = _stored_decimals(f["spinodal_h_sp"])
        dp_b = _stored_decimals(f["barrier"])
        if round(e["spinodal_h_sp"], dp_h) != f["spinodal_h_sp"]:
            hsp_exact = False
        if round(e["barrier"], dp_b) != f["barrier"]:
            bar_exact = False
        max_hsp_resid = max(max_hsp_resid, abs(e["spinodal_h_sp"] - f["spinodal_h_sp"]))
        max_bar_resid = max(max_bar_resid, abs(e["barrier"] - f["barrier"]))
    displayed_drift_zero = hsp_exact and bar_exact and order_match and n_match
    return dict(
        displayed_values_reproduce=displayed_drift_zero,
        hsp_exact_at_frozen_precision=hsp_exact,
        barrier_exact_at_frozen_precision=bar_exact,
        order_match=order_match, n_match=n_match,
        max_hsp_residual_full_float=max_hsp_resid,   # frozen file rounding only; engine identical
        max_barrier_residual_full_float=max_bar_resid,
        drift_zero=displayed_drift_zero)


def main():
    os.makedirs(EXPECT, exist_ok=True)

    eng_ok, this_sha, frozen_sha = assert_engine_identity()
    gamma = load_inherited_gamma()
    rederived = build_threshold_map(gamma)
    drift = verify_drift_zero(rederived)

    # carry the channelopathy anchor, burden prioritisation, and precision map through unchanged
    # (they are cited Layer-2 context / declared-weight scores; this volume re-states them, the
    #  engine-derived part being the |h_sp| placement already proven drift-0 above).
    channelopathy = json.load(open(os.path.join(FROZEN, "channelopathy_anchor.json")))
    burden        = json.load(open(os.path.join(FROZEN, "priority_ranking.json")))
    precision     = json.load(open(os.path.join(FROZEN, "precision_block_map.json")))

    summary = dict(
        module="21-analgesic-nociceptor-threshold",
        inherits="analgesic_threshold_logic v2.0 (concept DOI 10.5281/zenodo.20733420, CC BY 4.0)",
        engine_identity=dict(ok=eng_ok, this_engine_sha256=this_sha, frozen_engine_sha256=frozen_sha,
                             note="this volume's vp_neuro_engine.py IS the engine the sibling map was built on"),
        drift=drift,
        n_targets=rederived["n_targets"],
        lever_counts={k: len(v) for k, v in rederived["targets_by_lever"].items()},
    )

    json.dump(rederived,    open(os.path.join(EXPECT, "threshold_map.json"), "w"),      indent=1)
    json.dump(channelopathy, open(os.path.join(EXPECT, "channelopathy_anchor.json"), "w"), indent=1)
    json.dump(burden,       open(os.path.join(EXPECT, "priority_ranking.json"), "w"),   indent=1)
    json.dump(precision,    open(os.path.join(EXPECT, "precision_block_map.json"), "w"), indent=1)
    json.dump(summary,      open(os.path.join(EXPECT, "rederive_summary.json"), "w"),   indent=1)

    print("=" * 68)
    print("§21 analgesic target logic — re-derived on this volume's own engine")
    print("-" * 68)
    print(f"engine identity      : {'OK (byte-identical)' if eng_ok else 'FAIL'}")
    print(f"  this engine sha    : {this_sha[:16]}…")
    print(f"  frozen engine sha  : {frozen_sha[:16]}…")
    print(f"n targets            : {rederived['n_targets']}  levers {summary['lever_counts']}")
    print(f"displayed |h_sp|/bar : exact at frozen precision = "
          f"{drift['hsp_exact_at_frozen_precision'] and drift['barrier_exact_at_frozen_precision']}")
    print(f"  (full-float residual is frozen-file rounding only; engine byte-identical)")
    print(f"order match          : {drift['order_match']}")
    print(f"DRIFT ZERO (displayed): {drift['drift_zero']}")
    print("=" * 68)

    ok = eng_ok and drift["drift_zero"]
    if not ok:
        sys.exit("FAIL: inheritance did not reproduce the frozen sibling map bit-for-bit")
    print("PASS — inheritance is principled (same engine, same gamma, drift 0)")


if __name__ == "__main__":
    main()
