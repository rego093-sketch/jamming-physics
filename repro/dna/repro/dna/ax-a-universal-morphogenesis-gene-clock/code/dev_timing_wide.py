"""
dev_timing_wide.py -- v7 NEXT#2: WIDEN THE FEATURE TABLE BEYOND n=7 (lift the power floor).

HANDOFF v7. v5 (dev_timing.py) established an HONEST NULL -- measured promoter-stiffness gamma does
NOT predict Carnegie first-appearance staging for 7 [V]-master features -- and v6 (timing_predictors.py)
widened that null from "stiffness" to "proximal-promoter COMPOSITION" (gamma, GC, CpG o/e, TATA/GC-box/
CAAT density), every predictor [O], with an exact-permutation FLOOR of p=0.00079 at n=7. The HANDOFF
named the binding next step explicitly: n=7 is too small -- the floor is the power ceiling, and the one
moderately positive composition trend (cpg_oe/tata/caat) never gets a fair test. So v7 does exactly one
thing: it ADDS three more genuine [V]-master features (n -> 10), re-runs BOTH the gamma/spinodal test and
the v6 composition battery on the wider table, and reports whatever comes out -- never tuned.

THE THREE NEW FEATURES (each pinned from a primary source BEFORE any correlation, data/dev_timing_ext.json):
    FOXG1  -> future cerebral hemispheres (cerebral vesicle)  CS14   (Muller&O'Rahilly 1988, PMID 3377191)
    MITF   -> retinal pigment epithelium, first melanisation  CS15   (O'Rahilly&Muller; PMID 1927245)
    SOX9   -> first chondrification (cartilage)               CS17   (O'Rahilly&Muller Publ.637)
All three master genes are already in the locked morpho_gamma.json table; MITF/SOX9 promoter sequences are
COPIED BYTE-FOR-BYTE from morpho_promoters.cache.json (they recompute the locked gamma EXACTLY, delta=0),
FOXG1 was re-fetched once by the identical pipeline and frozen (reproduces the locked gamma within assembly
drift, |dgamma|=2e-4). Two scope corrections are documented, not silent: FOXG1 and SOX9 are tagged [F] in
the BROAD atlas (where they stand in for vague multi-feature programs), but for the SPECIFIC features here
("future cerebral hemispheres", "first chondrification") they are the canonical [V] masters. (FOXG1 is
literally the gene in the title of the CS14 staging paper.)

THE n=10 EXACT-PERMUTATION ENGINE (the technical heart of v7):
    At n=7 the apparatus brute-forced all 7!=5040 label permutations through scipy per predictor. At n=10
    that is 10!=3,628,800 per predictor x 6 predictors -- too slow that way. KEY FACT: under the exact
    permutation null, Spearman rho is an AFFINE function of S = sum_i rank_x[i]*rank_y[perm][i] (a=rank of
    predictor, b=rank of stage), so for any predictor with DISTINCT values (rank_x a permutation of 1..n)
    the null distribution of rho depends ONLY on the stage-rank multiset and n. We therefore compute the
    exact null distribution of S ONCE, by dynamic programming over the (tiny) multiset of remaining stage
    ranks, and reuse it for every predictor + the floor. Ties in a predictor (e.g. equal motif counts) are
    handled by giving that predictor its own rank multiset in the SAME DP. Ranks are scaled x2 so midranks
    are integers and the DP keys are exact integers; rho is recovered from S by the exact affine map. This
    DP is validated against the v5 brute-force oracle (DT._perm_p) at n=7,8 and against a vectorised oracle
    at n=9 IN THE GATE, before it is trusted at n=10 -- no unproven fast path.

THE RESULT (computed below, reported whatever it is): widening to n=10 drops the exact-permutation floor
from 7.9e-4 to ~2.2e-6, so Bonferroni significance is now amply reachable -- the test finally HAS power.
Whatever the rho/p then are for gamma/spinodal and for the composition battery, they are reported and
graded by the evidence ([V] iff Bonferroni perm p < alpha AND rho>0, else [O]); nothing is adjusted.

stdlib + numpy + scipy. Deterministic (pure arithmetic over frozen tables + frozen sequences).
"""
import os, json, math, hashlib, itertools
from collections import Counter
import numpy as np
from scipy import stats

import gene_clock as GC
import dev_timing as DT             # locked 7-feature loader, V_MASTERS, brute-force oracle _perm_p
import timing_predictors as TP      # composition_predictors, MOTIFS, locked gamma/GC, _revcomp

HERE = os.path.dirname(os.path.abspath(__file__))
EXT_JSON = os.path.join(HERE, "data", "dev_timing_ext.json")               # 3 NEW locked stages
EXT_CACHE = os.path.join(HERE, "data", "dev_timing_ext_promoters.cache.json")  # 3 NEW sequences
TIMING_CACHE = os.path.join(HERE, "data", "timing_promoters.cache.json")   # original 7 sequences

PREDICTOR_ORDER = ["gamma", "gc", "cpg_oe", "tata", "gcbox", "caat"]

# the new feature set adds two genuine [V] master->feature links that the BROAD atlas tags [F]
# (FOXG1=telencephalon, SOX9=chondrogenesis). Documented in dev_timing_ext.json _scope_note.
V_MASTERS_WIDE = set(DT.V_MASTERS) | {"FOXG1", "SOX9"}


# ===================================================================== exact-permutation engine
def _exact_S_distribution(a_scaled, b_scaled):
    """Exact distribution of S = sum_i a_sorted[i] * b_perm[i] over ALL n! permutations of b.

    a_scaled, b_scaled: integer arrays (ranks x2). Returns {S:int -> count:int}. Tied b-values are
    counted WITH multiplicity (each of the n! orderings weighted equally), so sum(count) == n! -- this
    is what an exact permutation test requires. DP state = counts of remaining distinct b-values; the
    per-state dict maps a partial S to the number of ways to reach it. Deterministic, exact (integers).
    """
    a = sorted(int(v) for v in a_scaled)            # fix a ascending; permuting b covers all bijections
    cnt = Counter(int(v) for v in b_scaled)
    vals = sorted(cnt)
    dp = {tuple(cnt[v] for v in vals): {0: 1}}
    for i in range(len(a)):
        ai = a[i]
        new = {}
        for state, sdict in dp.items():
            for vi, v in enumerate(vals):
                c = state[vi]
                if c == 0:
                    continue
                ns = list(state); ns[vi] -= 1; ns = tuple(ns)
                add = ai * v
                tgt = new.setdefault(ns, {})
                for s, w in sdict.items():
                    tgt[s + add] = tgt.get(s + add, 0) + w * c   # x c : tied copies are distinguishable
        dp = new
    (final_state, dist), = dp.items()
    assert all(c == 0 for c in final_state)
    return dist


def _rank_consts(x, stages):
    rx = stats.rankdata(x, method="average")
    ry = stats.rankdata(stages, method="average")
    return rx, ry, float(rx.mean()), float(ry.mean()), float(rx.std()), float(ry.std())


def perm_p_exact(x, stages):
    """Exact two-sided permutation p-value P(|rho| >= |rho_obs|) via the DP null of S.

    Matches DT._perm_p semantics exactly (same '>= |rho_obs| - 1e-12' rule), but in O(DP) not O(n!).
    Returns (p, n_perm). Degenerate (zero-variance) predictor -> (nan, 0). rho_obs is computed by the
    SAME affine map used for the null (and asserted equal to scipy.spearmanr to 1e-9), so the boundary
    is exact.
    """
    n = len(x)
    rx, ry, abar, bbar, sa, sb = _rank_consts(x, stages)
    if sa == 0.0 or sb == 0.0:
        return float("nan"), 0
    a2 = (2 * rx).round().astype(int)
    b2 = (2 * ry).round().astype(int)

    def rho_of_S(S):                                # S is the REAL sum_i rank_x*rank_y for that pairing
        return (S / n - abar * bbar) / (sa * sb)

    rho_obs = rho_of_S(float(np.dot(rx, ry)))
    rho_sp = stats.spearmanr(x, stages).statistic
    assert abs(rho_obs - rho_sp) < 1e-9, (rho_obs, rho_sp)

    dist = _exact_S_distribution(a2, b2)
    tot = sum(dist.values())
    assert tot == math.factorial(n), (tot, math.factorial(n))
    thr = abs(rho_obs) - 1e-12
    n_ge = sum(c for S4, c in dist.items() if abs(rho_of_S(S4 / 4.0)) >= thr)   # S4 = 4*real S
    return n_ge / tot, tot


def permutation_floor(stages):
    """Smallest exact-permutation p ANY continuous (tie-free) predictor could reach at this n, given
    the ties in `stages`. Uses the strictly-monotone synthetic predictor (ranks 1..n) and the same DP.
    Returns (max_abs_rho_achievable, floor_p, n_perm). Deterministic."""
    n = len(stages)
    mono = np.arange(1, n + 1, dtype=float)
    rx, ry, abar, bbar, sa, sb = _rank_consts(mono, stages)
    a2 = (2 * rx).round().astype(int)
    b2 = (2 * ry).round().astype(int)
    rho = lambda S: (S / n - abar * bbar) / (sa * sb)
    dist = _exact_S_distribution(a2, b2)
    tot = sum(dist.values())
    rhos = {S4: abs(rho(S4 / 4.0)) for S4 in dist}
    best = max(rhos.values())
    n_at_best = sum(dist[S4] for S4, r in rhos.items() if r >= best - 1e-12)
    return float(best), n_at_best / tot, tot


def _vectorised_perm_p(x, stages):
    """Independent oracle for the gate's n=9 cross-check: every permutation at once via numpy (affine
    map, no DP, no scipy-per-perm). Only used to VALIDATE perm_p_exact at brute-forceable n; never on
    the n=10 claim path."""
    n = len(x)
    rx, ry, abar, bbar, sa, sb = _rank_consts(x, stages)
    if sa == 0.0 or sb == 0.0:
        return float("nan")
    M = np.array(list(itertools.permutations(ry)), dtype=float)     # (n!, n)
    rho = (M @ rx / n - abar * bbar) / (sa * sb)
    rho_obs = (float(np.dot(rx, ry)) / n - abar * bbar) / (sa * sb)
    return float(np.mean(np.abs(rho) >= abs(rho_obs) - 1e-12))


# ===================================================================== load the wide (n=10) inputs
def load_ext_features(path=None):
    """The 3 NEW locked features only: [(name, gene, stage_int), ...] in file order."""
    J = json.load(open(path or EXT_JSON, encoding="utf-8"))
    return [(name, d["gene"], int(d["stage_cs"])) for name, d in J["features"].items()], J


def load_wide_features():
    """The full n=10 feature list = original 7 (loaded byte-for-byte from dev_timing.json, UNCHANGED)
    followed by the 3 new (dev_timing_ext.json). Returns [(name, gene, stage), ...]."""
    orig, _, _ = DT.load_dev_timing()                # the locked 7 -- never edited
    ext, _ = load_ext_features()
    return list(orig) + list(ext)


def ext_table_sha256(path=None):
    p = path or EXT_JSON
    blob = json.dumps(json.load(open(p, encoding="utf-8")), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def ext_cache_sha256(path=None):
    p = path or EXT_CACHE
    blob = json.dumps(json.load(open(p, encoding="utf-8")), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def load_wide_sequences():
    """Promoter sequences for all 10 master genes: original 7 from timing_promoters.cache.json,
    new 3 from dev_timing_ext_promoters.cache.json. Returns {gene: seq}."""
    a = json.load(open(TIMING_CACHE, encoding="utf-8"))["genes"]
    b = json.load(open(EXT_CACHE, encoding="utf-8"))["genes"]
    seqs = {g: d["seq"] for g, d in a.items()}
    seqs.update({g: d["seq"] for g, d in b.items()})
    return seqs


# ===================================================================== build the predictor matrix
def build_predictor_matrix():
    """(rows, preds): rows=[(feature, gene, stage)] for the n=10 set; preds={name: np.array aligned}.
    gamma/GC read VERBATIM from the locked morpho_gamma.json; cpg_oe/tata/gcbox/caat computed from the
    frozen sequences with the FIXED a-priori motifs (TP.MOTIFS, TP.composition_predictors)."""
    rows = load_wide_features()
    genes = [g for _, g, _ in rows]
    locked = TP.load_locked_gamma_gc()
    seqs = load_wide_sequences()
    preds = {"gamma": np.array([locked[g][0] for g in genes], float),
             "gc":    np.array([locked[g][1] for g in genes], float)}
    comp = {g: TP.composition_predictors(seqs[g]) for g in genes}
    for name in ("cpg_oe", "tata", "gcbox", "caat"):
        preds[name] = np.array([comp[g][name] for g in genes], float)
    return rows, preds


# ===================================================================== test 1: gamma/spinodal (n=10)
def calibrate_gamma(alpha=0.05):
    """The dev_timing test, widened to n=10: corr(spinodal(measured gamma), observed CS), exact perm-p
    via the DP engine. Graded by evidence ([V] iff perm_p<alpha and rho>0, else [O])."""
    rows = load_wide_features()
    gammas, _ = GC.load_gamma_table()
    sp = np.array([GC.spinodal(gammas[g]) for _, g, _ in rows], float)
    cs = np.array([s for _, _, s in rows], float)
    rho = float(stats.spearmanr(sp, cs).statistic)
    p_rho = float(stats.spearmanr(sp, cs).pvalue)
    r = float(stats.pearsonr(sp, cs).statistic)
    perm_p, n_perm = perm_p_exact(sp, cs)
    validated = bool((perm_p < alpha) and (rho > 0))
    return dict(
        n_features=len(rows),
        features=[dict(feature=f, gene=g, gamma=float(gammas[g]),
                       spinodal=float(GC.spinodal(gammas[g])), observed_cs=int(s))
                  for f, g, s in rows],
        spearman_rho=rho, spearman_p=p_rho, pearson_r=r,
        permutation_p=float(perm_p), n_permutations=int(n_perm),
        timing_validated=validated, grade="[V]" if validated else "[O]",
    )


# ===================================================================== test 2: composition battery (n=10)
def calibrate_battery(alpha=0.05):
    """The v6 predictor battery widened to n=10 (gamma, gc, cpg_oe, tata, gcbox, caat), Bonferroni
    K=6, exact perm-p via the DP engine, exact-permutation floor disclosed. Each predictor graded by
    its own evidence."""
    rows, preds = build_predictor_matrix()
    stages = np.array([s for _, _, s in rows], float)
    K = len(PREDICTOR_ORDER)
    alpha_bonf = alpha / K
    max_abs_rho_floor, floor_p, n_perm = permutation_floor(stages)

    results = []
    for name in PREDICTOR_ORDER:
        x = preds[name]
        if np.allclose(x, x[0]):
            results.append(dict(predictor=name, spearman_rho=float("nan"), perm_p=float("nan"),
                                perm_p_bonf=float("nan"), positive=False, validated=False,
                                grade="[O]", note="degenerate (zero variance) -- not testable"))
            continue
        rho = float(stats.spearmanr(x, stages).statistic)
        perm_p, _ = perm_p_exact(x, stages)
        perm_p_bonf = min(1.0, perm_p * K)
        positive = bool(rho > 0)
        validated = bool((perm_p_bonf < alpha) and positive)
        results.append(dict(predictor=name, values=[float(v) for v in x], spearman_rho=rho,
                            perm_p=float(perm_p), perm_p_bonf=float(perm_p_bonf),
                            positive=positive, validated=validated,
                            grade="[V]" if validated else "[O]"))

    any_validated = any(r["validated"] for r in results)
    return dict(
        n_features=len(rows), K_predictors=K, alpha=alpha, alpha_bonferroni=alpha_bonf,
        features=[dict(feature=f, gene=g, observed_cs=int(s)) for f, g, s in rows],
        predictor_order=PREDICTOR_ORDER, results=results,
        any_predictor_validated=any_validated,
        overall_grade=("[V]" if any_validated else "[O]"),
        permutation_floor=dict(max_abs_rho_achievable=float(max_abs_rho_floor), floor_p=float(floor_p),
                               n_permutations=int(n_perm), bonferroni_alpha=alpha_bonf,
                               floor_reachable_under_bonferroni=bool(floor_p < alpha_bonf),
                               note=("smallest exact-permutation p any tie-free predictor could reach "
                                     "at this n; if >= bonferroni_alpha NO predictor can be significant "
                                     "regardless of biology (pure power ceiling).")),
        motif_consensus={k: dict(motif=v, revcomp=TP._revcomp(v)) for k, v in TP.MOTIFS.items()},
    )


# ===================================================================== falsifiability self-checks
def apparatus_detects_signal():
    """Non-blindness at n=10: a synthetic predictor comonotone with the stages scores |rho|->1 with a
    small perm_p, a shuffle does not. Proves the null below is a TRUE null, not a dead test."""
    rows = load_wide_features()
    cs = np.array([s for _, _, s in rows], float)
    rho_perfect = float(stats.spearmanr(cs, cs).statistic)
    p_perfect, _ = perm_p_exact(cs + 0.0, cs)
    rng = np.random.default_rng(0)
    cs_shuf = cs.copy(); rng.shuffle(cs_shuf)
    rho_shuf = float(stats.spearmanr(cs, cs_shuf).statistic)
    ok = bool((abs(rho_perfect) > 0.999) and (p_perfect < 0.05) and (abs(rho_shuf) < 0.95))
    return ok, dict(rho_perfect=rho_perfect, perm_p_perfect=float(p_perfect), rho_shuffled=rho_shuf)


def dp_matches_bruteforce():
    """VALIDATE the DP exact-permutation engine before it is trusted at n=10. At n=7 and n=8 the DP is
    checked against the v5 brute-force oracle (DT._perm_p, scipy per permutation); at n=9 against an
    independent vectorised oracle (itself cross-checked against scipy-brute at n=7). Each n is probed
    with a deterministic mix of distinct-valued and tied predictors. Returns (ok, detail)."""
    rng = np.random.default_rng(7)
    cases = []
    ok = True

    # n=7 and n=8 vs scipy brute-force oracle (fast at these n)
    for st in ([9, 10, 12, 13, 13, 17, 18], [9, 10, 12, 13, 13, 15, 17, 17]):
        n = len(st)
        probes = [rng.random(n),                      # distinct-valued
                  rng.random(n),                      # distinct-valued
                  np.round(rng.random(n), 1)]         # 1-dp rounding -> likely tied predictor
        for x in probes:
            p_dp, _ = perm_p_exact(x, st)
            p_bf, _ = DT._perm_p(np.asarray(x, float), np.asarray(st, float), abs(stats.spearmanr(x, st).statistic))
            match = abs(p_dp - p_bf) < 1e-12
            ok = ok and match
            cases.append(dict(n=n, oracle="scipy_brute", p_dp=round(p_dp, 9), p_oracle=round(p_bf, 9), match=match))

    # n=9 vs vectorised oracle
    st9 = [9, 10, 12, 13, 13, 14, 15, 17, 17]
    for x in [rng.random(9), np.round(rng.random(9), 1)]:
        p_dp, _ = perm_p_exact(x, st9)
        p_vec = _vectorised_perm_p(x, st9)
        match = abs(p_dp - p_vec) < 1e-12
        ok = ok and match
        cases.append(dict(n=9, oracle="vectorised", p_dp=round(p_dp, 9), p_oracle=round(p_vec, 9), match=match))

    # cross-check the vectorised oracle itself against scipy-brute at n=7
    st7 = [9, 10, 12, 13, 13, 17, 18]; xv = rng.random(7)
    p_vec = _vectorised_perm_p(xv, st7)
    p_bf, _ = DT._perm_p(xv, np.asarray(st7, float), abs(stats.spearmanr(xv, st7).statistic))
    vec_ok = abs(p_vec - p_bf) < 1e-12
    ok = ok and vec_ok
    cases.append(dict(n=7, oracle="vec_vs_scipy", p_dp=round(p_vec, 9), p_oracle=round(p_bf, 9), match=vec_ok))
    return ok, dict(cases=cases)


def original_seven_unchanged():
    """The original 7 features here must be byte-for-byte the locked dev_timing.json ones (gene+stage),
    and the wide stage vector must be exactly the 7 locked stages followed by the 3 ext stages."""
    orig, _, _ = DT.load_dev_timing()
    wide = load_wide_features()
    head_ok = (list(wide[:7]) == list(orig))
    ext, _ = load_ext_features()
    tail_ok = (list(wide[7:]) == list(ext))
    masters_ok = all(g in V_MASTERS_WIDE for _, g, _ in wide)
    ints_ok = all(isinstance(s, int) for _, _, s in wide)
    ok = bool(head_ok and tail_ok and masters_ok and ints_ok)
    return ok, dict(original7_identical=head_ok, ext3_appended=tail_ok,
                    all_V_masters=masters_ok, integer_stages=ints_ok,
                    stage_vector=[s for _, _, s in wide])


def ext_inputs_reproduce_locked_gamma(tol=5e-3):
    """The 3 new master genes' frozen sequences must reproduce the LOCKED morpho_gamma.json gamma/gc:
    MITF/SOX9 (byte-for-byte cached) EXACTLY (residual 0); FOXG1 (re-fetched) within assembly drift.
    Also asserts MITF/SOX9 sequences are byte-identical to morpho_promoters.cache.json. Recomputes
    gamma from the frozen sequence with the SantaLucia NN table (identical to fetch_morpho_gamma.py)."""
    NN = {"AA": -1.00, "TT": -1.00, "AT": -0.88, "TA": -0.58, "CA": -1.45, "TG": -1.45,
          "GT": -1.44, "AC": -1.44, "CT": -1.28, "AG": -1.28, "GA": -1.30, "TC": -1.30,
          "CG": -2.17, "GC": -2.24, "GG": -1.84, "CC": -1.84}
    locked = TP.load_locked_gamma_gc()
    seqs = json.load(open(EXT_CACHE, encoding="utf-8"))["genes"]
    morpho = json.load(open(os.path.join(HERE, "data", "morpho_promoters.cache.json")))

    def gamma_gc(seq):
        steps = [-NN[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN]
        g = round(float(np.mean(steps)), 4)
        gc = round((seq.count("G") + seq.count("C")) / len(seq), 4)
        return g, gc

    rows = []; ok = True
    for g in ("MITF", "SOX9", "FOXG1"):
        seq = seqs[g]["seq"]
        rg, rgc = gamma_gc(seq)
        lg, lgc = locked[g][0], locked[g][1]
        resid = abs(rg - lg)
        copied = g in ("MITF", "SOX9")
        byte_id = (seq == morpho[g]["seq"]) if copied else None
        # copied genes must be EXACT (resid 0 and byte-identical); fetched within tol
        good = ((resid == 0.0 and byte_id) if copied else (resid <= tol))
        ok = ok and bool(good)
        rows.append(dict(gene=g, kind=("copied" if copied else "refetched"),
                         recomputed_gamma=rg, locked_gamma=lg, residual=round(resid, 6),
                         recomputed_gc=rgc, locked_gc=lgc, byte_identical=byte_id,
                         within_tol=bool(resid <= tol)))
    return ok, dict(tol=tol, genes=rows)


# ===================================================================== write + report
def calibrate():
    """Full v7 result: both tests + all falsifiability self-checks. Deterministic."""
    gam = calibrate_gamma()
    bat = calibrate_battery()
    det_ok, det = apparatus_detects_signal()
    dp_ok, dp = dp_matches_bruteforce()
    o7_ok, o7 = original_seven_unchanged()
    ext_ok, ext = ext_inputs_reproduce_locked_gamma()
    return dict(
        n_features=gam["n_features"],
        gamma_spinodal_test=gam,
        composition_battery=bat,
        timing_sha256=DT.timing_table_sha256(),         # locked 7-stage pin (== dev_timing's)
        ext_sha256=ext_table_sha256(),                  # locked 3-stage pin
        ext_cache_sha256=ext_cache_sha256(),
        falsifiability=dict(
            apparatus_detects_signal=dict(ok=det_ok, **det),
            dp_matches_bruteforce=dict(ok=dp_ok, **dp),
            original_seven_unchanged=dict(ok=o7_ok, **o7),
            ext_inputs_reproduce_locked_gamma=dict(ok=ext_ok, **ext),
        ),
    )


def write_results():
    res = calibrate()
    out = os.path.join(HERE, "..", "results", "dev_timing_wide.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=2)
    return res, out


def _fmt(res):
    g = res["gamma_spinodal_test"]; b = res["composition_battery"]
    L = []
    L.append("=" * 80)
    L.append("  DEVELOPMENTAL-TIMING WIDE TEST  (v7 #2: widen the feature table to n=10)")
    L.append("  measured promoter quantities  vs  locked Carnegie first-appearance staging")
    L.append("=" * 80)
    L.append(f"  {'feature':24s} {'gene':6s} {'gamma':>7s} {'spinodal':>9s} {'obs_CS':>6s}")
    for f in g["features"]:
        L.append(f"  {f['feature']:24s} {f['gene']:6s} {f['gamma']:7.4f} "
                 f"{f['spinodal']:9.5f} {f['observed_cs']:6d}")
    L.append("-" * 80)
    L.append(f"  [test 1] gamma/spinodal: Spearman rho = {g['spearman_rho']:+.4f}  "
             f"(exact perm p = {g['permutation_p']:.5f}, n!={g['n_permutations']:,}); grade {g['grade']}")
    fl = b["permutation_floor"]
    L.append(f"  exact-permutation FLOOR at n={b['n_features']}: smallest reachable p = {fl['floor_p']:.2e}"
             f"  (was 7.9e-4 at n=7) -> Bonferroni significance "
             f"{'IS' if fl['floor_reachable_under_bonferroni'] else 'is NOT'} reachable")
    L.append(f"  [test 2] composition battery (K={b['K_predictors']}, Bonferroni alpha={b['alpha_bonferroni']:.5f}):")
    L.append(f"  {'predictor':10s} {'rho':>8s} {'perm_p':>9s} {'perm_p*K':>9s} {'pos?':>5s}  grade")
    for r in b["results"]:
        rho = r["spearman_rho"]; pp = r["perm_p"]; ppb = r["perm_p_bonf"]
        rho_s = "  nan  " if rho != rho else f"{rho:+.4f}"
        pp_s = "  nan  " if pp != pp else f"{pp:.5f}"
        ppb_s = "  nan  " if ppb != ppb else f"{ppb:.5f}"
        L.append(f"  {r['predictor']:10s} {rho_s:>8s} {pp_s:>9s} {ppb_s:>9s} {str(r['positive']):>5s}  {r['grade']}")
    L.append("-" * 80)
    v1 = "PREDICTS timing (earned [V])" if g["timing_validated"] else "does NOT predict timing -> [O]"
    v2 = ("at least one composition predictor PREDICTS timing (earned [V])"
          if b["any_predictor_validated"] else
          "NO measured promoter quantity predicts Carnegie staging -> overall [O]")
    L.append(f"  VERDICT(gamma/spinodal): {v1}")
    L.append(f"  VERDICT(composition)   : {v2}")
    L.append(f"  (honest result, reported not tuned; the floor shows the test now HAS power)")
    fa = res["falsifiability"]
    L.append(f"  self-checks: detects_signal={fa['apparatus_detects_signal']['ok']}  "
             f"DP==bruteforce={fa['dp_matches_bruteforce']['ok']}  "
             f"orig7_unchanged={fa['original_seven_unchanged']['ok']}  "
             f"ext_reproduces_gamma={fa['ext_inputs_reproduce_locked_gamma']['ok']}")
    L.append("=" * 80)
    return "\n".join(L)


if __name__ == "__main__":
    res, out = write_results()
    print(_fmt(res))
    print(f"\n  wrote {out}")
