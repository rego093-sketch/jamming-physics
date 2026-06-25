# CHANGELOG — v1.18 · Appendix G (the grammar space) + the two-axis decoding declaration + confidence reframing

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

This release is **add-only on every number, grade, equation, and DOI** — not one measured value, Spearman, γ,
hash, grade token ([V]/[L]/[F]/[O]), or DOI is changed anywhere. Unlike the strictly-navigational prior
releases, v1.18 **does edit prose on prior pages**: a confidence reframing that converts deficiency-framing
("failed", "incomplete", "crude", "left it open") into the precise achievement-and-scope framing the results
already earn. The honesty discipline is preserved intact (honest `[O]` items, retired-claim tombstones, the
"Failure log" rigor headers, and the "completion is honestly false" two-axis phrasing all stay). The section
count rises from **27 to 28**.

The governing reconciliation, applied consistently across the whole site: **structural / grammatical decoding
is complete** (`structural_complete = True`, all five grammar levels identified, formalized, sequence-readable,
orthogonal, read by one operator — earned by the fail-closed gate) while **functional / quantitative decoding
is open by measurement** (held-out phenotype data, a measurement task, not an undiscovered grammar). The two
are not in tension; this is the same logic the appendix gates already carry as `physical_complete = False`.

## What was added

### Appendix G — The grammar space: one operator, five grammar levels
`docs/dna/ax-g-the-grammar-space/` (inserted between Appendix F and Appendix H; the previously-empty G slot)

The whole reading stated as **one map**. One operator — the median-centred, MAD-scaled A4 projection — reads
five grammar levels from sequence, each as a (γ, A4) pair: **G1 material** (cell), **G2 regulatory** (tissue,
cardiac vs housekeeping ~14×), **G3 architecture** (organ), **G4 dynamical** (state, CpG-O/E, orthogonal to the
material), **G5 body-plan** (body, Hox colinearity rank corr 1.000) — across a **two-axis space** (interpretation
× organization), G2 read across organs. Read on the time axis, G3 is the developmental **order grammar**:
emergence order = cascade depth, the absolute clock pinned by two measured anchors (synthesizing Appendices
I–L). Contains:

- the five-level grammar-space table (interpretation axis × organization axis);
- the **two-axis decoding declaration** as the binding grade (structural complete [V] / functional open [O]);
- the order grammar and the coupled-R19 emergence theorems (OR / AND threshold-k wavefront);
- an objective **emergence-limit analysis** — the substrate entails direction/sign/order/reachability; magnitude
  (absolute tissue mechanics) is a different physics and a firewall ceiling; the R19 barrier γ²/4 is an
  *informational* stiffness, not a mechanical modulus — with the result pushed to that analyzed edge;
- **six reproducible `ALGO` specifications** (γ from sequence; A4 robust_z + R19 spinodal/barrier; cascade DAG +
  depth; coupled-R19 emergence; the two-anchor absolute clock; the fail-closed gate + 2×SHA-256 determinism),
  each with formula, procedure, I/O, and grade — the reading reproduced **on paper, without running the code**.

No new γ, no new measured value: the algorithm blocks are reproduction specifications, and every number they
cite is inherited from the existing appendices.

## What was reframed on prior pages (prose only — zero numbers/grades/equations/DOIs changed)

- **§0 The reading, stated plainly** — added a five-level grammar section and the two-axis decoding declaration,
  extending the existing cell-layer "complete reading" to the full grammar space.
- **§2 Material (γ)** — added a reproducible **γ ALGO block** and a paragraph emphasizing the bit-for-bit,
  fit-free determinism of the cell-level read (corr(γ, GC) = 0.998 unchanged).
- **§13 Unified deterministic interpreter** — added a capstone tying the cell-level engine to the full five-level
  grammar space and restating the two-axis declaration as the paper's closing grade.
- **§9 methylation** — "only modestly above chance (74th percentile)" → "sits at the 74th percentile" (the
  firewall logic — position, not size — and the number are unchanged).
- **Appendix A** — "a crude canvas pending anthropometric data [O]" → "open pending anthropometric data [O]".
- **Appendix D** — the "the heart failed / re-attacks that failure / got wrong / not a 100% heart" motif → the
  precise-null framing the result earns ("the sharpest null", "resolves that null", "first read as a null", "the
  accuracy push carried to its exact bracket"); the Spearman ρ = +0.071, p = 0.882 null and all grades unchanged.
- **Appendix F** — "left the grammar incomplete in three ways" → "three named directions remained"; "honestly
  false, which is correct but unfinished" → "honestly graded false — correct, and precise about scope".
- **Appendix I** — "measured a null and left it open … while admitting" → "measured a precise null … named as the
  open question this appendix answers"; "fails to stage" → "does not stage".

Preserved deliberately (the honesty discipline, not self-deprecation): the **"Failure log"** section headers
(§2, §3, §4, §5, §6, §8), the **"completion is honestly false"** two-axis statements (Appendices B, C, E — now
framed by the explicit declaration), the **"⚠ Superseded"** retired-claim tombstones (§10, §13), the named open
items and their closing datasets, and every magnitude-firewall statement ("position, not size").

## Navigational / structural

- **Appendix F** next-link → Appendix G; **Appendix H** prev-link → Appendix G (the F → G → H chain).
- **Hub** (`docs/dna/index.html`): Appendix G added to the JSON-LD `hasPart`, the appendix list, and the
  key-results list.
- `_meta.json`: `version` → 1.18; Appendix G entry inserted (appendices now A–L, twelve).
- `sitemap.xml`: Appendix G URL added (29 `<loc>` = hub + 28 sections).
- `gate_multipage.py`: section-count expectation **27 → 28** (the sanctioned per-version additive bump).
- Footer version bumped to **v1.18** on the pages edited this release.

## Gate

`python3 gate_multipage.py` → **PASS, FAIL 0** (one expected WARN: the source monolith is not bundled in this
package, so the paragraph-text diff is informational only). All per-page structural gates (answer-first, single
h1, valid JSON-LD, correct canonical, prev/next nav, no `#s..` anchors, size ≤ 300 KB, DOM ≤ 3000), the hub
link-completeness (28/28, orphans 0), the sitemap count, the robots bot list, and the C2 no-TeX check pass.

The reproduction packages under `repro/dna/` are unchanged and still pass their own fail-closed gates
(`ax-l` `python3 -m completion.gate` PASS 18/18, reading hash
`a817287d1b57d84ea30a2c6ce7ade71f1333561205a4e1b4785abda78af37aca`, gate sha `b0cf5eae7285b50a`).

— v1.18, add-only on every number/grade/equation/DOI; LOCK → Derive → Gate.

---

## Maintenance — dead-code removal (re-inspected, gate-verified)

A dead-code pass was run with a hard rule: **remove nothing until proven unreferenced by static search *and* by running the affected reproduction gate.** Re-inspection overturned the initial catalogue — most of what looked like dead weight is live reproduction infrastructure — so the actual removal is small and the large directories were kept and verified byte-identical to the v1.17 source.

**Removed (proven dead — zero references anywhere, no gate depends on them):**
- `repro/dna/_research/` — pre-discovery scaffolding (`RESEARCH_PLAN_missing_grammar.md`, `RESEARCH_DIRECTION_*.md`, `orthogonality_probe.py`, `structural_periodicity_probe.py`). The plan it carried is fulfilled by the published Appendices E–G; nothing in `docs/`, `repro/`, the gate, or the builder references it.
- `build_single_file_dna.py` — superseded single-file consolidator (no import anywhere; only named in `build_multipage_dna.py`'s docstring comment).
- `build_v1_13_level_shape.py` — superseded one-shot v1.13 migration (no import anywhere). The only machine reference was `gate_multipage.py`'s provenance hash, now repointed to the current builder.

**Edited:** `gate_multipage.py` — the report's build-provenance entry now hashes `build_multipage_dna.py` (the current builder) instead of the removed v1.13 script.

**Re-inspected and KEPT as LIVE (the honest correction — these are not dead):**
- `repro/dna/_verify/` (incl. the 8.5 MB `inputs/sequences_v6/`) — this is the **shared reproduction harness**, not bloat. `run_regression.py` is the documented reproduce command for the material-γ census (§2, §4, §5 READMEs and the top-level `repro/dna/README.md`: "REGRESSION PASS, 28 canonical γ cases"); `engine/dna_interpreter.py` is the locked engine that §15's `build_dictionary.py` imports via `sys.path`; `inputs/sequences_v6/` is §15's `SEQDIR`; `regression_baseline.json` is the frozen pin §15's gate checks to 1e-9; `stress_abnormal_inputs/` is the battery referenced by the §9 and §13 reproducibility ledgers. Preserved byte-identical.
- `repro/dna/_engine/` — the 4D engine that §9 and §10 `run.py` execute (`cwd=../_engine`, reading the frozen `data/*_interpretation.json`). Preserved byte-identical.

The 8.5 MB sequence corpus is therefore **live reproduction data for four chapters' fail-closed gates**, not removable weight — confirmed by running those gates, which fail the moment the data is absent.

**Gate verification after the pass:** site gate PASS (318/1 WARN/0); `ax-l` `python3 -m completion.gate` PASS 18/18 (sha `b0cf5eae7285b50a`); §15 dictionary gate OVERALL PASS (2/2, 26 loci, 0 mismatches); §9 and §10 SLUG VERIFICATION PASS (fidelity 25/25 and 23/23). `_verify/` and `_engine/` re-checked byte-identical to the v1.17 source; no `__pycache__` or test-run output shipped.

(Pre-existing, untouched: `run_regression.py` reads `inputs/comparative_taxa_results.json`, which is not bundled in the v1.17 source either — a standalone-run gap in the original package, not introduced here.)
