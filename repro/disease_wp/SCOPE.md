# SCOPE — inclusion / exclusion boundary

This whitepaper covers **systemic-body genetic and rare diseases**. The brain, nervous system, heart, and
affect/emotion are owned by the **sibling neuro/mind whitepapers** and are *not* re-covered here. A crisp
boundary is stated below so future sessions do not have to re-decide it.

## IN scope (primary-system axis)

A disease entity is **in scope** when its *primary* classification falls in one of:

- **Metabolic** — inborn errors of metabolism (amino-acid, organic-acid, fatty-acid-oxidation, carbohydrate,
  urea-cycle, mitochondrial-metabolic disorders by their systemic manifestation).
- **Lysosomal / peroxisomal storage** — *systemic* (visceral, skeletal, hematologic) manifestations.
- **Connective tissue & skeletal** — collagenopathies, fibrillinopathies, skeletal dysplasias, osteogenesis imperfecta.
- **Hematologic** — hemoglobinopathies, coagulation disorders, bone-marrow-failure syndromes.
- **Immunologic** — primary immunodeficiencies, autoinflammatory syndromes.
- **Renal / hepatic / gastrointestinal / pulmonary / exocrine** — e.g., polycystic kidney disease, cystic fibrosis.
- **Endocrine / growth** — monogenic endocrine and growth disorders (systemic, not hypothalamic-behavioral).
- **Dermatologic** — genodermatoses.
- **Chromosomal & CNV syndromes** — for their *systemic* features (the boundary rule below governs CNS/cardiac features).

## OUT of scope (owned by neuro/mind)

- Primary **neurological / neurodegenerative** disorders (e.g., Huntington disease, hereditary
  ataxias/neuropathies, leukodystrophies as primarily-CNS entities).
- Primary **psychiatric / affect / emotion** disorders.
- Primary **cardiac** disorders (channelopathies, cardiomyopathies as primary-heart entities).
- Anything whose defining feature is brain, nerve, heart, or mood.

## Boundary rule for **multi-system** diseases (the part that prevents confusion)

Many genetic syndromes touch several organs, including the excluded ones. Apply this rule:

1. **Classify by the *primary/defining* system.** If primary ∈ IN-scope list → the entity is **included**.
2. For an included multi-system entity, the whitepaper covers the **molecular mechanism** and the
   **in-scope organ involvement** in full. The **CNS / cardiac / affective** components are **cross-referenced**
   to the neuro/mind whitepapers — *named and linked, not re-described in detail, and not duplicated*.
3. If the primary/defining system is brain, nerve, heart, or mood → the entity is **excluded** here (it belongs
   to the sibling), even if it has systemic features. Record it in `disease_index.csv` with `in_scope=false`
   and the reason — do **not** silently drop it (so the exclusion is auditable, per the "name it, don't hide it" discipline).

### Worked examples (illustrative; the real enumeration is Phase R1 from NCBI)

| entity | primary system | decision | handling |
|---|---|---|---|
| Cystic fibrosis (CFTR) | exocrine / pulmonary / GI | **IN** | full mechanism + systemic organs |
| Sickle cell disease (HBB) | hematologic | **IN** | full |
| Marfan syndrome (FBN1) | connective tissue (skeletal/ocular) | **IN** | full; **aortic/cardiovascular feature cross-referenced** to neuro/mind-cardiac, not duplicated |
| Duchenne muscular dystrophy (DMD) | skeletal muscle | **IN** | full; **cardiomyopathy cross-referenced**, not duplicated |
| Gaucher disease (GBA) | lysosomal / visceral | **IN** | systemic full; neuronopathic subtype's CNS axis cross-referenced |
| Huntington disease (HTT) | brain (neurodegenerative) | **OUT** | logged `in_scope=false`, reason "primary CNS → neuro" |
| Long-QT syndrome (KCNQ1 …) | heart (channelopathy) | **OUT** | logged, reason "primary cardiac → neuro/mind-cardiac" |

## Sibling body-system packages — etiologic-class ownership boundary

The neuro/mind boundary above (brain/nerve/heart/affect) is one of **two** sibling boundaries. The second is
against the **13 body-system packages** of the VP body framework (the 7 machine-dynamics packages, 3 integrated
homeostasis packages, 2 time/cross-cut layers, 1 special-sensory package — see the bundled
`VP_FRAMEWORK_MAP.md`, the cross-package master map carried in this package for exactly this reason). This
boundary exists to **prevent redundant research**: this volume and those packages must not both work up the
same disease.

**The dividing axis is etiologic class, not body region.** This volume *and* the body-system packages each
touch every region of the body (both touch the kidney, both touch the bone). Dividing by region collides.
Divide by **what scientific machine explains the disease**:

| owner | etiologic class | explanatory machine |
|---|---|---|
| **this volume (`disease`)** | **monogenic / rare / genetic** (gene-keyed) | gene → molecular mechanism → primary-system class + reproducible burden order |
| **machine-dynamics + sensory packages** | **acquired / multifactorial / common** (dynamics-keyed) | carcinogen → R19-barrier lowering → Kramers crossing; or setpoint dynamics failure |
| **integrated homeostasis / time packages** | **loop dysregulation** (no single organ) | failure to close a defended setpoint loop at a sibling seam (attractor-shift) |

**Binding rule (BOUNDARY-1).** This volume owns the disease iff its *primary etiology* is a **monogenic
lesion** and the entity is **rare/genetic**. A disease whose primary etiology is **acquired, multifactorial,
or a dynamics/setpoint failure** is **OUT of this volume** — it belongs to the relevant body-system package.
Record it in `disease_index.csv` with `in_scope=false` and the reason (`acquired/common → body-system
package`), and cross-reference; **do not** re-derive its dynamics here. (Same "name it, don't hide it"
discipline already applied to the neuro/mind exclusion.)

**Tie-break for the overlap zone (the part that prevents collisions):**

1. **Monogenic-defining and rare** → this volume. (The definition *is* the gene key.)
2. **Common acquired disease that has a monogenic subset** (familial HCM, MODY, familial
   hypercholesterolemia, hereditary RCC/VHL, BRCA breast cancer, Lynch colorectal cancer) → the
   **body-system package owns the common disease + its dynamics**; this volume owns the **monogenic subtype as
   a named entity** and *exports the gene-lesion parameter*. Cross-reference both ways; neither re-covers the
   other's layer.
3. **Carcinogen-driven cancer** (lung, melanoma, SCC, … — acquired *by construction*, carcinogen lowering the
   R19 barrier) → **body-system package**, never this volume. **Hereditary cancer syndromes** (Li-Fraumeni,
   VHL, Lynch, hereditary retinoblastoma, hereditary breast-ovarian) → **this volume**, with the body-system
   package cross-referencing.

**Synthesis seam (BOUNDARY-2).** Where this volume owns a monogenic lesion that a body-system package needs as
a parameter (e.g. MODY = a GCK setpoint parameter), this volume is the **SSOT of the gene-lesion fact** and
*exports* it by gene key; the body-system package is the **SSOT of the systemic-dynamics consequence** and
imports it. This volume does **not** compute systemic-loop trajectories — that is the body-system package's
layer. They compose by contract, never by merge. (The live wiring is an unbuilt cross-package harness item;
the contract is declared here so neither side duplicates the other.)

This boundary is checked for *wiring* (presence + the rules above carried in this file and the map) by
`tools/boundary_gate.py`. That gate verifies the boundary is **declared and embedded**, not that any specific
disease was classified correctly — semantic scope compliance remains the author's call at index time, under
BOUNDARY-1.

## Medical-safety scope

This is a **research whitepaper**, not clinical guidance. It describes mechanisms, population-level facts, and
established treatment *mechanisms*; it does **not** give dosing, individualized medical advice, or
diagnosis. Treatment sections describe *how a modality works*, not *what a given patient should take*.
