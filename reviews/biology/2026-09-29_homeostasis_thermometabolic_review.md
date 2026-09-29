# homeostasis_thermometabolic — light review (2026-09-29)

## Summary
Light two-reviewer review. R1 checked claims against data. R2 re-ran the engine functions with `python3 -B`, importing them directly so that `run_all.py`, which writes `reports/`, was not run.

Printed numbers match the pages exactly:
- sensitivity 0.053581 / 1.394014;
- loop width 1.3 with h_sp = 0.637588.

The magnitude firewall is clean: every restoration chapter withholds dose, efficacy and clinical magnitude.

The main problem is grading. The headline numbers are marked [V], but they come from chosen model parameters, not from data.

## Findings
1. **Endo 0.054 vs ecto 1.394 is a parameter artefact.** Severity: high.
   - Where: `repro/homeostasis_thermometabolic/repro/_engine/endotherm_ectotherm.py`, `setpoint_defense_sweep(g_endo=1.40, g_ecto=0.18, ambient_max=0.30)`.
   - The gains are chosen model values. The code docstring itself says "absolute loop-gains [O]".
   - Changing the inputs moves the outputs:
     | Change | Output |
     |---|---|
     | g_endo = 1.0 | 0.107 |
     | g_ecto = 0.30 | 1.246 |
     | drive = 0.20 | 0.033 / 1.309 |
   - The "~26×" ratio is therefore not a measurement.
   - 1.394 is a collapse fraction |s−s0|/2s0, and a value above 1 means the state overshot past the other well. The page describes it as tracking "almost one-to-one", which is not what the number means.
   - Pages: hub headline and `docs/.../endotherm-vs-ectotherm/`, both graded [V].
2. **Hysteresis width 1.3000 [V] is an identity plus a grid artefact.** Severity: medium.
   - Where: `vp_trm_engine.py`, `torpor_hysteresis_sweep`.
   - Any bistable cubic has a loop of width 2·h_sp. At g = 1.40 that is 1.275.
   - The printed value depends on the sweep grid: 1.32 / 1.30 / 1.29 / 1.28 at 121 / 241 / 481 / 961 points.
   - The page gives jumps at ±0.6500 in the text and ±0.6376 in the card.
   - No torpor observation was cited next to the claim.
3. **"16/16 stress targets" [V] are self-consistency checks of the model, not tests against data.** Severity: medium.
4. **The four γ nulls are sound code outputs on measured promoter reads.** Severity: low.
   - The code already grades the conclusion [O] because n is small.
   - The hub labelled them [V]; they are relabelled as code output.
5. **Observations are cited correctly** (UCP1/ADRB3 biology, BMR ratio ~5–10×, ~1–2 °C core stability). No issue.

## What I changed (docs/homeostasis_thermometabolic/ only)
- `index.html`:
  - added the Reading rule note after the h1;
  - claim strip changed from "[V] simulation-verified" to "code output (simulation)";
  - the four headline grades relabelled in place (code output / consistency / interpretation), with their input dependence and citations (Geiser 2004).
- `endotherm-vs-ectotherm/index.html`:
  - claim strip relabelled;
  - added a note on input dependence: the gain values, what the collapse fraction means, and the cited observation (Bennett & Ruben 1979).
- `torpor-switch/index.html`:
  - claim strip relabelled;
  - added a note on the identity and the grid dependence, citing Geiser 2004 and Heldmaier et al. 2004.
- No numeric result was changed and no author text was deleted.
