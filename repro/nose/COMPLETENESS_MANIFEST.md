# COMPLETENESS MANIFEST (누락금지) — vp_nose_emergence_seed

Every artifact this seed promises. `tools/verify_seed.py` fails if any is missing.

- [x] `README.md`
- [x] `VERSION`
- [x] `seed.json`
- [x] `BLUEPRINT.md`
- [x] `FIREWALL.md`
- [x] `INHERITANCE_LEDGER.md`
- [x] `COMPLETENESS_MANIFEST.md`
- [x] `WORK_HANDOVER.md`
- [x] `VP_SPEC_v1_8.md`
- [x] `tools/verify_seed.py`
- [x] `tools/fetch_promoter_gamma.py`
- [x] `inherited/vp_substrate.py`
- [x] `inherited/gamma_pipeline.py`
- [x] `inherited/dna_interpreter.py`
- [x] `inherited/key_pipeline_full.py`
- [x] `inherited/vp_dna_reading.py`
- [x] `inherited/nose_promoters.cache.json`
- [x] `inherited/organ_gamma.json`
- [x] `inherited/FROZEN_SHA256.json`
- [x] `research/E1-combinatorial-code/START_HERE.md`
- [x] `research/E1-combinatorial-code/run.py`
- [x] `research/E1-combinatorial-code/gate_E1.py`
- [x] `research/E2-transduction-switch/START_HERE.md`
- [x] `research/E2-transduction-switch/run.py`
- [x] `research/E2-transduction-switch/gate_E2.py`
- [x] `research/E3-bulb-map/START_HERE.md`
- [x] `research/E3-bulb-map/run.py`
- [x] `research/E3-bulb-map/gate_E3.py`
- [x] `research/E4-congenital-anosmia/START_HERE.md`
- [x] `research/E4-congenital-anosmia/run.py`
- [x] `research/E4-congenital-anosmia/gate_E4.py`
- [x] `research/E5-allergic-smell-loss/START_HERE.md`
- [x] `research/E5-allergic-smell-loss/run.py`
- [x] `research/E5-allergic-smell-loss/gate_E5.py`

### Volume layer (added v0.7.0; deposited with its concept DOI at v0.7.1) — the published multi-chapter HTML (VP-SPEC v1.8 §6)
- [x] `tools/vp_nose_ssot.py` — numeric single-source-of-truth (recomputes every displayed number; deterministic)
- [x] `tools/build_volume.py` — builds `docs/` from the SSOT (numbers enter HTML only via `num()` → drift 0)
- [x] `tools/gate_volume.py` — focused volume gate (G1–G7)
- [x] `docs/nose/index.html` — volume hub (`CreativeWorkSeries`)
- [x] `docs/nose/_meta.json`
- [x] `docs/nose/00-inherited-foundation/index.html` — §0
- [x] `docs/nose/01-combinatorial-code/index.html` — §1
- [x] `docs/nose/02-transduction-switch/index.html` — §2
- [x] `docs/nose/03-bulb-map/index.html` — §3
- [x] `docs/nose/04-congenital-anosmia/index.html` — §4 (disease; direction-only)
- [x] `docs/nose/05-allergic-smell-loss/index.html` — §5 (disease; direction-only)
- [x] `docs/sitemap.xml`
- [x] `docs/robots.txt`
- [x] `docs/llms.txt`
- [x] `docs/assets/css/site.css`

**Total: 49 artifacts** (34 research backbone + 15 volume layer). Foundation modules (run twice for determinism by `verify_seed.py` [2]):
`inherited/vp_dna_reading.py`, **`research/E1-combinatorial-code/run.py`** (E1), **`research/E2-
transduction-switch/run.py`** (E2), **`research/E3-bulb-map/run.py`** (E3), **`research/E4-congenital-
anosmia/run.py`** (E4), **`research/E5-allergic-smell-loss/run.py`** (E5, the acquired disease layer;
allergy mechanism cited to immune §11, not re-derived). **No wave module** is listed — smell has none;
the inherited universal is the R19 switch + the DNA reading (see `BLUEPRINT.md`).

The volume layer is checked by `verify_seed.py` **[5]**, which invokes `tools/gate_volume.py`: the numeric
SSOT (`tools/vp_nose_ssot.py`) is run twice for an identical sha256, every number shown in `docs/` is asserted
to come from that SSOT (HTML↔code drift exactly 0), and both disease chapters are asserted to carry the
non-clinical direction-only scope banner. [5] reads only the seed's own tools — no `inherited/` file is touched.

At **v0.7.1** the volume is **deposited**: it carries its own Zenodo **concept DOI 10.5281/zenodo.20790182**
(always resolves to the latest version), and the gate's **G8** asserts that DOI is present on the hub (visible
cite line + `CreativeWorkSeries` JSON-LD identifier), in `docs/nose/_meta.json`, in `docs/llms.txt`, and in
every chapter's claim-strip. No artifact was added (still **49**); the DOI is wired into the existing files.
