#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
neuropathic_pain_levers.py  —  §22 neuro-NATIVE disease reading: neuropathic / sensitised
                               pain as a firing-threshold shift, and the three improvement
                               levers, derived on THIS volume's own R19 engine.

SCOPE (VP_FRAMEWORK_MAP ownership contract). The primary somatosensory nociceptor is a
NEURO entity (this volume's sec.10 transduction, sec.12/sec.20 sensory atlas; master PRDM12,
Na_V1.7 = SCN9A). neuropathic pain is an ACQUIRED, dynamics-key condition — peripheral nerve
injury re-expresses/up-regulates depolarising channels (e.g. Na_V1.3) and a sensitising drive
(NGF/CGRP) LOWERS the firing threshold, so an innocuous input now fires the cell (allodynia)
and the cell fires un-provoked (spontaneous pain). That is exactly the firing-threshold the
shared R19 element runs, so it is owned HERE by dynamics. The monogenic pain channelopathies
named in the anchor below (inherited erythromelalgia, PEPD, CIP/CIPA) are gene-key ENTITIES
owned by disease_wp; this module owns only the THRESHOLD DYNAMICS and cross-references that
volume for the named entity. The FELT/affective pain is the Felt Cognition volume's; this
layer moves only the peripheral afferent firing-threshold term.

THE MODEL (one R19 element, nothing fitted).
  A nociceptor membrane element is the locked R19 switch ds/dt = g s - s^3 + h. From its
  quiescent rest s0 = -sqrt(g), a peripheral SENSITISATION bias b >= 0 slides the operating
  point s* = settle(g, b) toward the yield point. Two locked readings of the SAME element:
    * FIRING-THRESHOLD MARGIN   T(b) = spinodal(g) - b           (|h_sp| margin to the flip)
    * AFFERENT GAIN (1/k)       chi(b) = 1 / (3 s*^2 - g)        (restoring-curvature inverse)
  chi diverges as b -> spinodal(g) (saddle-node critical gain = allodynia/hyperalgesia). The
  baseline (b=0) gain is 1/(2g). Each of the three analgesic levers lowers the EFFECTIVE bias
  b_eff = b - delta (delta a STRUCTURAL fraction of the sensitisation removed, NOT a dose):
    L1 reduce inward current (Na_V/Ca_V/ASIC/P2X/TRP)  -> removes depolarising drive
    L2 increase outward K+ (open K_V7)                 -> hyperpolarises away from yield
    L3 remove the NGF/CGRP sensitising drive           -> un-does the sensitisation
  so for ALL THREE: T rises by delta (raise the firing threshold = the analgesic goal) and chi
  falls monotonically back toward the baseline 1/(2g). One substrate, one effect, three doors.

GRADES (honest):
  * T(b), chi(b), the monotone de-sensitisation, the baseline 1/(2g) are [V]/[F] (locked forms).
  * channelopathy DIRECTION (LOF -> no firing -> CIP; GOF -> spontaneous firing -> IEM/PEPD) is
    [V/F] anchored to measured phenotypes (cited).
  * lever -> drug-class placement is [F] structural (cited validated classes).
  * delta, absolute firing magnitude, potency, dose, in-vivo selectivity, efficacy are [O].
  * the felt/affective pain is mind's. No molecule designed; nothing prescribes.

Run:  python3 neuropathic_pain_levers.py  ->  expected/neuropathic_pain_levers.json
"""
import os, sys, json, math

HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
EXPECT = os.path.join(HERE, "expected")
sys.path.insert(0, ENGINE)
import vp_neuro_engine as VN     # spinodal/barrier/settle/sdot — the LOCKED R19 forms

# nociceptor master-gene gamma (measured, inherited from this volume's sec.20 atlas) sets the
# element's threshold scale. SCN9A (Na_V1.7) is the canonical peripheral firing gate.
GAMMA_NOCICEPTOR = 1.4014   # SCN9A, identical to repro/neuro/_engine/data/full_sensory_gamma.json


def restoring_curvature(g, b):
    """k = 3 s*^2 - g at the operating point bias b settles to (from s0 = -sqrt(g)).
    The afferent gain is 1/k; k = 2g at b=0 (stiffest, normal sensitivity)."""
    s_star = VN.settle(g, abs(b), s0=-math.sqrt(g))
    return 3.0 * s_star * s_star - g


def afferent_gain(g, b):
    k = restoring_curvature(g, b)
    return float("inf") if k <= 0.0 else 1.0 / k


def firing_threshold_margin(g, b):
    """|h_sp| margin: how much extra drive still fits before the flip. spinodal(g) - b."""
    return VN.spinodal(g) - abs(b)


LEVERS = {
    "L1": "reduce the inward (excitatory) current (block depolarising Na_V/Ca_V/ASIC/P2X/TRP) -> lower the effective sensitisation bias",
    "L2": "increase the outward K+ current (open K_V7) -> hyperpolarise away from yield -> lower the effective bias",
    "L3": "remove the up-stream NGF/CGRP sensitising drive -> un-do the sensitisation -> lower the effective bias",
}


def lever_de_sensitises(g, b0_frac=0.60):
    """A sensitised nociceptor at b0 = b0_frac * spinodal (peripheral/central sensitisation).
    Apply each lever at increasing STRUCTURAL strength delta and read T = spinodal - b_eff and
    chi = afferent_gain. For every lever: T rises monotonically (the analgesic goal) and chi
    falls monotonically back toward the baseline 1/(2g). Emergent from R19; nothing fitted."""
    sp = VN.spinodal(g)
    b0 = b0_frac * sp
    baseline_gain = afferent_gain(g, 0.0)             # 1/(2g)
    sens_gain = afferent_gain(g, b0)                  # elevated (hypersensitivity)
    deltas = [0.0, 0.25 * b0, 0.50 * b0, 0.75 * b0, b0]   # up to full reversal of the sensitisation
    sweep = []
    all_T_rise = all_gain_fall = True
    prevT = prevG = None
    for d in deltas:
        b_eff = max(0.0, b0 - d)
        T = firing_threshold_margin(g, b_eff)
        chi = afferent_gain(g, b_eff)
        if prevT is not None and not (T > prevT - 1e-12):
            all_T_rise = False
        if prevG is not None and not (chi < prevG + 1e-12):
            all_gain_fall = False
        sweep.append(dict(delta=round(d, 6),
                          firing_threshold_margin=round(T, 6),
                          afferent_gain=round(chi, 6)))
        prevT, prevG = T, chi
    returns_to_baseline = abs(sweep[-1]["afferent_gain"] - baseline_gain) < 1e-6
    return dict(
        gamma=g, spinodal=round(sp, 6),
        sensitisation_bias_b0=round(b0, 6), b0_fraction_of_spinodal=b0_frac,
        baseline_gain_1_over_2g=round(baseline_gain, 6),
        sensitised_gain=round(sens_gain, 6),
        gain_amplification=round(sens_gain / baseline_gain, 4),
        levers=LEVERS,
        note="shown once for one element; L1/L2/L3 are identical in direction (all lower b_eff)",
        sweep=sweep,
        all_T_rise_monotone=all_T_rise,
        all_gain_fall_monotone=all_gain_fall,
        full_reversal_returns_to_baseline=returns_to_baseline,
    )


CHANNELOPATHY_ANCHOR = {
    "title": "Channelopathy direction anchor — measured biology fixes the firing-threshold direction",
    "axis": "the nociceptor firing threshold is the pain knob: lower it -> more pain, raise it -> less pain",
    "anchors": [
        dict(locus="SCN9A (Na_V1.7)", dna_change="loss-of-function / null",
             threshold_direction="firing threshold -> infinity (gate never opens)",
             measured_phenotype="congenital insensitivity to pain (no pain under any circumstance)",
             owns_entity="disease_wp (gene-key)", citation="Cox 2006 Nature 444:894; Goldberg 2007 Clin Genet 71:311",
             grade="[V/F] direction anchored to measured phenotype"),
        dict(locus="SCN9A (Na_V1.7)", dna_change="gain-of-function lowering activation threshold",
             threshold_direction="firing threshold lowered (gate opens too easily)",
             measured_phenotype="inherited erythromelalgia (burning extremity pain)",
             owns_entity="disease_wp (gene-key)", citation="Drenth 2005 J Invest Dermatol 124:1333; Yang/Waxman",
             grade="[V/F] direction anchored to measured phenotype"),
        dict(locus="SCN9A (Na_V1.7)", dna_change="gain-of-function impairing inactivation",
             threshold_direction="sustained firing (gate fails to re-close)",
             measured_phenotype="paroxysmal extreme pain disorder (PEPD)",
             owns_entity="disease_wp (gene-key)", citation="Fertleman 2006; Estacion 2008 J Neurosci 28:11079",
             grade="[V/F] direction anchored to measured phenotype"),
        dict(locus="NTRK1 (TrkA)", dna_change="loss-of-function",
             threshold_direction="nociceptor developmental arm absent",
             measured_phenotype="congenital insensitivity to pain with anhidrosis (CIPA)",
             owns_entity="disease_wp (gene-key)", citation="Indo 1996 Nat Genet 13:485",
             grade="[V/F] direction anchored to measured phenotype"),
        dict(locus="SCN10A (Na_V1.8)", dna_change="pharmacological closed-state stabilisation (VSD2 binder)",
             threshold_direction="firing threshold RAISED (gate held closed) — the realised analgesic move",
             measured_phenotype="approved non-opioid analgesia for moderate-severe acute pain",
             owns_entity="machine (dynamics; realised L1)", citation="suzetrigine (VX-548/Journavx) FDA 2025-01-30",
             grade="[V/F] direction anchored to approved mechanism (magnitudes [O])"),
    ],
    "reading": ("The two DNA directions bracket the lever map: a LOF that drives the threshold to "
                "infinity ABOLISHES pain (CIP), and a GOF that lowers it CAUSES spontaneous pain "
                "(IEM/PEPD). The realised analgesic (Na_V1.8 closed-state stabiliser) sits on the "
                "SAME axis, pushed the protective way. So 'raise the firing threshold' is not an "
                "analogy — it is the measured pain axis, and the three levers are three ways onto it."),
}


# neuro-native disease -> lever pointer (which improvement lever, which cited validated class)
DISEASE_POINTERS = [
    dict(disorder="Peripheral neuropathic pain (post-injury, e.g. diabetic/post-herpetic)",
         mechanism="injury up-regulates Na_V1.3/Na_V1.7-Na_V1.8 traffic + NGF drive -> threshold lowered, gain up",
         levers=["L1", "L2", "L3"],
         pointer_classes="alpha2delta-1 gabapentinoids (CACNA2D1); Na_V1.8/Na_V1.7-selective (SCN10A/SCN9A); "
                         "K_V7 openers (KCNQ2/3/5); anti-NGF (NGF/NTRK1)"),
    dict(disorder="Trigeminal / migraine-associated pain (CGRP-driven)",
         mechanism="CGRP sensitising drive lowers the afferent threshold (validated in migraine)",
         levers=["L3"],
         pointer_classes="anti-CGRP mAbs / gepants (CALCA/CALCB/CALCRL/RAMP1)"),
    dict(disorder="Inflammatory / nociplastic pain (tissue acidosis + heat sensitisation)",
         mechanism="ASIC/TRPV1 inward current rises with acidosis/heat -> threshold lowered",
         levers=["L1"],
         pointer_classes="ASIC blockers (ASIC1/ASIC3); TRPV1 modulators; P2X3 (P2RX3)"),
    dict(disorder="Inherited erythromelalgia / PEPD (Na_V1.7 GOF)",
         mechanism="GOF lowers/sustains the firing gate -> spontaneous/triggered pain (gene-key entity = disease_wp)",
         levers=["L1"],
         pointer_classes="Na_V1.7-selective block (SCN9A); carbamazepine in PEPD (cited)"),
    dict(disorder="Refractory / severe central pain",
         mechanism="presynaptic N-type Ca2+ release (dorsal horn) drives the central gain",
         levers=["L1"],
         pointer_classes="N-type Ca_V2.2 block (CACNA1B, ziconotide, intrathecal)"),
]


def main():
    os.makedirs(EXPECT, exist_ok=True)
    g = GAMMA_NOCICEPTOR
    desens = lever_de_sensitises(g)
    out = dict(
        module="22-neuropathic-pain-firing-threshold",
        scope=("neuro-native acquired/dynamics-key reading of nociceptor sensitisation; gene-key "
               "monogenic pain channelopathies are disease_wp entities, cross-referenced only"),
        firewall=("peripheral afferent firing-threshold term only; delta is structural (not a dose); "
                  "every clinical magnitude is [O]; the felt/affective pain is the Felt Cognition volume's; "
                  "no molecule designed; nothing prescribes"),
        master_gene="PRDM12 (lineage) · SCN9A/Na_V1.7 (firing gate)",
        de_sensitisation=desens,
        channelopathy_anchor=CHANNELOPATHY_ANCHOR,
        disease_lever_pointers=DISEASE_POINTERS,
    )
    json.dump(out, open(os.path.join(EXPECT, "neuropathic_pain_levers.json"), "w"), indent=1)

    print("=" * 68)
    print("§22 neuropathic-pain firing-threshold + three improvement levers")
    print("-" * 68)
    print(f"nociceptor gamma (SCN9A)   : {g}")
    print(f"spinodal |h_sp|            : {desens['spinodal']}")
    print(f"baseline gain 1/(2g)       : {desens['baseline_gain_1_over_2g']}")
    print(f"sensitised gain (b0=.6 sp) : {desens['sensitised_gain']}  (x{desens['gain_amplification']} amplification)")
    print(f"all levers RAISE threshold : {desens['all_T_rise_monotone']}")
    print(f"all levers LOWER gain      : {desens['all_gain_fall_monotone']}")
    print(f"full reversal -> baseline  : {desens['full_reversal_returns_to_baseline']}")
    print(f"channelopathy anchors      : {len(CHANNELOPATHY_ANCHOR['anchors'])} (LOF/GOF bracket the axis)")
    print(f"disease lever pointers     : {len(DISEASE_POINTERS)}")
    print("=" * 68)

    ok = (desens["all_T_rise_monotone"] and desens["all_gain_fall_monotone"]
          and desens["full_reversal_returns_to_baseline"])
    if not ok:
        sys.exit("FAIL: de-sensitisation did not behave monotonically / return to baseline")
    print("PASS — every lever raises the firing threshold and returns the gain to baseline")


if __name__ == "__main__":
    main()
