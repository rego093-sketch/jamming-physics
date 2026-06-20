# Chapter 24 — Schizophrenia: the over-ignition mirror of autism

**Status (v1.33):** in-silico mechanism on the READ-ONLY engine cerebrum. **efficacy = 0 ·
NOT medical advice.** Every value below is an in-silico coupling state, **not** a clinical
measure, dose, or response rate. Loss of the selective gate is a *mechanism boundary*, not a
claim about the disorganised subjective state (Axis-A firewall; consciousness_claim = 0).

This is the first chapter of the **transdiagnostic fault-axis atlas** extension
(roadmap target **T1a**): re-cutting a condition by the same T/O/W ignitability axes that
carry autism, rather than by symptom checklist.

## Claims verified — the discriminant (`schizophrenia_discriminant.py`)
On the one shared ignitability axis (M3 R19 fold = `spinodal(g) = 2(g/3)^1.5 = 0.3849`,
measured-grounded):
- **SZ1 — over-ignition.** A disinhibitory/excitatory bias (+0.15) **lowers** the fold;
  the ignition threshold drops from health's 0.395 to **0.245**.
- **SZ2 — aberrant salience.** Weak, in-health-sub-fold candidate assemblies (indices 2,3)
  now ignite; the on-set grows from health's {4,5} to {2,3,4,5}, monotone in excitation, with
  **no relevant ignitions lost**.
- **Three-way fingerprint.** (ignition-direction, aberrant-vs-lost) separates HEALTH
  (normal / none / none), AUTISM-T (raised / none lost-relevant), and SCHIZOPHRENIA
  (lowered / recruited-irrelevant / none lost) **uniquely**.
- **RX signs (sign-only).** A uniform gain-reducing / threshold-raising antipsychotic-class
  push restores the healthy selective set {4,5} and **worsens autism-T**; the gain-raising
  stimulant that helped autism-T **worsens** schizophrenia (recruits more aberrant ignitions)
  — one handle, opposite signs at the two poles. The therapeutic (sedating) direction
  **aligns with sleep-need** — the mirror of autism.
- **Extreme limit.** Unbounded disinhibition lowers the fold until **all six** candidates
  ignite — total loss of the selective gate (the disorganisation limit shared with seizure).

## Claims verified — symptom-domain axis map (`schizophrenia_symptom_domains.py`)
The three symptom domains sit on three different T/O/W axes, and a single gain-reducing
operator reaches **only one** of them:
- **POSITIVE → threshold (over-ignition).** Antipsychotic raises the fold back and removes
  the aberrant ignitions — **REACHED**.
- **NEGATIVE → output/gain deficit.** R = 0.354 < health 0.390; the antipsychotic is itself
  a gain *reduction*, pushing output lower still (to 0.309) — **NOT reached** (wrong direction).
- **COGNITIVE → long-range wiring fault.** Locality 0.842 > health 0.794; a scalar gain
  operator leaves the locality imbalance **exactly invariant** — **NOT reached**.
- **DOM4 — discriminant.** One operator reverses POSITIVE only → the differential
  antipsychotic response is **axis-structured, not dose-structured**: the mechanistic account
  of why D2 blockade relieves positive but not negative/cognitive symptoms. Retires *more D2
  blockade* as a route to negative/cognitive benefit (an in-silico mechanistic null).

**Owed [O]:** which pole a given psychosis is, and which domain dominates it, need
per-individual external data (spectral E/I markers, connectomics, genetics); the secondary
global-R rise is engine-internal and is *not* the defining fingerprint (real schizophrenia is
dysconnective).

## Reproduce
```
cd ../_verify && python3 run_all_atlas.py
```
Discriminant `schizophrenia_results.json` → `40b9daff…`; symptom domains
`schizophrenia_symptom_domains_results.json` → `0499f74f…`. The engine tree stays
`0fbf4988…` and the engine file `e61083ae…` byte-unchanged. See
`_verify/schizophrenia_discriminant.py` and `_verify/schizophrenia_symptom_domains.py`.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 ·
no_cure_claimed 1 · hard_problem_open 1.
