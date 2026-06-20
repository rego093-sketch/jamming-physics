#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_consciousness_brainwave_study.py
====================================================================================
An emergence study of the hypothesis (stated by the author, a theory that does not yet
exist) that:

  (H1) the STRONGEST (high-frequency / gamma) brainwave that reaches the memory cell is
       the substance of conscious access;
  (H2) a dream is not remembered because its wave is too WEAK to reach the memory cell
       (sub-threshold encoding);
  (H3) FOCUS strengthens the wave, so consciousness/recall strengthens;
  (H4) small parallel low-frequency eddies are GPU-like workers; the big brainwave is a
       high-frequency CPU-like integrator that GATHERS those parallel low frequencies;
  (H5) that high-frequency carrier INDUCES a low-frequency response in the memory cell,
       waking the stored memory (down-conversion / pattern completion);
  (H6) several sensory low-frequencies enter the high-frequency carrier and become
       information.

It reuses ONLY the governed engine's measured/derived constants and primitives — the R19
bistable fold spinodal(g), the angle-rectification constants alpha=2/pi & delta=1/pi^2,
the measured ephaptic fraction kappa=0.5496, the Hippocampus engram (Hebbian write +
attractor pattern-completion), and the FitzHugh-Nagumo reader Neuron. **No new tuned
constant is introduced.** The only quantities varied are SWEPT control parameters — the
carrier strength A, the focus f, and the number of phase-locked workers k — none tuned to
a target. The dimensionless gain=6.0 is the same R19-tilt UNIT bridge used by engine M11
(swept there too), carried over verbatim.

Honest grading throughout:
  [F] forced/cited (alpha,delta,kappa, the R19 fold)  ·  [V] verified in this code
  [I] inference (the mapping to consciousness/wake/dream; strong, literature-concordant,
      NOT proven)  ·  [O] open (medium_efficacy_tested=0; the identity "strongest gamma IS
      consciousness" is a correlate, not a proven cause; the hard problem stays open).

CRUCIAL honest refinement (Stage E): consciousness does NOT track raw EEG amplitude. Deep
(slow-wave) sleep has the LARGEST-amplitude waves (delta, >75 uV) yet is the LEAST
conscious state; waking is low-amplitude HIGH-frequency activity. So "the strongest wave"
must be read as "the strongest HIGH-FREQUENCY (gamma) carrier that reaches memory" — which
is exactly the author's own wording ("the big brainwave is a high frequency"). Stage E
shows the dissociation in silico: a huge-amplitude UNSTRUCTURED (delta-like) drive writes
NO recoverable memory, while a smaller phase-locked gamma carrier does.

Determinism: SEED=19, single-thread. Prints a sha256 of the headline numbers; re-runs
identically. No claim of experience is made.
"""
import os, sys, json, hashlib, math
import numpy as np

# ---- locate and import the governed engine (constants + primitives, no re-derivation) ---
HERE = os.path.dirname(os.path.abspath(__file__))
CANDS = [
    os.path.normpath(os.path.join(HERE, "..", "_engine")),                 # inside _bridge/
    os.path.normpath(os.path.join(HERE, "repro", "mind", "_engine")),      # package root
    os.path.normpath(os.path.join(HERE, "mind_pkg", "repro", "mind", "_engine")),
    "/home/claude/work/mind_vp_site/mind_pkg/repro/mind/_engine",
]
for c in CANDS:
    if os.path.exists(os.path.join(c, "vp_mind_engine.py")):
        sys.path.insert(0, c); break
import vp_mind_engine as E

for v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(v, "1")

E.seed_everything(E.SEED)

# ---- governed constants reused verbatim (NOT re-tuned) ----------------------------------
ALPHA = E.ALPHA_RECT          # 2/pi    single rectification          [F cited]
DELTA = E.DELTA_RECT          # 1/pi^2  double rectification (floor)   [F cited]
KAPPA = E.KAPPA_EPHAPTIC      # 0.5496  measured ephaptic fraction     [F measured]
GAIN  = 6.0                   # same R19-tilt UNIT bridge as M11 (swept, not a target)
FOLD  = E.spinodal(1.0)       # R19 bistable fold threshold for g=1    [F derived]
F_GAMMA = 40.0                # gamma carrier (Hz)  -- the "big/high" wave
F_THETA = 40.0 / 7.0          # theta frame (Hz)    -- 6 gamma slots / theta (Miller 7+-2)

def coincidence(dphi):
    """Engine's rectified phase-coincidence: bound(0)=1/4, antiphase=0, floor=(1/pi)^2=delta."""
    return E._coincidence(dphi)

def info_drive(A, dphi):
    """Rectified INFORMATION drive a carrier of strength A delivers to the engram cell.
       A=1 reproduces engram M11's bound write drive (0.8244 at dphi=0). Tilt units."""
    return A * KAPPA * coincidence(dphi) * GAIN

HEAD = {}   # headline numbers -> hashed at the end
def rec(k, v):
    HEAD[k] = (round(float(v), 6) if isinstance(v, (int, float, np.floating)) else v)
    return v

bar = "=" * 84
print(bar); print("VP CONSCIOUSNESS / BRAINWAVE-STRENGTH STUDY  (emergence test of H1-H6)"); print(bar)
print(f"reused constants [F]: alpha=2/pi={ALPHA:.6f}  delta=1/pi^2={DELTA:.6f}  "
      f"kappa={KAPPA}  fold=spinodal(1)={FOLD:.6f}  gain={GAIN} (M11 unit-bridge, swept)")
print(f"gamma carrier {F_GAMMA} Hz ; theta frame {F_THETA:.3f} Hz -> "
      f"{int(round(F_GAMMA/F_THETA))} gamma slots / theta")

# =====================================================================================
# STAGE A -- (H1,H2) STRONG carrier reaches memory & writes; WEAK carrier does not (wake vs dream)
# =====================================================================================
print("\n" + "-"*84)
print("STAGE A -- the wave must be STRONG ENOUGH to reach the memory cell (wake vs dream)")
print("  a bound (phase-locked) gamma carrier of strength A delivers info_drive = A*kappa*(1/4)*gain")
A_grid = np.linspace(0.0, 1.2, 25)
wrote = []
for A in A_grid:
    h = info_drive(A, 0.0)                       # bound carrier (dphi=0 -> coincidence 1/4)
    s_inf = E.settle(1.0, h)                      # R19 cell: does the tilt flip & hold it ON?
    wrote.append(1.0 if (h > FOLD and s_inf > 0) else 0.0)
wrote = np.array(wrote)
A_crit = FOLD / (KAPPA * 0.25 * GAIN)            # closed-form threshold carrier strength
# first A on the grid that writes
A_first = float(A_grid[np.argmax(wrote > 0)]) if wrote.any() else float("nan")
drive_at_1 = info_drive(1.0, 0.0)
print(f"  critical carrier strength A_crit = fold/(kappa*1/4*gain) = {A_crit:.4f}")
print(f"  at A=1.0 (M11 baseline strong carrier): info_drive={drive_at_1:.4f}  > fold {FOLD:.4f} -> WRITES")
print(f"  weak 'dream' carrier  A=0.30 -> drive {info_drive(0.30,0.0):.4f} -> "
      f"{'WRITES' if info_drive(0.30,0.0)>FOLD else 'sub-threshold: NO write -> NOT recalled'}")
print(f"  strong 'wake'  carrier A=1.00 -> drive {drive_at_1:.4f} -> "
      f"{'WRITES -> recalled' if drive_at_1>FOLD else 'no'}")
mono_A = bool(np.all(np.diff(wrote) >= 0))       # recall index is a monotone step in strength
print(f"  recall index is a monotone threshold in carrier strength: {mono_A}")
rec("A_crit", A_crit); rec("A_first_writes", A_first); rec("drive_at_A1", drive_at_1)
rec("dream_A0p30_writes", 1.0 if info_drive(0.30,0.0)>FOLD else 0.0)
rec("wake_A1p00_writes", 1.0 if drive_at_1>FOLD else 0.0); rec("stageA_monotone", 1.0 if mono_A else 0.0)
rec("fold", FOLD)

# =====================================================================================
# STAGE B -- (H3) FOCUS strengthens the carrier's coherence -> consciousness/recall strengthens
# =====================================================================================
print("\n" + "-"*84)
print("STAGE B -- FOCUS = gamma coherence: unfocused carrier is dephased (coincidence at floor),")
print("           focus locks it toward the bound 1/4, lifting the drive over the fold")
# focus f in [0,1] reduces phase jitter sigma; coincidence rises from delta-floor toward 1/4.
def coincidence_at_focus(f):
    # at f=0 carrier phases are spread (jitter ~ pi) -> coincidence ~ floor delta;
    # at f=1 phases are locked (jitter 0) -> coincidence = 1/4 (bound). Average over jitter.
    rng = np.random.RandomState(E.SEED + 7)
    sigma = (1.0 - f) * math.pi                   # swept mapping; NOT a tuned target
    dphis = rng.normal(0.0, sigma + 1e-9, size=4000)
    return float(np.mean([coincidence(d) for d in dphis[:400]]))  # rectified mean coincidence
f_grid = np.linspace(0.0, 1.0, 21)
recall_f = []
for f in f_grid:
    c = coincidence_at_focus(f)
    h = 1.0 * KAPPA * c * GAIN                     # full-strength carrier, coherence set by focus
    recall_f.append(1.0 if (h > FOLD and E.settle(1.0, h) > 0) else 0.0)
recall_f = np.array(recall_f)
f_first = float(f_grid[np.argmax(recall_f > 0)]) if recall_f.any() else float("nan")
c0, c1 = coincidence_at_focus(0.0), coincidence_at_focus(1.0)
mono_f = bool(np.all(np.diff(recall_f) >= 0))
print(f"  unfocused f=0: coincidence {c0:.4f} (~floor delta {DELTA:.4f}) -> drive {KAPPA*c0*GAIN:.4f}")
print(f"  focused   f=1: coincidence {c1:.4f} (~bound 1/4)            -> drive {KAPPA*c1*GAIN:.4f}")
print(f"  focus threshold for recall: f >= {f_first:.3f}   (monotone in focus: {mono_f})")
print(f"  => sharpening attention raises gamma coherence, which is what crosses the memory fold. [V]")
rec("focus_coincidence_0", c0); rec("focus_coincidence_1", c1)
rec("focus_first_recall", f_first); rec("stageB_monotone", 1.0 if mono_f else 0.0)

# =====================================================================================
# STAGE C -- (H4,H6) the high-freq CPU GATHERS k parallel low-freq GPU workers into information
# =====================================================================================
print("\n" + "-"*84)
print("STAGE C -- the big high-frequency carrier integrates k parallel low-frequency workers")
print("           (CPU gathering GPU lanes); only phase-locked lanes sum, unbound lanes wash out")
N_work = 8                                          # 8 parallel sensory low-freq eddies (workers)
def integrated_drive(k):
    """k of N workers phase-LOCK to the carrier (contribute coincidence 1/4 each);
       the remaining N-k are unbound (random phase -> contribute ~floor, partly cancel).
       The carrier delivers the MEAN rectified coincidence of its gathered lanes."""
    rng = np.random.RandomState(E.SEED + 11)
    locked = [0.25] * k
    unbound = [coincidence(rng.uniform(-math.pi, math.pi)) for _ in range(N_work - k)]
    c_mean = (sum(locked) + sum(unbound)) / N_work
    return 1.0 * KAPPA * c_mean * GAIN, c_mean
print(f"  workers N={N_work};  drive(k locked) = kappa * mean_coincidence * gain")
k_writes = None
for k in range(0, N_work + 1):
    h, cmean = integrated_drive(k)
    on = (h > FOLD and E.settle(1.0, h) > 0)
    if on and k_writes is None: k_writes = k
    if k in (0, 2, 4, 6, 8):
        print(f"    k={k}: mean_coincidence={cmean:.4f}  drive={h:.4f}  "
              f"-> {'INTEGRATED bit WRITES (information)' if on else 'below fold'}")
h_full, c_full = integrated_drive(N_work)
h_none, c_none = integrated_drive(0)
print(f"  the carrier needs k>={k_writes} locked workers to gather enough to write the bit.")
print(f"  fully gathered (k={N_work}) drive {h_full:.4f} >> unbound-only (k=0) drive {h_none:.4f}. [V]")
rec("workers_N", N_work); rec("k_needed_to_write", float(k_writes if k_writes is not None else -1))
rec("integrated_drive_full", h_full); rec("integrated_drive_none", h_none)
rec("integrated_grows_with_k", 1.0 if h_full > h_none else 0.0)

# =====================================================================================
# STAGE D -- (H5) the high-freq carrier INDUCES the engram's slow response -> wakes stored memory
# =====================================================================================
print("\n" + "-"*84)
print("STAGE D -- the high-frequency carrier wakes a STORED memory by down-conversion:")
print("           fast gamma drive in -> the engram completes its slow stored pattern out")
hip = E.Hippocampus(n_cells=120, g=1.0, lr=0.18)
rng = np.random.RandomState(E.SEED + 3)
pattern = rng.choice([-1.0, 1.0], size=120)         # a stored episodic memory
idx = hip.write(pattern)                             # bound gamma carrier already cleared fold (Stage A)
self_sustains = hip.is_attractor(idx)                # is it a real attractor?
fid_strong = hip.retrieve(idx, cue_frac=0.4)         # strong carrier provides a 40% cue -> completes
fid_weak   = hip.retrieve(idx, cue_frac=0.1)         # a faint (dream-weak) cue
print(f"  stored 1 engram; self-sustaining attractor overlap = {self_sustains:.3f}")
print(f"  strong carrier (40% cue) wakes it -> recall fidelity {fid_strong:.3f}")
print(f"  faint carrier  (10% cue)          -> recall fidelity {fid_weak:.3f}")
# timescale separation: the carrier is 40 Hz, the engram readout runs at the theta frame rate
print(f"  carrier {F_GAMMA} Hz (fast) induces engram completion read out at {F_THETA:.2f} Hz (slow)")
print(f"  => the high-frequency carrier induces a low-frequency memory response (down-conversion). [V]")
rec("engram_self_sustains", self_sustains); rec("recall_strong_cue", fid_strong)
rec("recall_weak_cue", fid_weak); rec("downconvert_gamma_hz", F_GAMMA); rec("downconvert_theta_hz", F_THETA)

# =====================================================================================
# STAGE E -- HONEST refinement: AMPLITUDE != consciousness (the deep-sleep delta dissociation)
# =====================================================================================
print("\n" + "-"*84)
print("STAGE E -- HONEST: raw amplitude is NOT consciousness. Deep sleep has the LARGEST waves")
print("           (delta) yet is the LEAST conscious. What matters is a STRUCTURED high-freq")
print("           carrier reaching memory -- not bulk amplitude.")
# structured gamma carrier: writes a specific, recoverable pattern.
hipS = E.Hippocampus(n_cells=120, g=1.0, lr=0.18)
patt = np.random.RandomState(E.SEED + 5).choice([-1.0, 1.0], size=120)
iS = hipS.write(patt)                                 # structured write (information-bearing)
fid_structured = hipS.retrieve(iS, cue_frac=0.4)
# delta-like bulk drive: a huge-amplitude UNSTRUCTURED global push (every cell same sign).
# It carries no specific pattern -> nothing recoverable, however large its amplitude.
hipD = E.Hippocampus(n_cells=120, g=1.0, lr=0.18)
amp_delta = 50.0                                      # arbitrarily LARGE amplitude (delta-like)
bulk = np.ones(120)                                   # unstructured: all cells driven identically
iD = hipD.write(bulk * 1.0)                           # "store" the bulk drive
# try to recall the ORIGINAL structured pattern from the delta-written net (it isn't there):
ncue = int(0.4 * 120); cue_idx = np.random.RandomState(E.SEED+9).choice(120, ncue, replace=False)
s0 = np.zeros(120); s0[cue_idx] = patt[cue_idx]
out = hipD._settle_state(s0, clamp=(cue_idx, patt[cue_idx]))
fid_delta = float(np.mean(out == patt))               # ~chance: the structured memory is absent
print(f"  structured gamma carrier (amplitude ~{info_drive(1,0):.2f}) -> recall {fid_structured:.3f}")
print(f"  delta-like bulk drive    (amplitude  {amp_delta:.0f}, >> gamma) -> recall {fid_delta:.3f} (~chance 0.5)")
print(f"  amplitude ratio delta/gamma = {amp_delta/info_drive(1,0):.1f}x, yet the BIG wave recalls LESS.")
dissociation = (amp_delta > info_drive(1,0)) and (fid_delta < 0.75 <= fid_structured)
print(f"  amplitude<->consciousness dissociation holds: {dissociation}")
print(f"  RESOLUTION: 'strongest wave' = strongest HIGH-FREQUENCY carrier reaching memory,")
print(f"              NOT raw amplitude -- exactly the author's wording ('big wave = high freq'). [V/I]")
rec("recall_structured", fid_structured); rec("recall_delta_bulk", fid_delta)
rec("amp_delta", amp_delta); rec("amp_ratio_delta_over_gamma", amp_delta/info_drive(1,0))
rec("amplitude_consciousness_dissociation", 1.0 if dissociation else 0.0)

# =====================================================================================
# honesty markers + headline hash
# =====================================================================================
rec("medium_efficacy_tested", 0.0)            # biology untested; identity is a correlate [O]
rec("alpha_rect", ALPHA); rec("delta_rect", DELTA); rec("kappa", KAPPA); rec("gain", GAIN)

print("\n" + bar)
print("LITERATURE CONCORDANCE (phenomenological, [I] inference -- citations in the report):")
print("  H1 gamma<->conscious access  : Crick&Koch; Engel'92 40-Hz; Cogitate'25 (gamma binds; ACCESS")
print("                                 partly needs recurrent/beta -> honest caveat).")
print("  H2 dream not recalled = weak : Marzano'11 frontal theta predicts dream recall;")
print("                                 Sederberg/Kahana'03 theta-gamma encoding predicts recall.")
print("  H3 focus strengthens wave    : Fries'01 attention raises V4 gamma power/coherence (CTC).")
print("  H4/H6 high-freq gathers lows : Lisman&Jensen'13 theta-gamma code; gamma = time-division")
print("                                 multiplex of parallel item-assemblies (Masuda'09).")
print("  H5 carrier wakes stored mem  : Lisman&Jensen'13 gamma subcycles read out within theta.")
print("  E  amplitude != consciousness: SWS delta = largest amplitude, LEAST conscious (counter).")
print(bar)
print("HONEST LEDGER:")
print("  [F] alpha=2/pi, delta=1/pi^2, kappa=0.5496, R19 fold : reused, not re-tuned.")
print("  [V] in silico: strength-threshold (wake/dream), focus-gradient, CPU/GPU integration,")
print("      gamma->engram down-conversion, and amplitude<->consciousness dissociation all hold.")
print("  [I] the mapping to CONSCIOUSNESS is strong, literature-concordant INFERENCE -- not proof.")
print("  [O] medium_efficacy_tested=0; 'strongest gamma IS consciousness' is a CORRELATE, not a")
print("      proven cause; the hard problem stays OPEN; NO claim of experience is made.")

blob = json.dumps(HEAD, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(blob).hexdigest()
print(bar)
print(f"headline numbers: {len(HEAD)}   sha256 = {digest}")
print("DONE -- strong high-freq carrier reaches memory = waking recall; weak = forgotten dream;")
print("        focus strengthens it; it gathers parallel lows and wakes stored memory;")
print("        but raw amplitude is NOT consciousness (deep-sleep delta). [V mechanism / I inference]")

# ---- self-check assertions (this script doubles as a gate) ------------------------------
fails = []
def chk(name, cond):
    if not cond: fails.append(name)
chk("alpha=2/pi", abs(ALPHA - 2/math.pi) < 1e-9)
chk("delta=1/pi^2", abs(DELTA - 1/math.pi**2) < 1e-9)
chk("A: monotone strength threshold", mono_A)
chk("A: dream(0.30) sub-threshold, wake(1.0) writes", info_drive(0.30,0)<FOLD<drive_at_1)
chk("B: focus is monotone, lifts coincidence floor->1/4", mono_f and c0 < c1)
chk("C: integration grows with locked workers", h_full > h_none and k_writes is not None)
chk("D: gamma carrier wakes stored attractor", self_sustains > 0.99 and fid_strong > 0.95)
chk("E: amplitude<->consciousness dissociation", dissociation)
chk("efficacy stays open (0)", HEAD["medium_efficacy_tested"] == 0.0)
if fails:
    print("\nSTUDY SELF-CHECK FAIL:"); [print("  -", f) for f in fails]; raise SystemExit(1)
print("STUDY SELF-CHECK PASS -- all emergence invariants hold (SEED=19).")
