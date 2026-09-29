"""BC6: rectenna optimization at realistic ESS temperatures (implements PREREG.json). Deterministic, numpy only."""
import json, os, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
h, kB, q, SIG = 6.62607015e-34, 1.380649e-23, 1.602176634e-19, 5.670374419e-8
ABS, T_C = 0.96, 293.0
nu = np.linspace(1e10, 6e14, 300000); dnu = nu[1] - nu[0]
mode = lambda T: h * nu / np.expm1(np.clip(h * nu / (kB * T), 1e-12, 700))
R_grid = np.logspace(1, 6, 201)

def eta_TE(Th, ZT):
    m = np.sqrt(1 + ZT); return (1 - T_C / Th) * (m - 1) / (m + T_C / Th)

def optimize(Th, n, C):
    net = mode(Th) - mode(T_C); tot = np.sum(net)
    beta = q / (2 * n * kB * T_C); Vmax = n * kB * T_C / q
    F = ABS * SIG * (Th ** 4 - T_C ** 4); carnot = 1 - T_C / Th
    best = None
    for R in R_grid:
        fc = 1 / (2 * np.pi * R * C); w = 1 / (1 + (nu / fc) ** 2)
        frac = np.sum(net * w) / tot; P_in = ABS * np.sum(net * w) * dnu
        V = np.sqrt(P_in * R)
        if V > Vmax: continue                                   # outside square-law validity
        eta = min(beta ** 2 * P_in * R / 4, carnot)
        P = F * frac * eta
        if best is None or P > best["P_out_W_m2"]:
            best = {"R_ohm": R, "f_c_THz": fc / 1e12, "frac": frac, "P_in_W": P_in, "V_ac_mV": V * 1e3, "eta_rect": eta,
                    "eta_on_net_flux": frac * eta, "P_out_W_m2": P}
    best.update({"net_flux_W_m2": F, "carnot_W_m2": F * carnot, "TE_ZT1_W_m2": F * eta_TE(Th, 1.0), "TE_CuO_ZT005_W_m2": F * eta_TE(Th, 0.05)})
    return best

res = {f"Th={Tc}C,n={n},C={C:g}": optimize(Tc + 273.15, n, C) for Tc in (300, 400, 500, 600) for n in (1.0, 1.5) for C in (1e-18, 1e-17)}
g = lambda T, n, C: res[f"Th={T}C,n={n},C={C:g}"]
P1 = all(v["eta_on_net_flux"] < 0.0625 for v in res.values())
P2 = g(500, 1.0, 1e-18)["P_out_W_m2"] >= 100
P3 = all(v["TE_ZT1_W_m2"] > v["P_out_W_m2"] for v in res.values())
P4 = g(500, 1.0, 1e-18)["P_out_W_m2"] > 2 * g(500, 1.0, 1e-17)["P_out_W_m2"]
out = {"results": res, "verdicts": {k: ("PASS" if v else "FAIL") for k, v in
       {"P1_square_law_ceiling": P1, "P2_500C_output": P2, "P3_TE_wins": P3, "P4_capacitance": P4}.items()}}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(f"{'case':26s} {'R':>8s} {'f_c':>6s} {'pass':>5s} {'V mV':>6s} {'eta_net':>8s} {'P_out':>8s} {'TE ZT1':>8s} {'TE CuO':>7s} {'Carnot':>7s}  (W/m2)")
for k, v in res.items():
    print(f"{k:26s} {v['R_ohm']:8.0f} {v['f_c_THz']:6.1f} {v['frac']:5.2f} {v['V_ac_mV']:6.1f} {v['eta_on_net_flux']:8.4f} {v['P_out_W_m2']:8.1f} {v['TE_ZT1_W_m2']:8.0f} {v['TE_CuO_ZT005_W_m2']:7.0f} {v['carnot_W_m2']:7.0f}")
print(out["verdicts"])
