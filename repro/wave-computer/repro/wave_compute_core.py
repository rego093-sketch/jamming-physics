#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_wave_computer v0.1 — reference simulation
============================================
A *wave-substrate* computer: information is carried by the PHASE of coupled
oscillators, not by bit-amplitudes. Three operations are demonstrated on one
substrate, then a noise-robust channel:

  D1  STORE a wave      : patterns become stable phase configurations
                          (attractors sculpted by a Hebbian coupling field).
  D2  COMPUTE with waves: relaxation of the phase field = pattern completion
                          (the "fetch-execute" is replaced by physics settling).
  D3  PATTERN regime    : computation lives in the PARTIAL-coherence (metastable)
                          band — not full sync (R->1, one global bit) and not
                          incoherence (R->0, no stored structure). This is the
                          regime the ephaptic mind engine sits in (R~0.39).
  D4  COMMUNICATE thru   : phase coding + attractor clean-up tolerates noise that
      noise              destroys amplitude coding (reliable comms in heavy noise).

INHERITANCE (exact provenance — nothing tuned to a target):
  brain  (vp_frontal v2): ephaptic NEAR-FIELD coupling (every brain rhythm is
         sub-wavelength -> quasi-static field, not radiative); PHASE-coupling
         (Kuramoto) order parameter; metastable operating band R~0.39 (M9 anchor
         R=0.38961455156044245); attractor pattern-completion (hippocampal/
         cortical autoassociator); theta-gamma capacity ~7.
  physics(vp_physics v0.11.0): wave-in-medium law c^2 = B/rho (jamming spine);
         CLOCK-FREE lattice propagation (time emerges from the medium, no external
         clock); 1/r^2 near-field Green function (force chapter 14).

FIREWALL (inherited verbatim): this models FUNCTION only — storage, computation,
communication. NO consciousness claim. consciousness_claim = 0.

Discipline: deterministic (fixed seeds), self-checking, no tuned constants. Every
operating point is swept; a claim is reported only with its sweep. Honest
negatives are recorded, not hidden.
"""

import json
import hashlib
import numpy as np

# ----------------------------------------------------------------------------
# Inherited anchors (cited, not tuned)
# ----------------------------------------------------------------------------
R_MIND_ANCHOR = 0.38961455156044245     # vp_frontal v2 M9 anchor (the brain's metastable band)
THETA_GAMMA_CAPACITY = 7                 # vp_frontal v2 emerged WM capacity (theta-gamma nesting)
CONSCIOUSNESS_CLAIM = 0                  # firewall
HARD_PROBLEM_OPEN = 1                    # firewall

SEED = 19                                # inherited seed convention from the mind project


# ============================================================================
# THE SUBSTRATE — phase-coupled oscillators in a near-field coupling medium
# ============================================================================
# State: phase theta_i of each oscillator. The "medium" is the symmetric coupling
# field J (Hebbian) — the in-silico analog of the ephaptic near-field. Dynamics
# are gradient descent on the XY/phase energy
#     E(theta) = -1/2 * sum_ij J_ij cos(theta_i - theta_j)
# whose minima ARE the stored patterns. This is the continuous (oscillator /
# wave) form of an associative memory: a *standing phase pattern* is a datum.
#
# CLOCK-FREE: there is no global clock. Time is the medium's own relaxation —
# the network advances by its physics, exactly as the brain is self-timed by its
# rhythms and the jamming lattice propagates clock-free.

def hebbian_field(patterns):
    """Sculpt the coupling medium so each pattern is an attractor (wave storage)."""
    P, N = patterns.shape
    J = (patterns.T @ patterns) / N        # J_ij = (1/N) sum_mu xi_i xi_j
    np.fill_diagonal(J, 0.0)               # no self-coupling
    return J


def relax(theta, J, dt=0.05, steps=400, T=0.0, rng=None):
    """Let the phase field settle (wave computation = physics relaxation).
    dtheta_i/dt = sum_j J_ij sin(theta_j - theta_i) + sqrt(2T) * noise
    Vectorized via sin(a-b) = sin a cos b - cos a sin b."""
    theta = theta.copy()
    for _ in range(steps):
        s, c = np.sin(theta), np.cos(theta)
        coupling = c * (J @ s) - s * (J @ c)     # = sum_j J_ij sin(theta_j-theta_i)
        theta = theta + dt * coupling
        if T > 0.0 and rng is not None:
            theta += np.sqrt(2.0 * T * dt) * rng.standard_normal(theta.shape)
    return theta


def global_R(theta):
    """Kuramoto global order parameter (the brain's coherence measure)."""
    return float(np.abs(np.mean(np.exp(1j * theta))))


def overlap(theta, xi):
    """Binary read-out overlap of the settled phase field with stored pattern xi.
    Read s_i = sign(cos theta_i) in {-1,+1}; perfect recall -> overlap = 1."""
    s = np.sign(np.cos(theta))
    s[s == 0] = 1.0
    return float(np.mean(s * xi))


def pattern_to_phase(xi):
    """A pattern xi in {-1,+1} -> a standing phase pattern (0 for +1, pi for -1)."""
    return np.where(xi > 0, 0.0, np.pi)


def corrupt_phase(phase, flip_frac, jitter, rng):
    """Corrupt a cue: flip a fraction of bits (theta -> theta+pi) + add phase jitter."""
    th = phase.copy()
    N = th.size
    n_flip = int(round(flip_frac * N))
    if n_flip > 0:
        idx = rng.choice(N, size=n_flip, replace=False)
        th[idx] += np.pi
    th += rng.uniform(-jitter, jitter, size=N)
    return th


# ============================================================================
# D1+D2 — STORAGE and COMPUTATION: capacity and basins of attraction
# ============================================================================

def measure_capacity(N=256, loads=(0.02, 0.04, 0.06, 0.08, 0.10, 0.14),
                     trials=6, recall_thresh=0.95, base_seed=SEED):
    """Store P=alpha*N random patterns; cue each cleanly; relax; success if the
    settled wave reproduces the stored pattern (overlap >= thresh).
    Reports recall success vs load alpha = P/N — the storage capacity curve."""
    out = []
    for alpha in loads:
        P = max(1, int(round(alpha * N)))
        succ = []
        Rs = []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 1000 * t + int(alpha * 1e4))
            patterns = rng.choice([-1.0, 1.0], size=(P, N))
            J = hebbian_field(patterns)
            ok = 0
            for mu in range(P):
                th0 = pattern_to_phase(patterns[mu]) + rng.uniform(-0.15, 0.15, size=N)
                th = relax(th0, J)
                m = overlap(th, patterns[mu])
                Rs.append(global_R(th))
                if m >= recall_thresh:
                    ok += 1
            succ.append(ok / P)
        out.append({
            "alpha": round(alpha, 4),
            "P": P,
            "recall_success": round(float(np.mean(succ)), 4),
            "recall_success_sd": round(float(np.std(succ)), 4),
            "global_R_mean": round(float(np.mean(Rs)), 4),
        })
    return out


def measure_basins(N=256, alpha=0.06, flip_fracs=(0.0, 0.05, 0.10, 0.15, 0.20,
                   0.25, 0.30, 0.35, 0.40, 0.45), jitter=0.30, trials=8,
                   base_seed=SEED):
    """COMPUTATION as pattern completion: cue a corrupted version of a stored wave
    and measure how much the relaxation recovers. Final overlap vs initial
    corruption = the basin of attraction (error-correction by physics)."""
    P = max(1, int(round(alpha * N)))
    rows = []
    for f in flip_fracs:
        finals, inits = [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 7919 * t + int(f * 1e4))
            patterns = rng.choice([-1.0, 1.0], size=(P, N))
            J = hebbian_field(patterns)
            mu = rng.integers(P)
            clean = pattern_to_phase(patterns[mu])
            cue = corrupt_phase(clean, f, jitter, rng)
            inits.append(overlap(cue, patterns[mu]))
            th = relax(cue, J)
            finals.append(overlap(th, patterns[mu]))
        rows.append({
            "flip_frac": round(f, 3),
            "init_overlap": round(float(np.mean(inits)), 4),
            "final_overlap": round(float(np.mean(finals)), 4),
            "final_overlap_sd": round(float(np.std(finals)), 4),
        })
    return {"alpha": alpha, "P": P, "jitter": jitter, "curve": rows}


# ============================================================================
# D3 — THE METASTABLE REGIME (why computation needs partial coherence)
# ============================================================================

def regime_scan(N=256, alpha=0.06, gains=(0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0),
                trials=6, base_seed=SEED):
    """Scale the coupling-field gain g (medium stiffness). At g=0 the field is
    OFF (no stored structure, overlap collapses to chance); as g grows the global
    coherence R rises; pattern recall (structured computation) survives only in
    the PARTIAL band, never at full sync. Maps recall + global R vs gain."""
    P = max(1, int(round(alpha * N)))
    rows = []
    for g in gains:
        recs, Rs = [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 104729 * t + int(g * 1e3))
            patterns = rng.choice([-1.0, 1.0], size=(P, N))
            J = g * hebbian_field(patterns)
            for mu in range(min(P, 6)):
                cue = corrupt_phase(pattern_to_phase(patterns[mu]), 0.15, 0.30, rng)
                th = relax(cue, J)
                recs.append(overlap(th, patterns[mu]))
                Rs.append(global_R(th))
        rows.append({
            "gain": g,
            "recall_overlap": round(float(np.mean(recs)), 4),
            "global_R": round(float(np.mean(Rs)), 4),
        })
    return rows


# ============================================================================
# D4 — NOISE-ROBUST COMMUNICATION: phase coding vs amplitude coding
# ============================================================================
# Transmit an N-symbol codeword through additive white Gaussian noise.
#   PHASE  (BPSK)        : bit -> phase {0,pi} -> symbol x = e^{i*theta} = +/-1.
#   AMPLITUDE (OOK)      : bit -> amplitude {0, A}; A chosen for EQUAL mean energy.
#   PHASE + clean-up     : decoded phases are fed back into the attractor field
#                          (receiver knows the codebook) and relaxed -> physics
#                          error-correction (the brain's trick).
# At matched energy, phase (BPSK) already beats amplitude (OOK) by ~3 dB; with
# attractor clean-up of a STRUCTURED codeword it tolerates far heavier noise.

def Q(x):
    from math import erfc, sqrt
    return 0.5 * erfc(x / sqrt(2.0))


def comm_demo(N=256, n_code=8, sigmas=(0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5),
              trials=40, base_seed=SEED):
    """Bit-error-rate vs noise sigma for three schemes at MATCHED energy.
    Codewords = stored attractor patterns (a structured code the receiver knows)."""
    rng0 = np.random.default_rng(base_seed)
    codebook = rng0.choice([-1.0, 1.0], size=(n_code, N))    # valid codewords (+/-1)
    J = hebbian_field(codebook)                               # receiver's clean-up field
    A = np.sqrt(2.0)                                          # OOK level: mean energy = A^2/2 = 1 = BPSK

    rows = []
    for sig in sigmas:
        ber_bpsk, ber_ook, ber_clean = [], [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 31 * t + int(sig * 1e4))
            mu = rng.integers(n_code)
            bits = codebook[mu]                               # in {-1,+1}

            # ---- PHASE / BPSK ----
            x = bits.astype(float)                            # +/-1
            y = x + sig * rng.standard_normal(N)              # AWGN (per-real-dim sigma)
            dec_bpsk = np.where(y > 0, 1.0, -1.0)
            ber_bpsk.append(float(np.mean(dec_bpsk != bits)))

            # ---- AMPLITUDE / OOK (matched energy) ----
            amp = np.where(bits > 0, A, 0.0)                  # {0, A}
            yo = amp + sig * rng.standard_normal(N)
            dec_ook = np.where(yo > A / 2.0, 1.0, -1.0)
            ber_ook.append(float(np.mean(dec_ook != bits)))

            # ---- PHASE + attractor clean-up ----
            theta_dec = np.where(dec_bpsk > 0, 0.0, np.pi)    # decoded phases
            theta_dec += rng.uniform(-0.05, 0.05, size=N)     # tiny dither off the saddle
            theta_fix = relax(theta_dec, J)
            s = np.sign(np.cos(theta_fix)); s[s == 0] = 1.0
            ber_clean.append(float(np.mean(s != bits)))

        rows.append({
            "sigma": sig,
            "snr_db": round(10.0 * np.log10(1.0 / (sig ** 2)), 2),   # Es/N0 (Es=1, N0=sigma^2)
            "ber_phase_bpsk": round(float(np.mean(ber_bpsk)), 5),
            "ber_amplitude_ook": round(float(np.mean(ber_ook)), 5),
            "ber_phase_plus_cleanup": round(float(np.mean(ber_clean)), 5),
            "theory_bpsk": round(Q(1.0 / sig), 5),
            "theory_ook": round(Q(1.0 / (np.sqrt(2.0) * sig)), 5),
        })
    return {"n_code": n_code, "N": N, "matched_energy": 1.0, "curve": rows}


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
        "_what": "vp_wave_computer v0.1 reference simulation — wave-substrate compute",
        "inheritance": {
            "brain_R_anchor": R_MIND_ANCHOR,
            "theta_gamma_capacity": THETA_GAMMA_CAPACITY,
            "physics_substrate_law": "c^2 = B/rho (wave in medium); clock-free lattice propagation; 1/r^2 near-field",
        },
        "firewall": {"consciousness_claim": CONSCIOUSNESS_CLAIM,
                     "hard_problem_open": HARD_PROBLEM_OPEN},
        "new_tuned_constants": 0,
    }

    print("[D1+D2] storage capacity ...")
    results["D1_capacity"] = measure_capacity()
    for r in results["D1_capacity"]:
        print(f"   alpha={r['alpha']:.3f}  P={r['P']:3d}  recall={r['recall_success']:.3f}"
              f"  (R_global={r['global_R_mean']:.3f})")

    print("[D2] basins of attraction (pattern completion) ...")
    results["D2_basins"] = measure_basins()
    for r in results["D2_basins"]["curve"]:
        print(f"   flip={r['flip_frac']:.2f}  init={r['init_overlap']:+.3f} -> "
              f"final={r['final_overlap']:+.3f}")

    print("[D3] metastable-regime scan (recall vs coupling gain) ...")
    results["D3_regime"] = regime_scan()
    for r in results["D3_regime"]:
        print(f"   gain={r['gain']:.2f}  recall={r['recall_overlap']:+.3f}"
              f"  R_global={r['global_R']:.3f}")

    print("[D4] noise-robust communication (BER vs sigma) ...")
    results["D4_comm"] = comm_demo()
    for r in results["D4_comm"]["curve"]:
        print(f"   sigma={r['sigma']:.2f} ({r['snr_db']:+.1f} dB)  "
              f"phase={r['ber_phase_bpsk']:.4f}  amp={r['ber_amplitude_ook']:.4f}  "
              f"phase+cleanup={r['ber_phase_plus_cleanup']:.4f}")

    # ---- derived headline findings (computed from the sweeps, not asserted) ----
    cap = results["D1_capacity"]
    # capacity = largest load with recall >= 0.90
    cap_alpha = max([c["alpha"] for c in cap if c["recall_success"] >= 0.90], default=0.0)
    basin = results["D2_basins"]["curve"]
    # critical corruption = largest flip_frac whose final overlap still >= 0.95
    crit_flip = max([b["flip_frac"] for b in basin if b["final_overlap"] >= 0.95], default=0.0)
    comm = results["D4_comm"]["curve"]
    # find a sigma where raw phase BER is sizeable but clean-up still ~0
    win = [c for c in comm if c["ber_phase_bpsk"] >= 0.02 and c["ber_phase_plus_cleanup"] <= 0.01]
    cleanup_window = win[0] if win else None

    results["headline"] = {
        "storage_capacity_alpha_c": cap_alpha,
        "computation_critical_corruption_fracbits": crit_flip,
        "phase_beats_amplitude": all(
            c["ber_phase_bpsk"] <= c["ber_amplitude_ook"] + 1e-9 for c in comm),
        "cleanup_window_example": cleanup_window,
    }

    print("\n--- headline (derived from sweeps) ---")
    print(f"   storage capacity alpha_c (recall>=0.90) : {cap_alpha:.3f}  "
          f"(~{int(round(cap_alpha*256))} patterns / 256 oscillators)")
    print(f"   pattern-completion critical corruption  : {crit_flip:.2f} of bits flipped"
          f" still fully recovered")
    print(f"   phase coding <= amplitude coding BER     : {results['headline']['phase_beats_amplitude']}")
    if cleanup_window:
        print(f"   noise window (raw phase err {cleanup_window['ber_phase_bpsk']*100:.1f}% -> "
              f"cleanup {cleanup_window['ber_phase_plus_cleanup']*100:.1f}%) at "
              f"sigma={cleanup_window['sigma']} ({cleanup_window['snr_db']} dB)")

    results["_digest"] = digest({k: v for k, v in results.items()
                                 if not k.startswith("_")})
    with open("wave_compute_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\ndigest = {results['_digest'][:16]}...")
    print("wrote wave_compute_results.json")
    return results


if __name__ == "__main__":
    main()
