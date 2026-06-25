# -*- coding: utf-8 -*-
"""
heart.lock -- the LOCKED constant surface for the heart composite-renormalization
accuracy test.

DISCIPLINE (inherited verbatim from Appendix C / the cell- and tissue-level engines):
  * EVERY physical input is read from this package's locked param_db.json. There is NOT
    ONE inline magic number. Any constant that is a modelling choice is named, graded,
    and sourced.
  * The engine reads ONLY this DB for PHYSICAL inputs (cell modulus, ECM modulus, volume
    fractions). It NEVER reads the validation TARGET (the measured tissue stiffness
    trajectory) when computing a PREDICTION -- the target is fetched separately and only
    compared in the explicit accuracy checks. That separation is the non-fit invariant.
  * Grades carried verbatim from the DB: [L] measured/cited, [V] exact/logical,
    [F] modelling choice, [O] open (the specific co-registered measurement is absent).

WHAT THIS PACKAGE ADDS BEYOND APPENDIX C:
  Appendix C climbed a tower of ONE phase (cells) packed in VOID, and its absolute moduli
  were [O] placeholders. Here the moduli are MEASURED cardiac values, and the myocardium
  is treated as its real TWO-PHASE composite: a CELL phase and a stiff ECM/COLLAGEN phase.
  This makes an ACCURACY test possible -- does the exact elastic-mixture bracket, built
  from measured phase moduli, CONTAIN the measured myocardium, and does it explain the
  developmental stiffening that pure cell-jamming and the sequence material gamma cannot?
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_DB_PATH = os.path.join(_HERE, "..", "param_db.json")


def _load_db():
    if not os.path.exists(_DB_PATH):
        raise FileNotFoundError(
            "param_db.json not found. The heart engine refuses to invent cardiac "
            "moduli; place the locked DB (measured, cited) next to it."
        )
    with open(_DB_PATH, encoding="utf-8") as fh:
        return json.load(fh), os.path.relpath(_DB_PATH, _HERE)


DB, DB_PATH = _load_db()


def _entry(*path):
    node = DB
    for k in path:
        node = node[k]
    return node["value"], node.get("grade", "[?]"), node.get("provenance", "")


# ----------------------------------------------------------------------------
# CELL phase (measured single-cardiomyocyte modulus)
# ----------------------------------------------------------------------------
def cell_immature_kpa():
    """Immature/embryonic single cardiomyocyte modulus (hiPSC-CM ~1.25 kPa). [L]."""
    return _entry("cell_phase", "single_cardiomyocyte_immature_kpa")


def cell_adult_kpa():
    """Adult single cardiomyocyte modulus (rat AFM ~35 kPa). [L]."""
    return _entry("cell_phase", "single_cardiomyocyte_adult_kpa")


def cell_density_kg_per_m3():
    """Myocardial mass density ~1060 kg/m^3. [L] (anchor for c^2=B/rho only)."""
    return _entry("cell_phase", "cardiomyocyte_density_kg_per_m3")


# ----------------------------------------------------------------------------
# ECM / COLLAGEN phase (measured decellularized-myocardium modulus)
# ----------------------------------------------------------------------------
def ecm_lv_kpa():
    """Decellularized LV myocardial ECM modulus ~5 kPa. [L]."""
    return _entry("ecm_phase", "decellularized_LV_ECM_kpa")


def ecm_san_kpa():
    """Decellularized SAN myocardial ECM modulus ~17 kPa. [L]."""
    return _entry("ecm_phase", "decellularized_SAN_ECM_kpa")


def ecm_central_kpa():
    """Working central ECM-phase modulus ~8 kPa (within measured 5-17 kPa). [F]."""
    return _entry("ecm_phase", "ecm_phase_central_kpa")


def ecm_range_kpa():
    """Measured ECM-phase modulus range [5,17] kPa (decellularized myocardium)."""
    lo, glo, _ = ecm_lv_kpa()
    hi, ghi, _ = ecm_san_kpa()
    return (lo, hi)


# ----------------------------------------------------------------------------
# COMPOSITION (volume fractions, collagen trajectory shape)
# ----------------------------------------------------------------------------
def phi_cell_adult():
    """Cardiomyocyte volume fraction in adult myocardium ~0.80. [F]."""
    return _entry("composition", "cardiomyocyte_volume_fraction_adult")


def phi_ecm_embryonic_start():
    """ECM volume fraction early (sparse collagen) ~0.02. [F]."""
    return _entry("composition", "collagen_fraction_embryonic_start")


def collagen_rises_faster_than_weight():
    """Collagen fraction rises over development (measured). [L]."""
    return _entry("composition", "collagen_rises_faster_than_heart_weight")


# ----------------------------------------------------------------------------
# TARGET trajectory (MEASURED tissue stiffness) -- fetched separately, never read
# inside a prediction (non-fit invariant)
# ----------------------------------------------------------------------------
def target_chick_intercept_kpa():
    return _entry("tissue_stiffness_trajectory", "chick_embryo_intercept_kpa")


def target_chick_slope_kpa_per_day():
    return _entry("tissue_stiffness_trajectory", "chick_embryo_slope_kpa_per_day")


def target_murine_E2_kpa():
    return _entry("tissue_stiffness_trajectory", "murine_E2_kpa")


def target_murine_E14_kpa():
    return _entry("tissue_stiffness_trajectory", "murine_E14_kpa")


def target_adult_rat_kpa():
    return _entry("tissue_stiffness_trajectory", "adult_rat_myocardium_central_kpa")


def target_adult_human_range_kpa():
    return _entry("tissue_stiffness_trajectory", "adult_human_myocardium_range_kpa")


# ----------------------------------------------------------------------------
# GAMMA control (Appendix A null reproduced)
# ----------------------------------------------------------------------------
def gamma_time_invariant():
    return _entry("gamma_axis_control", "gamma_is_time_invariant_over_development")


def appendix_a_null_rho():
    return _entry("gamma_axis_control", "appendix_a_heart_timing_null_rho")


def appendix_a_null_p():
    return _entry("gamma_axis_control", "appendix_a_heart_timing_null_p")


# ----------------------------------------------------------------------------
# JAMMING (inherited from Appendix C)
# ----------------------------------------------------------------------------
def phi_c():
    return _entry("jamming_inherited", "phi_c_3d")


def rigidity_onset_exponent():
    return _entry("jamming_inherited", "rigidity_onset_exponent")


def lock_manifest():
    """A flat, auditable dump of every measured cardiac input this test stands on, with
    grade and provenance, so a hostile reviewer can confirm no modulus was tuned to the
    target. Printed in the gate."""
    def pack(getter):
        v, g, p = getter()
        return {"value": v, "grade": g, "provenance": p}
    return {
        "db_path": DB_PATH,
        "cell_phase": {
            "immature_kpa": pack(cell_immature_kpa),
            "adult_kpa": pack(cell_adult_kpa),
            "density_kg_per_m3": pack(cell_density_kg_per_m3),
        },
        "ecm_phase": {
            "decellularized_LV_kpa": pack(ecm_lv_kpa),
            "decellularized_SAN_kpa": pack(ecm_san_kpa),
            "central_kpa": pack(ecm_central_kpa),
        },
        "composition": {
            "phi_cell_adult": pack(phi_cell_adult),
            "phi_ecm_embryonic_start": pack(phi_ecm_embryonic_start),
            "collagen_rises_faster_than_weight": pack(collagen_rises_faster_than_weight),
        },
        "target_trajectory_MEASURED": {
            "chick_intercept_kpa": pack(target_chick_intercept_kpa),
            "chick_slope_kpa_per_day": pack(target_chick_slope_kpa_per_day),
            "murine_E2_kpa": pack(target_murine_E2_kpa),
            "murine_E14_kpa": pack(target_murine_E14_kpa),
            "adult_rat_kpa": pack(target_adult_rat_kpa),
        },
        "gamma_control": {
            "gamma_time_invariant": pack(gamma_time_invariant),
            "appendix_a_null_rho": pack(appendix_a_null_rho),
            "appendix_a_null_p": pack(appendix_a_null_p),
        },
        "jamming_inherited": {
            "phi_c": pack(phi_c),
            "rigidity_onset_exponent": pack(rigidity_onset_exponent),
        },
        "inline_magic_numbers": 0,
    }
