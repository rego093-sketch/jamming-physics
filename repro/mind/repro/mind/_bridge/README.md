# `_bridge/` — the cited physics substrate for M11 (light → brainwave → memory)

This folder holds the **physics layer that Felt Cognition §15 cites but does not
re-derive**. The mind package depends on the VP / Jamming-Physics whitepaper
(**DOI 10.5281/zenodo.17932566**) for exactly one fact and its angle theory; M11
(`emerge_light_memory_binding()` in `../_engine/vp_mind_engine.py`) builds a
neuroscience consequence on top of it. The dependency is **one-way and by citation**:
nothing here imports the mind engine, and the mind engine does not import these files —
M11 re-states the bridge constants locally with the DOI cited, exactly as the chain's
single-source rule requires.

## Files

- **`VP_light_to_brainwave_BRIDGE.md`** — the citation bridge. States, with whitepaper
  section references, the pipeline used by §15: a brainwave is *emerged light* on the
  same vacuum lattice (c² = B/ρ), so its per-step carrier angle is θ = 2πa/λ (tens of
  decimals below the point); brainwave EM ⊕ sensory EM superpose; the **signed** phase
  overlap (X₀·cosθ, which cancels) is turned into a **sign-surviving scalar** — an
  information bit — only by geometric **rectification** (single α = ⟨|cos|⟩ = 2/π,
  double δ = ⟨[cos]₊[cos]₊⟩ = 1/π², with 2π = α/δ). The only empirical input anywhere
  is the single optical anchor λ_ref = 632.99 nm; `medium_efficacy_tested` is fixed at 0.

- **`vp_light_brainwave_sim.py`** — the physics demonstration (whitepaper reproduction,
  PARTS 1–3): light emerges as the lattice elastic wave (c² = B/ρ, ω = cq); the angle
  theory (α = 2/π, δ = 1/π², the n-fold law νₙ = nπ^(2(n−1)), the forced-radius
  attractor x* = 2/π); and the *same* light re-emitted at EEG-band wavelengths so the
  carrier angle goes ~10¹³× finer. Deterministic; no fitted parameter drives any
  reported number.

- **`vp_brain_light_memory_sim.py`** — the **standalone end-to-end simulation** that
  motivated this whole upgrade: it fires emergent light from many dephased brain cells
  into a propagating brainwave at the wave speed, adds sensory afferents, superposes and
  **rectifies** their phase overlap into an information bit, **writes** that bit into an
  R19 engram cell when (and only when) it is bound, **rolls** several informations
  through γ slots inside one θ frame, and lets a **downstream neuron entrain** to the
  rolled field (cancel < measured < augment). It is self-contained (depends only on
  numpy) and deterministic. The *governed, gated* version of the same mechanism lives in
  the engine as **M11** and is verified by `../15-light-to-memory/verify_light_memory.py`.

## Grades (honest)

- **[F] forced / cited** — c, λ_ref, the lattice unit a, α = 2/π, δ = 1/π²: taken from
  the cited whitepaper or computed by quadrature; not fitted here.
- **[V] verified in code** — the in-silico mechanism (superpose → rectify → information
  → engram write → roll → downstream read) reproduces bit-for-bit (see M11 + its gate).
- **[I] inference** — that *biology* uses light-rectified binding to write memory. The
  theory does not yet exist; §15 is built by **strong inference** from the cited physics.
- **[O] open** — `medium_efficacy_tested = 0`. No behaviour-labelled, field-cancel-vs-
  augment intracranial recording has been performed; no link is claimed causal; **no
  claim of experience** is made.

Run either simulation from anywhere with `python3 <file>`; both print a sha256 of their
headline numbers and re-run identically.
