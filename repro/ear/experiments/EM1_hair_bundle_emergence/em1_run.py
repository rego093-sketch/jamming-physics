"""EM1: single hair bundle emergence (implements PREREG.json). Deterministic RK4, numpy only."""
import json, os, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
lam, lam_a = 2.8e-6, 10e-6                 # N s/m
Kgs, Ksp = 750e-6, 600e-6                  # N/m
D, N, S, gam = 61e-9, 50, 0.65, 0.14
kT = 4.0e-21
delta = N * kT / (Kgs * D)                 # gating length scale
A = np.exp(10.0 + Kgs * D ** 2 / (2 * N * kT))

def Po(y): return 1.0 / (1.0 + A * np.exp(-y / delta))

def rhs(X, Xa, Fmax, F):
    p = Po(X - Xa); fgs = Kgs * (X - Xa - D * p)
    return (-fgs - Ksp * X + F) / lam, (fgs - Fmax * (1 - S * p)) / lam_a   # amended: no gamma on the motor term (PREREG_AMENDMENT.json)

def run(Fmax, T, dt=5e-6, F0=0.0, f=0.0, X0=0.0, Xa0=0.0, rec_from=0.0):
    X, Xa = X0, Xa0; n = int(T / dt); xs = []
    for i in range(n):
        t = i * dt
        F1 = F0 * np.sin(2 * np.pi * f * t)
        k1 = rhs(X, Xa, Fmax, F1)
        Fm = F0 * np.sin(2 * np.pi * f * (t + dt / 2))
        k2 = rhs(X + dt / 2 * k1[0], Xa + dt / 2 * k1[1], Fmax, Fm)
        k3 = rhs(X + dt / 2 * k2[0], Xa + dt / 2 * k2[1], Fmax, Fm)
        F2 = F0 * np.sin(2 * np.pi * f * (t + dt))
        k4 = rhs(X + dt * k3[0], Xa + dt * k3[1], Fmax, F2)
        X += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); Xa += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        if t >= rec_from and i % 5 == 0: xs.append(X)
    return np.array(xs), X, Xa

def osc(Fmax):
    xs, _, _ = run(Fmax, 1.2, rec_from=0.6, X0=5e-9)
    ptp = xs.max() - xs.min(); dt_rec = 5 * 5e-6
    x = xs - xs.mean(); zc = np.where((x[:-1] < 0) & (x[1:] >= 0))[0]
    freq = (len(zc) - 1) / ((zc[-1] - zc[0]) * dt_rec) if len(zc) > 2 else 0.0
    return ptp, freq

scan = {}
for Fm in np.arange(40, 60.01, 0.5):
    ptp, fr = osc(Fm * 1e-12); scan[f"{Fm:.1f}"] = {"ptp_nm": ptp * 1e9, "freq_Hz": fr}
osc_F = [float(k) for k, v in scan.items() if v["ptp_nm"] > 5]
ptp_rep, f_rep = osc(50.3e-12)
res = {"scan": scan, "oscillating_Fmax_pN": osc_F, "at_50_3pN": {"ptp_nm": ptp_rep * 1e9, "freq_Hz": f_rep}}
# locate the quiescent-side edge of the window and probe the forced response there
edges = sorted(osc_F)
if edges:
    lo = edges[0]
    Fq = None
    for Fm in np.arange(lo - 0.5, lo - 2.01, -0.1):   # walk down from the window edge to the first quiescent value
        if osc(Fm * 1e-12)[0] < 1e-9: Fq = round(Fm, 2); break
    ptp_e, f_e = osc(lo * 1e-12)
    f0 = f_e if f_e > 0 else 20.0
    amps, forces = [], np.logspace(-13, -10.5, 11)          # 0.1 - 31.6 pN
    for F0 in forces:
        xs, _, _ = run(Fq * 1e-12, 1.2, F0=F0, f=f0, rec_from=0.7)
        amps.append((xs.max() - xs.min()) / 2)
    amps = np.array(amps); slopes = np.diff(np.log(amps)) / np.diff(np.log(forces))
    res["forced"] = {"Fmax_quiescent_pN": Fq, "f0_Hz": f0, "force_pN": (forces * 1e12).tolist(), "amp_nm": (amps * 1e9).tolist(),
                     "local_exponent": slopes.tolist(), "min_exponent": float(slopes.min())}
P1 = bool(edges) and (50.3 >= min(edges) - 2.5) and (50.3 <= max(edges) + 2.5) and ptp_rep > 5e-9
P2 = 5 <= f_rep <= 50 and 20 <= ptp_rep * 1e9 <= 150
fr_ = res.get("forced", {}); sl = np.array(fr_.get("local_exponent", [9]))
P3 = bool(np.any((sl >= 0.25) & (sl <= 0.45)))
P4 = bool(sl.min() >= 0.25) if sl.size else False
res["verdicts"] = {k: ("PASS" if v else "FAIL") for k, v in {"P1_hopf_emerges": P1, "P2_frequency_amplitude": P2, "P3_compression": P3, "P4_organ_gap": P4}.items()}
txt = json.dumps(res, indent=2)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print("oscillating F_max window (pN):", edges)
print(f"at 50.3 pN: ptp {ptp_rep*1e9:.1f} nm, freq {f_rep:.1f} Hz")
if "forced" in res:
    print(f"forced at F_max={fr_['Fmax_quiescent_pN']} pN, f0={fr_['f0_Hz']:.1f} Hz; local exponents:", [round(x, 2) for x in fr_["local_exponent"]])
print(res["verdicts"])
