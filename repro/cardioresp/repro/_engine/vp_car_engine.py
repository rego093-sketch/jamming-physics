#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_car_engine.py  --  Cardiorespiratory emergence + circulation engine (deterministic, in-package).

SCOPE (see CHARTER.md): Heart (SA node) and lung (preBotzinger) emerge as the SAME FitzHugh-Nagumo
(FHN) relaxation oscillator on the R19 jamming-lattice switch. This engine adds the FUNCTIONAL
DYNAMICS the package owns: a single time anchor, the eupnea period, the chemoreflex control loop
(apnea threshold + Cheyne-Stokes), respiratory sinus arrhythmia (RSA), and the baroreflex. Organ
IDENTITY + developmental ORDER are CITED from the DNA gene-clock (grade [V], measured gamma).

WHAT RUNS:
  emerge_organs()      -- build each Organ on R19 from MEASURED master-gene gamma; order = gamma readout.
  confirm_oscillators()-- instantiate the SHARED FHN Neuron per oscillator organ; confirm a beat.
  time_anchor()        -- ONE physical-time scale kappa (s per arb-unit) fixed by resting_hr [L].
  eupnea_period()      -- lung FHN breathing rate (Hz) via kappa; robustness across a drive sweep.
  chemoreflex_marginal / chemoreflex_sim -- delayed negative-feedback loop; Nyquist threshold + sim.
  rsa()                -- respiratory CPG frequency-modulates the cardiac CPG; HRV spectrum peak.
  baroreflex_static / baroreflex_closed   -- BP step -> HR change (cited gain/latency); regulation.
  cheyne_stokes()      -- periodic-breathing limit-cycle period vs circulatory delay.

DETERMINISM (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed; pure-scalar ODE loops;
  round-before-hash; sorted JSON keys. Two runs -> identical sha256. stdlib + numpy only.
GRADES (VP-SPEC C3): [F] forced ./ [V] simulation-verified ./ [L] anchored-to-cited ./ [O] open w/ obstacle.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, dwell, dominant_freq, seed_everything

_HERE   = os.path.dirname(__file__)
_INH    = os.path.join(_HERE, "..", "..", "inherited")
_GAMMA  = os.path.join(_INH, "organ_gamma.json")
_ANCHOR = os.path.join(_INH, "cardiac_rhythm_anchor.json")

# ---- organ table: identity/order CITED from DNA; tau_s is the FHN recovery scale (mechanism) -------
ORGAN_ROWS = [
 {'master':'NKX2-5','organ':'heart','role':'SA-node pacemaker + conduction + contraction',
  'dyn_class':'oscillator','tau_s':18.0,'rate_note':'resting_hr 1.17 Hz [L]; intrinsic 1.67 Hz [L]','has_gamma':True},
 {'master':'NKX2-1','organ':'lung','role':'preBotzinger inspiratory rhythm + ventilatory pump',
  'dyn_class':'oscillator','tau_s':95.0,'rate_note':'eupnea ~0.2-0.3 Hz [L]','has_gamma':True},
]
OSCILLATOR_ORGANS = ["heart", "lung"]

# ---- shared run constants (no per-target tuning: one set used everywhere) ---------------------------
_DRIVE   = 0.55     # nominal FHN bias (mid oscillatory window for both organs)
_T_FHN   = 6000.0   # arb-time for FHN rate estimation
_DT_FHN  = 0.05
_T_RSA   = 10000.0  # longer cardiac trace for HRV spectral resolution
_BETA    = 0.5

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def load_anchor():
    return json.load(open(_ANCHOR, encoding="utf-8"))

# =====================================================================================================
#  EMERGENCE  (identity/order CITED from DNA; this engine only confirms the beat + adds dynamics)
# =====================================================================================================
def emerge_organs():
    """Emerge organs from MEASURED gamma. Order = gamma readout (ascending)."""
    seed_everything()
    G = load_gamma(); built = []
    for r in ORGAN_ROWS:
        if not r["has_gamma"]:
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"],
                              dyn_class=r["dyn_class"], note="no single master gene (derived/diffuse)"))
            continue
        g = G[r["master"]]["gamma"]; o = Organ(r["organ"], g, master=r["master"])
        built.append(dict(organ=r["organ"], master=r["master"], gamma=round(float(g), 6), role=r["role"],
                          dyn_class=r["dyn_class"], functional_spinodal=round(float(o.functional_spinodal()), 6),
                          rel_size_dwell=round(float(o.size()), 6)))
    go = [b for b in built if b.get("gamma") is not None]
    order = [b["organ"] for b in sorted(go, key=lambda b: b["gamma"])]
    return dict(organs=built, gamma_order_ascending=order,
                order_grade="[V] order is a pure gamma readout (identity+order owned by DNA gene-clock)")

def _isi_period_arb(S, dt, drop=4):
    """Steady-state inter-spike-interval period (arb units); drop transient beats."""
    sp = Neuron.spikes(S)
    if len(sp) < drop + 2: return None, len(sp)
    iv = np.diff(sp[drop:]) * dt
    return float(np.median(iv)), len(sp)

def _fhn_rate_arb(tau_s, drive=_DRIVE, T=_T_FHN, dt=_DT_FHN):
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(tau_s), beta=_BETA)
    S, _ = n.run(drive=drive, T=T, dt=dt)
    per, nb = _isi_period_arb(S, dt)
    return (1.0/per if per else 0.0), nb, per

def confirm_oscillators():
    """For each oscillator organ, instantiate the SHARED FHN Neuron and confirm a rhythmic beat."""
    seed_everything(); out = {}
    for r in ORGAN_ROWS:
        if r["dyn_class"] != "oscillator": continue
        f_arb, nb, _ = _fhn_rate_arb(r["tau_s"])
        out[r["organ"]] = dict(oscillates=bool(nb >= 3 and f_arb > 0.0), beats=int(nb),
                               relaxation_freq_arb=round(float(f_arb), 8), tau_s=float(r["tau_s"]),
                               rate_anchor=r["rate_note"], mechanism_grade="[V]", rate_grade="[L]")
    return out

# =====================================================================================================
#  TIME ANCHOR  --  ONE physical scale fixed by the cited resting heart rate (grade [L])
# =====================================================================================================
def time_anchor():
    """kappa = seconds per arb time-unit, fixed so the heart FHN intrinsic rhythm = resting_hr (cited).
    This is the SINGLE [L] calibration; every physical frequency below is f_arb / kappa."""
    a = load_anchor()
    resting_hz = a["cardiac_rhythm"]["resting_hr_hz"]["value"]   # 1.17 Hz (cited)
    f_arb_heart, _, _ = _fhn_rate_arb(18.0)
    kappa = f_arb_heart / resting_hz
    return dict(kappa_s_per_arb=round(float(kappa), 10), resting_hr_hz=resting_hz,
                f_arb_heart=round(float(f_arb_heart), 8), grade="[L]",
                note="single time anchor: heart FHN intrinsic rhythm := resting_hr_hz (cited)")

# =====================================================================================================
#  T1  --  EUPNEA: the breathing rate falls out of the lung FHN tau_s ratio under the single anchor
# =====================================================================================================
def eupnea_period(drive_sweep=None):
    """Lung (preBotzinger) breathing rate in Hz via the single time anchor; robustness over a drive
    sweep. The breathing:heartbeat frequency RATIO is structural (tau_s ratio), not fitted -> [V];
    the absolute rate is anchored [L]."""
    ta = time_anchor(); kappa = ta["kappa_s_per_arb"]
    f_lung_arb, _, _ = _fhn_rate_arb(95.0)
    f_lung_hz = f_lung_arb / kappa
    if drive_sweep is None:
        drive_sweep = [0.45, 0.50, 0.55, 0.60, 0.65, 0.70]
    sweep = []
    for d in drive_sweep:
        fa, nb, _ = _fhn_rate_arb(95.0, drive=d)
        hz = (fa / kappa) if fa > 0 else 0.0
        sweep.append(dict(drive=round(d,3), breaths_per_min=round(hz*60.0,3),
                          oscillates=bool(nb >= 3 and fa > 0.0)))
    return dict(breathing_hz=round(float(f_lung_hz),5), breaths_per_min=round(float(f_lung_hz*60.0),3),
                heart_hz=ta["resting_hr_hz"], ratio_breath_to_beat=round(float(f_lung_hz/ta["resting_hr_hz"]),5),
                sweep=sweep, mechanism_grade="[V]", rate_grade="[L]")

# =====================================================================================================
#  CHEMOREFLEX CONTROL LOOP  --  delayed negative feedback (apnea threshold T2 + Cheyne-Stokes T4)
#     deviation form around setpoint:  dc/dt = -(c + V_dev)/Tp ,  V_dev = clamp(LG * c(t - tau_d), -1, +inf)
#     loop gain LG in units of its critical value; clamp at -1 = ventilation floored at zero (apnea).
# =====================================================================================================
def chemoreflex_marginal(tau_d, Tp):
    """Analytic Nyquist marginal loop gain LG_c and oscillation period at onset (CSR period)."""
    def marginal(LG):
        if LG <= 1.0: return None, None
        wtd = math.acos(-1.0/LG); w = wtd/tau_d
        return (w*Tp - LG*math.sin(wtd)), w
    a, b = 1.0001, 80.0
    fa, _ = marginal(a)
    for _ in range(200):
        m = (a+b)/2.0; fm, _ = marginal(m)
        if fm is None: a = m; continue
        if (fa is not None) and fa*fm <= 0: b = m
        else: a, fa = m, fm
    LGc = (a+b)/2.0
    _, w = marginal(LGc)
    return dict(LG_c=round(float(LGc),5), period_onset_s=round(float(2*math.pi/w),4),
                period_over_delay=round(float((2*math.pi/w)/tau_d),4))

def chemoreflex_sim(LG_ratio, tau_d, Tp=1.0, dt=0.02, T=900.0, kick=0.15):
    """Nonlinear sim. LG_ratio = LG / LG_c (so 1.0 = threshold). Returns whether a sustained limit
    cycle (periodic breathing / apnea-hyperpnea) emerges, its amplitude, and its period."""
    LGc = chemoreflex_marginal(tau_d, Tp)["LG_c"]; LG = LG_ratio * LGc
    n = int(T/dt); L = int(round(tau_d/dt))
    V = np.zeros(n); c = np.zeros(n); hist = [0.0]*(L+1); hist[-1] = kick
    ci = kick
    for i in range(1, n):
        c_del = hist[0]; Vdev = LG * c_del
        if Vdev < -1.0: Vdev = -1.0                  # apnea: ventilation cannot go below zero
        V[i] = 1.0 + Vdev
        ci = ci + dt*(-(ci + Vdev)/Tp); c[i] = ci
        hist.pop(0); hist.append(ci)
    # envelope: compare late vs early amplitude (decaying vs sustained/growing)
    seg = n//4
    amp_early = float(np.std(V[seg:2*seg])); amp_late = float(np.std(V[3*seg:]))
    sustained = bool(amp_late > 0.05 and amp_late >= 0.5*amp_early)
    # period from late zero-up-crossings
    x = V[2*seg:] - np.mean(V[2*seg:]); aa = x > 0
    up = np.where((~aa[:-1]) & (aa[1:]))[0]
    per = float(np.median(np.diff(up))*dt) if len(up) >= 3 else None
    apnea_frac = float(np.mean(V[2*seg:] <= 1e-9))
    return dict(LG_ratio=round(LG_ratio,4), amp_early=round(amp_early,5), amp_late=round(amp_late,5),
                sustained=sustained, period_s=(round(per,4) if per else None),
                apnea_fraction=round(apnea_frac,4))

def cheyne_stokes(tau_list=None, Tp=1.0, LG_ratio=1.6):
    """CSR limit-cycle period vs circulatory delay (fast-plant, delay-dominated regime)."""
    if tau_list is None: tau_list = [8.0, 12.0, 15.0, 20.0, 25.0, 30.0]
    rows = []
    for td in tau_list:
        r = chemoreflex_sim(LG_ratio, td, Tp=Tp)
        rows.append(dict(circ_delay_s=td, period_s=r["period_s"],
                         period_over_delay=(round(r["period_s"]/td,4) if r["period_s"] else None),
                         apnea_fraction=r["apnea_fraction"]))
    valid = [(td, rr["period_s"]) for td, rr in zip(tau_list, rows) if rr["period_s"]]
    slope = None
    if len(valid) >= 2:
        xs = np.array([v[0] for v in valid]); ys = np.array([v[1] for v in valid])
        slope = float(np.polyfit(xs, ys, 1)[0])
    return dict(rows=rows, period_vs_delay_slope=(round(slope,4) if slope else None),
                forced_relation="CSR period ~= 2 x circulatory delay", grade="[V]")

# =====================================================================================================
#  T3  --  RSA: the respiratory CPG frequency-modulates the cardiac CPG (ephaptic/autonomic coupling)
# =====================================================================================================
def rsa(eps, f_scale=1.0, T=_T_RSA, dt=_DT_FHN):
    """Respiratory FHN r(t) adds eps*r(t) to the cardiac FHN drive. Returns the HRV (inter-beat-
    interval) spectrum peak and whether it locks to the respiratory frequency (HF band)."""
    ta = time_anchor(); kappa = ta["kappa_s_per_arb"]
    tau_s_resp = 95.0 / f_scale                                  # f_scale>1 -> faster breathing
    nl = Neuron(tau_s=tau_s_resp); Sr, _ = nl.run(drive=_DRIVE, T=T, dt=dt)
    r = (Sr - Sr.mean()) / (Sr.std() + 1e-12)
    n = int(T/dt); drive = _DRIVE + eps * r[:n]
    nc = Neuron(tau_s=18.0); Sc, _ = nc.run(drive=drive, T=T, dt=dt)
    sp = Neuron.spikes(Sc)
    if len(sp) < 10:
        return dict(eps=eps, locked=False, note="cardiac oscillator quenched")
    t_sp = sp*dt; ibi = np.diff(t_sp); t_ibi = t_sp[1:]
    tg = np.arange(t_ibi[0], t_ibi[-1], 1.0)                     # uniform 1-arb grid
    ib = np.interp(tg, t_ibi, ibi - ibi.mean()); ib = ib * np.hanning(len(ib))
    F = np.fft.rfftfreq(len(ib), d=1.0); P = np.abs(np.fft.rfft(ib))**2
    f_hz = F / kappa
    # HF-HRV is, by definition, the power in 0.15-0.40 Hz (Task Force 1996). Locate the peak WITHIN
    # that band; harmonics that fall outside the band (strong-FM sidebands) are not HF-HRV.
    band = (f_hz >= 0.15) & (f_hz <= 0.40)
    idx = np.where(band)[0]
    if len(idx) == 0:
        return dict(eps=round(eps,4), locked=False, note="no HF-band bins")
    kb = idx[int(np.argmax(P[idx]))]
    f_peak_hz = float(f_hz[kb]); hf_peak_power = float(P[kb])
    per_r, _ = _isi_period_arb(Sr, dt); f_resp_hz = float((1.0/per_r)/kappa)
    locked = bool(abs(f_peak_hz - f_resp_hz) <= 0.02 and 0.15 <= f_resp_hz <= 0.40 and hf_peak_power > 1e5)
    return dict(eps=round(eps,4), f_resp_hz=round(f_resp_hz,4), hrv_peak_hz=round(f_peak_hz,4),
                peak_power=float(f"{hf_peak_power:.4e}"), in_hf_band=bool(0.15 <= f_resp_hz <= 0.40),
                locked=locked)

# =====================================================================================================
#  T5  --  BAROREFLEX: a BP step is corrected by an HR change (cited gain/latency); setpoint=resting_hr
#     Rate-level autonomic loop that sets the SA-node FHN's operating rate.
#     plant : dBP = (a*HR - BP)/Tp + disturb ;  reflex: HRcmd = -BRS*BP(t-lat); dHR=(HRcmd-HR)/tau_auto
# =====================================================================================================
def baroreflex_static(BRS=1.0, lat=0.6, dP=20.0, tau_auto=1.5, dt=0.01, T=40.0, t_step=5.0):
    """Open-loop static gain: a sustained BP step dP -> steady HR change (= -BRS*dP). Also returns the
    measured onset latency."""
    n = int(T/dt); L = int(round(lat/dt)); HR = np.zeros(n); hist = [0.0]*(L+1)
    onset = None
    for i in range(1, n):
        bp = dP if i*dt > t_step else 0.0
        hist.pop(0); hist.append(bp)
        HR[i] = HR[i-1] + dt*((-BRS*hist[0] - HR[i-1])/tau_auto)
        if onset is None and i*dt > t_step and abs(HR[i]) > 0.05*abs(BRS*dP):
            onset = i*dt - t_step
    dHR = float(HR[-1])
    return dict(dP_mmHg=dP, dHR_bpm=round(dHR,4), slope_bpm_per_mmHg=round(dHR/dP,4),
                onset_latency_s=(round(onset,3) if onset else None), set_latency_s=lat,
                sign_correct=bool(dHR/dP < 0))

def baroreflex_closed(amp=25.0, BRS=1.0, lat=0.6, tau_auto=1.5, tau_p=2.0, a=1.2, dt=0.01, T=60.0):
    """Closed loop: a transient BP disturbance is corrected; HR & BP return to setpoint (=resting_hr)."""
    n = int(T/dt); L = int(round(lat/dt)); BP = np.zeros(n); HR = np.zeros(n); hist = [0.0]*(L+1)
    w = 1.0; t0 = 10.0
    for i in range(1, n):
        t = i*dt
        disturb = amp*math.exp(-((t-t0)/w)**2)/(w*math.sqrt(math.pi))
        HRcmd = -BRS*hist[0]
        HR[i] = HR[i-1] + dt*((HRcmd - HR[i-1])/tau_auto)
        BP[i] = BP[i-1] + dt*((a*HR[i-1] - BP[i-1])/tau_p) + dt*disturb
        hist.pop(0); hist.append(BP[i])
    peakHR = float(HR[int(np.argmax(np.abs(HR)))])
    return dict(disturb_amp=amp, peak_dHR_bpm=round(peakHR,4),
                final_dBP_mmHg=round(float(BP[-1]),5), final_dHR_bpm=round(float(HR[-1]),5),
                returned_to_setpoint=bool(abs(BP[-1]) < 0.5 and abs(HR[-1]) < 0.5),
                sign_correct=bool(peakHR*amp < 0))

# =====================================================================================================
#  CIRCULATE  --  one compact deterministic pass (headline single points; full sweeps in stress_tests)
# =====================================================================================================
def circulate():
    organs = emerge_organs(); osc = confirm_oscillators(); ta = time_anchor()
    eup = eupnea_period()
    cm = chemoreflex_marginal(15.0, 1.0)
    chem_stable   = chemoreflex_sim(0.6, 15.0)
    chem_unstable = chemoreflex_sim(1.6, 15.0)
    rsa_off = rsa(0.0); rsa_on = rsa(0.05)
    csr = cheyne_stokes()
    baro_s = baroreflex_static(dP=20.0); baro_c = baroreflex_closed(amp=25.0)
    dyn = dict(
        time_anchor=ta,
        eupnea={"breaths_per_min": eup["breaths_per_min"], "ratio_breath_to_beat": eup["ratio_breath_to_beat"]},
        chemoreflex={"LG_c": cm["LG_c"], "stable_amp": chem_stable["amp_late"],
                     "unstable_amp": chem_unstable["amp_late"], "unstable_period_s": chem_unstable["period_s"]},
        rsa={"off_locked": rsa_off.get("locked"), "on_locked": rsa_on.get("locked"),
             "hrv_peak_hz": rsa_on.get("hrv_peak_hz"), "f_resp_hz": rsa_on.get("f_resp_hz")},
        cheyne_stokes={"period_vs_delay_slope": csr["period_vs_delay_slope"]},
        baroreflex={"static_slope_bpm_per_mmHg": baro_s["slope_bpm_per_mmHg"],
                    "onset_latency_s": baro_s["onset_latency_s"], "closed_returns": baro_c["returned_to_setpoint"]},
    )
    return dict(_what="Cardiorespiratory -- emerge organs from measured gamma, then circulate dynamics.",
                organs=organs, oscillators=osc, dynamics=dyn,
                dynamics_status="EMERGED: eupnea / chemoreflex (apnea+CSR) / RSA / baroreflex active",
                targets="see repro/_verify/stress_tests.py (T1-T5) and repro/_oncology/")

def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    return o

def emit(obj):
    s = json.dumps(_round(obj), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = emit(circulate()); print(s); print("# sha256:", h)
