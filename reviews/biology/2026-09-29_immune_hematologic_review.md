# immune_hematologic — light review (2026-09-29)

## Summary
- R1 compared the hub, §3 and §15 claims with embryology and immunology data.
- R2 ran scripts from a scratch copy of `repro/immune_hematologic/` with `python3 -B`:
  - `_dynamics/lineage_order.py`, `_dynamics/emergent_durable_boost.py` and `_dynamics/emergent_immunosenescence.py` each finished in under 7 s;
  - `run_all.py` printed the emergence block, then hit the 120 s limit in the stress battery.
- Every printed number matches the pages:
  - γ: RUNX1 1.3225, TLX1 1.4228, FOXN1 1.4533, PAX5 1.4892;
  - boost: t_θ 29.54 / 35.51 / 35.89 / 47.64; PF 1.00 at r = 1, 0.38 at r = 0.25, 0.49 at r = 3;
  - involution: escape 0.29 % → 3.71 %, naive export 32.9 % → 15.9 %.
- Magnitude firewall: clean. Every therapy page states "direction/class only". There is no dose, titre or real-time schedule.
- The hub and all 21 chapters carried [V] or [F] badges on biological claims.

## Findings
1. **§3 lineage order graded [V]: "endpoints match embryology".** Severity: high.
   - Where: `docs/immune_hematologic/03-developmental-lineage-order-gamma-readout/` and the hub.
   - The γ ranking puts bone-marrow haematopoiesis first.
   - Observation: bone marrow is the last haematopoietic site to be colonised, after yolk sac, AGM, fetal liver and spleen, and after the thymus is seeded (Tavian & Péault 2005).
   - The page conflates the early RUNX1 programme (AGM; North et al. 1999) with the bone-marrow organ.
2. **§3 "shared-drive race confirms the order dynamically".** Severity: medium.
   - Under one rising shared drive, each switch commits at its own spinodal.
   - So commit order and spacing (0.0213 vs 0.0211) reproduce the γ ranking by construction. This is a consistency check, not a test.
3. **§15 "optimal re-boost interval emerges at the measured half-life".** Severity: high.
   - Where: `emergent_durable_boost.py`, lines 23 and 105.
   - The horizon is set to T_H = n_b · t_θ. Boosting every t_θ therefore covers 100 % of the horizon by construction.
   - r* = 1 is read on a 7-point grid.
   - The "measured half-life" is a model output: D = 0.28, θ = 0.5.
4. **Seam and harness "[V]/[F]" in §16–§21.** Severity: low.
   - These pages record a cross-package drift of 0 and pointer declarations. They are consistency checks between shipped engines, not biological verification.
   - I relabelled them without changing the text.
5. **γ provenance.** Positive finding.
   - The four promoter windows are byte-exact against NCBI GRCh38.p14. This is a genuine observation-level check, and it is now labelled as one.

## What I changed (docs/immune_hematologic only)
- **Hub.**
  - Added the reading-rule note after `<h1>`.
  - The intro's order sentence is now labelled code output and interpretation, with [O] per dna §RB and the observed site sequence.
  - The §3 and §15 list entries are rewritten.
  - The legend sentence now reads "measured inputs or model outputs".
- **§3.** Two added paragraphs:
  - the observation (Tavian & Péault 2005; North et al. 1999);
  - the race relabelled as a consistency check.
  - The answer paragraph is rewritten to match.
- **§15.** Added a paragraph on input dependence and the horizon construction; the answer paragraph is reworded.
- **All pages, relabelled outside the existing lt-note asides:**
  - [V] → code output;
  - [F] → consistency;
  - the γ "[V] canonical derivation" → observation (measured).
- No number or lt-note was removed.
