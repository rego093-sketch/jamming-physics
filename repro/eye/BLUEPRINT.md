# BLUEPRINT (청사진) — vp_eye_emergence_seed

## Scope & Safety — theoretical research, NON-CLINICAL (read first, above all tasks)

This program is **purely academic, theoretical computational research** — it is **not** a medical
product, **not** clinical or diagnostic software, and **not** medical advice. It derives the visual
sense from first principles (inherited wave physics + DNA γ measured from public NCBI promoter
sequences) and studies the **mechanism layer** of congenital vision conditions (Leber congenital
amaurosis, retinitis pigmentosa, achromatopsia) as a question in **physics and dynamical-systems
theory** — the R19 switch, the spatial code, the emergence order — graded honestly [F]/[V]/[L]/[O].

What this program studies is **structure only**. What it deliberately does **NOT** do (binding,
enforced by `FIREWALL.md`): it does **not** diagnose, treat, prescribe, screen, or triage; it
designs **no** molecule and states **no** dose, potency, selectivity, efficacy, or clinical effect;
**every disease section is direction-only and proposal-only**, behind a magnitude firewall that
blocks all quantitative clinical tokens. The felt percept is deferred to the mind volume. Nothing
here is intended for, or usable as, patient care or clinical decision-making.

**Purpose & value.** Open scholarship (CC BY 4.0, ORCID 0009-0002-7535-8245, governed by VP-SPEC
v1.8) toward a first-principles **theoretical understanding** of how vision emerges and how
congenital mechanisms fail. This is upstream basic research — the kind that may one day *inform*
future scientific work, never substitute for it. The blueprint's value is exactly this: a rigorous,
falsifiable, fully-reproducible theory of sensory emergence whose disease layer stays strictly
hypothesis-level. The firewall above is what keeps the work theoretical, and it is never relaxed.

**Goal.** Reveal, **step by step and in full mechanistic detail, the complete down-conversion ladder**
by which the eye turns the **high-frequency light band** (a ~10¹⁴ Hz electromagnetic carrier) into the
**low-frequency neural band** (a ~10–100 Hz spike code) — the central question of how a special sense
works at all. The eye is the **core sensory organ**; the same skeleton serves the sibling senses. The
ladder is emerged from the inherited wave theory + measured DNA γ, climbs through the R19 transduction
switch read as an **event-detector**, and ends at the neural code (the felt percept deferred to the mind
volume). The **congenital-blindness mechanism layer** (built, v0.6.0) is the rung where the ladder breaks
— theoretical research toward understanding the congenitally affected, never clinical.

**The frequency ladder (the spine of this volume).**
> A photoreceptor cannot oscillate at 10¹⁴ Hz, so the eye does **not** down-convert by mixing or
> heterodyne. It down-converts by **EVENT-DETECTION + LOW-PASS INTEGRATION**: a single photon's *energy*
> drives one discrete all-or-none R19 flip (the carrier frequency is discarded), and the transduction
> cascade's *time constant* sets the surviving band. The carrier's identity — **colour** — is preserved
> orthogonally, in the **propagation angle χ** (geometry), which is why colour survives a ~13-order
> frequency collapse; WHERE (the image) is geometry too.
>
> 10¹⁴ Hz carrier ─(photon energy → one isomerisation; R19 event-detector)─▶ discrete flip-events
> ─(cascade low-pass, time-constant τ)─▶ graded ~Hz signal ─(rate re-quantisation)─▶ ~10–100 Hz spikes

**The organising insight (shared with the sibling sense).**
> A special sense is **a wave property → a spatial code → an R19 transduction switch that detects events
> and low-passes them into the neural band**, and a congenital sensory disease is **that switch failing
> to flip**. Vision: colour ← propagation **angle**; the frequency collapse ← the single-photon switch.
> Hearing: pitch ← basilar-membrane **place**. Same skeleton, two media.

## Research increments (the plan)

**E0 — inherited foundation (DONE; verified in this seed).**
- Light **emerges** as the jammed-lattice longitudinal wave, c=√(B/ρ); the quantum size
  **D = 2λ_C,e = 6π⁶ r_p = 4.852620 pm** is invariant (`vp_light_emergence_quantum.py`, [V]).
- The **angle law** sinχ=λ/(mD), m=⌈λ/D⌉, from one right triangle. D fixed ⇒ **χ depends on λ
  alone**, so different colours sit at different angles (633 nm→89.9378°, 532 nm→89.8248°). [F]
- **Visible-band canon inherited from physics v0.11.0** (`vp_visible_band_canonical.py`, v0.7.0): the
  §10.9 **band table** placing gamma (m=1, quasi-longitudinal) → **visible (m≈10⁵, near-transverse
  89.8°–89.9°)** → radio (transverse), and the **RCROSS(633/532)** two-channel closure m·sinχ·D/λ=1 on
  the one shared D (the precise, cross-validated method for fixing a visible wavelength from its angle).
  This is **rung 1** of the frequency ladder — *which carrier the eye is handed*. [F]+[V]
- The R19 substrate (`vp_substrate.py`) and **19 master-gene readings** are loaded: each gene read
  from DNA as **γ (LEVEL) + A4 coordinate (SHAPE)** (DNA v1.13), not γ alone — `vp_dna_reading.py`
  computes both from the cached promoters and proves A4 = signal − γ (orthogonality) per gene.

**E1 — angle → cone (DONE; built v0.3.0, `research/E1-angle-to-cone/run.py`, in the verifier).**
- The three cone opsins **OPN1LW / OPN1MW / OPN1SW** are placed on the angle map by their
  MEASURED λmax (S 420 / M 530 / L 560 nm, [L] cited literature — not from γ, not fitted) and land
  at three DISTINCT angle-bands (S 89.7497° / M 89.8006° / L 89.8428°) ⇒ trichromacy. The committed
  633/532 anchor (sep 0.1130°) holds as the falsifier — no fitting. [F]/[L]
- The cone/rod lineage is emerged via the R19 `Organ`: order = argsort(spinodal(γ)) (lowest-threshold
  switch first), relative size = dwell ∝ γ^1.5. [F] order/size-proportionality; absolute size and the
  correspondence to real developmental TIME are named [O].
- The **A4 SHAPE breaks γ-ties**: CNGA1/CNGB1 (the rod CNG α/β subunits, Δγ=0.0003, the closest γ
  pair) COLLAPSE at γ-only 3-decimal resolution and are separated deterministically by their A4 shape
  (amplitude differs 2.17×) — equal-γ genes are not interchangeable. [V]

**E2 — the single-photon switch (DONE; built v0.4.0, `research/E2-single-photon-switch/run.py`, in the verifier).**
- Rod phototransduction (**RHO · CNGA1 · CNGB1 · GNAT1**, γ measured) as a cooperative all-or-none
  R19 flip: the FROZEN field ds/dt=γ·s−s³+h settled from rest (s0=−√γ) under a drive sweeping
  through each gene's spinodal **flips DISCONTINUOUSLY** — dark below h* (s<0), snaps on above it
  (s>0), finite saddle-node jump ≈+2.26 for all four. One quantum of drive across h* flips the whole
  switch; less does nothing. [V] structure; the absolute photon→drive→Hz scale is a named [O].
- The **cooperativity IS the cubic −s³** (order n=3) [F] — where "Hill≈3" comes from, not a fit —
  and it is **necessary**: deleting the cubic (a first-order control field, NOT the substrate)
  removes the threshold, the basin, and the jump (the response becomes graded; the cubic switch is
  ≈231× steeper across the fold, formally →∞). The literal in-vivo rod Hill value is [O].
- The four switches order by **spinodal(γ)** (lowest threshold first) [F]; the **A4 SHAPE** separates
  the CNG channel's α/β subunits CNGA1/CNGB1 (one channel, two genes, degenerate γ collapsing at 3dp;
  shapes differ 2.17×) — even inside one switch, γ alone is lossy [V]. Whether the substrate
  threshold-order matches the real biochemical cascade SEQUENCE is [O] (needs kinetics; not fitted).

> **Scope reminder (applies to the next task and everything below it):** the remaining increments
> — including the congenital-disease layer — are **theoretical, non-clinical** analysis only,
> **direction-only / proposal-only** under `FIREWALL.md`. No diagnosis, treatment, dose, or efficacy
> is produced; see the Scope & Safety section at the top of this blueprint.

**E3 — image formation (DONE; built v0.5.0, `research/E3-image-formation/run.py`, in the verifier).**
- Grounds the reduced-eye optics on the **internal angle law** (sinχ=λ/(mD), D invariant), with
  external Snell kept only as its lab-space SHADOW — so the increment stays substrate-derived instead
  of collapsing onto a measured-index black box. (A) **Snell IS the transverse-oscillation match**:
  θ₂ from the wavefront/SPEED construction = the index form bit-for-bit, TIR onsets at arcsin(c₁/c₂),
  and **n = c_vac/c_med = √((B/ρ)_vac /(B/ρ)_med)** is the lattice meaning of refractive index. [F]/[V]
- (B) the cited Emsley reduced eye (n=4/3, R=5.55 mm) forms a real **inverted** image — power ≈60 D, a
  distant point focused at the ≈22.2 mm retina, m<0 (the spatial position code). Honest: this is
  classical ray arithmetic — it consumes the substrate-grounded Snell + measured n,R but is NOT
  substrate dynamics. Flagged **[V-arith]**, exactly as the task demanded.
- (C) refraction conserves frequency f ⇒ the **colour-angle χ(λ) survives the optics** (red 633→
  89.9378° ≠ green 532→89.8248°) while a single index co-locates the colours on the retina (first-order
  chromatic split = 0): optics gives WHERE, the angle law gives WHAT COLOUR — two orthogonal channels
  on one wave (robust θ + hypersensitive χ). [F]. The chromatic-aberration MAGNITUDE needs c_med(λ)
  and is a named **[O]** — no diopter invented. Deterministic (2×sha256); foundation frozen; no γ added.

**E4 — congenital BLINDNESS (DONE; built v0.6.0, `research/E4-congenital-blindness/run.py`, in the verifier).**
- The goal increment, read as E2's single-photon switch **in reverse**. Six congenital-blindness
  master genes — **GUCY2D, RPE65, CNGB3** (loaded) + **AIPL1, RPGR, PDE6B** (γ now measured from
  NCBI, folded into the cache/atlas: 16→19 genes) — each as an R19 transduction **failure mode**.
  (A) **LOF = the switch held below its own spinodal**: on the FROZEN field ds/dt=γ·s−s³+h settled
  from rest, a healthy drive 1.15·h* clears the fold and flips on (s>0); the LOF drive 0.85·h* never
  clears it and stays dark (s<0) — the *only* difference is whether the drive crosses h*(γ). The dark
  basin is the sole basin; the all-or-none flip simply never fires. [V] structure; the photon→drive
  scale stays the E2 [O].
- (B) the **substrate-inverse lever, DIRECTION-ONLY**: since the flip condition is drive ≥ h*(γ), the
  inverse is exactly (i) raise the drive past the existing h*, or (ii) lower the threshold below the
  residual drive — shown with a *hypothetical* threshold probe γ′=3(h*/2)^(2/3) while the real
  measured γ is never touched. Which physical knob, which molecule, any quantity or clinical magnitude
  = **firewall-blocked [O]**: a machine-checked MAGNITUDE FIREWALL in `run.py` asserts the whole
  output carries no dose/potency/efficacy/diopter/concentration token and no "%". [F] direction only.
- (C) the six switches **rank by spinodal(γ)** as a STRUCTURAL fragility ordering (lowest threshold
  first: CNGB3 < RPE65 < GUCY2D < RPGR < AIPL1 < PDE6B) — **not** clinical severity. Honest finding:
  all six γ are already distinct at 3 dp (no γ-tie to break), yet the **A4 SHAPE** rides orthogonal
  and the closest-γ pair (GUCY2D/RPGR) is A4-separated anyway — γ alone stays lossy. **Brutal caveat,
  stated in the increment:** the measured γ is **promoter** context, while almost every real blindness
  lesion is **coding / downstream** — so the gene-to-disease map is literature [L] (mechanism, not
  diagnosis) and the clinical correspondence is a named **[O]**. Deterministic (2×sha256); foundation
  frozen; no γ added by the increment itself.

### Ladder map of the built increments (E0–E8), read as the down-conversion spine
- **Rung 1 — the carrier (E0 + the inherited visible-band canon).** ν_light=c/λ ≈ 4.7×10¹⁴ Hz (633 nm)
  to 7.9×10¹⁴ Hz (380 nm); a near-transverse oscillation of rotating quanta at angle χ(λ). WHAT (colour)
  lives in the **angle**, fixed by the invariant D and cross-validated by **RCROSS(633/532)**. [F]+[V]
- **Colour channel (E1).** angle → cone trichromacy (the WHAT, placed on the angle map).
- **Rung 2 — the collapse (E2).** the single-photon R19 flip **IS** the event-detector: a quantum of
  drive across the spinodal flips the switch; the carrier frequency is discarded. [V]
- **WHERE channel (E3).** image formation — geometry, survives the collapse.
- **The break (E4).** congenital blindness = the switch failing to flip. [direction-only, firewalled]
- **The whole collapse, quantified (E5).** ν≈10¹⁴ Hz → ~13-order drop → ~10–100 Hz: down-conversion is
  event-detection + low-pass (carrier-invariant, band ∝ 1/τ), **not** mixing. [F]/[V]
- **Why the carrier is VISIBLE (E6).** geometry PLACES the band (sandwiched in m, near-transverse) but the
  angle never gates it; the chromophore's reversible energy window (~1.8–3.3 eV → 375.71–688.80 nm) PINS
  ~380–750 nm. WHERE/colour are geometry; the band edges are photochemistry [O for the molecular tuning].
- **The low-pass made explicit (E7).** the FROZEN switch's recovery law **is** a single-pole low-pass; the
  surviving band is set by the recovery τ at **f_c = β/(2πτ_s)** — carrier-invariant AND γ-invariant, so it
  is **τ, not the carrier and not γ**, that fixes the band (γ secondary via dwell ∝ γ^1.5). [F]/[V]
- **The hand-off, re-quantised (E8).** the graded low-pass signal is re-encoded as a ganglion spike **RATE**
  by the FROZEN R19 neuron's fold-crossing events — a **thresholded** (rheobase), **bounded**
  (depolarisation-block ceiling: a bandpass in drive), **monotone** clock. The **carrier stays gone** (rate
  ⟂ carrier, rate ∝ envelope) and the train sits in the neural low band ⇒ the collapse is preserved
  end-to-end. The felt percept → mind volume (firewall). [F]/[V] structure; absolute Hz [O]. **Spine complete.**

**E5 — the frequency ladder, quantified (DONE; built v0.8.0, `research/E5-frequency-ladder/run.py`, in the verifier).**
Lays out and GATES every rung's frequency and shows the full **~13-order collapse**: ν_light≈10¹⁴ Hz
(c/λ; 633→4.74×10¹⁴, 532→5.64×10¹⁴ Hz, E=1.96/2.33 eV) → a photon's energy E=hν drives ONE discrete
isomerisation (the carrier is never tracked) → R19 flip → cascade → graded ~Hz → spike rate ~10–100 Hz.
On the FROZEN Neuron it **demonstrates** the central, falsifiable claim — **down-conversion is
event-detection + low-pass, NOT mixing**: a fast carrier (24×–476× the intrinsic rhythm) is averaged away
(out/f_c→0), the output is **carrier-frequency-invariant** (≈11% move across a 20× carrier span ⇒ output
⟂ carrier; a mixer would track it), the **cubic is the all-or-none event** (deleting −s³ destroys the
threshold), and the surviving **band is set by the recovery τ** (∝1/τ), not the carrier. Honest: the
substrate cannot carry 10¹⁴ Hz literally, so the MECHANISM is shown in substrate-time and the MAGNITUDE
accounted separately; the RATIO is forced [F]/[V], the absolute biological Hz at each rung is [O]. No γ
added; γ(GUCY2D) byte-equal to the frozen atlas; SEED=19; `gate_E5.py` 8 checks → `E5 GATE: PASS`.

**E6 — why the band is VISIBLE (DONE; built v0.9.0, `research/E6-why-visible/run.py`, in the verifier).**
Answers *why* the carrier the eye is handed is the **visible** band with two unrelated constraints that
select the same window. **GATE (i) — geometry PLACES it** (the §10.9 canon, read-only): m=⌈λ/D⌉ is monotone
in λ, so visible (m≈10⁵) is **sandwiched in m** between x-ray (smaller m) and infrared (larger m), in the
near-transverse manifold; its identity — colour — is its angle χ(λ). [F] **GATE (ii) — photochemistry PINS
it:** a photon must carry enough energy to drive the *reversible* 11-cis→all-trans retinal isomerisation
(a FLOOR) yet not ionise/photodamage (a CEILING); the cited window ~1.8–3.3 eV maps, through the forced
E=hc/λ, onto **exactly 375.71–688.80 nm**, and every already-measured visible anchor (the RCROSS channels
633/532 nm + the cone-opsin λmax 420/530/560 nm) lands inside it. [L]+[F] **The honest finding:** geometry
only **places** the band — the angle is a smooth **sawtooth** (633 nm has a *smaller* near-grazing deficit
than 750 nm though it is shorter), with **no kink at the band edges**, so the angle **never gates a band**;
the edges are **photochemical**, not geometric (an IR probe at 10 µm is excluded by the energy floor even
though its deficit is *smaller* than visible's — geometry would admit it). The **deep-red edge is soft**
(750 nm = 1.6531 eV sits ~0.147 eV below the 1.8 eV floor), and the chromophore energy that sets the floor
is coding/photochemistry — the promoter-γ this package reads has **no lever** on the retinal pocket, a
named **[O]**. **Precision discipline:** the **wavelength is the anchor**, mapped EXACTLY to ν=c/λ, period
T=1/ν, and E=hν with the SI-exact constants (no rounding); angles carried to full precision (χ to 10 dp +
the deficit 90°−χ, no 1−sin²χ cancellation) with the closure m·sinχ·D/λ=1 held to 1e-15. No γ added; D
byte-equal to the inherited invariant; SEED=19; `gate_E6.py` 8 checks → `E6 GATE: PASS`. What E6 forces is
the band PLACEMENT (geometry) and the energy-window LOGIC — it invents no chromophore.

**E7 — the cascade as the band-setting low-pass (DONE; built v0.10.0, `research/E7-cascade-lowpass/run.py`, in the verifier).**
Turns E5's qualitative "the carrier is averaged away" into an **explicit, measured filter**. The FROZEN
Neuron's recovery law `w += dt*(s − β·w)/τ_s` (quoted verbatim) **is** a first-order leaky integrator — a
single-pole low-pass with transfer function H(f)=1/(β+i·2πf·τ_s). The one claim, **the band is set by the
recovery time-constant, f_c = β/(2πτ_s)**, is read off the frozen substrate four ways that agree: DC gain
= 1/β = 2.000 [F]; measured cutoff = β/(2πτ) to 0.16% [V]; phase lag at cutoff = 44.99° (one pole ⇒ 45°)
[V]; high-f roll-off = −19.96 dB/decade (one pole ⇒ −20) [V]. Sweeping τ∈{20,40,80} gives **f_c ∝ 1/τ
exactly** (f_c·τ = β/2π = 0.07958 held constant to 0.27%), and the band is invariant to **both** the
carrier and the promoter-γ — it is **τ, not the carrier and not γ**, that fixes the band. The full FROZEN
neuron then inherits this: its emergent rhythm falls monotonically in τ with range(τ) ≫ range(γ), so γ is
a **secondary** mover (via dwell ∝ γ^1.5) at fixed τ. **Honest scope:** the full-neuron rhythm is only
**approximately** ∝1/τ (a relaxation period = slow τ-recovery + a τ-independent fast transit) — a named
**[O]**, alongside the single-pole idealisation vs. the real multi-stage cascade
(rhodopsin→transducin→PDE→cGMP→CNG) and the absolute τ→Hz calibration. No γ added; Neuron
β=0.5/τ_f=1.0/τ_s=40.0 and γ(GUCY2D)=1.365 byte-equal to the frozen substrate/atlas; SEED=19; `gate_E7.py`
8 checks → `E7 GATE: PASS`.

**E8 — graded → spike-rate re-quantisation (DONE; built v0.11.0, `research/E8-graded-to-spike-rate/run.py`, in the verifier).**
The ladder's **last rung**: the retina re-encodes E7's **graded** ~Hz signal as a discrete ganglion-cell
spike **RATE** (rate coding). The re-quantiser is the FROZEN R19 Neuron itself — the same neuron whose slow
recovery set the band (E7) now **fires**, each spike a membrane up-crossing = an all-or-none fold-crossing
event (inherited `spikes`/`rate_hz`/`dominant_freq`). Measured on the FROZEN substrate (operating point an
INPUT, never fitted), the rate code is **thresholded** (a rheobase FLOOR — the switch must clear its fold
to spike), **bounded** (a depolarisation-block CEILING — the full-range f–I is a *bandpass in drive*,
silent on BOTH sides), **monotone** (rate ↑ strictly with the graded amplitude across the operating band),
and a near-periodic clock (CV(ISI)≈0.0002 — a genuine re-quantiser). The central result, **the carrier
stays gone (no mixing)**, closes the loop with E5/E7: fix the slow envelope and sweep the carrier ⇒ rate
invariant (1.53% over a 20× span, rate ⟂ carrier); raise the envelope ⇒ rate rises (rate ∝ envelope); the
train sits in the neural low band (dominant_freq = rate, orders below the carrier) ⇒ the ~13-order
down-conversion is **preserved end-to-end**. γ is shown READ-ONLY as a structural excitability OFFSET (it
shifts the rheobase via spinodal(γ), not the band [τ, E7] and not the signal [the drive]); E8 makes **no**
"γ negligible" claim. The **felt percept** of sight is OUT OF SCOPE — it hands off to the **mind** volume
(firewall). [F] the rate-code structure (floor/monotone/ceiling/carrier-invariance); named **[O]**: the
absolute Hz/spike-count, the f–I shape, and the single-stage collapse of the retinal network. No γ added;
Neuron β=0.5/τ_f=1.0/τ_s=40.0 and γ(GUCY2D)=1.365 byte-equal; SEED=19; `gate_E8.py` 8 checks → `E8 GATE:
PASS`. **With E8 the down-conversion spine E0→E8 is complete.**

**E9 — red-green colour vision / dichromacy (DONE; built v0.13.0, `research/E9-red-green-dichromacy/run.py`, in the verifier).**
The **first mechanism extension beyond the spine**: it carries the carrier no further down — it asks what
the FROZEN E1 angle map already FORCES about colour discrimination, and *why* the commonest inherited
colour-vision difference is **red-green**. Colour is propagation angle χ(λ) (E1/E6), so three cones are
three angle-samples and the three discrimination axes are the three pairwise angle **margins** (read
byte-equal off the frozen `chi_deg` at the measured λmax): S-M = 0.0509°, **M-L (green-red) = 0.0421° — the
SMALLEST** (1.208× tighter than S-M), S-L = 0.0931°. [F]↔[L] headline: **the angle map makes green-red the
structurally most fragile colour axis, matching the epidemiology** — no fit, no new γ. FORCED, not tuned:
**(1) coincidence ⇒ collapse** — χ depends on λ alone, so equal λmax ⇒ equal angle ⇒ margin **exactly
0.000000°**; a hypothetical L′ slid toward λ(M) drives the margin monotonically to 0 (sawtooth-proof: the
limit of convergence *is* the loss), unifying **dichromacy** (drop one angle-sample ⇒ the within-red-green
axis vanishes, exactly one chromatic axis survives) and **anomalous trichromacy** (peaks converge, margin →
0) as ONE continuum. **(2) direction-only lever** — peaks together ⇒ margin shrinks, apart ⇒ grows; the
magnitude is a named **[O]** (firewalled). **(3) orthogonality** — colour (angle, E1) ⟂ position (image,
E3) ⟂ brightness (switch, E2); the surviving cones' R19 switch is spinodal-stable (untouched), so losing
one cone costs **exactly one colour axis** while acuity and single-photon detection stay intact — *why* it
is colour-blindness, not blindness. **(4) γ READ-ONLY** (OPN1LW γ=1.4820, OPN1MW γ=1.4058, Δγ=0.0762, A4
shapes 1.40× apart) as a structural offset, **no** claim γ predicts λmax; the X-linked OPN1LW/OPN1MW tandem
array is [L] genomics, not γ. This is the package's **second firewalled clinical chapter** (after E4):
direction-only, proposal-only, `run.py` carries its own `MAGNITUDE_BLOCK` and asserts the transcript holds
none of those tokens. No γ added; cone angles byte-equal from the frozen map; λmax already-measured;
SEED=19; `gate_E9.py` 8 checks → `E9 GATE: PASS`. The **felt percept** of colour is OUT OF SCOPE (→ mind
volume). **The foundation does not move:** E9 fetched nothing and re-froze nothing — `FROZEN_SHA256.json`
is byte-identical to v0.12.0.

**E10 — light/dark adaptation as gain control on the R19 switch (DONE; built v0.14.0, `research/E10-light-dark-adaptation/run.py`, in the verifier).**
The **second mechanism extension beyond the spine**, and — unlike E9 — a **NORMAL, non-clinical** chapter
(like E5–E8: no `MAGNITUDE_BLOCK`, no firewall). It asks what the FROZEN R19 switch already FORCES about
how the eye spans ~10 decades of background light with a bounded response. The mechanism is **the switch's
own saturating ON branch**: E2's bistable field `γ·s − s³ + h = 0`, on its ON branch, is the real root of
`s³ − γ·s − h = 0`, and for a large background drive h the cubic dominates ⇒ the steady state
**s*(h) → h^(1/3)** — a compressive cube-root response, read off the FROZEN substrate four ways.
**(A) Dynamic-range compression:** a **5.000000-decade** background sweep (1→10⁵) fits a **1.500207-decade**
response (compression **3.332873**); the deep sweep 100→10⁸ gives the cubic order **n=3** (every s* a true
zero of the frozen field, max residual 2.3e-13 [V]). **(B) Automatic gain control:** the incremental gain
`ds*/dh = 1/(3s*²−γ)` falls **1296.0×** dim→bright (∝ h^(−2/3)) — saturation *is* the gain control, **no
separate machinery invoked** [F]. **(C) headline — a Weber-Fechner-like law, FORCED not fitted:** the
contrast gain `(h/s*)·ds*/dh` is pinned by the pure-cube limit **EXACTLY at 1/n = 1/3 = 0.333333** for any
h, and is **γ-INDEPENDENT** (RHO γ=1.4719 → 0.333301, CNGB3 γ=1.2425 → 0.333306 at h=10⁶) — equal
fractional steps feel equal regardless of the gene; the compression is the cubic **order**, not the
threshold γ. Honest scope, stated not hidden: this is the saturated tail; near the fold (small h) the γ·s
term matters and the response is steeper than a clean power law. **(D) two regimes:** **DARK** = near the
fold h*(γ)=0.68733 (highest gain + E2's single-photon flip), **BRIGHT** = deep in the cube root (low gain,
compressed) — adaptation is the operating point **sliding** fold→cube-root. **γ READ-ONLY** sets the
fold/offset (the compression law is γ-independent — an OFFSET, as in E7/E8); the dark re-sensitisation
**recovery τ_s=40.0 (β=0.5)** is the same FROZEN time-constant that set the band (E7) and the rate code
(E8) — structure [F], absolute seconds the inherited **[O]**. No γ added; substrate/Neuron byte-equal;
SEED=19; `gate_E10.py` 8 checks → `E10 GATE: PASS`. The **felt brightness percept** is OUT OF SCOPE (→ mind
volume). **The foundation does not move:** E10 fetched nothing and re-froze nothing — `FROZEN_SHA256.json`
is byte-identical to v0.12.0 and v0.13.0.

**E11 — accommodation & refractive error as the power↔length match on the E3 eye (DONE; built v0.15.0, `research/E11-accommodation-refraction/run.py`, in the verifier).**
The **third mechanism extension beyond the spine**, and — like E9 — a **CLINICAL/condition** chapter
(myopia/hyperopia/presbyopia), so it is in `DISEASE_CHAPTERS` and covered by `gate_volume.py` **G5** (plus its
own `gate_E11.py` **G8**). It consumes E3's FROZEN single-surface optics **read-only** (`importlib`, never
re-derived) and asks what that frozen eye already FORCES about focus. E3 images a distant object at
**v_∞ = n₂/P** with **P = (n₂−n₁)/R**; it lands on the retina ⇔ **P·L = n₂**, so the whole story is the
dimensionless **match ratio ρ ≡ P·L/n₂**, read off four ways. **(A) Emmetropia is ρ = 1:** the frozen Emsley
reduced eye sits **exactly** there (**ρ = 1.000000** [V-arith]); focus is a *whole curve* in the power×length
plane, not a single eye. **(B) Refractive error is sign(ρ−1):** **ρ = 1.050000 > 1** ⇒ distant focus *in
front* ⇒ **MYOPIA**; **ρ = 0.950000 < 1** ⇒ *behind* ⇒ **HYPEROPIA** — each reachable **two ways** (an eye
too long OR too powerful) because **only the product P·L matters** (a too-strong eye `q·ℓ = 1` shortened to
match returns **ρ = 1.000000**); stated **direction-only**, the dioptric magnitude a named **[O]**. **(C)
Accommodation is a one-signed power lever:** a near object at `u = −k·L` needs `P_req/P_∞ = 1 + n₁/(n₂·k)`,
**monotonically rising** as the object nears (**1.000750 → 1.007500 → 1.030000 → 1.075000 → 1.187500 →
1.375000**) and **always ≥ 1** — supplied by **rounding the lens** (R↓ ⇒ P↑; `R_req/R_∞` nearest **0.727273**
re-focuses on the retina); amplitude and absolute near-distances **[O]**. **(D) The lever is lattice
geometry:** power rides curvature **dP/P = −dR/R** (P ∝ 1/R; the same √(B/ρ) refractive-index rule as E3),
while the *length* axis is the substrate **dwell size-law size ∝ γ^1.5** (E1) — PAX6 read-only (PAX6/RAX dwell
ratio **1.059595**) instantiates the *direction* of the growth shift (more eye-field growth ⇒ longer eye ⇒
myopic), the gene→axial-elongation map itself an **[O]**. **Firewall:** E11's `MAGNITUDE_BLOCK` mirrors E9's
and **adds** `diopter`/`dioptre` and bare `mm`, so every fact is a dimensionless ratio or a sign — G8 and G5
both confirm no magnitude token, no "%". No γ added; substrate byte-equal; SEED=19; `gate_E11.py` 8 checks →
`E11 GATE: PASS`. The **felt blur/clarity percept** is OUT OF SCOPE (→ mind volume). **The foundation does not
move:** E11 fetched nothing and re-froze nothing — `FROZEN_SHA256.json` is byte-identical to v0.12.0, v0.13.0
and v0.14.0.

**E12 — acquired/degenerative disease as the R19 switch carried OVER its fold, with hysteresis (DONE; built v0.16.0, `research/E12-acquired-degeneration/run.py`, in the verifier).**
The **fourth mechanism extension beyond the spine**, and — like E4/E9/E11 — a **CLINICAL/condition** chapter
(the late picture shared across AMD, glaucoma and diabetic retinopathy), so it is in `DISEASE_CHAPTERS` and
covered by `gate_volume.py` **G5** (plus its own `gate_E12.py` **G8**). It consumes only the **FROZEN** R19
field `ds/dt = γ·s − s³ + h`, its fold `h*(γ) = 2(γ/3)^1.5`, and the atlas γ — **read-only**, adding no γ. The
honest physics is distinct from E4: a congenital switch is one *born below* its fold (static, **never flips**);
a degenerative disease is the opposite history — a switch that **started healthy** (settles ON, s>0) and is
carried *over* its fold by accumulating stress, read four ways. **(A) Degeneration = a slow drift over the
fold:** on RHO (read-only, γ **1.4719**, fold h\* **0.687330**, barrier **0.541622**) the healthy state
(**s = 1.316420**) tracks the upper branch down and **collapses in one step** at **h = -0.691855 ≈ −h\* =
-0.687330** — a *tipping point* [V], start-independent (a different start collapses at **-0.689701**), E4's
spinodal reached *dynamically from the ON side*. **(B) Hysteresis:** recovery comes only at the *opposite* fold
**+h\* = 0.687330** (drive **0.691855**), loop width **1.383710 ≈ 2·h\* = 1.374661** = the irreversibility
margin — recovery needs **over-correction past +h\***; the substrate's account of why **early ≠ late**. **(C)
One geometry, many routes:** a **LOAD route** (lower h to −h\*) and a **BASIN-SHALLOWING route** (erode γ under
fixed load **-0.300000** until the shrinking fold **h\*(γ) = 0.296976** meets it at **γ = 0.841231**, analytic
γ_crit **0.846932**) **both land on the one locus h = −h\*(γ)** (gap **0.003024**) — so the shared *late*
picture across the three diseases is **forced** while each primary stress's identity (oxidative vs mechanical
vs metabolic) is a named **[O]**. **(D) γ as STRUCTURAL fragility:** lower γ ⇒ shallower basin ⇒ tips under
less stress (spinodal-monotone CNGB3 h\* **0.533080** → PDE6B h\* **0.732285**, span **1.373687**),
READ-ONLY/byte-equal — with the **loudest caveat in the volume:** the disease-gene→γ map is *even more* **[O]**
than E4 (polygenic, age/environment-gated, mostly non-promoter common variants; promoter-γ has essentially
**no monogenic purchase** here). **Firewall:** E12's `MAGNITUDE_BLOCK` mirrors E9's and **adds**
`hba1c`/`mg/dl`/`mmol/l`/`mmol/dl` and bare `mm`/`mmhg` guards, so every stress is a dimensionless multiple of
the gene's own fold — G8 and G5 both confirm no magnitude token, no "%". No γ added; substrate byte-equal;
SEED=19; `gate_E12.py` 8 checks → `E12 GATE: PASS`. The **felt loss of sight** is OUT OF SCOPE (→ mind volume).
**The foundation does not move:** E12 fetched nothing and re-froze nothing — `FROZEN_SHA256.json` is
byte-identical to v0.12.0 through v0.15.0.

> **Beyond the ladder spine — complete.** All four mechanism extensions are built: red-green dichromacy (E9),
> light/dark adaptation (E10), accommodation + refractive error (E11), and the acquired/degenerative disease
> layer (E12, the hardest). The planned arc of the eye volume is finished; only optional items remain (e.g.
> **SIX6**, the one eye-field TF still `_to_measure` in the atlas — additive, changes no result). Every
> **felt** percept stays deferred one-way to the **mind** volume.

## What is forced vs measured vs open (grading discipline, VP-SPEC C3)
- **[F] forced / [V] verified:** the wave emergence (c=√(B/ρ)), the spatial-code SHAPE, the R19
  switch structure, the emergence order argsort(spinodal(γ)), and the DNA reading **γ (LEVEL) + A4
  (SHAPE)** with its orthogonality A4 = signal − γ.
- **[L] measured/calibrated:** every γ (from NCBI), the absolute place/angle calibration constants.
- **[O] open:** absolute magnitudes (photon/SPL → firing Hz), the **absolute frequency calibration at
  every ladder rung** (carrier → event → cascade τ → spike rate; only the COLLAPSE RATIO and the
  mechanism are forced), the **retinal chromophore isomerisation energy** that pins the visible band
  (coding/photochemistry, outside the promoter-γ this package reads), the full traveling-wave
  hydrodynamics (ear), the full A4 anchor/loop/anchor-relative-phase (needs the genomic feature table),
  the felt percept (→ mind volume). Each [O] names its obstacle in the research ledger.

## Definition of done for the FULL volume (what this seed grows into)
A multi-chapter HTML volume (VP-SPEC v1.8 §6) that **walks the full frequency ladder E0→E8** — the
high→low down-conversion, from the ~10¹⁴ Hz visible carrier through the R19 event-detector and the
cascade low-pass to the ~10–100 Hz neural spike code — where every displayed number is reproduced
deterministically (2×sha256, HTML↔code drift 0), every γ is measured-and-cached, the disease layer is
proposal-only under the firewall, and `verify_*` passes — delivered as **one zip**.
