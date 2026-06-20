# FUTURE WORK — Cardiorespiratory (research roadmap)

**Status of this document.** These are PROPOSED, not gate-passed, results. Each item carries an
*anticipated* grade, not an achieved one. Nothing here enters the canonical site (`docs/`) until it
passes its own discriminant under wide sweeps with **no per-target tuning** — the same research-first
rule that governed T1–T5 and the oncology kernel. This file is a planning artifact at the package
root (a sibling of `CHARTER.md`), deliberately kept out of `docs/`.

**Scope discipline.** This package models cardiorespiratory disease at the level of **mechanism
dynamics** — relaxation oscillators, delayed control loops, and R19 bistable switches — *not* molecular
immunology, viral kinetics, allergic-cascade biochemistry, or pharmacodynamics. Those upstream causes
enter the model only as an applied **bias** or a parameter shift; the molecular layer belongs to a
future sibling package (see §4) or stays exogenous. We model the *dynamical consequence*, honestly
bounded.

> **UPDATE — priorities 1–6 now have deterministic prototype results.** The six top-priority items in
> §7 (Mayer waves, asthma, OSA, the CSA spectrum, fever co-scaling, cough) are implemented in
> `repro/_disease/respiratory_disease.py`, graded by `repro/_disease/disease_battery.py`, and summarized
> in `DISEASE_FINDINGS.md`. The battery passes **6/6** and the module is deterministic (two-run identical
> sha256). NO new substrate primitive was needed — every disease reuses R19 + FHN, as anticipated. The
> grades in the tables below remain *anticipated*; what was achieved is recorded in `DISEASE_FINDINGS.md`,
> where several items advanced from "anticipated [V?]" toward demonstrated mechanism reuse while ALL
> absolute magnitudes (PC20, Pcrit, C5, absolute febrile rate) stayed honestly **[O]**. None of this is
> canonical until it passes a writing gate of its own; it stays out of `docs/`.

---

## 0. How a disease enters this framework

Every respiratory disorder is cast as a perturbation of an object this package already built. There
are exactly three mechanism classes, plus seam crossings — and **none of them needs a new substrate
primitive**. That is itself a claim of the program: one substrate (R19 switch + FitzHugh–Nagumo
relaxation oscillator) suffices.

| class | meaning | new primitive? | example |
|---|---|---|---|
| **A — parameter perturbation** | shift a gain/delay/setpoint/stiffness of an existing loop or oscillator | none | chronic hypercapnia resets chemoreflex setpoint |
| **B — new R19 switch** | a tissue with two stable mechanical states; attack = spinodal crossing; hysteresis = bistable loop | reuses R19 (`barrier`, `spinodal`) | airway smooth-muscle tone; pharyngeal patency |
| **C — new threshold reflex** | a stereotyped pulse triggered above an irritant threshold = FHN in the *excitable* (sub-Hopf) regime | reuses FHN `Neuron` | cough |
| **seam** | coupling to a sibling package (circulatory; a future immune package) | n/a | cor pulmonale; allergic sensitization |

Each task below states: VP-native mechanism · class · which existing object it reuses · the
discriminant that would verify or falsify it · the anticipated grade · the cited clinical anchor it
would be tested against.

---

## 1. Near-term consolidation (within current scope, high confidence)

These tighten what is already built and are the cheapest wins.

- **Mayer-wave baroreflex oscillation (~0.1 Hz)** — class A, reuses T5. The baroreflex loop (gain BRS,
  latency ~0.6 s) is a delayed negative feedback; by the *same* logic that gives Cheyne–Stokes a period
  of about twice the chemoreflex delay (T4), the baroreflex loop should self-oscillate near **0.1 Hz**
  when its loop gain exceeds one. This is a forced prediction and a clean discriminant.
  *Anticipated grade:* **[V]** (mechanism reuse); absolute frequency [L] against the cited Mayer-wave band.
  *Anchor:* Mayer waves ~0.1 Hz; LF-HRV band 0.04–0.15 Hz (already in `cardiac_rhythm_anchor.json`).

- **Full LF/HF autonomic balance** — class A, extend RSA (T3). Use both cited bands (LF 0.04–0.15,
  HF 0.15–0.40) to reproduce the LF/HF ratio shift between vagal and sympathetic states.
  *Grade:* directions **[V]**; absolute ratio [L].

- **Operating-point shifts (exercise, sleep, posture)** — class A. The drive/τ sweep already shows the
  oscillator’s rate sensitivity; map named autonomic states to operating points.
  *Grade:* directions **[V]**.

---

## 2. Disease-extension program (the requested expansion)

### 2.1 Asthma — class B (airway smooth-muscle tone switch) · **strongest extension**
**Mechanism.** Airway smooth muscle is bistable: a relaxed (open) basin and a constricted basin. This
is an **R19 switch**, identical in form to every other switch in the program. A bronchoconstrictor
(methacholine, histamine, allergen-driven mediators) is a sustained **bias h>0** that *lowers the
barrier* toward the constricted basin — exactly the role the carcinogen bias plays in §8, but
**reversible**: a bronchodilator is the opposite (negative) bias toward the open basin. An acute attack
is a **spinodal crossing** (sudden, threshold, all-or-none). Clinically observed **airway hysteresis**
is the bistable hysteresis loop; **deep-inspiration bronchodilation** is a mechanical drive perturbation
that flips the switch back across the spinodal.

**Reuse.** This extension reuses the *already-derived* exact barrier machinery from the oncology module
(`barrier_eff` from the cubic `s³ − γs − h = 0`, Kramers occupancy). A prototype confirms it is
numerically coherent: a convex, thresholded constriction-vs-dose curve that saturates near the spinodal,
fully reversible by sign of the bias.

**Discriminant.** (i) Methacholine/histamine challenge dose–response: airway resistance vs dose has the
convex/threshold R19 shape, with **PC20** (the provocative dose for a 20% FEV₁ fall) acting as a
spinodal-like crossing threshold — the *same* curve family as the oncology RR(dose) plot, with a
removable bias. (ii) Hysteresis between the constriction and dilation limbs. (iii) Deep-inspiration
reversal as a mechanical re-crossing.
*Anticipated grade:* bistable hypothesis + hysteresis **[V?]**; challenge dose–response *shape* **[V]**
(reuses the built kernel); absolute **PC20** magnitude **[O]** — *same obstacle as the oncology absolute
RR:* the switch noise scale and the molecular dose→bias conversion are not fixed by substrate geometry.
*Anchor:* methacholine-challenge PC20; published airway-resistance hysteresis curves.

### 2.2 Obstructive sleep apnea (OSA) — class B (pharyngeal patency switch) + existing loop gain
**Mechanism.** The pharynx has two mechanical states (patent / collapsed) — another R19 switch. During
sleep the dilator drive falls; below a critical value the patent basin disappears and the airway
**collapses at a spinodal** (the critical closing pressure **Pcrit**). Mixed apnea = the pharyngeal
switch *coupled to* the chemoreflex loop already built in T2.
**Reuse.** The normalized loop gain `LG/LGc` from T2 maps directly onto the clinical **“loop gain”**
endotype that stratifies OSA patients — this is the same quantity the OSA-physiology literature uses by
that exact name.
*Discriminant:* (i) collapse is discontinuous/hysteretic in airway pressure (Pcrit = spinodal); (ii)
high loop gain predisposes to ventilatory instability (reuses T2).
*Anticipated grade:* bistable collapse **[V?]**; loop-gain endotype mapping **[V]** (T2 reuse); absolute
Pcrit **[O]**. *Anchor:* Pcrit measurements; loop-gain endotyping.

### 2.3 Central sleep apnea / periodic-breathing spectrum — class A (largely already done)
**Mechanism.** Altitude (hypoxic gain ↑), heart failure (circulatory delay ↑ — already T4), and opioids
(drive ↓) are each *one axis* of the existing apnea machinery (loop gain, delay, drive). The model
already predicts the direction for each.
*Anticipated grade:* directions **[V]** (reuse T2/T4); absolute thresholds **[O]**.
*Anchor:* altitude periodic breathing; CHF Cheyne–Stokes (T4 anchor); opioid-induced central apnea.

### 2.4 COPD / emphysema — class A (pump mechanics) + chemoreflex reset
**Mechanism.** Loss of elastic recoil changes the ventilatory-pump stiffness/time constant; air
trapping; chronic hypercapnia resets the chemoreflex setpoint and alters loop gain → altered periodic-
breathing susceptibility. The “pink puffer” and “blue bloater” pictures become two operating regimes of
the *same* control system.
*Anticipated grade:* directions **[V]**; absolute lung mechanics **[O]** (needs patient calibration).
*Anchor:* spirometry / recoil and chronic-hypercapnia data.

### 2.5 Common cold / acute viral infection + fever — class A + a substrate-distinctive thermal lever
**Mechanism.** Acute mucosal swelling and secretions raise airway resistance transiently (class A). The
*distinctive* prediction is the **fever lever**: in this program γ is set by nearest-neighbor stacking
free energy, which is **temperature-dependent** (SantaLucia). Fever (T↑) lowers effective stacking
stability → lowers the R19 barrier `B = γ²/4`. Because the heart and lung FHN oscillators **share** this
γ/temperature dependence, febrile **tachypnea and tachycardia must rise together**, and the HR–RR
relationship under fever should follow a substrate-forced co-scaling rather than two independent drifts.
*Discriminant:* febrile HR vs RR co-scaling with a forced ratio; the clinical “~10 bpm per °C” rule as a
calibration anchor. A prototype confirms γ↓ lowers both oscillators’ barriers together.
*Anticipated grade:* co-scaling direction **[V?]**; quantitative ratio **[V/L]**; absolute rates **[O]**.
*Anchor:* febrile heart-rate / respiratory-rate rules. (Connects to the program’s temperature-dependent-γ
thread shared with the DNA/thermodynamic volume.)

### 2.6 Cough — class C (threshold-triggered protective reflex)
**Mechanism.** Cough is an irritant accumulation crossing a threshold that triggers a stereotyped high-
amplitude expiratory pulse = a *single FHN excitation* in the excitable (sub-Hopf) regime, not the
oscillatory regime. Chronic cough = a sensitized (lowered) threshold.
*Discriminant:* all-or-none response above a capsaicin-challenge threshold (C5/C2) = the excitation
threshold of the FHN unit.
*Anticipated grade:* threshold-excitation **[V?]**; absolute C5 **[O]**. *Anchor:* capsaicin cough challenge.

### 2.7 Pulmonary fibrosis / restrictive disease — class A (stiffness ↑)
Increased stiffness drives a rapid-shallow-breathing operating point of the ventilatory pump.
*Anticipated grade:* direction **[V?]**; absolute mechanics **[O]**.

### 2.8 Pulmonary hypertension / cor pulmonale — **seam** (lung → circulatory → cardiac)
Chronic lung disease raises pulmonary vascular load and strains the right heart, feeding back to the
cardiac oscillator. This crosses the seam to `circulatory_vp_site` (pump) and is **joint future work**;
it cannot be closed inside this package alone.
*Anticipated grade:* **[O]** until the circulatory package exists.

---

## 3. New primitives required (and their status)

The honest accounting: **no new substrate primitive is needed.** Every extension reuses R19 and FHN.

| effector to add | what it is | reuses | status |
|---|---|---|---|
| airway-tone switch | reversible-bias R19 switch (asthma, COPD bronchospasm) | `barrier`, `spinodal`, oncology `barrier_eff` | math ready; needs measured/cited γ_airway and a bias map |
| pharyngeal-patency switch | reversible-bias R19 switch (OSA), Pcrit = spinodal | same | math ready; needs Pcrit anchor |
| cough excitation | FHN in excitable (sub-Hopf) regime | `Neuron` | regime exists; needs threshold anchor |
| temperature → γ map | read-only thermal dependence of stacking ΔG (fever) | DNA/thermodynamic seam | seam, not a new primitive |

A planned home for the code: `repro/_disease/` (airway switch, pharynx switch, cough excitation), with
per-target stress tests mirroring `stress_tests.py`, and per-disease anchors under `inherited/`.

---

## 4. Seam / boundary work

- **`circulatory_vp_site` seam** — PaO₂/PaCO₂, cardiac output, cor pulmonale. This package is SSOT for the
  gas/pump boundary; the circulatory package cites it. Do not re-emerge these here.
- **Proposed `immune_vp_site` seam (does not yet exist)** — allergic sensitization, eosinophilic
  inflammation, viral replication are **upstream** of the dynamics. Today they are represented *only* as
  the applied bias `h` that lowers a switch barrier (asthma) or a transient parameter shift (cold). A
  future immune package would own that biochemistry. Until then this is **honestly out of scope** and
  flagged, not silently absorbed.

---

## 5. Discriminant summary

| disease | class | object reused | discriminant | anticipated grade | anchor |
|---|---|---|---|---|---|
| Mayer waves | A | baroreflex (T5) | ~0.1 Hz BP oscillation when loop gain > 1 | [V] / abs [L] | Mayer-wave band |
| Asthma | B | oncology kernel (reversible) | convex/threshold challenge curve; PC20 = spinodal; hysteresis | shape [V], hyst [V?], abs [O] | methacholine PC20 |
| OSA | B + loop | T2 | Pcrit = spinodal collapse; loop-gain endotype | [V?]/[V]; Pcrit [O] | Pcrit, loop gain |
| CSA spectrum | A | T2/T4 | altitude/CHF/opioid each one axis | directions [V]; abs [O] | periodic-breathing data |
| COPD | A | pump + chemoreflex | recoil ↓, hypercapnia setpoint reset | directions [V]; abs [O] | spirometry |
| Cold + fever | A + thermal | both oscillators via γ(T) | HR–RR co-scaling, ~10 bpm/°C | [V?] / [V/L] / abs [O] | febrile HR/RR rules |
| Cough | C | FHN excitable | all-or-none above capsaicin threshold | [V?]; abs [O] | capsaicin C5 |
| Fibrosis | A | pump | rapid-shallow operating point | [V?]; abs [O] | restrictive PFTs |
| Cor pulmonale | seam | circulatory | RV strain feedback | [O] (awaits sibling) | PH data |

---

## 6. Honest limits (what this framework will NOT claim)

- It does **not** model molecular immunology, viral kinetics, pharmacodynamics, or the allergic cascade.
  It models the **dynamical consequence** (oscillator / loop / switch perturbation), with the molecular
  driver as an exogenous bias or a sibling-package seam.
- **Absolute magnitudes** (Pcrit, PC20, capsaicin C5, absolute lung mechanics, absolute febrile rates)
  are **[O]** for the *same structural reason* as absolute organ size (§1, §9) and absolute cancer RR
  (§8): the switch noise scale and the stimulus→bias conversion are not fixed by substrate geometry and
  need external calibration. The **shapes and directions** are the forced/verifiable content.
- These are hypotheses with *anticipated* grades. None becomes canonical until it passes its discriminant
  under wide sweeps with no per-target tuning.

---

## 7. Priority ordering

1. **Mayer-wave baroreflex oscillation (~0.1 Hz)** — near-term, forced, reuses T5.
2. **Asthma methacholine dose–response** — directly reuses the built oncology Kramers kernel (reversible
   bias); highest payoff.
3. **OSA pharyngeal switch + loop-gain endotype** — reuses T2.
4. **Periodic-breathing spectrum (altitude / CHF / opioid)** — reuses T2/T4.
5. **Fever HR–RR co-scaling** — substrate-distinctive shared-oscillator prediction.
6. **Cough excitation threshold** — reuses FHN excitable regime.
7. **Cor pulmonale seam** — awaits the circulatory package.

---

## 8. Reproducibility-technology inheritance (from `analgesic_threshold_logic` v2.0)

This roadmap originally carried the *scientific* extension program (sections 0–7) but **omitted the
reproducibility apparatus** that `analgesic_threshold_logic` v2.0 had matured
(concept DOI `10.5281/zenodo.20733420`). That gap is closed in **v0.5.0**: the apparatus is inherited,
actively applied to this package, and scheduled for retroactive application across the sibling packages.

### 8.1 What was inherited and applied here (v0.5.0)

The "reproducibility technology" is the delivery-side guarantee layer, distinct from the scientific
content. As applied to this package it consists of:

1. **File-level fingerprint manifest** — `manifest/SHA256SUMS.txt`, a SHA256 over the whole canonical
   tree (code + site + inherited assets + governance docs), `sha256sum -c` compatible. Catches silent
   byte-drift in *any* shipped file, not just engine output. **Fail-closed**: an absent or empty
   manifest is a FAIL, never a silent pass.
2. **Fail-closed forbidden-claim scanner** — `repro/_verify/claim_scanner.py`, curated regex patterns
   over `docs/**`. Blocks drug-dosing, prescriptive, treatment-of-disease, and efficacy/safety language
   while deliberately preserving the legitimate epidemiological vocabulary of the oncology chapter.
   Enforces the CHARTER firewall (mechanism, not clinic) mechanically.
3. **Whole-harness determinism (drift-0)** — a single recompute of the full result blob
   (engine ⊕ stress ⊕ oncology ⊕ disease) twice, byte-identical, with all wall-clock removed from the
   build and from report snapshots.
4. **Offline self-containment proof** — the engine and stress battery reproduce with the network
   socket disabled; no hidden remote dependency.
5. **`CONSTITUTION.md`** — the inviolable articles (firewall, honest grading, no-tuning, research-first,
   determinism, provenance) gathered into one normative document.
6. **Unified one-command harness** — `repro/run_all.py` ending in a single
   `OVERALL: PASS (N/N checks)  drift 0  DOI …` line, returning a non-zero exit on any failure.
7. **Provenance binding** — the package concept DOI `10.5281/zenodo.20755371` wired into every section
   page, the hub, structured metadata (JSON-LD), `_meta.json`, and `llms.txt`; a DOI-consistency gate
   (R10) fails the build if any surface drifts or any placeholder survives.
8. **Archival deposit triple** — LaTeX → PDF whitepaper (scalable fonts, no Type-3) plus the
   reproducibility ZIP, deposited together under the concept DOI.

The grading discipline is unchanged: every absolute clinical magnitude remains **[O]** (section 6),
and the scanner exists precisely so that the reproducibility layer can never be mistaken for a clinical
claim.

### 8.2 Retroactive-application plan for sibling packages

The same eight-point apparatus is to be inherited by the existing VP-Theory packages that predate it.
For each package the inheritance is the identical checklist — **(a)** file-level `SHA256SUMS` manifest
(fail-closed) · **(b)** `claim_scanner` tuned to that package's legitimate vocabulary · **(c)**
whole-harness drift-0 with wall-clock removed · **(d)** offline self-containment proof · **(e)**
`CONSTITUTION.md` · **(f)** unified `OVERALL: PASS` entry point · **(g)** concept-DOI binding + R-gate ·
**(h)** archival deposit triple — and is complete only when that package's `run_all` reports
`OVERALL: PASS  drift 0`.

| # | Sibling package | Inheritance status | Notes |
|---|-----------------|--------------------|-------|
| 1 | `analgesic_threshold_logic` (v2.0) | **source** | Origin of the apparatus; DOI `10.5281/zenodo.20733420`. |
| 2 | `cardioresp_vp_site` (v0.5.0) | **done (this release)** | First full inheritance; reference implementation. |
| 3 | `mind_vp_site` | planned | Largest tree (faculty atlas §17, D-series); scanner must whitelist the neuro/affective lexicon. |
| 4 | `dna_vp_site` | planned | Methylation/lactase chapters; manifest over the multi-page canonical layout. |
| 5 | `neuro_emergence_chain_integrated` | planned | 20-chapter chain; drift-0 over the full sensory/motor/sleep blob. |
| 6 | `disease_wp` | planned | 35-disease dossier cohort; scanner tuned to dossier vocabulary (burden/treatment-mechanism survey is descriptive, not prescriptive). |
| 7 | `universal_morphogenesis_geneclock` | planned | Cross-species blob; offline proof over the gene-clock recompute. |
| 8 | `vp_physics` / `geodynamics` / `cosmology` / `fluid_dynamics` | planned | Already at VP-SPEC v1.8; add manifest + drift-0 + DOI gate to each. |
| 9 | `integumentary_vp_site` (v0.3.0, in progress) | adopt-at-source | New package — build the apparatus in from the start rather than retrofitting. |

**Ordering.** Priority follows tree size and clinical-surface risk: packages whose sites carry the most
disease/clinical-adjacent prose (mind, disease_wp, cardioresp ✓) get the fail-closed scanner first;
the pure-physics packages (vp_physics, geodynamics, cosmology) need mainly the manifest + drift-0 +
DOI gate. New work (`integumentary_vp_site`) adopts the apparatus at source, which is cheaper than
retrofitting and is the standing policy for all future packages.
