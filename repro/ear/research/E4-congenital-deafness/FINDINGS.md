# FINDINGS — increment E4 (congenital DEAFNESS: the R19 failure-mode decomposition)

**Status:** DELIVERED (v0.5.0) — **the volume's goal**. Deterministic module `run.py` (2×sha256
identical: `ebaa515b…`), small gate `gate.py` (7/7 PASS), folded into `tools/verify_seed.py`
foundation list. Three new measured genes folded into the cache+atlas with hashes **re-frozen
deliberately** (INHERITANCE_LEDGER.md); the inherited foundation is otherwise untouched. No constant
tuned.

## What E4 builds
The congenital-deafness mechanism layer — the destination of the whole volume — **emerged** as a
**decomposition of the inherited R19 cubic**. The keystone: the cubic `ṡ = g·s − s³ + h` has exactly
**three loci** a congenital sensory switch can fail at, plus the **critical regime** the E3 amplifier
occupies:

| locus | what fails | deafness class | genes (cited function) |
|---|---|---|---|
| **DRIVE h** | the endolymphatic power that pushes s past the spinodal | **drive** | GJB2, GJB6 (K⁺ recycling, DFNB1), SLC26A4 (pendrin, Pendred) |
| **STRUCTURE g** | the gating apparatus itself (stereocilia / tip-link) | **structure** | LHFPL5, MYO15A, USH2A, MYO7A (+ TMC1, the pore) |
| **DOWNSTREAM** | the layer *after* the flip (synaptic release) | **readout** | OTOF (auditory neuropathy/DFNB9) |
| **CRITICAL g→0** | operation at the critical point (the F^(−2/3) gain) | **amplifier** | SLC26A5 (prestin — the E3 amplifier) |

Each gene maps to **one** locus by its **cited protein function**, and the R19 geometry then forces a
**different substrate-inverse lever DIRECTION** per class — **direction-only, proposal-only**. This is
the firewall made constructive: it states which failures are switch-recoverable in principle and which
are not, and it refuses to name a molecule, a dose, or an efficacy for any of them.

## Results (every number reproduced offline, bit-for-bit)
- **Every deafness gene reproduces.** All 10 genes' γ + A4 recompute from the frozen promoter cache and
  equal the atlas bit-for-bit; A4 = signal − γ (|mean(shape)| < 1e-9). The **three newly-fetched** genes
  — **SLC26A4** (γ=1.3612, NC_000007.14), **LHFPL5** (γ=1.4043, NC_000006.12), **MYO15A** (γ=1.4960,
  NC_000017.11) — recompute identically; their cache+atlas hashes were re-frozen deliberately. **[V]**
- **DRIVE class is RECOVERABLE — forced by the cubic.** A structurally-intact switch (g=γ_TMC1=1.3028,
  spinodal=0.5724) sits OFF at drive h=0 (the K⁺-recycling failure: s=−1.1414) and flips **ON** once h
  is restored past the spinodal (s=+1.3864 at h=1.5·sp). The apparatus is whole; the power is off; the
  switch **recovers** when drive is restored. Substrate-inverse lever (DIRECTION ONLY, proposal-only):
  restore h toward +spinodal(g). **[F]/[V]**
- **STRUCTURE class is NOT drive-rescuable — an honest negative forced by the discriminant.** The
  switch's defining property is a finite bistable window in drive, width **2·spinodal(g) = 4(g/3)^1.5**,
  set by the **structure g**, not by h. It is **monotone in g** and **→ 0 as g → 0** (2·spinodal(0.01)
  = 0.00077; the integrator hysteresis loop collapses from 1.1763 at g=1.30 to the grid floor at
  g=0.01). Drive moves you *along* the h-axis; it cannot restore the window the lost structure created.
  So **no finite drive flips a structure-class failure** — the lever must act on g (a structural/genetic
  layer this substrate cannot supply). **[F]/[V]**
- **READOUT class is invisible to the cubic.** In an OTOF (auditory-neuropathy) ear the hair-cell MET
  switch flips **normally** (OFF s=−1.1414 → ON s=+1.3864, identical to a hearing ear): the substrate
  sees nothing wrong, because the broken layer is the Ca²⁺-triggered ribbon-synapse release, **downstream**
  of the flip. The cubic is the wrong layer; no (g,h) change addresses it. The synaptic layer is **[O]**.
- **AMPLIFIER class (the E3 bridge).** At criticality g=0 the inherited integrator gives gain r/F with
  fitted exponent **−0.666667** (|Δ|=1.2e-15): outer-hair-cell / prestin failure pulls the operating
  point off criticality, collapsing the **F^(−2/3)** compression ⇒ elevated thresholds + lost dynamic
  range. Lever: restore operation toward g→0⁺ (direction only); magnitude **[O]** (E3 N1). **[F]/[V]**
- **The substrate-inverse lever is direction-only and proposal-only.** Four classes, four lever
  directions; **two are honest negatives** (structure forbids drive-rescue; readout is the wrong layer).
  Every cell is a direction — no dose, molecule, in-vivo selectivity, or efficacy. **[F]**
- **Emergence placement — the deafness genes ARE the lineage genes.** argsort(spinodal(γ)) over the E4
  genes places **USH2A earliest-flipping (spinodal 0.5575) … GJB2 latest (0.7338)**, with the four
  failure classes **interleaved** (USH2A·TMC1·SLC26A4·SLC26A5·LHFPL5·OTOF·GJB6·MYO15A·MYO7A·GJB2). The
  deafness genes are not a separate catalogue; they are the emergence-lineage genes, read by **where**
  on the cubic each fails. Order **[F]**; γ measured **[L]**; class cited **[L]**.
- **The firewall, quantified — γ does NOT separate the classes.** drive-class γ ∈ [1.3612, 1.5375]
  overlaps structure-class γ ∈ [1.2801, 1.5086] by **0.1474**, and **no single γ-threshold separates
  them** (separable=False). γ reads promoter STRUCTURE (stiffness), **not protein FUNCTION**; the class
  labels come from cited biology and the R19 geometry supplies the lever. γ never becomes a function, a
  drive, a dose, or an effect. **[V]**

## Honest negatives / open items (preserved, not hidden)
- **N1.** EVERY physical magnitude is **[O]** — the drive in volts/Hz, the structural g in real units,
  the amplifier gain/dB/Q, any threshold value. Only **directions** and **exponents** are forced.
- **N2.** The failure CLASS is **cited protein function, not derived from γ** ([H] proves γ cannot
  assign it). A gene with mixed roles (e.g. MYO7A: tip-link tension *and* transport) is placed by its
  dominant transduction role; finer multi-locus failure is **[O]**.
- **N3.** The substrate-inverse lever is **proposal-only and direction-only**. No molecule is designed,
  no dose or efficacy is stated, nothing is diagnosed or treated (firewall).
- **N4.** The READOUT layer (OTOF / synapse) is **not modelled** by this transduction cubic — its
  rescue direction is **[O]** (a different substrate: Ca²⁺-vesicle release).
- **N5.** The amplifier-gain [V] inherits E3's small-drive under-convergence (E3 N5): the rigorous
  result is the analytic fixed point; the integrator fit holds on the converged range.
- **N6.** The full fluid-loaded dispersive traveling-wave **ENVELOPE** is **still the named [O]** — a
  closed envelope needs Q + fluid mass-loading + the E3 amplifier, and would require **tuning Q**
  (forbidden). E4 does not touch it; it remains open with its obstacle named.

## Why this is the goal, honestly stated
E4 is the disease layer the volume was built toward — and it delivers the **most useful honest output a
first-principles framework can give the congenitally affected**: a structural classification of *why*
each deafness happens (the switch's power is off ∥ the switch itself is missing ∥ the switch works but
the wire is cut ∥ the amplifier left criticality), and **which of those are switch-recoverable in
principle** (drive-class: connexins/pendrin) versus **which are not** (structure-class: the apparatus
must be rebuilt). It states **directions, never doses**. Nothing here is a diagnosis, a treatment, or a
promise; it is a map of where the inherited substrate says the lever must act — and where the geometry
itself says the easy hope fails.

## Naming note (flagged, not silently fixed)
This delivers **BLUEPRINT-E4** in the unambiguous folder `research/E4-congenital-deafness/`. The v0.3.0
folder-numbering slip stands flagged (BLUEPRINT-E2, the MET switch, shipped in the folder labelled `E1`;
**BLUEPRINT-E1**, the traveling-wave ENVELOPE, remains the named **[O]**). A future session may reconcile
`BLUEPRINT.md`'s E-numbering with the folder names; E4 introduces no new inconsistency.

## Firewall
γ read promoter STRUCTURE only (never a channel function, a drive, a motor force, a voltage, a dose, an
in-vivo selectivity, or an effect). The disease layer is **proposal-only** — direction-only R19 failure
modes and substrate-inverse lever directions. The percept of hearing is the mind volume's.
