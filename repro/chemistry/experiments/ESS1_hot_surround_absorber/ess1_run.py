"""ESS1: black-copper absorber with and without the hot-surround (ESS) boundary condition.
Implements PREREG.json. Deterministic, numpy only.
"""
import json, os, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIG = 5.670374419e-8
ALPHA, T_AMB, T_SKY = 0.96, 293.0, 283.0
C_STORE = 46 * 3.6e6 / 118.0            # J/K   (CA.5: 46 kWh over 118 K)
UA_STORE = C_STORE / (5.4 * 86400.0)     # W/K   (CA.5: tau = 5.4 days)
C_PLATE = 8960 * 1e-3 * 385.0            # 1 m^2 x 1 mm copper plate, J/K
DT, DAYS = 60.0, 30


def G(t):
    s = t % 86400.0
    day0, day1 = 8 * 3600.0, 16 * 3600.0  # 8 h day centred at noon
    if day0 <= s <= day1:
        return 800.0 * np.sin(np.pi * (s - day0) / (day1 - day0))
    return 0.0


def front_loss(T, eps, h):
    return eps * SIG * (T ** 4 - T_SKY ** 4) + h * (T - T_AMB)


def case_A(eps, h):
    """free-standing plate: both faces lose heat; no store."""
    T = T_AMB; Tmax = T; absorbed = lost = 0.0
    for n in range(int(DAYS * 86400 / DT)):
        q_in = ALPHA * G(n * DT)
        q_out = 2 * front_loss(T, eps, h)
        T += DT * (q_in - q_out) / C_PLATE
        absorbed += q_in * DT; lost += q_out * DT; Tmax = max(Tmax, T)
    kept = C_PLATE * (T - T_AMB)
    return {"peak_T_C": Tmax - 273.15, "absorbed_kWh": absorbed / 3.6e6, "kept_kWh": kept / 3.6e6,
            "kept_fraction": kept / absorbed}


def case_B(eps, h):
    """plate = top face of the hot-sand store; rear loss 0; store insulated with UA_STORE."""
    T = T_AMB; absorbed = front = side = 0.0; daily_T = []
    for n in range(int(DAYS * 86400 / DT)):
        q_in = ALPHA * G(n * DT)
        qf = front_loss(T, eps, h); qs = UA_STORE * (T - T_AMB)
        T += DT * (q_in - qf - qs) / (C_STORE + C_PLATE)
        absorbed += q_in * DT; front += qf * DT; side += qs * DT
        if (n + 1) % int(86400 / DT) == 0:
            daily_T.append(T - 273.15)
    stored = (C_STORE + C_PLATE) * (T - T_AMB)
    carnot = 1 - T_AMB / T
    return {"store_T_day5_C": daily_T[4], "store_T_day30_C": daily_T[-1], "absorbed_kWh": absorbed / 3.6e6,
            "front_loss_kWh": front / 3.6e6, "insulation_loss_kWh": side / 3.6e6, "stored_kWh": stored / 3.6e6,
            "stored_fraction": stored / absorbed, "carnot_limit_at_store_T": carnot,
            "daily_store_T_C": [round(x, 2) for x in daily_T]}


res = {}
for eps in (0.90, 0.15):
    for glazed, h in (("unglazed", 10.0), ("glazed", 3.0)):
        key = f"eps={eps},{glazed}"
        res[key] = {"A_free_standing": case_A(eps, h), "B_ESS_hot_surround": case_B(eps, h)}

A90 = res["eps=0.9,unglazed"]["A_free_standing"]
P1 = abs(A90["kept_fraction"]) < 0.01 and A90["peak_T_C"] < 200
P2 = any(v["B_ESS_hot_surround"]["store_T_day30_C"] - v["B_ESS_hot_surround"]["store_T_day5_C"] > 50 for v in res.values())
P3 = all(v["B_ESS_hot_surround"]["stored_kWh"] >= 10 * max(v["A_free_standing"]["kept_kWh"], 1e-9) for v in res.values())
P4 = all(res[f"eps=0.9,{g}"]["B_ESS_hot_surround"]["store_T_day30_C"] < res[f"eps=0.15,{g}"]["B_ESS_hot_surround"]["store_T_day30_C"]
         for g in ("unglazed", "glazed"))
out = {"inputs": {"alpha": ALPHA, "C_store_J_per_K": C_STORE, "UA_store_W_per_K": UA_STORE, "C_plate_J_per_K": C_PLATE},
       "results": res,
       "P1_escape": "PASS" if P1 else "FAIL", "P2_keeps_absorbing": "PASS" if P2 else "FAIL",
       "P3_hot_surround_gain": "PASS" if P3 else "FAIL", "P4_front_limit": "PASS" if P4 else "FAIL"}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
for k, v in res.items():
    a, b = v["A_free_standing"], v["B_ESS_hot_surround"]
    print(f"{k:22s} A: peak {a['peak_T_C']:6.1f} C kept {a['kept_fraction']*100:5.2f}% | "
          f"B: T5 {b['store_T_day5_C']:6.1f} C T30 {b['store_T_day30_C']:6.1f} C stored {b['stored_kWh']:6.1f} kWh "
          f"({b['stored_fraction']*100:4.1f}% of {b['absorbed_kWh']:.0f}) front {b['front_loss_kWh']:.0f} ins {b['insulation_loss_kWh']:.0f} Carnot {b['carnot_limit_at_store_T']:.2f}")
print({k: out[k] for k in out if k.startswith("P")})
