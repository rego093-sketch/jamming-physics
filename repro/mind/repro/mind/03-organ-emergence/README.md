# repro/mind/03-organ-emergence

EMERGES OFFLINE (module M0 of the in-package engine, `../_engine/vp_mind_engine.py`,
`emerge_organs()`). The four brain organs are emerged from their master-gene bistable
parameter gamma (FOXG1 cerebrum 1.4737, EN1 cerebellum 1.4692, SIM1 hypothalamus 1.4465,
LHX2 hippocampus 1.5172; measured, read-only, vendored in `../_engine/data/brain_organ_gamma.json`).
Each gamma sets an R19 spinodal = 2(gamma/3)^1.5; ordering the organs by ascending spinodal
gives the developmental order hypothalamus -> cerebellum -> cerebrum -> hippocampus. Organs are
present under the "on" developmental drive and absent under "off" (gated emergence).

GRADES: ordering [F] forced by the measured gamma; gated present/absent [V] verified in code;
absolute organ size / cell counts / cortical projection length [O] open (needs developmental
rate constants + a morphogen field this engine does not carry).

Reproduce: `cd ../_engine && python3 run_all.py`, then `cd ../_verify && python3 run_regression.py`
(REGRESSION PASS — determinism + mechanism invariants; consciousness NOT reproduced, hard problem OPEN).
