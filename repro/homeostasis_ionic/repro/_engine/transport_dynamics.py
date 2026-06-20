#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
transport_dynamics.py  --  REMEDIATION module (v0.7.0, Tier-3 increment, gap G5): the molecular
TRANSPORT-DYNAMICS primitive -- the "how, molecularly" layer beneath the volume's loop arms.

Closes Tier-3 gap G5 from the v0.4.0 audit (REMEDIATION_PLAN.md). Until now the ion transporters that
do the actual work of the loops -- TRPV5/6 (Ca reabsorption/absorption), ENaC/SCNN1A (Na), the
alpha-intercalated H+-ATPase (acid-base) -- were CITED by NAME and ROLE only; there was no molecular
model of channel GATING or ion FLUX. This is the one place the volume still answered "the loop holds the
setpoint" without saying, at the membrane, HOW. This module supplies that with a NEW PRIMITIVE (the first
new primitive since the substrate): the Goldman-Hodgkin-Katz constant-field ion-flux equation plus a
Boltzmann/Hill channel-gating open-probability.

THE NEW PRIMITIVE (exact physics, [F]):
  * GHK constant-field flux of an ion of valence z through a channel of permeability P, at membrane
    potential Vm, with internal/external concentrations Ci/Co:
        u = z F Vm / (R T)
        Phi = P z u ( Ci - Co e^-u ) / ( 1 - e^-u )        (limit u->0 : Phi = P ( Ci - Co ))
    Flux is zero at the Nernst potential E = (R T / z F) ln(Co/Ci) -- a built-in cross-check.
  * Boltzmann/Hill gating: a channel's open probability responds to its regulator (membrane voltage, or
    a ligand such as 1,25-vitamin-D up-regulating TRPV5/6, or luminal/cytosolic pH for the H+-ATPase).

WHY THIS IS NOT JUST A NEW MODEL BUT A GROUNDING (the load-bearing result, [V]):
  The rest of the volume controls every setpoint with one abstract knob -- the OU loop gain k
  (vp_loops.ou_setpoint: err = load/k, Var = sigma^2/2k, tau = 1/k). k was [O] in absolute units. This
  module shows WHERE k comes from at the membrane: a reabsorptive transporter that defends a controlled
  concentration C runs a net defended flux J(C) = N * p_open(C) * Phi_unit, whose negative slope at the
  setpoint IS the loop gain,
        k_molecular = - dJ/dC | (C = setpoint).
  So the molecular "how" (channel number N, single-channel flux, gating steepness) is not a separate
  story -- it is the SAME k the OU law already uses. We prove the identity by feeding k_molecular back
  into the volume's OWN ou_setpoint and recovering Var = sigma^2/2 k_molecular and err = load/k_molecular.

WHAT IT EXPLAINS (each a reproduced DIRECTION [V]; absolute conductances/densities [O]):
  * Vitamin-D gating: raising the 1,25-vitD signal raises TRPV5/6 open probability -> larger Ca-
    reabsorptive permeability and flux -- the slow VDR arm, now at the channel.
  * Density -> stiffness: raising transporter number N (or gating steepness) raises k_molecular and so
    TIGHTENS the setpoint (Var = sigma^2/2k falls, a load is rejected harder). The molecular substrate of
    a high-gain loop is simply more / steeper channels.
  * Loss-of-function = loop-gain drop, molecularly: a LOF transporter (low N or low max p_open) drops
    k_molecular, inflating variance and the offset under a load -- the membrane-level cause of the
    loop-gain-drop failure mode already derived in setpoint_failure.py. Cited LOF diseases map directly:
    TRPV5 loss -> renal Ca wasting; ENaC/SCNN1A loss -> PHA1 renal salt wasting; H+-ATPase (ATP6V1B1/
    ATP6V0A4) loss -> distal renal tubular acidosis (the same arm whose REPAIR vs buffering is H-ARM).

GRADES (VP-SPEC C3): the GHK constant-field flux and the Boltzmann/Hill gating are EXACT physics [F];
the identity k_molecular = -dJ/dC and its tightening of the OU variance as N rises is reproduced [V]; the
ABSOLUTE single-channel conductances, permeabilities and channel densities (the physical N, P) are [O]
(need electrophysiological calibration -- the same class of residual as TmP/GFR). No clinical efficacy is
asserted. Cited transporter identities / LOF phenotypes are [L].

DETERMINISM (C1): pure deterministic functions of the cited constants + the volume's own ou_setpoint
(sigma=0 where a steady value is needed; the variance demonstration uses the volume's seeded OU); round-
before-return; two runs -> identical sha. This module is ADDITIVE -- it is NOT imported by the research
gate (gamma-emergence + stress battery: gates.py -> vp_ion_engine + stress_tests only), so the research
sha is unchanged.
"""
import os, sys, math, json, hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import importlib
loops = importlib.import_module("vp_loops")

# Physical constants (SI); used only as ratios in u = zFVm/RT, so the scale is exact [F].
F_FARADAY = 96485.0      # C/mol
R_GAS     = 8.314        # J/(mol K)
T_BODY    = 310.15       # K (37 C)
RT_F      = R_GAS * T_BODY / F_FARADAY   # ~26.7 mV thermal voltage


# ===========================================================================
# THE NEW PRIMITIVE 1 -- GHK constant-field ion flux (exact [F])
# ===========================================================================
def ghk_flux(P, z, Vm_mV, Ci, Co):
    """Goldman-Hodgkin-Katz constant-field flux. Vm in mV; Ci/Co in matched concentration units; P a
       permeability in flux/concentration units. Returns flux in P*concentration units (sign: + = inward
       for a cation convention used consistently here). Numerically safe at the small-voltage limit."""
    u = z * (Vm_mV / 1000.0) / RT_F            # dimensionless zFVm/RT
    if abs(u) < 1e-7:                          # L'Hopital limit u->0
        return P * (Ci - Co)
    return P * z * u * (Ci - Co * math.exp(-u)) / (1.0 - math.exp(-u))


def nernst_mV(z, Ci, Co):
    """Equilibrium (reversal) potential E = (RT/zF) ln(Co/Ci), in mV."""
    return 1000.0 * (RT_F / z) * math.log(Co / Ci)


def ghk_checks():
    """The constant-field flux reverses sign exactly at the Nernst potential and rectifies. [F]/[V]."""
    z, Ci, Co, P = 1, 12.0, 145.0, 1.0        # a Na-like gradient (Ci<Co): E>0
    E = nernst_mV(z, Ci, Co)
    flux_at_E   = ghk_flux(P, z, E, Ci, Co)            # must be ~0 (definition of reversal)
    flux_below  = ghk_flux(P, z, E - 30.0, Ci, Co)     # more negative drive -> one sign
    flux_above  = ghk_flux(P, z, E + 30.0, Ci, Co)     # other side of reversal -> opposite sign
    # GHK rectification: with Ci != Co the conductance is voltage-asymmetric about E (|slopes| differ)
    eps = 5.0
    g_neg = (ghk_flux(P, z, E - eps, Ci, Co) - flux_at_E) / (-eps)
    g_pos = (ghk_flux(P, z, E + eps, Ci, Co) - flux_at_E) / (eps)
    return dict(
        nernst_mV=round(E, 4),
        flux_at_nernst=round(flux_at_E, 8),
        reverses_at_nernst=bool(abs(flux_at_E) < 1e-6),
        flux_below_reversal=round(flux_below, 5), flux_above_reversal=round(flux_above, 5),
        flux_changes_sign_across_reversal=bool(flux_below * flux_above < 0),
        chord_slope_hyperpolarized=round(g_neg, 6), chord_slope_depolarized=round(g_pos, 6),
        ghk_rectifies=bool(abs(g_neg - g_pos) > 1e-6),
        grade="[F] GHK constant-field flux is exact; reversal at Nernst and rectification reproduced [V]",
    )


# ===========================================================================
# THE NEW PRIMITIVE 2 -- channel gating (Boltzmann / Hill open probability)
# ===========================================================================
def p_open_boltzmann(signal, half=1.0, slope=0.15):
    """Boltzmann open probability vs a regulator signal (e.g. voltage). slope in signal units."""
    return 1.0 / (1.0 + math.exp(-(signal - half) / slope))


def p_open_hill(ligand, half=1.0, n=2.0):
    """Hill open probability vs a ligand (e.g. 1,25-vitD up-regulating TRPV5/6). Saturating, monotone up."""
    x = max(ligand, 0.0) ** n
    return x / (half ** n + x)


def vitamin_d_gating():
    """The slow VDR arm at the channel: raising the 1,25-vitamin-D signal raises TRPV5/6 open probability
       and hence the Ca-reabsorptive permeability/flux. Direction [V]; absolute EC50 [O]."""
    z, Ci, Co, Vm = 2, 0.1, 1.2, -60.0          # a Ca-like reabsorptive gradient at a resting Vm
    levels = [0.25, 0.5, 1.0, 2.0, 4.0]         # 1,25-vitD signal (dimensionless, baseline=1)
    rows = []
    for L in levels:
        po = p_open_hill(L, half=1.0, n=2.0)
        P_eff = po                               # permeability scales with open probability (unit channel)
        # reabsorptive Ca flux MAGNITUDE (the channel conducts Ca inward; the reabsorption rate = |GHK flux|)
        J = abs(ghk_flux(P_eff, z, Vm, Ci, Co))
        rows.append(dict(vitd_signal=L, p_open=round(po, 5), ca_reabsorptive_flux=round(J, 5)))
    popens = [r["p_open"] for r in rows]; fluxes = [r["ca_reabsorptive_flux"] for r in rows]
    mono = lambda xs: all(xs[i] <= xs[i + 1] + 1e-12 for i in range(len(xs) - 1))
    return dict(
        levels=rows,
        open_probability_rises_with_vitd=bool(mono(popens)),
        ca_flux_rises_with_vitd=bool(mono(fluxes)),
        anchor="1,25-dihydroxyvitamin-D (VDR arm) transcriptionally up-regulates the epithelial Ca channels "
               "TRPV5 (kidney) / TRPV6 (gut) and calbindin -> raises transcellular Ca reabsorption/absorption",
        grade="[L] VDR->TRPV5/6 identity; [V] open probability and Ca flux rise monotonically with the "
              "vitamin-D signal (Hill gating x GHK flux); [O] absolute EC50 / single-channel permeability",
    )


# ===========================================================================
# THE GROUNDING -- molecular flux slope IS the OU loop gain k
# ===========================================================================
# A reabsorptive transporter defends a controlled concentration C about its setpoint C*=1. Its open
# probability is a NEGATIVE-FEEDBACK gate: when C falls below setpoint the controller (e.g. PTH) opens
# more channels, so p_open decreases with C. The net defended flux is J(C) = N * p_open(C) * Phi_unit(C).
# k_molecular = -dJ/dC | C* is exactly the proportional loop gain the OU law uses.
_Z_CA, _CI_CA, _CO_CA, _VM = 2, 0.1, 1.2, -60.0     # Ca-like reabsorptive channel operating point
_SETPOINT = 1.0
# Single-channel reabsorptive flux MAGNITUDE from the GHK equation at the operating point. _P_UNIT is the
# uncalibrated single-channel permeability ([O]); it is chosen so the molecular loop gain lands in the
# regime where the discrete OU law is faithful (k*dt << 1). The GROUNDING is scale-free: k scales linearly
# with channel number N regardless of this unit, and the OU laws Var=sigma^2/2k, err=load/k are recovered.
_P_UNIT = 0.11
_PHI1 = abs(ghk_flux(_P_UNIT, _Z_CA, _VM, _CI_CA, _CO_CA))   # fixed positive per-channel reabsorptive flux


def _defended_flux(C, N, gate_slope=0.15, gmax=1.0):
    """Net reabsorptive flux that RAISES the controlled concentration C, defended about the setpoint.
       The controller modulates the channel OPEN PROBABILITY in negative feedback: p_open FALLS as C rises
       above setpoint (channels are opened when C is low), so the defended flux falls with C -> restoring.
       The single-channel flux _PHI1 is the (fixed) GHK driving flux; the controlled-variable sensitivity
       lives entirely in the gate. k = -dJ/dC > 0 is therefore N * _PHI1 * |dp_open/dC|."""
    p_open = gmax / (1.0 + math.exp((C - _SETPOINT) / gate_slope))
    return N * p_open * _PHI1


def _k_molecular(N, gate_slope=0.15, gmax=1.0, h=1e-3):
    """Loop gain from the membrane: k = -dJ/dC at the setpoint (central difference)."""
    Jp = _defended_flux(_SETPOINT + h, N, gate_slope, gmax)
    Jm = _defended_flux(_SETPOINT - h, N, gate_slope, gmax)
    return -(Jp - Jm) / (2.0 * h)


def molecular_gain_grounds_k():
    """Show k_molecular = -dJ/dC, that it RISES with channel number N and gating steepness, and that it
       is the SAME k the OU law uses: feeding k_molecular into vp_loops.ou_setpoint reproduces
       Var = sigma^2/2k and err = load/k. This is the load-bearing grounding result."""
    loops.seed_everything()
    sigma = 0.3
    densities = [0.5, 1.0, 2.0, 4.0]                     # channel number N (healthy ladder)
    rows = []
    for N in densities:
        k = _k_molecular(N)
        st = loops.ou_setpoint(k, sigma=sigma, load=0.0)          # variance under noise
        det = loops.ou_setpoint(k, sigma=0.0, load=1.0)           # step error under a load
        rows.append(dict(channel_number=N, k_molecular=round(k, 6),
                         ou_variance=st["variance"], var_times_2k_over_sigma2=round(st["variance"] * 2 * k / sigma ** 2, 3),
                         step_error=det["mean_offset"], error_times_k=round(det["mean_offset"] * k, 3)))
    ks = [r["k_molecular"] for r in rows]
    vars_ = [r["ou_variance"] for r in rows]
    k_monotone_in_density = all(ks[i] <= ks[i + 1] + 1e-9 for i in range(len(ks) - 1))
    variance_falls_with_density = all(vars_[i] >= vars_[i + 1] - 1e-9 for i in range(len(vars_) - 1))
    var_law_ok = all(0.7 <= r["var_times_2k_over_sigma2"] <= 1.3 for r in rows)
    err_law_ok = all(0.9 <= r["error_times_k"] <= 1.1 for r in rows)
    # gating steepness also raises k (steeper gate = stiffer loop) at fixed N
    k_shallow = _k_molecular(1.0, gate_slope=0.30)
    k_steep = _k_molecular(1.0, gate_slope=0.075)
    steeper_gate_raises_k = bool(k_steep > k_shallow)
    return dict(
        ladder=rows,
        k_is_minus_dJ_dC="k_molecular = -dJ/dC at the setpoint -- the proportional restoring flux per unit deviation",
        k_rises_with_channel_number=bool(k_monotone_in_density),
        setpoint_variance_falls_with_channel_number=bool(variance_falls_with_density),
        ou_variance_law_recovered=bool(var_law_ok),
        ou_rejection_law_recovered=bool(err_law_ok),
        steeper_gate_raises_k=steeper_gate_raises_k,
        k_molecular_is_the_OU_loop_gain=bool(var_law_ok and err_law_ok),
        grade="[F] GHK flux + gating exact; [V] k=-dJ/dC rises with channel number / gating steepness and, "
              "fed into the volume's own ou_setpoint, recovers Var=sigma^2/2k and err=load/k -- the molecular "
              "gain IS the loop gain; [O] absolute channel density / single-channel permeability",
    )


# ===========================================================================
# DISEASE -- loss-of-function transporter = loop-gain drop at the membrane
# ===========================================================================
_CITED_LOF = [
    ("TRPV5 / TRPV6 (epithelial Ca channels)", "loss -> renal/intestinal Ca wasting (hypercalciuria); the VDR arm's effector"),
    ("ENaC / SCNN1A,B,G (epithelial Na channel)", "loss -> pseudohypoaldosteronism type 1 (PHA1): renal salt wasting, hyperkalemia"),
    ("H+-ATPase (ATP6V1B1 / ATP6V0A4, a-intercalated cell)", "loss -> distal renal tubular acidosis (the acid arm of H-ARM)"),
]


def lof_is_loop_gain_drop():
    """A loss-of-function transporter (low channel number N, or low max open probability) drops
       k_molecular, so the SAME load leaves a larger offset and the variance inflates -- the membrane-
       level realization of the loop-gain-drop failure mode (setpoint_failure.py). Direction [V]."""
    loops.seed_everything()
    N_healthy, N_lof = 4.0, 1.0
    k_healthy = _k_molecular(N_healthy)
    k_lof = _k_molecular(N_lof)
    # same load, two gains: offset = load/k
    off_healthy = loops.ou_setpoint(k_healthy, sigma=0.0, load=1.0)["mean_offset"]
    off_lof = loops.ou_setpoint(k_lof, sigma=0.0, load=1.0)["mean_offset"]
    var_healthy = loops.ou_setpoint(k_healthy, sigma=0.3)["variance"]
    var_lof = loops.ou_setpoint(k_lof, sigma=0.3)["variance"]
    # also: a reduced MAX open probability (partial LOF) lowers k at fixed N
    k_partial = _k_molecular(N_healthy, gmax=0.4)
    return dict(
        k_healthy=round(k_healthy, 6), k_lof=round(k_lof, 6),
        lof_drops_k=bool(k_lof < k_healthy),
        offset_healthy=off_healthy, offset_lof=off_lof,
        lof_offset_larger=bool(abs(off_lof) > abs(off_healthy) + 1e-9),
        offset_ratio=round(abs(off_lof) / abs(off_healthy), 3),
        predicted_ratio_k_healthy_over_k_lof=round(k_healthy / k_lof, 3),
        offset_ratio_matches_gain_law=bool(abs(abs(off_lof) / abs(off_healthy) - k_healthy / k_lof) < 1e-2),
        variance_healthy=var_healthy, variance_lof=var_lof, lof_variance_blows_up=bool(var_lof > var_healthy),
        partial_lof_max_popen_also_drops_k=bool(k_partial < k_healthy),
        cited_lof_transporters=[{"transporter": t, "phenotype": p} for t, p in _CITED_LOF],
        anchor="loss-of-function of an epithelial ion transporter weakens the loop arm it serves: "
               "TRPV5/6 -> renal/gut Ca wasting; ENaC/SCNN1A -> PHA1 salt wasting; H+-ATPase (ATP6V) -> distal RTA",
        grade="[L] cited LOF transporter->disease identities; [V] a LOF transporter (low N or low max "
              "open probability) drops k_molecular, enlarging the offset (ratio == gain ratio) and inflating "
              "variance -- the membrane cause of the loop-gain-drop mode; [O] absolute conductances",
    )


# ===========================================================================
# status (frontier-style honest roll-up)
# ===========================================================================
def status():
    loops.seed_everything()
    gh = ghk_checks()
    vd = vitamin_d_gating()
    mg = molecular_gain_grounds_k()
    lf = lof_is_loop_gain_drop()

    ghk_ok = bool(gh["reverses_at_nernst"] and gh["flux_changes_sign_across_reversal"] and gh["ghk_rectifies"])
    vd_ok = bool(vd["open_probability_rises_with_vitd"] and vd["ca_flux_rises_with_vitd"])
    grd_ok = bool(mg["k_rises_with_channel_number"] and mg["setpoint_variance_falls_with_channel_number"]
                  and mg["k_molecular_is_the_OU_loop_gain"] and mg["steeper_gate_raises_k"])
    lof_ok = bool(lf["lof_drops_k"] and lf["lof_offset_larger"] and lf["offset_ratio_matches_gain_law"]
                  and lf["lof_variance_blows_up"])
    demonstrations_pass = bool(ghk_ok and vd_ok and grd_ok and lof_ok)

    return {
        "_what": "Tier-3 molecular transport-dynamics primitive (gap G5): the GHK constant-field ion-flux "
                 "equation + Boltzmann/Hill channel gating -- the molecular 'how' beneath the loop arms. The "
                 "load-bearing result is the grounding k_molecular = -dJ/dC: the membrane flux slope IS the "
                 "OU loop gain the rest of the volume uses, so channel number / gating steepness set setpoint "
                 "stability, and a loss-of-function transporter is the loop-gain-drop failure mode at the membrane.",
        "new_primitive": "GHK constant-field flux (ghk_flux) + channel gating (p_open_boltzmann / p_open_hill)",
        "GHK_constant_field_flux": gh,
        "vitamin_d_channel_gating": vd,
        "molecular_gain_grounds_loop_gain_k": mg,
        "loss_of_function_is_loop_gain_drop": lf,
        "GHK_checks_pass": ghk_ok,
        "vitamin_d_gating_pass": vd_ok,
        "grounding_pass": grd_ok,
        "lof_pass": lof_ok,
        "demonstrations_pass": demonstrations_pass,
        "grade": "[F] GHK constant-field flux + Boltzmann/Hill gating are exact physics; [V] k_molecular=-dJ/dC "
                 "is the OU loop gain (recovers Var=sigma^2/2k and err=load/k), rises with channel number / "
                 "gating steepness, and a LOF transporter drops it (loop-gain-drop at the membrane); [L] cited "
                 "transporter identities and LOF phenotypes; [O] absolute single-channel conductances / channel "
                 "densities (electrophysiological calibration, the TmP/GFR class of residual)",
    }


if __name__ == "__main__":
    s = json.dumps(status(), sort_keys=True)
    print(json.dumps(status(), indent=1))
    print("sha:", hashlib.sha256(s.encode()).hexdigest()[:12])
