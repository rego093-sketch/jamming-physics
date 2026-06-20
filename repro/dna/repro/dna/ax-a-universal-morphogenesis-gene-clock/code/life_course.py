"""
life_course.py -- Layer-3 (gene clock, TIME axis) + Layer-4 (adipose, ENERGY axis) coupled into
ONE CONTINUOUS R19 PROCESS for a single individual.  (HANDOFF Layer-4 NEXT #4.)

The gene clock makes the ORDER/TIMING of feature appearance a readout of measured gamma; the
adipose fold makes body COMPOSITION (lean<->heavy) a readout of measured obesity-gamma + an energy
dial. Until now those two axes ran in separate demos. This module runs them TOGETHER on one genome:
a single person lived forward as

    (developmental time tau in [0,1])  x  (lifelong chronic energy E(t))

at each life point we build the gene-clock body FROZEN at tau (which features have emerged is the
gamma readout) and then INFLATE it by the adipose fold's alpha(E, genome) over the anatomical
depot. The result is one continuous trajectory -- small lean child -> grown lean adult -> grown
heavier adult -- and BOTH clocks are literally the SAME R19 switch:

    gene_clock.spinodal == adipose.spinodal == morpho_core.spinodal   (asserted < 1e-12)

so child->adult->heavy is one fold expressed first in TIME and then in ENERGY. That is the unifying
claim of the whole package made concrete on a single individual: one switch writes DNA, fires
neurons, folds the body, schedules the face, AND defends the fat set-point -- across a lifetime.

WHAT IS MEASURED vs FORCED (neuro VP-SPEC C3 discipline):
  [V] one continuous fold: the TIME clock and the ENERGY clock are the SAME spinodal (< 1e-12).
  [L] gamma (gene clock) and obesity-gamma (adipose) -- measured, read-only.
  [V] (derived) the trajectory is MONOTONE: developmental completeness A(tau) rises with tau, and
      adiposity rises with E at fixed maturity; the emergence order stays the gamma readout.
  [F] the life schedule E(t)/tau(t) is an INPUT (a chosen life, not a prediction); the depot map is
      the ADULT anatomical map applied throughout life (a forced simplification, declared).
  [O] real ages/BMI in absolute units, and a specific person's trajectory -- not fitted here.

BASELINE PRESERVED: at the lean reference (E=E_lean, neutral genome) alpha=0 for the whole tau
sweep, so the inflated surface == the pure gene-clock surface BIT-FOR-BIT -- the energy axis
perturbs nothing at lean, and Layer 3's convergence proof survives untouched. (verify check #4.)

stdlib + numpy (+ scipy/skimage for meshing, reused). Deterministic.
"""
import os, io, json, hashlib, contextlib
import numpy as np
import scipy.ndimage as ndi
from skimage import measure
import body as B
import gene_clock as GC
import adipose as AD
import adipose_atlas as AA
import morpho_core as mc
from grow_to_target import smoothstep, egg_sdf


# ===================================================================== one continuous fold
def assert_one_continuous_fold(tol=1e-12):
    """Prove the developmental (gene-clock) fold AND the adipose (energy) fold are BOTH the body
    fold -- one switch shared across the TIME and ENERGY axes. Returns the max deviation."""
    gs = np.linspace(1.2, 1.8, 121)
    d_time = max(abs(GC.spinodal(g) - mc.spinodal(g)) for g in gs)     # time clock
    d_energy = max(abs(AD.spinodal(g) - mc.spinodal(g)) for g in gs)   # energy clock
    assert d_time <= tol and d_energy <= tol, f"fold mismatch: time={d_time}, energy={d_energy}"
    return float(max(d_time, d_energy))


# ===================================================================== developing body @ tau
class DevTarget:
    """The gene-clock developing body FROZEN at developmental time tau, exposed as a point-
    sampleable SDF (so the adipose inflater composes with it directly, exactly as for a static
    scan). sample(P) = (1-A)*egg(P) + A*lean_body(P with each feature scaled to its a_f(tau)).
    At tau>=1: A=1 and every a_f=1 -> sample == the full lean target (convergence proof intact).

    The per-feature presence a_f(tau) is the gene clock's R19 emergence curve at THIS tau (so the
    ORDER in which features appear over the life is the measured-gamma readout). The only thing
    omitted vs grow_gene_clock is the residual sub-feature low-pass (a cosmetic crispening, and 0
    at tau=1 anyway) -- so the developmental field stays a clean point-sampleable SDF."""

    def __init__(self, ftarget, tau, sched, egg_c, egg_r):
        self.ft = ftarget
        self.tau = float(tau)
        self.box = ftarget.box
        self.name = f"{ftarget.name}@tau={tau:.2f}"
        self.A = float(smoothstep(self.tau))
        self.egg_c = np.asarray(egg_c, float)
        self.egg_r = float(egg_r)
        ts = np.array([self.tau], float)
        self.present = {}
        for f, _g in ftarget.features:
            d = sched["features"][f]
            self.present[f] = float(GC.emergence_curve(d["gamma"], ts, d["tau_on"])[0])

    def n_emerged(self, thr=0.5):
        return int(sum(1 for a in self.present.values() if a > thr))

    def sample(self, P, scales=None):
        egg = egg_sdf(P, self.egg_c, self.egg_r)
        body = self.ft.sample(P, self.present)
        return (1.0 - self.A) * egg + self.A * body


# ===================================================================== the life course
class LifeCourse:
    """One genome lived forward across the TIME axis (gene clock) and the ENERGY axis (adipose)."""

    def __init__(self, scene="face", genome="neutral", android=0.5, t_max=3.0,
                 tau0=0.12, tau1=0.92, sign=+1, gamma_body=1.287, seed_vox=1.4):
        self.scene = scene
        self.genome = genome
        self.t_max = float(t_max)
        self.ft, self.depot = AA.SCENES[scene](android)
        self.model = AD.AdiposeModel()                         # asserts the adipose fold == body fold
        self.gammas, self.prov = GC.load_gamma_table()         # measured gene-clock table (read-only)
        self.sched = GC.feature_schedule(self.ft.features, self.gammas,
                                         tau0=tau0, tau1=tau1, sign=sign)
        self.one_switch = assert_one_continuous_fold()         # one fold across TIME and ENERGY
        # egg seed (matches grow_gene_clock): centroid of the full lean target + gamma-scaled radius
        box = self.ft.box
        nx, ny, nz = [max(8, int(b / seed_vox)) for b in box]
        P, _axes, _dx = B.grid(nx, ny, nz, box)
        T = self.ft.sample(P, None)
        inside = P[T <= 0]
        self.egg_c = inside.mean(0) if len(inside) else np.zeros(3)
        self.egg_r = 0.30 * min(box) * (gamma_body / 1.287)

    # ---- one life point -> field/metrics
    def dev_target(self, tau):
        return DevTarget(self.ft, tau, self.sched, self.egg_c, self.egg_r)

    def sampler(self, tau, E, genome=None):
        """The inflated developing surface at (tau, E): gene-clock body @ tau, adipose-inflated @ E."""
        dev = self.dev_target(tau)
        return AD.inflate_sampler(dev, self.model, self.depot, E,
                                  genome or self.genome, t_max=self.t_max), dev

    def _field(self, sampler, vox):
        nx, ny, nz = [max(8, int(b / vox)) for b in self.ft.box]
        P, axes, dx = B.grid(nx, ny, nz, self.ft.box)
        return sampler(P).astype(np.float32), axes, dx, (nx, ny, nz)

    def occupancy(self, sampler, vox):
        v, _, _, _ = self.occupancy_volume(sampler, vox)
        return v

    def occupancy_volume(self, sampler, vox):
        return AD.occupancy_volume(sampler, self.ft.box, vox)

    def trajectory(self, points, vox=1.0):
        """points : [(label, tau, E), ...] a chosen life. Returns a per-point list with
        developmental completeness A(tau), gene-clock presence, adipose alpha(E), occupancy volume,
        an anthropometric index, and a deterministic field sha256."""
        rows = []
        lean_ref = None
        for label, tau, E in points:
            s, dev = self.sampler(tau, E)
            vol, grid, dx = self.occupancy_volume(s, vox)
            field, _, _, _ = self._field(s, vox)
            sha = hashlib.sha256(np.round(field, 5).tobytes()).hexdigest()[:16]
            # an index: face roundness for the face scene, waist:hip for the body scene
            v, f = self._mesh_faces(s, vox)
            if self.scene == "face":
                idx = AD.face_width_height_ratio(v); idx_name = "WH"
            else:
                idx = AD.waist_hip_ratio(v, 8.0, -5.0); idx_name = "WHR"
            rows.append(dict(label=label, tau=float(tau), E=float(E),
                             A_developmental=float(smoothstep(tau)),
                             alpha_adipose=float(s.alpha),
                             n_emerged=dev.n_emerged(), n_features=len(self.ft.features),
                             occupancy_volume=float(vol), index=float(idx), index_name=idx_name,
                             field_sha=sha))
        return rows

    def _mesh_faces(self, sampler, vox, smooth=0.6):
        field, axes, dx, (nx, ny, nz) = self._field(sampler, vox)
        sm = ndi.gaussian_filter((field <= 0).astype(np.float32), smooth)
        if sm.max() < 0.5 or sm.min() > 0.5:
            return None, None
        v, f, _, _ = measure.marching_cubes(sm, 0.5)
        xs, ys, zs = axes
        vm = np.stack([np.interp(v[:, 0], np.arange(len(xs)), xs),
                       np.interp(v[:, 1], np.arange(len(ys)), ys),
                       np.interp(v[:, 2], np.arange(len(zs)), zs)], 1)
        return vm, f.astype(int)

    # ---- invariants / falsifiable properties
    def baseline_preserved(self, taus, vox=1.2):
        """At the lean reference (E_lean, neutral genome) alpha must be 0 for EVERY tau, so the
        inflated field equals the pure gene-clock field bit-for-bit -> the energy axis perturbs
        nothing at lean and the gene-clock/convergence proof survives. Returns (ok, max|alpha|,
        max|field difference|)."""
        max_a = 0.0
        max_diff = 0.0
        for tau in taus:
            dev = self.dev_target(tau)
            lean = AD.inflate_sampler(dev, self.model, self.depot, self.model.E_lean,
                                      "neutral", t_max=self.t_max)
            max_a = max(max_a, abs(float(lean.alpha)))
            nx, ny, nz = [max(8, int(b / vox)) for b in self.ft.box]
            P, _ax, _dx = B.grid(nx, ny, nz, self.ft.box)
            diff = float(np.max(np.abs(lean(P) - dev.sample(P))))
            max_diff = max(max_diff, diff)
        return (max_a < 1e-9 and max_diff < 1e-9), float(max_a), float(max_diff)

    def order_is_gamma_readout(self):
        return bool(self.sched["order_is_gamma_readout"])

    def emergence_order(self):
        return list(dict.fromkeys([self.sched["features"][f]["gene"] for f in self.sched["order"]]))


# ===================================================================== a canonical chosen life
def default_life():
    """A chosen life: lean development child->adult (TIME axis), then chronic surplus adult
    (ENERGY axis). The first four points share E_lean and raise tau (growth); the last three share
    tau=1 (maturity) and raise E (fattening). child -> adult -> heavy, one continuous fold."""
    return [
        ("infant",        0.35, -1.0),
        ("child",         0.55, -1.0),
        ("adolescent",    0.78, -1.0),
        ("adult lean",    1.00, -1.0),     # lean reference: alpha == 0 (baseline preserved)
        ("adult surplus", 1.00,  0.25),
        ("adult heavy",   1.00,  0.55),
    ]


if __name__ == "__main__":
    lc = LifeCourse(scene="face")
    print(f"one continuous fold (time==energy==body): max|delta| = {lc.one_switch:.2e}")
    print(f"emergence order (gamma readout={lc.order_is_gamma_readout()}): "
          f"{' < '.join(lc.emergence_order())}")
    rows = lc.trajectory(default_life(), vox=1.0)
    print(f"\n  {'life point':14s} {'tau':>4s} {'E':>6s} {'A':>5s} {'alpha':>6s} "
          f"{'emerged':>8s} {'volume':>9s} {'index':>7s}")
    for r in rows:
        print(f"  {r['label']:14s} {r['tau']:4.2f} {r['E']:+6.2f} {r['A_developmental']:5.2f} "
              f"{r['alpha_adipose']:6.2f} {r['n_emerged']:3d}/{r['n_features']:<4d} "
              f"{r['occupancy_volume']:9.1f} {r['index']:7.3f}")
    ok, ma, md = lc.baseline_preserved([0.35, 0.55, 0.78, 1.0])
    print(f"\n  baseline preserved (alpha==0 over the lean sweep): {ok}  "
          f"(max|alpha|={ma:.1e}, max|field diff|={md:.1e})")
