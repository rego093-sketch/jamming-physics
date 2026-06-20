# repro/mind/05-memory-physics

EMERGES OFFLINE (module M2 of the in-package engine, `../_engine/vp_mind_engine.py`,
`emerge_memory()`). Hippocampal engram cells are R19 bistables. WRITE = Hebbian outer-product,
deepening the stored pattern's attractor (basin ~56x the single-cell spinodal); a written
pattern self-sustains with no cue (overlap 1.0). RETRIEVE = pattern completion: a 10% partial
cue completes to the full memory (overlap 1.0 for cue fractions 0.1..0.7). Long-term capacity
= 21 patterns in 120 cells (~0.18/N, Hopfield order ~0.14). THETA-PHASE separation (Hasselmo):
writing on one theta phase and retrieving on the other drives catastrophic interference from
~0.036 (interleaved) to 0.0 (separated) — the emerged theta brainwave (M1) is the clock that
protects memory. Working-memory capacity = the theta/gamma slot count (~6) from M1.

GRADES: attractor storage, cue completion, capacity, and theta-phase interference protection
[V] verified in code; absolute synaptic depth (mV), theta period (ms), current scale (uA)
[O] open (needs membrane RC + channel densities this engine does not carry).

Reproduce: `cd ../_engine && python3 run_all.py`, then `cd ../_verify && python3 run_regression.py`.
