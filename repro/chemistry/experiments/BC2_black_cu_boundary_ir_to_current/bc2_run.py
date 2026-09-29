"""BC2: black-copper boundary in the ESS — infrared -> directed electron motion? (implements PREREG.json)
Deterministic, numpy only. Detailed-balance diode: the boundary at T_b re-emits photons and photoemits
backwards with the same yield, so an isothermal boundary gives exactly zero net power (second law, [F]).
"""
import json, os, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
q, kB_eV, h, c, SIG = 1.602176634e-19, 8.617333262e-5, 6.62607015e-34, 2.99792458e8, 5.670374419e-8
A_STAR, ABS, EF, N_CU, VF = 1.2e6, 0.96, 7.0, 8.5e28, 1.57e6
E = np.linspace(0.005, 3.0, 60000)                                    # eV
dE = E[1] - E[0]

def photon_flux(T):                                                  # photons / (m^2 s eV), hemispherical
    x = E / (kB_eV * T)
    return 2 * np.pi / (h ** 3 * c ** 2) * (E * q) ** 2 / np.expm1(np.clip(x, 1e-12, 700)) * q

def jph(T, phi, mode):
    y = np.where(E > phi, 1.0 if mode == "ideal" else (E - phi) ** 2 / (8 * EF * E), 0.0)
    return q * ABS * np.sum(photon_flux(T) * y) * dE                  # A/m^2

def best_power(Ts, Tb, phi, mode):
    Js, Jb = jph(Ts, phi, mode), jph(Tb, phi, mode)
    J0 = A_STAR * Tb ** 2 * np.exp(-phi / (kB_eV * Tb))
    Vt = kB_eV * Tb
    V = np.concatenate([[0.0], np.logspace(-9, 0.5, 4000)])
    J = Js - Jb * np.exp(V / Vt) - J0 * np.expm1(V / Vt)
    P = J * V
    i = int(np.argmax(P))
    return {"P_W_m2": float(max(P[i], 0.0)), "V": float(V[i]), "J_A_m2": float(J[i]), "Jsc_A_m2": float(Js - Jb), "J0_A_m2": float(J0)}

T_S, T_COLD = [340.0, 423.0, 573.0, 773.0], 293.0
PHI = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
res = {}
for Ts in T_S:
    absorbed = ABS * SIG * Ts ** 4
    r = {"absorbed_W_m2": absorbed, "net_radiative_W_m2": ABS * SIG * (Ts ** 4 - T_COLD ** 4),
         "carnot_W_m2": ABS * SIG * (Ts ** 4 - T_COLD ** 4) * (1 - T_COLD / Ts),
         "photon_fraction_above_CuO_gap_1.35eV": float(np.sum(photon_flux(Ts)[E > 1.35]) / np.sum(photon_flux(Ts)))}
    for mode in ("ideal", "fowler"):
        s1 = {str(p): best_power(Ts, Ts, p, mode)["P_W_m2"] for p in PHI}
        s2 = {str(p): best_power(Ts, T_COLD, p, mode) for p in PHI}
        bp = max(s2, key=lambda k: s2[k]["P_W_m2"])
        r[mode] = {"S1_isothermal_max_P": s1, "S1_max_rel": max(s1.values()) / absorbed,
                   "S2_by_phi": s2, "S2_best_phi_eV": float(bp), "S2_best_P_W_m2": s2[bp]["P_W_m2"],
                   "S2_best_drift_v_m_s": abs(s2[bp]["J_A_m2"]) / (N_CU * q)}
    res[str(int(Ts))] = r

# thermoelectric across the coating
dT_coat = 1000.0 * 1e-7 / 3.0
V_coat = 1e-3 * dT_coat

g = lambda T, m, k: res[str(T)][m][k]
P = {
 "P1_isothermal_zero": all(g(T, m, "S1_max_rel") < 1e-9 for T in (340, 423, 573, 773) for m in ("ideal", "fowler")),
 "P2_ESS2_store_tiny": g(340, "ideal", "S2_best_P_W_m2") < 1.0,
 "P3_fowler_penalty": all(g(T, "fowler", "S2_best_P_W_m2") <= 0.01 * g(T, "ideal", "S2_best_P_W_m2") for T in (340, 423, 573, 773)),
 "P4_hot_store_nonzero": g(773, "ideal", "S2_best_P_W_m2") > 10.0,
 "P5_motion_not_direction": all(g(T, m, "S2_best_drift_v_m_s") / VF < 1e-6 for T in (340, 423, 573, 773) for m in ("ideal", "fowler")),
 "P6_coating_thermoelectric_negligible": dT_coat < 1e-3 and V_coat < 1e-6,
}
out = {"results": res, "coating_dT_K": dT_coat, "coating_V_at_1mV_per_K": V_coat,
       "verdicts": {k: "PASS" if v else "FAIL" for k, v in P.items()}}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
for T, r in res.items():
    print(f"T_s={T} K ({int(T)-273} C): absorbed {r['absorbed_W_m2']:.0f}  net {r['net_radiative_W_m2']:.0f}  Carnot {r['carnot_W_m2']:.1f} W/m2  "
          f">1.35eV photons {r['photon_fraction_above_CuO_gap_1.35eV']:.1e}")
    for m in ("ideal", "fowler"):
        x = r[m]
        print(f"   {m:6s} S1 max {x['S1_isothermal_max_P'][max(x['S1_isothermal_max_P'], key=x['S1_isothermal_max_P'].get)]:.1e}  "
              f"S2 best {x['S2_best_P_W_m2']:.3e} W/m2 at phi={x['S2_best_phi_eV']}  v_d {x['S2_best_drift_v_m_s']:.1e} m/s  "
              + " ".join(f"{p}:{x['S2_by_phi'][p]['P_W_m2']:.1e}" for p in x['S2_by_phi']))
print(f"coating dT {dT_coat:.1e} K, V {V_coat:.1e} V")
print(out["verdicts"])
