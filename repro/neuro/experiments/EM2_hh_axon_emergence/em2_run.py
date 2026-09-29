"""EM2: Hodgkin-Huxley axon emergence (implements PREREG.json). Deterministic, numpy only."""
import json, os, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
Cm, gNa, gK, gL, ENa, EK, EL = 1.0, 120.0, 36.0, 0.3, 115.0, -12.0, 10.613
T = 18.5; phi = 3.0 ** ((T - 6.3) / 10.0)
def an(V): return 0.01 * (10 - V) / (np.exp((10 - V) / 10) - 1) if np.ndim(V) == 0 and abs(V - 10) < 1e-6 else 0.01 * (10 - V) / np.expm1((10 - V) / 10)
def bn(V): return 0.125 * np.exp(-V / 80)
def am(V): return 0.1 * (25 - V) / np.expm1((25 - V) / 10)
def bm(V): return 4.0 * np.exp(-V / 18)
def ah(V): return 0.07 * np.exp(-V / 20)
def bh(V): return 1.0 / (np.exp((30 - V) / 10) + 1)
def ss(V): return am(V) / (am(V) + bm(V)), ah(V) / (ah(V) + bh(V)), an(V) / (an(V) + bn(V))
V0 = 1e-6; m0, h0, n0 = ss(V0)

def gates(V, m, h, n, dt):
    # exponential-Euler update of gating variables (exact for fixed V over dt)
    for (a, b, x) in ((am(V), bm(V), 'm'), (ah(V), bh(V), 'h'), (an(V), bn(V), 'n')):
        tau = 1 / (phi * (a + b)); inf = a / (a + b)
        if x == 'm': m = inf + (m - inf) * np.exp(-dt / tau)
        elif x == 'h': h = inf + (h - inf) * np.exp(-dt / tau)
        else: n = inf + (n - inf) * np.exp(-dt / tau)
    return m, h, n

def iion(V, m, h, n): return gNa * m ** 3 * h * (V - ENa) + gK * n ** 4 * (V - EK) + gL * (V - EL)

def space_clamp(stims, t_end=30.0, dt=0.005):     # stims: list of (t_on ms, dur ms, amp uA/cm2)
    V, m, h, n = V0, m0, h0, n0; Vs = []
    for i in range(int(t_end / dt)):
        t = i * dt; I = sum(a for (t0, d, a) in stims if t0 <= t < t0 + d)
        m, h, n = gates(V, m, h, n, dt)
        V += dt * (I - iion(V, m, h, n)) / Cm; Vs.append(V)
    return np.array(Vs)

# P3 threshold (1 ms pulse)
peaks = {}
for amp in (1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20):
    peaks[amp] = float(space_clamp([(1.0, 1.0, amp)], 15.0).max())
sub = [a for a, p in peaks.items() if p < 10]; sup = [a for a, p in peaks.items() if p > 80]
thr = min(sup) if sup else None
P3 = bool(sub) and bool(sup) and max(sub) < min(sup)
amp_rest = max(peaks.values())
# P4 refractory: two pulses at 1.5x threshold
A = 1.5 * thr
def second_peak(gap):
    v = space_clamp([(1.0, 1.0, A), (1.0 + gap, 1.0, A)], 1.0 + gap + 12.0)
    i0 = int((1.0 + gap) / 0.005); return float(v[i0:].max())
p2, p15 = second_peak(2.0), second_peak(15.0)
P4 = p2 < 80 and p15 > 80

# P1 conduction on a cable: a/(2 Ri) d2V/dx2 = Cm dV/dt + Iion ; implicit (backward Euler) diffusion
a_cm, Ri = 238e-4, 35.4
L_cm, dx = 6.0, 0.02; N = int(L_cm / dx) + 1; dt = 0.005   # ms
Dcoef = a_cm / (2 * Ri) * 1e3        # (cm / ohm cm) -> mS/cm ; with Cm in uF/cm2 and t in ms: dV/dt [mV/ms]
r = Dcoef * dt / (Cm * dx * dx)
main = np.full(N, 1 + 2 * r); off = np.full(N - 1, -r); main[0] = main[-1] = 1 + r   # sealed ends
from numpy.linalg import solve
Amat = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
Ainv = np.linalg.inv(Amat)
V = np.full(N, V0); m = np.full(N, m0); h = np.full(N, h0); n = np.full(N, n0)
x1, x2 = int(2.0 / dx), int(4.0 / dx); t1 = t2 = None
for i in range(int(12.0 / dt)):
    t = i * dt
    I = np.zeros(N); I[:int(0.2 / dx)] = 2000.0 if t < 0.3 else 0.0   # amended launch (PREREG_AMENDMENT.json)
    m, h, n = gates(V, m, h, n, dt)
    V = Ainv @ (V + dt * (I - iion(V, m, h, n)) / Cm)
    if t1 is None and V[x1] > 50: t1 = t
    if t2 is None and V[x2] > 50: t2 = t
vel = (x2 - x1) * dx / 100.0 / ((t2 - t1) / 1000.0) if (t1 and t2) else 0.0   # m/s
P1 = abs(vel / 21.2 - 1) <= 0.15
P2 = 90 <= amp_rest <= 120
res = {"threshold_1ms_uA_cm2": thr, "peaks_by_amp": peaks, "spike_amplitude_mV_from_rest": amp_rest,
       "second_spike_peak_gap2ms": p2, "second_spike_peak_gap15ms": p15, "velocity_m_s": vel,
       "compare": {"measured_velocity_m_s": 21.2, "HH_1952_computed_m_s": 18.8},
       "verdicts": {k: ("PASS" if v else "FAIL") for k, v in {"P1_velocity": P1, "P2_amplitude": P2, "P3_all_or_none": P3, "P4_refractory": P4}.items()}}
txt = json.dumps(res, indent=2)
res["sha256x2"] = hashlib.sha256(hashlib.sha256(txt.encode()).digest()).hexdigest()
json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
print(f"threshold (1 ms) = {thr} uA/cm2; peaks {peaks}")
print(f"spike amplitude {amp_rest:.1f} mV; second spike at +2 ms {p2:.1f} mV, at +15 ms {p15:.1f} mV")
print(f"conduction velocity {vel:.2f} m/s (measured 21.2; HH computed 18.8)")
print(res["verdicts"])
