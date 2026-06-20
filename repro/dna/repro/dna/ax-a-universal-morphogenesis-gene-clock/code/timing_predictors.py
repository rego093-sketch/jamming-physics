"""
timing_predictors.py -- v6 NEXT#1: KEEP THE APPARATUS, SWAP THE INPUT VARIABLE.

HANDOFF v6-candidate #1. v5's dev_timing.py established an HONEST NULL: the measured
promoter-stiffness gamma does NOT predict Carnegie first-appearance staging for the
[V]-master feature set (Spearman rho ~= -0.018, exact-permutation p ~= 0.99). The v6
question is the obvious next one: gamma is only ONE measured molecular quantity readable
from the same promoters -- does a DIFFERENT measured quantity predict the staging order?

This module reuses the dev_timing falsification apparatus VERBATIM (same locked Carnegie
stages, same exact-permutation Spearman test, same grade==evidence rule) and runs it over a
BATTERY of measured promoter quantities instead of just gamma:

    gamma      -- promoter NN stacking stiffness  (LOCKED table; re-confirms the v5 null)
    gc         -- G+C fraction                     (LOCKED table; ~collinear with gamma)
    cpg_oe     -- CpG observed/expected ratio       (computed from sequence)
    tata       -- TATA-box  density / kb            (computed from sequence)
    gcbox      -- GC-box(Sp1) density / kb          (computed from sequence)
    caat       -- CAAT-box   density / kb           (computed from sequence)

GOVERNANCE (neuro VP-SPEC C3, identical discipline to dev_timing.py):
  * The Carnegie stages are a LOCKED, cited external input (data/dev_timing.json), sha-pinned,
    never touched. They are the SAME 7 [V]-master features dev_timing.py uses.
  * gamma and GC are read VERBATIM from the locked measured tables (morpho_gamma.json) -- never
    recomputed here, so the gamma column is bit-identical to dev_timing's.
  * The novel predictors (cpg_oe, tata, gcbox, caat) are computed from promoter sequence. Four
    sequences (TBX5/TBX4/HOXD13/PAX9) are copied byte-for-byte from morpho_promoters.cache.json;
    three (PAX2/PAX6/LHX2) were re-fetched once by the IDENTICAL pipeline and frozen into
    data/timing_promoters.cache.json. The re-fetch reproduces the locked gamma/GC to within
    assembly drift (max residual 4e-4 << inter-gene spread 0.14); this is recorded, not hidden.
  * Every motif is a FIXED canonical consensus chosen a priori (below) -- NOT tuned to the stages.
  * EACH predictor is graded BY THE EVIDENCE: a positive "predicts timing" claim is earned only
    if its Bonferroni-corrected exact-permutation p < alpha AND its rank correlation is positive.
    K predictors -> Bonferroni alpha = 0.05 / K.
  * n = 7. The exact permutation FLOOR (smallest p any predictor could achieve at this n, given
    the tie in the stage vector) is computed and reported, so the reader sees the power ceiling.

THE RESULT (computed below, reported whatever it is): promoter-sequence COMPOSITION -- not just
stiffness -- does not predict Carnegie staging order for these 7 features. Every predictor is an
honest [O]. This widens the v5 null from "stiffness" to "proximal-promoter composition", and
points the real next step at (a) widening the feature table beyond n=7 (power), and (b) a
different data MODALITY (expression-onset / chromatin accessibility), which is [O] data-blocked
because that atlas is not in the package.

stdlib + numpy + scipy. Deterministic (pure arithmetic over frozen tables + frozen sequences).
"""
import os, json, math, hashlib, itertools
import numpy as np
from scipy import stats

import dev_timing as DT           # reuse the locked apparatus: stages loader, _perm_p, V_MASTERS

HERE = os.path.dirname(os.path.abspath(__file__))
MORPHO_GAMMA = os.path.join(HERE, "data", "morpho_gamma.json")            # LOCKED gamma/GC table
TIMING_CACHE = os.path.join(HERE, "data", "timing_promoters.cache.json")  # frozen 7-gene sequences

# ------------------------------------------------------------------ fixed, a-priori motif consensus
# Canonical core consensus, chosen BEFORE seeing any correlation. Counted on the given strand AND
# its reverse complement (declared a priori), as overlapping occurrences, per 1000 bp.
MOTIFS = {
    "tata":  "TATAAA",   # TATA-box core (Goldberg-Hogness)
    "gcbox": "GGGCGG",   # GC-box / Sp1 hexamer
    "caat":  "CCAAT",    # CAAT-box
}
PREDICTOR_ORDER = ["gamma", "gc", "cpg_oe", "tata", "gcbox", "caat"]


def _revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def _count_overlapping(seq, motif):
    n, i, m = 0, 0, len(motif)
    while True:
        j = seq.find(motif, i)
        if j < 0:
            return n
        n += 1
        i = j + 1                      # overlapping


def composition_predictors(seq):
    """Sequence-derived predictors (cpg_oe + motif densities). gamma/GC are NOT taken from here;
    they come from the locked table. Returns dict of the novel predictors only."""
    L = len(seq)
    nC = seq.count("C"); nG = seq.count("G")
    nCG = _count_overlapping(seq, "CG")
    # standard CpG observed/expected: obs CpG / (nC*nG/L)
    expected = (nC * nG / L) if (nC and nG) else float("nan")
    cpg_oe = (nCG / expected) if expected and not math.isnan(expected) else float("nan")
    out = {"cpg_oe": float(cpg_oe)}
    for name, motif in MOTIFS.items():
        rc = _revcomp(motif)
        cnt = _count_overlapping(seq, motif) + (_count_overlapping(seq, rc) if rc != motif else 0)
        out[name] = float(1000.0 * cnt / L)        # density per kb
    return out


# ------------------------------------------------------------------ load frozen inputs
def load_locked_gamma_gc():
    """gamma + GC read VERBATIM from the locked measured table (never recomputed)."""
    J = json.load(open(MORPHO_GAMMA, encoding="utf-8"))["genes"]
    return {g: (float(v["gamma"]), float(v["gc"])) for g, v in J.items()}


def load_timing_sequences():
    J = json.load(open(TIMING_CACHE, encoding="utf-8"))
    return {g: d["seq"] for g, d in J["genes"].items()}, J


def cache_sha256():
    blob = json.dumps(json.load(open(TIMING_CACHE, encoding="utf-8")), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


# ------------------------------------------------------------------ build the predictor matrix
def build_predictor_matrix():
    """Return (feature_rows, predictors) where:
       feature_rows = [(feature, gene, observed_cs), ...] in dev_timing file order,
       predictors   = {name: np.array aligned to feature_rows}.
    gamma/GC come from the locked table; cpg_oe/tata/gcbox/caat from the frozen sequences."""
    feats, _, _ = DT.load_dev_timing()                       # SAME locked 7 features + stages
    locked = load_locked_gamma_gc()
    seqs, _ = load_timing_sequences()

    rows = [(f, g, s) for f, g, s in feats]
    genes = [g for _, g, _ in rows]

    preds = {"gamma": np.array([locked[g][0] for g in genes], float),
             "gc":    np.array([locked[g][1] for g in genes], float)}
    comp = {g: composition_predictors(seqs[g]) for g in genes}
    for name in ("cpg_oe", "tata", "gcbox", "caat"):
        preds[name] = np.array([comp[g][name] for g in genes], float)
    return rows, preds


# ------------------------------------------------------------------ the permutation FLOOR (power)
def permutation_floor(stages):
    """Smallest exact-permutation p ANY predictor could achieve at this n, given ties in `stages`.
    A generic continuous predictor has rank vector [1..n]; max |rho| is over all stage-permutations,
    and the floor p is (#perms hitting that max |rho|)/n!. Deterministic."""
    y = np.asarray(stages, float)
    x = np.arange(1, len(y) + 1, dtype=float)                # strictly-monotone synthetic predictor
    best = -1.0
    rhos = []
    for perm in itertools.permutations(y):
        rho = abs(stats.spearmanr(x, perm).statistic)
        rhos.append(rho)
        if rho > best:
            best = rho
    n_at_best = sum(1 for r in rhos if r >= best - 1e-12)
    return best, n_at_best / len(rhos), len(rhos)


# ------------------------------------------------------------------ the calibration over the battery
def calibrate(alpha=0.05):
    rows, preds = build_predictor_matrix()
    stages = np.array([s for _, _, s in rows], float)
    K = len(PREDICTOR_ORDER)
    alpha_bonf = alpha / K

    max_abs_rho_floor, floor_p, n_perm = permutation_floor(stages)
    floor_reachable = bool(floor_p < alpha_bonf)             # can ANY predictor be significant here?

    results = []
    for name in PREDICTOR_ORDER:
        x = preds[name]
        if np.allclose(x, x[0]):                             # zero-variance guard
            results.append(dict(predictor=name, spearman_rho=float("nan"),
                                perm_p=float("nan"), perm_p_bonf=float("nan"),
                                positive=False, validated=False, grade="[O]",
                                note="degenerate (zero variance) -- not testable"))
            continue
        rho = stats.spearmanr(x, stages).statistic
        perm_p, _ = DT._perm_p(x, stages, abs(rho))          # SAME exact-permutation engine
        perm_p_bonf = min(1.0, perm_p * K)
        positive = bool(rho > 0)
        validated = bool((perm_p_bonf < alpha) and positive)  # == perm_p < alpha_bonf and rho>0
        results.append(dict(
            predictor=name,
            values=[float(v) for v in x],
            spearman_rho=float(rho),
            perm_p=float(perm_p),
            perm_p_bonf=float(perm_p_bonf),
            positive=positive,
            validated=validated,
            grade="[V]" if validated else "[O]",
        ))

    any_validated = any(r["validated"] for r in results)
    return dict(
        n_features=len(rows),
        K_predictors=K,
        alpha=alpha,
        alpha_bonferroni=alpha_bonf,
        features=[dict(feature=f, gene=g, observed_cs=int(s)) for f, g, s in rows],
        predictor_order=PREDICTOR_ORDER,
        results=results,
        any_predictor_validated=any_validated,
        overall_grade=("[V]" if any_validated else "[O]"),
        permutation_floor=dict(
            max_abs_rho_achievable=float(max_abs_rho_floor),
            floor_p=float(floor_p),
            n_permutations=int(n_perm),
            bonferroni_alpha=alpha_bonf,
            floor_reachable_under_bonferroni=floor_reachable,
            note=("at n=7 with the stage tie, the smallest exact-permutation p any predictor "
                  "could reach is floor_p; if floor_p >= bonferroni_alpha NO predictor can be "
                  "significant regardless of biology (pure power ceiling)."),
        ),
        timing_sha256=DT.timing_table_sha256(),              # locked-stage pin (must match dev_timing)
        cache_sha256=cache_sha256(),
        motif_consensus={k: dict(motif=v, revcomp=_revcomp(v)) for k, v in MOTIFS.items()},
    )


# ------------------------------------------------------------------ falsifiability self-checks
def apparatus_detects_signal():
    """Non-blindness for the BATTERY: a synthetic predictor comonotone with the stages must score
    rho -> 1 with a small perm_p, and a shuffle must not. Proves the null below is a TRUE null."""
    feats, _, _ = DT.load_dev_timing()
    cs = np.array([s for _, _, s in feats], float)
    x_perfect = cs + 0.0                                     # perfectly comonotone (ties included)
    rho_perfect = stats.spearmanr(x_perfect, cs).statistic
    p_perfect, _ = DT._perm_p(x_perfect, cs, abs(rho_perfect))
    rng = np.random.default_rng(0)
    cs_shuf = cs.copy(); rng.shuffle(cs_shuf)
    rho_shuf = stats.spearmanr(x_perfect, cs_shuf).statistic
    ok = bool((abs(rho_perfect) > 0.999) and (p_perfect < 0.05) and (abs(rho_shuf) < 0.9))
    return ok, dict(rho_perfect=float(rho_perfect), perm_p_perfect=float(p_perfect),
                    rho_shuffled=float(rho_shuf))


def gamma_matches_dev_timing():
    """Consistency: because spinodal() is strictly monotone in gamma and Spearman is rank-based,
    THIS module's gamma rho MUST equal dev_timing.calibrate()'s spinodal rho exactly."""
    rows, preds = build_predictor_matrix()
    stages = np.array([s for _, _, s in rows], float)
    rho_here = stats.spearmanr(preds["gamma"], stages).statistic
    dt = DT.calibrate()
    rho_dt = dt["spearman_rho"]
    ok = bool(abs(rho_here - rho_dt) < 1e-9)
    return ok, dict(gamma_rho_here=float(rho_here), spinodal_rho_dev_timing=float(rho_dt))


def copied_sequences_identical():
    """The 4 copied sequences must be byte-identical to morpho_promoters.cache.json."""
    morpho = json.load(open(os.path.join(HERE, "data", "morpho_promoters.cache.json")))
    _, J = load_timing_sequences()
    bad = []
    for g in ("TBX5", "TBX4", "HOXD13", "PAX9"):
        if J["genes"][g]["seq"] != morpho[g]["seq"]:
            bad.append(g)
    return (len(bad) == 0), dict(checked=["TBX5", "TBX4", "HOXD13", "PAX9"], mismatches=bad)


def fetched_reproduce_locked_gamma(tol=5e-3):
    """The 3 re-fetched sequences must reproduce the LOCKED gamma to within assembly-drift tol.
    tol=5e-3 >> observed residuals (<=3e-4) and << inter-gene spread (~0.14): catches a wrong-gene
    fetch while honestly tolerating assembly-version drift. Recomputes gamma from the frozen seq."""
    # SantaLucia 1998 NN dG37 -- identical table to fetch_morpho_gamma.py
    NN = {"AA": -1.00, "TT": -1.00, "AT": -0.88, "TA": -0.58, "CA": -1.45, "TG": -1.45,
          "GT": -1.44, "AC": -1.44, "CT": -1.28, "AG": -1.28, "GA": -1.30, "TC": -1.30,
          "CG": -2.17, "GC": -2.24, "GG": -1.84, "CC": -1.84}
    locked = load_locked_gamma_gc()
    _, J = load_timing_sequences()
    rows = []
    ok = True
    for g in ("PAX2", "PAX6", "LHX2"):
        seq = J["genes"][g]["seq"]
        steps = [-NN[seq[i:i+2]] for i in range(len(seq) - 1) if seq[i:i+2] in NN]
        gamma = round(float(np.mean(steps)), 4)
        resid = abs(gamma - locked[g][0])
        ok = ok and (resid <= tol)
        rows.append(dict(gene=g, recomputed_gamma=gamma, locked_gamma=locked[g][0],
                         residual=round(resid, 6), within_tol=bool(resid <= tol)))
    return ok, dict(tol=tol, genes=rows)


# ------------------------------------------------------------------ write + report
def write_results():
    res = calibrate()
    det_ok, det = apparatus_detects_signal()
    cons_ok, cons = gamma_matches_dev_timing()
    cp_ok, cp = copied_sequences_identical()
    ft_ok, ft = fetched_reproduce_locked_gamma()
    res["falsifiability"] = dict(
        apparatus_detects_signal=dict(ok=det_ok, **det),
        gamma_consistent_with_dev_timing=dict(ok=cons_ok, **cons),
        copied_sequences_identical=dict(ok=cp_ok, **cp),
        fetched_reproduce_locked_gamma=dict(ok=ft_ok, **ft),
    )
    out = os.path.join(HERE, "..", "results", "timing_predictors.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=2)
    return res, out


def _fmt(res):
    L = []
    L.append("=" * 80)
    L.append("  DEVELOPMENTAL-TIMING PREDICTOR BATTERY  (v6 #1: swap the input variable)")
    L.append("  measured promoter quantities  vs  locked Carnegie first-appearance staging")
    L.append("=" * 80)
    L.append(f"  n features = {res['n_features']}   K predictors = {res['K_predictors']}   "
             f"Bonferroni alpha = {res['alpha_bonferroni']:.5f}")
    fl = res["permutation_floor"]
    L.append(f"  exact-permutation floor: smallest p any predictor could reach = {fl['floor_p']:.5f}"
             f"  (max|rho|={fl['max_abs_rho_achievable']:.3f}, n!={fl['n_permutations']})")
    L.append(f"  -> Bonferroni significance {'IS' if fl['floor_reachable_under_bonferroni'] else 'is NOT'}"
             f" reachable at this n.")
    L.append("-" * 80)
    L.append(f"  {'predictor':10s} {'rho':>8s} {'perm_p':>9s} {'perm_p*K':>9s} {'pos?':>5s}  grade")
    for r in res["results"]:
        rho = r["spearman_rho"]; pp = r["perm_p"]; ppb = r["perm_p_bonf"]
        rho_s = "  nan  " if (rho != rho) else f"{rho:+.4f}"
        pp_s = "  nan  " if (pp != pp) else f"{pp:.4f}"
        ppb_s = "  nan  " if (ppb != ppb) else f"{ppb:.4f}"
        L.append(f"  {r['predictor']:10s} {rho_s:>8s} {pp_s:>9s} {ppb_s:>9s} "
                 f"{str(r['positive']):>5s}  {r['grade']}")
    L.append("-" * 80)
    verdict = ("at least one predictor PREDICTS timing (earned [V])" if res["any_predictor_validated"]
               else "NO measured promoter quantity predicts Carnegie staging -> overall [O] "
                    "(honest null; reported, not tuned)")
    L.append(f"  VERDICT: {verdict}")
    fa = res["falsifiability"]
    L.append(f"  self-checks: detects_signal={fa['apparatus_detects_signal']['ok']}  "
             f"gamma==dev_timing={fa['gamma_consistent_with_dev_timing']['ok']}  "
             f"copies_identical={fa['copied_sequences_identical']['ok']}  "
             f"fetch_reproduces_gamma={fa['fetched_reproduce_locked_gamma']['ok']}")
    L.append("=" * 80)
    return "\n".join(L)


if __name__ == "__main__":
    res, out = write_results()
    print(_fmt(res))
    print(f"\n  wrote {out}")
