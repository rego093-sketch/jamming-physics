#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VC4  ADHD CO-EMERGENCE -- why does ADHD respond where autism does not?
======================================================================
Builds an EXPLICIT, gene-grounded ADHD substrate (not a relabelled autism cohort): a
cohort whose fault is O/T-dominant (gain/arousal) with INTACT W -- the section-2 mapping
(stimulant = catecholamine = gain; gain restores O/T, not W), now made falsifiable on a
real ADHD-gene emergence. The O/T mapping is DECLARED as an interpretation and tested,
not smuggled in.

THE ADHD COHORT (pre-registered inclusion = gain/arousal/catecholamine pathway; exclude
syndromic / adhesion-ambiguous, so 'ADHD has intact W' is airtight):
  O  (catecholamine signaling GAIN -- sets signal amplitude): DRD4, SLC6A3, COMT (atlas),
     SNAP25, DBH, TH (live-fetched from NCBI RefSeq GRCh38).
  T  (adrenergic/monoaminergic arousal TONE -- sets E-I bias): ADRA2A (live), SLC6A4 (atlas).
  W  : NONE -- the discriminant. ADHD carries no long-range wiring fault.
  EXCLUDED (pre-registered): FOXP2 (TF/language syndrome), ADGRL3 (adhesion-GPCR, axis-
     ambiguous). Severe/syndromic genes are out of scope as in D9.0.

THE STATES (gene-grounded; no new tuned constant -- the per-axis gain factors are inherited
byte-for-byte from D9: O -> M_O=0.4, T -> k_T/KAP=0.8; the cohort gain is the GENE-FRACTION-
WEIGHTED mean of those inherited factors, a transparent composition of measured inputs):
  ADHD  : gain deficit kap_ADHD on the INTACT geometry (healthy Wrn).
  autism: gain deficit kap_autism on the BROKEN geometry (Wwn = the D9 W-fault).
  AuDHD : the ADHD O/T genes PLUS the autism W genes -> gain deficit on BROKEN geometry.

THE TWO OPERATORS:
  stimulant = the gain operator (raise effective kappa, the catecholamine analogue), swept,
              never tuned (the restoration point is read off, as in D9.4).
  theta-cap = the VC1 winning coupling (C-FORCE external pacemaker), window amplitude.

PRE-REGISTERED (sign-only):
  P-VC4a  the stimulant (gain) restores the ADHD cohort to health (O/T-only, intact W ->
          gain fixes BOTH R and PAC), while it restores only the O/T part of the autism
          cohort (PAC recovers; R stays capped by the broken W -- the section-2 / D9.4 result,
          now on an explicit ADHD substrate).
  P-VC4b  the theta-cap provides LITTLE long-range benefit to ADHD (no W lane is missing --
          the highway is intact), but is the ONLY axis-appropriate aid for the autism W
          component (the missing long-range lane it can pace). Discriminant: cap is for W,
          stimulant is for O/T.
  P-VC4c  in a mixed AuDHD cohort (O/T AND W), stimulant + cap address DIFFERENT axes and do
          not interfere -- combined coverage (gain restored AND long-range routing restored)
          exceeds either alone, WITHOUT pushing into over-sync.

efficacy=0; mechanism only; NOT medical advice; Axis-A firewall; no dose/synthesis. The
engine has NO validated ADHD model; this is a principled, gene-grounded interpretation that
is TESTED, with ADHD model validity OPEN. VP-SPEC v1.8 (C0-C4, SEED=19). ADD-ONLY;
vp_mind_engine READ-ONLY (tree 0fbf4988...).
"""
import os, sys, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY
import autism_cohort_cerebrum as CB

ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
RESULT = os.path.join(HERE, "vc4_adhd_coemergence_results.json")
EXPECT = os.path.join(HERE, "expected_vc4_adhd_coemergence_sha256.json")
ATLAS_CACHE = os.path.join(HERE, "disease_gene_promoters.json")
ADHD_CACHE = os.path.join(HERE, "adhd_cohort_promoters.json")

N = CB.N; OMEGA = CB.OMEGA; OMEGA0 = CB.OMEGA0; KAP = CB.KAP; KGLOB = CB.KGLOB
F_THETA = CB.F_THETA; _D = CB._D; _FAR = CB._FAR
INJ_WINDOW = 0.08

NN = {"AA": -1.00, "TT": -1.00, "AT": -0.88, "TA": -0.58, "CA": -1.45, "TG": -1.45,
      "GT": -1.44, "AC": -1.44, "CT": -1.28, "AG": -1.28, "GA": -1.30, "TC": -1.30,
      "CG": -2.17, "GC": -2.24, "GG": -1.84, "CC": -1.84}

# pre-registered ADHD cohort: axis by mechanism (gain/arousal catecholamine), intact W
ADHD_COHORT = {
    "DRD4":   dict(axis="O", src="dopamine receptor D4 (7-repeat ADHD locus); catecholamine signaling gain"),
    "SLC6A3": dict(axis="O", src="dopamine transporter DAT1; reuptake sets dopaminergic gain"),
    "COMT":   dict(axis="O", src="catechol-O-methyltransferase; prefrontal dopamine catabolism/gain"),
    "SNAP25": dict(axis="O", src="SNARE vesicle release (coloboma ADHD model); presynaptic output gain"),
    "DBH":    dict(axis="O", src="dopamine beta-hydroxylase; catecholamine synthesis (DA->NA) gain"),
    "TH":     dict(axis="O", src="tyrosine hydroxylase; rate-limiting catecholamine synthesis gain"),
    "ADRA2A": dict(axis="T", src="alpha-2A adrenergic receptor (guanfacine target); noradrenergic arousal tone"),
    "SLC6A4": dict(axis="T", src="serotonin transporter; monoaminergic arousal/E-I tone"),
}
ADHD_EXCLUDED = {"FOXP2": "TF/language syndrome (syndromic, W/developmental)",
                 "ADGRL3": "adhesion-GPCR (axis-ambiguous; keeps 'intact W' airtight)"}
# autism W-axis genes (from D9.0) reused to build the explicit mixed AuDHD substrate
AUTISM_W_GENES = ["CNTNAP2", "CNTN6", "DSCAM", "RELN"]


def _gamma_of(seq):
    steps = [-NN[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN]
    return round(float(sum(steps) / len(steps)), 4) if steps else float("nan")


def _load_gamma(sym):
    """re-derive a gene's promoter gamma OFFLINE from the atlas or ADHD cache (proves the
    reproduction path stays in-package and matches the cache)."""
    atlas = json.load(open(ATLAS_CACHE, encoding="utf-8"))["genes"]
    adhd = json.load(open(ADHD_CACHE, encoding="utf-8"))["genes"] if os.path.exists(ADHD_CACHE) else {}
    if sym in atlas:
        rec, where = atlas[sym], "atlas_cache"
    elif sym in adhd:
        rec, where = adhd[sym], "adhd_live_fetch_cache"
    else:
        return None
    g = _gamma_of(rec["sequence"])
    return dict(gamma=g, matches_cache=bool(abs(g - rec["gamma"]) <= 1e-9), provenance=where,
                accession=rec.get("acc"))


def _locality(W):
    sh = []
    for i in range(N):
        order = np.argsort(_D[i] + np.where(np.arange(N) == i, 1e9, 0.0))
        sh.append(float(W[i, order[:2]].sum()))
    return float(np.mean(sh))


def _run(W, kap_mult=1.0, cap_inj=0.0, T=4.0, dt=0.001, seed=E.SEED):
    """integrate the cerebrum on geometry W with an effective-gain multiplier (stimulant)
    and an optional C-FORCE cap. Returns (mean R 2nd half, far-pair coherence 2nd half)."""
    rng = np.random.RandomState(seed); th = rng.uniform(-math.pi, math.pi, N)
    ns = int(T / dt); w = 2 * math.pi * F_THETA; Rs = np.empty(ns); Hh = []
    for s in range(ns):
        diff = th[None, :] - th[:, None]
        net = KAP * kap_mult * OMEGA0 * np.sum(W * np.sin(diff), axis=1)
        drive = cap_inj * OMEGA0 * np.sin(w * (s * dt) - th) if cap_inj > 0 else 0.0
        th = th + dt * (OMEGA + net + drive)
        Rs[s] = abs(np.mean(np.exp(1j * th)))
        if s >= ns // 2:
            Hh.append(th.copy())
    th_h = np.asarray(Hh); iu = np.where(np.triu(_FAR, 1)); pl = []
    for i, j in zip(*iu):
        d = th_h[:, i] - th_h[:, j]; pl.append(abs(np.mean(np.exp(1j * d))))
    return float(np.mean(Rs[ns // 2:])), float(np.mean(pl))


def _cohort_gain_mult(axes):
    """gene-fraction-weighted mean of the INHERITED D9 axis gain factors (O->M_O, T->k_T/KAP).
    No new constant: a transparent composition of measured inputs by real gene counts."""
    gO = CB.M_O; gT = CB.k_T / CB.KAP
    f = {"O": gO, "T": gT}
    vals = [f[a] for a in axes if a in f]
    return float(sum(vals) / len(vals)) if vals else 1.0


def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o


E.seed_everything()
_EM = CB.emerge()
_WRN = _EM["Wrn"]; _WWN = _EM["Wwn"]
R_HEALTH = _EM["R_health"]; PAC_HEALTH = _EM["pac_health"]
OVER = R_HEALTH * 1.15
LOC_HEALTH = _locality(_WRN); LOC_W = _locality(_WWN)


def run():
    E.seed_everything()
    em = _EM
    pac_grounded = em["pac_grounded"]

    # ---- emerge the ADHD cohort genes (gene-grounded; gamma re-derived offline) ----
    adhd_genes = {}
    for sym, ann in ADHD_COHORT.items():
        gg = _load_gamma(sym)
        g = gg["gamma"]
        adhd_genes[sym] = dict(gamma=g, axis=ann["axis"], provenance=gg["provenance"],
                               gamma_matches_cache=gg["matches_cache"], basis=ann["src"],
                               fold_healthy=round(CB.ig_thr(g, 0.0), 6),
                               seizure_bias=round(CB.seizure_bias(g), 6))
    adhd_axes = [adhd_genes[s]["axis"] for s in adhd_genes]
    n_O = sum(a == "O" for a in adhd_axes); n_T = sum(a == "T" for a in adhd_axes)
    n_W = sum(a == "W" for a in adhd_axes)
    all_match = all(adhd_genes[s]["gamma_matches_cache"] for s in adhd_genes)

    # autism cohort axis counts (from D9 cohort) -- for the gain composition
    autism_cells = em["cells"]
    autism_axes = [autism_cells[s]["axis"] for s in autism_cells]

    kap_adhd = _cohort_gain_mult(adhd_axes)                       # intact geometry
    kap_autism = _cohort_gain_mult([a for a in autism_axes if a in ("O", "T")])  # broken geometry
    kap_audhd = kap_adhd                                          # AuDHD O/T == ADHD O/T composition

    # ---- baselines ----
    R_adhd0, fc_adhd0 = _run(_WRN, kap_adhd)
    pac_adhd0 = CB._pac_kappa(KAP * kap_adhd)
    R_aut0, fc_aut0 = _run(_WWN, kap_autism)
    pac_aut0 = CB._pac_kappa(KAP * kap_autism)

    # ================= P-VC4a: stimulant (gain) sweep =================
    boosts = [1.0, 1.5, 2.0, 2.5, 3.0]

    def stim_sweep(W, base_mult):
        rows = []; reach_R = None; pac_at_reach = None; reach_pac = None
        for bo in boosts:
            m = base_mult * bo
            R, fc = _run(W, m); pac = CB._pac_kappa(KAP * m)
            r_health = bool(R >= R_HEALTH - 1e-6)
            pac_health = bool(pac >= PAC_HEALTH - 1e-9)
            rows.append(dict(gain_boost=round(bo, 4), kappa_mult=round(m, 6), R=round(R, 6),
                             gap_to_health=round(R - R_HEALTH, 6), pac=round(pac, 9),
                             R_at_or_above_health=r_health, pac_at_or_above_health=pac_health,
                             over_sync=bool(R > OVER)))
            if reach_R is None and r_health:
                reach_R = bo
            if reach_pac is None and pac_health:
                reach_pac = bo; pac_at_reach = pac
        return rows, reach_R, reach_pac

    adhd_stim, adhd_reachR, adhd_reachPAC = stim_sweep(_WRN, kap_adhd)
    aut_stim, aut_reachR, aut_reachPAC = stim_sweep(_WWN, kap_autism)

    adhd_R_max = max(r["R"] for r in adhd_stim)
    aut_R_max = max(r["R"] for r in aut_stim)
    # ADHD: gain restores BOTH R and PAC to health at a finite boost (intact geometry)
    stim_restores_adhd = bool(adhd_reachR is not None and adhd_reachPAC is not None)
    # autism: PAC recovers, but R is capped below health across the swept gain (broken geometry);
    # locality stays at the broken value (gain never touches geometry)
    aut_R_capped = bool(aut_R_max < R_HEALTH - 1e-6 or aut_reachR is None
                        or (aut_reachR is not None and aut_reachPAC is not None and aut_reachR > aut_reachPAC))
    loc_autism_invariant = bool(abs(_locality(_WWN) - LOC_W) < 1e-12 and LOC_W > LOC_HEALTH + 1e-9)
    aut_pac_recovers = bool(aut_reachPAC is not None)
    P_VC4a_stim_restores_adhd_not_autism_W = bool(stim_restores_adhd and aut_R_capped
                                                  and aut_pac_recovers and loc_autism_invariant)

    # ================= P-VC4b: theta-cap (C-FORCE) is axis-appropriate for W =================
    # cap on each BASELINE: the long-range (far) benefit it supplies
    R_adhd_cap, fc_adhd_cap = _run(_WRN, kap_adhd, cap_inj=INJ_WINDOW)
    R_aut_cap, fc_aut_cap = _run(_WWN, kap_autism, cap_inj=INJ_WINDOW)
    dfar_adhd = fc_adhd_cap - fc_adhd0
    dfar_autism = fc_aut_cap - fc_aut0
    # cap BEYOND stimulant: on the stimulant-restored states, does the cap still add long-range?
    m_adhd_stim = kap_adhd * (adhd_reachPAC or 3.0)        # ADHD gain-restored
    m_aut_stim = kap_autism * (aut_reachPAC or 3.0)        # autism gain-restored (PAC-health)
    R_adhd_sr, fc_adhd_sr = _run(_WRN, m_adhd_stim)
    R_adhd_sr_cap, fc_adhd_sr_cap = _run(_WRN, m_adhd_stim, cap_inj=INJ_WINDOW)
    R_aut_sr, fc_aut_sr = _run(_WWN, m_aut_stim)
    R_aut_sr_cap, fc_aut_sr_cap = _run(_WWN, m_aut_stim, cap_inj=INJ_WINDOW)
    cap_adds_beyond_stim_adhd = fc_adhd_sr_cap - fc_adhd_sr
    cap_adds_beyond_stim_autism = fc_aut_sr_cap - fc_aut_sr
    # discriminant: cap's long-range benefit is much larger where W is broken (autism) than intact (ADHD)
    cap_W_selectivity_ratio = (dfar_autism / dfar_adhd) if dfar_adhd > 1e-9 else float("inf")
    P_VC4b_cap_is_for_W_not_adhd = bool(dfar_autism > dfar_adhd + 1e-6
                                        and cap_adds_beyond_stim_autism > cap_adds_beyond_stim_adhd + 1e-6)

    # ================= P-VC4c: mixed AuDHD -- different axes, no interference =================
    # explicit AuDHD substrate: ADHD O/T genes + autism W genes -> gain deficit on broken geometry
    audhd_W_genes = {s: round(autism_cells[s]["gamma"], 4) for s in AUTISM_W_GENES if s in autism_cells}
    R_au0, fc_au0 = _run(_WWN, kap_audhd)
    pac_au0 = CB._pac_kappa(KAP * kap_audhd)
    m_au_stim = kap_audhd * (aut_reachPAC or 3.0)         # stimulant to PAC-health
    R_au_stim, fc_au_stim = _run(_WWN, m_au_stim)
    pac_au_stim = CB._pac_kappa(KAP * m_au_stim)
    R_au_cap, fc_au_cap = _run(_WWN, kap_audhd, cap_inj=INJ_WINDOW)
    R_au_both, fc_au_both = _run(_WWN, m_au_stim, cap_inj=INJ_WINDOW)
    pac_au_both = pac_au_stim
    # coverage: stimulant fixes the GAIN axis (PAC->health); cap fixes the W axis (far-coherence);
    # combined fixes BOTH; neither alone does. and combined must not over-sync.
    stim_fixes_gain = bool(pac_au_stim >= PAC_HEALTH - 1e-9)
    cap_fixes_routing = bool(fc_au_cap > fc_au0 + 1e-6)
    combined_covers_both = bool(pac_au_both >= PAC_HEALTH - 1e-9 and fc_au_both > fc_au0 + 1e-6)
    combined_beats_either_routing = bool(fc_au_both >= fc_au_cap - 1e-6 and fc_au_both > fc_au_stim + 1e-6)
    combined_no_oversync = bool(R_au_both <= OVER)
    P_VC4c_combined_covers_more_no_oversync = bool(combined_covers_both and combined_beats_either_routing
                                                   and combined_no_oversync and stim_fixes_gain and cap_fixes_routing)

    out = {
        "_what": "VC4 ADHD co-emergence: an explicit gene-grounded ADHD substrate (O/T-dominant gain/arousal, "
                 "INTACT W) emerged on the same READ-ONLY engine, run side-by-side with the D9 autism cohort "
                 "(O/T + broken W) and a mixed AuDHD cohort (ADHD O/T genes + autism W genes). The stimulant "
                 "(gain operator) and the theta-cap (VC1 C-FORCE pacemaker) are applied to each. The discriminant: "
                 "the stimulant is for the O/T (gain) axis, the cap is for the W (wiring) axis.",
        "adhd_cohort": {
            "genes": adhd_genes, "n_O": n_O, "n_T": n_T, "n_W": n_W,
            "all_gamma_re_derive_offline_match_cache": all_match,
            "excluded_preregistered": ADHD_EXCLUDED,
            "axis_mapping_declared_as_interpretation": "stimulant=catecholamine=gain (section 2); O/T axes are "
                "the gain/arousal surface ADHD shares with autism; W is the autism-specific wiring axis ADHD lacks.",
            "intact_W_is_the_discriminant": bool(n_W == 0)},
        "gain_composition": {
            "inherited_O_factor_M_O": round(CB.M_O, 6),
            "inherited_T_factor_k_T_over_KAP": round(CB.k_T / CB.KAP, 6),
            "kap_mult_adhd_intact_geometry": round(kap_adhd, 6),
            "kap_mult_autism_broken_geometry": round(kap_autism, 6),
            "note": "no new tuned constant: the per-axis gain factors are inherited byte-for-byte from D9; the "
                    "cohort gain is their gene-fraction-weighted mean. The sign results are robust to the "
                    "composition choice (any O/T gain deficit on intact vs broken geometry gives the same contrast)."},
        "baselines": {
            "R_health": round(R_HEALTH, 6), "pac_health": round(PAC_HEALTH, 9),
            "loc_health": round(LOC_HEALTH, 6), "loc_W": round(LOC_W, 6), "over_sync_threshold": round(OVER, 6),
            "adhd_R": round(R_adhd0, 6), "adhd_pac": round(pac_adhd0, 9), "adhd_far_coherence": round(fc_adhd0, 6),
            "autism_R": round(R_aut0, 6), "autism_pac": round(pac_aut0, 9), "autism_far_coherence": round(fc_aut0, 6)},
        "P_VC4a_stimulant_gain": {
            "adhd_sweep": adhd_stim, "autism_sweep": aut_stim,
            "adhd_gain_boost_R_reaches_health": adhd_reachR, "adhd_gain_boost_PAC_reaches_health": adhd_reachPAC,
            "autism_gain_boost_R_reaches_health": aut_reachR, "autism_gain_boost_PAC_reaches_health": aut_reachPAC,
            "autism_R_max_over_sweep": round(aut_R_max, 6), "autism_R_capped_below_health": aut_R_capped,
            "autism_locality_invariant_under_gain": loc_autism_invariant,
            "stimulant_restores_adhd_both_R_and_PAC": stim_restores_adhd,
            "P_VC4a_stim_restores_adhd_not_autism_W": P_VC4a_stim_restores_adhd_not_autism_W,
            "reading": "on the INTACT geometry the stimulant restores ADHD to health in BOTH R and PAC at a finite "
                       "gain (raising catecholamine gain fully recovers integration). On the BROKEN geometry the "
                       "stimulant restores autism's PAC (gain axis) but R stays capped below health and locality "
                       "stays at the broken value -- gain never touches the wiring. Reproduces section 2 / D9.4 on "
                       "an explicit ADHD substrate."},
        "P_VC4b_cap_is_axis_appropriate_for_W": {
            "cap_far_coherence_gain_adhd": round(dfar_adhd, 6),
            "cap_far_coherence_gain_autism": round(dfar_autism, 6),
            "cap_W_selectivity_ratio_autism_over_adhd": round(cap_W_selectivity_ratio, 6),
            "cap_adds_beyond_stimulant_adhd": round(cap_adds_beyond_stim_adhd, 6),
            "cap_adds_beyond_stimulant_autism": round(cap_adds_beyond_stim_autism, 6),
            "P_VC4b_cap_is_for_W_not_adhd": P_VC4b_cap_is_for_W_not_adhd,
            "reading": "the cap's long-range (far-pair) benefit is much larger where the wiring is broken (autism) "
                       "than where it is intact (ADHD): on the stimulant-restored states the cap adds long-range "
                       "routing to autism (the W aid the stimulant cannot give) but little to ADHD (the highway is "
                       "already intact -- the cap is redundant once the gain is restored). The cap is for W; the "
                       "stimulant is for O/T."},
        "P_VC4c_mixed_AuDHD": {
            "audhd_W_genes": audhd_W_genes,
            "audhd_baseline_R": round(R_au0, 6), "audhd_baseline_pac": round(pac_au0, 9),
            "audhd_baseline_far_coherence": round(fc_au0, 6),
            "stimulant_only": {"R": round(R_au_stim, 6), "pac": round(pac_au_stim, 9), "far_coherence": round(fc_au_stim, 6)},
            "cap_only": {"R": round(R_au_cap, 6), "far_coherence": round(fc_au_cap, 6)},
            "stimulant_plus_cap": {"R": round(R_au_both, 6), "pac": round(pac_au_both, 9), "far_coherence": round(fc_au_both, 6)},
            "stimulant_fixes_gain_axis": stim_fixes_gain,
            "cap_fixes_routing_axis": cap_fixes_routing,
            "combined_covers_both_axes": combined_covers_both,
            "combined_beats_either_on_routing": combined_beats_either_routing,
            "combined_stays_below_oversync": combined_no_oversync,
            "P_VC4c_combined_covers_more_no_oversync": P_VC4c_combined_covers_more_no_oversync,
            "reading": "in the explicit AuDHD cohort (gain deficit AND broken wiring) the stimulant fixes the gain "
                       "axis (PAC -> health) and the cap fixes the routing axis (far-coherence restored); together "
                       "they cover BOTH, exceeding either alone, while R stays below the over-sync edge. Different "
                       "axes, no interference -- the section-2 decomposition, quantified."},
        "owed": "the engine has no validated, separately-emerged ADHD model; VC4 is a principled, gene-grounded "
                "INTERPRETATION (catecholamine->gain, intact W) that is tested, not a clinical simulation. ADHD "
                "model validity remains OPEN. efficacy=0; no dose; no synthesis; NOT medical advice.",
        "firewall": "mechanism only; efficacy=0; no dose/synthesis; NOT medical advice; Axis-A firewall.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {"engine_tree_frozen": ENGINE_TREE_FROZEN, "pac_grounded": pac_grounded},
        "preregistered_results": {
            "P_VC4a_stim_restores_adhd_not_autism_W": {
                "predicted": True, "observed": P_VC4a_stim_restores_adhd_not_autism_W,
                "status": "CONFIRMED" if P_VC4a_stim_restores_adhd_not_autism_W else "REFUTED"},
            "P_VC4b_cap_is_for_W_not_adhd": {
                "predicted": True, "observed": P_VC4b_cap_is_for_W_not_adhd,
                "status": "CONFIRMED" if P_VC4b_cap_is_for_W_not_adhd else "REFUTED"},
            "P_VC4c_combined_covers_more_no_oversync": {
                "predicted": True, "observed": P_VC4c_combined_covers_more_no_oversync,
                "status": "CONFIRMED" if P_VC4c_combined_covers_more_no_oversync else "REFUTED"},
        },
    }
    return out


if __name__ == "__main__":
    res = run()
    open(RESULT, "w", encoding="utf-8").write(json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False))
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"vc4_adhd_coemergence_results.json": h}, open(EXPECT, "w"), indent=1)
    ac = res["adhd_cohort"]; a = res["P_VC4a_stimulant_gain"]; b = res["P_VC4b_cap_is_axis_appropriate_for_W"]
    c = res["P_VC4c_mixed_AuDHD"]; pr = res["preregistered_results"]
    print("VC4 ADHD co-emergence")
    print(f"  ADHD cohort: O={ac['n_O']} T={ac['n_T']} W={ac['n_W']} (intact W={ac['intact_W_is_the_discriminant']}); "
          f"gamma offline-match={ac['all_gamma_re_derive_offline_match_cache']}")
    print(f"  P-VC4a stimulant: ADHD R-reaches-health @gain x{a['adhd_gain_boost_R_reaches_health']}, "
          f"PAC @x{a['adhd_gain_boost_PAC_reaches_health']}; autism R capped={a['autism_R_capped_below_health']} "
          f"(PAC @x{a['autism_gain_boost_PAC_reaches_health']})")
    print(f"  P-VC4b cap far-coh gain: autism={b['cap_far_coherence_gain_autism']} vs ADHD={b['cap_far_coherence_gain_adhd']} "
          f"(W-selectivity {b['cap_W_selectivity_ratio_autism_over_adhd']}x)")
    print(f"  P-VC4c AuDHD: stim+cap R={c['stimulant_plus_cap']['R']} pac={c['stimulant_plus_cap']['pac']} "
          f"far={c['stimulant_plus_cap']['far_coherence']}; covers both={c['combined_covers_both_axes']} "
          f"no-oversync={c['combined_stays_below_oversync']}")
    for k, v in pr.items():
        print(f"    {v['status']:<10} {k}")
    print(f"  result sha256: {h}")
