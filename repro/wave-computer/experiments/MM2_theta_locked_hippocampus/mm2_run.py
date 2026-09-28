"""MM2: theta-locked hippocampal module on the frozen wave-computer core (implements PREREG.json)."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, '..', '..', 'repro'))
import wave_compute_core as w

N, M, P, JIT, NS = 256, 4, 15, 0.8, 40
B = N // M


def relax_locked(theta, J, domega, kappa, dt=0.05, steps=600):
    """wave_compute_core.relax plus a frequency offset and theta locking (carrier frame)."""
    theta = theta.copy()
    for _ in range(steps):
        s, c = np.sin(theta), np.cos(theta)
        theta = theta + dt * (domega + c * (J @ s) - s * (J @ c) - kappa * np.sin(2 * theta))
    return theta


def overlap_inv(theta, xi):
    psi = np.angle(np.mean(xi * np.exp(1j * theta)))
    s = np.sign(np.cos(theta - psi)); s[s == 0] = 1.0
    return abs(float(np.mean(s * xi)))


def rate(sigma, kappa, k=2, coherent=True, use_J=True):
    ok = 0
    for s in range(NS):
        rng = np.random.default_rng(6000 + s)
        xi = rng.choice([-1, 1], size=(P, N))
        J = w.hebbian_field(xi) if use_J else np.zeros((N, N))
        dom = rng.normal(0, sigma, N)
        th = rng.uniform(0, 2 * np.pi, N)
        for m in range(k):
            blk = slice(m * B, (m + 1) * B)
            th[blk] = w.pattern_to_phase(xi[0 if coherent else m])[blk] + rng.normal(0, JIT, B)
        ok += overlap_inv(relax_locked(th, J, dom, kappa), xi[0]) >= 0.9
    return ok / NS


# identity check against the unmodified core
rng = np.random.default_rng(19); xi = rng.choice([-1, 1], size=(P, N)); J = w.hebbian_field(xi)
th0 = rng.uniform(0, 2 * np.pi, N)
identity = bool(np.allclose(relax_locked(th0, J, np.zeros(N), 0.0), w.relax(th0, J, steps=600)))

r = {"P1": rate(0.4, 0.0), "P2": rate(0.4, 0.3), "P3": rate(0.4, 0.3, use_J=False), "P4": rate(0.0, 0.8)}
ks = {k: rate(0.4, 0.3, k=k) for k in range(1, M + 1)}
inc4 = rate(0.4, 0.3, k=4, coherent=False)
grid = {f"sigma={sg}": {f"kappa={kp}": rate(sg, kp) for kp in (0.0, 0.1, 0.3, 0.5)} for sg in (0.0, 0.2, 0.4, 0.6)}
kv = [ks[k] for k in range(1, M + 1)]
res = {
    "identity_with_core": identity,
    "rates": {"no_lock_sigma0.4": r["P1"], "locked_sigma0.4": r["P2"], "locked_noJ_sigma0.4": r["P3"],
              "overlocked_sigma0_kappa0.8": r["P4"], "cue_sweep_congruent": ks, "incongruent_k4": inc4},
    "grid_k2": grid,
    "P1_collapse": "PASS" if r["P1"] <= 0.20 else "FAIL",
    "P2_rescue": "PASS" if (r["P2"] >= 0.60 and r["P2"] - r["P1"] >= 0.40) else "FAIL",
    "P3_content_from_memory": "PASS" if r["P3"] <= 0.05 else "FAIL",
    "P4_overlocking": "PASS" if r["P4"] <= 0.20 else "FAIL",
    "P5_amplification_survives": "PASS" if (all(b >= a for a, b in zip(kv, kv[1:])) and kv[-1] - kv[0] >= 0.40 and inc4 <= 0.20) else "FAIL",
}
json.dump(res, open(os.path.join(HERE, 'RESULT.json'), 'w'), indent=2)
print(json.dumps(res, indent=2))
