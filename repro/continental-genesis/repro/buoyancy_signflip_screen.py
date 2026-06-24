#!/usr/bin/env python3
"""
Continental-Genesis repro screen 6 -- buoyancy sign-flip & the CG-22 breaker test.
Author: Young Jae Lee - ORCID 0009-0002-7535-8245 - CC BY 4.0 - https://jamming-physics.org/
Governance: VP-SPEC - SEED=19, no-tuning, PRESENT-TENSE only; absolute ages RECORD both ways.

CG-22 (module 08) said: negative-buoyancy ocean skin sheds compression by subduction and stays
smooth; only positive-buoyancy felsic crust crumples. This screen TRIES TO BREAK that, as
promised, by (1) computing where oceanic lithosphere flips net-negative (half-space cooling),
and (2) honestly asking whether that sign-flip boundary IS the smooth/crumpled map boundary.

RESULT (firewall-honest): the sign-flip is the YOUNG-vs-OLD ocean boundary -- it does NOT map
onto the smooth/crumpled boundary, because crumpling is gated by felsic LOAD (ocean vs
continent), and BOTH young and old ocean lack that load. AND a real present-tense counter-case
(central Indian Ocean) shows negative-buoyancy ocean lithosphere CAN fold without subducting.
So CG-22 is DOWNGRADED from a law to a bounded tendency. falsification = discovery.
No absolute age is load-bearing: ages here are model inputs to a present-tense buoyancy state.
"""
import hashlib, math

SEED = 19

# ===== LOCK BLOCK (standard half-space-cooling & depth-age constants) =====
RHO_M   = 3300.0     # kg/m^3  hot mantle (reference)
RHO_CR  = 2900.0     # kg/m^3  oceanic crust
H_CR    = 7.0e3      # m       oceanic crust thickness
ALPHA   = 3.0e-5     # 1/K     thermal expansivity
DT_M    = 1350.0     # K       (T_mantle - T_surface)
KAPPA   = 1.0e-6     # m^2/s   thermal diffusivity
SEC_PER_MYR = 3.15576e13
D_RIDGE = 2500.0     # m       ridge-axis depth (depth-age relation)
D_COEF  = 350.0      # m/sqrt(Myr)  subsidence coefficient (GDH-style)
AGE_GRID_MA = [2, 5, 11, 20, 50, 80, 150]   # ages to tabulate the buoyancy state
# sensitivity band for the sign-flip (crust thickness, mantle dT)
SENS = [(6.0e3, 1400.0), (7.0e3, 1350.0), (8.0e3, 1300.0)]
# =========================================================================

B_CRUST = (RHO_M - RHO_CR) * H_CR              # constant positive buoyancy (kg/m^2)

def thermal_deficit(t_sec):                    # negative buoyancy from the cooled root
    return RHO_M * ALPHA * DT_M * 2.0 * math.sqrt(KAPPA * t_sec / math.pi)

def B_net(t_ma):                               # net buoyancy (kg/m^2), >0 floats
    return B_CRUST - thermal_deficit(t_ma * SEC_PER_MYR)

def t_star_ma(h_cr, dt_m):                     # sign-flip age (B=0), closed form
    bcr = (RHO_M - RHO_CR) * h_cr
    t_sec = math.pi * (bcr / (2.0 * RHO_M * ALPHA * dt_m))**2 / KAPPA
    return t_sec / SEC_PER_MYR

def depth(t_ma):
    return D_RIDGE + D_COEF * math.sqrt(t_ma)

t_star = t_star_ma(H_CR, DT_M)

L = []
L.append("BUOYANCY SIGN-FLIP & THE CG-22 BREAKER TEST")
L.append(f"VP-SPEC  SEED={SEED}  present-tense; ages are model inputs, RECORD")
L.append("="*64)
L.append("")
L.append("[1] net buoyancy of ocean lithosphere vs age (half-space cooling):")
L.append("      age      B_net          depth      sign / response-if-compressed")
for a in AGE_GRID_MA:
    b = B_net(a) / 1e6
    sign = "POS (resists subduction)" if b > 0 else "NEG (subductable)"
    L.append(f"     {a:4d} Ma   {b:7.2f} Mkg/m2   {depth(a):5.0f} m   {sign}")
L.append("")
L.append(f"    SIGN-FLIP at t* = {t_star:.1f} Ma  (depth ~ {depth(t_star):.0f} m)")
L.append("    sensitivity (crust km, dT K) -> t*:")
for h, dt in SENS:
    L.append(f"      h={h/1e3:.0f} km, dT={dt:.0f} K  ->  t* = {t_star_ma(h, dt):.1f} Ma")
L.append("    -> flip at ~10-30 Ma, a SMALL fraction of the ~180 Ma seafloor age range.")
L.append("    -> most of the deep Pacific floor is OLDER/DEEPER than t* => net-NEGATIVE.")
L.append("")
L.append("[2] does the sign-flip = the smooth/crumpled MAP boundary?  NO.")
L.append("    the sign-flip is the YOUNG-vs-OLD OCEAN boundary. But crumpling is gated by")
L.append("    felsic LOAD (ocean vs continent), and BOTH young AND old ocean lack felsic")
L.append("    load -> NEITHER crumples into thick relief. So the originally-proposed test")
L.append("    (sign-flip boundary vs smooth/crumpled boundary) MIS-MAPS: they are different")
L.append("    axes. The smooth/crumpled boundary is the OCEAN/CONTINENT (load) boundary (M08),")
L.append("    not the ocean buoyancy-sign boundary. Stating this honestly is the result.")
L.append("")
L.append("[3] the real BREAKER for CG-22 (present-tense [V] counter-case):")
L.append("    CENTRAL INDIAN OCEAN -- old (~50-80 Ma, net-NEGATIVE) oceanic lithosphere is")
L.append("    FOLDING under intraplate compression WITHOUT subducting: long-wavelength")
L.append("    lithospheric folds (~100-300 km), gravity/geoid undulations, reverse faulting,")
L.append("    large intraplate earthquakes. => negative-buoyancy bare skin CAN deform; it does")
L.append("    NOT always shed compression by subduction. CG-22's absolute form is FALSIFIED.")
L.append("")
L.append("[4] bounded, surviving claim (the honest refinement):")
L.append("    * THICK crumpling (mountain-scale relief) remains gated to felsic-loaded")
L.append("      (positive-buoyancy) crust -- this SURVIVES (no bare-ocean mountain belts).")
L.append("    * bare ocean skin under compression EITHER subducts (if a zone is available) OR,")
L.append("      where it cannot, folds only into LONG-wavelength, LOW-amplitude undulations")
L.append("      (central Indian Ocean) -- never thick relief (it is thin; M04 buckling).")
L.append("    => CG-22 DOWNGRADED: [F] law  ->  [L] bounded tendency, with a logged exception.")
L.append("")
L.append("VERDICT (firewall-clean): the proposed test did its job and BROKE the strong form.")
L.append("  the gate is a tendency, not a law; the thick-crumpling-needs-felsic-load core holds.")
L.append("  rate/when stays [O] both ways. falsification = discovery.")

body = "\n".join(L)
print(body)
h1 = hashlib.sha256(body.encode("utf-8")).hexdigest()
h2 = hashlib.sha256(h1.encode("utf-8")).hexdigest()
print()
print(f"2xSHA256 = {h2}")
EXPECT = "a51a6693b515ed48cdee49da8ddcfa1b8640fd1281b4458de79588e800f2ee1e"
assert h2 == EXPECT, f"REPRO GATE: FAIL (got {h2})"
print("REPRO GATE: PASS")
