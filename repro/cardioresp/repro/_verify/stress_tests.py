#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Cardiorespiratory STRESS BATTERY (T1-T5), exercised under WIDE sweeps.

VP-SPEC discipline (very high bar): every target is swept (not a single happy path) and must hold
with ONE shared physiological parameter set (cited anchors are not tuned per target). A target may
be [O] with a STATED obstacle; a silent pass is not allowed. run_battery() must be all PASS before
gates.write_research_complete() and PHASE=writing. Each suite returns value/grade/obstacle + raw sweep.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import importlib
eng = importlib.import_module("vp_car_engine")

# ---- cited anchors (grade [L]; NOT tuned to pass a target) -----------------------------------------
EUPNEA_BPM   = (12.0, 18.0)     # Guyton/Hall normal resting respiratory rate, breaths/min
HF_BAND_HZ   = (0.15, 0.40)     # Task Force 1996 high-frequency HRV band (vagal/RSA)
BRS_CITED    = 1.0              # baroreflex sensitivity ~1 bpm/mmHg (HR-BP slope), order-of-magnitude
BRS_TOL      = 0.30            # +/-30% tolerance on the anchored gain magnitude
LAT_CITED    = 0.6             # vagal baroreflex latency ~0.5-1 s
CSR_SLOPE_LO, CSR_SLOPE_HI = 1.7, 2.4   # "period ~= 2 x circulatory delay"

def _suite(tid, desc, status, value, grade, obstacle=None, sweep=None):
    return {"target": tid, "description": desc, "status": status, "value": value,
            "grade": grade, "obstacle_if_open": obstacle, "sweep": sweep}

# ===================================================================================================
def t1_eupnea():
    e = eng.eupnea_period()
    bpm = e["breaths_per_min"]
    in_band = EUPNEA_BPM[0] <= bpm <= EUPNEA_BPM[1]
    oscillates_all = all(r["oscillates"] for r in e["sweep"])
    bpm_vals = [r["breaths_per_min"] for r in e["sweep"] if r["oscillates"]]
    sweep_ok = oscillates_all and (min(bpm_vals) >= 8.0 and max(bpm_vals) <= 24.0)  # stays respiratory
    status = "PASS" if (in_band and sweep_ok) else "FAIL"
    return _suite("T1",
        "preBotC FHN intrinsic period matches cited 12-18 breaths/min; rate via single anchor",
        status, {"breaths_per_min": bpm, "ratio_breath_to_beat": e["ratio_breath_to_beat"],
                 "in_eupnea_band": in_band, "robust_across_drive": sweep_ok},
        "[V] ratio is structural (tau_s); [L] absolute rate anchored to resting_hr", sweep=e["sweep"])

# ===================================================================================================
def t2_apnea_threshold():
    sweep = []; ok = True
    for tau_d in (12.0, 20.0):
        stable_amps, unstable_amps = [], []
        for lg in (0.5, 0.7, 0.9, 1.1, 1.3, 2.0):
            r = eng.chemoreflex_sim(lg, tau_d)
            sweep.append({"tau_d": tau_d, "LG_ratio": lg, "amp_late": r["amp_late"],
                          "sustained": r["sustained"], "apnea_fraction": r["apnea_fraction"]})
            (unstable_amps if lg > 1.0 else stable_amps).append(r["amp_late"])
        # clean bifurcation: all sub-critical stable (~0), all super-critical sustained, separation wide
        sub_ok   = all(a < 0.05 for a in stable_amps)
        super_ok = all(a > 0.10 for a in unstable_amps)
        sep_ok   = (min(unstable_amps) > 3.0 * (max(stable_amps) + 1e-6))
        ok = ok and sub_ok and super_ok and sep_ok
    status = "PASS" if ok else "FAIL"
    return _suite("T2",
        "chemoreflex loop-gain > 1 -> periodic-breathing onset (Hopf bifurcation at LG_c~1)",
        status, {"bifurcation_at_LG_ratio": 1.0, "clean_separation": ok,
                 "LG_c_example_tau15": eng.chemoreflex_marginal(15.0, 1.0)["LG_c"]},
        "[V] bifurcation existence + apnea clamp; threshold normalized to its critical value", sweep=sweep)

# ===================================================================================================
def t3_rsa():
    sweep = []
    off = eng.rsa(0.0); sweep.append({"phase": "decoupled", **{k: off.get(k) for k in ("eps","hrv_peak_hz","f_resp_hz","locked")}})
    coupled_lock = True
    for eps in (0.02, 0.05, 0.10):
        r = eng.rsa(eps); sweep.append({"phase": "coupled", **{k: r.get(k) for k in ("eps","hrv_peak_hz","f_resp_hz","peak_power","locked")}})
        coupled_lock = coupled_lock and bool(r.get("locked"))
    # tracking: HRV peak follows the respiratory frequency as breathing rate changes
    track = []
    track_ok = True
    for fs in (0.85, 1.0, 1.20):
        r = eng.rsa(0.06, f_scale=fs)
        track.append({"f_scale": fs, "f_resp_hz": r.get("f_resp_hz"), "hrv_peak_hz": r.get("hrv_peak_hz"), "locked": r.get("locked")})
        track_ok = track_ok and bool(r.get("locked"))
    off_unlocked = (not off.get("locked"))
    status = "PASS" if (off_unlocked and coupled_lock and track_ok) else "FAIL"
    return _suite("T3",
        "HF-HRV spectral peak locks to the respiratory frequency only when CPGs are coupled",
        status, {"decoupled_locked": off.get("locked"), "coupled_locked": coupled_lock,
                 "peak_tracks_resp_freq": track_ok, "hf_band_hz": list(HF_BAND_HZ)},
        "[V] coupling creates an HF-HRV peak at f_resp; absent when decoupled", sweep=sweep + [{"tracking": track}])

# ===================================================================================================
def t4_cheyne_stokes():
    cs = eng.cheyne_stokes()
    slope = cs["period_vs_delay_slope"]
    ratios = [r["period_over_delay"] for r in cs["rows"] if r["period_over_delay"]]
    slope_ok  = (slope is not None and CSR_SLOPE_LO <= slope <= CSR_SLOPE_HI)
    ratios_ok = all(CSR_SLOPE_LO <= x <= CSR_SLOPE_HI for x in ratios) and len(ratios) >= 4
    status = "PASS" if (slope_ok and ratios_ok) else "FAIL"
    return _suite("T4",
        "Cheyne-Stokes period ~= 2 x circulatory delay (the forced number on the page)",
        status, {"period_vs_delay_slope": slope, "all_ratios_near_2": ratios_ok,
                 "forced_relation": "T_CSR ~= 2 * tau_circ"},
        "[V] limit-cycle period scales ~2x the transport delay (fast-plant, delay-dominated regime)",
        sweep=cs["rows"])

# ===================================================================================================
def t5_baroreflex():
    sweep = []; sign_ok = True; gain_ok = True
    for dP in (-20.0, -10.0, 10.0, 20.0, 30.0):
        r = eng.baroreflex_static(BRS=BRS_CITED, lat=LAT_CITED, dP=dP)
        sweep.append({"dP_mmHg": dP, "dHR_bpm": r["dHR_bpm"], "slope": r["slope_bpm_per_mmHg"],
                      "onset_latency_s": r["onset_latency_s"], "sign_correct": r["sign_correct"]})
        sign_ok = sign_ok and r["sign_correct"]
        gain_ok = gain_ok and (abs(abs(r["slope_bpm_per_mmHg"]) - BRS_CITED) <= BRS_TOL)
    # latency reflects the cited value
    lat_meas = eng.baroreflex_static(dP=20.0)["onset_latency_s"]
    lat_ok = (lat_meas is not None and abs(lat_meas - LAT_CITED) <= 0.25)
    # closed-loop: disturbances corrected, HR returns to setpoint, sign correct
    closed = []; closed_ok = True
    for amp in (-30.0, -15.0, 15.0, 30.0):
        c = eng.baroreflex_closed(amp=amp)
        closed.append({"disturb": amp, "peak_dHR_bpm": c["peak_dHR_bpm"], "final_dHR": c["final_dHR_bpm"],
                       "returned": c["returned_to_setpoint"], "sign_correct": c["sign_correct"]})
        closed_ok = closed_ok and c["returned_to_setpoint"] and c["sign_correct"]
    status = "PASS" if (sign_ok and gain_ok and lat_ok and closed_ok) else "FAIL"
    return _suite("T5",
        "a BP step is corrected by an HR change with cited gain/latency; setpoint = resting_hr",
        status, {"sign_correct": sign_ok, "gain_matches_cited_BRS": gain_ok, "BRS_bpm_per_mmHg": BRS_CITED,
                 "latency_matches_cited": lat_ok, "closed_loop_regulates": closed_ok, "setpoint_hr_bpm": 70.0},
        "[L] gain/latency anchored to cited baroreflex values; regulation to setpoint verified",
        sweep=sweep + [{"closed_loop": closed}])

# ===================================================================================================
def run_battery():
    base = eng.circulate()
    suites = [t1_eupnea(), t2_apnea_threshold(), t3_rsa(), t4_cheyne_stokes(), t5_baroreflex()]
    return {"emergence_ok": bool(base["organs"]["organs"]),
            "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values())
                               if base["oscillators"] else False),
            "suites": suites,
            "all_targets_pass": all(s["status"] == "PASS" for s in suites)}

if __name__ == "__main__":
    r = run_battery()
    for s in r["suites"]:
        print(f"{s['target']}  [{s['status']}]  {s['description']}")
        print("        value:", json.dumps(s["value"], ensure_ascii=False))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
