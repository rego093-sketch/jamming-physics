# START HERE — increment E10 (light/dark adaptation; beyond the spine)

The second **mechanism extension beyond the down-conversion spine** (E0→E8 complete; E9 built; see
`BLUEPRINT.md`). **BUILT (v0.14.0).**

**Scope — theoretical, NON-CLINICAL (binding, above the task).** Purely academic dynamical-systems
research into a **normal physiological mechanism** — how the eye keeps working across a huge range of
background light. It is **not** a disease chapter: it does **not** diagnose, treat, prescribe, screen, or
triage; it designs **no** molecule and states **no** dose, luminance, threshold, or Weber fraction. The
felt brightness percept is deferred to the **mind** volume.

**Task:** show that **light/dark adaptation needs no new machinery** — it is the **same** frozen R19
switch (E2) read on its **steady-state ON branch**, where the cubic makes the response **saturate**. E10
adds **no new γ**, fetches nothing, and re-derives nothing; it consumes the frozen field
`ds/dt = γ·s − s³ + h`, the fold `spinodal(γ)`, the Neuron recovery `τ_s`, and the already-measured γ of
RHO/CNGB3 (read-only).

**Why this framing (the productive path):** the steady state of the frozen field is the real root of
`s³ − γ·s − h = 0`; for a large background drive *h* the cubic dominates, so `s*(h) → h^(1/3)` — a
**compressive** response. That one fact yields all three signatures of adaptation:
(A) a ~5-decade background range is **log-compressed** into a ~1.5-decade response (deep in saturation the
compression → the cubic order **n = 3**) — dynamic range;
(B) the incremental gain `ds*/dh = 1/(3s*²−γ)` **falls** as the background rises — automatic gain control,
a bright surround turning the switch down;
(C) — the headline — the **contrast** gain `(h/s*)·ds*/dh → 1/n = 1/3 EXACTLY` (in the pure-cube limit
`s*=h^(1/3)` it is `0.333333` for any *h*), a **Weber-Fechner-like** law where equal fractional steps feel
equal, **forced by the cube and independent of γ** (the same limit for two different genes' γ).

**Deliverable (done):** a deterministic module `research/E10-light-dark-adaptation/run.py` that
(A) settles the ON-branch steady state across a background sweep and shows `s*/h^(1/3) → 1` (each `s*` a
**true zero** of the frozen field, residual ≈ 0), with the operating-sweep and saturated-sweep
log-compression (→ n=3);
(B) reads off the incremental gain `1/(3s*²−γ)`, shows it falls monotonically dim→bright (≈1296× across the
sweep) and `∝ h^(−2/3)`;
(C) shows the contrast gain rising to `1/3`, proves the **pure-cube limit is exactly 0.333333 = 1/n**, and
demonstrates **γ-independence** (RHO vs CNGB3 both → 1/3), with the honest note that this is the
**saturated** branch (near the fold the γ·s term matters and the response is steeper than a clean power
law — the Weber regime is the cube-root tail);
(D) names the **two regimes** (dark/fold = high gain + the single-photon FLIP of E2; bright = low gain,
compressed), reads **γ READ-ONLY** as the fold/offset (where dark sensitivity sits — *not* the compression
law, which is γ-independent, exactly as in E7/E8), reads the **recovery τ_s READ-ONLY** as the
dark-re-sensitisation time course (E7/E8; absolute seconds the inherited **[O]**), and hands the felt
percept to the mind volume. It prints every displayed number, self-hashes (2× run → identical sha256), and
declares grades [F]/[V]/[L]/[O] honestly. Plus `gate_E10.py` (`E10 GATE: PASS`, eight checks), folded into
the verifier's foundation list and absorbed into the HTML volume as chapter **E10**.

**Provenance (this increment):** **nothing was fetched and no γ was added.** E10 consumes only the frozen
substrate (`vp_substrate`: the field, the fold, the Neuron recovery τ) and the frozen atlas γ (read-only).
`inherited/FROZEN_SHA256.json` is **unchanged** — the foundation does not move for this increment. γ
measured, never fitted; the background drive *h* and the operating points are **inputs** that sweep the
field, never fitted targets.

**Firewall:** structure-only γ (never a channel voltage, gain, photocurrent, potency, dose, or clinical
effect); no clinical magnitude is produced (no absolute threshold, Weber fraction, or luminance unit); the
felt brightness percept is the mind volume's. (E10 is a normal-mechanism chapter, so unlike E4/E9 it carries
no disease-magnitude block — there is no condition layer to firewall — but it states no clinical quantity.)

**Next (same firewall, beyond the spine):** **accommodation + refractive error** (myopia/hyperopia)
extending E3's optics; and — much harder, multifactorial — an acquired/degenerative disease layer (AMD,
glaucoma, diabetic retinopathy). Still deferred: **SIX6** (eye-field TF), the one remaining gene in the
atlas `_to_measure`, foldable by the fetch→re-freeze discipline if a later increment needs it. The sibling
**hearing** sense ships as its own seed (`vp_ear_emergence_seed…`).
