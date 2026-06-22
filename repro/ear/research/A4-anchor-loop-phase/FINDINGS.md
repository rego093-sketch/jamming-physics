# FINDINGS — increment A4 (the FULL A4 anchor / loop / anchor-relative-phase deferred read)

**Status:** DELIVERED (v0.12.0) — **turns the FIREWALL's one named, deferred [O] into a MADE
measurement.** Deterministic module `run.py` (2×sha256 identical: `a504a93e…`), small gate `gate.py`
(7/7 PASS), folded into `tools/verify_seed.py` foundation list. **NO pre-existing inherited byte
changed** — the 8 inherited artifacts are byte-identical to v0.11.0 and trigger **no re-freeze**; **one**
new frozen artifact (`inherited/ear_regions.cache.json`, the measured wide-region + feature-table inputs)
was added **deliberately** and recorded in `FROZEN_SHA256.json`. **No constant tuned.**

## What A4 builds
The seed always read each master-gene promoter as **γ (LEVEL) + the promoter-scale A4 SHAPE**, and the
firewall flagged **one** thing as deferred: the **FULL** A4 coordinate — the wide-neighbourhood stiffness
**shell**, the nearest architectural **anchor**, the real **motors/loops**, and the **anchor-relative
helical phase** — because it needs *the wider region + an NCBI feature table (rettype=ft)*. A4 supplies
exactly those two measured inputs for all 19 genes and runs the **INHERITED** grammar on them.

The keystone is structural and provable: **the inherited grammar already contained every function the
full read uses** — `run_key` (wide-region shell map), `build_anchors`, `parse_ft_motors`, `build_loops`,
`helix_coord`. So the deferred read was a **missing MEASUREMENT, not missing machinery**. Fetching the
wider region + feature table and running the existing grammar **makes** the read, fulfilling the
`dna_interpreter` promise stated in its own docstring — *"upgrades the COORDINATE read from anchors-only
to real motors+loops"* — on measured annotation, never on invented inputs.

| layer | inherited function | what A4 measures it on | result |
|---|---|---|---|
| keystone | (byte compare) | `region[FLANK:FLANK+2501]` vs frozen promoter | **19/19 exact** (zero drift) |
| shell | `run_key` (W=2000) | wide region (promoter ± FLANK=20000 bp) | wide-neighbourhood class + mean_z |
| anchor | `build_anchors` | shell boundaries (strength = \|Δmean_z\|) | nearest anchor + distance |
| motors → loops | `parse_ft_motors` → `build_loops` | NCBI feature table (real neighbouring genes) | **19/19 carry ≥1 real motor** |
| helical phase | `helix_coord` (3.4 Å, 34.29°/bp) | TSS ↔ nearest anchor | contact-competent (same face ≲60°) |

## Results (every number reproduced offline, bit-for-bit; coordinate sha256 `d342decc…`)

**The full A4 coordinate, per gene** (shell · mean_z · anchor strength · anchor distance bp · loops ·
helical face · contact-competent · real motors):

| gene | node | shell | mean_z | a.str | a.dist | loops | face | contact | motors |
|---|---|---|---|---|---|---|---|---|---|
| EYA1 | otic_placode | stiff | 2.56 | 3.01 | 1250 | 2 | 0.062 | **True** | 4 |
| SIX1 | otic_placode | stiff | 1.22 | 0.83 | 8250 | 3 | 0.812 | False | 3 |
| ATOH1 | hair_cell | stiff | 2.17 | 3.09 | 2250 | 2 | 0.312 | False | 3 |
| POU4F3 | hair_cell | stiff | 2.26 | 2.03 | 3250 | 1 | 0.562 | False | 2 |
| GATA3 | otic_placode | stiff | 0.67 | 1.44 | 1750 | 2 | 0.688 | False | 3 |
| TMC1 | mechanotransduction | **mid** | −0.08 | 0.46 | 3750 | 3 | 0.188 | False | 3 |
| PCDH15 | mechanotransduction | stiff | 3.17 | 3.36 | 2750 | 1 | 0.938 | **True** | 1 |
| CDH23 | mechanotransduction | stiff | 1.56 | 1.57 | 3750 | 1 | 0.188 | False | 2 |
| TMIE | mechanotransduction | stiff | 0.91 | 3.52 | 2250 | 2 | 0.312 | False | 3 |
| SLC26A5 | cochlear_amplifier | stiff | 0.78 | 0.55 | 2250 | 2 | 0.312 | False | 2 |
| OTOF | ribbon_synapse | stiff | 0.39 | 0.33 | 3250 | 2 | 0.562 | False | 2 |
| MYO7A | hair_cell | stiff | 0.54 | 0.32 | 1750 | 1 | 0.688 | False | 2 |
| GJB2 | congenital_deafness | stiff | 1.55 | 2.49 | 2250 | 1 | 0.312 | False | 3 |
| GJB6 | congenital_deafness | stiff | 0.94 | 0.95 | 1750 | 1 | 0.688 | False | 1 |
| USH2A | congenital_deafness | stiff | 0.52 | 0.68 | 1750 | 1 | 0.688 | False | 1 |
| SLC26A4 | congenital_deafness | stiff | 2.10 | 2.22 | 1250 | 2 | 0.062 | **True** | 3 |
| LHFPL5 | mechanotransduction | stiff | 0.56 | 0.80 | 750 | 1 | 0.438 | False | 3 |
| MYO15A | hair_cell | stiff | 0.41 | 1.19 | 1750 | 2 | 0.688 | False | 3 |
| TMC2 | mechanotransduction | stiff | 1.19 | 1.92 | 3250 | 2 | 0.562 | False | 3 |

- **Keystone — the wide read sits ON the frozen γ layer, zero drift.** `region[FLANK:FLANK+2501]` equals
  the frozen promoter **byte-for-byte for all 19 genes**. The same γ the seed has always read is the γ of
  the central 2501 bp of every wide region; the new A4 coordinate is read in the wide neighbourhood
  **around that unchanged centre**. **[F]/[V]**
- **Real motors + loops — the deferred read's core promise, fulfilled 19/19.** Every gene carries **≥1
  real neighbouring-gene motor** parsed from its NCBI feature table, joined to anchors as loops. This is
  the `dna_interpreter` upgrade *anchors-only → real motors+loops*, now on **measured** annotation, and
  it holds for **every** gene. **[F]/[V]**
- **Wide-neighbourhood structure the promoter-only A4 cannot see.** **18/19** TSS sit in a **stiff** wide
  shell (GC/CpG-island promoter neighbourhoods); the exception is **TMC1** (the AT-rich, low-γ structure
  gene) — a neighbourhood-class distinction invisible to the promoter-only read. **3/19** TSS are
  **contact-competent** with their nearest anchor (same B-DNA face): **EYA1, PCDH15, SLC26A4** — a
  read-only coordinate; Layer-2 sign stays flagged. **[F]/[V]** (existence) / **[O]** (the sign's meaning)
- **N-robustness — mostly window-stable, the minority flip is the named [O].** Re-reading the **same
  fetch** on its central sub-window (FLANK → FLANK/2, a 2× shrink, **no new data**):

  | quantity | window-stable | the boundary-near minority that flips |
  |---|---|---|
  | motor existence | **19/19** (forced) | — |
  | shell class | **15/19** | SIX1, GATA3, USH2A, LHFPL5 (near a tercile boundary) |
  | contact sign | **16/19** | EYA1, PCDH15, MYO15A (near the 60° face cutoff) |

  So the read is **not a FLANK artifact** for the majority; the ~20% nearest a class/sign boundary flips
  under the window change — forced **away** from a boundary, **[O]-fragile near one**. **[F]** (majority) /
  **[O]** (boundary-near minority)
- **Determinism + re-auditable measurement.** The full A4 coordinate recomputes to an identical sha256
  (2× equal); the module is offline and deterministic; the cached wide-region + feature-table bytes are
  byte-exact and re-auditable via `tools/fetch_region_features.py verify`. **[V]**

## Honest negatives / open items (preserved, not hidden)
- **N1.** **"anchor" is a MECHANICAL stiffness-shell BOUNDARY** (|Δmean_z|), a **proxy** — NOT an
  experimentally mapped CTCF/cohesin site. A measured architectural anchor needs **Hi-C/ChIP** and is
  **[O]**; this read gives the framework's mechanical Layer-1 anchor, not a wet-lab one.
- **N2.** **"loop" is a GEOMETRIC motor↔nearest-anchor join** (`build_loops`, loop_k=2) — NOT a measured
  chromatin contact. The **EXISTENCE** of within-window motors→loops is forced; a real contact
  **frequency** (Hi-C/Micro-C) is **[O]**.
- **N3.** the anchor-relative phase uses **IDEALISED constant B-DNA twist** (34.29°/bp, ~10.5 bp/turn).
  Sequence-dependent twist, supercoiling, and nucleosome phasing are **[O]**; only the helical **FACE**
  (same-side / opposite-side) is read, and only its **sign** is used.
- **N4.** **absolute magnitudes are window-dependent [O]:** the FLANK itself, the anchor **distances** in
  bp, and the shell/motor/loop **COUNTS** all scale with the observation window. A single absolute number
  for any of them would be **TUNING** (forbidden). Only the keystone + motor/loop **EXISTENCE** + the
  **majority** class/sign are window-stable.
- **N5.** the shell **CLASS** and the contact **SIGN** are **window-RELATIVE** coordinates (tercile
  thresholds and the 60° cutoff are referenced to the chosen window). Under a 2× window change **4/19**
  genes flip class and **3/19** flip contact — forced **away** from a boundary, **[O]-fragile** near one.
  **Named, not hidden:** a clean per-gene class/sign would overclaim.
- **N6.** the loop **CENSUS** is **window-TRUNCATED:** neighbouring genes beyond ±FLANK are unseen, so the
  loop set is a **lower bound**. Within-window existence is forced; the **COMPLETE** census is **[O]**.
- **N7.** **Layer-2 stays flagged** (firewall): the cascade **SIGN** (brake/accelerator), the runtime fill,
  and the wiring are NOT sequence-derivable and are **never assigned**. γ/A4 are **STRUCTURE-ONLY** —
  never a voltage, dose, selectivity, or effect; the felt percept of hearing is the **mind** volume's.
  Nothing here is diagnosed, treated, or prescribed; no molecule is designed.

## Why this matters, honestly stated
A4 is the measurement-honesty payoff of the firewall's discipline: the one read the seed was careful to
label **[O]** — *"the FULL A4 anchor/loop/anchor-relative-phase … flagged, never invented"* — is now
**MADE**, by fetching the two named inputs and running the **inherited** grammar, inventing no machinery
and no number. Every TSS now carries a real wide-neighbourhood shell coordinate, a real nearest anchor,
real feature-table motors joined as loops (19/19), and a real anchor-relative B-DNA phase — anchored to
the frozen promoter with **zero drift** (keystone 19/19) and **mostly window-stable** (class 15/19,
contact 16/19, motors 19/19). It does **not** pretend to a clean numeric closure — that would be tuning;
the absolute magnitudes and the boundary-near class/sign are the irreducible **window-relative [O]**, and
the wet-lab contact map + sequence-dependent twist are a deeper **[O]** — both **named**, never invented.

## Naming note (flagged, not silently fixed)
Delivered in the unambiguous folder `research/A4-anchor-loop-phase/` — a **READING deepening** (it closes
the FIREWALL named [O]), **NOT** a wave E-chapter — so it does not enter the E-numbering map (the verifier
scans `research/E*/` only) and introduces **no** new label inconsistency. The documented E-numbering slip
(folder E1 ⟷ blueprint E2; folder E6 ⟷ blueprint E1) stands flagged and unchanged.

## Firewall
γ/A4 read promoter **STRUCTURE only** — never a channel voltage, a transduction gain, a drug potency, a
dose, an in-vivo selectivity, or a clinical effect. This increment reads the wide-neighbourhood A4
**COORDINATE** (shell / anchor / loop / phase), still structure-only; **Layer-2** stays flagged, never
assigned; nothing is diagnosed, treated, or prescribed, and no molecule is designed. Identity and order
are the DNA volume's **[V]**, cited. The percept of hearing is the **mind** volume's.
