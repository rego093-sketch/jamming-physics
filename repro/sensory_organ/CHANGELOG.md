# CHANGELOG — Special-Sense Organs (sensory_organ_vp_site)

Governed by VP-SPEC v1.8. Versions encode phase: `-research` (corpus + gates green) → `-writing`
(canonical HTML generated) → `-published` (concept DOI assigned; Zenodo-deposit PDF/TeX shipped). Every
quantity is a measured input or a derived value (no tuning); results are bit-for-bit reproducible
(2×sha256 identical). Concept DOI: 10.5281/zenodo.20755154.

## v0.4.0-published — concept DOI assigned; PDF + TeX deposit artifacts
**Phase:** published (PHASE=`published`). Research remains green; **no science changed, no new `[O]`** — the
concept DOI was wired into the generator and the canonical HTML re-rendered, and a deterministic LaTeX/PDF
whitepaper was generated from the same verified corpus (2×sha256 `6a68bc48…`).

- **Concept DOI `10.5281/zenodo.20755154` assigned.** Wired into the generator (not hand-edited into
  `docs/`): `_sns_render.py` gained `DOI`/`DOI_URL`, and the `DOI: TBD` placeholders in the claim-strip,
  footer, landing, `llms.txt`, and `_meta.json` were replaced with the live DOI; the chapter JSON-LD
  `ScholarlyArticle` gained `identifier` + `sameAs` (= the DOI URL) and the series `identifier`. `docs/`
  re-renders deterministically (byte-identical across two runs) with **0 FAIL / 0 WARN** and **0 `TBD`
  remaining**. The dead `.doi-tbd` CSS rule was repurposed to the now-active `.doi` link.
- **Deterministic PDF + TeX whitepaper** (`dist/sensory_organ_vp_site.{tex,pdf}`). New generator
  `tools/build_tex.py` renders the LaTeX from the **same** `_sns_content` prose-as-data and the **same**
  verified numbers that build the HTML — so the PDF cannot drift from the site (every quantity injected,
  none re-typed). 18 pages: title page with the VP-SPEC *Living version* line (hub URL + concept DOI) and a
  locked-quantity results table, grading-discipline page, then the twelve chapters with answer-first boxes,
  vp-cards, tables, and the references chapter. Fonts are scalable Type-1 (Times/Helvetica/Courier) so the
  PDF text is selectable/searchable. `tools/build_pdf.sh` compiles reproducibly (SOURCE_DATE_EPOCH +
  `\pdfinfoomitdate`/`\pdftrailerid`): the PDF is **byte-identical across independent compiles**
  (sha256 `c6593c81…`); the `.tex` is byte-identical on regeneration (sha256 `6e76c5dd…`).
- **Phase gate extended, safety-preserving.** `gates.writing_locked()` now unlocks for PHASE ∈
  {`writing`, `published`} — `published` is a strict superset of `writing` (research must still be signed
  off, `research_complete.json` all_green), so the generators run under the publication phase without
  weakening any gate.
- **No new `[O]`.** Publication renders/derives only from the verified corpus; the open-items table is
  unchanged. **No hard edits to `docs/`** — every change is in the generators and re-rendered (VP-SPEC C2).

## v0.3.1-writing — canonical HTML expanded, depth + provenance + retrieval/SEO
**Phase:** writing (PHASE=`writing`). Research remains green; **no science changed, no new `[O]`** — the
generator was extended and re-run, every number still loaded from the verified corpus (2×sha256 `6a68bc48…`).
Canonical `docs/` rebuilds **byte-identical** (tree `cd2ef245…`); search/SEO gate **0 FAIL / 0 WARN**.

- **Two new chapters** (10 → **12**). **§2 _Deterministic emergence: the no-tuning method_** makes the
  grounding explicit — what γ is (SantaLucia nearest-neighbour ΔG37 over the real human promoter, never
  fitted), the no-tuning discipline, LOCK→Derive→Gate, bit-for-bit reproducibility, and the grading
  vocabulary as the falsifiability mechanism. **§12 _References, gene accessions & methods provenance_**
  surfaces the literature registry: 5 master genes (NCBI), 10 transducer-channel genes (NCBI/UniProt), the
  classical optics / tonotopy / gating-spring / Hopf / canal references, and the 2023–2026 treatment
  literature, each at its grade (attribution only, paraphrased).
- **Every chapter deepened.** Body 2,329 → **4,375 words** (+88%); each topic page is now a self-contained
  landing page with question-style `<h2>` subheads (engine gained `h2`/`h3` block types + an `h3` CSS rule).
- **DNA-emergence foregrounded** on the hub, landing, and llms.txt: the organs **emerge** from measured
  human-DNA stacking stiffness γ (argsort gives the developmental order, taste-latest confirmed) — framed as
  a grounded, falsifiable derivation, not an illustrative simulation. Added a headline result for it.
- **Self-deprecating phrasing removed; honest grades retained.** Apologetic framings ("recorded honestly
  rather than forced", "honestly [L]-pending") rewritten as precise, deliberate scope statements; the
  [V]/[L]/[O]/[H] vocabulary and every stated obstacle are unchanged. The "Scope & honesty" block is now
  "Scope and grading discipline".
- **Retrieval/SEO.** JSON-LD `ScholarlyArticle` gained `keywords`, `name`, `inLanguage`, `abstract`,
  `publisher`; per-chapter SEO keyword sets added. Title/description derivation unchanged (§6-D). All 12
  answer-first blocks within 40–60 words; 73/73 internal cross-references resolve (cross-refs are slug links,
  number-independent); 0 double-escaped entities; `llms.txt` 4.08 KB (<5 KB); `sitemap.xml` 14 URLs.
- **No hard edits to `docs/`** — all changes are in the generator and re-rendered (VP-SPEC C2; "code is the
  agent"). Slugs renumbered (pre-publication, allowed); manifest + `_meta.json` regenerated to 12 rows.

## v0.3.0-writing — canonical HTML whitepaper built
**Phase:** writing (PHASE=`writing`). Research remains green; no science changed.

- **Generator implemented** (`tools/build_docs.py` was a lock-guarded stub; now the real WRITING-phase
  generator). "Code is the agent" (VP-SPEC §1): split into a deterministic rendering engine
  (`tools/_sns_render.py`) + authored chapter prose-as-data (`tools/_sns_content.py`); every number is
  loaded from the verified corpus (`reports/emergence_results.json`) and injected — none hand-typed.
- **Ten chapters** generated under `docs/sensory-organs/<slug>/index.html`: 01 organ emergence from
  measured γ · 02 unified R19 transducer · 03 phototransduction (rod CNG) · 04 ocular optics /
  accommodation · 05 cochlear tonotopy (Greenwood) · 06 cochlear Hopf amplifier (cube-root, exp 1/3) ·
  07 vestibular canal (torsion pendulum) · 08 chemodetection (taste / olfaction) · 09 disease as
  quadratic basin collapse · 10 root-cause treatment (inverse substrate). Body 2,329 words.
- **Hub + landing + access layer:** `sensory-organs/index.html` (scope, headline results, reproduction,
  grade legend), `docs/index.html`, `robots.txt` (7 AI/search bots Allow), `sitemap.xml` (12 URLs),
  `llms.txt` (3.2 KB < 5 KB), `llms-full.txt`, `_meta.json` (registry-ready paper card).
- **VP-SPEC §6 conformance:** each page is answer-first (40–60 words), with JSON-LD ScholarlyArticle +
  BreadcrumbList (+ ORCID `sameAs`), canonical link, claim-strip (grade + Reproduce + DOI: TBD), and
  vp-cards restating each locked quantity self-containedly. Title/description derived deterministically
  (§6-D: `subj45` ≤45 chars, description clamped to ≤160). Math is inline Unicode (no display SVG →
  `eq_display=0`, no orphan-SVG risk).
- **Determinism (C1):** BUILD_DATE fixed (no wall-clock); `docs/` rebuilds byte-identical. Search/SEO
  gate: **0 FAIL / 0 WARN**.
- **DOI honesty (C0):** DOI is TBD on publication, so it is omitted from links/JSON-LD rather than emitted
  broken; claim-strip and footer show "DOI: TBD".
- **No new `[O]`:** the writing phase renders the verified corpus only; the open-items table is unchanged.

## v0.2.0-research — research signed off (molecular layer + amplifier + treatment + literature)
**Phase:** research, green & locked (staged handoff — PHASE held at `research`).

- Six organ nodes emerge from measured DNA stiffness γ (PAX6 1.511, RAX 1.4541, EYA1 1.3638, SOX2 1.4573,
  TAS1R3 1.5555; vestibular balance diffuse, no master gene); developmental order = argsort(γ), broad
  signal "taste latest" validated [V], fine early-node order honest [L].
- **Unified molecular transducer [V]:** every special-sense channel is an R19 bistable switch (rod CNG,
  hair-cell MET, taste T1R→TRPM5; olfaction shares the rod CNG superfamily) — bistability + discontinuous
  flip + hysteresis, cooperative slopes ≈3.1–3.3. Effector-channel γ deferred to the DNA pipeline (SSOT).
- **Cochlear Hopf amplifier [V]:** at criticality (μ=0) response R=(F/β)^(1/3), parameter-free cube-root
  (exp 0.3333); small-signal gain rises 1 → 10 → 99 → 464 as μ→0. Active force = prestin (SLC26A5).
- **Classical organ instruments [V-arith]:** reduced-eye axial 22.27 mm, 2.69 D/mm, presbyopia 1 D@60;
  Greenwood place-map ~20 Hz–21 kHz; canal velocity-band flatness 0.018, VOR gain ~1.0.
- **Disease law [V] / [O]:** setpoint drift = quadratic basin collapse, barrier (g²/4)(1−d)², Kramers rate;
  seven non-rare eye/ear diseases mapped (shapes [V], absolute rates [O], needs noise scale D).
- **Root-cause treatment [V-structure] / [L]:** therapy = inverse substrate operation (five inverse ops,
  seven diseases); restoration demo recovers 73% of basin depth. Contested/partial results flagged
  (AMD complement: no functional acuity gain yet; cataract reversal: replication failed; ATOH1: immature).
- Literature registry (`literature/CITATIONS.md` + `citations.json`); gate suite RS1–RS5 PASS; determinism
  2×sha256 identical (`6a68bc48…`).
