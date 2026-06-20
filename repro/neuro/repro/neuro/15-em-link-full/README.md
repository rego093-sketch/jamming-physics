# §15 — The full EM link: conduction–radiation separation and matched-filter multiplex

`vp_em_link_full.py` is the production implementation of the unified ion → lattice → ion
electromagnetic link, clearing the two debts of the earlier prototype with **absorbing
(sponge-PML) boundaries** and **matched-filter receivers**. It runs on the same elastic
lattice as light (u_tt = c²∇²u + f, c² = B/ρ).

**Part A — 3-D dipole on a PML lattice (the near→far transition).** An oscillating ionic
dipole radiates on a 3-D lattice with a graded absorbing layer on all six faces. With the
boundary reflections removed, the shell-averaged field separates into a steep near zone
(∝1/r², the conduction / quasi-static regime, χ→0) and a far zone (∝1/r, radiation, χ→90°),
crossing over at the near-field boundary r ≈ λ/2π; the wavefront propagates at c. This is the
lattice confirmation of the conduction↔radiation split that the geometry forces `[V]`.

**Part B — 1-D PML lattice + matched-filter multiplex (the real cross-talk).** Several
channels at distinct carriers are summed on one linear lattice with absorbing ends; a matched
filter (windowed single-bin projection = the matched filter for a sinusoid, carriers placed on
exact DFT bins) separates each channel. The off-diagonal leakage is ~10⁻⁷ — orders of magnitude
below the prototype's wide-band figure and near the analytic ideal; every channel is recovered
to within rounding `[V]`.

Run: `python3 vp_em_link_full.py` (deterministic; 3-D PML + 1-D matched filter, 2× sha256 identical).

**Guardrail / boundary.** The near-field conduction is the neural signal; the field is at c.
The action-potential *speed* (0.5–120 m/s) is the membrane-charging (RC) regeneration rate — a
separate quantity from the field speed, which myelin increases (saltatory). A strong far-field
radiative broadcast is negligible by geometry (λ = c/f huge ⇒ near-field everywhere biological),
so EEG/MEG is the measurable near-field, not a radiated carrier. The absolute radiation
efficiency αₑₘ stays `[O]`. How θ/γ streams become thought/experience is deferred to the Mind paper.
