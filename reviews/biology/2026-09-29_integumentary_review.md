# integumentary — light review (2026-09-29)

## Summary
- R1 checked §1 (order), §5 (turnover) and §7 (UV carcinogenesis) against data.
- R2 ran `repro/run_all.py` from a scratch copy with `python3 -B`. It finished, with all PASS and determinism 2×sha256 identical (sha 1fb59f556e01…).
- R2 also probed `_oncology/carcinogen_dose_response.py` and `_engine/skn_dynamics.py`.
- Every printed number matches the pages:
  - γ: TP63 1.3643, KRT14 1.4894, MITF 1.3945, EDAR 1.3696;
  - order: epidermis → appendage → melanocyte → keratinocyte;
  - turnover 28 d;
  - melanoma burst RR 5.674.
- Magnitude firewall: clean. UV doses are in model units only.
- Theory grades appeared about 90 times across 14 chapters. The §11–§13 badges read "[V] Simulation-verified" and "[F] Forced (substrate)".

## Findings
1. **§1 developmental order read off γ ("falsifiable consequence").** Severity: high.
   - The ranking puts keratinocyte (KRT14) last.
   - Observation: K14 is expressed in the surface ectoderm from about E9.5 in mouse (Byrne, Tainsky & Fuchs 1994). That is well before EDAR-dependent hair placodes at about E14.5 (Headon & Overbeek 1999).
   - The abstract also showed a literal "&rarr;", caused by a double-escaped `&amp;rarr;`.
2. **§5 turnover "~28 d lands in the cited 28–40 d window" is true by construction.** Severity: high.
   - Where: `skn_dynamics.py`, lines 238–244.
   - `ratio = d_phase / d_phase` is 1 identically, so the total is 2 × the 14 d input = 28 d.
   - The grade was [V].
3. **§7 melanoma "burst RR up to ~5.7×" depends on the inputs and overshoots the observation.** Severity: medium.
   - The same code gives 2.2× at cumulative dose 4, 5.7× at 6 and 7.0× at 8, with the burst grid fixed at 20 → 7 exposures.
   - The observed summary RR is 1.61 (95 % CI 1.31–1.99; Gandini 2005). The page cites this value in a card, but not next to the model number.
   - The direction matches the observation; the magnitude does not.
4. **"[F] Forced (substrate)" occlusion and adhesion set-points in §11–§13.** Severity: low.
   - These are dimensionless regime scales of the cubic. They are now labelled consistency (substrate).

## What I changed (docs/integumentary only)
- **Hub.** Added the reading-rule note after `<h1>`.
- **Grade legends.** On the hub and the 14 chapter footers, the "Grades: [F] forced · [V] …" legend is now "Labels (reading rule 2026-09-29): consistency … code output … [L] … [O]".
- **§1.**
  - Added a label and observation paragraph with the K14 and EDAR citations and building marked [O] (dna §RB).
  - Fixed the `&amp;rarr;` escaping.
  - "falsifiable consequence" now reads "interpretation".
- **§5.** Added a consistency paragraph; the answer and abstract now say "(2 × 14 by construction)".
- **§7.** Added an input-dependence and observation paragraph; the answer and abstract now say "modelled" and give the observed 1.61.
- **All pages, relabelled outside the existing lt-note asides:**
  - [V] → code output;
  - [F] → consistency;
  - "simulation-verified" → "simulated".
- No number or lt-note was removed.
