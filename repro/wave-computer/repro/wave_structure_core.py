#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_wave_computer v0.3 — structured representation (L1 complete) + time (L2 start)
================================================================================
Builds additively on the FROZEN substrate L0 (wave_compute_core: phase-coupled
oscillators, Hebbian near-field coupling) and the L1 binding/bundle proven in v0.2
(wave_resonance_core). This session closes the L1 representation algebra and opens
the L2 time/sequence layer.

  L1a  PERMUTE closes the algebra (bind . bundle . permute):
        a sequence is bundled with a per-position PERMUTATION tag
        S = sum_l rho^l(a_l) ; item at position l recovered by rho^{-l} + cleanup.
        This is the third VSA operation (phase rotation / coordinate permutation)
        that turns a *set* (bundle) into an *ordered structure*.

  L1b  ROLE-VALUE TREE depth-capacity (the L1 milestone + its stress test):
        a depth-d, branching-b tree of role->value pairs is encoded in ONE
        composite wave (bind + bundle + permute-protect per level). A query walks a
        path of role keys and recovers the leaf. SWEEP DEPTH -> the *useful depth*
        d* (max depth with accuracy >= 0.95). STRESS: crosstalk collapses
        structured recovery before any useful depth (d* < 2 => only flat records,
        L3 hierarchy required).

  L2a  METASTABLE TRAJECTORY (sequence learn -> replay -> predict):
        ASYMMETRIC (time-delayed) Hebbian coupling on the L0 substrate makes the
        phase field TRAVERSE a learned cycle of attractors (heteroclinic chaining,
        Sompolinsky-Kanter/Kleinfeld form), kept in pure phase-coupling form so it
        reuses L0 exactly. SWEEP lambda -> the band where ordered replay holds.
        STRESS: too weak => stuck at a fixed point; too strong => diverges/scrambles
        (no band => metastable chaining fails). Also: predict-next from a partial cue.

  L2b  THETA-GAMMA WORKING MEMORY (reproduce B5's small finite capacity):
        items occupy distinct gamma phase-slots of one slow theta carrier
        (slot k = permutation rho^k -- L1a reused). Finite gamma phase precision
        (substrate jitter) caps the number of resolvable slots => a SMALL WM
        capacity. SWEEP jitter x n_slot -> the capacity emerges; the brain's
        number ~7 (FOXG1 gamma) is NOT transferred -- only the principle.

DISCIPLINE (inherited, every session):
  * Reuses the EXACT L0 substrate (wave_compute_core) -- non-circular.
  * new_tuned_constants = 0. No coupling/model value is fit to a target.
    (Read-out thresholds and structural choices -- delay length, slot count -- are
    SWEPT or fixed structurally, never fit to hit a number; inherited anchors are
    principles, never targets. The brain numbers R=0.39 and WM~7 are NOT transferred.)
  * Every claim with a sweep; sign-stable across seeds; non-circular read-outs.
  * Deterministic (fixed seeds; digest reproduces bit-for-bit).
  * Firewall: FUNCTION only. consciousness_claim = 0, hard_problem_open = 1.
  * Stress Principle: a claim earns [V]/[L] only by surviving a test built to break
    it; a collapse is recorded and that line restarts next session with the break.
"""

import json
import hashlib
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from wave_compute_core import (hebbian_field, relax, overlap, pattern_to_phase,
                               corrupt_phase, SEED, THETA_GAMMA_CAPACITY,
                               CONSCIOUSNESS_CLAIM, HARD_PROBLEM_OPEN)


def digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


# ============================================================================
# FHRR phasor algebra (the L1 representation; bind+bundle were proven in v0.2)
# ============================================================================
# An atom is a unit-phasor vector e^{i phi}, phi ~ U(0,2pi). The three operations:
#   bind    (x) : elementwise phasor product  (phase addition; invertible by conj)
#   bundle  (+) : sum then project back to the unit circle (FHRR normalization;
#                 ZERO free parameters -- the definitional FHRR bundle)
#   permute rho : cyclic coordinate shift (a fixed permutation; its own inverse by
#                 the opposite shift). This is the NEW operation closing the algebra.

def rand_phasors(n, N, rng):
    """n unit-phasor atoms of dimension N."""
    return np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, size=(n, N)))


def bind(a, b):
    """role (x) value : phasor product = phase addition."""
    return a * b


def unbind(c, a):
    """invert bind by the role's phase conjugate."""
    return c * np.conj(a)


def bundle_unit(vecs):
    """FHRR bundle: sum of phasors projected back to the unit circle (no free param)."""
    s = np.sum(vecs, axis=0)
    mag = np.abs(s)
    mag[mag == 0.0] = 1.0          # measure-zero guard
    return s / mag


def permute(x, k=1):
    """rho^k : cyclic shift by k (a fixed permutation). Inverse = permute(x,-k)."""
    return np.roll(x, k, axis=-1)


def resonance_scores(query, codebook):
    """Phase-conjugate resonance of a query phasor against every codebook atom:
    Re<codebook_v, query>/N. Matched atom -> ~1; others -> ~0 +/- sqrt(load/N).
    Read-out is over the WHOLE codebook (argmax) -> non-circular."""
    N = query.shape[-1]
    return (codebook @ np.conj(query)).real / N


# ============================================================================
# L1a — PERMUTE: ordered sequence coding (the third operation, demonstrated)
# ============================================================================

def permute_sequence(N=512, V=256, lengths=(2, 4, 8, 16, 24, 32, 48, 64),
                     trials=12, base_seed=SEED):
    """Encode a length-L sequence of distinct fillers as S = sum_l rho^l(a_l).
    Recover the item at each position by rho^{-l}(S) + cleanup vs the codebook.
    Sweep L: position-indexed recall accuracy vs sequence length (crosstalk grows
    as ~sqrt(L/N)). Proves rho closes bind+bundle into an ordered structure."""
    out = []
    for L in lengths:
        accs = []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 1301 * t + L)
            codebook = rand_phasors(V, N, rng)
            idx = rng.choice(V, size=L, replace=False)           # distinct fillers
            S = bundle_unit(np.stack([permute(codebook[idx[l]], l)
                                      for l in range(L)]))
            ok = 0
            for l in range(L):
                q = permute(S, -l)                               # undo position tag
                pred = int(np.argmax(resonance_scores(q, codebook)))
                ok += (pred == idx[l])
            accs.append(ok / L)
        out.append({
            "L": L,
            "load_L_over_N": round(L / N, 3),
            "position_recall_acc": round(float(np.mean(accs)), 4),
            "position_recall_sd": round(float(np.std(accs)), 4),
        })
    return out


# ============================================================================
# L1b — ROLE-VALUE TREE depth-capacity (L1 milestone + stress test)
# ============================================================================

def _build_tree(depth, b, roles, codebook, rng, leaf_log):
    """Recursively encode a b-ary, depth-`depth` role->value tree as ONE phasor
    wave. At each internal node: bundle_b( role_j (x) permute(child_j) ). The
    permute protects depth (makes the encoding non-commutative across levels).
    Records, for ONE random path, the ground-truth leaf and the role path."""
    if depth == 0:
        v = int(rng.integers(codebook.shape[0]))
        leaf_log["leaf"] = v
        return codebook[v]
    children = []
    on_path = int(rng.integers(b))            # which branch the tracked path takes
    for j in range(b):
        if j == on_path:
            sub = {"leaf": None, "path": []}
            child = _build_tree(depth - 1, b, roles, codebook, rng, sub)
            leaf_log["leaf"] = sub["leaf"]
            leaf_log["path"] = [j] + sub.get("path", [])
        else:
            # sibling subtree summary: a random phasor (realistic crosstalk source)
            child = rand_phasors(1, codebook.shape[1], rng)[0]
        children.append(bind(roles[j], permute(child, 1)))
    return bundle_unit(np.stack(children))


def tree_depth_capacity(N=512, branchings=((2, (1, 2, 3, 4, 5, 6, 7, 8)),
                                           (3, (1, 2, 3, 4, 5))),
                        V=256, trials=12, base_seed=SEED):
    """Encode a depth-d, branching-b tree in one wave; query the path of role keys;
    recover the leaf (argmax over the filler codebook -> non-circular). Sweep depth.
    Report accuracy vs depth and the USEFUL DEPTH d* (max depth with acc >= 0.95).
    STRESS: crosstalk collapses structured recovery before any useful depth."""
    results = {}
    for b, depths in branchings:
        rows = []
        for d in depths:
            accs = []
            for t in range(trials):
                rng = np.random.default_rng(base_seed + 5003 * t + 101 * b + d)
                codebook = rand_phasors(V, N, rng)
                roles = rand_phasors(b, N, rng)
                ok = 0
                reps = 6                                          # paths per tree
                for _ in range(reps):
                    log = {"leaf": None, "path": []}
                    root = _build_tree(d, b, roles, codebook, rng, log)
                    x = root
                    for j in log["path"]:
                        x = permute(unbind(x, roles[j]), -1)      # descend: unbind+unpermute
                    pred = int(np.argmax(resonance_scores(x, codebook)))
                    ok += (pred == log["leaf"])
                accs.append(ok / reps)
            rows.append({
                "depth": d,
                "structured_query_acc": round(float(np.mean(accs)), 4),
                "acc_sd": round(float(np.std(accs)), 4),
            })
        d_star = max([r["depth"] for r in rows if r["structured_query_acc"] >= 0.95],
                     default=0)
        results[f"b{b}"] = {
            "branching": b,
            "curve": rows,
            "useful_depth_d_star": d_star,
        }
    return results


# ============================================================================
# L2a — METASTABLE TRAJECTORY: asymmetric (delayed) Hebbian on the L0 substrate
# ============================================================================
# Symmetric Hebbian J_sym (from L0) makes each pattern a fixed-point attractor.
# An ASYMMETRIC, TIME-DELAYED term J_asym = (1/N) sum ξ_{μ+1} ξ_μ^T, driven by a
# DELAYED copy of the phase state, tilts the landscape from the current pattern
# toward its successor -> the field hops μ -> μ+1 -> ... (heteroclinic cycle).
# Kept in pure phase-coupling form  c*(J@s) - s*(J@c) = sum_j J_ij sin(θ_j-θ_i)
# so it reuses the L0 substrate exactly (non-circular).

def _phase_coupling(theta, J, theta_src=None):
    """sum_j J_ij sin(θ^src_j - θ_i), vectorized. theta_src=theta if None."""
    s, c = np.sin(theta), np.cos(theta)
    if theta_src is None:
        ss, cc = s, c
    else:
        ss, cc = np.sin(theta_src), np.cos(theta_src)
    return c * (J @ ss) - s * (J @ cc)


def _run_trajectory(theta0, Jsym, Jasym, lam, tau, dt=0.05, steps=600,
                    recog_floor=0.5, patterns=None):
    """Integrate the delayed-asymmetric dynamics; return the sequence of recognized
    pattern indices over time (argmax overlap if above recog_floor, else -1)."""
    theta = theta0.copy()
    buf = [theta.copy() for _ in range(tau)]            # delay line (length tau)
    visited = []
    m = patterns.shape[0]
    for _ in range(steps):
        th_del = buf[0]
        drive = _phase_coupling(theta, Jsym) + lam * _phase_coupling(theta, Jasym,
                                                                     theta_src=th_del)
        theta = theta + dt * drive
        buf.append(theta.copy()); buf.pop(0)
        ov = np.array([overlap(theta, patterns[mu]) for mu in range(m)])
        best = int(np.argmax(ov))
        visited.append(best if ov[best] >= recog_floor else -1)
    return visited


def _ordered_run_score(visited, m):
    """From the recognized-index timeseries, the fraction of the m-cycle traversed
    in correct cyclic order starting at pattern 0. De-dupe consecutive repeats; then
    count the longest prefix 0,1,2,... (mod m). Non-circular: order emerges from the
    dynamics, we only read overlaps."""
    seq = [v for v in visited if v != -1]
    dedup = []
    for v in seq:
        if not dedup or dedup[-1] != v:
            dedup.append(v)
    # find first occurrence of pattern 0, then count consecutive +1 (mod m)
    if 0 not in dedup:
        return 0.0
    start = dedup.index(0)
    expect = 0
    count = 0
    for v in dedup[start:]:
        if v == expect:
            count += 1
            expect = (expect + 1) % m
        else:
            break
    # count includes the starting pattern; transitions = count-1 out of m
    return round(min(count, m) / m, 4)


def heteroclinic_replay(N=256, m=6, lambdas=(0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0),
                        tau=12, trials=6, replay_steps=900, predict_steps=500,
                        base_seed=SEED):
    """Learn a cycle ξ_0->ξ_1->...->ξ_{m-1}->ξ_0. Two distinct claims, separately
    graded:
      PREDICT-NEXT (single transition μ->μ+1): cue a corrupted ξ_k; does the field
        advance to ξ_{k+1}? -- the core test that the asymmetric term implements
        'go to the successor'. (Verified mechanism if a clear band reaches ~1.)
      ORDERED REPLAY (sustained full m-cycle): from ξ_0, how much of the whole cycle
        is traversed in correct order within the step budget? -- the harder sustained
        claim (multi-hop chaining without re-cueing).
    Sweep lambda -> the band where chaining works. STRESS: too weak => stuck at a
    fixed point (replay = 1/m, predict = 0); too strong => diverges/scrambles. No
    band => metastable chaining fails and L2a restarts with the break."""
    rows = []
    for lam in lambdas:
        replay_scores, predict_acc = [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 7331 * t + int(lam * 1000))
            patterns = rng.choice([-1.0, 1.0], size=(m, N))
            Jsym = hebbian_field(patterns)
            # forward links μ -> μ+1 (cyclic), symmetric-Hebbian style outer products
            Jasym = np.zeros((N, N))
            for mu in range(m):
                nxt = (mu + 1) % m
                Jasym += np.outer(patterns[nxt], patterns[mu]) / N
            np.fill_diagonal(Jasym, 0.0)
            # (a) sustained ordered replay from ξ_0 (small jitter off the saddle)
            th0 = pattern_to_phase(patterns[0]) + rng.uniform(-0.05, 0.05, size=N)
            visited = _run_trajectory(th0, Jsym, Jasym, lam, tau,
                                      steps=replay_steps, patterns=patterns)
            replay_scores.append(_ordered_run_score(visited, m))
            # (b) predict-next: cue a corrupted ξ_k, read whether ξ_{k+1} is reached
            pn_ok = 0
            for k in range(m):
                cue = corrupt_phase(pattern_to_phase(patterns[k]), 0.12, 0.25, rng)
                vis = _run_trajectory(cue, Jsym, Jasym, lam, tau,
                                      steps=predict_steps, patterns=patterns)
                seq = [v for v in vis if v != -1]
                dd = []
                for v in seq:
                    if not dd or dd[-1] != v:
                        dd.append(v)
                # success if k appears and is immediately followed by (k+1) mod m
                nxt = (k + 1) % m
                hit = any(dd[i] == k and dd[i + 1] == nxt for i in range(len(dd) - 1))
                pn_ok += hit
            predict_acc.append(pn_ok / m)
        rows.append({
            "lambda": lam,
            "ordered_replay_mean": round(float(np.mean(replay_scores)), 4),
            "ordered_replay_sd": round(float(np.std(replay_scores)), 4),
            "predict_next_acc": round(float(np.mean(predict_acc)), 4),
            "predict_next_sd": round(float(np.std(predict_acc)), 4),
        })
    # predict-next band: single-transition mechanism verified (>=0.9, sign-stable)
    predict_band = [r["lambda"] for r in rows if r["predict_next_acc"] >= 0.9]
    # full-replay band: sustained chaining (>=0.8)
    replay_band = [r["lambda"] for r in rows if r["ordered_replay_mean"] >= 0.8]
    best_p = max(rows, key=lambda r: r["predict_next_acc"])
    best_r = max(rows, key=lambda r: r["ordered_replay_mean"])
    return {
        "curve": rows,
        "tau": tau,
        "predict_next_band_lambda": predict_band,
        "predict_band_exists": len(predict_band) > 0,
        "best_predict_next": best_p["predict_next_acc"],
        "best_predict_lambda": best_p["lambda"],
        "replay_band_lambda": replay_band,
        "replay_band_exists": len(replay_band) > 0,
        "best_ordered_replay": best_r["ordered_replay_mean"],
        "best_replay_lambda": best_r["lambda"],
    }


def replay_tau_robustness(N=256, m=6, lam=None, taus=(8, 12, 16), trials=6,
                          base_seed=SEED):
    """Check the replay band is not a knife-edge in the (structural) delay tau.
    lam defaults to a mid value; we report ordered replay at each tau."""
    if lam is None:
        lam = 1.0
    rows = []
    for tau in taus:
        scores = []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 7331 * t + int(lam * 1000))
            patterns = rng.choice([-1.0, 1.0], size=(m, N))
            Jsym = hebbian_field(patterns)
            Jasym = np.zeros((N, N))
            for mu in range(m):
                Jasym += np.outer(patterns[(mu + 1) % m], patterns[mu]) / N
            np.fill_diagonal(Jasym, 0.0)
            th0 = pattern_to_phase(patterns[0]) + rng.uniform(-0.05, 0.05, size=N)
            visited = _run_trajectory(th0, Jsym, Jasym, lam, tau, patterns=patterns)
            scores.append(_ordered_run_score(visited, m))
        rows.append({"tau": tau, "lambda": lam,
                     "ordered_replay_mean": round(float(np.mean(scores)), 4)})
    return rows


# ============================================================================
# L2b — THETA-GAMMA WORKING MEMORY: phase-slot multiplexing under finite precision
# ============================================================================
# One slow theta carrier nests gamma slots; item k lives in slot k (= permutation
# rho^k, reusing L1a). Finite gamma phase precision = substrate phase JITTER on the
# composite. Capacity = max #items still readable. The brain's ~7 (FOXG1 gamma) is
# NOT transferred; we test whether the MECHANISM yields a small finite capacity and
# read the number off the sweep.

def _phasor_jitter(z, sigma, rng):
    """Apply gamma-precision phase jitter: multiply each phasor by e^{i*eps}."""
    eps = rng.normal(0.0, sigma, size=z.shape)
    return z * np.exp(1j * eps)


def theta_gamma_wm(N=512, V=256, n_slots=(4, 8, 16, 24),
                   jitters=(0.0, 0.3, 0.6, 0.9, 1.2, 1.6), trials=10,
                   recall_thresh=0.9, base_seed=SEED):
    """Load m items (m up to n_slot) into gamma phase-slots of one theta cycle
    (slot k = rho^k); jitter the composite (finite gamma precision); read each slot
    by rho^{-k} + cleanup. Capacity = max m with mean slot recall >= thresh.
    Sweep (n_slot, jitter). HONEST capacity law: at low jitter capacity = n_slot
    (slot-limited); as precision degrades, capacity caps BELOW n_slot
    (precision-limited). The brain's ~7 = ~7 gamma slots (B5); the MECHANISM and its
    capacity law are reproduced, the number is NOT transferred."""
    grid = []
    for n_slot in n_slots:
        for sigma in jitters:
            cap_trials = []
            for t in range(trials):
                rng = np.random.default_rng(base_seed + 911 * t + 31 * n_slot
                                            + int(sigma * 100))
                codebook = rand_phasors(V, N, rng)
                cap = 0
                for m in range(1, n_slot + 1):
                    idx = rng.choice(V, size=m, replace=False)
                    S = bundle_unit(np.stack([permute(codebook[idx[k]], k)
                                              for k in range(m)]))
                    S = _phasor_jitter(S, sigma, rng)
                    ok = 0
                    for k in range(m):
                        q = permute(S, -k)
                        pred = int(np.argmax(resonance_scores(q, codebook)))
                        ok += (pred == idx[k])
                    if ok / m >= recall_thresh:
                        cap = m              # still readable at this load
                    else:
                        break                # capacity reached
                cap_trials.append(cap)
            grid.append({
                "n_slot": n_slot,
                "jitter_sigma": sigma,
                "wm_capacity_mean": round(float(np.mean(cap_trials)), 3),
                "wm_capacity_sd": round(float(np.std(cap_trials)), 3),
                "slot_limited": float(np.mean(cap_trials)) >= n_slot - 0.5,
            })
    # capacity law: is it slot-limited at low jitter and precision-limited at high?
    big = max(n_slots)
    low_j = [g for g in grid if g["n_slot"] == big and g["jitter_sigma"] <= 0.3]
    high_j = [g for g in grid if g["n_slot"] == big and g["jitter_sigma"] >= 1.2]
    slot_limited_low = all(g["slot_limited"] for g in low_j) if low_j else False
    precision_capped_high = (all(not g["slot_limited"] for g in high_j)
                             if high_j else False)
    # where (if anywhere) does precision cap capacity into the Miller (4-9) range?
    miller_like = sorted({(g["n_slot"], g["jitter_sigma"])
                          for g in grid if 4 <= g["wm_capacity_mean"] <= 9})
    return {
        "grid": grid,
        "note": "theta-gamma multiplexing; gamma precision = phase jitter. "
                "Capacity = min(n_slot, precision_limit(sigma)). B5 principle "
                "inherited; the number ~7 (FOXG1 gamma = ~7 slots) NOT transferred.",
        "inherited_capacity_anchor_NOT_a_target": THETA_GAMMA_CAPACITY,
        "capacity_is_slot_limited_at_low_jitter": slot_limited_low,
        "capacity_is_precision_capped_at_high_jitter": precision_capped_high,
        "precision_capacity_law_demonstrated": slot_limited_low and precision_capped_high,
        "miller_range_operating_points": [list(t) for t in miller_like],
    }


# ============================================================================
# RUN + DIGEST
# ============================================================================

def main():
    np.seterr(all="ignore")
    results = {
        "_what": "vp_wave_computer v0.3 — L1 complete (permute, tree depth) + L2 start (trajectory, theta-gamma WM)",
        "firewall": {"consciousness_claim": CONSCIOUSNESS_CLAIM,
                     "hard_problem_open": HARD_PROBLEM_OPEN},
        "new_tuned_constants": 0,
        "reuses_substrate": "wave_compute_core (L0) + wave_resonance_core (L1 bind/bundle) — exact, non-circular",
    }

    print("[L1a] permute closes the algebra: ordered sequence coding ...")
    results["L1a_permute_sequence"] = permute_sequence()
    for r in results["L1a_permute_sequence"]:
        print(f"   L={r['L']:3d} (L/N={r['load_L_over_N']:.2f})  "
              f"position_recall={r['position_recall_acc']:.3f}±{r['position_recall_sd']:.3f}")

    print("[L1b] role-value tree depth-capacity (milestone + stress) ...")
    results["L1b_tree_depth"] = tree_depth_capacity()
    for key, blk in results["L1b_tree_depth"].items():
        print(f"   branching b={blk['branching']}: useful depth d* = {blk['useful_depth_d_star']}")
        for r in blk["curve"]:
            print(f"      depth={r['depth']}  acc={r['structured_query_acc']:.3f}±{r['acc_sd']:.3f}")

    print("[L2a] metastable trajectory: delayed-asymmetric replay (sweep lambda) ...")
    results["L2a_heteroclinic"] = heteroclinic_replay()
    for r in results["L2a_heteroclinic"]["curve"]:
        print(f"   lambda={r['lambda']:.2f}  ordered_replay={r['ordered_replay_mean']:.3f}"
              f"±{r['ordered_replay_sd']:.3f}  predict_next={r['predict_next_acc']:.3f}"
              f"±{r['predict_next_sd']:.3f}")
    het = results["L2a_heteroclinic"]
    print(f"   predict-next band (>=0.9): lambda in {het['predict_next_band_lambda']}"
          f"  best={het['best_predict_next']} @ lambda={het['best_predict_lambda']}")
    print(f"   full-replay band (>=0.8): lambda in {het['replay_band_lambda']}"
          f"  best={het['best_ordered_replay']} @ lambda={het['best_replay_lambda']}")
    results["L2a_tau_robustness"] = replay_tau_robustness(lam=het["best_replay_lambda"])
    print("   tau robustness at best replay lambda:")
    for r in results["L2a_tau_robustness"]:
        print(f"      tau={r['tau']}  ordered_replay={r['ordered_replay_mean']:.3f}")

    print("[L2b] theta-gamma working memory: phase-slot multiplexing under jitter ...")
    results["L2b_theta_gamma_wm"] = theta_gamma_wm()
    for g in results["L2b_theta_gamma_wm"]["grid"]:
        print(f"   n_slot={g['n_slot']:2d}  jitter={g['jitter_sigma']:.1f}  "
              f"WM_capacity={g['wm_capacity_mean']:.2f}±{g['wm_capacity_sd']:.2f}"
              f"  slot_limited={g['slot_limited']}")

    # ---- headline (derived from the sweeps; not asserted) ----
    seq = results["L1a_permute_sequence"]
    perm_cap = max([s["L"] for s in seq if s["position_recall_acc"] >= 0.95], default=0)
    d2 = results["L1b_tree_depth"]["b2"]["useful_depth_d_star"]
    d3 = results["L1b_tree_depth"]["b3"]["useful_depth_d_star"]
    het = results["L2a_heteroclinic"]
    wm = results["L2b_theta_gamma_wm"]

    results["headline"] = {
        "L1_permute_ordered_capacity_L": perm_cap,
        "L1_algebra_closed": perm_cap >= 2,                  # bind+bundle+permute all work
        "L1_tree_useful_depth_b2": d2,
        "L1_tree_useful_depth_b3": d3,
        "L1_supports_structured_depth": (d2 >= 2 or d3 >= 2),   # stress: pass if depth>=2
        "L1_depth_is_shallow_L3_needed_for_deep": (max(d2, d3) <= 5),  # honest ceiling
        "L2_predict_next_mechanism_verified": het["predict_band_exists"],
        "L2_best_predict_next": het["best_predict_next"],
        "L2_sustained_replay_band_exists": het["replay_band_exists"],
        "L2_best_ordered_replay": het["best_ordered_replay"],
        "L2_wm_precision_capacity_law": wm["precision_capacity_law_demonstrated"],
        "L2_wm_slot_limited_low_jitter": wm["capacity_is_slot_limited_at_low_jitter"],
        # grades (honest; set from the sweeps above)
        "grade_L1a_permute": "[V]" if perm_cap >= 2 else "[O]",
        "grade_L1b_tree": "[V]" if (d2 >= 2 or d3 >= 2) else "[O]",
        "grade_L2a_predict_next": "[V]" if het["predict_band_exists"] else "[O]",
        "grade_L2a_sustained_replay": "[V]" if het["replay_band_exists"] else "[O]",
        "grade_L2b_theta_gamma": ("[V]" if wm["precision_capacity_law_demonstrated"]
                                  else "[O]"),
    }

    print("\n--- headline (derived from sweeps) ---")
    h = results["headline"]
    print(f"   L1 permute ordered capacity      : L≈{perm_cap}  -> algebra closed: {h['L1_algebra_closed']}  {h['grade_L1a_permute']}")
    print(f"   L1 tree useful depth (b=2 / b=3)  : d*={d2} / d*={d3}  -> structured depth: {h['L1_supports_structured_depth']} (shallow; L3 for deeper)  {h['grade_L1b_tree']}")
    print(f"   L2a predict-next (single hop)     : verified band={h['L2_predict_next_mechanism_verified']}, best={h['L2_best_predict_next']}  {h['grade_L2a_predict_next']}")
    print(f"   L2a sustained full-cycle replay   : band exists={h['L2_sustained_replay_band_exists']}, best={h['L2_best_ordered_replay']}  {h['grade_L2a_sustained_replay']}")
    print(f"   L2b theta-gamma capacity law      : precision/slot law shown={h['L2_wm_precision_capacity_law']}  {h['grade_L2b_theta_gamma']}")
    print(f"   (B5 anchor WM~{THETA_GAMMA_CAPACITY} = ~7 gamma SLOTS, cited as PRINCIPLE, number not transferred; new_tuned_constants=0)")

    results["_digest"] = digest({k: v for k, v in results.items()
                                 if not k.startswith("_")})
    with open("wave_structure_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\ndigest = {results['_digest'][:16]}...")
    print("wrote wave_structure_results.json")
    return results


if __name__ == "__main__":
    main()
