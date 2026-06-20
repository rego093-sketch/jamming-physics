# repro/mind/04-em-brainwave

EMERGES OFFLINE (module M1 of the in-package engine, `../_engine/vp_mind_engine.py`,
`emerge_brainwave()`). Coupled excitatory/inhibitory populations produce a local field
potential with a slow theta band (~0.008) and a fast gamma band (~0.049) in the engine's
dimensionless time; theta/gamma nesting ~6.1 (within working-memory 7+-2). The synchronous
gamma current is radiated through the driven wave equation u_tt = c^2 grad^2 u + f (the neuro
chain's emission engine); the emitted front travels at 1.01 c with non-zero radiated energy.

GRADES: emission exists and propagates at the wave speed c [V] verified in code; band ordering
theta < gamma [F] forced by the substrate; absolute hertz and radiated POWER in watts (antenna
efficiency) [O] open. The field is a real EMISSION (what EEG/MEG record).

Module M8 (`emerge_field_coherence()`) then EMERGES the brain-scale coherence of that
classical field: solved across a brain-sized transect (exact lossy-medium Maxwell wavenumber,
cross-checked by a numerical solve, swept 1-100 Hz), coherence across the brain ~0.998, with
the brain only ~1e-4 of a wavelength and skin depth >600x its width. So the old coherence-
length rejection is a CATEGORY ERROR: it imported the QUANTUM decoherence length (~1e9-1e10x
too short, Tegmark 2000) for a CLASSICAL field. Whether the field is the binding MEDIUM stays
OPEN [O] — that depends on field STRENGTH / ephaptic efficacy, which is NOT emerged here (no
claim either way; cf. McFadden's cemi field theory). See docs/mind/02-not-a-field.

Reproduce: `cd ../_engine && python3 run_all.py`, then `cd ../_verify && python3 run_regression.py`.
