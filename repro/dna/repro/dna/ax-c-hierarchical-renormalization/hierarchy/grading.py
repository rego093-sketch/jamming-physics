# -*- coding: utf-8 -*-
"""
hierarchy.grading -- the honest per-channel grade ledger for the hierarchical
scale-renormalization interpreter.

It enforces the single distinction the whole handover is built on:
    PRECISION (정밀): how exactly/reproducibly the engine computes ITS OWN formula.
    ACCURACY  (정확): how closely that formula matches an INDEPENDENT measurement.

Every [V] below means "reproduces bit-for-bit / exact closed form / exact theorem"
-- it is PRECISION, not a match to a measurement. The channels that would be
ACCURACY (the ABSOLUTE modulus of a real cell/tissue/organ; the REAL per-rung
packing fraction) are graded [O] with the EXACT missing dataset named -- never
quietly claimed as accurate (prohibition B1).

This module computes nothing physical; it is the contract that the interpreter and
the gate both read, so the grades are declared in ONE place and cannot drift
between the code and the prose.

THE KEY HONESTY OF THIS APPENDIX:
  The MACHINERY of the tower -- the density law rho'=phi*rho, the exact Voigt/Reuss
  bracket, the wave-speed softening ratio c'/c = sqrt(J), and the fact that R
  composes (renormalization-group semigroup) -- is EXACT [V]. The rigidity ONSET
  shape sqrt((phi-phi_c)/(1-phi_c)) is [L]-grounded (a composition of two cited
  universals). What is NOT claimed is any ABSOLUTE biological modulus: that needs a
  measured elastography/AFM atlas and measured per-rung stereology, both named [O].
  So the climb is precision-exact and the accuracy is honestly open.
"""

GRADE_MEANINGS = {
    "[L]": "locked: independently measured / universal law / exact theorem, cited; "
           "legitimate input",
    "[V]": "verified: exact closed form / theorem / bit-for-bit reproducible "
           "(PRECISION, not a measurement match)",
    "[F]": "fixed modelling choice (functional form / generic central value); declared",
    "[O]": "open: precision-exact but NO independent measurement compared yet; the "
           "specific missing dataset is named",
}


# the per-channel grade ledger -- the renormalization-tower mirror of the
# cell-level and tissue-level tables
LEDGER = [
    {
        "channel": "density renormalization  rho' = phi * rho",
        "grade": "[V]",
        "basis": "exact: void carries no mass, so aggregate density is the packing "
                 "fraction times the unit density; mass/volume conservation. "
                 "Deterministic, bit-for-bit.",
        "kind": "precision",
    },
    {
        "channel": "exact composite bounds  B_Reuss = 0,  B_Voigt = phi * B_unit",
        "grade": "[V]",
        "basis": "exact elastic-mixture THEOREMS (Reuss 1929 isostress lower; Voigt "
                 "1889 isostrain upper) with a void phase B_void=0; evaluated exactly. "
                 "The effective modulus is GUARANTEED inside this bracket.",
        "kind": "precision",
    },
    {
        "channel": "wave-speed softening ratio per rung  c'/c = sqrt(J(phi))",
        "grade": "[V]",
        "basis": "exact: the VP master relation c^2=B/rho applied at both levels gives "
                 "c'/c = sqrt(B'/B * rho/rho') = sqrt(phi*J / phi) = sqrt(J). "
                 "Deterministic closed form.",
        "kind": "precision",
    },
    {
        "channel": "renormalization-group composition (R∘R associativity)",
        "grade": "[V]",
        "basis": "exact: climbing two rungs equals one combined rung to < 1e-9 "
                 "(semigroup property); the ladder is a consistent RG flow.",
        "kind": "precision",
    },
    {
        "channel": "monotone wave-speed softening up the tower (uniform phi)",
        "grade": "[V]",
        "basis": "exact RG theorem of the idealized ladder: J<1 for every phi<1, so "
                 "c strictly decreases each rung. Holds for any phi<1 with no ECM "
                 "stiffening; that proviso is stated.",
        "kind": "precision",
    },
    {
        "channel": "rigidity-onset shape  J(phi) = sqrt((phi-phi_c)/(1-phi_c))",
        "grade": "[L]",
        "basis": "the SHAPE is the composition of two CITED universals: excess "
                 "coordination Delta_z ~ (phi-phi_c)^(1/2) (O'Hern 2003) and rigidity "
                 "G ~ Delta_z (Wyart 2005). Not a free choice; read from the locked DB.",
        "kind": "grounded",
    },
    {
        "channel": "jamming anchors  phi_c, z_iso=2d, onset exponent 1/2",
        "grade": "[L]",
        "basis": "independently published universals (O'Hern-Silbert-Liu-Nagel 2003; "
                 "Maxwell isostatic counting; Wyart-Nagel-Witten 2005), read from the "
                 "locked DB; no fit.",
        "kind": "grounded",
    },
    {
        "channel": "RG-ladder framing (repeated coarse-graining of jammed units)",
        "grade": "[L]",
        "basis": "the jamming transition admits a renormalization-group / scaling "
                 "description (Goodrich-Liu-Sethna 2016) and applies to CELL packings "
                 "(Bi-Lopez-Schwarz-Manning 2015); grounds the ladder construction.",
        "kind": "grounded",
    },
    {
        "channel": "orthogonality  mechanical LEVEL ⟂ SHAPE",
        "grade": "[V]",
        "basis": "SHAPE = robust_z(B(x)) is invariant under both LEVEL moves (field "
                 "scale, uniform stiffness offset) to machine epsilon (analytic) + "
                 "geometry moves SHAPE (numeric). Same robust_z as cell-level A4.",
        "kind": "precision",
    },
    {
        "channel": "scale classification ledger (every channel tagged L0..L4)",
        "grade": "[L]",
        "basis": "a declaration, not a computed quantity: each corpus reading channel "
                 "is tagged with the structural level it reads and how it connects to "
                 "the tower. Carries no fitted number; exists so scale cannot drift.",
        "kind": "grounded",
    },
    {
        "channel": "per-rung packing fraction profile phi_k (demonstration climb)",
        "grade": "[F]",
        "basis": "a documented jammed profile (all phi in (phi_c,1)) standing in for "
                 "measured per-rung stereology; the operator is GENERAL in phi -- "
                 "measured fractions change only the numbers, not the machinery.",
        "kind": "choice",
    },
    {
        "channel": "ladder length scales L0..L4 (cell~10um, tissue~100um, ...)",
        "grade": "[F]",
        "basis": "generic textbook orders of magnitude, used ONLY to count "
                 "units-per-rung (a reported volume ratio); the dimensionless flow "
                 "does not depend on them at all.",
        "kind": "choice",
    },
    {
        "channel": "ABSOLUTE modulus at each biological level (B in Pa)",
        "grade": "[O]",
        "basis": "ACCURACY untested. The single-unit modulus is a generic placeholder "
                 "and sets absolute magnitude only; the engine does NOT compare to a "
                 "measured modulus (that would be back-fit).",
        "kind": "accuracy_open",
        "named_obstacle": "measured per-scale modulus atlas (elastography MRE/USE, AFM "
                          "nanoindentation, micro-rheology) across cell -> tissue -> organ",
    },
    {
        "channel": "REAL per-rung packing fraction phi(level)",
        "grade": "[O]",
        "basis": "ACCURACY untested. The demonstration phi profile is a modelling "
                 "choice; the real per-level cell packing fraction is unmeasured here.",
        "kind": "accuracy_open",
        "named_obstacle": "measured cell packing fraction at each level by confocal/EM "
                          "stereology (and ECM volume fraction)",
    },
    {
        "channel": "REAL monotonicity vs ECM stiffening (cartilage, bone)",
        "grade": "[O]",
        "basis": "ACCURACY untested. The idealized flow softens monotonically; real "
                 "extracellular-matrix mineralization can RAISE the unit modulus and "
                 "break monotonicity. Not modelled; flagged as the named obstacle.",
        "kind": "accuracy_open",
        "named_obstacle": "per-tissue ECM / mineralization stiffness contribution "
                          "(e.g. measured cartilage/bone modulus vs cell modulus)",
    },
]


def precision_channels():
    return [e for e in LEDGER if e["kind"] == "precision"]


def grounded_channels():
    return [e for e in LEDGER if e["kind"] == "grounded"]


def open_accuracy_channels():
    return [e for e in LEDGER if e["kind"] == "accuracy_open"]


def declared_grades():
    """All grade symbols this interpreter uses -- the gate checks they are exactly
    the four sanctioned ones and that each carries a basis string."""
    return sorted({e["grade"] for e in LEDGER})


def completion_status():
    """The earned-completion test (handover 04): complete IFF every readable channel
    is either ACCURATE (a number landed on a measurement) or HONESTLY BOUNDED
    (precision-exact + named [O] obstacle). Here, three channels are still [O]
    (absolute modulus, real per-rung phi, ECM monotonicity) -> NOT complete; the
    precision is real, the accuracy work is named. We say so plainly (no false
    victory)."""
    open_ch = open_accuracy_channels()
    return {
        "complete": False,
        "reason": "the renormalization MACHINERY is precision-exact ([V]) and the "
                  "rigidity onset is [L]-grounded, but the ABSOLUTE biological moduli "
                  "and the REAL per-rung packing fractions are accuracy-untested [O]; "
                  "named obstacles below. Precision (정밀) is earned; accuracy (정확) "
                  "is not yet claimed.",
        "open_channels": [{"channel": e["channel"],
                           "named_obstacle": e["named_obstacle"]} for e in open_ch],
        "what_would_close_it": "supply the named measured datasets (per-scale modulus "
                               "atlas + per-rung stereology + ECM contribution), feed "
                               "the measured phi profile and B0 into the SAME operator, "
                               "compare the predicted softening trajectory to a measured "
                               "elastography ladder with a shuffle control, pre-register "
                               "the sign; then and only then mark 정확.",
    }
