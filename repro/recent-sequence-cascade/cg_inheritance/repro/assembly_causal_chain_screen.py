#!/usr/bin/env python3
"""
Continental-Genesis repro screen 12 -- Pacific-opening -> one-sided assembly: causal chain.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19. PURE PHYSICS ONLY. No geology, no dates, no deformation history.

The charge: assemble, from DATA + pure physics alone, the causal chain by which an opening
(a 'Pacific' rupture) FORCES a one-sided continental mass -- step by step, brutally, with NO
average/geological theory.

HARD HONESTY FIRST -- what 'simulation' can and cannot mean here:
  * A time-stepped reconstruction is FORBIDDEN: it needs absolute ages + a deformation history,
    which the firewall bars and which (the author's rule) geology cannot supply. So this is NOT
    a movie.
  * What pure physics CAN force is a CAUSAL DEPENDENCY CHAIN -- a sequence of ENTAILMENTS, each
    of the form 'given the present-tense facts X and conservation law L, Y is necessary'. The
    chain is logical/physical necessity, not a timeline. Every step states its FORCING law and
    its grade; every place geology would be needed is FLAGGED as a GAP, not filled.

This screen lays out the chain, computes the one quantitative kinematic closure that physics
forces (fixed-area sphere: opening area = closing area), and marks the gaps.
"""
import hashlib, math

SEED = 19

# ===== LOCK BLOCK (present-tense measured constants; no ages) =====
R_EARTH   = 6.371e6     # m     Earth radius (present-tense geodesy)
A_SPHERE  = 4*math.pi*R_EARTH**2          # m^2  total surface area (fixed: rigid radius)
RHO_M     = 3300.0      # kg/m^3 mantle
RHO_FEL   = 2800.0      # kg/m^3 felsic crust (buoyant)
RHO_BAS   = 2900.0      # kg/m^3 basaltic skin
# illustrative present-tense opening rate band (GPS-class), to show the closure is rate-FREE
V_OPEN_CM_YR = [2.0, 5.0, 10.0]   # used ONLY to show area-closure is independent of rate
# =================================================================

def cm_yr_to_m_s(v): return v/100.0/3.15576e7

L = []
L.append("PACIFIC-OPENING -> ONE-SIDED ASSEMBLY: CAUSAL CHAIN (pure physics)")
L.append(f"VP-SPEC  SEED={SEED}  NO geology, NO dates, NO deformation history")
L.append("="*64)
L.append("")
L.append("FRAME: this is a chain of ENTAILMENTS (physical necessity), NOT a timeline.")
L.append("Each step: [FORCING LAW] -> consequence -> grade. Gaps are FLAGGED, not filled.")
L.append("")

# --- STEP 0: the substrate (from the package, present-tense) ---
L.append("STEP 0  SUBSTRATE (present-tense, from M02/M11)")
L.append("  facts: a thin basaltic skin (rho=2900) over a hot mantle near its unjamming")
L.append("         threshold (rho=3300, flows on long timescales); buoyant felsic (rho=2800)")
L.append("         exists as a distinct light phase.")
L.append("  [V] present-tense densities + rheology. (Origin of the first felsic = GAP, CG-12.)")
L.append("")

# --- STEP 1: opening forces antipodal closing (THE load-bearing entailment) ---
L.append("STEP 1  OPENING ENTAILS CLOSING  [FORCING: mass/area conservation on a fixed-area sphere]")
A_demo = 0.10 * A_SPHERE     # illustrative: an opening that grows to 10% of the surface
L.append(f"  the sphere's area is FIXED (rigid radius): A = 4*pi*R^2 = {A_SPHERE:.3e} m^2.")
L.append(f"  therefore any area OPENED must be exactly BALANCED by area CLOSED elsewhere:")
L.append(f"     dA_open + dA_close = 0   (identity, not a model).")
L.append(f"  e.g. an opening reaching {A_demo:.2e} m^2 (~10% of surface) FORCES {A_demo:.2e} m^2")
L.append(f"     of convergence on the complementary surface. This is NECESSARY, rate-free:")
for v in V_OPEN_CM_YR:
    L.append(f"       at {v:.0f} cm/yr opening, closing rate = {v:.0f} cm/yr (same area flux), independent of the value")
L.append("  GRADE: [F] forced by conservation. (WHERE the closing localizes = STEP 2.)")
L.append("")

# --- STEP 2: closing localizes by buoyancy gate (from CG-22/24, present-tense) ---
L.append("STEP 2  CLOSING IS ABSORBED BY THE SKIN, NOT THE RAFT  [FORCING: buoyancy gate, CG-22/24]")
L.append("  the convergence of STEP 1 meets two materials. Net buoyancy decides the response:")
L.append("    * negatively-buoyant basaltic skin -> sinks (subducts), absorbing convergence.")
L.append("    * positively-buoyant felsic raft  -> cannot sink -> is SWEPT/SHORTENED, not consumed.")
L.append("  => the skin is the conveyor that is destroyed; the felsic is the flotsam that is")
L.append("     carried toward, and PILED AT, the closing side. (Density-gated; M08/M10.)")
L.append("  GRADE: [F] buoyancy (present-tense). (HOW MUCH piles = depends on supply = GAP.)")
L.append("")

# --- STEP 3: a buoyant raft on a conveyor collects at the sink (kinematic necessity) ---
L.append("STEP 3  BUOYANT FLOTSAM COLLECTS AT THE SINK  [FORCING: kinematics of a non-subductable float on a subducting sheet]")
L.append("  a float that cannot follow the sheet down accumulates where the sheet descends --")
L.append("  exactly as non-wetting scum collects at a drain, NOT by attraction but because the")
L.append("  carrier leaves and the float cannot. => felsic concentrates on the CLOSING side =")
L.append("  ONE-SIDEDNESS is FORCED once an opening/closing pair exists.")
L.append("  GRADE: [F] kinematic necessity. (This is the load-bearing link to the asymmetry.)")
L.append("")

# --- STEP 4: collected rafts weld (this is where physics runs out) ---
L.append("STEP 4  COLLECTED RAFTS WELD INTO ONE MASS  [FORCING: incomplete -- GAP]")
L.append("  pure physics forces COLLECTION (STEP 3) but NOT clean welding into a single rigid")
L.append("  block: suturing, accretion, and the strength of the joins are MATERIAL/contingent.")
L.append("  -> FLAGGED GAP: 'they touch' is forced; 'they become one continent' is NOT forced by")
L.append("     conservation+buoyancy alone. Do NOT import geological assembly as if necessary.")
L.append("  GRADE: [O] -- collection [F], welding NOT entailed.")
L.append("")

# --- STEP 5: the assembly is provisional (reversibility, present-tense) ---
L.append("STEP 5  THE ASSEMBLY IS PROVISIONAL  [FORCING: the same conservation law, run either way]")
L.append("  the area identity (STEP 1) has no preferred direction: an opening can later become a")
L.append("  closing and vice-versa. So a one-sided pile is a STATE the law permits, NOT a")
L.append("  terminus. (This is why the present asymmetry is neutral/[O], not a fixed scar --")
L.append("  consistent with the M14 audit: permanent-vs-cyclic is [O] both ways.)")
L.append("  GRADE: [F] reversibility; [O] on which phase 'now' is.")
L.append("")

# --- what is forced vs flagged ---
L.append("="*64)
L.append("WHAT PURE PHYSICS FORCES (the assembled causal chain):")
L.append("  opening  =FORCED=>  antipodal closing            [F] conservation")
L.append("           =FORCED=>  skin subducts, raft cannot   [F] buoyancy")
L.append("           =FORCED=>  raft collects at the sink    [F] kinematics")
L.append("           => ONE-SIDED felsic mass is ENTAILED by an opening/closing pair.  [F]")
L.append("")
L.append("WHAT PHYSICS DOES NOT FORCE (flagged gaps -- geology NOT imported):")
L.append("  * the FIRST felsic (origin)                       [O]  CG-12/CG-20")
L.append("  * the trigger / why THIS opening                  [O]")
L.append("  * clean WELDING into one rigid continent          [O]  STEP 4")
L.append("  * any RATE, DURATION, ORDER, or DATE              [O]  RECORD both ways")
L.append("  * which phase (opening vs closing) is 'now'        [O]  STEP 5")
L.append("")
L.append("VERDICT (firewall-clean): an opening/closing pair on a fixed-area sphere, acting on a")
L.append("buoyancy-gated skin+raft system, FORCES a one-sided felsic concentration -- this much is")
L.append("pure physics [F], no geology, no clock. Everything historical (first seed, trigger,")
L.append("welding, rate, order) stays [O]. The chain is a DEPENDENCY graph, not a reconstruction.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "6ed0210a6abc59f3a7b888cdad8fcbe298bc0980acd81ce1373da0049af1c79a"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
