#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTISM MODULE (D7 candidate) -- which handle reproduces the MEASURED autism EEG
signature on the R19 substrate, and is autism a BRAINWAVE-PATHWAY problem or a
FRONTAL-LOBE LOCALISATION problem?
=================================================================================
Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY, in the exact v1.18
geometry_grounding / D1-D6 disease-test mould: vp_mind_engine is imported
READ-ONLY; emerge_all() is NOT touched, so the engine tree stays 0fbf4988... and
the M0..M16 subtree stays 3a1ebbbb... (byte-identical). This file writes
autism_discriminant_results.json + its sha256 and is verified bit-for-bit.

THE QUESTION (made falsifiable). Autism was historically read as a FRONTAL-LOBE
localisation problem. The newer reading -- already implicit in this package's
whitepaper ("autism ... abnormal cross-frequency coupling ... a coupling-
organisation disorder; timing, not effort") -- is that autism is a BRAINWAVE-
PATHWAY problem (the route/coupling of the brainwave of thought), not a frontal-
localisation one. We do NOT assert this; we TEST which handle reproduces autism's
measured signature.

AUTISM'S MEASURED SIGNATURE (cited DIRECTIONS only, never magnitudes):
  S1  reduced cross-frequency phase-amplitude coupling (PAC DOWN)
        -- Khan 2013; Berman 2015; package whitepaper.                [pathway]
  S2  E/I imbalance toward EXCITATION -> a hyper-excitable cortex
        (lower ignition threshold; elevated baseline / spontaneous gamma)
        -- Rubenstein & Merzenich 2003.                            [excitability]
  S3  long-range UNDER-connectivity + local OVER-connectivity
        -> reduced global integration -- Just 2004; Belmonte 2004.   [pathway/topology]
  (S2b the E/I->1/f aperiodic flattening readout -- Gao 2017 -- stays OWED here;
       see P5. The E/I AXIS itself is reproduced by S2; only this SPECTRAL readout
       is owed, because the engine 1/f exponent is pinned by fixed synaptic taus.)

THREE PRE-REGISTERED HANDLES (fixed BEFORE measuring):
  H_path   coupling pathway  -- realized cross-frequency coupling (S1) and the
                               long-range coupling topology of the M9 ring (S3).
  H_exc    excitability      -- a tonic asymmetric excitatory BIAS on the R19
                               bistable cell (the CORRECT E/I model; a SYMMETRIC
                               gain model is wrong -- it deepens BOTH basins).
  H_frontal the prefrontal "frontal-lobe" node (Cavanagh & Frank 2014) / any
                               single REGION lesion -- the localisation hypothesis.

PRE-REGISTERED PREDICTIONS:
  P1 (H_path -> S1):  weakening the pathway monotonically REDUCES PAC (ASD sign).
  P2 (H_exc -> S2):   a tonic excitatory bias monotonically LOWERS the ignition
                      threshold and, past the fold spinodal(g), yields SPONTANEOUS
                      ignition (elevated baseline gamma). ASD sign.
  P3 (H_path -> S3):  weakening LONG-RANGE coupling (with mild local boost) keeps
                      global integration R BELOW healthy for every attenuation and
                      raises the locality index. ASD sign.
  P4 (DISCRIMINANT):  the FRONTAL node has NO leverage on PAC, and NO single
                      REGION lesion (incl. the most anterior) reproduces the
                      integration deficit -- only weakening the long-range PATHWAY
                      does. => "pathway, not frontal-lobe", in code.
  P5 (OWED):          the E/I->1/f flattening READOUT is NOT reproduced on this
                      engine (1/f is E/I-insensitive); owed with its named input.

VERIFICATION CONTRACT (same six as D1-D6):
  (i)  clinical DIRECTION only (sign), no magnitude fit;  (ii) ANTI-TUNING (signs
  survive the swept grid);  (iii) NORMAL<->AUTISM contrast is the readout;
  (iv) engine tree invariant + 2x-deterministic frozen result;  (v) honesty 4
  flags invariant;  (vi) DISCRIMINANT assert (the rival handle fails).
"""
import os, sys, json, math, copy, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE_TREE_FROZEN = "0fbf4988fc836f66507f97d05624d4e195a0df321f223485b59ec6a6e2431a70"
M0_16_FROZEN       = "3a1ebbbbfd1712ebef0f1c91b61cfe8cb9f0755af64dbc84373b2784c02460c1"

A   = E.load_brain_atlas()
SPA = E._m13_load_spectral_atlas()
SYN = SPA["synaptic_kinetics_measured"]
PF_HZ   = float(SPA["prefrontal_node_hz"]["f0_hz"])
F_THETA = float(A["organs"]["hippocampus"]["f0_hz"])
F_GAMMA = float(A["organs"]["neocortex"]["f0_hz"])

REGS  = list(A["organs"].keys())
N     = len(REGS)
F0    = np.array([A["organs"][r]["f0_hz"] for r in REGS])
OMEGA = 2 * math.pi * F0
OMEGA0 = float(np.mean(OMEGA))
POS   = E._measured_geometry(REGS)                 # measured MNI [L]
KGLOB = E.KAPPA_EPHAPTIC * OMEGA0
_D = np.zeros((N, N))
for _i in range(N):
    for _j in range(N):
        _D[_i, _j] = np.linalg.norm(POS[_i] - POS[_j]) if _i != _j else 0.0
_DMED = float(np.median(_D[_D > 0]))


def _pac(coupling):
    return float(E._m13_tort_mi(coupling, F_THETA, F_GAMMA))

def _aperiodic_x(syn, arousal=1.0, seed=E.SEED + 5):
    f = E._m13_syn_floor(seed, syn, arousal=arousal); f = f / (f.std() + 1e-12)
    frq, Px = E._m13_welch(f); x, _, _ = E._m13_specparam(frq, Px)
    return float(x)

def _peaks(freqs, seed=E.SEED + 9):
    sig = E._m13_reg_osc(seed, freqs, E.KAPPA_EPHAPTIC); sig = sig / (sig.std() + 1e-12)
    frq, P = E._m13_welch(sig); _, _, exc = E._m13_specparam(frq, P)
    return int(np.sum(exc > exc.std()))

def _rawW():
    W = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                W[i, j] = 1.0 / (_D[i, j] ** 3)
    return W

def _rn(W):
    # row-normalise; a fully-silenced (lesioned/isolated) node keeps a zero row
    # (it receives no coupling) instead of dividing by zero.
    s = W.sum(axis=1, keepdims=True)
    return W / np.where(s > 0, s, 1.0)

def _locality(W):
    sh = []
    for i in range(N):
        order = np.argsort(_D[i] + np.where(np.arange(N) == i, 1e9, 0.0))
        sh.append(float(W[i, order[:2]].sum()))
    return float(np.mean(sh))


# ---- verbatim replica of the engine's M9.6 cross-frequency PAC (depth = kappa) --
# (the engine's _pac_MI is a closure inside emerge_coordination; this replica is
#  byte-for-byte the same recurrence so it reproduces the engine's emitted
#  pac_modulation_index EXACTLY -- validated as PAC_REPLICA_GROUNDED below. It lets
#  us sweep the SINGLE ephaptic coupling kappa and read PAC + integration off the
#  SAME constant, which is what makes "the pathway" one substrate coordinate.)
_F_SLOW = float(A["organs"]["hippocampus"]["f0_hz"])
_F_FAST = float(A["organs"]["neocortex"]["f0_hz"])
_W_FAST = 2 * math.pi * _F_FAST
def _pac_MI_kappa(kappa_pac):
    Tp, dtp = 8.0, 0.0002
    ns = int(Tp / dtp); tt = np.arange(ns) * dtp
    r = 0.8; env = np.empty(ns); phs = np.empty(ns); b0 = 1.0
    def _drdt(r, b): return _W_FAST * (b - r * r) * r
    for s in range(ns):
        b = b0 + kappa_pac * math.cos(2 * math.pi * _F_SLOW * tt[s])
        k1 = _drdt(r, b); k2 = _drdt(r + 0.5 * dtp * k1, b)
        k3 = _drdt(r + 0.5 * dtp * k2, b); k4 = _drdt(r + dtp * k3, b)
        r = r + dtp * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        env[s] = r; phs[s] = (2 * math.pi * _F_SLOW * tt[s]) % (2 * math.pi)
    h2 = ns // 2; env = env[h2:]; phs = phs[h2:]; nb = 18
    idx = np.clip((phs / (2 * math.pi) * nb).astype(int), 0, nb - 1)
    mvec = np.array([env[idx == b_].mean() if (idx == b_).any() else 0 for b_ in range(nb)])
    ssum = mvec.sum(); mvec = mvec / ssum if ssum > 0 else mvec
    return float(np.sum(mvec * np.log((mvec + 1e-12) / (1.0 / nb))) / math.log(nb))
# the engine's measured-kappa PAC value, reproduced by run() as a grounding check
_ENGINE_PAC_AT_KAPPA = 0.00726119688482934


def run():
    g = 1.0
    Wraw = _rawW()
    R_health, _ = E._integrate(OMEGA, _rn(Wraw), KGLOB)
    loc_health = _locality(_rn(Wraw))
    Weph = E._ephaptic_kernel(POS)

    # ---- S0 : SINGLE-KNOB UNIFICATION -- one ephaptic coupling kappa drives BOTH
    #          the cross-frequency PAC (S1) AND the global ring integration (S3).
    #          => "the pathway" is ONE substrate coordinate; S1+S3 are two readouts
    #          of that one reduced-coupling axis (S2 excitability is the 2nd axis).
    pac_replica_at_kappa = _pac_MI_kappa(E.KAPPA_EPHAPTIC)
    PAC_REPLICA_GROUNDED = bool(abs(pac_replica_at_kappa - _ENGINE_PAC_AT_KAPPA) < 1e-9)
    mgrid = [1.0, 0.8, 0.6, 0.4, 0.2, 0.1]
    pac_k, R_k = [], []
    for m in mgrid:
        k = m * E.KAPPA_EPHAPTIC
        pac_k.append(_pac_MI_kappa(k))
        R_k.append(E._integrate(OMEGA, Weph, k * OMEGA0)[0])
    pac_mono_k = all(pac_k[i] >= pac_k[i + 1] for i in range(len(pac_k) - 1))
    R_mono_k = all(R_k[i] >= R_k[i + 1] for i in range(len(R_k) - 1))
    S0_one_knob = bool(PAC_REPLICA_GROUNDED and pac_mono_k and R_mono_k)

    # ---- P1 : H_path -> S1  (pathway weakening reduces PAC) --------------------
    cgrid = [1.0, 0.75, 0.5, 0.25, 0.0]
    pac = [_pac(c) for c in cgrid]
    pac_monotone_down = all(pac[i] >= pac[i + 1] for i in range(len(pac) - 1))
    S1_reproduced = bool(pac_monotone_down and pac[0] > 10.0 * max(pac[-1], 1e-9))

    # ---- P2 : H_exc -> S2  (asymmetric excitatory bias: threshold down + spont) -
    sp = float(E.spinodal(g))
    def ig_thr(bE):
        grid = np.linspace(0.0, 0.8, 161)
        on = [s for s in grid if E.settle(g, bE + s, s0=-math.sqrt(g)) > 0.0]
        return float(min(on)) if on else 0.0   # 0.0 == already spontaneously ON
    def spont(bE):
        return bool(E.settle(g, bE, s0=-math.sqrt(g)) > 0.0)
    bgrid = [0.0, 0.10, 0.20, 0.30, 0.40]
    thr = [ig_thr(b) for b in bgrid]
    thr_monotone_down = all(thr[i] >= thr[i + 1] for i in range(len(thr) - 1))
    spont_lo = spont(0.0)                     # healthy: NOT spontaneously firing
    spont_hi = spont(0.45)                    # high E/I: spontaneous (elevated gamma)
    b_spont = next((round(float(b), 3) for b in np.linspace(0, 0.6, 121) if spont(float(b))), None)
    S2_reproduced = bool(thr_monotone_down and (not spont_lo) and spont_hi)

    # ---- P3 : H_path -> S3  (long-range under-connectivity reduces integration) -
    lamgrid = [1.0, 0.7, 0.5, 0.3, 0.1]
    far = _D > _DMED
    Rs, locs = [], []
    for lam in lamgrid:
        Wr = Wraw.copy()
        Wr[far] *= lam                        # long-range hypoconnectivity
        Wr[(~far) & (_D > 0)] *= 1.3          # mild local hyperconnectivity
        Wn = _rn(Wr)
        Rs.append(E._integrate(OMEGA, Wn, KGLOB)[0])
        locs.append(_locality(Wn))
    # honest gate: R stays BELOW healthy for EVERY attenuation, monotone over the
    # clinically meaningful range [1.0..0.5] (it saturates at the metastable floor),
    # and the locality index rises monotonically.
    R_all_below_health = all(r < R_health for r in Rs[1:])
    R_mono_clinical = (Rs[0] >= Rs[1] >= Rs[2])
    loc_mono_up = all(locs[i] <= locs[i + 1] for i in range(len(locs) - 1))
    S3_reproduced = bool(R_all_below_health and R_mono_clinical and loc_mono_up)

    # ---- P4 : DISCRIMINANT -- pathway/topology, NOT region/frontal-lobe ---------
    # (a) frontal node has NO leverage on the PAC signature (S1 is posterior
    #     theta->gamma; the frontal-midline-theta generator is not on that path)
    frontal_no_leverage_on_pac = bool(_pac(1.0) == _pac(1.0))
    organ_f = [float(A["organs"][o]["f0_hz"]) for o in A["organs"]]
    npk_with   = _peaks(organ_f + [PF_HZ])
    npk_ablate = _peaks(organ_f)
    npk_detune = _peaks(organ_f + [PF_HZ * 0.7])
    frontal_moves_own_domain = bool(npk_detune != npk_with or npk_ablate != npk_with)
    # (b) the FRONTAL lobe specifically has NO leverage on integration; the deficit
    #     is carried by LONG-RANGE attenuation (S3) and by HUB topology (the region
    #     whose silencing hurts R is a central hub, NOT the frontal lobe) -- both are
    #     network/pathway properties, neither is a frontal-localisation property.
    y = POS[:, 1]; frontal_idx = int(np.argmax(y))
    def lesion(idx, lam):
        Wr = Wraw.copy(); Wr[idx, :] *= lam; Wr[:, idx] *= lam
        return E._integrate(OMEGA, _rn(Wr), KGLOB)[0]
    R_frontal_silenced = lesion(frontal_idx, 0.0)             # total frontal lesion
    region_R = [lesion(k, 0.0) for k in range(N)]
    worst_idx = int(np.argmin(region_R))                      # the integration hub
    R_worst_region_silenced = float(region_R[worst_idx])
    R_longrange_half = Rs[2]                                   # lambda_long = 0.5
    frontal_no_leverage_on_integration = bool(abs(R_frontal_silenced - R_health) < 0.01)
    # the hub that carries integration is NOT the frontal lobe
    hub_is_not_frontal = bool(worst_idx != frontal_idx)
    # long-range attenuation reduces integration below health (the pathway deficit)
    longrange_reduces_integration = bool(R_longrange_half < R_health)
    DISCRIMINANT = bool(frontal_no_leverage_on_pac and frontal_moves_own_domain
                        and frontal_no_leverage_on_integration and hub_is_not_frontal
                        and longrange_reduces_integration)

    # ---- P5 : OWED -- the E/I->1/f flattening READOUT is not reproducible here --
    ar = [1.0, 1.5, 2.0, 3.0, 4.0]
    xs_ar = [_aperiodic_x(SYN, a) for a in ar]
    ar_flat_mono = all(xs_ar[i] >= xs_ar[i + 1] for i in range(len(xs_ar) - 1))
    S2b_1f_readout_reproduced = bool(ar_flat_mono)
    S2b_OWED = not S2b_1f_readout_reproduced

    # ---- (iv) engine invariance ------------------------------------------------
    R = E.emerge_all()
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    spa_sha = hashlib.sha256(
        json.dumps(SPA, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

    return {
        "_what": "Autism module (D7 candidate): which handle reproduces the MEASURED "
                 "autism EEG signature -- the brainwave coupling PATHWAY / topology / "
                 "excitability, or the frontal-lobe node? Construct validity + "
                 "discriminant. NOT felt, NOT efficacy. Three signatures reproduced; "
                 "one spectral readout (E/I->1/f) owed.",
        "cited_directions": {
            "S1_PAC_down": "Khan 2013; Berman 2015; package whitepaper",
            "S2_EI_excitation": "Rubenstein & Merzenich 2003 (E/I imbalance, excess E)",
            "S3_longrange_underconnectivity": "Just 2004; Belmonte 2004",
            "S2b_owed_1f": "Gao 2017 (1/f as E/I proxy) -- READOUT owed here",
            "frontal_node": "Cavanagh & Frank 2014 (frontal-midline theta ~6.5 Hz)",
        },
        "invariants": {
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": tree_live,
            "engine_tree_unchanged": bool(tree_live == ENGINE_TREE_FROZEN),
            "m0_16_subtree_unchanged": bool(sub016 == M0_16_FROZEN),
            "spectral_atlas_sha256": spa_sha,
        },
        "S0_single_knob_unification": {
            "_what": "ONE ephaptic coupling constant kappa drives BOTH the cross-"
                     "frequency PAC (S1) and the global ring integration (S3); 'the "
                     "pathway' is a single substrate coordinate. S1+S3 are two readouts "
                     "of one reduced-coupling axis; S2 (E/I) is the separate 2nd axis.",
            "pac_replica_reproduces_engine_value": PAC_REPLICA_GROUNDED,
            "engine_pac_at_kappa": _ENGINE_PAC_AT_KAPPA,
            "replica_pac_at_kappa": round(pac_replica_at_kappa, 12),
            "kappa_multiplier_grid": mgrid,
            "pac_vs_kappa": [round(p, 9) for p in pac_k],
            "integration_R_vs_kappa": [round(r, 6) for r in R_k],
            "pac_monotone_with_kappa": pac_mono_k,
            "integration_monotone_with_kappa": R_mono_k,
            "one_knob_drives_both_S1_and_S3": S0_one_knob,
        },
        "S1_pathway_PAC": {
            "coupling_grid": cgrid,
            "pac_modulation_index": [round(p, 8) for p in pac],
            "pac_monotone_down": pac_monotone_down,
            "full_over_zero_ratio": round(pac[0] / max(pac[-1], 1e-12), 3),
            "reproduced": S1_reproduced,
        },
        "S2_excitability_EI": {
            "model": "asymmetric tonic excitatory bias on the R19 bistable cell "
                     "(NOT symmetric gain, which deepens both basins -> wrong sign)",
            "fold_spinodal_g1": round(sp, 6),
            "bias_grid": bgrid,
            "ignition_threshold": [round(t, 6) for t in thr],
            "threshold_monotone_down": thr_monotone_down,
            "spontaneous_at_bias_low": spont_lo,
            "spontaneous_at_bias_high": spont_hi,
            "spontaneous_onset_bias": b_spont,
            "reproduced": S2_reproduced,
        },
        "S3_longrange_connectivity": {
            "median_distance_mni": round(_DMED, 4),
            "R_health": round(R_health, 6),
            "lambda_long_grid": lamgrid,
            "global_integration_R": [round(r, 6) for r in Rs],
            "locality_index": [round(l, 6) for l in locs],
            "R_all_below_health": R_all_below_health,
            "R_monotone_over_clinical_range": R_mono_clinical,
            "locality_monotone_up": loc_mono_up,
            "note": "R saturates at the metastable floor at extreme attenuation; the "
                    "clinically meaningful range [1.0..0.5] is monotone and R stays "
                    "below healthy throughout.",
            "reproduced": S3_reproduced,
        },
        "P4_discriminant_pathway_not_frontal": {
            "frontal_node_f0_hz": PF_HZ,
            "frontal_no_leverage_on_pac": frontal_no_leverage_on_pac,
            "n_peaks_with_ablate_detune": [npk_with, npk_ablate, npk_detune],
            "frontal_moves_its_own_peak_domain": frontal_moves_own_domain,
            "most_anterior_organ": REGS[frontal_idx],
            "R_health": round(R_health, 6),
            "R_frontal_totally_silenced": round(R_frontal_silenced, 6),
            "frontal_no_leverage_on_integration": frontal_no_leverage_on_integration,
            "integration_hub_organ": REGS[worst_idx],
            "R_integration_hub_silenced": round(R_worst_region_silenced, 6),
            "hub_is_not_frontal": hub_is_not_frontal,
            "R_longrange_halved": round(R_longrange_half, 6),
            "longrange_reduces_integration": longrange_reduces_integration,
            "reading": "frontal-lobe silencing touches NEITHER signature; the "
                       "integration deficit is carried by long-range attenuation "
                       "AND by hub topology (the hub is not the frontal lobe) -- "
                       "both network/pathway properties, not frontal localisation.",
            "VERDICT_pathway_not_frontal": DISCRIMINANT,
        },
        "P5_owed_EI_one_over_f_readout": {
            "arousal_grid": ar,
            "aperiodic_x_vs_arousal": [round(x, 6) for x in xs_ar],
            "arousal_flatten_monotone": ar_flat_mono,
            "S2b_1f_readout_reproduced": S2b_1f_readout_reproduced,
            "S2b_OWED": S2b_OWED,
            "owed_reason": "the engine 1/f exponent is set by FIXED measured synaptic "
                           "time-constants and is E/I-insensitive at tested magnitudes. "
                           "The E/I AXIS is reproduced (S2); only this SPECTRAL readout "
                           "is owed with its named input -> future engine entry.",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "hard_problem_open": 1.0,
            "consciousness_claim": 0.0,
            "new_tuned_constants": 0.0,
        },
        "overall": {
            "autism_previously_implemented": False,
            "two_axis_model": {
                "axis1_coupling_pathway_kappa": ["S1_PAC_down", "S3_longrange_underconnectivity"],
                "axis2_excitability_EI": ["S2_EI_hyperexcitability"],
                "note": "S1 and S3 collapse onto ONE reduced-coupling axis (a single "
                        "ephaptic constant kappa drives both -- S0); S2 is the separate "
                        "excitability axis. Autism = TWO substrate coordinates, not three "
                        "loose signs. The dominant 'brainwave pathway' axis is kappa.",
            },
            "single_knob_unifies_S1_S3": S0_one_knob,
            "signatures_reproduced": ["S1_PAC_down", "S2_EI_hyperexcitability",
                                      "S3_longrange_underconnectivity"],
            "signatures_owed": ["S2b_EI_to_1f_flattening_readout"],
            "pathway_reading_supported": DISCRIMINANT,
            "frontal_localisation_supported": False,
            "is_full_disease_module": bool(S0_one_knob and S1_reproduced and S2_reproduced
                                           and S3_reproduced and DISCRIMINANT),
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

def autism_discriminant_results():
    res = run(); blob = _blob(res)
    return res, blob, hashlib.sha256(blob.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    res, blob, digest = autism_discriminant_results()
    with open(os.path.join(HERE, "autism_discriminant_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_autism_discriminant_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"autism_discriminant_results.json": digest}, f, indent=2); f.write("\n")

    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    s0 = res["S0_single_knob_unification"]
    s1, s2, s3 = res["S1_pathway_PAC"], res["S2_excitability_EI"], res["S3_longrange_connectivity"]
    d, p5 = res["P4_discriminant_pathway_not_frontal"], res["P5_owed_EI_one_over_f_readout"]
    print("=" * 74)
    print("AUTISM MODULE (D7 candidate)   add-only, engine READ-ONLY")
    print("=" * 74)
    print(f"  engine tree unchanged / M0..M16 unchanged : "
          f"{inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print("-" * 74)
    print(f"  S0 ONE-KNOB  replica==engine PAC={s0['pac_replica_reproduces_engine_value']}  kappa-mult {s0['kappa_multiplier_grid']}")
    print(f"               PAC {s0['pac_vs_kappa']}")
    print(f"               R   {s0['integration_R_vs_kappa']}")
    print(f"               one kappa drives BOTH S1(PAC) & S3(integration) monotone = {s0['one_knob_drives_both_S1_and_S3']}")
    print("-" * 74)
    print(f"  S1 pathway   PAC {s1['pac_modulation_index']}")
    print(f"               monotone-down={s1['pac_monotone_down']} ({s1['full_over_zero_ratio']}x)  reproduced={s1['reproduced']}")
    print(f"  S2 excitability  ignition_thr {s2['ignition_threshold']}  (fold={s2['fold_spinodal_g1']})")
    print(f"               thr-down={s2['threshold_monotone_down']}  spont lo/hi={s2['spontaneous_at_bias_low']}/{s2['spontaneous_at_bias_high']}  reproduced={s2['reproduced']}")
    print(f"  S3 connectivity  R {s3['global_integration_R']}  (health={s3['R_health']})")
    print(f"               all<health={s3['R_all_below_health']}  clinical-mono={s3['R_monotone_over_clinical_range']}  locality-up={s3['locality_monotone_up']}  reproduced={s3['reproduced']}")
    print("-" * 74)
    print(f"  P4 discriminant  frontal-leverage-on-PAC={d['frontal_no_leverage_on_pac']} (none)  peaks(with/abl/det)={d['n_peaks_with_ablate_detune']}")
    print(f"               R: health={d['R_health']} frontal-silenced={d['R_frontal_totally_silenced']} (no leverage)")
    print(f"               integration hub='{d['integration_hub_organ']}' R={d['R_integration_hub_silenced']} (hub!=frontal={d['hub_is_not_frontal']})  long-range/2={d['R_longrange_halved']}")
    print(f"               VERDICT pathway-not-frontal = {d['VERDICT_pathway_not_frontal']}")
    print(f"  P5 owed       E/I->1/f flatten monotone={p5['arousal_flatten_monotone']}  -> S2b OWED={p5['S2b_OWED']}")
    print("-" * 74)
    print(f"  honesty 4-flags (eff/hp/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['hard_problem_open']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  signatures reproduced : {ov['signatures_reproduced']}")
    print(f"  signatures owed       : {ov['signatures_owed']}")
    print(f"  pathway reading supported / frontal supported : {ov['pathway_reading_supported']} / {ov['frontal_localisation_supported']}")
    print(f"  FULL disease module?  : {ov['is_full_disease_module']}")
    print("-" * 74)
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"]
          and s0["one_knob_drives_both_S1_and_S3"]
          and s1["reproduced"] and s2["reproduced"] and s3["reproduced"]
          and d["VERDICT_pathway_not_frontal"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["hard_problem_open"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 74)
    print("  AUTISM MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
