# §13 stress test — is `contact_competent` real signal or chance?

> Verifies whether the anchor-relative helical `contact_competent` flag carries an element-level
> signal, or is geometry at chance. **Verify:** `python3 stress_helical.py` → prints the per-organism
> table + pooled verdict and writes `stress_helical_results.json`.

For each of the 12 cross-kingdom (§11) frozen 120 kb regions: build the A4 anchors, take the real
TSS motors from the region-relative feature table, and compute the same-helical-face rate of each
motor → nearest anchor (RISE 3.4 Å, TWIST 34.29°/bp). Compare to a permutation null (random motor
positions, 2000×, seed 19) and the analytic chance of 0.34.

**Expected output (frozen):** pooled over 246 motor–anchor pairs (10 organisms; maize/human skipped,
<3 motors) the observed same-face rate is **0.337 vs chance 0.340, z = −0.09 → AT CHANCE**. The bare
contact flag is deterministic Layer-1 geometry, not a biological phasing signal. The real helical
signal is the *global* WW ~10.5 bp nucleosome propensity (descriptive); realized functional contact
is Layer-2. Inputs frozen in `inputs_ft/` with `_provenance.json` (accession, region, sha256).
