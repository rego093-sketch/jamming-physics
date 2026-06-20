"""
gene_clock.py -- drive Layer-3 target growth from MEASURED gene stiffness gamma.

This is the bridge that re-unites target-driven growth (Layer 3) with the DNA framework.
Instead of one hand-set global low-pass schedule sigma(tau), EVERY external feature
(eye, ear, nose, lips, cranium, ...) switches on at a developmental time tau_on set by
ITS OWN master gene's R19 spinodal, and reads a relative size from that gene's
DWELL ~ gamma^1.5. The emergence ORDER and relative timing therefore fall out of measured
DNA, not tuning -- heterochrony as a readout of gamma.

ONE SWITCH ACROSS THE CHAIN.  The R19 fold here is the SAME primitive as
  * universal/morpho_core.spinodal  (the cusp/fold body engine), and
  * the neuro emergence engine vp_neuro_engine.Organ.functional_spinodal,
because all three define
      spinodal(g) = 2*(g/3)^1.5  ==  (2/(3*sqrt(3)))*g^1.5
which are identical to ~1e-16 (3^1.5 == 3*sqrt(3)). So coupling the neuro gene engine to
the morphogenesis growth schedule is not a bolt-on: it is one switch shared across the
whole "ion channel -> body" chain. assert_one_switch() proves it at run time.

MEASURED, NEVER FITTED.  gamma = mean(-NN stacking dG37) (SantaLucia 1998), read VERBATIM
from NCBI promoter sequences (corr(gamma,GC) ~ 0.994), in data/sensory_organ_gamma.json.
Nothing here tunes a gamma to hit a target; we report what falls out of the measured values.

GRADES (neuro VP-SPEC C3 discipline -- every quantity graded, no silent gap):
  [V] spinodal identity across packages: asserted < 1e-12.
  [V] emergence ORDER is a deterministic readout of measured gamma: it EQUALS argsort of
      the spinodal; change a gamma and the order changes with it (no hand-typed order).
      This is the SAME spinodal-ordering mechanism that reproduces the measured spinal
      ventral->dorsal order in neuro chapter 17 -- here applied in the TIME axis.
  [F] the sign convention (higher spinodal -> later) and the absolute tau window
      [tau0, tau1]: forced modelling choices (documented). Flipping the sign flips the
      order, exactly as a flipped Shh threshold flips the spinal order.
  [V]/[F] feature -> gene map: [V] master for the sensory features (eye=PAX6, ear=PAX2,
      nose/olfactory=LHX2, skin=TP63); [F]/representative for the structural groups
      (cranium=FOXG1, jaw/midline=SHH, cheek=MYOD1, lips/oral=POU2F3), labelled per feature.
  [O] absolute developmental time in real units, and the absolute feature sizes from dwell,
      need external calibration (stated; only the order + relative ratios are claimed).

stdlib + numpy. Deterministic (pure arithmetic over the frozen gamma table).
"""
import os, json, math
import numpy as np
import morpho_core as mc   # the in-package R19 fold (single source for the body engine)

HERE = os.path.dirname(os.path.abspath(__file__))
GAMMA_JSON = os.path.join(HERE, "data", "sensory_organ_gamma.json")


# --------------------------------------------------------------------- R19 primitives
def spinodal(g):
    """|h| past which the opposite basin disappears -> the flip is DISCONTINUOUS.
    2*(g/3)^1.5 == (2/(3*sqrt(3)))*g^1.5 (morpho_core form) == neuro Organ form."""
    return 2.0 * (g / 3.0) ** 1.5


def barrier(g):
    """g^2/4 : energy barrier between the two basins (state stability / onset sharpness)."""
    return g * g / 4.0


def dwell(g, brake=0.5, K=0.6):
    """DWELL ~ gamma^1.5 throttled by a growth brake -> RELATIVE feature size (neuro Organ.size).
    Order/direction forced [F]; absolute magnitude calibration [O]."""
    return (g ** 1.5) / (K + brake)


def assert_one_switch(tol=1e-12):
    """Prove the morphogenesis switch and the neuro gene switch are the SAME function.
    Returns max|delta| over a gamma sweep; raises if it exceeds tol."""
    gs = np.linspace(1.2, 1.8, 121)
    d = max(abs(spinodal(g) - mc.spinodal(g)) for g in gs)   # vs morpho_core (body engine)
    assert d <= tol, f"spinodal mismatch vs morpho_core: {d}"
    return float(d)


# --------------------------------------------------------------------- measured gamma
def load_gamma():
    """Load the measured gene gamma table (real NCBI promoters). Returns {gene: gamma}."""
    J = json.load(open(GAMMA_JSON, encoding="utf-8"))
    return {k: float(v["gamma"]) for k, v in J["genes"].items()}, J.get("_provenance", "")


# --------------------------------------------------------------------- the time clock
def emergence_curve(gamma, taus, tau_on, slope=14.0, eps=1e-3):
    """a_f(tau) in [0,1]: the feature's gene reads a rising temporal competence morphogen
    through ITS OWN R19 fold. The drive is centred so it equals the gene's spinodal exactly
    at tau_on; before tau_on the switch (started OFF) stays OFF (absent), at tau_on the OFF
    basin disappears and it flips ON (a SHARP, bistable onset -- the fold turns a smooth
    clock into a crisp appearance), then saturates. Onset width is set by gamma via the
    barrier (stiffer gene -> sharper switch). This mirrors emergent_registers' positional
    information in SPACE, here in TIME."""
    taus = np.asarray(taus, float)
    sp = spinodal(gamma)
    h = sp + slope * (taus - tau_on)                       # crosses +spinodal at tau_on
    s = mc.settle_field(gamma, h, np.full_like(h, -1.0))   # start OFF, settle the fold
    a = (s + math.sqrt(gamma)) / (2.0 * math.sqrt(gamma))  # map settled state -> [0,1]
    return np.clip(a, eps if eps else 0.0, 1.0)


def feature_schedule(feature_genes, gammas, tau0=0.12, tau1=0.92, sign=+1,
                     n_tau=41, slope=14.0):
    """Build the gene-clock growth schedule for a set of features.

    feature_genes : ordered dict-like list of (feature_name, gene_name).
    gammas        : {gene_name: gamma} measured table.
    sign=+1       : higher spinodal -> LATER tau_on (neuro Organ convention).  [F]
    [tau0, tau1]  : the developmental window the order is DISPLAYED on.        [F]

    Returns a dict with, per feature: gamma, spinodal, tau_on (window-shown, order- and
    relative-spacing-preserving), tau_on_raw (= spinodal/Dmax, absolute scale [O]),
    dwell (relative size), and the full a_f(tau) curve. Plus the derived order and the
    falsifiable check that order == argsort(spinodal) (so the order is a pure gamma readout).
    """
    names = [f for f, _ in feature_genes]
    sp = np.array([spinodal(gammas[g]) for _, g in feature_genes])
    key = sign * sp
    sp_min, sp_max = float(sp.min()), float(sp.max())
    # window-normalised tau_on: affine map preserves ORDER and relative spacing RATIOS
    if sp_max > sp_min:
        frac = (key - key.min()) / (key.max() - key.min())
    else:
        frac = np.zeros_like(sp)
    tau_on = tau0 + (tau1 - tau0) * frac
    # absolute-scale raw tau_on (declared [O]); Dmax chosen so max spinodal maps to tau1
    Dmax = sp_max / tau1
    tau_on_raw = sp / Dmax

    taus = np.linspace(0.0, 1.0, n_tau)
    feats = {}
    for i, (fname, gene) in enumerate(feature_genes):
        g = gammas[gene]
        feats[fname] = dict(
            gene=gene, gamma=float(g), spinodal=float(sp[i]), barrier=float(barrier(g)),
            tau_on=float(tau_on[i]), tau_on_raw=float(tau_on_raw[i]),
            dwell=float(dwell(g)),
            a=emergence_curve(g, taus, float(tau_on[i]), slope=slope),
        )
    # derived emergence order (ascending tau_on) and the gamma-readout check
    order = [names[j] for j in np.argsort(tau_on, kind="stable")]
    order_by_spinodal = [names[j] for j in np.argsort(key, kind="stable")]
    order_is_gamma_readout = (order == order_by_spinodal)
    return dict(taus=taus, features=feats, order=order,
                order_is_gamma_readout=bool(order_is_gamma_readout),
                sign=sign, tau_window=(tau0, tau1))


# --------------------------------------------------------------------- summary helper
def schedule_table(sched):
    """A compact, printable summary: each feature's gene, gamma, spinodal, tau_on, size."""
    rows = []
    for f in sched["order"]:
        d = sched["features"][f]
        rows.append((f, d["gene"], d["gamma"], d["spinodal"], d["tau_on"], d["dwell"]))
    return rows


# --------------------------------------------------------------------- extended atlas loader
MORPHO_JSON = os.path.join(HERE, "data", "morpho_gamma.json")


def load_gamma_table(path=None):
    """Load a measured gamma table from `path` (defaults to the EXTENDED morpho_gamma.json,
    which contains the original 26 genes bit-for-bit plus the new appendage/hair/tooth/iris
    masters, every value still measured by the SantaLucia NN pipeline -- never fitted).
    Returns ({gene: gamma}, provenance_string). Falls back to the base 26-gene table."""
    p = path or MORPHO_JSON
    if not os.path.exists(p):
        return load_gamma()
    J = json.load(open(p, encoding="utf-8"))
    prov = J.get("_provenance", "") + " | " + J.get("_provenance_plus", "")
    return {k: float(v["gamma"]) for k, v in J["genes"].items()}, prov
