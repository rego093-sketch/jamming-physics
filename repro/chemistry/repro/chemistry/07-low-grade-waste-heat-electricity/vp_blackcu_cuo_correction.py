# -*- coding: utf-8 -*-
# VP Chemistry & Electromagnetism - repro module (correction, 2026-09-29)
# Paper section: CA.9c black copper as a heat->electricity converter, recomputed with the right material.
# The original module vp_blackcu_absorber_not_generator.py (sha256 0067cbe1...) is kept unchanged for the
# record. It used the Seebeck coefficient of copper METAL (1.8 uV/K). The black layer is CuO, a p-type
# semiconductor, so the thermoelectric inputs must be those of CuO. Deterministic, stdlib + numpy.
"""
Inputs (declared, literature):
  S_CuO   = 204 uV/K   sputtered p-CuO films (PubMed 35521098)
  rho_CuO = 0.01 .. 570 ohm cm  (reported range for CuO films; spray-pyrolysis 5.69e2 ohm cm)
  k_CuO   = 3 W/m/K    (as in BC2)
  S_Cu = 1.8 uV/K, sigma_Cu = 5.96e7 S/m, k_Cu = 400 W/m/K
Questions:
  Q1 how large is the Seebeck voltage across the actual ~100 nm coating at 1 kW/m^2?  (BC2 P6)
  Q2 as a BULK thermoelectric, what figure of merit ZT = S^2 sigma T / k can CuO reach? (vs copper metal)
  Q3 what does a Cu/CuO thermocouple give per kelvin?
"""
import hashlib, numpy as np

S_CuO, k_CuO = 204e-6, 3.0
rho_ohm_cm = np.array([0.01, 1.0, 569.0])
sigma_CuO = 1.0 / (rho_ohm_cm * 1e-2)          # S/m
S_Cu, sigma_Cu, k_Cu = 1.8e-6, 5.96e7, 400.0
T, q, d_coat = 350.0, 1000.0, 100e-9

dT_coat = q * d_coat / k_CuO
V_coat = S_CuO * dT_coat
ZT_CuO = S_CuO ** 2 * sigma_CuO * T / k_CuO
ZT_Cu = S_Cu ** 2 * sigma_Cu * T / k_Cu
S_couple = S_CuO - S_Cu

print("BLACK COPPER, recomputed with CuO (the black layer), not Cu metal")
print(f"  Q1 coating 100 nm at 1 kW/m2: dT = {dT_coat:.2e} K -> V = {V_coat:.2e} V   (negligible: the COATING is too thin)")
for r, z in zip(rho_ohm_cm, ZT_CuO):
    print(f"  Q2 bulk CuO, rho = {r:g} ohm cm: ZT = {z:.2e}")
print(f"     copper metal: ZT = {ZT_Cu:.2e}   -> best CuO is {ZT_CuO.max()/ZT_Cu:.0f}x copper, still ~{1/ZT_CuO.max():.0f}x below ZT = 1")
print(f"  Q3 Cu/CuO thermocouple: {S_couple*1e6:.0f} uV/K  (a real, directional junction: ~20 mV per 100 K)")
print("Verdict: the 100 nm black coating is an absorber, not a converter (Q1) - the original conclusion stands,")
print("  but its reason changes: not 'copper Seebeck is negligible' but 'the coating holds no temperature drop'.")
print("  Bulk CuO is a weak thermoelectric (ZT <= ~0.05); a Cu/CuO junction is a genuine thermocouple.")
print("RESULT sha256 = " + hashlib.sha256(np.concatenate([[dT_coat, V_coat, ZT_Cu, S_couple], ZT_CuO]).tobytes()).hexdigest())
