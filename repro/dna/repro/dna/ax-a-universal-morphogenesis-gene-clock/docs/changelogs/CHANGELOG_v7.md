# CHANGELOG — universal_morphogenesis_geneclock v7

Built on neuro_emergence_chain_integrated v1.9 (VP-SPEC C3 no-tuning governance).
**Add-only, no engine edits, no fork of `organism/core.py`.** Unified entry `verify_all.py` now
**PASS 9/9** (seven gates 5/5 + sha256 source/measured-input pin drift 0 + seven fidelity baselines
leaf drift 0).

## v7 #2 — widen the developmental-timing table beyond n=7 (lift the power floor)

This is the binding next step the v6 HANDOFF named first. v5 established an honest null (measured
promoter-stiffness γ does not predict Carnegie first-appearance staging for 7 [V]-master features;
ρ = −0.018, perm p = 0.986); v6 widened it to proximal-promoter *composition* (γ, GC, CpG o/e,
TATA/GC-box/CAAT density), every predictor [O], with the exact-permutation **floor = 7.9e-4 at n=7**
flagged as the power ceiling and a moderate positive composition trend (ρ ≈ +0.4) left unresolved.
v7 does exactly the named step with the **same apparatus and zero tuning**: add three more genuine
[V]-master features (n → 10) and re-run BOTH the γ/spinodal test and the v6 composition battery.

### Three new locked features (each pinned from a primary source BEFORE any correlation)
- **FOXG1 → future cerebral hemispheres, CS14** (Müller & O'Rahilly 1988, PMID 3377191 — the gene
  in the title of the CS14 staging paper).
- **MITF → retinal pigment epithelium first melanisation, CS15** (O'Rahilly & Müller; melanogenesis
  literature, PMID 1927245).
- **SOX9 → first chondrification, CS17** (O'Rahilly & Müller Publ. 637: condensations CS16,
  chondrification CS17–18).

Full n=10 stage vector `[9,10,12,13,13,14,15,17,17,18]`. Two **documented scope corrections**
(not silent): FOXG1 and SOX9 are tagged [F] in the broad atlas (vague multi-feature programs) but are
the canonical [V] masters for these *specific* features (telencephalon; chondrogenesis). MITF was
already a [V] master in dev_timing's V_MASTERS.

### Locked γ never overwritten — the new masters reproduce it
γ/GC are read **verbatim** from locked `morpho_gamma.json`. The new promoter cache supplies raw
sequence only: **MITF and SOX9 sequences are byte-for-byte copies** of `morpho_promoters.cache.json`
and recompute the locked γ **exactly (Δ=0)**; **FOXG1 was re-fetched once** by the identical pipeline
(NC_000014.9 +, TSS−2000..+500) and reproduces the locked γ within assembly drift (Δγ=2e-4, ΔGC=4e-4,
≤ tol 5e-3 ≪ inter-gene spread ~0.14). Residuals recorded, not hidden.

### New exact-permutation engine (makes n=10 tractable, validated before use)
At n=10, 10!=3,628,800 permutations × 6 predictors is too slow to brute-force through scipy. Since
Spearman ρ is an **affine function** of `S = Σ rank_x·rank_y[perm]`, the permutation null of ρ
depends only on the stage-rank multiset (for tie-free predictors), so the exact null of `S` is
computed **once by dynamic programming** over the remaining stage-rank multiset and reused for every
predictor + the floor; predictor ties are handled in the same DP; ranks scaled ×2 → exact integer
keys; tied stages counted with multiplicity so the DP total is exactly n!. Runtime ~0.02 s. The
engine is **validated in the gate before the n=10 claim**: it reproduces the v5 brute-force oracle
(`DT._perm_p`) **bit-for-bit at n=7,8** and a vectorised oracle at **n=9**.

### Result (reported, not tuned) — every test [O], but now WITH power
Widening to n=10 **lifts the exact-permutation floor from 7.9e-4 to 2.2e-6**, so Bonferroni
significance (α=8.3e-3) is amply reachable.

| | ρ | exact perm p | grade |
|---|---|---|---|
| γ/spinodal | −0.280 | 0.429 | [O] |
| gamma | −0.280 | 0.429 | [O] |
| gc | −0.311 | 0.379 | [O] |
| cpg_oe | +0.402 | 0.248 | [O] |
| tata | +0.490 | 0.183 | [O] |
| gcbox | −0.434 | 0.215 | [O] |
| caat | +0.455 | 0.187 | [O] |

The moderate positive composition trend (tata +0.49, caat +0.46, cpg_oe +0.40) **survived the
widening and still did not reach significance** (best raw perm p = 0.183). Because the floor (2.2e-6)
shows the test now has ample power, this is a **real null at n=10**, not a power artifact: proximal-
promoter composition does not predict Carnegie staging order even with the floor lifted. The
γ/spinodal test reconfirms the v5/v6 sign and null on the wider table.

### Falsifiability (kept live)
n=10 non-blind self-test (synthetic comonotone predictor → ρ=1.0, perm p<0.05; shuffle collapses);
DP==oracle at n=7,8,9; original 7 features bit-identical to dev_timing.json with stage sha frozen;
new stages integer, γ-independent, not back-fitted (|ρ|=0.280<0.99).

### New gate, new files
New gate: **`verify_dev_timing_wide`** (PASS 5/5) → gate suite is now **seven gates**.
New files:
- `code/dev_timing_wide.py` (n=10 dual test + DP exact-permutation engine)
- `code/verify_dev_timing_wide.py` (the gate)
- `code/data/dev_timing_ext.json` (3 new locked Carnegie stages)
- `code/data/dev_timing_ext_promoters.cache.json` (MITF/SOX9 byte-for-byte + frozen FOXG1 re-fetch)
- `LEDGER_dev_timing_wide.md`, `CHANGELOG_v7.md`
- `repro/morpho/expected/dev_timing_wide_verify.json` (new fidelity baseline)

`expected_sha256.json` now pins **49** governed source + measured-input files (was 45: +2 code, +2
data). All six prior gates remain 5/5, untouched.

---
