#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
disease_battery.py  --  STRESS BATTERY for the disease extension (D1-D6).

Same research-first discipline as stress_tests.py: each disease target is exercised and must reproduce
the PREDICTED qualitative behavior of the object it reuses, under a sweep, with NO per-target tuning of
the cited anchors. The grades here are mostly [V?] (coherent mechanism reuse that needs an independent
dataset to promote to [V]) and absolutes stay [O] -- a PASS means "the reused mechanism produces the
predicted shape/direction", NOT that the absolute clinical magnitude is reproduced. This battery does
NOT unlock the canonical site; it is a separate research artifact for the extension program.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import importlib
rd = importlib.import_module("respiratory_disease")

def _suite(tid, name, status, value, grade, note=None):
    return {"target": tid, "disease": name, "status": status, "value": value, "grade": grade, "note": note}

def d1_mayer():
    r = rd.mayer_waves()
    in_band = r["any_in_mayer_band"]
    ratio_ok = 2.0 <= r["period_over_delay_mean"] <= 3.0   # forced ~2x family (as Cheyne-Stokes T4)
    status = "PASS" if (in_band and ratio_ok) else "FAIL"
    return _suite("D1", "Mayer waves (~0.1 Hz)", status,
                  {"any_in_mayer_band": in_band, "period_over_delay_mean": r["period_over_delay_mean"]},
                  "[V] mechanism reuse (T5); [L] absolute frequency",
                  "baroreflex self-oscillates by the same forced relation as Cheyne-Stokes")

def d2_asthma():
    ch = rd.asthma_challenge(); hy = rd.asthma_hysteresis()
    ci = [row["constriction_index"] for row in ch["rows"]]
    monotone = all(b >= a - 1e-9 for a, b in zip(ci, ci[1:]))
    collapses = any(not row["open_basin_exists"] for row in ch["rows"])     # open basin vanishes at spinodal
    reversible = hy["reversible"] and (hy["hysteresis_width"] or 0) > 0
    status = "PASS" if (monotone and collapses and reversible) else "FAIL"
    return _suite("D2", "Asthma (airway-tone switch)", status,
                  {"convex_monotone_shape": monotone, "spinodal_collapse": collapses,
                   "reversible_hysteresis": reversible, "hysteresis_width": hy["hysteresis_width"],
                   "pc20_bias": ch["pc20_bias"]},
                  "shape [V] (reuses oncology kernel); hysteresis [V?]; absolute PC20 [O]",
                  "reversible bias = bronchodilator; PC20 absolute needs calibration")

def d3_osa():
    lg = rd.osa_loop_gain_endotype(); ph = rd.osa_pharyngeal_collapse()
    stable_below = all((not row["unstable"]) for row in lg["rows"] if row["loop_gain_ratio"] <= 1.0)
    unstable_above = all(row["unstable"] for row in lg["rows"] if row["loop_gain_ratio"] > 1.0)
    collapse = ph["discontinuous_collapse"] and (ph["hysteresis_width"] or 0) > 0
    status = "PASS" if (stable_below and unstable_above and collapse) else "FAIL"
    return _suite("D3", "OSA (loop-gain + Pcrit switch)", status,
                  {"stable_below_LG1": stable_below, "unstable_above_LG1": unstable_above,
                   "pharyngeal_collapse_hysteretic": collapse, "pcrit_spinodal": ph["pcrit_spinodal"]},
                  "loop-gain endotype [V] (T2 reuse); Pcrit collapse [V?]; absolute Pcrit [O]",
                  "LG/LGc is exactly the clinical loop-gain endotype")

def d4_csa():
    alt = rd.csa_altitude(); hf = rd.csa_heart_failure(); op = rd.csa_opioid()
    alt_ok = alt["onset_gain_ratio"] is not None
    hf_ok = hf["any_in_csr_band"] and (1.7 <= (hf["slope"] or 0) <= 2.4)
    op_ok = (op["apnea_below_drive"] is not None) and op["robust_to_moderate_cut"]
    status = "PASS" if (alt_ok and hf_ok and op_ok) else "FAIL"
    return _suite("D4", "CSA spectrum (altitude/CHF/opioid)", status,
                  {"altitude_onset": alt["onset_gain_ratio"], "chf_in_csr_band": hf["any_in_csr_band"],
                   "chf_period_slope": hf["slope"], "opioid_quench_drive": op["apnea_below_drive"]},
                  "directions [V] (T2/T4 reuse); absolute thresholds [O]",
                  "three diseases = three axes of one apnea machinery")

def d5_fever():
    fv = rd.fever_coscaling()
    co = fv["co_scale_same_direction"]
    status = "PASS" if co else "FAIL"
    return _suite("D5", "Fever HR-RR co-scaling", status,
                  {"co_scale_same_direction": co, "hr_bpm_per_C": fv["hr_bpm_per_C"],
                   "rr_bpm_per_C": fv["rr_bpm_per_C"], "hr_rr_ratio": fv["hr_rr_coscaling_ratio"],
                   "cited_rule_bpm_per_C": fv["cited_hr_rule_bpm_per_C"]},
                  "co-scaling DIRECTION [V?] (substrate-distinctive); absolute slope [O]",
                  "shared gamma(T) forces HR & RR to move together; magnitude has exogenous "
                  "(metabolic/autonomic) contributions -> absolute is open")

def d6_cough():
    co = rd.cough_threshold()
    status = "PASS" if (co["all_or_none"] and co["threshold_amp"] is not None) else "FAIL"
    return _suite("D6", "Cough (excitable threshold)", status,
                  {"all_or_none": co["all_or_none"], "threshold_amp": co["threshold_amp"],
                   "resting_peak": co["resting_peak"], "fired_peak": co["fired_peak"]},
                  "all-or-none excitation [V?]; absolute capsaicin C5 [O]",
                  "FHN in the excitable (sub-Hopf) regime: single stereotyped pulse")

def run_battery():
    suites = [d1_mayer(), d2_asthma(), d3_osa(), d4_csa(), d5_fever(), d6_cough()]
    return {"suites": suites, "all_targets_pass": all(s["status"] == "PASS" for s in suites),
            "n_pass": sum(s["status"] == "PASS" for s in suites), "n_total": len(suites)}

if __name__ == "__main__":
    r = run_battery()
    print("=" * 86)
    print("DISEASE EXTENSION STRESS BATTERY  (D1-D6)  --  mechanism reuse, no new substrate primitive")
    print("=" * 86)
    for s in r["suites"]:
        print(f"{s['target']}  [{s['status']}]  {s['disease']:34}  {s['grade']}")
        print(f"        value: {json.dumps(s['value'], ensure_ascii=False)}")
    print(f"\n{r['n_pass']}/{r['n_total']} disease targets pass.")
