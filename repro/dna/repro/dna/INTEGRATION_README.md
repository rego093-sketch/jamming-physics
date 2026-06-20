# DNA paper — integrated front+back (VP-SPEC v1.8), chapters 01–12

This package is the single canonical DNA paper with the research extensions merged in.

## Provenance of each chapter
- **01–08** — canonical site `dna_vp_site_20260614` (Constitution, γ material, SET, STATE, DWELL, environment h, cases, bounds).
- **09–10** — research handoff v1.9 (methylation layer; lactase three-layer stack). Canonical HTML already conformant.
- **11–12** — authored this session to the §6 chapter template (cross-kingdom stress test; clade-specific methylation readers).

## Compatibility (verified)
Same γ engine end to end: the site's `gamma_lib_v10.py` and the 09–12 engines share a character-identical
SantaLucia-1998 nearest-neighbour table and `γ = −mean(NN ΔG)`. On human_SOX2 (302 512 bp) both give
γ = 1.287315 (Δ = 0). The site's 01–08 manifest rows are byte-identical to the v1.9 manifest. The two were
always one lineage; 09→12 is the advance, and §11 maps exactly where the site's headline (corr(γ,GC)=0.998,
CV 0.1–2%) holds — every kingdom for the correlation, iso-GC species only for the invariance.

## Verify
- `python3 repro/dna/11-cross-kingdom-stress-test/run.py` → SLUG VERIFICATION: PASS
- `python3 repro/dna/12-clade-methylation-readers/run.py` → SLUG VERIFICATION: PASS
- `python3 repro/dna/11-cross-kingdom-stress-test/audit/audit.py` → NCBI audit PASS (|Δγ| = 0)
- integration gate (this session): 18/18 PASS — see `reports/dna-integration-v1_8.gate.json`

## One inherited follow-up
Chapters 01–08 (from the canonical site, built before the v1.8 search gate) lack the answer-first
`<p class="answer">` block. The spec-correct fix is a Phase-2 `tools/derive_meta.py` run (deterministic,
word-count-neutral) — not hand-authoring, which §1 forbids. Chapters 09–12 already carry answer-first blocks.