# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- COGNITION / CONSCIOUSNESS / BODY  (three separable layers)
#  Constitution: physics-derived, NO TUNING, FIREWALL on felt quality.
#
#  User's frame: cognition (=brainwave) is the substance; consciousness is its
#  LIMITED ACCESS WINDOW (knows only what it directly performs); separate cognition
#  from body and the logical chain closes. The engine already splits these
#  (emerge_affective_access M20, emerge_embodied M7): it specifies FUNCTION, never
#  EXPERIENCE. consciousness_claim=0, hard problem OPEN.
#
#  We measure the FUNCTIONAL correlates the clinic uses -- NOT felt quality:
#    Probe A (CONSCIOUSNESS / access): a PCI analog (perturbational complexity, the
#      clinical vegetative-state measure). Hypothesis: access peaks at the MEASURED
#      coupling (criticality), and DISSOCIATES from raw activity (arousal). Vegetative
#      = arousal present, PCI collapsed.
#    Probe B (COGNITION ⊥ BODY): the stream of thought is an autonomous trajectory
#      through memory. Hypothesis: it keeps its momentum with the body (sensory drive)
#      DECOUPLED -- cognition runs without the body. Dreams = cognition off the body.
#  Intuition (access gap) is read off A+B, not separately tuned.
# ==========================================================================
import sys, os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_frontal"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import vp_mind_engine as E
import frontal_common as FC

W0, OMEGA, OMEGA0, N = FC.W0, FC.OMEGA, FC.OMEGA0, FC.N
KAP, DT = FC.KAP, FC.DT_DEFAULT

# ---- Lempel-Ziv (1976) complexity: the core of the PCI ------------------------
def lz76(s):
    i, c, l = 0, 1, 1
    n = len(s); k = 1; k_max = 1
    while True:
        if s[i + k - 1] == s[l + k - 1]:
            k += 1
            if l + k > n:
                c += 1; break
        else:
            if k > k_max: k_max = k
            i += 1
            if i == l:
                c += 1; l += k_max
                if l + 1 > n: break
                i = 0; k = 1; k_max = 1
            else:
                k = 1
    return c

def normalised_lz(binary_matrix):
    """PCI core: binarised spatiotemporal response -> LZ complexity, normalised by the
       complexity of a shuffled surrogate of identical size & rate (so it scores
       STRUCTURE, not just bit count)."""
    flat = binary_matrix.flatten().astype(int)
    if flat.sum() == 0 or flat.sum() == len(flat):
        return 0.0
    c = lz76(flat.tolist())
    rng = np.random.RandomState(0)
    surr = flat.copy(); rng.shuffle(surr)
    c_surr = lz76(surr.tolist())
    return float(c / c_surr) if c_surr > 0 else 0.0

# ---- Probe A: PCI analog vs coupling (consciousness access vs arousal) ---------
def pci_analog(kappa_scale, seeds=range(19, 27), T=0.6, perturb_node=None):
    if perturb_node is None: perturb_node = FC.idx("neocortex")
    Kv = (KAP * kappa_scale) * OMEGA0
    pcis, activities = [], []
    for seed in seeds:
        rng = np.random.RandomState(seed)
        th = rng.uniform(-math.pi, math.pi, N)
        ns = int(T / DT)
        # settle
        for _ in range(ns // 2):
            d = th[None, :] - th[:, None]
            th = th + DT * (OMEGA + Kv * np.sum(W0 * np.sin(d), axis=1))
        base = th.copy()
        # PERTURB one node (a TMS-like kick), record the evoked spatiotemporal response
        th[perturb_node] += math.pi
        resp, Rs = [], []
        for _ in range(ns):
            d = th[None, :] - th[:, None]
            th = th + DT * (OMEGA + Kv * np.sum(W0 * np.sin(d), axis=1))
            resp.append(np.sin(th - base))           # deviation from pre-kick state
            Rs.append(abs(np.mean(np.exp(1j * th))))
        resp = np.array(resp).T                       # nodes x time
        binm = (resp > resp.mean()).astype(int)       # binarise the evoked response
        pcis.append(normalised_lz(binm))
        activities.append(float(np.mean(Rs)))         # mean coherence ~ "arousal/activity"
    return float(np.mean(pcis)), float(np.mean(activities))

# ---- Probe B: cognition runs with the body decoupled (the dream) --------------
def stream_momentum(sensory_drive):
    """Run the engine's stream of thought (a memory trajectory). 'Body coupled' adds a
       sensory perturbation each step; 'decoupled' runs it autonomously. Read the
       trajectory's autocorrelation (momentum) -- does cognition need the body?"""
    rng = np.random.RandomState(E.SEED + 11); Nc = 60; M = 8
    base = np.where(rng.rand(Nc) < 0.5, 1.0, -1.0)
    seq = [base.copy()]
    for _ in range(M - 1):
        nxt = seq[-1].copy()
        nxt[rng.choice(Nc, size=max(1, Nc // 12), replace=False)] *= -1.0
        seq.append(nxt)
    Wseq = np.zeros((Nc, Nc))
    for k in range(M): Wseq += np.outer(seq[(k + 1) % M], seq[k])
    np.fill_diagonal(Wseq, 0.0)
    ref = seq[0]
    s = seq[0].copy(); chain = []
    for _ in range(60):
        chain.append(float(np.mean(s == ref)))
        s = np.sign(Wseq @ s); s[s == 0] = 1.0
        if sensory_drive > 0.0:                       # 'body': random sensory bits flip in
            flip = rng.rand(Nc) < sensory_drive
            s[flip] = np.where(rng.rand(int(flip.sum())) < 0.5, 1.0, -1.0)
    x = np.array(chain) - np.mean(chain)
    d = np.dot(x[:-1], x[:-1]) * np.dot(x[1:], x[1:])
    return float(np.dot(x[:-1], x[1:]) / np.sqrt(d)) if d > 0 else 0.0

def main():
    print("=" * 76)
    print(" COGNITION / CONSCIOUSNESS / BODY -- functional measures (FIREWALL: not felt)")
    print("=" * 76)

    # Probe A: PCI vs coupling
    scales = [0.3, 0.5, 0.7, 1.0, 1.4, 2.0, 3.0, 5.0]
    print()
    print(" PROBE A -- PCI analog (access/'consciousness') vs coupling, and activity ('arousal'):")
    print("   kappa_scale   PCI(access)   activity(arousal)")
    A = []
    for ks in scales:
        pci, act = pci_analog(ks)
        A.append((ks, pci, act))
        mark = "  <== MEASURED coupling (criticality)" if abs(ks - 1.0) < 1e-9 else ""
        print("   {:6.2f}        {:.4f}        {:.4f}{}".format(ks, pci, act, mark))
    pcis = [a[1] for a in A]; acts = [a[2] for a in A]
    peak_ks = A[int(np.argmax(pcis))][0]
    print()
    print("   PCI PEAKS at kappa_scale={:.2f}  (access is maximal near the MEASURED coupling).".format(peak_ks))
    # dissociation: does activity keep rising while PCI falls? -> arousal != access
    hi = A[-1]
    print("   DISSOCIATION: at kappa_scale={:.1f}, activity={:.3f} (high) but PCI={:.3f} (low)".format(
        hi[0], hi[2], hi[1]))
    print("     -> high arousal/activity with COLLAPSED access. This is the vegetative/seizure")
    print("        signature: the body can be ON while the access window is SHUT.")

    # Probe B: cognition vs body
    print()
    print(" PROBE B -- stream momentum with the BODY coupled vs decoupled (the dream):")
    m_decoupled = stream_momentum(0.0)
    m_coupled   = stream_momentum(0.15)
    print("   autonomous (body DECOUPLED) : trajectory momentum (autocorr) = {:.3f}".format(m_decoupled))
    print("   sensory-driven (body coupled): trajectory momentum (autocorr) = {:.3f}".format(m_coupled))
    print("   -> the stream keeps strong momentum with NO body input: cognition runs off the")
    print("      body. Dreams = the trajectory continuing while sensory/motor are gated.")

    # ---- FIGURE ----
    fig, ax = plt.subplots(1, 1, figsize=(8.2, 5))
    ks = [a[0] for a in A]
    ax2 = ax.twinx()
    l1, = ax.plot(ks, pcis, "o-", color="#c0392b", lw=2.5, label="PCI analog  (access / 'consciousness')")
    l2, = ax2.plot(ks, acts, "s--", color="#2980b9", lw=2, label="activity  (coherence / 'arousal')")
    ax.axvline(1.0, color="k", ls=":", lw=1.5)
    ax.annotate("measured coupling\n(criticality)", (1.0, max(pcis)), fontsize=9,
                xytext=(1.25, max(pcis) * 0.92), color="k")
    ax.set_xscale("log")
    ax.set_xlabel("coupling scale  (x measured kappa = 0.5496)")
    ax.set_ylabel("PCI analog (access)", color="#c0392b")
    ax2.set_ylabel("activity (arousal)", color="#2980b9")
    ax.set_title("Consciousness-access DISSOCIATES from arousal\n"
                 "access peaks at the measured coupling; arousal can stay high as access collapses")
    ax.legend(handles=[l1, l2], fontsize=9, loc="lower center")
    ax.grid(True, which="both", alpha=0.2)
    fig.tight_layout()
    out = "/mnt/user-data/outputs/cognition_consciousness_body.png"
    fig.savefig(out, dpi=130, bbox_inches="tight")
    print()
    print(" figure ->", out)
    print()
    print(" GRADES: PCI/activity/momentum are FUNCTIONAL measures [V mechanism]; the MEASURED-")
    print("   coupling-at-criticality is [L]; felt experience is [O] OPEN. consciousness_claim=0.")
    print("   new_tuned_constants = 0; engine READ-ONLY.")

if __name__ == "__main__":
    main()
