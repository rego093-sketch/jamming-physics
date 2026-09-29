# Noah-flood whitepaper reproduction bundles (v1.2–v1.3): recovered legacy

**Provenance.** The author supplied these on 2026-09-29 as `noah_flood_whitepaper_zenodo_bundle_compat.zip` and `vp_repro_bundle_v1_3_FINAL.zip`, and described them as old data. They come before the geodynamics volume's Atlantic-opening engine. They are kept here as the source data for the volume's HOLD predictions, which are data-pending. The whitepaper PDF and TeX files, and the nested zips, are left out.

**Contents**
- `vp_repro_bundle_v1_3/`: a data snapshot with full and mini sets. It covers:
  - RSL at 8 Mediterranean and Pacific sites;
  - IntCal20, Marine20 and Mediterranean ΔR;
  - Nile-delta cores and seismic data;
  - leaf-wax δD, tree rings, coal geochemistry;
  - mammoth and human aDNA tables;
  - dinosaur bone histology.

  It also holds the schema, codebook and provenance files, plus the QA, checksum and hardgate scripts.
- `noah_flood_bundle/`: the unpacked reproducibility sub-packs, with the `rsl_mod`, `delta_mod`, `bio_mod` and `run_all` stubs and the datasets v1.2.

**Checked 2026-09-29.** `python3 scripts/reproduce_all.py` ends with **hardgate: PASS** (QC flags OK on 16 files). `verify_checksums.py` gives 83 OK, 2 MISSING and 2 FAIL. The 2 MISSING are the whitepaper `.tex` files, which were deliberately left out. The 2 FAIL are `qa/qa_report.json` and `qa/qa_report.md`. They fail the same way in the pristine bundle as shipped, so the QA report was regenerated after the checksum list was written. Every data file matches its checksum.

**What this bundle is not.** It is not the Atlantic-opening engine. That engine is `../src/geodynamics/atl_bundle/`, where `validate_all.py` gives 39/39 PASS. The data here may feed the P16, P19 and P29 HOLD tests (sea-level and freshwater records) once their pre-registered pipelines are run.
