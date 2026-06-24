# Continental-Genesis Import — what to bring into the Recent-Sequence Cascade, and why

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · https://jamming-physics.org/
**Scope.** A decision + research note: which ideas from the separate `vp_continental_genesis`
volume to **inherit** into the Recent-Sequence Cascade, graded under the same firewall, plus
the reproducible artifact that turns them into a gated module (**M45**). The Continental
volume is *not* modified; this is additive, append-only, and inherits its **verified** objects
the same way the cascade inherits its engine bundle (re-run, not taken on faith).
**Motto:** 반증 = 발견.

---

## 0. The problem this serves (be precise)

After M33–M44 the cascade has exactly **one** genuine open frontier (HANDOVER §6):

> Are the source rocks, salt, and rifting **causally** part of the same recent relaxation as
> the (provably recent, M44) deglaciation — or coincidentally a separate deep-time history?

with two sub-parts the handover names:
1. **Causal vs coincidental coupling** — the 8-fold present-tense convergence makes eight
   independent coincidences implausible, but does not yet *prove* a single cause.
2. **"Slow now ≠ slow-always-old"** — present-day slow rates (Atlantic spreading ~2 cm/yr)
   *could* be the decaying tail of a recent fast event (the same fast-onset/slow-tail shape
   M44 proves for the ice).

The Continental-Genesis volume was built to answer a *different* question (why dry land
exists), but in doing so it derived three **present-tense, chronology-free** results that bear
directly on both sub-parts. Those — and only those — are what to import.

---

## 1. The decision: THREE ideas to inherit (+ one application)

| # | Inherit | Source (CG-ID / module) | What it is | Why it serves §6 |
|---|---|---|---|---|
| **I-1** | **The conservation identity** | **CG-30 / M15** | On a fixed-area sphere, an opening **forces** an equal antipodal closing: `dA_open + dA_close = 0`. An **identity**, **rate-free** [F]. | Gives the coupling a **first-principles cause** (sub-part 1) and the magnitude co-variation (P5/SH-20/C-2) a **conservation backbone**: open area == close area, *forced* — not just an empirical correlation. |
| **I-2** | **The jammed-Maxwell substrate** | **CG-26 / M11** | The mantle is a **jammed solid near unjamming** (the R19 switch): solid on seismic seconds (S-waves), fluid on Myr (convection) — a Maxwell-time medium. | Supplies the **mechanism** for "fast-onset / slow-tail" (sub-part 2): a relaxing medium, not a steadily-flowing one. Same `c²=B/ρ` substrate as the whole VP corpus. |
| **I-3** | **The forced-convection loop** | **CG-36 / M20** | A hot fluid sphere **must** convect (Ra ≫ crit); mass conservation forces **both** an upwelling and a downwelling limb. The rift **is** one limb; the convergence is its antipode. | Turns the coupling from "coincidence of independent processes" into "**one forced cell, one relaxation**" — the causal frame sub-part 1 needs. |
| **I-4** | *(application)* **Magnitude co-variation backbone** | I-1 applied to **M39** | M39 *observed* salt ∝ extension (r≈+0.97). Conservation **upgrades** this to "co-variation with a first-principles reason." | The C-2 / SH-20 discriminator gains the backbone it lacked; graded **[L]** (coherence, degenerate as a discriminator). |

These four are the import. Everything else in the Continental volume stays in the Continental
volume.

---

## 2. The research result (what the import actually buys, computed)

The reproducible module **M45** (`m45_continental_inheritance_conservation_relaxation.py`,
gate `a909856236fff33968baee088330750eb4df268b3f20c1829ad4ea32df88c363`, pure stdlib,
SEED=19) makes each import quantitative and present-tense:

**[1] Conservation identity — rate-free [F] + present-tense [V].**
On the real sphere (A = 4πR² = 5.101×10¹⁴ m², matching CG-30), the Atlantic basin (~20% of
the surface, ~1.02×10⁸ km²) **must** be balanced by an equal antipodal closing. And the
**present-day** global plate circuit *is* observed to close: ridge area-production
(~3 km²/yr) ≈ subduction consumption (~3 km²/yr), ratio ≈ 1.00. The balance holds at **any**
spreading rate (1/2/5/10 cm/yr) — it is **v-independent**. So "one motion, two ledgers" is
true on the present Earth **without any date**, and the magnitude co-variation gets a
conservation backbone: opening area == closing area, forced.

**[2] The relaxation-tail degeneracy — the firewall, made rigorous [F].**
The Maxwell time τ = η/μ ≈ 488 yr (η = 10²¹ Pa·s, μ = 6.5×10¹⁰ Pa): solid on seismic seconds
(τ/1 s ≈ 1.5×10¹⁰ → passes S-waves), fluid on Myr (τ/1 Myr ≈ 5×10⁻⁴ → convects). The
inherited rupture engine moves by **stick-slip** (peak slip 0.5 m/s vs apparent 2 cm/yr →
duty cycle ≈ 1.3×10⁻⁹: the apparent slow rate is sparse fast slip, time-averaged). Then the
**core result**: given only a present rate `v_now` and a decaying history `v(t)=v0·exp(-t/T)`,
the relation `v_now = v0·exp(-t_now/T)` is **one equation in two unknowns** → a **one-parameter
family for every T**. A single present-rate measurement is therefore **informationally
insufficient to date the event**. "Slow now" fits **both** a slow-old process **and** a
recent-fast event with a decaying tail. Present rate **[V]**; inferred age **[O] both ways**.
**This defends the two-edged firewall — it does not smuggle "recent."**

**[3] One-substrate consistency with M44 — present-tense [V] / age [O].**
The **same** mantle viscosity (η = 10²¹) sets **two** relaxation modes of the **same** jammed
solid: M44's flexural (load) τ ≈ 4,100 yr and the Maxwell (shear) τ ≈ 488 yr. So the
ice-rebound clock (M44) and the opening's shear relaxation are one substrate, two modes.
**Honest asymmetry, kept:** M44 earns recency for the *ice* from an **observed incompleteness**
(rebound is still going **today**); spreading has **no** analogous present-tense incompleteness
datum here, so its absolute age stays **[O]**. The import gives a **causal frame**, not a date
for the rift.

**[4] The cascade payoff — graded honestly [L].**
M39's observed salt ∝ extension is upgraded by conservation from "empirical co-variation" to
"co-variation with a first-principles reason" (one conserved opening → one accommodation
budget → the petroleum-suite magnitudes co-vary). This is the backbone C-2 / SH-20 lacked.
**[L]** — it strengthens *internal* coherence; it is **degenerate** as a discriminator
(mainstream also expects salt at high-extension margins), exactly as Continental grades its
own CG-22/CG-24 ("worth is internal unification, not a new discriminator").

---

## 3. New sub-hypotheses (append-only; continue the register past SH-61)

> Numbering note: the handover's explicitly-numbered register ends at **SH-61** (M39); M40–M44
> are un-numbered. These take the next free block **SH-62…SH-65**; if M40–M44 are later
> numbered they precede these. Final numbering is the author's call on integration.

| ID | Sub-hypothesis | Grade |
|---|---|---|
| **SH-62** | On a fixed-area sphere an opening **forces** an equal antipodal closing (`dA_open+dA_close=0`, rate-free); the present global plate circuit is observed to close (ridge≈subduction) | **[F]** identity / **[V]** present-tense closure · M45 (inherits CG-30) |
| **SH-63** | A single present rate cannot date the event: `v_now=v0·exp(-t/T)` is one equation in two unknowns → "slow now" is consistent with slow-old **and** recent-fast-with-tail; age **[O] both ways** | **[F]** — defends the two-edged firewall · M45 (inherits CG-26 + engine stick-slip) |
| **SH-64** | The same jammed mantle (one η) sets M44's flexural clock and the opening's Maxwell clock — one substrate, two modes; spreading recency is **not** claimed (no incompleteness datum) | **[V]** substrate / **[O]** spreading age · M45 (inherits CG-26, CG-36) |
| **SH-65** | Conservation gives the petroleum-suite magnitude co-variation (M39 salt ∝ extension) a first-principles backbone for P5 / SH-20 / C-2 | **[L]** coherence; degenerate as discriminator · M45 (CG-30 applied to M39) |

---

## 4. What is NOT imported (the firewall guard — this is the important half)

The discipline that makes the import legitimate is what it **refuses** to take:

1. **No rate / timing / order.** Continental holds its own magnitude/rate/order **[O] both
   ways** (CG-18/19/21). The import takes only the **rate-free** identity (I-1), the
   **present-tense** substrate property (I-2), and the **forced** loop topology (I-3) — never
   a number for "how fast" or "how recent."
2. **No spreading-recency.** The honest asymmetry in §2[3] is load-bearing: M44 gets ice
   recency from an *observed incompleteness*; the import does **not** manufacture an analogous
   claim for spreading. §6's absolute-timing question stays **open** — now sharpened, not
   answered.
3. **Continental's own M14 lesson is inherited too.** Its self-audit found that importing a
   dataset's *chronological reading* as present-tense fact was the cardinal breach. The import
   strips every borrowed result to its present-tense / conservation core before it bears any
   weight.
4. **Continental's R2 identity is preserved.** Continental concludes (CG-36/R2) that VP is the
   **`c²=B/ρ` foundation beneath mantle convection, not a competitor** to it. So these imports
   strengthen the cascade's coherence and its causal frame; they do **not** claim to beat
   mainstream tectonics, and the coupling-discriminator (I-4) is graded **[L]/degenerate**
   accordingly. No "explains everything" overreach (the Continental PUZZLE_MAP's explicit
   warning).

---

## 5. Net effect on the cascade (honest)

The import **sharpens** §6 without closing it:

- **Sub-part 1 (causal vs coincidental):** upgraded from "8 coincidences are implausible" to
  "the rift **is** one limb of one forced convection cell, and its magnitude is conservation-
  locked to the antipodal closing" — a **causal frame** [F]/[L], not a proof of occurrence.
- **Sub-part 2 ("slow now ≠ old"):** upgraded from a verbal analogy to a **rigorous [F]
  result** — a present rate is informationally insufficient to date the event, so the firewall
  correctly holds spreading-age **[O] both ways**. This is a *defense* of the firewall, which
  is the honest win, not a recency claim.
- **The discriminator (C-2 / SH-20):** gains its missing **conservation backbone** [L].

Nothing here promotes occurrence above **[O]**, and the one genuine residual — an
*incompleteness* observable for spreading analogous to M44's ongoing rebound — is named, not
papered over. That is reserved for the author's insight, exactly where §6 left it.

**Bottom line.** Bring in three things — the **rate-free conservation identity** (CG-30), the
**jammed-Maxwell substrate** (CG-26), and the **forced-convection loop** (CG-36) — plus their
one application to the petroleum magnitude co-variation. They give the cascade a causal frame
and a rigorous two-edged-firewall result, both present-tense and chronology-free, reproduced
under a double-SHA-256 gate (M45). They prove neither occurrence nor recency. 반증 = 발견.
