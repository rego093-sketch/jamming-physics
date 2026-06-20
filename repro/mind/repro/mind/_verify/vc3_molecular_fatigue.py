#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VC3  MOLECULAR-SCALE LONG-TERM FATIGUE -- does a reasonable carrier weaken the
     substrate's rigidity over a long horizon?
====================================================================================
The reviewer's photodamage analogy: continuous light slightly weakens a protein; a
carrier driven continuously for a very long time may slightly weaken the lattice
rigidity. This must be tested at the MOLECULAR scale -- the R19 switch the whole
framework rests on -- not the circuit scale. The fatigue law must be DERIVED from the
switch's own relaxation dynamics, with NO new tuned constant.

THE SWITCH (engine, READ-ONLY): ds/dt = g*s - s^3 + h (the double-well R19 primitive).
Its own dynamics give, with no free parameter:
  * relaxation rate at a basin minimum  lambda = 2g  (the eigenvalue d(sdot)/ds at
    s* = sqrt(g); verified here numerically against the engine), so tau_switch = 1/2g.
  * the energy barrier (stability scale)  g^2/4 = barrier(g).
  * the fold (spinodal) edge  |h_sp| = 2(g/3)^1.5 = spinodal(g): the drive past which
    the opposite basin disappears and the switch FLIPS (the molecular damage event).

THE CARRIER IN THE SWITCH'S OWN TIME (no tuned bridge): the engine's FHN neuron runs the
R19 switch at tau_f = 1, so switch-native time IS FHN time; the engine's emergent theta
rhythm is 0.008 cycles per FHN-time. So the physiological theta carrier is omega_theta =
2*pi*0.008 per switch-relaxation-time, and the dimensionless drive-to-relaxation ratio
Omega = omega_theta / lambda is read directly off the engine -- theta sits DEEP in the
quasi-static regime (Omega << 1: the switch relaxes ~40-50x faster than the carrier
cycles).

THE FATIGUE OBSERVABLES (both derived from the switch, no fitted constant):
  IRREVERSIBLE (structural): forced-cycle the FULL nonlinear switch at the carrier and
     ask whether the field ever FLIPS to the opposite basin (a permanent structural
     event = the molecular analogue of a damaged switch). Below the spinodal fold the
     bare switch is a MEMORYLESS RELAXOR (one state variable, no accumulator): it returns
     to its basin every cycle, so irreversible fatigue is ZERO at ANY cycle count. The
     boundary is therefore an AMPLITUDE (the spinodal), not a cycle count.
  REVERSIBLE (thermal): the per-cycle hysteresis loop area W_cycle = closed-integral h ds,
     the work the cycling dissipates and the bath RECOVERS each cycle. In the quasi-static
     theta regime W_cycle is tiny and scales ~ A^2 * omega/(lambda^2+omega^2); it does NOT
     accumulate. Duty-cycling ("cap off during sleep") reduces the time-integrated thermal
     load proportionally.

PRE-REGISTERED (sign-only; both branches declared before any number):
  P-VC3a  at the section-1 window amplitude and physiological theta, cumulative IRREVERSIBLE
          fatigue is BOUNDED / negligible below ANY cycle count (no basin flip -- the
          carrier is far below the spinodal fold) -- OR it is not, in which case report the
          cycle-count at which drift becomes material. The honest result is whichever the
          switch dynamics give; here the boundary is an AMPLITUDE (the spinodal), reported
          as the margin, not a cycle ceiling.
  P-VC3b  a REASONABLE protocol (low amplitude, structured, duty-cycled -- cap off during
          sleep) has materially lower cumulative cost than continuous strong drive
          (quantify the ratio).
  P-VC3c  over-sync-amplitude drive (the section-1 inj >= 0.15 regime) accelerates the
          per-cycle dissipation (~ A^2) and erodes the spinodal margin relative to the
          window amplitude (over-driving is bad at the molecular scale too).

HONESTY: the engine's R19 switch contains NO cumulative-damage state variable. Inventing
one (a slow degradation term) would require a new tuned constant, which no-tuning forbids;
so VC3 reports the bound the ACTUAL dynamics give -- below the fold, a memoryless relaxor
accumulates no structural damage. The deeper finding: the molecular substrate is MORE
robust than the network -- the cap's failure mode is network OVER-SYNC (section 1 / VC1),
not molecular damage.

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
RESULT = os.path.join(HERE, "vc3_molecular_fatigue_results.json")
EXPECT = os.path.join(HERE, "expected_vc3_molecular_fatigue_sha256.json")

# carrier in the switch's own (=FHN) time: the engine's emergent theta rhythm.
# (Population.lfp(tau_inh=60) -> dominant_freq = 0.008 cyc/FHN-time; tau_f=1 => switch time = FHN time.)
F_THETA_FHN = 0.008
A_WINDOW = 0.08            # section-1 / D9.4 window-centre carrier amplitude
A_OVERSYNC = 0.15          # section-1 over-sync onset amplitude
A_STRONG = 0.30            # a continuous strong open-loop amplitude
DUTY_AWAKE = 16.0 / 24.0   # "cap off during 8h sleep" duty fraction


def _measure_lambda(g):
    """relaxation rate magnitude at the basin minimum, from the engine's own sdot."""
    s_star = math.sqrt(g); eps = 1e-6
    return float(-(E.sdot(s_star + eps, g, 0.0) - E.sdot(s_star - eps, g, 0.0)) / (2 * eps))


def _forced_cycle(g, A, omega, n_cycles=6, spc=4000):
    """full nonlinear forced cycling of the R19 switch. Returns (per-cycle loop area
    |closed-integral h ds| over the final cycle, flipped_to_opposite_basin, min_field)."""
    s = math.sqrt(g); dt = (2 * math.pi / omega) / spc; ns = int(n_cycles * spc)
    H = np.empty(ns); S = np.empty(ns); flipped = False; smin = s
    for k in range(ns):
        h = A * math.sin(omega * k * dt)
        s = s + dt * E.sdot(s, g, h)
        H[k] = h; S[k] = s
        if s < 0.0:
            flipped = True
        smin = min(smin, s)
    Hl = H[-spc:]; Sl = S[-spc:]; area = 0.0
    for k in range(len(Sl)):
        area += 0.5 * (Hl[k] + Hl[(k + 1) % len(Sl)]) * (Sl[(k + 1) % len(Sl)] - Sl[k])
    return abs(float(area)), bool(flipped), float(smin)


def _round(o, nd=6):
    if isinstance(o, float): return round(o, nd)
    if isinstance(o, dict):  return {k: _round(v, nd) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v, nd) for v in o]
    return o


E.seed_everything()
_EM = CB.emerge()


def run():
    E.seed_everything()
    em = _EM
    pac_grounded = em["pac_grounded"]
    cells = em["cells"]
    gammas = sorted(set(round(c["gamma"], 4) for c in cells.values()))
    g_min, g_max = min(gammas), max(gammas)
    g_med = gammas[len(gammas) // 2]
    omega = 2 * math.pi * F_THETA_FHN

    # ---- the switch's own relaxation rate (verify lambda = 2g) ----
    lam_checks = []
    lambda_is_2g = True
    for g in (g_min, g_med, g_max):
        lam = _measure_lambda(g)
        ok = bool(abs(lam - 2 * g) < 1e-4)
        lambda_is_2g = lambda_is_2g and ok
        lam_checks.append(dict(gamma=g, measured_lambda=round(lam, 6), expected_2g=round(2 * g, 6),
                               barrier=round(E.barrier(g), 6), spinodal_fold=round(E.spinodal(g), 6),
                               matches=ok))
    Omega_theta = omega / (2 * g_med)
    quasi_static = bool(Omega_theta < 0.1)

    # ---- P-VC3a IRREVERSIBLE: flip test across the cohort + amplitude boundary ----
    # spinodal margin at the window amplitude for every cohort gamma (tightest = most vulnerable)
    margins_window = {f"g={g}": round(E.spinodal(g) - A_WINDOW, 6) for g in gammas}
    min_margin_window = min(margins_window.values())
    # flip test at the representative (median) gamma across amplitudes incl. up to/past the fold
    flip_sweep = []
    first_flip_amp = None
    for A in [A_WINDOW, A_OVERSYNC, A_STRONG, 0.50, round(E.spinodal(g_med), 4), 0.70]:
        W, flipped, smin = _forced_cycle(g_med, A, omega)
        flip_sweep.append(dict(amplitude=round(A, 4), loop_area=round(W, 9),
                               loop_area_frac_of_barrier=round(W / E.barrier(g_med), 9),
                               flips_basin=flipped, min_field=round(smin, 6),
                               margin_to_spinodal=round(E.spinodal(g_med) - A, 6)))
        if first_flip_amp is None and flipped:
            first_flip_amp = round(A, 4)
    no_flip_at_window = bool(not flip_sweep[0]["flips_basin"])
    no_flip_at_oversync = bool(not flip_sweep[1]["flips_basin"])
    # below the fold = memoryless relaxor -> bounded at ANY cycle count. confirm flips only past spinodal.
    flip_boundary_is_spinodal = bool(first_flip_amp is not None and first_flip_amp > E.spinodal(g_med) - 1e-6)
    P_VC3a_irreversible_bounded_below_fold = bool(no_flip_at_window and min_margin_window > 0.0)

    # ---- REVERSIBLE thermal dissipation (per-cycle), and gamma-independence of the ratio ----
    W_window = _forced_cycle(g_med, A_WINDOW, omega)[0]
    W_oversync = _forced_cycle(g_med, A_OVERSYNC, omega)[0]
    W_strong = _forced_cycle(g_med, A_STRONG, omega)[0]
    ratio_oversync_over_window = W_oversync / W_window if W_window > 0 else float("inf")
    # confirm the ratio is amplitude^2 (mechanism, not tuned) and ~gamma-independent
    W_window_gmin = _forced_cycle(g_min, A_WINDOW, omega)[0]
    W_oversync_gmin = _forced_cycle(g_min, A_OVERSYNC, omega)[0]
    ratio_gmin = W_oversync_gmin / W_window_gmin if W_window_gmin > 0 else float("inf")
    amp_sq_ratio = (A_OVERSYNC / A_WINDOW) ** 2

    # ---- P-VC3b duty-cycle: reasonable vs continuous strong / continuous over-sync ----
    # fatigue (reversible thermal load) per fixed wall-clock horizon ~ duty * (per-cycle dissipation)
    reasonable = DUTY_AWAKE * W_window               # window amplitude, off during sleep
    cont_strong = 1.0 * W_strong                     # continuous, strong amplitude
    cont_oversync = 1.0 * W_oversync                 # continuous, over-sync amplitude
    ratio_reasonable_vs_strong = reasonable / cont_strong if cont_strong > 0 else float("inf")
    ratio_reasonable_vs_oversync = reasonable / cont_oversync if cont_oversync > 0 else float("inf")
    P_VC3b_reasonable_materially_lower = bool(ratio_reasonable_vs_strong < 0.5
                                              and ratio_reasonable_vs_oversync < 0.5)

    # ---- P-VC3c over-sync accelerates fatigue + erodes spinodal margin ----
    margin_window_med = E.spinodal(g_med) - A_WINDOW
    margin_oversync_med = E.spinodal(g_med) - A_OVERSYNC
    P_VC3c_oversync_accelerates = bool(ratio_oversync_over_window > 1.0
                                       and margin_oversync_med < margin_window_med)

    out = {
        "_what": "VC3 molecular-scale long-term fatigue at the R19 switch (engine READ-ONLY). The fatigue law "
                 "is DERIVED from the switch's own relaxation dynamics (lambda=2g, barrier=g^2/4, fold "
                 "spinodal=2(g/3)^1.5), with NO new tuned constant. Irreversible structural fatigue = basin "
                 "flips under forced cycling (zero below the fold: the bare switch is a memoryless relaxor); "
                 "reversible thermal load = per-cycle hysteresis loop area (tiny, quasi-static at theta, ~A^2, "
                 "recovered each cycle, duty-reducible). The boundary on long-term use is an AMPLITUDE (the "
                 "spinodal), not a cycle count.",
        "switch_relaxation_dynamics": {
            "lambda_eq_2g_checks": lam_checks,
            "lambda_is_2g_verified": lambda_is_2g,
            "theta_carrier_omega_per_switch_time": round(omega, 6),
            "theta_carrier_freq_cyc_per_switch_time": F_THETA_FHN,
            "quasi_static_ratio_Omega_at_g_med": round(Omega_theta, 6),
            "theta_is_quasi_static": quasi_static,
            "reading": "the switch relaxes ~%.0fx faster than the theta carrier cycles (Omega<<1): the carrier "
                       "is deep in the quasi-static regime, where forced cycling is gentle and the field tracks "
                       "its instantaneous equilibrium." % (1.0 / Omega_theta)},
        "P_VC3a_irreversible_structural_fatigue": {
            "spinodal_margin_at_window_per_gamma": margins_window,
            "min_spinodal_margin_at_window": min_margin_window,
            "flip_sweep_at_g_med": flip_sweep,
            "no_basin_flip_at_window_amplitude": no_flip_at_window,
            "no_basin_flip_at_oversync_amplitude": no_flip_at_oversync,
            "first_flip_amplitude": first_flip_amp,
            "flip_boundary_is_the_spinodal_fold": flip_boundary_is_spinodal,
            "P_VC3a_irreversible_bounded_below_fold_any_cycle_count": P_VC3a_irreversible_bounded_below_fold,
            "reading": "below the spinodal fold the bare R19 switch is a MEMORYLESS RELAXOR: forced cycling at "
                       "the window amplitude (8x below the fold) never flips the basin, at ANY cycle count, so "
                       "cumulative irreversible fatigue is BOUNDED (zero structural events). The boundary on "
                       "long-term use is therefore an AMPLITUDE (the spinodal), reported as the margin, not a "
                       "cycle-count ceiling. The engine has no cumulative-damage variable; inventing one would "
                       "violate no-tuning, so this is the faithful bound the dynamics give."},
        "reversible_thermal_dissipation": {
            "per_cycle_loop_area_window_frac_barrier": round(W_window / E.barrier(g_med), 9),
            "per_cycle_loop_area_oversync_frac_barrier": round(W_oversync / E.barrier(g_med), 9),
            "oversync_over_window_dissipation_ratio": round(ratio_oversync_over_window, 6),
            "amplitude_squared_ratio_expected": round(amp_sq_ratio, 6),
            "ratio_at_g_min": round(ratio_gmin, 6),
            "ratio_is_amplitude_squared_and_gamma_independent": bool(
                abs(ratio_oversync_over_window - amp_sq_ratio) < 0.2 and abs(ratio_oversync_over_window - ratio_gmin) < 0.05),
            "reading": "the only molecular cost of sub-fold cycling is reversible hysteresis dissipation, "
                       "recovered each cycle (it does not accumulate). It is tiny in the quasi-static theta "
                       "regime and scales as amplitude^2 (mechanism, gamma-independent): a thermal-load term, "
                       "not a structural-damage term."},
        "P_VC3b_duty_cycle_reasonable_vs_continuous": {
            "duty_awake_fraction": round(DUTY_AWAKE, 6),
            "reasonable_window_dutycycled_load": round(reasonable, 9),
            "continuous_strong_load": round(cont_strong, 9),
            "continuous_oversync_load": round(cont_oversync, 9),
            "ratio_reasonable_vs_continuous_strong": round(ratio_reasonable_vs_strong, 6),
            "ratio_reasonable_vs_continuous_oversync": round(ratio_reasonable_vs_oversync, 6),
            "P_VC3b_reasonable_materially_lower": P_VC3b_reasonable_materially_lower,
            "reading": "a reasonable protocol (window amplitude, cap off during sleep) carries ~%.0f%% of the "
                       "thermal load of a continuous strong open-loop cap and ~%.0f%% of a continuous over-sync "
                       "cap -- 'jal ttae beotneunda' (off during sleep) plus a reasonable amplitude earns its "
                       "keep as a thermal-load reduction." % (100 * ratio_reasonable_vs_strong,
                                                              100 * ratio_reasonable_vs_oversync)},
        "P_VC3c_oversync_accelerates_fatigue": {
            "oversync_over_window_dissipation_ratio": round(ratio_oversync_over_window, 6),
            "spinodal_margin_window": round(margin_window_med, 6),
            "spinodal_margin_oversync": round(margin_oversync_med, 6),
            "P_VC3c_oversync_accelerates": P_VC3c_oversync_accelerates,
            "reading": "over-sync amplitude raises the per-cycle dissipation ~%.1fx (amplitude^2) and shrinks "
                       "the spinodal margin -- over-driving is worse at the molecular scale too, though even "
                       "the over-sync amplitude stays well below the fold." % ratio_oversync_over_window},
        "deeper_finding": "the molecular substrate is MORE robust than the network: across the whole sub-fold "
                          "range there are zero irreversible structural events at any cycle count, so the cap's "
                          "real failure mode is NETWORK over-synchronisation (section 1 / VC1), not molecular "
                          "damage. Long-term molecular safety of a reasonable, duty-cycled, window-amplitude "
                          "carrier is bounded by a large spinodal margin; the binding constraint is the circuit-"
                          "level over-sync edge, which closed-loop amplitude control (not strong open-loop wear) "
                          "is what manages.",
        "firewall": "mechanism only; efficacy=0; no dose/synthesis; NOT medical advice; Axis-A firewall.",
        "honesty_ledger": {"medium_efficacy_tested": 0, "consciousness_claim": 0,
                           "new_tuned_constants": 0, "no_cure_claimed": 1},
        "invariants": {"engine_tree_frozen": ENGINE_TREE_FROZEN, "pac_grounded": pac_grounded},
        "preregistered_results": {
            "P_VC3a_irreversible_fatigue_bounded_below_fold": {
                "predicted": True, "observed": P_VC3a_irreversible_bounded_below_fold,
                "status": "CONFIRMED" if P_VC3a_irreversible_bounded_below_fold else "REFUTED",
                "note": "the 'bounded' pre-registered branch: no cycle-count ceiling below the fold; the "
                        "boundary is the spinodal AMPLITUDE."},
            "P_VC3b_reasonable_dutycycled_materially_lower": {
                "predicted": True, "observed": P_VC3b_reasonable_materially_lower,
                "status": "CONFIRMED" if P_VC3b_reasonable_materially_lower else "REFUTED"},
            "P_VC3c_oversync_accelerates_fatigue": {
                "predicted": True, "observed": P_VC3c_oversync_accelerates,
                "status": "CONFIRMED" if P_VC3c_oversync_accelerates else "REFUTED"},
        },
    }
    return out


if __name__ == "__main__":
    res = run()
    open(RESULT, "w", encoding="utf-8").write(json.dumps(_round(res), indent=1, sort_keys=True, ensure_ascii=False))
    h = hashlib.sha256(json.dumps(_round(res), sort_keys=True, ensure_ascii=False,
                                  separators=(",", ":")).encode()).hexdigest()
    json.dump({"vc3_molecular_fatigue_results.json": h}, open(EXPECT, "w"), indent=1)
    sd = res["switch_relaxation_dynamics"]; a = res["P_VC3a_irreversible_structural_fatigue"]
    b = res["P_VC3b_duty_cycle_reasonable_vs_continuous"]; c = res["P_VC3c_oversync_accelerates_fatigue"]
    pr = res["preregistered_results"]
    print("VC3 molecular-scale long-term fatigue (R19 switch)")
    print(f"  lambda=2g verified: {sd['lambda_is_2g_verified']}; theta quasi-static Omega={sd['quasi_static_ratio_Omega_at_g_med']} (<<1)")
    print(f"  IRREVERSIBLE: no flip @ window={a['no_basin_flip_at_window_amplitude']}, "
          f"first flip @ A={a['first_flip_amplitude']} (spinodal boundary={a['flip_boundary_is_the_spinodal_fold']}); "
          f"min margin@window={a['min_spinodal_margin_at_window']}")
    print(f"  REVERSIBLE: oversync/window dissipation ratio={res['reversible_thermal_dissipation']['oversync_over_window_dissipation_ratio']} "
          f"(~A^2={res['reversible_thermal_dissipation']['amplitude_squared_ratio_expected']})")
    print(f"  duty-cycle: reasonable vs continuous-strong={b['ratio_reasonable_vs_continuous_strong']}, "
          f"vs continuous-oversync={b['ratio_reasonable_vs_continuous_oversync']}")
    for k, v in pr.items():
        print(f"    {v['status']:<10} {k}")
    print(f"  result sha256: {h}")
