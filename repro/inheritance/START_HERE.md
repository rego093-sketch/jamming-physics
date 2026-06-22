# START HERE — VP Inheritance Kit

> **Concept DOI:** [10.5281/zenodo.20783547](https://doi.org/10.5281/zenodo.20783547) (Zenodo, resolves to the latest version) · author Young Jae Lee, ORCID 0009-0002-7535-8245 · CC BY 4.0.

> **Research is COMPLETE — Tracks I–V all closed on the simulation axis (18 batteries green).** The one open frontier, the **(B) held-out validation**, is now **bidirectionally scored**: the corrective sign-law's **`−` arm** (battery **FV7**, v0.17.0, held-out DepMap CRISPR-KO: GOF oncogenes are dependencies, LOF suppressors are not — point-biserial = +0.494, exact p = 0.0227) **and its `+` RESTORE arm** (battery **FV8**, v0.18.0, held-out Horlbeck 2016 CRISPRa: LOF suppressors are growth-suppressive on activation, GOF oncogenes are not — point-biserial = +0.4852, exact p = 0.0274) are **both** confirmed — identified and firewall-clean — so the sign-law is now **BIDIRECTIONALLY `[V]`** (the kit's first and second held-out POSITIVES). **No simulation-axis (B) item remains open.** **O-22** (per-patient corrected-yes/no) nonetheless stays `[O]`: with both arms scored, its residual obstacle is no longer data but the **firewall itself** — a class-level direction-only sign-law cannot certify a per-patient absolute outcome (that needs the firewalled per-patient magnitude; absolute dose = **O-21**). If you are here to produce the final result, read
> `HANDOVER.md` first — it carries the status, the full findings synthesis, and the next steps.

> Drop this single zip into a fresh window and **read this file, then `00_CONTINUATION_BLUEPRINT.md`,
> then `CHARTER.md`** — you can begin research immediately, with no upstream whitepaper. The kit is
> self-contained: it carries the vendored substrate primitive (the R19 jamming switch), the measured
> promoter γ atlases (germline / immune / RNA-machinery / disease), the research engines, and a runnable gate.

## 0. One-line identity
The genome is read on **two channels**: the **SET** (the master-gene promoter γ that scales every R19
switch — fixed in the genome, the environment cannot rewrite it) and the **A4 COORDINATE** (where an
element sits in the compartment-shell + anchor-loop architecture, and whether it is on the same helical
FACE as its anchor — contact-competent). The environment writes a reversible **DRIVE** h, and it does so
through the **A4 channel** (and methylation), never through γ; a small RNA acts by sequence complementarity
= it specifies an A4 coordinate and deposits a drive there. This kit answers, on that one substrate, **how a
parent's environment reaches a child** (the drive must survive two genome-wide reprogramming erasures to
reach the germline), **how immunity is strengthened and inherited** (memory is a held basin; training is a
pre-tilt), and **how this extends to RNA vaccines and gene therapy** (a vaccine is a dosed supra-spinodal
drive; gene therapy is either a SET edit or a reversible drive-reset). The new physical objects are the **second writable channel — small RNA** (alongside the DNA paper's
methylation channel) and, central to all of it, the **A4 coordinate channel** that γ alone cannot specify:
γ is the unwritable material; A4 is the writable structure the environment reorganises and RNA targets.

## 1. Run it now (start research)
```
python repro/run_all.py
```
This runs, deterministically and offline: the **NCBI offline verify** (recompute the RNA-machinery γ from
the cached promoters; the SOX9 anchor must reproduce — the no-tuning gate), the **eighteen batteries**
(R / RS / A4 / TC / TG / GE / CH / I / IM / V / GT / AM / FM / DM / FV / PO / VK / LV), and a **2×sha256 determinism gate**. It writes `reports/research_complete.json`
with `all_green`. Current status: **all_green = true** (anchor reproduces, all eighteen batteries PASS,
determinism holds).

Run a single battery directly:
```
python engine/rna_layer.py                  # R1–R5  the RNA writable channel
python engine/rna_species.py                # RS1–RS5 species-resolved RNA (miRNA/piRNA/tsRNA/m6A)
python engine/a4_layer.py                   # A4-1..A4-5 the A4 coordinate channel (γ⊥A4, RNA targets coordinates)
python engine/two_channel.py                # TC1–TC4 methylation × RNA on one switch (add/veto/path)
python engine/env_to_germline.py            # TG1–TG6 environment -> germline (the reprogramming firewall)
python engine/germline_escapee.py           # GE1–GE4 imprinted escapees + two erasures + re-writing
python engine/coordinate_heritability.py    # CH1–CH4 γ↔A4 coupling (coordinate-resolved heritability, parent-of-origin)
python engine/transgenerational_immunity.py # I1–I4  immune strengthening + inherited priming
python engine/immune_maturation.py          # IM1–IM4 affinity maturation · innate/adaptive split · tolerance
python engine/rna_vaccine.py                # V1–V5  vaccine as a dosed RNA drive
python engine/gene_therapy.py               # GT1–GT4 two therapeutic levers
python engine/a4_application_map.py         # AM1–AM4 (γ,A4) application map + the 3D contact boundary curve
python engine/rna_feasibility_map.py        # FM1–FM4 "does RNA change the cell?" map (A) vs validation (B) + autism extension
python engine/disease_feasibility_map.py    # DM1–DM4 disease-class map: cancer + Parkinson's, corrective-sign law, two-lever decision, cross-package check
python engine/feasibility_validation.py     # FV1–FV8 the (B) held-out score (NULL) + GC-identifiability stress test + decomposition + sign-law `−` arm (DepMap) & `+` arm (CRISPRa), bidirectionally [V]
python engine/parent_of_origin.py           # PO1–PO3 parent-of-origin: sustained-maternal vs transient-paternal, sign law, universality
python engine/rna_vaccine_kinetics.py       # VK1–VK2 prime-boost interval optimum (GC rounds) · saRNA vs mRNA reachability
python engine/lever_map.py                  # LV1–LV4 lever map: A/B sub-types, decision boundary curve, edit-free durable correction
```
Re-measure γ from NCBI (online; not needed to reproduce — the cache already reproduces bit-for-bit):
```
python data/fetch_rna_gamma.py --fetch
```

## 2. What is inherited (vendored — do not re-derive)
- `inherited/vp_substrate.py` — the **single source** of the switch math: `sdot` (ds/dt = γs − s³ + h),
  `spinodal(γ)=2(γ/3)^1.5`, `barrier(γ)=γ²/4`, `settle`, `is_on`, `dwell`. Read-only.
- `inherited/vp_a4.py` — the **single source** of the A4 coordinate channel: `run_key` (sequence →
  compartment shells → anchors → loops) and `locate_in_A4` (shell class + nearest anchor + 3D helical
  contact phase), plus the orthogonal material read `cpg_oe`. Read-only.
- `inherited/germline_gamma.json` (+ `germline_promoters.cache.json`) — the **measured** gamete-machinery
  γ atlas (13 genes; DAZL 1.3803, REC8 1.4525, …). Offline bit-for-bit.
- `inherited/immune_gamma.json` (+ `immune_promoters.cache.json`) — the **measured** immune master γ
  (FOXN1 1.4533, PAX5 1.4892, TLX1 1.4228, RUNX1 1.3225).
- `inherited/neuro_gamma.json` — **measured (v0.7.0)**: the autism-spectrum master-gene γ (10 SFARI monogenic
  ASD genes: MECP2, FMR1, SHANK3, CHD8, NRXN1, NLGN3, PTEN, TSC2, SCN2A, SYNGAP1), declared by function,
  measured through the identical SOX9-anchor-gated pipeline. The brain-cell extension for FM.
- `inherited/onco_gamma.json` (+ cache) — **measured (v0.8.0)**: the cancer-gene γ atlas (16 genes; tumour
  suppressors TP53, RB1, PTEN, VHL, APC, BRCA1, NF1, CDKN2A, STK11 and oncogenes KRAS, MYC, EGFR, BRAF, MDM2,
  BCL2, PIK3CA), declared by function, measured through this kit's own SOX9-anchor-gated fetcher (γ-order
  APC 1.3748 → PTEN 1.5694). Each gene carries a mechanism-forced corrective sign. The cancer extension for DM.
- `inherited/neurodegen_gamma.json` (+ cache) — **measured (v0.8.0)**: the neurodegeneration γ atlas (9 genes;
  Parkinson's SNCA, LRRK2, VPS35, PRKN, PINK1, PARK7, GBA1 plus the HTT/SOD1 proteinopathy bridge), declared by
  function, same anchor-gated fetcher (γ-order SNCA 1.2490 → HTT 1.6142). The Parkinson's extension for DM.
- `inherited/rna_carrier_gamma.json` (+ cache) — **measured from NCBI**: the small-RNA / transgenerational-
  RNA machinery γ (12 genes; DROSHA, DGCR8, DICER1, AGO2, TARBP2, PIWIL1, MOV10L1, DDX4, METTL3, YTHDF2,
  ELAVL1, ANG). Anchor-gated by SOX9.
- `inherited/imprint_gamma.json` (+ cache) — **measured from NCBI (v0.2.0)**: imprinted / parent-of-origin
  locus γ (12 loci; IGF2, H19, KCNQ1OT1, SNRPN, MEST, PEG3, PLAGL1, GNAS, DLK1, MEG3, NNAT, GRB10) — the
  canonical reprogramming escapees. Anchor-gated by SOX9.
- `inherited/a4_coordinates.json` (+ `a4_windows.cache.json`) — **measured from NCBI (v0.3.0)**: the A4
  coordinate of each RNA carrier, read from wide (±15 kb) windows — the structure channel that is
  orthogonal to γ.
- `VP_SPEC_v1_8.md` — the vendored discipline (C0–C4).

All γ are MEASURED (NN-stacking ΔG37, SantaLucia 1998, promoter TSS−2000..+500, GRCh38), **never fitted**,
and accepted only because the pipeline reproduces the SOX9 anchor (γ=1.4598, GC=0.545).

## 3. The eighteen discriminant batteries (must stay green)
- **R (rna_layer)** — small RNA is a reversible h-write; two signs (siRNA→OFF / saRNA→ON); the measured
  carrier atlas is R19-bistable; the drive is reversible (payload cleared → basin returns). [V]
- **RS (rna_species)** — resolves small RNA into miRNA/piRNA/tsRNA/m6A by measured machinery: each a signed
  drive; production stability orders by machinery barrier (piRNA deepest); METTL3/YTHDF2 writer/eraser
  reversibility; germline-competent carriers (piRNA/tsRNA/VASA) identified. [V]
- **A4 (a4_layer)** — the A4 coordinate channel is ORTHOGONAL to γ (γ tracks GC R²≈69%, but the helical
  contact phase is ≈98% independent; same-γ/different-contact pairs exist); RNA is coordinate-targeting
  (contact-competence gates a fixed drive at fixed γ); the environment writes A4, not γ; inheritance is of
  an A4 configuration. **γ alone is degenerate — A4 is the writable, RNA-targeted channel.** [V]
- **TC (two_channel)** — methylation × RNA both write h on one switch: same-sign ADD, opposite-sign VETO,
  hysteresis PATH-DEPENDENCE (the order of writes latches the state). [V]
- **TG (env_to_germline)** — the SET is byte-identical parent→child; the reprogramming firewall squares a
  mark's survival (p²); heritability ranks ascending-γ (deeper barrier inherits better, Spearman ρ≈0.99);
  the inherited sign is preserved; an RNA-only drive decays by ~F3 while a deep-barrier mark persists. [V]
- **GE (germline_escapee)** — on the measured imprinted atlas: survival ranks ascending-γ (KCNQ1OT1 best,
  SNRPN worst, ρ=1.0); the two erasures resolved (PGC vs zygotic, harsher dominates); a measured critical
  re-write rate w* separates maintained from transient inheritance. [V]
- **CH (coordinate_heritability)** — heritability couples γ AND A4: at matched γ the contact-competent
  coordinate inherits better (MEST vs MOS); parent-of-origin contact configuration mapped; the joint
  (γ, A4) ordering puts deep-γ + contact-competent loci on top (NNAT). [V]
- **I (transgenerational_immunity)** — immune memory is a held basin whose lifetime (MFPT) ranks
  ascending-γ; trained immunity is a pre-tilt that lowers the recall drive; the tilt can ride the germline
  RNA payload (direction-only, fading). [V]/[O]
- **IM (immune_maturation)** — affinity maturation **emerges** from an iterated germinal-centre loop (the
  gain has an **interior optimum** in selection stringency, peaking at survivor-fraction 0.4); innate
  (RUNX1) vs adaptive (PAX5) is a **two-timescale durability split** (MFPT ratio ≈2.37, slow arm = deeper
  barrier, tracking the measured γ); tolerance is the **opposite-sign drive** on the same switch — memory↔
  tolerance with symmetric thresholds and **both** end-states held after the drive clears (hysteresis). [V]
- **V (rna_vaccine)** — a vaccine is a supra-spinodal flip into the protected basin, held after clearance;
  the boost schedule has an interior optimum tracking the measured protection half-life; the payload is
  transient yet protection persists. [V]
- **GT (gene_therapy)** — Lever A edits the SET (moves spinodal/barrier, irreversible by a drive); Lever B
  resets the drive reversibly via RNA; the lever choice is a geometry threshold. [V]
- **AM (a4_application_map)** — the applications live on the (γ, A4) plane: prime-boost dose is
  coordinate-dependent; the two levers partition (γ, contact); the **3D contact boundary curve** δ*(γ)
  rises with γ (a deeper switch needs more A4 contact-assist to stay drive-reachable). [V]
- **FM (rna_feasibility_map)** — answers "does putting RNA in actually change the cell?" honestly: the
  **map** is [V] (flip-drive = measured spinodal; absolute flip-drive ordered by measured γ; reversible vs
  latched by drive magnitude; saRNA↔siRNA sign), but a self-contained sim **cannot** return the yes/no — it
  rides on the firewalled drive Δh atop the assumed R19 dynamics, so a "flipped" screen is Δh-assumption
  replay, not evidence (the crossing to evidence is the **(B)** held-out score, no-tuning). Extends to the
  **measured autism atlas** (every ASD promoter R19-bistable, flip-drive ordered by γ). [V] map / yes-no [O].
- **DM (disease_feasibility_map)** — carries the feasibility map into the **disease class** (cancer + Parkinson's),
  inheriting the panels from the sibling `vp-site` program by **re-measuring** (never importing) γ — so four shared
  loci (PTEN, VHL, SOD1, HTT) reproduce to 4 decimals as a **no-tuning cross-package check**. DM1 every cancer +
  neurodegeneration promoter is R19-bistable, correction-difficulty ordered by measured γ. DM2 the **corrective-sign
  law**: the mechanism-forced sign (LOF→`+` restore / GOF→`−` knockdown) drives each gene out of its pathological
  basin while the opposite sign from the same basin does not — and the sign is **orthogonal to γ** (suppressors and
  oncogenes interleave, point-biserial ≈ −0.015). DM3 the **two-lever decision**: reversible Lever-B is reachable
  for every switch (required drive grows with γ), Lever-A reserved for coding-SET lesions (= the firewall). DM4 the
  (A)/(B) honesty gate + cross-package invariant. [V] map + sign law / per-patient yes-no [O].
- **FV (feasibility_validation)** — the **(B) held-out score, run once** on the ordering axis: scored against
  held-out Replogle 2022 CRISPRi knockdown depth (γ measured from DNA, frozen before any expression seen), it is
  a recorded **NULL** (ρ=−0.08, p=0.63) that promotes nothing. **FV5** is the GC-identifiability stress test: γ
  tracks promoter GC by construction (ρ≈0.99) and CRISPRi efficiency is GC/accessibility-driven, so partialling
  GC out leaves no identified γ signal — the ordering score is **non-identified**, not "signal absent". **FV6**
  generalises this to a partition: every γ-*ordered* prediction is non-identified as a class, and the corrective
  **sign-law** (DM2: LOF→`+`, GOF→`−`) is the **sole** crossing that is both identified (orthogonal to GC) and
  firewall-clean — its only obstacle is **bidirectional disease-correction data**, not Δh. **FV7** scores the
  sign-law's **`−` arm** on held-out DepMap CRISPR-**KO** (GOF oncogenes are dependencies, LOF suppressors are
  not — point-biserial=+0.494, exact p=0.0227) — the kit's **first held-out POSITIVE**. **FV8** scores the **`+`
  RESTORE arm** on held-out Horlbeck 2016 **CRISPRa** (LOF suppressors are growth-suppressive on activation, GOF
  oncogenes are not — point-biserial=+0.4852, exact p=0.0274) — the **second** held-out POSITIVE and the mirror
  of FV7, so the sign-law is now **bidirectionally `[V]`** (both arms, direction-only). **O-22** stays `[O]` — its
  obstacle is now the **firewall** (per-patient magnitude), not data; **O-21** (absolute dose) stays `[O]`. [V]
- **PO (parent_of_origin)** — parent-of-origin from the *temporal context* of the payload: the egg holds a
  **sustained** maternal drive, the sperm delivers a **transient** bolus, so at EQUAL amplitude a held switch is
  crossed by **duration** — maternal flips, transient paternal reverts (PO1); the dominant maternal **sign** is
  inherited under opposing parents, agreement reinforces (PO2); the asymmetry is **universal** across the measured
  germline atlas, 13/13 (PO3, with the honest ρ=−1.0 crossing-time ordering reported as-it-falls, not graded). [V]
  / absolute penetrance [O].
- **VK (rna_vaccine_kinetics)** — the prime–boost interval has an **interior optimum** in germinal-centre rounds
  (the IM1 GC loop reused unchanged, decay at the measured escape rate): too short under-matures, too long lets
  protection decay (VK1); saRNA's longer same-amplitude drive window crosses the protected basin **more reliably**
  than mRNA, with post-flip durability honestly the identical barrier (VK2). [V] / absolute days, titre [O].
- **LV (lever_map)** — the lever map: LV1 Lever-A sub-types (knockout/base-edit/prime-edit move the threshold;
  **CRISPRa re-classifies to Lever B**); LV2 Lever-B sub-types (siRNA −, ASO-splice a fixed-γ coordinate change,
  saRNA +, miRNA-sponge +, all reversible at fixed γ); LV3 the **decision boundary curve** h_path*(γ) = h_cap −
  spinodal(γ) falls with γ and crosses zero at a finite γ* beyond which Lever A is mandatory (substrate-confirmed
  both sides); LV4 durable correction **without an edit** by re-dosing above a critical re-write rate w*. [V] /
  absolute efficiency, schedule [O].

## 4. The firewall (non-negotiable)
We read **WHICH** switch is tilted, the **SIGN** of the drive, and the **ORDERING / DECAY** of
heritability and memory. We never assert an absolute inherited phenotype, dose, titre, or wild
generation-count — those are runtime **[O]**. Every clinical application (vaccination, gene therapy,
fertility care) is explicitly handed to **clinicians and regulators**. See
`IRREPRODUCIBILITY_LEDGER.md` for every [O] item and its obstacle.

## 5. Return contract
On exit, return **exactly one zip** whose internal root is `vp_inheritance_kit/`. Additive only — never a
fresh tree, never a regression. New work is merged onto the received files and handed forward as that one
zip. The next session bootstraps from `START_HERE.md → 00_CONTINUATION_BLUEPRINT.md → CHARTER.md` alone.
```

The full forward roadmap (RNA vaccines, gene therapy, and the science to harden) lives in
`00_CONTINUATION_BLUEPRINT.md`. Read it before adding anything.
