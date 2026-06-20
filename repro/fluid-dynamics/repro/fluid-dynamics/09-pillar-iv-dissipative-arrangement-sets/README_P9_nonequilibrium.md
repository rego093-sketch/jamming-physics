# P9 — non-equilibrium dissipation law (added v2.3)

Tests the dissipation *magnitude* law. In equilibrium C_eps = eps L/u'^3 is
constant (Taylor 0th law = the Pi_L event-RG fixed point). Out of equilibrium
Vassilicos's law gives C_eps ~ Re_lambda^{-1} — the framework's non-plateau RG
transient. A developed field is released into free decay and C_eps(Re_lambda) is
tracked.

Reproduce (fixed seeds, numpy only):
  # needs a developed state (state64.npz / state96.npz from the P4/ns3d driver)
  python decay.py 96 decay96.npz ce96.csv 220   # call repeatedly (checkpointed)
  python decay.py 64 decay64.npz ce64.csv 220   # wider Re_lambda span
  python analyze_ce.py                          # fit slope + detect plateau

Result: non-equilibrium C_eps ~ Re_lambda^{-1.01} (N=96, well-resolved) /
-1.14 (N=64), i.e. the Vassilicos -1, NOT the equilibrium constant; then the
slope flattens to ~-0.3 and C_eps -> plateau ~1.0 as the decay becomes
self-similar (the Pi_L fixed point). Module: nonequilibrium_dissipation.py
(see whitepaper Appendix app:nonequil, ledger row IV/C_eps).
