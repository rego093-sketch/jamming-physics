# INHERITANCE LEDGER (기초 상속자료) — vp_nose_emergence_seed

Every inherited artifact, its frozen sha256, and where it comes from. The verifier asserts each is
**byte-identical** to the hash below (no-regression). Nothing here was re-derived in this seed. The
five universal modules are byte-identical to the sibling **eye** seed (same hashes) — the shared VP
substrate and DNA-reading machinery reused without a single edit.

**The v0.7.x volume layer changes nothing here.** The published HTML volume (`docs/`) and its three tools
(`vp_nose_ssot.py`, `build_volume.py`, `gate_volume.py`) were added *on top of* this ledger (v0.7.0), and at
v0.7.1 the volume was **deposited** with its own Zenodo concept DOI (`10.5281/zenodo.20790182`) — a
presentation/metadata change only. The SSOT recomputes display numbers with the same inherited primitives
(imported read-only from `inherited/`), so every frozen hash above is still byte-identical at v0.7.1
(`verify_seed.py` [1] re-checks them, [5] checks the volume). No inherited DATA or CODE file was edited to
publish or deposit the volume.

| inherited artifact | sha256 (frozen) | provenance |
|---|---|---|
| `inherited/vp_substrate.py` | `a4bbbb18d564460a…` | R19 switch primitive (ds/dt=γ·s−s³+h; spinodal=(2/3√3)γ^1.5), byte-identical to eye seed |
| `inherited/dna_interpreter.py` | `4929932d90321790…` | canonical A4-grammar (DNA v1.13: γ, switch, helix geometry), byte-identical |
| `inherited/key_pipeline_full.py` | `3141fa22cfe34a94…` | canonical A4 region pipeline (shells/anchors/robust_z), byte-identical |
| `inherited/gamma_pipeline.py` | `4bde475df52a7a12…` | offline γ recompute (SantaLucia-1998 NN ΔG37) |
| `inherited/vp_dna_reading.py` | `f5ea1709bf091467…` | the seed reading: γ (LEVEL) + A4 (SHAPE) per promoter |
| `inherited/nose_promoters.cache.json` | `ee2b41be6dc87e7c…` | **20** measured human olfactory promoter sequences (NCBI, cached); re-frozen v0.6.0 (+PROKR2/PROK2), v0.6.1 (+OR2W1) |
| `inherited/organ_gamma.json` | `2451be7b1b6d019e…` | measured readable-layer atlas: γ (level) + A4 (shape), olfactory genes; re-frozen v0.6.0 (+PROKR2/PROK2), v0.6.1 (+OR2W1) |
| `inherited/FROZEN_SHA256.json` | (this file's manifest) | the no-regression hash set the verifier checks |

**Note — no wave module is inherited.** The eye seed inherited a light-emergence / angle-law / colour-
by-angle stack; **this seed inherits none of it**, because smell has no wave. The only universal that
carries over is the **R19 switch** (vp_substrate.py) and the **DNA reading**. That absence is itself
the honest structural statement of olfaction (see `BLUEPRINT.md`).

**Source volumes (cited, one-way — this seed consumes; it never edits the source):**
- **physics** (DOI 10.5281/zenodo.17932566) — the jammed-lattice substrate and the R19 bistable
  switch primitive that `vp_substrate.py` vendors.
- **dna** (DOI 10.5281/zenodo.20471407, **v1.13** "A Deterministic Two-Layer Interpretation of DNA")
  — the readable layer = **γ (level) + A4 coordinate (shape) + R19 switch-state + CpG handles**; the
  SantaLucia-1998 NN ΔG37 γ measure, the A4 grammar (`dna_interpreter.py` / `key_pipeline_full.py`,
  vendored byte-identical), and emergence order = argsort(spinodal(γ)). γ and A4 are the level and
  shape of one stiffness field — orthogonal, neither contains the other.
- **neuro / sensory_organ** (DOI 10.5281/zenodo.17979015 / 20755154) — the R19 substrate primitive
  and the transduction-switch reading this seed extends to olfaction.
- **eye sibling** (`vp_eye_emergence_seed`) — the cross-sense reference for **CNGB1** (the CNG β
  subunit shared by rod vision and olfaction); its independently-measured rod-vision CNGB1 γ=1.4357
  is cited in E2 and matches this seed's olfactory measurement byte-for-byte.
- **immune / hematologic** (DOI 10.5281/zenodo.20755280, **§11** "Allergy: sensitization, the latch,
  and controlled desensitization") — the **allergy mechanism** E5 **consumes, never re-derives**:
  sensitization at the R19 spinodal, the dose×repetition threshold, the latch, and controlled
  desensitization (= allergen immunotherapy = basin-acting re-tolerization), graded [V] there. E5 owns
  only the olfactory **consequence** (conductive drive-suppression + sensorineural organ degradation);
  the **absolute airway aeroallergen/mucosal scale** is the **respiratory volume's [O]**, deferred to
  the surface owner. One-way: this seed cites it and computes none of the immune mechanism.

**Measured γ provenance:** every sequence in `inherited/nose_promoters.cache.json` was fetched from
NCBI nuccore (GRCh38 current RefSeq chromosomes) by exact accession + TSS−2000..+500 window + strand,
and is cached so γ recomputes offline bit-for-bit. The fetcher that built it ships at
`tools/fetch_promoter_gamma.py`; re-audit against live NCBI with `--cache`. **20 genes** (v0.6.1) span
four nodes: olfactory_transduction (6), olfactory_receptor (7), olfactory_neuron_identity (3),
congenital_anosmia (4). The two Kallmann genes **PROKR2** (NC_000020.11, γ=1.4781) and **PROK2**
(NC_000003.12, γ=1.4634) were `_to_measure` at v0.4.0 and were **fetched from NCBI and folded in at
v0.6.0** for the E4 anosmia layer. The last deferred olfactory receptor **OR2W1** (NC_000006.12,
γ=1.2412) was **fetched from NCBI and folded in at v0.6.1**, completing the representative OR panel
(N=7) and emptying `_to_measure` (γ measured, never invented; on each addition the two DATA files were
re-frozen and the five universal CODE modules left untouched).
