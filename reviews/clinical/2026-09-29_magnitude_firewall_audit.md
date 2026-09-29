# Magnitude-firewall audit (2026-09-29)

**Scope.** All 1,597 pages were scanned for magnitude-bearing tokens that appear near a therapy-context word. Five classes were searched:

- doses: mg, µg, IU, g/day, mg/kg
- concentrations: mM, µM, nM, mmol/L, mg/dL, ng/mL
- regimens: once or twice daily, b.i.d., q#h
- titration and target phrases
- effect sizes: "reduce … by N%"

**Clinical volumes.** In disease_kit, disease_wp and analgesic_threshold (about 950 pages) there are **0 hits** for doses, concentrations, regimens or targets. The only percentages there are corpus statistics, such as the share of diseases by corrective direction.

**Corpus-wide.** There were 29 hits in all, and none is a prescribed magnitude:

- **Physiological reference values, about 15.** Examples: glucose 5 mM; ionized Ca 1.2 mM; Na 140 and K 4.2 mM.
- **Simulated physiological variables, 6.** Example: the glucose nadir after an insulin challenge.
- **Optics and physics units, 5.** These were false positives.
- **Borderline, 3 pages, now annotated:**
  - digestive §8 (processed-meat exposure–risk curve). The shape is [V]. The IARC anchor is [L], and one slope is calibrated to it. RR values extrapolated from the curve are not clinical estimates.
  - sensory_organ §11 and §12. The named myopia interventions and the "≥50% slowing" figure are literature citations [L], not framework outputs. No dose or schedule is given.

**Gate.** The magnitude-firewall pattern in `tools/gate.py` (section H) now also covers concentrations, regimens and titration targets. It still returns PASS.
