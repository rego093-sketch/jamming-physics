# START HERE — increment E1

The first emergence to build (see `BLUEPRINT.md` for the full plan).

**Task:** OPN1LW / OPN1MW / OPN1SW (cone opsins) on the angle map, using the **measured reading** already in `inherited/organ_gamma.json` — each gene's
**γ (LEVEL) and A4 coordinate (SHAPE)** — and the R19 `Organ` primitive in `inherited/vp_substrate.py`.
Order the lineage by spinodal(γ) and **break γ-ties with the A4 shape** (do not collapse genes of equal
γ). The seed modules to extend are `inherited/vp_color_by_angle.py` and `inherited/vp_dna_reading.py`.

**Deliverable:** a deterministic module `research/E1-*/run.py` that (a) reads the measured γ,
(b) emerges the lineage order via argsort(spinodal(γ)), (c) prints every displayed number and
self-hashes (2× run → identical sha256), and (d) declares grades [F]/[V]/[L]/[O] honestly. Then a
small gate, then fold into the verifier's foundation list. Keep the inherited foundation **frozen**.

**Firewall:** structure-only; no dose/efficacy; the felt percept is the mind volume's.
