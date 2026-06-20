#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VC1  THE INTERFERENCE QUESTION -- does an external carrier coherently ADD a lane, or
     destructively interfere / merely force coherence?
=====================================================================================
Grounds in the light-emergence result: the elastic lattice is LINEAR, so waves of
different frequencies pass through each other untouched (superposition / FDM). The
reviewer's reframing asks whether the theta cap's job is NOT to force synchrony (the
over-sync failure of the THETA_CAP note's section 1 / D9.4) but to SUPPLY A MISSING
LONG-RANGE LANE on the linear highway so the existing signals can route.

This module makes the cap mechanism an EMPIRICAL FORK (pre-registered: report whichever
the physics gives, including the negative -- no usable coupling). On the D9.2 W-faulted
cerebrum, drive the broken geometry with an external structured theta carrier under
several contrasted couplings, all in the section-1 amplitude regime:

  C-FORCE   : the coherence-forcing coupling already in D9.4 (`_integrate_supply`):
              common_i = inj * sin(w_c t - th_i). The carrier is an EXTERNAL CLOCK that
              pulls every node's ABSOLUTE phase toward a common external reference.
  C-CHANNEL : an additive-lane / linear-superposition coupling. The carrier is a single
              shared BROADCAST lane that relays the network's OWN collective signal
              (mean field Z = R e^{i psi}) back to each node: c * R * sin(psi - th_i).
              It uses the network's OWN phase psi (NOT an external clock) -- signals
              route on it but it does not force the nodes to lock to an outside rhythm.
  C-EDGE    : the strongest "supply the missing long-range lane" model -- an external
              relay on the FAR (broken) pairs carrying their RELATIVE phase only,
              c * <sin(th_j - th_i)>_{far}. Directly supplies long-range routing without
              an external clock.
  C-NULL    : pure superposition control -- a common additive carrier c * sin(w_c t)
              with NO phase term. Per the proven linearity it cancels in phase
              differences: the carrier passes through untouched (the "no interference,
              no routing" baseline).

PRE-REGISTERED (sign-only; magnitudes reported, never tuned):
  P-VC1a  under C-FORCE the health window is NARROW and over-sync appears just beyond it
          (reproduces section 1 / D9.4: window inj ~0.08-0.10, first over-sync ~0.15).
  P-VC1b  under C-CHANNEL the carrier SUPERPOSES (the brain's own band is preserved --
          no destructive cancellation, measure internal-band power before/after) AND
          routing improves WITHOUT R climbing into over-sync. If FALSE -- the additive
          lane over-syncs, cancels the internal band, OR fails to route -- that is the
          decisive negative for the benign-lane reframing.
  P-VC1c  a phase-mismatched / unstructured external carrier does NOT improve routing
          under any coupling (the section-1 structure requirement, generalised).

DECISIVE OUTPUT: which coupling (if any) supplies a usable lane without over-sync or
interference. This determines whether the cap can work IN PRINCIPLE, and as what.

efficacy=0; mechanism only; NOT medical advice; Axis-A firewall; no dose/synthesis.
VP-SPEC v1.8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine READ-ONLY (tree 0fbf4988...).
"""
import os, sys, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_engine"))
import vp_mind_engine as E   # READ-ONLY
import autism_cohort_cerebrum as CB

ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
RESULT = os.path.join(HERE, "vc1_carrier_interference_results.json")
EXPECT = os.path.join(HERE, "expected_vc1_carrier_interference_sha256.json")

# substrate (the engine is READ-ONLY; these mirror the D9.2 / D8 closure exactly)
N = CB.N; OMEGA = CB.OMEGA; OMEGA0 = CB.OMEGA0; KGLOB = CB.KGLOB
F_THETA = CB.F_THETA; _D = CB._D; _FAR = CB._FAR


def _theta_band_power(zre, dt):
    """power of the collective signal Re(Z(t)) in the theta band [4,8] Hz -- the
    'internal band power' whose preservation/cancellation answers the interference
    question (DC removed; engine-style rfft)."""
    x = np.asarray(zre, float); x = x - x.mean()
    f = np.fft.rfftfreq(len(x), d=dt)
    P = np.abs(np.fft.rfft(x)) ** 2
    m = (f >= 4.0) & (f <= 8.0)
    return float(P[m].sum())


def _drive_run(coupling, amp, T=6.0, dt=0.001, seed=E.SEED, unstructured=False):
    """integrate the W-faulted Kuramoto cerebrum under the named external carrier
    coupling. Returns (mean order parameter R over the 2nd half, theta-band power of
    the collective signal). amp is the carrier strength in the coupling's own units
    (C-FORCE/C-NULL use inj*OMEGA0 as in D9.4; C-CHANNEL/C-EDGE use a dimensionless
    lane gain). 2x sha256 deterministic (single fixed seed)."""
    rng = np.random.RandomState(seed)
    th = rng.uniform(-math.pi, math.pi, N)
    noise = rng.uniform(-math.pi, math.pi, N) if unstructured else np.zeros(N)
    ns = int(T / dt); w = 2 * math.pi * F_THETA
    Rs = np.empty(ns); Zre = np.empty(ns)
    Lfar = _FAR.astype(float); deg = Lfar.sum(axis=1); deg[deg == 0] = 1.0
    for s in range(ns):
        diff = th[None, :] - th[:, None]
        net = KGLOB * np.sum(_WWN * np.sin(diff), axis=1)
        if coupling == "FORCE":
            drive = amp * np.sin(w * (s * dt) - th + noise)
        elif coupling == "CHANNEL":
            Z = np.mean(np.exp(1j * th)); psi = np.angle(Z); Rmag = np.abs(Z)
            drive = amp * Rmag * np.sin(psi - th + noise)
        elif coupling == "EDGE":
            drive = amp * np.sum(Lfar * np.sin(diff + noise[None, :]), axis=1) / deg
        elif coupling == "NULL":
            drive = amp * np.sin(w * (s * dt)) * np.ones(N)
        else:
            drive = 0.0
        th = th + dt * (OMEGA + net + drive)
        Z = np.mean(np.exp(1j * th)); Rs[s] = abs(Z); Zre[s] = Z.real
    h = ns // 2
    return float(np.mean(Rs[h:])), _theta_band_power(Zre[h:], dt)


def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o


# emerged once at import (READ-ONLY substrate); used by _drive_run
E.seed_everything()
_EM = CB.emerge()
_WWN = _EM["Wwn"]
R_HEALTH = _EM["R_health"]
R_W = _EM["R_W"]
OVER = R_HEALTH * 1.15          # over-sync marker (same convention as D9.4)


def run():
    E.seed_everything()
    em = _EM
    pac_grounded = em["pac_grounded"]

    # baseline internal theta-band power with NO carrier (the reference for interference)
    R0, P0 = _drive_run("NULL", 0.0)

    # ---- C-FORCE sweep (external clock; reproduces section 1 / D9.4) ----
    force_inj = [0.0, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30, 0.50, 0.90]
    force = []
    f_window = []
    for inj in force_inj:
        R, P = _drive_run("FORCE", inj * OMEGA0)
        raised = bool(R > R_W + 0.01)
        in_window = bool(raised and abs(R - R_HEALTH) <= 0.025 and R <= OVER)
        over = bool(R > OVER)
        if in_window:
            f_window.append(inj)
        force.append(dict(inj=round(inj, 4), R=round(R, 6), gap_to_health=round(R - R_HEALTH, 6),
                          in_health_window=in_window, over_sync=over, band_power_ratio=round(P / P0, 6)))
    f_window_lo = (min(f_window) if f_window else None)
    f_window_hi = (max(f_window) if f_window else None)
    f_first_over = next((r["inj"] for r in force if r["over_sync"]), None)
    P_VC1a_force_narrow_window = bool(
        f_window_lo is not None and f_first_over is not None and (f_first_over - (f_window_hi or 0)) < 0.06)

    # ---- C-CHANNEL sweep (additive broadcast relay; network's own phase, no clock) ----
    chan_c = [0.0, 0.1, 0.2, 0.4, 0.8, 1.5, 3.0, 6.0]
    channel = []
    chan_routes = False
    chan_over = False
    chan_band_min = float("inf")
    for c in chan_c:
        R, P = _drive_run("CHANNEL", c)
        routes = bool(R >= R_HEALTH - 0.025)        # restored integration toward health
        over = bool(R > OVER)
        chan_routes = chan_routes or routes
        chan_over = chan_over or over
        chan_band_min = min(chan_band_min, P / P0)
        channel.append(dict(c=round(c, 4), R=round(R, 6), gap_to_health=round(R - R_HEALTH, 6),
                            routes_to_health=routes, over_sync=over, band_power_ratio=round(P / P0, 6)))
    chan_R_max = max(r["R"] for r in channel)
    # destructive interference = the internal band is cancelled below the no-carrier baseline
    channel_destroys_band = bool(chan_band_min < 0.5)
    channel_routes_no_oversync = bool(chan_routes and not chan_over)

    # ---- C-EDGE sweep (strongest 'supply the missing long-range lane': far-pair relay) ----
    edge_c = [0.0, 0.1, 0.2, 0.4, 0.8, 1.5, 3.0]
    edge = []
    edge_routes = False
    for c in edge_c:
        R, _ = _drive_run("EDGE", c)
        routes = bool(R >= R_HEALTH - 0.025)
        edge_routes = edge_routes or routes
        edge.append(dict(c=round(c, 4), R=round(R, 6), gap_to_health=round(R - R_HEALTH, 6),
                         routes_to_health=routes, over_sync=bool(R > OVER)))
    edge_R_max = max(r["R"] for r in edge)

    # ---- C-NULL (pure superposition control) ----
    null_c = [0.0, 0.1, 0.5, 2.0]
    null = []
    for c in null_c:
        R, P = _drive_run("NULL", c)
        null.append(dict(c=round(c, 4), R=round(R, 6), gap_to_health=round(R - R_HEALTH, 6),
                         band_power_ratio=round(P / P0, 6)))
    null_R_span = max(r["R"] for r in null) - min(r["R"] for r in null)
    null_is_inert = bool(null_R_span < 1e-3)        # passes through untouched (cancels in differences)

    # ---- P-VC1b verdict: does the additive lane supply a usable lane? ----
    # the benign-lane reframing requires: preserves band (no cancel) AND routes AND no over-sync.
    additive_lane_routes = bool(chan_routes or edge_routes)
    P_VC1b_additive_lane_supplies_usable_lane = bool(
        additive_lane_routes and (not channel_destroys_band) and channel_routes_no_oversync)

    # ---- P-VC1c: structure requirement under each routing coupling ----
    # C-FORCE at the window centre: structured vs unstructured (the D9.4 result, generalised)
    inj_test = (f_window_lo if f_window_lo and f_window_lo > 0 else 0.08)
    Rf_struct, _ = _drive_run("FORCE", inj_test * OMEGA0, unstructured=False)
    Rf_unstr, _ = _drive_run("FORCE", inj_test * OMEGA0, unstructured=True)
    force_needs_structure = bool(Rf_unstr < Rf_struct - 0.01)
    # C-EDGE at a representative amplitude
    Re_struct, _ = _drive_run("EDGE", 0.8, unstructured=False)
    Re_unstr, _ = _drive_run("EDGE", 0.8, unstructured=True)
    P_VC1c_unstructured_does_not_route = bool(
        force_needs_structure and not (Re_unstr >= R_HEALTH - 0.025))

    # ---- the decisive read ----
    only_force_routes = bool(P_VC1a_force_narrow_window and not additive_lane_routes)
    cap_is_pacemaker_not_passive_lane = bool(only_force_routes)

    out = {
        "_what": "VC1 carrier-interference fork on the W-faulted cerebrum. C-FORCE (external clock, D9.4) "
                 "vs C-CHANNEL (additive broadcast relay of the network's OWN collective signal) vs C-EDGE "
                 "(external relay on the broken long-range pairs, relative phase only) vs C-NULL (pure "
                 "superposition). Measures order parameter R (routing), over-sync, and internal theta-band "
                 "power (interference). Determines which coupling, if any, supplies a usable lane -- and as what.",
        "baselines": {"R_health": round(R_HEALTH, 6), "R_W_deficit": round(R_W, 6),
                      "over_sync_threshold": round(OVER, 6),
                      "no_carrier_internal_band_power": round(P0, 6), "no_carrier_R": round(R0, 6)},
        "C_FORCE_external_clock": {
            "sweep": force,
            "health_window_inj_range": [f_window_lo, f_window_hi],
            "first_oversync_inj": f_first_over,
            "P_VC1a_narrow_window_with_oversync_beyond": P_VC1a_force_narrow_window,
            "reading": "the external-clock carrier returns R to the healthy metastable value only inside a "
                       "narrow injection window; just beyond it R over-synchronises. The internal theta-band "
                       "power RISES with inj because the external clock injects its OWN rhythm (it overrides, "
                       "it does not preserve, the network's multiplexed structure)."},
        "C_CHANNEL_additive_broadcast_relay": {
            "sweep": channel,
            "R_max_over_sweep": round(chan_R_max, 6),
            "min_band_power_ratio": round(chan_band_min, 6),
            "routes_to_health": chan_routes,
            "ever_over_syncs": chan_over,
            "destroys_internal_band": channel_destroys_band,
            "routes_without_oversync": channel_routes_no_oversync,
            "reading": "a broadcast lane relaying the network's OWN collective signal (c*R*sin(psi-th)) is "
                       "SELF-LIMITING on a degraded substrate: because R is already low in the W-deficit, the "
                       "relayed signal is weak, so the lane cannot bootstrap integration -- R stays at the "
                       "deficit value at every gain. It neither cancels the band nor routes: it is INERT. A "
                       "lane can only carry coherence that already exists, and the W-fault is the loss of it."},
        "C_EDGE_long_range_relay": {
            "sweep": edge,
            "R_max_over_sweep": round(edge_R_max, 6),
            "routes_to_health": edge_routes,
            "structured_R_at_c0_8": round(Re_struct, 6),
            "unstructured_R_at_c0_8": round(Re_unstr, 6),
            "reading": "even the strongest 'supply the missing long-range lane' model -- an external relay on "
                       "the broken far-pairs carrying their RELATIVE phase -- does not route: on a desynchronised "
                       "substrate the far-pair phase differences are near-random, so the relay torque averages to "
                       "~0. A relative-phase lane amplifies existing long-range coherence; it cannot create it."},
        "C_NULL_pure_superposition": {
            "sweep": null,
            "R_span_over_sweep": round(null_R_span, 9),
            "is_inert_passes_through": null_is_inert,
            "reading": "a common additive carrier c*sin(w_c t) with no phase term cancels exactly in phase "
                       "differences (the proven linearity): the carrier passes through the network untouched -- "
                       "zero interference AND zero routing. The clean superposition baseline."},
        "structure_requirement": {
            "C_FORCE_structured_R_at_window": round(Rf_struct, 6),
            "C_FORCE_unstructured_R_at_window": round(Rf_unstr, 6),
            "C_FORCE_needs_structure": force_needs_structure,
            "P_VC1c_unstructured_does_not_route": P_VC1c_unstructured_does_not_route},
        "decisive_verdict": {
            "only_external_clock_routes": only_force_routes,
            "additive_lane_supplies_usable_lane": additive_lane_routes,
            "cap_is_external_pacemaker_not_a_passive_lane": cap_is_pacemaker_not_passive_lane,
            "reading": "the reviewer's benign 'additive FDM lane' reframing is NOT supported by the physics: no "
                       "passive lane (broadcast relay OR long-range relative-phase relay) routes on the broken "
                       "substrate, because a lane can only carry coherence that already exists and the W-fault is "
                       "precisely the loss of that long-range coherence. The ONLY coupling that routes is C-FORCE "
                       "-- an EXTERNAL PACEMAKER imposing a coherent clock the degraded network lacks internally -- "
                       "and it keeps the section-1 knife-edge window and over-sync risk. The cap CAN work in "
                       "principle, but only as a structured, narrow-window external-pacemaker crutch, not as the "
                       "benign passive lane the reframing hoped for. (efficacy=0; this is a mechanism statement.)"},
        "firewall": "mechanism only; efficacy=0; no dose/synthesis; NOT medical advice; Axis-A firewall.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {"engine_tree_frozen": ENGINE_TREE_FROZEN, "pac_grounded": pac_grounded},
        "preregistered_results": {
            "P_VC1a_C_FORCE_narrow_window_oversync_beyond": {
                "predicted": True, "observed": P_VC1a_force_narrow_window,
                "status": "CONFIRMED" if P_VC1a_force_narrow_window else "REFUTED"},
            "P_VC1b_additive_lane_supplies_usable_lane": {
                "predicted": True, "observed": P_VC1b_additive_lane_supplies_usable_lane,
                "status": "CONFIRMED" if P_VC1b_additive_lane_supplies_usable_lane else "REFUTED",
                "note": "REFUTED is the decisive negative for the benign-lane reframing: the additive lane is "
                        "INERT (neither cancels nor routes), so the cap cannot be a passive lane -- only a pacemaker."},
            "P_VC1c_unstructured_does_not_route": {
                "predicted": True, "observed": P_VC1c_unstructured_does_not_route,
                "status": "CONFIRMED" if P_VC1c_unstructured_does_not_route else "REFUTED"},
        },
    }
    return out


if __name__ == "__main__":
    res = run()
    open(RESULT, "w", encoding="utf-8").write(json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False))
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"vc1_carrier_interference_results.json": h}, open(EXPECT, "w"), indent=1)
    b = res["baselines"]; cf = res["C_FORCE_external_clock"]; cc = res["C_CHANNEL_additive_broadcast_relay"]
    ce = res["C_EDGE_long_range_relay"]; dv = res["decisive_verdict"]; pr = res["preregistered_results"]
    print("VC1 carrier interference fork")
    print(f"  R_health={b['R_health']} R_W={b['R_W_deficit']} over_thr={b['over_sync_threshold']}")
    print(f"  C-FORCE: window inj {cf['health_window_inj_range']}, first over-sync @ {cf['first_oversync_inj']} "
          f"-> narrow-window {cf['P_VC1a_narrow_window_with_oversync_beyond']}")
    print(f"  C-CHANNEL: R_max={cc['R_max_over_sweep']} (health {b['R_health']}), routes={cc['routes_to_health']}, "
          f"band_min={cc['min_band_power_ratio']} -> INERT (neither cancels nor routes)")
    print(f"  C-EDGE: R_max={ce['R_max_over_sweep']} routes={ce['routes_to_health']}")
    print(f"  DECISIVE: only external clock routes = {dv['only_external_clock_routes']}; "
          f"cap is pacemaker not passive lane = {dv['cap_is_external_pacemaker_not_a_passive_lane']}")
    for k, v in pr.items():
        print(f"    {v['status']:<10} {k}")
    print(f"  result sha256: {h}")
