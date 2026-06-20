# LEDGER — Phase 2: organ emergence + allometric growth law

Per-quantity grading (C3). The engine reads ONLY `param_db.json` (measured gamma + cited
allometric exponents); the measured organ fractions live in `validation_targets.json` and are
read ONLY by the gate's post-hoc test. That separation (asserted by the NON-FIT check) is what
keeps the cited exponents legitimate `[L]` inputs rather than a back-fit.

| quantity | grade | basis |
|---|---|---|
| organ-master γ (8 organs) | **[L]** | NCBI→SantaLucia, read-only (package `organ_gamma.json`) |
| organ emergence **ORDER** = argsort(spinodal γ) | **[V]** | deterministic γ-readout; biologically a null vs CS (package ρ≈−0.41), reproduced |
| relative **dwell** = γ^1.5/(K+brake) | **[F]** | relative size only; absolute size not claimed here |
| cited allometric **exponents b** | **[L]** | comparative-mammalian organ-mass scaling (Stahl 1965; Prothero), fixed independently of human fractions |
| **allometric growth law** f ~ M_body^(b−1) (direction of proportional change in growth) | **[L]-grounded prediction** | a coefficient-free, γ-free statement from the cited b; no per-organ coefficient chosen by us |
| **validation**: does cited b predict measured fraction-change? | **[O]** (n=8) → **[L]** (widened n=11) | Spearman(e_pred=b−1, e_obs)=**+0.690**, exact perm **p=0.069** (n=8) → graded [O] at the time. **Phase 5 widening (pre-registered organ set, n=11): ρ=+0.800, exact p=0.0047 → promoted [L]**; see `LEDGER_organ_allometry_wide.md` (wide gate 8/8, sha d82eeb925973). |
| brain strong-negative-allometry **anchor** | **[V]** | brain has the most negative exponent both predicted (b=0.75) and observed (e_obs=−0.559); direction unambiguous (gate check 5) |
| empirical vs cited **magnitude** for the brain | **[O]** | e_obs(brain)=−0.559 is steeper than e_pred=−0.25 — the human brain's developmental allometry exceeds the generic mammalian exponent; named, not hidden |
| **absolute organ mass** at fixed body size | **[O]** | needs per-organ coefficients / measured fractions; the engine never reads them (would be back-fit) |
| body/face shape axis | **[L]-anchored** | the dosage-instantiated `form(P,E)` decomposition (H²=0.51, twin +37%) from phase-0; referenced, unchanged |

**Gate** `verify_emergence_organs.py` → **6/6 PASS** (DB-sourced · non-fit invariant · determinism
sha `40225433a6` · allometric validation graded honestly · brain anchor · non-blind).

**Honest one-line:** cited comparative-mammalian allometry [L] carries real predictive content for how
human organ PROPORTIONS shift during growth (ρ=0.69 at n=8, brain nailed); the Phase 5 pre-registered
widening (n=11) reached ρ=0.80, exact p=0.0047 → **promoted [L]** (see `LEDGER_organ_allometry_wide.md`);
absolute organ MASS at a fixed size still needs measured coefficients [O].

**Correction recorded:** an earlier draft invented a `brain` γ to include the brain in Part A — removed,
because γ must be measured. Brain now enters Part B (allometric law) via its cited exponent only; no γ
is fabricated.

**Next:** Phase 3 (reduced-order reaction-diffusion trajectory, morphogen D from DB [L]); Phase 4
(fold into Appendix A add-only, relabel the old geometry demos, rewrite around emergence-through-the-parameter).
