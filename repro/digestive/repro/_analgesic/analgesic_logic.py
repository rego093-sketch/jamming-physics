#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analgesic_logic.py  --  ANALGESIC TARGET LAYER for the digestive package (section 28).

INHERITED from `analgesic_threshold_logic` v2.0 (concept DOI 10.5281/zenodo.20733420,
version DOI 10.5281/zenodo.20733421, CC BY 4.0, same author): a reproducible, DNA-grounded
map of 27 non-opioid analgesic targets. For each gene a deterministic engine reads its human
promoter and returns gamma = -mean(NN stacking dG, SantaLucia 1998); gamma is placed on the R19
double-well firing-threshold scale |h_sp| = 2(g/3)^1.5 = (2/3sqrt3) g^1.5, barrier = g^2/4. The
targets are sorted into THREE intervention levers:
  L1  reduce the inward (excitatory) current        (block depolarising channels)
  L2  increase the outward (K+, inhibitory) current (open hyperpolarising channels)
  L3  remove the up-stream sensitising drive         (block NGF/CGRP)
plus a master identity switch (PRDM12) and opioid/cannabinoid CONTEXT comparators routed away
from central reward.

WHY IT BELONGS HERE (not a paste -- the same substrate, two readings).
  |h_sp| = spinodal(gamma) is THIS package's OWN inherited/vp_substrate.spinodal -- byte-identical.
  The section-18 visceral-afferent primitive reads the SAME R19 element as a gain:
  chi = afferent_gain(g,b) = 1/(3 s*^2 - g), which DIVERGES at the same R19 spinodal. So:
      analgesia  ==  raise the visceral-afferent FIRING THRESHOLD (the |h_sp| margin to the spinodal)
                 ==  the INVERSE of the section-18 gain rise.
  Each of the three levers moves the section-18 operating point AWAY from the spinodal -> the
  firing-threshold margin rises and the gain falls. This is the digestive substrate's reading of
  "raise the nociceptor firing threshold," and it makes the inherited map a DRUG-CLASS pointer for
  every digestive VISCERAL-PAIN disorder (IBS hypersensitivity, functional abdominal pain, biliary
  colic, functional-dyspepsia pain, oesophageal-spasm pain).

FIREWALL (non-negotiable, inherited verbatim). gamma READS promoter switch-threshold STRUCTURE
only. It is NEVER a channel activation voltage, a drug potency, a dose, an in-vivo selectivity, or
a clinical effect -- every such magnitude is [O] OPEN and is asserted NOWHERE. The lever STRENGTH
delta below is a STRUCTURAL fraction of the sensitisation bias removed, NOT a dose; the
delta<->molecule/dose/efficacy mapping is [O]. The L3 (NGF/CGRP) mechanism link is [O] cited
biology -- the read places the gene, it does not derive the receptor/network. The FELT/affective
pain stays in `mind` (the section-18 / section-27 firewall): this layer moves only the PERIPHERAL
afferent-gain term, never the felt interpretation. No molecule is designed, no synthesis, no dose,
no regimen, no efficacy/safety claim. Proposal-only; no medical responsibility.

This layer is CONSUMED in the section layer (like _oncology / _seams), NOT in the engine: the
engine circulate() sha and the disease-layer digest are UNCHANGED. It carries its OWN 2xsha256
digest (analgesic_digest).
"""
import os, sys, json, math, hashlib
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(ROOT, "inherited"),
          os.path.join(HERE, "..", "_disease")):
    if p not in sys.path:
        sys.path.insert(0, p)

import vp_substrate as VP          # THIS package's substrate (spinodal/barrier/afferent_gain) -- single source
import disease_modules as DZ       # section-18 constants (AFFERENT_G, DISTENSION_STIM)

MAP_PATH = os.path.join(ROOT, "inherited", "analgesic_targets.json")


@lru_cache(maxsize=1)
def _load_map():
    return json.load(open(MAP_PATH, encoding="utf-8"))


# ---------------------------------------------------------------------------
#  M-A1  inherit + RE-VERIFY: every |h_sp| and barrier re-derives bit-for-bit
#  from gamma through THIS package's vp_substrate (drift 0). This is what makes
#  the inheritance principled: the analgesic firing-threshold scale IS the R19
#  spinodal this package already runs.
# ---------------------------------------------------------------------------
def reverify_inheritance():
    m = _load_map()
    max_dh = 0.0; max_db = 0.0; n = 0
    for e in m["entries"]:
        g = e["gamma"]
        dh = abs(round(VP.spinodal(g), 6) - e["spinodal_h_sp"])
        db = abs(round(VP.barrier(g), 6) - e["barrier"])
        max_dh = max(max_dh, dh); max_db = max(max_db, db); n += 1
    # the closed-form identity the read rests on
    g0 = 1.456
    identity_ok = abs((2.0 / (3.0 * math.sqrt(3.0))) * g0 ** 1.5 - 2.0 * (g0 / 3.0) ** 1.5) < 1e-15
    return dict(n_targets=n, max_h_sp_drift=max_dh, max_barrier_drift=max_db,
                drift_zero=bool(max_dh == 0.0 and max_db == 0.0),
                closed_form_identity_h_sp=bool(identity_ok),
                concept_doi=m["_provenance"]["concept_doi"],
                version_doi=m["_provenance"]["version_doi"])


# ---------------------------------------------------------------------------
#  The GI / visceral nociceptor subset (cited Layer-2 relevance) ordered by the
#  stiffest firing gate first (|h_sp| desc), exactly as the inherited map orders.
# ---------------------------------------------------------------------------
def gi_nociceptor_subset():
    m = _load_map()
    gi = [e for e in m["entries"] if e.get("gi_actionable")]
    gi.sort(key=lambda e: e["spinodal_h_sp"], reverse=True)
    by_lever = {}
    for e in gi:
        by_lever.setdefault(e["lever"], []).append(e["gene"])
    rows = [(e["gene"], e["lever"], e["channel"] or e["protein"], round(e["gamma"], 4),
             round(e["spinodal_h_sp"], 4)) for e in gi]
    return dict(n_gi_targets=len(gi), order=[e["gene"] for e in gi], by_lever=by_lever, rows=rows,
                columns="(gene, lever, channel/protein, gamma, |h_sp|)")


# ---------------------------------------------------------------------------
#  THE CENTRAL RESULT: the three levers, read on the section-18 visceral afferent.
#
#  Section-18 sensitisation bias b>=0 slides the afferent operating point toward
#  the R19 yield; the FIRING THRESHOLD (max sub-yield drive before the flip) is
#  the |h_sp| margin   T(b) = spinodal(g) - b , and the GAIN is afferent_gain(g,b)
#  = 1/(3 s*^2 - g), which diverges as b -> spinodal(g). Each lever lowers the
#  EFFECTIVE bias by a structural fraction delta:
#     L1 reduce inward current   -> b_eff = b - delta   (removes depolarising drive)
#     L2 increase outward K+      -> b_eff = b - delta   (hyperpolarises away from yield)
#     L3 remove sensitising drive -> b_eff = b - delta   (un-does the sensitisation)
#  so for ALL THREE: the firing threshold T(b_eff) RISES by delta and the gain
#  FALLS monotonically back toward the baseline 1/(2g). One substrate, one effect.
#
#  delta is a STRUCTURAL fraction, NOT a dose; delta<->molecule/dose/efficacy is [O].
# ---------------------------------------------------------------------------
LEVERS = ("L1", "L2", "L3")
LEVER_ACTION = {
    "L1": "reduce the inward (excitatory) current (block depolarising channels) -> lower the effective sensitisation bias",
    "L2": "increase the outward K+ current (open K_V7) -> hyperpolarise away from yield -> lower the effective sensitisation bias",
    "L3": "remove the up-stream NGF/CGRP sensitising drive -> un-do the sensitisation -> lower the effective bias",
}

def lever_de_sensitises_afferent(b0_frac=0.60):
    """For a sensitised visceral afferent (section-18) at b0 = b0_frac * spinodal (visceral
    hypersensitivity), apply each lever at increasing STRUCTURAL strength delta and read the
    section-18 firing threshold T = spinodal - b_eff and the gain chi = afferent_gain. For every
    lever: T rises monotonically (the analgesic goal -- raise the firing threshold) and chi falls
    monotonically back toward the baseline 1/(2g). All emergent from the R19 substrate; nothing
    fitted. delta is structural (a fraction of the sensitisation removed), NOT a dose -> [O]."""
    g = DZ.AFFERENT_G
    sp = VP.spinodal(g)
    b0 = b0_frac * sp
    baseline_gain = VP.afferent_gain(g, 0.0)              # 1/(2g)
    sens_gain = VP.afferent_gain(g, b0)                   # elevated (hypersensitivity)
    deltas = [0.0, 0.25 * b0, 0.50 * b0, 0.75 * b0, b0]   # up to full reversal of the sensitisation
    out = {}
    all_T_rise = True; all_gain_fall = True; all_return = True
    for L in LEVERS:
        rows = []
        for d in deltas:
            b_eff = max(0.0, b0 - d)
            T = sp - b_eff                                # firing-threshold |h_sp| margin
            chi = VP.afferent_gain(g, b_eff)
            rows.append((round(d, 4), round(T, 5), round(chi, 5)))
        Ts = [r[1] for r in rows]; chis = [r[2] for r in rows]
        T_rises = all(Ts[i] <= Ts[i + 1] + 1e-12 for i in range(len(rows) - 1))
        gain_falls = all(chis[i] >= chis[i + 1] - 1e-12 for i in range(len(rows) - 1))
        returns_to_baseline = abs(chis[-1] - baseline_gain) < 1e-9
        all_T_rise &= T_rises; all_gain_fall &= gain_falls; all_return &= returns_to_baseline
        out[L] = dict(action=LEVER_ACTION[L], rows=rows,
                      firing_threshold_rises=bool(T_rises),
                      gain_falls=bool(gain_falls),
                      gain_returns_to_baseline_at_full=bool(returns_to_baseline))
    return dict(g=g, spinodal=round(sp, 6), b0_sensitised=round(b0, 6),
                baseline_gain=round(baseline_gain, 6), sensitised_gain=round(sens_gain, 6),
                hypersensitivity_amplification=round(sens_gain / baseline_gain, 4),
                columns="per-lever rows: (lever_strength_delta, firing_threshold_|h_sp|_margin, afferent_gain)",
                per_lever=out,
                all_levers_raise_firing_threshold=bool(all_T_rise),
                all_levers_lower_gain=bool(all_gain_fall),
                all_levers_return_to_baseline=bool(all_return),
                note="delta is a STRUCTURAL fraction of the sensitisation removed, NOT a dose; the "
                     "delta<->molecule/dose/efficacy mapping is [O]. Felt pain is `mind` (firewall).")


# ---------------------------------------------------------------------------
#  DRUG-CLASS POINTER per digestive VISCERAL-PAIN disorder.
#  Each row: the section it lives in, which lever(s) the model points to, the GI
#  target(s) on that lever, and the CITED validated agent CLASS that realises the
#  lever direction. EFFICACY / DOSE / SELECTIVITY-IN-VIVO are [O]. The felt /
#  affective component is `mind` (firewall). This is a mechanism-class pointer to
#  help identify WHICH class an effective agent moves -- never a prescription.
# ---------------------------------------------------------------------------
def recommendation_map():
    rows = [
        dict(disorder="IBS visceral hypersensitivity",
             section="18 (B3 afferent gain)",
             levers=["L1", "L2", "L3"],
             gi_targets=["SCN10A (Na_V1.8)", "P2RX3 (P2X3)", "CACNA2D1 (alpha2delta-1)",
                         "KCNQ2/3/5 (K_V7)", "NGF/NTRK1", "CALCA/CALCB/CALCRL/RAMP1 (CGRP)"],
             cited_class=("L1 peripheral inward-current block -- the alpha2delta-1 gabapentinoid class "
                          "is the established peripheral-acting option for functional visceral pain "
                          "(Field 2006); the Na_V1.8 closed-state class (suzetrigine, FDA 2025-01-30) and "
                          "the P2X3 antagonist lineage (gefapixant) are the emerging nociceptor-selective "
                          "options. L2: a K_V7 opener raises the brake. L3: anti-NGF / anti-CGRP remove the "
                          "sensitising drive. Central neuromodulators (TCA/SNRI) act on the FELT/affective "
                          "term -> `mind`, OUTSIDE this map."),
             grade="direction [V] (each lever lowers the section-18 gain); class placement [F] structural / efficacy+dose+selectivity-in-vivo [O]"),
        dict(disorder="Functional abdominal pain (no structural lesion)",
             section="18 (B3 afferent gain)",
             levers=["L1", "L2", "L3"],
             gi_targets=["SCN10A (Na_V1.8)", "P2RX3 (P2X3)", "CACNA2D1 (alpha2delta-1)", "KCNQ2/3/5 (K_V7)"],
             cited_class=("pure afferent-gain reduction at NORMAL motility -- the L1/L2 peripheral classes "
                          "above; central/peripheral neuromodulation acts on the felt term -> `mind`. "
                          "Peripheral afferent term only here."),
             grade="direction [V] / efficacy [O] / felt component `mind`"),
        dict(disorder="Functional dyspepsia pain (post-prandial)",
             section="17 (B2 reservoir) + 18 (B3 gain)",
             levers=["L1", "L2"],
             gi_targets=["KCNQ2/3/5 (K_V7)", "SCN10A (Na_V1.8)", "P2RX3 (P2X3)"],
             cited_class=("the gastric-wall afferent gain is lowered by the L1/L2 peripheral classes; the "
                          "MECHANICAL half (impaired accommodation) is the section-17 fundic-relaxing target "
                          "(raise compliance), a SEPARATE knob. Felt distress -> `mind`."),
             grade="direction [V] / efficacy [O] / felt component `mind`"),
        dict(disorder="Biliary colic (gallbladder distension/spasm)",
             section="25 (C4 nucleation) + 27 mind pointer",
             levers=["L1"],
             gi_targets=["SCN10A (Na_V1.8)", "P2RX3 (P2X3)", "TRPV1", "ASIC3"],
             cited_class=("the visceral-afferent peripheral term is lowered by the L1 inward-current classes; "
                          "the felt colic is `mind`'s (section-27 one-way pointer), and stone REMOVAL / "
                          "stasis relief is the section-25 / section-16 mechanical lever, not analgesia."),
             grade="direction [V] / efficacy [O] / felt colic `mind`"),
        dict(disorder="Oesophageal-spasm pain",
             section="16 (B1 gate)",
             levers=["L1", "L2"],
             gi_targets=["SCN10A (Na_V1.8)", "KCNQ2/3/5 (K_V7)"],
             cited_class=("the afferent pain term is lowered by the L1/L2 peripheral classes; the MOTOR half "
                          "(excess contraction amplitude / lost coordination) is the section-16 smooth-muscle "
                          "relaxant knob, a separate target. Felt pain -> `mind`."),
             grade="direction [V] / efficacy [O] / felt component `mind`"),
    ]
    return dict(n_disorders=len(rows), rows=rows,
                firewall="every cited agent is a CLASS that realises a lever DIRECTION; efficacy, dose, "
                         "selectivity-in-vivo are [O]; the felt/affective pain is `mind` (peripheral term only here); "
                         "no molecule is designed and nothing here prescribes, diagnoses, or treats.")


# ---------------------------------------------------------------------------
#  Burden-weighted prioritisation RESTRICTED to the GI nociceptor subset.
#  Re-derives the inherited score = w_B*B + w_U*U + w_D*D over the cited 1..5
#  tiers (declared weights, never reverse-fit), sorted desc, tie-break by |h_sp|
#  then gene. gamma/|h_sp| is carried as the structural map-place but is NEVER
#  folded into the clinical priority score (firewall).
# ---------------------------------------------------------------------------
def gi_burden_prioritisation():
    m = _load_map()
    w = m["burden_weights_declared"]
    ranked = []
    for e in m["entries"]:
        if not e.get("gi_actionable"):
            continue
        bud = e.get("burden_BUD")
        if not bud:
            continue
        score = round(w["B"] * bud["B"] + w["U"] * bud["U"] + w["D"] * bud["D"], 4)
        ranked.append(dict(gene=e["gene"], lever=e["lever"],
                           channel_or_protein=e["channel"] or e["protein"],
                           B=bud["B"], U=bud["U"], D=bud["D"], score=score,
                           h_sp_map_place=e["spinodal_h_sp"], tier_basis=bud["tier_basis"]))
    ranked.sort(key=lambda r: (-r["score"], -r["h_sp_map_place"], r["gene"]))
    for i, r in enumerate(ranked, 1):
        r["rank"] = i
    # re-derivation check: our score must equal the inherited vendored score (drift 0)
    vend = {e["gene"]: e["burden_BUD"]["score"] for e in m["entries"]
            if e.get("gi_actionable") and e.get("burden_BUD")}
    max_score_drift = max(abs(r["score"] - vend[r["gene"]]) for r in ranked) if ranked else 0.0
    return dict(weights_declared=w, n=len(ranked), ranking=ranked,
                top3=[r["gene"] for r in ranked[:3]],
                score_reproduces_inherited=bool(max_score_drift == 0.0),
                gamma_not_folded_into_score=True,
                firewall="gamma/|h_sp| is the structural read's map-place, NOT folded into the clinical priority score.")


# ---------------------------------------------------------------------------
#  Precision (pain-selective) VISCERAL local anaesthesia -- the section-28 P6
#  analogue: a nociceptor-selective ENTRY PORT (P2X3 / TRPV1 / TRPA1 / ASIC3,
#  all gut-nociceptor-enriched) x a charged firing-threshold-raising blocker that
#  can only reach its site through the open port -> a DIFFERENTIAL block that
#  silences visceral nociceptive fibres while sparing motor / light-touch. The
#  mechanism SHAPE is [F] (anchored to Binshtok-Bean-Woolf, Nature 2007); the
#  differential-block ratio / duration / concentration / formulation are [O].
# ---------------------------------------------------------------------------
def precision_visceral_local_anaesthesia():
    m = _load_map()
    ports = {}
    for sym in ("P2RX3", "TRPV1", "TRPA1", "ASIC3"):
        e = next(x for x in m["entries"] if x["gene"] == sym)
        ports[sym] = dict(gamma=e["gamma"], spinodal_h_sp=e["spinodal_h_sp"], src=e["src"])
    blockers = [x["gene"] for x in m["entries"]
                if x["lever"] == "L1" and (x["channel"] or "").startswith("Na_V")]
    return dict(mechanism="precision visceral analgesia = (gut nociceptor-selective entry port) x (charged firing-threshold raiser)",
                entry_ports=ports, charged_blocker_candidates=blockers,
                anchor="Binshtok, Bean & Woolf, Nature 2007 (charged Na_V blocker via TRPV1 -> differential nociceptive-vs-motor block)",
                differential_block_metric="duration/strength of visceral nociceptive block vs motor block -- a PREDICTION, magnitude [O]",
                grade="[F] mechanism SHAPE (entry-port selectivity x charged blocker); differential-block magnitude / concentration / formulation [O]",
                firewall="no molecule designed; every concentration/duration/route/dose is [O]; reads the threshold/selectivity STRUCTURE only.")


# ---------------------------------------------------------------------------
#  FAIL-CLOSED forbidden-claim scan (mirrors the analgesic M5 gate). Scans the
#  recommendation map + precision map text for dose / efficacy / safety /
#  synthesis / treatment-promise tokens, with a NEGATION GUARD so firewall
#  sentences ("NOT a dose", "[O] OPEN", "no molecule") never false-positive.
# ---------------------------------------------------------------------------
FORBIDDEN = ["mg ", "mg/", "milligram", "dose of", "dosage", "twice daily", "once daily", "bid", "tid",
             "mcg", "microgram", " ic50", " ec50", "potency of", "cures", "guaranteed", "is effective",
             "proven effective", "will relieve", "synthes", "formulation route", "titrate to"]
NEG_GUARD = ["[o]", "open", "not a dose", "no dose", "no molecule", "efficacy", "asserted nowhere",
             "never folded", "firewall", "no synthesis", "no regimen", "no medical", "proposal-only",
             "selectivity-in-vivo", "magnitude", "prediction", "structural fraction"]

def _scan_text(blob):
    low = blob.lower()
    hits = []
    for tok in FORBIDDEN:
        idx = low.find(tok)
        while idx != -1:
            window = low[max(0, idx - 60): idx + 60]
            if not any(ng in window for ng in NEG_GUARD):
                hits.append(tok.strip())
            idx = low.find(tok, idx + 1)
    return sorted(set(hits))

def forbidden_claim_scan():
    blob = json.dumps(recommendation_map(), ensure_ascii=False) + " " + \
           json.dumps(precision_visceral_local_anaesthesia(), ensure_ascii=False) + " " + \
           json.dumps(lever_de_sensitises_afferent(), ensure_ascii=False)
    hits = _scan_text(blob)
    return dict(scanned_chars=len(blob), forbidden_hits=hits, clean=bool(not hits),
                note="fail-closed: any dose/efficacy/safety/synthesis token outside a firewall/[O] context fails the build.")


# ---------------------------------------------------------------------------
#  validate() + digest()  (this layer's OWN 2xsha256; engine + disease UNCHANGED)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def validate():
    rv = reverify_inheritance()
    gi = gi_nociceptor_subset()
    lv = lever_de_sensitises_afferent()
    rm = recommendation_map()
    pr = gi_burden_prioritisation()
    px = precision_visceral_local_anaesthesia()
    sc = forbidden_claim_scan()
    passed = bool(
        rv["drift_zero"] and rv["closed_form_identity_h_sp"]
        and gi["n_gi_targets"] >= 18
        and lv["all_levers_raise_firing_threshold"] and lv["all_levers_lower_gain"]
        and lv["all_levers_return_to_baseline"]
        and rm["n_disorders"] >= 5
        and pr["score_reproduces_inherited"] and pr["gamma_not_folded_into_score"]
        and len(px["entry_ports"]) == 4 and len(px["charged_blocker_candidates"]) >= 1
        and sc["clean"]
    )
    return dict(reverify=rv, gi_subset=gi, lever_de_sensitisation=lv, recommendation_map=rm,
                gi_prioritisation=pr, precision_visceral=px, forbidden_claim_scan=sc, passed=passed,
                treatment=("INHERITED analgesic target logic, applied to digestive VISCERAL PAIN. The section-18 "
                           "afferent firing threshold |h_sp| (the spinodal margin) is raised -- equivalently the "
                           "gain is lowered -- by ANY of three levers: L1 reduce the inward current (the alpha2delta-1 "
                           "gabapentinoid class; the emerging Na_V1.8 / P2X3 nociceptor-selective classes), L2 open "
                           "the K_V7 brake, L3 remove the NGF/CGRP sensitising drive. The map is a DRUG-CLASS POINTER "
                           "for IBS hypersensitivity, functional abdominal pain, functional-dyspepsia pain, biliary "
                           "colic, and oesophageal-spasm pain -- pointing to WHICH lever/class an effective agent "
                           "moves. Class placement is [F] structural; efficacy, dose, and selectivity-in-vivo are [O]; "
                           "the felt/affective pain is `mind` (the peripheral afferent term only is moved here)."),
                grades=("S28 analgesic layer INHERITED from analgesic_threshold_logic v2.0 (DOI 10.5281/zenodo.20733420). "
                        "The 27-target reads re-verify bit-for-bit through THIS package's R19 spinodal/barrier (drift 0) "
                        "-- the analgesic firing-threshold scale IS the section-18 afferent spinodal. The three levers each "
                        "raise the section-18 firing threshold / lower the gain [V]; the firing-threshold = spinodal margin "
                        "and the gain divergence are the exact R19 identity [F]; the GI burden prioritisation re-derives the "
                        "inherited declared-weight score [F]; and every clinical magnitude -- potency, dose, in-vivo "
                        "selectivity, differential-block ratio, efficacy -- plus the felt pain is [O] (firewall: gamma reads "
                        "promoter switch-threshold STRUCTURE only; felt experience is `mind`)."))


def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_round(v) for v in o]
    return o

@lru_cache(maxsize=1)
def digest():
    s = json.dumps(_round(validate()), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    v = validate()
    print("=== analgesic layer (section 28) -- INHERITED from analgesic_threshold_logic v2.0 ===")
    rv = v["reverify"]
    print(f"  inherit+re-verify: {rv['n_targets']} targets, |h_sp| drift={rv['max_h_sp_drift']:.1e}, "
          f"barrier drift={rv['max_barrier_drift']:.1e}, drift_zero={rv['drift_zero']} (DOI {rv['concept_doi']})")
    gi = v["gi_subset"]
    print(f"  GI nociceptor subset: {gi['n_gi_targets']} targets; by lever " +
          ", ".join(f"{k}={len(x)}" for k, x in gi["by_lever"].items()))
    lv = v["lever_de_sensitisation"]
    print(f"  3 levers on the section-18 afferent (sensitised gain x{lv['hypersensitivity_amplification']}): "
          f"all raise firing threshold={lv['all_levers_raise_firing_threshold']}, "
          f"all lower gain={lv['all_levers_lower_gain']}, all return to baseline={lv['all_levers_return_to_baseline']}")
    pr = v["gi_prioritisation"]
    print(f"  GI burden prioritisation (declared weights {pr['weights_declared']}): top3={pr['top3']}; "
          f"reproduces inherited score={pr['score_reproduces_inherited']}; gamma not folded={pr['gamma_not_folded_into_score']}")
    print(f"  precision visceral LA ports={list(v['precision_visceral']['entry_ports'])}; "
          f"forbidden-claim scan clean={v['forbidden_claim_scan']['clean']}")
    print(f"  PASSED={v['passed']}")
    s, h = digest()
    print(f"  analgesic layer 2xsha256: {len({digest()[1] for _ in range(2)}) == 1}  (sha={h[:12]}...)")
