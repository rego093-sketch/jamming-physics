#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
treatment.py  --  ROOT-CAUSE therapy dossier (the user's explicit ask: more FUNDAMENTAL treatments).

UNIFYING PRINCIPLE (derived from the same R19 substrate as the pathology). If disease is a failure of a
defended loop / instrument, then a ROOT-CAUSE therapy is the INVERSE operation on the substrate:
    (1) RESTORE LOOP GAIN  -> raise g_eff -> re-deepen the basin -> reset the drifted setpoint
    (2) RAISE THE ATTRACTOR BARRIER  -> protect the healthy state from crossing (neuroprotection)
    (3) RE-ENGAGE THE ERROR SIGNAL  -> re-close a broken feedback loop (e.g. defocus signal)
    (4) REPAIR / REGENERATE THE INSTRUMENT  -> rebuild the failed transducer or optic
    (5) LOWER A RUN-AWAY LOOP GAIN  -> reduce g on a pathological positive-feedback loop (inflammation)
A SYMPTOMATIC therapy instead bypasses the loop (corrects the output) without touching g -- it leaves
the substrate failure in place. This file classifies each current/emerging therapy on that axis and
grades the EVIDENCE honestly (approved / phase / preclinical / contested), citing the literature.

This is a STRUCTURED-DATA dossier (no fitted numbers); the only computed object is the substrate-level
"restoration" demo: restoring a fraction of lost loop gain re-grows the barrier (inverse of pathology).

Grades: mechanism mapped to substrate [V-structure]; clinical evidence level cited [L]; where a target is
unproven or contested we say so [contested] -- silent optimism is a C3 violation.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier

THERAPIES = [
    {"disease": "glaucoma",
     "root_cause": "outflow-conductance arm of the IOP loop fails (TM stiffening/ECM); RGC death attractor",
     "root_therapies": [
        {"name": "Rho-kinase (ROCK) inhibitors -- netarsudil (US), ripasudil/fasudil (JP)",
         "substrate_action": "(1)+(2): relax TM / clear ECM -> RESTORE conventional outflow conductance (resets the IOP setpoint at its source) AND IOP-independent RGC neuroprotection (raises the death-attractor barrier: up-Bcl-2, down-caspase-3, axon regrowth)",
         "evidence": "approved (netarsudil FDA; ripasudil JP/CN); neuroprotection preclinical",
         "ref": "J Exp Pharmacol S259297; MDPI Biomedicines 13:1871 2025; PMC11583991"},
        {"name": "TM regeneration / stem-cell repopulation; RGC neuroprotection & optic-nerve regeneration",
         "substrate_action": "(4)+(2): rebuild the outflow instrument and protect/repair the RGC attractor directly",
         "evidence": "preclinical / early trials", "ref": "Acta Neuropathol Commun 2024 40478-024-01859-z"}],
     "symptomatic_contrast": "prostaglandin analogues / aqueous suppressants / trabeculectomy lower IOP but bypass the diseased TM"},

    {"disease": "refractive error (myopia)",
     "root_cause": "emmetropization defocus-feedback loop broken -> axial-length run-away",
     "root_therapies": [
        {"name": "Peripheral myopic-defocus optics (DIMS spectacles, orthokeratology) + low-dose atropine (0.01-0.05%) + outdoor bright light (retinal dopamine) + repeated low-level red light (650 nm)",
         "substrate_action": "(3): RE-ENGAGE the defocus error signal / dopamine arm -> choroidal thickening -> halt axial elongation (slows progression >=50%); not merely optical correction",
         "evidence": "RCT-supported (>=50% slowing); IMI 2025 consensus; long-term safety still accruing",
         "ref": "IMI 2025 Digest; Ophthalmology S016164202400318X 2024; tvst 11.10.33"}],
     "symptomatic_contrast": "single-vision glasses / LASIK correct the focal error but leave the growth loop uncorrected"},

    {"disease": "presbycusis / noise-induced hearing loss",
     "root_cause": "transducer (hair cell) + active amplifier (OHC/prestin, Hopf mu) + synapse (synaptopathy) lost",
     "root_therapies": [
        {"name": "Hair-cell regeneration (ATOH1 transfer; Notch/Wnt modulation); prestin/OHC restoration; cochlear-synapse repair (NT-3/BDNF neurotrophins); OTOF gene therapy for DFNB9",
         "substrate_action": "(4)+(1): regenerate the transducer and push the amplifier mu BACK toward criticality (restore the F^{1/3} gain); re-grow the IHC-SGN synapse",
         "evidence": "OTOF gene therapy restored hearing in children (clinical, 2024); ATOH1-regenerated hair cells remain IMMATURE / thresholds not yet restored [contested for acquired SNHL]; synaptopathy repair preclinical",
         "ref": "PLoS One 0102077; Hum Gene Ther 2025.013; Front Neurosci 2023:1177791"}],
     "symptomatic_contrast": "hearing aids / cochlear implants substitute for the transducer but do not regrow it"},

    {"disease": "age-related macular degeneration (geographic atrophy)",
     "root_cause": "complement alternative-pathway regulation lost -> inflammatory positive-feedback loop gain rises -> RPE/photoreceptor atrophy",
     "root_therapies": [
        {"name": "Complement inhibitors -- pegcetacoplan (C3, Syfovre), avacincaptad pegol (C5, Izervay); MAC inhibition gene therapy (CD59)",
         "substrate_action": "(5): LOWER the run-away complement loop gain at C3/C5 -> slow atrophy expansion (~14-27% lesion-growth reduction)",
         "evidence": "FDA-approved 2023 (anatomic endpoint). HONEST CAVEAT: phase-3 showed NO functional visual-acuity benefit yet; exudation risk ~7-12% [partial]",
         "ref": "Apellis OAKS/DERBY; GATHER1/2; AJO S0002-9394(24)00076-X; Front Pharmacol 2024:1410172"},
        {"name": "RPE cell replacement (stem-cell-derived); visual-cycle modulators; photobiomodulation",
         "substrate_action": "(4): rebuild the RPE instrument", "evidence": "trials ongoing", "ref": "Front Pharmacol 2024:1410172"}],
     "symptomatic_contrast": "for WET AMD, anti-VEGF treats neovascular leakage (downstream) but not the complement driver"},

    {"disease": "cataract",
     "root_cause": "crystallins cross the aggregation spinodal (chaperone capacity overwhelmed) -> light scatter",
     "root_therapies": [
        {"name": "Pharmacological chaperones / aggregation reversal -- oxysterols (lanosterol, 25-hydroxycholesterol/VP1-001), non-sterol alpha-crystallin ligands; lanosterol-synthase mRNA-LNP; antioxidants",
         "substrate_action": "(1)/(4): raise the solubility barrier / boost alpha-crystallin chaperone capacity to dissolve aggregates",
         "evidence": "CONTESTED: Nature 2015 & Science 2015 reported reversal, but Daszynski 2019 (Sci Rep) and others FAILED to replicate disaggregation in cultured lenses -> efficacy unproven; surgery remains standard",
         "ref": "Nature 14650 2015; Science 350:674 2015; Sci Rep 2019 44676; PMC12474983 (mRNA-LNP)"}],
     "substrate_note": "aggregation is a near-IRREVERSIBLE spinodal crossing (huge reverse barrier) -- this is WHY pharmacological reversal is hard; prevention (UV/oxidation control) targets the forward crossing",
     "symptomatic_contrast": "phacoemulsification + IOL replaces the lens instrument (definitive) but is not molecular reversal"},

    {"disease": "diabetic retinopathy",
     "root_cause": "chronic hyperglycemia -> retinal microvascular damage -> ischemia/VEGF neovascular attractor",
     "root_therapies": [
        {"name": "Glycemic control (treats the systemic driver) + anti-VEGF / panretinal photocoagulation for the neovascular arm",
         "substrate_action": "(1) reset the systemic metabolic setpoint (root, cross-ref thermometabolic); anti-VEGF blocks the downstream attractor",
         "evidence": "glycemic control root-causal (cited); anti-VEGF approved for the complication",
         "ref": "cross-ref thermometabolic/diabetes package"}],
     "symptomatic_contrast": "anti-VEGF/laser manage the complication; glycemia is the root"},

    {"disease": "BPPV / vertigo",
     "root_cause": "otoconia displaced into a semicircular canal -> false angular-velocity signal",
     "root_therapies": [
        {"name": "Canalith-repositioning (Epley / Semont maneuver)",
         "substrate_action": "(4): mechanically return the otoconia to the utricle -> removes the false signal at its source -- already a ROOT-CAUSE, instrument-level fix",
         "evidence": "established standard of care (high efficacy)", "ref": "vestibular physiology; standard ENT practice"}],
     "symptomatic_contrast": "vestibular suppressants dull the symptom but leave the displaced otoconia"},
]


def restoration_demo(gamma=1.511, lost_fraction=0.6, restored_fraction=0.8):
    """Substrate-level inverse of pathology: a therapy that restores a fraction of lost loop gain
    re-grows the barrier. d_after = lost*(1-restored). Deterministic; shows the direction, not an absolute."""
    g = float(gamma); B0 = barrier(g)
    d_disease = min(max(lost_fraction, 0.0), 1.0)
    d_after = d_disease * (1.0 - min(max(restored_fraction, 0.0), 1.0))
    B_disease = B0 * (1.0 - d_disease) ** 2
    B_after = B0 * (1.0 - d_after) ** 2
    return dict(healthy_barrier=round(B0, 6), disease_barrier=round(B_disease, 6),
                treated_barrier=round(B_after, 6),
                recovered_fraction=round((B_after - B_disease) / (B0 - B_disease + 1e-12), 4),
                note="restoring loop gain re-deepens the basin (inverse of the pathology collapse) [V-direction]")


def status():
    demo = restoration_demo()
    classes = sorted({a["substrate_action"].split(":")[0].strip()
                      for t in THERAPIES for a in t["root_therapies"]})
    return {
        "principle": "root-cause therapy = inverse substrate operation: restore loop gain / raise attractor barrier / re-engage error signal / repair instrument / lower run-away loop gain",
        "action_classes_present": classes,
        "restoration_demo": demo,
        "therapies": THERAPIES,
        "honest_status": "mechanisms mapped to the R19 substrate [V-structure]; clinical evidence cited with level; contested/partial items flagged (AMD no functional gain yet; cataract reversal unreplicated; ATOH1 cells immature)",
        "grades": "substrate mapping [V] / clinical evidence [L] / contested where stated",
    }


if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
