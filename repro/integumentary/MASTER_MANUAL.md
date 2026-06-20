# MASTER MANUAL — `integumentary_vp_site` v1.0.0

**Author:** Young Jae Lee (ORCID 0009-0002-7535-8245) · **paper_id:** `integumentary_vp_site` ·
**code:** `skn` · **branch:** jamming (barrier/interface + external insult) ·
**governance:** VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`; constitution C0 overrides on conflict).

This manual is the operating reference for the package: what it is, how it is built, how to reproduce it
bit-for-bit, how to extend it without breaking the no-tuning discipline, and what its boundaries are. For
the bootstrap a new session needs only `START_HERE.md` → `CHARTER.md`; this manual is the deeper reference,
and `COMPLETION_LEDGER.md` is the SSOT for *what is done*.

---

## 1 · What this package is

It emerges the **skin (integumentary) organs by simulation and circulates their dynamics**, at the level
of physical **mechanism** (felt experience is the `mind` package's lane). Organ *identity* and
*developmental order* are owned by the DNA morphogenesis gene-clock and **cited** here (measured γ, never
fitted). Every result is derived from the shared **R19 bistable substrate** (FHN-class, vendored) and the
measured master-gene γ under a strict **no-tuning rule**, is **bit-reproducible** to a fixed SHA-256, and
is **graded** `F`/`V`/`L`/`O` with every open item carrying a stated obstacle.

The organising physics is **jamming**: barriers, interfaces and bonds that snap between states at spinodal
thresholds, with hysteresis where the system has memory. The skin is the body's boundary, so its diseases
are largely boundary-failure dynamics (barrier collapse, occlusion, de-adhesion, vasomotor lock) plus the
cleanest external-insult carcinogenesis case (UV).

## 2 · Architecture (file map)

```
integumentary_vp_site/
├── START_HERE.md            entry point (read first)
├── CHARTER.md               scope, organs, seams, targets, governance (read second)
├── MASTER_MANUAL.md         this file (operating reference)
├── COMPLETION_LEDGER.md     SSOT: what is done, on what evidence, what remains
├── HANDOVER.md              session-to-session handover (read third)
├── HANDOFF_NEXT_STEPS.md    detailed disease-coverage + next-steps rationale
├── ANCHORS_VERIFIED.md      v1.0.0 network verification of the cited [L] anchors
├── PATHOLOGY_FINDINGS.md    research narrative for the disease layers
├── IRREPRODUCIBILITY_LEDGER.md   every [O] open item + its obstacle
├── VP_SPEC_v1_8.md          governance spec (full text)
├── VERSION                  1.0.0
├── PHASE                    writing
├── inherited/               vendored DNA γ atlas + R19 substrate (read-only inputs)
│   ├── organ_gamma.json     measured γ (TP63/KRT14/MITF/EDAR/PRDM1); _to_measure now empty
│   ├── organ_promoters.cache.json   cached promoter sequences (γ reproduces offline)
│   ├── organ_identity.md
│   └── vp_substrate.py      FHN/R19 primitive
├── repro/                   the reproducible engine + additive layers (each its own hash)
│   ├── _engine/             core T1–T5 dynamics  ── DO NOT EDIT when adding content
│   ├── _oncology/           UV-carcinogenesis kernel ── DO NOT EDIT when adding content
│   ├── _verify/             gates.py (writing lock + research gate) ── DO NOT EDIT when adding content
│   ├── _pathology/          13-disease layer + 5-way discriminant
│   ├── _cycle/              T6 hair-cycle oscillator + 4 alopecias
│   ├── _seb/                T7 sebaceous-duct jam + acne + HS
│   ├── _adhesion/           T8 binding jam + pemphigus + BP
│   ├── _vasomotor/          T9 reactivity jam + rosacea + Raynaud
│   ├── _seam/               cross-package seam manifest (reads layers, alters none)
│   ├── run_all.py           core battery (gates writing)
│   ├── run_pathology.py / run_cycle.py / run_seb.py / run_adhesion.py / run_vasomotor.py / run_seam.py
│   ├── run_release_audit.py v1.0.0 consolidation gate (re-runs all; asserts frozen hashes)
│   └── REPRODUCE.md
├── reports/                 machine-readable results (per layer) + release_audit.json + seam_manifest.json
├── docs/                    CANONICAL artifact: per-title HTML (C4) + hub + _meta.json + sitemap/robots/llms
├── manifest/                file manifest (csv)
└── tools/build_docs.py      HTML generator (reads VERSION; refuses while writing is locked)
```

## 3 · How to reproduce (commands)

```
cd integumentary_vp_site
python repro/run_all.py            # core T1–T5 + oncology; all targets pass; writing unlocked; sha 1fb59f…
python repro/run_pathology.py      # 13 diseases + 5-way discriminant + 2×sha256;  sha 0a4404…
python repro/run_cycle.py          # hair-cycle oscillator + 4 alopecias + 3-way; sha d910fa…
python repro/run_seb.py            # sebaceous-duct jam + acne + HS + 3-way;        sha 1e8a55…
python repro/run_adhesion.py       # binding jam + pemphigus + BP + 3-axis;         sha 55dce8…
python repro/run_vasomotor.py      # reactivity jam + rosacea + Raynaud + 3-axis;   sha 53a99f…
python repro/run_seam.py           # seam manifest (RR 2.58/10.59/1.13) + 4 checks; sha 52b49a…
python repro/run_release_audit.py  # v1.0.0: re-runs all of the above; asserts every sha; writes release_audit.json
python tools/build_docs.py         # regenerate the 14 HTML sections + hub (writing must be unlocked)
```

Each runner prints `2×sha256 identical: True` (VP-SPEC C1 determinism, two independent processes). The
seven hashes are the **evidence of record**; `run_release_audit.py` checks them all at once.

## 4 · The grading system (VP-SPEC)

- **`[V]`** — a **simulation-verified shape**: a qualitative/relational result that the engine produces
  deterministically (e.g. "discontinuous collapse at the spinodal", "anagen-dominant waveform",
  "Nikolsky sign follows from which compartment failed"). Never fitted to data.
- **`[L]`** — a **cited literature anchor**: an external empirical fact the model is *consistent with*,
  recorded with a source (see `ANCHORS_VERIFIED.md`). The model is not tuned to hit it.
- **`[F]`** — a **regime-scale set-point**: a dimensionless threshold that locates a regime (e.g. an
  occlusion set-point) without claiming an absolute physical value.
- **`[O]`** — an **absolute magnitude left open**, with the obstacle stated (e.g. converting a
  dimensionless TEWL to g·m⁻²·h⁻¹ needs SC lipid permeability + water-activity gradient as cited inputs).
  Every `[O]` is logged in `IRREPRODUCIBILITY_LEDGER.md`.

The discipline that makes the grades meaningful is **no-tuning**: every constant is a measured input or a
derived value, never chosen to hit a target. PRDM1's γ was the last measured input added (v0.6.0,
fetched + cached + vendored); `_to_measure` is now empty.

## 5 · How to extend (the mechanism-first, no-tuning recipe)

To add a disease that the package cannot yet model, **never bolt it onto an unrelated knob**. The order is:

1. **Add the new target** — a new mechanism on an organ. Two valid patterns:
   - *new target on an existing measured organ* (the hair-cycle T6, adhesion T8, vasomotor T9 pattern):
     reuse an already-measured γ; **fetch nothing, fit nothing**.
   - *new measured organ* (the sebaceous T7 pattern): fetch the master gene's γ from NCBI through the
     identical promoter-ΔG pipeline (`fetch_morpho_gamma`), cache it so it reproduces offline, vendor it;
     **never fit it**.
2. **Give the target its own stress suite + gate** (`repro/_<target>/<target>_verify.py` →
   `<target>_gate()`) and a runner with its **own** 2×sha256 hash. Verify it green.
3. **Only then** add the disease(s) as **signed perturbations** of that target, each intervention = the
   drive reversed, separated by an opposite-property **discriminant**. Record `[O]` magnitudes as open.

**Invariant (CHARTER):** additions are **additive**. Do **not** touch `repro/_engine`,
`repro/_oncology`, or `repro/_verify` when adding pathology/doc content, and re-confirm the core
`run_all.py` hash is unchanged before packaging. Each new layer carries its own hash; the core hash and
every prior layer hash must stay byte-identical.

## 6 · Physical-class boundary (why these organs are one package; what is out)

Decomposition is by **physical regime / coupling topology**, not textbook organ-system labels. This is the
**jamming (barrier/interface + external insult)** class. Anything outside it belongs to a sibling package
and is reached **only** through cited seam variables (SSOT), never re-emerged here:

- **Seams IN (inherited):** circulatory dermal perfusion (cited); DNA organ identity + emergence order
  `[V]`; R19 substrate (vendored).
- **Seams OUT (this package is SSOT):** barrier integrity + thermoregulation interface (systemic boundary).
- **Out of class entirely:** single-gene genodermatoses (→ `disease_wp`, gene-key); immune-effector
  dermatoses (urticaria, lichen planus → `immune_hematologic`); pathogen-driven infections.

The full labelled record of every interface is the **seam manifest** (`repro/_seam/`, §4 of the ledger).

## 7 · Writing phase (VP-SPEC v1.8, C-clauses)

- **HTML is canonical** (C2). `docs/<slug>/index.html`, one page per title (C4): answer-first
  `<p class="answer">` (40–60 words), self-contained, JSON-LD (`ScholarlyArticle` + `BreadcrumbList`),
  `canonical`, a claim-strip (grade + reproduce link + concept DOI, also wired into the JSON-LD via
  `sameAs`), and one vp-card per cited
  `[L]` anchor.
- **Body in English** (C0), tables/figures included. Every quantitative result deterministically
  regenerated (C1, 2×sha256). Every `[O]` states its obstacle (C3).
- Outputs: `docs/<slug>/index.html` + `docs/index.html` (hub) + `_meta.json` + `sitemap.xml` +
  `robots.txt` (bots allowed) + `llms.txt`.
- The writing gate (`tools/build_docs.py`) **refuses** while `gates.writing_locked()` is True; it unlocks
  only when `research_gate` is `all_green`, `gates.write_research_complete()` has run, and `PHASE` is
  `writing`. All three currently hold.

## 8 · Governance invariants (the short list)

1. **No tuning.** Every constant is measured or derived. (`_to_measure` empty; no constant fitted.)
2. **Bit-for-bit determinism.** 2×sha256 identical across processes; seven frozen hashes.
3. **Additive layers.** Engine/oncology/gates frozen when adding content; each layer its own hash.
4. **Honest grading.** `F`/`V`/`L`/`O`; every `[O]` has an obstacle; "name it, don't hide it".
5. **Single deliverable + auto-handover.** One zip; `START_HERE` → `CHARTER` is the whole bootstrap;
   state passes by files only; the next session resumes from the single zip.

## 9 · Provenance / publication

- Series: **VP Theory — Jammed-Granular-Vacuum Emergence**, published at `jamming-physics.org`.
- License: CC BY 4.0 (series convention). Author ORCID 0009-0002-7535-8245.
- DOI: concept DOI **10.5281/zenodo.20754541** (Zenodo, minted 2026-06-19) is stamped into the claim-strip,
  the per-page JSON-LD (`sameAs`), and `docs/_meta.json`; the per-version DOI for v1.0.0 is
  **10.5281/zenodo.20754542**. Minting/stamping a DOI is a deposit-time action, not a code change — the
  seven frozen result hashes are unaffected (re-verified 7/7 by `run_release_audit.py`).
