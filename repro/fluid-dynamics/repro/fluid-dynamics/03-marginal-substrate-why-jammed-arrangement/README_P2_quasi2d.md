# P2 -- quasi-2D transition roughness ((2+1)D DP), added v2.4

Extends transition_dp.py to a 2D lattice (4 neighbours => (2+1)D directed
percolation). Same G-SOC rules (theta=0.45, q=0.35); only the dimension changes.
Locate lambda_c by the survival transition, then measure the turbulent-fraction
box roughness M2(r)-1 ~ r^{-2 beta/nu_perp} in the critical quasi-stationary state.

Run:  python transition_dp_2d.py   # numpy only, ~2 min, fixed seeds

Result: 2 beta/nu_perp = 1.475 +- 0.058 (L=384, 6 realisations) vs (2+1)D DP 1.591;
quasi-1D (prior) 0.482; 2D/1D ratio 3.06 vs DP 3.16 (both ~5-7% low: finite size).
See whitepaper sec:transition and appendix app:trans2d.
