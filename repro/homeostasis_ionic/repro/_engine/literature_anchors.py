#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
literature_anchors.py  --  CITED literature values + the explicit simulation<->literature cross-checks
this volume makes (VP-SPEC C1: external theory/observation is RESPECTED as a cited anchor, not re-derived;
the loop MECHANISM is what is reproduced [V]).

Each anchor carries: the cited value, the source, the grade, and -- where the engine touches it -- the
simulated quantity it is checked against. This is the "connect existing literature + review interactions"
layer: it makes every [L] anchor auditable and every [V] claim falsifiable against the literature.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import importlib
loops = importlib.import_module("vp_loops")

# ---- cited setpoints / curves / thresholds (the [L] anchors) ----
ANCHORS = [
 {"id":"A-CA",  "quantity":"serum calcium setpoint", "value":"ionized ~1.1-1.3 mM (total ~2.2-2.6 mM)",
  "grade":"[L]", "source":"Brown EM 1991 Physiol Rev; CaSR setpoint physiology",
  "checked_against":"RI1 returns serum Ca to setpoint after load/deficit"},
 {"id":"A-PTH", "quantity":"PTH-Ca relation", "value":"four-parameter inverse sigmoid; set-point = Ca at half-max PTH; Hill ~3",
  "grade":"[L]", "source":"Brown EM 1983 JCEM (four-parameter model)",
  "checked_against":"RI1 PTH suppressed by Ca load, raised by deficit (pth_curve)"},
 {"id":"A-PH",  "quantity":"blood pH setpoint", "value":"7.40 = 6.1 + log10(24/(0.03*40))",
  "grade":"[L]", "source":"Henderson-Hasselbalch; standard acid-base physiology",
  "checked_against":"RI2 pH returns to 7.40 after a metabolic acid load"},
 {"id":"A-WIN", "quantity":"respiratory compensation (metabolic acidosis)", "value":"expected pCO2 = 1.5*HCO3 + 8 (Winters); slope ~1.2-1.5",
  "grade":"[L]", "source":"Albert/Winters 1967 Ann Intern Med",
  "checked_against":"RI2 fast-arm compensation slope dPCO2/dHCO3 (~1.1, within band)"},
 {"id":"A-NAK", "quantity":"serum Na / K setpoints", "value":"Na ~140 mM ; K ~4.2 mM",
  "grade":"[L]", "source":"standard electrolyte reference ranges",
  "checked_against":"RI4 Na/K loads corrected by renal handling"},
 {"id":"A-CAP", "quantity":"Ca x PO4 precipitation ceiling", "value":"product held below precipitation (calcification/stone risk)",
  "grade":"[L]", "source":"calcium-phosphate solubility; CKD-MBD literature",
  "checked_against":"RI5 keeps Ca*PO4 below the precipitation threshold via FGF23"},
 {"id":"A-TMP", "quantity":"renal phosphate threshold TmP/GFR", "value":"adult reference 0.80-1.35 mmol/L; Walton-Bijvoet nomogram (TRP<=0.86 linear; >0.86 corrected)",
  "grade":"[L]", "source":"Walton & Bijvoet 1975 Lancet (nomogram); Payne 1998 Ann Clin Biochem (reference interval)",
  "checked_against":"renal_phosphate: normal TmP/GFR in reference; FGF23/PTH lower it (XLH < normal < hypoPTH)"},
 {"id":"A-DUAL", "quantity":"dual sclerostin + DKK1 inhibition", "value":"SOST inhibition raises DKK1 (beta-catenin target, negative feedback); dual block synergistic in rodents & non-human primates",
  "grade":"[L]", "source":"Florio et al. 2016 Nat Commun 7:11505",
  "checked_against":"frontier_quant H-DUAL: integrated anabolic window dual > single > untreated (single window closes)"},
 {"id":"A-OTOC", "quantity":"otoconial calcite saturation (BPPV)", "value":"otoconia = calcite; stability ~ Omega=[Ca][CO3]/Ksp; acidosis & low-Ca lower Omega -> dissolution; endolymph Ca 250-280 uM, pH 7.6-7.7",
  "grade":"[L]", "source":"Frontiers in Neurology 2025 (endolymph Ca/pH Omega BPPV model); Walther et al. PLOS One 2014 (calcite-otoconia dissolution)",
  "checked_against":"frontier_quant H-OTOC: acidosis & hypocalcemia drop Omega below 1 (dissolution-prone)"},
 {"id":"A-RESET", "quantity":"allosteric set-point reset of an ionic sensor (CaSR proof-of-concept)", "value":"a negative allosteric modulator (calcilytic) relocates the CaSR set-point; encaleret met all primary & key-secondary endpoints in Phase-3 CALIBRATE (ADH1)",
  "grade":"[L]", "source":"BridgeBio 2025 (CALIBRATE Phase 3, NCT05680818, encaleret in ADH1); cinacalcet (calcimimetic) resets CaSR down in hyperparathyroidism",
  "checked_against":"frontier_quant H-RESET: defended attractor = comparator set-point for every Hill slope -> reset is the unique durable fix across the sensor family"},
 {"id":"A-ARM", "quantity":"acid-base arm failure & its current therapy (distal RTA)", "value":"dRTA = failure of the renal acid arm (a-intercalated-cell H+-ATPase / AE1); standard of care is lifelong alkali (K-citrate/bicarbonate; ADV7103/Sibnayal, EMA-approved) -- replaces base, does not restore the transporter",
  "grade":"[L]", "source":"GeneReviews Hereditary Distal RTA (NCBI NBK547595); Lopez-Garcia/Boyer et al. ADV7103 trials (Pediatr Nephrol 2021; Pediatr Drugs 2024)",
  "checked_against":"frontier_quant H-ARM: restoring k (the arm) tightens variance & rejects fresh loads by k_high/k_low; buffering cancels the mean only"},
 {"id":"A-OU",  "quantity":"OU control law", "value":"Var = sigma^2/(2k) ; step error = load/k ; tau = 1/k",
  "grade":"[F]", "source":"Ornstein-Uhlenbeck / linear control (exact)",
  "checked_against":"ou_law sweep: Var*2k/sigma^2 ~ 1 and error*k ~ 1"},
 {"id":"A-OSMO", "quantity":"osmotic strategy across the animal kingdom (who regulates ions vs conforms)", "value":"most marine invertebrates osmoCONFORM (body fluid ~ seawater); marine elasmobranchs osmoconform via urea+TMAO yet iono-regulate Na/Cl; teleosts and tetrapods osmoREGULATE (gill ionocytes / renal loops hold a defended internal milieu against the environment)",
  "grade":"[L]", "source":"Schmidt-Nielsen 1997 Animal Physiology; Willmer/Stone/Johnston 2005; Evans/Piermarini/Choe 2005 (Physiol Rev, gill); Ballantyne 1997 (elasmobranch urea)",
  "checked_against":"comparative_ionoregulation: conformer internal state tracks the salinity load (offset=load/k large), regulator defends it (offset small); excursion monotone in loop gain k; ratio == k_reg/k_conf"},
 {"id":"A-MG", "quantity":"serum magnesium setpoint & its failure modes", "value":"serum Mg ~0.85 mM (defended); hypomagnesemia from absorption/reabsorption-arm failure (TRPM6 loss-of-fn = HSH; Gitelman SLC12A3 renal Mg/Ca wasting); hypermagnesemia from excretion-arm failure (renal insufficiency + Mg load)",
  "grade":"[L]", "source":"Schlingmann et al. 2002 Nat Genet 31:166 (TRPM6, HSH); Gitelman syndrome (SLC12A3); de Baaij/Hoenderop/Bindels 2015 Physiol Rev (magnesium in health and disease)",
  "checked_against":"tier2_ion_diseases G2: a defended-Mg loop with a failed arm (low k) leaves a large offset under the same drive (err=load/k), hypo for an Mg-loss drive and hyper for an Mg-intake drive, monotone in 1/k, ratio == gain ratio, variance blow-up"},
 {"id":"A-CKD", "quantity":"CKD-MBD / secondary hyperparathyroidism cascade", "value":"falling GFR -> phosphate retention, 1,25-dihydroxyvitamin-D deficiency (renal 1a-hydroxylase), hypocalcemia tendency, and secondary hyperparathyroidism; the Ca x PO4 product drives vascular calcification",
  "grade":"[L]", "source":"KDIGO 2017 Clinical Practice Guideline Update for CKD-MBD (Kidney Int Suppl)",
  "checked_against":"tier2_ion_diseases G3: stepping the renal integrator gain down drives PO4 up (err=load/k), 1,25-vitD down, Ca down and PTH up (secondary HPT) all monotone, with the Ca x PO4 product near-normal early and climbing to the precipitation ceiling in advanced CKD"},
 {"id":"A-PTHRP", "quantity":"humoral hypercalcemia of malignancy (PTHrP)", "value":"tumor-secreted PTHrP acts at the PTH1 receptor like PTH but is NOT under calcium-sensing-receptor feedback -> hypercalcemia with APPROPRIATELY SUPPRESSED endogenous PTH (the fingerprint that distinguishes it from primary hyperparathyroidism)",
  "grade":"[L]", "source":"Stewart AF 2005 N Engl J Med 352:373 (Hypercalcemia associated with cancer); PTHrP humoral hypercalcemia standard literature",
  "checked_against":"tier2_ion_diseases G4: an exogenous unsuppressible PTHrP drive relocates the defended calcium UP (monotone) -- the inverse of the T1 allosteric set-point reset -- while the endogenous PTH comparator output is suppressed below baseline despite the high calcium"},
 {"id":"A-GHK", "quantity":"constant-field ion flux (molecular transport law)", "value":"GHK flux J = P z F u (Ci - Co e^-u)/(1 - e^-u), u = zFVm/RT; reverses exactly at the Nernst potential and rectifies when [ion] differs across the membrane",
  "grade":"[F]", "source":"Goldman DE 1943 J Gen Physiol 27:37; Hodgkin & Katz 1949 J Physiol 108:37 (constant-field theory)",
  "checked_against":"transport_dynamics G5: ghk_flux reverses at Nernst (J=0), changes sign across reversal, and rectifies -- exact physics [F], reproduced in sim [V]"},
 {"id":"A-TRPV", "quantity":"vitamin-D-gated epithelial Ca channels (TRPV5/TRPV6)", "value":"1,25-dihydroxyvitamin-D (VDR) transcriptionally up-regulates the apical Ca channels TRPV5 (kidney distal tubule) and TRPV6 (gut) plus calbindin -> raises transcellular Ca reabsorption/absorption; their loss-of-function gives renal Ca wasting",
  "grade":"[L]", "source":"Hoenderop/Nijenhuis/Bindels 2005 Physiol Rev 85:373 (epithelial Ca channels); den Dekker et al. 2003 Cell Calcium 33:497 (vitamin-D regulation of TRPV5/6)",
  "checked_against":"transport_dynamics G5: a vitamin-D (Hill) signal raises channel open-probability and the GHK Ca reabsorptive flux monotonically [L]/[V]"},
 {"id":"A-ENAC", "quantity":"epithelial Na channel (ENaC / SCNN1A) loss-of-function", "value":"loss-of-function in the epithelial Na channel subunits (SCNN1A/B/G) causes systemic pseudohypoaldosteronism type 1 (PHA1): renal salt wasting, hyperkalemia and metabolic acidosis despite high aldosterone -- a failed Na-reabsorption arm at the membrane",
  "grade":"[L]", "source":"Chang et al. 1996 Nat Genet 12:248 (SCNN1A/B/G mutations, PHA1); Pseudohypoaldosteronism type 1 clinical literature",
  "checked_against":"transport_dynamics G5: a loss-of-function transporter (low channel number / conductance) drops the membrane loop gain k, enlarges the steady offset (err=load/k) and blows up the variance -- the loop-gain-drop failure mode at the membrane"},
 {"id":"A-HATPASE", "quantity":"distal-tubule proton pump (H+-ATPase / ATP6V) loss-of-function", "value":"loss-of-function in the a-intercalated-cell vacuolar H+-ATPase subunits (ATP6V0A4 / ATP6V1B1) causes autosomal-recessive distal renal tubular acidosis (dRTA): failure of the renal acid-secretion arm -> hyperchloremic metabolic acidosis, often with sensorineural deafness",
  "grade":"[L]", "source":"Karet et al. 1999 Nat Genet 21:84 (ATP6V1B1) and 1999 PNAS (ATP6V0A4); GeneReviews Hereditary Distal RTA (NCBI NBK547595)",
  "checked_against":"transport_dynamics G5: same membrane loop-gain-drop mechanism as A-ENAC -- a failed proton-pump arm lowers k so the defended pH carries a large offset (cf. A-ARM, where restoring k beats buffering)"},
 {"id":"A-ATP1A1", "quantity":"Na+,K+-ATPase alpha-1 (ATP1A1) as the osmoregulatory master gene", "value":"the Na+/K+-ATPase alpha-1 subunit is the universal animal ion pump that sets the trans-membrane Na/K gradient powering all secondary ion transport; it is the natural master-gene candidate for the osmotic-strategy axis (conform -> regulate)",
  "grade":"[V]", "source":"Kaplan JH 2002 Annu Rev Biochem 71:511 (Na,K-ATPase); Lingrel JB 2010 Annu Rev Physiol 72:395; NCBI Gene records (ATP1A1 orthologs, GeneID 476 human)",
  "checked_against":"comparative_gamma G6: ATP1A1 promoter gamma measured across 6 species (NCBI, SantaLucia 1998); human anchor reproduced and elasmobranch replicate near-identical [V], BUT gamma is non-monotone in the loop gain k and tracks promoter GC (rho~1) -- HONEST NEGATIVE: per-species gamma does not ground the comparative absolute k, which stays [O]"},
 {"id":"A-3LEVER", "quantity":"the three-lever therapeutic principle (inherited cross-volume technology)", "value":"a threshold-crossing / defended-setpoint has exactly three independent handles: L1 lower the DRIVE (load), L2 raise the loop GAIN / firing barrier (k), L3 reset the SET-POINT (x*). The OU asymmetry error=load/k vs variance=sigma^2/2k makes only L2 tighten the variance, so the corrupted parameter selects the primary lever",
  "grade":"[L]/[V]", "source":"Analgesic Threshold Logic (non-opioid), Young Jae Lee, concept DOI 10.5281/zenodo.20733420 (27 non-opioid targets sorted onto L1/L2/L3); the asymmetry is reproduced here from this volume's own OU law",
  "checked_against":"three_lever lever_asymmetry: L1 lowers the mean only (variance unchanged), L2 lowers mean AND variance (unique), L3 relocates the defended target durably; gain_lever_dna_ceiling: the L2 ceiling per arm = node barrier b=gamma^2/4 with gamma MEASURED"},
 {"id":"A-ANALGESIC", "quantity":"non-opioid analgesic drug classes mapped to the three levers (the source exemplars)", "value":"L1 (lower nociceptive drive): NSAID/COX inhibitors, anti-NGF. L2 (raise the firing barrier): Nav1.7/1.8 blockers (suzetrigine-class), Kv7 openers, local anaesthetics. L3 (reset central gain/set-point): gabapentinoids (Cav alpha2-delta), SNRIs / descending modulation, NMDA antagonists, alpha2-agonists",
  "grade":"[L]", "source":"Analgesic Threshold Logic three-lever organizing principle (concept DOI 10.5281/zenodo.20733420); FDA 2025 approval of suzetrigine (Nav1.8 inhibitor) as a non-opioid L2 exemplar; standard multimodal-analgesia pharmacology",
  "checked_against":"three_lever analgesic_lever_map: each analgesic lever placed next to its ionic-homeostasis twin (same R19/OU kernel, different defended variable) -- the technology transfer is explicit"},
]

# ---- molecular-interaction map (the "review interactions" layer) ----
INTERACTIONS = [
 "CaSR(-)PTH: rising Ca activates CaSR -> suppresses PTH (the comparator->effector inversion).",
 "PTH(+)bone resorption, PTH(+)renal Ca reabsorption, PTH(+)1a-hydroxylase -> 1,25-vitD (fast+slow arms).",
 "1,25-vitD(+)gut Ca absorption via TRPV6 ; (+)renal Ca via TRPV5 (the slow VDR arm effectors).",
 "PTH(+)phosphaturia and FGF23(+)phosphaturia + FGF23(-)1,25-vitD (PO4 lowering arm; Ca-PO4 cross-talk).",
 "kidney(SIX2): renal HCO3 regeneration (slow acid-base arm) AND renal Ca/PO4 handling (shared integrator).",
 "respiratory CO2 (cardioresp seam): fast acid-base arm; renal HCO3 the slow arm (two-timescale buffer).",
 "estrogen(-)bone resorption: withdrawal raises reservoir withdrawal -> post-menopausal depletion (RI3).",
 "sclerostin(-)bone formation (mechanically gated): loading lowers sclerostin -> refill (anabolic input).",
 "Na<->volume<->pressure (hemodynamic seam): pressure natriuresis closes the Na loop (cited, not re-emerged).",
 "TRPM6/7(+)Mg absorption (gut) + renal distal reabsorption: arm failure -> hypomagnesemia (HSH/Gitelman); the Mg loop is the third defended-ion attractor.",
 "renal 1a-hydroxylase(+)1,25-vitD: CKD lowers it -> vitD deficit -> low gut Ca -> CaSR raises PTH = secondary hyperparathyroidism; phosphate retention raises the Ca x PO4 product.",
 "PTHrP(+)PTH1R (tumor-autonomous, NOT CaSR-suppressed): drives the defended Ca UP with endogenous PTH suppressed = humoral hypercalcemia of malignancy (the inverse of an allosteric set-point reset).",
 "GHK(constant-field): the membrane flux per channel; its slope at the setpoint k=-dJ/dC IS the loop gain the volume uses -- the molecular 'how' beneath every arm above.",
 "1,25-vitD(+)TRPV5/6 open-probability (Hill gating): the slow VDR arm's molecular effector; channel number / gating steepness set the membrane loop gain (transport_dynamics G5).",
 "ENaC/SCNN1A(+)Na reabsorption & H+-ATPase/ATP6V(+)acid secretion: loss-of-function drops the membrane k -> PHA1 / distal RTA = the loop-gain-drop failure mode at the membrane (a transporter, not a sensor, fails).",
 "Na+,K+-ATPase/ATP1A1: the universal pump powering all secondary ion transport; its promoter gamma was MEASURED across the osmotic-strategy axis but does NOT ground the comparative loop gain (tracks GC; honest negative, comparative_gamma G6).",
 "THREE LEVERS (L1 load / L2 gain / L3 setpoint): the OU asymmetry error=load/k vs variance=sigma^2/2k means only L2 (raising k) tightens lability; the corrupted parameter selects the primary lever for every owned disease (three_lever; disease_remediation) -- the technology inherited from the non-opioid analgesic volume (concept DOI 10.5281/zenodo.20733420).",
]

def cross_checks():
    """Pull the engine's simulated values next to their cited anchors -> an auditable comparison table."""
    L = loops.run_loops()
    return [
      {"anchor":"A-CA/A-PTH", "cited":"Ca setpoint defended; PTH inverse-sigmoid",
       "simulated":{"ca_final":L["RI1_calcium"]["ca_final"],
                    "pth_suppressed_by_load":L["RI1_calcium"]["pth_suppressed_by_load"],
                    "pth_raised_by_deficit":L["RI1_calcium"]["pth_raised_by_deficit"]},
       "verdict":"consistent" if L["RI1_calcium"]["returns_to_setpoint"] else "FAIL"},
      {"anchor":"A-PH/A-WIN", "cited":"pH 7.40 ; Winters slope ~1.2-1.5",
       "simulated":{"pH_final":L["RI2_acidbase"]["pH_final"],
                    "winters_slope":L["RI2_acidbase"]["respiratory_compensation_slope_dPCO2_dHCO3"]},
       "verdict":"consistent" if (L["RI2_acidbase"]["two_timescale_restored"] and L["RI2_acidbase"]["winters_slope_match"]) else "FAIL"},
      {"anchor":"A-CAP", "cited":"Ca x PO4 below precipitation",
       "simulated":{"ca_po4_product_max":L["RI5_phosphate"]["ca_po4_product_max"]},
       "verdict":"consistent" if L["RI5_phosphate"]["ca_po4_below_precipitation"] else "FAIL"},
      {"anchor":"A-OU", "cited":"Var=sigma^2/2k ; err=load/k",
       "simulated":{"var_times_2k_over_sigma2":[s["var_times_2k_over_sigma2"] for s in L["ou_law"]["sweep"]],
                    "error_times_k":[s["error_times_k"] for s in L["ou_law"]["sweep"]]},
       "verdict":"consistent" if (L["ou_law"]["variance_law_Var_eq_sigma2_over_2k"] and L["ou_law"]["rejection_law_err_eq_load_over_k"]) else "FAIL"},
    ]

def status():
    cc=cross_checks()
    return dict(anchors=ANCHORS, interactions=INTERACTIONS, cross_checks=cc,
                all_cross_checks_consistent=all(c["verdict"]=="consistent" for c in cc),
                note="external theory/observation is a cited anchor [L]/[F]; the loop mechanism is reproduced [V].")

if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=1))
