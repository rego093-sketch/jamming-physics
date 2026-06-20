# The main carrier — emerging the access-correlated high-frequency wave from its measured source

**Author program:** VP / Jamming-Physics (Young Jae Lee).
**Document type:** self-contained study note (portable). Companion code:
`vp_main_carrier_emergence.py` (+ `verify_main_carrier.py`), reusing the governed engine
`vp_mind_engine.py`. **Physics / observation / evidence / causality only.**

**Headline (frozen, SEED=19, 2× bit-identical):**
`8d05cfeccb9cf57c924b1b2aea3f716caaf6069f690171bf8d2fae47004b2de7` — **13/13 gate checks
PASS**, **11 invariants** locked, **zero new tuned constants**, `medium_efficacy_tested=0`,
`hard_problem_open=1`, no claim of subjective experience.

---

## 0. The forcing observation

Across states, the wave that tracks responsiveness is **not raw amplitude**: deep slow-wave
sleep carries the **largest-amplitude** delta yet is the least responsive state, while wake and
REM are **low-amplitude, high-frequency**. The amplitude reading therefore fails. What is left
once amplitude is removed is the **structured high-frequency carrier** that is present in
wake/REM and suppressed in deep SWS. This note emerges that carrier **from its measured
biological source** and characterises it as a physical object: its activity range, the state in
which it is operative, the operating window in which it carries information, and how many such
carriers run in parallel to reinstate memory. **None of this is a claim that the carrier is
experience** (§E).

## 1. The source — what SETS the carrier (made explicit, the way M14 sets the spindle)

In the engine, `Population.lfp(tau_inh)` is a relaxation oscillator whose band is set by the
**inhibitory recovery time-constant**. The carrier's source is therefore the **measured GABA_A
decay kinetics of fast-spiking interneurons** — not a free parameter:

- **τ(GABA_A) = 6.0 ms** — **[F]** Destexhe 1998 (fast GABAergic), already locked in this
  package's `synaptic_kinetics_measured` atlas (it is the same kinetic that sets the M13
  aperiodic floor).
- **inhibition decay sets the gamma period** — **[F]** Bartos, Vida & Jonas 2007 (Nat Rev
  Neurosci 8:45): in interneuron networks the GABA_A decay time-constant fixes the gamma cycle.
- **PV fast-spiking interneurons are the gamma generators, causally** — **[F]** Cardin et al.
  2009 (Nature 459:663) and Sohal et al. 2009 (Nature 459:698): optogenetic drive of PV cells
  produces gamma and gates cortical transmission.

We introduce **no new τ**. We set the existing carrier's `tau_inh` to the measured GABA_A value
and report the emergent band.

**Result [V].** carrier frequency **0.0490** > slow-reference **0.0080** (engine units), a
dimensionless ratio **6.125**. Sweeping the measured fast-GABA_A interval {3,4,6,8,10} ms gives a
**monotonic 1/τ** carrier band over **[0.034, 0.0768]** — faster inhibition, higher carrier.
**Absolute Hz stays [O]** (engine substrate units); the **1/τ relation** and the **ratio** are
the verified claims.

## 2. State selectivity — the carrier is operative only where responsiveness is present [V/I]

A drive is "operative" if it writes a **recoverable** memory (partial-cue recall above chance).

- **Structured fast carrier** (wake/REM): recall **1.000**.
- **Large UNSTRUCTURED slow drive** (deep SWS, amplitude up to 60× the carrier — the delta:gamma
  analogue, paced by the measured cortical slow-adaptation τ=600 ms / GABA_B τ=180 ms): recall
  **collapses monotonically** to **0.700** (the clamped-cue chance level).

The far smaller **structured** carrier beats the far larger **unstructured** slow drive. The
operative, memory-reaching carrier is the **activated wake/REM high-frequency** wave, not the
**large-amplitude deep-SWS** wave — **concordant [I]** with the high-vs-low complexity split of
responsive vs unresponsive states (the PCI literature; see §E for the honest negative).

## 3. The operating window is metastable — not silence, not global synchrony [V]

Recall as a function of regime is an **inverted-U**:

| regime | recall | reading |
|---|---|---|
| **silence** (sub-fold: no basin consolidated) | **0.675** | nothing written |
| **metastable** (measured structured carrier) | **1.000** | operative |
| **global-sync** (uniform field — seizure analogue) | **0.692** | information destroyed |

The **biggest / most-synchronised** field is **not** the operative carrier — globally locked
activity carries no distinguishable pattern. This is the engine's M9 partial-metastable window
(R<0.9) seen from the memory side, and it is the honesty anchor of §0 restated as a gate.

## 4. Many carriers in parallel — the slow index reinstates fast content [V/I]

Emerging the slow and fast bands together gives a parallel capacity = **floor(6.125) = 6** gamma
sub-slots per slow cycle — **within 7±2** (Lisman–Jensen theta-gamma code, **[I]**). Storing six
memories as `[slow index | fast content]` and cueing with **the index alone**:

- each content is reinstated from its own index at fidelity **1.000** (all six);
- the same read-out matches a **different** memory's content only at **cross-talk 0.497** (chance)
  — the slow index is a **specific, content-addressable address**;
- the integrated parallel drive **grows monotonically** with locked workers and **crosses the
  R19 fold (0.385)** — reusing the whitepaper's [V] unbound-vs-gathered anchors; more bound slots
  write a deeper trace.

So multiple parallel carriers do not compete into noise: a slow index binds several fast contents
and fires them back together — the mechanism of "recall brings back the whole moment."

## E. What this is, and is NOT (honesty ledger — carried, not reproduced)

- **[V]** in silico, deterministic, reusing only governed constants: the measured-source carrier
  and its 1/τ activity range; the structured-vs-unstructured state selectivity; the
  silence/metastable/global-sync inverted-U; the parallel multiplex and index→content
  reinstatement with chance-level cross-talk.
- **[I]** literature-concordant, not proof: the mapping of the structured-fast carrier onto
  wake/REM-vs-SWS responsiveness, and the 7±2 capacity.
- **[O] open:** `medium_efficacy_tested = 0`; **no in-vivo test** that biology *uses* this carrier;
  the **PCI access marker remains an HONEST NEGATIVE** (it did not robustly reproduce — carried
  from `12-open-problem`). The study reproduces the **measured source, activity range,
  state-selectivity, operating window, and parallel memory function of a high-frequency carrier**.
  It does **not** show that this carrier **is** experience. `consciousness_claim = 0`,
  `hard_problem_open = 1`, **no new tuned constant anywhere.**

---

## References (as retrieved; paraphrased)

- Destexhe A, Mainen ZF, Sejnowski TJ. *Kinetic models of synaptic transmission.* In *Methods in
  Neuronal Modeling* (1998) — fast/slow GABAergic time-constants.
- Bartos M, Vida I, Jonas P. *Synaptic mechanisms of synchronized gamma oscillations in
  inhibitory interneuron networks.* **Nat. Rev. Neurosci.** 8 (2007) 45–56.
- Cardin JA et al. *Driving fast-spiking cells induces gamma rhythm and controls sensory
  responses.* **Nature** 459 (2009) 663–667.
- Sohal VS et al. *Parvalbumin neurons and gamma rhythms enhance cortical circuit performance.*
  **Nature** 459 (2009) 698–702.
- Lisman JE, Jensen O. *The theta-gamma neural code.* **Neuron** 77 (2013) 1002–1016.
- Steriade M, Nuñez A, Amzica F. *A novel slow (<1 Hz) oscillation of neocortical neurons.*
  **J. Neurosci.** 13 (1993) 3252–3265 — slow-wave-sleep large-amplitude, low-frequency state.
- Massimini M et al.; Casali AG et al. *A theoretically based index of consciousness (PCI).*
  **Sci. Transl. Med.** 5 (2013) 198ra105 — the access marker held here as an honest negative.
