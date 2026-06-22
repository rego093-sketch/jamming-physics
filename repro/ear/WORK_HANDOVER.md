# WORK_HANDOVER — vp_ear_emergence_seed (research SEED, v0.12.0)

## How to pick this up (one file)
Re-upload exactly **one** file: this package zip. Everything needed is inside it. First action:
extract, `cd` in, run `python3 tools/verify_seed.py`, confirm **SEED VERIFY: PASS**. That single
command re-establishes the entire trusted state.

## The binding rules (do not violate)
1. **OUTPUT is always ONE zip.** Never split the deliverable; never ship loose files. One archive,
   package-relative paths.
2. **회귀금지 / no-regression.** The inherited foundation never drifts. If you must update an
   inherited artifact, re-freeze its hash in `inherited/FROZEN_SHA256.json` deliberately (delete the
   key, re-run the verifier to record the new hash) and note *why* in the inheritance ledger —
   never silently.
3. **누락금지 / no-omission.** Every artifact in `COMPLETENESS_MANIFEST.md` / `seed.json` stays
   present. The verifier fails if any is missing. Add new artifacts to the manifest.
4. **No tuning.** Measured-or-derived only; γ from NCBI, never fitted. Each [O] names its obstacle.
5. **Firewall stays verbatim** (`FIREWALL.md`): structure-only γ; proposal-only disease layer;
   felt percept → mind.

## Next session (start here)
**E1, E3, E4, and E5 are DONE.** E1 (v0.3.0): tip-link MET switch on the place map. E3 (v0.4.0): the
cochlear amplifier (prestin / `SLC26A5`) as the R19 cubic at criticality (`F^(1/3)` / `F^(−2/3)`).
E4 (v0.5.0, the goal): congenital deafness emerged as the cubic's failure-mode decomposition (four
classes — drive `h` / structure `g` / readout downstream / amplifier `g→0`), one of which (READOUT /
OTOF) was deliberately left an honest **[O]**.
**E5 (v0.6.0): that READOUT [O] is now MODELLED** (`research/E5-readout-synapse/`). The readout layer is
shown to be a substrate **distinct from** the R19 cubic — release is non-negative, monotone, saturating,
and NON-bistable, so the minimal form is a **rectified saturating Ca²⁺ sensor** (otoferlin), which is the
provable reason the E4 cubic is blind to OTOF. Composing the sensor with the **frozen** switch reproduces
**auditory neuropathy** (a sound flips the switch to s=+1.3864, IDENTICAL in a hearing and an OTOF ear,
but the removed sensor zeroes release 0.5810→0.0000); forces the **composed compression exponent
`F^(m/3)`** = E3 cube-root (1/3) × synaptic cooperativity m (cited [L], machine-precision fit); forces the
**OAE⁺/ABR⁻** clinical signature (amplifier E3/OHC intact ∥ readout E5/IHC-synapse zeroed — separable
stages); and forces the OTOF lever **DIRECTION** (restore the readout stage, not the switch). Six honest
negatives N1–N6. All four research gates pass; the inherited foundation stayed frozen — **E5 changed no
inherited byte** (no re-freeze); only E4's deliberate atlas/cache re-freeze stands.
**E6 (v0.7.0): the seed's DEEPEST [O] — the traveling-wave ENVELOPE — is now CHARACTERISED**
(`research/E6-traveling-wave-envelope/`). It does not close the [O] by tuning a sharpness (forbidden); it
proves the envelope is a **one-parameter family in Q**. Modelling the partition as a driven damped
resonator on the **frozen** Greenwood CF(x): the velocity **peak sits at ω0=CF(x) for every Q** (= E1's
place, |Δ|=0.0000); the partition reactance `χ=1−(f/CF)²` flips sign at CF, forcing a propagating basal
tail and an **evanescent apical cutoff** (asymmetry SIGN, κ-robust); the −3 dB velocity bandwidth is
**exactly ω0/Q**; the active amplifier is **negative damping** `Q_eff=Q0/(1−G)` whose critical point is
the E3 cube root; the group delay **peaks at CF** with magnitude 2Q/ω0. Every LOCATION is forced and
Q-invariant; every MAGNITUDE scales with Q and is fixed by no inherited constant — so **Q is the single
irreducible [O]**, and a number for it would be tuning. Seven honest negatives N1–N7; gate 7/7 PASS;
**E6 changed no inherited byte** (no re-freeze).
**E7 (v0.8.0): the audible BAND is now DERIVED** (`research/E7-audible-band/`) — *why only ~20 Hz–20 kHz is
heard* emerges as a **geometry-carved bandpass** on the inherited `√(stiffness/inertia)` wave law, same
form-forced / magnitude-[O] discipline as E6. The **keystone** `N_oct = ½·log₂(S_base/S_apex)` is verified
**exact** (the √-law HALVES the stiffness decades into octaves): the inherited Greenwood apex/base
(19.848 Hz / 20677.07 Hz) give a **10.0248-oct** span ⟺ stiffness ratio **1.085×10⁶**, `½·log₂(S_ratio)`
closing to |Δ|=0.0; the span decomposes as 6.976 oct (bare `10^(a·x)`) + 3.059 oct (helicotrema apical
bend) − 0.010 oct. The **LOW edge** is a helicotrema high-pass (the `−A·k` offset is a LOW-END-only relief,
fractional weight 0.88 apex vs 0.0070 base = ratio 10^a, bending the apex down ~3 oct to ~20 Hz; the apical
hole forces a lows-cut SIDE, order-robust); the **HIGH edge** is a middle-ear low-pass (the ossicular MASS
forces a **−12 dB/oct** highs-cut robust to ζ, and the stiff base fixes a **finite** CF_max=20677 Hz). The
band is the **product** — a unimodal bandpass whose SHAPE and every edge SIGN are forced by geometry, while
the absolute edges and three corners are the irreducible measured-geometry [O] (a number = tuning). Seven
honest negatives N1–N7; gate 7/7 PASS; **E7 changed no inherited byte** (no re-freeze). This also supplies
the **place axis** E8 needs (now consumed in v0.9.0).

**E8 (v0.9.0): band-specific hearing loss is now DERIVED** (`research/E8-band-specific-loss/`) — the
characteristic audiogram SHAPES emerge by composing **E4's failure-CLASS axis × E7's PLACE axis**: a disease
is a **2-D object** (a class acting over a band of places). The **keystone** is that the inherited place map
`CF(x)` is strictly **monotone**, so place→frequency is an **order-isomorphism** — a contiguous band of
FAILED PLACES maps to a contiguous band of LOST FREQUENCIES, order preserved, and `inv_greenwood` maps it
back **exactly** (`|Δ|<1e-9`). So the audiogram SHAPE *is the image* of *where* the failure sits: **basal →
high-frequency down-slope** (presbycusis — the base cycles fastest, `CF` *is* the rate, so cumulative load
is basal-first, load(base)/load(apex)=1042×); **apical → low-frequency reverse-slope** (WFS1/ion regime);
**mid → cookie-bite** (the isomorphism's mid-place→mid-frequency, locus mid-concentration cited — the
weakest of the four); and a localized **over-drive at the outer/middle-ear transfer peak → a notch BELOW the
top** (the transfer = canal resonance × the E7 ossicular low-pass is unimodal with an interior peak below
CF_max — the ~3–6 kHz C5-dip). The lever is the **E4 direction applied at the E7 band**, proposal-only; and
E4's honest negative **carries** (a structure-class high-frequency loss has no drive rescue — the bistable
window `2·spinodal(g)→0` as `g→0`). Every DIRECTION forced; every threshold/slope/notch-Hz/age `[O]` (a
number = tuning); seven honest negatives N1–N7; gate 7/7 PASS; **E8 changed no inherited byte** (no
re-freeze).

**A4 (v0.12.0): the FIREWALL's one named, deferred [O] — the FULL A4 anchor/loop/anchor-relative-phase
read — is now MEASURED** (`research/A4-anchor-loop-phase/`). The firewall §1 named exactly one deferred
read: *"the FULL A4 anchor/loop/anchor-relative-phase needs the wider region + an NCBI feature table and is
a named [O] deferred read — flagged, never invented."* A4 turns it into a **MADE measurement** — the key
realisation is that **it was a missing MEASUREMENT, not missing machinery**: the inherited grammar
(`dna_interpreter` + `key_pipeline_full`) **already** contained every function the full read uses
(`run_key`, `build_anchors`, `parse_ft_motors`, `build_loops`, `helix_coord`). So A4 fetches the two named
inputs for all 19 genes (`tools/fetch_region_features.py`: the frozen promoter window EXTENDED by a single
gene-independent **FLANK=20000 bp** each genomic side → the wide region + the feature table over the same
region, strand-corrected), caches the raw bytes in the **new frozen** artifact
`inherited/ear_regions.cache.json` (added to `FROZEN_SHA256.json` as a NEW key — the 8 inherited entries
stay byte-identical, **NO re-freeze**), and recomputes the full A4 coordinate **offline, deterministically**
by importing the inherited grammar — inventing **no machinery and no number**. **Result:** the **keystone**
`region[FLANK:FLANK+2501]` == the frozen promoter **byte-for-byte 19/19** (the wide read sits on the
unchanged γ layer, ZERO drift); every gene's TSS carries a real wide-neighbourhood **shell** (18/19 stiff;
TMC1 the AT-rich exception), a real nearest **anchor** (strength = |Δmean_z|), real feature-table **motors
joined as loops (19/19 carry ≥1)** — fulfilling the `dna_interpreter` promise *anchors-only → real
motors+loops* on MEASURED annotation — and a real anchor-relative **B-DNA phase** (3/19 contact-competent:
EYA1, PCDH15, SLC26A4). The read is **mostly window-stable** under a 2× sub-window shrink of the SAME fetch
(no new data): motor existence **19/19**, shell class **15/19**, contact sign **16/19** — so it is NOT a
FLANK artifact for the majority; the boundary-near minority that flips (class: SIX1/GATA3/USH2A/LHFPL5;
contact: EYA1/PCDH15/MYO15A) is the named **window-relative [O]**. **No clean numeric closure is claimed**
(that would be tuning): the absolute FLANK/distances/counts and boundary-near class/sign are window-relative
[O], "anchor" is a mechanical proxy (not a measured CTCF/cohesin site), "loop" is geometric (not a Hi-C
contact), the twist is idealised, and Layer-2 stays flagged — each obstacle named (N1–N7). Gate 7/7 PASS;
**A4 changed no pre-existing inherited byte**, adding **one** new frozen artifact deliberately.

**Open items remaining (pick any):**
1. ~~**The named [O] — the dispersive traveling-wave ENVELOPE.**~~ **CHARACTERISED in v0.7.0 (E6).** The
   envelope FORM is now forced and its openness reduced to a single dimensionless scalar Q: every
   LOCATION (peak place = E1's place, apical-cutoff side, group-delay peak) is forced and Q-invariant,
   every MAGNITUDE (width = ω0/Q exactly, height, slope, absolute delay) scales with Q and is fixed by no
   inherited constant — so Q is the single irreducible [O] and a number for it would be **tuning
   (forbidden)**. What remains genuinely [O] is the **full 2-D/3-D fluid (Lighthill/Zweig) hydrodynamics**
   — the short-wave region right at the peak, the "second filter," the active feedback's spatial extent
   (E6-N5) — plus a measured/derived value for Q itself. A follow-on would attempt the full hydrodynamic
   envelope, but a closed numeric envelope still requires fixing Q, so weigh the no-tuning rule before
   opening it.
2. ~~**Fold `TMC2`** — the last gene in the atlas `_to_measure`.~~ **DONE in v0.9.1.** TMC2 (second MET
   pore-forming subunit, mechanotransduction node, STRUCTURE class, paralog of TMC1) was fetched via
   `tools/fetch_promoter_gamma.py` (NCBI nuccore, GRCh38, chr20 `NC_000020.11`, gene 117532; two live
   fetches byte-identical, γ=1.4160 recomputes offline bit-for-bit, A4 = signal − γ holds), folded into
   `ear_promoters.cache.json` + `organ_gamma.json` (now **19** genes), and the two files' hashes re-frozen
   **deliberately** (key deleted, new hash recorded; old→new in `INHERITANCE_LEDGER.md`); the other six
   inherited hashes stayed byte-identical. The atlas `_to_measure` is now **EMPTY — the readable layer is
   complete**. Read-only: TMC2 lands at #8/19 in the spinodal emergence order, far ahead of TMC1 at #2/19,
   with opposite A4 skew (same family, not interchangeable at the readable layer). `SEED VERIFY: PASS` over
   19 genes; no new files (still 48 artifacts). ~~A follow-on could attempt the FULL A4 anchor/loop/
   anchor-relative-phase deferred read (needs the wider region + an NCBI feature table, `rettype=ft`) — the
   named [O] flagged in the firewall — but that is a new read, not a number to invent.~~ **DONE in v0.12.0
   (A4)** (`research/A4-anchor-loop-phase/`): the wider region + feature table were fetched for all 19 genes
   and the inherited grammar makes the full read (keystone 19/19, real motors+loops 19/19, anchor-relative
   B-DNA phase) — no number invented; the residual is the window-relative + wet-lab [O] (N1–N7).
3. ~~**Extend the OTOF READOUT class** into its own substrate.~~ **DONE in v0.6.0 (E5).** The follow-on
   would be to add the explicit synaptic-vesicle-pool DYNAMICS (depletion/replenishment, adaptation,
   spontaneous-rate baseline) on top of the static E5 sensor — but every added rate constant is [O]
   without tuning, so weigh that before opening it.
4. ~~**The E-numbering reconciliation**~~ **DONE in v0.11.0** (`E_NUMBERING.md` + `e_numbering.json`).
   The slip (flagged since v0.3.0) was: the folder labelled `E1` ships BLUEPRINT-**E2** content (the MET
   switch), and BLUEPRINT-**E1** (the traveling-wave ENVELOPE) ships in folder `E6`. It is now reconciled
   — *not* by renaming folders (that would touch the no-omission manifest, the `seed.json`
   `foundation_modules` paths, the SSOT loader, and the cross-links already deposited in sibling/site
   releases — the frozen-hash lineage was never the blocker, since only the eight `inherited/` artifacts
   are hash-frozen and none is a research folder) — but by recording the **chronological-folder
   convention** in an authoritative map and *enforcing* it. The convention matches BLUEPRINT-canonical
   numbering for E3/E4/E5/E7/E8 and differs in exactly two places by design (folder `E1`⟷BLUEPRINT `E2`;
   folder `E6`⟷BLUEPRINT `E1`). The verifier gained block **[5] E-NUMBERING CONSISTENT** (folder
   set-equality both directions, every mapped `run.py` a registered foundation module, `blueprint_E`
   injective, the two slip pairs exact, canonical carriers round-trip), so the labels can never silently
   drift; a negative test confirms [5] fails on a silent "fix" or a dropped folder. If a future session
   *does* physically rename a folder, it must update `e_numbering.json` in the same change — [5] enforces
   it (deliberate, never silent). No inherited byte changed; no number changed; no folder renamed.
5. ~~**Grow the seed into the full HTML volume**~~ **DONE in v0.10.0** (`docs/`, built by
   `volume/`). The seed is now a multi-chapter deterministic HTML volume per VP-SPEC v1.8 §6 —
   **11 pages**: a hub (`docs/index.html`, `CreativeWorkSeries` JSON-LD + a contents list and the
   honest open-obstacle ledger), **7 chapters** (§1–§7, one per research E-chapter, `ScholarlyArticle`
   + `BreadcrumbList` JSON-LD, answer-first, claim-strip with `LOCK→Derive→Gate` + repro + DOI,
   self-contained concept cards, honest-negatives block, firewall), and **3 locked-concept pages**
   (`DefinedTerm` JSON-LD). The anti-tuning invariant is enforced **structurally**: every displayed
   number comes only from `volume/tools/vp_numeric_ssot.py` (a NUMERIC single-source-of-truth that
   imports the **frozen** foundation + **verified** E-modules and calls the same functions they do —
   no number is re-implemented, hand-typed, or fitted), is emitted only as
   `<span class="vp-num" data-vp="KEY">…</span>`, and `volume/tools/gate_volume.py` re-derives every
   one and asserts **HTML↔code drift = 0** (latest gate: **81 numbers, drift 0**), plus 2×-process
   SSOT determinism, byte-identical on-disk⟷builder output, full per-page structure, no-omission, and
   145 internal links resolving. Static HTML, system fonts (offline-deterministic), `sitemap.xml` +
   AI-bot-friendly `robots.txt` + `llms.txt`. **Changed no inherited byte** (no re-freeze). Build:
   `python3 volume/tools/build_volume.py` → gate: `python3 volume/tools/gate_volume.py` → view:
   `cd docs && python3 -m http.server`. NOTE the DOI honesty — this volume's own **concept DOI is now
   minted** (`10.5281/zenodo.20790201`, the version-independent latest-resolver), cited in the footer and
   carried in every page's JSON-LD (`identifier` + `sameAs`); the footer still cites the DNA-volume DOI
   (`10.5281/zenodo.20471407`) as the readable-layer source. What remains honestly *pending* is **deployment
   only**: the canonical `jamming-physics.org/ear` URLs are still forward-looking until `docs/` is published.
   A follow-on would deploy.
6. ~~**Build E7 — the audible BAND.**~~ **DONE in v0.8.0 (E7)** (`research/E7-audible-band/`). The
   geometry-carved bandpass is built: keystone `N_oct = ½·log₂(S_base/S_apex)` locked (exact; 10.025 oct ⟺
   1.085×10⁶), the LOW edge a helicotrema high-pass (the `−A·k` offset is a LOW-END-only relief, ratio of
   fractional weights = 10^a, bending the apex down 3.06 oct to ~20 Hz), the HIGH edge a middle-ear low-pass
   (ossicular mass → −12 dB/oct, ζ-robust) plus a finite basal ceiling (CF_max=20677 Hz); the band is the
   unimodal product, SHAPE + every edge SIGN forced, absolute edges/corners the measured-geometry `[O]`.
   Gate 7/7; no inherited byte changed. A follow-on would attempt the full 2-D/3-D fluid transfer (E7-N5)
   and a measured value for each corner — but a closed numeric band still requires fixing those measured
   magnitudes, so weigh the no-tuning rule before opening it.
7. ~~**Build E8 — band-specific hearing loss.**~~ **DONE in v0.9.0 (E8)** (`research/E8-band-specific-loss/`).
   Frequency-**selective** audiograms emerged as **E4's failure-class axis × E7's place axis**: the place→
   frequency **order-isomorphism** (CF monotone) forces the four shapes — high-frequency/presbycusis
   (basal-first, the base cycles fastest), the **4 kHz noise notch** (the outer/middle-ear transfer's
   interior peak below CF_max), **cookie-bite** mid-frequency (the isomorphism's mid→mid; locus
   mid-concentration cited — the weakest of the four), low-frequency/reverse-slope (apical/ion regime). The
   lever is the E4 direction at the E7 band, proposal-only; E4's structure-class negative carries (no drive
   rescue for a structural high-frequency loss). Gate 7/7; no inherited byte changed. A follow-on could add
   the readout-class synaptic band-shape (E8-N7, a different substrate) or per-patient/quantitative
   audiograms — but every dB/slope/notch-Hz is [O] without tuning, so weigh the no-tuning rule first.

**With #4 and #5 both delivered, the research E-chain E1/E3/E4/E5/E6/E7/E8 is complete through
band-specific loss, the readable-layer atlas is COMPLETE (19 genes, `_to_measure` empty), the deterministic
HTML volume publishes all seven chapters drift-0, the volume's concept DOI is minted, the E-numbering
slip is reconciled (open item #4 → see `E_NUMBERING.md` + `e_numbering.json`, now enforced by verifier
check [5]), and — new in v0.12.0 — the FIREWALL's one named, deferred [O], the FULL A4 anchor/loop/
anchor-relative-phase read, is now MEASURED (`research/A4-anchor-loop-phase/`: the wider region + NCBI
feature table fetched for all 19 genes, the inherited grammar making the read, keystone 19/19, no number
invented). The remaining open work is now operational rather than scientific: deploy `docs/` to
`jamming-physics.org/ear` (then the footer's forward-looking canonical URLs can be made concrete — the
DOI-minting half of that step is already done). The deeper scientific residue is honestly [O] and named,
not a number to invent: a measured wet-lab architectural contact map (Hi-C/ChIP — A4-N1/N2), sequence-
dependent helical twist (A4-N3), the full 2-D/3-D fluid traveling-wave hydrodynamics + a value for Q
(E6-N5), and synaptic-pool dynamics on the readout substrate (E5 follow-on) — each would need measured
inputs, never a fitted constant.**

When a new master gene's γ is needed, run `python3 tools/fetch_promoter_gamma.py SYMBOL`, fold the
result into `inherited/ear_promoters.cache.json` (+ `organ_gamma.json`), re-freeze its hash deliberately
(ledger note), and re-verify. Build each new increment as a deterministic module under `research/`
(self-hashing, grades declared), wire a gate, fold its `run.py` into `seed.json` `foundation_modules`
and all four files into `completeness` + `COMPLETENESS_MANIFEST.md`, and keep the inherited foundation
frozen.

## Sibling
This is one of a split pair. The other sense ships as its **own** seed zip
(`vp_eye_emergence_seed…`). Keep them
apart — two files, two lanes. They share only the organising insight (wave → spatial code → R19
switch) and the √(B/ρ) wave rule, not code.
