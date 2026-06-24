# DNA Emergence — inherited here, runnable for verification

This directory carries the **full, runnable** VP DNA-Emergence work so that opening this package's whitepaper, a reader can actually *reproduce the DNA emergence*, not just read about it. Two self-contained sub-packages:

- **`animal/`** — VP Recent-Sequence DNA Emergence (mammoth/elephant, Neanderthal/human).
- **`plant/`** — VP Plant Environment DNA Emergence (cold vs UV; material as a lineage property).

Each is a complete package with its own `WHITEPAPER.md`, `GOVERNANCE.md`, `REPRODUCIBILITY_MAP.md`, `MANIFEST.sha256`, `modules/`, and a `repro/` spine that runs from **frozen NCBI records** with **no network and no tuning**.

## Run / verify

```bash
# animal: mammoth/elephant + Neanderthal/human
cd animal/repro && python3 vp_gamma_engine.py     # instrument self-test (deterministic gamma)
python3 run_all.py                                 # -> results/RESULTS.txt + figure

# plant: cold vs UV, material = lineage property
cd ../../plant/repro && python3 vp_gamma_engine.py
python3 run_all.py                                 # -> results/RESULTS.txt + figure
```

Both use the same inherited material engine (`vp_gamma_engine.py`, SantaLucia 1998 LOCK table, SEED = 19, no fitted parameter). To re-fetch the raw sequences live from NCBI and re-run, each has a `repro/fetch_ncbi.py`.

## What the DNA emergence establishes (present-tense, [V]) — and how it bears on the cascade

Three measured facts, reproduced in two kingdoms:

1. **Material (γ) is a lineage/kind property, not an environment property.** Animal: mammoth/elephant and Neanderthal/human each read as one material kind. Plant: the plastid core is conserved *across* grasses and nightshades (band centres 1.2821 vs 1.2809).
2. **The molecular clock is decoupled from the material.** r(substitutions, |Δγ|) ≈ −0.08 (animal) and +0.09 (plant). A clock count cannot be read as elapsed time or as material.
3. **The environment writes to STATE / inventory / dwell, not to the material.** Cold (CBF) and UV (CHS/UVR8) are different loci; CHS γ tracks lineage, not habitat.

**Bearing on the cascade (the firewall link).** The cascade asks whether a flood is *physically permitted* and holds its occurrence **[O]**. The DNA emergence shows that **DNA does not decide that occurrence in either direction**: because material is decoupled from time (fact 2) and conserved regardless of kind/time (fact 1), a small sequence difference is consistent with any elapsed time, so DNA is **neutral** on whether a quiet interval was long or short. It removes the standard "DNA proves deep time" objection *and* refuses to be promoted to positive flood evidence — symmetrically. The flood, like every occurrence claim, lives in the **history channel** (see `../GOVERNANCE.md` Art. 1–2 and the `TIME_SILENCE_RULING`-style reasoning recorded in the modules).

## Note (open strand)

The **fossil-count** side of the DNA/biology↔history bridge is younger and is carried separately in `../fossil_audit/`. It confirms ancient remains are genuinely sparse ([V]) but shows the counts cannot, by themselves, attribute that sparseness to any cause ([O]). This is the "DNA-fossil research needs more work" strand, kept open and honest.
