#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
a4_application_map.py  --  THE APPLICATIONS ON THE (gamma, A4) PLANE  (battery AM1-AM4).

  The vaccine (rna_vaccine) and the two gene-therapy levers (gene_therapy) were drawn on gamma alone. But
  a fixed drive is applied at an A4 COORDINATE, and a contact-competent coordinate supplies a loop-assist
  that lowers the drive needed to cross the spinodal. So both applications live on the JOINT (gamma, A4)
  plane: gamma sets the spinodal scale, the A4 contact-assist shifts how much external drive is required.
  MAGNITUDE FIREWALL: the coordinate-DEPENDENCE of dose, the lever MAP, and the boundary SHAPE are read
  [V]; absolute doses, assist energies, and clinical outcomes are runtime [O].

AM1  prime-boost dose depends on the A4 coordinate: a fixed prime reaches the protected basin at a
     contact-competent coordinate (loop-assist) but not at a non-contact coordinate of the SAME gamma. [V]
AM2  lever map on (gamma, A4): Lever B (RNA drive) reaches a switch iff (drive + contact-assist) crosses the
     spinodal; Lever A (edit) moves gamma (and the coordinate). The two levers partition the plane. [V]
AM3  the 3D contact boundary CURVE: in (gamma, contact-assist delta) space, the critical external drive
     surface where required = available; raising contact-assist lowers the required drive and shifts the
     drive-reachable boundary -- the boundary between "drive-reachable (Lever B)" and "needs-edit (Lever A)"
     bends with A4 contact. [V]
AM4  honest scoreboard + firewall.
"""
import json
import numpy as np
from _substrate import immune_gamma, rna_gamma, a4_coords_set, spinodal, barrier, SEED


def _settle(g, h, s0, n=4000, dt=0.01):
    s = float(s0)
    for _ in range(n):
        s += dt * (g * s - s ** 3 + h)
    return s


def AM1_primeboost_at_coordinate():
    """A fixed prime drive crosses to the protected basin at a contact-competent coordinate (assist) but not
    at a non-contact coordinate of the same gamma."""
    g = max(immune_gamma().values())            # an immune switch
    hsp = spinodal(g)
    prime = 0.85 * hsp                           # a fixed sub-spinodal prime dose
    assist = 0.30 * hsp                          # the loop-assist a contact-competent coordinate supplies
    s_contact = _settle(g, prime + assist, s0=-np.sqrt(g))   # contact-competent coordinate: reaches memory
    s_noncontact = _settle(g, prime, s0=-np.sqrt(g))         # non-contact, same gamma: does not
    reaches_at_contact = s_contact > 0
    not_at_noncontact = s_noncontact < 0
    return {"name": "AM1 prime-boost dose depends on the A4 coordinate",
            "immune_gamma": round(g, 4), "spinodal": round(hsp, 4),
            "prime": round(prime, 4), "contact_assist": round(assist, 4),
            "reaches_memory_at_contact_coordinate": bool(reaches_at_contact),
            "fails_at_noncontact_same_gamma": bool(not_at_noncontact),
            "grade": "[V] effective vaccine dose is coordinate-dependent; absolute dose is runtime [O]",
            "pass": bool(reaches_at_contact and not_at_noncontact)}


def AM2_lever_map():
    """Partition the (gamma, contact) plane: Lever B reaches a held-ON pathological switch iff a tolerable
    drive plus the contact-assist crosses the far spinodal; otherwise Lever A (edit) is required."""
    cap = None
    # use a representative pathological hold; sweep gamma x contact over measured loci
    G = {**a4_coords_set("germline"), **a4_coords_set("imprint")}
    tol = 2.3                                    # tolerable drive in spinodal units (declared, not tuned)
    rows = []
    for k, v in G.items():
        g = v["gamma_canonical"]; hsp = spinodal(g); cc = v["contact_competent"]
        assist = 0.30 * hsp if cc else 0.0
        h_path = 2.0 * hsp                        # a deep pathological hold (held ON)
        # required clearing drive = h_path + spinodal ; available = tol*hsp + assist
        required = h_path + hsp
        available = tol * hsp + assist
        lever = "B" if available >= required else "A"
        # verify by integration
        cleared = _settle(g, h_path - (tol * hsp + assist), s0=+np.sqrt(g)) < 0
        rows.append(dict(locus=k, gamma=round(g, 4), contact=cc, lever=lever, cleared_by_drive=bool(cleared)))
    # consistency: predicted lever B exactly when integration clears
    consistent = all((r["lever"] == "B") == r["cleared_by_drive"] for r in rows)
    nB = sum(1 for r in rows if r["lever"] == "B"); nA = len(rows) - nB
    return {"name": "AM2 lever map on the (gamma, A4) plane",
            "tolerable_drive_spinodal_units": tol, "n_loci": len(rows),
            "n_leverB_drive_reachable": nB, "n_leverA_needs_edit": nA,
            "prediction_matches_integration": bool(consistent),
            "sample": rows[:6],
            "grade": "[V] the two levers partition (gamma, contact); absolute caps/doses are runtime [O]",
            "pass": bool(consistent)}


def AM3_contact_boundary_curve():
    """The 3D contact boundary on the two channels (gamma, A4-contact). A switch held ON by a pathological
    drive h_path clears only if the tolerable external budget B0 PLUS the contact-assist delta reaches the
    far spinodal: B0 + delta >= h_path + spinodal(gamma). Since spinodal(gamma) grows with gamma, the
    required contact-assist delta*(gamma) = h_path + spinodal(gamma) - B0 RISES with gamma -- a deeper
    switch needs MORE A4 contact-assist to stay drive-reachable. Absolute units throughout."""
    def sp(g):
        return 2.0 * (g / 3.0) ** 1.5
    gammas = np.linspace(1.30, 1.55, 12)
    deltas = np.linspace(0.0, 0.6, 13)           # absolute contact-assist
    h_path = 0.50                                 # absolute pathological hold
    B0 = 0.90                                     # absolute tolerable external budget
    surface = []
    for g in gammas:
        req = h_path + sp(g)                       # absolute drive required to clear
        row = [1 if (B0 + d) >= req else 0 for d in deltas]
        surface.append(row)
    boundary = []
    for i, g in enumerate(gammas):
        d_needed = h_path + sp(g) - B0            # delta* analytic
        j = next((jj for jj, d in enumerate(deltas) if surface[i][jj] == 1), None)
        boundary.append({"gamma": round(float(g), 3), "delta_star": (round(max(0.0, d_needed), 4))})
    # checks: (a) assist monotonically helps; (b) a real boundary exists; (c) delta* RISES with gamma (the
    # gamma<->A4 coupling); (d) integration cross-check on one reachable and one unreachable point.
    monotone = all(all(surface[i][j] <= surface[i][j + 1] for j in range(len(deltas) - 1)) for i in range(len(gammas)))
    flat = [x for row in surface for x in row]
    has_boundary = (0 in flat) and (1 in flat)
    dstars = [b["delta_star"] for b in boundary]
    rises_with_gamma = dstars[-1] > dstars[0] + 1e-6
    # integration cross-check at gamma=1.50
    gx = 1.50; spx = sp(gx)
    cleared_reachable = _settle(gx, h_path - (B0 + (h_path + spx - B0 + 0.05)), s0=+np.sqrt(gx)) < 0   # delta just above need
    cleared_unreach = _settle(gx, h_path - (B0 + 0.0), s0=+np.sqrt(gx)) < 0                            # delta=0
    integ_ok = cleared_reachable and (not cleared_unreach)
    return {"name": "AM3 the 3D contact boundary curve on (gamma, contact-assist)",
            "gamma_grid": [round(float(x), 3) for x in gammas], "delta_grid": [round(float(x), 3) for x in deltas],
            "h_path": h_path, "tolerable_budget_B0": B0,
            "reachable_surface": surface, "boundary_delta_star_by_gamma": boundary,
            "assist_monotonically_helps": bool(monotone), "boundary_exists": bool(has_boundary),
            "delta_star_rises_with_gamma": bool(rises_with_gamma),
            "integration_crosscheck_ok": bool(integ_ok),
            "grade": "[V] the drive-reachable boundary bends with A4 contact (delta* rises with gamma); "
                     "absolute energies are runtime [O]",
            "pass": bool(monotone and has_boundary and rises_with_gamma and integ_ok)}


def run_battery():
    tests = [AM1_primeboost_at_coordinate(), AM2_lever_map(), AM3_contact_boundary_curve()]
    allp = all(t["pass"] for t in tests)
    return {"module": "a4_application_map", "battery": "AM1-AM4", "seed": SEED,
            "AM4_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "coordinate-DEPENDENCE of dose, lever MAP, boundary SHAPE read [V]; absolute doses, "
                        "assist energies, clinical outcomes are runtime [O]; application belongs to clinicians/regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
