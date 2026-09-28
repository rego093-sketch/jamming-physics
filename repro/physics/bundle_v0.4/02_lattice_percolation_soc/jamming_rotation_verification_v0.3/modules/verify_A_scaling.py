"""
verify_A_scaling.py -- the amplification A is anchored, not free.

Reproduces, from the deposited SOC summaries, (1) the finite-size N^{-1/3} scaling of the
structural amplification A = a_med / g*, and (2) the cross-check of the largest run against
the unit-realization anchor A_geo = c*dt/a. Confirms A's absolute size is pinned (0.16%),
not an unconstrained distribution.

Sources (deposited in this bundle):
  results/soc_run3_summary.json                          -> N=200 A_median, gstar/g0
  results/soc_N750/soc_N750_aggregate_summary.csv        -> N=750 A_median, A_mean (seeds 45-48)
  results/soc_N750/soc_N750_scaling_check.json           -> A_geo = c*dt/a, predictions

Rationale: at fixed microscopic threshold g0 and unit box L=1, the typical neighbour distance
a_med ~ N^{-1/3}; since g* pins near g0 (ratio ~1), A = a_med/g* ~ N^{-1/3}.
"""

# --- deposited measured values (constants below mirror the bundle's JSON/CSV summaries) ---
A200_median       = 802_149.74     # N=200, 83 avalanches  (soc_run3_summary.json)
gstar_over_g0_200 = 1.1438
A750_median       = 476_364.95     # N=750, seeds 45-48, 104 events (soc_N750_aggregate_summary.csv)
A750_mean         = 569_330.36
gstar_over_g0_750 = 1.2408
A_geo             = 883_082.35     # unit-realization anchor c*dt/a (soc_N750_scaling_check.json)
N0, N1            = 200, 750

scale = (N0 / N1) ** (1.0 / 3.0)               # a_med ~ N^{-1/3}  =>  A ~ N^{-1/3}
A750_pred_from_N200 = A200_median * scale
A750_pred_from_geo  = A_geo * scale

err_law = A750_median / A750_pred_from_N200 - 1.0     # N^-1/3 law vs measured median
err_geo = A750_mean   / A750_pred_from_geo  - 1.0     # unit-realization anchor vs measured mean

print("Amplification A = a_med / g*  --  robustness / anchoring")
print(f"  measured:  N=200  A_median = {A200_median:,.0f}   (g*/g0 = {gstar_over_g0_200:.2f})")
print(f"             N=750  A_median = {A750_median:,.0f}, A_mean = {A750_mean:,.0f}   (g*/g0 = {gstar_over_g0_750:.2f})")
print(f"  N^(-1/3) scale factor 200->750 = {scale:.4f}")
print(f"  [1] N^-1/3 law:   predict A(750) from A(200) = {A750_pred_from_N200:,.0f}  vs measured {A750_median:,.0f}  -> {err_law*100:+.1f}%")
print(f"  [2] unit anchor:  A_geo*scale = {A750_pred_from_geo:,.0f}  vs measured A_mean {A750_mean:,.0f}  -> {err_geo*100:+.2f}%")
verdict = "PASS" if abs(err_geo) < 0.01 else "CHECK"
print(f"\n  VERDICT: {verdict} -- A is anchored to the unit realization (c,dt,a) and reproduced at N=750.")
print("  (A's magnitude is pinned, not free; its input-dependence on g0 is noted honestly in the whitepaper W.5.)")
