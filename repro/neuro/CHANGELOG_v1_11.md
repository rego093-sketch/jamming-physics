# CHANGELOG — neuro_emergence_chain_integrated

## v1.11.0 — Analgesic target-logic inheritance + neuro-native pain + explicit DNA-emergence (2026-06-19)

This session propagated the **digestive_vp_site v0.16 authoring session** into the neuro volume and
**inherited the analgesic technique** (`analgesic_threshold_logic` v2.0, concept DOI
**10.5281/zenodo.20733420**, CC BY 4.0). Per VP_FRAMEWORK_MAP, work stayed inside the neuro lane:
the primary somatosensory nociceptor is a neuro entity, so this volume is the **canonical home** of
the analgesic firing-threshold reading (the digestive volume's §28 visceral-pain section points
here). Gene-key monogenic pain channelopathies remain **disease_wp** entities (cross-referenced
only); the felt/affective pain remains the **mind** volume's. Governed by VP-SPEC v1.8 (C1–C4).

### Added — reproduction (`repro/neuro/`)
- **`21-analgesic-nociceptor-threshold/rederive_on_neuro_engine.py`** — re-derives the inherited
  27-target three-lever firing-threshold map on **this volume's own engine**. Asserts (a) **engine
  identity**: `repro/neuro/_engine/vp_neuro_engine.py` is **byte-identical** (sha256
  `c933ee8d…`) to the engine the frozen sibling map was built on, and (b) **drift 0**: every
  displayed |h_sp| and barrier reproduces the frozen sibling map exactly at the frozen precision,
  order identical. Vendors the sibling's inherited γ + frozen baselines under `_inherited_analgesic/`.
- **`22-neuropathic-pain-firing-threshold/neuropathic_pain_levers.py`** — the neuro-native disease
  reading: neuropathic/sensitised pain as a firing-threshold shift on the locked R19 element, with
  the afferent gain χ = 1/(3s*²−g) rising ×1.68 at b = 0.6·spinodal; the three levers each lower
  b_eff so the firing threshold rises and the gain falls **monotonically** back to the baseline
  1/(2g). Carries the channelopathy direction anchor (Na_V1.7 LOF/GOF bracket the axis) and a
  disease→lever pointer table.
- **`20b-dna-emergence-inheritance/verify_dna_emergence.py`** — makes the DNA-emergence inheritance
  **explicit and active**: emerges the nociceptor lineage from one inherited measured promoter γ via
  the shared R19 `Organ` primitive (form ← γ; emergence order = argsort spinodal; dwell ∝ γ^1.5),
  and asserts that γ is **bit-for-bit** the measured atlas γ the §21 map and §22 dynamics read.
- All three added to `repro/neuro/run_all.py` (now **21 modules**, determinism + frozen hashes).

### Added — canonical site (`docs/neuro/`), VP-SPEC v1.8 §6 template, each a **separate** page
- **§21 `21-analgesic-nociceptor-threshold-map/`** — the inherited 27-target three-lever map
  (drift-0 re-derivation), the nociceptor's home reading.
- **§22 `22-neuropathic-pain-improvement-levers/`** — neuropathic pain as a firing-threshold shift +
  the three improvement levers (drug-class pointer per disorder).
- **§23 `23-pain-channelopathy-and-dna-grounding/`** — the measured channelopathy direction anchor +
  the explicit DNA-emergence grounding (one measured γ → three readings) + the forward plan for the
  existing chapters.
- **`faq/`** (FAQPage JSON-LD) and **`methods/`** volume pages (digestive-session standard).

### Added — C4 retrieval-readiness (was missing in v1.10.1)
- **`docs/assets/css/site.css`** (4.3 KB) — the chapters referenced `/assets/css/site.css` but no
  stylesheet shipped; added (covers chapter + hub classes).
- **`docs/robots.txt`** — allows the 7 required bots (Googlebot, Bingbot, OAI-SearchBot, GPTBot,
  PerplexityBot, ClaudeBot, Google-Extended) + Sitemap.
- **`docs/sitemap.xml`** (+ `docs/neuro/sitemap.xml`) — hub + all 24 chapters + faq + methods.
- **`docs/llms.txt`** (3.0 KB, < 5 KB) — authoritative summary + section index + firewall.

### Changed
- **`docs/neuro/index.html`** (hub) — extended the contents TOC from §1–§9 to **all 24 chapters
  (§0–§23)**, fixing pre-existing orphans for §10–§20 and registering §21–§23 (hub orphans now **0**).
- **`docs/neuro/_meta.json`** — added the 3 chapters, bumped `version` 1.11.0, updated totals
  (24 chapters), appended the analgesic-inheritance headline result.
- **`inherited/organ_gamma.json`** (new) — explicit inherited DNA-grounded γ for the nociceptor
  lineage, with provenance to the DNA volume (DOI 10.5281/zenodo.20471407).
- **`VERSION`** (new) → `1.11.0`.

### Added — gate
- **`tools/gate_neuro_v1_11.py`** — 11 checks: drift-0 inheritance, engine identity, de-sensitisation
  monotonicity + baseline return, DNA-grounding match, the 3 chapters' §6 template + JSON-LD,
  hub orphans 0, C4 files (robots/sitemap/llms<5KB/css), _meta↔disk consistency, and a chapter
  **rebuild byte-identity** check (HTML↔code drift 0). Auto-collected by `verify_all.py`.

### Verification
- `python3 verify_all.py` → **OVERALL: PASS (6/6)** (run_all 21 modules + 2 slug gates + 3 chapter
  gates incl. v1.11). `python3 tools/gate_neuro_v1_11.py` → **PASS (11/11)**.

### Firewall (binding, inherited verbatim)
γ reads promoter switch-threshold **STRUCTURE only** — never a channel voltage, drug potency, dose,
in-vivo selectivity, or clinical effect (all **[O]**). The lever strength δ is structural, not a
dose. The felt/affective pain is the **mind** volume's. Monogenic pain channelopathies are gene-key
**disease_wp** entities. No molecule is designed; nothing diagnoses, treats, or prescribes — every
new section is a proposal-only target hypothesis. γ is measured, never fitted.

---

(Earlier history: see `CHANGELOG_v1_9.md` for v1.9 and the v1.10/v1.10.1 chapter additions
[§16 muscle force–length, §17 spinal-cord locomotor CPG, §18–§20 EM/sensory-atlas capstones].)
