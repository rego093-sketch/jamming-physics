# INTEGRATION — `vp_frontal` inside the mind v1.57 corpus (decoupled)

This bundle is the **mind v1.57 cross-axis-synthesis** package with the **independent `vp_frontal` simulation merged in** as a co-located but **decoupled** subtree. The two share the same frozen R19 engine, but they **run separately**.

## The decoupling contract (non-negotiable)

- **One bundle, two runners.** `repro/mind/` is the heavy atlas (28 modules; `run_all_atlas.py` re-runs all of them per build, ~40 min). `repro/frontal/` is the lightweight frontal probe with its **own** gate (`repro/frontal/_gate/frontal_gate.py`).
- **The frontal sim NEVER calls the atlas runner.** `frontal_gate.py` carries a hard guard that refuses to run if `run_all_atlas` is ever imported into the process. Wiring the frontal cohort sweeps into the atlas runner would make atlas builds impossible — *you could not even attempt the frontal sim*. That is the whole reason it is decoupled.
- **The frontal sim is self-contained.** It carries its **own** READ-ONLY copies of the engine (`repro/frontal/_engine/vp_mind_engine.py`) and the three reusable layers (`repro/frontal/_layers/`), hash-pinned to the same digests as `repro/mind`. It does **not** import anything from `repro/mind`. Co-located, not coupled.
- **The engine is byte-identical across both.** `repro/frontal/_engine/vp_mind_engine.py` and the mind engine share sha `e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371`. The frontal tripwire reproduces the M9 anchor `R = 0.38961455156044245` **bit-for-bit** via the engine integrator and asserts the engine tree + M0–M16 subtree are byte-unchanged.

## What `vp_frontal` is — a preserved honest negative

F1 asked whether the engine's cortical node is a temporal chain-holder, then tried to FIND the frontal-lobectomy patient record in the simulation. The robust answer: the engine identifies the cortical node's **static structure** (lowest fan-in → not a gatherer; a fast 40 Hz broadcaster) but reproduces **no robust frontal-lesion behavioural phenotype** — temporal-holding is negligible under seed-averaging, and the leucotomy perseveration signal flips sign under a duration sweep (an operating-point artefact). This is **Hard Limit 1** in its strongest form: a 12-node engine with an undifferentiated cortical lump cannot carry a stable frontal phenotype.

**The failure is kept on purpose.** It is fully recorded, gated and reproducible — the honest starting line for a future v2 attempt that resolves cortical microstructure (a substrate that would, by design, break the frozen engine). Next time, properly.

## How to run

```bash
# the decoupled frontal sim (independent of the atlas):
cd repro/frontal
python3 _gate/frontal_gate.py --full-tree            # -> FRONTAL GATE: PASS

# the mind atlas is unchanged and runs by its own (heavy) path under repro/mind/.
```

## Where things are

```
repro/mind/                     the mind v1.57 atlas (untouched)
repro/frontal/                  the decoupled frontal sim (self-contained)
  _engine/ _layers/ _frontal/ _gate/
frontal_sim/                    frontal docs:
  README_frontal_sim.md
  WHITEPAPER_F1_frontal_temporal_holding.md   (English; the F1 chapter + the 3 honest negatives)
  GOVERNANCE_frontal_sim.md                   (Korean; decoupling + gate policy + failure preservation)
  HANDOVER_frontal_v0_1_to_next.md            (Korean; result + v2/F2/F3 plan)
INTEGRATION_frontal_decoupled.md              (this file)
```

No file under `repro/mind/` was modified by the integration; the frontal sim was only **added**.
