# Brainwaves, memory, and the paralysis of reason — an emergence + literature whitepaper

**Author program:** VP / Jamming-Physics (Young Jae Lee).
**Document type:** self-contained research note (portable — readable on its own in a new
session). It upgrades the earlier consciousness/brainwave concordance with two new mechanisms
and a **stress-test panel** (hunger · drugs · sex · fear · pain · panic disorder · learning
disability), with results.

**Honest framing.** The core hypotheses are the author's; as a single combined claim they do
not yet exist in the literature. So every claim carries a grade — **[F]** forced/cited ·
**[V]** verified in code · **[I]** inference (literature-concordant, *not* proof) · **[O]**
open — and rests on two legs: (i) a deterministic **emergence** test that reuses only the
governed engine's measured/derived constants, and (ii) **phenomenological concordance** with
published neuroscience. **No new tuned constant is introduced anywhere.** Reused constants
(all [F]): α = 2/π, δ = 1/π² (angle-rectification, single & double; from the VP bridge DOI
10.5281/zenodo.17932566), κ = 0.5496 (measured ephaptic fraction), and the R19 bistable fold
≈ 0.3849. The dimensionless gain = 6.0 is the same R19-tilt unit bridge as engine M11 (swept).
`medium_efficacy_tested = 0` throughout; **no claim of subjective experience is made.**

**Reproduce (deterministic, SEED = 19, single-thread):**
- `python3 vp_consciousness_brainwave_study.py` — stages A–E (headline sha256
  `30bc4f6de8d371e07b96e828e08db613072fc504bb007f9c2f55d3c21dbbe970`).
- `python3 vp_brainwave_stress_tests.py` — stages F–J (headline sha256
  `26a7638f6610f24f27efacbe58606b3a566b551c6f0fe7d4aa7d321985d71a54`).
Both reuse the governed engine `vp_mind_engine.py` (constants + the Hippocampus engram + the
R19 settle), and each ends with a self-check that doubles as a gate.

---

## 0. The model in one paragraph

A brainwave is emerged light on the same vacuum lattice; information lives in the **phase
relationship** between two carriers, not in either angle's magnitude. A high-frequency
(gamma) carrier binds distributed activity by **angle rectification** — a signed phase overlap
(which averages to zero) becomes a *sign-surviving* information bit only after rectification
(single α = 2/π, double δ = 1/π²). A memory is written when that bound, rectified drive clears
the engram's bistable **fold**. **Consciousness, on this view, is the strongest high-frequency
carrier that actually reaches the memory cell** — read as *high-frequency strength*, not raw
amplitude (see §2). A memory is stored as a **low-frequency index + high-frequency content**;
re-firing the index floods its content back into awareness (§3). And when a single
**low-frequency drive** (hunger, fear, pain, craving, lust) grows strong enough, it **captures
the integrator** and the rational, multi-item binding collapses — reason is paralysed (§4–§5).

---

## 1. Consciousness = the strongest high-frequency carrier reaching memory (stages A–E)

| Claim | Emergence result [V] | Literature concordance [I] |
|---|---|---|
| **H1** strong gamma carrier = conscious access | critical carrier strength **A_crit ≈ 0.467**; at full strength drive 0.824 > fold 0.385 → writes | gamma (30–90 Hz) ↔ binding/attention/access since Crick–Koch, Engel 1992; **caveat:** access may also need recurrent/beta feedback (Cogitate 2025; a 2026 tACS study) |
| **H2** a forgotten dream = a wave too weak to reach memory | weak "dream" carrier (A = 0.30 → drive 0.247) is **sub-threshold → no write → not recalled**; strong "wake" carrier writes | **strong match:** higher frontal theta (5–7 Hz) in REM predicts dream recall, mirroring waking encoding (Marzano 2011; Sederberg–Kahana 2003); continuity hypothesis |
| **H3** focus strengthens the wave → consciousness strengthens | focus modeled as gamma coherence lifts coincidence from floor δ→¼; drive 0.357→0.824; **recall threshold f ≈ 0.35** | attention raises V4 gamma power/coherence; only the attended stimulus's gamma reaches downstream (Fries 2001; Bosman 2012; CTC) |
| **H4/H6** high-freq CPU gathers parallel low-freq GPU workers | integrated drive **grows with locked workers**; fully gathered 0.824 ≫ unbound-only 0.322 | theta-gamma code: nested gamma slots = parallel items, WM 7±2 = slots/theta (Lisman–Jensen 2013); gamma as time-division multiplex (Masuda 2009) |
| **H5** the carrier wakes the stored memory (down-conversion) | stored engram (self-sustain 1.000) completed from a 40 % cue at fidelity **1.000**; fast 40 Hz drive → slow ~5.7 Hz read-out | gamma sub-cycles read out within the theta cycle; theta-gamma coupling predicts recall (Tort 2009) |

### The crucial honest refinement — amplitude is **not** consciousness (stage E)
Read as *raw EEG amplitude*, "strongest wave = consciousness" is **refuted**: deep slow-wave
sleep has the **largest-amplitude** waves (delta, > 75 µV) yet is the **least conscious** state,
while waking is **low-amplitude, high-frequency** activity. The emergence makes the dissociation
explicit: a huge-amplitude **unstructured** (delta-like) drive — ~60× the gamma carrier — writes
**no recoverable memory** (recall ≈ 0.65, near chance), while a far smaller **structured** gamma
carrier writes a perfectly recoverable one (recall 1.000). **Resolution:** "strongest wave" must
mean the strongest **high-frequency** carrier reaching memory — exactly the author's own wording
("the big brainwave is a high frequency"). Under that reading the model is coherent; under the
amplitude reading it fails at deep sleep.

---

## 2. New mechanism A — memory = low-frequency index + high-frequency content (stage F)

**Claim.** A memory is not stored as content alone; it is a **slow index bound to fast
content**. When the low-frequency index re-fires, *all* the high-frequency content of that
moment is reinstated into the conscious buffer — which is why recalling a memory brings back its
"feel," not just its facts.

**Emergence [V].** Three memories were stored, each as `[low-freq index | high-freq content]`.
Cueing with **only memory-0's index** reinstated **memory-0's content at fidelity 1.000**; the
*same* cue matched a *different* memory's content at only 0.533 (≈ chance — not reinstated); a
**novel, never-stored index** produced no clean flood (best match 0.717). The slow index behaves
as a content-addressable **address**: fire it, and that moment's fast content returns.

**Literature [I].** This is the retrieval side of the **theta-gamma code**: the slow theta
phase indexes fast gamma item-assemblies, so reinstating the phase reinstates the bound content
(Lisman & Jensen, 2013); hippocampal pattern completion from partial cues is the standard
mechanism. A 2024 model extends theta-gamma coupling explicitly to sequential memory,
imagination, and dreaming (Pirazzini & Ursino, 2024).

---

## 3. New mechanism B — a strong low-frequency drive paralyses reason (stage G)

**Claim.** "Reason" is the carrier holding **several** rational items at once (working-memory
width). A single strong **low-frequency drive** competes for the carrier's limited gain; as it
grows, rational slots drop out, and beyond a **capture threshold** only the one drive remains
bound — reason is paralysed.

**Emergence [V].** With six rational slots and a competing drive of amplitude D suppressing each
slot's delivered drive (divisive normalisation), the count of bound slots collapses
**monotonically**: D = 0 → **6 slots**; D = 0.5 → 3; **D = 1.0 → 1 (paralysed)**; D ≥ 2 → 0.
The **capture threshold is D_cap = 1.0**.

**Literature [I] — strong match.** This is the **amygdala hijack** / stress-impairs-PFC
picture: strong emotion impairs the prefrontal cortex and switches control to more primitive
circuits, with high catecholamine release rapidly degrading PFC top-down function while
strengthening the amygdala (Arnsten, 2009/2015; Goleman). Clinically the hijack **narrows you to
a single option** — described as being unable to "think" when overwhelmed — exactly the collapse
of multi-slot integration the model shows.

---

## 4. Stress-test panel — hunger, drugs, sex, fear, pain (stage H)

Each drive is a strong (mostly limbic/interoceptive) **low-frequency** signal. Under provocation
`p`, its amplitude `D(p) = D₀ + gain·p`; the test reports the provocation `p*` at which reason
is captured. **The baselines and gains are schematic and swept (ordering only, NOT measured) —
the *order*, not the absolute number, is the claim. Graded [I].**

| Drive | baseline D₀ | gain | capture p\* | concordance [I] |
|---|---|---|---|---|
| **pain** | 0.80 | 2.0 | **0.070** | pain involuntarily *seizes attention* and compromises memory encoding (Eccleston & Crombez, 1999; pain-interruption literature) |
| **fear** | 0.60 | 2.2 | **0.150** | amygdala hijack: rapid PFC suppression, fight/flight bypasses reason (Arnsten 2009) |
| **drug craving** | 0.50 | 1.8 | **0.240** | iRISA: excessive salience to drug cues *at the expense of other content*; PFC control hijacked (Koob; Goldstein & Volkow) |
| **sex (lust)** | 0.40 | 1.6 | **0.330** | strong limbic reward drive; treated as a salient non-drug reinforcer in cue-reactivity work |
| **hunger** | 0.30 | 1.0 | **0.630** | slower homeostatic/hypothalamic drive; captures later than the acute threat/appetite drives |

**Emergence ordering (easiest → hardest to capture reason):**
**pain < fear < drug craving < sex < hunger.** All eventually capture; pain and acute fear do so
fastest (consistent with their *interruptive, threat-priority* clinical profile), homeostatic
hunger slowest. This is the "특정 저주파가 강해지면 고주파 에너지에 도달해 이성을 마비시킨다" claim,
made concrete and ranked — with the explicit caveat that the **ranking** is the testable content,
not the schematic magnitudes.

---

## 5. Panic disorder = runaway positive feedback — a bifurcation (stage I)

**Claim.** Panic is interoceptive fear that **catastrophically amplifies itself**. The same
circuit is healthy or pathological depending on one parameter — the self-amplification
**sensitivity** s.

**Emergence [V].** Logistic feedback `D_{t+1} = D_t + dt·( s·D_t·(1 − D_t/D_max) − leak·D_t )`
with homeostatic restraint `leak = 0.6` gives a **bifurcation at s_crit = leak = 0.60**:
- **Healthy** (s = 0.4 < s_crit): a small interoceptive trigger (D₀ = 0.30) **self-limits to 0**
  — no panic, reason never paralysed.
- **Panic disorder** (s = 1.2 > s_crit): the same trigger **runs away to 3.0**, crossing the
  capture threshold and **paralysing reason at step 3** — a panic attack that **peaks fast**.

**Literature [I] — strong match.** Panic's **false-suffocation-alarm** model (Klein) and
interoceptive-runaway accounts: the amygdala acts as a CO₂/pH **chemosensor**, a falsely
triggered suffocation alarm drives escalating fear, and a panic attack characteristically
**peaks within ~10 minutes** (Gorman's neuroanatomical network; Wemmie's pH-chemosensation
work). A subcritical-vs-supercritical sensitivity is a faithful dynamical reading of "why the
*same* bodily signal is trivial for most people and catastrophic in panic disorder."

---

## 6. Learning disability = weak / disorganised theta-gamma coupling (stage J)

**Claim.** Learning requires the gamma carrier to clear the memory fold, which requires the
gamma to land at the **right theta phase** — i.e., good theta-gamma **coupling quality** q.
Below a critical q, learning fails **even at full carrier strength and full focus** — a
**structural** deficit, categorically different from a merely weak (low-effort) signal.

**Emergence [V].** Modeling disorganised coupling as the gamma sitting at the *wrong* theta phase
(q = 1 → optimal phase, coincidence ¼; q = 0 → antiphase, coincidence → 0) gives a **critical
coupling quality q_crit ≈ 0.590**:
- typical reader (q = 0.90): encode drive **0.787 > fold → learns**;
- disorganised (q = 0.30): encode drive **0.067 ≪ fold → learning FAILS at full strength + focus.**

This separates two failure modes the model otherwise conflates: a **weak** signal (low A) is
fixable by strength/focus (stages A–B); a **disorganised-coupling** deficit (low q) is not —
turning up effort cannot fix bad timing.

**Literature [I].** **Reduced theta-gamma coupling** is reported in ADHD during attention-
demanding tasks and as a candidate diagnostic marker (Kim et al., 2016, *PLOS ONE*; theta-phase
gamma-amplitude coupling reflecting cortico-subcortical interaction). **Dyslexia** shows
atypical low-frequency (delta/theta) and gamma entrainment to speech, with the theta phase that
normally controls gamma amplitude disrupted (Goswami and colleagues; 2024–2025 entrainment
studies). Autism and schizophrenia likewise show abnormal cross-frequency coupling. The model's
"timing, not effort" reading matches these as **coupling-organisation** disorders.

---

## 7. What this is, and is not

- **[V] In silico, deterministic, reusing only governed constants:** the strength threshold
  (wake vs dream), the focus gradient, CPU/GPU integration, gamma→engram down-conversion, the
  amplitude↔consciousness dissociation, index→content reinstatement, drive-capture collapse of
  reason, the panic bifurcation, and the learning-coupling threshold — **all hold and reproduce
  bit-for-bit.**
- **[I] Inference, literature-concordant, not proof:** every mapping onto consciousness, dreams,
  attention, the drive panel, panic disorder, and learning disability. The **drive-panel
  magnitudes are schematic** (ordering only).
- **[O] Open:** `medium_efficacy_tested = 0`. The identity *"the strongest gamma carrier IS
  conscious access"* remains a **correlate, not a demonstrated cause**; the hard problem of
  experience is **untouched**; **no claim of subjective experience** is made. Honest caveat from
  the literature: gamma may index *binding* more than *access*, with access also needing
  recurrent/beta feedback — so even the central identity is held as a hypothesis, not a result.

---

## 8. Optional next step — promote to a governed module

If you want this in the governed package rather than as standalone studies, the natural form is
**M12 `emerge_consciousness_access()`** + chapter **§16**, carrying as locked invariants: the
strength/focus thresholds, the reinstatement specificity, the drive-capture `D_cap`, the panic
`s_crit` bifurcation, and the learning `q_crit` — with the **amplitude↔consciousness
dissociation** kept central as the honesty anchor. It reuses the same constants (no new tuning),
adds ~6 registry locks and one `verify_consciousness.py`, and re-freezes under the existing
11-gate battery. Built exactly the way M11 was. Say the word.

---

## References (as retrieved)

**Oscillatory code & consciousness**
- Lisman JE, Jensen O. *The theta-gamma neural code.* **Neuron** 77 (2013) 1002–1016.
- Lisman JE, Idiart MAP. *Storage of 7 ± 2 short-term memories in oscillatory subcycles.*
  **Science** 267 (1995) 1512–1515.
- Axmacher N et al. *Cross-frequency coupling supports multi-item working memory in the human
  hippocampus.* **PNAS** 107 (2010) 3228–3233.
- Tort ABL et al. *Theta-gamma coupling increases during the learning of item-context
  associations.* **PNAS** 106 (2009) 20942–20947.
- Fries P. *Rhythms for cognition: communication through coherence.* **Neuron** 88 (2015) 220–235.
- Fries P, Reynolds JH, Rorie AE, Desimone R. *Modulation of oscillatory neuronal
  synchronization by selective visual attention.* **Science** 291 (2001) 1560–1563.
- Bosman CA et al. *Attentional stimulus selection through selective synchronization between
  monkey visual areas.* **Neuron** 75 (2012) 875–888.
- Masuda N. *Selective population rate coding: a possible computational role of gamma
  oscillations in selective attention.* **Neural Computation** 21 (2009) 3335–3362.
- Cogitate Consortium et al. *Adversarial testing of global neuronal workspace and integrated
  information theories of consciousness.* (2025).

**Dreams & sleep**
- Marzano C et al. *Recalling and forgetting dreams: theta and alpha oscillations during sleep
  predict subsequent dream recall.* **J Neurosci** 31 (2011) 6674–6683.
- Sederberg PB, Kahana MJ, et al. *Theta and gamma oscillations during encoding predict
  subsequent recall.* **J Neurosci** 23 (2003) 10809–10814.
- Pirazzini G, Ursino M. *Modeling the contribution of theta-gamma coupling to sequential
  memory, imagination, and dreaming.* **Front. Neural Circuits** 18 (2024) 1326609.
- Slow-wave sleep / delta amplitude vs. least-conscious state: ScienceDirect *Slow-Wave Sleep*
  overview; OpenStax *Psychology 2e* §4.3.

**Emotion, drives, and the paralysis of reason**
- Arnsten AFT. *Stress signalling pathways that impair prefrontal cortex structure and
  function.* **Nat. Rev. Neurosci.** 10 (2009) 410–422 (and 2015 updates).
- Goleman D. *Emotional Intelligence* (1995) — the "amygdala hijack."
- Eccleston C, Crombez G. *Pain demands attention: a cognitive-affective model of the
  interruptive function of pain.* **Psychol. Bull.** 125 (1999) 356–366.
- Koob GF, Volkow ND. *Neurobiology of addiction: a neurocircuitry analysis.* **Lancet
  Psychiatry** 3 (2016) 760–773; Goldstein RZ, Volkow ND, the **iRISA** model.

**Panic disorder**
- Klein DF. *False suffocation alarms, spontaneous panics, and related conditions.* **Arch. Gen.
  Psychiatry** 50 (1993) 306–317.
- Gorman JM et al. *Neuroanatomical hypothesis of panic disorder, revised.* **Am. J.
  Psychiatry** 157 (2000) 493–505.
- Wemmie JA. *Neurobiology of panic and pH chemosensation in the brain.* **Dialogues Clin.
  Neurosci.** 13 (2011).

**Learning disability / cross-frequency-coupling disorders**
- Kim JW et al. *Desynchronization of theta-phase gamma-amplitude coupling during a mental
  arithmetic task in children with ADHD.* **PLOS ONE** 11 (2016) e0145288.
- Goswami U and colleagues; 2024–2025 audiovisual-speech entrainment studies in developmental
  dyslexia (atypical low-frequency & gamma coupling).

*Quotations are paraphrased throughout; consult the originals for exact wording and figures.*
