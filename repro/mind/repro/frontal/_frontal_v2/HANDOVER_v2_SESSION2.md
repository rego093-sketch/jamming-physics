# vp_frontal v2 — Session-2 Handover Note

**One bounded load this session: Chunk A — ST-1 (EM field-efficacy robustness).**
**Outcome: the causal window SURVIVED the stress test.**

> The living plan is `START_HERE_HANDOVER_v2.md` (now updated through S2). This note is the Session-2 record. The Session-1 record is `HANDOVER_v2_SESSION1.md` (frozen, untouched).

---

## What was done

Built `repro/frontal/_frontal_v2/field_efficacy_robustness.py` and ran it to completion.

- **Non-circular by construction:** it imports the EXACT Gap-1 `pci_analog` from `cognition_consciousness_body.py` — the stress test attacks the real code, not a re-implementation.
- **Engine untouched:** asserts the M9 anchor `R = 0.38961455156044245` bit-for-bit on every run; `new_tuned_constants = 0`; frozen kernel READ-ONLY.
- **Sweep (anti-tuning discipline):** 3 seed cohorts (19–22, 23–26, 27–30) × 3 durations (0.4/0.6/1.0 s) × 4 perturbation nodes (neocortex, thalamus, hippocampus, striatum) = **36 cells**, each over couplings `[0,1,2,3,5,8] × measured κ` (κ = 0.5496). Abs PCI margin 0.012.
- **Three signed, falsifiable features per cell:** `F_necessity`, `F_collapse` (interior peak **and** real over-drive drop), `F_dissociation` (arousal ↑ while access turns over). Believed only if **sign-stable** across all 36.

## Result

Every cell peaks at **3× measured coupling**. `window_sign_stable = True`, `broke_on = []`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| necessity | 36 | 0 | 0 | True |
| over-drive collapse | 36 | 0 | 0 | True |
| dissociation | 33 | 0 | 3 | True |

The 3 ambiguous cells are 0.4 s runs with a tiny arousal wiggle — not contradictions; evidence the classifier is not rubber-stamping.

**Baseline (seeds 19–26, T 0.6, neocortex):** PCI 0.068(OFF) → 0.118(measured) → 0.126 → **0.131(peak@3×)** → 0.110 → 0.081(8×); activity rises monotonically 0.256 → 0.709.

## Grade & honest residual

- **Gap-1 → `[L]` in-silico** (the window survives stress). What survived is the **dissociation / window shape**.
- **`[O]` preserved (unchanged from S1):** the peak sits ~3× **above** the measured coupling, so "criticality AT the measured coupling" is *not* shown. The in-vivo test (field cancel / augment) is still owed.
- Firewall held: `consciousness_claim = 0`, `hard_problem_open = 1`. Function modeled; experience not. This is an in-silico model stress-test result — **not** validated neuroscience and not clinical guidance.

## Artifacts (in `repro/frontal/_frontal_v2/`)

- `field_efficacy_robustness.py` — the module (resumable, budget-bounded, deterministic → cells are call-invariant).
- `field_efficacy_robustness_results.json` — internal digest `05a7d317…`, matches `expected_field_efficacy_robustness_sha256.json`.
- `field_efficacy_robustness.png` — 2-panel: PCI window (interior peak) + monotone arousal, verdict in suptitle.

## Next session — Chunk B (per Section 5 of the whitepaper)

ST-1 did **not** break, so the plan proceeds (no restart owed).

**Chunk B = Gap-2 build:** additive cortical micro-model (cortico-cortical hubs + reentrant loop, hippocampus-precedent style — must keep M9 bit-identical), **then ST-2** (cortical micro-model non-circularity: does the frontal phenotype appear in a read-out independent of the perturbed edge, and is set-shifting sign-stable under a duration sweep?). *Break for ST-2:* the phenotype only appears in a circular read-out, or flips. *If broken:* reconsider resolving cortex **inside** the kernel — which breaks M9 (a major fork).

*Apply the Stress Principle — build it, then break it before trusting it.*
