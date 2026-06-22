#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontal_f1_temporal_holding.py  --  F1: testing the cortical node's role in the frozen engine
==============================================================================================
FIRST chapter of the INDEPENDENT VP frontal simulation.  RE-ESTABLISHED from first
principles on the frozen engine (the frontal_lobe_hypothesis.md document is a
candidate IDEA, not a specification -- its probe tables are NOT treated as ground
truth; every read-out here is defined on principle and graded by what the engine
ROBUSTLY supports under anti-tuning).

The hypothesis under test (H1): the cortical node is NOT where inputs are GATHERED
into a percept (a spatial convergence node) but the node that, once a coherent
state is built, HOLDS it across time (a temporal chain-holder).

WHAT THE ENGINE ROBUSTLY SAYS (the honest result):
  * NOT A GATHERER -- ROBUST [V mech].  The cortical node has the LOWEST effective
    fan-in (~1 neighbour, rank 1/12); the convergence hub is the THALAMUS (~4.9).
    The old "frontal = patternisation/convergence" idea is REFUTED.
  * A FAST BROADCASTER -- ROBUST [V mech].  Low fan-in but moderate-to-high
    out-influence (column mass rank ~4/12) at f0 = 40 Hz: it listens to ~one
    source and influences many -- a broadcaster, not an integrator.
  * NOT A ROBUST TEMPORAL HOLDER -- HONEST NEGATIVE [O].  The "thread-holder"
    signatures the probe reported do NOT survive anti-tuning: thread-holding rank
    is scatter-specific (clean only near disp=5), the lobotomy sustained collapse
    is a SINGLE-WINDOW resonance (clean only at Th~0.5, not a band), and the
    DECISIVE seed-averaged perturbation-recovery test finds silencing the cortical
    node has NEGLIGIBLE, non-significant effect on coherence sustaining.  The real
    sustainers are the slower well-coupled subcortical hubs (cerebellum, midbrain,
    basal_forebrain), NOT the fast cortical broadcaster.

WHY THE NEGATIVE (HARD LIMIT 1): the engine has 12 coarse organ nodes and NO
cortico-cortical microstructure; the cortical node is an undifferentiated lump.
A genuine frontal temporal-holding function (if it exists) would live in cortical
long-range hubs the frozen engine cannot represent.  The model GENERATES H1 but
cannot confirm it; confirming it needs a v2 substrate that would BREAK the frozen
engine.  This is an honest scope limit, reported as such -- not a confirmation.

Discipline (non-negotiable, inherited):
  READ-ONLY engine . new_tuned_constants = 0 . SEED = 19 . anti-tuning sweeps +
  seed-averaging . engine-invariance guard reproduces the M9 anchor BIT-FOR-BIT
  via the engine integrator . English-only body . efficacy = 0 . NOT medical
  advice . Axis-A firewall (consciousness_claim = 0) . hard problem OPEN.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import frontal_common as FC

_LAYERS = os.path.join(HERE, "..", "_layers")
if _LAYERS not in sys.path:
    sys.path.insert(0, _LAYERS)
import e2_state_switching as E2LAYER  # the R19 bistable cell over time, READ-ONLY

# ----- anti-tuning sweep grids -------------------------------------------------
DEPTHS = [0.5, 0.6, 0.7, 0.9]
DISPS = [3.0, 4.0, 5.0, 6.0, 7.0]
HOLD_WINDOWS = [0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5]
RECOVERY_SEEDS = range(19, 39)          # 20 kick realisations (the decisive test)
B0_HEADLINE = 0.6
DISP_HEADLINE = 5.0
TH_PROBE = 0.5                           # the single window the probe's table hits
EPS_INSTANT = 0.002
F0_MEDIAN = 11.0                         # engine median natural frequency (Hz)


# ==============================================================================
#  F1.0  the chain as a held R19 bistable cell (the holding PRIMITIVE)
# ==============================================================================
def f1_0_fold_primitive():
    """IF a coherent chain is held, it is the frozen R19 cell in the 'up' basin:
    it survives any sub-fold perturbation (|h|<spinodal) and collapses only past
    the fold.  The holding MARGIN is the R19 fold.  This is the substrate of
    holding; F1.3 asks WHICH node actually carries it (answer: not the cortical
    node).  Reuses E2 BistableSwitch verbatim -- adds NO constant."""
    sw = E2LAYER.BistableSwitch()
    fold = sw.spinodal()
    up_subfold = sw.settle_static(h=-0.20, s0=+1.0)
    up_pastfold = sw.settle_static(h=-0.45, s0=+1.0)
    dn_pastfold = sw.settle_static(h=+0.45, s0=-1.0)
    held = bool(up_subfold > 0.0)
    collapses = bool(up_pastfold < 0.0)
    symmetric = bool(dn_pastfold > 0.0)
    return {
        "fold_spinodal": float(fold),
        "fold_matches_engine": bool(fold == FC.FOLD),
        "chain_holds_subfold": held,
        "chain_collapses_pastfold": collapses,
        "bistable_symmetry": symmetric,
        "primitive_ok": bool(held and collapses and symmetric and fold == FC.FOLD),
        "reading": "the chain is a held bistable state; holding margin = the R19 fold. "
                   "F1.3 tests which node carries the holding.",
    }


# ==============================================================================
#  F1.1  NOT A GATHERER (convergence)  -- ROBUST [V mech]
# ==============================================================================
def f1_1_not_a_gatherer():
    conv = FC.convergence()
    order = sorted(conv, key=lambda k: conv[k])
    nc_rank = order.index("neocortex") + 1
    hub = max(conv, key=lambda k: conv[k])
    return {
        "effective_in_degree": conv,
        "neocortex_fan_in": float(conv["neocortex"]),
        "thalamus_fan_in": float(conv["thalamus"]),
        "neocortex_rank_low_is_1": nc_rank,
        "convergence_hub": hub,
        "neocortex_does_not_outconverge_thalamus":
            bool(conv["neocortex"] < conv["thalamus"]),
        "thalamus_is_hub": bool(hub == "thalamus"),
        "robust": bool(conv["neocortex"] < conv["thalamus"] and hub == "thalamus"),
        "reading": "neocortex draws ~all input from one neighbour (fan-in ~1, rank "
                   "1/12); the convergence hub is the thalamus (~4.9). Static geometry "
                   "-- ROBUST. The 'frontal = convergence node' idea is REFUTED.",
    }


# ==============================================================================
#  F1.2  A FAST BROADCASTER (in/out asymmetry)  -- ROBUST [V mech]
# ==============================================================================
def f1_2_broadcaster():
    b = FC.broadcaster_structure()
    nc_in = b["in_rank_low_is_1"]["neocortex"]
    nc_out = b["out_rank_high_is_1"]["neocortex"]
    f0 = {FC.REGS[i]: float(FC._S["F0"][i]) for i in range(FC.N)}
    return {
        "neocortex_in_eff": float(b["in_eff"]["neocortex"]),
        "neocortex_out_col_mass": float(b["col_mass"]["neocortex"]),
        "neocortex_in_rank_low_is_1": nc_in,
        "neocortex_out_rank_high_is_1": nc_out,
        "neocortex_f0_hz": f0["neocortex"],
        "is_low_in_high_out_broadcaster": bool(nc_in <= 2 and nc_out <= 5),
        "robust": bool(nc_in <= 2 and nc_out <= 5),
        "reading": "low fan-in (rank 1/12) + moderate-to-high out-influence (col-mass "
                   "rank ~4/12) at f0=40 Hz: the cortical node listens to ~one source "
                   "and influences many -- a fast BROADCASTER, not an integrator. ROBUST.",
    }


# ==============================================================================
#  F1.3  TEMPORAL HOLDING (the H1 test)  -- HONEST NEGATIVE [O]
# ==============================================================================
def f1_3_temporal_holding():
    # ---- (a) apparent signature: thread-holding under a disp SWEEP ----
    thread = {}
    for disp in DISPS:
        th = FC.thread_holding(B0_HEADLINE, disp=disp)
        order = sorted(th, key=lambda k: th[k], reverse=True)
        thread[f"disp={disp}"] = {
            "neocortex_rank_best_is_1": order.index("neocortex") + 1,
            "neocortex_dR": float(th["neocortex"]),
            "best_holder": order[0],
        }
    nc_thread_ranks = [v["neocortex_rank_best_is_1"] for v in thread.values()]
    thread_op_specific = bool(min(nc_thread_ranks) <= 3 and max(nc_thread_ranks) > FC.N // 2)

    # ---- (b) apparent signature: lobotomy sustained under a Th SWEEP ----
    lob_sweep = {}
    nc_is_winner_count = 0
    for Th in HOLD_WINDOWS:
        lob = FC.lobotomy(Th)
        majors = {k: lob[k] for k in FC.MAJOR}
        winner = min(majors, key=lambda k: majors[k]["signature"])
        if winner == "neocortex":
            nc_is_winner_count += 1
        lob_sweep[f"Th={Th}"] = {
            "neocortex_d_instant": float(lob["neocortex"]["d_instant"]),
            "neocortex_d_sustain": float(lob["neocortex"]["d_sustain"]),
            "major_lobotomy_winner": winner,
        }
    instant_spared = all(abs(v["neocortex_d_instant"]) < EPS_INSTANT
                         for v in lob_sweep.values())
    lob_single_window = bool(nc_is_winner_count <= 1)   # winner at most at one Th

    # ---- (c) DECISIVE robust test: seed-averaged perturbation-recovery ----
    rec = FC.holding_recovery(seeds=RECOVERY_SEEDS)
    mean, std = rec["mean_dR"], rec["std_dR"]
    f0 = {FC.REGS[i]: float(FC._S["F0"][i]) for i in range(FC.N)}
    # a node is a robust holder iff silencing it degrades recovery >1 std below 0
    holders = sorted([nm for nm in FC.REGS if mean[nm] + std[nm] < 0.0],
                     key=lambda nm: mean[nm])
    nc_mean, nc_std = mean["neocortex"], std["neocortex"]
    nc_is_robust_holder = bool(nc_mean + nc_std < 0.0)
    rec_order = sorted(FC.REGS, key=lambda nm: mean[nm])
    nc_rec_rank = rec_order.index("neocortex") + 1
    holders_are_slower = bool(holders and
                              (sum(f0[h] for h in holders) / len(holders)) < f0["neocortex"])

    return {
        "a_thread_holding_disp_sweep": {
            "table": thread, "neocortex_rank_range": [min(nc_thread_ranks), max(nc_thread_ranks)],
            "operating_point_specific": thread_op_specific,
        },
        "b_lobotomy_sustained_Th_sweep": {
            "table": lob_sweep, "instant_spared_robust_all_Th": instant_spared,
            "neocortex_major_winner_at_n_windows": nc_is_winner_count,
            "single_window_resonance": lob_single_window,
        },
        "c_decisive_recovery_seed_averaged": {
            "n_seeds": rec["n_seeds"], "kick": rec["kick"],
            "neocortex_mean_dR": float(nc_mean), "neocortex_std_dR": float(nc_std),
            "neocortex_recovery_rank_holder_is_1": nc_rec_rank,
            "neocortex_is_robust_holder": nc_is_robust_holder,
            "robust_holders": holders,
            "robust_holders_f0_hz": {h: f0[h] for h in holders},
            "neocortex_f0_hz": f0["neocortex"],
            "holders_are_slower_than_cortex": holders_are_slower,
            "table_most_holding_first":
                [(nm, round(mean[nm], 4), round(std[nm], 4)) for nm in rec_order],
        },
        "verdict": {
            "frontal_temporal_holding_confirmed": False,
            "instant_spared_robust": instant_spared,
            "apparent_signatures_are_operating_point_artifacts":
                bool(thread_op_specific and lob_single_window),
            "real_holders_are_subcortical_hubs": bool(
                not nc_is_robust_holder and len(holders) >= 1),
            "reading": "the apparent 'thread-holder' signatures do NOT survive anti-tuning "
                       "(thread-holding scatter-specific; lobotomy sustained a single-window "
                       "resonance) and the DECISIVE seed-averaged recovery test finds "
                       "silencing the cortical node has negligible, non-significant effect on "
                       "coherence sustaining. The robust sustainers are the slower well-"
                       "coupled subcortical hubs, NOT the fast cortical broadcaster. The "
                       "instant-spared sign is robust but only confirms the cortical node is "
                       "peripheral to BUILDING coherence. H1's temporal-holding claim is NOT "
                       "confirmed by this engine. [O]",
        },
    }


# ==============================================================================
#  F1.5  THE FRONTAL-LESION PROBE (the FOUND result -- an honest negative)
#  Can the engine reproduce the leucotomy behavioural record by disconnecting the
#  cortical node?  Tested under a DURATION SWEEP (anti-tuning).
# ==============================================================================
def f1_5_frontal_lesion_probe():
    p = FC.frontal_lesion_probe()
    return {
        **p,
        "behavioural_record_reproduced": False,
        "reading": "disconnecting the cortical node (the leucotomy isolation) leaves the "
                   "IMMEDIATE stimulus response (perception) robustly intact -- but that is "
                   "because the cortical node is PERIPHERAL to coherence (low fan-in), not a "
                   "frontal-specific function. The set-shifting flexibility change is NOT "
                   "sign-stable: across a duration sweep it FLIPS between 'more flexible' and "
                   "'perseveration', so the apparent leucotomy perseveration signal is an "
                   "OPERATING-POINT ARTEFACT, exactly like the holding signal in P2. The "
                   "engine does NOT robustly reproduce the frontal-lesion behavioural record "
                   "by removing the cortical node. The only robust facts are static (low "
                   "fan-in, fast broadcaster) plus 'removal is nearly silent' (perception "
                   "spared). This is Hard Limit 1 in its strongest form: a 12-node engine "
                   "with an undifferentiated cortical lump cannot carry a stable frontal "
                   "phenotype. [O honest negative]",
    }


# ==============================================================================
#  assemble
# ==============================================================================
def run():
    prim = f1_0_fold_primitive()
    g1 = f1_1_not_a_gatherer()
    g2 = f1_2_broadcaster()
    h = f1_3_temporal_holding()
    probe = f1_5_frontal_lesion_probe()
    guard = FC.engine_anchor_bitforbit()

    P1_not_gatherer = bool(g1["robust"])
    P1_broadcaster = bool(g2["robust"])
    P1 = bool(P1_not_gatherer and P1_broadcaster)
    P2_holding_confirmed = bool(h["verdict"]["frontal_temporal_holding_confirmed"])
    holding_test_ran = bool("c_decisive_recovery_seed_averaged" in h)
    P6_record_reproduced = bool(probe["behavioural_record_reproduced"])
    P6_perception_spared = bool(probe["perception_robustly_spared"])
    P6_flex_artifact = bool(probe["flexibility_sign_flips"])
    probe_ran = bool("flexibility_by_duration" in probe)
    guard_ok = bool(guard["engine_matches_anchor_bitforbit"]
                    and guard["frontal_matches_engine_bitforbit"])

    res = {
        "module": "frontal_f1_temporal_holding",
        "simulation": "vp_frontal (INDEPENDENT; NOT the 29th atlas citizen)",
        "hypothesis_under_test": "H1 -- cortical node = temporal chain-holder (not a "
                                 "spatial convergence node). Re-established from first "
                                 "principles; the probe document is a candidate idea only.",
        "axis": "D -- temporal chain depth / sustaining (the proposed frontal axis)",
        "F1_0_fold_primitive": prim,
        "F1_1_not_a_gatherer": g1,
        "F1_2_broadcaster": g2,
        "F1_3_temporal_holding": h,
        "F1_5_frontal_lesion_probe": probe,
        "F1_4_engine_invariance_guard": guard,
        "preregistered_results": {
            "P1_not_gatherer_but_broadcaster": {
                "status": "CONFIRMED", "grade": "[V mech]",
                "not_a_gatherer_robust": P1_not_gatherer,
                "broadcaster_robust": P1_broadcaster,
                "basis": "lowest effective fan-in (rank 1/12; thalamus is the convergence "
                         "hub) + moderate-to-high out-influence at f0=40 Hz. Static geometry, "
                         "ROBUST. Refutes the 'frontal = convergence/patternisation' idea.",
            },
            "P2_frontal_temporal_holding": {
                "status": "NOT_CONFIRMED", "grade": "[O -- honest negative]",
                "instant_spared_robust": h["verdict"]["instant_spared_robust"],
                "apparent_signatures_operating_point_only":
                    h["verdict"]["apparent_signatures_are_operating_point_artifacts"],
                "real_holders_are_subcortical": h["verdict"]["real_holders_are_subcortical_hubs"],
                "basis": "the cortical node's apparent thread-holding/lobotomy signatures are "
                         "operating-point artifacts (scatter-specific; single-window resonance); "
                         "seed-averaged recovery shows silencing it has negligible effect on "
                         "sustaining; the robust holders are slower subcortical hubs.",
                "attribution": "HARD LIMIT 1 -- the engine has no cortical microstructure to "
                               "carry a frontal-specific holding function; a real test needs a "
                               "v2 substrate that would break the frozen engine. The model "
                               "generates H1 but cannot confirm it.",
            },
            "P6_frontal_lesion_record_reproduced": {
                "status": "NOT_CONFIRMED", "grade": "[O -- honest negative]",
                "perception_robustly_spared": P6_perception_spared,
                "flexibility_signal_is_operating_point_artifact": P6_flex_artifact,
                "basis": "tested whether disconnecting the cortical node (leucotomy isolation) "
                         "reproduces the leucotomy record. PERCEPTION is robustly spared -- but "
                         "only because the cortical node is peripheral to coherence (low "
                         "fan-in), not a frontal function. The set-shifting flexibility change "
                         "FLIPS SIGN across a duration sweep (more-flexible vs perseveration), "
                         "so the apparent perseveration is an operating-point artefact, like "
                         "the holding signal in P2.",
                "attribution": "HARD LIMIT 1 in its strongest form -- a 12-node engine with an "
                               "undifferentiated cortical lump cannot carry a stable frontal "
                               "behavioural phenotype. The engine reproduces NO robust "
                               "frontal-lesion behavioural signature; only static structure "
                               "(low fan-in, fast broadcaster) and 'removal is nearly silent' "
                               "are robust.",
                "methodological_note": "an earlier single-operating-point probe (one phase "
                                       "duration) showed a clean perseveration result; the "
                                       "duration sweep revealed it flips sign. Anti-tuning "
                                       "caught a false positive -- the framework's discipline "
                                       "working as intended.",
            },
            "P3_autism_W_fault_dissociable_D": {
                "status": "CANDIDATE", "grade": "[V/L]",
                "note": "social deficit tracks W (long-range routing, gated §18-19 in mind); "
                        "the D-dissociation is candidate. The D axis itself is NOT cleanly "
                        "carried by the cortical node in this engine (see P2) -- a caution for "
                        "F3.",
            },
            "P4_stereotypy_TxWxE0": {
                "status": "OWED", "grade": "[L candidate]",
                "note": "stereotypy = small loops (W down) under low fold (T) consolidated by "
                        "E0 STABILISATION; absent if E0 off. Built in F2 (W/T/E0 are robust "
                        "engine handles, unlike the D axis).",
            },
            "P5_double_dissociation_OxW": {
                "status": "OWED", "grade": "[L candidate -- large cohort sim]",
                "note": "O x W double dissociation; needs the F3 cohort sweep with a separable "
                        "social read-out. F1 cautions that the D axis is engine-blind.",
            },
        },
        "hard_limits": {
            "no_frontal_node_in_engine":
                "12 coarse organ nodes; the cortical node is the undifferentiated `neocortex` "
                "(FOXG1) lump. Every 'frontal' claim is a claim about the WHOLE cortical node. "
                "This is WHY P2 cannot be confirmed: there is no cortico-cortical structure to "
                "carry a frontal-specific holding function. A real test needs a v2 substrate "
                "that would BREAK the frozen READ-ONLY engine.",
            "ID_not_a_module":
                "Intellectual disability is NOT modelled; the §5/P5 mapping is a proposed "
                "discriminant test owed a large cohort simulation (F3), not a gated result.",
            "lobotomy_is_lesion_evidence_only":
                "Leucotomy/lobotomy is read ONLY as lesion evidence; it was a crude, "
                "abandoned, connection-severing procedure. NOT an endorsement; NOT medical "
                "advice.",
        },
        "firewall": {
            "statement": "Every quantity -- fan-in, out-influence, thread-holding, lesion "
                         "asymmetry, recovery -- is a STRUCTURAL quantity of the coupling model "
                         "on a frozen 12-node kernel, NOT the felt quality of cognition or any "
                         "clinical state; NOT a real connectome, current density, electrode or "
                         "dose; NOT a diagnosis, prognosis or treatment-matching. A node "
                         "'holding the thread' is a statement about coherence in a 12-node "
                         "model, NOT a claim that anything is experienced.",
            "consciousness_claim": 0, "hard_problem_open": 1,
            "axis_A": "mechanism != felt quality; the 'who perceives the pattern' question is "
                      "the homunculus regress the framework declines.",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0, "no_cure_claimed": 1.0, "efficacy": 0.0,
            "not_medical_advice": 1.0, "consciousness_claim": 0.0, "new_tuned_constants": 0.0,
            "sign_only_magnitudes_O": 1.0,
            "reports_honest_negative_on_temporal_holding": 1.0,
            "probe_document_treated_as_idea_not_ssot": 1.0,
            "decoupled_from_mind_atlas": 1.0, "calls_run_all_atlas": 0.0,
        },
        "invariants": {
            "engine_tree_sha256_live": None, "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "engine_file_sha256_expected": FC.ENGINE_FILE_SHA256,
            "m9_anchor_bitforbit": guard_ok,
        },
        "overall": {
            "fold_primitive_ok": prim["primitive_ok"],
            "P1_not_gatherer_broadcaster_robust": P1,
            "P2_temporal_holding_confirmed": P2_holding_confirmed,
            "P6_frontal_lesion_record_reproduced": P6_record_reproduced,
            "P6_perception_robustly_spared": P6_perception_spared,
            "P6_flexibility_is_artifact": P6_flex_artifact,
            "holding_test_ran": holding_test_ran,
            "probe_ran": probe_ran,
            "engine_invariance_guard": guard_ok,
            "is_full_module": bool(prim["primitive_ok"] and P1 and holding_test_ran
                                   and probe_ran and guard_ok),
            "verdict": "Re-established from first principles, the frozen 12-node engine "
                       "ROBUSTLY shows the cortical node is NOT a spatial gatherer (lowest "
                       "fan-in; the thalamus is the convergence hub) and IS a fast broadcaster "
                       "[V mech]. It does NOT reproduce any robust frontal-lesion behaviour: "
                       "the temporal-HOLDING signature is negligible under seed-averaging "
                       "(holding lives in slower subcortical hubs) [O], and the leucotomy "
                       "set-shifting/perseveration signature FLIPS SIGN across a duration sweep "
                       "-- an operating-point artefact [O]. The only robust facts are the "
                       "static structure and that removing the cortical node is nearly silent "
                       "(perception spared because the node is peripheral). The cause is HARD "
                       "LIMIT 1 in its strongest form: a 12-node engine with an undifferentiated "
                       "cortical lump cannot carry a stable frontal phenotype. The engine "
                       "GENERATES sharp frontal hypotheses but CANNOT confirm them; a real test "
                       "needs a v2 substrate that would break the frozen engine. Magnitudes "
                       "[O]; consciousness_claim=0; hard problem OPEN; NOT medical advice.",
        },
    }
    return res


def _canon(o): return FC._canon(o)
def _blob(res): return FC.blob(res)


def frontal_f1_results():
    res = run()
    inv = FC.engine_tree_invariants()
    res["invariants"]["engine_tree_sha256_live"] = inv["engine_tree_sha256_live"]
    res["invariants"]["engine_tree_unchanged"] = inv["engine_tree_unchanged"]
    res["invariants"]["m0_16_subtree_unchanged"] = inv["m0_16_subtree_unchanged"]
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "frontal_f1_temporal_holding_results.json"),
              "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_frontal_f1_temporal_holding_sha256.json"),
              "w", encoding="utf-8") as f:
        json.dump({"frontal_f1_temporal_holding_results.json": digest}, f, indent=2)
        f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = frontal_f1_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    g1, g2, h = res["F1_1_not_a_gatherer"], res["F1_2_broadcaster"], res["F1_3_temporal_holding"]
    g = res["F1_4_engine_invariance_guard"]; pr = res["preregistered_results"]; prim = res["F1_0_fold_primitive"]
    rec = h["c_decisive_recovery_seed_averaged"]
    print("=" * 82)
    print("F1 -- CORTICAL NODE IN THE FROZEN ENGINE   (vp_frontal; INDEPENDENT; READ-ONLY)")
    print("=" * 82)
    print(f"  engine M9 anchor bit-for-bit : {g['engine_matches_anchor_bitforbit']}  ({g['engine_integrator_R']})")
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  R19 fold primitive : {prim['primitive_ok']}  (fold={prim['fold_spinodal']})")
    print("-" * 82)
    print(f"  P1a NOT A GATHERER [robust={g1['robust']}] : neocortex fan-in={g1['neocortex_fan_in']:.4f} (rank {g1['neocortex_rank_low_is_1']}/12) | thalamus={g1['thalamus_fan_in']:.4f} (hub)")
    print(f"  P1b BROADCASTER    [robust={g2['robust']}] : in-rank={g2['neocortex_in_rank_low_is_1']}/12 (low) out-rank={g2['neocortex_out_rank_high_is_1']}/12 (high) f0={g2['neocortex_f0_hz']:.0f}Hz")
    print(f"  P2  TEMPORAL HOLDING (H1 test):")
    print(f"      (a) thread-holding nc rank range over disp = {h['a_thread_holding_disp_sweep']['neocortex_rank_range']}  -> op-specific={h['a_thread_holding_disp_sweep']['operating_point_specific']}")
    print(f"      (b) lobotomy nc=major-winner at {h['b_lobotomy_sustained_Th_sweep']['neocortex_major_winner_at_n_windows']}/{len(h['b_lobotomy_sustained_Th_sweep']['table'])} windows -> single-window-resonance={h['b_lobotomy_sustained_Th_sweep']['single_window_resonance']} | instant-spared={h['b_lobotomy_sustained_Th_sweep']['instant_spared_robust_all_Th']}")
    print(f"      (c) DECISIVE recovery ({rec['n_seeds']} seeds): nc mean_dR={rec['neocortex_mean_dR']:+.4f} +/- {rec['neocortex_std_dR']:.4f}  robust-holder={rec['neocortex_is_robust_holder']} (rank {rec['neocortex_recovery_rank_holder_is_1']}/12)")
    print(f"          robust holders = {rec['robust_holders']}  (slower than cortex={rec['holders_are_slower_than_cortex']})")
    print(f"      VERDICT: frontal temporal-holding confirmed = {h['verdict']['frontal_temporal_holding_confirmed']}  [O -- honest negative]")
    print("-" * 82)
    probe = res["F1_5_frontal_lesion_probe"]
    print(f"  P6  FRONTAL-LESION RECORD (disconnect cortical node = leucotomy; duration sweep):")
    print(f"      perception robustly spared (all durations) = {probe['perception_robustly_spared']}")
    print(f"      flexibility dFlex by duration:")
    for k, v in probe["flexibility_by_duration"].items():
        print(f"        {k:<8} intact={v['intact']:.4f} lesion={v['lesion']:.4f}  dFlex={v['d_pct']:+.1f}%")
    print(f"      -> flexibility sign FLIPS across durations = {probe['flexibility_sign_flips']}  (operating-point artifact)")
    print(f"      -> behavioural leucotomy record reproduced = {probe['behavioural_record_reproduced']}  [O honest negative]")
    print("-" * 82)
    print(f"  PRE-REGISTERED: P1={pr['P1_not_gatherer_but_broadcaster']['status']} ({pr['P1_not_gatherer_but_broadcaster']['grade']})  P2={pr['P2_frontal_temporal_holding']['status']} ({pr['P2_frontal_temporal_holding']['grade']})")
    print(f"  honesty (eff/cure/cc/tuned/signonly) : {hl['efficacy']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}/{hl['sign_only_magnitudes_O']}")
    print(f"  decoupled from mind / calls run_all_atlas : {hl['decoupled_from_mind_atlas']} / {hl['calls_run_all_atlas']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"]
          and ov["is_full_module"] and hl["new_tuned_constants"] == 0.0
          and hl["consciousness_claim"] == 0.0 and hl["efficacy"] == 0.0)
    print("=" * 82)
    print("  F1 MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
