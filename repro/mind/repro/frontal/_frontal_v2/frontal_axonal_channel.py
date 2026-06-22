# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- THE AXONAL COUPLING CHANNEL (the second physical channel)
#  Constitution: physical only, NO TUNING, public cited values grounded, data decides.
#  STATUS: hypothesis-forming. Do NOT confirm; sweep and try to break.
#
#  The frozen kernel W0 is EPHAPTIC (proximity/field): W0[cortex,thalamus]=4e-4,
#  W0[cortex,hypothalamus]=2e-5 -- essentially zero, because they are not spatial
#  neighbours. But leucotomy severed an AXONAL WHITE-MATTER TRACT. Ephaptic != axonal.
#  This adds the missing axonal channel, grounded in PUBLISHED human/primate anatomy.
#
#  GROUNDED RELATIVE STRENGTHS (the [L] inputs; absolute gain is [O], swept):
#    cortex<->thalamus(MD) : HEAVY, RECIPROCAL  -> A=1.0
#        Klein 2010 NeuroImage 51:555 (DWI-DT human/macaque MD-PFC topography);
#        Vanderhaeghen/Jneurosci 43:7780 2023 (MD massively & reciprocally connected
#        to all PFC; 39 area-specific MD-PFC tracts/hemisphere). THE leucotomy tract.
#    cortex->hypothalamus  : SPARSE, DIFFUSE     -> A=0.15  [magnitude O]
#        Ongur, An & Price 1998 J Comp Neurol 401:480 (PFC->hypothalamus arises from
#        medial PFC network); Radley 2006 J Neurosci 26:12967 (mPFC->peri-PVH diffuse,
#        sparse within PVN proper; net inhibitory HPA control).
#
#  The frozen W0 stays READ-ONLY. The experiment runs on W0 + kappa_axon*A (a NEW,
#  separately provenanced physical substrate -- NOT the frozen M9 kernel). The
#  leucotomy lesion REVERTS the cortex<->thalamus edge to ephaptic-only (severs the
#  axon, keeps the field). The lesion effect must be SIGN-STABLE across the kappa
#  sweep to be believed (the F1 discipline). new_tuned_constants = 0.
# ==========================================================================
import sys, os, math
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_frontal"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import frontal_common as FC                       # FROZEN engine + grounded read-outs

W0, OMEGA, OMEGA0, N = FC.W0, FC.OMEGA, FC.OMEGA0, FC.N
DT = FC.DT_DEFAULT
CX, TH, HY = FC.idx("neocortex"), FC.idx("thalamus"), FC.idx("hypothalamus")

# ---- the grounded axonal connectome (relative strengths cited above) ----------
def axonal_connectome():
    A = np.zeros((N, N))
    A[CX, TH] = A[TH, CX] = 1.00      # heavy reciprocal MD-PFC tract   [L ordering]
    A[CX, HY] = A[HY, CX] = 0.15      # sparse mPFC<->hypothalamus       [L sparse; O magnitude]
    return A
A = axonal_connectome()

def W_total(kappa_axon, sever_axon=None):
    """Two physical channels: frozen ephaptic W0 + axonal kappa_axon*A.
       sever_axon=(i,j) reverts that edge to ephaptic-only (the faithful leucotomy:
       cut the white-matter tract, leave the field coupling)."""
    W = W0 + kappa_axon * A
    if sever_axon is not None:
        i, j = sever_axon
        W[i, j] = W0[i, j]; W[j, i] = W0[j, i]
    return W

def _order(th): return float(abs(np.mean(np.exp(1j * th))))

def _focal_K(i, b0=0.7):
    bv = np.zeros(N); bv[i] = abs(b0)
    return np.array([FC.k_bias(x) for x in bv]) * OMEGA0

# ---- PHYSICAL read-outs (no 'emotion' label) ---------------------------------
def cortico_thalamic_transmission(W, seeds, T=1.0):
    """Drive the cortex; measure the phase-locking value (PLV) between cortex and
       thalamus over the second half. This IS the physical frontal->thalamic
       transmission the leucotomy severs. High = thalamus tracks cortex."""
    vals = []
    K = _focal_K(CX)
    for seed in seeds:
        rng = np.random.RandomState(seed)
        th = rng.uniform(-math.pi, math.pi, N)
        ns = int(T / DT); dphi = []
        for s in range(ns):
            d = th[None, :] - th[:, None]
            th = th + DT * (OMEGA + K * np.sum(W * np.sin(d), axis=1))
            if s > ns // 2: dphi.append(th[CX] - th[TH])
        vals.append(float(abs(np.mean(np.exp(1j * np.array(dphi))))))
    return float(np.mean(vals))

def perception(W, seeds, T=1.0):
    """Immediate stimulus response: order parameter R while a SENSORY cue is driven
       (cue nodes, NOT cortex). The function leucotomy patients RETAIN."""
    vals = []
    for c in FC.CUE_NODES:
        Kc = _focal_K(FC.idx(c))
        for seed in seeds:
            rng = np.random.RandomState(seed)
            th = rng.uniform(-math.pi, math.pi, N)
            ns = int(T / DT); Rs = np.empty(ns)
            for s in range(ns):
                d = th[None, :] - th[:, None]
                th = th + DT * (OMEGA + Kc * np.sum(W * np.sin(d), axis=1))
                Rs[s] = _order(th)
            vals.append(float(np.mean(Rs[ns // 2:])))
    return float(np.mean(vals))

# ---- EXPERIMENT: leucotomy (sever cortex<->thalamus axon) across a kappa sweep --
def run(seeds=range(19, 25), kappas=(0.05, 0.1, 0.2, 0.5, 1.0)):
    rows = []
    for k in kappas:
        Wi = W_total(k)                          # intact: both channels
        Wl = W_total(k, sever_axon=(CX, TH))     # leucotomy: axon severed
        t_i = cortico_thalamic_transmission(Wi, seeds)
        t_l = cortico_thalamic_transmission(Wl, seeds)
        p_i = perception(Wi, seeds)
        p_l = perception(Wl, seeds)
        rows.append(dict(kappa=k,
                         transmission_intact=t_i, transmission_lesion=t_l,
                         d_transmission=t_l - t_i,
                         perception_intact=p_i, perception_lesion=p_l,
                         d_perception=p_l - p_i))
    return rows

def main():
    print("=" * 76)
    print(" vp_frontal v2 -- FAITHFUL LEUCOTOMY on the AXONAL channel (hypothesis-forming)")
    print(" two physical channels: frozen ephaptic W0 + grounded axonal kappa*A")
    print(" lesion = sever cortex<->thalamus AXON (keep field). NO TUNING. do NOT confirm.")
    print("=" * 76)
    rows = run()
    print()
    print(" kappa | cortico-thalamic transmission    | perception (sensory cue)")
    print("       |  intact   lesion    Δ            |  intact   lesion    Δ")
    for r in rows:
        print("  {:.2f} |  {:.4f}  {:.4f}  {:+.4f}      |  {:.4f}  {:.4f}  {:+.4f}".format(
            r["kappa"], r["transmission_intact"], r["transmission_lesion"], r["d_transmission"],
            r["perception_intact"], r["perception_lesion"], r["d_perception"]))

    dT = [r["d_transmission"] for r in rows]
    dP = [r["d_perception"] for r in rows]
    trans_all_neg = all(d < -1e-3 for d in dT)
    perc_all_spared = all(abs(d) < 0.03 for d in dP)
    print()
    print("-" * 76)
    print(" SIGN-STABILITY across the kappa sweep (the F1 anti-tuning test):")
    print("   transmission deficit negative at EVERY kappa : {}  (range {:+.4f}..{:+.4f})".format(
        trans_all_neg, min(dT), max(dT)))
    print("   perception spared at EVERY kappa             : {}  (range {:+.4f}..{:+.4f})".format(
        perc_all_spared, min(dP), max(dP)))
    print()
    if trans_all_neg and perc_all_spared:
        print(" => CANDIDATE DISSOCIATION (sign-stable on this substrate): severing the frontal")
        print("    axonal tract removes cortico-thalamic transmission while sparing perception.")
        print("    This is a HYPOTHESIS, not a confirmation. It is owed: (1) the absolute axonal")
        print("    gain is [O] (only the ORDERING thal>>hypo is grounded); (2) a cohort/seed test;")
        print("    (3) a duration sweep; (4) the read-out is a 12-node phase model, not behaviour.")
        print("    GRADE: [L candidate], frontal-transmission-specific. consciousness_claim=0.")
    else:
        print(" => NO sign-stable dissociation. Reported as an honest negative; do not claim it.")
    print()
    print(" FIREWALL: transmission/perception are phase quantities of a coupling model, NOT a")
    print("   felt state. 'frontal->emotion' is NOT asserted -- only a physical channel and what")
    print("   severing it does. Interpretation stays OPEN. new_tuned_constants=0; W0 unchanged.")

if __name__ == "__main__":
    main()
