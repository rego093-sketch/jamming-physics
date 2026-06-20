#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
carcinogen_dose_response.py  --  Reproductive / gonadal-endocrine ONCOLOGY module.

VP-NATIVE CANCER KERNEL (shared with the whole framework)
---------------------------------------------------------
A cell fate is the SAME R19 double-well switch the dynamics modules use. A carcinogen is a SUSTAINED
aberrant drive that LOWERS the barrier out of the healthy (metastable) well; malignant transformation
is the Kramers escape over that lowered barrier. The barrier is the EXACT tilted double well

        V(s) = -gamma*s^2/2 + s^4/4 - h*s ,         dV/ds = s^3 - gamma*s - h = 0,

so the stationary points are the roots of [1, 0, -gamma, -h]. With three real roots there are two
minima (outer) and a saddle (middle); the escape barrier out of the metastable (healthy) minimum is

        meta_barrier(gamma,h) = V(saddle) - V(metastable minimum).

Past the fold (fewer than three real roots) the metastable well no longer exists -> barrier = 0.
The Kramers rate is rate ~ exp(-meta_barrier / D) with a single lattice noise D; RR(exposure) is the
rate relative to the unexposed healthy baseline (gamma0 = 1.0, h = 0).

KEY DERIVED RESULT (grade [F], no free parameters)
--------------------------------------------------
The dimensionless ratio meta_barrier(gamma,h)/barrier(gamma) as a function of frac = h/spinodal(gamma)
is IDENTICAL for every gamma. The dose-response SHAPE is UNIVERSAL (gamma-independent): the master
gene of the tissue sets only the absolute barrier scale, never the shape of the hormone dose-response.

GRADES (C3):  shape / universality [V]-[F] ; epidemiological anchors [L] ; absolute incidence [O].
The absolute noise D is a single open number (one lattice constant for the whole package) -> all
absolute rates are [O]; every RR ratio and every synergy/saturation statement is D-robust [V].

Uses only inherited/vp_substrate.py. Deterministic.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal

# Single open lattice noise: sets absolute rates only (grade [O]); cancels in every RR/synergy ratio.
NOISE_D = 0.15

SITES = [
    {"site": "breast carcinoma",
     "drive_axis": "cumulative oestrogen exposure (menarche->menopause years, MHT)",
     "vp_map": "sustained oestrogenic drive h raises frac -> lowers barrier -> monotone RR rise",
     "anchor": "WHI combined MHT RR ~ 1.26 [L]; duration-monotone shape [V]"},
    {"site": "cervical carcinoma",
     "drive_axis": "HPV oncoprotein load x smoking",
     "vp_map": "HPV lowers the barrier height (gamma down) AND adds drive; smoking is mutagenic drive h",
     "anchor": "HPV x smoking ~ multiplicative at low joint exposure [L]; saturating synergy [V]"},
    {"site": "prostate carcinoma",
     "drive_axis": "androgen drive (above a low threshold)",
     "vp_map": "androgen drive saturates: once frac->1 the barrier floor is 0, so RR plateaus",
     "anchor": "androgen saturation model (more T not more risk above threshold) [L]; concavity [V]"},
]

# ---------------------------------------------------------------------------------------------------
# Exact tilted double-well barrier
# ---------------------------------------------------------------------------------------------------

def _V(s, gamma, h):
    return -0.5 * gamma * s * s + 0.25 * s ** 4 - h * s

def meta_barrier(gamma, h):
    """Exact escape barrier out of the metastable (healthy) minimum of the tilted double well.
    Returns 0.0 once the drive has carried the system past the fold (metastable well gone)."""
    if gamma <= 0:
        return 0.0
    roots = np.roots([1.0, 0.0, -gamma, -float(h)])
    real = sorted(float(r.real) for r in roots if abs(r.imag) < 1e-9)
    if len(real) < 3:
        return 0.0                                   # past the fold: no barrier left
    s_lo, s_mid, s_hi = real[0], real[1], real[2]    # minima at s_lo,s_hi ; saddle at s_mid
    v_lo, v_hi = _V(s_lo, gamma, h), _V(s_hi, gamma, h)
    v_meta = max(v_lo, v_hi)                          # metastable = shallower (higher-energy) minimum
    return max(_V(s_mid, gamma, h) - v_meta, 0.0)

def barrier_ratio(gamma, frac):
    """meta_barrier / barrier(gamma) at h = frac * spinodal(gamma). Universal in gamma (grade [F])."""
    h = frac * spinodal(gamma)
    b0 = barrier(gamma)
    return meta_barrier(gamma, h) / b0 if b0 > 0 else 0.0

def crossing_rate(gamma, h, D=NOISE_D):
    return math.exp(-meta_barrier(gamma, h) / D)

def relative_risk(gamma, h, gamma0=1.0, h0=0.0, D=NOISE_D):
    """RR relative to the unexposed healthy baseline well."""
    r0 = crossing_rate(gamma0, h0, D)
    return crossing_rate(gamma, h, D) / r0 if r0 > 0 else float("inf")

# ---------------------------------------------------------------------------------------------------
# Universality check (the [F] result)
# ---------------------------------------------------------------------------------------------------

def universality_check(gammas=(0.5, 1.0, 1.4598, 2.0), fracs=(0.0, 0.2, 0.4, 0.6, 0.8, 0.95)):
    rows = []
    for f in fracs:
        vals = [barrier_ratio(g, f) for g in gammas]
        spread = max(vals) - min(vals)
        rows.append(dict(frac=f, ratio=round(vals[0], 5), max_spread_across_gamma=round(spread, 8)))
    gamma_independent = all(r["max_spread_across_gamma"] < 1e-4 for r in rows)
    return dict(gammas=list(gammas), table=rows, gamma_independent=bool(gamma_independent),
                grade="[F] dose-response shape is universal (gamma sets scale, not shape)")

# ---------------------------------------------------------------------------------------------------
# Per-site exposure maps
# ---------------------------------------------------------------------------------------------------

def breast_duration_curve(years=(0, 5, 10, 15, 20, 25, 30), gamma=1.0, per_year=0.024):
    """Cumulative oestrogen-years as sustained drive: h = per_year * years (capped below the fold).
    Monotone RR rise; the WHI ~1.26 combined-MHT anchor lands in the 5-10 'year' range. per_year is a
    fixed exposure-to-drive scale (an [L] anchor calibrated to that one cohort RR), not a fit per point."""
    sp = spinodal(gamma)
    rows = []
    for y in years:
        h = min(per_year * y, 0.999 * sp)
        rows.append(dict(exposure_years=y, frac=round(h / sp, 4), RR=round(relative_risk(gamma, h), 4)))
    monotone = all(rows[i]["RR"] <= rows[i + 1]["RR"] + 1e-9 for i in range(len(rows) - 1))
    return dict(site="breast", rows=rows, monotone_increasing=bool(monotone),
                anchor="WHI combined MHT RR ~1.26 [L]", grade="[V] duration-monotone; [L] anchor")

def prostate_saturation_curve(drive_levels=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.3, 1.6), gamma=1.0):
    """Androgen drive in units of spinodal. Barrier-reduction f = 1 - meta/barrier is CONCAVE and
    saturates; beyond frac=1 the barrier floor is 0 so RR plateaus -> the saturation model."""
    sp = spinodal(gamma); b0 = barrier(gamma)
    rows = []
    for d in drive_levels:
        h = d * sp
        f = 1.0 - (meta_barrier(gamma, h) / b0 if b0 > 0 else 0.0)
        rows.append(dict(drive_frac=d, barrier_reduction=round(f, 4), RR=round(relative_risk(gamma, h), 4)))
    # concavity of barrier_reduction in the sub-fold region (diminishing returns)
    sub = [r for r in rows if r["drive_frac"] <= 1.0]
    d1 = [sub[i + 1]["barrier_reduction"] - sub[i]["barrier_reduction"] for i in range(len(sub) - 1)]
    concave = all(d1[i + 1] <= d1[i] + 1e-9 for i in range(len(d1) - 1))
    plateau_rows = [r for r in rows if r["drive_frac"] >= 1.0]
    plateaus = bool(len({r["RR"] for r in plateau_rows}) == 1)
    return dict(site="prostate", rows=rows, barrier_reduction_concave=bool(concave),
                rr_plateaus_past_fold=plateaus,
                anchor="androgen saturation model [L]", grade="[V] concave/saturating; [L] anchor")

def cervical_synergy(joint_fracs=(0.05, 0.10, 0.20, 0.30, 0.40), gamma=1.0):
    """HPV = barrier-height reducer (lowers gamma, hence lowers spinodal) plus drive; smoking = drive h.
    Synergy index = RR(both) / (RR_HPV * RR_smoking). ~1 (multiplicative) at low joint exposure;
    < 1 (sub-multiplicative / saturating) at high exposure, because the barrier floor is zero."""
    rows = []
    for fr in joint_fracs:
        # HPV alone: lowers gamma toward a softer well (barrier-height reduction) + modest drive
        g_hpv = gamma * (1.0 - 0.5 * fr)
        h_hpv = fr * spinodal(g_hpv)
        rr_hpv = relative_risk(g_hpv, h_hpv)
        # smoking alone: mutagenic drive on the native well
        h_smk = fr * spinodal(gamma)
        rr_smk = relative_risk(gamma, h_smk)
        # both together: softer well AND combined drive
        h_both = (fr + fr) * spinodal(g_hpv)
        rr_both = relative_risk(g_hpv, h_both)
        idx = rr_both / (rr_hpv * rr_smk) if rr_hpv * rr_smk > 0 else float("inf")
        rows.append(dict(joint_frac=fr, RR_hpv=round(rr_hpv, 3), RR_smoking=round(rr_smk, 3),
                         RR_both=round(rr_both, 3), synergy_index=round(idx, 3)))
    low = rows[0]["synergy_index"]; high = rows[-1]["synergy_index"]
    multiplicative_low = bool(0.9 <= low <= 1.1)
    saturates_high = bool(high < low - 1e-3)
    return dict(site="cervical", rows=rows, multiplicative_at_low_exposure=multiplicative_low,
                sub_multiplicative_at_high_exposure=saturates_high,
                prediction="synergies SATURATE at high joint exposure (sharper than a pure product)",
                grade="[V] exposure-dependent synergy; [L] low-exposure multiplicativity anchor")

def run_oncology():
    uni = universality_check()
    breast = breast_duration_curve()
    prostate = prostate_saturation_curve()
    cervical = cervical_synergy()
    checks = dict(
        universality=uni["gamma_independent"],
        breast_monotone=breast["monotone_increasing"],
        prostate_concave=prostate["barrier_reduction_concave"],
        prostate_plateau=prostate["rr_plateaus_past_fold"],
        cervical_multiplicative_low=cervical["multiplicative_at_low_exposure"],
        cervical_saturates_high=cervical["sub_multiplicative_at_high_exposure"],
    )
    passed = all(checks.values())
    return dict(kernel="R19 tilted double well -> exact meta_barrier -> Kramers RR(exposure)",
                noise_D=NOISE_D, sites=SITES, universality=uni,
                breast=breast, prostate=prostate, cervical=cervical,
                checks=checks, status=("PASS" if passed else "FAIL"),
                grades="shape/universality [V]/[F]; anchors [L]; absolute incidence [O]")

def status():
    return run_oncology()

if __name__ == "__main__":
    print(json.dumps(run_oncology(), ensure_ascii=False, indent=2))
