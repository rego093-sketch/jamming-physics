# CHANGELOG — Neural Emergence Chain v1.8 → v1.10

Author-directed **integrity** release. Builds on `neuro_emergence_chain_integrated_v1_8`.
The theme is the VP-SPEC C1 rule taken to its conclusion: **every constant is either a
measured input (locked + cited) or a derived value — never a number chosen to hit a
target.** Nothing scientific is silently changed; where a number was a fit, it is replaced
by an honest range, a derivation, or an explicit `[O]`. Every chapter's reproduction still
regenerates deterministically and `verify_all.py` is still **5/5**.

DOI of record stays **10.5281/zenodo.17979015** (concept DOI). v1.9 is a new living-version
snapshot; the published Zenodo deposit is unchanged by this repo edit.

---

## v1.10.1 — §03 dimensionless γ/θ ratio brought IN-PACKAGE (the last open in-track item)

Closes the one remaining actionable neuro-side item from the v1.10.0 handover (open item #5):
the §03 working-memory ratio γ/θ ≈ 7±2 was previously reproducible **only** in the separate
`neuro_extension` lane. This release adds a **minimal in-package gate** so the **dimensionless
ratio — and only that claim** — re-checks from the one package zip alone. The full model+real-data
§03 regression (τ_inh sweep, autism/Alzheimer tilts, the 17× phase modulation, OpenNeuro reads)
**stays** in the separate lane, unchanged — this is purely additive. `verify_all.py` is still
**5/5**; `run_all.py` is still **18 modules**, all hashes byte-identical (no existing module
touched). No constant is tuned (C1 holds); the ratio is **derived** and validated by **containment**.

DOI of record stays **10.5281/zenodo.17979015**. spec_version stays **1.8** (additive gate, not a
spec or content-milestone change).

- **New gate `repro/neuro/03-rhythm-bands-coupling/verify_band_ratio.py`** (stdlib-only,
  deterministic, bit-for-bit — 2× run gives identical stdout sha256; **BAND-RATIO LOCK PASS 5/5**).
  Kept **outside** `verify_all.py` (exactly like `verify_em_thesis.py` / `verify_boundary.py` /
  `verify_terminology.py`), so `verify_all` stays 5/5. Run standalone: `python3 verify_band_ratio.py`.
- **The derivation is honest, not a fit (C1).** γ/θ is the ratio of **geometric-mean band centres** —
  `geomean(25,50)/geomean(4,8) = √((25·50)/(4·8)) = √39.0625 = 6.25` — using the package's **own**
  non-tuned "centre of a range" (the same construction §14 uses for its geometric-mean cell). It is
  then **validated by containment** in Miller's **independently-measured** 7±2 = [5,9]. The band
  edges come from electrophysiology; the 7±2 from psychophysics — two unrelated measurements that
  **agree**, so the agreement (not a circular fit) is the claim.
- **The containment has teeth (falsifiable).** Broad gamma (30–100 Hz) gives
  `geomean(30,100)/geomean(4,8) = √93.75 = 9.68`, **outside** [5,9] → the gate would FAIL. So the
  check **selects** the biologically-correct theta-coupled **slow** gamma (Colgin 2009); it does not
  assume it. A tamper test confirms the self-verifying `payload_sha256` trips on any silent band-edge
  edit even when the altered ratio still lands in-window.
- **New locked, cited input `…/inputs/band_ratio_properties.json`** (self-verifying `payload_sha256`,
  asserted on load): theta 4–8 Hz (canonical taxonomy; Buzsáki & Draguhn 2004); slow gamma 25–50 Hz
  (the theta-coupled component; **Colgin et al. 2009**, *Nature* 462:353–357, doi:10.1038/nature08573);
  Miller 7±2 (**Miller 1956**, *Psychol Rev* 63:81–97, the independent bound); the count = WM-span
  identity (**Lisman & Jensen 2013**, *Neuron* 77:1002–1016, doi:10.1016/j.neuron.2013.03.007).
- **Honest scope kept `[O]`:** the **absolute** theta and gamma frequencies in Hz are **not** derived
  (they depend on the absolute inhibitory time-constant τ_inh, an external calibration) — matching the
  §03 chapter's existing `[O]`. The ~17× theta-phase modulation depth is the **separate-lane**
  quantity, explicitly out of this gate's scope. All graded in the new
  `…/03-rhythm-bands-coupling/IRREPRODUCIBILITY_LEDGER.md`.
- **`README.md`** in `…/03-rhythm-bands-coupling/` updated to record the in-package gate alongside the
  (unchanged) separate-lane disclosure. **No chapter HTML, no existing module, no frozen hash, and no
  `verify_all` gate count was changed** — the §03 chapter already stated γ/θ ≈ 7±2 as validated with
  Hz `[O]`; this release makes that headline number re-derivable from the one zip.

---

## v1.10.0 — SENSORY ATLAS COMPLETE (the sensory side closed)

The milestone release that **closes the sensory/neural side of the chain**. The motor/EM
side was already complete (EM-emission §13, the full EM link §15, motor quantification §14,
muscle force §16, spinal CPG §17, brain-circulation field §18, ephaptic threshold §19). The
remaining gap was sensory: §10/§12 had emerged five modalities (vision · hearing · smell ·
taste · skin-temperature), leaving touch, pain, proprioception, and balance unaccounted. This
release adds the **§20 capstone**, in which those four remaining modalities **emerge from real
measured γ** and transduce — so all **nine** human sensory modalities now stand on the same
substrate. `verify_all.py` is still **5/5**; `run_all.py` is now **18 modules**, all
deterministic, hashes frozen, HTML↔code drift 0. No constant is tuned to a target (C1 holds).

DOI of record stays **10.5281/zenodo.17979015** (concept DOI). spec_version stays **1.8**
(this is a content milestone, not a spec change).

- **New chapter `docs/neuro/20-complete-sensory-atlas/` (canonical HTML) + `repro/neuro/20-…/`
  (reproduction).** The four remaining modalities emerge from their master genes' measured
  stacking stiffness γ — the **same READ-ONLY primitive** that writes DNA genes and fires
  neurons — and each is wired to a transducer whose **defining property is measured, never
  tuned**:
  - **(5) touch** — low-threshold mechanoreceptor (PIEZO2) on the already-emerged skin organ.
  - **(6) warmth** — low-threshold thermoreceptor (the §10 receptor), same skin organ.
  - **(7) pain** — HIGH-threshold polymodal nociceptor (master **PRDM12**, **TRPV1** heat arm).
    Stays **silent** at innocuous 35 °C / gentle 0.2 press; **fires** at noxious 50 °C / 1.0
    press. The high-vs-low threshold ORDER is anchored to the **measured TRPV1 43 °C**
    (Caterina 1997) — a locked, cited input, not a fitted number.
  - **(8) proprioception** — muscle spindle (master **RUNX3** · PIEZO2). Ia firing rises with
    stretch and feeds the §11 `ReflexArc`, **closing the reflex loop onto an ACTUAL afferent
    organ** (closed-loop error 0.0481 vs open 0.5000, disturbance rejection ×10.4) — §11 had
    only referenced an abstract "stretch feedback".
  - **(9) vestibular** — directional hair cell (master **ATOH1** · OTOP1). The response is
    **signed** about a resting discharge (equal-magnitude accelerations of opposite sign give
    different firing), unlike unsigned pressure — from hair-cell morphological polarisation.
- **Real measured γ for 14 sensory master genes**, fetched from NCBI (Homo sapiens, GRCh38;
  the reproducible `[TSS−2000, TSS+500]` promoter window; SantaLucia-1998 NN stacking table)
  and **cached for offline reproduction** in `repro/neuro/_engine/data/`. New files:
  `full_sensory_gamma.json` (the γ atlas + `_atlas` master-gene map), `full_sensory_promoters.cache.json`
  (the cached sequences — re-running the fetch reproduces identical γ), and the fetch script
  `fetch_full_sensory_gamma.py`. Honesty check: **corr(γ, GC) = 0.997** over the new genes
  (organ atlas 0.994, taste 0.995) — γ tracks measured sequence, so the organs emerge from
  biology, never fitted.
- **Engine extended ADDITIVELY** (`repro/neuro/_engine/vp_neuro_engine.py`): two stimulus
  classes (`StretchStimulus`, `AccelStimulus`) and three receptors (`Nociceptor`,
  `Proprioceptor`, `VestibularReceptor`). **All existing classes are untouched**, so every one
  of the 17 prior modules produces **byte-identical** output (verified: all "matches frozen ✓",
  drift 0). The new receptors keep the framework discipline — the only constants are measured-cited
  (`T_NOX = 43.0 °C`, TRPV1) or explicitly `[O]` (`P_NOX` mechanical noxious threshold; `REST`
  vestibular resting rate/gain; all absolute magnitudes).
- **`repro/neuro/20-…/IRREPRODUCIBILITY_LEDGER.md` (new, VP-SPEC C3).** Enumerates §20's five
  `[O]` items — absolute organ size, absolute developmental time, absolute firing rates, the
  absolute mechanical noxious threshold, the vestibular resting rate/gain — each with a stated
  obstacle and a named closing dataset, and separates them from what IS measured (TRPV1 43 °C,
  the 14 γ values) and what reproduces (order, relative size, threshold order, loop closure,
  directionality).
- **What is LOCKED vs OPEN.** Layer-1 `[F]` (from measured γ): the developmental **ORDER**
  (vestibular → proprioceptor → nociceptor), the relative **SIZE** (nociceptor > proprioceptor
  > vestibular, DWELL ∝ γ^1.5), and the threshold **ORDER** (nociceptor HIGH vs touch/warmth
  LOW). Layer-2 `[O]` (in the ledger): the absolute size/time/firing magnitudes, the absolute
  mechanical noxious threshold, and the vestibular resting rate/gain.
- **Harness + metadata updated.** `run_all.py` now lists §20 (18 modules; self-reports the
  count); `docs/neuro/_meta.json` adds the §20 chapter entry (21 chapters total); `REPRODUCE.md`
  updated to the 18-module roster + the new sensory modules + a §20 worked cross-check.

> **Near-completion status.** With this release the **sensory side is closed** the same way the
> motor/EM side already was: every modality emerges from a measured-γ organ and transduces into
> the low-frequency spike train the chain reads, with each illustrative magnitude honestly graded
> `[O]`. What remains genuinely open is **subjective experience**, which is deferred by design to
> the companion `mind` paper (see `PROJECT_BOUNDARY_neuro_mind.md`) — not a gap in the sensory
> emergence chain, but its declared boundary.

---

## v1.9.5 — EM terminology reconciliation (neuro ⟷ mind), shared-SSOT set

Cross-paper alignment pass (the `neuro`/`mind` "left hand / right hand" reconciliation). **No
scientific number changed; no neuro chapter body changed.** All neuro gates stay green
(`verify_all.py` 5/5, `verify_boundary.py` 5/5, `verify_em_thesis.py` 6/6, `verify_terminology.py`
PASS). The work fixes the *words and the register split* so the two papers stop colliding on EM.

- **`EM_NEAR_FAR_THESIS.md` — new §1.2 (the two registers).** Adds, above the affirmed/retired
  body, the explicit split: the disambiguated objects (cable conduction A / ephaptic B, the angle
  law, the three speeds) are the **object layer, owned by `neuro`**; the abstraction the cognition
  reading rides is **"EM = the brainwave = the low-frequency (δ/θ/γ) field,"** stated lock-safely
  (low-frequency = the rhythm/source rate, not a velocity; the field is still `c`). `mind` cites
  `neuro` for the objects; `neuro` owns them.
- **`TERMINOLOGY_canonical.md` — new §7 (register & ownership) + mind-register banned rows.**
  An ownership map (own = use in full vs cite = restate with a status tag) and the per-paper rule:
  `neuro` writes the object, `mind` writes the brainwave and cites the object. §5 BANNED gains
  mind-side rows (no re-deriving `neuro`'s ΔVm / radiated fraction / velocity ratio in `mind`; no
  bare "weak"; no single-object "near-field" as carrier).
- **`PROJECT_BOUNDARY_neuro_mind.md` — shared set, not a single file.** §0/§6/§9 updated: the
  byte-identical shared SSOT is now the **three-file set** (EM thesis + terminology canonical +
  this boundary), all mirrored into both packages and guarded.
- **`sync_shared_ssot.py` (new, package root).** The cross-package drift guard: self-check
  (markers present + sha256), `--with <sibling>` (assert byte-identity), `--push <sibling>`
  (one-way mirror). Run after any shared-file edit. The three shared files are currently
  byte-identical across `neuro` and `mind`.

> The mirror half of this work lives in the `mind` package (its §2/§4 prose moved to the cited
> register; it received the full shared SSOT set + mirror `verify_boundary.py` /
> `verify_terminology.py`). The two ship as **two zips, never merged** — see
> `PROJECT_BOUNDARY_neuro_mind.md` §4 and VP-SPEC C4.

---

## 0. Point release v1.9.1 — §14 recruitment bound to CITED motoneuron datasets

The one remaining v1.9 open item (handover item #1: "§14 motoneuron constants are representative,
not a single cited dataset") is now closed. The size-principle derivation is unchanged in form —
recruitment order still falls out of Ohm's law, `rheobase = dVth / R_input` — but its inputs are no
longer representative constants. They are locked to two cited, verbatim-checked datasets, and the
chapter now reports the measured *deviation* from pure Ohm's law instead of inventing per-type means.

- **New locked input file** `repro/neuro/14-motor-quantification/inputs/motoneuron_properties.json`,
  carrying a self-verifying `payload_sha256` (the engine asserts it on load, so silent edits fail):
  - **Fleshman, Munson, Sypert & Friedman (1981)** *J Neurophysiol* 46:1326–1338
    (doi:10.1152/jn.1981.46.6.1326) — cat medial-gastrocnemius motoneuron pool: input resistance
    **0.8–5.1 MΩ**, rheobase **0.8–17.1 nA**.
  - **Gustafsson & Pinter (1984)** *J Physiol* 357:453–483 (doi:10.1113/jphysiol.1984.sp015511) —
    rheobase ∝ input conductance, but the rheobase range **exceeds the conductance range by ~2×**
    because threshold depolarisation rises with rheobase (so it is *not* pure constant-dVth Ohm).
- **Derivation (no tuning).** From the measured resistance span, constant-threshold Ohm's law
  predicts a rheobase span of **×6.375**. A single threshold depolarisation of **7.471 mV** — the
  pool's geometric-mean cell, derived not chosen — puts the pure-Ohm rheobases at **1.465→9.339 nA**,
  both **inside** Fleshman's measured 0.8–17.1 nA range. The magnitude is therefore validated by
  **CONTAINMENT** (the §16 pattern), not by fitting a target nA. The engine `assert`s the containment.
- **Honest deviation reported.** The measured rheobase span (**×21.375**) exceeds the conductance-only
  prediction by **×3.353** — the Gustafsson-&-Pinter signature that threshold rises with rheobase.
  That drift, and the absolute newton force scale, stay explicitly **[O]**. The v1.8/v1.9 "population
  mean ~9.8 nA within 2 nA of a measured value" framing is gone for good (it required tuning); the
  validated claims are now the recruitment **order** and the **containment**.
- **Verification.** `motor_quantification.py` re-frozen (`run_all.py` records a new full-stdout hash);
  the §14 HTML carries only numbers the engine prints (HTML↔code drift 0, 11/11 numbers reproduced);
  `verify_all.py` stays **5/5**. No constant is tuned to hit a target; the package stays one zip.

---

## 0b. Point release v1.9.1 — §18 EM near-field circulation (capstone synthesis)

A new **capstone chapter §18 "EM near-field circulation in the brain"** is added. It writes no new
physics: it **wires the modules already in the package together** — the engine's ionic oscillators,
the §13/§15 lattice emission, and the inherited light-emergence anchor — into one closed near-field
circulation loop, so the chain's own pieces are shown interacting rather than asserted to.

- **New module** `repro/neuro/18-em-brain-circulation/vp_em_brain_circulation.py`. It imports
  `Neuron, dominant_freq, seed_everything` from `_engine` (the same FHN relaxation oscillator the
  whole chain runs on) and pins BLAS threads for determinism, exactly as §15 does. There is **no RNG**.
  - **PART 0 — geometry.** Every EEG band (δ 2, θ 6, α 10, β 20, γ 40 Hz) puts the head at
    `r/(λ/2π) ≈ 10⁻⁸`: the brain sits **deep in the near field**. The radiated fraction is therefore
    negligible **by geometry** (θ: ≈1.143×10⁻¹⁶) and the EM transit lag across the head is ≈3.402×10⁻⁹
    of a cycle. EM is not, and geometrically cannot be, the timing. `[V]`
  - **PART A — ionic ring.** A ring of regions carrying the engine's real FHN waveform, with a
    conduction-delay phase lag; the total loop lag is 1.06814 cycle (**winding 1**), the measured
    Fourier winding is 0.98225, and the phase velocity 3.2044 m/s **≈ the conduction speed** — so the
    clock is **ionic**. `[V]`
  - **PART B — emitted near-field.** The emitted field is `1/r³`-local (nearest-neighbour fraction
    0.3976) and rotates **0.98225 turn per period in lockstep with the ions**. `[V]`
  - **PART C — multiplex.** δ/θ/α/β/γ ride the one medium with recovery error ≈0 and cross-talk
    **≈5.000×10⁻¹⁶** — the §15 matched-filter result, now on the brain ring. `[V]`
- **New chapter** `docs/neuro/18-em-brain-circulation/index.html` — canonical, answer-first (60 words),
  JSON-LD `ScholarlyArticle` position 18 + `BreadcrumbList`, claim-strip, `prev`→§17, no `next`. Every
  displayed ≥3-decimal number is printed by the module (HTML↔code drift 0, **16/16 reproduced**).
- **Honesty (unchanged boundary, §9 register enforced).** What is built is the **physics of
  circulation**, graded `[V]`. Whether the human brain **uses** this near-field for coordination stays
  **OPEN and deferred to the companion paper (Mind)** — there is no dedicated electric organ and
  incidental EEG is weak. The **retired** claims stay retired: no light-speed axonal waveguide / TIR
  fibre, no radiative EEG carrier, no low-freq-sum→information. The affirmed near-field/conduction
  communication (electric-fish lineage) is what §18 builds on.
- **No tuning.** §18 introduces no fitted constant. The representative geometry/conduction inputs
  (R_BRAIN 0.085 m, V_AXON 3.0 m/s, N_REG 8, the band set) are explicitly marked **[O]**; the physics
  conclusions (near-field dominance, ionic timing, lockstep circulation, multiplex separation) do not
  depend on their exact values.
- **Wiring & verification.** `repro/neuro/run_all.py` gains §18 as both a `MODULES` entry and a
  `NEW_CHAPTERS` entry; the module is deterministic (2×/3× sha256 identical) and its full-stdout hash
  is frozen in `expected_sha256.json`. `docs/neuro/_meta.json` gains the §18 chapter (grade `model`,
  1022 words) and `totals` becomes **19 chapters / 9453 words**. `gate_neuro_17.py` (which reads only
  the §17 `_meta` entry) is unaffected. **`verify_all.py` stays 5/5.** The package stays one zip.

---

## 0c. Point release v1.9.2 — §14 force-frequency saturation DERIVED (twitch fusion); dual code unified onto the measured pool

The two remaining v1.9.1 handover items for §14 are now closed the honest way — no tuned constant
is introduced, and the package stays one zip with `verify_all.py` still **5/5**.

**Item #2 (force-frequency was linear, not saturating) — CLOSED by a twitch-fusion derivation.**
The earlier `Muscle.force()` made force rise *linearly* with rate toward the locked twitch:tetanus
ratio, which is not the measured sigmoidal shape. The saturating force-frequency relation is now
**derived from first principles with no free parameter**, and the physics it rests on is *twitch
fusion*:

- **New locked input** `repro/neuro/14-motor-quantification/inputs/muscle_twitch_properties.json`,
  carrying a self-verifying `payload_sha256` (the module asserts it on load):
  - **Fuglevand, Winter & Patla (1993)** *J Neurophysiol* 70:2470–2488 (doi:10.1152/jn.1993.70.6.2470)
    — the analytical motor-unit twitch `h(τ) = τ·exp(1−τ)` (τ = t/T, T = contraction time), the
    impulse response of a critically-damped 2nd-order system, peak 1 at τ=1, carrying **no free
    parameter**; and the result that force-frequency curves **collapse** when rate is normalized to
    the inverse contraction time 1/T.
  - **Rack & Westbury (1969)** *J Physiol* 204:443–460 (doi:10.1113/jphysiol.1969.sp008923) — the
    measured **sigmoidal** isometric tension–frequency relation of cat soleus (twitches fuse into a
    smooth tetanus as rate rises) that the derivation reproduces.
  - **Buchthal & Schmalbruch (1970)** *Acta Physiol Scand* 79:435–452 — human soleus contraction
    time **156.5 ± 14.7 ms**, fixing the scale of the (open) absolute rate axis.
- **Derivation (no tuning).** Summing the cited twitch at firing rate `f` gives a steady-state force
  whose **fusion index** `FI = F_min/F_max` over one cycle rises **monotonically 0→1 and SATURATES**,
  and the whole curve is **universal in the dimensionless rate ν = f·T**: `FI = 0.001, 0.622, 0.884,
  0.969, 0.998` at `ν = 0.1, 0.5, 1, 2, 8`, crossing a **stated** well-fused criterion `FI = 0.90`
  (a readable landmark, not a fitted target) at **ν\* = 1.083**. The module `assert`s monotonicity
  and saturation. This is the §03 pattern: a **dimensionless** shape is derived/validated `[V]`,
  while the absolutes stay `[O]`.
- **Honest scope (stated, not papered over).** Under *linear* twitch summation the **mean** force
  does **not** plateau — only the **fusion** (disappearance of ripple) saturates. The sigmoidal
  **mean-force plateau** additionally needs **nonlinear calcium summation**, which is **not modelled**
  here and stays `[O]`; the **absolute** fusion frequency `f = ν/T` (T muscle/species-dependent,
  tens of ms to ~150 ms) stays `[O]`; the tetanus **amplitude** ratio (~3.9×) remains a locked
  measured input `[O]`. The model is **not** "validated" by reproducing its own amplitude input.

**Item #3 (dual code used the toy 20-unit `Muscle`, not the rheobase pool) — CLOSED by unification.**
The dual-code crossover is now computed on the **same** 5-unit measured rheobase pool used for
recruitment (force = Σ recruited unit sizes × the rate gain `1 + (TET−1)·rate_frac`): **2 units @
max-rate = 1.980 < 5 units @ low-rate = 4.802**, so low force is recruitment-limited and high force
rate-limited on one consistent axis. The toy 20-unit `Muscle` is now **entirely removed from §14**
(`Muscle` dropped from the import); §14's quantitative claims rest only on the cited measured pool
and the derived twitch fusion.

- **Engine and §11 untouched.** The shared `Muscle` class in `_engine/vp_neuro_engine.py` is **not
  edited**, so `11-sensorimotor-loop/run_loop.py` re-verifies **byte-identical** (`matches frozen ✓`).
  Only §14's own module changed.
- **Verification.** `motor_quantification.py` re-frozen (`run_all.py` records a new full-stdout hash);
  the §14 HTML force-frequency section is rewritten to the derived fusion result and carries only
  numbers the module prints (**HTML↔code drift 0, 17/17 numbers reproduced**); `verify_all.py` stays
  **5/5**. No constant is tuned to hit a target; the package stays one zip.

---

## 0d. Point release v1.9.3 — §19 ephaptic threshold: the endogenous near-field measured against the coupling bound (capstone synthesis; the §18 "weak" word corrected)

Author-directed continuation of the **EM thread** — the electromagnetic field is *not* retired by
bias. The chain opens with EM (the neural signal **is** an electromagnetic event; EEG/MEG **are** its
near-field) and §18 built the near-field circulation. But §18's boundary carried one un-measured word:
it called the brain's incidental field *"weak"*, silently conflating two different objects — the
**volume-conducted scalp EEG** (genuinely µV-small) and the **local near-field inside the tissue** (the
LFP gradient, mV/mm — not small). §19 closes that gap the honest way: it **quantifies** the local
endogenous near-field against the **measured** ephaptic-effect threshold, with no tuned constant, and
finds it sits **at** the threshold, not below it. The package stays one zip with `verify_all.py` still
**5/5**.

This is neither tuning to a belief nor dismissing one. The far-field *radiative* carrier stays
correctly **retired** (the brain is geometrically deep in the near field; radiated fraction ≈10⁻¹⁶);
the *near-field ephaptic* coupling is a **different physical object**, and the measurement shows it is
real and at threshold. The two are kept orthogonal — refuting the broadcast does not refute the
coupling.

- **New locked input** `repro/neuro/19-em-ephaptic-threshold/inputs/ephaptic_field_properties.json`,
  carrying a self-verifying `payload_sha256` (the module asserts it on load, so silent edits fail).
  Four cited, verbatim-checked sources:
  - **Fröhlich & McCormick (2010)** *Neuron* 67:129–143 (doi:10.1016/j.neuron.2010.06.005,
    PMID 20624597) — endogenous cortical E-field in vivo `|avg| = 2.29 ± 0.27 mV/mm` (peak 2.36,
    max ≈4.52; in vitro 0.87), and the key result that weak fields **entrain** the slow oscillation
    with an amplitude threshold **inside** that endogenous range.
  - **Bikson et al. (2004)** *J Physiol* 557:175–190 (doi:10.1113/jphysiol.2003.055772,
    PMID 14978199) — somatic field→polarisation is **linear** at `s = 0.12 ± 0.05 mV per (mV/mm)`.
  - **Anastassiou, Perin, Markram & Koch (2011)** *Nat Neurosci* 14:217–223 (doi:10.1038/nn.2727) —
    directly-measured induced subthreshold somatic `ΔVm < 0.5 mV` that nonetheless **strongly entrains
    spike timing** (especially slow rhythms).
  - **Buzsáki, Anastassiou & Koch (2012)** *Nat Rev Neurosci* 13:407–420 (doi:10.1038/nrn3241) — the
    scalp EEG is the attenuated far signal; the local LFP is orders of magnitude larger (the object
    §18 should have named).
- **The carrier is §18's field, not a new one.** `vp_em_ephaptic_threshold.py` **imports**
  `near_field_geometry, ring_positions, near_field_locality, R_BRAIN, BANDS, N_REG` from the §18
  module, so the field analysed is literally §18's near-field (nearest-neighbour share 0.3976,
  radiated fraction 1.143×10⁻¹⁶, lag 3.402×10⁻⁹ cycle — reproduced, not re-asserted). BLAS threads
  pinned; no RNG.
- **Derivation (no tuning), validated by CONTAINMENT — the §16 pattern.** Scaling the measured field
  by the measured sensitivity gives a **derived** membrane polarisation
  `ΔVm = s·E_endo = 0.12 × 2.29 = 0.2748 mV` (range 0.1414–0.4352; 0.5424 at the peak field). This
  sits **inside** Anastassiou's independently-measured bound `ΔVm < 0.500 mV` (margin 0.2252) — two
  labs, two methods (field×sensitivity vs. direct intracellular) agree, so the magnitude is
  **validated `[V]`**, not fitted. The module `assert`s the containment.
- **At threshold, not weak `[V]`.** The endogenous-field / entrainment-threshold ratio is `≈ 1`
  (O(1), not ≪1): the field sits **at** the ephaptic threshold, and the cited measurement shows it
  entrains spike timing. `ΔVm` is 0.0229 of a representative 12 mV distance-to-threshold `[O]` — small
  in isolation, but near threshold the slow trajectory makes it bite. The §18 "weak" claim is thereby
  shown true **only of the scalp signal**.
- **Honest grades.** `[F]` an oscillating ionic charge sources a field (momentum balance, §13).
  `[V]` the contained polarisation and the at-threshold ratio. `[O]` the **absolute** field magnitude
  (a measured input = the §15 αₑₘ, supplied not derived), the in-vitro/in-vivo state dependence (ratio
  2.632), the representative distance-to-threshold. **OPEN (→ Mind):** whether cognition *functionally
  uses* this measured entrainment — open because the **in-vivo behavioural role is untested**, *not*
  because the field is weak. The decisive test is named: a behaviour-labelled intracranial recording
  with the local field **cancelled vs. augmented** in real time (the §9 register's experiment;
  Fröhlich ran the in-vitro feedback version). **RETIRED (never revived):** the far-field radiative
  carrier, the light-speed axonal waveguide, coherent radiative broadcast, low-frequency
  sums→energy→information, DNA phase memory, the vortex field.
- **§18 prose corrected, hash untouched.** `docs/neuro/18-em-brain-circulation/index.html` has its
  boundary clause reworded to distinguish the weak *scalp* EEG from the at-threshold *local*
  near-field, cross-referencing §19, and a `next`→§19 link added. **No number is changed** in §18, so
  the §18 module and its frozen hash are **untouched** (`vp_em_brain_circulation.py` still
  `matches frozen ✓`).
- **Verification.** `vp_em_ephaptic_threshold.py` runs deterministically (2× identical full-stdout
  hash, frozen in `expected_sha256.json`); the §19 HTML carries only numbers the module prints
  (**HTML↔code drift 0, 16/16 numbers reproduced**); the §19 DOIs/citations live in the locked JSON,
  none in the HTML body (matching §18). `docs/neuro/_meta.json` gains the §19 entry (chapters 19→20,
  `totals.words` → new sum 10451), `spec_version` unchanged. `verify_all.py` → **OVERALL: PASS (5/5)**.
  No constant is tuned to hit a target; the package stays one zip.

---

## 1. Scientific corrections (the substance)

### 1.1 §16 bare-zone "fit" — REMOVED (replaced by a derived range + containment)
- **What changed.** v1.8 locked the bare zone as the measured range `b ∈ [0.15, 0.20] µm`
  but then reported the plateau top at the **low end (2.20 µm)** and validated it against
  GHJ-1966's measured 2.20 as an exact `|Δ| = 0` match. Picking `b = 0.15` to land on the
  target is a fit, not a derivation — a C1 violation.
- **Fix.** The plateau top is now reported as the **DERIVED RANGE 2.20–2.25 µm** (the full
  image of the measured bare-zone range under `2I + z + b`). GHJ's 2.20 is validated by
  **CONTAINMENT** — it falls at the **lower edge** of the derived range — not by an exact
  endpoint hit. The three single-valued landmarks (`zero_long` 3.65, `plateau_bot` 2.05,
  `steepen` 1.65 vs measured 1.67) are still validated by `|Δ|`, max **0.02 µm**.
- **Code.** `repro/neuro/_engine/vp_muscle_force_law.py` splits the validation into POINT
  landmarks (tested by `|Δ|`) and a RANGE landmark (tested by containment); the result JSON
  carries `validation_vs_GHJ1966.plateau_top = {derived_lo, derived_hi, measured, in_range,
  edge, dist_to_range_um}`. Chapter prose, the answer/abstract, and the §16 ledger are
  re-worded to the containment framing. `gate_neuro_16` = 16/16, slug-16 fidelity 27/27.

### 1.2 §17 spinodal order — DE-CIRCULARIZED (derived from measured data, not hard-coded)
- **What changed.** v1.8 hard-coded `domains = ["p3","pMN","p2","p1","p0"]` and then
  "validated" that this equals the measured order — a circular check (the answer was typed in).
- **Fix.** `spinodal_order()` now **derives** the ventral→dorsal sequence from two measured
  facts read from the data file: the cross-repression **adjacency names** (`"p3/pMN"`, …) and
  the Shh-**threshold ranking** (higher Shh ⇒ more ventral). The order falls out of
  `[first.ventral] + [each.dorsal]` after ranking the switches by threshold. The Briscoe-2000
  match is now a genuine check (perturb a threshold and the derived order would change).
- **No numeric change.** Output JSON is **bit-identical** to v1.8 (thresholds unchanged,
  representative; absolute Shh profile already `[O]`). slug-17 fidelity 148/148; `gate_neuro_17`
  = 39/39; ledger unchanged (21 items, F10/V3/L3/O3/B2).

### 1.3 §14 size principle — BOUND to measured biology (the middle-link binding)
- **What changed.** v1.8 built the motor unit with a toy size set and asserted the
  force-frequency ratio `≈ 3.9×` against the very `tetanus_ratio = 3.9` it was constructed with
  (`assert abs(ratio − 3.9) < 1e-6`) — a circular self-validation, and the prose claimed
  "exactly 3.9×".
- **Fix (recruitment).** Recruitment order is now **derived from Ohm's law**: a motor neuron
  fires at its rheobase `I = V_threshold / R_input`. With representative measured motoneuron
  constants (an ~11 mV size-invariant threshold and input resistances 2.1→0.7 MΩ across the
  pool; Henneman 1965, Kernell 2006, Heckman & Enoka 2012, Gustafsson & Pinter 1984), the
  derived rheobases rise 5.2→15.7 nA — **ascending = small-first = the size principle**,
  matching the measured **orderly recruitment**. The force-recruitment shape is derived
  (monotone). The population rheobase (~9.8 nA) lies **within the measured motoneuron range**
  (~3–30 nA); the constants are representative measured inputs, **not tuned to a target**.
  *(SUPERSEDED by v1.9.1 §0: these representative constants were replaced by two cited datasets —
  Fleshman 1981 + Gustafsson & Pinter 1984 — with the magnitude validated by containment. The
  recruitment-from-Ohm's-law mechanism is unchanged; only the inputs and the validation tightened.)*
- **Fix (force-frequency).** The twitch→tetanus ratio (~3.9×) is relabelled as a **locked
  measured input** (muscle/species/temperature dependent; precise value `[O]`); the circular
  assertion is replaced by the genuinely-true check that force **rises monotonically** with rate.
- **Open.** The **absolute newton force scale** and the precise per-cell constants stay `[O]`.
- **Code.** `repro/neuro/14-motor-quantification/motor_quantification.py` (rheobase derivation),
  `vp_neuro_engine.py::Muscle` docstring (ratio relabelled — comments only, output unchanged),
  the §14 chapter HTML (recruitment section rewritten), README, and `_meta.json` §14 one-liner.
  The module's frozen hash in `expected_sha256.json` is **re-frozen** to the new deterministic
  value (the change is intentional, output is 2×-sha256 identical, HTML↔code drift 0).

### 1.4 §03 absolute-Hz — SHARPENED (the dimensionless ratio is the one validated thing)
- The chapter now states explicitly that the **dimensionless** γ/θ ratio (gamma cycles per
  theta cycle) ≈ **7±2** — Miller's working-memory capacity, the one cross-frequency quantity
  with a direct causal test (rhythm-locked tACS) — is what is validated, while the **absolute**
  theta and gamma frequencies in Hz depend on the absolute inhibitory time-constant (an external
  calibration) and remain `[O]`. The §03 README is corrected so its regression-lane claim points
  at the separate `neuro_extension` lane (not a bundled `_verify/` folder). No derivation of
  absolute Hz is forced (per the SPEC: do not force a derivation that is not there).

### 1.5 Tuning audit (C1 sweep of every engine)
- Every `repro/neuro/**/*.py` was grepped for constants that match a target output. The **only**
  "assert an input equals itself" anti-pattern was §14's `tetanus_ratio` (fixed in 1.3). All
  other asserts are ordinal/monotonic/sign checks or validations against independent physical
  constants (e.g. §13 emission speed ≈ c; inherited modules' laser wavelengths and round-trip
  self-consistency), which are legitimate.

---

## 2. Structure & tooling

- **Builder path bug fixed.** `tools/build_chapter_neuro.py` set `ROOT = dirname(__file__)`
  (= `tools/`) and therefore wrote chapters to `tools/docs/…`, contradicting its own docstring
  and breaking the C1 "rebuild HTML then re-gate" loop (the gate reads package-root `docs/`).
  `ROOT` is now the package root, so the builder writes to `docs/` as documented. Output is
  byte-identical content; only the destination is corrected.
- **`docs/neuro/_meta.json`**: `spec_version` 1.8 → 1.9; the §14 one-liner corrected to the
  honest implemented result (it had described a tighter "11 nA vs 13 nA within 2 nA" rheobase
  match that is **not** reproducible without tuning constants, so it is replaced by the
  order-validated, within-range statement that the code actually produces).
- The package remains **ONE** self-contained zip (chapters 00–17), not per-chapter fragments.

---

## 3. What is unchanged (immutable / byte-identical)

- **All other chapters' science and numbers**: every module except `motor_quantification.py`
  reproduces its v1.8 frozen `expected_sha256.json` hash bit-for-bit (verified). §17's result
  JSON is bit-identical; §16's canonical number set is unchanged.
- **γ, the locked grammar, the NCBI inputs, the DOIs**: untouched.
- **The verification contract**: `run_all.py`, the slug `run.py`s, and the `gate_neuro_*` gates
  are unchanged; only the §14 frozen hash was re-recorded for the intentional honest edit.

---

## 0e. Point release v1.9.4 — EM near/far thesis LOCK (§9 de-conflict + canonical thesis + gate)

v1.9.3 *measured* the endogenous near-field at the ephaptic threshold (§19) and corrected §18's
one un-measured word. v1.9.4 **locks the resulting thesis across the package** so it cannot drift
back toward "retire EM" in any later session.

**Root cause fixed.** `docs/neuro/09-bounds-open-retired/` had its **answer and abstract** (the
text generative search and session summaries grab first) list **"EM"** flatly among the retired
items (`vortex, EM, TIR, energy = information, DNA phase memory — retired`). That headline
contradicted §18/§19 **and §9's own buried amendment**, so every summarisation propagated "EM
retired." The conflict that stalled progress had this single source: a headline word, wrong.

**Edits (C0 — correcting wrong content is permitted; body meaning otherwise preserved):**
- §9 **answer + abstract**: blanket "EM" → **"the radiative EM far-field carrier"**, with an
  explicit carve-out that EM as such is **not** retired (an electrical signal *is* electromagnetic)
  and the **near-field (ephaptic) form is affirmed (§18–§19)**, only its functional role open.
- §9 **amendment**: added the three measurements that forbid the far-field carrier (non-radiation
  radiated fraction ~10⁻¹⁵; transparency head/δ ~10⁻³; velocity 10⁶× too slow); replaced the
  residual pre-§19 phrase *"the incidental EEG field is weak"* with the §19 result (**scalp** EEG
  weak; **local** near-field **at threshold**, ΔVm ≈ 0.27 mV ⊂ measured < 0.5 mV); heading order
  fixed (the empty `Consciousness → Mind` h2 was reinstated above its own paragraph).
- `_meta.json` §9 `one_liner` now states the EM carve-out; §9 `words` 475 → **588** (the measured
  EM-lock body delta **+113**, gate exclusion rule). *Honest note:* the 475 baseline is the
  package's known-stale older word metric (the v1.8 amendment was never counted; true pre-edit body
  ≈ 693) — only the **edit delta** is applied, to keep `_meta` on one consistent accounting across
  chapters (see `WORK_HANDOVER` inventory note). totals 10451 → **10564**.

**New artifacts (additions, not fragments — C0):**
- **`EM_NEAR_FAR_THESIS.md`** (package root) — the single source of truth both §9 here and Mind §2
  are read under. One physics (Maxwell); near-field/ephaptic **affirmed**; radiative far-field /
  optical-fibre carrier **retired by measurement**; the open variable is **function, not strength**.
- **`repro/neuro/09-bounds-open-retired/verify_em_thesis.py`** — deterministic gate (no RNG; every
  constant a measured input or derived value) that re-derives the numbers and asserts **both**
  boundaries, so it fails if a session tries to retire EM wholesale **or** revive the far-field
  broadcast. `reports/lock-neuro-09-em-thesis.gate.json` records **6/6 PASS**. Kept standalone
  (outside `run_all`, which is why `verify_all.py` stays 5/5); wire into `verify_all.py` when desired.

**Anti-drift rule (now locked):** "EM" is never a blanket retired item; only the radiative
far-field / TIR carrier is. To retire EM wholesale or revive the far-field broadcast, a session
must first overturn one of the cited measurements — run `verify_em_thesis.py`.

---

## 0f. Boundary lock — neuro⟷mind separation written down and gated (governance only; no science changed)

This session adds the **neuro⟷mind boundary** as an explicit, mechanically-checked artifact. No
chapter, number, hash, or science is touched; `verify_all.py` stays **5/5** and every frozen hash
still matches. The boundary rules already existed but were **scattered** (VP-SPEC §1.6 lanes, §2
registry derivation relations, the mind `CONVERSION_REPORT` IN/OUT, the `WORK_HANDOVER`, and
`EM_NEAR_FAR_THESIS.md`); they are now consolidated into one source and an enforcing gate.

- **`PROJECT_BOUNDARY_neuro_mind.md`** (package root) — the authoritative two-sided definition.
  Pins: (i) **ownership** IN/OUT — neuro = verified substrate, mind = frontier model on top;
  (ii) the **one-way dependency** — `mind` cites `neuro` with status tags, `neuro` carries only
  forward-defer *pointers* to Mind and never depends on it (protects neuro's citability);
  (iii) **lane / one-file-per-track** — two zips, never merged, no cross-lane files (VP-SPEC §1.6);
  (iv) the **hand-off interface** — the exact named OPEN items that cross to Mind (functional use
  of the at-threshold near-field; the access question; the hard problem; the re-grounded
  parallel-eddy reading), each with its status tag and decisive test; (v) the **one shared object**
  — `EM_NEAR_FAR_THESIS.md`, byte-identical in both, edited only in lockstep.
- **`verify_boundary.py`** (package root) — deterministic neuro-side gate (no RNG; 2× identical),
  **5/5 PASS**, report `reports/lock-neuro-boundary.gate.json`. Checks: (1) **0** neuro→mind code
  imports; (2) **lane purity** (no `docs/mind`, `repro/mind`, `manifest/mind*` in this package);
  (3) `EM_NEAR_FAR_THESIS.md` present at root; (4) `verify_em_thesis.py` still **6/6** (content
  boundary pinned); (5) standalone verification contract intact. It also reports (info, not a
  failure) that **6** HTML files carry forward-defer pointers to Mind — the allowed interface, not
  a dependency. Kept **outside** `run_all.py`, so `verify_all.py` stays **5/5**.
- **Audit result (current packages):** neuro→mind = **0** code imports (forward-defer prose only);
  mind→neuro = citation in prose, **0** code imports — the one-way cite rule holds on both sides,
  and each package verifies from its own single zip with the sibling absent.
- **Housekeeping (C0 — deleting non-source cruft is permitted):** the two shipped `__pycache__/`
  folders (`repro/neuro/_engine/`, `repro/neuro/18-em-brain-circulation/`) were removed. They are
  regenerated automatically on run and should not ship; no `.py`, frozen hash, HTML, or gate is
  affected. `verify_all.py` re-confirmed **5/5** after removal.

**Anti-drift rule (now locked):** to make `neuro` depend on `mind`, merge the two zips, or drop a
cross-lane file into either package is a boundary violation — run `verify_boundary.py`. When the
**Mind** track is next opened, mirror `PROJECT_BOUNDARY_neuro_mind.md` + `EM_NEAR_FAR_THESIS.md`
into the mind package and run the mind-side checklist (`PROJECT_BOUNDARY` §8).

---

## 4. Gate status (v1.9)

`python3 verify_all.py` → **OVERALL: PASS (5/5)**:
- `repro/neuro/run_all.py` — 17 modules deterministic (2× sha256), frozen hashes match, HTML↔code drift 0 (incl. §18 + §19 capstones, 16/16 numbers each).
- slug `16-muscle-force-length` — gate + determinism + fidelity **27/27** + 4 `[O]` declared → PASS.
- slug `17-spinal-cord-locomotor-cpg` — gate + determinism + fidelity **148/148** + ledger (21 items, 0 ungraded) → PASS.
- `tools/gate_neuro_16.py` — **16/16** (every displayed number regenerated, drift 0; plateau-top containment).
- `tools/gate_neuro_17.py` — **39/39** (ledger counts match engine; order derived from data).

Package: `neuro_emergence_chain_integrated_v1_9_4.zip` (point release v1.9.4; repo-relative paths).
The v1.9.4 EM-thesis lock (§0e) adds a deterministic standalone gate
`repro/neuro/09-bounds-open-retired/verify_em_thesis.py` (**6/6 PASS**, both boundaries pinned);
`verify_all.py` stays **5/5** (§9 is prose, outside `run_all`). `verify_all.py` → **OVERALL: PASS (5/5)** from a fresh extract.
`verify_all.py` → **OVERALL: PASS (5/5)** from a fresh extract.

---

## 5. Terminology consolidation (v1.9.5) — the "near-field" overload, fixed at the source

**Why.** One word — "near-field" — was naming **two different physical objects**, and three
different **speeds** were being collapsed into one. That single overload is what made the EM
question feel slippery and brought the same confusion back every session. Fixed once, at the
source, under VP-SPEC C1 (every term maps to a measured/derived object).

**Added — `TERMINOLOGY_canonical.md` (package root): the controlled-vocabulary SSOT.**
- The χ→0 (near-field) regime is **two objects, not one**: **(A) cable conduction = the spike /
  the signal** (guided along the axon, λ_cable ≈ 1.6 mm, advances at the conduction velocity
  0.5–120 m/s = the membrane-charging / reaction-diffusion *front* rate — not light, not the
  field's c, not particle transport) vs **(B) ephaptic near-field = the coupling** (the
  extracellular 1/r³ field (A) sources; c-instant disturbance, slow pattern; measured at threshold
  ΔVm = 0.2748 mV). **(C)** far-field/TIR carrier stays retired.
- The **three speeds**, never to be collapsed: field propagation `c`; signal conduction
  0.5–120 m/s (a front, not transport); rhythm/source rate 1–100 Hz (a rate, not a velocity —
  comparing it to c is a category error).
- What a **spike** physically is (EM in its fields: E ≈ 2×10⁷ V/m across the membrane, EEG=E /
  MEG=B; reaction-diffusion in its travel — no transport term; ions drift only locally, electrons
  carry nothing). **Light emergence** explained (the angle law χ; light reaches the eye, is
  absorbed/down-converted, and from there the **spike**, not light, carries it). A **banned→use**
  table of the exact confusing phrasings and their required replacements.

**Refined — `EM_NEAR_FAR_THESIS.md` §1 table + new §1.1.** The §1 regime table previously listed
"near-field" as one row whose role was "couples neighbours (ephaptic)" — which silently dropped
object (A), the signal. It now splits into (A) cable conduction and (B) ephaptic coupling, with a
new **§1.1 disambiguation** carrying the same A/B split in brief. **All locked claims and every
number are unchanged** — `verify_em_thesis.py` re-confirmed **PASS** (physics untouched; the edit
is terminology only). *This file is the shared byte-identical SSOT with `mind`; the mirror must now
carry the refined version (see §6 mind-mirror note).*

**Scrubbed — two confusing phrasings in chapter bodies** (numbers untouched; gates re-confirmed):
- §15 `15-em-link-full`: "myelin … speeds it **toward c**" → "speeds it up, **though still vastly
  below c**" (fastest nerve is ~10⁶× below light; saltatory never approaches c).
- §18 `18-em-brain-circulation`: "circulates … **at the conduction speed**" → "the field
  disturbance is **at c, while its pattern tracks the slow ionic rate**" (separates the c-fast
  field from the slow pattern rate).

**Added — `verify_terminology.py` (package root): deterministic regression guard.** Pins the canon
present (objects A/B, three-speeds, banned table), the thesis §1.1 disambiguation present, and the
banned phrasings **absent** from every chapter body. **PASS.** Kept **outside** `run_all.py`, so
`verify_all.py` stays **5/5** (mirrors the `verify_boundary.py` pattern).

**Gate status (v1.9.5):** `verify_all.py` **5/5** · `verify_em_thesis.py` **PASS** (both
boundaries) · `verify_boundary.py` **5/5** · `verify_terminology.py` **PASS** — all from a fresh
extract.

**mind-mirror note (updated):** when the **Mind** track is next opened, mirror **three** root files
byte-identical into the mind package — `PROJECT_BOUNDARY_neuro_mind.md`, the **refined**
`EM_NEAR_FAR_THESIS.md` (with §1.1), and the new **`TERMINOLOGY_canonical.md`** — then run the
`PROJECT_BOUNDARY` §8 mind-side checklist. The controlled vocabulary governs `mind` §2/§4 as well.
