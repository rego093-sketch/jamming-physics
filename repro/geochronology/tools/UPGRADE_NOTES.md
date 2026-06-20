# UPGRADE NOTES — geochronology · VP-SPEC v1.6 → v1.8

**Paper:** Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit
**paper_id:** `geochronology` · **code:** `chr` · **DOI:** 10.5281/zenodo.20568673
**Upgrade date:** 2026-06-15 (fixed constant → deterministic `dateModified`)
**Verdict:** PASS (see `reports/phase1-2-geochronology.gate.json`)

---

## 1. What changed (v1.6 → v1.8)

v1.8 keeps every v1.6 guarantee and adds the **C4 "retrieval-readiness"** layer
(plus the v1.7 grade-span and constitution gates). All edits were confined to
**gate-excluded zones** so that the body word count, equations, figures, tables,
and numeric content of all 14 chapters are **unchanged** (verified byte-identical).

| Area | v1.6 state | v1.8 upgrade | Zone |
|------|------------|--------------|------|
| **Answer-first** | absent | `<p class="answer">` injected as the first content block after each `<h1>` (14 chapters + hub). 40–60 words, self-contained: entity + value/conclusion, no dangling cross-ref. | excluded |
| **vp-card** | absent | `<aside class="vp-card">` for the single locked derived quantity `N_D = Dτ/L² ≡ Fo`, on the two chapters that cite it downstream (§5, §6). Carries value + meaning + grade + link to the canonical derivation. | excluded |
| **Derivation anchor** | none | `id="fo"` added to the §4 closure-number figure (`chr-04-001.svg`) so vp-cards can deep-link to the canonical derivation. | attribute |
| **Grade span (v1.7)** | absent | `<span class="grade g-…">[X] …</span>` injected as the first child of each `.claim-strip`, where the page grade = most-frequent body epistemic token (tie → F>I>A). Chapters with no tokens (§5, §13, §14) get no span. | excluded |
| **JSON-LD (6-R.4)** | basic | Chapter `<head>` rebuilt to `ScholarlyArticle` with `isPartOf` → `CreativeWorkSeries`, plus `identifier` (DOI), `datePublished`, `dateModified`, `isBasedOn` (repro URL), `author.sameAs` (ORCID), `license`, `knowsAbout[]`. Hub rebuilt to `CreativeWorkSeries` with `hasPart` (14 chapters). `BreadcrumbList` on every page. | head |
| **Hub meta description** | truncated mid-word ("…prot") | repaired to a complete ≤160-char description. | head |
| **`_meta.json` grade** | all `null` | filled with computed per-chapter grades; agrees with the rendered claim-strip spans (0 mismatch). | sidecar |

Per-chapter grade map (most-frequent body token):

```
01 F   02 F   03 I   04 I   05 –   06 F   07 F
08 F   09 F   10 F   11 F   12 F   13 –   14 –
```

Corpus epistemic census: **[F]=26, [I]=13, [A]=8, [O]=0**. Because there are no
`[O]` items, constitution **C3** is satisfied trivially; see
`IRREPRODUCIBILITY_LEDGER.md`.

## 2. Body invariance (how 0-drift is guaranteed)

The v1.6 word counter excluded only `.abstract` and `.claim-strip`. The v1.8
counter (`tools/vp_v18_gate.py::count_words`) additionally excludes `.answer`
and `.vp-card`. Since the original bodies contained neither, the recomputed count
equals the **manifest value exactly** — the gate asserts `==` (0 drift), not the
v1.6 `±0.5%` tolerance. Manifest numbers were **not** edited.

Independent check: stripping the injected `.answer`, `.vp-card`, grade `<span>`,
the `id="fo"` attribute, the rebuilt JSON-LD, and the repaired head meta, the
remaining prose of all 15 documents is **byte-identical** to the pre-upgrade
backup (`docs__bak/`).

## 3. Deviation from the canonical pipeline (disclosed)

The canonical VP build kit (`build/sections_data.py`, `generate.py`, `common.py`,
`render_eq.mjs`) is the body/TeX single-source-of-truth and lives under `build/`
and `src/`. Those directories are **Phase-0/derivation inputs**, not
distribution artifacts. Per constitution **C2** (the canonical material is HTML;
TeX/SSOT must not ship), the upgrade was implemented as an **additive,
deterministic post-processor over the canonical HTML** (`tools/`), rather than by
re-running the generator. This mirrors the precedent already set in
`build/BUILD_NOTES.md`, where the Phase-0 kit was absent and re-implemented
in-tree.

Consequence for packaging: the distribution zip **excludes** `src/` (TeX) and
`build/` (body/TeX SSOT + `render_eq.mjs`). Nothing canonical is lost — the five
source PNGs are byte-identical duplicates already present in
`docs/geochronology/img/` (sha256-verified), and the rendered equation SVGs ship
under `docs/eq/geochronology/`.

## 4. The v1.8 tools kit (ships in `tools/`)

| File | Role | Determinism |
|------|------|-------------|
| `answers.py` | authored answer-first text (14 + hub), the `N_D≡Fo` vp-card, and the slug list that receives it. Every numeric token also appears in the corresponding body. | static data |
| `vp_v18_upgrade.py` | the post-processor: injects answer-first, grade span, vp-card, `id="fo"`, and rebuilds JSON-LD. `UPGRADE_DATE`/`PUB_YEAR` are fixed constants (no clock/RNG) → re-runnable to an identical result. | deterministic |
| `vp_v18_gate.py` | strict **superset** of `build/gate.py`: all v1.6/v1.7 checks + the v1.8 C4 checks (answer-first, vp-card, JSON-LD 6-R.4, grade span) + constitution C1/C2/C3. Recomputes from written files; imports nothing from `build/`, so it runs standalone inside the shipped kit. | independent |

Re-run end to end:

```
python3 tools/vp_v18_upgrade.py     # idempotent re-application to docs/
python3 tools/vp_v18_gate.py        # writes reports/…gate.json, prints PASS
```

## 5. Known soft warnings (non-fatal)

The gate emits 30 soft warnings for body paragraphs exceeding the §6-R "≤3
sentences" guidance. These are pre-existing in the author's prose and are **left
untouched** to preserve byte-level body invariance; §6-R marks this rule *soft*,
so they do not affect the verdict.
