# CHARTER — Aging and Senescence: the Systemic Decline of Homeostatic Setpoints over the Lifespan

**paper_id:** `aging_senescence_vp_site`  ·  **code:** `age`  ·  **branch:** integrative capstone (the temporal decline axis)  ·  **version:** 0.1.0-research
**DOI:** 10.5281/zenodo.20756155 (Zenodo concept DOI, published; resolves at https://doi.org/10.5281/zenodo.20756155).

## Scope (one line)
The capstone temporal layer: aging is the slow drift and loss of gain of EVERY homeostatic setpoint, plus the accumulation of cells stuck in pathological R19 attractors (senescence). It is the dominant RISK MULTIPLIER for the oncology/pathology kernels across the whole framework. Sarcopenia, frailty, and multimorbidity are the disease axis.

## What this package emerges and circulates
Primary objects are LOOPS / OSCILLATORS / sense-organ instruments — node identity + order are owned by
DNA (measured γ, never fitted); nodes whose γ is not yet in the atlas are honest **to-measure** inputs.
It re-emerges NO organs owned elsewhere; it cites the seams below (SSOT) and adds its own dynamics.

### Nodes
- **cellular_senescence** (`TP53`) — γ **to-measure** (named master `TP53`; fetch via DNA pipeline, never fitted) — cells stuck in a pathological R19 attractor (irreversible arrest + SASP) — *dyn:* stuck-attractor — *anchor:* senescent-cell accumulation rate [L]; TP53 gamma TO-MEASURE
- **senescence_arrest_switch** (`CDKN2A`) — γ **to-measure** (named master `CDKN2A`; fetch via DNA pipeline, never fitted) — the p16INK4a senescence arrest program (the switch) — *dyn:* stuck-attractor — *anchor:* p16 accumulation with age [L]; CDKN2A gamma TO-MEASURE
- **longevity_signaling** (`FOXO3`) — γ **to-measure** (named master `FOXO3`; fetch via DNA pipeline, never fitted) — the insulin/IGF-mTOR-FOXO longevity axis (loop-gain maintenance) — *dyn:* maintenance — *anchor:* longevity-pathway tone [L]; FOXO3 gamma TO-MEASURE
- **telomere_maintenance** (`TERT`) — γ **to-measure** (named master `TERT`; fetch via DNA pipeline, never fitted) — telomere attrition -> the replicative limit (reservoir clock) — *dyn:* reservoir-depletion — *anchor:* telomere shortening rate [L]; TERT gamma TO-MEASURE
- **homeostatic_setpoint_drift** (`(systemic_setpoint_drift)`) — no single master gene (circuit/derived/diffuse) — the slow drift of ALL imported setpoints (cross-package) — *dyn:* integrative-decline — *anchor:* multi-setpoint drift; imports siblings

### Seams IN (inherited / cited)
- ALL packages: every defended setpoint this layer watches decline (cited)
- immune: immunosenescence raises oncology crossing (seam)
- DNA: the gene-clock life_course baseline (cited)
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- aging RISK MULTIPLIER -> every oncology + pathology kernel (cross-cutting time axis; raises crossing rates)

## Research program (excavated)

The CAPSTONE temporal layer. Aging is not an organ; it is the slow drift and loss of gain of EVERY
homeostatic setpoint built in the other packages, plus the accumulation of cells stuck in pathological
R19 attractors (senescence). It is the dominant RISK MULTIPLIER for the oncology/pathology kernels across
the whole framework. This package imports the other packages' setpoints and models their decline.

- **RA1** Setpoint drift: each defended setpoint (glucose, pressure, Ca, temperature) loses defense gain
  with time, so the defended value drifts -- the unifying signature of aging across systems. *Discriminant:*
  a monotone gain decline reproduces the multi-system drift. [V].
- **RA2** Cellular senescence as a STUCK attractor: a cell crosses into an irreversible arrested R19 basin
  (cannot return; SASP). *Discriminant:* accumulation of stuck-attractor cells over time; irreversibility. [V].
- **RA3** Reservoir / stem depletion: the DWELL ~ gamma^1.5 reservoir is finite; stem-cell exhaustion =
  reservoir depletion (telomere/TERT attrition as the clock). *Discriminant:* depletion rate vs cited. [V]/[O].
- **RA4** Hallmarks mapping: map the hallmarks of aging (genomic instability, proteostasis loss, cellular
  senescence, stem exhaustion, dysregulated nutrient sensing) to substrate phenomena (R19 switch errors,
  stuck attractors, depletion, loop-gain loss). *Discriminant:* each hallmark -> a substrate mechanism. [V]/[O].
- **RA5** Risk multiplier: aging raises the crossing rate of EVERY oncology + pathology kernel (accumulated
  barrier-crossings + immunosenescence, seam to immune). *Discriminant:* the steep age-incidence slope of
  cancer emerges from accumulated crossings. [V], absolute [O].
- **RA6** Rate of aging: is there ONE rate parameter (biological vs chronological age) or per-system rates?
  *Discriminant:* do systems age at a shared rate or independently? [V]/[O].
- Grades (C3): drift/accumulation mechanism [V]; cited rates [L]; absolute lifespans/incidence [O].

## Major diseases (non-rare) — covered here; rare/monogenic → disease_wp
Disease is modeled as a failure of a defended setpoint / clock / sense organ on the SAME R19 substrate.
The MAJOR (common, polygenic, acquired, age-related) diseases of this system are covered here; RARE and
monogenic forms are owned by disease_wp and only cross-referenced (entered here as a cited parameter).
Grades: anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle).
- **sarcopenia** ← age-related muscle decline (cross-ref musculoskeletal) -> loss of actuator capacity
  - anchor/grade: decline rate vs cited age [L]; cross-loop [V]
- **frailty / multimorbidity** ← co-decline of multiple setpoints crossing a function threshold
  - anchor/grade: multi-setpoint co-failure [V]; cited [L]
- **aging as the cancer risk multiplier** ← accumulated R19 barrier-crossings + immunosenescence raise ALL-site incidence
  - anchor/grade: the steep age-incidence curve vs cited [L]; crossing accumulation [V]; absolute [O]
- **(progeroid syndromes -> disease_wp)** ← monogenic accelerated aging is rare/genetic
  - anchor/grade: cross-ref disease_wp; here only as a rate parameter

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase + C1/C3 in research. C0 overrides on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and research signed off.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **DOI:** 10.5281/zenodo.20756155 (Zenodo concept DOI, published; resolves at https://doi.org/10.5281/zenodo.20756155).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state passes by files only.
