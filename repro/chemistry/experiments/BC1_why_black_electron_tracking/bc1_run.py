"""BC1: why black copper is black, and where its photo-excited electrons go (implements PREREG.json).
Deterministic (SEED = 19), numpy only.
Declared choices not fixed in PREREG (made before the first run):
  * Cu interband strength: Im eps_ib = 5*sqrt(E - 2.1 eV) (order of measured Cu eps2 at 2.5-3 eV).
  * Carrier speed 1e5 m/s -> D = v*lambda/3; transport integrated as a Gaussian random walk, dt = 0.5 ps,
    after one ballistic first flight along the (isotropic) initial direction.
  * Temperature gradient: Ito random walk (step size set at the departure point), i.e. J = -d(D n)/dz,
    the kinetic-gas form; P5 is judged on the gradient-induced part (case minus C1).
  * Holes are tracked as well (same D, opposite charge) so the CHARGE current is reported next to the
    pre-registered electron flux.
"""
import json, os, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SEED, kB = 19, 8.617333e-5

# ---------- A: colour ----------
E = np.linspace(1.65, 3.10, 146)
def R_fresnel(eps):
    n = np.sqrt(eps.astype(complex)); return np.abs((n - 1) / (n + 1)) ** 2
eps_cu = 1 - 8.8 ** 2 / (E ** 2 + 1j * 0.09 * E) + 1j * 5 * np.sqrt(np.clip(E - 2.1, 0, None))
R_cu = R_fresnel(eps_cu)
Eg, d = 1.35, 1e-6
A0 = 1e7 / np.sqrt(2.5 - Eg)                                   # alpha(2.5 eV) = 1e5 /cm = 1e7 /m
alpha = A0 * np.sqrt(np.clip(E - Eg, 0, None))
R_cuo = ((2.6 - 1) / (2.6 + 1)) ** 2 / 20
Abs_cuo = (1 - R_cuo) * (1 - np.exp(-alpha * d))
at = lambda arr, e: float(arr[np.argmin(abs(E - e))])
colour = {"Cu_metal_mean_R_visible": float(R_cu.mean()), "Cu_R_red_1.8eV": at(R_cu, 1.8), "Cu_R_blue_2.8eV": at(R_cu, 2.8),
          "CuO_mean_absorptance_visible": float(Abs_cuo.mean()), "CuO_min_absorptance_visible": float(Abs_cuo.min()),
          "CuO_absorption_depth_2.5eV_nm": 1e9 / (A0 * np.sqrt(2.5 - Eg))}

# ---------- B: electron (and hole) tracking ----------
LAM, V, TAU, DT, TMAX, N = 5e-9, 1e5, 1e-9, 5e-13, 5e-9, 20000
D300 = V * LAM / 3

def track(sign, field, Tfun, rng):
    """sign=-1 electron, +1 hole. Returns counts collected at front (z=0), back (z=d), recombined."""
    a = A0 * np.sqrt(2.5 - Eg)
    z = -np.log(1 - rng.random(N) * (1 - np.exp(-a * d))) / a        # Beer-Lambert inside the slab
    mu = 2 * rng.random(N) - 1                                        # isotropic initial direction
    z = z + mu * LAM * rng.exponential(1.0, N)                        # ballistic first flight
    life = rng.exponential(TAU, N)
    state = np.zeros(N, int)                                          # 0 alive, 1 front, 2 back, 3 recombined
    state[z <= 0] = 1; state[z >= d] = 2
    t = 0.0
    while t < TMAX and (state == 0).any():
        al = state == 0
        T = Tfun(z[al]); Dl = D300 * T / 300.0
        mob = Dl / (kB * T)                                            # Einstein, m^2/Vs (kT in eV)
        z[al] += np.sqrt(2 * Dl * DT) * rng.standard_normal(al.sum()) + sign * mob * field * DT
        t += DT
        idx = np.where(al)[0]
        zz = z[idx]
        state[idx[zz <= 0]] = 1; state[idx[zz >= d]] = 2
        still = idx[(zz > 0) & (zz < d)]
        state[still[life[still] <= t]] = 3
    state[state == 0] = 3
    return {"front": int((state == 1).sum()), "back": int((state == 2).sum()), "recombined": int((state == 3).sum())}

T_uni = lambda z: np.full_like(z, 300.0)
T_grad = lambda z: 400.0 - 100.0 * np.clip(z, 0, d) / d               # hot at front (lit face)
T_grad_rev = lambda z: 300.0 + 100.0 * np.clip(z, 0, d) / d
cases = {"C1_no_field": (0.0, T_uni), "C2_junction": (1e5, T_uni),
         "C3_gradient": (0.0, T_grad), "C3r_gradient_reversed": (0.0, T_grad_rev)}
out_B = {}
for k, (F, Tf) in cases.items():
    e = track(-1, F, Tf, np.random.default_rng(SEED)); h = track(+1, F, Tf, np.random.default_rng(SEED + 1))
    e_net = (e["back"] - e["front"]) / N
    # charge current into the back contact per absorbed photon (+ = holes to back / electrons to front)
    q_net = ((h["back"] - h["front"]) - (e["back"] - e["front"])) / (2 * N)
    out_B[k] = {"electrons": e, "holes": h, "electron_net_flux_back_minus_front": e_net, "charge_current_per_photon": q_net}

c1, c2, c3, c3r = (out_B[k] for k in cases)
Eph = 2.5
heat_C1 = 1 - abs(c1["charge_current_per_photon"]) * Eg / Eph              # upper bound on electrical share
g3 = c3["electron_net_flux_back_minus_front"] - c1["electron_net_flux_back_minus_front"]
g3r = c3r["electron_net_flux_back_minus_front"] - c1["electron_net_flux_back_minus_front"]
P = {
 "P1_colour": colour["Cu_metal_mean_R_visible"] > 0.5 and colour["Cu_R_red_1.8eV"] > colour["Cu_R_blue_2.8eV"]
              and colour["CuO_mean_absorptance_visible"] > 0.9,
 "P2_black_alone_no_direction": abs(c1["electron_net_flux_back_minus_front"]) < 0.02,
 "P3_heat": heat_C1 > 0.9,
 "P4_junction_directs": abs(c2["electron_net_flux_back_minus_front"]) > 0.3,
 "P5_gradient_directs": g3 > 0 and g3r < 0,
}
out = {"colour": colour, "tracking": out_B, "heat_fraction_C1_upper": heat_C1,
       "gradient_induced_electron_flux": {"hot_front": g3, "hot_back": g3r},
       "diffusion_length_um": 1e6 * np.sqrt(D300 * TAU),
       "results": {k: "PASS" if v else "FAIL" for k, v in P.items()}}
txt = json.dumps(out, indent=2)
out["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(json.dumps({k: out[k] for k in ("colour", "heat_fraction_C1_upper", "gradient_induced_electron_flux", "diffusion_length_um")}, indent=1))
for k, v in out_B.items():
    print(k, v["electrons"], v["holes"], "e_net %.4f  charge %.4f" % (v["electron_net_flux_back_minus_front"], v["charge_current_per_photon"]))
print(out["results"])
