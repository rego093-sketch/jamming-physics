# Exhaustive ledger — clade-specific methylation readers

> Grades: **[F]** read & reproduced · **[V]** measured in-package · **[L]** peer-reviewed ·
> **[O]** open-empirical, naming the closing dataset · **[B]** category boundary.

**Totals:** 16 quantities — **11 [F] · 0 [V] · 3 [L] · 2 [O] · 0 [B]**. Positively evidenced (F/V/L) = **14/16**. Ungraded = **0**.

Regenerate: `python3 repro/dna/12-clade-methylation-readers/run.py`.

## Vertebrate reference (the contrast)

| quantity | grade | basis / obstacle |
|---|:---:|---|
| human bulk CG/CHG/CHH O/E | **[F]** | window median, recomputed |
| global CG methylation (vertebrate) | **[L]** | Smith & Meissner 2013; whole-genome 5mCG |

## Plant reader (CG+CHG+CHH)

| quantity | grade | basis / obstacle |
|---|:---:|---|
| bulk CG/CHG/CHH O/E for 6 plant genomes | **[F]** | window median, recomputed |
| CG+CHG depletion = plant signature (incl. basal moss) | **[F]** | all 6 < 1.0 |
| CHH not depleted (sparse asymmetric context) | **[F]** | CHH ~1.1 across plants |
| plant CG+CHG+CHH methylation via RdDM | **[L]** | Law & Jacobsen 2010 |
| absolute plant methylation beta per context (CG/CHG/CHH levels) | **[O]** | the depletion gives the evolutionary substrate; live beta needs plant WGBS CX-report |

## Insect reader (bulk-none + per-gene targeted)

| quantity | grade | basis / obstacle |
|---|:---:|---|
| bulk CG/CHG O/E for 6 insect genomes | **[F]** | window median, recomputed |
| NO bulk CG depletion in any insect (architecture != vertebrate/plant) | **[F]** | all bulk CG >= 0.85; methylation, where present, is not global |
| per-gene CpG O/E profile (spread + low-CpG fraction) for 6 insects | **[F]** | recomputed from RefSeq mRNA sets |
| honeybee targeted gene-body methylation (per-gene low-CpG class) | **[F]** | spread 0.32, 11% genes <0.6; the Elango/Lyko bimodal signature |
| Hymenoptera methylate, Diptera do not (the within-insect split) | **[L]** | Lyko et al. 2010 (Apis gene-body 5mC); Raddatz et al. 2013 (Drosophila no 5mC) |
| Diptera substrate inert -> methylation-independent regulation | **[F]** | fly/mosquito per-gene tight ~1, 0% low-CpG class |
| weak-signal insects (wasp/silkmoth/beetle) below detection at this sample | **[O]** | resolving needs larger RefSeq mRNA panels or direct WGBS per species |

## Auto-detector

| quantity | grade | basis / obstacle |
|---|:---:|---|
| methylation-regime classification (4 regimes) | **[F]** within ~33-45% GC | bulk-then-per-gene router; correct for all in-panel cases AND out-of-panel plants/mammals (v1.9 stress, tomato/cow/dog). **Bounded: false-positive PLANT for extreme-AT genomes (GC <= ~25%)** — see correction below |
| architecture-matched reading (global->bulk, targeted->per-gene) | **[F]** | the principle: read the substrate the way the clade writes it |

## v1.9 stress correction — auto-detector GC boundary (Workstream: stress battery)

The "all test cases correct" claim above held only for the original panel. Two v1.9
stress tests (`stress_detector_adversarial/`, and the out-of-sample validation in
`../14-defensive-guards/stress_guard_validation/`) found a **characterized
false-positive boundary**:

| finding | grade | basis |
|---|:---:|---|
| within-regime generalization to unseen species (plants, mammals) | **[F]** | tomato->PLANT, cow/dog->VERTEBRATE all correct (out-of-panel, frozen inputs) |
| out-of-category biology declined honestly (fungal RIP, mollusk gene-body) | **[F]** | neurospora, oyster -> `no_global` (no fabricated class) |
| **false-positive PLANT for extreme-AT genomes (GC <= ~25%)** | **[O]->corrected** | Plasmodium 20.4%, Dictyostelium 22.3%, **Entamoeba 24.5%** (out-of-sample) all raw-called PLANT despite no global 5mC. Obstacle: CpG/CpHpG depletion at extreme AT is composition-driven, not methylation — proven by matched-composition nulls (iid + mono-shuffle return CHG O/E ~0.99, no class). Corrected at the chapter-14 guard layer (`detect_regime_safe`, GC floor 0.25), validated out-of-sample (no real methylator < 31.6% GC; guarded 7/7) |
| **shipped panel Plasmodium call** `PLANT_global_CG_CHG_CHH` | **corrected** | this is itself an instance of the false-positive mode; `detect_regime_safe` returns `no_global` + `low_GC_composition_confounded` (raw call retained for audit). Locked engine unchanged; correction lives in the guard wrapper |

The router's principle ("read the substrate the way the clade writes it") stands; the
**numeric thresholds** simply have no valid domain below ~25% GC, where the depletion
signal they read is not written by methylation. No threshold was changed in the locked
engine (a GC-conditioned threshold would be a new version); the guard wraps it.

## The principle

The methylation substrate is not just a **context** (CG vs CHG vs CHH) but an **architecture**
(global blanket vs targeted gene-body vs none). A vertebrate-style bulk-CpG reader returns a
**false negative** for honeybee, whose methylation is real but targeted to a gene subset. The
auto-detector reads bulk first and escalates to per-gene only when there is no global signal —
so it correctly reports vertebrate (global CG), plant (global CG+CHG+CHH), targeted-insect
(Hymenoptera gene-body), and non-methylating insect (Diptera). **Read the substrate the way
the clade writes it.**