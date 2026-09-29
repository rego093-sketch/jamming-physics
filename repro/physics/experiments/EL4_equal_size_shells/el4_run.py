"""EL4: equal-size shells (implements PREREG.json). Deterministic."""
import json, os, hashlib, math
HERE = os.path.dirname(os.path.abspath(__file__))
target, r_p, a0, D = 137.035999, 0.8414e-15, 52.9177e-12, 4.852620477e-12
inv_alpha = lambda n: math.sqrt(4 * math.pi * n)
routes = {"N1_consumption": 3 * math.pi ** 4, "N2_mass": 6 * math.pi ** 5, "N3_structure": 89}
res = {"formula": "1/alpha = sqrt(4 pi n), eps = sqrt(4 pi / n)", "routes": {}}
for k, n in routes.items():
    v = inv_alpha(n); res["routes"][k] = {"n": n, "inv_alpha": v, "rel": v / target - 1, "HIT": abs(v / target - 1) < 1e-3}
n_req = target ** 2 / (4 * math.pi); eps = 4 * math.pi / target
R = D / eps
shells = math.log(R / r_p) / math.log(1 + eps)
res["required"] = {"n_per_shell": n_req, "eps_bead_over_radius": eps, "R_over_D": R / D, "R_m": R,
                   "shells_from_proton_radius": shells, "n_over_nu_p": n_req / (3 * math.pi ** 4), "n_over_mass_ratio": n_req / (6 * math.pi ** 5)}
txt = json.dumps(res, indent=2)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
for k, r in res["routes"].items():
    print(f"{k:15s} n = {r['n']:8.1f} -> 1/alpha = {r['inv_alpha']:7.2f} ({r['rel']:+.3f}) HIT={r['HIT']}")
q = res["required"]
print(f"required: n = {q['n_per_shell']:.1f} per shell (= {q['n_over_nu_p']:.2f} nu_p = {q['n_over_mass_ratio']:.3f} m_p/m_e), eps = {q['eps_bead_over_radius']:.4f}, "
      f"R = {q['R_over_D']:.3f} D, shells from r_p = {q['shells_from_proton_radius']:.0f}")
