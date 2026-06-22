# START HERE — increment E4 (the goal)

The fourth emergence and the **goal of this seed** (see `BLUEPRINT.md` for the full plan).
**BUILT (v0.6.0).**

**Scope — theoretical, NON-CLINICAL (binding, above the task).** Purely academic dynamical-systems
research. It does **not** diagnose, treat, prescribe, screen, or triage; it designs **no** molecule
and states **no** dose, potency, selectivity, or efficacy. The congenital-blindness layer is
**direction-only** and **proposal-only**, behind a **machine-checked magnitude firewall** (`run.py`'s
`main()` asserts the entire output carries no quantitative clinical token, and `gate_E4.py` re-asserts
it). The felt percept of sight is deferred to the **mind** volume.

**Task:** read each congenital-blindness master gene — **GUCY2D** (LCA1), **RPE65** (LCA2), **AIPL1**
(LCA4), **RPGR** (X-linked RP), **PDE6B** (RP), **CNGB3** (achromatopsia), every γ **measured** from
NCBI — from the FROZEN R19 substrate as one shared **failure mode**: a loss-of-function lesion means
the effective drive to the transduction switch can no longer clear the switch's own threshold
`h* = spinodal(γ)`, so the all-or-none flip established in **E2** never fires — no transduction. E4 is
the E2 single-photon switch **read in reverse**.

**Why this framing (the productive path):** E2 showed one quantum of drive across the spinodal flips
the switch all-or-none. E4 reads the same fold from the other side — when the drive **cannot** clear
`h*`, the dark basin is the only basin and the switch is stuck dark. The disease and its cure-direction
fall out of the same saddle-node, with no new dynamics and nothing fitted.

**Deliverable (done):** a deterministic module `research/E4-congenital-blindness/run.py` that
(A) settles the FROZEN field from the dark rest basin for all six genes — a clearing drive (1.15·h*)
flips it on (transduction, = E2); the LOF-attenuated drive (0.85·h*) leaves it dark (cannot flip) —
the only difference being whether the drive clears `h*`, with a sharp all-or-none threshold shown on
GUCY2D; (B) the **substrate-inverse lever**, direction-only: because the flip condition is exactly
`drive ≥ h*(γ)`, its inverse has two directions — **(i)** raise the effective drive back across `h*`
(demonstrated: re-supplying drive re-flips, only past `h*`), or **(ii)** lower the effective threshold
below the residual drive (demonstrated with a hypothetical threshold probe; the measured γ is never
altered) — stating only the directions, every magnitude a firewall-blocked **[O]**; (C) ranks the six
switches by `spinodal(γ)` (a **structural** fragility / rescue-direction ordering, explicitly **not** a
clinical severity claim), reports honestly that the six γ are **all distinct at 3dp** (no tie to break
here) yet each carries non-trivial **A4 SHAPE** and the closest-γ pair is A4-separated (read γ AND A4,
per DNA v1.13), and states the brutal caveat outright — the measured γ is the **promoter** stiffness,
while almost every blindness lesion is **coding/downstream**, so γ is the switch's threshold **context**,
not the lesion site (a named **[O]**). It prints every displayed number, self-hashes (2× run →
identical sha256), passes the magnitude firewall, and declares grades [F]/[V]/[L]/[O] honestly. Plus
`gate_E4.py` (`E4 GATE: PASS`, eight checks incl. the firewall), folded into the verifier's foundation
list.

**Provenance (this increment):** the three deferred genes **AIPL1, RPGR, PDE6B** were fetched with
`tools/fetch_promoter_gamma.py` (measured γ = −mean SantaLucia-1998 NN ΔG37, TSS−2000..+500), folded
into `inherited/eye_promoters.cache.json` and `inherited/organ_gamma.json`, and those two inherited
artifacts were **deliberately re-frozen** in `inherited/FROZEN_SHA256.json` (logged in
`INHERITANCE_LEDGER.md`) — the only sanctioned way the foundation changes. The substrate, the wave
modules, the DNA grammar, and the reading are all untouched. γ measured, never fitted.

**Firewall:** structure-only γ (never a channel voltage, gain, current, potency, dose, selectivity, or
clinical effect); the order parameter s is the abstract R19 field, not a photocurrent/voltage/firing
rate; the disease layer is direction-only / proposal-only and machine-checked; the felt percept of
sight is the mind volume's.

**Next:** grow the seed into the full multi-chapter HTML volume (VP-SPEC v1.8 §6) — E0→E4 with every
displayed number reproduced deterministically (2×sha256, HTML↔code drift 0), the disease layer
proposal-only under the firewall, `verify_seed.py` green — delivered, as always, as **one zip**. The
remaining deferred gene **SIX6** (eye-field TF) can be folded by the same fetch→re-freeze discipline if
a later increment needs it. The sibling **hearing** sense ships as its own seed (`vp_ear_emergence_seed…`).
