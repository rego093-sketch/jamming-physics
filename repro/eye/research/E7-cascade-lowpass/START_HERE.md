# E7 — the cascade as the band-setting low-pass  (START HERE)

**The rung after the ladder spine:** E5 showed *how* the ~10¹⁴ Hz carrier collapses to the neural
band, and noted in passing that the surviving band is set by the recovery τ (out_dom ∝ 1/τ) while the
carrier is "averaged away". E7 turns that aside into the **named filter**: it reads an explicit
transfer function off the FROZEN substrate, locates the cutoff, and shows the cutoff IS the closed
form **f_c = β/(2π·τ)** — the output band is *manufactured* by the recovery τ, not inherited from the
light.

## Run it
```
python3 research/E7-cascade-lowpass/run.py        # closed form + the measured filter (deterministic)
python3 research/E7-cascade-lowpass/gate_E7.py    # 8 independent checks → E7 GATE: PASS
```

## The one claim
The filter is **already in the substrate** — no new math. The FROZEN Neuron updates its recovery by
the verbatim law `w ← w + dt·(s − β·w)/τ_s`, which is a first-order **leaky integrator** = a single-pole
low-pass on the membrane signal. In the Fourier domain (s in, w out):

> H(f) = 1/(β + i·2πf·τ_s),  |H(f)| = 1/√(β² + (2πf·τ_s)²)

so three things are **forced** (closed form, no fit): the passband gain is **1/β**, the −3 dB **cutoff
is β/(2π·τ_s)** (hence **f_c·τ_s = β/2π**, i.e. f_c ∝ 1/τ *exactly*), the phase lag at the cutoff is
**45°**, and the roll-off is **−20 dB/decade**. The band the eye speaks in is the cutoff of this filter.

## What each part shows (and its grade)
- **(0) the closed-form filter.** straight from the substrate's own recovery law: DC gain 1/β=2.0,
  cutoff β/(2π·τ), 45° cutoff phase, −20 dB/dec roll-off. [F]
- **(1) the MEASURED transfer function** (a lock-in on the verbatim recovery law, τ_s=40 = the Neuron
  default) reproduces the closed form: DC gain **1.999** (=1/β); cutoff **0.001993** vs β/(2πτ)=0.001989
  (**ratio 1.002**); phase lag at the cutoff **45.0°**; high-f slope **−19.96 dB/decade**. The cascade
  IS a first-order low-pass and its band edge is the explicit number β/(2π·τ). [F]/[V]
- **(2) the band is β/(2πτ): manufactured by the recovery, not the carrier, not γ.** sweep τ_s ∈
  {20,40,80}: the cutoff halves with τ, and the product **f_c·τ_s is constant to 0.27%** (= β/2π) ⇒
  f_c ∝ 1/τ *exactly*. The recovery law carries **no carrier term and no γ** ⇒ the band is **purely τ**:
  orthogonal to the carrier (§E5's no-mixing) AND orthogonal to γ. [F]/[V]
- **(3) the low-pass *is* E5's "averaged away".** E5's fast carriers sit at f ≫ f_c, where the
  closed-form |H| ∝ 1/f drives the response to ~0 — the carrier-rejection of §E5 is **exactly** this
  −20 dB/dec roll-off (f=5.0 ≈ 2500× f_c ⇒ |H|/DC ≈ 4×10⁻⁴). The real ~10¹⁴ Hz carrier sits ~17 orders
  above any plausible f_c ⇒ total rejection. [F]
- **(4) the full neuron inherits the band.** on the FROZEN Neuron the intrinsic rhythm falls
  monotonically as τ_s rises (0.01875 → 0.00300 over τ 20→160) — but only **approximately** ∝ 1/τ:
  out_dom·τ drifts upward (0.375 → 0.480) because a relaxation period = (slow recovery ∝ τ) +
  (a τ-independent fast transit). The **clean** 1/τ law lives in the explicit filter; the neuron
  inherits it. γ (the switch nonlinearity, dwell ∝ γ^1.5) is the **secondary** mover — at fixed τ the
  eye γ's shift the rhythm only mildly while τ sets the decade. [V]

## Honesty / firewall
E7 is pure sensory **mechanism** — no disease, diagnostic, or clinical claim (that layer is E4,
firewalled). Nothing is fitted: β, τ_f, τ_s are the FROZEN Neuron's own constants, the recovery law is
copied **verbatim**, every γ used is read byte-equal from the frozen atlas (READ-ONLY), and the cutoff is
the substrate's closed form; SEED=19; deterministic 2×sha256.

Two named **[O]** are stated plainly:
- **one pole vs a cascade.** the substrate models the *net* transduction as a **single pole**
  (−20 dB/dec). The real photoreceptor cascade is multi-stage (rhodopsin→transducin→PDE→cGMP→CNG) —
  higher-order, so the real roll-off is steeper. The single-pole **structure** and **band ∝ 1/τ** are
  forced; the pole **count** is the [O].
- **absolute Hz.** the cutoff is in 1/unit-time; the **absolute τ** in seconds (hence the absolute
  cutoff in Hz) is not fixed by the promoter-γ — the same [O] running through every rung of the ladder.
  Only the *scaling* and the filter's *shape* are forced.

## The result, in one line
The neural band is not chosen by the photon — it is the **cutoff of the transduction low-pass,
f_c = β/(2π·τ)**: raise the recovery τ and the band drops with it, while the carrier and γ leave the
cutoff untouched. The carrier is detected as one event (§E2) and then **filtered out**; what survives is
the recovery's own band.

## Next
**E8 — graded → spike-rate re-quantisation (the hand-off to the neural code).** Re-encode the graded
photoreceptor signal as a ganglion-cell spike **RATE** (rate coding at the low band). The ladder ends
there, at the neural code; the **felt percept** of sight stays deferred to the **mind** volume. [F] the
rate-code structure; absolute rates [O]. Still deferred: **SIX6** (eye-field TF), the one remaining gene
in the atlas `_to_measure`.
