# CHARTER — Environmental Inheritance, the RNA Layer, and the Path to RNA Vaccines & Gene Therapy

**kit_id:** `vp_inheritance_kit` · **code:** `inh` · **branch:** jamming (germline / RNA / immune) ·
**version:** 0.1.0-research · **phase:** research

## Scope (one line)
On the shared R19 jamming substrate, with the genome as a fixed SET (measured promoter γ) and the
environment as a reversible DRIVE (h), this kit emerges the mechanism of **transgenerational environmental
inheritance** (a drive surviving the two reprogramming erasures into the germline), the **second writable
channel (small RNA)**, **immune strengthening and its inheritance**, and the extension to **RNA vaccines**
(a dosed supra-spinodal drive) and **gene therapy** (SET edit vs reversible drive-reset). Everything is
direction-only and firewalled; clinical application belongs to clinicians and regulators.

## What this kit emerges (and what it does not)
It emerges, by deterministic simulation on the vendored substrate at measured γ: the RNA drive channel,
the reprogramming firewall, heritability ordering by barrier, immune-memory durability ordering, the
vaccine flip-and-hold, the boost-schedule optimum, and the two therapeutic levers. It does **not** emerge,
and explicitly firewalls out, any absolute phenotype magnitude, dose, titre, wild generation-count, or
clinical outcome — those are [O], named in the ledger.

## Inherited (vendored — read-only, do not re-derive)
- **substrate:** `inherited/vp_substrate.py` — R19 switch / spinodal / barrier / settle / dwell (single source).
- **A4 channel:** `inherited/vp_a4.py` — the coordinate/structure channel (shells / anchors / loops / helical contact); single source. `inherited/a4_coordinates.json` (+ wide-window cache) — measured A4 reads for the carriers.
- **germline γ:** `inherited/germline_gamma.json` (13 genes, measured; DAZL anchor 1.3803) + offline cache.
- **immune γ:** `inherited/immune_gamma.json` (FOXN1/TLX1/RUNX1/PAX5, measured) + offline cache.
- **RNA-carrier γ:** `inherited/rna_carrier_gamma.json` (12 genes, **measured here from NCBI**, SOX9-gated) + cache.
- **discipline:** `VP_SPEC_v1_8.md` (C0–C4), and `00_CONTINUATION_BLUEPRINT.md` Part A (the four invariants).

## Seams (this kit is SSOT for the new objects; it cites the rest)
- **IN (cited):** organ identity + emergence order (DNA gene-clock); the methylation writable channel (DNA
  §6/§9); the gamete machinery + embryo logic (reproductive package); immune memory / prime-boost dynamics
  (immune package). Cited, not re-emerged.
- **OUT (SSOT here):** the small-RNA writable channel; the environment→germline reprogramming firewall; the
  heritability-by-barrier ordering; the vaccine-as-dosed-drive and gene-therapy two-lever maps.

## Discriminant targets (must pass before any writing)
- **R1–R5** RNA writable channel: reversible h-write, two signs, measured atlas, reversibility. [V]
- **A4-1..A4-5** A4 coordinate channel: orthogonal to γ, RNA coordinate-targeting, environment writes A4 not γ, inheritance of an A4 configuration. [V]
- **TG1–TG6** environment→germline: SET invariance, reprogramming firewall (p²), heritability ranks γ,
  sign preserved, RNA decays / methylation persists. [V]
- **I1–I4** immune strengthening: memory MFPT ranks γ, trained pre-tilt, inherited priming (direction-only). [V]/[O]
- **V1–V5** RNA vaccine: supra-spinodal flip + hold, interior schedule optimum, transient-payload/persistent. [V]
- **GT1–GT4** gene therapy: SET-edit moves threshold, reversible drive-reset, decision rule. [V]

## Governance
- VP-SPEC v1.8 governs writing and C1 (determinism) / C3 ([O] reasons) in research. Constitution (C0) wins on conflict.
- **No-tuning:** γ measured from NCBI; the pipeline is accepted only because the SOX9 anchor reproduces.
- **DNA emergence:** every number traces to measured promoter γ + the R19 switch.
- **Magnitude firewall:** WHICH / SIGN / ORDERING read; absolute magnitude / dose / titre / generation [O].
- **Research-first:** writing is locked until the chosen batteries are green and research is signed off.
- **Single deliverable:** one additive zip, internal root `vp_inheritance_kit/`; bootstrap is
  `START_HERE.md → 00_CONTINUATION_BLUEPRINT.md → CHARTER.md`; state passes by files only.
