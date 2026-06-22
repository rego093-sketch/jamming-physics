# START HERE — increment E3

The third emergence of the nose seed (see `BLUEPRINT.md` for the full plan). **BUILT (v0.6.0).**

**Task:** the **bulb map** — smell's substitute for the sibling senses' spatial image. The axons of
every olfactory sensory neuron expressing the same OR converge onto specific **glomeruli** in the
olfactory bulb, turning the receptor-space combinatorial code (E1) into a spatial **odour map**
(Mombaerts; Mori). Use the **measured reading** already in `inherited/organ_gamma.json` (the
OSN-identity organisers LHX2/EBF1/EMX2 and the OR bank) and the R19 **Organ** + switch in
`inherited/vp_substrate.py`.

**Deliverable (done):** a deterministic module `research/E3-bulb-map/run.py` that
(A) emerges the OSN-identity organisers as inherited **R19 Organs** in **spinodal(γ)** order and shows
the "parts present ≠ trait" presence threshold (absent below h*, present above); (B) proves the
one-OR→one-glomerulus convergence is a **bijection** that **preserves the combinatorial capacity** —
the full 2^N subset lattice maps to 2^N distinct spatial patterns, and E1's nested thermometer maps
to a nested thermometer **in space** (≤ N+1) because a bijection preserves subset chains; (C) states
the **honest [O]** — the **targeting coordinate** (which glomerulus an OR maps to) is **axon-guidance
chemistry** (OR → cAMP → guidance-receptor gradient), **not in γ** — the same kind of molecular gap as
E1's odorant key. It prints every number and self-hashes (2× run → identical sha256) and declares
grades [F]/[V]/[L]/[O] honestly. Plus `gate_E3.py` (`E3 GATE: PASS`), folded into the verifier's
foundation list. The inherited foundation stays **frozen**.

**Firewall:** structure-only; γ is promoter structure (threshold/expression/order), **never** a
guidance-receptor gradient, an axon target, a glomerular coordinate, or a percept; the targeting
coordinate is a named [O]; the abstract relabelling in Part B only proves the bijection theorem (it is
not a measured map); the felt percept of a smelled odour is the mind volume's.

**Next:** `BLUEPRINT.md` → **E4 — congenital ANOSMIA** (the goal): CNGA2/CNGB1 (transduction-switch
failure) + ANOS1/FGFR1/PROKR2/PROK2 (organ-formation failure) as R19 failure modes, **direction-only /
proposal-only** under `FIREWALL.md`; note CNGB1 LOF impairs **both** smell and rod vision.
