#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
D9.2  COHORT CEREBRUM EMERGENCE -- instantiate the moderate-or-below cohort on the
substrate the candidates are simulated on (the engine's MEASURED ephaptic cerebrum)
====================================================================================
"Emerge the cerebrum, then simulate your candidates on it." This module emerges the
engine's measured cerebrum (brain atlas geometry + the M9.6 ephaptic coupling that
drives PAC and global integration R), then instantiates EACH of the 17 cohort genes
(D9.0) as a cell of its real promoter-gamma stiffness, carrying the fault its axis
implies. This is the baseline (UNTREATED) cohort state D9.3 acts on.

THE SUBSTRATE (vendored byte-identically from the D8 mechanism discriminant; the
engine is imported READ-ONLY and these are exact replicas of its M9.6 closure):
  * geometry W : 1/r^3 over the measured MNI organ positions, row-normalised.
  * KAP = 0.5496 (measured dVm/threshold) ; KGLOB = KAP*OMEGA0.
  * PAC depth = _pac_kappa(kappa) : cross-frequency theta->gamma coupling, depends
    ONLY on scalar kappa (geometry does NOT enter) -- grounded to the engine's emitted
    M9.6 value 0.00726119688482934 to 1e-9.
  * R = E._integrate(OMEGA, W, kappa*OMEGA0)[0] : global integration, depends on BOTH
    kappa AND geometry W.

THE THREE FAULT AXES, applied per cohort gene by its D9.0 axis (exact D8 forms):
  T (threshold/excitability): tonic inhibitory bias B_T=-0.25 -> RAISED R19 fold (the
      cell fires reluctantly) and kappa lowered via the denominator k_T=KAP/(1+|B_T|).
  O (output-weak/gain): kappa NUMERATOR down, k_O=M_O*KAP (M_O=0.4); fold normal.
  W (wiring): long-range (>median-distance) edges attenuated (LAM=0.3) and near edges
      boosted 1.3x -- routing broken; kappa (hence PAC) EXACTLY unchanged.

Each cell also carries its fold (engine R19 cusp at its OWN gamma) and its margin to
the spontaneous-ignition (seizure) edge -- the quantities the candidate moves in D9.3.

efficacy=0; this module emerges a MODELLING substrate; no treatment/dose/efficacy
claim; NOT medical advice; Axis-A firewall. VP-SPEC v1.8 (C0-C4, SEED=19). ADD-ONLY;
vp_mind_engine READ-ONLY (tree 0fbf4988...). 2x sha256 deterministic.
"""
import os, sys, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY

ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
COHORT_RESULT = os.path.join(HERE, "autism_cohort_moderate_results.json")
RESULT = os.path.join(HERE, "autism_cohort_cerebrum_results.json")
EXPECT = os.path.join(HERE, "expected_autism_cohort_cerebrum_sha256.json")

# ============================ substrate (vendored from D8 discriminant, exact) =========
A      = E.load_brain_atlas()
REGS   = list(A["organs"].keys())
N      = len(REGS)
F0     = np.array([A["organs"][r]["f0_hz"] for r in REGS])
OMEGA  = 2 * math.pi * F0
OMEGA0 = float(np.mean(OMEGA))
POS    = E._measured_geometry(REGS)
KAP    = E.KAPPA_EPHAPTIC                 # 0.5496 measured
KGLOB  = KAP * OMEGA0
F_THETA = float(A["organs"]["hippocampus"]["f0_hz"])
F_GAMMA = float(A["organs"]["neocortex"]["f0_hz"])
G       = 1.0
_W_FAST = 2 * math.pi * F_GAMMA
_ENGINE_PAC_AT_KAPPA = 0.00726119688482934

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

def ig_thr(g, b, cap=2.0, ngrid=801):
    for s in np.linspace(0.0, cap, ngrid):
        if E.settle(g, b + float(s), s0=-math.sqrt(g)) > 0.0:
            return float(s)
    return float("inf")

def spontaneous(g, b):
    return bool(E.settle(g, b, s0=-math.sqrt(g)) > 0.0)

def seizure_bias(g, lo=0.0, hi=1.5, ngrid=601):
    """smallest net-excitatory bias at which the cell self-ignites (the seizure edge)."""
    for b in np.linspace(lo, hi, ngrid):
        if spontaneous(g, float(b)):
            return float(b)
    return float("inf")

# fault parameters (exact D8 forms)
B_T = -0.25
k_T = KAP / (1.0 + abs(B_T))
M_O = 0.4
k_O = M_O * KAP
LAM = 0.3

def cohort():
    return json.load(open(COHORT_RESULT, encoding="utf-8"))["genes"]

def emerge():
    """emerge substrate baselines + instantiate each cohort gene as a faulted cell."""
    Wraw = _rawW(); Wrn = _rn(Wraw)
    R_health   = E._integrate(OMEGA, Wrn, KGLOB)[0]
    pac_health = _pac_kappa(KAP)
    pac_grounded = bool(abs(pac_health - _ENGINE_PAC_AT_KAPPA) < 1e-9)

    # global W-fault state (driven by the W-axis cohort genes acting on routing)
    Ww = Wraw.copy(); Ww[_FAR] *= LAM; Ww[(~_FAR) & (_D > 0)] *= 1.3
    Wwn = _rn(Ww)
    R_W = E._integrate(OMEGA, Wwn, KGLOB)[0]

    # gain-fault global states (O and T lower kappa -> lower PAC and R)
    R_O = E._integrate(OMEGA, Wrn, k_O * OMEGA0)[0]; pac_O = _pac_kappa(k_O)
    R_T = E._integrate(OMEGA, Wrn, k_T * OMEGA0)[0]; pac_T = _pac_kappa(k_T)

    co = cohort()
    cells = {}
    for sym, rec in co.items():
        g = rec["gamma"]; axis = rec["fault_axis"]
        fold_healthy_cell = round(ig_thr(g, 0.0), 6)        # this cell's OWN healthy fold
        seiz = round(seizure_bias(g), 6)                    # this cell's seizure edge
        if axis == "T":
            b0 = B_T
            cells[sym] = dict(gamma=g, axis=axis, lever=rec["lever"], b_fault=b0,
                              fold_fault=round(ig_thr(g, b0), 6), fold_healthy=fold_healthy_cell,
                              kappa_eff=round(k_T, 6), seizure_bias=seiz,
                              margin_health_to_seizure=round(seiz - 0.0, 6))
        elif axis == "O":
            cells[sym] = dict(gamma=g, axis=axis, lever=None, b_fault=0.0,
                              fold_fault=fold_healthy_cell, fold_healthy=fold_healthy_cell,
                              kappa_eff=round(k_O, 6), seizure_bias=seiz,
                              margin_health_to_seizure=round(seiz - 0.0, 6))
        else:  # W
            cells[sym] = dict(gamma=g, axis=axis, lever=None, b_fault=0.0,
                              fold_fault=fold_healthy_cell, fold_healthy=fold_healthy_cell,
                              kappa_eff=round(KAP, 6), seizure_bias=seiz,
                              margin_health_to_seizure=round(seiz - 0.0, 6))
    return dict(Wrn=Wrn, Wwn=Wwn, R_health=R_health, pac_health=pac_health,
                pac_grounded=pac_grounded, R_W=R_W, R_O=R_O, R_T=R_T,
                pac_O=pac_O, pac_T=pac_T, cells=cells)

def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o

def run():
    E.seed_everything()
    em = emerge()
    cells = em["cells"]
    by_axis = {ax: sorted(s for s in cells if cells[s]["axis"] == ax) for ax in ("T", "O", "W")}

    # the cohort's untreated deficit, summarised
    folds_T = {s: cells[s]["fold_fault"] for s in by_axis["T"]}
    out = {
        "_what": "D9.2 cohort cerebrum: the engine's measured ephaptic cerebrum (PAC grounded to M9.6) "
                 "with each of the 17 moderate-or-below cohort genes instantiated as a cell of its real "
                 "promoter-gamma stiffness, carrying the fault its axis implies (T raised-fold, O gain-down, "
                 "W routing-broken). This is the untreated baseline D9.3 acts on.",
        "substrate": {
            "n_regions": N, "KAPPA_measured": round(KAP, 6), "OMEGA0": round(OMEGA0, 6),
            "R_health": round(em["R_health"], 6), "pac_health": round(em["pac_health"], 9),
            "pac_grounded_to_engine_M9_6": em["pac_grounded"],
            "median_distance_split_for_far_edges": round(_DMED, 6),
        },
        "fault_global_states": {
            "R_health": round(em["R_health"], 6),
            "R_W_wiring": round(em["R_W"], 6), "R_O_output": round(em["R_O"], 6), "R_T_threshold": round(em["R_T"], 6),
            "pac_health": round(em["pac_health"], 9),
            "pac_O_output": round(em["pac_O"], 9), "pac_T_threshold": round(em["pac_T"], 9),
            "pac_W_wiring_equals_health": True,
            "fault_signature": "W: R down, PAC unchanged | O: R+PAC down, fold normal | T: R+PAC down, fold RAISED",
        },
        "cells_by_axis": by_axis,
        "cells": cells,
        "T_fault_folds": folds_T,
        "checks": {
            "pac_grounded": em["pac_grounded"],
            "R_W_below_health": bool(em["R_W"] < em["R_health"]),
            "R_O_below_health": bool(em["R_O"] < em["R_health"]),
            "R_T_below_health": bool(em["R_T"] < em["R_health"]),
            "pac_O_below_health": bool(em["pac_O"] < em["pac_health"]),
            "pac_T_below_health": bool(em["pac_T"] < em["pac_health"]),
            "every_T_cell_fold_raised": all(cells[s]["fold_fault"] > cells[s]["fold_healthy"] + 1e-9 for s in by_axis["T"]),
            "n_cells": len(cells),
        },
        "firewall": "modelling substrate only; efficacy=0; no dose/synthesis; NOT medical advice; Axis-A firewall.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {"engine_tree_frozen": ENGINE_TREE_FROZEN},
    }
    return out

if __name__ == "__main__":
    res = run()
    open(RESULT, "w", encoding="utf-8").write(json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False))
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"autism_cohort_cerebrum_results.json": h}, open(EXPECT, "w"), indent=1)
    s = res["substrate"]; c = res["checks"]
    print("D9.2 cohort cerebrum")
    print(f"  substrate: {s['n_regions']} regions, R_health={s['R_health']}, pac_health={s['pac_health']} "
          f"(grounded to M9.6: {s['pac_grounded_to_engine_M9_6']})")
    g = res["fault_global_states"]
    print(f"  R: health {g['R_health']} | W {g['R_W_wiring']} | O {g['R_O_output']} | T {g['R_T_threshold']}")
    print(f"  PAC: health {g['pac_health']} | O {g['pac_O_output']} | T {g['pac_T_threshold']} | W = health")
    print(f"  cells by axis: T={res['cells_by_axis']['T']}")
    print(f"                 O={res['cells_by_axis']['O']}")
    print(f"                 W={res['cells_by_axis']['W']}")
    print(f"  every T-cell fold raised: {c['every_T_cell_fold_raised']}  ;  n_cells={c['n_cells']}")
    print(f"  result sha256: {h}")
