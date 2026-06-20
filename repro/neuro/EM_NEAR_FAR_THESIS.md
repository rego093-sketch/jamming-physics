# EM_NEAR_FAR_THESIS — the locked thesis on electromagnetism in neural signalling

**Status:** LOCKED · settled by measurement, not preference.
**Scope:** single source of truth for **both** papers — `neuro` (the verified substrate) and
`mind` (felt cognition). `neuro` §9 and `mind` §2 are read under this file.
**Enforced by:** `verify_em_thesis.py` (deterministic gate; pins *both* boundaries).
**Author:** Young Jae Lee · governed by VP-SPEC C1 (every constant is a measured input or a
derived value — never chosen to hit a target).

---

## 0. The one-line lock (read this first)

An electrical signal **is** electromagnetic (Maxwell). What is retired is **not "EM"** — it is
exactly **one form** of it: the **radiative far-field / optical-fibre (TIR) carrier**. The
**near-field / conduction (ephaptic)** form is **affirmed and load-bearing**, measured at the
ephaptic threshold in `neuro` §19.

> **The word "EM" must never appear as a blanket retired item, anywhere, under any name.**
> Retirement applies to the radiative far-field carrier **only**.

This is the bright line that stops the recurring drift toward "retire EM." The collision that
blocks progress comes from one source: writing "EM" where the precise object is "the radiative
far-field carrier." Fix the word, and the conflict dissolves — `neuro` §18/§19 and `mind` §4
stop contradicting `neuro` §9.

---

## 1. One physics, two regimes (why "electrical" and "EM" are not two things)

A neuron firing is ions (Na⁺/K⁺) crossing the membrane = charge moving = current. By Maxwell,
a time-varying current **necessarily** produces an electromagnetic field. EEG measures its
electric potential; MEG measures its magnetic field. The neuron does not *fail* to make an EM
field — it **cannot help** making one. (The chemistry chapter §1 states the same identity:
electricity, a radio wave and a γ-ray "differ only by an angle" — one medium, one motion seen
two ways.)

The **same** field appears in two regimes, and the entire question turns on which one:

| regime / object | character | falls off | role |
|---|---|---|---|
| **near-field (A) — cable conduction (the spike)** (χ→0, guided along the axon) | internal ionic current, wire-like (λ_cable ≈ 1.6 mm) | — (guided) | **carries the signal** (the labelled line) |
| **near-field (B) — ephaptic field (the coupling)** (χ→0, volume-conducted) | reactive, local | 1/r²–1/r³ | **couples neighbours (ephaptic)** |
| **far-field** (χ→90°, transverse, radiative) | propagating, broadcast | 1/r | would carry information at distance — **retired** |

"Electrical signal vs EM" is the wrong axis. The real axis is **near-field vs far-field** — and,
within the near-field, **cable conduction (A) vs ephaptic coupling (B)** (see §1.1).

### 1.1 The χ→0 near-field is TWO objects, not one (disambiguation)

"Near-field" names a *regime* (χ→0, non-radiative), **not a single object.** Inside it sit two
physically distinct things, and conflating them is the source of the recurring confusion:

- **(A) cable conduction — the spike / the signal.** The ionic current flowing *along* the axon
  (internal, wire-like, λ_cable ≈ 1.6 mm), self-regenerating as a reaction-diffusion front; it
  carries the content. It advances at the **conduction velocity 0.5–120 m/s = the membrane-charging
  / front rate** — not light, not the field's c, and not particle transport (the front moves; ions
  drift only locally, electrons carry nothing).
- **(B) ephaptic near-field — the coupling.** The extracellular field that current (A) *sources*
  (1/r³, nearest-neighbour-dominated), which couples to neighbours; measured at threshold
  (ΔVm = 0.2748 mV, §2). Its field disturbance is c-instant; its *pattern* tracks the slow ions.

Both are χ→0; neither is the retired far-field. When this file or either paper writes "near-field"
it means the *regime* — the **object** must be named (A) or (B). Full controlled vocabulary and the
three-speeds rule: `TERMINOLOGY_canonical.md` (shared SSOT companion to this file).

### 1.2 The two registers — the object layer (`neuro`) and the brainwave abstraction (`mind`)

The disambiguation above (A/B, the angle χ, the three speeds) is the **object layer**: the
precise physics of *which* field, measured and bounded. It is **owned by `neuro`** and used there
in full. `mind` does **not** re-run it — `mind` rides one **abstraction** built on top of it and
**cites** `neuro` for every object and every number. This is the seam where the two papers stopped
agreeing; naming the register fixes it.

**The abstraction `mind` uses — "the EM brainwave."** In the cognition papers, "EM" in the
signalling context names exactly one thing: **the brainwave = the low-frequency (1–100 Hz, δ/θ/γ)
brain field** — the field the synchronous ionic populations source, the thing an EEG/MEG reads.
Its **job is timing** (it gates *when* a receiving assembly is excitable —
communication-through-coherence), **not** carrying content; the **content carrier is named** — the
ion spike + synaptic current (object A, `neuro` §13/§15). The working identity, stated once for
both papers:

> **EM = the brainwave = the low-frequency (δ/θ/γ) field.**

Read precisely, so it can never collapse the three speeds (`TERMINOLOGY_canonical.md` §2):
- **"low-frequency" is the rhythm / source rate** — the band the *source* reconfigures at
  (1–100 Hz), the EEG band. It is **not a velocity.** The field itself is still **`c`-instant**;
  only the field's *pattern* rotates at this slow rate.
- It is the **χ→0 near-field's pattern** (object B's field), **not** a new object and **emphatically
  not** the retired high-frequency optical / radiative far-field carrier (§3).

**Division of labour (so the two papers stop colliding):**
- `neuro` **owns** the object layer: cable conduction (A), ephaptic near-field (B), the far-field
  (retired), the three speeds, the angle law, and the measured numbers (ΔVm ≈ 0.27 mV; radiated
  fraction ~10⁻¹⁵; conduction 0.5–120 m/s, ~10⁶× below light).
- `mind` **owns** the abstraction: "the EM brainwave," its CTC timing role, the eddy/stream
  reading — and **cites** `neuro`'s objects with their status tags. `mind` does **not** restate
  `neuro`'s derivations as its own (no re-deriving ΔVm, the radiated fraction, or the velocity
  ratio in `mind` prose — cite `neuro` §18/§19). `mind`'s *own* emerged numbers (front speed = `c`,
  classical coherence ≈ 0.998, θ/γ ≈ 6.1) are `mind`'s and stay.

Full ownership map and the per-paper register rules: `TERMINOLOGY_canonical.md` §7.

---

## 2. AFFIRMED — the near-field / conduction (ephaptic) form  `[V]`

- The ionic current's **local quasi-static field** directly shifts the membrane potential of
  nearby cells (ephaptic coupling).
- **Measured at threshold** (`neuro` §19): the measured cortical field
  *E* = 2.29 mV/mm (Fröhlich & McCormick 2010) × measured sensitivity *s* = 0.12 mV per mV/mm
  (Bikson 2004) gives a derived **ΔVm = 0.2748 mV**, **contained** in the independently
  measured bound **< 0.5 mV** (Anastassiou 2011). The field is **at** the entrainment threshold
  (ratio ≈ 1) — **not below it**. The near-field is real and non-negligible.
- **Biology demonstrably uses the near-field form**: weakly-electric fish run frequency-division
  electrocommunication with a jamming-avoidance response (verified in
  `repro/neuro/_inherited/vp_electrocommunication.py`; ~10⁻¹⁴ cross-talk).
- **The observed current is this form.** Nerve current measured in the lab is the **ionic cable
  current** flowing internally; cable-theory space constant **λ_cable ≈ 1.6 mm** (it flows
  internally, like a leaky wire). That same ionic current is the **source** of the near-field.
  Chain: observed current (internal, wire-like) → near-field (local, ephaptic, **measured**) →
  far-field radiation ≈ 0. One consistent line.

---

## 3. RETIRED — the radiative far-field / optical-fibre (TIR) carrier  `[F]` (by measurement)

Retired because three independent measurements forbid it — none of which may be silently
re-decided:

1. **Non-radiation (not reflection).** The brain is far smaller than the wavelength
   (r/(λ/2π) ≈ 10⁻⁸ at EEG bands), so the **radiated fraction ≈ 10⁻¹⁵–10⁻¹⁶** (`neuro` §18).
   The propagating wave essentially never forms; the energy stays reactive in the near-field.
   This is *non-radiation*, a different mechanism from reflection.
2. **Transparency.** At EEG wavelengths the tissue thickness is ≪ skin depth
   (head/δ ≈ 10⁻³), so a far-field wave would **pass through** tissue, not reflect off it.
   Reflection cannot be the container; non-radiation already is. (Tissue *does* reflect/scatter
   at **optical** wavelengths — white matter looks white because myelin scatters visible light —
   but that is the short-λ regime, not the EEG far-field.)
3. **Conduction velocity.** Measured nerve conduction is **0.5–120 m/s**; light in tissue is
   ~**2×10⁸ m/s** — a **10⁶–10⁸×** mismatch. A waveguided/optical-fibre EM carrier would travel
   near light speed. It does not; the signal is ionic cable conduction.

The only **named** entity that stays forbidden is the **"consciousness vortex field"** / a
**quantum** carrier (the ~10⁹× coherence-length shortfall is the *quantum* decoherence case
only; it never described the classical near-field).

---

## 4. OPEN — deferred to `mind`

Whether cognition **functionally uses** the (measured, at-threshold) near-field/ephaptic
coupling. Decisive test (named in `neuro` §9/§19): a **behaviour-labelled intracranial recording
with the local endogenous field cancelled vs. augmented** in real time.

> **The open variable is FUNCTION, not STRENGTH.** Strength is *measured* (`neuro` §19: at
> threshold). Do **not** re-open "is the field strong enough" — that is answered. "Weak"
> describes the **scalp** EEG (µV, volume-conducted) **only**; the **local** near-field is at
> threshold.

---

## 5. Anti-drift lock (read before editing either paper, or summarising this work)

1. "EM" alone is **never** retired. The retired object is the **radiative far-field / TIR
   carrier**, named in full every time.
2. The **near-field / ephaptic** form is **affirmed by measurement** (`neuro` §19). It is
   load-bearing, not a hedge.
3. To retire EM wholesale, **or** to revive the far-field broadcast, you must first **overturn
   one of the three measurements in §3** (radiated fraction, transparency, conduction velocity)
   or the §2 ephaptic-threshold measurement. None may be paraphrased away or dropped from a
   summary.
4. Any chapter's **answer/abstract** (the part that gets summarised first) must carry the
   precise object ("radiative EM carrier"), never the blanket word "EM" — because the headline
   is what propagates.
5. Run `verify_em_thesis.py` after **any** edit touching the EM question. It asserts **both**
   boundaries (near-field affirmed AND far-field retired). If it fails, the edit drifted —
   revert, do not paper over.

---

### Citations (load-bearing, locked)
- Fröhlich F. & McCormick D.A. (2010) *Neuron* 67:129–143 — endogenous field |avg| 2.29 mV/mm.
- Bikson M. et al. (2004) *J Physiol* 557:175–190 — field sensitivity 0.12 mV per mV/mm.
- Anastassiou C.A. et al. (2011) *Nat Neurosci* 14:217–223 — ephaptic ΔVm bound < 0.5 mV.
- `neuro` §18 (`vp_em_brain_circulation.py`) — sub-wavelength radiated fraction ~10⁻¹⁶.
- `neuro` §19 (`vp_em_ephaptic_threshold.py`) — derived ΔVm 0.2748 mV, at threshold.
- Conduction velocity 0.5–120 m/s vs light ~2×10⁸ m/s — standard neurophysiology.
