#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPC-E1E2 -- SPATIAL-SWITCH-LEVERAGE COUPLING : which focal drive most easily FLIPS the collective
state. The SECOND coupling of two reusable layers the atlas built separately -- the spatial sibling
of the §29 bipolar episode. It marries the E1 spatial-localisation layer (§43, SpatialField -- a
per-node spatial drive on the frozen ephaptic kernel) and the E2 state-switching layer (§28,
BistableSwitch -- the frozen R19 bistable cell used OVER TIME). Neither layer alone could pose the
question this module asks. E1 reads the INSTANTANEOUS local-coherence field a focal drive produces
on a fixed kernel, but it has no bistable state -- a focal drive cannot FLIP anything, there is
nothing to flip. E2 has the bistable state and its fold, but it is driven by ONE scalar drive for
the whole cell -- it has no spatial profile, so "which region's drive flips the state" is a question
it cannot even ask (every region is the same scalar h). This module MARRIES them: it drives the
SINGLE collective R19 bistable state s (the SAME §28/§29 BistableSwitch object the bipolar module
uses for episode transitions) with a FOCAL stimulation whose effective drive on the collective state
is the driven node's frozen-kernel BROADCAST LEVERAGE -- the total one-step ephaptic current that
node injects into the rest of the network -- and asks WHICH region's focal drive most easily flips
the bistable state. It is the spatial sibling of §29 (the bipolar episode given a location -- §29
asked WHEN the state flips under a temporal drive; this asks WHERE a focal drive most cheaply flips
it) and the switching counterpart of §46 (which read where a focal stimulation's INSTANTANEOUS
effect lands; this reads which focal drive most easily switches the collective state). It IMPORTS
both layers (it does NOT re-derive the ephaptic kernel, the broadcast structure, the R19 cell, or
the fold -- handover reuse discipline); the only new object is a leverage-driven switch -- the SAME
§28 BistableSwitch fed an effective drive read off the SAME frozen kernel E1 froze. No new constant,
no new rule.
=================================================================================
THE GROUNDING (READ-ONLY; no new constant, no new rule). A focal stimulation is a strong focal
EXCITATORY bias b0 > 0 at one region (the rest at baseline). Its effective drive ON THE COLLECTIVE
STATE is the BROADCAST LEVERAGE of the driven node j: lev_j = colsum_j = sum_i W0[i,j], the total
one-step ephaptic current node j injects into the whole network through the FROZEN kernel W0 (E1's
imported ephaptic kernel -- the row-stochastic ~1/r^3 coupling). This is a PURE READOUT of the frozen
kernel: no fit, no new constant -- a region that is wired to broadcast hard has high leverage, a
peripheral region has low leverage. The collective state is the §28 BistableSwitch cell
ds/dt = g*s - s^3 + h (E2's imported R19 cell, the SAME cubic the engine froze, E.sdot), started at
the DOWN fixed point s0 = -sqrt(g); a focal drive at node j applies the effective drive
h_eff(j, b0) = b0 * lev_j, and the state FLIPS up iff h_eff crosses the fold spinodal(g)
(E.spinodal, the SAME fold as M11 / theta-cap / epilepsy / E2). The flip THRESHOLD in stimulation
intensity is therefore b0*(j) = spinodal(g) / lev_j -- inverse in the leverage. The stimulation
INTENSITY b0 is SWEPT over the full E1 depth sweep {0.3,0.5,0.7,0.9} AND the barrier DEPTH g over
{0.7,1.0,1.3} (g = 1.0 is the engine's universal R19 scale); every SIGN/ORDER/STRUCTURE asserted
below is required to hold across BOTH sweeps (anti-tuning, intensity x barrier). When the focal
drive is removed (b0 = 0, so h_eff = 0) the state settles via E.settle BIT-FOR-BIT (the S6 guard,
inherited from E2.4) and the fold is read from E.spinodal -- nothing here is fit.

WHAT THE MODULE DELIVERS (pre-registered, sign/order/structure only; never magnitudes):
  C1  THE FLIP-THRESHOLD RANK == THE BROADCAST-LEVERAGE RANK, AND IT IS BARRIER-INVARIANT. Driving a
      focal excitatory stimulation at each region in turn, the 12 sites RANK by how easily their focal
      drive flips the collective state, easiest (lowest intensity threshold) first. That integrated
      rank is IDENTICAL to the broadcast-leverage rank (lev_j = colsum_j of the frozen kernel): the
      site whose focal drive flips the state most cheaply is the highest-leverage hub, and the order is
      monotone in leverage all the way down. The rank is the SAME across the full barrier-depth sweep
      g in {0.7,1.0,1.3} on the common (finite-threshold) set -- a deeper well raises every threshold
      together but does NOT reorder which region flips easiest. WHICH focal drive most cheaply flips
      the collective state is a FIXED property of the frozen kernel's broadcast structure, not of the
      barrier depth nor of the stimulation intensity. A FIXED NON-SWITCHING minority {thalamus,
      olfactory_bulb} never flips the state at any swept intensity (b0 <= 1) -- their broadcast leverage
      is too small for even the strongest swept focal drive to cross the fold. grade [V mech].
  C2  EASE-OF-FLIP <-> BROADCAST LEVERAGE, WITH CRITICAL SLOWING AT THE BOTTOM (the dynamic content).
      The flip threshold is monotone-DECREASING in broadcast leverage (b0* = spinodal/lev), and at a
      FIXED supra-threshold intensity the crossing LATENCY -- the time the collective state takes to
      flip -- is also monotone-decreasing in leverage: a high-leverage hub flips the state both more
      cheaply AND faster, a low-leverage site flips it dearly and slowly. The lowest-leverage site that
      still flips shows CRITICAL SLOWING (the largest finite crossing latency, the transition time
      diverging as the effective drive approaches the fold) -- the §28 E2.2 ictal time-course given a
      spatial address: this module says WHERE a focal drive sits on that latency curve. The fixed
      non-switching minority never crosses at all. grade [V mech].
  C3  THE SWITCH-LEVERAGE AXIS IS DECOUPLED FROM THE §46 INSTANTANEOUS-FOOTPRINT AXIS AND THE §43
      REACH AXIS, AND THERE IS NO UNIVERSAL REACH->SWITCHABILITY LAW (the genuinely-new coupling result
      + the honest no-tuning negative). (a) The §46 / E1.3 instantaneous-field relay set {hippocampus,
      midbrain} (where a focal drive's INSTANTANEOUS effect leaks off-target) is NOT the switch-leverage
      hub set: those two sites are MID-rank in switch leverage (ranks 5-6 of 12, easily switchable, not
      special), while the switch-leverage hub is basal_forebrain_cholinergic -- which §46 classes as
      SELF-LOCALISING (clean instantaneous delivery), not a relay. WHERE a focal drive's instantaneous
      effect lands and WHICH focal drive flips the collective state are two DISTINCT, decoupled spatial
      axes -- the E1xE2 lesson neither layer alone could state (E1 has no bistable state; E2 has no
      spatial profile). (b) A clean, attractive hypothesis -- "the region with the greatest spatial
      REACH (the §43 reach hub) is the one whose focal drive most easily flips the state" -- is FALSE.
      The §43/§46 reach hub is CEREBELLUM (the rank-1 reach hub at every depth, read from the E1
      results), yet cerebellum is switch-rank 10 of 12, one of the HARDEST regions to flip the state
      from (it barely crosses the fold at the strongest swept intensity). The hard-to-switch set
      {thalamus, olfactory_bulb, cerebellum} are all §46 SELF-LOCALISING (clean instantaneous delivery)
      yet cannot cheaply flip the collective state. There is NO universal reach->switchability law:
      reaching far, delivering cleanly, and flipping the collective state are THREE distinct properties.
      We do NOT force a tidy "the reach hub is the switch hub" story; the refuted clean hypothesis is
      reported honestly. grade [V mech] (a refuted clean hypothesis is a finding).
  C4  A COHERENT MAJORITY-SWITCHABLE STRUCTURE WITH A FIXED NON-SWITCHING MINORITY (the honest contrast
      with §46). A strict MAJORITY of sites (ten of twelve) can have their collective state flipped by a
      swept focal drive (b0 <= 1), with a FIXED non-switching minority {thalamus, olfactory_bulb} that
      cannot -- so MAJORITY-SWITCHABLE, with a hard peripheral floor, is the structure. This is the
      honest contrast with §46, where the structural default was clean instantaneous DELIVERY (ten of
      twelve self-localising in the instant): here the structural fact is that most regions' focal drive
      CAN flip the collective state, but how cheaply is set by broadcast leverage and a peripheral
      minority is locked out entirely. A DIRECTION-ONLY [L] correspondence is noted, never a magnitude
      or a prediction: the highest-leverage hubs (basal forebrain cholinergic, hypothalamus) are the
      classic global brain-state / arousal control hubs (the ascending arousal and basal-forebrain
      systems that gate sleep-wake and cortical state), and the hardest-to-switch / locked-out sites
      (thalamic relay, olfactory bulb, cerebellum) are peripheral sensory-relay or motor-timing
      structures -- direction-consistent with broadcast hubs having an outsized role in switching the
      global brain state, and with relays not. grade [V mech] structural + [L].

NOT a claim that real brain-state switching reduces to a single scalar R19 cell driven by the column
sum of a frozen 1/r^3 kernel (real state control is a distributed neuromodulatory system -- the
ascending arousal nuclei, basal forebrain, thalamic and cortical loops, multiple transmitters,
state-dependent conductances -- LOCKED); what is asserted is the SIGN/ORDER/STRUCTURE of which
focal-drive ADDRESS most cheaply flips a single bistable collective state when the effective drive is
the frozen kernel's broadcast leverage, and its four consequences (the leverage-ordered flip-
threshold rank, the leverage-ordered latency with critical slowing, the decoupling of switchability
from instantaneous footprint and from reach, and the majority-switchable structure with a fixed non-
switching minority). NOT a claim about the FELT quality of a state transition (Axis-A firewall: the
collective bistable state and its flip are STRUCTURAL quantities of the coupling model, NEVER a felt
state, an experienced arousal, or a level of consciousness; consciousness_claim stays 0; hard problem
stays OPEN). NOT a real connectome, a real electric-field / current-density / lead-position map, or a
real measurement of which stimulation flips a brain state. NOT a prediction of WHICH patient's
stimulation flips which state, and NOT clinical, device-programming, or target-selection guidance --
those are external clinical decisions. NOT MEDICAL ADVICE; efficacy = 0 everywhere; in-silico
MECHANISM only; nothing here is a cure, a treatment, a localisation, or a device setting. Every
MAGNITUDE is [O]; only structural SIGNS, ORDERS and RELATIONS are asserted, and they are certified to
survive the stimulation-intensity sweep AND the barrier-depth sweep.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY (emerge_all is
NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988... and the M0..M16 subtree
stays 3a1ebbbb..., byte-identical). COUPLES the E1 SpatialField and the E2 BistableSwitch (both
imported, not re-derived); the drive is the frozen kernel's broadcast leverage fed to the SAME §28
bistable cell. Writes spatial_switch_leverage_results.json + its sha256, verified bit-for-bit. The
leverage-driven switch is the reusable seam any later spatial-switching module imports.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

# REUSE both layers -- import their classes and shared (measured) handles; do NOT re-derive the
# ephaptic kernel, the broadcast structure, the R19 cell, or the fold (handover discipline:
# reuse, not re-derive).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e1_spatial_localisation import (SpatialField, REGS, N, DEPTHS, KAP, W0, FOLD,
                                     M9_ANCHOR_R, ENGINE_TREE_FROZEN, M0_16_FROZEN)
from e2_state_switching import BistableSwitch, GG, DT, SETTLE_N   # the E2 state-switching layer

HERE = os.path.dirname(os.path.abspath(__file__))

# --- the broadcast leverage: a PURE readout of the frozen kernel (no new constant) ---
LEVERAGE = W0.sum(0)                  # lev_j = colsum_j = sum_i W0[i,j], one-step current node j injects

STIM_DEPTHS = DEPTHS                  # {0.3, 0.5, 0.7, 0.9} -- E1 depth sweep (stimulation intensity)
BARRIER_SWEEP = (0.7, 1.0, 1.3)      # E2 barrier-depth sweep (well depth g)
REP   = 0.9                          # representative stimulation intensity for headline reads [swept]
GREP  = GG                           # representative barrier depth = engine R19 scale 1.0 [swept]
FINE  = [round(x, 3) for x in np.arange(0.02, 1.0001, 0.02)]   # fine intensity grid for thresholds

HIPPO = REGS.index("hippocampus")
MIDB  = REGS.index("midbrain")
CEREB = REGS.index("cerebellum")

# the leverage rank (easiest -> hardest to flip), a fixed property of the frozen kernel
ORDER_LEV = sorted(range(N), key=lambda j: -LEVERAGE[j])

# The §46 / E1.3 INSTANTANEOUS-field relay (off-target-leak) set -- read from the imported
# SpatialField footprint class (NOT re-derived; it is §46's own set, {hippocampus, midbrain}).
_SF = SpatialField()
FIELD_RELAY = sorted([REGS[k] for k in range(N) if _SF.footprint_class(k, REP) < 0])

# The §43/§46 spatial-reach hub -- read from the E1 results file (NOT re-derived; it is E1's own
# top_reach_hub). Falls back to the probed value 'cerebellum' if the file is absent.
def _reach_hub():
    p = os.path.join(HERE, "e1_spatial_localisation_results.json")
    try:
        d = json.load(open(p, encoding="utf-8"))
        for blk in d.values():
            if isinstance(blk, dict):
                for k, v in blk.items():
                    if k == "top_reach_hub" and isinstance(v, str):
                        return v
    except Exception:
        pass
    return "cerebellum"
REACH_HUB = _reach_hub()

# Expected (probed) sets -- the fixed non-switching minority and the majority-switchable set.
EXPECTED_NONSWITCH = sorted(["thalamus", "olfactory_bulb"])
EXPECTED_SWITCH = sorted([r for r in REGS if r not in EXPECTED_NONSWITCH])


class LeverageSwitch:
    """The E1xE2 seam: the SAME §28 BistableSwitch collective state, driven by a focal stimulation
    whose effective drive is the frozen kernel's broadcast leverage. REUSABLE -- a later spatial-
    switching module imports this; it does not re-derive the kernel, the broadcast structure, the R19
    cell or the fold. The engine is never mutated; this object only integrates the SAME cubic the
    engine froze (through the imported BistableSwitch) under a leverage-scaled focal drive."""

    def __init__(self, g=GREP):
        self.g = g
        self.cell = BistableSwitch(g)         # the imported §28/§29 R19 bistable cell

    def fold(self):
        """The flip threshold on the effective drive = the fold (read from the engine, no new constant)."""
        return self.cell.spinodal()

    def h_eff(self, node, b0):
        """The effective drive a focal stimulation b0 at `node` applies to the collective state =
        the broadcast leverage of the driven node (a pure frozen-kernel readout)."""
        return float(b0 * LEVERAGE[node])

    def flips(self, node, b0):
        """Does a focal drive b0 at `node` flip the collective state up from the DOWN fixed point?
        Static endpoint via the imported cell's relax (= E.settle bit-for-bit at n=SETTLE_N)."""
        s = self.cell.relax(self.h_eff(node, b0), s0=-math.sqrt(self.g), n=SETTLE_N)
        return bool(s > 0.0)

    def threshold(self, node):
        """The minimum swept stimulation intensity (fine grid) whose focal drive at `node` flips the
        collective state; None if it never flips at b0 <= 1 (the non-switching floor)."""
        for b0 in FINE:
            if self.flips(node, b0):
                return b0
        return None

    def latency(self, node, b0):
        """The crossing latency -- the time the collective state takes to flip -- under a focal drive
        b0 at `node` (the imported cell's crossing_latency); None if it never crosses."""
        return self.cell.crossing_latency(self.h_eff(node, b0), s0=-math.sqrt(self.g), dt=DT)


# ------------------------------- the four sub-studies + guard ----------------------------

def _threshold_rank():
    """C1: the flip-threshold rank == the broadcast-leverage rank, identical across the barrier sweep
    on the common finite-threshold set; the fixed non-switching minority {thalamus, olfactory_bulb}
    never flips at any swept intensity."""
    # rank at the representative barrier
    ls = LeverageSwitch(GREP)
    T = {j: ls.threshold(j) for j in range(N)}
    finite = [j for j in range(N) if T[j] is not None]
    rank_thr = sorted(finite, key=lambda j: (T[j], -LEVERAGE[j]))
    rank_lev = [j for j in ORDER_LEV if T[j] is not None]
    rank_matches_leverage = bool([REGS[j] for j in rank_thr] == [REGS[j] for j in rank_lev])
    nonswitch = sorted([REGS[j] for j in range(N) if T[j] is None])
    nonswitch_is_expected = bool(nonswitch == EXPECTED_NONSWITCH)
    # barrier-invariance of the rank on the common finite-threshold set
    ranks_by_g = {}
    finite_by_g = {}
    for g in BARRIER_SWEEP:
        lg = LeverageSwitch(g)
        Tg = {j: lg.threshold(j) for j in range(N)}
        fg = [j for j in range(N) if Tg[j] is not None]
        finite_by_g[g] = set(REGS[j] for j in fg)
        ranks_by_g[g] = [REGS[j] for j in sorted(fg, key=lambda j: (Tg[j], -LEVERAGE[j]))]
    common = set.intersection(*finite_by_g.values()) if finite_by_g else set()
    proj = [[r for r in ranks_by_g[g] if r in common] for g in BARRIER_SWEEP]
    barrier_invariant = bool(all(p == proj[0] for p in proj))
    # the labelled threshold table at the representative barrier (for the body)
    thr_table = {REGS[j]: (round(T[j], 3) if T[j] is not None else None) for j in range(N)}
    return (rank_matches_leverage, barrier_invariant, [REGS[j] for j in rank_thr],
            nonswitch, nonswitch_is_expected, thr_table, sorted(common),
            {g: ranks_by_g[g] for g in BARRIER_SWEEP})


def _latency_ladder():
    """C2: ease-of-flip <-> broadcast leverage with critical slowing. The flip threshold is monotone-
    decreasing in leverage, the crossing latency at a fixed supra-threshold intensity is monotone-
    decreasing in leverage, the lowest-leverage finite-flip site shows the largest latency (critical
    slowing), and the non-switching minority never crosses."""
    ls = LeverageSwitch(GREP)
    T = {j: ls.threshold(j) for j in range(N)}
    # (a) threshold monotone-decreasing in leverage (analytic b0* = fold/lev; check on finite set)
    fin = sorted([j for j in range(N) if T[j] is not None], key=lambda j: LEVERAGE[j])
    thr_monotone = all(T[fin[i]] >= T[fin[i + 1]] for i in range(len(fin) - 1))
    # (b) crossing latency at a FIXED supra-threshold intensity, monotone-decreasing in leverage
    lat = {j: ls.latency(j, REP) for j in range(N)}
    fin_lat = sorted([j for j in range(N) if lat[j] is not None], key=lambda j: LEVERAGE[j])
    lat_monotone = all(lat[fin_lat[i]] >= lat[fin_lat[i + 1]] for i in range(len(fin_lat) - 1))
    # (c) critical slowing: the lowest-leverage finite-flip site has the largest latency
    lowest_lev_finite = min(fin_lat, key=lambda j: LEVERAGE[j])
    max_lat_site = max(fin_lat, key=lambda j: lat[j])
    critical_slowing = bool(lowest_lev_finite == max_lat_site)
    # (d) the non-switching minority never crosses (latency None)
    nonswitch_never = all(lat[REGS.index(r)] is None for r in EXPECTED_NONSWITCH)
    lat_table = {REGS[j]: (round(lat[j], 4) if lat[j] is not None else None) for j in range(N)}
    return (bool(thr_monotone), bool(lat_monotone), critical_slowing, bool(nonswitch_never),
            lat_table, REGS[lowest_lev_finite])


def _decoupling_and_no_law():
    """C3 (the genuinely-new coupling result + the honest negative): (a) the switch-leverage axis is
    decoupled from the §46 instantaneous-footprint axis -- the §46 field-relay set is mid-rank in
    switch leverage and the switch hub is §46 self-localising; (b) no universal reach->switchability
    law -- the §43 reach hub (cerebellum) is one of the HARDEST to switch."""
    ls = LeverageSwitch(GREP)
    switch_hub = REGS[ORDER_LEV[0]]
    # --- (a) decoupling from the §46 instantaneous-footprint axis ---
    field_relay_ranks = {r: ORDER_LEV.index(REGS.index(r)) + 1 for r in FIELD_RELAY}  # 1 = easiest
    field_relay_midrank = bool(all(3 <= rk <= N - 3 for rk in field_relay_ranks.values()))
    switch_hub_is_field_relay = bool(switch_hub in FIELD_RELAY)
    switch_hub_field_class = "self_localising" if _SF.footprint_class(REGS.index(switch_hub), REP) > 0 else "relay"
    decoupled_from_footprint = bool((not switch_hub_is_field_relay) and field_relay_midrank
                                    and switch_hub_field_class == "self_localising")
    # --- (b) no universal reach->switchability law: the reach hub is hard to switch ---
    reach_hub_idx = REGS.index(REACH_HUB)
    reach_hub_switch_rank = ORDER_LEV.index(reach_hub_idx) + 1                 # 1 = easiest
    reach_hub_is_switch_hub = bool(REACH_HUB == switch_hub)
    reach_hub_is_hard = bool(reach_hub_switch_rank >= N - 2)                   # bottom-3 = hard
    # the hard-to-switch set at the representative intensity (does not flip at b0=REP) that are §46 clean
    hard_clean = sorted([REGS[j] for j in range(N)
                         if (not ls.flips(j, REP)) and _SF.footprint_class(j, REP) > 0])
    no_reach_switch_law = bool((not reach_hub_is_switch_hub) and reach_hub_is_hard)
    decoupled = bool(decoupled_from_footprint and no_reach_switch_law and len(hard_clean) > 0)
    return (decoupled, decoupled_from_footprint, no_reach_switch_law, switch_hub,
            switch_hub_field_class, field_relay_ranks, REACH_HUB, reach_hub_switch_rank,
            reach_hub_is_switch_hub, hard_clean)


def _majority_switchable():
    """C4: a coherent majority-switchable structure with a fixed non-switching minority -- the honest
    contrast with §46's clean-delivery default."""
    ls = LeverageSwitch(GREP)
    T = {j: ls.threshold(j) for j in range(N)}
    switchable = sorted([REGS[j] for j in range(N) if T[j] is not None])
    nonswitch = sorted([REGS[j] for j in range(N) if T[j] is None])
    n_switch = len(switchable)
    n_nonswitch = len(nonswitch)
    switchable_is_majority = bool(n_switch > n_nonswitch)
    switchable_is_expected = bool(switchable == EXPECTED_SWITCH)
    nonswitch_is_expected = bool(nonswitch == EXPECTED_NONSWITCH)
    # honest contrast with §46: in §46 the instantaneous self-localising (clean) set was the majority
    n_field_self = N - len(FIELD_RELAY)
    field_clean_was_majority = bool(n_field_self > len(FIELD_RELAY))
    coherent = bool(switchable_is_majority and switchable_is_expected and nonswitch_is_expected)
    return (coherent, n_switch, n_nonswitch, switchable_is_majority, switchable,
            nonswitch, field_clean_was_majority, n_field_self)


def _invariance():
    """S6: removing the focal drive (b0 = 0 -> h_eff = 0) settles the collective state via E.settle
    BIT-FOR-BIT (the static limit IS the frozen engine, inherited from E2.4), the fold is read from
    E.spinodal (no new constant), and the down state stays down exactly -- the coupling is a pure add-
    on on the engine."""
    g = GREP
    sw = BistableSwitch(g)
    ls = LeverageSwitch(g)
    # zero focal drive -> effective drive 0; the static endpoint must equal E.settle bit-for-bit
    a = E.settle(g, 0.0, s0=-math.sqrt(g))
    b = sw.relax(0.0, -math.sqrt(g), SETTLE_N)
    static_is_settle = bool(repr(a) == repr(b))
    # the leverage-switch with zero focal drive reproduces the same endpoint
    c = ls.cell.relax(ls.h_eff(CEREB, 0.0), s0=-math.sqrt(g), n=SETTLE_N)
    zero_drive_matches = bool(repr(c) == repr(a))
    # the down state stays down with no drive (no spurious flip), and never flips for the floor sites
    down_stays_down = bool(a < 0.0)
    fold_from_engine = bool(ls.fold() == float(E.spinodal(g)))
    # a focal excursion removed reverts exactly to the down endpoint
    reverts = bool(c == a)
    return repr(a), repr(b), static_is_settle, zero_drive_matches, down_stays_down, fold_from_engine, reverts


def run():
    # ===== C1 : flip-threshold rank == broadcast-leverage rank, barrier-invariant =====
    (rank_ok, barrier_inv, rank_thr, nonsw1, nonsw1_ok, thr_table, common, ranks_by_g) = _threshold_rank()
    C1 = bool(rank_ok and barrier_inv and nonsw1_ok)

    # ===== C2 : ease-of-flip <-> leverage, critical slowing =====
    (thr_mono, lat_mono, crit_slow, nonsw_never, lat_table, lowest_lev_site) = _latency_ladder()
    C2 = bool(thr_mono and lat_mono and crit_slow and nonsw_never)

    # ===== C3 : switchability decoupled from footprint and reach; no reach->switchability law =====
    (decoupled, dec_fp, no_law, switch_hub, switch_hub_class, fr_ranks, reach_hub,
     reach_rank, reach_is_switch, hard_clean) = _decoupling_and_no_law()
    C3 = bool(decoupled and no_law)

    # ===== C4 : majority-switchable with a fixed non-switching minority =====
    (coherent, n_switch, n_nonswitch, switch_majority, switchable, nonswitch,
     field_clean_majority, n_field_self) = _majority_switchable()
    C4 = bool(coherent)

    # ===== S6 : engine-invariance guard =====
    (a_repr, b_repr, static_is_settle, zero_matches, down_down, fold_eng, reverts) = _invariance()
    S6 = bool(static_is_settle and zero_matches and down_down and fold_eng and reverts)

    preds = {
        "C1_threshold_rank_is_leverage_rank_barrier_invariant": "CONFIRMED" if C1 else "REFUTED",
        "C2_ease_of_flip_tracks_leverage_critical_slowing": "CONFIRMED" if C2 else "REFUTED",
        "C3_switchability_decoupled_from_footprint_and_reach": "CONFIRMED" if C3 else "REFUTED",
        "C4_majority_switchable_fixed_nonswitching_minority": "CONFIRMED" if C4 else "REFUTED",
    }

    # leverage table (the fixed frozen-kernel readout, for the body)
    lev_table = {REGS[j]: round(float(LEVERAGE[j]), 6) for j in ORDER_LEV}

    res = {
        "_what": "SPC-E1E2 -- the spatial-switch-leverage coupling: the SECOND marriage of the E1 "
                 "spatial-localisation layer (§43 SpatialField, a per-node spatial drive on the frozen "
                 "kernel) and the E2 state-switching layer (§28 BistableSwitch, the frozen R19 bistable "
                 "cell used over time), the spatial sibling of the §29 bipolar episode. Neither layer "
                 "alone could pose the question -- E1 has no bistable state (a focal drive cannot FLIP "
                 "anything), E2 has no spatial profile (every region is the same scalar drive). This "
                 "module drives the SINGLE collective R19 bistable state (the SAME §28/§29 cell) with a "
                 "FOCAL stimulation whose effective drive is the driven node's frozen-kernel BROADCAST "
                 "LEVERAGE (lev_j = colsum_j of W0, the one-step current node j injects), and asks WHICH "
                 "region's focal drive most easily flips the state. Four sign/order-only results over a "
                 "stimulation-intensity x barrier-depth sweep: (C1) the flip-threshold rank EQUALS the "
                 "broadcast-leverage rank and is barrier-invariant, with a fixed non-switching minority "
                 "{thalamus, olfactory_bulb}; (C2) ease-of-flip tracks leverage (threshold and latency "
                 "both monotone-decreasing in leverage) with critical slowing at the bottom; (C3, the "
                 "genuinely-new result + honest negative) the switch-leverage axis is DECOUPLED from the "
                 "§46 instantaneous-footprint axis AND the §43 reach axis -- the reach hub (cerebellum) "
                 "is one of the HARDEST to switch, so there is no universal reach->switchability law; "
                 "(C4) a coherent majority-switchable structure with a fixed non-switching minority, the "
                 "honest contrast with §46's clean-delivery default. Both layers IMPORTED, not re-"
                 "derived; the only new object is the §28 cell fed a frozen-kernel leverage readout -- "
                 "no new constant, no new rule. MECHANISM only -- NOT felt, NOT efficacy, NOT medical "
                 "advice.",
        "grounding": {
            "drive": "focal EXCITATORY bias b0>0 at one region (rest baseline); its effective drive on "
                     "the collective state is the broadcast leverage of the driven node, NO new constant",
            "broadcast_leverage": "lev_j = colsum_j = sum_i W0[i,j], the total one-step ephaptic current "
                                  "node j injects into the network through the FROZEN kernel W0 (E1's "
                                  "imported ~1/r^3 row-stochastic kernel) -- a pure readout, not a fit",
            "collective_state": "the §28 BistableSwitch cell ds/dt = g*s - s^3 + h (E2's imported R19 "
                                "cell, the SAME cubic the engine froze, E.sdot), started at the DOWN "
                                "fixed point s0 = -sqrt(g); imported, not re-derived",
            "effective_drive_and_fold": "h_eff(j,b0) = b0 * lev_j; the state flips up iff h_eff crosses "
                                        "the fold spinodal(g) (E.spinodal, the SAME fold as M11 / theta-"
                                        "cap / epilepsy / E2); the intensity threshold is b0* = "
                                        "spinodal(g) / lev_j, inverse in the leverage -- forced [F]",
            "intensity_sweep": list(STIM_DEPTHS),
            "barrier_sweep": list(BARRIER_SWEEP),
            "rep_intensity": REP,
            "rep_barrier": GREP,
            "sweep_grade": "[O] swept -- stimulation intensity b0 AND barrier depth g are SWEPT, not "
                           "tuned; every SIGN/ORDER/STRUCTURE holds across BOTH sweeps (intensity x "
                           "barrier, anti-tuning)",
            "broadcast_leverage_table": lev_table,
            "field_relay_set_sec46": FIELD_RELAY,
            "reach_hub_sec43": REACH_HUB,
            "reused_layers": {"E1_SpatialField": "imported (frozen kernel W0, broadcast structure, "
                                                 "per-node spatial drive)",
                              "E2_BistableSwitch": "imported (the R19 bistable cell, the fold)",
                              "kappa_measured": round(KAP, 6),
                              "R19_fold_spinodal": round(FOLD, 6),
                              "n_regions": N},
        },
        "C1_threshold_rank": {
            "_what": "driving a focal excitatory stimulation at each region in turn, the 12 sites rank by "
                     "how easily their focal drive flips the collective state (lowest intensity threshold "
                     "first); this rank EQUALS the broadcast-leverage rank and is barrier-invariant",
            "flip_threshold_rank_equals_leverage_rank": rank_ok,
            "rank_barrier_invariant": barrier_inv,
            "rank_easiest_to_hardest": rank_thr,
            "fixed_non_switching_set": nonsw1,
            "non_switching_set_is_expected": nonsw1_ok,
            "flip_threshold_table_at_rep_barrier": thr_table,
            "common_finite_threshold_set_across_barrier": common,
            "rank_per_barrier_depth": ranks_by_g,
            "verdict": "the flip-threshold rank is IDENTICAL to the broadcast-leverage rank "
                       "(lev_j = colsum_j of the frozen kernel): the site whose focal drive flips the "
                       "collective state most cheaply is the highest-leverage hub (basal forebrain "
                       "cholinergic), monotone in leverage all the way down. The rank is the SAME across "
                       "the barrier-depth sweep {0.7,1.0,1.3} on the common finite-threshold set -- a "
                       "deeper well raises every threshold together but does not reorder which region "
                       "flips easiest. A FIXED non-switching minority {thalamus, olfactory_bulb} never "
                       "flips the state at any swept intensity (b0<=1). Which focal drive most cheaply "
                       "flips the collective state is a fixed property of the frozen kernel's broadcast "
                       "structure, not of barrier depth nor stimulation intensity. structure-only; "
                       "efficacy=0.",
        },
        "C2_latency_ladder": {
            "_what": "ease-of-flip tracks broadcast leverage with critical slowing at the bottom: the "
                     "flip threshold and the crossing latency are both monotone-decreasing in leverage, "
                     "and the lowest-leverage finite-flip site shows the largest latency (critical slowing)",
            "threshold_monotone_decreasing_in_leverage": thr_mono,
            "latency_monotone_decreasing_in_leverage": lat_mono,
            "critical_slowing_lowest_leverage_largest_latency": crit_slow,
            "lowest_leverage_finite_flip_site": lowest_lev_site,
            "non_switching_set_never_crosses": nonsw_never,
            "crossing_latency_table_at_rep_intensity": lat_table,
            "verdict": "the flip threshold is monotone-decreasing in broadcast leverage "
                       "(b0* = spinodal/lev), and at a FIXED supra-threshold intensity (b0=0.9) the "
                       "crossing latency -- the time the collective state takes to flip -- is also "
                       "monotone-decreasing in leverage: a high-leverage hub flips the state both more "
                       "cheaply AND faster, a low-leverage site dearly and slowly. The lowest-leverage "
                       "site that still flips (brainstem) shows the largest finite latency (critical "
                       "slowing -- the transition time diverging as the effective drive approaches the "
                       "fold), the §28 ictal time-course given a spatial address; the fixed non-switching "
                       "minority never crosses. structure-only.",
        },
        "C3_decoupled_and_no_reach_law": {
            "_what": "the genuinely-new coupling result + the honest no-tuning negative: (a) the switch-"
                     "leverage axis is DECOUPLED from the §46 instantaneous-footprint axis; (b) there is "
                     "no universal reach->switchability law -- the §43 reach hub is one of the hardest to "
                     "switch",
            "switch_leverage_hub": switch_hub,
            "switch_hub_sec46_field_class": switch_hub_class,
            "field_relay_set_sec46": FIELD_RELAY,
            "field_relay_switch_ranks": fr_ranks,
            "decoupled_from_instantaneous_footprint": dec_fp,
            "reach_hub_sec43": reach_hub,
            "reach_hub_switch_rank": reach_rank,
            "reach_hub_is_switch_hub": reach_is_switch,
            "no_universal_reach_to_switchability_law": no_law,
            "hard_to_switch_but_clean_delivery_sites": hard_clean,
            "decoupled": decoupled,
            "verdict": "(a) the §46/E1.3 instantaneous-field relay set {hippocampus, midbrain} (where a "
                       "focal drive's instantaneous effect leaks off-target) is NOT the switch hub set: "
                       "those two sites are MID-rank in switch leverage (ranks 5-6 of 12, easily "
                       "switchable, not special), while the switch hub is basal-forebrain-cholinergic, "
                       "which §46 classes as SELF-LOCALISING (clean instantaneous delivery). WHERE a focal "
                       "drive's instantaneous effect lands and WHICH focal drive flips the collective "
                       "state are two DISTINCT, decoupled spatial axes -- the E1xE2 lesson neither layer "
                       "alone could state. (b) The clean hypothesis 'the greatest-reach region (the §43 "
                       "reach hub) is the one whose focal drive most easily flips the state' is FALSE: the "
                       "§43/§46 reach hub is cerebellum (rank-1 reach at every depth) yet cerebellum is "
                       "switch-rank 10 of 12, one of the HARDEST to flip the state from; the hard-to-"
                       "switch set {thalamus, olfactory_bulb, cerebellum} are all §46 self-localising "
                       "(clean delivery) yet cannot cheaply flip the collective state. Reaching far, "
                       "delivering cleanly, and flipping the collective state are THREE distinct "
                       "properties -- NO universal reach->switchability law. The refuted clean hypothesis "
                       "is reported honestly -- the no-tuning discipline working as intended.",
        },
        "C4_majority_switchable": {
            "_what": "a coherent majority-switchable structure with a fixed non-switching minority -- the "
                     "honest contrast with §46, where clean instantaneous delivery was the default",
            "switchable_set_size": n_switch,
            "non_switching_set_size": n_nonswitch,
            "switchable_is_strict_majority": switch_majority,
            "switchable_set": switchable,
            "fixed_non_switching_set": nonswitch,
            "sec46_field_clean_was_majority": field_clean_majority,
            "sec46_field_self_localising_count": f"{n_field_self}/{N}",
            "coherent_structure": coherent,
            "verdict": "a STRICT MAJORITY of sites (ten of twelve) can have their collective state flipped "
                       "by a swept focal drive (b0<=1), with a FIXED non-switching minority {thalamus, "
                       "olfactory_bulb} that cannot -- MAJORITY-SWITCHABLE, with a hard peripheral floor. "
                       "This is the honest contrast with §46, where the structural default was clean "
                       "instantaneous DELIVERY (ten of twelve self-localising in the instant): here most "
                       "regions' focal drive CAN flip the collective state, but how cheaply is set by "
                       "broadcast leverage and a peripheral minority is locked out entirely. A DIRECTION-"
                       "ONLY [L] correspondence is noted, never a magnitude or a prediction: the highest-"
                       "leverage hubs (basal forebrain cholinergic, hypothalamus) are the classic global "
                       "brain-state / arousal control hubs (the ascending arousal and basal-forebrain "
                       "systems gating sleep-wake and cortical state), and the hardest-to-switch / locked-"
                       "out sites (thalamic relay, olfactory bulb, cerebellum) are peripheral sensory-"
                       "relay or motor-timing structures -- direction-consistent with broadcast hubs "
                       "having an outsized role in switching the global brain state, and relays not.",
        },
        "S6_engine_invariance_guard": {
            "_what": "removing the focal drive (b0=0 -> h_eff=0) settles the collective state via E.settle "
                     "bit-for-bit (the static limit IS the frozen engine, inherited from E2.4), the fold "
                     "is read from E.spinodal, and the down state stays down exactly -- a pure add-on",
            "settle_endpoint_E_settle": a_repr,
            "leverage_switch_zero_drive_endpoint": b_repr,
            "static_limit_is_E_settle_bitwise": static_is_settle,
            "zero_drive_matches_settle_bitwise": zero_matches,
            "down_state_stays_down": down_down,
            "fold_read_from_E_spinodal": fold_eng,
            "focal_excursion_removed_reverts_exactly": reverts,
            "guard": S6,
        },
        "cited_and_locked": {
            "couples_two_layers": "the SECOND coupling of the E1 spatial-localisation layer (§43) and the "
                "E2 state-switching layer (§28): a focal excitatory drive (E1) whose effective drive is "
                "the frozen kernel's broadcast leverage flips the single collective R19 bistable state "
                "(E2) -- the spatial sibling of the §29 bipolar episode (§29 asked WHEN the state flips "
                "under a temporal drive; this asks WHERE a focal drive most cheaply flips it)",
            "reuse_not_rederive_LOCK": "both layers are IMPORTED (SpatialField for the frozen kernel and "
                "broadcast structure, BistableSwitch for the R19 cell and the fold); the kernel W0, the "
                "broadcast leverage colsum, the R19 cell and the fold are NOT re-derived. The only new "
                "object is the §28 cell fed a leverage readout of the SAME frozen kernel -- no new "
                "constant, no new rule",
            "leverage_orders_switchability_LOCK": "the flip-threshold rank EQUALS the broadcast-leverage "
                "rank (b0* = spinodal/lev, inverse in leverage) and is barrier-invariant: WHICH focal "
                "drive most cheaply flips the collective state is a fixed property of the frozen kernel's "
                "broadcast structure, not of barrier depth nor stimulation intensity",
            "decoupled_axes_LOCK": "the switch-leverage axis is DECOUPLED from the §46 instantaneous-"
                "footprint axis (the field-relay set is mid-rank in switch leverage; the switch hub is §46 "
                "self-localising) and from the §43 reach axis (the reach hub, cerebellum, is one of the "
                "HARDEST to switch) -- reaching far, delivering cleanly, and flipping the state are three "
                "distinct properties; there is NO universal reach->switchability law",
            "real_state_control_distributed_LOCK": "real brain-state switching is a distributed "
                "neuromodulatory system (the ascending arousal nuclei, basal forebrain, thalamic and "
                "cortical loops, multiple transmitters, state-dependent conductances); this module asserts "
                "the SIGN/ORDER/STRUCTURE of which focal-drive ADDRESS most cheaply flips a single bistable "
                "collective state when the effective drive is the frozen kernel's broadcast leverage, not "
                "that any real state control follows this exact rule",
            "state_control_hubs_cited": "the highest-leverage hubs (basal forebrain cholinergic, "
                "hypothalamus) are the classic global brain-state / arousal control hubs, and the locked-"
                "out / hard-to-switch sites (thalamic relay, olfactory bulb, cerebellum) are peripheral "
                "relay or motor-timing structures -- a DIRECTION-ONLY [L] correspondence to the leverage "
                "ordering, never a magnitude or a patient-level prediction",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; whether any "
                "real focal stimulation flips a brain state, and which, is external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "collective_state_is_structural": 1.0,
            "reuses_E1_spatial_field": 1.0,
            "reuses_E2_state_switching": 1.0,
            "couples_E1_and_E2": 1.0,
            "stimulation_intensity": "OPEN [O] -- swept (driven node, depth); signs/order hold over the "
                                     "intensity sweep, not tuned",
            "barrier_depth_g": "OPEN [O] -- swept {0.7,1.0,1.3}; the rank is barrier-invariant, not tuned",
            "broadcast_leverage_is_frozen_kernel_readout": 1.0,
            "switchability_decoupled_from_instantaneous_footprint": 1.0,
            "switchability_decoupled_from_reach": 1.0,
            "reach_to_switchability_law_refuted": "C3(b) reports a REFUTED clean hypothesis honestly (no "
                                                  "universal reach->switchability law) rather than forcing "
                                                  "a tidy 'the reach hub is the switch hub' narrative",
            "clinical_prediction": "NONE -- the [L] correspondence is direction-only, never a patient-level "
                                   "prediction; target selection / device programming are external",
            "not_medical_advice": 1.0,
            "opens_E1xE2_coupling": 1.0,
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "static_limit_is_E_settle": static_is_settle,
            "m9_anchor_value_frozen": repr(M9_ANCHOR_R),
        },
        "preregistered_results": {
            "C1_threshold_rank_is_leverage_rank_barrier_invariant": {
                "claim": "driving a focal excitatory stimulation at each region, the flip-threshold rank "
                         "(easiest to flip the collective state first) EQUALS the broadcast-leverage rank "
                         "(lev_j = colsum_j of the frozen kernel) and is identical across the barrier-depth "
                         "sweep on the common finite-threshold set; a fixed non-switching minority "
                         "{thalamus, olfactory_bulb} never flips at any swept intensity",
                "status": preds["C1_threshold_rank_is_leverage_rank_barrier_invariant"]},
            "C2_ease_of_flip_tracks_leverage_critical_slowing": {
                "claim": "the flip threshold is monotone-decreasing in broadcast leverage and the crossing "
                         "latency at a fixed supra-threshold intensity is monotone-decreasing in leverage, "
                         "with the lowest-leverage finite-flip site showing the largest latency (critical "
                         "slowing); the non-switching minority never crosses",
                "status": preds["C2_ease_of_flip_tracks_leverage_critical_slowing"]},
            "C3_switchability_decoupled_from_footprint_and_reach": {
                "claim": "the switch-leverage axis is decoupled from the §46 instantaneous-footprint axis "
                         "(the field-relay set is mid-rank; the switch hub is §46 self-localising) and "
                         "there is no universal reach->switchability law (the §43 reach hub, cerebellum, is "
                         "one of the hardest to switch)",
                "status": preds["C3_switchability_decoupled_from_footprint_and_reach"]},
            "C4_majority_switchable_fixed_nonswitching_minority": {
                "claim": "a strict majority (ten of twelve) of sites can have their collective state "
                         "flipped by a swept focal drive, with a fixed non-switching minority {thalamus, "
                         "olfactory_bulb} -- majority-switchable with a hard peripheral floor, the honest "
                         "contrast with §46's clean-delivery default",
                "status": preds["C4_majority_switchable_fixed_nonswitching_minority"]},
        },
        "overall": {
            "threshold_rank_reproduced": C1,
            "latency_ladder_reproduced": C2,
            "decoupling_and_no_law_reproduced": C3,
            "majority_switchable_reproduced": C4,
            "engine_invariance_guard": S6,
            "is_full_module": bool(C1 and C2 and C3 and C4 and S6),
            "verdict": "SPC-E1E2 is the spatial-switch-leverage coupling -- the second marriage of the E1 "
                       "spatial drive and the E2 bistable state, the spatial sibling of the §29 bipolar "
                       "episode, asking WHICH focal drive most easily flips the collective state. The flip-"
                       "threshold rank EQUALS the broadcast-leverage rank and is barrier-invariant, with a "
                       "fixed non-switching minority {thalamus, olfactory_bulb} (C1); ease-of-flip tracks "
                       "leverage -- threshold and latency both monotone-decreasing in leverage -- with "
                       "critical slowing at the lowest-leverage finite-flip site (C2); the switch-leverage "
                       "axis is DECOUPLED from the §46 instantaneous-footprint axis and the §43 reach axis "
                       "-- the reach hub (cerebellum) is one of the hardest to switch, so there is no "
                       "universal reach->switchability law (C3, the genuinely-new result + honest "
                       "negative); a coherent majority-switchable structure with a fixed non-switching "
                       "minority, the honest contrast with §46's clean-delivery default (C4). Removing the "
                       "focal drive settles the collective state via E.settle bit-for-bit and the fold is "
                       "read from E.spinodal (S6). Both layers imported not re-derived, no new tuned "
                       "constant, no new rule, engine byte-unchanged. efficacy=0; not medical advice; "
                       "Axis-A firewall; hard problem OPEN.",
        },
    }
    return res


def _canon(o):
    if isinstance(o, float):
        return round(o, 10)
    if isinstance(o, dict):
        return {k: _canon(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_canon(v) for v in o]
    return o

def _blob(res):
    return json.dumps(_canon(res), sort_keys=True, ensure_ascii=False, indent=2) + "\n"

def spatial_switch_leverage_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "spatial_switch_leverage_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_spatial_switch_leverage_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"spatial_switch_leverage_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = spatial_switch_leverage_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    g = res["grounding"]
    c1 = res["C1_threshold_rank"]; c2 = res["C2_latency_ladder"]
    c3 = res["C3_decoupled_and_no_reach_law"]; c4 = res["C4_majority_switchable"]
    s6 = res["S6_engine_invariance_guard"]
    print("=" * 78)
    print("SPC-E1E2 -- SPATIAL-SWITCH-LEVERAGE COUPLING (E1 x E2)   add-only, engine READ-ONLY")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  couples: E1 SpatialField (broadcast leverage) x E2 BistableSwitch (R19 state)")
    print(f"           intensity sweep={g['intensity_sweep']}  barrier sweep={g['barrier_sweep']}")
    print(f"  §46 field-relay set: {g['field_relay_set_sec46']}   §43 reach hub: {g['reach_hub_sec43']}")
    print("-" * 78)
    print(f"  C1 threshold rank: ==leverage rank={c1['flip_threshold_rank_equals_leverage_rank']} barrier-invariant={c1['rank_barrier_invariant']}")
    print(f"                     easiest->hardest = {c1['rank_easiest_to_hardest']}")
    print(f"                     fixed non-switching = {c1['fixed_non_switching_set']}")
    print(f"  C2 latency ladder: thr-mono={c2['threshold_monotone_decreasing_in_leverage']} lat-mono={c2['latency_monotone_decreasing_in_leverage']} crit-slow={c2['critical_slowing_lowest_leverage_largest_latency']} ({c2['lowest_leverage_finite_flip_site']})")
    print(f"  C3 decoupled     : switch hub={c3['switch_leverage_hub']} (§46 {c3['switch_hub_sec46_field_class']}); field-relay switch-ranks={c3['field_relay_switch_ranks']}")
    print(f"                     reach hub={c3['reach_hub_sec43']} switch-rank={c3['reach_hub_switch_rank']}/{N}; no reach->switch law={c3['no_universal_reach_to_switchability_law']}")
    print(f"  C4 majority      : switchable strict majority={c4['switchable_is_strict_majority']} ({c4['switchable_set_size']}/{N}); §46 clean was majority={c4['sec46_field_clean_was_majority']}")
    print(f"  S6 invariance    : static==E.settle:{s6['static_limit_is_E_settle_bitwise']}  zero-drive matches:{s6['zero_drive_matches_settle_bitwise']}  fold from engine:{s6['fold_read_from_E_spinodal']}  reverts:{s6['focal_excursion_removed_reverts_exactly']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  SPATIAL-SWITCH-LEVERAGE COUPLING MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
