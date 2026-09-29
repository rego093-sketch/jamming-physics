"""WB1: pre-registered predictions for the Gaia wide-binary test of a0 = c*H0/(2*pi).
Computes only what each hypothesis predicts (no data read). Deterministic."""
import json, math, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))
G, c, Msun, AU = 6.67430e-11, 2.99792458e8, 1.98847e30, 1.495978707e11
Mpc = 3.0856775814913673e22
H0 = {"Planck2018_67.4": 67.4e3 / Mpc, "SH0ES_73.0": 73.0e3 / Mpc}
a0_vp = {k: c * h / (2 * math.pi) for k, h in H0.items()}
g_ext_MW = (233e3) ** 2 / (8.2e3 * 3.0856775814913673e16)   # circular speed 233 km/s at R0 8.2 kpc (cited Galactic values)
nu = lambda x: 1.0 / (1.0 - math.exp(-math.sqrt(x)))            # the volume's own interpolation (ch6_galaxy_rar.py)
M = 1.5 * Msun                                                   # typical total mass of a pair in the El-Badry+2021 sample
rows = []
for s_kau in (1, 2, 3, 5, 7, 10, 15, 20, 30):
    s = s_kau * 1e3 * AU
    gN = G * M / s ** 2
    r = {"s_kAU": s_kau, "gN_over_a0": {k: gN / a for k, a in a0_vp.items()}}
    # H_VP_internal: law applied to the internal field only (as the volume writes it; no external-field term stated)
    r["vel_boost_VP_internal"] = {k: math.sqrt(nu(gN / a)) for k, a in a0_vp.items()}
    # H_VP_EFE_bound: if the Galactic field enters the argument, the boost is bounded by nu(g_ext/a0) (quasi-Newtonian regime)
    r["vel_boost_VP_EFE_bound"] = {k: math.sqrt(nu((gN + g_ext_MW) / a)) for k, a in a0_vp.items()}
    r["vel_boost_Newton"] = 1.0
    rows.append(r)
res = {"a0_vp": a0_vp, "g_ext_MW": g_ext_MW, "g_ext_over_a0": {k: g_ext_MW / a for k, a in a0_vp.items()}, "rows": rows}
txt = json.dumps(res, indent=1, sort_keys=True)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "PREDICTIONS.json"), "w"), indent=1, sort_keys=True)
print(f"a0 (VP) = {a0_vp['Planck2018_67.4']:.3e} .. {a0_vp['SH0ES_73.0']:.3e} m/s^2; Galactic field at Sun = {g_ext_MW:.2e} ({g_ext_MW/a0_vp['Planck2018_67.4']:.2f} a0)")
print(" s[kAU]  gN/a0   boost_internal  boost_EFE_bound  Newton")
for r in rows:
    k = "Planck2018_67.4"
    print(f"{r['s_kAU']:6}  {r['gN_over_a0'][k]:6.2f}   {r['vel_boost_VP_internal'][k]:.3f}           {r['vel_boost_VP_EFE_bound'][k]:.3f}            1.000")
