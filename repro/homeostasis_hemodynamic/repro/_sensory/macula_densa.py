#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_densa.py  --  the SENSORY CELL beneath the slow loop (the fundamental, not the visible mechanism).

The kidney_volume_integrator node (SIX2, the slow integrator of RP3) does not sense pressure directly --
it senses SALT. The macula densa is a plaque of ~15-20 modified thick-ascending-limb cells at the
juxtaglomerular apparatus that reads luminal NaCl via the apical Na-K-2Cl cotransporter NKCC2 and turns
it into two outputs:
  (1) tubuloglomerular feedback (TGF): HIGH luminal NaCl -> afferent arteriole constriction -> GFR down
      (a fast, single-nephron autoregulator), and
  (2) renin control: LOW luminal NaCl -> renin release up -> angiotensin/aldosterone (RAAS) up ->
      Na/volume retention -> pressure up  (the slow pressure/volume reference of RP3/RP4).

So the macula densa is the chemosensory front-end that sets the RENAL REFERENCE the integral controller
defends. This module emerges the two monotone transduction relations (renin = decreasing in [NaCl];
TGF constriction = increasing in [NaCl]) deterministically. It connects directly to therapy: SGLT2
inhibitors raise NaCl delivery to the macula densa, restoring TGF and damping glomerular hyperfiltration
-- a leading mechanistic account of their renal/cardiovascular benefit (one of the HF "four pillars").

GRADES (C3): the monotone NKCC2 transduction SHAPES = [V]; the JGA anatomy + NKCC2 identity + the
SGLT2i->TGF link = [L]; ABSOLUTE renin secretion rates / GFR values = [O] (calibration).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import math, json

NACL_MIN = 10.0     # luminal [NaCl] window at the macula densa (mM, illustrative) [L]
NACL_MAX = 60.0
NACL_OP  = 30.0     # operating midpoint (steepest transduction)


def nkcc2_uptake(nacl_mM):
    """NKCC2 cotransporter flux (saturating in luminal [NaCl]) -- the sensed variable."""
    return nacl_mM / (nacl_mM + 0.5 * NACL_OP)          # Michaelis-like saturation


def renin_release(nacl_mM):
    """Renin is INVERSELY related to luminal NaCl (low salt -> high renin -> RAAS up)."""
    u = nkcc2_uptake(nacl_mM)
    return 1.0 - u                                       # decreasing in [NaCl]


def tgf_constriction(nacl_mM):
    """Tubuloglomerular feedback: afferent constriction INCREASES with luminal NaCl."""
    return nkcc2_uptake(nacl_mM)                          # increasing in [NaCl]


def transduction_curves():
    xs = [round(NACL_MIN + i * (NACL_MAX - NACL_MIN) / 10.0, 3) for i in range(11)]
    renin = [round(renin_release(x), 6) for x in xs]
    tgf = [round(tgf_constriction(x), 6) for x in xs]
    renin_decreasing = all(renin[i + 1] <= renin[i] + 1e-9 for i in range(len(renin) - 1))
    tgf_increasing = all(tgf[i + 1] >= tgf[i] - 1e-9 for i in range(len(tgf) - 1))
    return dict(nacl_mM=xs, renin_arb=renin, tgf_constriction_arb=tgf,
                renin_decreasing_in_nacl=bool(renin_decreasing),
                tgf_increasing_in_nacl=bool(tgf_increasing))


def sglt2i_effect():
    """SGLT2 inhibition blocks proximal Na/glucose reabsorption -> MORE NaCl reaches the macula densa
    -> stronger TGF / restored afferent tone / less hyperfiltration. Shown as a shift of the sensed
    point upward in [NaCl]."""
    base = NACL_OP
    on_drug = NACL_OP * 1.6                               # more distal NaCl delivery
    return dict(nacl_baseline_mM=round(base, 3), nacl_on_sglt2i_mM=round(on_drug, 3),
                tgf_baseline=round(tgf_constriction(base), 6), tgf_on_sglt2i=round(tgf_constriction(on_drug), 6),
                tgf_restored=bool(tgf_constriction(on_drug) > tgf_constriction(base)),
                link="raised macula-densa NaCl delivery restores TGF and damps hyperfiltration -- a leading account of SGLT2i renal/CV benefit [L]")


def status():
    curves = transduction_curves()
    return dict(
        sensory_cell="macula densa (JGA plaque of ~15-20 modified thick-ascending-limb cells)",
        transducer="apical Na-K-2Cl cotransporter NKCC2 (furosemide-sensitive)",
        sets="the RENAL reference the integral controller defends (RP3/RP4) via renin/RAAS + TGF",
        curves=curves,
        both_transductions_monotone=bool(curves["renin_decreasing_in_nacl"] and curves["tgf_increasing_in_nacl"]),
        sglt2i=sglt2i_effect(),
        shape_grade="[V]", identity_grade="[L]", absolute_grade="[O]",
        anchor="macula-densa NaCl sensing via NKCC2 -> TGF + renin (JASN/AJP reviews); SGLT2i act via raised MD NaCl delivery / TGF")


if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
