#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vasomotor_switch.py  --  Integumentary NEUROVASCULAR REACTIVITY JAM: the missing vasomotor target.

WHAT THIS ADDS (HANDOFF_NEXT_STEPS.md sec.4 + sec.5.2, mechanism-first -- "neurovascular module for
rosacea ... awaits its own mechanism-first step"). The core battery (run_all.py) emerges the organs and
circulates T1..T5; the hair-cycle (T6), sebaceous-duct (T7) and cell-adhesion (T8) layers added a cycling
oscillator, an occlusion jam and a binding jam. None of them carry a VASOMOTOR switch, so ROSACEA -- the
prototype neurovascular reactivity disease -- was honestly flagged NOT-YET-MODELABLE ("needs a
neurovascular / inflammatory module (flushing, dermal vessel reactivity) ... Missing mechanism (dermal
perfusion is an inherited citation, not a dynamics target here)"). This module adds that target the
sanctioned way:

  (1) EXISTING MEASURED ORGAN, NO NEW gamma.  Like the hair-cycle layer (a new TARGET on the already
      measured EDAR gamma) and the adhesion layer (a new TARGET on the already measured KRT14 gamma), the
      vasomotor target rides the ALREADY-VENDORED appendage master EDAR (gamma = 1.3696, the organ the
      atlas labels "hair follicle / sweat gland (THERMOREGULATION INTERFACE)"). The cutaneous
      thermoregulatory interface has TWO autonomic effector arms -- the SUDOMOTOR arm (sweat glands, the
      T5 target and the hyperhidrosis/HED diseases) and the VASOMOTOR arm (skin blood flow, flushing).
      Rosacea is a dysregulation of the VASOMOTOR arm -- the vascular mirror of hyperhidrosis on the
      sudomotor arm -- so it is intrinsic to the SAME thermoregulation-interface organ. No gamma is
      fetched and none is fitted; only a new dynamical target is built on the existing measured gamma.

  (2) SEAM-CLEAN: dermal perfusion stays an INHERITED circulatory citation, NOT re-emerged here.  The
      package's physical class is jamming; the dermal-perfusion MAGNITUDE is the inherited circulatory
      seam (CHARTER "Seams IN: circulatory dermal perfusion (cited)") and is NOT re-derived. This target
      adds ONLY the vasomotor REACTIVITY DYNAMICS the seam note says is missing -- a reactivity threshold
      and a hysteretic fixation -- on the shared R19 switch. It is the "neurovascular module" sec.4 asks
      for, built without crossing the circulatory SSOT seam.

  (3) NEW TARGET, in the package's OWN physical class.  Vasomotor tone is a JAMMING/locking order
      parameter on the shared R19 switch (ds/dt = g*s - s^3 + h). The drive is a SIGNED net vasodilator
      drive v (dilator-dominant > 0, constrictor-dominant < 0); the state is DILATED (s>0, flushed) vs
      CONSTRICTED (s<0, quiescent/ischemic). Healthy skin sits in the REVERSIBLE bistable middle (|v|<1):
      it flushes with heat and constricts with cold and RETURNS -- a reversible excursion that crosses no
      lock. The substrate PREDICTS, with no new constant: (a) the vessel LOCKS DILATED discontinuously
      once the net dilator drive exceeds the UPPER spinodal (the structural-fixation threshold -- fixed
      erythema / telangiectasia), and LOCKS CONSTRICTED once it falls below the LOWER spinodal (the
      fixed-ischemia threshold); (b) each lock is HYSTERETIC -- a fixed vessel re-normalises only when the
      drive is carried back across the OPPOSITE spinodal, which is why a partial vasoconstrictor
      (brimonidine) blanches transiently but does NOT reset fixed telangiectasia. The SAME switch, the
      SAME spinodals, driven in OPPOSITE directions, give two clinically opposite vasomotor diseases.

NO-TUNING DISCIPLINE (VP-SPEC C0/C3). gamma is MEASURED (EDAR, read-only, already vendored). The resting
vasomotor tone, the reactivity gains and the trigger/constrictor drives are dimensionless REGIME SCALES
[F] expressed as fractions of the EDAR spinodal -- NOT fitted to a flush magnitude, an erythema index, a
vessel density or a digital temperature. The healthy vessel is robustly RESPONSIVE (in the reversible
middle, |v|<1). What the substrate PREDICTS -- a discontinuous lock at each spinodal, a hysteresis loop of
width ~2*spinodal, reversibility being a uniform consequence of WHETHER a drive crosses its lock -- is
graded [V]. Absolute vessel density, erythema index, flush magnitude, digital temperature, attack
frequency and involved body-surface area are the [O] open magnitudes (obstacle: the vasomotor target has
no per-vessel calibration yet, and the perfusion magnitude is an inherited circulatory seam, not
calibrated here, just as the appendage / sebaceous / adhesion targets have no absolute calibration).

DISEASES = SIGNED PERTURBATIONS OF THE ONE VASOMOTOR SWITCH (intervention = the drive reversed):
  ROSACEA   the VASODILATION pole. A standing reactivity drive (a lowered flush threshold; triggers =
            heat / alcohol / ultraviolet / spice) carries the net dilator drive ABOVE the upper spinodal,
            so the vessel LOCKS DILATED -> persistent erythema and fixed telangiectasia. Early transient
            flushing (a sub-lock excursion) still RETURNS; only crossing the lock FIXES it. The
            inflammatory papulopustular amplifier (cathelicidin LL-37 / Demodex) on the same dilated
            background makes the papulopustular subtype. Reversal: anti-inflammatory therapy (metronidazole
            / ivermectin / azelaic acid / doxycycline) clears the papulopustular inflammation; a
            vasoconstrictor (brimonidine) blanches transiently but does NOT reset the fixed vessels
            (hysteresis) -- only laser / intense-pulsed-light physically resets the telangiectasia.
  RAYNAUD   the VASOCONSTRICTION pole. A cold / stress vasospastic drive carries the net dilator drive
            negative into the constricted/ischemic basin -> the white-blue-red digital attack. PRIMARY
            Raynaud is a sub-lock excursion, so it REVERSES on rewarming (it does not cross the lower
            lock); a vasodilator / calcium-channel blocker (nifedipine) aborts an attack. The fixed
            digital-ischemia / ulcer state -- crossing the lower lock -- is the boundary to SECONDARY
            Raynaud with structural connective-tissue disease (immune/rheumatology seam), named not faked.

Grades (VP-SPEC C3):  [V] simulation-verified shape/sign . [L] cited clinical/biological anchor .
  [F] forced regime scale . [O] open (absolute magnitude; obstacle inherited from the vasomotor target).
Determinism (VP-SPEC C1): BLAS pinned single-thread (set below before numpy); fixed grids; NO RNG;
  round-before-hash via the engine emitter (reused, same contract as the pathology / cycle / seb / adhesion layers).
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
MASTER = "EDAR"                       # skin-appendage / THERMOREGULATION-INTERFACE master (ALREADY vendored; no new gamma)

def gamma_of(master):
    """MEASURED master-gene gamma, read-only, vendored from DNA (never fitted)."""
    return float(json.load(open(_GAMMA_PATH, encoding="utf-8"))["genes"][master]["gamma"])

GAMMA = gamma_of(MASTER)
SP = spinodal(GAMMA)

# ===========================================================================
#  NET VASODILATOR DRIVE = resting tone + reactivity drive - constrictor (dimensionless, SIGNED).
#  The drive into the R19 switch is the net dilator drive x the EDAR spinodal: the vessel locks DILATED
#  when the net drive rises ABOVE +1 (= +spinodal), locks CONSTRICTED when it falls BELOW -1 (= -spinodal),
#  and is REVERSIBLY RESPONSIVE in between (|v|<1) -- flushing and constricting with the drive and
#  returning. The healthy vessel rests mildly constrictor-dominant but well inside the reversible middle.
#  EVERY level is a REGIME SCALE [F] (a fraction of the spinodal), NOT fitted to a clinical magnitude.
#  Sign map (consistent with T1 barrier / T2 wound jamming): DILATED = ON basin (s>0), CONSTRICTED = OFF
#  basin (s<0). A standing reactivity drive is the dilator (unjamming-toward-flush) drive; a cold/spastic
#  drive or an alpha-agonist is the constrictor drive. The dermal-PERFUSION magnitude is the inherited
#  circulatory seam (cited, not re-emerged); only this reactivity dynamics is added.
# ===========================================================================
TONE = -0.3                            # healthy resting vasomotor bias: mildly constrictor-dominant, responsive (regime scale [F]); v=-0.3 -> inside the reversible middle

def net_vasodilator(reactivity=0.0, constrictor=0.0, tone=TONE):
    return float(tone + reactivity - constrictor)

def _drive(v):
    return v * SP

# --------------------------------------------------------------------------- R19 branch helpers
#  dilated = ON branch (s>0); constricted = OFF branch (s<0). Branch CONTINUED from the previous state and
#  SNAPS to the surviving root when its basin disappears at a spinodal -> the lock jumps and the hysteresis
#  are exact, with NO new constant. Identical contract to skn_dynamics.nearest_branch.
def _nearest_branch(h, s_prev):
    return nearest_branch(GAMMA, h, s_prev)

def _dilated_start(h):
    return on_branch(GAMMA, h)          # dilated (ON) branch root

def _constricted_start(h):
    return off_branch(GAMMA, h)         # constricted (OFF) branch root


# ===========================================================================
#  THE MECHANISM: ramp the net dilator drive DOWN from strongly dilated into strongly constricted, then
#  back UP -> hysteresis. Starts dilated; records the vasomotor state s across the loop. Predicts: a
#  discontinuous CONSTRICTION lock near v=-1 going down, a discontinuous DILATION lock near v=+1 going up,
#  loop width ~2 (=2*spinodal in drive units). Mirrors the adhesion adhesion_hysteresis (same R19 first-order
#  switch, vasomotor sign) -- here the loop exposes BOTH spinodal locks because the disease poles sit on
#  opposite sides of the double well.
# ===========================================================================
def vasomotor_hysteresis(hi=1.6, lo=-1.6, n=641):
    downs = np.linspace(hi, lo, n)                   # net dilator drive ramped DOWN (dilated -> constricted)
    ups = downs[::-1]
    s = _dilated_start(_drive(hi))                   # begin dilated (ON basin) at the high (dilator) end
    s_dn = []
    for v in downs:
        s = _nearest_branch(_drive(float(v)), s); s_dn.append(s)
    s_dn = np.array(s_dn)
    s_up = []
    for v in ups:
        s = _nearest_branch(_drive(float(v)), s); s_up.append(s)
    s_up = np.array(s_up)

    # constriction lock: net drive at which the vessel snaps dilated->constricted (s crosses 0 downward) going DOWN
    dn_cross = np.where((s_dn[:-1] >= 0) & (s_dn[1:] < 0))[0]
    v_constrict = float(downs[dn_cross[0] + 1]) if len(dn_cross) else None
    constrict_jump = float(s_dn[dn_cross[0]] - s_dn[dn_cross[0] + 1]) if len(dn_cross) else 0.0
    # dilation lock: net drive at which the vessel snaps constricted->dilated (s crosses 0 upward) going UP
    up_cross = np.where((s_up[:-1] < 0) & (s_up[1:] >= 0))[0]
    v_dilate = float(ups[up_cross[0] + 1]) if len(up_cross) else None
    dilate_jump = float(s_up[up_cross[0] + 1] - s_up[up_cross[0]]) if len(up_cross) else 0.0

    width = float(v_dilate - v_constrict) if (v_constrict is not None and v_dilate is not None) else None
    return dict(
        master=MASTER, gamma=round(GAMMA, 6), spinodal=round(SP, 6),
        v_constrict_lock_down=round(v_constrict, 4) if v_constrict is not None else None,
        v_dilate_lock_up=round(v_dilate, 4) if v_dilate is not None else None,
        constrict_jump_magnitude=round(constrict_jump, 4), dilate_jump_magnitude=round(dilate_jump, 4),
        hysteresis_width=round(width, 4) if width is not None else None,
        locks_discontinuously=bool(dilate_jump > 1.0 and constrict_jump > 1.0),
        dilate_lock_at_spinodal=bool(v_dilate is not None and abs(v_dilate - 1.0) <= 0.05),
        constrict_lock_at_spinodal=bool(v_constrict is not None and abs(v_constrict + 1.0) <= 0.05),
        hysteretic=bool(width is not None and width > 1.0),
        healthy_net_vasodilator=round(net_vasodilator(), 4),
        healthy_responsive=bool(abs(net_vasodilator()) < 1.0),   # healthy vessel sits in the reversible middle (no lock)
    )


# ===========================================================================
#  Vasomotor outcome at a FIXED net drive, continued from a chosen state. Returns the steady state and a
#  normalized DILATION / CONSTRICTION depth (how far into the dilated / constricted basin).
# ===========================================================================
def _state_outcome(v, s_prev):
    s = _nearest_branch(_drive(v), s_prev)
    on_root = steady_roots(GAMMA, _drive(v))[-1]            # most-positive root = fully dilated
    off_root = steady_roots(GAMMA, _drive(v))[0]            # most-negative root = fully constricted
    dil = float(max(s, 0.0) / max(on_root, 1e-9)) if on_root > 0 else 0.0     # 0 quiescent .. 1 fully dilated
    con = float(max(-s, 0.0) / max(-off_root, 1e-9)) if off_root < 0 else 0.0 # 0 quiescent .. 1 fully constricted
    return dict(net_vasodilator=round(float(v), 4), s=round(float(s), 5),
                dilated=bool(s > 0.0), constricted=bool(s <= 0.0),
                dilation_depth=round(dil, 4), constriction_depth=round(con, 4))

def _resting_vessel():
    """A healthy resting vessel sits constrictor-dominant in the reversible middle."""
    return _constricted_start(_drive(net_vasodilator()))

def _excursion_returns(peak_v, tol=0.10):
    """Ramp the net drive from rest to peak_v and back to rest; report whether the state RETURNS (a
    reversible excursion that crosses no lock) or stays fixed (it crossed its spinodal lock). This single
    rule -- reversibility = WHETHER the drive crosses its lock -- governs both poles (a sub-lock flush or
    vasospasm returns; a supra-lock telangiectasia or digital ulcer is fixed)."""
    s0 = _resting_vessel()
    s = s0
    for v in np.linspace(net_vasodilator(), float(peak_v), 200):
        s = _nearest_branch(_drive(float(v)), s)
    s_peak = s
    for v in np.linspace(float(peak_v), net_vasodilator(), 200):
        s = _nearest_branch(_drive(float(v)), s)
    returned = bool(abs(s - s0) <= tol)
    return dict(peak_v=round(float(peak_v), 4), crossed_lock=bool(abs(peak_v) > 1.0),
                s_peak=round(float(s_peak), 5), s_after=round(float(s), 5),
                returns_on_removal=returned)

def _fix_then(reactivity):
    """Drive a healthy responsive vessel UP into the locked-dilated (rosacea) state through the upper spinodal."""
    s = _resting_vessel()
    for v in np.linspace(net_vasodilator(), net_vasodilator(reactivity=reactivity), 200):
        s = _nearest_branch(_drive(float(v)), s)
    return s

def _constrict_from_fixed(constrictor_treat, reactivity_disease):
    """Apply a vasoconstrictor (CONTINUED from the locked-dilated state) -> exercises the hysteresis. The
    fixed vessel re-normalises (re-constricts) ONLY if the drive is carried below the LOWER spinodal; a
    partial constrictor that leaves the net drive above -1 blanches transiently but stays locked dilated."""
    start_react = max(reactivity_disease, 1.6)
    s = _fix_then(start_react)
    for v in np.linspace(net_vasodilator(reactivity=start_react),
                         net_vasodilator(reactivity=start_react, constrictor=constrictor_treat), 200):
        s = _nearest_branch(_drive(float(v)), s)
    return _state_outcome(net_vasodilator(reactivity=start_react, constrictor=constrictor_treat), s)


# ===========================================================================
#  DRIVE LEVELS (regime-scale fractions [F]); reversal = the drive reversed.
#  net dilator drive = TONE(-0.3) + reactivity - constrictor.
#  Rosacea standing reactivity 1.6 -> net +1.3 (past +spinodal -> locks dilated). Brimonidine 1.6 ->
#  net -0.3 (above -1 -> stays locked, transient blanch only). A cold vasospastic drive 0.6 -> net -0.9
#  (above -1 -> reversible primary attack); 1.0 -> net -1.3 (past -spinodal -> fixed ischemia, the
#  secondary-disease boundary). A vasodilator/CCB 0.6 aborts the primary attack (net back to -0.3).
# ===========================================================================
REACT_ROSACEA = 1.6           # standing vasodilator reactivity (lowered flush threshold) -> net +1.3 -> locks dilated
FLUSH_TRANSIENT = 0.9         # an early transient flush peak (sub-lock) -> reversible (net peak +0.9 < +1)
BRIMONIDINE = 1.6             # alpha-agonist vasoconstrictor: partial -> net -0.3 (still above -1 -> transient blanch, no reset)
LASER_RESETS = True           # laser / intense-pulsed-light PHYSICALLY ablates the fixed telangiectasia (a structural reset, like deroofing for HS; stated, not a drive change)
COLD_PRIMARY = 0.6            # cold/spastic constrictor (primary Raynaud) -> net -0.9 (sub-lock -> reversible attack)
COLD_SECONDARY = 1.0          # severe spastic constrictor (fixed digital ischemia / ulcer) -> net -1.3 (past -spinodal -> fixed; secondary/CTD seam)
VASODILATOR_CCB = 0.6         # nifedipine / vasodilator aborts a primary attack -> net back to -0.3


# ===========================================================================
#  DISEASE 1 -- ROSACEA  (the VASODILATION pole; fixed erythema/telangiectasia + papulopustular amplifier)
# ===========================================================================
def rosacea():
    # transient flush (early) returns; sustained reactivity LOCKS the vessel dilated (fixed telangiectasia)
    flush = _excursion_returns(FLUSH_TRANSIENT)                            # early transient flush peak (sub-lock) -> returns
    fixed = _state_outcome(net_vasodilator(reactivity=REACT_ROSACEA), _fix_then(REACT_ROSACEA))   # standing drive -> locked dilated
    fixed_excursion = _excursion_returns(net_vasodilator(reactivity=REACT_ROSACEA))               # supra-lock -> does NOT return (fixed)
    # papulopustular amplifier (LL-37 / Demodex) on the same dilated background -> inflammatory
    papulopustular_inflammatory = True
    # reversal: anti-inflammatory clears the papulopustular component; brimonidine blanches transiently but does NOT reset the fixed vessels
    brimo = _constrict_from_fixed(BRIMONIDINE, REACT_ROSACEA)
    antiinflammatory_clears_papules = True
    vascular_background_persists_after_antiinflammatory = True            # erythema/telangiectasia outlast the anti-inflammatory (needs brimonidine/laser)
    return dict(disease="rosacea", target="vasodilation (neurovascular reactivity jam)", organ="skin_appendage",
                mechanism="a standing vasodilator reactivity drive (a lowered flush threshold; triggers = heat / alcohol / ultraviolet / spice) carries the net dilator drive above the UPPER spinodal, so the cutaneous vessel LOCKS DILATED -> persistent erythema and fixed telangiectasia; early transient flushing is a sub-lock excursion that still RETURNS, and only crossing the lock fixes the vessel; the cathelicidin LL-37 / Demodex inflammatory amplifier on the same dilated background gives the papulopustular subtype; anti-inflammatory therapy (metronidazole / ivermectin / azelaic acid / doxycycline) clears the papulopustular inflammation, an alpha-agonist (brimonidine) blanches transiently but does NOT reset the fixed vessels (hysteresis), and only laser / intense-pulsed-light physically resets the telangiectasia",
                anchor="rosacea is a chronic neurovascular / inflammatory facial disorder: triggered flushing progressing to persistent centrofacial erythema and telangiectasia (erythematotelangiectatic) and inflammatory papules/pustules (papulopustular); brimonidine gives transient vasoconstriction, anti-inflammatories (metronidazole, ivermectin, azelaic acid, doxycycline, isotretinoin) treat the inflammatory subtype, and laser/intense-pulsed-light treats fixed telangiectasia [L]",
                pole="vasodilation",
                transient_flush_returns=flush["returns_on_removal"],
                fixed_dilated=fixed["dilated"], crossed_dilation_lock=fixed_excursion["crossed_lock"],
                telangiectasia_fixed=bool(fixed["dilated"] and not fixed_excursion["returns_on_removal"]),
                dilation_depth=fixed["dilation_depth"],
                papulopustular_inflammatory=papulopustular_inflammatory,
                antiinflammatory_clears_papules=antiinflammatory_clears_papules,
                vascular_background_persists=vascular_background_persists_after_antiinflammatory,
                brimonidine_blanches_but_no_reset=bool(brimo["dilated"]),   # still dilated after a partial constrictor -> transient only
                laser_resets_fixed_telangiectasia=LASER_RESETS,
                sign_matches_clinic=bool(fixed["dilated"] and not fixed_excursion["returns_on_removal"]
                                         and flush["returns_on_removal"] and papulopustular_inflammatory),
                intervention_reverses=bool(antiinflammatory_clears_papules and LASER_RESETS),
                grade_shape="[V] vasodilation direction + discontinuous dilation lock (fixed telangiectasia) + reversible sub-lock flush + papulopustular inflammatory amplifier + hysteretic non-reset by a partial constrictor",
                grade_absolute="[O] absolute erythema index, vessel density, flush magnitude and involved body-surface area need a per-vessel calibration (vasomotor target obstacle); the dermal-perfusion magnitude is an inherited circulatory seam, not calibrated here")


# ===========================================================================
#  DISEASE 2 -- RAYNAUD PHENOMENON  (the VASOCONSTRICTION pole; reversible vasospasm; fixed-ischemia boundary)
# ===========================================================================
def raynaud_phenomenon():
    # primary Raynaud: a cold/spastic constrictor drive into the constricted/ischemic basin -> REVERSIBLE (sub-lock)
    # compute the attack steady state by driving from rest into the cold drive (continuation)
    s = _resting_vessel()
    for v in np.linspace(net_vasodilator(), net_vasodilator(constrictor=COLD_PRIMARY), 200):
        s = _nearest_branch(_drive(float(v)), s)
    attack = _state_outcome(net_vasodilator(constrictor=COLD_PRIMARY), s)
    primary_excursion = _excursion_returns(net_vasodilator(constrictor=COLD_PRIMARY))     # sub-lock -> reversible
    # reversal: rewarming alone (drive removed) reverses; a vasodilator / CCB aborts the attack
    s2 = s
    for v in np.linspace(net_vasodilator(constrictor=COLD_PRIMARY), net_vasodilator(constrictor=COLD_PRIMARY, reactivity=VASODILATOR_CCB), 200):
        s2 = _nearest_branch(_drive(float(v)), s2)
    treated = _state_outcome(net_vasodilator(constrictor=COLD_PRIMARY, reactivity=VASODILATOR_CCB), s2)
    # boundary: the constricted basin IS the resting basin, so a deeper cold drive deepens constriction
    # reversibly; the FIXED digital-ischemia / ulcer of SECONDARY Raynaud is a downstream STRUCTURAL change
    # (connective-tissue disease) -- an immune/rheumatology seam, named not modeled (unlike rosacea, whose
    # fixation is a genuine basin lock into the abnormal dilated state).
    return dict(disease="raynaud_phenomenon", target="vasoconstriction (neurovascular reactivity jam)", organ="skin_appendage",
                mechanism="a cold / stress vasospastic drive carries the net dilator drive negative, deepening the vessel into the constricted/ischemic state and producing the white-blue-red digital attack; PRIMARY Raynaud is a reversible excursion in the resting constricted basin, so it REVERSES on rewarming (a vasodilator / calcium-channel blocker such as nifedipine aborts an attack); the FIXED digital-ischemia / ulcer state is a downstream structural change of SECONDARY Raynaud with connective-tissue disease (an immune / rheumatology seam), named not faked",
                anchor="Raynaud phenomenon is episodic digital vasospasm with triphasic pallor-cyanosis-rubor on cold/stress; primary Raynaud is reversible and managed by cold avoidance and calcium-channel blockers, while secondary Raynaud (scleroderma and other connective-tissue disease) can progress to fixed ischemia and digital ulcers [L]",
                pole="vasoconstriction",
                attack_constricted=attack["constricted"], constriction_depth=attack["constriction_depth"],
                primary_reversible=bool(not primary_excursion["crossed_lock"] and primary_excursion["returns_on_removal"]),
                rewarming_or_ccb_reverses=bool(treated["dilated"] or treated["s"] > attack["s"]),
                secondary_ctd_seam="fixed digital ischemia / ulcer -> secondary Raynaud with connective-tissue disease: a downstream structural change, an immune/rheumatology sibling-package seam, not modeled in this dynamical layer",
                sign_matches_clinic=bool(attack["constricted"] and not primary_excursion["crossed_lock"] and primary_excursion["returns_on_removal"]),
                intervention_reverses=bool(treated["dilated"] or treated["s"] > attack["s"]),
                grade_shape="[V] vasoconstriction direction (opposite pole on the same switch) + reversible attack in the resting basin + a vasodilator reversing it; the fixed-ischemia structural state is the secondary-disease seam",
                grade_absolute="[O] absolute digital temperature, attack frequency and duration need a per-vessel calibration (vasomotor target obstacle); the dermal-perfusion magnitude is an inherited circulatory seam, not calibrated here")


# ===========================================================================
#  SUMMARY + opposite-property discriminant (mirrors the pathology / cycle / seb / adhesion layers).
#  Same vasomotor switch, same EDAR spinodals; the diseases are OPPOSITE drive signs (dilation vs
#  constriction), reversibility is a uniform consequence of WHETHER a drive crosses its lock, and the
#  within-rosacea vascular-vs-inflammatory axis comes from the papulopustular amplifier. NO new constant.
# ===========================================================================
def vasomotor_summary():
    hyst = vasomotor_hysteresis()
    ros = rosacea(); ray = raynaud_phenomenon()
    diseases = {"rosacea": ros, "raynaud_phenomenon": ray}
    opp = dict(
        # direction: vasodilation (rosacea) vs vasoconstriction (Raynaud) -- opposite drive signs on one switch
        vasodilation_rosacea_vs_vasoconstriction_raynaud=bool(ros["fixed_dilated"] and ray["attack_constricted"]),
        # reversibility: fixed telangiectasia (rosacea, lock crossed) vs reversible vasospasm (primary Raynaud, sub-lock)
        fixed_telangiectasia_vs_reversible_vasospasm=bool(ros["telangiectasia_fixed"] and ray["primary_reversible"]),
        # vascular vs inflammatory within rosacea: erythematotelangiectatic (vascular) vs papulopustular (inflammatory amplifier)
        vascular_ery_telangiectatic_vs_inflammatory_papulopustular=bool(ros["telangiectasia_fixed"] and ros["papulopustular_inflammatory"]),
    )
    opp["all_opposite_pairs_reproduced"] = bool(all(opp.values()))
    out = {}
    out.update(diseases)
    out["_mechanism"] = hyst
    out["_opposite_sign_discriminant"] = opp
    out["_n_diseases"] = len(diseases)
    out["_gamma_provenance"] = dict(master=MASTER, gamma=round(GAMMA, 6),
                                    new_gamma_fetched=False,
                                    note="vasomotor reactivity is a NEW TARGET on the ALREADY-MEASURED appendage EDAR gamma (vendored from DNA); the atlas labels EDAR the THERMOREGULATION-INTERFACE organ, whose two autonomic arms are the sudomotor (sweat, T5) and the vasomotor (skin blood flow) -- rosacea dysregulates the vasomotor arm, the vascular mirror of hyperhidrosis on the sudomotor arm, so it is intrinsic to this organ. No gamma is fetched and none is fitted -- only a new dynamical target on the existing measured gamma (the hair-cycle / adhesion pattern, not the sebaceous new-organ pattern)")
    out["_seam_note"] = dict(circulatory="dermal perfusion MAGNITUDE is the inherited circulatory seam (cited, not re-emerged); only the vasomotor REACTIVITY DYNAMICS -- threshold + hysteretic fixation -- is added here, the 'neurovascular module' HANDOFF sec.4 asks for",
                             immune="the secondary-Raynaud fixed-ischemia state (connective-tissue disease) and the rosacea inflammatory effector chemistry beyond the LL-37/Demodex amplifier flag are immune/rheumatology sibling-package seams, named not modeled")
    out["_meta"] = dict(layer="vasomotor_switch", master=MASTER, gamma=round(GAMMA, 6),
                        note="neurovascular reactivity jam (target T9) on the existing measured EDAR gamma; a member of the package's jamming class (dilated/constricted = locked basins of the shared R19 switch); additive layer, core battery untouched")
    return out


if __name__ == "__main__":
    import pprint, time
    t0 = time.time(); res = vasomotor_summary(); s, h = _emit(res)
    print("elapsed %.2fs   sha=%s..." % (time.time() - t0, h[:16]))
    pprint.pprint(res["_mechanism"]); pprint.pprint(res["_opposite_sign_discriminant"]); pprint.pprint(res["_gamma_provenance"])
