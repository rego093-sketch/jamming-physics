#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
respiratory_disease.py  --  Cardiorespiratory DISEASE-EXTENSION research module.

Every disorder below is cast as a PERTURBATION of an object this package already built and verified
(T1-T5 + the oncology Kramers kernel). NO new substrate primitive is introduced: each disease reuses
the R19 bistable switch (`barrier`, `spinodal`, `barrier_eff`) or the FitzHugh-Nagumo relaxation
oscillator / delayed control loop. The molecular driver (allergen, virus, opioid, hypoxia) enters ONLY
as an applied bias h or a parameter shift; the biochemistry is exogenous (FUTURE_WORK Sec.6).

SCOPE (FUTURE_WORK Sec.2/Sec.7 priority order):
  D1 Mayer waves       -- baroreflex self-oscillation ~0.1 Hz (reuse T5 + Nyquist marginal solver)
  D2 Asthma            -- airway smooth-muscle R19 switch, REVERSIBLE bias (reuse oncology barrier_eff)
  D3 OSA               -- loop-gain endotype (reuse T2) + pharyngeal Pcrit = spinodal collapse
  D4 CSA spectrum      -- altitude / CHF / opioid as three axes of (gain, delay, drive) (reuse T2/T4)
  D5 Fever             -- HR-RR co-scaling via the SHARED substrate gamma(T) (SantaLucia dG(T))
  D6 Cough             -- single FHN excitation above an irritant threshold (excitable, sub-Hopf)

GRADES (VP-SPEC C3): [F] forced / [V] reproduced+checked / [V?] coherent hypothesis, mechanism reuse,
needs an independent dataset / [L] anchored to a cited clinical value / [O] open, obstacle stated.
HONESTY: every absolute magnitude (Pcrit, PC20, capsaicin C5, absolute febrile rate) is [O] for the
SAME structural reason as absolute organ size and absolute cancer RR -- the switch noise scale and the
stimulus->bias conversion are not fixed by substrate geometry. SHAPES and DIRECTIONS are the content.
DETERMINISM (C1): BLAS pinned single-thread; fixed seed; round-before-hash. stdlib + numpy only.
"""
import os, sys, json, math, hashlib
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for sub in (("..","_engine"), ("..","_oncology"), ("..","..","inherited")):
    sys.path.insert(0, os.path.join(_HERE, *sub))
import importlib
eng  = importlib.import_module("vp_car_engine")
onco = importlib.import_module("carcinogen_dose_response")
from vp_substrate import Neuron, spinodal, barrier, settle, sdot, seed_everything

# ======================================================================================================
#  CITED CLINICAL ANCHORS  (grade [L]; NOT tuned to make a target pass)
# ======================================================================================================
MAYER_BAND_HZ   = (0.04, 0.15)   # LF / Mayer-wave band (Task Force 1996); Mayer wave classically ~0.1 Hz
CSR_HF_PERIOD_S = (45.0, 90.0)   # Cheyne-Stokes cycle length in heart failure (clinical CSR)
FEBRILE_BPM_PER_C = 10.0         # heart rate rises ~8-10 bpm per degC of fever (Liebermeister's rule)
LG_ENDOTYPE_HI  = 1.0            # clinical "high loop gain" endotype: LG at/above its critical value

# ======================================================================================================
#  D1  --  MAYER WAVES  (~0.1 Hz baroreflex self-oscillation)
#  Same forced mechanism as Cheyne-Stokes (T4): a delayed negative-feedback loop self-oscillates when
#  its loop gain exceeds 1, at a period ~= 2x the loop delay. The baroreflex IS such a loop. Its
#  SYMPATHETIC arm (vascular tone) is slow, so the effective loop delay is seconds, not 0.6 s, and the
#  marginal frequency lands in the cited Mayer/LF band. We do NOT tune the delay to hit 0.1 Hz; we read
#  the marginal frequency off the engine's Nyquist solver for a range of cited delays and report overlap.
# ======================================================================================================
def mayer_waves(delay_list=None, Tp=1.0):
    """Baroreflex marginal self-oscillation frequency vs effective loop delay (sympathetic arm).
    Reuses eng.chemoreflex_marginal -- a GENERIC delayed-negative-feedback marginal-gain/period solver."""
    if delay_list is None:
        # effective baroreflex (sympathetic) loop delay, seconds -- cited range, slow vascular arm
        delay_list = [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    rows = []
    for td in delay_list:
        m = eng.chemoreflex_marginal(td, Tp)
        f = 1.0 / m["period_onset_s"]
        rows.append(dict(loop_delay_s=td, period_onset_s=m["period_onset_s"],
                         freq_hz=round(f, 4), period_over_delay=m["period_over_delay"],
                         in_mayer_band=bool(MAYER_BAND_HZ[0] <= f <= MAYER_BAND_HZ[1])))
    in_band = [r for r in rows if r["in_mayer_band"]]
    # the period/delay ratio is the forced ~2x relation (identical to CSR T4)
    ratio = np.mean([r["period_over_delay"] for r in rows])
    return dict(rows=rows, period_over_delay_mean=round(float(ratio), 4),
                any_in_mayer_band=bool(in_band), band_hz=list(MAYER_BAND_HZ),
                forced_relation="baroreflex loop self-oscillates at period ~2x loop delay when LG>1 (same as T4)",
                grade_mechanism="[V]", grade_abs_freq="[L]")

# ======================================================================================================
#  D2  --  ASTHMA  (airway smooth-muscle bistable switch; REVERSIBLE bias)
#  Airway smooth muscle = R19 switch: open (relaxed) basin vs constricted basin. A bronchoconstrictor
#  (methacholine/histamine/allergen) is a SUSTAINED bias h>0 that lowers the barrier toward the
#  constricted basin -- the SAME role the carcinogen bias plays in oncology, but REVERSIBLE: a
#  bronchodilator is the opposite (negative) bias. An acute attack is a SPINODAL crossing. We reuse the
#  exact `barrier_eff` (cubic s^3 - g s - h = 0) and demonstrate threshold + hysteresis + reversibility.
# ======================================================================================================
_G_AIRWAY = 1.5   # airway-tone switch stiffness (representative; absolute value is calibration [O])

def _settle_sign(g, h, s0):
    """Settle the R19 field from s0 under bias h; return final position (basin)."""
    return settle(g, h, s0=s0, n=4000, dt=0.01)

def asthma_challenge(g=_G_AIRWAY, h_grid=None):
    """Constriction-vs-dose: as bronchoconstrictor bias h rises, the barrier toward 'constricted' falls
    (convex/threshold), and at the spinodal the open basin VANISHES (PC20-like all-or-none collapse).
    Returns the dose-response and the spinodal threshold. Reuses onco.barrier_eff."""
    sp = spinodal(g)
    if h_grid is None:
        h_grid = [round(x, 4) for x in np.linspace(0.0, 1.15 * sp, 14)]
    B0 = barrier(g)
    rows = []
    for h in h_grid:
        be = onco.barrier_eff(g, h)                       # barrier the OPEN basin must climb to constrict
        # Kramers occupancy of the constricted basin (finite switch noise = barrier/3, declared) -> resistance proxy
        scale = max(B0 / 3.0, 1e-9)
        constrict_rate = math.exp(-be / scale) if be > 0 else 1.0
        rows.append(dict(bias_h=h, frac_of_spinodal=round(h / sp, 4),
                         barrier_to_constrict=round(be, 6),
                         constriction_index=round(min(constrict_rate, 1.0), 6),
                         open_basin_exists=bool(h < sp)))
    # PC20-analog: first dose where constriction_index crosses 0.20 (a 20%-fall surrogate)
    pc20 = next((r["bias_h"] for r in rows if r["constriction_index"] >= 0.20), None)
    return dict(rows=rows, spinodal_bias=round(sp, 6), pc20_bias=pc20,
                shape="convex/threshold, saturating near spinodal (same family as oncology RR(dose))",
                grade_shape="[V]", grade_pc20_abs="[O]",
                obstacle="absolute PC20 needs the switch noise scale + molecular dose->bias map (external)")

def asthma_hysteresis(g=_G_AIRWAY, h_max=None, n=60):
    """Sweep bias UP (increasing constrictor) then DOWN (adding bronchodilator). The switch stays in its
    basin until the spinodal, so the up-limb and down-limb DIFFER -> a hysteresis loop. Deep-inspiration
    bronchodilation = a mechanical re-crossing of the spinodal. Bistable hysteresis -> [V?]."""
    sp = spinodal(g)
    if h_max is None:
        h_max = 1.3 * sp
    ups = np.linspace(-h_max, h_max, n)
    downs = ups[::-1]
    s = settle(g, -h_max, s0=-math.sqrt(g), n=4000, dt=0.01)  # start open (negative basin)
    up_state = []
    for h in ups:
        s = _settle_sign(g, h, s); up_state.append(s)
    dn_state = []
    for h in downs:
        s = _settle_sign(g, h, s); dn_state.append(s)
    up_state = np.array(up_state); dn_state = np.array(dn_state[::-1])  # realign to ascending h
    # hysteresis width = bias gap between the up-switch and down-switch crossings of s=0
    def crossing(hs, st):
        sgn = st > 0
        idx = np.where(sgn[:-1] != sgn[1:])[0]
        return float(hs[idx[0]]) if len(idx) else None
    h_close = crossing(ups, up_state)        # open->constricted (rising constrictor)
    h_open  = crossing(ups, dn_state)         # constricted->open (rising dilator, i.e. falling constrictor)
    width = (h_close - h_open) if (h_close is not None and h_open is not None) else None
    return dict(spinodal_bias=round(sp, 6),
                close_bias=(round(h_close, 5) if h_close is not None else None),
                reopen_bias=(round(h_open, 5) if h_open is not None else None),
                hysteresis_width=(round(width, 5) if width is not None else None),
                reversible=bool(width is not None and width > 0),
                grade="[V?]", note="bistable hysteresis = clinically observed airway hysteresis")

# ======================================================================================================
#  D3  --  OBSTRUCTIVE SLEEP APNEA  (loop-gain endotype + pharyngeal Pcrit switch)
#  (a) the normalized loop gain LG/LGc from T2 IS the clinical "loop gain" endotype.
#  (b) the pharynx is a second R19 switch: patent vs collapsed; below a critical dilator drive the
#      patent basin disappears at a SPINODAL = the critical closing pressure Pcrit. Hysteretic reopening.
# ======================================================================================================
_G_PHARYNX = 1.5

def osa_loop_gain_endotype(tau_d=15.0):
    """High loop gain -> ventilatory instability (reuses T2 chemoreflex bifurcation). Maps LG/LGc onto
    the clinical loop-gain endotype: stable below 1, periodic/apneic above 1."""
    LGc = eng.chemoreflex_marginal(tau_d, 1.0)["LG_c"]
    rows = []
    for lg in (0.5, 0.8, 1.0, 1.2, 1.5):
        r = eng.chemoreflex_sim(lg, tau_d)
        rows.append(dict(loop_gain_ratio=lg, unstable=bool(r["sustained"]),
                         apnea_fraction=r["apnea_fraction"], period_s=r["period_s"]))
    return dict(LG_critical=LGc, rows=rows,
                endotype_rule="ventilatory instability appears as LG crosses 1 (clinical 'high loop gain')",
                grade="[V]", note="LG/LGc is exactly the quantity the OSA-physiology literature calls loop gain")

def osa_pharyngeal_collapse(g=_G_PHARYNX):
    """Pharyngeal patency switch: sweep dilator drive (negative bias = collapsing pressure) and show a
    DISCONTINUOUS collapse at the spinodal (Pcrit), with hysteretic reopening. Pcrit absolute [O]."""
    hy = asthma_hysteresis(g=g)   # identical R19 machinery, reinterpreted as patency
    return dict(pcrit_spinodal=hy["spinodal_bias"], collapse_bias=hy["close_bias"],
                reopen_bias=hy["reopen_bias"], hysteresis_width=hy["hysteresis_width"],
                discontinuous_collapse=bool(hy["close_bias"] is not None),
                grade_collapse="[V?]", grade_pcrit_abs="[O]",
                note="Pcrit = spinodal of the pharyngeal-patency switch; reopening pressure < closing (hysteresis)")

# ======================================================================================================
#  D4  --  CENTRAL SLEEP APNEA / PERIODIC-BREATHING SPECTRUM
#  Altitude (controller gain up), heart failure (circulatory delay up = T4), opioid (drive down) are
#  THREE AXES of the SAME apnea machinery. The model already predicts each direction.
# ======================================================================================================
def csa_altitude(tau_d=15.0):
    """Hypoxic ventilatory response raises controller gain -> LG crosses 1 -> periodic breathing onset."""
    rows = []
    for gain in (0.6, 0.9, 1.0, 1.2, 1.5):   # controller gain as fraction of critical (altitude raises it)
        r = eng.chemoreflex_sim(gain, tau_d)
        rows.append(dict(controller_gain_ratio=gain, periodic=bool(r["sustained"]), period_s=r["period_s"]))
    onset = next((r["controller_gain_ratio"] for r in rows if r["periodic"]), None)
    return dict(rows=rows, onset_gain_ratio=onset, axis="controller gain (hypoxic drive)",
                direction="altitude -> higher gain -> periodic breathing", grade="[V]")

def csa_heart_failure(delay_list=None):
    """Long circulatory delay (low cardiac output) -> long Cheyne-Stokes cycle (reuses T4 ~2x delay).
    For CHF round-trip delays of ~25-45 s, predict CSR cycles in the cited 45-90 s clinical band."""
    if delay_list is None:
        delay_list = [10.0, 20.0, 25.0, 30.0, 40.0, 45.0]   # lung->chemoreceptor delay, seconds
    cs = eng.cheyne_stokes(tau_list=delay_list, LG_ratio=1.6)
    rows = []
    for r in cs["rows"]:
        per = r["period_s"]
        rows.append(dict(circ_delay_s=r["circ_delay_s"], csr_period_s=per,
                         period_over_delay=r["period_over_delay"],
                         in_clinical_csr_band=bool(per is not None and CSR_HF_PERIOD_S[0] <= per <= CSR_HF_PERIOD_S[1])))
    band_hits = [r for r in rows if r["in_clinical_csr_band"]]
    return dict(rows=rows, slope=cs["period_vs_delay_slope"], any_in_csr_band=bool(band_hits),
                csr_band_s=list(CSR_HF_PERIOD_S), axis="circulatory delay (cardiac output)",
                direction="lower CO -> longer delay -> longer CSR cycle", grade="[V]", grade_abs="[L]")

def csa_opioid(tau_d=15.0):
    """Opioids depress respiratory drive. Starting at the eupneic operating point and progressively
    lowering the tonic drive, the CPG keeps oscillating across a wide window, then QUENCHES once the
    drive falls below the lower Hopf bifurcation (~-0.77 here) -> central apnea (no rhythm). The wide
    oscillatory window is itself a finding: the rhythm is robust and only a DEEP drive cut silences it,
    matching the clinical fact that opioid central apnea requires substantial respiratory depression."""
    rows = []
    for drive in (0.55, 0.30, 0.0, -0.50, -0.77, -0.85, -1.00):  # progressive opioid depression
        fa, nb, _ = eng._fhn_rate_arb(95.0, drive=drive)
        rows.append(dict(drive=drive, breathing=bool(nb >= 3 and fa > 0.0), beats=int(nb)))
    # quench point = first drive (descending) at which the oscillation stops
    quench = next((r["drive"] for r in rows if not r["breathing"]), None)
    robust = bool(rows[1]["breathing"] and rows[2]["breathing"])   # still breathing at moderate cuts
    return dict(rows=rows, apnea_below_drive=quench, robust_to_moderate_cut=robust,
                axis="respiratory drive (opioid)",
                direction="opioid lowers drive; rhythm quenches only past the lower Hopf -> central apnea",
                grade="[V]", note="quench threshold = lower Hopf of the preBotC FHN (forced feature)")

# ======================================================================================================
#  D5  --  FEVER  (substrate-distinctive: HR-RR co-scaling via the SHARED gamma(T))
#  In this program gamma = -mean NN stacking dG (SantaLucia). dG(T)=dH - T*dS, so gamma is
#  TEMPERATURE-DEPENDENT. Fever (T up) makes stacking less stable -> gamma DOWN -> barrier B=gamma^2/4
#  DOWN. Because BOTH the heart and lung FHN oscillators sit on this SAME substrate gamma, a fever shifts
#  BOTH oscillators' stiffness together -> tachycardia and tachypnea must CO-SCALE (not drift
#  independently). That shared-substrate co-scaling is the forced/falsifiable content; the absolute
#  ~10 bpm/degC is the calibration anchor.
# ======================================================================================================
# Representative Watson-Crick NN stacking thermodynamics (SantaLucia 1998 unified set, averaged):
_NN_dH = -8.0     # kcal/mol  (enthalpy, stabilizing)
_NN_dS = -0.0220  # kcal/mol/K (entropy, dS<0)
_T37   = 310.15   # K

def _gamma_of_T(T_K, gamma_ref):
    """Scale a reference gamma by the SantaLucia dG(T) temperature dependence.
    gamma ~ -dG = -dH + T*dS  ; gamma(T)/gamma(37) = (-dH + T*dS)/(-dH + T37*dS)."""
    g37 = (-_NN_dH + _T37 * _NN_dS)
    gT  = (-_NN_dH + T_K * _NN_dS)
    return gamma_ref * (gT / g37)

def _fhn_rate_for_gamma(gamma, tau_s, drive=0.55, T=6000.0, dt=0.05):
    """FHN intrinsic ISI rate (arb) as a function of the cubic stiffness gamma (the substrate lever)."""
    n = Neuron(gamma=float(gamma), tau_f=1.0, tau_s=float(tau_s), beta=0.5)
    S, _ = n.run(drive=drive, T=T, dt=dt)
    sp = Neuron.spikes(S)
    if len(sp) < 6:
        return 0.0
    iv = np.diff(sp[4:]) * dt
    per = float(np.median(iv))
    return (1.0 / per) if per > 0 else 0.0

def fever_coscaling(gamma_sub=1.51, fevers_C=None):
    """Apply gamma(T) to the SHARED substrate stiffness feeding BOTH oscillators; report whether HR and
    RR move in the SAME direction and the forced co-scaling ratio. Direction is the [V?] content."""
    seed_everything()
    if fevers_C is None:
        fevers_C = [37.0, 38.0, 39.0, 40.0, 41.0]
    ta = eng.time_anchor(); kappa = ta["kappa_s_per_arb"]
    # baseline rates at 37C set the kappa-consistent reference
    rows = []
    base_heart = base_lung = None
    for Tc in fevers_C:
        T_K = 273.15 + Tc
        g = _gamma_of_T(T_K, gamma_sub)
        f_heart_arb = _fhn_rate_for_gamma(g, 18.0)
        f_lung_arb  = _fhn_rate_for_gamma(g, 95.0)
        hr_bpm = (f_heart_arb / kappa) * 60.0
        rr_bpm = (f_lung_arb  / kappa) * 60.0
        if base_heart is None:
            base_heart, base_lung = hr_bpm, rr_bpm
        rows.append(dict(fever_C=Tc, gamma=round(g, 5),
                         HR_bpm=round(hr_bpm, 3), RR_bpm=round(rr_bpm, 3),
                         dHR_from_37=round(hr_bpm - base_heart, 3),
                         dRR_from_37=round(rr_bpm - base_lung, 3)))
    # co-scaling: signs of dHR and dRR agree across fever?
    dHR = [r["dHR_from_37"] for r in rows[1:]]
    dRR = [r["dRR_from_37"] for r in rows[1:]]
    same_sign = all((a >= 0) == (b >= 0) for a, b in zip(dHR, dRR)) and any(abs(a) > 1e-6 for a in dHR)
    # slope per degC (heart) and the HR:RR co-scaling ratio
    Tc_arr = np.array([r["fever_C"] for r in rows])
    hr_arr = np.array([r["HR_bpm"] for r in rows]); rr_arr = np.array([r["RR_bpm"] for r in rows])
    hr_slope = float(np.polyfit(Tc_arr, hr_arr, 1)[0])
    rr_slope = float(np.polyfit(Tc_arr, rr_arr, 1)[0])
    ratio = (hr_slope / rr_slope) if abs(rr_slope) > 1e-9 else None
    return dict(rows=rows, hr_bpm_per_C=round(hr_slope, 4), rr_bpm_per_C=round(rr_slope, 4),
                hr_rr_coscaling_ratio=(round(ratio, 4) if ratio else None),
                co_scale_same_direction=bool(same_sign),
                cited_hr_rule_bpm_per_C=FEBRILE_BPM_PER_C,
                forced_content="HR and RR share one substrate gamma(T) -> they co-scale under fever",
                grade_direction="[V?]", grade_abs="[O]", grade_rule="[L]",
                note="sign/coupling is the falsifiable claim; absolute degC->gamma slope needs calibration")

# ======================================================================================================
#  D6  --  COUGH  (single FHN excitation above an irritant threshold; excitable / sub-Hopf regime)
#  Cough is NOT the oscillatory regime: it is a stereotyped all-or-none expiratory pulse triggered when
#  an irritant (capsaicin) crosses a threshold = a SINGLE excitation of an FHN unit held just below the
#  Hopf. Chronic cough = a sensitized (lowered) threshold. Absolute capsaicin C5 [O].
# ======================================================================================================
def cough_threshold(tau_s=40.0, base_drive=-1.0, dt=0.02, T=300.0):
    """Hold the FHN in its QUIESCENT regime (base drive below the lower Hopf -> a single stable fixed
    point, no spontaneous rhythm), apply a BRIEF irritant kick of rising amplitude, and find the
    threshold above which a FULL spike (cough) fires. Below threshold the perturbation decays; above it
    fires one all-or-none excursion and returns to rest -- the excitable (sub-Hopf) signature."""
    seed_everything()
    rows = []; thr = None
    for amp in [round(a, 3) for a in np.linspace(0.0, 2.2, 23)]:
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=tau_s, beta=0.5)
        N = int(T / dt)
        drive = np.full(N, base_drive)
        t0 = int(40.0 / dt); dur = int(1.0 / dt)        # brief irritant pulse
        drive[t0:t0 + dur] += amp
        S, _ = n.run(drive=drive, T=T, dt=dt, s0=-0.68, w0=-1.36)   # start at the quiescent fixed point
        peak = float(np.max(S[t0:]))
        fired = bool(peak > 0.5)                          # full excursion crosses well past the FP
        rows.append(dict(stimulus_amp=amp, peak=round(peak, 3), cough=fired))
        if fired and thr is None:
            thr = amp
    below = [r["peak"] for r in rows if not r["cough"]]
    above = [r["peak"] for r in rows if r["cough"]]
    all_or_none = bool(below and above and (min(above) > 2.0 * (max(below) + 1e-6)))
    return dict(rows=rows, threshold_amp=thr, all_or_none=all_or_none,
                resting_peak=(round(max(below), 3) if below else None),
                fired_peak=(round(min(above), 3) if above else None),
                regime="excitable (sub-Hopf): single excitation, not a limit cycle",
                grade="[V?]", grade_c5_abs="[O]",
                note="chronic cough = lowered threshold; absolute capsaicin C5 needs calibration")

# ======================================================================================================
#  AGGREGATE
# ======================================================================================================
def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    return o

def results():
    seed_everything()
    return dict(
        _what="Cardiorespiratory disease extension -- each disorder is a perturbation of a verified object.",
        D1_mayer_waves   = mayer_waves(),
        D2_asthma        = dict(challenge=asthma_challenge(), hysteresis=asthma_hysteresis()),
        D3_osa           = dict(loop_gain=osa_loop_gain_endotype(), pharynx=osa_pharyngeal_collapse()),
        D4_csa_spectrum  = dict(altitude=csa_altitude(), heart_failure=csa_heart_failure(), opioid=csa_opioid()),
        D5_fever         = fever_coscaling(),
        D6_cough         = cough_threshold(),
        no_new_primitive = True,
        substrate        = "R19 switch + FitzHugh-Nagumo relaxation oscillator (reused; none added)",
    )

def emit(obj):
    s = json.dumps(_round(obj), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = emit(results()); print(s); print("# sha256:", h)
