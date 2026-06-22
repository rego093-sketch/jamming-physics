# vp_frontal — VP Frontal Simulation (independent, decoupled)

An **independent** scientific-computing probe in the VP / Jamming-Physics framework. It shares the frozen R19 engine and three reusable layers (e0/e1/e2) from the `mind` v1.57 atlas **READ-ONLY** (hash-pinned), has its **own lightweight gate**, and **never** calls the atlas runner `run_all_atlas.py`. It is **not** the 29th atlas citizen.

## Why independent (the decoupling contract)
The atlas runner re-runs all 28 modules per build (~40 min, linear in module count). The frontal work involves cohort sweeps; wiring it into the atlas runner would make atlas builds impossible — *you could not even attempt the frontal sim*. So the frontal probe is co-located but decoupled: a self-contained subtree (`repro/frontal/`) with its own engine/layer copies and its own gate (`repro/frontal/_gate/frontal_gate.py`). A hard guard in the gate refuses to run if the atlas runner is ever imported.

## F1 result — a preserved honest negative (the failure, kept on purpose)
The probe document `frontal_lobe_hypothesis.md` is treated as a **candidate idea, not a specification**. Re-establishing the question on the frozen engine under anti-tuning, and then trying to FIND the frontal-lobectomy patient record in the simulation (input → process → output):

- **The cortical node is NOT a gatherer** — lowest effective fan-in (≈1, rank 1/12); the thalamus is the convergence hub (≈4.95). Robust **[V mech]**. Refutes "frontal = convergence node".
- **The cortical node is a fast broadcaster** — low fan-in, moderate-to-high out-influence at 40 Hz. Robust **[V mech]**.
- **The engine reproduces NO robust frontal-lesion behavioural phenotype.** Three honest negatives:
  1. *Temporal holding* — seed-averaged perturbation-recovery finds silencing the cortical node negligible; holding lives in slower subcortical hubs. **[O]**
  2. *Leucotomy perseveration* — disconnecting the cortical node (the faithful tract-severing lesion) gives a clean perseveration/set-shifting deficit at one phase duration, but the sign **flips** across a duration sweep (more-flexible ↔ perseveration). An operating-point artefact. **[O]**
  3. *Only robust behavioural fact* — removing the cortical node is nearly silent (perception spared), because the node is **peripheral to coherence**, not because of a frontal function.
- **Why:** Hard Limit 1 in its strongest form — a 12-node engine whose cortical node is an undifferentiated lump cannot carry a stable frontal phenotype. The model **generates** sharp frontal hypotheses but the frozen engine **cannot confirm** them; a real test needs a v2 substrate that would break the frozen engine.

**This is kept deliberately.** A failed probe, fully recorded and reproducible, is the honest starting line for a future v2 attempt — *next time, properly.*

## Layout
```
repro/frontal/
  _engine/   frozen R19 engine (READ-ONLY, sha e61083ae…) — byte-identical to repro/mind's engine
  _layers/   e0/e1/e2 reusable layers (READ-ONLY, hash-pinned)
  _frontal/  frontal_common.py, frontal_f1_temporal_holding.py
  _gate/     provenance.json, engine_tripwire.py, frontal_registry.py, frontal_gate.py
frontal_sim/   (docs)  README, WHITEPAPER_F1, GOVERNANCE, HANDOVER
```

## Run (independently — never via the atlas runner)
```bash
cd repro/frontal
python3 _frontal/frontal_f1_temporal_holding.py        # F1 module (prints PASS)
python3 _gate/engine_tripwire.py --full-tree           # substrate integrity (~29 s)
python3 _gate/frontal_gate.py --full-tree              # full gate -> PASS
```

## Discipline
READ-ONLY engine · `new_tuned_constants = 0` · SEED = 19 · anti-tuning sweeps + seed-averaging · honest grading [V]/[L]/[O] · English-only body · efficacy = 0 · NOT medical advice · Axis-A firewall (`consciousness_claim = 0`) · hard problem OPEN. The M9 anchor `R = 0.38961455156044245` reproduces **bit-for-bit** via the engine integrator; the engine tree + M0–M16 subtree are byte-unchanged. F1 result sha `21bf28f6…`.

**Next:** F2 (stereotypy = T × W × E0) and F3 (O × W × T × D cohort double dissociation), built on the robust W/T/E0 handles — with F1's caution that the D axis is engine-blind and that any frontal-lesion signature must be shown sign-stable under a duration sweep before it is believed.
