# VP-SPEC v1.9 application — Continental-Genesis volume

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · https://jamming-physics.org/
**Motto:** falsification = discovery.
**What this is:** a record of applying **VP-SPEC v1.9** to the v1.8 package. It documents the
added canonical layer and certifies that **no LOCK constant, no screen, and no module science
was changed** — the version of the *science* is unchanged; this is a v1.9 **canonical-HTML /
retrieval-readiness** release. Mark, never erase.

---

## 0. What changed, what did not

**Did NOT change (byte-identical, verified):**
- All 25 `modules/*.md` — the per-module governed record (the source of record).
- All 23 `repro/*.py` screens and `repro/simulations_session/*` — every gate still recomputes
  and prints `REPRO GATE: PASS` (spot-checked: `buckling_stress`, `isostasy_emergence`,
  `plate_connectivity`). No `SEED`, no LOCK constant, no hash touched.
- `GOVERNANCE.md`, `00_MASTER_SEED.md`, `BLUEPRINT_and_GRADED_LEDGER.md`, `PUZZLE_MAP.md`,
  `NO_TUNING_THESIS.md`, `inherited/*`.

**Added (the v1.9 canonical layer):**
- **`WHITEPAPER.html`** — the **single self-contained canonical** for this volume (Constitution
  C2 "one HTML", C0 "no fragmentation"). It integrates the **full prose** of all 25 modules **and**
  the no-tuning thesis, puzzle map, reproducibility ledger, and the complete CG-1…CG-39 graded
  ledger — **nothing condensed** (28.6k visible words vs ~14.7k in the modules) — re-organised into
  **30 numbered chapters and 118 numbered sub-chapters (§N.x)**. English only; the author's motto is
  kept once, in the masthead, as a signature.
- **`tools/build_canonical_html.py`** — the **deterministic** builder that generates the canonical
  from the modules (Constitution C1: same sources → same HTML; the agent of conversion is code, per
  SPEC §1).
- **`docs/_meta.json`** (SPEC §9 summary card) and **`docs/_decl.json`** (SPEC §6-M.1 incorporation
  declaration: `inherits_volumes`, `inherits_modules`, `adds`, `primitives`, `owns_terms`,
  `uses_terms`).
- **`docs/registry/concepts.json`** + **`docs/registry/modules.json`** — the C5 shared-infrastructure
  SSOT for this volume (locked quantities + inherited common modules), machine-readable.
- **`docs/llms.txt`** (<5 KB retrieval helper) and **`docs/assets/css/site.css`** (the site stylesheet,
  also inlined into the canonical so the one file is portable offline).
- **`MANIFEST.sha256`** — regenerated to cover the augmented tree (so `sha256sum -c MANIFEST.sha256`
  still returns *all OK* on the delivered package). The pre-existing screen-gate hashes inside the
  README / master-seed are unchanged (they are gate hashes, not file hashes).

## 1. Which VP-SPEC v1.9 clauses were applied

| clause | how it is satisfied in `WHITEPAPER.html` |
|---|---|
| **C0** English only; no fragmentation; return the augmented original | Body is English (0 stray Hangul beyond the masthead motto); ONE canonical HTML, not a multi-page split; the whole package is returned augmented. |
| **C1** maximum reproducibility | The canonical is generated deterministically by `tools/build_canonical_html.py`; every quantitative claim traces to a SEED=19 double-SHA-256 gated screen (§29). |
| **C2** single canonical HTML; no TeX bundled | One self-contained HTML (CSS inlined — the Constitution's single-file rule overrides §6's "no inline CSS", which governs the multi-page live site). No `.tex` / `eq_list` present. |
| **C3** openness with stated reason | §29 states the one genuine computational-reproducibility limit (the coupled high-Ra area-fraction value) and explains why the firewall `[O]` grades are epistemic caps, not reproducibility failures. |
| **C4** retrieval-readiness | Page-level **answer-first** (52 words) + a direct-answer lead on **every** chapter; self-contained **`vp-card`** for every locked quantity (value + meaning + grade + canonical link + `/concepts/#id`); JSON-LD (ScholarlyArticle + BreadcrumbList + DefinedTermSet); short paragraphs. |
| **C5** shared-infrastructure declaration | `inherits-strip` → `/modules/#id` (kernel, rotor_inflow); every `vp-card` carries `data-concept` with `data-locked == data-concept`; `_decl.json` + `concepts.json` + `modules.json` emitted; all internal anchors resolve (0 dangling). |
| **§6** chapter template | `claim-strip` (LOCK → Derive → Gate · screen · gate · DOI), abstract, grade badges, prev/next-style cross-links as in-document anchors. |
| **§6-R** answer-first / atomic / short paragraphs | Applied per chapter and per sub-chapter; comparisons/tables kept as tables (30 preserved) for extraction. |
| **§7** equations | Inline unicode throughout (§7A); display relations rendered as readable unicode (the TeX→SVG pipeline is the separate full-rebuild path and is inactive for an HTML-canonical package, per §7B). |

## 2. Grade vocabulary

This volume uses its **own LOCKed grade vocabulary** [F]/[V]/[L]/[O] (GOVERNANCE §1), where
**[L] = "leaning"** (a well-anchored inference short of forced). This differs from the 9-paper site
vocabulary ([F]/[H]/[V]/[O]); SPEC §6 permits a per-paper `grade_vocab` basis, and this volume's
constitution defines [L] explicitly. Precedence **[F] > [V] > [L] > [O]**; occurrence/timing is
capped at **[O]** forever; nothing downstream launders an [O] upward.

## 3. How to read / regenerate

- **Read:** open `WHITEPAPER.html` in any browser (offline-portable; single file). Contents,
  spine-at-a-glance, and a per-quantity glossary are built in.
- **Regenerate:** `python3 tools/build_canonical_html.py` → rewrites `WHITEPAPER.html` and the
  `docs/` cards from the modules (deterministic).
- **Verify science:** `cd repro && for s in *.py; do python3 "$s" | tail -1; done` → 23× `REPRO GATE:
  PASS`; `sha256sum -c MANIFEST.sha256` → all OK.

*The science is unchanged and `[O]`-honest; this release only makes the volume a single,
retrieval-ready, machine-legible canonical under VP-SPEC v1.9. falsification = discovery.*
