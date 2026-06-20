# COMPLETION LEDGER — `integumentary_vp_site` v1.0.0

**Author:** Young Jae Lee (ORCID 0009-0002-7535-8245) · **branch:** jamming (barrier/interface +
external insult) · **governance:** VP-SPEC v1.8 (C0 constitution overrides on conflict).
**This is the single source of truth for what v1.0.0 declares complete, on what evidence, and what
remains.** It is a documentation artifact; the evidence of record is the seven frozen determinism hashes
and the green gates, reproduced by `repro/run_release_audit.py`.

Grade key: **`[V]`** simulation-verified shape · **`[L]`** cited literature anchor · **`[F]`**
regime-scale set-point · **`[O]`** absolute magnitude, open with stated obstacle.

---

## 0 · Release verdict

| check | value |
|---|---|
| in-lane program (jamming class) | **COMPLETE** |
| targets verified | **10** (T1–T9 + oncology kernel) |
| diseases covered + verified | **23** (13 + 4 + 2 + 2 + 2) |
| seam manifest | INHERITED-IN 3 · INTERNAL-LIVE 1 · DECLARED-OUT 6 |
| canonical doc sections (HTML, C4) | **14** + hub |
| frozen determinism hashes (all match) | **7 / 7** |
| all layer gates green | **yes** |
| no-tuning discipline | held (no constant fitted; every γ measured or a named to-measure input — `_to_measure` now empty) |
| release-readiness audit | `reports/release_audit.json` → `all_ok = true` |

The only work remaining is the **live wiring of cross-package contracts** (§4 below), which needs an
integration harness that does not exist in this self-contained package. It is recorded as DECLARED-OUT,
not faked.

---

## 1 · Organs (identity + emergence order owned by DNA; γ measured, never fitted)

| master gene | organ | measured γ | dyn class | provenance |
|---|---|---|---|---|
| TP63 | epidermis | 1.3643 | barrier | vendored morpho_gamma `[V]` |
| KRT14 | keratinocyte | 1.4894 | barrier | vendored morpho_gamma `[V]` |
| MITF | melanocyte | 1.3945 | defense | vendored, NCBI NC_000003.12 `[V]` |
| EDAR | skin_appendage | 1.3696 | appendage | vendored, NCBI NC_000002.12 `[V]` |
| PRDM1 (Blimp1) | sebaceous_gland | 1.3432 | jamming | **fetched** v0.6.0, NCBI NC_000006.12, cached + vendored, reproduces offline `[V]` |

Emergence order (γ ascending, measured): epidermis → skin_appendage → melanocyte → keratinocyte.
PRDM1 is the atlas's lowest γ → earliest spinodal (an emergence-order prediction graded by sign `[V]`).
`inherited/organ_gamma.json` `_to_measure` is now **empty**: no organ is deferred.

## 2 · Targets (the discriminant battery)

| target | mechanism (one line) | grade summary | layer / hash |
|---|---|---|---|
| **T1** barrier permeability | TEWL crosses a diffusion threshold as the barrier thins; discontinuous collapse under insult; tolerance ~γ^1.5 | shape `[V]`, abs `[O]` | core `1fb59f…` |
| **T2** wound healing | injury → unjamming (q>q*=3.81) → collective migration → re-jamming closure; non-closure below critical drive | jamming/unjamming `[V]` | core `1fb59f…` |
| **T3** melanin UV response | UV raises melanin concavely to a protective plateau (negative feedback); screen removal abolishes protection | `[V]`, abs `[O]` | core `1fb59f…` |
| **T4** epidermal turnover | sum of comparable substrate-dwell phases; SC ~14 d → total ~28 d in cited window | shape `[V]`, window `[L]`, days `[O]` | core `1fb59f…` |
| **T5** thermoregulation | sweat recruited past a thermal threshold; evaporative interface flux regulates core temp; runaway above capacity | `[V]`, abs `[O]` | core `1fb59f…` |
| **T6** hair-follicle cycle | relaxation oscillator on existing EDAR γ; anagen-dominant, plateau→collapse | shape `[V]`, fraction/period `[O]` | cycle `d910fa…` |
| **T7** sebaceous-duct occlusion | hysteretic two-state occlusion jam on new measured PRDM1 γ; discontinuous closure / hysteretic reopen (loop ≈2.01) | `[V]`, set-points `[F]`, counts `[O]` | seb `1e8a55…` |
| **T8** cell adhesion | hysteretic two-state binding jam on existing KRT14 γ; two compartments (DSG3 / BP180) on the *same* γ; derived Nikolsky sign | `[V]`, reserve/titres `[F]`, clinical `[L]`, abs `[O]` | adhesion `55dce8…` |
| **T9** neurovascular reactivity | hysteretic two-lock reactivity jam on existing EDAR γ; dilation lock above / constriction lock below; reversible middle | `[V]`, drives `[F]`, clinical `[L]`, abs `[O]`; perfusion magnitude inherited (seam) | vasomotor `53a99f…` |
| **ONCO** UV carcinogenesis | one convex multistage rate: SCC near-linear in cumulative dose; melanoma intermittent/burst-sensitive; tan paradox | shapes `[V]`, anchors `[L]`, incidence `[O]` | core `1fb59f…` |

## 3 · Diseases (23) — each a signed perturbation of one existing knob; intervention = the knob reversed

**Core pathology layer (13)** — `repro/run_pathology.py`, hash `0a4404ccde6559a7…`; 5-way opposite-sign
discriminant passes.

| # | disease | target | covered as |
|---|---|---|---|
| 1 | atopic dermatitis | T1 | chronic barrier-reserve collapse |
| 2 | contact dermatitis | T1 | acute insult crossing the discontinuous collapse |
| 3 | ichthyosis (dynamics) | T1+T4 | desquamation retention near the spinodal |
| 4 | psoriasis | T4 | differentiation-spinodal threshold + autonomous acceleration |
| 5 | chronic / diabetic / pressure wound | T2 | non-closure below the critical unjamming drive |
| 6 | vitiligo | T3 | discontinuous melanocyte-viability loss |
| 7 | melasma / hyperpigmentation | T3 | regulated melanin overshoot (opposite pole of vitiligo) |
| 8 | albinism / OCA (dynamics) | T3→onco | melanin screen removed → hazard RR |
| 9 | hypohidrotic ectodermal dysplasia (dynamics) | T5 | capped sweat → danger band at lower load |
| 10 | primary hyperhidrosis | T5 | lowered recruitment threshold (opposite pole of HED) |
| 11 | heat stroke | T5 | capacity exceeded → runaway |
| 12 | skin cancer (melanoma / SCC / BCC) | onco | intermittent-vs-cumulative + pigment-loss burst |
| 13 | actinic keratosis | onco | SCC precursor (fewer multistage hits) |

**Hair-cycle layer (4)** — `repro/run_cycle.py`, hash `d910fa5d2854…`; 3-way opposite-timing discriminant.

| # | disease | handle | covered as |
|---|---|---|---|
| 14 | androgenetic alopecia | anagen duration | standing anti-growth drive → miniaturisation (0.59→0.49); minoxidil → 0.63 |
| 15 | alopecia areata | premature catagen | sustained immune-type drive collapses anagen (→0.48); regrows on removal (hysteresis) |
| 16 | telogen effluvium | phase sync | transient stressor synchronises a cohort; sheds **one telogen later** (365-step lag), self-limited |
| 17 | anagen effluvium | anagen-matrix arrest | cytotoxic insult sheds **immediately** (lag 0), bypassing telogen |

**Sebaceous-duct layer (2)** — `repro/run_seb.py`, hash `1e8a557d9a8d…`; 3-way opposite-mode discriminant.

| # | disease | handle | covered as |
|---|---|---|---|
| 18 | acne vulgaris | standing high occlusion | drive ≈1.10 past upper spinodal → inflammatory comedo; combined comedolytic+sebostatic+antimicrobial / isotretinoin reopens; de-inflame alone leaves comedonal residue |
| 19 | hidradenitis suppurativa | deep occlusion + rupture | same jam ≈1.50 in deeper apocrine follicles → plug ruptures → scarring sinus-tract; biologics de-inflame, deroofing/excision resets the scar |

**Cell-adhesion layer (2)** — `repro/run_adhesion.py`, hash `55dce8c267ea…`; 3-axis opposite-property
discriminant (plane / Nikolsky / tension) at the *same* antibody magnitude.

| # | disease | compartment | covered as |
|---|---|---|---|
| 20 | pemphigus vulgaris | cell-cell (DSG3) | anti-DSG3 → intraepidermal/suprabasal split, matrix intact ("tombstone"); lateral failure → shear propagates → **Nikolsky +**, flaccid; clearance (rituximab) re-adheres |
| 21 | bullous pemphigoid | cell-matrix (BP180) | anti-BP180, *same magnitude* → subepidermal split, cell-cell intact (lifts whole); basal failure → no propagation → **Nikolsky −**, tense; corticosteroid re-adheres |

**Vasomotor layer (2)** — `repro/run_vasomotor.py`, hash `53a99f522ad6…`; 3-axis opposite-property
discriminant (direction / reversibility-by-lock / vascular-vs-inflammatory).

| # | disease | drive | covered as |
|---|---|---|---|
| 22 | rosacea | standing vasodilator (lowered flush threshold) | net dilator drive past **upper** spinodal → locks dilated (persistent erythema, fixed telangiectasia); early flush is a sub-lock excursion that returns; LL-37/Demodex amplifier → papulopustular; brimonidine blanches but does not reset (hysteresis); laser/IPL resets vessels |
| 23 | Raynaud phenomenon | cold/stress vasoconstrictor | net drive negative → constricted/ischemic basin → **reversible** vasospastic attack (primary crosses no lock); rewarming + vasodilator/CCB abort it |

Boundaries honoured: congenital **epidermolysis bullosa** (KRT14/COL17A1/LAMB3) → gene-key
(`disease_wp`); **secondary Raynaud** fixed ischemia (connective-tissue disease) → immune/rheumatology
seam; **dermal-perfusion magnitude** → inherited circulatory seam. None re-emerged in a dynamics layer.

## 4 · Seam manifest (`repro/run_seam.py`, hash `52b49a95a9ad…`; 4 fidelity checks green)

- **INHERITED-IN (3):** circulatory dermal-perfusion *magnitude* (cited, consumed by T9); DNA organ
  identity + emergence order + measured γ `[V]`; R19 substrate primitive. Vendored read-only, never
  re-derived.
- **INTERNAL-LIVE (1):** pigment-loss → oncology coupling, **re-exported verbatim** from the pathology
  layer (SCC hazard RR ≈2.58×; melanoma burst RR ≈10.59×; sunscreen → SCC hazard RR ≈1.13×; screen =
  causal lever). The seam output provably **is** the internal link surfaced, not a parallel
  implementation. Read `ANCHORS_VERIFIED.md` §A3 for the honesty flag on the melanoma-burst figure
  (kernel-sensitivity, **not** an OCA melanoma-incidence claim — and consistent with OCA's clinical
  melanoma-rarity).
- **DECLARED-OUT (6):** sibling-package contracts, flagged *declared, not yet live wiring*: gene-lesion →
  `disease_wp` (the genodermatosis list); immune/rheumatology seams (urticaria, lichen planus,
  secondary-Raynaud fixed ischemia, rosacea inflammatory chemistry beyond the LL-37/Demodex flag);
  out-of-class cutaneous infections.

## 5 · Frozen determinism contract (evidence of record)

Reproduce with `python repro/run_release_audit.py` (re-runs each canonical runner; asserts each sha):

| layer | runner | sha256 |
|---|---|---|
| core T1–T5 + oncology | `run_all.py` | `1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` |
| pathology (13 + 5-way) | `run_pathology.py` | `0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8` |
| hair-cycle (T6 + 4) | `run_cycle.py` | `d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822` |
| sebaceous (T7 + 2) | `run_seb.py` | `1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84` |
| adhesion (T8 + 2) | `run_adhesion.py` | `55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad` |
| vasomotor (T9 + 2) | `run_vasomotor.py` | `53a99f522ad684a11bcc6d4d33c5e8123d1f4dff5a75836c0bbced6736a62003` |
| seam manifest | `run_seam.py` | `52b49a95a9add070a05a02848b1a4cef0589f4a36791167232fda3fc1c1d58f7` |

The v1.0.0 release is **label-only** over v0.9.0's computation: the version string and build date were
bumped and the HTML re-stamped; the seven hashes above are **byte-identical** to v0.9.0. The release adds
exactly one additive, read-only artifact (`repro/run_release_audit.py`) and the governance documents.

## 6 · Anchor verification (v1.0.0, network)

Recorded in full in `ANCHORS_VERIFIED.md`: T4 turnover window resolved (`TO-ANCHOR` cleared); melanoma
intermittent/sunburn + chronic-protective dichotomy confirmed (Gandini SRR ~1.6, chronic inverse); SCC
cumulative near-linear confirmed (occupational OR ~1.77); OCA → SCC hazard confirmed (SCC 75–88 %, up to
~1000× in African albinos) with the melanoma-burst figure flagged as a kernel-sensitivity quantity. No
computation changed.

## 7 · Open items (the honest remainder)

1. **Live wiring of DECLARED-OUT contracts** (HANDOFF §5.3 first bullet + §5.4): import `disease_wp`
   gene-key parameters (XP/OCA/EDA/genetic-ichthyosis), have the dynamics entries emit the
   systemic-trajectory side, and register each gene-lesion on the `disease_wp` side with a back-pointer.
   **Blocked on the integration harness, which does not exist.** Out of this package's self-contained
   scope by construction.
2. **Sibling-package seams** for urticaria / angioedema and lichen planus (immune-effector), and the
   fixed-ischemia secondary-Raynaud connective-tissue seam (rheumatology). Named, not this package's
   jamming-class lane.
3. **Out-of-class** cutaneous infections (impetigo, cellulitis, dermatophytosis, herpes, warts):
   pathogen-driven, not an R19-dynamics failure. Not in any dynamics lane.
4. **DOI minting / deposit (done 2026-06-19):** concept DOI **10.5281/zenodo.20754541** (all versions) and
   per-version DOI **10.5281/zenodo.20754542** (v1.0.0) are minted on Zenodo and stamped into every
   chapter + hub claim-strip, the per-page JSON-LD (`sameAs`), `docs/_meta.json`, and `DEPOSIT_README.md`.
   This was a deposit-time action, not a code change — the seven frozen hashes re-verify 7/7 unchanged.
5. **Optional refinements** (recorded, not blocking): widen the stated T4 window toward ~48–56 d to match
   the newer literature; split BCC from SCC toward the intermittent pole. Both are documentation/anchor
   refinements that would not touch the `[V]` shapes.
