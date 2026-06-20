# Chapter 26 — The plasticity layer: consolidation and the reversible→chronified switch

**Status (v1.34):** in-silico mechanism on the READ-ONLY engine cerebrum. **efficacy = 0 ·
NOT medical advice.** Every value below is an in-silico coupling state, **not** a clinical
measure, dose, or protocol. A retained structural trace is a *mechanism boundary*, not a
claim about the felt quality of learning, stimulation, or chronic illness (Axis-A firewall;
consciousness_claim = 0; hard problem OPEN).

The **plasticity / consolidation layer** (roadmap target **E0**) the structural atlas never
had. The frozen engine has **no plasticity variable** — which is exactly why the θ-cap
chapters (§20–21) could only read the cap as *pacing, not repair* and left its plasticity
sign OPEN. This module adds a slow phase-correlation Hebbian update to the ephaptic kernel
`W` on top of the READ-ONLY engine. It is the **layer, not an application**: the temporal
disorders that use it (depression T1b, bipolar T2b, addiction T3a) are owed to later modules,
and import the reusable `PlasticConnectome` class rather than re-deriving the rule.

## The rule (form forced [F]; rate [O], not tuned)
On phase oscillators the time-averaged STDP window reduces to a function of the phase
difference (in-phase potentiation, anti-phase depression) — Hebb read on phase. With the
steady-state pairwise correlation `C_ij = <cos(θ_j − θ_i)>`:

```
W_ij  ←  max(0, W_ij · (1 + η · C_ij)) ,   then row-renormalise (Σ_j W_ij = 1)
```

The **form** has no free constant (diagonal 0, weights ≥ 0, row-stochastic so the `~1/r³`
ephaptic locality is preserved). The **rate η is [O]** (representative), and every sign below
is required to hold over an η **sweep** (anti-tuning). The coupling-vs-bias map is the **same**
`k = κ/(1−|b|)` [excit] / `κ/(1+|b|)` [inhib], cap `2κ`, used in the schizophrenia and
epilepsy modules — **no new tuned constant**.

## Claims verified (`e0_plasticity.py`)
- **E0.1 — consolidation / after-effect.** Driving the healthy operating point under
  plasticity and then removing the drive leaves `R` at or **above** baseline (0.390 → 0.391,
  ΔR > 0), positive across the η sweep. The substrate for learning, stimulation after-effects,
  and use-dependent change the plasticity-free engine could not represent. (P1 CONFIRMED.)
- **E0.2 — continuous vs periodic dosing (resolves the §20–21 [O]).** The same total cap dose
  delivered **spaced** (periodic ON/OFF) leaves a **larger retained structural trace** `‖ΔW‖`
  (0.225) than **massed** (continuous, 0.115) — a spacing effect from pure phase-plasticity,
  holding at every point of an η×epochs sweep. With plasticity the cap **repairs** (a lasting
  trace exists) and **pacing beats holding** (pulse, do not hold). Sign-only. (P2 CONFIRMED.)
  *The robust signal is the structural trace `‖ΔW‖`; post-drive `R` is usually but not always
  higher for spaced — reported, not asserted.*
- **E0.3 — the reversible→chronified switch.** **Without** plasticity (η=0) a faulted
  excitatory excursion fully **reverts** when the bias is removed (`R` back to baseline
  exactly) — the §20 "paces not repairs / no rebound" result, now shown to be a *consequence
  of the plasticity-free substrate*. **With** plasticity (η>0) the same excursion leaves a
  retained trace that does not revert (`R` 0.394 > 0.390): a faulted state writing itself into
  the structure. **Plasticity is the switch between a reversible state and a chronified one.**
  (P3 CONFIRMED. *Monotonicity in exposure is false and is not claimed.*)
- **E0.4 — engine-invariance guard.** With η=0 the layer reproduces the frozen M9 coordination
  anchor **bit-for-bit** (`R = 0.38961455156044245`) and leaves `W` identical to the kernel —
  a pure add-on.

**Owed [O]:** the rate η (representative; only the signs are asserted, over a sweep); the
applications (depression / bipolar / addiction are later modules); and which real plasticity
rule(s) operate (real plasticity is heterogeneous — LTP/LTD, STDP, homeostatic scaling,
metaplasticity — only the phase-correlation Hebbian sign and its three consequences are
asserted).

## Reproduce
```
cd ../_verify && python3 run_all_atlas.py
```
`e0_plasticity_results.json` → `5dbfd6df…`. The engine tree stays `0fbf4988…` and the engine
file `e61083ae…` byte-unchanged (the E0.4 guard makes this operational at the layer level).
See `_verify/e0_plasticity.py`; the reusable layer is the `PlasticConnectome` class.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1 ·
hard_problem_open 1.
