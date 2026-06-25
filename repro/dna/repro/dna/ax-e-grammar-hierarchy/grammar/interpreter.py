# -*- coding: utf-8 -*-
"""
grammar.interpreter -- the grammar-hierarchy reading (해석기).

The blueprint read at three grammatical levels, each with its (gamma, A4) pair via the same
robust_z operator: G1 material (cell), G2 regulatory (tissue), G3 architecture (organ). The
reading returns the three reads per sequence, the three establishing results (tissue
identity readable, upper-grammar-above-material, orthogonality), the same-operator proof,
the heart resolution, and honest grades.
"""
import json
import hashlib

from . import lock, material, regulatory, architecture, hierarchy, heart, grading


def interpret_grammar_hierarchy():
    """The full grammar-hierarchy reading."""
    per_seq = {}
    for key in lock.sequence_keys():
        seq, tissue, _ = lock.sequence(key)
        per_seq[key] = {
            "tissue": tissue,
            "levels": hierarchy.read_all_levels(seq),
        }

    reading = {
        "_what": "the DNA blueprint read at THREE grammatical levels -- the cell-level "
                 "grammar (gamma, A4) lifted up the tower. The corpus had read only the "
                 "bottom (material) level; this finds the tissue-level and organ-level "
                 "grammars it missed, and locates in them the arrangement the heart forced "
                 "Appendix D to import as external measured moduli.",
        "the_hierarchy": {
            "G1_material_cell": "phonology -- stacking dG -> (gamma_1, A4_1); cell stiffness",
            "G2_regulatory_tissue": "syntax -- cardiac TF grammar -> (gamma_2, A4_2); tissue "
                                    "identity (THE MISSED UPPER A4)",
            "G3_architecture_organ": "discourse -- element layout -> (gamma_3, A4_3); the "
                                     "arrangement map (배치도)",
        },
        "per_sequence_reads": per_seq,

        "result_1_tissue_identity_readable": hierarchy.tissue_identity_separation(),
        "result_2_upper_grammar_above_material": hierarchy.shuffle_test(),
        "result_3_levels_orthogonal": hierarchy.cross_grammar_orthogonality(),
        "same_operator_all_levels": hierarchy.same_operator_proof(),

        "heart_resolution": heart.heart_arrangement_is_in_sequence(),
        "what_each_level_supplies": heart.what_each_level_supplies_to_the_heart(),
        "remaining_external_dependence": heart.remaining_external_dependence(),

        "grade_ledger": grading.LEDGER,
        "completion": grading.completion_status(),
    }
    return reading


def reading_hash(reading):
    """Stable 16-char SHA-256 over the reading (determinism witness)."""
    blob = json.dumps(reading, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:16]
