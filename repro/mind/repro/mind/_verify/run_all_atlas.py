#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all_atlas.py -- transdiagnostic fault-axis atlas gate suite
================================================================
Runs the atlas disorder modules that re-cut conditions by MECHANISM (the T/O/W axes
+ over-sync pole) rather than by symptom checklist. Each module is RE-RUN as a fresh
subprocess so it rewrites its own results.json and expected_*.json; the gate then takes
the sha256 of the WRITTEN file and checks it against the FROZEN constant held *here*
(the module rewrites its own expected_*.json each run, so the orchestrator's own frozen
constants are the true regression guard). It also confirms the engine file is byte-
unchanged (e61083ae...), the live emergence tree is frozen (0fbf4988...), and every
module's honesty ledger holds (efficacy=0, no consciousness claim, no tuned constants,
and either no_cure_claimed=1 or hard_problem_open=1). Writes gate.json. Exit 0 iff every
module reproduces bit-for-bit AND the engine is unchanged AND the discipline holds.

Atlas roadmap coverage (RESEARCH_ROADMAP_post_autism_adhd.md):
  T1a Schizophrenia -- the T/O/W+ discriminant   (over-ignition mirror of autism-T)
      + symptom-domain axis map (positive=T / negative=O / cognitive=W)
  T2a Epilepsy      -- the over-synchronisation pole (R above the over-sync threshold)
  E0  Plasticity    -- the consolidation layer: a phase-correlation Hebbian update on the
      frozen ephaptic W. Makes after-effects representable, RESOLVES the open continuous-vs-
      periodic dosing question (spaced > massed for retained structure), and builds the
      reversible->chronified switch every temporal disorder (depression, bipolar, addiction)
      depends on. eta=0 reproduces the frozen M9 anchor bit-for-bit (pure add-on).
  T1b Depression    -- the first TEMPORAL disorder, built ON TOP of E0 (imports PlasticConnectome).
      Major depression as the chronification of a low-coordination operating point: a sustained
      HPA-driven withdrawal lowers R below health (acute, reversible); with plasticity the
      excursion writes a retained structural trace (chronification); antidepressant delayed onset
      = a consolidation timescale; treatment resistance = the depth of the chronified trace.
      No new tuned constant; eta=0/stress=0 reproduces the frozen M9 anchor bit-for-bit.
  E2  State-switching -- the R19 bistable cell used OVER TIME (the switching LAYER). Hysteresis
      (a finite loop width = 2*spinodal), a transition latency that diverges at the fold (critical
      slowing -- this CLOSES the §25 epilepsy ictal time-course that was OWED to E2), and a
      barrier handle that sets the switching threshold. g=1.0 universal scale; fold=spinodal from
      the engine; const-drive integration reproduces E.settle bit-for-bit. Pure add-on.
  T2b Bipolar       -- two operating poles on ONE valence axis (mania above health, depression
      below), built ON TOP of E2 + E0. An episode is a bistable transition (E2 hysteresis+latency);
      kindling is the E0 retained trace accumulating across alternating episodes (each switch easier);
      a mood stabiliser is the barrier-raising sign (raises the flip threshold). No new tuned constant;
      eta=0 reproduces the frozen M9 anchor bit-for-bit.
  T2b-L Bipolar levers -- the threshold-shift INTERVENTION logic inherited from analgesic_threshold_
      logic v2.0 (Zenodo 10.5281/zenodo.20733420). B4 proved the stabiliser sign is "raise the barrier"
      but treated the stabiliser as ONE abstract operator; this module decomposes that operator into a
      DNA-grounded three-lever target map: L1 reduce inward (excitatory) current, L2 increase outward
      (K+) current, L3 remove the up-stream circadian/HPA sensitising drive. gamma = -mean(NN stacking
      dG, SantaLucia 1998) is read from each gene's own promoter window (TSS-2000..+500) on the SAME
      R19 substrate (E.spinodal/E.barrier, READ-ONLY) -- 16 bipolar excitability genes (CACNA1C, ANK3,
      GSK3B, the KCNQ/KCNB outward set, the circadian/HPA set). A fail-closed L3-honesty gate keeps
      every L3 mechanism link graded [O] cited biology; a fail-closed forbidden-claim scanner forbids
      dose/efficacy/safety/synthesis; a burden-weighted prioritisation ranks TARGETS (never drugs or
      doses) with gamma carried alongside but NEVER folded into the score. FIREWALL: the promoter
      |h_sp| is the gene's own switch stiffness, never equated with the sec.29 network mood-switch
      barrier g, nor with channel voltage / potency / dose / clinical effect. efficacy=0; no new tuned
      constant; engine READ-ONLY.
  T2a-L Epilepsy levers -- the SAME threshold-shift intervention logic applied to the over-sync pole.
      §25 (T2a) proved seizures are the network crossing the over-synchronisation threshold on the global
      order parameter R, but the corrective push ("raise the over-sync threshold") was ONE abstract
      operator; this module decomposes it into a DNA-grounded three-lever target map on the SAME R19
      substrate: L1 reduce inward Na/Ca/NMDA current, L2 increase outward K+ current (dominant here --
      the KCNQ2/3 M-current is the textbook retigabine axis), L3 remove the up-stream mTOR drive ([O],
      cited). 16 epilepsy excitability genes (the SCN/CACNA inward set, the KCNQ/KCNB/KCNA/KCNT outward
      set, the GABA-A inhibitory pair, the GATOR1/TSC mTOR set); gamma = -mean(NN stacking dG, SantaLucia
      1998) is read from each gene's own promoter window (TSS-2000..+500). KCNQ2/KCNQ3/KCNB1/SCN2A/GRIN2A
      reuse the bipolar promoter cache VERBATIM (gamma is strand-symmetric, bit-identical). Two honest
      caveats are recorded, not hidden: KCNT1 is sign-INVERTED (its gain-of-function is pathological), and
      the L1 Na-block direction is CONTRAINDICATED in Dravet/SCN1A loss-of-function -- exactly why gamma is
      [V] for promoter STRUCTURE only, trait-blind, with clinical direction graded [O]. A fail-closed
      L3-honesty gate keeps every mTOR mechanism link [O]; a fail-closed forbidden-claim scanner forbids
      dose/efficacy/safety/synthesis (incl. "seizure-freedom" language); a burden-weighted prioritisation
      ranks TARGETS with gamma carried alongside but NEVER folded into the score (the stiffest promoter
      CACNA1H ranks LOW; the top-priority SCN1A reads nearly softest -- the decoupling witness). FIREWALL:
      the promoter |h_sp| is the gene's own switch stiffness, never equated with the §25 network over-sync
      threshold on R, nor with channel voltage / potency / dose / clinical effect. efficacy=0; no new tuned
      constant; engine READ-ONLY.
  T1b-L Depression levers -- the SAME threshold-shift intervention logic applied to the TEMPORAL low-
      coordination pole, and the first case that is L3-DOMINANT rather than channel-led. §27 (T1b) placed
      major depression as the chronification of an operating point with R BELOW health, driven by a sustained
      up-stream (HPA) withdrawal; the corrective sign there is "restore the deficient drive" -- the mirror of
      the epilepsy/bipolar "reduce the excess" -- and §27 left that restoration as ONE abstract operator. This
      module decomposes it into a DNA-grounded three-lever target map on the SAME R19 substrate, but with the
      weight on L3: of 18 genes, 12 are L3 up-stream drives in three sub-axes -- (a) HPA REMOVE (NR3C1, CRHR1,
      FKBP5), (b) monoamine RESTORE (SLC6A4, SLC6A2, MAOA, TPH2, HTR1A, HTR2A, COMT), (c) neurotrophic RESTORE
      (BDNF, NTRK2) -- while L1 inward (GRIN2B/GRIN2A/CACNA1C) and L2 outward (KCNQ2/KCNQ3/GABRA1) are the
      minor channel levers. gamma = -mean(NN stacking dG, SantaLucia 1998) is read from each gene's own
      promoter window (TSS-2000..+500); NR3C1/CRHR1/GRIN2A/CACNA1C/KCNQ2/KCNQ3 reuse the bipolar cache and
      GABRA1 reuses the epilepsy cache VERBATIM (gamma is strand-symmetric, bit-identical). Honest caveats are
      recorded, not hidden: the disorder-level sign FLIP (depression is the hypo-coordination pole, so the
      restoring direction is opposite to epilepsy's), HTR2A's non-monotone direction, and the ketamine subtlety
      (an NMDA antagonist acting through a downstream disinhibition route, so the naive L1 sign is flagged sign-
      subtle). A fail-closed L3-honesty gate keeps every up-stream-drive link [O] cited biology AND asserts L3
      is dominant; a fail-closed forbidden-claim scanner forbids dose/efficacy/safety/synthesis (incl. "lifts
      mood"/"remission"/"antidepressant efficacy" language); a burden-weighted prioritisation ranks TARGETS
      with gamma carried alongside but NEVER folded into the score (top priority BDNF reads mid-range stiffness;
      the stiffest promoter KCNQ2 ranks LOW and non-actionable -- the decoupling witness). FIREWALL: the promoter
      |h_sp| is the gene's own switch stiffness, never equated with the §27 network coordination level R, nor
      with channel voltage / potency / dose / clinical effect. efficacy=0; no new tuned constant; engine READ-ONLY.

  T1a-L Schizophrenia levers -- the SAME threshold-shift intervention logic applied to the §24 over-ignition
      (aberrant-salience) pole, and the first case that is L1+L3 CO-DOMINANT and the first that is DOMAIN-
      RESTRICTED. §24 (T1a) placed the positive domain as an operating point whose ignition fold sits too low
      (weak assemblies ignite as percepts/beliefs); the corrective sign is "reduce the excess drive / raise the
      fold" -- the SAME direction as epilepsy/bipolar-mania -- but §24 left that as ONE abstract operator. This
      module decomposes it into a DNA-grounded three-lever target map on the SAME R19 substrate, with the weight
      split EVENLY across L1 and L3 (6 targets each): L1 = the glutamate/NMDA axis (GRIN1, GRIN2A, GRIN2B, GRIA3,
      CACNA1C, CACNB2) and L3 = the dopamine antipsychotic axis in three sub-axes -- receptors (DRD2, DRD4),
      synthesis/transport (TH, SLC6A3), serotonergic modulation (HTR2A) and prefrontal catabolism (COMT) -- while
      L2 (GABRA1, GABRB3) is the minor PV-interneuron-restore lever. gamma = -mean(NN stacking dG, SantaLucia
      1998) is read from each gene's own promoter window (TSS-2000..+500); GRIN2A/CACNA1C/CACNB2 reuse the bipolar
      cache, GRIN2B/COMT/HTR2A/GABRA1 reuse the depression cache, and the remaining genes reuse the disease/ADHD
      caches VERBATIM (gamma is strand-symmetric, bit-identical). The NEW structural finding is the DOMAIN
      RESTRICTION: the gain-reducing scalar lever reverses the POSITIVE domain ONLY; the NEGATIVE (output-deficit)
      and COGNITIVE (long-range wiring) domains are NOT reached -- a threshold shift cannot re-route geometry nor
      restore a deficit by lowering a fold. Honest caveats are recorded, not hidden: the NMDA-hypofunction sign
      subtlety (L1 GRIN1/GRIN2A act through PV-interneuron hypofunction -> downstream disinhibition, the SZ
      analogue of depression's ketamine caveat) and HTR2A's non-monotone direction. A fail-closed L3-honesty gate
      keeps every dopamine-axis link [O] cited biology AND asserts L1+L3 co-dominance AND the positive-domain
      restriction; a fail-closed forbidden-claim scanner forbids dose/efficacy/safety/synthesis (incl. "treats
      psychosis"/"remission"/"relapse-prevention"/"antipsychotic efficacy" language); a burden-weighted
      prioritisation ranks TARGETS with gamma carried alongside but NEVER folded into the score (top priority
      GRIN2A reads mid-range stiffness, and the unmet-need tier lifts the glutamatergic L1 route ABOVE the
      established D2 route; the stiffest promoter SLC6A3 ranks LOW and non-actionable -- the decoupling witness).
      FIREWALL: the promoter |h_sp| is the gene's own switch stiffness, never equated with the §24 network over-
      ignition threshold, nor with channel voltage / potency / dose / clinical effect. efficacy=0; no new tuned
      constant; engine READ-ONLY.

  ASD-T-L Autism levers -- the SAME threshold-shift intervention logic applied to the sec.18-19 E/I over-
      excitation pole, and the UNIFICATION case: rather than introducing a new lever combination it re-expresses
      the pre-existing autism_multilever_threshold.py under the formal L1/L2/L3 frame. sec.18-19 placed autism's
      excitability/E-I axis (the T-fault) as an operating point whose ignition fold sits too low (over-excitation);
      the corrective sign is "reduce the excess drive / restore inhibition / raise the fold" -- the SAME direction
      as epilepsy/schizophrenia-positive -- but the existing module carried it under informal A1/A2/A3 levers. This
      module decomposes it into a DNA-grounded three-lever target map on the SAME R19 substrate, L1-DOMINANT with a
      nearly-empty L3 (the 5th distribution pattern across the T-L series): L1 = the excitatory-reduce axis (GRIN2A,
      GRIN2B, GRIA1, SCN2A, CACNA1C, 5 targets), L2 = the inhibitory-restore axis (KCNQ3 M-current K+, GABRB3,
      GABRA5, GABRA2, 4 targets), L3 = a single cautious serotonergic node (SLC6A4, [O], non-monotone). gamma =
      -mean(NN stacking dG, SantaLucia 1998) is read from each gene's own promoter window (TSS-2000..+500);
      GRIN2A/GRIN2B/CACNA1C/GABRB3 reuse the schizophrenia cache, SCN2A/KCNQ3 reuse the bipolar cache, and SLC6A4
      reuses the depression cache VERBATIM (gamma is strand-symmetric, bit-identical). Autism carries TWO structural
      strengthenings beyond the schizophrenia domain-restriction template: (1) the OUT-OF-REACH axes are NAMED with
      real genes -- O (output-deficit) = SHANK3/SYNGAP1/NRXN1, W (long-range wiring) = CNTNAP2/RELN, plus the
      syndromic MECP2 -- carried alongside but explicitly NOT levers; (2) the W-axis unreachability is PROVEN, not
      merely asserted: sec.19 (autism_candidate_limits) showed a scalar threshold lever can only MASK the wiring
      fault via over-synchronisation (the seizure analogue, P5_threshold_lowering_is_mask_not_correction), never
      CORRECT it (P4_chemical_cannot_fix_W). Honest caveats are recorded, not hidden: SCN2A/GRIN2B are GoF/LoF
      sign-subtle (a gain-of-function pushes the early DEE/seizure pole, a loss-of-function the milder ASD/ID pole),
      and the T-lever pushed too hard is itself the seizure edge (the real ASD+epilepsy comorbidity). A fail-closed
      L3-honesty gate keeps the serotonergic link [O] cited biology AND asserts L1 UNIQUE dominance, L3 SPARSITY,
      the T-axis domain restriction, and the NAMED+sec.19-proven O/W out-of-reach axes; a fail-closed forbidden-
      claim scanner forbids dose/efficacy/safety/synthesis PLUS an autism-specific QUACKERY class (chelation/MMS/
      bleach) and a NORMALISE-framing class (neurodiversity respect: autism is a DIFFERENCE, not only a deficit); a
      burden-weighted prioritisation ranks TARGETS with gamma carried alongside but NEVER folded into the score (the
      AUTISM unmet-need signature -- no approved CORE-feature pharmacology -- keeps U uniformly high, and the L2
      inhibitory-restore route surfaces as the cleanest ACTIONABLE direction because the high-scoring L1 excitatory
      genes are GoF/LoF sign-subtle; the stiffest promoter SLC6A4 ranks LOWEST and non-actionable -- the decoupling
      witness). FIREWALL: the promoter |h_sp| is the gene's own switch stiffness, never equated with the sec.18
      network over-excitation fold, nor with channel voltage / potency / dose / clinical effect. efficacy=0; no new
      tuned constant; engine READ-ONLY.

  ADHD-T-L ADHD levers -- the SAME threshold-shift intervention logic applied to the sec.22 adhd_axis_specific
      substrate (gain/arousal with INTACT wiring), and the FIRST PARTIAL [L] fit of the series: it maps the sec.22
      substrate onto the L1/L2/L3 frame by REACHABILITY, and the frame reaches only the SECONDARY axis. ADHD is
      L3-ONLY -- L1 (ionic-fold) and L2 (network-timing) are BOTH EMPTY -- the 6th and purest distribution pattern:
      every reachable lever is an upstream catecholamine/monoaminergic DRIVE-TONE node. L3 = the drive-tone axis
      (SLC6A3/DAT, SLC6A2/NET, SLC6A4/SERT, ADRA2A/alpha-2A, DRD4/D4, 5 targets; SLC6A3/DRD4 are sec.22-O genes
      reachable here as drive-TONE, recorded per-gene with a sec22_axis field). gamma = -mean(NN stacking dG,
      SantaLucia 1998) is read from each gene's own promoter window (TSS-2000..+500); SLC6A3/DRD4/COMT/TH reuse the
      schizophrenia cache and SLC6A4/SLC6A2 reuse the depression cache VERBATIM (bit-identical), and ADRA2A/DBH/
      SNAP25 are live-fetched (GRCh38, strand-aware); gamma is strand-symmetric. ADHD carries THREE structural
      properties beyond the autism domain-restriction template: (1) it is L3-ONLY (L1==L2==0), the purest single-
      lever loading in the series; (2) the OUT-OF-REACH axis is the DOMINANT one -- the GA gain-amplitude genes
      (TH/DBH SYNTHESIS, SNAP25 RELEASE, + COMT clearance BOUNDARY) are NAMED out-of-reach (a drive-tone reuptake/
      receptor lever has no handle on synthesis/release), which is exactly WHY the fit is PARTIAL [L], not the clean
      [V] of the five prior disorders -- the dominant axis is the out-of-reach one; (3) the W (long-range wiring)
      axis is ABSENT from the disorder -- ADHD has INTACT wiring (sec.22), ZERO wiring genes -- the DISCRIMINANT
      from autism and the autism INVERSE (autism reached its dominant T axis and missed O+W; ADHD reaches only the
      secondary DT axis and misses the dominant GA axis, with no W axis at all). A fail-closed L3-honesty gate keeps
      every drive-tone link [O] cited biology AND asserts L3 UNIQUE dominance, L1/L2 EMPTINESS, the DT-axis domain
      restriction, the GA out-of-reach axis NAMED, the W axis ABSENT, and the PARTIAL [L] fit; a fail-closed
      forbidden-claim scanner forbids dose/efficacy/safety/synthesis PLUS an ADHD-specific STIMULANT-MISUSE class
      (get-high/snort/euphoria/recreational) and a COGNITIVE-ENHANCEMENT class (smart-drug/nootropic/boost-focus/
      limitless); a burden-weighted prioritisation ranks TARGETS with gamma carried alongside but NEVER folded into
      the score (the ADHD unmet-need signature -- the AUTISM MIRROR: established core routes LOWER unmet on the
      reachable transporters, U-floor=2, the lowest in the series, while the out-of-reach GA gain genes carry the
      unmet-need CEILING and are non-actionable -- so the highest-need targets are precisely the unreachable ones;
      the stiffest promoter SLC6A3 sits MID-table because its established route lowers its unmet need -- the
      decoupling witness, here the autism inverse). FIREWALL: the promoter |h_sp| is the gene's own switch
      stiffness, never equated with the sec.22 network gain/arousal quantity, nor with transporter occupancy /
      potency / dose / clinical effect. efficacy=0; no new tuned constant; engine READ-ONLY.

  ADD-T-L Addiction levers -- the SAME threshold-shift intervention logic applied to the sec.28 state-switching /
      sec.26 E0 plasticity incentive-sensitisation substrate, and the SECOND PARTIAL [L] fit of the series: it maps
      that substrate onto the L1/L2/L3 frame by REACHABILITY, and the frame reaches the INSTANTANEOUS drive/
      excitability operating point richly but NOT the dominant consolidated-gain fault. Addiction is L3-DOMINANT
      WITH L1 AND L2 BOTH PRESENT -- the 7th distribution pattern and the TEXTURAL INVERSE of ADHD's L3-only
      emptiness (ADHD was 'not a channelopathy'; addiction engages the ionic levers too). L3 = the reward-drive axis
      (OPRM1/mu-opioid, OPRK1/kappa-opioid, DRD2/D2, SLC6A3/DAT, CHRNA5/nAChR, 5 targets), L1 = the glutamate-
      plasticity substrate (GRIN2A/GRIN2B, 2), L2 = the inhibitory-restore arm (GABRA2/GABRG3, 2). gamma = -mean(NN
      stacking dG, SantaLucia 1998) is read from each gene's own promoter window (TSS-2000..+500); DRD2 reuses the
      schizophrenia cache, BDNF the depression cache, GRIN2A/GRIN2B/GABRA2 the autism cache and SLC6A3 the ADHD
      cache VERBATIM (bit-identical), and OPRM1/OPRK1/CHRNA5/GABRG3/FOSB/CREB1/ARC are live-fetched (GRCh38, strand-
      aware); gamma is strand-symmetric. Addiction carries THREE structural properties beyond the ADHD partial-fit
      template: (1) it is L3-DOMINANT but NOT L3-only -- L1 and L2 are BOTH present (the ADHD inverse), a richer
      reachable surface; (2) the OUT-OF-REACH axis is the DOMINANT one and is reached for a DEEPER reason than ADHD
      -- the SG consolidated-sensitisation-gain genes (FOSB/deltaFosB, BDNF, CREB1, ARC) are NAMED out-of-reach
      because SG is a GAIN not a fold (the ADHD lesson) AND moreover CONSOLIDATED/LEARNED, a plasticity (E0-layer,
      sec.26) variable -- even a drive lever that dampens the instantaneous response cannot ERASE the durable trace
      -- which is exactly WHY the fit is PARTIAL [L]; (3) the SG axis is precisely the E0 plasticity layer (sec.26),
      so addiction is the CONVERGENCE point where threshold-leverisation (B-i) structurally meets the dynamics route
      (B-ii) -- B-i NAMES the learned trace out-of-reach honestly. A fail-closed L3-honesty gate keeps every reward-
      drive link [O] cited biology AND asserts L3 UNIQUE dominance, L1/L2 BOTH PRESENT, the INSTANT-axis domain
      restriction, the SG out-of-reach axis NAMED, and the SECOND PARTIAL [L] fit; a fail-closed forbidden-claim
      scanner forbids dose/efficacy/safety/synthesis PLUS an addiction-specific DRUG-SEEKING class (where-to-buy/
      how-to-obtain/inject/snort/get-high/euphoria) and a CURE-MIRACLE class (miracle-cure/guaranteed-sober/detox-
      miracle/addiction-gone); a burden-weighted prioritisation ranks TARGETS with gamma carried alongside but
      NEVER folded into the score (the addiction unmet-need signature -- a MIDDLE case between ADHD and autism:
      established core routes exist but are only PARTIALLY effective with HIGH RELAPSE, so the reachable levers
      carry only MODERATE unmet, U-floor=3, above ADHD's clean-route floor, while the out-of-reach SG gain genes
      carry the unmet-need CEILING and are non-actionable -- so the highest-need targets are precisely the
      unreachable ones; the stiffest promoter SLC6A3 sits MID-table because its established route lowers its unmet
      need -- the decoupling witness). FIREWALL: the promoter |h_sp| is the gene's own switch stiffness, never
      equated with the consolidated sensitisation gain, nor with receptor occupancy / potency / dose / clinical
      effect; addiction is a TREATABLE MEDICAL CONDITION, not a moral failing. efficacy=0; no new tuned constant;
      engine READ-ONLY.
  ADD-T3a Addiction sensitisation dynamics -- the OTHER HALF of the §36 (ADD-T-L, B-i) convergence: B-i NAMED the
      integrated sensitisation gain (the deltaFosB trace that makes addiction chronic and relapsing) OUT OF REACH for
      the instant L1/L2/L3 levers, for two reasons -- it is a GAIN not a fold (the ADHD lesson) AND a LEARNED/
      CONSOLIDATED plasticity variable -- so no instant lever can move it. This module MODELS that exact trace
      DIRECTLY by IMPORTING the E0 PlasticConnectome (sec.26; it does NOT re-derive the Hebbian rule or the coupling
      map) and driving it with a REWARD bias whose SIGN is grounded READ-ONLY in the engine: M5 (dopamine reward-
      prediction error) potentiates the rewarded eddy's laid-down probability above an unrewarded control, and M4
      (basal-ganglia selection) commits a winner -- reward POTENTIATES, so a reward-exposure epoch maps to a positive
      reward-drive bias and the E0 phase-correlation Hebbian update accumulates it into a retained ||W-W0|| (the
      integrated gain as a structural quantity). Five pre-registered SIGN-only results, all CONFIRMED over an eta
      sweep: A1 incentive sensitisation (repeated exposure monotonically builds the trace -- the gain accumulating);
      A2 cue-reactivity (the sensitised connectome responds MORE to the same reward cue than a naive one, R_sens(cue)
      > R_naive(cue) -- the relapse substrate; only the response-exceeds-naive sign is asserted, the marginal cue gain
      is NOT claimed monotone); A3 extinction-persistence (removing the reward does NOT return the trace to zero under
      plasticity, eta>0 trace > 0, while eta=0 trace == 0 exactly -- extinction removes the DRIVE, the reachable
      instant axis, but not the LEARNED TRACE, the out-of-reach axis: the convergence seam, dynamically); A4 the
      plasticity-variable guard (with eta=0 the reward excursion reverts EXACTLY and W stays identical to the kernel
      -- the gain VANISHES without plasticity, proving it is a learned variable, which is precisely why B-i's instant
      levers cannot reach it; eta=0 reproduces the frozen M9 anchor bit-for-bit); and A5 the dynamics handle (SPACED/
      intermittent reward exposure consolidates a LARGER trace than MASSED/continuous at equal total exposure --
      intermittent reinforcement sensitises more, the E0.2 spacing effect applied to reward -- the structural HANDLE
      on the trace the instant frame could not reach). The two halves of the convergence meet in ONE disorder: B-i
      names the gain unreachable for instant levers, B-ii exhibits it AND gives a structural handle on it. FIREWALL:
      the retained trace is the integrated gain as a STRUCTURAL quantity, never a claim about the FELT quality of
      craving/reward/relapse (Axis-A; consciousness_claim=0; hard problem OPEN); real addiction plasticity is
      heterogeneous (deltaFosB/CREB/BDNF cascades, AMPA trafficking, spine remodelling, epigenetics -- LOCKED), only
      the SIGN is asserted; the reward SIGN is grounded in M5 RPE and every MAGNITUDE (including eta) is [O]; addiction
      is a CHRONIC RELAPSING MEDICAL condition, not a moral failing, and nothing is a cure or a licence to use any
      substance. efficacy=0; no new tuned constant; engine READ-ONLY; reuses the E0 PlasticConnectome.

  AD-T3b-L Alzheimer's threshold-levers -- the SAME threshold-shift intervention logic applied to the cholinergic /
      glutamatergic-excitotoxicity / inhibitory-network substrate of Alzheimer's, and the THIRD & DEEPEST PARTIAL [L]
      fit of the series. The frame re-cuts the disorder by REACHABILITY and reaches the INSTANTANEOUS symptomatic
      operating point richly but NOT the dominant neurodegenerative-progression fault, so the fit is PARTIAL [L]. The
      reachable SYMP surface is purely SYMPTOMATIC with a SPLIT corrective sign -- L3 cholinergic DRIVE is RESTORED
      (deficient acetylcholine tone up: ACHE/BCHE/CHRNA7/CHRM1, the donepezil/rivastigmine/galantamine direction, the
      DOMINANT lever, 4 nodes); L1 glutamatergic EXCITOTOXICITY is REDUCED (excess NMDA drive down: GRIN2B/GRIN2A, the
      memantine direction, 2 nodes); L2 inhibitory tone is RESTORED against AD network HYPEREXCITABILITY (GABRA1/
      GABRA5/GABRB3, 3 nodes) -- the FIRST reachable surface in the series that is both purely symptomatic AND
      split-sign (the 8th distribution pattern; gross shape shared with addiction's L3-dominant-plus-L1/L2 but
      distinguished by SPLIT SIGN and SYMPTOMATIC-ONLY reach). The out-of-reach axis is the DOMINANT one and is reached
      for the DEEPEST reason in the series: the PROG neurodegenerative-progression genes (APP/PSEN1/PSEN2 amyloid/
      gamma-secretase, MAPT tau, APOE clearance, TREM2 microglial) are NAMED out-of-reach because PROG is a gain/loss
      not a fold (the ADHD lesson), AND a PROGRESSION over time -- a plasticity (E0-layer) variable (the addiction
      lesson), AND moreover a DEGENERATION -- a cumulative, irreversible LOSS, an E0 DECAY that is the structural
      INVERSE of addiction's E0 GAIN; so even a drive lever that restores instantaneous tone cannot HALT the cumulative
      loss. Two fail-closed gates: an L3-honesty gate (every L3 cholinergic-drive node graded [O] cited-biology, not
      derived; L3 UNIQUE dominance + L1/L2 BOTH present; the SYMPTOMATIC split-sign domain restriction; the PROG axis
      NAMED out-of-reach -- the deepest partial fit), and a forbidden-claim scanner (dose/efficacy/safety/synthesis
      PLUS an Alzheimer's-specific CURE_REVERSAL class -- reverse/cure/prevent AD, stop/halt the progression, restore
      lost memory, regrow neurons, miracle cure -- PLUS a DIGNITY class -- empty shell/no longer a person/vegetable/
      already gone/not worth treating). A burden-weighted prioritisation ranks TARGETS with gamma carried alongside but
      NEVER folded into the score (the Alzheimer's unmet-need signature -- the DEEPEST partial fit: the reachable
      surface is purely symptomatic, the cholinergic levers carry MODERATE unmet need where an established but
      SYMPTOMATIC/temporary route exists, while the OUT-OF-REACH PROG progression axis carries the unmet CEILING --
      disease-MODIFICATION, the single greatest unmet need, only modestly touched even by lecanemab/donanemab -- so the
      highest-need targets are exactly the unreachable ones, for the deepest reason). FIREWALL: promoter |h_sp| is not
      a neurodegeneration rate, an amyloid burden, or a tau load; cholinesterase inhibitors and memantine are
      SYMPTOMATIC ONLY and do NOT slow progression; the anti-amyloid antibodies (lecanemab/donanemab) target the
      out-of-reach PROG axis and are progression-modifiers, not threshold levers; a person living with dementia remains
      a person (Axis-A; consciousness_claim=0; hard problem OPEN). efficacy=0; no new tuned constant; engine READ-ONLY;
      reuses the autism (GRIN2A/GRIN2B/GABRA5/GABRB3) and epilepsy (GABRA1) promoter caches verbatim.

  AD-T3b-D Alzheimer's progression dynamics -- the OTHER HALF of the §38 (AD-T3b-L, B-i) convergence, and the exact
      INVERSE of the addiction convergence (sec.36/sec.37). B-i NAMED the dominant PROG neurodegenerative-progression
      axis (the cumulative, irreversible loss of synapses and neurons) OUT OF REACH for the instant symptomatic levers,
      for the DEEPEST reason in the series: it is a gain/loss not a fold (the ADHD lesson), AND a PROGRESSION over time
      -- a plasticity (E0-layer) variable (the addiction lesson), AND a DEGENERATION -- a cumulative IRREVERSIBLE LOSS
      = E0 DECAY, the structural INVERSE of addiction's E0 GAIN (addiction consolidates a trace the levers cannot erase;
      Alzheimer's loses a substrate the levers cannot rebuild). This module MODELS that decay DIRECTLY by REUSING the
      E0 plasticity LAYER (it imports the sec.26 PlasticConnectome, the kernel W0, the coupling map, and the order-
      parameter machinery -- it does NOT re-derive them) and applying to that kernel the STRUCTURAL INVERSE of E0's
      Hebbian consolidation: a slow progressive CONNECTIVITY ATTRITION (synapse/neuron loss, mass DOWN where sec.37
      drove mass UP). Unlike sec.37 -- whose reward SIGN came from an ENGINE signal (M5 RPE) -- the engine has NO
      degeneration signal, so the loss DIRECTION is grounded as the structural inverse of E0 GAIN (definitional loss),
      not in an engine pathology signal; what IS grounded READ-ONLY is the BASELINE being lost (the frozen M9 anchor)
      and the GUARD. Five pre-registered SIGN-only results, all CONFIRMED over a decay-rate sweep, each the inverse of a
      sec.37 result: D1 progressive degeneration (progression monotonically accumulates connectivity loss; deeper ->
      less surviving mass and lower coordination R -- inverse of incentive sensitisation); D2 loss of responsiveness
      (a degenerated connectome responds LESS to the same coordinating cue than a healthy one, R_degen(cue) <
      R_healthy(cue) -- progressive functional decline, inverse of cue-reactivity); D3 levers-do-not-rebuild (the
      symptomatic cue, the B-i reachable instant axis, leaves the cumulative structural loss EXACTLY unchanged, and at
      deep loss even the maximum cue cannot reach the healthy anchor -- relief WITHOUT disease modification, the
      convergence seam, inverse of extinction-persistence; exactly why cholinesterase inhibitors and memantine are
      symptomatic only); D4 the structural-variable guard (with decay rate = 0 the connectome stays identical to the
      kernel and the order parameter returns to the frozen M9 anchor bit-for-bit -- degeneration is a structural-loss
      variable the instant levers cannot reach; pure add-on; mirror of the addiction plasticity-variable guard); and
      D5 the dynamics handle (a LOWER decay rate preserves STRICTLY MORE structure at equal progression time, while the
      symptomatic cue has NO handle on the structural trajectory -- the handle lives ONLY on the PROGRESSION axis, the
      disease-modification direction where the anti-amyloid antibodies act; inverse of the spacing handle). The two
      halves of the AD convergence meet in ONE disorder: B-i names the decay unreachable for instant levers, B-ii
      exhibits it AND shows the handle is on the progression axis alone. FIREWALL: the connectivity loss is the
      progression as a STRUCTURAL quantity, never a claim about the FELT quality of memory/loss/selfhood in dementia
      (Axis-A; consciousness_claim=0; hard problem OPEN); a person living with dementia REMAINS a person -- the loss is
      a substrate boundary, NOT a subtraction of the person; real neurodegeneration is heterogeneous (amyloid/tau/
      synapse loss/neuroinflammation -- LOCKED), only the SIGN of cumulative loss is asserted; magnitudes [O]; nothing
      is a cure, reversal, prevention or halt of progression. efficacy=0; no new tuned constant; engine READ-ONLY;
      reuses the E0 PlasticConnectome (imported, not re-derived).
  OCD-T3c-L OCD CSTC-loop levers -- the SAME threshold-shift intervention logic applied to obsessive-compulsive
      disorder, the roadmap's "cortico-striatal-thalamic loop as a pathological limit-cycle / stuck attractor"
      (needs E1 + E2). The FOURTH PARTIAL [L] fit and a NEW MODE. OCD is, before anything else, a disorder of a STUCK
      LOOP: its dominant fault is a self-sustaining, over-consolidated, pathologically STABILISED CSTC attractor. The
      frame reaches the INSTANTANEOUS CSTC excitability operating point across L1/L2/L3 -- L3 the up-stream
      serotonergic/dopaminergic DRIVE (SLC6A4/HTR2A/HTR1B RESTORE the serotonergic tone via the SSRI first-line; DRD2
      REDUCE the dopaminergic drive via antipsychotic augmentation), L1 the glutamatergic EXCITATORY axis (SLC1A1/EAAT3
      the most replicated OCD gene, GRIN2B, GRIK2 -- REDUCE the hyperactive loop drive), and a SPARSE L2 inhibitory-
      restore arm (GABRA1, a single weak node) -- the NINTH distribution pattern (L3-dominant, L1 strong, L2 sparse;
      OCD's GABAergic arm is thin) with a MIXED/split corrective sign, and unlike Alzheimer's purely-symptomatic surface
      the OCD levers are the actual mainstay/investigational routes that genuinely (PARTIALLY) help. But it does NOT
      reach the DOMINANT fault, the LOCK pathological-stabilisation axis -- the over-deep basin / hysteresis that holds
      the compulsive loop -- named with four real circuit-fixation genes (DLGAP3/SAPAP3 the corticostriatal scaffold of
      the canonical OCD model, SLITRK5, PTPRD, BTBD3), graded [F] NOT REACHED. The LOCK axis is out of reach for three
      reasons: it is not a fold (the ADHD lesson: a lever moves a set-point, not a basin depth), AND a consolidated/
      learned plasticity (E0-layer) variable (the addiction lesson), AND -- the NEW mode -- a pathological STABILISATION
      / LOCK: an over-deep basin / hysteresis (an E2 phenomenon), the THIRD distinct E0 mode, distinct from addiction's
      E0 GAIN and Alzheimer's E0 DECAY (completing the trio addiction GAIN -> Alzheimer's DECAY -> OCD STABILISATION).
      So the instantaneous levers nudge the operating point but cannot UNSTICK the loop -- which is exactly why response
      is partial and slow, and why a DYNAMICS intervention (CSTC deep-brain stimulation, ERP extinction that
      re-plasticises the loop) reaches refractory cases the levers cannot; OCD is the convergence point with the E2/E0
      dynamics layer (a future B-ii). An L3-honesty gate keeps all four serotonergic/dopaminergic-drive links [O] cited
      biology AND asserts L3 unique dominance, L1 present, L2 SPARSE, the INSTANT domain restriction, the LOCK-axis
      named-out-of-reach, and the PARTIAL [L] fit; a forbidden-claim scanner rejects dose/efficacy/safety/synthesis PLUS
      an OCD CURE_MIRACLE class and a MORAL_FRAMING/STIGMA class (OCD is a treatable medical condition and intrusive
      thoughts are a symptom, not a confession or a weakness); a burden-weighted prioritisation ranks all 12 TARGETS
      with gamma carried alongside but NEVER folded into the score (the deepest-unmet U=5 tier is held ENTIRELY by the
      out-of-reach loop-lock genes, while the leading actionable target SLC1A1 is reachable but only partially helps;
      decoupling: the stiffest promoter DLGAP3 sits at priority #3 not the top). FIREWALL: the promoter |h_sp| is the
      gene's own switch stiffness, NEVER the basin depth / hysteresis width / strength of the compulsive lock (Axis-A;
      consciousness_claim=0; hard problem OPEN). efficacy=0; no new tuned constant; engine READ-ONLY.
  OCD-T3c-D OCD stabilisation dynamics -- the OTHER HALF of the OCD convergence OCD-T3c-L (B-i) opened: the dominant
      compulsion-maintaining axis, the self-sustaining STUCK LOOP, modelled DIRECTLY on the E0 plasticity layer as the
      THIRD E0 MODE (completing addiction GAIN -> Alzheimer's DECAY -> OCD STABILISATION). REUSES the E0 PlasticConnectome
      (imported, not re-derived) and drives the frozen kernel through E0's potentiating Hebbian update, at a negatively-
      reinforced coordinated operating point, until the connectome writes the coordination into its own structure -- a
      self-sustaining locked loop. S1 PROGRESSIVE STABILISATION: consolidation monotonically writes structure (trace up
      over BOTH an eta and a bias sweep) and the locked state deepens (Rlock deeper >= shallower) -- a basin-depth variable
      the instant levers cannot reach. S2 SELF-SUSTAINING LOOP (the defining readout): a consolidated connectome started
      from a COORDINATED (locked) IC holds its coordination at/above the frozen M9 anchor at rest, and at/above the cold-
      start (fresh) branch, with NO external cue (the loop runs itself); the excess Rlock-M9 grows -- distinct from
      addiction's cue-reactivity and Alzheimer's decline. S3 LEVERS-DO-NOT-UNSTICK (the seam): the symptomatic lever leaves
      the retained trace EXACTLY unchanged and even the maximum lever cannot reduce it -- relief without re-writing the
      loop, exactly why SSRIs/augmentation manage symptoms and do not by themselves erase the compulsion loop. S4 GUARD:
      with consolidation=0 the connectome stays identical to the kernel and the order parameter (FAITHFUL integrator from
      the engine's own fixed incoherent-seed IC) returns to the frozen M9 anchor bit-for-bit, trace zero -- stabilisation
      is a structural variable the instant levers cannot reach (pure add-on). S5 DYNAMICS HANDLE: a lower consolidation
      rate writes strictly less structure while the lever has NO structural handle -- the handle lives ONLY on the
      consolidation (learning/plasticity) axis where ERP re-writing acts. HONEST DISANALOGY with §37: the engine has NO
      stuck-loop signal, so the stabilisation sign is grounded as the SAME E0 consolidation family as the addiction GAIN
      (both write a trace), DISTINGUISHED by the self-sustaining-at-rest readout -- NOT in an engine pathology signal (the
      addiction sign came from M5 RPE). The basin-depth concept is grounded in the READ-ONLY R19 barrier B(g)=g^2/4=0.25;
      the NETWORK has NO clean bistability under these couplings, so NO network-hysteresis is claimed (the proper over-deep
      basin is an E2/R19-cusp phenomenon). FIREWALL: the retained trace is the loop as a STRUCTURAL quantity, never a claim
      about the FELT quality of an intrusive thought, an urge, or the distress of a compulsion (Axis-A; consciousness_claim
      =0; hard problem OPEN); OCD is a TREATABLE condition and an intrusive thought is a symptom, not a wish or a moral
      failing; real OCD is heterogeneous (CSTC hyperconnectivity, SAPAP3/DLGAP3 PSD pathology, SLITRK5, serotonergic/
      glutamatergic dysregulation -- LOCKED), only the SIGN of a self-sustaining stabilisation is asserted; magnitudes [O];
      nothing is a cure, reversal or prevention. efficacy=0; no new tuned constant; engine READ-ONLY; reuses the E0
      PlasticConnectome (imported, not re-derived).
  E0-SYNTH the E0 triad synthesis -- the v1.49 capstone. A meta-synthesis (ZERO new measurement, ZERO new machinery,
      ZERO new tuned constant) that cross-reads the three now-frozen E0-dynamics faces -- addiction GAIN (§37), Alzheimer's
      DECAY (§39), OCD STABILISATION (§41) -- and certifies the single structural statement they jointly make: ONE plasticity
      layer, read three ways. It re-verifies the three source results bit-for-bit (sha256 == frozen) before reading them, then
      emerges the engine READ-ONLY for the invariants and certifies five claims. T1 ONE SHARED LAYER: all three are applications
      of the E0 consolidation update on the SAME imported PlasticConnectome, and with plasticity OFF all three revert to the
      frozen M9 anchor bit-for-bit (each module's own revert flag). T2 THREE DIRECTIONS OF MASS: the same layer moves structure
      UP under reward (gain), DOWN under degeneration (decay), and UP into a self-holding well under negatively-reinforced
      coordination (stabilisation) -- three distinct headline signs. T3 THREE READOUTS: cue-reactivity (gain), loss-of-
      responsiveness (decay), self-sustains-at-rest with Rlock above the anchor (stabilisation). T4 SAME FAMILY, DIFFERENT
      READOUT: gain and stabilisation write the SAME trace at the same operating point (0.35285 == 0.35285) and are separated
      ONLY by the self-sustaining-at-rest readout -- exactly the honest disanalogy §41 already declared. T5 SEAM + HANDLE: in
      all three the symptomatic levers are structurally inert and the only handle lives on the plasticity (consolidation) axis.
      FIREWALL inherited unchanged from all three faces: every trace is a STRUCTURAL quantity, never a claim about the felt
      quality of a craving, a decline, or an intrusive thought (Axis-A; consciousness_claim=0; hard problem OPEN); nothing is a
      cure. efficacy=0; new_measurement=0; no new tuned constant; engine READ-ONLY; a synthesis of frozen modules only.

Note: the gate verifies REPRODUCIBILITY and DISCIPLINE, not that every pre-registered
prediction is CONFIRMED -- refutations are findings. ADD-ONLY; vp_mind_engine READ-ONLY.
SEED=19, stdlib+numpy.
"""
import os, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
ENGINE_FILE_SHA    = "e61083ae956206e943ed292f5f69f9d3964ef50778e2d7344de93207ade48371"

# (tag, roadmap-id, script, written-results-file, FROZEN sha256 -- the regression guard)
MODULES = [
    ("SZ-DISC", "T1a", "schizophrenia_discriminant.py",
     "schizophrenia_results.json",
     "40b9daff9a6c0501ce29c475529bba6769d95e160359f198b76e0b9875097258"),
    ("SZ-DOM",  "T1a", "schizophrenia_symptom_domains.py",
     "schizophrenia_symptom_domains_results.json",
     "0499f74f83f0539f7a34726d5f580fb583cd23192207cef54c2bdc6fec0f0fc5"),
    ("EPI",     "T2a", "epilepsy_oversync.py",
     "epilepsy_oversync_results.json",
     "d363f0a5fcfd20294e62cb0edc26550cb366dbde8fc671c83bc0814a60d95334"),
    ("E0-PLAS", "E0",  "e0_plasticity.py",
     "e0_plasticity_results.json",
     "5dbfd6dff69e301dc6aa2bdaeed93599472ab582b787e0e831f657b508ce8caf"),
    ("DEP-T1b", "T1b", "depression_chronification.py",
     "depression_chronification_results.json",
     "498f546cb4a79f4af33b5e1859fa50e6b588db6c9c844fca1713bfc40fb17d62"),
    ("E2-SWITCH", "E2", "e2_state_switching.py",
     "e2_state_switching_results.json",
     "47c35e06c86e6f22d9321f449f0bf438e9fa6396b6f90ecd5f6b8a2da83aa159"),
    ("BIP-T2b", "T2b", "bipolar_state_switching.py",
     "bipolar_state_switching_results.json",
     "5c55c0e7b2815bac209ae777ae5106154f859bd641b1b63a84ef2e52cbbdd4be"),
    ("BIP-T2b-L", "T2b-L", "bipolar_threshold_levers.py",
     "bipolar_threshold_levers_results.json",
     "a9f30d732c991bd64d3462e440f1cea34a630a4bcef695cce4370743b69fd0ef"),
    ("EPI-T2a-L", "T2a-L", "epilepsy_threshold_levers.py",
     "epilepsy_threshold_levers_results.json",
     "22879b696cf9226efc660acdea1f017a8018c3d1eb93f324f32da53dbfc14fcf"),
    ("DEP-T1b-L", "T1b-L", "depression_threshold_levers.py",
     "depression_threshold_levers_results.json",
     "d07aab40ba56ee5dd234d65ee8691ac80458a9c71b6355bacfccbd1efdb69f30"),
    ("SZ-T1a-L", "T1a-L", "schizophrenia_threshold_levers.py",
     "schizophrenia_threshold_levers_results.json",
     "8e0137bccfe6dfe751af078a1e340accef578698992e569703865c6c27fe8c30"),
    ("ASD-T-L", "T-L", "autism_threshold_levers.py",
     "autism_threshold_levers_results.json",
     "5b65a271ac182fecc744f20e2bb035043f81c9c1bc3f15608547ec00a31b77c4"),
    ("ADHD-T-L", "T-L", "adhd_threshold_levers.py",
     "adhd_threshold_levers_results.json",
     "d29a3dc8971250ff31d8bc37329a9ce3b1e067a0af81cf869950ce47b1505a35"),
    ("ADD-T-L", "T-L", "addiction_threshold_levers.py",
     "addiction_threshold_levers_results.json",
     "f23e3c126f30e5f137db2773223212625f5e08a9fb34f97583fcad312380e2bb"),
    ("ADD-T3a", "T3a", "addiction_sensitization_dynamics.py",
     "addiction_sensitization_dynamics_results.json",
     "20dfb3e902ffba2132617669f1e065bc6bcf399cb91e338c4cf2711142e845e3"),
    ("AD-T3b-L", "T3b-L", "alzheimers_threshold_levers.py",
     "alzheimers_threshold_levers_results.json",
     "68029dab06ed152da919bdc3d0529058d06226356027e803647441a82b4067fe"),
    ("AD-T3b-D", "T3b", "alzheimers_progression_dynamics.py",
     "alzheimers_progression_dynamics_results.json",
     "7a8e851390e66760c12c96ec6070c5b0e1579293da207129ccb14be65a60d843"),
    ("OCD-T3c-L", "T3c-L", "ocd_threshold_levers.py",
     "ocd_threshold_levers_results.json",
     "c5e2af0eefc404d39725faf48d6085470c63e6965596b332d29b5253882e1456"),
    ("OCD-T3c-D", "T3c", "ocd_stabilisation_dynamics.py",
     "ocd_stabilisation_dynamics_results.json",
     "ef37d619baba3643a16ee564ebe2200e4b3fcc1dea7c23f651b9d9bc1a4fbe79"),
    # --- v1.50 foundational layer: E1 spatial-localisation / field-shaping.
    #     The SPATIAL sibling of the §26 plasticity layer (E0 was the temporal
    #     core). Placed before E0-SYNTH so the synthesis remains the final
    #     atlas citizen; E1 is a new foundational axis, not part of the triad.
    ("E1-SPATIAL", "E1", "e1_spatial_localisation.py",
     "e1_spatial_localisation_results.json",
     "48c83d85edb3e7a24a3e31829085e0029f316b577ae89fd50d58f9ce4d7bbf44"),
    # --- v1.51 first E1 region-specific application: focal epilepsy containment vs
    #     secondary generalisation. The spatial refinement of §25 (T2a) over-sync
    #     epilepsy. Imports the §43 SpatialField (not re-derived) and reads which foci
    #     CONTAIN a focal ictal drive and which BROADCAST it (secondarily generalise);
    #     finds broadcast (off-target relay) is NOT the same axis as the §25 global
    #     over-synchronisation (F3, honest negative). Placed after E1-SPATIAL so the
    #     E1 layer JSON it depends on is freshly regenerated first; before E0-SYNTH.
    ("FOC-EPI-E1", "E1-FOC", "focal_epilepsy_spread.py",
     "focal_epilepsy_spread_results.json",
     "7bbf6a338133080ce0090a44fb3971f2287cd3799688c3b16ccd8e8cff39094b"),
    # --- v1.49 capstone: meta-synthesis of the three frozen E0-dynamics faces
    #     (GAIN / DECAY / STABILISATION). Placed LAST so the three source
    #     results JSONs are freshly regenerated by their own modules above
    #     before this synthesis re-reads and cross-certifies them.
    ("E0-SYNTH", "E0-SYNTH", "e0_triad_synthesis.py",
     "e0_triad_synthesis_results.json",
     "62b49afc94574a3eaf11139832dc7679338e08d90bb6a69bc037ba593b668d10"),
]


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def engine_file_ok():
    p = os.path.join(HERE, "..", "_engine", "vp_mind_engine.py")
    return sha256_file(p) == ENGINE_FILE_SHA


def invariants_ok(res):
    """Engine-frozen across both the byte-frozen constant and the live re-emerge.
    Module ledgers spell the frozen anchor differently (engine_tree_frozen vs
    engine_tree_sha256_unchanged); accept either, as long as it equals FROZEN."""
    inv = res.get("invariants", {})
    frozen = (inv.get("engine_tree_frozen") == ENGINE_TREE_FROZEN
              or inv.get("engine_tree_sha256_unchanged") == ENGINE_TREE_FROZEN)
    live = inv.get("engine_tree_sha256_live")
    live_ok = (live == ENGINE_TREE_FROZEN) if live is not None else True
    unchanged = bool(inv.get("engine_tree_unchanged", True))
    sub = bool(inv.get("m0_16_subtree_unchanged", True))
    return bool(frozen and live_ok and unchanged and sub), {
        "engine_tree_frozen_anchor": frozen,
        "engine_tree_sha256_live_ok": live_ok,
        "engine_tree_unchanged": unchanged,
        "m0_16_subtree_unchanged": sub,
    }


def honesty_ok(res):
    """efficacy=0, no consciousness claim, no tuned constants; and an explicit
    no-cure / hard-problem-open flag (ledger shape differs across modules)."""
    hl = res.get("honesty_ledger", {})
    eff = (hl.get("medium_efficacy_tested", 0) == 0)
    cc = (hl.get("consciousness_claim", 0) == 0)
    tuned = (hl.get("new_tuned_constants", 0) == 0)
    no_cure = (hl.get("no_cure_claimed", 0) == 1) or (hl.get("hard_problem_open", 0) == 1)
    return bool(eff and cc and tuned and no_cure), {
        "efficacy_zero": eff, "no_consciousness_claim": cc,
        "no_tuned_constants": tuned, "no_cure_or_hard_problem_open": no_cure,
    }


def _preds(res):
    """Collect any pre-registered sign-only predictions, whatever the module calls them."""
    for key in ("preregistered_results", "preregistered", "predictions"):
        pr = res.get(key)
        if isinstance(pr, dict) and pr:
            out = {}
            for k, v in pr.items():
                out[k] = v.get("status") if isinstance(v, dict) else v
            return out
    return {}


def main():
    rows = []
    all_ok = True
    n_conf = n_ref = 0
    for tag, rid, script, resfile, frozen_sha in MODULES:
        path = os.path.join(HERE, script)
        # 1) fresh subprocess re-run -> module rewrites results.json + expected_*.json
        proc = subprocess.run([sys.executable, path], cwd=HERE,
                              capture_output=True, text=True)
        ran_ok = (proc.returncode == 0)
        # 2) sha256 the WRITTEN file vs the orchestrator's FROZEN constant
        respath = os.path.join(HERE, resfile)
        got = sha256_file(respath) if os.path.exists(respath) else None
        repro = (got == frozen_sha)
        # 3) load the written result for invariant + honesty + prediction checks
        try:
            res = json.load(open(respath, encoding="utf-8"))
        except Exception:
            res = {}
        inv_ok, inv_detail = invariants_ok(res)
        hon_ok, hon_detail = honesty_ok(res)
        preds = _preds(res)
        n_conf += sum(s == "CONFIRMED" for s in preds.values())
        n_ref += sum(s == "REFUTED" for s in preds.values())
        ok = ran_ok and repro and inv_ok and hon_ok
        all_ok = all_ok and ok
        rows.append(dict(tag=tag, roadmap_id=rid, module=script, results_file=resfile,
                         ran_ok=ran_ok, sha256=got, frozen_sha256=frozen_sha,
                         reproduced=repro, engine_invariants_ok=inv_ok,
                         engine_invariants=inv_detail, honesty_ledger_ok=hon_ok,
                         honesty_ledger=hon_detail, preregistered=preds))
        print(f"  {tag:<8} [{rid}] {script:<34} ran={ran_ok} repro={repro} "
              f"engine={inv_ok} honest={hon_ok}")

    eng = engine_file_ok()
    all_ok = all_ok and eng
    gate = {
        "suite": "transdiagnostic fault-axis atlas (T1a schizophrenia, T2a epilepsy, "
                 "E0 plasticity/consolidation layer, T1b depression/TRD, E2 state-switching "
                 "layer, T2b bipolar)",
        "roadmap": "RESEARCH_ROADMAP_post_autism_adhd.md",
        "n_modules": len(MODULES),
        "engine_file_sha256_ok": eng,
        "engine_file_sha256": ENGINE_FILE_SHA,
        "engine_tree_frozen": ENGINE_TREE_FROZEN,
        "regression_guard": "sha256 of each written results.json vs frozen constants held "
                            "in run_all_atlas.py (modules rewrite their own expected_*.json "
                            "each run, so the orchestrator's constants are the true guard)",
        "modules": rows,
        "preregistered_tally": {"confirmed": n_conf, "refuted": n_ref,
                                "note": "refutations are findings, not gate failures"},
        "all_pass": bool(all_ok),
        "gate_meaning": "every atlas module re-runs from scratch and reproduces bit-for-bit "
                        "against the frozen constants, the engine is byte-unchanged (file sha "
                        "and frozen tree 0fbf4988...), and the honesty ledger holds (efficacy=0, "
                        "no cure / hard-problem-open, no tuned constants, no consciousness "
                        "claim). The gate certifies reproducibility and discipline; the "
                        "scientific verdicts live in the module results and the chapter HTML.",
    }
    json.dump(gate, open(os.path.join(HERE, "gate_atlas.json"), "w"),
              indent=1, ensure_ascii=False)
    print(f"\n  engine file byte-unchanged: {eng}")
    print(f"  pre-registered tally: {n_conf} CONFIRMED, {n_ref} REFUTED (refutations are findings)")
    print(f"  ATLAS GATE ALL PASS: {all_ok}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
