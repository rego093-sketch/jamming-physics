# Reproduce — one command verifies the whole neuro chain

Everything quantitative in this upgrade is regenerated from standard-library + numpy
modules with fixed seeds, and checked three ways (VP-SPEC Constitution C1, drift 0).

## Run it

```bash
cd repro/neuro
python3 run_all.py
```

Expected last line: `RESULT: PASS — 18 modules deterministic, hashes frozen, HTML↔code drift 0`.

## What it checks

1. **Determinism (A).** Every one of the 18 modules is run **twice**; the two stdout
   sha256 must be identical (same input → same output). (Chapters §16 and §17 ship their
   own per-slug `run.py` harness and are verified separately by `verify_all.py`, alongside
   their dedicated C1 gates — see the repo root.)
2. **Frozen hashes (B).** Each module's sha256 is compared to `expected_sha256.json`.
   The file is written on the first run and verified on every run after — any change to a
   module's output trips a failure. (Hashes are keyed to this environment's float
   formatting; the determinism and HTML checks below are environment-robust.)
3. **HTML ↔ code (C).** Every decimal number **displayed in the canonical HTML**
   (`docs/neuro/00, 10–15, 18, 19, 20`) is confirmed to be reproduced by some module's
   output — exactly, or as the HTML's rounding of a longer computed value. This is what
   guarantees the pages cannot drift from the code.

A machine-readable summary is written to `reports/reproduction_manifest.json`.

## The 18 modules

Inherited chain (`repro/neuro/_inherited/`): `vp_light_emergence_quantum`,
`vp_color_by_angle`, `vp_ion_low_frequency`, `vp_phototransduction_4d`,
`vp_frequency_multiplexing`, `vp_electrocommunication`, `vp_ion_em_information`,
`vp_sensory_frequencies`. Chapter modules: `_engine/verify_neuro_emergence`,
`10/run_transduction`, `11/run_loop`, `12/sensory_emergence_4d`, `13/vp_em_emission`,
`14/motor_quantification`, `15/vp_em_link_full`, `18/vp_em_brain_circulation`,
`19/vp_em_ephaptic_threshold`, `20/complete_sensory_atlas`.

Chapters **§16** (`16/run.py`, muscle force–length) and **§17** (`17/run.py`, spinal
locomotor CPG) carry their own per-slug harness + C1 gate and are run by `verify_all.py`,
not by `run_all.py`. The §20 capstone closes the sensory side: the four remaining
modalities (touch · pain · proprioception · vestibular) emerge from real measured γ
(14 master genes, fetched from NCBI and cached for offline reproduction), completing all
nine human sensory modalities.

## Worked examples of the cross-check

- **D = 4.852620 pm** (§0, §13) ← `vp_light_emergence_quantum.py` (D = 2h/mₑc).
- **χ(633) = 89.9378°, χ(532) = 89.8248°** (§0) ← same module (sinχ = λ/mD).
- **Δχ = 0.156°** for +0.03% in λ/D at 633 nm (§13) ← `vp_color_by_angle.py` (0.1557°, rounded).
- **corr(γ,GC) = 0.993** (§12) ← `sensory_emergence_4d.py` (0.9926 over 26 catalog genes).
- **force–frequency 3.9×, reflex ×10.4** (§14) ← `motor_quantification.py`.
- **corr(γ,GC) = 0.997, reflex rejection ×10.4** (§20) ← `complete_sensory_atlas.py`
  (14 new sensory master genes; the proprioceptive loop closes the §11 reflex onto a real spindle).

Full derivations and evidence are at the DOIs in §0 (physics 10.5281/zenodo.17932566,
chemistry 10.5281/zenodo.20680540, dna 10.5281/zenodo.20471407, neuro 10.5281/zenodo.17979015).
