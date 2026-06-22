# START HERE — increment E11 (accommodation & refractive error; beyond the spine)

The third **mechanism extension beyond the down-conversion spine** (E0→E8 complete; E9 + E10 built; see
`BLUEPRINT.md`). **BUILT (v0.15.0).**

**Scope — theoretical, NON-CLINICAL (binding, above the task).** Purely academic geometry/optics research
that extends E3's reduced-eye optics. It covers a **normal** mechanism (accommodation — a variable-power
lens) *and* the **mechanism layer** of the two commonest refractive conditions (**myopia** = near-sighted,
**hyperopia** = far-sighted). Because it touches a condition layer it is treated as a **firewalled clinical
chapter** (like E4/E9): it does **not** diagnose, treat, prescribe, screen, classify a person, or triage; it
designs **no** molecule and states **no** clinical quantity — and the firewall here additionally blocks any
**power magnitude in dioptres** and any **length in mm**, forcing the whole chapter to speak in dimensionless
**ratios** and **signs** only. The felt percept of blur/clarity is deferred to the **mind** volume.

**Task:** read E3's single-surface eye as a **MATCH** between two numbers the eye owns — its **power** and
its **length** — and show that (i) emmetropia is that match, (ii) refractive error is the *signed* mismatch,
(iii) accommodation is a one-signed power lever, (iv) each axis of the match has a forced **direction** from
the inherited foundation. E11 adds **no new γ**, fetches nothing, and re-derives nothing: it **consumes** the
frozen E3 optics (the single-surface equation `n₂/v − n₁/u = P`, `P=(n₂−n₁)/R`, and `n=√((B/ρ) ratio)`), the
frozen substrate size law `dwell ∝ γ^1.5`, and the already-measured γ of PAX6/RAX (read-only).

**Why this framing (the productive path):** from E3, a distant object images at `v_∞ = n₂/P`, and the eye is
in focus for distance ⇔ `v_∞ = L` (the axial length) ⇔ **`P·L = n₂`**. Define the dimensionless match ratio
`ρ ≡ P·L/n₂`. That one relation yields everything:
(A) **emmetropia** is `ρ = 1` — and the frozen Emsley reduced eye sits **exactly** on it (the cited n,R
cohere, not a fit); it is a whole **curve** in (power, length), a longer eye needing proportionally less
power;
(B) because `L − v_∞ = (P·L − n₂)/P`, the **sign** of the mismatch fixes the side: `ρ > 1` ⇒ focus **in
front** ⇒ **myopia**; `ρ < 1` ⇒ focus **behind** ⇒ **hyperopia** — and the *same* error is reachable two
independent ways, too **long** (axial) or too **powerful** (refractive), because only the **product** `P·L`
matters;
(C) **accommodation**: a near object at `u=−k·L` needs `P_req/P_∞ = 1 + n₁/(n₂·k)`, a pure number that
**rises monotonically** as the object nears and is **always ≥ 1** — a strictly **one-signed (additive)**
lever (the eye can only *round* the lens, `R↓ ⇒ P↑`, to pull focus nearer, never the reverse);
(D) the lever is pure lattice **geometry** (`P ∝ 1/R` ⇒ `dP/P = −dR/R`; `n=√((B/ρ) ratio)`, E3), while the
length axis is the substrate's own **size law** (`dwell ∝ γ^1.5`, E1) — so the growth axis has a forced
direction (more growth ⇒ longer eye ⇒ the myopic side), with the gene→elongation map and emmetropization
feedback the named **[O]**.

**Deliverable (done):** a deterministic module `research/E11-accommodation-refraction/run.py` that
(A) reads `ρ=1` off the frozen reduced eye (the surface focus verified two ways against E3's own equation);
(B) shows, for the **axial** and **refractive** routes, that the geometric blur side **equals `sign(ρ−1)`**
on E3's frozen surface equation, and that an equal-product (`q·ℓ=1`) eye returns to `ρ=1` — all via
dimensionless scale factors, never a magnitude;
(C) tabulates `P_req/P_∞` rising one-signed as the object nears, with the lens-radius ratio `R_req/R_∞ < 1`
(rounder), and asserts the implied `R_req` images the near object **onto the retina** (E3);
(D) verifies the geometric lever `dP/P = −dR/R`, reads PAX6/RAX **γ READ-ONLY** (byte-equal to the atlas) to
instantiate the size law `dwell ∝ γ^1.5`, fixes the growth-axis direction, and hands the felt percept to the
mind volume. It prints every displayed number, self-hashes (2× run → identical sha256), passes a
**machine-checked MAGNITUDE FIREWALL** (no dose/potency/power-magnitude/length token, no '%'), and declares
grades [F]/[V]/[V-arith]/[L]/[O] honestly. Plus `gate_E11.py` (`E11 GATE: PASS`, eight checks — the optics
**independently re-derived**, not imported), folded into the verifier's foundation list and absorbed into the
HTML volume as chapter **E11** (registered in `DISEASE_CHAPTERS`, so the volume's G5 firewall re-checks the
rendered page).

**Provenance (this increment):** **nothing was fetched and no γ was added.** E11 consumes only the frozen E3
optics (loaded read-only; its `run()` is `__main__`-guarded, so loading it only exposes the surface-imaging
helpers + the cited constants — the single source of the optics this chapter extends), the frozen substrate
size law, and the frozen atlas γ (read-only). `inherited/FROZEN_SHA256.json` is **unchanged** — the
foundation does not move for this increment. γ measured, never fitted; the object distances and the
power/length scalings are **inputs** expressed as dimensionless ratios, never fitted targets and never a
clinical magnitude.

**Firewall:** structure-only γ (never an optical power, a growth rate, a potency, a dose, or a clinical
effect); proposal-only / direction-only condition layer (myopia/hyperopia stated by **sign** only); **no**
power magnitude (dioptres blocked), **no** axial length (mm blocked), **no** accommodation amplitude or
near/far distance, **no** '%'. The felt percept of blur/clarity is the mind volume's.

**Next (same firewall, beyond the spine):** the much harder, multifactorial **acquired/degenerative disease
layer** (AMD, glaucoma, diabetic retinopathy) — firewalled, direction-only. Still deferred: **SIX6**
(eye-field TF), the one remaining gene in the atlas `_to_measure`, foldable by the fetch→re-freeze discipline
if a later increment needs it. The sibling **hearing** sense ships as its own seed
(`vp_ear_emergence_seed…`).
