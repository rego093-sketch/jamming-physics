# WORK_HANDOVER — vp_nose_emergence_seed (research SEED + published volume, deposited, v0.7.1)

## One command re-establishes the entire trusted state
From the package root:

    python3 tools/verify_seed.py        # → SEED VERIFY: PASS

This asserts, in order: [1] **no-regression** (every inherited artifact byte-identical to
`inherited/FROZEN_SHA256.json`), [2] **theory reproduces** (each foundation module runs clean and is
deterministic — identical sha256 twice), [3] **DNA reading recomputes offline** — γ (LEVEL) **and**
A4 (SHAPE) — from the cached promoter bytes, bit-for-bit against the atlas, with A4 orthogonality
|mean(shape)|≈0 per gene, **no network**, [4] **no-omission** (every promised artifact present), and
[5] **volume reproduces** (the published HTML volume in `docs/nose/` is drift-checked by its own gate —
the numeric SSOT is deterministic and every displayed number comes from it, HTML↔code drift exactly 0).
Per-increment gates (each prints `… GATE: PASS`, exit 0), plus the focused volume gate:

    python3 research/E1-combinatorial-code/gate_E1.py
    python3 research/E2-transduction-switch/gate_E2.py
    python3 research/E3-bulb-map/gate_E3.py
    python3 research/E4-congenital-anosmia/gate_E4.py
    python3 research/E5-allergic-smell-loss/gate_E5.py
    python3 tools/gate_volume.py            # → VOLUME GATE: PASS

To rebuild the volume from the verified base (numbers re-sourced from the SSOT; never hand-typed):

    python3 tools/build_volume.py           # writes docs/ ; then gate_volume.py re-checks drift=0

## What this seed is (and is not)
This is the **nose (olfaction)** sibling of the eye/ear emergence seeds — a self-contained,
verifiable package for **theoretical, non-clinical** research into how smell emerges from the
inherited R19 substrate + measured DNA γ. It ships at **v0.7.1**: **E0 (foundation) + E1 + E2 + E3 +
E4 + E5 all built and verified** — the full research backbone, from the combinatorial code through the
bulb map to the disease layer: **congenital** anosmia (E4) and **acquired** allergic smell loss (E5,
whose immune mechanism is cited to the immune volume, not re-derived) — **now published as the full
multi-chapter HTML volume** (`docs/nose/`, VP-SPEC v1.8 §6: 1 hub + 6 chapters, HTML↔code drift 0). It
does **not** diagnose, treat, or prescribe; every disease section is direction-only / proposal-only
under `FIREWALL.md`; the felt percept is the mind volume's.

## The one idea (and why smell is different)
A special sense is *a stimulus property → a code → an R19 transduction switch*. Vision/hearing: the
stimulus is a **wave**, the code is a single **physical place** (angle / membrane position). **Smell
has no wave** — the stimulus is a molecule — so the code is **combinatorial** over a large receptor
repertoire (a pattern over many R19 switches). **What survives** is the R19 transduction switch (the
olfactory CNG channel, literally the same gene family as rod vision). **What changes** is the front
end: identity's key — which odorant binds which receptor — is **molecular recognition**, NOT in the
promoter γ. That is the named **[O]** and the seed's central honest negative: the framework reaches
smell's **threshold + transduction** layers, **not** its odorant-identity layer.

## Current trusted state (v0.7.1)
- **E0 foundation (frozen):** R19 switch + DNA reading (γ LEVEL + A4 SHAPE) inherited byte-identical
  from the eye seed (same hashes); **no wave module inherited** (smell has none). **20 olfactory
  master genes** measured from NCBI promoters (γ never fitted; offline-reproducible): transduction
  (GNAL, ADCY3, CNGA2, CNGA4, CNGB1, ANO2), ORs (OR1D2, OR2J3, **OR2W1**, OR5AN1, OR6A2, OR51E2,
  OR7D4), identity TFs (LHX2, EBF1, EMX2), congenital-anosmia (ANOS1, FGFR1, PROKR2, PROK2). The cache
  and atlas DATA hashes were re-frozen at v0.6.0 (PROKR2/PROK2) and again at v0.6.1 (OR2W1, completing
  the OR panel; `_to_measure` now empty); the verifier re-confirms all 20 bit-for-bit.
- **E1 — combinatorial code (DONE):** each OR an R19 switch; spinodal(γ) sets the threshold order;
  capacity 2^N ≫ N; uniform-drive thermometer readout (substrate-derived) vs the full richness that
  needs the ligand vector [O]; honest negative — smell's "what" is not a substrate quantity.
- **E2 — transduction switch (DONE):** all-or-none flip past spinodal(γ); the cubic (n=3) necessary
  (≈229× steeper than a graded control); **cross-sense CNGB1** byte-identical to rod vision (the
  shared switch); CNG subunits γ-separable.
- **E3 — bulb map (DONE):** OSN-identity organisers (LHX2, EBF1, EMX2) emerge as R19 `Organ`s in
  spinodal(γ) order (EBF1 first; "parts present ≠ trait" enforced); one-OR→one-glomerulus convergence
  is a **bijection** so capacity **2^N = 128 is preserved** (the OR panel is N=7) and E1's thermometer
  becomes a nested
  spatial thermometer; the targeting **coordinate** (Neuropilin-1/Sema3A axon guidance) is the
  honest **[O]** — same KIND of gap as E1's odorant key.
- **E4 — congenital anosmia (DONE; the goal):** two disjoint R19 failure modes (6 genes) —
  **channelopathy** (CNGA2, CNGB1: deleting the cubic destroys the flip, ≈229× shallower) and
  **organ-formation** (Kallmann ANOS1, FGFR1, PROKR2, PROK2: the `Organ` never clears presence) —
  each an inverse-lever **direction only** (no dose/molecule/efficacy). Cross-sense: CNGB1 LOF
  predicted to impair **both smell and rod vision** (forced, γ byte-identical). Firewall-in-action:
  no diagnosis/dose/molecule; odorant key stays [O]; felt percept → mind volume.
- **E5 — allergic (acquired) smell loss (DONE; the acquired disease layer):** allergic rhinitis is an
  **immune** disease, so its mechanism (sensitization · latch · desensitization) is **consumed from the
  immune/hematologic §11**, DOI 10.5281/zenodo.20755280 [V] — **cited, not re-derived**; the absolute
  aeroallergen/airway scale is the **respiratory volume's [O]**. E5 owns only the olfactory
  **consequence**, told apart by **restoring the drive**: **conductive** loss = a reversible drive
  suppression (κ↓) on the intact E1/E2 switches (γ untouched → recovers at κ=1); **sensorineural** loss =
  a persistent OSN **Organ** degradation on E2/E3 (the acquired form of E4's organ-formation failure →
  no κ rescues). Direction-only; adds **no gene** (frozen DATA untouched).
- **Volume — published HTML (DONE + DEPOSITED; v0.7.1):** the verified E0–E5 base is rendered as a multi-chapter
  volume at `docs/nose/` — a `CreativeWorkSeries` hub + 6 chapters (§0 foundation, §1 code, §2 switch,
  §3 bulb map, §4 congenital, §5 acquired). Every number on every page is emitted from a single numeric
  source of truth (`tools/vp_nose_ssot.py`, deterministic 2×sha256) via `build_volume.py`'s `num()`, so
  the volume gate measures **HTML↔code drift = 0** (262 displayed numbers, 0 mismatch). Both disease
  chapters carry the non-clinical direction-only scope banner; E5 cites immune §11. Access layer shipped
  (sitemap / robots / llms.txt / external CSS). **The volume carries its own Zenodo concept DOI
  `10.5281/zenodo.20790182`** (always the latest version) on the hub (cite line + `citation_doi` +
  `CreativeWorkSeries` identifier), every chapter claim-strip/footer, `_meta.json`, and `llms.txt`.
  Checked by `tools/gate_volume.py` (**G1–G8**, G8 = volume DOI present) and `verify_seed.py` [5].

## Next session (start here)
The full multi-chapter HTML volume is **built, drift-checked, and deposited** (`docs/nose/`, VOLUME GATE:
PASS incl. G8, HTML↔code drift 0; concept DOI `10.5281/zenodo.20790182` wired throughout) — the deposit
half of the milestone is **done**. The remaining milestone is the **site merge**:
1. **Site merge** — fold `docs/nose/` into the unified `jamming-physics.org` tree (add the volume to the
   top-level index + the framework map by its DOI, extend the root sitemap), then re-submit to Search
   Console.
2. **On each future re-deposit** — render the LaTeX/PDF whitepaper **from the same SSOT numbers** (PDF and
   HTML agree by construction) and upload it as a new version under the **same concept DOI**. The HTML
   needs **no DOI edit**: a concept DOI already resolves to the newest version. (If a per-version DOI is
   ever wanted on the pages, add it beside the concept DOI in `build_volume.py` — do not replace it.)
3. Re-run `python3 tools/verify_seed.py` (expect **SEED VERIFY: PASS** incl. [5]) before zipping.

The representative gene set is complete (**OR2W1** folded in at v0.6.1, `_to_measure` empty) — there is
no outstanding NCBI fetch. The odorant-identity key stays **[O]**; depositing does not change the science.
Open `BLUEPRINT.md` for the per-chapter map.

## Rules that never bend (see FIREWALL.md / VP_SPEC_v1_8.md)
γ measured, never fitted · γ is promoter structure, **never** a ligand affinity/occupancy/rate/percept
· the odorant-identity layer is [O] · inherited CODE stays byte-frozen permanently; DATA re-frozen
only when genes are added (no-regression) · every promised artifact present (no-omission) · disease
sections proposal-only · determinism by 2×sha256 · **output is always one zip.**
