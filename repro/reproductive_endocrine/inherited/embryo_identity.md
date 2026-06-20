# Developmental / body-plan identity (RECEIVED from DNA, then read-only)

The v0.5.0 package emerged the two **gametes** (the germline, G1–G6): a free-running oscillator (the sperm)
and a switch held at metaphase II (the egg). The embryo chapter (§12, module `repro/_embryo/`) carries the
story forward — the gametes are made, so they **meet**, a new genome **emerges**, and a fetus is **built** —
each step a discriminant against the same shared substrate (R19 switch + FHN relaxation oscillator),
reusing the gamete results. The only NEW input is the **measured promoter γ** of a focused DEVELOPMENTAL
master-gene panel, received through the identical DNA pipeline used for the organ and gamete masters
(NN-stacking ΔG37, SantaLucia 1998; promoter window TSS−2000…+500; GRCh38.p14 = GCF_000001405.40).
Sequences are cached in `inherited/embryo_promoters.cache.json` for offline bit-for-bit reproduction; γ
values are read-only and **never fitted**.

The panel was declared **by developmental stage and HOX axis position, before any γ was seen** (no
cherry-picking). Each gene carries its `stage_rank` (the pre-registered hypothesis order: pluripotency = 1 <
germ-layer = 2 < organ-primordium = 3) so the read-out cannot be retrofitted. The reception refuses to
persist unless BOTH vendored anchors reproduce exactly: SOX9 (1.4598) and the v0.5.0 germline master DAZL
(1.3803).

| master gene | stage | measured γ | role in the body plan |
|---|---|---|---|
| NANOG | pluripotency | 1.3479 | inner-cell-mass pluripotency (epiblast competence) |
| SOX17 | germ-layer | 1.3821 | definitive endoderm specifier |
| GATA4 | germ-layer | 1.3933 | endoderm + cardiac-mesoderm specifier |
| HOXB4 | AP-axis (HOX pos 2) | 1.4453 | mid-cluster (trunk) |
| PAX3 | germ-layer | 1.4479 | neural crest / paraxial mesoderm |
| CDX2 | germ-layer | 1.4500 | trophectoderm specifier (ICM-vs-TE decision) |
| SOX2 | pluripotency | 1.4576 | pluripotency + neuroectoderm competence |
| **SOX9** | organ-primordium | **1.4598** | chondrocyte/skeleton master (+gonad) — vendored anchor |
| PDX1 | organ-primordium | 1.4732 | pancreas/duodenum master |
| POU5F1 | pluripotency | 1.4874 | core pluripotency master (OCT4) |
| HOXA1 | AP-axis (HOX pos 1) | 1.4923 | 3′ (anterior, earliest) of the cluster |
| MYOD1 | organ-primordium | 1.4937 | skeletal-muscle master |
| FOXA2 | organ-primordium | 1.4986 | node/notochord → gut/liver/floor-plate master |
| PAX6 | organ-primordium | 1.5110 | eye + forebrain master |
| NKX2-5 | organ-primordium | 1.5130 | cardiac (heart-field) master |
| TBXT | germ-layer | 1.5130 | Brachyury/T: mesoderm + primitive streak |
| HOXA13 | AP-axis (HOX pos 3) | 1.5427 | 5′ (posterior, latest) of the cluster |

> **What γ is used for, and what it is NOT.** The body-plan **emergence order** is the gene-clock —
> `order = argsort(spinodal(γ))` over the measured masters (E4). Because the spinodal is monotone in γ, the
> order is simply γ-ascending: a lower-γ master clears its presence threshold sooner, so it acts earlier in
> development. γ also sets each structure's **relative** size via `DWELL ∝ γ^1.5`. The qualitative results of
> the other stages — fertilisation as a one-way supra-spinodal flip (E1); 1N+1N→2N diploidy restoration and
> the 10⁹⁴ uniqueness floor (E1); 2ⁿ symmetric cleavage with mass conservation (E2); the ICM/TE bistable
> split (E2); ZGA as a one-step spinodal crossing (E3) — are **structural** and do not depend on the γ values.
>
> **Pre-registered γ tests (E4), reported as they fall.** (1) A permutation test of whether γ rises with the
> DECLARED developmental stage (pluripotency < germ-layer < organ-primordium); the stage means rise
> (1.4310 < 1.4373 < 1.4916) and the Spearman test is reported with its p-value, a NULL permitted. (2) A HOX
> 3′→5′ colinearity test (anterior → posterior = early → late); the posterior-most HOX (HOXA13) does sit
> highest, but the small panel gives only partial colinearity, reported honestly. No claim is graded **[V]**
> on the strength of a γ correlation unless the test supports it.
>
> **FIREWALL (CHARTER).** This package owns the **fertilisation event** (its two gametes meeting) and the
> **early embryo** (the oocyte-to-embryo transition — ZAR1/NLRP5, which live in the germline cache). The full
> multi-organ **morphogenesis atlas** and the gene-clock **law** (`argsort(spinodal(γ))`) are the **DNA
> 4D-Blueprint** package's single source of truth; the panel above is a measured **demonstration** of that
> cited clock, not a competing atlas. Brain-facing HPA / felt experience remain firewalled to the Felt
> Cognition paper.
>
> **SSOT.** The developmental genes and their γ are RECEIVED from DNA and live here read-only. γ changes at
> the DNA source and propagates by re-vendoring — never edited locally. The reception was a measurement
> (cached), not a fit. Honest grades travel with each result in `embryogenesis.py` ([V] / [L] / [O]).
