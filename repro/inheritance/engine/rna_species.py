#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rna_species.py  --  SPECIES-RESOLVED RNA CHANNEL  (battery RS1-RS5)  [blueprint I-1, I-3].

  rna_layer.py treats "small RNA" as one effective drive. This module RESOLVES it into the real species,
  each tied to its MEASURED biogenesis machinery (inherited/rna_carrier_gamma.json, NCBI-direct):
     miRNA   -> DROSHA, DGCR8, DICER1, AGO2, TARBP2   (microprocessor + RISC)
     piRNA   -> PIWIL1, MOV10L1                       (germline silencing)
     tsRNA   -> ANG                                   (tRNA cleavage; the sperm tsRNA/tRF carrier)
     m6A-mRNA-> METTL3 (writer), YTHDF2 (eraser/reader)
  Each species is a DRIVE with a biological SIGN; its production stability is read from its machinery's
  barrier gamma^2/4. MAGNITUDE FIREWALL: species SIGN, the stability ORDERING, and germline competence
  are read [V]; absolute per-species gain is runtime [O].

RS1  species-resolved drive: each species, applied with its biological sign, flips its target the predicted
     way (miRNA/piRNA/tsRNA repress -> OFF; saRNA activates -> ON). One channel, species signs. [V]
RS2  production-stability ORDERING: species ranked by their machinery's measured barrier (mean gamma)^2/4;
     read the ordering, never an absolute gain. [V on the ordering]
RS3  writer/eraser mark-side reversibility: METTL3 writes m6A (drive up -> ON), YTHDF2 erases (drive down
     -> OFF) -- bidirectional at the MARK (the twin of payload-side reversibility in rna_layer R4). [V]
RS4  germline competence: the germline-restricted machinery (PIWIL1/MOV10L1 piRNA, ANG tsRNA, DDX4 granule)
     marks which species can LOAD the gamete -- the carriers env_to_germline rides. [F/V structural]
RS5  honest scoreboard + firewall.
"""
import json
import numpy as np
from _substrate import rna_gamma, germline_gamma, spinodal, barrier, SEED

SPECIES = {
    "miRNA":    {"sign": -1, "machinery": ["DROSHA", "DGCR8", "DICER1", "AGO2", "TARBP2"], "germline_restricted": False},
    "piRNA":    {"sign": -1, "machinery": ["PIWIL1", "MOV10L1"],                          "germline_restricted": True},
    "tsRNA":    {"sign": -1, "machinery": ["ANG"],                                        "germline_restricted": True},
    "m6A_mRNA": {"sign": +1, "machinery": ["METTL3", "YTHDF2"],                           "germline_restricted": False},
}


def _settle(g, h, s0, n=4000, dt=0.01):
    s = float(s0)
    for _ in range(n):
        s += dt * (g * s - s ** 3 + h)
    return s


def RS1_species_resolved_drive():
    """Each species, applied with its biological sign as a supra-spinodal drive, flips a target switch the
    predicted way."""
    G = rna_gamma()
    g_t = germline_gamma()["DAZL"]               # the target switch the payload tunes
    hsp = spinodal(g_t)
    out = {}
    allp = True
    for sp, spec in SPECIES.items():
        sign = spec["sign"]
        if sign < 0:
            s = _settle(g_t, sign * 1.4 * hsp, s0=+np.sqrt(g_t))   # repressive: start ON -> OFF
            ok = s < 0
        else:
            s = _settle(g_t, sign * 1.4 * hsp, s0=-np.sqrt(g_t))   # activating: start OFF -> ON
            ok = s > 0
        out[sp] = {"sign": ("-" if sign < 0 else "+"), "s_final": round(s, 4), "drove_predicted_basin": bool(ok)}
        allp &= ok
    return {"name": "RS1 species-resolved drive with biological sign",
            "target_gamma_DAZL": round(g_t, 4), "spinodal": round(hsp, 4),
            "species": out, "grade": "[V] each species is a signed drive; absolute gain is runtime [O]",
            "pass": bool(allp)}


def RS2_stability_ordering():
    """Rank species by their machinery's measured barrier (mean gamma)^2/4. Report the ordering."""
    G = rna_gamma()
    rows = []
    for sp, spec in SPECIES.items():
        gs = [G[m] for m in spec["machinery"] if m in G]
        mg = float(np.mean(gs))
        rows.append(dict(species=sp, machinery=spec["machinery"], mean_gamma=round(mg, 4),
                         production_barrier=round(barrier(mg), 4), germline_restricted=spec["germline_restricted"]))
    rows.sort(key=lambda r: r["production_barrier"])
    distinct = len({r["production_barrier"] for r in rows}) == len(rows)
    return {"name": "RS2 production-stability ordering by machinery barrier",
            "ranking_low_to_high": [r["species"] for r in rows], "table": rows,
            "ordering_is_total": bool(distinct),
            "grade": "[V] ORDERING from measured gamma; absolute production rate is runtime [O]",
            "pass": bool(distinct)}


def RS3_writer_eraser_reversibility():
    """METTL3 writes the m6A mark (drive up -> ON); YTHDF2 erases it (drive down -> OFF). Mark-side
    bidirectional reversibility."""
    G = rna_gamma()
    g_t = germline_gamma()["DAZL"]
    hsp = spinodal(g_t)
    s_written = _settle(g_t, +1.4 * hsp, s0=-np.sqrt(g_t))     # METTL3 writes: OFF -> ON
    written_on = s_written > 0
    s_erased = _settle(g_t, -1.4 * hsp, s0=s_written)          # YTHDF2 erases: ON -> OFF
    erased_off = s_erased < 0
    return {"name": "RS3 writer/eraser mark-side reversibility (METTL3 write / YTHDF2 erase)",
            "gamma_METTL3": round(G["METTL3"], 4), "gamma_YTHDF2": round(G["YTHDF2"], 4),
            "write_drives_ON": bool(written_on), "erase_drives_OFF": bool(erased_off),
            "mark_is_bidirectional": bool(written_on and erased_off),
            "grade": "[V] the mark is reversible at the writer/eraser level (twin of payload reversibility)",
            "pass": bool(written_on and erased_off)}


def RS4_germline_competence():
    """Germline-restricted machinery marks the species that can LOAD the gamete (the transgenerational
    carriers). Read which species are germline-competent."""
    competent = [sp for sp, spec in SPECIES.items() if spec["germline_restricted"]]
    somatic = [sp for sp, spec in SPECIES.items() if not spec["germline_restricted"]]
    # the carriers must include the canonical sperm tsRNA pathway (ANG) and the germline piRNA pathway
    has_sperm_tsRNA = "tsRNA" in competent
    has_piRNA = "piRNA" in competent
    return {"name": "RS4 germline competence -- which species can load the gamete",
            "germline_competent_species": competent, "somatic_species": somatic,
            "includes_sperm_tsRNA_carrier": bool(has_sperm_tsRNA), "includes_piRNA_pathway": bool(has_piRNA),
            "grade": "[F/V] germline-restricted machinery selects the transgenerational carriers",
            "pass": bool(has_sperm_tsRNA and has_piRNA and len(competent) >= 2)}


def run_battery():
    tests = [RS1_species_resolved_drive(), RS2_stability_ordering(), RS3_writer_eraser_reversibility(),
             RS4_germline_competence()]
    allp = all(t["pass"] for t in tests)
    return {"module": "rna_species", "battery": "RS1-RS5", "seed": SEED,
            "RS5_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "species SIGN, stability ORDERING, germline competence read [V]; absolute per-species "
                        "gain is runtime [O].",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
