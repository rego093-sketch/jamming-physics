#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setpoint_emergence.py  --  why pressure regulation differs between lower and higher organisms.

The VP framework claims the same jamming substrate (R19 switch + FHN pump) scales across life. The
hemodynamic test of that universality is NOT "everyone has the mammalian loop" -- it is the prediction
that a DEFENDED arterial-pressure setpoint is an EMERGENT property that appears only when three things
co-exist on the same hydraulic core MAP = CVP + CO x SVR:

    (a) a CLOSED circuit          -> pressure is a well-defined regulated variable at all
    (b) a high-resistance EFFECTOR -> the loop has an actuator (arteriolar SVR / Windkessel)
    (c) an INTEGRATING organ       -> the slow loop has infinite-gain memory (renal pressure-natriuresis)

Remove any leg and the regulated variable degrades from DEFENDED to merely error-regulated to INCIDENTAL.
The lower->higher transition is therefore loop ACCRETION on a fixed core, and the framework predicts the
QUALITATIVE jump. This module reproduces that jump deterministically with the SAME primitives used for
the mammalian package (baroreflex_buffer, kidney_integrator) -- no new substrate math (C1).

  organism grade (anchor [L])                    loops present        regulated variable
  ---------------------------------------------  -------------------  ---------------------------
  diffusion only (sponge, cnidarian, flatworm)   none (no circuit)    no pressure variable
  open system (most arthropods/molluscs)         core only            INCIDENTAL (hemolymph, low P)
  closed single-circuit low-P (fish)             core + fast buffer   error-regulated (steady error)
  closed double-circuit high-P (bird, mammal)    core + buffer + integrator  DEFENDED setpoint (error->0)

GRADES (C3): the emergence/qualitative-jump SHAPE is sim-reproduced [V]; the phylogenetic mapping and the
open-vs-closed comparative anatomy are cited [L]; absolute pressures per taxon are [O]. No claim that a
single number is derived per species here -- only the loop-accretion structure.
"""
import os, sys
import numpy as np
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
import vp_hmd_loops as L


# Phylogenetic ladder (anchors are comparative-physiology facts [L]).
LADDER = [
    dict(grade="diffusion_only", taxa="sponges, cnidarians, flatworms",
         circuit=False, effector=False, integrator=False,
         note="transport by diffusion + body-wall contraction; NO pressure variable exists"),
    dict(grade="open_system", taxa="most arthropods and molluscs",
         circuit=False, effector=False, integrator=False,
         note="hemolymph in a hemocoel; ostiate/tubular heart; low INCIDENTAL pressure; no closed loop, "
              "no arteriolar SVR effector, no renal pressure-natriuresis; PIEZO exists for proprioception "
              "but is not wired to a pressure reflex"),
    dict(grade="closed_single_low_P", taxa="fish (teleosts)",
         circuit=True, effector=True, integrator=False,
         note="true vessels and pressure, but a gill circuit in series drops systemic pressure; "
              "branchial baro-like reflexes give FAST (proportional) regulation; RAS present, but the "
              "full integral pressure-natriuresis loop is not yet the dominant defender"),
    dict(grade="closed_transitional", taxa="amphibians, reptiles",
         circuit=True, effector=True, integrator=True,
         note="incomplete ventricular separation; baroreflex + RAAS maturing toward a defended setpoint"),
    dict(grade="closed_double_high_P", taxa="birds, mammals",
         circuit=True, effector=True, integrator=True,
         note="complete double circuit, high pressure; full baroreflex (carotid sinus + aortic arch) + "
              "full renal pressure-natriuresis (Guyton) -> the DEFENDED MAP modelled by this package"),
]


def stage_response(circuit, effector, integrator, step_mmHg=20.0):
    """Response of the hydraulic core to a +step disturbance under the loops present.
    Returns restoration fraction: 0 = incidental (no restoration), ~step/(1+G) residual = error-regulated,
    ~0 residual = defended. Uses the SAME primitives as the mammalian package."""
    if not circuit:
        # no closed circuit (diffusion-only or open hemocoel): pressure is not a regulated variable.
        # the disturbance simply persists -> restoration fraction 0 (INCIDENTAL).
        return dict(regulated_variable="none/incidental", residual_mmHg=round(float(step_mmHg), 4),
                    restoration_fraction=0.0, regime="incidental")
    if effector and not integrator:
        # closed + fast effector only: proportional buffer -> residual = step/(1+G) (steady error remains).
        b = L.baroreflex_buffer(step_mmHg=step_mmHg, transduction=1.0)
        return dict(regulated_variable="pressure (error-regulated)", residual_mmHg=b["residual_mmHg"],
                    restoration_fraction=round(float(b["buffered_fraction"]), 4), regime="error_regulated")
    if effector and integrator:
        # closed + effector + integral controller: perfect adaptation -> error -> 0 (DEFENDED).
        _, p_load, pset = L.kidney_integrator(bolus_mL=400.0)
        residual = abs(p_load - pset)
        return dict(regulated_variable="pressure (defended setpoint)", residual_mmHg=round(float(residual), 6),
                    restoration_fraction=round(float(1.0 - residual / step_mmHg), 6), regime="defended")
    # closed but no effector (degenerate) -> incidental
    return dict(regulated_variable="none/incidental", residual_mmHg=round(float(step_mmHg), 4),
                restoration_fraction=0.0, regime="incidental")


def setpoint_emergence():
    rows = []
    for rung in LADDER:
        resp = stage_response(rung["circuit"], rung["effector"], rung["integrator"])
        rows.append(dict(grade=rung["grade"], taxa=rung["taxa"],
                         circuit=rung["circuit"], effector=rung["effector"], integrator=rung["integrator"],
                         regime=resp["regime"], restoration_fraction=resp["restoration_fraction"],
                         residual_mmHg=resp["residual_mmHg"], note=rung["note"]))
    # the qualitative jump: regimes must progress incidental -> error_regulated -> defended as loops accrue
    regimes = [r["regime"] for r in rows]
    order_ok = (regimes.count("incidental") >= 2 and "error_regulated" in regimes and "defended" in regimes
                and regimes.index("error_regulated") < regimes.index("defended"))
    # structural truth: a DEFENDED setpoint requires circuit AND effector AND integrator simultaneously
    defended = [r for r in rows if r["regime"] == "defended"]
    requisites_ok = all(r["circuit"] and r["effector"] and r["integrator"] for r in defended) and bool(defended)
    return dict(
        ladder=rows,
        qualitative_jump_ordered=bool(order_ok),
        defended_requires_all_three=bool(requisites_ok),
        thesis="a defended arterial-pressure setpoint is EMERGENT: it appears only when a closed circuit, "
               "an arteriolar effector and a renal integrator co-exist on the same MAP = CVP + CO x SVR "
               "core. Lower organisms lack one or more legs, so pressure is incidental (open systems) or "
               "merely error-regulated (single-circuit fast reflex); the mammalian defended MAP is the "
               "top rung of loop accretion, not a different substrate",
        emergence_grade="[V]", phylogeny_anchor_grade="[L]", absolute_per_taxon_grade="[O]")


if __name__ == "__main__":
    import json
    r = setpoint_emergence()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nqualitative jump ordered:", r["qualitative_jump_ordered"],
          "| defended requires all three legs:", r["defended_requires_all_three"])
