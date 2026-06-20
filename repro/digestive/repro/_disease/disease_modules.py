#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
disease_modules.py  --  Digestive / Metabolic DISEASE modules (Tier-1 perturbations of built modules).

These three modules are PERTURBATIONS of already-validated mechanisms; they introduce NO new substrate
primitive (FUTURE_WORK.md Tier 1). Each disease moves ONE parameter of an existing module and the
pathological phenotype EMERGES -- it is never fitted. Grades follow C3: emergent mechanism [V];
cited clinical thresholds [L]; absolute population rates [O] (obstacle stated in the ledger).

  D1  Gastric dysrhythmia + gastroparesis   -- perturbs the gastric pacemaker / slow-wave chain (s2/s3)
        * dysrhythmia : the FHN rate parameter tau_s moves the recorded slow-wave through the cited EGG
          band -> bradygastria (<2.5 cpm) / normal (~3 cpm) / tachygastria (>3.7 cpm). [V] / [L] band
        * ectopic focus : a faster distal pacemaker, once it out-paces the antrum AND couples, ENTRAINS
          the recording upward past the tachygastria threshold (the clinical mechanism of tachygastria). [V]
        * gastroparesis : ICC pacemaker density rho scales the antral contraction; emptying RATE
          (displacement in a fixed window) falls monotonically with rho, with functional reserve then
          collapse -- "delayed emptying emerges from ICC depletion; rate tracks density". [V] / [O] abs rate

  D2  Diabetes (T1/T2 spectrum)              -- perturbs the glucose homeostat (s5/s6) on TWO axes
        * T1 axis  : beta-cell secretory CAPACITY (Smax_i * beta_frac) depletes -> fasting glucose rises
          ACCELERATINGLY past the cited 7 mM diabetes threshold; meal loads stop returning to setpoint. [V]/[L]
        * T2 axis  : insulin SENSITIVITY (k_u * sens) falls -> the fixed point drifts to a STABLE ELEVATED
          setpoint (insulin resistance), saturating; return is preserved. [V]/[L]
        * IGT      : a mild point on the T2 axis (fasting 5.6-6.9 mM, the cited pre-diabetes band). [V]/[L]
        One loop, two failure modes: capacity loss is catastrophic (accelerating), gain loss is graceful.

  D3  Gastritis + peptic ulcer              -- reuses the s7 / s10 exact-barrier Kramers kernel
        * erosion  : aggression (acid / NSAID) is a bias h lowering the mucosal-integrity barrier ->
          erosion crossing RR rises monotone + convex (same Kramers form as s7); slope calibrated to a
          cited NSAID ulcer RR. [L] anchor / [V] shape
        * ulcer site split : gastric ulcer = DEFENCE failure (low barrier scale g, moderate acid) vs
          duodenal ulcer = ACID excess (normal g, high h) -- both cross to the ulcer basin by distinct
          routes (the textbook site split). [V]
        * continuum : the SAME g_Hp that s10 uses for the cancer step is the barrier scale chronic
          H. pylori gastritis lowers -> one kernel spans inflammation -> erosion -> ulcer -> the first
          step of the neoplasia sequence. [V] mechanism / [O] absolute incidence

DETERMINISM (C1): no RNG; noise-free integrations; BLAS pinned by the engine import; round-before-hash;
sorted keys. digest() emits a canonical JSON + sha256 so the disease layer is 2x-sha256 reproducible.
"""
import os, sys, math, json, hashlib
from functools import lru_cache
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_oncology"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import importlib
eng  = importlib.import_module("vp_dig_engine")
onco = importlib.import_module("carcinogen_dose_response")
from vp_substrate import (spinodal, barrier, gate_open, gate_resistance, settle, is_on,
                          wall_stiffness, reservoir_compliance, meal_pressure, sdot,
                          afferent_gain, afferent_signal,
                          flare_state, flare_burden, inflammatory_barrier_scale,
                          autoactivation_threshold, autodigestion_latched,
                          perfusion_threshold, viability_margin, tissue_viable,
                          nucleation_barrier, supersaturation_drive, stone_nucleates,
                          laplace_pressure, herniation_threshold, wall_herniates)

# ===========================================================================
#  D1  GASTRIC DYSRHYTHMIA + GASTROPARESIS   (perturbs s2 pacemaker / s3 chain)
# ===========================================================================
# Cited electrogastrography band (the normal antral slow wave and its dysrhythmia thresholds):
EGG_NORMAL_LO = 2.5     # cpm  [L]
EGG_NORMAL_HI = 3.7     # cpm  [L]

def gastric_cpm(tau_s, drive=0.55):
    """Recorded gastric slow-wave rate (cpm) at FHN recovery constant tau_s, via the s2 gastric clock."""
    return float(eng.K_TIME * eng.fhn_freq(float(tau_s), drive))

def classify_rhythm(cpm):
    if cpm < EGG_NORMAL_LO: return "bradygastria"
    if cpm > EGG_NORMAL_HI: return "tachygastria"
    return "normal"

def dysrhythmia_map():
    """Sweep the pacemaker rate parameter tau_s; the recorded rate crosses the cited EGG band
    monotonically: long tau_s -> bradygastria, the s2 anchor -> normal, short tau_s -> tachygastria."""
    rows = []
    for tau_s in [240.0, 300.0, 380.0, 520.0, 760.0]:
        cpm = gastric_cpm(tau_s)
        rows.append((float(tau_s), round(cpm, 3), classify_rhythm(cpm)))
    cpms = [r[1] for r in rows]
    monotone = all(cpms[i] >= cpms[i + 1] - 1e-9 for i in range(len(cpms) - 1))  # rate falls as tau_s grows
    spans = {c for _, _, c in rows}
    return dict(rows=rows, monotone_in_tau=monotone,
                spans_brady_normal_tachy=spans == {"bradygastria", "normal", "tachygastria"})

def _entrained_cpm(tau_prox, tau_dist, coupling, T=20000.0, dt=0.2):
    """Two weakly (Kuramoto) coupled slow-wave oscillators -- the SAME phase-coupling reduction the s4
    peristalsis module uses -- with intrinsic rates from the real FHN. Returns the proximal RECORDED
    rate (cpm). A faster distal focus that couples in entrains the antral recording upward.
    (dt=0.2 is ample for this smooth phase ODE; the brady/normal/tachy classification is dt-invariant.)"""
    wp = 2.0 * math.pi * eng.fhn_freq(float(tau_prox))
    wd = 2.0 * math.pi * eng.fhn_freq(float(tau_dist))
    thp, thd = 0.0, 0.3
    n = int(T / dt); ups = 0; last = False
    for _ in range(n):
        thp += dt * (wp + coupling * math.sin(thd - thp))
        thd += dt * (wd + coupling * math.sin(thp - thd))
        on = math.cos(thp) > 0.0
        if on and not last: ups += 1
        last = on
    return float(eng.K_TIME * (ups / T))

def ectopic_entrainment():
    """Tachygastria mechanism: a normal distal focus leaves the antral recording in the normal band,
    but a FASTER distal ectopic focus with sufficient coupling entrains it above the tachy threshold."""
    base       = _entrained_cpm(380.0, 380.0, 0.0)
    normal_cpl = _entrained_cpm(380.0, 380.0, 0.010)    # normal focus + coupling -> no upshift
    fast_uncpl = _entrained_cpm(380.0, 110.0, 0.000)    # faster focus, NOT coupled -> antrum unaffected
    fast_cpl   = _entrained_cpm(380.0, 110.0, 0.010)    # faster focus + coupling -> entrains up (tachy)
    return dict(base_cpm=round(base, 3), normal_focus_coupled_cpm=round(normal_cpl, 3),
                fast_focus_uncoupled_cpm=round(fast_uncpl, 3), fast_focus_coupled_cpm=round(fast_cpl, 3),
                tachy_only_when_faster_and_coupled=bool(
                    fast_cpl > EGG_NORMAL_HI and normal_cpl <= EGG_NORMAL_HI and fast_uncpl <= EGG_NORMAL_HI))

def gastroparesis_emptying(rho, N=16, coupling=0.06, Tt=600.0, dt=0.05, Dtrans=0.25, wwin=0.5):
    """Gastric emptying RATE proxy: the centre-of-mass displacement of an antral bolus in a FIXED
    window (a scintigraphy-style rate). ICC pacemaker density rho scales the contraction (occlusion)
    amplitude -- diffuse ICC loss makes every contraction weaker, so the bolus advances more slowly
    (delayed emptying). Built on the validated s4 transport mechanics; rho is the only change."""
    taus = np.linspace(eng.TAU_DUO, eng.TAU_DUO * 1.2, N)
    omega = 2.0 * math.pi * np.array([eng.fhn_freq(float(t)) for t in taus])
    theta = np.linspace(0.0, 0.4, N)
    c = np.zeros(N); c[1:4] = 1.0; pos = np.arange(N); com0 = (c * pos).sum() / c.sum()
    for _ in range(int(Tt / dt)):
        dth = omega.copy()
        dth[:-1] += coupling * np.sin(theta[1:] - theta[:-1])
        dth[1:]  += coupling * np.sin(theta[:-1] - theta[1:])
        theta = theta + dt * dth
        a = rho * (np.cos(theta) > math.cos(wwin)).astype(float)     # density-scaled occlusion amplitude
        fwd = Dtrans * np.maximum(a[:-1] - a[1:], 0.0) * c[:-1]
        bwd = Dtrans * np.maximum(a[1:] - a[:-1], 0.0) * c[1:]
        c[:-1] -= fwd; c[1:] += fwd
        c[1:]  -= bwd; c[:-1] += bwd
    return float((c * pos).sum() / c.sum() - com0)

def gastroparesis_curve():
    e_norm = gastroparesis_emptying(1.0)
    rows = [(round(r, 2), round(gastroparesis_emptying(r), 4),
             round(gastroparesis_emptying(r) / e_norm * 100.0, 1))
            for r in [1.0, 0.8, 0.6, 0.4, 0.3, 0.2, 0.1, 0.0]]
    rates = [v for _, v, _ in rows]
    monotone = all(rates[i] >= rates[i + 1] - 1e-6 for i in range(len(rates) - 1))
    severe_pct = rows[-2][2]                              # rho = 0.1
    collapses = abs(rows[-1][1]) < 1e-6                   # rho = 0 -> no emptying
    return dict(normal_displacement=round(e_norm, 3), rows=rows,
                monotone_in_density=monotone, severe_depletion_pct_of_normal=severe_pct,
                no_emptying_at_zero_density=collapses)

@lru_cache(maxsize=1)
def validate_d1():
    dm = dysrhythmia_map(); ee = ectopic_entrainment(); gp = gastroparesis_curve()
    # robustness of emptying monotonicity across coupling x flux scale
    rob = True
    for cp in [0.04, 0.06, 0.09]:
        for Dt in [0.20, 0.25, 0.30]:
            s = [gastroparesis_emptying(r, coupling=cp, Dtrans=Dt) for r in [1.0, 0.3, 0.1]]
            if not (s[0] >= s[1] >= s[2] and s[0] > 0 and s[2] < 0.6 * s[0]): rob = False
    passed = bool(dm["monotone_in_tau"] and dm["spans_brady_normal_tachy"] and
                  ee["tachy_only_when_faster_and_coupled"] and
                  gp["monotone_in_density"] and gp["no_emptying_at_zero_density"] and
                  gp["severe_depletion_pct_of_normal"] < 50.0 and rob)
    return dict(dysrhythmia=dm, ectopic=ee, gastroparesis=gp, emptying_robust=rob, passed=passed,
                grades="rhythm band [L] / dysrhythmia + entrainment + emptying mechanism [V] / absolute emptying rate [O]")

# ===========================================================================
#  D2  DIABETES (T1/T2 spectrum)            (perturbs the s5/s6 glucose homeostat)
# ===========================================================================
# Cited ADA fasting plasma glucose thresholds (mM):
FPG_NORMAL_HI = 5.6     # < 5.6 normal  [L]
FPG_DIABETES  = 7.0     # >= 7.0 diabetes (126 mg/dL)  [L]   (5.6-6.9 = impaired fasting glucose / pre-diabetes)

def _homeostat_disease(beta_frac=1.0, sens=1.0, T=160.0):
    """Disease parametrisation of the validated homeostat: beta_frac scales beta-cell secretory
    CAPACITY (Smax_i); sens scales insulin SENSITIVITY (k_u). Returns the fasting fixed point plus a
    post-load probe (peak + final) under a standard meal."""
    Pp = dict(eng.HOMEOSTAT_P)
    Pp["Smax_i"] = eng.HOMEOSTAT_P["Smax_i"] * beta_frac
    Pp["k_u"]    = eng.HOMEOSTAT_P["k_u"]    * sens
    _, Gf = eng.glucose_homeostat(G0=5.0, T=T, Pp=Pp); fast = float(Gf[-1])
    _, Gm = eng.glucose_homeostat(G0=fast, meal=eng._pulse(3.0), T=60.0, Pp=Pp)
    return fast, float(Gm.max()), float(Gm[-1])

def classify_fpg(f):
    if f < FPG_NORMAL_HI: return "normal"
    if f >= FPG_DIABETES: return "diabetes"
    return "impaired (pre-diabetes)"

# matched depth grid for the two homeostat axes (even spacing so the comparison is fair)
_DEPTHS = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1]

def t1_axis():
    """beta-cell CAPACITY depletion (T1, insulin-dependent). Fasting glucose rises into SEVERE
    hyperglycaemia, crossing the cited diabetes threshold and running away as capacity -> 0; meal loads
    no longer return to a normal setpoint -- the catastrophic failure mode."""
    rows = []
    for b in _DEPTHS:
        f, pk, fin = _homeostat_disease(beta_frac=b)
        rows.append((round(b, 2), round(f, 2), round(pk, 2), round(fin, 2), classify_fpg(f)))
    fasts = [r[1] for r in rows]
    monotone = all(fasts[i] <= fasts[i + 1] + 1e-9 for i in range(len(fasts) - 1))   # rises as capacity falls
    crosses_diabetes = any(f >= FPG_DIABETES for f in fasts)
    severe = fasts[-1] > 10.0                                                          # deep depletion -> severe
    return dict(rows=rows, monotone_rise=monotone, crosses_diabetes_threshold=crosses_diabetes,
                severe_at_deep_depletion=severe, deepest_fasting=fasts[-1])

def t2_axis():
    """insulin SENSITIVITY loss (T2 / insulin resistance). Fasting drifts to an ELEVATED but STABLE
    setpoint and the meal still returns to it; the rise stays comparatively MILD across the sweep --
    the compensated failure mode (a raised fixed point, not a runaway)."""
    rows = []
    for s in _DEPTHS:
        f, pk, fin = _homeostat_disease(sens=s)
        returns = abs(fin - f) < 0.25                        # settles back to the (elevated) fixed point
        rows.append((round(s, 2), round(f, 2), round(pk, 2), round(fin, 2), classify_fpg(f), bool(returns)))
    fasts = [r[1] for r in rows]
    monotone = all(fasts[i] <= fasts[i + 1] + 1e-9 for i in range(len(fasts) - 1))
    sub_severe = fasts[-1] < 8.0                             # stays compensated even at deep resistance
    all_return = all(r[5] for r in rows)
    return dict(rows=rows, monotone_rise=monotone, sub_severe_across_sweep=sub_severe,
                return_preserved=all_return, deepest_fasting=fasts[-1])

def igt_point():
    """Impaired glucose tolerance = a mild point on the T2 axis: fasting in the cited 5.6-6.9 band."""
    f, pk, fin = _homeostat_disease(sens=0.5)
    return dict(sens=0.5, fasting_mM=round(f, 2), classification=classify_fpg(f),
                in_pre_diabetes_band=bool(FPG_NORMAL_HI <= f < FPG_DIABETES))

@lru_cache(maxsize=1)
def validate_d2():
    t1 = t1_axis(); t2 = t2_axis(); ig = igt_point()
    # the two axes are mechanistically distinct: at MATCHED depletion depth, capacity loss (T1) is always
    # >= sensitivity loss (T2) in fasting glucose, and the gap WIDENS with depth -- capacity depletion is
    # catastrophic (severe, runaway), sensitivity loss is compensated (milder, stable elevated setpoint).
    gaps = [t1["rows"][i][1] - t2["rows"][i][1] for i in range(len(_DEPTHS))]
    gap_widens = all(gaps[i + 1] >= gaps[i] - 1e-6 for i in range(len(gaps) - 1)) and gaps[-1] > gaps[0]
    capacity_worse = all(g >= -1e-9 for g in gaps)
    distinct = bool(capacity_worse and gap_widens and
                    t1["severe_at_deep_depletion"] and t1["crosses_diabetes_threshold"] and
                    t2["sub_severe_across_sweep"] and t2["return_preserved"])
    passed = bool(t1["monotone_rise"] and t2["monotone_rise"] and distinct and ig["in_pre_diabetes_band"])
    return dict(t1_capacity=t1, t2_sensitivity=t2, igt=ig, matched_depth_gap=[round(g, 2) for g in gaps],
                axes_distinct=distinct, passed=passed,
                grades="FPG thresholds [L] / two-axis emergence [V] / absolute prevalence [O]")

# ===========================================================================
#  D3  GASTRITIS + PEPTIC ULCER             (reuses the s7 / s10 barrier-Kramers kernel)
# ===========================================================================
D_NOISE = onco.D_NOISE                                       # ONE shared substrate noise scale (s7)

def RR_erosion(g, h):
    """Mucosal-erosion crossing RR vs an intact baseline (g=1, h=0): aggression h lowers the integrity
    barrier; the SAME exact Kramers kernel as the s7 carcinogen module (cell-fate -> mucosal-integrity)."""
    return onco.crossing_rate(g, h, D_NOISE) / onco.crossing_rate(1.0, 0.0, D_NOISE)

NSAID_ULCER_RR = 4.0    # [L] cited peptic-ulcer relative risk for NSAID exposure (reference aggression = 1.0)

def _calib_aggression(dose_ref=1.0, RR_ref=NSAID_ULCER_RR, g=1.0):
    """Calibrate the aggression dose -> bias slope kappa to ONE cited ulcer RR (no shape tuning)."""
    lo, hi = 1e-6, spinodal(g) / dose_ref * 0.999
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if RR_erosion(g, mid * dose_ref) < RR_ref: lo = mid
        else: hi = mid
    return (lo + hi) / 2.0

def erosion_dose_response():
    """Acute gastritis: erosion RR vs aggression (acid / NSAID) dose, anchored to the cited NSAID ulcer
    RR; the curve shape (monotone + convex) is forced by the same barrier kernel as s7."""
    k = _calib_aggression()
    doses = [0.0, 0.5, 1.0, 1.5, 2.0]
    curve = [(float(d), round(RR_erosion(1.0, k * d), 3)) for d in doses]
    rr = [v for _, v in curve]
    monotone = all(rr[i + 1] > rr[i] for i in range(len(rr) - 1))
    convex = all(rr[i + 2] - rr[i + 1] >= rr[i + 1] - rr[i] - 1e-6 for i in range(len(rr) - 2))
    anchor_hit = abs(dict(curve)[1.0] - NSAID_ULCER_RR) < 0.02
    return dict(kappa=round(k, 6), curve=curve, monotone=monotone, convex=convex, anchor_hit=anchor_hit)

def ulcer_site_split():
    """Peptic-ulcer site split on the SAME barrier: a GASTRIC ulcer crosses by DEFENCE failure (a low
    barrier scale g at moderate acid h); a DUODENAL ulcer crosses by ACID excess (normal g, high h).
    Both reach a high crossing rate through mechanistically distinct corners of the (g, h) plane."""
    g_gastric, h_gastric = 0.7, 0.10        # impaired mucosal defence + moderate acid
    g_duodenal, h_duodenal = 1.0, 0.22      # intact defence + high acid load
    rr_g = RR_erosion(g_gastric, h_gastric)
    rr_d = RR_erosion(g_duodenal, h_duodenal)
    thr = 10.0                              # "ulcer-crossing" threshold (well above intact baseline)
    return dict(gastric=dict(g=g_gastric, h=h_gastric, RR=round(rr_g, 2), route="defence failure (low g)"),
                duodenal=dict(g=g_duodenal, h=h_duodenal, RR=round(rr_d, 2), route="acid excess (high h)"),
                both_cross=bool(rr_g > thr and rr_d > thr),
                distinct_routes=bool(g_gastric < 1.0 and h_duodenal > h_gastric))

def gastritis_continuum():
    """Chronic H. pylori gastritis lowers the SAME barrier scale g_Hp that the s10 cancer step uses,
    so one kernel spans inflammation -> erosion -> the first neoplasia step (the inflammation-to-
    neoplasia continuum on a single barrier axis)."""
    v = onco.validate(); g_Hp = v["gastric"]["g_Hp"]
    rr_chronic = RR_erosion(g_Hp, 0.0)                       # baseline erosion lift from chronic Hp alone
    return dict(g_Hp_shared_with_s10=g_Hp, chronic_gastritis_baseline_RR=round(rr_chronic, 3),
                same_g_as_cancer_step=True)

@lru_cache(maxsize=1)
def validate_d3():
    er = erosion_dose_response(); ss = ulcer_site_split(); ct = gastritis_continuum()
    passed = bool(er["monotone"] and er["convex"] and er["anchor_hit"] and
                  ss["both_cross"] and ss["distinct_routes"] and ct["same_g_as_cancer_step"])
    return dict(erosion=er, ulcer_site_split=ss, continuum=ct, shared_noise_scale_D=round(D_NOISE, 6),
                passed=passed,
                grades="NSAID ulcer anchor [L] / erosion shape + site split + continuum [V] / absolute incidence [O]")

# ===========================================================================
#  D4  INTESTINAL MOTILITY / PROPULSION DISORDERS  (perturbs s4 peristalsis)
# ===========================================================================
# All four reuse the validated s4 travelling-wave transporter; the disease knobs are propulsive drive
# (the aboral frequency-gradient spread), ICC pacemaker density (the SAME lesion as s11 gastroparesis),
# and a transient drive gate. Net aboral centre-of-mass displacement in a FIXED window is the transit-rate
# proxy (cf. a colonic-transit study). Treatment = the model's reading of which parameter an effective
# therapy must move, in which direction, and the regime where it works (a mechanistic prediction; absolute
# efficacy is [O], needing trials).

def gut_transport(gradient_drive=1.0, coupling=0.05, icc_density=1.0, drive_gate=None,
                  N=16, Tt=300.0, dt=0.05, Dtrans=0.20, wwin=0.5, return_state=False):
    """Generalised aboral transport on the validated s4 mechanics. gradient_drive scales the aboral
    tau_s spread (propulsive directional drive); icc_density scales contraction amplitude (ICC lesion,
    shared with s11); drive_gate(t)->bool transiently switches the slow-wave drive off (ileus).
    return_state=True additionally exposes the final luminal profile (c, pos, com0) WITHOUT changing
    the default return path -- used by the SIBO stasis reader to measure a retained proximal fraction."""
    taus = np.linspace(eng.TAU_DUO, eng.TAU_ILE, N)
    mean = taus.mean()
    taus = mean + gradient_drive * (taus - mean)             # flatten the gradient as drive -> 0
    omega0 = 2.0 * math.pi * np.array([eng.fhn_freq(float(t)) for t in taus])
    theta = np.linspace(0.0, 0.4, N)
    c = np.zeros(N); c[1:4] = 1.0; pos = np.arange(N); com0 = (c * pos).sum() / c.sum()
    t = 0.0
    for _ in range(int(Tt / dt)):
        g = 1.0 if (drive_gate is None or drive_gate(t)) else 0.0
        dth = g * omega0.copy()
        dth[:-1] += coupling * np.sin(theta[1:] - theta[:-1])
        dth[1:]  += coupling * np.sin(theta[:-1] - theta[1:])
        theta = theta + dt * dth
        a = icc_density * (np.cos(theta) > math.cos(wwin)).astype(float)
        fwd = Dtrans * np.maximum(a[:-1] - a[1:], 0.0) * c[:-1]
        bwd = Dtrans * np.maximum(a[1:] - a[:-1], 0.0) * c[1:]
        c[:-1] -= fwd; c[1:] += fwd
        c[1:]  -= bwd; c[:-1] += bwd
        t += dt
    disp = float((c * pos).sum() / c.sum() - com0)
    if return_state:
        return disp, c, pos, com0
    return disp

def _off_window(lo_dur, t0=60.0):
    return lambda t: not (t0 <= t < t0 + lo_dur)

def propulsive_drive_axis():
    """Slow-transit constipation and colonic inertia are one axis at two severities: reducing the
    propulsive drive slows transit monotonically (slow-transit, responsive), and below a threshold
    transport COLLAPSES to near-zero (colonic inertia, refractory)."""
    norm = gut_transport()
    rows = [(round(d, 2), round(gut_transport(gradient_drive=d) / norm * 100.0, 1)) for d in
            [1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1]]
    pct = [p for _, p in rows]
    graded_monotone = all(pct[i] >= pct[i + 1] - 2.0 for i in range(len(pct) - 1))
    inertia_collapse = pct[-1] < 20.0 and rows[3][1] > 40.0       # 0.4 graded, 0.1 collapsed
    return dict(rows=rows, graded_monotone=graded_monotone, inertia_collapse_below_threshold=inertia_collapse,
                slow_transit_regime="drive 0.3-1.0 (graded, transit prolonged)",
                colonic_inertia_regime="drive < ~0.3 (collapsed, refractory)",
                treatment=("slow-transit: prokinetics RAISE propulsive drive -> restore transit (works in the "
                           "graded regime); colonic inertia: below the threshold a modest drive boost stays "
                           "sub-threshold, so it is refractory to prokinetics -> subtotal colectomy is the "
                           "model-consistent escalation. The threshold itself is the falsifiable prediction."))

def cipo_curve():
    """Chronic intestinal pseudo-obstruction = ICC pacemaker density falls -> propulsion fails while the
    lumen stays patent (functional, NOT mechanical, obstruction). Same ICC lesion as s11 gastroparesis."""
    norm = gut_transport()
    rows = [(round(r, 2), round(gut_transport(icc_density=r) / norm * 100.0, 1)) for r in
            [1.0, 0.6, 0.4, 0.2, 0.1]]
    pct = [p for _, p in rows]
    monotone = all(pct[i] >= pct[i + 1] - 2.0 for i in range(len(pct) - 1))
    functional_obstruction = pct[-1] < 40.0
    return dict(rows=rows, monotone=monotone, functional_obstruction_lumen_patent=functional_obstruction,
                treatment=("efficacy tracks RESIDUAL ICC density: prokinetics help only while enough pacemaker "
                           "substrate remains; with severe depletion it is refractory -> decompression and "
                           "nutritional support. No mechanical target exists (the lumen is patent)."))

def ileus_reversibility():
    """Paralytic ileus = transient global loss of slow-wave drive -> propulsion stops, then RECOVERS when
    drive returns. The deficit scales with the duration of the loss; permanent loss = no propulsion."""
    Tt = 540.0; norm = gut_transport(Tt=Tt)
    rows = [(off, round(gut_transport(Tt=Tt, drive_gate=_off_window(off)) / norm * 100.0, 1)) for off in
            [0, 150, 300, 450]]
    never_on = round(gut_transport(Tt=Tt, drive_gate=lambda t: False) / norm * 100.0, 1)
    pct = [p for _, p in rows]
    reversible = rows[1][1] > never_on + 5.0 and pct[1] >= pct[2] >= pct[3] - 2.0
    return dict(rows=rows, never_on_pct=never_on, reversible_scales_with_duration=reversible,
                treatment=("REMOVE the transient suppressant (opioids, post-operative inflammation, "
                           "electrolyte derangement) -> drive returns -> spontaneous recovery. The model's "
                           "reversibility is exactly why ileus is managed by removing the cause and waiting, "
                           "unlike colonic inertia (a fixed sub-threshold collapse)."))

def icc_unifying_lesion():
    """Cross-disease unifying hypothesis #1: ONE ICC-density lesion, MANY sites. The same density parameter
    collapses gastric emptying (s11, stomach) AND aboral transit (s14, gut) monotonically -- one cause
    (ICC depletion) behind gastroparesis + slow-transit/CIPO."""
    e_norm = gastroparesis_emptying(1.0); t_norm = gut_transport()
    rows = []
    for r in [1.0, 0.6, 0.4, 0.2, 0.1]:
        st = gastroparesis_emptying(r) / e_norm * 100.0
        gt = gut_transport(icc_density=r) / t_norm * 100.0
        rows.append((round(r, 2), round(st, 1), round(gt, 1)))
    stom = [s for _, s, _ in rows]; gut = [g for _, _, g in rows]
    both_collapse = (all(stom[i] >= stom[i + 1] - 2.0 for i in range(len(stom) - 1)) and stom[-1] < 50.0 and
                     all(gut[i] >= gut[i + 1] - 2.0 for i in range(len(gut) - 1)) and gut[-1] < 50.0)
    return dict(density_axis=rows, both_sites_collapse_monotonically=both_collapse,
                columns="(icc_density, stomach_emptying_%_of_normal, gut_transit_%_of_normal)")

@lru_cache(maxsize=1)
def validate_d4():
    pa = propulsive_drive_axis(); ci = cipo_curve(); il = ileus_reversibility(); un = icc_unifying_lesion()
    passed = bool(pa["graded_monotone"] and pa["inertia_collapse_below_threshold"] and
                  ci["monotone"] and ci["functional_obstruction_lumen_patent"] and
                  il["reversible_scales_with_duration"] and un["both_sites_collapse_monotonically"])
    return dict(slow_transit_and_inertia=pa, cipo=ci, ileus=il, icc_unifying=un, passed=passed,
                grades="transit mechanisms [V] / clinical transit anchors [L-pending] / absolute transit time [O]")
# ===========================================================================
#  D5  ADDITIONAL TIER-1 PERTURBATIONS  (group A: in-substrate, NO new primitive)
# ===========================================================================
# Five scattered Tier-1 phenotypes that reuse already-validated modules. Each moves ONE parameter (or
# reads one validated module on a new switch) and the phenotype emerges -- never fitted. Where the
# substrate genuinely cannot express a feature without a new primitive, that piece is recorded as an
# honest [O] with the obstacle stated and deferred to the named Tier-2 element (group B) -- the
# No-Tuning discipline forbids manufacturing the missing effect.
#
#   D5a  Dumping syndrome           -- mirror of s11 gastroparesis / s14 slow-transit (rapid side) + s5
#   D5b  Reflux esophagitis         -- the s7/s13 barrier-Kramers kernel on the oesophageal mucosa
#   D5c  Insulinoma / reactive hypo -- mirror of s12 type-1 capacity loss (an autonomous insulin source)
#   D5d  Functional dyspepsia (mot) -- a MILD point on the s11 ICC/amplitude axis (mild emptying delay)
#   D5e  SIBO (motility part)       -- stasis from low propulsive drive on the s4 transporter

HYPO_THRESHOLD = 3.9    # mM  [L] cited clinical hypoglycaemia alert value (70 mg/dL, ADA)

def _meal(load, t0=2.0, dur=2.0):
    """A meal delivering a FIXED total glucose `load` over duration `dur` (rate = load/dur). Rapid
    gastric emptying = short dur (a sharp tall pulse); normal emptying = a broad pulse. Load conserved."""
    amp = load / dur
    return lambda t: amp if (t0 <= t < t0 + dur) else 0.0

def _ins_window(amp, t0, dur=4.0):
    """A sustained/again-windowed exogenous-or-autonomous insulin drive (reuses the validated
    ins_kick channel that T5 exercises)."""
    return lambda t: amp if (t0 <= t < t0 + dur) else 0.0

# --------------------------------------------------------------------------- D5a  Dumping
def dumping_mechanical():
    """The MECHANICAL rapid-emptying claim, tested honestly on the validated s4/s14 transporter. The
    conserved-bolus transporter expresses SLOWING cleanly (the s11/s14 direction) but SATURATES on the
    rapid side: at normal gain the travelling wave already moves the geometry-limited maximum per pass,
    so raising the emptying gate / propulsive drive cannot overshoot normal. This is an honest negative
    for the pure in-substrate rapid-emptying magnitude -- the true dumping lesion is loss of the gastric
    accommodation reservoir / pyloric brake, a Tier-2 element (group B). Direction [V]; magnitude [O]."""
    norm = gut_transport()                                   # normal aboral transport (default window)
    slow = gut_transport(gradient_drive=0.5)                 # reduced drive -> slower (s14 side)
    rapid = gut_transport(gradient_drive=2.5, Dtrans=0.50)   # raised drive+gate -> rapid side
    slow_reduces = slow < norm - 1e-6
    overshoot_pct = (rapid - norm) / norm * 100.0
    rapid_saturates = overshoot_pct < 5.0                    # rapid side cannot exceed normal (ceiling)
    return dict(normal_disp=round(norm, 4), slow_side_disp=round(slow, 4),
                rapid_side_disp=round(rapid, 4), rapid_overshoot_pct=round(overshoot_pct, 3),
                slow_side_reduces=bool(slow_reduces), rapid_side_saturates=bool(rapid_saturates),
                grade="[O] mechanical magnitude (substrate saturates; reservoir = Tier-2/group B)")

def dumping_early_curve():
    """EARLY dumping (post-prandial hyperglycaemia): the same glucose LOAD delivered FASTER (a sharper
    pulse = rapid gastric emptying) drives a monotonically higher glucose peak on the validated s5 loop.
    The total load is conserved across the sweep, so the rising peak is a delivery-RATE effect [V]."""
    LOAD = 6.0
    rows = []
    for dur in [6.0, 4.0, 3.0, 2.0, 1.5, 1.0]:
        _, G = eng.glucose_homeostat(G0=5.0, meal=_meal(LOAD, dur=dur), T=45.0)
        rows.append((round(dur, 2), round(float(np.max(G)), 3)))
    peaks = [p for _, p in rows]
    peak_rises = all(peaks[i] <= peaks[i + 1] + 1e-9 for i in range(len(peaks) - 1))
    return dict(load=LOAD, rows=rows, peak_rises_with_emptying_speed=bool(peak_rises),
                fastest_peak_mM=peaks[-1])

def dumping_late_curve():
    """LATE dumping (reactive hypoglycaemia): rapid delivery PLUS an exaggerated incretin-driven insulin
    response (the s12/s5 secretion arm over-firing after the sharp glucose surge) -> a BIPHASIC excursion:
    a high peak followed by a reactive undershoot that DEEPENS as delivery speeds up, crossing the cited
    hypoglycaemia threshold at fast delivery. The insulin-response gain is one model parameter; the
    falsifiable, emergent claim is the biphasic DIRECTION (faster delivery -> higher peak AND deeper
    nadir). Absolute nadir is [O] (uncalibrated incretin gain); the biphasic mechanism is [V]."""
    LOAD = 6.0; GAIN = 2.4
    rows = []
    for dur in [6.0, 4.0, 3.0, 2.0, 1.5, 1.0]:
        insamp = GAIN * (2.0 / dur)                          # incretin surge tracks delivery sharpness
        _, G = eng.glucose_homeostat(G0=5.0, meal=_meal(LOAD, dur=dur),
                                     ins_kick=_ins_window(insamp, t0=2.0 + dur, dur=4.0), T=50.0)
        G = np.asarray(G); ip = int(np.argmax(G))
        rows.append((round(dur, 2), round(float(G.max()), 3), round(float(G[ip:].min()), 3)))
    peaks = [p for _, p, _ in rows]; nadirs = [n for _, _, n in rows]
    peak_rises = all(peaks[i] <= peaks[i + 1] + 1e-9 for i in range(len(peaks) - 1))
    nadir_deepens = all(nadirs[i] >= nadirs[i + 1] - 1e-9 for i in range(len(nadirs) - 1))
    crosses_hypo = nadirs[-1] < HYPO_THRESHOLD
    return dict(load=LOAD, insulin_gain=GAIN, rows=rows,
                peak_rises=bool(peak_rises), reactive_nadir_deepens=bool(nadir_deepens),
                fast_delivery_crosses_hypo=bool(crosses_hypo), biphasic=bool(peak_rises and nadir_deepens))

@lru_cache(maxsize=1)
def validate_d5a():
    mech = dumping_mechanical(); ec = dumping_early_curve(); lc = dumping_late_curve()
    passed = bool(mech["slow_side_reduces"] and mech["rapid_side_saturates"] and
                  ec["peak_rises_with_emptying_speed"] and lc["biphasic"] and
                  lc["fast_delivery_crosses_hypo"])
    return dict(mechanical=mech, early_dumping=ec, late_dumping=lc, passed=passed,
                treatment=("slow gastric emptying and carbohydrate delivery -- the INVERSE of the s11/s14 "
                           "prokinetic target: smaller, more frequent, lower-glycaemic meals broaden the "
                           "delivery pulse and flatten the peak; surgically, restoring the reservoir / "
                           "pyloric brake is the mechanical target (Tier-2/group B). Direction [V]; "
                           "absolute efficacy [O]."),
                grades="early/late metabolic mechanism [V] / hypo threshold [L] / mechanical magnitude + absolute nadir [O]")

# --------------------------------------------------------------------------- D5b  Reflux esophagitis
def reflux_erosion():
    """Reflux oesophagitis (the mucosal-injury part): oesophageal acid exposure is a sustained bias h
    that lowers the mucosal-integrity barrier -- the IDENTICAL exact-barrier Kramers kernel as s13, read
    on the oesophageal mucosa. Erosion RR rises monotone + convex in acid-exposure dose, with the SAME
    calibrated slope as the s13 gastritis curve (no new anchor, no shape fit). The reflux SOURCE (LES
    incompetence) is the Tier-2 sphincter gate (group B); this section owns only the acid-injury crossing."""
    k = _calib_aggression()                                  # reuse the s13 NSAID-anchored slope
    doses = [0.0, 0.5, 1.0, 1.5, 2.0]
    curve = [(float(d), round(RR_erosion(1.0, k * d), 3)) for d in doses]
    rr = [v for _, v in curve]
    monotone = all(rr[i + 1] > rr[i] for i in range(len(rr) - 1))
    convex = all(rr[i + 2] - rr[i + 1] >= rr[i + 1] - rr[i] - 1e-6 for i in range(len(rr) - 2))
    return dict(kappa_shared_with_s13=round(k, 6), curve=curve, monotone=monotone, convex=convex,
                treatment=("lower the acid-exposure bias h -- acid suppression (proton-pump inhibitors) "
                           "moves the system back DOWN the convex erosion curve; eliminating the reflux "
                           "SOURCE needs the Tier-2 lower-oesophageal-sphincter gate (group B). The "
                           "target direction is forced [V]; absolute efficacy [O]."),
                grades="erosion shape (shared s13 kernel) [V] / NSAID-anchored slope [L] / absolute incidence [O]")

@lru_cache(maxsize=1)
def validate_d5b():
    er = reflux_erosion()
    passed = bool(er["monotone"] and er["convex"])
    return dict(erosion=er, passed=passed, grades=er["grades"])

# --------------------------------------------------------------------------- D5c  Insulinoma / reactive hypo
def insulinoma_axis():
    """Insulinoma: an AUTONOMOUS, unregulated insulin source (a constant insulin drive on the validated
    s5 loop) pulls the fasting fixed point BELOW the 5 mM setpoint and below the cited hypoglycaemia
    threshold, deepening monotonically with the source strength -- the exact MIRROR of s12 type-1
    capacity loss (there a missing insulin arm raised glucose past 7 mM; here an excess insulin source
    lowers it past 3.9 mM). Removing the source returns the loop to setpoint (the resection prediction)."""
    rows = []
    for A in [0.0, 1.0, 2.0, 4.0, 6.0, 8.0, 12.0]:
        _, G = eng.glucose_homeostat(G0=5.0, ins_kick=_ins_window(A, t0=0.0, dur=1e9), T=160.0)
        rows.append((round(A, 2), round(float(G[-1]), 3)))
    fasts = [f for _, f in rows]
    monotone_falls = all(fasts[i] >= fasts[i + 1] - 1e-9 for i in range(len(fasts) - 1))
    crosses_hypo = any(f < HYPO_THRESHOLD for f in fasts)
    # resection: with the source removed, a hypoglycaemic patient returns to setpoint
    _, Gr = eng.glucose_homeostat(G0=3.0, T=120.0); recovers = abs(float(Gr[-1]) - eng.G_SET) < 0.4
    return dict(rows=rows, fasting_monotone_falls=bool(monotone_falls),
                crosses_hypo_threshold=bool(crosses_hypo), deepest_fasting=fasts[-1],
                recovery_on_source_removal_mM=round(float(Gr[-1]), 3), recovers_on_resection=bool(recovers))

def reactive_hypo_curve():
    """Reactive (post-prandial) hypoglycaemia: a meal followed by an exaggerated/delayed insulin response
    drives a reactive undershoot below baseline that deepens with the insulin overshoot -- the shared
    s5 mechanism behind LATE dumping. Distinct aetiology, same loop signature."""
    rows = []
    for spike in [0.0, 1.0, 2.0, 3.0, 4.0]:
        _, G = eng.glucose_homeostat(G0=5.0, meal=_meal(3.0, dur=2.0),
                                     ins_kick=_ins_window(spike, t0=3.0, dur=3.0), T=40.0)
        rows.append((round(spike, 1), round(float(np.max(G)), 3), round(float(np.min(G)), 3)))
    nadirs = [n for _, _, n in rows]
    nadir_deepens = all(nadirs[i] >= nadirs[i + 1] - 1e-9 for i in range(len(nadirs) - 1))
    dips_below_baseline = nadirs[-1] < 5.0 - 0.5
    return dict(rows=rows, nadir_deepens=bool(nadir_deepens), dips_below_baseline=bool(dips_below_baseline))

@lru_cache(maxsize=1)
def validate_d5c():
    ia = insulinoma_axis(); rh = reactive_hypo_curve()
    passed = bool(ia["fasting_monotone_falls"] and ia["crosses_hypo_threshold"] and
                  ia["recovers_on_resection"] and rh["nadir_deepens"] and rh["dips_below_baseline"])
    return dict(insulinoma=ia, reactive_hypoglycemia=rh, passed=passed,
                treatment=("insulinoma -- REMOVE the autonomous source (surgical resection / limit the "
                           "unregulated secretion term); the model shows the loop returns to setpoint once "
                           "the source is gone. Reactive hypoglycaemia -- BLUNT the post-prandial insulin "
                           "spike (slower carbohydrate, smaller meals). Target direction [V]; efficacy [O]."),
                grades="mirror-of-T1 mechanism [V] / hypoglycaemia threshold [L] / absolute glucose [O]")

# --------------------------------------------------------------------------- D5d  Functional dyspepsia (motility)
# Emptying-RATE window sized to resolve a MILD delay (a rate measured before completion, per the recipe's
# saturation-trap warning); FD lives at the MILD end of the s11 ICC/amplitude axis.
FD_RATE_WINDOW = 300.0

def fd_motility_curve():
    """Functional dyspepsia (motility component): a MILD reduction of the gastric contraction amplitude
    (a mild s11 ICC lesion) produces a MILD emptying-rate delay -- present and monotone, but far short of
    the severe-gastroparesis collapse. FD is a mild point on the SAME s11 axis. The post-prandial-distress
    / early-satiation (felt) component needs the Tier-2 accommodation reservoir + afferent-gain term and
    stays OPEN here; the felt interpretation lives in `mind` (firewall kept)."""
    norm = gastroparesis_emptying(1.0, Tt=FD_RATE_WINDOW)
    rows = [(round(r, 2), round(gastroparesis_emptying(r, Tt=FD_RATE_WINDOW) / norm * 100.0, 1))
            for r in [1.0, 0.9, 0.8, 0.7, 0.6, 0.4, 0.2]]
    pct = [p for _, p in rows]
    monotone = all(pct[i] >= pct[i + 1] - 1.0 for i in range(len(pct) - 1))
    mild_point = dict(rows)[0.8]                              # FD operating point (mild amplitude loss)
    severe_point = dict(rows)[0.2]                            # severe gastroparesis for contrast
    mild_delay_present = 80.0 < mild_point < 100.0           # a real but mild delay
    distinct_from_severe = mild_point > severe_point + 20.0  # clearly milder than gastroparesis
    return dict(rows=rows, monotone=monotone, mild_emptying_pct=mild_point, severe_emptying_pct=severe_point,
                mild_delay_present=bool(mild_delay_present), distinct_from_severe=bool(distinct_from_severe))

@lru_cache(maxsize=1)
def validate_d5d():
    fd = fd_motility_curve()
    passed = bool(fd["monotone"] and fd["mild_delay_present"] and fd["distinct_from_severe"])
    return dict(fd_motility=fd, passed=passed,
                treatment=("prokinetics raise the effective gastric contraction (as in s11) -> restore the "
                           "emptying rate; the post-prandial-distress part is the Tier-2 accommodation "
                           "reservoir (fundic-relaxing agents) + afferent gain (neuromodulators), with the "
                           "felt component in `mind`. Motility target [V]; felt component [O]."),
                grades="mild emptying-rate delay (mild point on s11) [V] partial / felt component [O]")

# --------------------------------------------------------------------------- D5e  SIBO (motility part)
def _sibo_retention(drive, k=5, **kw):
    """Retained proximal fraction after a fixed window on the validated s4 transporter: the fraction of
    the bolus that has NOT cleared the proximal k segments. Reads the s14 transporter's final luminal
    profile (no new mechanics). High retention = stasis."""
    _, c, _pos, _com0 = gut_transport(gradient_drive=drive, return_state=True, **kw)
    return float(c[:k].sum() / c.sum())

def sibo_stasis_curve():
    """SIBO (motility part): loss of the strong periodic housekeeping propulsion (reduced propulsive
    drive on the s4 transporter) -> STASIS, read as a rising retained proximal fraction, with a collapse
    threshold mirroring colonic inertia (s14). The motility part is near-Tier-1 and emerges here; the
    bacterial OVERGROWTH load itself is OUT of model ([O], needs a microbial layer), and the explicit
    migrating-motor-complex periodic-sweep element is deferred to Tier-2 (group B) per the No-Tuning rule."""
    rows = [(round(d, 2), round(_sibo_retention(d), 3)) for d in [1.0, 0.7, 0.5, 0.4, 0.3, 0.2, 0.1]]
    ret = [r for _, r in rows]
    monotone_rises = all(ret[i] <= ret[i + 1] + 1e-9 for i in range(len(ret) - 1))  # falls drive -> rises
    clears_at_normal = ret[0] < 0.05
    stasis_at_low_drive = ret[-1] > 0.5
    return dict(rows=rows, retention_monotone_rises_as_drive_falls=bool(monotone_rises),
                clears_at_normal_drive=bool(clears_at_normal), stasis_at_low_drive=bool(stasis_at_low_drive),
                columns="(propulsive_drive, retained_proximal_fraction)")

@lru_cache(maxsize=1)
def validate_d5e():
    sb = sibo_stasis_curve()
    passed = bool(sb["retention_monotone_rises_as_drive_falls"] and sb["clears_at_normal_drive"] and
                  sb["stasis_at_low_drive"])
    return dict(sibo=sb, passed=passed,
                treatment=("restore the periodic propulsive sweep -- prokinetics / motilin-class agents "
                           "reinstate clearance and lower the retained fraction; reducing the bacterial "
                           "load itself is out-of-model (a microbial layer). Motility target [V]; "
                           "bacterial load [O]."),
                grades="stasis-from-low-drive [V] motility / bacterial load [O] / MMC sweep deferred (Tier-2)")

@lru_cache(maxsize=1)
def validate_d5():
    a = validate_d5a(); b = validate_d5b(); c = validate_d5c(); d = validate_d5d(); e = validate_d5e()
    return dict(d5a_dumping=a, d5b_reflux_esophagitis=b, d5c_insulinoma_reactive_hypo=c,
                d5d_functional_dyspepsia_motility=d, d5e_sibo_stasis=e,
                passed=bool(a["passed"] and b["passed"] and c["passed"] and d["passed"] and e["passed"]),
                grades="five scattered Tier-1 readings; emergent [V] where supported, honest [O] (with obstacle) where the substrate needs a Tier-2 element")

# ===========================================================================
#  D6 (section 16) -- B1: sphincter / valve gate diseases (Tier-2, ONE new
#  primitive: the tonically-closed R19 gate `gate_open`). GERD and achalasia are
#  the TWO OPPOSITE failure modes of the SAME gate (tone-too-low vs cannot-open),
#  the gate analogue of the s11/s14 one-ICC-lesion mirror; Oddi is the same gate
#  at the biliary outlet; spasm is a s4 coordination pathology (amplitude cannot
#  rescue lost coordination). All readings emerge; the gate is derived from R19.
# ===========================================================================
GATE_TONE_NORMAL = 1.20     # [V] a continent resting LES tone (gate stays closed at rest, refluxes 0)
SWALLOW_RELAX    = 1.40     # [V] a coordinated swallow relaxation drive (opens a normal-tone gate)

def _reflux_transients(n=21, lo=0.30, hi=1.30):
    """A fixed, deterministic spectrum of intra-gastric pressure transients (TLESRs /
    strain). Each opens the gate iff it exceeds the gate resistance; the spectrum is
    never tuned to a target -- only the gate tone is swept."""
    return list(np.linspace(lo, hi, n))

def gerd_reflux_curve():
    """GERD = the gate fails CLOSED. As resting LES tone falls, more of the fixed
    pressure-transient spectrum clears the gate resistance (tone + spinodal), so the
    retrograde reflux burden rises monotonically -- continent at high tone (zero events),
    incompetent at low tone. The esophagitis CONSEQUENCE is the s15 reflux-erosion reader;
    this owns the reflux SOURCE (the gate)."""
    transients = _reflux_transients()
    rows = []
    for tone in [1.20, 1.00, 0.80, 0.60, 0.40, 0.20, 0.05]:
        thr = gate_resistance(tone)
        events = int(sum(1 for p in transients if gate_open(tone, p)))
        burden = float(sum(max(p - thr, 0.0) for p in transients if gate_open(tone, p)))
        rows.append((round(tone, 2), events, round(burden, 3)))
    bd = [b for _, _, b in rows]
    monotone_rises = all(bd[i] <= bd[i + 1] + 1e-9 for i in range(len(rows) - 1))
    return dict(rows=rows, columns="(LES_tone, reflux_events_of_21, retrograde_burden)",
                burden_monotone_rises_as_tone_falls=bool(monotone_rises),
                continent_at_high_tone=bool(rows[0][1] == 0), incompetent_at_low_tone=bool(rows[-1][1] > 0))

def achalasia_gate_stasis():
    """Achalasia = the gate fails OPEN (the mirror of GERD on the same gate). The
    coordinated swallow relaxation can no longer flip the gate, so the bolus is retained
    at the junction (stasis/dilatation). Two routes reach the same stuck gate: a failing
    relaxation drive (transduction loss) and a rising gate tone -- both make open_drive <
    gate_resistance. Aperistalsis (loss of the s4 wave) compounds upstream clearance."""
    relax = []
    for frac in [1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10]:
        opened = gate_open(0.60, SWALLOW_RELAX * frac)
        relax.append((round(frac, 2), bool(opened), 0.0 if opened else 1.0))
    tone_route = []
    for tone in [0.40, 0.70, 1.00, 1.30, 1.60]:
        opened = gate_open(tone, SWALLOW_RELAX)
        tone_route.append((round(tone, 2), bool(opened), 0.0 if opened else 1.0))
    norm = gut_transport()
    aperi = [(round(gd, 2), round(gut_transport(gradient_drive=gd) / norm * 100.0, 1))
             for gd in [1.0, 0.6, 0.3, 0.1]]
    return dict(relaxation_route=relax, tone_route=tone_route, aperistalsis=aperi,
                columns="relax/tone: (knob, gate_open, retained_fraction); aperistalsis: (coord, transit_pct)",
                passes_when_competent=bool(relax[0][1] and tone_route[0][1]),
                stasis_when_gate_fails_to_open=bool((not relax[-1][1]) and (not tone_route[-1][1])),
                aperistalsis_degrades_transit=bool(aperi[-1][1] < 40.0))

def esophageal_spasm_curve():
    """Spasm / jackhammer / nutcracker = a s4 COORDINATION pathology. Net directed
    transport collapses as the aboral phase coordination is lost, and -- the jackhammer
    signature -- raising contraction AMPLITUDE does NOT rescue transit (vigorous but
    uncoordinated contraction fails to move the bolus). The felt chest-pain component is
    out of scope (afferent gain -> `mind`)."""
    norm = gut_transport()
    coord = [(round(gd, 2), round(gut_transport(gradient_drive=gd) / norm * 100.0, 1))
             for gd in [1.0, 0.8, 0.6, 0.4, 0.2, 0.05]]
    pct = [p for _, p in coord]
    coord_monotone = all(pct[i] >= pct[i + 1] - 2.0 for i in range(len(pct) - 1))
    amp_rescue = [(round(a, 1), round(gut_transport(gradient_drive=0.1, icc_density=a) / norm * 100.0, 1))
                  for a in [1.0, 1.5, 2.0, 3.0]]
    return dict(coordination_axis=coord, amplitude_rescue=amp_rescue,
                columns="coordination: (coord, transit_pct); amplitude_rescue: (amplitude, transit_pct)",
                transit_collapses_as_coordination_lost=bool(coord_monotone and pct[-1] < 20.0),
                amplitude_cannot_rescue=bool(all(p < 20.0 for _, p in amp_rescue)))

def oddi_outflow():
    """Sphincter of Oddi dysfunction = the SAME gate primitive at the biliary / pancreatic
    outlet. A stuck-closed gate (failing relaxation) gives an outflow-obstruction proxy:
    biliary outflow ceases when the gate cannot open. The treatment mirror (sphincterotomy
    = force the gate open) is the same as achalasia. (Biliary layer itself is group C.)"""
    rows = []
    for frac in [1.00, 0.80, 0.60, 0.40, 0.20]:
        opened = gate_open(0.60, SWALLOW_RELAX * frac)
        rows.append((round(frac, 2), bool(opened), 1.0 if opened else 0.0))
    return dict(rows=rows, columns="(relax_competence, gate_open, biliary_outflow)",
                outflow_obstructs_when_gate_stuck=bool(rows[0][1] and (not rows[-1][1])))

@lru_cache(maxsize=1)
def validate_d6a():
    g = gerd_reflux_curve()
    passed = bool(g["burden_monotone_rises_as_tone_falls"] and g["continent_at_high_tone"] and g["incompetent_at_low_tone"])
    return dict(gerd=g, passed=passed,
                treatment=("GERD -- RAISE the gate tone / lower the intra-gastric opening drive: the model reduces "
                           "reflux events by lifting the gate resistance (tone + spinodal) back above the pressure-"
                           "transient spectrum (anti-reflux barrier / fundoplication; weight loss lowers the driving "
                           "pressure). The mucosal-injury CONSEQUENCE is treated on the s15 reflux-erosion curve (acid "
                           "suppression). Target direction [V]; absolute reflux frequency [O]."),
                grades="reflux-burden-from-falling-tone [V] / continence anchor [V] / absolute reflux frequency [O]")

@lru_cache(maxsize=1)
def validate_d6b():
    a = achalasia_gate_stasis()
    passed = bool(a["passes_when_competent"] and a["stasis_when_gate_fails_to_open"] and a["aperistalsis_degrades_transit"])
    return dict(achalasia=a, passed=passed,
                treatment=("achalasia -- FORCE the gate-open transition: pneumatic dilation / myotomy / botulinum to "
                           "the gate all drop the gate resistance so the (preserved) relaxation drive can again clear "
                           "it; the model predicts efficacy tracks how far the resistance is lowered below the available "
                           "open drive. Aperistalsis (the s4 wave) is not restored by opening the gate -- the residual "
                           "transit deficit is the falsifiable prediction. Direction [V]; efficacy [O]."),
                grades="gate-stuck-closed stasis (mirror of GERD) [V] / aperistalsis [V] / absolute clearance [O]")

@lru_cache(maxsize=1)
def validate_d6c():
    s = esophageal_spasm_curve()
    passed = bool(s["transit_collapses_as_coordination_lost"] and s["amplitude_cannot_rescue"])
    return dict(spasm=s, passed=passed,
                treatment=("spasm / jackhammer -- RESTORE coordination and/or REDUCE the excessive amplitude (smooth-"
                           "muscle relaxants, nitrates / calcium-channel blockers): the model shows lowering amplitude "
                           "alone does not restore transit unless coordination returns, which is exactly why these "
                           "disorders are refractory -- the falsifiable prediction. The felt chest-pain component is "
                           "afferent-gain (B3 / `mind`), out of scope here. Direction [V]; efficacy [O]."),
                grades="coordination-loss collapses transit [V] / amplitude-independence (jackhammer) [V] / felt pain [O]")

@lru_cache(maxsize=1)
def validate_d6d():
    o = oddi_outflow()
    passed = bool(o["outflow_obstructs_when_gate_stuck"])
    return dict(oddi=o, passed=passed,
                treatment=("sphincter of Oddi dysfunction -- RELAX / ablate the gate (endoscopic sphincterotomy): the "
                           "same force-the-gate-open mirror as achalasia, restoring biliary / pancreatic outflow. "
                           "Direction [V]; absolute outflow and patient selection [O] (biliary layer is group C)."),
                grades="stuck-gate outflow obstruction (same gate, biliary outlet) [V] / absolute outflow [O]")

def validate_d6():
    a = validate_d6a(); b = validate_d6b(); c = validate_d6c(); d = validate_d6d()
    return dict(d6a_gerd=a, d6b_achalasia=b, d6c_esophageal_spasm=c, d6d_sphincter_of_oddi=d,
                passed=bool(a["passed"] and b["passed"] and c["passed"] and d["passed"]),
                grades=("B1 sphincter-gate Tier-2 cluster on ONE new R19-derived gate primitive; GERD and achalasia "
                        "are the two opposite failure modes of the same gate (the gate analogue of the one-ICC-lesion "
                        "mirror); all motor readings [V], felt / absolute quantities [O] with stated obstacles"))


# ===========================================================================
#  D7 (section 17) -- B2: gastric accommodation reservoir (Tier-2, ONE new
#  primitive: the fundic COMPLIANCE element reservoir_compliance / meal_pressure).
#  Impaired fundic accommodation -> a stiff reservoir -> a fixed meal raises pressure
#  PREMATURELY (early satiation / post-prandial distress) = functional dyspepsia,
#  post-prandial distress syndrome (PDS). This is the post-prandial-distress component
#  that the s15 FD-motility reader explicitly left OPEN; together they cover the two
#  recognised FD axes (epigastric-pain/motility at s15, post-prandial-distress here).
#  The reservoir is the SAME R19 element relaxed from its contracted basin toward yield;
#  the wall stiffness is the R19 restoring curvature, the compliance its inverse -- no fit.
#  The FELT distress mapping stays OPEN [O] (needs the B3 afferent-gain term; the felt
#  interpretation lives in `mind`, firewall kept).
# ===========================================================================
FUNDUS_G      = 1.0     # [V] the gastric R19 scale (same switch as the s2 slow-wave / s16 gate)
MEAL_VOLUME   = 1.0     # model volume unit (absolute scale [O], like the s6 glycogen capacity)
ACC_NORMAL_FR = 0.90    # a healthy relaxing fundus: accommodation near (below) the yield drive
ACC_FD_FR     = 0.15    # impaired accommodation (the FD post-prandial-distress operating point)

def accommodation_pressure_curve():
    """Functional dyspepsia (post-prandial distress): as fundic accommodation falls, the
    reservoir wall stiffens and a FIXED meal raises intra-gastric pressure prematurely.
    Accommodation is expressed as a fraction of the yield (spinodal) drive, so the knob is
    tied to the substrate and never tuned. As the fraction falls the operating point retreats
    toward the contracted rest s=-sqrt(g): wall stiffness k=3s^2-g RISES, compliance C=1/k
    FALLS (early satiation -- less meal tolerated per unit satiation pressure), and the fixed-
    meal pressure P=V*k RISES. Normal accommodation absorbs the meal; impaired accommodation is
    premature pressure. Thresholds are RELATIVE to the substrate's own stiff baseline P0=2gV
    (no fitted clinical number)."""
    g, V = FUNDUS_G, MEAL_VOLUME
    sp = spinodal(g)
    P0 = 2.0 * g * V                                          # stiffest (unaccommodated) baseline pressure
    rows = []
    for fr in [0.90, 0.75, 0.60, 0.45, 0.30, 0.15, 0.05]:    # accommodation fraction, DESCENDING
        h = fr * sp
        k = wall_stiffness(g, h)
        C = reservoir_compliance(g, h)
        P = meal_pressure(g, h, V)
        rows.append((round(fr, 2), round(C, 4), round(k, 4), round(P, 4)))
    Ps = [P for _, _, _, P in rows]; Cs = [C for _, C, _, _ in rows]
    pressure_rises = all(Ps[i] <= Ps[i + 1] + 1e-9 for i in range(len(rows) - 1))
    compliance_falls = all(Cs[i] >= Cs[i + 1] - 1e-9 for i in range(len(rows) - 1))  # = satiation volume falls
    normal_P = meal_pressure(g, ACC_NORMAL_FR * sp, V)
    fd_P     = meal_pressure(g, ACC_FD_FR * sp, V)
    return dict(rows=rows, baseline_stiff_pressure=round(P0, 4),
                columns="(accommodation_fraction_of_yield, compliance, wall_stiffness, meal_pressure)",
                pressure_rises_as_accommodation_falls=bool(pressure_rises),
                compliance_falls_as_accommodation_falls=bool(compliance_falls),
                normal_pressure=round(normal_P, 4), fd_pressure=round(fd_P, 4),
                normal_absorbs_meal=bool(normal_P < 0.40 * P0),
                premature_pressure_when_impaired=bool(fd_P > 0.80 * P0))

def accommodation_treatment_axis():
    """Treatment direction: a fundic-relaxing agent RAISES the accommodation / compliance term.
    Starting from the impaired FD operating point and lifting accommodation back toward normal
    LOWERS the fixed-meal pressure monotonically -- the model's mechanistic prediction (efficacy
    absolute value is [O])."""
    g, V = FUNDUS_G, MEAL_VOLUME; sp = spinodal(g)
    rows = [(round(fr, 2), round(meal_pressure(g, fr * sp, V), 4))
            for fr in [0.15, 0.30, 0.45, 0.60, 0.75, 0.90]]   # rising accommodation
    Ps = [p for _, p in rows]
    lowers = all(Ps[i] >= Ps[i + 1] - 1e-9 for i in range(len(rows) - 1))
    return dict(rows=rows, columns="(accommodation_fraction, meal_pressure)",
                raising_compliance_lowers_pressure=bool(lowers))

def accommodation_yield_identity():
    """Substrate identity (exact, closed form): the yield point -- where the wall stiffness
    vanishes and the compliance diverges -- IS the R19 spinodal. At s=-sqrt(g/3) the stiffness
    k=3s^2-g=0 exactly, and that s is a (double) root of the field g*s-s^3+h at h=spinodal(g),
    i.e. the contracted fixed point merges with the unstable point exactly at the spinodal drive.
    The accommodation reservoir's maximal-compliance limit is therefore a property of the R19
    double well, not a fitted bound. (Computed in closed form: settle() under-resolves the
    marginal saddle-node by critical slowing, so readings operate strictly below yield.)"""
    g = FUNDUS_G
    s_yield = -math.sqrt(g / 3.0)
    k_yield = 3.0 * s_yield * s_yield - g                     # exact 0
    field_at_yield = sdot(s_yield, g, spinodal(g))            # exact 0 -> double root at the spinodal
    return dict(s_yield=round(s_yield, 6), k_at_yield=k_yield, field_at_spinodal=field_at_yield,
                yield_is_r19_spinodal=bool(abs(k_yield) < 1e-12 and abs(field_at_yield) < 1e-12))

@lru_cache(maxsize=1)
def validate_d7():
    cv = accommodation_pressure_curve(); tx = accommodation_treatment_axis(); yi = accommodation_yield_identity()
    passed = bool(cv["pressure_rises_as_accommodation_falls"] and cv["compliance_falls_as_accommodation_falls"]
                  and cv["normal_absorbs_meal"] and cv["premature_pressure_when_impaired"]
                  and tx["raising_compliance_lowers_pressure"] and yi["yield_is_r19_spinodal"])
    return dict(accommodation=cv, treatment_axis=tx, yield_identity=yi, passed=passed,
                treatment=("functional dyspepsia (post-prandial distress) -- RESTORE fundic accommodation: a fundic-"
                           "relaxing agent raises the compliance term, sliding the reservoir wall back toward its yield "
                           "point so a fixed meal is absorbed without the premature pressure rise (the model lowers the "
                           "meal pressure monotonically as accommodation is restored). The motility/emptying component "
                           "is the s15 prokinetic target; this reader owns the accommodation/early-satiation axis. The "
                           "FELT distress itself is afferent-gain (B3) with the felt interpretation in `mind` (firewall). "
                           "Target direction [V]; absolute efficacy and the felt symptom mapping [O]."),
                grades=("B2 accommodation-reservoir Tier-2 reader on ONE new R19-derived compliance primitive; the "
                        "premature-pressure / early-satiation mechanism is [V] partial (the post-prandial-distress axis "
                        "s15 left open), the felt distress is [O] (B3 afferent gain + `mind` firewall), and the absolute "
                        "meal-volume / pressure scale is a model unit [O]"))


# ===========================================================================
#  D8 (section 18) -- B3: visceral afferent-gain disorders (Tier-2, ONE new
#  primitive: the R19-derived afferent susceptibility afferent_gain / afferent_signal).
#  The visceral afferent is the SAME R19 element resting quiescent; its static gain is the
#  restoring-curvature inverse 1/k -- the IDENTICAL quantity the s17 reservoir reads as
#  fundic COMPLIANCE (one R19 curvature, two readings: sensory gain here, mechanical
#  compliance there). IBS = an s14 motility SUBTYPE (the transport bias sets C/M/D) PLUS a
#  raised afferent gain (the visceral hypersensitivity); functional abdominal pain = raised
#  afferent gain at NORMAL motility (no structural lesion). The gain rises monotonically with
#  a peripheral sensitization bias and DIVERGES at the R19 spinodal -- the SAME marginal point
#  as the s17 reservoir yield -- so allodynia and (past yield) spontaneous firing are a
#  saddle-node critical gain, not a fitted curve. FIREWALL: this owns the PERIPHERAL afferent
#  term only; the felt / affective interpretation is `mind` ([O]). HPA is never re-emerged here.
# ===========================================================================
AFFERENT_G       = 1.0      # [V] the gut R19 scale (same switch as the s2 slow-wave / s16 gate / s17 wall)
DISTENSION_STIM  = 0.10     # a fixed NORMAL wall-distension input (model unit; absolute scale [O])
IBS_C_DRIVE      = 0.20     # IBS-C operating point: low transport bias -> slow transit (retained)
IBS_M_DRIVE      = 0.25     # IBS-M operating point: intermediate transport bias (mixed)
IBS_D_DRIVE      = 0.60     # IBS-D operating point: normal/high transport bias -> cleared (rapid)

def ibs_subtype_axis():
    """IBS subtype (IBS-C / IBS-M / IBS-D) emerges from the s14 transport bias: the retained proximal
    fraction (the s15 SIBO reader) falls monotonically as the propulsive/transport drive rises, so one
    bias parameter ORDERS the subtypes -- IBS-C (low drive, retained = slow transit) -> IBS-M
    (intermediate) -> IBS-D (cleared = rapid transit). The constipation side is the s14 slow-transit
    mechanism [V]; the diarrhoea side hits the SAME conserved-bolus ceiling as s15 dumping (the occlusion
    wave cannot express transit FASTER than normal), so the absolute rapid-transit MAGNITUDE is an honest
    [O] -- but the subtype assignment (which way the bias points) and the C->D ordering are [V]. The
    hypersensitivity that, layered on this motility subtype, makes it IBS is the afferent gain below."""
    drives = [0.20, 0.25, 0.30, 0.40, 0.60, 0.90]
    rows = [(round(d, 2), round(_sibo_retention(d, Tt=300.0), 3)) for d in drives]
    ret = [r for _, r in rows]
    monotone_falls = all(ret[i] >= ret[i + 1] - 1e-9 for i in range(len(ret) - 1))
    c_ret = _sibo_retention(IBS_C_DRIVE, Tt=300.0)         # IBS-C (slow, retained)
    m_ret = _sibo_retention(IBS_M_DRIVE, Tt=300.0)         # IBS-M (intermediate)
    d_ret = _sibo_retention(IBS_D_DRIVE, Tt=300.0)         # IBS-D (cleared, rapid)
    subtypes_ordered = bool(c_ret > m_ret > d_ret - 1e-9 and c_ret > 0.4 and d_ret < 0.05)
    # the diarrhoea-side absolute magnitude ceiling (shared with s15 dumping): the rapid side saturates
    norm_disp = gut_transport()
    rapid_disp = gut_transport(gradient_drive=2.5, Dtrans=0.50)
    rapid_overshoot_pct = (rapid_disp - norm_disp) / norm_disp * 100.0
    rapid_magnitude_saturates = rapid_overshoot_pct < 5.0
    return dict(rows=rows, columns="(transport_drive, retained_proximal_fraction)",
                retention_monotone_falls_as_drive_rises=bool(monotone_falls),
                ibs_c_retained=round(c_ret, 3), ibs_m_retained=round(m_ret, 3), ibs_d_retained=round(d_ret, 3),
                subtypes_ordered_C_M_D=subtypes_ordered,
                rapid_overshoot_pct=round(rapid_overshoot_pct, 3),
                rapid_magnitude_saturates=bool(rapid_magnitude_saturates))

def visceral_hypersensitivity_axis():
    """Visceral hypersensitivity = a raised afferent gain on the NEW R19-derived afferent element. A
    peripheral sensitization bias b (inflammation / mediators / peripheral facilitation) slides the
    quiescent afferent operating point toward yield, so the static gain chi = 1/k = afferent_gain(g,b)
    RISES monotonically and the afferent SIGNAL for a FIXED normal wall-distension rises with it
    (allodynia: the same distension yields a larger signal -- a hypersensitivity proxy). Past the R19
    spinodal the same normal distension flips the element DISCONTINUOUSLY into the firing basin
    (spontaneous / un-provoked afferent activity -- a 'crisis'). gain monotonicity + allodynia are [V],
    the divergence-at-spinodal is the exact R19 identity [F]; the FELT pain is `mind` [O] (firewall)."""
    g, sp, stim = AFFERENT_G, spinodal(AFFERENT_G), DISTENSION_STIM
    base_gain = afferent_gain(g, 0.0)                      # 1/(2g) baseline sensitivity
    rows = []                                              # sub-yield sweep: b+stim stays below the spinodal
    for fr in [0.00, 0.15, 0.30, 0.45, 0.60]:
        b = fr * sp
        rows.append((round(fr, 2), round(afferent_gain(g, b), 4), round(afferent_signal(g, b, stim), 5)))
    gains = [gn for _, gn, _ in rows]; sigs = [s for _, _, s in rows]
    gain_rises = all(gains[i] <= gains[i + 1] + 1e-9 for i in range(len(rows) - 1))
    signal_rises = all(sigs[i] <= sigs[i + 1] + 1e-9 for i in range(len(rows) - 1))   # allodynia
    allodynia_ratio = sigs[-1] / sigs[0]                  # same distension, signal amplified by the gain
    # crisis: a normal distension flips the sensitized element ON once b passes ~the spinodal region
    fires_at_rest_lo = settle(g, 0.60 * sp, s0=-math.sqrt(g)) > 0.0          # not yet (sub-yield)
    fires_with_stim_hi = settle(g, 0.80 * sp + stim, s0=-math.sqrt(g)) > 0.0  # provoked flip past yield
    fires_at_rest_hi = settle(g, 1.10 * sp, s0=-math.sqrt(g)) > 0.0           # spontaneous (rest past spinodal)
    return dict(rows=rows, columns="(sensitization_fraction_of_yield, afferent_gain, afferent_signal_at_fixed_distension)",
                baseline_gain=round(base_gain, 4), gain_rises_with_sensitization=bool(gain_rises),
                signal_rises_allodynia=bool(signal_rises), allodynia_amplification=round(allodynia_ratio, 2),
                quiescent_at_sub_yield=bool(not fires_at_rest_lo),
                provoked_firing_past_yield=bool(fires_with_stim_hi),
                spontaneous_firing_past_spinodal=bool(fires_at_rest_hi))

def functional_abdominal_pain_axis():
    """Functional abdominal pain = a raised afferent gain at NORMAL motility, no structural lesion. At a
    NORMAL transport bias (drive=1.0, where the s14 transit is normal -- the retained fraction ~0) the
    afferent signal proxy for a fixed distension RISES with the sensitization bias: the pain proxy
    increases while motility stays normal -- the feature that distinguishes functional abdominal pain
    (pure afferent gain) from IBS (afferent gain PLUS an s14 motility subtype). The proxy rise is [V];
    that the proxy IS the felt pain is `mind` [O] (peripheral afferent term only here -- firewall)."""
    g, sp, stim = AFFERENT_G, spinodal(AFFERENT_G), DISTENSION_STIM
    normal_motility_retention = _sibo_retention(1.00, Tt=300.0)   # transit is normal (no motility lesion)
    rows = [(round(fr, 2), round(afferent_signal(g, fr * sp, stim), 5)) for fr in [0.00, 0.20, 0.40, 0.60]]
    sigs = [s for _, s in rows]
    pain_proxy_rises = all(sigs[i] <= sigs[i + 1] + 1e-9 for i in range(len(rows) - 1))
    motility_normal = normal_motility_retention < 0.05
    return dict(rows=rows, columns="(sensitization_fraction_of_yield, afferent_signal_proxy)",
                normal_motility_retained_fraction=round(normal_motility_retention, 3),
                motility_normal=bool(motility_normal), pain_proxy_rises_at_normal_motility=bool(pain_proxy_rises))

def afferent_gain_identity():
    """Substrate identity (exact): the visceral-afferent GAIN and the s17 fundic COMPLIANCE are the SAME
    R19 curvature inverse 1/k, read two ways. (1) afferent_gain(g,b) == reservoir_compliance(g,b) for all
    b (gain == compliance, an algebraic identity of the operating point). (2) The analytic susceptibility
    equals the simulated small-signal response: afferent_signal(g,b,eps)/eps -> afferent_gain(g,b) as
    eps->0. (3) The gain DIVERGES exactly at the R19 spinodal -- the SAME marginal saddle-node as the s17
    reservoir yield -- where 3*s^2 - g = 0 at s = -sqrt(g/3) and the field has a double root at the
    spinodal drive (computed in closed form; settle under-resolves the marginal point by critical slowing).
    One R19 marginal point, three readings: critical gain (B3), maximal compliance (B2), discontinuous
    flip (R19)."""
    g, sp = AFFERENT_G, spinodal(AFFERENT_G)
    gain_eq_compliance = max(abs(afferent_gain(g, fr * sp) - reservoir_compliance(g, fr * sp))
                             for fr in [0.0, 0.3, 0.6, 0.9])
    eps = 1e-4
    selfconsist = max(abs(afferent_signal(g, fr * sp, eps) / eps - afferent_gain(g, fr * sp))
                      / afferent_gain(g, fr * sp) for fr in [0.0, 0.3, 0.6])
    s_yield = -math.sqrt(g / 3.0)
    k_yield = 3.0 * s_yield * s_yield - g                  # exact 0 -> gain diverges
    field_at_yield = sdot(s_yield, g, sp)                  # exact 0 -> double root at the spinodal
    return dict(gain_equals_compliance_maxabs=gain_eq_compliance,
                gain_is_b2_compliance=bool(gain_eq_compliance < 1e-12),
                susceptibility_selfconsistent_relerr=round(selfconsist, 6),
                susceptibility_matches_response=bool(selfconsist < 1e-3),
                s_yield=round(s_yield, 6), k_at_yield=k_yield, field_at_spinodal=field_at_yield,
                gain_diverges_at_r19_spinodal=bool(abs(k_yield) < 1e-12 and abs(field_at_yield) < 1e-12))

@lru_cache(maxsize=1)
def validate_d8():
    sub = ibs_subtype_axis(); hs = visceral_hypersensitivity_axis()
    fap = functional_abdominal_pain_axis(); idn = afferent_gain_identity()
    passed = bool(sub["retention_monotone_falls_as_drive_rises"] and sub["subtypes_ordered_C_M_D"]
                  and sub["rapid_magnitude_saturates"]
                  and hs["gain_rises_with_sensitization"] and hs["signal_rises_allodynia"]
                  and hs["quiescent_at_sub_yield"] and hs["provoked_firing_past_yield"]
                  and hs["spontaneous_firing_past_spinodal"]
                  and fap["motility_normal"] and fap["pain_proxy_rises_at_normal_motility"]
                  and idn["gain_is_b2_compliance"] and idn["susceptibility_matches_response"]
                  and idn["gain_diverges_at_r19_spinodal"])
    return dict(ibs_subtype=sub, visceral_hypersensitivity=hs, functional_abdominal_pain=fap,
                gain_identity=idn, passed=passed,
                treatment=("IBS -- subtype-directed motility correction PLUS lowering the afferent gain. The "
                           "motility target is the s14 transport bias: IBS-C raises the propulsive drive "
                           "(prokinetics / secretagogues), IBS-D lowers it (antimotility agents) -- the same "
                           "knob, opposite sign by subtype. The hypersensitivity target is the afferent gain: "
                           "neuromodulators lower the sensitization bias, sliding the operating point away from "
                           "yield so the same distension produces a smaller signal (the model lowers the "
                           "afferent signal monotonically as the gain is lowered). Functional abdominal pain -- "
                           "lower the afferent gain alone (central / peripheral neuromodulation), since motility "
                           "is normal. The brain-gut / felt / affective interpretation stays in `mind` behind "
                           "the firewall; only the peripheral afferent term is moved here. Target directions [V]; "
                           "absolute efficacy and the felt symptom mapping [O]."),
                grades=("B3 visceral afferent-gain Tier-2 cluster on ONE new R19-derived afferent primitive; the "
                        "IBS motility subtype (s14 transport bias) is [V] for the C->D ordering with the absolute "
                        "rapid-transit magnitude an honest [O] (the s15 conserved-bolus ceiling), the visceral "
                        "hypersensitivity (gain rise + allodynia) is [V] with the divergence-at-spinodal an exact "
                        "[F] identity (the same marginal point as the s17 reservoir yield), and the felt pain / "
                        "affective experience is [O] -- the peripheral afferent term only, felt interpretation in "
                        "`mind` (firewall kept)"))


# ===========================================================================
#  D9 (section 22) -- C1: immune / inflammation layer (Tier-3, ONE new
#  R19-derived relapsing-inflammation primitive: flare_state / flare_burden +
#  the section-7 coupling inflammatory_barrier_scale). Mucosal inflammation is the
#  SAME R19 switch read as a RELAPSING-REMITTING element (remission -s basin vs
#  flare +s basin); a cumulative flare burden lowers the section-7 fate-stability
#  scale g -> a higher malignant-crossing rate (the IBD->colorectal / Crohn's
#  small-bowel neoplasia continuity -- closing the section-21 out-of-kernel small-
#  bowel boundary). IBD = relapsing inflammation; flares = barrier-scale excursions.
#  Celiac / microscopic colitis / eosinophilic / autoimmune are the same layer
#  (driver removal -> remission -> barrier/villous recovery). The FELT/affective
#  component is `mind` (firewall). New layer; absolute incidence + the absorptive
#  magnitude are [O] with stated obstacles.
# ===========================================================================
IBD_G            = 1.0      # [V] the mucosal R19 scale (same switch as the s2 slow-wave / s7 barrier)
IBD_ANTIGEN      = 0.50     # a sustained luminal-antigen / dysbiosis drive in active extensive disease
IBD_CRC_RR       = 2.4      # [L] population SIR for UC colorectal cancer (Jess 2012); Eaden 2001 higher for extensive long-standing

def ibd_relapsing_course():
    """IBD (Crohn's / ulcerative colitis) = relapsing-remitting inflammation on the NEW R19-derived
    inflammation element. (1) HYSTERESIS: ramping the antigen drive UP from remission flips to a flare past
    the R19 spinodal, and ramping it back DOWN leaves the flare SELF-SUSTAINING (the relapsing course -- a
    flare does not spontaneously resolve when the antigen merely subsides). (2) INDUCTION: suppression must
    exceed antigen + spinodal(g) to flip a flare back to remission. (3) MAINTENANCE asymmetry: once in
    remission a much LOWER suppression holds it (remission persists until antigen - suppression > spinodal) --
    the induction-vs-maintenance dosing asymmetry, an exact property of the double well. All emergent; nothing
    fitted."""
    g, sp = IBD_G, spinodal(IBD_G)
    # (1) hysteresis: up-ramp then down-ramp, carrying the state
    s = -math.sqrt(g); up = []
    for a in [0.0, 0.10, 0.20, 0.30, 0.40, 0.50]:
        s = flare_state(g, a, 0.0, in_flare=(s > 0)); up.append((round(a, 2), round(s, 3)))
    down = []
    for a in [0.50, 0.40, 0.30, 0.20, 0.10, 0.0]:
        s = flare_state(g, a, 0.0, in_flare=(s > 0)); down.append((round(a, 2), round(s, 3)))
    flips_up   = bool(up[0][1] < 0 and up[-1][1] > 0)            # remission -> flare on the up-ramp
    self_sustaining = bool(down[-1][1] > 0)                       # still in flare at antigen 0 (relapsing)
    # (2) induction threshold: suppression > antigen + spinodal flips flare -> remission
    induction_thr = IBD_ANTIGEN + sp
    ind = [(round(supp, 2), round(flare_state(g, IBD_ANTIGEN, supp, in_flare=True), 3))
           for supp in [0.40, 0.60, induction_thr - 0.01, induction_thr + 0.01, 0.90]]
    induction_works = bool(ind[-1][1] < 0 and ind[0][1] > 0)
    # (3) maintenance asymmetry (the bistable gap): a mid dose BETWEEN the maintenance threshold
    # (antigen - spinodal) and the induction threshold (antigen + spinodal) HOLDS remission but cannot
    # INDUCE it -- the same suppression gives two outcomes by history (a dose that maintains is not enough
    # to induce). This is the induction-vs-maintenance asymmetry, exact in the double well.
    mid_dose = IBD_ANTIGEN                                        # = 0.50, lies in (antigen-sp, antigen+sp)
    from_flare    = flare_state(g, IBD_ANTIGEN, mid_dose, in_flare=True)    # cannot break the flare
    from_remission = flare_state(g, IBD_ANTIGEN, mid_dose, in_flare=False)  # holds remission
    maint = [(round(mid_dose, 2), round(from_flare, 3), round(from_remission, 3))]
    maintenance_lower = bool(from_flare > 0 and from_remission < 0)
    return dict(up_ramp=up, down_ramp=down, induction=ind,
                maintenance_same_dose_two_outcomes=maint,
                induction_threshold=round(induction_thr, 4), maintenance_threshold=round(IBD_ANTIGEN - sp, 4),
                columns="up/down: (antigen, state); induction: (suppression, state_from_flare); "
                        "maintenance: (dose, state_from_flare, state_from_remission)",
                relapsing_hysteresis=bool(flips_up and self_sustaining),
                induction_needs_suppression_past_antigen_plus_spinodal=induction_works,
                maintenance_threshold_lower_than_induction=maintenance_lower)

@lru_cache(maxsize=1)
def _calib_ibd_kappa():
    """ONE bisection: the cumulative-inflammatory-burden -> barrier-scale coupling kappa such that the MAX
    sustained flare burden (active extensive long-standing disease) reproduces the cited IBD-CRC RR via the
    SAME section-7 kernel. No curve-shape tuning -- one anchor, one bisection."""
    bmax = flare_burden(IBD_G, IBD_ANTIGEN, 0.0, in_flare=True)
    lo, hi = 1e-6, (1.0 - 0.2) / bmax * 0.999
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if onco.RR(inflammatory_barrier_scale(1.0, bmax, mid), 0.0) < IBD_CRC_RR: lo = mid
        else: hi = mid
    return (lo + hi) / 2.0

def ibd_neoplasia_bridge():
    """IBD -> colorectal / small-bowel neoplasia: the relapsing inflammation BRIDGES to the section-7
    barrier-Kramers kernel. A cumulative flare burden (extent x duration x activity) lowers the section-7
    fate-stability scale g (the IDENTICAL g-reduction the section-10 chronic-Hp step uses), so the malignant-
    crossing RR rises monotonically with cumulative burden -- the duration/extent-dependent IBD cancer risk.
    The deepest-burden point is anchored to a cited IBD-CRC RR by ONE bisection. Suppression (mucosal healing
    -> burden 0) collapses the RR back to baseline -- the surveillance/treatment lever, and the reason
    sustained remission lowers cancer risk. This closes the section-21 out-of-kernel small-bowel-adenocarcinoma
    boundary: the C1 immune layer now supplies its barrier-lowering driver (Crohn's small-bowel; UC colorectal)."""
    kappa = _calib_ibd_kappa()
    bmax = flare_burden(IBD_G, IBD_ANTIGEN, 0.0, in_flare=True)
    rows = []
    for frac in [0.0, 0.25, 0.50, 0.75, 1.00]:                    # cumulative burden fraction
        b = bmax * frac
        g_eff = inflammatory_barrier_scale(1.0, b, kappa)
        rows.append((round(frac, 2), round(g_eff, 4), round(onco.RR(g_eff, 0.0), 3)))
    rrs = [r for _, _, r in rows]
    monotone = all(rrs[i + 1] > rrs[i] - 1e-9 for i in range(len(rrs) - 1))
    anchor_hit = abs(rrs[-1] - IBD_CRC_RR) < 0.05
    # treatment: drive the burden to 0 (remission) -> RR collapses to baseline
    collapse = [(int(f * 100), round(onco.RR(inflammatory_barrier_scale(1.0, bmax * (1.0 - f), kappa), 0.0), 3))
                for f in [0.0, 0.25, 0.5, 0.75, 1.0]]            # f = fraction of burden removed by suppression
    crs = [v for _, v in collapse]
    treatment_collapses = bool(all(crs[i + 1] < crs[i] for i in range(len(crs) - 1)) and abs(crs[-1] - 1.0) < 0.05)
    return dict(kappa=round(kappa, 6), burden_rr=rows, suppression_collapse=collapse,
                columns="burden_rr: (cumulative_burden_fraction, g_eff, CRC_RR); collapse: (% burden removed, RR)",
                rr_rises_with_burden=bool(monotone), anchor_hit=bool(anchor_hit),
                suppression_collapses_rr=treatment_collapses,
                closes_small_bowel_boundary=True)

def immune_same_layer_readings():
    """Companion diseases on the SAME C1 inflammation element, in its ANTIGEN-DEPENDENT regime (less
    hysteretic than IBD's relapsing course): the driver sets the state, and its removal is the lever. Celiac:
    a gluten-antigen drive flips the mucosal element from its remission baseline into a flare (villous
    atrophy); removing the antigen (gluten-free) leaves it in remission (mucosal/villous recovery) -- the
    absorptive-surface MAGNITUDE and timescale need an absorption layer [O], but the antigen-removal direction
    is [V]. Microscopic colitis / eosinophilic oesophagitis-gastroenteritis / autoimmune pancreatitis-hepatitis:
    same element, same lever (remove the antigen / eosinophil / immune driver). Evaluated from the remission
    baseline so the reading is the natural-history antigen dependence; returns the present->flare / absent->
    remission flags (shared)."""
    g = IBD_G
    flare_on  = flare_state(g, 0.50, 0.0, in_flare=False) > 0.0    # antigen present -> flares
    remit_off = flare_state(g, 0.05, 0.0, in_flare=False) < 0.0    # antigen removed -> quiescent (remission)
    return dict(celiac_gluten_flare=bool(flare_on), celiac_glutenfree_remission=bool(remit_off),
                shared_lever_remove_driver_restores_barrier=bool(flare_on and remit_off),
                note="celiac / microscopic / eosinophilic / autoimmune are antigen-dependent on this element "
                     "(driver removal -> remission -> barrier/villous recovery); the celiac absorptive magnitude "
                     "and timescale are [O] -- need an absorption layer. IBD's relapsing-remitting hysteresis "
                     "(active suppression to induce remission) is the distinct regime shown in ibd_relapsing_course.")

@lru_cache(maxsize=1)
def validate_d9():
    rc = ibd_relapsing_course(); br = ibd_neoplasia_bridge(); sl = immune_same_layer_readings()
    passed = bool(rc["relapsing_hysteresis"]
                  and rc["induction_needs_suppression_past_antigen_plus_spinodal"]
                  and rc["maintenance_threshold_lower_than_induction"]
                  and br["rr_rises_with_burden"] and br["anchor_hit"] and br["suppression_collapses_rr"]
                  and sl["shared_lever_remove_driver_restores_barrier"])
    return dict(relapsing_course=rc, neoplasia_bridge=br, same_layer=sl, passed=passed,
                treatment=("IBD -- SUPPRESS the inflammatory drive: an immunosuppressant / biologic raises the "
                           "suppression term past the induction threshold (antigen + spinodal) to flip an active flare "
                           "back to remission, then a LOWER maintenance dose holds it (the model's induction-vs-"
                           "maintenance asymmetry). Sustained remission restores the section-7 barrier scale, so the "
                           "model frames dysplasia surveillance and cancer risk on the SAME barrier step -- mucosal "
                           "healing lowers the crossing RR back toward baseline. For celiac / microscopic / eosinophilic "
                           "/ autoimmune the lever is removing the antigen / eosinophil / immune driver (the barrier and, "
                           "for celiac, the villous surface recover). Target directions [V]; absolute remission rates, "
                           "cancer incidence, and the celiac absorptive magnitude [O]."),
                grades=("C1 immune-layer Tier-3 cluster on ONE new R19-derived relapsing-inflammation primitive bridged "
                        "to the section-7 kernel; the relapsing-remitting hysteresis, the induction-vs-maintenance "
                        "asymmetry, and the burden->barrier->cancer continuity (closing the section-21 small-bowel "
                        "boundary) are [V] with the spinodal thresholds an exact [F] identity and the CRC anchor [L]; the "
                        "felt/affective component (`mind`, firewall), the absolute incidence, and the celiac absorptive "
                        "magnitude are [O] with stated obstacles"))


# ===========================================================================
#  D10 (section 23) -- C2: exocrine secretion + autodigestion layer (Tier-3, ONE
#  new R19-derived AUTOCATALYTIC primitive: autoactivation_threshold /
#  autodigestion_latched, plus a module-level secretory-reserve reading). The
#  pancreatic zymogen switch is the SAME R19 switch in the RUNAWAY (latching)
#  regime: acute pancreatitis is a TRANSIENT trigger that flips it past threshold
#  into a SELF-SUSTAINING active basin (irreversible autodigestion -- why there is
#  no pharmacological 'off-switch'; intervention must be PRE-threshold). Recurrent
#  attacks destroy acinar mass -> chronic pancreatitis -> EPI (exocrine
#  insufficiency), which the large secretory RESERVE delays until >~90% loss (the
#  cited steatorrhea threshold); PERT restores output. CF is gene-key (CFTR) ->
#  cross-ref disease_wp, while this package owns the ductal-secretion dynamics. New
#  layer; the absolute trigger/inhibitor and demand scales are [O] with obstacles.
# ===========================================================================
PANC_G           = 1.0      # [V] the zymogen R19 scale
PANC_INHIBITOR   = 0.20     # protective trypsin-inhibitor capacity (SPINK1); PRSS1 gain / SPINK1 loss lowers it
EPI_DEMAND       = 0.10     # digestive demand (model unit); steatorrhea below ~10% acinar output (DiMagno 1973 >90% loss) [L]-flavoured

def acute_pancreatitis_autocatalysis():
    """Acute pancreatitis = the zymogen R19 switch flipped into the autocatalytic runaway basin. (1) The
    activation THRESHOLD rises with the protective inhibitor (a PRSS1 gain / SPINK1 loss lowers it ->
    hereditary pancreatitis). (2) A supra-threshold transient trigger flips the switch AND LATCHES it -- the
    self-sustaining active state persists after the trigger is removed (irreversible autodigestion), while a
    sub-threshold trigger neither flips nor latches. (3) Intervention must be PRE-threshold: removing a
    sub-threshold trigger prevents the flip, but removing a supra-threshold trigger does NOT reverse the latch.
    (4) A strong inhibitor (> spinodal) abolishes the self-sustaining basin -> reversible (trypsin-inhibitor
    protection). Emergent from the R19 hysteresis; nothing fitted."""
    g, sp, inh = PANC_G, spinodal(PANC_G), PANC_INHIBITOR
    thr_rows = [(round(i, 2), round(autoactivation_threshold(g, i), 4)) for i in [0.0, 0.10, 0.20, 0.30]]
    thr_rises = all(thr_rows[k + 1][1] > thr_rows[k][1] for k in range(len(thr_rows) - 1))
    thr = autoactivation_threshold(g, inh)
    latch_rows = []                                              # (trigger, flipped, latched)
    for trig in [0.20, 0.40, thr - 0.02, thr + 0.02, 0.80, 1.20]:
        fl, lat = autodigestion_latched(g, trig, inh)
        latch_rows.append((round(trig, 3), bool(fl), bool(lat)))
    sub_safe   = bool(not latch_rows[0][2] and not latch_rows[1][2])      # sub-threshold: no latch
    supra_latches = bool(latch_rows[-1][2] and latch_rows[-2][2])          # supra-threshold: latched
    # pre-threshold intervention: sub-threshold removal -> never ON; supra-threshold removal -> stays ON
    pre_ok  = (not autodigestion_latched(g, thr - 0.05, inh)[1])           # below threshold: safe
    post_irrev = autodigestion_latched(g, thr + 0.10, inh)[1]              # above threshold: irreversible
    # strong inhibitor abolishes the latch (reversible)
    strong = [(round(i, 2), bool(autodigestion_latched(g, 1.5, i)[1])) for i in [0.20, 0.35, 0.45]]
    strong_reversible = bool(strong[0][1] and not strong[-1][1])
    return dict(threshold_rows=thr_rows, latch_rows=latch_rows, strong_inhibitor=strong,
                activation_threshold=round(thr, 4),
                columns="threshold: (inhibitor, trigger_threshold); latch: (trigger, flipped, latched); strong: (inhibitor, latched)",
                threshold_rises_with_inhibitor=bool(thr_rises),
                subthreshold_safe=sub_safe, suprathreshold_latches=supra_latches,
                pre_threshold_intervention_prevents=bool(pre_ok),
                post_threshold_irreversible=bool(post_irrev),
                strong_inhibitor_reversible=strong_reversible)

def _epi_adequacy(capacity, pert=0.0):
    """Module-level secretory-reserve reading: effective enzyme output = surviving acinar capacity +
    exogenous enzyme (PERT); maldigestion (steatorrhea) emerges only once output < the digestive demand."""
    output = max(0.0, float(capacity)) + max(0.0, float(pert))
    return output, bool(output >= EPI_DEMAND)

def chronic_pancreatitis_epi():
    """Recurrent acute autodigestion destroys acinar mass -> chronic pancreatitis -> exocrine pancreatic
    insufficiency (EPI). Because exocrine RESERVE is large, the secretory output stays adequate as capacity
    falls until it drops below the digestive demand at ~10% (the cited >90%-acinar-loss threshold for
    steatorrhea), then maldigestion emerges. PERT (exogenous enzyme) restores adequacy at very low capacity.
    The capacity-loss reading parallels the section-12 type-1 beta-capacity axis; the absolute demand scale is
    a model unit [O]."""
    cap_rows = []
    for cap in [1.0, 0.50, 0.20, 0.12, 0.10, 0.08, 0.05]:
        out, ok = _epi_adequacy(cap); cap_rows.append((round(cap, 2), bool(ok)))
    large_reserve = bool(cap_rows[0][1] and cap_rows[3][1] and not cap_rows[-1][1])   # adequate at 12%, fails at 5%
    monotone = True
    seen_fail = False
    for _, ok in cap_rows:
        if not ok: seen_fail = True
        if seen_fail and ok: monotone = False                  # once inadequate, stays inadequate as capacity falls
    pert_rows = [(round(p, 2), bool(_epi_adequacy(0.04, p)[1])) for p in [0.0, 0.05, 0.07, 0.10]]
    pert_restores = bool((not pert_rows[0][1]) and pert_rows[-1][1])
    return dict(capacity_rows=cap_rows, pert_rows=pert_rows,
                columns="capacity: (acinar_capacity, adequate); pert: (exogenous_enzyme, adequate)",
                large_reserve_steatorrhea_only_past_90pct_loss=large_reserve,
                adequacy_monotone_in_capacity=bool(monotone), pert_restores_adequacy=pert_restores)

@lru_cache(maxsize=1)
def validate_d10():
    ap = acute_pancreatitis_autocatalysis(); ce = chronic_pancreatitis_epi()
    passed = bool(ap["threshold_rises_with_inhibitor"] and ap["subthreshold_safe"]
                  and ap["suprathreshold_latches"] and ap["pre_threshold_intervention_prevents"]
                  and ap["post_threshold_irreversible"] and ap["strong_inhibitor_reversible"]
                  and ce["large_reserve_steatorrhea_only_past_90pct_loss"]
                  and ce["adequacy_monotone_in_capacity"] and ce["pert_restores_adequacy"])
    return dict(acute_autocatalysis=ap, chronic_epi=ce, passed=passed,
                treatment=("Acute pancreatitis -- the model predicts IRREVERSIBILITY past the autocatalytic "
                           "threshold, so the lever is PRE-threshold: remove the trigger (relieve the gallstone "
                           "obstruction, stop alcohol, lower triglycerides) BEFORE it crosses, and raise the "
                           "protective inhibitor (a strong-enough inhibitor abolishes the self-sustaining basin); "
                           "once established, only supportive care, because no parameter move reverses the latch. "
                           "Chronic pancreatitis / EPI -- the lever is REPLACEMENT: PERT (exogenous enzyme) restores "
                           "the secretory output above the digestive demand. Cystic fibrosis is gene-key (CFTR) -> "
                           "disease_wp owns the gene defect while this package owns the ductal-secretion dynamics. "
                           "Target directions [V]; absolute trigger/inhibitor thresholds, the demand scale, and "
                           "established-disease outcomes [O]."),
                grades=("C2 exocrine-layer Tier-3 cluster on ONE new R19-derived autocatalytic primitive (plus a "
                        "module-level secretory-reserve reading); the threshold-rises-with-inhibitor, the irreversible "
                        "supra-threshold latch (pre-threshold-only intervention), the strong-inhibitor reversibility, "
                        "and the large-reserve EPI (>90%-loss steatorrhea) + PERT rescue are [V] with the latch a forced "
                        "R19 hysteresis [F] and the reserve threshold [L]-flavoured; the absolute trigger/inhibitor and "
                        "demand scales and established-disease outcomes are [O] with stated obstacles"))


# ===========================================================================
#  D11 (section 24) -- C3: perfusion / vascular layer (Tier-3, ONE new
#  R19-derived tissue-VIABILITY primitive: perfusion_threshold /
#  viability_margin / tissue_viable). Tissue viability is the SAME R19 switch
#  SUSTAINED by perfusion: a VIABLE (+s) basin held up by oxygen delivery vs an
#  ischemic (-s) basin, with net drive h = perfusion - metabolic demand. Chronic
#  mesenteric ischemia is the post-prandial demand RISE eating the viability margin
#  ('intestinal angina'); acute mesenteric ischemia / ischemic colitis is the
#  viable->ischemic flip when perfusion drops below demand - spinodal, with a
#  SALVAGEABLE window (re-perfusion recovers) set by the bistable hysteresis -- the
#  established structural infarct (cell death) is out-of-model [O]. NAFLD / MASLD is
#  read as the metabolic-overlap part (the insulin-resistance gain loss reuses the
#  section-12 homeostat); the lipid-handling layer and the perfusion FIELD itself are
#  SEAMS to `circulatory` (cited, not re-emerged). GI bleeding / angiodysplasia are
#  sibling-owned vascular events (cited). New layer; absolute perfusion/demand scales
#  and the infarct timescale are [O] with stated obstacles.
# ===========================================================================
ISCH_G            = 1.0      # [V] the tissue-viability R19 scale
ISCH_PERF_FIXED   = 0.90     # a fixed splanchnic supply (chronic stenosis: limited but resting-adequate)
ISCH_DEMAND_ACUTE = 0.60     # an elevated (active, post-prandial) gut metabolic demand for the acute axis

def mesenteric_ischemia_axis():
    """Chronic mesenteric ischemia = 'intestinal angina'. On a FIXED (stenosed) splanchnic supply, the
    viability MARGIN = perfusion - (demand + spinodal) falls monotonically as the post-prandial metabolic
    DEMAND rises, crossing into deficit after a meal -- exactly the post-prandial pain that defines chronic
    mesenteric ischemia. The rescue threshold demand + spinodal rises with demand (same FORM as the gate /
    autoactivation threshold). Treatment (revascularization) RAISES perfusion so the margin stays positive
    across the demand range. Emergent from the R19 viability switch; nothing fitted."""
    g, sp = ISCH_G, spinodal(ISCH_G)
    rows = []                                                  # (demand, rescue_threshold, margin, ischemic?)
    for dem in [0.0, 0.20, 0.40, 0.60, 0.80]:
        thr = perfusion_threshold(g, dem); mar = viability_margin(g, ISCH_PERF_FIXED, dem)
        rows.append((round(dem, 2), round(thr, 4), round(mar, 4), bool(mar < 0)))
    margins = [m for _, _, m, _ in rows]
    margin_falls = all(margins[i + 1] < margins[i] - 1e-9 for i in range(len(margins) - 1))
    crosses_postprandial = bool(rows[0][3] is False and rows[-1][3] is True)   # adequate at rest, deficit at high demand
    # treatment: revascularization (raise perfusion) keeps the margin positive across the whole demand range
    perf_revasc = ISCH_PERF_FIXED + 2.0 * sp
    treat = [(round(d, 2), bool(viability_margin(g, perf_revasc, d) >= 0)) for d in [0.0, 0.40, 0.80]]
    revasc_restores = bool(all(ok for _, ok in treat))
    return dict(margin_rows=rows, treatment_revasc=treat, perfusion_fixed=ISCH_PERF_FIXED,
                columns="margin: (demand, rescue_threshold, viability_margin, ischemic); treatment: (demand, viable_after_revascularization)",
                margin_falls_as_demand_rises=bool(margin_falls),
                crosses_to_deficit_postprandially=crosses_postprandial,
                revascularization_restores_margin=revasc_restores)

def _ischemia_episode(perf_occlusion, perf_reperfuse, demand):
    """Acute episode in two phases (mirrors the autodigestion latch test, but the CONCLUSION is opposite):
    (1) drop perfusion to perf_occlusion from the viable rest -> does the tissue flip to the ischemic basin?
    (2) RESTORE perfusion to perf_reperfuse from that ischemic state -> does it recover? Returns
    (flipped_under_occlusion, recovered_on_reperfusion). In the R19 viability switch re-perfusion within the
    bistable window DOES recover (the salvageable ischemic window) -- the irreversible structural infarct is
    a one-way cell-death transition OUTSIDE this reversible double well (graded [O])."""
    s_occ = tissue_viable(ISCH_G, perf_occlusion, demand, infarcted=False)        # phase 1: occlusion
    s_rep = tissue_viable(ISCH_G, perf_reperfuse, demand, infarcted=(s_occ < 0))   # phase 2: re-perfuse
    return (s_occ < 0.0), (s_rep > 0.0)

def acute_ischemia_curve():
    """Acute mesenteric ischemia / ischemic colitis. At an elevated gut demand, sweeping perfusion DOWN, the
    tissue holds viable through its reserve and then flips DISCONTINUOUSLY to the ischemic basin once perfusion
    < demand - spinodal -- the abrupt acute infarction onset. The salvageable window: re-perfusing the ischemic
    tissue recovers it provided perfusion clears the rescue threshold demand + spinodal (the clinical urgency of
    timely revascularization). Past structural cell death the tissue is irreversibly infarcted -- a one-way
    transition the reversible R19 switch does not model (honest [O]). Emergent; nothing fitted."""
    g, sp, dem = ISCH_G, spinodal(ISCH_G), ISCH_DEMAND_ACUTE
    flip_thr = dem - sp                                        # below this perfusion: viable -> ischemic
    rescue_thr = dem + sp                                      # above this perfusion: ischemic -> viable (re-perfusion)
    rows = []                                                  # (perfusion, viable-from-viable?)
    for perf in [1.00, 0.80, flip_thr + 0.03, flip_thr - 0.03, 0.10, 0.0]:
        rows.append((round(perf, 3), bool(tissue_viable(g, perf, dem, infarcted=False) > 0)))
    flips_when_supply_fails = bool(rows[0][1] is True and rows[-1][1] is False)
    # salvageable window: occlude (below flip), then re-perfuse above the rescue threshold -> recovers
    occluded, reperf_recovers = _ischemia_episode(flip_thr - 0.05, rescue_thr + 0.05, dem)
    # re-perfuse only PARTIALLY (into the bistable window, below rescue threshold) -> stays ischemic (still salvageable region but not yet recovered)
    _occ2, partial_recovers = _ischemia_episode(flip_thr - 0.05, dem, dem)
    return dict(perfusion_rows=rows, flip_threshold=round(flip_thr, 4), rescue_threshold=round(rescue_thr, 4),
                reserve_window=round(2.0 * sp, 4),
                columns="perfusion: (perfusion, tissue_viable_from_viable)",
                flips_to_ischemic_when_supply_fails=flips_when_supply_fails,
                occlusion_flips=bool(occluded),
                reperfusion_recovers_within_window=bool(reperf_recovers),
                partial_reperfusion_stays_ischemic=bool(not partial_recovers))

def nafld_metabolic_overlap():
    """NAFLD / MASLD -- the in-scope METABOLIC-overlap part only. The insulin-resistance core is the SAME
    section-5/section-12 homeostat GAIN loss (reduced insulin sensitivity), so NAFLD's metabolic axis reuses the
    type-2 reading: lowering the insulin-action gain raises the fasting glucose operating point (compensated, not
    catastrophic -- the section-12 type-2 signature), and the model's lever is restoring insulin sensitivity (as
    type-2 diabetes) plus reducing lipid load. The lipid-HANDLING layer (hepatic steatosis magnitude, NASH
    fibrosis progression) is a SEAM to `circulatory` -- cited, not re-emerged ([O] here). Returns the reused
    type-2 gain-loss flag and the seam declaration."""
    # reuse the section-12 type-2 homeostat axis (gain loss -> compensated fasting rise)
    t2 = t2_axis()
    ir_compensated = bool(t2["sub_severe_across_sweep"] and t2["monotone_rise"])
    return dict(insulin_resistance_reuses_s12_type2_gain_loss=ir_compensated,
                lipid_handling_is_circulatory_seam=True,
                note="NAFLD/MASLD: the insulin-resistance overlap IS the section-12 type-2 homeostat gain loss "
                     "(restore insulin sensitivity + reduce lipid load is the lever); the lipid-handling layer and "
                     "NASH-fibrosis progression are a `circulatory` seam ([O], not re-emerged here).")

@lru_cache(maxsize=1)
def validate_d11():
    ma = mesenteric_ischemia_axis(); ac = acute_ischemia_curve(); nf = nafld_metabolic_overlap()
    passed = bool(ma["margin_falls_as_demand_rises"] and ma["crosses_to_deficit_postprandially"]
                  and ma["revascularization_restores_margin"]
                  and ac["flips_to_ischemic_when_supply_fails"] and ac["occlusion_flips"]
                  and ac["reperfusion_recovers_within_window"] and ac["partial_reperfusion_stays_ischemic"]
                  and nf["insulin_resistance_reuses_s12_type2_gain_loss"])
    return dict(chronic_mesenteric=ma, acute_ischemia=ac, nafld=nf, passed=passed,
                treatment=("Mesenteric ischemia -- RESTORE perfusion: the model's lever is raising the splanchnic "
                           "supply above the demand-dependent rescue threshold (demand + spinodal), i.e. "
                           "revascularization (angioplasty/stent or bypass) for chronic 'intestinal angina', and "
                           "URGENT revascularization for acute occlusion because re-perfusion recovers the tissue only "
                           "within the salvageable ischemic window -- past structural infarction (cell death) no "
                           "parameter move helps (resect dead bowel). Lowering the post-prandial demand (small "
                           "frequent meals) raises the margin symptomatically. NAFLD/MASLD -- the metabolic lever is "
                           "restoring insulin sensitivity (as type-2 diabetes) and reducing lipid load; the lipid-"
                           "handling and fibrosis layer is a `circulatory` seam. GI bleeding / angiodysplasia are "
                           "sibling-owned vascular events. Target directions [V]; absolute perfusion/demand scales, "
                           "the infarct timescale, and the lipid layer [O]."),
                grades=("C3 perfusion/vascular Tier-3 cluster on ONE new R19-derived tissue-viability primitive; the "
                        "post-prandial margin collapse (chronic 'intestinal angina'), the discontinuous viable->ischemic "
                        "flip past demand - spinodal, the salvageable-window re-perfusion recovery, and the NAFLD insulin-"
                        "resistance overlap (reusing the section-12 type-2 gain loss) are [V] with the threshold/window an "
                        "exact spinodal identity [F]; the absolute perfusion and demand scales, the structural-infarct "
                        "timescale (out-of-model irreversibility), and the hepatic lipid-handling/fibrosis layer "
                        "(`circulatory` seam) are [O] with stated obstacles; the perfusion FIELD itself is `circulatory`'s"))


# ===========================================================================
#  D12 (section 25) -- C4: hepatobiliary / bile layer (Tier-3, ONE new
#  R19-derived SUPERSATURATION/NUCLEATION primitive: nucleation_barrier /
#  supersaturation_drive / stone_nucleates). Cholesterol gallstone formation is the
#  SAME R19 switch read as a crystallization: a DISSOLVED (-s) basin vs a STONE (+s)
#  basin, driven by the cholesterol saturation index offset h = CSI - 1, with the R19
#  barrier g^2/4 as the classical-nucleation-theory free-energy barrier. Below the
#  spinodal the supersaturated bile is METASTABLE (no stone); past it nucleation is
#  spontaneous; and once a stone exists the dissolution HYSTERESIS (persists until
#  CSI < 1 - spinodal) is why bile-acid therapy works only on small/early stones and
#  cholecystectomy is definitive. Biliary stasis (impaired emptying = a B1 gate) and
#  cholecystitis (cystic-duct obstruction = a stuck B1 gate + a C1 flare) are CITED
#  seams, not re-emerged. Cirrhosis / hepatitis / cholestasis are sibling/`circulatory`
#  -owned; hepatic encephalopathy SEAMS to `mind` (only the ammonia source in scope).
#  New layer; absolute CSI scale, stone size, and the nucleation timescale are [O].
# ===========================================================================
BILE_G            = 1.0      # [V] the crystallization R19 scale (nucleation barrier g^2/4)

def cholelithiasis_axis():
    """Cholesterol cholelithiasis = the crystallization R19 switch driven past nucleation. Sweeping the
    cholesterol saturation index CSI UP from dissolved, the bile stays a clear (metastable) supersaturated
    solution and then nucleates a stone DISCONTINUOUSLY once CSI - 1 > spinodal(g) (the labile zone) -- so
    supersaturation is necessary but NOT sufficient, exactly the clinical picture (most supersaturated bile
    never stones). The nucleation barrier is the R19 basin barrier g^2/4. Emergent; nothing fitted."""
    g, sp = BILE_G, spinodal(BILE_G)
    nuc_csi = 1.0 + sp                                         # spontaneous-nucleation CSI threshold
    rows = []                                                  # (CSI, supersaturated?, stone?)
    for csi in [1.00, 1.20, nuc_csi - 0.02, nuc_csi + 0.02, 1.60, 2.00]:
        s = stone_nucleates(g, csi, seeded=False)
        rows.append((round(csi, 3), bool(supersaturation_drive(csi) > 0), bool(s > 0)))
    supersat_not_sufficient = bool(rows[1][1] is True and rows[1][2] is False)   # supersaturated yet metastable
    nucleates_past_spinodal = bool(rows[2][2] is False and rows[3][2] is True)
    return dict(csi_rows=rows, nucleation_csi=round(nuc_csi, 4), nucleation_barrier=round(nucleation_barrier(g), 4),
                columns="csi: (CSI, supersaturated, stone_nucleates)",
                supersaturation_metastable_not_sufficient=supersat_not_sufficient,
                nucleates_only_past_spinodal=nucleates_past_spinodal)

def gallstone_dissolution_hysteresis():
    """The dissolution HYSTERESIS and why it dictates therapy. An existing stone does NOT redissolve the moment
    bile becomes undersaturated: lowering CSI back below 1, the stone PERSISTS until CSI - 1 < -spinodal(g),
    i.e. CSI < 1 - spinodal -- a much harder target than merely correcting supersaturation. So bile-acid (UDCA)
    dissolution is feasible only for small / early / non-calcified stones (where the effective barrier is low
    enough to reach the dissolved basin), and CHOLECYSTECTOMY -- removing the supersaturated reservoir entirely
    -- is definitive. Emergent from the R19 hysteresis; nothing fitted."""
    g, sp = BILE_G, spinodal(BILE_G)
    dissolve_csi = 1.0 - sp                                    # below this CSI an existing stone redissolves
    rows = []                                                  # (CSI, stone persists?)
    for csi in [1.00, 0.80, dissolve_csi + 0.02, dissolve_csi - 0.02, 0.20]:
        s = stone_nucleates(g, csi, seeded=True)
        rows.append((round(csi, 3), bool(s > 0)))
    persists_below_saturation = bool(rows[0][1] is True and rows[1][1] is True)   # still a stone at CSI 1.0 and 0.8
    redissolves_only_far_below = bool(rows[2][1] is True and rows[3][1] is False)
    # the hysteresis gap: nucleate above 1+spinodal, dissolve only below 1-spinodal (width 2*spinodal)
    return dict(dissolution_rows=rows, dissolution_csi=round(dissolve_csi, 4),
                hysteresis_gap=round(2.0 * sp, 4),
                columns="dissolution: (CSI, stone_persists)",
                stone_persists_below_saturation=persists_below_saturation,
                redissolves_only_far_below_saturation=redissolves_only_far_below)

def biliary_seams():
    """The cited seams (not re-emerged). Biliary STASIS -- impaired gallbladder emptying (pregnancy, prolonged
    fasting, TPN, rapid weight loss) -- prolongs bile residence and promotes nucleation; mechanistically it is a
    B1-gate (gallbladder/cystic-duct control-loop) problem, and the time-to-nucleate magnitude is a Kramers-rate
    -over-the-barrier reading [O] (as in the carcinogen kernel). CHOLECYSTITIS is a stone obstructing the cystic
    duct -- a stuck B1 gate -- plus a C1 relapsing-inflammation flare on the gallbladder wall. BILIARY DYSKINESIA
    is a B1-gate ejection problem. Returns the seam declarations."""
    return dict(stasis_is_b1_gate_seam=True, cholecystitis_is_b1_gate_plus_c1_flare=True,
                dyskinesia_is_b1_gate=True, nucleation_time_is_kramers_rate=True,
                note="biliary stasis = B1 gallbladder/cystic-duct gate (residence -> nucleation, rate [O]); "
                     "cholecystitis = stuck B1 gate (stone obstruction) + C1 flare; biliary dyskinesia = B1 gate; "
                     "cirrhosis/hepatitis/cholestasis = sibling/`circulatory`; hepatic encephalopathy = `mind` "
                     "(only the metabolic ammonia source in scope here, the felt/cognitive effect behind the firewall).")

@lru_cache(maxsize=1)
def validate_d12():
    ch = cholelithiasis_axis(); dh = gallstone_dissolution_hysteresis(); sm = biliary_seams()
    passed = bool(ch["supersaturation_metastable_not_sufficient"] and ch["nucleates_only_past_spinodal"]
                  and dh["stone_persists_below_saturation"] and dh["redissolves_only_far_below_saturation"]
                  and sm["stasis_is_b1_gate_seam"] and sm["cholecystitis_is_b1_gate_plus_c1_flare"])
    return dict(cholelithiasis=ch, dissolution=dh, seams=sm, passed=passed,
                treatment=("Cholelithiasis -- LOWER the cholesterol saturation index (reduce biliary cholesterol "
                           "secretion: weight loss, statins/ezetimibe effects; or bile-acid therapy, UDCA), but the "
                           "dissolution hysteresis means lowering CSI below 1 is NOT enough -- the stone persists "
                           "until CSI < 1 - spinodal, so UDCA is feasible only for small / early / non-calcified "
                           "stones; CHOLECYSTECTOMY (removing the supersaturated reservoir) is definitive. RESTORE "
                           "gallbladder emptying (treat stasis -- the B1 gate) to prevent nucleation. Cholecystitis "
                           "is the stone obstructing the cystic duct (a stuck B1 gate) plus a C1 inflammatory flare -- "
                           "relieve the obstruction and suppress the flare. Cirrhosis / hepatitis / cholestasis are "
                           "sibling/`circulatory`-owned; hepatic encephalopathy's ammonia source is in scope (lactulose/"
                           "rifaximin lower it) while the felt/cognitive effect is `mind`'s. Target directions [V]; "
                           "absolute CSI/stone-size scales and the nucleation timescale [O]."),
                grades=("C4 hepatobiliary/bile Tier-3 cluster on ONE new R19-derived supersaturation/nucleation "
                        "primitive; the supersaturated-but-metastable zone (supersaturation necessary not sufficient), "
                        "the discontinuous nucleation past CSI = 1 + spinodal, and the dissolution hysteresis (an "
                        "existing stone persists until CSI = 1 - spinodal -- why UDCA works only on small/early stones "
                        "and cholecystectomy is definitive) are [V] with the nucleation/dissolution thresholds exact "
                        "spinodal identities [F]; the absolute CSI scale, stone size, and nucleation timescale (a "
                        "Kramers-rate-over-the-barrier reading), plus the cited B1-gate (stasis/cholecystitis/dyskinesia), "
                        "`circulatory` (lipid/hepatic-structural), and `mind` (felt biliary pain, hepatic-encephalopathy "
                        "cognition) seams, are [O] with stated obstacles"))


# ===========================================================================
#  D13 (section 26) -- C5: structural / mechanical layer (Tier-3, ONE new
#  R19-derived WALL-MECHANICS primitive: laplace_pressure / herniation_threshold /
#  wall_herniates). Colonic-wall integrity is the SAME R19 switch: an INTACT (-s)
#  basin vs a HERNIATED (+s) basin, driven by the segmental luminal pressure with the
#  R19 scale g_wall as the wall's structural strength. Laplace's law P = tension/radius
#  feeds the geometry: a low-fibre small-radius segment under a strong segmenting
#  contraction raises P past the herniation threshold spinodal(g_wall) -> a diverticulum;
#  a weaker wall (aging / collagen disorder) lowers the threshold. Treatment is the
#  geometry in reverse (fibre -> larger radius + softer segmenting -> lower P).
#  DiverticulITIS reuses the C1 flare (cited). Mechanical FIXED-block obstructions
#  (hernia / volvulus / intussusception / adhesions) are the counterpart the section-14
#  FUNCTIONAL (patent-lumen) module explicitly excludes (cited boundary; therapy often
#  surgical, out-of-model). New layer; absolute pressure/strength scales are [O].
# ===========================================================================
WALL_G            = 1.0      # [V] the colonic-wall structural-strength R19 scale
WALL_TENSION_HI   = 0.40     # segmenting-contraction tension (low-fibre, strong segmentation)
WALL_TENSION_LO   = 0.22     # softened segmenting tension (high-fibre, bulky stool)

def diverticular_pressure_axis():
    """Diverticular disease = wall herniation under segmental Laplace pressure. By Laplace P = tension/radius,
    a low-fibre diet (small hard stools -> a SMALL luminal radius gripped by STRONG high-pressure segmenting
    contractions) raises the wall pressure monotonically as the radius falls; once P exceeds the herniation
    threshold spinodal(g_wall) the intact wall buckles out at its weak points -> a diverticulum. Emergent from
    the R19 wall switch; nothing fitted."""
    g, thr = WALL_G, herniation_threshold(WALL_G)
    rows = []                                                  # (radius, Laplace P, herniates?)
    for r in [1.20, 0.90, 0.60, 0.45, 0.35]:
        p = laplace_pressure(WALL_TENSION_HI, r)
        rows.append((round(r, 2), round(p, 3), bool(wall_herniates(g, p) > 0)))
    pressures = [p for _, p, _ in rows]
    pressure_rises = all(pressures[i + 1] > pressures[i] for i in range(len(pressures) - 1))
    herniates_at_small_radius = bool(rows[0][2] is False and rows[-1][2] is True)
    return dict(radius_rows=rows, herniation_threshold=round(thr, 4),
                columns="radius: (luminal_radius, laplace_pressure, wall_herniates)",
                laplace_pressure_rises_as_radius_falls=bool(pressure_rises),
                herniates_at_low_fibre_small_radius=herniates_at_small_radius)

def wall_strength_axis():
    """Wall WEAKNESS lowers the herniation threshold. At a fixed segmental pressure that a normal wall
    withstands, a weaker wall (lower g_wall -- aging connective tissue, Ehlers-Danlos / Marfan collagen
    disorders) herniates, because its threshold spinodal(g_wall) is lower -- the age-rising diverticulosis
    prevalence and the connective-tissue-disorder association. Emergent; nothing fitted."""
    p_fixed = laplace_pressure(WALL_TENSION_HI, 0.89)          # a moderate segmental pressure a normal wall withstands
    rows = []                                                  # (wall strength g, threshold, herniates at p_fixed?)
    for gw in [1.30, 1.00, 0.70, 0.50]:
        rows.append((round(gw, 2), round(herniation_threshold(gw), 4), bool(wall_herniates(gw, p_fixed) > 0)))
    thresholds = [t for _, t, _ in rows]
    threshold_falls = all(thresholds[i + 1] < thresholds[i] for i in range(len(thresholds) - 1))
    weak_wall_herniates = bool(rows[0][2] is False and rows[-1][2] is True)     # strong holds, weak fails
    return dict(strength_rows=rows, pressure=round(p_fixed, 3),
                columns="strength: (wall_strength_g, herniation_threshold, herniates_at_fixed_pressure)",
                threshold_falls_as_wall_weakens=bool(threshold_falls),
                weaker_wall_herniates_at_same_pressure=weak_wall_herniates)

def fibre_treatment_and_boundary():
    """Treatment and the honest boundary. Treatment is the geometry in reverse: dietary FIBRE bulks the stool
    (a LARGER luminal radius) and softens the segmenting contractions (LOWER tension), dropping Laplace P back
    BELOW the herniation threshold -- so the same colon no longer out-pouches. DiverticulITIS (a formed pouch
    inflaming/obstructing) reuses the C1 relapsing-inflammation flare (cited). The mechanical FIXED-block
    obstructions -- hernia (incl. hiatal), volvulus, intussusception, adhesive obstruction -- are the structural
    counterpart the section-14 FUNCTIONAL motility module explicitly excludes (it keeps a patent lumen); their
    lever is relieving the block (often surgical, out-of-model). Returns the treatment flag + boundary."""
    g, thr = WALL_G, herniation_threshold(WALL_G)
    p_lowfibre  = laplace_pressure(WALL_TENSION_HI, 0.42)      # small radius + strong segmenting -> high P
    p_highfibre = laplace_pressure(WALL_TENSION_LO, 1.30)      # large radius + soft segmenting -> low P
    herniates_lowfibre  = bool(wall_herniates(g, p_lowfibre) > 0)
    herniates_highfibre = bool(wall_herniates(g, p_highfibre) > 0)
    fibre_prevents = bool(herniates_lowfibre and not herniates_highfibre)
    return dict(p_lowfibre=round(p_lowfibre, 3), p_highfibre=round(p_highfibre, 3), threshold=round(thr, 4),
                fibre_lowers_pressure_below_threshold=fibre_prevents,
                diverticulitis_is_c1_flare_seam=True, mechanical_block_is_s14_excluded_counterpart=True,
                note="treatment: fibre -> larger radius + softer segmenting -> Laplace P below the herniation "
                     "threshold (the same colon stops out-pouching). DiverticulITIS = C1 flare (cited). Mechanical "
                     "fixed-block obstruction (hernia/volvulus/intussusception/adhesions) = the section-14 patent-lumen "
                     "FUNCTIONAL module's structural counterpart (relieve the block, often surgical -- out-of-model).")

@lru_cache(maxsize=1)
def validate_d13():
    dp = diverticular_pressure_axis(); ws = wall_strength_axis(); ft = fibre_treatment_and_boundary()
    passed = bool(dp["laplace_pressure_rises_as_radius_falls"] and dp["herniates_at_low_fibre_small_radius"]
                  and ws["threshold_falls_as_wall_weakens"] and ws["weaker_wall_herniates_at_same_pressure"]
                  and ft["fibre_lowers_pressure_below_threshold"])
    return dict(diverticular_pressure=dp, wall_strength=ws, treatment_boundary=ft, passed=passed,
                treatment=("Diverticular disease -- LOWER the segmental pressure: dietary fibre bulks the stool "
                           "(larger luminal radius) and softens the high-pressure segmenting contractions (lower "
                           "tension), so by Laplace P = tension/radius the wall pressure drops back below the "
                           "herniation threshold and the colon stops out-pouching. DiverticulITIS adds a C1 "
                           "inflammatory flare on a formed pouch -- manage the inflammation (and the obstruction). "
                           "Mechanical FIXED-block obstruction (hernia incl. hiatal, volvulus, intussusception, "
                           "adhesions) is the structural counterpart the section-14 functional module excludes; its "
                           "lever is relieving the block, often surgical (out-of-model for parameter therapy). Target "
                           "directions [V]; absolute pressure and wall-strength scales [O]."),
                grades=("C5 structural/mechanical Tier-3 cluster on ONE new R19-derived wall-mechanics primitive; the "
                        "Laplace pressure rising as the luminal radius falls (low-fibre small stools), the discontinuous "
                        "herniation past P = spinodal(g_wall), the lower threshold of a weaker wall (aging / collagen "
                        "disorder), and the fibre treatment dropping P below threshold are [V] with the herniation "
                        "threshold an exact spinodal identity [F]; the absolute pressure and wall-strength scales are "
                        "[O], the diverticulITIS inflammation is a cited C1 flare seam, and the mechanical fixed-block "
                        "obstructions are the cited section-14 functional-module counterpart (surgical, out-of-model)"))


# ===========================================================================
#  D14 (section 29) -- REMAINING IN-SUBSTRATE perturbations (Tier-1 effort; NO
#  new primitive, NO sibling package required). Five readings that CLOSE the
#  in-substrate digestive Tier-1 surface (FUTURE_WORK sections 1A-1D), each
#  REUSING an already-validated module / primitive:
#    D14a  Dyssynergic defecation  -- the s16 gate read at the ANORECTAL OUTLET
#          (the achalasia mirror at the outlet) + s4 propulsion. MINE.
#    D14b  Hirschsprung (motility consequence) -- a SEGMENTAL aganglionic lesion
#          (absent oscillators in a distal segment) on the s1 emergence + s4
#          transport. The RET gene lesion is gene-key (disease_wp); the s1+s4
#          CONSEQUENCE is mine (imported-lesion seam).
#    D14c  MODY (trajectory) -- a TARGETED partial beta-secretory deficit on the
#          s12 homeostat -> a distinct, stable, REGULATED curve (NOT the T1
#          runaway). The PDX1/HHEX gene subtype is gene-key (disease_wp); the
#          s12 trajectory is mine.
#    D14d  Hepatic GSD type I (counter-reg consequence) -- a crippled hepatic
#          glycogen-buffer RELEASE arm (HHEX role) on the s6 counter-regulation
#          -> fasting hypoglycaemia + failed recovery. The G6PC / enzyme gene is
#          gene-key (disease_wp); the s6 consequence is mine.
#    D14e  Autoimmune gastritis -- the s22 relapsing-inflammation flare read
#          CORPUS-LOCALISED + the s7 barrier -> a regional barrier lesion + an
#          acid-output drop (achlorhydria), coupled. Common/acquired -> MINE
#          (HLA priors cross-ref).
#  All phenotypes EMERGE under wide sweeps; nothing is fitted. Felt components
#  and absorptive magnitudes are `mind` / absorption-layer [O] with obstacles.
# ===========================================================================
OUTLET_TONE     = 0.60      # [V] resting anorectal-outlet gate tone (tonically closed at rest)
DEFEC_RELAX     = 1.40      # [V] coordinated defecatory relaxation drive (RAIR + voluntary EAS relaxation; same scale as SWALLOW_RELAX)
MODY_BETA_FRAC  = 0.45      # PDX1/HHEX-linked targeted partial beta-secretory capacity (gene link [L]; disease_wp owns the subtype)
GSD_OUTPUT      = [1.00, 0.70, 0.50, 0.30, 0.10]   # hepatic free-glucose output fraction (G6PC deficiency cripples glycogenolysis + gluconeogenesis)
CORPUS_G        = 1.0       # [V] the gastric-corpus R19 scale (same switch as the s2 slow-wave / s7 barrier / s22 flare)
AIG_ANTIGEN     = 0.50      # a sustained anti-parietal autoimmune drive (corpus-restricted active disease)
AIG_KAPPA       = 0.5       # declared corpus burden -> barrier/parietal-mass coupling (absolute scale [O]; no clean AIG RR anchor)


# --------------------------------------------------------------------------- D14a  Dyssynergic defecation
def dyssynergic_defecation():
    """Dyssynergic defecation (anismus / pelvic-floor dyssynergia) = the SAME s16 gate primitive read at
    the ANORECTAL OUTLET -- the achalasia mirror at the outlet. The outlet gate is tonically closed and
    should open on a coordinated defecatory relaxation (the RAIR + voluntary external-sphincter relaxation
    against the propulsive push); in dyssynergia that relaxation FAILS (or the floor paradoxically
    contracts) so the gate stays closed and the bolus is RETAINED despite normal propulsion. Two routes
    reach the same stuck-closed outlet: a failing relaxation drive and a rising (paradoxical-contraction)
    outlet tone. CRUCIALLY the propulsive DRIVE is intact -- the lesion is the gate, not the drive (the
    falsifiable distinction from colonic inertia, a s14 DRIVE collapse)."""
    relax_route = []
    for frac in [1.00, 0.85, 0.70, 0.55, 0.40, 0.25, 0.10]:
        opened = gate_open(OUTLET_TONE, DEFEC_RELAX * frac)
        relax_route.append((round(frac, 2), bool(opened), 0.0 if opened else 1.0))
    tone_route = []
    for tone in [0.40, 0.70, 1.00, 1.30, 1.60]:
        opened = gate_open(tone, DEFEC_RELAX)
        tone_route.append((round(tone, 2), bool(opened), 0.0 if opened else 1.0))
    norm = gut_transport()
    propulsion_intact_pct = round(gut_transport() / norm * 100.0, 1)   # the DRIVE is normal (lesion is the outlet)
    return dict(relaxation_route=relax_route, paradoxical_tone_route=tone_route,
                propulsion_intact_pct=propulsion_intact_pct,
                columns="relax/tone: (knob, gate_open, retained_bolus)",
                clears_when_relaxation_competent=bool(relax_route[0][1]),
                retained_when_relaxation_fails=bool(not relax_route[-1][1]),
                retained_when_paradoxical_contraction=bool(not tone_route[-1][1]),
                lesion_is_gate_not_drive=bool(propulsion_intact_pct > 95.0))

@lru_cache(maxsize=1)
def validate_d14a():
    d = dyssynergic_defecation()
    passed = bool(d["clears_when_relaxation_competent"] and d["retained_when_relaxation_fails"]
                  and d["retained_when_paradoxical_contraction"] and d["lesion_is_gate_not_drive"])
    return dict(dyssynergic=d, passed=passed,
                treatment=("Dyssynergic defecation -- RETRAIN the coordinated relaxation (anorectal biofeedback): "
                           "restore the gate-open transition / lower the paradoxical outlet tone so the (intact) "
                           "propulsive push again clears the gate -- the same force-the-gate-open lever as achalasia, "
                           "at the outlet. Because the DRIVE is normal, the model predicts drive-raising agents "
                           "(stimulant laxatives / prokinetics) do NOT fix a closed outlet -- the falsifiable "
                           "distinction from colonic inertia (a s14 drive collapse, where they DO help). Direction "
                           "[V]; absolute evacuation fraction and biofeedback response rate [O]."),
                grades=("dyssynergic defecation reuses the s16 gate primitive at the anorectal outlet (no new "
                        "primitive): the bolus is retained when the outlet gate stays closed by either failing "
                        "relaxation or a paradoxical-contraction tone rise, while the propulsive drive stays intact "
                        "(the gate-not-drive distinction from colonic inertia) [V]; the felt straining/incomplete-"
                        "evacuation sensation is afferent-gain / `mind` and the absolute evacuation fraction is [O]"))


# --------------------------------------------------------------------------- D14b  Hirschsprung (motility consequence)
def _segmental_transport(aganglionic_frac, N=16):
    """Reuse the VALIDATED s4 transport mechanics with a PER-CELL density array (gut_transport's icc_density
    accepts a scalar OR a length-N vector with zero change to the scalar path): the DISTAL aganglionic_frac of
    cells carry NO oscillator (density 0 -> no contraction amplitude -> cannot propagate). Returns the net
    displacement, the fraction reaching the distal-most (deep aganglionic) cell, the final centre-of-mass, and
    the live/dead boundary cell."""
    dens = np.ones(N); k = int(round(N * (1.0 - aganglionic_frac))); dens[k:] = 0.0
    disp, c, pos, com0 = gut_transport(icc_density=dens, N=N, return_state=True)
    distal_most = float(c[-1] / c.sum())
    com_final = float((c * pos).sum() / c.sum())
    return disp, distal_most, com_final, k

def hirschsprung_segmental():
    """Hirschsprung disease (motility CONSEQUENCE) = a distal AGANGLIONIC segment has NO slow-wave oscillator
    (the s1-emergence reading: a segment whose gene lesion prevents oscillator emergence -> density 0), so the
    bolus cannot be propagated THROUGH it and is retained at/proximal to the transition zone (proximal
    dilatation -- the megacolon above the narrowed aganglionic distal segment). On the s4 mechanics: a NORMAL
    uniform gut advances the bolus to the distal end; an aganglionic distal segment blocks aboral clearance
    progressively (net displacement falls as the dead segment lengthens) and the deep aganglionic zone is never
    traversed (the distal-most cell stays empty; the COM is stuck at the transition zone). The RET-aganglionosis
    gene lesion itself is gene-key -> `disease_wp`; the s1-emergence + s4-consequence is owned here (an imported-
    lesion seam, cross-referenced both ways)."""
    N = 16
    r = gut_transport(N=N, return_state=True)
    disp_n = r[0]; cN = r[1]; posN = r[2]
    distal_n = float(cN[-1] / cN.sum()); com_n = float((cN * posN).sum() / cN.sum())
    rows = []
    for af in [0.15, 0.25, 0.40, 0.55]:
        disp, distal_most, com, k = _segmental_transport(af, N=N)
        rows.append((round(af, 2), k, round(disp, 3), round(distal_most, 4), round(com, 2)))
    disps = [row[2] for row in rows]
    monotone_block = all(disps[i] >= disps[i + 1] - 1e-9 for i in range(len(disps) - 1))
    distal_zone_never_traversed = all(row[3] < 0.05 for row in rows) and distal_n > 0.5
    com_stuck_at_transition = all(abs(row[4] - row[1]) < 1.0 for row in rows) and abs(com_n - (N - 1)) < 1.0
    return dict(normal=dict(net_disp=round(disp_n, 3), distal_most_frac=round(distal_n, 3), com_final=round(com_n, 2)),
                aganglionic_rows=rows,
                columns="aganglionic_rows: (aganglionic_fraction, transition_cell, net_disp, distal_most_frac, com_final)",
                transit_blocked_monotone_with_length=bool(monotone_block),
                distal_aganglionic_zone_never_traversed=bool(distal_zone_never_traversed),
                bolus_retained_proximal_at_transition=bool(com_stuck_at_transition))

@lru_cache(maxsize=1)
def validate_d14b():
    d = hirschsprung_segmental()
    passed = bool(d["transit_blocked_monotone_with_length"] and d["distal_aganglionic_zone_never_traversed"]
                  and d["bolus_retained_proximal_at_transition"])
    return dict(hirschsprung=d, passed=passed,
                treatment=("Hirschsprung disease -- the model lever is restoring an OSCILLATING distal segment: "
                           "clinically the aganglionic segment is resected and the ganglionic bowel pulled through "
                           "(surgical, out-of-model for parameter therapy). The model's CONSEQUENCE reading shows why "
                           "the obstruction is functional-at-a-fixed-segment (a patent but non-propagating distal "
                           "zone) and why the proximal bowel dilates above it. The RET-aganglionosis gene lesion is "
                           "owned by `disease_wp` (gene-key); the s1-emergence + s4 transport consequence is owned "
                           "here. Direction [V]; the gene lesion and surgical specifics [L]/`disease_wp` and [O]."),
                grades=("Hirschsprung reuses the s1 emergence + s4 transport (no new primitive) via a per-cell density "
                        "array (an aganglionic distal segment = absent oscillators): aboral transit is blocked "
                        "progressively as the dead segment lengthens, the deep aganglionic zone is never traversed, "
                        "and the bolus is retained at/proximal to the transition zone (proximal dilatation) [V]; the "
                        "RET gene lesion is gene-key -> `disease_wp` (cross-ref), and absolute transit time + the "
                        "surgical outcome are [O]"))


# --------------------------------------------------------------------------- D14c  MODY (trajectory)
def mody_trajectory():
    """MODY (maturity-onset diabetes of the young), a single-gene defect -- here a PDX1/HHEX-linked TARGETED,
    partial, FIXED beta-secretory-capacity deficit on the s12 homeostat. Unlike the s12 TYPE-1 axis (capacity
    depleted toward 0 -> an accelerating, catastrophic runaway past 11 mM with the setpoint lost), the MODY
    lesion settles a DISTINCT, STABLE, fully-REGULATED elevated curve: the meal load still returns to the
    (mildly raised) fasting fixed point and the peak stays bounded -- the monogenic, stable, often-mild
    phenotype. The PDX1/HHEX gene subtype is gene-key (-> `disease_wp`; the gene link is cited from DNA); the
    s12 trajectory is owned here."""
    f, pk, fin = _homeostat_disease(beta_frac=MODY_BETA_FRAC)
    returns = abs(fin - f) < 0.25                                   # settles back to the (elevated) fixed point
    t1_deep = t1_axis()["deepest_fasting"]                          # catastrophic runaway, for contrast
    sweep = []
    for bf in [0.55, 0.45, 0.35]:                                   # a small sweep AROUND the MODY operating point
        ff, pp, fn = _homeostat_disease(beta_frac=bf)
        sweep.append((round(bf, 2), round(ff, 2), round(pp, 2), round(fn, 2), bool(abs(fn - ff) < 0.25)))
    return dict(beta_frac=MODY_BETA_FRAC, fasting_mM=round(f, 2), peak_mM=round(pk, 2), final_mM=round(fin, 2),
                classification=classify_fpg(f), regulated_returns_to_setpoint=bool(returns),
                t1_deepest_fasting_for_contrast=t1_deep,
                distinct_from_t1_runaway=bool(f < 8.0 and pk < 11.5 and t1_deep > 10.0),
                operating_sweep=sweep, columns="operating_sweep: (beta_frac, fasting, peak, final, returns)",
                all_regulated_across_sweep=bool(all(row[4] for row in sweep)))

@lru_cache(maxsize=1)
def validate_d14c():
    d = mody_trajectory()
    passed = bool(d["regulated_returns_to_setpoint"] and d["distinct_from_t1_runaway"]
                  and d["all_regulated_across_sweep"])
    return dict(mody=d, passed=passed,
                treatment=("MODY -- the model lever RAISES the residual beta-secretory capacity (the secretory term), "
                           "NOT insulin sensitivity: the lesion is a secretory deficit, so a beta-cell secretagogue is "
                           "the model-consistent target (mirroring the classic sulfonylurea responsiveness of HNF1A/4A "
                           "MODY), distinct from the s12 type-2 insulin-resistance lever. The gene-specific mapping is "
                           "cited from DNA and owned by `disease_wp` (gene-key). Direction [V]; gene link [L]; absolute "
                           "glucose levels and the per-subtype therapy [O]/`disease_wp`."),
                grades=("MODY reuses the s12 homeostat (no new primitive): a targeted partial beta-secretory lesion "
                        "reproduces a DISTINCT, stable, regulated elevated curve (meal returns to the raised fixed "
                        "point, bounded peak) clearly distinct from the s12 type-1 catastrophic runaway [V]; the "
                        "PDX1/HHEX gene link is cited [L] and the subtype is gene-key -> `disease_wp` (cross-ref), with "
                        "absolute levels [O]"))


# --------------------------------------------------------------------------- D14d  Hepatic GSD-I (counter-reg consequence)
def hepatic_gsd_counterreg():
    """Hepatic glycogen storage disease type I (von Gierke, glucose-6-phosphatase deficiency) = the hepatic
    glycogen buffer (the HHEX role) cannot RELEASE free glucose -- glycogenolysis AND gluconeogenesis both fail
    to deliver glucose to the blood. On the s6 counter-regulation loop this is a crippled hepatic-output arm
    (P_basal + the glucagon-driven glycogenolytic output k_glu + the glycogen mobilisation k_draw all scaled
    down). The CONSEQUENCE: (1) FASTING -- a normal liver holds glucose at the setpoint, but with the output
    crippled the uptake outpaces hepatic production and glucose DRIFTS into hypoglycaemia (the hallmark fasting
    hypoglycaemia of GSD-I); (2) a hypoglycaemia CHALLENGE -- counter-regulation can no longer return glucose to
    the setpoint (the failed counter-reg). The G6PC / glycogen-enzyme gene is gene-key (-> `disease_wp`); the s6
    counter-reg consequence is owned here."""
    def _cripple(rf):
        Pp = dict(eng.HOMEOSTAT_P)
        Pp["P_basal"] = eng.HOMEOSTAT_P["P_basal"] * rf
        Pp["k_glu"]   = eng.HOMEOSTAT_P["k_glu"]   * rf
        Pp["k_draw"]  = eng.HOMEOSTAT_P["k_draw"]  * rf
        return Pp
    fasting = []                                                    # (1) fasting axis: hold at setpoint or drift hypoglycaemic?
    for rf in GSD_OUTPUT:
        _, G = eng.glucose_homeostat(G0=5.0, meal=None, T=80.0, Pp=_cripple(rf))
        fasting.append((round(rf, 2), round(float(G[-1]), 2), bool(float(G[-1]) < HYPO_THRESHOLD)))
    fast_levels = [row[1] for row in fasting]
    fasting_monotone = all(fast_levels[i] >= fast_levels[i + 1] - 1e-9 for i in range(len(fast_levels) - 1))
    fasting_crosses_hypo = bool(any(row[2] for row in fasting) and not fasting[0][2])   # normal holds, crippled crosses
    chall = []                                                      # (2) counter-reg challenge: recover from an insulin kick?
    for rf in [1.00, 0.50, 0.20]:
        _, G = eng.glucose_homeostat(G0=5.0, ins_kick=eng._pulse(2.0), T=60.0, Pp=_cripple(rf))
        chall.append((round(rf, 2), round(float(G.min()), 2), round(float(G[-1]), 2), bool(float(G[-1]) > 4.5)))
    counterreg_fails = bool(chall[0][3] and (not chall[-1][3]))                          # normal recovers, crippled fails
    return dict(fasting_axis=fasting, challenge_axis=chall,
                columns="fasting: (hepatic_output_frac, fasting_glucose_mM, hypoglycaemic); "
                        "challenge: (hepatic_output_frac, nadir_mM, final_mM, recovered)",
                fasting_drifts_hypoglycaemic_as_output_falls=bool(fasting_monotone and fasting_crosses_hypo),
                counter_regulation_fails_when_buffer_crippled=counterreg_fails)

@lru_cache(maxsize=1)
def validate_d14d():
    d = hepatic_gsd_counterreg()
    passed = bool(d["fasting_drifts_hypoglycaemic_as_output_falls"] and d["counter_regulation_fails_when_buffer_crippled"])
    return dict(hepatic_gsd=d, passed=passed,
                treatment=("Hepatic GSD-I -- the model lever is CONTINUOUS exogenous glucose supply (uncooked "
                           "cornstarch / frequent feeds / overnight drip): because the endogenous RELEASE arm is "
                           "broken, the model cannot restore hepatic output, so maintaining euglycaemia requires "
                           "supplying glucose from outside -- NOT a counter-regulation booster (glucagon is ineffective "
                           "exactly because the release arm is the lesion, a model-consistent prediction). The G6PC / "
                           "enzyme gene is owned by `disease_wp` (gene-key); the s6 counter-reg consequence is owned "
                           "here. Direction [V]; absolute fasting tolerance and feeding schedule [O]."),
                grades=("Hepatic GSD-I reuses the s6 counter-regulation (no new primitive): with the hepatic glycogen-"
                        "buffer RELEASE arm crippled, fasting glucose drifts into hypoglycaemia as the output falls and "
                        "a hypoglycaemia challenge can no longer be returned to the setpoint (the failed counter-reg) "
                        "[V]; the G6PC / enzyme gene is gene-key -> `disease_wp` (cross-ref), and absolute fasting "
                        "tolerance is [O]"))


# --------------------------------------------------------------------------- D14e  Autoimmune gastritis
def autoimmune_gastritis():
    """Autoimmune gastritis (anti-parietal-cell / anti-intrinsic-factor) = the s22 relapsing-inflammation flare
    read CORPUS-LOCALISED. A sustained autoimmune drive ignites a corpus flare past the R19 spinodal, whose
    cumulative burden lowers the s7 fate-stability scale of the corpus (a REGIONAL barrier lesion) AND -- the
    parietal-cell-loss consequence -- drops the acid output, which tracks the intact corpus/parietal scale
    (achlorhydria). The two are COUPLED (acid proportional to the corpus barrier). This is the corpus-restricted,
    achlorhydric signature that distinguishes it from s13 antral H. pylori gastritis (acid preserved / raised).
    Suppressing the autoimmune driver past the induction threshold reverts the flare and the corpus barrier +
    acid recover (the treatment direction). The downstream B12 / iron malabsorption (pernicious anaemia) is an
    absorption-layer [O]. Common / acquired (HLA-linked, not single-gene) -> MINE."""
    g, sp = CORPUS_G, spinodal(CORPUS_G)
    ignite = []                                                     # autoimmune-drive sweep: corpus barrier + acid output
    for ag in [0.0, 0.20, 0.35, 0.50, 0.65]:
        burden = flare_burden(g, ag, 0.0, in_flare=(ag > sp))
        g_corpus = inflammatory_barrier_scale(1.0, burden, AIG_KAPPA)
        acid = round(max(g_corpus, 0.0), 3)                         # acid output ~ intact corpus/parietal scale
        ignite.append((round(ag, 2), round(burden, 3), round(g_corpus, 3), acid))
    barrier_drops = bool(ignite[0][2] > 0.95 and ignite[-1][2] < 0.6)
    acid_tracks_barrier = bool(all(abs(row[2] - row[3]) < 1e-6 for row in ignite))  # acid coupled to corpus barrier
    suppress = []                                                   # treatment: suppress the driver -> recovery
    for supp in [0.0, 0.40, 0.60, sp + AIG_ANTIGEN + 0.01, 0.95]:
        s = flare_state(g, AIG_ANTIGEN, supp, in_flare=True)
        b = flare_burden(g, AIG_ANTIGEN, supp, in_flare=True)
        g_corpus = inflammatory_barrier_scale(1.0, b, AIG_KAPPA)
        suppress.append((round(supp, 3), round(s, 3), round(g_corpus, 3), bool(s < 0)))
    suppression_recovers = bool((not suppress[0][3]) and suppress[-1][3] and suppress[-1][2] > 0.95)
    return dict(ignition_axis=ignite, suppression_axis=suppress,
                columns="ignition: (autoimmune_drive, flare_burden, corpus_barrier, acid_output_rel); "
                        "suppression: (suppression, flare_state, corpus_barrier, remission)",
                corpus_barrier_and_acid_drop_on_ignition=barrier_drops,
                acid_output_coupled_to_corpus_barrier=acid_tracks_barrier,
                regional_corpus_restricted=True,
                suppression_recovers_corpus_and_acid=suppression_recovers)

@lru_cache(maxsize=1)
def validate_d14e():
    d = autoimmune_gastritis()
    passed = bool(d["corpus_barrier_and_acid_drop_on_ignition"] and d["acid_output_coupled_to_corpus_barrier"]
                  and d["suppression_recovers_corpus_and_acid"])
    return dict(autoimmune_gastritis=d, passed=passed,
                treatment=("Autoimmune gastritis -- the model lever SUPPRESSES the autoimmune driver (the s22 flare "
                           "lever): past the induction threshold the corpus flare reverts and the corpus barrier + acid "
                           "output recover. In practice the dominant management is REPLACING the malabsorption "
                           "consequence -- B12 (and iron) for the achlorhydria-driven pernicious anaemia -- which is an "
                           "out-of-model absorption-layer effect, and endoscopic surveillance (the achlorhydria-driven "
                           "ECL hyperplasia -> type-1 gastric carcinoid risk is the s21 out-of-kernel neuroendocrine "
                           "boundary, `disease_wp`). Direction [V]; absolute acid loss, the B12 magnitude, and the "
                           "carcinoid risk [O]."),
                grades=("autoimmune gastritis reuses the s22 relapsing-inflammation flare CORPUS-LOCALISED + the s7 "
                        "barrier (no new primitive): a sustained autoimmune drive drops the corpus barrier and the acid "
                        "output together (a regional, achlorhydric lesion distinct from antral H. pylori), the acid "
                        "output is coupled to the corpus barrier (parietal-mass loss), and driver suppression recovers "
                        "both [V]; the absolute acid loss, the B12 / iron malabsorption magnitude (absorption layer), "
                        "and the carcinoid boundary (`disease_wp`) are [O]"))


# --------------------------------------------------------------------------- D14 aggregator
@lru_cache(maxsize=1)
def validate_d14():
    a = validate_d14a(); b = validate_d14b(); c = validate_d14c(); d = validate_d14d(); e = validate_d14e()
    return dict(d14a_dyssynergic_defecation=a, d14b_hirschsprung=b, d14c_mody=c,
                d14d_hepatic_gsd=d, d14e_autoimmune_gastritis=e,
                passed=bool(a["passed"] and b["passed"] and c["passed"] and d["passed"] and e["passed"]),
                grades=("D14 closes the in-substrate digestive Tier-1 surface (FUTURE_WORK 1A-1D) REUSING already-"
                        "validated modules / primitives with NO new primitive and NO sibling package: D14a dyssynergic "
                        "defecation (s16 gate at the anorectal outlet + s4), D14b Hirschsprung motility consequence (s1 "
                        "emergence + s4 segmental aganglionosis; RET gene-key -> disease_wp), D14c MODY trajectory (s12 "
                        "homeostat targeted secretory lesion; PDX1/HHEX gene-key -> disease_wp), D14d hepatic GSD-I "
                        "counter-reg consequence (s6 crippled glycogen-buffer release; G6PC gene-key -> disease_wp), "
                        "D14e autoimmune gastritis (s22 corpus-localised flare + s7 barrier). Each phenotype EMERGES "
                        "under wide sweeps (never fitted); felt components are `mind` and absorptive magnitudes are an "
                        "absorption-layer [O] with stated obstacles; the three gene-key items are imported-lesion seams "
                        "cross-referenced both ways with `disease_wp`."))


@lru_cache(maxsize=1)
def validate():
    d1 = validate_d1(); d2 = validate_d2(); d3 = validate_d3(); d4 = validate_d4()
    d5 = validate_d5(); d6 = validate_d6(); d7 = validate_d7(); d8 = validate_d8()
    d9 = validate_d9(); d10 = validate_d10()
    d11 = validate_d11(); d12 = validate_d12(); d13 = validate_d13()
    d14 = validate_d14()
    return dict(d1_dysrhythmia_gastroparesis=d1, d2_diabetes=d2, d3_gastritis_ulcer=d3,
                d4_intestinal_motility=d4, d5_scattered_tier1=d5, d6_sphincter_gate=d6,
                d7_accommodation_reservoir=d7, d8_afferent_gain=d8,
                d9_immune_ibd=d9, d10_exocrine_pancreatitis=d10,
                d11_perfusion_ischemia=d11, d12_hepatobiliary_bile=d12, d13_structural_wall=d13,
                d14_remaining_in_substrate=d14,
                passed=bool(d1["passed"] and d2["passed"] and d3["passed"]
                            and d4["passed"] and d5["passed"] and d6["passed"]
                            and d7["passed"] and d8["passed"]
                            and d9["passed"] and d10["passed"]
                            and d11["passed"] and d12["passed"] and d13["passed"]
                            and d14["passed"]))
    return {"modules": ["D1 gastric dysrhythmia + gastroparesis (perturbs s2/s3)",
                        "D2 diabetes T1/T2 spectrum (perturbs s5/s6 homeostat)",
                        "D3 gastritis + peptic ulcer (reuses s7/s10 barrier kernel)",
                        "D4 intestinal motility / propulsion disorders (perturbs s4 peristalsis)",
                        "D5 scattered Tier-1 perturbations: dumping / reflux-esophagitis / "
                        "insulinoma+reactive-hypo / functional-dyspepsia-motility / SIBO-stasis",
                        "D6 sphincter-gate Tier-2 cluster (NEW gate primitive): GERD / achalasia / "
                        "esophageal-spasm / sphincter-of-Oddi (GERD<->achalasia = one gate, two failures)",
                        "D7 accommodation-reservoir Tier-2 reader (NEW compliance primitive): functional "
                        "dyspepsia post-prandial distress (impaired fundic accommodation -> premature meal "
                        "pressure / early satiation; the post-prandial-distress axis s15 left open)",
                        "D8 visceral afferent-gain Tier-2 cluster (NEW afferent primitive): IBS-C/-M/-D "
                        "(s14 transport bias sets the subtype) + functional abdominal pain (raised afferent "
                        "gain at normal motility); gain = 1/k diverges at the R19 spinodal = the s17 reservoir "
                        "yield (one curvature: sensory gain vs mechanical compliance); felt pain -> `mind` (firewall)",
                        "D9 immune-layer Tier-3 cluster (NEW relapsing-inflammation primitive, bridged to s7): IBD "
                        "(Crohn's / UC) relapsing-remitting hysteresis + induction-vs-maintenance dosing asymmetry + "
                        "the cumulative-burden -> s7-barrier -> colorectal/small-bowel neoplasia continuity (closes "
                        "the s21 small-bowel boundary); celiac / microscopic / eosinophilic / autoimmune share the "
                        "element and the remove-the-driver lever; felt component -> `mind` (firewall)",
                        "D10 exocrine-layer Tier-3 cluster (NEW autocatalytic zymogen primitive): acute pancreatitis = "
                        "a transient trigger latched past threshold into a self-sustaining runaway (irreversible "
                        "autodigestion -> pre-threshold-only intervention; strong inhibitor restores reversibility); "
                        "recurrent attacks -> chronic pancreatitis -> EPI delayed by the large secretory reserve "
                        "(>90%-loss steatorrhea) with PERT rescue; CFTR cross-ref disease_wp"],
            "principle": "Tier-1 disease = one perturbed parameter of a validated module; phenotype emerges, never fitted",
            "grades": "clinical thresholds [L] / emergent mechanism [V] / absolute population rates [O]"}

def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    if isinstance(o, tuple): return [_round(v) for v in o]
    return o

@lru_cache(maxsize=1)
def digest():
    s = json.dumps(_round(validate()), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = digest(); print(s); print("# disease sha256:", h)
    print("# D1 pass:", validate_d1()["passed"], " D2 pass:", validate_d2()["passed"],
          " D3 pass:", validate_d3()["passed"])
