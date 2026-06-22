# INHERITANCE LEDGER (기초 상속자료) — vp_ear_emergence_seed

Every inherited artifact, its frozen sha256, and where it comes from. The verifier asserts each
is **byte-identical** to the hash below (no-regression). Nothing here was re-derived in this seed.

| inherited artifact | sha256 (frozen) | provenance |
|---|---|---|
| `inherited/dna_interpreter.py` | `4929932d90321790…` | canonical A4-grammar (DNA v1.13: γ, switch, helix geometry), byte-identical |
| `inherited/ear_promoters.cache.json` | `621456c0297757b7…` | **19** measured human promoter sequences (NCBI, cached) — re-frozen v0.9.1 (was 18 at v0.5.0, 15 at seed) |
| `inherited/ear_regions.cache.json` | `dc1b151d363431e0…` | **19** measured WIDE genomic regions (promoter ±FLANK=20000 bp) + NCBI feature tables (rettype=ft), cached — the FULL-A4 inputs; **NEW frozen key added v0.12.0** (the 8 others byte-identical) |
| `inherited/gamma_pipeline.py` | `4bde475df52a7a12…` | offline γ recompute (SantaLucia-1998 NN ΔG37) |
| `inherited/key_pipeline_full.py` | `3141fa22cfe34a94…` | canonical A4 region pipeline (shells/anchors/robust_z), byte-identical |
| `inherited/organ_gamma.json` | `f6cd7490d807db07…` | measured readable-layer atlas: γ (level) + A4 (shape) — **19** genes, `_to_measure` EMPTY (complete), re-frozen v0.9.1 (was 18) |
| `inherited/vp_dna_reading.py` | `f5ea1709bf091467…` | the seed reading: γ (LEVEL) + A4 (SHAPE) per promoter |
| `inherited/vp_sound_wave.py` | `87db8cc1671ecdc2…` | sound = √(B/ρ) wave + Greenwood-shape tonotopy (new, derived) |
| `inherited/vp_substrate.py` | `a4bbbb18d564460a…` | R19 switch primitive (sensory_organ/neuro, byte-identical) |

**v0.12.0 — DELIBERATE ADD of one new frozen artifact (회귀금지 — never silent), NO re-freeze of any
existing inherited byte.** Increment **A4** (the FULL A4 anchor/loop/anchor-relative-phase deferred read —
the FIREWALL's one named [O], now MEASURED) needs two inputs the seed never cached: per gene, a **wider
genomic region** and an **NCBI feature table**. Both were **measured, not invented**:
`tools/fetch_region_features.py` fetched, for each of the 19 genes, the frozen promoter window EXTENDED by a
single, **gene-independent FLANK = 20000 bp** each genomic side (rettype=fasta, strand-corrected → a 42501-bp
region) and the feature table over the **same** region (rettype=ft, same strand), and the **keystone** was
verified at fetch time and again offline: `region[FLANK:FLANK+2501]` equals the frozen promoter **byte-for-
byte for all 19 genes** (the wide region literally CONTAINS the unchanged γ window). The raw bytes are cached
in the **new** inherited artifact `inherited/ear_regions.cache.json` (the region sequence + feature table +
per-gene SHA-256 + provenance), and its hash was recorded in `inherited/FROZEN_SHA256.json` as a **NEW key**
(added, never overwriting): 

| file | action | sha256 (v0.12.0) |
|---|---|---|
| `inherited/ear_regions.cache.json` | **ADDED (new frozen key)** | `dc1b151d363431e0…` |

Crucially this is an **ADD, not a re-freeze**: every one of the **8 pre-existing** inherited hashes in the
table above is **byte-identical** to its v0.11.0 value (the verifier's no-regression block now checks **9**
files and confirms all 8 unchanged; A4's gate G3 independently asserts the 8-file set intact AND the new
cache matching). The atlas `_to_measure` is unchanged (still EMPTY). The FULL A4 coordinate (shell / anchor /
motors+loops / B-DNA phase) is recomputed **offline, deterministically** from the cached bytes inside
`research/A4-anchor-loop-phase/run.py` by **importing the inherited grammar** (`dna_interpreter` +
`key_pipeline_full` — `run_key`/`build_anchors`/`parse_ft_motors`/`build_loops`/`helix_coord`): the read
invents **no new machinery** and **no new number**. The measured region/feature-table is **never** used as a
contact frequency, a CTCF occupancy, a dose, a band edge, or any effect (firewall): it yields a
promoter-structure **COORDINATE** only, and Layer-2 stays flagged. The cache is re-auditable against live
NCBI with `python3 tools/fetch_region_features.py verify inherited/ear_regions.cache.json`.


(`docs/`, built by `volume/`) — a publication layer over the existing science, not a change to it.
All **eight** inherited hashes above are **byte-identical** to their v0.9.1 values (the verifier's
no-regression block confirms each). The new numeric single-source-of-truth
`volume/tools/vp_numeric_ssot.py` is registered as a **foundation module** and **reads** the frozen
foundation + verified E-modules — it imports them and calls their own functions to reproduce every
displayed number; it **writes nothing inherited and fits nothing**. The verifier runs it twice and
confirms determinism (canonical sha256 `ee6e681f3828e3aa…`), and `volume/tools/gate_volume.py`
independently asserts HTML↔code drift 0 (81 numbers). Twenty artifacts were added (manifest 48→68); the
no-omission block passes at 68. **Not one inherited byte moved — no re-freeze** (only v0.9.1's deliberate
TMC2 re-freeze stands).

**v0.9.1 DELIBERATE RE-FREEZE (회귀금지 — never silent) — the readable-layer atlas is now COMPLETE.**
The last deferred gene in the atlas `_to_measure` — **TMC2**, the second MET pore-forming subunit
(mechanotransduction node, STRUCTURE class, paralog of TMC1) — was **measured and folded in**. It was
**not** invented: it was fetched by `tools/fetch_promoter_gamma.py` from NCBI nuccore (GRCh38,
TSS−2000..+500, 2501 bp), **two independent live fetches returned byte-identical sequence**
(seq_sha256 `3b806e41acadc441…`), and its γ recomputes offline from the cached bytes bit-for-bit — the
fetcher's `gamma_of` and the canonical `dna_interpreter.gamma` agree to the 4th decimal (γ=1.4160), and
A4 = signal − γ holds (|mean(shape)|=0.0). The two affected inherited artifacts
(`ear_promoters.cache.json`, `organ_gamma.json`) had their hashes re-frozen in
`inherited/FROZEN_SHA256.json` **deliberately** (key deleted, new hash recorded):

| file | old sha256 (v0.5.0) | new sha256 (v0.9.1) |
|---|---|---|
| `inherited/ear_promoters.cache.json` | `7ee8ae5c510e1b54…` | `621456c0297757b7…` |
| `inherited/organ_gamma.json` | `971ee6321bf0a6a1…` | `f6cd7490d807db07…` |

No other inherited artifact moved; the remaining six frozen hashes are byte-identical to seed time
(the verifier's no-regression block confirms). The atlas `_to_measure` is now **EMPTY** — the ear
readable layer is complete at **19** master genes, each carrying γ (LEVEL) + A4 (SHAPE), all MEASURED.
The folded gene:

| gene | γ (measured) | spinodal | accession (GRCh38) | NCBI gene | node | role |
|---|---|---|---|---|---|---|
| `TMC2` | 1.4160 | 0.6485 | NC_000020.11 | 117532 | mechanotransduction | second MET pore-forming subunit — tip-link transduction channel (DFNB-spectrum); STRUCTURE class |

**Read-only observation (no tuning).** In the emergence order = argsort(spinodal(γ)), TMC2 lands at
position **#8/19** (between LHFPL5 and OTOF), well ahead of its paralog **TMC1 at #2/19**. The two
MET-pore subunits differ by **Δγ = +0.1132 / Δspinodal = +0.0761** and carry **opposite A4 skew** (TMC1
soft-skewed, stiff-side 0.449, stiffest at +1875 bp; TMC2 stiff-skewed, stiff-side 0.6122, stiffest at
+2075 bp) — the same family, yet **not interchangeable at the readable layer**: reading γ ALONE would
discard a real structural difference. No constant was fitted; γ is measured, the order is the cubic's
spinodal, and the A4 shape is the inherited grammar's — this fold neither diagnoses, treats, nor
prescribes (firewall intact: TMC2's γ is a promoter-structure LEVEL, never a channel gain or effect).

**v0.5.0 DELIBERATE RE-FREEZE (회귀금지 — never silent).** For increment **E4** (congenital deafness),
three deafness-gene promoters were measured and folded in. They were **not** invented: each was fetched
by `tools/fetch_promoter_gamma.py` from NCBI nuccore (GRCh38, TSS−2000..+500, 2501 bp) and its γ
recomputes offline from the cached bytes bit-for-bit; A4 = signal − γ holds per gene. The two affected
inherited artifacts (`ear_promoters.cache.json`, `organ_gamma.json`) had their hashes re-frozen in
`inherited/FROZEN_SHA256.json` **deliberately** (old → new recorded above). The atlas `_to_measure` now
lists only **TMC2** (still deferred). The three folded genes:

| gene | γ (measured) | accession (GRCh38) | NCBI gene | node | role |
|---|---|---|---|---|---|
| `SLC26A4` | 1.3612 | NC_000007.14 | 5172 | congenital_deafness | pendrin — Cl⁻/HCO₃⁻ exchange, endolymph homeostasis (Pendred/DFNB4) |
| `LHFPL5` | 1.4043 | NC_000006.12 | 222662 | mechanotransduction | MET-complex member, tip-link tension (DFNB67) |
| `MYO15A` | 1.4960 | NC_000017.11 | 51168 | hair_cell | myosin XVa — stereocilia elongation/structure (DFNB3) |

No other inherited artifact moved; the remaining six frozen hashes are unchanged from seed time.

**v0.6.0 — NO RE-FREEZE (회귀금지 — clean).** Increment **E5** (the otoferlin / OTOF readout substrate,
turning E4's READOUT [O] into a modelled auditory-neuropathy failure) builds **entirely** by importing
the frozen foundation. It fetched **no** new gene, folded nothing into the cache/atlas, and changed
**not one inherited byte** — so **no hash was re-frozen**. Every entry in the table above is byte-identical
to its v0.5.0 value (the verifier's no-regression block and E5's gate G2 both confirm the frozen set is
intact). The atlas `_to_measure` still lists only **TMC2** (deferred). E5's downstream Ca²⁺-sensor is a
NEW substrate distinct from the inherited cubic; it is defined inside `research/E5-readout-synapse/run.py`,
not in the inherited layer, so the foundation stays frozen.

**v0.7.0 — NO RE-FREEZE (회귀금지 — clean).** Increment **E6** (the cochlear traveling-wave ENVELOPE —
BLUEPRINT-E1, the seed's deepest [O], turned from a black box into a characterised one) builds
**entirely** by importing the frozen foundation: the R19 cubic (`vp_substrate.py`) and the √-law /
Greenwood place map (`vp_sound_wave.py`), reusing E1's inverse-Greenwood. It fetched **no** new gene,
folded nothing into the cache/atlas, and changed **not one inherited byte** — so **no hash was
re-frozen**. Every entry in the table above is byte-identical to its v0.6.0 value (the verifier's
no-regression block and E6's gate G2 both confirm the frozen set is intact). The active-amplifier gene
SLC26A5 is *reproduced* offline inside `research/E6-traveling-wave-envelope/run.py` only to anchor the E3
bridge and to demonstrate no inherited byte moved; its γ is **never** used as a damping, a Q, or a force
(firewall). The driven-resonator envelope and its single open scalar Q live in the increment, not in the
inherited layer, so the foundation stays frozen. The atlas `_to_measure` still lists only **TMC2**
(deferred).

**v0.9.0 — NO RE-FREEZE (회귀금지 — clean).** Increment **E8** (band-specific / frequency-selective hearing
loss — the audiogram shapes derived by composing E4's failure-CLASS axis with E7's PLACE axis) builds
**entirely** by importing the frozen foundation: the √-law / Greenwood place map (`vp_sound_wave.py`), E1's
inverse map (`inv_greenwood`) and reading, the inherited cubic's `spinodal` (to carry E4's structure-class
negative), and E4's class labels. It fetched **no** new gene, folded nothing into the cache/atlas, and
changed **not one inherited byte** — so **no hash was re-frozen**. Every entry in the table above is
byte-identical to its v0.8.0 value (the verifier's no-regression block and E8's gate G2 both confirm the
frozen set is intact). One already-cached gene per E4 class (SLC26A4 / MYO15A / OTOF / SLC26A5) is
*reproduced* offline inside `research/E8-band-specific-loss/run.py` only to confirm no-regression and to
anchor the cross-axis composition to the same frozen atlas; their γ is **never** used as a band edge, a load
rate, a dB threshold, or a notch frequency (firewall). WFS1 is named only as a cited clinical archetype — no
new γ is measured for it. The (class × band) directions and the lever directions live in the increment, not
in the inherited layer, so the foundation stays frozen. The atlas `_to_measure` still lists only **TMC2**
(deferred).

**v0.8.0 — NO RE-FREEZE (회귀금지 — clean).** Increment **E7** (the audible BAND — the audible range
derived as a geometry-carved bandpass on the inherited `√(stiffness/inertia)` wave law) builds **entirely**
by importing the frozen foundation: the √-law / Greenwood place map (`vp_sound_wave.py`), reusing E1's
reading. It fetched **no** new gene, folded nothing into the cache/atlas, and changed **not one inherited
byte** — so **no hash was re-frozen**. Every entry in the table above is byte-identical to its v0.7.0 value
(the verifier's no-regression block and E7's gate G2 both confirm the frozen set is intact). A reference
structure gene (TMC1) is *reproduced* offline inside `research/E7-audible-band/run.py` only to confirm
no-regression; its γ is **never** used as a stiffness, a corner, an area, or a band edge (firewall). The
band's bandpass form and its measured-geometry [O] edges live in the increment, not in the inherited layer,
so the foundation stays frozen. The atlas `_to_measure` still lists only **TMC2** (deferred).

**Source volumes (cited, one-way — this seed consumes; it never edits the source):**
- **physics** (DOI 10.5281/zenodo.17932566) — the jammed-lattice light emergence, c=√(B/ρ), the
  invariant quantum size D, the angle law (physics §SP/§10.9).
- **chemistry** (DOI 10.5281/zenodo.20680540) — electromagnetism from the lattice; conduction↔
  radiation by angle (chemistry §1).
- **dna** (DOI 10.5281/zenodo.20471407, **v1.13** "A Deterministic Two-Layer Interpretation of DNA")
  — the readable layer = **γ (level) + A4 coordinate (shape) + R19 switch-state + CpG handles**; the
  SantaLucia-1998 NN ΔG37 γ measure, the A4 grammar (`dna_interpreter.py` / `key_pipeline_full.py`,
  vendored byte-identical), and emergence order = argsort(spinodal(γ)). γ and A4 are the level and
  shape of one stiffness field — orthogonal, neither contains the other.
- **neuro / sensory_organ** (DOI 10.5281/zenodo.17979015 / 20755154) — the R19 substrate primitive
  and the colour-by-angle / transduction-switch readings this seed extends.

**Measured γ provenance:** every sequence in `inherited/ear_promoters.cache.json` was fetched from NCBI
nuccore (GRCh38 current RefSeq chromosomes) by exact accession + TSS−2000..+500 window + strand,
and is cached so γ recomputes offline bit-for-bit. The fetcher that built it ships at
`tools/fetch_promoter_gamma.py`; re-audit against live NCBI with `--cache`.

**Measured FULL-A4 provenance (v0.12.0):** every wide region + feature table in
`inherited/ear_regions.cache.json` was fetched from the **same** NCBI nuccore accessions as the promoter
cache, over the **same strand**, as the promoter window EXTENDED by a single gene-independent FLANK=20000 bp
each genomic side (sequence: rettype=fasta; annotation: rettype=ft). The cache stores the raw bytes + a
per-gene SHA-256 + the keystone flag (`region[FLANK:FLANK+2501]` == frozen promoter), so the full A4
coordinate recomputes offline bit-for-bit. The fetcher ships at `tools/fetch_region_features.py`; re-audit
against live NCBI with `python3 tools/fetch_region_features.py verify inherited/ear_regions.cache.json`.
