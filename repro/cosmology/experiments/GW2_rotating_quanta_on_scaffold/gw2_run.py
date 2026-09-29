"""GW2: rotating quanta carried on the VP scaffold (implements PREREG.json).

VP scaffold = 1-D chain along the ray (always full, c_L = a*sqrt(k/m) = 1).
Quanta     = rotors about the ray axis at occupied sites, coupled to the local strain:
             V = sum 1/2 k eps^2 + sum_occ 1/2 kappa (theta - g eps)^2   (two-way coupling).
Measured: strain-peak speed (P1), rotation-pattern speed and arrival after a quanta-empty gap
(P2, P3), and the polarization content of dipole / quadrupole quanta read on a ring (P4).
Deterministic; numpy only.
"""
import json, os, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PRE = json.load(open(os.path.join(HERE, 'PREREG.json')))
N, W, G, I = 6000, 20.0, 1.0, 1.0
GAP = (3000, 3600)
PROBES = [1500, 2500, 3300, 4200, 5200]
X0 = 700.0


def run(kappa, dt=0.1):
    occ = np.ones(N - 1); occ[GAP[0]:GAP[1]] = 0.0              # quanta live on bonds (strain sites)
    x = np.arange(N, dtype=float)
    u = np.exp(-((x - X0) / W) ** 2)                           # displacement pulse
    v = 2 * (x - X0) / W ** 2 * u                               # right-moving: v = -c du/dx
    eps = np.diff(u)
    th = G * eps * occ                                          # rotors start slaved (no kick)
    om = G * np.diff(v) * occ
    t_end = 5600.0
    nsteps = int(t_end / dt)
    rec_e = {p: [] for p in PROBES}; rec_t = {p: [] for p in PROBES}; ts = []

    def acc(u, th):
        e = np.diff(u)
        sig = e - G * kappa * (th - G * e) * occ               # k=1
        F = np.zeros(N); F[:-1] += sig; F[1:] -= sig
        F[0] = F[-1] = 0.0
        a_th = -kappa * (th - G * e) / I * occ
        return F, a_th

    Fu, Ft = acc(u, th)
    for n in range(nsteps):
        v += 0.5 * dt * Fu; om += 0.5 * dt * Ft
        u += dt * v; th += dt * om
        Fu, Ft = acc(u, th)
        v += 0.5 * dt * Fu; om += 0.5 * dt * Ft
        if n % 5 == 0:
            e = np.diff(u); ts.append((n + 1) * dt)
            for p in PROBES:
                rec_e[p].append(e[p]); rec_t[p].append(th[p])
    ts = np.array(ts)

    def arrival(sig):
        s = np.abs(np.array(sig)); i = int(np.argmax(s))
        if i == 0 or i == len(s) - 1 or s[i] == 0:
            return float('nan'), 0.0
        y0, y1, y2 = s[i - 1], s[i], s[i + 1]; d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
        return float(ts[i] + d * (ts[1] - ts[0])), float(s.max())
    ae = {p: arrival(rec_e[p]) for p in PROBES}
    at = {p: arrival(rec_t[p]) for p in PROBES}
    return ae, at


def speed(a, p, q):
    return (q - p) / (a[q][0] - a[p][0])


pulse_freq = 1.0 / W                                            # c_L / w
res = {}
for name, ratio in (("slaved", 10.0), ("heavy", 1.0)):
    kappa = I * (ratio * pulse_freq) ** 2
    ae, at = run(kappa)
    r = {"kappa": kappa,
         "strain_speed_before": speed(ae, 1500, 2500), "strain_speed_gap": speed(ae, 2500, 3300),
         "strain_speed_after": speed(ae, 4200, 5200),
         "rotation_speed_before": speed(at, 1500, 2500), "rotation_speed_after": speed(at, 4200, 5200),
         "rotation_arrival_speed_across_gap": speed(at, 2500, 4200),
         "rotation_amp_before": at[2500][1], "rotation_amp_after": at[4200][1],
         "rotation_in_gap_amp": at[3300][1]}
    res[name] = r

# ---- P4: polarization content read on a ring of M test points around the ray ----
M = 360
phi = 2 * np.pi * np.arange(M) / M


def ring_response(l, th0, dth=1e-3):
    """field of a body-fixed multipole of order l (l=1 dipole, l=2 traceless quadrupole) at the
    ring, change when the quantum turns by dth. Returns Fourier power by harmonic m=0,1,2,..."""
    f = lambda th: np.cos(l * (phi - th))
    d = f(th0 + dth) - f(th0)
    c = np.fft.rfft(d) / M
    p = np.abs(c) ** 2
    return p / p.sum(), d


pol = {}
for l in (1, 2):
    p, d_a = ring_response(l, 0.0)
    shift = np.pi / (2 * l)                                     # 90 deg (l=1) / 45 deg (l=2)
    _, d_b = ring_response(l, shift)
    overlap = float(abs(np.dot(d_a, d_b)) / (np.linalg.norm(d_a) * np.linalg.norm(d_b)))
    pol[f"l={l}"] = {"monopole_fraction": float(p[0]), f"harmonic_{l}_fraction": float(p[l]),
                     "second_state_rotated_deg": float(np.degrees(shift)),
                     "overlap_between_the_two_states": overlap}

s, h = res["slaved"], res["heavy"]
within = lambda v, tol=0.01: abs(v - 1.0) <= tol
P1 = all(within(s[k]) for k in ("strain_speed_before", "strain_speed_gap", "strain_speed_after"))
P2 = within(s["rotation_speed_before"]) and within(s["rotation_speed_after"]) and within(s["rotation_arrival_speed_across_gap"])
P3 = any(not within(h[k]) for k in ("rotation_speed_before", "rotation_speed_after", "rotation_arrival_speed_across_gap"))
q = pol["l=2"]; d1 = pol["l=1"]
P4 = (q["monopole_fraction"] < 1e-10 and q["harmonic_2_fraction"] > 0.99 and q["overlap_between_the_two_states"] < 1e-6
      and d1["harmonic_1_fraction"] > 0.99 and d1["overlap_between_the_two_states"] < 1e-6)
out = {"propagation": res, "polarization": pol,
       "P1_c_maintained": "PASS" if P1 else "FAIL", "P2_carried": "PASS" if P2 else "FAIL",
       "P3_condition": "PASS" if P3 else "FAIL", "P4_polarization": "PASS" if P4 else "FAIL"}
txt = json.dumps(out, indent=2, default=float)
out["sha256"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(out, open(os.path.join(HERE, 'RESULT.json'), 'w'), indent=2, default=float)
print(json.dumps(out, indent=2, default=float))
