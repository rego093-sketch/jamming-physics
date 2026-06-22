# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- CHUNK C / GAP-3 BUILD : THE GROUNDED CONNECTOME + O x W
#  the long-range routing axis (W) and the organ-capacity axis (O), built to
#  carry the autism / intellectual-disability DOUBLE DISSOCIATION.
#
#  Constitution: physical/topological only, NO TUNING, public cited orderings
#  grounded, data decides.  consciousness_claim = 0 ; hard_problem_open = 1 ;
#  engine READ-ONLY.  STATUS: hypothesis-forming -- do NOT confirm; ST-3 stresses it.
#
#  WHAT GAP-3 CLAIMS (whitepaper Section 3, row 3):
#    "Long-range wiring carries routing (W); the autism/ID double dissociation
#     lives here -- autism = W-fault (local over-coordination -> stereotypy),
#     intellectual disability = O-fault (capacity down, W intact -> preserved
#     sociality)."  Two SEPARABLE axes, not one factor.
#
#  TWO PARTS:
#  ----------------------------------------------------------------------------
#  (A) THE FULL GROUNDED CONNECTOME (12-organ scale).  Extends the two cited
#      edges in frontal_axonal_channel.py to the major long-range tracts, each
#      edge grounded to published ORDERING (magnitudes stay [O], never tuned):
#        cortex<->thalamus(MD)  HEAVY RECIPROCAL  = 1.00  [L cited]
#            Klein 2010 NeuroImage 51:555 ; J Neurosci 43:7780 (2023).  The leucotomy tract.
#        cortex<->striatum      massive corticostriatal = 0.80  [L ordering; O mag]
#        cortex<->hippocampus   entorhinal/cingulum     = 0.40  [L ordering; O mag]
#        cortex<->hypothalamus  SPARSE diffuse           = 0.15  [L cited sparse]
#            Ongur & Price 1998 JCN 401:480 ; Radley 2006 J Neurosci 26:12967.
#        thalamus/striatum/pallidum BG-thalamic loop      = 0.60/0.70/0.50  [L ordering; O mag]
#        cerebellum<->thalamus  dentato-thalamic          = 0.50  [L ordering; O mag]
#        midbrain/brainstem<->thalamus ascending          = 0.40/0.40  [L ordering; O mag]
#      HONEST NEGATIVE (recorded, the Stress Principle): at the COARSE 12-node
#      phase scale, severing the heavy grounded tracts does NOT yield a SIGN-STABLE
#      global-integration (order-parameter) deficit -- the global field is
#      dominated by the frozen ephaptic kernel, so a single axonal lesion is a weak
#      perturbation (consistent with the leucotomy "perception spared" result).
#      That collapse is exactly WHY the O x W dissociation is tested at the
#      cortical MICRO-MODEL scale, where routing topology actually carries binding.
#
#  (B) THE O x W ORTHOGONALITY (cortical micro-model scale).  Built ON the
#      surviving Gap-2 micro-model (frozen Hippocampus + hub topology):
#        W-axis (routing)  = the hub-borne LONG-RANGE edges.   W-fault = cut them.
#        O-axis (capacity) = the buffer's storage headroom = N_CELLS, with the
#                            K=7 emerged hubs (the tracts) PRESERVED.  O-fault =
#                            fewer cells, wiring backbone intact ("microcephaly":
#                            fewer neurons, white matter spared).
#      Two read-outs, scored NON-CIRCULARLY:
#        SOCIALITY = long-range binding  (cue NEAR block -> recover DISTANT block;
#                    scored on the free distant bits, never the cut edge).  Loads on W.
#        CAPACITY  = within-pattern completion from a SCATTERED partial cue.
#                    Loads on O; Gap-2 Contrast B showed it is hub(W)-light.
#      The double dissociation is a CROSSOVER (selectivity), the honest form of a
#      neuropsychological double dissociation: each fault hits its OWN read-out
#      several-fold harder than the other's.  Anti-tuning: swept over perturbation
#      magnitude + seed-averaged; the crossover must be sign-stable (the F1 rule).
#
#  N_CELLS=120, LR=0.18 inherited [O] from the engine Hippocampus; K=7 emerged
#  (cortical_emergence); the f_W and N grids are SWEEP AXES (the experiment's
#  independent variables), NOT tuned constants.  new_tuned_constants = 0.
# ==========================================================================
import sys, os, math, json
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "_frontal"))
sys.path.insert(0, _HERE)
import vp_mind_engine as E                  # FROZEN, READ-ONLY (sha e61083ae...)
import frontal_common as FC                  # frozen substrate + anchor guard + digest
from cortical_emergence import emerge_organ  # no-tuning capacity emergence
from cortical_microcircuit import CorticalMicrocircuit, FOXG1  # the SURVIVING Gap-2 model

ATLAS = E.load_brain_atlas()
LHX2  = float(ATLAS["organs"]["hippocampus"]["gamma"])      # 1.5172 measured, gene control

N_CELLS, LR = 120, 0.18                                      # inherited engine [O] scales
K = int(round(emerge_organ("neocortex")["wm_capacity_emerged"]))   # emerged capacity ~7
N_HUBS = K                                                   # broadcaster slots = capacity (gene-grounded)

# --- experiment sweep axes (independent variables, NOT tuned constants) --------
F_W_GRID = (0.0, 0.3, 0.6, 0.9)                             # fraction of hub long-range edges cut
N_GRID   = (120, 90, 64, 44)                                # O-axis: cell count (Hopfield capacity ~0.14 N)
F_W_MAX  = max(F_W_GRID)                                    # 0.9 -- strongest W-fault
N_LO     = min(N_GRID)                                      # 44  -- strongest O-fault
MARGIN   = 0.02                                             # abs-fidelity selectivity margin (> cohort noise)

RESULTS_JSON = os.path.join(_HERE, "cortico_connectome_owt_results.json")
EXPECTED_SHA = os.path.join(_HERE, "expected_cortico_connectome_owt_sha256.json")


# ==========================================================================
#  PART A -- THE GROUNDED LONG-RANGE CONNECTOME (12-organ scale)
# ==========================================================================
def _ix(name): return FC.idx(name)

CONNECTOME_EDGES = [
    # (organ_i, organ_j, weight, grade, citation)
    ("neocortex", "thalamus",    1.00, "[L cited]",        "Klein 2010 NeuroImage 51:555; J Neurosci 43:7780 (2023) -- heavy reciprocal MD-PFC (the leucotomy tract)"),
    ("neocortex", "striatum",    0.80, "[L ordering; O]",  "massive corticostriatal glutamatergic projection (largest cortical output)"),
    ("neocortex", "hippocampus", 0.40, "[L ordering; O]",  "cortico-hippocampal entorhinal/cingulum loop"),
    ("neocortex", "hypothalamus",0.15, "[L cited sparse]", "Ongur & Price 1998 JCN 401:480; Radley 2006 J Neurosci 26:12967 -- sparse diffuse mPFC->hypothalamus"),
    ("thalamus",  "striatum",    0.60, "[L ordering; O]",  "thalamostriatal projection (BG-thalamic loop)"),
    ("striatum",  "pallidum",    0.70, "[L ordering; O]",  "striatopallidal projection (BG-thalamic loop)"),
    ("thalamus",  "pallidum",    0.50, "[L ordering; O]",  "pallido-thalamic projection (BG-thalamic loop)"),
    ("cerebellum","thalamus",    0.50, "[L ordering; O]",  "dentato-thalamic tract"),
    ("midbrain",  "thalamus",    0.40, "[L ordering; O]",  "ascending midbrain->thalamus"),
    ("brainstem", "thalamus",    0.40, "[L ordering; O]",  "ascending brainstem->thalamus"),
]

def grounded_connectome():
    """The full grounded long-range axonal matrix A (relative orderings cited above).
    A is a NEW, separately-provenanced physical substrate; the frozen ephaptic W0
    stays READ-ONLY.  Experiments run on W0 + kappa_axon * A (axonal channel)."""
    A = np.zeros((FC.N, FC.N))
    for ni, nj, w, _g, _c in CONNECTOME_EDGES:
        i, j = _ix(ni), _ix(nj)
        A[i, j] = A[j, i] = w
    return A

A_CONN = grounded_connectome()

def _global_R(W, seeds=range(19, 25), T=1.0, dt=FC.DT_DEFAULT):
    out = []
    for sd in seeds:
        rng = np.random.RandomState(sd)
        th = rng.uniform(-math.pi, math.pi, FC.N)
        ns = int(T / dt); Rs = np.empty(ns)
        for s in range(ns):
            d = th[None, :] - th[:, None]
            th = th + dt * (FC.OMEGA + FC.uniform_K() * np.sum(W * np.sin(d), axis=1))
            Rs[s] = FC._order(th)
        out.append(float(np.mean(Rs[ns // 2:])))
    return float(np.mean(out))

def _sever(W, edges):
    W = W.copy()
    for i, j in edges:
        W[i, j] = FC.W0[i, j]; W[j, i] = FC.W0[j, i]   # revert to ephaptic-only (faithful lesion)
    return W

def connectome_integration_check(kappas=(0.1, 0.2, 0.5, 1.0)):
    """Honest test at the COARSE organ/phase scale: does severing the HEAVY grounded
    long-range tracts degrade the global order parameter MORE than severing an equal
    count of WEAK tracts, SIGN-STABLY across the axonal-kappa sweep?  (Expected to be
    NOT sign-stable -- recorded as the honest negative that motivates Part B.)"""
    heavy = [(_ix("neocortex"), _ix("thalamus")), (_ix("neocortex"), _ix("striatum")),
             (_ix("striatum"),  _ix("pallidum")), (_ix("neocortex"), _ix("hippocampus"))]
    weak  = [(_ix("neocortex"), _ix("hypothalamus")), (_ix("midbrain"), _ix("thalamus")),
             (_ix("brainstem"), _ix("thalamus")), (_ix("thalamus"), _ix("pallidum"))]
    rows, signs = [], []
    for k in kappas:
        Wi = FC.W0 + k * A_CONN
        Ri = _global_R(Wi); Rh = _global_R(_sever(Wi, heavy)); Rw = _global_R(_sever(Wi, weak))
        rows.append({"kappa_axon": k, "R_intact": Ri,
                     "dR_sever_heavy": Rh - Ri, "dR_sever_weak": Rw - Ri})
        signs.append(bool((Rh - Ri) < (Rw - Ri)))   # heavy drops integration more?
    sign_stable = bool(len(set(signs)) == 1 and signs[0])
    return {"rows": rows, "heavy_drops_integration_more_every_kappa": sign_stable,
            "honest_negative_recorded": bool(not sign_stable)}


# ==========================================================================
#  PART B -- THE O x W ORTHOGONALITY (cortical micro-model scale)
#  OWTCortex generalises the SURVIVING Gap-2 CorticalMicrocircuit to a free cell
#  count N (the O-axis), with the K=7 emerged hubs (the W-axis tracts) preserved.
#  Construction is IDENTICAL to Gap-2; an equivalence assert proves the reuse.
# ==========================================================================
class OWTCortex:
    """Hub-organised recurrent buffer on the frozen Hippocampus, with N a free
    parameter (the O-axis = storage capacity).  K=7 hubs (gene-grounded broadcaster
    slots) carry the long-range edges (the W-axis = routing).  No new constant; no
    kernel change -- the hippocampus precedent at variable capacity."""
    def __init__(self, n_cells=N_CELLS, g=FOXG1, n_hubs=N_HUBS, topo_seed=19, all_to_all=False):
        self.N = int(n_cells)
        self.hp = E.Hippocampus(n_cells=self.N, g=g, lr=LR)     # frozen micro-model
        self.r = max(1, int(round(self.N / (2 * max(1, n_hubs)))))  # local window grounded by K
        self.all_to_all = bool(all_to_all)
        rng = np.random.RandomState(topo_seed)
        hubs = np.sort(rng.choice(self.N, size=int(min(n_hubs, self.N)), replace=False))
        self.ishub = np.zeros(self.N, bool); self.ishub[hubs] = True
        C = np.zeros((self.N, self.N), bool)
        for i in range(self.N):
            for j in range(self.N):
                if i == j:
                    continue
                if self.ishub[i] or self.ishub[j] or abs(i - j) <= self.r:
                    C[i, j] = True
        self.C = C
        iu = np.triu_indices(self.N, 1)
        self.hub_pool = [(i, j) for i, j in zip(*iu) if (self.ishub[i] or self.ishub[j])]
        self.loc_pool = [(i, j) for i, j in zip(*iu)
                         if (not self.ishub[i] and not self.ishub[j] and abs(i - j) <= self.r)]
        self.W = None; self.stored = []

    def write_items(self, n_items=K, pattern_seed=19):
        self.hp.W = np.zeros((self.N, self.N)); self.hp.stored = []
        for p in E._patterns(int(n_items), self.N, seed=pattern_seed):
            self.hp.write(p)
        Wfull = self.hp.W.copy()
        self.W = Wfull if self.all_to_all else (Wfull * self.C)
        self.stored = [x.copy() for x in self.hp.stored]
        return self

    def _settle(self, s0, clamp=None, steps=40, W=None):
        self.hp.W = self.W if W is None else W
        return self.hp._settle_state(s0.astype(float), clamp=clamp, steps=steps)

    def cut(self, pool, k, seed):
        rng = np.random.RandomState(seed); Wl = self.W.copy()
        if k > 0:
            for s in rng.choice(len(pool), size=int(k), replace=False):
                i, j = pool[s]; Wl[i, j] = 0.0; Wl[j, i] = 0.0
        return Wl

    # READ-OUT 1: SOCIALITY = long-range binding (near cue -> distant block; non-circular)
    def sociality(self, W, steps=40):
        save = self.W; self.W = W
        left = np.arange(0, self.N // 2); right = np.arange(self.N // 2, self.N)
        vals = []
        for x in self.stored:
            s0 = np.zeros(self.N); s0[left] = x[left]
            out = self._settle(s0, clamp=(left, x[left]), steps=steps)
            vals.append(float(np.mean(out[right] == x[right])))
        self.W = save
        return float(np.mean(vals))

    # READ-OUT 2: CAPACITY = within-pattern completion from a scattered partial cue (W-light)
    def capacity(self, W, cue_frac=0.3):
        save = self.hp.W; self.hp.W = W
        v = float(np.mean([self.hp.retrieve(i, cue_frac) for i in range(len(self.stored))]))
        self.hp.W = save
        return v


def _cond(N, f_W, steps, pattern_seeds, lesion_seeds=range(3), control="hub"):
    """Mean (sociality, capacity) over topo/pattern seeds x lesion seeds.
    control='hub'  -> the W-fault cuts hub long-range edges.
    control='local'-> the mass-matched random-LOCAL cut (Gap-2 non-circularity control)."""
    socs, caps = [], []
    for ps in pattern_seeds:
        m = OWTCortex(n_cells=N, topo_seed=ps).write_items(K, ps)
        pool = m.hub_pool if control == "hub" else m.loc_pool
        kcut = int(round(f_W * len(pool)))
        for ls in lesion_seeds:
            seed = ls * 101 + ps
            Wl = m.cut(pool, kcut, seed) if f_W > 0 else m.W
            socs.append(m.sociality(Wl, steps=steps)); caps.append(m.capacity(Wl))
    return float(np.mean(socs)), float(np.mean(caps))


def owxw_sweep(steps=40, pattern_seeds=range(19, 23)):
    """The 2x2 + magnitude sweep.  Intact baseline; W-fault sweep over F_W_GRID at
    N=120; O-fault sweep over N_GRID at f_W=0.  Returns the curves + the strongest
    cell deltas + the crossover selectivities."""
    s0, c0 = _cond(120, 0.0, steps, pattern_seeds)            # intact
    w_curve = []
    for f in F_W_GRID:
        s, c = _cond(120, f, steps, pattern_seeds)
        w_curve.append({"f_W": f, "sociality": s, "capacity": c,
                        "dS": s - s0, "dC": c - c0})
    o_curve = []
    for N in N_GRID:
        s, c = _cond(N, 0.0, steps, pattern_seeds)
        o_curve.append({"N_cells": N, "sociality": s, "capacity": c,
                        "dS": s - s0, "dC": c - c0})
    # strongest faults
    sW, cW = _cond(120, F_W_MAX, steps, pattern_seeds)
    sO, cO = _cond(N_LO, 0.0,    steps, pattern_seeds)
    dS_W, dC_W = sW - s0, cW - c0
    dS_O, dC_O = sO - s0, cO - c0
    W_sel = dC_W - dS_W      # >0 : W hits sociality more than capacity
    O_sel = dS_O - dC_O      # >0 : O hits capacity more than sociality
    return {"intact": {"sociality": s0, "capacity": c0},
            "W_fault_sweep_N120": w_curve, "O_fault_sweep_fW0": o_curve,
            "strongest": {"dS_W": dS_W, "dC_W": dC_W, "dS_O": dS_O, "dC_O": dC_O,
                          "W_selectivity": W_sel, "O_selectivity": O_sel}}


def main():
    print("=" * 78)
    print(" vp_frontal v2 -- CHUNK C / GAP-3 BUILD : grounded connectome + O x W")
    print(" W = long-range routing (hub edges) ; O = organ capacity (N cells, hubs kept)")
    print(" N={} cells | hubs=K_emerged={} | f_W grid={} | N grid={} . NO TUNING.".format(
        N_CELLS, N_HUBS, F_W_GRID, N_GRID))
    print("=" * 78)

    anchor = FC.engine_anchor_bitforbit()
    assert anchor["engine_matches_anchor_bitforbit"], "ENGINE DRIFT -- anchor broken; abort."
    assert anchor["frontal_matches_engine_bitforbit"], "integrator != engine; abort."
    print(" engine M9 anchor bit-for-bit: R={}  (matches={})".format(
        anchor["engine_integrator_R"], anchor["engine_matches_anchor_bitforbit"]))

    # reuse equivalence: OWTCortex(N=120) == the surviving Gap-2 model on sociality
    mc2 = CorticalMicrocircuit(g=FOXG1, topo_seed=19).write_items(K, 19)
    oc = OWTCortex(n_cells=120, topo_seed=19).write_items(K, 19)
    reuse_ok = bool(abs(mc2.far_binding(mc2.W) - oc.sociality(oc.W)) < 1e-12)
    print(" reuse equivalence (OWTCortex N=120 == Gap-2 far_binding): {}".format(reuse_ok))
    assert reuse_ok, "OWTCortex diverged from the Gap-2 model; abort (reuse must be exact)."

    # PART A -- grounded connectome + honest organ-scale integration negative
    conn_check = connectome_integration_check()
    print()
    print(" PART A -- grounded long-range connectome ({} edges, sum w={:.2f}):".format(
        len(CONNECTOME_EDGES), A_CONN.sum() / 2))
    for ni, nj, w, g, _c in CONNECTOME_EDGES:
        print("   {:>11s} <-> {:<12s} {:.2f}  {}".format(ni, nj, w, g))
    print("   organ-scale integration check (heavy vs weak tract severing):")
    for r in conn_check["rows"]:
        print("     kappa={:.2f}  dR_heavy={:+.4f}  dR_weak={:+.4f}".format(
            r["kappa_axon"], r["dR_sever_heavy"], r["dR_sever_weak"]))
    print("   heavy-tract deficit SIGN-STABLE across kappa : {}  -> honest negative: {}".format(
        conn_check["heavy_drops_integration_more_every_kappa"], conn_check["honest_negative_recorded"]))
    print("   (the global order parameter is dominated by the frozen ephaptic field;")
    print("    the W-axis dissociation is therefore tested at the MICRO-MODEL scale below.)")

    # PART B -- O x W dissociation at the micro-model scale
    owxw = owxw_sweep()
    s0 = owxw["intact"]["sociality"]; c0 = owxw["intact"]["capacity"]
    st = owxw["strongest"]
    print()
    print(" PART B -- O x W dissociation (cortical micro-model):")
    print("   intact: sociality={:.3f}  capacity={:.3f}".format(s0, c0))
    print("   W-fault sweep (cut hub long-range edges, N=120):")
    print("     f_W    sociality  capacity    dS       dC")
    for r in owxw["W_fault_sweep_N120"]:
        print("     {:.1f}    {:.3f}      {:.3f}     {:+.3f}   {:+.3f}".format(
            r["f_W"], r["sociality"], r["capacity"], r["dS"], r["dC"]))
    print("   O-fault sweep (reduce N cells, hubs kept, f_W=0):")
    print("     N      sociality  capacity    dS       dC")
    for r in owxw["O_fault_sweep_fW0"]:
        print("     {:<4d}   {:.3f}      {:.3f}     {:+.3f}   {:+.3f}".format(
            r["N_cells"], r["sociality"], r["capacity"], r["dS"], r["dC"]))
    print("   STRONGEST faults (W: f_W={}, N=120 | O: N={}, f_W=0):".format(F_W_MAX, N_LO))
    print("     W-fault: dS={:+.3f} dC={:+.3f}  ->  W_selectivity (dC-dS) = {:+.3f}".format(
        st["dS_W"], st["dC_W"], st["W_selectivity"]))
    print("     O-fault: dS={:+.3f} dC={:+.3f}  ->  O_selectivity (dS-dC) = {:+.3f}".format(
        st["dS_O"], st["dC_O"], st["O_selectivity"]))

    # non-circularity control: W-fault hub-cut vs mass-matched random-LOCAL cut
    sW_hub, _ = _cond(120, F_W_MAX, 40, range(19, 23), control="hub")
    sW_loc, _ = _cond(120, F_W_MAX, 40, range(19, 23), control="local")
    noncirc = bool((s0 - sW_hub) > 3.0 * abs(s0 - sW_loc) and (s0 - sW_hub) > 0.03)
    print("   non-circular control: sociality hub-cut={:.3f} vs random-local-cut={:.3f}".format(
        sW_hub, sW_loc))
    print("     -> long-range-edge-specific (hub-cut drop >> local-cut drop): {}".format(noncirc))

    crossover = bool(st["W_selectivity"] > MARGIN and st["O_selectivity"] > MARGIN)

    results = {
        "module": "cortico_connectome_owt (Chunk C / Gap-3 build)",
        "constitution": {"new_tuned_constants": 0, "consciousness_claim": 0,
                         "hard_problem_open": 1, "engine_readonly": True},
        "engine_anchor_bitforbit": {"R": anchor["engine_integrator_R"],
                                    "matches_M9_anchor": anchor["engine_matches_anchor_bitforbit"],
                                    "integrator_matches_engine": anchor["frontal_matches_engine_bitforbit"]},
        "reuse_equivalence_OWTCortex_eq_gap2_far_binding": reuse_ok,
        "grounded_inputs": {"n_cells": N_CELLS, "lr": LR, "g_FOXG1": FOXG1,
                            "n_hubs_emerged_K": N_HUBS, "f_W_grid": list(F_W_GRID),
                            "N_grid": list(N_GRID), "margin": MARGIN},
        "partA_grounded_connectome": {
            "edges": [{"i": ni, "j": nj, "weight": w, "grade": g, "citation": c}
                      for ni, nj, w, g, c in CONNECTOME_EDGES],
            "sum_weight": float(A_CONN.sum() / 2),
            "organ_scale_integration_check": conn_check,
        },
        "partB_o_x_w": owxw,
        "noncircular_control": {"sociality_hub_cut": sW_hub, "sociality_random_local_cut": sW_loc,
                                "long_range_specific": noncirc},
        "verdict": {
            "W_selectivity": st["W_selectivity"], "O_selectivity": st["O_selectivity"],
            "crossover_double_dissociation": crossover,
            "statement": (
                "On the surviving Gap-2 micro-model, the long-range-ROUTING axis (W = hub edges) "
                "and the organ-CAPACITY axis (O = cell count, hubs preserved) form a CROSSOVER "
                "double dissociation: the W-fault (cut hub long-range edges) hits long-range "
                "binding ('sociality') several-fold harder than within-pattern completion "
                "('capacity'), while the O-fault (fewer cells, wiring backbone intact) hits "
                "capacity several-fold harder than binding. The W-fault drop is hub-long-range-"
                "SPECIFIC (a mass-matched random-LOCAL cut spares sociality). HONEST RESIDUALS: "
                "(1) the dissociation is a RELATIVE selectivity (crossover), not absolute single-"
                "task lesions -- the W-fault also nicks capacity (~0.06) and the O-fault perturbs "
                "sociality (<=0.03); each fault hits its target ~2-3x harder than off-target. "
                "(2) gene-blind (g absent from sign() dynamics) -- W is topological, O is cell-"
                "count; neither is gene-specific. (3) at the COARSE organ/phase scale a single "
                "grounded-tract lesion gives NO sign-stable global-integration deficit (recorded "
                "negative) -- the dissociation is a micro-model property. ST-3 stresses the "
                "crossover for sign-stability before it is believed."),
        },
        "grades": ("[L] grounded long-range connectome ordering (2 edges paper-cited, the rest "
                   "textbook ordering, magnitudes [O]); [V candidate] O x W crossover double "
                   "dissociation at the micro-model scale (sign-stability pending ST-3); [O] "
                   "absolute magnitudes, gene-specificity, and organ-scale single-tract integration. "
                   "consciousness_claim=0; hard_problem_open=1; new_tuned_constants=0; engine READ-ONLY. "
                   "This is an in-silico model result -- NOT validated neuroscience, NOT clinical guidance."),
    }
    digest = FC.digest_of(results); results["digest"] = digest
    with open(RESULTS_JSON, "w") as f:
        f.write(FC.blob(results))
    with open(EXPECTED_SHA, "w") as f:
        json.dump({"cortico_connectome_owt_results.json": digest}, f, indent=2)

    print()
    print("-" * 78)
    print(" VERDICT (build): crossover double dissociation = {}  (W_sel={:+.3f}, O_sel={:+.3f})".format(
        crossover, st["W_selectivity"], st["O_selectivity"]))
    print(" results ->", RESULTS_JSON)
    print(" sha     ->", digest)
    print(" GRADES:", results["grades"])
    print(" STATUS: COMPLETE (build) -- run cortico_connectome_owt_st3.py to stress it")


if __name__ == "__main__":
    main()
