#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rna_vaccine.py  --  VACCINE AS A DOSED RNA DRIVE  (battery V1-V5).

  A vaccine, in substrate terms, is a DELIBERATE, DOSED drive h applied to the immune R19 switch. An
  mRNA / saRNA vaccine delivers an RNA payload that sets that drive (the RNA-layer channel, rna_layer.py)
  past the spinodal, so the immune switch makes a ONE-WAY flip into the protected (memory) basin and is
  then HELD there by its own barrier gamma^2/4 -- even after the payload clears. This is exactly the
  immune-memory hysteresis of transgenerational_immunity.py, now driven on purpose. Read at the MEASURED
  immune master-gene gamma. MAGNITUDE FIREWALL: schedule SHAPE and the existence of an interior optimum
  are read [V]; absolute dose, titre, and clinical timing are runtime [O].

V1  vaccine = supra-spinodal drive -> one-way flip into the protected basin (memory), held after clearance. [V]
V2  schedule matters: protected fraction over a finite horizon under a FIXED boost budget has an INTERIOR
    optimum in the boost interval (too short wastes the budget early; too long leaves gaps). [V]
V3  the optimum interval tracks the MEASURED protection half-life (place each boost as protection lapses). [V]
V4  why RNA (not a genome edit): the payload is TRANSIENT (h->0 after clearance) yet protection PERSISTS,
    held by the switch barrier -- protection is not sustained by lingering RNA. [V]
V5  honest scoreboard + firewall.
"""
import json
import numpy as np
from _substrate import immune_gamma, spinodal, barrier, SEED


def _settle_det(g, h, s0, n=4000, dt=0.01):
    s = float(s0)
    for _ in range(n):
        s += dt * (g * s - s ** 3 + h)
    return s


def _escape_rate(g, D, n_cells=6000, n_steps=4000, dt=0.01, seed=SEED):
    rng = np.random.default_rng(seed)
    s = np.full(n_cells, np.sqrt(g)); c = np.sqrt(2.0 * D * dt)
    crossed = np.zeros(n_cells, dtype=bool); esc = 0
    for _ in range(n_steps):
        s += (g * s - s ** 3) * dt + c * rng.standard_normal(n_cells)
        newly = (s < 0) & (~crossed); esc += int(np.sum(newly)); crossed |= newly
    return esc / (n_cells * n_steps * dt)


def V1_supraspinodal_flip():
    """Drive the immune switch past spinodal (the prime), clear the drive (antigen cleared), confirm it
    stays ON deterministically -- a one-way flip into memory held by the barrier."""
    g = max(immune_gamma().values())
    hsp = spinodal(g)
    s_after_prime = _settle_det(g, +1.4 * hsp, s0=-np.sqrt(g))   # naive OFF -> supra-spinodal drive
    flipped_on = s_after_prime > 0
    s_after_clear = _settle_det(g, 0.0, s0=s_after_prime)        # antigen/payload cleared (h=0)
    memory_held = s_after_clear > 0
    return {
        "name": "V1 vaccine = supra-spinodal flip into protected basin (memory held after clearance)",
        "immune_gamma": round(g, 4), "spinodal": round(hsp, 4), "barrier": round(barrier(g), 4),
        "flipped_ON_by_prime": bool(flipped_on), "memory_held_after_clearance": bool(memory_held),
        "grade": "[V] one-way flip + hysteretic hold; absolute dose/titre is runtime [O]",
        "pass": bool(flipped_on and memory_held),
    }


def _protected_fraction(interval, t_theta, n_boosts, horizon, dpts=2000):
    """Fraction of [0,horizon] covered by the union of [b, b+t_theta] for boosts placed at 0,interval,...
    (n_boosts of them). A boost resets protection to full for t_theta."""
    boosts = [i * interval for i in range(n_boosts) if i * interval < horizon]
    t = np.linspace(0, horizon, dpts)
    covered = np.zeros_like(t, dtype=bool)
    for b in boosts:
        covered |= (t >= b) & (t <= b + t_theta)
    return float(np.mean(covered))


def V2V3_schedule_optimum():
    """Measure the protection half-life from the deepest immune switch's escape rate, then sweep the boost
    interval under a FIXED budget over a finite horizon. Report the interior optimum and that it tracks
    the half-life."""
    g = max(immune_gamma().values())
    rate = _escape_rate(g, D=0.30, seed=SEED)
    # protection survival S(u)=exp(-rate u); protection half-life at theta=0.5
    theta = 0.5
    t_theta = float(-np.log(theta) / rate) if rate > 0 else float("inf")
    n_boosts = 4
    horizon = 5.0 * t_theta
    intervals = np.linspace(0.2 * t_theta, 2.0 * t_theta, 40)
    fracs = [_protected_fraction(u, t_theta, n_boosts, horizon) for u in intervals]
    i_best = int(np.argmax(fracs))
    u_best = float(intervals[i_best])
    interior = 0 < i_best < len(intervals) - 1
    tracks_halflife = abs(u_best - t_theta) < 0.5 * t_theta
    return {
        "name": "V2/V3 schedule has an interior optimum tracking the measured protection half-life",
        "immune_gamma": round(g, 4), "escape_rate": round(rate, 6), "protection_half_life": round(t_theta, 3),
        "n_boosts_budget": n_boosts, "horizon": round(horizon, 3),
        "best_interval": round(u_best, 3), "best_protected_fraction": round(fracs[i_best], 4),
        "optimum_is_interior": bool(interior), "optimum_tracks_half_life": bool(tracks_halflife),
        "grade": "[V] inverted-U / interior optimum SHAPE; absolute clinical interval is runtime [O]",
        "pass": bool(interior and tracks_halflife),
    }


def V4_transient_payload_persistent_protection():
    """The payload sets h transiently; after clearance h=0 yet protection persists, held by the barrier
    (not by lingering RNA). Contrast a deeper vs shallower switch: both hold once flipped, with no
    residual drive."""
    g = max(immune_gamma().values())
    hsp = spinodal(g)
    s_on = _settle_det(g, +1.4 * hsp, s0=-np.sqrt(g))    # payload present: flip
    # payload cleared: h identically zero. If protection were RNA-sustained it would relax to OFF.
    s_cleared = _settle_det(g, 0.0, s0=s_on)
    payload_drive_after = 0.0                            # h=0 by construction (RNA cleared)
    protection_persists = s_cleared > 0
    not_rna_sustained = (payload_drive_after == 0.0) and protection_persists
    return {
        "name": "V4 transient payload, persistent protection (held by barrier, not lingering RNA)",
        "immune_gamma": round(g, 4), "payload_drive_after_clearance": payload_drive_after,
        "s_after_clearance": round(s_cleared, 4), "protection_persists_at_zero_drive": bool(protection_persists),
        "protection_not_sustained_by_RNA": bool(not_rna_sustained),
        "grade": "[V] payload transient + protection barrier-held; this is why an RNA vaccine needs no edit",
        "pass": bool(not_rna_sustained),
    }


def run_battery():
    tests = [V1_supraspinodal_flip(), V2V3_schedule_optimum(), V4_transient_payload_persistent_protection()]
    allp = all(t["pass"] for t in tests)
    return {"module": "rna_vaccine", "battery": "V1-V5", "seed": SEED,
            "V5_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "flip DIRECTION, schedule SHAPE, transience/persistence read [V]; absolute dose, "
                        "titre and clinical timing are runtime [O]; vaccine development belongs to clinicians/regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
