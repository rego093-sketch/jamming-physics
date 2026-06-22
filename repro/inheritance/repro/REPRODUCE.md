# REPRODUCE — VP Inheritance Kit

Self-contained. No upstream whitepaper, no network needed to reproduce (the promoter sequences are cached).

## Requirements
- Python 3.9+ and `numpy`. Nothing else.

## One command (the research gate)
```
python repro/run_all.py
```
This runs, deterministically and offline:
1. **NCBI offline verify** — recompute the RNA-machinery γ from `inherited/rna_carrier_promoters.cache.json`
   and confirm the **SOX9 anchor reproduces** (the no-tuning fidelity gate) and the atlas matches.
2. **The five batteries** — R (rna_layer), TG (env_to_germline), I (transgenerational_immunity),
   V (rna_vaccine), GT (gene_therapy).
3. **Determinism gate (VP-SPEC C1)** — each battery emitted twice, byte-identical (2×sha256).

It writes `reports/research_complete.json` with **all_green** and `reports/emergence_results.json` with the
full battery detail. Expected: `all_green = true` (anchor reproduces, 5/5 batteries PASS, determinism holds).

## Run a single battery
```
python engine/rna_layer.py
python engine/env_to_germline.py
python engine/transgenerational_immunity.py
python engine/rna_vaccine.py
python engine/gene_therapy.py
```

## Re-measure γ from NCBI (optional; not needed to reproduce)
```
python data/fetch_rna_gamma.py --fetch      # online: resolve coords + fetch promoters + rebuild cache/atlas
python data/fetch_rna_gamma.py              # offline: verify only (default)
```
The online fetch **refuses to write** unless the SOX9 anchor reproduces (γ=1.4598, GC=0.545). The cached
atlas already reproduces bit-for-bit, so the fetch is provenance, not a dependency.

## Determinism / no-tuning notes
- Every stochastic battery uses the inherited substrate seed (`SEED=19`); a fixed seed makes the Langevin
  survival/escape statistics byte-reproducible.
- No γ is fitted. The pipeline is accepted only because it reproduces the SOX9 anchor; the measured panel is
  declared by function before any γ is seen.
- Every number traces to a measured promoter γ + the vendored R19 switch (DNA emergence). Absolute
  magnitudes are firewalled out as [O] (see `IRREPRODUCIBILITY_LEDGER.md`).
