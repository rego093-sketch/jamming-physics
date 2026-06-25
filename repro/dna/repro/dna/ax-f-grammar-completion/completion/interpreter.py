# -*- coding: utf-8 -*-
"""
completion.interpreter -- the grammar-completion reading (해독기).

The blueprint's grammar completed in three directions and declared honestly: the organ atlas
(G2 across cardiac/neural/hepatic), the dynamical grammar G4 (pragmatics, CpG-O/E state
family), the body-plan grammar G5 (genre, Hox colinearity), the 2D grammar-space map with
its one-operator proof, and the two-axis decoding declaration (structural complete /
functional open).
"""
import json
import hashlib

from . import (lock, atlas, dynamical, bodyplan, grammar_space, declaration, grading)


def interpret_grammar_completion():
    """The full grammar-completion reading."""
    reading = {
        "_what": ("the DNA blueprint's grammar COMPLETED and declared honestly. Appendix E found "
                  "a 3-level tower (G1 material, G2 regulatory, G3 architecture); this fills the "
                  "grammar SPACE -- the organ atlas (G2 across organs), the dynamical grammar G4 "
                  "(state), the body-plan grammar G5 (body) -- all read by one operator, and "
                  "issues a two-axis decoding declaration: structural decoding complete, "
                  "functional decoding open."),
        "grammar_space": grammar_space.grammar_space_map(),
        "one_operator_proof": grammar_space.same_operator_proof(),

        "organ_atlas_G2_generalized": atlas.confusion_matrix(),
        "dynamical_G4": {
            "orthogonality_to_material": dynamical.orthogonality_to_material(),
            "reads": {k: dynamical.read(lock.promoter(k)[0]) for k in lock.promoter_keys()},
            "state_family_example": dynamical.state_family(
                lock.promoter(lock.promoter_keys()[0])[0]),
        },
        "bodyplan_G5": {
            "colinearity": bodyplan.colinearity(),
            "read": bodyplan.read(),
        },

        "decoding_declaration": declaration.decoding_declaration(),

        "grade_ledger": grading.LEDGER,
        "completion": grading.completion_status(),
    }
    return reading


def reading_hash(reading):
    """Stable 16-char SHA-256 over the reading (determinism witness)."""
    blob = json.dumps(reading, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]
