# -*- coding: utf-8 -*-
"""
hierarchy/ — VP DNA hierarchical scale-renormalization interpreter.

Appendix B dualized two scales (cell γ/A4; tissue morphogen LEVEL/SHAPE) but left
them UNCONNECTED and carried only the CHEMICAL axis. This package repairs the
over-simplification on both counts:

  CLASSIFY  every reading channel by the structural level it reads
            L0 molecular → L1 cell → L2 tissue → L3 organ → L4 organ system/body
  CLIMB     the tower with the renormalization operator R, so each level's
            stiffness B, density ρ and wave speed c are DERIVED from the level
            below by jamming physics — the formal statement of
            "세포들이 모이면 그자체로 부피이자 강성이 될것이다"
            (cells gather and become, by that act, both VOLUME and STIFFNESS).

The renormalization operator R, on units (B, ρ) packed at fraction φ:

      ρ' = φ·ρ                         (density — EXACT, void carries no mass)   [V]
      0 = B_Reuss ≤ B' ≤ B_Voigt = φ·B (stiffness — EXACT elastic-mixture bracket) [V]
      B' = φ·B·J(φ),  J(φ) ∈ [0,1]     (placed in the bracket by the jamming onset)
      c' = √(B'/ρ') = c·√J             (VP master c²=B/ρ applied twice — EXACT)   [V]

so the wave-speed SOFTENING RATIO per rung is exactly √J, and the signal speed
DECREASES monotonically up the tower for any φ<1 (idealized RG theorem). The
rigidity fraction J(φ)=√((φ−φ_c)/(1−φ_c)) above φ_c is [L]-grounded (a composition
of O'Hern 2003 and Wyart 2005); the ABSOLUTE biological moduli are [O].

At any level the stiffness field B(x) is split into the SAME orthogonal projections
as the cell γ/A4:
      LEVEL = mean(B(x))      → the effective modulus (how stiff)        [γ-mirror]
      SHAPE = robust_z(B(x))  → the stiffness pattern (where stiff)      [A4-mirror]
with LEVEL ⟂ SHAPE proven to machine epsilon.

Design law (no compromise):
  * every constant is LOCKed from param_db.json — zero inline magic numbers
  * the density law, the Voigt/Reuss bracket, the √J softening ratio, and the RG
    composition are EXACT [V]; the rigidity onset is [L]-grounded
  * precision ≠ accuracy is enforced in exactly one place (grading.py): the
    machinery is [V]/[L]; the map to a real elastography/AFM modulus atlas and the
    real per-rung packing fractions are [O] (named, open obstacles)

The through-line is c²=B/ρ — the SAME relation the VP core thesis applies to the
vacuum (vacuum as a jammed elastic solid). R is the bridge between the DNA/biology
volumes and the VP core physics volume.
"""

from . import lock
from . import jamming
from . import renorm
from . import ladder
from . import level
from . import shape
from . import orthogonality
from . import classify
from . import grading
from . import interpreter
# NOTE: `gate` is the fail-closed entry point run as `python3 -m hierarchy.gate`.
# It is intentionally NOT eagerly imported here: doing so would place it in
# sys.modules before runpy executes it as __main__, raising a spurious
# RuntimeWarning. Import it explicitly where needed (run.py does).

from .lock import lock_manifest, phi_c, ladder_rungs
from .jamming import rigidity_fraction, jamming_state, is_jammed
from .renorm import renormalize, compose_two, voigt_ceiling, reuss_floor
from .ladder import climb, default_phi_profile
from .level import read_level
from .shape import read_shape
from .orthogonality import certify
from .classify import classification_table, levels_covered, coverage_ok
from .interpreter import interpret_hierarchy, reading_hash, renormalization_demo
from .grading import completion_status

__all__ = [
    "lock", "jamming", "renorm", "ladder", "level", "shape",
    "orthogonality", "classify", "grading", "interpreter",
    "lock_manifest", "phi_c", "ladder_rungs",
    "rigidity_fraction", "jamming_state", "is_jammed",
    "renormalize", "compose_two", "voigt_ceiling", "reuss_floor",
    "climb", "default_phi_profile",
    "read_level", "read_shape", "certify",
    "classification_table", "levels_covered", "coverage_ok",
    "interpret_hierarchy", "reading_hash", "renormalization_demo",
    "completion_status",
]

__version__ = "0.1.0"
