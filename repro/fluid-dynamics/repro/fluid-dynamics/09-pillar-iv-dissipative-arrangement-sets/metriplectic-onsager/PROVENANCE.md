# Provenance — merged into "The Configured Continuum" (§9 / Appendix E)

This directory was originally prepared as a **standalone reproducibility
package** for the manuscript

> "Vortex-Merger Thermodynamics in 2D Turbulence:
>  A Metriplectic Scenario for the Onsager Anomaly"

(former standalone DOI `10.5281/zenodo.17758705`, v3.0.0). That manuscript
was not registered as a separate Letter; its content and evidence are now
**folded into** the fluid-dynamics whitepaper *The Configured Continuum*
(concept DOI `10.5281/zenodo.17972568`) as the full evidence backing for:

- **§9 — Pillar IV (Dissipative: arrangement sets dissipation)**, and
- **Appendix E — the metriplectic vortex-gas model**.

## Why it lives here (relation to the in-page model)

The whitepaper already ships a lightweight, self-contained reference model
in `../metriplectic_vortex.py`. That script demonstrates only the mean-field
**budget closure** and the `eps_tot -> I` saturation plateau (it explicitly
leaves the microscopic support-localization as an open GATE item).

This package is the **production-grade ensemble evidence** behind the same
claim: the offline ADG (Average Discrete Gradient) ensemble, the
Navier–Stokes viscous reference at 64^2 / 256^2 / 512^2, and the N-/seed-/
r_c-robustness diagnostics. Numerically the two agree — the ensemble
`eps_tot_mean` clusters at ~0.205–0.216, matching the in-page plateau
`I = 0.21`, while extending the reach to `Re_eff ~ 5000` with real scatter.

So the two are deliberately co-located:
- `../metriplectic_vortex.py`  -> in-page reference model (laptop, instant)
- `./` (this folder)           -> full ensemble + NS reference + robustness

## How to run

See `README.md` in this folder (unchanged from the original package).
All scripts depend only on numpy / pandas / matplotlib (`requirements.txt`).

## Note on the old DOI

`DOI_and_Citation.txt` preserves the original standalone citation for
provenance only. The **live, canonical** version of this work is now the
Configured Continuum record (`10.5281/zenodo.17972568`); the site claim-strip
and PDF point there. The old Zenodo record (`17758705`), if it still exists,
should be marked as superseded-by / is-version-of the Configured Continuum
record (author action on Zenodo).
