# FINDINGS — increment E8 (band-specific hearing loss: E4's CLASS axis × E7's PLACE axis)

**Status:** DELIVERED (v0.9.0) — **derives the characteristic audiogram SHAPES by composing E4's failure-
CLASS axis with E7's PLACE axis**. Deterministic module `run.py` (2×sha256 identical: `e23484ea…`), small
gate `gate.py` (7/7 PASS), folded into `tools/verify_seed.py` foundation list. **NO inherited byte changed**
— E8 fetches no new gene, folds nothing into the cache/atlas, and triggers **no re-freeze** (every frozen
hash is byte-identical to v0.8.0). No constant tuned.

## What E8 builds
E4 answered **which** cubic locus fails (structure / drive / readout / amplifier). E7 supplied the **place**
axis. But a real audiogram is frequency-**selective**, so a disease is a **2-D object** — a failure **class**
acting over a **band of places**. E8 composes the two axes in the **same forced-direction / `[O]`-magnitude
discipline as E6/E7**. It does **not** pin an audiogram (that would be tuning, forbidden); it
**characterises** the SHAPE: it proves which DIRECTIONS the geometry **forces** (the tilt of each audiogram,
the side of the notch) and which stay the irreducible **measured magnitude** `[O]` (every dB, every slope,
the notch Hz, the age).

The keystone is structural: **the inherited place map is monotone, so place→frequency is an order-
isomorphism** — the audiogram SHAPE is literally the **image** of *where* on the cochlea the failure sits.

| audiogram shape | E4 class × E7 band | what forces the DIRECTION | status |
|---|---|---|---|
| **place→frequency isomorphism** | (the keystone) | `CF(x)` strictly monotone (E7-D) ⇒ contiguous band ⟺ contiguous band, exact inverse | **forced [F]/[V]** |
| **high-frequency / down-sloping** (presbycusis) | degeneration × **basal** | base cycles fastest (`CF` = rate) ⇒ cumulative load **basal-first** | **direction forced [F]** |
| **4 kHz NOTCH** (noise-induced) | over-drive × **transfer-peak place** | ear transfer (canal × ossicular low-pass) has an interior peak **below CF_max** | **direction forced [F]** |
| **mid-frequency / cookie-bite** | mid-gradient locus × **middle** | the isomorphism: mid PLACE → mid FREQUENCY | **image forced [F]; locus cited [L]** |
| **low-frequency / reverse-slope** (WFS1) | ion/drive regime × **apical** | the isomorphism: apical PLACE → low FREQUENCY | **direction forced [F]** |
| **the lever** (per shape) | E4 direction **@** E7 band | a 2-D direction (restore which locus, at which band) | **proposal-only [F-direction]** |
| **E4 negative carries** | structure × basal | bistable window `2·spinodal(g)→0` as `g→0` (E4-C) | **forced [F]/[V]** |
| **every dB / slope / notch-Hz / age** | — | needs measured anatomy/physiology | **[O] — a number = tuning** |

## Results (every number reproduced offline, bit-for-bit)
- **One cached gene per E4 class reproduces; nothing inherited moved.** SLC26A4 (drive, γ=**1.3612**),
  MYO15A (structure, γ=**1.4960**), OTOF (readout, γ=**1.4245**), SLC26A5 (amplifier, γ=**1.4023**) each
  recompute from the frozen cache bit-for-bit with the atlas (A4 = signal − γ, |mean(shape)|<1e-9). E8
  fetched no gene and changed **no inherited byte** — the full frozen-hash set is identical to v0.8.0 (gate
  G2 verifies). The genes are reproduced only to confirm no-regression and to anchor the cross-axis
  composition to the **same** frozen atlas; their γ is **never** used as a band edge, a load rate, or a dB.
  **[V]**
- **The KEYSTONE — the place→frequency map is an order-isomorphism.** The inherited `CF(x)` is strictly
  increasing apex→base (CF_apex=**19.8 Hz**, CF_base=**20677.1 Hz**), so a contiguous band of failed places
  maps to a contiguous band of lost frequencies, **order preserved**, and `inv_greenwood` maps it back to
  the **same** band to machine precision: basal `x∈[0.7,1.0]` → CF∈[4736, 20677] Hz (**high** → down-slope),
  middle `x∈[0.4,0.6]` → CF∈[999, 2864] Hz (**mid** → cookie-bite), apical `x∈[0.0,0.3]` → CF∈[19.8, 560] Hz
  (**low** → reverse-slope), each round-tripping `|Δ|<1e-9`. No constant is tuned — this is the monotonicity
  of the inherited map turned into an isomorphism. **WHERE fails ⇒ WHICH band is lost.** **[F]/[V]**
- **HIGH-FREQUENCY / DOWN-SLOPING (presbycusis) = degeneration × the basal band.** The base is the
  highest-CF place, so it **cycles fastest** (`CF` *is* the cycling rate); if load accumulates with cycles,
  the cumulative-load ordering is **monotone**, maximal at the base (load(base)/load(apex) = **1042×**). So
  the basal/high-CF places are loaded first ⇒ fail first ⇒ a high-frequency loss progressing down the map —
  exactly the classic basal/high-frequency-first presbycusis (Schuknecht). The **direction** (basal-first ⇒
  down-sloping) is forced; the slope/threshold/age are `[O]`. **[F]**
- **The 4 kHz NOTCH (noise) = an over-drive × the transfer-peak place.** The outer/middle-ear energy-delivery
  transfer = (ear-canal resonance) × (the E7 ossicular-mass low-pass); drawn with illustrative corners
  (passed in only to **show** the shape, never tuned) it is **unimodal** with an interior maximum at
  `f_peak` (illustrative ≈ 3549 Hz) that is strictly **below CF_max** (20677 Hz) and maps to an **interior**
  place (x≈0.64, below the base). The place tuned to the transfer maximum receives the most input energy ⇒
  over-drives ⇒ fails first ⇒ a **notch below the very top** — the classic ~3–6 kHz C5-dip. The **direction**
  (a notch below the top, not at it) is forced; the exact notch Hz (ear-canal length + ossicular transfer)
  is `[O]`. **[F]**
- **MID-FREQUENCY / COOKIE-BITE = a mid-gradient locus × the middle band.** A locus whose vulnerability
  peaks mid-cochlea maps, by the isomorphism, to a mid-frequency loss with better edges
  (`x∈[0.4,0.6]→CF∈[999,2864] Hz`). The **forced** part is only mid PLACE → mid FREQUENCY; the
  mid-**concentration** of the locus is a cited/empirical input, **not** derived — the honestly **weakest**
  of the four (N2). **[F-image; L-locus]**
- **LOW-FREQUENCY / REVERSE-SLOPE (WFS1 archetype) = an apical ion/fluid locus × the apical band.** The apex
  is where the helicotrema relief (E7-C: the `−A·k` offset is apical-only) and the endolymph/ion regulation
  dominate; an apical-specific regulation failure maps to low frequencies (`x∈[0.0,0.3]→CF∈[19.8,560] Hz`) ⇒
  a low-frequency / up-sloping (reverse) loss. The **direction** (apical ⇒ low-frequency) is forced by the
  place map; the locus's apical concentration is cited biology `[L]` (WFS1/Wolframin is a low-frequency,
  often fluctuating SNHL tied to ion homeostasis — a drive/ion-regime class in E4 terms); magnitude `[O]`.
  WFS1 is named **only** as the cited archetype — no new γ is measured for it. **[F]**
- **The 2-D picture + the lever.** Each audiogram is a **(class × band)** hypothesis: which of E4's loci,
  over which of E7's place bands, reproduces the shape. The substrate-inverse lever is the **E4 direction
  applied at the E7 band** — a 2-D direction (restore which locus, at which band). E4's honest negative
  **carries**: the bistable window `2·spinodal(g)` collapses as `g→0` (1.1410 → 0.00077), so the
  **structural** component of a high-frequency loss admits **no drive rescue** (the switch is gone, not
  un-driven); only the drive-class (the apical reverse-slope ion regime) is switch-recoverable in principle —
  and even then only the **direction** is named. No molecule, dose, in-vivo selectivity, diagnosis, or
  efficacy. **[F]/[V]**
- **The META-result — the SHAPE and every DIRECTION are forced; every magnitude is `[O]`.** Forced and
  parameter-free: the place→frequency order-isomorphism and the four shape directions (basal→HF down-slope,
  apical→LF reverse, mid→cookie-bite, the transfer-peak notch below the top), the basal-first load ordering,
  and that E4's structure-class drive-non-rescue carries. `[O]` measured magnitude: every dB threshold,
  every dB/oct slope, the notch frequency (Hz), the age of onset, the cumulative-load rate, the absolute
  band edges. The inherited map and the cubic give only the **order** and the **signs**; the magnitudes need
  measured anatomy/physiology, and γ is promoter structure only (firewall) — never a load rate, a band edge,
  or a dB. Therefore a **closed numeric audiogram = a CHOICE of those magnitudes = TUNING (forbidden)**. So
  E8 does not pin an audiogram; it **characterises** the SHAPE: every direction forced, every magnitude the
  irreducible measured `[O]` — the E6/E7 discipline, now on the 2-D (class × band) object. **[F]**

## Honest negatives / open items (preserved, not hidden)
- **N1.** Every **magnitude is `[O]`** — the dB thresholds, the dB/oct slopes, the notch frequency in Hz,
  the age of onset, the load rate, the absolute band edges. Only the SHAPE and the DIRECTIONS (the tilt, the
  notch side) are forced. A number on any of them would be **tuning**.
- **N2.** **Cookie-bite is the weakest** of the four — the isomorphism forces only mid PLACE → mid FREQUENCY;
  the mid-**concentration** of the locus is a cited/empirical input, not derived. E8 does not explain **why**
  a given gene's vulnerability peaks mid-cochlea; that is `[O]` (the locus's position on the cochlear
  gradient — anatomy / the DNA volume).
- **N3.** The **notch frequency (~3–6 kHz) is `[O]`** — it needs the ear-canal length + the ossicular
  transfer. Only the **existence** of an interior transfer peak (hence a notch **below the top**) is forced;
  the illustrative `f_peak` is **not** a claim.
- **N4.** **Presbycusis is multi-factorial** (sensory, strial/metabolic, neural — Schuknecht's types). E8
  forces only the **basal-first direction** of the cyclic-load component; the full cellular taxonomy and the
  relative weights of the mechanisms are cited/`[O]`, not derived.
- **N5.** The cumulative-load argument forces the **ordering** (basal-first) but **assumes** load accrues
  monotone with cycling rate — a cited biophysical premise, not derived here. The rate, the accrual law, and
  any threshold are `[O]`.
- **N6.** Real audiograms are **individual and noisy**; E8 is a SHAPE-**direction** claim about the
  population **tendency** of each etiology, **not** a per-patient predictor. Overlap between etiologies
  (e.g. a noise notch on a presbycusic slope) is expected and not resolved here.
- **N7.** The **readout class (OTOF/synapse) has no place-band shape** in this transduction map — its failure
  is downstream of the flip (E4-D); a band-specific readout audiogram needs the synaptic substrate, which is
  `[O]`. And the **felt experience** of band-specific loss (losing consonants in HF loss, losing bass in LF
  loss) is the **mind** volume's (firewall).

## Why this matters, honestly stated
A band-specific audiogram is the kind of clinical fact a tuned model would simply *fit* (draw the curve,
read off the numbers). E8 refuses. It proves what the two inherited axes **do** force — that because the
place map is monotone, *where* on the cochlea a failure sits **is** *which* frequency band is lost (an exact
order-isomorphism), that the base's being the fastest-cycling place forces presbycusis to be high-frequency-
first, that an interior transfer peak forces the noise notch to sit **below** the top, and that the apex's
ion/relief regime forces a WFS1-type loss to be low-frequency — and then names what the geometry **cannot**
force without a measured number: every threshold, slope, notch-Hz, and age. The audiogram becomes a
**characterised** object: not pinned numbers, but a precise statement of which directions are forced and
which magnitudes are the irreducible measured `[O]`, with a proof that writing the numbers down would be
tuning. The disease layer states **directions**, never doses — and even keeps E4's honest negatives, refusing
to promise a drive rescue for a structural high-frequency loss. That is the same honesty E6/E7 brought to the
envelope and the band, now on the 2-D (class × band) object.

## Naming note (flagged, not silently fixed)
Delivered in the unambiguous folder `research/E8-band-specific-loss/` — this is **BLUEPRINT-E8 CONTENT**
(band-specific loss). As with E6/E7, the **existing folders are NOT renamed** (to preserve every frozen hash
and the no-omission set), so the v0.3.0 E1/E2 label slip stays flagged as a separate bookkeeping item; E8's
own folder is unambiguous. A future session may reconcile `BLUEPRINT.md`'s E-numbering with the folder names.

## Firewall
γ read promoter STRUCTURE only — it is **NOT** a band edge, **NOT** a load rate, **NOT** a dB threshold,
**NOT** a notch frequency, **NOT** an in-vivo selectivity or a clinical effect (one cached gene per class is
reproduced offline ONLY to show the cache still recomputes and no inherited byte moved). The disease layer is
**proposal-only**: direction-only (class × band) failure modes and substrate-inverse lever **directions**. No
molecule, dose, in-vivo selectivity, or efficacy; nothing diagnosed or treated. **WFS1 is named only as a
cited clinical archetype** — no new γ is measured for it. Every magnitude is **[O]** with its obstacle named.
The felt experience of band-specific hearing loss is the **mind** volume's.
