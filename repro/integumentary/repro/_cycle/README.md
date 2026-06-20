# `_cycle` — the hair-follicle cycle: the package's first autonomous oscillator

The core battery (`repro/run_all.py`) reports **"no autonomous oscillator organ in this physical
class"** — its four organs run as steady-state switches (barrier, melanin, sweat, turnover). The hair
follicle is the missing piece: it **cycles** (anagen → catagen → telogen → exogen → re-entry). This
module emerges that cycle as the **shared FitzHugh–Nagumo relaxation oscillator** (`vp_substrate.Neuron`)
running on the **existing, measured** appendage master-gene γ (**EDAR**). It is a **new target on an
existing organ** — the EDAR appendage read in its *oscillating* regime rather than its steady
sweat-flux regime (CHARTER T5). It is a **research artifact**: it writes `reports/cycle_results.json`
and does **not** touch the core writing gate; the core T1..T5+oncology battery hash is **unchanged**.

This implements `HANDOFF_NEXT_STEPS.md` §5.2 (mechanism-first) for the alopecia lane previously flagged
in §4 as *"NOT YET MODELABLE — missing target (the appendage organ exists; the cycling dynamics target
does not)."* The missing target now exists.

## Run

```
python repro/run_cycle.py
```

Prints the oscillator emergence, the disease → mechanism map, the mechanism + clinical-sign +
intervention-reversal battery, the opposite-sign/opposite-timing discriminant, selected readouts, and
the 2×sha256 determinism check; writes `reports/cycle_results.json`.

## The no-tuning rule (VP-SPEC C0/C3)

> γ is **measured** (EDAR, read-only). `tau_f/tau_s/beta` are the **substrate** relaxation-oscillator
> defaults (neuro 02); `tau_s` is the slow cycle clock — it sets the **period**, never the duty cycle.
> The healthy growth bias is a **substrate-scaled** fraction of the spinodal (a dimensionless regime
> scale `[F]`, **not** fitted to a duty target). What the substrate **predicts** — autonomous
> oscillation, a relaxation (plateau+collapse) waveform, an anagen-**dominant** duty cycle that
> lengthens with the growth drive — is `[V]`. The absolute anagen **fraction** (cited ~85–90%) and the
> absolute **period** (years) are the `[L]`/`[O]` anchors the substrate is compared against by **sign
> and dominance**; they are not claimed as fitted matches.

Why this matters: a single constant drive **cannot** be pushed to the cited ~88% anagen fraction
without killing the oscillation (the Hopf line back to a fixed point). Rather than tune around that,
the layer grades the substrate honestly — it gets the **dominance, the relaxation shape, and every
disease direction**, and leaves the absolute fraction as a cited anchor.

## Disease → knob (4) — each a signed shift on the **one** oscillator

| disease | knob moved | intervention (knob reversed) |
|---|---|---|
| androgenetic alopecia (AGA) | standing anti-growth (miniaturisation) drive → anagen shortens, terminal→vellus | minoxidil / anti-androgen: pro-growth drive lengthens anagen |
| alopecia areata (AA) | **sustained** premature-catagen drive → anagen collapses, patch held in telogen (persistent) | remove the drive → anagen resumes (regrowth, hysteresis) |
| telogen effluvium (TE) | **transient** synchronising pulse → an anagen cohort shifts to telogen, sheds one telogen later (delayed), self-limited | self-limited; remove the stressor |
| anagen effluvium (AnE) | direct anagen-matrix arrest (chemo/radiation) → **immediate** shed, bypassing telogen | reversible when the insult stops |

## The headline check — opposite-sign / opposite-timing discriminant

The **same** oscillator, driven with **opposite** signs (or transient vs sustained), reproduces
clinically **opposite** entities with **no new constant**, across three axes:

- **anagen duration** — AGA (short) ↔ minoxidil (long).
- **shed timing** — telogen effluvium (delayed, *via* telogen, at exactly **one telogen duration**) ↔
  anagen effluvium (immediate, *bypassing* telogen).
- **persistence** — alopecia areata (sustained drive → persistent) ↔ telogen effluvium (transient →
  self-limited).

`run_cycle.py` asserts all three (`all_opposite_pairs_reproduced`). The TE shed landing at exactly one
telogen arc is the substrate's clean account of *"TE sheds ~3 months (one telogen) after the
stressor."*

## Files

- `hair_cycle.py` — the oscillator (`cycle_metrics`), the deterministic shedding-population model
  (`shedding_dichotomy`), the 4 alopecias, and `hair_cycle_summary()`.
- `cycle_verify.py` — the mechanism + clinical-sign + intervention-reversal battery, the discriminant,
  the determinism check, and `cycle_gate()` (this layer's research-first lock).

## Honest notes

- **anagen fraction** — the substrate gives a strongly anagen-dominant cycle (~0.59 here); the cited
  ~85–90% is the `[L]` anchor, matched in **dominance and direction**, not as a fitted number.
- **absolute period** — `tau_s` sets a dimensionless period; the conversion to years (anagen 2–6 yr,
  telogen ~3 mo) is `[O]` (needs a per-follicle cycle-clock calibration). The **shed lag = one
  telogen** result is a dimensionless `[V]` ratio independent of that absolute.
- **core untouched** — this layer reuses the substrate + the engine emitter only; it does not modify
  `_engine`, `_oncology`, or `_verify`, so `repro/run_all.py`'s result hash is unchanged.
