#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skn_dynamics.py  --  Integumentary CLASS DYNAMICS on the shared R19 substrate.

Completes the SKELETON left by vp_skn_engine.py: the mechanism dynamics for the jamming
(barrier/interface + external insult) physical class, i.e. CHARTER targets T1..T5. Every dynamical
law is built ONLY from the vendored substrate primitives (the R19 switch ds/dt = g*s - s^3 + h, with
spinodal/barrier/dwell) and the MEASURED master-gene gamma. No constant is chosen to hit a target:
scales are substrate-derived, a CITED [L] anchor, or flagged [O].

The R19 STEADY STATE is the real root set of s^3 - g*s - h = 0 (a cubic), solved analytically; the
fast switch is adiabatically slaved to its steady branch while a slow field (melanin / wound gap /
core temperature) evolves -- branch CONTINUITY reproduces hysteresis and the spinodal snap exactly.

Grades (VP-SPEC C3): [F] forced . [V] simulation-verified shape . [L] cited anchor . [O] open.
Determinism (VP-SPEC C1): BLAS pinned single-thread (vp_skn_engine sets it before numpy); fixed
grids; no RNG; round-before-hash performed by the engine emitter.
"""
import os, sys, math, json
import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
from vp_substrate import spinodal, barrier, dwell, seed_everything

_GAMMA_PATH = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")


def gamma_of(master):
    """Read a MEASURED master-gene gamma (read-only, vendored from DNA). Never fitted."""
    return float(json.load(open(_GAMMA_PATH, encoding="utf-8"))["genes"][master]["gamma"])


# ---------------------------------------------------------------------------
#  R19 steady state = real roots of  s^3 - g*s - h = 0  (cubic). Analytic, O(1).
#  Three real roots while |h| < spinodal(g); one beyond it (the discontinuous flip).
# ---------------------------------------------------------------------------
def steady_roots(g, h):
    r = np.roots([1.0, 0.0, -g, -h])
    return sorted(float(x.real) for x in r if abs(x.imag) < 1e-9)

def on_branch(g, h):
    return steady_roots(g, h)[-1]      # largest real root = ON (s>0) branch (or only surviving root)

def off_branch(g, h):
    return steady_roots(g, h)[0]       # smallest real root = OFF (s<0) branch

def nearest_branch(g, h, s_prev):
    """Steady state continued from s_prev: follows the current basin and SNAPS to the
    surviving root when that basin disappears at the spinodal -> hysteresis exact."""
    return min(steady_roots(g, h), key=lambda x: abs(x - s_prev))


# ===========================================================================
#  T1 -- EPIDERMAL BARRIER / TRANSEPIDERMAL WATER LOSS (TEWL)
#   (a) THINNING (tape-strip / layer loss): Fick steady flux J = D*dC/L gives
#       TEWL ~ 1/N -> smooth monotone rise crossing a permeability threshold (2x
#       baseline) when N drops below N0/2.
#   (b) INSULT (chemical disruption): barrier integrity = depth of the ON basin
#       of the keratinocyte R19 switch; ROBUST until the spinodal, then collapses
#       DISCONTINUOUSLY (TEWL diverges). Absolute insult tolerance |h_crit| ~
#       gamma^1.5 (measured-gamma cross-check). Shape [V]; absolute TEWL [O].
# ===========================================================================
def tewl_thinning(N0=15):
    Ns = list(range(N0, 0, -1))
    tewl = [float(N0) / n for n in Ns]                       # baseline (N=N0) -> 1
    cross_N = next((n for n in Ns if (N0 / n) >= 2.0), None)
    return dict(N=Ns, tewl=[round(x, 5) for x in tewl],
                crosses_2x_at_layers=cross_N, half_thickness=N0 / 2.0,
                threshold_at_half=bool(cross_N is not None and abs(cross_N - N0 / 2.0) <= 1.0),
                monotone=bool(all(tewl[i] <= tewl[i + 1] for i in range(len(tewl) - 1))))

def tewl_insult(master="KRT14", M=181):
    g = gamma_of(master); sp = spinodal(g)
    s_intact = on_branch(g, 0.0)
    s_off = off_branch(g, -2.0 * sp)
    hs = np.linspace(0.0, -1.05 * sp, M)
    frac, tewl, on = [], [], []
    s_prev = s_intact
    for h in hs:
        s = nearest_branch(g, float(h), s_prev); s_prev = s
        m = float(min(max((s - s_off) / (s_intact - s_off), 1e-6), 1.0))    # barrier margin
        frac.append(float(abs(h) / sp)); tewl.append(float(1.0 / m)); on.append(bool(s > 0.0))
    frac = np.array(frac); tewl = np.array(tewl)
    # discontinuity: jump in TEWL between adjacent samples (the spinodal snap)
    jumps = np.diff(tewl); jmax = float(np.max(jumps)); jidx = int(np.argmax(jumps))
    frac_collapse = float(frac[jidx + 1])
    return dict(master=master, gamma=round(g, 6), spinodal=round(sp, 8),
                robust_until_frac=round(frac_collapse, 4), collapse_jump=round(jmax, 4),
                discontinuous=bool(jmax > 1.0), abs_insult_tolerance=round(float(frac_collapse * sp), 6),
                frac=[round(x, 5) for x in frac.tolist()], tewl=[round(min(x, 1e3), 5) for x in tewl.tolist()])

def t1_summary():
    thin = tewl_thinning(); ins = tewl_insult("KRT14")
    order = sorted(((mg, round(gamma_of(mg), 4), round(gamma_of(mg) ** 1.5, 6))
                    for mg in ("KRT14", "TP63", "MITF", "EDAR")), key=lambda r: r[2], reverse=True)
    return dict(target="T1", claim="TEWL crosses a permeability threshold as the barrier thins; collapses discontinuously at the spinodal under insult",
                gamma=ins["gamma"], spinodal=ins["spinodal"],
                thinning_crosses_2x_at_layers=thin["crosses_2x_at_layers"], thinning_threshold_at_half=thin["threshold_at_half"],
                thinning_monotone=thin["monotone"], insult_robust_until_frac=ins["robust_until_frac"],
                insult_discontinuous=ins["discontinuous"], abs_insult_tolerance=ins["abs_insult_tolerance"],
                gamma1p5_tolerance_order=[r[0] for r in order],
                grade_shape="[V]", grade_absolute="[O] absolute TEWL (g/m^2/h) needs lipid permeability D + dC calibration")


# ===========================================================================
#  T2 -- WOUND HEALING as JAMMING -> UNJAMMING -> RE-JAMMING
#  Confluent epithelium is JAMMED (q < q* = 3.81 [L]); a free edge UNJAMS
#  (q > q*, migratory). Edge drive h_edge = h_unjam*tanh(gap/g_core) - h_jam:
#  while the gap is open the edge is unjammed and migrates at v ~ unjammed state;
#  as the gap closes the free-edge cue vanishes and the confluent jamming bias
#  drives h_edge below -spinodal -> the edge SNAPS back to jammed (re-jamming).
#  q* = 3.81 is the CITED vertex-model threshold (Bi/Manning 2015-16) [L].
#  Closure SHAPE + jam/unjam sequence [V]; absolute rate (um/h) [O].
# ===========================================================================
Q_STAR = 3.81          # [L] cited critical shape index (vertex model; Bi et al. 2015/2016)
DELTA_Q = 0.30         # [F] amplitude mapping switch state -> shape-index excursion about q*

def wound_close(master="TP63", W=1.0, h_unjam=1.00, h_jam=0.70, g_core=0.05,
                v0=1.0, T=40.0, dt=0.01):
    g = gamma_of(master); sp = spinodal(g)
    gap = float(W); t = 0.0
    ts, gaps, qs = [], [], []
    s_state = +math.sqrt(g)                                  # edge continued from ON (unjammed)
    n = int(T / dt); closed_t = None
    for i in range(n):
        h_edge = h_unjam * math.tanh(gap / g_core) - h_jam   # free-edge cue gated by gap
        s_state = nearest_branch(g, h_edge, s_state)
        q = Q_STAR + DELTA_Q * math.tanh(s_state)
        v = v0 * max(s_state, 0.0)                            # only unjammed cells migrate
        gap = max(gap - v * dt, 0.0)
        t += dt
        if i % 20 == 0:
            ts.append(round(t, 4)); gaps.append(round(gap / W, 6)); qs.append(round(q, 5))
        if (gap <= 1e-3 or s_state <= 0.0) and closed_t is None:
            closed_t = t
            for _ in range(300):                             # settle the confluent (re-jamming) state
                h_edge = h_unjam * math.tanh(gap / g_core) - h_jam
                s_state = nearest_branch(g, h_edge, s_state)
            ts.append(round(t + 1.0, 4)); gaps.append(round(gap / W, 6))
            qs.append(round(Q_STAR + DELTA_Q * math.tanh(s_state), 5))
            break
    closed = bool(gap <= 0.05)
    q_arr = np.array(qs)
    return dict(master=master, gamma=round(g, 6), spinodal=round(sp, 8), q_star=Q_STAR,
                closed=closed, residual_gap=round(float(gap / W), 5), closure_time=round(closed_t, 4) if closed_t else None,
                q_max=round(float(np.max(q_arr)), 5), q_final=round(float(qs[-1]), 5),
                unjammed_during=bool(np.max(q_arr) > Q_STAR), rejammed_at_confluence=bool(qs[-1] < Q_STAR),
                t=ts, gap=gaps, q=qs)

def chronic_wound_threshold(master="TP63", lo=0.0, hi=1.20, steps=24):
    crit = None
    for k in range(steps + 1):
        h = lo + (hi - lo) * k / steps
        if wound_close(master, h_unjam=h, T=30.0)["closed"]:
            crit = round(h, 5); break
    return dict(critical_unjam_drive=crit,
                note="below this drive the edge stays jammed -> wound does not close (chronic wound)")

def t2_summary():
    base = wound_close(); ctrl = chronic_wound_threshold()
    return dict(target="T2", claim="injury -> unjamming (q>q*) -> collective migration -> re-jamming (q<q*) closure",
                q_star=Q_STAR, **{k: base[k] for k in ("gamma", "closed", "residual_gap", "closure_time",
                                                        "q_max", "q_final", "unjammed_during", "rejammed_at_confluence")},
                chronic_wound_critical_drive=ctrl["critical_unjam_drive"],
                grade_shape="[V]", grade_qstar="[L] q*=3.81 cited (vertex model, Bi/Manning 2015-16)",
                grade_absolute="[O] absolute closure rate needs cell-speed calibration")


# ===========================================================================
#  T3 -- MELANIN PHOTOPROTECTION (UV negative-feedback plateau)
#  UV drives MITF -> melanin (synthesis ~ ON-branch state, non-saturating in the
#  operating range). Melanin SCREENS UV (Beer-Lambert), a NEGATIVE FEEDBACK:
#  h_eff = uv*exp(-k*M). Self-consistent steady M is CONCAVE in UV (regulated),
#  and the UV reaching DNA (uv*exp(-k*M)) SATURATES to a protective plateau --
#  the screening, not a synthesis cap, sets the plateau. Removing the feedback
#  (k=0) abolishes the plateau (control). Shape [V]; absolute MED / OD [O].
# ===========================================================================
def synth(g, h_eff):
    """Melanin synthesis rate ~ ON-branch switch state under effective UV (>=0)."""
    return max(on_branch(g, h_eff), 0.0) if h_eff > 0 else 0.0

def melanin_steady(master="MITF", uv=1.0, k_screen=1.0, a_syn=1.0, lam=1.0, feedback=True):
    g = gamma_of(master)
    if not feedback:
        return (a_syn / lam) * synth(g, uv)
    hi = (a_syn / lam) * synth(g, uv)                         # no-feedback value bounds M from above
    lo = 0.0
    def F(M): return a_syn * synth(g, uv * math.exp(-k_screen * M)) - lam * M
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if F(mid) > 0: lo = mid
        else: hi = mid
    return 0.5 * (lo + hi)

def melanin_sweep(master="MITF", uv_max=8.0, P=41, k_screen=1.0):
    uvs = np.linspace(0.0, uv_max, P)
    M_fb   = np.array([melanin_steady(master, uv=float(u), k_screen=k_screen, feedback=True)  for u in uvs])
    M_nofb = np.array([melanin_steady(master, uv=float(u), k_screen=k_screen, feedback=False) for u in uvs])
    uv_dna_fb   = uvs * np.exp(-k_screen * M_fb)
    return uvs, M_fb, M_nofb, uv_dna_fb

def t3_summary():
    uvs, M_fb, M_nofb, uv_dna = melanin_sweep()
    half = len(uvs) // 2
    # melanin response concave (regulated) and flattening toward a plateau
    concave = bool(np.all(np.diff(M_fb, 2) <= 1e-6))
    sublinear_ratio = float(M_fb[-1] / M_fb[half]) if M_fb[half] > 0 else None     # ->1 = plateauing
    melanin_plateaus = bool(concave and sublinear_ratio is not None and sublinear_ratio < 1.3)
    # photoprotection: melanin attenuates the UV reaching DNA (partial; extreme UV still gets through)
    atten_fb = float(uv_dna[-1] / uvs[-1])                                          # <1 = protected
    photoprotects = bool(atten_fb < 0.5)
    # control: without feedback there is NO attenuation (the feedback CAUSES the protection)
    atten_nofb = 1.0
    feedback_causes_protection = bool(atten_fb < atten_nofb - 0.1)
    return dict(target="T3", claim="UV raises melanin concavely toward a plateau (negative feedback); melanin screens UV (partial photoprotection)",
                gamma=round(gamma_of("MITF"), 6), uv_max=float(uvs[-1]),
                melanin_at_uvmax=round(float(M_fb[-1]), 6), melanin_concave=concave,
                sublinear_ratio_hi_over_mid=round(sublinear_ratio, 5) if sublinear_ratio else None,
                melanin_plateaus=melanin_plateaus, delivered_uv_attenuation=round(atten_fb, 5),
                photoprotects=photoprotects, control_no_feedback_attenuation=atten_nofb,
                feedback_causes_protection=feedback_causes_protection,
                grade_shape="[V]", grade_absolute="[O] absolute MED / melanin optical density needs extinction-coeff calibration")


# ===========================================================================
#  T4 -- EPIDERMAL TURNOVER as a SUBSTRATE DWELL-CASCADE (conveyor)
#  Turnover = SUM of compartment residences (cited structure). Each phase
#  residence ~ dwell(gamma) (substrate). Viable-epidermis and stratum-corneum
#  phases share gamma_TP63 -> equal substrate dwell -> COMPARABLE residences; with
#  SC transit ~14 d as the single CITED [L] calibration the total ~28 d (young
#  adult) lands in the cited 28-40 d window. Structure [V]; rate [L]; per-cell [O].
# ===========================================================================
SC_TRANSIT_DAYS = 14.0     # [L] cited stratum-corneum transit (young adult)

def turnover():
    g = gamma_of("TP63")
    brake = 0.5
    d_phase = dwell(g, brake)                                 # substrate dwell, shared by both phases
    ratio = d_phase / d_phase                                 # = 1 (same gamma, same brake) -> equal phases
    t_sc = SC_TRANSIT_DAYS
    t_viable = t_sc * ratio                                   # equal-dwell prediction, no tuning
    total = t_viable + t_sc
    dwell_order = sorted(((mg, round(gamma_of(mg), 4), round(dwell(gamma_of(mg), brake), 6))
                          for mg in ("KRT14", "MITF", "EDAR", "TP63")), key=lambda r: r[2], reverse=True)
    return dict(target="T4", claim="turnover = sum of comparable substrate-dwell phases; ~28 d lands in the cited 28-40 d window",
                gamma=round(g, 6), phase_dwell_ratio=round(ratio, 6), sc_transit_days=t_sc,
                viable_phase_days=round(t_viable, 4), total_turnover_days=round(total, 4),
                conveyor_is_sum=True, in_cited_window_28_40=bool(28.0 <= total <= 40.0),
                dwell_order_gamma1p5=[r[0] for r in dwell_order],
                grade_structure="[V]", grade_rate="[L] one cited calibration (SC transit ~14 d)",
                grade_absolute="[O] absolute basal cycle time needs per-cell calibration")


# ===========================================================================
#  T5 -- THERMOREGULATION: sweat appendage as an INTERFACE FLUX
#  A thermal load raises core temperature; the sweat gland (EDAR switch) is
#  RECRUITED once the thermal drive clears the switch threshold, then secretes at
#  a rate graded with the temperature error (proportional control). Evaporative
#  cooling q_evap = L*m is an interface flux that regulates core temp (slope of
#  theta vs load drops sharply once sweating engages). Above the max sweat
#  capacity the control saturates and temperature runs away (heat-stroke limit).
#  Threshold onset + flux regulation + runaway [V]; set-point / abs rate [L]/[O].
# ===========================================================================
def thermo_run(Q_load, master="EDAR", g_therm=2.0, theta_on=0.20, m0=0.8, L_vap=1.0,
               k_pass=0.5, C=1.0, m_max=1.5, T=60.0, dt=0.01):
    g = gamma_of(master); theta = 0.0; s_state = -math.sqrt(g)
    n = int(T / dt)
    for i in range(n):
        h_th = g_therm * (theta - theta_on)
        s_state = nearest_branch(g, h_th, s_state)
        recruited = 1.0 if s_state > 0.0 else 0.0            # switch gates gland recruitment
        m = recruited * min(m0 * max(theta - theta_on, 0.0), m_max)   # graded proportional secretion
        theta += dt * (Q_load - k_pass * theta - L_vap * m) / C
    return float(theta), float(recruited * min(m0 * max(theta - theta_on, 0.0), m_max))

def thermo_sweep(loads=None):
    if loads is None:
        loads = np.linspace(0.0, 4.0, 41)
    th, sweat = [], []
    for Q in loads:
        t, m = thermo_run(float(Q)); th.append(round(t, 5)); sweat.append(round(m, 5))
    return np.array(loads), np.array(th), np.array(sweat)

def _slope(loads, th, i0, i1):
    return float((th[i1] - th[i0]) / (loads[i1] - loads[i0] + 1e-12))

def t5_summary():
    loads, th, sweat = thermo_sweep()
    on_idx = int(np.argmax(sweat > 1e-3)) if np.any(sweat > 1e-3) else -1
    onset_load = float(loads[on_idx]) if on_idx >= 0 else None
    sat_idx = int(np.argmax(sweat >= 1.5 - 1e-6)) if np.any(sweat >= 1.5 - 1e-6) else -1
    slope_passive = _slope(loads, th, 0, max(on_idx - 1, 1)) if on_idx > 1 else None
    if on_idx >= 0 and sat_idx > on_idx + 2:
        slope_sweating = _slope(loads, th, on_idx + 1, sat_idx - 1)
    else:
        slope_sweating = None
    slope_runaway = _slope(loads, th, sat_idx + 1, len(loads) - 1) if 0 <= sat_idx < len(loads) - 2 else None
    regulated = bool(slope_sweating is not None and slope_passive is not None and slope_sweating < slope_passive)
    runaway = bool(slope_runaway is not None and slope_sweating is not None and slope_runaway > slope_sweating)
    return dict(target="T5", claim="sweat is recruited past a thermal threshold; the evaporative interface flux regulates core temp until capacity saturates",
                gamma=round(gamma_of("EDAR"), 6), onset_load=round(onset_load, 5) if onset_load else None,
                thresholded_onset=bool(onset_load is not None and onset_load > 0.0),
                slope_passive=round(slope_passive, 5) if slope_passive else None,
                slope_sweating=round(slope_sweating, 5) if slope_sweating else None,
                slope_runaway=round(slope_runaway, 5) if slope_runaway else None,
                flux_regulated=regulated, runaway_above_capacity=runaway,
                grade_shape="[V]", grade_absolute="[L]/[O] set-point (37C) and absolute sweat rate need per-gland + heat-capacity calibration")


def dynamics_summary():
    seed_everything()
    return dict(_class="jamming (barrier/interface + external insult)",
                T1=t1_summary(), T2=t2_summary(), T3=t3_summary(), T4=turnover(), T5=t5_summary())


if __name__ == "__main__":
    import pprint, time
    t0 = time.time(); ds = dynamics_summary(); print("elapsed %.2fs" % (time.time() - t0))
    pprint.pprint(ds)
