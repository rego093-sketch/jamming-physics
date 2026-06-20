"""
tier2_ion_diseases.py  --  REMEDIATION module (v0.6.0, Tier-2 disease-coverage increment).

Closes the Tier-2 gaps from the v0.4.0 audit (REMEDIATION_PLAN.md, gaps G2/G3/G4): the three major
ion diseases the volume named but had not yet MODELLED -- magnesium homeostasis, CKD-MBD / secondary
hyperparathyroidism, and humoral hypercalcemia of malignancy (PTHrP). The audit's standing question
"is every ion imbalance disease covered?" was answered "representative seven yes, these three not yet,
by design (rare/specific forms enter as a cited parameter)." This module supplies them WITHOUT any new
primitive: each is one of the six failure modes already derived in setpoint_failure.py, driven by the
volume's OWN closed-loop law (vp_loops.ou_setpoint, step error = load/k) and its OWN PTH comparator
(vp_loops.pth_curve). No new tuning is introduced -- the failure modes and the control law are reused.

  gap   disease                                   reused failure mode (setpoint_failure.py)         reused primitive
  ----  ----------------------------------------  ------------------------------------------------  ---------------------------
  G2    hypo-/hypermagnesemia                     loop-gain drop / buffer-arm failure               ou_setpoint (err = load/k)
  G3    CKD-MBD + secondary hyperparathyroidism   multi-arm loop-gain drop (renal integrator)       ou_setpoint + pth_curve
  G4    humoral hypercalcemia of malignancy       setpoint drift UP (the inverse of the T1 reset)   pth_curve (PTH comparator)

THE THREE RESULTS (each a reproduced DIRECTION [V]; absolute magnitudes [O]):
  * G2  A defended-magnesium setpoint, given the same load, drifts further from target as the loop gain
        falls (err = load/k): an absorption/reabsorption-arm failure (low k) under a renal/gut Mg-loss
        drive yields hypomagnesemia, an excretion-arm failure (low k) under an Mg-intake drive yields
        hypermagnesemia, both monotone in 1/k, the offset ratio equal to the gain ratio -- the volume's
        own load/k law, now read on a third ion.
  * G3  Stepping the renal integrator gain down (nephron loss) drives the CKD-MBD cascade in the cited
        order: serum phosphate rises (its excretion arm err = load/k grows), 1,25-vitamin-D falls
        (renal 1a-hydroxylase), serum calcium tends down, and the CaSR comparator raises PTH (secondary
        hyperparathyroidism) -- all four monotone in the falling renal gain, with the calcium x phosphate
        product climbing toward the precipitation ceiling.
  * G4  An exogenous PTHrP drive that the CaSR comparator cannot suppress (tumor-autonomous) relocates
        the defended calcium UPWARD (hypercalcemia), monotone in the PTHrP level -- the exact inverse of
        the T1 allosteric set-point reset (which relocates it back DOWN). The clinical fingerprint is
        reproduced: endogenous PTH is appropriately SUPPRESSED while calcium is high (unlike primary
        hyperparathyroidism, where PTH is high), because the CaSR loop works -- it simply cannot turn off
        a drive that is not its own.

GRADES (VP-SPEC C3): each disease maps to a cited failure mode and the reproduced direction is [V]; the
cited setpoints / variants / guidelines are [L] (serum Mg ~0.85 mM; TRPM6 HSH Schlingmann 2002; Gitelman
SLC12A3; KDIGO 2017 CKD-MBD; PTHrP humoral hypercalcemia Stewart 2005 NEJM); the ABSOLUTE excursion
magnitudes, the per-stage CKD progression timing, and the absolute hypercalcemia level are [O] (stated in
the ledger). No clinical efficacy is asserted.

DETERMINISM (C1): pure functions of the cited tables + the volume's OU law and PTH comparator; sigma=0 in
ou_setpoint (the RNG term vanishes) and G4 is a deterministic Euler settle with no RNG; round-before-
return; two runs -> identical sha. This module is ADDITIVE -- it is NOT imported by the research gate
(gamma-emergence + stress battery: gates.py -> vp_ion_engine + stress_tests only), so the research sha is
unchanged.
"""
import os, sys, math, json, hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import importlib
loops = importlib.import_module("vp_loops")


# ===========================================================================
# G2  MAGNESIUM  --  a third defended ion on the volume's own load/k law
# ===========================================================================
# Serum Mg setpoint (cited [L]); the loop holds it with a healthy gain. Disease = an arm losing gain so
# the same disturbance is no longer rejected (err = load/k): low k -> large offset (hypo OR hyper, by the
# sign of the unrejected drive).  This reuses vp_loops.ou_setpoint (the volume's signature control law).
MG_SETPOINT_mM = 0.85                 # serum magnesium reference midpoint (cited)
_K_HEALTHY_MG  = 4.0                  # tight regulator gain (same tier as the terrestrial baseline)
_K_ARM_FAILED  = 1.0                  # an arm (TRPM6/7 absorption, or renal excretion) loses gain
_MG_DRIVE      = 1.0                  # the unrejected disturbance magnitude (dimensionless, baseline load)


def _offset(k, load):
    """Deterministic steady internal displacement under a load: ou_setpoint err = load/k (sigma=0)."""
    return loops.ou_setpoint(k, sigma=0.0, load=load)["mean_offset"]


def magnesium_failures():
    """Hypo- and hypermagnesemia as the SAME loop-gain-drop law read with opposite drive signs.
       hypomagnesemia : reabsorption/absorption arm fails (low k) under an Mg-LOSS drive (load < 0)
                        -> internal Mg pulled DOWN by load/k ; deeper as k falls (TRPM6 / Gitelman).
       hypermagnesemia: excretion arm fails (low k) under an Mg-INTAKE drive (load > 0)
                        -> internal Mg pushed UP by load/k ; higher as k falls (renal insufficiency + load).
    """
    # healthy loop rejects either drive to a small residual offset
    healthy_loss = _offset(_K_HEALTHY_MG, -_MG_DRIVE)
    healthy_gain = _offset(_K_HEALTHY_MG, +_MG_DRIVE)
    # an arm failure (gain drop) leaves a large residual offset
    hypo  = _offset(_K_ARM_FAILED, -_MG_DRIVE)        # hypomagnesemia (down)
    hyper = _offset(_K_ARM_FAILED, +_MG_DRIVE)        # hypermagnesemia (up)
    # variance blow-up of the failed loop (Var = sigma^2/2k), reusing the OU statistics
    var_healthy = loops.ou_setpoint(_K_HEALTHY_MG, sigma=0.3)["variance"]
    var_failed  = loops.ou_setpoint(_K_ARM_FAILED, sigma=0.3)["variance"]
    return dict(
        setpoint_mM=MG_SETPOINT_mM, k_healthy=_K_HEALTHY_MG, k_arm_failed=_K_ARM_FAILED,
        healthy_offset_under_loss=round(healthy_loss, 5), healthy_offset_under_intake=round(healthy_gain, 5),
        hypomagnesemia_offset=round(hypo, 5), hypermagnesemia_offset=round(hyper, 5),
        # the failed-arm excursion is larger than the healthy-loop residual, in BOTH directions
        hypo_worse_than_healthy=bool(abs(hypo) > abs(healthy_loss) + 1e-9),
        hyper_worse_than_healthy=bool(abs(hyper) > abs(healthy_gain) + 1e-9),
        # the excursion ratio equals the gain ratio (the load/k law): |offset_failed|/|offset_healthy| = k_healthy/k_failed
        excursion_ratio=round(abs(hypo) / abs(healthy_loss), 3),
        predicted_gain_ratio=round(_K_HEALTHY_MG / _K_ARM_FAILED, 3),
        ratio_matches_load_over_k=bool(abs(abs(hypo) / abs(healthy_loss) - _K_HEALTHY_MG / _K_ARM_FAILED) < 1e-3),
        variance_healthy=var_healthy, variance_failed=var_failed,
        variance_blows_up=bool(var_failed > var_healthy),
        anchor="serum Mg ~0.85 mM (cited); hypomagnesemia: TRPM6 loss (HSH, Schlingmann 2002) / Gitelman "
               "(SLC12A3) renal Mg wasting = absorption/reabsorption-arm gain drop; hypermagnesemia: renal "
               "excretion-arm failure (renal insufficiency + Mg load)",
        grade="[L] setpoint + TRPM6/Gitelman anchors; [V] err=load/k drives both directions, monotone in k, "
              "ratio == gain ratio, variance blow-up; [O] absolute Mg excursion magnitude",
    )


# ===========================================================================
# G3  CKD-MBD  --  multi-arm gain drop of the renal integrator drives the cascade
# ===========================================================================
# The kidney node (SIX2, the volume's renal integrator) loses gain as nephrons are lost. The CKD-MBD
# cascade is the SAME loop-gain-drop mode applied to SEVERAL arms at once: phosphate excretion weakens
# (PO4 up, err = load/k), renal 1a-hydroxylase falls (1,25-vitD down), gut Ca absorption falls (Ca down),
# and the CaSR comparator raises PTH (secondary hyperparathyroidism). All reuse ou_setpoint + pth_curve.
_RENAL_GAIN_STAGES = [4.0, 3.0, 2.0, 1.0, 0.5]     # healthy -> advanced CKD (renal integrator gain falling)
_PO4_DIET_LOAD     = 1.0                            # dietary phosphate drive the failing kidney must excrete


def ckd_mbd_cascade():
    """Step the renal integrator gain DOWN and read the four cascade variables. Each is anchored to a
       reused law: PO4 offset = load/k_renal (ou_setpoint); vitD ~ k_renal/k_healthy (1a-hydroxylase arm);
       Ca driven DOWN by the vitamin-D deficit; PTH = pth_curve(Ca) rises as Ca falls (secondary HPT)."""
    k0 = _RENAL_GAIN_STAGES[0]
    pth_baseline = loops.pth_curve(1.0)                     # endogenous PTH at the normal setpoint
    rows = []
    for k in _RENAL_GAIN_STAGES:
        po4 = 1.0 + _offset(k, _PO4_DIET_LOAD)             # phosphate rises: weaker excretion arm, err=load/k
        vitd = round(k / k0, 5)                            # 1,25-vitD falls with renal 1a-hydroxylase capacity
        ca = round(1.0 - 0.30 * (1.0 - vitd), 5)           # less gut Ca (vitD-dependent) -> Ca tends down
        pth = loops.pth_curve(ca)                          # CaSR comparator: lower Ca -> higher PTH (2ndary HPT)
        rows.append(dict(renal_gain=k, serum_po4=round(po4, 5), vitamin_d=vitd, serum_ca=ca,
                         pth=round(pth, 5), ca_x_po4=round(ca * po4, 5)))
    # monotonicity of the cascade as the renal gain falls (stages already ordered high->low gain)
    po4s = [r["serum_po4"] for r in rows]; vitds = [r["vitamin_d"] for r in rows]
    cas = [r["serum_ca"] for r in rows]; pths = [r["pth"] for r in rows]; prods = [r["ca_x_po4"] for r in rows]
    mono_up = lambda xs: all(xs[i] <= xs[i + 1] + 1e-9 for i in range(len(xs) - 1))
    mono_dn = lambda xs: all(xs[i] >= xs[i + 1] - 1e-9 for i in range(len(xs) - 1))
    # The FOUR primary KDIGO cascade signs are the gating claim (each cleanly monotone in the falling
    # renal gain). The Ca x PO4 product is a DERIVED downstream quantity: it is near-normal early (a small
    # early dip as Ca falls before PO4 retention dominates -- faithful to early-CKD product control) and
    # CLIMBS to the precipitation ceiling only in ADVANCED CKD. We report that honestly, not as monotone.
    primary_cascade = bool(mono_up(po4s) and mono_dn(vitds) and mono_dn(cas) and mono_up(pths))
    advanced_prods = prods[-3:]                                   # the advanced stages (k <= 2.0)
    product_climbs_advanced = bool(prods[-1] > prods[0] + 1e-9 and mono_up(advanced_prods))
    return dict(
        stages=rows,
        phosphate_rises=bool(mono_up(po4s)),
        vitamin_d_falls=bool(mono_dn(vitds)),
        calcium_falls=bool(mono_dn(cas)),
        pth_rises_secondary_hyperparathyroidism=bool(mono_up(pths)),
        pth_above_baseline_in_advanced_ckd=bool(pths[-1] > pth_baseline),
        ca_po4_product_near_normal_early=bool(abs(prods[1] - prods[0]) < 0.1),   # not a runaway early
        ca_po4_product_climbs_to_ceiling_in_advanced_ckd=product_climbs_advanced,
        ca_po4_product_start=round(prods[0], 5), ca_po4_product_advanced=round(prods[-1], 5),
        cascade_direction_reproduced=primary_cascade,
        anchor="KDIGO 2017 CKD-MBD: falling GFR -> phosphate retention, 1,25-vitD deficiency, hypocalcemia "
               "tendency, secondary hyperparathyroidism; Ca x PO4 product drives vascular calcification",
        grade="[L] KDIGO CKD-MBD cascade; [V] the four primary signs PO4 up / vitD down / Ca down / PTH up "
              "(secondary HPT) all monotone in the falling renal gain; the Ca x PO4 product is near-normal "
              "early and climbs to the ceiling in advanced CKD; [O] absolute per-stage progression timing",
    )


# ===========================================================================
# G4  HUMORAL HYPERCALCEMIA OF MALIGNANCY (PTHrP)  --  setpoint drift UP (inverse of T1)
# ===========================================================================
# PTHrP acts at the PTH receptor like PTH but is tumor-autonomous: the CaSR comparator cannot suppress it.
# In the setpoint-drift plant (PTH effector vs a constant loss; setpoint_failure.setpoint_drift), an
# exogenous UNSUPPRESSIBLE effector E relocates the defended calcium UPWARD. This is the exact inverse of
# the T1 allosteric set-point reset (which relocates it back DOWN). Clinical fingerprint reproduced:
# endogenous PTH is SUPPRESSED while Ca is high (CaSR loop intact; it just cannot turn off a foreign drive).
_M_CASR  = 3.0          # CaSR comparator Hill slope (as elsewhere in the volume)
_PMIN, _PMAX = 0.1, 1.0
_G_EFF   = 2.0          # PTH effector gain (as in setpoint_failure)
_PTHRP_LEVELS = [0.0, 0.10, 0.20, 0.30]   # exogenous PTHrP drive (0 = no tumor; dimensionless effector units)


def _settle_hhm(E, T=400.0, dt=0.02):
    """Deterministic settle of the calcium loop with an exogenous, NON-suppressible PTHrP effector E.
       dca = g_eff*PTH(ca) + E - loss, loss calibrated so E=0 -> defended ca = 1.0 (normal). PTH(ca) is
       the CaSR-controlled endogenous arm (suppressible); E is the tumor drive (not suppressible)."""
    loss = _G_EFF * (_PMIN + _PMAX) / 2.0                  # E=0 fixed point: PTH* = mean -> ca = setpoint = 1.0
    ca = 1.0; n = int(T / dt)
    for _ in range(n):
        P = loops.pth_curve(ca, 1.0, _M_CASR, _PMIN, _PMAX)
        ca += dt * (_G_EFF * P + E - loss)
    endo_pth = loops.pth_curve(ca, 1.0, _M_CASR, _PMIN, _PMAX)
    return float(ca), float(endo_pth)


def hhm_pthrp():
    """Sweep the PTHrP drive: defended calcium rises monotonically (hypercalcemia) while endogenous PTH
       is suppressed below baseline -- the humoral-hypercalcemia fingerprint, and the inverse of T1."""
    loops.seed_everything()
    pth_baseline = loops.pth_curve(1.0, 1.0, _M_CASR, _PMIN, _PMAX)   # = (pmin+pmax)/2 = 0.55
    rows = []
    for E in _PTHRP_LEVELS:
        ca, endo = _settle_hhm(E)
        rows.append(dict(pthrp_drive=E, defended_calcium=round(ca, 5), endogenous_pth=round(endo, 5),
                         endogenous_pth_suppressed=bool(endo < pth_baseline - 1e-6)))
    cas = [r["defended_calcium"] for r in rows]
    tumor = rows[-1]                                       # the with-tumor case (highest PTHrP)
    return dict(
        levels=rows, pth_baseline=round(pth_baseline, 5),
        # (1) defended calcium rises monotonically with the PTHrP drive (setpoint drift UP)
        calcium_rises_with_pthrp=bool(all(cas[i] <= cas[i + 1] + 1e-9 for i in range(len(cas) - 1))),
        # (2) with tumor present the defended calcium is hypercalcemic (above the normal setpoint)
        hypercalcemia_when_tumor_present=bool(tumor["defended_calcium"] > 1.0 + 1e-3),
        # (3) the clinical fingerprint: endogenous PTH SUPPRESSED despite high Ca (unlike primary hyperPTH)
        endogenous_pth_suppressed_despite_high_ca=bool(tumor["endogenous_pth_suppressed"]),
        # (4) this is the inverse of the T1 reset: T1 moves the defended value DOWN, PTHrP moves it UP
        inverse_of_T1_setpoint_reset="T1 allosteric reset relocates the defended value DOWN toward normal; "
                                     "an unsuppressible PTHrP drive relocates it UP -- same comparator, opposite sign",
        anchor="humoral hypercalcemia of malignancy: tumor PTHrP acts at PTH1R, is NOT under CaSR feedback "
               "-> hypercalcemia with SUPPRESSED endogenous PTH (Stewart 2005 NEJM; PTHrP standard literature)",
        grade="[L] PTHrP humoral-hypercalcemia mechanism; [V] defended Ca drifts UP monotone in PTHrP with "
              "endogenous PTH suppressed (fingerprint), the inverse of the T1 reset; [O] absolute hypercalcemia level",
    )


# ===========================================================================
# status (frontier-style honest roll-up)
# ===========================================================================
def status():
    loops.seed_everything()
    mg = magnesium_failures()
    ckd = ckd_mbd_cascade()
    hhm = hhm_pthrp()

    mg_ok = bool(mg["hypo_worse_than_healthy"] and mg["hyper_worse_than_healthy"]
                 and mg["ratio_matches_load_over_k"] and mg["variance_blows_up"])
    ckd_ok = bool(ckd["cascade_direction_reproduced"] and ckd["pth_above_baseline_in_advanced_ckd"]
                  and ckd["ca_po4_product_climbs_to_ceiling_in_advanced_ckd"])
    hhm_ok = bool(hhm["calcium_rises_with_pthrp"] and hhm["hypercalcemia_when_tumor_present"]
                  and hhm["endogenous_pth_suppressed_despite_high_ca"])
    demonstrations_pass = bool(mg_ok and ckd_ok and hhm_ok)

    return {
        "_what": "Tier-2 disease-coverage increment: magnesium (G2), CKD-MBD + secondary hyperparathyroidism "
                 "(G3) and humoral hypercalcemia of malignancy / PTHrP (G4) modelled by REUSING the six "
                 "failure modes and the volume's own load/k law + PTH comparator -- no new primitive",
        "G2_magnesium": mg,
        "G3_ckd_mbd": ckd,
        "G4_humoral_hypercalcemia_pthrp": hhm,
        "G2_magnesium_pass": mg_ok,
        "G3_ckd_mbd_pass": ckd_ok,
        "G4_hhm_pass": hhm_ok,
        "demonstrations_pass": demonstrations_pass,
        "reused_failure_modes": {
            "G2": "loop-gain drop / buffer-arm failure (ou_setpoint err=load/k)",
            "G3": "multi-arm loop-gain drop of the renal integrator (ou_setpoint + pth_curve)",
            "G4": "setpoint drift UP -- the inverse of the T1 allosteric reset (pth_curve)",
        },
        "grade": "[L] cited setpoints/variants/guidelines (Mg ~0.85 mM; TRPM6/Gitelman; KDIGO CKD-MBD; PTHrP "
                 "Stewart 2005); [V] each disease's reproduced direction via a reused failure mode + the "
                 "volume's load/k law; [O] absolute excursion magnitudes, CKD per-stage timing, hypercalcemia level",
    }


if __name__ == "__main__":
    s = json.dumps(status(), sort_keys=True)
    print(json.dumps(status(), indent=1))
    print("sha:", hashlib.sha256(s.encode()).hexdigest()[:12])
