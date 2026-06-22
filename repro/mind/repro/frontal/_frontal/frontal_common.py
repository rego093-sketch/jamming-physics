#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontal_common.py  --  shared substrate + read-outs for the VP FRONTAL simulation
==================================================================================
INDEPENDENT simulation, NOT the 29th atlas citizen.  It shares the frozen R19
engine and the three reusable layers READ-ONLY (hash-pinned by the gate); it has
its own lightweight gate and NEVER calls the mind atlas runner (run_all_atlas.py).

Everything here is a STRUCTURAL quantity of the frozen ephaptic coupling model on
a 12-node kernel.  Sign/structure only; all magnitudes [O].  No new constant.

Substrate (frozen, READ-ONLY):
    N = 12 organ nodes (the engine's coarse brain; the cortical node is the
        undifferentiated `neocortex`/FOXG1 lump -- there is NO frontal-lobe node;
        see the two HARD LIMITS in the F1 module and the README).
    OMEGA0  = mean natural frequency           (M9 operating point)
    KAPPA   = E.KAPPA_EPHAPTIC                  (the one global coupling)
    FOLD    = E.spinodal(1.0)                   (the R19 ignition fold)
    W0      = E._ephaptic_kernel(POS)           (row-stochastic 1/r^3 kernel)

Effective per-node coupling map (IDENTICAL to the schizophrenia / epilepsy / E0
modules -- imported convention, NOT a new constant):
    k(b) = KAPPA / (1 - |b|)   for b >= 0  (excitatory drive),  capped at 2*KAPPA
    k(b) = KAPPA / (1 + |b|)   for b <  0  (inhibitory silence)

Bit-for-bit anchor:  the per-node integrator below, with a UNIFORM drive,
reproduces the engine M9 anchor R = 0.38961455156044245 EXACTLY (verified:
engine_anchor_bitforbit()).  That is the engine-invariance guard.
"""
import os, sys, math, json, hashlib

# --- BLAS pinned single-thread BEFORE numpy (determinism across machines) ------
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
_ENGINE_DIR = os.path.join(HERE, "..", "_engine")
_LAYERS_DIR = os.path.join(HERE, "..", "_layers")
if _ENGINE_DIR not in sys.path:
    sys.path.insert(0, _ENGINE_DIR)
import vp_mind_engine as E   # the frozen engine, READ-ONLY

SEED = E.SEED                 # 19
DT_DEFAULT = 0.001
T_DEFAULT = 6.0

# --- frozen provenance the sim asserts (directive + SSOT §9) -------------------
ENGINE_FILE_SHA256 = "e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371"
ENGINE_TREE_SHA256 = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"
M9_ANCHOR_R        = 0.38961455156044245

# ------------------------------------------------------------------------------
#  Substrate (loaded once from the frozen engine)
# ------------------------------------------------------------------------------
def load_substrate():
    A = E.load_brain_atlas()
    regs = list(A["organs"].keys())
    f0 = np.array([A["organs"][r]["f0_hz"] for r in regs], dtype=float)
    omega = 2.0 * math.pi * f0
    omega0 = float(np.mean(omega))
    pos = E._measured_geometry(regs)
    W0 = E._ephaptic_kernel(pos)
    kap = float(E.KAPPA_EPHAPTIC)
    fold = float(E.spinodal(1.0))
    return {
        "REGS": regs, "N": len(regs), "F0": f0,
        "OMEGA": omega, "OMEGA0": omega0,
        "POS": pos, "W0": W0, "KAP": kap, "FOLD": fold,
    }

_S = load_substrate()
REGS, N = _S["REGS"], _S["N"]
OMEGA, OMEGA0 = _S["OMEGA"], _S["OMEGA0"]
POS, W0, KAP, FOLD = _S["POS"], _S["W0"], _S["KAP"], _S["FOLD"]

# the eight nodes with non-negligible mass on both lesion axes (the rest are
# peripheral; the SSOT reads the lobotomy signature among MAJOR nodes only).
MAJOR = ("neocortex", "thalamus", "midbrain", "basal_forebrain_chol",
         "cerebellum", "hippocampus", "striatum", "pallidum")

def idx(name):
    return REGS.index(name)

# ------------------------------------------------------------------------------
#  Effective coupling map  (imported convention -- NO new constant)
# ------------------------------------------------------------------------------
def k_bias(b):
    """k(b)=KAP/(1-|b|) excit (cap 2*KAP) ; KAP/(1+|b|) inhib. Same as the
    schizophrenia / epilepsy / E0 modules."""
    if b >= 0.0:
        return min(KAP / (1.0 - min(b, 0.95)), 2.0 * KAP)
    return KAP / (1.0 + abs(b))

def uniform_K():
    return np.full(N, KAP * OMEGA0)

def focal_K(i, b0):
    """Excitatory focal drive of depth b0 on node i, baseline elsewhere."""
    bv = np.zeros(N); bv[i] = abs(b0)
    return np.array([k_bias(x) for x in bv]) * OMEGA0

def silence_K(i, b=-0.9):
    """Inhibitory SILENCE of node i (the §45 lesion pattern); baseline elsewhere.
    NOT a real lesion -- a coupling-bias read on a 12-node model (firewall)."""
    bv = np.zeros(N); bv[i] = b
    return np.array([k_bias(x) for x in bv]) * OMEGA0

def scattered_omega(disp):
    """Frequency-dispersion knob. disp=1 -> frozen engine; disp>1 -> scattered
    input (the deviation of each node's frequency from the mean is multiplied)."""
    return OMEGA0 + disp * (OMEGA - OMEGA0)

# ------------------------------------------------------------------------------
#  Integrator -- byte-identical to E._integrate when Kvec is uniform
#  (verified: engine_anchor_bitforbit()).  Per-node Kvec generalises it.
# ------------------------------------------------------------------------------
def _order(th):
    return float(abs(np.mean(np.exp(1j * th))))

def integrate(Kvec, omega, ic="random", t_a=None, t_b=None,
              T=T_DEFAULT, dt=DT_DEFAULT, seed=SEED):
    """Phase dynamics identical to the engine integrator.
       ic='random'   : incoherent IC  (build a percept from scattered input)
       ic='coherent' : synchronised IC (hold an already-built chain)
       [t_a,t_b]     : averaging window in seconds; default = second half."""
    rng = np.random.RandomState(seed)
    th = rng.uniform(-math.pi, math.pi, N) if ic == "random" else np.zeros(N)
    ns = int(T / dt)
    Rs = np.empty(ns)
    for s in range(ns):
        diff = th[None, :] - th[:, None]
        th = th + dt * (omega + Kvec * np.sum(W0 * np.sin(diff), axis=1))
        Rs[s] = _order(th)
    if t_a is None:
        h = ns // 2
        return float(np.mean(Rs[h:]))
    return float(np.mean(Rs[int(t_a / dt):int(t_b / dt)]))

# ------------------------------------------------------------------------------
#  READ-OUTS (exact definitions from SSOT §2-§3; reproduced on the frozen kernel)
# ------------------------------------------------------------------------------
def convergence():
    """SSOT §2 -- 'patternisation' = effective in-degree (fan-in) of each kernel
    ROW = 1 / sum_j W0[i,j]^2 (inverse participation ratio). High => the node
    gathers input from many neighbours (a convergence hub); ~1 => it draws ~all
    of its input from a single neighbour. Static; no dynamics."""
    return {REGS[i]: float(1.0 / np.sum(W0[i] ** 2)) for i in range(N)}

def thread_holding(b0, disp=5.0):
    """SSOT §3 Test 2 -- establish coherence by focally driving node i, inject
    scatter (disp), measure how well the GLOBAL order parameter R is maintained
    against the scatter: dR(i) = R(focal drive i, disp) - R(baseline, disp).
    The thread-HOLDER keeps R up against scatter; the gatherer does not."""
    om = scattered_omega(disp)
    base = integrate(uniform_K(), om, ic="random")
    return {REGS[i]: float(integrate(focal_K(i, b0), om, ic="random") - base)
            for i in range(N)}

def broadcaster_structure():
    """Robust static asymmetry: fan-IN (effective in-degree of row i, IPR) vs
    OUT-influence (column mass others place on node i). A node with LOW fan-in but
    HIGH out-influence is a broadcaster locked to ~one source, NOT a gatherer."""
    in_eff = {REGS[i]: float(1.0 / np.sum(W0[i] ** 2)) for i in range(N)}
    col_mass = {REGS[j]: float(W0[:, j].sum()) for j in range(N)}
    in_order = sorted(in_eff, key=lambda k: in_eff[k])           # ascending
    out_order = sorted(col_mass, key=lambda k: -col_mass[k])     # descending
    return {
        "in_eff": in_eff, "col_mass": col_mass,
        "in_rank_low_is_1": {k: in_order.index(k) + 1 for k in REGS},
        "out_rank_high_is_1": {k: out_order.index(k) + 1 for k in REGS},
    }

def holding_recovery(seeds=range(19, 39), kick=0.6, settle_T=4.0, rec_T=3.0,
                     b_silence=-0.9, dt=DT_DEFAULT):
    """ROBUST temporal-holding test (seed-averaged): settle to the coherent
    attractor, apply a standardised phase KICK, measure recovered R (second half)
    with node i silenced vs baseline.  A genuine HOLDER's silencing degrades
    recovery (mean dR << 0, significantly).  Averaging over kick realisations is
    the anti-tuning that the single-point probe lacked -- it is what distinguishes
    a real sustaining role from an operating-point artefact."""
    def settle(Kvec, seed, T):
        rng = np.random.RandomState(seed)
        th = rng.uniform(-math.pi, math.pi, N)
        for _ in range(int(T / dt)):
            d = th[None, :] - th[:, None]
            th = th + dt * (OMEGA + Kvec * np.sum(W0 * np.sin(d), axis=1))
        return th
    def recover(Kvec, th0, seed, T):
        rng = np.random.RandomState(seed)
        th = th0 + kick * rng.uniform(-math.pi, math.pi, N)
        ns = int(T / dt); Rs = np.empty(ns)
        for s in range(ns):
            d = th[None, :] - th[:, None]
            th = th + dt * (OMEGA + Kvec * np.sum(W0 * np.sin(d), axis=1))
            Rs[s] = _order(th)
        return float(np.mean(Rs[ns // 2:]))
    agg = {nm: [] for nm in REGS}
    for seed in seeds:
        th0 = settle(uniform_K(), seed, settle_T)
        base = recover(uniform_K(), th0, seed * 7, rec_T)
        for i in range(N):
            agg[REGS[i]].append(recover(silence_K(i, b_silence), th0, seed * 7, rec_T) - base)
    mean = {nm: float(np.mean(agg[nm])) for nm in REGS}
    std = {nm: float(np.std(agg[nm])) for nm in REGS}
    return {"mean_dR": mean, "std_dR": std,
            "n_seeds": len(list(seeds)), "kick": kick}

def lobotomy(Th, b_silence=-0.9):
    """SSOT §3 Test 3 -- silence node i, measure
        d_instant  : built coherence from an INCOHERENT IC (perception built
                     from scattered input) -- the steady second-half R.
        d_sustain  : held coherence of an ALREADY-COHERENT state over the holding
                     window [0,Th] (the chain held before it re-equilibrates).
    The lobotomy signature = most-negative (d_sustain - d_instant): instant
    SPARED, sustained COLLAPSES. d_instant is window-free; the sustained collapse
    is a finite-DEPTH holding phenomenon (washes out as Th grows -> the network
    re-equilibrates to the same attractor; see the Th sweep in F1)."""
    base_i = integrate(uniform_K(), OMEGA, ic="random")
    base_s = integrate(uniform_K(), OMEGA, ic="coherent", t_a=0.0, t_b=Th)
    out = {}
    for i in range(N):
        Ksil = silence_K(i, b_silence)
        di = integrate(Ksil, OMEGA, ic="random") - base_i
        ds = integrate(Ksil, OMEGA, ic="coherent", t_a=0.0, t_b=Th) - base_s
        out[REGS[i]] = {"d_instant": float(di), "d_sustain": float(ds),
                        "signature": float(ds - di)}
    return out

# ------------------------------------------------------------------------------
#  FRONTAL-LESION read-outs (the leucotomy DISSOCIATION + the flexibility axis)
#  Lesion model: a leucotomy/lobotomy SEVERS the cortical node's connections
#  (white-matter tract), it does NOT silence the node.  So the frontal lesion is
#  a DISCONNECTION (zero the node's coupling row + column), isolating it -- not an
#  inhibitory bias.  No new constant.
# ------------------------------------------------------------------------------
CUE_NODES = ("thalamus", "hippocampus", "striatum", "midbrain")
SHIFT_PAIRS = (("thalamus", "hippocampus"), ("thalamus", "striatum"),
               ("hippocampus", "striatum"), ("striatum", "pallidum"))

def disconnect_W(i):
    """Leucotomy isolation: sever node i from the ephaptic field (zero its row and
    column in the coupling kernel). The node free-runs; the field no longer feels
    it. This is the connection-severing lesion, not a silence."""
    W = W0.copy(); W[i, :] = 0.0; W[:, i] = 0.0
    return W

def immediate_response(Wmat, cues=CUE_NODES, seeds=range(19, 31), depth=0.7,
                       t=1.0, dt=DT_DEFAULT):
    """Perception: the order parameter R WHILE a stimulus is present (focal drive
    on a cue node). Seed-averaged over cues. This is the 'input present -> output'
    response that frontal patients RETAIN."""
    vals = []
    for c in cues:
        ci = idx(c)
        for seed in seeds:
            rng = np.random.RandomState(seed)
            th = rng.uniform(-math.pi, math.pi, N)
            bv = np.zeros(N); bv[ci] = depth
            K = np.array([k_bias(b) for b in bv]) * OMEGA0
            ns = int(t / dt); Rs = np.empty(ns)
            for s in range(ns):
                d = th[None, :] - th[:, None]
                th = th + dt * (OMEGA + K * np.sum(Wmat * np.sin(d), axis=1))
                Rs[s] = _order(th)
            vals.append(float(np.mean(Rs[ns // 2:])))
    return float(np.mean(vals))

def flexibility(Wmat, pairs=SHIFT_PAIRS, seeds=range(19, 31), depth=0.7,
                tA=1.0, tB=1.0, dt=DT_DEFAULT):
    """Set-shifting: drive cue A, then SWITCH the drive to cue B; measure how much
    the field's phase configuration moved away from the A-pattern.
    flexibility = 1 - |<exp(i*(th_endB - th_endA))>|.  LOW flexibility = the output
    stayed locked to A despite the input switching = PERSEVERATION. Seed-averaged
    over pairs (both directions)."""
    vals = []
    for an, bn in pairs:
        a, b = idx(an), idx(bn)
        for seed in seeds:
            for A, B in ((a, b), (b, a)):
                rng = np.random.RandomState(seed)
                th = rng.uniform(-math.pi, math.pi, N)
                bA = np.zeros(N); bA[A] = depth
                bB = np.zeros(N); bB[B] = depth
                KA = np.array([k_bias(x) for x in bA]) * OMEGA0
                KB = np.array([k_bias(x) for x in bB]) * OMEGA0
                for s in range(int(tA / dt)):
                    d = th[None, :] - th[:, None]
                    th = th + dt * (OMEGA + KA * np.sum(Wmat * np.sin(d), axis=1))
                thA = th.copy()
                for s in range(int(tB / dt)):
                    d = th[None, :] - th[:, None]
                    th = th + dt * (OMEGA + KB * np.sum(Wmat * np.sin(d), axis=1))
                vals.append(1.0 - float(abs(np.mean(np.exp(1j * (th - thA))))))
    return float(np.mean(vals))

DURATIONS = (0.8, 1.0, 1.2, 1.5)

def frontal_lesion_probe(seeds=range(19, 27)):
    """Probe whether disconnecting the cortical node reproduces the leucotomy
    behavioural record (perception spared + a sustained/flexibility deficit).
    PERCEPTION is measured across durations (robustly spared?).  FLEXIBILITY
    (set-shifting) is measured across a DURATION SWEEP -- the anti-tuning that
    reveals whether the perseveration signal is sign-stable (robust) or flips
    (an operating-point artefact)."""
    nc = idx("neocortex")
    Wi, Wl = W0.copy(), disconnect_W(nc)
    perc = {}
    for t in DURATIONS:
        pi = immediate_response(Wi, seeds=seeds, t=t)
        pl = immediate_response(Wl, seeds=seeds, t=t)
        perc[f"t={t}"] = {"intact": pi, "lesion": pl,
                          "d_pct": float(100.0 * (pl - pi) / pi)}
    flx = {}
    for t in DURATIONS:
        fi = flexibility(Wi, seeds=seeds, tA=t, tB=t)
        fl = flexibility(Wl, seeds=seeds, tA=t, tB=t)
        flx[f"t={t}"] = {"intact": fi, "lesion": fl, "d": float(fl - fi),
                         "d_pct": float(100.0 * (fl - fi) / fi)}
    perception_spared_all = bool(all(abs(v["d_pct"]) < 6.0 for v in perc.values()))
    signs = [(1 if v["d"] > 0 else -1) for v in flx.values() if abs(v["d"]) > 0.005]
    flex_sign_stable = bool(len(signs) >= 2 and len(set(signs)) == 1)
    return {
        "perception_by_duration": perc,
        "flexibility_by_duration": flx,
        "perception_robustly_spared": perception_spared_all,
        "flexibility_sign_stable_across_durations": flex_sign_stable,
        "flexibility_sign_flips": bool(not flex_sign_stable and len(signs) >= 2),
    }


def engine_anchor_bitforbit():
    """The directive's guard: a uniform/zero-bias drive reproduces the frozen M9
    anchor EXACTLY (not ~1e-13) -- proving the read-outs run on the unmodified
    substrate. Uses the engine integrator E._integrate directly."""
    R_engine, _ = E._integrate(OMEGA, W0, KAP * OMEGA0)
    R_frontal = integrate(uniform_K(), OMEGA, ic="random")   # our integrator, uniform
    return {
        "engine_integrator_R": float(R_engine),
        "frontal_integrator_R_uniform": float(R_frontal),
        "anchor_target": M9_ANCHOR_R,
        "engine_matches_anchor_bitforbit": bool(R_engine == M9_ANCHOR_R),
        "frontal_matches_engine_bitforbit": bool(R_frontal == R_engine),
    }

def engine_tree_invariants():
    """Re-emerge the engine READ-ONLY and confirm the full tree + the M0..M16
    developmental subtree are byte-unchanged (the engine is not mutated)."""
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items()
                          if int(k.split("_")[0][1:]) <= 16})
    return {
        "engine_tree_sha256_live": tree_live,
        "engine_tree_unchanged": bool(tree_live == ENGINE_TREE_SHA256),
        "m0_16_subtree_unchanged": bool(sub016 == M0_16_FROZEN),
    }

# ------------------------------------------------------------------------------
#  Canonicalisation -- IDENTICAL convention to every atlas module
# ------------------------------------------------------------------------------
def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def digest_of(res):
    return hashlib.sha256(blob(res).encode()).hexdigest()


if __name__ == "__main__":
    g = engine_anchor_bitforbit()
    print("frontal_common substrate")
    print(f"  N={N}  OMEGA0={OMEGA0:.6f}  KAPPA={KAP}  FOLD={FOLD}")
    print(f"  engine M9 anchor bit-for-bit : {g['engine_matches_anchor_bitforbit']}  ({g['engine_integrator_R']})")
    print(f"  frontal integrator == engine : {g['frontal_matches_engine_bitforbit']}")
    print(f"  MAJOR nodes : {MAJOR}")
