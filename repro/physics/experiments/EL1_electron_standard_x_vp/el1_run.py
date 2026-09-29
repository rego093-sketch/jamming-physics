"""EL1: standard electron data x whitepaper electron definition (implements PREREG.json). Deterministic, no fitting."""
import json, os, hashlib, math
HERE = os.path.dirname(os.path.abspath(__file__))
# CODATA 2018
m_e, e, hbar, c = 9.1093837015e-31, 1.602176634e-19, 1.054571817e-34, 2.99792458e8
mu_e, a_e, alpha = 9.2847647043e-24, 1.15965218128e-3, 7.2973525693e-3
a0, lamC = 5.29177210903e-11, 2.42631023867e-12
D = 4.852620477e-12                     # corpus D_anch (physics s10, s13)
R_POINT = 1e-18                         # m, conservative point-like bound
# Seebeck near 300 K, uV/K (Kasap 2001 table; Ni, Fe, Co standard values)
S = {"Li": 14.0, "Na": -5.0, "K": -12.5, "Mg": -1.4, "Al": -1.8, "Pb": -1.15, "Pd": -9.0, "Pt": -5.28,
     "Mo": 5.6, "Cu": 1.84, "Ag": 1.51, "Au": 1.94, "Ni": -19.5, "Fe": 15.0, "Co": -30.8}

r_mu = 2 * mu_e / (e * c)
P1_val = r_mu / (D / (4 * math.pi) * (1 + a_e)) - 1
P2_val = hbar * c / r_mu / (m_e * c ** 2) - 1
P3_val = (a0 / r_mu) / ((1 / alpha) / (1 + a_e)) - 1
P4_ratio = D / R_POINT
neg = sum(v < 0 for v in S.values()); pos = len(S) - neg
P5_best = max(neg, pos) / len(S)
hop_floor = D / 1.0                      # m/s, one host per electron-second
r_event = D / (2 * math.pi ** 2)
res = {
 "P1_moment_radius": {"r_mu_m": r_mu, "D_over_4pi_times_1pa_m": D / (4 * math.pi) * (1 + a_e), "rel_diff": P1_val,
                      "verdict": "PASS" if abs(P1_val) < 1e-6 else "FAIL", "grade": "[L] consistency through the D anchor (D = 2 lambda_C)"},
 "P2_rotation_energy": {"hbar_c_over_r_mu_over_mc2_minus_1": P2_val, "verdict": "PASS" if abs(P2_val) < 0.01 else "FAIL"},
 "P3_stand_off": {"a0_over_r_mu": a0 / r_mu, "inverse_alpha_over_1pa": (1 / alpha) / (1 + a_e), "rel_diff": P3_val,
                  "verdict": "PASS" if abs(P3_val) < 3e-3 else "FAIL",
                  "consequence": "stand-off in rotator radii = 1/alpha; the whitepaper stand-off claim is equivalent to deriving alpha_em (measured input, s14.5) -> stays [O]"},
 "P4_pointlike": {"D_over_bound": P4_ratio, "R_ext_verdict": "FAIL (excluded)" if P4_ratio > 1e6 else "not excluded",
                  "R_pt_verdict": "survives (a point charge circulating on r_mu has no form factor at the host scale)"},
 "P5_seebeck_direction_rule": {"n_negative": neg, "n_positive": pos, "best_universal_fraction": P5_best,
                               "verdict": "PASS" if P5_best >= 0.9 else "FAIL", "data": S},
 "P6_hop_floor": {"floor_m_per_s": hop_floor, "atomic_electron_speed_alpha_c": alpha * c,
                  "verdict": "non-discriminating (floor is ~1e18 below atomic speeds)"},
 "observation_event_radius": {"r_e_event_m": r_event, "over_r_mu": r_event / r_mu, "two_over_pi": 2 / math.pi,
                              "note": "D/(2 pi^2) = (2/pi) * reduced Compton length (algebraic via D = 2 lambda_C); structural echo, not evidence"},
}
txt = json.dumps(res, indent=2)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(f"P1 r_mu = {r_mu*1e15:.4f} fm vs D/4pi(1+a_e) = {D/(4*math.pi)*(1+a_e)*1e15:.4f} fm  rel {P1_val:.2e}  {res['P1_moment_radius']['verdict']}")
print(f"P2 hbar c / r_mu / mc^2 - 1 = {P2_val:.2e}  {res['P2_rotation_energy']['verdict']}")
print(f"P3 a0/r_mu = {a0/r_mu:.3f} vs (1/alpha)/(1+a_e) = {(1/alpha)/(1+a_e):.3f}  rel {P3_val:.2e}  {res['P3_stand_off']['verdict']}")
print(f"P4 D / point bound = {P4_ratio:.1e}  R_ext {res['P4_pointlike']['R_ext_verdict']}")
print(f"P5 Seebeck signs: {neg} negative / {pos} positive -> best universal {P5_best:.2f}  {res['P5_seebeck_direction_rule']['verdict']}")
print(f"P6 hop floor {hop_floor:.2e} m/s vs alpha c {alpha*c:.2e} m/s")
print(f"obs r_e(event)/r_mu = {r_event/r_mu:.6f}, 2/pi = {2/math.pi:.6f}")
