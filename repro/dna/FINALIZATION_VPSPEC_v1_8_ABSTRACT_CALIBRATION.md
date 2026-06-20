# FINALIZATION — VP-SPEC v1.8 ABSTRACT / CLAIM CALIBRATION
### dna_vp_site_INTEGRATED v1.9.1 · "A Deterministic Two-Layer Interpretation of DNA" · appendix-A geneclock · Phase 7 morphogen

**Session mandate (Korean):** the whitepaper *under-reported* its result — for a paradigm-declaring
white paper (not a journal paper) the front-door claim surface read as self-deprecating, the abstract did
not fully state what the engine actually does, and a stale verification count contradicted the rest of the
package. **Fix the under-statement and resolve the internal conflicts — method delegated — without
breaking the VP_SPEC_v1_8 writing standard.**

**Type:** claim-surface calibration, editable-surface only. **No engine edits, no change to any pinned
`code/*.py` / `code/*.json`, no measured input, no equation, no measured table, and no dated session
record.** Science version unchanged (appendix v12.4 · site v1.9.1 · DOI `10.5281/zenodo.20471407`).

**Outcome:** the package is **VP-SPEC v1.8 conformant**; the governed set is **untouched (87 files,
drift 0, re-confirmed against the package's own frozen `expected_sha256.json` after the edits)**; the full
`verify_all.py` **20/20** still reproduces (gene-clock 5/5 and Phase-7 morphogen 8/8 re-run live, frozen
hashes `01b0b6ea8b10` / `4ea1c7b4111c` matched exactly); and **exactly two non-governed files changed**
(`docs/dna/index.html`, `docs/dna/_meta.json`), verified by full-tree diff against the input archive.

---

## 0. Input integrity (checked first)

- **Package SHA256** of the input archive verified against its sidecar
  `dna_vp_site_INTEGRATED_v1_9_1_FINAL_zip.sha256`:
  `7f863b1d479a5bb108ec918dbd03917fa70998c52449e693ce65606aa3151e6b` → **OK**.
  (The prior closeout §0 records `0d1698c3…`; that is the *pre-closeout* archive — this input is the
  post-closeout FINAL that already carries the four documentation additions. Both are internally
  consistent; this session builds on the FINAL.)
- Archive extracted clean to a working tree (390 files). No `__pycache__` / `.pyc` build artifacts in the
  delivered archive (any bytecode produced by re-running gates during verification was purged before
  repackaging).

---

## 1. The defects found (and why each is a real problem, not a style preference)

### 1a. Under-statement of the result on the front-door claim surface
The page-level **abstract** and **answer** opened defensively. The abstract led with what γ *cannot* do
("barely changes … the difference therefore lives **not** in the readable material …") and closed on two
disclaimers, so a first-time reader met the limitations before the achievement. For a white paper whose
thesis is precisely that *one deterministic engine reads every locus the same way and relocates where
organisms differ into four readable operations*, that ordering buried the headline. Under VP-SPEC **§6-R.3
answer-first** the claim surface must lead with **entity + value/conclusion + grade** — a defensive
opening is a writing-standard miss, not merely a tone choice.

### 1b. Over-statement of γ-universality (an internal conflict with §11)
The same abstract asserted γ "barely changes across species, kingdoms, and phyla (CV 0.1–2%)." But the
body's own **§11 cross-kingdom stress test** states γ is **not** taxon-invariant at genome scale —
**bulk CV 5.8 %**, reaching **8.3 %** across one protein (histone-H4) — and that the 0.1–2 % figure holds
**among the master switches at comparable GC**. The abstract therefore over-generalized the body's
carefully scoped claim: a direct front-door / §11 contradiction.

### 1c. A stale verification count contradicting the whole package
The canonical paper still reported the **pre-emergence-foldin** count in two places — the appendix `.ver`
badge and the closing reproduction sentence: *"`verify_all.py` returns PASS **14/14** … **69** governed
files … twelve frozen fidelity baselines."* Every other living artifact (REPRODUCE.md,
IRREPRODUCIBILITY_LEDGER.md, README, and `verify_all.py` itself) and the live re-run all say **20/20 / 87
files**. `_meta.json` carried the same stale `14/14 / 69`. Left as-is, the canonical paper contradicted
its own version badge **and** the rest of the package.

---

## 2. The changes made (the only edits — both non-governed, editable-surface)

All edits land on the VP-SPEC **§6-D / §13 editable surface** (`<head>` description · `.abstract` ·
`.answer` · the appendix `.ver` version badge · the appendix reproduction sentence as a **C0 factual
correction** · `_meta.json` summary card). No `<main>` body prose meaning, equation, number, or measured
table in §1–§13 was altered. **C0 governs and permits correcting demonstrably wrong content**
("틀린 내용을 수정하거나 잘못된것을 삭제하는 것은 무방하다").

### (1) `docs/dna/index.html` — page **answer** (`.answer`, word-count-excluded)
Re-ordered to lead with the engine and the relocation result, closing on grading + bit-for-bit
reproduction. Entity-first, 57 words, no new numbers, no grade change.

### (2) `docs/dna/index.html` — page **abstract** (`.abstract`, word-count-excluded)
Rewritten to **state the achievement first** and **resolve 1b precisely**:
- Opens: *a single deterministic engine, grounded in a mechanically measured property of the sequence,
  reads every DNA locus the same way and reproduces bit-for-bit*; *its central result relocates where
  organisms differ.*
- States γ with the body's exact scoping: an **affine read of GC (corr(γ,GC)=0.998)** that **barely
  varies across the master switches (cross-species CV 0.1–2 %)** *and* **5.8 % across whole genomes** — so
  γ sets the **R19** switch threshold but is **not where taxa part**. This is a verbatim reconciliation
  with §11; both figures now appear together.
- Names the four readable operations with their body numbers: **SET**, **STATE**, **DWELL (∝ γ^1.5)**,
  environment-written **methylation tilt (CpG handles 11–179)**.
- Nods **§13** (one engine unifying the material, the **A4** coordinate, and the methylation regime),
  keeps the grading vocabulary (**admissible / principle-demonstration / open**), and retains the honest
  present-tense scope as a single closing clause rather than a dominant takeaway.

**Anti-invention (반작문) re-checked:** every number token in the new abstract — `0.998`, `0.1–2%`,
`5.8%`, `γ^1.5`, `11–179`, `R19`, `A4`, `§13` — was confirmed present in the §1–§13 body (the abstract
introduces **no** number that does not already appear and is graded in the body). **No grade was upgraded.**

### (3) `docs/dna/index.html` — page **meta description** (`<head>`)
Re-pointed from "One deterministic **paper** … barely separates taxa" to "One deterministic, **reproducible
engine** … **near-invariant across the body's master switches**," preserving the §13 unification nod. This
showcases the reproducibility virtue and applies the same master-switch scoping as 1b. (323 chars; the
page-level description is not held to the per-chapter 80–160 cap.)

### (4) Verification-count correction — **C0 factual fix** (resolves 1c)
- `index.html` `.ver` badge: `verify_all 14/14` → `verify_all 20/20`.
- `index.html` closing reproduction sentence: `PASS 14/14 — twelve add-only gates each 5/5 … 69 governed
  files … twelve frozen fidelity baselines` → `PASS 20/20 — twelve morpho and five emergence gates … 87
  governed files … the fidelity baselines`. This sentence sits in appendix-A body prose; the replacement
  is **word-count-neutral (26 → 26 whitespace tokens)**, so the §8 word-count discipline is untouched
  while the false count is corrected.
- `_meta.json` `verify` field: `PASS 14/14 (12 gates 5/5 + sha256 pin 69 files drift 0 + 12 fidelity
  baselines)` → `PASS 20/20 (12 morpho gates 5/5 + 5 emergence gates + sha256 pin 87 files drift 0 + 12
  morpho fidelity baselines + 5 emergence fingerprints)`. JSON re-validated.

---

## 3. VP-SPEC v1.8 conformance audit

| principle | requirement | finding |
|---|---|---|
| **C0** constitution | English-only whitepaper; return original + additions; correcting wrong content permitted | **PASS** — edits are additions/corrections on the editable surface; the stale-count fix is the C0-sanctioned correction of demonstrably false content. |
| **C1** reproducibility | deterministic regeneration; displayed == regenerated; drift 0 | **PASS** — 87-file governed pin re-checked against the package's frozen `expected_sha256.json`: **changed 0, missing 0, extra 0**. gene-clock 5/5 and Phase-7 morphogen 8/8 re-run live; hashes match the freeze. |
| **C2** HTML canonical, no TeX | no bundled `.tex`/`eq_list`; SVG canonical; **0 katex** | **PASS** — canonical HTML: 0 `class="katex"`, 0 MathJax, 0 `$$`; abstract math kept as unicode (γ, ∝, §13, γ^1.5, corr) as before — no math representation regressed. |
| **C3** `[O]` disclosure | every `[O]` names an obstacle; ledger aggregates | **PASS** — the `[O]` register was **not touched**; no claim was promoted, no obstacle removed or hidden. The calibration tightens *wording*, not the grade ledger. |
| **C4** retrieval-readiness | answer-first, self-contained, JSON-LD, static | **PASS** — now strictly answer-first (1a fixed); 2 JSON-LD blocks re-validated; exactly 1 `<h1>`; 85 130 B ≤ 300 KB; ~766 DOM nodes ≤ 3000; 51 in-page/section links intact. |
| **§6-R.3** answer-first | page + section lead = entity + value + grade | **PASS** — page answer and abstract both now open on the engine and its result; grade vocabulary retained. |
| **§8** word-count / no grade upgrade | body words within ±0.5 %; grades not upgraded | **PASS** — the only edit touching `<main>` prose is **word-count-neutral** (26↔26 tokens); all other edits are in word-count-excluded zones; **no grade upgraded**. |
| **anti-invention (반작문)** | every abstract/description number exists in body | **PASS** — re-verified token-by-token; the abstract introduces no number absent from §1–§13. |

---

## 4. Drift-zero proof (the discipline held)

The governed pin was recomputed **after** the edits, exactly as `verify_all.governed_files()` defines it
(every `.py` and `.json` under `code/`), and diffed against the package's frozen baseline
`expected_sha256.json`: **87 files frozen, 87 live — changed 0, missing 0, extra 0 → drift 0.** A full
recursive tree diff against the input archive shows the **only** two differing files are
`docs/dna/index.html` and `docs/dna/_meta.json` — both non-governed, both on the editable surface. No
`code/*.py`, no `code/*.json`, no measured γ / Carnegie-stage table, no equation, and no dated session
record (`gate.json` / `CHANGELOG` / `HANDOFF` / `LEDGER`) was touched. The no-tuning / add-only /
bit-for-bit invariant is intact: a green `verify_all.py` still certifies that the released numbers
reproduce and nothing measured was silently edited.

---

## 5. Scope boundary (named, not fabricated)

**The Phase 7 morphogen length-scale result is validated in the repro layer and pinned by the emergence
gates, but it is deliberately *not* surfaced as a body claim — and the abstract does not claim it.** Doing
so would require *adding* new body prose and new numbers to §1–§13 / appendix-A, which is (a) outside the
§6-D / §13 editable surface and (b) an *addition of claims*, not a C0 *correction of wrong content*. The
calibrated abstract is therefore restricted to the engine's existing, graded §1–§13 content (which is also
what keeps it anti-invention-clean). Promoting Phase 7 into the narrative is a full-body editing lane —
named here as a known boundary, not papered over, and not fabricated into the abstract.

The single-paper lane boundary from the prior closeout still holds: site-level common files
(`docs/index.html`, `sitemap.xml`, `robots.txt`, `llms.txt`) are intentionally absent and belong to the
full-site Phase 5/6 assembly, not this single-paper package.

---

## 6. Out-of-scope observations (reported, not edited — §1 "report bugs, don't rewrite tools")

1. **`verify_all.py` docstring undercount.** The module docstring narrates "three" emergence gates while
   `EMERGENCE_GATES` lists **five** (heart, organs, trajectory, organs_wide, morphogen). This is stale
   prose *inside governed code* — correcting it would perturb the bit-for-bit pin, so per §1 it is
   **reported, not edited**. The executable list, the gate count, and the live 20/20 are all correct; only
   the comment lags.
2. **Grade vocabulary convention.** The manifest/claim-strip uses the paper's **domain** grades
   (`admissible` / `principle-demonstration` / `open`) rendered through VP-SPEC's generic grade classes
   (e.g. a `g-forced` class carrying the label `admissible`). This is the paper's documented convention,
   consistent throughout; noted for cross-paper alignment, intentionally left unchanged.
3. **`_meta.json` totals vs `manifest/dna.csv`** measure different scopes (the closeout §6 residual);
   build-time reconciled, not a drift, and untouched here.

---

## 7. Deliverable

- **Package:** `dna_vp_site_INTEGRATED_v1_9_1_FINAL_abstract_calibrated.zip`
- **Contents:** the full input package with **two non-governed files calibrated**
  (`docs/dna/index.html`, `docs/dna/_meta.json`) and this report added at the root. Bytecode artifacts
  excluded.
- **Single-entry verification:** `python3 verify_all.py` → **OVERALL: PASS (20/20 checks)** (unchanged;
  gene-clock 5/5 and Phase-7 morphogen 8/8 re-run live this session).
- **Governed pin:** 87 files, **drift 0** — re-confirmed post-edit against the frozen `expected_sha256.json`.
- **Tree diff vs input:** exactly 2 files differ, both intended, both editable-surface.
- **DOI of record:** `10.5281/zenodo.20471407` maintained (registry · `_meta.json` · canonical HTML
  agree). This is a documentation/claim-surface living-version snapshot; science version v12.4.
- A fresh `.sha256` sidecar accompanies the finalized archive.

— closeout (VP-SPEC v1.8 · abstract / claim calibration) —
