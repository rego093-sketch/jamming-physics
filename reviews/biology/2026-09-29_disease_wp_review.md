# disease_wp — light two-reviewer review (2026-09-29)

Scope: the hub, §1 (the framework), 35 disease pages and 2 mechanism-class pages in `docs/disease_wp/`, and the pipeline in `repro/disease_wp/`.

Sampled pages: §1, 02 achondrogenesis II, 07 DMD, 17 PKU, 18 CF, 37, 38.

## R1 — claims against data, and the magnitude firewall
- **Firewall is clean.** There is no dose, concentration, regimen or effect size. Treatments are named as observed standard of care from GeneReviews and accession-dated sources.
- **Grade vocabulary is mostly honest.** It is [L] registry / [H] inference / [O] open. Most clinical inputs are correctly labelled [L] (observation), and inferences are labelled [H].
- **[V] on clinical claims.** The legend defines [V] as "law / proof, or quantitative published distribution". Pages then say axes are "[L]/[V]". A published distribution is an observation, so it should read [L].
- **[F] on the mechanism-class pages (37, 38).** Grouping diseases by mechanism is a classification based on observation. It is not forced.
- **Efficacy offset e.** The pages use values 0.85 / 0.55 / 0.30 / 0.10 / 0.00. These are declared a-priori bins for evidence status. They are not measured clinical effect sizes. However, the residual score built from them is shown with the grade [L], for example PKU 0.3375 [L]. The residual is a code output that depends on these bins and the equal weights. The pipeline's own sensitivity analysis shows the order moves under reweighting (ρ from 0.89 to 0.98).
- **The order is correctly declared a provisional [H] device.** The pages state this plainly.

## R2 — code runs (python3 -B, scratch copy, timeout 120 s)
- `r3_burden_index.py` → `burden_scores.json`: byte-identical (set sha 0f788821e0fc).
- `r4_burden_residual.py` → `burden_residual.json`: byte-identical (sha d41d4e95b8b1). The CSV differs only in line endings.
- `r15_severity_litcurate.py` → `burden_residual_registry.json` and `burden_scores_registry.json`: byte-identical (registry sha efe81b447194). These are the files the pages read. Page checks match exactly:
  - PKU 0.3375, rank 16
  - CF 0.3075, rank 17
  - DMD 0.4760, rank 6
  - achondrogenesis 0.9167, rank 1
- `r15_gate.py` on a pristine copy: FAIL, 15/16. The failing check is `prior_round_artifacts_preserved`: 10 R9–R14 join/excluded CSVs no longer match their recorded digests. This problem already exists in the repository; it is not caused by this review.

## Edits made (docs only; no numeric change)
- Hub: added the reading-rule note. The two mechanism-class entries changed from "[F]" to "class · observation (mechanism classification)".
- §1: the abstract drops "[V] law". The legend rows [V] and [F] are annotated as not used for biological claims. The completion criterion "[L]/[V]" becomes "[L] (observation)". The efficacy offset e is annotated as a declared bin, not a clinical effect size, and the residual as a code output.
- 02, 07, 17 and 18: "[L]/[V]" becomes "[L] (observation)". The residual sentence is annotated "a code output of declared bins; e is an a-priori efficacy tier, not a clinical effect size".
- 37 and 38: the claim strip changed from "[F] mechanism class" to "observation: mechanism class".

## Open for the author
- Apply the same two template edits to the remaining disease pages: "[L]/[V]" appears on 02, 03, 07, 17, 20 and 23, and the residual sentence appears on all placed pages.
- Consider showing the residual score's grade as "code output" rather than [L].
- Re-freeze or explain the R9–R14 digest drift.
- Run `tools/record_page_notes.py`.
