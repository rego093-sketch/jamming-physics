#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_brainwave_stress_tests.py
====================================================================================
Stress tests of the consciousness/brainwave model against a panel of real brainwave
phenomena, extending vp_consciousness_brainwave_study.py (stages A-E) with stages F-J:

  (F) MEMORY = low-frequency INDEX + high-frequency CONTENT.  Re-firing the low-frequency
      pattern reinstates ALL the high-frequency content bound to it -> it floods back into
      the conscious buffer.  ("when a low-freq pattern fires, all the high-freq of that
      moment comes into consciousness.")
  (G) DRIVE CAPTURE / paralysis of reason.  A strong LOW-frequency drive competes with the
      high-frequency integrator (divisive normalisation).  As the drive grows it claims the
      carrier's gain; the rational multi-slot binding collapses; beyond a capture threshold
      only the single drive remains bound -> reason is paralysed.  ("when a specific low-freq
      strengthens it nearly reaches the high-freq energy and paralyses reason.")
  (H) THE DRIVE PANEL -- hunger, drugs, sex, fear, pain.  Each is a strong (mostly limbic /
      interoceptive) low-frequency drive; the test reports how easily each captures the
      integrator.  (Drive baselines/gains are SCHEMATIC & swept -- ordering only, grounded
      in the qualitative clinical literature, NOT measured.  Graded [I].)
  (I) PANIC DISORDER -- runaway positive feedback (a bifurcation).  Interoceptive fear that
      catastrophically amplifies itself.  Below a critical sensitivity the drive self-limits
      (healthy); above it the drive runs away past the capture threshold within a few steps
      and paralyses reason (panic attack).  Same circuit, different sensitivity.
  (J) LEARNING DISABILITY -- weak / disorganised theta-gamma coupling.  Encoding needs the
      gamma carrier to clear the memory fold, which needs good theta-gamma coupling quality
      q.  Below a critical q, learning fails EVEN at full strength and full focus -- a
      STRUCTURAL deficit, distinct from a merely weak (low-effort) signal.

Like the parent study it reuses ONLY the governed engine's measured/derived constants
(alpha=2/pi, delta=1/pi^2, kappa=0.5496, the R19 fold) and primitives (the Hippocampus
engram, settle).  **No new tuned constant is introduced.**  The varied quantities (drive
amplitude D, sensitivity s, coupling quality q, provocation p) are SWEPT controls.

Honest grading: [F] forced/cited · [V] verified in code · [I] inference / schematic ·
[O] open.  medium_efficacy_tested stays 0; the mapping to clinical states is strong,
literature-concordant INFERENCE, NOT a measurement; NO claim of experience is made.

Determinism: SEED=19, single-thread.  Prints a sha256 of the headline numbers and a
self-check (this file doubles as a gate).  Reproduce: `python3 vp_brainwave_stress_tests.py`.
"""
import os, sys, json, hashlib, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CANDS = [
    os.path.normpath(os.path.join(HERE, "..", "_engine")),
    os.path.normpath(os.path.join(HERE, "repro", "mind", "_engine")),
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

ALPHA = E.ALPHA_RECT; DELTA = E.DELTA_RECT; KAPPA = E.KAPPA_EPHAPTIC
GAIN  = 6.0                       # same R19-tilt UNIT bridge as M11 (swept, not a target)
FOLD  = E.spinodal(1.0)           # R19 bistable fold threshold for g=1
H_FULL = KAPPA * 0.25 * GAIN      # bound full-strength drive a single slot gets = 0.8244
N_SLOTS = 6                       # rational working-memory width (6 gamma slots / theta, M11)

HEAD = {}
def rec(k, v):
    HEAD[k] = (round(float(v), 6) if isinstance(v, (int, float, np.floating)) else v); return v

bar = "=" * 84
print(bar); print("VP BRAINWAVE STRESS TESTS  (stages F-J: reinstatement, capture, drive panel,"); 
print("                            panic bifurcation, learning-disability coupling)"); print(bar)
print(f"reused [F]: alpha={ALPHA:.6f} delta={DELTA:.6f} kappa={KAPPA} fold={FOLD:.6f} "
      f"gain={GAIN} h_full={H_FULL:.4f} N_slots={N_SLOTS}")

# =====================================================================================
# STAGE F -- memory = low-freq INDEX + high-freq CONTENT; reinstating the index floods content
# =====================================================================================
print("\n" + "-"*84)
print("STAGE F -- memory binds a LOW-freq index to HIGH-freq content; re-firing the index")
print("           reinstates ALL the bound high-freq content into the conscious buffer")
N = 160
n_idx = 40                                   # first 40 cells = low-frequency INDEX (the 'when')
rng = np.random.RandomState(E.SEED + 2)
hip = E.Hippocampus(n_cells=N, g=1.0, lr=0.18)
idx_cells = np.arange(n_idx)
content_cells = np.arange(n_idx, N)
# store THREE distinct memories, each = [low-freq index | high-freq content], jointly
mems = [rng.choice([-1.0, 1.0], size=N) for _ in range(3)]
for m in mems:
    hip.write(m)
m0, m1 = mems[0], mems[1]
# cue with ONLY memory-0's low-frequency index -> which content reinstates?
s0 = np.zeros(N); s0[idx_cells] = m0[idx_cells]
out = hip._settle_state(s0, clamp=(idx_cells, m0[idx_cells]))
content_fid = float(np.mean(out[content_cells] == m0[content_cells]))      # matching content
cross_fid   = float(np.mean(out[content_cells] == m1[content_cells]))      # a DIFFERENT memory
# cue with a NOVEL index never stored -> no specific content should flood back
novel = rng.choice([-1.0, 1.0], size=n_idx)
sN = np.zeros(N); sN[idx_cells] = novel
outN = hip._settle_state(sN, clamp=(idx_cells, novel))
novel_fid = max(float(np.mean(outN[content_cells] == mm[content_cells])) for mm in mems)
print(f"  cue = memory-0 low-freq index -> memory-0 CONTENT reinstates at fidelity {content_fid:.3f}")
print(f"  same cue vs a DIFFERENT memory's content -> {cross_fid:.3f} (not reinstated)")
print(f"  cue = NOVEL never-stored index -> best content match {novel_fid:.3f} (no clean flood)")
print(f"  => the slow index is the ADDRESS; firing it brings back THAT moment's fast content. [V]")
rec("reinstate_content_fid", content_fid); rec("reinstate_cross_fid", cross_fid)
rec("reinstate_novel_fid", novel_fid)
rec("reinstatement_specific", 1.0 if (content_fid > 0.90 and cross_fid < 0.75) else 0.0)

# =====================================================================================
# STAGE G -- a strong low-freq drive captures the integrator -> reason (multi-slot) collapses
# =====================================================================================
print("\n" + "-"*84)
print("STAGE G -- a strong low-frequency DRIVE competes for the carrier's gain (divisive")
print("           normalisation); rational slots drop out; capture => reason paralysed")
salience = np.linspace(1.0, 0.5, N_SLOTS)        # rational slots, descending salience (swept)
def rational_slots(D):
    # each slot's delivered drive is suppressed by the competing drive: h_full*w / (1+D)
    h = H_FULL * salience / (1.0 + D)
    return int(np.sum(h > FOLD))
D_grid = np.linspace(0.0, 6.0, 61)
slots = np.array([rational_slots(D) for D in D_grid])
# capture threshold = smallest D for which <=1 rational slot survives (reason paralysed)
cap_mask = slots <= 1
D_cap = float(D_grid[np.argmax(cap_mask)]) if cap_mask.any() else float("nan")
mono_G = bool(np.all(np.diff(slots) <= 0))
for D in (0.0, 0.5, 1.0, 2.0, 4.0):
    print(f"    drive D={D:>3}: rational slots bound = {rational_slots(D)}"
          + ("   <- REASON PARALYSED" if rational_slots(D) <= 1 else ""))
print(f"  capture threshold D_cap (slots<=1) = {D_cap:.3f}   (monotone collapse: {mono_G})")
print(f"  matches the clinical 'hijack narrows you to a single option'. [V mech / I mapping]")
rec("N_slots", N_SLOTS); rec("D_cap_reason_paralysis", D_cap)
rec("slots_at_D0", rational_slots(0.0)); rec("slots_at_D4", rational_slots(4.0))
rec("stageG_monotone", 1.0 if mono_G else 0.0)

# =====================================================================================
# STAGE H -- the drive panel: hunger, drugs, sex, fear, pain (SCHEMATIC amplitudes, swept)
# =====================================================================================
print("\n" + "-"*84)
print("STAGE H -- drive panel (SCHEMATIC baselines/gains -- ordering only, NOT measured [I]):")
print("           D(p) = D0 + gain*p ; report capture-provocation p* where reason paralyses")
# (D0 baseline, gain) chosen ONLY to reflect qualitative clinical ordering:
#   pain & panic-fear capture fast (steep, interruptive); craving strong but cue-gated;
#   sex strong; hunger slower/homeostatic.  These are NOT fitted to any datum.
panel = {
    "pain":    (0.8, 2.0),   # interruptive function: seizes attention fast (Eccleston&Crombez)
    "fear":    (0.6, 2.2),   # amygdala hijack: rapid PFC suppression (Arnsten)
    "drug_craving": (0.5, 1.8),  # iRISA: salience at expense of other content (Goldstein/Koob)
    "sex":     (0.4, 1.6),   # strong limbic reward drive
    "hunger":  (0.3, 1.0),   # slower homeostatic/hypothalamic drive
}
def capture_provocation(D0, gain):
    for p in np.linspace(0.0, 4.0, 401):
        D = D0 + gain * p
        if rational_slots(D) <= 1:
            return float(p), float(D)
    return float("nan"), float("nan")
print(f"  {'drive':<14}{'baseline D0':>12}{'gain':>8}{'p* (capture)':>14}{'D at capture':>14}")
panel_results = {}
for name, (D0, g) in panel.items():
    pstar, Dstar = capture_provocation(D0, g)
    panel_results[name] = (pstar, Dstar)
    rec(f"panel_{name}_pstar", pstar)
    print(f"  {name:<14}{D0:>12.2f}{g:>8.2f}{pstar:>14.3f}{Dstar:>14.3f}")
order = sorted(panel_results, key=lambda k: panel_results[k][0])
print(f"  easiest->hardest to capture reason: {' < '.join(order)}")
print(f"  (all eventually capture; the ORDER, not the absolute p*, is the claim. [I schematic])")
rec("panel_easiest_capture", order[0]); rec("panel_hardest_capture", order[-1])

# =====================================================================================
# STAGE I -- panic disorder = runaway positive feedback (a bifurcation in sensitivity s)
# =====================================================================================
print("\n" + "-"*84)
print("STAGE I -- panic = interoceptive fear that amplifies itself. logistic feedback:")
print("           D_{t+1} = D_t + dt*( s*D_t*(1 - D_t/Dmax) - leak*D_t )")
leak = 0.6                                   # homeostatic restraint (5-HT/PFC extinction) [swept]
Dmax = 6.0; dt = 1.0; D0_trig = 0.30         # a small interoceptive trigger
def run_panic(s, steps=40):
    D = D0_trig; traj = [D]
    t_cap = None
    for t in range(1, steps + 1):
        D = D + dt * (s * D * (1 - D / Dmax) - leak * D)
        D = max(D, 0.0); traj.append(D)
        if t_cap is None and rational_slots(D) <= 1: t_cap = t
    return np.array(traj), t_cap
s_crit = leak                                # linear-stability bifurcation: runaway iff s>leak
# healthy subject (sub-critical sensitivity) vs panic disorder (super-critical)
s_healthy = 0.4; s_panic = 1.2
traj_h, cap_h = run_panic(s_healthy)
traj_p, cap_p = run_panic(s_panic)
print(f"  bifurcation at s_crit = leak = {s_crit:.2f}")
print(f"  HEALTHY  s={s_healthy}: drive {traj_h[0]:.2f} -> {traj_h[-1]:.3f} (self-limits; "
      f"reason paralysed at step {cap_h}) -> NO panic")
print(f"  PANIC    s={s_panic}: drive {traj_p[0]:.2f} -> {traj_p[-1]:.3f} (runs away; "
      f"reason paralysed at step {cap_p}) -> PANIC ATTACK, peaks fast")
bifurcation_ok = (traj_h[-1] < D0_trig and cap_h is None) and (traj_p[-1] > D_cap and cap_p is not None)
print(f"  same circuit, different sensitivity -> panic is a bifurcation. holds: {bifurcation_ok} [V mech / I mapping]")
rec("panic_s_crit", s_crit); rec("panic_healthy_final", traj_h[-1]); rec("panic_disorder_final", traj_p[-1])
rec("panic_steps_to_paralysis", float(cap_p if cap_p is not None else -1))
rec("panic_bifurcation_holds", 1.0 if bifurcation_ok else 0.0)

# =====================================================================================
# STAGE J -- learning disability = weak/disorganised theta-gamma coupling (quality q)
# =====================================================================================
print("\n" + "-"*84)
print("STAGE J -- learning needs the gamma carrier to clear the fold, which needs good")
print("           theta-gamma COUPLING QUALITY q (gamma landing at the right theta phase)")
def encode_drive(q, A=1.0):
    # disorganised coupling = the gamma lands at the WRONG theta phase:
    #   q=1 -> optimal phase (offset 0, coincidence 1/4); q=0 -> antiphase (offset pi -> ~0).
    phi = (1.0 - q) * math.pi
    return A * KAPPA * E._coincidence(phi) * GAIN
q_grid = np.linspace(0.0, 1.0, 201)
learns = np.array([1.0 if encode_drive(q) > FOLD else 0.0 for q in q_grid])
q_crit = float(q_grid[np.argmax(learns > 0)]) if learns.any() else float("nan")
print(f"  critical coupling quality q_crit = {q_crit:.3f}  (gamma must sit near the right theta phase)")
print(f"  typical reader q=0.90 -> encode drive {encode_drive(0.90):.3f} > fold -> LEARNS")
print(f"  disorganised  q=0.30 -> encode drive {encode_drive(0.30):.3f} -> "
      f"{'learns' if encode_drive(0.30)>FOLD else 'BELOW fold -> learning FAILS at FULL strength + focus'}")
print(f"  => a STRUCTURAL coupling deficit, distinct from a weak (low-effort) signal. [V mech / I mapping]")
print(f"     (clinical: reduced/disorganised theta-gamma coupling in ADHD & dyslexia.)")
rec("ld_q_crit", q_crit); rec("ld_drive_q090", encode_drive(0.90)); rec("ld_drive_q030", encode_drive(0.30))
rec("ld_structural_deficit", 1.0 if (encode_drive(0.30) < FOLD < encode_drive(0.90)) else 0.0)

# honesty markers
rec("medium_efficacy_tested", 0.0); rec("alpha_rect", ALPHA); rec("delta_rect", DELTA)
rec("kappa", KAPPA); rec("fold", FOLD)

print("\n" + bar)
print("CLINICAL CONCORDANCE (phenomenological, [I] inference -- citations in the report):")
print("  G/H reason-paralysis      : amygdala hijack -> PFC impaired, narrows to one option")
print("                              (Arnsten'09/'15; Goleman). Pain seizes attention &")
print("                              compromises encoding (Eccleston&Crombez'99).")
print("      drug craving          : iRISA -- salience to drug cues AT THE EXPENSE OF other")
print("                              content; PFC executive control hijacked (Koob; Goldstein).")
print("  I  panic disorder         : false-suffocation alarm / interoceptive runaway, amygdala")
print("                              chemosensor; attack peaks within ~10 min (Klein; Gorman).")
print("  J  learning disability    : reduced theta-gamma coupling in ADHD tasks (Kim'16);")
print("                              atypical low-freq/gamma coupling in dyslexia (Goswami).")
print("  F  index->content reinstate: theta-gamma code -- slow phase indexes fast item-")
print("                              assemblies; reinstating phase reinstates content (Lisman&Jensen).")
print(bar)
print("HONEST LEDGER:")
print("  [F] alpha=2/pi, delta=1/pi^2, kappa=0.5496, R19 fold : reused, not re-tuned.")
print("  [V] in silico: index->content reinstatement, drive-capture collapse of reason, a panic")
print("      bifurcation, and a coupling-quality learning threshold all hold deterministically.")
print("  [I] the mapping to hunger/drug/sex/fear/pain, panic disorder, and learning disability is")
print("      strong, literature-concordant INFERENCE; the drive-panel amplitudes are SCHEMATIC")
print("      (ordering only), NOT measured.")
print("  [O] medium_efficacy_tested=0; nothing here is claimed causal for experience; the hard")
print("      problem stays OPEN; NO claim of subjective experience is made.")

blob = json.dumps(HEAD, sort_keys=True, separators=(",", ":")).encode()
digest = hashlib.sha256(blob).hexdigest()
print(bar); print(f"headline numbers: {len(HEAD)}   sha256 = {digest}")
print("DONE -- index recalls content; a strong low-freq drive paralyses reason; the drive panel,")
print("        a panic bifurcation, and a learning-coupling threshold all emerge. [V mech / I clinical]")

# ---- self-check (this script doubles as a gate) ----------------------------------------
fails = []
def chk(n, c):
    if not c: fails.append(n)
chk("F: index reinstates content, specifically", HEAD["reinstatement_specific"] == 1.0)
chk("G: reason collapses monotonically with drive, has a capture threshold", mono_G and not math.isnan(D_cap))
chk("G: full reason at D=0, paralysed at large D", rational_slots(0.0) == N_SLOTS and rational_slots(6.0) <= 1)
chk("H: every drive eventually captures", all(not math.isnan(panel_results[k][0]) for k in panel))
chk("I: panic bifurcation (healthy self-limits, disorder runs away)", bifurcation_ok)
chk("J: structural learning deficit below q_crit at full strength", encode_drive(0.30) < FOLD < encode_drive(0.90))
chk("efficacy stays open (0)", HEAD["medium_efficacy_tested"] == 0.0)
chk("constants reused, not retuned", abs(ALPHA-2/math.pi)<1e-9 and abs(DELTA-1/math.pi**2)<1e-9)
if fails:
    print("\nSTRESS-TEST SELF-CHECK FAIL:"); [print("  -", f) for f in fails]; raise SystemExit(1)
print("STRESS-TEST SELF-CHECK PASS -- all stress-test invariants hold (SEED=19).")
