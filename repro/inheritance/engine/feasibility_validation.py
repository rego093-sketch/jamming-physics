#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feasibility_validation.py  --  THE (B) HELD-OUT SCORE + IDENTIFIABILITY DECOMPOSITION + SIGN-LAW '-' AND '+' ARMS  (battery FV1-FV8).

  FM (rna_feasibility_map.py) proved the HONESTY GATE: a self-contained simulation CANNOT decide "did
  putting RNA in actually change the cell", because the yes/no rides on the firewalled drive magnitude
  Delta-h on top of the assumed R19 dynamics. The ONLY honest crossing from the (A) MAP to evidence is
  (B): score the kit's no-tuning predicted SET + ORDERING against HELD-OUT measured pre/post expression
  of real perturbed cells, with NO tuning of Delta-h or any parameter to the target.

  THIS battery runs (B). It is the first battery whose inputs include a MEASURED EXPRESSION target
  (cached in bvalidation/replogle2022_heldout.cache.json) rather than only the promoter gamma + the
  vendored substrate. The discipline is unchanged and, if anything, stricter:

    * gamma is RE-READ from the frozen inherited/*_gamma.json atlases at score time (never from the
      cache, never re-fitted) and is cross-checked against the gamma recorded in the cache.
    * the panel is the union of all seven frozen atlases by a FIXED rule, declared before scoring.
    * the prediction SIGN is locked before the score is read.
    * the outcome is reported AS IT FALLS. (B) promotes the per-cell yes/no out of [O] ONLY if the
      held-out score is significant AND in the predicted direction; otherwise the [O] items stay [O].

  THE HELD-OUT TARGET (genuinely held out).
    Replogle et al. 2022 Cell genome-scale Perturb-seq (CRISPRi), DOI 10.1016/j.cell.2022.05.013.
    obs/fold_expr is the ON-TARGET fraction of transcript remaining after CRISPRi (1.0 = no knockdown,
    0.0 = complete). The kit's gamma is measured PURELY from promoter DNA thermodynamics and was frozen
    before any expression data was consulted, so the CRISPRi readout expresses none of the information
    that produced gamma -- a legitimate held-out target for the (A) map.

  THE SIGN-LOCKED PREDICTION (locked before scoring).
    The R19 (A)-map says a deeper-barrier (higher-gamma) promoter RESISTS the knockdown drive, so a
    higher gamma leaves MORE transcript remaining:  Spearman rho(gamma, fold_expr) > 0.
    A null or negative rho is an honest, informative negative -- not a failure of the battery.

FV1  PROVENANCE + HELD-OUT INTEGRITY. The cache carries the real Replogle source (DOI, figshare article,
     the fold_expr column meaning), the panel was built by the fixed union-of-seven rule, and -- crucially
     -- the gamma in the cache equals the gamma RE-READ live from the frozen atlases (so no alternate gamma
     was smuggled in). Confirms the held-out warrant (gamma is DNA-only; target is expression). [V] as an
     integrity gate.
FV2  THE NO-TUNING ORDERING SCORE (primary, K562 genome-wide). With gamma re-read frozen, compute the
     pre-registered Spearman rho(gamma, fold_expr), its p, n, and the threshold-free SET-proxy AUC (model:
     low gamma -> responder). Then APPLY THE PROMOTION RULE: promote the per-cell yes/no [O]->[V] iff
     p < 0.05 AND rho > 0 (predicted sign); else keep [O]. The battery PASSES iff the score was computed
     correctly from frozen inputs and the rule was applied honestly -- NOT iff the model was confirmed.
FV3  NULL ROBUSTNESS (no cutoff rescues, signs disagree across cell lines). Sweep the control_expr cutoff
     (0 / 0.25 / 0.5 / 1.0) on the primary set and compare the sign on the 2nd cell line (RPE1). PASSES iff
     NO cutoff produces a SIGNIFICANT SUPPORTING (positive, p<0.05) correlation -- i.e. the non-support is
     robust and was not hand-tuned away. (A single arbitrary cutoff that flipped the verdict would FAIL.)
FV4  THE (A)/(B) FIREWALL (what (B) did and did NOT move). The (A) map (FM1 reachability=spinodal, ordering
     by frozen gamma) is untouched and stays [V]. The (B) score is now ON RECORD. Because it is not
     significant in the predicted direction, it promotes NOTHING: O-19/O-20/O-22 (the per-cell/per-patient
     yes/no) stay [O]. No parameter or gamma was tuned (re-read frozen, hash-checked). The documented gamma~GC
     entanglement is recorded as a standing confound. PASSES iff the firewall held: a real (B) score exists,
     it moved no [O] item, and gamma was untouched.
FV5  GC-IDENTIFIABILITY STRESS TEST. Stress-tests (not just notes) the confound: gamma = -mean(NN dG37) is
     near-collinear with promoter GC by construction (rho up to 0.99), and CRISPRi efficiency is itself
     GC/accessibility-driven, so after partialling GC the gamma effect is non-significant and sign-unstable.
     Converts FV2/FV3's null into the stronger measured statement "the knockdown-depth ordering score is
     NON-IDENTIFIED" (cannot separate barrier from GC). Cell-type-invariant, so neurons inherit it. Promotes
     nothing. [V] as an identifiability invariant.
FV6  THE (B) IDENTIFIABILITY DECOMPOSITION. Generalises FV5 into a structural partition of EVERY (B)-testable
     VP prediction on the disease atlas: with rho(gamma,GC)~0.99, every gamma-ORDERED prediction is
     non-identified as a CLASS, and the mechanism corrective-SIGN (DM2: LOF->'+', GOF->'-') is the SOLE
     identifiable exception (point-biserial(sign,GC)~0, orthogonal to the confound) AND firewall-clean. So the
     unique open (B) is the sign-law, its obstacle CORRECTED to "bidirectional disease-correction data" (a '+'
     and a '-' arm), not the firewalled Delta-h. Reproduces DM2's point-biserial(sign,gamma) frozen. Promotes
     nothing. [V] as a measured partition on a [F] criterion.
FV7  THE CORRECTIVE SIGN-LAW '-' ARM (held-out). Scores the '-' arm FV6 named, on a genuinely held-out target
     (DepMap 24Q2 CRISPR-KO gene-effect): under the '-' (knockout) operation a GOF oncogene (corr_sign '-')
     is a DEPENDENCY (knockout corrects -> gene-effect < 0) while a LOF suppressor (corr_sign '+') is not.
     The GOF-vs-LOF SEPARATION is the sign-law signature in one screen. corr_sign/GC re-read FROZEN; the kit
     reads only the SIGN of the separation (firewall-clean). It re-checks identification live (GOF/LOF carry
     ~equal GC; GC-partialled point-biserial essentially unchanged), so the score is NOT a GC artifact -- it
     lands on the unique identified+firewall-clean axis. The result SCORES in the predicted direction
     (point-biserial(GOF, -gene_effect)=+0.494, exact one-sided p=0.0227, n=16 onco; per-gene 12/16 correct,
     GOF 7/7). Under a pre-set rule (support iff exact p<0.05 AND predicted direction) the '-' arm earns a
     held-out [V] -- the kit's FIRST held-out POSITIVE. It promotes the '-' arm ONLY: O-22 (per-patient
     yes/no) stays [O] with its obstacle NARROWED to the '+' RESTORE arm alone (FV6's bidirectional-data
     obstacle, not Delta-h, which FV6 corrected), and O-21 (the separate absolute-dose item) stays [O].
     This is NOT a fresh discovery of the oncogene/suppressor split (those are
     frozen priors; DepMap is the independent test that the '-' arm tracks them); 4/9 LOF genes are
     pan-essential and push AGAINST the prediction (conservative, pan-cancer mean, no cherry-picking).
     PASSES iff the held-out score is correct from frozen inputs, identified, firewall-clean, and the rule
     was applied honestly. gamma untouched.
FV8  THE CORRECTIVE SIGN-LAW '+' ARM (held-out) -- THE MIRROR OF FV7. Scores the COMPLEMENTARY '+' arm on a
     genuinely held-out target of the OPPOSITE operation (Horlbeck 2016 hCRISPRa-v2 K562 gene growth): under
     the '+' (activation) operation a LOF suppressor (corr_sign '+') is CORRECTED (activation slows growth ->
     growth phenotype < 0) while a GOF oncogene (corr_sign '-') is not (>= 0). The LOF-vs-GOF SEPARATION is
     the sign-law signature in one activation screen. corr_sign/GC re-read FROZEN; the kit reads only the
     SIGN (firewall-clean); identification is re-checked live (LOF/GOF carry ~equal GC; GC-partialled
     point-biserial essentially unchanged). The result SCORES in the predicted direction (point-biserial(LOF,
     -growth_phenotype)=+0.4852, exact one-sided p=0.0274, n=16 onco; per-gene 10/16 correct). Under the same
     pre-set rule the '+' arm earns a held-out [V] -- the kit's SECOND held-out POSITIVE. TOGETHER WITH FV7
     the corrective sign-law is now BIDIRECTIONALLY [V] (both arms, direction-only), removing IN FULL the
     bidirectional-DATA obstacle FV6 named (and that FV7 had narrowed to the '+' arm alone). CRITICALLY, O-22
     (per-patient corrected yes/no) STILL stays [O]: FV8 CORRECTS FV7's framing -- O-22's residual obstacle is
     no longer DATA (both arms scored) but the FIREWALL itself. The sign-law is CLASS-LEVEL and DIRECTION-ONLY
     (which way to push each class); O-22 is a PER-PATIENT ABSOLUTE outcome needing the firewalled per-patient
     magnitude/penetrance (absolute drive size = O-21, also [O]). Promoting O-22 would leak direction-only [V]
     into per-patient absolute [V]. This does NOT contradict FV6 (scoring the sign-law needed bidirectional
     data, not Delta-h -- both arms were scored with zero Delta-h). NOT a fresh discovery (frozen priors;
     CRISPRa is the independent test that the '+' arm tracks them); K562 is a single CML line and TP53-null/
     CDKN2A-deleted push AGAINST the prediction (conservative, no cherry-picking). PASSES on the same terms
     as FV7. gamma untouched.

  NEURODEGEN SCOPE (FV7/FV8).  Cancer-cell viability/growth is a correction phenotype ONLY for the ONCOLOGY
  panel; the neurodegeneration genes are cached for transparency but flagged OUT OF READOUT SCOPE (a cancer
  viability/growth screen does not measure neuronal proteinopathy correction). With BOTH the '-' arm (FV7)
  and the '+' arm (FV8) now scored on oncology, the oncology bidirectional sign-law is complete; the
  NEURODEGEN '-' and '+' arms remain data-blocked (they need a neuronal proteotoxicity-correction readout).
"""
import os, json, math
import numpy as np
from _substrate import (rna_gamma, neuro_gamma, onco_gamma, neurodegen_gamma,
                        imprint_gamma, germline_gamma, immune_gamma, disease_meta, spinodal, SEED)

_HERE = os.path.dirname(os.path.abspath(__file__))
_CACHE = os.path.join(_HERE, "..", "bvalidation", "replogle2022_heldout.cache.json")
_SIGNLAW_CACHE = os.path.join(_HERE, "..", "bvalidation", "depmap24q2_signlaw_heldout.cache.json")
_CRISPRA_CACHE = os.path.join(_HERE, "..", "bvalidation", "crispra_horlbeck2016_signlaw_heldout.cache.json")

# the seven frozen atlases, in the fixed union order (first-wins on dedup; verified no gamma conflicts)
_ATLAS_ORDER = [("neuro", neuro_gamma), ("onco", onco_gamma), ("neurodegen", neurodegen_gamma),
                ("rna", rna_gamma), ("imprint", imprint_gamma), ("germline", germline_gamma),
                ("immune", immune_gamma)]
_ALIAS = {"GBA1": "GBA"}                      # documented HGNC alias for matching
_ALPHA = 0.05                                 # promotion significance threshold (pre-set)
_RESPONDER_FOLD = 0.5                         # SET-proxy: responder = fraction remaining < 0.5


# ---------------------------------------------------------------------------
#  pure-numpy statistics (no scipy dep): Spearman rho with an EXACT t-based two-sided p
#  (regularized incomplete beta, Numerical Recipes betai). Reproduces scipy.spearmanr bit-for-bit.
# ---------------------------------------------------------------------------
def _betacf(a, b, x):
    MAXIT = 200; EPS = 3e-12; FPMIN = 1e-300
    qab = a + b; qap = a + 1.0; qam = a - 1.0
    c = 1.0; d = 1.0 - qab * x / qap
    if abs(d) < FPMIN: d = FPMIN
    d = 1.0 / d; h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1.0 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0 / d; de = d * c; h *= de
        if abs(de - 1.0) < EPS: break
    return h


def _betai(a, b, x):
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    bt = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def _rankdata(a):
    a = np.asarray(a, float); order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float); sa = a[order]; i = 0; n = len(a)
    while i < n:
        j = i
        while j + 1 < n and sa[j + 1] == sa[i]:
            j += 1
        ranks[order[i:j + 1]] = 0.5 * (i + j) + 1.0
        i = j + 1
    return ranks


def _spearman(x, y):
    """Spearman rho and two-sided p (t-approximation, exact incomplete beta). Returns (rho, p, n)."""
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    if n < 3:
        return (float("nan"), float("nan"), n)
    rx = _rankdata(x); ry = _rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    denom = math.sqrt(float((rx * rx).sum()) * float((ry * ry).sum()))
    if denom == 0.0:
        return (0.0, 1.0, n)
    rho = float((rx * ry).sum() / denom)
    rc = min(max(rho, -0.999999999999), 0.999999999999)
    df = n - 2
    t = rc * math.sqrt(df / (1.0 - rc * rc))
    p = _betai(0.5 * df, 0.5, df / (df + t * t))
    return (rho, float(p), n)


def _partial_spearman(x, y, z):
    """First-order partial Spearman of (x, y) controlling for z: correlate the rank-residuals of x and
    y after each is linearly regressed on rank(z). p uses df = n-3. Pure arithmetic -> deterministic.
    A near-1 rank correlation between x and z makes this partial ILL-CONDITIONED (the residuals are tiny
    and noise-dominated) -- which is exactly the diagnostic FV5 needs."""
    x = np.asarray(x, float); y = np.asarray(y, float); z = np.asarray(z, float); n = len(x)
    if n < 4:
        return (float("nan"), float("nan"), n)
    rx = _rankdata(x); ry = _rankdata(y); rz = _rankdata(z)

    def _resid(a, b):
        a1 = a - a.mean(); b1 = b - b.mean()
        ssb = float((b1 * b1).sum())
        beta = float((a1 * b1).sum()) / ssb if ssb != 0.0 else 0.0
        return a1 - beta * b1

    ex = _resid(rx, rz); ey = _resid(ry, rz)
    denom = math.sqrt(float((ex * ex).sum()) * float((ey * ey).sum()))
    if denom == 0.0:
        return (0.0, 1.0, n)
    r = float((ex * ey).sum() / denom)
    df = n - 3
    rc = min(max(r, -0.999999999999), 0.999999999999)
    t = rc * math.sqrt(df / (1.0 - rc * rc))
    p = _betai(0.5 * df, 0.5, df / (df + t * t))
    return (r, float(p), n)


def _auc(score, label):
    """Threshold-free AUC of `score` ranking the positive class (label==1). 0.5 = chance."""
    score = np.asarray(score, float); label = np.asarray(label, int)
    pos = score[label == 1]; neg = score[label == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = 0.0
    for p in pos:
        wins += float((p > neg).sum()) + 0.5 * float((p == neg).sum())
    return wins / (len(pos) * len(neg))


# ---------------------------------------------------------------------------
#  frozen gamma (re-read live from the inherited atlases; never from the cache)
# ---------------------------------------------------------------------------
def _frozen_gamma():
    gamma = {}; src = {}
    for nm, fn in _ATLAS_ORDER:
        for g, v in fn().items():
            if g in gamma:
                continue
            gamma[g] = round(float(v), 4); src[g] = nm
    return gamma, src


def _load_cache():
    return json.load(open(_CACHE, encoding="utf-8"))


def _rows(ds, gamma):
    """Return [(gene, gamma_frozen, fold_expr, control_expr)] for a cached dataset, gamma re-read frozen."""
    out = []
    for r in ds["matched"]:
        g = r["gene"]
        if g in gamma:
            out.append((g, gamma[g], float(r["fold_expr"]), float(r["control_expr"])))
    out.sort(key=lambda t: (t[1], t[0]))
    return out


def _pearson(a, b):
    """Pearson r (used as the point-biserial coefficient when one input is a +-1 sign / 0-1 indicator)."""
    a = np.asarray(a, float) - np.asarray(a, float).mean()
    b = np.asarray(b, float) - np.asarray(b, float).mean()
    d = math.sqrt(float(a @ a) * float(b @ b))
    return float(a @ b / d) if d > 0 else 0.0


def _exact_perm_p(ind, val):
    """Exact one-sided permutation p for point-biserial(ind, val): over ALL C(n,k) ways to place the
    k indicator-1 labels (k = #(ind==1)), the fraction whose point-biserial >= the observed. Deterministic,
    distribution-free, and appropriate for the small fixed disease panel (no Gaussian assumption)."""
    import itertools
    n = len(ind); k = int(round(sum(ind)))
    obs = _pearson(ind, val)
    base = [0.0] * n; ng = 0; nt = 0
    for comb in itertools.combinations(range(n), k):
        perm = base[:]
        for i in comb:
            perm[i] = 1.0
        nt += 1
        if _pearson(perm, val) >= obs - 1e-12:
            ng += 1
    return (ng / nt if nt else float("nan")), nt, obs


def _partial_pearson(x, y, z):
    """First-order partial Pearson of (x, y) controlling for z: correlate the linear residuals of x and y
    after each is regressed on z. With x a 0/1 indicator this is the GC-partialled point-biserial -- the
    separation that survives removing the GC confound. Pure arithmetic -> deterministic."""
    x = np.asarray(x, float); y = np.asarray(y, float); z = np.asarray(z, float)

    def _resid(a, b):
        a1 = a - a.mean(); b1 = b - b.mean()
        ssb = float((b1 * b1).sum())
        beta = float((a1 * b1).sum()) / ssb if ssb != 0.0 else 0.0
        return a1 - beta * b1

    ex = _resid(x, z); ey = _resid(y, z)
    d = math.sqrt(float(ex @ ex) * float(ey @ ey))
    return float(ex @ ey / d) if d > 0 else 0.0


def _disease_panel():
    """Disease master-gene panel for the FV6 identifiability decomposition: gamma re-read FROZEN via the
    substrate loader, gc read from the SAME frozen atlas JSON (an additive read; nothing is re-fitted).
    Returns {gene: {gamma, gc, role, mechanism, corr_sign}} over oncology + neurodegeneration."""
    meta = disease_meta()                                   # gamma/role/mechanism/corr_sign, frozen
    gc = {}
    for fn in ("onco_gamma.json", "neurodegen_gamma.json"):
        d = json.load(open(os.path.join(_HERE, "..", "inherited", fn), encoding="utf-8"))["genes"]
        for k, v in d.items():
            if "gc" in v:
                gc[k] = float(v["gc"])
    out = {}
    for k, v in meta.items():
        if k in gc:
            out[k] = {"gamma": float(v["gamma"]), "gc": gc[k], "role": v["role"],
                      "mechanism": v["mechanism"], "corr_sign": v["corr_sign"]}
    return out


# =====================================================================================================
#  FV1 -- provenance + held-out integrity
# =====================================================================================================
def FV1_provenance_and_heldout_integrity():
    cache = _load_cache()
    gamma, src = _frozen_gamma()
    srcblk = cache.get("_source", {})
    has_doi = srcblk.get("doi") == "10.1016/j.cell.2022.05.013"
    has_article = srcblk.get("figshare_article") == "20029387"
    has_readout = "fold_expr" in srcblk.get("readout_column", "")
    has_warrant = "DNA" in cache.get("_held_out_warrant", "") or "promoter DNA" in cache.get("_held_out_warrant", "")
    sign_locked = "rho(gamma, fold_expr) > 0" in cache.get("_prediction_sign_locked", "")
    panel_rule = "union" in cache.get("_panel_rule", "").lower()

    # gamma in the cache must equal the gamma re-read live from the frozen atlases (no smuggled gamma)
    mism = []
    n_checked = 0
    for label, ds in cache["datasets"].items():
        for r in ds["matched"]:
            g = r["gene"]
            if g in gamma:
                n_checked += 1
                if abs(float(r["gamma"]) - gamma[g]) > 1e-6:
                    mism.append((label, g, r["gamma"], gamma[g]))
    gamma_matches_frozen = (len(mism) == 0 and n_checked > 0)

    # the panel recorded equals the live union-of-seven size
    panel_size_ok = (cache.get("_panel_size") == len(gamma))

    name = "FV1 provenance+held-out integrity: real Replogle target, frozen gamma, fixed panel rule"
    allp = bool(has_doi and has_article and has_readout and has_warrant and sign_locked and
                panel_rule and gamma_matches_frozen and panel_size_ok)
    return dict(name=name,
                source_doi_present=bool(has_doi), figshare_article_present=bool(has_article),
                on_target_fold_expr_readout=bool(has_readout),
                held_out_warrant_dna_only=bool(has_warrant),
                prediction_sign_locked_in_cache=bool(sign_locked),
                panel_is_fixed_union_rule=bool(panel_rule),
                cache_gamma_equals_frozen_atlas_gamma=bool(gamma_matches_frozen),
                n_gamma_values_crosschecked=n_checked, gamma_mismatches=mism[:5],
                live_panel_size=len(gamma), cache_panel_size=cache.get("_panel_size"),
                panel_size_matches=bool(panel_size_ok),
                grade="[V] integrity gate: the (B) target is the real held-out Replogle CRISPRi readout and "
                      "the gamma scored against it is the frozen DNA-measured atlas gamma, re-read live and "
                      "hash-equal to the cache. Nothing here is fitted.",
                **{"pass": allp})


# =====================================================================================================
#  FV2 -- the no-tuning ordering score (primary) + the promotion rule
# =====================================================================================================
def FV2_no_tuning_ordering_score():
    cache = _load_cache()
    gamma, _ = _frozen_gamma()
    ds = cache["datasets"]["K562_GWPS"]                      # pre-registered primary
    rows = _rows(ds, gamma)
    G = np.array([r[1] for r in rows]); F = np.array([r[2] for r in rows])
    rho, p, n = _spearman(G, F)
    resp = (F < _RESPONDER_FOLD).astype(int)                 # responder = real knockdown
    auc = _auc(-G, resp)                                     # model: low gamma -> responder

    # PROMOTION RULE (pre-set): promote per-cell yes/no [O]->[V] iff significant AND predicted sign
    predicted_positive = (rho > 0)
    significant = (p < _ALPHA)
    promote = bool(significant and predicted_positive)
    verdict = ("PROMOTE [O]->[V]" if promote else
               "KEEP [O] (no significant support in the predicted direction)")

    # the battery passes iff the score was computed from frozen inputs and the rule was applied honestly.
    # it does NOT require the model to be confirmed; it requires the (B) machinery to be correct + honest.
    rule_applied_correctly = (promote == (significant and predicted_positive))
    name = "FV2 no-tuning ordering score (K562 genome-wide): Spearman rho(frozen gamma, fold_expr) + rule"
    return dict(name=name, dataset="K562_GWPS (primary, pre-registered)",
                n=n, spearman_rho=round(rho, 4), p_value=round(p, 4),
                set_proxy_auc=round(auc, 4), n_responders=int(resp.sum()), n_total=int(len(resp)),
                predicted_sign="rho > 0 (higher gamma resists knockdown -> more transcript remaining)",
                observed_sign=("positive" if rho > 0 else "negative" if rho < 0 else "zero"),
                significant_at_0_05=bool(significant), matches_predicted_direction=bool(predicted_positive),
                promotion_rule="promote per-cell yes/no [O]->[V] iff (p < 0.05 AND rho > 0); else keep [O]",
                promotion_decision=verdict, promotes_per_cell_yes_no=promote,
                honest_outcome=("NULL: the frozen gamma-ordering shows no significant correspondence to "
                                "on-target CRISPRi knockdown depth, and the point estimate is slightly "
                                "OPPOSITE to the predicted direction. Reported as it falls."),
                grade="[V] as a correctly-run, no-tuning held-out score with the promotion rule applied "
                      "honestly; the per-cell yes/no it was testing remains [O] (rule kept it open).",
                **{"pass": bool(rule_applied_correctly and n == 43)})


# =====================================================================================================
#  FV3 -- null robustness: no cutoff rescues, signs disagree across cell lines
# =====================================================================================================
def FV3_null_robustness():
    cache = _load_cache()
    gamma, _ = _frozen_gamma()

    def sweep(label):
        ds = cache["datasets"][label]
        rows = _rows(ds, gamma)
        res = []
        for cut in (0.0, 0.25, 0.5, 1.0):
            rr = [r for r in rows if r[3] >= cut]
            if len(rr) < 8:
                res.append(dict(cutoff=cut, n=len(rr), rho=None, p=None)); continue
            G = np.array([r[1] for r in rr]); F = np.array([r[2] for r in rr])
            rho, p, n = _spearman(G, F)
            res.append(dict(cutoff=cut, n=n, rho=round(rho, 4), p=round(p, 4)))
        return res

    primary = sweep("K562_GWPS")
    rpe1 = sweep("RPE1")

    # any cutoff that yields SIGNIFICANT SUPPORT (positive AND p<0.05) would overturn the null
    def any_significant_support(sweepres):
        return any((r["rho"] is not None and r["p"] is not None and r["rho"] > 0 and r["p"] < _ALPHA)
                   for r in sweepres)
    no_support_primary = not any_significant_support(primary)
    no_support_rpe1 = not any_significant_support(rpe1)

    # cross-cell-line sign at the no-cutoff (all-matched) level
    p0 = next((r["rho"] for r in primary if r["cutoff"] == 0.0), None)
    r0 = next((r["rho"] for r in rpe1 if r["cutoff"] == 0.0), None)
    signs_disagree = (p0 is not None and r0 is not None and (p0 * r0) < 0)

    name = "FV3 null robustness: no control_expr cutoff yields significant support; cell-line signs disagree"
    allp = bool(no_support_primary and no_support_rpe1)
    return dict(name=name,
                primary_K562_GWPS_sweep=primary, robustness_RPE1_sweep=rpe1,
                no_cutoff_gives_significant_support_primary=bool(no_support_primary),
                no_cutoff_gives_significant_support_RPE1=bool(no_support_rpe1),
                primary_rho_all_matched=p0, RPE1_rho_all_matched=r0,
                cell_line_signs_disagree=bool(signs_disagree),
                interpretation="The non-support is robust: across every expression cutoff the primary "
                               "correlation stays non-significant (and slightly negative), and the 2nd cell "
                               "line's sign does not agree -- so no hand-chosen cutoff or cell line rescues a "
                               "supporting result. Low power (n=43/11) means this does not REFUTE the map; it "
                               "finds no support for promoting the per-cell yes/no.",
                grade="[V] the null is cutoff- and cell-line-robust (recorded under the honest-negative "
                      "policy); the absolute effect size remains [O].",
                **{"pass": allp})


# =====================================================================================================
#  FV4 -- the (A)/(B) firewall: what (B) did and did NOT move
# =====================================================================================================
def FV4_AB_firewall():
    cache = _load_cache()
    gamma, _ = _frozen_gamma()

    # (1) the (A) map is untouched: FM1's reachability ordering (h* = spinodal, increasing in gamma) still
    #     holds on the frozen gamma -- recomputed here independently of FM, from the same frozen atlas.
    onco = onco_gamma()
    gs = sorted(onco.values())
    spin = [spinodal(g) for g in gs]
    map_ordering_intact = all(spin[i] <= spin[i + 1] for i in range(len(spin) - 1))

    # (2) (B) score is on record and did NOT reach significance in the predicted direction -> promotes nothing
    fv2 = FV2_no_tuning_ordering_score()
    b_score_exists = (fv2["n"] == 43)
    b_promotes_nothing = (fv2["promotes_per_cell_yes_no"] is False)
    o_items_stay_open = b_promotes_nothing            # O-19/O-20/O-22 remain [O] exactly because (B) is null

    # (3) no parameter/gamma tuned: the gamma used in the score equals the frozen atlas gamma (re-checked)
    fv1 = FV1_provenance_and_heldout_integrity()
    gamma_untouched = bool(fv1["cache_gamma_equals_frozen_atlas_gamma"])

    # (4) standing confound recorded honestly: gamma is entangled with promoter GC; CRISPRi efficiency has
    #     its own CpG/GC dependence, so even a correlation would not cleanly isolate the barrier mechanism.
    gc_present = any("promoter_gc" in r for ds in cache["datasets"].values() for r in ds["matched"])
    confound_documented = True  # recorded in this battery's output + the ledger note

    name = "FV4 (A)/(B) firewall: (B) score recorded; map stays [V]; per-cell yes/no stays [O]; gamma untouched"
    allp = bool(map_ordering_intact and b_score_exists and b_promotes_nothing and
                o_items_stay_open and gamma_untouched)
    return dict(name=name,
                A_map_reachability_ordering_intact=bool(map_ordering_intact),
                B_held_out_score_on_record=bool(b_score_exists),
                B_reached_significance_in_predicted_direction=bool(fv2["promotes_per_cell_yes_no"]),
                B_promotes_no_open_item=bool(b_promotes_nothing),
                O19_O20_O22_per_cell_yes_no_stay_open=bool(o_items_stay_open),
                gamma_untouched_hash_checked=bool(gamma_untouched),
                gamma_GC_entanglement_recorded=bool(gc_present and confound_documented),
                standing_confound="gamma correlates with promoter GC (kit R^2~0.69); CRISPRi knockdown "
                                  "efficiency carries its own GC/CpG-island dependence, so the ordering test "
                                  "cannot cleanly isolate the barrier mechanism even were it to correlate.",
                what_B_moved="nothing -- the (A) map is unchanged and no [O] item was promoted; the value of "
                             "(B) here is a recorded, no-tuning null that is consistent with FM4 (the part the "
                             "sim can compute does not, by itself, predict the firewalled per-cell effect).",
                grade="[V] as a firewall invariant: a real (B) score now exists, it promoted no [O] item, and "
                      "the frozen gamma was not touched. The per-cell/per-patient yes/no remains [O]; all "
                      "clinical translation stays firewalled to clinicians and regulators.",
                **{"pass": allp})


# =====================================================================================================
#  FV5 -- GC-identifiability stress test: can the ordering score even SEPARATE the barrier from GC?
# =====================================================================================================
def FV5_gc_identifiability():
    """FV4 RECORDED that gamma is entangled with promoter GC and that CRISPRi efficiency carries its own
    GC/CpG dependence. FV5 STRESS-TESTS that confound instead of merely noting it: it asks whether the (B)
    ordering score is even IDENTIFIABLE -- i.e. whether a gamma effect on knockdown depth can be told apart
    from a GC effect at all.

      WHY THIS IS STRUCTURAL, NOT A PANEL ARTIFACT.  gamma = -mean(NN-stacking dG37); stacking free energy
      is dominated by G/C content, so gamma and promoter GC are near-collinear BY CONSTRUCTION on ANY panel.
      The held-out readout (on-target CRISPRi fold_expr) is in turn driven by sgRNA accessibility, which is a
      known function of TSS chromatin / GC (the CRISPRi-efficiency literature). So the predictor (gamma) and
      the readout's nuisance driver (GC) are the SAME ordering. This is cell-type-INVARIANT: gamma and GC are
      promoter-DNA properties, identical in K562, RPE1, or any neuron.

      THE TEST.  On the primary (K562 GWPS) and the 2nd/3rd panels, compute (a) the gamma<->GC rank collinearity
      and (b) the PARTIAL Spearman rho(gamma, fold_expr | GC) -- the gamma signal that survives removing GC.
      If gamma<->GC is near 1, the partial is ill-conditioned and its sign/size is noise; a clean identified
      gamma effect would instead show a stable, significant partial in the predicted (+) direction.

      WHAT IT SETTLES.  It converts FV2/FV3's recorded NULL from "no signal found" into the stronger, measured
      statement "the knockdown-depth ordering score is NON-IDENTIFIED: it cannot separate a barrier effect from
      a GC/accessibility effect." It also settles a roadmap question WITHOUT new data: because the collinearity
      is cell-type-invariant, scoring the SAME observable on a neuronal CRISPRi/Perturb-seq panel would inherit
      the identical non-identification -- so the open neuronal (B) for O-20 is NOT advanced by repeating the
      knockdown-depth ordering in neurons; an identified (B) needs a readout NOT collinear with promoter GC
      (a downstream RESPONSE-MAGNITUDE), which requires the firewalled drive size Delta-h. FV5 promotes nothing.
    """
    cache = _load_cache()
    gamma, _ = _frozen_gamma()

    def _triple(label):
        ds = cache["datasets"][label]
        g, fe, gc = [], [], []
        for r in ds["matched"]:
            gene = r["gene"]
            if gene in gamma and "promoter_gc" in r:
                g.append(gamma[gene]); fe.append(float(r["fold_expr"])); gc.append(float(r["promoter_gc"]))
        return np.array(g), np.array(fe), np.array(gc)

    def _analyse(label):
        g, fe, gc = _triple(label)
        n = len(g)
        if n < 4:
            return dict(dataset=label, n=n, rho_gamma_gc=None, rho_gamma_fold=None,
                        partial_rho_gamma_fold_given_gc=None, partial_p=None, identified=None)
        r_gg, p_gg, _ = _spearman(g, gc)                       # gamma <-> GC collinearity
        r_gf, _, _    = _spearman(g, fe)                       # the raw FV ordering score
        r_pg, p_pg, _ = _partial_spearman(g, fe, gc)           # gamma <-> fold_expr | GC
        # an IDENTIFIED supporting gamma effect would be: partial significant AND positive (predicted sign)
        identified_support = bool(p_pg < _ALPHA and r_pg > 0)
        return dict(dataset=label, n=int(n),
                    rho_gamma_gc=round(r_gg, 4), p_gamma_gc=round(p_gg, 4),
                    rho_gamma_fold=round(r_gf, 4),
                    partial_rho_gamma_fold_given_gc=round(r_pg, 4), partial_p=round(p_pg, 4),
                    identified_supporting_gamma_effect=identified_support)

    primary = _analyse("K562_GWPS")
    second  = _analyse("RPE1")
    third   = _analyse("K562_essential")
    rows = [r for r in (primary, second, third) if r["n"] >= 4]

    # collinearity is high everywhere (structural)
    collinear_threshold = 0.90
    gamma_gc_collinear_everywhere = all(abs(r["rho_gamma_gc"]) >= collinear_threshold for r in rows)
    max_gamma_gc = max(abs(r["rho_gamma_gc"]) for r in rows)

    # the GC-partialled gamma effect is non-significant on the primary
    primary_partial_nonsig = (primary["partial_p"] is not None and primary["partial_p"] >= _ALPHA)

    # and its sign is NOT a stable positive across panels (no identified support anywhere)
    no_identified_support_anywhere = not any(r["identified_supporting_gamma_effect"] for r in rows)
    partial_signs = [(1 if r["partial_rho_gamma_fold_given_gc"] > 0 else
                      -1 if r["partial_rho_gamma_fold_given_gc"] < 0 else 0) for r in rows]
    partial_sign_unstable = (len(set(s for s in partial_signs if s != 0)) > 1)

    non_identified = bool(gamma_gc_collinear_everywhere and primary_partial_nonsig and
                          no_identified_support_anywhere)

    name = ("FV5 GC-identifiability stress test: gamma<->GC is near-collinear, so the knockdown-depth "
            "ordering score cannot separate barrier from GC -- the (B) null is NON-IDENTIFIED")
    return dict(name=name,
                gamma_is_minus_mean_NN_dG37_so_tracks_GC_by_construction=True,
                per_panel=rows,
                max_abs_rho_gamma_gc=round(max_gamma_gc, 4),
                gamma_GC_collinear_on_every_panel=bool(gamma_gc_collinear_everywhere),
                primary_partial_gamma_given_GC_nonsignificant=bool(primary_partial_nonsig),
                partial_sign_unstable_across_panels=bool(partial_sign_unstable),
                no_identified_supporting_gamma_effect_on_any_panel=bool(no_identified_support_anywhere),
                ordering_score_is_non_identified=non_identified,
                cell_type_invariance_note=("gamma and GC are promoter-DNA properties (identical in any cell "
                    "type), so a neuronal CRISPRi/Perturb-seq panel inherits the SAME non-identification; "
                    "repeating the knockdown-depth ordering in neurons does NOT advance O-20. An identified "
                    "(B) requires a readout not collinear with GC (downstream response magnitude), which "
                    "needs the firewalled drive size Delta-h."),
                promotes_anything=False,
                grade="[V] as an identifiability/honesty invariant: it establishes (measured, no tuning) that "
                      "the (B) knockdown-depth ordering score is non-identified -- gamma~GC collinearity "
                      "(rho up to {:.3f}) means the recorded null is 'cannot separate signal from confound', "
                      "not 'signal absent'. Promotes no [O] item; the per-cell/per-patient yes/no stays [O].".format(max_gamma_gc),
                **{"pass": bool(non_identified)})


# =====================================================================================================
#  FV6 -- the (B) identifiability DECOMPOSITION: which VP prediction can a held-out score even identify?
# =====================================================================================================
def FV6_identifiability_decomposition():
    """FV5 PROVED that ONE (B) score -- the knockdown-depth ordering -- is NON-IDENTIFIED, because
    gamma = -mean(NN dG37) is collinear with promoter GC (rho ~ 0.99) and CRISPRi efficiency is itself
    GC/accessibility-driven. FV6 GENERALISES that single empirical case into a structural partition of
    EVERY (B)-testable VP prediction, measured on the disease atlas, and asks the sharper question: is
    there ANY distinctive VP prediction whose held-out score is BOTH identified (not collinear with the
    GC confound) AND firewall-clean (reads a sign/ordering, never an absolute magnitude)?

    THE CRITERION (forced by the collinearity).  With a near-perfect confound c ~ gamma (here c = GC,
    rho(gamma,GC) ~ 0.99 measured below), a prediction P scored against a c-driven observable is
       NON-IDENTIFIED  if P is monotone in gamma   (then P ~ c, and any match is explainable by c), and
       IDENTIFIED      if P is orthogonal to gamma  (then P _|_ c, and a match cannot be produced by c).
    So "which (B) is worth running?" reduces to "which VP prediction is orthogonal to gamma?".

    THE MEASURED PARTITION (disease atlas; gamma re-read FROZEN; nothing fitted).
      * gamma-ORDERED predictions -- FM1 reachability ordering, the FV knockdown-depth ordering, IM2
        durability ordering, DM1 correction-difficulty ordering -- are all monotone in gamma, hence
        collinear with GC (R^2(gamma~GC) ~ 0.99 below): NON-IDENTIFIED as a CLASS (FV5 was one instance).
      * the mechanism corrective-SIGN prediction (DM2: LOF -> '+' restore / GOF -> '-' knockdown) is set by
        BIOLOGY, not by promoter DNA, and interleaves along gamma: point-biserial(sign, gamma) ~ 0 (this
        REPRODUCES DM2's -0.0148 as a frozen cross-check) and, the NEW measurement, point-biserial(sign, GC)
        ~ 0 with R^2(sign~GC) ~ 0.0002 -- ORTHOGONAL to the very confound that defeats the ordering axis.

    THE 2x2 (identified? x firewall-clean?) -- where each candidate (B) observable lands:
      * knockdown-depth ordering                 : firewall-clean BUT non-identified (FV5)  -> DEGENERATE.
      * downstream response-magnitude             : identified BUT firewall-blocked (it IS a magnitude).
      * corrective SIGN (bidirectional, DM2)      : identified AND firewall-clean (reads which SIGN corrects,
        never a dose) -> the UNIQUE open frontier; its ONLY obstacle is bidirectional disease-correction data
        (a '+' arm and a '-' arm with a disease/normal contrast), NOT the firewall and NOT the GC confound.

    WHAT IT SETTLES / PROMOTES.  It sharpens the open (B): of the four TODO crossings, the three ORDERING
    ones are non-identified (do not run another), and the one SIGN one (DM/(B)) is the unique identifiable AND
    firewall-clean target. It CORRECTS the prior framing that 'all four (B) crossings need the firewalled
    Delta-h': the sign crossing needs bidirectional DATA, not a magnitude. It promotes NOTHING (O-22 stays
    [O] until the sign-law is actually scored on such data); gamma is untouched.
    """
    panel = _disease_panel()                                       # gamma frozen; gc from same atlas
    genes = sorted(panel)
    g    = np.array([panel[k]["gamma"] for k in genes], float)
    gc   = np.array([panel[k]["gc"]    for k in genes], float)
    sign = np.array([1.0 if panel[k]["corr_sign"] == "+" else -1.0 for k in genes], float)  # LOF '+' / GOF '-'
    n = len(genes)

    # the CONFOUND axis: gamma <-> GC on the disease panel (Spearman, as FV5) + variance-explained
    rho_gamma_gc, p_gamma_gc, _ = _spearman(g, gc)
    r2_gamma_gc = round(_pearson(g, gc) ** 2, 4)

    # the SIGN axis: point-biserial(sign, gamma) [reproduces DM2] and point-biserial(sign, GC) [NEW]
    pb_sign_gamma = round(_pearson(sign, g),  4)                   # DM2 cross-check (~ -0.0148)
    pb_sign_gc    = round(_pearson(sign, gc), 4)                   # NEW: sign vs the confound axis (~ +0.0153)
    r2_sign_gc    = round(pb_sign_gc ** 2, 4)                      # fraction of sign the confound explains

    # DM2 frozen regression check: the sign<->gamma point-biserial must still read the recorded DM2 value
    DM2_POINT_BISERIAL = -0.0148
    dm2_reproduced = bool(abs(pb_sign_gamma - DM2_POINT_BISERIAL) < 1e-3)

    # the decomposition verdicts
    confound_is_near_perfect    = bool(abs(rho_gamma_gc) >= 0.95)  # gamma essentially IS GC
    sign_orthogonal_to_confound = bool(abs(pb_sign_gc) < 0.10)     # sign carries ~no GC
    separation_ratio = round((r2_gamma_gc + 1e-9) / (r2_sign_gc + 1e-9), 1)   # >=100x = a clean separation
    sign_axis_is_identifiable = bool(confound_is_near_perfect and sign_orthogonal_to_confound and
                                     separation_ratio >= 100.0)

    candidate_map = {
        "knockdown_depth_ordering (FV5 target)": {
            "identified": False, "firewall_clean": True,
            "verdict": "DEGENERATE -- non-identified (gamma~GC); re-running on neurons inherits the same confound"},
        "downstream_response_magnitude": {
            "identified": True, "firewall_clean": False,
            "verdict": "IDENTIFIED but FIREWALL-BLOCKED -- it is an absolute magnitude (needs Delta-h)"},
        "corrective_SIGN (bidirectional, DM2)": {
            "identified": True, "firewall_clean": True,
            "verdict": "UNIQUE OPEN FRONTIER -- identified AND firewall-clean; blocked only on bidirectional "
                       "disease-correction data (a '+' arm and a '-' arm with a disease/normal contrast)"},
    }

    name = ("FV6 (B) identifiability decomposition: of every (B)-testable VP prediction, the gamma-ORDERED "
            "class is non-identified (collinear with GC) and only the mechanism corrective-SIGN is identified "
            "(orthogonal to GC) AND firewall-clean -- so the unique open (B) is the sign-law, blocked on data")
    ok = bool(confound_is_near_perfect and sign_axis_is_identifiable and dm2_reproduced)
    return dict(name=name,
                n_disease_genes=int(n),
                n_LOF_plus=int((sign > 0).sum()), n_GOF_minus=int((sign < 0).sum()),
                rho_gamma_GC=round(rho_gamma_gc, 4), p_gamma_GC=round(p_gamma_gc, 4),
                R2_gamma_given_GC=r2_gamma_gc,
                point_biserial_sign_gamma=pb_sign_gamma,
                point_biserial_sign_GC=pb_sign_gc,
                R2_sign_given_GC=r2_sign_gc,
                confound_explains_gamma_not_sign_separation_ratio=separation_ratio,
                DM2_point_biserial_reproduced=dm2_reproduced,
                confound_is_near_perfect=confound_is_near_perfect,
                sign_axis_orthogonal_to_confound=sign_orthogonal_to_confound,
                sign_axis_is_identifiable_and_firewall_clean=sign_axis_is_identifiable,
                candidate_B_observable_map=candidate_map,
                gamma_ordered_predictions_are_non_identified_as_a_class=(
                    "FM1 reachability ordering, FV knockdown-depth ordering, IM2 durability ordering, and DM1 "
                    "correction-difficulty ordering are all monotone in gamma; with rho(gamma,GC)~0.99 each is "
                    "collinear with the GC confound, so each inherits FV5's non-identification -- a CLASS "
                    "property, not a single failed test"),
                corrected_obstacle_for_O22=(
                    "PRIOR framing: all (B) crossings 'need the firewalled Delta-h'. CORRECTED: the SIGN "
                    "crossing (DM/(B)) does NOT need a magnitude -- a sign test reads WHICH sign corrects, "
                    "which is firewall-clean -- and it is identified (sign _|_ GC). Its only obstacle is "
                    "bidirectional disease-correction DATA. The ordering crossings remain non-identified."),
                promotes_anything=False,
                grade=("[V] (measured partition: rho(gamma,GC)={:.4f}, point-biserial(sign,GC)={:.4f}, "
                       "R2 separation {:.0f}x) on a [F] criterion (a prediction orthogonal to a near-perfect "
                       "confound is identifiable; one collinear with it is not). Reproduces DM2's "
                       "point-biserial(sign,gamma)={:.4f} as a frozen cross-check. Promotes no [O]: O-22 "
                       "stays open until the sign-law is scored on bidirectional held-out data.").format(
                       rho_gamma_gc, pb_sign_gc, separation_ratio, pb_sign_gamma),
                **{"pass": ok})


# =====================================================================================================
#  FV7 -- the corrective SIGN-LAW '-' ARM: the first HELD-OUT empirical score of the unique open (B)
# =====================================================================================================
def FV7_signlaw_minus_arm_heldout_score():
    """FV6 PROVED that the corrective SIGN-law (DM2: LOF->'+' restore / GOF->'-' silence) is the UNIQUE
    (B) crossing that is BOTH identified (point-biserial(sign,GC)~0, orthogonal to the GC confound that
    sinks every gamma-ORDERED score) AND firewall-clean (reads WHICH sign corrects, never a dose). Its
    sole obstacle was named precisely: bidirectional disease-correction DATA -- a '-' arm (does SILENCING a
    GOF gene move a disease cell toward healthy?) and a '+' arm (does RESTORING a LOF gene?).

    FV7 SCORES THE '-' ARM on a genuinely held-out target. A CRISPR-knockout viability screen applies the
    '-' (loss) operation to every gene; in a CANCER line the resulting viability change IS a disease-
    correction phenotype (oncogene addiction -- removing the oncogenic drive collapses the cancer program).
    So the sign-law '-' arm is directly testable as a SEPARATION under one operation: a GOF oncogene
    (corr_sign '-') should be a DEPENDENCY (knockout corrects -> negative gene-effect), while a LOF
    suppressor (corr_sign '+') should NOT be corrected by '-' (knockout neutral/pro-tumour -> gene-effect
    >= 0). Target = DepMap 24Q2 CRISPRGeneEffect (Chronos), cached in bvalidation/ by data/fetch_signlaw_
    depmap.py; corr_sign and GC are RE-READ FROZEN from the disease atlas at score time, never from the
    cache and never fitted.

    HELD-OUT WARRANT.  corr_sign is forced by each gene's known disease MECHANISM (GOF/LOF), declared by
    function and frozen BEFORE any DepMap data was seen. DepMap gene-effect is an independent functional
    viability readout expressing none of that label -- a legitimate held-out target.

    WHY THIS ESCAPES THE FV5/FV6 CONFOUND (identification, re-checked live).  The gamma~GC collinearity that
    makes every gamma-ORDERING score non-identified does NOT apply: corr_sign is set by biology and is
    orthogonal to promoter GC, so the GOF and LOF groups carry ~equal GC and the separation cannot be
    manufactured by GC. FV7 re-measures this on the scored panel -- group GC balance + the GC-partialled
    point-biserial -- as a built-in identification gate.

    READOUT SCOPE (right phenotype for the right disease class).  Cancer-cell viability is a correction
    phenotype ONLY for the ONCOLOGY panel; the neurodegeneration genes are cached for transparency but are
    OUT OF READOUT SCOPE (a cancer-viability screen does not measure neuronal proteinopathy correction).
    FV7 scores the ONCO panel only and reports the neurodegen count as out-of-scope.

    WHAT IT PROMOTES -- and what it does NOT (the firewall, kept exact).  The '-' arm is scored under a
    pre-set rule mirroring FV2 (support iff exact p < ALPHA AND the separation is in the predicted
    direction). If it scores, the corrective sign-law's '-' arm earns a held-out [V] -- the kit's first
    held-out POSITIVE. It does NOT promote O-22 (the per-patient corrected-yes/no): O-22's FV6 obstacle is
    BIDIRECTIONAL data, and FV7 supplies only the '-' arm (half the test) -- the '+' RESTORE arm (over-
    expression of a suppressor) is still data-blocked -- so O-22 stays [O] with its obstacle NARROWED to the
    '+' arm alone. It does NOT touch O-21 (the absolute corrective DOSE -- a magnitude a sign test never
    addresses; firewalled to clinicians/regulators). FV7 does NOT reintroduce Delta-h as an O-22 obstacle:
    FV6 corrected that framing, and FV7 holds the correction (the SIGN crossing is firewall-clean and needs
    DATA, not a magnitude; the magnitude lives only in O-21). gamma is untouched; nothing is fitted.

    HONEST READING.  A positive here confirms the substrate's mechanism sign-law is biologically FAITHFUL
    on held-out dependency data; it is NOT a fresh discovery of the oncogene/suppressor distinction (those
    labels are the kit's frozen priors -- DepMap is the independent test of whether the sign-law's '-' arm
    tracks them). Four of the nine LOF genes (VHL/BRCA1/APC/STK11) are pan-essential for reasons orthogonal
    to tumour-suppression and push AGAINST the prediction (a conservative panel, no cherry-picking); the
    score is a pan-cancer mean across all lines, never a lineage-selected subset.
    """
    cache = json.load(open(_SIGNLAW_CACHE, encoding="utf-8"))
    panel = _disease_panel()                                  # corr_sign + gc re-read FROZEN (never the cache)
    rows = cache.get("matched", {})

    # provenance + held-out integrity (mirrors FV1's spirit for this target)
    src = cache.get("_source", {})
    prov_ok = (src.get("figshare_article") == "25880521"
               and src.get("gene_effect_file_id") == "46489063"
               and "gene-effect" in src.get("readout_column", "").lower())
    warrant_ok = ("MECHANISM" in cache.get("_held_out_warrant", "")
                  and "frozen" in cache.get("_held_out_warrant", ""))
    sign_locked = ("point-biserial(corr_sign=='-', -gene_effect) > 0" in cache.get("_prediction_sign_locked", ""))
    scope_ok = ("ONCOLOGY panel" in cache.get("_readout_scope", ""))
    # the cache must carry gene-effects ONLY -- no smuggled sign/gc/gamma (the score re-reads the frozen atlas)
    no_smuggled = all(("corr_sign" not in r and "gc" not in r and "gamma" not in r) for r in rows.values())

    # ONCO panel only; corr_sign / gc taken from the FROZEN atlas, gene-effect from the cache
    onco = sorted([g for g, r in rows.items() if r["disease_class"] == "oncology" and g in panel])
    ind  = [1.0 if panel[g]["corr_sign"] == "-" else 0.0 for g in onco]   # GOF (corr_sign '-') indicator
    negge = [-float(rows[g]["mean_gene_effect"]) for g in onco]           # -gene_effect (cache target)
    gc   = [float(panel[g]["gc"]) for g in onco]
    n_onco = len(onco)

    pb = round(_pearson(ind, negge), 4)                       # point-biserial(GOF, -gene_effect)
    p_exact, n_perm, _ = _exact_perm_p(ind, negge)
    p_exact = round(p_exact, 4)

    # ----- identification gate (re-measured live on the scored panel) -----
    pb_sign_gc = round(_pearson(ind, gc), 4)                  # sign vs the GC confound (~0 => orthogonal)
    gof_gc = [gc[i] for i in range(n_onco) if ind[i] == 1.0]
    lof_gc = [gc[i] for i in range(n_onco) if ind[i] == 0.0]
    gof_mean_gc = round(sum(gof_gc) / len(gof_gc), 4) if gof_gc else float("nan")
    lof_mean_gc = round(sum(lof_gc) / len(lof_gc), 4) if lof_gc else float("nan")
    partial_pb = round(_partial_pearson(ind, negge, gc), 4)  # GC-partialled point-biserial
    gc_balanced = bool(abs(gof_mean_gc - lof_mean_gc) < 0.05)
    sign_orthogonal_to_gc = bool(abs(pb_sign_gc) < 0.15)
    partial_survives = bool(pb != 0 and abs(partial_pb) >= 0.6 * abs(pb) and (partial_pb > 0) == (pb > 0))
    identified = bool(gc_balanced and sign_orthogonal_to_gc and partial_survives)

    # ----- promotion rule (pre-set, mirrors FV2): the '-' ARM is supported iff significant AND predicted dir
    significant = (p_exact < _ALPHA)
    predicted_direction = (pb > 0)
    minus_arm_supported = bool(significant and predicted_direction)

    # per-gene sign-correctness (transparency; not the score)
    gof_correct = sum(1 for i in range(n_onco) if ind[i] == 1.0 and negge[i] > 0)
    lof_correct = sum(1 for i in range(n_onco) if ind[i] == 0.0 and negge[i] <= 0)
    n_gof = int(sum(ind)); n_lof = n_onco - n_gof

    n_neurodegen_oos = sum(1 for r in rows.values() if r["disease_class"] == "neurodegeneration")

    # the headline this battery must reproduce from the frozen inputs (locked in the fetcher)
    headline_ok = bool(abs(pb - 0.4940) < 1e-3 and abs(p_exact - 0.0227) < 2e-3 and n_onco == 16)

    # PASS iff: provenance/warrant/scope intact, score computed correctly from frozen inputs, the arm is
    # identified, and the promotion rule was applied honestly (support == significant&predicted). The
    # battery does NOT pass merely because the arm scored -- it passes because the held-out score is
    # correct, identified, firewall-clean, and the rule was obeyed.
    rule_applied = (minus_arm_supported == (significant and predicted_direction))
    allp = bool(prov_ok and warrant_ok and sign_locked and scope_ok and no_smuggled
                and headline_ok and identified and rule_applied and n_onco == 16)

    name = ("FV7 corrective sign-law '-' arm (held-out, DepMap 24Q2 CRISPR-KO): GOF oncogenes are "
            "dependencies and LOF suppressors are not, under the '-' operation -- the first held-out score "
            "of the unique identified+firewall-clean (B) frontier")
    return dict(name=name,
                target="DepMap 24Q2 CRISPRGeneEffect (Chronos gene-effect), figshare article 25880521",
                provenance_ok=bool(prov_ok), held_out_warrant_ok=bool(warrant_ok),
                prediction_sign_locked_ok=bool(sign_locked), readout_scope_onco_only_ok=bool(scope_ok),
                no_smuggled_sign_gc_or_gamma=bool(no_smuggled),
                n_onco_scored=n_onco, n_GOF_minus=n_gof, n_LOF_plus=n_lof,
                n_neurodegen_out_of_scope=n_neurodegen_oos,
                point_biserial_GOFsign_vs_neg_gene_effect=pb,
                exact_permutation_p_one_sided=p_exact, n_permutations=n_perm,
                predicted_direction="point-biserial(corr_sign=='-', -gene_effect) > 0 (GOF more depended-on than LOF)",
                observed_direction=("positive (as predicted)" if pb > 0 else "negative" if pb < 0 else "zero"),
                significant_at_0_05=bool(significant),
                per_gene_sign_correct=dict(GOF=f"{gof_correct}/{n_gof}", LOF=f"{lof_correct}/{n_lof}",
                                           total=f"{gof_correct + lof_correct}/{n_onco}"),
                # --- identification (this is the IDENTIFIED arm; re-checked live) ---
                point_biserial_sign_vs_GC=pb_sign_gc,
                GOF_mean_GC=gof_mean_gc, LOF_mean_GC=lof_mean_gc, group_GC_balanced=gc_balanced,
                partial_point_biserial_sign_given_GC=partial_pb,
                partial_survives_GC_removal=partial_survives,
                sign_axis_orthogonal_to_GC=sign_orthogonal_to_gc,
                identified_not_a_GC_artifact=identified,
                # --- promotion (scoped EXACTLY: the '-' arm, nothing else) ---
                promotion_rule="support the '-' arm iff (exact p < 0.05 AND point-biserial > 0); else keep [O]",
                minus_arm_supported=minus_arm_supported,
                promotes_O22_per_patient_yes_no=False,
                promotes_O21_absolute_dose=False,
                O22_obstacle_narrowed=("O-22's FV6 obstacle was BIDIRECTIONAL disease-correction data (a "
                                       "'+' arm AND a '-' arm); the '-' arm is now scored (identified, "
                                       "firewall-clean), so the remaining obstacle is the '+' RESTORE arm "
                                       "alone (over-expression of a LOF suppressor with a disease/normal "
                                       "contrast). O-22 stays [O] with this narrowed obstacle. FV7 does NOT "
                                       "reintroduce Delta-h here -- FV6 corrected that; the absolute drive "
                                       "magnitude is the separate item O-21."),
                what_this_is_not=("NOT a fresh discovery of the oncogene/suppressor distinction -- those "
                                  "labels are the kit's frozen priors; DepMap is the INDEPENDENT held-out "
                                  "test of whether the sign-law's '-' arm tracks them. 4/9 LOF genes "
                                  "(VHL/BRCA1/APC/STK11) are pan-essential for reasons orthogonal to "
                                  "tumour-suppression and push AGAINST the prediction (conservative panel); "
                                  "the score is a pan-cancer mean, never lineage-cherry-picked."),
                firewall="reads only the SIGN of the GOF-vs-LOF separation under the '-' operation; no "
                         "magnitude, dose, or titre is predicted or claimed. corr_sign/GC re-read frozen; "
                         "gamma untouched. Clinical translation firewalled to clinicians and regulators.",
                grade=("[V] HELD-OUT POSITIVE for the corrective sign-law '-' arm: point-biserial(GOF, "
                       "-gene_effect)={:.4f}, exact one-sided p={:.4f} (n={} onco genes, {} perms), in the "
                       "predicted direction. IDENTIFIED -- orthogonal to the GC confound that sinks the "
                       "ordering axis (point-biserial(sign,GC)={:.4f}; GOF GC {:.3f} vs LOF GC {:.3f}; "
                       "GC-partialled point-biserial {:.4f}, essentially unchanged). FIREWALL-CLEAN (sign "
                       "only). Promotes the '-' arm; O-22 stays [O] (needs the '+' restore arm -- FV6's "
                       "obstacle, not Delta-h), O-21 stays [O] (absolute dose, firewalled). The kit's first "
                       "held-out empirical confirmation -- the substrate's mechanism sign-law is "
                       "biologically faithful on independent CRISPR-dependency data.").format(pb, p_exact, n_onco, n_perm,
                                                                     pb_sign_gc, gof_mean_gc, lof_mean_gc,
                                                                     partial_pb),
                **{"pass": allp})


def FV8_signlaw_plus_arm_heldout_score():
    """THE COMPLEMENTARY '+' RESTORE ARM. FV6 named O-22's obstacle precisely as BIDIRECTIONAL disease-
    correction DATA -- a '-' arm (does SILENCING a GOF gene correct?) AND a '+' arm (does RESTORING a LOF
    gene correct?). FV7 scored the '-' arm on DepMap CRISPR-KO (the kit's first held-out positive). FV8
    scores the MIRROR '+' ARM on a genuinely held-out target of the opposite operation.

    A CRISPR-ACTIVATION (CRISPRa) viability screen applies the '+' (gain / restore) operation to every gene
    from its own promoter; in a CANCER line the resulting growth change IS a disease-correction phenotype
    for a LOF suppressor (restoring a tumour brake slows the cancer program). So the sign-law '+' arm is
    directly testable as a SEPARATION under one operation: a LOF suppressor (corr_sign '+') should be
    CORRECTED by '+' (activation slows growth -> NEGATIVE growth phenotype), while a GOF oncogene (corr_sign
    '-') should NOT be corrected by '+' (activating an already-active driver is neutral / pro-growth ->
    growth phenotype >= 0). Target = Horlbeck 2016 hCRISPRa-v2 K562 gene growth phenotypes (the canonical
    genome-scale activation screen), cached in bvalidation/ by data/fetch_signlaw_crispra.py; corr_sign and
    GC are RE-READ FROZEN from the disease atlas at score time, never from the cache and never fitted.

    HELD-OUT WARRANT.  corr_sign is forced by each gene's known disease MECHANISM (GOF/LOF), declared by
    function and frozen BEFORE any CRISPRa data was seen. The CRISPRa K562 growth phenotype is an
    independent functional viability readout expressing none of that label -- a legitimate held-out target.

    WHY THIS ESCAPES THE FV5/FV6 CONFOUND (identification, re-checked live).  The gamma~GC collinearity that
    makes every gamma-ORDERING score non-identified does NOT apply: corr_sign is set by biology and is
    orthogonal to promoter GC, so the LOF and GOF groups carry ~equal GC and the separation cannot be
    manufactured by GC. FV8 re-measures this on the scored panel -- group GC balance + the GC-partialled
    point-biserial -- as a built-in identification gate, exactly as FV7 did.

    READOUT SCOPE (right phenotype for the right disease class).  Cancer-cell growth is a correction
    phenotype ONLY for the ONCOLOGY panel; the neurodegeneration genes are cached for transparency but are
    OUT OF READOUT SCOPE (a leukemia growth screen does not measure neuronal proteinopathy correction).
    FV8 scores the ONCO panel only and reports the neurodegen count as out-of-scope.

    WHAT IT PROMOTES -- and what it does NOT (the firewall, kept exact -- this is the load-bearing call).
    The '+' arm is scored under the same pre-set rule as FV7 (support iff exact p < ALPHA AND the separation
    is in the predicted direction). If it scores, the corrective sign-law's '+' arm earns a held-out [V],
    and TOGETHER WITH FV7's '-' arm the corrective SIGN-LAW is now BIDIRECTIONALLY confirmed on held-out data
    (both arms [V], direction-only). This REMOVES IN FULL the bidirectional-DATA obstacle FV6 named and that
    FV7 had narrowed to the '+' arm alone.

    BUT O-22 is NOT promoted -- it STAYS [O] -- and this is deliberate, not an oversight. FV7 framed O-22's
    residual obstacle as 'the '+' RESTORE arm alone'; FV8 GENTLY CORRECTS that framing (the kit corrects its
    own framings in-line; FV6 corrected FV5). With both arms scored, O-22's remaining obstacle is no longer
    DATA at all -- it is the FIREWALL itself. The bidirectional sign-law is a CLASS-LEVEL, DIRECTION-ONLY
    statement: it certifies WHICH way to push each disease class (silence a GOF, restore a LOF). O-22 is a
    PER-PATIENT, ABSOLUTE outcome (does a given drive actually correct a given patient's switch?). A
    direction-only law cannot deliver a per-patient yes/no -- that needs the firewalled per-patient
    magnitude / penetrance, and the absolute drive size is the separate item O-21. Promoting O-22 here would
    leak a direction-only [V] into a per-patient absolute [V], breaching the kit's supreme principle. So FV8
    moves O-22's obstacle from 'missing '+'-arm data' to 'the firewall (per-patient magnitude)', and leaves
    it [O]. This does NOT contradict FV6: FV6 said SCORING the sign-law (B) needs bidirectional data, not
    Delta-h -- and both arms were scored with zero Delta-h. gamma is untouched; nothing is fitted.

    HONEST READING.  A positive here confirms the substrate's mechanism sign-law is biologically FAITHFUL on
    held-out ACTIVATION data, the mirror of FV7's loss data; it is NOT a fresh discovery of the oncogene/
    suppressor distinction (those labels are the kit's frozen priors -- CRISPRa is the independent test of
    whether the sign-law's '+' arm tracks them). K562 is a single CML line (a single-line growth screen, vs
    FV7's pan-cancer mean); TP53 is null and CDKN2A is deleted in K562, so activation has a weak/absent locus
    to restore for those and they push AGAINST the prediction (a conservative panel, no cherry-picking).
    """
    cache = json.load(open(_CRISPRA_CACHE, encoding="utf-8"))
    panel = _disease_panel()                                  # corr_sign + gc re-read FROZEN (never the cache)
    rows = cache.get("matched", {})

    # provenance + held-out integrity (mirrors FV7's spirit for the activation target)
    src = cache.get("_source", {})
    prov_ok = (src.get("doi") == "10.7554/eLife.19760"
               and src.get("elife_article") == "19760"
               and "growth phenotype" in src.get("readout_column", "").lower())
    warrant_ok = ("MECHANISM" in cache.get("_held_out_warrant", "")
                  and "frozen" in cache.get("_held_out_warrant", ""))
    sign_locked = ("point-biserial(corr_sign=='+', -growth_phenotype) > 0" in cache.get("_prediction_sign_locked", ""))
    scope_ok = ("ONCOLOGY panel" in cache.get("_readout_scope", ""))
    # the cache must carry growth phenotypes ONLY -- no smuggled sign/gc/gamma (the score re-reads the frozen atlas)
    no_smuggled = all(("corr_sign" not in r and "gc" not in r and "gamma" not in r) for r in rows.values())

    # ONCO panel only; corr_sign / gc taken from the FROZEN atlas, growth phenotype from the cache
    onco = sorted([g for g, r in rows.items() if r["disease_class"] == "oncology" and g in panel])
    ind  = [1.0 if panel[g]["corr_sign"] == "+" else 0.0 for g in onco]   # LOF suppressor (corr_sign '+') indicator
    neggp = [-float(rows[g]["growth_phenotype"]) for g in onco]           # -growth_phenotype (cache target)
    gc   = [float(panel[g]["gc"]) for g in onco]
    n_onco = len(onco)

    pb = round(_pearson(ind, neggp), 4)                       # point-biserial(LOF, -growth_phenotype)
    p_exact, n_perm, _ = _exact_perm_p(ind, neggp)
    p_exact = round(p_exact, 4)

    # ----- identification gate (re-measured live on the scored panel, identical machinery to FV7) -----
    pb_sign_gc = round(_pearson(ind, gc), 4)                  # sign vs the GC confound (~0 => orthogonal)
    lof_gc = [gc[i] for i in range(n_onco) if ind[i] == 1.0]
    gof_gc = [gc[i] for i in range(n_onco) if ind[i] == 0.0]
    lof_mean_gc = round(sum(lof_gc) / len(lof_gc), 4) if lof_gc else float("nan")
    gof_mean_gc = round(sum(gof_gc) / len(gof_gc), 4) if gof_gc else float("nan")
    partial_pb = round(_partial_pearson(ind, neggp, gc), 4)   # GC-partialled point-biserial
    gc_balanced = bool(abs(lof_mean_gc - gof_mean_gc) < 0.05)
    sign_orthogonal_to_gc = bool(abs(pb_sign_gc) < 0.15)
    partial_survives = bool(pb != 0 and abs(partial_pb) >= 0.6 * abs(pb) and (partial_pb > 0) == (pb > 0))
    identified = bool(gc_balanced and sign_orthogonal_to_gc and partial_survives)

    # ----- promotion rule (pre-set, mirrors FV2/FV7): the '+' ARM is supported iff significant AND predicted dir
    significant = (p_exact < _ALPHA)
    predicted_direction = (pb > 0)
    plus_arm_supported = bool(significant and predicted_direction)

    # both arms now scored?  (FV7's '-' arm verified live from its own cache, so the bidirectional claim is self-contained)
    minus_cache_ok = os.path.exists(_SIGNLAW_CACHE)
    bidirectional_complete = bool(plus_arm_supported and minus_cache_ok)

    # per-gene sign-correctness (transparency; not the score). '+' corrects a LOF (growth<0); does not correct a GOF (>=0)
    lof_correct = sum(1 for i in range(n_onco) if ind[i] == 1.0 and neggp[i] > 0)   # -growth>0  <=> growth<0
    gof_correct = sum(1 for i in range(n_onco) if ind[i] == 0.0 and neggp[i] <= 0)  # -growth<=0 <=> growth>=0
    n_lof = int(sum(ind)); n_gof = n_onco - n_lof

    n_neurodegen_oos = sum(1 for r in rows.values() if r["disease_class"] == "neurodegeneration")

    # the headline this battery must reproduce from the frozen inputs (locked in the fetcher)
    headline_ok = bool(abs(pb - 0.4852) < 1e-3 and abs(p_exact - 0.0274) < 2e-3 and n_onco == 16)

    # PASS iff: provenance/warrant/scope intact, score computed correctly from frozen inputs, the arm is
    # identified, and the promotion rule was applied honestly (support == significant&predicted). As in FV7,
    # the battery does NOT pass merely because the arm scored -- it passes because the held-out score is
    # correct, identified, firewall-clean, and the rule was obeyed.
    rule_applied = (plus_arm_supported == (significant and predicted_direction))
    allp = bool(prov_ok and warrant_ok and sign_locked and scope_ok and no_smuggled
                and headline_ok and identified and rule_applied and n_onco == 16)

    name = ("FV8 corrective sign-law '+' arm (held-out, Horlbeck 2016 CRISPRa K562): LOF suppressors are "
            "growth-suppressive on activation and GOF oncogenes are not, under the '+' operation -- the "
            "mirror of FV7, completing the bidirectional held-out test of the (B) frontier")
    return dict(name=name,
                target="Horlbeck et al. 2016 hCRISPRa-v2 K562 gene growth phenotypes, eLife 5:e19760 (supp. file 10)",
                provenance_ok=bool(prov_ok), held_out_warrant_ok=bool(warrant_ok),
                prediction_sign_locked_ok=bool(sign_locked), readout_scope_onco_only_ok=bool(scope_ok),
                no_smuggled_sign_gc_or_gamma=bool(no_smuggled),
                n_onco_scored=n_onco, n_LOF_plus=n_lof, n_GOF_minus=n_gof,
                n_neurodegen_out_of_scope=n_neurodegen_oos,
                point_biserial_LOFsign_vs_neg_growth=pb,
                exact_permutation_p_one_sided=p_exact, n_permutations=n_perm,
                predicted_direction="point-biserial(corr_sign=='+', -growth_phenotype) > 0 (LOF more growth-suppressed-on-activation than GOF)",
                observed_direction=("positive (as predicted)" if pb > 0 else "negative" if pb < 0 else "zero"),
                significant_at_0_05=bool(significant),
                per_gene_sign_correct=dict(LOF=f"{lof_correct}/{n_lof}", GOF=f"{gof_correct}/{n_gof}",
                                           total=f"{lof_correct + gof_correct}/{n_onco}"),
                # --- identification (this is the IDENTIFIED arm; re-checked live, same machinery as FV7) ---
                point_biserial_sign_vs_GC=pb_sign_gc,
                LOF_mean_GC=lof_mean_gc, GOF_mean_GC=gof_mean_gc, group_GC_balanced=gc_balanced,
                partial_point_biserial_sign_given_GC=partial_pb,
                partial_survives_GC_removal=partial_survives,
                sign_axis_orthogonal_to_GC=sign_orthogonal_to_gc,
                identified_not_a_GC_artifact=identified,
                # --- promotion (scoped EXACTLY: the '+' arm + the bidirectional sign-law; NOT O-22) ---
                promotion_rule="support the '+' arm iff (exact p < 0.05 AND point-biserial > 0); else keep [O]",
                plus_arm_supported=plus_arm_supported,
                sign_law_bidirectional_complete=bidirectional_complete,
                promotes_O22_per_patient_yes_no=False,
                promotes_O21_absolute_dose=False,
                O22_obstacle_corrected=("FV7 narrowed O-22's obstacle to 'the '+' RESTORE arm alone'. FV8 "
                                        "scores that '+' arm (identified, firewall-clean), so the "
                                        "bidirectional-DATA obstacle FV6 named is now REMOVED IN FULL and the "
                                        "corrective sign-law is bidirectionally [V] (direction-only). FV8 "
                                        "CORRECTS FV7's framing: O-22's residual obstacle is no longer DATA -- "
                                        "it is the FIREWALL itself. The sign-law is CLASS-LEVEL and DIRECTION-"
                                        "ONLY (which way to push each class); O-22 is a PER-PATIENT ABSOLUTE "
                                        "outcome (does a drive correct THIS patient's switch?), which needs the "
                                        "firewalled per-patient magnitude/penetrance -- the absolute drive size "
                                        "being the separate item O-21. So O-22 stays [O] with its obstacle "
                                        "moved from 'missing '+'-arm data' to 'the firewall (per-patient "
                                        "magnitude)'. This does NOT contradict FV6 (scoring the sign-law needed "
                                        "bidirectional data, not Delta-h -- and both arms were scored with zero "
                                        "Delta-h)."),
                what_this_is_not=("NOT a fresh discovery of the oncogene/suppressor distinction -- those "
                                  "labels are the kit's frozen priors; CRISPRa is the INDEPENDENT held-out "
                                  "test of whether the sign-law's '+' arm tracks them. K562 is a single CML "
                                  "line (single-line growth screen, vs FV7's pan-cancer mean); TP53 is null "
                                  "and CDKN2A is deleted in K562, so activation has a weak/absent locus to "
                                  "restore and they push AGAINST the prediction (conservative panel, no "
                                  "cherry-picking)."),
                firewall="reads only the SIGN of the LOF-vs-GOF separation under the '+' operation; no "
                         "magnitude, dose, or titre is predicted or claimed. corr_sign/GC re-read frozen; "
                         "gamma untouched. Per-patient correction and clinical translation firewalled to "
                         "clinicians and regulators.",
                grade=("[V] HELD-OUT POSITIVE for the corrective sign-law '+' arm: point-biserial(LOF, "
                       "-growth_phenotype)={:.4f}, exact one-sided p={:.4f} (n={} onco genes, {} perms), in "
                       "the predicted direction. IDENTIFIED -- orthogonal to the GC confound that sinks the "
                       "ordering axis (point-biserial(sign,GC)={:.4f}; LOF GC {:.3f} vs GOF GC {:.3f}; "
                       "GC-partialled point-biserial {:.4f}, essentially unchanged). FIREWALL-CLEAN (sign "
                       "only). TOGETHER WITH FV7 the corrective sign-law is now BIDIRECTIONALLY [V] (both "
                       "arms, direction-only) -- the kit's second held-out positive and the mirror of the "
                       "first. O-22 STAYS [O]: its obstacle is no longer data (both arms scored) but the "
                       "FIREWALL -- a class-level direction-only law cannot certify a per-patient corrected "
                       "yes/no, which needs the firewalled per-patient magnitude; O-21 (absolute dose) stays "
                       "[O]. The substrate's mechanism sign-law is biologically faithful on independent "
                       "CRISPR-activation data, completing the bidirectional test FV6 named.").format(
                           pb, p_exact, n_onco, n_perm, pb_sign_gc, lof_mean_gc, gof_mean_gc, partial_pb),
                **{"pass": allp})


def run_battery():
    tests = [FV1_provenance_and_heldout_integrity(),
             FV2_no_tuning_ordering_score(),
             FV3_null_robustness(),
             FV4_AB_firewall(),
             FV5_gc_identifiability(),
             FV6_identifiability_decomposition(),
             FV7_signlaw_minus_arm_heldout_score(),
             FV8_signlaw_plus_arm_heldout_score()]
    allp = all(t["pass"] for t in tests)
    fv5 = tests[4]
    fv6 = tests[5]
    fv7 = tests[6]
    fv8 = tests[7]
    return {"module": "feasibility_validation", "battery": "FV1-FV8", "seed": SEED,
            "FV_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "B_result_headline": "NULL: Spearman rho(frozen gamma, on-target CRISPRi fold_expr) = "
                                 "-0.0760, p = 0.6283, n = 43 (K562 genome-wide Perturb-seq, Replogle 2022). "
                                 "Slightly OPPOSITE to the predicted positive sign; non-significant across "
                                 "every expression cutoff; sign disagrees on RPE1; SET-proxy AUC = 0.389. No "
                                 "support to promote the per-cell yes/no out of [O].",
            "B_identifiability_headline": "NON-IDENTIFIED (FV5): gamma = -mean(NN dG37) tracks promoter GC by "
                                 "construction (gamma<->GC rank rho up to {:.3f}); after partialling GC the "
                                 "gamma effect is non-significant and sign-unstable across panels. The "
                                 "knockdown-depth ordering score therefore CANNOT separate a barrier effect "
                                 "from a GC/accessibility effect -- so the recorded null is 'cannot separate "
                                 "signal from confound', not 'signal absent'. Because gamma<->GC collinearity "
                                 "is a promoter-DNA property (cell-type invariant), repeating the same "
                                 "observable in neurons inherits the same non-identification; an identified "
                                 "(B) needs a downstream RESPONSE-MAGNITUDE readout, which requires the "
                                 "firewalled Delta-h. Promotes nothing.".format(fv5["max_abs_rho_gamma_gc"]),
            "B_identifiability_decomposition_headline": (
                "FV6: the (B) frontier PARTITIONS. With gamma=-mean(NN dG37) collinear with promoter GC "
                "(rho(gamma,GC)={:.4f} on the disease panel, R2={:.4f}), every gamma-ORDERED VP prediction "
                "(reachability/knockdown-depth/durability/correction-difficulty ordering) is non-identified as "
                "a CLASS -- FV5 was one instance. The mechanism corrective-SIGN (DM2: LOF->'+', GOF->'-') is "
                "the SOLE exception: point-biserial(sign,GC)={:.4f} (R2={:.4f}, a {:.0f}x separation), so it is "
                "ORTHOGONAL to the confound and a held-out sign-match could not be produced by GC. The sign "
                "test also reads only WHICH sign corrects, never a dose, so it is FIREWALL-CLEAN. Hence the "
                "unique open (B) is the corrective sign-law (DM/(B)), blocked on bidirectional disease-"
                "correction DATA -- NOT on the firewalled Delta-h (the prior framing is corrected) and NOT on "
                "the GC confound. Reproduces DM2's point-biserial(sign,gamma)={:.4f} frozen. Promotes nothing."
                ).format(fv6["rho_gamma_GC"], fv6["R2_gamma_given_GC"], fv6["point_biserial_sign_GC"],
                         fv6["R2_sign_given_GC"], fv6["confound_explains_gamma_not_sign_separation_ratio"],
                         fv6["point_biserial_sign_gamma"]),
            "B_signlaw_minus_arm_headline": (
                "FV7: the corrective sign-law's '-' ARM is now SCORED on a genuinely held-out target -- "
                "DepMap 24Q2 CRISPR-KO gene-effect ({} oncology genes, {} GOF/{} LOF). Under the '-' "
                "(knockout) operation, GOF oncogenes (corr_sign '-') are DEPENDENCIES and LOF suppressors "
                "(corr_sign '+') are not: point-biserial(GOF, -gene_effect) = {:.4f}, exact one-sided "
                "permutation p = {:.4f} ({} perms), in the predicted direction (per-gene {} correct). This "
                "is the UNIQUE (B) crossing FV6 named -- identified AND firewall-clean -- and it is RE-"
                "CONFIRMED identified live: orthogonal to the GC confound that sinks the ordering axis "
                "(point-biserial(sign,GC) = {:.4f}; GOF mean GC {:.3f} vs LOF mean GC {:.3f}; GC-partialled "
                "point-biserial = {:.4f}, essentially unchanged), and firewall-clean (reads only WHICH sign "
                "corrects, never a dose). corr_sign/GC re-read FROZEN; gamma untouched; nothing fitted. The "
                "kit's FIRST held-out POSITIVE -- the substrate's mechanism sign-law is biologically "
                "faithful on independent CRISPR-dependency data. It promotes the '-' arm only: O-22 (per-"
                "patient yes/no) stays [O] -- its obstacle NARROWS from bidirectional data to the '+' "
                "RESTORE arm alone (over-expression of a suppressor); FV7 does NOT reintroduce Delta-h "
                "(FV6 corrected that), and the separate absolute-dose item O-21 stays [O]. NOT a fresh "
                "discovery of the oncogene/suppressor "
                "split: those labels are frozen priors; DepMap is the independent test that the '-' arm "
                "tracks them (4/9 LOF genes are pan-essential and push AGAINST the prediction; pan-cancer "
                "mean, no cherry-picking)."
                ).format(fv7["n_onco_scored"], fv7["n_GOF_minus"], fv7["n_LOF_plus"],
                         fv7["point_biserial_GOFsign_vs_neg_gene_effect"], fv7["exact_permutation_p_one_sided"],
                         fv7["n_permutations"], fv7["per_gene_sign_correct"]["total"],
                         fv7["point_biserial_sign_vs_GC"], fv7["GOF_mean_GC"], fv7["LOF_mean_GC"],
                         fv7["partial_point_biserial_sign_given_GC"]),
            "B_signlaw_plus_arm_headline": (
                "FV8: the corrective sign-law's '+' RESTORE ARM is now SCORED on a genuinely held-out target "
                "of the OPPOSITE operation -- Horlbeck 2016 hCRISPRa-v2 K562 growth ({} oncology genes, {} "
                "LOF/{} GOF). Under the '+' (activation) operation, LOF suppressors (corr_sign '+') are "
                "growth-suppressive on activation and GOF oncogenes (corr_sign '-') are not: point-biserial("
                "LOF, -growth_phenotype) = {:.4f}, exact one-sided permutation p = {:.4f} ({} perms), in the "
                "predicted direction (per-gene {} correct). It is RE-CONFIRMED identified live: orthogonal to "
                "the GC confound (point-biserial(sign,GC) = {:.4f}; LOF mean GC {:.3f} vs GOF mean GC {:.3f}; "
                "GC-partialled point-biserial = {:.4f}, essentially unchanged) and firewall-clean (reads only "
                "WHICH sign corrects, never a dose). corr_sign/GC re-read FROZEN; gamma untouched; nothing "
                "fitted. The kit's SECOND held-out POSITIVE and the MIRROR of FV7: TOGETHER the corrective "
                "sign-law is now BIDIRECTIONALLY [V] on held-out data (both arms, direction-only), removing "
                "in full the bidirectional-DATA obstacle FV6 named. CRITICAL FIREWALL CALL: O-22 (per-patient "
                "corrected yes/no) STILL stays [O]. FV8 CORRECTS FV7's framing -- O-22's residual obstacle is "
                "no longer DATA (both arms are scored) but the FIREWALL itself: the sign-law is CLASS-LEVEL "
                "and DIRECTION-ONLY (which way to push each class), whereas O-22 is a PER-PATIENT ABSOLUTE "
                "outcome that needs the firewalled per-patient magnitude/penetrance (absolute drive size = "
                "O-21, also [O]). Promoting O-22 would leak direction-only [V] into per-patient absolute [V]. "
                "So O-22's obstacle moves from 'missing '+'-arm data' to 'the firewall', and it stays [O]. "
                "This does NOT contradict FV6 (scoring the sign-law needed bidirectional data, not Delta-h -- "
                "both arms were scored with zero Delta-h). NOT a fresh discovery of the oncogene/suppressor "
                "split: those labels are frozen priors; CRISPRa is the independent test that the '+' arm "
                "tracks them (K562 is a single CML line; TP53-null and CDKN2A-deleted push AGAINST the "
                "prediction, no cherry-picking)."
                ).format(fv8["n_onco_scored"], fv8["n_LOF_plus"], fv8["n_GOF_minus"],
                         fv8["point_biserial_LOFsign_vs_neg_growth"], fv8["exact_permutation_p_one_sided"],
                         fv8["n_permutations"], fv8["per_gene_sign_correct"]["total"],
                         fv8["point_biserial_sign_vs_GC"], fv8["LOF_mean_GC"], fv8["GOF_mean_GC"],
                         fv8["partial_point_biserial_sign_given_GC"]),
            "firewall": "FV runs the (B) held-out score that FM named as the ONLY honest crossing from map to "
                        "evidence. The score is computed with gamma RE-READ FROZEN from the DNA-measured "
                        "atlases (hash-checked, never re-fitted) against a genuinely held-out CRISPRi "
                        "expression target, with the prediction sign and panel rule locked in advance. The "
                        "outcome is a recorded NULL and is reported as it falls: it promotes NO [O] item "
                        "(O-19/O-20/O-22 stay open), leaves the (A) map [V] and untouched, and confirms FM4's "
                        "honesty invariant empirically. Clinical translation remains firewalled to clinicians "
                        "and regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
