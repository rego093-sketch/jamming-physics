# 09-pillar-iv-dissipative-arrangement-sets
Verifies: Pillar IV: budget+Onsager saturation ->0.998I; flux on events exact in 1D, stable 2D, converged 3D (corr~0.80, N<=128).
Section: §9 — Pillar IV --- Dissipative: arrangement sets dissipation (whitepaper v2.1, concept DOI 10.5281/zenodo.17972568)

## Reproduction map
- `metriplectic_vortex.py` (+ `.out.txt`) — in-page lightweight reference model:
  mean-field budget closure + `eps_tot -> I = 0.21` saturation plateau.
  Laptop-instant; the support-localization step is left as an open GATE item.
- `metriplectic-onsager/` — full ensemble evidence backing the same claim
  (folded in from the former standalone "Onsager anomaly" package; see
  `metriplectic-onsager/PROVENANCE.md`). Contains the offline ADG ensemble,
  Navier–Stokes viscous reference at 64^2/256^2/512^2, and N-/seed-/r_c
  robustness scans. Ensemble `eps_tot_mean ~ 0.205–0.216` matches the
  in-page plateau and extends reach to `Re_eff ~ 5000`.
  Quick run:  `cd metriplectic-onsager && python -m src.parameter_sweep && python -m src.plot_dissipation_saturation`
