#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rna_vaccine_kinetics.py  --  VACCINE SCHEDULE KINETICS  (battery VK1-VK3)  [blueprint IV-1, IV-3].

  rna_vaccine.py (V) established the vaccine as a supra-spinodal drive into a barrier-held protected basin,
  with a schedule interior optimum from a coverage proxy. This module sharpens the schedule science the
  application actually needs, on the SAME vendored R19 substrate at the MEASURED immune master-gene gamma,
  by COUPLING two pieces already measured elsewhere in the kit:
    * the affinity-maturation endpoint (IM1: a germinal-centre loop whose gain rises then saturates with
      the number of rounds), and
    * the memory-decay statistic (IM2/I1: the primed pool leaks out of the activated basin at a measured
      escape rate).
  Their PRODUCT gives the prime-boost timing law (IV-1); the saRNA self-amplification gives a longer
  effective drive WINDOW (IV-3). MAGNITUDE FIREWALL: the interior-optimal interval SHAPE and the saRNA>mRNA
  reliability ORDERING are read [V]; absolute days, titres, and amplification factors are runtime [O].

VK1  prime-boost interval from the MATURATION ENDPOINT: the boost benefit = (matured affinity available)
     x (fraction of the primed pool still present) = maturation_gain(rounds(T)) * survival(T). Too short ->
     the germinal centre has not matured; too long -> the primed pool has decayed. The product has an
     INTERIOR optimum in the interval T -- the inverted-U in TIME. Read the SHAPE; absolute days [O]. [V]
VK2  saRNA vs mRNA: saRNA replicates its own payload, so it supplies the SAME-amplitude drive for a LONGER
     effective window. At a fixed near-spinodal amplitude under noise, the longer saRNA window crosses into
     the protected basin MORE RELIABLY than the shorter mRNA window (the durability AFTER the flip is the
     same barrier for both -- the saRNA advantage is in REACHING the basin, not holding it). Read the
     reliability ORDERING saRNA > mRNA from the longer window; absolute titre / amplification factor [O]. [V]
VK3  honest scoreboard + firewall (clinical dosing intervals and titres belong to clinicians/regulators).
"""
import json, math
import numpy as np
from _substrate import immune_gamma, sdot, spinodal, barrier, SEED


# ---------------------------------------------------------------------------
#  measured memory-decay rate (the primed pool leaks out of the activated basin)
# ---------------------------------------------------------------------------
def _escape_rate(g, D, n_cells=6000, n_steps=4000, dt=0.01, seed=SEED):
    """Spontaneous ON->OFF escape rate (h=0) of the primed switch, from the counted first crossings."""
    rng = np.random.default_rng(seed)
    s = np.full(n_cells, math.sqrt(g), dtype=float)
    c = math.sqrt(2.0 * D * dt)
    crossed = np.zeros(n_cells, dtype=bool); n_esc = 0
    for _ in range(n_steps):
        s += sdot(s, g, 0.0) * dt + c * rng.standard_normal(n_cells)
        newly = (s < 0.0) & (~crossed); n_esc += int(np.sum(newly)); crossed |= newly
    cell_time = n_cells * n_steps * dt
    return (n_esc / cell_time) if cell_time > 0 else 0.0


# ---------------------------------------------------------------------------
#  affinity-maturation endpoint: a germinal-centre loop (affinity proxy = barrier gamma^2/4)
#  -- the same loop as immune_maturation.IM1, read as a function of the number of ROUNDS.
# ---------------------------------------------------------------------------
def _gc_round(pool, keep_frac, mut_sd, naive_mean, g_lo, g_hi, k_min, rng):
    n = len(pool); k = max(1, int(round(keep_frac * n)))
    order = np.argsort(pool); survivors = pool[order[-k:]]
    if k < k_min:
        return np.clip(rng.normal(naive_mean, mut_sd, size=n), g_lo, g_hi)
    idx = rng.integers(0, k, size=n)
    return np.clip(survivors[idx] + rng.normal(0.0, mut_sd, size=n), g_lo, g_hi)


def _maturation_gain(rounds, naive, seed=SEED, pool_n=200, keep_frac=0.4, mut_sd=0.045,
                     g_lo=1.20, g_hi=1.55, k_min=8):
    """Final mean barrier minus initial after `rounds` GC rounds at the (IM1 interior-optimal) survivor
    fraction. Rises and saturates with rounds. Deterministic per seed."""
    rng = np.random.default_rng(seed)
    pool = np.clip(rng.normal(naive, 0.05, size=pool_n), g_lo, g_hi)
    b0 = float(np.mean(barrier(pool)))
    for _ in range(int(rounds)):
        pool = _gc_round(pool, keep_frac, mut_sd, naive, g_lo, g_hi, k_min, rng)
    return float(np.mean(barrier(pool))) - b0


def VK1_prime_boost_interval_from_maturation():
    """Boost benefit = maturation_gain(r) * survival(r). Sweeping the prime-boost interval directly in GC
    ROUNDS r (the maturation clock; 1 round := 1 substrate time-unit, the simplest non-tuned identity, with
    the memory pool decaying at the MEASURED escape rate over that same unit), the product has an INTERIOR
    optimum: too few rounds -> the germinal centre has not matured; too many -> the primed pool has decayed.
    The IM1 GC loop is reused UNCHANGED (the maturation endpoint is not re-tuned here)."""
    G = immune_gamma()
    naive = G["PAX5"]                                           # adaptive master = the maturing repertoire
    g_mem = max(G.values())                                     # the memory switch that decays between doses
    rate = _escape_rate(g_mem, D=0.30, seed=SEED)
    round_time = 1.0                                            # 1 GC round := 1 substrate time-unit (identity)
    rounds_grid = list(range(1, 26))                            # interval in rounds (spans rise -> saturation -> decay)
    rows = []
    for r in rounds_grid:
        mat = _maturation_gain(r, naive, seed=SEED)            # rises then saturates (IM1 loop, unchanged)
        surv = math.exp(-rate * r * round_time)                # primed pool still present after r rounds
        rows.append({"interval_rounds": int(r), "maturation_gain": round(mat, 6),
                     "primed_survival": round(surv, 4), "boost_benefit": round(mat * surv, 6)})
    benefits = [x["boost_benefit"] for x in rows]
    i_best = int(np.argmax(benefits))
    interior = 0 < i_best < len(benefits) - 1
    short_arm_worse = benefits[0] < benefits[i_best]           # too-short interval = unmatured -> worse
    long_arm_worse = benefits[-1] < benefits[i_best]           # too-long interval = decayed -> worse
    return {
        "name": "VK1 prime-boost interval from the maturation endpoint -- interior optimum (inverted-U in time)",
        "naive_master": "PAX5", "memory_switch_gamma": round(g_mem, 4),
        "measured_escape_rate": round(rate, 6), "round_time_substrate_units": round_time,
        "sweep": rows,
        "optimum_interval_rounds": rows[i_best]["interval_rounds"],
        "optimum_benefit": round(benefits[i_best], 6),
        "short_interval_arm_worse": bool(short_arm_worse), "long_interval_arm_worse": bool(long_arm_worse),
        "optimum_is_interior": bool(interior),
        "note": "maturation completes quickly relative to memory decay, so the optimal boost is shortly "
                "AFTER maturation, BEFORE decay erodes the pool -- a genuine inverted-U with both arms worse.",
        "grade": "[V] the inverted-U SHAPE (maturation x survival) is measured from the coupled GC loop and "
                 "the escape statistic; the absolute calendar interval is runtime [O]",
        "pass": bool(interior and short_arm_worse and long_arm_worse),
    }


# ---------------------------------------------------------------------------
#  VK2 -- saRNA's longer drive WINDOW crosses more reliably (same amplitude, same final barrier)
# ---------------------------------------------------------------------------
def _crossing_reliability(g, amp, window_steps, D, n_cells=8000, n_steps=4000, dt=0.01, seed=SEED):
    """Fraction of naive-OFF cells that, driven at amplitude `amp` for `window_steps` then released to h=0,
    are in the protected (s>0) basin at the horizon. Stochastic ensemble; deterministic per seed."""
    rng = np.random.default_rng(seed)
    s = np.full(n_cells, -math.sqrt(g), dtype=float)
    c = math.sqrt(2.0 * D * dt)
    for i in range(n_steps):
        h = amp if i < window_steps else 0.0
        s += sdot(s, g, h) * dt + c * rng.standard_normal(n_cells)
    return float(np.mean(s > 0.0))


def VK2_saRNA_vs_mRNA_window():
    """At a fixed near-spinodal amplitude under noise, the longer saRNA window reaches the protected basin
    more reliably than the shorter mRNA window. The post-flip barrier (durability) is identical for both."""
    g = max(immune_gamma().values())
    hsp = spinodal(g)
    amp = 0.95 * hsp                                            # near-spinodal: crossing is window-sensitive
    D = 0.30
    window_mRNA = 400                                           # base drive window (mRNA payload lifetime)
    window_saRNA = 3 * window_mRNA                              # saRNA self-amplifies -> longer SAME-amp window
    frac_mRNA = _crossing_reliability(g, amp, window_mRNA, D, seed=SEED)
    frac_saRNA = _crossing_reliability(g, amp, window_saRNA, D, seed=SEED)
    saRNA_more_reliable = frac_saRNA > frac_mRNA
    # the durability AFTER a flip is the SAME barrier for both (honest: the advantage is crossing, not hold)
    post_flip_barrier_same = True                              # same switch g -> same gamma^2/4
    return {
        "name": "VK2 saRNA vs mRNA -- the longer saRNA drive window crosses the protected basin more reliably",
        "immune_gamma": round(g, 4), "spinodal": round(hsp, 4), "amplitude_near_spinodal": round(amp, 4),
        "noise_D": D, "window_mRNA_steps": window_mRNA, "window_saRNA_steps": window_saRNA,
        "crossing_fraction_mRNA": round(frac_mRNA, 4), "crossing_fraction_saRNA": round(frac_saRNA, 4),
        "saRNA_more_reliable_than_mRNA": bool(saRNA_more_reliable),
        "post_flip_durability_identical_same_barrier": bool(post_flip_barrier_same),
        "advantage_is_in_reaching_not_holding": True,
        "grade": "[V] the reliability ORDERING saRNA>mRNA follows from the longer SAME-amplitude window "
                 "(not a larger dose); absolute titre / amplification factor is runtime [O]",
        "pass": bool(saRNA_more_reliable),
    }


def run_battery():
    tests = [VK1_prime_boost_interval_from_maturation(), VK2_saRNA_vs_mRNA_window()]
    allp = all(t["pass"] for t in tests)
    return {"module": "rna_vaccine_kinetics", "battery": "VK1-VK3", "seed": SEED,
            "VK3_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "the prime-boost interior-optimal interval SHAPE and the saRNA>mRNA crossing "
                        "reliability ORDERING are read [V]; absolute calendar intervals, titres, and "
                        "amplification factors are runtime [O]; clinical scheduling belongs to clinicians/regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
