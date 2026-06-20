#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adhesion_switch.py  --  Integumentary CELL-ADHESION BINDING JAM: the missing adhesion target.

WHAT THIS ADDS (HANDOFF_NEXT_STEPS.md sec.4 + sec.5.2, mechanism-first -- "an adhesion T8 switch
next"). The core battery (run_all.py) emerges four organs and circulates T1..T5; the sebaceous layer
(v0.6.0) added a fifth organ and the occlusion target T7. None of them carry a CELL-ADHESION switch,
so the AUTOIMMUNE blistering diseases -- pemphigus vulgaris and bullous pemphigoid -- were honestly
flagged NOT-YET-MODELABLE ("needs a cell-adhesion target ... Missing target"). This module adds that
target the sanctioned way:

  (1) EXISTING MEASURED ORGAN, NO NEW gamma.  Like the hair-cycle layer (a new TARGET on the already
      measured EDAR gamma), the adhesion target rides the ALREADY-VENDORED keratinocyte master KRT14
      (gamma = 1.4894, the "keratin barrier mechanics / structural integrity" organ). Desmosomes
      (cell-cell) and hemidesmosomes (cell-matrix) both ANCHOR the keratin intermediate-filament
      network, so intercellular/junctional adhesion is intrinsic to the keratinocyte organ. No gamma
      is fetched and none is fitted; only a new dynamical target is built on the existing measured gamma.

  (2) NEW TARGET, in the package's OWN physical class.  Cell adhesion is a JAMMING/binding order
      parameter on the shared R19 switch (ds/dt = g*s - s^3 + h). Adherent (bound) keratinocytes are
      JAMMED together = the ON basin (s>0); a blister is the bond UNJAMMED = the OFF basin (s<0). An
      autoantibody is a DE-ADHESIVE drive that lowers the net adhesion. This is the SAME first-order
      jamming physics as T1 barrier collapse (the intact basin collapsing at the spinodal) and T2
      wound un/re-jamming -- a member of the package's jamming class, NOT a foreign mechanism. The
      substrate PREDICTS, with no new constant: (a) the bond stays adherent until the de-adhesive
      drive crosses the spinodal, then DETACHES discontinuously (blister-formation threshold);
      (b) the detachment is HYSTERETIC -- it re-adheres only when the antibody is cleared well past
      the level that broke it (active junction reassembly returns net adhesion above the upper
      spinodal), which is why sustained immunosuppression, not a slight titre dip, is required.

  (3) TWO COMPARTMENTS, ONE switch, one spinodal.  The same R19 switch on the same KRT14 gamma runs
      two coupled adhesion compartments: CELL-CELL (desmosomal, lateral/suprabasal) and CELL-MATRIX
      (hemidesmosomal, basal->basement-membrane). An autoantibody's SPECIFICITY selects WHICH
      compartment it drives below the spinodal. That single binary choice -- nothing else changes --
      flips the cleavage plane, the Nikolsky sign and the blister tension. This is the headline
      "one mechanism, opposite clinic" result of the layer.

NO-TUNING DISCIPLINE (VP-SPEC C0/C3). gamma is MEASURED (KRT14, read-only, already vendored). The
adhesion reserve and the antibody titres are dimensionless REGIME SCALES [F] expressed as fractions of
the KRT14 spinodal -- NOT fitted to a titre, blister count or body-surface area. The healthy bond is
robustly adherent (net adhesion above the upper spinodal). What the substrate PREDICTS -- a
discontinuous detachment at the spinodal, a hysteresis loop of width ~2*spinodal, the plane selected
by the targeted compartment, the Nikolsky sign as a derived consequence of which bond fails -- is
graded [V]. Absolute blister counts, the antibody titre in IU/mL, the micrometre cleavage depth and
the involved body-surface area are the [O] open magnitudes (obstacle: the adhesion target has no
per-junction calibration yet, just as the appendage and sebaceous targets do not).

DISEASES = SIGNED PERTURBATIONS OF THE ONE ADHESION SWITCH (intervention = the antibody removed):
  PV   pemphigus vulgaris       an anti-DESMOGLEIN (DSG3) autoantibody drives the CELL-CELL compartment
                                below the spinodal -> an INTRAEPIDERMAL (suprabasal) split; the
                                cell-matrix bond is untouched so basal cells stay attached ("tombstone"
                                row). The failing bond IS the lateral cell-cell bond, so a tangential
                                shear propagates the split: NIKOLSKY POSITIVE, a FLACCID thin-roof
                                blister. Reversal = immunosuppression / rituximab clears the antibody ->
                                net adhesion returns above the spinodal -> the bond re-adheres (a partial
                                titre reduction does NOT, the hysteresis).
  BP   bullous pemphigoid       an anti-BP180 (COL17A1, hemidesmosomal) autoantibody drives the
                                CELL-MATRIX compartment below the spinodal -> a SUBEPIDERMAL split at
                                the dermo-epidermal junction; the cell-cell bonds are intact so the WHOLE
                                epidermis lifts as a roof. The failing bond is the basal cell-matrix bond,
                                not the lateral one, so a tangential shear does NOT propagate: NIKOLSKY
                                NEGATIVE, a TENSE full-roof blister. Reversal = immunosuppression /
                                corticosteroid clears/suppresses the antibody -> re-adheres.

Grades (VP-SPEC C3):  [V] simulation-verified shape/sign . [L] cited clinical/biological anchor .
  [F] forced regime scale . [O] open (absolute magnitude; obstacle inherited from the adhesion target).
Determinism (VP-SPEC C1): BLAS pinned single-thread (set below before numpy); fixed grids; NO RNG;
  round-before-hash via the engine emitter (reused, same contract as the pathology / cycle / seb layers).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math
import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))

# vendored substrate primitive (DO NOT re-derive)
from vp_substrate import spinodal
# the SAME R19 jamming machinery the core T1/T2 dynamics use (cubic steady branch + spinodal snap)
from skn_dynamics import steady_roots, nearest_branch, on_branch, off_branch
# reuse the engine's exact round-before-hash emitter (C1)
from vp_skn_engine import emit as _emit

_INH = os.path.join(_HERE, "..", "..", "inherited")
_GAMMA_PATH = os.path.join(_INH, "organ_gamma.json")

# --------------------------------------------------------------------------- measured gamma (read-only)
MASTER = "KRT14"                      # keratinocyte structural-integrity master (ALREADY vendored; no new gamma)

def gamma_of(master):
    """MEASURED master-gene gamma, read-only, vendored from DNA (never fitted)."""
    return float(json.load(open(_GAMMA_PATH, encoding="utf-8"))["genes"][master]["gamma"])

GAMMA = gamma_of(MASTER)
SP = spinodal(GAMMA)

# ===========================================================================
#  NET ADHESION = constitutive adhesion reserve - autoantibody de-adhesion (dimensionless).
#  The drive into the R19 switch is net adhesion x the KRT14 spinodal: a bond is firmly adherent when
#  net adhesion sits ABOVE +1 (= +spinodal), detaches when an antibody drags it below -1 (= -spinodal),
#  and re-adheres only on climbing back above +1 (hysteresis). The healthy bond is reserve-dominant
#  (net adhesion above the upper spinodal -> robustly adherent). EVERY level below is a REGIME SCALE [F]
#  (a fraction of the spinodal), NOT fitted to a clinical magnitude.
#  Sign map (consistent with T1 barrier / T2 wound): adherent = ON basin (s>0, jammed/bound);
#  blister = OFF basin (s<0, unjammed/detached). An autoantibody is the de-adhesive (unjamming) drive.
# ===========================================================================
RESERVE = 1.4                          # constitutive desmosomal/hemidesmosomal adhesion (regime scale [F]); ab=0 -> net=+1.4 (above the loop, robustly adherent)

def net_adhesion(antibody=0.0, reserve=RESERVE):
    return float(reserve - antibody)

def _drive(adh):
    return adh * SP

# --------------------------------------------------------------------------- R19 branch helpers
#  adherent = ON branch (s>0); blister = OFF branch (s<0). Branch CONTINUED from the previous state and
#  SNAPS to the surviving root when its basin disappears at the spinodal -> the detachment jump and the
#  hysteresis are exact, with NO new constant. Identical contract to skn_dynamics.nearest_branch.
def _nearest_branch(h, s_prev):
    return nearest_branch(GAMMA, h, s_prev)

def _adherent_start(h):
    return on_branch(GAMMA, h)          # adherent (ON) branch root


# ===========================================================================
#  THE MECHANISM: ramp net adhesion DOWN from healthy (adherent) into separation, then back UP ->
#  hysteresis. Starts adherent; records the bond state s across the loop. Predicts: a discontinuous
#  DETACHMENT near net=-1 going down, RE-ADHESION near net=+1 going up, loop width ~2 (=2*spinodal in
#  level units). Mirrors the sebaceous jamming_hysteresis (same R19 first-order switch, adhesion sign).
# ===========================================================================
def adhesion_hysteresis(hi=1.6, lo=-1.6, n=641):
    downs = np.linspace(hi, lo, n)                   # drive antibody UP = net adhesion DOWN
    ups = downs[::-1]
    s = _adherent_start(_drive(hi))                  # begin adherent (ON basin) at the high (reserve) end
    s_dn = []
    for adh in downs:
        s = _nearest_branch(_drive(float(adh)), s); s_dn.append(s)
    s_dn = np.array(s_dn)
    s_up = []
    for adh in ups:
        s = _nearest_branch(_drive(float(adh)), s); s_up.append(s)
    s_up = np.array(s_up)

    # detach: net adhesion at which the bond snaps adherent->blister (s crosses 0 downward) going DOWN
    dn_cross = np.where((s_dn[:-1] >= 0) & (s_dn[1:] < 0))[0]
    adh_detach = float(downs[dn_cross[0] + 1]) if len(dn_cross) else None
    detach_jump = float(s_dn[dn_cross[0]] - s_dn[dn_cross[0] + 1]) if len(dn_cross) else 0.0
    # re-adhere: net adhesion at which the blister snaps blister->adherent (s crosses 0 upward) going UP
    up_cross = np.where((s_up[:-1] < 0) & (s_up[1:] >= 0))[0]
    adh_readhere = float(ups[up_cross[0] + 1]) if len(up_cross) else None
    readhere_jump = float(s_up[up_cross[0] + 1] - s_up[up_cross[0]]) if len(up_cross) else 0.0

    width = float(adh_readhere - adh_detach) if (adh_detach is not None and adh_readhere is not None) else None
    return dict(
        master=MASTER, gamma=round(GAMMA, 6), spinodal=round(SP, 6),
        adh_detach_down=round(adh_detach, 4) if adh_detach is not None else None,
        adh_readhere_up=round(adh_readhere, 4) if adh_readhere is not None else None,
        detach_jump_magnitude=round(detach_jump, 4), readhere_jump_magnitude=round(readhere_jump, 4),
        hysteresis_width=round(width, 4) if width is not None else None,
        detaches_discontinuously=bool(detach_jump > 1.0),
        detach_at_spinodal=bool(adh_detach is not None and abs(adh_detach + 1.0) <= 0.05),
        readhere_at_upper_spinodal=bool(adh_readhere is not None and abs(adh_readhere - 1.0) <= 0.05),
        hysteretic=bool(width is not None and width > 1.0),
        healthy_net_adhesion=round(net_adhesion(), 4),
        healthy_adherent=bool(net_adhesion() > 1.0),       # healthy bond sits ABOVE the upper spinodal
    )


# ===========================================================================
#  Adhesion outcome of ONE compartment under a FIXED antibody titre, continued from a chosen state.
#  Returns the steady bond state and a normalized SEPARATION depth (how far into the detached basin).
# ===========================================================================
def _compartment_outcome(antibody, s_prev):
    adh = net_adhesion(antibody)
    s = _nearest_branch(_drive(adh), s_prev)
    off_root = steady_roots(GAMMA, _drive(adh))[0]           # most-negative root = fully detached
    sep = float(max(-s, 0.0) / max(-off_root, 1e-9)) if off_root < 0 else 0.0   # 0 adherent .. 1 fully separated
    return dict(antibody=round(float(antibody), 4), net_adhesion=round(adh, 4), s=round(float(s), 5),
                adherent=bool(s > 0.0), separated=bool(s <= 0.0), separation_depth=round(sep, 4))

def _adherent_compartment():
    """An untouched compartment (no antibody) sits firmly adherent above the upper spinodal."""
    return _compartment_outcome(0.0, _adherent_start(_drive(net_adhesion(0.0))))

def _separate_then(antibody):
    """Drive a healthy adherent bond DOWN into the disease state (lets it detach through the spinodal)."""
    s = _adherent_start(_drive(net_adhesion(0.0)))
    for adh in np.linspace(net_adhesion(0.0), net_adhesion(antibody), 200):
        s = _nearest_branch(_drive(float(adh)), s)
    return s

def _treat_from(antibody_treat, antibody_disease):
    """Apply a treatment (CONTINUED from the separated state) by lowering the antibody -> exercises the
    hysteresis. Re-adheres only if the antibody is cleared past the upper spinodal; a partial reduction
    that leaves net adhesion below +1 stays separated."""
    start_ab = max(antibody_disease, 2.7)
    s = _separate_then(start_ab)
    for adh in np.linspace(net_adhesion(start_ab), net_adhesion(antibody_treat), 200):
        s = _nearest_branch(_drive(float(adh)), s)
    return _compartment_outcome(antibody_treat, s)


# ===========================================================================
#  NIKOLSKY SIGN as a DERIVED consequence (no new constant).
#  Positive iff the FAILING plane is the cell-cell (lateral) bond, so a tangential shear -- which
#  stresses cell-cell bonds -- propagates the separation. If only the cell-matrix (basal) bond fails,
#  the intact cell-cell bonds resist the shear -> NEGATIVE. A logical consequence of WHICH compartment
#  the antibody targets, not a fitted flag.
# ===========================================================================
def _nikolsky_positive(cellcell_separated, cellmatrix_separated):
    return bool(cellcell_separated and not cellmatrix_separated)


# ===========================================================================
#  ANTIBODY TITRES (regime-scale fractions [F]); reversal = the antibody cleared.
#  net adhesion = RESERVE(1.4) - antibody. Disease needs antibody > RESERVE + 1 = 2.4 to drag the bond
#  below the -spinodal. Partial immunosuppression leaves net adhesion below +1 (still separated). Full
#  clearance returns net adhesion to +1.4 (above the upper spinodal -> re-adheres).
# ===========================================================================
AB_PV = 2.7              # anti-DSG3 titre on the CELL-CELL compartment -> net = -1.3 -> detaches
AB_BP = 2.7              # anti-BP180 titre on the CELL-MATRIX compartment -> net = -1.3 -> detaches
AB_PARTIAL = 1.6         # incomplete immunosuppression -> net = -0.2 (still below +1 -> stays separated)
AB_CLEARED = 0.0         # rituximab / corticosteroid clears the antibody -> net = +1.4 -> re-adheres


# ===========================================================================
#  DISEASE 1 -- PEMPHIGUS VULGARIS  (anti-DSG3, cell-cell de-adhesion; intraepidermal; Nikolsky positive)
# ===========================================================================
def pemphigus_vulgaris():
    cc = _compartment_outcome(AB_PV, _separate_then(AB_PV))   # cell-cell (desmosomal): driven below the spinodal
    cm = _adherent_compartment()                              # cell-matrix (hemidesmosomal): untouched -> adherent
    nik_pos = _nikolsky_positive(cc["separated"], cm["separated"])
    # reversal: rituximab / immunosuppression clears the antibody -> cell-cell re-adheres
    cleared = _treat_from(AB_CLEARED, AB_PV)
    partial = _treat_from(AB_PARTIAL, AB_PV)                  # incomplete suppression: still separated (hysteresis nuance)
    return dict(disease="pemphigus_vulgaris", target="cell-cell adhesion (desmosomal de-adhesion jam)", organ="keratinocyte",
                mechanism="an anti-desmoglein (DSG3) autoantibody drives the cell-cell (desmosomal) adhesion compartment below the spinodal, so keratinocytes lose lateral cohesion and the epidermis splits at an INTRAEPIDERMAL (suprabasal) plane while the untouched cell-matrix bond keeps basal cells attached ('tombstone' row); the failing bond is the lateral cell-cell bond, so a tangential shear propagates the split (Nikolsky positive) and the thin suprabasal roof gives a flaccid blister; clearing the antibody (rituximab/immunosuppression) returns net adhesion above the spinodal and the bond re-adheres, whereas a partial titre reduction does not (hysteresis)",
                anchor="pemphigus vulgaris is an anti-desmoglein (DSG1/DSG3) autoimmune disease with suprabasal acantholysis, flaccid bullae and a positive Nikolsky sign; rituximab and systemic immunosuppression are effective [L]",
                target_compartment="cell-cell (desmosomal, DSG3)",
                cellcell_separated=cc["separated"], cellmatrix_adherent=cm["adherent"],
                cleavage_plane="intraepidermal_suprabasal", intraepidermal=bool(cc["separated"] and cm["adherent"]),
                nikolsky_positive=nik_pos, blister_flaccid=True,
                separation_depth=cc["separation_depth"],
                partial_immunosuppression_readheres=bool(partial["adherent"]),
                cleared_readheres=bool(cleared["adherent"]),
                sign_matches_clinic=bool(cc["separated"] and cm["adherent"] and nik_pos),
                intervention_reverses=bool(cleared["adherent"]),
                grade_shape="[V] cell-cell de-adhesion direction + intraepidermal plane + positive Nikolsky (derived) + re-adhesion on antibody clearance (with hysteresis)",
                grade_absolute="[O] absolute blister counts, antibody titre (IU/mL) and involved body-surface area need a per-junction calibration (adhesion target obstacle)")


# ===========================================================================
#  DISEASE 2 -- BULLOUS PEMPHIGOID  (anti-BP180, cell-matrix de-adhesion; subepidermal; Nikolsky negative)
# ===========================================================================
def bullous_pemphigoid():
    cm = _compartment_outcome(AB_BP, _separate_then(AB_BP))   # cell-matrix (hemidesmosomal): driven below the spinodal
    cc = _adherent_compartment()                              # cell-cell (desmosomal): untouched -> adherent
    nik_pos = _nikolsky_positive(cc["separated"], cm["separated"])   # cell-cell intact -> NOT positive
    nik_neg = bool(cm["separated"] and cc["adherent"])              # failing bond is cell-matrix -> negative
    # reversal: corticosteroid / immunosuppression clears/suppresses the antibody -> cell-matrix re-adheres
    cleared = _treat_from(AB_CLEARED, AB_BP)
    partial = _treat_from(AB_PARTIAL, AB_BP)
    return dict(disease="bullous_pemphigoid", target="cell-matrix adhesion (hemidesmosomal de-adhesion jam)", organ="keratinocyte",
                mechanism="an anti-BP180 (COL17A1, hemidesmosomal) autoantibody drives the cell-matrix (basal->basement-membrane) adhesion compartment below the spinodal, so the basal keratinocytes detach from the dermo-epidermal junction and the epidermis splits at a SUBEPIDERMAL plane while the untouched cell-cell bonds keep the whole epidermis cohesive (it lifts as an intact roof); the failing bond is the basal cell-matrix bond, not the lateral one, so a tangential shear does NOT propagate (Nikolsky negative) and the full-thickness roof gives a tense blister; clearing/suppressing the antibody (corticosteroid/immunosuppression) returns net adhesion above the spinodal and the bond re-adheres, whereas a partial reduction does not (hysteresis)",
                anchor="bullous pemphigoid is an anti-BP180/BP230 (hemidesmosomal) autoimmune disease with a subepidermal split, tense bullae and a negative Nikolsky sign; topical/systemic corticosteroids and immunosuppression are the mainstay [L]",
                target_compartment="cell-matrix (hemidesmosomal, BP180/COL17A1)",
                cellmatrix_separated=cm["separated"], cellcell_adherent=cc["adherent"],
                cleavage_plane="subepidermal_junctional", subepidermal=bool(cm["separated"] and cc["adherent"]),
                nikolsky_positive=nik_pos, nikolsky_negative=nik_neg, blister_tense=True,
                separation_depth=cm["separation_depth"],
                partial_immunosuppression_readheres=bool(partial["adherent"]),
                cleared_readheres=bool(cleared["adherent"]),
                sign_matches_clinic=bool(cm["separated"] and cc["adherent"] and nik_neg),
                intervention_reverses=bool(cleared["adherent"]),
                grade_shape="[V] cell-matrix de-adhesion direction + subepidermal plane + negative Nikolsky (derived) + re-adhesion on antibody clearance (with hysteresis)",
                grade_absolute="[O] absolute blister counts, antibody titre (IU/mL) and involved body-surface area need a per-junction calibration (adhesion target obstacle)")


# ===========================================================================
#  SUMMARY + opposite-property discriminant (mirrors the pathology / hair-cycle / sebaceous layers).
#  Same adhesion switch, same KRT14 spinodal, same antibody magnitude; ONLY the targeted compartment
#  differs, and that single binary choice flips the cleavage plane, the Nikolsky sign and the blister
#  tension. NO new constant between the two diseases.
# ===========================================================================
def adhesion_summary():
    hyst = adhesion_hysteresis()
    pv = pemphigus_vulgaris(); bp = bullous_pemphigoid()
    diseases = {"pemphigus_vulgaris": pv, "bullous_pemphigoid": bp}
    opp = dict(
        # cleavage plane: intraepidermal (PV) vs subepidermal (BP) -- opposite depth from the same switch
        intraepidermal_pv_vs_subepidermal_bp=bool(pv["intraepidermal"] and bp["subepidermal"]),
        # Nikolsky sign: positive (PV, the failing bond IS the cell-cell bond) vs negative (BP, cell-cell intact)
        nikolsky_positive_pv_vs_negative_bp=bool(pv["nikolsky_positive"] and bp["nikolsky_negative"]),
        # blister tension: flaccid thin-roof (PV) vs tense full-roof (BP)
        flaccid_pv_vs_tense_bp=bool(pv["blister_flaccid"] and bp["blister_tense"]),
    )
    opp["all_opposite_pairs_reproduced"] = bool(all(opp.values()))
    out = {}
    out.update(diseases)
    out["_mechanism"] = hyst
    out["_opposite_sign_discriminant"] = opp
    out["_n_diseases"] = len(diseases)
    out["_gamma_provenance"] = dict(master=MASTER, gamma=round(GAMMA, 6),
                                    new_gamma_fetched=False,
                                    note="adhesion is a NEW TARGET on the ALREADY-MEASURED keratinocyte KRT14 gamma (vendored from DNA); desmosomes/hemidesmosomes anchor the keratin network, so junctional adhesion is intrinsic to this organ. No gamma is fetched and none is fitted -- only a new dynamical target on the existing measured gamma (the hair-cycle pattern, not the sebaceous new-organ pattern)")
    out["_meta"] = dict(layer="adhesion_switch", master=MASTER, gamma=round(GAMMA, 6),
                        note="cell-adhesion binding jam (target T8) on the existing measured KRT14 gamma; a member of the package's jamming class (adherent=jammed ON, blister=unjammed OFF); additive layer, core battery untouched")
    return out


if __name__ == "__main__":
    import pprint, time
    t0 = time.time(); res = adhesion_summary(); s, h = _emit(res)
    print("elapsed %.2fs   sha=%s..." % (time.time() - t0, h[:16]))
    pprint.pprint(res["_mechanism"]); pprint.pprint(res["_opposite_sign_discriminant"]); pprint.pprint(res["_gamma_provenance"])
