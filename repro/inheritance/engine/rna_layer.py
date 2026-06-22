#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rna_layer.py  --  THE RNA WRITABLE CHANNEL  (battery R1-R5).

CENTRAL NEW OBJECT OF THIS KIT.
  The parent DNA framework reads a fixed SET (gamma + R19 switches) and lets the ENVIRONMENT write a
  reversible DRIVE h on those switches. The DNA paper exposed ONE writable channel: methylation (the
  CpG handles). This module adds the SECOND: SMALL RNA. A small-RNA payload (miRNA / siRNA / piRNA /
  tsRNA-tRF) sets h on a target switch post-transcriptionally WITHOUT changing gamma -- it is a drive,
  never an edit. This is the molecular carrier that the transgenerational battery (env_to_germline.py)
  rides into the germline.

  All results are read on the SAME R19 substrate (ds/dt = gamma*s - s^3 + h) at the MEASURED promoter
  gamma of the RNA-biogenesis machinery (inherited/rna_carrier_gamma.json, NCBI-direct). MAGNITUDE
  FIREWALL: we read WHICH switch and the SIGN of the drive, and we verify reversibility; absolute
  payload-to-phenotype dose is runtime [O].

R1  RNA as a reversible h-write: a payload tunes the target switch's effective drive; the switch flips
    only past its spinodal; gamma is unchanged. [V]
R2  Two signs, one channel: siRNA/miRNA = a NEGATIVE drive (knockdown -> OFF); saRNA = a POSITIVE drive
    (activation -> ON). One mechanism, two signs (like methylation vs temperature in the DNA paper). [V]
R3  Carrier atlas: the RNA machinery's promoter gamma is MEASURED (NCBI), anchor-gated (SOX9). [V on the measurement]
R4  Reversibility: remove the payload and the switch RELAXES BACK to the environmental basin -- unlike a
    genome edit. This is why RNA therapeutics are tunable/reversible. [V]
R5  honest scoreboard + firewall.
"""
import numpy as np
from _substrate import rna_gamma, rna_roles, spinodal, barrier, sdot, SEED


def _settle(g, h, s0, n=4000, dt=0.01):
    s = float(s0)
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s


def R1_reversible_write():
    """A payload sets h_target = h_env - k*[RNA] (knockdown sign). A switch held ON by the environment
    flips only when the payload drives it past the FAR spinodal (-spinodal) -- hysteresis. gamma is
    untouched throughout (read-only SET)."""
    g = rna_gamma()["DICER1"]            # a measured machinery switch
    hsp = spinodal(g)
    h_env = +0.9 * hsp                   # environment holds it ON, sub-spinodal
    k = 1.0
    doses = np.linspace(0.0, 3.0 * hsp, 31)
    h_at_flip = None
    for d in doses:
        h = h_env - k * d                # RNA pushes the drive down
        s = _settle(g, h, s0=+np.sqrt(g))
        if s < 0 and h_at_flip is None:
            h_at_flip = float(h)         # the drive value at which the held-ON basin disappeared
    gamma_unchanged = (rna_gamma()["DICER1"] == g)   # SET never edited
    # the held-ON switch flips only at the opposite saddle-node h = -spinodal (memory / hysteresis)
    crossed_far_spinodal = h_at_flip is not None and abs(h_at_flip + hsp) < 0.25 * hsp
    return {
        "name": "R1 RNA as a reversible drive-write (gamma unchanged)",
        "gamma_DICER1": round(g, 4), "spinodal": round(hsp, 4),
        "h_at_flip": None if h_at_flip is None else round(h_at_flip, 4),
        "flip_at_far_spinodal_hysteretic": bool(crossed_far_spinodal),
        "gamma_unchanged_SET_readonly": bool(gamma_unchanged),
        "grade": "[V] held switch flips only past the opposite spinodal (memory); gamma never edited",
        "pass": bool(crossed_far_spinodal and gamma_unchanged),
    }


def R2_two_signs():
    """siRNA/miRNA = negative drive (-> OFF); saRNA = positive drive (-> ON). One channel, two signs."""
    g = rna_gamma()["AGO2"]
    hsp = spinodal(g)
    # start at the ridge (h_env = 0, bistable). A supra-spinodal payload of each sign parks the basin.
    s_neg = _settle(g, -1.3 * hsp, s0=+np.sqrt(g))   # siRNA: knockdown
    s_pos = _settle(g, +1.3 * hsp, s0=-np.sqrt(g))   # saRNA: activation
    neg_off = s_neg < 0
    pos_on  = s_pos > 0
    return {
        "name": "R2 two signs on one channel (siRNA-OFF vs saRNA-ON)",
        "gamma_AGO2": round(g, 4), "spinodal": round(hsp, 4),
        "siRNA_drives_OFF": bool(neg_off), "s_after_siRNA": round(s_neg, 4),
        "saRNA_drives_ON": bool(pos_on),  "s_after_saRNA": round(s_pos, 4),
        "grade": "[V] one writable channel carries a sign; magnitude is runtime [O]",
        "pass": bool(neg_off and pos_on),
    }


def R3_carrier_atlas():
    """The RNA machinery promoter gamma is MEASURED (NCBI), anchor-gated. Report the atlas + bistability."""
    G = rna_gamma()
    roles = rna_roles()
    rows = []
    all_bistable = True
    for k in sorted(G, key=lambda x: G[x]):
        g = G[k]
        b = g > 0  # R19 bistable (can-fire) for gamma>0
        all_bistable &= b
        rows.append(dict(gene=k, gamma=round(g, 4), spinodal=round(spinodal(g), 4),
                         barrier=round(barrier(g), 4), bistable=b, role=roles[k]))
    return {
        "name": "R3 measured RNA-carrier gamma atlas (NCBI-direct, anchor-gated)",
        "n_genes": len(rows), "gamma_min": round(min(G.values()), 4), "gamma_max": round(max(G.values()), 4),
        "all_R19_bistable": bool(all_bistable),
        "atlas": rows,
        "grade": "[V] measured promoter gamma; pipeline validated by SOX9 anchor reproduction",
        "pass": bool(all_bistable and len(rows) >= 10),
    }


def R4_reversibility():
    """With the environment's own drive supra-spinodal (it actively wants ON), a payload can transiently
    override it, but clearance restores the environment-set state. RNA != genome edit."""
    g = rna_gamma()["TARBP2"]
    hsp = spinodal(g)
    h_env = +1.3 * hsp                    # environment SUPRA-spinodally wants ON
    # 1) payload ON (drives net past the far spinodal) -> forced OFF
    s_payload = _settle(g, h_env - 2.6 * hsp, s0=+np.sqrt(g))
    forced_off = s_payload < 0
    # 2) payload cleared (h back to h_env, supra-spinodal ON): the OFF basin is gone -> returns ON
    s_cleared = _settle(g, h_env, s0=s_payload)
    returned_on = s_cleared > 0
    return {
        "name": "R4 reversibility -- payload cleared, basin returns (vs irreversible edit)",
        "gamma_TARBP2": round(g, 4), "spinodal": round(hsp, 4),
        "forced_OFF_under_payload": bool(forced_off), "s_under_payload": round(s_payload, 4),
        "returns_ON_after_clearance": bool(returned_on), "s_after_clearance": round(s_cleared, 4),
        "grade": "[V] RNA drive is reversible; a SET-edit (gene_therapy Lever A) is not",
        "pass": bool(forced_off and returned_on),
    }


def run_battery():
    tests = [R1_reversible_write(), R2_two_signs(), R3_carrier_atlas(), R4_reversibility()]
    allp = all(t["pass"] for t in tests)
    return {"module": "rna_layer", "battery": "R1-R5",
            "R5_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "WHICH switch + SIGN of drive read [V]; absolute payload->phenotype dose is runtime [O]; "
                        "clinical RNA dosing belongs to clinicians.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    import json
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
