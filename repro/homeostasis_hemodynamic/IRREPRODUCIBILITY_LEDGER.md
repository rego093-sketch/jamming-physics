# IRREPRODUCIBILITY LEDGER

Every `[O]` (open) quantity must be listed with its specific obstacle (VP-SPEC C3). An `[O]` without a
stated obstacle is a gate FAIL. This package reproduces loop/curve **shapes and directions** ([V]) and
cites external **identities/gains/mortality** ([L]); the items below are the ABSOLUTE scales it does not
claim to derive.

## Resolved (v0.4.0)
- **REN master-gene γ (raas_endocrine)** `[O]→[V]` **DONE.** Previously a named master not yet in the DNA
  γ atlas; now MEASURED in-package, γ = 1.3634 (gc 0.4746), via the identical NN-stacking ΔG37 pipeline
  (SantaLucia 1998) on the cited promoter (NC_000001.11 minus, TSS 204166337 = NCBI gene-model 5' end,
  cross-checked vs Ensembl canonical ENST00000272190; window TSS-2000..+500). The pipeline is validated by
  reproducing the locked SIX2 atlas value exactly (1.5556 / 0.6381, length 2501) from the documented
  convention with no fitting — a measured input, never fitted. Sequence cached in
  `inherited/organ_promoters.cache.json`; recomputed offline by `inherited/measure_gamma.py`. Recorded in
  `inherited/organ_gamma.json` (genes.REN). No master-gene γ remains to measure for this package.

## Open (absolute scales — declared boundaries)

| item | grade | obstacle | location |
|---|---|---|---|
| absolute arterial pressure scale (mmHg) | [O] | RP1/RP3/RP4 fix the relation and the SHAPE (MAP=CVP+CO·SVR; perfect adaptation; reset opposed back); the absolute mmHg mapping needs external calibration of the seam units (CO, SVR, CVP) | repro/_engine/vp_hmd_loops.py (RP1, RP3, RP4) |
| absolute baroreflex gain + latency | [O]/[L] | RP2 reproduces the buffering SHAPE (residual ≈ step/(1+G)); the absolute open-loop gain and closed-loop latency are cited anchors, not derived | repro/_engine/vp_hmd_loops.py (RP2) |
| absolute baroreceptor firing rate (Hz) | [O] | S1 reproduces the monotone transduction CURVE and the KO-flat phenotype; the absolute Hz scale (and threshold/saturation pressures) needs electrophysiological calibration | repro/_sensory/baroreceptor.py |
| absolute macula-densa NaCl set + GFR scale | [O] | S2 reproduces the monotone renin↓ / TGF↑ transductions and the SGLT2i direction; absolute luminal NaCl (mM) and GFR (mL/min) need external calibration | repro/_sensory/macula_densa.py |
| absolute disease incidence rate (hypertension) | [O] | the setpoint-reset SHAPE reproduces (P*=P0+dPset, opposed back); absolute incidence needs epidemiological calibration (cohort) | repro/_pathology/setpoint_failure.py |
| absolute HF progression / event rate | [O] | the saddle-node collapse DYNAMICS reproduce (spinodal(κ*)=|load|); absolute event rates need clinical calibration | repro/_pathology/setpoint_failure.py |
| absolute therapy effect sizes (RDN ΔSBP; four-pillar HR/NNT) | [O]/[L] | T1/T2 fix only the DIRECTION (durability ∝ reference reset; mortality benefit ∝ margin growth); the cited effect sizes (e.g. RDN ~ −20 mmHg @3yr; ARNI −16%) are anchors [L], not derived; absolute model effect sizes [O] need calibration | repro/_therapy/fundamental_targets.py |
| absolute hypotension thresholds + shock incidence (RP6–RP9) | [O] | RP6–RP9 fix only the failure NODE and direction (orthostatic buffer loss; downward reference reset; SVR-floor collapse; one-directional volume fold); the absolute postural-drop mmHg, the perfusion-floor MAP, and shock incidence/mortality need clinical calibration | repro/_pathology/hypotension_family.py |
| absolute per-taxon pressures + the exact phylogenetic transition point (C1) | [O] | C1 fixes only the loop-accretion SHAPE (incidental → error-regulated → defended) and the three-leg requisite; the absolute pressure per taxon and the precise clade where the integral loop becomes dominant need comparative-physiology calibration | repro/_comparative/setpoint_emergence.py |

## Open (comfort-logic intervention layer — v0.7.0, firewalled by design)

The comfort-logic layer (`repro/_intervention/`) READS the proven loop directions (RP4 reject / T1
durable / T2 margin) and PLACES each axis on a lever. The lever placement is `[V]` (structural, read off
a proven loop). Everything a structural loop reading cannot establish stays `[O]` and is enforced
fail-closed by the forbidden-claim firewall — stating any of these as fact refuses the build.

| item | grade | obstacle | location |
|---|---|---|---|
| per-axis molecular mechanism (receptor / transporter / channel pharmacology) | [O] | `comfort_map()` places each axis on a lever from the loop read; the actual pharmacology that could realise the direction is cited biology, NOT derived from the loop — and is graded `[O]` per axis by the honesty gate | repro/_intervention/intervention_logic.py; counterreg_honesty.py |
| any molecule / exposure schedule / regimen | [O] | the package names none; HP1–HP7 are structural directions only. No molecule is designed, no exposure schedule or route is given | repro/_intervention/comfort_proposal.json (explicit_non_claims) |
| efficacy / potency in patients | [O] | the loop read fixes only the DIRECTION (reference-reset durable vs operating-point rejected); no efficacy result is asserted or derivable | repro/_intervention/forbidden_claim_scan.py (EFFICACY_AS_FACT) |
| tolerability / safety of any agent | [O] | "counter-regulation-free" is a STRUCTURAL property of where a lever acts (no operating-point error for the integrator to reject); it is NOT a tolerability or safety statement about any molecule, which is a cited clinical question outside the model | repro/_intervention/forbidden_claim_scan.py (SAFETY_AS_FACT); §20 firewall |
| absolute counter-regulation magnitudes (reflex HR rise, renin escape size) | [O] | RP4/RP2 fix only the DIRECTION of counter-regulation (an operating-point push is opposed back; a reference reset is not); the absolute magnitudes of the reflex responses need clinical calibration | repro/_intervention/intervention_logic.py (anchors from RP4/T1) |

## Calibrated (v0.6.0)

The absolute scales above remain **un-derived from first principles** (each first-principles row stays
`[O]` with its obstacle intact — calibration is **not** derivation, exactly as absolute *g* stays open in
the physics volume even once anchored to a measured length). What v0.6.0 adds is a **`[CAL]` calibration
layer** (`repro/_calibration/scale_calibration.py`, wired into the engine and gated by CAL1–CAL7 in the
21-suite stress battery): each absolute scale is fixed by **(i)** an explicitly cited external anchor,
**(ii)** propagated through an already-LOCKED `[V]` relation that reuses existing primitives (no new
substrate math, C1), and **(iii)** cross-checked against an **independent** cited reference *not* used as
the anchor, via a **computed discriminant** (no silent pass). Genuinely un-calibratable quantities are
**not** forced into a pass — they are listed as residual `[O]` below.

| id | absolute scale | grade | cited anchor → locked relation | independent cross-check | residual `[O]` (not calibrated) |
|---|---|---|---|---|---|
| CAL1 | arterial pressure scale (mmHg) | `[O]→[CAL]` | resting CO 5.0 L·min⁻¹, SVR 17.8 WU, CVP 4 mmHg → RP1 hydraulic identity MAP=CVP+CO·SVR | all four quantities land inside independent normal clinical bands at once (MAP≈93, SVR upper-edge) | first-principles absolute mmHg |
| CAL2 | baroreflex gain + buffered step (mmHg) | `[O]/[L]→[CAL]` | open-loop gain G=3 → RP2 control law buffered=G/(1+G), residual=step/(1+G) on CAL1 scale | buffered fraction 0.75 and residual mmHg match the cited carotid-sinus closed-loop range | absolute closed-loop latency (ms) |
| CAL3 | baroreceptor firing rate (Hz) | `[O]→[CAL]` | one cited saturation point F_max≈100 Hz → baroreceptor sigmoid (single anchor scales the whole curve) | firing ≈50 Hz at setpoint and ≈96 Hz near saturation match independent single-fiber afferent reports | exact threshold/saturation pressures per fiber type |
| CAL4 | macula-densa NaCl set + GFR scale | `[O]→[CAL]` | cited distal NaCl operating point ≈30–45 mM → NKCC2 transduction curve | predicted delivered-NaCl band overlaps independent micropuncture range (honest ~2× order-of-magnitude note recorded) | single-nephron GFR (mL·min⁻¹) and NKCC2 K_m |
| CAL5 | hypertension reset in clinical SBP | `[O]→[CAL]` | cited resting SBP≈120 mmHg + reset shift → RP4 reset on CAL1 scale | reset defended SBP lands in the cited stage-1/stage-2 hypertensive band | absolute disease **incidence** (cohort) |
| CAL6 | therapy effect sizes (RDN ΔSBP; HF sign) | `[O]/[L]→[CAL]` | cited RDN ≈ −20 mmHg @3 yr; PARADIGM-HF / PROMISE signs → T1/T2 margins on CAL1 scale | model RDN drop within 15 % of the anchor; HF inotrope (−) vs four-pillar (+) signs match independent trials | absolute HR / NNT / event rates |
| CAL7 | perfusion floor + orthostatic threshold | `[O]→[CAL]` | cited organ-perfusion MAP floor ≥65 mmHg; consensus orthostatic ΔSBP≥20 mmHg → RP8 floor / RP6 step | RP8 vasoplegic floor sits at the cited MAP floor; RP6 un-buffered step meets the consensus orthostatic definition | absolute shock incidence/mortality; per-taxon pressures; exact phylogenetic transition clade |

**Net effect.** Each absolute-scale `[O]` now has a companion `[CAL]` row that places the model on the
clinical scale and survives an independent cross-check; the **first-principles** derivation of every one of
these scales, and the five residual `[O]` items in the last column (disease incidence, single-nephron
GFR/K_m, trial HR/NNT, per-taxon pressures, exact transition clade), remain **open with their obstacles
unchanged**. `n_scales_closed = 7/7`; `n_residual_open_items = 5`; calibration is deterministic and
re-derived offline by `scale_calibration.all_calibration()`.
