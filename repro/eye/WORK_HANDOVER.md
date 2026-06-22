# WORK_HANDOVER — vp_eye_emergence_seed (research SEED, v0.16.0)

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
**E4 is DONE** (v0.6.0) — the goal increment. `research/E4-congenital-blindness/run.py` (in the
verifier's foundation list) + `gate_E4.py` (`E4 GATE: PASS`, 8 checks). It reads E2's single-photon
switch **in reverse**: six congenital-blindness master genes — **GUCY2D, RPE65, CNGB3** (loaded) +
**AIPL1, RPGR, PDE6B** (γ measured from NCBI this version, folded into cache+atlas, 16→19 genes, two
inherited hashes deliberately re-frozen and logged) — each as an R19 transduction **failure mode**.
(A) **LOF = the switch held below its own spinodal**: healthy drive 1.15·h* clears the fold (s>0),
LOF drive 0.85·h* never clears it (s<0); the only difference is crossing h*(γ). (B) the
**substrate-inverse lever, DIRECTION-ONLY**: flip needs drive ≥ h*, so the inverse is (i) raise drive
past h* or (ii) lower threshold below residual drive (shown with a *hypothetical* probe γ′; real γ
untouched) — any quantity/molecule/clinical magnitude is firewall-blocked [O], enforced by a
machine-checked MAGNITUDE FIREWALL (no dose/potency/efficacy/diopter token, no "%"). (C) the six rank
by **spinodal(γ)** as STRUCTURAL fragility (CNGB3 < RPE65 < GUCY2D < RPGR < AIPL1 < PDE6B), **not**
clinical severity; all six γ already distinct at 3 dp, A4 separates the closest pair (GUCY2D/RPGR)
anyway. **Brutal caveat (in the increment):** measured γ is **promoter** context while most blindness
lesions are **coding/downstream** — gene→disease is literature [L] (mechanism, not diagnosis), the
clinical correspondence a named **[O]**. Foundation frozen; no γ added by the increment itself.

**v0.7.0 — the goal was re-scoped and rung 1 was inherited.** The BLUEPRINT goal is now the **complete
high→low down-conversion ladder**: how the ~10¹⁴ Hz visible carrier becomes the ~10–100 Hz neural spike
code, revealed rung by rung. The central claim to prove across the ladder is that the eye down-converts
by **event-detection + low-pass, not by mixing** — colour (angle) and place (image) survive a ~13-order
collapse because they are geometry, not frequency. To stand rung 1 on solid ground, a new frozen
foundation module — `inherited/vp_visible_band_canonical.py` — was brought in from **vp_physics v0.11.0**
(§9.4 D; §10.9 band table; §11 unit-realization + **RCROSS(633/532)**). It reproduces the band placement
(gamma→visible→radio) and the anchor-free two-channel closure m·sinχ·D/λ=1, adds no biology and no
tuning, and is in the verifier's foundation list (runs 2× for determinism). See `INHERITANCE_LEDGER.md`
v0.7.0 entry.

**E6 is DONE** (v0.9.0):
`research/E6-why-visible/run.py` (in the verifier's foundation list) + `gate_E6.py` (`E6 GATE: PASS`,
8 checks). It answers *why* the carrier is the **visible** band with two unrelated constraints selecting
the same window — (i) the inherited §10.9 **geometric placement** (visible sandwiched in m between x-ray
and infrared, near-transverse) [F]; (ii) the **photochemical energy window** (reversible 11-cis→all-trans
isomerisation ~1.8–3.3 eV → exactly 375.71–688.80 nm) [L] — and reaches the **honest** conclusion that
**geometry only PLACES the band while the chromophore energy PINS it**: the angle is a smooth sawtooth
(633 nm has a *smaller* near-grazing deficit than 750 nm) that **never gates a band**, so the edges are
photochemical, not geometric; the deep-red edge is soft (750 nm = 1.6531 eV sits ~0.147 eV below the
1.8 eV floor), and the chromophore tuning is a named **[O]** (no lever from the promoter-γ on the retinal
pocket). **Precision discipline (this rev):** the **wavelength is the anchor**, mapped EXACTLY to ν=c/λ,
period T=1/ν, and E=hν with the **SI-exact** constants (c=299792458 m/s, h=6.62607015e-34 J·s) — no
rounding, no invented round-number edges — anchored on **already-measured** visible wavelengths (the
RCROSS channels 633/532 nm + the cone-opsin λmax 420/530/560 nm, all shown INSIDE the window); angles are
carried to full precision (χ to 10 dp **plus** the meaningful near-grazing deficit 90°−χ, computed without
the 1−sin²χ cancellation) and each satisfies the canonical closure m·sinχ·D/λ=1 to 1e-15. No γ added;
D byte-equal to the inherited invariant; SEED=19.

**E7 is DONE** (v0.10.0): `research/E7-cascade-lowpass/run.py` (in the verifier's foundation list) +
`gate_E7.py` (`E7 GATE: PASS`, 8 checks). It turns E5's qualitative "the carrier is averaged away" into
an **explicit, measured filter**: the FROZEN Neuron's recovery law `w += dt*(s − β·w)/τ_s` (quoted
verbatim) **is** a first-order leaky integrator — a single-pole low-pass H(f)=1/(β+i·2πf·τ_s). The one
claim, **f_c = β/(2πτ_s)** (the band is set by the recovery time-constant), is read off the frozen
substrate four agreeing ways: DC gain = 1/β = 2.000 [F]; measured cutoff = β/(2πτ) to 0.16% [V]; phase
lag at cutoff = 44.99° (one pole ⇒ 45°) [V]; roll-off = −19.96 dB/dec (⇒ −20) [V]. Sweeping τ ⇒
**f_c ∝ 1/τ exactly** (f_c·τ = β/2π = 0.07958 const to 0.27%), and the band is invariant to **both** the
carrier and the promoter-γ — it is **τ, not the carrier and not γ**, that fixes the band. The full FROZEN
neuron inherits this: its emergent rhythm falls monotonically in τ with range(τ) ≫ range(γ), so γ is a
**secondary** mover (via dwell ∝ γ^1.5) at fixed τ. Honest **[O]**: the full-neuron rhythm is only
**approximately** ∝1/τ (a relaxation period = slow τ-recovery + a τ-independent fast transit), plus the
single-pole idealisation vs. the real multi-stage cascade (rhodopsin→transducin→PDE→cGMP→CNG) and the
absolute τ→Hz calibration. No γ added; substrate β=0.5/τ_f=1.0/τ_s=40.0 and γ(GUCY2D)=1.365 byte-equal;
SEED=19. See `INHERITANCE_LEDGER.md` v0.10.0.

**E8 is DONE** (v0.11.0): `research/E8-graded-to-spike-rate/run.py` (in the verifier's foundation list) +
`gate_E8.py` (`E8 GATE: PASS`, 8 checks). The ladder's **last rung** — the retina re-encodes E7's
**graded** ~Hz signal as a discrete ganglion spike **RATE** (rate coding). The re-quantiser is the FROZEN
R19 Neuron itself: the same neuron whose recovery set the band (E7) now **fires**, each spike a membrane
up-crossing = an all-or-none fold-crossing event (inherited `spikes`/`rate_hz`/`dominant_freq`). Measured
on the FROZEN substrate (the operating point is an INPUT, never fitted), the rate code is **thresholded**
(a rheobase FLOOR — silent at g≤0.20 from a hyperpolarised rest, fires at g≥0.30: the switch must clear
its fold), **bounded** (a depolarisation-block CEILING — the full-range f–I is a *bandpass in drive*,
SILENT on BOTH sides, firing only in the operating band), **monotone** (rate ↑ strictly with the graded
amplitude across the band, 0.00783→0.01133), and a near-periodic clock (CV(ISI)≈0.0002 — a genuine
re-quantiser). The central result — **the carrier stays gone (no mixing)** — closes the loop with E5/E7:
fix the slow envelope and sweep the carrier ⇒ rate invariant (spread **1.53%** over a 20× span, rate ⟂
carrier); fix the carrier and raise the envelope ⇒ rate rises (rate ∝ envelope); the train sits in the
neural low band (dominant_freq = rate, orders below the carrier) ⇒ the ~13-order down-conversion is
PRESERVED end-to-end. γ is shown READ-ONLY as a structural excitability OFFSET (it shifts the rheobase via
spinodal(γ), not the band [τ, E7] and not the signal [the drive]); because γ moves the rate ~as much as
the drive here, E8 makes **no** "γ negligible" claim. The **felt percept** of sight is OUT OF SCOPE — it
hands off to the **mind** volume (firewall). No γ added; Neuron β=0.5/τ_f=1.0/τ_s=40.0 and γ(GUCY2D)=1.365
byte-equal; SEED=19. Named **[O]**: absolute Hz/spike-count, the f–I shape, the single-stage collapse of
the retinal network (photoreceptor→bipolar→amacrine→ganglion lateral processing), and the felt percept
(→ mind). See `INHERITANCE_LEDGER.md` v0.11.0. **With E8 the down-conversion spine E0→E8 is complete.**

**THE HTML VOLUME IS BUILT (v0.12.0) — the deliverable now exists.** The ladder E0→E8 has been grown
into a multi-chapter **HTML volume** under `docs/eye/` (a hub + nine chapter pages + nine `facts/*.json`
+ `assets/volume.css` + `sitemap.xml`/`robots.txt`/`llms.txt`), built by `tools/build_volume.py` and
re-proven by `tools/gate_volume.py`. To rebuild and re-verify, read **`BUILD_VOLUME.md`** and run, from
the package root:
```
python3 tools/build_volume.py     # render docs/eye/ FROM each run.py        → BUILD VOLUME: DONE
python3 tools/gate_volume.py      # independent re-proof, HTML↔code drift 0   → VOLUME GATE: PASS
python3 tools/verify_seed.py      # one-command package gate (78 artifacts)   → SEED VERIFY: PASS
```
The contract is met: every displayed number is the **code's own output** — the builder runs each
chapter's `run.py`, embeds its verbatim transcript hash-pinned, and asserts at build time (`F()`) that
every prose number is a substring of that live transcript; the gate re-proves it with seven checks (G1
determinism, G2 code→facts sha, **G3 page→code byte-identity = drift 0**, G4 fact-in-transcript-and-HTML,
G5 the magnitude firewall on the rendered disease chapters (E4 + E9 as of v0.13.0), G6 static JSON-LD-only machine-readability, G7
no-omission) and was checked to be **non-vacuous**. **No `run.py` was edited** — the volume is a pure
publication layer (no physics, no γ, no tuning). The numbers are **not** hand-transcribed; if a number
must change, edit the responsible `run.py` and rebuild (there is no second place to update).

**Out of this package's lane (do NOT add here):** the official live-site merge — canonical `paper_id`,
`301` redirects from old URLs, and the cross-volume DOI registry entry — is a separate VP-SPEC **Phase 5**
step done against the live site. It cannot be verified offline, so it stays out of the seed.

**E9 is DONE (v0.13.0) — the first mechanism extension beyond the spine.**
`research/E9-red-green-dichromacy/run.py` (in the verifier's foundation list) + `gate_E9.py` (`E9 GATE:
PASS`, 8 checks), rendered as `docs/eye/e9-red-green-dichromacy/index.html` (+ its `facts/*.json`) and
re-proven by `gate_volume.py`. It carries the carrier no further down — it reads what the FROZEN **E1**
angle map already FORCES about colour, and *why* the commonest inherited colour-vision difference is
**red-green**. Colour is propagation angle χ(λ), so three cones are three angle-samples and the three
discrimination axes are the three pairwise angle **margins** (byte-equal off the frozen `chi_deg` at the
measured λmax): S-M = 0.0509°, **M-L (green-red) = 0.0421° — the SMALLEST** (1.208× tighter than S-M), S-L
= 0.0931°. Headline [F]↔[L]: **the angle map makes green-red the structurally most fragile colour axis,
matching the epidemiology** — no fit, no new γ. FORCED: (1) **coincidence ⇒ collapse** — equal λmax ⇒ equal
angle ⇒ margin **exactly 0.000000°**; sliding a hypothetical L′ toward λ(M) drives the margin monotonically
to 0 (sawtooth-proof), unifying **dichromacy** (drop one sample ⇒ the within-red-green axis vanishes, one
chromatic axis survives) and **anomalous trichromacy** (peaks converge) as ONE continuum. (2) a
**direction-only** lever (peaks together ⇒ margin shrinks; magnitude named **[O]**, firewalled). (3)
**orthogonality** — colour (angle, E1) ⟂ position (image, E3) ⟂ brightness (switch, E2); the surviving
cones' R19 switch is spinodal-stable, so losing one cone costs **exactly one colour axis** while acuity and
single-photon detection stay intact (*why* it is colour-blindness, not blindness). (4) **γ READ-ONLY**
(OPN1LW γ=1.4820, OPN1MW γ=1.4058, Δγ=0.0762, A4 shapes 1.40× apart), **no** claim γ predicts λmax; the
X-linked OPN1LW/OPN1MW tandem array is [L] genomics. This is the package's **second firewalled clinical
chapter** (after E4): direction-only, proposal-only; `run.py` carries its own `MAGNITUDE_BLOCK` and asserts
the transcript holds none of those tokens. No γ added; cone angles byte-equal from the frozen map; λmax
already-measured; SEED=19. Felt percept OUT OF SCOPE (→ mind). **The foundation does not move:** E9 fetched
nothing and re-froze nothing — `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0 (see
`INHERITANCE_LEDGER.md` v0.13.0).

**E10 is DONE (v0.14.0) — the second mechanism extension beyond the spine; a NORMAL (non-clinical) chapter.**
`research/E10-light-dark-adaptation/run.py` (in the verifier's foundation list) + `gate_E10.py` (`E10 GATE:
PASS`, 8 checks), rendered as `docs/eye/e10-light-dark-adaptation/index.html` (+ its `facts/*.json`) and
re-proven by `gate_volume.py`. Unlike E9 it is **not** a disease chapter — like E5–E8 it carries **no**
`MAGNITUDE_BLOCK` and no firewall. It asks what the FROZEN R19 switch already FORCES about how the eye spans
~10 decades of background light with a bounded response. The mechanism is **the switch's own saturating ON
branch**: E2's field `γ·s − s³ + h = 0`, on its ON branch, is the real root of `s³ − γ·s − h = 0`, and for
large background drive h the cubic dominates ⇒ the steady state **s*(h) → h^(1/3)** (compressive cube root),
read off the FROZEN substrate four ways. (A) **Dynamic-range compression** — a **5.000000-decade** sweep
(1→10⁵) fits a **1.500207-decade** response (compression **3.332873**); the deep sweep gives the cubic order
**n=3** (every s* a true zero, max residual 2.3e-13). (B) **Automatic gain control** — incremental gain
`1/(3s*²−γ)` falls **1296.0×** dim→bright (∝ h^(−2/3)), **no separate machinery**. (C) **headline Weber-law**
— contrast gain `(h/s*)·ds*/dh` pinned by the pure-cube limit **EXACTLY at 1/n = 1/3 = 0.333333** for any h,
**γ-INDEPENDENT** (RHO γ=1.4719 → 0.333301, CNGB3 γ=1.2425 → 0.333306 at h=10⁶) — equal fractional steps feel
equal regardless of the gene; honest scope: this is the saturated tail, near the fold the response is
steeper than a clean power law. (D) **two regimes** — DARK (near fold h*=0.68733, highest gain + E2's
single-photon flip) vs BRIGHT (deep cube root, low gain); adaptation = the operating point **sliding**
fold→cube-root. **γ READ-ONLY** (fold/offset; the law is γ-independent — an OFFSET, as in E7/E8); dark
re-sensitisation **recovery τ_s=40.0** is the same FROZEN time-constant as E7/E8 — structure [F], absolute
seconds **[O]**. No γ added; substrate/Neuron byte-equal; SEED=19. Felt brightness percept OUT OF SCOPE
(→ mind). **The foundation does not move:** E10 fetched nothing and re-froze nothing —
`inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0 and v0.13.0 (see `INHERITANCE_LEDGER.md` v0.14.0).

**E11 is DONE (v0.15.0) — the third mechanism extension beyond the spine; a CLINICAL (firewalled) chapter
extending E3's optics.** `research/E11-accommodation-refraction/run.py` (in the verifier's foundation list) +
`gate_E11.py` (`E11 GATE: PASS`, 8 checks), rendered as `docs/eye/e11-accommodation-refraction/index.html`
(+ its `facts/*.json`) and re-proven by `gate_volume.py`. Like E9 (and unlike the normal E5–E8/E10) it **is**
a disease/condition chapter — it is in `DISEASE_CHAPTERS`, so the `gate_volume.py` **G5 firewall** covers its
rendered HTML. It asks what E3's FROZEN single-surface eye already FORCES about focus. E3 images a distant
object at `v_∞ = n₂/P` with `P = (n₂−n₁)/R`; the image lands on the retina ⇔ `v_∞ = L` ⇔ **P·L = n₂**, so the
whole story turns on the dimensionless **match ratio ρ ≡ P·L/n₂** read off the frozen optics four ways.
(A) **Emmetropia is ρ = 1** — the frozen Emsley reduced eye sits **exactly** there (**ρ = 1.000000**); focus is
a *whole curve* in the power×length plane, not a point. (B) **Refractive error is the signed mismatch**
`sign(ρ−1)`: **ρ = 1.050000 > 1** puts the distant focus *in front* of the retina ⇒ **MYOPIA**;
**ρ = 0.950000 < 1** *behind* ⇒ **HYPEROPIA** — and each is reachable **two ways**, an eye too long OR too
powerful, because **only the product P·L matters** (a too-strong eye `q·ℓ = 1` shortened to compensate returns
**ρ = 1.000000**); stated **direction-only**, the dioptric magnitude a named **[O]**. (C) **Accommodation is a
one-signed power lever** — a near object at `u = −k·L` needs `P_req/P_∞ = 1 + n₁/(n₂·k)`, which rises
**monotonically** as the object nears (**1.000750 → 1.007500 → 1.030000 → 1.075000 → 1.187500 → 1.375000**) and
is **always ≥ 1**; the eye supplies it by **rounding the lens** (R↓ ⇒ P↑, `R_req/R_∞` nearest **0.727273**
focuses back on the retina); amplitude and absolute near-distances **[O]**. (D) **The lever is lattice
geometry**: power rides curvature `dP/P = −dR/R` (P ∝ 1/R, the same √(B/ρ) refractive-index rule as E3), while
the *length* axis is the substrate **dwell-size law size ∝ γ^1.5** (E1) — PAX6 read-only (PAX6/RAX dwell ratio
**1.059595**) instantiates the *direction* (more eye-field growth ⇒ longer eye ⇒ myopic shift), the gene→axial-
elongation map itself an **[O]**. **Firewall:** E11's `MAGNITUDE_BLOCK` mirrors E9's list and **adds**
`diopter`/`dioptre` and bare `mm`, so every fact is a **dimensionless ratio or a sign** — `gate_E11.py` G8 and
`gate_volume.py` G5 both confirm no magnitude token and no "%". No γ added; substrate/Neuron byte-equal;
SEED=19. Felt blur/clarity percept OUT OF SCOPE (→ mind). **The foundation does not move:** E11 fetched
nothing and re-froze nothing — `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0, v0.13.0 and
v0.14.0 (see `INHERITANCE_LEDGER.md` v0.15.0).

**E12 is DONE (v0.16.0) — the fourth mechanism extension beyond the spine; a CLINICAL (firewalled) chapter,
the hardest one: acquired/degenerative disease.** `research/E12-acquired-degeneration/run.py` (in the
verifier's foundation list, sha256 `aebf37d4882325dd…`) + `gate_E12.py` (`E12 GATE: PASS`, 8 checks), rendered
as `docs/eye/e12-acquired-degeneration/index.html` (+ its `facts/*.json`) and re-proven by `gate_volume.py`.
It **is** a disease/condition chapter — in `DISEASE_CHAPTERS`, so the `gate_volume.py` **G5 firewall** covers
its rendered HTML. The honest physics is distinct from E4 and is a **saddle-node collapse with hysteresis** on
the **frozen** R19 field `ds/dt = γ·s − s³ + h`. E4 read a switch *born below* its fold (static, **never
flips**); E12 reads the opposite history — a switch that **started healthy** (settles ON, s>0) and is carried
*over* its own fold by accumulating stress, in **four** parts. (A) **Degeneration = a slow drift over the
fold**: on RHO (read-only, γ **1.4719**, fold h\* **0.687330**) the healthy state (**s = 1.316420**) tracks
the upper branch down and **collapses in one step** at **h = -0.691855 ≈ −h\* = -0.687330** — a *tipping
point*, start-independent (a different start collapses at **-0.689701**), E4's spinodal reached *dynamically
from the ON side*. (B) **Hysteresis**: recovery comes only at the *opposite* fold **+h\* = 0.687330** (drive
**0.691855**), loop width **1.383710 ≈ 2·h\* = 1.374661** = the irreversibility margin — recovery needs
**over-correction past +h\***, the substrate's account of why **early ≠ late**. (C) **One geometry, many
routes**: a **LOAD route** (lower h to −h\*) and a **BASIN-SHALLOWING route** (erode γ under fixed load
**-0.300000** until the shrinking fold **h\*(γ) = 0.296976** meets it at **γ = 0.841231**, analytic γ_crit
**0.846932**) **both land on the one locus h = −h\*(γ)** (gap **0.003024**) — so the shared *late* picture
across AMD/glaucoma/diabetic retinopathy is **forced** while each primary stress's identity is a named **[O]**.
(D) **γ as STRUCTURAL fragility**: lower γ ⇒ shallower basin ⇒ tips under less stress (spinodal-monotone CNGB3
h\* **0.533080** → PDE6B h\* **0.732285**, span **1.373687**), READ-ONLY/byte-equal, with the **loudest caveat
in the volume** — the disease-gene→γ map is *even more* **[O]** than E4 (polygenic, age/environment-gated,
mostly non-promoter common variants: promoter-γ has essentially **no monogenic purchase** here). **Firewall:**
E12's `MAGNITUDE_BLOCK` mirrors E9's and **adds** `hba1c`/`mg/dl`/`mmol/l`/`mmol/dl` and bare `mm`/`mmhg`
guards, so every stress is a **dimensionless multiple of the gene's own fold** — `gate_E12.py` G8 and
`gate_volume.py` G5 both confirm no magnitude token and no "%". No γ added; substrate byte-equal; SEED=19.
Felt **loss** of sight OUT OF SCOPE (→ mind). **The foundation does not move:** E12 fetched nothing and
re-froze nothing — `inherited/FROZEN_SHA256.json` is byte-identical to v0.12.0 through v0.15.0 (see
`INHERITANCE_LEDGER.md` v0.16.0).

**What to build next.** The down-conversion spine (E0→E8) is published and **all four mechanism extensions are
now built** — red-green dichromacy (**E9**), light/dark adaptation (**E10**), accommodation + refractive error
(**E11**), and the acquired/degenerative disease layer (**E12**, the hardest, now done). The eye volume's
planned arc is therefore **complete**; what remains are small, optional items, not a missing pillar. Still
deferred: **SIX6** (eye-field TF), the one remaining gene in the atlas `_to_measure` — adding it would extend
the fragility/eye-field readings but changes no result. Absolute Hz at every rung stays **[O]**, and every
**felt** percept (colour, brightness, blur, the *loss* of sight) is deferred one-way to the **mind** volume.
Any new chapter is added to `VOLUME` in `tools/_volume_lib.py`, given a `body_*()` in `build_volume.py` with
every number wrapped in `F()`, registered in `BODIES`, and re-gated (and, if it is a clinical chapter, added to
`DISEASE_CHAPTERS` so the G5 firewall covers it) — the discipline carries over unchanged.

## Sibling
This is one of a split pair. The other sense ships as its **own** seed zip
(`vp_ear_emergence_seed…`). Keep them
apart — two files, two lanes. They share only the organising insight (wave → spatial code → R19
switch) and the √(B/ρ) wave rule, not code.
