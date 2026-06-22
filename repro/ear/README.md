# vp_ear_emergence_seed — v0.11.0  (research SEED + HTML volume)

A self-contained **starting package** for properly emerging the **ear (hearing)** from first
principles, for research toward the congenitally affected. Author: Young Jae Lee
(ORCID 0009-0002-7535-8245) · Licence CC BY 4.0 · Governed by **VP-SPEC v1.8** (bundled).

This is a SEED, not a finished volume: it ships the **verified foundation**, the **measured
inputs**, and a **working research pipeline**, plus the blueprint of what to build. The
emergence work itself is the research this package launches (see `BLUEPRINT.md`).

**v0.11.0 — the volume is now CITABLE (its own concept DOI is minted) and the E-numbering is RECONCILED.**
Two gate-clean closeouts, no inherited byte changed. **[A]** This volume's own **concept DOI**
**`10.5281/zenodo.20790201`** is minted (the same author/ORCID Zenodo workflow as the sibling volumes), so
every "pending Zenodo deposit" placeholder is replaced: the `docs/` footer links the concept DOI, `llms.txt`
cites it, and the structured data (JSON-LD) on all 11 pages now carries it as `identifier` + `sameAs` —
closing the VP-SPEC v1.8 requirement the volume had left open. The DNA-volume DOI (`10.5281/zenodo.20471407`)
is still cited as the *readable-layer source*; deployment to `jamming-physics.org/ear` is still honestly
"pending". The drift-0 gate is unaffected (81 numbers, drift 0; 145 links resolve). **[B]** Open item #4 —
the E-numbering slip flagged since v0.3.0 — is **reconciled**: a new authoritative map (`e_numbering.json`)
and `E_NUMBERING.md` record that research folders follow a **chronological-build-order** convention that
matches BLUEPRINT-canonical numbering for E3/E4/E5/E7/E8 and differs in exactly two places by design (folder
`E1` carries BLUEPRINT-**E2**, the MET switch; folder `E6` carries BLUEPRINT-**E1**, the envelope). No folder
is renamed; instead the verifier gains block **[5] E-NUMBERING CONSISTENT** that enforces the map against the
filesystem and `seed.json`, so the labels can never silently drift. Two artifacts added (now **70**); no
foundation module added; **no re-freeze** (only v0.9.1's deliberate TMC2 re-freeze stands). `SEED VERIFY: PASS`.

**v0.10.0 — the seed is now also a deterministic HTML VOLUME (`docs/`, built by `volume/`).**
The complete research chain is published as an 11-page static site per VP-SPEC v1.8 §6: a hub, the
**7 chapters** (§1 place map & MET switch · §2 cochlear amplifier · §3 congenital deafness · §4 readout
synapse · §5 traveling-wave envelope · §6 audible band · §7 band-specific loss), and **3 locked-concept
pages**. The no-tuning rule is enforced *structurally*: every number on every page is produced only by
`volume/tools/vp_numeric_ssot.py` — which imports the **frozen** foundation and **verified** E-modules
and calls the very functions they use (nothing re-typed or fitted) — and `volume/tools/gate_volume.py`
re-derives each one and asserts **HTML↔code drift = 0** (81 numbers, drift 0), alongside 2×-process
determinism, byte-identical on-disk⟷builder output, per-page structure (JSON-LD, canonical, answer-first,
honest-negatives, firewall), no-omission, and all internal links resolving. Build/gate/view commands are
below. **No inherited byte changed** (no re-freeze); this volume's own snapshot DOI is *pending Zenodo
deposit* (the footer cites the real DNA-volume DOI as the readable-layer source).

**v0.9.1 — atlas completion: the last gene TMC2 is folded; the ear readable layer is now COMPLETE (deliberate re-freeze).**
The atlas `_to_measure` held one deferred gene — **TMC2**, the second MET pore-forming subunit
(mechanotransduction node, STRUCTURE class, paralog of TMC1). It is now **measured and folded in**, taking the
atlas to **19** master genes, each carrying γ (LEVEL) + A4 (SHAPE), all MEASURED — `_to_measure` is now **empty**.
TMC2 was **not invented**: it was fetched by `tools/fetch_promoter_gamma.py` from NCBI nuccore (GRCh38, chr20
`NC_000020.11`, gene 117532, TSS−2000..+500, 2501 bp), **two independent live fetches returned byte-identical
sequence**, and its γ recomputes offline bit-for-bit (γ=1.4160; the fetcher's `gamma_of` and the canonical
`dna_interpreter.gamma` agree; A4 = signal − γ holds, |mean(shape)|=0.0). The two affected inherited files
(`ear_promoters.cache.json`, `organ_gamma.json`) had their hashes re-frozen in `inherited/FROZEN_SHA256.json`
**deliberately** (key deleted, new hash recorded; old→new in `INHERITANCE_LEDGER.md`); the other six inherited
hashes are byte-identical to seed time. **Read-only observation (no tuning):** in the emergence order =
argsort(spinodal(γ)), TMC2 lands at **#8/19** (between LHFPL5 and OTOF), far ahead of its paralog **TMC1 at
#2/19** — the two MET pores differ by Δγ=+0.1132 and carry **opposite A4 skew**, so the same family is **not
interchangeable at the readable layer** (γ alone would be lossy). No constant was fitted; the firewall holds
(TMC2's γ is a promoter-structure LEVEL, never a channel gain, dose, or clinical effect). No new files (still 48
artifacts); `SEED VERIFY: PASS` over 19 genes. Everything else is byte-identical to v0.9.0.

**v0.9.0 — increment E8 delivered (band-specific hearing loss — E4's class axis × E7's place axis).**
Frequency-**selective** audiograms are EMERGED as a **2-D (class × band) object** (`research/E8-band-specific-loss/`):
a disease is a failure **class** acting over a **band of places**. The **keystone** is that the inherited
place map `CF(x)` is strictly monotone, so place→frequency is an **order-isomorphism** — a contiguous band of
failed places maps to a contiguous band of lost frequencies, order preserved, `inv_greenwood` mapping it back
exactly (`|Δ|<1e-9`). The audiogram SHAPE *is the image* of *where* the failure sits: **basal → high-frequency
down-slope** (presbycusis — the base cycles fastest), **apical → low-frequency reverse-slope** (WFS1/ion
regime), **mid → cookie-bite** (the weakest — mid→mid forced, the locus's mid-concentration cited), and a
localized **over-drive at the outer/middle-ear transfer peak → a notch below the top** (the ~3–6 kHz C5-dip).
The lever is the E4 direction at the E7 band, **proposal-only**; E4's honest negative carries (no drive rescue
for a structural high-frequency loss). Every DIRECTION forced; every dB/slope/notch-Hz/age `[O]`; seven honest
negatives N1–N7; gate 7/7 PASS; **no inherited byte changed** (no re-freeze). One foundation module registered,
four artifacts added (now 48).

**v0.8.0 — increment E7 delivered (the audible BAND — a geometry-carved bandpass on the inherited wave law).**
*Why only ~20 Hz–20 kHz is heard* is DERIVED (`research/E7-audible-band/`) in the same forced-form /
`[O]`-magnitude discipline as E6. The **keystone** `N_oct = ½·log₂(S_base/S_apex)` is verified **exact** (the
√-law HALVES the stiffness decades into octaves): the inherited Greenwood apex/base (19.848 Hz / 20677.07 Hz)
give a **10.0248-octave** span ⟺ a stiffness ratio **1.085×10⁶**, `½·log₂(S_ratio)` closing to |Δ|=0.0. The
**low edge** is a helicotrema high-pass (the `−A·k` offset is a LOW-END-only relief, fractional-weight ratio =
10^a, bending the apex down ~3 oct to ~20 Hz); the **high edge** is a middle-ear low-pass (the ossicular MASS
forces a **−12 dB/oct** highs-cut, ζ-robust) plus a finite basal ceiling (CF_max=20677 Hz). The band is the
unimodal **product**, SHAPE + every edge SIGN forced, the absolute edges/corners the irreducible
measured-geometry `[O]` (a number = tuning). Seven honest negatives N1–N7; gate 7/7 PASS; **no inherited byte
changed** (no re-freeze). One foundation module registered, four artifacts added (was 40 → 44).

**v0.7.1 — BLUEPRINT expansion (plan only; no new code, no inherited byte changed).** Two new increments
were specified in `BLUEPRINT.md` to close a real gap — *why only certain frequency bands are audible*, and
the band-specific diseases: **E7 — the audible BAND** (the audible range derived as a **geometry-carved
bandpass** on the inherited `√(stiffness/inertia)` wave law; the forced, parameter-free core
`N_oct = ½·log₂(S_base/S_apex)` is verified — a stiffness ratio ~10⁶ gives the human ~10-octave span — with
the low edge a helicotrema high-pass and the high edge a middle-ear low-pass, edge SIGNS forced, corners
`[O]`); and **E8 — band-specific hearing loss** (frequency-selective audiograms as E4's failure-class axis
× E7's place axis: presbycusis high-frequency, the 4 kHz noise notch, cookie-bite mid-frequency,
low-frequency/reverse-slope). Both are **planned**, not yet built; the deliverable is the updated blueprint.
Everything else is byte-identical to v0.7.0.

**v0.7.0 — increment E6 delivered (the traveling-wave ENVELOPE — the seed's deepest [O], characterised
without tuning).** The inherited wave module names the fluid-loaded dispersive traveling-wave **envelope**
as *"the named [O] this seed exists to take up"*: E1 forced its **peak place**, but its shape, asymmetry,
sharpness, and delay were open. E6 takes it up the only honest way — it does **not** pick a sharpness
(that is tuning, forbidden); it **characterises** the obstacle. Modelling the partition near its place as
a driven damped resonator on the **frozen** Greenwood CF(x), the single-pole velocity response forces:
**(1)** the **peak sits at ω0=CF(x) for every Q** — exactly E1's place (|Δ|=0.0000); **(2)** the partition
reactance `χ=1−(f/CF)²` flips sign at CF, so a tone **propagates basal** and is **cut off apical** of its
place — the asymmetry SIGN is forced and κ-robust; **(3)** the −3 dB velocity bandwidth is **exactly
ω0/Q** (machine precision); **(4)** the active amplifier is **negative damping** `Q_eff=Q0/(1−G)`, landing
at criticality on the inherited **E3 cube root**; **(5)** the group delay **peaks at CF** with magnitude
2Q/ω0. The keystone: the envelope is a **one-parameter family in Q** — every LOCATION (peak place, cutoff
side, delay peak) is forced and Q-invariant, every MAGNITUDE (width, height, slope, absolute delay) scales
with Q and is fixed by **no inherited constant** — so Q is the **single irreducible [O]**, and a closed
numeric envelope would require **tuning** it. The black box is now a characterised box: not a number, but
a precise statement of which one number is irreducibly open and why. Every magnitude stays **[O]**, **no
constant is tuned**, and **no inherited byte changed** (no re-freeze — clean no-regression). Run
`python3 research/E6-traveling-wave-envelope/run.py` and its `gate.py` (7 checks). See that folder's
`FINDINGS.md` for the results and the seven honest negatives.

**v0.6.0 — increment E5 delivered (the readout substrate — E4's [O] turned into a modelled failure).**
E4 left the READOUT class (`OTOF` / auditory neuropathy) as an honest **[O]** — "the switch flips fine;
the broken layer is the downstream synapse." E5 supplies that layer. The keystone is **forced**: the
readout **cannot** be the R19 cubic, because release is **non-negative, monotone, saturating, and
NON-bistable** (zero hysteresis) — so the minimal form is a **rectified saturating Ca²⁺ sensor**
(otoferlin), a genuinely *different* substrate downstream of the switch. That is the provable reason the
E4 cubic is blind to OTOF. Composed with the **frozen** switch it forces three results: **(1)** auditory
neuropathy = a sound flips the switch to **s=+1.3864, identical in a hearing AND an OTOF ear** (the
substrate sees nothing wrong), but the removed sensor zeroes release (0.5810 → 0.0000); **(2)** the
auditory-nerve rate inherits the **composed compression exponent `F^(m/3)`** = the E3 amplifier cube-root
(1/3) × the synaptic Ca²⁺-cooperativity m (cited [L]), fit to m/3 at machine precision; **(3)** the
**OAE-present / ABR-absent** clinical signature is forced by *separable stages* (the amplifier E3 / outer
hair cell intact ∥ the readout E5 / inner-hair-cell synapse zeroed). The OTOF lever **DIRECTION** — left
[O] by E4 — is now forced: restore the **readout stage**, not the switch. Every magnitude stays **[O]**,
**no constant is tuned**, and **no inherited byte changed** (no re-freeze — clean no-regression). Run
`python3 research/E5-readout-synapse/run.py` and its `gate.py` (7 checks). See that folder's `FINDINGS.md`
for the results and the six honest negatives.

**v0.5.0 — increment E4 delivered (congenital deafness — the goal).** Congenital deafness is EMERGED
as the inherited R19 cubic's **failure modes**: the cubic `ṡ = g·s − s³ + h` has exactly three failure
loci plus its critical regime, and each deafness gene is assigned to ONE locus by its **cited protein
function** (never by γ — the firewall), which then forces a *different* direction-only, proposal-only
substrate-inverse lever per class. **DRIVE-class** (endolymphatic power: `GJB2`, `GJB6`, `SLC26A4`) —
switch intact, only `h` removed → RECOVERABLE in principle by restoring `h` past +spinodal. **STRUCTURE-
class** (apparatus: `LHFPL5`, `MYO15A`, `USH2A`, `MYO7A`, `TMC1`) — `g` collapses → an **honest negative**:
the bistable window `2·spinodal(g)=4(g/3)^1.5` is monotone in `g` and →0, so drive can NOT rescue a window
that structure destroyed. **READOUT-class** (`OTOF`/auditory neuropathy) — the switch flips normally, the
broken layer is the downstream synapse [O]. **AMPLIFIER-class** (`SLC26A5`/prestin) — the E3 bridge: loss
of criticality loses the `F^(−2/3)` gain. The firewall is *quantified*: drive- and structure-class γ-ranges
**overlap** (0.1474), so no single γ-threshold can assign class — proving γ reads structure only. Three new
master genes (`SLC26A4`, `LHFPL5`, `MYO15A`) were fetched from NCBI and the inherited cache re-frozen
deliberately (see `INHERITANCE_LEDGER.md`). Run `python3 research/E4-congenital-deafness/run.py` and its
`gate.py` (7 checks). See that folder's `FINDINGS.md` for the results and the six honest negatives.

**v0.4.0 — increment E3 delivered (the cochlear amplifier).** The outer-hair-cell active amplifier
(prestin / `SLC26A5`) is EMERGED as the inherited R19 cubic **at its critical point**: the response
**compresses as the parameter-free cube root** `r ∝ F^(1/3)` (the cubic's signature, not a fitted
constant), the gain falls as `F^(−2/3)` (the ear's ~120 dB dynamic-range compression), `SLC26A5` takes
its place in the spinodal order, and every tonotopic place compresses by the SAME 1/3. The keystone
insight: the E1 transduction switch and the E3 amplifier are **one cubic in two regimes** — bistable
detection ∥ critical amplification. Run `python3 research/E3-cochlear-amplifier/run.py` (self-hashes)
and `python3 research/E3-cochlear-amplifier/gate.py` (7 checks). See that folder's `FINDINGS.md` for
the result and the five honest negatives preserved as the E4 starting line.

**v0.3.0 — increment E1 delivered.** The tip-link MET switch (`TMC1 / PCDH15 / CDH23`) is EMERGED on
the place map: order = argsort(spinodal(γ)) with the A4 SHAPE breaking γ-ties, the R19 switch
all-or-none, the traveling-wave **peak place** parameter-free; the full dispersive ENVELOPE stays the
named [O]. Run `python3 research/E1-place-and-traveling-wave/run.py` and its `gate.py`.

## The one idea
The hearing sense reads a **wave** (sound (mechanical longitudinal)) and turns it into a spatial code, then an
all-or-none R19 transduction switch. Here the spatial code is **pitch by PLACE on the basilar membrane (ω=√(S/m), log-graded stiffness ⇒ exponential map)**. The whole
chain is grounded on the precise wave theory inherited from physics/chemistry — not assumed. Each
master gene is read from DNA as **γ (LEVEL) *and* its A4 coordinate (SHAPE)** — not γ alone (DNA
v1.13): γ is the window-mean of the stacking-stiffness signal, A4 is that same signal with the mean
removed (where the promoter is stiff vs soft relative to its own average). They are orthogonal —
neither contains the other — so reading γ alone is the compressed view this seed deliberately avoids.

## Verify everything with one command
```
python3 tools/verify_seed.py
```
Expected: `SEED VERIFY: PASS`. It checks (1) no-regression — inherited artifacts byte-identical
to the frozen seed; (2) the foundation reproduces deterministically; (3) the 19
master-gene readings — γ (LEVEL) **and** A4 (SHAPE) — recompute offline bit-for-bit, with the A4
orthogonality (A4 = signal − γ) asserted per gene; (4) no-omission — every promised artifact present;
(5) E-numbering consistent — the folder ⟷ BLUEPRINT-canonical map (`e_numbering.json`) agrees with the
filesystem and `seed.json`, so the reconciliation (open item #4) cannot silently drift (see `E_NUMBERING.md`).

## The HTML volume (`docs/`, built deterministically by `volume/`)
```
python3 volume/tools/build_volume.py    # writes docs/ (hub + 7 chapters + 3 concepts + sitemap/robots/llms.txt)
python3 volume/tools/gate_volume.py     # asserts HTML↔code drift 0; writes docs/gate.json; prints GATE: PASS
cd docs && python3 -m http.server       # view at http://localhost:8000
```
`volume/tools/vp_numeric_ssot.py` is the NUMERIC single-source-of-truth (also wired into the verifier as
a deterministic foundation module): it imports the frozen + verified code and computes every displayed
value by calling the same functions, so the prose **cannot** drift from the code. `volume/content/chapters.py`
holds the chapter text, with numbers written only as `[[KEY]]` placeholders the builder resolves against the
SSOT. The volume is static HTML with system fonts (offline-deterministic), grade-encoded colour
([F]/[V] green, [O] amber), a tonotopic navigation rail, JSON-LD on every page, and an AI-crawler-friendly
`robots.txt` + `llms.txt`. Canonical `jamming-physics.org/ear` URLs are forward-looking (deployment pending).

## Inherited foundation (verified, frozen — `inherited/`)
  - `inherited/vp_sound_wave.py` — sound = √(B/ρ) longitudinal wave + Greenwood-shape tonotopy
  - `inherited/vp_dna_reading.py` — γ (LEVEL) + A4 coordinate (SHAPE) per master gene
  - `inherited/vp_substrate.py` — the R19 bistable switch primitive (spinodal/barrier/Organ)
  - `inherited/dna_interpreter.py`, `inherited/key_pipeline_full.py` — the **canonical DNA v1.13 A4
    grammar** (γ, R19 switch, helix geometry, shells/anchors/robust_z), byte-identical to the source
  - `inherited/gamma_pipeline.py` — offline γ = −mean(SantaLucia-1998 NN ΔG37) recompute
  - `inherited/ear_promoters.cache.json` — 19 measured human promoter sequences (offline)
  - `inherited/organ_gamma.json` — the measured readable-layer atlas (γ LEVEL + A4 SHAPE) + extensions
  - `inherited/FROZEN_SHA256.json` — the no-regression hash set

## Research base (`tools/`)
  - `tools/fetch_promoter_gamma.py` — the WORKING NCBI fetcher (add a master gene → measured γ)
  - `tools/verify_seed.py` — the one-command gate

## HTML-volume tooling (`volume/`, output in `docs/`)
  - `volume/tools/vp_numeric_ssot.py` — deterministic NUMERIC single-source-of-truth (frozen+verified code → every displayed number)
  - `volume/content/chapters.py` — chapter content (numbers as `[[KEY]]`, never hand-typed)
  - `volume/tools/build_volume.py` — deterministic static-HTML builder (hub + 7 chapters + 3 concepts + SEO)
  - `volume/tools/gate_volume.py` — the HTML↔code drift-0 gate (writes `docs/gate.json`)

## Rules (binding)
  - **OUTPUT is always ONE zip.** Every session returns the whole package as a single archive.
  - **회귀금지 / no-regression.** Inherited values never drift; the verifier enforces byte-identity.
  - **누락금지 / no-omission.** Every promised artifact stays present; the verifier enforces it.
  - **No tuning.** Every constant is a measured input (cited) or a derived value — never fitted.
  - **Firewall** (`FIREWALL.md`): γ reads promoter STRUCTURE only; the felt percept is the mind
    volume's; nothing diagnoses, treats, or prescribes — every disease section is proposal-only.
