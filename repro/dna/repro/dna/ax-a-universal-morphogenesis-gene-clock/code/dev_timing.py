"""
dev_timing.py -- CALIBRATE the gene-clock emergence schedule against REAL developmental timing.

This is HANDOFF open-item #1 (the gene-clock and morpho-plus NEXT lists both name it first):

    "Calibrate the emergence order against real developmental timing. We claim the order is a
     deterministic, falsifiable function of measured gamma -- NOT that it matches biology yet.
     Pull Carnegie-stage appearance data for a few unambiguous features and test
     corr(tau_on, observed_stage). This is the honest leap from 'DNA-determined order' to
     'DNA-PREDICTED order'."

It is the FALSIFICATION APPARATUS the framework has been promising. It does exactly one thing:
it takes the schedule the model derives PURELY from measured gamma (no tuning) and the observed
first-appearance Carnegie stages (a locked, cited external input, data/dev_timing.json), and it
reports the correlation between them -- WHATEVER that correlation is. Nothing here is adjusted to
make the number come out nicely; that is the whole point and the whole governance.

THE RESULT (reported honestly, computed below): for the [V]-master feature set, the measured
promoter-stiffness gamma schedule does NOT predict the observed staging (Spearman rho ~ 0,
permutation p ~ 1). So the model's emergence-order claim is, after this test, correctly graded:

    [O]  the emergence order is a DETERMINISTIC, FALSIFIABLE function of measured gamma, and it
         has now been TESTED against canonical human staging and does NOT (yet) match it. Promoter
         stiffness is evidently not the molecular correlate of developmental timing. This is a
         STRONGER, more honest position than the previous untested hedge -- the central open claim
         is now backed by a measurement rather than a caveat.

That null is not a failure of the apparatus: the falsifiability self-check below shows the test
WOULD report rho -> 1 if a gamma table happened to order the stages, and rho -> 0 for a shuffle.
The apparatus works; the biology simply says promoter stiffness != timing.

GRADES (neuro VP-SPEC C3 discipline):
  [V] spinodal identity (one switch) -- asserted < 1e-12.
  [V] the derived schedule for the test features is a pure measured-gamma readout
      (order == argsort(spinodal)), and the correlation + permutation p are correctly computed.
  [L] the observed Carnegie stages -- canonical, cited, read-only, independent of gamma.
  [O] a positive 'DNA predicts timing' claim -- NOT earned (rho ~ 0). Reported as such.

stdlib + numpy + scipy. Deterministic (pure arithmetic over the two frozen tables).
"""
import os, json, math, hashlib, itertools
import numpy as np
from scipy import stats
import gene_clock as GC

HERE = os.path.dirname(os.path.abspath(__file__))
TIMING_JSON = os.path.join(HERE, "data", "dev_timing.json")

# the [V]-master genes the timing test is allowed to use (genuine masters only -- see dev_timing.json)
V_MASTERS = {"PAX6", "PAX2", "LHX2", "TP63", "EDAR", "MITF", "PAX9", "TBX5", "TBX4", "HOXD13", "BMP4"}


# --------------------------------------------------------------------- load the locked input
def load_dev_timing(path=None):
    """Load the locked, cited Carnegie-stage table. Returns (features_list, provenance, raw_json).
    features_list = [(feature_name, gene, observed_stage_int), ...] in file order."""
    p = path or TIMING_JSON
    J = json.load(open(p, encoding="utf-8"))
    feats = [(name, d["gene"], int(d["stage_cs"])) for name, d in J["features"].items()]
    return feats, J.get("_provenance", ""), J


def timing_table_sha256(path=None):
    """sha256 of the canonical JSON content (frozen-input check)."""
    p = path or TIMING_JSON
    blob = json.dumps(json.load(open(p, encoding="utf-8")), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


# --------------------------------------------------------------------- the DNA-derived schedule
def derived_schedule(gammas, timing_feats):
    """For each timing feature, the model's gamma-derived quantities (PURE readout, no tuning):
    spinodal(gamma of its master gene), and the model tau_on from gene_clock.feature_schedule.
    Returns dict(feature -> dict(gene, gamma, spinodal, tau_on)) + the derived order."""
    fg = [(f, g) for f, g, _ in timing_feats]
    sched = GC.feature_schedule(fg, gammas)               # the SAME schedule the grower uses
    out = {}
    for f, g, _ in timing_feats:
        d = sched["features"][f]
        out[f] = dict(gene=g, gamma=d["gamma"], spinodal=d["spinodal"], tau_on=d["tau_on"])
    order = sched["order"]                                  # ascending tau_on == argsort(spinodal)
    return out, order, bool(sched["order_is_gamma_readout"])


# --------------------------------------------------------------------- the calibration
def _perm_p(x, y, observed_abs_rho):
    """Exact permutation p-value: fraction of label permutations with |rho| >= observed.
    n is small (~7), so n! is enumerable and the p-value is exact + deterministic."""
    y = np.asarray(y, float)
    n_ge = 0
    n_tot = 0
    for perm in itertools.permutations(y):
        rho = stats.spearmanr(x, perm).statistic
        n_ge += int(abs(rho) >= observed_abs_rho - 1e-12)
        n_tot += 1
    return n_ge / n_tot, n_tot


def calibrate(gammas=None, alpha=0.05):
    """Run the timing calibration and return an honest result dict.

    Reports (under the model's sign convention sign=+1, higher spinodal -> later):
      spearman_rho / p, pearson_r / p, permutation_p, and -- crucially -- whether a POSITIVE
      'DNA predicts timing' claim is earned. The grade is set BY THE EVIDENCE, never the reverse:
        validated == (perm_p < alpha) and (spearman_rho > 0)   ->  grade '[V]' else '[O]'.
    Also reports which sign convention the data would prefer (a free [F] choice this test
    constrains), with the explicit caveat that a non-significant rho constrains NOTHING.
    """
    if gammas is None:
        gammas, _ = GC.load_gamma_table()
    feats, prov, J = load_dev_timing()

    # all test genes must be genuine [V] masters (scope discipline)
    bad = [g for _, g, _ in feats if g not in V_MASTERS]
    masters_ok = (len(bad) == 0)

    sp = np.array([GC.spinodal(gammas[g]) for _, g, _ in feats], float)   # measured-gamma readout
    cs = np.array([s for _, _, s in feats], float)                        # locked observed stages

    rho = stats.spearmanr(sp, cs).statistic
    p_rho = stats.spearmanr(sp, cs).pvalue
    r = stats.pearsonr(sp, cs).statistic
    p_r = stats.pearsonr(sp, cs).pvalue
    perm_p, n_perm = _perm_p(sp, cs, abs(rho))

    # the honest grade: a positive prediction claim is earned ONLY by significant POSITIVE rank corr
    validated = bool((perm_p < alpha) and (rho > 0))
    grade = "[V]" if validated else "[O]"

    # which sign would the data prefer? (only meaningful if significant; we say so)
    sign_pref = (+1 if r >= 0 else -1)
    sign_constrained = bool(perm_p < alpha)

    sched, order, readout_ok = derived_schedule(gammas, feats)
    obs_order = [f for f, _, _ in sorted(feats, key=lambda t: t[2])]

    return dict(
        n_features=len(feats),
        features=[dict(feature=f, gene=g, gamma=float(gammas[g]),
                       spinodal=float(GC.spinodal(gammas[g])), observed_cs=int(s))
                  for f, g, s in feats],
        masters_only_V=masters_ok,
        spearman_rho=float(rho), spearman_p=float(p_rho),
        pearson_r=float(r), pearson_p=float(p_r),
        permutation_p=float(perm_p), n_permutations=int(n_perm),
        timing_validated=validated, grade=grade,
        sign_preferred_by_data=int(sign_pref), sign_is_constrained=sign_constrained,
        derived_order=order, observed_order=obs_order,
        order_is_gamma_readout=readout_ok,
        timing_sha256=timing_table_sha256(), provenance=prov,
    )


# --------------------------------------------------------------------- falsifiability self-checks
def apparatus_detects_signal(gammas=None):
    """Prove the test is NOT blind: if we hand it a SYNTHETIC gamma table whose spinodal is ordered
    to match the observed stages, |rho| -> 1; and a SHUFFLE of the stages gives |rho| small. So the
    null we report for the real gamma is a TRUE null (promoter stiffness != timing), not a dead test.
    Returns (ok, detail). This uses synthetic numbers ONLY to test the apparatus; it never touches
    the real measured gamma used for the actual claim."""
    feats, _, _ = load_dev_timing()
    cs = np.array([s for _, _, s in feats], float)
    # synthetic 'perfect' gamma: proportional to the observed STAGE VALUE, so tied stages get
    # identical gamma and the tie structure matches -> spinodal(g) is comonotone with cs (rho=1).
    g_perfect = 1.30 + 0.02 * (cs - cs.min())
    sp_perfect = GC.spinodal(g_perfect)
    rho_perfect = stats.spearmanr(sp_perfect, cs).statistic
    # shuffled stages vs the SAME synthetic gamma -> should NOT be a perfect match (deterministic)
    rng = np.random.default_rng(0)
    cs_shuf = cs.copy(); rng.shuffle(cs_shuf)
    rho_shuf = stats.spearmanr(sp_perfect, cs_shuf).statistic
    ok = bool((abs(rho_perfect) > 0.999) and (abs(rho_shuf) < 0.9))
    return ok, dict(rho_when_gamma_matches_stages=float(rho_perfect),
                    rho_when_stages_shuffled=float(rho_shuf))


def stages_independent_of_gamma(gammas=None, bump=0.1):
    """Anti-back-fit check: the observed stages are an EXTERNAL input -- perturbing the measured
    gamma table must NOT change a single observed stage (it cannot; stages are loaded from JSON).
    Also assert the observed order is NOT a suspiciously perfect match to the gamma order
    (|rho| < 0.99), i.e. nobody reverse-engineered the stages from gamma. Returns (ok, detail)."""
    feats, _, _ = load_dev_timing()
    cs0 = [s for _, _, s in feats]
    if gammas is None:
        gammas, _ = GC.load_gamma_table()
    g2 = dict(gammas); 
    for k in list(g2)[:5]:
        g2[k] = g2[k] + bump                     # perturb measured gamma
    feats2, _, _ = load_dev_timing()             # re-load: stages must be identical
    cs1 = [s for _, _, s in feats2]
    unchanged = bool(cs0 == cs1)
    sp = np.array([GC.spinodal(gammas[g]) for _, g, _ in feats], float)
    rho = abs(stats.spearmanr(sp, np.array(cs0, float)).statistic)
    not_backfit = bool(rho < 0.99)
    return (unchanged and not_backfit), dict(stages_unchanged_under_gamma_perturbation=unchanged,
                                             abs_rho=float(rho), not_backfit=not_backfit)


# --------------------------------------------------------------------- write results + report
def write_results():
    res = calibrate()
    det_ok, det = apparatus_detects_signal()
    ind_ok, ind = stages_independent_of_gamma()
    res["falsifiability"] = dict(apparatus_detects_signal=dict(ok=det_ok, **det),
                                 stages_independent_of_gamma=dict(ok=ind_ok, **ind))
    out = os.path.join(HERE, "..", "results", "dev_timing.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(res, open(out, "w"), indent=2)
    return res, out


def _fmt(res):
    L = []
    L.append("=" * 78)
    L.append("  DEVELOPMENTAL-TIMING CALIBRATION  (gene clock vs canonical Carnegie staging)")
    L.append("=" * 78)
    L.append(f"  {'feature':18s} {'gene':7s} {'gamma':>7s} {'spinodal':>9s} {'obs_CS':>6s}")
    for f in res["features"]:
        L.append(f"  {f['feature']:18s} {f['gene']:7s} {f['gamma']:7.4f} "
                 f"{f['spinodal']:9.5f} {f['observed_cs']:6d}")
    L.append("-" * 78)
    L.append(f"  Spearman rho(spinodal, observed_CS) = {res['spearman_rho']:+.4f}  "
             f"(perm p = {res['permutation_p']:.4f}, n!={res['n_permutations']})")
    L.append(f"  Pearson   r  (spinodal, observed_CS) = {res['pearson_r']:+.4f}  "
             f"(p = {res['pearson_p']:.4f})")
    L.append(f"  DNA-derived order : {' < '.join(res['derived_order'])}")
    L.append(f"  observed   order  : {' < '.join(res['observed_order'])}")
    L.append("-" * 78)
    verdict = ("PREDICTS timing (earned [V])" if res["timing_validated"]
               else "does NOT predict timing -> grade [O] (honest null; reported, not tuned)")
    L.append(f"  VERDICT: measured promoter-stiffness gamma {verdict}")
    L.append(f"  (a positive claim requires perm p < 0.05 AND positive rank corr; "
             f"here p={res['permutation_p']:.2f})")
    L.append("=" * 78)
    return "\n".join(L)


if __name__ == "__main__":
    res, out = write_results()
    print(_fmt(res))
    print(f"\n  wrote {out}")
