# 17-spinal-cord-locomotor-cpg

**Verifies:** the spinal cord's ventral motor architecture and the locomotor **central
pattern generator (CPG)** are emerged from the **4D-DNA reading** — γ (the DNA volume's
nearest-neighbour metric, recomputed in-package from NCBI promoters) as the Layer-1 material
identity, a morphogen-threshold **spinodal** of cross-repressive R19 switches for the
dorsoventral order, and the neuron-class code for the CPG wiring. The measured
Briscoe-2000 domain order and the Kiehn/Goulding CPG module→function map are the
validation targets, never inputs (VP-SPEC C1). This is the missing CPG / spinal-structure
link of the neural chain.

**Method (identical to the DNA volume, validated bit-for-bit on LCT):**
`γ(seq) = mean(−ΔG37)` over nearest-neighbour dinucleotides (SantaLucia 1998);
`CpG O/E = (nCpG·L)/(nC·nG)` (Gardiner-Garden & Frommer) = the methylation substrate.

**Inputs (real, NCBI E-utilities, GRCh38):** 19 master-gene promoters in `inputs/`
([TSS−2000, TSS+500] = 2501 bp, coding strand). γ is **recomputed from these sequences**
in the engine, so the reproduction path is in-package (C1).

**Run:** `python3 run.py`
**Expected output:** `SLUG VERIFICATION: PASS` — engine gate (derived ventral→dorsal order
**[p3, pMN, p2, p1, p0] == measured**; one material class; CPG complete: rhythm + left-right
+ flexor-extensor + output), deterministic (2×sha256 identical), fidelity 148/148 to
`expected/`, and the exhaustive **5-grade ledger** (21 quantities: 10 [F] · 3 [V] · 3 [L] ·
3 [O] · 2 [B]; 16/21 positively evidenced; 0 ungraded) — see `IRREPRODUCIBILITY_LEDGER.md`.

**Engine:** `../_engine/vp_spinal_cpg.py` (stdlib+numpy, deterministic);
data `../_engine/data/spinal_master_genes.json` (NCBI features + measured targets, read-only).
