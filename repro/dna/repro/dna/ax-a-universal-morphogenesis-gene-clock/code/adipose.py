"""
adipose.py -- Layer 4: ADIPOSE / ENERGY-BALANCE MORPHOLOGY.

The DNA gene clock (Layer 3 perp DNA) makes the ORDER and TIMING of feature appearance a
readout of measured gamma. But the single largest source of variation in a real individual's
external form -- the same genome looking lean vs heavy, in the FACE and the BODY -- is body
COMPOSITION, i.e. adipose deposition. This layer adds exactly that axis, with no HPC and no
learned data: it is an analytic deformation field driven by

    (1) MEASURED obesity-gene gamma  (the same NCBI -> SantaLucia-NN pipeline; [L], never fitted)
    (2) an ENERGY-BALANCE dial E      (chronic caloric surplus(+)/deficit(-); an INPUT, not fitted)
    (3) an anatomical DEPOT map        (WHERE fat sits; sex/pattern-influenced; geometry is [F])

ONE SWITCH, AGAIN.  An adipocyte's "store vs mobilize" set-point is bistable with hysteresis (a
defended fat set-point). We model it with the SAME R19 fold that writes DNA, fires neurons, folds
the body and schedules the face:
      setpoint(drive) = map( settle_field(gamma, h(drive), s_prev=lean) )
the identical morpho_core.settle_field / spinodal primitive. assert_one_switch_adipose() proves
it at run time (< 1e-12). So adiposity is NOT a bolt-on: it is the time clock's twin in the
COMPOSITION axis -- the face clock turns a smooth temporal drive into a crisp feature onset;
the fat clock turns a smooth energy drive into a defended storage set-point.

GENE x ENVIRONMENT (the user's point: "obesity genes also matter, human or animal").  The fold's
drive is  drive = k_E * E + P_geno(measured obesity gamma).  A high-propensity ("thrifty") genome
shifts the set-point so the fold flips to STORE at LOWER E -- it gains readily; a lean/thermogenic
genome resists. P_geno is a deterministic readout of measured gamma (perturb a gamma -> propensity
moves in the annotated direction: propensity_is_gamma_readout), exactly as the emergence ORDER is.

WHAT IS MEASURED vs FORCED (neuro VP-SPEC C3 discipline -- every quantity graded):
  [L] obesity-gene gamma: mean(-NN dG37), SantaLucia 1998, read verbatim from NCBI promoters.
  [V] the adipose fold == the body fold == the neuro fold (asserted < 1e-12).
  [V] (derived) total adipose volume is MONOTONE in E and in genome propensity, and propensity is
      a readout of measured gamma -- falsifiable, not tuned.
  [F] the SIGN of each gene's adipose effect (pro-storage vs satiety/thermogenic); the depot
      geometry; the max subcutaneous thickness t_max; the energy window; android/gynoid default.
  [O] absolute fat mass in kg, real BMI calibration, and matching a specific person's depot
      pattern need anthropometric data we do NOT fit here (only the index + the laws are claimed).

stdlib + numpy (+ scipy/skimage only for meshing, reused from the package). Deterministic.
"""
import os, json, math
import numpy as np
import morpho_core as mc          # the in-package R19 fold (single source for the body engine)
import gene_clock as GC           # spinodal (same fold), measured gamma loader

HERE = os.path.dirname(os.path.abspath(__file__))
OBESITY_JSON = os.path.join(HERE, "data", "obesity_gamma.json")


# ===================================================================== R19 adipose fold
def spinodal(g):
    """The SAME switch as gene_clock.spinodal and morpho_core.spinodal (2*(g/3)^1.5)."""
    return 2.0 * (g / 3.0) ** 1.5


def adipose_setpoint(gamma, drive, slope=1.5, a0=0.55):
    """Defended fat SET-POINT fraction (RAW, ~[0,1]) as a readout of the R19 fold.

    The adipocyte reads an energy/genome `drive` through ITS OWN bistable fold (started from the
    LEAN basin). The drive enters as h = spinodal * (a0 + slope*drive), so h crosses +spinodal at
    drive_flip = (1-a0)/slope: BELOW that the LEAN basin still exists and -- because we start in
    it -- the set-point stays low (defended leanness); AT the flip the lean basin DISAPPEARS and
    the set-point jumps UP (a sharp, hysteretic 'tipping into storage'); ABOVE it the single upper
    branch rises and saturates. This is the SAME construction gene_clock.emergence_curve uses in
    the TIME axis, here in the ENERGY axis -- the face clock's twin.

    Monotone non-decreasing in `drive` (lower branch rises a little -> jumps at the spinodal ->
    upper branch saturates). Genome/energy shift `drive`, so a thrifty genome reaches the flip at
    lower E (gains readily) and a lean genome may never reach it (resists) -- gene x environment.
    """
    drive = np.asarray(drive, float)
    sp = spinodal(gamma)
    h = sp * (a0 + slope * drive)                              # crosses +spinodal at (1-a0)/slope
    s = mc.settle_field(gamma, h, np.full_like(h, -1.0))      # start in the LEAN basin
    a = (s + math.sqrt(gamma)) / (2.0 * math.sqrt(gamma))     # settled state -> ~[0,1]
    return a


def assert_one_switch_adipose(tol=1e-12):
    """Prove the adipose fold uses the SAME spinodal as the body engine (morpho_core)."""
    gs = np.linspace(1.2, 1.8, 121)
    d = max(abs(spinodal(g) - mc.spinodal(g)) for g in gs)
    assert d <= tol, f"adipose spinodal mismatch vs morpho_core: {d}"
    return float(d)


# ===================================================================== measured obesity gamma
def load_obesity_gamma(path=None):
    """Load the measured gamma table that INCLUDES the obesity panel (read-only, never fitted).
    Falls back to the morpho 42-gene table if the obesity fetch has not been run."""
    p = path or OBESITY_JSON
    if not os.path.exists(p):
        g, prov = GC.load_gamma_table()
        return g, prov + " | (obesity panel not fetched; using morpho table)"
    J = json.load(open(p, encoding="utf-8"))
    prov = " | ".join(s for s in [J.get("_provenance", ""), J.get("_provenance_plus", ""),
                                  J.get("_provenance_obesity", "")] if s)
    return {k: float(v["gamma"]) for k, v in J["genes"].items()}, prov


# --------------------------------------------------------------------------------------------
# The OBESITY PANEL with the forced [F] BIOLOGICAL SIGN of each gene's effect on adiposity.
# sign = +1 : pro-storage / orexigenic (more activity -> more fat)
# sign = -1 : satiety / thermogenic / insulin-sensitising (more activity -> less fat)
# This SIGN is an annotation (textbook directionality), NOT measured from a promoter -> grade [F].
# The MAGNITUDE of each gene's pull is its MEASURED spinodal -> so propensity is a gamma readout.
# --------------------------------------------------------------------------------------------
PANEL_SIGN = {
    # pro-storage capacity / orexigenic
    "PPARG": +1, "CEBPA": +1, "LPL": +1, "FTO": +1, "NPY": +1, "AGRP": +1, "GHRL": +1, "INSR": +1,
    # satiety / adipostat / thermogenic
    "MC4R": -1, "LEP": -1, "LEPR": -1, "POMC": -1, "SIM1": -1, "BDNF": -1, "ADIPOQ": -1,
    "ADRB3": -1, "UCP1": -1,
}
PANEL_ROLE = {
    "PPARG": "adipogenesis master", "CEBPA": "adipogenesis master", "LPL": "lipid uptake",
    "FTO": "common-variant adiposity locus", "NPY": "orexigenic", "AGRP": "orexigenic",
    "GHRL": "ghrelin/hunger", "INSR": "insulin/storage",
    "MC4R": "melanocortin satiety", "LEP": "leptin adipostat", "LEPR": "leptin receptor",
    "POMC": "satiety precursor", "SIM1": "hypothalamic satiety", "BDNF": "energy balance",
    "ADIPOQ": "adiponectin", "ADRB3": "lipolysis/thermogenesis", "UCP1": "brown-fat thermogenesis",
}
PANEL_CONF = {  # neuro "representative, cited" labels
    "PPARG": "V", "CEBPA": "V", "LPL": "F", "FTO": "V", "NPY": "V", "AGRP": "V", "GHRL": "V",
    "INSR": "F", "MC4R": "V", "LEP": "V", "LEPR": "V", "POMC": "V", "SIM1": "V", "BDNF": "V",
    "ADIPOQ": "V", "ADRB3": "F", "UCP1": "V",
}

# Genome PRESETS: weightings over the SAME measured panel (choosing WHICH genome to simulate is a
# forced [F] choice, like sex; the gamma values read are identical and measured). 1.0 = baseline.
GENOME_PRESETS = {
    "neutral": {g: 1.0 for g in PANEL_SIGN},
    # "thrifty": emphasise the pro-storage / orexigenic masters (a fat-prone genome)
    "thrifty": {**{g: 1.0 for g in PANEL_SIGN},
                "PPARG": 2.2, "CEBPA": 2.0, "FTO": 2.2, "NPY": 1.8, "AGRP": 1.8, "LPL": 1.6,
                "GHRL": 1.6, "MC4R": 0.5, "LEP": 0.6, "LEPR": 0.6, "UCP1": 0.5, "ADRB3": 0.6},
    # "lean": emphasise the satiety / thermogenic axis (a fat-resistant genome)
    "lean":    {**{g: 1.0 for g in PANEL_SIGN},
                "MC4R": 2.2, "LEP": 2.0, "LEPR": 2.0, "POMC": 1.8, "UCP1": 2.2, "ADRB3": 1.8,
                "ADIPOQ": 1.8, "PPARG": 0.5, "CEBPA": 0.6, "FTO": 0.5, "NPY": 0.6, "AGRP": 0.6},
}


def _panel_drive(gammas, weights):
    """Weighted mean SIGNED spinodal over the obesity panel = the genome's adipostat shift.
    A pure readout of MEASURED gamma (the sign is the only annotation)."""
    num = den = 0.0
    for g, w in weights.items():
        if g not in gammas:
            continue
        z = PANEL_SIGN[g] * spinodal(gammas[g])     # signed measured switch strength
        num += w * z; den += abs(w)
    return num / den if den else 0.0


_CANON_GAMMAS = None
def _canon_gammas():
    """The frozen canonical measured table; the neutral-genome reference drive is taken from it
    so that perturbing a measured gamma genuinely MOVES propensity (the gamma-readout property)."""
    global _CANON_GAMMAS
    if _CANON_GAMMAS is None:
        _CANON_GAMMAS, _ = load_obesity_gamma()
    return _CANON_GAMMAS


def genome_propensity(gammas, genome="neutral", gain=6.0):
    """P_geno in (-1,1): how strongly this genome biases toward STORAGE, relative to a neutral
    (equal-weight) panel on the FROZEN canonical table. >0 thrifty, <0 lean. The neutral genome on
    the canonical table is 0 by construction; bumping a pro-storage gene's measured gamma raises
    it, bumping a satiety gene's gamma lowers it (propensity_is_gamma_readout). Deterministic."""
    weights = GENOME_PRESETS.get(genome, genome) if not isinstance(genome, dict) else genome
    D = _panel_drive(gammas, weights)
    D_ref = _panel_drive(_canon_gammas(), GENOME_PRESETS["neutral"])   # FROZEN canonical reference
    return float(math.tanh(gain * (D - D_ref)))


def propensity_is_gamma_readout(gammas, bump=0.05):
    """Falsifiable self-check: raising a PRO-storage gene's measured gamma must RAISE propensity,
    and raising a SATIETY gene's gamma must LOWER it. Returns (ok, detail)."""
    base = genome_propensity(gammas, "neutral")
    g_pro = dict(gammas); g_pro["PPARG"] = gammas["PPARG"] + bump      # pro-storage up
    g_sat = dict(gammas); g_sat["MC4R"] = gammas["MC4R"] + bump        # satiety up
    p_pro = genome_propensity(g_pro, "neutral")
    p_sat = genome_propensity(g_sat, "neutral")
    ok = (p_pro > base) and (p_sat < base)
    return ok, dict(base=base, pro_bump=p_pro, sat_bump=p_sat)


# ===================================================================== the adipose model
class AdiposeModel:
    """Turns (energy E, genome) into a scalar adipose ACTIVATION alpha in [0,1] through the fold,
    using a representative adipogenic-master stiffness (PPARG -- the genuine differentiation
    master; using its gamma as the fold stiffness is the [F] modelling choice, its value is [L]).

    ENERGY CONVENTION: E is chronic surplus ABOVE weight maintenance. alpha is floor-subtracted so
    that the LEAN REFERENCE (neutral genome at E = E_lean) gives alpha = 0 exactly -- the inflated
    surface then equals the lean target there, so the package's headline convergence proof at the
    lean baseline is preserved untouched. Surplus (E>0) and/or a thrifty genome raise alpha."""

    def __init__(self, gammas=None, fold_gene="PPARG", k_E=1.0, slope=1.5, a0=0.55, E_lean=-1.0):
        if gammas is None:
            gammas, _ = load_obesity_gamma()
        self.gammas = gammas
        self.fold_gene = fold_gene
        self.gamma_adipo = float(gammas[fold_gene])      # [L] measured stiffness of the fat fold
        self.k_E = float(k_E)
        self.slope = float(slope)
        self.a0 = float(a0)
        self.E_lean = float(E_lean)
        assert_one_switch_adipose()                      # the fat fold IS the body fold
        # lean floor: RAW fold readout for the neutral genome at the lean reference energy
        d_floor = self.k_E * self.E_lean + genome_propensity(self.gammas, "neutral")
        self._floor = float(adipose_setpoint(self.gamma_adipo, d_floor, self.slope, self.a0))

    def propensity(self, genome="neutral"):
        return genome_propensity(self.gammas, genome)

    def drive(self, E, genome="neutral"):
        """Total fold drive = environment tilt + genome tilt (gene x environment)."""
        return self.k_E * float(E) + self.propensity(genome)

    def activation(self, E, genome="neutral"):
        """alpha in [0,1]: how 'switched-on' adipose storage is, scalar over the body.
        Monotone in E and in propensity; 0 at the lean reference (baseline preserved); the
        defended-set-point readout of the fold (sharp 'tipping' once drive crosses the spinodal)."""
        raw = float(adipose_setpoint(self.gamma_adipo, self.drive(E, genome), self.slope, self.a0))
        return float(np.clip((raw - self._floor) / (1.0 - self._floor + 1e-9), 0.0, 1.0))


# ===================================================================== anatomical depot map
def _ellip_falloff(P, c, r, soft=1.6):
    """Smooth region weight in [0,1]: 1 deep inside the ellipsoid (c,r), 0 well outside.
    A soft indicator (not an SDF) used to localise a fat depot to an anatomical region."""
    q = (np.asarray(P) - np.asarray(c, float)) / np.asarray(r, float)
    d = np.linalg.norm(q, axis=-1)               # 1.0 on the ellipsoid surface
    return np.clip(1.0 - (d - 1.0) / soft, 0.0, 1.0) * (d <= 1.0 + soft)


class DepotMap:
    """WHERE fat sits: a set of anatomical subcutaneous regions, each (center, radii, weight, tag),
    combined as a soft-OR. `android` in [0,1] mixes between central/visceral (apple, android=1)
    and gluteofemoral (pear, android=0) depots -- sex/pattern influenced (default a forced [F]).
    weight(P) returns a depot field in [0,1]; thickness = t_max * alpha * weight(P)."""

    def __init__(self, regions, android=0.5, name="depot"):
        # regions: list of dict(c=(x,y,z), r=(rx,ry,rz), w=float, tag='central'|'gluteofemoral'|'face'|None)
        self.regions = regions
        self.android = float(android)
        self.name = name

    def weight(self, P):
        P = np.asarray(P, float)
        out = np.zeros(P.shape[:-1], float)
        for reg in self.regions:
            w = float(reg.get("w", 1.0))
            tag = reg.get("tag")
            if tag == "central":
                w *= self.android
            elif tag == "gluteofemoral":
                w *= (1.0 - self.android)
            f = w * _ellip_falloff(P, reg["c"], reg["r"], soft=reg.get("soft", 1.6))
            out = 1.0 - (1.0 - out) * (1.0 - np.clip(f, 0.0, 1.0))   # soft-OR
        return np.clip(out, 0.0, 1.0)


# ===================================================================== surface inflation
def inflate_sampler(target, model, depot, E, genome="neutral", t_max=3.0, scales=None):
    """Return a sampler phi'(P) = phi_lean(P) - t(P), where t(P)=t_max*alpha(E,genome)*depot(P).
    Subtracting a positive thickness field from an SDF DILATES the solid by that thickness (an
    offset surface); a spatially-varying t gives spatially-varying inflation == fat depots.
    At the lean end alpha->0 so phi'->phi_lean and the headline convergence proof is untouched."""
    alpha = model.activation(E, genome)

    def sample(P):
        base = target.sample(P, scales)
        t = t_max * alpha * depot.weight(P)
        return base - t
    sample.alpha = alpha
    sample.t_max = t_max
    return sample


# ===================================================================== quantitative readouts
def occupancy_volume(sampler, box, vox):
    """Inside-voxel volume of phi'<=0 on a fixed grid (a fat-mass proxy in model units^3)."""
    import body as B
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    occ = sampler(P) <= 0
    return float(occ.sum()) * (dx ** 3), (nx, ny, nz), dx


def adiposity_index(sampler_E, sampler_lean, box, vox):
    """AI = (V(E) - V_lean)/V_lean : fractional volume added by adipose, from real occupancy."""
    vE, _, _ = occupancy_volume(sampler_E, box, vox)
    vL, _, _ = occupancy_volume(sampler_lean, box, vox)
    return float((vE - vL) / vL) if vL > 0 else 0.0, vE, vL


def mesh_of(sampler, box, vox, smooth=0.6):
    """Marching-cubes surface (verts, normals) of phi'<=0 (reuses the package mesher)."""
    import body as B
    from grow_to_target import _mesh
    nx, ny, nz = [max(8, int(b / vox)) for b in box]
    P, axes, dx = B.grid(nx, ny, nz, box)
    field = sampler(P).astype(np.float32)
    v, n = _mesh(field, axes, smooth=smooth)
    return v, n


def face_width_height_ratio(verts, y_split=None):
    """Lower-face WIDTH:HEIGHT from the mesh (an anthropometric 'roundness' index).
    Adipose widens the CHEEK/JOWL band (lower-mid face) while the bony cranial width and the face
    height barely move, so a fuller face reads as a higher lower-face width:height. width = MAX
    x-extent over the jaw->mid-cheek band (y in [0.20,0.50] of height, where buccal/jowl/jawline
    pads sit); height = full face y-extent. A measurement on the surface, not a depot tuning: an
    isotropic inflation would leave it flat; it rises only because subcutaneous fat is lower-face
    weighted. Pass y_split to force a single thin band instead."""
    if verts is None or len(verts) < 20:
        return float("nan")
    ymin, ymax = verts[:, 1].min(), verts[:, 1].max()
    H = ymax - ymin
    if H <= 0:
        return float("nan")
    if y_split is not None:
        band = verts[np.abs(verts[:, 1] - y_split) < 0.08 * H]
        width = (band[:, 0].max() - band[:, 0].min()) if len(band) >= 8 else \
                (verts[:, 0].max() - verts[:, 0].min())
        return float(width / H)
    lo, hi = ymin + 0.20 * H, ymin + 0.50 * H
    band = verts[(verts[:, 1] >= lo) & (verts[:, 1] <= hi)]
    if len(band) < 8:
        band = verts
    width = band[:, 0].max() - band[:, 0].min()
    return float(width / H)


def waist_hip_ratio(verts, waist_y, hip_y, half=0.06):
    """Waist:hip circumference proxy from horizontal mesh slabs (android vs gynoid signature)."""
    if verts is None or len(verts) < 20:
        return float("nan")
    yr = verts[:, 1].max() - verts[:, 1].min()

    def girth(y0):
        s = verts[np.abs(verts[:, 1] - y0) < half * yr]
        if len(s) < 8:
            return float("nan")
        # cross-sectional extent in x,z (an ellipse-perimeter proxy)
        rx = 0.5 * (s[:, 0].max() - s[:, 0].min())
        rz = 0.5 * (s[:, 2].max() - s[:, 2].min())
        return math.pi * (3 * (rx + rz) - math.sqrt((3 * rx + rz) * (rx + 3 * rz)))  # Ramanujan
    w, h = girth(waist_y), girth(hip_y)
    return float(w / h) if (h and h == h and h > 0) else float("nan")
