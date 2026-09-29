"""EL2: attempt 1/alpha from the stiff-zone principle (implements PREREG.json). Observations + internal quantities only."""
import json, os, hashlib, math
HERE = os.path.dirname(os.path.abspath(__file__))
E_ann, E_ion, mpme = 510998.95, 13.598434, 1836.15267     # eV, eV, ratio (observed)
a0, lamC = 52.918e-12, 2.42631e-12                          # m (observed)
D, nu_p, phi = 4.852620477e-12, 3 * math.pi ** 4, 0.63      # whitepaper
target = math.sqrt(E_ann / (2 * E_ion) / (1 + 1 / mpme))
r_rot = D / (4 * math.pi)
bridge = a0 / r_rot
R_of_N = lambda N: (D / 2) * (N / phi) ** (1 / 3)
routes = {
    "R1_reservoir": R_of_N(nu_p),
    "R2_competition": R_of_N(nu_p ** 2),
    "R3_mass_count": R_of_N(6 * math.pi ** 5),
    "R4_inflow_vs_hop": math.sqrt(nu_p * (math.pi / 6) * D ** 3 / (4 * math.pi * D)),
}
res = {"target_inv_alpha_obs": target, "bridge_a0_over_r_rot": bridge, "bridge_rel": bridge / target - 1,
       "bridge_ok": abs(bridge / target - 1) < 1e-3, "routes": {}}
for k, R in routes.items():
    v = R / r_rot
    res["routes"][k] = {"R_over_D": R / D, "inv_alpha": v, "rel": v / target - 1, "HIT": abs(v / target - 1) < 1e-3}
R_star = target * r_rot
res["would_hit"] = {"R_over_D": R_star / D, "N_quanta_phi_jam": phi * (2 * R_star / D) ** 3,
                    "N_over_nu_p": phi * (2 * R_star / D) ** 3 / nu_p}
txt = json.dumps(res, indent=2)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(f"target 1/alpha_obs = {target:.4f};  bridge a0/(D/4pi) = {bridge:.4f} (rel {res['bridge_rel']:.1e}) ok={res['bridge_ok']}")
for k, r in res["routes"].items():
    print(f"{k:18s} R = {r['R_over_D']:6.2f} D  -> 1/alpha = {r['inv_alpha']:8.2f}  rel {r['rel']:+.3f}  HIT={r['HIT']}")
w = res["would_hit"]; print(f"would hit: R = {w['R_over_D']:.3f} D, N = {w['N_quanta_phi_jam']:.0f} quanta = {w['N_over_nu_p']:.2f} nu_p")
