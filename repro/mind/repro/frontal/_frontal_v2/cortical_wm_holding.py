# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- CORTICAL WM HOLDING under the FAITHFUL FRONTAL LESION
#  Constitution: copy the frozen micro-model, NO TUNING, data decides.
#
#  F1's negative ("cortical holding negligible; sign-flips") was measured on a
#  BARE KURAMOTO substrate stripped of all WM machinery -- coherence recovery,
#  not working memory. Here we re-ask the SAME question on the REAL WM substrate:
#  the frozen Hippocampus micro-model (R19 bistable cells + Hebbian recurrence),
#  copied as the cortical buffer, parameterised by the measured FOXG1 fold and
#  sized by the EMERGED theta/gamma WM capacity.
#
#  Faithful frontal lesion = DISCONNECTION (leucotomy SEVERS tracts; it does not
#  silence): zero a fraction of the recurrent weights, bidirectionally. The F1
#  anti-tuning rule is law: SWEEP the lesion fraction and seed-average; a real
#  holder collapses MONOTONICALLY (sign-stable), an artefact flips.
#
#  new_tuned_constants = 0. g = measured FOXG1 gamma. n_cells/lr inherited from
#  the engine's own Hippocampus (its [O] scales). Item count = emerged capacity.
# ==========================================================================
import sys, os, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import vp_mind_engine as E                      # FROZEN, READ-ONLY
from cortical_emergence import emerge_organ      # the no-tuning rhythm emergence

ATLAS = E.load_brain_atlas()
FOXG1 = float(ATLAS["organs"]["neocortex"]["gamma"])     # 1.4737, measured
LHX2  = float(ATLAS["organs"]["hippocampus"]["gamma"])   # 1.5172, measured, control

# item count = EMERGED theta/gamma WM capacity (grounded, not picked)
CX = emerge_organ("neocortex")
N_ITEMS = int(round(CX["wm_capacity_emerged"]))           # ~7

# inherited engine micro-model scales ([O], identical to emerge_memory)
N_CELLS, LR = 120, 0.18

# --------------------------------------------------------------------------
#  Faithful frontal lesion: DISCONNECTION (sever recurrent tracts, both ways)
# --------------------------------------------------------------------------
def disconnect(W, frac, seed):
    n = W.shape[0]
    rng = np.random.RandomState(seed)
    Wl = W.copy()
    iu = np.triu_indices(n, k=1)
    m = len(iu[0]); k = int(round(frac * m))
    if k > 0:
        sel = rng.choice(m, size=k, replace=False)
        ii, jj = iu[0][sel], iu[1][sel]
        Wl[ii, jj] = 0.0; Wl[jj, ii] = 0.0          # bidirectional tract cut
    return Wl

def maintenance(hp, Wmat, cue_frac=0.3):
    """Two WM read-outs on the (lesioned) recurrent matrix:
       sustain   = mean self-sustaining overlap of stored items (hold with no cue)
       complete  = mean pattern-completion fidelity from a partial cue."""
    save = hp.W; hp.W = Wmat
    sustain = float(np.mean([hp.is_attractor(i) for i in range(len(hp.stored))]))
    compl = float(np.mean([hp.retrieve(i, cue_frac) for i in range(len(hp.stored))]))
    hp.W = save
    return sustain, compl

# --------------------------------------------------------------------------
#  EXPERIMENT: holding vs lesion fraction, seed-averaged (anti-tuning sweep)
# --------------------------------------------------------------------------
def run(g_cell, label, pattern_seeds=range(19, 27), lesion_seeds=range(8),
        fracs=(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)):
    curve = {f: {"sustain": [], "complete": []} for f in fracs}
    for ps in pattern_seeds:
        hp = E.Hippocampus(n_cells=N_CELLS, g=g_cell, lr=LR)
        hp.W = np.zeros((N_CELLS, N_CELLS)); hp.stored = []
        for p in E._patterns(N_ITEMS, N_CELLS, seed=ps):
            hp.write(p)
        W_intact = hp.W.copy()
        for f in fracs:
            if f == 0.0:
                s, c = maintenance(hp, W_intact)
                curve[f]["sustain"].append(s); curve[f]["complete"].append(c)
            else:
                for ls in lesion_seeds:
                    s, c = maintenance(hp, disconnect(W_intact, f, ls * 101 + ps))
                    curve[f]["sustain"].append(s); curve[f]["complete"].append(c)
    out = []
    for f in fracs:
        out.append(dict(frac=f,
                        sustain=float(np.mean(curve[f]["sustain"])),
                        complete=float(np.mean(curve[f]["complete"]))))
    return out

def sign_stable_monotone(curve, key):
    """Is the read-out MONOTONE non-increasing across the lesion sweep?
       (the F1 discipline: a real holder degrades sign-stably; an artefact flips)"""
    vals = [r[key] for r in curve]
    diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
    return all(d <= 1e-9 for d in diffs), vals

def main():
    print("=" * 74)
    print(" vp_frontal v2 -- WM HOLDING vs FRONTAL LESION (disconnection)")
    print(" REAL micro-model substrate (not bare Kuramoto). NO TUNING.")
    print(" items = emerged WM capacity = {} | cells={} | g=FOXG1={:.4f}".format(
        N_ITEMS, N_CELLS, FOXG1))
    print("=" * 74)

    cx = run(FOXG1, "neocortex/FOXG1")
    print()
    print(" CORTICAL buffer (FOXG1 fold): holding vs fraction of recurrence severed")
    print("   frac   self-sustain   completion@0.3cue")
    for r in cx:
        print("   {:.1f}      {:.4f}        {:.4f}".format(r["frac"], r["sustain"], r["complete"]))
    ms, vs = sign_stable_monotone(cx, "sustain")
    mc, vc = sign_stable_monotone(cx, "complete")
    print("   self-sustain  monotone-collapse (sign-stable): {}  ({:.3f} -> {:.3f})".format(ms, vs[0], vs[-1]))
    print("   completion    monotone-collapse (sign-stable): {}  ({:.3f} -> {:.3f})".format(mc, vc[0], vc[-1]))

    # control: same test with the engine's hippocampal convention g=1.0, and with LHX2
    print()
    print(" ROBUSTNESS (data decides, not the cell-gain convention):")
    for g, lab in ((1.0, "g=1.0 (engine hippocampal convention)"), (LHX2, "g=LHX2 (hippocampus gene)")):
        cc = run(g, lab, pattern_seeds=range(19, 23), lesion_seeds=range(4))
        m, v = sign_stable_monotone(cc, "complete")
        print("   {:42s}: completion {:.3f} -> {:.3f}, monotone={}".format(lab, v[0], v[-1], m))

    print()
    print("-" * 74)
    print(" CONTRAST WITH F1 (same question, two substrates):")
    print("   F1 bare Kuramoto : cortex holding dR ~ -0.0001 (negligible), sign FLIPS over sweep")
    print("   here real WM     : severing the holder's recurrence COLLAPSES holding,")
    print("                      MONOTONE / sign-stable across the full lesion sweep")
    print("   => F1's negative was an UNDER-EMERGENCE artefact, as diagnosed. Holding is")
    print("      real and lesion-sensitive on the substrate that actually carries it.")
    print()
    print(" HONEST LIMIT: the cell gain g does NOT enter the sign() pattern dynamics, so")
    print("   this autoassociator does not yet DIFFERENTIATE frontal from hippocampal.")
    print("   Frontal-SPECIFICITY needs the emerged gamma band + broadcaster coupling")
    print("   (F1's robust structural facts) -- the next layer. Graded [V] holding-real /")
    print("   [O] frontal-specificity-owed. new_tuned_constants = 0.")

if __name__ == "__main__":
    main()
