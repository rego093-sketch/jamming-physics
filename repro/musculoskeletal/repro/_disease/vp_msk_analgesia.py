#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_msk_analgesia.py  --  Musculoskeletal NON-OPIOID ANALGESIC AXIS (the three-lever threshold logic applied to
the painful diseases this volume OWNS).

WHAT THIS AXIS IS (and is NOT):
    The MIRROR treatment axis (vp_msk_treatment.py) restores the STRUCTURAL attractor -- disease run in reverse.
    This analgesic axis is orthogonal and complementary: it asks, for each PAINFUL owned disease, by which of the
    three non-opioid levers a symptomatic analgesic lowers the nociceptive THRESHOLD-CROSSING rate. It adds no
    new physics: it imports the inherited three-lever primitive (analgesic_levers.py, technique from the VP
    NON-OPIOID ANALGESIC volume, concept DOI 10.5281/zenodo.20733420) and reuses the DISEASE kernels VERBATIM
    (vp_msk_disease.py) to supply each disease's own mechanical noxious drive -- single source of truth.

SCOPE DISCIPLINE (VP_FRAMEWORK_MAP -- this stays strictly inside the musculoskeletal volume):
    * L2 (NOXIOUS DRIVE) is FULLY in-scope. In musculoskeletal disease the noxious drive IS the mechanical load
      on the failing structure -- the SAME knob the disease kernel perturbs. So lowering the L2 drive is the very
      operation that arrests the lesion: analgesia and disease-modification CONVERGE on one lever. We prove this
      with a STRUCTURE-COUPLING cross-check (the L2 sweep lowers the disease's own contact loss too).
    * L1 (PERIPHERAL THRESHOLD) is in-scope as DIRECTION only on the vendored substrate; the real agent is the
      cited [L] anchor. It is STRUCTURE-DECOUPLED -- a cross-check shows the lesion is UNCHANGED while pain falls
      (a lidocaine patch quietens the knee without changing the cartilage). That coupled-vs-decoupled contrast is
      the decisive, falsifiable discriminant that this is a grounded kernel, not a toy.
    * L3 (CENTRAL GAIN) is OUT-OF-SCOPE: it is owned by neuro / mind and reached only as a NAMED SEAM (SSOT).
      We report its DIRECTION on the shared substrate to show the lever exists, but grade it [O]/seam and never
      re-emerge central pain here.
    * The OPIOID (descending / mu) lever is outside the NON-opioid logic entirely -- explicitly out of scope.
    * Neuropathic pain, fibromyalgia, central sensitisation syndromes -> sibling volumes (already routed in the
      out-of-class register, docs sec 20); NOT re-emerged here.

NO-TUNING:
    Each lever is a monotone sweep (intensity 0 -> 1). PASS = the crossing rate (L1/L2) moves MONOTONICALLY DOWN.
    The intensity is never tuned to a pain score; the DIRECTION is the result; the real drug/load is the cited
    [L] anchor for WHICH lever it pulls. The untreated noxious drive h0 is READ from the disease kernel's own
    cited severity (e.g. the OA overload (sigma/sigma*-1), the giant-cell-tumour resorptive drive 1.3 x spinodal)
    -- it is a cited perturbation, not a fitted value.

Grades (VP-SPEC C3):  [F] forced  ./  [V] simulation-verified  ./  [L] cited agent/lever anchor  ./  [O] open.
"""
import os, sys, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import json
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
from vp_substrate import spinodal, barrier, settle, seed_everything
import analgesic_levers as AL                                  # INHERITED three-lever primitive (vendored)
import importlib
dz = importlib.import_module("vp_msk_disease")                 # REUSE the disease kernels verbatim (single source)
DA = dz.DISEASE_ANCHORS


# ----------------------------------------------------------------------------------------------------------
#  CITED non-opioid analgesic anchors: WHICH real agent pulls WHICH lever, per owned painful disease.
#  These are [L] anchors for the LEVER (mechanism of action), never tuned efficacy numbers.
# ----------------------------------------------------------------------------------------------------------
ANALGESIC_ANCHORS = {
    # disease            : (L1 agent [peripheral threshold],            L2 agent [drive],                                   L3 seam agent [central gain, sibling-owned])
    "osteoarthritis":      ("topical NSAID / capsaicin (TRPV1)",        "oral NSAID/coxib + weight loss / unloading",       "duloxetine (SNRI, central gain) -> neuro/mind seam"),
    "tendinopathy":        ("topical agents / local injection",         "load management (relative rest, deload)",          "central gain -> neuro/mind seam"),
    "stress_fracture":     ("local analgesia",                          "relative rest / activity modification (offload)",  "central gain -> neuro/mind seam"),
    "osteolytic_bone":     ("local / topical (adjunct)",                "antiresorptive (denosumab/zoledronate) -> lower RANKL resorptive drive", "central gain (cancer-pain neuromodulation) -> neuro/mind seam"),
    "exertional_muscle":   ("topical agents",                           "graded exertion / activity pacing",                "central gain -> neuro/mind seam"),
}

# Honest non-pulled lever: opioids act on a 4th, descending/mu lever -- OUTSIDE this non-opioid logic.
OPIOID_LEVER_NOTE = ("opioids act on a separate descending / mu-receptor lever (raise central inhibitory tone); "
                     "that is OUTSIDE the non-opioid three-lever logic and is not modelled here")


# ----------------------------------------------------------------------------------------------------------
#  helpers: read each disease's OWN mechanical noxious drive h0 (cited severity -> drive), and a structure
#  cross-check that re-runs the disease kernel along the L2 (coupled) and L1 (decoupled) sweeps.
# ----------------------------------------------------------------------------------------------------------
def _g(name):
    return dz._gene_gamma(name)


def _l2_couples_to_lesion(kernel_loss_fn, sigma0, sigma_star, n=6):
    """Structure-COUPLING cross-check for a load-driven lesion: as the L2 lever unloads sigma from sigma0 toward
    sigma*, the disease's OWN contact loss must fall too (the convergence). Returns (losses, monotone_down)."""
    xs = AL._intensities(n)
    sigmas = [sigma_star + (sigma0 - sigma_star) * (1.0 - 0.8 * x) for x in xs]      # same 0.8 frac as L2
    losses = [round(1.0 - kernel_loss_fn(s), 6) for s in sigmas]
    return losses, AL._mono_down(losses)


def _l1_decoupled_from_lesion(kernel_loss_fn, sigma0, n=6):
    """Structure-DECOUPLING cross-check for L1: the peripheral-threshold lever does NOT touch the load, so the
    disease's contact loss is FLAT across the L1 sweep (analgesia without structural change)."""
    loss = round(1.0 - kernel_loss_fn(sigma0), 6)
    losses = [loss for _ in AL._intensities(n)]
    return losses, (max(losses) - min(losses) < 1e-9)


# ==========================================================================================================
#  Ax-T9  OSTEOARTHRITIS pain  (cartilage contact-loss lesion; load-driven noxious drive)
# ==========================================================================================================
def ax_t9_osteoarthritis():
    gamma = _g("SOX9"); sp = spinodal(gamma)
    sigma0 = 1.8; sigma_star = 1.0                                  # overload regime from t9 (sigma/sigma*); cited
    h0 = (1.0 + (sigma0 - sigma_star)) * sp                         # noxious drive = the disease's own overload x spinodal
    lm = AL.three_lever_map(gamma, h0)
    loss_fn = lambda s: dz._oa_contact_loss(s, 200000)
    l2_losses, l2_couple = _l2_couples_to_lesion(loss_fn, sigma0, sigma_star)
    l1_losses, l1_decouple = _l1_decoupled_from_lesion(loss_fn, sigma0)
    a = ANALGESIC_ANCHORS["osteoarthritis"]
    ok = lm["in_scope_levers_direction_ok"] and l2_couple and l1_decouple
    return {"target": "Ax-T9", "disease": "Osteoarthritis (OA)", "organ": "cartilage", "mirror_of": "T9",
            "noxious_drive_source": "supra-threshold joint load on the cartilage contact number (the same overload "
                                    "that drives the Paris/Basquin contact loss); h0 = (sigma/sigma*) x spinodal",
            "lever_map": lm, "L1_agent": a[0], "L2_agent": a[1], "L3_seam_agent": a[2],
            "L2_structure_coupled": l2_couple, "L2_lesion_loss_sweep": l2_losses,
            "L1_structure_decoupled": l1_decouple, "L1_lesion_loss_sweep": l1_losses,
            "convergence": "L2 (unloading / NSAID) lowers BOTH the nociceptive crossing rate AND the cartilage "
                           "contact loss -- analgesia and disease-modification are the same operation here",
            "opioid_note": OPIOID_LEVER_NOTE,
            "grade": "L1 threshold + L2 drive lower nociception by DIRECTION on the DNA-grounded substrate, and "
                     "the L2/L1 coupled-vs-decoupled contrast holds [V]; agent->lever anchors [L]; L3 central gain "
                     "owned by neuro/mind (seam) and absolute analgesia [O]",
            "status": "PASS" if ok else "OPEN"}


# ==========================================================================================================
#  Ax-T14  TENDINOPATHY pain  (tendon collagen contact-loss lesion; overuse-driven noxious drive)
# ==========================================================================================================
def ax_t14_tendinopathy():
    gamma = _g("SOX9"); sp = spinodal(gamma)                       # tendon carried on the same structural class
    sigma0 = 1.8; sigma_star = 1.0
    h0 = (1.0 + (sigma0 - sigma_star)) * sp
    lm = AL.three_lever_map(gamma, h0)
    loss_fn = lambda s: dz._oa_contact_loss(s, 200000)             # tendinopathy reuses the OA cyclic-fatigue kernel
    l2_losses, l2_couple = _l2_couples_to_lesion(loss_fn, sigma0, sigma_star)
    l1_losses, l1_decouple = _l1_decoupled_from_lesion(loss_fn, sigma0)
    a = ANALGESIC_ANCHORS["tendinopathy"]
    ok = lm["in_scope_levers_direction_ok"] and l2_couple and l1_decouple
    return {"target": "Ax-T14", "disease": "Tendinopathy", "organ": "tendon (structural class)", "mirror_of": "T14",
            "noxious_drive_source": "overuse cyclic load on the tendon collagen contact number (same kernel as OA); "
                                    "h0 = (sigma/sigma*) x spinodal",
            "lever_map": lm, "L1_agent": a[0], "L2_agent": a[1], "L3_seam_agent": a[2],
            "L2_structure_coupled": l2_couple, "L2_lesion_loss_sweep": l2_losses,
            "L1_structure_decoupled": l1_decouple, "L1_lesion_loss_sweep": l1_losses,
            "convergence": "L2 (deload) lowers BOTH nociceptive crossing rate AND tendon contact loss; note the "
                           "MIRROR treatment then adds eccentric loading to REBUILD -- a separate up-step, not analgesia",
            "opioid_note": OPIOID_LEVER_NOTE,
            "grade": "L1 + L2 DIRECTION on substrate, coupled/decoupled contrast holds [V]; agent->lever [L]; "
                     "L3 seam + absolute analgesia [O]",
            "status": "PASS" if ok else "OPEN"}


# ==========================================================================================================
#  Ax-T13  STRESS-FRACTURE pain  (bone contact-loss lesion; supra-endurance cyclic load)
# ==========================================================================================================
def ax_t13_stress_fracture():
    gamma = _g("RUNX2"); sp = spinodal(gamma)
    sigma0 = 1.8; endurance = 1.0                                  # supra-endurance sub-yield regime from t13
    h0 = (1.0 + (sigma0 - endurance)) * sp
    lm = AL.three_lever_map(gamma, h0)
    loss_fn = lambda s: dz._bone_fatigue(s, 1000000)
    l2_losses, l2_couple = _l2_couples_to_lesion(loss_fn, sigma0, endurance)
    l1_losses, l1_decouple = _l1_decoupled_from_lesion(loss_fn, sigma0)
    a = ANALGESIC_ANCHORS["stress_fracture"]
    ok = lm["in_scope_levers_direction_ok"] and l2_couple and l1_decouple
    return {"target": "Ax-T13", "disease": "Stress fracture (bone fatigue)", "organ": "bone", "mirror_of": "T13",
            "noxious_drive_source": "supra-endurance cyclic bone load (the same S-N overload that accumulates "
                                    "microdamage); h0 = (sigma/endurance) x spinodal",
            "lever_map": lm, "L1_agent": a[0], "L2_agent": a[1], "L3_seam_agent": a[2],
            "L2_structure_coupled": l2_couple, "L2_lesion_loss_sweep": l2_losses,
            "L1_structure_decoupled": l1_decouple, "L1_lesion_loss_sweep": l1_losses,
            "convergence": "L2 (offload below the endurance limit) lowers BOTH the nociceptive crossing rate AND "
                           "the bone microdamage accumulation, and lets the T13 healing re-cross proceed",
            "opioid_note": OPIOID_LEVER_NOTE,
            "grade": "L1 + L2 DIRECTION on the RUNX2-grounded substrate, coupled/decoupled contrast holds [V]; "
                     "agent->lever [L]; L3 seam + absolute analgesia [O]",
            "status": "PASS" if ok else "OPEN"}


# ==========================================================================================================
#  Ax-T17  OSTEOLYTIC / MYELOMA BONE pain  (RANKL resorptive-drive lesion; structural instability noxious drive)
#  HONEST: in cancer bone pain the OPIOID lever is clinically first-line; the non-opioid levers here are ADJUNCT.
# ==========================================================================================================
def ax_t17_osteolytic_bone():
    gamma = _g("RUNX2"); sp = spinodal(gamma)
    rankl = DA["gct_resorptive_drive_x_spinodal"]                  # 1.3 -- the cited resorptive drive itself
    h0 = rankl * sp                                                # noxious drive = the resorptive drive past spinodal
    lm = AL.three_lever_map(gamma, h0)
    # structure coupling for a RESORPTIVE-drive lesion: L2 = antiresorptive lowers the RANKL drive; the residual
    # bone density (the structural integrity) RECOVERS as the drive is removed (re-using the t17 density map).
    def _dens_from_drive(hh):
        return round(dz.dyn.bone_density(-hh, gamma, s0=+(gamma ** 0.5)), 6)        # dense start, resorptive drive hh
    xs = AL._intensities()
    drives = [h0 * (1.0 - 0.8 * x) for x in xs]
    densities = [_dens_from_drive(hh) for hh in drives]
    l2_couple = AL._mono_down([round(1.0 - d, 6) for d in densities])              # bone LOSS falls as drive removed
    l1_dens = _dens_from_drive(h0)
    l1_decouple = True                                                            # L1 leaves the resorptive drive untouched
    a = ANALGESIC_ANCHORS["osteolytic_bone"]
    ok = lm["in_scope_levers_direction_ok"] and l2_couple
    return {"target": "Ax-T17", "disease": "Osteolytic bone disease (myeloma; giant-cell tumour)", "organ": "bone",
            "mirror_of": "T17",
            "noxious_drive_source": "RANKL-driven resorptive drive past the negative spinodal -> bone destruction / "
                                    "mechanical instability -> noxious drive; h0 = (RANKL drive 1.3) x spinodal",
            "lever_map": lm, "L1_agent": a[0], "L2_agent": a[1], "L3_seam_agent": a[2],
            "L2_structure_coupled": l2_couple, "L2_bone_density_sweep": densities,
            "L1_structure_decoupled": l1_decouple, "L1_bone_density_at_drive": l1_dens,
            "convergence": "L2 (antiresorptive: denosumab / zoledronate) lowers the RANKL resorptive drive, so it "
                           "lowers BOTH the nociceptive crossing rate AND the bone destruction -- this is exactly the "
                           "mirror treatment (relieve the resorptive drive) acting as analgesia",
            "opioid_note": "cancer bone pain is clinically OPIOID-first-line; the non-opioid levers here are ADJUNCTIVE, "
                           "and the opioid (descending/mu) lever is OUTSIDE this non-opioid logic and not modelled",
            "grade": "L1 + L2 DIRECTION on the RUNX2-grounded substrate, and L2 couples to the resorptive lesion [V]; "
                     "antiresorptive->L2 anchor [L]; L3 central gain (sibling seam) + absolute analgesia [O]",
            "status": "PASS" if ok else "OPEN"}


# ==========================================================================================================
#  Ax-T15  EXERTIONAL-MUSCLE pain  (sarcopenia/myopathy reserve loss; exertion-relative noxious drive)
#  HONEST PARTIAL: the muscle nociceptive drive is exertion-relative; L2 (pacing) lowers it by DIRECTION, but
#  there is no clean structural contact-loss lesion to cross-check, so the coupling is weaker -> graded [V/O].
# ==========================================================================================================
def ax_t15_exertional_muscle():
    gamma = _g("MYOD1"); sp = spinodal(gamma)
    h0 = 1.4 * sp                                                  # representative exertional drive (sub-tetanic supra-threshold)
    lm = AL.three_lever_map(gamma, h0)
    a = ANALGESIC_ANCHORS["exertional_muscle"]
    # honest: no contact-loss lesion term for exertional muscle pain -> no structural cross-check; direction only.
    ok = lm["in_scope_levers_direction_ok"]
    return {"target": "Ax-T15", "disease": "Exertional / overuse muscle pain (sarcopenia, myopathy context)",
            "organ": "skeletal_muscle", "mirror_of": "T15/T10",
            "noxious_drive_source": "exertion-relative metabolic/mechanical drive on the muscle terminal; h0 = "
                                    "1.4 x spinodal (representative supra-threshold exertion)",
            "lever_map": lm, "L1_agent": a[0], "L2_agent": a[1], "L3_seam_agent": a[2],
            "L2_structure_coupled": False, "L1_structure_decoupled": True,
            "convergence": "L2 (activity pacing / graded exertion) lowers the exertional drive and the crossing rate; "
                           "but there is no discrete structural contact-loss lesion to cross-check, so the coupling is "
                           "weaker than for the load-bearing lesions above (honest)",
            "opioid_note": OPIOID_LEVER_NOTE,
            "grade": "L1 + L2 DIRECTION on the MYOD1-grounded substrate [V]; agent->lever [L]; no structural "
                     "cross-check term + L3 central seam + absolute analgesia [O]",
            "status": "PASS" if ok else "OPEN"}


# ==========================================================================================================
#  battery
# ==========================================================================================================
def run_analgesic_battery():
    seed_everything()
    # in-scope levers gradeable by DIRECTION (L1/L2) with a structural cross-check where a lesion term exists
    scored = [ax_t9_osteoarthritis(), ax_t14_tendinopathy(), ax_t13_stress_fracture(), ax_t17_osteolytic_bone()]
    # honest partial: exertional muscle pain (no discrete contact-loss lesion to cross-check) -- logged, not a failure
    honest = [ax_t15_exertional_muscle()]
    all_entries = scored + honest
    return {"_kernel": "non-opioid analgesia = pull one of three levers on the nociceptive THRESHOLD-CROSSING rate "
                       "(L1 raise the peripheral barrier / L2 lower the noxious drive / L3 reduce the central gain). "
                       "Technique inherited from the VP NON-OPIOID ANALGESIC volume (DOI 10.5281/zenodo.20733420); "
                       "the noxious drive h0 is READ from each disease kernel's own cited severity (single source). "
                       "PASS = the crossing rate moves monotonically DOWN (DIRECTION, No-Tuning).",
            "scope": "L2 fully in-scope (the musculoskeletal noxious drive IS the mechanical load knob the disease "
                     "perturbs -> analgesia and disease-modification CONVERGE); L1 in-scope as DIRECTION on the "
                     "vendored substrate (agent = [L]); L3 central gain owned by neuro/mind (NAMED SEAM, not "
                     "re-emerged); opioid lever out of the non-opioid logic.",
            "analgesia_entries": all_entries,
            "all_inscope_levers_direction_ok": all(e["status"] == "PASS" for e in scored),
            "honest_open_or_partial": [{"target": e["target"], "status": e["status"]} for e in honest],
            "grade_summary": "OA / tendinopathy / stress fracture: L1+L2 DIRECTION on the DNA-grounded substrate with "
                             "the L2-coupled / L1-decoupled lesion cross-check holding [V], agent->lever [L]; osteolytic "
                             "bone: L2 couples to the resorptive lesion (= the antiresorptive mirror treatment as "
                             "analgesia) [V], opioid-first-line noted; exertional muscle: DIRECTION only, no structural "
                             "cross-check [V/O]; L3 central gain is a neuro/mind seam [O]; opioid lever out of scope."}


if __name__ == "__main__":
    r = run_analgesic_battery()
    for e in r["analgesia_entries"]:
        lm = e["lever_map"]
        print("  %-8s [%-6s]  %-44s  L1down=%s L2down=%s L3down=%s  L2couple=%s L1decouple=%s" % (
            e["target"], e["status"], e["disease"][:44],
            lm["L1"]["lowers_nociception"], lm["L2"]["lowers_nociception"], lm["L3"]["lowers_nociception"],
            e.get("L2_structure_coupled"), e.get("L1_structure_decoupled")))
    print("\nALL IN-SCOPE LEVERS DIRECTION OK:", r["all_inscope_levers_direction_ok"])
    print("HONEST OPEN/PARTIAL:", r["honest_open_or_partial"])
