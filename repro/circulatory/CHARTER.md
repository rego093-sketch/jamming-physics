# CHARTER — Circulatory Transport and Clearance: Hemodynamics, Renal Filtration, and Hepatic Clearance from the Jamming Substrate

**paper_id:** `circulatory_vp_site`  ·  **code:** `cir`  ·  **branch:** jamming (pressure-flow + clearance)  ·  **version:** 0.1.0

## Scope (one line)
Vasculature (Windkessel pressure-flow), kidney (glomerular filtration + osmoregulation loop) and liver (hepatic clearance) emerge as a transport+clearance network driven by the cardiac pump boundary condition.

## What this package emerges and circulates
Like the mind package, this package **emerges its organs by simulation and circulates their dynamics**
— but at the level of physical MECHANISM, not felt experience. Organ *identity* and *developmental
order* are owned by the DNA morphogenesis gene-clock and are CITED here (grade [V], measured γ, never
fitted); this package adds the functional DYNAMICS.

### Organs
- **kidney** (`SIX2`, γ-emerged identity from DNA [V]) — metanephric nephron: filtration + tubular transport + osmoregulation — *dyn class:* control-loop — *rate anchor:* GFR ~120 mL/min [L] TO-ANCHOR; RAAS/ADH loop
- **liver** (`HHEX`, γ-emerged identity from DNA [V]) — hepatic blood flow + first-pass clearance/metabolism — *dyn class:* clearance — *rate anchor:* hepatic extraction ratio [L] TO-ANCHOR
- **vessels** (`(vasculature)`, γ-emerged identity from DNA [V]) — pressure-driven flow network (no single master gene; mesodermal/diffuse) — *dyn class:* transport — *rate anchor:* MAP = CO x SVR; Windkessel C,R

## Physical-class boundary (why these organs are one package)
The decomposition is by **physical regime / coupling topology**, not textbook organ-system labels.
This package is the **jamming (pressure-flow + clearance)** class. Anything outside that class belongs to a sibling package
and is reached only through the cited seam variables below — never re-emerged here (SSOT).

### Seams IN (inherited / cited)
- cardioresp: cardiac output + arterial PaO2/PaCO2 (boundary conditions, cited)
- DNA: organ identity (SIX2, HHEX) + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- renal clearance of solutes -> shared interstitial milieu
- hepatic clearance kinetics -> digestive_vp_site (first-pass seam)

### Cross-volume gene-key references (CONSUMED, not re-emerged — single source: `inherited/cross_references.json`)
Monogenic gene-key entities that touch the flow+clearance organs but are OWNED by `disease_wp` (MASTER MAP 6.1).
circulatory records identity + cited magnitude + seam only; the cell-fate barrier-height derivation stays with the owner.
- **VHL** (3p25-26) -> hereditary clear-cell RCC. Seam: trichloroethylene (acquired RCC carcinogen, §22) acts via the
  same VHL/HIF pathway whose germline loss defines hereditary RCC. Grade [V] identity+seam.
- **HFE** (6p22.2, p.C282Y) -> hereditary haemochromatosis -> HCC. Seam: iron-overload cirrhosis is a chronic drive on
  the same liver R19 axis carrying the acquired HCC carcinogens (§23). Anchor: Atkins JAMA 2020, HR 10.5. Grade [V].

### CKD ownership (DECIDED, v0.5.0)
Chronic kidney disease is **not** circulatory-owned. It is the downstream final-common-pathway readout of sibling
etiologies — diabetic/hypertensive nephropathy (homeostasis siblings) and intrinsic age-related nephron loss
(`aging_senescence`). §15 (T13) is retained **only** as a demonstration of the renal autoregulation relation
(total GFR = surviving-nephron fraction × the autoregulated per-nephron value), not as a circulatory-owned disease.

## Discriminant targets (must pass before writing)
- T1 MAP: mean arterial pressure = CO x SVR reproduces cited resting ~93 mmHg from the pump BC [V], abs [O]
- T2 Windkessel: diastolic pressure decay time constant = R x C matches cited aortic value [V]
- T3 GFR autoregulation: tubuloglomerular feedback holds GFR flat across a BP range (plateau) [V]
- T4 osmoregulation: an osmotic load is corrected by the ADH loop to setpoint ~285 mOsm/kg [L] [V]
- T5 hepatic clearance: first-pass extraction ratio sets oral bioavailability for a cited tracer [V]

## Oncology scope (carcinogen → incidence)
External-stimulus (carcinogen) exposure mechanism: how much MORE cancer occurs with exposure. Shared
R19 kernel (barrier-lowering → Kramers crossing → RR(dose)); per-site cited epidemiological anchors.
Grades: anchor [L] / dose-response shape [V] / absolute incidence [O] (state obstacle).
- **renal cell carcinoma** ← tobacco smoke; trichloroethylene; aristolochic acid
  - anchor/grade: RR vs exposure (smoking, TCE cohorts) [L]; shape [V]
- **hepatocellular carcinoma** ← aflatoxin B1; chronic HBV/HCV; ethanol
  - anchor/grade: aflatoxin x HBV multiplicative synergy RR [L]; barrier-lowering synergy [V]

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase and the C1/C3 discipline in
  the research phase. Constitution (C0) overrides any clause on conflict.
- **Research-first:** writing (`tools/build_docs.py`) is locked until the stress battery is green and
  research is signed off. See START_HERE.md §5.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable:** return exactly one zip; do not fragment (C0).
