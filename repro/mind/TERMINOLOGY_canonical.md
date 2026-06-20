# TERMINOLOGY_canonical — the single source of truth for the words that keep drifting

**Status:** LOCKED · a controlled vocabulary, not prose. Settled by physics, not preference.
**Scope:** governs how `neuro` (and, mirrored, `mind`) name **spikes, fields, conduction, and
the emergence of light**. Read alongside `EM_NEAR_FAR_THESIS.md` (the physics lock) — this file
fixes the *words*; that file fixes the *measurements*.
**Enforced by:** `verify_terminology.py` (deterministic regression guard: the banned phrases of
§5 must stay absent; the canonical objects of §1 must stay present).
**Author:** Young Jae Lee · governed by VP-SPEC C1 (every term maps to a measured or derived
physical object — a term that names nothing physical is a bug, not a style).

> **Why this file exists.** One word — "near-field" — was doing the work of **two different
> physical objects**, and three different **speeds** were being collapsed into one. That single
> overload is the whole reason the EM question feels slippery and the same confusion returns
> every session. Fix the words once, here, and the slipperiness is gone. When in doubt about any
> term below, this file is the authority; align the chapter to it, never the reverse.

---

## 0. The one principle everything hangs on

There is **one** electromagnetic phenomenon, ordered by a single **propagation angle χ**
(angle law `sinχ = λ/(mD)`, `D = 2λ_C,e = 4.852620 pm`). Conduction and radiation are **not two
things** — they are the `χ→0` and `χ→90°` limits of the same object. So:

- A nerve signal **is** electromagnetic. Not "electrical, and separately EM" — the membrane
  voltage **is** an E-field; the ionic current **is** a current that sources E and B. (Measured:
  EEG = its E-field, MEG = its B-field. You cannot measure a magnetic field from a non-EM thing.)
- "**EM** vs electrical" is a non-question. The real axis is **`χ→0` (near-field) vs `χ→90°`
  (far-field)**, and inside `χ→0` there are **two distinct objects** (§1). Name the object, never
  just the regime.

---

## 1. THE DISAMBIGUATION — `χ→0` (near-field) is **two** objects, not one

This is the core of the file. The non-radiative `χ→0` regime contains **two physically distinct
objects with different geometry, strength, and job.** "Near-field" alone names neither — it names
the *regime they share*. Always say which object.

| symbol | canonical name | geometry | what it is | role | speed it moves at | strength |
|---|---|---|---|---|---|---|
| **(A)** | **cable conduction** — *the spike / the signal* | **guided, along the axon** (internal) | the self-regenerating transmembrane-voltage transient; the ionic cable current (space constant `λ_cable ≈ 1.6 mm`, flows internally like a leaky wire) | **carries the content** (the labelled line) | **conduction velocity 0.5–120 m/s** = the membrane-charging / reaction-diffusion *front* rate (§2) — **not** light, **not** the field's `c` | full signal |
| **(B)** | **ephaptic near-field** — *the coupling* | **volume-conducted, through tissue, to neighbours** | the extracellular near-field that current (A) **sources**; the `1/r³`, nearest-neighbour-dominated field | **couples neighbours** (may bias their spike timing) | the field **disturbance** propagates at **`c`** (crosses the brain in ~`3.4×10⁻⁹` of a cycle); its **pattern** rotates at the slow ionic rate | at the **measured threshold** `ΔVm = 0.2748 mV` (`neuro` §19) — real, not negligible, but small |
| **(C)** | **radiative far-field / TIR carrier** — *RETIRED* | broadcast, transverse | a propagating wave that would carry information at a distance | would broadcast | `c` | **≈ 0** (radiated fraction `~10⁻¹⁵–10⁻¹⁶`) — **retired by measurement** (§3 of the thesis) |

**Read this twice.** (A) is the **signal**: it goes where the wire goes, it is strong, and it
moves at the slow **front** rate. (B) is the **coupling**: it is the field that (A) emits into the
surrounding tissue, it is weak (at threshold), and the field itself is `c`-fast while its *pattern*
is slow. (C) is **gone**. The recurring error is using "near-field" for (A) when you mean the
signal, or for (B) when you mean the coupling, as if they were the same — they are not.

> **One-line test before writing "near-field":** *do I mean the spike travelling down the axon
> (A), or the field leaking to neighbours (B)?* If you can't answer, you don't yet know what you
> are claiming. Write (A) as **"cable conduction (the spike)"** and (B) as **"ephaptic near-field
> (the coupling)."**

---

## 2. THE THREE SPEEDS — never collapse them into one

A second overload: **three different speeds** were all being called, loosely, "fast" or "the
conduction speed." They are not the same number and not the same kind of thing.

| speed | symbol / value | what it is the speed *of* | what it is **not** |
|---|---|---|---|
| **field propagation** | `c ≈ 2×10⁸ m/s` (in tissue, `c/n`) | the EM field disturbance crossing the brain (object B's field, and any far-field) | not the signal; not anything a particle does |
| **signal conduction** | **0.5–120 m/s** | the **spike** advancing along the axon (object A) — the **membrane-charging / reaction-diffusion front** rate | **not** light; **not** ion transport; **not** electron transport (see §3) |
| **rhythm / source rate** | **1–100 Hz** | how fast the source *reconfigures* (the EEG band; the `f = 1/2πτ` corner of the membrane/circuit time constant) | not a velocity at all — a **rate** (Hz), not m/s. Comparing it to `c` is a category error |

**Therefore:** "the brain is slow" is about the **rhythm/source rate** (Hz) — the electrochemistry.
The **field** is `c`-instant. The **spike** moves at the front rate. Three clocks, three jobs.

---

## 3. WHAT A SPIKE *IS* (its physical substance, so it is never mis-said again)

A spike is a **self-regenerating transmembrane-voltage transient.** Two true statements at once:

- **As a field (configuration):** it is a real E-field — ~`100 mV` across a ~`5 nm` membrane is
  `E ≈ 2×10⁷ V/m`, an enormous local field — plus a tiny B from the ionic current. It is `χ→0`
  near-field (radiated fraction `~10⁻¹⁶`); it is **not** a free, radiating wave. Measured halves:
  **EEG = its E-field, MEG = its B-field.**
- **As propagation (travel):** **nothing is transported along the axon.** Each membrane patch
  re-fires from **its own** ionic gradient and triggers the next — a **reaction-diffusion front**
  (the engine's R19 bistable switch). The cable equation has **no transport term**, yet a pulse
  propagates; so the speed is a **front velocity `√(D/τ)`**, not a particle velocity.
  - Ions drift only **locally, across** the membrane (~`nm`), at `µm/s–mm/s` — never **along** the
    axon at metres/second.
  - Electrons carry **nothing** — axoplasm has no metallic conduction band. An electron-current
    axon would be fiction.

So: **a spike is EM in its fields and a reaction-diffusion front in its travel.** That is the
whole of it. It is object (A) of §1.

---

## 4. THE EMERGENCE OF LIGHT (the hard concept, stated plainly)

Light is **not a separate substance from the EM above** — it is the **`χ→90°` (high-angle) limit**
of the same one phenomenon (§0). It "emerges by **angle**": with `sinχ = λ/(mD)`, `m = ⌈λ/D⌉`,

- a γ-ray sits at `χ→0°` (the **conduction-like** end — this is why a spike and a γ-ray are *the
  same kind of thing at different angles*),
- a radio wave sits at `χ→90°` (the broadcast end),
- **visible light** sits at `χ ≈ 89.8°–89.9°` — a narrow high-angle band.

The eye separates **colour by this angle**: different wavelengths arrive at slightly different `χ`,
and the cone array (whose pigments are set by the opsin genes — §12) reads each. **But the light's
own carrier stops at the photoreceptor:**

1. Light is **guided to** the photoreceptors inside the eye (Müller glia act as light pipes) —
   real biological light-guiding, but only *up to* transduction.
2. At the photoreceptor the light is **absorbed** — its optical frequency (`~10¹³–10¹⁴ Hz`) is
   **down-converted** to the neural band, and the optical **phase is discarded** (incoherent
   detection). Colour survives as **which cone absorbed it** (a channel identity), not as optical
   phase.
3. From there onward the message is a **spike** — object (A), `χ→0` cable conduction — **not
   light.** No lossless re-up-conversion exists, so the lowered state is **maintained and sent**,
   not reconverted.

**So "light emerges" never means "light travels to the brain."** Light emerges (by angle) in the
world and reaches the eye; the **spike** carries it from the eye onward.

---

## 5. BANNED → USE INSTEAD (the regression table `verify_terminology.py` guards)

Left column = the confusing/non-physical phrasings that caused the recurring drift. Right column =
the required replacement. The banned forms must not reappear in chapter bodies.

| ✗ banned / confusing | ✓ use instead | why |
|---|---|---|
| "near-field" used **alone** for the **signal** | **"cable conduction (the spike)"** / "`χ→0` guided conduction" | (A)≠(B); name the object (§1) |
| "near-field" used **alone** for the **coupling** | **"ephaptic near-field (the coupling)"** | name the object (§1) |
| conduction "**speeds toward `c`**" / "toward light speed" (e.g. myelin) | **"speeds it up, though still ≪ `c` (≤120 m/s)"** | fastest nerve is `~10⁶×` below `c`; never approaches it (§2) |
| "the field **circulates at the conduction speed**" | **"the field propagates at `c`; its *pattern* rotates at the slow ionic rate"** | conflates field speed with pattern rate (§2) |
| "**ions / electrons move** at the conduction velocity" | **"the state-transition *front* moves at conduction velocity; ions drift only locally, electrons carry nothing"** | the velocity is a front, not transport (§3) |
| "the spike **travels / is carried** [as transport]" | **"the spike propagates as a reaction-diffusion front"** | no transport term exists (§3) |
| "**EM carrier**" (unqualified) | **"`χ→0` conduction"** (kept) **or** **"radiative far-field carrier"** (retired) | "EM" is never retired wholesale (§0; thesis §0) |
| "the brain is too **slow** for EM" | **"the *rhythm rate* (Hz) is slow; the *field* is `c`-instant"** | three speeds, not one (§2) |

**Mind-register rows** (apply to `mind` chapter bodies — the abstraction layer; see §7):

| ✗ banned (in `mind` prose) | ✓ use instead | why |
|---|---|---|
| restating `neuro`'s **ΔVm / radiated fraction / velocity ratio** as a `mind` result | **cite** "`neuro` §18/§19 `[V]`" | the object layer is `neuro`'s; `mind` cites (§7) |
| bare "**near-field**" as a single object in `mind` | "the **EM brainwave** (the low-frequency field)" **or** cite object A/B by reference | `mind` rides the abstraction, not the object (§7.1) |
| "the field is **weak**" (unqualified) in `mind` | "the **local** near-field is **at threshold** (`neuro` §19); 'weak' is the **scalp** EEG only" | strength is *measured*; the open variable is **function** (thesis §4) |

---

## 6. Cross-references (where each object is built and measured)

- `EM_NEAR_FAR_THESIS.md` — the physics lock (objects A/B affirmed, C retired); §1.1 carries this
  same disambiguation in brief.
- `neuro` §2 (`02-substrate-neuron-switch`) — the R19 switch; the spike as object (A).
- `neuro` §13 (`13-em-emission-bridge`) — the momentum balance: ionic current → field.
- `neuro` §15 (`15-em-link-full`) — the `χ→0`/`χ→90°` split; "conduction velocity is the
  membrane-charging rate, not the field" (the correct statement to keep).
- `neuro` §18 (`18-em-brain-circulation`) — object (B)'s field: `1/r³`, `c`-instant disturbance,
  slow pattern; radiated fraction `~10⁻¹⁶`.
- `neuro` §19 (`19-em-ephaptic-threshold`) — object (B) measured at threshold (`ΔVm = 0.2748 mV`).
- `neuro` §10/§12 (`10-…transduction`, `12-…sensory-organ-emergence-4d`) — light reaches the eye,
  is absorbed, and becomes a spike (§4 here).

---

## 7. REGISTER & OWNERSHIP — the brainwave abstraction (`mind`) vs the object layer (`neuro`)

§1–§4 fix the **objects** (the physics). This section fixes **who uses which words**, so the two
papers — `neuro` (the verified substrate) and `mind` (felt cognition built on it) — stop drifting
into each other's register. The whole rule is one sentence: **`neuro` owns the objects; `mind`
rides one abstraction and cites `neuro` for the objects.** (Direction and packaging of the cite:
`PROJECT_BOUNDARY_neuro_mind.md`.)

### 7.1 The abstraction term `mind` uses — "the EM brainwave"

In the cognition papers, "EM" in the signalling context is **one** thing: **the brainwave = the
low-frequency (1–100 Hz, δ/θ/γ) brain field** that the synchronous ionic populations source — what
an EEG/MEG reads. Canonical identity, for both papers:

> **EM = the brainwave = the low-frequency (δ/θ/γ) field.**

Stated precisely, so §2's three speeds never collapse:
- **"low-frequency" = the rhythm / source rate (Hz)** — the band the *source* reconfigures at;
  **not a velocity.** The field is still **`c`**-instant; its *pattern* rotates at this slow rate.
- It is the **`χ→0` near-field's pattern** (object B's field, §1), **not** a new object and **not**
  the retired optical / radiative far-field carrier.
- Its **job is timing / gating** (communication-through-coherence): it sets *when* a message gets
  through; it does **not** carry the content. The **content carrier is named** — the spike
  (object A) + synaptic current.

### 7.2 Ownership map — own (use in full) vs cite (restate with a status tag)

| term / object | `neuro` (substrate) | `mind` (felt cognition) |
|---|---|---|
| **cable conduction (A) — the spike** | **OWNS** — uses in full (the signal) | names the spike as carrier; **cites** `neuro` for the object |
| **ephaptic near-field (B) — the coupling** | **OWNS** — measures it (§19) | **cites** "at threshold, ΔVm ≈ 0.27 mV `[V]`, `neuro` §19" |
| **far-field / TIR carrier (retired)** | **OWNS** the retirement (§18) | **cites** "retired, `neuro` §18" |
| **the three speeds** (`c` / 0.5–120 m/s / 1–100 Hz) | **OWNS** | uses only the rhythm rate ("low-frequency"); **cites** the rest |
| **angle law χ, χ→0, radiated fraction, velocity ratio** | **OWNS** | does **not** restate; **cites** `neuro` §15/§18 |
| **the EM brainwave** (the low-frequency field, by job) | grounds it physically (§18 = object B's pattern) | **OWNS** the abstraction — rides it as the θ/γ clock |
| **eddy, stream, CTC binding** | n/a | **OWNS** (the functional reading) |

`mind`'s **own** emerged numbers — front speed = `c`, classical coherence ≈ 0.998, θ/γ ≈ 6.1 — are
`mind`'s (its modules M1/M2/M8) and stay; they are not `neuro` citations.

### 7.3 The `mind` register rule (what to write, what not to)

- **Lead with the abstraction:** "the **EM brainwave** (the low-frequency δ/θ/γ field; carrier =
  ion spikes + synaptic currents, `neuro` §13/§15)." Ride the brainwave/timing reading.
- **Cite, do not re-derive:** any magnitude that is `neuro`'s — ΔVm, the radiated fraction, the
  velocity ratio — is **cited with its status tag**, never restated as a `mind` derivation.
- **Name the object only by reference:** if `mind` must point at A vs B, write "the near-field
  (cable conduction A / ephaptic B, per `neuro` §1.1)" and move on — do **not** re-run the
  disambiguation.
- **Never** write bare "near-field" in `mind` as if it were a single object; either say "the EM
  brainwave / the low-frequency field" (the abstraction) or cite the named object.

This is the same disambiguation as §1 and the same retirement as the thesis — only the **register**
differs: `neuro` writes the object, `mind` writes the brainwave and cites the object.

— end (canonical terminology, v1.1 — adds §7 register/ownership) —
