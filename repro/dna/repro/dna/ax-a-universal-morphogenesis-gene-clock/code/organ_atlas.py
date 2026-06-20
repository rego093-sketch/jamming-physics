"""
organ_atlas.py -- INTERNAL (visceral) organ emergence as a gene-clock readout (v10).

The existing package grows the EXTERNAL form (face/body/skeleton) and the COMPOSITION
axis (adipose) from measured gamma. What was missing for a complete "DNA -> body" arc is
the INTERNAL organs: in assemble.anatomy_spec they exist only as hand-placed ellipsoids that
"inherit the switch decisions" geometrically. This module gives each visceral organ its own
master gene, so the ORDER and relative timing of organ appearance fall out of the SAME R19
gene clock that already drives the face features -- internal organogenesis as heterochrony,
a deterministic readout of measured gamma, not a hand-set sequence.

WHAT THIS MODULE CLAIMS (and does not):
  * [V] the emergence ORDER of the visceral organs is a pure measured-gamma readout
        (order == argsort(spinodal(gamma))); perturb a gamma and the order resorts. This is the
        same spinodal-ordering mechanism the kit already uses for the face and (in neuro ch17)
        for the spinal ventral->dorsal order -- here in the TIME axis, for internal organs.
  * [F] the gene -> organ map (master genes), the sign convention (higher spinodal -> later),
        and the absolute tau window: forced modelling choices, documented per organ.
  * [O] whether this DNA-derived order MATCHES real organogenesis timing is NOT asserted here;
        it is TESTED separately in organ_timing.py against locked Carnegie stages, and (as the
        v5-v8 dev-timing line already established for external features) it does NOT match --
        promoter stiffness is not the molecular correlate of organ timing. organ_timing.py
        reports that honest null; this atlas only produces the deterministic schedule.
  * [O] organ SIZE, SHAPE and 3D placement from dwell: only relative dwell is given here; the
        coupling of this schedule into the actual Layer-2 anatomy volume fill (assemble.
        anatomy_spec) is the documented next step (see HANDOFF), not claimed in v10.

gamma is READ-ONLY, fetched by the identical NCBI->SantaLucia pipeline (data/organ_gamma.json),
never fitted. stdlib + numpy. Deterministic.
"""
import os, json
import numpy as np
import gene_clock as GC

HERE = os.path.dirname(os.path.abspath(__file__))
ORGAN_GAMMA_JSON = os.path.join(HERE, "data", "organ_gamma.json")

# ---------------------------------------------------------------------------------------------
# The visceral organ -> master gene map. grade is the gene->organ-master confidence.
# anat_label links to assemble.TIS / anatomy_spec so the next session can wire the schedule into
# the existing Layer-2 organ ellipsoids (heart/lung/liver/gut already exist there; the rest are
# the new organs this module introduces).
# (organ_feature, master_gene, grade, anat_label, note)
# ---------------------------------------------------------------------------------------------
ORGAN_MASTERS = [
    ("heart_tube",            "NKX2-5", "[V]", "heart", "cardiac master; cardiogenic plate -> heart tube"),
    ("hepatic_diverticulum",  "HHEX",   "[V]", "liver", "liver-bud specifier (also thyroid/forebrain: noted)"),
    ("gastric_dilation",      "BARX1",  "[V]", "gut",   "gastric mesenchyme master (stomach; new organ vs anat 'gut')"),
    ("lung_bud",              "NKX2-1", "[V]", "lung",  "lung/thyroid master (TTF1); respiratory diverticulum"),
    ("dorsal_pancreatic_bud", "PDX1",   "[V]", "gut",   "pancreatic master (new organ; budding off foregut)"),
    ("metanephric_cap",       "SIX2",   "[V]", "gut",   "metanephric nephron-progenitor master (kidney; new organ)"),
    ("splenic_primordium",    "TLX1",   "[V]", "gut",   "spleen master (HOX11; new organ in dorsal mesogastrium)"),
    # midgut/intestine: [V] master but SOFT first-appearance staging -> in the atlas (geometry)
    # but EXCLUDED from the locked organ_timing.json test (see organ_timing.json _scope_note).
    ("midgut_intestine",      "CDX2",   "[V]", "gut",   "posterior-gut/intestine master; SOFT staging, atlas-only"),
]

# the subset whose staging is crisp enough for the locked timing test (mirrors organ_timing.json)
TIMING_ORGANS = [t for t in ORGAN_MASTERS if t[0] != "midgut_intestine"]


def load_organ_gamma(path=None):
    """Load the measured visceral-organ master gamma table. Returns ({gene: gamma}, provenance)."""
    p = path or ORGAN_GAMMA_JSON
    J = json.load(open(p, encoding="utf-8"))
    return {k: float(v["gamma"]) for k, v in J["genes"].items()}, J.get("_provenance", "")


def organ_schedule(include_midgut=True):
    """Build the gene-clock emergence schedule for the visceral organs (PURE gamma readout).

    Returns the gene_clock.feature_schedule dict (per-organ gamma/spinodal/tau_on/dwell/a(tau),
    the derived emergence order, and the order_is_gamma_readout self-check). The order is
    argsort(spinodal(gamma)); change a gamma and it resorts -- no hand-typed order.
    """
    gammas, _ = load_organ_gamma()
    masters = ORGAN_MASTERS if include_midgut else TIMING_ORGANS
    feature_genes = [(organ, gene) for organ, gene, _, _, _ in masters]
    return GC.feature_schedule(feature_genes, gammas)


def schedule_rows(include_midgut=True):
    """Compact printable rows in emergence order: organ, gene, grade, gamma, spinodal, tau_on, dwell."""
    sched = organ_schedule(include_midgut=include_midgut)
    meta = {organ: (gene, grade, note) for organ, gene, grade, _, note in ORGAN_MASTERS}
    rows = []
    for organ in sched["order"]:
        d = sched["features"][organ]
        gene, grade, _ = meta[organ]
        rows.append((organ, gene, grade, d["gamma"], d["spinodal"], d["tau_on"], d["dwell"]))
    return rows, sched["order_is_gamma_readout"]


def assert_one_switch(tol=1e-12):
    """The organ gene clock uses the SAME R19 fold as the body engine (proof at run time)."""
    return GC.assert_one_switch(tol=tol)


def _fmt():
    rows, readout = schedule_rows(include_midgut=True)
    L = ["=" * 82,
         "  INTERNAL (VISCERAL) ORGAN EMERGENCE  |  gene-clock readout of measured gamma",
         "=" * 82,
         f"  {'organ':22s} {'gene':7s} {'gr':3s} {'gamma':>7s} {'spinodal':>9s} {'tau_on':>7s} {'dwell':>7s}"]
    for organ, gene, grade, g, sp, t, dw in rows:
        L.append(f"  {organ:22s} {gene:7s} {grade:3s} {g:7.4f} {sp:9.5f} {t:7.4f} {dw:7.4f}")
    L.append("-" * 82)
    L.append(f"  DNA-derived emergence order (earliest -> latest):")
    L.append("    " + " < ".join(r[0] for r in rows))
    L.append(f"  order_is_gamma_readout (order == argsort(spinodal)) : {readout}")
    L.append(f"  one-switch (organ fold == body fold) max|delta|     : {assert_one_switch():.2e}")
    L.append("=" * 82)
    L.append("  NOTE: whether this order matches real organogenesis timing is TESTED, not assumed,")
    L.append("        in organ_timing.py (locked Carnegie stages). Per the dev-timing line it is a")
    L.append("        measured [O] null -- promoter stiffness is not the organ-timing correlate.")
    return "\n".join(L)


if __name__ == "__main__":
    print(_fmt())
