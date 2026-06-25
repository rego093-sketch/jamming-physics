# -*- coding: utf-8 -*-
"""
tissue.shape -- the SHAPE projection of the tissue field c(x): the "WHAT FORM" channel.

Exact tissue analogue of the cell-level A4 coordinate. At the cell level A4 is
built by taking the stiffness signal and SUBTRACTING ITS OWN MEDIAN (robust_z),
i.e. removing the very number that IS gamma -- so "gamma in A4" is impossible; A4
is, by construction, the part gamma is not. Here the tissue SHAPE is built by the
IDENTICAL robust_z applied to the morphogen field c(x): it removes the LEVEL and
keeps the form -- where the gradient rises, dips, and where the TERRITORY
BOUNDARIES (the cliffs / the tissue's "anchors") sit. So the tissue LEVEL is not
inside the tissue SHAPE either: they are the level and shape of ONE morphogen
field, two orthogonal projections (proven in tissue.orthogonality).

robust_z is byte-identical to key_pipeline_full.robust_z (the cell-level engine):
    z = (x - median(x)) / (1.4826 * max(MAD, eps))
This is deliberate: the SAME operator that defines A4 from s(x) defines the tissue
SHAPE from c(x). The level/shape split is one idea applied at two scales.

Territory boundaries are EXACT (closed-form threshold crossings of c(x)), NOT the
old coarse-grid sub-grid interpolation. The French-flag partition is recovered
exactly; the negative size-allometry mechanism falls out with no fitted fraction.
"""
import math
import numpy as np

from . import lock, field

_EPS = 1e-9   # identical role to key_pipeline_full.LOCK['eps']


# ----------------------------------------------------------------------------
# robust_z -- the SAME operator that builds A4 at the cell level
# ----------------------------------------------------------------------------
def robust_z(x, eps=_EPS):
    """Median-removed, MAD-scaled signal. Byte-identical to the cell-level
    key_pipeline_full.robust_z. This is the operator that REMOVES the level."""
    x = np.asarray(x, dtype=np.float64)
    m = np.median(x)
    d = np.median(np.abs(x - m))
    return (x - m) / (1.4826 * max(d, eps))


# ----------------------------------------------------------------------------
# the SHAPE of the planar morphogen field
# ----------------------------------------------------------------------------
def planar_shape(L_um, n_samples=4001, lam_um=None):
    """The mean-removed SHAPE of the morphogen profile over [0, L].
    Returns (x grid, robust_z of c). Carries the form; the level is gone."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    xs = np.linspace(0.0, L_um, n_samples)
    c = field.planar_profile(xs, L_um, lam_um)
    return xs, robust_z(c)


# ----------------------------------------------------------------------------
# territories (French-flag) -- EXACT boundaries, the tissue's "anchors"
# ----------------------------------------------------------------------------
def territory_thresholds(theta=None, k=4):
    """Geometric ladder theta, theta^2, ... -> equal-width territories of width
    lambda*ln(1/theta) in the far field. theta is the ONE modelling choice [F];
    the widths are physics."""
    if theta is None:
        theta, _, _ = lock.territory_theta()
    return [theta ** (i + 1) for i in range(k)]


def territory_boundaries(L_um, theta=None, k=4, lam_um=None):
    """Exact axial boundaries of the nested territories: each is the closed-form
    crossing  x_k = L - lambda*acosh(theta_k * cosh(L/lambda))  of the morphogen
    field. These are the tissue SHAPE's ANCHORS -- the cliffs where one territory
    ends and the next begins, mirroring A4's shell-boundary anchors. Exact, not
    a coarse-grid readout."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    thr = territory_thresholds(theta, k)
    return [round(field.planar_threshold_crossing(t, L_um, lam_um), 6) for t in thr]


def territory_volume_fracs(L_um, theta=None, k=4, lam_um=None):
    """3-D volume fraction of each band {theta_k <= c < theta_{k-1}}. For the
    separable full-face geometry the field depends only on x, so a volume fraction
    equals the axial LENGTH fraction of that band -- computed EXACTLY from the
    closed-form boundaries (no voxel counting, no grid)."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    thr = [1.0] + territory_thresholds(theta, k)
    bnds = [0.0] + [field.planar_threshold_crossing(t, L_um, lam_um) for t in thr[1:]]
    fr = []
    for i in range(len(thr) - 1):
        x_hi = bnds[i]            # outer edge of band i (higher c)
        x_lo = bnds[i + 1]        # inner edge (lower c)
        fr.append(round((x_lo - x_hi) / L_um, 6))
    return fr


def apical_axial_frac(L_um, theta=None, lam_um=None):
    """Fraction of the domain occupied by the leading (apical) territory of fixed
    physical width up to the theta crossing. Fixed width / growing L -> falls."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    if theta is None:
        theta, _, _ = lock.territory_theta()
    return field.planar_threshold_crossing(theta, L_um, lam_um) / L_um


# ----------------------------------------------------------------------------
# emergent negative allometry of FORM -- mechanism, exact, no fitted fraction
# ----------------------------------------------------------------------------
def form_allometry(devtimes, theta=None, lam_um=None):
    """Apical-territory axial fraction vs domain length over developmental time.
    A FIXED lambda in a growing domain => the leading territory's body-fraction
    FALLS. Returns the fitted exponent (expected ~ -1). The domain grows by the
    LEVEL channel's universal rule; the fraction is a SHAPE readout -- the two
    channels meeting only through the shared field, never fitted to each other."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    if theta is None:
        theta, _, _ = lock.territory_theta()
    from .level import domain_length_um
    Ls, fr = [], []
    for t in devtimes:
        L = domain_length_um(t, lam_um)
        Ls.append(L)
        fr.append(apical_axial_frac(L, theta, lam_um))
    e = np.polyfit(np.log(Ls), np.log(fr), 1)[0]
    return dict(L_um=[round(x, 3) for x in Ls],
                apical_axial_frac=[round(x, 6) for x in fr],
                frac_vs_L_exponent=round(float(e), 4))


# ----------------------------------------------------------------------------
# the SHAPE read of a single tissue
# ----------------------------------------------------------------------------
def read_shape(L_um, theta=None, k=4, lam_um=None):
    """The complete SHAPE reading of one tissue domain: the territory boundaries
    (anchors), per-territory volume fractions, apical fraction. All exact closed
    form. Carries the form; the level is removed (that is what makes it SHAPE)."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    if theta is None:
        theta, _, _ = lock.territory_theta()
    bnds = territory_boundaries(L_um, theta, k, lam_um)
    fr = territory_volume_fracs(L_um, theta, k, lam_um)
    width = lam_um * math.log(1.0 / theta)
    n_terr = int(L_um // width)
    return {
        "theta": theta,
        "territory_boundaries_um": bnds,
        "territory_volume_fracs": fr,
        "n_territories": n_terr,
        "apical_width_um": round(width, 6),
        "apical_axial_frac": round(apical_axial_frac(L_um, theta, lam_um), 8),
        "level_removed": True,       # SHAPE = field with the LEVEL taken out
        "closed_form": "x_k = L - lambda*acosh(theta_k*cosh(L/lambda))",
        "grade_form": "[V] exact (precision)",
        "grade_form_vs_real_anatomy": "[O] needs measured enhancer-promoter "
                                      "contact (Hi-C/Micro-C/capture-C) or a "
                                      "tissue-territory boundary map",
    }
