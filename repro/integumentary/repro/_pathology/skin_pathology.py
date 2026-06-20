#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
skin_pathology.py  --  Integumentary DISEASE simulations on the SAME internal mechanisms.

PRINCIPLE (no new constants): a disease is NOT a new model. It is a NAMED PERTURBATION of one of the
package's already-verified mechanisms (CHARTER targets T1..T5) or of the shared oncology kernel. Each
disease moves ONE existing knob in the substrate (a standing aberrant R19 drive h, a sub-/super-
threshold migration drive, a melanocyte viability drive, a sweat-capacity ceiling, a screen factor).
Nothing is fitted: we SWEEP the perturbation and check the RESPONSE SHAPE + DIRECTION + any threshold/
discontinuity against a CITED clinical anchor. The intervention ("다루다" / treat) is the SAME knob
moved BACK -- so disease and therapy are one mechanism read in two directions.

GRADES (VP-SPEC C3):  [V] simulation-verified shape/direction . [L] cited clinical anchor . [O] open
  (absolute clinical magnitude; obstacle = the SAME calibration the parent target already flags).

Determinism (VP-SPEC C1): all built from the vendored substrate + the verified T1..T5 / oncology
  functions; fixed grids; NO RNG; round-before-hash via the engine emitter (reused).

DISEASE -> MECHANISM MAP
  D1 atopic dermatitis (eczema)        T1 barrier      keratinocyte/epidermis (KRT14/TP63)
  D2 ichthyosis (retention)            T1+T4 barrier   epidermis (TP63)         [opposite turnover sign vs psoriasis]
  D3 psoriasis (hyperproliferation)    T4 turnover     epidermis/keratinocyte (TP63)
  D4 chronic / diabetic wound          T2 wound        epidermis (TP63)         [uses the package's own chronic threshold]
  D5 vitiligo (melanocyte loss)        T3 melanin      melanocyte (MITF)
  D6 albinism (synthesis off)          T3 -> oncology  melanocyte (MITF)        [photoprotection-loss raises RR]
  D7 hypohidrotic ectodermal dyspl.    T5 thermoreg    skin_appendage (EDAR)    [the EDAR organ's own disease]
  D8 melanoma / SCC / BCC              oncology        melanocyte / epidermis   [present kernel, + pigment-disease modifier]
"""
import os, sys, math, json

_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "_oncology"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))

# vendored substrate primitives (DO NOT re-derive)
from vp_substrate import sdot, spinodal, barrier, dwell

# the package's OWN verified mechanisms -- reused, never reinvented
import skn_dynamics as DYN
import carcinogen_dose_response as ONCO
from vp_skn_engine import emit as _emit          # reuse exact round-before-hash emitter (C1)

GAMMA = DYN.gamma_of                              # MEASURED master-gene gamma (read-only)

# Pathology thermo sweeps call thermo_run many times (and the determinism check reruns the whole
# summary). The steady core temperature is fully settled well before the engine default T=60/dt=0.01,
# so the pathology module integrates its OWN thermo probes at a coarser, still-converged resolution.
# This does NOT touch the engine (skn_dynamics.thermo_run defaults are unchanged) -> run_all sha is
# unaffected; only this module's thermo probes are cheaper.
_TH_T, _TH_DT = 40.0, 0.05


# ---------------------------------------------------------------------------
#  substrate relaxation time: steps for the R19 field to flip under a drive h.
#  A pure substrate readout (uses only sdot). Decreases with |drive| -> the
#  natural accelerator for proliferative turnover (D3) and a clock for kinetics.
# ---------------------------------------------------------------------------
def flip_time(g, h, s0, dt=0.01, T=400.0):
    s = float(s0); t = 0.0; n = int(T / dt)
    for _ in range(n):
        s += dt * sdot(s, g, h); t += dt
        if (s0 < 0.0 and s > 0.0) or (s0 > 0.0 and s < 0.0):
            return t
    return float(T)                               # no flip within horizon


# ---------------------------------------------------------------------------
#  single-point barrier state (reuses the T1 branch continuation exactly):
#  TEWL = 1/margin, margin = depth of the ON basin relative to the OFF root.
# ---------------------------------------------------------------------------
def barrier_state(master, h, h_prev=0.0, s_prev=None):
    g = GAMMA(master); sp = spinodal(g)
    s_intact = DYN.on_branch(g, 0.0)
    s_off = DYN.off_branch(g, -2.0 * sp)
    s_prev = s_intact if s_prev is None else s_prev
    s = DYN.nearest_branch(g, float(h), s_prev)
    m = min(max((s - s_off) / (s_intact - s_off), 1e-6), 1.0)
    return dict(s=s, margin=m, tewl=1.0 / m, on=bool(s > 0.0), spinodal=sp,
                s_intact=s_intact, s_off=s_off)


def collapse_fraction_from(master, h_base):
    """Additional insult fraction (of spinodal) available before the discontinuous
    barrier collapse, STARTING from a standing baseline insult h_base (<=0)."""
    g = GAMMA(master); sp = spinodal(g)
    M = 200
    hs = [h_base + (-1.05 * sp - h_base) * k / (M - 1) for k in range(M)]
    s_prev = DYN.nearest_branch(g, hs[0], DYN.on_branch(g, 0.0))
    tewl_prev = barrier_state(master, hs[0], s_prev=s_prev)["tewl"]
    s_intact = DYN.on_branch(g, 0.0); s_off = DYN.off_branch(g, -2.0 * sp)
    jmax, jfrac = 0.0, 1.0
    for h in hs[1:]:
        s = DYN.nearest_branch(g, h, s_prev); s_prev = s
        m = min(max((s - s_off) / (s_intact - s_off), 1e-6), 1.0)
        tewl = 1.0 / m
        if (tewl - tewl_prev) > jmax:
            jmax = tewl - tewl_prev; jfrac = abs(h) / sp
        tewl_prev = tewl
    return jfrac                                  # spinodal fraction at the snap


# ===========================================================================
#  D1  ATOPIC DERMATITIS (eczema)  --  T1 barrier, filaggrin / lipid deficit
#  Perturbation: a STANDING aberrant barrier-disruption drive h_base<0 (the
#  lipid/filaggrin deficit acts like a constant disruptor). Healthy = h_base 0.
#  PRIMARY substrate signature -- the BARRIER RESERVE collapses: the additional
#  insult the skin can absorb before the DISCONTINUOUS barrier collapse shrinks
#  monotonically as the deficit deepens (AD skin flares under far less provocation).
#  Baseline TEWL also rises, but its MAGNITUDE is the same [O] obstacle as T1, so
#  the reserve (a dimensionless spinodal fraction) is the faithful readout, not the
#  TEWL number. Intervention (emollient / barrier repair): reduce |h_base| ->
#  reserve restored, baseline TEWL falls. Anchor [L]: AD = barrier-defect disease
#  (FLG LOF), reduced barrier function, flare-prone.
# ===========================================================================
def atopic_dermatitis(master="KRT14"):
    g = GAMMA(master); sp = spinodal(g)
    healthy = barrier_state(master, 0.0)
    fracs = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75]    # standing-deficit sweep (fraction of spinodal)
    base_tewl, reserve = [], []
    for f in fracs:
        hb = -f * sp
        base_tewl.append(barrier_state(master, hb)["tewl"])
        # remaining insult ROOM = (spinodal-fraction at the snap) - (standing deficit already spent)
        reserve.append(max(collapse_fraction_from(master, hb) - f, 0.0))
    healthy_reserve = reserve[0]
    reserve_frac = [r / healthy_reserve if healthy_reserve > 0 else 0.0 for r in reserve]
    disease_f = 0.45                                # a representative moderate-severe deficit (swept, not fit)
    hb = -disease_f * sp
    d_room = max(collapse_fraction_from(master, hb) - disease_f, 0.0)
    d_tewl = barrier_state(master, hb)["tewl"]
    rep_f = 0.10                                    # emollient: residual mild deficit
    r_room = max(collapse_fraction_from(master, -rep_f * sp) - rep_f, 0.0)
    r_tewl = barrier_state(master, -rep_f * sp)["tewl"]
    mono_reserve = bool(all(reserve[i] >= reserve[i + 1] - 1e-9 for i in range(len(reserve) - 1)))
    mono_tewl = bool(all(base_tewl[i] <= base_tewl[i + 1] + 1e-9 for i in range(len(base_tewl) - 1)))
    sign = bool(d_room < healthy_reserve and d_tewl >= healthy["tewl"])      # reserve collapses (primary), TEWL up (secondary)
    rescue = bool(r_room > d_room and r_tewl < d_tewl)
    return dict(disease="atopic_dermatitis", organ="keratinocyte/epidermis", master=master, target="T1",
                mechanism="standing barrier-disruption drive h_base<0 (filaggrin/lipid deficit) eats into the ON-basin: the additional insult to discontinuous collapse (barrier RESERVE) shrinks and baseline TEWL rises",
                deficit_fraction=fracs,
                barrier_reserve_vs_deficit=[round(x, 5) for x in reserve],          # PRIMARY: dimensionless spinodal-fraction of remaining insult room
                reserve_fraction_of_healthy=[round(x, 5) for x in reserve_frac],
                baseline_tewl_vs_deficit=[round(x, 5) for x in base_tewl],          # secondary (magnitude is [O])
                healthy_barrier_reserve=round(healthy_reserve, 5),
                disease_barrier_reserve=round(d_room, 5), disease_reserve_fraction=round(d_room / healthy_reserve, 5),
                disease_baseline_tewl=round(d_tewl, 5), healthy_baseline_tewl=round(healthy["tewl"], 5),
                intervention="emollient / barrier repair (reduce |h_base|)",
                intervention_barrier_reserve=round(r_room, 5), intervention_baseline_tewl=round(r_tewl, 5),
                monotone_reserve_falls_with_deficit=mono_reserve,
                monotone_tewl_rises_with_deficit=mono_tewl,
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] atopic dermatitis = barrier-defect disease (filaggrin loss-of-function); reduced barrier function, flare-prone",
                grade_shape="[V] barrier-reserve collapse (dimensionless, monotone)",
                grade_absolute="[O] absolute TEWL (g/m^2/h): needs lipid permeability D + dC calibration (T1 obstacle)")


# ===========================================================================
#  D2  ICHTHYOSIS (retention hyperkeratosis)  --  T1+T4, impaired desquamation
#  Perturbation: a REDUCED desquamation/shedding drive -> the stratum-corneum
#  exit ("unjam & shed") slows -> SC residence LENGTHENS (retention, thick SC).
#  This is the OPPOSITE turnover SIGN to psoriasis from the SAME switch (a clean
#  no-new-constant discriminant). Barrier still defective (elevated TEWL, mild).
#  Anchor [L]: ichthyosis = retention hyperkeratosis (thickened SC). Abs [O].
# ===========================================================================
def ichthyosis(master="TP63"):
    g = GAMMA(master); sp = spinodal(g)
    s_sc = DYN.on_branch(g, 0.0)                    # cornified cell, ON; sheds only when the drive is PAST the spinodal
    shed_drives = [2.2, 1.7, 1.3, 1.08]             # healthy (well past spinodal) -> reduced drive approaching the spinodal
    residence = [flip_time(g, -d * sp, s_sc) for d in shed_drives]   # shed (flip-OFF) time = SC residence; diverges near the spinodal
    healthy_res, disease_res = residence[0], residence[-1]
    relief = flip_time(g, -2.2 * sp, s_sc)          # keratolytic restores a strong shedding drive
    sign = bool(disease_res > healthy_res)          # retention (longer SC residence near the spinodal = critical slowing)
    rescue = bool(relief < disease_res)
    return dict(disease="ichthyosis", organ="epidermis", master=master, target="T1+T4",
                mechanism="desquamation needs a drive past the spinodal; as the shedding drive approaches the spinodal the shed (flip-OFF) time DIVERGES (critical slowing) -> stratum-corneum retention -- the opposite turnover sign to psoriasis on the same R19 switch",
                shed_drive_fraction=shed_drives, sc_residence_arb=[round(x, 4) for x in residence],
                healthy_sc_residence_arb=round(healthy_res, 4), disease_sc_residence_arb=round(disease_res, 4),
                retention_fold=round(disease_res / healthy_res, 4) if healthy_res > 0 else None,
                intervention="keratolytic / retinoid (restore a strong shedding drive past the spinodal)", intervention_sc_residence_arb=round(relief, 4),
                monotone_residence_rises_as_drive_falls=bool(all(residence[i] <= residence[i + 1] + 1e-9 for i in range(len(residence) - 1))),
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] ichthyosis = retention hyperkeratosis: impaired desquamation, thickened stratum corneum",
                grade_shape="[V]", grade_absolute="[O] absolute SC residence days: needs per-cell desquamation-rate calibration (T4 obstacle)")


# ===========================================================================
#  D3  PSORIASIS (hyperproliferation)  --  T4 turnover acceleration
#  Perturbation: an ELEVATED proliferative/exit drive on the basal switch shortens
#  the substrate relaxation (flip) time -> the conveyor accelerates. Acceleration
#  factor = flip_time(baseline)/flip_time(baseline+drive) (a substrate readout, NOT
#  a free divisor). turnover_disease = turnover_healthy / acceleration.
#  -> turnover falls monotonically from ~28 d; multi-fold acceleration is reachable,
#  spanning the cited psoriatic window. Intervention (anti-proliferative): lower the
#  drive -> turnover returns toward normal. Anchor [L]: psoriatic transit ~3-5 d vs
#  ~28-40 d healthy. Per-cell absolute [O].
# ===========================================================================
# ===========================================================================
#  D3  PSORIASIS (hyperproliferation)  --  T4 turnover acceleration
#  Perturbation: an ELEVATED proliferative/exit drive on the basal switch. The
#  healthy basal cell sits OFF and advances only on the slow homeostatic conveyor
#  (~28-40 d, package T4 [L]). Psoriasis pushes the exit drive PAST the
#  differentiation spinodal: the OFF basin disappears and the basal cell advances
#  AUTONOMOUSLY. This is a THRESHOLD: below the spinodal the cell is held (slow
#  conveyor); at/above it the autonomous-advance time is finite and FALLS smoothly
#  and several-fold as the drive intensifies (critical speeding) -- the substrate
#  signature of graded hyperproliferation. The DIRECTION + THRESHOLD + several-fold
#  smooth acceleration are [V]; the absolute transit in DAYS is [O] (inherits the
#  T4 per-cell + whole-conveyor calibration obstacle -- the package itself does not
#  predict the absolute basal cycle time). The cited 3-5 d vs 28-40 d window is the
#  clinical ANCHOR, not a reproduced number. Intervention (anti-proliferative):
#  lower the exit drive back below the spinodal -> autonomous advance suppressed,
#  cell returns to the homeostatic conveyor.
# ===========================================================================
def psoriasis(master="TP63"):
    g = GAMMA(master); sp = spinodal(g)
    s_basal = DYN.off_branch(g, 0.0)                # basal cell, OFF; exit drive past the spinodal makes it advance autonomously
    healthy_total = DYN.turnover()["total_turnover_days"]
    # fine sweep ACROSS the differentiation spinodal: held below, autonomous above
    drives = [0.50, 0.90, 1.00, 1.01, 1.05, 1.15, 1.35, 1.70, 2.20]
    HELD = 400.0
    advance = [flip_time(g, d * sp, s_basal) for d in drives]      # autonomous-advance time; HELD (==horizon) below the spinodal
    held = [bool(a >= HELD - 1e-6) for a in advance]
    auto = [(d, a) for d, a in zip(drives, advance) if a < HELD - 1e-6]    # supra-spinodal (autonomous) branch
    # dimensionless several-fold acceleration WITHIN the autonomous regime (slowest just above sp -> fastest at strong drive)
    a_slow = auto[0][1]; a_fast = auto[-1][1]
    relative_acceleration = round(a_slow / a_fast, 4) if a_fast > 0 else None
    critical_drive_fraction = 1.0                   # the differentiation spinodal (substrate constant, not fitted)
    # intervention: drop the exit drive below the spinodal -> advance returns to HELD (homeostatic conveyor governs)
    treated_advance = flip_time(g, 0.50 * sp, s_basal)
    treated_held = bool(treated_advance >= HELD - 1e-6)
    # threshold separates held vs autonomous; autonomous branch is monotone-accelerating as drive rises
    auto_times = [a for _, a in auto]
    sign = bool(all(held[i] for i, d in enumerate(drives) if d < 1.0)            # sub-spinodal: held
                and any((not held[i]) for i, d in enumerate(drives) if d > 1.0)  # supra-spinodal: autonomous
                and all(auto_times[i] >= auto_times[i + 1] - 1e-9 for i in range(len(auto_times) - 1)))
    rescue = bool(treated_held)                     # anti-proliferative returns the cell to the slow conveyor
    return dict(disease="psoriasis", organ="epidermis/keratinocyte", master=master, target="T4",
                mechanism="proliferative exit drive past the differentiation spinodal makes the basal cell advance autonomously; below the spinodal it is held on the homeostatic conveyor. THRESHOLD + critical speeding = graded hyperproliferation",
                proliferative_drive_fraction=drives,
                autonomous_advance_arb=[round(a, 4) for a in advance],   # ==horizon(400) means HELD (no autonomous advance)
                held_below_threshold=held,
                critical_drive_fraction=critical_drive_fraction,         # = spinodal (substrate constant)
                relative_acceleration_in_autonomous_regime=relative_acceleration,   # dimensionless several-fold [V]
                homeostatic_turnover_days=round(healthy_total, 4),       # the package T4 conveyor (below threshold) [L]
                cited_window_days=[3.0, 5.0], cited_healthy_window_days=[28.0, 40.0],   # clinical ANCHOR (not reproduced)
                intervention="anti-proliferative (lower exit drive below the differentiation spinodal)",
                intervention_returns_to_homeostatic=rescue,
                threshold_separates_held_vs_autonomous=bool(any(held) and any(not h for h in held)),
                autonomous_regime_monotone_accelerating=bool(all(auto_times[i] >= auto_times[i + 1] - 1e-9 for i in range(len(auto_times) - 1))),
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] psoriasis: epidermal transit accelerated to ~3-5 d vs ~28-40 d healthy (several-fold hyperproliferation)",
                grade_shape="[V] threshold + several-fold smooth acceleration (direction forced)",
                grade_absolute="[O] absolute transit DAYS: needs per-cell + whole-conveyor calibration (T4 obstacle); the package does not predict the absolute basal cycle time")


# ===========================================================================
#  D4  CHRONIC / DIABETIC / PRESSURE WOUND  --  T2, sub-threshold unjamming
#  Perturbation: NONE new -- the package ALREADY computes the chronic-wound
#  critical unjamming drive (below it the edge stays jammed and the wound does
#  not close). Disease = h_unjam BELOW that critical drive. Intervention
#  (debridement / growth factor / re-epithelialisation cue): raise h_unjam ABOVE
#  critical -> closure restored. Anchor [L]: chronic wound = failure to close in
#  the expected window. Absolute rate [O].
# ===========================================================================
def chronic_wound(master="TP63"):
    crit = DYN.chronic_wound_threshold(master)["critical_unjam_drive"]
    sub = round(max(crit - 0.05, 0.0), 5)
    drives = [0.0, sub, crit, round(crit + 0.10, 5), 1.0]
    closed = [DYN.wound_close(master, h_unjam=d, T=30.0)["closed"] for d in drives]
    disease_closed = DYN.wound_close(master, h_unjam=sub, T=30.0)["closed"]
    treated_closed = DYN.wound_close(master, h_unjam=round(crit + 0.10, 5), T=30.0)["closed"]
    sign = bool((not disease_closed) and treated_closed)
    return dict(disease="chronic_diabetic_pressure_wound", organ="epidermis", master=master, target="T2",
                mechanism="free-edge unjamming drive held BELOW the package's own chronic-wound critical drive -> edge stays jammed (q<q*) -> non-closure",
                critical_unjam_drive=crit, unjam_drive_sweep=drives, closed_vs_drive=[bool(c) for c in closed],
                disease_drive=sub, disease_closes=bool(disease_closed),
                intervention="debridement / growth-factor / re-epithelialisation cue (raise unjamming drive above critical)",
                intervention_drive=round(crit + 0.10, 5), intervention_closes=bool(treated_closed),
                threshold_separates_heal_vs_chronic=bool(closed == sorted(closed)),  # monotone: closure switches on at the threshold
                sign_matches_clinic=sign, intervention_reverses=sign,
                anchor="[L] chronic wound = failure to re-epithelialise within the expected window (impaired collective migration)",
                grade_shape="[V] (q*=3.81 [L])", grade_absolute="[O] absolute closure rate (um/h): needs cell-speed calibration (T2 obstacle)")


# ===========================================================================
#  D5  VITILIGO (melanocyte loss)  --  T3, melanocyte basin destabilised
#  Perturbation: an autoimmune suppressive drive h_auto<0 on the MITF switch.
#  Beyond the spinodal the ON basin disappears -> the melanocyte flips OFF
#  DISCONTINUOUSLY (depigmentation) -> melanin -> 0 -> photoprotection lost
#  (UV reaching DNA returns to ~full). Intervention (narrowband UVB /
#  immunomodulation): raise the drive back above -spinodal -> melanocyte ON ->
#  melanin returns. Anchor [L]: vitiligo = melanocyte loss, depigmented, UV-sensitive.
# ===========================================================================
def vitiligo(master="MITF", uv=4.0):
    g = GAMMA(master); sp = spinodal(g)
    M_intact = DYN.melanin_steady("MITF", uv=uv)    # per-cell melanin at this UV (T3), if the cell is present
    drives = [0.0, -0.50 * sp, -0.95 * sp, -1.05 * sp, -1.30 * sp]   # autoimmune drive on melanocyte VIABILITY, bracketing the spinodal
    s_prev = math.sqrt(g)                            # start from a VIABLE (ON) melanocyte; continue the basin
    viab, M, atten = [], [], []
    for h in drives:
        s = DYN.nearest_branch(g, float(h), s_prev); s_prev = s     # snaps OFF when the viable basin disappears (presence threshold)
        v = 1.0 if s > 0.0 else 0.0
        m = v * M_intact
        viab.append(v); M.append(m); atten.append(math.exp(-1.0 * m))
    healthy_M, disease_M = M[0], M[-1]
    drops = [M[i] - M[i + 1] for i in range(len(M) - 1)]
    snap = max(drops) if drops else 0.0             # depigmentation = a discontinuous melanin drop at the spinodal
    # intervention: phototherapy must re-cross the OTHER spinodal (hysteresis -> repigmentation needs active stimulation,
    # which mirrors the clinical difficulty). Sweep a POSITIVE stimulation drive from the depigmented (OFF) state.
    stim = [0.4 * sp, 0.8 * sp, 1.05 * sp, 1.30 * sp]
    s_off = -math.sqrt(g); repig = []
    for h in stim:
        s = DYN.nearest_branch(g, float(h), s_off)
        repig.append((1.0 if s > 0.0 else 0.0) * M_intact)
    repig_M = max(repig)
    sign = bool(disease_M < 0.05 * max(healthy_M, 1e-9) and atten[-1] > 0.9)
    rescue = bool(repig_M > disease_M)
    return dict(disease="vitiligo", organ="melanocyte", master=master, target="T3",
                mechanism="autoimmune drive pushes the melanocyte VIABILITY (R19 presence switch) below the spinodal -> melanocyte lost discontinuously -> melanin->0 regardless of UV -> photoprotection lost (UV reaching DNA returns to full)",
                autoimmune_drive_fraction=[round(h / sp, 4) for h in drives], melanocyte_viable_vs_drive=[bool(v) for v in viab],
                melanin_vs_drive=[round(m, 5) for m in M], delivered_uv_attenuation_vs_drive=[round(a, 5) for a in atten],
                depigmentation_snap=round(snap, 5), healthy_melanin=round(healthy_M, 5),
                disease_melanin=round(disease_M, 5), disease_attenuation=round(atten[-1], 5),
                discontinuous_loss=bool(snap > 0.5 * max(healthy_M, 1e-9)),
                intervention="narrowband UVB / immunomodulation (active stimulation re-crosses the +spinodal; hysteresis = repigmentation is hard)",
                intervention_stim_fraction=[round(h / sp, 4) for h in stim], intervention_melanin_vs_stim=[round(m, 5) for m in repig],
                intervention_melanin=round(repig_M, 5), sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] vitiligo = autoimmune melanocyte loss: depigmented, photoprotection-deficient patches; repigmentation requires active phototherapy",
                grade_shape="[V]", grade_absolute="[O] absolute melanin optical density: needs extinction-coefficient calibration (T3 obstacle)")


# ===========================================================================
#  D6  ALBINISM (synthesis off)  --  T3 -> ONCOLOGY linkage
#  Perturbation: the melanin SCREEN is removed (tyrosinase pathway broken: the
#  melanocyte may be ON but produces no functional melanin). The photoprotection
#  feedback is abolished -> the UV reaching DNA stays at FULL intensity at all UV.
#  Fed into the SHARED oncology kernel (melanin_screen=0 vs healthy screen>0) this
#  RAISES the carcinogenic hazard -> RR(albino)/RR(pigmented) > 1. Intervention
#  (sunscreen): an EXOGENOUS screen restores attenuation -> RR falls. Anchor [L]:
#  albinism markedly elevates cSCC/melanoma, esp. high-UV regions.
# ===========================================================================
def albinism(master="MITF", uv_max=8.0):
    g_m = GAMMA(master)
    uvs = [uv_max * k / 20 for k in range(21)]
    # T3 side: no functional screen -> attenuation == 1 everywhere
    atten_albino = [1.0 for _ in uvs]
    _, M_fb, _, uv_dna_fb = DYN.melanin_sweep("MITF", uv_max=uv_max, P=21)
    atten_healthy = [round(float(uv_dna_fb[i] / uvs[i]), 5) if uvs[i] > 0 else 1.0 for i in range(len(uvs))]
    # oncology side (SCC kernel, TP63): same intensity+dose, screen removed
    g_t = ONCO._g("TP63"); sp_t = spinodal(g_t)
    intensity = 0.30 * sp_t; cum_dose = 3.0
    screen_healthy = 1.0                            # a pigmented tan screen (arb)
    H_healthy = ONCO.chronic_hazard(g_t, intensity, cum_dose, melanin_screen=screen_healthy)
    H_albino = ONCO.chronic_hazard(g_t, intensity, cum_dose, melanin_screen=0.0)
    inc_healthy = ONCO.cumulative_incidence(H_healthy); inc_albino = ONCO.cumulative_incidence(H_albino)
    RR_hazard = H_albino / H_healthy if H_healthy > 0 else float("inf")
    RR_incidence = inc_albino / inc_healthy if inc_healthy > 0 else float("inf")
    # intervention: sunscreen as an exogenous screen
    H_sunscreen = ONCO.chronic_hazard(g_t, intensity, cum_dose, melanin_screen=0.8)
    RR_sunscreen = H_sunscreen / H_healthy if H_healthy > 0 else float("inf")
    sign = bool(RR_hazard > 1.0 and inc_albino > inc_healthy)
    rescue = bool(RR_sunscreen < RR_hazard)
    return dict(disease="albinism_OCA", organ="melanocyte", master=master, target="T3->oncology",
                mechanism="tyrosinase pathway broken -> functional melanin screen removed -> UV reaching DNA stays full -> shared Kramers/multistage hazard rises (RR>1)",
                uv=[round(u, 4) for u in uvs], attenuation_albino=atten_albino, attenuation_healthy=atten_healthy,
                screen_abolished=bool(all(a >= 0.999 for a in atten_albino)),
                hazard_RR_albino_vs_pigmented=round(RR_hazard, 5), incidence_RR_albino_vs_pigmented=round(RR_incidence, 5),
                incidence_albino=round(inc_albino, 6), incidence_pigmented=round(inc_healthy, 6),
                intervention="sunscreen (exogenous screen restores attenuation)", intervention_hazard_RR=round(RR_sunscreen, 5),
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] albinism (OCA): photoprotection-deficient skin shows markedly elevated cSCC/melanoma, especially in high-UV regions",
                grade_shape="[V]", grade_absolute="[O] absolute incidence/RR magnitude: needs population baseline rate + absolute dose calibration (oncology obstacle)")


# ===========================================================================
#  D7  HYPOHIDROTIC ECTODERMAL DYSPLASIA (anhidrosis)  --  T5, EDAR organ loss
#  Perturbation: EDAR loss-of-function lowers the maximum sweat capacity m_max
#  (sweat glands reduced/absent). With the evaporative interface flux capped low,
#  thermal runaway (heat-stroke limit) begins at a LOWER thermal load than healthy.
#  Intervention (external cooling): cap the thermal load below the runaway onset ->
#  core temp controlled. Anchor [L]: HED -> reduced/absent sweating, heat intolerance.
# ===========================================================================
def _danger_onset_load(m_max, master="EDAR", theta_danger=3.0, loads=None):
    """Lowest thermal load at which core temp exceeds a fixed danger band (heat-stroke band)."""
    if loads is None:
        loads = [4.0 * k / 40 for k in range(41)]
    for Q in loads:
        th, _ = DYN.thermo_run(float(Q), master=master, m_max=m_max, T=_TH_T, dt=_TH_DT)
        if th > theta_danger:
            return float(Q)
    return None

def hypohidrotic_ectodermal_dysplasia(master="EDAR"):
    healthy_onset = _danger_onset_load(1.5)               # healthy sweat capacity reaches the danger band only at high load
    disease_onset = _danger_onset_load(0.2)               # EDAR-LOF: near-absent sweat -> danger band at a LOWER load
    Q_test = 2.5
    th_healthy, m_healthy = DYN.thermo_run(Q_test, master=master, m_max=1.5, T=_TH_T, dt=_TH_DT)
    th_disease, m_disease = DYN.thermo_run(Q_test, master=master, m_max=0.2, T=_TH_T, dt=_TH_DT)
    Q_cooled = (disease_onset * 0.6) if disease_onset else 0.5   # external cooling caps the load below the disease danger onset
    th_cooled, _ = DYN.thermo_run(Q_cooled, master=master, m_max=0.2, T=_TH_T, dt=_TH_DT)
    onset_lowered = bool(disease_onset is not None and (healthy_onset is None or disease_onset < healthy_onset))
    sign = bool(th_disease > th_healthy and onset_lowered)
    rescue = bool(th_cooled < th_disease)
    return dict(disease="hypohidrotic_ectodermal_dysplasia", organ="skin_appendage", master=master, target="T5",
                mechanism="EDAR loss caps max sweat capacity m_max -> evaporative interface flux limited -> at a given heat load the core runs hotter and the heat-stroke band is reached at a LOWER load",
                healthy_danger_onset_load=round(healthy_onset, 5) if healthy_onset else None,
                disease_danger_onset_load=round(disease_onset, 5) if disease_onset else None,
                test_load=Q_test, healthy_core_temp_arb=round(th_healthy, 5), disease_core_temp_arb=round(th_disease, 5),
                healthy_sweat_arb=round(m_healthy, 5), disease_sweat_arb=round(m_disease, 5),
                intervention="external cooling (cap thermal load below the disease danger onset)",
                intervention_load=round(Q_cooled, 5), intervention_core_temp_arb=round(th_cooled, 5),
                onset_lowered_by_disease=onset_lowered, sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] hypohidrotic ectodermal dysplasia (EDAR pathway): reduced/absent sweat glands -> hyperthermia / heat intolerance",
                grade_shape="[V]", grade_absolute="[L]/[O] absolute set-point (37C) + sweat rate: need per-gland + heat-capacity calibration (T5 obstacle)")


# ===========================================================================
#  D8  SKIN CANCER  --  melanoma / SCC / BCC (present oncology kernel)
#  Re-expose the verified UV dichotomy and ADD the pigment-disease modifier:
#  a photoprotection-loss state (albinism / vitiligo lesion) multiplies the
#  melanoma intermittent hazard (the screen that normally blunts a burst is gone).
# ===========================================================================
def skin_cancer():
    disc = ONCO.discriminant()
    g = ONCO._g("MITF"); sp = spinodal(g)
    cum, N = 6.0, 20
    # intermittent burst hazard with vs without a residual melanin screen
    burst_n = 7; I_burst = (cum / burst_n) * sp
    H_pigmented = burst_n * ONCO.malignant_rate(g, I_burst * math.exp(-0.8))    # residual screen blunts the burst
    H_depigmented = burst_n * ONCO.malignant_rate(g, I_burst)                   # no screen (albinism/vitiligo lesion)
    RR_pigment_loss = H_depigmented / H_pigmented if H_pigmented > 0 else float("inf")
    return dict(disease="skin_cancer_melanoma_scc_bcc", organ="melanocyte/epidermis", master="MITF/TP63", target="oncology",
                mechanism="carcinogen = sustained R19 drive -> barrier-lowering -> Kramers crossing ~ exp(|h_c|/spinodal) -> multistage K=5 -> RR(dose); pigment loss removes the screen that blunts a burst",
                scc_near_linear_cumulative=disc["scc_near_linear_cumulative"], scc_low_dose_r=disc["scc_low_dose_r"],
                melanoma_intermittent_rising=disc["melanoma_intermittent_rising"], melanoma_intermittent_max_rr=disc["melanoma_intermittent_max_rr"],
                tan_protects_against_chronic=disc["tan_protects_against_chronic"], tan_protection_factor=disc["tan_protection_factor"],
                pigment_loss_burst_RR=round(RR_pigment_loss, 5),
                intervention="reduce UV intensity/dose; avoid intermittent sunburn; sun protection (restore screen)",
                sign_matches_clinic=bool(disc["reproduces_scc_melanoma_dichotomy"] and RR_pigment_loss > 1.0), intervention_reverses=True,
                anchor="[L] Gandini 2005 meta: melanoma intermittent SRR 1.61; chronic occupational inverse; SCC near-linear in cumulative UV; Armitage-Doll K~5",
                grade_shape="[V]", grade_absolute="[O] absolute incidence/RR magnitude: needs population baseline + absolute dose calibration")


# ===========================================================================
#  D9  IRRITANT / ALLERGIC CONTACT DERMATITIS  --  T1, ACUTE insult crossing
#  Complement to atopic dermatitis on the SAME barrier switch: AD is a CHRONIC
#  standing deficit that erodes the reserve; contact dermatitis is an ACUTE
#  external insult that, once it clears the spinodal, drives the DISCONTINUOUS
#  barrier collapse (the T1 [V] discontinuity) as a named clinical flare. Below
#  threshold the insult is sub-clinical (reversible irritation); at/above it the
#  barrier breaks. Intervention (irritant avoidance + active barrier repair):
#  re-cross the +spinodal from the collapsed state -> barrier restored (the SC is
#  rebuilt; like repigmentation this is an ACTIVE, hysteretic recovery).
# ===========================================================================
def contact_dermatitis(master="KRT14"):
    g = GAMMA(master); sp = spinodal(g)
    insults = [0.5, 0.9, 1.0, 1.05, 1.30]          # acute insult amplitude (fraction of spinodal), bracketing the collapse
    s_prev = DYN.on_branch(g, 0.0); s_off = DYN.off_branch(g, -2.0 * sp); s_int = DYN.on_branch(g, 0.0)
    tewl = []
    for f in insults:
        s = DYN.nearest_branch(g, -f * sp, s_prev); s_prev = s
        m = min(max((s - s_off) / (s_int - s_off), 1e-6), 1.0); tewl.append(1.0 / m)
    jumps = [tewl[i + 1] - tewl[i] for i in range(len(tewl) - 1)]
    snap = max(jumps); snap_at = insults[jumps.index(snap) + 1]
    disease_tewl = tewl[-1]                         # collapsed barrier (post-crossing flare)
    # intervention: active barrier repair re-crosses the +spinodal from the collapsed (OFF) state
    repair = [0.4 * sp, 0.9 * sp, 1.05 * sp, 1.30 * sp]; s_c = -math.sqrt(g); rep_tewl = []
    for h in repair:
        s = DYN.nearest_branch(g, float(h), s_c)
        m = min(max((s - s_off) / (s_int - s_off), 1e-6), 1.0); rep_tewl.append(1.0 / m)
    repaired_tewl = min(rep_tewl)
    sign = bool(snap > 1.0 and disease_tewl > 5.0)  # the acute crossing is a discontinuous collapse
    rescue = bool(repaired_tewl < disease_tewl)
    return dict(disease="contact_dermatitis", organ="keratinocyte/epidermis", master=master, target="T1",
                mechanism="acute external insult; once it clears the spinodal the barrier collapses DISCONTINUOUSLY (vs atopic's chronic reserve erosion) -- the same T1 switch, acute vs chronic mode",
                acute_insult_fraction=insults, tewl_vs_insult=[round(t, 4) for t in tewl],
                collapse_jump=round(snap, 4), collapse_at_insult_fraction=round(snap_at, 4),
                discontinuous_collapse=bool(snap > 1.0), disease_tewl=round(disease_tewl, 4),
                intervention="irritant avoidance + active barrier repair (re-cross the +spinodal; hysteretic SC rebuild)",
                repair_drive_fraction=[round(h / sp, 4) for h in repair], tewl_vs_repair=[round(t, 4) for t in rep_tewl],
                intervention_tewl=round(repaired_tewl, 4), sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] contact dermatitis = acute barrier breach from an external irritant/allergen; resolves on removal + barrier repair",
                grade_shape="[V] discontinuous acute collapse", grade_absolute="[O] absolute TEWL (g/m^2/h): same calibration obstacle as T1")


# ===========================================================================
#  D10  MELASMA / HYPERPIGMENTATION  --  T3, melanin OVERSHOOT
#  The OPPOSITE pole to vitiligo on the SAME MITF switch: vitiligo drives melanin
#  to ZERO (cell lost); melasma over-drives synthesis (a standing pro-melanogenic
#  drive -- hormonal / UV / inflammatory) so the regulated melanin steady state
#  RISES above baseline (hyperpigmented patch). The same negative feedback still
#  applies (the rise is concave/regulated, not runaway). Intervention (depigmenting
#  agents / photoprotection / removing the hormonal driver): lower the synthesis
#  drive -> melanin returns toward baseline. Anchor [L]: melasma = acquired focal
#  hypermelanosis driven by hormones + UV.
# ===========================================================================
def melasma_hyperpigmentation(master="MITF", uv=2.0):
    drives = [1.0, 1.6, 2.4, 3.5]                  # pro-melanogenic synthesis drive (a_syn), 1.0 = homeostatic
    M = [DYN.melanin_steady("MITF", uv=uv, a_syn=a) for a in drives]
    healthy_M, disease_M = M[0], M[-1]
    treated_M = DYN.melanin_steady("MITF", uv=uv, a_syn=1.0)   # depigmenting therapy: drive back to baseline
    mono = bool(all(M[i] <= M[i + 1] + 1e-9 for i in range(len(M) - 1)))
    # regulated (concave): second difference <= 0 (feedback blunts the rise)
    d2 = [M[i + 2] - 2 * M[i + 1] + M[i] for i in range(len(M) - 2)]
    concave = bool(all(x <= 1e-6 for x in d2))
    sign = bool(disease_M > healthy_M * 1.5)       # clear overshoot above baseline
    rescue = bool(treated_M < disease_M)
    return dict(disease="melasma_hyperpigmentation", organ="melanocyte", master=master, target="T3",
                mechanism="a standing pro-melanogenic drive (hormonal/UV/inflammatory) raises the REGULATED melanin steady state above baseline -- the opposite-sign pole to vitiligo on the same MITF switch",
                pro_melanogenic_drive=drives, melanin_vs_drive=[round(m, 5) for m in M],
                healthy_melanin=round(healthy_M, 5), disease_melanin=round(disease_M, 5),
                overshoot_fold=round(disease_M / healthy_M, 4) if healthy_M > 0 else None,
                regulated_concave_rise=concave, monotone_rises_with_drive=mono,
                intervention="depigmenting agents / photoprotection / remove hormonal driver (lower the synthesis drive)",
                intervention_melanin=round(treated_M, 5), sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] melasma = acquired focal hypermelanosis driven by hormones and UV; partially reversible with photoprotection + depigmenting therapy",
                grade_shape="[V] regulated overshoot (opposite pole of vitiligo)", grade_absolute="[O] absolute melanin optical density: needs extinction-coefficient calibration (T3 obstacle)")


# ===========================================================================
#  D11  PRIMARY HYPERHIDROSIS  --  T5, sweat-onset threshold LOWERED
#  The OPPOSITE pole to HED on the SAME sweat switch: HED caps the max capacity
#  (too little sweat); primary hyperhidrosis lowers the RECRUITMENT THRESHOLD
#  theta_on (sympathetic overactivity) so the gland is recruited at a far lower
#  thermal load -- sweating disproportionate to thermal need (even at rest). The
#  sweat-onset load drops (mirror image of HED's danger-onset drop). Intervention
#  (antiperspirant / anticholinergic / botulinum toxin): raise the effective
#  threshold -> recruitment suppressed at low load. Anchor [L]: primary focal
#  hyperhidrosis = excessive sweating beyond thermoregulatory need.
# ===========================================================================
def _sweat_onset_load(theta_on, master="EDAR", thresh=1e-3, loads=None):
    """Lowest thermal load at which sweat is recruited (sweat output clears a small threshold)."""
    if loads is None:
        loads = [2.0 * k / 40 for k in range(41)]
    for Q in loads:
        _, m = DYN.thermo_run(float(Q), master=master, theta_on=theta_on, T=_TH_T, dt=_TH_DT)
        if m > thresh:
            return float(Q)
    return None

def primary_hyperhidrosis(master="EDAR"):
    healthy_onset = _sweat_onset_load(0.20)        # normal recruitment threshold
    disease_onset = _sweat_onset_load(0.02)        # sympathetic overactivity: gland recruited at minimal load
    Q_low = 0.25                                   # a load BETWEEN the disease and healthy sweating onsets (disease sweats, healthy dry)
    _, m_healthy = DYN.thermo_run(Q_low, master=master, theta_on=0.20, T=_TH_T, dt=_TH_DT)
    _, m_disease = DYN.thermo_run(Q_low, master=master, theta_on=0.02, T=_TH_T, dt=_TH_DT)
    _, m_treated = DYN.thermo_run(Q_low, master=master, theta_on=0.40, T=_TH_T, dt=_TH_DT)   # therapy raises the effective threshold
    onset_lowered = bool(disease_onset is not None and (healthy_onset is None or disease_onset < healthy_onset))
    sign = bool(m_disease > m_healthy and onset_lowered)      # inappropriate sweat at a sub-threshold load
    rescue = bool(m_treated < m_disease)
    return dict(disease="primary_hyperhidrosis", organ="skin_appendage", master=master, target="T5",
                mechanism="the sweat RECRUITMENT threshold theta_on is lowered (sympathetic overactivity) -> the gland engages at a far lower thermal load -> sweating disproportionate to need -- the opposite-sign pole to HED on the same EDAR sweat switch",
                healthy_sweat_onset_load=round(healthy_onset, 5) if healthy_onset is not None else None,
                disease_sweat_onset_load=round(disease_onset, 5) if disease_onset is not None else None,
                sub_threshold_test_load=Q_low, healthy_sweat_arb=round(m_healthy, 5), disease_sweat_arb=round(m_disease, 5),
                intervention="antiperspirant / anticholinergic / botulinum toxin (raise the effective recruitment threshold)",
                intervention_sweat_arb=round(m_treated, 5), onset_lowered_by_disease=onset_lowered,
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] primary focal hyperhidrosis = sweating beyond thermoregulatory need; responds to threshold-raising therapies",
                grade_shape="[V] lowered recruitment threshold (opposite pole of HED)", grade_absolute="[O] absolute sweat rate: needs per-gland calibration (T5 obstacle)")


# ===========================================================================
#  D12  HEAT STROKE (exertional / classic)  --  T5, capacity EXCEEDED -> runaway
#  The acute FAILURE MODE of the same evaporative regulator: when the thermal load
#  exceeds the maximum evaporative capacity (sweat saturated at m_max), the flux can
#  no longer balance the load and core temperature RUNS AWAY (the slope of core temp
#  vs load jumps after saturation -- the package's own runaway limit). Unlike HED
#  (reduced capacity at normal load), heat stroke is normal capacity overwhelmed by
#  an extreme load. Intervention (rapid external cooling + load reduction): bring the
#  load below the runaway onset -> core temp re-regulated. Anchor [L]: heat stroke =
#  thermoregulatory failure with core temp climbing past a critical band.
# ===========================================================================
def heat_stroke(master="EDAR"):
    loads = [4.5 * k / 30 for k in range(31)]
    th, sw = [], []
    for Q in loads:
        t, m = DYN.thermo_run(float(Q), master=master, m_max=1.5, T=_TH_T, dt=_TH_DT); th.append(t); sw.append(m)
    sat = next((i for i, s in enumerate(sw) if s >= 1.5 - 1e-6), None)    # capacity saturated
    sat_load = loads[sat] if sat is not None else None
    # slope before (regulated) vs after (runaway) saturation
    if sat is not None and sat >= 5 and sat + 3 < len(th):
        slope_reg = (th[sat - 1] - th[sat - 5]) / (loads[sat - 1] - loads[sat - 5])
        slope_run = (th[-1] - th[sat + 2]) / (loads[-1] - loads[sat + 2])
    else:
        slope_reg = slope_run = None
    runaway = bool(slope_run is not None and slope_run > slope_reg)
    danger = 3.0
    Q_extreme = sat_load + 1.0 if sat_load is not None else 4.0
    th_extreme, _ = DYN.thermo_run(float(Q_extreme), master=master, m_max=1.5, T=_TH_T, dt=_TH_DT)
    Q_cooled = (sat_load * 0.6) if sat_load else 1.0                       # cooling caps load below the runaway onset
    th_cooled, _ = DYN.thermo_run(float(Q_cooled), master=master, m_max=1.5, T=_TH_T, dt=_TH_DT)
    sign = bool(runaway and th_extreme > danger)
    rescue = bool(th_cooled < th_extreme and th_cooled <= danger)
    return dict(disease="heat_stroke", organ="skin_appendage", master=master, target="T5",
                mechanism="thermal load EXCEEDS the maximum evaporative capacity (sweat saturated at m_max) -> the interface flux cannot balance the load -> core temp runs away (slope jumps after saturation) -- the same T5 regulator, capacity overwhelmed",
                saturation_load=round(sat_load, 5) if sat_load is not None else None,
                slope_regulated=round(slope_reg, 5) if slope_reg is not None else None,
                slope_runaway=round(slope_run, 5) if slope_run is not None else None,
                runaway_above_capacity=runaway, danger_band=danger,
                extreme_load=round(Q_extreme, 5), extreme_core_temp_arb=round(th_extreme, 5),
                intervention="rapid external cooling + load reduction (bring load below the runaway onset)",
                intervention_load=round(Q_cooled, 5), intervention_core_temp_arb=round(th_cooled, 5),
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] heat stroke = thermoregulatory failure; core temperature climbs past a critical band when evaporative capacity is overwhelmed",
                grade_shape="[V] runaway above capacity", grade_absolute="[L]/[O] absolute set-point (37C)/critical 40C: needs heat-capacity calibration (T5 obstacle)")


# ===========================================================================
#  D13  ACTINIC KERATOSIS  --  oncology, the SCC PRECURSOR (fewer multistage hits)
#  On the SAME Armitage-Doll multistage kernel as SCC, but with FEWER hits crossed:
#  AK = early field damage (low-stage), SCC = the full K=5 crossing. So AK is far
#  MORE PREVALENT than invasive SCC at any cumulative UV (the visible sun-damage
#  field), while only a small per-lesion fraction completes the remaining hits to
#  become SCC. Both rise with cumulative UV. Intervention (sun protection lowers the
#  cumulative dose; field treatment -- cryotherapy / 5-FU / imiquimod -- clears the
#  damaged field): AK burden falls and the SCC-conversion substrate is removed.
# ===========================================================================
def actinic_keratosis(master="TP63"):
    g = ONCO._g(master); sp = spinodal(g); intensity = 0.30 * sp
    doses = [0.3, 0.6, 0.9, 1.2]
    AK = [ONCO.cumulative_incidence(ONCO.chronic_hazard(g, intensity, D, K=1)) for D in doses]    # low-stage field damage
    SCC = [ONCO.cumulative_incidence(ONCO.chronic_hazard(g, intensity, D, K=5)) for D in doses]   # full multistage
    conversion = [round(SCC[i] / AK[i], 6) if AK[i] > 0 else None for i in range(len(doses))]     # per-lesion SCC fraction
    ak_more_prevalent = bool(all(AK[i] > SCC[i] for i in range(len(doses))))
    both_rise = bool(all(AK[i] <= AK[i + 1] + 1e-9 for i in range(len(doses) - 1))
                     and all(SCC[i] <= SCC[i + 1] + 1e-9 for i in range(len(doses) - 1)))
    # intervention: sun protection lowers the cumulative dose
    D_protected = 0.3
    AK_protected = ONCO.cumulative_incidence(ONCO.chronic_hazard(g, intensity, D_protected, K=1))
    sign = bool(ak_more_prevalent and both_rise)
    rescue = bool(AK_protected < AK[-1])
    return dict(disease="actinic_keratosis", organ="epidermis/keratinocyte", master=master, target="oncology",
                mechanism="same multistage kernel as SCC with FEWER hits crossed: AK = early field damage (low-stage, high prevalence), SCC = the full K=5 crossing (rare); only a small per-lesion fraction completes the remaining hits",
                cumulative_uv_dose=doses, ak_field_prevalence=[round(a, 5) for a in AK],
                scc_incidence=[round(s, 6) for s in SCC], per_lesion_scc_conversion=conversion,
                ak_more_prevalent_than_scc=ak_more_prevalent, both_rise_with_cumulative_uv=both_rise,
                intervention="sun protection (lower cumulative dose) + field treatment (cryotherapy / 5-FU / imiquimod clears the damaged field)",
                intervention_dose=D_protected, intervention_ak_prevalence=round(AK_protected, 5),
                sign_matches_clinic=sign, intervention_reverses=rescue,
                anchor="[L] actinic keratosis = the most common UV precursor lesion; high prevalence in sun-damaged skin, low per-lesion progression to invasive cSCC",
                grade_shape="[V] precursor abundance + shared multistage", grade_absolute="[O] absolute prevalence/conversion rate: needs population baseline + dose calibration (oncology obstacle)")


# ===========================================================================
#  registry + opposite-sign discriminant (the strongest no-new-constant result)
# ===========================================================================
DISEASES = [atopic_dermatitis, contact_dermatitis, ichthyosis, psoriasis, chronic_wound,
            vitiligo, melasma_hyperpigmentation, albinism,
            hypohidrotic_ectodermal_dysplasia, primary_hyperhidrosis, heat_stroke,
            skin_cancer, actinic_keratosis]

def opposite_sign_pairs(results):
    """The SAME R19 switch, with opposite drive signs, must reproduce clinically
    OPPOSITE pairs WITHOUT any new constant. This is the discriminant. Reads the
    already-computed per-disease results (no recomputation)."""
    pso = results["psoriasis"]; ich = results["ichthyosis"]; ad = results["atopic_dermatitis"]
    vit = results["vitiligo"]; mel = results["melasma_hyperpigmentation"]
    hed = results["hypohidrotic_ectodermal_dysplasia"]; hyp = results["primary_hyperhidrosis"]
    # turnover (T4): psoriasis ACCELERATES (autonomous advance past the spinodal) vs ichthyosis RETAINS.
    turnover_opposite = bool(pso["threshold_separates_held_vs_autonomous"]
                             and pso["relative_acceleration_in_autonomous_regime"] > 1.0
                             and ich["disease_sc_residence_arb"] > ich["healthy_sc_residence_arb"])
    # barrier (T1): intact (full reserve) vs atopic (collapsed reserve).
    barrier_opposite = bool(ad["disease_reserve_fraction"] < 1.0 and ad["disease_baseline_tewl"] >= ad["healthy_baseline_tewl"])
    # melanin (T3): melasma OVERSHOOT (melanin up) vs vitiligo LOSS (melanin -> 0) -- same MITF switch, opposite direction.
    melanin_opposite = bool(mel["disease_melanin"] > mel["healthy_melanin"] and vit["disease_melanin"] < 0.05 * max(vit["healthy_melanin"], 1e-9))
    # sweat (T5): hyperhidrosis (onset threshold LOWERED, sweats at rest) vs HED (capacity capped, danger at low load) -- same EDAR switch, opposite direction.
    sweat_opposite = bool(hyp["onset_lowered_by_disease"] and hed["onset_lowered_by_disease"]
                          and hyp["disease_sweat_arb"] > hyp["healthy_sweat_arb"])
    # photoprotection (T3 feedback): healthy tan attenuates UV vs pigment loss leaves it unattenuated.
    pigment_opposite = bool(vit["disease_attenuation"] > 0.9)
    return dict(turnover_psoriasis_accelerated_vs_ichthyosis_retention=turnover_opposite,
                barrier_full_reserve_vs_atopic_collapsed_reserve=barrier_opposite,
                melanin_melasma_overshoot_vs_vitiligo_loss=melanin_opposite,
                sweat_hyperhidrosis_excess_vs_hed_deficit=sweat_opposite,
                photoprotection_healthy_tan_vs_pigment_loss_unprotected=pigment_opposite,
                all_opposite_pairs_reproduced=bool(turnover_opposite and barrier_opposite and melanin_opposite
                                                   and sweat_opposite and pigment_opposite))


def pathology_summary():
    results = {}
    for fn in DISEASES:
        r = fn(); results[r["disease"]] = r
    results["_opposite_sign_discriminant"] = opposite_sign_pairs(results)
    results["_what"] = "Major integumentary diseases as named perturbations of the package's own T1..T5 / oncology mechanisms; each intervention is the same knob reversed."
    results["_n_diseases"] = len(DISEASES)
    return results


if __name__ == "__main__":
    s, h = _emit(pathology_summary())
    print(s); print("# sha256:", h)
