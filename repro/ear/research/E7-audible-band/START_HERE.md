# START HERE — increment E7 (the audible BAND: a geometry-carved bandpass on the inherited wave law)

**One-line goal.** Derive **why only certain frequencies are heard** — why the audible range has EDGES at
all (~20 Hz–20 kHz, not 1 Hz or 1 MHz) — as a **geometry-carved bandpass** sitting on the inherited
`√(stiffness/inertia)` wave law, in the same forced-form / `[O]`-magnitude discipline as E6: the bandpass
**SHAPE** and the **SIGN of every edge** are forced; the band's absolute edges and three corners stay `[O]`.

## Why this increment exists
E0 already states sound and light share **one** elastic-wave law (light `c²=B/ρ`, air `vₛ=√(γP/ρ)`,
cochlea `ω=√(S/m)` — the same `√(stiffness/inertia)`). E1 forced the place-map **SHAPE**; E6 characterised
the near-peak **envelope**. But *why the band has edges* was, until here, only a cited calibration span
`[L]` (the Greenwood A/a/k). E7 closes that gap the honest way — it does **not** pin the band's numbers
(that would be tuning, forbidden); it **characterises** the band, proving what geometry forces (the shape,
the exponent, every edge sign) and what stays the irreducible measured-geometry `[O]` (the absolute edges
and corners).

## What it delivers (all in this folder)
- `run.py` — the deterministic module (self-hashing, 2×sha256). Imports the **frozen** `vp_sound_wave`
  Greenwood place map and reuses E1's reading; **edits no inherited byte** and triggers **no re-freeze**
  (E7 fetches no gene).
- `gate.py` — the standalone gate (G1–G7).
- `FINDINGS.md` — results + seven honest negatives.
- `START_HERE.md` — this card.

## The result in one paragraph
Because the resonance obeys the √-law (`CF ∝ √S`), the octave span is **exactly half** the log₂ of the
basilar-membrane stiffness ratio: the **keystone** `N_oct = ½·log₂(S_base/S_apex)`, which closes to machine
precision on the inherited Greenwood map (human **10.025 octaves ⟺ a stiffness ratio 1.085×10⁶**). The
√-law's whole job is the **exponent ½** — it **halves** the ~6 stiffness decades into ~10 octaves; *why ~10
octaves* is forced once the (measured) ratio is known. The two band edges are forced **topological**
rolloffs with `[O]` corners: the **low edge** is a **helicotrema high-pass** — the inherited `−A·k` offset
is a **low-END-only** relief (fractional weight 0.88 apex vs 0.007 base, ratio = 10^a) bending the apex
down ~3 octaves to ~20 Hz, and the apical hole forces a lows-cut **side**; the **high edge** is a
**middle-ear low-pass** — an ossicular **mass** forces a −12 dB/oct highs-cut (slope robust to the damping)
and the stiff base fixes a **finite** CF_max. The band is the **product** of the three — a bandpass whose
SHAPE and every edge SIGN are forced by geometry, while the absolute edges and three corners are the
irreducible measured-geometry `[O]`. A number for any of them would be **tuning**.

## How to run / verify
```
python3 research/E7-audible-band/run.py     # prints the emergence; ends with 'sha256: …'
python3 research/E7-audible-band/gate.py    # 'E7 GATE: PASS' iff all 7 hold
python3 tools/verify_seed.py                # whole-seed gate; E7 is in the foundation list
```

## Firewall (binding)
γ reads promoter **structure only** — it is **NOT** a stiffness S, **NOT** a corner frequency, **NOT** the
helicotrema area, **NOT** the ossicular mass, **NOT** a band edge or a clinical effect (the reference gene
is reproduced offline ONLY to show the cascade gene still recomputes and no inherited byte moved). **No
disease claim** — E7 is the healthy band geometry; the band-specific losses are **E8**, proposal-only. No
molecule, dose, or efficacy; nothing diagnosed or treated. Every magnitude is **[O]** with its obstacle
named, and the felt pitch/loudness RANGE as experience is the **mind** volume's.
