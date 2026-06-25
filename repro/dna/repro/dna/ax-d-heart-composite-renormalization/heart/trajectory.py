# -*- coding: utf-8 -*-
"""
heart.trajectory -- the developmental stiffening trajectory: the MEASURED target and the
PREDICTED composite trajectory.

THE MEASURED TARGET (read from the DB; the engine NEVER reads it inside a prediction):
  * chick: E(t) ~ 0.1 + 0.3*t kPa, t in days -- approximately LINEAR (Majkut 2013)
  * murine: E2 < 1 kPa -> E14 ~ 10 kPa (~10x), = neonate/adult (Majkut 2013)
  * adult: ~18 kPa (rat, Berry 2006); 10-50 kPa (human)

THE PREDICTED COMPOSITE TRAJECTORY (the engine's forward model):
  the proteomics (Majkut 2013) identifies the daily drivers of stiffening as COLLAGEN plus
  excitation-contraction proteins -- i.e. ECM DEPOSITION and CELL MATURATION/JAMMING. So
  the forward model raises, monotonically over a developmental parameter s in [0,1]:
    - the ECM (collagen) volume fraction phi_ecm(s): sparse early -> ~0.20 adult [F] shape,
      MEASURED to rise (collagen rises faster than heart weight; neonatal-high collagen)
    - the cell jamming fraction J(s): cells loosely packed early (soft cardiac jelly
      dominates, J->0) -> jammed adult (J->1), using the Appendix C [L]-grounded onset
  at FIXED measured phase moduli (B_cell, B_ecm). The composite modulus is the
  jamming-weighted Voigt B_eff(s) = phi_cell*J(s)*B_cell + phi_ecm(s)*B_ecm, which is
  always <= the exact Voigt bound (J <= 1) and >= 0, so it never leaves the exact bracket.

IMPORTANT (the discipline): the PREDICTION uses only measured PHASE moduli and monotone,
measured-grounded composition schedules. It does NOT read the target trajectory. The
schedules' SHAPE is a modelling choice [F]; what is NOT tuned is the phase moduli (measured
[L]) or the endpoints. The trajectory MATCH is therefore graded [F]-illustration, while the
parameter-free results (bracket containment, the cell-jamming-ceiling inequality, the gamma
time-invariance) carry the [V]/[L] weight (heart.decomposition).
"""
import numpy as np

from . import lock, composite


# ----------------------------------------------------------------------------
# the MEASURED target (read from DB; compared, never used to fit)
# ----------------------------------------------------------------------------
def measured_chick(days):
    """Measured chick trajectory E(t) = intercept + slope*t kPa (Majkut 2013)."""
    b, _, _ = lock.target_chick_intercept_kpa()
    m, _, _ = lock.target_chick_slope_kpa_per_day()
    days = np.asarray(days, dtype=np.float64)
    return b + m * days


def measured_endpoints():
    """The measured embryonic and adult endpoints (murine/rat), for containment checks."""
    E2, _, _ = lock.target_murine_E2_kpa()
    E14, _, _ = lock.target_murine_E14_kpa()
    adult, _, _ = lock.target_adult_rat_kpa()
    return {"embryonic_E2_kpa": E2, "E14_kpa": E14, "adult_kpa": adult}


# ----------------------------------------------------------------------------
# the monotone, measured-grounded composition schedules (forward-model inputs)
# ----------------------------------------------------------------------------
def _jamming_fraction(phi_pack):
    """Appendix C [L]-grounded rigidity fraction J(phi) = sqrt((phi-phi_c)/(1-phi_c)) for
    phi>phi_c, else 0. Cells bear load only once jammed."""
    pc, _, _ = lock.phi_c()
    psi, _, _ = lock.rigidity_onset_exponent()
    phi = np.asarray(phi_pack, dtype=np.float64)
    base = np.maximum((phi - pc) / (1.0 - pc), 0.0)
    return np.where(phi > pc, base ** psi, 0.0)


def ecm_fraction_schedule(s):
    """phi_ecm(s): ECM/collagen volume fraction rising from the embryonic-sparse start to
    the adult value. Monotone; SHAPE [F]; the RISE is measured (collagen rises faster than
    heart weight; neonatal-high collagen)."""
    start, _, _ = lock.phi_ecm_embryonic_start()
    phi_cell_adult, _, _ = lock.phi_cell_adult()
    adult = 1.0 - phi_cell_adult
    s = np.asarray(s, dtype=np.float64)
    return start + (adult - start) * s


def cell_packing_schedule(s):
    """phi_cell_pack(s): the cell PACKING fraction rising from loosely-packed (below the
    jamming onset -> soft cardiac jelly dominates) to jammed. Monotone; SHAPE [F]. Spans
    below->above phi_c so J ramps 0->1."""
    pc, _, _ = lock.phi_c()
    s = np.asarray(s, dtype=np.float64)
    lo = pc - 0.12          # below jamming early (fluid)
    hi = 0.86               # jammed late
    return lo + (hi - lo) * s


# ----------------------------------------------------------------------------
# the predicted composite trajectory
# ----------------------------------------------------------------------------
def predicted_composite(s, B_cell_kpa=None, B_ecm_kpa=None):
    """B_eff(s) = phi_cell*J(s)*B_cell + phi_ecm(s)*B_ecm (jamming-weighted Voigt), at
    FIXED measured phase moduli. Monotone rising; always within the exact bracket."""
    if B_cell_kpa is None:
        # use a representative adult cell modulus for the load-bearing (mature) phase;
        # the early softness comes from J->0, not from a soft cell value
        B_cell_kpa, _, _ = lock.cell_adult_kpa()
    if B_ecm_kpa is None:
        B_ecm_kpa, _, _ = lock.ecm_central_kpa()
    s = np.asarray(s, dtype=np.float64)
    phi_ecm = ecm_fraction_schedule(s)
    phi_cell = 1.0 - phi_ecm
    J = _jamming_fraction(cell_packing_schedule(s))
    B_eff = phi_cell * J * B_cell_kpa + phi_ecm * B_ecm_kpa
    return B_eff


def predicted_trajectory_table(n=11):
    """The predicted composite trajectory across development, with the cell-jamming-only
    ceiling and the gamma-constant control alongside, for inspection."""
    s = np.linspace(0.0, 1.0, n)
    B_cell, _, _ = lock.cell_adult_kpa()
    B_ecm, _, _ = lock.ecm_central_kpa()
    B_eff = predicted_composite(s, B_cell, B_ecm)
    phi_ecm = ecm_fraction_schedule(s)
    J = _jamming_fraction(cell_packing_schedule(s))
    rows = []
    for i in range(n):
        rows.append({
            "s_dev": round(float(s[i]), 4),
            "phi_ecm": round(float(phi_ecm[i]), 4),
            "cell_jamming_J": round(float(J[i]), 4),
            "B_composite_kpa": round(float(B_eff[i]), 4),
            "c_passive_m_per_s": round(composite.wave_speed_m_per_s(float(B_eff[i])), 4),
        })
    return rows


def trajectory_spans_measured():
    """Does the predicted composite trajectory SPAN the measured embryonic->adult range?
    (start near the soft embryonic value, end within the adult range). This is the
    [F]-illustration that the composition flow reproduces the trajectory shape."""
    s = np.linspace(0.0, 1.0, 101)
    B_eff = predicted_composite(s)
    ep = measured_endpoints()
    adult_lo, adult_hi = lock.target_adult_human_range_kpa()[0]
    start_ok = float(B_eff[0]) <= ep["embryonic_E2_kpa"] + 1.0     # starts soft (<~1.5 kPa)
    end_in_adult = adult_lo <= float(B_eff[-1]) <= adult_hi        # ends in adult band
    monotone = bool(np.all(np.diff(B_eff) >= -1e-9))
    return {
        "predicted_start_kpa": round(float(B_eff[0]), 4),
        "predicted_end_kpa": round(float(B_eff[-1]), 4),
        "measured_embryonic_kpa": ep["embryonic_E2_kpa"],
        "measured_adult_band_kpa": [adult_lo, adult_hi],
        "starts_soft": bool(start_ok),
        "ends_in_adult_band": bool(end_in_adult),
        "monotone_rising": monotone,
        "spans_measured_range": bool(start_ok and end_in_adult and monotone),
        "grade": "[F] illustration: monotone measured-grounded composition schedules at "
                 "fixed MEASURED phase moduli reproduce the embryonic->adult span; the "
                 "tight parameter-free results are in heart.decomposition",
    }
