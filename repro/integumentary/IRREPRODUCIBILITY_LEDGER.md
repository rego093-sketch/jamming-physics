# IRREPRODUCIBILITY LEDGER

Every `[O]` (open) quantity must be listed with its specific obstacle (VP-SPEC C3). An `[O]` without a
stated obstacle is a gate FAIL. The shapes, controls, orderings, and dichotomies in the site stand
independently of these open absolute magnitudes.

| item | grade | obstacle (why not reproducible in-package) | location |
|---|---|---|---|
| to-measure master-gene γ | [O]→[V] | none deferred for this package (`_to_measure: []`); any future master fetched via the DNA atlas as a measured input, not fitted | inherited/organ_gamma.json |
| absolute TEWL (g·m⁻²·h⁻¹) | [O] | T1 threshold + discontinuous-collapse SHAPE verified [V]; absolute flux needs stratum-corneum lipid permeability D and the trans-barrier water-activity gradient ΔC | docs/02, repro/_engine/skn_dynamics.py |
| absolute wound closure rate (µm·h⁻¹) | [O] | T2 unjam→migrate→rejam sequence + chronic-wound threshold verified [V]; q*=3.81 cited [L]; absolute rate needs a measured single-cell migration speed | docs/03, skn_dynamics.py |
| absolute minimal erythema dose / melanin OD | [O] | T3 concave-plateau response, partial attenuation, and feedback-off control verified [V]; absolute MED needs the melanin extinction coefficient | docs/04, skn_dynamics.py |
| absolute basal cycle time (per cell) | [O] | T4 conveyor-sum STRUCTURE verified [V] and rate set by one cited anchor (SC transit ~14 d) [L]; per-cell basal cycle needs a per-cell calibration | docs/05, skn_dynamics.py |
| absolute set-point (37 °C) & sweat rate | [O] | T5 thresholded onset, flux-regulated slope drop, and runaway-above-capacity verified [V]; absolute set-point/rate need per-gland output and body heat capacity | docs/06, skn_dynamics.py |
| absolute cancer incidence & RR magnitude | [O] | ONCO dichotomy directions verified [V] on cited anchors [L] (Gandini SRR 1.61; Armitage–Doll K≈5); absolute incidence/RR need a population baseline rate and absolute dose calibration | docs/07, repro/_oncology/carcinogen_dose_response.py |
| absolute organ size / mass | [O] | DWELL ∝ γ^1.5 fixes RELATIVE size/order [F]; absolute scale needs external calibration | repro/_engine |

All `[O]` items above are mirrored on the site's Methods page (docs/08) under the obstacle ledger.

## Pathology module (repro/_pathology) — added v0.2.0

Each disease is a NAMED perturbation of an existing target's knob; the intervention is the same knob
reversed. The mechanism SHAPE (direction / threshold / discontinuity) is verified [V] and the clinical
direction is anchored [L]; every absolute magnitude INHERITS the parent target's `[O]` obstacle — no
disease introduces a new constant. The opposite-sign discriminant (same R19 switch, opposite drive
signs → clinically opposite pairs, no new constant) is [V].

| disease ([V] shape) | parent target | absolute quantity left [O] | inherited obstacle |
|---|---|---|---|
| atopic dermatitis | T1 | absolute baseline TEWL (g·m⁻²·h⁻¹) | same as T1 (lipid permeability D + ΔC); the barrier-RESERVE collapse is dimensionless [V] |
| contact dermatitis | T1 | absolute baseline TEWL (g·m⁻²·h⁻¹) | same as T1; the ACUTE discontinuous collapse at the spinodal is [V] |
| ichthyosis | T1+T4 | absolute stratum-corneum residence (days) | same as T4 per-cell + desquamation-rate calibration; the retention FOLD vs the spinodal is dimensionless [V] |
| psoriasis | T4 | absolute epidermal transit (days) | same as T4; the package does not predict the absolute basal cycle time. THRESHOLD at the differentiation spinodal + several-fold autonomous acceleration are [V]; cited 3–5 d vs 28–40 d is the anchor [L], not a reproduced number |
| chronic / diabetic / pressure wound | T2 | absolute closure rate (µm·h⁻¹) | same as T2 (single-cell migration speed); non-closure BELOW the package's own critical unjamming drive is [V] |
| vitiligo | T3 | absolute repigmentation dose / time | same as T3 (melanin extinction coeff.); discontinuous melanocyte-viability loss at the spinodal + hysteresis + photoprotection loss are [V] |
| melasma / hyperpigmentation | T3 | absolute melanin optical density | same as T3; the regulated OVERSHOOT fold above baseline (opposite pole of vitiligo) is dimensionless [V] |
| albinism (OCA) | T3→oncology | absolute cancer incidence | same as ONCO (population baseline + dose calibration); the melanin-screen-removed hazard RATIO vs pigmented skin is [V] |
| hypohidrotic ectodermal dysplasia | T5 | absolute core-temperature set-point (°C) | same as T5 (per-gland output + body heat capacity); the capped-sweat danger-band SHIFT to lower load is [V] |
| primary hyperhidrosis | T5 | absolute sweat rate | same as T5; the LOWERED recruitment-threshold / sweat-onset shift (opposite pole of HED) is [V] |
| heat stroke | T5 | absolute critical core temperature (≈40 °C) | same as T5; the RUNAWAY slope jump once evaporative capacity is exceeded is [V] |
| skin cancer (melanoma / SCC / BCC) | oncology | absolute incidence & RR magnitude | same as ONCO; the intermittent-vs-cumulative DICHOTOMY + pigment-loss burst-RR elevation are [V] |
| actinic keratosis | oncology | absolute prevalence / conversion rate | same as ONCO; the precursor ABUNDANCE (low-stage » full multistage) and shared-kernel rise are [V] |

Pathology results are written to `reports/pathology_results.json` by `repro/run_pathology.py`. This is a
RESEARCH artifact and does NOT touch the writing gate; the core T1..T5+ONCO battery
(`repro/run_all.py`, sha unchanged) is untouched and remains the gate of record.

## Hair-cycle module (repro/_cycle) — added v0.5.0

A NEW emergent relaxation oscillator on the EXISTING measured EDAR γ (no new organ, no new fitted
constant). The cycle SHAPE — that it oscillates, that anagen dominates, that the waveform is a
plateau-then-collapse relaxation cycle, and the delayed-vs-immediate shedding dichotomy — is verified
[V]; the clinical directions are anchored [L]. The honest constraint specific to this layer: the
oscillator is graded against its anchors by **dominance and direction, not magnitude**, because a constant
drive strong enough to hit the cited absolute anagen fraction would cross the element's Hopf point and
**destroy the oscillation**. So the absolute anagen fraction and the years-long period are deliberately
held [O], not tuned. Each alopecia is a NAMED signed perturbation of the one oscillator; intervention is
the same drive reversed; the three-way opposite-sign / opposite-timing discriminant is [V].

| item ([V] shape) | grade | obstacle (why not reproducible in-package) | location |
|---|---|---|---|
| absolute anagen fraction (cited ~85–90 %) | [O] | the anagen-DOMINANCE and the relaxation WAVEFORM are dimensionless [V]; the absolute fraction cannot be tuned without crossing the Hopf point and killing the limit cycle, and otherwise needs a per-follicle calibration (the appendage target's standing obstacle) | docs/10, repro/_cycle/hair_cycle.py |
| absolute cycle period (years) | [O] | the relaxation TIMING ratios (e.g. the one-telogen shed lag) are dimensionless and reproduced [V]; the absolute years-long period needs an external clock calibration for the appendage | docs/10, repro/_cycle/hair_cycle.py |
| androgenetic alopecia — absolute hair count / vellus fraction | [O] | inherits the appendage obstacle (per-follicle calibration); the anagen-shortening DIRECTION + progressive miniaturisation + minoxidil reversal are [V] | docs/10, repro/_cycle |
| alopecia areata — absolute patch extent / regrowth latency | [O] | inherits the appendage obstacle; the anagen-COLLAPSE under a sustained drive + regrowth-on-removal hysteresis are [V] | docs/10, repro/_cycle |
| telogen effluvium — absolute shed count / 3-month latency | [O] | needs an absolute cycle period (above); the DELAYED synchronised shed at exactly one telogen lag and self-limitation are [V] | docs/10, repro/_cycle |
| anagen effluvium — absolute shed fraction / onset | [O] | inherits the appendage obstacle; the IMMEDIATE shed (no telogen delay) and reversibility on removal are [V] | docs/10, repro/_cycle |

Hair-cycle results are written to `reports/cycle_results.json` by `repro/run_cycle.py`. Like pathology,
this is a RESEARCH artifact with its own 2×sha256 determinism hash
(`d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822`); it does NOT touch the writing gate,
and the core battery (`repro/run_all.py`, sha `1fb59f556e01…` unchanged) remains the gate of record.

---

## Sebaceous-duct module (repro/_seb) — added v0.6.0

A NEW measured organ (PRDM1/Blimp1, γ=1.3432, fetched + cached + vendored through the same promoter-ΔG
pipeline validated against MITF/EDAR — reproduces offline bit-for-bit, so it is **not** an `[O]` item) run
as a hysteretic two-state occlusion jam on the EXISTING R19 switch (no new fitted constant). The jam SHAPE
— discontinuous closure at the upper spinodal, hysteretic reopening only at a lower one, the healthy-patent
set-point, and the reversible-vs-irreversible depth discriminant — is verified `[V]`. The occlusion
set-points are dimensionless regime scales `[F]` (forced, not fitted; not `[O]`). The absolute magnitudes
below remain open, each inheriting the new sebaceous target's standing obstacle (a per-gland calibration):

| item ([V] shape) | grade | obstacle (why not reproducible in-package) | location |
|---|---|---|---|
| acne vulgaris — absolute comedo / lesion counts | [O] | the occlusion-jam DIRECTION, the discontinuous closure, the inflammatory branch, and the reopening on the reversed knobs are dimensionless `[V]`; absolute comedo/lesion counts need a per-gland calibration (the sebaceous target's obstacle) | docs/11, repro/_seb/sebaceous_duct.py |
| hidradenitis suppurativa — absolute Hurley-stage extent / sinus-tract counts | [O] | the deeper-occlusion jam, the rupture/scar branch absent in acne, and the drive-down irreversibility are `[V]`; absolute tract counts and Hurley extent need a per-gland calibration | docs/11, repro/_seb |
| absolute sebum excretion rate | [O] | the jam SHAPE is `[V]` and the occlusion set-points are dimensionless regime scales `[F]`; the absolute sebum output rate needs a per-gland secretion calibration | docs/11, repro/_seb/sebaceous_duct.py |

Sebaceous results are written to `reports/seb_results.json` by `repro/run_seb.py`. Like pathology and the
hair-cycle layer, this is a RESEARCH artifact with its own 2×sha256 determinism hash
(`1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84`); it does NOT touch the writing gate,
and the core battery (`repro/run_all.py`, sha `1fb59f556e01…` unchanged) remains the gate of record.

---

## Cell-adhesion module (repro/_adhesion) — added v0.7.0

A NEW target on the EXISTING measured KRT14 γ (no new organ, no γ fetched, none fitted — desmosomes and
hemidesmosomes anchor the keratinocyte's keratin network, so junctional adhesion is intrinsic to this organ;
the hair-cycle pattern, not the sebaceous new-organ pattern) run as a hysteretic two-state binding jam on the
EXISTING R19 switch (no new fitted constant). The jam SHAPE — discontinuous detachment at the lower spinodal,
hysteretic re-adhesion only at a higher one, the healthy-adherent set-point above the upper spinodal, the
compartment-selected cleavage plane, the **derived** Nikolsky sign, and the blister-tension direction — is
verified `[V]`. The adhesion reserve and the antibody titres are dimensionless regime scales `[F]` (forced,
not fitted; not `[O]`). The clinical mappings are cited anchors `[L]`. The absolute magnitudes below remain
open, each inheriting the adhesion target's standing obstacle (a per-junction calibration):

| item ([V] shape) | grade | obstacle (why not reproducible in-package) | location |
|---|---|---|---|
| pemphigus vulgaris — absolute blister count / involved BSA | [O] | the cell-cell de-adhesion DIRECTION, the discontinuous detachment, the intraepidermal plane, the derived positive Nikolsky sign, and the re-adhesion on antibody clearance are dimensionless `[V]`; absolute blister counts and body-surface area need a per-junction calibration (the adhesion target's obstacle) | docs/12, repro/_adhesion/adhesion_switch.py |
| bullous pemphigoid — absolute blister count / involved BSA | [O] | the cell-matrix de-adhesion DIRECTION, the subepidermal plane, the derived negative Nikolsky sign, and the re-adhesion on clearance are `[V]`; absolute counts and BSA need a per-junction calibration | docs/12, repro/_adhesion |
| absolute autoantibody titre (IU/mL) | [O] | the de-adhesion threshold SHAPE is `[V]` and the titres are dimensionless regime scales `[F]`; the absolute titre in IU/mL needs a per-assay calibration | docs/12, repro/_adhesion/adhesion_switch.py |
| absolute cleavage depth (µm) | [O] | the cleavage-plane SELECTION (intraepidermal vs subepidermal, from the targeted compartment) is `[V]`; the absolute split depth in microns needs a per-junction histological calibration | docs/12, repro/_adhesion/adhesion_switch.py |

Adhesion results are written to `reports/adhesion_results.json` by `repro/run_adhesion.py`. Like pathology,
the hair-cycle layer and the sebaceous layer, this is a RESEARCH artifact with its own 2×sha256 determinism
hash (`55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad`); it does NOT touch the writing
gate, and the core battery (`repro/run_all.py`, sha `1fb59f556e01…` unchanged) remains the gate of record.

---

## Vasomotor module (repro/_vasomotor) — added v0.8.0

A NEW target on the EXISTING measured EDAR γ (no new organ, no γ fetched, none fitted — the cutaneous
thermoregulatory interface, the EDAR organ, carries two autonomic effector arms, the sudomotor/sweat arm
(T5) and the vasomotor/blood-flow arm; rosacea dysregulates the vasomotor arm, the vascular mirror of
hyperhidrosis on the sudomotor arm, so vasomotor reactivity is intrinsic to this organ; the hair-cycle /
adhesion pattern, not the sebaceous new-organ pattern) run as a hysteretic two-lock reactivity jam on the
EXISTING R19 switch (no new fitted constant). The jam SHAPE — a discontinuous dilation lock at the upper
spinodal, a discontinuous constriction lock at the lower one, the healthy-responsive set-point in the
reversible middle, and reversibility as a uniform consequence of **whether a drive crosses its lock** — is
verified `[V]`. The resting tone, reactivity gains and trigger/constrictor drives are dimensionless regime
scales `[F]` (forced, not fitted; not `[O]`). The clinical mappings are cited anchors `[L]`. **The
dermal-perfusion magnitude is an INHERITED circulatory seam, not re-emerged here** — only the reactivity
dynamics is added. The absolute magnitudes below remain open, each inheriting the vasomotor target's
standing obstacle (a per-vessel calibration):

| item ([V] shape) | grade | obstacle (why not reproducible in-package) | location |
|---|---|---|---|
| rosacea — absolute erythema index / vessel density / involved BSA | [O] | the vasodilation DIRECTION, the discontinuous dilation lock (fixed telangiectasia), the reversible sub-lock flush, the papulopustular amplifier and the hysteretic non-reset by a partial constrictor are dimensionless `[V]`; absolute erythema index, vessel density and BSA need a per-vessel calibration, and the perfusion magnitude is an inherited circulatory seam (the vasomotor target's obstacle) | docs/13, repro/_vasomotor/vasomotor_switch.py |
| Raynaud phenomenon — absolute digital temperature / attack frequency / duration | [O] | the vasoconstriction DIRECTION (opposite pole on the same switch), the reversible attack, and the vasodilator/CCB reversal are `[V]`; absolute digital temperature, attack frequency and duration need a per-vessel calibration, and the perfusion magnitude is an inherited circulatory seam | docs/13, repro/_vasomotor |
| absolute flush magnitude / dermal perfusion | [O] | the reactivity-jam SHAPE is `[V]` and the tone/reactivity/constrictor drives are dimensionless regime scales `[F]`; the absolute flush magnitude and the dermal-perfusion level are an INHERITED circulatory seam (cited, not re-emerged), not calibrated in this package | docs/13, repro/_vasomotor/vasomotor_switch.py |
| secondary-Raynaud fixed digital ischemia / ulcer | [O]→seam | NOT modeled here: the fixed digital-ischemia / ulcer of secondary Raynaud is a downstream structural change of connective-tissue disease — an immune/rheumatology sibling-package seam, named not faked; the in-package layer covers the reversible primary vasospasm `[V]` | docs/13, HANDOFF §2/§4 |

Vasomotor results are written to `reports/vasomotor_results.json` by `repro/run_vasomotor.py`. Like
pathology, the hair-cycle layer, the sebaceous layer and the adhesion layer, this is a RESEARCH artifact with
its own 2×sha256 determinism hash
(`53a99f522ad684a11bcc6d4d33c5e8123d1f4dff5a75836c0bbced6736a62003`); it does NOT touch the writing gate, and
the core battery (`repro/run_all.py`, sha `1fb59f556e01…` unchanged) remains the gate of record.

---

## Seam-manifest module (repro/_seam) — added v0.9.0

NOT a new physical sweep and **NOT a source of any new `[O]`** — a consolidation layer that gathers the
package's interfaces (master map §9.2) into one labelled, machine-readable record, in three honestly
distinct classes (INHERITED-IN / INTERNAL-LIVE / DECLARED-OUT). It adds **no new mechanism and no new
constant**. The one INTERNAL-LIVE coupling it surfaces — pigment-loss → oncology (a melanocyte-target T3
screen-loss raising the shared oncology-kernel hazard) — is **re-exported verbatim** from the already-graded
pathology layer, not recomputed, so it introduces no new quantity to grade: its absolute magnitude simply
**inherits the oncology obstacle** already on the books (row "absolute cancer incidence & RR magnitude",
docs/07 — population baseline rate + absolute dose calibration). The seam's truthfulness is enforced by its
own gate rather than by a physical sweep, and the only items to record here are the honesty/provenance
properties that gate verifies:

| item | grade | obstacle / property (why it is honest, not reproducible-by-fiat) | location |
|---|---|---|---|
| pigment-loss → oncology absolute RR (SCC hazard ≈ 2.58× / melanoma burst ≈ 10.59× / sunscreen-restored ≈ 1.13×) | [O] | the coupling DIRECTION + the sunscreen causal-lever SIGN are dimensionless `[V]` and re-exported verbatim from the verified pathology layer (so the seam output provably *is* the internal link, not a parallel implementation); the absolute RR magnitude INHERITS the oncology obstacle — a population baseline rate and absolute dose calibration (docs/07), nothing new added here | docs/14, repro/_seam/seam_manifest.py |
| DECLARED-OUT sibling-package seams (gene-lesion → `disease_wp`; immune/rheumatology; out-of-class infections) | [O]→seam | NOT live wiring: these are contracts flagged honestly as **declared, not yet wired** — the §5.3/§5.4 integration harness does not exist; each carries its in-package back-pointer (master map §6.2), named not faked | docs/14, HANDOFF §5.3/§5.4 |
| re-export fidelity (seam INTERNAL value == pathology's own return) | [V] | gate check (A): every internal field equals the pathology layer's own value field-by-field — the property that makes "expose the already-internal link" a true statement rather than a re-derivation | repro/_seam/seam_verify.py |
| non-disturbance (the seam reads the disease layer, it does not perturb it) | [V] | gate check (D): the pathology layer's own 2×sha256 hash `0a4404ccde65…` is **unchanged** after the seam runs, and the core battery is never imported here — the seam is a reader, never a writer | repro/_seam/seam_verify.py |

Seam results are written to `reports/seam_manifest.json` (the machine-readable seam record) and
`reports/seam_results.json` (the gate record) by `repro/run_seam.py`. Like every additive layer before it,
this is a RESEARCH artifact with its own 2×sha256 determinism hash
(`52b49a95a9add070a05a02848b1a4cef0589f4a36791167232fda3fc1c1d58f7`); it does NOT touch the writing gate, it
does NOT alter any disease layer it reads (pathology `0a4404ccde65…` unchanged), and the core battery
(`repro/run_all.py`, sha `1fb59f556e01…` unchanged) remains the gate of record.
