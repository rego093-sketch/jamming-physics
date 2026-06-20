# CHARTER — Cardiorespiratory Emergence: Heart and Lung as Coupled Relaxation Oscillators under Reflex Control

**paper_id:** `cardioresp_vp_site`  ·  **code:** `car`  ·  **branch:** jamming (autonomic oscillator + control-loop)  ·  **version:** 0.1.0-research

## Scope (one line)
Heart (SA node) and lung (preBotzinger) emerge as the SAME FHN relaxation oscillator; their reflex closed loops (baroreflex, chemoreflex) and their coupling (RSA, Cheyne-Stokes) are the targets.

## What this package emerges and circulates
Like the mind package, this package **emerges its organs by simulation and circulates their dynamics**
— but at the level of physical MECHANISM, not felt experience. Organ *identity* and *developmental
order* are owned by the DNA morphogenesis gene-clock and are CITED here (grade [V], measured γ, never
fitted); this package adds the functional DYNAMICS.

### Organs
- **heart** (`NKX2-5`, γ-emerged identity from DNA [V]) — SA-node pacemaker + conduction + contraction — *dyn class:* oscillator — *rate anchor:* resting_hr 1.17 Hz [L]; intrinsic 1.67 Hz [L]
- **lung** (`NKX2-1`, γ-emerged identity from DNA [V]) — preBotzinger inspiratory rhythm + ventilatory pump — *dyn class:* oscillator — *rate anchor:* eupnea ~0.2-0.3 Hz [L] TO-ANCHOR

## Physical-class boundary (why these organs are one package)
The decomposition is by **physical regime / coupling topology**, not textbook organ-system labels.
This package is the **jamming (autonomic oscillator + control-loop)** class. Anything outside that class belongs to a sibling package
and is reached only through the cited seam variables below — never re-emerged here (SSOT).

### Seams IN (inherited / cited)
- DNA: organ identity (NKX2-5, NKX2-1) + emergence order [V]
- substrate: FHN Neuron + R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- arterial PaO2/PaCO2 -> circulatory_vp_site (this pkg is SSOT)
- cardiac output (stroke vol x HR) -> circulatory_vp_site (pump boundary condition)
- SA-node rate anchor -> mind M18 (felt/afferent arm cites this pkg)

## Discriminant targets (must pass before writing)
- T1 eupnea period: preBotC FHN intrinsic period matches cited 12-18 breaths/min [V], rate [L]
- T2 apnea threshold: chemoreflex loop-gain > 1 -> periodic breathing onset (instability bifurcation) [V]
- T3 RSA: HF-HRV spectral peak locks to the respiratory frequency when CPGs are ephaptically coupled [V]
- T4 Cheyne-Stokes: CSR period ~= 2 x circulatory delay (the forced number -> vp-card on the written page) [V]
- T5 baroreflex: a BP step is corrected by an HR change with cited gain/latency; setpoint = resting_hr [L]

## Oncology scope (carcinogen → incidence)
External-stimulus (carcinogen) exposure mechanism: how much MORE cancer occurs with exposure. Shared
R19 kernel (barrier-lowering → Kramers crossing → RR(dose)); per-site cited epidemiological anchors.
Grades: anchor [L] / dose-response shape [V] / absolute incidence [O] (state obstacle).
- **lung carcinoma** ← tobacco smoke condensate; radon progeny; PM2.5/diesel
  - anchor/grade: RR vs pack-years (Doll & Peto class) [L]; near-linear no-threshold shape [V]
- **(heart: sarcoma rare)** ← n/a primary; baseline incidence only
  - anchor/grade: background crossing rate only; not a dose-response target

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase and the C1/C3 discipline in
  the research phase. Constitution (C0) overrides any clause on conflict.
- **Research-first:** writing (`tools/build_docs.py`) is locked until the stress battery is green and
  research is signed off. See START_HERE.md §5.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable:** return exactly one zip; do not fragment (C0).
