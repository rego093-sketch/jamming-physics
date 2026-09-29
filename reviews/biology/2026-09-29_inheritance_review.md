# inheritance — light review (2026-09-29)

## Summary
R2 ran `engine/env_to_germline.py`, `engine/lever_map.py` and `engine/feasibility_validation.py` from `repro/inheritance/` with `python3 -B`. None of them writes files.

The printed numbers match the pages:
- TG5: 0.45 and 0.7238 series, RNA undetectable at F3;
- LV: w* = 0.05527, γ* crossing, loss 0.5527;
- FV8: point-biserial 0.4852, p 0.0274, GC-partialled 0.4731.

The magnitude firewall is clean. Every dose, titre, interval and schedule is [O], and the only numbers are in model units.

§15 is a strong section: pre-registered held-out tests against Replogle 2022, DepMap and Horlbeck 2016, including an honest null.

## Findings
1. **Gene-therapy γ edits are entered values that are not physically plausible.** Severity: high.
   - §11: +0.08 is set in `gene_therapy.py:42`.
   - §18: a knockout is set to 0.05·γ in `lever_map.py:85`, and base and prime edits shift γ by fixed amounts.
   - A single base substitution changes 2 of the 2500 dinucleotides in the window, so γ moves by at most about 0.0013.
   - Coding edits do not change promoter γ.
   - Gene addition (AAV) is missing from the lever map.
   - γ* = 1.4598 holds by the choice of h_cap.
2. **Imprinted "escapees survive both erasures" (§6) conflicts with observation.** Severity: high.
   - Imprints are erased in PGCs and re-set by sex (Hajkova 2002; Reik & Walter 2001).
   - ρ = 1.00 at fixed D holds by construction.
3. **[F] on biological claims.** Severity: medium.
   - §1: the SET/drive decomposition. The environment can also mutate DNA (Kong 2012).
   - §14: the corrective sign is the textbook oncogene/suppressor classification (Vogelstein 2013).
4. **[V] on results that hold by construction.** Severity: medium.
   - §4: add, veto and latch.
   - §5: p² and γ-ranked survival at fixed D.
   - §12 and §13: spinodal monotonicity.
   - §16: the 13/13 asymmetry follows from a paternal burst shorter than the crossing time.
   - §19 (the page named "16-scoreboard"): "18/18 green".
5. **Grid and parameter artefacts.** Severity: low.
   - §9: the "optimum at 0.40" is the first point of a plateau, with gain +0.033064 identical down to 0.033.
   - §7: the maternal contact fraction of 0.00 rests on n = 2.
   - §8: the MFPT values differ by about 2 %.
   - §17: the saRNA vs mRNA difference (0.5317 vs 0.5072) depends on the chosen windows.
   - FV8: only 3 of 7 GOF genes fall on the predicted side.
6. **Missing observations.** Severity: medium.
   - two demethylation waves (Seisenberger 2012);
   - *C. elegans* small-RNA inheritance (Rechavi 2011);
   - sperm tsRNA (Chen 2016; Sharma 2016);
   - the mammalian debate (Heard & Martienssen 2014);
   - trained immunity and the disputed inheritance of it (Netea 2016; Katzmarski 2021; Kaufmann 2022);
   - antibody waning with persistent memory B cells after mRNA vaccination (Levin 2021; Goel 2021);
   - approved siRNA, ASO, editing and AAV therapies.

## What I changed (docs/inheritance only)
- **Hub:** added a Reading-rule note after the `<h1>`. The two chapter-list `[F]` gtags become `interp.`.
- **§1:** the `[F] forced` badge and the lede `[F]` become "interpretation".
- **§14:** the badge becomes "observation + interpretation", and the lede becomes "observation (sign) / code output / [O]".
- **All 19 chapters:** each gets one lt-note with its input dependence, consistency status, or the conflicting and missing observations, with citations.
- No numbers changed and nothing deleted.
