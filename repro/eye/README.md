# vp_eye_emergence_seed — v0.16.0  (research SEED)

A self-contained **starting package** for properly emerging the **eye (vision)** from first
principles, for research toward the congenitally affected. Author: Young Jae Lee
(ORCID 0009-0002-7535-8245) · Licence CC BY 4.0 · Governed by **VP-SPEC v1.8** (bundled).
Concept DOI (always resolves to the latest version): **10.5281/zenodo.20790134**.

This is a SEED, not a finished volume: it ships the **verified foundation**, the **measured
inputs**, and a **working research pipeline**, plus the blueprint of what to build. The
emergence work itself is the research this package launches (see `BLUEPRINT.md`).

## The one idea
The vision sense reads a **wave** (light (electromagnetic)) and turns it into a spatial code, then an
all-or-none R19 transduction switch. Here the spatial code is **colour by propagation ANGLE χ (sinχ=λ/(mD), D fixed ⇒ each λ its own angle)**. The whole
chain is grounded on the precise wave theory inherited from physics/chemistry — not assumed. Each
master gene is read from DNA as **γ (LEVEL) *and* its A4 coordinate (SHAPE)** — not γ alone (DNA
v1.13): γ is the window-mean of the stacking-stiffness signal, A4 is that same signal with the mean
removed (where the promoter is stiff vs soft relative to its own average). They are orthogonal —
neither contains the other — so reading γ alone is the compressed view this seed deliberately avoids.

**The goal (v0.7.0 re-scope).** Reveal, step by step, the **complete down-conversion ladder** by which
the eye turns the **high-frequency light band** (~10¹⁴ Hz carrier) into the **low-frequency neural band**
(~10–100 Hz spike code). The key claim: the eye down-converts by **event-detection + low-pass, not by
mixing** — a photon's energy drives one discrete R19 flip (carrier frequency discarded), the cascade
time constant sets the surviving band, and the carrier's identity (colour) survives only because it lives
in the **angle** (geometry), not in a frequency the cell could follow. See `BLUEPRINT.md` for the ladder
spine and the increment plan (E0→E8, plus the E9 colour-vision, E10 light/dark-adaptation, E11 accommodation/refractive-error, and E12 acquired/degenerative-disease mechanism extensions beyond the spine).

## Verify everything with one command
```
python3 tools/verify_seed.py
```
Expected: `SEED VERIFY: PASS`. It checks (1) no-regression — inherited artifacts byte-identical
to the frozen seed; (2) the foundation reproduces deterministically; (3) the 19
master-gene readings — γ (LEVEL) **and** A4 (SHAPE) — recompute offline bit-for-bit, with the A4
orthogonality (A4 = signal − γ) asserted per gene; (4) no-omission — every promised artifact present.

## Inherited foundation (verified, frozen — `inherited/`)
  - `inherited/vp_light_emergence_quantum.py` — light emergence + the angle law
  - `inherited/vp_color_by_angle.py` — colour separated by propagation angle χ
  - `inherited/vp_visible_band_canonical.py` — **visible-band canon from physics v0.11.0** (§9.4 D;
    §10.9 band table gamma→visible→radio; §11 **RCROSS(633/532)** two-channel closure) — rung 1 of the
    frequency ladder; forced relations recomputed bit-exact, unit-realization chain quoted (v0.7.0)
  - `inherited/vp_dna_reading.py` — γ (LEVEL) + A4 coordinate (SHAPE) per master gene
  - `inherited/vp_substrate.py` — the R19 bistable switch primitive (spinodal/barrier/Organ)
  - `inherited/dna_interpreter.py`, `inherited/key_pipeline_full.py` — the **canonical DNA v1.13 A4
    grammar** (γ, R19 switch, helix geometry, shells/anchors/robust_z), byte-identical to the source
  - `inherited/gamma_pipeline.py` — offline γ = −mean(SantaLucia-1998 NN ΔG37) recompute
  - `inherited/eye_promoters.cache.json` — 19 measured human promoter sequences (offline)
  - `inherited/organ_gamma.json` — the measured readable-layer atlas (γ LEVEL + A4 SHAPE) + extensions
  - `inherited/FROZEN_SHA256.json` — the no-regression hash set

## Research base (`tools/`, `research/`)
  - `tools/fetch_promoter_gamma.py` — the WORKING NCBI fetcher (add a master gene → measured γ)
  - `tools/verify_seed.py` — the one-command gate
  - `research/E1-angle-to-cone/run.py` — **E1, BUILT (v0.3.0):** the three cone opsins
    (OPN1LW/MW/SW) placed on the angle map by measured λmax → three distinct angle-bands
    (trichromacy); the cone/rod lineage emerged via the R19 `Organ`, order = argsort(spinodal(γ));
    and the **A4 SHAPE tie-break** demonstrated on the real CNGA1/CNGB1 γ-degeneracy (equal-γ genes
    are not interchangeable). Deterministic (2×sha256), folded into the verifier's foundation list.
  - `research/E1-angle-to-cone/gate_E1.py` — the focused E1 pass/fail gate (`E1 GATE: PASS`).
  - `research/E2-single-photon-switch/run.py` — **E2, BUILT (v0.4.0):** rod phototransduction
    (OPN→RHO·CNGA1·CNGB1·GNAT1, γ measured) as a cooperative **all-or-none** R19 flip: the frozen
    field settled from rest flips DISCONTINUOUSLY past each gene's spinodal (dark below, snaps on
    above, finite saddle-node jump ≈+2.26) — one quantum of drive flips the whole switch. The
    cooperativity IS the cubic −s³ (order n=3) and is necessary (delete it → graded; the cubic switch
    is ≈231× steeper). The CNG channel's α/β subunits (degenerate γ) are separated by their A4 SHAPE.
    Deterministic (2×sha256), folded into the verifier's foundation list. Absolute photon→Hz scale [O].
  - `research/E2-single-photon-switch/gate_E2.py` — the focused E2 pass/fail gate (`E2 GATE: PASS`).
  - `research/E3-image-formation/run.py` — **E3, BUILT (v0.5.0):** the reduced-eye optics grounded on
    the **internal angle law** (sinχ=λ/(mD), D invariant), external Snell kept only as its lab-space
    shadow. (A) Snell IS the transverse-oscillation match — wavefront/SPEED θ₂ = index θ₂ bit-for-bit,
    TIR at arcsin(c₁/c₂), and n = c_vac/c_med = √((B/ρ) ratio) is the lattice meaning of refractive
    index. (B) the cited Emsley reduced eye (n=4/3, R=5.55 mm) forms a real **inverted** image (power
    ≈60 D, distant focus at the ≈22.2 mm retina, m<0) — honest classical **[V-arith]**. (C) refraction
    conserves f, so the colour-angle χ(λ) survives the optics (633≠532) while a single index co-locates
    the colours on the retina: optics gives WHERE, the angle law gives WHAT COLOUR. Chromatic-aberration
    magnitude [O]. Deterministic (2×sha256), folded into the verifier's foundation list; no γ added.
  - `research/E3-image-formation/gate_E3.py` — the focused E3 pass/fail gate (`E3 GATE: PASS`).
  - `research/E4-congenital-blindness/run.py` — **E4, BUILT (v0.6.0):** the six congenital-blindness
    master genes read as R19 transduction **failure modes** (LOF = switch held below its spinodal),
    the substrate-inverse lever **direction-only** under the magnitude firewall, ranked by spinodal(γ)
    as structural fragility — proposal-only, no diagnosis/dose/efficacy.
  - `research/E4-congenital-blindness/gate_E4.py` — the focused E4 pass/fail gate (`E4 GATE: PASS`).
  - `research/E5-frequency-ladder/run.py` — **E5, BUILT (v0.8.0):** the high→low **frequency ladder** —
    ν=c/λ≈10¹⁴ Hz carrier → ~13-order collapse → ~10–100 Hz neural band — demonstrating on the FROZEN
    Neuron that the eye down-converts by **event-detection + low-pass, not mixing** (carrier-invariant
    output; band ∝ 1/τ). No γ added; no clinical claim.
  - `research/E5-frequency-ladder/gate_E5.py` — the focused E5 pass/fail gate (`E5 GATE: PASS`).
  - `research/E6-why-visible/run.py` — **E6, BUILT (v0.9.0):** *why the carrier is the **visible** band* —
    two unrelated constraints select the same window: GATE (i) the §10.9 geometric placement (visible
    sandwiched in m between x-ray and infrared, near-transverse) [F]; GATE (ii) the photochemical energy
    window (reversible 11-cis→all-trans isomerisation ~1.8–3.3 eV → exactly 375.71–688.80 nm) [L]. The
    honest finding: **geometry only PLACES the band, the chromophore energy PINS it** — the angle is a
    smooth sawtooth that never gates a band, so the edges are photochemical (the deep-red edge is soft;
    the chromophore tuning is a named [O]). The **wavelength is the anchor**, mapped EXACTLY (ν=c/λ,
    period T=1/ν, E=hν, SI-exact constants) on already-measured wavelengths (633/532 nm + opsin λmax
    420/530/560 nm); angles to full precision with the closure m·sinχ·D/λ=1 held to 1e-15. No γ added.
  - `research/E6-why-visible/gate_E6.py` — the focused E6 pass/fail gate (`E6 GATE: PASS`).
  - `research/E7-cascade-lowpass/run.py` — **E7, BUILT (v0.10.0):** *the cascade as the band-setting
    low-pass* — the FROZEN Neuron's recovery law is a single-pole low-pass H(f)=1/(β+i·2πf·τ_s), and the
    surviving band is set by the recovery τ at **f_c = β/(2πτ_s)**: DC gain 1/β [F], measured cutoff =
    β/(2πτ) [V], 45° phase at cutoff [V], −20 dB/dec roll-off [V]; sweeping τ ⇒ f_c ∝ 1/τ exactly, the
    band invariant to **both** carrier and γ (γ a secondary mover via dwell ∝ γ^1.5). Honest [O]: the
    full-neuron rhythm is only approximately ∝1/τ, the single-pole vs. real multi-stage cascade, and the
    absolute τ→Hz. No γ added; no clinical claim.
  - `research/E7-cascade-lowpass/gate_E7.py` — the focused E7 pass/fail gate (`E7 GATE: PASS`).
  - `research/E8-graded-to-spike-rate/run.py` — **E8, BUILT (v0.11.0):** *graded → spike-rate
    re-quantisation* — the ladder's last rung. The FROZEN R19 Neuron whose recovery set the band (E7)
    now FIRES: each spike is a membrane up-crossing = an all-or-none fold-crossing event (inherited
    `spikes`/`rate_hz`/`dominant_freq`). The graded photoreceptor signal (the drive) is re-encoded as a
    ganglion spike **RATE** — a **thresholded** (rheobase floor: silent until the switch clears its
    fold), **bounded** (depolarisation-block ceiling — the f–I is a bandpass in drive, block on BOTH
    sides), **monotone** (rate ↑ strictly with amplitude across the operating band) code, a near-periodic
    clock (CV(ISI)≈0.0002). Crucially the **carrier stays gone**: rate ⟂ carrier (1.53% over a 20× span)
    and rate ∝ envelope — the re-quantiser tracks the slow envelope and never re-introduces the carrier,
    so the E5/E7 ~13-order down-conversion is preserved end-to-end; the train sits in the neural low band.
    γ is shown READ-ONLY as a structural excitability OFFSET (shifts the rheobase, not the band/signal),
    no "γ negligible" claim. The **felt percept** hands off to the **mind** volume (firewall). Absolute
    Hz/spike-count, the f–I shape, and the single-stage collapse are named [O]. Deterministic (2×sha256),
    folded into the verifier's foundation list; no γ added. **The down-conversion spine E0→E8 is complete.**
  - `research/E8-graded-to-spike-rate/gate_E8.py` — the focused E8 pass/fail gate (`E8 GATE: PASS`).
  - `research/E9-red-green-dichromacy/run.py` — **E9, BUILT (v0.13.0):** *red-green colour vision /
    dichromacy* — the **first mechanism extension beyond the spine**. It carries the carrier no further
    down; it reads what the FROZEN **E1** angle map already FORCES about colour and *why* the commonest
    inherited colour-vision difference is **red-green**. Colour is propagation angle χ(λ), so three cones
    are three angle-samples and the three discrimination axes are the three pairwise angle **margins**
    (byte-equal off the frozen `chi_deg`): S-M = 0.0509°, **M-L green-red = 0.0421° — the smallest**
    (1.208× tighter than S-M), S-L = 0.0931° ⇒ [F]↔[L] **the angle map makes green-red the structurally
    most fragile axis, matching the epidemiology**. FORCED: coincident λmax ⇒ margin **exactly
    0.000000°**, with a monotone within-band convergence to 0 (sawtooth-proof) that unifies **dichromacy**
    (drop one sample ⇒ one chromatic axis survives) and **anomalous trichromacy** (peaks converge) as ONE
    continuum; a **direction-only** lever (magnitude [O]); and orthogonality colour (angle) ⟂ position
    (image) ⟂ brightness (switch) so the loss costs **exactly one colour axis** while acuity and
    single-photon detection survive (*why* it is colour-blindness, not blindness). γ is READ-ONLY (OPN1LW
    γ=1.4820, OPN1MW γ=1.4058, Δγ=0.0762), **no** claim γ predicts λmax; the X-linked OPN1LW/OPN1MW tandem
    array is [L] genomics. Second firewalled clinical chapter (direction-only, proposal-only). No γ added;
    cone angles byte-equal from the frozen map; SEED=19. Felt percept → mind volume. **The foundation does
    not move:** E9 fetched nothing and re-froze nothing.
  - `research/E9-red-green-dichromacy/gate_E9.py` — the focused E9 pass/fail gate (`E9 GATE: PASS`).
  - `research/E10-light-dark-adaptation/run.py` — **E10, BUILT (v0.14.0):** *light/dark adaptation as gain
    control* — the **second mechanism extension beyond the spine**, and a **NORMAL (non-clinical)** chapter
    (no `MAGNITUDE_BLOCK`, no firewall). It asks what the FROZEN R19 switch already FORCES about how the eye
    spans ~10 decades of background light with a bounded response. The mechanism is **the switch's own
    saturating ON branch**: E2's field on its ON branch is the real root of `s³ − γ·s − h = 0`, so for large
    background h the cubic dominates ⇒ **s*(h) → h^(1/3)** (compressive cube root). (A) a **5.000000-decade**
    background fits a **1.500207-decade** response (compression **3.332873**; cubic order **n=3**); (B) the
    incremental gain `1/(3s*²−γ)` falls **1296.0×** dim→bright (∝ h^(−2/3)) — **automatic** gain control, no
    separate machinery; (C) the headline **Weber-Fechner-like law**: contrast gain `(h/s*)·ds*/dh` pinned by
    the pure-cube limit **EXACTLY at 1/n = 1/3 = 0.333333** and **γ-INDEPENDENT** (RHO 0.333301, CNGB3
    0.333306 at h=10⁶); (D) two regimes — DARK (near fold h*=0.68733, highest gain + E2's single-photon flip)
    vs BRIGHT (deep cube root, low gain). γ READ-ONLY (fold/offset — an OFFSET, as in E7/E8); dark
    re-sensitisation recovery **τ_s=40.0** is the same FROZEN time-constant as E7/E8 (structure [F], absolute
    seconds [O]). No γ added; substrate/Neuron byte-equal; SEED=19. Felt brightness percept → mind volume.
    **The foundation does not move:** E10 fetched nothing and re-froze nothing.
  - `research/E10-light-dark-adaptation/gate_E10.py` — the focused E10 pass/fail gate (`E10 GATE: PASS`).
  - `research/E11-accommodation-refraction/run.py` — **E11, BUILT (v0.15.0):** *accommodation & refractive
    error as the power↔length match* — the **third mechanism extension beyond the spine**, and a
    **CLINICAL (firewalled)** chapter (in `DISEASE_CHAPTERS`, covered by the volume G5 firewall). It consumes
    E3's FROZEN single-surface optics **read-only** and asks what that frozen eye already FORCES about focus:
    a distant object images at **v_∞ = n₂/P**, lands on the retina ⇔ **P·L = n₂**, so everything is the
    dimensionless **match ratio ρ ≡ P·L/n₂**. (A) **emmetropia = ρ = 1** — the frozen Emsley reduced eye sits
    exactly there (**ρ = 1.000000**); focus is a whole curve in power×length, not one eye. (B) **refractive
    error = sign(ρ−1)** — **ρ = 1.050000 > 1** ⇒ focus in front ⇒ **MYOPIA**, **ρ = 0.950000 < 1** ⇒ behind
    ⇒ **HYPEROPIA**, reachable by an eye too long OR too powerful (only the **product** matters; `q·ℓ = 1` ⇒
    **ρ = 1.000000**), direction-only, magnitude **[O]**. (C) **accommodation = a one-signed power lever** —
    `P_req/P_∞ = 1 + n₁/(n₂·k)` rises **monotonically** as the object nears (**1.000750 → 1.375000**), always
    **≥ 1**, supplied by rounding the lens (R↓ ⇒ P↑; `R_req/R_∞` nearest **0.727273**); amplitude **[O]**.
    (D) the lever is **lattice geometry** — `dP/P = −dR/R` (P ∝ 1/R) — and the length axis is the substrate
    **size ∝ γ^1.5** law (PAX6/RAX dwell ratio **1.059595**, read-only, setting the *direction* of the growth
    shift); gene→axial-elongation map **[O]**. Firewall adds `diopter`/`dioptre` + bare `mm` to E9's block, so
    every fact is a dimensionless ratio or a sign (no magnitude token, no "%"). No γ added; substrate
    byte-equal; SEED=19. Felt blur/clarity percept → mind volume. **The foundation does not move:** E11 fetched
    nothing and re-froze nothing.
  - `research/E11-accommodation-refraction/gate_E11.py` — the focused E11 pass/fail gate (`E11 GATE: PASS`).
  - `research/E12-acquired-degeneration/run.py` — **E12, BUILT (v0.16.0):** *acquired/degenerative disease as
    the R19 switch carried OVER its fold, with hysteresis* — the **fourth (and hardest) mechanism extension
    beyond the spine**, and a **CLINICAL (firewalled)** chapter (in `DISEASE_CHAPTERS`, covered by the volume
    G5 firewall). It consumes only the **FROZEN** R19 field `ds/dt = γ·s − s³ + h` and its fold
    `h*(γ) = 2(γ/3)^1.5` **read-only**, adding no γ. Distinct from E4: a congenital switch is *born below* its
    fold (static, never flips); a degenerative one **started healthy** (settles ON, s>0) and is carried *over*
    its fold. (A) **drift over the fold** — on RHO (γ **1.4719**, fold h\* **0.687330**) the healthy state
    (**s = 1.316420**) tracks the upper branch down and **collapses in one step** at **h = -0.691855 ≈ −h\* =
    -0.687330** (a *tipping point*, start-independent: a different start collapses at **-0.689701**). (B)
    **hysteresis** — recovery only at the opposite fold **+h\* = 0.687330** (drive **0.691855**), loop width
    **1.383710 ≈ 2·h\* = 1.374661** = the irreversibility margin (early ≠ late). (C) **one geometry, many
    routes** — a LOAD route and a BASIN-SHALLOWING route (erode γ under fixed load **-0.300000** until the fold
    **h\*(γ) = 0.296976** meets it at **γ = 0.841231**) **both land on the one locus h = −h\*(γ)** (gap
    **0.003024**), so the shared late picture across AMD/glaucoma/diabetic retinopathy is **forced** while each
    primary stress's identity is **[O]**. (D) **γ = STRUCTURAL fragility** — lower γ ⇒ shallower basin ⇒ tips
    under less stress (CNGB3 h\* **0.533080** → PDE6B h\* **0.732285**, span **1.373687**, read-only), with the
    loudest caveat in the volume: the disease-gene→γ map is *even more* **[O]** than E4 (polygenic,
    age/environment-gated, mostly non-promoter — no monogenic purchase). Firewall adds
    `hba1c`/`mg/dl`/`mmol/l`/`mmol/dl` + bare `mm`/`mmhg` to E9's block, so every stress is a dimensionless
    multiple of the gene's own fold (no magnitude token, no "%"). No γ added; substrate byte-equal; SEED=19.
    Felt loss of sight → mind volume. **The foundation does not move:** E12 fetched nothing and re-froze nothing.
  - `research/E12-acquired-degeneration/gate_E12.py` — the focused E12 pass/fail gate (`E12 GATE: PASS`).
  - **OUTPUT is always ONE zip.** Every session returns the whole package as a single archive.
  - **회귀금지 / no-regression.** Inherited values never drift; the verifier enforces byte-identity.
  - **누락금지 / no-omission.** Every promised artifact stays present; the verifier enforces it.
  - **No tuning.** Every constant is a measured input (cited) or a derived value — never fitted.
  - **Firewall** (`FIREWALL.md`): γ reads promoter STRUCTURE only; the felt percept is the mind
    volume's; nothing diagnoses, treats, or prescribes — every disease section is proposal-only.
