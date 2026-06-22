# FINDINGS — increment E1 (tip-link MET switch on the place map)

**Status:** DELIVERED (v0.3.0). Deterministic module `run.py` (2×sha256 identical), small gate
`gate.py` (7/7 PASS), folded into `tools/verify_seed.py` foundation list. Inherited foundation
untouched (frozen hashes valid). No constant tuned.

## What E1 builds
The hair-cell **mechanotransduction (MET) tip-link switch** — `TMC1 / PCDH15 / CDH23` (the three
genes `START_HERE.md` names; `TMIE` shown as the 4th MET partner) — **emerged** from the measured
DNA reading and the R19 `Organ` primitive, sitting on the inherited √-law place map. Each gene is
read as **γ (LEVEL) + A4 coordinate (SHAPE)**, not γ alone (DNA v1.13).

## Results (every number reproduced offline, bit-for-bit)
- **Inputs reproduce.** γ + A4 of all four MET genes recompute from the frozen promoter cache and
  equal the atlas bit-for-bit; A4 = signal − γ (|mean(shape)| < 1e-9 per gene). **[V]**
- **Emergence order** = argsort(spinodal(γ)), spinodal = 2·(γ/3)^1.5:
  **TMC1 (0.5724) < PCDH15 (0.6233) < CDH23 (0.7336)** < TMIE (0.7467). Lower discontinuous
  threshold ⇒ earlier switch competence. **[F]** structure; γ measured **[L]**.
- **A4 tie-break refuses to collapse equal-γ genes.** A constructed same-γ pair (identical γ ⇒
  identical spinodal, an exact primary-key tie) is kept distinct by the A4 SHAPE (count 2, not 1).
  The compressed "γ alone" view would lose them. **[V]**
- **R19 all-or-none gating.** The MET switch is OFF up to 0.99·spinodal and flips ON discontinuously
  past it (steady state −0.71 → +1.31) — no graded leak across the barrier. **[F]** structure;
  absolute SPL→Hz scale **[O]**.
- **Place map** (inherited, re-verified): ω=√(S/m) + log-graded stiffness ⇒ exponential place map;
  √S ∝ 10^(a·x) reproduces Greenwood's term to max|ratio−1| = 2.2e-16. **[F/V]**; A/a/k measured **[L]**.
- **Traveling-wave PEAK PLACE** is parameter-free: x*(f) = inverse-Greenwood(f) round-trips to
  < 1e-12 Hz (250 Hz→x*0.18, 1 kHz→0.40, 4 kHz→0.67, 16 kHz→0.95). **[F/V]**

## Honest negatives / open items — the E1→E2 starting line (preserved, not hidden)
- **N1.** The A4 tie-break **never fires** on this atlas — all MET γ are distinct (spinodal ties = 0).
  It is correct and proven non-vacuous on constructed inputs, but its necessity **on this data is
  null**. Kept because equal-γ genes can occur in general; reading γ alone would be unsafe.
- **N2.** argsort(spinodal(γ)) is a structural **[F]** order. Its concordance with the **measured**
  hair-cell developmental sequence is **NOT** asserted — **[O]**, needs cited timing data. *Obstacle:
  no developmental-timing dataset is bundled.*
- **N3.** Only the traveling-wave **peak place** is forced. The full fluid-loaded, dispersive
  **ENVELOPE** (peak width, phase accumulation, apical cutoff slope, active gain) is **[O]**.
  *Obstacle:* a passive envelope needs a damping/Q and the cochlear fluid mass-loading
  (Lighthill/Zweig hydrodynamics) plus the E3 active amplifier; a closed envelope would require
  **tuning Q** — forbidden. This is the named open target the seed exists to take up.
- **N4.** **No per-gene tonotopic place** is claimed — MET genes span the whole partition; assigning
  one would be invention.

## Naming note (flagged, not silently fixed)
The folder is `E1-place-and-traveling-wave`, and `BLUEPRINT.md`'s **E1** is the full traveling-wave
hydrodynamics while its **E2** is the MET switch. The `START_HERE.md` task in this folder is the
**MET switch on the place map** (BLUEPRINT-E2 content). This increment delivers exactly the
`START_HERE` task and forces only the traveling-wave **peak place**, leaving the full ENVELOPE (the
BLUEPRINT-E1 [O]) open. A future session should reconcile the E-numbering in `BLUEPRINT.md`.

## Firewall
γ read promoter STRUCTURE only (never voltage/gain/dose/effect). No disease claim (E1 is
pre-disease). The percept of hearing is the mind volume's.
