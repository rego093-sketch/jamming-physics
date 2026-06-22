# BLUEPRINT (청사진) — vp_ear_emergence_seed

**Goal.** Properly emerge the **ear (hearing)** from the inherited wave theory and measured DNA γ,
ending at a **congenital DEAFNESS (DFNB1/connexin-26, auditory neuropathy/OTOF, Usher syndrome)** mechanism layer — research toward the congenitally affected.

**The organising insight (shared with the sibling sense).**
> A special sense is **a wave property → a spatial code → an R19 transduction switch**, and a
> congenital sensory disease is **that switch failing to flip**. Vision: colour ← propagation
> **angle**. Hearing: pitch ← basilar-membrane **place**. Same skeleton, two media.

## Research increments (the plan)

**E0 — inherited foundation (DONE; verified in this seed).**
- Sound is light's rule in matter: a **longitudinal wave at c=√(B/ρ)** (the same √(stiffness/
  inertia) form). The lattice keeps only the longitudinal branch; sound is that branch in a
  medium (`vp_sound_wave.py`: air 343 m/s, water 1478 m/s reproduced, wave emerges at c=1 [V]).
- The **√-law is why the ear is a spectrum analyser**: a resonant place rings at ω=√(S/m); a
  **log-graded stiffness** ⇒ an **exponential place→frequency map** = Greenwood's measured SHAPE
  (forced to machine precision; absolute A/a/k are calibration [L]).
- The R19 substrate (`vp_substrate.py`) and **15 master-gene readings** are loaded: each gene read
  from DNA as **γ (LEVEL) + A4 coordinate (SHAPE)** (DNA v1.13), not γ alone — `vp_dna_reading.py`
  computes both from the cached promoters and proves A4 = signal − γ (orthogonality) per gene.

**E1 — the full traveling wave (the named open derivation).** Move from the place-resonance
account to the **fluid-loaded, dispersive cochlear traveling wave** (Lighthill/Zweig
hydrodynamics) built on the lattice wave + graded impedance. This is the honest [O] this seed
exists to close — the place map is the starting line, not the finished wave.

> **STATUS (v0.3.0): the `START_HERE.md` E1 task is DELIVERED** — the tip-link MET lineage
> (`TMC1 / PCDH15 / CDH23`, + TMIE) emerged on the place map (`research/E1-place-and-traveling-wave/`):
> order = argsort(spinodal(γ)), A4 breaks γ-ties (no-collapse proven), the R19 switch all-or-none,
> and the traveling-wave **peak place** x*(f)=inverse-Greenwood is parameter-free **[F/V]**. The full
> dispersive **ENVELOPE** above (width/phase/cutoff/active gain) remains **[O]** — a passive envelope
> would require tuning Q (forbidden). *Naming note:* the `START_HERE` task is BLUEPRINT-E2 content
> delivered under the chronological `E1` folder; this slip is now **reconciled** and authoritative in
> `E_NUMBERING.md` (+ `e_numbering.json`, enforced by `tools/verify_seed.py` check [5]). Next: E2/E3 +
> the envelope [O]. See `FINDINGS.md`.
>
> **UPDATE (v0.7.0): the ENVELOPE [O] is now CHARACTERISED** — increment **E6**
> (`research/E6-traveling-wave-envelope/`) takes up exactly this open derivation. It does not close it by
> tuning Q; it proves the envelope is a **one-parameter family in Q** — every LOCATION (peak place = E1's
> place, apical-cutoff side, group-delay peak) is forced and Q-invariant, every MAGNITUDE (width = ω0/Q
> exactly, height, slope, absolute delay) scales with Q and is fixed by no inherited constant — so Q is
> the **single irreducible [O]**, and a number for it would be tuning. The black box is now a
> characterised box. So this envelope slot is delivered as BLUEPRINT-E1 CONTENT under the unambiguous
> E6 folder name (folders are not renamed — frozen-hash / no-omission — and the slip is now **reconciled**
> in `E_NUMBERING.md`). See
> `research/E6-traveling-wave-envelope/FINDINGS.md`.

**E2 — the mechanotransduction switch.** Hair-cell MET (**TMC1 · PCDH15 · CDH23 · TMIE**, γ
measured) as the **tip-link gating spring = R19 switch**: stereocilia deflection → open-probability
flip (discontinuous past spinodal). Emerge the hair-cell lineage via the `Organ`: order =
argsort(spinodal(γ)), dwell ∝ γ^1.5, **using the A4 SHAPE to break γ-ties**. [V] structure; absolute
SPL→Hz scale [O].

**E3 — the active amplifier.** Prestin (**SLC26A5**, γ measured) somatic motility at the Hopf
bifurcation: the cube-root (1/3) compression is parameter-free [V]; otoacoustic emissions as the
amplifier's signature.

> **STATUS (v0.4.0): E3 is DELIVERED** — the cochlear amplifier (prestin / `SLC26A5`) emerged as the
> inherited R19 cubic **at its critical point** (`research/E3-cochlear-amplifier/`): the response
> **compresses as the parameter-free cube root** `r ∝ F^(1/3)` (proven as the analytic fixed point of
> the *inherited* cubic `sdot(s,0,F)`, residual <1e-12, then verified on the inherited integrator,
> exponent 0.333333), the gain falls as `F^(−2/3)` (exponent −0.666667), `SLC26A5` takes its place in
> the spinodal order (between PCDH15 and ATOH1), and every tonotopic place compresses by the SAME 1/3
> **[F/V]**. The keystone: the E1 transduction switch and the E3 amplifier are **one R19 cubic in two
> regimes** — bistable detection ∥ critical amplification. The absolute gain/dB/Q and the OAE
> amplitudes remain **[O]** (a number would require tuning — forbidden). Next: E4 + the envelope [O].
> See `research/E3-cochlear-amplifier/FINDINGS.md`.

**E4 — congenital DEAFNESS (the goal).** Each congenital-deafness gene — **GJB2, GJB6** (DFNB1,
the commonest), **OTOF** (auditory neuropathy), **USH2A, MYO7A** (Usher) (loaded) + **SLC26A4,
LHFPL5, MYO15A** (to fetch) — as an R19/transduction **failure mode**. Direction-only hypotheses
under the firewall; the research aim is the **substrate-inverse lever** — proposal-only. The felt
percept of sound is deferred to the **mind** volume.

> **STATUS (v0.5.0): E4 is DELIVERED** — congenital deafness emerged as the inherited R19 cubic's
> **failure-mode decomposition** (`research/E4-congenital-deafness/`). The cubic `ṡ = g·s − s³ + h`
> has exactly three failure loci + its critical regime; each deafness gene is assigned to ONE locus
> by its **cited protein function — never by γ** (the firewall), and the geometry then forces a
> *different* direction-only, proposal-only substrate-inverse lever per class **[F/V]**:
> **(1) DRIVE** (`h`: `GJB2`/`GJB6`/`SLC26A4`, endolymphatic power) — switch intact, RECOVERABLE by
> restoring `h` past +spinodal (intact `g`=γ_TMC1: h=0→OFF s=−1.1414, h=1.5·sp→ON s=+1.3864);
> **(2) STRUCTURE** (`g`: `LHFPL5`/`MYO15A`/`USH2A`/`MYO7A`/`TMC1`, the apparatus) — NOT drive-rescuable,
> an **honest negative**: the bistable window `2·spinodal(g)=4(g/3)^1.5` is monotone in `g` and →0
> (2·sp(0.01)=0.00077), the hysteresis loop collapses to the grid floor — drive cannot restore a
> window that structure destroyed; **(3) READOUT** (`OTOF`/auditory neuropathy) — the switch flips
> normally, the cubic sees nothing wrong, the broken layer is the downstream synapse **[O]**;
> **(4) AMPLIFIER** (`SLC26A5`/prestin) — the E3 bridge, loss of criticality loses the `F^(−2/3)` gain
> (re-verified −0.666667). The firewall is **quantified**: drive-class γ∈[1.3612,1.5375] and
> structure-class γ∈[1.2801,1.5086] **overlap by 0.1474**, so no single γ-threshold can assign class —
> γ reads structure only. Three new genes (`SLC26A4` 1.3612, `LHFPL5` 1.4043, `MYO15A` 1.4960) fetched
> from NCBI; the inherited cache + atlas re-frozen deliberately (ledger note). Six honest negatives
> N1–N6 preserved. Gate: 7/7 PASS. Next: the envelope [O], fold TMC2, extend the OTOF readout class.
> See `research/E4-congenital-deafness/FINDINGS.md`.

**E5 — the READOUT substrate (otoferlin / OTOF): E4's [O] turned into a modelled failure.** E4 left the
READOUT class (OTOF / auditory neuropathy) as an honest **[O]** — "the switch flips fine; the broken
layer is downstream." E5 supplies that downstream layer and composes it with the **frozen** cubic.

> **STATUS (v0.6.0): E5 is DELIVERED** — the auditory-neuropathy READOUT class is now **modelled**
> (`research/E5-readout-synapse/`). The keystone is structural and forced: the readout **cannot** be the
> R19 cubic — release is **non-negative, monotone, saturating, and NON-bistable** (zero hysteresis), so
> the minimal form is a **rectified saturating Ca²⁺ sensor**, a DIFFERENT substrate downstream of the
> switch (this is the provable reason E4's cubic is blind to OTOF). Composed with the frozen switch it
> forces three results: **(1)** auditory neuropathy = a sound flips the switch to **s=+1.3864 — identical
> in a hearing AND an OTOF ear** (the substrate sees nothing wrong) but the removed sensor zeroes release
> (0.5810 → 0.0000); **(2)** the auditory-nerve rate inherits the **composed exponent `F^(m/3)`** = the
> E3 amplifier cube-root (1/3) × the synaptic cooperativity m (cited [L]), fit to m/3 at machine
> precision; **(3)** the **OAE⁺/ABR⁻** clinical signature is forced by separable stages (amplifier E3/OHC
> intact ∥ readout E5/IHC-synapse zeroed). The OTOF lever DIRECTION — left [O] by E4 — is now **forced**:
> restore the **readout stage**, not (g,h). Every magnitude stays **[O]**; **no constant tuned**; and
> **no inherited byte changed** (no re-freeze — clean no-regression). Six honest negatives N1–N6. Gate:
> 7/7 PASS. Next: the envelope [O], fold TMC2, the E-numbering reconciliation, the HTML volume. See
> `research/E5-readout-synapse/FINDINGS.md`.

**E6 — the traveling-wave ENVELOPE (BLUEPRINT-E1 content): the seed's deepest [O], characterised.** The
inherited wave module names the fluid-loaded dispersive cochlear traveling-wave **envelope** as the open
derivation the seed exists to take up. E1 forced its peak place; E6 takes up its shape — without tuning.

> **STATUS (v0.7.0): E6 is DELIVERED** — the cochlear traveling-wave envelope is turned from a black box
> into a **characterised** one (`research/E6-traveling-wave-envelope/`). Modelling the partition near its
> place as a driven damped resonator on the **frozen** Greenwood CF(x), the single-pole velocity response
> forces: **(1)** the **peak sits at ω0=CF(x) for every Q** — exactly E1's inverse-Greenwood place
> (|Δ|=0.0000), the FORM is the universal single pole; **(2)** the partition reactance `χ=1−(f/CF)²` flips
> sign at CF, forcing a propagating basal tail and an **evanescent APICAL CUTOFF** — the asymmetry SIGN is
> forced and robust to the decay scale κ; **(3)** the −3 dB velocity bandwidth is **exactly ω0/Q** (to
> machine precision, |Δ|≈1e-16); **(4)** the active amplifier is **negative damping** `Q_eff=Q0/(1−G)`
> whose critical point is the inherited **E3 cube root** (exponent 0.333333); **(5)** the group delay
> **peaks at CF** with magnitude 2Q/ω0. The keystone: the whole envelope is a **one-parameter family in
> Q** — every LOCATION (peak place, cutoff side, delay peak) is forced and Q-invariant, every MAGNITUDE
> (width, height, slope, absolute delay) scales with Q and is fixed by **no inherited constant** (the
> √-law fixes the place, the wave speed fixes propagation, γ is structure-only by firewall — not a
> damping) — so Q is the **single irreducible [O]**, and a closed numeric envelope would require **tuning
> it** (forbidden). E6 does NOT close the [O]; it CHARACTERISES it: FORM forced, exactly ONE scalar Q
> open. Every magnitude stays **[O]**; **no constant tuned**; **no inherited byte changed** (no re-freeze
> — clean no-regression). Seven honest negatives N1–N7 (sharpness Q, cutoff slope dB/oct, active-gain
> magnitude = E3 [O], absolute delay/phase/wave-speed, the long-wave/WKB approximation, two-tone
> suppression/distortion products, the felt percept → mind). Gate: 7/7 PASS. *Naming note:* delivered as
> BLUEPRINT-E1 CONTENT under the E6 folder; folders are not renamed (frozen-hash / no-omission), and the
> v0.3.0 E-numbering slip is now **reconciled** and authoritative in `E_NUMBERING.md` (enforced by verifier
> check [5]). Next: fold TMC2, the HTML
> volume. See `research/E6-traveling-wave-envelope/FINDINGS.md`.

**E7 — the audible BAND (why only certain frequencies are heard): the GEOMETRY that carves the
passband.** *(PLANNED — added v0.7.1; the forced core below is verified, the increment is not yet built.)*
The inherited foundation already states that sound and light share **one** elastic-wave law: light is the
jammed lattice's elastic wave `c²=B/ρ` (physics **§SP**, the lattice stiffness B), the speed of sound in
air is `vₛ=√(γP/ρ)` (physics **§K**, air's adiabatic stiffness), and the local cochlear resonance is
`ω(x)=√(S(x)/m)` — the SAME `√(stiffness/inertia)`. E1 forced the place-map SHAPE; E6 characterised the
envelope. But **why the audible range has EDGES** — why we hear ~20 Hz–20 kHz and not 1 Hz or 1 MHz — is
currently only a *cited calibration span* `[L]` (the Greenwood A/a/k). E7 derives the band as a
**geometry-carved bandpass**, in the same forced-form / `[O]`-magnitude discipline as E6.

> **The forced core (already verified).** Because the resonance obeys the √-law (`CF ∝ √S`), the total
> span in **octaves** is exactly **half** the log₂ of the basilar-membrane **stiffness ratio**:
> **`N_oct = ½·log₂(S_base/S_apex)`** — parameter-free **[F]**. For the human cochlea this gives **~10
> octaves** from a stiffness ratio **~10⁶** (verified against the inherited Greenwood constants: span
> **10.025 oct** ⟺ implied ratio **1.085×10⁶**, exact). So *"why ~10 octaves"* is forced once the stiffness
> ratio is known; *"why a ratio of ~10⁶"* is the BM's graded geometry (it widens and thins ~base→apex) —
> a **measured** input, never a fit. The √-law **halves** the stiffness decades into octaves.

The two band EDGES are each a forced **topological** rolloff with an `[O]` corner — exactly a bandpass =
high-pass × low-pass:
- **LOW edge (high-pass) — the helicotrema.** The apical hole joining the two scalae short-circuits slow
  (DC-ward) pressure: below a corner frequency the pressure equalises through it before a traveling wave
  forms. The **existence and side** (a low-frequency rolloff) are **forced** by the topology (a hole at the
  apex); the **corner** is `[O]` (needs helicotrema area + cochlear compliance). In the inherited Greenwood
  map this same apical relief is the offset term `−A·k`, which (verified) bends the apical end **down ~3
  octaves to ~20 Hz**; the constant k is `[L]`.
- **HIGH edge (low-pass) — the middle ear + the basal stiffness ceiling.** The ossicular chain
  (malleus/incus/stapes) has **mass**; an inertia in the drive path is a mechanical **low-pass** that rolls
  off the top before it reaches the cochlea. And the stiffest place (the base) fixes the absolute ceiling
  `CF_max=(1/2π)√(S_base/m)`. The **existence and side** (a high-frequency rolloff) are **forced** (a mass →
  low-pass; a finite max stiffness → finite CF_max); the **corner / CF_max** value is `[O]`.

So the audible band is the **product** of (a) the place-map passband, (b) a helicotrema high-pass, (c) a
middle-ear low-pass — a **bandpass whose SHAPE and the SIGN of each edge are forced by geometry**, while
the three corner magnitudes are `[O]` (a number = tuning). This is the precise cochlear analogue of how a
sensory band sits inside the lattice's elastic-wave behaviour, and the same discipline as E6 (form forced,
magnitudes `[O]`). **The ear's band is a geometry problem on top of the inherited wave law — not a new
physics.** *Grades:* `N_oct=½·log₂(ratio)` **[F]**; edge SIGNS (helicotrema high-pass, middle-ear low-pass)
**[F]**; absolute edges CF_min/CF_max, the two corners, k — `[O]`/`[L]`. *Firewall:* γ is structure-only
(never a stiffness, a corner, or an area); loudness/pitch RANGE as *experience* → **mind**; no number tuned.

> **STATUS (v0.8.0): E7 is DELIVERED** — the audible band is EMERGED as a **geometry-carved bandpass** on
> the inherited `√(stiffness/inertia)` wave law (`research/E7-audible-band/`), in the same forced-form /
> `[O]`-magnitude discipline as E6. The **keystone** `N_oct = ½·log₂(S_base/S_apex)` is verified **exact**
> (the √-law HALVES the stiffness decades into octaves): on the inherited Greenwood map the apex/base CFs
> (19.848 Hz / 20677.07 Hz) give a **10.0248-octave** span ⟺ an implied stiffness ratio **1.085×10⁶**, with
> `½·log₂(S_ratio)` returning the span to |Δ|=0.0. The span decomposes cleanly: the bare `10^(a·x)` term =
> `a·log₂(10)` = **6.976 oct**, + a **3.059-oct** helicotrema apical bend, − a 0.010-oct basal effect =
> 10.025 oct. The **LOW edge** is a **helicotrema high-pass**: the inherited `−A·k` offset is a LOW-END-only
> relief (fractional weight 0.88 apex vs 0.0070 base, ratio = 10^a exactly) bending the apex DOWN ~3 oct to
> ~20 Hz, and the apical hole forces a lows-cut SIDE (monotone high-pass, robust to the order). The **HIGH
> edge** is a **middle-ear low-pass**: the ossicular MASS forces a highs-cut with a **−12 dB/oct** (slope
> −2.000) asymptote robust to the damping ζ, and the stiff base fixes a **finite** ceiling
> (CF_max=20677 Hz; the inherited place map is strictly increasing apex→base and finite at the base). The
> band is the **product** of the three — a unimodal bandpass whose SHAPE and every edge SIGN are forced by
> geometry, while the absolute edges and three corners are the irreducible measured-geometry `[O]` (a number
> for any = tuning). Every magnitude stays **[O]**; **no constant tuned**; **no inherited byte changed** (no
> re-freeze — clean no-regression). Seven honest negatives N1–N7. Gate: 7/7 PASS. *Naming note:* delivered
> as BLUEPRINT-E7 content under the unambiguous E7 folder; folders are not renamed (full map in
> `E_NUMBERING.md`). Next: E8 (band-specific
> hearing loss — now DELIVERED in v0.9.0), fold TMC2, the HTML volume. See
> `research/E7-audible-band/FINDINGS.md`.

**E8 — band-specific / frequency-selective hearing loss (WHERE on the map fails): E4's class-axis ×
E7's place-axis.** *(DELIVERED in v0.9.0 — see the status block below.)* E4 answered **which** cubic locus fails
(drive / structure / readout / amplifier). E7 supplies the **place** axis (which frequency sits where). A
real audiogram is frequency-**selective** — loss concentrated in a band — so a disease is a **2-D** object:
a failure **class** acting over a **band of places**. E8 composes the two axes (direction-only,
proposal-only, firewall) to explain the characteristic audiogram **shapes** the seed does not yet touch:
- **High-frequency (down-sloping) loss — presbycusis, many ototoxic & genetic losses.** The **basal**
  (highest-CF, stiffest, highest-throughput, first-built) end is the most metabolically/mechanically
  stressed and degenerates first → basal places fail first → a high-frequency loss. *Direction* forced
  (basal-first vulnerability ⇒ down-sloping); slope/threshold/age magnitudes `[O]`.
- **The 4 kHz "notch" — noise-induced hearing loss.** A specific mid-high **notch**, not the very top.
  Candidate forced reason (to test): the external/middle-ear transfer peaks near ~3–4 kHz (E7's low-pass
  shaping + ear-canal resonance), concentrating energy at the place tuned there → that band over-drives and
  fails first. *Direction*-only; the exact notch place `[O]`.
- **Mid-frequency ("cookie-bite") loss — several congenital/genetic forms.** A loss centred in the
  **middle** of the map with better edges → points to a locus tied to a mid-cochlear gradient, not the base
  or apex. *Direction*-only.
- **Low-frequency / reverse-slope loss — e.g. WFS1/Wolfram low-frequency SNHL, fluctuating low-freq loss.**
  The **apical** (low-CF) end fails preferentially → an up-sloping audiogram → an apical-specific locus
  (the region where the helicotrema relief and endolymph regulation dominate). *Direction*-only.

Each pattern is a **(class × band)** hypothesis: which of E4's loci, acting over which of E7's place bands,
reproduces the audiogram **shape**. **Proposal-only, direction-only** — no molecule, dose, diagnosis, or
efficacy; the substrate-inverse lever is named only as a *direction* (restore which locus, at which band).
*Grades:* the **(class × band) decomposition** and the audiogram-shape **directions** **[F]**/`[O]`; all
thresholds, slopes, notch-places, and ages `[O]`; firewall verbatim; the felt experience → **mind**.

> **STATUS (v0.9.0): E8 is DELIVERED** — band-specific / frequency-selective hearing loss is EMERGED as a
> **2-D (class × band) object** by composing E4's failure-CLASS axis with E7's PLACE axis
> (`research/E8-band-specific-loss/`), in the same forced-direction / `[O]`-magnitude discipline as E6/E7.
> The **keystone** is that the inherited place map `CF(x)` is strictly **monotone**, so the place→frequency
> map is an **order-isomorphism**: a contiguous band of FAILED PLACES maps to a contiguous band of LOST
> FREQUENCIES, order preserved, and `inv_greenwood` maps it back **exactly** (verified `|Δ|<1e-9` for the
> basal/mid/apical bands). So the audiogram SHAPE **is the image** of *where* the failure concentrates:
> **basal → high-frequency down-slope** (presbycusis — the base cycles fastest, `CF` *is* the rate, so
> cumulative load is basal-first, load(base)/load(apex)=1042×); **apical → low-frequency reverse-slope**
> (WFS1/ion regime — the apex is the helicotrema-relief/ion-regulation end); **mid → cookie-bite** (the
> isomorphism's mid-place→mid-frequency, the locus's mid-concentration cited `[L]`, the honestly weakest of
> the four); and a localized **over-drive at the outer/middle-ear transfer peak → a notch BELOW the top**
> (the transfer = canal resonance × the E7 ossicular low-pass is unimodal with an interior peak below
> CF_max, mapping to an interior place — the ~3–6 kHz C5-dip). The lever is the **E4 direction applied at the
> E7 band** (a 2-D direction), **proposal-only**; and E4's honest negative **carries** — a structure-class
> high-frequency loss has **no drive rescue** (the bistable window `2·spinodal(g)→0` as `g→0`). Every
> DIRECTION is forced; every threshold, slope, notch-Hz, and age stays **[O]** (a number = tuning); **no
> constant tuned**; **no inherited byte changed** (no re-freeze — clean no-regression). Seven honest
> negatives N1–N7. Gate: 7/7 PASS. *Naming note:* delivered as BLUEPRINT-E8 content under the unambiguous E8
> folder; folders are not renamed (full map in `E_NUMBERING.md`; the E-numbering slip is now reconciled and
> verifier-enforced). Next: fold **TMC2**, the HTML volume. See
> `research/E8-band-specific-loss/FINDINGS.md`.

**A4 — the FULL A4 anchor/loop/anchor-relative-phase READ (a READING deepening, not a wave E-chapter):
the FIREWALL's one named, deferred [O], now MEASURED.** Every prior increment read each master-gene
promoter as **γ (LEVEL) + the promoter-scale A4 SHAPE**; the firewall flagged exactly one thing as
deferred — the **FULL** A4 coordinate (wide-neighbourhood shell, nearest architectural anchor, real
motors/loops, anchor-relative helical phase) — because it needs *the wider region + an NCBI feature table
(rettype=ft)*. This increment supplies those two measured inputs and runs the **inherited** grammar on
them. It ships in folder `research/A4-anchor-loop-phase/` — a reading deepening, **not** an E-wave
chapter, so it is correctly **outside** the E-numbering map (verifier check [5] scans `research/E*/` only).

> **STATUS (v0.12.0): A4 is DELIVERED — the named [O] is now MEASURED, not invented**
> (`research/A4-anchor-loop-phase/`). The key realisation: the [O] was a missing **MEASUREMENT**, not
> missing machinery — the inherited grammar (`dna_interpreter` + `key_pipeline_full`) **already** contained
> every function the full read uses (`run_key`, `build_anchors`, `parse_ft_motors`, `build_loops`,
> `helix_coord`). So `tools/fetch_region_features.py` fetched, per gene, the frozen promoter window EXTENDED
> by a single gene-independent **FLANK=20000 bp** each genomic side (the wide region + the feature table over
> the same region, strand-corrected); `inherited/ear_regions.cache.json` caches the raw bytes; and the new
> module recomputes the full A4 coordinate **offline, deterministically** by importing that grammar — **no
> new machinery, no new number**. **Result:** the **keystone** `region[FLANK:FLANK+2501]` == the frozen
> promoter **byte-for-byte 19/19** (the wide read sits on the unchanged γ layer, ZERO drift); every TSS now
> carries a real wide-neighbourhood **shell** (18/19 stiff; TMC1 the AT-rich exception), a real nearest
> **anchor**, real feature-table **motors joined as loops (19/19 carry ≥1)** — fulfilling the
> `dna_interpreter` promise *anchors-only → real motors+loops* on MEASURED annotation — and a real
> anchor-relative **B-DNA phase** (3/19 contact-competent: EYA1, PCDH15, SLC26A4). The read is **mostly
> window-stable** under a 2× sub-window shrink of the SAME fetch (motor existence **19/19**, shell class
> **15/19**, contact sign **16/19**) — so it is NOT a FLANK artifact for the majority; the boundary-near
> minority that flips is the named **window-relative [O]**. **No clean numeric closure is claimed** (that
> would be tuning): the absolute FLANK/distances/counts and boundary-near class/sign are window-relative
> `[O]`, "anchor" is a mechanical stiffness-boundary **proxy** (not a measured CTCF/cohesin site — Hi-C/ChIP
> `[O]`), "loop" is a geometric join (not a measured Hi-C contact), the phase uses **idealised** constant
> twist (sequence-dependent twist/supercoiling/nucleosome phasing `[O]`), and Layer-2 stays flagged — each
> obstacle named **N1–N7**. **No constant tuned.** Governance: **one** new frozen artifact added
> **deliberately** (`inherited/ear_regions.cache.json`, recorded as a new key in `FROZEN_SHA256.json` + the
> ledger); the **8 pre-existing inherited bytes are byte-identical** (NO re-freeze). Gate: **7/7 PASS**;
> master `verify_seed.py` PASS (9 frozen files, 76 artifacts). Next: deploy `docs/`; the deeper residue
> (wet-lab contact map, sequence-dependent twist) stays honestly `[O]`. See
> `research/A4-anchor-loop-phase/FINDINGS.md`.


## What is forced vs measured vs open (grading discipline, VP-SPEC C3)
- **[F] forced / [V] verified:** the wave emergence (c=√(B/ρ)), the spatial-code SHAPE, the R19
  switch structure, the emergence order argsort(spinodal(γ)), and the DNA reading **γ (LEVEL) + A4
  (SHAPE)** with its orthogonality A4 = signal − γ.
- **[L] measured/calibrated:** every γ (from NCBI), the absolute place/angle calibration constants.
- **[O] open:** absolute magnitudes (photon/SPL → firing Hz), the full traveling-wave hydrodynamics
  (ear) — E6 (v0.7.0) characterised the near-peak envelope FORM and reduced its openness to the single
  scalar Q, but the full 2-D/3-D fluid problem and a number for Q remain **[O]**; the full A4
  anchor/loop/anchor-relative-phase was the firewall's named deferred read and is now **MEASURED in
  v0.12.0 (A4)** (wider region + NCBI feature table fetched for all 19 genes, the inherited grammar making
  the read — keystone 19/19, real motors+loops 19/19, no number invented), with the residual staying
  **[O]** and named: the absolute magnitudes / boundary-near class+sign are window-relative, the
  architectural "anchor"/"loop" are mechanical/geometric proxies awaiting a wet-lab contact map
  (Hi-C/ChIP), and the helical phase uses idealised constant twist (sequence-dependent twist **[O]**); the
  felt percept (→ mind volume).
  Each [O] names its obstacle in the research ledger.

## Definition of done for the FULL volume (what this seed grows into)
A multi-chapter HTML volume (VP-SPEC v1.8 §6) where every displayed number is reproduced
deterministically (2×sha256, HTML↔code drift 0), every γ is measured-and-cached, the disease layer
is proposal-only under the firewall, and `verify_*` passes — delivered as **one zip**.
