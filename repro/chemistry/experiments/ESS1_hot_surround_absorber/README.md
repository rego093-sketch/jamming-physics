# ESS1: black-copper absorber with and without a hot rear surround

This tests the author's hypothesis: the black-copper test failed because the heat escaped, and inside a hot-sand ESS the absorber would keep absorbing. The design and predictions were registered first in `PREREG.json`.

| Prediction | Result |
|---|---|
| P1: a free-standing plate keeps no heat | PASS (kept 0%, peak 41–107 °C) |
| P2: with the rear against the hot store, the store keeps accumulating (+50 K by day 30) | **FAIL** (the store stalls at 26–42 °C) |
| P3: the hot rear surround keeps at least 10× more heat | PASS (plate 0 kWh vs store 2.3–8.6 kWh) |
| P4: the front face sets the limit | PASS |

**Why P2 failed.** The absorber's front face still looks at the sky at night, so it radiates the store's heat away. Front losses were 64–102 kWh over 30 days. The hot surround has to enclose the front face too, which leads to ESS2.

Run: `python3 ess1_run.py` (about 1 s, deterministic).
