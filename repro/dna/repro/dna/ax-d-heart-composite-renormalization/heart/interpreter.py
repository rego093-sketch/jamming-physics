# -*- coding: utf-8 -*-
"""
heart.interpreter -- the heart composite-renormalization ACCURACY reading (해석기).

This is the 'challenge the heart' reading: the case that 'failed' in Appendix A (gamma
orthogonal to developmental timing, sharpest in the heart) is re-attacked with the
Appendix C renormalization tower upgraded to (a) a real two-phase (cell + ECM) composite
and (b) MEASURED cardiac phase moduli, so an ACCURACY test becomes possible.

The reading returns:
  * the measured phase moduli and tissue trajectory (locked, cited)
  * the exact two-phase bracket and whether it CONTAINS the measured tissue
  * the predicted composition-flow trajectory and whether it SPANS the measured range
  * the three parameter-free results: jamming insufficiency (falsification), gamma
    orthogonality (explanation of the null), bracket consistency
  * the axis identification (the discovery) and honest grades / completion

The through-line is the VP master c^2 = B/rho applied to the composite myocardium; the
discovery is that the heart's developmental stiffening is a COMPOSITION + MATURATION flow,
not the sequence material gamma -- which is exactly why gamma was orthogonal to heart
timing.

Deterministic; 2x SHA-256; constants from heart.lock; nothing fitted.
"""
import json
import hashlib

from . import lock, composite, trajectory, decomposition, grading


def interpret_heart():
    """The full heart accuracy reading."""
    # measured endpoints + adult bracket containment
    B_cell_adult, _, _ = lock.cell_adult_kpa()
    B_ecm_lv, _, _ = lock.ecm_lv_kpa()
    phi_cell, _, _ = lock.phi_cell_adult()
    adult, _, _ = lock.target_adult_rat_kpa()

    reading = {
        "_what": "heart composite-renormalization ACCURACY reading: the Appendix A heart "
                 "null re-attacked with the Appendix C tower upgraded to a real two-phase "
                 "(cell + ECM) composite and MEASURED cardiac phase moduli. The stiffening "
                 "is shown to be a COMPOSITION + MATURATION flow (ECM collagen), not the "
                 "sequence material gamma -- explaining the null.",
        "vp_master_relation": "c^2 = B/rho applied to the composite myocardium "
                              "(passive elastic wave; distinct from the active contraction "
                              "wave, which Majkut 2013 finds linear in E_t)",

        # 1) measured inputs (locked, cited)
        "measured_phase_moduli_kpa": {
            "cell_immature": lock.cell_immature_kpa()[0],
            "cell_adult": lock.cell_adult_kpa()[0],
            "ecm_LV": lock.ecm_lv_kpa()[0],
            "ecm_SAN": lock.ecm_san_kpa()[0],
        },
        "measured_tissue_trajectory_kpa": {
            "chick": "E(t) = %.1f + %.1f*t (t in days)" % (
                lock.target_chick_intercept_kpa()[0],
                lock.target_chick_slope_kpa_per_day()[0]),
            "murine_E2": lock.target_murine_E2_kpa()[0],
            "murine_E14": lock.target_murine_E14_kpa()[0],
            "adult_rat": lock.target_adult_rat_kpa()[0],
            "adult_human_range": lock.target_adult_human_range_kpa()[0],
        },

        # 2) the exact two-phase bracket + containment
        "two_phase_bracket": composite.bracket(B_cell_adult, B_ecm_lv, phi_cell),
        "bracket_contains_measured_adult": composite.contains(
            B_cell_adult, B_ecm_lv, phi_cell, adult),

        # 3) the predicted composition-flow trajectory
        "predicted_trajectory": trajectory.predicted_trajectory_table(11),
        "trajectory_spans_measured": trajectory.trajectory_spans_measured(),

        # 4) the three parameter-free results
        "RESULT_A_jamming_insufficiency": decomposition.jamming_insufficiency(),
        "RESULT_B_gamma_orthogonality": decomposition.gamma_orthogonality(),
        "RESULT_C_bracket_consistency": decomposition.bracket_consistency(),

        # 5) the discovery
        "axis_identification": decomposition.axis_identification(),

        # 6) honest grades
        "grade_ledger": grading.LEDGER,
        "completion": grading.completion_status(),
    }
    return reading


def reading_hash(reading):
    """Stable 16-char SHA-256 over the reading (determinism witness)."""
    blob = json.dumps(reading, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]
