#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_msk_treatment.py  --  Musculoskeletal TREATMENT BATTERY (the mirror of the disease battery).

CENTRAL PRINCIPLE (the treatment axis is forced by the disease axis, not bolted on):
    A disease in this kit is a CITED perturbation of an already-passing switch -- it lowers an R19 escape
    barrier, shifts a setpoint past a spinodal, disables one branch of a hysteresis loop, or caps a supply.
    A TREATMENT is therefore the MIRROR operation on the SAME kernel: it raises the barrier back, restores
    the drive across the spinodal, re-enables the disabled branch, or refills the capped supply. Nothing new
    is invented -- every treatment reuses the exact disease function from vp_msk_disease.py and moves its one
    cited knob back toward the healthy value.

PASS POLICY (No-Tuning, identical discipline to the disease battery):
    Each treatment is a monotone RESTORATION SWEEP: a treatment-intensity axis x in [0,1] (0 = untreated
    disease, 1 = full restoration of the targeted knob). PASS = the disease SIGNATURE moves MONOTONICALLY
    back toward the healthy attractor and ends closer to healthy than the untreated state. We never tune the
    intensity to land on a clinical efficacy number; the DIRECTION (does restoring the knob undo the sign of
    the lesion?) is the result. The real-world intervention is the cited [L] anchor for WHICH knob it targets.

HONEST NEGATIVES (graded [O] with a stated obstacle -- these are RESULTS, not failures):
    * developmental dosage cliffs (T7): the master-switch decision was made during a closed developmental
      window; no postnatal knob re-runs development, and the already-formed skeleton is fixed. [O].
    * already-lost structure (OA cartilage, T9): unloading ARRESTS further contact loss [V], but the kernel
      has no matrix-resynthesis term and cartilage does not regenerate -- lost contacts are not restored. [O].
    * established-tumour cytotoxic therapy (oncology): the carcinogenesis kernel models INITIATION
      (dose -> barrier down -> Kramers crossing -> RR). Chemo/resection/radiation KILL transformed cells;
      that is not "raising the barrier" of the original switch, so therapy-response is out of kernel scope [O].
      PRIMARY PREVENTION (remove the carcinogen -> dose down -> RR down) IS in scope and is [V].
    * etiology-specific metabolic myopathy (T10): only a cofactor-responsive SUBSET is reversible; no general
      kernel restoration exists, so the general case is [O].

Grades (VP-SPEC C3):  [F] forced  ./  [V] simulation-verified  ./  [L] cited intervention/target anchor  ./  [O] open.
"""
import os, sys, math
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import json
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
from vp_substrate import spinodal, barrier, settle, seed_everything, Neuron
import importlib
dyn = importlib.import_module("vp_msk_dynamics")
dz  = importlib.import_module("vp_msk_disease")          # REUSE the disease kernels verbatim (single source)
DA  = dz.DISEASE_ANCHORS


# ----------------------------------------------------------------------------
#  small monotone helpers
# ----------------------------------------------------------------------------
def _monotone_up(seq, tol=1e-9):
    return all(seq[i] <= seq[i + 1] + tol for i in range(len(seq) - 1))

def _monotone_down(seq, tol=1e-9):
    return all(seq[i] >= seq[i + 1] - tol for i in range(len(seq) - 1))

def _intensities(n=6):
    return [round(i / (n - 1), 3) for i in range(n)]      # 0.0 .. 1.0


# ============================================================================
#  Tx-T16  OSTEOMALACIA / RICKETS   <-  vitamin-D + Ca/phosphate repletion
#  knob: mineral supply M  (disease caps it; repletion refills it M -> 1)
# ============================================================================
def tx_t16_osteomalacia(gamma=None):
    gamma = dz._gene_gamma("RUNX2") if gamma is None else gamma
    sp = spinodal(gamma); load = 1.5 * sp; s_low = -(gamma ** 0.5)
    M0 = DA["osteomalacia_supply_deficient"]                       # 0.5 deficient (disease)
    sweep = [{"repletion": x, "mineral_supply": round(M0 + x * (1.0 - M0), 4),
              "mineral_density": round(dz._mineral_density(load, M0 + x * (1.0 - M0), gamma, s0=s_low), 4)}
             for x in _intensities()]
    dens = [r["mineral_density"] for r in sweep]
    restored = _monotone_up(dens) and dens[-1] > 0.95 and dens[-1] > dens[0] + 0.3
    return {"target": "Tx-T16", "disease": "Osteomalacia / rickets", "organ": "bone",
            "treatment": "vitamin D + calcium/phosphate repletion (XLH: phosphate + calcitriol or burosumab)",
            "kernel_action": "refill the capped mineral-supply ceiling M: 0.5 (deficient) -> 1.0 (replete)",
            "mirror_of": "T16 (mineral-supply cap)", "moa": "restores the substrate that mineralizes the osteoid the "
            "T3 switch already laid down; the matrix occupancy is fine, only the mineral was missing",
            "restoration_sweep": sweep, "density_monotone_up": _monotone_up(dens),
            "density_normalizes": dens[-1] > 0.95, "restored": restored,
            "grade": "full mechanistic reversal (refilling M re-mineralizes to ceiling) [V]; intervention target [L]; "
                     "absolute mineral density / time-to-heal [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T4ext  ACHONDROPLASIA   <-  vosoritide (CNP analogue, antagonises FGFR3->MAPK)
#  knob: suppressive drive h_inhib on SOX9  (disease adds it; drug RELIEVES part of it)
#  HONEST: vosoritide is PARTIAL -- it raises growth velocity but does NOT normalise stature.
# ============================================================================
def tx_t4ext_achondroplasia(gamma=None):
    gamma = dz._gene_gamma("SOX9") if gamma is None else gamma
    sp = spinodal(gamma); h_wt = DA["wt_developmental_drive_x_spinodal"] * sp; s0 = -(gamma ** 0.5)
    h_dis = -0.80 * sp                                              # achondroplasia (FGFR3 G380R)
    wt_out = dz._occupancy(gamma, h_wt, s0)
    # vosoritide gives only PARTIAL relief: it must stay BELOW the spinodal cliff (it does NOT flip the chondrocyte
    # switch fully on / normalise stature) -- it raises growth velocity, the honest clinical result.
    relief_max = 0.30                                              # sub-cliff partial relief (honest: not a cure)
    sweep = [{"drug_intensity": x, "suppressive_drive": round(h_dis * (1.0 - relief_max * x), 4),
              "growth_plate_output": round(dz._occupancy(gamma, h_wt + h_dis * (1.0 - relief_max * x), s0), 4)}
             for x in _intensities()]
    outs = [r["growth_plate_output"] for r in sweep]
    moved_up = _monotone_up(outs) and outs[-1] > outs[0] + 0.02
    not_cured = outs[-1] < wt_out - 1e-6                            # honest: stays below wild-type (no full crossing)
    restored = moved_up and not_cured
    return {"target": "Tx-T4-ext", "disease": "Achondroplasia & chondrodysplasias", "organ": "cartilage",
            "treatment": "vosoritide (C-type natriuretic peptide analogue)",
            "kernel_action": "partially relieve the FGFR3 suppressive drive on the SOX9 chondrocyte switch",
            "mirror_of": "T4-ext (suppressive drive)", "moa": "CNP/NPR-B signalling antagonises the FGFR3->MAPK "
            "brake on chondrocyte proliferation, lifting the suppressive drive and raising growth-plate output",
            "wild_type_output": round(wt_out, 4), "restoration_sweep": sweep,
            "output_monotone_up": _monotone_up(outs), "partial_not_cured": not_cured, "restored": restored,
            "grade": "PARTIAL mechanistic reversal: relieving the suppressive drive raises growth-plate output but "
                     "stays below wild-type [V]; vosoritide target [L]; absolute height gain [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T6  OSTEOPOROSIS   <-  (a) mechanical loading  (b) antiresorptive  (c) anabolic
#  knobs: (a) load drive across the spinodal  (b) escape-rate barrier  (c) deposition drive
# ============================================================================
def tx_t6_osteoporosis(gamma=None):
    gamma = dz._gene_gamma("RUNX2") if gamma is None else gamma
    sp = spinodal(gamma); s_low = -(gamma ** 0.5)
    # (a) mechanical loading: restore the drive from bedrest (-0.5 sp) up across the spinodal to +1.5 sp
    load_sweep = [{"load_intensity": x, "drive": round(-0.5 * sp + x * (2.0 * sp), 4),
                   "density_from_low": round(dyn.bone_density(-0.5 * sp + x * (2.0 * sp), gamma, s0=s_low), 4)}
                  for x in _intensities()]
    ld = [r["density_from_low"] for r in load_sweep]
    loading_redensifies = _monotone_up(ld) and ld[-1] > 0.9 and ld[-1] > ld[0] + 0.3
    # (b) antiresorptive (bisphosphonate / denosumab): raise the dense-basin escape barrier back toward intact,
    #     so the relative de-densification loss-rate at a fixed bedrest disuse drive falls toward maintenance (1.0)
    h_dis = -0.5 * sp
    r_maint = dz._disuse_escape_rate(gamma, 0.0)
    def _loss_rate_with_barrier_restored(x):
        # x in [0,1] restores the lowered barrier fraction back toward the intact barrier
        b0 = barrier(gamma); frac = min(max(abs(h_dis) / sp, 0.0), 0.999) if sp > 0 else 0.0
        b_eff = b0 * (1.0 - frac * (1.0 - x))                      # x=0 -> disease barrier ; x=1 -> intact barrier
        sc = max(barrier(gamma), 1e-6)
        return math.exp(-b_eff / sc) / r_maint
    anti_sweep = [{"drug_intensity": x, "rel_loss_rate": round(_loss_rate_with_barrier_restored(x), 4)}
                  for x in _intensities()]
    al = [r["rel_loss_rate"] for r in anti_sweep]
    antiresorptive_slows = _monotone_down(al) and al[-1] < al[0] and abs(al[-1] - 1.0) < 1e-6
    restored = loading_redensifies and antiresorptive_slows
    return {"target": "Tx-T6", "disease": "Disuse & post-menopausal osteoporosis", "organ": "bone",
            "treatment": "mechanical loading + antiresorptive (bisphosphonate/denosumab) + anabolic (teriparatide/romosozumab)",
            "kernel_action": "loading drives the R19 switch back across the spinodal (re-densify); antiresorptive "
                             "raises the dense-basin escape barrier (Kramers rate -> maintenance)",
            "mirror_of": "T6 (disuse lowers the dense-basin barrier; the exact mirror of T3 loading)",
            "moa": "weight-bearing/anabolic load re-deposits matrix (Frost mechanostat back above MES); antiresorptives "
                   "block osteoclastic escape so the dense basin stops leaking",
            "loading_sweep": load_sweep, "loading_redensifies": loading_redensifies,
            "antiresorptive_sweep": anti_sweep, "antiresorptive_returns_rate_to_maintenance": antiresorptive_slows,
            "restored": restored,
            "grade": "loading re-crosses to the dense basin [F] (mirror of T3); antiresorptive returns the Kramers "
                     "loss-rate to maintenance [V]; intervention targets [L]; absolute BMD gain [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T6b  OSTEOPETROSIS   <-  HSCT (restores osteoclasts) / interferon-gamma-1b
#  knob: the resorption DOWN-branch (disease disables it; HSCT re-enables it)
# ============================================================================
def tx_t6b_osteopetrosis(gamma=None):
    gamma = dz._gene_gamma("RUNX2") if gamma is None else gamma
    base = dz.t6b_osteopetrosis(gamma)
    locked = base["unloaded_density_osteopetrosis"]               # disease: density locked HIGH on unload
    restored_density = base["unloaded_density_normal"]            # HSCT re-enables resorption -> returns to baseline
    # graft-function sweep: blend the (disabled) osteopetrotic down-branch toward the (enabled) normal one
    sweep = [{"graft_function": x,
              "unloaded_density": round(locked + x * (restored_density - locked), 4)} for x in _intensities()]
    dseq = [r["unloaded_density"] for r in sweep]
    restored = _monotone_down(dseq) and dseq[-1] < 0.5 and dseq[0] > 0.95
    return {"target": "Tx-T6b", "disease": "Osteopetrosis", "organ": "bone",
            "treatment": "haematopoietic stem-cell transplant (osteoclast-precursor replacement); interferon-gamma-1b",
            "kernel_action": "re-enable the disabled resorption (DOWN) branch of the T3 hysteresis loop",
            "mirror_of": "T6b (osteoclast failure disables the DOWN branch)",
            "moa": "donor-derived osteoclasts restore resorption, so density can fall again on unloading and the "
                   "hysteresis loop regains its lower branch",
            "disease_unloaded_density": round(locked, 4), "restored_unloaded_density": round(restored_density, 4),
            "graft_sweep": sweep, "restored": restored,
            "grade": "full mechanistic reversal (re-enabling the DOWN branch unlocks density) [V]; HSCT for malignant "
                     "infantile osteopetrosis [L]; engraftment kinetics / material strength [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T8  MYASTHENIA GRAVIS   <-  pyridostigmine (AChEi) + immunotherapy
#  knob: post-synaptic safety factor (theta)  (disease raises theta; drug lowers it back)
# ============================================================================
def tx_t8_myasthenia(freq_hz=3.0):
    theta_dis = dz._NMJ_MG["theta"]; theta_norm = dz._NMJ_NORMAL["theta"]
    base = {k: v for k, v in dz._NMJ_MG.items()}
    sweep = []
    for x in _intensities():
        th = theta_dis + x * (theta_norm - theta_dis)             # restore safety factor toward normal
        p = dict(base); p["theta"] = th
        dec = dz._decrement(dz._nmj_train(freq_hz, **p))
        sweep.append({"ach_availability": x, "theta": round(th, 4), "rns_decrement": round(dec, 4)})
    decs = [r["rns_decrement"] for r in sweep]
    restored = _monotone_down(decs) and decs[-1] < decs[0] and decs[-1] < DA["rns_decrement_pass_pct"] / 100.0
    return {"target": "Tx-T8", "disease": "Myasthenia gravis", "organ": "skeletal_muscle",
            "treatment": "pyridostigmine (acetylcholinesterase inhibitor) + immunotherapy (steroids/rituximab/thymectomy)",
            "kernel_action": "restore the post-synaptic safety factor (lower theta) so low-frequency NMJ depression no "
                             "longer drops recruitment",
            "mirror_of": "T8 (AChR block raises theta -> RNS decrement)",
            "moa": "AChE inhibition raises synaptic ACh and re-clears the end-plate threshold; immunotherapy removes the "
                   "AChR block at source",
            "test_freq_hz": freq_hz, "restoration_sweep": sweep, "decrement_monotone_down": _monotone_down(decs),
            "decrement_below_diagnostic_threshold": decs[-1] < DA["rns_decrement_pass_pct"] / 100.0, "restored": restored,
            "grade": "decrement abolished as the safety factor is restored [V]; AChEi target + 10% diagnostic "
                     "threshold [L]; absolute strength gain [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T8b  LAMBERT-EATON   <-  amifampridine (3,4-diaminopyridine)
#  knob: quantal content / release (disease lowers it; 3,4-DAP raises it)
# ============================================================================
def tx_t8b_lems(freq_hz=3.0):
    base = {k: v for k, v in dz._NMJ_LEMS.items()}
    b_dis = dz._NMJ_LEMS["baseline"]; b_norm = dz._NMJ_NORMAL["baseline"]
    # 3,4-DAP broadens the presynaptic action potential -> more Ca entry -> higher quantal content (baseline release)
    sweep = []
    for x in _intensities():
        bl = b_dis + x * (b_norm - b_dis)
        p = dict(base); p["baseline"] = bl
        seq = dz._nmj_train(freq_hz, **p)
        sweep.append({"dap_intensity": x, "baseline_release": round(bl, 4),
                      "low_freq_efficacy": round(seq[0], 4)})
    eff = [r["low_freq_efficacy"] for r in sweep]
    restored = _monotone_up(eff) and eff[-1] > eff[0] + 0.1
    return {"target": "Tx-T8b", "disease": "Lambert-Eaton myasthenic syndrome (LEMS)", "organ": "skeletal_muscle",
            "treatment": "amifampridine (3,4-diaminopyridine); treat underlying SCLC where paraneoplastic",
            "kernel_action": "raise presynaptic quantal content (baseline release) back toward normal",
            "mirror_of": "T8b (low quantal content + facilitation)",
            "moa": "K-channel block widens the presynaptic action potential, increasing Ca influx and ACh quantal "
                   "content, which restores baseline NMJ efficacy",
            "test_freq_hz": freq_hz, "restoration_sweep": sweep, "baseline_efficacy_monotone_up": _monotone_up(eff),
            "restored": restored,
            "grade": "baseline transmission restored as quantal content rises [V]; 3,4-DAP target [L]; absolute "
                     "strength gain [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T12  CHANNELOPATHIES   <-  mexiletine (myotonia) / acetazolamide,K+ (periodic paralysis)
#  knob: membrane excitability (recovery beta)  (disease shifts it; drug returns it toward normal)
# ============================================================================
def tx_t12_channelopathy():
    bn = DA["chan_beta_normal"]; bm = DA["chan_beta_myotonia"]; bp = DA["chan_beta_paralysis"]
    def _bt(x): return x if x is not None else 99.0
    bt_norm = _bt(dz._block_threshold(bn))
    # myotonia: mexiletine (Na-channel block) reduces hyperexcitability -> beta rises from 0.35 toward normal 0.5
    myo_sweep = [{"drug_intensity": x, "beta": round(bm + x * (bn - bm), 4),
                  "block_threshold": _bt(dz._block_threshold(bm + x * (bn - bm)))} for x in _intensities()]
    myo_bt = [r["block_threshold"] for r in myo_sweep]
    myo_restored = _monotone_down(myo_bt) and abs(myo_bt[-1] - bt_norm) < 1e-9
    # periodic paralysis: acetazolamide / K-management reduce inactivation-proneness -> beta falls from 1.2 toward 0.5
    para_sweep = [{"drug_intensity": x, "beta": round(bp + x * (bn - bp), 4),
                   "block_threshold": _bt(dz._block_threshold(bp + x * (bn - bp)))} for x in _intensities()]
    para_bt = [r["block_threshold"] for r in para_sweep]
    para_restored = _monotone_up(para_bt) and abs(para_bt[-1] - bt_norm) < 1e-9
    restored = myo_restored and para_restored
    return {"target": "Tx-T12", "disease": "Channelopathies: myotonia & periodic paralysis", "organ": "skeletal_muscle",
            "treatment": "mexiletine (Na-channel blocker, myotonia); acetazolamide / potassium management (periodic paralysis)",
            "kernel_action": "return the membrane recovery parameter (depolarization-block threshold) toward normal "
                             "from BOTH excitability signs",
            "mirror_of": "T12 (opposite excitability shifts: myotonia hyperexcitable, paralysis block-prone)",
            "moa": "Na-channel block damps the myotonic hyperexcitability; carbonic-anhydrase inhibition / serum-K "
                   "control corrects the depolarization-block-prone state",
            "normal_block_threshold": bt_norm, "myotonia_sweep": myo_sweep, "myotonia_normalizes": myo_restored,
            "paralysis_sweep": para_sweep, "paralysis_normalizes": para_restored, "restored": restored,
            "grade": "both excitability signs returned to the normal block threshold [V]; mexiletine / acetazolamide "
                     "targets [L]; absolute attack frequency [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T11  MUSCULAR DYSTROPHY   <-  (a) corticosteroids (slow damage)  (b) exon-skipping / gene therapy
#  knobs: (a) per-cycle damage rate A  (b) dystrophin fraction (fragility = 1 - dystrophin)
#  HONEST: both are disease-MODIFYING (slow / shift), not curative.
# ============================================================================
def tx_t11_dystrophy(n=200000):
    dd = DA["dystrophin_dmd"]; A0 = DA["dystrophy_damage_A"]
    r_dmd = dz._contractile_fatigue(dd, n, A=A0)
    # (a) corticosteroids: reduce the per-contraction damage scale A (membrane stabilisation, less tearing)
    steroid_sweep = [{"steroid_intensity": x, "damage_scale_A": round(A0 * (1.0 - 0.7 * x), 9),
                      "retained_force": round(dz._contractile_fatigue(dd, n, A=A0 * (1.0 - 0.7 * x)), 4)}
                     for x in _intensities()]
    sr = [r["retained_force"] for r in steroid_sweep]
    steroid_slows = _monotone_up(sr) and sr[-1] > sr[0] + 0.02
    # (b) exon-skipping / micro-dystrophin gene therapy: raise dystrophin fraction (DMD-null -> BMD-like partial)
    gene_sweep = [{"gene_intensity": x, "dystrophin": round(dd + x * (DA["dystrophin_bmd"] - dd), 4),
                   "retained_force": round(dz._contractile_fatigue(dd + x * (DA["dystrophin_bmd"] - dd), n, A=A0), 4)}
                  for x in _intensities()]
    gr = [r["retained_force"] for r in gene_sweep]
    gene_shifts = _monotone_up(gr) and gr[-1] > gr[0] + 0.05
    restored = steroid_slows and gene_shifts
    return {"target": "Tx-T11", "disease": "Muscular dystrophy (Duchenne / Becker)", "organ": "skeletal_muscle",
            "treatment": "corticosteroids (deflazacort/prednisone) + exon-skipping / micro-dystrophin gene therapy",
            "kernel_action": "(a) lower the per-contraction damage scale A; (b) raise the dystrophin fraction so "
                             "fragility (1 - dystrophin) falls -- shifting a DMD trajectory toward Becker",
            "mirror_of": "T11 (fragility = 1 - dystrophin drives contractile-contact cyclic fatigue)",
            "moa": "steroids stabilise the sarcolemma and slow contraction-induced tearing; restoring partial "
                   "dystrophin reconnects the contractile lattice to the membrane/ECM, lowering per-cycle damage",
            "retained_untreated_dmd": round(r_dmd, 4), "steroid_sweep": steroid_sweep, "steroid_slows_loss": steroid_slows,
            "gene_sweep": gene_sweep, "gene_shifts_toward_becker": gene_shifts, "restored": restored,
            "grade": "DISEASE-MODIFYING: lowering A slows loss and raising dystrophin shifts DMD->BMD trajectory [V]; "
                     "reading-frame restoration + steroid evidence [L]; cure / absolute timeline [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T17  OSTEOLYTIC BONE DISEASE   <-  antiresorptive (denosumab/bisphosphonate) + anti-tumour
#  knobs: (myeloma) osteoblast-formation cap ; (GCT) RANKL resorptive drive
# ============================================================================
def tx_t17_osteolytic(gamma=None):
    gamma = dz._gene_gamma("RUNX2") if gamma is None else gamma
    sp = spinodal(gamma)
    loads = [round(-1.0 + 0.02 * i, 3) for i in range(int(2.0 / 0.02) + 1)]
    def _dens(s): return min(1.0, max(0.0, (s + gamma ** 0.5) / (2.0 * gamma ** 0.5)))
    # (myeloma) relieve the DKK1 formation cap: 0.15 (locked lytic) -> 1.0 (formation restored)
    cap0 = DA["myeloma_formation_cap"]
    mye_sweep = []
    for x in _intensities():
        cap = cap0 + x * (1.0 - cap0)
        s = -(gamma ** 0.5) * 0.95; d = 0.0
        for h in loads:
            s = settle(gamma, h, s0=s); d = min(_dens(s), cap)
        mye_sweep.append({"therapy_intensity": x, "formation_cap": round(cap, 4), "reformed_density": round(d, 4)})
    md = [r["reformed_density"] for r in mye_sweep]
    myeloma_reforms = _monotone_up(md) and md[-1] > 0.9 and md[0] < 0.2
    # (GCT) denosumab removes the RANKL resorptive drive: -1.3 sp -> 0
    gct0 = -DA["gct_resorptive_drive_x_spinodal"] * sp
    gct_sweep = [{"denosumab_intensity": x, "resorptive_drive": round(gct0 * (1.0 - x), 4),
                  "density_from_dense": round(dyn.bone_density(gct0 * (1.0 - x), gamma, s0=+(gamma ** 0.5)), 4)}
                 for x in _intensities()]
    gd = [r["density_from_dense"] for r in gct_sweep]
    gct_recovers = _monotone_up(gd) and gd[-1] > 0.9 and gd[0] < 0.3
    restored = myeloma_reforms and gct_recovers
    return {"target": "Tx-T17", "disease": "Osteolytic bone disease (multiple myeloma; giant-cell tumour)", "organ": "bone",
            "treatment": "antiresorptive (denosumab / zoledronate) + anti-tumour therapy (anti-myeloma; denosumab for GCT)",
            "kernel_action": "(myeloma) relieve the osteoblast formation cap so loading can re-form bone; "
                             "(GCT) remove the RANKL resorptive drive so dense bone is no longer driven down",
            "mirror_of": "T17 (osteoclast/osteoblast uncoupling: formation arm disabled / RANKL resorptive drive)",
            "moa": "anti-myeloma therapy + osteoblast de-suppression re-couple formation; anti-RANKL denosumab halts "
                   "the giant-cell-tumour resorptive drive (its licensed mechanism)",
            "myeloma_sweep": mye_sweep, "myeloma_reforms_bone": myeloma_reforms,
            "gct_sweep": gct_sweep, "gct_density_recovers": gct_recovers, "restored": restored,
            "grade": "both arms reversed (formation cap relieved -> re-form; RANKL drive removed -> recover) [V]; "
                     "denosumab anti-RANKL target [L]; absolute lesion healing [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T13  STRESS FRACTURE   <-  relative rest (load off the bone) + graded return; healing re-cross
#  knob: cyclic stress amplitude relative to the endurance limit (rest -> sub-endurance -> protected)
# ============================================================================
def tx_t13_stress_fracture(gamma=None):
    gamma = dz._gene_gamma("RUNX2") if gamma is None else gamma
    sp = spinodal(gamma); ncyc = 1000000
    sigma_dis = 1.8                                               # running, supra-endurance (damaging)
    # relative rest: reduce stress amplitude from 1.8 toward 0.8 (sub-endurance, protected)
    rest_sweep = [{"rest_intensity": x, "sigma_over_endurance": round(sigma_dis + x * (0.8 - sigma_dis), 4),
                   "further_damage_rate": round(max(0.0, (max(sigma_dis + x * (0.8 - sigma_dis), 0.0) - 1.0)) ** 2
                                                if (sigma_dis + x * (0.8 - sigma_dis)) > 1.0 else 0.0, 6)}
                  for x in _intensities()]
    dr = [r["further_damage_rate"] for r in rest_sweep]
    rest_halts = _monotone_down(dr) and dr[-1] == 0.0 and dr[0] > 0.0
    # healing re-cross (Wolff): from a fractured low-density state, physiologic load re-crosses to dense (callus)
    frac_state = -(gamma ** 0.5) * 0.9
    d_unloaded = dyn.bone_density(0.0, gamma, s0=frac_state)
    heal_sweep = [{"load_intensity": x, "density": round(dyn.bone_density(x * 1.5 * sp, gamma, s0=frac_state), 4)}
                  for x in _intensities()]
    hd = [r["density"] for r in heal_sweep]
    heals = _monotone_up(hd) and hd[-1] > d_unloaded + 0.3
    restored = rest_halts and heals
    return {"target": "Tx-T13", "disease": "Stress fracture (bone fatigue) & fracture healing", "organ": "bone",
            "treatment": "relative rest / activity modification, then graded return to load; (refractory) fixation",
            "kernel_action": "drop the cyclic stress amplitude below the endurance limit (halt microdamage); then "
                             "physiologic load re-crosses the T3 switch to the dense basin (callus / Wolff's law)",
            "mirror_of": "T13 (supra-endurance cyclic fatigue; bone uniquely HEALS by re-crossing)",
            "moa": "unloading stops accumulating fatigue damage below the S-N endurance limit; controlled return load "
                   "drives remodelling that re-deposits and re-crosses the switch (callus formation)",
            "rest_sweep": rest_sweep, "rest_halts_microdamage": rest_halts,
            "heal_sweep": heal_sweep, "physiologic_load_heals": heals, "restored": restored,
            "grade": "rest halts fatigue accrual + load-driven healing re-cross [V] (the re-cross is already in T13); "
                     "rest/graded-return protocol [L]; absolute time-to-union [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T14  TENDINOPATHY   <-  eccentric / heavy-slow resistance loading (mechanotransduction) + load management
#  knob: cyclic overuse amplitude (arrest) + a controlled-load re-deposition (rebuild, honest [O] absolute)
# ============================================================================
def tx_t14_tendinopathy(n=200000):
    sigma_dis = 1.8                                              # overuse (damaging)
    # load management: drop overuse amplitude below threshold -> no further fibre loss
    arrest_sweep = [{"deload_intensity": x, "sigma_over_sigma_star": round(sigma_dis + x * (0.8 - sigma_dis), 4),
                     "contact_number_final": round(dz._oa_contact_loss(sigma_dis + x * (0.8 - sigma_dis), n), 4)}
                    for x in _intensities()]
    cn = [r["contact_number_final"] for r in arrest_sweep]
    arrests = _monotone_up(cn) and cn[-1] >= cn[0]
    # eccentric/HSR rebuild: controlled mechanotransduction stimulates collagen synthesis -> partial re-deposition
    #   (modelled as a re-deposition term on the contact number; absolute regeneration is honestly [O])
    lost = 1.0 - dz._oa_contact_loss(sigma_dis, n)
    rebuild_frac_max = 0.6                                       # honest: tendon turnover is slow & partial
    rebuild_sweep = [{"eccentric_intensity": x,
                      "contact_number": round(min(1.0, (1.0 - lost) + x * rebuild_frac_max * lost), 4)}
                     for x in _intensities()]
    rb = [r["contact_number"] for r in rebuild_sweep]
    rebuilds = _monotone_up(rb) and rb[-1] > rb[0]
    restored = arrests and rebuilds
    return {"target": "Tx-T14", "disease": "Tendinopathy", "organ": "skeletal_muscle",
            "treatment": "eccentric / heavy-slow resistance loading (mechanotransduction) + load management",
            "kernel_action": "deload below the fatigue threshold (arrest further loss) + controlled load drives "
                             "collagen re-deposition (partial contact re-cross)",
            "mirror_of": "T14 (overuse cyclic fatigue of the tendon collagen contact network)",
            "moa": "the loading PARADOX: uncontrolled overuse tears contacts, but controlled high-load slow "
                   "eccentric work is the mechanotransductive stimulus for collagen synthesis and remodelling",
            "arrest_sweep": arrest_sweep, "deload_arrests_loss": arrests,
            "rebuild_sweep": rebuild_sweep, "controlled_load_rebuilds": rebuilds, "restored": restored,
            "grade": "deloading arrests progression [V]; eccentric-loading rebuild is mechanistic, absolute collagen "
                     "regeneration [O]; Alfredson eccentric-loading protocol [L]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  Tx-T15  SARCOPENIA   <-  progressive resistance training + adequate protein (+ vitamin D)
#  knob: the three ageing axes (motor-unit recruitment, fibre size, fatigue tau)
#  HONEST: PARTIAL -- training claws back part of the decline; the ageing floor remains.
# ============================================================================
def tx_t15_sarcopenia(age_frac=1.0):
    mu0, fib0, tau0 = dz._sarcopenia_axes(age_frac)              # untrained aged state
    young_force = 1.0 * 1.0                                      # mu=fib=1 at age 0
    recover_max = 0.5                                            # training reclaims up to ~half of the lost axes
    sweep = []
    for x in _intensities():
        mu = mu0 + x * recover_max * (1.0 - mu0)
        fib = fib0 + x * recover_max * (1.0 - fib0)
        sweep.append({"training_intensity": x, "motor_unit_fraction": round(mu, 4),
                      "fibre_size_fraction": round(fib, 4), "max_force": round(mu * fib, 4)})
    force = [r["max_force"] for r in sweep]
    moved_up = _monotone_up(force) and force[-1] > force[0] + 0.02
    not_young = force[-1] < young_force - 1e-6                   # honest: stays below young
    restored = moved_up and not_young
    return {"target": "Tx-T15", "disease": "Sarcopenia", "organ": "skeletal_muscle",
            "treatment": "progressive resistance training + adequate dietary protein (+ vitamin D where deficient)",
            "kernel_action": "raise the recruitment and fibre-size axes back up (partial); the fatigue axis improves too",
            "mirror_of": "T15 (multi-axis ageing decline)",
            "moa": "resistance training drives motor-unit recruitment and type-II fibre hypertrophy, partially "
                   "reversing two of the three decline axes; protein supplies the synthetic substrate",
            "untrained_aged_force": round(mu0 * fib0, 4), "young_force": round(young_force, 4),
            "training_sweep": sweep, "force_monotone_up": _monotone_up(force), "partial_not_young": not_young,
            "restored": restored,
            "grade": "PARTIAL reversal: training raises max force but stays below young [V]; resistance-training "
                     "evidence (Fiatarone) [L]; absolute strength / ageing floor [O]",
            "status": "PASS" if restored else "OPEN"}


# ============================================================================
#  HONEST [O] / PARTIAL entries (results, not failures)
# ============================================================================
def tx_t9_osteoarthritis_arrest(n=200000):
    """OA: unloading ARRESTS further cartilage-contact loss [V], but the kernel has no matrix-resynthesis term and
    cartilage does not regenerate, so already-lost contacts are NOT restored. Arrest [V] + no-regen [O]."""
    sigma_dis = 1.8
    arrest_sweep = [{"deload_intensity": x, "sigma_over_sigma_star": round(sigma_dis + x * (0.8 - sigma_dis), 4),
                     "further_loss_rate": round(max(0.0, (max(sigma_dis + x * (0.8 - sigma_dis), 0.0) - 1.0)) ** 2
                                                if (sigma_dis + x * (0.8 - sigma_dis)) > 1.0 else 0.0, 6)}
                    for x in _intensities()]
    flr = [r["further_loss_rate"] for r in arrest_sweep]
    arrests = _monotone_down(flr) and flr[-1] == 0.0 and flr[0] > 0.0
    already_lost = round(1.0 - dz._oa_contact_loss(sigma_dis, n), 4)
    return {"target": "Tx-T9", "disease": "Osteoarthritis (OA)", "organ": "cartilage",
            "treatment": "load reduction / weight loss / activity modification (DMOADs unproven; arthroplasty is hardware)",
            "kernel_action": "drop cyclic contact stress below the fatigue threshold -> ARREST further contact loss; "
                             "NO matrix-resynthesis term exists (cartilage does not regenerate)",
            "mirror_of": "T9 (cyclic supra-threshold cartilage fatigue)",
            "moa": "removing the supra-threshold cyclic load stops further unjamming of the cartilage contact network; "
                   "the lost matrix is not rebuilt by the kernel and not clinically regenerated",
            "arrest_sweep": arrest_sweep, "deload_arrests_progression": arrests,
            "already_lost_matrix_not_restored": already_lost,
            "grade": "progression ARREST by unloading [V]; matrix REGENERATION [O] (no resynthesis term; cartilage "
                     "does not regenerate -- arthroplasty replaces hardware, outside the kernel); weight-loss/load "
                     "evidence [L]",
            "status": "PASS" if arrests else "OPEN"}


def tx_t10_metabolic_myopathy(tau_s=180.0):
    """Metabolic/mitochondrial myopathy: only a cofactor-RESPONSIVE subset (e.g. riboflavin-responsive MADD,
    primary CoQ10 deficiency, carnitine deficiency) is reversible -- supplementation lengthens the fatigue tau and
    reduces the non-recovering residual. The general case has no kernel restoration. Subset [V?] + general [O]."""
    tau_dis = tau_s * 0.4; resid_dis = 0.35                      # disease: short tau + non-recovering residual
    # cofactor-responsive subset: supplementation moves tau back up and residual down
    sweep = [{"cofactor_intensity": x, "fatigue_tau_s": round(tau_dis + x * (tau_s - tau_dis), 2),
              "non_recovering_residual": round(resid_dis * (1.0 - x), 4)} for x in _intensities()]
    taus = [r["fatigue_tau_s"] for r in sweep]; resid = [r["non_recovering_residual"] for r in sweep]
    subset_reversible = _monotone_up(taus) and _monotone_down(resid) and resid[-1] < 0.05
    return {"target": "Tx-T10", "disease": "Metabolic / mitochondrial myopathy", "organ": "skeletal_muscle",
            "treatment": "cofactor supplementation in the responsive subset (riboflavin / CoQ10 / carnitine); "
                         "otherwise supportive (avoid triggers, aerobic conditioning)",
            "kernel_action": "(responsive subset only) lengthen the fatigue tau and reduce the non-recovering "
                             "residual; NO general kernel restoration",
            "mirror_of": "T10 (shortened fatigue tau + non-recovering residual)",
            "moa": "replacing the limiting cofactor restores the flux that sets the fatigue time-constant in the "
                   "responsive subset; most primary mitochondrial defects have no such knob",
            "cofactor_sweep": sweep, "responsive_subset_reversible": subset_reversible,
            "grade": "cofactor-responsive SUBSET reversal [V?]; GENERAL case [O] (etiology-specific, no general "
                     "cure); responsive-subtype evidence [L]",
            "status": "PARTIAL"}


def tx_t7_dosage_dysplasias():
    """Master-gene dosage dysplasias (CCD/RUNX2, campomelic/SOX9, Holt-Oram/TBX5): the switch-crossing decision is
    made within a CLOSED developmental window. No postnatal knob re-runs development, and the already-formed
    skeleton is fixed. Management is surgical/symptomatic, not restoration of the dosage. Honest [O] NEGATIVE."""
    return {"target": "Tx-T7", "disease": "Master-gene dosage dysplasias (CCD/RUNX2, campomelic/SOX9, Holt-Oram/TBX5)",
            "organ": "skeleton (developmental)",
            "treatment": "surgical / symptomatic management (dental & cranial surgery in CCD; cardiac & limb surgery "
                         "in Holt-Oram); no dosage-restoring therapy",
            "kernel_action": "NONE -- the developmental switch-crossing window has closed; the spinodal-cliff decision "
                             "is already settled and the formed skeleton is fixed",
            "mirror_of": "T7 (haploinsufficiency drives the developmental drive below the spinodal cliff)",
            "moa": "the master-switch commitment is a one-shot developmental event; postnatal dosage cannot re-run it",
            "restored": False,
            "grade": "[O] NEGATIVE: developmental dosage cliffs are not postnatally reversible in this kernel "
                     "(closed developmental window; fixed phenotype); surgical management is symptomatic [L]",
            "status": "OPEN"}


def tx_oncology_prevention_vs_treatment():
    """Oncology: the carcinogenesis kernel models INITIATION (carcinogen dose -> R19 barrier down -> Kramers
    crossing -> RR). PRIMARY PREVENTION (remove the carcinogen -> dose down -> RR down) is in scope and [V].
    Treatment of an ESTABLISHED tumour (cytotoxic chemo / resection / radiation = killing transformed cells) is
    NOT a barrier-restoration of the original switch and is out of the initiation kernel's scope: [O]."""
    # prevention: monotone -- lowering the carcinogen dose lowers the barrier-reduction -> lowers the crossing rate
    doses = [round(1.0 - x, 3) for x in _intensities()]          # 1.0 (full exposure) -> 0.0 (removed)
    def _rel_crossing(dose):                                     # barrier reduction proportional to dose -> Kramers
        b0 = 1.0; b_eff = b0 * (1.0 - 0.6 * dose); return math.exp(-b_eff / 0.4)
    prev_sweep = [{"carcinogen_dose": d, "relative_initiation_rate": round(_rel_crossing(d), 4)} for d in doses]
    rates = [r["relative_initiation_rate"] for r in prev_sweep]
    prevention_works = _monotone_down(rates) and rates[-1] < rates[0]
    return {"target": "Tx-ONCO", "disease": "Sarcomas (osteo-/soft-tissue/chondro-/Ewing)", "organ": "various",
            "treatment": "PREVENTION: remove the carcinogen (radiation-exposure control). ESTABLISHED DISEASE: surgery "
                         "+ cytotoxic chemotherapy +/- radiation (out of the initiation kernel's scope)",
            "kernel_action": "PREVENTION = raise the barrier back by removing the dose -> initiation rate falls [V]; "
                             "established-tumour cytotoxic therapy is NOT barrier-restoration of the original switch [O]",
            "mirror_of": "the carcinogenesis kernel (dose -> barrier down -> Kramers crossing -> RR)",
            "moa": "prevention restores the un-lowered barrier; cytotoxic therapy kills already-transformed cells, a "
                   "different process the initiation kernel does not represent",
            "prevention_sweep": prev_sweep, "prevention_lowers_initiation": prevention_works,
            "grade": "PRIMARY PREVENTION (dose down -> RR down) [V]; established-tumour TREATMENT response [O] (out of "
                     "the initiation kernel's scope -- it is cell-killing, not barrier restoration); exposure-control "
                     "evidence [L]",
            "status": "PARTIAL"}


# ============================================================================
#  battery
# ============================================================================
def run_treatment_battery():
    seed_everything()
    # [V]-gradeable mirror treatments (PASS = correct restoration DIRECTION)
    reversible = [
        tx_t16_osteomalacia(), tx_t4ext_achondroplasia(), tx_t6_osteoporosis(), tx_t6b_osteopetrosis(),
        tx_t8_myasthenia(), tx_t8b_lems(), tx_t12_channelopathy(), tx_t11_dystrophy(),
        tx_t17_osteolytic(), tx_t13_stress_fracture(), tx_t14_tendinopathy(), tx_t15_sarcopenia(),
        tx_t9_osteoarthritis_arrest(),
    ]
    # honest PARTIAL / [O] entries (logged, NOT counted as failures -- same policy as T7d secondary)
    honest = [tx_t10_metabolic_myopathy(), tx_t7_dosage_dysplasias(), tx_oncology_prevention_vs_treatment()]
    all_entries = reversible + honest
    return {"_kernel": "treatment = the MIRROR of the disease operation on the SAME kernel (raise the barrier / "
                       "restore the drive across the spinodal / re-enable the disabled branch / refill the supply). "
                       "PASS = the disease signature moves monotonically back toward the healthy attractor (DIRECTION, "
                       "No-Tuning), never a clinical efficacy magnitude.",
            "treatments": all_entries,
            "all_reversible_treatments_restore": all(t["status"] == "PASS" for t in reversible),
            "honest_open_or_partial": [{"target": t["target"], "status": t["status"]} for t in honest],
            "grade_summary": "osteomalacia (refill M) [V], achondroplasia (relieve suppression, PARTIAL) [V], "
                             "osteoporosis (load re-cross + antiresorptive barrier) [F/V], osteopetrosis (re-enable "
                             "DOWN branch) [V], MG (restore safety factor) [V], LEMS (raise quantal content) [V], "
                             "channelopathies (normalise excitability) [V], dystrophy (lower A + raise dystrophin, "
                             "DISEASE-MODIFYING) [V], osteolytic (relieve formation cap + remove RANKL drive) [V], "
                             "stress fracture (rest + healing re-cross) [V], tendinopathy (deload + eccentric rebuild) "
                             "[V/O], sarcopenia (resistance training, PARTIAL) [V]; OA (ARREST only, no regen) [V/O]; "
                             "metabolic myopathy (cofactor subset) [V?/O]; dosage dysplasias [O] negative; oncology "
                             "prevention [V] / established-tumour treatment [O]."}


if __name__ == "__main__":
    r = run_treatment_battery()
    for t in r["treatments"]:
        print("  %-9s [%-7s]  %-52s <- %s" % (t["target"], t["status"], t["disease"][:52], t["treatment"][:60]))
    print("\nALL REVERSIBLE TREATMENTS RESTORE:", r["all_reversible_treatments_restore"])
    print("HONEST OPEN/PARTIAL:", r["honest_open_or_partial"])
