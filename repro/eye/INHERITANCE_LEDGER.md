# INHERITANCE LEDGER (기초 상속자료) — vp_eye_emergence_seed

Every inherited artifact, its frozen sha256, and where it comes from. The verifier asserts each
is **byte-identical** to the hash below (no-regression). Nothing here was re-derived in this seed.

| inherited artifact | sha256 (frozen) | provenance |
|---|---|---|
| `inherited/dna_interpreter.py` | `4929932d90321790…` | canonical A4-grammar (DNA v1.13: γ, switch, helix geometry), byte-identical |
| `inherited/eye_promoters.cache.json` | `1a35cc128b367df8…` | **19** measured human promoter sequences (NCBI, cached) — 16 + AIPL1/RPGR/PDE6B (v0.6.0) |
| `inherited/gamma_pipeline.py` | `4bde475df52a7a12…` | offline γ recompute (SantaLucia-1998 NN ΔG37) |
| `inherited/key_pipeline_full.py` | `3141fa22cfe34a94…` | canonical A4 region pipeline (shells/anchors/robust_z), byte-identical |
| `inherited/organ_gamma.json` | `eedc65510f30746e…` | measured readable-layer atlas: γ (level) + A4 (shape) — **19** genes incl. AIPL1/RPGR/PDE6B (v0.6.0) |
| `inherited/vp_color_by_angle.py` | `7aeb66b8530c1d4b…` | colour separated by propagation angle χ |
| `inherited/vp_dna_reading.py` | `f5ea1709bf091467…` | the seed reading: γ (LEVEL) + A4 (SHAPE) per promoter |
| `inherited/vp_light_emergence_quantum.py` | `e0e987517c6f3318…` | light emergence + angle law (physics §10.9) |
| `inherited/vp_substrate.py` | `a4bbbb18d564460a…` | R19 switch primitive (sensory_organ/neuro, byte-identical) |
| `inherited/vp_visible_band_canonical.py` | `77fd18c38ac3fd67…` | **visible-band canon from physics v0.11.0 (§9.4/§10.9/§11)**: D, the band table, the RCROSS(633/532) two-channel closure — forced relations recomputed bit-exact, unit-realization chain quoted (v0.7.0) |

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

**Measured γ provenance:** every sequence in `inherited/eye_promoters.cache.json` was fetched from NCBI
nuccore (GRCh38 current RefSeq chromosomes) by exact accession + TSS−2000..+500 window + strand,
and is cached so γ recomputes offline bit-for-bit. The fetcher that built it ships at
`tools/fetch_promoter_gamma.py`; re-audit against live NCBI with `--cache`.

## Deliberate re-freeze log (no-regression, 회귀금지 — the ONLY sanctioned way the foundation changes)

- **v0.6.0 (E4, congenital blindness).** The three deferred congenital-blindness master genes
  **AIPL1** (NC_000017.11, −, γ=1.4656), **RPGR** (NC_000023.11, −, γ=1.3915), and **PDE6B**
  (NC_000004.12, +, γ=1.5354) were fetched with `tools/fetch_promoter_gamma.py` (measured γ =
  −mean SantaLucia-1998 NN ΔG37 over TSS−2000..+500), folded into `inherited/eye_promoters.cache.json`
  and `inherited/organ_gamma.json` (16 → 19 genes; removed from the atlas `_to_measure` queue, SIX6
  remains deferred), with the full γ (LEVEL) + A4 (SHAPE) reading recomputed by the canonical grammar.
  Those two artifacts were then **re-frozen** here (cache `e88cfd5c…`→`1a35cc12…`, atlas
  `59650f9e…`→`eedc6551…`). *Why:* E4 is the seed's goal increment (the blindness layer) and needs the
  six blindness switches present and verifiable offline. No other inherited artifact changed; the
  substrate, the wave modules, the DNA grammar, and the reading module are byte-identical to v0.5.0.
  γ measured, never fitted.

- **v0.7.0 (visible-band canon, inherited from physics).** One new frozen foundation module,
  `inherited/vp_visible_band_canonical.py` (sha `77fd18c38ac3fd67…`), was brought in from the
  **physics** source volume **v0.11.0** (DOI 10.5281/zenodo.17932566), reproducing: the invariant
  quantum diameter **D = 4.852620 pm** and its two-route cross-check (§9.4 / §3.4); the
  light-propagation-angle **band table** sinχ=λ/(mD), m=⌈λ/D⌉ that places gamma (m=1, quasi-longitudinal)
  → **visible (m≈10⁵, near-transverse 89.8°–89.9°)** → radio (m huge, transverse) (§10.9); and the
  **RCROSS(633/532)** two-channel closure m·sinχ·D/λ=1 on the one shared D, with the unit-realization
  chain a=λ_ref/N, A=a/g*, D=2πλ/A, Δt=Aa/c **quoted** from §11.2–11.6. *Why:* the re-scoped goal (the
  high→low-frequency down-conversion ladder; see `BLUEPRINT.md`) needs rung 1 — *which carrier the eye
  is handed, and the precise 633/532 method that fixes a visible wavelength* — to be inherited and
  verifiable offline, rather than re-derived. The module adds **no biology and no tuning**: the FORCED
  relations are recomputed bit-exact from D; the jammed-lattice percolation that *measures* the
  amplification A lives in the physics bundle and is consumed, not re-measured ([V-elsewhere]). No
  existing inherited artifact changed; this is a pure addition (9 → 10 frozen files).

- **v0.8.0 (E5, the frequency ladder) — no re-freeze.** E5 is a pure research increment
  (`research/E5-frequency-ladder/`); it added **no** inherited artifact and re-froze **nothing**. Every
  inherited file remains byte-identical to v0.7.0. E5 reads γ(GUCY2D) byte-equal from the frozen atlas,
  the substrate/Neuron from the frozen `vp_substrate.py`, and rung 1 from the frozen
  `vp_visible_band_canonical.py`; ν/E are forced from the SI-exact constants. Recorded here only to keep
  the per-version discipline (every version states what it did or did not change).

- **v0.9.0 (E6, why the band is visible) — no re-freeze.** E6 is a pure research increment
  (`research/E6-why-visible/`); it added **no** inherited artifact and re-froze **nothing**. Every
  inherited file remains byte-identical to v0.7.0/v0.8.0 (the 10 frozen hashes above are unchanged). E6
  reads the angle law, the SI-exact constants (c=299792458 m/s, h=6.62607015e-34 J·s), and the invariant
  **D = 4.852620 pm** byte-equal from the frozen `vp_visible_band_canonical.py`, and γ(GUCY2D) byte-equal
  from the frozen atlas for its no-drift check; SEED=19. The two physiological/optical inputs it cites —
  the conventional visible band (380–750 nm) and the reversible 11-cis→all-trans isomerisation window
  (~1.8–3.3 eV) — are **measured/cited inputs frozen as written**, not fits and not derived from package
  data. The chromophore energy that sets the window is coding/photochemistry **outside** the promoter-γ
  this seed reads — a named **[O]**, not invented. No genome re-derived; no tuning.

- **v0.10.0 (E7, the cascade as the band-setting low-pass) — no re-freeze.** E7 is a pure research
  increment (`research/E7-cascade-lowpass/`); it added **no** inherited artifact and re-froze **nothing**.
  Every inherited file remains byte-identical to v0.7.0/v0.8.0/v0.9.0 (the 10 frozen hashes above are
  unchanged). E7 imports the **FROZEN** `vp_substrate.py` and reads the linear filter directly off its
  recovery law `w += dt*(s − β·w)/τ_s` exactly as written (β=0.5, τ_f=1.0, τ_s=40.0 byte-equal); it
  measures the transfer function of that frozen integrator (DC gain 1/β, cutoff f_c=β/(2πτ_s), 45° phase,
  −20 dB/dec) and confirms the full FROZEN Neuron inherits a band that falls in τ. γ(GUCY2D)=1.365 is
  read byte-equal from the frozen atlas for the no-drift check and the γ-secondary comparison; SEED=19.
  The filter law and all constants are **quoted from the frozen substrate, not refitted** — E7 adds no γ
  and introduces no tuning knob. The single-pole idealisation (vs. the real multi-stage
  rhodopsin→transducin→PDE→cGMP→CNG cascade) and the absolute τ→Hz calibration are named **[O]**, not
  invented. No genome re-derived; no inherited byte changed.

- **v0.11.0 (E8, graded→spike-rate re-quantisation) — no re-freeze.** E8 is a pure research increment
  (`research/E8-graded-to-spike-rate/`); it added **no** inherited artifact and re-froze **nothing**.
  Every inherited file remains byte-identical to v0.7.0–v0.10.0 (the 10 frozen hashes above are
  unchanged). E8 imports the **FROZEN** `vp_substrate.py` and treats its R19 Neuron's fold-crossing
  up-crossings *as* the spike train — the graded photoreceptor signal is the drive, the output is the
  spike **rate**. It reads the FitzHugh-Nagumo constants byte-equal as written (β=0.5, τ_f=1.0,
  τ_s=40.0) and re-derives, never refits: the rheobase floor (silent below the fold), the strictly
  monotone rate code over the operating band g∈[0.25,0.90], the discrete-clock regularity (ISI
  CV≈0.0002), the honest depolarisation-block ceiling (the f–I curve is a **bandpass in drive**, not
  monotone — kept as an honest negative, 반증=발견), carrier-invariance of the rate (rate⟂carrier f,
  spread 1.53%; rate∝envelope, closing the loop with E5/E7), and that the spike rate sits in the low
  (~10–100 Hz) band. γ(GUCY2D)=1.365 is read byte-equal from the frozen atlas only as a structural
  excitability **offset** (it shifts rheobase via spinodal(γ), not the band or the signal); the E7-style
  ">3× secondary" γ inequality was tested and **deliberately not forced** (γ moves rate about as much as
  drive does) — another preserved honest negative. SEED=19; deterministic 2×SHA-256
  (E8 run.py sha `bf47f1d0ea6c85f4…`). The absolute Hz/spike-count calibration, the precise f–I shape,
  the single-stage collapse of the real retinal spiking network, and the felt percept (→ mind volume)
  are named **[O]**, not invented. With E8 the high→low-frequency **down-conversion spine E0→E8 is
  complete**. No genome re-derived; no inherited byte changed.

- **v0.12.0 (the multi-chapter HTML volume) — no re-freeze.** This is the *publication* layer over the
  finished E0→E8 spine; it is a pure additive increment that re-froze **nothing** and added **no**
  inherited artifact. Every inherited file remains byte-identical (the 10 frozen hashes above are
  unchanged). The new code (`tools/{_volume_lib.py, build_volume.py, gate_volume.py}`) and the rendered
  site (`docs/eye/`: a hub, nine chapter pages, nine `facts/*.json`, `assets/volume.css`, and
  `sitemap.xml`/`robots.txt`/`llms.txt`) **consume** the increments one-way and **edit no `run.py`** — the
  chapter scripts stay in the verifier's determinism list, untouched. The volume adds **no physics, no γ,
  and no tuning**: it does not re-derive a single number, it *runs* each chapter's `run.py` and republishes
  that script's own verbatim output. The discipline is mechanical: the page embeds each transcript
  hash-pinned (`<pre data-run data-sha>`), every prose number is asserted to be a substring of that live
  transcript at build time (`F()`), and `tools/gate_volume.py` re-proves the whole deliverable from the
  shipped files with seven checks (`VOLUME GATE: PASS`) — determinism (G1), code→facts sha (G2),
  page→code byte-identity / **drift 0** (G3), fact-in-transcript-and-HTML (G4), the **E4** magnitude
  firewall in the rendered prose (G5, no `MAGNITUDE_BLOCK` token, no `%`), static machine-readability (G6,
  JSON-LD only, no executable JS), and no-omission (G7). The gate was checked to be **non-vacuous**
  (corrupting a prose number trips G4; flipping one transcript byte trips G3). The firewall token list is
  read **verbatim** from E4's `run.py` (`load_magnitude_block()`), so it cannot drift from the code it
  guards. Named **[O]**, not invented: the official live-site merge — canonical `paper_id`, `301`
  redirects, and the cross-volume DOI registry entry — is a separate VP-SPEC **Phase 5** step against the
  live site and is deliberately **outside** this offline-verifiable package. No genome re-derived; no
  inherited byte changed. **The Eye volume now ships as one zip.**

- **v0.13.0 (E9, red-green colour vision / dichromacy) — no re-freeze.** E9 is a pure research increment
  (`research/E9-red-green-dichromacy/`) and the **first mechanism extension beyond the down-conversion
  spine**; it added **no** inherited artifact, **fetched nothing**, and re-froze **nothing**. Every
  inherited file remains byte-identical to v0.7.0–v0.12.0 (the 10 frozen hashes above are unchanged, and
  `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0). E9 imports the **FROZEN** angle map and
  reads `chi_deg` byte-equal at the already-measured cone λmax (S 420, M 530, L 560 nm) — it does **not**
  re-derive a single inherited number. From the frozen angles it re-derives, never refits: the three
  colour-discrimination axes as the three pairwise angle **margins** (S-M = 0.0509°, **M-L green-red =
  0.0421° — the smallest**, 1.208× tighter than S-M; S-L = 0.0931°), the **exactly-zero** margin at
  coincident λmax (χ is a function of λ alone), the monotone within-band convergence to 0 (sawtooth-proof,
  unifying dichromacy and anomalous trichromacy as one continuum), the direction-only lever (magnitude
  named **[O]**), and the orthogonality of colour (angle) ⟂ position (image) ⟂ brightness (switch) that
  makes the loss cost **exactly one colour axis** while acuity and single-photon detection survive. γ is
  read **READ-ONLY** from the frozen atlas (OPN1LW γ=1.4820, OPN1MW γ=1.4058, Δγ=0.0762, A4 shapes 1.40×
  apart) as a structural offset, with **no** claim that γ predicts λmax; the X-linked OPN1LW/OPN1MW tandem
  array is named **[L]** genomics, not γ. This is the package's **second firewalled clinical chapter**
  (after E4): direction-only, proposal-only, with its own `MAGNITUDE_BLOCK` asserted absent from the
  transcript, and the rendered chapter is now covered by `gate_volume.py`'s G5 firewall (which loops both
  E4 and E9). SEED=19; deterministic 2×SHA-256. The felt percept of colour is named **[O]** (→ mind
  volume), not invented. No genome re-derived; no inherited byte changed; the foundation does not move.

- **v0.14.0 (E10, light/dark adaptation = gain control on the R19 switch) — no re-freeze.** E10 is a pure
  research increment (`research/E10-light-dark-adaptation/`) and the **second mechanism extension beyond
  the down-conversion spine**, and — unlike E9 — a **NORMAL, non-clinical mechanism** chapter (like E5–E8:
  no `MAGNITUDE_BLOCK`, no firewall, no clinical claim). It added **no** inherited artifact, **fetched
  nothing**, and re-froze **nothing**. Every inherited file remains byte-identical to v0.7.0–v0.13.0 (the
  10 frozen hashes above are unchanged, and `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0 and
  v0.13.0). E10 imports the **FROZEN** R19 field (`vp_substrate.sdot`/`spinodal`, the Neuron's τ_s=40.0/β=0.5)
  and the atlas γ — it does **not** re-derive a single inherited number. From the frozen switch it
  re-derives, never refits: E2's ON-branch steady state as the real root of `s³ − γ·s − h = 0`, which for
  large background drive saturates onto the cube root **s*(h) → h^(1/3)** (every s* a true zero of the
  frozen field, max residual 2.3e-13). The forced results: dynamic-range compression (a **5.000000-decade**
  background fits a **1.500207-decade** response, compression **3.332873**; the deep sweep gives the cubic
  order **n=3**); automatic gain control with **no separate machinery** (incremental gain `1/(3s*²−γ)` falls
  **1296.0×** dim→bright, ∝ h^(−2/3)); and the headline **Weber-Fechner-like law** — the contrast gain
  `(h/s*)·ds*/dh` is pinned by the pure-cube limit **EXACTLY at 1/n = 1/3 = 0.333333** and is
  **γ-INDEPENDENT** (RHO γ=1.4719 → 0.333301, CNGB3 γ=1.2425 → 0.333306 at h=10⁶). γ is read **READ-ONLY**
  from the frozen atlas as a fold/offset (it sets where dark sensitivity sits; the compression law is the
  cubic *order*, not γ — an OFFSET, as in E7/E8); the dark re-sensitisation **recovery τ_s=40.0** is the
  same FROZEN time-constant that set the band (E7) and the rate code (E8) — structure **[F]**, absolute
  seconds the inherited **[O]**. SEED=19; deterministic 2×SHA-256 (steady state solved by deterministic
  Newton). The felt brightness percept is named **[O]** (→ mind volume), not invented. No genome
  re-derived; no inherited byte changed; the foundation does not move.

- **v0.15.0 (E11, accommodation & refractive error = the power↔length match on the R19/E3 eye) — no
  re-freeze.** E11 is a pure research increment (`research/E11-accommodation-refraction/`) and the **third
  mechanism extension beyond the down-conversion spine** — and, like E9, a **CLINICAL/condition** chapter
  (myopia/hyperopia/presbyopia), so it joins `DISEASE_CHAPTERS` and is covered by the `gate_volume.py` **G5**
  firewall (and its own `gate_E11.py` **G8**). It added **no** inherited artifact, **fetched nothing**, and
  re-froze **nothing**. Every inherited file remains byte-identical to v0.7.0–v0.14.0 (the 10 frozen hashes
  above are unchanged, and `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0, v0.13.0 and v0.14.0).
  E11 imports E3's **FROZEN** single-surface optics (read-only, via `importlib`, never re-derived) and the
  substrate **dwell** size-law + atlas γ — it does **not** refit a single inherited number. From the frozen
  reduced eye it re-derives, never tunes: the distance image forms at `v_∞ = n₂/P` with `P = (n₂−n₁)/R`, lands
  on the retina ⇔ `P·L = n₂`, so everything turns on the dimensionless **match ratio ρ ≡ P·L/n₂**. The forced
  results: **emmetropia = ρ = 1** (the frozen Emsley reduced eye sits exactly there, **ρ = 1.000000**, focus a
  whole curve in power×length); **refractive error = sign(ρ−1)** (**ρ = 1.050000 > 1** ⇒ focus in front ⇒
  myopia; **ρ = 0.950000 < 1** ⇒ behind ⇒ hyperopia; reachable by an eye too long OR too powerful because only
  the **product** matters — a too-strong eye `q·ℓ = 1` returns **ρ = 1.000000**), stated **direction-only**;
  **accommodation = a one-signed power lever** `P_req/P_∞ = 1 + n₁/(n₂·k)` rising **monotonically** as the
  object nears (**1.000750 → 1.375000**) and always **≥ 1**, supplied by rounding the lens (R↓ ⇒ P↑,
  `R_req/R_∞` nearest **0.727273** re-focuses on the retina); and the **lever = lattice geometry** (`dP/P =
  −dR/R`, P ∝ 1/R; the √(B/ρ) index rule of E3) with the **length** axis the substrate size-law **size ∝
  γ^1.5** (E1) — PAX6 read-only (PAX6/RAX dwell ratio **1.059595**) instantiates the *direction* of the
  growth shift. γ is **READ-ONLY**; the dioptric magnitude, accommodation amplitude, absolute near-distances,
  and the gene→axial-elongation map are each named **[O]**. **Firewall:** E11's `MAGNITUDE_BLOCK` mirrors E9's
  and **adds** `diopter`/`dioptre` and bare `mm`, forcing every fact to be a dimensionless ratio or a sign —
  G8 and G5 both confirm no magnitude token, no "%". SEED=19; deterministic 2×SHA-256 (run.py sha256
  c2acaf2613319917…). The felt blur/clarity percept is named **[O]** (→ mind volume), not invented. No genome
  re-derived; no inherited byte changed; the foundation does not move.

- **v0.16.0 (E12, acquired/degenerative disease = the R19 switch carried OVER its fold, with hysteresis) — no
  re-freeze.** E12 is a pure research increment (`research/E12-acquired-degeneration/`) and the **fourth
  mechanism extension beyond the down-conversion spine** — and, like E4/E9/E11, a **CLINICAL/condition**
  chapter (the late picture shared across AMD, glaucoma and diabetic retinopathy), so it joins
  `DISEASE_CHAPTERS` and is covered by the `gate_volume.py` **G5** firewall (and its own `gate_E12.py` **G8**).
  It added **no** inherited artifact, **fetched nothing**, and re-froze **nothing**. Every inherited file
  remains byte-identical to v0.7.0–v0.15.0 (the 10 frozen hashes above are unchanged, and
  `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0 through v0.15.0). E12 imports only the **FROZEN**
  R19 field (`vp_substrate.sdot`/`spinodal`/`barrier`) and the atlas γ (read-only) — it does **not** refit a
  single inherited number, and adds no γ. The honest physics (distinct from E4): a congenital switch is one
  *born below its fold* (static, **never flips**); a degenerative disease is the opposite history on the same
  field — a switch that **started healthy** (settles ON, s>0) and is carried *over* its own fold by an
  accumulating stress. On RHO (read-only, **γ = 1.4719**, fold **h\*(γ) = 0.687330**, barrier **γ²/4 =
  0.541622**) the healthy state settles at **s = 1.316420** and tracks the upper branch down to the spinodal,
  collapsing in one step at **h = -0.691855 ≈ −h\* = -0.687330** (a **tipping point**, start-independent: a
  different healthy start collapses at **h = -0.689701**). Because the transition is a fold it is **hysteretic**
  — recovery comes only at the *opposite* fold **+h\* = 0.687330** (drive **0.691855**), the loop width
  **1.383710 ≈ 2·h\* = 1.374661** being the irreversibility margin (early ≠ late). One catastrophe geometry,
  many routes: a **load route** (lower h to −h\*) and a **basin-shallowing route** (erode γ under a fixed load
  **-0.300000** until the shrinking fold **h\*(γ) = 0.296976** meets it at **γ = 0.841231**) **both land on the
  one locus h = −h\*(γ)** — so the shared late picture is *forced* while each primary stress's identity stays a
  named **[O]**. γ is **READ-ONLY** as a *structural* fragility offset (lower γ ⇒ shallower basin ⇒ tips under
  less stress; spinodal-monotone CNGB3 **h\* = 0.533080** → PDE6B **h\* = 0.732285**, span **1.373687**), with
  the **loudest caveat in the volume**: the disease-gene→γ map is *even more* **[O]** than E4 — these diseases
  are polygenic, age/environment-gated, mostly non-promoter common variants, so the promoter-γ this package
  reads has essentially **no monogenic purchase** here. **Firewall:** E12's `MAGNITUDE_BLOCK` mirrors E9's and
  **adds** `hba1c`/`mg/dl`/`mmol/l`/`mmol/dl` and bare `mm`/`mmhg` guards, forcing every stress to be a
  dimensionless multiple of the gene's *own* fold — G8 and G5 both confirm no magnitude token, no "%". SEED=19;
  deterministic 2×SHA-256 (run.py sha256 aebf37d4882325dd…). The felt **loss** of sight is named **[O]** (→
  mind volume), not invented. No genome re-derived; no inherited byte changed; the foundation does not move.

**This seed's own persistent identifier (Zenodo concept DOI, all-versions):**
**10.5281/zenodo.20790134** — resolves to the latest `vp_eye_emergence_seed` release. (This is the
package's *own* identity, distinct from the *source* volume DOIs listed above, which this seed consumes
one-way and never edits.)
