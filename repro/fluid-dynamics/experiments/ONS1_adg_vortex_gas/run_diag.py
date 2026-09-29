"""Diagnostics: (a) merger-free first-passage counts vs threshold for N=32,64,128;
(b) dt-halving check on the one configuration that merged inside the window."""
import json, os, time, multiprocessing as mp
import adg_vortex_gas as m
HERE = os.path.dirname(os.path.abspath(__file__))
THR = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]

def job(a):
    try:
        return m.run(**a)
    except TimeoutError:
        return dict(a, timeout=True)

if __name__ == "__main__":
    jobs = [dict(N=128, rc=1e-9, seed=s, track=THR, wall_limit=2400) for s in (101, 102)]
    jobs += [dict(N=64, rc=0.002, seed=101, dt_max_T0=1 / 4000, wall_limit=2400)]
    jobs += [dict(N=N, rc=1e-9, seed=s, track=THR, wall_limit=2400) for N in (64, 32) for s in (101, 102, 103, 104, 105)]
    t0 = time.time()
    with mp.Pool(4) as p:
        res = p.map(job, jobs, chunksize=1)
    print("done", time.time() - t0)
    json.dump(dict(runs=res), open(os.path.join(HERE, "runs_diag.json"), "w"), indent=1)
