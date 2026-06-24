# Shared-Core Dependency Coverage (VP-SPEC v1.9 _decl.json)

All **31 volumes** carry a gate-valid `_decl.json` (REQUIRED tier 31/31 PASS). Derived by
`tools/build_decls.py`: REQUIRED fields verbatim from the manifest; `owns_terms` from concept ownership;
`uses_terms`+`inherits_modules` from an auditable body card-scan (dna_interpretation also via the γ primitive).

## Module inheritance (which volumes build on each common module)

- **kernel** — 31/31: aging_senescence, analgesic_threshold, cardioresp, chemistry, circadian, circulatory, continental-genesis-cascade, cosmology, digestive, disease_kit, disease_wp, dna, ear, eye, fluid-dynamics, geochronology, geodynamics, homeostasis_hemodynamic, homeostasis_ionic, homeostasis_thermometabolic, immune_hematologic, inheritance, integumentary, mind, musculoskeletal, neuro, nose, physics, reproductive_endocrine, sensory_organ, wave-computer
- **light emergence** — 4/31: chemistry, cosmology, neuro, physics
- **dna interpretation** — 24/31: aging_senescence, analgesic_threshold, cardioresp, circadian, circulatory, continental-genesis-cascade, digestive, disease_kit, disease_wp, dna, ear, eye, homeostasis_hemodynamic, homeostasis_ionic, homeostasis_thermometabolic, immune_hematologic, inheritance, integumentary, mind, musculoskeletal, neuro, nose, reproductive_endocrine, sensory_organ
- **rotor inflow** — 2/31: continental-genesis-cascade, cosmology

## Per-volume declaration

| volume | tier | inherits_modules | owns | uses |
|---|---|---|---|---|
| aging_senescence | 7 | kernel, dna interpretation | 0 | 0 |
| analgesic_threshold | 8 | kernel, dna interpretation | 1 | 0 |
| cardioresp | 6 | kernel, dna interpretation | 0 | 4 |
| chemistry | 1 | kernel, light emergence | 2 | 1 |
| circadian | 7 | kernel, dna interpretation | 0 | 0 |
| circulatory | 6 | kernel, dna interpretation | 0 | 1 |
| continental-genesis-cascade | 1 | kernel, dna interpretation, rotor inflow | 26 | 13 |
| cosmology | 1 | kernel, light emergence, rotor inflow | 5 | 2 |
| digestive | 6 | kernel, dna interpretation | 0 | 5 |
| disease_kit | 8 | kernel, dna interpretation | 0 | 0 |
| disease_wp | 8 | kernel, dna interpretation | 0 | 1 |
| dna | 2 | kernel, dna interpretation | 10 | 1 |
| ear | 5 | kernel, dna interpretation | 0 | 0 |
| eye | 5 | kernel, dna interpretation | 0 | 0 |
| fluid-dynamics | 1 | kernel | 0 | 1 |
| geochronology | 1 | kernel | 0 | 0 |
| geodynamics | 1 | kernel | 0 | 0 |
| homeostasis_hemodynamic | 7 | kernel, dna interpretation | 0 | 4 |
| homeostasis_ionic | 7 | kernel, dna interpretation | 0 | 3 |
| homeostasis_thermometabolic | 7 | kernel, dna interpretation | 0 | 0 |
| immune_hematologic | 6 | kernel, dna interpretation | 0 | 3 |
| inheritance | 3 | kernel, dna interpretation | 0 | 0 |
| integumentary | 6 | kernel, dna interpretation | 0 | 0 |
| mind | 4 | kernel, dna interpretation | 1 | 5 |
| musculoskeletal | 6 | kernel, dna interpretation | 0 | 3 |
| neuro | 4 | kernel, light emergence, dna interpretation | 3 | 5 |
| nose | 5 | kernel, dna interpretation | 0 | 3 |
| physics | 1 | kernel, light emergence | 18 | 0 |
| reproductive_endocrine | 6 | kernel, dna interpretation | 0 | 4 |
| sensory_organ | 5 | kernel, dna interpretation | 1 | 0 |
| wave-computer | 1 | kernel | 0 | 0 |
