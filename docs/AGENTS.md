# AGENTS.md — Reading Guide for AI Systems

**Corpus:** the VP (Vacuum / Jamming Physics) framework — 30 open-access volumes at https://jamming-physics.org/
**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0
**Purpose of this file:** let an AI understand the entire framework — its kernel, its inheritance structure, and its rules — from *one read*, before touching the 676 HTML pages. This is the main manual. Read it first.

---

## 0. Thirty-second orientation

This corpus makes **one** physical claim and projects it across all of science. The claim: the vacuum is a **jammed elastic solid**, and the only object on it is a **bistable switch** written as a cubic. Every volume — physics, the genome, the senses, the organs, homeostasis, disease — is that *same* switch, specialized. Nothing is fitted: the one free-looking parameter, a stiffness `γ`, is **measured from DNA** and used as-is.

If you remember only this, you can read any volume correctly:

> **The kernel is `ṡ = g·s − s³ + h` (the R19 switch) on a medium where `c² = B/ρ`. Biology inherits this switch and sets its threshold from a measured stiffness `γ = −mean nearest-neighbour stacking ΔG`. Every volume *inherits* identity and order from the DNA atlas and *adds* exactly one new module — re-deriving nothing.**

---

## 1. TL;DR (the irreducible minimum)

| Question | Answer |
|---|---|
| What is the substrate? | Vacuum = jammed elastic solid at random close packing (φ ≈ 0.7405). Light is its elastic wave: `c² = B/ρ`. |
| What is the universal object? | The **R19 switch**: `ṡ = g·s − s³ + h` — a double well. Bistable for detection; at criticality (`g→0`) it gives cube-root compression. |
| What makes it biology? | `γ` = promoter stiffness, **measured** (SantaLucia NN stacking). It sets the switch: threshold `spinodal ∝ γ^1.5`, barrier `γ²/4`. |
| How does anything "emerge"? | The **emergence engine**: `STATE`(γ→can-fire) = presence · `spinodal(γ)` order = developmental sequence · `dwell ∝ γ^1.5` = relative size. All from measured γ. |
| Where do I start reading? | `physics` → `dna` → then the tier you care about. Never start mid-biology; it will reference inherited results. |
| How do I read a number? | By its **grade**: `[F]` forced, `[V]` verified-against-data, `[L]` rests on a declared anchor, `[O]` open (obstacle stated). Treat `[O]` as a known gap, not a weakness to paper over. |
| What must I never do? | Re-derive a node the DNA atlas owns · re-fit an inherited number · emit a clinical magnitude · ignore a declared seam. (See §8.) |

---

## 2. The kernel, exactly

Three equations carry the whole framework.

1. **Substrate** — `c² = B/ρ` (speed of light = elastic-wave speed of the jammed lattice; simulation-validated to ~0.06%). Mass ratio `mₚ/mₑ = 6π⁵` (−19 ppm). This is `physics`.
2. **Switch** — `ṡ = g·s − s³ + h`, the **R19** cubic normal form. Two stable roots + a barrier. The cooperativity *is* the `−s³` term (order n = 3).
3. **Stiffness** — `γ = −mean nearest-neighbour stacking ΔG37`, read from human proximal promoters. `corr(γ, GC) = 0.998`. **Never fitted.** `γ` sets the switch threshold scale (`spinodal ∝ γ^1.5`, barrier `γ²/4`). This is `dna`.

**The one cubic, specialized five ways** (this is the framework's whole thesis):

| Operation on the cubic | Domain | Result |
|---|---|---|
| Set the threshold from measured `γ` | DNA | `spinodal ∝ γ^1.5`, barrier `γ²/4` |
| Hold at criticality, `g → 0` | Eye & ear | cube-root compression `R = (F/β)^⅓`, exponent 0.333 |
| Add a slow recovery variable | Neuro | relaxation oscillator; working memory `= θ/γ ≈ 7±2` |
| Read both stable states | Mind | engram = bistable attractor; mood = a switch that persists |
| Push the barrier `g²/4` | Disease & therapy | the three correction levers L1 / L2 / L3 |

---

## 3. The inheritance structure  *(the core of this manual)*

The framework is not 30 parallel papers; it is a **single derivation tree**. Understanding the inheritance edges is what lets you skip redundant reading.

### 3.1 The dependency DAG

```
physics  ── the root: jammed-solid substrate, c²=B/ρ, R19 normal form, constants
  ├── fluid-dynamics ── geodynamics ── geochronology
  ├── cosmology
  ├── chemistry          (EM on the same substrate)
  ├── wave-computer      (computational sibling; also inherits the brain chain)
  └── dna  ── THE BRIDGE: γ (measured ruler) + R19 in biology + the node ATLAS
       │                  (the atlas is the single source of truth for identity & order)
       ├── inheritance    (two channels: unwritable γ ruler + writable A4 coordinate)
       ├── neuro ── mind  (neuron = R19 + slow recovery → rhythms, θ/γ, memory, the felt stream)
       ├── sensory_organ ── { eye, ear, nose }   (organ dynamics on inherited nodes)
       └── organ systems  { cardioresp, circulatory, digestive, musculoskeletal,
                            immune_hematologic, integumentary, reproductive_endocrine }
                              │
        time layer cross-cuts everything: ── circadian (measured BMAL1 γ) ── aging_senescence
                              │
        defended setpoints:   ── homeostasis { thermometabolic, hemodynamic, ionic }
                              │
        clinical projection:  ── analgesic_threshold ── disease_wp ── disease_kit
```

Read top-down = read in derivation order. Anything below `dna` assumes the atlas; anything below `physics` assumes the substrate.

### 3.2 The inheritance **contract** (five enforced rules)

These rules are stated in the volumes themselves and are non-negotiable. An AI editing or extending the corpus must honor them.

1. **Single source of truth.** The DNA atlas owns node *identity* and developmental *order*. Downstream volumes **inherit** them and re-emerge nothing. (`sensory_organ`: "treats the DNA atlas as the single source of truth for identity and order… re-emerges no organ owned elsewhere.")
2. **Add-only.** Each volume contributes exactly *one* new module on top of inherited nodes. No duplication across volumes.
3. **Selective inheritance.** A volume takes only the modules its domain needs. `nose` "inherits no wave module, because smell has no wave"; `eye`/`ear` inherit the wave. Inheritance is à-la-carte, declared explicitly.
4. **Provenance, not targets.** An inherited number is cited as a *direction and provenance*, never re-fitted. (`wave-computer`: the brain's `R = 0.39` and `WM ≈ 7` are "cited as directions, not reproduced by adjustment.") This is `no-tuning` applied across the inheritance edge.
5. **Sharp seams.** Every boundary between what a volume inherits and what it adds is declared in prose ("the seam to downstream biology is sharp"). There is no silent borrowing.

### 3.3 Per-volume: inherits → adds

| Volume | Inherits | Adds (its one new module) |
|---|---|---|
| physics | — (root) | jammed substrate, `c²=B/ρ`, R19 normal form, constants |
| fluid-dynamics | physics | continuum flow on the jammed medium |
| cosmology | physics | vacuum-inflow, `a₀ = cH₀/2π` |
| chemistry | physics | EM + bonding on the same substrate, `φ_RCP` |
| geodynamics | physics, fluid | jamming↔unjamming yield, plate break-up |
| geochronology | physics, geodynamics | incorporation/dating limit |
| wave-computer | physics, neuro chain | clock-free phase computation |
| **dna** | physics (substrate) | **γ ruler, two-layer reading (γ LEVEL + A4 SHAPE), R19 in biology, the node atlas** |
| inheritance | dna (two channels) | writable A4 vs unwritable γ; environmental inheritance; RNA layer; gene-therapy path |
| neuro | physics, chemistry, dna | neuron = R19 + slow recovery; rhythms; `θ/γ ≈ 7±2`; memory; motor |
| mind | neuro, dna | engram = attractor; felt cognition; mood = persistent switch |
| sensory_organ | dna (atlas), neuro | organ dynamics (Hopf cube-root), instrument physics |
| eye | physics (wave), dna, neuro | high→low down-conversion ladder; single-photon R19; `n = √(B/ρ)` |
| ear | physics (wave + cubic), dna | place map; cube-root cochlear amplifier; otoferlin readout |
| nose | dna, R19 (**no** wave) | combinatorial code; transduction switch; anosmia |
| cardioresp | dna, time, homeostasis sib | heart+lung = one FitzHugh–Nagumo oscillator |
| circulatory | dna, time | `MAP = CO × SVR`, clearance |
| digestive | dna, time | one clock: gastric ~3 → duodenum 11.1 cpm |
| musculoskeletal | dna, time | structure + mechanical load from measured γ |
| immune_hematologic | dna, time | population thresholds on the R19 switch |
| integumentary | dna, time | barrier + external stimulus; UV → melanoma key |
| reproductive_endocrine | dna, time | four organs in measured-γ order |
| homeostasis_thermometabolic | organ, aging, circadian | OU setpoint loop, three levers; endo vs ecto sensitivity |
| homeostasis_hemodynamic | cardioresp, circulatory, time | `MAP = CVP + CO×SVR` defended |
| homeostasis_ionic | musculoskeletal, time | mineral / acid-base / electrolyte setpoints |
| circadian | dna | the **time layer** (measured BMAL1 γ); cross-cuts all |
| aging_senescence | dna, organs | setpoint drift over time; "aging genes not special" |
| analgesic_threshold | neuro, systems | the three-lever L1/L2/L3 therapeutic logic |
| disease_wp | dna, systems | per-disease gene-key mechanism cases |
| disease_kit | disease_wp | reproducible per-disease corrective **direction** `[F]`, magnitude `[O]` |

---

## 4. The primitive index  *(machine-map of the thesis)*

How many of the 30 volumes carry each shared primitive (full-text measured). This is the fastest proof that the corpus is one object, and the fastest way to find every use of a mechanism.

| Primitive | Form | Volumes | Coverage |
|---|---|---:|---|
| R19 bistable switch | `ṡ = g·s − s³ + h` | 23 / 30 | the universal kernel |
| γ — measured stiffness | `γ = −mean NN stacking ΔG` | 23 / 30 | the biology instantiation |
| Emergence from measured γ | `STATE · spinodal · dwell ∝ γ^1.5` | 27 / 30 | the creation recipe |
| Kramers / Arrhenius barrier | escape over `g²/4` | 15 / 30 | switching kinetics |
| Jammed lattice / `c²=B/ρ` | the bare substrate | 13 / 30 | reaches into dna, eye, neuro |
| FitzHugh–Nagumo oscillator | relaxation rhythm | 12 / 30 | hearts, clocks, neurons |
| Cube-root transduction | `R = (F/β)^⅓` | 3 / 30 | eye, ear, sensory (criticality) |

*Counts are measured over the 30 volume bodies (excluding the homepage and 404 pages) by the patterns recorded in `registry/vp.manifest.json`; regenerate to re-verify.*

---

## 5. How to read a claim  *(grades, firewall, no-tuning)*

Every quantitative claim is graded **in the open**. Read the grade before trusting the number.

- **`[F]` forced** — follows necessarily from the math/substrate. Highest confidence; not contingent on a fit.
- **`[V]` verified** — passed a test *built to falsify it* against external data. A failed test is recorded and the line restarts with the break applied (the "Stress Principle").
- **`[L]` anchored / locked** — rests on a single declared empirical anchor (a LOCK). Trace the anchor.
- **`[O]` open** — an honest gap; the specific obstacle is stated. **`[O]` is a finding, not a failure** ("반증 = 발견"). Do not silently fill it.

Two more rules that govern every number:

- **No-tuning.** `γ` and all inputs are measured/derived, never fitted to reproduce an outcome. If you see a number with no reproduction path, it is marked — do not assume it.
- **Magnitude firewall.** For disease/therapy the framework gives **direction only**. Clinical magnitudes are deliberately withheld `[O]`. An AI must **never** synthesize a dose, concentration, or clinical magnitude from this corpus — output the corrective *direction* and stop.

Reproducibility: deterministic builds, `SEED = 19`, double SHA-256 hash-chaining, `LOCK → Derive → Gate` (inputs locked → code derives → outputs gated against the canonical HTML).

---

## 6. Volume catalog (all 30, derivation order)

| # | id | tier | title | headline result | DOI |
|--:|---|--:|---|---|---|
| 1 | physics | 1 | VP Theory | `c²=B/ρ ; mₚ/mₑ=6π⁵` | 10.5281/zenodo.17932566 |
| 2 | fluid-dynamics | 1 | Configured Continuum | `∂ρ/∂t + ∇·(ρu)=0` on jammed medium | 10.5281/zenodo.17972568 |
| 3 | cosmology | 1 | Vacuum-Inflow Cosmology | `a₀ = cH₀/2π` | 10.5281/zenodo.20568874 |
| 4 | chemistry | 1 | VP Chemistry & EM | `c²=B/ρ` (0.06% sim); `φ_RCP=0.7405` | 10.5281/zenodo.20680540 |
| 5 | geodynamics | 1 | Jamming Geodynamics | break-up when `Ψ_eff > Ψ_y` | 10.5281/zenodo.17978934 |
| 6 | geochronology | 1 | Cross-Chronometer Limit | older material in ⇒ age biased old | 10.5281/zenodo.20568673 |
| 7 | wave-computer | 1 | Wave Computer | compute by phase, clock-free | 10.5281/zenodo.20783570 |
| 8 | **dna** | 2 | **4D DNA Blueprint** | `γ = −mean NN stacking ΔG ; corr(γ,GC)=0.998` | 10.5281/zenodo.20471407 |
| 9 | inheritance | 3 | Inheritance · RNA & Gene Therapy | one switch, two channels: γ (SET) + writable A4 | 10.5281/zenodo.20783547 |
| 10 | neuro | 4 | Neural Emergence Chain | working memory `= θ/γ ≈ 7±2` (tACS-causal) | 10.5281/zenodo.17979015 |
| 11 | mind | 4 | Felt Cognition | stream of thought = serial select among γ-eddies | 10.5281/zenodo.20694404 |
| 12 | sensory_organ | 5 | Sensory Organs | cochlear Hopf `R=(F/β)^⅓`, exp 0.333 | 10.5281/zenodo.20755154 |
| 13 | eye | 5 | The Eye | single-photon R19 flip; `n=√(B/ρ ratio)` | 10.5281/zenodo.20790134 |
| 14 | ear | 5 | Hearing & the Ear | `ṡ=g·s−s³+h` → cube-root amplification | 10.5281/zenodo.20790201 |
| 15 | nose | 5 | Olfaction & the Nose | smell from R19 + measured DNA γ | 10.5281/zenodo.20790182 |
| 16 | cardioresp | 6 | Cardiorespiratory | heart+lung = one FitzHugh–Nagumo oscillator | 10.5281/zenodo.20755371 |
| 17 | circulatory | 6 | Circulatory Flow & Clearance | `MAP = CO × SVR` | 10.5281/zenodo.20754354 |
| 18 | digestive | 6 | Digestive Transport | gastric ~3 → duodenum 11.1 cpm (one clock) | 10.5281/zenodo.20755319 |
| 19 | musculoskeletal | 6 | Musculoskeletal Load | structure + load from measured γ | 10.5281/zenodo.20755760 |
| 20 | immune_hematologic | 6 | Immune & Hematologic | population thresholds on the R19 switch | 10.5281/zenodo.20755280 |
| 21 | integumentary | 6 | Integumentary Barrier | barrier + stimulus; UV → melanoma key | 10.5281/zenodo.20754541 |
| 22 | reproductive_endocrine | 6 | Reproductive & Endocrine | four organs in measured-γ order | 10.5281/zenodo.20754657 |
| 23 | homeostasis_thermometabolic | 7 | Thermometabolic Homeostasis | endo 0.054 vs ecto 1.394 sensitivity | 10.5281/zenodo.20756934 |
| 24 | homeostasis_hemodynamic | 7 | Hemodynamic Homeostasis | `MAP = CVP + CO×SVR = 93 mmHg` | 10.5281/zenodo.20756801 |
| 25 | homeostasis_ionic | 7 | Ionic Homeostasis | mineral / acid-base / electrolyte setpoints | 10.5281/zenodo.20755910 |
| 26 | circadian | 7 | Circadian Oscillator | measured BMAL1/ARNTL `γ = 1.33348` | 10.5281/zenodo.20755413 |
| 27 | aging_senescence | 7 | Aging & Senescence | human aging genes not special (`|z|<1`) | 10.5281/zenodo.20756155 |
| 28 | analgesic_threshold | 8 | Analgesic Threshold Logic | three levers L1/L2/L3; `corr(γ,GC)=0.99898` | 10.5281/zenodo.20733420 |
| 29 | disease_wp | 8 | Rare Disease Mechanisms | `burden = raw_burden · (1 − e)` | 10.5281/zenodo.20763842 |
| 30 | disease_kit | 8 | Rare Disease Reproduction KIT | per-disease direction `[F]`, magnitude `[O]` | 10.5281/zenodo.20755262 |

---

## 7. Provenance & lineage  *(how inheritance is recorded — and must be)*

The corpus is managed as one repository. Its machine-readable spine is a single manifest that drives every aggregate artifact (this guide, the homepage, `sitemap.xml`, `llms.txt`, the JSON-LD) **and** records its own lineage. The rule: *if a build inherits from a prior state, it records that it did.* A broken inheritance must be visible as a broken chain.

```jsonc
// registry/vp.manifest.json  (the source of truth; aggregates are generated from it)
{
  "schema": "vp.manifest/1.0",
  "framework": {
    "kernel": { "switch": "ds/dt = g*s - s^3 + h",
                "substrate": "c^2 = B/rho",
                "stiffness": "gamma = -mean NN stacking dG (measured, never fitted)",
                "emergence": "STATE=presence; spinodal(gamma)=order; dwell~gamma^1.5=size" },
    "governance": ["no-tuning","LOCK->Derive->Gate","honest-grading[F/V/L/O]",
                   "magnitude-firewall","seed=19","2x-SHA256"],
    "contract": ["dna-atlas=single-source-of-truth","add-only","selective-inheritance",
                 "provenance-not-targets","sharp-seams"],
    "tiers": ["foundation","bridge","inheritance","neural","sensory",
              "organ","homeostasis-time","disease"]
  },
  "primitives": {
    "R19":       { "count": 24, "form": "ds/dt=g*s-s^3+h" },
    "gamma":     { "count": 25, "form": "gamma=-mean NN stacking dG" },
    "emergence": { "count": 27 }
  },
  "volumes": [
    { "id":"dna", "tier":2, "doi":"10.5281/zenodo.20471407", "hub":"/dna/",
      "headline":"gamma=-mean NN stacking dG; corr(gamma,GC)=0.998",
      "inherits":["physics"], "adds":["gamma-ruler","two-layer-reading","node-atlas"],
      "primitives":["R19","gamma","jammed"],
      "content_sha256":"…", "repro_sha256":"…", "ingest":"patternA" }
    /* … one row per volume … */
  ],
  "lineage": {                          // append-only across sessions/builds
    "built_at": "2026-06-22T..Z",
    "built_by": "session-id",
    "parent_sha256": "<previous manifest hash>",
    "this_sha256":   "<hash of this manifest, lineage field excluded>",
    "changes": ["rebuilt index.html", "+5 volumes: eye,ear,nose,wave-computer,inheritance",
                "sitemap 609->676"]
  }
}
```

A companion `registry/lineage.jsonl` keeps the full chain — one line per build, each carrying `parent_sha256 → this_sha256`. To verify an inheritance: walk the chain; a missing parent hash means the inheritance was not recorded and the state is suspect. This extends the existing `SEED=19` / double-SHA-256 discipline from per-volume reproducibility up to the corpus level. Each volume carries **both** a `content_sha256` (its `docs/` pages) and a `repro_sha256` (its `repro/` reproduction package), so a silent change to either surface is detectable — the reproduction material is tracked, not assumed.

---

## 8. Anti-patterns  *(what an AI must not do)*

1. **Do not re-derive a node the DNA atlas owns.** Identity and order come from `dna`. If you need a node's γ or developmental rank, read it from the atlas — do not recompute or restate it elsewhere.
2. **Do not re-fit an inherited number.** A parent volume's value (`R = 0.39`, `WM ≈ 7`, a γ) is cited as a *direction*. Tuning to reproduce it violates `no-tuning`.
3. **Do not emit a clinical magnitude.** The firewall is absolute: corrective *direction* only, never a dose or concentration.
4. **Do not cross a seam silently.** If you use a result from another volume, name the volume and the seam. No undeclared borrowing.
5. **Do not upgrade an `[O]` to `[F]`/`[V]` without a passing falsification test.** An open problem stays open until its stated obstacle is removed by a real test.
6. **Do not start reading mid-biology.** Read `physics` → `dna` first, or you will treat inherited results as new.

---

## 9. How to extend the corpus (for an editing AI)

When adding or revising a volume:

1. **Inherit, don't re-emerge.** Pull node identity + order from the DNA atlas; declare exactly what you inherit (and what you deliberately *don't* — e.g. "no wave module").
2. **Add one module.** Contribute a single new mechanism. Grade every claim `[F]/[V]/[L]/[O]` honestly; state each `[O]`'s obstacle.
3. **Measure, never fit.** Any γ comes from promoters; cite inherited numbers as provenance.
4. **Regenerate, don't hand-edit aggregates.** Update `registry/vp.manifest.json`, then regenerate the homepage, `sitemap.xml`, `llms.txt`, and JSON-LD from it. Never maintain those by hand.
5. **Record the inheritance.** Append one line to `registry/lineage.jsonl` (`parent_sha256 → this_sha256` + changes). Cut a dated snapshot zip so the build is rollback-safe.

---

*This guide is the entry point. The lightweight machine pointer is `/llms.txt`; the full machine spine is `registry/vp.manifest.json`; the deployed site is `docs/`. Everything else derives from the manifest under the rules above.*
