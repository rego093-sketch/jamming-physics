# disease_kit — light two-reviewer review (2026-09-29)

Scope: the hub, 6 section pages, 839 disease pages (`docs/disease_kit/dz/*`) and the package in `repro/disease_kit/`.

Sampled pages: hub, §01 method, §03 validation, and the disease pages aadc_deficiency, choroideremia and alkaptonuria (via the §03 table). A scan across all 839 pages covered grade tokens, classification counts and fragility values.

## R1 — claims against data, and the magnitude firewall
- **Firewall is clean.**
  - Every page repeats the no-dose notice three times.
  - Agents are listed as mechanism-direction labels, graded [O].
  - There is no numeric dose, concentration, regimen or effect size.
  - Borderline wording: the qualitative phrase "high-dose fat-soluble-vitamin substitution" in the abetalipoproteinemia row of §03. No number is given.
- **The "corrective direction [F] forced" label is wrong.**
  - In code, the corrective sign is `-DIRINT[emergent_axis_direction]` (`pipeline/treatment_switch.py`).
  - The axis direction is itself graded "[F] forced by (role x mechanism); cited biology" (`analysis.json`). In other words, it is set by the curated lesion class (LOF → supply, GOF → reduce), not by γ.
  - γ sets only the barrier size, γ²/4, and the spinodal.
  - The direction is therefore a code output of cited inputs, read as an interpretation of the model. It is not a forced biological fact.
- **"Recovering the standard of care" is presented as "genuine validation".** Because the sign follows the LOF/GOF label, agreement with enzyme replacement, gene supply or inhibition is largely by construction. The 322/839 matches are a consistency check with practice, not independent validation of the γ geometry.
- **[V] "verified" is used for the R19 cusp geometry.** This is a deterministic code output. barrier = γ²/4 and s_on = ±√γ are algebraic identities; for AADC, 1.3688²/4 = 0.4684 and √1.3688 = 1.170, both correct.
- **Counts reconcile.** 322 match + 29 novel + 488 hold = 839, and this was recounted from the pages.
- **Fragility is not a constant artefact.** Its value varies across pages from 0.00 to 1.00.

## R2 — code runs (python3 -B, scratch copy, timeout 120 s)
- `repro/run_all.py`: OVERALL PASS. All 6 stages pass (72 resolved and 13 suspended), and every per-disease, module, site and system-inheritance hash shows drift 0.
- **Coverage gap.** The in-repo package is v0.32 with 85 disease analyses (`diseases/_registry.json`). The site is release 0.42.1 with 839 disease pages. About 750 pages have no reproduction path inside this repository.
- **AADC check.** The page values γ 1.3688, barrier 0.4684 and spinodal 0.6164 match `diseases/aadc_deficiency/analysis.json` (0.61639).

## Edits made (docs only; no numeric change)
- **Hub.** Added the reading-rule note. The §01 line changes from "corrective sign is forced [F]" to "an interpretation of the model". The §03 line changes from "genuine validation" to "consistency check, partly by construction". The two [F] badges and the legend "[F] forced" become "interpretation".
- **§01 and §03 section pages.** The same relabels, applied to the answer, meta and legend text.
- **Template strings replaced across all 839 disease pages.** Each is an exact string, and each replacement count was asserted:
  - claim-strip "[F] forced" → "interpretation" (839)
  - "(… [F] forced below)" → "(cited role × mechanism, below)" (838)
  - "The corrective direction is forced [F];" → "an interpretation of the model (a code output whose sign follows from the cited lesion role and mechanism)" (839)
  - "load-bearing output … it is [F] forced" → "an interpretation of the model (code output, not a forced biological fact)" (839)
  - "<b>[F]</b> direction." → "Interpretation (direction)." (839)
  - emergent-axis "DOWN/UP [F]" → "(cited role × mechanism)" (596 + 242)
  - "DOWN [F] switch" → "DOWN switch" (672); "UP/DOWN [F] disease" → without [F] (84 + 12)
  - evidence-table rows: "[V] verified" → "code output" (839); "[F] forced … forced by the cusp sign" → "interpretation … sign follows from cited lesion role × mechanism; magnitude [O]" (839)
  - "validation signal for the logic" → "consistency check with established practice (partly by construction)" (319)
  - the "VALIDATION SIGNAL --" key is annotated the same way (839)
- **Result.** No [F] or [V] token remains on any disease page. "Direction only [O]" and "magnitude [O]" are unchanged.

## Open for the author
- §03 still has the heading "Why a recovery counts as validation" and the sentence "main evidence … tracking real biology"; these need rewording.
- The site builder in `repro/disease_kit/tools/build_disease_site.py` still emits the old labels. Do not rebuild into `docs/`.
- Publish the 0.42.1 reproduction inputs for the roughly 750 pages that lack them.
- Run `tools/record_page_notes.py`.
