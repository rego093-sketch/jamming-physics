# CONSTITUTION_disease — project rules (subordinate to VP-SPEC v1.8 §0)

VP-SPEC v1.8 Chapter 0 is supreme. Where this file and VP-SPEC conflict, **VP-SPEC §0 wins**. The clauses below
*add* disease-domain rules; they do not override the standard. No-tuning, add-only, and bit-for-bit
reproducibility carry over unchanged.

**C-D1 — Observed vs reproduced.** Clinical/epidemiologic facts from NCBI are **observed inputs**: respected and
cited, never asserted as "reproduced." The package's reproducible layer is the *analysis* (classification, burden
index, baseline annotation). These two are tracked in separate columns (`DATA_PROVENANCE.md`).

**C-D2 — Every entity is fully tagged.** Each disease carries inheritance class + mechanism class + organ system +
burden score + treatment status, each with provenance and a grade. Untagged entities do not enter `data/curated/`.

**C-D3 — Treatment honesty.** A treatment *mechanism* is stated only when mechanistically established in the
literature. Experimental/uncertain mechanisms are graded `[O]`/`[H]` with the obstacle named (VP-SPEC C3).
**Incurable diseases become open-problem sections** — mechanistic reasoning about candidate approaches is allowed
and welcome, but it is graded `[O]`/`[H]`, and **no cure is fabricated or implied as established.**

**C-D4 — Medical safety.** This is a research whitepaper, not clinical guidance. No dosing, no individualized
medical advice, no diagnosis. Treatment text explains *how a modality works*, not *what a patient should take*.
Where relevant, sections note that clinical decisions belong to qualified clinicians.

**C-D5 — Language.** Whitepaper and all committed artifacts in **English only** (VP-SPEC constitution). Reporting
to the author in chat is in **Korean, plain terms**.

**C-D6 — Scope.** Per `SCOPE.md`: systemic-body genetic/rare diseases; brain/nerve/heart/affect deferred to the
neuro/mind whitepapers; multi-system entities handled by the boundary rule (classify by primary system,
cross-reference excluded organs, never silently drop). The **second** sibling boundary — against the 13
body-system packages (acquired/common/loop-dysregulation disease) — is governed by **C-D10** and
`VP_FRAMEWORK_MAP.md`.

**C-D7 — Phasing.** Phases R1–R4 are investigation only (data + notes, no whitepaper prose). VP-SPEC's full
authoring discipline switches on at Phase W1, after the consolidation gate (`ROADMAP.md`).

**C-D8 — Drift discipline.** The carried emergence engine (`code/emergence_v2/`) is governed by
`MANIFEST_governed.sha256`. It is a read-only baseline here: this project does not edit pinned engine files.
Any session touching the package re-verifies the pin (drift 0) before handoff.

**C-D9 — Reporting tone.** Reports are written confidently and precisely. Excessive self-deprecation is avoided —
it adds no information and constrains the next session's reasoning. Honest uncertainty about the *science*
(grades, named obstacles) is required and is distinct from self-deprecation.

**C-D10 — Sibling-package boundary (anti-redundancy, binding).** Per `SCOPE.md` → *Sibling body-system packages*
and the bundled cross-package master map `VP_FRAMEWORK_MAP.md` (carried in this package): this volume owns
**monogenic/rare/genetic** disease (gene-keyed). Disease whose primary etiology is **acquired, multifactorial,
or a dynamics/setpoint failure** — including carcinogen-driven cancers — is **owned by the body-system
packages**, not re-derived here (record `in_scope=false`, reason `acquired/common → body-system package`,
cross-reference). Where a monogenic lesion is needed by a body-system package, this volume **exports the
gene-lesion parameter** (SSOT of the gene fact) and does **not** compute the systemic-loop trajectory (the
body-system package's layer). The boundary's *wiring* (its declaration + embedding) is gate-checked by
`tools/boundary_gate.py`; *semantic* classification of any specific disease stays the author's call at index
time. This clause prevents redundant research across the body framework; it does not override VP-SPEC §0.
