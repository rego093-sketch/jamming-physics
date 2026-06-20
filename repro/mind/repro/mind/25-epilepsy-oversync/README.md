# Chapter 25 — Epilepsy: the over-synchronisation pole

**Status (v1.33):** in-silico mechanism on the READ-ONLY engine cerebrum. **efficacy = 0 ·
NOT medical advice.** Every value below is an in-silico coupling state, **not** a clinical
measure or dose. The collapse of the selective gate is a *mechanism boundary*, not a claim
about ictal experience (Axis-A firewall; consciousness_claim = 0).

Second chapter of the **transdiagnostic fault-axis atlas** extension (roadmap target
**T2a**). Epilepsy is the framework's *own* over-synchronisation failure mode — the ceiling
the θ-cap (§20) must stay below — made the object of study; the cleanest dynamical fit in the
atlas.

## Claims verified (`epilepsy_oversync.py`)
On the synchrony axis (global Kuramoto order parameter `R` on the measured ephaptic kernel,
plus the M3 R19 ignition gate):
- **EP1 — over-sync axis.** An excitatory/disinhibitory E/I bias raises `R` **monotonically**
  toward an over-sync **ceiling at 0.422** (health 0.390): 0.390 → 0.399 → 0.406 → 0.411 → …
  → 0.422.
- **EP2 — ictal gate collapse.** As the bias rises the selective single-winner gate leaks
  (2 → 3 → 5 ignited) and, past a critical bias (**+0.3**), **collapses entirely** — all six
  candidate assemblies ignite at once (the ictal state, loss of gating).
- **EP3 — anticonvulsant sign (sign-only).** From an ictal bias, an inhibitory /
  threshold-raising (GABAergic anticonvulsant-class) push moves `R` back **down**
  (0.411 → 0.406 → 0.399 → 0.384 → 0.366) and **restores the selective gate** (6 → … → 0),
  raising the seizure threshold (moving the operating point away from the ceiling).
- **EP4 — axis ordering.** On one synchrony axis: **autism-T (under-ignited, R 0.379) <
  health (selective, 0.390) < schizophrenia (aberrant, 0.401) < epilepsy (all ignited,
  0.422)**. The over-sync ceiling here is the same ceiling the θ-cap must stay below.

**Owed [O]:** this module characterises the *static* susceptibility — how close the operating
point sits to the over-sync ceiling and which way each handle moves it — but **not** the
*ictal time-course*. The onset/offset dynamics (interictal ↔ ictal transitions over time) are
a movement *between* attractors and require the state-switching layer (**E2**) the roadmap
reserves for the episodic disorders.

## Reproduce
```
cd ../_verify && python3 run_all_atlas.py
```
`epilepsy_oversync_results.json` → `d363f0a5…`. The engine tree stays `0fbf4988…` and the
engine file `e61083ae…` byte-unchanged. See `_verify/epilepsy_oversync.py`.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1.
