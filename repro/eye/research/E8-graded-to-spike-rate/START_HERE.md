# E8 — graded → spike-rate re-quantisation  (START HERE)

**The ladder's last rung.** E5/E6/E7 leave the eye's output as a **graded** low-pass signal whose band
is set by the recovery τ (E7: f_c = β/(2π·τ)). E8 is the final step: the retina re-encodes that
continuous ~Hz signal as a discrete ganglion-cell spike **RATE** — a re-quantisation at the low band
(rate coding) — and the carrier that was discarded at the single-photon flip (E2) must **not** reappear.
With E8 the whole down-conversion spine **E0→E8 is complete**; where seeing *feels like something* hands
off to the **mind** volume (firewall).

## Run it
```
python3 research/E8-graded-to-spike-rate/run.py        # the rate code, measured on the FROZEN Neuron (deterministic)
python3 research/E8-graded-to-spike-rate/gate_E8.py    # 8 independent checks → E8 GATE: PASS
```

## The one claim
The **re-quantiser is the FROZEN R19 neuron** — no new math. The same FROZEN Neuron whose slow recovery
*set the band* in E7 now **fires**: a spike is a membrane up-crossing = an all-or-none R19 fold-crossing
event (E2's cubic −s³ is what makes it all-or-none). The inherited readers (`Neuron.spikes` /
`Neuron.rate_hz` / `dominant_freq`) turn the continuous membrane signal into a discrete count → a rate.
The graded photoreceptor signal enters as the slowly-varying **drive**; the output is the spike **RATE**.

> **graded amplitude → firing RATE**: a thresholded (rheobase), bounded (depolarisation-block ceiling),
> monotone code that carries the slow **envelope** and never the **carrier**.

## The honest shape of the code (measured, not assumed)
The FROZEN Neuron is an autonomous relaxation oscillator, so its rate code is a **bandpass in drive**:
silent in a deep-hyperpolarised basin (a rheobase **floor** — the switch must be driven across its fold),
firing across an operating band, and silenced again by **depolarisation block** past the band (a
**ceiling** — the switch sticks ON, the oscillation stops). The code is clean and monotone *inside* that
band; that is the honest operating envelope, and the absolute band edges/rates are a named **[O]**.

## What each part shows (and its grade)
- **(0) the re-quantiser.** the FROZEN Neuron's up-crossings ARE the spike train; the inherited readers
  give a discrete count → a rate. graded in, rate out. [F]
- **(1) the rheobase floor.** from a silent hyperpolarised rest (drive=−1.0), a graded increment g is
  **SILENT at g≤0.20, FIRES at g≥0.30** — the all-or-none switch must clear its fold to spike (E2/E4 read
  forward). The code has a floor. [V]
- **(2) the monotone code.** above the floor the rate rises **strictly** with the graded amplitude across
  the operating band (g 0.25→0.90 ⇒ rate 0.00783→0.01133): the amplitude is re-encoded as a rate. [F]/[V]
- **(3) a genuine quantiser.** the spike train is a near-periodic point process — **CV(ISI) ≈ 0.0002**
  (a clean clock): the continuous input is genuinely **re-quantised** into a rate-coded train. [F]/[V]
- **(4) the honest ceiling.** the full-range f–I is **non-monotone** — SILENT on BOTH sides
  (hyperpolarisation floor at drive≤−0.8 **and** depolarisation-block ceiling at drive≥+1.0), firing only
  in between. The monotone code lives in a **finite** band; the bandpass STRUCTURE is forced, the absolute
  edges a named **[O]**. [V]+[O]
- **(5) the carrier stays gone (no mixing).** hold the slow envelope fixed and sweep the carrier
  frequency ⇒ the rate is **invariant** (spread **1.53%** across a 20× carrier span, rate ⟂ carrier);
  hold the carrier fixed and raise the envelope ⇒ the rate **rises** (rate ∝ envelope). The re-quantiser
  tracks the envelope and does **not** re-introduce the carrier — the E5/E7 ~13-order down-conversion is
  **preserved**. [F]/[V]
- **(6) the rate lives in the low band.** the spike train's dominant frequency **equals** the firing rate
  (0.01083) and sits orders below the carrier — the re-quantisation does not undo the collapse; what
  crosses to the brain is the low-band rate. [F]
- **(7) where γ sits (read-only).** raising a gene's γ raises its spinodal (the switch is harder to flip),
  shifting the f–I curve's **position** (the rheobase moves) without changing the code's shape — γ is a
  **structural excitability offset**, *not* the band (that is τ, E7) and *not* the signal (the graded
  drive). γ moves the rate ~as much as the drive here, so E8 makes **no** "γ negligible" claim; γ is read
  byte-equal from the atlas only to show the offset. [F]/[V]

## Honesty / firewall
E8 is pure sensory **mechanism** — no disease, diagnostic, or clinical claim (that layer is E4,
firewalled). Nothing is fitted: β, τ_f, τ_s are the FROZEN Neuron's own constants, the spike reader is
inherited **verbatim**, every γ used is read byte-equal from the frozen atlas (READ-ONLY), and the
operating point is an **input**, not a fitted target; SEED=19; deterministic 2×sha256.

Four named **[O]** are stated plainly:
- **absolute Hz / spike-count** — the rate is in spikes/unit-time; the absolute spikes·s⁻¹ (and any real
  refractory period, ganglion gain, or saturation count) is not fixed by the promoter-γ — the ladder's
  standing [O]. Only the code STRUCTURE is forced.
- **the f–I shape** — only the thresholded, bounded, monotone STRUCTURE is forced; whether the real curve
  is linear / sqrt / log and where it saturates is substrate/biology.
- **one stage vs the retinal network** — the substrate collapses photoreceptor→bipolar→amacrine→ganglion
  lateral processing (centre–surround, temporal filtering) into a single re-quantiser; the receptive-field
  structure is out of scope.
- **the felt percept** — where seeing feels like something hands off to the **mind** volume (firewall).
  E8 ends at the neural RATE, not the experience.

## The result, in one line
The eye's last step is a **re-quantiser, not a mixer**: the graded transduction signal is turned into an
all-or-none spike train whose **RATE** encodes the graded amplitude — thresholded, bounded, monotone —
carrying the slow **envelope** while the carrier stays discarded (E2) and filtered (E7). The down-
conversion survives **end-to-end** because colour/place are geometry and the rate is the envelope, never
the carrier.

## Next
**The ladder spine E0→E8 is complete.** Grow E0→E8 into the full multi-chapter **HTML volume** (VP-SPEC
v1.8 §6) — every displayed number 2×sha256-reproduced, HTML↔code drift 0, the disease layer proposal-only
under the firewall — shipped as **one zip**. Candidate later increments (same firewall, beyond the spine):
common **red–green dichromacy** via the E1 angle map; **light/dark adaptation** as gain control on the
switch; **accommodation + refractive error** extending E3's optics; and a much harder
acquired/degenerative disease layer (AMD, glaucoma, diabetic retinopathy). Still deferred: **SIX6**
(eye-field TF), the one remaining gene in the atlas `_to_measure`. Absolute Hz at every rung stays [O].
