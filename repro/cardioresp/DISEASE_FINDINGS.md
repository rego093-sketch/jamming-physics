# DISEASE FINDINGS — Cardiorespiratory extension (research artifact)

**Status.** Research-layer results, NOT canonical. Produced by `repro/_disease/respiratory_disease.py`
and graded by `repro/_disease/disease_battery.py`. Deterministic (two-run identical sha256). Nothing
here enters `docs/` until it passes a writing gate of its own. This file is a sibling of `CHARTER.md`
and `FUTURE_WORK.md`, deliberately out of `docs/`.

**The one-line result.** Six respiratory disorders were each cast as a perturbation of an object the
base package already built and verified (T1–T5 + the oncology Kramers kernel). **All six reproduce the
predicted qualitative behavior, and not one needs a new substrate primitive** — they reuse only the R19
bistable switch and the FitzHugh–Nagumo relaxation oscillator. That "one substrate suffices" outcome is
itself the headline.

Run it:
```
python repro/_disease/disease_battery.py        # D1–D6 pass/fail + grades
python repro/_disease/respiratory_disease.py     # full numeric block + sha256
```

---

## What each disease reuses, and what came out

| D | disease | object reused | result | grade |
|---|---|---|---|---|
| D1 | Mayer waves (~0.1 Hz) | baroreflex (T5) + Nyquist solver | loop self-oscillates; for cited sympathetic-arm delays 3–5 s the frequency lands at 0.10–0.13 Hz, inside the Mayer/LF band; period ≈ 2.5× delay (same forced family as Cheyne–Stokes) | mechanism **[V]**, abs freq **[L]** |
| D2 | Asthma | oncology `barrier_eff` (reversible) | convex/threshold constriction-vs-dose curve; the open basin VANISHES at the spinodal (PC20-like all-or-none attack); a negative bias (bronchodilator) reopens it, with a hysteresis loop (width ≈ 1.43) | shape **[V]**, hysteresis **[V?]**, abs PC20 **[O]** |
| D3 | OSA | chemoreflex (T2) + R19 switch | LG/LGc behaves exactly as the clinical "loop-gain endotype" (stable below 1, unstable above); the pharynx collapses DISCONTINUOUSLY at its spinodal (= Pcrit) with hysteretic reopening | loop gain **[V]**, Pcrit collapse **[V?]**, abs Pcrit **[O]** |
| D4 | CSA spectrum | chemoreflex/Cheyne–Stokes (T2/T4) | three diseases = three axes: altitude (gain ↑ → instability at gain ratio ≈ 1.2), CHF (delay ↑ → CSR period 52–81 s at 25–40 s delays, inside the clinical 45–90 s band, slope ≈ 1.96), opioid (drive ↓ → rhythm quenches at the lower Hopf, drive ≈ −0.77) | directions **[V]**, abs thresholds **[O]** |
| D5 | Fever | BOTH FHN oscillators via shared γ(T) | SantaLucia ΔG(T) lowers the shared substrate γ with temperature, so heart and lung rates RISE TOGETHER — tachycardia and tachypnea CO-SCALE (same direction), the substrate-distinctive prediction. HR:RR co-scaling ratio ≈ 3.8 | co-scale direction **[V?]**, abs slope **[O]** |
| D6 | Cough | FHN excitable (sub-Hopf) regime | held below the lower Hopf the unit is silent; a brief irritant kick below threshold decays (peak ≈ −0.50) while above threshold it fires one full all-or-none excursion (peak ≈ +1.10) — the cough reflex as a single excitation | all-or-none **[V?]**, abs C5 **[O]** |

**Battery: 6/6 pass.**

---

## The honest negatives and open items (the important part)

- **D5 fever magnitude is ~10× too small, and that is reported, not hidden.** The shared-γ(T) mechanism
  gives HR ≈ +0.9 bpm/°C, against the clinical Liebermeister ≈ 10 bpm/°C. The DIRECTION and the
  CO-SCALING are forced by the shared substrate (the falsifiable structural claim); the absolute slope
  is **[O]** because febrile tachycardia also has exogenous metabolic-rate (Q10) and sympathetic
  contributions that are NOT in this substrate. The substrate predicts *coupling*, not the full
  magnitude — stated plainly.
- **D4 opioid: the rhythm is hard to silence.** Lowering the tonic drive across a WIDE window does not
  quench breathing; only a deep cut past the lower Hopf does. This robustness is a genuine model output
  (matching that opioid central apnea needs substantial depression), not a tuned result.
- **Every absolute magnitude is [O]** (PC20, Pcrit, capsaicin C5, absolute febrile rate) for the SAME
  structural reason as absolute organ size and absolute cancer RR: the switch noise scale and the
  stimulus→bias conversion are not fixed by substrate geometry and need external calibration. The
  SHAPES and DIRECTIONS are the forced/verifiable content.
- **Out of scope, flagged not absorbed:** molecular immunology, viral kinetics, the allergic cascade,
  and pharmacodynamics are upstream of the dynamics and enter only as an exogenous bias `h`. Cor
  pulmonale crosses the seam to a circulatory package that does not yet exist → it stays **[O]**.

---

## Why this matters for the program

The base paper showed heart and lung are the SAME oscillator. This extension shows their **diseases**
are the same three objects too — a delayed control loop going unstable (Mayer waves, OSA loop gain,
CSA, Cheyne–Stokes), an R19 switch crossing a spinodal (asthma attack, pharyngeal collapse), or an FHN
unit firing one excitation (cough) — with the molecular cause entering only as a bias or a parameter
shift. No disorder required inventing new substrate physics. The framework's content is the forced
SHAPES (threshold, hysteresis, ≈2× delay, all-or-none, co-scaling); its honest limit is that absolute
clinical magnitudes need external calibration.
