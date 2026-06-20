#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
organ_optics.py  --  CLASSICAL organ-level instrument physics (documented + linked, NOT an R19 claim).

This is the honest boundary of the package (CHARTER RS1/RS3/RS4): the organ-level OPTICS and ACOUSTICS
are classical physics. We DOCUMENT the standard relations and VERIFY that they reproduce the cited
clinical/physiological anchors deterministically -- we do NOT re-derive them from the R19 substrate.
The R19 substrate is used only for the cellular transduction switch (transduction.py).

Modules:
  (A) reduced-eye dioptrics + the axial-length<->refraction conversion (geometric optics, derived);
  (B) accommodation amplitude vs age (Hofstetter), giving presbyopia;
  (C) cochlear place-frequency map (Greenwood 1990) -- the tonotopy [L];
  (D) semicircular-canal torsion-pendulum transfer -> the canal computes angular VELOCITY over the band.

Cited anchors (measured inputs, locked [L]):
  reduced-eye power ~60 D (cornea ~40 + lens ~20); n' = 1.336; emmetropic axial length ~22.3 mm
    (Dioptre, Wikipedia; UIowa schematic eye; Lin 2017 PMC5514268).
  clinical axial-length->myopia ~2.7-3.0 D/mm (UIowa; Lin 2017).
  Hofstetter max amplitude (D) = 25 - 0.40*age ; presbyopia ~1 D by age ~60 (Dioptre).
  Greenwood human: f = 165.4 (10^{2.1 x} - 0.88), x in [0 apex,1 base] -> 20 Hz .. ~20 kHz (Greenwood 1990 JASA 87:2592).
  semicircular canal: overdamped torsion pendulum; afferent dominant time constant ~4-7 s, central
    velocity-storage extends to ~15-25 s; VOR gain ~1 in healthy young humans
    (Steinhausen 1933; Van Egmond/Groen/Jongkees 1949; Jones & Milsum 1965; Reichenbach & Hudspeth 2014).

Grades: classical relations (cited, NOT R19) ; the package VERIFIES the arithmetic reproduces the anchor [V-arith].
"""
import numpy as np

# ---- locked physical anchors (measured inputs) --------------------------------------------------
N_VITREOUS = 1.336          # reduced-eye image-space index [L]
EYE_POWER_D = 60.0          # relaxed total power, dioptres [L]
GREENWOOD = dict(A=165.4, a=2.1, k=0.88)   # human coefficients [L] (Greenwood 1990)
CANAL_T_LONG_S = 5.0        # peripheral afferent dominant time constant, s [L] (~4-7 s)
CANAL_T_SHORT_S = 0.003     # cupula (fast) time constant, s [L] (~ms)
VOR_GAIN = 1.0             # healthy young human [L]


# ====================== (A) reduced-eye dioptrics ==================================================
def emmetropic_axial_length_mm():
    """Emmetropia requires image-space dioptric length K' = n'/k' to equal the eye power F_e.
    => k' = n'/F_e. Pure geometric optics; matches the ~22.3-22.6 mm schematic eye."""
    k_m = N_VITREOUS / EYE_POWER_D
    return k_m * 1000.0


def diopters_per_mm_axial():
    """d(refraction)/d(axial length). For the reduced eye, vergence error per metre of axial change is
    dF = -d(n'/k') = (n'/k'^2) dk'. Evaluated at the emmetropic k'. DERIVED from geometry (no fit)."""
    k_m = N_VITREOUS / EYE_POWER_D
    d_per_m = N_VITREOUS / (k_m ** 2)     # D per metre
    return d_per_m / 1000.0               # D per mm


def refractive_error_from_axial(delta_axial_mm):
    """Myopic shift (D) for an axial elongation of delta_axial_mm beyond emmetropia (sign: + = myopia)."""
    return diopters_per_mm_axial() * float(delta_axial_mm)


# ====================== (B) accommodation vs age (Hofstetter) ======================================
def accommodation_amplitude_D(age_years):
    """Hofstetter maximum amplitude of accommodation (D) = 25 - 0.40*age (floored at 0)."""
    return max(0.0, 25.0 - 0.40 * float(age_years))


# ====================== (C) cochlear place-frequency map (Greenwood) ===============================
def greenwood_freq_hz(x):
    """Characteristic frequency at fractional cochlear position x (0 apex .. 1 base)."""
    A, a, k = GREENWOOD["A"], GREENWOOD["a"], GREENWOOD["k"]
    return A * (10.0 ** (a * float(x)) - k)


# ====================== (D) semicircular-canal torsion pendulum ====================================
def canal_velocity_band_response(freqs_hz, T1=CANAL_T_LONG_S, T2=CANAL_T_SHORT_S):
    """Overdamped torsion-pendulum transfer from head angular VELOCITY to cupula deflection.
    Magnitude |H(w)| = (w T1) / sqrt((1+(w T1)^2)(1+(w T2)^2)).  Between the corner frequencies
    1/T1 and 1/T2 the gain is ~flat and IN PHASE with velocity: the canal computes angular velocity."""
    w = 2.0 * np.pi * np.asarray(freqs_hz, float)
    mag = (w * T1) / np.sqrt((1.0 + (w * T1) ** 2) * (1.0 + (w * T2) ** 2))
    return mag


def verify_optics_acoustics():
    """Verify each classical relation reproduces its cited anchor (deterministic arithmetic check)."""
    axial = emmetropic_axial_length_mm()
    dpm = diopters_per_mm_axial()
    # Greenwood endpoints -> human audible range
    f_apex = greenwood_freq_hz(0.0)
    f_base = greenwood_freq_hz(1.0)
    # canal: flat velocity band check over 0.1-6 Hz (std deviation of magnitude small vs mean)
    fb = np.array([0.1, 0.3, 1.0, 3.0, 6.0])
    mag = canal_velocity_band_response(fb)
    flat_ratio = float(np.std(mag) / np.mean(mag))
    checks = dict(
        reduced_eye_axial_length_mm=round(axial, 3),         # ~22.27 mm (cited ~22.3-22.6) [L/V-arith]
        axial_length_match=bool(21.5 <= axial <= 23.5),
        diopters_per_mm_axial=round(dpm, 3),                 # ~2.69 (cited ~2.7-3.0) [V-arith]
        diopters_per_mm_match=bool(2.4 <= dpm <= 3.1),
        accommodation_D_age15=round(accommodation_amplitude_D(15), 2),   # 19.0 (cited 11-16 min..max)
        accommodation_D_age60=round(accommodation_amplitude_D(60), 2),   # 1.0 (presbyopia ~1 D) [V-arith]
        presbyopia_match=bool(accommodation_amplitude_D(60) <= 2.0),
        greenwood_apex_hz=round(f_apex, 1),                  # ~19.8 ~ 20 Hz
        greenwood_base_hz=round(f_base, 0),                  # ~20672 ~ 20 kHz
        greenwood_range_match=bool(15 <= f_apex <= 25 and 18000 <= f_base <= 23000),
        canal_velocity_band_flatness_ratio=round(flat_ratio, 3),         # small -> ~flat velocity band
        canal_velocity_band_ok=bool(flat_ratio < 0.5),
        vor_gain_cited=VOR_GAIN,
        grade="classical optics/acoustics (cited, NOT R19); arithmetic reproduces the anchor [V-arith]",
    )
    checks["pass_"] = bool(checks["axial_length_match"] and checks["diopters_per_mm_match"]
                           and checks["presbyopia_match"] and checks["greenwood_range_match"]
                           and checks["canal_velocity_band_ok"])
    return checks


if __name__ == "__main__":
    import json
    print(json.dumps(verify_optics_acoustics(), ensure_ascii=False, indent=2))
