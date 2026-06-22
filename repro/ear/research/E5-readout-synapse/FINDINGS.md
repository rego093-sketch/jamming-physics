# FINDINGS — increment E5 (the READOUT substrate: otoferlin Ca²⁺-triggered ribbon-synapse release)

**Status:** DELIVERED (v0.6.0) — **turns E4's named [O] into a modelled result**. Deterministic module
`run.py` (2×sha256 identical: `69eca2ba…`), small gate `gate.py` (7/7 PASS), folded into
`tools/verify_seed.py` foundation list. **NO inherited byte changed** — E5 fetches no new gene, folds
nothing into the cache/atlas, and triggers **no re-freeze** (every frozen hash is byte-identical to
v0.5.0). No constant tuned.

## What E5 builds
E4 closed congenital deafness as the cubic's failure-mode decomposition but left **one** class an honest
**[O]**: the READOUT class (OTOF / auditory neuropathy). E4's words — *"the switch flips normally, the
cubic sees nothing wrong, the broken layer is the downstream synapse [O]."* E5 supplies that downstream
layer **explicitly** and composes it with the **frozen, unedited** transduction cubic, so the OTOF
phenotype stops being asserted and becomes **reproduced**.

The keystone is structural: **the readout layer cannot be the R19 cubic, and that is forced, not
assumed.** The cubic `ṡ = g·s − s³ + h` is two-sided, odd-symmetric, and **bistable** (a detector). A
vesicle-release rate is **non-negative** (you cannot release negative vesicles), **monotone** in Ca²⁺,
and **saturating** (a finite readily-releasable pool) — none of which the cubic is. The minimal normal
form carrying exactly those three properties is a **rectified saturating (Hill) sensor**, a genuinely
**different substrate** downstream of the switch. So E4 was right that the cubic is blind to OTOF, and
E5 says precisely **why**.

| stage | substrate | what it is | OTOF status |
|---|---|---|---|
| transduction switch (E1/E2) | R19 cubic `g·s−s³+h` | bistable, all-or-none | **intact** (flips normally) |
| active amplifier (E3) | R19 cubic at criticality `g→0` | compressive `F^(1/3)` (OHC) | **intact** (OAE present) |
| **readout (E5)** | **rectified saturating Ca²⁺ sensor** | graded, one-sided, NOT bistable (IHC synapse) | **broken** (release → 0) |

## Results (every number reproduced offline, bit-for-bit)
- **OTOF reproduces; nothing inherited moved.** OTOF's γ=1.4245 + A4 recompute from the frozen cache
  and equal the atlas bit-for-bit (A4 = signal − γ, |mean(shape)|<1e-9). E5 fetched no gene and changed
  **no inherited byte** — the full frozen-hash set is identical to v0.5.0 (gate G2 verifies). **[V]**
- **The readout is a DIFFERENT normal form — forced by what release is.** The sensor is non-negative,
  monotone in Ca²⁺, saturating to Rmax, and **non-bistable** (a pure function of Ca²⁺ — zero hysteresis,
  max|up−down|<1e-15), in direct contrast to the bistable cubic. This is the provable reason the E4 cubic
  cannot see OTOF: it is the **wrong layer**. **[F]/[V]**
- **Auditory neuropathy MODELLED — the dissociation falls out of the cascade.** Driving a sound (h past
  the spinodal) flips the frozen switch to **s=+1.3864 — byte-identical in a hearing AND an OTOF ear**
  (the substrate sees nothing wrong, exactly E4's READOUT finding). The intact sensor then gives evoked
  release 0.5810 (nerve **fires**); the removed sensor gives release **0.0000** (nerve **silent**). The
  defect is purely **downstream of the flip**. **[F]/[V]**
- **The composed compression exponent — the E3 bridge.** At criticality the transduction output
  compresses as `settle(0,F) ≈ F^(1/3)` (E3); feeding it into a power-law sensor `R ∝ Ca^m` gives the
  cascade **`R ∝ F^(m/3)`** — fit to m/3 at machine precision for m∈{1,2,3,4} (max|Δ|=5.6e-15). The
  auditory-nerve rate-level slope is the **amplifier cube-root (1/3, forced) × the synaptic
  cooperativity m (cited [L])**. Falsifiable: ~1/3 if mature IHC m≈1. **[F]/[V]**
- **The OAE⁺/ABR⁻ clinical fingerprint — forced by separable stages.** The amplifier stage (E3, outer
  hair cell / prestin) keeps its cube-root response (exponent 0.333333) in an OTOF ear → **otoacoustic
  emissions PRESENT**; the readout stage (E5, inner hair cell / otoferlin) is zeroed → **auditory-
  brainstem response ABSENT**. Because the amplifier (OHC, upstream/parallel) and the readout (IHC
  synapse, downstream) are **different stages of one cascade**, one is intact while the other fails —
  the textbook auditory-neuropathy signature, now structurally explained. It also **distinguishes** the
  readout class from the drive/structure classes (which would also degrade OAE / thresholds). **[F]/[V]**
- **The lever DIRECTION is now forced (E4 had it [O]).** The geometry forces the substrate-inverse lever
  to act on the **readout stage** (restore Ca²⁺-sensor coupling / Ca²⁺-triggered fusion), **not** on the
  switch (g,h) — the switch is provably intact. This is the **opposite locus** from the drive class
  (restore h) and the structure class (rebuild g). **Direction-only, proposal-only** — no molecule, dose,
  in-vivo selectivity, or efficacy. **[F]** direction; magnitude **[O]**.

## Honest negatives / open items (preserved, not hidden)
- **N1.** EVERY magnitude is **[O]**: absolute [Ca²⁺], the sensor Kd/Rmax, the readily-releasable-pool
  size, the release rate (vesicles/s), the auditory-nerve rate (Hz), any real-unit threshold. Only the
  STRUCTURE (rectifying/saturating/non-bistable), the dissociation, and the composed exponent m/3 are forced.
- **N2.** The synaptic cooperativity **m is cited biology [L]**, study-dependent (~1 mature IHC / ~3–4
  conventional; Dodge & Rahamimoff 1967, Beutner et al. 2001, Johnson et al. 2005), **never derived from
  the substrate and never tuned**. The composed result is given parametrically in m; its qualitative
  force (silence on knockout) is **m-independent**.
- **N3.** The Ca²⁺(s) map is a **minimal monotone rectifying proxy** Ca ∝ s₊ on the substrate's own zero.
  The real map (CaV1.3 I–V curve + Ca²⁺-nanodomain geometry) is **[O]**; only the sign/rectification is
  used, and the disease result does not depend on its detailed shape.
- **N4.** "Sensor removed" is modelled as evoked release ≡ 0 (no Ca²⁺-triggered fusion). Graded/partial
  otoferlin loss, temperature-sensitive variants, and the spontaneous (resting) release component are
  **[O]**; E5 models the **evoked**, sound-driven release only.
- **N5.** The lever is **direction-only and proposal-only** (firewall). No molecule is designed, no dose
  or efficacy stated; nothing is diagnosed or treated. The felt percept is the mind volume's.
- **N6.** The full fluid-loaded dispersive traveling-wave **ENVELOPE** is **still the named [O]** — a
  closed envelope needs Q + fluid mass-loading + the E3 amplifier and would require **tuning Q**
  (forbidden). E5 does not touch it; it remains open with its obstacle named.

## Why this matters, honestly stated
E5 is the model-honesty payoff of E4's discipline: the class E4 was careful to label **[O]** ("the cubic
is the wrong layer") is now turned into a **modelled** layer that earns its keep. It explains, from the
cascade structure alone, **why** a child with otoferlin loss can have a normally amplifying cochlea
(OAEs present) yet a silent auditory nerve (ABR absent) — the amplifier and the readout are different
stages — and it states **where** the lever must act (the sensor stage, the opposite locus from the
connexin/pendrin drive class and the stereocilia structure class). It states **directions and a
composed exponent, never doses**. Nothing here is a diagnosis, a treatment, or a promise.

## Naming note (flagged, not silently fixed)
Delivered in the unambiguous folder `research/E5-readout-synapse/` as the **E4-N4 READOUT extension**.
The v0.3.0 folder-numbering slip stands flagged (BLUEPRINT-E2, the MET switch, shipped in the folder
labelled `E1`; **BLUEPRINT-E1**, the traveling-wave ENVELOPE, remains the named **[O]**). E5 introduces
no new inconsistency; a future session may reconcile `BLUEPRINT.md`'s E-numbering with the folder names.

## Firewall
γ read promoter STRUCTURE only (never a Ca²⁺-sensor affinity, a release rate, a vesicle count, a voltage,
a dose, an in-vivo selectivity, or an effect). The disease layer is **proposal-only** — a direction-only
READOUT-failure mode and a direction-only substrate-inverse lever. The percept of hearing is the mind
volume's.
