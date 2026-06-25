# Appendix D — challenging the heart: composite renormalization to measured cardiac mechanics

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

The heart **failed** in Appendix A. The morphogenesis gene-clock asked whether the sequence
material **γ** predicts when organ features emerge, and for the heart the answer was an
honest **null** — γ orthogonal to developmental timing, *sharpest in the heart*
(Spearman ρ = +0.071, exact p = 0.882, graded `[O]`). This appendix re-attacks that failure
with the Appendix C renormalization tower **upgraded** to a real two-phase composite and to
**measured** cardiac mechanics, and turns the failure into a mechanistic explanation.

> **반증 = 발견.** The heart's "failure" was the clue. Its developmental stiffening does not
> live on the material-γ axis; it lives on the **ECM-composition axis** the renormalization
> tower exposes. Falsifying the wrong axes reveals the right one.

---

## The question, made measurable

The heart's developmental stiffening is one of the cleanest mechanical datasets in
embryology (Majkut, Idema, Swift, Krieger, Liu & Discher 2013, *Curr. Biol.* 23:2434-2439):

- chick: `E(t) ≈ 0.1 + 0.3·t` kPa (t in days) — approximately **linear**
- murine: `E2 < 1 kPa → E14 ~ 10 kPa` (~10×), the same value measured in neonate and adult
- adult: ~18 kPa (rat, Berry 2006); 10–50 kPa (human)

Proteomics in the same paper identifies the daily drivers of the rise as a small subset of
proteins — **collagen plus excitation-contraction proteins**. So the candidate axes are:
(1) the sequence material **γ**; (2) **pure cell-jamming** (Appendix C, cells in void); or
(3) **ECM composition** (collagen deposition). This appendix decides between them with
measured moduli and exact bounds — no fitted parameters.

## What is upgraded from Appendix C

Appendix C renormalized **one** phase (cells) packed in **void**, and its absolute moduli
were `[O]` placeholders. Two changes make an **accuracy** test possible:

1. **A real two-phase composite.** Myocardium is cells embedded in a stiff collagen ECM, not
   cells in void. The exact elastic-mixture bounds (Voigt 1889 isostrain upper, Reuss 1929
   isostress lower, Hill 1952) bracket the composite modulus with **both** phases real:

   ```
   Voigt (upper)  B_V = φ_cell·B_cell + φ_ecm·B_ecm        [V] exact
   Reuss (lower)  1/B_R = φ_cell/B_cell + φ_ecm/B_ecm       [V] exact
   B_R ≤ B_eff ≤ B_V   (guaranteed; no free parameter)
   ```

2. **Measured cardiac phase moduli** (all `[L]`, cited): single-cardiomyocyte AFM
   (immature hiPSC-CM ~1.25 kPa; adult rat ~35 kPa), decellularized myocardial **ECM**
   (LV ~5 kPa, SAN ~17 kPa), tissue trajectory as above.

## The three results

**RESULT A — pure cell-jamming is insufficient (the falsification, parameter-free).**
Cells in void (Appendix C) cap at `B_eff ≤ B_cell`. The **embryonic** cell is soft
(~1.25 kPa), so cells-in-void can reach at most ~1.25 kPa — yet the tissue stiffens to
~10–18 kPa, a rise of **>10×** past that ceiling. The stiff ECM phase and/or cell maturation
is therefore **necessary**; the pure-jamming tower is **falsified** for the trajectory. This
is a strict inequality on measured moduli — `[V]`. It matches the proteomics exactly
(collagen + EC-proteins drive the daily rise).

**RESULT B — γ is orthogonal to the stiffening (the explanation of the null).**
γ is computed from the genomic sequence, identical at every developmental stage, hence
**time-invariant**. The trajectory rises ~14×. A constant cannot encode a ramp, so γ is
orthogonal to the trajectory **by logical necessity** — which reproduces Appendix A's
measured heart null (ρ = +0.071, p = 0.882) and **explains** it: the timing/stiffening axis
is **composition (ECM)**, orthogonal to the material γ. `[V]` + `[L]`.

**RESULT C — the exact bracket contains the measured tissue (consistency, honest about
sensitivity).** The two-phase bracket from measured ventricular inputs (cell ~35 kPa, LV ECM
~5 kPa, φ_cell ~0.8) is **[15.9, 29] kPa**, which **contains** the measured adult ventricular
tissue (~18 kPa). The measured tissue sits **low** in the bracket because the isolated
single-cell modulus (~35 kPa, transverse AFM) exceeds the in-situ cell contribution — a known
effect. With the stiffer SAN ECM the measured tissue falls below the bracket. So this is a
**consistency** check, not a tight prediction; the sensitivity to cross-study inputs is
exactly why the named obstacle is a single co-registered preparation. `[L]` / `[O]`.

**Illustration (`[F]`).** A composition-flow trajectory — ECM fraction rising and cell
jamming ramping (both monotone, measured-grounded) at **fixed measured** phase moduli —
reproduces the embryonic→adult span (0.16 → 23.5 kPa, monotone, starting soft because the
cell network is unjammed early so the soft cardiac jelly dominates, ending in the adult
band [10, 50]). The schedule *shape* is a modelling choice; the phase moduli are measured.

## The discovery

The heart's developmental stiffening is a **composition + maturation flow** (ECM collagen
deposition + cell jamming), **not** the sequence material γ and **not** pure cell-packing.
Falsifying pure-jamming (Result A) and material-γ (Result B) **reveals** the right axis — and
that axis is exactly why γ was orthogonal to heart timing in Appendix A. The heart is
converted from an **unexplained null** into a **mechanistically explained, exactly bracketed,
falsification-tested** case.

## What is honestly NOT claimed

`completion.complete = False`. This is **not** a 100%-accurate heart. The exact bracket `[V]`,
the falsification of pure jamming `[V]`, the explanation of the null `[V]`, the measured
phase moduli `[L]`, and the bracket-consistency `[L]` are in hand. A **tight zero-parameter
trajectory prediction** is not — three accuracy channels remain `[O]`:

1. **co-registered developmental series** — one preparation giving, per stage,
   `(E_tissue, φ_ecm, φ_cell, B_cell, B_ecm)`. With it the composite predicts `E_tissue(t)`
   with **zero** free parameters and the trajectory match becomes a tight accuracy `[V]`.
2. **active tension** (myosin) vs passive composite — Majkut's contraction wave speed is
   linear in `E_t` (active), distinct from the passive VP elastic wave `c = √(B/ρ)`.
3. **large-strain** nonlinear strain-stiffening — the bracket here is the small-strain modulus.

The distance to a tight accuracy claim is **one named measured dataset**. The machinery, the
measured phase moduli, the falsification, and the explanation are already in place.

## Reproduce

```
python3 run.py            # → expected/*.json + RESULT.txt (deterministic, 2×SHA-256)
python3 -m heart.gate     # → fail-closed D1..D9; exit 0 iff all pass
```

Gate **PASS 9/9** (`D1` two-phase bracket exact · `D2` bracket contains measured tissue ·
`D3` pure jamming insufficient/falsified · `D4` γ orthogonal/reproduces null · `D5`
composition trajectory spans measured · `D6` no magic · `D7` non-fit · `D8` determinism ·
`D9` honest grades). Reference reading hash `a01f16ecc3637ed8`; gate `sha=94355b40c40c3791`.

## Files

```
param_db.json            every measured cardiac input (moduli, fractions, trajectory) with grade + provenance
heart/
  lock.py                the locked measured surface; zero inline magic numbers
  composite.py           the exact two-phase Voigt/Reuss bracket (cell + ECM); VP wave speed
  trajectory.py          measured tissue trajectory + predicted composition-flow trajectory
  decomposition.py       RESULT A (falsification), B (null explained), C (bracket consistency)
  grading.py             the one place precision ≠ accuracy; honest ledger + completion
  interpreter.py         interpret_heart() — the full accuracy reading; reading_hash
  gate.py                fail-closed D1..D9
run.py                   top-level runner → expected/ + RESULT.txt
README.md / LEDGER.md    this file / the auto-generated grade ledger
expected/                reference outputs (byte-identical across runs)
```

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증 = 발견.*
*The heart that failed is now understood — its stiffening axis identified, its modulus*
*bracketed by measured phases, its prior null explained. One co-registered measurement closes it.*
