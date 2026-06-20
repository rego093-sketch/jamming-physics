# P4 — dissipation-event size law (added v2.2)

Tests the prediction that the dissipation events of developed 3D turbulence are
marginal-stability avalanches: thresholded dissipation structures follow
P(s) ~ s^{-tau} with the pre-registered Lin-Wyart band tau in [1.4,1.5], not an
exponential.

Reproduce (fixed seeds, numpy+scipy only):
  python dev64.py 220        # develop N=64 (call until DEVELOPED, ~2 calls)
  python analyze64.py 8      # N=64 snapshots + threshold-scan fit
  python embed96.py 220      # spectral-embed N=64 -> N=96, relax (~2 calls)
  python analyze.py 96 state96.npz pool96.npz 11   # N=96 fit (accumulate)
  python consolidate_p4.py   # resolution trend -> final numbers

Result: tau = 1.60 (N=64) -> 1.46 (N=96), into [1.4,1.5]; d_f ~ 2.0-2.2;
power law (R^2 ~ 0.97-0.99), exponential rejected. Captured outputs:
avalanche_N64.out.txt, avalanche_N96.out.txt, p4_consolidated.out.txt.
Module: dissipation_avalanche.py (see whitepaper Appendix, ledger row IV/size law).
