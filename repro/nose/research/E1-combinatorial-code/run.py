#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E1-combinatorial-code/run.py — INCREMENT E1: the combinatorial code (the honest departure).

WHAT E1 DOES (BLUEPRINT.md E1; research/E1-combinatorial-code/START_HERE.md).
  This is where the sibling senses' organising insight HONESTLY BREAKS. Vision and hearing are a
  WAVE property → a single PHYSICAL place (propagation angle χ / basilar-membrane position) → one R19
  switch. Smell has NO wave: the stimulus is a MOLECULE. There is no single place and no angle to
  read, so the identity is carried a different way — a COMBINATORIAL pattern across a large receptor
  repertoire (Buck & Axel): each odorant activates a SUBSET of olfactory receptors, each receptor
  responds to many odorants, and the odorant's identity is the PATTERN of which receptors fire.

  Built ONLY on the frozen inherited substrate + the measured atlas, three things — stated honestly:

    PART A — EACH OR IS AN R19 SWITCH; MEASURED γ SETS THE THRESHOLD ORDER (the ONE thing γ supplies).
      The olfactory-receptor genes (OR1D2, OR2J3, OR2W1, OR5AN1, OR6A2, OR51E2, OR7D4 — γ MEASURED) are a
      bank of inherited R19 switches. Their measured γ gives each switch a spinodal threshold
      h*=(2/3√3)γ^1.5 (vp_substrate, FROZEN); ordering by spinodal(γ) ranks them from most to least
      trigger-happy [F]. That excitability/expression ordering is the ONLY thing the promoter γ
      encodes here. It does NOT encode which odorant binds which receptor.

    PART B — THE CODE IS COMBINATORIAL (capacity 2^N ≫ N); the FULL richness needs the ligand [O].
      A bank of N all-or-none switches has up to 2^N distinguishable ON/OFF patterns — vastly more
      than N. THAT is why the genome carries hundreds of OR genes: not one-receptor-per-odour, but a
      COMBINATORIAL code over the bank. We show the readout MECHANISM honestly: under a uniform drive
      swept upward, the FROZEN switches flip ON in spinodal(γ) order — a nested THERMOMETER readout of
      N+1 patterns, fully substrate-derived from the measured thresholds. But the thermometer reaches
      only N+1 of the 2^N patterns; the rest require an ODORANT-SPECIFIC drive VECTOR (different drive
      per receptor) — and that vector (which molecule drives which receptor, how hard) is NOT in the
      promoter γ. It is the receptor protein's binding-pocket chemistry (coding sequence + 3D fold) —
      the named [O]. We feed only an ABSTRACT illustrative vector to show the readout; no odorant
      affinity is invented or claimed.

    PART C — THE HONEST NEGATIVE: smell's "what" is NOT a substrate quantity (unlike vision's colour).
      In vision the percept's identity — colour — IS a substrate quantity: the propagation angle χ(λ),
      forced by the invariant quantum D [F]. In smell the percept's identity — odour — is NOT a
      substrate quantity: it is a combinatorial pattern whose KEY (odorant→receptor matching) lives in
      molecular recognition, outside the promoter γ and even outside the A4 SHAPE. The OR genes have
      distinct (γ, A4) readings — they are not degenerate — but that distinguishes their EXPRESSION /
      THRESHOLD structure, never their odorant TUNING. This is the seed's central, deliberately
      preserved finding: the VP wave-substrate reaches the olfactory THRESHOLD and TRANSDUCTION layers
      (E2) but NOT the odorant-identity layer — and exactly where it stops is nameable [O], not hidden.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E1 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing, fits nothing.
    - the R19 switch math (spinodal/settle/is_on) ← inherited/vp_substrate.py (frozen, no-regression)
    - γ (LEVEL) + A4 (SHAPE) per OR gene          ← inherited/organ_gamma.json (MEASURED [L]; the
                                                    verifier [3] re-proves it offline bit-for-bit [V])
  γ is measured, never fitted (FIREWALL #2); γ is promoter STRUCTURE only — never a ligand affinity,
  a receptor occupancy, a firing rate, or a percept (FIREWALL #1). The odorant→receptor drive is a
  named [O] (binding-pocket chemistry); the felt experience of smelling belongs to the mind volume
  (FIREWALL #4). Nothing here diagnoses or treats (FIREWALL #3). The abstract drive vector in Part B
  exists only to illustrate the readout; it is not a measured affinity and is never used as one.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen substrate's scalar helpers — pure math, no RNG.
Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import spinodal, barrier, settle, is_on        # FROZEN: the R19 switch primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the olfactory-receptor bank (by atlas node) — stated, not selected to a target.
OR_GENES = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_receptor"))

N_STEPS, DT = 1500, 0.02            # the FROZEN settle() defaults — fixed, not tuned


def rest_basin(g):
    return -math.sqrt(g)


def on_pattern(drive_vec):
    """The combinatorial barcode: which OR switches flip ON under a per-receptor drive vector.
    Uses ONLY the FROZEN R19 switch + the measured γ thresholds. drive_vec maps OR symbol → drive h."""
    pat = {}
    for sym in OR_GENES:
        g = ATLAS[sym]["gamma"]
        pat[sym] = bool(settle(g, drive_vec[sym], s0=rest_basin(g), n=N_STEPS, dt=DT) > 0.0)
    return pat


def run(P):
    P("=" * 80)
    P("E1 — THE COMBINATORIAL CODE   (smell has no wave; identity is a pattern over R19 switches)")
    P("=" * 80)
    P("consumes (frozen): vp_substrate.spinodal/settle/is_on · organ_gamma.json γ+A4 (MEASURED)")
    P("re-derives: nothing. γ measured, never fitted. γ = promoter STRUCTURE only (firewall).")
    P("the honest departure: vision/hearing read a WAVE→PLACE; smell reads a MOLECULE→PATTERN.")
    P(f"the measured OR bank (N={len(OR_GENES)}): {', '.join(OR_GENES)}")

    # ------------------------------------------------------------------------------------------
    # PART A — each OR is an R19 switch; measured γ sets the threshold order
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — each OR is an inherited R19 switch; MEASURED γ sets the threshold order  [F]")
    P("-" * 80)
    P("the ONE thing the promoter γ encodes here is each switch's excitability (spinodal threshold):")
    order = sorted(OR_GENES, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    P(f"  {'rank':>4} {'OR gene':8s} {'role':34s} {'γ':>7s} {'h*=spinodal':>11s} {'barrier':>8s}")
    for k, sym in enumerate(order, 1):
        g = ATLAS[sym]["gamma"]
        P(f"  {k:4d} {sym:8s} {ATLAS[sym].get('role',''):34s} {g:7.4f} {spinodal(g):11.5f} {barrier(g):8.4f}")
    # the ordering is real and monotone in γ (lowest γ = lowest threshold = most trigger-happy)
    by_gamma = sorted(OR_GENES, key=lambda s: ATLAS[s]["gamma"])
    assert order == by_gamma, "spinodal order must be monotone in γ (lowest γ flips first)"
    P("  → ordered most→least trigger-happy by spinodal(γ).  [F] threshold order · [L] γ measured.")
    P("    [O] this is EXCITABILITY/expression only — NOT which odorant binds which receptor.")

    # ------------------------------------------------------------------------------------------
    # PART B — the code is combinatorial (2^N ≫ N); the full richness needs the ligand [O]
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — the identity code is COMBINATORIAL: capacity 2^N ≫ N; full richness needs the ligand [O]")
    P("-" * 80)
    N = len(OR_GENES)
    P(f"a bank of N={N} all-or-none switches has up to 2^N = {2**N} distinguishable ON/OFF patterns")
    P(f"  — vastly more than the N={N} receptors. THAT is why the genome carries hundreds of OR genes:")
    P(f"  a COMBINATORIAL code, not one-receptor-per-odour. (Human repertoire ≈400 ORs → 2^400 patterns,")
    P(f"  astronomically beyond any number of odours — the combinatorial scheme's whole point.)")

    # the readout MECHANISM, substrate-derived: a uniform drive swept up flips switches in spinodal order
    P("\n[thermometer readout — fully substrate-derived] uniform drive swept up: switches flip in h* order:")
    thresholds = sorted(spinodal(ATLAS[s]["gamma"]) for s in OR_GENES)
    seen = set(); patterns_uniform = []
    P(f"  {'uniform h':>10s} {'# ON':>5s}  ON set (combinatorial barcode at this drive)")
    for frac in (0.0, 0.50, 0.80, 0.90, 0.95, 1.00, 1.05, 1.20):
        h = frac * thresholds[-1] * 1.05          # sweep from 0 to just past the highest threshold
        vec = {s: h for s in OR_GENES}            # UNIFORM drive (not odorant-specific)
        pat = on_pattern(vec)
        on_set = tuple(s for s in order if pat[s])
        key = on_set
        if key not in seen:
            seen.add(key); patterns_uniform.append(on_set)
        P(f"  {h:10.5f} {sum(pat.values()):5d}  {on_set if on_set else '(all off)'}")
    n_uniform = len(patterns_uniform)
    P(f"  → uniform drive yields a NESTED thermometer code of {n_uniform} patterns (≤ N+1={N+1}),")
    P(f"    determined entirely by the measured spinodal(γ) thresholds + the FROZEN R19 flip.  [V]")
    assert n_uniform <= N + 1, "a uniform drive can reach at most N+1 nested patterns (thermometer)"

    # the FULL combinatorial richness requires an odorant-specific drive VECTOR = the ligand [O]
    P("\n[the gap — the ligand [O]] the thermometer reaches only %d of 2^%d=%d patterns; the other %d"
      % (n_uniform, N, 2**N, 2**N - n_uniform))
    P("  require an ODORANT-SPECIFIC drive VECTOR (different drive per receptor). Example: an ABSTRACT")
    P("  vector that drives only the 1st & 3rd-ranked ORs hard (NOT a measured affinity — illustration):")
    illustrative = {s: (1.2 * spinodal(ATLAS[s]["gamma"]) if s in (order[0], order[2]) else 0.0)
                    for s in OR_GENES}            # abstract: lights a NON-nested subset
    pat = on_pattern(illustrative)
    on_set = tuple(s for s in order if pat[s])
    P(f"    abstract odorant → ON set {on_set}  — a NON-nested pattern unreachable by uniform drive.")
    nested_keys = {p for p in patterns_uniform}
    assert tuple(on_set) not in nested_keys, "the vector-driven pattern must be outside the thermometer set"
    P("  → the COMBINATORIAL richness is real, but its KEY — the odorant→receptor drive — is NOT in γ.")
    P("    [O] it is the receptor binding-pocket chemistry (coding sequence + 3D fold); never invented.")

    # ------------------------------------------------------------------------------------------
    # PART C — the honest negative: smell's "what" is not a substrate quantity
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — the honest negative: smell's IDENTITY is not a substrate quantity (unlike vision's colour)")
    P("-" * 80)
    P("vision: the percept's identity (COLOUR) IS a substrate quantity — the propagation angle χ(λ),")
    P("        forced by the invariant quantum D.  [F]")
    P("smell:  the percept's identity (ODOUR) is NOT a substrate quantity — it is a combinatorial")
    P("        pattern whose key (odorant↔receptor) is molecular recognition, outside γ AND A4.")
    # the OR genes are NOT degenerate in (γ, A4) — but that is expression structure, not odour tuning
    P("\n[OR (γ, A4) readings are distinct — but this is EXPRESSION structure, not odorant tuning]:")
    P(f"  {'OR gene':8s} {'γ':>7s} {'shape_amp(A4)':>13s} {'stiff_side':>10s}")
    amps = []
    for sym in order:
        a = ATLAS[sym]
        amps.append(a["shape_amplitude"])
        P(f"  {sym:8s} {a['gamma']:7.4f} {a['shape_amplitude']:13.5f} {a['stiff_side_frac']:10.4f}")
    distinct = len(set(round(x, 5) for x in amps)) == len(amps)
    P(f"  all {len(OR_GENES)} A4 shape amplitudes distinct? {distinct} — the ORs are not degenerate in shape,")
    P("  yet (γ, A4) fixes their THRESHOLD/expression layer only. Odorant tuning stays [O] (binding pocket).")
    assert distinct, "the measured OR genes should be non-degenerate in A4 shape (expression structure)"

    # ------------------------------------------------------------------------------------------
    # grades + learned
    # ------------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E1 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : each OR is the inherited R19 switch; spinodal(γ) orders the bank by")
    P("                 excitability; a bank of N all-or-none switches has 2^N combinatorial patterns.")
    P("  [V] verified : the threshold order is monotone in γ; a uniform drive flips the FROZEN switches")
    P("                 in spinodal order into a nested thermometer code (≤N+1); an odorant-specific")
    P("                 vector reaches a non-nested pattern outside it; the OR (γ,A4) readings are")
    P("                 distinct. (γ+A4 re-proved offline bit-for-bit by verify_seed [3].)")
    P("  [L] measured : every OR-gene γ (+A4) from NCBI promoters, cached, byte-identical to atlas.")
    P("  [O] open     : THE ODORANT→RECEPTOR DRIVE — which molecule binds which OR, how hard — is the")
    P("                 receptor binding-pocket chemistry (coding sequence + 3D fold), NOT in γ or A4.")
    P("                 This is the combinatorial code's key; it is named, never invented or fitted.")
    P("                 The felt experience of smelling → mind volume.")
    P("\nLEARNED: smell breaks the wave→place skeleton honestly. The inherited substrate still supplies")
    P("         the OR bank (R19 switches), the spinodal(γ) excitability order, and the combinatorial")
    P("         readout mechanism — but the IDENTITY of an odour is a pattern whose key is molecular")
    P("         recognition, outside the promoter γ and even the A4 shape. Unlike vision (colour = a")
    P("         substrate angle), smell's 'what' is NOT a substrate quantity. The seed states exactly")
    P("         where the framework reaches (threshold + transduction, E2) and where it stops (odorant")
    P("         tuning, [O]). Foundation untouched; nothing fitted; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
