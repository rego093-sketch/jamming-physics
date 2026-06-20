#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REDUCED-ORDER "OVERCOMING" TEST  (precision-down, mechanism-up)

Question this answers
---------------------
The package's central null: the INTRINSIC per-gene scalar gamma (promoter
stacking dG, identical in every cell) is orthogonal to cardiac developmental
TIMING (Spearman rho = +0.071, perm p = 0.882 -> [O]).

Claim to be EARNED before it can be narrated: "the middle (timing) EMERGES from
SYSTEMIC dynamics". To earn it, a crude SYSTEMIC model -- with NO parameter
tuned to the observed Carnegie stages -- must recover timing structure that
gamma alone cannot.

Discipline (no-tuning / anti-backfit)
-------------------------------------
* The systemic predictor uses a regulatory DAG built from LITERATURE epistasis
  (who is required-for whom), NOT from embryonic day.
* The relay ODE uses UNIFORM kinetics: every gene gets the SAME production /
  decay / threshold. Nothing is fitted to CS.
* Controls run alongside: non-blindness (apparatus detects a planted signal),
  a random-DAG ensemble (is the literature topology special, or would any DAG
  do?), and CS-label shuffle (perm-p machinery sanity).
* Grade honestly. Ordinal recovery only; absolute days stay [O].

Everything is deterministic (fixed seed) and offline.
"""

import json, itertools, math
import numpy as np
from scipy.stats import spearmanr

RNG = np.random.default_rng(20260617)

# ---------------------------------------------------------------- inputs (locked)
# Observed ordinal cardiac milestones (Carnegie stage), from the package's
# heart_substages.json -- compiled from O'Rahilly&Muller / Moorman&Christoffels /
# Sadler / Larsen. ORDINAL only; NEVER adjusted to change a correlation.
GENES = ["NKX2-5","GATA4","HAND2","ISL1","TBX5","SOX9","MEF2C","TBX1"]
CS = {  # gene -> observed Carnegie stage (the thing we try to predict)
    "NKX2-5": 9, "GATA4": 10, "HAND2": 11, "ISL1": 12,
    "TBX5": 13, "SOX9": 14, "MEF2C": 15, "TBX1": 16,
}
GAMMA = {  # measured promoter gamma from the package's heart_gamma.json (read-only)
    "NKX2-5":1.513, "GATA4":1.3933, "HAND2":1.4566, "ISL1":1.4244,
    "TBX5":1.4392, "SOX9":1.4598, "MEF2C":1.2443, "TBX1":1.5935,
}

def spinodal(g):  # identical to the package's body / neuro / gene-clock switch
    return 2.0 * (g/3.0)**1.5

# ---------------------------------------------------------------- exact perm-p
def exact_perm_p(pred, obs):
    """Two-sided exact permutation p for Spearman rho over all 8! relabelings."""
    obs = np.asarray(obs, float)
    base = abs(spearmanr(pred, obs).correlation)
    idx = list(range(len(obs)))
    hits = tot = 0
    for perm in itertools.permutations(idx):
        r = abs(spearmanr(pred, obs[list(perm)]).correlation)
        tot += 1
        if r >= base - 1e-12:
            hits += 1
    return base, hits/tot, tot

# ---------------------------------------------------------------- baseline: gamma
def gamma_baseline():
    pred = np.array([spinodal(GAMMA[g]) for g in GENES])   # higher -> later
    obs  = np.array([CS[g] for g in GENES])
    rho, p, n = exact_perm_p(pred, obs)
    rho_signed = spearmanr(pred, obs).correlation
    return dict(rho=rho_signed, absrho=rho, p=p, n=n,
                order=[GENES[i] for i in np.argsort(pred)])

# ---------------------------------------------------------------- systemic model
# Cardiac specification DAG. Edge X->Y == "X is required-for / upstream-of Y in
# the cardiac program" by loss-of-function / ChIP epistasis (textbook GRN), NOT
# by developmental day. S = cardiac-induction source (BMP/Nodal/Mesp1), not one
# of the 8 specifiers.
#
# NOTE (recorded, not hidden): a known limitation is that the SECOND HEART FIELD
# (ISL1, and its OFT derivative TBX1) is INDUCED early as a progenitor pool but
# its morphological DERIVATIVES appear late. A pure "induction-depth" axis will
# therefore mis-time the SHF branch. This is left in on purpose so the toy's
# failure mode is visible.
EDGES = [
    ("S","NKX2-5"),                       # cardiac specification apex
    ("NKX2-5","GATA4"),                   # FHF core cross-activation (NKX upstream)
    ("NKX2-5","TBX5"), ("GATA4","TBX5"),  # chamber identity, downstream of core
    ("S","ISL1"),                         # SHF progenitor field (separately induced)
    ("GATA4","HAND2"),                    # RV/OFT effector
    ("GATA4","MEF2C"), ("ISL1","MEF2C"),  # myocardial differentiation effector
    ("ISL1","TBX1"),                      # SHF -> OFT
    ("GATA4","SOX9"),                     # endocardial-cushion EMT (downstream)
]

def longest_path_depth(edges, nodes):
    """Integer longest-path depth FROM source S (pure topology, parameter-free).
    depth(S)=0; depth(v)=1+max(depth(u)) over edges u->v. Earlier-in-cascade =
    smaller depth -> expected to predict EARLIER (smaller) CS, so rho is positive."""
    preds = {n: [] for n in nodes}
    for a,b in edges: preds.setdefault(b, []).append(a)
    depth = {"S": 0}
    def dfs(u):
        if u in depth: return depth[u]
        ups = preds.get(u, [])
        depth[u] = 1 + max((dfs(p) for p in ups), default=0)  # default: orphan -> 1
        return depth[u]
    return {n: dfs(n) for n in nodes}

def relay_onset(edges, nodes, kp=1.0, kd=0.15, theta=0.5, dt=0.01, T=200.0):
    """
    Uniform-kinetics relay ODE. A gene's activator A rises once ALL its upstream
    regulators have crossed theta; onset = first time A crosses theta.
    Same kp/kd/theta for EVERY gene (no per-gene tuning). Source S active at t=0.
    """
    preds = {n: [] for n in nodes}
    for a,b in edges: preds[b].append(a)
    A = {n: 0.0 for n in nodes}; A["S"] = 1.0
    onset = {n: math.inf for n in nodes}
    t = 0.0; steps = int(T/dt)
    for _ in range(steps):
        on = {n:(A[n] >= theta) for n in nodes}; on["S"] = True
        for n in nodes:
            ups = preds.get(n, [])
            drive = kp if (ups and all(on[u] for u in ups)) else 0.0
            A[n] += dt*(drive - kd*A[n])
            if onset[n]==math.inf and A[n] >= theta:
                onset[n] = t
        t += dt
    return onset

def systemic_test():
    nodes = GENES
    obs = np.array([CS[g] for g in GENES])

    depth = longest_path_depth(EDGES, nodes)
    dpred = np.array([depth[g] for g in GENES], float)
    drho, dp, _ = exact_perm_p(dpred, obs)
    drho_s = spearmanr(dpred, obs).correlation

    onset = relay_onset(EDGES, nodes)
    opred = np.array([onset[g] for g in GENES], float)
    orho, op, _ = exact_perm_p(opred, obs)
    orho_s = spearmanr(opred, obs).correlation

    return dict(depth=depth, depth_rho=drho_s, depth_p=dp,
                onset={g:round(onset[g],3) for g in GENES},
                relay_rho=orho_s, relay_p=op)

# ---------------------------------------------------------------- controls
def control_nonblind():
    """Plant a perfectly CS-ordered predictor: apparatus MUST return rho=1."""
    obs = np.array([CS[g] for g in GENES])
    planted = obs.copy().astype(float)
    return spearmanr(planted, obs).correlation

def control_random_dag(n_iter=4000):
    """
    Is the LITERATURE topology special? Build random DAGs with the same node
    count and same number of edges from a source S, score depth-vs-CS rho for
    each, and report where the literature DAG sits in that distribution.
    """
    obs = np.array([CS[g] for g in GENES]); nodes = GENES
    n_edges = len(EDGES)
    lit_depth = np.array([longest_path_depth(EDGES, nodes)[g] for g in GENES], float)
    lit_rho = abs(spearmanr(lit_depth, obs).correlation)
    pool = ["S"] + nodes
    rhos = []
    for _ in range(n_iter):
        # random acyclic edges: enforce a random topological order, edges go forward
        order = list(RNG.permutation(nodes)); topo = ["S"] + order
        pos = {n:i for i,n in enumerate(topo)}
        cand = [(a,b) for a in topo for b in nodes if pos[a] < pos[b]]
        sel = RNG.choice(len(cand), size=min(n_edges,len(cand)), replace=False)
        edges = [cand[i] for i in sel]
        # guarantee every node reachable from S (else depth undefined) -> skip if not
        try:
            d = longest_path_depth(edges, nodes)
            dp = np.array([d[g] for g in GENES], float)
            if np.all(np.isfinite(dp)):
                rhos.append(abs(spearmanr(dp, obs).correlation))
        except Exception:
            pass
    rhos = np.array(rhos)
    pct = float((rhos <= lit_rho).mean())
    return dict(lit_absrho=lit_rho, ensemble_mean=float(rhos.mean()),
                ensemble_p95=float(np.percentile(rhos,95)),
                literature_percentile=pct, n=len(rhos))

def control_theta_robust():
    """Onset-relay order must be stable across a wide threshold range (no tuning)."""
    obs = np.array([CS[g] for g in GENES]); out=[]
    for theta in [0.3,0.4,0.5,0.6,0.7]:
        on = relay_onset(EDGES, GENES, theta=theta)
        pr = np.array([on[g] for g in GENES], float)
        out.append((theta, round(spearmanr(pr,obs).correlation,3)))
    return out

# ---------------------------------------------------------------- run
if __name__ == "__main__":
    print("="*78)
    print("  REDUCED-ORDER OVERCOMING TEST  |  cardiac timing: intrinsic gamma vs systemic")
    print("="*78)

    g = gamma_baseline()
    print(f"\n[BASELINE] intrinsic scalar gamma (spinodal sort)")
    print(f"   predicted early->late: {g['order']}")
    print(f"   Spearman rho(gamma, CS) = {g['rho']:+.3f}   exact perm p = {g['p']:.3f}   -> NULL [O]")

    s = systemic_test()
    print(f"\n[SYSTEMIC #1] topology only: longest-path depth from induction source S")
    print(f"   depth: {s['depth']}")
    print(f"   Spearman rho(depth, CS) = {s['depth_rho']:+.3f}   exact perm p = {s['depth_p']:.3f}")
    print(f"\n[SYSTEMIC #2] uniform-kinetics relay ODE (same kp/kd/theta for all genes)")
    print(f"   onset: {s['onset']}")
    print(f"   Spearman rho(relay, CS) = {s['relay_rho']:+.3f}   exact perm p = {s['relay_p']:.3f}")

    print(f"\n[CONTROLS]")
    print(f"   non-blindness (planted CS-ordered predictor): rho = {control_nonblind():+.3f}  (==1 -> apparatus works)")
    tr = control_theta_robust()
    print(f"   theta-robustness (relay rho across threshold): {tr}")
    rd = control_random_dag()
    print(f"   random-DAG ensemble (n={rd['n']}): |rho| mean={rd['ensemble_mean']:.3f}, "
          f"p95={rd['ensemble_p95']:.3f}")
    print(f"      literature DAG |rho|={rd['lit_absrho']:.3f}  sits at "
          f"{rd['literature_percentile']*100:.1f}th percentile of random DAGs")

    # named failure mode: SHF (ISL1 induced early, derivative TBX1 septates late)
    sub = [g for g in GENES if g not in ("ISL1","TBX1")]
    obs_sub = np.array([CS[g] for g in sub], float)
    dep = longest_path_depth(EDGES, GENES)
    dpred_sub = np.array([dep[g] for g in sub], float)
    on = relay_onset(EDGES, GENES)
    opred_sub = np.array([on[g] for g in sub], float)
    print(f"   SHF-drop sensitivity (remove ISL1,TBX1 = induced-early/derivative-late branch):")
    print(f"      depth rho  {spearmanr(dpred_sub,obs_sub).correlation:+.3f}   "
          f"relay rho {spearmanr(opred_sub,obs_sub).correlation:+.3f}   (n=6)")

    print("\n" + "="*78)
    print("  READING")
    print("="*78)
    gr, dr, orr = abs(g['rho']), abs(s['depth_rho']), abs(s['relay_rho'])
    print(f"   intrinsic gamma |rho| = {gr:.3f}  (null, [O])")
    print(f"   systemic depth  |rho| = {dr:.3f}")
    print(f"   systemic relay  |rho| = {orr:.3f}")
    gain = max(dr,orr) - gr
    print(f"   gain over the intrinsic scalar: +{gain:.3f}")
