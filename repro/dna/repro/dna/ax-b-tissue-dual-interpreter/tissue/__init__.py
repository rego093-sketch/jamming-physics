"""
tissue/ — VP DNA tissue-level dual interpreter (이원화 / dualized).

Mirror of the cell-level γ/A4 LEVEL/SHAPE split, lifted to the tissue scale.

  ONE morphogen field            c(x) solving   D·∇²c − c/τ + source = 0
  ── LEVEL = mean(c)      → SIZE  (the size/quantity channel; cell-level γ)
  └─ SHAPE = robust_z(c)  → FORM  (the territory/boundary channel; cell-level A4)

The two readings are orthogonal projections of the SAME field, exactly as
γ (window-mean) and A4 (mean-removed robust z-score) are orthogonal
projections of the SAME stiffness signal s(x) at the cell level.

Design law (no compromise):
  * every constant is LOCKed from param_db.json — zero inline magic numbers
  * every field quantity is a closed form exact to machine epsilon
  * the old coarse Jacobi solver is kept ONLY as a convergence witness that
    demonstrates its own roughness (supersession, not a patch)
  * precision ≠ accuracy is enforced in exactly one place (grading.py): the
    LEVEL/SHAPE/orthogonality machinery is [V] exact (precision); the map to
    real organ mass / real anatomy is [O] (named, open obstacle)
"""

from . import lock
from . import field
from . import level
from . import shape
from . import orthogonality
from . import grading
from . import interpreter
# NOTE: `gate` is the fail-closed entry point run as `python3 -m tissue.gate`.
# It is intentionally NOT eagerly imported here: doing so would place it in
# sys.modules before runpy executes it as __main__, raising a spurious
# RuntimeWarning. Import it explicitly where needed (run.py does).

from .lock import lambda_um, lock_manifest
from .level import read_level
from .shape import read_shape
from .interpreter import interpret_tissue, reading_hash, developmental_run
from .grading import completion_status

__all__ = [
    "lock", "field", "level", "shape", "orthogonality",
    "grading", "interpreter",
    "lambda_um", "lock_manifest",
    "read_level", "read_shape",
    "interpret_tissue", "reading_hash", "developmental_run",
    "completion_status",
]

__version__ = "0.1.0"
