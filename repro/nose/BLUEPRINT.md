# BLUEPRINT (청사진) — vp_nose_emergence_seed

## Scope & Safety — theoretical research, NON-CLINICAL (read first, above all tasks)

This program is **purely academic, theoretical computational research** — it is **not** a medical
product, **not** clinical or diagnostic software, and **not** medical advice. It studies how the
sense of **smell** emerges from first principles (the inherited R19 switch substrate + DNA γ measured
from public NCBI promoter sequences) and the **mechanism layer** of congenital olfactory conditions
(congenital anosmia, Kallmann syndrome) as a question in **physics and dynamical-systems theory** —
the R19 switch, the combinatorial code, the emergence order — graded honestly [F]/[V]/[L]/[O].

What this program studies is **structure only**. What it deliberately does **NOT** do (binding,
enforced by `FIREWALL.md`): it does **not** diagnose, treat, prescribe, screen, or triage; it
designs **no** molecule and states **no** dose, potency, selectivity, efficacy, or clinical effect;
**every disease section is direction-only and proposal-only**. The felt percept is deferred to the
mind volume. Nothing here is intended for, or usable as, patient care or clinical decision-making.

**Purpose & value.** Open scholarship (CC BY 4.0, ORCID 0009-0002-7535-8245, governed by VP-SPEC
v1.8) toward a first-principles **theoretical understanding** of how smell emerges and how congenital
mechanisms fail — and, just as importantly, **an honest map of where the VP wave/substrate framework
reaches and where it stops**. This is upstream basic research that may one day *inform* future
scientific work, never substitute for it.

**Goal.** Properly emerge the **nose (olfaction)** from the inherited R19 substrate and measured DNA
γ — as far as the substrate honestly reaches — ending at the disease layer: a **congenital ANOSMIA**
mechanism (E4) and the **acquired** allergic smell-loss consequence (E5; mechanism cited to the immune
volume, not re-derived).

## The organising insight — and why smell BREAKS the sibling skeleton (read this first)

The sibling senses (eye, ear) share one skeleton:
> A special sense is **a WAVE property → a single PHYSICAL place → an R19 transduction switch**, and a
> congenital sensory disease is **that switch failing to flip**. Vision: colour ← propagation **angle**.
> Hearing: pitch ← basilar-membrane **place**.

**Smell does not fit this.** The stimulus is a **molecule**, not a wave; there is no angle and no
single place. So the front-end code is replaced — honestly, not forced — by a **combinatorial code**:
each odorant activates a SUBSET of a large olfactory-receptor (OR) repertoire, each OR responds to
many odorants, and identity is the **pattern** over the bank (Buck & Axel). The honest consequences,
which this seed makes explicit rather than hiding:
- **What survives** is the **R19 transduction switch** — the olfactory CNG channel, literally the
  same gene family as rod vision's CNG (CNGB1 is the *same gene*). The back end is genuinely shared.
- **What changes** is the front end: identity is combinatorial, and its KEY — which odorant drives
  which receptor — is **molecular recognition** (the receptor binding pocket), which the promoter γ
  does **not** encode. That is a named **[O]**, the volume's central honest negative.
- **The contrast**: vision's "what" (colour) IS a substrate quantity (angle χ); smell's "what"
  (odour) is **NOT** a substrate quantity. The framework reaches smell's threshold and transduction
  layers, not its odorant-identity layer.

## Research increments (the plan)

**E0 — inherited foundation (DONE; verified in this seed).**
- The shared **R19 bistable switch** (`vp_substrate.py`, ds/dt = γ·s − s³ + h; spinodal = (2/3√3)γ^1.5)
  and the canonical **DNA reading** — γ (LEVEL) + A4 coordinate (SHAPE), DNA v1.13 — are inherited
  byte-identical and frozen. **No wave/angle module is inherited** (smell has no wave) — itself a
  meaningful structural statement; the universal that carries over is the switch, not a wave law.
- **20 olfactory master genes** are read from NCBI promoters as γ (LEVEL) + A4 (SHAPE): the
  transduction cascade (GNAL, ADCY3, CNGA2, CNGA4, CNGB1, ANO2), seven representative ORs (OR1D2,
  OR2J3, OR2W1, OR5AN1, OR6A2, OR51E2, OR7D4), the OSN-identity TFs (LHX2, EBF1, EMX2), and four
  congenital-anosmia genes (ANOS1, FGFR1, PROKR2, PROK2 — the Kallmann pair folded in at E4/v0.6.0;
  OR2W1 folded in at v0.6.1 to complete the OR panel). γ measured, never fitted; recomputed offline
  bit-for-bit by the verifier.

**E1 — the combinatorial code (DONE; built v0.4.0, `research/E1-combinatorial-code/run.py`).**
- Each OR is an inherited R19 switch; the MEASURED γ sets the **threshold order** (spinodal(γ),
  lowest γ most trigger-happy) — the *only* thing γ supplies here. [F]/[L]
- The identity code is **combinatorial**: a bank of N all-or-none switches has up to **2^N ≫ N**
  patterns (why the genome carries hundreds of OR genes). A uniform drive yields a substrate-derived
  **thermometer** readout (≤ N+1 nested patterns); the full combinatorial richness needs an
  odorant-specific **drive VECTOR** — the ligand match, which is **NOT in γ** ([O], binding pocket). [F]/[V]/[O]
- **The honest negative**: smell's identity is **not** a substrate quantity. The OR genes have
  distinct (γ, A4) readings, but that is expression structure, never odorant tuning. [F]/[O]

**E2 — the transduction switch (DONE; built v0.4.0, `research/E2-transduction-switch/run.py`).**
- The olfactory cascade (odorant → OR → Golf/GNAL → ADCY3/cAMP → CNG channel → ANO2) ends in the same
  **all-or-none R19 flip** as vision: the FROZEN field settled from rest flips DISCONTINUOUSLY past
  each gene's spinodal (dark below, snaps on above, finite jump ≈+2.2). [V]
- The cooperativity **IS the cubic −s³** (order n=3) and is necessary — delete it → graded (≈229×
  steeper across the fold). [F]/[V]
- **Cross-sense**: CNGB1 (CNG β) is the *same gene* in rod vision and olfaction — its measured γ is
  byte-identical to the rod-vision sibling. The transduction switch is **shared, not analogous**. [V]
- The absolute odorant→drive→firing (Hz) scale is a named [O] (same calibration gap as vision).

> **Scope reminder (applies to the disease tasks below):** every increment — including the
> congenital-anosmia layer — is **theoretical, non-clinical** analysis only, **direction-only /
> proposal-only** under `FIREWALL.md`. No diagnosis, treatment, dose, or efficacy is produced.

**E3 — the bulb map (DONE; built v0.6.0, `research/E3-bulb-map/run.py`).** Smell's substitute for the
sibling "spatial image": olfactory-receptor axons of the same OR converge onto specific **glomeruli**
in the olfactory bulb, turning the receptor-space combinatorial code (E1) into a spatial **odour map**.
- **PART A** — the OSN-identity organisers (LHX2, EBF1, EMX2) emerge as R19 `Organ`s in **spinodal(γ)
  order** (monotone in measured γ; EBF1 clears first), and "parts present ≠ trait" is enforced
  (Organ absent below 0.9·h*, present above 1.1·h*). [F]/[V]
- **PART B** — one-OR→one-glomerulus convergence is a **bijection**, so the combinatorial capacity
  **2^N = 128 is preserved** under the map (N=7 OR panel; full subset lattice → 128 distinct spatial
  images), and
  E1's nested thermometer carries over to a **nested spatial thermometer** (4 patterns, ≤ N+1 = 7,
  chains preserved). [F]/[V]
- **PART C** — the honest **[O]**: the targeting **COORDINATE** (which glomerulus an OR maps to) is
  axon-guidance chemistry (OR → cAMP → Neuropilin-1/Sema3A gradient), **not** in γ — the *same KIND*
  of gap as E1's odorant key. The map's ORDER/capacity is forced; its absolute coordinates are [O]. [F]/[O]

**E4 — congenital ANOSMIA (DONE; built v0.6.0 — the goal, `research/E4-congenital-anosmia/run.py`).**
Theoretical / non-clinical, **direction-only / proposal-only** with a prominent scope banner. Two R19
failure modes, separated cleanly (disjoint gene sets, 6 genes total):
- **(1) CHANNELOPATHY** (CNGA2, CNGB1) — a **transduction-switch failure**: WT flips past h*, but
  striking out the cubic (a local linear control) destroys the flip (≈229× shallower) → no
  transduction. Inverse-lever **DIRECTION only** (sign +, "re-enable the flip"; no dose/molecule/efficacy). [F]/[V]
- **(2) ORGAN-FORMATION** (Kallmann: ANOS1, FGFR1, PROKR2, PROK2 — all **measured**) — the R19
  `Organ` never clears the presence threshold (absent @0.9·h*, present @1.1·h*) → OSN/bulb never
  emerges → the anosmia + hypogonadotropic-hypogonadism signature. Inverse-lever **DIRECTION only**. [F]/[V]
- **PART B cross-sense** — CNGB1's measured γ = 1.4357 is **byte-identical** to rod vision, so CNGB1
  LOF is predicted to impair **both smell and rod (dim-light) vision** — forced, not analogy. [V]
- **PART C firewall-in-action** — no diagnosis/dose/molecule/efficacy; the odorant key stays [O]; the
  felt percept of smell is deferred to the **mind** volume. [F]/[O]
- **PROKR2, PROK2** were **fetched from NCBI and folded into the cache+atlas at v0.6.0** (measured,
  not invented); the cache/atlas DATA hashes were re-frozen and the verifier re-confirmed bit-for-bit.

**E5 — allergic (ACQUIRED) smell loss (DONE; built v0.6.2, `research/E5-allergic-smell-loss/run.py`).**
Theoretical / non-clinical, **direction-only / proposal-only** with a prominent scope banner. The
**acquired** disease layer — the sibling of E4's **congenital** anosmia, and the most common real-world
nose complaint: **allergic rhinitis** (Type-2 airway inflammation) and how it takes your **smell**. The
honest point is that allergic rhinitis is **not** primarily an olfactory disease — it is an **immune**
hypersensitivity — so its mechanism is **consumed, not re-derived**:
- **Consumed, not re-derived (one-way cite, `FIREWALL.md` #8):** the allergic **mechanism**
  (sensitization at the R19 spinodal, the dose×repetition threshold, the **latch**, controlled
  **desensitization** = allergen immunotherapy = basin-acting re-tolerization) is the **immune/
  hematologic volume's §11**, graded **[V]** there (**DOI 10.5281/zenodo.20755280**). E5 computes none of
  it. The **absolute** airway aeroallergen/mucosal scale is the **respiratory volume's [O]** (deferred to
  the surface owner, exactly as the immune volume does).
- **Owned here — the olfactory consequence (what no other volume can state):** allergic rhinitis takes
  smell two ways, told apart by **one move — restore the drive**:
  - **(A) CONDUCTIVE** loss = a **drive suppression** (κ↓) on the **intact** E1/E2 switches (mucosal
    swelling reduces odorant flux; the OR panel flips OFF in spinodal(γ) order, E1's thermometer in
    reverse). γ untouched → **restoring κ→1 recovers the percept EXACTLY**. **Reversible.** [F]/[V]
  - **(B) SENSORINEURAL** loss = an **organ degradation** on E2/E3 (chronic inflammation drops the OSN
    compartment's master cis-drive below its γ-set R19 **presence** threshold; "parts present ≠ trait")
    → no receptor carries a percept **regardless of κ** — the **same** organ-formation failure as E4,
    reached by inflammation, not a mutation. **Persistent.** [F]/[V]
  - **(C) the discriminator + firewall-in-action:** restoring the drive recovers conductive but not
    sensorineural; the substrate expresses the clinical split as **DRIVE (E1/E2) vs ORGAN (E2/E3)**.
    Direction-only levers (sign only): conductive → κ↑ (restore access; upstream cause = immune §11
    desensitization, cited); sensorineural → act on the **organ**, recovery not guaranteed. No
    dose/molecule/efficacy; the odorant key stays E1's [O]; the felt percept → mind volume. [F]/[O]
- E5 adds **no gene** (no new γ; the two frozen DATA files are untouched — no-regression). κ and the
  organ degradation are **abstract structural representations** (κ is not a measured airway value; the
  organ loss is the inherited `Organ` presence mechanism), never fitted.

## What is forced vs measured vs open (grading discipline, VP-SPEC C3)
- **[F] forced / [V] verified:** the R19 switch structure; the all-or-none flip past spinodal(γ);
  the cubic (n=3) cooperativity; the combinatorial capacity 2^N; the threshold/thermometer readout;
  the DNA reading γ (LEVEL) + A4 (SHAPE) with orthogonality A4 = signal − γ; the cross-sense CNGB1.
- **[L] measured/calibrated:** every γ (from NCBI); the cited rod-vision CNGB1 cross-reference.
- **[O] open:** **the odorant→receptor specificity** (binding-pocket chemistry — the combinatorial
  code's key); the glomerular targeting specificity (E3); the absolute odorant→firing (Hz) scale;
  **the allergy mechanism + the absolute aeroallergen/airway scale (E5 — cited to the immune §11 and
  respiratory volumes, not re-derived/owned here)**; the felt percept (→ mind volume). Each [O] names
  its obstacle in the research ledger.

## Definition of done for the FULL volume — **MET + DEPOSITED (v0.7.1)**
A multi-chapter HTML volume (VP-SPEC v1.8 §6) where every displayed number is reproduced
deterministically (2×sha256, HTML↔code drift 0), every γ is measured-and-cached, the disease layer
is proposal-only under the firewall, the odorant-identity [O] is named throughout, and `verify_*`
passes — delivered as **one zip**.

**Status: built, checked, and deposited.** `docs/nose/` ships a `CreativeWorkSeries` hub + 6 chapters
(§0–§5). A single numeric source of truth (`tools/vp_nose_ssot.py`, deterministic 2×sha256) feeds
`tools/build_volume.py`, which lets a number enter HTML **only** through `num()`; the focused gate
(`tools/gate_volume.py`, also run as `verify_seed.py` [5]) measures **HTML↔code drift = 0** across 262
displayed numbers, asserts each chapter's structure, the non-clinical direction-only banner on both
disease chapters (§4, §5), the E5→immune-§11 citation, and the access layer (sitemap/robots/llms).
**The volume now carries its own Zenodo concept DOI 10.5281/zenodo.20790182** (always the latest version),
wired into the hub (visible cite line + `citation_doi` meta + `CreativeWorkSeries` JSON-LD identifier),
every chapter's claim-strip and footer, `_meta.json`, and `llms.txt`; the gate's **G8** asserts it is
present everywhere. A concept DOI (not a version DOI) is used so the canonical link always points to the
newest deposit. Cross-volume DOIs in the per-claim cards remain the real sources they cite.

### Next milestone — site merge (does not change the science)
**Site merge** — fold `docs/nose/` into the unified `jamming-physics.org` tree (top-level index +
framework map + root sitemap), link it from the framework map by its new DOI, and re-submit to Search
Console. On each future re-deposit, the LaTeX/PDF whitepaper should be rendered **from the same SSOT
numbers** (PDF and HTML agree by construction) and uploaded as a new version under the **same concept
DOI** — the pages need no DOI edit because the concept DOI already resolves to the latest version.
The odorant-identity key stays **[O]**; publishing changes presentation, not the honest negatives.
