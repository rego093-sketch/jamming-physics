# -*- coding: utf-8 -*-
"""
grammar.heart -- the heart resolution: the arrangement Appendix D imported is WRITTEN in the
blueprint, at the regulatory grammar level.

Appendix D had to import MEASURED cardiac moduli (single-cell AFM, decellularized ECM)
because the developmental arrangement/timing was orthogonal to the cell-level material
gamma -- the Appendix A null (rho = +0.071). This module shows that the missing arrangement
is readable from sequence at the regulatory grammar G2: the cardiac TF code that specifies
cardiac tissue identity. The blueprint had the arrangement all along; the corpus had been
reading the wrong (material) level. This REDUCES, in principle, the external-data reliance:
the tissue-identity signal is a sequence read, not an import.
"""
import numpy as np

from . import lock, material, regulatory, hierarchy


def heart_arrangement_is_in_sequence():
    """The cardiac arrangement signal (G2) is present and strong in cardiac promoters and
    absent in the control -- so the arrangement Appendix D imported is sequence-readable."""
    sep = hierarchy.tissue_identity_separation()
    sh = hierarchy.shuffle_test()
    return {
        "claim": "the cardiac tissue arrangement is WRITTEN in the sequence at the "
                 "regulatory grammar level (G2), not absent from the blueprint",
        "cardiac_grammar_signal_cardiac_vs_control": {
            "cardiac_mean": sep["cardiac_mean_G2_total"],
            "control_mean": sep["control_mean_G2_total"],
            "ratio": sep["G2_cardiac_over_control_ratio"],
        },
        "material_level_blind_to_it": not sep["G1_separates_tissue"],
        "arrangement_above_material": sh["material_level_preserved_exactly"]
                                      and sh["cardiac_grammar_collapsed"],
        "appendix_d_needed_external_because": "it read the cell-level MATERIAL gamma, which "
            "is orthogonal to the arrangement (Appendix A null rho=+0.071); the arrangement "
            "lives one grammar level up, in the cardiac TF syntax",
        "external_data_reliance_reduced": "the tissue-identity signal is now a SEQUENCE read "
            "(the cardiac grammar G2), not an imported measurement",
        "grade": "[L] real cardiac vs control promoters + [V] exact shuffle invariance",
    }


def what_each_level_supplies_to_the_heart():
    """Map the three grammars to the heart blueprint: material -> cell stiffness; regulatory
    -> which tissue (cardiac identity); architecture -> the layout (배치도)."""
    return {
        "G1_material_cell": "the CELL's intrinsic stiffness (the cardiomyocyte material) -- "
            "what Appendix A/C/D read; necessary but blind to tissue identity",
        "G2_regulatory_tissue": "WHICH tissue a region builds -- the cardiac TF code (GATA, "
            "NKX2-5, MEF2, TBX5, HAND); the tissue-identity blueprint the corpus missed",
        "G3_architecture_organ": "the spatial LAYOUT of cardiac regulatory elements (the "
            "배치도) -- the arrangement map; toward the organ's exact form, which cells "
            "alone cannot give",
        "synthesis": "the heart's exact form needs all three grammars: material (cell), "
            "regulatory (tissue identity), architecture (arrangement). Reading only the "
            "material level forced the external-moduli import of Appendix D; the upper "
            "grammars are in the blueprint.",
    }


def remaining_external_dependence():
    """Honest: what still needs measured data even with the upper grammars read."""
    return {
        "still_external": [
            "ABSOLUTE modulus values (the cell/ECM moduli) -- the regulatory grammar reads "
            "tissue IDENTITY and arrangement, not the kilopascal magnitudes; those remain "
            "measured inputs (Appendix D).",
            "FUNCTIONAL validation -- that A4_2 predicts measured cardiac enhancer ACTIVITY "
            "(VISTA/ATAC/MPRA) is [O]; the grammar is read, its quantitative phenotype is "
            "not yet validated.",
            "the real 3D ARRANGEMENT MAP -- G3 here is the local element layout; the true "
            "spatial tissue 배치도 (Hi-C contacts, Hox-style colinearity) is [O].",
        ],
        "now_internal": [
            "tissue IDENTITY (cardiac vs not) -- now a sequence read (G2), 14x separation",
            "the arrangement SIGNAL (where cardiac control concentrates) -- A4_2 from sequence",
        ],
        "verdict": "the upper grammars convert tissue IDENTITY and ARRANGEMENT from imported "
                   "to sequence-readable; absolute MAGNITUDES and functional VALIDATION "
                   "remain measured -- a smaller, named external dependence than before",
    }
