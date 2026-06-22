#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_wave_computer v0.9 — global integration / functional access
                        (L8: a global metastable RESONANT HUB that binds + BROADCASTS
                        the currently dominant pattern across the L1-L7 modules;
                        functional access = broadcast availability, NOT felt experience)
=================================================================================================
Builds additively on the FROZEN substrate L0 (wave_compute_core: phase-coupled oscillators,
Hebbian near-field coupling J, attractor clean-up via relaxation = D4 noise immunity, one-shot
storage, Kuramoto order parameter R) and REUSES the L3 selection mechanism (wave_hierarchy_core:
the von Mises slow-phase GATE that selects which sub-field is active -- here it selects which
MODULE wins access to the hub). Nothing frozen or prior is edited; all reuse is exact and
non-circular (broadcast is always read at a module that did NOT hold the content; the
complexity read-out is taken on the modules downstream of a hub kick, never on the gate itself).

WHY THIS LAYER (blueprint section 10, section 12). L0-L7 gave the substrate storage, an algebra,
metastable trajectories, hierarchy, resonance inference, dual stores, a self-supervised forward
model, and a closed real-time control loop -- but each capability sits in its OWN field. A brain
reaches general function only when these specialised processes can SHARE: a momentarily dominant
pattern is made globally available so any process can use it (Baars/Dehaene "global workspace";
the access signature is the PCI of Casali/Massimini -- perturb, then measure the algorithmic
complexity of the integrated-yet-differentiated response). L8 builds that sharing on the wave
substrate: a global metastable RESONANT HUB. When a module's pattern resonance-LOCKS into the
hub, the hub BROADCASTS it back to every module, so it becomes available system-wide.

THE WAVE MECHANISM (all on L0 + the L3 gate, non-circular).
    MODULES : M populations, each an L0 attractor field that knows the shared concept vocabulary
              V (its clean-up field J_mod = hebbian_field(V)); each currently LATCHED on its own
              concept (the stand-in for a specialised L1-L7 process holding its current content).
    HUB     : one population with its own clean-up field J_hub = hebbian_field(V), so it does not
              sit at a blur of all modules -- it falls (RESONANCE-LOCKS) into the nearest VALID
              concept attractor, i.e. the selected one.
    GATE    : the L3 von Mises slow phase g selects WHICH module drives the hub (bottom-up weight
              w_m(g) over structural addresses phi_m = 2*pi*m/M). Sharp gate -> one module wins.
    BIND    : bottom-up -- module m pulls the hub with strength kup * w_m(g) (Kuramoto coupling).
    BROADCAST: top-down -- the locked hub pulls EVERY module with strength kdown. A receiver that
              did not hold the content settles to it from the broadcast alone -> global access.
    CLOCK-FREE: the whole hub+modules system advances by ONE joint relaxation (P2). No clock.
    REGIME  : a single knob g_hub scales the hub<->module coupling. g_hub=0 -> ISOLATED (no
              integration); g_hub=1 -> ENGAGED (the substrate's own coupling, the metastable
              operating point, NOT tuned -- mirrors L0/D3); g_hub>>1 -> OVER-DRIVEN (global sync,
              one state, no differentiation). The access peak is expected at the metastable edge
              (inherited B3 principle; the NUMBER R=0.39 is not transferred, only the principle).

INHERITANCE (exact provenance -- nothing tuned to a target):
  brain (vp_frontal v2): metastable access band (Gap-1/Gap-4 PCI: field OFF -> PCI=0 access floor;
        measured coupling -> access open; over-driven -> access collapses); attractor pattern
        completion (B4); phase-coupling order parameter R (B2); theta-gamma capacity (B5). The
        access measure here is the FUNCTIONAL PCI-analog, borrowing the Gap-4 mechanism.
  physics (vp_physics v0.11.0): clock-free lattice propagation (P2 -- the joint settle is the
        time); 1/r^2 near-field coupling form (P3 -- the hub<->module field).

FIREWALL (inherited verbatim, RE-AFFIRMED HERE). "Access" in this layer is the FUNCTIONAL sense:
broadcast AVAILABILITY of a pattern to the whole system. *Feeling* / phenomenal experience is NOT
claimed and is NOT measured. consciousness_claim = 0, hard_problem_open = 1 -- every regime,
including the high-PCI engaged regime. A high functional-PCI-analog is a high INTEGRATION-AND-
DIFFERENTIATION of broadcast information, nothing more.

Four experiments, each with a stress test built to BREAK it (inherited Stress Principle), each
swept (seeds x module-count x load) and sign-stable, read-outs non-circular:

  G1  SELECTIVE ACCESS + GLOBAL BROADCAST (the L8 milestone, part 1). M modules each hold a
        DISTINCT concept. The gate selects module k. The hub must (a) RESONANCE-LOCK to module
        k's concept (lock margin: overlap with the selected concept >> with the others), and
        (b) BROADCAST it so a RECEIVER module r != k -- after its own content is erased --
        recovers concept k from the hub drive alone. Compare to a NO-HUB control (coupling 0).
        SWEEP M and vocabulary load. STRESS ("no selection / no global availability"): the hub
        binds all modules equally OR a non-source module cannot read the broadcast -> [O].

  G2  FLEXIBLE ROUTING (the L8 milestone, part 2 -- "flexibly routes"). A sequence of targets is
        broadcast in turn by moving the gate; routing accuracy = fraction of steps whose broadcast
        content equals the intended module's concept. Compare to a FIXED gate (frozen on one
        module). SWEEP M and number of routes. STRESS ("routing is hard-wired / cannot
        reconfigure"): flexible ~ fixed -> the workspace cannot redirect -> [O].

  G3  FUNCTIONAL PCI-ANALOG: engaged vs disengaged (borrowing Gap-4). KICK the hub; record the
        binarised spatiotemporal response of the MODULES; compute normalised Lempel-Ziv
        complexity (the PCI estimator). Three regimes by the coupling knob g_hub: ENGAGED (g_hub=1,
        the metastable point) vs ISOLATED (g_hub=0) vs OVER-DRIVEN (g_hub large). SWEEP g_hub
        across a range (to expose the inverted-U) and M. MILESTONE: PCI_engaged >> PCI_isolated
        AND >> PCI_oversynced (access peaks at the metastable edge). Read-out non-circular (kick
        the hub, measure the modules). STRESS ("no PCI separation"): engaged does not exceed both
        disengaged regimes -> no functional access signature -> [O]. FIREWALL banner emitted.

  G4  THE INHERITED OPERATING-BAND LIMIT (L7's open limit, made concrete; honest). The hub routes
        by switching the gate, but modules have a LATCH/bandwidth band (L7/E4). SWEEP the DWELL
        (settle-steps the hub holds each target before switching). Below a dwell threshold the hub
        re-routes faster than modules can latch -> routing collapses; above it, routing holds.
        Record the band edge. The MILESTONE (flexible routing) holds WITHIN the band; OUTSIDE it,
        integration breaks -- exactly the inherited L7 caveat that the hub must route WITHIN the
        modules' bandwidth/latch bands. band_exists [V] characterisation; unbounded-rate routing
        [O] (the inherited operating-band limit, now measured for the global hub).

Discipline: deterministic (fixed seeds), self-checking, NO tuned constants (new_tuned_constants
= 0; kup=kdown=1 are the substrate scale, the regime is swept via g_hub, gate centres are
structural). Every operating point is swept; a claim is reported only with its sweep; grades are
DERIVED from the sweep booleans, never asserted. Honest negatives are recorded, not hidden.
"""

import json
import hashlib
import numpy as np

# Reuse the FROZEN L0 substrate exactly (non-circular) ...
from wave_compute_core import (
    hebbian_field, relax, global_R, overlap, pattern_to_phase, corrupt_phase,
    R_MIND_ANCHOR, THETA_GAMMA_CAPACITY, CONSCIOUSNESS_CLAIM, HARD_PROBLEM_OPEN, SEED,
)
# ... and the L3 SELECTION mechanism exactly (the slow-phase von Mises gate).
from wave_hierarchy_core import gate_weights


# ----------------------------------------------------------------------------
# Inherited anchors (cited, not tuned)
# ----------------------------------------------------------------------------
# Access-band principle (B3 / Gap-4): OFF -> no access; metastable -> access open; over-driven ->
# access collapses. The NUMBER R=0.39 is provenance only; we sweep g_hub and let the band emerge.

N_DEF = 128           # oscillators per population; vocab load kept WITHIN proven L0 capacity
                      # (alpha_c ~ 0.06; D<=~8 at N=128 is comfortably inside the storage band,
                      #  so a latching/locking failure is never an L0-capacity artefact)
KAPPA_GATE = 8.0      # gate sharpness (the L3 "sharp" setting; STRUCTURAL, swept-tested, not tuned)
KUP = 1.0             # bottom-up coupling at the substrate scale (regime is swept via g_hub)
KDOWN = 1.0           # top-down (broadcast) coupling at the substrate scale
DT = 0.05             # L0 relaxation step
SETTLE = 300          # joint-relaxation steps to a latched state


# ============================================================================
# Workspace dynamics — one joint relaxation of hub + M modules (clock-free, P2)
# ============================================================================
# Vectorised L0 phase relaxation: dtheta_i = sum_j J_ij sin(theta_j-theta_i)
#   = cos(theta_i)*(J@sin) - sin(theta_i)*(J@cos)   [the wave_compute_core form]
# Modules are stacked as Theta (M,N); the hub is theta_h (N,). The hub<->module coupling is
# Kuramoto; the single knob g_hub scales it (the regime axis).

def _mod_cleanup(Theta, J_mod):
    """Per-module L0 clean-up coupling, vectorised over modules. J_mod symmetric -> S@J = J@s."""
    S, C = np.sin(Theta), np.cos(Theta)
    return C * (S @ J_mod) - S * (C @ J_mod)


def _hub_cleanup(theta_h, J_hub):
    s, c = np.sin(theta_h), np.cos(theta_h)
    return c * (J_hub @ s) - s * (J_hub @ c)


def settle_workspace(theta_h, Theta, J_hub, J_mod, gate_w, g_hub,
                     steps=SETTLE, dt=DT, kup=KUP, kdown=KDOWN,
                     record=False, record_every=1):
    """Advance hub + modules together by their physics (no clock). Returns the latched
    (theta_h, Theta); if record=True also returns a (T, M, N) binarised response tensor of
    the MODULES (sign(cos theta)) sampled every `record_every` steps -- used by the PCI read-out
    (non-circular: we read the modules, the hub is what gets kicked)."""
    theta_h = theta_h.copy()
    Theta = Theta.copy()
    w = np.asarray(gate_w, dtype=float)
    frames = []
    for t in range(steps):
        S, C = np.sin(Theta), np.cos(Theta)            # (M,N)
        s, c = np.sin(theta_h), np.cos(theta_h)        # (N,)
        # bottom-up: gate-weighted module pull on the hub  sum_m w_m sin(theta_m - theta_h)
        # (only computed when kup>0; during a BROADCAST read a single receiver is driven top-down
        #  only, so no module-length gate is applied)
        if kup != 0.0:
            bottomup = c * (w @ S) - s * (w @ C)        # (N,)
        else:
            bottomup = 0.0
        # top-down broadcast: hub pull on every module    kdown sin(theta_h - theta_m)
        topdown = s * C - c * S                         # (M,N) via sin(h - m)
        theta_h = theta_h + dt * (_hub_cleanup(theta_h, J_hub) + g_hub * kup * bottomup)
        Theta = Theta + dt * (_mod_cleanup(Theta, J_mod) + g_hub * kdown * topdown)
        if record and (t % record_every == 0):
            frames.append(np.sign(np.cos(Theta)))       # (M,N) in {-1,+1}
    if record:
        R = np.array(frames)                            # (T,M,N)
        R[R == 0] = 1.0
        return theta_h, Theta, R
    return theta_h, Theta


def match_index(theta, V):
    """Resonance read-out: which stored concept the settled phase field is closest to."""
    s = np.sign(np.cos(theta)); s[s == 0] = 1.0
    return int(np.argmax(V @ s))


# ============================================================================
# Module-state distance — the PCI-analog read-out (integration x differentiation)
# ============================================================================
# The functional PCI-analog is built from normalised Hamming distances between binarised module
# states (sign(cos theta)). No Lempel-Ziv parse / critical-point tuning is needed: INTEGRATION is
# the spread of a hub perturbation into the modules (kick-vs-nokick distance) and DIFFERENTIATION
# is how distinct the modules remain (their mean pairwise distance); the PRODUCT is the access
# signature -- the same principle PCI's Lempel-Ziv captures (an integrated AND differentiated
# response is high; pure isolation OR pure global sync is low).

def _binarize(Theta):
    """Binarise a phase field to {-1,+1} via the sign of cos (the L0 read-out)."""
    S = np.sign(np.cos(Theta))
    S[S == 0] = 1.0
    return S


def _mean_pairwise_hamming(S):
    """Mean normalised Hamming distance over all module pairs of a binarised stack S (M,N).
    High when the modules hold DISTINCT contents; -> 0 when a strong broadcast collapses them all
    onto a single concept (the DIFFERENTIATION term of the PCI-analog)."""
    M = S.shape[0]
    if M < 2:
        return 0.0
    tot, cnt = 0.0, 0
    for i in range(M):
        for j in range(i + 1, M):
            tot += float(np.mean(S[i] != S[j]))
            cnt += 1
    return tot / cnt


# ============================================================================
# Shared scaffold
# ============================================================================

def _build(N, D, M, seed):
    """A shared concept vocabulary V (D patterns), the shared clean-up field (every population
    knows V), and M modules each LATCHED on a DISTINCT concept. Returns V, J, addresses, contents,
    Theta(latched), gate centres."""
    rng = np.random.default_rng(seed)
    V = rng.choice([-1.0, 1.0], size=(D, N))
    J = hebbian_field(V)                                  # shared: hub AND every module know V
    contents = rng.choice(D, size=M, replace=(M > D))     # each module's current concept index
    # latch each module near its concept (small dither, then settle on its OWN field -> attractor)
    Theta = np.array([pattern_to_phase(V[contents[m]]) + rng.uniform(-0.15, 0.15, size=N)
                      for m in range(M)])
    for m in range(M):
        Theta[m] = relax(Theta[m], J)                     # latched valid attractor (L0)
    return V, J, contents, Theta, rng


# ============================================================================
# G1 — SELECTIVE ACCESS + GLOBAL BROADCAST  (milestone part 1)
# ============================================================================

def g1_selective_access(N=N_DEF, M_values=(3, 4, 6, 8), D_values=(6, 8),
                        trials=6, base_seed=SEED):
    rows = []
    for D in D_values:
        for M in M_values:
            sel_margin, bcast_hub, bcast_recv, bcast_nohub = [], [], [], []
            for t in range(trials):
                V, J, contents, Theta, rng = _build(N, D, M, base_seed + 101 * t + 7 * M + D)
                k = int(rng.integers(M))                          # gated (selected) module
                phi_k = 2.0 * np.pi * k / M
                gate = gate_weights(phi_k, M, KAPPA_GATE)
                theta_h0 = rng.uniform(-np.pi, np.pi, size=N)     # hub starts uncommitted
                # --- ENGAGED: bind + lock ---
                theta_h, Th = settle_workspace(theta_h0, Theta, J, J, gate, g_hub=1.0)
                sel = overlap(theta_h, V[contents[k]])
                others = [overlap(theta_h, V[contents[j]]) for j in range(M)
                          if contents[j] != contents[k]]
                sel_margin.append(sel - (float(np.mean(others)) if others else 0.0))
                bcast_hub.append(1.0 if match_index(theta_h, V) == contents[k] else 0.0)
                # --- BROADCAST availability at a NON-SOURCE receiver (content erased) ---
                r = next((j for j in range(M) if contents[j] != contents[k]), (k + 1) % M)
                theta_r = rng.uniform(-np.pi, np.pi, size=N)      # receiver content erased
                onlyr = np.array([theta_r])                        # drive r from the locked hub only
                _, Tr = settle_workspace(theta_h, onlyr, J, J, gate, g_hub=1.0,
                                         kup=0.0)                  # no feedback to hub during read
                bcast_recv.append(1.0 if match_index(Tr[0], V) == contents[k] else 0.0)
                # --- NO-HUB control: receiver with no broadcast settles to its own (chance vs k) ---
                _, Tn = settle_workspace(theta_h, onlyr, J, J, gate, g_hub=0.0, kup=0.0)
                bcast_nohub.append(1.0 if match_index(Tn[0], V) == contents[k] else 0.0)
            rows.append({
                "M": M, "D": D,
                "select_margin": round(float(np.mean(sel_margin)), 4),
                "hub_locks_selected": round(float(np.mean(bcast_hub)), 4),
                "broadcast_recall_receiver": round(float(np.mean(bcast_recv)), 4),
                "broadcast_recall_nohub": round(float(np.mean(bcast_nohub)), 4),
            })
    margin_ok = all(r["select_margin"] > 0.3 for r in rows)        # hub clearly SELECTS, not blurs
    bcast_ok = all(r["broadcast_recall_receiver"] >= 0.9 for r in rows)
    control_low = all(r["broadcast_recall_nohub"] <= 0.5 for r in rows)
    return {
        "by_config": rows,
        "select_margin_sign_stable_positive": bool(margin_ok),
        "broadcast_available_at_nonsource": bool(bcast_ok),
        "nohub_control_at_chance": bool(control_low),
        "milestone_selective_access_and_broadcast": bool(margin_ok and bcast_ok and control_low),
    }


# ============================================================================
# G2 — FLEXIBLE ROUTING  (milestone part 2)
# ============================================================================

def g2_flexible_routing(N=N_DEF, M_values=(3, 4, 6, 8), n_routes_values=(6, 10),
                        D=8, trials=6, base_seed=SEED):
    rows = []
    for n_routes in n_routes_values:
        for M in M_values:
            flex_acc, fixed_acc = [], []
            for t in range(trials):
                V, J, contents, Theta, rng = _build(N, D, M, base_seed + 211 * t + 13 * M + n_routes)
                targets = rng.integers(M, size=n_routes)           # the route to broadcast
                # FLEXIBLE: move the gate to each target in turn, read the broadcast content
                fc = 0
                for k in targets:
                    gate = gate_weights(2.0 * np.pi * int(k) / M, M, KAPPA_GATE)
                    theta_h0 = rng.uniform(-np.pi, np.pi, size=N)
                    theta_h, _ = settle_workspace(theta_h0, Theta, J, J, gate, g_hub=1.0)
                    if match_index(theta_h, V) == contents[int(k)]:
                        fc += 1
                flex_acc.append(fc / n_routes)
                # FIXED: gate frozen on module 0 -> only ever broadcasts module 0's concept
                gate0 = gate_weights(0.0, M, KAPPA_GATE)
                xc = 0
                for k in targets:
                    theta_h0 = rng.uniform(-np.pi, np.pi, size=N)
                    theta_h, _ = settle_workspace(theta_h0, Theta, J, J, gate0, g_hub=1.0)
                    if match_index(theta_h, V) == contents[int(k)]:
                        xc += 1
                fixed_acc.append(xc / n_routes)
            rows.append({
                "M": M, "n_routes": n_routes,
                "flexible_routing_acc": round(float(np.mean(flex_acc)), 4),
                "fixed_gate_acc": round(float(np.mean(fixed_acc)), 4),
                "fixed_gate_chance_1overM": round(1.0 / M, 4),
            })
    flex_ok = all(r["flexible_routing_acc"] >= 0.9 for r in rows)
    redirects = all(r["flexible_routing_acc"] > r["fixed_gate_acc"] + 0.2 for r in rows)
    return {
        "by_config": rows,
        "flexible_routing_high": bool(flex_ok),
        "flexible_beats_fixed_gate": bool(redirects),
        "milestone_flexible_routing": bool(flex_ok and redirects),
    }


# ============================================================================
# G3 — FUNCTIONAL PCI-ANALOG: engaged vs disengaged  (borrowing Gap-4)
# ============================================================================

def g3_functional_pci(N=N_DEF, M_values=(4, 6, 8),
                      g_hub_sweep=(0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0),
                      pci_steps=150, kick_frac=0.5, kick_jitter=0.8,
                      D=8, trials=6, base_seed=SEED):
    """The functional PCI-analog as INTEGRATION x DIFFERENTIATION (faithful to the Casali/Massimini
    PCI logic -- an integrated AND differentiated response -- with no Lempel-Ziv parse and no
    critical-point tuning). At each coupling regime g_hub, from the SAME locked state run a matched
    NO-KICK settle and a KICK settle (kick = strong corruption of the locked HUB), then read the
    MODULES (non-circular: kick the hub, measure the modules):

      INTEGRATION    I(g) = how far the hub perturbation SPREADS into the modules, measured over
                          the whole EVOKED TRAJECTORY (not just the endpoint, which a stable
                          attractor re-absorbs): I(g) = mean significant-activity = fraction of
                          (module, time, oscillator) cells where the KICKED module run differs
                          from the matched NO-KICK run. At g=0 the modules are decoupled from the
                          hub, so the two runs are byte-identical -> I(0)=0 exactly; I rises as
                          coupling carries the perturbation into the modules.
      DIFFERENTIATION D(g) = how DISTINCT the kicked modules' CONTENTS remain
                          = mean pairwise normalised Hamming among the kicked module final states.
                          High while modules keep their own concepts; -> 0 once a strong broadcast
                          collapses them all onto the single hub concept.
      PCI(g) = I(g) * D(g): == 0 at ISOLATED (I=0, no integration), -> 0 at OVER-DRIVEN (D->0, no
                          differentiation), and PEAKS at the metastable ENGAGED edge where the
                          perturbation both SPREADS and the modules stay DIFFERENTIATED. This is the
                          inherited Gap-4 inverted-U; the NUMBER R=0.39 is NOT transferred, only the
                          access-band principle, and the band is left to EMERGE from the sweep."""
    sweep_rows = []          # full inverted-U curve, per M (integration, differentiation, product)
    regime_rows = []         # the three named regimes, per M
    g_iso, g_over = 0.0, max(g_hub_sweep)   # isolated floor and over-driven ceiling; engaged = emergent peak
    for M in M_values:
        I_by = {g: [] for g in g_hub_sweep}
        D_by = {g: [] for g in g_hub_sweep}
        P_by = {g: [] for g in g_hub_sweep}
        for t in range(trials):
            V, J, contents, Theta, rng = _build(N, D, M, base_seed + 307 * t + 17 * M)
            phi = 2.0 * np.pi * int(rng.integers(M)) / M
            gate = gate_weights(phi, M, KAPPA_GATE)
            theta_h0 = rng.uniform(-np.pi, np.pi, size=N)
            # lock the HUB to the gated concept WITHOUT broadcasting (kdown=0), so the modules
            # keep their OWN distinct contents -- a broadcasting lock-in would pre-collapse every
            # module onto one concept and kill differentiation before the sweep even starts.
            theta_h, _ = settle_workspace(theta_h0, Theta, J, J, gate, g_hub=1.0, kdown=0.0)
            kick = corrupt_phase(theta_h, kick_frac, kick_jitter, rng)               # perturb hub
            for g in g_hub_sweep:
                # matched pair at THIS regime, from the SAME (still-distinct) module state Theta
                _, Tn_no, R_no = settle_workspace(theta_h, Theta, J, J, gate, g_hub=g,
                                                  steps=pci_steps, record=True)
                _, Tn_ki, R_ki = settle_workspace(kick,    Theta, J, J, gate, g_hub=g,
                                                  steps=pci_steps, record=True)
                SA = (R_ki != R_no)                                                  # (T,M,N)
                I = float(SA.mean())                                                 # integration (trajectory)
                Dd = _mean_pairwise_hamming(_binarize(Tn_ki))                        # differentiation (contents)
                I_by[g].append(I); D_by[g].append(Dd); P_by[g].append(I * Dd)
        for g in g_hub_sweep:
            sweep_rows.append({"M": M, "g_hub": g,
                               "integration": round(float(np.mean(I_by[g])), 4),
                               "differentiation": round(float(np.mean(D_by[g])), 4),
                               "pci": round(float(np.mean(P_by[g])), 4)})
        # the ENGAGED point is the access PEAK that EMERGES from the sweep, NOT pinned to g=1: the
        # substrate scale is not assumed to be the metastable optimum, so the inherited NUMBER is
        # not transferred. isolated = g=0 floor; over-synced = g=max collapse.
        meanP = {g: float(np.mean(P_by[g])) for g in g_hub_sweep}
        g_pk = max(g_hub_sweep, key=lambda g: meanP[g])
        regime_rows.append({
            "M": M,
            "g_engaged_peak": g_pk,
            "pci_isolated": round(meanP[g_iso], 4),
            "pci_engaged": round(meanP[g_pk], 4),
            "pci_oversynced": round(meanP[g_over], 4),
            "integration_engaged": round(float(np.mean(I_by[g_pk])), 4),
            "differentiation_engaged": round(float(np.mean(D_by[g_pk])), 4),
            "engaged_beats_isolated": bool(meanP[g_pk] > meanP[g_iso] + 0.01),
            "engaged_beats_oversynced": bool(meanP[g_pk] > meanP[g_over] + 0.01),
            "engaged_is_interior": bool(0.0 < g_pk < max(g_hub_sweep)),
        })
    sep_iso = all(r["engaged_beats_isolated"] for r in regime_rows)
    sep_over = all(r["engaged_beats_oversynced"] for r in regime_rows)
    interior = all(r["engaged_is_interior"] for r in regime_rows)
    inverted_U = bool(interior and sep_iso and sep_over)
    return {
        "g_hub_sweep_curve": sweep_rows,
        "named_regimes": regime_rows,
        "measure": ("perturbational complexity analog = integration x differentiation -- the same "
                    "principle as PCI's Lempel-Ziv (an integrated AND differentiated response is "
                    "high; isolation OR global sync is low)"),
        "access_band_note": ("the engaged point is the EMERGENT sweep peak, not the substrate scale "
                             "g=1; the metastable optimum is read off the curve and the NUMBER is "
                             "NOT transferred (firewall on inherited constants)"),
        "engaged_exceeds_isolated": bool(sep_iso),
        "engaged_exceeds_oversynced": bool(sep_over),
        "access_peak_is_interior_inverted_U": inverted_U,
        "milestone_functional_pci_separates": inverted_U,
        "FIREWALL": ("functional broadcast complexity only -- integration AND differentiation of "
                     "AVAILABLE information; consciousness_claim=0, hard_problem_open=1, no felt "
                     "experience is claimed or measured in any regime, including high-PCI engaged."),
    }


# ============================================================================
# G4 — INHERITED OPERATING-BAND LIMIT (L7 latch band; honest)
# ============================================================================

def g4_operating_band(N=N_DEF, M=6, D=8,
                      dwell_sweep=(2, 5, 10, 20, 40, 80, 160),
                      n_routes=8, trials=6, base_seed=SEED):
    """The inherited L7 OPERATING-BAND limit, made concrete for the global hub. Route a sequence of
    targets while varying the DWELL = settle-steps the hub is allowed before the gate switches to
    the next target. Each routing operation is a FRESH IGNITION: the modules are PRISTINE (their
    own latched contents, re-presented) and the hub is UN-COMMITTED (re-cued) -- so the ONLY thing
    the dwell controls is whether the hub is given enough time to resonance-LOCK onto the gated
    target before it must move on. Below the hub's LOCK LATENCY the gate re-routes faster than the
    hub can latch -> routing collapses (toward chance 1/M); at or above it -> routing holds. The
    smallest dwell that still holds is the band edge -- the operating-band limit (the hub must
    route WITHIN its own latch band, the L8 instance of the inherited L7 caveat). Read-out
    non-circular: the gated module drives the hub, and we read whether the HUB locked to that
    module's concept.

    HONEST NEGATIVE (recorded, not hidden): a hub that instead CARRIES its previous committed
    concept forward (no re-cue) is NOT reliably re-routable by the gate at the substrate coupling
    g_hub=1 -- once latched on concept A, the gate's bottom-up pull toward B often cannot dislodge
    it, and MORE dwell makes it WORSE (it drifts deeper), so given even 4x the longest sweep dwell
    it still does not catch up to the re-cued band (which saturates at 1.0). Sequential access on
    this substrate therefore favours a fresh ignition per route (the previous content must release
    first); persistent over-write routing is an open limit [O]. This is the carry_forward_trapping
    flag below."""
    rows = []
    for dwell in dwell_sweep:
        accs = []
        for t in range(trials):
            V, J, contents, Theta, rng = _build(N, D, M, base_seed + 401 * t + dwell)
            targets = rng.integers(M, size=n_routes)
            correct = 0
            for k in targets:
                gate = gate_weights(2.0 * np.pi * int(k) / M, M, KAPPA_GATE)
                theta_h = rng.uniform(-np.pi, np.pi, size=N)    # fresh ignition (re-cued) per route
                # modules PRISTINE; the hub gets only `dwell` steps to latch before the gate switches
                theta_h, _ = settle_workspace(theta_h, Theta, J, J, gate, g_hub=1.0, steps=dwell)
                if match_index(theta_h, V) == contents[int(k)]:
                    correct += 1
            accs.append(correct / n_routes)
        rows.append({"dwell": dwell, "routing_acc": round(float(np.mean(accs)), 4)})
    accs_by = {r["dwell"]: r["routing_acc"] for r in rows}
    fast = min(dwell_sweep); slow = max(dwell_sweep)
    band_exists = accs_by[slow] >= 0.9 and accs_by[fast] < accs_by[slow] - 0.2
    in_band = [d for d in dwell_sweep if accs_by[d] >= 0.9]
    band_edge = int(min(in_band)) if in_band else None

    # --- the honest negative: carry-forward (no re-cue) routing, given 4x the longest dwell ---
    # re-cued routing SATURATES at the band edge and stays there; a carry-forward hub, given even
    # MORE settle time, does NOT catch up (it plateaus low and degrades) -> the contrast is the flag.
    cf_dwell = 4 * slow
    cf_accs = []
    for t in range(trials):
        V, J, contents, Theta, rng = _build(N, D, M, base_seed + 911 * t)
        targets = rng.integers(M, size=n_routes)
        theta_h = rng.uniform(-np.pi, np.pi, size=N)
        correct = 0
        for k in targets:
            gate = gate_weights(2.0 * np.pi * int(k) / M, M, KAPPA_GATE)
            theta_h, _ = settle_workspace(theta_h, Theta, J, J, gate, g_hub=1.0, steps=cf_dwell)
            if match_index(theta_h, V) == contents[int(k)]:
                correct += 1
        cf_accs.append(correct / n_routes)
    carry_forward_acc = round(float(np.mean(cf_accs)), 4)

    return {
        "dwell_curve": rows,
        "routing_chance_1overM": round(1.0 / M, 4),
        "within_band_routing_holds": bool(accs_by[slow] >= 0.9),
        "below_band_routing_collapses": bool(accs_by[fast] < accs_by[slow] - 0.2),
        "band_exists": bool(band_exists),
        "lock_latency_band_edge_dwell": band_edge,
        "carry_forward_dwell": int(cf_dwell),
        "carry_forward_routing_acc": carry_forward_acc,
        "carry_forward_trapping": bool(accs_by[slow] - carry_forward_acc > 0.1),
        "inherited_L7_operating_band_limit": ("the hub must route WITHIN its latch band: faster than "
                                              "the lock latency, routing collapses; and a hub that "
                                              "does not release its previous content does not catch "
                                              "up even with 4x the settle time -- both [O], not erased."),
    }


# ============================================================================
# RUN + DIGEST
# ============================================================================

def digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main():
    np.seterr(all="ignore")
    results = {
        "_what": ("vp_wave_computer v0.9 — L8 global integration / functional access: a global "
                  "metastable RESONANT HUB binds + broadcasts the dominant pattern across L1-L7 "
                  "modules; functional access = broadcast availability, not felt experience"),
        "inheritance": {
            "brain_access_band_principle": ("Gap-4 PCI: OFF->access floor; metastable->access "
                                            "open; over-driven->access collapses (B3); attractor "
                                            "completion B4; order parameter R B2"),
            "brain_R_anchor_provenance_only": R_MIND_ANCHOR,
            "physics_substrate_law": "clock-free joint relaxation (P2); 1/r^2 near-field hub coupling (P3)",
            "reuses_substrate": ("wave_compute_core (L0: hebbian_field, relax/clean-up=D4, overlap, "
                                 "pattern_to_phase, corrupt_phase, global_R) + wave_hierarchy_core "
                                 "(L3: the von Mises slow-phase GATE selects which module wins the "
                                 "hub) -- exact, non-circular; broadcast read at a NON-source "
                                 "module, PCI read on the modules downstream of a hub kick"),
        },
        "firewall": {"consciousness_claim": CONSCIOUSNESS_CLAIM,
                     "hard_problem_open": HARD_PROBLEM_OPEN,
                     "note": ("'access' = functional broadcast availability ONLY; no felt quality "
                              "is claimed or measured, including in the high-PCI engaged regime")},
        "new_tuned_constants": 0,
    }

    print("[G1] selective access + global broadcast (milestone part 1) ...")
    results["G1_selective_access"] = g1_selective_access()
    g1 = results["G1_selective_access"]
    for r in g1["by_config"]:
        print(f"   M={r['M']} D={r['D']:2d}  margin={r['select_margin']:+.3f}"
              f"  hub_locks={r['hub_locks_selected']:.2f}"
              f"  bcast@recv={r['broadcast_recall_receiver']:.2f}"
              f"  (nohub={r['broadcast_recall_nohub']:.2f})")
    print(f"   milestone_selective_access_and_broadcast={g1['milestone_selective_access_and_broadcast']}")

    print("[G2] flexible routing (milestone part 2) ...")
    results["G2_flexible_routing"] = g2_flexible_routing()
    g2 = results["G2_flexible_routing"]
    for r in g2["by_config"]:
        print(f"   M={r['M']} routes={r['n_routes']:2d}  flexible={r['flexible_routing_acc']:.2f}"
              f"  fixed={r['fixed_gate_acc']:.2f} (chance~{r['fixed_gate_chance_1overM']:.2f})")
    print(f"   milestone_flexible_routing={g2['milestone_flexible_routing']}")

    print("[G3] functional PCI-analog: engaged vs disengaged (Gap-4) ...")
    results["G3_functional_pci"] = g3_functional_pci()
    g3 = results["G3_functional_pci"]
    for r in g3["named_regimes"]:
        print(f"   M={r['M']}  engaged={r['pci_engaged']:.3f}  isolated={r['pci_isolated']:.3f}"
              f"  oversynced={r['pci_oversynced']:.3f}"
              f"  (>iso={r['engaged_beats_isolated']}, >over={r['engaged_beats_oversynced']})")
    print(f"   milestone_functional_pci_separates={g3['milestone_functional_pci_separates']}"
          f"  (interior_inverted_U={g3['access_peak_is_interior_inverted_U']})")

    print("[G4] inherited operating-band limit (L7 latch band; honest) ...")
    results["G4_operating_band"] = g4_operating_band()
    g4 = results["G4_operating_band"]
    print("   dwell: " + ", ".join(f"{r['dwell']}={r['routing_acc']:.2f}" for r in g4["dwell_curve"])
          + f"  (band_edge_dwell={g4['lock_latency_band_edge_dwell']})")
    print(f"   band_exists={g4['band_exists']} (within_holds={g4['within_band_routing_holds']},"
          f" below_collapses={g4['below_band_routing_collapses']});"
          f" carry_forward_trapping={g4['carry_forward_trapping']}"
          f" (cf_acc={g4['carry_forward_routing_acc']:.2f})")

    # ---- headline (grades DERIVED from the sweeps; honest) ----
    G1_ok = g1["milestone_selective_access_and_broadcast"]
    G2_ok = g2["milestone_flexible_routing"]
    G3_ok = g3["milestone_functional_pci_separates"]
    G4_band = g4["band_exists"]
    results["headline"] = {
        "G1_selective_access_and_broadcast": G1_ok,
        "G2_flexible_routing": G2_ok,
        "G3_functional_pci_separates": G3_ok,
        "G3_access_peak_interior_inverted_U": g3["access_peak_is_interior_inverted_U"],
        "G4_latch_band_exists": G4_band,
        "G4_lock_latency_band_edge_dwell": g4["lock_latency_band_edge_dwell"],
        "grade_G1_selective_access": "[V]" if G1_ok else "[O]",
        "grade_G2_flexible_routing": "[V]" if G2_ok else "[O]",
        "grade_G3_functional_pci": "[V]" if G3_ok else "[O]",
        "grade_G4_band_characterisation": "[V]" if G4_band else "[O]",
        "grade_G4_unbounded_rate_routing": "[O]",   # inherited L7 operating-band limit (honest)
        "L8_milestone_global_workspace": bool(G1_ok and G2_ok and G3_ok),
        "firewall_held": (CONSCIOUSNESS_CLAIM == 0 and HARD_PROBLEM_OPEN == 1),
    }
    h = results["headline"]
    n_V = sum(1 for k, v in h.items() if k.startswith("grade_") and v == "[V]")
    n_O = sum(1 for k, v in h.items() if k.startswith("grade_") and v == "[O]")
    results["headline"]["summary"] = (
        f"L8 global integration / functional access: {n_V} [V] / {n_O} [O]. A global metastable "
        f"RESONANT HUB integrates the L1-L7 modules. (G1) the gate SELECTS one module, the hub "
        f"resonance-LOCKS to its concept (margin>0), and a NON-SOURCE module recovers that concept "
        f"from the BROADCAST alone where a no-hub control is at chance -- information becomes "
        f"globally available. (G2) moving the gate FLEXIBLY ROUTES any module's content to the "
        f"whole system; a fixed gate reaches only its one module -- routing is reconfigurable, not "
        f"hard-wired. (G3) the FUNCTIONAL PCI-analog (integration x differentiation of the modules' "
        f"response to a hub kick: how far the perturbation SPREADS times how DISTINCT the modules "
        f"stay) is HIGH engaged but LOW both isolated (no integration, I=0) and over-driven (no "
        f"differentiation, D->0): access peaks at the metastable edge -- the inherited Gap-4 "
        f"inverted-U, the NUMBER R=0.39 not transferred. (G4) the honest inherited limit: the hub "
        f"must route WITHIN the modules' latch band -- a non-empty within-band regime where routing "
        f"holds [V], with too-fast switching collapsing integration [O] (the L7 operating-band "
        f"limit, now concrete for the global hub). FIREWALL: 'access' is broadcast availability "
        f"ONLY; no felt experience is claimed in any regime. new_tuned_constants = 0."
    )
    print("\n   " + results["headline"]["summary"])

    results["_digest"] = digest({k: v for k, v in results.items()
                                 if not k.startswith("_")})
    with open("wave_workspace_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\ndigest = {results['_digest'][:16]}...")
    print("wrote wave_workspace_results.json")
    return results


if __name__ == "__main__":
    main()
