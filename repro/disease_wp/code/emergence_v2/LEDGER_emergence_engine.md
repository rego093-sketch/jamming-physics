# LEDGER — DB-grounded dynamical emergence engine (phase 1: cardiac)

Honest, per-quantity grading under the project's C3 discipline. The engine replaces the old
target-fitting geometry with a forward run that **uses** the systemic parameters, and reads them
from a **locked, cited parameter DB** (`param_db.json`) — never from the validation targets.

**The legitimacy rule (author-directed):** a parameter is a valid input if it is (a) a UNIVERSAL law
or (b) an INDEPENDENTLY measured/published value, carried in the DB with provenance. A parameter is a
violation only if WE chose it to match a target. The gate's **NON-FIT invariant** asserts the engine
never reads a target, so every DB value is a locked input `[L]`, not a back-fit.

| quantity | grade | basis |
|---|---|---|
| one switch `spinodal(γ)=2(γ/3)^1.5` | **[V]** | identical to the body/neuro engines (imported, unchanged) |
| measured γ (cardiac masters) | **[L]** | NCBI→SantaLucia, read-only, corr(γ,GC)≈0.99 (package table) |
| intrinsic emergence **ORDER** = argsort(spinodal γ) | **[V]** | deterministic γ-readout (gate check 3a) — a property of γ, **biologically null** (the package's measured ρ≈0.07) |
| **WHEN** — relay onset **order** (systemic) | **[F]** | literature cardiac DAG + relay ODE; differs from γ-order (gate check 3b) — the systemic axis that tracks biology (ρ≈0.44 in the timing test) |
| **WHEN** — onset **absolute hours** | **[L]-grounded** | rate `kd=ln2/τ½` from MEASURED protein half-life 46 h (Schwanhäusser 2011); window ≈184 h (~7.7 d) emerges from physics, **not fitted to days** |
| **HOW BIG** — emergent **size** | **[F]** | `dwell(γ) × (time-available)^α`, α=1 a single UNIVERSAL supply rule applied to all organs identically; magnitudes not validated |
| size **vs real organ mass** | **[O]** | needs a per-organ developmental growth-rate atlas; engine does **not** compare to real mass (would be back-fit) |
| trajectory (continuum 3-D form) | **[O]** | reduced-order RD hook present (morphogen D from DB [L]); full cell-resolution form needs measured tissue mechanics + HPC |

**Gate:** `verify_emergence.py` → **7/7 PASS** (DB-sourced · non-fit invariant · intrinsic-vs-systemic
order distinction · θ-robust [0.3,0.7] · non-blind · determinism 2× sha `939ae9924a` · grades declared).

**What changed vs the old appendix:** the old Layer-2/3 forms hit a TARGET without the systemic
parameter (geometry-only `[O]`). This GROWS a (time, size) form by running γ + measured kinetics +
universal dosage forward, with no target and no fit — moving the absolute **timescale** from display-only
`[F]` to **[L]-grounded**, while the absolute **size magnitude** is honestly `[F]`/`[O]` until a measured
growth atlas replaces the universal rule.

**Phase 1 scope:** cardiac (8 masters). Phases 2–4 (organs+body/face; reduced-order RD trajectory;
fold-in + relabel of the old geometry demos) are the documented next steps.
