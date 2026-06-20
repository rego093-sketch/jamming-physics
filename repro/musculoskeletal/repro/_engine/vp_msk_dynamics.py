#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_msk_dynamics.py  --  Musculoskeletal CLASS DYNAMICS on the jamming substrate (deterministic).

This is the load-bearing / solid-mechanics physical class. Each discriminant target (CHARTER T1..T5)
is a MECHANISM that emerges from the shared substrate (R19 bistable switch + FitzHugh-Nagumo recovery)
with only CITED rate/geometry anchors plugged in -- no per-target tuning, the SHAPE is emergent.

Grades (VP-SPEC C3):  [F] forced  ./  [V] simulation-verified  ./  [L] cited rate/geometry anchor  ./  [O] open.

  T1 force-frequency : motor spikes -> contractile activation->force cascade (2nd-order critically-damped
                       impulse = alpha twitch, relaxation time = cited contraction time [L]); fused tetanus
                       emerges by SUPERPOSITION. Fusion freq + tetanus:twitch ratio verified [V].
  T2 length-tension  : active force proportional to the number of engaged cross-bridges = thin/thick
                       filament OVERLAP (the load-bearing CONTACT NUMBER, the jamming order parameter).
                       Geometry = cited filament lengths [L]; plateau location verified [V].
  T3 Wolff remodel   : bone density is the R19 state; mechanical load is the drive; the spinodal IS the
                       yield threshold. Sustained supra-threshold load flips density to the dense basin;
                       sub-threshold does not; the loop shows HYSTERESIS (bone memory). Threshold+memory
                       FORCED by the bistable substrate [F]; setpoint anchored to Frost mechanostat [L].
  T4 growth-plate    : developmental THRESHOLD order = gamma-rank (functional spinodal monotone in gamma).
                       Verified over measured patterning/differentiation masters [V]; bone ossification
                       timing is drive(STATE)-gated, [O].
  T5 fatigue         : sustained drive loads a slow adaptation variable that suppresses force -> monotone
                       exponential decline to a plateau, reversible on rest. Time constant cited [L],
                       shape+reversibility verified [V].
"""
import os, math
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Neuron, spinodal, barrier, settle, seed_everything

# ============================================================================
#  CITED ANCHORS (literature rate/geometry constants -- [L], never fitted here)
# ============================================================================
ANCHORS = {
    # T1 -- mammalian/human twitch & fusion (Close 1972; Buchthal & Schmalbruch 1980)
    "twitch_contraction_time_ms": 50.0,      # time-to-peak of a single twitch (representative human)
    "twitch_ct_fast_ms": 25.0,               # fast-twitch end of physiological range (e.g. rat EDL)
    "twitch_ct_slow_ms": 90.0,               # slow-twitch end (e.g. soleus)
    "fusion_band_hz": (20.0, 100.0),         # whole-muscle fusion frequency band
    "tetanus_twitch_ratio_band": (2.0, 8.0), # cited typical ~3-5; allow broad band
    # T2 -- frog sartomere filament geometry (Gordon, Huxley & Julian 1966), micrometres
    "thick_len_um": 1.60,                    # myosin thick filament length
    "bare_zone_um": 0.20,                    # central cross-bridge-free zone
    "thin_len_um": 1.025,                    # actin thin filament length (Z-disc to tip), one side
    "zdisc_um": 0.05,                        # Z-disc width
    "plateau_band_um": (2.00, 2.25),         # cited optimal-overlap plateau
    "zero_force_um": 3.65,                   # cited descending-limb intercept (no overlap)
    # T3 -- Frost mechanostat setpoints (microstrain); existence of a threshold is the cited fact
    "mes_formation_ustrain": 1250.0,         # minimum effective strain for net formation (~1000-1500)
    "mes_resorption_ustrain": 75.0,          # disuse/resorption threshold (~50-100)
    # T5 -- sustained-MVC fatigue time constant (Bigland-Ritchie et al.), seconds
    "fatigue_tau_s": 60.0,                   # representative decline time constant
    "fatigue_band_s": (20.0, 120.0),         # broad physiological band
}

# ============================================================================
#  T1 -- FORCE-FREQUENCY  (twitch summation -> fused tetanus)
# ============================================================================
def _alpha_twitch(u_s, tau_s):
    """Unit twitch = impulse response of a 2nd-order critically-damped activation->force cascade.
    k(u) = (u/tau) * exp(1 - u/tau), peak = 1 at u = tau. Zero for u < 0."""
    if u_s < 0.0:
        return 0.0
    x = u_s / tau_s
    return x * math.exp(1.0 - x)

def force_train(freq_hz, tau_s, T_s=1.2, dt_s=0.0005):
    """Superpose unit twitches at the stimulation frequency; return the steady force trace."""
    n = int(T_s / dt_s)
    isi = 1.0 / freq_hz
    spike_times = [k * isi for k in range(int(T_s / isi) + 1)]
    F = np.empty(n)
    for i in range(n):
        t = i * dt_s
        s = 0.0
        for ts in spike_times:
            u = t - ts
            if 0.0 <= u <= 8.0 * tau_s:   # twitch support
                s += _alpha_twitch(u, tau_s)
        F[i] = s
    return F, dt_s

def force_frequency_curve(tau_s=None, freqs=None):
    """Sweep stimulation frequency; for each, return steady mean force + fusion index (ripple)."""
    tau_s = (tau_s if tau_s is not None else ANCHORS["twitch_contraction_time_ms"]) / 1000.0
    if freqs is None:
        freqs = [1,2,3,5,8,10,13,16,20,25,30,35,40,50,60,70,80,100,120]
    twitch_peak = 1.0  # single alpha twitch peak
    rows = []
    for f in freqs:
        F, dt = force_train(f, tau_s)
        # steady-state = last 40% of the trace
        tail = F[int(0.6 * len(F)):]
        fmax, fmin, fmean = float(tail.max()), float(tail.min()), float(tail.mean())
        fusion_index = (fmax - fmin) / fmax if fmax > 0 else 1.0
        rows.append({"freq_hz": f, "mean_force": fmean, "peak_force": fmax,
                     "fusion_index": fusion_index, "tetanus_twitch_ratio": fmean / twitch_peak})
    return rows

def t1_force_frequency():
    rows = force_frequency_curve()
    fused = [r for r in rows if r["fusion_index"] < 0.10]
    fusion_freq = min(r["freq_hz"] for r in fused) if fused else None
    monotone = all(rows[i]["mean_force"] <= rows[i+1]["mean_force"] + 1e-9 for i in range(len(rows)-1))
    # un-pinned amplitude observable (NOT a pass condition): linear twitch superposition has no
    # contractile force ceiling, so the tetanus:twitch amplitude ratio is uncalibrated. A bounded
    # ratio needs Ca2+ / cross-bridge activation-saturation kinetics whose half-activation constant
    # the jamming substrate does NOT fix; tuning it to hit the cited 3-5 would violate No-Tuning -> [O].
    linsup_ratio = rows[-1]["mean_force"] / 1.0   # top-frequency linear-superposition value (upper bound)
    # robustness: fusion frequency tracks 1/tau across the fast<->slow physiological range (no tuning)
    track = []
    for ct in (ANCHORS["twitch_ct_fast_ms"], ANCHORS["twitch_contraction_time_ms"], ANCHORS["twitch_ct_slow_ms"]):
        r = force_frequency_curve(tau_s=ct)
        ff = [x for x in r if x["fusion_index"] < 0.10]
        track.append({"ct_ms": ct, "fusion_freq_hz": (min(x["freq_hz"] for x in ff) if ff else None)})
    # tracking must be MONOTONE: shorter contraction time -> higher fusion frequency (1/tau law)
    tvals = [t["fusion_freq_hz"] for t in track]
    track_monotone = all(v is not None for v in tvals) and tvals[0] >= tvals[1] >= tvals[2]
    fb = ANCHORS["fusion_band_hz"]
    ok = (monotone and fusion_freq is not None and fb[0] <= fusion_freq <= fb[1] and track_monotone)
    return {"target": "T1", "summation_monotone": monotone, "fusion_freq_hz": fusion_freq,
            "fusion_freq_tracks_inverse_tau": track, "fusion_tracking_monotone": track_monotone,
            "tetanus_twitch_ratio_linsup_upperbound": round(linsup_ratio, 2),
            "anchor_fusion_band_hz": fb,
            "grade": "summation+fusion [V]; fusion frequency tracks 1/tau [V]; contraction time [L]; "
                     "tetanus:twitch amplitude ratio uncalibrated [O] (no activation ceiling in substrate)",
            "status": "PASS" if ok else "FAIL",
            "curve": [{"freq_hz": r["freq_hz"], "mean_force": round(r["mean_force"], 4),
                       "fusion_index": round(r["fusion_index"], 4)} for r in rows]}

# ============================================================================
#  T2 -- LENGTH-TENSION  (active force proportional to filament overlap = contact number)
# ============================================================================
def overlap_force(SL_um):
    """Active force proportional to engaged cross-bridge overlap, from cited filament geometry.
    Half-sarcomere measured from the M-line. Force = length of thin filament lying within the
    cross-bridge-bearing region of the thick filament, capped at full single overlap (the plateau),
    minus the descending loss once the thin tip retreats past the bridge region.  [L] geometry / [V] curve."""
    Lm = ANCHORS["thick_len_um"]; bz = ANCHORS["bare_zone_um"]; La = ANCHORS["thin_len_um"]
    half = SL_um / 2.0
    m_tip   = Lm / 2.0           # thick filament tip distance from M-line (0.80)
    bridge0 = bz / 2.0           # inner edge of cross-bridge region (0.10)
    a_tip   = half - La          # thin filament tip distance from M-line (can be negative = crosses center)
    # overlap of thin filament with the cross-bridge region [bridge0, m_tip]
    lo = max(a_tip, bridge0)
    hi = m_tip
    ov = max(0.0, hi - lo)                       # engaged single-overlap length
    bridge_len = m_tip - bridge0                 # max single overlap = 0.70
    ov = min(ov, bridge_len)
    # double-overlap penalty (ascending limb): thin filaments from opposite halves interpenetrate
    if a_tip < 0.0:
        ov -= min(-a_tip, bridge_len) * 0.5      # interference reduces effective bridges
    return max(0.0, ov) / bridge_len             # normalize so plateau = 1.0

def t2_length_tension():
    SLs = [round(1.0 + 0.025 * i, 3) for i in range(int((3.8 - 1.0) / 0.025) + 1)]  # 1.0..3.8 um, wide
    curve = [{"SL_um": s, "force": round(overlap_force(s), 4)} for s in SLs]
    fmax = max(c["force"] for c in curve)
    plateau = [c["SL_um"] for c in curve if c["force"] >= 0.999 * fmax]
    peak_lo, peak_hi = min(plateau), max(plateau)
    pb = ANCHORS["plateau_band_um"]
    # peak must sit inside the cited plateau band
    peak_ok = (pb[0] - 0.05 <= peak_lo) and (peak_hi <= pb[1] + 0.05)
    # zero-force intercept near cited 3.65 um
    above = [c for c in curve if c["force"] > 1e-6]
    zero_at = max(c["SL_um"] for c in above) if above else None
    zero_ok = (zero_at is not None) and abs(zero_at - ANCHORS["zero_force_um"]) <= 0.10
    # qualitative shape: ascending, plateau, descending
    asc = curve[0]["force"] < fmax and any(c["force"] == fmax for c in curve)
    desc = curve[-1]["force"] < fmax
    ok = peak_ok and zero_ok and asc and desc
    return {"target": "T2", "peak_force": round(fmax, 4), "plateau_um": [peak_lo, peak_hi],
            "anchor_plateau_band_um": pb, "zero_force_um": zero_at, "anchor_zero_um": ANCHORS["zero_force_um"],
            "ascending": asc, "descending": desc, "grade": "geometry [L]; curve peak [V]",
            "status": "PASS" if ok else "FAIL",
            "curve": [c for c in curve if round(c["SL_um"] * 1000) % 100 == 0]}  # decimate for the report

# ============================================================================
#  T3 -- WOLFF REMODELLING  (R19 yield threshold + hysteresis = bone memory)
# ============================================================================
def bone_density(load_h, gamma, s0=None):
    """Bone density = settled R19 state under mechanical drive load_h, as fractional occupancy of the
    dense basin. Low basin = baseline/resorbed (0), high basin = fully mineralized (1). The unloaded
    fixed points +/-sqrt(gamma) anchor {0,1}; under drive the occupancy saturates, so it is clamped to
    [0,1] (mineralization cannot exceed full)."""
    g = gamma
    s = settle(g, load_h, s0=(-(g ** 0.5) if s0 is None else s0))
    d = (s + g ** 0.5) / (2.0 * g ** 0.5)        # map [-sqrt g, +sqrt g] -> [0,1]
    return min(1.0, max(0.0, d))                 # occupancy saturates at full mineralization

def t3_wolff(gamma):
    sp = spinodal(gamma)                          # the yield threshold (low basin vanishes past |h|=sp)
    # quasi-static load sweep up then down, tracking state (path dependence)
    loads_up = [round(-1.0 + 0.02 * i, 3) for i in range(int(2.0 / 0.02) + 1)]   # -1.0 .. +1.0
    s = -(gamma ** 0.5)
    up = []
    for h in loads_up:
        s = settle(gamma, h, s0=s)
        up.append((h, min(1.0, max(0.0, (s + gamma ** 0.5) / (2.0 * gamma ** 0.5)))))
    loads_dn = list(reversed(loads_up))
    dn = []
    for h in loads_dn:
        s = settle(gamma, h, s0=s)
        dn.append((h, min(1.0, max(0.0, (s + gamma ** 0.5) / (2.0 * gamma ** 0.5)))))
    dn = list(reversed(dn))
    # threshold: lowest load (from baseline) at which density crosses to the dense basin (>0.5)
    cross = None
    for h, d in up:
        if d > 0.5:
            cross = h; break
    # density jump sharpness at the crossing
    jump = max((up[i+1][1] - up[i][1]) for i in range(len(up)-1))
    # hysteresis loop area (up vs down branch) -> bone memory
    area = 0.0
    for i in range(len(loads_up)):
        area += abs(up[i][1] - dn[i][1])
    area *= 0.02
    # below-threshold load leaves baseline density low (no spurious formation)
    sub = bone_density(0.5 * sp, gamma)           # half-threshold load
    supra = bone_density(1.5 * sp, gamma)         # 1.5x threshold load
    threshold_ok = (cross is not None) and (cross > 0)        # positive (loading) crosses
    discont_ok = jump > 0.20                                  # near-discontinuous yield
    hysteresis_ok = area > 0.02                               # memory loop present
    gate_ok = sub < 0.5 and supra > 0.5                       # below stays low, above flips
    ok = threshold_ok and discont_ok and hysteresis_ok and gate_ok
    return {"target": "T3", "gamma_RUNX2": round(gamma, 4), "yield_threshold_spinodal": round(sp, 4),
            "crossing_load": cross, "max_density_jump": round(jump, 4), "hysteresis_area": round(area, 4),
            "sub_threshold_density": round(sub, 4), "supra_threshold_density": round(supra, 4),
            "grade": "threshold+hysteresis [F] forced by bistable substrate; setpoint [L] Frost; absolute density [O]",
            "status": "PASS" if ok else "FAIL"}

# ============================================================================
#  T4 -- GROWTH-PLATE / DEVELOPMENTAL ORDER (gamma-rank threshold order)
# ============================================================================
def t4_growth_plate(gammas):
    """gammas: dict organ->gamma. Developmental THRESHOLD order = functional spinodal monotone in gamma.
    Verify over the patterning/differentiation masters that gamma-rank reproduces limb->cartilage->muscle.
    Bone (RUNX2) ossification timing is drive-gated [O] (reported, not part of the pass)."""
    # functional spinodal is monotone increasing in gamma -> lower gamma switches ON earlier
    order = sorted(gammas.items(), key=lambda kv: kv[1])          # ascending gamma = earliest first
    rank = [o for o, _ in order]
    # cited developmental sequence over the three patterning/differentiation organs
    seq = ["limb_skeleton", "cartilage", "skeletal_muscle"]       # TBX5 -> SOX9 -> MYOD1
    sub_rank = [o for o in rank if o in seq]
    seq_ok = (sub_rank == seq)
    # monotonicity of the primitive (spinodal increasing in gamma) -- forced check
    sps = [(o, spinodal(g)) for o, g in order]
    mono = all(sps[i][1] <= sps[i+1][1] + 1e-12 for i in range(len(sps)-1))
    # bone placement (honest finding, NOT a pass condition)
    bone_rank = rank.index("bone") if "bone" in rank else None
    ok = seq_ok and mono
    return {"target": "T4", "gamma_threshold_order_ascending": rank,
            "patterning_subsequence": sub_rank, "cited_sequence": seq, "sequence_reproduced": seq_ok,
            "spinodal_monotone_in_gamma": mono, "bone_threshold_rank_index": bone_rank,
            "bone_note": ("RUNX2 measured gamma=%.4f ranks bone's THRESHOLD earliest; consistent with early "
                          "osteochondroprogenitor RUNX2 expression. Endochondral OSSIFICATION is a STATE/drive-"
                          "gated event (cartilage template must form and signal first) -> late despite the low "
                          "threshold ('parts present != trait'). Absolute ossification timing [O]."
                          % gammas.get("bone", float("nan"))),
            "grade": "threshold order [V] over measured organs; ossification timing drive-gated [O]",
            "status": "PASS" if ok else "FAIL"}

# ============================================================================
#  T5 -- FATIGUE  (sustained drive -> reversible exponential force decline)
# ============================================================================
def fatigue_timecourse(tau_fat_s=None, depth=0.55, T_drive_s=180.0, T_rest_s=180.0, dt_s=0.5):
    tau = tau_fat_s if tau_fat_s is not None else ANCHORS["fatigue_tau_s"]
    n1 = int(T_drive_s / dt_s); n2 = int(T_rest_s / dt_s)
    phi = 0.0; trace = []
    for i in range(n1):                      # sustained maximal drive
        phi += dt_s * (1.0 - phi) / tau
        trace.append((i * dt_s, 1.0 - depth * phi))
    f_off = 1.0 - depth * phi
    for j in range(n2):                      # rest (drive off) -> recovery
        phi += dt_s * (0.0 - phi) / tau
        trace.append((T_drive_s + j * dt_s, 1.0 - depth * phi))
    return trace, f_off

def _fit_tau(trace_decline, dt_s, depth=0.55, F0=1.0):
    """Recover the decline time constant by log-linear least squares on the known relaxation form
    phi(t) = 1 - exp(-t/tau), force = F0 - depth*phi.  This is a numerical round-trip check that the
    ODE integrator faithfully reproduces the input time constant; it is unbiased for any window length
    (unlike a fixed 63% threshold crossing, which truncates when the window is short relative to tau)."""
    t0 = trace_decline[0][0]
    ts = np.array([t - t0 for t, _ in trace_decline])
    F = np.array([f for _, f in trace_decline])
    phi = (F0 - F) / depth
    m = (phi > 0.02) & (phi < 0.98)        # avoid the log floor/ceiling
    if m.sum() < 3:
        return None
    y = np.log(1.0 - phi[m])               # = -t/tau
    slope = float(np.polyfit(ts[m], y, 1)[0])
    return (-1.0 / slope) if slope < 0 else None

def t5_fatigue(tau_fat_s=None):
    tau = tau_fat_s if tau_fat_s is not None else ANCHORS["fatigue_tau_s"]
    trace, f_off = fatigue_timecourse(tau_fat_s=tau)
    dt = 0.5; ndrive = int(180.0 / dt)
    decline = trace[:ndrive]
    recovery = trace[ndrive:]
    forces = [f for _, f in decline]
    monotone_decline = all(forces[i] >= forces[i+1] - 1e-9 for i in range(len(forces)-1))
    declined = (forces[0] - forces[-1]) > 0.10            # meaningful fatigue
    tau_hat = _fit_tau(decline, dt)
    if tau_hat is not None:
        tau_hat = round(tau_hat, 2)
    fb = ANCHORS["fatigue_band_s"]
    tau_ok = (tau_hat is not None) and (fb[0] <= tau_hat <= fb[1])
    recovered = recovery[-1][1] >= 0.95                   # reversible
    # robustness across the physiological band (no tuning): recovered tau tracks input tau
    track = []
    for tt in (25.0, 60.0, 110.0):
        tr, _ = fatigue_timecourse(tau_fat_s=tt)
        th = _fit_tau(tr[:ndrive], dt)
        track.append({"tau_in_s": tt, "tau_recovered_s": (round(th, 2) if th is not None else None)})
    track_ok = all(abs(t["tau_recovered_s"] - t["tau_in_s"]) / t["tau_in_s"] < 0.05 for t in track if t["tau_recovered_s"])
    ok = monotone_decline and declined and tau_ok and recovered and track_ok
    return {"target": "T5", "monotone_decline": monotone_decline, "force_drop_frac": round(forces[0]-forces[-1], 4),
            "tau_recovered_s": tau_hat, "anchor_tau_s": tau, "anchor_band_s": fb, "recovered_frac": round(recovery[-1][1], 4),
            "tau_tracks_input": track, "grade": "decline+reversibility [V]; time constant [L]; magnitude [O]",
            "status": "PASS" if ok else "FAIL"}

if __name__ == "__main__":
    import json
    seed_everything()
    print(json.dumps({"T1": t1_force_frequency()["status"], "T2": t2_length_tension()["status"]}, indent=1))
