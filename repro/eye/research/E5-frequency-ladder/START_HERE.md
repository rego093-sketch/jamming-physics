# E5 — the frequency ladder, quantified  (START HERE)

**The increment that answers the re-scoped goal:** how does the eye turn the **high-frequency light
band** (~10¹⁴ Hz carrier) into the **low-frequency neural band** (~10–100 Hz spike code)?

## Run it
```
python3 research/E5-frequency-ladder/run.py        # the ladder, end to end (deterministic)
python3 research/E5-frequency-ladder/gate_E5.py    # 8 independent checks → E5 GATE: PASS
```

## The one claim
The eye does **not** down-convert by mixing/heterodyne (a photoreceptor cannot oscillate at 10¹⁴ Hz).
It down-converts by **EVENT-DETECTION + LOW-PASS INTEGRATION**: a photon's *energy* E=hν drives one
discrete all-or-none R19 flip (the carrier frequency is discarded), and the cascade/recovery *time
constant* τ sets the surviving band (~1/τ). The carrier's identity — **colour** — survives the
~13-order collapse only because it rides the propagation **angle χ** (geometry, from rung 1 / the
inherited canon), not a frequency the cell could follow.

## What each part shows (and its grade)
- **(0) rung 1 — the carrier.** ν=c/λ and the photon energy E=hc/λ (633→1.96 eV, 532→2.33 eV). The
  receptor sees E as a *quantum of drive*, not a frequency. [L]/[F]
- **(1) the collapse.** ν_light / neural band ≈ 10¹²–10¹³ ≈ 13 orders. Ratio forced; absolute neural Hz [O].
- **(2) the mechanism, on the FROZEN Neuron (substrate-time):**
  - (2a) **low-pass** — a fast carrier (24×–476× the intrinsic rhythm) is averaged away; out/f_c → 0. [V]
  - (2b) **carrier-invariance** — across a 20× carrier span the output moves ~11%; output ⟂ carrier ⇒
    **not mixing** (a mixer would track f_c). [F]/[V]
  - (2c) **the cubic is the event** — crossing the spinodal flips discontinuously; deleting −s³ destroys
    the threshold. The carrier collapses onto ONE discrete event. [F]/[V]
- **(3) band-from-τ.** Larger recovery τ ⇒ lower output band; the band is manufactured by the recovery,
  **not** inherited from the light. [F]/[V]

## Honesty / firewall
E5 is pure sensory **mechanism** — no disease, diagnostic, or clinical claim (that layer is E4,
firewalled). No constant is fitted: γ(GUCY2D) is read byte-equal from the frozen atlas, D is the
inherited invariant, ν=c/λ and E=hc/λ are forced, the switch math is the vendored R19 field, SEED=19.
The substrate cannot carry 10¹⁴ Hz literally, so the **mechanism** is shown at a tractable ratio
(substrate-time) and the **magnitude** is accounted separately — both stated openly. Absolute biological
Hz at each rung is a named **[O]**.

## Next
E6 — *why the band is VISIBLE*: the §10.9 geometric placement [F] (already in the canon) **plus** the
photochemical energy window (reversible 11-cis→all-trans isomerisation ~1.8–3.3 eV) that pins ~380–750 nm
[L] — honest that the chromophore energy is coding/photochemistry, outside the promoter-γ ([O] for the
molecular tuning). Then E7 (cascade as the band-setting low-pass) and E8 (graded → spike-rate hand-off).
