"""MM1: multimodal cue amplification on the frozen wave-computer core (implements PREREG.json)."""
import json, os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(HERE, '..', '..', 'repro'))
import wave_compute_core as w

PRE = json.load(open(os.path.join(HERE, 'PREREG.json')))
N, M, P, JIT, NS = 256, 4, 15, 0.8, 40
B = N // M


def rate(k, coherent):
    ok, ovs = 0, []
    for s in range(NS):
        rng = np.random.default_rng(5000 + s)
        xi = rng.choice([-1, 1], size=(P, N)); J = w.hebbian_field(xi)
        th = rng.uniform(0, 2 * np.pi, N)
        for m in range(k):
            src = 0 if coherent else m
            blk = slice(m * B, (m + 1) * B)
            th[blk] = w.pattern_to_phase(xi[src])[blk] + rng.normal(0, JIT, B)
        o = abs(w.overlap(w.relax(th, J, steps=600), xi[0])); ovs.append(o); ok += o >= 0.9
    return ok / NS, float(np.mean(ovs))


coh = {k: rate(k, True) for k in range(0, M + 1)}
inc = {k: rate(k, False) for k in range(2, M + 1)}
r = [coh[k][0] for k in range(1, M + 1)]
p1 = all(b >= a for a, b in zip(r, r[1:])) and (coh[4][0] - coh[1][0]) >= 0.40
p2 = (coh[4][0] - inc[4][0]) >= 0.50
res = {"coherent": {k: {"recall_rate": v[0], "mean_overlap": v[1]} for k, v in coh.items()},
       "incoherent": {k: {"recall_rate": v[0], "mean_overlap": v[1]} for k, v in inc.items()},
       "P1_amplification": "PASS" if p1 else "FAIL", "P2_interference": "PASS" if p2 else "FAIL"}
json.dump(res, open(os.path.join(HERE, 'RESULT.json'), 'w'), indent=2)
print(json.dumps(res, indent=2))
