# -*- coding: utf-8 -*-
"""
completion.lock -- the LOCKED constant surface for the grammar-completion interpreter
(Appendix F).

Reads every input from param_db.json: the three ORGAN TF grammars (cardiac/neural/hepatic
consensus motifs), the nine REAL human promoter sequences (the organ atlas), the HOXD
cluster coordinates and AP body ranks (the G5 body-plan colinearity), the nearest-neighbour
stacking parameters (the material signal for G1/G4 orthogonality), and the declared analysis
settings (shuffle seed, shuffle count, CpG window, gate thresholds). Zero inline magic
numbers; every value carries a grade and provenance. Add-only: the cardiac grammar and the
three Appendix E sequences are re-locked unchanged.
"""
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_DB_PATH = os.path.join(_HERE, "..", "param_db.json")


def _load_db():
    if not os.path.exists(_DB_PATH):
        raise FileNotFoundError(
            "param_db.json not found. The completion engine refuses to invent sequences, "
            "motifs, coordinates, or thresholds; place the locked DB next to it."
        )
    with open(_DB_PATH, encoding="utf-8") as fh:
        return json.load(fh), os.path.relpath(_DB_PATH, _HERE)


DB, DB_PATH = _load_db()


# ----------------------------------------------------------------------------
# organ TF grammars (G2 generalized -- the atlas)
# ----------------------------------------------------------------------------
def organ_names():
    """The organ classes that have a grammar (cardiac, neural, hepatic)."""
    return [k for k in DB["organ_grammars"]
            if not k.startswith("_") and k != "grade"]


def organ_grammar(organ):
    """Consensus IUPAC motif set {name: regex} for one organ. [L]."""
    return dict(DB["organ_grammars"][organ]["motifs_IUPAC"])


def organ_grammars():
    """All organ grammars {organ: {name: regex}}."""
    return {o: organ_grammar(o) for o in organ_names()}


# ----------------------------------------------------------------------------
# atlas promoters (real human sequences)
# ----------------------------------------------------------------------------
def promoter_keys():
    return [k for k in DB["atlas_promoters"]
            if not k.startswith("_") and k != "grade"]


def promoter(key):
    """A real promoter (seq, organ, provenance) by key."""
    e = DB["atlas_promoters"][key]
    return e["seq"], e["organ"], e["provenance"]


def promoter_organ(key):
    return DB["atlas_promoters"][key]["organ"]


def organ_promoter_keys(organ):
    return [k for k in promoter_keys() if promoter_organ(k) == organ]


def control_keys():
    """The housekeeping (tissue-neutral) control promoter(s)."""
    return [k for k in promoter_keys() if promoter_organ(k) == "housekeeping"]


# ----------------------------------------------------------------------------
# HOXD colinearity (G5 body-plan)
# ----------------------------------------------------------------------------
def hox_genes():
    """Ordered HOXD genes with {accession, tss, ap_body_rank}. Order is the DB order
    (anterior HOXD1 ... posterior HOXD13). [L]."""
    return dict(DB["hox_colinearity"]["genes"])


def hox_order():
    return list(DB["hox_colinearity"]["genes"].keys())


def hox_tss_and_rank():
    """(list of TSS, list of AP body rank) in gene order."""
    g = DB["hox_colinearity"]["genes"]
    keys = list(g.keys())
    return [g[k]["tss"] for k in keys], [g[k]["ap_body_rank"] for k in keys]


# ----------------------------------------------------------------------------
# material (G1/G4 orthogonality reference)
# ----------------------------------------------------------------------------
def nn_dG():
    """SantaLucia 1998 NN Delta-G_37 table {dimer: kcal/mol}. [L] (re-locked from App. E)."""
    return dict(DB["nn_stacking_dG_kcal_per_mol"]["values"])


# ----------------------------------------------------------------------------
# declared settings
# ----------------------------------------------------------------------------
def shuffle_seed():
    return DB["settings"]["shuffle_seed"]["value"]


def atlas_nshuf():
    return DB["settings"]["atlas_nshuf"]["value"]


def cpg_window_bp():
    return DB["settings"]["cpg_window_bp"]["value"]


def control_quiet_z_max():
    return DB["settings"]["control_quiet_z_max"]["value"]


def g4_orthogonality_corr_max():
    return DB["settings"]["g4_orthogonality_corr_max"]["value"]


def g5_colinearity_corr_min():
    return DB["settings"]["g5_colinearity_corr_min"]["value"]


# ----------------------------------------------------------------------------
# manifest
# ----------------------------------------------------------------------------
def lock_manifest():
    """Auditable dump: every locked input with grade + provenance, zero inline magic."""
    og = DB["organ_grammars"]
    ap = DB["atlas_promoters"]
    hx = DB["hox_colinearity"]
    return {
        "db_path": DB_PATH,
        "organ_grammars": {
            o: {"motifs": list(organ_grammar(o).keys()),
                "grade": og[o]["grade"], "provenance": og[o]["provenance"]}
            for o in organ_names()
        },
        "atlas_promoters": {
            k: {"organ": ap[k]["organ"], "len": ap[k]["length"],
                "accession": ap[k]["accession"], "coords": ap[k]["coords"]}
            for k in promoter_keys()
        },
        "hox_colinearity": {
            "genes": list(hx["genes"].keys()),
            "grade": hx["grade"], "provenance": hx["provenance"],
        },
        "nn_dG_dimers": len(nn_dG()),
        "settings": {
            "shuffle_seed": shuffle_seed(),
            "atlas_nshuf": atlas_nshuf(),
            "cpg_window_bp": cpg_window_bp(),
            "control_quiet_z_max": control_quiet_z_max(),
            "g4_orthogonality_corr_max": g4_orthogonality_corr_max(),
            "g5_colinearity_corr_min": g5_colinearity_corr_min(),
        },
        "inline_magic_numbers": 0,
    }
