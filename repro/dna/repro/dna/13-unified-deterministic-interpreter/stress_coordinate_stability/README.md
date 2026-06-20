# stress_coordinate_stability — are A4 anchors robust or window artifacts? (T3.1+T3.4)

**Verifies:** whether shell/anchor positions are real sequence properties or artifacts of the
LOCK window parameters / arbitrary region edge. **Method:** per frozen §11 region, re-run `run_key`
at neighboring LOCK settings (W, step, smooth_radius, min_shell_bp) and after cropping the region
start; measure interior-anchor recall + precision at 500/1000/2000 bp tolerance. PROBE only — locked
params are never changed in the grammar. Pipeline imported single-source + sha256-pinned, no RNG.
**Expected output:** `stress_coordinate_stability_results.json` (deterministic, 2× sha256 identical).

**Finding:** positions ROBUST (85% recur within 2 kb under neighbor settings/crops); min_shell_bp is a
RESOLUTION knob (10 kb keeps a nested subset at baseline positions, precision 0.88, not relocation);
anchor positions carry ~kb uncertainty. Coordinate read graded as a robust multi-scale skeleton with a
resolution-set anchor count — not exact per-bp coordinates.
