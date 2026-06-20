#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
carcinogen_dose_response.py  --  Cardiorespiratory ONCOLOGY module.

VP-NATIVE CANCER MECHANISM (shared R19 kernel, instantiated per organ)
----------------------------------------------------------------------
A cell-fate is the SAME R19 bistable switch used everywhere in this program. The
switch potential is, EXACTLY,

        U(s) = -(gamma/2) s^2 + s^4/4 - h s          (sdot = -dU/ds = gamma*s - s^3 + h)

with two basins (normal / malignant) separated by a saddle. A carcinogen is a
SUSTAINED aberrant bias h_c (>0) that pushes toward the malignant basin and
LOWERS the barrier the normal basin must climb to flip. The malignant-crossing
rate is Kramers/Arrhenius over that barrier,

        rate(h_c) = rate0 * exp( - barrier_eff(gamma, h_c) / scale ),

and the relative risk is  RR(dose) = rate(h_c(dose)) / rate(0).

barrier_eff IS DERIVED, NOT POSTULATED. The three critical points are the real
roots of the depressed cubic s^3 - gamma*s - h = 0 (three reals exactly inside
the bistable window |h| < spinodal = 2(gamma/3)^1.5; trig / casus-irreducibilis
form). barrier_eff = U(saddle) - U(normal-basin). Two exact identities fall out
and are checked at import:
    (i)  barrier_eff(gamma, 0) == barrier(gamma) == gamma^2/4   (substrate value)
    (ii) d[barrier(gamma) - barrier_eff]/dh |_{h=0} == sqrt(gamma)   (origin slope)

FORCED RESULTS (independent of any calibration):
    * RR(0) = 1 exactly                                   grade [F]
    * RR monotone increasing; NO THRESHOLD (any dose>0 -> RR>1, slope sqrt(g)>0) [F]
    * convex / accelerating dose-response shape           grade [V]  (vs Doll&Peto class)

CALIBRATED (absolute magnitude only):
    * the noise energy `scale` and the dose->bias slope `kappa_dose` set the
      ABSOLUTE RR at a given pack-year. They are DECLARED here, not migrated to
      fit targets. Absolute RR magnitude is therefore  grade [O]  with the stated
      obstacle: the switch's effective noise temperature and the molecular
      dose->bias conversion are not fixed by substrate geometry and require an
      external population-hazard calibration -- exactly as absolute organ SIZE is
      [O] while size ORDER is [F].

GRADES (C3): epidemiological anchor [L]; reproduced SHAPE [V]; forced endpoints
[F]; ABSOLUTE incidence/RR magnitude [O] (obstacle stated). No silent claims.
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal

# ----------------------------------------------------------------------------
# DECLARED constants (calibration; NOT fitted to RR points). See module header.
SCALE_OVER_BARRIER = 1.0 / 3.0   # noise energy = barrier/3  -> RR ceiling exp(3)~20x
HEAVY_PKY          = 100.0       # pack-years taken as "lifetime heavy" exposure
HEAVY_FRAC_SPIN    = 0.9         # that exposure drives h_c to 0.9*spinodal (not across)

# Cited epidemiological anchor -------------------------------------------------
ANCHOR = {
    "relation": "lung-carcinoma RR rises with cumulative tobacco dose (pack-years)",
    "source":   "Doll & Peto class cohort epidemiology",
    "shape":    "monotone, convex/accelerating, no practical threshold (LNT at low dose)",
    "heavy_smoker_RR_order": "~10-30x vs never-smoker (order of magnitude)",
    "grade":    "[L]",
}

SITES = [
    {"site": "lung carcinoma",
     "carcinogens": "tobacco smoke condensate; radon progeny; PM2.5/diesel",
     "anchor": "RR vs pack-years (Doll & Peto class) [L]; near-linear no-threshold shape [V]",
     "is_dose_response_target": True},
    {"site": "heart (sarcoma, rare)",
     "carcinogens": "n/a primary; baseline incidence only",
     "anchor": "background crossing rate only; not a dose-response target",
     "is_dose_response_target": False},
]

# ----------------------------------------------------------------------------
def _U(s, g, h):
    """R19 switch potential (sdot = -dU/ds)."""
    return -(g / 2.0) * s * s + s ** 4 / 4.0 - h * s

def critical_points(g, h):
    """Three real roots of s^3 - g s - h = 0, returned low<mid<high.
    Valid (three reals) iff |h| < spinodal(g); returns None otherwise."""
    if g <= 0:
        return None
    sp = spinodal(g)
    if abs(h) >= sp:
        return None
    arg = (3.0 * h / (2.0 * g)) * math.sqrt(3.0 / g)
    arg = max(-1.0, min(1.0, arg))
    base = math.acos(arg) / 3.0
    roots = [2.0 * math.sqrt(g / 3.0) * math.cos(base - 2.0 * math.pi * k / 3.0)
             for k in range(3)]
    return sorted(roots)

def barrier_eff(gamma, h_c):
    """EXACT effective barrier from the normal basin over the saddle, under bias h_c.
    Reduces to barrier(gamma)=gamma^2/4 at h_c=0 (checked at import). For |h_c| past
    the spinodal the normal basin has vanished -> barrier 0 (flip is certain)."""
    r = critical_points(gamma, h_c)
    if r is None:
        return 0.0
    s_low, s_mid, _s_high = r          # normal basin = lower min; saddle = middle root
    return _U(s_mid, gamma, h_c) - _U(s_low, gamma, h_c)

def crossing_rate(gamma, h_c, rate0=1.0, scale=None):
    """Kramers/Arrhenius malignant-crossing rate over the R19 barrier."""
    scale = scale if scale is not None else max(barrier(gamma) * SCALE_OVER_BARRIER, 1e-9)
    return rate0 * math.exp(-barrier_eff(gamma, h_c) / scale)

# ----------------------------------------------------------------------------
def _kappa_dose(gamma):
    """Dose->bias slope (pack-years -> h_c). DECLARED: HEAVY_PKY pack-years map to
    HEAVY_FRAC_SPIN * spinodal. Linear in cumulative dose."""
    return (HEAVY_FRAC_SPIN * spinodal(gamma)) / HEAVY_PKY

def h_of_dose(gamma, pack_years):
    return _kappa_dose(gamma) * max(pack_years, 0.0)

def relative_risk(gamma, pack_years):
    """RR(dose) = rate(h_c(dose)) / rate(0).  RR(0)=1 exactly."""
    scale = barrier(gamma) * SCALE_OVER_BARRIER
    r0 = crossing_rate(gamma, 0.0, scale=scale)
    return crossing_rate(gamma, h_of_dose(gamma, pack_years), scale=scale) / r0

def dose_response_curve(gamma, pack_years_grid):
    return [{"pack_years": float(p),
             "RR": round(relative_risk(gamma, p), 6),
             "ln_RR": round(math.log(relative_risk(gamma, p)), 6)}
            for p in pack_years_grid]

def lnt_check(gamma, tiny=0.5):
    """No-threshold test: a tiny positive dose already raises RR>1, and the
    analytic origin slope of the barrier drop equals sqrt(gamma)>0 (forced)."""
    rr_tiny = relative_risk(gamma, tiny)
    h = 1e-5
    numeric_slope = (barrier(gamma) - barrier_eff(gamma, h)) / h
    return {
        "rr_at_tiny_dose": round(rr_tiny, 6),
        "tiny_dose_pack_years": tiny,
        "no_threshold": bool(rr_tiny > 1.0),
        "barrier_drop_slope_at_origin": round(numeric_slope, 6),
        "slope_equals_sqrt_gamma": bool(abs(numeric_slope - math.sqrt(gamma)) < 1e-3),
        "monotone_no_threshold_grade": "[F]",
    }

def synergy_check(gamma, frac_each=0.3):
    """Two carcinogens add their bias h. Reports RR(h1+h2) vs RR(h1)*RR(h2).
    Honest model OUTPUT (not tuned to a synergy figure): multiplicative in the
    low-dose limit (locally linear barrier drop), turning sub-multiplicative as
    the combined bias nears the spinodal (barrier collapse saturates)."""
    scale = barrier(gamma) * SCALE_OVER_BARRIER
    sp = spinodal(gamma)
    h1 = frac_each * sp
    h2 = frac_each * sp
    def RRh(h):
        return crossing_rate(gamma, h, scale=scale) / crossing_rate(gamma, 0.0, scale=scale)
    combined = RRh(min(h1 + h2, 0.999 * sp))
    product  = RRh(h1) * RRh(h2)
    ratio = combined / product
    regime = ("multiplicative" if abs(ratio - 1.0) < 0.1
              else "super-multiplicative" if ratio > 1.0
              else "sub-multiplicative")
    return {
        "frac_of_spinodal_each": frac_each,
        "RR_combined": round(combined, 4),
        "RR_product_of_singles": round(product, 4),
        "combined_over_product": round(ratio, 4),
        "regime": regime,
        "note": "falsifiable corollary; empirical agent-pair synergy varies",
        "grade": "[V]",
    }

# ----------------------------------------------------------------------------
def results(gamma_lung=None):
    """Full deterministic oncology result block (lung carcinoma dose-response)."""
    if gamma_lung is None:
        # NKX2-1 governs lung; read measured value, never fitted.
        here = os.path.dirname(__file__)
        gpath = os.path.join(here, "..", "..", "inherited", "organ_gamma.json")
        with open(gpath, "r", encoding="utf-8") as f:
            G = json.load(f)
        gamma_lung = float(G.get("NKX2-1", G.get("NKX2_1", 1.5088)))
    grid = [0, 5, 10, 20, 30, 40, 50, 60, 80, 100]
    curve = dose_response_curve(gamma_lung, grid)
    B0 = barrier(gamma_lung)
    return {
        "kernel": "R19 barrier-lowering -> Kramers crossing -> RR(dose)",
        "gamma_lung_NKX2_1": round(gamma_lung, 6),
        "barrier_h0_equals_substrate": bool(abs(barrier_eff(gamma_lung, 0.0) - B0) < 1e-12),
        "spinodal": round(spinodal(gamma_lung), 6),
        "scale_convention": "scale = barrier/3 (declared; sets RR ceiling exp(3)~20x) [O]",
        "dose_to_bias": f"{HEAVY_PKY:.0f} pack-years -> {HEAVY_FRAC_SPIN}*spinodal (declared) [O]",
        "RR_curve": curve,
        "RR_at_0_is_1": bool(abs(curve[0]["RR"] - 1.0) < 1e-9),
        "lnt": lnt_check(gamma_lung),
        "synergy": synergy_check(gamma_lung),
        "anchor": ANCHOR,
        "sites": SITES,
        "grades": {
            "RR(0)=1": "[F]", "monotone_no_threshold": "[F]",
            "convex_shape_vs_DollPeto": "[V]", "epidemiological_anchor": "[L]",
            "absolute_RR_magnitude": "[O]",
        },
        "open_obstacle": ("absolute RR magnitude needs population-hazard calibration: the "
                          "switch noise temperature (scale) and molecular dose->bias slope "
                          "(kappa) are not fixed by substrate geometry"),
    }

def status():
    return results()

# ----------------------------------------------------------------------------
# Import-time exact-identity checks (fail loudly if the derivation drifts).
def _self_check():
    for g in (1.513, 1.5088, 1.0, 2.0):
        assert abs(barrier_eff(g, 0.0) - barrier(g)) < 1e-12, "barrier_eff(0) != barrier(g)"
        h = 1e-6
        slope = (barrier(g) - barrier_eff(g, h)) / h
        assert abs(slope - math.sqrt(g)) < 1e-2, "origin slope != sqrt(gamma)"
_self_check()

if __name__ == "__main__":
    print(json.dumps(results(), ensure_ascii=False, indent=2))
