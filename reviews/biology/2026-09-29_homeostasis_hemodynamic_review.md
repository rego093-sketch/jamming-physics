# homeostasis_hemodynamic — light review (2026-09-29)

## Summary
R2 ran three pieces of code with `python3 -B`:
- `_therapy/fundamental_targets.py`;
- `map_from_seams()`;
- `rp2_baroreflex()`.

The printed numbers match the pages: MAP 93.0, reset 93→113, transient 15, durable 0 / 17, residual 5 mmHg (75 %), HF margin +0.180 / −0.139.

The main problems:
- Most of the headline mmHg numbers are either arithmetic on the inputs or equal to chosen inputs.
- Therapy effect sizes are shown as model results, which breaches the spirit of the magnitude firewall.

## Findings
1. **Therapy magnitudes echo their inputs (firewall).** Severity: high.
   - In `_therapy/fundamental_targets.py`, `hypertension_therapies(reset_up=20, op_drug=15, ref_reset=17)`, the "durable −17 mmHg" is exactly the input `ref_reset`. With ref_reset = 10 or 25 the output is 10 or 25.
   - Several chapters present it as a reproduced durable drop [V]: §6, §9, §13, and the hub via §14. It reads as an intervention effect size.
   - CAL6 in §12 reports "model RDN within 15 % of cited −20 mmHg". That compares a chosen input with the citation, so it is not an independent cross-check.
   - The +20 reset shift and the transient 15 are likewise inputs, returned exactly by the integral controller.
2. **MAP = 93 mmHg "error 0" [V]: consistency, not a test.** Severity: medium.
   - In `_engine/vp_hmd_loops.py`, SVR_REST_PRU = 17.8 = (93−4)/5, so closure holds by construction.
   - The inputs are cited resting values (CO 5 L/min, CVP 4 mmHg). No observation ranges were shown on the page.
3. **Loop results that hold by construction.** Severity: medium.
   - The baroreflex 75 % / 5 mmHg is 1/(1+G) with the anchored G = 3.
   - "Perfect adaptation, spread 0" is the defining property of an integral controller.
   - CAL5's ≈135 mmHg is 115 + 20.
   - All are consistency checks that were labelled [V].
4. **Node identity and order.** Severity: medium.
   - The hub says node identity is "fixed by" master-gene γ, and kidney "developmental order (DNA)" is inherited.
   - AGENTS.md and dna §RB say identity comes from the atlas, γ sets the switch threshold, and building (including order) is [O].
5. **Comfort proposal and prioritisation graded [F] forced.** Severity: low.
   - §17 and §18 are biological hypotheses and rankings. They are interpretation.
6. **Magnitude firewall otherwise clean.** Severity: none.
   - There is no dose, regimen or route.
   - The cited trial signs (PROMISE, PARADIGM-HF) and the RDN −20 mmHg are observations.

## What I changed (docs/homeostasis_hemodynamic/ only)
- `index.html`:
  - added the Reading rule note after the h1;
  - TOC grade labels: "[V] sim-reproduced" → "code output"; §1 → "consistency (arithmetic)"; §17 and §18 "[F] forced" → "interpretation";
  - added a note in the lede on how the γ identity should be read.
- `hmd-overview/index.html`:
  - added "[consistency: arithmetic on cited inputs]" after "forced [V]";
  - added a note with the observed ranges (Guyton & Hall), the SVR = (93−4)/5 construction, and the identity/order clarification.
- `hmd-hypertension-reset/`, `hmd-fundamental-therapy/`, `hmd-comfort-logic/`: added a firewall note stating that 20 / 15 / 17 are chosen inputs and not clinical effect sizes, with the RDN observation and Guyton 1991.
- `hmd-absolute-calibration/index.html`: added a note that CAL6 is circular and that CAL1, CAL2 and CAL5 are consistency or arithmetic.
- No numbers or author text were removed. The per-page `[V]` badges in the sub-pages are left for the author and are covered by the hub rule.

## Needs author
Whether to keep the −17 mmHg figure on these pages at all, given the magnitude firewall.
