"""BC5: black-copper IR rectenna (implements PREREG.json). Deterministic, numpy only."""
import json, os, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
h, kB, SIG = 6.62607015e-34, 1.380649e-23, 5.670374419e-8
ABS, T_C, BC2_IDEAL_340 = 0.96, 293.0, 6.379e-06
nu = np.linspace(1e9, 4e14, 400000); dnu = nu[1] - nu[0]
mode = lambda T: h * nu / np.expm1(np.clip(h * nu / (kB * T), 1e-12, 700))     # W/Hz, one mode

def run(Th, beta, Rd, fc):
    w = 1.0 / (1.0 + (nu / (fc * 1e12)) ** 2)
    net_spec = mode(Th) - mode(T_C)
    frac = np.sum(net_spec * w) / np.sum(net_spec) if Th != T_C else 0.0
    P_in = ABS * np.sum(net_spec * w) * dnu                      # W per antenna (one polarization)
    carnot = 1 - T_C / Th if Th > T_C else 0.0
    eta = min(beta ** 2 * max(P_in, 0) * Rd / 4.0, carnot)
    flux = ABS * SIG * (Th ** 4 - T_C ** 4) * frac                # covered net flux, W/m^2
    return {"frac_passed": frac, "P_in_W": P_in, "eta_rect": eta, "P_out_W_m2": flux * eta, "carnot_W_m2": ABS * SIG * (Th ** 4 - T_C ** 4) * carnot}

res = {}
for Th in (293.0, 340.0, 423.0, 573.0, 773.0):
    for beta in (0.5, 5.0):
        for Rd in (100.0, 1000.0):
            for fc in (1, 10, 30, 100):
                res[f"Th={Th:g},beta={beta},R={Rd:g},fc={fc}"] = run(Th, beta, Rd, fc)
g = lambda Th, b, R, f: res[f"Th={Th:g},beta={b},R={R:g},fc={f}"]
P1 = all(v["P_out_W_m2"] == 0 for k, v in res.items() if k.startswith("Th=293"))
P2 = g(340, 5.0, 1000.0, 1)["frac_passed"] < 0.05 and g(340, 5.0, 1000.0, 30)["frac_passed"] > 0.5
P3 = all(v["P_in_W"] < 1e-7 and v["eta_rect"] < 1e-3 for k, v in res.items() if k.startswith("Th=340"))
best340 = g(340, 5.0, 1000.0, 100)["P_out_W_m2"]
P4 = best340 >= 100 * BC2_IDEAL_340
P5 = g(773, 5.0, 1000.0, 100)["P_out_W_m2"] > 1.0
out = {"results": res, "verdicts": {k: ("PASS" if v else "FAIL") for k, v in
       {"P1_isothermal_zero": P1, "P2_cutoff": P2, "P3_small_signal": P3, "P4_beats_photoemission": P4, "P5_hot_store": P5}.items()}}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
for Th in (340.0, 423.0, 573.0, 773.0):
    r = g(Th, 5.0, 1000.0, 100); c = g(Th, 5.0, 1000.0, 30); lo = g(Th, 0.5, 100.0, 30)
    print(f"T_h={Th-273:.0f} C: pass(1/10/30/100 THz)= " + "/".join(f"{g(Th,5.0,1000.0,f)['frac_passed']:.2f}" for f in (1,10,30,100)) +
          f"  P_in={r['P_in_W']:.2e} W  best eta={r['eta_rect']:.2e}  P_out best={r['P_out_W_m2']:.2e} W/m2 (fc30 {c['P_out_W_m2']:.2e}; weak diode {lo['P_out_W_m2']:.2e})  Carnot {r['carnot_W_m2']:.0f}")
print(f"BC2 ideal photoemission at 67 C: {BC2_IDEAL_340:.1e} W/m2; best rectenna / BC2 = {best340/BC2_IDEAL_340:.0f}x")
print(out["verdicts"])
