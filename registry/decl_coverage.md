# Shared-Core Dependency Coverage (VP-SPEC v1.9 _decl.json)

All **32 volumes** carry a gate-valid `_decl.json` (REQUIRED tier 32/32 PASS). Derived by
`tools/build_decls.py`: REQUIRED fields verbatim from the manifest; `owns_terms` from concept ownership;
`uses_terms`+`inherits_modules` from an auditable body card-scan (dna_interpretation also via the γ primitive).

## Module inheritance (which volumes build on each common module)

- **kernel** — 32/32: aging_senescence, analgesic_threshold, cardioresp, chemistry, circadian, circulatory, continental-genesis, cosmology, digestive, disease_kit, disease_wp, dna, ear, eye, fluid-dynamics, geochronology, geodynamics, homeostasis_hemodynamic, homeostasis_ionic, homeostasis_thermometabolic, immune_hematologic, inheritance, integumentary, mind, musculoskeletal, neuro, nose, physics, recent-sequence-cascade, reproductive_endocrine, sensory_organ, wave-computer
- **light emergence** — 4/32: chemistry, cosmology, neuro, physics
- **dna interpretation** — 24/32: aging_senescence, analgesic_threshold, cardioresp, circadian, circulatory, digestive, disease_kit, disease_wp, dna, ear, eye, homeostasis_hemodynamic, homeostasis_ionic, homeostasis_thermometabolic, immune_hematologic, inheritance, integumentary, mind, musculoskeletal, neuro, nose, recent-sequence-cascade, reproductive_endocrine, sensory_organ
- **rotor inflow** — 3/32: continental-genesis, cosmology, recent-sequence-cascade

## Per-volume declaration

| volume | tier | inherits_modules | owns | uses |
|---|---|---|---|---|
| aging_senescence | 7 | kernel, dna interpretation | 0 | 0 |
| analgesic_threshold | 8 | kernel, dna interpretation | 1 | 0 |
| cardioresp | 6 | kernel, dna interpretation | 0 | 4 |
| chemistry | 1 | kernel, light emergence | 2 | 1 |
| circadian | 7 | kernel, dna interpretation | 0 | 0 |
| circulatory | 6 | kernel, dna interpretation | 0 | 1 |
| continental-genesis | 1 | kernel, rotor inflow | 17 | 5 |
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
| recent-sequence-cascade | 1 | kernel, dna interpretation, rotor inflow | 9 | 10 |
| reproductive_endocrine | 6 | kernel, dna interpretation | 0 | 4 |
| sensory_organ | 5 | kernel, dna interpretation | 1 | 0 |
| wave-computer | 1 | kernel | 0 | 0 |
