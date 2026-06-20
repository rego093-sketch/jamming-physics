#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_cir_engine.py  --  Circulatory Transport emergence engine (deterministic, in-package).

SCOPE (see CHARTER.md): Vasculature (Windkessel pressure-flow), kidney (glomerular filtration +
osmoregulation loop) and liver (hepatic clearance) emerge as a transport+clearance network driven
by the cardiac pump boundary condition.

WHAT RUNS (a fresh chat can execute `python repro/run_all.py`):
  emerge_organs()   -- load MEASURED master-gene gamma (vendored from DNA), build each Organ on the
                       R19 substrate, read the developmental ORDER off gamma.
  circulate()       -- emerge organs, then drive the three coupled dynamic regimes from the cardiac
                       pump boundary condition (CO, cited):
                         * vessels  : 2-element Windkessel  (transport)   -> MAP, SBP/DBP, tau=RC
                         * kidney   : Starling filtration + tubuloglomerular feedback (control-loop)
                                      + ADH osmostat                          -> GFR plateau, Osm setpoint
                         * liver    : well-stirred first-pass clearance (clearance) -> E, F

GRADES (VP-SPEC C3): the FORM of each law (Ohm pressure-flow, RC decay, Starling balance,
well-stirred saturation) is forced [F]; the SIMULATION reproducing the cited operating point is [V];
the absolute physiological inputs (CO, SVR, C, K_f, Q_H, ...) are cited literature anchors [L]; the
absolute organ scale/mass remains open [O] (DWELL fixes RELATIVE size only -- IRREPRODUCIBILITY_LEDGER).

This package adds DYNAMICS only. Organ IDENTITY + developmental ORDER are owned by the DNA
morphogenesis gene-clock and CITED here (measured gamma, never fitted). The substrate (R19 + FHN)
is vendored and NOT re-derived.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed; round-before-hash; sorted keys.
Two engine runs yield byte-identical sha256.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, dwell, dominant_freq, seed_everything

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

# ===========================================================================
#  Cited boundary conditions and vascular constants (literature anchors [L]).
#  Units kept explicit: pressure mmHg, flow mL/s (hemodynamics) or mL/min
#  (renal/hepatic), volume mL or L, time s (hemodynamics) or h (osmostat).
# ===========================================================================
CO_REST_ML_S   = 5000.0 / 60.0     # cardiac output 5 L/min  -> 83.333 mL/s  (cardioresp BC, cited)
HR_REST_BPM    = 75.0              # heart rate (sets beat period / stroke volume) [L]
SYS_FRACTION   = 0.35             # systolic ejection fraction of the cardiac cycle [L]
SVR_REST       = 1.10             # systemic vascular resistance, mmHg*s/mL  (~1467 dyn*s*cm^-5) [L]
C_ART_REST     = 1.40             # total arterial compliance, mL/mmHg  (cited 1-2) [L]
CVP_MMHG       = 4.0              # central venous (downstream) pressure, mmHg [L]

# renal (mL/min, mmHg, mmHg*min/mL)
K_F            = 12.5             # glomerular ultrafiltration coefficient, mL/min/mmHg [L]
PI_GC          = 28.0            # glomerular capillary oncotic pressure (mean), mmHg [L]
P_BS           = 16.0           # Bowman-space hydrostatic pressure, mmHg [L]
P_VEN_RENAL    = 8.0            # peritubular/venous pressure, mmHg [L]
RA_BASE        = 0.0418        # afferent arteriolar resistance baseline, mmHg*min/mL [L]
RE_BASE        = 0.0418        # efferent arteriolar resistance baseline, mmHg*min/mL [L]
GFR_SET        = 125.0        # GFR setpoint, mL/min [L]
AUTOREG_LO     = 80.0         # renal autoregulation lower bound, mmHg [L]
AUTOREG_HI     = 180.0        # renal autoregulation upper bound, mmHg [L]

# osmoregulation
OSM_SET        = 287.0        # plasma osmolality setpoint, mOsm/kg [L]
ADH_THR        = 280.0       # osmotic threshold for ADH release, mOsm/kg [L]
BODY_WATER_L   = 42.0       # total body water, L (70 kg adult) [L]

# hepatic (mL/min)
Q_H            = 1500.0      # hepatic blood flow, mL/min [L]
FU_PROP        = 0.11       # propranolol unbound fraction (89% protein bound) [L]
CLINT_PROP     = 40909.0   # propranolol intrinsic clearance, mL/min (-> E~0.75) [L]

ORGAN_ROWS = [{'master': 'SIX2',
  'organ': 'kidney',
  'role': 'metanephric nephron: filtration + tubular transport + osmoregulation',
  'dyn_class': 'control-loop',
  'tau_s': None,
  'rate_note': 'GFR ~125 mL/min [L]; tubuloglomerular feedback + ADH osmostat',
  'has_gamma': True},
 {'master': 'HHEX',
  'organ': 'liver',
  'role': 'hepatic blood flow + first-pass clearance/metabolism',
  'dyn_class': 'clearance',
  'tau_s': None,
  'rate_note': 'hepatic extraction ratio E; well-stirred F=1-E [L]',
  'has_gamma': True},
 {'master': '(vasculature)',
  'organ': 'vessels',
  'role': 'pressure-driven flow network (no single master gene; mesodermal/diffuse)',
  'dyn_class': 'transport',
  'tau_s': None,
  'rate_note': 'MAP = CO x SVR; Windkessel tau = R x C [L]',
  'has_gamma': False}]
OSCILLATOR_ORGANS = []   # the cardiac oscillator lives in cardioresp (cited BC), not here.

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

# ===========================================================================
#  EMERGENCE  (identity + order from measured gamma -- DNA-owned, cited [V])
# ===========================================================================
def emerge_organs():
    """Emerge organs from MEASURED gamma. Order = gamma readout (ascending functional spinodal)."""
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
                order_grade="[V] order is a pure gamma readout (SIX2 1.5556 > HHEX 1.525 => liver-before-kidney by functional spinodal)")

def confirm_oscillators():
    """No oscillator organ in this package (the heart is the cardioresp BC). Returns {} by design."""
    return {}

# ===========================================================================
#  VESSELS -- 2-element Windkessel (transport regime)
#     C dP/dt = Q_in(t) - (P - P_v)/R
#  steady-state mean:  MAP - P_v = CO*R   (Ohm pressure-flow, forced [F])  -> T1
#  diastole (Q_in=0):  P(t) = P_v + (P0-P_v) exp(-(t-t0)/RC)   tau = R*C [F]  -> T2
# ===========================================================================
def windkessel(co_ml_s=CO_REST_ML_S, R=SVR_REST, C=C_ART_REST, Pv=CVP_MMHG,
               hr_bpm=HR_REST_BPM, sys_frac=SYS_FRACTION, n_beats=40, steps_per_beat=2000):
    """Simulate the 2-element Windkessel to steady state; measure MAP, SBP, DBP, PP, and the
    diastolic decay time constant tau by exact log-linear fit of the no-inflow segment."""
    T  = 60.0 / hr_bpm                 # beat period (s)
    SV = co_ml_s * T                   # stroke volume per beat (mL)
    t_sys = sys_frac * T               # systolic ejection duration (s)
    dt = T / steps_per_beat
    P  = co_ml_s * R + Pv              # init near analytic mean for fast settle
    # inflow waveform: half-sine ejection over [0,t_sys], 0 over diastole; integral over beat = SV
    def q_in(t_in_beat):
        if t_in_beat < t_sys:
            return (math.pi / 2.0) * (SV / t_sys) * math.sin(math.pi * t_in_beat / t_sys)
        return 0.0
    last_P = None
    for b in range(n_beats):
        Pser = np.empty(steps_per_beat); tser = np.empty(steps_per_beat)
        for i in range(steps_per_beat):
            tb = i * dt
            q  = q_in(tb)
            dP = (q - (P - Pv) / R) / C
            P  = P + dt * dP
            Pser[i] = P; tser[i] = tb
        last_P = (tser, Pser, t_sys, dt)
    tser, Pser, t_sys, dt = last_P
    MAP = float(Pser.mean()); SBP = float(Pser.max()); DBP = float(Pser.min())
    # diastolic decay: window strictly after inflow stops (10% guard past t_sys), to beat end
    mask = tser > (t_sys + 0.10 * (tser[-1] - t_sys))
    td = tser[mask]; Pd = Pser[mask]
    y = np.log(np.maximum(Pd - Pv, 1e-9))
    A = np.vstack([td, np.ones_like(td)]).T
    slope, _ = np.linalg.lstsq(A, y, rcond=None)[0]
    tau_meas = float(-1.0 / slope) if slope < 0 else float("inf")
    return dict(MAP_mmHg=round(MAP, 4), SBP_mmHg=round(SBP, 4), DBP_mmHg=round(DBP, 4),
                PP_mmHg=round(SBP - DBP, 4), tau_meas_s=round(tau_meas, 6),
                tau_RC_s=round(R * C, 6), MAP_ohm_mmHg=round(co_ml_s * R + Pv, 4),
                CO_ml_s=round(co_ml_s, 4), R=round(R, 6), C=round(C, 6))

# ===========================================================================
#  KIDNEY -- Starling filtration + tubuloglomerular feedback (control-loop)
#     RBF = (P_a - P_v)/(R_a + R_e) ;  P_GC = P_v + RBF*R_e
#     GFR = K_f * (P_GC - PI - P_BS)        (Starling, forced [F])
#     TGF: dR_a/dt = +k*(GFR - GFR_set)     (afferent constriction when GFR high) -> plateau [V]
# ===========================================================================
def renal_steadystate(P_a, tgf=True, R_e=RE_BASE, ra_lo=0.5*RA_BASE, ra_hi=3.0*RA_BASE,
                      kp=2.0e-4, ki=4.0e-4, n=4000):
    """Settle the afferent arteriole under tubuloglomerular feedback at arterial pressure P_a.
    With tgf=False the afferent resistance is fixed at baseline (open loop, no autoregulation).
    Returns SINGLE-kidney (intact-nephron-mass) GFR; CKD staging scales this by remaining nephron
    fraction (DISEASE_EXTENSIONS T13), which lowers the plateau while leaving per-nephron
    autoregulation intact."""
    R_a = RA_BASE; I = 0.0
    def gfr_of(Ra):
        RBF = (P_a - P_VEN_RENAL) / (Ra + R_e)
        P_GC = P_VEN_RENAL + RBF * R_e
        return K_F * (P_GC - PI_GC - P_BS), RBF, P_GC
    if not tgf:
        gfr, RBF, P_GC = gfr_of(R_a)
        return dict(GFR=gfr, RBF=RBF, P_GC=P_GC, R_a=R_a)
    for _ in range(n):
        gfr, RBF, P_GC = gfr_of(R_a)
        err = gfr - GFR_SET
        I += err
        R_a = R_a + kp * err + ki * 1e-3 * I    # PI control; constrict when GFR>setpoint
        R_a = ra_lo if R_a < ra_lo else (ra_hi if R_a > ra_hi else R_a)
    gfr, RBF, P_GC = gfr_of(R_a)
    return dict(GFR=gfr, RBF=RBF, P_GC=P_GC, R_a=R_a)

# ===========================================================================
#  KIDNEY -- ADH osmostat (the osmoregulation control-loop)
#     Osm = solute/water ;  PI water-balance controller via ADH antidiuresis + thirst
#     restores Osm to OSM_SET after an osmotic load.   setpoint [L], correction [V]
# ===========================================================================
def osmostat(load_water_deficit_L=0.0, load_solute_mOsm=0.0, loop=True,
             kp=0.020, ki=0.010, dt_h=0.25, hours=72.0,
             max_flux_L_h=0.6, adh_gain=1.0, setpoint_shift_mOsm=0.0):
    """Apply an osmotic perturbation (water deficit and/or solute load) and run the ADH/thirst
    water-balance loop. Returns the osmolality trajectory and steady-state value.
    adh_gain scales antidiuretic/thirst authority (adh_gain=0 => no ADH response => diabetes
    insipidus, DISEASE_EXTENSIONS T11). setpoint_shift_mOsm shifts the DEFENDED osmolality
    (a sustained inappropriate antidiuretic bias => the loop defends a lower osmolality =>
    dilutional hyponatremia, the SIADH surrogate T12). Defaults (gain=1, shift=0) reproduce the
    healthy engine exactly."""
    set_eff = OSM_SET + setpoint_shift_mOsm
    S = OSM_SET * BODY_WATER_L + load_solute_mOsm      # total solute (mOsm)
    W = BODY_WATER_L - load_water_deficit_L            # total body water (L)
    I = 0.0; n = int(hours / dt_h)
    traj = np.empty(n + 1); traj[0] = S / W
    for i in range(n):
        Osm = S / W
        err = Osm - set_eff
        if loop:
            I += err * dt_h
            flux = adh_gain * (kp * err + ki * I)      # +err -> retain/ingest water -> W up -> Osm down
            flux = max(-max_flux_L_h, min(max_flux_L_h, flux))
        else:
            flux = 0.0
        W = W + flux * dt_h
        W = max(W, 1.0)
        traj[i + 1] = S / W
    return dict(osm_final=float(S / W), osm_peak=float(traj.max()), osm_set=OSM_SET,
                set_eff=float(set_eff), trajectory_first=float(traj[0]), trajectory=traj)

# ===========================================================================
#  LIVER -- well-stirred first-pass clearance (clearance regime)
#     E = fu*CLint/(Q_H + fu*CLint) ;  CL_H = Q_H*E ;  F = 1 - E    (forced [F])
# ===========================================================================
def hepatic_clearance(Qh=Q_H, fu=FU_PROP, clint=CLINT_PROP, F_abs=1.0):
    """Well-stirred hepatic extraction ratio E and oral bioavailability F = F_abs*(1-E)."""
    clu = fu * clint
    E = clu / (Qh + clu)
    CL_H = Qh * E
    F = F_abs * (1.0 - E)
    return dict(E=round(float(E), 6), F=round(float(F), 6), CL_H_ml_min=round(float(CL_H), 4),
                Qh=round(float(Qh), 4), clu=round(float(clu), 4))

# ===========================================================================
#  CIRCULATE -- one resting pass exercising every regime from the pump BC
# ===========================================================================
def circulate():
    organs = emerge_organs()
    osc    = confirm_oscillators()
    hemo   = windkessel()                                   # vessels (transport)
    renal  = renal_steadystate(P_a=100.0, tgf=True)          # kidney filtration at resting P_a
    osmo   = osmostat(load_water_deficit_L=0.0, loop=True)   # osmostat at rest (no load)
    hep    = hepatic_clearance()                             # liver clearance (propranolol)
    return dict(_what="Circulatory Transport -- emerge organs from measured gamma, then circulate "
                       "transport / control-loop / clearance dynamics from the cardiac pump BC.",
                organs=organs, oscillators=osc,
                hemodynamics=dict(MAP_mmHg=hemo["MAP_mmHg"], SBP_mmHg=hemo["SBP_mmHg"],
                                  DBP_mmHg=hemo["DBP_mmHg"], PP_mmHg=hemo["PP_mmHg"],
                                  tau_meas_s=hemo["tau_meas_s"], tau_RC_s=hemo["tau_RC_s"]),
                renal=dict(GFR_mL_min=round(renal["GFR"], 4), P_GC_mmHg=round(renal["P_GC"], 4),
                           RBF_mL_min=round(renal["RBF"], 4), GFR_set=GFR_SET),
                osmoregulation=dict(osm_rest=round(osmo["osm_final"], 4), osm_set=OSM_SET),
                hepatic=dict(E=hep["E"], F=hep["F"], CL_H_mL_min=hep["CL_H_ml_min"]),
                dynamics_status="EMERGED: vessels(Windkessel) + kidney(TGF+osmostat) + liver(well-stirred) "
                                "driven from the cardiac pump BC. Stress battery in repro/_verify; "
                                "carcinogen kernel in repro/_oncology.")

def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    if isinstance(o, np.ndarray): return [_round(float(v)) for v in o]
    return o

def emit(obj):
    s = json.dumps(_round(obj), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = emit(circulate()); print(s); print("# sha256:", h)
