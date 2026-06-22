# vp_frontal v2 — Session-5 Handover Note

**One bounded load this session: Chunk D — Gap-4 build (PCI clinical match via the emerged M14 sleep architecture) + ST-4.**
**Outcome: the CONSCIOUS/UNCONSCIOUS PCI split (wake≈REM ≫ NREM) SURVIVED the stress test (sign-stable separation); the within-unconscious ordering (NREM/anaesthesia/VS) COLLAPSED to one scalar — recorded honest negative `[O]`.**

> The living plan is `START_HERE_HANDOVER_v2.md` (now updated through S5). This note is the Session-5 record. The Session-1…Session-4 records (`HANDOVER_v2_SESSION{1,2,3,4}.md`) are frozen, untouched.

---

## What was done

Built two modules in `repro/frontal/_frontal_v2/` and ran both to completion: the Gap-4 PCI build, then its stress test. Engine READ-ONLY; `new_tuned_constants = 0`; M9 anchor asserted bit-for-bit on every run.

### 1. Gap-4 build — `pci_clinical_match.py`

Drives the **frozen M9 kernel** through the **emerged M14 sleep architecture** and scores a **faithful perturbational complexity index (PCI**, the clinical bedside consciousness measure). The point of the build: see whether the clinic's PCI ordering falls out of the kernel **with no new constant**.

**Grounding (the state→mechanism map is fixed by M14, not by us).** `emerge_sleep_architecture()` (M14) already emerged, from the frozen kernel + cited kinetics, the activated-vs-bistable distinction the module rides on — and the build **asserts those observables at run start** (it aborts if M14 drifts):
- `shift_index_rem ≈ 1.05` (REM = **activated / desynchronised**, no OFF-periods) ≫ `shift_index_nrem ≈ 0.045` (NREM = **bistable** slow Up/Down, OFF-periods present).
- spindle 15.4 Hz and slow-osc 0.49 Hz matched; `recall_rem 1.0` vs `recall_nrem 0.53`.
- the firewall holds inside the grounding source too: `is_consciousness_claim = 0`, `hard_problem_open = 1`.

So WAKE/REM are driven with the slow-adaptation **off** (`off_depth = 0`, activated tonic) and NREM with full bistability (`off_depth = 1`) at the cited nrem2 drive — no state we did not earn.

**The mechanism scored (the M14 construction, READ-ONLY engine helpers).** A 16-cell cortical population of R19 cubic-bistable cells (`s − s³ + drive − a`) coupled diffusively through the **M9 ephaptic ring at the measured κ = 0.5496**. The state is set **only** by `off_depth × A_GAIN` and the cited carrier — activated theta-gamma (`f ≈ 23.5 Hz`, atlas f0) for wake/REM, slow 0.5 Hz for NREM. Every quantity is measured: κ; `A_GAIN = 1.6`; `TAU_SO = 0.600 s` (Sanchez-Vives & McCormick 2000); `TAU_S = 0.025 s`; `drive = 0.60` (Steriade 1993). `new_tuned_constants = 0`.

**The faithful, non-circular PCI.** A single TMS-like kick (`+2.0` to one cell, 4 ms after a 4 s settle) is applied to a **perturbed** twin; an **unperturbed** twin shares identical initial conditions. PCI = **normalised Lempel-Ziv complexity of the binarised perturbed-minus-unperturbed causal divergence** over a 1.5 s post-pulse window (downsample 8×, binarise `D > D.mean()`). Subtracting the twin removes spontaneous activity → with no kick the divergence is identically zero → **PCI = 0 for every state** (the non-circular control). The LZ core (`lz76` / `normalised_lz`) is **imported** from `cognition_consciousness_body` (non-circular at the code level).

> *Why this readout (preserved learning from four prototypes).* A spatial-median-of-raw-response readout *worked* (0.48 vs 0.14) but its no-perturbation control gave Δ = +0.795 — i.e. it scored **spontaneous** complexity (REM diverse, NREM stereotyped), not **perturbational** complexity, so it was rejected as unfaithful to Casali PCI. Two other readouts (raw deviation + global-mean binarize; pre-stimulus significance threshold) gave degenerate values. The **twin-divergence** readout is the one that is genuinely perturbational (no kick → 0) and is what shipped.

**Found (build).** PCI by state (9-seed cohort; deterministic):

| state | grounding | PCI | raw activity |
|---|---|---|---|
| WAKE | grounded (off=0) | **0.464** | 1.221 |
| REM | grounded (off=0) | **0.464** | 1.221 |
| NREM | grounded (off=1) | **0.036** | 0.874 |
| ANES | extended (off=1.6) `[O]` | 0.048 | 0.879 |
| VS | extended (off=2.4) `[O]` | 0.081 | 0.871 |

- **Conscious/unconscious split is clean:** wake ≈ REM (0.464) ≫ NREM (0.036), Δ = **+0.428**, across the clinical cutoff `PCI* ≈ 0.31` (Casarotto 2016). The bistable OFF-periods truncate the evoked causal chain (Massimini 2005; Pigorini 2015), collapsing complexity.
- **Non-circular control:** no kick → PCI = **0.000** for every state.
- **Dissociation from arousal:** the unconscious states still carry substantial raw activity (0.87–0.88) yet collapse PCI, and the activity ordering does **not** track the PCI ordering — PCI is not an arousal proxy.
- **Honest negative (recorded in the build):** the single PCI scalar does **not** resolve the fine unconscious ordering — NREM/anaesthesia/VS collapse to ~one value (spread **0.045**), "deeper bistability → monotonically lower PCI" **breaks**, wake ≈ REM exactly.
- **Grade:** `[L]` in-silico conscious/unconscious split (sign-stability then pending ST-4); `[O]` within-unconscious ordering, wake-vs-REM gap, absolute magnitudes, felt quality. Internal digest `bde77370…`.

### 2. ST-4 — `pci_clinical_match_st4.py`

Imports the **exact** build model (`pci`, `STATES`, `ground_sleep_architecture` — the stress test attacks the real model). Asserts the M9 anchor bit-for-bit and re-asserts the M14 grounding; `new_tuned_constants = 0`.

- **Sweep:** 3 seed cohorts (C1 19–22, C2 23–26, C3 27–30) × post-pulse windows 1.0 / 1.5 / 2.0 s = **9 cells**, margin 0.05.
- **Three signed, falsifiable features:** `F_rem_gt_nrem` (PCI_REM − PCI_NREM > margin), `F_wake_gt_nrem`, `F_conscious_separated` (`min(wake,REM) − NREM`; scored −1 if an unconscious PCI reaches a conscious one). Believed only if **sign-stable** across all 9.
- The within-unconscious spread is reported **separately** as the recorded `[O]` (not a sign-stable claim).

## Result

The conscious/unconscious split SURVIVED. `conscious_unconscious_separation_sign_stable = True`, `broke_on = []`.

| feature | support | contradict | ambiguous | sign-stable |
|---|---|---|---|---|
| REM > NREM (PCI_REM − PCI_NREM > margin) | 9 | 0 | 0 | True |
| WAKE > NREM (PCI_WAKE − PCI_NREM > margin) | 9 | 0 | 0 | True |
| conscious separated (min(wake,REM) − NREM > margin) | 9 | 0 | 0 | True |

The conscious−unconscious margin ranged **+0.347 → +0.481** across the post-window sweep (always ≫ margin); the within-unconscious spread stayed **0.025 → 0.045** (always < margin), and "deeper → lower PCI" held on **no** cell. Internal digest `2ada85a4…`.

**Engine invariance (re-verified S5):** M9 anchor `R = 0.38961455156044245` bit-for-bit (engine ↔ frontal integrator both exact). The additive discipline held — the frozen kernel is byte-unchanged.

## Grade & honest residual

- **Gap-4 → `[L]` in-silico for the CONSCIOUS/UNCONSCIOUS split.** The clinical PCI's core finding (a conscious/unconscious *binary*) falls out of the frozen kernel with no new constant, once the M14 activated-vs-bistable distinction is in place. Held at arm's length as an *in-silico perturbational-complexity* result, **not** a clinical measure.
- **`[O]` — the within-unconscious ordering COLLAPSED (recorded, not avoided).** The single PCI scalar does **not** separate NREM vs anaesthesia vs VS (spread 0.045 < margin on every cell); the clinic's *full* ordering (NREM > anaesthesia > VS) is **not** reproduced. This is scientifically sensible: PCI's clinical strength **is** the conscious/unconscious binary, not fine unconscious discrimination — so the collapse is the *expected* honest negative, not a surprise failure.
- **`[O]` wake ≈ REM exactly.** The mechanism cannot resolve the small clinical wake>REM gap (`|wake − REM| = 0.000`).
- **`[O]` ANES/VS are an extended sweep.** They have **no** M14 grounding (no emerged sleep stage behind them) — they are a deeper-bistability extrapolation only.
- **`[O]` magnitudes.** Absolute PCI values are model units, not clinical PCI numbers.
- **Anti-tuning note:** the separation is post-window-invariant in **sign** (the sweep confirms **no flip**), with the margin shrinking smoothly as the window lengthens (longer windows let NREM accrue a little complexity) — never crossing.
- Firewall held: `consciousness_claim = 0`, `hard_problem_open = 1`. Function modeled; experience not. This is an in-silico model stress-test result — **not** validated neuroscience and not clinical guidance.

## Artifacts (in `repro/frontal/_frontal_v2/`)

- `pci_clinical_match.py` — the Gap-4 build (M14-grounded sleep states + twin-divergence PCI; deterministic → cells are call-invariant).
- `pci_clinical_match_results.json` — internal digest `bde77370…`, matches `expected_pci_clinical_match_sha256.json`.
- `pci_clinical_match_st4.py` — the ST-4 stress test (imports the exact build model).
- `pci_clinical_match_st4_results.json` — internal digest `2ada85a4…`, matches `expected_pci_clinical_match_st4_sha256.json`.
- `pci_clinical_match.png` — 2-panel: PCI by state vs the clinical cutoff + the PCI-vs-activity dissociation.
- `pci_clinical_match_st4.png` — 2-panel: per-cell PCI bands (conscious vs unconscious) + the signed separation margins, verdict in the suptitle.

## Next session — Chunk E (per Section 5 of the whitepaper)

ST-4 did **not** break the split (no restart owed); the within-unconscious collapse is a recorded `[O]`, by design — it does **not** trigger a Chunk D restart (the part that was claimable, the binary, survived).

All four fillable gaps (1–4) have now either survived their stress tests or carry recorded honest negatives:
- Gap-1 `[L]` (field causal window, S2) · Gap-2 `[L]` (cortical micro-model, S3) · Gap-3 `[L]` (O×W crossover, S4) · Gap-4 `[L]` conscious/unconscious split + `[O]` within-unconscious ordering (S5). Gap-5 remains the explicit firewall blank.

**Chunk E = the integration pass:** re-run the whole chain with the surviving hypotheses applied; update grades end-to-end; produce the **v2 atlas**. This is the step that moves Sim 2 toward its end condition (Section 7). ~1 session.

*Apply the Stress Principle — build it, then break it before trusting it.*
