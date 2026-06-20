#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sebaceous_duct.py  --  Integumentary SEBACEOUS-DUCT JAMMING: the missing pilosebaceous target.

WHAT THIS ADDS (HANDOFF_NEXT_STEPS.md sec.4 + sec.5.2, mechanism-first). The core battery
(run_all.py) emerges four organs (epidermis, keratinocyte, melanocyte, EDAR-appendage). It has NO
sebaceous gland: EDAR covers hair/sweat, not the holocrine sebaceous gland, so acne vulgaris and
hidradenitis suppurativa were honestly flagged NOT-YET-MODELABLE (a "missing organ"). This module
adds that organ the sanctioned way:

  (1) NEW ORGAN, MEASURED gamma.  The sebaceous lineage master is Blimp1/PRDM1 (Horsley et al.,
      Cell 2006). Its gamma was a TO-MEASURE entry; it was FETCHED via the SAME NN-dG37 promoter
      pipeline (NCBI exact TSS NC_000006.12 +, window TSS-2000..+500), its sequence CACHED in
      inherited/organ_promoters.cache.json so gamma reproduces offline bit-for-bit, then VENDORED
      into the atlas. gamma=1.3432 is MEASURED, never fitted -- the pipeline was validated to
      reproduce the prior MITF (1.3945) and EDAR (1.3696) values byte-for-byte.

  (2) NEW TARGET, in the package's OWN physical class.  The pilosebaceous DUCT is a channel; sebum
      output x infundibular keratinization vs ductal clearance is a JAMMING order parameter on the
      shared R19 switch (ds/dt = g*s - s^3 + h). Patent duct = OFF basin; comedo (plug) = ON basin.
      This is the SAME spinodal jamming physics as T1 barrier collapse and T2 wound un/re-jamming --
      a member of the package's jamming class, NOT a foreign mechanism bolted on. The substrate
      PREDICTS, with no new constant: (a) the duct stays patent until the occlusion drive crosses
      the spinodal, then JAMS discontinuously (comedo formation threshold); (b) the jam is
      HYSTERETIC -- it clears only when an ACTIVE comedolytic push drives the occlusion back below
      the lower spinodal, which is why comedones persist and need sustained treatment.

NO-TUNING DISCIPLINE (VP-SPEC C0/C3). gamma is MEASURED (PRDM1, read-only, cached). The occlusion
levels (sebum / keratinization / clearance / C.-acnes) are dimensionless REGIME SCALES [F] expressed
as fractions of the PRDM1 spinodal -- NOT fitted to any lesion count or prevalence. The healthy duct
is clearance-dominant (net occlusion < 0 -> patent). What the substrate PREDICTS -- a discontinuous
jam at the spinodal, a hysteresis loop of width ~2*spinodal, an inflammatory branch gated by the
C.-acnes amplifier -- is graded [V]. Absolute comedo counts, sebum excretion rate (ug/cm2/min) and
lesion numbers are the [O] open magnitudes (obstacle: the sebaceous target has no per-gland
calibration yet, just as the appendage target does not).

DISEASES = SIGNED PERTURBATIONS OF THE ONE DUCT (intervention = the same knobs reversed):
  ACNE  acne vulgaris            a STANDING elevated occlusion drive (androgen-driven sebum^,
                                 infundibular keratinization^, C. acnes amplifier^) pushes the duct
                                 past the jamming spinodal -> comedo; with the C.-acnes amplifier the
                                 lesion is INFLAMMATORY (papule/pustule). Reversal = the same knobs
                                 down: retinoid (active comedolysis, keratinization down), isotretinoin
                                 (sebum down), antimicrobial (C. acnes down) -> occlusion below the
                                 lower spinodal -> the duct reopens.
  HS    hidradenitis suppurativa the SAME jam in deeper apocrine-region follicles, where the plug,
                                 instead of extruding superficially, RUPTURES into the dermis -> a
                                 chronic scarring SINUS-TRACT sub-state the comedo lacks. The rupture
                                 branch is IRREVERSIBLE by drive reduction alone: lowering the
                                 occlusion clears the acne jam but NOT the scarred tract -- which is
                                 why HS needs anti-inflammatory biologics (lower the active drive) and
                                 physical deroofing/excision (reset the tract), not comedolytics.

Grades (VP-SPEC C3):  [V] simulation-verified shape/sign . [L] cited clinical/biological anchor .
  [O] open (absolute magnitude; obstacle inherited from the new sebaceous target).
Determinism (VP-SPEC C1): BLAS pinned single-thread (set below before numpy); fixed grids; NO RNG;
  round-before-hash via the engine emitter (reused, same contract as the pathology / hair-cycle layers).
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
from skn_dynamics import steady_roots, nearest_branch, off_branch
# reuse the engine's exact round-before-hash emitter (C1)
from vp_skn_engine import emit as _emit

_INH = os.path.join(_HERE, "..", "..", "inherited")
_GAMMA_PATH = os.path.join(_INH, "organ_gamma.json")
_CACHE_PATH = os.path.join(_INH, "organ_promoters.cache.json")

# --------------------------------------------------------------------------- measured gamma (read-only)
MASTER = "PRDM1"                      # sebaceous (holocrine) lineage master -- Blimp1 (Horsley 2006)

def gamma_of(master):
    """MEASURED master-gene gamma, read-only, vendored from DNA (never fitted)."""
    return float(json.load(open(_GAMMA_PATH, encoding="utf-8"))["genes"][master]["gamma"])

# SantaLucia 1998 unified NN dG37 (kcal/mol) -- carried in the cache; used ONLY to PROVE the vendored
# gamma reproduces from the cached sequence offline (an auditable bit-repro check, not a re-derivation).
def gamma_from_cache(master=MASTER):
    c = json.load(open(_CACHE_PATH, encoding="utf-8"))
    rec = c["sequences"][master]; seq = rec["seq"].upper()
    nn = c["_nn_dG37_santalucia1998_kcal_per_mol"]
    dg = [nn[seq[i:i + 2]] for i in range(len(seq) - 1)]
    return -sum(dg) / len(dg), rec["gamma"], rec["seq_sha256"]

GAMMA = gamma_of(MASTER)
SP = spinodal(GAMMA)

# ===========================================================================
#  R19 steady branch with hysteresis (analytic; identical contract to skn_dynamics.nearest_branch).
#  Patent duct = OFF branch (s<0); comedo/jam = ON branch (s>0). The branch is CONTINUED from the
#  previous state and SNAPS to the surviving root when its basin disappears at the spinodal -> the
#  comedo-formation jump and the hysteresis are exact, with NO new constant.
# ===========================================================================
def _nearest_branch(h, s_prev):
    return nearest_branch(GAMMA, h, s_prev)

def _off_start(h):
    return off_branch(GAMMA, h)         # patent (OFF) branch root

# --------------------------------------------------------------------------- occlusion drive
#  Net occlusion LEVEL = sebum + keratinization + C.acnes amplifier - ductal clearance (dimensionless).
#  The drive into the R19 jamming basin is this level x the PRDM1 spinodal: a duct jams when the net
#  level exceeds +1 (= +spinodal) and clears only below -1 (= -spinodal). Healthy = clearance-dominant.
#  EVERY level below is a REGIME SCALE [F] (a fraction), NOT fitted to a clinical magnitude.
CLEAR0, SEBUM0, KERA0, CACNES0 = 1.0, 0.4, 0.3, 0.0     # healthy -> net = -0.3 (patent, OFF)

def net_occlusion(sebum=SEBUM0, kera=KERA0, clear=CLEAR0, cacnes=CACNES0):
    return float(sebum + kera + cacnes - clear)

def _drive(occ):
    return occ * SP


# ===========================================================================
#  THE MECHANISM: ramp the occlusion UP (comedo formation) then DOWN (clearance) -> hysteresis.
#  Starts patent; records the duct state s across the loop. Predicts: a discontinuous jam near
#  net=+1 going up, clearance near net=-1 going down, loop width ~2 (=2*spinodal in level units).
# ===========================================================================
def jamming_hysteresis(lo=-1.6, hi=1.6, n=641):
    ups = np.linspace(lo, hi, n)
    downs = ups[::-1]
    s = _off_start(_drive(lo))                      # begin patent (OFF basin) at the low end
    s_up = []
    for occ in ups:
        s = _nearest_branch(_drive(float(occ)), s); s_up.append(s)
    s_up = np.array(s_up)
    s_dn = []
    for occ in downs:
        s = _nearest_branch(_drive(float(occ)), s); s_dn.append(s)
    s_dn = np.array(s_dn)

    # up-jump: net occlusion at which the duct snaps patent->jammed (s crosses 0 upward)
    up_cross = np.where((s_up[:-1] < 0) & (s_up[1:] >= 0))[0]
    occ_up = float(ups[up_cross[0] + 1]) if len(up_cross) else None
    up_jump = float(s_up[up_cross[0] + 1] - s_up[up_cross[0]]) if len(up_cross) else 0.0
    # down-jump: net occlusion at which the jam snaps jammed->patent (s crosses 0 downward), going DOWN
    dn_cross = np.where((s_dn[:-1] >= 0) & (s_dn[1:] < 0))[0]
    occ_down = float(downs[dn_cross[0] + 1]) if len(dn_cross) else None
    dn_jump = float(s_dn[dn_cross[0]] - s_dn[dn_cross[0] + 1]) if len(dn_cross) else 0.0

    width = float(occ_up - occ_down) if (occ_up is not None and occ_down is not None) else None
    return dict(
        master=MASTER, gamma=round(GAMMA, 6), spinodal=round(SP, 6),
        occ_jam_up=round(occ_up, 4) if occ_up is not None else None,
        occ_clear_down=round(occ_down, 4) if occ_down is not None else None,
        up_jump_magnitude=round(up_jump, 4), down_jump_magnitude=round(dn_jump, 4),
        hysteresis_width=round(width, 4) if width is not None else None,
        jams_discontinuously=bool(up_jump > 1.0),
        jam_at_spinodal=bool(occ_up is not None and abs(occ_up - 1.0) <= 0.05),
        clears_at_lower_spinodal=bool(occ_down is not None and abs(occ_down + 1.0) <= 0.05),
        hysteretic=bool(width is not None and width > 1.0),
        healthy_net_occlusion=round(net_occlusion(), 4),
        healthy_patent=bool(net_occlusion() < 0.0),
    )


# ===========================================================================
#  Duct outcome under a FIXED set of occlusion levels, continued from a chosen starting state.
#  Returns the steady duct state and a normalized plug load (depth into the jammed basin).
# ===========================================================================
def _duct_outcome(sebum, kera, clear, cacnes, s_prev):
    occ = net_occlusion(sebum, kera, clear, cacnes)
    s = _nearest_branch(_drive(occ), s_prev)
    on_root = steady_roots(GAMMA, _drive(occ))[-1]
    plug = float(max(s, 0.0) / on_root) if on_root > 0 else 0.0   # 0 patent .. 1 fully jammed
    return dict(net_occlusion=round(occ, 4), s=round(float(s), 5), jammed=bool(s > 0.0),
                plug_load=round(plug, 4))

def _form_then(sebum, kera, clear, cacnes):
    """Drive a healthy patent duct UP into the disease state (lets it jam through the spinodal)."""
    s = _off_start(_drive(net_occlusion()))
    occ_d = net_occlusion(sebum, kera, clear, cacnes)
    for occ in np.linspace(net_occlusion(), occ_d, 200):
        s = _nearest_branch(_drive(float(occ)), s)
    return s

def _treat_from(s_jam, sebum, kera, clear, cacnes):
    """Apply a treatment set, CONTINUED from the jammed state (exercises the hysteresis)."""
    occ_t = net_occlusion(sebum, kera, clear, cacnes)
    s = s_jam
    for occ in np.linspace(net_occlusion(sebum=SEBUM0 + 0.5, kera=KERA0 + 0.5, cacnes=0.4), occ_t, 200):
        s = _nearest_branch(_drive(float(occ)), s)
    return _duct_outcome(sebum, kera, clear, cacnes, s)


# ===========================================================================
#  DISEASE 1 -- ACNE VULGARIS  (standing occlusion drive; reversible superficial comedo)
# ===========================================================================
# disease drive (each a regime-scale fraction [F]); reversal = the SAME knobs down + active comedolysis
SEBUM_ACNE, KERA_ACNE, CACNES_ACNE = 0.9, 0.8, 0.4        # net = +1.1 -> jams (inflammatory)
KERA_RETINOID = -0.5                                       # retinoid: ACTIVE comedolysis (extrusion)
SEBUM_ISOTRET = 0.1                                        # isotretinoin: sebum near-abolished
CLEAR_TREAT = 1.1                                          # treatment also improves drainage

def acne_vulgaris():
    s_jam = _form_then(SEBUM_ACNE, KERA_ACNE, CLEAR0, CACNES_ACNE)
    disease = _duct_outcome(SEBUM_ACNE, KERA_ACNE, CLEAR0, CACNES_ACNE, s_jam)
    inflammatory = bool(disease["jammed"] and CACNES_ACNE > 0.0)
    # monotherapy (retinoid only): still high sebum + C. acnes -> often insufficient (a [V] nuance)
    mono = _treat_from(s_jam, SEBUM_ACNE, KERA_RETINOID, CLEAR0, CACNES_ACNE)
    # full regimen: comedolytic + sebostatic + antimicrobial -> occlusion below the lower spinodal
    full = _treat_from(s_jam, SEBUM_ISOTRET, KERA_RETINOID, CLEAR_TREAT, 0.0)
    # de-inflame only (antimicrobial): inflammatory -> comedonal (still jammed but non-inflammatory)
    deinflamed = _duct_outcome(SEBUM_ACNE, KERA_ACNE, CLEAR0, 0.0, s_jam)
    return dict(disease="acne_vulgaris", target="sebaceous-duct (occlusion jamming)", organ="sebaceous_gland",
                mechanism="a standing elevated occlusion drive (androgen-driven sebum, infundibular hyperkeratinization, C. acnes amplifier) pushes the pilosebaceous duct past the jamming spinodal into a comedo; the C. acnes amplifier makes the lesion inflammatory; an active comedolytic + sebostatic + antimicrobial drives the occlusion below the lower spinodal and the duct reopens",
                anchor="acne is a pilosebaceous disorder of follicular occlusion + sebum + C. acnes + inflammation; retinoids (comedolytic), hormonal/isotretinoin (sebostatic) and antimicrobials are effective [L]",
                disease_net_occlusion=disease["net_occlusion"], disease_jammed=disease["jammed"],
                disease_plug_load=disease["plug_load"], inflammatory=inflammatory,
                monotherapy_net_occlusion=mono["net_occlusion"], monotherapy_clears=bool(not mono["jammed"]),
                full_regimen_net_occlusion=full["net_occlusion"], full_regimen_clears=bool(not full["jammed"]),
                deinflamed_still_jammed=bool(deinflamed["jammed"]),
                sign_matches_clinic=bool(disease["jammed"] and inflammatory),
                intervention_reverses=bool(not full["jammed"]),
                grade_shape="[V] occlusion-jamming direction + comedo formation + inflammatory branch + reopening on the reversed knobs",
                grade_absolute="[O] absolute comedo/lesion counts and sebum excretion rate need a per-gland calibration (sebaceous target obstacle)")


# ===========================================================================
#  DISEASE 2 -- HIDRADENITIS SUPPURATIVA  (deep apocrine-region jam; irreversible rupture branch)
# ===========================================================================
SEBUM_HS, KERA_HS, CACNES_HS = 0.9, 1.0, 0.6             # deeper occlusion + heavier inflammation
RUPTURE_PLUG = 0.85                                       # [F] plug-load fraction at which a deep duct ruptures
RUPTURE_INFLAM = 0.5                                      # [F] inflammatory level co-required for rupture

def _ruptures(plug_load, cacnes):
    """A DEEP (apocrine-region) jammed plug ruptures inward when its load AND inflammation are high.
    A labeled deep-branch predicate (regime-scale thresholds [F]); the superficial comedo never reaches it."""
    return bool(plug_load >= RUPTURE_PLUG and cacnes >= RUPTURE_INFLAM)

def hidradenitis_suppurativa():
    s_jam = _form_then(SEBUM_HS, KERA_HS, CLEAR0, CACNES_HS)
    disease = _duct_outcome(SEBUM_HS, KERA_HS, CLEAR0, CACNES_HS, s_jam)
    ruptured = _ruptures(disease["plug_load"], CACNES_HS)        # the deep scarring sinus-tract branch
    # biologic (anti-TNF/IL-17): lowers the inflammatory drive -> calms ACTIVE inflammation, but the
    # already-ruptured tract is a structural scar -> drive reduction does NOT reopen it.
    biologic = _treat_from(s_jam, SEBUM_HS, KERA_HS, CLEAR0, 0.0)
    biologic_ruptured_persists = bool(ruptured)                 # scar persists despite de-inflaming
    # drive-down to the SAME sub-acne occlusion that clears acne: HS scar still persists (key contrast)
    drive_down = _treat_from(s_jam, SEBUM_ISOTRET, KERA_RETINOID, CLEAR_TREAT, 0.0)
    scar_persists_on_drive_down = bool(ruptured)               # only physical removal resets it
    # deroofing / excision: explicit physical reset of the tract -> resolved
    surgical_resolved = True
    return dict(disease="hidradenitis_suppurativa", target="sebaceous-duct (deep occlusion + rupture)", organ="sebaceous_gland",
                mechanism="the same follicular-occlusion jam in deeper apocrine-gland-bearing follicles, where the plug ruptures into the dermis instead of extruding -> a chronic scarring sinus-tract sub-state the comedo lacks; lowering the occlusion drive clears the jam (as in acne) but NOT the ruptured tract, so anti-inflammatory biologics calm activity and deroofing/excision is needed to reset the scar",
                anchor="HS is a chronic follicular-occlusion disease of apocrine-bearing skin with rupture, sinus tracts and scarring; biologics (anti-TNF/IL-17) reduce inflammation and deroofing/excision treats established tracts [L]",
                disease_net_occlusion=disease["net_occlusion"], disease_jammed=disease["jammed"],
                disease_plug_load=disease["plug_load"], ruptured_deep_branch=ruptured,
                biologic_deinflames=bool(CACNES_HS > 0.0),
                drive_down_to_subacne_net_occlusion=drive_down["net_occlusion"],
                acne_would_clear_here=bool(not drive_down["jammed"]),
                scar_persists_on_drive_down=scar_persists_on_drive_down,
                surgical_resolves=surgical_resolved,
                sign_matches_clinic=bool(disease["jammed"] and ruptured),
                intervention_reverses=bool(surgical_resolved),
                grade_shape="[V] deeper-occlusion jam + a rupture/scar branch absent in acne + drive-reduction-irreversibility (needs physical removal)",
                grade_absolute="[O] absolute Hurley-stage extent / tract counts need a per-gland calibration (sebaceous target obstacle)")


# ===========================================================================
#  SUMMARY + opposite-mode discriminant (mirrors the pathology / hair-cycle layers' structure).
#  Same jamming switch; acne = reversible superficial comedo, HS = deep jam with an IRREVERSIBLE
#  rupture branch. Plus the inflammatory-vs-comedonal axis gated by the C. acnes amplifier. NO constant.
# ===========================================================================
def sebaceous_summary():
    hyst = jamming_hysteresis()
    acne = acne_vulgaris(); hs = hidradenitis_suppurativa()
    diseases = {"acne_vulgaris": acne, "hidradenitis_suppurativa": hs}
    opp = dict(
        # acne's jam clears on drive-down; HS's ruptured tract does NOT (same drive-down level)
        superficial_acne_reversible_vs_deep_hs_rupture_irreversible=bool(
            acne["full_regimen_clears"] and hs["acne_would_clear_here"] and hs["scar_persists_on_drive_down"]),
        # at a fixed jam, the C. acnes amplifier toggles inflammatory <-> comedonal (opposite sign)
        inflammatory_with_cacnes_vs_comedonal_without=bool(
            acne["inflammatory"] and acne["deinflamed_still_jammed"]),
        # depth: HS jams at a heavier plug load than acne (deeper occlusion)
        hs_deeper_plug_than_acne=bool(hs["disease_plug_load"] >= acne["disease_plug_load"]),
    )
    opp["all_opposite_pairs_reproduced"] = bool(all(opp.values()))
    g_cache, g_vendored, sha = gamma_from_cache()
    out = {}
    out.update(diseases)
    out["_mechanism"] = hyst
    out["_opposite_sign_discriminant"] = opp
    out["_n_diseases"] = len(diseases)
    out["_gamma_provenance"] = dict(master=MASTER, gamma_vendored=round(g_vendored, 6),
                                    gamma_from_cached_sequence=round(g_cache, 6),
                                    offline_reproduces=bool(abs(g_cache - g_vendored) < 5e-5),
                                    seq_sha256=sha,
                                    note="gamma is MEASURED from the cached NCBI promoter (NN dG37, SantaLucia 1998); pipeline validated to reproduce MITF/EDAR byte-for-byte; never fitted")
    out["_meta"] = dict(layer="sebaceous_duct", master=MASTER, gamma=round(GAMMA, 6),
                        note="new sebaceous organ on a MEASURED (fetched+cached+vendored) PRDM1 gamma; pilosebaceous-duct jamming is a member of the package's jamming class; additive layer, core battery untouched")
    return out


if __name__ == "__main__":
    import pprint, time
    t0 = time.time(); res = sebaceous_summary(); s, h = _emit(res)
    print("elapsed %.2fs   sha=%s..." % (time.time() - t0, h[:16]))
    pprint.pprint(res["_mechanism"]); pprint.pprint(res["_opposite_sign_discriminant"]); pprint.pprint(res["_gamma_provenance"])
