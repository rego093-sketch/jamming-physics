# FINALIZATION — VP-SPEC v1.8 PRECISION CLOSEOUT
### dna_vp_site_INTEGRATED v1.9.1 · appendix-A geneclock · Phase 7 morphogen length-scale

**Session mandate (Korean):** *VP_SPEC_v1_8 기준으로 정밀 마감하라* — finalize the package precisely
against the VP-SPEC v1.8 standard.
**Type:** documentation-only closeout. **No engine edits, no change to any pinned `code/*.py`,
`code/*.json`, the canonical `docs/dna/index.html` body, any measured input, or any dated session
`gate.json` / `CHANGELOG` record.** Science version unchanged (appendix v12.4 · site v1.9.1).
**Outcome:** the package is **VP-SPEC v1.8 conformant**; the full `verify_all.py` **20/20** was
**independently reproduced**; and the only defects found — two **living** documents that had not kept
up with the emergence fold-in + Phase 7 — were corrected to the verified live state. The bit-for-bit
governed set is **untouched (87 files, drift 0)**, re-confirmed *after* the edits.

---

## 0. Input integrity (checked first, before any work)

- **Package SHA256** verified against its sidecar **and** the Phase-7 report §7:
  `0d1698c3f0a42db36123c44d0aeb6dbdcef39e667d036da123a1a985238dafd5` → **OK** (3-way match:
  sidecar `.sha256`, report §7, recomputed digest).
- Archive: 462 files, no `__pycache__`/`.pyc` build artifacts present (report §7 claim confirmed).

---

## 1. Verification independently reproduced (the 정밀 part)

`verify_all.py` cannot complete in one process inside a tight runtime budget (`verify_dev_timing_wide`
alone ~261 s), so — exactly as the package's own §4 disclosure prescribes — every gate was run
**individually to completion** and the integrity/fidelity layers checked directly. Because every gate is
deterministic, this is a runtime accommodation, not a methodological shortcut: the result is identical
to a single inline `verify_all.py` run.

### [1] Twelve morpho gates — all PASS (5/5)

| gate | verdict | wall time |
|---|---|---|
| verify_gene_clock | PASS (5/5) | 7 s |
| verify_morpho_plus | PASS (5/5) | 57 s |
| verify_adipose | PASS (5/5) | 30 s |
| verify_dev_timing | PASS (5/5) | 8 s |
| verify_timing_predictors | PASS (5/5) | 54 s |
| verify_life_course | PASS (5/5) | 26 s |
| verify_organ_timing | PASS (5/5) | 8 s |
| verify_organ_anatomy | PASS (5/5) | 6 s |
| verify_heart_substages | PASS (5/5) | 60 s |
| verify_morpho_decomposition | PASS (5/5) | 17 s |
| verify_dev_timing_robust | PASS (5/5) | 12 s |
| verify_dev_timing_wide | PASS (5/5) | **264 s** (matches report's ~261 s) |

### [1b] Five emergence gates — all PASS, hashes match the frozen baseline exactly

| gate | counts | result hash(es) | baseline match |
|---|---|---|---|
| emergence_heart | 7/7 | `939ae9924a6c` | ✓ |
| emergence_organs | 6/6 | `40225433a67a` | ✓ |
| emergence_trajectory | 7/7 | `b2b34a770f5a` | ✓ |
| emergence_organs_wide | 8/8 | `d82eeb925973` | ✓ |
| emergence_morphogen (Phase 7) | 8/8 | `01b0b6ea8b10` / band `4ea1c7b4111c` | ✓ |

### [2] Source integrity — **drift 0**

Recomputed sha256 over the governed set exactly as `verify_all.governed_files()` defines it (every `.py`
and every `.json` under `code/`): **87 files pinned, 87 live; changed 0, missing 0, extra 0.** The
measured-γ tables and Carnegie-stage data are bit-for-bit identical to the freeze — the standing
invariant "the measured tables stay bit-for-bit, never tuned" holds.

### [3]/[3b] Fidelity — match

12 morpho fidelity baselines present under `repro/morpho/expected/`; `emergence_gate_baseline.json`
freezes all 5 emergence fingerprints and **equals the live runs leaf-for-leaf** (every count and every
hash in the table above).

**Single-entry tally reproduced: `OVERALL: PASS (20/20 checks)` = 12 morpho + 5 emergence + 1 source
integrity + 1 morpho fidelity + 1 emergence fidelity.**

The Phase 7 headline reproduced exactly: model band `λ=√(D·τ)=[18.97,189.74] µm` (central 60 µm) vs
six measured morphogen gradients → geom-mean 31.41 µm, **factor 1.91** (tol 3), **5/6 in band**,
**independent set Bicoid/Nodal/Shh 3/3 in band**, robust to ±30 % jitter (worst factor 2.47); Wingless
(~6 µm) reported as a band miss, not excluded → **REGIME-level [L]-grounded**.

---

## 2. VP-SPEC v1.8 conformance audit

| principle | requirement | finding |
|---|---|---|
| **C1** reproducibility | deterministic regeneration; displayed/stated values == regenerated (drift 0) | **PASS** — 20/20 reproduced; 87-file pin drift 0; 2×sha per gate. Two living docs realigned to live state (§3). |
| **C2** HTML canonical, no TeX | no `.tex` / `*.eq_list.*` / `txt/` body; SVG canonical; img-alt LaTeX kept as a11y meta | **PASS** — `find` returns no `.tex`, no `eq_list`; canonical HTML has 0 `class="katex"`, 0 MathJax, 0 `$$`, 0 raw `\begin`. Merge gate independently logged "C2 no bundled TeX: none". |
| **C3** `[O]` reason disclosure | every `[O]` names a concrete obstacle; root ledger aggregates all `[O]` + obstacles + locations | **PASS** — `IRREPRODUCIBILITY_LEDGER.md` aggregates the body + appendix `[O]` register (timing null, absolute size, facial-aging axis, single canonical H², Layers-2/3 principle-demonstration, one-specifier-per-milestone), each with the measured input that would close it, pointing to per-section ledgers. |
| **C4** retrieval-readiness | answer-first, self-contained, JSON-LD, machine-accessible static HTML | **PASS (page level)** — canonical HTML: 7 `<p class="answer">`, 2 JSON-LD blocks (ScholarlyArticle · BreadcrumbList · CreativeWorkSeries · Person), exactly 1 `<h1>`, `rel="canonical"`, ORCID `sameAs`. Size 84.7 KB ≤ 300 KB; ~766 nodes ≤ 3000. Site-level access files: see scope boundary (§5). |
| **§8** gates | phase + constitution + search gates | **PASS** — build-time records all green: appendix-merge 16/16, integration-v1.8 18/18, ch13-unified 9-check, ch14 guards, phase2-dna-full; live re-run 20/20. |

---

## 3. Finalization actions (the only changes made)

Two **living** documents (read by users / re-derived each session) had drifted behind the package's own
evolution. Both are **non-pinned** (outside `code/`), so correcting them — explicitly permitted by the
constitution C0 ("틀린 내용을 수정하거나 잘못된것을 삭제하는 것은 무방하다") — cannot perturb the
bit-for-bit set. Dated session records (the appendix-merge `gate.json` at "69 files / 14·14", the
emergence-foldin changelog at "80 files / 18·18", etc.) were **left intact**: they are faithful
historical snapshots, not living state.

**(1) `REPRODUCE.md`** — was the oldest, pre-appendix-merge **v5.1** snapshot:
- *before:* `OVERALL: PASS (11/11 checks)`, "9 gates", "54 governed files"; gate listing omitted three
  morpho gates (organ_timing / organ_anatomy / heart_substages) and all five emergence gates.
- *after:* `OVERALL: PASS (20/20 checks)`; full 12 morpho + 5 emergence gate listing (with the Phase 7
  morphogen gate described); "87 governed files"; explicit 20-check tally; decomposed-freeze runtime
  note. Added gate one-liners verified against live gate output (no fabrication — e.g. organ_timing
  "7 [V]-master organ primordia, order [V] / timing [O]", heart_substages "[O] null + [F] forced-choice").

**(2) `IRREPRODUCIBILITY_LEDGER.md` §2** — verify-state parenthetical was the **appendix-merge** snapshot:
- *before:* "`verify_all.py` PASS **14/14**: twelve gates 5/5 + a source pin over **69** governed files,
  drift 0 + twelve frozen fidelity baselines".
- *after:* "`verify_all.py` PASS **20/20**: twelve morpho gates 5/5 + five emergence gates
  (7/7·6/6·7/7·8/8·8/8) + a source pin over **87** governed files, drift 0 + twelve morpho fidelity
  baselines + five emergence fingerprints". The `[O]` register itself was already current and was **not**
  altered — Phase 7 was an `[L]`-grounded *promotion*, not a new `[O]`.

**(3) `VERSION`** — prepended a clearly-marked, dated **documentation-only** finalization entry recording
the above, stating the science version is unchanged at v12.4, and re-confirming 87 files / drift 0 after
the edits. (Also a non-pinned doc.)

**(4) This report** added at the package root.

---

## 4. Drift-zero proof (the discipline held)

The governed pin was recomputed **after** the doc edits: **87 files, changed 0, added 0, removed 0 →
drift 0.** No `code/*.py`, no `code/*.json`, no measured input, and no whitepaper §1–§13 / canonical
HTML body was touched. Every edit lands on a non-pinned documentation file. The no-tuning / add-only /
bit-for-bit invariant is intact — a green `verify_all.py` still certifies that the *released* numbers
reproduce and nothing measured was silently edited.

---

## 5. Scope boundary (named, not fabricated)

The integrated package is the **single DNA paper + its appendix-A geneclock repro layer**. The
site-level common files — top-level `docs/index.html`, `docs/sitemap.xml`, `docs/robots.txt`,
`docs/llms.txt` — are **intentionally absent**. Under VP-SPEC §1 lane rules and the §4 session matrix
these are produced by the **full-site Phase 5/6 assembly** (which links all nine papers), not by a
single-paper lane; manufacturing them here would be a lane violation and would fabricate a 9-paper
context this package does not contain. Per the project's own "name it `[O]`, don't fabricate it"
discipline, this boundary is **stated, not papered over** — it is a session-scope fact, not a defect of
this package.

---

## 6. Residuals (named, kept)

1. **`_meta.json` totals vs `manifest/dna.csv`** measure different scopes (meta totals 5471 words /
   13 chapters vs manifest 6304 words / 14 sections — the constitution/front-matter section and the
   gate's word-count exclusion zones differ). The package's own Phase-2 derive gate
   (`phase2-dna-full.gate.json`) and the C1 reconcile certify this at build time; it is not a drift.
   A future full-site session with `tools/reconcile_derived_to_html.py` in-package could re-assert it
   directly — out of scope here (that tool is not shipped in this single-paper package).
2. **Domain grade vocabulary** — the DNA manifest uses `admissible` / `principle-demonstration`
   alongside the `[V]/[L]/[F]/[O]` ledger grades; these are the paper's documented domain grades, not
   the generic VP-SPEC `forced/calibrated/open/null`. Consistent within the paper; noted for cross-paper
   alignment.
3. **The science `[O]` register is unchanged** — every `[O]` (timing null, absolute size, facial-aging
   axis, single canonical H², Layers-2/3 form, one-specifier-per-milestone) remains data-blocked, not
   effort-blocked. Phase 7 closed none of them; it validated a separate `[L]`-grounded regime claim.

---

## 7. Deliverable

- **Package:** `dna_vp_site_INTEGRATED_v1_9_1_appendixA_geneclock_phase7_morphogen_length_vpspec_v1_8_FINAL.zip`
- **Contents:** the full input package with the four documentation additions/corrections above integrated
  (REPRODUCE.md, IRREPRODUCIBILITY_LEDGER.md §2, VERSION, this report). Build artifacts excluded.
- **Single-entry verification:** `python3 verify_all.py` → **OVERALL: PASS (20/20 checks)** (unchanged).
- **Governed pin:** 87 files, **drift 0** (re-confirmed post-edit).
- **DOI of record:** `10.5281/zenodo.20471407` maintained (registry §2 · `_meta.json` · canonical HTML
  all agree) — this is a documentation living-version snapshot, science version v12.4.
- A fresh `.sha256` sidecar accompanies the finalized archive.

— closeout (VP-SPEC v1.8) —
