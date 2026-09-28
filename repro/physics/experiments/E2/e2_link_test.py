"""E2: does the wavelength-free lattice amplification A link lambda (light) and D (electron)?

Implements PREREG.json exactly. numpy only. Writes RESULT.json next to this file.
"""
import hashlib, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PRE = json.load(open(os.path.join(HERE, "PREREG.json")))

LAMBDA = 6.3299121257859865746e-7          # m, I2-HeNe (CIPM)
LAMBDA_CE = 2.42631023538e-12              # m, CODATA 2022
D = 2 * LAMBDA_CE
A_REQ = 2 * math.pi * LAMBDA / D


def load(path):
    with open(path) as f:
        cols = f.readline().strip().split(",")
    a = np.genfromtxt(path, delimiter=",", skip_header=1)[:, cols.index("A_post")]
    return a[np.isfinite(a) & (a > 0)]


def main():
    per_seed, files = {}, {}
    for rel, want in PRE["data"]["files"].items():
        p = os.path.join(HERE, rel)
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        assert got == want, f"hash mismatch for {rel}"
        files[rel] = got
        per_seed[rel] = load(p)
    A = np.concatenate(list(per_seed.values()))
    med = float(np.median(A))

    rng = np.random.default_rng(19)
    boots = np.median(rng.choice(A, size=(10000, A.size), replace=True), axis=1)
    lo, hi = (float(x) for x in np.percentile(boots, [2.5, 97.5]))
    half = (hi - lo) / 2

    verdict = "PASS" if lo <= A_REQ <= hi else "FAIL"
    res = {
        "verdict": verdict,
        "A_req": A_REQ,
        "A_median_pooled": med,
        "A_median_CI95": [lo, hi],
        "n_avalanches": int(A.size),
        "per_seed_median": {k: float(np.median(v)) for k, v in per_seed.items()},
        "A_req_over_median": A_REQ / med,
        "pull_in_halfwidths": (A_REQ - med) / half,
        "CI_relative_width": (hi - lo) / med,
        "D_pred_pm": 2 * math.pi * LAMBDA / med * 1e12,
        "D_pred_CI_pm": [2 * math.pi * LAMBDA / hi * 1e12, 2 * math.pi * LAMBDA / lo * 1e12],
        "D_measured_pm": D * 1e12,
        "lambda_pred_nm": med * D / (2 * math.pi) * 1e9,
        "lambda_pred_CI_nm": [lo * D / (2 * math.pi) * 1e9, hi * D / (2 * math.pi) * 1e9],
        "lambda_measured_nm": LAMBDA * 1e9,
        "input_sha256": files,
    }
    json.dump(res, open(os.path.join(HERE, "RESULT.json"), "w"), indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
