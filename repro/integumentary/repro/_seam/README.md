# `_seam/` — cross-package seam manifest (HANDOFF §5.3)

This additive layer is **not a new mechanism** and **adds no new constant**. It is the integumentary
package's single, labelled, machine-readable **seam record** for the "one body" runner — the artifact
HANDOFF §5.3 asks for:

> *"The pigment-loss → oncology link (vitiligo/albinism lesion → melanoma burst sensitivity) is already
> internal here; expose it as a labelled seam output for the 'one body' runner."*

## What it produces
`python repro/run_seam.py` writes:
- `reports/seam_manifest.json` — the labelled manifest (the machine-readable seam record).
- `reports/seam_results.json` — the verification battery + `seam_gate()`.

## The three seam classes
| class | meaning | live? |
|---|---|---|
| **inherited_in** (3) | read-only inputs vendored from a sibling, never re-derived here — circulatory dermal-perfusion *magnitude* (cited, consumed by T9), DNA organ identity + emergence order + measured γ [V], the R19 substrate primitive | yes (vendored) |
| **internal_live** (1) | the §5.3 headline: the **pigment-loss → oncology** coupling, computed live in this package and now exposed as a labelled output. A melanocyte-target (T3) lesion removes the melanin screen, so the shared oncology hazard rises; the numbers are **re-exported verbatim** from the verified pathology layer (`albinism`, `skin_cancer`, `vitiligo`) | yes |
| **declared_out** (6) | contracts to sibling packages, honestly flagged **DECLARED, not yet live wiring** (the integration harness of §5.3/§5.4 does not exist yet): gene-lesion → `disease_wp` (with the in-package dynamics-side back-pointer per master-map §6.2), immune/rheumatology seams (urticaria, lichen planus, secondary-Raynaud fixed ischemia, rosacea inflammatory chemistry), and out-of-class cutaneous infections | no (declared) |

## The live coupling (exposed, not recomputed)
| field | value | source |
|---|---|---|
| SCC hazard RR, screen removed vs pigmented | re-exported | `skin_pathology.albinism().hazard_RR_albino_vs_pigmented` |
| SCC incidence RR, screen removed | re-exported | `skin_pathology.albinism().incidence_RR_albino_vs_pigmented` |
| SCC hazard RR *with sunscreen* (screen restored) | re-exported | `skin_pathology.albinism().intervention_hazard_RR` |
| melanoma **burst** RR on pigment loss | re-exported | `skin_pathology.skin_cancer().pigment_loss_burst_RR` |
| lesion delivered-UV attenuation (1.0 = no screen) | re-exported | `skin_pathology.vitiligo().disease_attenuation` |

The intervention RR being **lower** than the screen-removed RR is the evidence that the melanin screen is
the **causal lever**, not a correlate.

## Gate (`seam_verify.seam_gate()`)
Green iff all of: **(A) re-export fidelity** — every internal value equals the pathology layer's own
return value, field by field (this is what makes "expose the already-internal link" truthful);
**(B) coupling sign + causal lever** — screen removal raises the hazard (every exposed RR > 1) and an
exogenous sunscreen lowers it; **(C) provenance + contract validity** — every internal number traces to a
named pathology field (no orphan constant), and every declared-out seam is validly targeted or explicitly
out-of-class; **(D) non-disturbance** — the pathology layer's own 2× sha256 hash is unchanged after the
seam runs; plus **2× sha256** bit-reproducibility.

## Grades (C3)
The live coupling is a simulation-verified cross-target **shape [V]** resting on cited epidemiology **[L]**;
the absolute RR magnitude is **[O]** (inherits the oncology obstacle: population baseline + absolute dose
calibration). Inherited and declared seams carry the **owning package's** grade.

## Invariant
This layer **reads** the disease layers; it never alters them. The core `run_all.py` battery is never
imported here, so the core hash `1fb59f556e01…` is untouched a fortiori; the seam carries its own
independent hash. It does **not** touch `repro/_verify/gates.py`.
