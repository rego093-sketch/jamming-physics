# -*- coding: utf-8 -*-
"""
heart.decomposition -- the THREE parameter-free results that carry the weight of the heart
accuracy test. Unlike the trajectory illustration (graded [F]), these depend only on
MEASURED moduli and logical/exact relations -- no tuned schedule.

  RESULT A  JAMMING INSUFFICIENCY (the falsification -> discovery)
    Pure cell-jamming (Appendix C: cells in void) gives B_eff <= B_cell. The EMBRYONIC
    cell is soft (~1.25 kPa). The tissue stiffens to ~10-18 kPa. So the rise EXCEEDS what
    the embryonic cell can provide by a factor >> 1: the stiff ECM phase and/or cell
    maturation is NECESSARY. The pure-jamming tower is falsified for the trajectory, and
    that falsification reveals the ECM/maturation as the required driver -- exactly the
    proteomics finding (Majkut 2013: collagen + EC-proteins drive the daily rise).
    Parameter-free inequality on measured moduli. [V].

  RESULT B  GAMMA ORTHOGONALITY (the explanation of the Appendix A heart null)
    gamma is computed from the genomic SEQUENCE -> identical at every developmental stage
    -> TIME-INVARIANT. The trajectory rises ~14x. A constant cannot encode a ramp, so the
    correlation of gamma with the trajectory is zero/undefined. This REPRODUCES Appendix
    A's measured null (heart gamma-vs-timing rho = +0.071, p = 0.882) and EXPLAINS it: the
    stiffening/timing axis is COMPOSITION (ECM), orthogonal to the material gamma.
    Logical certainty + reproduced measured null. [V] + [L].

  RESULT C  BRACKET CONSISTENCY (the accuracy-consistency check, honest about sensitivity)
    The exact two-phase [Reuss, Voigt] bracket built from MEASURED ventricular inputs
    (cell ~35 kPa, LV ECM ~5 kPa, phi_cell ~0.8) CONTAINS the measured adult ventricular
    tissue (~18 kPa). With stiffer ECM inputs the measured tissue sits at/below the Reuss
    bound -- the known 'isolated cells stiffer than bulk tissue' effect. So this is a
    CONSISTENCY check (the composite is compatible with the measured tissue), not a tight
    parameter-free prediction; the sensitivity to cross-study inputs is precisely why the
    named [O] obstacle is a single co-registered preparation. [L] / [O].
"""
import numpy as np

from . import lock, composite


# ----------------------------------------------------------------------------
# RESULT A -- jamming insufficiency (the falsification)
# ----------------------------------------------------------------------------
def jamming_insufficiency():
    """The developmental stiffening exceeds the embryonic cell-jamming ceiling -> the ECM
    phase / cell maturation is necessary. Parameter-free."""
    B_cell_emb, _, _ = lock.cell_immature_kpa()
    ceiling = composite.cell_jamming_ceiling(B_cell_emb)   # = B_cell_emb (Voigt at phi->1)
    E2, _, _ = lock.target_murine_E2_kpa()
    E14, _, _ = lock.target_murine_E14_kpa()
    adult, _, _ = lock.target_adult_rat_kpa()
    rise_factor_to_E14 = E14 / ceiling
    rise_factor_to_adult = adult / ceiling
    insufficient = ceiling < E14            # embryonic cell jammed cannot reach E14 tissue
    return {
        "embryonic_cell_modulus_kpa": B_cell_emb,
        "pure_jamming_ceiling_kpa": round(ceiling, 4),
        "measured_E14_tissue_kpa": E14,
        "measured_adult_tissue_kpa": adult,
        "rise_factor_ceiling_to_E14": round(rise_factor_to_E14, 3),
        "rise_factor_ceiling_to_adult": round(rise_factor_to_adult, 3),
        "pure_cell_jamming_insufficient": bool(insufficient),
        "implication": "the stiff ECM phase and/or cell maturation is NECESSARY to reach "
                       "the measured tissue stiffness from the soft embryonic cell; the "
                       "Appendix-C pure-jamming tower is falsified for the trajectory",
        "matches_proteomics": "Majkut 2013: collagen + excitation-contraction proteins are "
                              "the measured daily drivers of the stiffening",
        "grade": "[V] parameter-free inequality on measured moduli",
    }


# ----------------------------------------------------------------------------
# RESULT B -- gamma orthogonality (the explanation)
# ----------------------------------------------------------------------------
def gamma_orthogonality():
    """gamma is time-invariant; the trajectory is a ramp; a constant cannot predict a ramp
    -> reproduces and explains the Appendix A heart null."""
    inv, ginv, _ = lock.gamma_time_invariant()
    rho, _, _ = lock.appendix_a_null_rho()
    p, _, _ = lock.appendix_a_null_p()
    # demonstrate: correlate a constant gamma series with a rising trajectory
    s = np.linspace(0.0, 1.0, 21)
    traj = 0.1 + 0.3 * (s * 14.0)        # a rising stand-in (shape only; not the target read)
    gamma_const = np.full_like(s, 1.30)  # gamma ~ constant (sequence-fixed)
    # corr of a constant with anything is undefined (zero variance) -> report as ~0
    var_gamma = float(np.var(gamma_const))
    corr = 0.0 if var_gamma < 1e-12 else float(np.corrcoef(gamma_const, traj)[0, 1])
    return {
        "gamma_time_invariant": bool(inv),
        "gamma_variance_over_development": round(var_gamma, 12),
        "corr_gamma_vs_rising_trajectory": corr,
        "appendix_a_heart_null_rho": rho,
        "appendix_a_heart_null_p": p,
        "reproduces_and_explains_null": bool(inv and abs(rho) < 0.2 and p > 0.5),
        "implication": "a SEQUENCE-FIXED (time-invariant) quantity cannot encode a "
                       "time-varying stiffening; the heart's timing axis is COMPOSITION "
                       "(ECM deposition), orthogonal to the material gamma -- which is why "
                       "Appendix A's gamma-vs-timing test was a null, sharpest in the heart",
        "grade": "[V] logical certainty + [L] reproduces the measured Appendix A null",
    }


# ----------------------------------------------------------------------------
# RESULT C -- bracket consistency (honest about sensitivity)
# ----------------------------------------------------------------------------
def bracket_consistency():
    """The exact two-phase bracket from measured ventricular inputs contains the measured
    adult ventricular tissue; report the sensitivity across the measured ECM range."""
    B_cell, _, _ = lock.cell_adult_kpa()
    phi_cell, _, _ = lock.phi_cell_adult()
    adult, _, _ = lock.target_adult_rat_kpa()
    B_lv, _, _ = lock.ecm_lv_kpa()
    B_san, _, _ = lock.ecm_san_kpa()

    lv = composite.contains(B_cell, B_lv, phi_cell, adult)
    san = composite.contains(B_cell, B_san, phi_cell, adult)

    return {
        "measured_adult_tissue_kpa": adult,
        "ventricular_LV_bracket_kpa": lv["bracket_kpa"],
        "contained_with_LV_ECM": lv["contained"],
        "where_in_LV_bracket": lv["where_in_bracket"],
        "SAN_bracket_kpa": san["bracket_kpa"],
        "contained_with_SAN_ECM": san["contained"],
        "note": "containment holds for the anatomically-correct ventricular (LV) ECM "
                "(~5 kPa); with the stiffer SAN ECM (~17 kPa) the measured ventricular "
                "tissue sits below the bracket. The measured tissue sits LOW in the LV "
                "bracket because the isolated single-cell modulus (~35 kPa, AFM) exceeds "
                "the in-situ cell contribution -- a known effect.",
        "consistency_holds": bool(lv["contained"]),
        "grade": "[L] consistency with measured ventricular inputs; tight prediction [O] "
                 "(needs a single co-registered preparation -- same cells, ECM, tissue)",
    }


# ----------------------------------------------------------------------------
# axis identification -- the one-line discovery
# ----------------------------------------------------------------------------
def axis_identification():
    """The synthesis: the heart's developmental stiffening is a COMPOSITION + MATURATION
    flow (ECM collagen + cell stiffening/jamming), NOT a material (gamma) flow and NOT a
    pure cell-packing flow -- and this explains, mechanically, the Appendix A heart null."""
    A = jamming_insufficiency()
    B = gamma_orthogonality()
    C = bracket_consistency()
    return {
        "the_axis": "composition (ECM collagen deposition) + cell maturation/jamming",
        "not_this": ["material gamma (sequence-fixed, time-invariant)",
                     "pure cell-jamming in void (Appendix C; capped at the soft "
                     "embryonic cell modulus)"],
        "falsification": A["pure_cell_jamming_insufficient"],
        "explains_appendix_a_heart_null": B["reproduces_and_explains_null"],
        "consistent_with_measured_tissue": C["consistency_holds"],
        "discovery": "the heart 'failed' in Appendix A (gamma orthogonal to timing) "
                     "because its timing/stiffening lives on the ECM-composition axis the "
                     "renormalization tower exposes -- not on the sequence material axis. "
                     "Falsifying pure-jamming and material-gamma REVEALS the right axis. "
                     "반증 = 발견.",
    }
