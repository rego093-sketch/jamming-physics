# P5 -- MDR event-statistics universality, added v2.4

Tests the falsifiable content of the maximum-drag-reduction prediction on the REAL
Pillar IV dissipation-event sizes (pool96.npz from dissipation_avalanche.py).
The framework: drag reduction = suppression of rearrangement events; Virk's MDR =
the marginal bounding line; event statistics there are polymer-universal (the
marginal-stability avalanche exponent, set by the substrate, not the polymer).

Run:  python mdr_universality.py   # numpy only, seconds

Result: under cutoff suppression (framework's polymer model) the surviving-event
exponent stays tau ~ 1.37 +- 0.04 (universal); size-dependent thinning shifts it
(~ +a; the rejection scenario). The quantitative Virk asymptote (slope 11.7) is an
EXPLICIT GATE (needs viscoelastic FENE-P DNS). See whitepaper sec:mdr, app:mdr.
