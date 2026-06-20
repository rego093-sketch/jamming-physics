# RESEARCH PROGRAM — 4D-DNA brain emergence → 100 % of measured brainwave phenomena

**Package:** `mind_vp_site_UPGRADED` **v1.15** · **Governance:** `VP_SPEC_v1_8.md` (C0–C4)
**Author program:** VP / Jamming-Physics (Young Jae Lee).

> **Mission.** Build the brain from **4D-DNA emergence** (organs from measured master-gene γ),
> emit a **real, propagating brainwave** whose properties equal **measured literature values**,
> drive that brainwave into the **hypothalamus** and study the closed circulatory/arousal loop,
> and let **4D-emerged memory cells respond** — then drive the catalogue of **measured brainwave
> observables (phenomena, NOT interpretations) to 100 % concordance**, across health and a broad
> set of diseases. Reproducing a phenomenon is never a claim about its interpretation;
> `medium_efficacy_tested` stays 0; the hard problem stays open; no claim of experience is made.

---

## 0. The discipline (non-negotiable)

1. **Measured values only.** Every scored observable is a *measured phenomenon* with a citation
   and a tolerance — a Hz, a coupling index, a propagation speed, a present/absent fact, a
   relational fact (X higher than Y). **Interpretations are never scored.**
2. **No tuning.** Concordance is raised **only** by adding emergence mechanisms that genuinely
   produce the measured value from the 4D-DNA substrate, or by a **named external calibration**
   that is *measured and cited*, never fabricated. Loosening a tolerance to force a match is
   forbidden.
3. **One substrate.** Organs emerge from 4D-DNA master genes (M0); the brainwave is emitted by
   the emerged populations (M1); memory is an emerged engram cell (M2); binding is angle
   rectification at the **measured** ephaptic fraction κ = 0.5496 (M9–M11). New disease regimes
   reuse these — no new tuned constant.
4. **Honest scoreboard.** Each observable is **matched** (emerged & reproduced) or **owed**
   (target, with the *named* external input or mechanism required). The concordance fraction is
   reported every release; the program's goal is to drive it to 1.0 honestly.

---

## 1. Current status (v1.15)

**M13 `emerge_spectral_observables()` shipped** — the brain-structure-like multi-source coupled
field (12 measured-master-gene organ nodes **+ a prefrontal frontal-midline-theta node**, placed
on the M9 ephaptic ring, phase-circulated through the measured-κ pathways) emits the full LFP, and
the **1/f aperiodic exponent EMERGES at x ≈ 1.94** inside the measured Voytek band [1.5, 3] — with
**no fitted slope** (the aperiodic floor is charge-weighted shot noise through four *measured*
synaptic kernels). This **closes the owed `eeg_aperiodic_1f_slope` by emergence**, lifting the
**core measured-observable catalogue to 16 / 20 = 0.80** (was 15/20 = 0.75 in v1.14). M13 also adds
three new matched observables (oscillatory peaks above the aperiodic floor; all-or-none recurrent
ignition; theta-gamma MI tied to the M2 recall outcome) and keeps one honestly **owed**
(`aperiodic_slope_flattens_with_arousal` — directional but 7/8 < the 0.9 robustness gate), giving an
**extended catalogue of 19 / 24 = 0.792**. The emitted brainwave still drives the hypothalamus in a
**bounded closed loop** (M12).

> **Honest scope.** Reproducing a phenomenon is never a claim about its interpretation. The
> `recurrent_ignition_nonlinear` observable reproduces a *measured nonlinear-threshold signature*
> only — it is **not** a claim of consciousness. `medium_efficacy_tested = 0`; the hard problem
> stays OPEN. Two runs → identical sha256; M0–M12 outputs are byte-identical to v1.14.

### Matched (16) — emerged from the 4D-DNA substrate, reproduced bit-for-bit
The 15 of v1.14 (EEG bands δ/θ/α/β/γ · canonical 40-Hz gamma · regional band diversity ·
working-memory 5–9 slots · LFP front ~c · cross-frequency coupling · hypothalamus slow/delta ·
theta-gamma MI = 0.011 · ADHD-like reduced TGC · dream-recall theta threshold · alpha
desynchronisation) **plus `eeg_aperiodic_1f_slope` now closed by M13 emergence (x ≈ 1.94)**.

### Owed (the explicit path to 100 %)
| Observable | Measured target | What 100 % requires (named) |
|---|---|---|
| `sleep_spindle_hz` | NREM-2 spindles 11–16 Hz | **mechanism:** a thalamo-reticular spindle generator (waxing-waning envelope), emerged (M14) |
| `aperiodic_slope_flattens_with_arousal` | 1/f flattens with arousal (Gao 2017) | **mechanism:** make the directional flattening robust (thalamocortical conductance model / longer record) — currently 7/8 < the 0.9 gate |
| `sws_delta_amplitude_uv` | δ peak-to-peak > 75 µV | **calibration:** a *measured* microvolt amplitude scale (M15) |
| `panic_peak_minutes` | attack peaks within ~10 min | **calibration:** a *measured* second/minute time scale (M15) |
| `p300_latency_ms` | oddball P300 ≈ 300 ms | **calibration:** a *measured* millisecond time scale + an oddball/ERP emergence (M15) |

Two distinct kinds of owed work remain: **(a) emergence mechanisms** (the spindle generator; making
the arousal-flattening robust; an ERP/oddball) that the substrate *can* support, and **(b) external
unit calibrations** (µV, ms) that must be *measured and cited*, never fitted. A genuine 100 % needs
both — each a named milestone, not a number to force.

---

## 2. Architecture roadmap (modules)

- **M0–M11 (shipped):** organ emergence · EM brainwave · engram memory · eddies/selection/
  learned-field/stream/embodied · field coherence · inter-organ ephaptic coordination · sensory
  coupling · **light→brainwave→rectified-information→memory binding**.
- **M12 (shipped, v1.14):** measured-observable concordance + hypothalamus loop (this scoreboard).
- **M13 `emerge_spectral_observables()` (shipped, v1.15):** the brain-structure-like multi-source
  coupled field (organs + a prefrontal node, ephaptic ring/pathways, Kuramoto circulation) emits the
  full LFP; the **1/f aperiodic exponent emerges at x ≈ 1.94** (Voytek band) with no fitted slope,
  plus oscillatory peaks above the floor, all-or-none recurrent ignition, and the **theta-gamma MI
  tied to recall** — closes `eeg_aperiodic_1f_slope` by emergence (core 16/20 = 0.80).
- **M14 `emerge_sleep_architecture()` (shipped, v1.16):** on the same substrate, a population of R19
  thalamocortical relaxation cells (carrier frequency **set by the cited T-current recovery τ_rec=13
  ms**) coupled through the M9 ephaptic ring as **diffusive (Laplacian)** coupling, with a bistable
  recruitment oscillator gated by the cited **Ca→Ih adaptation** (Lüthi & McCormick 1998) producing
  the **waxing-waning** envelope; the **spindle emerges at 15.38 Hz, 8/8 seeds in 11–16 Hz** — closing
  `sleep_spindle_hz` by emergence (**core 17/20 = 0.85**). Also adds the cortical **slow oscillation
  (<1 Hz, 0.49 Hz emerged)**, the **waxing-waning** signature, the **NREM/REM band shift**, and the
  **REM dream-recall loop** tied to the M2 Hippocampus (honors the already-matched M12
  `dream_recall_theta_increase` as a mechanism; not re-scored).
- **M15 `emerge_calibration_bridge()` (planned):** a single *measured, cited* µV and ms anchor
  (one voltage scale, one time scale) that converts dimensionless emergence to clinical units —
  unlocking `sws_delta_amplitude_uv`, `p300_latency_ms`, `panic_peak_minutes` **without tuning**
  (one calibration each, audited like λ_ref).
- **M16+ `emerge_disorder_*()` (planned):** the disease program (§3), each a regime of the same
  substrate with its measured brainwave signature as the target.

---

## 3. The disease program (large-scale)

Each disorder is modelled as a **regime of the emerged substrate** (a coupling-quality, drive,
sensitivity, or excitability setting — all reusing measured constants), and is scored by the
**measured brainwave/EEG signature** it must reproduce. Already-studied disorders have a
standalone emergence in `repro/mind/_bridge/`; the rest are planned modules.

| Disorder | Measured brainwave signature (the scored target) | Emergence handle | Status |
|---|---|---|---|
| **Panic disorder** | rapid paroxysmal escalation; interoceptive (CO₂/pH) false alarm; peaks ~10 min | runaway positive-feedback **bifurcation** (sensitivity s) | studied (stress test) → M16 + µs/ms calib |
| **ADHD** | **reduced theta-gamma coupling** during task; ↑θ/β ratio | disorganised coupling quality q → lower MI | **emerged in M12** + deepen |
| **Dyslexia** | atypical low-freq (δ/θ) & gamma speech entrainment; disrupted θ→γ | mis-phased coupling on sensory bands | studied → M16 |
| **Learning disability (general)** | encoding fails despite effort | coupling quality below q_crit (structural, not weak) | **emerged (stage J)** |
| **Epilepsy / seizure** | runaway hypersynchrony (R→1), spike-wave 3 Hz | coupling κ pushed past the lock threshold (M9 regime) | planned M17 |
| **Schizophrenia** | reduced evoked **40-Hz gamma**; impaired θ-γ; ↓PAC | gamma-generation / coupling deficit | planned M17 |
| **Alzheimer's / MCI** | slowing (↑δ/θ, ↓α/γ); ↓theta-gamma coupling | organ-band drift + coupling loss | planned M18 |
| **Parkinson's** | exaggerated **β-band** synchrony (subthalamic) | β over-coupling in a basal-ganglia node | planned M18 |
| **Depression (MDD)** | frontal **α asymmetry**; altered θ cordance | inter-hemispheric α imbalance | planned M19 |
| **Autism (ASD)** | abnormal **α-γ** coupling; altered connectivity; E/I imbalance | cross-band coupling shift + long-range under-connectivity + E/I excitability | **studied (D7+D8 candidate)** — D7: S1 reduced PAC + S2 E/I hyper-excitability + S3 long-range under-connectivity reproduced, "pathway, not frontal-lobe"; **D8: the κ-deficit split into WIRING vs OUTPUT-weak vs THRESHOLD-high via a unique (ΔPAC, ignition) fingerprint** — a gain/threshold drug reverses gain faults but cannot correct wiring (the ADHD-med discriminant), an exogenous 4–8 Hz supply rescues all incl. wiring (over-syncs if over-dosed); E/I→1/f readout + which-fault-is-real-autism owed |
| **PTSD** | ↑θ, exaggerated threat-evoked responses; amygdala dominance | drive-capture + low extinction (M11/stress) | studied (capture) → M16 |
| **Addiction / craving** | cue-evoked salience capture; PFC hijack | strong drive captures the integrator (stage G) | **emerged (stage G)** |
| **Bipolar (mania/depression)** | state-dependent band/arousal swings | arousal-loop set-point shifts (M12 loop) | planned M20 |
| **Anaesthesia / coma / DoC** | loss of complexity; α-front/burst-suppression; ↓PCI | drive/coupling collapse; the §12 honest PCI negative | planned M20 — **vegetative-limit MECHANISM touched in D8**: when the R19 fold exceeds the measured ephaptic ceiling κ no neighbour can re-ignite (never self-recovers); only exogenous drive above the fold crosses it (ignition ≠ experience — Axis A firewall, consciousness_claim=0) |
| **Migraine** | cortical spreading depression; pre-ictal rhythm change | propagating depolarisation on the lattice (M1) | planned M21 |
| **Sleep disorders (insomnia/narcolepsy)** | spindle/SO/REM anomalies | M14 sleep architecture perturbed | planned (after M14) |

**Scoring rule for every disorder:** it counts as *reproduced* only when the emergence yields
the **measured** signature (a band shift, a coupling change, a synchrony regime, a relational
fact) at the stated tolerance — never an interpretation, never a forced fit. Each disorder adds
its measured signatures to the M12-style scoreboard, growing the catalogue toward a comprehensive
**measured-phenomenology coverage**.

---

## 4. Milestones (toward 100 %)

1. **v1.14 (this release):** M12 concordance 0.55 → **0.75**; brainwave studies packaged; this
   research program set as the governing goal. ✓
2. **v1.15 — M13 spectral:** emit full LFP; **1/f slope x ≈ 1.94 (Voytek band)**, oscillatory peaks,
   all-or-none ignition, **MI→recall loop** → `eeg_aperiodic_1f_slope` closed by emergence; **core
   catalogue 0.75 → 0.80** (extended 19/24 = 0.792). The ≈0.85 estimate is *approached*; the honest
   measured number is reported, with `aperiodic_slope_flattens_with_arousal` owed until robust. ✓
3. **v1.16 — M14 sleep architecture:** thalamo-reticular spindles (15.38 Hz, 8/8 in 11–16 Hz; carrier
   set by cited τ_rec, waxing-waning from cited Ca→Ih), cortical slow oscillation (0.49 Hz < 1 Hz),
   NREM/REM band shift, REM dream-recall loop → `sleep_spindle_hz` closed by emergence; **core
   catalogue 0.80 → 0.85** (17/20; extended 23/27 = 0.852). No tuning; the honest measured numbers are
   reported. ✓
4. **v1.17 — M15 calibration bridge:** one measured µV + one measured ms anchor (audited like
   λ_ref) → `sws_delta_amplitude_uv`, `p300_latency_ms`, `panic_peak_minutes` unlocked → **≈ 1.0
   on the core catalogue.**
5. **v1.18+ — M16…M21 disorder modules:** expand the catalogue with each disease's measured
   signature; drive *comprehensive* measured-phenomenology coverage to 100 %.

**Definition of done (100 %).** Every catalogued **measured** observable — healthy and
disease — is reproduced by the 4D-DNA emergence at its stated tolerance, with all unit anchors
**measured and cited**, no tuned constant anywhere, and the honest [V]/[I]/[O] ledger intact.
Anything that cannot be reached without fabricating a value stays **owed** with its named input —
honesty before completeness.

---

## 5. Honest ledger (program-wide)

- **[F]** forced/cited: c, λ_ref, the lattice unit, α = 2/π, δ = 1/π², κ = 0.5496, atlas γ.
- **[V]** verified in code: every emerged observable reproduces deterministically (SEED = 19,
  bit-for-bit), gated.
- **[I]** inference: all clinical/cognitive *mappings* (consciousness, dreams, the drive panel,
  the disorder regimes) are literature-concordant inference, **not proof**; schematic drive
  magnitudes are ordering-only.
- **[O]** open: `medium_efficacy_tested = 0`; nothing is claimed causal for experience; the hard
  problem is untouched; the µV/ms calibrations and several mechanisms are **owed**, named, and
  un-fabricated.

*Reproduce the current scoreboard:* `cd repro/mind/_engine && python3 run_all.py` then read
`results/mind_emergence_results.json → M12_brainwave_phenomenology`. The brainwave studies behind
the disorder regimes are in `repro/mind/_bridge/` (each deterministic and self-checking).
