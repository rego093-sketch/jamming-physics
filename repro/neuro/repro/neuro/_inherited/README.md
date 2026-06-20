# `_inherited/` — light emerged in the quantum basis (the core Mind inherits)

Light emergence and the light angle ARE the core, so the verified quantum-unit
simulation is embedded here for downstream papers (Mind) to inherit directly.
Re-learned from physics §10.9 by reproducing the bundled module (05+06).

- `vp_light_emergence_quantum.py` — **light emerged in the quantum basis.**
  05: the quantum is INVARIANT, D = 2λ_C,e = 2h/(mₑc) = 6π⁶rₚ = 4.852620 pm (derived,
  not assumed). 06: light emerges as the lattice elastic wave c=√(B/ρ), worked in
  quantum units (spacing D, time τ_q) so the speed is exactly 1 D/τ_q. The angle law
  is one right triangle — chain mD = hypotenuse, scaffold mD·cosχ = adjacent, swing λ
  = opposite — giving sinχ = λ/(mD), m=⌈λ/D⌉. Verifies msinχ·D/λ=1, the anchor-free
  633/532 closure (1.189831), the band structure (γ 12° → radio 90°), and the
  rotating-chain vs continuum control (4.5D vs 6.75D, the paper's numbers). D fixed ⇒
  each wavelength has its own angle.

- `vp_color_by_angle.py` — **the eye separates colour by χ.** Red 633nm (89.9378°) and
  green 532nm (89.8248°) sit at distinct angles; near χ=90° the map is hypersensitive
  (a few nm → 0.1°) and, because D=ℓ_rot carries a spread, χ(λ) is a distribution and
  not a smooth monotone — colour discrimination is by the fine angle band, not a sharp
  lookup. This is the angle theory's first biological use.

- `vp_ion_low_frequency.py` — **ions make the low frequency.** The neuron is the R19
  switch + slow recovery = a FitzHugh–Nagumo relaxation oscillator: fast Na⁺ upstroke,
  slow K⁺ recovery (ε≪1). The slow recovery dominates the cycle, so the rhythm is LOW
  and is set by ε — slower ions ⇒ lower Hz. Contrast: colour rides the quantum carrier
  (~6×10¹⁹ Hz), the neural rhythm is ~1–40 Hz, ~10¹⁸× lower, purely because ions
  recover slowly. (Low frequency is a slow-ion fact, NOT 'energy→information' — retired §9.)

Run each: `python3 <file>` (stdlib/numpy; each prints a deterministic sha256).

- `vp_phototransduction_4d.py` — **light → low neural frequency, the chemistry bridge.**
  The eye does not track light's ~10¹⁴–10¹⁹ Hz cycle; it ABSORBS it (the wave flips the
  rhodopsin R19 switch) and a cascade of progressively slower R19/leaky stages
  (rhodopsin*→transducin→PDE/cGMP→membrane) amplifies and slows it to the ionic
  relaxation oscillator. Shows: the frequency cascade (~5×10¹³× down-conversion); the
  output Hz is set by the IONS and is INDEPENDENT of the input frequency (blue vs red →
  same rhythm); ~50× amplification; colour preserved by the angle χ (which cone fires),
  not by frequency. The cascade is what the 4D photoreceptor (PAX6 γ) builds. Honest: the
  femtosecond light oscillation is not resolved — absorption is where the down-conversion
  happens, so it need not be.

- `vp_frequency_multiplexing.py` — **many channels on one substrate, the cerebrum hears
  all.** Because the jammed lattice is LINEAR (∂ₜ²u=c²∇²u), waves of different frequencies
  superpose and pass through each other untouched (verified to 10⁻¹⁶). The same linearity
  lets N neural rhythms (δ/θ/α/β/γ) summed on one line be recovered with ~0 error and
  ~10⁻¹⁶ cross-talk; two channels at the SAME frequency collide (so each needs its own
  frequency — the radio rule); the multi-band cortex decodes all at once. ~19 channels fit
  1–80 Hz at 4 Hz spacing. Honest: ionic-rhythm multiplexing (linear summation + band
  separation), NOT neural signals as EM/lattice waves (retired §9).

- `vp_electrocommunication.py` — **biological EM communication, verified (electric fish).**
  An electrical signal IS electromagnetic (chemistry: conduction χ→0 and radiation χ→90° are
  one phenomenon). An oscillating electric organ (a charge = synchronized rotation) sources a
  field that PROPAGATES to a receiver and arrives at the EOD frequency — the signal goes. At
  fish scale it is the NEAR-FIELD dipole (∝1/r³): electromagnetic, real, short-range, slow —
  the conduction/longitudinal aspect, NOT a light-speed radiative broadcast. Several fish at
  distinct EOD frequencies multiplex cleanly (cross-talk ~10⁻¹⁴); the jamming-avoidance response
  shifts frequencies apart. This refines §9: the RADIATIVE/light-speed carrier stays retired; the
  near-field/conduction electric communication is affirmed. (Human-brain ephaptic role stays open.)

- `vp_ion_em_information.py` — **why the neural code is a WAVE (EM/light), not scalar
  electricity.** The information proof: a scalar amplitude channel carries ~346 bits/s, but
  real-time vision needs ~10⁷ bits/s — unreachable with amplitude (SNR≈2^10⁵), forcing a
  wave code of ~29000 frequency×phase modes. Then the ion↔EM↔ion logic: an ionic FHN current
  is an oscillating field source at its frequency (ion→EM, same op as "emerge electricity from
  ions"); the cortical/cerebellar bands demux the multi-frequency field (the brain RECEIVES the
  wave); each read value drives the next ionic oscillator (RE-EMERGES it). ion = EM = light, one
  phenomenon distinguished only by the information it carries. Caveat (empirical, orthogonal): AP
  propagation velocity is ion-limited (0.5–120 m/s), not light-speed — capacity, not velocity,
  is the argument.

- `vp_sensory_frequencies.py` — **each sense emerges its own rhythm from ions, vs measured,
  then merges with the EEG.** The same ionic oscillator (R19 + slow recovery = FHN) with each
  modality's own recovery rate ε makes each sense's characteristic frequency. Against measured
  values — taste ~5 Hz (θ), touch ~30 Hz, hearing ~40 Hz, vision ~50 Hz, smell ~65 Hz (γ) — the
  emerged set matches within 0.91–1.19× under a single global model→Hz scale (the relative
  ordering/spacing is the check). Because electrical = EM, that rhythm IS the cell's characteristic
  EM wave. The distinct sensory rhythms then occupy distinct EEG bands and merge on the cortical
  substrate, demuxed back per sense — the last step before consciousness/memory (Mind).