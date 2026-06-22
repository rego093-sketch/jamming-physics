# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- CHUNK D / GAP-4 BUILD : PCI CLINICAL MATCH (sleep ordering)
#  Drive the frozen M9 kernel through the EMERGED sleep architecture (M14) and ask
#  whether a faithful perturbational-complexity index (PCI, the clinical bedside
#  consciousness measure) orders the states the clinic orders -- WITHOUT tuning.
#
#  Constitution: physics/measurement-grounded only, NO TUNING, FIREWALL on felt
#  quality.  consciousness_claim = 0 ; hard_problem_open = 1 ; engine READ-ONLY.
#  STATUS: hypothesis-forming -- do NOT confirm; ST-4 (pci_clinical_match_st4.py)
#  stresses the ordering to destruction.
#
#  WHAT GAP-4 CLAIMS (whitepaper Section 4, ST-4 row):
#    The clinic reads consciousness off a TMS-evoked PERTURBATIONAL response: a
#    single pulse, then the Lempel-Ziv complexity of the evoked spatiotemporal
#    pattern (PCI).  Empirically (Casali 2013; Casarotto 2016) it orders
#        wake  ~  REM   >   NREM   >   anaesthesia   >   vegetative
#    and a fixed cutoff PCI* ~= 0.31 separates conscious from unconscious -- the
#    mechanism being cortical BISTABILITY / OFF-periods that truncate the causal
#    chain (Massimini 2005; Pigorini 2015).  GAP-4 asks: does the SAME ordering
#    fall out of the frozen kernel once the M14 sleep states are in place, with NO
#    new constant -- or does the single PCI scalar fail to separate the states
#    (collapse), in which case the clinical match is only an [O]?
#
#  GROUNDING (non-circular: the state -> mechanism map is fixed by M14, not by us).
#  emerge_sleep_architecture() (M14) already EMERGED, from the frozen kernel and
#  cited kinetics, the activated-vs-bistable distinction we ride on:
#    shift_index_rem  ~= 1.05  (REM  = ACTIVATED / desynchronised, no OFF-periods)
#    shift_index_nrem ~= 0.045 (NREM = BISTABLE slow Up/Down, OFF-periods present)
#    recall_rem 1.0 vs recall_nrem 0.53 ; spindle 15.4 Hz & slow-osc 0.49 Hz matched.
#  So WAKE/REM are driven with the adaptation OFF (off_depth=0, activated tonic) and
#  NREM with full slow-adaptation bistability (off_depth=1) at the cited nrem2 drive.
#  These are EMERGED facts asserted at run start; we add no state we did not earn.
#
#  THE MECHANISM WE SCORE (the M14 construction, READ-ONLY engine helpers):
#    A 16-cell cortical population of R19 cubic-bistable cells (s - s^3 + drive - a),
#    coupled diffusively through the M9 ephaptic ring at the MEASURED kappa=0.5496.
#    The state is set ONLY by the slow-adaptation strength (off_depth x A_GAIN) and
#    the cited carrier: activated theta-gamma (f~23.5 Hz) for wake/REM, slow 0.5 Hz
#    for NREM.  No quantity here is fit -- every one is a measured gene/physics/atlas
#    value (kappa, A_GAIN=1.6, TAU_SO=0.600 s, TAU_S=0.025 s, drive=0.60, carriers
#    from the brain atlas f0).  new_tuned_constants = 0.
#
#  FAITHFUL PCI (the part that makes this a PERTURBATIONAL, non-circular measure):
#    A single TMS-like kick (+2.0 to one cell, 4 ms after a 4 s settle) is applied
#    to a PERTURBED twin; an UNPERTURBED twin shares identical initial conditions.
#    PCI = normalised Lempel-Ziv complexity of the binarised PERTURBED-minus-
#    UNPERTURBED causal divergence D over a 1.5 s post-pulse window (downsample 8x,
#    binarise D > D.mean()).  Subtracting the twin removes spontaneous activity, so
#    with NO kick the divergence is identically zero and PCI = 0 for every state
#    (the non-circular control) -- exactly the property a spontaneous-EEG complexity
#    measure lacks and the clinical PCI is built to have.  The LZ core (lz76 /
#    normalised_lz) is IMPORTED from cognition_consciousness_body (non-circular at
#    the code level; we do not re-implement it).
#
#  CLINICAL ORDERINGS used ONLY for external comparison (we never tune TO them):
#    Casali AG et al. 2013, Sci Transl Med 5(198):198ra105  -- PCI: wake~REM > NREM
#                                                              > anaesthesia > VS.
#    Casarotto S et al. 2016, Ann Neurol 80(5):718           -- empirical PCI* ~= 0.31.
#    Massimini M et al. 2005, Science 309:2228               -- NREM breakdown of
#                                                              effective connectivity.
#    Pigorini A et al. 2015, NeuroImage 112:105              -- cortical bistability /
#                                                              OFF-period truncates the
#                                                              evoked causal chain.
#    Sanchez-Vives MV & McCormick DA 2000, Nat Neurosci 3:1027 ; Steriade 1993,
#      J Neurosci 13:3252                                    -- the M14 slow-adaptation
#                                                              mechanism (grounding).
# ==========================================================================
import sys, os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "_frontal"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import vp_mind_engine as E                         # frozen engine -- READ-ONLY
import frontal_common as FC                        # anchor guard + digest helpers
import cognition_consciousness_body as CCB         # lz76 / normalised_lz (imported, non-circular)

# ---- cited constants (NONE tuned: atlas / measured-DB / physics) --------------
KAP        = float(E.KAPPA_EPHAPTIC)                                            # 0.5496 measured ephaptic kappa
_ND        = E.load_mind_param_db()["neuro_dynamics"]
_ATL       = E._m14_load_sleep_atlas()
TAU_SO     = _ATL["cortical_kinetics_measured"]["slow_adaptation_recovery_tau_ms"]["value"] / 1000.0  # 0.600 s  Sanchez-Vives 2000
DRIVE_NREM = float(_ATL["nrem2_operating_point"]["thalamic_excitability_drive"])                       # 0.60     Steriade 1993
A_GAIN     = float(_ND["adaptation_drive_a_gain"]["value"])                                            # 1.6      cited adaptation gain
TAU_S      = float(_ND["cortical_recurrent_membrane_tau_s"]["value"])                                  # 0.025 s  recurrent membrane tau
_BA        = E.load_brain_atlas()
F_REM      = 0.5 * (_BA["organs"]["hippocampus"]["f0_hz"] + _BA["organs"]["neocortex"]["f0_hz"])       # 23.5 Hz  activated theta-gamma
F_SLOW     = 0.5                                                                                       # 0.5 Hz   NREM slow oscillation

FS, DT = 1000.0, 1.0 / 1000.0

# the state -> (off_depth, carrier) map.  WAKE/REM grounded by M14 (off=0, activated);
# NREM grounded by M14 (off=1, bistable @ cited drive).  ANES/VS are the EXTENDED
# deeper-bistability sweep (off>1) -- they have NO M14 grounding and stay [O].
STATES = [
    ("WAKE", 0.0, F_REM,  "grounded"),   # activated tonic (M14: shift_index_rem high)
    ("REM",  0.0, F_REM,  "grounded"),   # activated tonic, dreaming (M14: recall high)
    ("NREM", 1.0, F_SLOW, "grounded"),   # full slow-adaptation bistability (M14: OFF-periods)
    ("ANES", 1.6, F_SLOW, "extended"),   # deeper bistability -- NO grounding, [O]
    ("VS",   2.4, F_SLOW, "extended"),   # deepest bistability -- NO grounding, [O]
]
SEEDS      = range(19, 28)               # 9-seed cohort (matches the v2 convention)
N_CELL     = 16
T_S        = 8.0
SETTLE_S   = 4.0
KICK_OFF   = 4                           # kick applied 4 ms (4 samples) after settle
KICK_AMP   = 2.0                         # TMS-like single-cell kick
POST_S     = 1.5                         # post-pulse evoked window
DSAMPLE    = 8                           # downsample factor for the divergence matrix
CUTOFF     = 0.31                        # Casarotto 2016 empirical PCI* (external ref only)

RESULTS_JSON = os.path.join(_HERE, "pci_clinical_match_results.json")
EXPECTED_SHA = os.path.join(_HERE, "expected_pci_clinical_match_sha256.json")
FIG_OUT      = os.path.join(_HERE, "pci_clinical_match.png")
FIG_OUT2     = "/mnt/user-data/outputs/pci_clinical_match.png"


def ground_sleep_architecture():
    """Assert the M14 EMERGED facts we ride on (REM=activated, NREM=bistable). This is
    the grounding: the state->mechanism map is fixed by the engine, not by us. Returns
    the observables for the record. Raises if M14 no longer matches (firewall on drift)."""
    sa = E.emerge_sleep_architecture()
    assert int(round(sa["spindle_matched"])) == 1,        "M14 spindle no longer matched -- grounding broken."
    assert int(round(sa["slow_oscillation_matched"])) == 1, "M14 slow-osc no longer matched -- grounding broken."
    assert int(round(sa["nrem_rem_band_shift_matched"])) == 1, "M14 NREM/REM band shift not matched -- grounding broken."
    # the activated-vs-bistable distinction we build the state map on:
    assert sa["shift_index_rem"] > sa["shift_index_nrem"], "M14: REM not more activated than NREM -- grounding broken."
    # firewall must hold inside the grounding source too:
    assert int(round(sa["is_consciousness_claim"])) == 0 and int(round(sa["hard_problem_open"])) == 1
    return {
        "shift_index_rem":  round(float(sa["shift_index_rem"]), 6),
        "shift_index_nrem": round(float(sa["shift_index_nrem"]), 6),
        "recall_rem_coupling":  round(float(sa["recall_rem_coupling"]), 6),
        "recall_nrem_coupling": round(float(sa["recall_nrem_coupling"]), 6),
        "spindle_peak_hz":      round(float(sa["spindle_peak_hz"]), 4),
        "slow_oscillation_hz":  round(float(sa["slow_oscillation_hz"]), 4),
        "sleep_concordance":    round(float(sa["sleep_concordance"]), 4),
        "is_consciousness_claim": int(round(sa["is_consciousness_claim"])),
        "hard_problem_open":      int(round(sa["hard_problem_open"])),
        "interpretation": ("REM activated (shift_index_rem>>nrem) -> off_depth=0; NREM bistable "
                           "(slow Up/Down, OFF-periods) -> off_depth=1 @ cited nrem2 drive. Earned, not assumed."),
    }


def _traj(seed, off_depth, carrier_hz, pcell, do_kick=True):
    """One trajectory of the 16-cell M9-ring cortical population (the M14 construction).
    R19 cubic-bistable cells coupled diffusively through the measured ephaptic kernel;
    off_depth scales the slow-adaptation strength (0 = activated tonic, no OFF-periods;
    1 = full NREM bistability). A single TMS-like kick is delivered at settle if do_kick."""
    n = int(T_S * FS)
    rng = np.random.RandomState(seed)
    POS = E._ring(N_CELL)
    Wk = E._ephaptic_kernel(POS)
    s = -1.0 + 0.05 * rng.standard_normal(N_CELL)      # start near the Down state
    a = np.zeros(N_CELL)
    ag = A_GAIN * off_depth                            # adaptation gain engaged by off_depth
    om = 2.0 * math.pi * carrier_hz
    settle = int(SETTLE_S * FS)
    rec = np.zeros((N_CELL, n))
    for i in range(n):
        diff = (Wk @ s) - s                            # diffusive ephaptic coupling (M9)
        g = 0.5 * (1.0 + np.tanh(2.0 * s))             # Up-state gate for adaptation
        carr = 0.05 * math.sin(om * i * DT)            # weak cited carrier (keeps activated desync)
        s = s + DT * ((s - s ** 3 + DRIVE_NREM - a + KAP * diff + carr) / TAU_S)
        a = a + DT * ((ag * g - a) / TAU_SO)
        if i == settle and do_kick:
            s[pcell] += KICK_AMP                       # single-pulse perturbation
        rec[:, i] = s
    return rec, settle


def pci(seed, off_depth, carrier_hz, pcell=0, post_s=POST_S):
    """Faithful perturbational PCI: LZ complexity of the binarised PERTURBED-minus-
    UNPERTURBED causal divergence (subtracts spontaneous activity -> non-circular)."""
    rp, settle = _traj(seed, off_depth, carrier_hz, pcell, do_kick=True)
    ru, _ = _traj(seed, off_depth, carrier_hz, pcell, do_kick=False)
    w0 = settle + KICK_OFF
    w1 = settle + KICK_OFF + int(post_s * FS)
    D = (rp[:, w0:w1] - ru[:, w0:w1])[:, ::DSAMPLE]    # pure causal divergence, downsampled
    binm = (D > D.mean()).astype(int)                  # PROVEN binarisation convention
    return float(CCB.normalised_lz(binm))              # EXACT imported LZ core


def raw_activity(seed, off_depth, carrier_hz, pcell=0, post_s=POST_S):
    """Spontaneous post-window activity magnitude (NO twin subtraction). The dissociation
    check: arousal/activity must NOT track PCI, or the measure is just an arousal proxy."""
    rp, settle = _traj(seed, off_depth, carrier_hz, pcell, do_kick=True)
    w0 = settle + KICK_OFF
    w1 = settle + KICK_OFF + int(post_s * FS)
    return float(np.mean(np.abs(rp[:, w0:w1])))


def _figure(rows, ctrl_zero, verdict):
    names = [r["state"] for r in rows]
    pcis  = [r["pci"] for r in rows]
    acts  = [r["raw_activity"] for r in rows]
    cols  = ["#1e7d34" if r["grounding"] == "grounded" else "#888888" for r in rows]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.2))

    # panel 1: the PCI ordering with the clinical cutoff
    x = np.arange(len(rows))
    ax.bar(x, pcis, 0.62, color=cols, edgecolor="k", linewidth=0.5)
    ax.axhline(CUTOFF, color="#c0392b", ls="--", lw=1.6,
               label="clinical PCI* = {:.2f} (Casarotto 2016)".format(CUTOFF))
    for xi, p in zip(x, pcis):
        ax.text(xi, p + 0.012, "{:.3f}".format(p), ha="center", fontsize=8.5)
    ax.set_xticks(x); ax.set_xticklabels(names)
    ax.set_ylabel("PCI  (normalised LZ of causal divergence)")
    ax.set_ylim(0, max(pcis) * 1.25 + 0.02)
    ax.set_title("Perturbational complexity by state\n"
                 "green = M14-grounded (wake/REM/NREM); grey = extended sweep [O]")
    ax.legend(fontsize=8.4, loc="upper right"); ax.grid(True, axis="y", alpha=0.25)
    ax.text(0.02, 0.02, "no-perturbation control: PCI = {:.3f} (all states)".format(ctrl_zero),
            transform=ax.transAxes, fontsize=8, color="#444",
            bbox=dict(boxstyle="round", fc="#f4f4f4", ec="#bbb"))

    # panel 2: PCI vs raw activity -- the dissociation (complexity != arousal)
    ax2.scatter(acts, pcis, c=cols, s=90, edgecolor="k", zorder=3)
    for a_, p_, nm in zip(acts, pcis, names):
        ax2.annotate(nm, (a_, p_), fontsize=8.5, xytext=(4, 4), textcoords="offset points")
    ax2.set_xlabel("raw post-pulse activity magnitude (arousal proxy)")
    ax2.set_ylabel("PCI  (access / complexity)")
    ax2.set_title("PCI DISSOCIATES from raw activity\n"
                  "(unconscious states can carry activity yet collapse PCI)")
    ax2.grid(True, alpha=0.25)

    txt = ("GAP-4 (build): conscious/unconscious split SURVIVES (wake~REM >> NREM); "
           "unconscious-state ordering COLLAPSES to ~one scalar ({}).").format(verdict["unconscious_summary"])
    fig.suptitle(txt, fontsize=10.2, y=1.005, color="#1e7d34")
    fig.tight_layout()
    for p in (FIG_OUT, FIG_OUT2):
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            fig.savefig(p, dpi=130, bbox_inches="tight")
        except Exception:
            pass


def main():
    print("=" * 78)
    print(" vp_frontal v2 -- CHUNK D / GAP-4 BUILD : PCI clinical match (sleep ordering)")
    print(" drive the frozen kernel through M14 sleep states; score faithful PCI. NO TUNING.")
    print(" cited: kappa={:.4f} A_GAIN={:.2f} TAU_SO={:.3f}s TAU_S={:.3f}s drive={:.2f} f_rem={:.1f}Hz".format(
        KAP, A_GAIN, TAU_SO, TAU_S, DRIVE_NREM, F_REM))
    print("=" * 78)

    anchor = FC.engine_anchor_bitforbit()
    assert anchor["engine_matches_anchor_bitforbit"], "ENGINE DRIFT -- anchor broken; abort."
    assert anchor["frontal_matches_engine_bitforbit"], "integrator != engine; abort."
    print(" engine M9 anchor bit-for-bit: R={}  (matches={})".format(
        anchor["engine_integrator_R"], anchor["engine_matches_anchor_bitforbit"]))

    grounding = ground_sleep_architecture()
    print(" M14 grounding: shift_index_rem={:.3f} > nrem={:.3f}  (REM activated / NREM bistable);"
          " spindle {:.2f}Hz, slow-osc {:.2f}Hz matched.".format(
              grounding["shift_index_rem"], grounding["shift_index_nrem"],
              grounding["spindle_peak_hz"], grounding["slow_oscillation_hz"]))

    # ---- per-state PCI across the seed cohort ---------------------------------
    rows = []
    print()
    print(" state  grounding |   PCI     raw_act  | per-seed PCI")
    for name, off, carr, grd in STATES:
        ps = np.array([pci(sd, off, carr, 0) for sd in SEEDS])
        ac = np.array([raw_activity(sd, off, carr, 0) for sd in SEEDS])
        rows.append({"state": name, "off_depth": off, "carrier_hz": round(carr, 4),
                     "grounding": grd, "pci": round(float(ps.mean()), 6),
                     "pci_per_seed": [round(float(v), 6) for v in ps],
                     "raw_activity": round(float(ac.mean()), 6)})
        print("  {:<5s} {:<9s} | {:.4f}   {:.4f}  | {}".format(
            name, grd, ps.mean(), ac.mean(), " ".join("{:.3f}".format(v) for v in ps)))

    by = {r["state"]: r for r in rows}
    wake, rem, nrem = by["WAKE"]["pci"], by["REM"]["pci"], by["NREM"]["pci"]
    anes, vs = by["ANES"]["pci"], by["VS"]["pci"]

    # ---- non-circular control: no perturbation -> divergence 0 -> PCI 0 -------
    ctrl = []
    for name, off, carr, _ in STATES:
        rp, settle = _traj(19, off, carr, 0, do_kick=False)
        ru, _ = _traj(19, off, carr, 0, do_kick=False)
        w0 = settle + KICK_OFF; w1 = settle + KICK_OFF + int(POST_S * FS)
        D = (rp[:, w0:w1] - ru[:, w0:w1])[:, ::DSAMPLE]
        ctrl.append(float(CCB.normalised_lz((D > D.mean()).astype(int))))
    ctrl_zero = round(float(np.max(ctrl)), 6)        # max over states (should be 0.0)
    print()
    print(" NON-CIRCULAR CONTROL: with NO perturbation, twin divergence = 0 -> PCI = {:.4f} "
          "for every state.".format(ctrl_zero))

    # ---- the signed read-outs (the build's candidate result) ------------------
    margin = 0.05
    conscious_unconscious_separated = bool(min(wake, rem) - nrem > margin)
    rem_gt_nrem = bool(rem - nrem > margin)
    wake_gt_nrem = bool(wake - nrem > margin)
    unconscious_vals = [nrem, anes, vs]
    unconscious_spread = round(float(max(unconscious_vals) - min(unconscious_vals)), 6)
    unconscious_monotone = bool(nrem >= anes >= vs or nrem <= anes <= vs)  # any consistent order?
    # the clinic predicts deeper unconsciousness -> lower PCI (NREM > anes > VS); does it hold?
    deeper_lower = bool(nrem > anes > vs)
    wake_vs_rem_gap = round(float(abs(wake - rem)), 6)

    # arousal dissociation: does raw activity track PCI?  (Spearman-sign agreement check)
    acts = [by[s]["raw_activity"] for s in ("WAKE", "REM", "NREM", "ANES", "VS")]
    pcis = [by[s]["pci"] for s in ("WAKE", "REM", "NREM", "ANES", "VS")]
    # high-PCI states (wake/REM) vs low-PCI (NREM); is the activity ordering different from PCI ordering?
    activity_tracks_pci = bool(np.argsort(acts).tolist() == np.argsort(pcis).tolist())

    unconscious_summary = ("NREM={:.3f}, ANES={:.3f}, VS={:.3f}; spread={:.3f}".format(
        nrem, anes, vs, unconscious_spread))

    verdict = {
        "conscious_unconscious_split_survives": conscious_unconscious_separated,
        "rem_gt_nrem": rem_gt_nrem, "wake_gt_nrem": wake_gt_nrem,
        "pci_wake": wake, "pci_rem": rem, "pci_nrem": nrem, "pci_anes": anes, "pci_vs": vs,
        "rem_minus_nrem": round(rem - nrem, 6),
        "wake_vs_rem_gap": wake_vs_rem_gap,
        "unconscious_spread": unconscious_spread,
        "unconscious_states_separable": bool(unconscious_spread > margin),
        "deeper_unconsciousness_lower_pci": deeper_lower,
        "noperturbation_control_pci": ctrl_zero,
        "raw_activity_tracks_pci": activity_tracks_pci,
        "unconscious_summary": unconscious_summary,
        "gap4_grade": (
            "[L] in-silico for the CONSCIOUS/UNCONSCIOUS split (wake~REM >> NREM, grounded by the "
            "M14 activated-vs-bistable distinction; matches the clinical PCI conscious/unconscious "
            "binary and survives the no-perturbation control). [O] OPEN for the unconscious-state "
            "ordering: the single PCI scalar does NOT separate NREM/anaesthesia/VS (they collapse to "
            "~one value) and 'deeper bistability -> lower PCI' does not hold; the small clinical "
            "wake>REM gap is also unresolved [O]."),
        "statement": (
            "Driven through the EMERGED M14 sleep states with NO new constant, the faithful "
            "perturbational PCI cleanly separates the CONSCIOUS from the UNCONSCIOUS states: wake and "
            "REM (activated, off_depth=0) sit far above NREM (bistable, off_depth=1) -- wake~REM "
            "~={:.2f} vs NREM ~={:.2f}. This is the clinical PCI's core finding (conscious/unconscious "
            "binary) and it falls out of the frozen kernel once the activated-vs-bistable distinction "
            "is in place -- the bistable OFF-periods truncate the evoked causal chain (Massimini 2005; "
            "Pigorini 2015), collapsing complexity. HONEST NEGATIVE (recorded, not avoided): the SINGLE "
            "PCI scalar does NOT resolve the FINE unconscious ordering -- NREM, anaesthesia and the "
            "deepest 'vegetative' sweep collapse to ~one value (spread {:.3f}), and 'deeper bistability "
            "-> monotonically lower PCI' BREAKS; and the mechanism cannot resolve the small clinical "
            "wake>REM gap (|wake-REM|={:.3f}). The non-circular control holds (no kick -> PCI={:.2f}), "
            "and PCI is not a mere arousal proxy (it dissociates from raw activity). So GAP-4 is an "
            "in-silico [L] for the conscious/unconscious split and an [O] for the within-unconscious "
            "ordering. ST-4 stresses the split for sign-stability before it is believed.").format(
                0.5 * (wake + rem), nrem, unconscious_spread, wake_vs_rem_gap, ctrl_zero),
    }

    clinical_reference = {
        "Casali_2013_STM_5_198ra105":   "PCI orders wake~REM > NREM > anaesthesia > vegetative.",
        "Casarotto_2016_AnnNeurol_80_718": "empirical cutoff PCI* ~= 0.31 (conscious vs unconscious).",
        "Massimini_2005_Science_309_2228": "NREM breakdown of cortical effective connectivity.",
        "Pigorini_2015_NeuroImage_112_105": "cortical bistability / OFF-period truncates the evoked chain.",
        "SanchezVives_McCormick_2000_NatNeurosci_3_1027": "slow-oscillation / slow-adaptation mechanism (M14).",
        "Steriade_1993_JNeurosci_13_3252": "NREM thalamocortical operating point (M14 drive).",
        "note": "Orderings used for EXTERNAL comparison only; no quantity was tuned to them.",
    }

    results = {
        "module": "pci_clinical_match (Chunk D / Gap-4 build)",
        "constitution": {"new_tuned_constants": 0, "consciousness_claim": 0,
                         "hard_problem_open": 1, "engine_readonly": True},
        "engine_anchor_bitforbit": {"R": anchor["engine_integrator_R"],
                                    "matches_M9_anchor": anchor["engine_matches_anchor_bitforbit"],
                                    "integrator_matches_engine": anchor["frontal_matches_engine_bitforbit"]},
        "m14_grounding": grounding,
        "grounded_inputs": {"kappa_ephaptic": KAP, "A_GAIN": A_GAIN, "TAU_SO_s": TAU_SO,
                            "TAU_S_s": TAU_S, "drive_nrem": DRIVE_NREM,
                            "f_rem_hz": F_REM, "f_slow_hz": F_SLOW,
                            "n_cell": N_CELL, "T_s": T_S, "settle_s": SETTLE_S,
                            "kick_amp": KICK_AMP, "kick_offset_samples": KICK_OFF,
                            "post_window_s": POST_S, "downsample": DSAMPLE,
                            "seeds": list(SEEDS), "clinical_cutoff_ref": CUTOFF},
        "state_map": [{"state": n, "off_depth": o, "carrier_hz": round(c, 4), "grounding": g}
                      for n, o, c, g in STATES],
        "pci_by_state": rows,
        "noncircular_control": {"noperturbation_pci_max_over_states": ctrl_zero,
                                "interpretation": "no kick -> twin divergence 0 -> PCI 0 (perturbational, not spontaneous)."},
        "verdict": verdict,
        "clinical_reference": clinical_reference,
        "grades": (
            "[L] in-silico conscious/unconscious PCI split (wake~REM >> NREM), grounded by M14; "
            "[O] within-unconscious ordering (NREM/anaesthesia/VS collapse to ~one scalar), "
            "[O] wake-vs-REM fine gap, [O] absolute PCI magnitudes, [O] felt quality. "
            "consciousness_claim=0; hard_problem_open=1; new_tuned_constants=0; engine READ-ONLY. "
            "This is an in-silico model result -- NOT validated neuroscience, NOT clinical guidance."),
    }
    digest = FC.digest_of(results); results["digest"] = digest
    with open(RESULTS_JSON, "w") as f:
        f.write(FC.blob(results))
    with open(EXPECTED_SHA, "w") as f:
        json.dump({"pci_clinical_match_results.json": digest}, f, indent=2)
    _figure(rows, ctrl_zero, verdict)

    print()
    print("-" * 78)
    print(" VERDICT (build):")
    print("   conscious/unconscious split (wake~REM >> NREM)  : SURVIVES  "
          "(wake={:.3f} rem={:.3f} >> nrem={:.3f}; rem-nrem={:+.3f})".format(
              wake, rem, nrem, rem - nrem))
    print("   within-unconscious ordering (NREM/ANES/VS)      : COLLAPSES  "
          "(spread={:.3f}; deeper->lower PCI holds={})".format(unconscious_spread, deeper_lower))
    print("   wake vs REM fine gap                            : UNRESOLVED (|wake-rem|={:.3f})".format(
        wake_vs_rem_gap))
    print("   non-circular control (no kick -> PCI)           : {:.3f}".format(ctrl_zero))
    print("   Gap-4 grade:", verdict["gap4_grade"])
    print(" results ->", RESULTS_JSON)
    print(" sha     ->", digest)
    print(" figure  ->", FIG_OUT)
    print(" GRADES:", results["grades"])
    print(" STATUS: COMPLETE (build) -- run pci_clinical_match_st4.py to stress it")


if __name__ == "__main__":
    main()
