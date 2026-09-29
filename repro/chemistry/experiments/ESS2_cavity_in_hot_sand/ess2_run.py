"""ESS2: black copper lining a cavity inside the hot-sand store (implements PREREG.json).
The absorber's front also faces the hot store; light enters through an aperture A_coll/CR, which is
shuttered at night. Deterministic, numpy only.
"""
import json, os, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = 5.670374419e-8
ALPHA, T_AMB, T_SKY = 0.96, 293.0, 283.0
ETA_OPT, CAV_RATIO, H_AP = 0.85, 20.0, 10.0
C_STORE = 46 * 3.6e6 / 118.0
UA_STORE = C_STORE / (5.4 * 86400.0)
DT, DAYS, A_COLL = 60.0, 30, 1.0
ALPHA_EFF = ALPHA / (ALPHA + (1 - ALPHA) / CAV_RATIO)


def G(t):
    s = t % 86400.0
    d0, d1 = 8 * 3600.0, 16 * 3600.0
    return 800.0 * np.sin(np.pi * (s - d0) / (d1 - d0)) if d0 <= s <= d1 else 0.0


def run(CR):
    A_ap = A_COLL / CR
    T = T_AMB; absorbed = ap = side = 0.0; daily = []
    for n in range(int(DAYS * 86400 / DT)):
        g = G(n * DT)
        q_in = ETA_OPT * ALPHA_EFF * g * A_COLL
        q_ap = (SIG * (T ** 4 - T_SKY ** 4) + H_AP * (T - T_AMB)) * A_ap if g > 0 else 0.0   # shutter at night
        q_side = UA_STORE * (T - T_AMB)
        T += DT * (q_in - q_ap - q_side) / C_STORE
        absorbed += q_in * DT; ap += q_ap * DT; side += q_side * DT
        if (n + 1) % int(86400 / DT) == 0:
            daily.append(T - 273.15)
    stored = C_STORE * (T - T_AMB)
    return {"CR": CR, "aperture_m2": A_ap, "store_T_day5_C": daily[4], "store_T_day30_C": daily[-1],
            "absorbed_kWh": absorbed / 3.6e6, "aperture_loss_kWh": ap / 3.6e6, "insulation_loss_kWh": side / 3.6e6,
            "stored_kWh": stored / 3.6e6, "carnot_limit_at_store_T": 1 - T_AMB / T,
            "daily_store_T_C": [round(x, 2) for x in daily]}


res = {f"CR={cr}": run(cr) for cr in (1, 10, 50, 200)}
g = lambda cr: res[f"CR={cr}"]
P1 = all(g(cr)["store_T_day30_C"] - g(cr)["store_T_day5_C"] > 50 for cr in (50, 200))
P2 = all(g(cr)["stored_kWh"] > 8.6 for cr in (10, 50, 200))
P3 = all(g(cr)["insulation_loss_kWh"] > g(cr)["aperture_loss_kWh"] for cr in (50, 200))
P4 = g(1)["store_T_day30_C"] - g(1)["store_T_day5_C"] < 50
out = {"alpha_eff_cavity": ALPHA_EFF, "results": res,
       "P1_accumulates": "PASS" if P1 else "FAIL", "P2_beats_ESS1": "PASS" if P2 else "FAIL",
       "P3_limit_is_insulation": "PASS" if P3 else "FAIL", "P4_CR1_no_rescue": "PASS" if P4 else "FAIL"}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(f"alpha_eff (cavity) = {ALPHA_EFF:.4f}")
for k, r in res.items():
    print(f"{k:7s} T5 {r['store_T_day5_C']:6.1f} C  T30 {r['store_T_day30_C']:6.1f} C  stored {r['stored_kWh']:6.1f} kWh "
          f"of {r['absorbed_kWh']:.0f}  aperture {r['aperture_loss_kWh']:6.1f}  insulation {r['insulation_loss_kWh']:6.1f}  Carnot {r['carnot_limit_at_store_T']:.2f}")
print({k: out[k] for k in out if k.startswith('P')})
