"""BC4 companion: standard-physics predictions, systematic budget and thresholds for the bench test (PREREG.json).
Deterministic, numpy only. Inputs are literature values, declared below.
"""
import json, os, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SIG, C = 5.670374419e-8, 2.99792458e8
K_CU, D_PLATE, EPS = 400.0, 3e-3, 0.96          # W/m/K, m, black-face emissivity
S_CU_INHOM = 0.1e-6                               # V/K, lot-to-lot Cu inhomogeneity (same spool: smaller)
S_CUO = 204e-6                                    # V/K, sputtered p-CuO films (PubMed 35521098)
DT_LEADS = 2.0                                    # K, worst-case temperature difference between lead clamps
N_CU, Q_E, SKIN = 8.5e28, 1.602176634e-19, 2e-8
T_P = 293.0 + 20                                  # plate front ~ 40 C on a cooled block
rows = {}
for Ts_C in (67, 150, 300):
    Ts = Ts_C + 273.15
    q = EPS * SIG * (Ts ** 4 - T_P ** 4)          # net radiative flux into the black face, W/m^2
    dT_plate = q * D_PLATE / K_CU                 # front-back drop through 3 mm copper
    V_inhom = S_CU_INHOM * (DT_LEADS + dT_plate)  # systematic bound, same-metal circuit
    V_cuo_if_contacted = S_CUO * dT_plate         # what a lead ON the black face would add (avoided by design)
    p_rad = q / C                                  # momentum flux absorbed, N/m^2 (photon drag upper bound)
    E_drag = p_rad / (N_CU * Q_E * SKIN)          # equivalent field if all momentum went to skin-depth electrons
    V_drag = E_drag * SKIN                        # voltage across the skin depth (normal to surface)
    rows[str(Ts_C)] = {"net_flux_W_m2": q, "plate_dT_K": dT_plate, "systematic_bound_V": V_inhom,
                       "CuO_contact_artifact_V": V_cuo_if_contacted, "photon_drag_upper_V": V_drag,
                       "threshold_V": max(3 * V_inhom, 3e-6)}
out = {"inputs": {"k_Cu": K_CU, "plate_m": D_PLATE, "S_Cu_inhom": S_CU_INHOM, "S_CuO": S_CUO, "dT_leads": DT_LEADS},
       "standard_prediction_DeltaV": 0.0, "rows": rows}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "PREDICTION.json"), "w"), indent=2)
for k, r in rows.items():
    print(f"T_s={k:>3} C  q={r['net_flux_W_m2']:7.0f} W/m2  plate dT={r['plate_dT_K']*1e3:6.2f} mK  "
          f"systematic<{r['systematic_bound_V']*1e6:.2f} uV  CuO-contact {r['CuO_contact_artifact_V']*1e6:.2f} uV  "
          f"photon-drag<{r['photon_drag_upper_V']:.1e} V  threshold {r['threshold_V']*1e6:.1f} uV")
