#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prioritise_diseases.py  --  burden-weighted prioritisation of DISEASES/READS (not drugs).

  *** INHERITED from analgesic_threshold_logic_v2_0  M10 (build_prioritisation.py),
      DOI 10.5281/zenodo.20733420.  Same declared weights, same firewall discipline,
      ported from analgesic TARGETS to disease-kit RESOLVED DISEASES. ***

The author's stated goal is to lower the MAXIMUM suffering for the GREATEST number of people.
So this is a small, transparent ranking that combines three CITED Layer-2 tiers --
  B = burden        (prevalence x severity of the disease; epidemiology-anchored, 1..5)
  U = unmet need    (how poorly the current LEAD lever serves it; 1..5 -- a no-DMT / downstream-
                     only / investigational lead scores HIGH, a transformative approved switch
                     lever scores LOW)
  D = druggability  (clinical validation / tractability of the lead lever; 1..5 -- a *consistency
                     floor* is derived from the lead lever's own `status` field in the frozen
                     analysis.json, so D cannot silently disagree with the shipped evidence)
under DECLARED weights, to surface the burden leaders.

THE WEIGHTS ARE DECLARED, NOT TUNED TO A DESIRED ANSWER (identical to analgesic M10):
  w_B=0.40, w_U=0.35, w_D=0.25  -- burden and unmet-need lead (the stated goal: most suffering,
  most people); druggability is included so the ranking favours tractable directions but cannot
  let mechanistic elegance override need.  score = w_B*B + w_U*U + w_D*D   (range 1..5).

HONESTY (binding -- inherited firewall):
  - B/U/D are CITED Layer-2 tiers; the weights are an explicit editorial choice. The ranking is
    therefore [F] from cited tiers + declared weights -- NOT a [V] engine output.
  - The engine read's place in the map (primary-switch gamma and barrier depth) is carried
    ALONGSIDE each disease as STRUCTURAL context. It is NOT folded into the clinical priority
    score: gamma/barrier is a promoter-stiffness read, not a clinical magnitude, and the firewall
    forbids equating them. (This is the analgesic gamma-|h_sp| rule, verbatim in spirit.)
  - This ranks DISEASES/READS, not drugs. No molecule, dose, efficacy, or safety is ranked here.
  - SUSPENDED diseases are NOT ranked (no analyzable single-gene switch -> no read to prioritise).

No tuning: fixed cited tiers + fixed declared weights + deterministic sort. stdlib only.

Run:  python3 pipeline/prioritise_diseases.py [--write]
        --write  also writes repro/modules/expected/disease_priority_ranking.json
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DISEASES = os.path.join(ROOT, "diseases")

# DECLARED weights (explicit; sum = 1.0) -- IDENTICAL to analgesic M10. Burden/unmet-need-leading.
WEIGHTS = {"B": 0.40, "U": 0.35, "D": 0.25}

# Consistency floor: the lead lever's frozen `status` bounds D so the editorial tier cannot
# silently over-state tractability beyond the shipped evidence.
STATUS_D_FLOOR = {"approved": 4, "clinical": 3, "investigational": 2}
STATUS_D_CAP   = {"approved": 5, "clinical": 3, "investigational": 2}

# CITED tiers per RESOLVED disease (B,U,D in 1..5) with a one-line epidemiology+lead-lever basis.
# B = prevalence x severity; U = unmet need given the lead lever; D = tractability of the lead lever.
DISEASE_TIERS = {
  # ---- highest population burden (common, severe monogenic disease) ----
  "sickle_cell_disease": dict(B=5, U=3, D=5,
     cite="millions affected globally, severe pain/organ damage/early mortality; exa-cel HbF re-induction approved 2023, access+scale-limited (Frangoul 2021 NEJM)"),
  "beta_thalassaemia": dict(B=5, U=3, D=5,
     cite="among the commonest monogenic disorders, transfusion-dependence; luspatercept (FDA 2019) + beti-cel gene therapy, transfusion burden persists (Cappellini 2020)"),
  "familial_hypercholesterolaemia": dict(B=5, U=3, D=5,
     cite="heterozygous ~1/250-313, major premature-ASCVD population burden; PCSK9 inhibitors approved, HoFH+undertreatment residual (Nordestgaard 2013)"),
  "cystic_fibrosis": dict(B=4, U=3, D=5,
     cite="~1/2,500 European-ancestry, severe multi-organ; CFTR modulators transformative, non-F508del + advanced disease residual (Middleton 2019 NEJM)"),
  "hereditary_haemochromatosis_type_1": dict(B=4, U=2, D=5,
     cite="C282Y homozygosity ~1/200 N. European (reduced penetrance), iron-overload organ damage; phlebotomy simple and effective when caught (Adams 2005)"),
  "duchenne_muscular_dystrophy": dict(B=4, U=5, D=4,
     cite="~1/3,500-5,000 males, progressive/fatal; micro-dystrophin transfer partial, not curative (Mendell 2023)"),
  "spinal_muscular_atrophy": dict(B=4, U=3, D=5,
     cite="~1/10,000, historically a leading genetic infant mortality; SMN2 modifiers + gene therapy transformative, timing-dependent residual (Finkel 2017 NEJM)"),
  "huntington_disease": dict(B=4, U=5, D=3,
     cite="~1/10,000-15,000, uniformly progressive/fatal; NO approved disease-modifying therapy -- HTT-lowering still clinical (Tabrizi 2019)"),
  "hypertrophic_cardiomyopathy": dict(B=4, U=3, D=5,
     cite="~1/500, commonest inherited cardiomyopathy, SCD risk; mavacamten (FDA 2022) modifies obstruction, not curative (Olivotto 2020)"),
  "phenylketonuria": dict(B=4, U=3, D=5,
     cite="~1/10,000-15,000 newborns (screened), severe if untreated; diet + sapropterin + pegvaliase, lifelong dietary burden (Blau 2010)"),
  # ---- high severity, intermediate prevalence ----
  "transthyretin_amyloidosis": dict(B=3, U=3, D=5,
     cite="commonest hereditary amyloidosis, polyneuropathy/cardiomyopathy; patisiran/tafamidis effective, established organ disease residual (Adams 2018 NEJM)"),
  "wilson_disease": dict(B=3, U=2, D=5,
     cite="~1/30,000, hepatic/neurologic, fatal untreated; chelation/zinc effective lifelong therapy (Roberts 2008)"),
  "gaucher_disease": dict(B=3, U=3, D=5,
     cite="commonest LSD; ERT/SRT effective for type-1 visceral disease, neuronopathic forms unserved (Grabowski 2008)"),
  "fabry_disease": dict(B=3, U=3, D=5,
     cite="X-linked LSD ~1/40k-117k, multi-organ; ERT + migalastat slow, residual cardiac/renal + antibodies (Germain 2016)"),
  "pompe_disease": dict(B=3, U=3, D=5,
     cite="~1/40,000, infantile fatal / late-onset progressive; ERT improves survival, residual muscle/respiratory (Kishnani 2007)"),
  "friedreich_ataxia": dict(B=3, U=5, D=4,
     cite="commonest inherited ataxia ~1/40k-50k, progressive + cardiomyopathy; omaveloxolone (FDA 2023) is DOWNSTREAM -- does NOT restore frataxin (Lynch 2023)"),
  "rett_syndrome": dict(B=3, U=5, D=4,
     cite="~1/10,000 females, severe neurodevelopmental regression; trofinetide (FDA 2023) acts DOWNSTREAM -- does NOT restore MeCP2 (Neul 2023)"),
  "x_linked_hypophosphataemia": dict(B=3, U=3, D=5,
     cite="commonest inherited rickets ~1/20,000, lifelong skeletal; burosumab anti-FGF23 (FDA 2018) targets the hormone axis (Carpenter 2018)"),
  "x_linked_adrenoleukodystrophy": dict(B=3, U=4, D=4,
     cite="~1/17,000, cerebral form rapidly fatal; eli-cel / HSCT only for early cerebral ALD, narrow window, genotype-phenotype unpredictable (Eichler 2017 NEJM)"),
  "metachromatic_leukodystrophy": dict(B=3, U=4, D=4,
     cite="~1/40,000-100,000, untreated late-infantile form uniformly progressive/fatal; atidarsagene autotemcel ex-vivo HSC gene therapy (FDA 2024 / EMA 2020) only PRE-/early-symptomatic and most cases present after onset (no routine newborn screen) -> large residual, the leukodystrophy/HSC-gene-therapy sibling of X-ALD (Fumagalli 2022 Lancet 399:372)"),
  "haemophilia_a": dict(B=3, U=3, D=5,
     cite="~1/5,000 males, bleeding + inhibitors; emicizumab works past inhibitors, gene-therapy durability open (Oldenburg 2017)"),
  "cystinuria": dict(B=3, U=4, D=5,
     cite="~1/7,000, commonest inherited cause of stones, recurrent painful stones; tiopronin (FDA 1988) + alkalinisation modest, recurrence frequent (Pak 1986)"),
  "hereditary_antithrombin_deficiency": dict(B=3, U=3, D=5,
     cite="~1/2,000-5,000, high venous-thromboembolism risk; antithrombin concentrate (FDA 2009) + factor-Xa inhibitors, lifelong management (Patnaik 2008)"),
  "alpha1_antitrypsin_deficiency": dict(B=3, U=4, D=4,
     cite="PiZZ ~1/2,000-5,000, lung + liver; A1AT augmentation is lung-only, hepatic Z-polymer axis unserved (Stoller 2005)"),
  "sod1_amyotrophic_lateral_sclerosis": dict(B=3, U=4, D=5,
     cite="SOD1 ~2% of ALS, fatal motor-neuron disease; tofersen (FDA 2023) slows SOD1-ALS, narrow genotype, not curative (Miller 2022 NEJM)"),
  "familial_mediterranean_fever": dict(B=3, U=3, D=5,
     cite="commonest monogenic autoinflammatory, high in Mediterranean populations, AA-amyloidosis risk; colchicine first-line, ~5-10% resistant (Ben-Chetrit 1998)"),
  # ---- rare / ultra-rare (individually low prevalence; high per-patient severity) ----
  "achondroplasia": dict(B=3, U=3, D=4,
     cite="commonest skeletal dysplasia ~1/25,000, disabling non-fatal; vosoritide (CNP analogue, approved 2021) modifies growth (Savarirayan 2020)"),
  "ornithine_transcarbamylase_deficiency": dict(B=2, U=4, D=5,
     cite="commonest urea-cycle disorder, X-linked hyperammonaemic crises; nitrogen scavengers manage, crisis risk persists, transplant curative (Batshaw 2014)"),
  "niemann_pick_disease_type_a_b": dict(B=2, U=4, D=5,
     cite="rare LSD, type-A neurodegenerative/fatal; olipudase alfa (FDA 2022) corrects visceral, CNS unserved (Wasserstein 2022)"),
  "niemann_pick_disease_type_c": dict(B=2, U=4, D=4,
     cite="rare, progressive neurodegeneration; miglustat (EMA) + arimoclomol (FDA 2024) slow, not curative (Patterson 2007)"),
  "menkes_disease": dict(B=2, U=5, D=3,
     cite="~1/100,000-300,000 males, often fatal in infancy; copper-histidine partial/timing-dependent, BBB-limited, NOT a conventional approval (Kaler 2008)"),
  "mecp2_duplication_syndrome": dict(B=2, U=5, D=2,
     cite="rare severe neurodevelopmental disorder; MECP2-lowering ASO INVESTIGATIONAL -- NO approved therapy (Sztainberg 2015)"),
  "primary_hyperoxaluria_type_1": dict(B=2, U=3, D=5,
     cite="rare, renal failure / systemic oxalosis; lumasiran RNAi substantially lowers oxalate (FDA 2020, Garrelfs 2021 NEJM)"),
  "hereditary_angioedema": dict(B=2, U=2, D=5,
     cite="~1/50,000, potentially fatal laryngeal attacks; lanadelumab/berotralstat effective prophylaxis (Banerji 2018)"),
  "acute_intermittent_porphyria": dict(B=2, U=3, D=5,
     cite="rare, acute neurovisceral attacks; givosiran (FDA 2019) upstream ALAS1 restraint + hemin (Balwani 2020 NEJM)"),
  "classical_homocystinuria": dict(B=2, U=4, D=5,
     cite="rare aminoacidopathy, thromboembolism + ectopia lentis; betaine (FDA 1996) + B6 (responsive genotypes), thrombotic risk persists (Mudd 1985)"),
  "hereditary_tyrosinaemia_type_1": dict(B=2, U=2, D=5,
     cite="rare, hepatic/renal + HCC risk; nitisinone + diet transformed outcomes since 1992, HCC risk reduced if early (Lindstedt 1992 Lancet)"),
  "haemophilia_b": dict(B=2, U=3, D=5,
     cite="~1/30,000 males (rarer than A); etranacogene dezaparvovec gene therapy (FDA 2022) + EHL factor IX (Pipe 2023)"),
  "tetrahydrobiopterin_deficiency": dict(B=2, U=4, D=5,
     cite="rare, hyperphenylalaninaemia + monoamine-neurotransmitter depletion; sapropterin + precursors partial, central restoration incomplete (Opladen 2020)"),
  "leber_congenital_amaurosis_2": dict(B=2, U=3, D=5,
     cite="ultra-rare inherited retinal dystrophy, congenital blindness; voretigene neparvovec (FDA 2017) improves vision, durability open (Russell 2017 Lancet)"),
  "cystinosis": dict(B=2, U=4, D=5,
     cite="ultra-rare ~1/100k-200k; cysteamine substrate-depleter slows but does not halt nephropathy, adherence hard (Gahl 2002)"),
  "alkaptonuria": dict(B=2, U=4, D=5,
     cite="ultra-rare; nitisinone (EMA 2020) slows ochronosis -- the same upstream HPD lever as tyrosinaemia (Ranganath 2020)"),
  "leptin_receptor_deficiency": dict(B=2, U=3, D=5,
     cite="ultra-rare; setmelanotide MC4R-agonist receptor-bypass (FDA 2020), partial (Clement 2020)"),
  "congenital_leptin_deficiency": dict(B=2, U=2, D=5,
     cite="ultra-rare; metreleptin near-curative for the hormone deficiency (Farooqi 1999 NEJM)"),
  "aadc_deficiency": dict(B=2, U=4, D=5,
     cite="ultra-rare neurodegeneration; eladocagene exuparvovec brain-delivered gene therapy (FDA 2024) -- gene-restore IS the lead (Hwu 2012)"),
  "familial_chylomicronaemia_syndrome": dict(B=2, U=4, D=5,
     cite="ultra-rare, pancreatitis risk; olezarsen first FCS-specific therapy (FDA 2024), pancreatitis risk persists (Stroes 2024)"),
  "sitosterolaemia": dict(B=2, U=3, D=5,
     cite="ultra-rare, premature ASCVD/xanthomas; ezetimibe blocks sterol absorption effectively (Salen 2004)"),
  "hypophosphatasia": dict(B=2, U=3, D=5,
     cite="rare, perinatal-lethal to mild; asfotase alfa enzyme replacement (FDA 2015) effective in severe forms (Whyte 2016)"),
  "lysosomal_acid_lipase_deficiency": dict(B=2, U=3, D=5,
     cite="rare, Wolman fatal-infantile / CESD; sebelipase alfa enzyme replacement (FDA 2015) (Burton 2015)"),
  "cerebrotendinous_xanthomatosis": dict(B=2, U=3, D=5,
     cite="ultra-rare; chenodiol (CDCA, FDA 2025) replaces the missing bile acid, early-treatment-dependent (Salen 2004 CTX)"),
  "cryopyrin_associated_periodic_syndrome": dict(B=2, U=2, D=5,
     cite="ultra-rare autoinflammatory; canakinumab IL-1beta blockade (FDA 2009) highly effective (Hoffman 2001)"),
  "deficiency_of_il1_receptor_antagonist": dict(B=2, U=2, D=5,
     cite="ultra-rare neonatal autoinflammatory; anakinra supplies the missing IL-1 antagonist, effective (Aksentijevich 2009 NEJM)"),
  "tuberous_sclerosis_complex": dict(B=3, U=3, D=5,
     cite="~1/6,000 births, multisystem hamartomas/epilepsy/SEGA/renal angiomyolipoma + neuropsychiatric burden; everolimus (mTOR inhibitor, FDA TSC indications) targets the pathway, not curative, TAND/cognitive residual (Krueger 2010 NEJM; Bissler 2013)"),
  "von_hippel_lindau_disease": dict(B=3, U=3, D=5,
     cite="~1/36,000, hereditary clear-cell RCC/CNS+retinal haemangioblastoma/phaeochromocytoma/pNET; belzutifan (HIF-2alpha inhibitor, FDA 2021) systemic option for previously surgery-only tumours, not curative, residual disease (Jonasch 2021 NEJM)"),
  # ---- v0.21.0 reads: lead lever is honestly NOT a clean approved switch-drug (clinical floor=cap=3) ----
  "x_linked_retinitis_pigmentosa": dict(B=3, U=5, D=3,
     cite="X-linked forms ~10-15% of retinitis pigmentosa (RP overall ~1/3,500-4,000), RPGR ~70% of XLRP, progressive male blindness from photoreceptor loss; botaretigene sparoparvovec (bota-vec) RPGR gene transfer still clinical -- Phase 3 LUMEOS missed its primary endpoint, no approved therapy (Cehajic-Kapetanovic 2020 Nat Med)"),
  "hereditary_haemorrhagic_telangiectasia": dict(B=3, U=5, D=3,
     cite="~1/5,000-8,000, recurrent epistaxis/GI bleeding/iron-deficiency anaemia + pulmonary/cerebral/hepatic AVMs; no approved targeted therapy -- only off-label downstream anti-angiogenics (bevacizumab; pomalidomide PATH-HHT) that do not restore the ENG/ACVRL1 brake (Faughnan 2020 guidelines; Al-Samkari 2024 NEJM PATH-HHT)"),
  # ---- v0.22.0 reads ----
  # clinical-not-approved gene-replacement lead (Huntington/XLRP honest pattern): clinical floor=cap=3
  "choroideremia": dict(B=2, U=5, D=3,
     cite="choroideremia ~1/50,000-100,000 males, progressive X-linked chorioretinal degeneration to central-vision loss; timrepigene emparvovec (AAV2-REP1 / BIIB111) gene transfer still clinical -- phase 3 STAR missed its primary AND key secondary endpoints, no approved therapy (Biogen STAR 2021 NCT03496012; MacLaren 2014 Lancet)"),
  # approved first-line lead but genotype-limited (diazoxide-unresponsive in biallelic-null): approved floor 4
  "congenital_hyperinsulinism": dict(B=3, U=3, D=4,
     cite="commonest cause of persistent neonatal hypoglycaemia ~1/28,000-50,000, hypoglycaemic brain-injury risk; diazoxide (K_ATP-channel opener) approved first-line but biallelic-null ABCC8/KCNJ11 forms are characteristically diazoxide-unresponsive and need near-total pancreatectomy (Bellanne-Chantelot 2010 J Med Genet; Hewat 2021 Eur J Endocrinol)"),
  # ---- v0.23.0 reads (channelopathy pair: SCN5A GOF / SCN1A LOF) ----
  # cardiac Na-channel GOF, gene-specific approved lead but genotype-limited + ICD mainstay: approved floor 4
  "long_qt_syndrome_3": dict(B=3, U=3, D=4,
     cite="LQTS ~1/2,000 (LQT3 ~10% -> ~1/20,000), torsades/sudden cardiac death often at rest; mexiletine (late-INa blocker) is gene-specific for LQT3 and an approved antiarrhythmic, but genotype-dependent (mexiletine-sensitive vs -insensitive SCN5A alleles) and an ICD remains the mainstay for high-risk -- beta-blockers are less effective and even pro-arrhythmic in LQT3 (Mazzanti 2016 JACC; Schwartz 2012 Circulation gene-specific therapy)"),
  # neuronal Na-channel LOF, no approved switch-drug (Huntington shape): investigational floor=cap=2, U=5
  "dravet_syndrome": dict(B=3, U=5, D=2,
     cite="Dravet ~1/15,700 births, treatment-resistant developmental/epileptic encephalopathy with the highest known SUDEP risk; approved fenfluramine/cannabidiol/stiripentol are downstream/palliative (no cure) and do NOT restore NaV1.1 -- the switch-level corrective (SCN1A/NaV1.1 upregulation, zorevunersen/STK-001) is investigational (Phase 3 EMPEROR) (Wu 2015 Pediatrics incidence; Han 2020 Sci Transl Med TANGO)"),
  # ---- v0.24.0 reads (4th ocular proteinopathy + first GPCR axis; both Huntington-pattern, no approved switch-drug) ----
  # ocular toxic-GOF proteinopathy, mutation-specific knockdown lead clinical-not-approved (Huntington/XLRP shape): clinical floor=cap=3, U=5
  "rho_autosomal_dominant_retinitis_pigmentosa": dict(B=2, U=5, D=3,
     cite="adRP ~1/12,000-25,000 (RP overall ~1/3,500-4,000; RHO ~20-30% of adRP), progressive autosomal-dominant photoreceptor loss to blindness; NO approved therapy -- mutation-specific toxic-allele knockdown (QR-1123 P23H ASO) reached Phase 1/2 and ablate-and-replace (EDIT-103) is preclinical, none approved (Dryja 1990 Nature; Cideciyan 2018 PNAS knockdown-and-replace)"),
  # GPCR (V2R) LOF, switch-level pharmacochaperone rescue investigational, downstream-only approved management (strongest-unmet shape): investigational floor=cap=2, U=5
  "nephrogenic_diabetes_insipidus_x_linked": dict(B=2, U=5, D=2,
     cite="X-linked NDI rare, dilute polyuria with recurrent hypernatraemic dehydration; NO approved targeted therapy -- thiazide/amiloride/NSAIDs are downstream-symptomatic, and switch-level V2R pharmacochaperone rescue is investigational (genotype-limited to misfolding mutants) (Bichet 2020 CJASN; Morello 2000 JCI; Bernier 2006 JASN SR49059)"),
  # ---- v0.25.0 reads (5th ocular read [structural, syndromic] + 2nd GPCR axis [AVPR2 GOF mirror]) ----
  # 5th ocular read: usherin structural-adhesion LOF, exon-13-skip ASO (ultevursen) lead clinical-not-approved (Huntington/XLRP/choroideremia shape): clinical floor=cap=3, U=5
  "usher_syndrome_type_2a": dict(B=2, U=5, D=3,
     cite="Usher type 2 ~1/12,000-30,000, commonest cause of combined congenital deafness + retinitis pigmentosa (deaf-blindness); NO approved targeted therapy -- exon-13-skip ASO ultevursen (QR-421a) completed Phase 1/2, now Phase 2b LUNA (Sepul Bio), and CRISPR EDIT-102 is preclinical, none approved (Eudy 1998 Science; Dulla 2021 Mol Ther Nucleic Acids)"),
  # 2nd GPCR axis: AVPR2 GOF mirror of NDI; tolvaptan an APPROVED on-target V2R inverse-agonist but genotype-limited (Arg137 vaptan-resistant): approved floor 4, U=4
  "nephrogenic_siad": dict(B=2, U=4, D=4,
     cite="NSIAD ultra-rare X-linked hyponatraemia with undetectable vasopressin; tolvaptan (approved vaptan) is the direct on-target V2R inverse-agonist and works in vaptan-SENSITIVE mutants (F229V/I130N), but the COMMONEST Arg137 (R137C/L) mutants are vaptan-RESISTANT -> high residual unmet need, alternative (ROCK-pathway) restraint investigational (Feldman 2005 NEJM; Tiulpakov 2016; Ranieri 2020 Cells)"),
  # ---- v0.26.0 reads (1st procoagulant-factor GOF [coagulation axis UP] + 2nd syndromic ciliopathy) ----
  # procoagulant accelerator GOF (factor V Leiden / APC resistance); the lead is an APPROVED but INDIRECT downstream anticoagulant (no F5-targeted agent exists): approved floor 4, U=3
  "factor_v_leiden": dict(B=3, U=3, D=4,
     cite="Factor V Leiden the commonest heritable thrombophilia (~5% of Europeans heterozygous, monogenic single-gene defect); the VTE manifestation is treated on-label by general anticoagulation (warfarin / DOACs, approved) but that is DOWNSTREAM and does NOT restore factor Va APC sensitivity -- NO F5-targeted therapy exists, so high residual switch-level unmet need (Bertina 1994 Nature 369:64; Kearon 2016 Chest)"),
  # 2nd syndromic ciliopathy (pairs USH2A); BBSome ciliary-trafficking LOF on the satiety axis; lead setmelanotide APPROVED for BBS obesity but INDIRECT (MC4R bypass) and covers only the obesity sub-phenotype: approved floor 4, U=4
  "bardet_biedl_syndrome": dict(B=3, U=4, D=4,
     cite="Bardet-Biedl syndrome ~1/140,000-160,000, multi-system ciliopathy (obesity, rod-cone dystrophy -> blindness, renal anomalies, polydactyly); setmelanotide (Imcivree, MC4R agonist) FDA-approved 2022 for BBS obesity/hyperphagia ONLY -- a downstream bypass of the BBSome defect, with the retinal degeneration and renal disease still without approved therapy -> high residual unmet need (Mykytyn 2002 Nat Genet 31:435; Haqq 2022 Lancet Diabetes Endocrinol 10:859)"),
  # ---- v0.27.0 reads (1st complement-cascade brake-LOF [complement axis UP] + 9th lysosomal read / new GAG substrate class) ----
  # complement factor H brake-LOF -> alternative-pathway over-activation; lead is APPROVED but INDIRECT (anti-C5 eculizumab/ravulizumab act DOWNSTREAM at C5, no CFH-restoring agent exists): approved floor 4, U=3
  "atypical_hemolytic_uremic_syndrome": dict(B=2, U=3, D=4,
     cite="aHUS ultra-rare (~0.5-2 per million/yr) but life-/kidney-threatening complement-mediated TMA; eculizumab/ravulizumab (anti-C5, approved for aHUS) are transformative but act DOWNSTREAM at C5 and do NOT restore factor-H regulation of the convertase -- lifelong, very costly, meningococcal-risk, relapse on withdrawal, and no CFH-restoring corrective exists -> real residual switch-level unmet need (Warwicker 1998 Kidney Int 53:836; Legendre 2013 NEJM 368:2169)"),
  # 9th lysosomal read, NEW glycosaminoglycan substrate class; alpha-L-iduronidase enzyme-LOF -> dermatan/heparan-sulfate storage; lead laronidase APPROVED + DIRECT ERT but does NOT cross the BBB (CNS unaddressed in Hurler): approved floor 4, D=5 per the lysosomal-ERT siblings (Gaucher/Fabry/Pompe)
  "mucopolysaccharidosis_type_i": dict(B=2, U=4, D=5,
     cite="MPS I (Hurler/Hurler-Scheie/Scheie) ~1/100,000; laronidase (Aldurazyme, ERT) FDA 2003 corrects somatic GAG storage on-label but does NOT cross the blood-brain barrier, so the neurocognitive decline of severe Hurler is unaddressed (HSCT, the early-Hurler standard, gives only partial CNS protection) -> high residual CNS unmet need (Scott 1991 PNAS 88:9695; Wraith 2004 J Pediatr 144:581; Aldenhoven 2015 Blood 125:2164)"),
  # ---- v0.32.0 reads (skeletal-muscle Na-channel / calcium-sensing GPCR / cofactor + transporter replace) ----
  # SCN4A channel-GOF (skeletal twin of LQT3); lead mexiletine APPROVED + disease-specific (Namuscla) but genotype-variable + pain-limited: approved floor 4
  "scn4a_skeletal_muscle_channelopathy": dict(B=2, U=3, D=4,
     cite="non-dystrophic myotonia / periodic paralysis ~1/100,000, significant lifelong stiffness/falls/paralytic attacks (rarely fatal); mexiletine (NaMuscla) EMA-approved 2018 is the first disease-specific antimyotonic and effective on stiffness but is genotype-variable and less effective on pain, and dichlorphenamide (Keveyis, FDA 2015) for the paralysis variants is INDIRECT -> moderate residual unmet need (Ptacek 1991 Cell 67:1021; Statland 2012 JAMA 308:1357)"),
  # CASR brake-LOF (1st calcium-sensing-GPCR axis); lead cinacalcet APPROVED for related HPT but OFF-LABEL here + genotype-dependent (true nulls need surgery): approved floor 4, U=3
  "neonatal_severe_hyperparathyroidism": dict(B=2, U=3, D=4,
     cite="NSHPT ultra-rare but life-threatening neonatal hypercalcaemia (FHH1 ~1/78,000 but usually benign); cinacalcet (calcimimetic, approved for 2-deg HPT/parathyroid carcinoma/PHPT) used OFF-LABEL is effective first-line in many NSHPT/symptomatic-FHH cases but is GENOTYPE-DEPENDENT -- true-null alleles are unresponsive and still require parathyroidectomy -> real residual unmet need (Pollak 1993 Cell 75:1297; Gannon 2014 JCEM 99:7)"),
  # BTD enzyme-LOF cofactor-recycling; lead oral biotin APPROVED, cheap, dramatically effective, newborn-screened: approved cap 5, U low
  "biotinidase_deficiency": dict(B=2, U=2, D=5,
     cite="biotinidase deficiency ~1/60,000 (profound + partial), severe-if-untreated (seizures, hearing loss, optic atrophy) but among the most TREATABLE inborn errors: lifelong inexpensive oral biotin, newborn-screened, normal course if pre-symptomatic -> low residual unmet need (chief gap = irreversible damage if treatment is late) (Wolf 1983 J Pediatr 103:233; Wolf 2010 GeneReviews)"),
  # SLC22A5 transporter-LOF; lead levocarnitine APPROVED, lifesaving, reverses cardiomyopathy if early: approved cap 5, U low-moderate
  "primary_carnitine_deficiency": dict(B=2, U=2, D=5,
     cite="primary carnitine deficiency ~1/40,000-120,000, can cause sudden cardiac death untreated but largely REVERSIBLE: high-dose oral levocarnitine (Carnitor, FDA-approved for primary/secondary carnitine deficiency) reverses cardiomyopathy/myopathy/hypoglycaemia when started early, lifelong dependence -> low-moderate residual unmet need (late-presenting irreversible cases) (Nezu 1999 Nat Genet 21:91; Magoulas 2012 Orphanet J Rare Dis 7:68)"),
}


def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["D"]*t["D"], 4)


def load_resolved():
    reg = json.load(open(os.path.join(DISEASES, "_registry.json"), encoding="utf-8"))
    out = {}
    for slug in reg["diseases"]:
        a = json.load(open(os.path.join(DISEASES, slug, "analysis.json"), encoding="utf-8"))
        if a.get("status") != "RESOLVED":
            continue
        ps = a["emergence"]["primary_switch"]["gene"]
        pg = next(g for g in a["emergence"]["per_gene"] if g["gene"] == ps)
        lead = a["treatment_A_switch"]["lead_corrective_lever"]
        out[slug] = {
            "disease": a["disease"],
            "primary_gene": ps,
            "gamma": float(pg["gamma"]),
            "barrier": float(pg["barrier"]),
            "lever": lead["lever"],
            "lead_target": lead["target_gene"],
            "lead_status": lead["status"],
            "indirect": lead["target_gene"] != ps,
        }
    return out


def build():
    resolved = load_resolved()

    # fail-closed: every resolved disease MUST carry a cited tier, and no tier may reference a
    # disease that isn't resolved (keeps the editorial layer honest against the frozen artifacts).
    missing = sorted(set(resolved) - set(DISEASE_TIERS))
    extra = sorted(set(DISEASE_TIERS) - set(resolved))
    if missing or extra:
        raise SystemExit(f"tier/disease mismatch  missing_tiers={missing}  stale_tiers={extra}")

    rows, d_floor_violations = [], []
    for slug, r in resolved.items():
        t = DISEASE_TIERS[slug]
        # D consistency floor/cap from the frozen lead-lever status
        floor = STATUS_D_FLOOR.get(r["lead_status"], 1)
        cap = STATUS_D_CAP.get(r["lead_status"], 5)
        if not (floor <= t["D"] <= cap):
            d_floor_violations.append({"slug": slug, "D": t["D"], "status": r["lead_status"],
                                        "allowed": [floor, cap]})
        rows.append({
            "slug": slug,
            "disease": r["disease"],
            "primary_gene": r["primary_gene"],
            "lever": r["lever"],
            "lever_class": "indirect (downstream/upstream)" if r["indirect"] else "gene-restore",
            "lead_target": r["lead_target"],
            "lead_status": r["lead_status"],
            "B_burden": t["B"], "U_unmet": t["U"], "D_druggability": t["D"],
            "priority_score": score(t),
            # the read's place in the map, STRUCTURAL context ONLY (NOT in the score -- firewall):
            "map_place": {"primary_gamma": r["gamma"], "primary_barrier": r["barrier"]},
            "tier_basis_cited": t["cite"],
            "grade": "[F] from cited B/U/D tiers + declared weights (Layer-2 ranking, not a [V] engine output)",
        })

    if d_floor_violations:
        raise SystemExit(f"D-consistency-floor violated (D disagrees with frozen lead status): "
                         f"{d_floor_violations}")

    # deterministic sort: score desc, tie-break by barrier depth desc (structural), then slug.
    ranked = sorted(rows, key=lambda r: (-r["priority_score"], -r["map_place"]["primary_barrier"],
                                          r["slug"]))
    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    # informational: how the top quartile splits across lever class + simple organ clusters
    n = len(ranked)
    topq = {r["slug"] for r in ranked[:max(1, n // 4)]}
    by_class = {"gene-restore": sorted(r["slug"] for r in ranked if r["lever_class"].startswith("gene")),
                "indirect": sorted(r["slug"] for r in ranked if r["lever_class"].startswith("indirect"))}

    return {
        "title": "Burden-weighted prioritisation of RESOLVED DISEASES/READS (not drugs)",
        "inherited_from": "analgesic_threshold_logic_v2_0 M10 (build_prioritisation.py); DOI 10.5281/zenodo.20733420",
        "method": "score = w_B*B + w_U*U + w_D*D over cited 1..5 tiers; deterministic sort by score, "
                  "tie-break by primary-switch barrier depth then slug.",
        "weights_declared": WEIGHTS,
        "weights_sum": round(sum(WEIGHTS.values()), 6),
        "label": "This is a prioritisation of DISEASES/READS, NOT a ranking of drugs, doses, or efficacy.",
        "firewall_note": ("primary-switch gamma/barrier is shown as the structural read's place in the map "
                          "and is NOT folded into the clinical priority score (it is a promoter-stiffness "
                          "read, not a clinical magnitude) -- inherited verbatim from analgesic M10."),
        "d_consistency_rule": ("D is bounded by the lead lever's frozen `status` "
                               f"(floor/cap {STATUS_D_FLOOR}/{STATUS_D_CAP}); the build FAILS CLOSED if any "
                               "editorial D disagrees with the shipped evidence."),
        "n_ranked": n,
        "ranking": ranked,
        "top_quartile_slugs": sorted(topq),
        "by_lever_class": by_class,
    }


if __name__ == "__main__":
    out = build()
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "repro", "modules", "expected", "disease_priority_ranking.json")
        json.dump(out, open(p, "w"), indent=1)
        print(f"wrote {os.path.relpath(p, ROOT)}")
    print("Disease burden-weighted prioritisation (DISEASES, not drugs)  [inherited: analgesic M10]")
    print(f"  weights (declared): {out['weights_declared']}  sum={out['weights_sum']}  n={out['n_ranked']}")
    print(f"  {'#':>2} {'disease slug':38} {'lever':10} {'class':10} B U D {'score':>5}  {'γ':>6} {'barr':>6}")
    for r in out["ranking"]:
        cls = "indir" if r["lever_class"].startswith("indirect") else "gene"
        print(f"  {r['rank']:>2} {r['slug']:38} {r['lever']:10} {cls:10} "
              f"{r['B_burden']} {r['U_unmet']} {r['D_druggability']} {r['priority_score']:5.2f}  "
              f"{r['map_place']['primary_gamma']:6.3f} {r['map_place']['primary_barrier']:6.3f}")
    print(f"  top quartile: {out['top_quartile_slugs']}")
