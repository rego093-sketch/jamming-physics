# R8 — NOTES AND HANDOVER (Disease Mechanisms volume → v0.10, phase R8)

Phase R8 raised the one axis R7 left open — **SEVERITY** — using an **open, citeable** source (the
HPO clinical-modifier *Severity* subtree), after an author directive corrected the R8 framing. Single
author (Young Jae Lee, ORCID 0009-0002-7535-8245). English deliverables, VP-SPEC v1.8 discipline
(no-tuning, bit-reproducible, honest grading `[O]<[H]<[L]<[V]`). All gates green; engine pin drift 0.

The R3/R4 BANKED files stay byte-identical (gate-verified); the registry layer (cumulative
**R5+R6+R7+R8**) is what advances. Registry-set sha **c40c6942872d** (2× identical); site-set sha
**4f614681a165** (2× identical).

## 1. The directive — OMIM removed (not deferred); open data used, flexibly AND honestly

The R7 closeout left two R8 paths: an OMIM API key, or human curation. The author corrected this:

- The **OMIM API key is PERMANENTLY unobtainable for an individual researcher** (no institutional
  registration). It is therefore **REMOVED as a path — not "deferred."** R8 sources no severity from
  OMIM, and the gate (`omim_path_removed_documented`) asserts the OMIM stage stays `SKIPPED`, the path
  is documented removed, and **no `S` value originates from OMIM**.
- But **reliable open data (NCBI-grade / HPO) should be usable** — "be flexible while honest"
  (융통성을 보이면서 정직하면 된다). R8 does exactly that: it lifts severity from the **open HPO Severity
  subtree** (the same pinned, programmatically-read dataset that already powers the onset/organ axes),
  through a disciplined, cited join — lifting only where an annotation honestly represents the disease,
  and recording per-disease why the rest cannot be used.

Neither of the handover's two paths is the mechanism R8 actually uses: the source is **open HPO**, not
OMIM and not a hand-fed file; the only curatorial element is the dominant-sequela judgment, and it is
bound to an **obligate, cited** open annotation that the gate re-verifies.

## 2. The handover correction (factual) — HP:0012824 exists

The R7 closeout recorded "HPO severity modifiers are feature-level" — true for the cohort at large, but
it under-stated the ontology. The HPO clinical-modifier **Severity** branch **HP:0012824 EXISTS** and
maps 1:1 to the BURDEN_INDEX S tiers, and it is already carried (per-feature) in the pinned
`phenotype.hpoa` (v2026-06-06, sha **1effb4e06afe**):

| HPO modifier | name | S tier |
|---|---|---|
| HP:0012825 | Mild | 0.25 |
| HP:0012826 | Moderate | 0.5 |
| HP:0012827 | Borderline | *(no tier — does not lift)* |
| HP:0012828 | Severe | 0.75 |
| HP:0012829 | Profound | 1.0 |

So severity **can** be wired from the same open source already in use — **where an annotation honestly
represents the whole disease**.

## 3. The open-source design — Severity subtree + cited dominant-sequela join + obligate criterion

Severity lifts **ONLY** through a cited **dominant-sequela curation join** over the open HPO Severity
subtree (`methodology/severity_hpo_join.csv`, sha **0b2fa7847cc5**; 1 row) — the exact discipline R7
used for the GBD disability join. A disease's `S` lifts **iff**, in the pinned hpoa, it carries a
Severity-modifier annotation that is:

1. **OBLIGATE** on the annotated feature — HPO frequency **100%** (`n/m` with `n==m`) or term HP:0040280
   — so the modifier reflects the **whole disease**, not a sub-phenotype;
2. on the disease's **cited dominant sequela** (`dominant_sequela_basis` recorded); and
3. for a **non-spectrum** (non-umbrella) entity.

Condition (1) is checked **programmatically against the open source at BUILD and GATE time**;
(2)–(3) are cited curatorial inputs recorded per row. This **a-priori inclusion criterion** is declared
in the registry (`severity_inclusion_criterion`) — the selection is **criterion-driven and
machine-auditable against open data, NOT a bare hand-pick, and NOT fitted** to any target order.

- Cut-points are a-priori (the HPO→tier map above), declared in the registry
  (`severity_modifier_cutpoints`), not chosen to fit.
- Each join row is re-validated against the pinned hpoa (phenotype + Severity modifier + frequency +
  reference) at build time or the **build exits nonzero**; the obligate criterion is asserted in-builder.
- **add-only**: a registry `[L]` supersedes a prior `[H]`/`[O]`; an existing `[L]` is corroborated (max).
  An absent/declined annotation **never downgrades** a value.

## 4. The disciplined 1-include / 6-exclude

All **7** annotation-bearing cohort diseases were reviewed. `methodology/severity_hpo_excluded.csv`
(sha **1f9b7e85c1f6**; 6 rows) records, per disease, why the others are **feature-level** and would be a
**category error** as a disease tier:

| disease | annotation considered | why declined |
|---|---|---|
| Osteogenesis imperfecta | Mild @ osteopenia (type I) | umbrella **spectrum** (types I–IV); a sub-type/feature modifier cannot tier it |
| Osteogenesis imperfecta | Severe @ osteoporosis (type III) | **opposite** modifier on the same umbrella — proves a sub-type severity ≠ disease tier |
| Classic homocystinuria | Mild @ tall stature | modifier on a **morphological** feature — severity-uninformative |
| Fabry disease | Mild @ airway obstruction | **non-dominant** feature (burden is renal/cardiac/cerebrovascular/pain) |
| Achondroplasia | Severe @ platyspondyly | one feature; disease is **mild-mod** overall (banked M=0.4) — would overstate |
| Duchenne MD | Mild @ intellectual disability | **non-dominant** (burden is progressive motor failure) — would catastrophically understate |

**INCLUDED — the unique disease meeting the criterion:** **Achondrogenesis type II**.
- Severe (HP:0012828) on its **defining** sequela **Short long bone** (HP:0003026), **OBLIGATE**
  (frequency **1/1**), cited **PMID:34573377** (curator HPO:probinson), under **OMIM:200610**.
- The disease is uniformly **perinatal-lethal** (non-spectrum), consistent with its banked **M=1.0 [L]**.
- `S` **0.75 [H] → 0.75 [L]** — the **value is unchanged** (0.75), only the **grade** is lifted, so
  `raw_burden` does not move.

## 5. Results (all gate-verified)

- **S-axis grade coverage** (over 35): `[L]` **2→3** · `[H]` **22→21** · `[O]` **11** (unchanged).
- The single grade lift **creates the 2nd order-locked disease**: **order_locked 1→2** =
  **Achondrogenesis type II** (O[L]/S[L]/M[L], every scored axis now registry-grade) + **Tyrosinemia
  type II** (unchanged). Six diseases were *one S-lift from a lock* but have no defensible open
  annotation and **stay [H]** (Hurler, factor VIII, Gaucher type I, Gaucher, beta-thalassemia, PKD2).
- **No promotions** (a grade lift on an already-scored axis moves no rankability); the placed/not-placed
  split and the residual **ORDER** are numerically identical to R7. **O/P/M/D are byte-identical to R7**
  (R8 touches only S).
- Sensitivity (Spearman vs equal default): equal 1.00 · onset 0.921 · mortality 0.990 · severity 0.924 ·
  disability 0.937 · drop-disability-core4 0.892.
- Digests: `burden_scores_registry.json` **8d3775ca14ac** / `.csv` **27050cda5674** ·
  `burden_residual_registry.json` **c362b29f0e66** · `treatments_registry.json` **8b3eb63b1496**
  (byte-identical to R5/R6/R7 — R8 does not touch the treatment layer).

## 6. Gate

`code/pipeline/r8_gate.py` (sha **6db8b1ff0a2d**) **PASS (16/16)**, report `reports/r8.gate.json`
(sha **e4400eddf765**). Re-derives every claim independently of any recorded digest and proves the
**r5→r6→r7→r8** chain deterministic (2× identical, registry-set sha **c40c6942872d**):

`determinism_chain_2x` · `banked_unchanged` (R3/R4 byte-identical) · `cumulative_over_r7` ·
`severity_join_anchored_cited` (join re-found in the pinned hpoa: phenotype+modifier+frequency+reference;
cited basis present; tier from a-priori cut-points; audit binds tier) · **`severity_annotation_obligate`**
(declared a-priori criterion present; every lifted feature OBLIGATE in the pinned source) ·
`severity_cutpoints_a_priori` · `severity_excluded_recorded` (6 declined, in cohort, reason present, S
not HPO-lifted) · `addonly_no_downgrade` (no grade weakened / no scored value dropped vs R7) ·
`s_lift_only_where_joined` (O/P/M/D identical to R7; S changed only for the joined disease) ·
**`new_order_lock_proven`** (Achondrogenesis II order_locked R7=False→R8=True; count 1→2) ·
`raw_burden_rederived` · `rankability_and_promotions` (0 new promotions) · `residual_correct` ·
`order_lock_rule_and_sensitivity` (2 locked) · `omim_path_removed_documented` (status SKIPPED; path
documented removed, key unobtainable; no S value sourced from OMIM) · `engine_pin_drift_zero`.

`r8_severity_registry.py` (sha **259ec1d65413**) and `r8_gate.py` are **living code** (post-date the R2
freeze), intentionally **NOT** in the frozen engine pin (verified `engine_pin_drift_zero`, 15/15).

## 7. W1.5 site sync

`tools/w1_build.py` (sha **301baffc09af**). The W1 prose, which still called severity "the one remaining
[L] lift / no open structured source," is brought into line with reality. **Numbers stay data-bound from
the curated CSVs; only narrative framing + the now-dynamic order_locked names/count were edited:**

- four registry passes now stated (R5/R6/R7/R8); per-disease pages credit the **HPO Severity subtree**
  where `S` is registry `[L]`; the **Achondrogenesis type II** page shows S `[L]` and carries the
  order-locked value note;
- the methodology / framework / hub / ledger state that the **rest of severity is feature-level in the
  open annotations** (a category error if read as a disease tier) and that the **OMIM path is REMOVED**
  (key unobtainable for an individual), **not deferred**; the order_locked note now names **both** locked
  diseases dynamically;
- `IRREPRODUCIBILITY_LEDGER.md` counts recompute from the registry (severity `[L]` 3, order_locked 2).

W1 gate `tools/w1_gate.py` **PASS (17/17)** with the R8 numbers; site-set sha **4f614681a165** (2×).
Retrieval surface unchanged in shape: sitemap 39 URLs (sha 8cd2d054f427) · `llms.txt` < 5 KB (4,988 B,
sha e9095fc45b53) · `_meta.json` (sha 783690f9eb60). (The registry `.json` gained the
`severity_inclusion_criterion` field, but the site reads the registry `.csv`, which is unchanged, so the
site is byte-identical to the pre-criterion R8 build.)

All prior gates still green: R1 5/5 · R2 7/7 · R3 9/9 · R4 11/11 · consolidation 10/10 · R6 14/14 ·
R7 16/16. Engine pin `MANIFEST_governed.sha256` verifies OK (drift 0, 15/15).

## 8. Honest bound + next phase

**Severity is only PARTIALLY liftable from open data, and is not over-claimed.** Exactly **one** cohort
disease has a defensible obligate dominant-sequela Severity annotation. The six diseases that sit one
S-lift from a lock carry **no** defensible open annotation and stay `[H]` — not guessed. The OMIM
clinical synopsis (the only disease-level alternative) is API-key-gated and the key is unobtainable for
an individual researcher: **removed, not deferred**.

### Next phase (R9 candidate) — the remaining severity/progression lift

The only discipline-compatible path left for the rest of severity (and most progression) is a
**deliberate, human-in-the-loop, per-disease curation from citeable published functional & survival
literature** — each entry a declared dominant-sequela mapping with an obligate/explicit basis and a
pinned citation, graded `[L]` (curation join), validated at build time exactly as R8's single row is.
There is **no open structured disease-level severity-magnitude tier** beyond the obligate HPO
annotations already consumed. Absent such curation, severity for the other 34 diseases stays `[H]`/`[O]`
with the precise obstacle named on every page and in the ledger — and the burden **ORDER** stays a
**provisional `[H]` prioritisation device** cohort-wide. The registry now carries **onset (R6),
disability + corroborated mortality (R7), and severity (R8)** at registry-grade `[L]`.

---

*Anchor facts (for a future session).* Achondrogenesis type II severity row = `OMIM:200610`,
`HP:0003026` "Short long bone", modifier `HP:0012828` Severe, frequency `1/1`, ref `PMID:34573377`,
curator `HPO:probinson`, in pinned `phenotype.hpoa` sha `1effb4e06afe`. Inclusion criterion = obligate
(freq 100% / HP:0040280) + cited dominant sequela + non-spectrum. Registry-set sha `c40c6942872d`;
site-set sha `4f614681a165`. R8 gate 16/16; W1 gate 17/17; all prior gates green; engine pin drift 0.
