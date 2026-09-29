
# JFM_DOI_FULLSTORY_v4 — DNS demo addendum (reproducible)

**What is this?** An upgrade over `JFM_DOI_FULLSTORY_v3` that adds a minimal,
fully reproducible **2‑D Navier–Stokes DNS demonstration** of the spectrally rotating
forcing and shows how to compute the selected length \(L^\star\) and the control observable
\(S_b\) on a tiny suite of runs.

- `JFM_DOI_FULLSTORY_v3.zip` — your original v3 archive (preserved verbatim).
- `code/dns2d.py` — compact pseudo‑spectral vorticity–streamfunction solver (RK4).
- `scripts/run_dns_suite.py` — generates 5 tiny DNS runs (N=64) with different forcing magnitudes.
- `scripts/analyze_dns_suite.py` — computes \(S_b\), \(L^\star\) and a log–log slope (demo).
- `data/dns_runs/` — **already contains outputs** from a tiny suite so figures can be made immediately.
- `logs/seeds.json` — all random seeds.
- `requirements.txt` / `environment.yml` — pinned dependencies.

## One‑click (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_dns_suite.py         # re‑generate the tiny suite (optional)
python scripts/analyze_dns_suite.py     # produce dns_suite_with_Sb.csv and slope.txt
```

Outputs are placed in `data/dns_runs/`. The file `slope.txt` prints the demo slope
on the 5‑point suite.

## Protocol (representative parameter set)
- Domain: periodic square \([0,1]^2\), grid \(N=64\) (demo; increase for production).
- Viscosity/drag: \(\nu=10^{-3}\), \(\alpha=5\times 10^{-3}\).
- Forcing: spectral annulus centered at \(k_0=8\) with width \(\sigma_k=0.6\);
  sector half‑angle \(15^\circ\) (labelled `theta_deg=30` total opening);
  azimuth rotates at \(\Omega=1.0\) rad/unit time.
- OU amplitude: mean \(A_0\in\{0.25,0.35,0.45,0.60,0.80\}\), time \(\\tau=0.6\), stdev \(\sigma_A=0.15\).
- Time stepping: RK4, \(\\Delta t=0.004\), steps \(=400\), save every 40 steps (demo scale).
- Measurement: average kinetic‑energy spectrum over saved frames; \(k_\star=\arg\max_k E(k)\);
  \(L^\star=2\pi/k_\star\).
- Observable mapping: \(S_b = S/L_0^2\) with \(S=(C^2+w_E E)/\\varepsilon_{\\rm bind}\), \(C^2=\\theta^2\) (rad\(^2\)),
  \(E=\\langle A^2\\rangle\), \(\\varepsilon_{\\rm bind}=\\nu k_0^2+\\alpha\), \(w_E=0.20\), \(L_0=1\).

This matches the *Bridge to measurement* and *Numerics* descriptions in the manuscript (units and
LOOCV policy; tables and captions unchanged).

## Notes
- The solver is intentionally compact and readable. For high‑Re or long integrations, increase N,
  adopt ETDRK4, and raise `steps`. The interface stays identical.
- The archived outputs are tiny and deterministic (seeds logged). Re‑running will reproduce the same
  statistics within numerical noise.
