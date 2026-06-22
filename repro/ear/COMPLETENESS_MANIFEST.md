# COMPLETENESS MANIFEST (누락금지) — vp_ear_emergence_seed

Every artifact this seed promises. `tools/verify_seed.py` fails if any is missing.

- [x] `README.md`
- [x] `VERSION`
- [x] `seed.json`
- [x] `BLUEPRINT.md`
- [x] `FIREWALL.md`
- [x] `INHERITANCE_LEDGER.md`
- [x] `COMPLETENESS_MANIFEST.md`
- [x] `WORK_HANDOVER.md`
- [x] `VP_SPEC_v1_8.md`
- [x] `E_NUMBERING.md`                                      ← (v0.11.0) folder ⟷ BLUEPRINT-canonical reconciliation (open item #4)
- [x] `e_numbering.json`                                   ← (v0.11.0) machine-readable E-numbering map (checked by verify_seed.py [5])
- [x] `tools/verify_seed.py`
- [x] `tools/fetch_promoter_gamma.py`
- [x] `tools/fetch_region_features.py`                     ← (v0.12.0) live NCBI wide-region + feature-table fetcher (FULL A4 inputs)
- [x] `inherited/vp_substrate.py`
- [x] `inherited/gamma_pipeline.py`
- [x] `inherited/dna_interpreter.py`
- [x] `inherited/key_pipeline_full.py`
- [x] `inherited/vp_dna_reading.py`
- [x] `inherited/ear_promoters.cache.json`
- [x] `inherited/ear_regions.cache.json`                   ← (v0.12.0) FROZEN measured wide-region + NCBI feature-table bytes (FULL A4); NEW frozen key
- [x] `inherited/organ_gamma.json`
- [x] `inherited/FROZEN_SHA256.json`
- [x] `inherited/vp_sound_wave.py`
- [x] `research/E1-place-and-traveling-wave/START_HERE.md`
- [x] `research/E1-place-and-traveling-wave/run.py`        ← (v0.3.0) E1 emergence module (foundation)
- [x] `research/E1-place-and-traveling-wave/gate.py`       ← (v0.3.0) E1 standalone gate (7 checks)
- [x] `research/E1-place-and-traveling-wave/FINDINGS.md`   ← (v0.3.0) E1 result + honest negatives
- [x] `research/E3-cochlear-amplifier/START_HERE.md`       ← (v0.4.0) E3 task card
- [x] `research/E3-cochlear-amplifier/run.py`              ← (v0.4.0) E3 emergence module (foundation)
- [x] `research/E3-cochlear-amplifier/gate.py`             ← (v0.4.0) E3 standalone gate (7 checks)
- [x] `research/E3-cochlear-amplifier/FINDINGS.md`         ← (v0.4.0) E3 result + 5 honest negatives
- [x] `research/E4-congenital-deafness/START_HERE.md`      ← (v0.5.0) E4 task card (the goal)
- [x] `research/E4-congenital-deafness/run.py`             ← (v0.5.0) E4 emergence module (foundation)
- [x] `research/E4-congenital-deafness/gate.py`            ← (v0.5.0) E4 standalone gate (7 checks)
- [x] `research/E4-congenital-deafness/FINDINGS.md`        ← (v0.5.0) E4 result + 6 honest negatives
- [x] `research/E5-readout-synapse/START_HERE.md`          ← (v0.6.0) E5 task card (E4-N4 readout)
- [x] `research/E5-readout-synapse/run.py`                 ← (v0.6.0) E5 emergence module (foundation)
- [x] `research/E5-readout-synapse/gate.py`                ← (v0.6.0) E5 standalone gate (7 checks)
- [x] `research/E5-readout-synapse/FINDINGS.md`            ← (v0.6.0) E5 result + 6 honest negatives
- [x] `research/E6-traveling-wave-envelope/START_HERE.md`  ← (v0.7.0) E6 task card (BLUEPRINT-E1 envelope)
- [x] `research/E6-traveling-wave-envelope/run.py`         ← (v0.7.0) E6 emergence module (foundation)
- [x] `research/E6-traveling-wave-envelope/gate.py`        ← (v0.7.0) E6 standalone gate (7 checks)
- [x] `research/E6-traveling-wave-envelope/FINDINGS.md`    ← (v0.7.0) E6 result + 7 honest negatives
- [x] `research/E7-audible-band/START_HERE.md`             ← (v0.8.0) E7 task card (BLUEPRINT-E7 audible band)
- [x] `research/E7-audible-band/run.py`                    ← (v0.8.0) E7 emergence module (foundation)
- [x] `research/E7-audible-band/gate.py`                   ← (v0.8.0) E7 standalone gate (7 checks)
- [x] `research/E7-audible-band/FINDINGS.md`               ← (v0.8.0) E7 result + 7 honest negatives
- [x] `research/E8-band-specific-loss/START_HERE.md`       ← (v0.9.0) E8 task card (BLUEPRINT-E8 band-specific loss)
- [x] `research/E8-band-specific-loss/run.py`              ← (v0.9.0) E8 emergence module (foundation)
- [x] `research/E8-band-specific-loss/gate.py`             ← (v0.9.0) E8 standalone gate (7 checks)
- [x] `research/E8-band-specific-loss/FINDINGS.md`         ← (v0.9.0) E8 result + 7 honest negatives
- [x] `research/A4-anchor-loop-phase/START_HERE.md`        ← (v0.12.0) A4 task card (FIREWALL named [O] → MEASURED)
- [x] `research/A4-anchor-loop-phase/run.py`               ← (v0.12.0) A4 full-read module (foundation)
- [x] `research/A4-anchor-loop-phase/gate.py`              ← (v0.12.0) A4 standalone gate (7 checks)
- [x] `research/A4-anchor-loop-phase/FINDINGS.md`          ← (v0.12.0) A4 result + 7 honest negatives (N1–N7)
- [x] `volume/tools/vp_numeric_ssot.py`                    ← (v0.10.0) NUMERIC single-source-of-truth (foundation module)
- [x] `volume/content/chapters.py`                         ← (v0.10.0) chapter content (numbers as `[[KEY]]`)
- [x] `volume/tools/build_volume.py`                       ← (v0.10.0) deterministic static-HTML builder
- [x] `volume/tools/gate_volume.py`                        ← (v0.10.0) HTML↔code drift-0 gate
- [x] `docs/index.html`                                    ← (v0.10.0) volume hub (CreativeWorkSeries + contents + O-ledger)
- [x] `docs/01-place-and-traveling-wave/index.html`        ← (v0.10.0) §1 chapter
- [x] `docs/02-cochlear-amplifier/index.html`              ← (v0.10.0) §2 chapter
- [x] `docs/03-congenital-deafness-failure-modes/index.html` ← (v0.10.0) §3 chapter
- [x] `docs/04-readout-synapse-otoferlin/index.html`       ← (v0.10.0) §4 chapter
- [x] `docs/05-traveling-wave-envelope/index.html`         ← (v0.10.0) §5 chapter
- [x] `docs/06-audible-band/index.html`                    ← (v0.10.0) §6 chapter
- [x] `docs/07-band-specific-hearing-loss/index.html`      ← (v0.10.0) §7 chapter
- [x] `docs/concepts/r19-bistable-switch/index.html`       ← (v0.10.0) concept (DefinedTerm)
- [x] `docs/concepts/greenwood-place-map/index.html`       ← (v0.10.0) concept (DefinedTerm)
- [x] `docs/concepts/gamma-level-a4-shape/index.html`      ← (v0.10.0) concept (DefinedTerm)
- [x] `docs/assets/css/site.css`                           ← (v0.10.0) site stylesheet (offline, grade-encoded colour)
- [x] `docs/sitemap.xml`                                   ← (v0.10.0) sitemap (11 URLs)
- [x] `docs/robots.txt`                                    ← (v0.10.0) robots (AI crawlers allowed) + sitemap
- [x] `docs/llms.txt`                                      ← (v0.10.0) machine-readable volume index
- [x] `docs/gate.json`                                     ← (v0.10.0) drift-0 gate report (deterministic)

**Total: 76 artifacts.** Foundation modules: `inherited/vp_sound_wave.py`,
`inherited/vp_dna_reading.py`, `research/E1-place-and-traveling-wave/run.py`,
`research/E3-cochlear-amplifier/run.py`, `research/E4-congenital-deafness/run.py`,
`research/E5-readout-synapse/run.py`, `research/E6-traveling-wave-envelope/run.py`,
`research/E7-audible-band/run.py`, `research/E8-band-specific-loss/run.py`,
`research/A4-anchor-loop-phase/run.py`, `volume/tools/vp_numeric_ssot.py`.

**v0.12.0 — increment A4 (the FULL A4 anchor/loop/anchor-relative-phase deferred read): the FIREWALL's one named [O], now MEASURED. ONE new frozen artifact added deliberately; the 8 pre-existing inherited bytes UNCHANGED, NO re-freeze.**
The FIREWALL §1 named exactly one deferred read: *"the FULL A4 anchor/loop/anchor-relative-phase needs the
wider region + an NCBI feature table and is a named [O] deferred read — flagged, never invented."* Increment
**A4** turns it into a **MADE measurement** — not by inventing numbers, but by fetching the two named inputs
for all 19 genes (`tools/fetch_region_features.py`: the promoter window EXTENDED by a single, gene-independent
**FLANK=20000 bp** each genomic side → the wide region sequence + the feature table over the same region, both
strand-corrected) and running the **INHERITED** grammar on them (`dna_interpreter` + `key_pipeline_full`:
`run_key`/`build_anchors`/`parse_ft_motors`/`build_loops`/`helix_coord` — the [O] was a missing MEASUREMENT,
**not** missing machinery). The raw measured bytes are cached in `inherited/ear_regions.cache.json` (added to
`FROZEN_SHA256.json` as **one new frozen key**; SHA `dc1b151d…`) and the full A4 coordinate is recomputed
**offline, deterministically** in `research/A4-anchor-loop-phase/run.py` (foundation module; 2×sha256
`a504a93e…`). **Result:** the keystone `region[FLANK:FLANK+2501]` == the frozen promoter **byte-for-byte
19/19** (the wide read sits on the unchanged γ layer, **zero drift**); every gene's TSS now carries a real
wide-neighbourhood **shell** (18/19 stiff; TMC1 the AT-rich exception), a real nearest **anchor**, real
feature-table **motors joined as loops (19/19 carry ≥1)**, and a real anchor-relative **B-DNA phase** (3/19
contact-competent: EYA1, PCDH15, SLC26A4); the read is **mostly window-stable** under a 2× sub-window shrink
of the same fetch (motor existence 19/19, shell class 15/19, contact sign 16/19). **No clean numeric closure
is claimed** (that would be tuning): the absolute FLANK/distances/counts and the boundary-near class/sign are
the named **window-relative [O]**, "anchor" is a mechanical proxy (not CTCF), "loop" is geometric (not Hi-C),
the twist is idealised, and Layer-2 stays flagged — each obstacle named (N1–N7). **Six artifacts were added
(now 76, was 70)** — the fetch tool, the frozen region cache, and the A4 increment's four files — and **one
foundation module** (`research/A4-anchor-loop-phase/run.py`) was registered (the verifier runs it twice and
confirms determinism). The no-regression block now checks **9** frozen files: the 8 inherited entries are
byte-identical to v0.11.0 (NO re-freeze; only v0.9.1's deliberate TMC2 re-freeze stands) and the one new
region cache matches. `SEED VERIFY: PASS` over 19 genes, 76 artifacts, [5] all-pass (the A4 folder does not
start with "E", so it is correctly outside the E-numbering map).

**v0.11.0 — citable concept DOI minted + E-numbering reconciled (open item #4). No inherited byte changed; NO re-freeze.**
Two non-scientific closeouts, both gate-clean. **[A] DOI reflection.** This volume's own **concept DOI**
`10.5281/zenodo.20790201` is now minted (same author/ORCID workflow as the sibling volumes), so the
"pending Zenodo deposit" placeholder is replaced everywhere it rendered: the `docs/` footer now links the
concept DOI (`doi:10.5281/zenodo.20790201`), `llms.txt` cites it, and the JSON-LD on every page carries it
as `identifier` + `sameAs` (chapters' `ScholarlyArticle` + their `isPartOf` series, the hub
`CreativeWorkSeries`, and the concept `DefinedTermSet`) — closing the VP-SPEC v1.8 `sameAs`/`identifier`
requirement the volume previously left open. The DNA-volume DOI (`10.5281/zenodo.20471407`) is still cited
as the *readable-layer source*; deployment to `jamming-physics.org/ear` remains honestly "pending". The
drift-0 gate is unaffected (the DOI is a hyperlink, not a `data-vp` number): **81 numbers, drift 0**, 145
links resolve. **[B] E-numbering reconciliation.** Open item #4 (flagged since v0.3.0) is closed: a new
authoritative map `e_numbering.json` + `E_NUMBERING.md` records that research folders use a
**chronological-build-order** convention which coincides with BLUEPRINT-canonical numbering for E3/E4/E5/E7/E8
and differs in exactly two places by design — folder `E1` carries BLUEPRINT-**E2** (the MET switch) and
folder `E6` carries BLUEPRINT-**E1** (the envelope). No folder is renamed (no-omission + foundation paths +
deposited cross-links). The verifier gains block **[5] E-NUMBERING CONSISTENT** which enforces the map
against the filesystem and `seed.json` (folder set-equality both directions, every mapped `run.py` a
registered foundation module, `blueprint_E` injective, the two slip pairs exact, canonical carriers
round-trip) — so the labels can never silently drift; a negative test confirms [5] fails on a silent fix or a
dropped folder. **Two artifacts were added (now 70, was 68)**; no foundation module added; the no-regression
block is untouched (**not one inherited byte changed**, no re-freeze — only v0.9.1's deliberate TMC2 re-freeze
stands). `SEED VERIFY: PASS` over 19 genes, 70 artifacts, [5] all-pass.


The complete E-chain is published as an 11-page static site per VP-SPEC v1.8 §6 (hub + 7 chapters + 3
concept pages), plus `sitemap.xml`/`robots.txt`/`llms.txt`. Every displayed number is produced only by
`volume/tools/vp_numeric_ssot.py` (which imports the **frozen** foundation + **verified** E-modules and
calls the same functions — nothing re-typed or fitted) and emitted as `<span data-vp="KEY">`;
`volume/tools/gate_volume.py` re-derives each and asserts **HTML↔code drift 0** (81 numbers), 2×-process
SSOT determinism, byte-identical on-disk⟷builder output, full per-page structure, no-omission, and all
145 internal links resolving. **Twenty artifacts were added (now 68, was 48)** and **one foundation
module** (`volume/tools/vp_numeric_ssot.py`) was registered — the verifier runs it twice and confirms it
is deterministic (sha256 `ee6e681f…`). The verifier's no-regression block is untouched: **not one
inherited byte changed**, so there is **no re-freeze** (only v0.9.1's deliberate TMC2 re-freeze stands).
This volume's own snapshot DOI is *pending Zenodo deposit*; the footer cites the real DNA-volume DOI
(`10.5281/zenodo.20471407`) as the readable-layer source, and the canonical `jamming-physics.org/ear`
URLs are forward-looking (deployment pending).

**v0.9.1 — atlas completion (fold TMC2), DELIBERATE inherited re-freeze (see `INHERITANCE_LEDGER.md`).**
The last deferred gene **TMC2** (second MET pore-forming subunit; mechanotransduction node, STRUCTURE
class) was fetched via `tools/fetch_promoter_gamma.py` (NCBI nuccore, GRCh38, TSS−2000..+500; two live
fetches byte-identical) and folded into `inherited/ear_promoters.cache.json` + `inherited/organ_gamma.json`
(now **19** genes each); γ recomputes offline bit-for-bit. Both files' hashes were re-frozen in
`inherited/FROZEN_SHA256.json` **deliberately**; the other six inherited hashes are byte-identical to seed
time. The atlas `_to_measure` is now **EMPTY** — the readable layer is complete. **No new files** were
added or removed (still **48** artifacts) and no foundation module was added; only inherited bytes (two
files) changed, by design. The verifier's no-omission block is unaffected; its no-regression block now
checks the two re-frozen hashes and [3] recomputes 19 genes.

**v0.9.0 — increment E8 (band-specific hearing loss), NO inherited re-freeze.** Increment **E8** (band-
specific / frequency-selective hearing loss — the characteristic audiogram shapes derived by composing E4's
failure-CLASS axis with E7's PLACE axis) imports the **frozen** Greenwood place map and E1's inverse map,
reproduces one already-cached gene per E4 class, fetched **no** new gene, and folded nothing into the
cache/atlas: it touches **not one inherited byte** and triggers **no re-freeze**. Four artifacts were added
(now **48**, was 44) and one foundation module (`research/E8-band-specific-loss/run.py`) was registered. The
full frozen-hash set is byte-identical to v0.8.0. The atlas `_to_measure` still lists only TMC2 (deferred).

**v0.8.0 — increment E7 (the audible band), NO inherited re-freeze.** Increment **E7** (the audible BAND —
the audible range derived as a geometry-carved bandpass on the inherited `√(stiffness/inertia)` wave law)
imports the **frozen** Greenwood place map, fetched **no** new gene, and folded nothing into the
cache/atlas: it touches **not one inherited byte** and triggers **no re-freeze**. Four artifacts were added
(now **44**, was 40 — the v0.7.1 patch added no files) and one foundation module (`research/E7-audible-band/run.py`)
was registered. The full frozen-hash set is byte-identical to v0.7.0. The atlas `_to_measure` still lists
only TMC2 (deferred). E8 (band-specific hearing loss) was specified here and is **built in v0.9.0** (above).

**v0.7.1 — BLUEPRINT-only patch (no artifact-set change).** Two planned increments (**E7** the audible
band / geometric bandwidth; **E8** band-specific hearing loss) were specified in `BLUEPRINT.md`; no files
were added or removed (still **40** artifacts), no foundation module added, and **no inherited byte
changed**. The verifier's no-omission and no-regression blocks are unaffected.

**v0.7.0 — NO inherited re-freeze.** Increment **E6** (the cochlear traveling-wave ENVELOPE —
BLUEPRINT-E1, the seed's deepest [O]) imports the **frozen** substrate + place map, fetched **no** new
gene, and folded nothing into the cache/atlas: it touches **not one inherited byte** and triggers **no
re-freeze**. The full frozen-hash set is byte-identical to v0.6.0. The atlas `_to_measure` still lists
only TMC2 (deferred).

**v0.6.0 — NO inherited re-freeze.** Increment **E5** (the otoferlin readout substrate) fetched **no**
new gene and folded nothing into the cache/atlas: it touches **not one inherited byte** and triggers
**no re-freeze**. The full frozen-hash set is byte-identical to v0.5.0. The atlas `_to_measure` still
lists only TMC2 (deferred).

**v0.5.0 inherited re-freeze (deliberate, never silent — see `INHERITANCE_LEDGER.md`).** Three new
measured genes (SLC26A4, LHFPL5, MYO15A) were fetched via `tools/fetch_promoter_gamma.py` and folded
into `inherited/ear_promoters.cache.json` + `inherited/organ_gamma.json` (now 18 genes each); both
files' hashes were re-frozen in `inherited/FROZEN_SHA256.json` deliberately. The atlas `_to_measure`
now lists only TMC2 (deferred).

