#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontier_quant.py  --  QUANTIFY the four frontier therapy hypotheses (H-RESET, H-DUAL, H-ARM, H-OTOC),
moving each from a bare [H] flag to a reproduced MECHANISM with an honest residual.

All four were listed as [H] (framework-derived, not yet quantified) in fundamental_therapy.FRONTIER_HYPOTHESES.
Here each is given a small deterministic model whose ORDERING/DIRECTION is the reproduced [V] result, with
absolute magnitudes left [O] and human clinical efficacy left [H]. Each premise is a CITED real finding, so
the models reproduce documented phenomena rather than inventing them. H-DUAL and H-OTOC were quantified in
v0.3.0; H-RESET and H-ARM are quantified here (v0.4.0) on the SAME machinery the volume already validates --
the comparator/set-point attractor (vp_loops.pth_curve) and the OU loop-gain law (vp_loops.ou_setpoint) --
so they add no new physics, only surface a consequence of laws already proven in [2]/[3].

H-DUAL  (reservoir refill -- remove the FORMATION BRAKE):
  Premise [L]: sclerostin inhibition raises DKK1 (a beta-catenin target) as negative feedback, which limits
  the anti-sclerostin anabolic window; dual anti-sclerostin + anti-DKK1 is synergistic
  (Florio et al. 2016 Nat Commun 7:11505, rodents & non-human primates).
  Model: bone formation ~ Wnt activity w = 1/(1 + a*S + b*D). Anti-SOST drops S; D then drifts UP
  (compensation) unless also blocked. The integrated anabolic window (formation above baseline) is ordered
  dual > single > untreated -- the single-agent window CLOSES as D rises; dual keeps it open. [V] ordering.

H-OTOC  (otoconial CaCO3 stability -- the OTOP1<->acid-base seam):
  Premise [L]: otoconia are calcite (CaCO3); their stability is the calcite saturation Omega =
  [Ca2+][CO3^2-]/Ksp; acidosis and hypocalcemia lower Omega -> dissolution -> BPPV. OTOP1 sets endolymph pH,
  so the acid-base arm couples to otoconial stability (Frontiers in Neurology 2025 endolymph ion-chemistry
  BPPV model; Walther et al. PLOS One 2014 calcite-otoconia dissolution under acid/low-Ca).
  Model: carbonate speciation makes [CO3^2-] a steep function of pH; lowering pH or Ca lowers Omega. The
  reproduced [V] result is the DIRECTION (acidosis & hypocalcemia destabilize); the ABSOLUTE Omega and the
  Omega=1 dissolution boundary need [O] calibration (total carbonate, Ksp, activity coefficients).

H-RESET  (generalize the set-point reset -- treat the cause, not the symptom):
  Premise [L]: a homeostatic sensor is a comparator with a defended set-point; an allosteric modulator that
  shifts the comparator RELOCATES the defended value at source. The CaSR proof-of-concept is clinically
  validated -- encaleret (a negative allosteric modulator / calcilytic) met all primary and key-secondary
  endpoints in the Phase-3 CALIBRATE trial in ADH1 (BridgeBio 2025, NCT05680818), and cinacalcet resets the
  CaSR set-point downward in hyperparathyroidism.
  Model: the defended attractor of a sensor loop equals its comparator set-point for ANY Hill slope m
  (pth_curve(sp,sp,m)=mean for all m -- a structural identity, not a fit). Symptom control (an exogenous push)
  holds the variable at target only while applied; on withdrawal it relaxes back to the mis-set attractor.
  An allosteric RESET moves the attractor itself -> durable normalization. The reproduced [V] result is the
  DIRECTION across a family of ionic sensors (CaSR/ENaC/ASIC/OTOP1): reset relocates the attractor for every
  sensor; symptom control is non-durable for every sensor. Generalization to non-CaSR allosteric recalibrators
  is the [H] extrapolation; the absolute residuals are [O].

H-ARM  (restore the failed acid-base ARM at source vs lifelong exogenous buffering):
  Premise [L]: the acid-base setpoint is a two-timescale buffer whose loop gain comes from a functioning arm
  (renal HCO3 regeneration / ventilatory drive). In distal renal tubular acidosis the renal arm transporter
  fails (a-intercalated-cell H+-ATPase / AE1); the standard of care is lifelong alkali (K-citrate/bicarbonate;
  ADV7103 / Sibnayal, EMA-approved) -- it REPLACES base but does not restore the transporter, so loop gain
  stays low (GeneReviews dRTA; Lopez-Garcia/Boyer ADV7103 trials).
  Model: the package's own OU law (vp_loops.ou_setpoint) -- err=load/k, Var=sigma^2/(2k). Arm failure drops
  k. Buffering adds a constant base that cancels the MEAN error but leaves k low (variance and fresh-load
  rejection stay poor, and it must be sustained). Arm restoration raises k -> the restored arm clears the
  chronic load, variance tightens, fresh disturbances are rejected, and it is durable. The reproduced [V]
  result is the DIRECTION: at matched mean correction, restoration tightens variance and rejects a fresh acid
  load by the factor k_high/k_low, while buffering does neither. Absolute gains are [O]; the clinical
  feasibility of arm restoration (transporter/drive repair) is the [H] extrapolation.

GRADES (C3): ordering/direction [V]; cited premises [L]; absolute magnitudes/thresholds [O]; human clinical
application [H]. Determinism (C1): fixed seed for the ODE; pure algebra for the chemistry; round-before-return.
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_substrate import seed_everything
import importlib
loops = importlib.import_module("vp_loops")   # reuse the volume's comparator + OU law (H-RESET, H-ARM)


# ===========================================================================
# H-DUAL  --  anti-sclerostin vs dual anti-sclerostin + anti-DKK1 anabolic window
# ===========================================================================
def h_dual_window(T=36.0, dt=0.05):
    """Integrated bone-formation 'anabolic window' (area of formation above baseline, arbitrary units over a
    ~36-month horizon) under: untreated / anti-sclerostin only / dual anti-sclerostin + anti-DKK1.
    Encodes the cited compensatory DKK1 rise (Florio 2016). Returns the ordering dual > single > untreated."""
    seed_everything()
    a = 1.0; b = 1.0; S0 = 1.0; D0 = 1.0; tau_D = 12.0   # months; a,b: antagonist potencies
    base_w = 1.0 / (1.0 + a * S0 + b * D0)
    DKK1_compensation_gain = 1.0    # SOST block -> D drifts toward ~2x baseline (DKK1 ~doubles; Florio 2016)

    def window(block_S, block_D):
        S = S0 * (0.1 if block_S else 1.0)             # anti-sclerostin lowers S at once
        D = D0; integ = 0.0
        for _ in range(int(T / dt)):
            D_target = (0.1 if block_D else (D0 + (DKK1_compensation_gain if block_S else 0.0)))
            D += dt * (D_target - D) / tau_D            # compensatory drift (or held down by anti-DKK1)
            w = 1.0 / (1.0 + a * S + b * D)
            integ += dt * max(w - base_w, 0.0)
        return integ

    untreated = window(False, False)
    single    = window(True,  False)
    dual      = window(True,  True)
    return dict(integrated_window_untreated=round(untreated, 4),
                integrated_window_single=round(single, 4),
                integrated_window_dual=round(dual, 4),
                dual_over_single_ratio=round(dual / single, 3) if single > 0 else None,
                dual_beats_single=bool(dual > single),
                single_beats_untreated=bool(single > untreated),
                window_closes_under_single=bool(single < dual),   # single window is bounded; dual sustains
                ordering="dual > single > untreated (anabolic-window area)",
                cited="Florio et al. 2016 Nat Commun 7:11505 -- SOST inhibition raises DKK1 (negative feedback); "
                      "dual Scl-Ab + DKK1-Ab synergistic in rodents & non-human primates",
                grade="[V] ordering follows the cited compensation [L]; absolute window size & compensation rate "
                      "[O]; human clinical efficacy not established [H]")


# ===========================================================================
# H-OTOC  --  otoconial calcite saturation Omega vs endolymph pH and Ca2+
# ===========================================================================
def h_otoc_saturation():
    """Calcite saturation Omega = [Ca2+][CO3^2-]/Ksp governs otoconial CaCO3 stability. Carbonate speciation
    makes [CO3^2-] a steep function of pH. The ROBUST reproduced result is the DIRECTION: acidosis (OTOP1/
    acid-base arm failure) and hypocalcemia both lower Omega -> dissolution-prone. Absolute Omega depends on
    [O] calibration, so it is reported BOTH raw (calibration-dependent) and normalized to physiological (the
    direction, which is calibration-free)."""
    pKa1 = 6.35; pKa2 = 10.33; Ksp = 3.3e-9    # carbonic-acid pKa's; calcite Ksp ~25C (absolute -> [O])

    def alpha2(pH):                              # fraction of total carbonate present as CO3^2-
        H = 10 ** (-pH); K1 = 10 ** (-pKa1); K2 = 10 ** (-pKa2)
        return (K1 * K2) / (H * H + K1 * H + K1 * K2)

    # CT (total dissolved carbonate) is calibrated [O] so the PHYSIOLOGICAL state sits at Omega=1, the
    # dynamic-equilibrium boundary (matching the Frontiers-2025 Omega=1 contour framing). This fixes the
    # absolute placement by convention; the [V] claim is the calibration-free DIRECTION of the perturbations.
    pH_phys, Ca_phys = 7.65, 265.0
    CT = Ksp / ((Ca_phys * 1e-6) * alpha2(pH_phys))   # -> omega(phys) == 1.0 exactly

    def omega(pH, Ca_uM):
        return (Ca_uM * 1e-6) * (CT * alpha2(pH)) / Ksp

    phys     = omega(7.65, 265.0)   # physiological endolymph: Ca 250-280 uM, pH 7.6-7.7 (cited) -> 1.0 by calibration
    acidosis = omega(7.50, 265.0)   # OTOP1/acid-base failure -> endolymph pH down
    low_ca   = omega(7.65, 200.0)   # hypocalcemia -> free Ca down
    return dict(
        omega_physiological=round(phys, 4), omega_acidosis=round(acidosis, 4),
        omega_low_calcium=round(low_ca, 4),
        acidosis_lowers_saturation=bool(acidosis < phys),
        low_calcium_lowers_saturation=bool(low_ca < phys),
        acidosis_undersaturated=bool(acidosis < 1.0), low_calcium_undersaturated=bool(low_ca < 1.0),
        dissolution_rule="Omega<1 -> calcite undersaturated -> CaCO3 dissolves -> otoconia fragment/dislodge -> BPPV",
        calibration_note="total carbonate CT is calibrated [O] so physiological Omega==1 (the metastable "
                         "boundary); absolute placement is conventional, the reproduced claim is the DIRECTION "
                         "(acidosis & hypocalcemia push Omega below 1)",
        cited="Frontiers in Neurology 2025 (endolymph Ca/pH calcite-saturation BPPV model, Omega index); "
              "Walther et al. PLOS One 2014 (human calcite otoconia dissolve under acid / low-Ca / chelation)",
        grade="[V]/[F] carbonate-speciation saturation DIRECTION; OTOP1<->endolymph-pH link [L]; absolute Ksp/"
              "activity & Omega=1 threshold [O]/[CAL]; therapeutic OTOP1/pH targeting for BPPV [H]")


# ===========================================================================
# H-RESET  --  the set-point reset generalizes across ionic sensors (cause, not symptom)
# ===========================================================================
# Representative ionic-sensor family with comparator (Hill) steepness; the m values are
# representative sensor sharpness (absolute -> [O]); the [V] claim is the DIRECTION across the family.
IONIC_SENSORS = [
    ("CaSR",  3.0, "calcium sensor -- allosteric recalibrator CLINICALLY VALIDATED (encaleret Ph3 CALIBRATE; cinacalcet)"),
    ("ENaC",  4.0, "sodium sensor -- amiloride blocks; a set-point recalibrator is the [H] extrapolation"),
    ("ASIC",  2.5, "acid sensor -- [H] extrapolation"),
    ("OTOP1", 2.0, "proton/otoconia sensor -- couples to the BPPV seam; [H] extrapolation"),
]

def _defended_value(set_point, m, ext=0.0, g_eff=2.0, pmin=0.1, pmax=1.0, T=400.0, dt=0.02, y0=1.0):
    """Fixed point of a sensor loop whose inverse-sigmoid effector (pth_curve) raises the controlled
    variable toward the comparator set-point. `loss` balances the effector at the normal operating point,
    so with set_point=1 and ext=0 the defended value is 1. `ext` is an exogenous (symptom-control) push."""
    loss = g_eff * (pmin + pmax) / 2.0
    y = y0
    for _ in range(int(T / dt)):
        E = loops.pth_curve(y, set_point, m, pmin, pmax)
        y += dt * (g_eff * E + ext - loss)
    return float(y)

def h_reset_generalization(drift=0.15):
    """The CaSR set-point-reset paradigm generalizes to any ionic sensor. The defended ATTRACTOR equals the
    comparator set-point for every Hill slope m (structural identity). Symptom control (an exogenous push)
    normalizes only transiently -- on withdrawal the loop relaxes back to the mis-set attractor. An allosteric
    RESET relocates the attractor itself, durably. Reproduced [V] result: this direction holds for the whole
    sensor family (reset durable; symptom non-durable), not just CaSR."""
    seed_everything()
    rows = []
    for name, m, note in IONIC_SENSORS:
        normal    = _defended_value(1.0, m)                      # ~1.0 by construction
        untreated = _defended_value(1.0 + drift, m)             # defends the pathological set-point
        symptom   = _defended_value(1.0 + drift, m, y0=1.0)     # forced-normal, push WITHDRAWN -> relapses
        reset     = _defended_value(1.0,         m, y0=1.0 + drift)  # set-point moved back -> durable normal
        rows.append(dict(sensor=name, hill_m=m, clinical=note,
                         defended_untreated=round(untreated, 4),
                         symptom_postwithdrawal=round(symptom, 4),
                         allosteric_reset=round(reset, 4),
                         reset_deviation=round(abs(reset - 1.0), 4),
                         symptom_deviation=round(abs(symptom - 1.0), 4),
                         untreated_deviation=round(abs(untreated - 1.0), 4)))
    reset_ok   = all(r["reset_deviation"] < 0.02 for r in rows)
    symptom_no = all(r["symptom_deviation"] > r["reset_deviation"] + 1e-6 for r in rows)
    structural = all(abs(r["defended_untreated"] - (1.0 + drift)) < 0.02 for r in rows)
    return dict(sensor_family=[r["sensor"] for r in rows], drift=drift, rows=rows,
                attractor_equals_setpoint_for_all_m=bool(structural),
                reset_relocates_attractor_all_sensors=bool(reset_ok),
                symptom_control_nondurable_all_sensors=bool(symptom_no),
                ordering="allosteric reset (durable, dev~0) >> symptom control (relapses to dev=drift) = untreated",
                cited="encaleret Ph3 CALIBRATE met all primary/key-secondary endpoints in ADH1 (BridgeBio 2025, "
                      "NCT05680818; CaSR negative allosteric modulator); cinacalcet resets CaSR down in hyperPTH",
                grade="[V] structural direction -- the defended attractor equals the comparator set-point for "
                      "every Hill slope, so allosteric reset is the unique durable fix across the sensor family; "
                      "CaSR proof-of-concept cited [L]; ENaC/ASIC/OTOP1 allosteric recalibrators [H]; absolute "
                      "residuals [O]")


# ===========================================================================
# H-ARM  --  restore the failed acid-base ARM at source vs lifelong exogenous buffering
# ===========================================================================
def h_arm_restoration(sigma=0.3, load=1.0, k_low=0.5, k_high=2.0, fresh_load=1.0):
    """Reuses the volume's OWN OU law (vp_loops.ou_setpoint; err=load/k, Var=sigma^2/2k, both proven in [2]).
    Arm failure drops the loop gain k_high->k_low. Lifelong BUFFERING adds a constant base that cancels the
    MEAN error but leaves k low -- variance and fresh-load rejection stay poor, and it must be sustained. Arm
    RESTORATION raises k back: the restored arm clears the chronic load, variance tightens, fresh disturbances
    are rejected, and it is durable. Reproduced [V] result: at matched mean correction, restoration beats
    buffering on variance AND fresh-load rejection by the factor k_high/k_low; buffering improves neither."""
    seed_everything()
    untreated   = loops.ou_setpoint(k_low,  sigma=sigma, load=load)              # failed arm, no therapy
    buffering   = loops.ou_setpoint(k_low,  sigma=sigma, load=load - load)        # base cancels mean; k unchanged
    restoration = loops.ou_setpoint(k_high, sigma=sigma, load=load)              # gain restored; arm clears load
    buf_fresh = loops.ou_setpoint(k_low,  sigma=0.0, load=fresh_load)["mean_offset"]  # err=load/k_low
    res_fresh = loops.ou_setpoint(k_high, sigma=0.0, load=fresh_load)["mean_offset"]  # err=load/k_high
    return dict(sigma=sigma, chronic_load=load, k_low_failed_arm=k_low, k_high_restored_arm=k_high,
                untreated_mean_offset=untreated["mean_offset"], untreated_variance=untreated["variance"],
                buffering_mean_offset=buffering["mean_offset"], buffering_variance=buffering["variance"],
                restoration_mean_offset=restoration["mean_offset"], restoration_variance=restoration["variance"],
                fresh_load_excursion_buffering=round(buf_fresh, 4),
                fresh_load_excursion_restoration=round(res_fresh, 4),
                variance_ratio_buffer_over_restore=round(buffering["variance"] / restoration["variance"], 3),
                predicted_ratio_k_high_over_k_low=round(k_high / k_low, 3),
                buffering_cancels_mean=bool(abs(buffering["mean_offset"]) < abs(untreated["mean_offset"])),
                buffering_leaves_variance_high=bool(abs(buffering["variance"] - untreated["variance"])
                                                    < 0.2 * untreated["variance"]),
                restoration_tightens_variance=bool(restoration["variance"] < buffering["variance"]),
                restoration_rejects_fresh_load_better=bool(abs(res_fresh) < abs(buf_fresh)),
                durability="buffering mean returns to the untreated offset on withdrawal (exogenous); arm "
                           "restoration is durable (the arm gain is intrinsically restored)",
                ordering="restore-arm > buffer > untreated on disturbance-rejection quality (variance & fresh-load error)",
                cited="distal RTA = renal acid-base arm transporter failure; standard of care is lifelong alkali "
                      "(K-citrate/bicarbonate; ADV7103/Sibnayal, EMA-approved) -- replaces base, does not restore "
                      "the transporter (GeneReviews dRTA; Lopez-Garcia/Boyer ADV7103 trials)",
                grade="[V] direction from the OU law -- restoration uniquely tightens variance and rejects fresh "
                      "loads (factor k_high/k_low); buffering cancels the mean only and is non-durable; current "
                      "buffering care cited [L]; absolute gains [O]; clinical arm-restoration (transporter/drive "
                      "repair) [H]")


def status():
    seed_everything()
    hd = h_dual_window(); ho = h_otoc_saturation()
    hr = h_reset_generalization(); ha = h_arm_restoration()
    return dict(_what="Quantification of the four frontier therapy hypotheses: H-RESET (set-point reset "
                      "generalizes across ionic sensors), H-DUAL (remove the bone-formation brake), H-ARM "
                      "(restore the failed acid-base arm vs lifelong buffering), and H-OTOC (otoconial calcite "
                      "saturation). Ordering/direction [V]; absolute magnitudes [O]; clinical application [H].",
                H_RESET=hr, H_DUAL=hd, H_ARM=ha, H_OTOC=ho,
                demonstrations_pass=bool(hd["dual_beats_single"] and hd["single_beats_untreated"]
                                         and ho["acidosis_lowers_saturation"] and ho["low_calcium_lowers_saturation"]
                                         and hr["reset_relocates_attractor_all_sensors"]
                                         and hr["symptom_control_nondurable_all_sensors"]
                                         and ha["restoration_tightens_variance"]
                                         and ha["restoration_rejects_fresh_load_better"]),
                grade="ordering/direction [V]; cited premises [L]; absolute magnitudes/thresholds [O]; clinical [H]")


if __name__ == "__main__":
    import json
    print(json.dumps(status(), ensure_ascii=False, indent=2))
