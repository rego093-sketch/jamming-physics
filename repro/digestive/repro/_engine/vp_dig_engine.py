#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_dig_engine.py  --  Digestive / Metabolic emergence engine (deterministic, in-package).

SCOPE (see CHARTER.md): Gut (ICC slow-wave + peristalsis) and the endocrine pancreas/liver
(glucose-insulin-glucagon loop) emerge on the substrate; brain-facing (HPA/neuromodulator)
endocrine stays in mind -- this package owns BODY-metabolic endocrine only.

WHAT RUNS (a fresh chat can execute `python repro/run_all.py`):
  emerge_organs()       -- load MEASURED master-gene gamma (vendored from DNA), build each Organ on the
                           R19 substrate, read developmental ORDER off gamma.
  confirm_oscillators() -- for each OSCILLATOR organ instantiate the SHARED FHN Neuron, confirm a beat
                           (mechanism [V]; absolute rate [L], cited -- exactly as mind M18 does).
  slow_wave_clock()     -- ONE gastric-anchored time constant K_TIME converts model-Hz -> cpm; the
                           duodenal/jejunal/ileal rates are then PREDICTIONS (no intestinal tuning).
  intestinal_chain()    -- aboral tau_s gradient -> monotone falling cpm (the slow-wave gradient).
  peristalsis_transport()-- weak-coupled phase oscillators + occlusion -> net ABORAL flux; reverses
                           under a reversed gradient (control).
  glucose_homeostat()   -- full glucose/insulin/glucagon/hepatic-glycogen loop; secretion is a
                           population of R19 switches (graded). Returns the closed-loop integrator.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; round-before-hash; sorted keys; no RNG dependence
(all traces are noise-free integrations). circulate() emits a canonical digest of EVERY subsystem so the
2x-sha256 fingerprint covers the whole model, not just emergence.

GRADES (VP-SPEC C3):  [F] forced  /  [V] simulation-verified  /  [L] cited-locked anchor  /  [O] open.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib, functools
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, barrier, settle, dwell, dominant_freq, seed_everything

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

# ===========================================================================
#  ORGAN TABLE  -- identity/order are cited from DNA [V]; this package adds DYNAMICS.
#  tau_s (the FHN slow-recovery constant) is the only per-organ timescale; it is the
#  knob the gastric anchor fixes, NOT a free fit (one anchor sets the whole clock).
# ===========================================================================
ORGAN_ROWS = [
 {'master':'BARX1','organ':'stomach','role':'gastric ICC slow-wave + mixing',
  'dyn_class':'oscillator','tau_s':380.0,
  'rate_note':'gastric slow wave ~3 cpm = 0.05 Hz [L] ANCHOR','has_gamma':True},
 {'master':'CDX2','organ':'intestine','role':'intestinal ICC slow-wave + peristaltic propulsion',
  'dyn_class':'oscillator','tau_s':95.0,
  'rate_note':'duodenal slow wave ~12 cpm = 0.2 Hz [L] PREDICTED from clock','has_gamma':True},
 {'master':'PDX1','organ':'pancreas','role':'endocrine islet: insulin/glucagon glucose homeostat',
  'dyn_class':'control-loop','tau_s':None,
  'rate_note':'fasting glucose ~5 mM [L]','has_gamma':True},
 {'master':'HHEX','organ':'liver','role':'hepatic glucose storage/release (glycogen buffer)',
  'dyn_class':'control-loop','tau_s':None,
  'rate_note':'liver identity shared with circulatory (SSOT=DNA); METABOLIC role only','has_gamma':True},
]
OSCILLATOR_ORGANS = ["stomach", "intestine"]

# ===========================================================================
#  SLOW-WAVE CLOCK  -- ONE constant, fixed by the stomach alone.
# ===========================================================================
TAU_STOMACH = 380.0
TAU_DUO     = 95.0
GRAD_FACTOR = 1.5                 # aboral tau_s growth (duodenum -> ileum)
TAU_ILE     = TAU_DUO * GRAD_FACTOR   # = 142.5
GASTRIC_CPM = 3.0                 # [L] cited gastric slow-wave anchor (cycles/min)

@functools.lru_cache(maxsize=4096)
def fhn_freq(tau_s, drive=0.55, T=8000.0, dt=0.05):
    """Intrinsic relaxation frequency (model-Hz) of the SHARED FHN oscillator at recovery
    constant tau_s. Cached: the same tau_s recurs across the pipeline (keeps circulate fast)."""
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(tau_s), beta=0.5)
    S, _dt = n.run(drive=float(drive), T=T, dt=dt)
    return dominant_freq(S, _dt)

# K_TIME (cpm per model-Hz) is set ONCE by the gastric anchor; everything aboral is a prediction.
K_TIME = GASTRIC_CPM / fhn_freq(TAU_STOMACH)

def slow_wave_clock(drive=0.55):
    """The single clock and the rates it PREDICTS. Gastric is the [L] anchor; duodenum/jejunum/ileum
    are forward predictions with ZERO intestinal tuning. Mechanism [V]; absolute rate [L]."""
    g = K_TIME * fhn_freq(TAU_STOMACH, drive)
    d = K_TIME * fhn_freq(TAU_DUO, drive)
    j = K_TIME * fhn_freq((TAU_DUO + TAU_ILE) / 2.0, drive)
    i = K_TIME * fhn_freq(TAU_ILE, drive)
    return dict(K_time_cpm_per_modelHz=round(float(K_TIME), 6),
                gastric_cpm=round(float(g), 4), duodenum_cpm=round(float(d), 4),
                jejunum_cpm=round(float(j), 4), ileum_cpm=round(float(i), 4),
                cited_gastric=3.0, cited_duodenum=12.0, cited_jejunum=10.0, cited_ileum=8.0,
                mechanism_grade="[V]", rate_grade="[L]")

def intestinal_chain(N=12, drive=0.55):
    """Aboral chain of N segments with linearly growing tau_s -> monotone FALLING cpm. The gradient
    DIRECTION/shape is forced by the substrate [V]; absolute values inherit the [L] clock."""
    taus = np.linspace(TAU_DUO, TAU_ILE, N)
    return [round(float(K_TIME * fhn_freq(float(t), drive)), 4) for t in taus]

def peristalsis_transport(gradient_sign=+1, N=16, coupling=0.05, Tt=6000.0, dt=0.05,
                          Dtrans=0.20, wwin=0.5):
    """Weak nearest-neighbour (Kuramoto) coupling on the FHN-set intrinsic frequencies builds a
    travelling phase wave; an occlusion indicator + mass-conserving pressure flux moves luminal
    content. A physiological (proximal-fast) gradient yields net ABORAL displacement; a reversed
    gradient yields oral (control). Net directed transport from a phase gradient is forced [V]."""
    taus = np.linspace(TAU_DUO, TAU_ILE, N)
    if gradient_sign < 0:
        taus = taus[::-1]                                    # reversed gradient (control)
    omega = 2.0 * math.pi * np.array([fhn_freq(float(t)) for t in taus])
    theta = np.linspace(0.0, 0.4, N)                         # small initial phase spread
    c = np.zeros(N); c[1:4] = 1.0                            # proximal tracer bolus (conserved)
    pos = np.arange(N); com0 = (c * pos).sum() / c.sum()
    for _ in range(int(Tt / dt)):
        dth = omega.copy()
        dth[:-1] += coupling * np.sin(theta[1:] - theta[:-1])
        dth[1:]  += coupling * np.sin(theta[:-1] - theta[1:])
        theta = theta + dt * dth
        a = (np.cos(theta) > math.cos(wwin)).astype(float)   # contracting (occluding) segments
        fwd = Dtrans * np.maximum(a[:-1] - a[1:], 0.0) * c[:-1]   # i -> i+1 (aboral)
        bwd = Dtrans * np.maximum(a[1:] - a[:-1], 0.0) * c[1:]    # i -> i-1 (oral)
        c[:-1] -= fwd; c[1:] += fwd
        c[1:]  -= bwd; c[:-1] += bwd
    com1 = (c * pos).sum() / c.sum()
    return float(com1 - com0)

# ===========================================================================
#  GLUCOSE HOMEOSTAT  -- full glucose / insulin / glucagon / hepatic-glycogen loop.
#  Secretion is a POPULATION of R19 switches (graded sigmoid via a settle() lookup table).
# ===========================================================================
G_SET  = 5.0                                                 # [L] fasting setpoint (mM)
_GGRID = np.linspace(0.0, 16.0, 161)

def _secretion_fraction(G, low, k=0.9, spread=2.0, M=15, greg=1.0):
    """Fraction of a population of M R19 switches that are ON at glucose G. low=True -> glucagon
    cells (ON when glucose is LOW); low=False -> beta cells (ON when glucose is HIGH)."""
    thr = np.linspace(G_SET - spread, G_SET + spread, M); on = 0
    for t in thr:
        h = k * ((t - G) if low else (G - t))
        if settle(greg, h, n=400) > 0:
            on += 1
    return on / M

@functools.lru_cache(maxsize=1)
def _secretion_tables():
    """Precompute beta/alpha activation curves over the glucose grid ONCE (settle() is too slow to
    call inside the integrator loop). Cached for the whole pipeline; deterministic."""
    beta  = np.array([_secretion_fraction(G, False) for G in _GGRID])
    alpha = np.array([_secretion_fraction(G, True)  for G in _GGRID])
    return beta, alpha

def beta_on(G):
    beta, _ = _secretion_tables();  return float(np.interp(G, _GGRID, beta))
def alpha_on(G):
    _, alpha = _secretion_tables(); return float(np.interp(G, _GGRID, alpha))

# constants solved so the fasting fixed point lands at G*=G_SET (no residual offset):
#   at G=5, beta=alpha=0.40 -> Ins*=Glc*=0.40 ; dG/dt=0 with k_draw balancing store at setpoint.
HOMEOSTAT_P = dict(Smax_i=1.0, tau_i=0.20, Smax_g=1.0, tau_g=0.20, k_u0=0.05, k_u=0.40,
                   P_basal=1.05, k_glu=0.50, k_supp=0.50,
                   k_sto=0.08, k_draw=0.40, Glyc_max=4.0, Glyc_ref=2.0)

def glucose_homeostat(G0=5.0, meal=None, ins_kick=None, T=30.0, dt=0.02, Pp=None, track=False):
    """Integrate the closed loop. meal(t) adds exogenous glucose; ins_kick(t) injects exogenous
    insulin (hypoglycaemia challenge). Hepatic glycogen is a FINITE buffer (HHEX role): insulin+
    glucose store it, glucagon draws it; HGP rises when glucose is low and is suppressed by insulin.
    Homeostasis (return to a stable setpoint) is forced by the loop [V]; the setpoint value is [L]."""
    Pp = Pp or HOMEOSTAT_P
    n = int(T / dt); tt = np.arange(n) * dt
    G = G0; Ins = 0.40; Glc = 0.40; Glyc = Pp["Glyc_ref"]
    Gtr = np.empty(n); Itr = np.empty(n); Ctr = np.empty(n); Ytr = np.empty(n)
    for i in range(n):
        b = beta_on(G); a = alpha_on(G)
        Rmeal = meal(tt[i]) if meal else 0.0
        if ins_kick is not None:
            Ins += ins_kick(tt[i]) * dt
        Ins += dt * (b * Pp["Smax_i"] - Ins) / Pp["tau_i"]
        Glc += dt * (a * Pp["Smax_g"] - Glc) / Pp["tau_g"]
        store = Pp["k_sto"] * Ins * G; draw = Pp["k_draw"] * Glc
        Glyc += dt * (store - draw); Glyc = min(max(Glyc, 0.0), Pp["Glyc_max"])
        avail = Glyc / Pp["Glyc_ref"]
        HGP = Pp["P_basal"] + Pp["k_glu"] * Glc * avail - Pp["k_supp"] * Ins
        dG = Rmeal + HGP - (Pp["k_u0"] + Pp["k_u"] * Ins) * G
        G += dt * dG; G = max(G, 0.05)
        Gtr[i] = G; Itr[i] = Ins; Ctr[i] = Glc; Ytr[i] = Glyc
    return (tt, Gtr, Itr, Ctr, Ytr) if track else (tt, Gtr)

def _pulse(amp, t0=4.0, dur=2.0):
    return lambda x: amp if (t0 <= x < t0 + dur) else 0.0

# ===========================================================================
#  EMERGENCE  (unchanged: identity/order off measured gamma)
# ===========================================================================
def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def emerge_organs():
    """Emerge organs from MEASURED gamma. Order = gamma readout (SIGN validated vs cited timing)."""
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
                order_grade="[V] order is a pure gamma readout; SIGN validated vs cited timing anchor")

def confirm_oscillators():
    """For each OSCILLATOR organ, instantiate the SHARED FHN Neuron and confirm a beat. Mechanism [V]; rate [L]."""
    seed_everything(); out = {}
    for r in ORGAN_ROWS:
        if r["dyn_class"] != "oscillator": continue
        taus = r["tau_s"] if r["tau_s"] is not None else 40.0
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(taus), beta=0.5, name=r["organ"])
        S, dt = n.run(drive=0.55, T=4000.0, dt=0.05)
        f = dominant_freq(S, dt); nb = len(Neuron.spikes(S))
        out[r["organ"]] = dict(oscillates=bool(nb >= 3 and f > 0.0), beats=int(nb),
                               relaxation_freq_arb=round(float(f), 8), tau_s=float(taus),
                               predicted_cpm=round(float(K_TIME * f), 4),
                               rate_anchor=r["rate_note"], mechanism_grade="[V]", rate_grade="[L]")
    return out

# ===========================================================================
#  CIRCULATE  -- emerge, then run a CANONICAL pass of every dynamic subsystem so the
#  determinism fingerprint (2x sha256) covers the whole model. WIDE sweeps live in stress_tests.
# ===========================================================================
def circulate():
    organs = emerge_organs(); osc = confirm_oscillators()
    clock  = slow_wave_clock()
    chain  = intestinal_chain(N=12)
    peri   = dict(physiologic_aboral_disp=round(peristalsis_transport(+1), 4),
                  reversed_oral_disp=round(peristalsis_transport(-1), 4),
                  grade="[V]")
    # canonical homeostat probes
    _, Gf = glucose_homeostat(G0=5.0, T=60.0); fast = float(Gf[-1])
    _, Gm = glucose_homeostat(G0=fast, meal=_pulse(3.0), T=30.0)
    _, Gk = glucose_homeostat(G0=5.0, ins_kick=_pulse(2.0), T=30.0)
    homeo = dict(fasting_fixed_point_mM=round(fast, 4),
                 meal_amp3_peak_mM=round(float(Gm.max()), 4), meal_amp3_final_mM=round(float(Gm[-1]), 4),
                 insulin_kick2_nadir_mM=round(float(Gk.min()), 4), insulin_kick2_final_mM=round(float(Gk[-1]), 4),
                 setpoint_mM=G_SET, homeostasis_grade="[V]", setpoint_grade="[L]")
    return dict(_what="Digestive / Metabolic -- organs emerge from measured gamma; one gastric clock + a "
                      "closed metabolic loop drive the dynamics.",
                organs=organs, oscillators=osc,
                dynamics=dict(slow_wave_clock=clock, intestinal_chain_cpm_N12=chain,
                              peristalsis=peri, glucose_homeostat=homeo))

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
