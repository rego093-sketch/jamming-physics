# Whitepaper v1 — Reproducibility Pack

This archive contains data, configs, scripts, and docs to reproduce the **RSL / Delta / BIO** checks described in the whitepaper.
ASCII-only labels are used inside figures to avoid font issues; Korean explanations are provided in captions outside images.

## Structure
- `data/PF_DataPack_v1.0/` — human/mammoth/plant panels and QC
- `data/RSL_Delta_BIO_Finalize/` — RSL series, delta CI & cores, posterior share summary
- `config/` — prereg thresholds (Ω‑NoGo), label standards (SLC24A5 rs1426654)
- `scripts/` — minimal, dependency-free stubs for quick verification
- `docs/` — List of Tables/ Figures DOCX and figure PNGs (ASCII labels)

## Quick test
```bash
make all
```

## Notes
- Figures generated with matplotlib, one plot per figure, default styles (no custom colors).
- Label standard: SLC24A5 rs1426654 — derived=A (Light), ancestral=G (Dark).
- Pack build time (UTC): 2025-10-19T14:17:13.702257Z
