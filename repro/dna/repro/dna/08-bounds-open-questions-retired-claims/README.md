# repro/dna/08-bounds-open-questions-retired-claims

**§8 — Bounds, open questions, retired claims**

Standing reference; the bounds and the failure log derive from the chapters above (see `../_verify/` for the measured backbone).

Claim grade: (governance/reference — no badge)

---

## v1.9 stress battery — bounds added (standing register)

The second-session stress battery (chapters 02/12/13/14, `stress_*/`; all deterministic,
2×sha256; locked grammar byte-identical) added these bounds. Detail and proof live in the
cited chapter ledgers; this register aggregates them per C3.

1. **Methylation auto-detector — false-positive below ~25% GC.** The 4-regime classifier
   false-positives `PLANT` on extreme-AT genomes (Plasmodium 20.4%, Dictyostelium 22.3%,
   Entamoeba 24.5% — the last out-of-sample) that have no global 5mC. Cause: composition-
   driven CpG/CpHpG depletion (not methylation), proven by matched-composition nulls.
   **Corrected** at the chapter-14 guard (`detect_regime_safe`, GC floor 0.25), validated
   out-of-sample. Detail: `../12-clade-methylation-readers/LEDGER_clade_readers.md`,
   `../14-defensive-guards/stress_guard_validation/`.

2. **Retired/corrected claim — "auto-detector all test cases correct."** The §12 ledger's
   blanket "all test cases correct" is corrected to "correct within ~33–45% GC and for
   out-of-panel plants/mammals; bounded below ~25% GC." The shipped panel's Plasmodium
   call (`PLANT_global_CG_CHG_CHH`) is an instance of the false-positive and is corrected
   at the guard layer (raw call retained for audit). Locked engine unchanged.

3. **γ "two projections" link is GC-domain-limited.** The γ-beyond-GC residual couples to
   CpG O/E in the normal band but **inverts at GC ≈ 20%**; not a universal identity.
   Detail: `../02-material-threshold-scale/stress_gamma_vs_gc/`.

4. **A4 anchor count is resolution-relative.** Anchor *positions* are stable (93% within
   2 kb); anchor *count* is set by `min_shell_bp`, not absolute.
   Detail: `../13-unified-deterministic-interpreter/stress_coordinate_stability/`.

5. **Engine robustness — `run_key` sub-window input.** Raises an opaque `IndexError` on
   `len < W=2000` (loud, not silently wrong); guarded to a clean `[O]`
   (`../14-defensive-guards/`). A locked-engine fix would be a new version.

No locked grammar, threshold, γ, NN table, or frozen `expected/` was modified; all
corrections live in the chapter-14 guard **wrapper** (single-source import + sha256 pin).
