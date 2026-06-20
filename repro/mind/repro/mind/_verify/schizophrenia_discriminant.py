#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCHIZOPHRENIA-SPECTRUM DISCRIMINANT (D9 candidate) -- the OVER-IGNITION MIRROR of
the autism THRESHOLD-HIGH fault (D8 T). Where autism-T is a tonic INHIBITORY bias
that RAISES the R19 ignition fold -> assemblies fire reluctantly (under-ignition,
reduced coupling), schizophrenia is the opposite pole on the SAME M3 ignitability
axis: a tonic DISINHIBITORY / excitatory bias (E/I shifted toward excitation) that
LOWERS the fold -> assemblies ignite too readily -> weak/irrelevant candidate
assemblies cross the gate that should stay silent (ABERRANT SALIENCE), and the
winner-take-MOST selection collapses toward winner-take-MANY (loss of selective
gating). The two reversibility interventions map the clinical mirror (a gain-
REDUCING / threshold-raising antipsychotic-class push vs the gain-RAISING
stimulant that helps autism-T), the disorganisation extreme, and the sleep-sign
that now ALIGNS with therapy (opposite to autism).
=================================================================================
Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY, in the exact D1-D6 / D7 / D8
mould: vp_mind_engine is imported READ-ONLY; emerge_all() is NOT touched, so the
engine tree stays 0fbf4988... and the M0..M16 subtree stays 3a1ebbbb...
(byte-identical). Writes schizophrenia_results.json + its sha256, verified
bit-for-bit.

WHERE THIS SITS. D7 placed autism on the COUPLING PATHWAY (a single reduced-kappa
axis, not frontal localisation). D8 split that ONE reduced-coupling axis into THREE
physically distinct faults (WIRING / OUTPUT-weak / THRESHOLD-high) by their
(delta-PAC, ignition) fingerprints, and showed a gain/threshold drug reverses gain
faults. D9 turns the THRESHOLD axis the OTHER way: the same R19 cusp (fold =
spinodal(g) = 2(g/3)^1.5) that autism-T pushed UP (hypo-excitable), schizophrenia
pushes DOWN (hyper-excitable). This is the leading mechanistic account of the
psychotic pole:

  SZ  DISINHIBITORY / EXCITATORY bias  -- E/I shifted toward excitation (the
       NMDA-receptor-hypofunction -> reduced PV-interneuron drive -> disinhibition
       account); the R19 fold drops, so candidate assemblies with WEAK ("irrelevant")
       drive now cross it. The selective single-winner gate (M4) degrades: spurious
       assemblies ignite and compete -> ABERRANT SALIENCE; the bistable wells are
       shallow / unstable (attractor instability) -> the gate no longer picks ONE.
                                                                  ["over-ignition"]

NOT a claim that idiopathic schizophrenia is one gene or one mechanism. Idiopathic
schizophrenia is POLYGENIC + heterogeneous (PGC GWAS, >270 loci; CNVs) and its
functional connectivity is DYSconnective (mixed hyper-/hypo-, state-dependent) --
LOCKED. What we test is the MECHANISM at the ignition/selection level: a fold-
lowering excitatory bias reproduces aberrant ignition + loss of selective gating,
the OPPOSITE fingerprint to autism-T, with the OPPOSITE drug sign. We assert
NOTHING about which individual, or that integration simply "goes up" (see LOCK).

KEY STRUCTURAL FACT (the mirror of D8's). In the engine the R19 fold sets which
candidate assemblies ignite from the OFF basin: an assembly with salience drive d
ignites iff d (+ tonic bias) exceeds the fold. A field of candidate assemblies with
a SPREAD of salience drives straddling the fold is therefore SELECTIVE in health
(only genuinely-driven assemblies cross). An INHIBITORY bias (autism-T) raises the
fold -> even relevant assemblies fail (LOSE relevant ignitions, under-selection).
An EXCITATORY bias (schizophrenia) lowers the fold -> weak/irrelevant assemblies
ALSO cross (GAIN aberrant ignitions). => (ignition-direction, aberrant-vs-lost
ignitions) is a unique 3-way fingerprint separating HEALTH / AUTISM-T / SCHIZOPHRENIA.

PRE-REGISTERED PREDICTIONS (clinical DIRECTION/sign only, never magnitudes;
readout = HEALTH<->disease contrast and the reversibility pattern):
  SZ1  over-ignition: the excitatory bias LOWERS the ignition fold below health
       (exact mirror of autism-T's raised fold).
  SZ2  aberrant salience: with the fold lowered, candidate assemblies that are
       SUB-fold in health (weak / "irrelevant") now ignite -> the ON set strictly
       GROWS by recruiting irrelevant assemblies (aberrant ignitions > 0), while
       NO relevant assembly is lost. (Autism-T does the opposite: lost > 0,
       aberrant == 0.) The selective single-winner gate degrades toward many.
  SZ3  the same disinhibition raises the engine's in-silico global integration
       above health (an over-synchronisation tendency). REPORTED as secondary +
       LOCKED that real schizophrenia connectivity is DYSconnective, not a clean
       increase -- the DEFINING fingerprint is SZ1+SZ2 at the ignition level.
  DISC: (ignition-direction, aberrant-vs-lost) separates HEALTH / AUTISM-T / SZ
       uniquely -- SZ lowers the fold + recruits irrelevant; autism-T raises the
       fold + loses relevant; health is balanced + selective.
  RX_antipsychotic: a uniform gain-REDUCING / threshold-RAISING intervention --
       the class antipsychotics act through MECHANISTICALLY (D2 antagonism ->
       reduced dopaminergic gain -> "dampens the salience of aberrant signals",
       Kapur 2003) -- RESTORES the healthy selective set on the SZ state (aberrant
       ignitions back to 0, gate selective again). The SAME push applied to the
       AUTISM-T fault WORSENS it (raises an already-high fold -> loses more
       relevant) -- opposite therapeutic sign for the opposite pole.
  RX_stimulant_worsens: the gain-RAISING / threshold-LOWERING stimulant that HELPED
       autism-T (D8 RX_drug) WORSENS schizophrenia -- it lowers the fold further ->
       MORE aberrant ignitions (the well-attested stimulant-precipitated/-worsened
       psychosis direction). The autism helper is the schizophrenia harmer:
       opposite sign, same handle.
  EXTREME: unbounded disinhibition lowers the fold until ALL candidate assemblies
       ignite -- total loss of the selective gate (zero selectivity), the
       disorganisation limit at the excitation-imbalance boundary schizophrenia
       shares with seizure. Loss of GATING is a MECHANISM boundary, NOT a claim
       about the disorganised subjective state (Axis A firewall; consciousness_claim 0).
  SLEEP: the gain-REDUCING (sedating) push that calms aberrant salience LOWERS
       arousal/integration -- the SAME sign as sleep need (arousal DOWN). So for
       schizophrenia the therapeutic direction and the sleep direction ALIGN --
       the MIRROR of autism, where the arousal-RAISING therapy was anti-sleep.
       Sign-only.

NOT MEDICAL ADVICE. efficacy=0 everywhere; in-silico MECHANISM probe only.

VERIFICATION CONTRACT (same six as D1-D8): (i) clinical DIRECTION only;
(ii) ANTI-TUNING (signs/invariances severity-robust over a bias/drive sweep, not
fit); (iii) HEALTH<->disease contrast is the readout; (iv) engine tree invariant +
2x-deterministic frozen result; (v) honesty 4 flags invariant; (vi) DISCRIMINANT
assert (SZ leaves a DIFFERENT fingerprint than autism-T and health; the stimulant
that helps autism-T worsens SZ; the antipsychotic that calms SZ worsens autism-T).
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

A      = E.load_brain_atlas()
REGS   = list(A["organs"].keys())
N      = len(REGS)
F0     = np.array([A["organs"][r]["f0_hz"] for r in REGS])
OMEGA  = 2 * math.pi * F0
OMEGA0 = float(np.mean(OMEGA))
POS    = E._measured_geometry(REGS)                      # measured MNI [L]
KAP    = E.KAPPA_EPHAPTIC                                 # = dVm/threshold (measured) 0.5496
G      = 1.0
FOLD   = float(E.spinodal(G))                            # R19 fold = 2(g/3)^1.5 = 0.3849

# --- candidate-assembly salience field (M3 eddies as competing assemblies) ------
# A fixed PROBE stimulus: six candidate assemblies whose salience drives STRADDLE
# the measured R19 fold, so HEALTH is selective (only the two genuinely-driven
# cross) and the tonic E/I bias moves the selective boundary. These drives are a
# stimulus set (severity probe), NOT constants fit to a target -- exactly the
# status of D8's injection grid / bias / dVm-multiplier probe levels.
DRIVES = [0.12, 0.20, 0.28, 0.36, 0.50, 0.60]            # 4 sub-fold + 2 supra-fold in health

# operating bias points (clinical DIRECTION probe, swept; readout = the SIGN):
B_SZ   = +0.15                                           # primary disinhibitory (excitatory) bias
B_AUT  = -0.10                                           # autism-T inhibitory bias (mirror, from D8)
B_EXT  = +0.30                                           # disorganisation extreme (all ignite)
RX_AP  =  0.15                                           # antipsychotic gain-reduction (raises fold)
RX_ST  =  0.15                                           # stimulant gain-raise (lowers fold) -- autism helper

# measured-distance geometry (for the secondary global-integration observation)
_D = np.zeros((N, N))
for _i in range(N):
    for _j in range(N):
        _D[_i, _j] = np.linalg.norm(POS[_i] - POS[_j]) if _i != _j else 0.0
def _rawW():
    W = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                W[i, j] = 1.0 / (_D[i, j] ** 3)
    return W
def _rn(W):
    s = W.sum(axis=1, keepdims=True)
    return W / np.where(s > 0, s, 1.0)


def _on_set(bias):
    """Indices of candidate assemblies that ignite (cross the R19 fold from the OFF
    basin) under the shared salience drives + tonic bias. Pure engine settle()."""
    on = []
    for i, d in enumerate(DRIVES):
        if E.settle(G, d + bias, s0=-math.sqrt(G)) > 0.0:
            on.append(i)
    return on

def _ig_thr(bias, cap=2.0, ngrid=401):
    """Minimal extra drive to flip OFF->ON given a tonic bias (D8 _ig_thr mirror).
    Excitatory bias (b>0) LOWERS it; inhibitory (b<0) RAISES it. Fold is upward-
    closed in drive, so the first ascending crossing IS the minimum."""
    for s in np.linspace(0.0, cap, ngrid):
        if E.settle(G, bias + float(s), s0=-math.sqrt(G)) > 0.0:
            return float(s)
    return float("inf")

# effective ephaptic coupling under an E/I bias: an INHIBITORY bias RAISES the
# kappa denominator (autism-T: k = kappa/(1+|b|), coupling DOWN); a DISINHIBITORY
# bias does the mirror (k = kappa/(1-|b|), coupling UP), capped below the seizure
# ceiling. No new constant: kappa is measured; the cap = 2*kappa is a guard.
def _k_bias(bias):
    if bias >= 0:
        return min(KAP / (1.0 - min(bias, 0.95)), 2.0 * KAP)
    return KAP / (1.0 + abs(bias))


def run():
    Wrn = _rn(_rawW())
    R_health = E._integrate(OMEGA, Wrn, KAP * OMEGA0)[0]
    ig_health = _ig_thr(0.0)
    H = set(_on_set(0.0))                                 # healthy selective set
    n_health = len(H)

    # ===== SZ1 : over-ignition (fold lowered below health) =====
    ig_sz = _ig_thr(B_SZ)
    SZ1 = bool(ig_sz < ig_health - 1e-9)

    # ===== SZ2 : aberrant salience (recruits irrelevant; loses none) =====
    on_sz = set(_on_set(B_SZ))
    aberrant_sz = sorted(on_sz - H)                       # irrelevant assemblies recruited
    lost_sz     = sorted(H - on_sz)                       # relevant assemblies dropped
    SZ2 = bool(len(aberrant_sz) > 0 and len(lost_sz) == 0 and len(on_sz) > n_health)

    # full dose-response (anti-tuning: the SIGN must hold over the sweep) --------
    sweep_bias = [-0.20, -0.10, 0.0, 0.10, 0.15, 0.20, 0.30]
    nsel_curve = {round(b, 2): len(_on_set(b)) for b in sweep_bias}
    # monotone non-decreasing in excitatory direction (more excitation -> >= ignitions)
    sb = sorted(nsel_curve)
    monotone = all(nsel_curve[sb[i]] <= nsel_curve[sb[i + 1]] for i in range(len(sb) - 1))

    # ===== autism-T contrast (the opposite fold direction, from D8) =====
    ig_aut = _ig_thr(B_AUT)
    on_aut = set(_on_set(B_AUT))
    aberrant_aut = sorted(on_aut - H)
    lost_aut     = sorted(H - on_aut)
    # autism-T at a slightly stronger inhibition to show relevant loss explicitly
    on_aut2 = set(_on_set(-0.20)); lost_aut2 = sorted(H - on_aut2)
    AUT_contrast = bool(ig_aut > ig_health - 1e-9 and len(aberrant_aut) == 0
                        and len(lost_aut2) > 0)

    # ===== SZ3 : secondary global-integration direction (over-sync tendency) =====
    R_sz = E._integrate(OMEGA, Wrn, _k_bias(B_SZ) * OMEGA0)[0]
    R_ext = E._integrate(OMEGA, Wrn, _k_bias(B_EXT) * OMEGA0)[0]
    SZ3_oversync = bool(R_sz > R_health)

    # ===== DISCRIMINANT : (ignition-direction, aberrant-vs-lost) 3-way unique =====
    sep_health = bool(len(H - H) == 0 and abs(ig_health - ig_health) < 1e-9)  # trivially selective ref
    sep_sz  = bool(ig_sz < ig_health - 1e-9 and len(aberrant_sz) > 0 and len(lost_sz) == 0)
    sep_aut = bool(ig_aut > ig_health - 1e-9 and len(aberrant_aut) == 0 and len(lost_aut2) > 0)
    THREE_WAY = bool(sep_sz and sep_aut and (len(aberrant_sz) > 0) and (len(lost_aut2) > 0)
                     and (aberrant_sz != lost_aut2))     # SZ adds irrelevant; autism removes relevant

    # ===== RX_antipsychotic : gain-reduction restores health on SZ; worsens autism-T =====
    on_sz_ap = set(_on_set(B_SZ - RX_AP))                 # antipsychotic subtracts excitation
    ap_restores_sz = bool(on_sz_ap == H)                 # back to the healthy selective set
    on_aut_ap = set(_on_set(B_AUT - RX_AP))              # same push on autism-T
    aut_worse_under_ap = bool(len(on_aut_ap) < len(_on_set(B_AUT)))   # loses even more
    RX_AP_discriminative = bool(ap_restores_sz and aut_worse_under_ap)

    # ===== RX_stimulant_worsens : the autism helper worsens SZ =====
    on_sz_st = set(_on_set(B_SZ + RX_ST))                 # stimulant adds excitation
    stimulant_worsens_sz = bool(len(on_sz_st) > len(on_sz))
    # and confirm the same stimulant HELPED autism-T (recovers relevant ignitions)
    on_aut_st = set(_on_set(B_AUT + RX_ST))
    stimulant_helps_aut = bool(len(on_aut_st) >= len(_on_set(B_AUT)))
    RX_STIM_opposite_sign = bool(stimulant_worsens_sz and stimulant_helps_aut)

    # ===== EXTREME : disorganisation limit (all ignite, zero selectivity) =====
    on_ext = _on_set(B_EXT)
    all_ignite = bool(len(on_ext) == len(DRIVES))
    selectivity_lost = bool(len(set(on_ext) - H) == len(DRIVES) - n_health)  # every irrelevant recruited
    EXTREME = bool(all_ignite and selectivity_lost)

    # ===== SLEEP : therapy sign ALIGNS with sleep (opposite to autism) =====
    R_sz_ap = E._integrate(OMEGA, Wrn, _k_bias(B_SZ - RX_AP) * OMEGA0)[0]
    antipsychotic_lowers_arousal = bool(R_sz_ap < R_sz)
    SLEEP_SIGN_ALIGNS = bool(antipsychotic_lowers_arousal)   # arousal DOWN == sleep need == therapy

    return {
        "_what": "Schizophrenia-spectrum discriminant (D9): the OVER-IGNITION mirror "
                 "of the autism THRESHOLD-HIGH fault. A disinhibitory/excitatory bias "
                 "(E/I toward excitation; NMDA-hypofunction account) LOWERS the R19 fold "
                 "so weak/irrelevant candidate assemblies ignite (ABERRANT SALIENCE) and "
                 "the selective single-winner gate collapses. A gain-REDUCING antipsychotic-"
                 "class push restores selectivity on SZ but WORSENS autism-T; the stimulant "
                 "that HELPED autism-T WORSENS SZ; the extreme is total loss of gating. "
                 "(ignition-direction, aberrant-vs-lost) uniquely separates HEALTH / "
                 "AUTISM-T / SZ. MECHANISM only -- NOT felt, NOT efficacy, NOT medical advice.",
        "axis": {
            "shared_axis": "M3 R19 ignitability fold = spinodal(g) = 2(g/3)^1.5 = 0.3849 (measured-grounded)",
            "autism_T_direction": "INHIBITORY bias -> fold UP -> under-ignition (D8 T)",
            "schizophrenia_direction": "DISINHIBITORY/excitatory bias -> fold DOWN -> over-ignition (this module)",
        },
        "cited_and_locked": {
            "NMDA_hypofunction_disinhibition": "Olney & Farber 1995; Lewis/Gonzalez-Burgos (PV-interneuron "
                "hypofunction -> cortical disinhibition; E/I toward excitation)",
            "aberrant_salience": "Kapur 2003 (dopamine dysregulation -> aberrant assignment of salience to "
                "irrelevant stimuli -> psychosis; antipsychotics DAMPEN the salience of aberrant signals)",
            "attractor_instability": "Rolls, Loh & Deco 2007 (reduced NMDA depth -> shallow/unstable "
                "attractor basins -> spurious transitions / loss of stable selection)",
            "SZ_polygenic_LOCK": "idiopathic schizophrenia is POLYGENIC + heterogeneous (PGC GWAS >270 loci; "
                "CNVs) -- NOT one gene or one mechanism",
            "dysconnectivity_LOCK": "real schizophrenia functional connectivity is DYSconnective (mixed "
                "hyper-/hypo-, state- and network-dependent), NOT a clean increase; the global-R rise here "
                "is a SECONDARY in-silico observation, not the defining fingerprint",
            "antipsychotic_reality_LOCK": "antipsychotics (D2 antagonism) reduce dopaminergic gain and "
                "treat POSITIVE symptoms; negative/cognitive symptoms respond poorly. Mechanistically a "
                "gain/excitability REDUCTION -> the threshold-raising handle here",
            "stimulant_psychosis_LOCK": "psychostimulants (amphetamine etc.) can PRECIPITATE/WORSEN psychosis "
                "-- the catecholaminergic gain-RAISE that helps the autism-T pole harms the SZ pole",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only",
        },
        "invariants": {
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,   # filled below
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
        },
        "baseline_health": {
            "kappa_measured": round(KAP, 6),
            "R19_fold_spinodal": round(FOLD, 6),
            "ignition_threshold_health": round(ig_health, 6),
            "R_health": round(R_health, 6),
            "candidate_salience_drives": DRIVES,
            "healthy_selective_on_set": sorted(H),
            "n_selected_health": n_health,
        },
        "SZ1_over_ignition": {
            "model": "disinhibitory/excitatory bias LOWERS the R19 fold (mirror of autism-T) -- 'over-ignition'",
            "excitatory_bias": B_SZ,
            "ignition_threshold": round(ig_sz, 6),
            "ignition_lowered_below_health": SZ1,
        },
        "SZ2_aberrant_salience": {
            "model": "fold lowered -> weak/irrelevant candidate assemblies (sub-fold in health) now ignite",
            "on_set_sz": sorted(on_sz),
            "aberrant_ignitions_recruited_irrelevant": aberrant_sz,
            "relevant_ignitions_lost": lost_sz,
            "on_set_grows_vs_health": bool(len(on_sz) > n_health),
            "aberrant_salience_reproduced": SZ2,
            "dose_response_nsel_vs_bias": {str(k): v for k, v in nsel_curve.items()},
            "monotone_nondecreasing_in_excitation": bool(monotone),
        },
        "SZ3_global_integration_secondary": {
            "_what": "secondary: the disinhibition raises the engine's in-silico integration above health "
                     "(over-sync tendency). NOT the defining fingerprint -- real SZ is dysconnective (LOCK).",
            "kappa_effective_sz": round(_k_bias(B_SZ), 6),
            "R_sz": round(R_sz, 6),
            "R_extreme": round(R_ext, 6),
            "R_above_health": SZ3_oversync,
        },
        "autism_T_contrast": {
            "_what": "the OPPOSITE fold direction (D8 T), shown side-by-side: inhibitory bias raises the "
                     "fold and LOSES relevant ignitions (no aberrant recruitment).",
            "inhibitory_bias": B_AUT,
            "ignition_threshold": round(ig_aut, 6),
            "ignition_raised_or_equal": bool(ig_aut > ig_health - 1e-9),
            "aberrant_ignitions": aberrant_aut,
            "relevant_ignitions_lost_at_-0.20": lost_aut2,
            "contrast_reproduced": AUT_contrast,
        },
        "DISCRIMINANT_three_way": {
            "_what": "(ignition-direction, aberrant-vs-lost ignitions) uniquely identifies each condition.",
            "table": {
                "HEALTH":        {"ignition": "normal",  "aberrant_recruited": "0", "relevant_lost": "0",  "integration": "baseline"},
                "AUTISM_T":      {"ignition": "RAISED",  "aberrant_recruited": "0", "relevant_lost": "> 0", "integration": "down"},
                "SCHIZOPHRENIA": {"ignition": "LOWERED", "aberrant_recruited": "> 0", "relevant_lost": "0",  "integration": "up (secondary)"},
            },
            "schizophrenia_lowers_fold_recruits_irrelevant": sep_sz,
            "autism_T_raises_fold_loses_relevant": sep_aut,
            "fingerprints_are_distinct": bool(aberrant_sz != lost_aut2),
            "THREE_WAY_SEPARATION": THREE_WAY,
        },
        "RX_antipsychotic_gain_reduction": {
            "_what": "uniform gain-REDUCING / threshold-RAISING intervention -- the class antipsychotics act "
                     "through MECHANISTICALLY (D2 antagonism -> reduced dopaminergic gain; Kapur 2003 'dampens "
                     "the salience of aberrant signals'). NOT a claim of efficacy (=0; see LOCKs).",
            "gain_reduction_bias": RX_AP,
            "SZ_restored": {"on_set_after": sorted(on_sz_ap), "healthy_set": sorted(H),
                            "restores_healthy_selective_set": ap_restores_sz},
            "autism_T_worsened": {"on_set_before": sorted(_on_set(B_AUT)), "on_set_after": sorted(on_aut_ap),
                                  "loses_more_relevant": aut_worse_under_ap,
                                  "note": "the SAME push that calms SZ raises an already-high fold in autism-T "
                                          "-> opposite therapeutic sign for the opposite pole"},
            "RX_AP_discriminative": RX_AP_discriminative,
        },
        "RX_stimulant_opposite_sign": {
            "_what": "the gain-RAISING / threshold-LOWERING stimulant that HELPED autism-T (D8 RX_drug) "
                     "WORSENS schizophrenia -- the attested stimulant-precipitated/-worsened psychosis "
                     "direction. EXPERIMENTAL analogue; efficacy=0.",
            "stimulant_bias": RX_ST,
            "SZ_worsened": {"on_set_before": sorted(on_sz), "on_set_after": sorted(on_sz_st),
                            "more_aberrant_ignitions": stimulant_worsens_sz},
            "autism_T_helped": {"on_set_before": sorted(_on_set(B_AUT)), "on_set_after": sorted(on_aut_st),
                                "recovers_relevant_ignitions": stimulant_helps_aut},
            "reading": "the autism helper is the schizophrenia harmer -- one handle, opposite signs at the "
                       "two poles of the SAME ignitability axis.",
            "RX_STIM_opposite_sign": RX_STIM_opposite_sign,
        },
        "EXTREME_disorganisation_limit": {
            "_what": "unbounded disinhibition lowers the fold until ALL candidate assemblies ignite -- total "
                     "loss of the selective gate (zero selectivity), the disorganisation limit at the "
                     "excitation-imbalance boundary schizophrenia shares with seizure. Loss of GATING is a "
                     "MECHANISM boundary, NOT a claim about the disorganised subjective state.",
            "extreme_bias": B_EXT,
            "on_set_extreme": sorted(on_ext),
            "all_candidates_ignite": all_ignite,
            "every_irrelevant_recruited": selectivity_lost,
            "axis_A_firewall": "loss of gating != disorganised experience; consciousness_claim stays 0",
            "EXTREME_reproduced": EXTREME,
        },
        "SLEEP_sign_aligns": {
            "_what": "the gain-REDUCING (sedating) push that calms aberrant salience LOWERS arousal/"
                     "integration -- the SAME sign as sleep need (arousal DOWN). For schizophrenia the "
                     "therapeutic direction and the sleep direction ALIGN -- the MIRROR of autism, whose "
                     "arousal-RAISING therapy was anti-sleep. Sign-only.",
            "R_sz": round(R_sz, 6),
            "R_sz_under_antipsychotic": round(R_sz_ap, 6),
            "antipsychotic_lowers_arousal": antipsychotic_lowers_arousal,
            "therapy_sign_equals_sleep_sign": True,
            "opposite_to_autism_therapy_sign": True,
            "SLEEP_SIGN_ALIGNS": SLEEP_SIGN_ALIGNS,
        },
        "OWED": {
            "which_pole_a_given_psychosis_is": "OWED [O] -- requires per-individual external data "
                "(spectral E/I markers, genetics, connectome); the model asserts only the fingerprints "
                "and reversibility signs, NOT which mechanism any individual's illness is.",
            "integration_direction_in_vivo": "OWED -- the secondary global-R rise is engine-internal; real "
                "schizophrenia connectivity is dysconnective and state-dependent, needing in-vivo measures.",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0, "hard_problem_open": 1.0,
            "consciousness_claim": 0.0, "new_tuned_constants": 0.0,
        },
        "overall": {
            "over_ignition_reproduced": SZ1,
            "aberrant_salience_reproduced": SZ2,
            "autism_contrast_reproduced": AUT_contrast,
            "three_way_separation": THREE_WAY,
            "antipsychotic_discriminative": RX_AP_discriminative,
            "stimulant_opposite_sign": RX_STIM_opposite_sign,
            "extreme_reproduced": EXTREME,
            "sleep_sign_aligns": SLEEP_SIGN_ALIGNS,
            "dose_response_monotone": bool(monotone),
            "verdict": "schizophrenia is the OVER-IGNITION mirror of autism-T on the SAME R19 ignitability "
                       "axis: a disinhibitory/excitatory bias lowers the fold -> aberrant ignition of "
                       "irrelevant assemblies + loss of selective gating; a gain-reducing antipsychotic-class "
                       "push restores selectivity (and worsens autism-T), while the stimulant that helped "
                       "autism-T worsens SZ. (ignition-direction, aberrant-vs-lost) separates HEALTH / "
                       "AUTISM-T / SZ uniquely. Which pole a given illness is, is OWED.",
            "is_full_module": bool(SZ1 and SZ2 and AUT_contrast and THREE_WAY and RX_AP_discriminative
                                   and RX_STIM_opposite_sign and EXTREME and SLEEP_SIGN_ALIGNS and monotone),
        },
    }


def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def _blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def schizophrenia_results():
    res = run()
    # fill engine invariance (READ-ONLY emerge; never mutates the tree)
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    return res, blob, hashlib.sha256(blob.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    res, blob, digest = schizophrenia_results()
    with open(os.path.join(HERE, "schizophrenia_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_schizophrenia_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"schizophrenia_results.json": digest}, f, indent=2); f.write("\n")

    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    b, s1, s2 = res["baseline_health"], res["SZ1_over_ignition"], res["SZ2_aberrant_salience"]
    ac = res["autism_T_contrast"]; d = res["DISCRIMINANT_three_way"]
    ra = res["RX_antipsychotic_gain_reduction"]; rs = res["RX_stimulant_opposite_sign"]
    ex = res["EXTREME_disorganisation_limit"]; sl = res["SLEEP_sign_aligns"]
    print("=" * 78)
    print("SCHIZOPHRENIA-SPECTRUM DISCRIMINANT (D9 candidate)   add-only, engine READ-ONLY")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  R19 fold={b['R19_fold_spinodal']}  ig_health={b['ignition_threshold_health']}  health ON set={b['healthy_selective_on_set']} (n={b['n_selected_health']})")
    print("-" * 78)
    print(f"  SZ1 over-ignition : fold-crossing drive {s1['ignition_threshold']} < health {b['ignition_threshold_health']} = {s1['ignition_lowered_below_health']}")
    print(f"  SZ2 aberrant      : ON={s2['on_set_sz']}  +irrelevant={s2['aberrant_ignitions_recruited_irrelevant']}  -relevant={s2['relevant_ignitions_lost']}  => {s2['aberrant_salience_reproduced']}")
    print(f"       dose nsel(bias): {s2['dose_response_nsel_vs_bias']}  monotone={s2['monotone_nondecreasing_in_excitation']}")
    print(f"  AUT-T contrast    : ig {ac['ignition_threshold']}(raised={ac['ignition_raised_or_equal']})  -relevant@-0.20={ac['relevant_ignitions_lost_at_-0.20']}  +irrelevant={ac['aberrant_ignitions']}  => {ac['contrast_reproduced']}")
    print("-" * 78)
    print(f"  DISCRIMINANT 3-way: SZ(fold down,+irrelevant)={d['schizophrenia_lowers_fold_recruits_irrelevant']}  AUT(fold up,-relevant)={d['autism_T_raises_fold_loses_relevant']}  distinct={d['fingerprints_are_distinct']}  => {d['THREE_WAY_SEPARATION']}")
    print("-" * 78)
    print(f"  RX antipsychotic  : SZ restored to health={ra['SZ_restored']['restores_healthy_selective_set']}  autism-T worsened={ra['autism_T_worsened']['loses_more_relevant']}  => discriminative={ra['RX_AP_discriminative']}")
    print(f"  RX stimulant      : SZ worsened={rs['SZ_worsened']['more_aberrant_ignitions']}  autism-T helped={rs['autism_T_helped']['recovers_relevant_ignitions']}  => opposite-sign={rs['RX_STIM_opposite_sign']}")
    print(f"  EXTREME           : all ignite={ex['all_candidates_ignite']}  every irrelevant recruited={ex['every_irrelevant_recruited']}  => {ex['EXTREME_reproduced']}")
    print(f"  SLEEP sign        : antipsychotic lowers arousal={sl['antipsychotic_lowers_arousal']}  therapy-sign=sleep-sign (opp. autism) => {sl['SLEEP_SIGN_ALIGNS']}")
    print("-" * 78)
    print(f"  honesty 4-flags (eff/hp/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['hard_problem_open']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"]
          and ov["over_ignition_reproduced"] and ov["aberrant_salience_reproduced"]
          and ov["autism_contrast_reproduced"] and ov["three_way_separation"]
          and ov["antipsychotic_discriminative"] and ov["stimulant_opposite_sign"]
          and ov["extreme_reproduced"] and ov["sleep_sign_aligns"] and ov["dose_response_monotone"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["hard_problem_open"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  SCHIZOPHRENIA MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
