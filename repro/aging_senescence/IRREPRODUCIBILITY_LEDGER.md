# IRREPRODUCIBILITY LEDGER

Every `[O]` (open) quantity must be listed with its specific obstacle (VP-SPEC C3). An `[O]` without a
stated obstacle is a gate FAIL. This ledger is cross-checked against the canonical HTML in `docs/`.

As of v1.0.0-writing the four master-gene γ values are **measured and vendored** (NCBI RefSeq promoters,
SantaLucia 1998 NN ΔG37, window TSS−2000..+500), so the former "to-measure γ" row is **resolved** and
removed. The reproducible result hash is byte-identical across two runs (SEED=19): `d6506074f9f9ae61…`.

As of v1.2.0-writing the γ–lifespan trend has been **audited against the confounds it was flagged for**
(`repro/_verify/xspecies_robustness_audit.py`, artifact `c771cf7e…`). The audit shows γ is a GC proxy
(ρ=0.96–1.00), the weak shared 4-gene lean (raw combined p≈0.054) is **fully confound-attributable**
(body-mass-corrected p=0.16; phylogenetic independent contrasts p=0.55; multivariate LOOCV label-perm
p=0.115), so the null is now **[V] robust**, not merely untested. One residual **[O]** remains (TERT) and
is listed below.

As of v1.3.0-writing the package adds a telomere deep-dive (RA9) and an OBSERVATION-ONLY archaic↔present-day
comparison (RA8). The measured parts are **[V]** (per-individual γ, γ spread, substitution counts, the
TERT cancer-hotspot invariance, the telomere-repeat γ invariance and lowest-γ ranking) and reproduce
offline bit-for-bit from the committed archaic cache (25/25 sequences match). The two interpretive items
they raise are **[O]** and listed below; the archaic-data coverage and frame caveats are recorded in a
dedicated section at the end. The result hash is re-pinned at `62d5e1eb93db8963…`.

| item | grade | obstacle | location |
|---|---|---|---|
| residual TERT γ–longevity lean | [O] | TERT is the most lifespan-leaning master and the only one whose lean is not removed by body-mass correction (size-corrected ρ=+0.54) and that carries the largest phylogenetic-contrast correlation (+0.58); it still never reaches significance (n=10, p≈0.12), so it is a lead for a larger species panel, not a result. The real telomere lever on lifespan is off the promoter-γ axis (somatic telomerase suppression in large mammals) | repro/_verify/xspecies_robustness_audit.py · docs/09-cross-species-longevity-discriminant/ |
| meaning of the archaic genotype co-occurrences (RA8) | [O] | the package measures, per individual, the promoter γ, the γ spread, and which positions differ — all [V]. WHY the states co-occur across the cross-sectional set is **out of scope by constitution**: a snapshot of present-states does not, and is not used to, support any account of how a state arose. Only the measured co-occurrence is asserted | repro/_engine/archaic_discriminant.py · docs/10-archaic-and-present-day-aging-promoters/ |
| telomere "keystone is dynamics, not γ" synthesis (RA9) | [O] | the telomere-repeat γ invariance, strand symmetry, and lowest-γ ranking are measured [V], and the γ^1.5 reservoir law is the vendored substrate [F]; the *reading* that the telomere is the keystone of aging dynamics (reservoir length + attrition) rather than of γ organizes the package's own measured facts but is an interpretation, not an in-package derivation | repro/_engine/telomere_keystone.py · docs/11-telomere-keystone-dynamics-not-gamma/ |
| absolute incidence / lifespan / calendar rate (RA1, RA2, RA3, RA5; sarcopenia, frailty, cancer) | [O] | the SHAPES reproduce [V] (drift, convex age-incidence, accelerating co-failure), but mapping them to absolute years / probabilities needs an external clock or calibration the package does not contain | repro/_pathology/setpoint_failure.py · repro/_engine/aging_dynamics.py · docs/03,05,07,12 |
| pathology noise scale T and chronic-stressor magnitudes h | [O] | these are stated, round, non-tuned RELATIVE scales that set curve shape only (e.g. cancer hazard T=0.1, frailty stressors −0.22…−0.40); the absolute magnitudes they would imply are not claimed | repro/_pathology/setpoint_failure.py · docs/12 |

## Cited anchors (graded [L], not [O] — listed for provenance)
- Elephant TP53 copy number ≈ 20 (the off-γ longevity switch): Abegglen et al. 2015 (JAMA); Sulak et al. 2016 (eLife). Per-copy γ is essentially unchanged (1.4269), so the switch is dosage, not promoter γ.
- Somatic telomerase suppression in large mammals (the off-γ telomere lever): Gomes et al. 2011 (Aging Cell).
- Telomere length and per-division attrition rates (RA9): Harley et al. 1990; Frenck et al. 1998; Aubert & Lansdorp 2008.
- Archaic / dated-modern genomes (RA8 provenance): Altai Neanderthal — Prüfer et al. 2014; Vindija 33.19 — Prüfer et al. 2017; Chagyrskaya — Mafessoni et al. 2020; Denisova — Meyer et al. 2012; Ust'-Ishim — Fu et al. 2014; Loschbour — Lazaridis et al. 2014. High-coverage all-sites VCFs from the Max Planck EVA archive, GRCh37-aligned.
- Maximum lifespan (MLSP) and adult body mass values: AnAge / Tacutu et al. 2018.

## Archaic-data coverage & frame caveats (v1.3.0 — reproducibility notes, not [O] claims)
- **Chagyrskaya is TERT-only.** The Chagyrskaya VCF is plain-gzip (not bgzf), so random access by genomic coordinate is not economical; only the shallow chr5/TERT window was streamed for that individual. The other two genome-wide genes (TP53, CDKN2A, FOXO3) therefore use the three bgzf-indexed archaic individuals (Altai, Vindija, Denisova). This asymmetry is visible in the §10 table (Chagyrskaya appears only on TERT) and does not affect any per-gene conclusion.
- **Coverage / missingness.** Each reconstructed promoter window is the GRCh37 reference plus that individual's homozygous-derived FILTER-pass substitutions; **uncovered positions default to the reference base and are counted** (covered bp per window ≈ 84–93% of 2501 bp). A reference-fallback at an uncovered site can only make an individual look *more* reference-like, so the small measured γ offsets are lower bounds on the true difference, never inflated.
- **GRCh37 vs NCBI-RefSeq γ frame offset (~0.003).** The archaic data is GRCh37-aligned, so RA8/RA9 measure γ in the GRCh37 frame (e.g. TP53 1.4333), which differs from the §2/§9 NCBI-RefSeq value (TP53 1.4298) by ~0.003 due to assembly/annotation/window-placement. Both place every gene in the same narrow band; all archaic Δγ are computed *within* the GRCh37 frame (correct, since the comparison is internal to that frame) and are never mixed across frames.

## Resolved (no longer open)
- master-gene γ (TP53/CDKN2A/FOXO3/TERT): now measured + vendored in `inherited/organ_gamma.json`; reproduces offline from `inherited/aging_promoters.cache.json` (37/37 checked, 0 mismatches).
- γ–lifespan trend "no signal" (v1.2.0): the null is now **[V]** — audited robust to GC, body-mass, phylogenetic, and multivariate confounds. The over-strong "no trend" wording is corrected to "a weak shared lean that is fully confound-attributable." Only the residual TERT lean remains [O] (above).
