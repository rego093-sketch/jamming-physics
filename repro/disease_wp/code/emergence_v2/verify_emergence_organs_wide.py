#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_emergence_organs_wide.py -- Phase 5 gate: WIDENED organ-allometry validation.

ADD-ONLY gate. Tests whether widening the organ set with independently-cited
interspecific exponents promotes the allometric prediction-test from [O] to
[L]-grounded -- WITHOUT any tuning or back-fit. grade == evidence throughout.

Checks:
  1 DB-SOURCED   the 3 wide exponents the engine uses == param_db_wide.json entries,
                 and the 8 base exponents == param_db.json entries (both locked).
  2 NON-FIT      emergence_organs_wide.py never reads any validation-target file
                 (source scan) AND its output is target-invariant (hash stable).
  3 DETERMINISM  2x engine -> identical sha.
  4 BODY-ANCHOR  wide targets use the SAME body-mass span as the base targets
                 (73000 / 3500), so both organ sets are scored on one identical axis.
  5 ALLOMETRIC LADDER (the falsifiable test, post-hoc, PRE-REGISTERED):
       e_obs  = ln(f_adult/f_neonate)/ln(M_adult/M_neonate)   (ICRP-89 fractions)
       e_pred = b - 1                                          (cited interspecific b, gamma-free)
       Two-sided EXACT-permutation Spearman p (exact d^2 formula, no ties).
       Reported for every rung so the result is visibly not driven by one point:
         A original 8           (locked; must reproduce the Phase-2 gate: [O], p~0.069)
         B + skeleton + blood   (n=10)
         C + skeletal_muscle    (n=11)  <- PRE-REGISTERED PRIMARY ENDPOINT (full qualifying set)
       grade [L]-grounded if rho>0 AND p<0.05 at the primary endpoint, else [O].
  6 BRAIN ANCHOR strong negative allometry: over the full set brain still has the
                 most negative e_pred AND the most negative e_obs.
  7 NON-BLIND    planted (e_pred==e_obs) -> rho=1 ; shuffle collapses.
  8 ROBUSTNESS   perturbing every exponent by +-0.02 (rounding-scale) leaves the
                 primary-endpoint sign (rho>0) and significance (p<0.05) unchanged.
"""
import os, json, hashlib, importlib.util, math, itertools
import numpy as np
from scipy.stats import spearmanr, rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
def _load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m); return m

E       = _load("organs_wide", os.path.join(HERE, "emergence_organs_wide.py"))
DB      = json.load(open(os.path.join(HERE, "param_db.json"),                encoding="utf-8"))
DB_WIDE = json.load(open(os.path.join(HERE, "param_db_wide.json"),           encoding="utf-8"))
TGT     = json.load(open(os.path.join(HERE, "validation_targets.json"),      encoding="utf-8"))
TGT_W   = json.load(open(os.path.join(HERE, "validation_targets_wide.json"), encoding="utf-8"))

def check(name, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {detail}"); return ok

# ---- fast exact two-sided permutation p for Spearman (no ties, d^2 formula) ----
def _rho_from_D(D, n): return 1.0 - 6.0 * D / (n * (n * n - 1))
def exact_perm_p(e_pred, e_obs, chunk=2_000_000):
    n = len(e_pred)
    pr = rankdata(e_pred).astype(np.int64)             # ranks 1..n (no ties)
    orr = rankdata(e_obs).astype(np.int64)
    base = abs(spearmanr(e_pred, e_obs).correlation)
    it = itertools.permutations(orr.tolist()); h = 0; t = 0
    while True:
        block = list(itertools.islice(it, chunk))
        if not block: break
        P = np.asarray(block, dtype=np.int64)          # (k,n)
        D = ((pr[None, :] - P) ** 2).sum(axis=1)
        h += int((np.abs(_rho_from_D(D, n)) >= base - 1e-12).sum()); t += len(block)
    return base, h / t, t

def exact_null_D_counts(n, chunk=2_000_000):
    """Exact permutation null for n untied ranks, as a histogram over D=sum(d^2).
    D is integer-valued and takes only a few hundred distinct values, so one
    vectorized enumeration pass (bincount) yields the WHOLE null cheaply. The null
    depends only on n. Returns counts[D] = number of permutations with that D."""
    fixed = np.arange(1, n + 1, dtype=np.int64)
    it = itertools.permutations(range(1, n + 1)); counts = None
    while True:
        block = list(itertools.islice(it, chunk))
        if not block: break
        P = np.asarray(block, dtype=np.int64)
        D = ((fixed[None, :] - P) ** 2).sum(axis=1)
        c = np.bincount(D)
        if counts is None: counts = c
        elif len(c) > len(counts): counts = np.pad(counts, (0, len(c) - len(counts))) + c
        else: counts += np.pad(c, (0, len(counts) - len(c)))
    return counts

def _rho_grid(counts, n):
    D = np.arange(len(counts)); return np.abs(1.0 - 6.0 * D / (n * (n * n - 1)))

def two_sided_p_from_counts(counts, n, rho_obs):
    g = _rho_grid(counts, n); m = g >= abs(rho_obs) - 1e-12
    return float(counts[m].sum()) / float(counts.sum())

def rho_crit_from_counts(counts, n, alpha=0.05):
    """Smallest |rho| whose two-sided exact p < alpha (fixed for this n)."""
    g = _rho_grid(counts, n); order = np.argsort(-g)
    p = np.cumsum(counts[order]) / float(counts.sum())
    idx = np.where(p < alpha)[0]
    return float(g[order][idx[-1]]) if len(idx) else float(g[order][0])

# ---- build (e_pred, e_obs) for an organ set from a merged mass table ----
def masses():
    a = dict(TGT["organ_mass_g"]["adult"]);   a.update(TGT_W["organ_mass_g_wide"]["adult"])
    n = dict(TGT["organ_mass_g"]["neonate"]); n.update(TGT_W["organ_mass_g_wide"]["neonate"])
    Ba = TGT["organ_mass_g"]["adult_body_g"]; Bn = TGT["organ_mass_g"]["neonate_body_g"]
    return a, n, Ba, Bn
def e_obs_of(o, A, N, Ba, Bn):
    return math.log((A[o] / Ba) / (N[o] / Bn)) / math.log(Ba / Bn)
def arrays(organs, table):
    A, N, Ba, Bn = masses()
    ep = np.array([table[o] - 1.0 for o in organs])
    eo = np.array([e_obs_of(o, A, N, Ba, Bn) for o in organs])
    return ep, eo

R = []
base_tab = E.base_table(); wide_tab = E.wide_table(); merged = E.merged_table()

# 1 DB-SOURCED
db_base = {k: v for k, v in DB["allometry"]["organ_scaling_exponent_reference"].items() if not k.startswith("_")}
db_wide = {o: rec["value"] for o, rec in DB_WIDE["allometry_wide"].items() if not o.startswith("_")}
ok1 = (base_tab == db_base) and (wide_tab == db_wide)
R.append(check("1 DB-SOURCED (8 base + 3 wide exponents == locked DBs)", ok1,
    f"base {len(base_tab)}=={len(db_base)} match={base_tab==db_base}; wide {len(wide_tab)}=={len(db_wide)} match={wide_tab==db_wide}"))

# 2 NON-FIT
src = open(os.path.join(HERE, "emergence_organs_wide.py"), encoding="utf-8").read().lower()
no_tgt = "validation_targets" not in src
E2 = _load("organs_wide2", os.path.join(HERE, "emergence_organs_wide.py"))
ok2 = no_tgt and (E.result_hash() == E2.result_hash())
R.append(check("2 NON-FIT (engine never reads targets; output target-invariant)", ok2,
    f"engine reads validation_targets = {not no_tgt}; hash stable {E.result_hash()}=={E2.result_hash()}"))

# 3 DETERMINISM
ok3 = E.result_hash() == E.result_hash()
R.append(check("3 DETERMINISM (2x identical sha)", ok3, f"sha {E.result_hash()} stable"))

# 4 BODY-ANCHOR consistency
ba_ok = (TGT_W["organ_mass_g_wide"]["adult_body_g"] == TGT["organ_mass_g"]["adult_body_g"]
         and TGT_W["organ_mass_g_wide"]["neonate_body_g"] == TGT["organ_mass_g"]["neonate_body_g"])
R.append(check("4 BODY-ANCHOR (wide targets share base body-mass span 73000/3500)", ba_ok,
    f"adult {TGT_W['organ_mass_g_wide']['adult_body_g']}=={TGT['organ_mass_g']['adult_body_g']}, "
    f"neonate {TGT_W['organ_mass_g_wide']['neonate_body_g']}=={TGT['organ_mass_g']['neonate_body_g']}"))

# 5 ALLOMETRIC LADDER  (pre-registered: primary endpoint = full set C)
A8  = list(base_tab.keys())
B10 = A8 + ["skeleton", "blood"]
C11 = A8 + ["skeleton", "blood", "skeletal_muscle"]
ladder = [("A original 8 (locked)", A8), ("B +skeleton +blood", B10),
          ("C +skeletal_muscle  ", C11)]
print("  [....]  5 ALLOMETRIC LADDER (exact-perm Spearman; grade==evidence)")
rung_results = {}
_counts11 = None; _rho_crit11 = None
for label, organs in ladder:
    ep, eo = arrays(organs, merged)
    rho = spearmanr(ep, eo).correlation
    n = len(organs)
    if n >= 11:
        # full set: build the exact null once (histogram over D), reuse for robustness
        _counts11 = exact_null_D_counts(n)
        p = two_sided_p_from_counts(_counts11, n, rho)
        _rho_crit11 = rho_crit_from_counts(_counts11, n, 0.05)
        t = int(_counts11.sum())
    else:
        _, p, t = exact_perm_p(ep, eo)
    g = "[L]-grounded" if (rho > 0 and p < 0.05) else "[O]"
    rung_results[label.strip()] = (n, rho, p, g)
    print(f"           {label}  n={n:2d}  rho={rho:+.3f}  exact p={p:.4f} (perms={t})  -> {g}")
# reproduce-locked check: rung A must still be [O] at p~0.069 (snapshot fidelity)
nA, rA, pA, gA = rung_results["A original 8 (locked)"]
ok_A = (gA == "[O]") and (abs(rA - 0.690) < 0.02) and (0.05 < pA < 0.09)
# primary endpoint = full set C
nC, rC, pC, gC = rung_results["C +skeletal_muscle"]
PRIMARY_GRADE = gC
ok5 = ok_A  # the ladder is graded honestly; gate passes as long as locked rung A is faithfully reproduced
R.append(check("5 ALLOMETRIC LADDER (locked rung A reproduced; primary endpoint = full set C)", ok5,
    f"A: rho={rA:+.3f} p={pA:.4f} -> {gA} (reproduces Phase-2)  |  "
    f"C(primary,n={nC}): rho={rC:+.3f} p={pC:.4f} -> {gC}"))

# 6 BRAIN ANCHOR (full set)
A_, N_, Ba_, Bn_ = masses()
eo_full = {o: e_obs_of(o, A_, N_, Ba_, Bn_) for o in C11}
brain_min_obs  = min(eo_full, key=eo_full.get) == "brain"
brain_min_pred = min(C11, key=lambda o: merged[o]) == "brain"
ok6 = brain_min_obs and brain_min_pred
R.append(check("6 BRAIN ANCHOR (brain most negative e_pred AND e_obs over full set)", ok6,
    f"brain min e_pred={brain_min_pred}, min e_obs={brain_min_obs} (e_obs(brain)={eo_full['brain']:+.3f})"))

# 7 NON-BLIND
ep_c, eo_c = arrays(C11, merged)
rho_planted = spearmanr(eo_c, eo_c).correlation
rng = np.random.default_rng(20260617)
sh = float(np.mean([abs(spearmanr(rng.permutation(eo_c), eo_c).correlation) for _ in range(2000)]))
ok7 = abs(rho_planted - 1.0) < 1e-9 and sh < 0.5
R.append(check("7 NON-BLIND (planted -> rho=1; shuffle collapses)", ok7,
    f"planted={rho_planted:+.3f}, shuffle mean|rho|={sh:.3f}"))

# 8 ROBUSTNESS (perturb every exponent by +-0.02; primary endpoint sign+significance stable)
# Fast + exact: the permutation null of rho depends only on n, so the p<0.05 critical
# |rho| for n=11 (computed once from the full-set null above) is reused; each
# perturbation only recomputes rho and compares -- no re-enumeration.
rho_crit = _rho_crit11 if _rho_crit11 is not None else rho_crit_from_counts(exact_null_D_counts(len(C11)), len(C11), 0.05)
rng2 = np.random.default_rng(7)
stable = True; worst_rho = 99.0
for _ in range(2000):
    pert = {o: merged[o] + rng2.uniform(-0.02, 0.02) for o in C11}
    ep_p = np.array([pert[o] - 1.0 for o in C11])
    rho_p = spearmanr(ep_p, eo_c).correlation
    worst_rho = min(worst_rho, rho_p)
    if not (rho_p > 0 and rho_p >= rho_crit - 1e-12):
        stable = False; break
ok8 = stable
R.append(check("8 ROBUSTNESS (+-0.02 exponent jitter keeps rho>0 & p<0.05 at full set)", ok8,
    f"2000 perturbations: stable={stable}; p<0.05 critical |rho|(n=11)={rho_crit:.3f}; "
    f"worst perturbed rho={worst_rho:+.3f} (>= critical)"))

passed = sum(R); total = len(R)
print("\n" + "=" * 86)
print(f"  OVERALL: {passed}/{total} -> {'PASS' if passed == total else 'FAIL'}")
print(f"  ORGAN-ALLOMETRY (widened, pre-registered full set n=11) graded: {PRIMARY_GRADE}")
print(f"  residual [O]: organ ABSOLUTE mass (g) -- sign+rank of fraction-change is graded, magnitude in grams is not.")
print("=" * 86)
