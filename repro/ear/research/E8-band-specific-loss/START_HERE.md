# START HERE — increment E8 (band-specific hearing loss: E4's CLASS axis × E7's PLACE axis)

**One-line goal.** Derive the characteristic **audiogram SHAPES** — high-frequency/down-sloping, the 4 kHz
notch, cookie-bite, low-frequency/reverse-slope — by composing **E4's failure-CLASS axis** (drive /
structure / readout / amplifier) with **E7's PLACE axis** (which frequency sits where). Same discipline as
E4/E6/E7: the **SHAPE** and every **DIRECTION** (which way the audiogram tilts, which side the notch sits)
are forced; every threshold, slope, notch-Hz, and age stays `[O]`; the lever is **proposal-only,
direction-only**; the firewall is verbatim.

## Why this increment exists
E4 answered **which** locus of the inherited cubic `ṡ = g·s − s³ + h` fails (structure g / drive h / readout
downstream / critical g→0). E7 supplied the **place** axis: the inherited √-law Greenwood map `CF(x)` is
strictly increasing apex→base. But a real audiogram is frequency-**selective** — loss concentrated in a
**band** — so a disease is a **2-D object**: a failure **class** acting over a **band of places**. E8
composes the two axes the honest way: it does **not** pin an audiogram (numbers would be tuning, forbidden);
it **characterises** the SHAPE, proving which DIRECTIONS the geometry forces and which magnitudes stay the
irreducible measured `[O]`.

## What it delivers (all in this folder)
- `run.py` — the deterministic module (self-hashing, 2×sha256). Imports the **frozen** `vp_sound_wave`
  Greenwood map, reuses E1's `inv_greenwood`/`read_measured`, consumes the inherited cubic's `spinodal`
  (to carry E4's negative) and E4's class labels; **edits no inherited byte** and triggers **no re-freeze**
  (E8 fetches no gene).
- `gate.py` — the standalone gate (G1–G7).
- `FINDINGS.md` — results + seven honest negatives.
- `START_HERE.md` — this card.

## The result in one paragraph
Because the inherited place map `CF(x)` is strictly **monotone** (E7-D), the place→frequency map is an
**order-isomorphism**: a contiguous band of **failed places** maps to a contiguous band of **lost
frequencies**, preserving order, and `inv_greenwood` maps it back exactly. So the audiogram SHAPE **is the
image** of *where* the failure concentrates — **basal** failure → **high**-frequency down-slope, **apical**
failure → **low**-frequency reverse-slope, **mid** failure → cookie-bite, and a localized **over-drive** at
the outer/middle-ear transfer peak → a **notch below the top**. The four shapes are read off this one
isomorphism plus three forced facts: the base **cycles fastest** (`CF` *is* the cycling rate), so cumulative
load is **basal-first** (→ presbycusis is high-frequency-first); the ear transfer (`canal resonance × E7
ossicular low-pass`) has an **interior peak below CF_max**, so noise over-drives a place **below the top**
(the ~3–6 kHz C5-dip); and the apex is where the **helicotrema relief + ion regulation** dominate (→ a
WFS1-type apical loss is low-frequency). The lever is the **E4 direction applied at the E7 band** (a 2-D
direction), proposal-only — and E4's honest negative **carries**: a structure-class high-frequency loss has
**no drive rescue** (the bistable window `2·spinodal(g)→0` as `g→0`). Every DIRECTION is forced; every
threshold, slope, notch-Hz, and age is the irreducible measured `[O]`.

## How to run / verify
```
python3 research/E8-band-specific-loss/run.py     # prints the emergence; ends with 'sha256: …'
python3 research/E8-band-specific-loss/gate.py    # 'E8 GATE: PASS' iff all 7 hold
python3 tools/verify_seed.py                       # whole-seed gate; E8 is in the foundation list
```

## Firewall (binding)
γ reads promoter **structure only** — it is **NOT** a band edge, **NOT** a load rate, **NOT** a dB
threshold, **NOT** a notch frequency, **NOT** an in-vivo selectivity or a clinical effect (one cached gene
per class is reproduced offline ONLY to show the cache still recomputes and no inherited byte moved). The
disease layer is **proposal-only**: direction-only (class × band) failure modes and substrate-inverse lever
**directions**. No molecule, dose, diagnosis, or efficacy; nothing diagnosed or treated. **WFS1 is named
only as a cited clinical archetype** — no new γ is measured for it. Every magnitude is **[O]** with its
obstacle named, and the felt experience of band-specific loss is the **mind** volume's.
