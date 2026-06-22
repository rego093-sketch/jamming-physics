#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E3-bulb-map/run.py — INCREMENT E3: the bulb map (the spatial projection of the code).

WHAT E3 DOES (BLUEPRINT.md E3; research/E3-bulb-map/START_HERE.md).
  E1 established smell's identity code in RECEPTOR space: a combinatorial pattern over the OR bank
  (2^N patterns), substrate-derived in its threshold/order but ligand-limited in its KEY [O]. The
  sibling senses turn their code into a spatial IMAGE on a sheet (retinotopy / tonotopy). Smell's
  substitute is the OLFACTORY BULB MAP: the axons of every olfactory sensory neuron expressing the
  SAME OR converge onto one (or a few) specific GLOMERULI, so the receptor-space code becomes a
  spatial ODOUR MAP — a fixed pattern of glomerular activity per odorant (Mombaerts; Mori).

  E3 reads what the frozen substrate + measured atlas can HONESTLY say about that map, and — exactly
  as E1 separated a switch's THRESHOLD (in γ) from its odorant KEY (not in γ) — separates what the
  substrate fixes (the map's ORDER and CAPACITY) from what it does NOT (the map's COORDINATES).
  Three things, stated honestly:

    PART A — THE MAP'S DEVELOPMENTAL ORDER: the organisers emerge as R19 ORGANS in spinodal(γ) order.
      The OSN-identity transcription factors (LHX2, EBF1, EMX2 — γ MEASURED) govern OSN
      differentiation and OR-gene choice, i.e. they BUILD the apparatus that lays the map down. Each
      is the inherited R19 Organ primitive (vp_substrate.Organ, FROZEN): its measured γ sets a
      DISCONTINUOUS presence threshold h*=(2/3√3)γ^1.5, the organisers emerge in spinodal(γ) order,
      and an intact downstream pathway with the master switch OFF still yields ABSENCE ("parts
      present ≠ trait"). That emergence ORDER is forced by the measured γ [F]/[L]. The absolute
      developmental TIME (in days) is the dwell-calibration [O], as always.

    PART B — CONVERGENCE IS A BIJECTION; IT PRESERVES THE COMBINATORIAL CAPACITY (code → spatial map).
      The one-OR→one-glomerulus convergence is, structurally, an INJECTIVE relabelling of the N
      receptor channels onto N bulb positions. A bijection on N channels induces a bijection on their
      2^N ON/OFF subsets [F] — so the receptor-space code's full capacity 2^N (E1) is carried INTACT
      into bulb space as 2^N distinguishable spatial activity maps. We PROVE this on the full subset
      lattice with a fixed abstract relabelling (NOT a measured coordinate — illustration only): the
      image of all 2^N subsets is again 2^N distinct subsets. And because a bijection preserves
      subset CHAINS, E1's nested-thermometer readout (a uniform developmental drive flips glomeruli ON
      in spinodal(γ) order) maps to a nested thermometer IN SPACE (≤ N+1 nested spatial patterns),
      fully substrate-derived. The spatial map inherits the code's order and capacity [V].

    PART C — THE HONEST [O]: the TARGETING COORDINATE — which glomerulus an OR maps to — is not in γ.
      What the substrate does NOT supply is WHICH physical glomerulus a given OR's axons navigate to.
      That targeting coordinate is set by AXON-GUIDANCE chemistry — the OR protein's own signalling
      (OR → cAMP level → graded guidance-receptor expression: Neuropilin-1/Sema3A, ephrin-A/EphA,
      etc.) — which lives in the receptor's coding sequence + cascade, NOT in the promoter γ. It is
      the same KIND of [O] as E1's odorant key: the substrate fixes the map's ORDER and CAPACITY; it
      does NOT fix its COORDINATES. Named, never invented or fitted.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E3 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing, fits nothing.
    - the R19 Organ + switch math (Organ/spinodal/settle/is_on/dwell) ← inherited/vp_substrate.py (frozen)
    - γ (LEVEL) + A4 (SHAPE) per organiser/OR gene                    ← inherited/organ_gamma.json (MEASURED
                                                                        [L]; verify_seed [3] re-proves it offline)
  γ is measured, never fitted (FIREWALL #3); γ is promoter STRUCTURE only — never a guidance-receptor
  gradient, an axon target, a glomerular coordinate, or a percept (FIREWALL #1/#2). The glomerular
  targeting coordinate is a named [O] (axon-guidance chemistry); the felt percept of a smelled odour
  belongs to the mind volume (FIREWALL #5). Nothing here diagnoses or treats (FIREWALL #4). The
  abstract relabelling in Part B exists only to prove the bijection theorem; it is not a measured map.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen substrate's scalar helpers + the Organ primitive — pure math, no RNG.
Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import spinodal, barrier, settle, is_on, dwell, Organ   # FROZEN: the R19 switch + Organ

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the OSN-identity organisers (by atlas node) — they build the map-laying apparatus; stated, not selected.
ORGANISERS = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_neuron_identity"))
# the OR bank (the combinatorial channels of E1) — the same N receptor channels that converge to glomeruli.
OR_GENES   = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_receptor"))

N_STEPS, DT = 1500, 0.02            # the FROZEN settle() defaults — fixed, not tuned


def rest_basin(g):
    return -math.sqrt(g)


def thermometer_on_sets():
    """E1's substrate-derived readout: a uniform developmental drive swept up flips the FROZEN OR
    switches ON in spinodal(γ) order — the nested thermometer (receptor-space). Returns the ordered
    list of distinct ON-sets (channels named by OR symbol), each a tuple in spinodal order."""
    order = sorted(OR_GENES, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    thr   = sorted(spinodal(ATLAS[s]["gamma"]) for s in OR_GENES)
    seen  = []
    for frac in (0.0, 0.50, 0.80, 0.90, 0.95, 1.00, 1.05, 1.20):
        h = frac * thr[-1] * 1.05
        on = tuple(s for s in order
                   if settle(ATLAS[s]["gamma"], h, s0=rest_basin(ATLAS[s]["gamma"]), n=N_STEPS, dt=DT) > 0.0)
        if on not in seen:
            seen.append(on)
    return order, seen


def run(P):
    P("=" * 80)
    P("E3 — THE BULB MAP   (one OR → one glomerulus: the combinatorial code becomes a spatial map)")
    P("=" * 80)
    P("consumes (frozen): vp_substrate.Organ/spinodal/settle/is_on/dwell · organ_gamma.json γ+A4 (MEASURED)")
    P("re-derives: nothing. γ measured, never fitted. γ = promoter STRUCTURE only (firewall).")
    P("builds on E1: the receptor-space combinatorial code (2^N) is PROJECTED onto the olfactory bulb.")
    P(f"the measured organisers (N={len(ORGANISERS)}): {', '.join(ORGANISERS)}")
    P(f"the OR bank that converges (N={len(OR_GENES)}): {', '.join(OR_GENES)}")

    # ------------------------------------------------------------------------------------------
    # PART A — the map's developmental order: organisers emerge as R19 Organs in spinodal(γ) order
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — the map's developmental ORDER: the organisers emerge as R19 Organs in spinodal(γ) order  [F]")
    P("-" * 80)
    P("the OSN-identity TFs build the apparatus that lays the map down; each is the inherited R19 Organ:")
    organs = {s: Organ(s, ATLAS[s]["gamma"], master=s, layer="olfactory_neuron_identity") for s in ORGANISERS}
    order = sorted(ORGANISERS, key=lambda s: organs[s].functional_spinodal())
    P(f"  {'order':>5} {'organiser':9s} {'role':34s} {'γ':>7s} {'h*=spinodal':>11s} {'dwell∝γ^1.5':>11s}")
    for k, sym in enumerate(order, 1):
        o = organs[sym]
        P(f"  {k:5d} {sym:9s} {ATLAS[sym].get('role','')[:34]:34s} {o.g:7.4f} "
          f"{o.functional_spinodal():11.5f} {o.size(brake=0.5):11.5f}")
    by_gamma = sorted(ORGANISERS, key=lambda s: ATLAS[s]["gamma"])
    assert order == by_gamma, "organiser emergence order must be monotone in γ (spinodal order)"
    P("  → the organisers emerge in spinodal(γ) order; lowest γ = lowest presence threshold = first.  [F]")

    # "parts present ≠ trait": an organiser is present only if its master cis drive clears the γ-threshold
    P("\n[parts present ≠ trait] each Organ is PRESENT only if its master cis-drive clears its γ-threshold:")
    P(f"  {'organiser':9s} {'present@0.90·h*':>15s} {'present@1.10·h*':>15s}")
    for sym in order:
        o = organs[sym]; hstar = o.functional_spinodal()
        lo = o.present(0.90 * hstar); hi = o.present(1.10 * hstar)
        P(f"  {sym:9s} {str(lo):>15s} {str(hi):>15s}")
        assert (lo is False) and (hi is True), f"{sym}: Organ must be absent below h*, present above"
    P("  → an intact downstream pathway with the master switch OFF still yields ABSENCE (a real organ,")
    P("    not parts).  [F] order/presence · [L] γ measured · [O] absolute developmental time (dwell scale).")

    # ------------------------------------------------------------------------------------------
    # PART B — convergence is a bijection; it preserves the combinatorial capacity (code → spatial map)
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — convergence is a BIJECTION; it preserves the combinatorial capacity 2^N (code → map)")
    P("-" * 80)
    N = len(OR_GENES)
    P(f"one OR → one glomerulus is, structurally, an injective relabelling of the N={N} receptor channels")
    P(f"onto N={N} bulb positions. A bijection on N channels induces a bijection on their 2^N ON/OFF")
    P(f"subsets [F] — so the receptor-space code's capacity is carried INTACT into bulb space.")

    # PROVE it on the full subset lattice with a FIXED abstract relabelling (NOT a measured coordinate).
    chans = list(range(N))                                   # the N abstract receptor-channel indices
    perm  = {c: (N - 1 - c) for c in chans}                  # an ABSTRACT bijection (reverse) — illustration only
    images = set()
    for mask in range(2 ** N):                               # enumerate all 2^N ON/OFF subsets
        subset = frozenset(c for c in chans if (mask >> c) & 1)
        images.add(frozenset(perm[c] for c in subset))       # the convergence-relabelled (glomerulus) subset
    P(f"\n[capacity theorem] enumerated all 2^{N} = {2**N} receptor ON/OFF subsets; under a fixed bijective")
    P(f"  relabelling (abstract, NOT a measured map) the IMAGE set has {len(images)} distinct glomerulus")
    P(f"  patterns = 2^{N} = {2**N}. The combinatorial capacity is PRESERVED — the code becomes a SPATIAL")
    P(f"  odour map of the same size.  [F] (a bijection preserves the subset count exactly).")
    assert len(images) == 2 ** N, "a bijection must preserve the 2^N subset count (capacity)"

    # the substrate-derived nested thermometer maps to a nested thermometer IN SPACE (chains preserved)
    P("\n[spatial thermometer] E1's nested-thermometer readout (uniform developmental drive flips switches")
    P("  ON in spinodal(γ) order) is a subset CHAIN; a bijection preserves chains, so it maps to a nested")
    P("  thermometer IN SPACE — glomeruli light in the same order, ≤ N+1 nested spatial patterns:")
    ord_or, on_sets = thermometer_on_sets()
    pos = {sym: i for i, sym in enumerate(ord_or)}           # the convergence relabelling: OR → bulb position
    P(f"  {'# ON':>5s}  receptor-space ON set            →  bulb-space positions (glomeruli)")
    spatial = []
    for on in on_sets:
        glo = tuple(sorted(pos[s] for s in on))
        spatial.append(set(glo))
        rs = ("{" + ",".join(on) + "}") if on else "{}"
        P(f"  {len(on):5d}  {rs:32s} →  {('g' + ',g'.join(map(str, glo))) if glo else '(none)'}")
    nested = all(spatial[i].issubset(spatial[i + 1]) for i in range(len(spatial) - 1))
    assert nested and len(spatial) <= N + 1, "the spatial thermometer must be nested and ≤ N+1 (chain preserved)"
    P(f"  → {len(spatial)} nested spatial patterns (≤ N+1={N+1}); the map inherits the code's ORDER and")
    P(f"    CAPACITY from the FROZEN switch + measured γ.  [V] (full 2^N richness still needs the ligand [O]).")

    # ------------------------------------------------------------------------------------------
    # PART C — the honest [O]: the targeting coordinate — which glomerulus an OR maps to — is not in γ
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — the honest [O]: the TARGETING COORDINATE (which glomerulus an OR maps to) is NOT in γ")
    P("-" * 80)
    P("the substrate fixes the map's ORDER (Part A) and CAPACITY (Part B). It does NOT fix WHICH physical")
    P("glomerulus a given OR's axons navigate to — the targeting COORDINATE. That is axon-guidance")
    P("chemistry: the OR protein's own signalling (OR → cAMP level → graded guidance-receptor expression,")
    P("e.g. Neuropilin-1/Sema3A, ephrin-A/EphA), in the receptor's coding sequence + cascade, NOT in γ.")
    # show concretely that γ orders the channels but says nothing about a spatial coordinate
    P("\n[what γ gives vs what it cannot]:")
    P(f"  {'OR gene':8s} {'γ':>7s} {'spinodal(γ)':>11s} {'→ channel rank':>14s} {'glomerulus coordinate':>22s}")
    for k, sym in enumerate(ord_or, 1):
        P(f"  {sym:8s} {ATLAS[sym]['gamma']:7.4f} {spinodal(ATLAS[sym]['gamma']):11.5f} "
          f"{k:14d} {'[O] axon-guidance':>22s}")
    P("  → γ supplies the channel/excitability RANK (a 1-D order), never a 2-D bulb COORDINATE.")
    P("    This is the SAME KIND of gap as E1's odorant key: structure (order, capacity) is substrate-")
    P("    derived; the molecular SPECIFICITY (which odorant / which glomerulus) is the named [O].")

    # ------------------------------------------------------------------------------------------
    # grades + learned
    # ------------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E3 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : the organisers emerge as R19 Organs in spinodal(γ) order; the one-OR→one-")
    P("                 glomerulus convergence is a bijection, and a bijection on N channels induces a")
    P("                 bijection on the 2^N subsets — so the code's capacity is preserved as a map.")
    P("  [V] verified : the organiser order is monotone in γ and each Organ is absent below h* / present")
    P("                 above (parts present ≠ trait); the full 2^N subset lattice maps to 2^N distinct")
    P("                 spatial patterns; E1's nested thermometer maps to a nested spatial thermometer")
    P("                 (≤ N+1). (γ+A4 re-proved offline bit-for-bit by verify_seed [3].)")
    P("  [L] measured : every organiser/OR γ (+A4) from NCBI promoters, cached, byte-identical to atlas.")
    P("  [O] open     : the TARGETING COORDINATE — which glomerulus an OR maps to — is axon-guidance")
    P("                 chemistry (OR→cAMP→guidance-receptor gradient), NOT in γ; the full 2^N spatial")
    P("                 richness still needs the odorant key (E1 [O]); the absolute developmental TIME")
    P("                 (dwell scale); the FELT percept of the smelled odour (→ mind volume).")
    P("\nLEARNED: the bulb map is smell's spatial image, and the substrate reaches exactly its STRUCTURE.")
    P("         The R19 Organ primitive forces the organisers' emergence ORDER (spinodal(γ)); the one-")
    P("         OR→one-glomerulus convergence is a bijection, so the receptor-space combinatorial code")
    P("         (E1, 2^N) is carried INTACT into bulb space as a 2^N spatial odour map with the same")
    P("         order. What the substrate does NOT give is the map's COORDINATES — which physical")
    P("         glomerulus each OR targets — exactly as it did not give E1's odorant key. Both are the")
    P("         same KIND of molecular [O], named not hidden. Foundation untouched; nothing fitted.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
