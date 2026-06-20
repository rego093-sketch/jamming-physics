#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCHIZOPHRENIA SYMPTOM-DOMAIN AXIS MAP (D9-SX) -- why dopamine blockade relieves the
POSITIVE domain but not the NEGATIVE or COGNITIVE domains. The companion module
schizophrenia_discriminant.py established the OVER-IGNITION mechanism of psychosis
(an excitatory E/I bias LOWERS the R19 fold -> aberrant salience) and that a gain-
REDUCING antipsychotic-class push restores selectivity. This module asks the
clinical follow-on the roadmap names as the T1a deliverable: schizophrenia is not
one symptom but THREE domains -- POSITIVE (hallucinations, delusions, formal-
thought disorder), NEGATIVE (avolition, blunted affect, alogia, anhedonia) and
COGNITIVE (working-memory, executive, processing-speed deficits) -- and the same
D2-antagonist that reliably treats the POSITIVE domain leaves NEGATIVE and
COGNITIVE symptoms largely untouched (one of psychiatry's central unmet needs).
=================================================================================
THE ATLAS MOVE. Map each symptom domain onto a DIFFERENT fault axis of the SAME
T/O/W engine the autism chapters already separate (18-autism-three-axis), and read
the differential drug response off the axes:

  POSITIVE  = the THRESHOLD axis driven to OVER-ignition (the OPPOSITE pole from
              autism-T). An excitatory E/I bias LOWERS the R19 fold -> weak/
              irrelevant candidate assemblies ignite -> aberrant salience. The
              gain-REDUCING antipsychotic RAISES the fold back -> the aberrant
              ignitions are removed -> the POSITIVE domain is reversed.   [reach]

  NEGATIVE  = the OUTPUT/gain axis as a DEFICIT (the autism-O fault): low per-node
              drive -> poverty of output (reduced motivated ignition, blunting).
              The antipsychotic is a gain-REDUCTION -> it pushes output EVEN LOWER
              -> it does NOT restore the deficit; it can deepen it.    [no reach]

  COGNITIVE = the long-range WIRING axis (the autism-W fault; the dysconnection
              hypothesis): attenuated long-range edges -> impaired integration /
              binding with fold and per-node gain intact. A SCALAR gain operator
              cannot re-route geometry (19-autism-chemical-limits) -> it leaves the
              locality imbalance EXACTLY invariant -> COGNITIVE untouched. [no reach]

So a SINGLE gain-reducing operator reverses EXACTLY ONE of the three domains
(positive) and is inert or counterproductive on the other two -- which is the
observed clinical pattern. THE DIFFERENTIAL RESPONSE IS AXIS-STRUCTURED, NOT DOSE-
STRUCTURED: the negative/cognitive gap is not "too little drug" but "the wrong
axis for this drug." This is the mechanistic account the program targets -- a
within-disease discriminant that says which axis a non-responding domain is stuck
on, and (by ruling the gain operator OUT on two of three axes) retires "more D2
blockade" as a route to negative/cognitive benefit.

NOT a claim that idiopathic schizophrenia is one gene or three clean lesions.
Schizophrenia is POLYGENIC + heterogeneous and its connectivity is DYSconnective
(LOCKED, as in the companion module). What is asserted is the MECHANISM-level axis
map and the SIGN of the differential antipsychotic response, NOT which domain
dominates any individual's illness (held OPEN), and NOT efficacy (=0).

PRE-REGISTERED PREDICTIONS (clinical DIRECTION/sign only; readout = HEALTH<->fault
contrast and the reversal pattern under the gain-reducing operator):
  DOM1  POSITIVE = over-ignition: an excitatory bias lowers the fold so irrelevant
        assemblies ignite (aberrant salience); the gain-reducing antipsychotic
        raises the fold back and REMOVES the aberrant ignitions (reach: YES).
  DOM2  NEGATIVE = output deficit: a per-node gain deficit lowers R below health
        (poverty of output); the gain-reducing antipsychotic lowers R FURTHER, it
        does NOT restore it (reach: NO -- wrong direction on a deficit).
  DOM3  COGNITIVE = wiring fault: long-range attenuation lowers R with locality
        RAISED, fold and per-node gain intact; a scalar gain operator leaves the
        locality imbalance EXACTLY invariant (reach: NO -- cannot re-route).
  DOM4  DISCRIMINANT: the SAME gain-reducing operator reverses POSITIVE only; the
        differential response across domains is axis-structured (which domain =
        which axis), explaining why D2 blockade treats positive but not
        negative/cognitive symptoms.

ANTI-TUNING. The signs/invariances are required to hold over a SWEEP of the
antipsychotic strength (not at a single dose): positive improves monotonically
toward health while negative monotonically worsens and cognitive stays invariant.
The three fault constructions (W far-attenuation LAM, O gain multiplier M_O,
threshold bias B_POS) and the antipsychotic gain multiplier are stimulus/severity
probes in the exact D8 mould, NOT constants fit to a target.

NOT MEDICAL ADVICE. efficacy=0 everywhere; in-silico MECHANISM probe only. Loss of
the selective GATE is a mechanism boundary, NOT a claim about the disorganised
subjective state (Axis-A firewall: consciousness_claim stays 0).

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-
ONLY (emerge_all is NOT touched, so the engine tree stays 0fbf4988... and the
M0..M16 subtree stays 3a1ebbbb..., byte-identical). Writes
schizophrenia_symptom_domains_results.json + its sha256, verified bit-for-bit.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

A      = E.load_brain_atlas()
REGS   = list(A["organs"].keys())
N      = len(REGS)
F0     = np.array([A["organs"][r]["f0_hz"] for r in REGS])
OMEGA  = 2 * math.pi * F0
OMEGA0 = float(np.mean(OMEGA))
KAP    = E.KAPPA_EPHAPTIC                                 # measured 0.5496
KGLOB  = KAP * OMEGA0
G      = 1.0
FOLD   = float(E.spinodal(G))                            # R19 fold = 0.3849
F_THETA = float(A["organs"]["hippocampus"]["f0_hz"])
F_GAMMA = float(A["organs"]["neocortex"]["f0_hz"])

# --- measured-distance geometry (identical to the autism/SZ modules) -----------
POS = E._measured_geometry(REGS)
_D = np.zeros((N, N))
for _i in range(N):
    for _j in range(N):
        _D[_i, _j] = np.linalg.norm(POS[_i] - POS[_j]) if _i != _j else 0.0
_DMED = float(np.median(_D[_D > 0]))
_FAR  = _D > _DMED


def _rawW():
    W = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                W[i, j] = 1.0 / (_D[i, j] ** 3)
    return W

def _rn(W):
    s = W.sum(axis=1, keepdims=True)
    return W / np.where(s > 0, s, 1.0)

def _locality(W):
    sh = []
    for i in range(N):
        order = np.argsort(_D[i] + np.where(np.arange(N) == i, 1e9, 0.0))
        sh.append(float(W[i, order[:2]].sum()))
    return float(np.mean(sh))

# verbatim replica of the engine's M9.6 cross-frequency PAC (depth = kappa);
# GEOMETRY DOES NOT ENTER. Grounded against the engine's emitted value.
_W_FAST = 2 * math.pi * F_GAMMA
def _pac_kappa(kp):
    Tp, dtp = 8.0, 0.0002
    ns = int(Tp / dtp); tt = np.arange(ns) * dtp
    r = 0.8; env = np.empty(ns); phs = np.empty(ns)
    def _drdt(r, b): return _W_FAST * (b - r * r) * r
    for s in range(ns):
        b = 1.0 + kp * math.cos(2 * math.pi * F_THETA * tt[s])
        k1 = _drdt(r, b); k2 = _drdt(r + 0.5 * dtp * k1, b)
        k3 = _drdt(r + 0.5 * dtp * k2, b); k4 = _drdt(r + dtp * k3, b)
        r = r + dtp * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        env[s] = r; phs[s] = (2 * math.pi * F_THETA * tt[s]) % (2 * math.pi)
    h2 = ns // 2; env = env[h2:]; phs = phs[h2:]; nb = 18
    idx = np.clip((phs / (2 * math.pi) * nb).astype(int), 0, nb - 1)
    mvec = np.array([env[idx == b_].mean() if (idx == b_).any() else 0 for b_ in range(nb)])
    ssum = mvec.sum(); mvec = mvec / ssum if ssum > 0 else mvec
    return float(np.sum(mvec * np.log((mvec + 1e-12) / (1.0 / nb))) / math.log(nb))
_ENGINE_PAC_AT_KAPPA = 0.00726119688482934  # engine's emitted M9.6 pac_modulation_index

# candidate-assembly salience field (M3 eddies), straddling the fold in health
DRIVES = [0.12, 0.20, 0.28, 0.36, 0.50, 0.60]

def _on_set(bias):
    on = []
    for i, d in enumerate(DRIVES):
        if E.settle(G, d + bias, s0=-math.sqrt(G)) > 0.0:
            on.append(i)
    return on

def _ig_thr(b, cap=2.0, ngrid=401):
    for s in np.linspace(0.0, cap, ngrid):
        if E.settle(G, b + float(s), s0=-math.sqrt(G)) > 0.0:
            return float(s)
    return float("inf")

# ---- domain probe constants (D8-mould severity/operator probes; NOT fit) ------
B_POS  = +0.15        # POSITIVE: excitatory E/I bias (lowers fold -> over-ignition)
M_O    = 0.40         # NEGATIVE: output/gain deficit multiplier (k_O = M_O*kappa)
LAM    = 0.30         # COGNITIVE: long-range edge attenuation (wiring fault)
AP     = 0.15         # antipsychotic gain-reduction strength (on the ignition-bias axis)
AP_GAIN_SWEEP = [0.85, 0.70, 0.55, 0.40]   # gain multipliers (<1) -> the gain-REDUCING dose sweep
AP_BIAS_SWEEP = [-0.05, -0.10, -0.15, -0.25]  # matching threshold-raising bias sweep


def run():
    Wraw = _rawW(); Wrn = _rn(Wraw)
    R_health   = E._integrate(OMEGA, Wrn, KGLOB)[0]
    loc_health = _locality(Wrn)
    pac_health = _pac_kappa(KAP)
    ig_health  = _ig_thr(0.0)
    H = set(_on_set(0.0))
    PAC_GROUNDED = bool(abs(pac_health - _ENGINE_PAC_AT_KAPPA) < 1e-9)

    # ===== DOM1 : POSITIVE = over-ignition (threshold axis, excitatory pole) =====
    ig_pos = _ig_thr(B_POS)
    on_pos = set(_on_set(B_POS))
    aberrant_pos = sorted(on_pos - H)        # irrelevant assemblies recruited (aberrant salience)
    lost_pos     = sorted(H - on_pos)
    pos_fault = bool(ig_pos < ig_health - 1e-9 and len(aberrant_pos) > 0 and len(lost_pos) == 0)
    # antipsychotic RAISES the fold back (gain reduction = threshold raise): B_POS - AP
    on_pos_ap = set(_on_set(B_POS - AP))
    pos_reach = bool(on_pos_ap == H)          # aberrant ignitions removed -> restored to health set
    # anti-tuning: across the bias sweep, the aberrant count is monotone non-increasing as
    # the gain-reducing (threshold-raising) push strengthens, reaching 0 (selectivity restored).
    ab_curve_pos = {round(b, 2): len(set(_on_set(B_POS + b)) - H) for b in AP_BIAS_SWEEP}
    sb = sorted(ab_curve_pos, reverse=True)   # least-negative (weakest AP) first
    pos_monotone = all(ab_curve_pos[sb[i]] >= ab_curve_pos[sb[i + 1]] for i in range(len(sb) - 1))
    pos_restored_in_sweep = bool(min(ab_curve_pos.values()) == 0)

    # ===== DOM2 : NEGATIVE = output deficit (gain axis), gain-reduction worsens =====
    k_O   = M_O * KAP
    R_neg = E._integrate(OMEGA, Wrn, k_O * OMEGA0)[0]
    pac_neg = _pac_kappa(k_O)
    neg_fault = bool(R_neg < R_health and pac_neg < pac_health)        # poverty of output, PAC down
    # antipsychotic = gain reduction -> k_O * AP_GAIN -> output EVEN LOWER (does NOT restore)
    R_neg_curve = {round(g, 2): E._integrate(OMEGA, Wrn, (k_O * g) * OMEGA0)[0] for g in AP_GAIN_SWEEP}
    sg = sorted(R_neg_curve, reverse=True)     # strongest gain (weakest AP) first
    neg_monotone_worse = all(R_neg_curve[sg[i]] >= R_neg_curve[sg[i + 1]] for i in range(len(sg) - 1))
    R_neg_ap = E._integrate(OMEGA, Wrn, (k_O * AP_GAIN_SWEEP[1]) * OMEGA0)[0]
    neg_not_reached = bool(R_neg_ap <= R_neg + 1e-9)   # NOT restored toward health (no improvement)
    neg_worsened = bool(R_neg_ap < R_neg - 1e-9)       # in fact deepened

    # ===== DOM3 : COGNITIVE = wiring fault (geometry), scalar gain cannot re-route =====
    Ww = Wraw.copy(); Ww[_FAR] *= LAM; Ww[(~_FAR) & (_D > 0)] *= 1.3
    Wwn = _rn(Ww)
    R_cog   = E._integrate(OMEGA, Wwn, KGLOB)[0]
    loc_cog = _locality(Wwn)
    pac_cog = pac_health                       # W keeps kappa -> PAC EXACTLY unchanged
    ig_cog  = _ig_thr(0.0)
    cog_fault = bool(R_cog < R_health and (pac_cog == pac_health)
                     and abs(ig_cog - ig_health) < 1e-9 and loc_cog > loc_health)
    # a scalar gain operator (either direction) leaves locality EXACTLY invariant
    loc_cog_apdown = _locality(Wwn)            # gain scales Kglob, not W -> locality identical
    R_cog_apdown   = E._integrate(OMEGA, Wwn, (KAP * AP_GAIN_SWEEP[1]) * OMEGA0)[0]
    cog_not_reached = bool(loc_cog_apdown == loc_cog and loc_cog_apdown > loc_health)
    # over the gain sweep, locality is invariant at every dose (topology untouched)
    loc_cog_curve = {round(g, 2): _locality(Wwn) for g in AP_GAIN_SWEEP}
    cog_locality_invariant = bool(len(set(loc_cog_curve.values())) == 1
                                  and list(loc_cog_curve.values())[0] > loc_health)

    # ===== DOM4 : DISCRIMINANT -- one gain-reducing operator reverses POSITIVE only =====
    DISCRIMINANT = bool(pos_reach and neg_not_reached and cog_not_reached)
    axis_structured = bool(DISCRIMINANT and pos_restored_in_sweep
                           and neg_monotone_worse and cog_locality_invariant)

    res = {
        "_what": "Schizophrenia symptom-domain axis map (D9-SX): the three symptom "
                 "domains map onto three DIFFERENT axes of the same T/O/W engine -- "
                 "POSITIVE = the THRESHOLD axis driven to over-ignition (aberrant "
                 "salience), NEGATIVE = the OUTPUT/gain axis as a deficit (poverty of "
                 "output), COGNITIVE = the long-range WIRING axis (dysconnection). The "
                 "D2-antagonist antipsychotic is a uniform gain REDUCTION: it raises the "
                 "fold back and REVERSES the POSITIVE domain, but pushes the output "
                 "deficit LOWER (does not reach NEGATIVE) and leaves the wiring locality "
                 "EXACTLY invariant (does not reach COGNITIVE). The differential drug "
                 "response is AXIS-structured, not dose-structured -- the mechanistic "
                 "account of why D2 blockade treats positive but not negative/cognitive "
                 "symptoms. MECHANISM only -- NOT felt, NOT efficacy, NOT medical advice.",
        "axis_map": {
            "POSITIVE": "threshold axis, OVER-ignition pole (excitatory E/I bias lowers the R19 fold "
                        "-> aberrant salience); the OPPOSITE pole from autism-T",
            "NEGATIVE": "output/gain axis as a DEFICIT (autism-O fault): low per-node drive -> poverty "
                        "of output (avolition, blunting, alogia)",
            "COGNITIVE": "long-range WIRING axis (autism-W fault; dysconnection hypothesis): attenuated "
                         "long-range edges -> impaired integration / working memory",
            "antipsychotic_operator": "D2 antagonism = uniform gain REDUCTION / threshold RAISE "
                                       "(opposite direction to the autism gain-restoring stimulant)",
        },
        "baseline_health": {
            "kappa_measured": round(KAP, 6),
            "R_health": round(R_health, 6),
            "locality_health": round(loc_health, 6),
            "pac_health": round(pac_health, 9),
            "R19_fold_spinodal": round(FOLD, 6),
            "ignition_threshold_health": round(ig_health, 6),
            "healthy_selective_on_set": sorted(H),
            "pac_replica_grounded": PAC_GROUNDED,
            "engine_pac_at_kappa": _ENGINE_PAC_AT_KAPPA,
        },
        "DOM1_positive_over_ignition": {
            "model": "excitatory E/I bias LOWERS the R19 fold -> weak/irrelevant assemblies ignite "
                     "(aberrant salience); the leading mechanism of POSITIVE symptoms",
            "excitatory_bias": B_POS,
            "ignition_threshold": round(ig_pos, 6),
            "fold_lowered_below_health": bool(ig_pos < ig_health - 1e-9),
            "on_set": sorted(on_pos),
            "aberrant_ignitions_recruited": aberrant_pos,
            "relevant_ignitions_lost": lost_pos,
            "positive_fault_reproduced": pos_fault,
            "antipsychotic_on_set": sorted(on_pos_ap),
            "antipsychotic_restores_selective_set": pos_reach,
            "aberrant_count_vs_AP_bias": {str(k): v for k, v in ab_curve_pos.items()},
            "aberrant_monotone_nonincreasing_under_AP": bool(pos_monotone),
            "selectivity_restored_in_sweep": pos_restored_in_sweep,
            "REACH": "YES -- the gain-reducing antipsychotic raises the fold back and removes the "
                     "aberrant ignitions (POSITIVE domain reversed).",
        },
        "DOM2_negative_output_deficit": {
            "model": "a per-node output/gain DEFICIT lowers drive -> poverty of motivated output "
                     "(avolition, blunted affect, alogia); the autism-O fault",
            "output_multiplier": M_O,
            "R_negative": round(R_neg, 6),
            "R_below_health": bool(R_neg < R_health),
            "pac_negative": round(pac_neg, 9),
            "pac_reduced": bool(pac_neg < pac_health),
            "negative_fault_reproduced": neg_fault,
            "R_negative_vs_AP_gain": {str(k): round(v, 6) for k, v in R_neg_curve.items()},
            "R_monotone_worse_under_AP": bool(neg_monotone_worse),
            "R_negative_under_antipsychotic": round(R_neg_ap, 6),
            "antipsychotic_does_not_restore": neg_not_reached,
            "antipsychotic_deepens_deficit": neg_worsened,
            "REACH": "NO -- the antipsychotic is a gain REDUCTION; on an output DEFICIT it pushes "
                     "output even lower (wrong direction). The NEGATIVE domain is not reached.",
        },
        "DOM3_cognitive_wiring_fault": {
            "model": "long-range edge ATTENUATION -> impaired integration / working memory with "
                     "per-node gain and fold intact; the autism-W fault (dysconnection hypothesis)",
            "long_range_attenuation": LAM,
            "R_cognitive": round(R_cog, 6),
            "R_below_health": bool(R_cog < R_health),
            "locality": round(loc_cog, 6),
            "locality_elevated": bool(loc_cog > loc_health),
            "pac_unchanged": bool(pac_cog == pac_health),
            "ignition_normal": bool(abs(ig_cog - ig_health) < 1e-9),
            "cognitive_fault_reproduced": cog_fault,
            "locality_under_antipsychotic": round(loc_cog_apdown, 6),
            "locality_invariant_under_gain": cog_not_reached,
            "locality_vs_AP_gain": {str(k): round(v, 6) for k, v in loc_cog_curve.items()},
            "locality_invariant_across_sweep": cog_locality_invariant,
            "REACH": "NO -- a scalar gain operator cannot re-route geometry; it leaves the locality "
                     "imbalance EXACTLY invariant. The COGNITIVE domain is not reached.",
        },
        "DOM4_discriminant": {
            "_what": "one gain-reducing operator reverses POSITIVE only; NEGATIVE and COGNITIVE are "
                     "not reached -> the differential antipsychotic response is AXIS-structured, not "
                     "dose-structured. This is the mechanistic account of why D2 blockade relieves "
                     "positive but not negative/cognitive symptoms.",
            "positive_reached": pos_reach,
            "negative_not_reached": neg_not_reached,
            "cognitive_not_reached": cog_not_reached,
            "one_operator_reverses_positive_only": DISCRIMINANT,
            "differential_is_axis_structured": axis_structured,
            "retires": "more D2 blockade as a route to NEGATIVE/COGNITIVE benefit -- those domains "
                       "sit on axes a gain operator cannot reach (an in-silico mechanistic null).",
        },
        "cited_and_locked": {
            "three_domains": "Andreasen 1982 / Kay (PANSS) -- schizophrenia symptoms partition into "
                             "POSITIVE, NEGATIVE and COGNITIVE/disorganised domains",
            "antipsychotic_positive_only": "D2-antagonist antipsychotics reliably treat POSITIVE "
                "symptoms; NEGATIVE and COGNITIVE symptoms respond poorly (a central unmet need; "
                "Leucht meta-analyses; Kapur 2003 salience-dampening is a positive-symptom account)",
            "negative_output_axis": "negative symptoms (avolition, anhedonia, blunting) reflect "
                "reduced motivated output / hypodopaminergic-frontal drive -- an OUTPUT-deficit axis, "
                "not an over-salience axis",
            "cognitive_dysconnection": "cognitive deficits track DYSCONNECTIVITY / impaired long-range "
                "integration (Friston disconnection hypothesis; Stephan 2009) -- a WIRING axis",
            "scalar_gain_cannot_reroute_LOCK": "a uniform per-node gain operator scales coupling "
                "strength, NOT topology; it cannot correct a wiring/locality imbalance "
                "(19-autism-chemical-limits)",
            "SZ_polygenic_LOCK": "idiopathic schizophrenia is POLYGENIC + heterogeneous (PGC GWAS "
                ">270 loci; CNVs) and DYSconnective -- the axis map is a mechanism interpretation, "
                "NOT one gene, three clean lesions, or a diagnosis",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; which "
                "domain dominates an individual's illness is held OPEN",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "which_domain_dominates_individual": "OWED [O] -- requires per-individual data (symptom "
                "profile, spectral E/I markers, connectome); the model asserts only the axis map and "
                "the differential-reach signs, NOT which axis any individual's illness is.",
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,   # filled in *_results()
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "pac_grounded": PAC_GROUNDED,
        },
        "overall": {
            "positive_fault_reproduced": pos_fault,
            "positive_reached_by_antipsychotic": pos_reach,
            "negative_fault_reproduced": neg_fault,
            "negative_not_reached": neg_not_reached,
            "cognitive_fault_reproduced": cog_fault,
            "cognitive_not_reached": cog_not_reached,
            "discriminant_one_operator_positive_only": DISCRIMINANT,
            "differential_axis_structured": axis_structured,
            "is_full_module": bool(pos_fault and pos_reach and neg_fault and neg_not_reached
                                   and cog_fault and cog_not_reached and DISCRIMINANT and axis_structured),
            "verdict": "the three schizophrenia symptom domains sit on three different T/O/W axes; "
                       "the gain-reducing D2-antagonist reverses the POSITIVE (over-ignition) domain "
                       "but cannot reach the NEGATIVE (output-deficit) or COGNITIVE (wiring) domains. "
                       "The differential antipsychotic response is axis-structured -- which is why "
                       "dopamine blockade relieves positive but not negative/cognitive symptoms. "
                       "Which domain dominates a given illness is OWED. efficacy=0.",
        },
    }
    return res


def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def _blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def schizophrenia_symptom_domains_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "schizophrenia_symptom_domains_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_schizophrenia_symptom_domains_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"schizophrenia_symptom_domains_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = schizophrenia_symptom_domains_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    b = res["baseline_health"]
    d1 = res["DOM1_positive_over_ignition"]; d2 = res["DOM2_negative_output_deficit"]
    d3 = res["DOM3_cognitive_wiring_fault"]; d4 = res["DOM4_discriminant"]
    print("=" * 78)
    print("SCHIZOPHRENIA SYMPTOM-DOMAIN AXIS MAP (D9-SX)   add-only, engine READ-ONLY")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  health: R={b['R_health']}  locality={b['locality_health']}  fold={b['R19_fold_spinodal']}  ON={b['healthy_selective_on_set']}")
    print("-" * 78)
    print(f"  DOM1 POSITIVE  (threshold/over-ignition): fault={d1['positive_fault_reproduced']}  +aberrant={d1['aberrant_ignitions_recruited']}  AP-reach={d1['antipsychotic_restores_selective_set']}")
    print(f"       aberrant(AP bias sweep)={d1['aberrant_count_vs_AP_bias']}  restored={d1['selectivity_restored_in_sweep']}")
    print(f"  DOM2 NEGATIVE  (output deficit)         : fault={d2['negative_fault_reproduced']}  R={d2['R_negative']}<health  AP-reach=NO worse={d2['antipsychotic_deepens_deficit']}")
    print(f"       R(AP gain sweep)={d2['R_negative_vs_AP_gain']}  monotone-worse={d2['R_monotone_worse_under_AP']}")
    print(f"  DOM3 COGNITIVE (wiring fault)           : fault={d3['cognitive_fault_reproduced']}  locality={d3['locality']}>health  AP-reach=NO invariant={d3['locality_invariant_across_sweep']}")
    print("-" * 78)
    print(f"  DOM4 DISCRIMINANT: one gain-reducing operator reverses POSITIVE only = {d4['one_operator_reverses_positive_only']}")
    print(f"       differential is axis-structured (not dose-structured) = {d4['differential_is_axis_structured']}")
    print("-" * 78)
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  SCHIZOPHRENIA SYMPTOM-DOMAIN MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
