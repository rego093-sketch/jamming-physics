# FINDINGS — increment E7 (the audible BAND: a geometry-carved bandpass on the inherited wave law)

**Status:** DELIVERED (v0.8.0) — **derives the audible RANGE as a geometry-carved bandpass on the inherited
`√(stiffness/inertia)` wave law**. Deterministic module `run.py` (2×sha256 identical: `ba1f2804…`), small
gate `gate.py` (7/7 PASS), folded into `tools/verify_seed.py` foundation list. **NO inherited byte changed**
— E7 fetches no new gene, folds nothing into the cache/atlas, and triggers **no re-freeze** (every frozen
hash is byte-identical to v0.7.0). No constant tuned.

## What E7 builds
The seed already had the place-map SHAPE (E1) and the near-peak envelope (E6), but *why the audible band
has edges at all* — why we hear ~20 Hz–20 kHz and not 1 Hz or 1 MHz — was only a **cited calibration span**
`[L]` (the Greenwood A/a/k). E7 derives the band itself, in the **same forced-form / `[O]`-magnitude
discipline as E6**, by composing only the **frozen** Greenwood place map. It does **not** pin the band's
numbers (that would be tuning, forbidden); it **characterises** the band: it proves what geometry **forces**
(the bandpass shape, the √-law exponent, the sign of every edge) and what stays the irreducible **measured
geometry** `[O]` (the absolute edges and the three corners).

The keystone is structural: **the √-law HALVES the stiffness decades into octaves** — so the octave count
is forced once the stiffness ratio is known, and the band is a **bandpass = (place passband) × (low-edge
high-pass) × (high-edge low-pass)** whose shape and edge signs are geometry, not tuning.

| feature of the band | what sets it | status |
|---|---|---|
| **octave span ↔ stiffness ratio** | the √-law: `N_oct = ½·log₂(S_base/S_apex)` (exact) | **forced [F]/[V]** |
| **the exponent ½** (decades → octaves) | `CF ∝ √S` (the √-law) | **forced [F]** |
| **low edge = high-pass** (lows cut) | helicotrema topology (apical hole short-circuit) | **side forced, order-robust [F]/[V]** |
| **high edge = low-pass** (highs cut) | ossicular MASS (inertia in the drive path) | **side + −12 dB/oct forced, ζ-robust [F]/[V]** |
| **finite top** (a hard ceiling exists) | finite S_base → finite `CF_max=(1/2π)√(S_base/m)` | **existence forced [F]/[V]** |
| **band = bandpass** (unimodal product) | the three rolloffs multiplied | **shape forced [F]/[V]** |
| **absolute edges** CF_min / CF_max (Hz) | S_apex, S_base, ossicular mass, helicotrema area | **[O] — a number = tuning** |
| **low corner** | helicotrema area + cochlear compliance | **[O]** |
| **high corner** | ossicular mass + path stiffness | **[O]** |
| **the ~10⁶ stiffness ratio** | BM graded geometry (widens & thins base→apex) | **measured [L]** |

## Results (every number reproduced offline, bit-for-bit)
- **A reference structure gene reproduces; nothing inherited moved.** TMC1 (the MET pore-forming subunit,
  the seed's structure reference) recomputes from the frozen cache as γ(level)=**1.3028** + its A4 shape,
  bit-for-bit with the atlas (A4 = signal − γ, |mean(shape)|<1e-9). E7 fetched no gene and changed **no
  inherited byte** — the full frozen-hash set is identical to v0.7.0 (gate G2 verifies). The gene is
  reproduced here only to confirm no-regression; its γ is **never** used as a stiffness, a corner, or a
  band edge. **[V]**
- **The KEYSTONE is exact — `N_oct = ½·log₂(S_base/S_apex)`.** Read off the **inherited** Greenwood map,
  the apex (x=0) is CF=**19.848 Hz** and the base (x=1) is CF=**20677.074 Hz**, an audible span of
  **10.024823 octaves** (≈ human 10). Inverting via the √-law (`S_ratio = (CF_base/CF_apex)²`) gives an
  implied stiffness ratio **1.0853×10⁶** (≈ 10⁶), and `½·log₂(S_ratio)` returns the span to machine
  precision (|Δ|=**0.0e+00**). *Why ~10 octaves* is forced once the ratio is known; *why a ratio ~10⁶* is
  the BM's measured graded geometry `[L]`, never a fit. **[F]/[V]**
- **The ½ is the forced contribution — the span decomposes cleanly.** The bare exponential `10^(a·x)` term
  spans `log₂(10^a) = a·log₂(10) = ` **6.976049 oct** (forced by the √-law on a log-graded stiffness); the
  helicotrema apical bend adds **+3.058894 oct** (the `−A·k` relief, below); a tiny basal offset effect
  subtracts **−0.010120 oct**; the sum is **10.024823 oct = the full span** (|Δ|<1e-9). The exponential
  SHAPE (octaves per stiffness decade) is forced; the absolute decades (~10⁶) are measured `[L]`. **[F]/[V]**
- **The LOW edge is a helicotrema high-pass.** (i) The inherited offset `−A·k` is a **constant subtracted
  from an exponential**, hence a **low-END-only** correction: its fractional weight is **0.88 at the apex**
  vs **0.0070 at the base** — a ratio of **125.893 = 10^a exactly** — so it reshapes **only** the low edge,
  bending the apical end **down 3.0589 oct to ~20 Hz**. (ii) The **topology** forces a high-pass: the apical
  hole short-circuits slow (DC-ward) pressure, so the lows are cut below a corner — a monotone-increasing,
  lows-cut rolloff (|H| at 0.05·ω_c = 0.04994 / 0.00250 / 0.00012 for order n=1/2/3, **→0**), **robust to the
  filter order**. The low-frequency rolloff's **existence and side (apical/low)** are forced; the **corner**
  (helicotrema area + cochlear compliance) is `[O]`, and k is calibration `[L]`. **[F]/[V]**
- **The HIGH edge is a middle-ear low-pass + a finite ceiling.** (i) The ossicular chain has **mass**; a
  driven inertia is a second-order **low-pass** — above its resonance the transmission is
  monotone-**decreasing** with a forced **−12 dB/oct** (slope −2.000 in log-log, the `∝1/ω²` mass term)
  asymptote, **robust to the damping** ζ∈{0.3,0.7,1.0,2.0}. (ii) The stiffest place (the base, x=1) fixes a
  **finite** absolute ceiling `CF_max=(1/2π)√(S_base/m)`: the inherited place map is strictly **increasing**
  apex→base and **finite** at the base (**CF(1)=20677 Hz**). The high-frequency rolloff's **existence and
  side (basal/high)** are forced (a mass → low-pass; a finite S_base → a finite CF_max); the **corner /
  CF_max value** (ossicular mass, S_base) is `[O]`. **[F]/[V]**
- **The BAND is the bandpass PRODUCT.** With placeholder corners (passed in only to **draw** the shape,
  never derived or tuned), the product (low-edge high-pass) × (high-edge low-pass) is **unimodal** — strictly
  rising below its single interior peak, strictly falling above it. The peak place and the two edges **move
  with** the `[O]` corners; only the **shape** (a bandpass, every edge sign forced) is the claim. The
  audible band is a **geometry problem** on top of the inherited wave law — not a new physics. **[F]/[V]**
- **The META-result — the √-law forces the exponent and every sign; the magnitudes are `[O]`.** Forced and
  geometry-invariant: the bandpass shape, the exponent ½ (octaves = ½·log₂ S-ratio), the low-edge high-pass
  side, the high-edge low-pass side, the −12 dB/oct mass asymptote, the finite basal ceiling. `[O]` measured
  geometry: CF_min, CF_max (← S_apex, S_base), the ~10⁶ ratio, the low corner (← helicotrema area +
  compliance), the high corner / CF_max (← ossicular mass + S_base). **None** of those magnitudes is fixed
  by an inherited constant — the √-law gives only the **exponent**, and γ is promoter STRUCTURE only
  (firewall), **not** a stiffness or an edge. The only things that set the edges are measured
  lengths/stiffnesses/masses, none derivable without a measured number. Therefore a **closed numeric band =
  a CHOICE of those magnitudes = TUNING (forbidden)**. E7 does not pin the band; it **characterises** it:
  SHAPE + exponent + every SIGN forced, the absolute edges/corners the irreducible measured-geometry `[O]`.
  *(The E6 parallel: there exactly one scalar Q was open; here the open quantities are the measured
  geometry — same form-forced / magnitude-`[O]` discipline.)* **[F]**

## Honest negatives / open items (preserved, not hidden)
- **N1.** The **absolute band edges CF_min / CF_max (Hz) are `[O]`** — they need S_apex and S_base (the BM
  stiffness at each end), the ossicular mass, and the helicotrema area. Only the bandpass SHAPE, the √-law
  EXPONENT ½, and the SIGN of each edge are forced. A number = **tuning**.
- **N2.** The **low (helicotrema) corner is `[O]`** — it needs the helicotrema area + the scala/cochlear
  compliance. Only the **existence** and the **side (apical/low)** are forced (the topology); the `−A·k`
  offset that places the apex at ~20 Hz uses the measured calibration k `[L]`.
- **N3.** The **high (middle-ear) corner / CF_max is `[O]`** — it needs the ossicular mass + the path
  stiffness, and S_base for CF_max. Only the **existence**, the **side (high)**, and the **−12 dB/oct mass
  asymptote** are forced.
- **N4.** The **stiffness RATIO itself (~10⁶) is a measured anatomical input** — the basilar membrane
  widens (~5×) and thins base→apex; this volume consumes it via Greenwood, never fits it. The √-law forces
  only the **factor (½)** converting it to octaves, not the ratio.
- **N5.** The band here is the **long-wave / place-resonance** account (same scope as E6-N5). The full
  2-D/3-D fluid problem, the cochlear input impedance, and the middle ear's own multi-resonance transfer
  are **not** solved — the deeper `[O]` hydrodynamics. The forced results are the band's shape, exponent,
  and edge signs — not the full transfer function.
- **N6.** The **absolute BM stiffness gradient law S(x)** and the developmental program that builds the
  graded membrane are anatomy / the DNA volume's — `[O]` here. (γ is structure-only, never a stiffness;
  this volume consumes the Greenwood SHAPE, not the gradient's molecular origin.)
- **N7.** The **felt pitch / loudness RANGE as experience** — why ~20 Hz–20 kHz "is" the audible world —
  is the **mind** volume's (firewall). E7 moves only the physical band edges, not the percept.

## Why this matters, honestly stated
The audible band is the kind of fact a tuned model would simply *assert* (pick 20 Hz and 20 kHz, draw a
curve through them). E7 refuses. It proves what the inherited √-law **does** force — that the octave count
is exactly half the log₂ of the stiffness ratio (so the ~10-octave span is the ~10⁶ ratio seen through the
√-law's halving), that a constant subtracted from an exponential can only reshape the low edge (the
helicotrema relief), that an apical hole forces a lows-cut and an ossicular mass forces a highs-cut, and
that the base's finite stiffness forces a finite ceiling — and then names what the geometry **cannot** force
without a measured length, stiffness, or mass: the absolute edges and the three corners. The band becomes a
**characterised** object: not pinned numbers, but a precise statement of which quantities are forced
(shape, exponent, every sign) and which are the irreducible measured-geometry `[O]`, with a proof that
writing the corners down would be tuning. That is the same honesty E6 brought to the envelope — falsifiable
where it can be, explicit about the open magnitudes where it must be.

## Naming note (flagged, not silently fixed)
Delivered in the unambiguous folder `research/E7-audible-band/` — this is **BLUEPRINT-E7 CONTENT** (the
audible band). As with E6, the **existing folders are NOT renamed** (to preserve every frozen hash and the
no-omission set), so the v0.3.0 E1/E2 label slip stays flagged as a separate bookkeeping item; E7's own
folder is unambiguous. A future session may reconcile `BLUEPRINT.md`'s E-numbering with the folder names.

## Firewall
γ read promoter STRUCTURE only — it is **NOT** a stiffness S, **NOT** a corner frequency, **NOT** the
helicotrema area, **NOT** the ossicular mass, **NOT** a band edge or a clinical effect (the reference gene
is reproduced offline ONLY to show the cascade gene still recomputes and no inherited byte moved). **No
disease claim** here — E7 is the healthy band geometry; the band-specific losses are **E8**, proposal-only.
No molecule, dose, in-vivo selectivity, or efficacy; nothing diagnosed or treated. Every magnitude is
**[O]** with its obstacle named. The felt pitch/loudness RANGE as experience is the **mind** volume's.
