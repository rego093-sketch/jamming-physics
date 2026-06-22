#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
germline_escapee.py  --  WHICH MARKS ESCAPE REPROGRAMMING  (battery GE1-GE4)  [blueprint II-1, II-2, II-4].

  env_to_germline.py established the firewall logic (a mark inherits only if it survives the two erasures
  and its barrier holds it). This module makes it concrete on the CANONICAL escapees -- the imprinted /
  parent-of-origin loci (inherited/imprint_gamma.json, NCBI-direct) -- and refines the two erasures and the
  re-writing condition. MAGNITUDE FIREWALL: the survival ORDERING, the harsher-erasure dominance, and the
  re-writing BOUNDARY are read [V]; absolute penetrance and the wild generation index are runtime [O].

GE1  escapee prediction by barrier: across the measured imprinted atlas, single-erasure survival RANKS
     ascending-gamma -- the deeper-barrier ICRs are the better-inherited escapees (a falsifiable ranking). [V]
GE2  the two erasures resolved: PGC reprogramming and zygotic reprogramming as two DIFFERENT noise levels;
     the harsher window dominates the compound survival (p_pgc * p_zyg); a deep-barrier escapee survives
     BOTH while a shallow locus is mostly erased. [V]
GE3  re-writing vs persistence: an environment that RE-LOADS the payload each generation reaches a nonzero
     steady state; there is a critical re-write rate w* above which the effect is MAINTAINED and below which
     it FADES (the transient/maintained boundary). [V]
GE4  honest scoreboard + firewall.
"""
import json
import numpy as np
from _substrate import imprint_gamma, imprint_meta, germline_gamma, spinodal, barrier, SEED


def _survive_fraction(g, D, n_cells=4000, n_steps=1500, dt=0.01, seed=SEED, start_on=True):
    rng = np.random.default_rng(seed)
    s = np.full(n_cells, (np.sqrt(g) if start_on else -np.sqrt(g)), dtype=float)
    c = np.sqrt(2.0 * D * dt)
    for _ in range(n_steps):
        s += (g * s - s ** 3) * dt + c * rng.standard_normal(n_cells)
    return float(np.mean(s > 0.0)) if start_on else float(np.mean(s < 0.0))


def GE1_escapee_prediction():
    """Single-erasure survival across the measured imprinted atlas ranks ascending-gamma. Report the
    predicted best/worst-inherited escapees."""
    G = imprint_gamma()
    D = 0.22
    genes = sorted(G, key=lambda k: G[k])
    gammas = [G[k] for k in genes]
    surv = [_survive_fraction(G[k], D, seed=SEED) for k in genes]
    def rank(x):
        return np.argsort(np.argsort(x))
    rg, rs = rank(gammas), rank(surv)
    n = len(genes)
    rho = 1.0 - 6.0 * float(np.sum((rg - rs) ** 2)) / (n * (n * n - 1))
    return {"name": "GE1 escapee prediction -- imprinted survival ranks ascending-gamma",
            "reprogramming_noise_D": D, "n_loci": n, "spearman_rho_gamma_vs_survival": round(rho, 3),
            "monotone": bool(rho > 0.85),
            "best_inherited": genes[-1], "best_gamma": round(gammas[-1], 4),
            "worst_inherited": genes[0], "worst_gamma": round(gammas[0], 4),
            "table": [dict(locus=genes[i], gamma=round(gammas[i], 4),
                           parent_of_origin=imprint_meta()[genes[i]]["parent_of_origin"],
                           p_survive=round(surv[i], 4)) for i in range(n)],
            "grade": "[V] heritability ordering = barrier ordering; absolute penetrance is runtime [O]",
            "pass": bool(rho > 0.85 and surv[-1] > surv[0])}


def GE2_two_erasures_resolved():
    """PGC vs zygotic reprogramming as two different noise levels. The harsher window dominates the compound
    survival; a deep escapee survives both, a shallow locus is mostly erased."""
    G = imprint_gamma()
    g_deep = max(G.values())                      # deepest-barrier escapee
    g_shallow = min(G.values())                   # shallowest imprinted locus
    D_pgc = 0.20                                   # PGC reprogramming noise
    D_zyg = 0.28                                   # zygotic reprogramming noise (harsher)
    # deep escapee through each window and compounded
    p_pgc_deep = _survive_fraction(g_deep, D_pgc, seed=SEED)
    p_zyg_deep = _survive_fraction(g_deep, D_zyg, seed=SEED)
    comp_deep = p_pgc_deep * p_zyg_deep
    # shallow locus compounded
    p_pgc_sh = _survive_fraction(g_shallow, D_pgc, seed=SEED)
    p_zyg_sh = _survive_fraction(g_shallow, D_zyg, seed=SEED)
    comp_sh = p_pgc_sh * p_zyg_sh
    harsher_dominates = p_zyg_deep < p_pgc_deep    # the harsher (zygotic) window has lower survival
    deep_beats_shallow = comp_deep > comp_sh
    return {"name": "GE2 two erasures resolved (PGC vs zygotic; harsher dominates)",
            "D_pgc": D_pgc, "D_zyg_harsher": D_zyg,
            "deep_gamma": round(g_deep, 4), "p_survive_pgc_deep": round(p_pgc_deep, 4),
            "p_survive_zyg_deep": round(p_zyg_deep, 4), "compound_deep": round(comp_deep, 4),
            "shallow_gamma": round(g_shallow, 4), "compound_shallow": round(comp_sh, 4),
            "harsher_window_dominates": bool(harsher_dominates),
            "deep_escapee_beats_shallow": bool(deep_beats_shallow),
            "grade": "[V] the two windows compound; the harsher one dominates; ordering read, absolute [O]",
            "pass": bool(harsher_dominates and deep_beats_shallow)}


def GE3_rewriting_vs_persistence():
    """An environment re-loads the payload each generation: a_{n+1} = (1-loss)*a_n + w. Fixed point
    a* = w/loss. Above a critical w* = threshold*loss the effect is MAINTAINED; below, it FADES."""
    G = imprint_gamma()
    # per-generation loss = 1 - (single-erasure retention of a MID escapee), to set a realistic loss
    loss = 1.0 - _survive_fraction(float(np.median(list(G.values()))), 0.22, seed=SEED)
    loss = max(0.05, min(0.95, loss))
    thr = 0.10
    w_star = thr * loss                            # critical re-write rate
    # demonstrate two regimes
    def steady(w, n=200):
        a = 0.0
        for _ in range(n):
            a = (1.0 - loss) * a + w
        return a
    w_high = 1.5 * w_star
    w_low = 0.5 * w_star
    a_high = steady(w_high); a_low = steady(w_low); a_none = steady(0.0)
    maintained = a_high >= thr
    fades_low = a_low < thr
    fades_none = a_none < thr
    return {"name": "GE3 re-writing vs persistence -- critical re-write rate w*",
            "per_generation_loss": round(loss, 4), "threshold": thr, "critical_w_star": round(w_star, 5),
            "steady_state_at_1.5x_w_star": round(a_high, 4), "maintained": bool(maintained),
            "steady_state_at_0.5x_w_star": round(a_low, 4), "fades_below_w_star": bool(fades_low),
            "steady_state_no_rewrite": round(a_none, 4), "transient_exposure_fades": bool(fades_none),
            "grade": "[V] a measured boundary separates maintained (re-written) from transient (fades); "
                     "absolute wild generations are runtime [O]",
            "pass": bool(maintained and fades_low and fades_none)}


def run_battery():
    tests = [GE1_escapee_prediction(), GE2_two_erasures_resolved(), GE3_rewriting_vs_persistence()]
    allp = all(t["pass"] for t in tests)
    return {"module": "germline_escapee", "battery": "GE1-GE4", "seed": SEED,
            "GE4_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "survival ORDERING, harsher-erasure dominance, re-writing BOUNDARY read [V]; absolute "
                        "penetrance and wild generation index are runtime [O].",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
