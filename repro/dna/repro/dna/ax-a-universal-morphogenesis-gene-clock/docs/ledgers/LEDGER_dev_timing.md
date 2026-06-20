# LEDGER — developmental-timing calibration (v5)

Grading discipline borrowed from the neuro VP-SPEC (C3): every quantity is either a **measured
input** (locked + cited) or a **derived value** — never a number chosen to hit a target. Each open
item names its obstacle. Grades: **[V]** simulation/cross-package verified · **[F]** forced
modelling choice · **[O]** open (the claim was tested and is *not* established) · **[L]** locked
measured input.

## What this is
From v1 the package made a deliberately narrow claim: feature emergence **order** is a deterministic
function of measured promoter-stiffness γ (`order = argsort(spinodal(γ))`), and it **disclaimed** any
match to real developmental timing — that match was logged as the open [O] next step (README v3).

v5 stops disclaiming and **tests it**. It treats canonical human-embryo **Carnegie staging** as a
locked, cited input and asks one question with **zero tuning**:

> Does the package's own γ-derived schedule correlate with the order in which these features
> actually appear in the human embryo?

The grade is then set **by the evidence**, not by hope. This is the governance's whole purpose: a
central open claim is put at risk of falsification, and whatever comes out is reported.

## The result (the headline of this ledger)
**It does not correlate.** On the 7 genuine-master features with a defensible first-appearance stage:

| statistic | value | meaning |
|---|---|---|
| Spearman ρ(spinodal, observed CS) | **−0.018** | essentially zero rank association (and the wrong sign) |
| exact permutation p (n! = 5040) | **0.986** | the observed ρ is utterly typical of random orderings |
| Pearson r | −0.257 | weak, negative, not significant |
| Pearson p | 0.578 | — |

**Conclusion:** measured promoter stiffness γ is **evidently not** the molecular correlate of human
developmental timing. The order claim is therefore graded a **measured [O]** — *tested and not
matching* — which is a **stronger and more honest** position than the prior untested hedge. The
package now *knows* (and reports) that its γ-schedule is an internal ordering device, not a predictor
of real staging.

This is **not a failure of the package**; it is the calibration apparatus doing its job. The
no-tuning rule exists precisely so that a result like this is surfaced rather than massaged away.

## Quantity-by-quantity

| quantity | grade | basis |
|---|---|---|
| first-appearance **Carnegie stage** of 7 master features (PAX2/otic CS9, PAX6/optic CS10, TBX5/upper-limb CS12, LHX2/olfactory CS13, TBX4/lower-limb CS13, HOXD13/digital-rays CS17, PAX9/tooth-germ CS18) | **[L]** | `data/dev_timing.json`, from O'Rahilly & Müller *Developmental Stages in Human Embryos*, Larsen's *Human Embryology*, and the UNSW Hill embryology atlas. **Read-only, cited, frozen by sha256.** Stages are recorded as **ordinals** and scored by **rank** correlation (robust to ±1-stage disagreement between sources). |
| the locked table is **independent of γ** (no back-fitting) | **[V]** | `stages_independent_of_gamma()` — the stage values never reference the γ table; the verifier (check 2) re-derives the sha and confirms the input is fixed before the test runs. |
| the package's derived schedule `= argsort(spinodal(γ))` over the same 7 genes | **[V]** | same `spinodal` as everywhere else; one-switch `< 1e-12` (check 1). The thing being tested is the *real* package output, not a stand-in. |
| ρ / permutation-p / Pearson between derived schedule and observed staging | **[V]** (derived) | computed exactly (full n!=5040 permutation null) in `calibrate()`; **ρ=−0.018, p=0.986**. Deterministic (check 5). |
| **the grade is set by the evidence** (`[V]` iff `perm_p<0.05 AND ρ>0`, else `[O]`) | **[V]** | `verify_dev_timing.py` check 3 enforces **grade == evidence**. PASS means "the reported grade matches what the data shows", **not** "the correlation was good". |
| the apparatus can **detect** a real signal (is not blind) | **[V]** | `apparatus_detects_signal()`: a synthetic γ made proportional to stage → **ρ=1.0 exactly**; a shuffled assignment collapses it (check 4). So the null above is a genuine null. |
| **does γ predict real developmental timing?** | **[O]** | **Answer from this test: no** (ρ=−0.018, p=0.99). Whether *some other* measured molecular quantity predicts staging is the next open question; promoter stiffness γ is now ruled out as that predictor for these features. |
| **absolute ages / hours-post-fertilization** of each event | **[O]** | not modelled; only the **rank order** of appearance is used (the robust, source-agnostic signal). Calibrating to real clock time needs a different dataset. |

## What is explicitly NOT claimed
- **Not** that the emergence order matches biology — v5 shows it **does not** (this is the point).
- **Not** that the framework is therefore wrong: the order is still a valid, deterministic,
  reproducible **γ readout**; v5 only refutes the *interpretation* that this readout tracks real
  staging.
- **Not** that the staging numbers are exact to the stage: they are treated as **ordinals** and
  scored by rank, precisely because sources disagree by ±1 stage.
- **Not** a tuned result. No γ value, no spinodal constant, and no stage was adjusted to change the
  correlation. Doing so would be the exact anti-pattern this gate exists to forbid.

## Invariants to preserve
- `data/dev_timing.json` is **read-only measured**, frozen by sha256; never edit a stage to move ρ.
- γ values remain read-only measured; never tune a γ to make the calibration "pass".
- `verify_dev_timing.py` enforces **grade == evidence** — a green gate certifies *honesty*, not a
  good correlation. If a future measured quantity *does* correlate, the grade flips to [V] **by the
  evidence**, never by hand.
- the calibration must stay **falsifiable**: `apparatus_detects_signal()` (synthetic perfect γ →
  ρ=1.0) must keep passing, or the test has gone blind and any null is meaningless.

## Reproduce
```
cd code
python3 dev_timing.py          # prints ρ, exact permutation p, Pearson, and the evidence-set grade ([O])
python3 verify_dev_timing.py   # 5/5 gate: locked+cited+γ-independent input, grade == evidence, falsifiable
```
Outputs: `results/dev_timing.json` (the numbers) and `results/dev_timing_verify.json` (the gate).
