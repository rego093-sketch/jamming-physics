# homeostasis_ionic — light review (2026-09-29)

## Summary
R2 ran `ri1_calcium()` and `ri2_acidbase()` from `repro/homeostasis_ionic/repro/_engine/vp_loops.py` with `python3 -B`.

The printed numbers match the pages:
- acid-base: pH 7.167 / 7.307 / 7.401 and slope 1.105;
- calcium: peak 2.1283, nadir −0.0435, final 1.0003.

The network fetchers (`fetch_gamma.py`, `comparative_gamma.py`) were not run.

The magnitude firewall is clean: dosing is [O] throughout, and TmP/GFR is quoted only as a reference range.

The §13 ATP1A1 honest negative is a good example of the reading rule already being followed.

## Findings
1. **Hub: "Node identity and order come from measured master-gene γ".** Severity: high.
   - This conflicts with AGENTS.md and dna §RB: order comes from regulatory-cascade depth, and building is [O].
2. **§3: Winters slope "1.10, matching ~1.2–1.5".** Severity: medium.
   - The slope is a code output of the chosen controller pCO₂* = 40·(HCO₃/24)^0.6.
   - 1.10 lies below the range the page itself quotes. The code accepts anything in 1.0–1.6.
   - The pH returns to 7.401 by construction, because HCO₃ and pCO₂ return to 24 and 40.
3. **§1: OU laws graded [V].**
   - Var·2k/σ² = 1, error·k = 1 and zero integral error are identities of the Ornstein–Uhlenbeck process. They are consistency checks.
   - "γ supplies k" (barrier γ²/4 → loop stiffness) is interpretation.
   - Severity: medium.
4. **§2: normalized calcium values depend on the chosen load and deficit.** Severity: low.
   - The deficit nadir is −0.043, a negative calcium, which is not physical.
   - Only the return to setpoint is a property of the loop.
5. **Measured γ values labelled "[V] measured input".** Severity: low.
   - They are fine as code outputs on measured sequence.

## What I changed (docs/homeostasis_ionic/ only)
- `index.html`:
  - added the Reading rule note after the h1;
  - added an interpretation / [O] bracket to the "identity and order" sentence, with a link to /dna/.
- `01-substrate-loop-gain-setpoint-stability/index.html`:
  - claim strip "[V] mechanism" → "code output + consistency; γ→k interpretation";
  - added brackets marking the OU laws as consistency and node emergence as interpretation.
- `02-calcium-setpoint-loop/index.html`: added a bracket on input dependence and the non-physical negative nadir.
- `03-acid-base-two-timescale-buffer/index.html`: added a bracket stating the slope's origin, that it falls below the cited range (Albert, Dell & Winters 1967), and that pH 7.401 holds by construction.
- No numbers or author text were removed.
