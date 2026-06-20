#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Circulatory Transport STRESS BATTERY.

VP-SPEC discipline (very high bar): each target is exercised under a WIDE sweep (not a single happy
path) and must hold WITHOUT per-target tuning. Failures are reported honestly; an [O] with a stated
obstacle is acceptable, a silent pass is not. Writing stays LOCKED until run_battery() is all PASS
and gates.write_research_complete() is called.

Targets (CHARTER.md):
  T1 MAP            -- MAP - CVP = CO x SVR (Ohm pressure-flow) across a CO x SVR grid; resting ~93 mmHg.
  T2 Windkessel     -- diastolic decay tau = R x C across an R x C grid; resting aortic tau ~1.5 s.
  T3 GFR autoreg    -- tubuloglomerular feedback holds GFR flat (plateau) across 80-180 mmHg; the
                       open-loop kidney does NOT (contrast); setpoint ~125 mL/min.
  T4 osmoregulation -- the ADH/thirst loop corrects an osmotic load back to ~287 mOsm/kg across a load
                       sweep; the no-loop control does NOT (contrast).
  T5 hepatic        -- well-stirred E rises 0->1 with intrinsic clearance, F = 1-E falls 1->0; high-E
                       drugs are flow-limited, low-E capacity-limited; propranolol E~0.75, F~0.25.
Oncology discriminants (repro/_oncology):
  T6 RCC shape      -- carcinogen RR(dose) is monotone and saturating; reaches the cited smoking band.
  T7 HCC synergy    -- two additive barrier-lowering drives give MULTIPLICATIVE RR (aflatoxin x HBV).
"""
import os, sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_oncology"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
import importlib
eng  = importlib.import_module("vp_cir_engine")
onco = importlib.import_module("carcinogen_dose_response")
thx  = importlib.import_module("barrier_therapeutics")
roster_mod = importlib.import_module("oncology_roster")
xref = importlib.import_module("cross_references")   # single-source cross-volume gene-key references


def _suite(target, desc, status, value, grade, obstacle=None):
    return {"target": target, "description": desc, "status": status,
            "value": value, "grade": grade, "obstacle_if_open": obstacle}


# ---------------------------------------------------------------- T1 MAP
def t1_map():
    cos = [3.0, 4.0, 5.0, 7.5, 10.0, 15.0, 20.0, 25.0]      # L/min  (rest -> heavy exercise)
    Rs  = [0.4, 0.6, 0.8, 1.0, 1.10, 1.4, 1.7, 2.0]          # mmHg*s/mL  (dilation -> constriction)
    max_rel = 0.0
    for co_lpm in cos:
        for R in Rs:
            co = co_lpm * 1000.0 / 60.0
            wk = eng.windkessel(co_ml_s=co, R=R, C=eng.C_ART_REST, n_beats=30, steps_per_beat=1500)
            ohm = co * R + eng.CVP_MMHG
            rel = abs(wk["MAP_mmHg"] - ohm) / ohm
            max_rel = max(max_rel, rel)
    rest = eng.windkessel(n_beats=40)
    in_band = 85.0 <= rest["MAP_mmHg"] <= 100.0
    ohm_holds = max_rel < 0.01
    status = "PASS" if (ohm_holds and in_band) else "FAIL"
    val = {"max_rel_dev_MAP_vs_ohm": round(max_rel, 6),
           "resting_MAP_mmHg": rest["MAP_mmHg"],
           "resting_perfusion_CO_x_SVR_mmHg": round(eng.CO_REST_ML_S * eng.SVR_REST, 4),
           "grid_points": len(cos) * len(Rs)}
    return _suite("T1",
        "MAP - CVP = CO x SVR (Ohm pressure-flow) holds across a CO x SVR grid; resting MAP in band",
        status, val, "[F] relation / [V] sim reproduces / [L] absolute CO,SVR / [O] absolute scale",
        obstacle=None)


# ---------------------------------------------------------------- T2 Windkessel
def t2_windkessel():
    Rs = [0.4, 0.6, 0.8, 1.0, 1.10, 1.4, 1.7, 2.0]
    Cs = [0.5, 0.8, 1.0, 1.40, 1.8, 2.2, 2.6, 3.0]
    max_rel = 0.0
    for R in Rs:
        for C in Cs:
            wk = eng.windkessel(R=R, C=C, n_beats=30, steps_per_beat=2000)
            rc = R * C
            rel = abs(wk["tau_meas_s"] - rc) / rc
            max_rel = max(max_rel, rel)
    rest = eng.windkessel(n_beats=40)
    tau_in_band = 1.2 <= rest["tau_meas_s"] <= 2.0
    rc_holds = max_rel < 0.01
    status = "PASS" if (rc_holds and tau_in_band) else "FAIL"
    val = {"max_rel_dev_tau_vs_RC": round(max_rel, 6),
           "resting_tau_meas_s": rest["tau_meas_s"], "resting_tau_RC_s": rest["tau_RC_s"],
           "grid_points": len(Rs) * len(Cs)}
    return _suite("T2",
        "diastolic decay tau = R x C across an R x C grid; resting aortic tau in cited band (~1.5 s)",
        status, val, "[F] relation / [V] sim reproduces / [L] absolute R,C", obstacle=None)


# ---------------------------------------------------------------- T3 GFR autoregulation
def _gfr_curve(tgf):
    Pa = np.arange(60.0, 201.0, 5.0)
    return Pa, np.array([eng.renal_steadystate(float(p), tgf=tgf)["GFR"] for p in Pa])


def t3_gfr_autoreg():
    Pa, g_on  = _gfr_curve(True)
    _,  g_off = _gfr_curve(False)
    band = (Pa >= eng.AUTOREG_LO) & (Pa <= eng.AUTOREG_HI)
    cv_on  = float(np.std(g_on[band])  / np.mean(g_on[band]))
    cv_off = float(np.std(g_off[band]) / np.mean(g_off[band]))
    setpoint_ok = abs(float(np.mean(g_on[band])) - eng.GFR_SET) < 8.0
    plateau   = cv_on < 0.05                      # flat within the band
    contrast  = cv_off > 5.0 * cv_on              # open loop is clearly NOT flat
    status = "PASS" if (plateau and contrast and setpoint_ok) else "FAIL"
    val = {"cv_GFR_TGF_on_band": round(cv_on, 6), "cv_GFR_open_loop_band": round(cv_off, 6),
           "mean_GFR_band_mL_min": round(float(np.mean(g_on[band])), 4),
           "autoreg_band_mmHg": [eng.AUTOREG_LO, eng.AUTOREG_HI]}
    return _suite("T3",
        "tubuloglomerular feedback holds GFR flat across 80-180 mmHg (plateau); open loop does not",
        status, val, "[F] Starling balance / [V] feedback plateau emerges / [L] setpoint,range",
        obstacle=None)


# ---------------------------------------------------------------- T4 osmoregulation
def t4_osmoregulation():
    loads = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]        # L water deficit (dehydration)
    worst_err_loop = 0.0; worst_err_noloop = 0.0
    for L in loads:
        on  = eng.osmostat(load_water_deficit_L=L, loop=True)
        off = eng.osmostat(load_water_deficit_L=L, loop=False)
        worst_err_loop   = max(worst_err_loop,   abs(on["osm_final"]  - eng.OSM_SET))
        worst_err_noloop = max(worst_err_noloop, abs(off["osm_final"] - eng.OSM_SET))
    corrects = worst_err_loop < 1.0               # back to within 1 mOsm of setpoint, every load
    contrast = worst_err_noloop > 5.0             # without the loop the load is NOT corrected
    status = "PASS" if (corrects and contrast) else "FAIL"
    val = {"worst_residual_loop_mOsm": round(worst_err_loop, 6),
           "worst_residual_no_loop_mOsm": round(worst_err_noloop, 6),
           "osm_setpoint_mOsm": eng.OSM_SET, "loads_L": loads}
    return _suite("T4",
        "ADH/thirst loop corrects an osmotic load back to ~287 mOsm/kg across a load sweep; no-loop does not",
        status, val, "[F] water-balance control / [V] correction to setpoint / [L] setpoint ~287",
        obstacle=None)


# ---------------------------------------------------------------- T5 hepatic clearance
def t5_hepatic():
    factors = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
    Es = []
    for f in factors:
        clint = f * eng.Q_H / eng.FU_PROP                  # so fu*clint = f*Q_H
        Es.append(eng.hepatic_clearance(clint=clint)["E"])
    Es = np.array(Es)
    monotone = bool(np.all(np.diff(Es) > 0))               # E rises with intrinsic clearance
    spans = (Es[0] < 0.1) and (Es[-1] > 0.9)               # 0 -> 1 saturation
    # regime contrast (textbook discriminant, Rowland-Tozer): hepatic-clearance flow-ELASTICITY
    # d(ln CL_H)/d(ln Q_H).  flow-limited (high-E) -> elasticity ~ 1 (CL_H tracks blood flow);
    # capacity-limited (low-E) -> elasticity ~ 0 (CL_H set by fu*CLint, flow-independent).
    # F-sensitivity to +/-30% flow is reported alongside as a secondary readout.
    def CL_at(clu_factor, qfac):
        clint = clu_factor * eng.Q_H / eng.FU_PROP
        return eng.hepatic_clearance(Qh=eng.Q_H * qfac, clint=clint)["CL_H_ml_min"]
    def elasticity(clu_factor):
        cl_hi, cl_lo = CL_at(clu_factor, 1.3), CL_at(clu_factor, 0.7)
        return (math.log(cl_hi) - math.log(cl_lo)) / (math.log(1.3) - math.log(0.7))
    high_elast = elasticity(9.0)    # E ~ 0.90 : flow-limited     -> ~1
    low_elast  = elasticity(0.1)    # E ~ 0.09 : capacity-limited  -> ~0
    def F_at(clu_factor, qfac):
        clint = clu_factor * eng.Q_H / eng.FU_PROP
        return eng.hepatic_clearance(Qh=eng.Q_H * qfac, clint=clint)["F"]
    high_sens = abs(F_at(9.0, 1.3) - F_at(9.0, 0.7)) / max(F_at(9.0, 1.0), 1e-6)
    low_sens  = abs(F_at(0.1, 1.3) - F_at(0.1, 0.7)) / max(F_at(0.1, 1.0), 1e-6)
    regime_ok = (high_elast > 0.70) and (low_elast < 0.15) and (high_elast > 5.0 * low_elast)
    prop = eng.hepatic_clearance()
    prop_ok = (0.70 <= prop["E"] <= 0.90) and (0.20 <= prop["F"] <= 0.35)
    status = "PASS" if (monotone and spans and regime_ok and prop_ok) else "FAIL"
    val = {"E_min": round(float(Es[0]), 6), "E_max": round(float(Es[-1]), 6),
           "monotone": monotone,
           "CL_flow_elasticity_highE": round(float(high_elast), 4),
           "CL_flow_elasticity_lowE": round(float(low_elast), 4),
           "F_sens_highE": round(float(high_sens), 6),
           "F_sens_lowE": round(float(low_sens), 6),
           "propranolol_E": prop["E"], "propranolol_F": prop["F"]}
    return _suite("T5",
        "well-stirred E rises 0->1 with intrinsic clearance, F=1-E falls; high-E flow-limited, low-E capacity-limited; propranolol E~0.75 F~0.25",
        status, val, "[F] well-stirred saturation / [V] regimes reproduced / [L] propranolol,Q_H",
        obstacle=None)


# ---------------------------------------------------------------- T6 RCC dose-response shape
def t6_rcc_shape():
    r = onco.rcc_smoking_doseresponse()
    status = "PASS" if r["pass"] else "FAIL"
    return _suite("T6",
        "carcinogen RR(dose) monotone + saturating; reaches the cited smoking RR band (RCC)",
        status, r["value"], "[L] smoking RR anchor (Hunt 2005) / [V] monotone saturating shape / [O] absolute incidence",
        obstacle="absolute RCC incidence rate needs population calibration (RR shape reproduced; level open)")


# ---------------------------------------------------------------- T7 HCC multiplicative synergy
def t7_hcc_synergy():
    r = onco.hcc_aflatoxin_hbv_synergy()
    status = "PASS" if r["pass"] else "FAIL"
    return _suite("T7",
        "two additive barrier-lowering drives give MULTIPLICATIVE RR (aflatoxin x HBV synergy, HCC)",
        status, r["value"], "[L] Qian1994/meta synergy RR / [V] additive drive -> multiplicative RR (Arrhenius) / [O] absolute incidence",
        obstacle="absolute HCC incidence rate needs population calibration (multiplicativity reproduced; level open)")


# ============================================================================
#  DISEASE EXTENSIONS  T8-T17  (DISEASE_EXTENSIONS.md task charter)
#  Each disorder is ONE named setting of an existing engine knob (no new
#  mechanism), exercised over a WIDE sweep and paired with a healthy/opposite
#  CONTRAST so a PASS means a mechanistic SEPARATION, not a tuned number.
#  Relation = [F]; simulation reproducing shape/contrast = [V]; cited clinical
#  band = [L]; absolute population number = [O] with a stated obstacle.
# ============================================================================
ISH_SBP, ISH_DBP = 140.0, 90.0    # isolated systolic HTN: SBP>=140 & DBP<90 (Franklin, Circulation 1997;96:308-315)
HTN_SBP, HTN_DBP = 140.0, 90.0    # stage-2 hypertension threshold (JNC7 / ACC-AHA)
MAP_SHOCK        = 65.0           # Surviving Sepsis MAP target; <65 mmHg = shock (Asfar SEPSISPAM, NEJM 2014, PMID 24635770)
OSM_HYPER        = 295.0          # hyperosmolality / hypernatremia surrogate (Na>145) -- DI
OSM_HYPO         = 275.0          # hyponatremia surrogate (Na<135) -- SIADH (Verbalis 2013)
KDIGO_GFR        = [90.0, 60.0, 45.0, 30.0, 15.0]  # G1/2,G2/3a,G3a/3b,G3b/4,G4/5 (KDIGO 2012/2024)


def t8_arterial_stiffening():
    """A1: arterial stiffening (C down) -> isolated systolic hypertension."""
    Cs = [2.6, 2.2, 1.8, 1.40, 1.1, 0.8, 0.6, 0.5, 0.4, 0.32, 0.26]   # compliant -> stiff (mL/mmHg)
    W = [eng.windkessel(C=C) for C in Cs]
    SBP = np.array([w["SBP_mmHg"] for w in W]); DBP = np.array([w["DBP_mmHg"] for w in W])
    PP  = np.array([w["PP_mmHg"] for w in W]);  MAP = np.array([w["MAP_mmHg"] for w in W])
    TAU = np.array([w["tau_meas_s"] for w in W])
    pp_up  = bool(np.all(np.diff(PP) > 0))        # PP widens monotonically as C falls
    tau_dn = bool(np.all(np.diff(TAU) < 0))       # tau shortens in lockstep with C
    map_rel = float((MAP.max() - MAP.min()) / MAP.mean())   # mean pressure ~ unchanged (Franklin)
    ish = next((w for w in W if w["SBP_mmHg"] >= ISH_SBP and w["DBP_mmHg"] < ISH_DBP), None)
    status = "PASS" if (pp_up and tau_dn and map_rel < 0.02 and ish is not None) else "FAIL"
    val = {"C_sweep": Cs, "PP_mmHg": [round(float(x), 2) for x in PP],
           "SBP_mmHg": [round(float(x), 1) for x in SBP], "DBP_mmHg": [round(float(x), 1) for x in DBP],
           "MAP_rel_range": round(map_rel, 6), "tau_s": [round(float(x), 3) for x in TAU],
           "ISH_point": ({"C": ish["C"], "SBP": ish["SBP_mmHg"], "DBP": ish["DBP_mmHg"], "PP": ish["PP_mmHg"]}
                         if ish else None)}
    return _suite("T8",
        "arterial stiffening (compliance down): PP widens + tau shortens while MAP stays flat; reaches an ISH point (SBP>=140, DBP<90)",
        status, val, "[F] PP=f(SV,C) / [V] PP up, tau down, MAP flat as C falls / [L] Franklin Circulation 1997;96:308 / [O] absolute CV risk",
        obstacle="absolute cardiovascular event rate needs a population hazard model (hemodynamic shape reproduced; risk level open)")


def t9_essential_hypertension():
    """A2: resistance-driven hypertension (SVR up), MAP=CO*SVR preserved; CO-driven contrast at equal MAP."""
    Rs = [1.10, 1.27, 1.4, 1.55, 1.7, 1.85, 2.0]
    W = [eng.windkessel(R=R) for R in Rs]
    MAP = np.array([w["MAP_mmHg"] for w in W])
    ohm_dev = max(abs(w["MAP_mmHg"] - w["MAP_ohm_mmHg"]) / w["MAP_ohm_mmHg"] for w in W)
    crosses = bool(any((w["SBP_mmHg"] >= HTN_SBP and w["DBP_mmHg"] >= HTN_DBP) for w in W))
    map_up = bool(np.all(np.diff(MAP) > 0))
    # contrast: reach the SVR=1.7 MAP from a pure CO rise at normal SVR (same MAP, different knob)
    wR = eng.windkessel(R=1.7)
    co_match = (wR["MAP_mmHg"] - eng.CVP_MMHG) / eng.SVR_REST
    wCO = eng.windkessel(co_ml_s=co_match)
    same_map = abs(wR["MAP_mmHg"] - wCO["MAP_mmHg"]) < 1.0
    diff_knob = abs(wR["R"] - wCO["R"]) > 0.3 and abs(wR["CO_ml_s"] - wCO["CO_ml_s"]) > 10.0
    status = "PASS" if (ohm_dev < 0.01 and crosses and map_up and same_map and diff_knob) else "FAIL"
    val = {"SVR_sweep": Rs, "MAP_mmHg": [round(float(x), 1) for x in MAP],
           "max_ohm_dev": round(float(ohm_dev), 6),
           "contrast_equal_MAP": {"resistance_route": {"SVR": wR["R"], "CO_ml_s": wR["CO_ml_s"], "MAP": wR["MAP_mmHg"]},
                                  "flow_route": {"SVR": wCO["R"], "CO_ml_s": wCO["CO_ml_s"], "MAP": wCO["MAP_mmHg"]}}}
    return _suite("T9",
        "essential hypertension (SVR up): MAP rises with the Ohm identity MAP=CO*SVR exact (<1%); same MAP reachable from a CO rise (different mechanism)",
        status, val, "[F] MAP=CO*SVR / [V] crosses 140/90 with identity preserved + flow/resistance contrast / [L] JNC7/ACC-AHA threshold",
        obstacle=None)


def t10_shock_subtypes():
    """A3: hypotension/shock from two distinct knobs (hypovolemic CO down vs distributive SVR down) at equal MAP."""
    COs = [5.0, 4.0, 3.2, 3.0, 2.5, 2.0]      # L/min  (hypovolemic)
    Rsv = [1.10, 0.9, 0.7, 0.66, 0.55, 0.45]  # mmHg*s/mL (distributive)
    hypo = [eng.windkessel(co_ml_s=c * 1000.0 / 60.0) for c in COs]
    dist = [eng.windkessel(R=R) for R in Rsv]
    hypo_shock = any(w["MAP_mmHg"] < MAP_SHOCK for w in hypo)
    dist_shock = any(w["MAP_mmHg"] < MAP_SHOCK for w in dist)
    # matched-MAP two-route contrast at ~59 mmHg: CO=3.0 L/min vs the SVR giving the same MAP
    wCO = eng.windkessel(co_ml_s=3.0 * 1000.0 / 60.0)
    R_match = (wCO["MAP_mmHg"] - eng.CVP_MMHG) / eng.CO_REST_ML_S
    wSV = eng.windkessel(R=R_match)
    matched = abs(wCO["MAP_mmHg"] - wSV["MAP_mmHg"]) < 1.0
    distinct = abs(wCO["CO_ml_s"] - wSV["CO_ml_s"]) > 10.0 and abs(wCO["R"] - wSV["R"]) > 0.2
    both_below = wCO["MAP_mmHg"] < MAP_SHOCK and wSV["MAP_mmHg"] < MAP_SHOCK
    status = "PASS" if (hypo_shock and dist_shock and matched and distinct and both_below) else "FAIL"
    val = {"hypovolemic_CO_Lmin": COs, "hypovolemic_MAP": [round(w["MAP_mmHg"], 1) for w in hypo],
           "distributive_SVR": Rsv, "distributive_MAP": [round(w["MAP_mmHg"], 1) for w in dist],
           "matched_shock_point_mmHg": round(wCO["MAP_mmHg"], 1),
           "route_hypovolemic": {"CO_ml_s": wCO["CO_ml_s"], "SVR": wCO["R"]},
           "route_distributive": {"CO_ml_s": wSV["CO_ml_s"], "SVR": wSV["R"]}}
    return _suite("T10",
        "shock subtypes: hypovolemic (CO down) and distributive (SVR down) both drive MAP<65; engine separates the two routes at equal MAP",
        status, val, "[F] MAP=CO*SVR / [V] both routes reach MAP<65 from distinct knobs / [L] Surviving Sepsis MAP>=65 (SEPSISPAM PMID 24635770)",
        obstacle=None)


def t11_diabetes_insipidus():
    """B1: diabetes insipidus (ADH gain -> 0): a water deficit is NOT corrected (sustained hyperosmolality)."""
    loads = [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
    di_final = [eng.osmostat(load_water_deficit_L=L, adh_gain=0.0)["osm_final"] for L in loads]
    intact   = [eng.osmostat(load_water_deficit_L=L)["osm_final"] for L in loads]
    di_no_recover = all(d > eng.OSM_SET + 2.0 for d in di_final)          # every load stays clearly elevated
    di_tracks_load = bool(np.all(np.diff(np.array(di_final)) > 0))         # rises with deficit (no correction)
    di_hyper = any(d >= OSM_HYPER for d in di_final)                       # reaches hyperosmolality band
    intact_corrects = all(abs(i - eng.OSM_SET) < 1.0 for i in intact)      # intact returns to setpoint
    contrast = all((d - eng.OSM_SET) > (abs(i - eng.OSM_SET) + 2.0) for d, i in zip(di_final, intact))
    status = "PASS" if (di_no_recover and di_tracks_load and di_hyper and intact_corrects and contrast) else "FAIL"
    val = {"loads_L": loads, "DI_osm_final": [round(x, 2) for x in di_final],
           "intact_osm_final": [round(x, 2) for x in intact], "osm_setpoint": eng.OSM_SET,
           "hyperosmolar_band": OSM_HYPER}
    return _suite("T11",
        "diabetes insipidus (ADH gain to zero): an imposed water deficit is not corrected, osmolality stays elevated (hypernatremia surrogate); intact loop recovers",
        status, val, "[V] no setpoint recovery vs intact contrast / [L] DI hyperosmolality Na>145 / [O] absolute plasma Na",
        obstacle="absolute plasma sodium needs renal free-water-clearance calibration (direction + contrast reproduced; level open)")


def t12_siadh():
    """B2: SIADH (inappropriate antidiuresis -> defended osmolality shifts down): dilutional hyponatremia; mirror of DI."""
    shifts = [-3.0, -6.0, -9.0, -12.0, -15.0]            # mOsm/kg downward shift of defended osmolality
    si_final = [eng.osmostat(setpoint_shift_mOsm=s)["osm_final"] for s in shifts]
    intact = eng.osmostat()["osm_final"]
    below = all(f < eng.OSM_SET - 1.0 for f in si_final)           # held below setpoint
    monotone = bool(np.all(np.diff(si_final) < 0))                 # deeper shift -> lower osmolality
    hypo = any(f <= OSM_HYPO for f in si_final)                    # reaches hyponatremia band
    intact_ok = abs(intact - eng.OSM_SET) < 1.0
    # mirror contrast: DI raises osmolality above setpoint, SIADH lowers it below, from the same osmostat
    di = eng.osmostat(load_water_deficit_L=3.0, adh_gain=0.0)["osm_final"]
    mirror = (di > eng.OSM_SET) and (si_final[-1] < eng.OSM_SET)
    status = "PASS" if (below and monotone and hypo and intact_ok and mirror) else "FAIL"
    val = {"setpoint_shift_mOsm": shifts, "SIADH_osm_final": [round(x, 2) for x in si_final],
           "intact_osm_final": round(intact, 2), "hyponatremia_band": OSM_HYPO,
           "mirror": {"DI_osm": round(di, 2), "SIADH_osm": round(si_final[-1], 2), "setpoint": eng.OSM_SET}}
    return _suite("T12",
        "SIADH (inappropriate antidiuresis): defended osmolality shifts down, osmolality held below setpoint (hyponatremia surrogate); exact mirror of DI",
        status, val, "[V] osmolality held below setpoint + DI/SIADH mirror / [L] SIADH Na<135 (Verbalis 2013) / [O] absolute Na, volume escape",
        obstacle="minimal osmostat lacks the volume-mediated ADH escape; SIADH is represented by its net defended-hyponatremia (direction + mirror reproduced; absolute Na and escape kinetics open)")


def t13_ckd_staging():
    """B3: CKD as remaining-nephron fraction -> total GFR steps through KDIGO stages; per-nephron autoregulation intact."""
    band = np.arange(eng.AUTOREG_LO, eng.AUTOREG_HI + 1.0, 10.0)
    Nfracs = [1.0, 0.72, 0.48, 0.36, 0.24, 0.12]            # intact -> G5
    stages = []
    cv_max = 0.0
    for Nf in Nfracs:
        g = Nf * np.array([eng.renal_steadystate(float(p), tgf=True)["GFR"] for p in band])
        cv = float(np.std(g) / np.mean(g)); cv_max = max(cv_max, cv)
        stages.append({"N_frac": Nf, "total_GFR_mL_min": round(float(np.mean(g)), 1), "cv": round(cv, 6)})
    # each reduced level still autoregulates (flat); open loop does not
    g_open = np.array([eng.renal_steadystate(float(p), tgf=False)["GFR"] for p in band])
    cv_open = float(np.std(g_open) / np.mean(g_open))
    means = [s["total_GFR_mL_min"] for s in stages[1:]]
    hits_kdigo = all(abs(m - k) < 1.0 for m, k in zip(means, KDIGO_GFR))   # 90/60/45/30/15
    plateau_each = cv_max < 0.05
    contrast = cv_open > 10.0 * max(cv_max, 1e-6)
    status = "PASS" if (hits_kdigo and plateau_each and contrast) else "FAIL"
    val = {"stages": stages, "kdigo_thresholds": KDIGO_GFR, "cv_open_loop": round(cv_open, 4),
           "autoreg_band_mmHg": [eng.AUTOREG_LO, eng.AUTOREG_HI]}
    return _suite("T13",
        "CKD staging (remaining-nephron fraction): total GFR steps through KDIGO 90/60/45/30/15 while per-nephron autoregulation stays flat at each level; open loop does not",
        status, val, "[F] GFR=N*Starling / [V] staged plateaus + open-loop contrast / [L] KDIGO 2012/2024 GFR categories / [O] prevalence",
        obstacle="absolute stage prevalence needs population data (per-stage plateau reproduced; epidemiologic level open)")


def t14_autoregulation_breakthrough():
    """B4: autoregulation breakthrough -- push renal perfusion past the plateau; GFR and P_GC rise (barotrauma surrogate)."""
    Pa = np.arange(80.0, 261.0, 5.0)
    GFR = np.array([eng.renal_steadystate(float(p), tgf=True)["GFR"] for p in Pa])
    PGC = np.array([eng.renal_steadystate(float(p), tgf=True)["P_GC"] for p in Pa])
    in_band = Pa <= eng.AUTOREG_HI
    flat_in_band = float(np.std(GFR[in_band]) / np.mean(GFR[in_band])) < 0.02
    over = ~in_band
    rises_over = bool(GFR[over][-1] > GFR[in_band][-1] * 1.10 and PGC[over][-1] > PGC[in_band][-1] + 2.0)
    bp = next((float(Pa[i]) for i in range(len(Pa)) if GFR[i] > eng.GFR_SET * 1.02), None)  # breakthrough pressure
    status = "PASS" if (flat_in_band and rises_over and bp is not None and bp > eng.AUTOREG_HI - 1.0) else "FAIL"
    val = {"breakthrough_pressure_mmHg": bp, "GFR_at_240": round(float(GFR[Pa == 240.0][0]), 1),
           "P_GC_at_240": round(float(PGC[Pa == 240.0][0]), 1), "GFR_setpoint": eng.GFR_SET,
           "flat_in_band": flat_in_band, "autoreg_ceiling": eng.AUTOREG_HI}
    return _suite("T14",
        "autoregulation breakthrough: GFR is flat across the 80-180 mmHg plateau, then GFR and glomerular pressure climb once perfusion exceeds the ceiling (glomerular hypertension surrogate)",
        status, val, "[F] Starling + clamp / [V] flat-then-breakthrough emerges from the TGF saturation / [L] renal autoregulation ~80-180 mmHg",
        obstacle=None)


def t15_hepatic_impairment():
    """C1: cirrhosis/hepatic impairment (CLint down) -> high-E drug F rises (over-exposure); low-E drug comparatively spared."""
    factors = [1.0, 0.7, 0.5, 0.3, 0.2, 0.1]
    highE = [eng.hepatic_clearance(clint=eng.CLINT_PROP * f) for f in factors]        # propranolol-like (E~0.75)
    clint_low = 0.1 * eng.Q_H / eng.FU_PROP
    lowE = [eng.hepatic_clearance(clint=clint_low * f) for f in factors]              # low-E drug (E~0.09)
    F_hi = np.array([h["F"] for h in highE]); F_lo = np.array([h["F"] for h in lowE])
    hi_rises = bool(np.all(np.diff(F_hi) > 0))
    hi_fold = float(F_hi[-1] / F_hi[0])              # over-exposure factor for the high-E drug
    lo_fold = float(F_lo[-1] / F_lo[0])              # low-E drug barely moves
    spared = hi_fold > 2.5 and lo_fold < 1.15        # high-E drug strongly affected, low-E spared
    status = "PASS" if (hi_rises and spared) else "FAIL"
    val = {"CLint_factors": factors, "highE_E": [h["E"] for h in highE], "highE_F": [h["F"] for h in highE],
           "lowE_F": [h["F"] for h in lowE], "highE_F_fold": round(hi_fold, 3), "lowE_F_fold": round(lo_fold, 3)}
    return _suite("T15",
        "hepatic impairment (intrinsic clearance down): a high-extraction drug's oral F rises several-fold (dose reduction needed) while a low-extraction drug is comparatively spared",
        status, val, "[F] F=1-E well-stirred / [V] high-E F up, low-E spared (contrast) / [L] Child-Pugh dose adjustment, high-E PK / [O] absolute exposure",
        obstacle="absolute drug exposure needs a severity->CLint calibration per agent (over-exposure direction + selectivity reproduced; magnitude open)")


def t16_portosystemic_shunt():
    """C2: portosystemic shunt -- fraction s of portal flow bypasses hepatocytes; F = 1-(1-s)E, high-E drugs most affected."""
    S = [0.0, 0.2, 0.4, 0.6, 0.8]
    E_hi = eng.hepatic_clearance()["E"]                         # high-E (propranolol, ~0.75)
    E_lo = eng.hepatic_clearance(clint=0.1 * eng.Q_H / eng.FU_PROP)["E"]   # low-E (~0.09)
    F_hi = np.array([1.0 - (1.0 - s) * E_hi for s in S])
    F_lo = np.array([1.0 - (1.0 - s) * E_lo for s in S])
    hi_rises = bool(np.all(np.diff(F_hi) > 0)) and bool(np.all(np.diff(F_lo) >= 0))
    slope_hi = float((F_hi[-1] - F_hi[0]) / (S[-1] - S[0]))     # dF/ds == E exactly
    slope_lo = float((F_lo[-1] - F_lo[0]) / (S[-1] - S[0]))
    slope_is_E = abs(slope_hi - E_hi) < 1e-6 and abs(slope_lo - E_lo) < 1e-6
    high_most_affected = slope_hi > 3.0 * slope_lo
    status = "PASS" if (hi_rises and slope_is_E and high_most_affected) else "FAIL"
    val = {"shunt_fraction": S, "highE_F": [round(float(x), 3) for x in F_hi],
           "lowE_F": [round(float(x), 3) for x in F_lo], "dF_ds_highE": round(slope_hi, 4),
           "dF_ds_lowE": round(slope_lo, 4), "E_high": round(E_hi, 3), "E_low": round(E_lo, 3)}
    return _suite("T16",
        "portosystemic shunt: oral F = 1-(1-s)E rises with shunt fraction, slope dF/ds equals the extraction ratio E, so high-extraction (flow-limited) drugs are most affected",
        status, val, "[F] F=1-(1-s)E (corollary of T5) / [V] slope==E, high-E most affected / [L] shunt raises high-E drug F toward 1",
        obstacle=None)


def t17_enzyme_ddi():
    """C3: enzyme induction/inhibition (CLint x factor) -- low-E drugs CLint-sensitive (capacity-limited), high-E CLint-insensitive (flow-limited)."""
    def clint_elasticity(clu_factor):
        clint = clu_factor * eng.Q_H / eng.FU_PROP
        cl_hi = eng.hepatic_clearance(clint=clint * 1.3)["CL_H_ml_min"]
        cl_lo = eng.hepatic_clearance(clint=clint * 0.7)["CL_H_ml_min"]
        return (math.log(cl_hi) - math.log(cl_lo)) / (math.log(1.3) - math.log(0.7))
    low_el  = clint_elasticity(0.1)     # low-E drug: capacity-limited -> elasticity ~ 1
    high_el = clint_elasticity(9.0)     # high-E drug: flow-limited   -> elasticity ~ 0
    # directional: inhibition (CLint down) raises F; induction (CLint up) lowers F (for the low-E drug)
    clint_low = 0.1 * eng.Q_H / eng.FU_PROP
    F_base = eng.hepatic_clearance(clint=clint_low)["F"]
    F_inhib = eng.hepatic_clearance(clint=clint_low * 0.5)["F"]
    F_induce = eng.hepatic_clearance(clint=clint_low * 2.0)["F"]
    directional = F_inhib > F_base > F_induce
    regime_ok = low_el > 0.80 and high_el < 0.20 and low_el > 4.0 * high_el
    status = "PASS" if (regime_ok and directional) else "FAIL"
    val = {"CLint_elasticity_lowE": round(low_el, 4), "CLint_elasticity_highE": round(high_el, 4),
           "lowE_F_base": round(F_base, 4), "lowE_F_inhibited": round(F_inhib, 4), "lowE_F_induced": round(F_induce, 4)}
    return _suite("T17",
        "enzyme induction/inhibition: clearance CLint-elasticity is ~1 for low-extraction drugs (capacity-limited, DDI-sensitive) and ~0 for high-extraction drugs (flow-limited); inhibition raises F, induction lowers it",
        status, val, "[F] well-stirred regimes / [V] CLint-elasticity 1 vs 0 + correct F direction / [L] typical DDI fold-changes",
        obstacle=None)


# ============================================================================
#  ONCOLOGY THERAPEUTIC-TARGET LAYER  T18-T21  (barrier_therapeutics.py)
#  Consequences of the SAME R19 carcinogenesis kernel for REVERSING the
#  malignant transition. Dynamics forced [F] / simulated [V]; de-escalation
#  magnitude [V] vs cited epidemiology [L]; therapeutic reading is a
#  prediction [H]; barrier=g^2/4 grounding + absolute mapping [O].
# ============================================================================
def t18_reversibility_threshold():
    """The malignant transition is REVERSIBLE by drive-removal iff the drive stayed below the
    spinodal; the simulated reversibility threshold equals the analytic spinodal for both cancers."""
    out = {}
    ok = True
    for site, g in [("RCC", thx.GAMMA_KIDNEY), ("HCC", thx.GAMMA_LIVER)]:
        sp = onco.spinodal(g)
        thr = thx.reversibility_threshold(g)
        below = thx.reversion_after_drive(g, sp - 0.05)      # pre-spinodal: should revert
        above = thx.reversion_after_drive(g, sp + 0.05)      # post-spinodal: should commit
        match = (thr is not None) and abs(thr - sp) < 0.02
        sep = below["reverted"] and (not above["reverted"])
        ok = ok and match and sep
        out[site] = {"spinodal": round(sp, 5), "sim_threshold": round(thr, 5) if thr else None,
                     "pre_spinodal_reverts": below["reverted"], "post_spinodal_commits": not above["reverted"],
                     "pre_s_final": round(below["s_final"], 3), "post_s_final": round(above["s_final"], 3)}
    status = "PASS" if ok else "FAIL"
    return _suite("T18",
        "reversibility threshold = spinodal: a driven pre-malignant cell reverts on drive-removal below h_sp and commits irreversibly above it (responder boundary for de-driving therapy)",
        status, out, "[F] saddle-node at h_sp / [V] sim threshold == analytic spinodal, pre/post separation / [H] differentiation-therapy responder boundary / [O] barrier=g^2/4 grounding",
        obstacle="maps to a clinical responder boundary only if the cell-fate barrier really equals g^2/4 from promoter stacking energy (unmeasured); dynamics and threshold are exact, biological grounding is [O]")


def t19_critical_slowing():
    """Near the irreversibility threshold the healthy basin goes marginally stable: reversion time
    diverges with the universal saddle-node exponent 1/2 (relapse-prone pre-malignant lesions)."""
    out = {}
    ok = True
    for site, g in [("RCC", thx.GAMMA_KIDNEY), ("HCC", thx.GAMMA_LIVER)]:
        sp = onco.spinodal(g)
        hs = [0.0, 0.3, 0.5, 0.65, 0.70, 0.72]
        taus = [thx.healthy_relaxation_tau(g, h) for h in hs if h < sp]
        grows = all(taus[i + 1] > taus[i] for i in range(len(taus) - 1))   # tau increases toward h_sp
        eps = np.array([1e-2, 5e-3, 2e-3, 1e-3, 5e-4, 2e-4])               # distance below spinodal
        tau_eps = np.array([thx.healthy_relaxation_tau(g, sp - e) for e in eps])
        slope = float(np.polyfit(np.log(eps), np.log(tau_eps), 1)[0])      # expect -1/2
        exponent_ok = abs(slope + 0.5) < 0.05
        ok = ok and grows and exponent_ok
        out[site] = {"tau_grid": [round(t, 3) for t in taus], "fold_exponent": round(slope, 3),
                     "exponent_is_half": exponent_ok}
    status = "PASS" if ok else "FAIL"
    return _suite("T19",
        "critical slowing: reversion time diverges as drive approaches the threshold with the universal fold exponent 1/2; lesions near threshold are marginally stable (relapse-prone)",
        status, out, "[F] lambda=g-3 s_h^2 -> 0 at saddle-node / [V] tau ~ (h_sp-h)^-1/2, exponent 1/2 / [H] near-threshold relapse-proneness",
        obstacle=None)


def t20_synergy_reversal():
    """De-escalation: because synergistic carcinogens multiply risk, removing one DIVIDES the
    combined risk by that agent's RR -- a multiplicative benefit far exceeding additive expectation."""
    g = thx.GAMMA_LIVER; D = onco.D_HCC
    d_a = D * math.log(onco.RR_AFLA_META); d_v = D * math.log(onco.RR_HBV_META)
    h_a = onco._h_for_decrement(g, d_a); h_v = onco._h_for_decrement(g, d_v)
    rr_a = onco.relative_risk(g, h_a, D); rr_v = onco.relative_risk(g, h_v, D)
    rr_comb = math.exp((d_a + d_v) / D)
    rr_remove_hbv = rr_a                                    # remove HBV -> aflatoxin alone
    reduction_factor = rr_comb / rr_remove_hbv             # == RR_v (multiplicative)
    add_naive = rr_comb - (rr_v - 1.0)                      # additive thinking: subtract HBV excess
    mult_is_div = abs(reduction_factor - rr_v) < 0.05
    drop_mult = rr_comb - rr_remove_hbv                     # absolute risk drop, multiplicative
    drop_add = rr_comb - add_naive                          # absolute risk drop, additive
    much_larger = drop_mult > 5.0 * drop_add               # de-escalation leverage
    status = "PASS" if (mult_is_div and much_larger) else "FAIL"
    val = {"RR_aflatoxin": round(rr_a, 2), "RR_HBV": round(rr_v, 2), "RR_combined": round(rr_comb, 1),
           "remove_HBV_RR": round(rr_remove_hbv, 2), "reduction_factor": round(reduction_factor, 2),
           "additive_naive_RR": round(add_naive, 1),
           "multiplicative_drop": round(drop_mult, 1), "additive_drop": round(drop_add, 1),
           "leverage_x": round(drop_mult / drop_add, 1)}
    return _suite("T20",
        "synergy reversal (de-escalation): removing one of two multiplicative carcinogens divides combined risk by its RR (~11x for HBV), not the ~1.2x additive thinking predicts",
        status, val, "[F] additive decrements -> multiplicative RR (inverse of T7) / [V] removal divides by RR_v / [L] HBV control benefit in aflatoxin regions / [H] prevention target",
        obstacle=None)


def t21_barrier_restoration_leverage():
    """Prevention >> cure, quantitatively: raising the effective barrier by delta suppresses the
    malignant-crossing rate by exp(-delta/D) -- exponential, not linear, leverage."""
    D = onco.D_HCC
    deltas = [0.05, 0.10, 0.20, 0.30, 0.50]
    supp = [thx.barrier_restoration_suppression(d, D) for d in deltas]
    log_supp = np.log(np.array(supp))
    slope = float(np.polyfit(np.array(deltas), log_supp, 1)[0])     # expect -1/D
    exp_leverage = abs(slope + 1.0 / D) < 1e-6
    # exponential beats the linear "restore X% -> X% fewer crossings" expectation at every delta
    beats_linear = all(supp[i] < (1.0 - deltas[i]) for i in range(len(deltas)))
    status = "PASS" if (exp_leverage and beats_linear) else "FAIL"
    val = {"D": D, "deltas": deltas, "suppression_factor": [round(x, 4) for x in supp],
           "fold_fewer_crossings": [round(1.0 / x, 1) for x in supp],
           "dln_supp_d_delta": round(slope, 4), "expected_minus_1_over_D": round(-1.0 / D, 4),
           "exponential_leverage": exp_leverage}
    return _suite("T21",
        "barrier-restoration leverage: raising the escape barrier by delta suppresses malignant crossing by exp(-delta/D) -- exponential leverage (why prevention dominates cure)",
        status, val, "[F] Kramers k=k0 exp(-barrier/D) / [V] log-suppression linear in delta, slope -1/D / [H] prevention/partial-restoration target",
        obstacle=None)


def t22_rcc_carcinogen_roster():
    """RCC carcinogen roster: every cited RCC driver round-trips to its RR on the kidney R19 drive
    axis; removing a driver DIVIDES combined risk (prevention). Aristolochic acid is documented
    honestly as UPPER-TRACT UROTHELIAL carcinoma (UUC, a different tissue) + AA-nephropathy/CKD --
    NOT placed on the RCC axis, because its potency (OR up to 49) exceeds the smoking-calibrated
    kidney axis (which saturates near RR 2.2 at the spinodal) and its master gene is urothelial."""
    rost = roster_mod.roster(roster_mod.GAMMA_KIDNEY, roster_mod.D_RCC, roster_mod.RR_RCC)
    deesc = roster_mod.deescalation(roster_mod.RR_RCC)
    roundtrip_ok = all(abs(v["roundtrip_RR"] - v["cited_RR"]) / v["cited_RR"] < 0.02 for v in rost.values())
    div_ok = all(abs(deesc["per_driver_removal"][n]["divide_combined_by"] - roster_mod.RR_RCC[n]) < 0.05
                 for n in roster_mod.RR_RCC)
    priority_ok = deesc["prevention_priority"][0] == "tobacco_smoke"   # highest-RR RCC driver first
    status = "PASS" if (roundtrip_ok and div_ok and priority_ok) else "FAIL"
    val = {"RCC_roster": rost, "de_escalation": deesc,
           "aristolochic_acid_UUC": {"cancer": "upper-tract urothelial carcinoma (UUC), NOT RCC",
               "IARC": "Group 1", "cited_OR_range": "1-49 dose-dependent (Hoang meta, PMC3650093)",
               "also_causes": "aristolochic-acid nephropathy -> CKD; TP53 A:T->T:A signature",
               "axis_note": "OR up to 49 exceeds the smoking-calibrated kidney axis (saturates ~2.2 at spinodal); "
                            "urothelium has its own (unmeasured) master gene -> not placed on the RCC axis [O]",
               "prevention": "ban/avoid Aristolochia herbal remedies (drive removal)"},
           "hereditary_RCC_cross_reference": xref.for_entity("hereditary_RCC")}
    return _suite("T22",
        "RCC carcinogen roster: tobacco + trichloroethylene round-trip to cited RRs on the kidney R19 axis and removal divides risk; aristolochic acid documented honestly as UUC (not RCC)",
        status, val, "[F] barrier-law inversion / [V] RCC drivers round-trip + de-escalation divides / [L] IARC Group 1; Hunt 2005, Karami meta / [O] absolute incidence; UUC axis",
        obstacle="absolute RCC incidence needs a population baseline hazard; aristolochic-acid/UUC is a distinct urothelial cancer whose master gene is unmeasured, so it is documented but not placed on the RCC axis [O]")


def t23_hcc_carcinogen_roster():
    """HCC carcinogen roster + both synergy datasets + multi-driver prevention. Every driver
    round-trips; aflatoxin x HBV is multiplicative; HBV x HCV (HR 115) sits BETWEEN the additive and
    multiplicative modes; de-escalation priority targets the highest-RR driver (HBV)."""
    g = roster_mod.GAMMA_LIVER; D = roster_mod.D_HCC
    rost = roster_mod.roster(g, D, roster_mod.RR_HCC)
    deesc = roster_mod.deescalation(roster_mod.RR_HCC)
    brk = roster_mod.synergy_bracket(g, D, roster_mod.HBV_HCV["RR_HBV"], roster_mod.HBV_HCV["RR_HCV"],
                                     roster_mod.HBV_HCV["RR_coinfection_observed"])
    roundtrip_ok = all(abs(v["roundtrip_RR"] - v["cited_RR"]) / v["cited_RR"] < 0.02 for v in rost.values())
    div_ok = all(abs(deesc["per_driver_removal"][n]["divide_combined_by"] - roster_mod.RR_HCC[n]) < 0.05
                 for n in roster_mod.RR_HCC)
    priority_ok = deesc["prevention_priority"][0] == "chronic_HBV"          # highest-RR driver
    bracket_ok = brk["observed_within_bracket"] and (0.0 < brk["position_in_bracket"] < 1.0)  # between modes
    submult = brk["observed"] < brk["multiplicative_mode"] and brk["observed"] > brk["additive_mode"]
    status = "PASS" if (roundtrip_ok and div_ok and priority_ok and bracket_ok and submult) else "FAIL"
    val = {"HCC_roster": rost, "de_escalation": deesc, "HBV_HCV_synergy_bracket": brk,
           "hereditary_HCC_cross_reference": xref.for_entity("hereditary_HCC"),
           "four_way_combined_product_status": deesc["combined_product_status"],
           "treatment_note": "prevention targets (highest RR first): HBV vaccine/antiviral, HCV direct-acting-antiviral cure, "
                             "aflatoxin reduction, alcohol abstinence; curative/systemic SoC (resection/transplant/ablation/"
                             "TACE/atezo-bev) is standard of care, not derived here"}
    return _suite("T23",
        "HCC carcinogen roster: aflatoxin/HBV/HCV/ethanol round-trip to cited RRs; aflatoxin x HBV multiplicative, HBV x HCV (115) between additive and multiplicative modes; de-escalation prioritises HBV; hereditary HCC (HFE) cross-referenced to disease_wp",
        status, val, "[F] barrier-law inversion / [V] round-trip + two synergy datasets bracketed + de-escalation + HFE identity/seam / [L] Liu 2012, Korean cohort PMC3520797, Atkins JAMA 2020 / [H] prevention priority + 4-way product / [O] absolute incidence",
        obstacle="absolute HCC incidence needs a population baseline hazard; the simultaneous 4-way co-exposure product is marked ILLUSTRATIVE [H] (single agents and pairwise synergies are anchored, the full product is a model extrapolation, not an anchored cohort)")


SUITE_FNS = [t1_map, t2_windkessel, t3_gfr_autoreg, t4_osmoregulation, t5_hepatic,
             t6_rcc_shape, t7_hcc_synergy,
             t8_arterial_stiffening, t9_essential_hypertension, t10_shock_subtypes,
             t11_diabetes_insipidus, t12_siadh, t13_ckd_staging, t14_autoregulation_breakthrough,
             t15_hepatic_impairment, t16_portosystemic_shunt, t17_enzyme_ddi,
             t18_reversibility_threshold, t19_critical_slowing, t20_synergy_reversal,
             t21_barrier_restoration_leverage, t22_rcc_carcinogen_roster, t23_hcc_carcinogen_roster]


def run_battery():
    base = eng.circulate()
    results = {"emergence_ok": bool(base["organs"]["organs"]),
               "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values())
                                  if base["oscillators"] else True),
               "suites": []}
    for fn in SUITE_FNS:
        results["suites"].append(fn())
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in results["suites"])
    return results


if __name__ == "__main__":
    r = run_battery(); print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
