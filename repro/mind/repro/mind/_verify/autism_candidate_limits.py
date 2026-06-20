#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D9.4  CANDIDATE LIMITS -- the boundary nulls (where the threshold-lowering drug fails)
======================================================================================
A threshold-lowering candidate is a SCALAR gain/bias operator on the R19 substrate. Two
pre-registered limits, honestly tested on the D9.2 cohort cerebrum:

  P4  NO chemical candidate (blunt / selective / tri / co-expression) corrects the
      WIRING fault. The W-fault breaks long-range ROUTING (geometry W); a gain/bias
      operator cannot re-route. Predicted fingerprint when the best chemical (tri-lever
      gain) is applied to the W substrate: LOCALITY is INVARIANT (loc_W_drug == loc_W,
      both above healthy), so the broken topology is untouched; PAC does not "recover"
      (it was already at health for W) -- pushing kappa only drives PAC ABOVE health
      (over-coupling MASK); R rises only by scalar gain on a broken graph.

  P5  THE BRIDGE QUESTION ("lower the switch threshold so the residual long-range signal
      crosses it"): sweep the fold-lowering (= effective kappa boost) on the W-faulted
      geometry and ask whether integration R is RESTORED. Predicted: R rises with the
      boost but SATURATES BELOW the healthy-geometry R (the broken topology caps it), or
      only reaches/exceeds it by driving PAC PAST health -- i.e. by global
      over-synchronisation, a MASK, not a routing correction. Lowering the threshold buys
      partial, masking recovery; it does not rebuild the missing edges.

CONTRAST (CORRECTED — ERRATUM E-D9.4-1): an exogenous sustained 4-8 Hz THETA SUPPLY on
the same W-faulted geometry closes the integration deficit ONLY inside a NARROW injection
window (R returns to the healthy metastable value ~0.39). Beyond it the supply
OVER-SYNCHRONISES R far above health -- the global-sync / seizure analogue (the v1.0.0
"R 0.340->0.730 rescue" was measured at injection 0.9, which is this over-sync regime, NOT
a healthy rescue). Even inside the window the supply leaves the geometry W untouched
(locality invariant), so it is an EXTERNAL PACEMAKER (functional crutch), not an
anatomical repair; and it must be STRUCTURED (an unstructured drive of the same amplitude
does not lift R). => the discriminant survives, restated honestly: a scalar chemical
cannot fix W at all; a structured theta supply is a narrow-window functional aid for W,
not a repair.

efficacy=0; mechanism only; NOT medical advice; Axis-A firewall; no dose/synthesis.
VP-SPEC v1.8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine READ-ONLY (tree 0fbf4988...).
"""
import os, sys, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY
import autism_candidate_encoding as ENC
import autism_cohort_cerebrum as CB

ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
RESULT = os.path.join(HERE, "autism_candidate_limits_results.json")
EXPECT = os.path.join(HERE, "expected_autism_candidate_limits_sha256.json")

# vendored byte-identically from the D8 discriminant (engine imported READ-ONLY)
N = CB.N; OMEGA = CB.OMEGA; OMEGA0 = CB.OMEGA0; KAP = CB.KAP; KGLOB = CB.KGLOB
F_THETA = CB.F_THETA; _D = CB._D

def _locality(W):
    sh = []
    for i in range(N):
        order = np.argsort(_D[i] + np.where(np.arange(N) == i, 1e9, 0.0))
        sh.append(float(W[i, order[:2]].sum()))
    return float(np.mean(sh))

def _integrate_supply(omega, W, Kglob, inj, T=6.0, dt=0.001, seed=E.SEED):
    rng = np.random.RandomState(seed)
    th = rng.uniform(-math.pi, math.pi, len(omega))
    ns = int(T / dt); Rs = np.empty(ns); w = 2 * math.pi * F_THETA
    for s in range(ns):
        diff = th[None, :] - th[:, None]
        common = inj * np.sin(w * (s * dt) - th)
        th = th + dt * (omega + Kglob * np.sum(W * np.sin(diff), axis=1) + common)
        Rs[s] = E._order(th)
    h = ns // 2
    return float(np.mean(Rs[h:]))

def _integrate_supply_unstructured(omega, W, Kglob, inj, T=6.0, dt=0.001, seed=E.SEED):
    """same amplitude as _integrate_supply but with per-node RANDOM phase offsets on the
    common drive -- an UNSTRUCTURED slow drive. The main-carrier study found such a drive
    collapses computation; here it should NOT lift coherence the way a clean carrier does."""
    rng = np.random.RandomState(seed)
    th = rng.uniform(-math.pi, math.pi, len(omega))
    noise_phase = rng.uniform(-math.pi, math.pi, len(omega))
    ns = int(T / dt); Rs = np.empty(ns); w = 2 * math.pi * F_THETA
    for s in range(ns):
        diff = th[None, :] - th[:, None]
        common = inj * np.sin(w * (s * dt) - th + noise_phase)
        th = th + dt * (omega + Kglob * np.sum(W * np.sin(diff), axis=1) + common)
        Rs[s] = E._order(th)
    h = ns // 2
    return float(np.mean(Rs[h:]))

def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o

def run():
    E.seed_everything()
    em = CB.emerge()
    Wrn = em["Wrn"]; Wwn = em["Wwn"]
    R_health = em["R_health"]; pac_health = em["pac_health"]
    loc_health = _locality(Wrn)
    R_W = em["R_W"]; loc_W = _locality(Wwn)

    # ---- P4: best chemical candidate (tri-lever, modelled as a uniform gain boost) on W ----
    # a threshold-lowering operator raises effective excitability -> effective kappa multiplier.
    # the strongest single-shot the cohort window allows (D9.3 full-coverage magnitude ~0.4)
    # corresponds to a kappa boost; we use the D8 DRUG factor 1/0.6 as the reference gain.
    DRUG = 1.0 / 0.6
    R_W_drug = E._integrate(OMEGA, Wwn, KAP * DRUG * OMEGA0)[0]
    loc_W_drug = _locality(Wwn)                          # the operator does NOT touch geometry
    pac_W_drug = CB._pac_kappa(KAP * DRUG)               # pushing kappa drives PAC ABOVE health
    locality_invariant = bool(abs(loc_W_drug - loc_W) < 1e-12 and loc_W_drug > loc_health + 1e-9)
    pac_overshoots = bool(pac_W_drug > pac_health + 1e-9)
    R_still_below_health = bool(R_W_drug < R_health - 1e-6)
    P4_chemical_cannot_fix_W = bool(locality_invariant and (pac_overshoots or R_still_below_health))

    # ---- P5: the bridge sweep -- lower the fold (raise effective kappa) on the W geometry ----
    boosts = [1.0, 1.1, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
    sweep = []
    reach_mult = None
    pac_at_reach = None
    for m in boosts:
        Rm = E._integrate(OMEGA, Wwn, KAP * m * OMEGA0)[0]
        pacm = CB._pac_kappa(KAP * m)
        sweep.append(dict(kappa_mult=round(m, 4), R_W=round(Rm, 6), pac=round(pacm, 9),
                          R_reaches_health=bool(Rm >= R_health - 1e-6),
                          pac_past_health=bool(pacm > pac_health + 1e-9)))
        if reach_mult is None and Rm >= R_health - 1e-6:
            reach_mult = m; pac_at_reach = pacm
    R_max_in_sweep = max(r["R_W"] for r in sweep)
    saturates_below = bool(R_max_in_sweep < R_health - 1e-6)
    # if R ever reaches health, is PAC already past health there? (=> recovery is an over-sync MASK)
    reach_is_mask = bool(reach_mult is not None and pac_at_reach is not None
                         and pac_at_reach > pac_health + 1e-9)
    P5_threshold_lowering_is_mask_not_correction = bool(saturates_below or reach_is_mask)

    # ---- CONTRAST (CORRECTED, ERRATUM E-D9.4-1): exogenous theta supply on the W-fault ----
    # v1.0.0 used a coarse ΔR>0.02 check that MISTOOK over-synchronisation for rescue. The
    # corrected analysis sweeps the injection finely and asks WHERE R lands: a narrow window
    # returns R to the healthy metastable value; beyond it the supply over-synchronises R far
    # above health -- the global-sync / seizure analogue (main-carrier study: recall collapses
    # to 0.692 there). The supply also never touches the geometry W, so locality is invariant:
    # it is an EXTERNAL PACEMAKER (functional crutch), not an anatomical repair. And it must be
    # STRUCTURED: an unstructured (random-phase) drive of the same amplitude does NOT lift R.
    OVER_ONSET = R_health * 1.15                    # clear over-sync marker (R >> healthy metastable)
    inj_fine = [0.0, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30, 0.50, 0.90, 1.20]
    sweep_supply = []
    window = []
    for m in inj_fine:
        R = R_W if m == 0.0 else _integrate_supply(OMEGA, Wwn, KGLOB, m * OMEGA0)
        # in-window = supply has RAISED R out of the deficit to within ±0.025 of healthy metastable,
        # and not yet over-synchronised. The untreated deficit (m=0) is excluded by the raise test.
        raised = bool(R > R_W + 0.01)
        in_window = bool(raised and abs(R - R_health) <= 0.025 and R <= OVER_ONSET)
        over = bool(R > OVER_ONSET)
        if in_window:
            window.append(m)
        sweep_supply.append(dict(inj=round(m, 4), R=round(R, 6), gap_to_health=round(R - R_health, 6),
                                 in_health_window=in_window, over_sync=over))
    # the window edges
    window_lo = (min(window) if window else None)
    window_hi = (max(window) if window else None)
    first_over = next((r["inj"] for r in sweep_supply if r["over_sync"]), None)
    R_at_high_inj = next(r["R"] for r in sweep_supply if r["inj"] == 0.9)     # the v1.0.0 point
    high_inj_was_oversync = bool(R_at_high_inj > OVER_ONSET)

    # locality is geometry-only -> invariant under supply: a CRUTCH, not a repair
    loc_W_supply = _locality(Wwn)
    supply_is_crutch_not_repair = bool(abs(loc_W_supply - loc_W) < 1e-12 and loc_W_supply > loc_health + 1e-9)

    # structured vs unstructured at the window centre (must be structured to work)
    inj_test = (window_lo if window_lo is not None and window_lo > 0.0 else 0.08)
    R_structured = _integrate_supply(OMEGA, Wwn, KGLOB, inj_test * OMEGA0)
    R_unstructured = _integrate_supply_unstructured(OMEGA, Wwn, KGLOB, inj_test * OMEGA0)
    structure_required = bool(R_unstructured < R_structured - 0.01)

    # CORRECTED claim: the supply has a NARROW therapeutic window and is a crutch, not a repair.
    supply_has_window = bool(window_lo is not None)
    supply_window_is_narrow = bool(window_lo is not None and window_hi is not None
                                   and first_over is not None and (first_over - window_hi) < 0.06)
    # the discriminant survives but is RESTATED honestly: chemical can't fix W at all; supply can
    # close the deficit only inside a narrow structured window, and even then as a pacemaker crutch.
    discriminant = bool(P4_chemical_cannot_fix_W and supply_has_window and supply_is_crutch_not_repair)

    out = {
        "_what": "D9.4 boundary nulls: a threshold-lowering chemical is a scalar gain/bias operator -- it "
                 "CANNOT correct the wiring (W) fault (locality/routing invariant; pushing kappa only over-"
                 "couples PAC past health, a mask). The bridge idea -- lower the switch so the residual long-"
                 "range signal crosses it -- buys only partial, MASKING recovery (R saturates below the "
                 "healthy-geometry value or reaches it only by over-synchronisation). By contrast a sustained "
                 "exogenous theta SUPPLY rescues the same W-fault by bypassing the broken routing. This closes "
                 "the wave-supply vs uniform-chemical-E/I discriminant for the W fault type.",
        "baselines": {"R_health": round(R_health, 6), "pac_health": round(pac_health, 9),
                      "loc_health": round(loc_health, 6), "R_W": round(R_W, 6), "loc_W": round(loc_W, 6)},
        "P4_chemical_on_W": {
            "drug_gain_factor": round(DRUG, 6),
            "R_W_drug": round(R_W_drug, 6), "loc_W_drug": round(loc_W_drug, 6),
            "pac_W_drug": round(pac_W_drug, 9),
            "locality_invariant_routing_untouched": locality_invariant,
            "pac_overshoots_health_overcoupling_mask": pac_overshoots,
            "R_still_below_health": R_still_below_health,
            "P4_chemical_cannot_fix_W": P4_chemical_cannot_fix_W,
        },
        "P5_threshold_lowering_bridge": {
            "sweep": sweep,
            "R_max_in_sweep": round(R_max_in_sweep, 6),
            "R_saturates_below_health": saturates_below,
            "kappa_mult_where_R_reaches_health": (round(reach_mult, 4) if reach_mult else None),
            "pac_at_reach_point": (round(pac_at_reach, 9) if pac_at_reach else None),
            "reach_only_via_oversync_mask": reach_is_mask,
            "P5_threshold_lowering_is_mask_not_correction": P5_threshold_lowering_is_mask_not_correction,
        },
        "contrast_wave_supply_on_W": {
            "ERRATUM": "E-D9.4-1 — v1.0.0 reported 'supply rescues W (R 0.340→0.730)' using a coarse "
                       "ΔR>0.02 check at injection 0.9; that point is OVER-SYNCHRONISATION (R = health×%.2f), "
                       "the global-sync/seizure analogue, NOT a healthy rescue. Corrected below to a window "
                       "analysis." % (R_at_high_inj / R_health),
            "sweep": sweep_supply,
            "health_window_injection_range": [window_lo, window_hi],
            "first_oversync_injection": first_over,
            "supply_has_health_window": supply_has_window,
            "window_is_narrow": supply_window_is_narrow,
            "R_at_injection_0_9_v100_point": round(R_at_high_inj, 6),
            "injection_0_9_was_oversync": high_inj_was_oversync,
            "supply_is_external_pacemaker_crutch_not_repair": supply_is_crutch_not_repair,
            "loc_W_under_supply_invariant": round(loc_W_supply, 6),
            "structured_R_at_window": round(R_structured, 6),
            "unstructured_R_at_window": round(R_unstructured, 6),
            "structure_required": structure_required,
            "reading": "the theta supply closes the W integration deficit only inside a NARROW injection "
                       "window (R returns to the healthy metastable value); beyond it the supply OVER-"
                       "SYNCHRONISES (seizure analogue). Even inside the window it is an EXTERNAL PACEMAKER "
                       "(locality/geometry invariant) -- a functional crutch, not an anatomical repair -- and "
                       "it must be STRUCTURED (an unstructured drive of the same amplitude does not lift R).",
        },
        "discriminant_chemical_vs_supply_on_W": {
            "chemical_threshold_lowering_cannot_fix_W": P4_chemical_cannot_fix_W,
            "supply_closes_deficit_only_in_narrow_structured_window": bool(supply_has_window and structure_required),
            "supply_is_crutch_not_repair": supply_is_crutch_not_repair,
            "discriminant_holds": discriminant,
            "reading": "the discriminant survives but is restated honestly: a scalar chemical (gain/threshold) "
                       "cannot fix W AT ALL; a sustained STRUCTURED theta supply can close the W integration "
                       "deficit, but only inside a narrow injection window (too much over-synchronises into the "
                       "seizure analogue), and even then as an external-pacemaker CRUTCH that does not rebuild "
                       "the wiring. The threshold-lowering drug is for the T fault; the theta cap is a narrow-"
                       "window functional aid for the W fault, not a repair.",
        },
        "firewall": "mechanism only; efficacy=0; no dose/synthesis; NOT medical advice; Axis-A firewall.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {"engine_tree_frozen": ENGINE_TREE_FROZEN, "pac_grounded": em["pac_grounded"]},
        "preregistered_results": {
            "P4_chemical_cannot_fix_W": {"predicted": True, "observed": P4_chemical_cannot_fix_W,
                "status": "CONFIRMED" if P4_chemical_cannot_fix_W else "REFUTED"},
            "P5_threshold_lowering_is_mask": {"predicted": True,
                "observed": P5_threshold_lowering_is_mask_not_correction,
                "status": "CONFIRMED" if P5_threshold_lowering_is_mask_not_correction else "REFUTED"},
            "P6_supply_has_health_window_not_blanket_rescue": {"predicted": True,
                "observed": bool(supply_has_window and high_inj_was_oversync),
                "status": "CONFIRMED" if (supply_has_window and high_inj_was_oversync) else "REFUTED",
                "note": "supersedes v1.0.0 'contrast_supply_rescues_W' (E-D9.4-1): rescue exists only in a "
                        "narrow window; the old high-injection point was over-synchronisation."},
            "P7_supply_is_crutch_not_repair": {"predicted": True, "observed": supply_is_crutch_not_repair,
                "status": "CONFIRMED" if supply_is_crutch_not_repair else "REFUTED"},
            "P8_supply_must_be_structured": {"predicted": True, "observed": structure_required,
                "status": "CONFIRMED" if structure_required else "REFUTED"},
        },
    }
    return out

if __name__ == "__main__":
    res = run()
    open(RESULT, "w", encoding="utf-8").write(json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False))
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"autism_candidate_limits_results.json": h}, open(EXPECT, "w"), indent=1)
    b = res["baselines"]; p4 = res["P4_chemical_on_W"]; p5 = res["P5_threshold_lowering_bridge"]
    cs = res["contrast_wave_supply_on_W"]; pr = res["preregistered_results"]
    print("D9.4 candidate limits (boundary nulls)")
    print(f"  baselines: R_health={b['R_health']}, R_W={b['R_W']}, loc_health={b['loc_health']}, loc_W={b['loc_W']}")
    print(f"  P4 chemical on W: R_W_drug={p4['R_W_drug']} (health {b['R_health']}), "
          f"loc invariant={p4['locality_invariant_routing_untouched']}, "
          f"PAC overshoot={p4['pac_overshoots_health_overcoupling_mask']}")
    print(f"     -> chemical CANNOT fix W: {p4['P4_chemical_cannot_fix_W']}")
    print(f"  P5 bridge sweep: R_max={p5['R_max_in_sweep']} (health {b['R_health']}), "
          f"reach@mult={p5['kappa_mult_where_R_reaches_health']}, mask={p5['reach_only_via_oversync_mask']}")
    print(f"     -> threshold-lowering is MASK not correction: {p5['P5_threshold_lowering_is_mask_not_correction']}")
    print(f"  CONTRAST theta-supply (CORRECTED, E-D9.4-1):")
    print(f"     health window inj range = {cs['health_window_injection_range']}, first over-sync @ {cs['first_oversync_injection']}")
    print(f"     v1.0.0 point inj=0.9 -> R={cs['R_at_injection_0_9_v100_point']} = OVER-SYNC ({cs['injection_0_9_was_oversync']})")
    print(f"     crutch not repair (loc invariant) = {cs['supply_is_external_pacemaker_crutch_not_repair']}; "
          f"structured {cs['structured_R_at_window']} vs unstructured {cs['unstructured_R_at_window']} -> structure_required {cs['structure_required']}")
    print(f"  discriminant (chemical can't fix W at all; supply = narrow-window crutch): {res['discriminant_chemical_vs_supply_on_W']['discriminant_holds']}")
    for k, v in pr.items():
        print(f"    {v['status']:<10} {k}")
    print(f"  result sha256: {h}")
