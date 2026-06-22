# START HERE — increment E4 (congenital DEAFNESS: the R19 failure-mode decomposition)

The fourth emergence and the volume's **goal** (BLUEPRINT.md slot E4; delivered in v0.5.0). See
`FINDINGS.md` for the result.

**Task (delivered):** read the congenital-deafness genes — **GJB2, GJB6** (DFNB1), **SLC26A4**
(Pendred/DFNB4), **LHFPL5** (DFNB67), **MYO15A** (DFNB3), **USH2A, MYO7A** (Usher), **OTOF** (auditory
neuropathy), with **SLC26A5** (prestin, the E3 amplifier) as a fourth class — not one-by-one but as a
**decomposition of the inherited R19 cubic** `ṡ = g·s − s³ + h`. The cubic has exactly **three loci** a
congenital sensory switch can fail at — its **STRUCTURE g**, its **DRIVE h**, or the layer **DOWNSTREAM**
of the flip — plus the **CRITICAL regime g→0** (the E3 amplifier). Each gene maps to one locus by its
**cited protein function**, and the geometry then forces a **different substrate-inverse lever DIRECTION**
per class — **direction-only, proposal-only**.

**Deliverable (met):** a deterministic module `research/E4-congenital-deafness/run.py` that
(0) reproduces every deafness gene's γ+A4 from the frozen cache (incl. the three newly-fetched genes),
(A) states the cubic's three failure loci + the critical regime and assigns each gene by cited biology,
(B) shows the **DRIVE class is recoverable** (an intact-g switch flips once h is restored past the
spinodal — [F]/[V]), (C) shows the **STRUCTURE class is NOT drive-rescuable** (the bistable window
`2·spinodal(g)` → 0 as g→0, forced by the cubic discriminant — an **honest negative**), (D) shows the
**READOUT class is invisible** to the cubic (the switch flips fine; OTOF is downstream — [O] synapse),
(E) bridges to E3 (the **AMPLIFIER class**: criticality lost ⇒ the `F^(−2/3)` gain lost), (F) tabulates
the **substrate-inverse lever** (direction-only, proposal-only — two of four classes are honest
negatives), (G) **emerges** the placement (argsort(spinodal(γ)) — the deafness genes interleave the
lineage), (H) proves the **firewall negative** that γ/A4 do **not** separate the classes (γ is
structure-only), self-hashes (2× → identical sha256), and grades [F]/[V]/[L]/[O] honestly. Plus a gate
(`gate.py`, 7 checks), folded into the verifier's foundation list. The inherited foundation stayed
**frozen** (the cache+atlas hashes were re-frozen **deliberately** for the three new genes — see
`INHERITANCE_LEDGER.md`).

**New measured γ (folded in, hashes re-frozen):** SLC26A4 (γ=1.3612, NC_000007.14), LHFPL5 (γ=1.4043,
NC_000006.12), MYO15A (γ=1.4960, NC_000017.11) — fetched by `tools/fetch_promoter_gamma.py`, recompute
offline bit-for-bit.

**Firewall (binding):** γ reads promoter STRUCTURE only — never a channel function, a drive magnitude,
a motor force, a dose, an in-vivo selectivity, or a clinical effect. The disease layer is
**proposal-only**: direction-only R19 failure modes and substrate-inverse lever **directions**. Nothing
diagnoses, treats, or prescribes; no molecule is designed; no dose or efficacy is stated. The felt
percept of hearing is the **mind** volume's.

**Next (open):** the named **[O]** — the full fluid-loaded dispersive traveling-wave **ENVELOPE** (needs
Q + fluid mass-loading + the E3 amplifier; a closed envelope would require **tuning Q**, forbidden).
Also open: fold **TMC2** (the second MET pore, still in the atlas `_to_measure`) for a fuller MET set;
extend the readout-class to a Ca²⁺-vesicle-release substrate (OTOF, currently [O]); and grow the seed
into the full HTML volume (VP-SPEC v1.8 §6) — delivered, as always, as **one zip**.
