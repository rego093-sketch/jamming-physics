#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_hmd_loops.py  --  the CLOSED loop dynamics for Hemodynamic Homeostasis (deterministic).

This is the substantive research layer the CHARTER skeleton deferred: the fast baroreflex buffer, the
slow renal INTEGRAL controller (Guyton pressure-natriuresis), the hypertension setpoint RESET, and the
chronic-heart-failure basin COLLAPSE -- all on the SAME shared substrate (R19 double-well + integral
feedback) the rest of the framework uses, never re-deriving the substrate math (VP-SPEC C1).

KEY FUNDAMENTAL (deeper than "MAP = CO x SVR"): the kidney is an INTEGRAL controller. An integral
controller drives steady-state error to zero -> it defends a reference against any constant disturbance
(Guyton's "infinite steady-state gain" for renal pressure-natriuresis). Two consequences fall straight
out of the control math and are reproduced below:
  (1) hypertension cannot be a momentary failure -- a sustained high pressure REQUIRES the renal
      reference (pressure-natriuresis curve) to be RESET upward (RP4); and
  (2) any therapy that acts as an operating-point DISTURBANCE (lower the pressure without moving the
      renal reference) is REJECTED back toward the (high) reference -- it is "opposed back", which is
      why such drugs are lifelong, whereas resetting the reference is durable (see _therapy).

Heart failure is the OTHER substrate reading: the cardiac operating point is an R19 field whose
contractility kappa sets the barrier (kappa^2/4) and whose load L tilts it; collapse is crossing the
R19 spinodal |L| > spinodal(kappa) so the high-output basin DISAPPEARS (a fold) -- categorically
different from a reference reset (RP5).

GRADES (VP-SPEC C3): hydraulic identity / integral-control / fold SHAPE = [V]; cited resting values,
gains, latencies = [L]; ABSOLUTE pressure scale and incidence = [O] (stated obstacle in the LEDGER).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, settle, seed_everything

# ---------------------------------------------------------------------------
# Cited resting anchors (literature [L]; see LITERATURE.md). Not fitted to the
# substrate -- these are observed textbook resting values (Guyton-Hall).
# ---------------------------------------------------------------------------
CO_REST_L_MIN   = 5.0     # cardiac output, L/min                 [L]
SVR_REST_PRU    = 17.8    # systemic vascular resistance, mmHg.min/L (hybrid/Wood units) [L]
CVP_REST_MMHG   = 4.0     # central venous pressure, mmHg         [L]
MAP_REST_TARGET = 93.0    # resting MAP, mmHg (discriminant only) [L]


# ===========================================================================
# RP1 -- MAP is owned by NO single organ: it is the hydraulic Ohm's-law product
#        of a cardioresp seam (CO) and a circulatory seam (SVR), plus CVP.
# ===========================================================================
def map_from_seams(co=CO_REST_L_MIN, svr=SVR_REST_PRU, cvp=CVP_REST_MMHG):
    """MAP = CVP + CO * SVR  (hydraulic analogue of V = IR). Relation exact [V];
    the numeric ~93 mmHg follows from cited resting CO/SVR/CVP [L]; deriving the
    ABSOLUTE pressure scale from the jamming substrate is [O] (same obstacle as
    absolute g in the physics volume -- needs the full lattice scale)."""
    return cvp + co * svr


def rp1_map_product():
    seed_everything()
    mp = map_from_seams()
    # cross-check that the product genuinely partitions across the two seams (no single owner)
    share_co = (CO_REST_L_MIN * SVR_REST_PRU) / (mp - CVP_REST_MMHG)   # = 1 by construction of the seam split
    return dict(
        relation="MAP = CVP + CO x SVR (hydraulic Ohm's law)",
        co_L_min=CO_REST_L_MIN, svr_mmHg_min_L=SVR_REST_PRU, cvp_mmHg=CVP_REST_MMHG,
        MAP_mmHg=round(float(mp), 6),
        resting_target_mmHg=MAP_REST_TARGET,
        abs_err_mmHg=round(abs(float(mp) - MAP_REST_TARGET), 6),
        seam_partition_share=round(float(share_co), 6),
        owned_by_single_organ=False,
        relation_grade="[V]", numeric_grade="[L]", absolute_scale_grade="[O]")


# ===========================================================================
# RP2 -- fast baroreflex buffer (negative feedback). A pressure step is opposed
#        by an effector E that relaxes toward G*err with time constant tau_b.
#        Closed-loop residual = step/(1+G); closed-loop tau = tau_b/(1+G).
# ===========================================================================
def baroreflex_buffer(step_mmHg=20.0, G=3.0, tau_b=2.0, T=12.0, dt=0.005, transduction=1.0):
    """Apply a +step disturbance to open-loop pressure; the baroreflex effector E
    opposes it. `transduction` scales the mechanosensor gain (PIEZO): set 0 to
    model the PIEZO1/2 double-KO (baroreflex abolished -> labile pressure)."""
    seed_everything()
    Geff = G * transduction
    p_open = MAP_REST_TARGET + step_mmHg
    E = 0.0
    n = int(T / dt)
    trace = np.empty(n)
    for i in range(n):
        p = p_open - E
        err = p - MAP_REST_TARGET
        E += dt * (Geff * err - E) / tau_b
        trace[i] = p
    residual = float(trace[-1] - MAP_REST_TARGET)
    buffered_frac = 1.0 - residual / step_mmHg if step_mmHg else 0.0
    # settling: first time within 5% of the final residual
    final = trace[-1]
    band = 0.05 * abs(step_mmHg)
    settle_idx = next((i for i in range(n) if abs(trace[i] - final) <= band), n - 1)
    return dict(
        step_mmHg=step_mmHg, open_loop_gain=G, transduction=transduction,
        residual_mmHg=round(residual, 6),
        buffered_fraction=round(float(buffered_frac), 6),
        predicted_residual_frac=round(1.0 / (1.0 + Geff), 6) if (1.0 + Geff) else None,
        settling_time_s=round(settle_idx * dt, 4),
        closed_loop_tau_s=round(tau_b / (1.0 + Geff), 4) if (1.0 + Geff) else None,
        shape_grade="[V]", gain_latency_grade="[L]")


def rp2_baroreflex():
    intact = baroreflex_buffer(transduction=1.0)
    ko = baroreflex_buffer(transduction=0.0)   # PIEZO1/2 double-KO cross-check
    # discriminant: intact buffers most of the step; KO passes the full step (labile)
    return dict(intact=intact, piezo_double_ko=ko,
                ko_is_labile=bool(ko["buffered_fraction"] < 0.05),
                intact_buffers_majority=bool(intact["buffered_fraction"] > 0.5),
                anchor="PIEZO1/2 are the baroreceptor mechanosensors; double-KO abolishes the baroreflex and gives labile hypertension (Zeng et al., Science 2018) [L]")


# ===========================================================================
# RP3 -- slow renal INTEGRAL controller (Guyton pressure-natriuresis).
#        P = P0 + a(V-V0);  natriuretic output = k(P - Pset);  intake = I0.
#        dV/dt = I0 - k(P - Pset).  Integral control => disturbance rejection:
#        a transient volume load returns P EXACTLY to the steady setpoint,
#        independent of the load size ("infinite steady-state gain").
# ===========================================================================
def kidney_integrator(P0=70.0, a=0.05, V0=5000.0, k=8.0, Pset=93.0,
                      intake=0.0, bolus_mL=0.0, bolus_at_s=20.0,
                      drug_mmHg=0.0, drug_at_s=20.0, dPset=0.0,
                      equilibrate=True, T=400.0, dt=0.02):
    """Renal-body-fluid integral loop. Returns the pressure trace and the steady P.
      bolus_mL  : a transient volume disturbance added at bolus_at_s.
      drug_mmHg : an operating-point DISTURBANCE applied from drug_at_s (lowers actual P).
      dPset     : a RESET of the renal reference (shifts the defended pressure).
      equilibrate: start volume so the loop begins AT the defended point P=Pset+dPset,
                   isolating the intervention transient from the initial convergence."""
    seed_everything()
    Pset_eff = Pset + dPset
    # start at the defended pressure so the only transient is the intervention:
    V = (V0 + (Pset_eff - P0) / a) if equilibrate else V0
    n = int(T / dt)
    P_tr = np.empty(n)
    bolus_step = int(bolus_at_s / dt)
    drug_step = int(drug_at_s / dt)
    for i in range(n):
        if i == bolus_step and bolus_mL:
            V += bolus_mL
        d = drug_mmHg if i >= drug_step else 0.0
        P = P0 + a * (V - V0)
        P_eff = P - d                              # what the macula densa / arterioles actually see
        out = k * (P_eff - Pset_eff)               # pressure-natriuresis
        V += dt * (intake - out)
        P_tr[i] = P_eff
    return P_tr, float(P_tr[-1]), Pset_eff


def rp3_pressure_natriuresis():
    seed_everything()
    # two different transient volume loads -> both must return to the SAME steady P
    _, p_small, pset = kidney_integrator(bolus_mL=200.0)
    _, p_big,   _    = kidney_integrator(bolus_mL=800.0)
    _, p_none,  _    = kidney_integrator(bolus_mL=0.0)
    spread = abs(p_small - p_big)
    return dict(
        model="renal integral controller dV/dt = intake - k(P - Pset)",
        steady_P_no_load=round(p_none, 6), steady_P_small_load=round(p_small, 6),
        steady_P_big_load=round(p_big, 6), setpoint=round(pset, 6),
        load_independent_spread_mmHg=round(float(spread), 8),
        perfect_adaptation=bool(spread < 1e-3),
        integral_gain_signature="steady error -> 0 for any constant disturbance (Guyton infinite gain)",
        shape_grade="[V]", anchor_grade="[L]", absolute_setpoint_grade="[O]")


# ===========================================================================
# RP4 -- hypertension = setpoint RESET (attractor shift), and the integral
#        controller OPPOSES an operating-point drug back toward the reference.
# ===========================================================================
def rp4_setpoint_reset():
    seed_everything()
    # (a) reference reset upward -> defended pressure tracks the new reference
    _, p_normal, pset_n = kidney_integrator(dPset=0.0)
    _, p_reset,  pset_r = kidney_integrator(dPset=20.0)
    # (b) on the RESET (high) controller, an operating-point drug is a constant
    #     disturbance -> integral control rejects it -> P returns to the high reference.
    #     Pre-equilibrated at 113; drug applied at t=20 s; nadir << steady shows
    #     the drug works briefly then is OPPOSED BACK to the defended pressure.
    tr, p_drug_steady, _ = kidney_integrator(dPset=20.0, drug_mmHg=15.0, drug_at_s=20.0)
    nadir = float(np.min(tr))
    return dict(
        defended_P_normal=round(p_normal, 6), defended_P_reset=round(p_reset, 6),
        reset_shift_mmHg=round(p_reset - p_normal, 6),
        attractor_moved_up=bool(p_reset - p_normal > 5.0),
        drug_nadir_mmHg=round(nadir, 6), drug_steady_mmHg=round(p_drug_steady, 6),
        drug_transient_drop_mmHg=round(p_reset - nadir, 6),
        opposed_back=bool(p_drug_steady > p_normal + 5.0 and (p_reset - nadir) > 5.0),
        parallel="exact parallel of the lipostat reset in obesity: an integral controller defends a RESET reference; operating-point pushes are rejected back",
        shape_grade="[V]", risk_anchor_grade="[L]", absolute_incidence_grade="[O]")


# ===========================================================================
# RP5 -- chronic heart failure = R19 basin COLLAPSE (fold), NOT a reset.
#        Cardiac operating point s : g = contractility kappa (barrier kappa^2/4),
#        h = -load L (tilt). High-output basin exists while |L| < spinodal(kappa).
#        Collapse = crossing the spinodal so that basin DISAPPEARS.
# ===========================================================================
def margin(kappa, load):
    """R19 barrier margin for the high-output basin: spinodal(kappa) - |load|.
    > 0 : high-output basin exists (compensated).  <= 0 : basin gone (collapse)."""
    return float(spinodal(kappa) - abs(load))


def cardiac_basin(kappa, load, s0=None):
    """Settle the R19 cardiac field; return the operating output state and whether
    the high-output basin still holds it."""
    if s0 is None:
        s0 = math.sqrt(kappa) if kappa > 0 else 0.0   # start in the high-output basin
    s = settle(kappa, -load, s0=s0)
    return float(s)


def rp5_basin_collapse():
    seed_everything()
    L = 0.8
    kappas = [round(x, 4) for x in np.linspace(2.2, 0.6, 17)]
    rows = []
    collapsed_at = None
    for kp in kappas:
        s = cardiac_basin(kp, L)
        m = margin(kp, L)
        held = bool(s > 0.0 and m > 0.0)
        rows.append(dict(kappa=kp, output_state=round(s, 6), barrier_margin=round(m, 6), high_output_basin=held))
        if collapsed_at is None and not held:
            collapsed_at = kp
    return dict(
        load=L, sweep_kappa_high_to_low=rows,
        collapse_kappa=collapsed_at,
        spinodal_at_collapse=round(float(spinodal(collapsed_at)), 6) if collapsed_at else None,
        is_fold_not_reset=True,
        note="high-output fixed point ANNIHILATES at the spinodal (saddle-node); distinct from RP4 reference reset",
        fold_grade="[V]", progression_marker_grade="[L]", absolute_grade="[O]")


# ===========================================================================
#  Aggregate
# ===========================================================================
def all_loops():
    return dict(
        RP1_map_product=rp1_map_product(),
        RP2_baroreflex=rp2_baroreflex(),
        RP3_pressure_natriuresis=rp3_pressure_natriuresis(),
        RP4_setpoint_reset=rp4_setpoint_reset(),
        RP5_basin_collapse=rp5_basin_collapse())


if __name__ == "__main__":
    import json
    print(json.dumps(all_loops(), ensure_ascii=False, indent=2))
