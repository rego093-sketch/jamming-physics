# HANDOVER — v1.19 → v1.20  (Felt Cognition / mind package)

Governed by `VP_SPEC_v1_8.md` (C0–C4, SEED=19). DOI of record (concept):
**10.5281/zenodo.20694404** (Zenodo deposit unchanged; this is a living-version snapshot).

---

## 1. WHAT v1.19 DELIVERED (all complete, all gates green)

v1.19 took the two results that v1.18 had carried as **add-only decision-checks/studies**
(measured M9 geometry; main carrier) and **promoted them into the engine** — the single
allowed exception to add-only, **VP-SPEC §6-6 intentional hash change**, with **0 new tuned
constants**. Plus two add-only decision-checks (node decomposition; theta-pacing anchor).

| Task | What | Result |
|---|---|---|
| **1A** | M9 ephaptic geometry `ring [O]` → `measured MNI [L]` as the **engine default** (`POS=_measured_geometry`) | M9 fc **0.0734→0.13468**, R 0.329→**0.390**, regime still **partial_metastable** (R<0.9). Cascade: M0–M8·M10–M15 **byte-identical**, only M9 changed, M16 new. |
| **2A** | Main high-frequency carrier promoted **verbatim** into engine as **M16** (`emerge_main_carrier`, wired last in `emerge_all`) | engine M16 headline reproduces study `8d05cfec…` bit-for-bit; +19 `mc_*` regression invariants; new **chapter 17**. |
| **1B** | M9 node decomposition (sulcal-bank folding critique), add-only decision-check | 3 pre-registered resolutions (12 / 85 / 117), **all partial_metastable**; AAL = gyral-centroid → **PARTIAL grounding**, literal mm bank walls need sub-gyral parcellation = **OWED [O]**. |
| **2B** | Theta (slow-index) pacing anchor — obstacle declared, add-only | canonical pacing anchor (medial-septum GABA pacemaker / Ih HCN) **not** in package, neuro pkg absent → slow leg stays **[O]**; GABA_B 180 ms is synaptic-decay, **candidate only**. Anti-tuning: 6.125 ≠ GABA_B 16.333. |

**Pre-existing gate fixes (orthogonal, 0 computational change):** (i) chapter-16 phenomenology
**re-frozen** to the deterministic engine M12 `bab1be8f…` (engine had been upgraded to 15-matched
/0.75 in a prior version; chapter freeze was stale at 11-matched/0.55; registry+engine were already
aligned). (ii) search layer **rebuilt** (`gate.py` idempotency compares disk docs vs a fresh build;
two builds are byte-identical — only the on-disk sitemap date was stale).

---

## 2. FROZEN HASHES (verify against these)

| Artifact | sha256 |
|---|---|
| **v1.17 PRE-promotion engine tree** (HISTORICAL anchor, preserve forever) | `b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7` |
| **v1.19 NEW promoted engine tree** (2× deterministic; §6-6 exception) | `3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1` |
| regression_scalars.json | `ebdc81e090fc7bdbaaff743c2b3b959652fc4eb061f68c0f1613ead50052543d` |
| geometry decision-check (`geometry_grounding.py`) | `8ad43a72b2f8282cae801ed8468c883b79eab0c79363ebd98621cbbfc18ff80f` |
| geometry atlas (`brain_geometry_atlas.json`) | `99daa8f5cc66edb79bf84921a2222e3db74dc53c9146253b32a9b13e43c9b8e4` |
| AAL builder (`build_geometry_atlas.py`) | `94700d2f33c770239f06184d55f31a93aa653494402a78911bb52c012c1f98cb` |
| 1B node decomposition (`node_decomposition_results.json`) | `0c22317f9956a9a41a14dad1574533d45eaeb93bd336daad4e0492bbde9ab783` |
| 2B theta-anchor (`theta_pacing_anchor_status` results) | `31722498380e5a5a1efff2523e236878bf1b03c32de0b29936f7d0e28f8711b5` |
| carrier study / engine M16 headline | `8d05cfeccb9cf57c924b1b2aea3f716caaf6069f690171bf8d2fae47004b2de7` |
| chapter-16 phenomenology M12 (re-frozen) | `bab1be8ff7df3a76cb838233a37d74af09df00130e70373fb4587e36812d64d4` |

**Honesty ledger (unchanged):** `medium_efficacy_tested=0`, `hard_problem_open=1`,
`consciousness_claim=0`, `new_tuned_constants=0`. M16 / measured geometry are **measurements,
NOT consciousness claims**; PCI access marker = **honest negative**.

---

## 3. GATE STATUS — 13 / 13 PASS (exit 0)

`tools/gate.py` (71/71) · `verify_boundary` · `verify_terminology` · `registry validate` (23
locks, 15 chapters) · `02-not-a-field/verify_em_thesis` · `13/verify_expand` (14) · `13/verify_loro`
(15) · `14/verify_sensory` · `15/verify_light_memory` · `16/verify_phenomenology` (19) ·
`17/verify_main_carrier` (NEW) · `_consciousness/verify_main_carrier` · `_verify/run_regression`
(**114**). Regression count 112 → 114 (M9-geom block reframed to historical-anchor + promotion-landed).

### How to reproduce (from package root)
```
cd repro/mind/_engine && python3 run_all.py            # re-freezes engine -> tree 3a1ebbbb…
cd ../_verify        && PYTHONPATH=../_engine python3 run_regression.py   # 114 PASS
# each chapter:  cd repro/mind/<chapter> && PYTHONPATH=../_engine python3 verify_*.py
```
The 13-em-coordination verifies now treat the **ring sweep as the v1.17 HISTORICAL lineage**
(`matches_full_sweep`/`matches_engine` honestly **False** post-promotion; engine reports measured).

---

## 4. v1.20 ENTRY POINTS (next session)

1. **(1A′) Sulcal-bank mm walls.** 1B grounded the folding critique only **partially** — AAL is
   a *gyral-centroid* resolution (Precentral/Postcentral centroids ~17 mm apart; the literal
   facing sulcal banks ~mm are unresolved). To close the **OWED [O]**: obtain a **sub-gyral /
   sulcal-bank parcellation** (e.g. a finer atlas than AAL) and re-run `geometry_node_decomposition`
   at that resolution; report fc·regime as-is (do **not** back-fit to a target).
2. **(2B′) Theta-pacing anchor [O]→[L].** When the **neuro package** is available in-session,
   take the canonical theta-**pacing** anchor (medial-septum GABAergic pacemaker rate / Ih(HCN)
   kinetics) as a **single-source verbatim [L]** constant and promote the carrier:slow ratio's slow
   leg from engine-[O] `tau_inh=60` to measured. Keep the anti-tuning check (the adopted anchor must
   not be chosen to reproduce 6.125).
3. **(housekeeping) phenomenology prose.** Chapter-16 HTML body still narrates the older 11-matched
   /0.55 figures; the JSON/freeze/registry are at 15-matched/0.75. Optional: refresh the prose to
   match (documentation only; no computational effect).
4. **(optional) sitemap determinism.** `build_search_layer.write_sitemap()` stamps
   `datetime.date.today()`, so `gate.py` idempotency only holds on the build day. If strict
   cross-day reproducibility is wanted, freeze the sitemap `lastmod` to a recorded constant.

---

## 5. DoD (v1.19) — MET

1A ✓ · 1B ✓ · 2A ✓ · 2B ✓ · cascade isolation ✓ · registry ✓ · regression 114 ✓ · chapter 17 ✓ ·
CHANGELOG ✓ · **all 13 gates exit 0** ✓ · final determinism (engine 2× `3a1ebbbb`, geom 2× `8ad43a72`) ✓
· single packaged zip + sha256 ✓.
