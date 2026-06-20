# FUTURE_WORK — Disease Mechanisms volume (disease_wp)

This forward plan is carried **inside the whitepaper package** and is mirrored in the published
whitepaper itself (site §1 *Forward plan and completion criteria*,
`/disease/01-classification-burden-treatment-framework/#forward`). It is updated in **every version**
and is replaced only by a dated **completion declaration** (see §C). It supersedes the forward section
of `ROADMAP.md`.

Discipline (non-negotiable, VP-SPEC v1.8): every pass either lifts a burden axis to registry grade
through a **cited, gate-enforced** rule, or records — per disease — the **precise obstacle** that
prevents it. No value is ever guessed to advance the plan. No cut-point is ever widened to obtain a
lift. Every lift is gated; every decline is recorded with its reason.

---

## Sibling-package boundary (governance, embedded v0.13.1)

To prevent **redundant research** across the VP body framework, the ownership boundary between this volume
and the **13 body-system packages** is now embedded in the package and gate-checked. Divided by **etiologic
class, not body region**: this volume owns **monogenic/rare/genetic** disease (gene-keyed); the body-system
packages own **acquired/common/multifactorial/loop-dysregulation** disease (dynamics-keyed), including
carcinogen-driven cancers. A disease whose primary etiology is acquired/dynamics is **OUT** here (recorded
`in_scope=false`, reason `acquired/common → body-system package`, cross-reference only — never re-derived).
Where a monogenic lesion is needed by a body-system package, this volume **exports the gene-lesion parameter**
and does not compute the systemic-loop trajectory. Canonical: `SCOPE.md` → *Sibling body-system packages*
(BOUNDARY-1/BOUNDARY-2), constitution **C-D10**, the carried master map `VP_FRAMEWORK_MAP.md`; wiring guard
`tools/boundary_gate.py` (PASS 6/6). This is the second sibling boundary (the first, neuro/mind, is unchanged).

---

## Status — what has landed (v0.17, phase R15)

Cumulative registry layer **R5 + R6 + R7 + R8 + R9 + R10 + R11 + R12 + R13 + R14 + R15** (the R3/R4 BANKED files stay byte-identical):

- **R5** — treatments accession-dated to GeneReviews Management → `[L]` (33/35; 2 honestly `[H]`, no
  disease-directed therapy).
- **R6** — onset → registry `[L]` (28/35, Orphanet/Orphadata AverageAgeOfOnset) + 1 mortality.
- **R7** — disability → registry `[L]` (13/35, GBD 2013 disability-weights table) + 2 mortality axes
  corroborated from PMC survival literature.
- **R8** — severity → registry `[L]` (1 disease) via the open **HPO Severity subtree (HP:0012824)**
  cited dominant-sequela join → 2nd `order_locked`.
- **R9** — progression → registry `[L]` via **curated PMC open-access** dominant-sequela literature,
  **tier DERIVED by the frozen R3 tier function** over the verbatim cited sentence (no new cut-points):
  Niemann-Pick disease type A → tier 1.0 (**3rd `order_locked`**); Duchenne MD corroborated to `[L]`
  but deliberately **not** locked (its severity was honestly declined at R8). Five considered statements
  declined and recorded.
- **R10** — progression round 2, same rule, same **frozen R3 tier function**, shipped as a **dedicated
  cumulative stage over R9** (`code/pipeline/r10_severity_litcurate.py`, R9 artifacts left byte-identical):
  **two grade-only corroborations** — Fabry disease and Marfan syndrome, each progression `[H]` → `[L]`
  with the **value unchanged** — and **neither locks** (Fabry keeps S/M `[H]`; Marfan keeps S `[H]`), so
  **no new `order_locked`** and **no new placement**. **Three declines recorded** (Hb SS disease
  progression + severity, Alpha-1-antitrypsin deficiency progression): each OA sentence was found and
  verbatim-pinned but is **umbrella/genotype-scoped or spectrum**, so no disease-level tier is defensibly
  isolable — HbSS and AATD stay **not-placed**, now with these as **permanent open-data-irreducible
  obstacles** (§C(b)).
- **R11** — severity round 3, same rule, same **frozen R3 tier function**, shipped as a **dedicated
  cumulative stage over R10** (`code/pipeline/r11_severity_litcurate.py`, R9 + R10 artifacts left
  byte-identical): **one VALUE+GRADE severity lift** — Marfan syndrome severity `[H]` → `[L]` (0.50 → 0.75,
  tier **derived** by the frozen R3 function via 'life-threatening' from the disease-defining sentence) —
  and because Marfan's onset, progression and mortality were **already** registry-`[L]`, this single lift
  makes Marfan **`order_locked`** (the **4th**). **Two declines recorded** (Gaucher disease type I severity,
  Gaucher disease umbrella severity): each OA sentence was found and verbatim-pinned but is **comparative**
  (GD1 = least-severe-of-three / "devastating" attributed to GD3), so no clean disease-level severity tier
  is defensibly isolable — both Gaucher severities stay `[H]`, not lifted.
- **R12** — severity round 4, same rule, same **frozen R3 tier function**, shipped as a **dedicated
  cumulative stage over R11** (`code/pipeline/r12_severity_litcurate.py`, R9 + R10 + R11 artifacts left
  byte-identical): **two severity lifts** — Duchenne muscular dystrophy severity `[H]` → `[L]` (0.50 → 0.75,
  **VALUE+GRADE**, tier **derived** by the frozen R3 function via 'severe' from the disease-defining
  sentence) and Tyrosinemia type I severity `[H]` → `[L]` (0.75 → 0.75, **grade-only**). Because Duchenne
  MD's onset, progression, mortality **and** disability were **already** registry-`[L]`, the DMD severity
  lift makes Duchenne MD **`order_locked`** (the **5th**, and the only cohort disease with all **five**
  axes scored and every one registry-`[L]`); HT-1's grade-only lift does **not** lock (onset + mortality
  stay `[H]`). **Two declines recorded** (Hurler syndrome severity = comparative phenotype-class label
  "the severe phenotype" vs the attenuated MPS I forms; Beta-thalassemia severity = umbrella spectrum with
  'severe' attached to the major form), and **Hemophilia A**'s only retrievable 'severe' framing is a
  factor-activity **sub-phenotype** ("severe hemophilia A (FVIII < 1%)"), recorded as a **frontier
  observation** rather than forced into a decline.
- **R13** — severity/progression round 5, same rule, same **frozen R3 tier function**, shipped as a
  **dedicated cumulative stage over R12** (`code/pipeline/r13_severity_litcurate.py`, R9 + R10 + R11 + R12
  artifacts left byte-identical): **three lifts** — Maple syrup urine disease severity `[H]` → `[L]`
  (0.50 → 0.75, **VALUE+GRADE**, via 'life-threatening'), Cystic fibrosis and Glycogen storage disease
  type II / Pompe progression `[H]` → `[L]` (**grade-only**). **None locks** (MSUD retains onset `[H]`;
  CF and Pompe retain mortality `[H]`). **Two declines recorded** (Osteogenesis imperfecta = comparative
  Sillence phenotype-class; alpha-Thalassemia = umbrella spectrum), with Hemophilia B (factor-activity
  sub-phenotype) and Becker MD (dystrophinopathy-class-only 'severe') recorded as **frontier observations**.
- **R14** — severity/progression round 6, same rule, same **frozen R3 tier function**, shipped as a
  **dedicated cumulative stage over R13** (`code/pipeline/r14_severity_litcurate.py`, R9 + R10 + R11 + R12 +
  R13 artifacts left byte-identical): **three lifts** — Classic homocystinuria and Fabry disease severity
  `[H]` → `[L]` (0.50 → 0.75, **VALUE+GRADE**, via 'life-threatening' / 'severe'), and Becker muscular
  dystrophy progression `[H]` → `[L]` (**grade-only**, via 'progressive' — advancing the R13 BMD frontier
  on a *different* axis from a clean BMD-specific sentence). **None locks** (Classic homocystinuria retains
  mortality + disability `[H]`; Fabry retains mortality `[H]`; Becker retains severity `[H]`), taking
  severity coverage to **9/35** and progression to **12/35**. **Two declines recorded** (Polycystic kidney
  disease 2 = PKD1-vs-PKD2 comparative; Osteogenesis imperfecta progression = moderate-to-mild umbrella
  spectrum).
- **R15** — severity round 7, same rule, same **frozen R3 tier function**, shipped as a **dedicated
  cumulative stage over R14** (`code/pipeline/r15_severity_litcurate.py`, R9 + R10 + R11 + R12 + R13 + R14
  artifacts left byte-identical): **three severity lifts**, all to tier 0.75 via 'severe' — Acute
  intermittent porphyria 0.50 → 0.75 (**VALUE+GRADE**; only 2 scored axes, sub-rankable, **no lock**),
  Achondroplasia `[O]` → 0.75 (**previously-unscored axis**; becomes rankable but retains mortality `[H]`,
  **no lock**), and Phenylketonuria `[O]` → 0.75 (**previously-unscored axis**). Because PKU's onset
  O 1.0 `[L]` and disability D 0.50 `[L]` were **already** `[L]`, scoring severity `[L]` makes its three
  scored axes all `[L]` and **completes its order-lock (5 → 6) — disclosed as a CONSEQUENCE, not
  engineered** (S and D are orthogonal axes from different sources; the cited sentence passes every
  inclusion criterion independently; suppressing a defensible lift to avoid the lock would itself be
  tuning). Severity coverage rises to **12/35**; progression unchanged at **12/35**. **Two declines
  recorded** (21-Hydroxylase-Deficient CAH = form-specific severest-form salt-wasting; Hemochromatosis
  type 1 = high-vs-low-TSAT comparative) plus a Wilson disease frontier observation.
- **§4 deliverable** — read-only **unmet-need / treatment-gap surface**
  (`data/curated/unmet_need_surface.*`): residual = `raw_burden·(1−e)`, framed as a research-
  prioritisation signal, never clinical advice. Honest headline (burden `[L]` + no disease-directed
  therapy) = Achondrogenesis type II + Niemann-Pick type A.

**order_locked 6/35** (Achondrogenesis type II, Niemann-Pick type A, Tyrosinemia type II, Marfan
syndrome, **Duchenne muscular dystrophy**, **Phenylketonuria**) — Duchenne MD added by R12's single
VALUE+GRADE severity lift (the only cohort disease with all five axes scored and every one registry-`[L]`),
and **Phenylketonuria added by R15** as a disclosed consequence (its onset + disability were already `[L]`,
so the round-7 severity lift completed the all-`[L]` ≥3-axis pattern). The burden **order** remains a
provisional `[H]` prioritisation device cohort-wide.

Gates green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 · R7 16/16 ·
R8 16/16 · R9 15/15 · R10 16/16 · R11 16/16 · R12 16/16 · R13 16/16 · R14 16/16 · **R15 16/16** · **unmet-need 6/6** · **W1 site 17/17** ·
boundary 6/6. Engine pin drift 0. Registry-set sha **efe81b447194**; unmet-need surface sha **a3c6c16fdeeb**
(recomputed — R15 raises Achondroplasia's and Phenylketonuria's raw_burden, so the residual surface
moves and Achondroplasia enters the placed residual order; the headline rule is unaffected); W1 site-set sha **c5559c704a75**.

---

## A. THE NEXT TASK — R16: remaining severity / progression (and mortality) lift

R9–R15 have taken the curated-PMC-OA frontier through the **clearly defensible** disease-level joins
reached so far (3 progression lifts with NPD-A locking; Fabry/Marfan progression grade-only; the Marfan
**severity** lift completing its order-lock at R11; the Duchenne MD **severity** lift completing its
order-lock at R12 + HT-1 grade-only severity; MSUD severity + CF/Pompe progression at R13; Classic
homocystinuria/Fabry severity + Becker MD progression at R14 — none of those completing a new lock; AIP +
Achondroplasia + PKU severity at R15, of which **PKU completes its order-lock as a disclosed consequence**
since its onset + disability were already `[L]`). **17 placed diseases still carry at
least one `[H]` axis** — overwhelmingly **severity** — so the frontier remains wide. The next pass
continues the **same rule** on the placed cohort's remaining `[H]`/`[O]` **severity** and **progression**
axes (and any further **mortality** axis), lifting **only** where a cited PMC open-access source gives a
defensible disease-level magnitude:

1. a cited PMC **open-access** source states a **disease-level** magnitude for the disease's **dominant
   untreated sequela** — *not* a sub-phenotype, *not* a treated-cohort figure, *not* spectrum/continuum
   ("ranges from mild to severe") language, *not* a comparative reference to other forms;
2. the **frozen R3 tier function** (`first_match` over `PATTERNS["S_severity"]` / `["P_progression"]`)
   applied to the **verbatim** cited sentence yields the declared tier (the tier is **derived**, never
   hand-asserted);
3. the sentence is re-found **verbatim** in the pinned OA cache at build and gate time, and the R3
   **spectrum override** does not trip.

**Mortality** lifts only where a quantitative disease-typical **survival figure** exists (free text does
not fill an open mortality axis — over-trigger risk), consistent with R7.

Mechanics (the **established pattern**, as R7 was a separate stage over R6, R10 over R9, R11 over R10,
R12 over R11, R13 over R12, R14 over R13, and R15 over R14): implement the pass as a **new dedicated cumulative stage**
`code/pipeline/r16_*.py` over the
R15 registry — **do not mutate** any prior stage's CSVs or recorded shas — with its own curated join /
excluded CSVs (`severity_litcurate8_*`), its own fetch+pin step, and its own `r16_gate.py` that re-proves
determinism, add-only-no-downgrade vs R15, source-binding, and prior-artifact preservation (all
R9–R15 CSVs byte-identical). The **OMIM clinical-synopsis path stays REMOVED** (key unobtainable for
an individual researcher), not deferred.

Note the frontier is **obstacle-bound** for two entities: **Hb SS disease** (progression + severity) and
**Alpha-1-antitrypsin deficiency** (progression) have only umbrella/genotype-scoped or spectrum OA
statements available and are recorded as permanent §C(b) obstacles — **not** re-litigated unless an
entity-specific disease-level OA magnitude becomes retrievable. The two **Gaucher** severities (type I,
umbrella) were considered at R11 and declined as **comparative** (recorded in
`severity_litcurate3_excluded.csv`); the **Hurler syndrome** severity (comparative phenotype-class label)
and the **Beta-thalassemia** severity (umbrella spectrum) were considered at R12 and declined (recorded in
`severity_litcurate4_excluded.csv`); the **Osteogenesis imperfecta** severity (comparative Sillence
phenotype-class, declined at R13) and again its **progression** (moderate-to-mild umbrella spectrum,
declined at R14), the **alpha-Thalassemia** severity (umbrella spectrum, R13), and the **Polycystic
kidney disease 2** severity (PKD1-vs-PKD2 comparative, R14) are likewise recorded in their
`severity_litcurate{5,6}_excluded.csv` and re-litigable only on a clean disease-level OA magnitude. Each
is re-litigable only if a clean disease-level (non-comparative,
non-spectrum) OA severity magnitude for the entity's own dominant sequela becomes retrievable. **Hemophilia
A** (and, from R13, **Hemophilia B**) remain noted frontiers: the only retrievable 'severe' framing is the
factor-activity sub-phenotype ("severe hemophilia A (FVIII < 1%)"), so severity is liftable only if a
disease-level (not factor-stratum) OA
magnitude becomes retrievable. **Becker muscular dystrophy** — an R13 *severity* frontier (the only 'severe'
framing jointly grouped Duchenne+Becker) — had its **progression** lifted at R14 from a clean BMD-specific
'progressive' sentence; its severity remains the open frontier. **New at R15:** the **21-Hydroxylase-Deficient
CAH** severity was declined as **form_specific** (the 'life-threatening' magnitude attaches to the severest
classic salt-wasting form, not the whole entity) and the **Hemochromatosis type 1** severity as **comparative**
(high-vs-low-TSAT between-stratum contrast; its retrievable disease-level framings are now exhausted) — both
in `severity_litcurate7_excluded.csv`; and **Wilson disease** severity is a recorded **frontier observation**
(only sub-symptom 'severe' framings retrievable, not yet a recorded decline). Near-term, this curated-OA path remains the only `[L]`-lift route open from
open data; it is the route to any further `order_locked` diseases and not-placed → placed promotions, and
ultimately toward the §C completion criterion.

## B. Standing deliverables to keep in sync each pass

- The **published whitepaper** must always carry this forward plan (site §1 `#forward`), updated to the
  current pass, until §C.
- `VERSION` (new versioned entry), `IRREPRODUCIBILITY_LEDGER.md` (recomputed counts + each open
  obstacle), `ROADMAP.md` one-line status, and a `reports/R<n>_NOTES_AND_HANDOVER.md`.
- The unmet-need surface and the W1 site re-derive from the registry; re-run their builds + gates so the
  whole package stays bit-reproducible and offline-verifiable.

## C. COMPLETION DECLARATION — the criterion

This volume will be declared **complete** when, for **every placed disease**, either:

- **(a)** all scored axes are registry grade `[L]`/`[V]` (the disease is `order_locked` and its burden
  *value* is registry-locked); **or**
- **(b)** every remaining open axis carries a **permanent, named obstacle that is irreducible from open
  data** (a magnitude that exists only behind an unobtainable licensed source).

At that point the burden order is either **fully registry-locked** or **provably as locked as open data
allows**; the residual `[H]` openness is itemised in `IRREPRODUCIBILITY_LEDGER.md` with each obstacle;
and a **dated completion declaration** is written into `VERSION`, the whitepaper §1 (replacing this
forward plan), and a final `reports/COMPLETION_DECLARATION.md`. Only then does the forward-plan
discipline end.
