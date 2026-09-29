"""LE1 (implements PREREG.json). Deterministic, numpy only."""
import json, os, hashlib, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
h, c, kB, e, me = 6.62607015e-34, 2.99792458e8, 1.380649e-23, 1.602176634e-19, 9.1093837015e-31
lamC = h / (me * c); D = 2 * lamC; WIEN = 2.897771955e-3

def chi_deg(lam):
    m = math.ceil(lam / D); return math.degrees(math.asin(min(1.0, lam / (m * D)))), m

E_thr_keV = h * c / D / e / 1e3
P1 = abs(E_thr_keV / (me * c ** 2 / e / 1e3 / 2) - 1) < 1e-12
T45 = WIEN / (D * math.sin(math.radians(45)))
def log10_frac_below(T, lam_cut):
    # photon-number fraction with lambda < lam_cut  (x = hc/(lam kT) > x0), asymptotic x0^2 e^-x0 / (2 zeta(3))
    x0 = h * c / (lam_cut * kB * T)
    return (2 * math.log(x0) - x0 / math.log(10) * math.log(10) - math.log(2 * 1.2020569)) / math.log(10) if x0 > 50 else math.log10(max(1e-300, 1.0))
fr = {T: (2 * math.log10(h * c / (D * kB * T)) - (h * c / (D * kB * T)) / math.log(10) - math.log10(2 * 1.2020569)) for T in (3000, 1e6, 1e8)}
P2 = T45 > 8e8 * 0.95 and fr[3000] < -100
V45 = h * c / (e * D * math.sin(math.radians(45)))
rows_V = {f"{V/1e3:g} kV": chi_deg(h * c / (e * V)) for V in (1e5, 2.555e5, 3.6e5, 1e6, 1e7)}
chi511, m511 = chi_deg(h * c / (511e3 * e))
P3 = 0.3e6 < V45 < 0.4e6
P4 = m511 == 1 and abs(chi511 - 30) < 0.1
rows_T = {f"{T:g} K": chi_deg(WIEN / T) for T in (300, 1373, 3000, 5778, 1e6, 1e8, 8.45e8, 3.4e9)}
res = {"D_pm": D * 1e12, "P1_threshold_keV": E_thr_keV, "P1": P1,
       "P2_T_for_45deg_K": T45, "P2_log10_fraction_lambda_below_D": fr, "P2": P2,
       "P3_V_for_45deg": V45, "P3_rows": rows_V, "P3": P3,
       "P4_chi_511keV": chi511, "P4": P4, "chi_vs_T_wien_peak": rows_T,
       "P5": "argument + observation: isotropic thermal emission carries zero net momentum; bremsstrahlung from a straight electron beam is forward-beamed (measured); no computation"}
txt = json.dumps(res, indent=2, default=str)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2, default=str)
print(f"D = {D*1e12:.4f} pm; P1 near-longitudinal threshold = {E_thr_keV:.2f} keV = m_e c^2/2 -> {P1}")
print(f"P2 heat: Wien peak reaches chi=45 deg at T = {T45:.3e} K; log10 fraction(lambda<D): " + ", ".join(f"{k:g}K {v:.3g}" for k, v in fr.items()) + f" -> {P2}")
for k, (x, m) in rows_T.items(): print(f"   thermal peak {k:>10s}: chi = {x:8.4f} deg (m={m})")
print(f"P3 straight electron: chi=45 deg at V = {V45/1e3:.0f} kV -> {P3}")
for k, (x, m) in rows_V.items(): print(f"   {k:>9s}: lambda_min chi = {x:7.3f} deg (m={m})")
print(f"P4 annihilation 511 keV: chi = {chi511:.3f} deg (m={m511}) -> {P4}")
