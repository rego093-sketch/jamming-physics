# TREATMENT AXIS — Musculoskeletal (v0.6.0)

Every musculoskeletal disease this package owns now carries BOTH its root mechanism AND its treatment,
documented as a four-page canonical cluster (§21–§24) on a **DNA-grounded substrate**.

## This is a grounded, DNA-emerged simulation — not a toy model

The switches that diseases perturb and treatments restore are **not free parameters**. Each organ is emerged
from a single MEASURED gene parameter:

> **γ = the negative mean nearest-neighbour stacking free energy (−ΔG37, SantaLucia 1998) of the master
> gene's promoter, read directly from the human reference genome.**

For bone, RUNX2 gives **γ = 1.2414**, measured offline from assembly **NC_000006.12** (MANE NM_001024630.4,
promoter window TSS−2000..+500) by the identical DNA pipeline used across the VP body-physiology program.
The value is **read, not fitted**, and reproduces bit-for-bit on any machine. The entire disease + treatment
battery therefore sits on a switch the genome built — a disease perturbs it, a treatment restores it.

## The conceptual contribution: treatment is the mirror of disease on one kernel

A disease lowers an R19 escape barrier, shifts a setpoint past a spinodal, disables one branch of a remodelling
hysteresis loop, or caps a supply. **Its treatment performs the inverse operation** — raise the barrier, restore
the drive across the spinodal, re-enable the branch, refill the supply. The treatment code imports the disease
function verbatim and moves its single cited knob back toward health as a monotone **restoration sweep**
(intensity 0 → 1). PASS = the disease signature moves monotonically back toward the healthy attractor by
DIRECTION (No-Tuning). The real drug or load is the cited [L] anchor for WHICH knob it targets — never a tuned
efficacy number.

## Documentation (VP-SPEC v1.8, answer-first, AI-search / Google ready)
- **§21** `21-treatment-axis-barrier-restoration/` — methodology + DNA grounding ([V]).
- **§22** `22-treatment-bone-and-cartilage/` — osteoporosis, osteopetrosis, osteomalacia, osteolytic bone
  disease, stress fracture, achondroplasia, osteoarthritis ([V]).
- **§23** `23-treatment-muscle-and-neuromuscular/` — myasthenia gravis, Lambert-Eaton, channelopathies,
  muscular dystrophy, sarcopenia, tendinopathy ([V]).
- **§24** `24-treatment-honest-limits-and-scope/` — developmental dosage cliffs, cartilage regeneration,
  established-tumour therapy vs prevention, metabolic myopathy ([O] / scope).

Each page is answer-first (self-contained 40–60-word direct answer), carries a `ScholarlyArticle` + breadcrumb
JSON-LD with a **page-specific `knowsAbout` keyword set** (Google / AI-overview entity surface), keeps
paragraphs ≤3 sentences, and links each treatment back to its once-derived mechanism page (SSOT). All four pages
pass the VP-SPEC title (≤45 / ≤90), description (80–160), DOM (≤3000) and size (≤300 KB) limits.

## Where the axis lives (code)
- **Engine of the axis:** `repro/_disease/vp_msk_treatment.py` (mirrors every disease kernel; reuses
  `vp_msk_disease.py` verbatim — single source of truth).
- **Gate/docs reshaper:** `repro/_verify/stress_tests.py::run_treatment_suite()`.
- **Gate:** `repro/_verify/gates.py::research_gate()` requires `treatment_all_reversible_restore`.
- **Runner:** `repro/run_all.py` section `[3c]`.
- **Open items:** treatment-axis `[O]` negatives in `IRREPRODUCIBILITY_LEDGER.md` (each names its obstacle).

## Result
- **13 reversible (mirror) treatments restore** the healthy attractor by direction, each citing the real
  intervention (vosoritide, pyridostigmine, amifampridine, mexiletine, denosumab, vitamin D, HSCT, resistance
  training, eccentric loading, mechanical loading, bisphosphonates, …).
- **Honest negatives, graded [O] with a stated obstacle (results, not failures):** developmental dosage
  dysplasias (closed developmental window), cartilage regeneration (no resynthesis term; arthroplasty is
  hardware), established-tumour cytotoxic therapy (the kernel models INITIATION, not therapy response — PRIMARY
  PREVENTION is [V]), and general metabolic myopathy (only a cofactor-responsive subset reverses).

## Determinism
The treatment battery is a **separate module that reuses the disease kernels and never touches the engine**, so
the engine determinism hash is unchanged: **`7cf99d3baa263c8029224af9f197e2ce2e4c0b957a4b5d3729c6b5c71757a126`**
(2×sha256 identical). Research gate `all_green: True`; writing unlocked; the build reproduces `docs/`
byte-identically (idempotent).

Scope note: this is the *musculoskeletal* (mechanical-dynamics) volume of the broader VP body-physiology program
(see `VP_FRAMEWORK_MAP`). It owns acquired/multifactorial musculoskeletal diseases via the dynamics-key;
single-gene rare disease is `disease_wp`'s, and loop-dysregulation is the homeostasis volumes'.
