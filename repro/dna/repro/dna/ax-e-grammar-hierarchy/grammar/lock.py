# -*- coding: utf-8 -*-
"""
grammar.lock -- the LOCKED constant surface for the grammar-hierarchy interpreter.

Reads every input from param_db.json: the SantaLucia 1998 nearest-neighbour stacking
parameters (the G1 material), the cardiac TF consensus motifs (the G2 regulatory grammar),
the three REAL human promoter sequences (two cardiac, one housekeeping), and the
dinucleotide-shuffle settings. Zero inline magic numbers; every value carries a grade and
provenance.
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_DB_PATH = os.path.join(_HERE, "..", "param_db.json")


def _load_db():
    if not os.path.exists(_DB_PATH):
        raise FileNotFoundError(
            "param_db.json not found. The grammar engine refuses to invent sequences, "
            "stacking parameters, or motifs; place the locked DB next to it."
        )
    with open(_DB_PATH, encoding="utf-8") as fh:
        return json.load(fh), os.path.relpath(_DB_PATH, _HERE)


DB, DB_PATH = _load_db()


# ----------------------------------------------------------------------------
# G1 material -- nearest-neighbour stacking dG
# ----------------------------------------------------------------------------
def nn_dG():
    """SantaLucia 1998 NN Delta-G_37 table {dimer: kcal/mol}. [L]."""
    return dict(DB["nn_stacking_dG_kcal_per_mol"]["values"])


# ----------------------------------------------------------------------------
# G2 regulatory -- cardiac TF grammar
# ----------------------------------------------------------------------------
def cardiac_motifs():
    """Cardiac TF consensus motifs {name: IUPAC regex}. [L] (JASPAR + cardiac GRN)."""
    return dict(DB["cardiac_tf_grammar"]["motifs_IUPAC"])


def regulatory_window_bp():
    """Sliding-window half-width for the regulatory density signal. [F]."""
    return DB["cardiac_tf_grammar"]["window_bp"]["value"]


# ----------------------------------------------------------------------------
# real sequences
# ----------------------------------------------------------------------------
def sequence(name):
    """A real promoter sequence by key (NPPA_cardiac / TNNT2_cardiac / GAPDH_housekeeping)."""
    e = DB["real_sequences"][name]
    return e["seq"], e["tissue"], e["provenance"]


def sequence_keys():
    return [k for k in DB["real_sequences"] if not k.startswith("_") and k != "grade"]


def cardiac_keys():
    return [k for k in sequence_keys() if DB["real_sequences"][k]["tissue"] == "cardiac"]


def control_keys():
    return [k for k in sequence_keys()
            if DB["real_sequences"][k]["tissue"] != "cardiac"]


# ----------------------------------------------------------------------------
# shuffle
# ----------------------------------------------------------------------------
def shuffle_seed():
    return DB["shuffle"]["seed"]["value"]


def lock_manifest():
    """Auditable dump: every locked input with grade + provenance, and zero inline magic."""
    rs = DB["real_sequences"]
    return {
        "db_path": DB_PATH,
        "G1_material": {
            "nn_dG_dimers": len(nn_dG()),
            "grade": DB["nn_stacking_dG_kcal_per_mol"]["grade"],
            "provenance": DB["nn_stacking_dG_kcal_per_mol"]["provenance"],
        },
        "G2_regulatory": {
            "cardiac_motifs": list(cardiac_motifs().keys()),
            "grade": DB["cardiac_tf_grammar"]["grade"],
            "provenance": DB["cardiac_tf_grammar"]["provenance"],
        },
        "real_sequences": {
            k: {"tissue": rs[k]["tissue"], "len": rs[k]["length"],
                "accession": rs[k]["accession"], "coords": rs[k]["coords"]}
            for k in sequence_keys()
        },
        "shuffle": {
            "seed": shuffle_seed(),
            "grade": DB["shuffle"]["grade"],
            "provenance": DB["shuffle"]["provenance"],
        },
        "inline_magic_numbers": 0,
    }
