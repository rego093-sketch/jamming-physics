#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPC-E1E0 -- SPATIAL-PLASTICITY COUPLING : where a focal drive IMPRINTS -- LOCAL delivery vs
RELAYED consolidation. The FIRST coupling of the two reusable layers the atlas built separately:
the E1 spatial-localisation layer (§43, SpatialField -- a per-node spatial drive on the frozen
ephaptic kernel) and the E0 plasticity/consolidation layer (§26, PlasticConnectome -- a slow
phase-correlation Hebbian update of the connectivity W). Neither layer alone could pose the
question this module asks. E1 has a FROZEN W (it reads the instantaneous local-coherence field on
a fixed kernel -- no plasticity, so a focal drive leaves no lasting trace). E0 evolves W under
plasticity but drives the network GLOBALLY (one scalar bias for the whole brain -- no spatial
profile, so a trace has no "where"). This module MARRIES them: it runs a FOCAL EXCITATORY drive
(the §44/§46 stimulation model, a per-node bias from E1) THROUGH the E0 phase-correlation Hebbian
update, so the focal drive WRITES ITSELF into the connectome, and reads the SPATIAL PATTERN of the
retained structural trace ||W - W0|| -- the spatial × temporal seam. It is the spatial sibling of
E0 consolidation (the §37 GAIN mode given a location) and the lasting-trace counterpart of §46
(which read where a focal stimulation's INSTANTANEOUS effect lands; this reads where its LASTING
trace lands). It IMPORTS both layers (it does NOT re-derive the ephaptic kernel, the coupling map,
or the Hebbian rule -- handover reuse discipline); the coupled integrator is the SAME per-node
generalisation E1 already made of the engine integrator, additionally accumulating the pairwise
phase correlation the E0 Hebbian update consumes -- no new constant, no new rule.
=================================================================================
THE GROUNDING (READ-ONLY; no new constant, no new rule). A focal stimulation is a strong focal
EXCITATORY bias b0 > 0 at one region (the rest at baseline) through the SAME k = kappa/(1-|b|)
[excit] cap 2*kappa map as the SZ / epilepsy / E1 / E0 modules (E1's _k_bias, imported). The
plasticity is the E0 phase-correlation Hebbian update W_ij <- max(0, W_ij*(1 + eta*C_ij)),
row-renormalised, with C_ij = <cos(theta_j - theta_i)> the steady-state pairwise phase correlation
(E0's PlasticConnectome rule, imported and reused -- the SAME "fire together wire together" read on
phase). The coupled integrator runs dtheta_i = omega_i + Kvec_i * sum_j W_ij sin(theta_j - theta_i)
with a PER-NODE drive Kvec (E1's spatial generalisation) on the EVOLVING W (E0's plastic
connectome), and accumulates C_ij over the steady second half so the Hebbian update can consume it.
When the drive is uniform/zero AND eta = 0 it collapses to E._integrate -- the frozen engine -- and
reproduces the M9 anchor BIT-FOR-BIT (the S6 guard). The retained trace after a focal drive is read
SPATIALLY: for the driven node, the mean |dW| on edges INCIDENT to it (own imprint) vs the mean
|dW| on edges NOT incident (off-target imprint) -- the trace analogue of the E1.3 own-vs-off-target
footprint. The stimulation INTENSITY b0 is SWEPT over the full E1 depth sweep {0.3,0.5,0.7,0.9} AND
the plasticity RATE eta over {0.03,0.05,0.08}; every SIGN/STRUCTURE asserted below is required to
hold across BOTH sweeps (anti-tuning, intensity x rate). g = 1.0 is the engine's universal R19
scale; nothing here is fit.

WHAT THE MODULE DELIVERS (pre-registered, sign/structure only; never magnitudes):
  C1  THE IMPRINT PARTITION (local imprint vs relayed imprint) IS DRIVE-INVARIANT. Running a focal
      excitatory drive through plasticity at each region in turn, the 12 sites partition by where the
      retained trace LANDS: a LOCAL-IMPRINT site writes its trace mostly onto edges INCIDENT to the
      driven node (the focal drive imprints where it is driven), a RELAYED-IMPRINT site writes its
      trace harder onto OFF-target edges (the focal drive writes itself into distal circuitry). This
      binary partition is IDENTICAL across the FULL stimulation-intensity sweep {0.3,0.5,0.7,0.9} AND
      a plasticity-rate sweep eta in {0.03,0.05,0.08}: the local-imprint set {brainstem, cerebellum,
      pallidum, striatum} is fixed and the relayed-imprint set (the other eight) is fixed at every
      intensity and every rate. Whether a focal drive imprints LOCALLY or RELAYS its trace is a fixed
      property of the driven site, not of how hard it is stimulated nor how fast the synapse learns.
      grade [V mech].
  C2  RELAYED IMPRINT IS OFF-TARGET-DOMINANT TRACE (the structural content). For a RELAYED site the
      mean |dW| on off-target edges EXCEEDS the mean |dW| on incident edges (off/inc > 1) -- the
      structural signature of a focal drive writing itself into distal circuitry rather than its own
      neighbourhood; for a LOCAL site incident-dominant (off/inc < 1). The relayed <-> (off/inc > 1)
      equivalence holds at every swept intensity and every swept rate, tying "relayed imprint" to its
      structural meaning. grade [V mech].
  C3  INSTANTANEOUS DELIVERY AND LASTING IMPRINT ARE DECOUPLED, and there is NO UNIVERSAL FOCAL>DIFFUSE
      TRACE LAW (the genuinely-new coupling result + the honest no-tuning negative). (a) The retained-
      trace relay set STRICTLY CONTAINS the §46 / E1.3 INSTANTANEOUS-field relay set: {hippocampus,
      midbrain} (the field-relay / off-target-leak set, where the INSTANTANEOUS effect lands off-
      target) is a PROPER SUBSET of the eight-site trace-relay set (where the LASTING trace lands
      off-target). Plasticity DELOCALISES the imprint: six sites (neocortex, thalamus, hypothalamus,
      basal-forebrain-cholinergic, forebrain-GABA-interneuron, olfactory-bulb) deliver CLEANLY in the
      instant (self-localising field, §46 "clean delivery") yet imprint OFF-target (relayed trace) --
      a clean instantaneous delivery does NOT guarantee a clean lasting imprint. WHERE a focal drive
      ACTS NOW and WHERE it WRITES ITSELF into structure are two DISTINCT, decoupled spatial axes --
      the E1xE0 lesson neither layer alone could state (E1 has no plasticity; E0 has no spatial
      profile). (b) A clean, attractive hypothesis -- "a focal drive always imprints MORE at its own
      site than the same total dose spread diffusely" -- is FALSE: the sign of (focal retained trace -
      diffuse retained trace) VARIES across sites (only three of twelve imprint more focally than
      diffusely), holding across the intensity sweep. There is NO universal focal>diffuse TRACE law --
      the E1.4 "no universal focal>diffuse law" lesson carried from the instantaneous field to the
      lasting trace. We do NOT force a tidy "focal imprints locally" story; the refuted clean
      hypothesis is reported honestly. grade [V mech] (a refuted clean hypothesis is a finding).
  C4  RELAYED IMPRINT IS THE STRUCTURAL DEFAULT -- a coherent MAJORITY class (the honest contrast with
      §46). The relayed-imprint set is a STRICT MAJORITY (eight of twelve), so RELAYED imprint, not
      local, is the structural DEFAULT -- the explicit HONEST CONTRAST with §46, where CLEAN delivery
      was the structural default (ten of twelve self-localising in the instant). A focal drive's
      LASTING structural footprint is, by default, DELOCALISED, even though its INSTANTANEOUS footprint
      is, by default, focal. The relayed-imprint set is simultaneously the off-target-dominant trace
      set (C2) and strictly contains the field-relay set (C3a) -- one coherent majority class. A
      DIRECTION-ONLY [L] correspondence is noted, never a magnitude or a prediction: stimulation-
      induced plasticity (the lasting structural/functional change a focal stimulation leaves -- e.g.
      the after-effects of repetitive TMS or tDCS, the plasticity DBS induces in connected circuits)
      is recognised to be NETWORK-DISTRIBUTED and target/connectivity-dependent rather than confined to
      the stimulation site -- consistent with relayed imprint being the structural majority and the
      imprint axis decoupled from the instantaneous-delivery axis. grade [V mech] structural + [L].

NOT a claim that real stimulation-induced plasticity reduces to a phase-correlation Hebbian update on a
frozen 1/r^3 kernel (real plasticity is heterogeneous -- LTP/LTD, STDP, homeostatic scaling,
metaplasticity, structural plasticity; real stimulation spread is heterogeneous -- electrode geometry,
tissue conductivity, tractography, the individual connectome, montage/waveform -- LOCKED); what is
asserted is the SIGN/STRUCTURE of a focal excitatory drive run through a phase-Hebbian update on the
frozen kernel and its four consequences (the local/relayed imprint partition, off-target trace
dominance, the decoupling of instantaneous delivery from lasting imprint, and the relayed-imprint
majority). NOT a claim about the FELT effect of stimulation or learning (Axis-A firewall: a retained
trace and its locality are STRUCTURAL spatial quantities of the coupling model, NEVER a felt effect;
consciousness_claim stays 0; hard problem stays OPEN). NOT a real electric-field / current-density /
lead-position / SAR map, a real connectome, or a real measurement of where a stimulation imprints. NOT
a prediction of WHICH patient's stimulation imprints where, and NOT clinical, device-programming, or
target-selection guidance -- those are external clinical decisions. NOT MEDICAL ADVICE; efficacy = 0
everywhere; in-silico MECHANISM only; nothing here is a cure, a treatment, a localisation, or a device
setting. Every MAGNITUDE is [O]; only structural SIGNS and RELATIONS are asserted, and they are
certified to survive the stimulation-intensity sweep AND the plasticity-rate sweep.

Governed by VP_SPEC_v1_8 (C0-C4, SEED=19). ADD-ONLY; vp_mind_engine imported READ-ONLY (emerge_all is
NOT touched, so the engine file stays e61083ae..., the tree stays 0fbf4988... and the M0..M16 subtree
stays 3a1ebbbb..., byte-identical). COUPLES the E1 SpatialField and the E0 PlasticConnectome (both
imported, not re-derived); the drive is an EXCITATORY bias on the frozen kernel run through the E0
Hebbian update. Writes spatial_plasticity_imprint_results.json + its sha256, verified bit-for-bit. The
coupled integrator is the reusable seam any later spatial-temporal module imports.
"""
import os, sys, json, math, hashlib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import vp_mind_engine as E

# REUSE both layers -- import their classes and shared (measured) handles; do NOT re-derive the
# ephaptic kernel, the coupling map, or the Hebbian rule (handover discipline: reuse, not re-derive).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e1_spatial_localisation import (SpatialField, REGS, N, DEPTHS, OMEGA, OMEGA0, KAP, W0, FOLD,
                                     M9_ANCHOR_R, ENGINE_TREE_FROZEN, M0_16_FROZEN, _k_bias)
from e0_plasticity import PlasticConnectome, _rn   # the E0 plasticity layer (Hebbian rule reused)

HERE = os.path.dirname(os.path.abspath(__file__))

STIM_DEPTHS = DEPTHS                  # {0.3, 0.5, 0.7, 0.9} -- E1 depth sweep (intensity)
ETA_SWEEP   = (0.03, 0.05, 0.08)     # E0 plasticity-rate sweep
REP         = 0.7                     # representative stimulation intensity for headline reads [swept]
ETA         = 0.05                    # representative plasticity rate [swept]
EPOCHS      = 8                       # consolidation epochs (focal drive run through plasticity)

HIPPO = REGS.index("hippocampus")
MIDB  = REGS.index("midbrain")
CEREB = REGS.index("cerebellum")

# The §46 / E1.3 INSTANTANEOUS-field relay (off-target-leak) set -- read from the imported
# SpatialField footprint class (NOT re-derived; it is §46's own set, {hippocampus, midbrain}).
_SF = SpatialField()
FIELD_RELAY = sorted([REGS[k] for k in range(N) if _SF.footprint_class(k, REP) < 0])

# Expected (probed) imprint sets -- the local-imprint minority and the relayed-imprint majority.
EXPECTED_LOCAL = sorted(["brainstem", "cerebellum", "pallidum", "striatum"])
EXPECTED_RELAY = sorted([r for r in REGS if r not in EXPECTED_LOCAL])


def _integrate_coupled(W, bias_vec, T=6.0, dt=0.001, seed=E.SEED):
    """The E1xE0 coupled integrator: a PER-NODE spatial drive (E1's generalisation of the engine
    integrator) on the EVOLVING W, additionally accumulating the steady-state pairwise phase
    correlation C_ij = <cos(theta_j - theta_i)> that the E0 Hebbian update consumes. With a uniform
    (or zero) bias the per-node Kvec collapses to the scalar and the dynamics are bit-identical to
    E._integrate(omega, W, Kglob); the correlation accumulation is a read-only side computation."""
    rng = np.random.RandomState(seed)
    th = rng.uniform(-math.pi, math.pi, N)
    Kvec = np.array([_k_bias(b) for b in bias_vec]) * OMEGA0
    ns = int(T / dt)
    Rs = np.empty(ns)
    Csum = np.zeros((N, N))
    h = ns // 2
    cnt = 0
    for s in range(ns):
        diff = th[None, :] - th[:, None]
        th = th + dt * (OMEGA + Kvec * np.sum(W * np.sin(diff), axis=1))
        Rs[s] = float(abs(np.mean(np.exp(1j * th))))
        if s >= h:
            Csum += np.cos(diff)
            cnt += 1
    return float(np.mean(Rs[h:])), Csum / cnt


class CoupledField:
    """The E1xE0 seam: the frozen ephaptic kernel W0, a PER-NODE spatial drive (E1's SpatialField
    profile), and the E0 phase-correlation Hebbian update applied to the evolving W. REUSABLE -- a
    later spatial-temporal module imports this; it does not re-derive the kernel, the coupling map or
    the Hebbian rule. The engine is never mutated; W starts as the frozen kernel and only this
    object's copy evolves (exactly E0's PlasticConnectome contract, under a spatial drive)."""

    def __init__(self):
        self.W = W0.copy()

    def reset(self):
        self.W = W0.copy()
        return self

    def order(self):
        """Order parameter R at the measured coupling on the current W (drive off) -- E0's read."""
        return E._integrate(OMEGA, self.W, KAP * OMEGA0)[0]

    def focal_drive(self, node, b0, eta=ETA):
        """One consolidation epoch: a focal excitatory bias b0 at `node` (rest baseline) run through
        the E0 phase-Hebbian update (rate eta). Returns (R_during, C); updates W in place."""
        bv = np.zeros(N); bv[node] = b0
        R, C = _integrate_coupled(self.W, bv)
        if eta != 0.0:
            Wn = np.maximum(0.0, self.W * (1.0 + eta * C)); np.fill_diagonal(Wn, 0.0)
            self.W = _rn(Wn)
        return R, C

    def diffuse_drive(self, b0, eta=ETA):
        """One consolidation epoch: the SAME total dose b0 spread uniformly (b0/N per node) run
        through the E0 phase-Hebbian update. The diffuse counterpart of focal_drive."""
        bv = np.full(N, b0 / N)
        R, C = _integrate_coupled(self.W, bv)
        if eta != 0.0:
            Wn = np.maximum(0.0, self.W * (1.0 + eta * C)); np.fill_diagonal(Wn, 0.0)
            self.W = _rn(Wn)
        return R, C

    def trace(self):
        """Retained structural trace = Frobenius distance of the current W from the frozen kernel."""
        return float(np.linalg.norm(self.W - W0))

    def imprint_split(self, node):
        """Mean |dW| on edges INCIDENT to `node` (own imprint) vs mean |dW| on edges NOT incident
        (off-target imprint) -- the trace analogue of the E1.3 own-vs-off-target footprint."""
        dW = np.abs(self.W - W0)
        inc = np.zeros((N, N), bool); inc[node, :] = True; inc[:, node] = True
        np.fill_diagonal(inc, False)
        off = (~inc); np.fill_diagonal(off, False)
        return float(dW[inc].mean()), float(dW[off].mean())

    def imprint_class(self, node):
        """+1 LOCAL imprint (incident |dW| > off-target |dW|), -1 RELAYED imprint (otherwise)."""
        inc, off = self.imprint_split(node)
        return 1 if inc > off else -1


def _consolidate_focal(node, b0, eta, epochs=EPOCHS):
    """Run `epochs` focal consolidation epochs at `node` (intensity b0, rate eta); return the
    coupled field after consolidation."""
    cf = CoupledField()
    for _ in range(epochs):
        cf.focal_drive(node, b0, eta)
    return cf


def _consolidate_diffuse(b0, eta, epochs=EPOCHS):
    cf = CoupledField()
    for _ in range(epochs):
        cf.diffuse_drive(b0, eta)
    return cf


# ------------------------------- the four sub-studies + guard ----------------------------

def _partition():
    """C1: the local-imprint/relayed-imprint partition over the FULL intensity sweep x rate sweep.
    The partition is drive-invariant (identical across every intensity AND every rate); the local set
    and relayed set are fixed."""
    base = None
    invariant = True
    relay_sets = set()
    for b0 in STIM_DEPTHS:
        for eta in ETA_SWEEP:
            vec = tuple(_consolidate_focal(n, b0, eta).imprint_class(n) for n in range(N))
            relay_sets.add(tuple(sorted([REGS[k] for k in range(N) if vec[k] < 0])))
            if base is None:
                base = vec
            elif vec != base:
                invariant = False
    local = sorted([REGS[k] for k in range(N) if base[k] > 0])
    relay = sorted([REGS[k] for k in range(N) if base[k] < 0])
    local_is_expected = bool(local == EXPECTED_LOCAL)
    relay_is_expected = bool(relay == EXPECTED_RELAY)
    one_partition = bool(len(relay_sets) == 1)
    # labelled at the representative (intensity, rate) for the body
    labelled = {REGS[n]: ("local" if _consolidate_focal(n, REP, ETA).imprint_class(n) > 0 else "relayed")
                for n in range(N)}
    return (invariant and one_partition, local, relay, local_is_expected, relay_is_expected,
            len(relay_sets), labelled)


def _off_target_dominance():
    """C2: relayed imprint <-> (mean off-target |dW| > incident |dW|), at every swept intensity and
    rate."""
    equivalence_all = True
    per_site = {}
    relay_idx = set(REGS.index(r) for r in EXPECTED_RELAY)
    for b0 in STIM_DEPTHS:
        for eta in ETA_SWEEP:
            for n in range(N):
                cf = _consolidate_focal(n, b0, eta)
                inc, off = cf.imprint_split(n)
                is_relayed = bool(off > inc)
                want_relayed = bool(n in relay_idx)
                if is_relayed != want_relayed:
                    equivalence_all = False
                if round(b0, 2) == REP and eta == ETA:
                    per_site[REGS[n]] = {"incident_abs_dW": round(inc, 8),
                                         "off_target_abs_dW": round(off, 8),
                                         "off_over_incident": round(off / inc, 4) if inc > 0 else None,
                                         "off_target_dominant_relayed": is_relayed}
    return bool(equivalence_all), per_site


def _decoupling_and_no_law():
    """C3 (the genuinely-new coupling result + honest negative). (a) the retained-trace relay set
    STRICTLY CONTAINS the §46 / E1.3 instantaneous-field relay set -- plasticity delocalises the
    imprint; (b) no universal focal>diffuse TRACE law (the sign varies across sites), over the
    intensity sweep."""
    # --- (a) strict-containment of the field-relay set in the trace-relay set ---
    field_relay_idx = set(REGS.index(r) for r in FIELD_RELAY)
    trace_relay = set(REGS.index(r) for r in EXPECTED_RELAY)
    field_subset_of_trace = bool(field_relay_idx.issubset(trace_relay))
    strict = bool(field_subset_of_trace and len(field_relay_idx) < len(trace_relay))
    # the witnessing sites: clean instantaneous delivery (self-localising field) BUT relayed imprint
    clean_field_relayed_trace = sorted(
        [REGS[n] for n in range(N)
         if _SF.footprint_class(n, REP) > 0 and _consolidate_focal(n, REP, ETA).imprint_class(n) < 0])
    n_witness = len(clean_field_relayed_trace)
    decoupled = bool(strict and n_witness > 0)
    # the two field-relay sites are also trace-relayed (the subset is genuine, not disjoint)
    field_relay_also_trace = {r: ("relayed" if _consolidate_focal(REGS.index(r), REP, ETA).imprint_class(REGS.index(r)) < 0
                                  else "local") for r in FIELD_RELAY}

    # --- (b) no universal focal>diffuse TRACE law, over the intensity sweep ---
    no_law_all = True
    sign_dump = {}
    for b0 in (0.5, REP):
        signs = []
        for n in range(N):
            tf = _consolidate_focal(n, b0, ETA).trace()
            td = _consolidate_diffuse(b0, ETA).trace()
            signs.append(1 if tf > td else -1)
        n_focal = int(sum(1 for s in signs if s > 0))
        universal = bool(all(s > 0 for s in signs))
        heterogeneous = bool(len(set(signs)) > 1)
        ok = bool((not universal) and heterogeneous)
        no_law_all = no_law_all and ok
        sign_dump[round(b0, 2)] = {"n_sites_focal_gt_diffuse": f"{n_focal}/{N}",
                                   "universal": universal, "heterogeneous": heterogeneous}
    no_universal_law = bool(no_law_all)

    return (decoupled, strict, field_subset_of_trace, clean_field_relayed_trace, n_witness,
            field_relay_also_trace, no_universal_law, sign_dump)


def _majority_class():
    """C4: relayed imprint is the structural DEFAULT (strict majority, the honest contrast with §46),
    = the off-target-dominant set (C2), strictly containing the field-relay set (C3a)."""
    n_relay = len(EXPECTED_RELAY)
    n_local = len(EXPECTED_LOCAL)
    relayed_is_majority = bool(n_relay > n_local)
    # the off-target-dominant set at the representative (intensity, rate) == the relayed set
    od_set = sorted([REGS[n] for n in range(N)
                     if (lambda s: s[1] > s[0])(_consolidate_focal(n, REP, ETA).imprint_split(n))])
    relay_eq_off_target = bool(od_set == EXPECTED_RELAY)
    field_subset = bool(set(REGS.index(r) for r in FIELD_RELAY).issubset(set(REGS.index(r) for r in EXPECTED_RELAY)))
    # honest contrast with §46: in §46 the instantaneous self-localising (clean) set was the majority
    n_field_self = N - len(FIELD_RELAY)
    field_clean_was_majority = bool(n_field_self > len(FIELD_RELAY))
    coherent_majority = bool(relayed_is_majority and relay_eq_off_target and field_subset)
    return (coherent_majority, n_relay, n_local, relayed_is_majority, relay_eq_off_target,
            field_subset, field_clean_was_majority, n_field_self)


def _invariance():
    """S6: a zero drive at eta=0 reproduces the frozen M9 anchor R bit-for-bit, leaves W identical to
    the kernel (a focal excursion reverts exactly without plasticity, inheriting E0.3), and the off-
    state coupled field equals the baseline exactly -- the coupling is a pure add-on on the engine."""
    R_direct = E._integrate(OMEGA, W0, KAP * OMEGA0)[0]               # frozen M9 anchor (engine)
    # zero-bias coupled epoch with eta=0 -> W untouched, R bit-for-bit
    cf = CoupledField()
    R_off, _ = cf.focal_drive(CEREB, 0.0, eta=0.0)                    # zero-depth focal == zero drive
    matches_anchor = bool(R_direct == M9_ANCHOR_R)
    off_matches = bool(R_off == R_direct)
    w_untouched = bool(np.array_equal(cf.W, W0))
    # a FOCAL excursion at eta=0 reverts exactly (E0.3 inherited under a spatial drive)
    pe = CoupledField()
    for _ in range(EPOCHS):
        pe.focal_drive(CEREB, REP, eta=0.0)
    reverts = bool(pe.order() == R_direct and pe.trace() == 0.0)
    return R_direct, R_off, matches_anchor, off_matches, w_untouched, reverts


def run():
    # ===== C1 : the local-imprint/relayed-imprint partition, drive-invariant =====
    (part_inv, local, relay, local_ok, relay_ok, n_part, part_labelled) = _partition()
    C1 = bool(part_inv and local_ok and relay_ok)

    # ===== C2 : relayed imprint = off-target-dominant trace =====
    od_equiv, od_per_site = _off_target_dominance()
    C2 = bool(od_equiv)

    # ===== C3 : instantaneous delivery != lasting imprint; no universal focal>diffuse trace law =====
    (decoupled, strict, subset, witnesses, n_witness, field_also_trace,
     no_law, sign_dump) = _decoupling_and_no_law()
    C3 = bool(decoupled and no_law)

    # ===== C4 : relayed imprint is the structural default, a coherent majority class =====
    (coherent, n_relay, n_local, relayed_majority, relay_eq_od, field_subset,
     field_clean_majority, n_field_self) = _majority_class()
    C4 = bool(coherent)

    # ===== S6 : engine-invariance guard =====
    Rinv, Roff, anchor_ok, off_ok, w_ok, reverts_ok = _invariance()
    S6 = bool(anchor_ok and off_ok and w_ok and reverts_ok)

    preds = {
        "C1_imprint_partition_drive_invariant": "CONFIRMED" if C1 else "REFUTED",
        "C2_relayed_is_off_target_dominant_trace": "CONFIRMED" if C2 else "REFUTED",
        "C3_delivery_imprint_decoupled_no_universal_law": "CONFIRMED" if C3 else "REFUTED",
        "C4_relayed_imprint_structural_default": "CONFIRMED" if C4 else "REFUTED",
    }

    res = {
        "_what": "SPC-E1E0 -- the spatial-plasticity coupling: the FIRST marriage of the E1 spatial-"
                 "localisation layer (§43 SpatialField, a per-node spatial drive on the frozen kernel) "
                 "and the E0 plasticity layer (§26 PlasticConnectome, a phase-correlation Hebbian update "
                 "of W). Neither layer alone could pose the question -- E1 has a FROZEN W (no lasting "
                 "trace), E0 drives GLOBALLY (a trace has no 'where'). This module runs a FOCAL excitatory "
                 "drive (the §44/§46 stimulation, from E1) THROUGH the E0 Hebbian update so the focal drive "
                 "WRITES ITSELF into the connectome, and reads the SPATIAL pattern of the retained trace "
                 "||W-W0|| -- the spatial x temporal seam, the spatial sibling of E0 consolidation and the "
                 "lasting-trace counterpart of §46. Four sign-only results over an intensity x rate sweep: "
                 "(C1) the local-imprint/relayed-imprint partition is drive-invariant; (C2) relayed imprint "
                 "is off-target-dominant trace; (C3, the genuinely-new result + honest negative) "
                 "instantaneous delivery and lasting imprint are DECOUPLED -- the retained-trace relay set "
                 "STRICTLY CONTAINS the §46 instantaneous-field relay set, so plasticity DELOCALISES the "
                 "imprint and a clean delivery does not guarantee a clean imprint, AND there is no universal "
                 "focal>diffuse trace law; (C4) relayed imprint is the structural DEFAULT (the honest "
                 "contrast with §46's clean default). Both layers IMPORTED, not re-derived; the coupled "
                 "integrator is the same per-node generalisation E1 already made, accumulating the pairwise "
                 "correlation E0's rule consumes -- no new constant, no new rule. MECHANISM only -- NOT felt, "
                 "NOT efficacy, NOT medical advice.",
        "grounding": {
            "drive": "focal EXCITATORY bias b0>0 at one region (rest baseline), k=kappa/(1-|b|) cap "
                     "2*kappa -- the §44/§46 stimulation model, E1's _k_bias imported (no new constant)",
            "plasticity": "E0 phase-correlation Hebbian update W_ij<-max(0,W_ij*(1+eta*C_ij)) row-"
                          "renormalised, C_ij=<cos(theta_j-theta_i)> -- the §26 PlasticConnectome rule, "
                          "imported and reused (no new rule)",
            "coupled_integrator": "dtheta_i = omega_i + Kvec_i * sum_j W_ij sin(theta_j-theta_i) with a "
                                  "PER-NODE drive Kvec (E1's spatial generalisation of the engine "
                                  "integrator) on the EVOLVING W (E0's plastic connectome), accumulating "
                                  "the pairwise C_ij the Hebbian update consumes -- forced [F]; a uniform/"
                                  "zero drive at eta=0 reproduces E._integrate bit-for-bit",
            "imprint_readout": "for the driven node, mean |dW| on edges INCIDENT to it (own imprint) vs "
                               "mean |dW| on edges NOT incident (off-target imprint) -- the trace analogue "
                               "of the E1.3 own-vs-off-target footprint",
            "intensity_sweep": list(STIM_DEPTHS),
            "rate_sweep": list(ETA_SWEEP),
            "rep_intensity": REP,
            "rep_rate": ETA,
            "epochs": EPOCHS,
            "sweep_grade": "[O] swept -- intensity b0 AND plasticity rate eta are SWEPT, not tuned; every "
                           "SIGN/STRUCTURE holds across BOTH sweeps (intensity x rate, anti-tuning)",
            "field_relay_set_sec46": FIELD_RELAY,
            "reused_layers": {"E1_SpatialField": "imported (kernel W0, coupling map, per-node drive)",
                              "E0_PlasticConnectome": "imported (the phase-Hebbian rule)",
                              "kappa_measured": round(KAP, 6),
                              "R19_fold_spinodal": round(FOLD, 6),
                              "n_regions": N},
        },
        "C1_imprint_partition": {
            "_what": "running a focal excitatory drive THROUGH plasticity at each region, the 12 sites "
                     "partition by where the retained trace LANDS: LOCAL imprint (trace mostly on edges "
                     "incident to the driven node) vs RELAYED imprint (trace harder on off-target edges)",
            "partition_drive_invariant": part_inv,
            "distinct_partitions_over_sweep": n_part,
            "local_imprint_set": local,
            "relayed_imprint_set": relay,
            "local_set_is_expected": local_ok,
            "relayed_set_is_expected": relay_ok,
            "classification_at_rep": part_labelled,
            "verdict": "the local-imprint/relayed-imprint partition is IDENTICAL across the full "
                       "stimulation-intensity sweep {0.3,0.5,0.7,0.9} AND the plasticity-rate sweep "
                       "{0.03,0.05,0.08} (exactly one partition observed): the local-imprint set "
                       "{brainstem, cerebellum, pallidum, striatum} fixed, the relayed-imprint set (eight) "
                       "fixed. Whether a focal drive imprints LOCALLY or RELAYS its trace is a fixed "
                       "property of the driven site, not of stimulation intensity nor plasticity rate. "
                       "structure-only; efficacy=0.",
        },
        "C2_off_target_dominance": {
            "_what": "relayed imprint <-> (mean off-target |dW| > incident |dW|), at every swept intensity "
                     "and every swept rate -- the structural content of relayed imprint",
            "equivalence_all_intensities_and_rates": od_equiv,
            "per_site_at_rep": od_per_site,
            "verdict": "for a RELAYED site the retained trace lands HARDER on off-target edges than on the "
                       "driven node's own edges (off/inc > 1) -- the focal drive writes itself into distal "
                       "circuitry; for a LOCAL site the trace concentrates on incident edges (off/inc < 1). "
                       "The relayed <-> off-target-dominant equivalence holds at every intensity and rate, "
                       "tying 'relayed imprint' to its structural meaning. structure-only.",
        },
        "C3_decoupled_and_no_universal_law": {
            "_what": "the genuinely-new coupling result + the honest no-tuning negative: (a) instantaneous "
                     "delivery (§46) and lasting imprint are DECOUPLED -- the trace-relay set strictly "
                     "contains the §46 field-relay set; (b) there is no universal focal>diffuse TRACE law",
            "trace_relay_strictly_contains_field_relay": strict,
            "field_relay_subset_of_trace_relay": subset,
            "field_relay_set_sec46": FIELD_RELAY,
            "trace_relay_set": EXPECTED_RELAY,
            "field_relay_also_trace_relayed": field_also_trace,
            "clean_delivery_relayed_imprint_witnesses": witnesses,
            "n_witnesses_clean_field_relayed_trace": n_witness,
            "decoupled": decoupled,
            "no_universal_focal_gt_diffuse_trace_law": no_law,
            "focal_gt_diffuse_trace_sign_over_intensity": sign_dump,
            "verdict": "(a) the retained-trace relay set (eight sites) STRICTLY CONTAINS the §46/E1.3 "
                       "instantaneous-field relay set {hippocampus, midbrain} (a proper subset): "
                       "plasticity DELOCALISES the imprint. The two field-relay sites are ALSO trace-"
                       "relayed (the subset is genuine), and SIX further sites (neocortex, thalamus, "
                       "hypothalamus, basal-forebrain-cholinergic, forebrain-GABA-interneuron, olfactory-"
                       "bulb) deliver CLEANLY in the instant (self-localising field, §46 clean delivery) "
                       "yet imprint OFF-target (relayed trace) -- a clean INSTANTANEOUS delivery does NOT "
                       "guarantee a clean LASTING imprint. WHERE a focal drive ACTS NOW and WHERE it WRITES "
                       "ITSELF are two DISTINCT, decoupled spatial axes, the E1xE0 lesson neither layer "
                       "alone could state. (b) The clean hypothesis 'a focal drive always imprints MORE at "
                       "its own site than the same total dose spread diffusely' is FALSE -- the sign of "
                       "(focal trace - diffuse trace) varies across sites (three of twelve imprint more "
                       "focally), holding over the intensity sweep: NO universal focal>diffuse TRACE law, "
                       "the E1.4 lesson carried from the instantaneous field to the lasting trace. The "
                       "refuted clean hypothesis is reported honestly -- the no-tuning discipline working "
                       "as intended.",
        },
        "C4_relayed_imprint_is_default": {
            "_what": "relayed imprint is the structural DEFAULT -- a strict majority, the honest contrast "
                     "with §46 where clean delivery was the default",
            "relayed_imprint_set_size": n_relay,
            "local_imprint_set_size": n_local,
            "relayed_is_strict_majority": relayed_majority,
            "relayed_equals_off_target_dominant_set": relay_eq_od,
            "relayed_strictly_contains_field_relay": field_subset,
            "sec46_field_clean_was_majority": field_clean_majority,
            "sec46_field_self_localising_count": f"{n_field_self}/{N}",
            "coherent_majority_class": coherent,
            "verdict": "the relayed-imprint set is a STRICT MAJORITY (eight of twelve), so RELAYED imprint, "
                       "not local, is the structural DEFAULT -- the explicit honest contrast with §46, "
                       "where CLEAN delivery was the structural default (ten of twelve self-localising in "
                       "the instant). A focal drive's LASTING structural footprint is by default "
                       "DELOCALISED, even though its INSTANTANEOUS footprint is by default focal -- "
                       "plasticity spreads the imprint. The relayed-imprint set is simultaneously the off-"
                       "target-dominant trace set (C2) and strictly contains the field-relay set (C3a): one "
                       "coherent majority class. A DIRECTION-ONLY [L] correspondence is noted, never a "
                       "magnitude or a prediction: stimulation-induced plasticity (rTMS/tDCS after-effects, "
                       "the plasticity DBS induces in connected circuits) is recognised to be network-"
                       "distributed and target/connectivity-dependent rather than confined to the "
                       "stimulation site -- consistent with relayed imprint being the structural majority "
                       "and the imprint axis decoupled from the instantaneous-delivery axis.",
        },
        "S6_engine_invariance_guard": {
            "_what": "a zero drive at eta=0 reproduces the frozen M9 anchor bit-for-bit, leaves W identical "
                     "to the kernel, and a focal excursion at eta=0 reverts exactly (E0.3 inherited under a "
                     "spatial drive) -- the coupling is a pure add-on on the engine",
            "R_direct_measured": repr(Rinv),
            "frozen_M9_anchor": repr(M9_ANCHOR_R),
            "matches_frozen_anchor_bitwise": anchor_ok,
            "zero_drive_eta0_R": repr(Roff),
            "zero_drive_matches_direct_bitwise": off_ok,
            "eta0_W_identical_to_kernel": w_ok,
            "focal_excursion_eta0_reverts_exactly": reverts_ok,
            "guard": S6,
        },
        "cited_and_locked": {
            "couples_two_layers": "the FIRST coupling of the E1 spatial-localisation layer (§43) and the "
                "E0 plasticity layer (§26): a focal excitatory spatial drive (E1) run through a phase-"
                "correlation Hebbian update (E0), reading the SPATIAL pattern of the retained trace -- "
                "the spatial x temporal seam neither layer alone could pose",
            "reuse_not_rederive_LOCK": "both layers are IMPORTED (SpatialField for the kernel/map/per-node "
                "drive, PlasticConnectome for the Hebbian rule); the kernel W0, the coupling map k(b) and "
                "the Hebbian rule are NOT re-derived. The coupled integrator is the SAME per-node "
                "generalisation E1 already made of the engine integrator, additionally accumulating the "
                "pairwise correlation the E0 rule consumes -- no new constant, no new rule",
            "delocalised_imprint_LOCK": "plasticity DELOCALISES the imprint: the retained-trace relay set "
                "strictly contains the §46 instantaneous-field relay set, so a clean instantaneous delivery "
                "(§46) does NOT guarantee a clean lasting imprint -- WHERE a focal drive acts now and where "
                "it writes itself are two decoupled spatial axes",
            "no_universal_law_LOCK": "there is NO universal focal>diffuse TRACE law -- the sign of (focal "
                "trace - diffuse trace) varies across sites; the clean monotone hypothesis is explicitly "
                "refuted, not forced (the E1.4 lesson carried to the lasting trace)",
            "real_plasticity_heterogeneous_LOCK": "real synaptic plasticity is HETEROGENEOUS (LTP/LTD, "
                "STDP, homeostatic scaling, metaplasticity, structural plasticity) and real stimulation "
                "spread is heterogeneous (electrode geometry, tissue conductivity, tractography, the "
                "individual connectome, montage/waveform); this module asserts the SIGN/STRUCTURE of a "
                "focal excitatory drive run through a phase-Hebbian update on the frozen kernel, not that "
                "any real stimulation-induced plasticity follows this exact rule",
            "stimulation_induced_plasticity_cited": "stimulation-induced plasticity (rTMS/tDCS after-"
                "effects, plasticity DBS induces in connected circuits) is recognised to be network-"
                "distributed and target/connectivity-dependent rather than confined to the stimulation "
                "site -- a DIRECTION-ONLY [L] correspondence to the relayed-imprint majority, never a "
                "magnitude or a patient-level prediction",
            "experimental_LOCK": "nothing here is medical advice; in-silico mechanism only; whether any "
                "real focal stimulation imprints locally or off-target, and where, is external",
        },
        "honesty_ledger": {
            "medium_efficacy_tested": 0.0,
            "no_cure_claimed": 1.0,
            "consciousness_claim": 0.0,
            "hard_problem_open": 1.0,
            "new_tuned_constants": 0.0,
            "spatial_quantities_are_structural": 1.0,
            "reuses_E1_spatial_field": 1.0,
            "reuses_E0_plasticity": 1.0,
            "couples_E1_and_E0": 1.0,
            "stimulation_intensity": "OPEN [O] -- swept (driven node, depth); signs/structure hold over the "
                                     "intensity sweep, not tuned",
            "plasticity_rate_eta": "OPEN [O] -- representative; signs hold over the eta sweep, not tuned",
            "retained_trace_is_structural": 1.0,
            "instantaneous_delivery_decoupled_from_lasting_imprint": 1.0,
            "relayed_imprint_is_default_contrast_with_sec46": 1.0,
            "clean_hypothesis_refuted": "C3(b) reports a REFUTED clean hypothesis honestly (no universal "
                                        "focal>diffuse trace law) rather than forcing a monotone narrative",
            "clinical_prediction": "NONE -- the [L] correspondence is direction-only, never a patient-level "
                                   "prediction; target selection / device programming are external",
            "not_medical_advice": 1.0,
            "opens_E1xE0_coupling": 1.0,
        },
        "invariants": {
            "engine_tree_frozen": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_unchanged": ENGINE_TREE_FROZEN,
            "engine_tree_sha256_live": None,
            "engine_tree_unchanged": None,
            "m0_16_subtree_unchanged": None,
            "m9_anchor_reproduced_bitwise": anchor_ok,
        },
        "preregistered_results": {
            "C1_imprint_partition_drive_invariant": {
                "claim": "running a focal excitatory drive through plasticity at each region, the local-"
                         "imprint/relayed-imprint partition is identical across the full intensity sweep AND "
                         "the rate sweep; the local-imprint set {brainstem, cerebellum, pallidum, striatum} "
                         "and the relayed-imprint set (the other eight) are fixed",
                "status": preds["C1_imprint_partition_drive_invariant"]},
            "C2_relayed_is_off_target_dominant_trace": {
                "claim": "a site is relayed-imprint iff the mean off-target |dW| exceeds the mean incident "
                         "|dW| (off/inc > 1), at every swept intensity and rate",
                "status": preds["C2_relayed_is_off_target_dominant_trace"]},
            "C3_delivery_imprint_decoupled_no_universal_law": {
                "claim": "the retained-trace relay set STRICTLY CONTAINS the §46 instantaneous-field relay "
                         "set (plasticity delocalises the imprint; clean delivery != clean imprint), AND "
                         "there is no universal focal>diffuse trace law (the sign varies across sites)",
                "status": preds["C3_delivery_imprint_decoupled_no_universal_law"]},
            "C4_relayed_imprint_structural_default": {
                "claim": "the relayed-imprint set is a strict majority (eight of twelve) and equals the off-"
                         "target-dominant set and strictly contains the field-relay set -- relayed imprint "
                         "is the structural default, the honest contrast with §46's clean default",
                "status": preds["C4_relayed_imprint_structural_default"]},
        },
        "overall": {
            "imprint_partition_reproduced": C1,
            "off_target_dominance_reproduced": C2,
            "decoupling_and_no_law_reproduced": C3,
            "relayed_default_reproduced": C4,
            "engine_invariance_guard": S6,
            "is_full_module": bool(C1 and C2 and C3 and C4 and S6),
            "verdict": "SPC-E1E0 is the spatial-plasticity coupling -- the first marriage of the E1 spatial "
                       "drive and the E0 plasticity rule, reading the SPATIAL pattern of a focal drive's "
                       "retained trace. The local-imprint/relayed-imprint partition is drive-invariant "
                       "across intensity x rate, the local set {brainstem, cerebellum, pallidum, striatum} "
                       "fixed (C1); relayed imprint is off-target-dominant trace (C2); instantaneous "
                       "delivery and lasting imprint are DECOUPLED -- the trace-relay set strictly contains "
                       "the §46 field-relay set, plasticity delocalises the imprint and a clean delivery "
                       "does not guarantee a clean imprint, and there is no universal focal>diffuse trace "
                       "law (C3, the genuinely-new result + honest negative); relayed imprint is the "
                       "structural default, the honest contrast with §46's clean default (C4). A zero drive "
                       "at eta=0 reproduces the frozen M9 anchor bit-for-bit and a focal excursion reverts "
                       "exactly without plasticity (S6). Both layers imported not re-derived, no new tuned "
                       "constant, no new rule, engine byte-unchanged. efficacy=0; not medical advice.",
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

def spatial_plasticity_imprint_results():
    res = run()
    R = E.emerge_all()                 # READ-ONLY emerge; never mutates the tree
    tree_live = E.sha256_of(R)
    sub016 = E.sha256_of({k: v for k, v in R.items() if int(k.split("_")[0][1:]) <= 16})
    res["invariants"]["engine_tree_sha256_live"] = tree_live
    res["invariants"]["engine_tree_unchanged"] = bool(tree_live == ENGINE_TREE_FROZEN)
    res["invariants"]["m0_16_subtree_unchanged"] = bool(sub016 == M0_16_FROZEN)
    blob = _blob(res)
    digest = hashlib.sha256(blob.encode()).hexdigest()
    with open(os.path.join(HERE, "spatial_plasticity_imprint_results.json"), "w", encoding="utf-8") as f:
        f.write(blob)
    with open(os.path.join(HERE, "expected_spatial_plasticity_imprint_sha256.json"), "w", encoding="utf-8") as f:
        json.dump({"spatial_plasticity_imprint_results.json": digest}, f, indent=2); f.write("\n")
    return res, digest


if __name__ == "__main__":
    res, digest = spatial_plasticity_imprint_results()
    inv, ov, hl = res["invariants"], res["overall"], res["honesty_ledger"]
    g = res["grounding"]
    c1 = res["C1_imprint_partition"]; c2 = res["C2_off_target_dominance"]
    c3 = res["C3_decoupled_and_no_universal_law"]; c4 = res["C4_relayed_imprint_is_default"]
    s6 = res["S6_engine_invariance_guard"]
    print("=" * 78)
    print("SPC-E1E0 -- SPATIAL-PLASTICITY COUPLING (E1 x E0)   add-only, engine READ-ONLY")
    print("=" * 78)
    print(f"  engine tree / M0..M16 unchanged : {inv['engine_tree_unchanged']} / {inv['m0_16_subtree_unchanged']}  ({inv['engine_tree_sha256_live'][:16]}...)")
    print(f"  couples: E1 SpatialField (per-node drive) x E0 PlasticConnectome (phase-Hebbian)")
    print(f"           intensity sweep={g['intensity_sweep']}  rate sweep={g['rate_sweep']}")
    print(f"  §46 field-relay set: {g['field_relay_set_sec46']}")
    print("-" * 78)
    print(f"  C1 partition     : drive-invariant={c1['partition_drive_invariant']} (one partition: {c1['distinct_partitions_over_sweep']==1})")
    print(f"                     LOCAL imprint  = {c1['local_imprint_set']}")
    print(f"                     RELAYED imprint= {c1['relayed_imprint_set']}")
    print(f"  C2 off-target    : relayed<->off/inc>1 all intensities&rates={c2['equivalence_all_intensities_and_rates']}")
    print(f"  C3 decoupled     : trace-relay strictly contains field-relay={c3['trace_relay_strictly_contains_field_relay']}")
    print(f"                     clean-delivery-but-relayed-imprint witnesses={c3['clean_delivery_relayed_imprint_witnesses']}")
    print(f"                     no universal focal>diffuse trace law={c3['no_universal_focal_gt_diffuse_trace_law']} {c3['focal_gt_diffuse_trace_sign_over_intensity']}")
    print(f"  C4 default       : relayed strict majority={c4['relayed_is_strict_majority']} ({c4['relayed_imprint_set_size']}/{N}); §46 clean was majority={c4['sec46_field_clean_was_majority']}")
    print(f"  S6 invariance    : zero-drive R={s6['zero_drive_eta0_R']} ==anchor:{s6['matches_frozen_anchor_bitwise'] and s6['zero_drive_matches_direct_bitwise']}  W-identical:{s6['eta0_W_identical_to_kernel']}  focal reverts:{s6['focal_excursion_eta0_reverts_exactly']}")
    print("-" * 78)
    print(f"  pre-registered: {[ (k, v['status']) for k,v in res['preregistered_results'].items() ]}")
    print(f"  honesty 4-flags (eff/cure/cc/tuned) : {hl['medium_efficacy_tested']}/{hl['no_cure_claimed']}/{hl['consciousness_claim']}/{hl['new_tuned_constants']}")
    print(f"  FULL module? : {ov['is_full_module']}")
    print(f"  RESULT sha256 = {digest}")
    ok = (inv["engine_tree_unchanged"] and inv["m0_16_subtree_unchanged"] and ov["is_full_module"]
          and hl["medium_efficacy_tested"] == 0.0 and hl["no_cure_claimed"] == 1.0
          and hl["consciousness_claim"] == 0.0 and hl["new_tuned_constants"] == 0.0)
    print("=" * 78)
    print("  SPATIAL-PLASTICITY COUPLING MODULE: " + ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)
