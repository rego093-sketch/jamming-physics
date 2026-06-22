# vp_nose_emergence_seed — v0.7.1  (research SEED + published HTML volume, deposited)

A self-contained, verifiable starting package for **theoretical, non-clinical** research into how the
sense of **smell (olfaction)** emerges from first principles — the inherited **R19 jamming-lattice
switch** + **DNA γ** measured from public NCBI promoter sequences. The sibling of the eye/ear
emergence seeds. Open scholarship under VP-SPEC v1.8 (CC BY 4.0; ORCID 0009-0002-7535-8245).

> **Not a medical device.** This studies *structure and mechanism* only. It does **not** diagnose,
> treat, screen, or prescribe; it designs no molecule and states no dose or efficacy; every disease
> section is **direction-only / proposal-only** (`FIREWALL.md`). The felt percept is the mind volume's.

## The one idea — and why smell is different
A special sense is *a stimulus property → a code → an R19 transduction switch*. Vision and hearing
read a **wave** as a single **physical place** (propagation angle χ / basilar-membrane position).
**Smell has no wave** — the stimulus is a **molecule** — so identity is a **combinatorial pattern**
over a large olfactory-receptor repertoire (Buck & Axel): each odorant lights a subset of receptors,
each receptor answers to many odorants.
- **What survives:** the **R19 transduction switch** — the olfactory CNG channel, the *same gene
  family* as rod vision (CNGB1 is literally the same gene).
- **What changes:** the front-end key — which odorant binds which receptor — is **molecular
  recognition** (the receptor binding pocket), which the promoter γ does **not** encode. A named [O].
- **The honest negative:** vision's "what" (colour) IS a substrate quantity (angle χ); smell's "what"
  (odour) is **NOT**. The framework reaches smell's **threshold + transduction** layers, not its
  odorant-identity layer — and says so plainly.

## Verify everything (one command, offline)

    python3 tools/verify_seed.py        # → SEED VERIFY: PASS

[1] no-regression (inherited artifacts byte-identical to the frozen seed) · [2] theory reproduces
(foundation modules deterministic, 2×sha256) · [3] DNA reading recomputes offline — γ (LEVEL) + A4
(SHAPE) — bit-for-bit against the atlas, A4 orthogonality per gene, no network · [4] no-omission
(every promised artifact present) · [5] **volume reproduces** (the published HTML in `docs/nose/` is
drift-checked — the numeric SSOT is deterministic and every displayed number comes from it, HTML↔code
drift exactly 0). Per-increment gates (each `… GATE: PASS`), plus the focused volume gate:
`research/E1-combinatorial-code/gate_E1.py`, `research/E2-transduction-switch/gate_E2.py`,
`research/E3-bulb-map/gate_E3.py`, `research/E4-congenital-anosmia/gate_E4.py`,
`research/E5-allergic-smell-loss/gate_E5.py`, `tools/gate_volume.py` (`VOLUME GATE: PASS`).

## What's inside
- **Inherited foundation (frozen, byte-identical to the eye seed):**
  - `inherited/vp_substrate.py` — the R19 bistable switch (ds/dt = γ·s − s³ + h; spinodal=(2/3√3)γ^1.5).
  - `inherited/dna_interpreter.py`, `inherited/key_pipeline_full.py`, `inherited/gamma_pipeline.py`,
    `inherited/vp_dna_reading.py` — the canonical DNA reading: γ (LEVEL) + A4 coordinate (SHAPE), DNA v1.13.
  - **No wave/angle module** — smell has none; that absence is the honest structural statement.
  - `inherited/nose_promoters.cache.json` + `inherited/organ_gamma.json` — **20 measured** olfactory
    master-gene promoters (NCBI, GRCh38), γ (LEVEL) + A4 (SHAPE), cached so the reading reproduces
    offline bit-for-bit. γ measured, never fitted. (PROKR2, PROK2 added at v0.6.0; OR2W1 added at
    v0.6.1 to complete the OR panel; DATA hashes re-frozen, `_to_measure` now empty.)
  - `inherited/FROZEN_SHA256.json` — the no-regression hash set.
- **Research base (built):**
  - `research/E1-combinatorial-code/run.py` — **E1, BUILT (v0.4.0):** each OR an R19 switch;
    spinodal(γ) sets the threshold order; capacity 2^N ≫ N; uniform-drive **thermometer** readout
    (substrate-derived) vs the full richness needing the ligand **[O]**; the honest negative (smell's
    "what" is not a substrate quantity). Deterministic; in the verifier's foundation list.
  - `research/E1-combinatorial-code/gate_E1.py` — the focused E1 gate (`E1 GATE: PASS`).
  - `research/E2-transduction-switch/run.py` — **E2, BUILT (v0.4.0):** the olfactory cascade ends in
    the all-or-none R19 flip (discontinuous past spinodal); the cubic −s³ (n=3) is necessary (≈229×
    steeper than a graded control); **cross-sense CNGB1** byte-identical to rod vision (the shared
    switch); CNG subunits read by (γ, A4). Deterministic; in the verifier's foundation list.
  - `research/E2-transduction-switch/gate_E2.py` — the focused E2 gate (`E2 GATE: PASS`).
  - `research/E3-bulb-map/run.py` — **E3, BUILT (v0.6.0):** OSN-identity organisers (LHX2, EBF1,
    EMX2) emerge as R19 `Organ`s in spinodal(γ) order (EBF1 first; "parts present ≠ trait" enforced);
    one-OR→one-glomerulus convergence is a **bijection**, so capacity **2^N = 128 is preserved** (the
    measured OR panel is N=7) and
    E1's thermometer becomes a nested spatial thermometer; the targeting **coordinate**
    (Neuropilin-1/Sema3A axon guidance) is the honest **[O]** — same KIND of gap as E1's odorant key.
    Deterministic; in the verifier's foundation list.
  - `research/E3-bulb-map/gate_E3.py` — the focused E3 gate (`E3 GATE: PASS`).
  - `research/E4-congenital-anosmia/run.py` — **E4, BUILT (v0.6.0) — the goal:** theoretical /
    non-clinical, **direction-only / proposal-only**. Two disjoint R19 failure modes (6 genes):
    **channelopathy** (CNGA2, CNGB1 — deleting the cubic destroys the flip, ≈229× shallower) and
    **organ-formation** (Kallmann ANOS1, FGFR1, PROKR2, PROK2 — the `Organ` never clears presence),
    each an inverse-lever **direction only** (no dose/molecule/efficacy). Cross-sense: CNGB1 LOF
    predicted to impair **both smell and rod vision** (forced, γ byte-identical). Deterministic; in
    the verifier's foundation list.
  - `research/E4-congenital-anosmia/gate_E4.py` — the focused E4 gate (`E4 GATE: PASS`).
  - `research/E5-allergic-smell-loss/run.py` — **E5, BUILT (v0.6.2) — the acquired disease layer:**
    theoretical / non-clinical, **direction-only / proposal-only**. Allergic rhinitis is an **immune**
    disease, so its mechanism (sensitization · latch · desensitization) is **consumed from immune/
    hematologic §11** (DOI 10.5281/zenodo.20755280 [V]) — **cited, not re-derived**; the absolute
    aeroallergen/airway scale is the **respiratory volume's [O]**. E5 owns only the olfactory
    **consequence**, told apart by **restoring the drive**: **conductive** loss = a reversible drive
    suppression (κ↓) on the intact E1/E2 switches (γ untouched → recovers); **sensorineural** loss = a
    persistent OSN `Organ` degradation on E2/E3 (the acquired form of E4's organ-formation failure → no κ
    rescues). Adds **no gene** (frozen DATA untouched). Deterministic; in the verifier's foundation list.
  - `research/E5-allergic-smell-loss/gate_E5.py` — the focused E5 gate (`E5 GATE: PASS`).
- **Published volume (built + deposited, v0.7.1 — VP-SPEC v1.8 §6):**
  - `tools/vp_nose_ssot.py` — the numeric **single source of truth**: imports the frozen substrate +
    reads `organ_gamma.json`, recomputes (same methods as the E1–E5 increments) **every number the
    volume displays**, returns them as formatted strings, and prints JSON + sha256. Deterministic
    (2×sha256). This is the only place display numbers come from.
  - `tools/build_volume.py` — builds `docs/` from that SSOT. A number can enter the HTML **only**
    through `num(key)` (which emits a `data-key` span), so **HTML↔code drift is 0 by construction**;
    prose is hand-written, numbers are never hard-coded. Writes the hub + 6 chapters + sitemap / robots /
    llms.txt / external CSS.
  - `tools/gate_volume.py` — the focused volume gate (`VOLUME GATE: PASS`): G1 SSOT determinism · G2
    drift = 0 (every shown number re-checked against the SSOT) · G3 chapter structure · G4 firewall
    (both disease chapters carry the non-clinical direction-only banner; E5 cites immune §11) · G5 no
    KaTeX residue · G6 access layer · G7 self-contained locked-quantity cards · G8 the volume's own
    concept DOI present (hub text + `CreativeWorkSeries` identifier, `_meta.json`, `llms.txt`, every chapter).
  - `docs/nose/` — the volume: an `index.html` hub (`CreativeWorkSeries`) + 6 chapters
    (`00-inherited-foundation` … `05-allergic-smell-loss`), `_meta.json`, and the shared
    `docs/sitemap.xml` / `docs/robots.txt` / `docs/llms.txt` / `docs/assets/css/site.css`. **Deposited:**
    the volume carries its own Zenodo **concept DOI 10.5281/zenodo.20790182** (always resolves to the
    latest version) — shown on the hub (visible cite line + `citation_doi` meta + `CreativeWorkSeries`
    JSON-LD identifier), in every chapter's claim-strip and footer, in `_meta.json`, and in `llms.txt`.
    Cross-volume DOIs in the per-claim cards remain the real sources they cite.
- **Tools:** `tools/verify_seed.py` (the one-command gate), `tools/fetch_promoter_gamma.py` (the NCBI
  γ fetcher this seed ships with — add a gene during research, then re-freeze its hash).
- **Governance:** `BLUEPRINT.md` (the plan; E0–E5 built, the HTML volume built **and deposited** with
  its concept DOI — next is the unified-site merge),
  `FIREWALL.md` (binding boundaries — clause 2: γ is **not** odorant-receptor specificity; clause 8: the allergy mechanism is the immune volume's, cited not re-derived),
  `INHERITANCE_LEDGER.md`, `COMPLETENESS_MANIFEST.md`, `WORK_HANDOVER.md`, `VP_SPEC_v1_8.md`, `VERSION`.

## Version
**v0.7.1** — the published volume, **now deposited** with its own Zenodo **concept DOI
10.5281/zenodo.20790182** (always the latest version). The science and every displayed number are
**byte-identical to v0.7.0** — **E0 foundation + E1 (combinatorial code) + E2 (transduction switch) +
E3 (bulb map) + E4 (congenital anosmia) + E5 (allergic smell loss), on 20 measured genes**, rendered as
`docs/nose/` (a `CreativeWorkSeries` hub + 6 chapters) where every number is emitted from one
deterministic SSOT (`tools/vp_nose_ssot.py`) through `tools/build_volume.py`, so the volume gate measures
**HTML↔code drift = 0** (262 displayed numbers, 0 mismatch). v0.7.1 wires the volume's concept DOI into
the hub (visible cite line + `citation_doi` + `CreativeWorkSeries` identifier), every chapter
claim-strip/footer, `_meta.json`, and `llms.txt`; the volume gate gains **G8 (volume DOI present)**. Both
disease chapters keep the non-clinical direction-only banner; E5 still cites immune §11 (DOI
10.5281/zenodo.20755280); the odorant-identity key stays **[O]**. Verified end-to-end by
`tools/verify_seed.py` [1]–[5] + all five increment gates + `tools/gate_volume.py` (G1–G8).
`BLUEPRINT.md` → next is the **unified-site merge**.

## Rules that never bend
γ measured, never fitted · γ is promoter structure, **never** a ligand affinity/occupancy/rate/percept
· the odorant-identity layer is an honest **[O]** · grade honestly [F]/[V]/[L]/[O] · inherited
artifacts stay byte-frozen (no-regression) · every promised artifact present (no-omission) · disease
sections proposal-only · the allergy mechanism is **cited (immune §11), never re-derived** · determinism by 2×sha256 · **output is always one zip.**
