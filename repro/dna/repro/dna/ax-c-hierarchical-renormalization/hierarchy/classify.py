# -*- coding: utf-8 -*-
"""
hierarchy.classify -- the SCALE-CLASSIFICATION ledger.

The over-simplification Appendix B left in place was to act as if there were only TWO scales (cell,
tissue) and to leave them unconnected. The user's instruction is to CLASSIFY which reading channel
lives at which scale -- some are molecular, some cellular, some tissue, some organ -- and to make
the climb between them explicit.

This module is that classification. It is the map a reviewer reads to see, for every channel in the
whole corpus, WHICH structural level it reads and HOW it connects to the renormalization tower.
It is data, not physics; it carries no fitted number. It exists so the scale of every read is
declared in ONE place and cannot drift.

THE TOWER (levels the operator climbs):
    L0 molecular/chromatin -> L1 cell -> L2 tissue -> L3 organ -> L4 organ system/body
"""

# every reading channel in the corpus, tagged with the level it reads
CHANNELS = [
    {
        "channel": "NN stacking dG -> gamma (MATERIAL level)",
        "reads_level": "L0 molecular (base-step) -> L1 cell",
        "what": "per-dinucleotide stacking stiffness; mean over a window = gamma, the cell's "
                "genome-stiffness LEVEL (the polymer modulus the cell is built from)",
        "source": "chapters 2, 13",
        "axis": "stiffness LEVEL (gamma-mirror)",
        "connects_to_tower": "sets B at the BASE (the cell's intrinsic stiffness anchor)",
    },
    {
        "channel": "A4 coordinate (shell / anchor / helical phase)",
        "reads_level": "L0 molecular -> L1 cell",
        "what": "the SHAPE of the same stiffness signal (gamma's mean removed by robust_z); "
                "contact-competent geometry",
        "source": "chapter 13",
        "axis": "stiffness SHAPE (A4-mirror)",
        "connects_to_tower": "the cell-level instance of the LEVEL/SHAPE split the tower repeats",
    },
    {
        "channel": "R19 switch (spinodal, barrier, |s|)",
        "reads_level": "L1 cell",
        "what": "the bistable state of one regulatory switch, derived from gamma alone",
        "source": "chapters 3, 4",
        "axis": "switch state (within a cell)",
        "connects_to_tower": "intra-cell dynamics; not a tower rung (the tower is mechanical "
                             "aggregation, orthogonal to the switch read)",
    },
    {
        "channel": "CpG O/E -> methylation drive h",
        "reads_level": "L1 cell (environment write)",
        "what": "the writable drive that moves the switch; environment-set, sequence-read",
        "source": "chapters 6, 9",
        "axis": "drive (within a cell)",
        "connects_to_tower": "intra-cell; orthogonal to the mechanical tower",
    },
    {
        "channel": "morphogen LEVEL = mean(c) -> SIZE",
        "reads_level": "L2 tissue",
        "what": "the morphogen budget of a tissue domain (the CHEMICAL/patterning axis)",
        "source": "Appendix B",
        "axis": "chemical LEVEL (size)",
        "connects_to_tower": "the CHEMICAL axis at L2 -- runs ALONGSIDE the mechanical tower, not "
                             "in place of it (the gap Appendix B left)",
    },
    {
        "channel": "morphogen SHAPE = robust_z(c) -> FORM (territories)",
        "reads_level": "L2 tissue",
        "what": "the territory boundaries of a tissue domain (the CHEMICAL/patterning axis)",
        "source": "Appendix B",
        "axis": "chemical SHAPE (form)",
        "connects_to_tower": "the territories are the natural phi(x) domains the MECHANICAL SHAPE "
                             "(this appendix) reads -- the chemical and mechanical axes meet here",
    },
    {
        "channel": "packing fraction phi, jamming J, B_eff, rho_eff, c_eff",
        "reads_level": "L1->L4 (EVERY mechanical rung)",
        "what": "the effective stiffness and density an aggregate ACQUIRES by packing its units "
                "(the MECHANICAL axis 'cells gather -> volume + stiffness')",
        "source": "Appendix C (this)",
        "axis": "mechanical LEVEL (B) + SHAPE (stiffness pattern)",
        "connects_to_tower": "IS the tower: the renormalization operator R that climbs every rung",
    },
    {
        "channel": "isostatic coordination z_iso = 2d",
        "reads_level": "structural invariant (all rungs)",
        "what": "the marginal contact number at jamming; the anchor of the rigidity onset",
        "source": "Appendix C (this)",
        "axis": "mechanical structural invariant",
        "connects_to_tower": "the universal anchor that makes the rigidity emergence parameter-free",
    },
    {
        "channel": "VP master c^2 = B/rho (wave speed per level)",
        "reads_level": "L0->L4 (the through-line)",
        "what": "the mechanical signal speed at every level; the SAME relation the VP core thesis "
                "applies to the vacuum (vacuum as a jammed elastic solid)",
        "source": "Appendix C (this) <- core physics volume",
        "axis": "the unifying relation across all scales",
        "connects_to_tower": "the invariant carried up every rung; softens by sqrt(J) per rung",
    },
]


def levels_covered():
    """The set of tower levels that at least one channel reads (for the gate's coverage check)."""
    levels = set()
    for c in CHANNELS:
        levels.add(c["reads_level"])
    return sorted(levels)


def classification_table():
    """The full classification, returned as the ledger a reviewer reads."""
    return CHANNELS


def coverage_ok():
    """True iff every channel has a non-empty level tag and a tower connection (no channel left
    unclassified -- the gate H9 keys on this)."""
    return all(c.get("reads_level") and c.get("connects_to_tower") for c in CHANNELS)
