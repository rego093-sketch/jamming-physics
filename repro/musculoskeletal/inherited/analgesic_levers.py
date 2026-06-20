#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analgesic_levers.py  --  INHERITED three-lever non-opioid analgesic THRESHOLD LOGIC primitive.

PROVENANCE (inherited, not re-derived here):
    The three-lever organising principle (L1 / L2 / L3) is the core technique of the VP NON-OPIOID
    ANALGESIC volume -- *analgesic_threshold_logic* v2.0, concept DOI 10.5281/zenodo.20733420 (Young Jae Lee,
    CC BY 4.0). That volume locks the 27-target non-opioid analgesic atlas; the technique it locks is reused
    here VERBATIM as a kernel, exactly as `inherited/vp_substrate.py` vendors the neuro R19/FHN primitives.
    This file adds NO new physics and NO new constant: it is the analgesic volume's threshold logic expressed
    on the SAME R19 substrate this package already uses (spinodal / barrier / settle from vp_substrate).

THE ONE IDEA (threshold logic):
    Nociception is a THRESHOLD-CROSSING process. A nociceptor terminal is an excitable R19/FHN element with an
    escape barrier dV = barrier(gamma) = gamma^2/4. A noxious DRIVE h pushes the membrane state toward the
    saddle; when h erodes the effective barrier to zero (h past the spinodal drive) the terminal fires
    continuously. Between those limits the firing (threshold-crossing) RATE follows a Kramers-type law
    rate ~ exp(-dV_eff / D). The perceived nociceptive SIGNAL is a downstream GAIN g times that rate:

        dV_eff(h, dV_L1) = max(0, barrier(gamma) + dV_L1 - kappa * h)      # drive erodes the barrier; L1 adds back
        rate(h, dV_L1)   = exp(-dV_eff / D)                                # Kramers crossing rate (>0)
        signal(g, rate)  = g * rate                                        # post-crossing amplification

THE THREE LEVERS (every non-opioid analgesic acts on exactly one; opioids act on a 4th, descending/mu lever
that is OUT of this NON-opioid logic):
    * L1  RAISE THE PERIPHERAL THRESHOLD/BARRIER   dV_L1: 0 -> dV_max   => dV_eff up   => rate DOWN.
          real anchors [L]: local anaesthetics / Na_v blockers (lidocaine 5% patch), topical agents, membrane
          stabilisers. STRUCTURE-DECOUPLED: it silences the terminal without changing the tissue lesion.
    * L2  LOWER THE DRIVE   h: h0 -> h0*(1 - frac)   => dV_eff up   => rate DOWN.
          real anchors [L]: NSAIDs / coxibs (remove the prostaglandin sensitising drive), and -- the
          musculoskeletal special case -- MECHANICAL UNLOADING, which lowers the very same load knob the
          disease kernel perturbs. STRUCTURE-COUPLED: lowering h both quietens the terminal AND arrests the
          mechanical lesion (the convergence this volume documents).
    * L3  REDUCE THE GAIN   g: 1 -> 1 - frac   => signal DOWN (rate unchanged).
          real anchors [L]: gabapentinoids, SNRIs (duloxetine), descending modulation. This is CENTRAL gain;
          it is OWNED BY neuro / mind and reached only as a NAMED SEAM (SSOT) -- never re-emerged here.

NO-TUNING (identical discipline to the disease and treatment batteries):
    A lever is pulled along an intensity x in [0,1]. PASS = the crossing-rate (L1/L2) or signal (L3) moves
    MONOTONICALLY DOWN. We never tune x to a clinical pain score; the DIRECTION (does pulling the lever lower
    the nociceptive crossing rate?) is the result, and the real agent is the cited [L] anchor for WHICH lever
    it pulls -- never a tuned efficacy number. No absolute pain units are emitted (all rates are normalised to
    the untreated state).

Grades (VP-SPEC C3):  [F] forced  ./  [V] simulation-verified  ./  [L] cited agent/lever anchor  ./  [O] open.
"""
import os, sys, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
_HERE = os.path.dirname(__file__)
sys.path.insert(0, _HERE)
from vp_substrate import spinodal, barrier            # vendored R19 primitives (single source, unchanged)

# Provenance constant (cited, not a tuned parameter).
ANALGESIC_SOURCE_DOI = "10.5281/zenodo.20733420"       # analgesic_threshold_logic v2.0 (three-lever technique)

# Kramers proxy temperature: a FIXED scale, NOT fitted (it only sets the unit of the exponent; every result is
# normalised to the untreated rate so its value cannot change any DIRECTION verdict). Chosen = 1.0 (natural).
_D = 1.0
_KAPPA = 1.0                                           # drive->barrier-erosion coupling (natural units, fixed)


def crossing_rate(gamma, h, dV_L1=0.0, D=_D, kappa=_KAPPA):
    """Kramers-type nociceptor firing (threshold-crossing) rate under noxious drive h with an effective
    barrier (base R19 barrier + L1 addition - drive erosion). Always > 0; rises as h rises, falls as dV_L1
    rises. Grounded on the SAME barrier(gamma) the rest of the package uses (no new physics)."""
    dV_eff = max(0.0, barrier(gamma) + dV_L1 - kappa * h)
    return math.exp(-dV_eff / D)


def signal(gain, rate):
    """Perceived nociceptive signal = downstream gain x crossing rate (the L3 lever scales `gain`)."""
    return gain * rate


def _intensities(n=6):
    return [round(i / (n - 1), 3) for i in range(n)]    # 0.0 .. 1.0


def _mono_down(seq, tol=1e-12):
    return all(seq[i] >= seq[i + 1] - tol for i in range(len(seq) - 1))


# ----------------------------------------------------------------------------------------------------------
#  The three lever operators. Each returns a sweep + a DIRECTION verdict (No-Tuning). `h0` is the UNTREATED
#  noxious drive -- in this package it is supplied BY a disease kernel's mechanical state (structure coupling).
# ----------------------------------------------------------------------------------------------------------
def lever_L1_raise_threshold(gamma, h0, dV_max=None, n=6, kappa=_KAPPA):
    """L1: raise the peripheral barrier dV_L1 from 0 to dV_max. rate must fall monotonically. STRUCTURE-DECOUPLED
    (the tissue load h0 is untouched). dV_max defaults to kappa*h0 -- the magnitude of the noxious drive the lever
    must counter, i.e. a FULL peripheral conduction block restores the resting firing threshold against the present
    drive (rate -> the unstimulated exp(-barrier/D)). This is NOT tuned to a pain score: it is fixed by the drive
    the lever faces, so when a severe load has fully eroded the barrier (rate saturated at 1) the lever can still
    climb back -- a small dose dents a maximally-firing terminal little (honest), a full block restores rest."""
    dV_max = kappa * h0 if dV_max is None else dV_max
    sweep = [{"intensity": x, "dV_L1": round(x * dV_max, 5),
              "rate": round(crossing_rate(gamma, h0, dV_L1=x * dV_max), 6)} for x in _intensities(n)]
    rates = [r["rate"] for r in sweep]
    return {"lever": "L1", "axis": "peripheral threshold / barrier (dV up)", "structure_coupled": False,
            "sweep": sweep, "rate_monotone_down": _mono_down(rates),
            "lowers_nociception": rates[-1] < rates[0] - 1e-9}


def lever_L2_lower_drive(gamma, h0, frac=0.8, n=6):
    """L2: lower the noxious DRIVE h from h0 to h0*(1-frac). rate must fall monotonically. STRUCTURE-COUPLED:
    in this package h0 IS the mechanical load on the failing structure, so lowering it is the same operation
    that arrests the lesion (documented convergence with the mirror treatment)."""
    sweep = [{"intensity": x, "drive_h": round(h0 * (1.0 - frac * x), 6),
              "rate": round(crossing_rate(gamma, h0 * (1.0 - frac * x)), 6)} for x in _intensities(n)]
    rates = [r["rate"] for r in sweep]
    return {"lever": "L2", "axis": "noxious drive (mechanical/inflammatory input, h down)", "structure_coupled": True,
            "sweep": sweep, "rate_monotone_down": _mono_down(rates),
            "lowers_nociception": rates[-1] < rates[0] - 1e-9}


def lever_L3_reduce_gain(gamma, h0, frac=0.8, n=6, owner="neuro/mind (central gain seam -- SSOT, not re-emerged)"):
    """L3: reduce downstream GAIN g from 1 to 1-frac (rate unchanged). signal must fall monotonically. This is
    CENTRAL gain: it is OWNED BY a sibling volume and reached only as a NAMED SEAM. We compute the DIRECTION on
    the shared substrate to show the lever exists, but the mechanism is the sibling's (graded [O]/seam here)."""
    rate0 = crossing_rate(gamma, h0)
    sweep = [{"intensity": x, "gain": round(1.0 - frac * x, 4),
              "signal": round(signal(1.0 - frac * x, rate0), 6)} for x in _intensities(n)]
    sigs = [r["signal"] for r in sweep]
    return {"lever": "L3", "axis": "central gain (post-crossing amplification, g down)", "structure_coupled": False,
            "owner_seam": owner, "sweep": sweep, "signal_monotone_down": _mono_down(sigs),
            "lowers_nociception": sigs[-1] < sigs[0] - 1e-9}


def three_lever_map(gamma, h0, frac_L2=0.8, frac_L3=0.8):
    """Run all three levers for one painful target and return the standard lever-map block. The in-scope levers
    (L1, L2) are DIRECTION-graded here; L3 is reported as a seam-out (owned by neuro/mind)."""
    L1 = lever_L1_raise_threshold(gamma, h0)
    L2 = lever_L2_lower_drive(gamma, h0, frac=frac_L2)
    L3 = lever_L3_reduce_gain(gamma, h0, frac=frac_L3)
    return {"gamma": round(gamma, 4), "untreated_drive_h0": round(h0, 6),
            "untreated_rate": round(crossing_rate(gamma, h0), 6),
            "L1": L1, "L2": L2, "L3": L3,
            "in_scope_levers_direction_ok": bool(L1["lowers_nociception"] and L1["rate_monotone_down"]
                                                 and L2["lowers_nociception"] and L2["rate_monotone_down"]),
            "source_doi": ANALGESIC_SOURCE_DOI}


if __name__ == "__main__":
    import json
    # self-test on bone's RUNX2 gamma with a representative supra-threshold drive
    g = 1.2414
    demo = three_lever_map(g, h0=1.2 * spinodal(g))
    print(json.dumps(demo, ensure_ascii=False, indent=2))
    print("\nin-scope (L1,L2) direction ok:", demo["in_scope_levers_direction_ok"])
