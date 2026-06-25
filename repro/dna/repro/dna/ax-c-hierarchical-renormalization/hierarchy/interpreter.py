# -*- coding: utf-8 -*-
"""
hierarchy.interpreter -- the HIERARCHICAL scale-renormalization interpreter (해석기).

Appendix B dualized exactly TWO scales (cell gamma/A4; tissue morphogen LEVEL/SHAPE)
and treated them as UNCONNECTED -- tissue constants were looked up, never DERIVED
from the cell, and only the CHEMICAL (morphogen) axis was carried. The
over-simplification was twofold:
    (1) only two scales, with no rule to climb between them, and
    (2) only the chemical axis -- the MECHANICAL axis the user names
        ("세포들이 모이면 그자체로 부피이자 강성이 될것이다" -- cells gather and
        become, by that very act, both VOLUME and STIFFNESS) was missing entirely.

This interpreter repairs both. It:

    * CLASSIFIES every reading channel by the structural level it reads
      (L0 molecular -> L1 cell -> L2 tissue -> L3 organ -> L4 body)   [hierarchy.classify]
    * CLIMBS the tower with the renormalization operator R, so each level's
      stiffness B, density rho and wave speed c are DERIVED from the level below
      by jamming physics, not assumed                                  [hierarchy.ladder]
    * at any level, projects the stiffness field into the SAME orthogonal
      LEVEL/SHAPE split as the cell gamma/A4                  [hierarchy.level / .shape]
    * proves LEVEL ⟂ SHAPE to machine epsilon                 [hierarchy.orthogonality]
    * grades every channel honestly: the machinery is [V] exact / [L] grounded;
      the absolute biological moduli are [O] with named obstacles      [hierarchy.grading]

The through-line is the VP master relation c^2 = B/rho -- the SAME relation the VP
core thesis applies to the vacuum (vacuum as a jammed elastic solid), applied here
one structural level up at a time. The renormalization operator R is the bridge
between the DNA/biology volumes and the VP core physics volume.

Deterministic: pure arithmetic over closed forms; 2x SHA-256; fail-closed in the
gate. All constants inherited from the locked DB; nothing is fitted.
"""
import json
import hashlib

from . import lock, jamming, renorm, ladder, level, shape, orthogonality, classify, grading


def interpret_hierarchy(phis=None, phi_x=None):
    """The full hierarchical reading.

    Returns a dict with: the scale classification of every channel, the
    renormalization climb up the tower (B, rho, c derived rung by rung), the
    LEVEL/SHAPE dual of a structural level's stiffness field, the orthogonality
    certificate, the RG-composition (associativity) witness, the grade ledger, and
    an honest completion status.

    phis : optional per-rung packing-fraction profile for the climb (defaults to a
           documented jammed profile [F]); pass measured fractions to get the real
           flow (still [O] in absolute magnitude).
    phi_x: optional packing-fraction profile phi(x) across a level's domain for the
           LEVEL/SHAPE projection (defaults to a documented smoothstep [F]).
    """
    # --- the climb up the tower (mechanical aggregation; "cells -> volume+stiffness")
    climb = ladder.climb(phis)

    # --- the LEVEL/SHAPE dual of a structural level's stiffness field
    level_read = level.read_level(phi_x) if phi_x is not None else level.read_level(
        shape.smoothstep_phi_profile())
    shape_read = shape.read_shape(phi_x)

    # --- orthogonality certificate (LEVEL ⟂ SHAPE, exact)
    ortho = orthogonality.certify(phi_x)

    # --- RG-composition (associativity) witness: climbing two rungs == one combined
    pc, _, _ = lock.phi_c()
    phi1 = round(pc + 0.40 * (1.0 - pc), 6)
    phi2 = round(pc + 0.70 * (1.0 - pc), 6)
    B0, _, _ = lock.unit_bulk_modulus_pa()
    rho0, _, _ = lock.unit_density_kg_per_m3()
    composition = renorm.compose_two(B0, rho0, phi1, phi2)

    reading = {
        "_what": "hierarchical scale-renormalization interpreter: classify every "
                 "reading channel by structural level, then climb the tower with the "
                 "renormalization operator R (jamming) so each level's stiffness and "
                 "density are DERIVED from the level below -- 'cells gather and become "
                 "volume and stiffness'. The cell gamma/A4 LEVEL/SHAPE split is "
                 "repeated at every mechanical rung.",
        "vp_master_relation": "c^2 = B / rho  (same relation the VP core applies to "
                              "the vacuum; here applied one structural level up)",

        # 1) the classification the user demanded (the '분류')
        "scale_classification": {
            "tower_levels": ["L0 molecular/chromatin", "L1 cell", "L2 tissue",
                             "L3 organ", "L4 organ system/body"],
            "channels": classify.classification_table(),
            "levels_covered": classify.levels_covered(),
            "coverage_ok": classify.coverage_ok(),
        },

        # 2) the climb (the 'how to go up level by level')
        "renormalization_climb": climb,

        # 3) the LEVEL/SHAPE dual at a structural level (mechanical gamma/A4)
        "LEVEL_channel_stiffness_size": level_read,
        "SHAPE_channel_stiffness_pattern": shape_read,

        # 4) orthogonality + RG-composition (the flow is a consistent RG semigroup)
        "orthogonality": ortho,
        "rg_composition_associativity": composition,

        # 5) honest grades
        "grade_ledger": grading.LEDGER,
        "completion": grading.completion_status(),
    }
    return reading


def reading_hash(reading):
    """Stable 16-char SHA-256 over the reading (determinism witness)."""
    blob = json.dumps(reading, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]


def renormalization_demo(phis=None):
    """A compact, human-facing demonstration of the climb: the per-level (B, rho, c)
    trajectory and the exact softening ratio per rung. Shares the SAME operator as
    the full reading; nothing fitted."""
    climb = ladder.climb(phis)
    levels = climb["levels"]
    return {
        "levels": [{
            "level": L["level"], "name": L["name"],
            "B_pa": L["B_pa"], "rho_kg_per_m3": L["rho_kg_per_m3"],
            "c_m_per_s": L["c_m_per_s"],
            "softening_ratio_c_over_prev": L.get("softening_ratio_c_over_prev"),
            "rigidity_fraction_J": L.get("rigidity_fraction_J"),
        } for L in levels],
        "wave_speed_trajectory_m_per_s": climb["wave_speed_trajectory_m_per_s"],
        "wave_speed_monotone_decreasing": climb["wave_speed_monotone_decreasing"],
        "note": "softening ratio per rung = sqrt(J(phi)) EXACT [V]; absolute moduli [O].",
    }
