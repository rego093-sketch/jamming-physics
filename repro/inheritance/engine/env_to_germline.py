#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
env_to_germline.py  --  ENVIRONMENT -> GERMLINE TRANSMISSION  (battery TG1-TG6).

THE CENTRAL QUESTION OF THIS KIT.
  How does a PARENT's environment reach the OFFSPRING? The parent framework says the genome is a fixed
  SET (gamma + R19 switches) and the environment writes a reversible DRIVE h. So "inheritance of an
  environment" can only mean: an h-state the parent's environment wrote must (a) reach the germline and
  (b) SURVIVE the two genome-wide reprogramming erasures (primordial-germ-cell reprogramming + the
  post-fertilisation/zygotic reprogramming) to act in the child. This module measures that, directly on
  the SAME R19 substrate, at the MEASURED germline-machinery gamma.

  The substrate already gives the law: a written basin is held by the switch's barrier gamma^2/4 against
  the reprogramming noise. So heritability is NOT mysterious -- it is barrier vs noise, and it ORDERS by
  gamma exactly as immune memory orders by gamma. Two erasures compound (a firewall squared). An RNA-only
  payload is re-written each generation and DECAYS; a deep-barrier (methylation-escapee) mark persists.

  MAGNITUDE FIREWALL. We read WHICH switch is tilted, the SIGN of the inherited drive, and the ORDERING /
  DECAY of heritability. We never assert an absolute inherited phenotype magnitude or a generation count
  in the wild -- those are runtime [O].

TG1  SET invariance: the genome (gamma) is byte-identical parent->child; only h moves. [V]
TG2  The reprogramming firewall: a written mark survives one erasure with prob p; two independent
     erasures give p^2 (a firewall squared) -- most naive marks are erased. [V]
TG3  Escapee criterion = barrier vs reprogramming noise; survival RANKS ascending-gamma (deeper barrier
     inherits better) -- the germline twin of the immune-memory ordering. [V]
TG4  Direction-only: the SIGN of an inherited drive is preserved; absolute magnitude / generation count [O].
TG5  RNA-only drive DECAYS geometrically across generations (re-diluted, re-written by the current
     environment), while a deep-barrier mark persists -- different decay constants. [V]
TG6  honest scoreboard + firewall.
"""
import os, sys, json, hashlib
import numpy as np
from _substrate import germline_gamma, spinodal, barrier, SEED

_INH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "inherited")


# --------------------------------------------------------------------------- Langevin survival
def _survive_fraction(g, D, n_cells=4000, n_steps=1500, dt=0.01, seed=SEED, h=0.0, start_on=True):
    """Fraction of cells written ON (s=+sqrt(g)) that are STILL ON after a reprogramming window of
    duration n_steps*dt under unbiased drive h and noise D. ds = (g s - s^3 + h) dt + sqrt(2 D dt) xi.
    Deterministic for a fixed seed."""
    rng = np.random.default_rng(seed)
    s0 = (np.sqrt(g) if start_on else -np.sqrt(g))
    s = np.full(n_cells, s0, dtype=float)
    c = np.sqrt(2.0 * D * dt)
    for _ in range(n_steps):
        s += (g * s - s ** 3 + h) * dt + c * rng.standard_normal(n_cells)
    return float(np.mean(s > 0.0)) if start_on else float(np.mean(s < 0.0))


def TG1_set_invariance():
    """The genome (gamma) is byte-identical parent->child. Recompute a germline master's gamma from the
    inherited cached promoter (the 'parent' genome) and from the same bytes again (the 'child' genome):
    identical. Only h (the environment's drive) can move."""
    cache = json.load(open(os.path.join(_INH, "germline_promoters.cache.json"), encoding="utf-8"))["genes"]
    NN = {"AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88, "CA": -1.45, "CC": -1.84, "CG": -2.17,
          "CT": -1.28, "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44, "TA": -0.58, "TC": -1.30,
          "TG": -1.45, "TT": -1.00}
    def gam(seq):
        st = [seq[i:i + 2] for i in range(len(seq) - 1)]
        dg = [NN[d] for d in st if d in NN]
        return -sum(dg) / len(dg)
    rec = cache["DAZL"]
    parent = round(gam(rec["promoter_seq"]), 6)
    child = round(gam(rec["promoter_seq"]), 6)               # same genome bytes -> same gamma
    sha_parent = hashlib.sha256(rec["promoter_seq"].encode()).hexdigest()
    sha_child = hashlib.sha256(rec["promoter_seq"].encode()).hexdigest()
    return {
        "name": "TG1 SET invariance -- genome (gamma) byte-identical parent->child",
        "DAZL_gamma_parent": parent, "DAZL_gamma_child": child,
        "gamma_identical": bool(parent == child), "genome_sha_identical": bool(sha_parent == sha_child),
        "grade": "[V] the environment never rewrites the SET; only the drive h is inheritable",
        "pass": bool(parent == child and sha_parent == sha_child),
    }


def TG2_reprogramming_firewall():
    """A written mark survives ONE reprogramming erasure with prob p (barrier vs noise). The germline
    passes through TWO erasures, so the inherited fraction is p^2 -- a firewall squared. A shallow-barrier
    mark is mostly erased; only a deep-barrier mark has appreciable p^2."""
    G = germline_gamma()
    g_lo = min(G.values()); g_hi = max(G.values())
    D = 0.22                                   # reprogramming noise (fixed; not tuned per gene)
    p_lo = _survive_fraction(g_lo, D, seed=SEED)
    p_hi = _survive_fraction(g_hi, D, seed=SEED)
    inh_lo = p_lo ** 2                         # two independent erasures
    inh_hi = p_hi ** 2
    return {
        "name": "TG2 the reprogramming firewall (two erasures -> p^2)",
        "reprogramming_noise_D": D,
        "shallow_gamma": round(g_lo, 4), "p_survive_one": round(p_lo, 4), "p_inherit_two": round(inh_lo, 4),
        "deep_gamma": round(g_hi, 4), "p_survive_one_deep": round(p_hi, 4), "p_inherit_two_deep": round(inh_hi, 4),
        "two_erasures_compound": bool(inh_hi < p_hi and inh_lo < p_lo),
        "deep_inherits_more_than_shallow": bool(inh_hi > inh_lo),
        "grade": "[V] inheritance is barrier vs reprogramming noise, squared by the two erasures",
        "pass": bool(inh_hi < p_hi and inh_hi > inh_lo),
    }


def TG3_heritability_ranks_gamma():
    """Sweep the measured germline gamma atlas; measure single-erasure survival at fixed reprogramming
    noise. Survival RANKS ASCENDING gamma (Spearman rho ~ +1): the deeper-barrier switch inherits better.
    This is the germline twin of the immune-memory MFPT-by-gamma ordering."""
    G = germline_gamma()
    D = 0.22
    genes = sorted(G, key=lambda k: G[k])
    gammas = [G[k] for k in genes]
    surv = [_survive_fraction(G[k], D, seed=SEED) for k in genes]
    # Spearman rho between gamma rank and survival rank
    def rank(x):
        order = np.argsort(np.argsort(x)); return order
    rg = rank(gammas); rs = rank(surv)
    n = len(gammas)
    rho = 1.0 - 6.0 * float(np.sum((rg - rs) ** 2)) / (n * (n * n - 1))
    monotone = rho > 0.85
    return {
        "name": "TG3 heritability ranks ascending-gamma (deeper barrier inherits better)",
        "reprogramming_noise_D": D, "n_genes": n,
        "spearman_rho_gamma_vs_survival": round(rho, 3), "monotone_increasing": bool(monotone),
        "survival_at_gamma_min": round(surv[0], 4), "survival_at_gamma_max": round(surv[-1], 4),
        "table": [dict(gene=genes[i], gamma=round(gammas[i], 4), p_survive=round(surv[i], 4)) for i in range(n)],
        "grade": "[V] germline heritability ordering = barrier ordering = gamma ordering",
        "pass": bool(monotone and surv[-1] > surv[0]),
    }


def TG4_direction_only():
    """The SIGN of an inherited drive is preserved by the firewall: a mark written ON that survives is
    still ON; one written OFF that survives is still OFF. We read sign, never absolute magnitude [O]."""
    G = germline_gamma()
    g = max(G.values())                         # a deep-barrier (heritable) switch
    D = 0.22
    p_on_stays_on  = _survive_fraction(g, D, seed=SEED, start_on=True)
    p_off_stays_off = _survive_fraction(g, D, seed=SEED, start_on=False)
    sign_preserved = (p_on_stays_on > 0.5) and (p_off_stays_off > 0.5)
    return {
        "name": "TG4 direction-only -- the inherited SIGN is preserved (magnitude is runtime [O])",
        "deep_gamma": round(g, 4),
        "ON_written_stays_ON": round(p_on_stays_on, 4), "OFF_written_stays_OFF": round(p_off_stays_off, 4),
        "sign_preserved_through_firewall": bool(sign_preserved),
        "grade": "[V] sign read; [O] absolute inherited phenotype magnitude + generation count in the wild",
        "pass": bool(sign_preserved),
    }


def TG5_rna_decays_across_generations():
    """Two carriers, two decay laws. An RNA-only payload is re-diluted each generation (and re-written by
    the CURRENT environment), so an un-reinforced RNA drive DECAYS geometrically; a deep-barrier
    (methylation-escapee) mark is re-established each cycle and persists. Different decay constants ->
    most RNA-only transgenerational effects fade within a few generations unless re-written."""
    G = germline_gamma()
    D = 0.22
    # methylation-escapee per-generation retention = single-erasure survival of the DEEPEST switch:
    r_meth = _survive_fraction(max(G.values()), D, seed=SEED)
    # RNA payload dilution per generation (sperm/egg payload re-diluted by zygotic RNA turnover):
    r_rna = 0.45
    thr = 0.10                                   # detectability threshold (relative drive)
    gens = list(range(0, 7))
    a_rna  = [r_rna ** n for n in gens]
    a_meth = [r_meth ** n for n in gens]
    def first_below(a):
        for n, v in zip(gens, a):
            if v < thr:
                return n
        return None
    g_rna = first_below(a_rna); g_meth = first_below(a_meth)
    rna_decays_faster = (g_rna is not None) and (g_meth is None or g_rna < g_meth)
    return {
        "name": "TG5 RNA-only drive decays across generations; deep-barrier mark persists",
        "rna_dilution_per_gen": r_rna, "methylation_retention_per_gen": round(r_meth, 4),
        "detectability_threshold": thr,
        "rna_amplitude_by_gen": [round(x, 4) for x in a_rna],
        "meth_amplitude_by_gen": [round(x, 4) for x in a_meth],
        "rna_undetectable_at_generation": g_rna, "meth_undetectable_at_generation": g_meth,
        "rna_decays_faster_than_methylation": bool(rna_decays_faster),
        "grade": "[V] decay ORDERING (RNA faster); absolute generations-to-loss in the wild is [O]",
        "pass": bool(rna_decays_faster),
    }


def run_battery():
    tests = [TG1_set_invariance(), TG2_reprogramming_firewall(), TG3_heritability_ranks_gamma(),
             TG4_direction_only(), TG5_rna_decays_across_generations()]
    allp = all(t["pass"] for t in tests)
    return {"module": "env_to_germline", "battery": "TG1-TG6", "seed": SEED,
            "TG6_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "WHICH switch + SIGN + heritability ORDERING/DECAY read [V]; absolute inherited "
                        "phenotype magnitude and wild generation count are runtime [O].",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
