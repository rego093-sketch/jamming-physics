#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
immune_maturation.py  --  IMMUNE STRENGTHENING, END TO END  (battery IM1-IM4).

  The strengthening side of the immune switch, on the SAME vendored R19 substrate, at the MEASURED
  immune master-gene gamma (inherited/immune_gamma.json: FOXN1, TLX1, RUNX1 innate, PAX5 adaptive).
  This battery closes the three open Track-III roadmap items (00_CONTINUATION_BLUEPRINT B.3):
  affinity maturation as iterated selection (III-1), the innate-vs-adaptive durability split (III-2),
  and tolerance as the opposite-sign drive (III-3). It is the immune feed into the vaccine application
  (V) -- still direction-only behind the magnitude firewall.

IM1  Affinity maturation EMERGES from an iterated germinal-centre loop (compete -> select -> reseed/
     mutate). Affinity is grounded as the switch BARRIER (gamma^2/4: a deeper basin is a more committed,
     longer-lived memory clone). Sweeping the selection PRESSURE, the maturation gain has an INTERIOR
     OPTIMUM -- too weak, no directional maturation; too stringent, the germinal centre dies and re-founds
     from naive precursors. The inverted-U is MEASURED from the loop, not asserted. Absolute pressure [O]. [V]
IM2  Innate vs adaptive is a TWO-TIMESCALE durability split: trained/innate immunity sits on the SHALLOWEST
     measured barrier (RUNX1) and adaptive memory on the DEEPEST (PAX5). The memory lifetime (MFPT, measured
     from the escape statistic) of the adaptive switch exceeds the innate one and the two timescales are
     well-separated -- so protection decays as fast(innate)+slow(adaptive), the slow arm being the deep
     barrier. The ratio is read; absolute lifetimes [O]. [V]
IM3  Tolerance is the OPPOSITE-SIGN drive on the SAME switch: a +drive past the spinodal flips OFF->ON
     (responsive memory); a -drive of EQUAL magnitude flips ON->OFF (unresponsive tolerance). Both are HELD
     basins after the drive clears (hysteresis), so desensitisation persists exactly as memory does. The SIGN
     selects memory<->tolerance -- the shared substrate of vaccination and allergen desensitisation. [V]
IM4  honest scoreboard + firewall (clinical immunisation / desensitisation belong to clinicians).
"""
import os, json, math
import numpy as np
from _substrate import immune_gamma, sdot, spinodal, barrier, SEED


# ---------------------------------------------------------------------------
#  substrate integrators -- drift term taken from the VENDORED sdot (single source);
#  the stochastic loop adds noise locally (the substrate has no noise primitive).
# ---------------------------------------------------------------------------
def _settle(g, h, s0=None, n=4000, dt=0.01):
    """Deterministic settle of the R19 field to steady state under fixed drive h."""
    s = (-math.sqrt(g) if (s0 is None) else float(s0))
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s


def _mfpt_survival(g, D, n_steps, n_cells=8000, dt=0.01, seed=SEED):
    """Mean first-passage time out of the activated basin under additive noise D (drive h=0), measured
    from the SURVIVING FRACTION at the horizon -- the standard exponential first-passage estimator,
    stable in the rare-escape (Kramers) regime where a deep barrier escapes only rarely:
        S = fraction not yet crossed at horizon T ;  rate = -ln(S)/T ;  MFPT = 1/rate.
    ds = sdot(s,g,0) dt + sqrt(2 D dt) xi, start ON at s=+sqrt(g). Deterministic per seed.
    Returns (mfpt, surviving_fraction)."""
    rng = np.random.default_rng(seed)
    s = np.full(n_cells, math.sqrt(g), dtype=float)
    c = math.sqrt(2.0 * D * dt)
    crossed = np.zeros(n_cells, dtype=bool)
    for _ in range(n_steps):
        s += sdot(s, g, 0.0) * dt + c * rng.standard_normal(n_cells)
        crossed |= (s < 0.0)
    surv = 1.0 - float(np.mean(crossed))
    T = n_steps * dt
    if surv <= 0.0:
        return 0.0, surv
    if surv >= 1.0:
        return float("inf"), surv
    rate = -math.log(surv) / T
    return ((1.0 / rate) if rate > 0 else float("inf")), surv


# ===========================================================================
#  IM1 -- affinity maturation EMERGES from iterated selection; interior optimum
# ===========================================================================
def _gc_round_pool(pool, keep_frac, mut_sd, naive_mean, g_lo, g_hi, k_min, rng):
    """One germinal-centre round on a pool of clone gammas (affinity proxy = barrier gamma^2/4).
    Select the top keep_frac by barrier; if the survivor count < k_min the GC DIES and re-founds from
    naive precursors (a reset toward the baseline); else reseed to full size from survivors + somatic
    hypermutation. Returns the next pool. Higher-barrier clones win (selection acts on stability)."""
    n = len(pool)
    k = max(1, int(round(keep_frac * n)))
    order = np.argsort(pool)                 # ascending gamma == ascending barrier
    survivors = pool[order[-k:]]             # keep the highest-barrier clones
    if k < k_min:
        # over-stringent selection -> germinal-centre death -> re-found from naive precursors
        nxt = rng.normal(naive_mean, mut_sd, size=n)
    else:
        idx = rng.integers(0, k, size=n)     # reseed pool from survivors (with replacement)
        nxt = survivors[idx] + rng.normal(0.0, mut_sd, size=n)
    return np.clip(nxt, g_lo, g_hi)


def _maturation_gain(keep_frac, rounds, pool0, mut_sd, naive_mean, g_lo, g_hi, k_min, seed):
    """Final mean barrier minus initial mean barrier after `rounds` GC rounds at this selection pressure."""
    rng = np.random.default_rng(seed)
    pool = pool0.copy()
    b0 = float(np.mean(barrier(pool)))
    traj = [b0]
    for _ in range(rounds):
        pool = _gc_round_pool(pool, keep_frac, mut_sd, naive_mean, g_lo, g_hi, k_min, rng)
        traj.append(float(np.mean(barrier(pool))))
    return traj[-1] - b0, traj


def IM1_affinity_maturation_interior_optimum():
    """Maturation gain vs selection pressure has an INTERIOR optimum (emergent, measured from the loop)."""
    G = immune_gamma()
    naive = G["PAX5"]                                   # adaptive master -> the founding affinity scale
    pool_n, rounds, mut_sd, k_min = 300, 14, 0.045, 10
    g_lo, g_hi = 1.20, 1.55                             # plausible promoter-gamma range (immune atlas span)
    rng0 = np.random.default_rng(SEED)
    pool0 = np.clip(rng0.normal(naive, 0.05, size=pool_n), g_lo, g_hi)   # founding clone repertoire
    # sweep survivor fraction f (selection pressure = 1 - f): f=1 no selection, f small over-stringent
    fracs = [1.0, 0.6, 0.4, 0.25, 0.15, 0.10, 0.06, 0.033, 0.02, 0.01]
    rows = []
    for f in fracs:
        gain, _ = _maturation_gain(f, rounds, pool0, mut_sd, naive, g_lo, g_hi, k_min, seed=SEED)
        rows.append({"survivor_frac": f, "pressure": round(1.0 - f, 3), "maturation_gain": round(gain, 6)})
    gains = [r["maturation_gain"] for r in rows]
    i_best = int(np.argmax(gains))
    interior = (0 < i_best < len(gains) - 1)            # optimum is neither weakest nor most stringent
    emerges = gains[i_best] > 0.0                       # maturation actually happens at the optimum
    # the optimum trajectory should rise (progressive maturation, not a one-shot jump)
    _, traj_best = _maturation_gain(fracs[i_best], rounds, pool0, mut_sd, naive, g_lo, g_hi, k_min, seed=SEED)
    rises = traj_best[-1] > traj_best[0]
    weak_arm = gains[0]                                 # f=1.0 : no selection
    strict_arm = gains[-1]                              # f=0.01: GC death / reset
    return {
        "name": "IM1 affinity maturation emerges from iterated selection; gain has an interior optimum",
        "pool": pool_n, "rounds": rounds, "mutation_sd": mut_sd, "k_min_viable": k_min,
        "naive_master": "PAX5", "naive_gamma": round(naive, 4),
        "sweep": rows,
        "optimum_pressure": rows[i_best]["pressure"], "optimum_survivor_frac": fracs[i_best],
        "optimum_gain": round(gains[i_best], 6),
        "weak_selection_gain": round(weak_arm, 6), "over_stringent_gain": round(strict_arm, 6),
        "interior_optimum": bool(interior), "maturation_emerges": bool(emerges),
        "optimum_trajectory_rises": bool(rises),
        "grade": "[V] inverted-U + emergence MEASURED from the GC loop on the substrate; "
                 "absolute selection pressure -> affinity in real units is runtime [O]",
        "pass": bool(interior and emerges and rises),
    }


# ===========================================================================
#  IM2 -- innate vs adaptive : a two-timescale durability split (measured MFPT)
# ===========================================================================
def IM2_innate_vs_adaptive_two_timescales():
    """Trained/innate (RUNX1, shallowest barrier) vs adaptive (PAX5, deepest): the adaptive memory
    lifetime (MFPT) exceeds the innate one and the two timescales are well-separated -- the substrate
    origin of fast(innate)+slow(adaptive) protection decay."""
    G = immune_gamma()
    g_innate, g_adaptive = G["RUNX1"], G["PAX5"]
    # confirm the role assignment matches the measured barrier ordering (shallowest = innate)
    innate_is_shallowest = (g_innate == min(G.values()))
    adaptive_is_deepest  = (g_adaptive == max(G.values()))
    D, steps = 0.12, 8000                              # rare-escape regime: the deep barrier escapes only rarely
    mfpt_innate,   surv_innate   = _mfpt_survival(g_innate,   D, steps, seed=SEED)
    mfpt_adaptive, surv_adaptive = _mfpt_survival(g_adaptive, D, steps, seed=SEED)
    ratio = (mfpt_adaptive / mfpt_innate) if (math.isfinite(mfpt_adaptive) and mfpt_innate > 0) else float("inf")
    adaptive_outlasts = (mfpt_adaptive > mfpt_innate)
    well_separated = (ratio >= 2.0)                    # two clearly distinct decay timescales (fast vs slow arm)
    tracks_barrier = (barrier(g_adaptive) > barrier(g_innate)) == adaptive_outlasts
    return {
        "name": "IM2 innate vs adaptive = two-timescale durability split (slow arm = deep barrier)",
        "noise_D": D, "horizon_steps": steps,
        "innate": {"gene": "RUNX1", "gamma": round(g_innate, 4), "barrier": round(barrier(g_innate), 4),
                   "surviving_fraction": round(surv_innate, 4),
                   "mfpt": (round(mfpt_innate, 2) if math.isfinite(mfpt_innate) else "inf")},
        "adaptive": {"gene": "PAX5", "gamma": round(g_adaptive, 4), "barrier": round(barrier(g_adaptive), 4),
                     "surviving_fraction": round(surv_adaptive, 4),
                     "mfpt": (round(mfpt_adaptive, 2) if math.isfinite(mfpt_adaptive) else "inf")},
        "mfpt_ratio_adaptive_over_innate": (round(ratio, 3) if math.isfinite(ratio) else "inf"),
        "role_matches_barrier_ordering": bool(innate_is_shallowest and adaptive_is_deepest),
        "adaptive_outlasts_innate": bool(adaptive_outlasts),
        "timescales_well_separated": bool(well_separated),
        "durability_tracks_measured_gamma": bool(tracks_barrier),
        "grade": "[V] durability ordering + separation EMERGE from the measured escape statistic and track "
                 "the measured gamma; absolute lifetimes (days/years) are runtime [O]",
        "pass": bool(innate_is_shallowest and adaptive_is_deepest and adaptive_outlasts
                     and well_separated and tracks_barrier),
    }


# ===========================================================================
#  IM3 -- tolerance is the opposite-sign drive on the same switch
# ===========================================================================
def _min_abs_drive_to_flip(g, sign, h_base=0.0, s0=None, cap_mult=2.5, npts=251):
    """Smallest |drive| of the given sign that, settling from s0 under h_base+sign*|d|, crosses the ridge."""
    hsp = spinodal(g)
    s_start = (-math.sqrt(g) if s0 is None else s0)
    for d in np.linspace(0.0, cap_mult * hsp, npts):
        s = _settle(g, h_base + sign * d, s0=s_start)
        if (s > 0.0) if sign > 0 else (s < 0.0):
            return float(d)
    return float("inf")


def IM3_tolerance_is_opposite_sign():
    """Memory (+drive into the responsive basin) and tolerance (-drive into the unresponsive basin) are
    the SAME switch, opposite sign; both states are HELD after the drive clears (hysteresis)."""
    G = immune_gamma()
    g = G["PAX5"]                                       # the adaptive switch carries both memory and tolerance
    hsp = spinodal(g)
    d_to_memory   = _min_abs_drive_to_flip(g, +1.0, s0=-math.sqrt(g))   # naive OFF -> responsive ON
    d_to_tolerance = _min_abs_drive_to_flip(g, -1.0, s0=+math.sqrt(g))  # activated ON -> tolerant OFF
    # the substrate is sign-symmetric: the two flip thresholds equal the spinodal magnitude
    symmetric = (math.isfinite(d_to_memory) and math.isfinite(d_to_tolerance)
                 and abs(d_to_memory - d_to_tolerance) <= 0.02 * hsp)
    near_spinodal = (abs(d_to_memory - hsp) <= 0.06 * hsp) and (abs(d_to_tolerance - hsp) <= 0.06 * hsp)
    # hysteresis: with the drive cleared, BOTH basins are held (bistable memory of the last drive sign)
    held_responsive = _settle(g, 0.0, s0=+math.sqrt(g)) > 0.0      # memory persists after antigen clears
    held_tolerant   = _settle(g, 0.0, s0=-math.sqrt(g)) < 0.0      # desensitisation persists after dosing stops
    both_held = bool(held_responsive and held_tolerant)
    # the sign of the drive selects the inherited outcome: memory vs tolerance are opposite
    memory_outcome   = _settle(g, 0.0, s0=_settle(g, +1.05 * hsp, s0=-math.sqrt(g))) > 0.0
    tolerance_outcome = _settle(g, 0.0, s0=_settle(g, -1.05 * hsp, s0=+math.sqrt(g))) < 0.0
    sign_law = bool(memory_outcome and tolerance_outcome)
    return {
        "name": "IM3 tolerance is the opposite-sign drive on the same switch (memory <-> tolerance)",
        "switch": "PAX5", "gamma": round(g, 4), "spinodal": round(hsp, 4),
        "drive_to_memory": round(d_to_memory, 4), "drive_to_tolerance": round(d_to_tolerance, 4),
        "flip_thresholds_symmetric": bool(symmetric),
        "thresholds_at_spinodal_magnitude": bool(near_spinodal),
        "responsive_state_held_after_clear": bool(held_responsive),
        "tolerant_state_held_after_clear": bool(held_tolerant),
        "both_states_hysteretic": both_held,
        "plus_drive_gives_memory_minus_gives_tolerance": sign_law,
        "grade": "[V] the sign law (memory<->tolerance) and the held basin of BOTH states are measured from "
                 "the substrate; absolute desensitisation dose/schedule is [O]; clinical tolerance to clinicians",
        "pass": bool(symmetric and near_spinodal and both_held and sign_law),
    }


def run_battery():
    tests = [IM1_affinity_maturation_interior_optimum(),
             IM2_innate_vs_adaptive_two_timescales(),
             IM3_tolerance_is_opposite_sign()]
    allp = all(t["pass"] for t in tests)
    return {"module": "immune_maturation", "battery": "IM1-IM4", "seed": SEED,
            "IM4_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "affinity-maturation SHAPE (interior optimum), innate/adaptive durability ORDERING, "
                        "and the memory<->tolerance SIGN read [V]; absolute selection pressure, memory "
                        "lifetimes, and desensitisation dose are runtime [O]; clinical immunisation and "
                        "desensitisation belong to clinicians and regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
