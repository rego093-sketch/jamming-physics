# E6 — why the band is VISIBLE  (START HERE)

**The increment after the ladder:** E5 showed *how* the ~10¹⁴ Hz carrier collapses to the neural
band. E6 answers the prior question — **why is the carrier the eye is handed the *visible* band**
(~380–750 nm) and not some other slice of the spectrum?

## Run it
```
python3 research/E6-why-visible/run.py        # the two gates, end to end (deterministic)
python3 research/E6-why-visible/gate_E6.py    # 8 independent checks → E6 GATE: PASS
```

## The one claim
Two completely different constraints, read on the FROZEN foundation, bracket the **same** narrow band:
- **GATE (i) — GEOMETRY places it.** In lattice units the quantum count m=⌈λ/D⌉ is monotone in λ, so
  the bands sit in a fixed order: gamma (m=1, the lone quasi-longitudinal band) → x-ray → **VISIBLE**
  → infrared → radio. Visible is **sandwiched in m** between x-ray (smaller m) and infrared (larger m),
  in the near-transverse manifold; its identity — **colour** — is its propagation angle χ(λ). [F]
- **GATE (ii) — PHOTOCHEMISTRY pins it.** A photon must carry enough energy to drive the *reversible*
  11-cis→all-trans retinal isomerisation (an energy **floor**) yet not so much that it ionises /
  photodamages (a **ceiling**): the cited window ~1.8–3.3 eV maps, through the forced E=hc/λ, onto
  ~376–689 nm. [L] (chromophore photochemistry) + [F] (the arithmetic).

## What each part shows (and its grade)
- **(0) the exact carrier map.** every ALREADY-MEASURED visible anchor (the RCROSS channels 633/532 nm
  and the cone-opsin λmax 420/530/560 nm) mapped EXACTLY: λ → ν=c/λ → period T=1/ν=λ/c → E=hν, with the
  SI-exact constants (c=299792458 m/s, h=6.62607015e-34 J·s). T=1/ν and E=hν hold to 1e-15. No rounding,
  no round-number band edges invented. Carrier ≈ 4.7–7.1×10¹⁴ Hz, period ≈ 1.4–2.1 fs. [L]/[F]
- **(1) gate (i): m-sandwich.** m strictly increases gamma<x-ray<visible<IR<radio; gamma (m=1) is the
  only quasi-longitudinal band, visible is near-transverse. Angles are carried to **full precision** (χ to
  10 dp) **and** via the near-grazing deficit (90°−χ), computed without the 1−sin²χ cancellation; each
  satisfies the canonical closure m·sinχ·D/λ=1 to 1e-15. [F]
- **(2) gate (ii): the energy window.** cited 1.8–3.3 eV → exactly 375.71–688.80 nm; EVERY measured
  visible anchor lands inside, each E to 8 dp. Below the floor no flip; above the ceiling damage. [L]/[F]
- **(3) the honest split — geometry PLACES but cannot PIN; energy PINS.**
  - (3a) the band-internal angle deficit (90°−χ) is tiny (<0.3°) and **non-monotone** — a sawtooth from
    the m=⌈⌉ quantisation: **633 nm has a smaller deficit than 750 nm even though it is shorter** — vs a
    >78° gamma deficit, so there is **no geometric kink** at the band edges; the edges cannot be geometric. [F]
  - (3b) the edges coincide with the **energy** window, not a geometric boundary: an infrared probe
    (10 µm, ≈0.124 eV) is excluded by the energy floor although its deficit is **smaller** than visible's
    (more transverse) — geometry would admit it. The pinning is photochemical. [F]/[L]

> **Precision note (why this rev exists):** the angle is shown to full precision **and** through the
> deficit, but it is **not** the band's gate — it never excludes a band; the WAVELENGTH (mapped exactly
> to ν and period) and its photon ENERGY are what pin the band. No rough arithmetic; measured wavelengths
> are the anchors.

## Honesty / firewall
E6 is pure sensory **mechanism** — no disease, diagnostic, or clinical claim (that layer is E4,
firewalled). The two windows are **cited inputs** (the conventional visible band; the reversible
isomerisation window 1.8–3.3 eV), frozen as written — **not** fits, **not** derived from package data;
E=hc/λ is forced; the angle law and D are the inherited frozen canon (read-only); no γ is added; SEED=19.
**The red edge is soft and we say so:** 750 nm (1.65 eV) sits ~0.15 eV *below* the clean isomerisation
floor (deep red is low-efficiency, perceived only bright), so the conventional band slightly overhangs
the clean window on the red side. And the chromophore energy that sets the floor is **coding /
photochemistry** — the promoter-γ this package reads has **no lever** on the retinal pocket: a named
**[O]**. E6 forces the band **placement** (geometry) and the energy-window **logic**; it invents no
chromophore and tunes nothing.

## The result, in one line
'Visible' is neither chosen nor geometric: geometry only **places** the band (angle↔colour, sandwiched in
m), while the chromophore's **reversible energy window** pins ~380–750 nm — two unrelated constraints
landing on the same band, with the molecular tuning of that window left a named [O].

## Next
**E7 — the cascade as the band-setting low-pass.** Make the transduction cascade's time constant τ the
explicit filter that fixes the output band (~1/τ): model the R19 switch's settling (dwell ∝ γ^1.5) and
recovery as a low-pass and show the ~10–100 Hz band emerges **from τ, not the carrier** (E5 already shows
the τ-dependence; E7 makes it the filter). [F] the low-pass structure and band-from-τ; absolute τ (hence
absolute Hz) a named [O]. Then **E8** (graded → spike-rate re-quantisation, the hand-off; felt percept →
mind volume). Still deferred: **SIX6** (eye-field TF), the one remaining gene in the atlas `_to_measure`.
